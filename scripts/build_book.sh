#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="${DOCS_DIR:-${ROOT_DIR}/docs}"
REPORTS_DIR="${REPORTS_DIR:-${ROOT_DIR}/reports}"
BUILD_DIR="${BUILD_DIR:-${DOCS_DIR}/build}"
ASSETS_DIR="${ASSETS_DIR:-${BUILD_DIR}/assets}"
DEFAULTS_COMMON="${DOCS_DIR}/pandoc-common.yaml"
DEFAULTS_PDF="${DOCS_DIR}/pandoc-pdf.yaml"
DEFAULTS_EPUB="${DOCS_DIR}/pandoc-epub.yaml"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Pandoc no está instalado. Instálalo para compilar el libro." >&2
  exit 1
fi

mkdir -p "${BUILD_DIR}" "${ASSETS_DIR}"

if [[ -d "${REPORTS_DIR}" ]]; then
  while IFS= read -r -d '' src; do
    rel="${src#${REPORTS_DIR}/}"
    dest="${ASSETS_DIR}/${rel}"
    mkdir -p "$(dirname "${dest}")"
    cp "${src}" "${dest}"
  done < <(find "${REPORTS_DIR}" -type f \( \
    -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o \
    -iname '*.svg' -o -iname '*.pdf' -o -iname '*.csv' -o \
    -iname '*.tsv' \
  \) -print0)
fi

mapfile -t sources < <(find "${DOCS_DIR}" -maxdepth 1 -name '*.md' -print | sort)
if [[ ${#sources[@]} -eq 0 ]]; then
  echo "No hay archivos Markdown en ${DOCS_DIR}." >&2
  exit 1
fi

BOOK_DATE="${BOOK_DATE:-$(date +%Y-%m-%d)}"
PANDOC_FLAGS=(
  --defaults "${DEFAULTS_COMMON}"
  --metadata date="${BOOK_DATE}"
)

pandoc "${PANDOC_FLAGS[@]}" --defaults "${DEFAULTS_PDF}" "${sources[@]}" \
  -o "${BUILD_DIR}/libro-aventuras-de-conocimiento.pdf"

pandoc "${PANDOC_FLAGS[@]}" --defaults "${DEFAULTS_EPUB}" "${sources[@]}" \
  -o "${BUILD_DIR}/libro-aventuras-de-conocimiento.epub"

echo "PDF y EPUB generados en ${BUILD_DIR}."
