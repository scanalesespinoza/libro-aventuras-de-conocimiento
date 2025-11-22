from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import pathlib
import re
import subprocess
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


@dataclasses.dataclass(frozen=True)
class Topic:
    name: str
    keywords: Sequence[str]
    seed_phrases: Sequence[str]


@dataclasses.dataclass
class TextRecord:
    repo: str
    time_bucket: str
    source: str
    text: str


@dataclasses.dataclass
class ScoredRecord(TextRecord):
    topic: str
    score: float


DEFAULT_TOPICS: Tuple[Topic, ...] = (
    Topic(
        name="documentacion",
        keywords=(
            "documentacion",
            "readme",
            "manual",
            "guia",
            "documento",
            "escribir",
            "redaccion",
        ),
        seed_phrases=(
            "documentacion del proyecto",
            "notas y guias para usuarios",
            "actualizar el readme",
        ),
    ),
    Topic(
        name="datos",
        keywords=(
            "datos",
            "dataset",
            "csv",
            "parquet",
            "etl",
            "limpieza",
            "procesamiento",
        ),
        seed_phrases=(
            "procesamiento de datos",
            "pipeline de datos",
            "normalizar datasets",
        ),
    ),
    Topic(
        name="automatizacion_y_herramientas",
        keywords=(
            "script",
            "automatizacion",
            "pipeline",
            "workflow",
            "herramienta",
            "cli",
            "robot",
        ),
        seed_phrases=(
            "scripts de automatizacion",
            "herramientas para tareas repetitivas",
            "mejorar el flujo de trabajo",
        ),
    ),
    Topic(
        name="ia_y_modelado",
        keywords=(
            "ia",
            "ml",
            "modelo",
            "embedding",
            "clasificacion",
            "llm",
            "inteligencia",
        ),
        seed_phrases=(
            "experimentos con modelos",
            "aplicaciones de inteligencia artificial",
            "modelo de lenguaje",
        ),
    ),
    Topic(
        name="infraestructura",
        keywords=(
            "infraestructura",
            "deploy",
            "docker",
            "kubernetes",
            "cloud",
            "aws",
            "gcp",
        ),
        seed_phrases=(
            "infraestructura en la nube",
            "despliegues y contenedores",
            "configuracion de servidores",
        ),
    ),
    Topic(
        name="gestion_de_proyecto",
        keywords=(
            "plan",
            "roadmap",
            "gestion",
            "organizacion",
            "reunion",
            "coordinacion",
            "issue",
        ),
        seed_phrases=(
            "planificacion del proyecto",
            "seguimiento de tareas",
            "organizar entregables",
        ),
    ),
)


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-záéíóúüñ]+", text.lower())


def normalize_counter(counter: Counter[str]) -> Dict[str, float]:
    norm = sum(value * value for value in counter.values()) ** 0.5
    if not norm:
        return {}
    return {key: value / norm for key, value in counter.items()}


def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    keys = vec_a.keys() & vec_b.keys()
    return sum(vec_a[key] * vec_b[key] for key in keys)


def build_topic_vectors(topics: Sequence[Topic]) -> Dict[str, Dict[str, float]]:
    vectors: Dict[str, Dict[str, float]] = {}
    for topic in topics:
        tokens = tokenize(" ".join((*topic.keywords, *topic.seed_phrases)))
        vectors[topic.name] = normalize_counter(Counter(tokens))
    return vectors


def keyword_score(tokens: Counter[str], keywords: Sequence[str]) -> float:
    score = 0.0
    for keyword in keywords:
        score += tokens.get(keyword.lower(), 0)
    return score


def classify_text(text: str, topic_vectors: Dict[str, Dict[str, float]], topics: Sequence[Topic]) -> Tuple[str, float]:
    tokens = tokenize(text)
    token_counts = Counter(tokens)
    normalized = normalize_counter(token_counts)

    best_topic = "otros"
    best_score = -1.0

    for topic in topics:
        kw_score = keyword_score(token_counts, topic.keywords)
        similarity = cosine_similarity(normalized, topic_vectors.get(topic.name, {}))
        combined = kw_score * 1.5 + similarity
        if combined > best_score:
            best_topic = topic.name
            best_score = combined

    if best_score <= 0:
        return "otros", 0.0
    return best_topic, best_score


def read_git_log(repo_path: pathlib.Path) -> List[TextRecord]:
    if not (repo_path / ".git").exists():
        return []

    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        "--pretty=format:%H|%cI|%s",
    ]
    output = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="ignore")
    records: List[TextRecord] = []
    for line in output.splitlines():
        if "|" not in line:
            continue
        sha, timestamp, subject = line.split("|", maxsplit=2)
        bucket = timestamp[:7]
        records.append(
            TextRecord(
                repo=repo_path.name,
                time_bucket=bucket,
                source="commit",
                text=subject.strip(),
            )
        )
    return records


