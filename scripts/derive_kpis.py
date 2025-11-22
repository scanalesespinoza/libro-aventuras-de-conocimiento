#!/usr/bin/env python3
"""Deriva KPIs a partir de datos procesados y exporta tablas a `reports/tables/`.

El script toma como entrada `data/processed/topics.csv` y genera tablas
resumen en formato CSV y Markdown para alimentar el manuscrito.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

import pandas as pd

DATA_PATH = Path("data/processed/topics.csv")
OUTPUT_DIR = Path("reports/tables")
EXPECTED_COLUMNS = [
    "repo",
    "time_bucket",
    "dominant_topic",
    "topic_score",
    "text_count",
    "source_breakdown",
]


def write_markdown_table(df: pd.DataFrame, path: Path) -> None:
    """Escribe una tabla Markdown simple sin depender de librerías extra."""
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in df.itertuples(index=False):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_table(df: pd.DataFrame, name: str) -> None:
    """Exporta una tabla en CSV y Markdown dentro de OUTPUT_DIR."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / f"{name}.csv"
    md_path = OUTPUT_DIR / f"{name}.md"
    df.to_csv(csv_path, index=False)
    write_markdown_table(df, md_path)


def parse_source_breakdown(series: Iterable[str]) -> pd.DataFrame:
    """Agrega los conteos declarados en la columna `source_breakdown`."""
    counts: dict[str, int] = {}
    for entry in series:
        if not isinstance(entry, str):
            continue
        for raw_pair in entry.split(","):
            if ":" not in raw_pair:
                continue
            key, value = raw_pair.split(":", maxsplit=1)
            key = key.strip()
            try:
                counts[key] = counts.get(key, 0) + int(value.strip())
            except ValueError:
                continue
    data = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return pd.DataFrame(data, columns=["fuente", "textos"])


def build_summary(topics: pd.DataFrame) -> pd.DataFrame:
    """Construye KPI de alto nivel para el corpus procesado."""
    avg_score = round(float(topics["topic_score"].mean()), 2)
    summary_rows = [
        {
            "kpi": "Repos observados",
            "valor": str(int(topics["repo"].nunique())),
            "detalle": "Repositorios con textos clasificados",
        },
        {
            "kpi": "Ventanas temporales",
            "valor": str(int(topics["time_bucket"].nunique())),
            "detalle": "Buckets (mes o semana) presentes en el set procesado",
        },
        {
            "kpi": "Textos clasificados",
            "valor": str(int(topics["text_count"].sum())),
            "detalle": "Total de textos usados para clasificación",
        },
        {
            "kpi": "Temas dominantes",
            "valor": str(topics["dominant_topic"].nunique()),
            "detalle": "Número de temas asignados como dominantes",
        },
        {
            "kpi": "Puntaje promedio de tema",
            "valor": f"{avg_score:.2f}",
            "detalle": "Confianza promedio en la clasificación de tópicos",
        },
    ]
    return pd.DataFrame(summary_rows)


def group_by_topic(topics: pd.DataFrame) -> pd.DataFrame:
    """Agrega textos y puntajes por tema dominante."""
    grouped = (
        topics.groupby("dominant_topic", as_index=False)
        .agg(
            textos=("text_count", "sum"),
            puntaje_promedio=("topic_score", "mean"),
        )
        .sort_values(by=["textos"], ascending=False)
    )
    grouped["puntaje_promedio"] = grouped["puntaje_promedio"].round(2)
    return grouped


def group_by_period(topics: pd.DataFrame) -> pd.DataFrame:
    """Agrega textos y puntajes por periodo temporal y tema."""
    aggregated = (
        topics.groupby(["time_bucket", "dominant_topic"], as_index=False)
        .agg(
            textos=("text_count", "sum"),
            puntaje_promedio=("topic_score", "mean"),
        )
        .sort_values(by=["time_bucket", "textos"], ascending=[True, False])
    )
    aggregated["puntaje_promedio"] = aggregated["puntaje_promedio"].round(2)
    return aggregated


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {DATA_PATH}")

    rows: list[dict[str, str]] = []
    with DATA_PATH.open() as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            extras = row.pop(None, [])
            breakdown = row.get("source_breakdown", "") or ""
            if extras:
                breakdown = ",".join(filter(None, [breakdown, *extras]))
            row["source_breakdown"] = breakdown
            rows.append(row)

    topics = pd.DataFrame(rows, columns=EXPECTED_COLUMNS)
    topics["topic_score"] = topics["topic_score"].astype(float)
    topics["text_count"] = topics["text_count"].astype(int)

    summary_df = build_summary(topics)
    export_table(summary_df, "kpis_resumen")

    source_df = parse_source_breakdown(topics["source_breakdown"].tolist())
    export_table(source_df, "textos_por_fuente")

    topic_df = group_by_topic(topics)
    export_table(topic_df, "textos_por_tema")

    period_df = group_by_period(topics)
    export_table(period_df, "textos_por_periodo")


if __name__ == "__main__":
    main()
