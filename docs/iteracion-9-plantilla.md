# Plantilla de tarea – Iteración 9

Usa esta plantilla para redactar cualquier capítulo futuro (cap-03, cap-04, etc.). Sustituye {CAP_ID} por el identificador real del capítulo.

## Task – Redactar el capítulo {CAP_ID} del libro

**Entradas:**
- data/contexto-autor.md
- docs/instrucciones-redaccion.md
- data/fichas-documentales.yml
- data/lineas-narrativas.yml
- data/indice-libro.yml
- data/esquema-capitulos.yml

### Pasos previos
1. Leer `data/contexto-autor.md` para entender el perfil, los principios y el estilo del autor.
2. Leer `docs/instrucciones-redaccion.md` y seguir estrictamente esas reglas de redacción.
3. En `data/indice-libro.yml`, localizar el capítulo con id = {CAP_ID}: título, línea narrativa asociada y `repositorios_clave`.
4. En `data/esquema-capitulos.yml`, localizar la entrada de {CAP_ID} y su lista de secciones.
5. En `data/fichas-documentales.yml`, leer las fichas de los `repositorios_clave`.
6. En `data/lineas-narrativas.yml`, leer la línea narrativa asociada al capítulo.

### Objetivo
Redactar el capítulo {CAP_ID} en formato Markdown, siguiendo el estilo descrito en `contexto-autor.md` y el proceso definido en `instrucciones-redaccion.md`, respetando la estructura de secciones definida en `esquema-capitulos.yml`.

### Instrucciones de redacción
- Tono serio, tranquilo y lógico.
- Lenguaje claro y directo.
- Describir hechos, contexto, decisiones y aprendizajes observables.
- No imponer juicios de valor ("esto está bien/mal", "así se debe hacer").
- No centrar el texto en el “yo” ni en logros personales; el foco está en el proceso y los proyectos.
- No usar lenguaje poético ni exagerado.
- Mostrar dificultades y esfuerzo sin victimización ni dramatización.

### Formato de salida
- Markdown.
- Encabezado de nivel 2 para el capítulo, por ejemplo: `## {título del capítulo}`.
- Para cada sección definida en `esquema-capitulos.yml` para {CAP_ID}:
  - Encabezado de nivel 3 con el título de la sección.
  - Entre 3 y 7 párrafos que desarrollen esa sección, usando como base las fichas documentales y la línea narrativa.

### Salida
Devolver solo el contenido del capítulo en Markdown, listo para guardarse como `manuscrito/{CAP_ID}.md`.
