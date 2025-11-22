# Guiones breves para casos de estudio

## Caso 1: Cartografía de fuentes y datos (Capítulo 1)
- **0:00–0:20.** Presenta el contexto: un corpus inicial de 13 textos clasificados en la ventana 2025-11, todos provenientes del mismo repositorio. Refuerza que se usó el pipeline `tools/repo_harvester.py` + `scripts/clean_data.py` para obtener la muestra.
- **0:20–0:45.** Menciona los KPIs: puntaje promedio de confianza en tópicos de **6.62** y un único repositorio como fuente. Enfatiza que el set es compacto pero bien etiquetado.
- **0:45–1:15.** Desglosa la procedencia: **85 %** de los textos vienen de commits y el resto de documentación, lo que confirma que la narrativa de desarrollo sostiene la evidencia. Aclara que los informes se apoyan en las Tablas 1 y 2 de `reports/tables/`.
- **1:15–1:40.** Cierra con el valor narrativo: este mapeo inicial sirve como línea base para seguir cómo evoluciona el corpus y qué tan confiables son las etiquetas a medida que se sumen nuevas ventanas temporales.

## Caso 2: Propósito y alcance (Capítulo 2)
- **0:00–0:20.** Introduce la idea central: la evidencia se concentra en **automatización y herramientas**, que cubren el **100 %** de los textos clasificados en la ventana 2025-11.
- **0:20–0:45.** Repite el tamaño del corpus (13 textos) y la confianza promedio de **6.62**, destacando que la clasificación es consistente con el pipeline de temas mencionado en el capítulo anterior.
- **0:45–1:15.** Explica que el único bucket temporal (2025-11) será la base para contrastar variaciones futuras cuando ingresen más periodos; las Tablas 3 y 4 mostrarán cómo cambia la proporción de temas.
- **1:15–1:45.** Concluye señalando que el foco en automatización refleja el propósito del libro: documentar experimentación sostenida con pipelines y utilidades, y que los próximos cortes permitirán medir el alcance longitudinal del proyecto.
