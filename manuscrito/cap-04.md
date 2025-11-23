## Capítulo 4 – Resiliencia aplicada en demos cloud native

### Objetivo de resiliencia y alcance de las demos
La línea narrativa de resiliencia y operación cloud native busca validar patrones que mantengan servicios disponibles ante fallas controladas. Los repositorios reunidos en este capítulo funcionan como laboratorio para observar cómo responde una pila completa cuando se aplican pruebas de presión. El objetivo no es prometer infalibilidad, sino mostrar mecanismos concretos para sostener la operación y recuperar estabilidad.

La selección de repositorios cubre desde componentes mínimos hasta demos integrales. Cada pieza aporta un ángulo específico: definición de patrones, empaquetado de manifiestos, instrumentación de fallos o visualización de resultados. La narrativa documenta cómo estos elementos se combinan para formar escenarios reproducibles en Kubernetes u OpenShift.

El alcance se limita a experimentos observables. Se describen configuraciones, flujos de despliegue y formas de monitorear efectos. Al mantener el foco en evidencias y no en promesas, el capítulo sigue el tono sobrio definido en el contexto del autor y las instrucciones de redacción.

### Evolución de patrones desde mínimos a integrales
**minimal-service** ofrece el punto de partida: demuestra cómo construir servicios livianos y performantes en Java. Su énfasis en sencillez establece una base sobre la que se pueden probar patrones de tolerancia a fallas sin carga excesiva. Actúa como núcleo sobre el que se agregan otras capacidades.

El repositorio `super-app-framework` amplía esa base con un marco orientado a alta disponibilidad. Propone componentes para crear aplicaciones resilientes y seguras, también en Java. En la narrativa, este repositorio representa el salto desde un servicio mínimo hacia una arquitectura que anticipa fallos y busca absorberlos.

**updated-manifests-bundle** y **sc-cloud-native-demo** muestran cómo empaquetar y desplegar esas ideas. El primero reúne manifiestos que habilitan un MVP de monitoreo de estabilidad con Quarkus nativo; el segundo funciona como demo generada desde plantillas de Quarkus. Juntos ilustran la progresión: partir de un servicio pequeño, encapsularlo en manifiestos reproducibles y mostrarlo en un entorno demo.

### Pruebas de estabilidad y observabilidad
**resilient-app** es el backend que concentra las estrategias de resiliencia: maneja fallos, mantiene persistencia y ofrece el servicio principal de la demo. Se complementa con **resilient-frontend**, que expone en JavaScript cómo un cliente gestiona errores al comunicarse con el backend. Esta dupla permite observar la interacción completa bajo condiciones adversas.

**resilient-demo** agrega instrucciones para montar el entorno completo con base de datos PostgreSQL y contenedores. Al documentar cómo lanzar la demo, facilita reproducir pruebas y verificar que la resiliencia funcione más allá del código fuente. La narrativa destaca esta reproducibilidad como factor clave para que otros equipos evalúen los patrones.

Las pruebas se enfocan en instrumentar fallos y monitorear recuperación. Aunque los repositorios no detallan métricas específicas, la combinación de backend, frontend y guías de despliegue permite aplicar interrupciones controladas y observar respuestas. Se privilegia la descripción de los mecanismos disponibles sobre afirmaciones generales de robustez.

### Interfaces y reportes asociados
**quarkus-txt-report-frontend** ofrece una vista ligera para mostrar métricas sobre despliegues no listos. Su rol es dar feedback rápido durante las pruebas, reforzando la idea de que la resiliencia también se comunica a través de interfaces simples. La narrativa lo ubica como punto de observación que acompaña a las demos principales.

Otros frontends presentes en la línea, como resilient-frontend, sirven para validar la experiencia del usuario cuando el sistema enfrenta fallos. Al registrar cómo manejan errores y reconexiones, se obtiene una perspectiva complementaria a los logs o métricas internas. Esto ayuda a traducir la estabilidad técnica en señales perceptibles para quienes usan el servicio.

La conexión entre interfaces y backend cierra el ciclo de evaluación. Los reportes y vistas no solo informan; también facilitan decisiones sobre siguientes iteraciones. Documentar esta conexión mantiene coherencia con la práctica de revisiones compartidas que atraviesa el libro.

### Aprendizajes operativos y próximos pasos
Un aprendizaje central es que la resiliencia requiere un recorrido gradual. Comenzar con minimal-service y `super-app-framework` permite probar patrones en pequeño antes de escalar a demos completas. Esa progresión reduce riesgos y deja trazabilidad sobre qué ajustes funcionaron.

Otro hallazgo es la importancia de empaquetar y guiar la ejecución. updated-manifests-bundle y resilient-demo muestran que las instrucciones claras son tan necesarias como el código. Sin ellas, las pruebas pierden repetibilidad y se diluye la observabilidad.

Quedan pendientes mejoras en métricas y automatización de fallos. quarkus-txt-report-frontend y Kubernetes pueden integrarse con alertas más sofisticadas para detectar degradaciones temprano. Los próximos pasos apuntan a conectar estas demos con pipelines de GitOps y monitoreo continuo, manteniendo el mismo rigor que guía el resto del libro.
