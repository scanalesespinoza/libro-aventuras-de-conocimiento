from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import logging
import pathlib
from typing import Iterable, List, Optional

import pandas as pd


@dataclasses.dataclass
class AuthorAlias:
    canonical: str
    email: Optional[str] = None
    name: Optional[str] = None


PYARROW_AVAILABLE = importlib.util.find_spec("pyarrow") is not None


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Limpia datos de commits y los normaliza para análisis.")
    parser.add_argument(
        "--input-dir",
        type=pathlib.Path,
        default=pathlib.Path("data/raw"),
        help="Directorio con archivos CSV o Parquet generados por el recolector.",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=pathlib.Path("data/processed"),
        help="Directorio donde se guardarán los archivos procesados.",
    )
    parser.add_argument(
        "--author-map",
        type=pathlib.Path,
        help="Archivo CSV opcional con columnas canonical,email,name para agrupar identidades de autor.",
    )
    parser.add_argument(
        "--skip-parquet",
        action="store_true",
        help="No escribir salida en formato Parquet.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Nivel de detalle para los logs.",
    )
    return parser.parse_args(argv)


def load_author_aliases(path: Optional[pathlib.Path]) -> List[AuthorAlias]:
    if not path:
        return []
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de alias: {path}")

    df = pd.read_csv(path)
    if "canonical" not in df.columns:
        raise ValueError("El archivo de alias debe tener una columna 'canonical'.")

    aliases: List[AuthorAlias] = []
    for _, row in df.iterrows():
        aliases.append(
            AuthorAlias(
                canonical=str(row.get("canonical", "")).strip(),
                email=str(row.get("email", "")).strip() or None,
                name=str(row.get("name", "")).strip() or None,
            )
        )
    return aliases


def load_commits(input_dir: pathlib.Path) -> pd.DataFrame:
    if not input_dir.exists():
        raise FileNotFoundError(f"No existe el directorio de entrada: {input_dir}")

    frames: List[pd.DataFrame] = []
    for csv_file in sorted(input_dir.glob("*.csv")):
        logging.info("Cargando %s", csv_file)
        frames.append(pd.read_csv(csv_file))

    parquet_files = sorted(input_dir.glob("*.parquet"))
    if parquet_files and not PYARROW_AVAILABLE:
        raise ImportError("pyarrow es necesario para leer archivos Parquet de entrada.")

    for parquet_file in parquet_files:
        logging.info("Cargando %s", parquet_file)
        frames.append(pd.read_parquet(parquet_file))

    if not frames:
        raise FileNotFoundError(f"No se encontraron CSV o Parquet en {input_dir}")

    return pd.concat(frames, ignore_index=True)


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    timestamps = pd.to_datetime(df["authored_at"], errors="coerce", utc=True)
    df = df.copy()
    df["authored_at_utc"] = timestamps.dt.tz_convert("UTC")
    df["authored_at_utc_iso"] = df["authored_at_utc"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return df


def mark_merges(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["insertions"] = pd.to_numeric(df["insertions"], errors="coerce")
    df["deletions"] = pd.to_numeric(df["deletions"], errors="coerce")
    df["is_merge"] = df["subject"].str.startswith("Merge", na=False)
    df["effective_insertions"] = df["insertions"].where(~df["is_merge"], other=0)
    df["effective_deletions"] = df["deletions"].where(~df["is_merge"], other=0)
    df["effective_loc"] = df["effective_insertions"].fillna(0) + df["effective_deletions"].fillna(0)
    return df


def build_author_lookup(aliases: Iterable[AuthorAlias]) -> List[AuthorAlias]:
    filtered = [alias for alias in aliases if alias.canonical]
    logging.debug("Alias activos: %d", len(filtered))
    return filtered


def normalize_author(row: pd.Series, lookup: List[AuthorAlias]) -> str:
    name = str(row.get("author_name", "")).strip()
    email = str(row.get("author_email", "")).strip()

    for alias in lookup:
        if alias.email and email.lower() == alias.email.lower():
            return alias.canonical
        if alias.name and name.lower() == alias.name.lower():
            return alias.canonical

    if email:
        return email.lower()
    if name:
        return name.lower()
    return "desconocido"


def group_authors(df: pd.DataFrame, aliases: List[AuthorAlias]) -> pd.DataFrame:
    df = df.copy()
    lookup = build_author_lookup(aliases)
    df["canonical_author"] = df.apply(lambda row: normalize_author(row, lookup), axis=1)
    return df


def write_outputs(df: pd.DataFrame, output_dir: pathlib.Path, skip_parquet: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "commits_clean.csv"
    df.to_csv(csv_path, index=False)
    logging.info("Archivo CSV guardado en %s", csv_path)

    if skip_parquet:
        logging.info("Omitiendo Parquet por configuración.")
        return

    if not PYARROW_AVAILABLE:
        logging.warning("pyarrow no está disponible; no se generará Parquet.")
        return

    parquet_path = output_dir / "commits_clean.parquet"
    df.to_parquet(parquet_path, index=False)
    logging.info("Archivo Parquet guardado en %s", parquet_path)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level), format="[%(levelname)s] %(message)s")

    aliases = load_author_aliases(args.author_map)
    commits = load_commits(args.input_dir)

    logging.info("Normalizando fechas a UTC")
    commits = normalize_dates(commits)

    logging.info("Marcando merges y descontando LOC efectivos")
    commits = mark_merges(commits)

    logging.info("Agrupando identidades de autor")
    commits = group_authors(commits, aliases)

    write_outputs(commits, args.output_dir, args.skip_parquet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
