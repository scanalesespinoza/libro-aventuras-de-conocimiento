# Instrucciones de redacción con contexto de autor

Este documento concentra las pautas para redactar capítulos y el prólogo del libro usando el archivo `data/contexto-autor.md` como referencia obligatoria.

## Propósito de `data/contexto-autor.md`

- Define quién habla: perfil, trayectoria y focos (cloud native, plataformas, comunidad).
- Define desde dónde habla: principios de trabajo y uso de IA como apoyo.
- Define cómo debe sonar el libro: tono serio y tranquilo, sin juicios de valor ni victimización.

Mientras este archivo exista y se mantenga estable, no hace falta volver a explicar el estilo en cada tarea: basta con leerlo y respetarlo.

## Plantilla para redacción de capítulos

**Task – Redactar el capítulo `{CAP_ID}` del libro**

Entradas:
- `data/contexto-autor.md`
- `data/fichas-documentales.yml`
- `data/lineas-narrativas.yml`
- `data/indice-libro.yml`
- `data/esquema-capitulos.yml`

Objetivo:
Escribir el texto completo del capítulo `{CAP_ID}`, siguiendo el esquema definido para ese capítulo y el estilo narrativo descrito en `data/contexto-autor.md`.

Pasos previos:
1. Leer por completo `data/contexto-autor.md` y tomarlo como referencia de tono, forma de relatar y principios de trabajo.
2. Mantener ese estilo en todo el texto del capítulo.

Instrucciones de contenido:
1. Localizar en `data/indice-libro.yml` el capítulo con id = `{CAP_ID}`: título, línea narrativa asociada, `repositorios_clave`.
2. En `data/esquema-capitulos.yml`, buscar la entrada de `{CAP_ID}` y sus secciones.
3. En `data/fichas-documentales.yml`, leer las fichas de los `repositorios_clave`.
4. En `data/lineas-narrativas.yml`, leer la línea narrativa asociada.

Redacción:
- Formato Markdown.
- Encabezado de nivel 2 para el capítulo: `## {título del capítulo}`.
- Para cada sección definida en el esquema:
  - Encabezado de nivel 3 con el título de la sección.
  - 3 a 7 párrafos desarrollando la sección.

Estilo (según `data/contexto-autor.md`):
- Tono serio, tranquilo y lógico.
- Lenguaje claro y directo.
- Describir hechos, contexto, decisiones y aprendizajes observables.
- No imponer juicios de valor.
- No centrar el texto en el ego del autor; el foco está en el proceso y los proyectos.
- No usar lenguaje poético ni exagerado.
- Mostrar dificultades y esfuerzo sin victimización ni dramatización.

Salida:
- Devolver solo el contenido del capítulo en Markdown, listo para guardarse como `manuscrito/{CAP_ID}.md`.

## Plantilla para el prólogo

**Task – Redactar el prólogo del libro**

Entradas:
- `data/contexto-autor.md`
- `data/lineas-narrativas.yml`
- `data/indice-libro.yml`

Objetivo:
Escribir el prólogo del libro como una introducción sobria y descriptiva, alineada con el contexto y estilo definidos en `data/contexto-autor.md`.

Pasos previos:
1. Leer `data/contexto-autor.md` para entender quién es el autor, qué ámbitos trabaja y qué tono debe tener el texto.
2. Leer las líneas narrativas e índice para comprender la estructura general del libro.

Contenido mínimo del prólogo:
- Explicar qué tipo de libro es: un documental del contenido de varios repositorios, construido a partir de años de trabajo, experimentos y uso de IA como apoyo.
- Describir el contexto general: trabajo en software, cloud, open source y comunidades; necesidad de documentar lo aprendido.
- Anticipar qué encontrará el lector: partes y capítulos que recorren marcos conceptuales, arquitecturas vivas, demos, juegos y comunidad.
- Cerrar explicando que el objetivo es compartir un proceso de trabajo y aprendizaje, dejando espacio al lector para observar y pensar por su cuenta.

Estilo:
- Seguir el tono descrito en `data/contexto-autor.md`.
- Evitar frases de autoelogio o de victimización.
- No emitir juicios de valor; solo presentar el propósito y el enfoque del libro.

Salida:
- Texto en Markdown, con encabezado `# Prólogo` o `## Prólogo`, listo para guardarse como `manuscrito/prologo.md`.
