# Iteración 11 – Aplicar revisiones a los capítulos

Esta iteración toma las observaciones de:

- `data/revision-tecnica-capitulos.yml`
- `data/revision-estilo-capitulos.yml`

y las aplica a los archivos:

- `manuscrito/cap-01.md`
- `manuscrito/cap-02.md`
- `manuscrito/cap-03.md`
- `manuscrito/cap-04.md`
- (y siguientes capítulos cuando existan)

El objetivo es ajustar solo lo necesario, sin reescribir los capítulos desde cero.

---

## Patrón de task por capítulo

Para cada capítulo (`CAP_ID`, por ejemplo `cap-03`):

```text
Task – Actualizar manuscrito/{CAP_ID}.md aplicando revisiones

Entradas:
- data/contexto-autor.md
- docs/instrucciones-redaccion.md
- data/revision-tecnica-capitulos.yml
- data/revision-estilo-capitulos.yml
- manuscrito/{CAP_ID}.md

Objetivo:
Generar una nueva versión de manuscrito/{CAP_ID}.md aplicando las observaciones técnicas y de estilo asociadas a este capítulo, manteniendo la estructura y el sentido original.

Instrucciones:
1. Leer data/contexto-autor.md y docs/instrucciones-redaccion.md para asegurar consistencia de tono.
2. En data/revision-tecnica-capitulos.yml:
   - Buscar la entrada con id = {CAP_ID}.
   - Para cada observación:
     - Localizar en el capítulo la parte relevante.
     - Ajustar la descripción de repositorio o tecnología según el comentario.
3. En data/revision-estilo-capitulos.yml:
   - Buscar la entrada con id = {CAP_ID}.
   - Para cada observación:
     - Localizar la frase original.
     - Reformularla según la recomendación, respetando:
       - tono serio, tranquilo y lógico,
       - lenguaje claro,
       - ausencia de juicios de valor fuertes.
4. No reescribir el capítulo completo:
   - Mantener encabezados y secciones,
   - Modificar solo lo necesario para abordar las observaciones.
5. Entregar como salida el contenido completo y actualizado de manuscrito/{CAP_ID}.md en formato Markdown.

Salida:
- Texto en Markdown listo para sobrescribir manuscrito/{CAP_ID}.md.
```
