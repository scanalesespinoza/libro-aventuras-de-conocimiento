# Iteración 12 – Ensamblado del libro completo

Esta iteración toma:

- `manuscrito/prologo.md`
- `manuscrito/cap-01.md`
- `manuscrito/cap-02.md`
- `manuscrito/cap-03.md`
- `manuscrito/cap-04.md`
- (y el resto de capítulos)
- `data/indice-libro.yml`

y construye un manuscrito único del libro en:

- `manuscrito/libro-completo.md`

---

## Objetivo

Unir prólogo y capítulos en el orden definido por `data/indice-libro.yml`, respetando:

- el orden de partes y capítulos,
- los encabezados,
- y el tono original de cada archivo.

No se hacen modificaciones de contenido dentro de los capítulos en esta iteración; solo se ensamblan.

---

## Task para Codex – Ensamblar el libro

```text
Task – Construir manuscrito/libro-completo.md

Entradas:
- data/indice-libro.yml
- manuscrito/prologo.md
- manuscrito/cap-01.md
- manuscrito/cap-02.md
- manuscrito/cap-03.md
- manuscrito/cap-04.md
- (agregar el resto de capítulos según el índice)

Objetivo:
Generar un solo archivo Markdown que contenga el libro completo, en el orden definido por data/indice-libro.yml.

Instrucciones:
1. Leer data/indice-libro.yml para:
   - conocer las partes del libro,
   - conocer los capítulos y su orden.
2. Estructurar el manuscrito así:
   - Título general del libro (si aplica).
   - Prólogo (contenido de manuscrito/prologo.md).
   - Para cada parte:
     - Encabezado de nivel 1 con el título de la parte.
     - Para cada capítulo de esa parte, en el orden indicado:
       - Incluir el contenido completo del archivo manuscrito/cap-0X.md correspondiente.
3. No modificar el contenido interno de prólogo ni de los capítulos:
   - respetar encabezados y texto tal como están.
4. Asegurarse de que haya saltos de línea suficientes entre secciones para que el Markdown quede legible.

Salida:
- Un único archivo lógico equivalente a manuscrito/libro-completo.md con todo el contenido ensamblado.
```
