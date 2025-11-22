# Esquema narrativo y vínculos de evidencia

## Acto I: Preparar el terreno

### Capítulo 1: Cartografía de fuentes y datos
- **Métricas y gráficas**: [Actividad semanal de commits por repositorio](../reports/figures/actividad-semanal.png) generada con `tools/repo_harvester.py` y depurada con `scripts/clean_data.py` para poblar `data/processed/topics.csv`.
- **Repos y commits de referencia**:
  - `libro-aventuras-de-conocimiento@5c85310`: incorporación del recolector de repositorios.
  - `libro-aventuras-de-conocimiento@c5c9a12`: limpiador de commits para normalizar zonas horarias y merges.
- **Citas clave para la narración**:
  - > "Repositorio del libro *Aventuras de conocimiento*, centrado en experiencias con tecnología e inteligencia artificial." (README)
  - > "Este libro reúne años de trabajo, intentos, errores y experimentos con tecnología e inteligencia artificial." (Prólogo)

### Capítulo 2: Propósito y alcance
- **Métricas y gráficas**: [Distribución de temas por mes](../reports/figures/temas-por-mes.png) tomando como insumo `data/processed/topics.csv` y el pipeline de clasificación de tópicos.
- **Repos y commits de referencia**:
  - `libro-aventuras-de-conocimiento@135b929`: pipeline de clasificación de temas.
  - `libro-aventuras-de-conocimiento@a87faa3`: integración de extracción de textos y clasificación en el flujo principal.
- **Citas clave para la narración**:
  - > "Capturar el camino de trabajo con IA: intentos, errores, ajustes y aprendizajes." (README)
  - > "El contenido que sigue se ha formado a partir de conversaciones... y una gran cantidad de borradores que fueron descartados o reformulados." (Prólogo)

## Acto II: Pruebas, tropiezos y ajustes

### Capítulo 3: Ritmos de trabajo y desgaste
- **Métricas y gráficas**: [Curva de actividad y pausas](../reports/figures/tiempo-entre-commits.png) derivada del notebook `notebooks/analysis.ipynb`, resaltando periodos de baja frecuencia.
- **Repos y commits de referencia**:
  - `libro-aventuras-de-conocimiento@f0c3301`: notebook inicial para métricas de actividad.
  - `libro-aventuras-de-conocimiento@05a5cdc`: métricas agregadas y gráficos incorporados al pipeline.
- **Citas clave para la narración**:
  - > "En ese entorno, los cambios son rápidos, las expectativas son altas y el volumen de información es grande... aparece el cansancio y la sensación de no llegar a todo." (Prólogo)
  - > "El camino no ha estado libre de dificultades... algunos firmes y otros dubitativos." (Prólogo)

### Capítulo 4: IA como copiloto de iteraciones
- **Métricas y gráficas**: [Comparativa de iteraciones asistidas vs. manuales](../reports/figures/iteraciones-ia-vs-manuales.png) construida a partir de los logs de generación en `data/raw/` y las versiones depuradas en `data/processed/`.
- **Repos y commits de referencia**:
  - `libro-aventuras-de-conocimiento@1c27c31`: configuración de revisión lingüística automática (indicador de apoyo asistido).
  - `libro-aventuras-de-conocimiento@9f2dd77`: acción de ortografía que evidencia el cuidado editorial temprano.
- **Citas clave para la narración**:
  - > "La IA ayudó a proponer estructuras, aclarar formulaciones, ordenar información y ofrecer alternativas." (Prólogo)
  - > "Lo que sí cambió fue la distribución de ese esfuerzo..." (Prólogo)

## Acto III: Sistematización y difusión

### Capítulo 5: Estándares, repos y trazabilidad
- **Métricas y gráficas**: [Mapa de repositorios y dependencias](../reports/figures/mapa-repos-dependencias.png) acompañado de tabla de commits clave y cambios de versión.
- **Repos y commits de referencia**:
  - `libro-aventuras-de-conocimiento@444d52a`: incorporación de scripts bilingües para análisis (Go/Python).
  - `libro-aventuras-de-conocimiento@f53f63a`: integración de transformación de datos (punto de control para etiquetar versión v0.1 narrativa).
- **Citas clave para la narración**:
  - > "La organización busca separar el prólogo, las ideas principales y las futuras secciones del libro para facilitar su desarrollo incremental." (Estructura del libro)
  - > "Cada texto que aparece aquí pasó por varias versiones." (Prólogo)

### Capítulo 6: Aprendizajes y próximos experimentos
- **Métricas y gráficas**: [Línea de tiempo de hallazgos y backlog](../reports/figures/timeline-aprendizajes.png) con marcas de commits y tareas pendientes.
- **Repos y commits de referencia**:
  - `libro-aventuras-de-conocimiento@a87faa3`: consolidación de extracción y clasificación como cierre de ciclo.
  - Propuesta de tag `v0.1-hitos-ia` al publicar la primera versión completa del esquema y métricas.
- **Citas clave para la narración**:
  - > "Si de este relato surge alguna idea aplicable, alguna pregunta nueva o simplemente una sensación de compañía... el esfuerzo habrá cumplido su propósito." (Prólogo)
  - > "Establecer una convención para versiones y revisiones de cada texto." (Estructura del libro)
