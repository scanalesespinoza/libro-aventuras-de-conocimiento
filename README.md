# Aventuras de conocimiento

Repositorio del libro *Aventuras de conocimiento*, centrado en experiencias con tecnología e inteligencia artificial. Aquí se documenta el proceso de escritura, las iteraciones del prólogo y la organización de capítulos futuros.

## Estructura

- `libro/`: manuscrito y material editorial.
  - `prologo/`: prólogo completo, ideas centrales, frase resumen y descripción del tipo de libro.
  - `capitulos/` (por crear): capítulos principales y sus borradores.
  - `anexos/` (por crear): glosarios, referencias y guías complementarias.
- `tools/`: utilidades para recolectar historial de repositorios.
- `scripts/clean_data.py`: normalización de commits (fechas a UTC, merges y agrupación de autores) con salida en `data/processed/`.

## Datos y limpieza

1. Recolecta commits con `tools/repo_harvester.py`, que deja archivos en `data/raw/`.
2. Ejecuta el limpiador para generar la vista consolidada y en UTC:

   ```bash
   python scripts/clean_data.py --input-dir data/raw --output-dir data/processed --author-map data/alias.csv
   ```

## Objetivo

Capturar el camino de trabajo con IA: intentos, errores, ajustes y aprendizajes. El enfoque es ofrecer un testimonio transparente que pueda servir a quienes viven retos similares en software, nube y comunidades open source.