def last_commit_date(repo_path: pathlib.Path, file_path: pathlib.Path) -> Optional[str]:
    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        "-1",
        "--format=%cI",
        "--",
        str(file_path.relative_to(repo_path)),
    ]
    try:
        output = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="ignore").strip()
        if output:
            return output
    except subprocess.CalledProcessError:
        return None
    return None


def read_readmes(repo_path: pathlib.Path) -> List[TextRecord]:
    records: List[TextRecord] = []
    for readme_path in repo_path.rglob("README.md"):
        if ".git" in readme_path.parts:
            continue
        try:
            text = readme_path.read_text(encoding="utf-8")
        except OSError:
            continue
        timestamp = last_commit_date(repo_path, readme_path)
        bucket = (timestamp or dt.datetime.utcnow().isoformat())[:7]
        records.append(
            TextRecord(
                repo=repo_path.name,
                time_bucket=bucket,
                source="readme",
                text=text,
            )
        )
    return records


def read_issues_csv(path: pathlib.Path, repo: str) -> List[TextRecord]:
    if not path.exists():
        return []
    records: List[TextRecord] = []
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - fallback path
        raise SystemExit("pandas es necesario para leer issues en CSV") from exc

    df = pd.read_csv(path)
    title_col = "title" if "title" in df.columns else None
    date_col = "created_at" if "created_at" in df.columns else None
    if not title_col:
        return []
    for _, row in df.iterrows():
        text = str(row[title_col])
        if not text.strip():
            continue
        timestamp = str(row[date_col]) if date_col and not pd.isna(row[date_col]) else dt.datetime.utcnow().isoformat()
        bucket = timestamp[:7]
        records.append(
            TextRecord(
                repo=repo,
                time_bucket=bucket,
                source="issue",
                text=text,
            )
        )
    return records


def aggregate_records(records: Iterable[ScoredRecord]) -> List[Dict[str, object]]:
    grouped: Dict[Tuple[str, str], Dict[str, object]] = {}

    for record in records:
        key = (record.repo, record.time_bucket)
        if key not in grouped:
            grouped[key] = {
                "repo": record.repo,
                "time_bucket": record.time_bucket,
                "topic_scores": defaultdict(float),
                "sources": defaultdict(int),
                "text_count": 0,
            }
        entry = grouped[key]
        entry["topic_scores"][record.topic] += record.score
        entry["sources"][record.source] += 1
        entry["text_count"] += 1

    rows: List[Dict[str, object]] = []
    for key, entry in grouped.items():
        topic_scores: Dict[str, float] = entry["topic_scores"]
        if topic_scores:
            dominant = max(topic_scores.items(), key=lambda item: item[1])
            dominant_topic, dominant_score = dominant
        else:
            dominant_topic, dominant_score = "otros", 0.0

        rows.append(
            {
                "repo": entry["repo"],
                "time_bucket": entry["time_bucket"],
                "dominant_topic": dominant_topic,
                "topic_score": round(dominant_score, 3),
                "text_count": entry["text_count"],
                "source_breakdown": ",".join(
                    f"{source}:{count}" for source, count in sorted(entry["sources"].items())
                ),
            }
        )
    rows.sort(key=lambda row: (row["repo"], row["time_bucket"]))
    return rows


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clasifica textos y genera temas dominantes por repositorio y mes.")
    parser.add_argument(
        "--repo",
        type=pathlib.Path,
        default=pathlib.Path("."),
        help="Ruta al repositorio a analizar.",
    )
    parser.add_argument(
        "--issues-file",
        type=pathlib.Path,
        help="Archivo CSV opcional con issues. Debe contener columnas title y created_at.",
    )
    parser.add_argument(
        "--output-file",
        type=pathlib.Path,
        default=pathlib.Path("data/processed/topics.csv"),
        help="Ruta de salida para la tabla de temas.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    repo_path = args.repo.resolve()

    topic_vectors = build_topic_vectors(DEFAULT_TOPICS)

    records: List[TextRecord] = []
    records.extend(read_git_log(repo_path))
    records.extend(read_readmes(repo_path))
    if args.issues_file:
        records.extend(read_issues_csv(args.issues_file, repo_path.name))

    scored: List[ScoredRecord] = []
    for record in records:
        topic, score = classify_text(record.text, topic_vectors, DEFAULT_TOPICS)
        scored.append(
            ScoredRecord(
                repo=record.repo,
                time_bucket=record.time_bucket,
                source=record.source,
                text=record.text,
                topic=topic,
                score=score,
            )
        )

    rows = aggregate_records(scored)
    output_path = args.output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    header = "repo,time_bucket,dominant_topic,topic_score,text_count,source_breakdown"
    lines = [header]
    for row in rows:
        line = ",".join(
            [
                str(row["repo"]),
                str(row["time_bucket"]),
                str(row["dominant_topic"]),
                str(row["topic_score"]),
                str(row["text_count"]),
                str(row["source_breakdown"]),
            ]
        )
        lines.append(line)

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
