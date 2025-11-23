# Iteración 10 – Revisión técnica y de estilo de capítulos

Esta iteración tiene como objetivo revisar todos los capítulos escritos hasta ahora desde dos ángulos:

- **Revisión técnica**: comprobar que lo que se dice de cada repositorio y tecnología es coherente con `data/fichas-documentales.yml`.
- **Revisión de estilo**: comprobar que el texto respeta el tono definido en `data/contexto-autor.md` y las reglas de `docs/instrucciones-redaccion.md`.

La salida de esta iteración se consolida en:

- `data/revision-tecnica-capitulos.yml`
- `data/revision-estilo-capitulos.yml`

Estos archivos se consideran acumulativos: se pueden ir actualizando a medida que aparezcan nuevos capítulos.

---

## Alcance

Capítulos a revisar (ejemplo, ajustar según estado real):

- `manuscrito/cap-01.md`
- `manuscrito/cap-02.md`
- `manuscrito/cap-03.md`
- `manuscrito/cap-04.md`
- (y los siguientes `cap-0X.md` cuando existan)

---

## 10.1 Revisión técnica

### Objetivo

Verificar que las descripciones de:

- repositorios,
- tecnologías,
- relaciones entre proyectos,

sean coherentes con lo documentado en `data/fichas-documentales.yml`.

### Salida esperada

Archivo YAML:

- `data/revision-tecnica-capitulos.yml`

Ejemplo de estructura:

```yaml
capitulos:
  - id: cap-01
    observaciones:
      - tipo: "repositorio"
        repo: "all-about-me"
        comentario: "Descripción coherente con la ficha."
      - tipo: "repositorio"
        repo: "the-wise-tech"
        comentario: "Aquí podría mencionarse también su rol como marco conceptual."
  - id: cap-03
    observaciones:
      - tipo: "tecnologia"
        tecnologia: "GitOps"
        comentario: "Se podría precisar que el enfoque está orientado a declaratividad más sincronización continua."

Task para Codex – Revisión técnica
Task – Revisión técnica de capítulos

Entradas:
- data/fichas-documentales.yml
- manuscrito/cap-01.md
- manuscrito/cap-02.md
- manuscrito/cap-03.md
- manuscrito/cap-04.md
- (agregar más capítulos cuando existan)

Objetivo:
Revisar los capítulos y registrar observaciones técnicas sobre cómo se describen repositorios y tecnologías, comparando con la información de data/fichas-documentales.yml.

Instrucciones:
1. Para cada capítulo:
   - Detectar menciones a repositorios y tecnologías.
   - Comparar su descripción con la ficha correspondiente en data/fichas-documentales.yml.
2. Cuando veas:
   - descripciones inconsistentes,
   - detalles que faltan,
   - oportunidades de precisión,
   agrega una entrada en la salida YAML.
3. Usa este formato:
   ```yaml
   capitulos:
     - id: cap-01
       observaciones:
         - tipo: "repositorio"
           repo: "id-del-repo"
           comentario: "Observación breve."
         - tipo: "tecnologia"
           tecnologia: "nombre"
           comentario: "Observación breve."
     - id: cap-02
       observaciones:
         - ...



Mantén un tono neutro y descriptivo, sin juicios de valor.


Entrega solo el documento YAML final como salida.



---

## 10.2 Revisión de estilo

### Objetivo

Verificar que cada capítulo mantenga el estilo definido en:

- `data/contexto-autor.md`
- `docs/instrucciones-redaccion.md`

En particular:

- tono serio, tranquilo y lógico,
- lenguaje claro y directo,
- sin juicios de valor fuertes,
- sin victimización ni autoexaltación,
- sin épica ni adornos innecesarios.

### Salida esperada

Archivo YAML:

- `data/revision-estilo-capitulos.yml`

Ejemplo de estructura:

```yaml
capitulos:
  - id: cap-02
    observaciones:
      - seccion: "Contexto de los marcos conceptuales"
        frase_original: "Este enfoque es la forma correcta de abordar el trabajo con equipos."
        recomendacion: "Reformular de manera descriptiva, por ejemplo: 'Este enfoque propone una forma de abordar el trabajo con equipos basada en...'."
  - id: cap-04
    observaciones:
      - seccion: "Aprendizajes operativos"
        frase_original: "Estos patrones garantizan la resiliencia del sistema."
        recomendacion: "Cambiar a 'Estos patrones apuntan a mejorar la resiliencia del sistema en los escenarios descritos.'"

Task para Codex – Revisión de estilo
Task – Revisión de estilo de capítulos

Entradas:
- data/contexto-autor.md
- docs/instrucciones-redaccion.md
- manuscrito/cap-01.md
- manuscrito/cap-02.md
- manuscrito/cap-03.md
- manuscrito/cap-04.md
- (agregar más capítulos cuando existan)

Objetivo:
Identificar frases o párrafos que no se alineen con el estilo definido en contexto-autor.md e instrucciones-redaccion.md y proponer reformulaciones.

Instrucciones:
1. Leer primero data/contexto-autor.md y docs/instrucciones-redaccion.md.
2. Para cada capítulo:
   - Recorrer el texto sección por sección.
   - Localizar frases o párrafos que:
     - suenen a juicio de valor fuerte,
     - muestren autoexaltación,
     - presenten victimización,
     - usen un tono demasiado épico o adornado.
3. Por cada caso, registrar:
   - la sección aproximada,
   - la frase original,
   - una recomendación de reformulación más neutra y descriptiva.
4. Usar este formato:
   ```yaml
   capitulos:
     - id: cap-01
       observaciones:
         - seccion: "título o referencia"
           frase_original: "texto original"
           recomendacion: "texto sugerido."



Mantener recomendaciones breves y concretas.


Entregar solo el YAML como salida.
