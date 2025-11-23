## Capítulo 3 – Arquitecturas vivas y eventos como código

### Visión declarativa y objetivos iniciales
La línea narrativa de plataformas declarativas y flujos GitOps parte de una inquietud: la documentación de arquitecturas suele quedarse estática mientras los sistemas cambian. La búsqueda es llevar esa documentación a un estado ejecutable que acompañe cada ajuste operativo. El objetivo inmediato es mantener consistencia entre la intención arquitectónica y lo que realmente corre en Kubernetes u OpenShift.

Las prácticas GitOps aparecen como respuesta a esa brecha. Versionar configuraciones y procesos permite que los cambios viajen con trazabilidad y revisión. Al situar los repositorios en control de versiones, la arquitectura se convierte en un artefacto vivo que se puede auditar y reproducir. El capítulo se apoya en esta idea para describir cómo se orquestan servicios, eventos y migraciones.

El punto de partida reconoce que la declaratividad no es solo un estilo de escritura, sino una forma de coordinar equipos y entornos. La narrativa mantiene el foco en decisiones observables: qué se versiona, cómo se sincroniza y qué problemas resuelve. Con esa base se abre el camino para explicar el rol de cada repositorio.

### Repositorios clave y roles complementarios
**Arkit8s** encarna la aspiración de una arquitectura viva. Propone flujos GitOps que mantengan documentación y despliegues alineados. El repositorio sirve como marco para pensar cómo versionar decisiones arquitectónicas y convertirlas en objetos que el clúster pueda aplicar. Actúa como puente entre la intención de diseño y la operación diaria.

**eventflow** aborda la gestión de eventos con planificación automatizada. Se concibe como plataforma que organiza espacios, actividades y asistentes, y sugiere personalización a través de reglas. En la narrativa funciona como ejemplo de aplicación empresarial que se beneficia de describir eventos y flujos de manera declarativa.

**eventflow-event-as-code** extiende esa idea al almacenar definiciones de eventos como código. Mantener las entidades y reglas en archivos versionados permite coherencia entre la lógica de negocio y su implementación. La combinación con eventflow muestra cómo la declaratividad baja al nivel de objetos concretos que otros servicios pueden consumir.

### Ejecución operada desde Git
**3scale-gitops-service** automatiza la sincronización de servicios API en 3scale a partir de definiciones en repositorios. Su rol es demostrar que la gestión de API también puede seguir el camino GitOps: se revisa un CSV en control de versiones y se aplican comandos para mantener la plataforma alineada. Esto aporta un ejemplo claro de ejecución repetible desde Git.

**deploymentconfig-2-deployment** se enfoca en migraciones de DeploymentConfig a Deployment. Al ofrecer una interfaz para guiar el traslado, refleja cómo la declaratividad facilita modernizaciones controladas. Versionar estos pasos permite reproducirlos y reducir riesgos durante la transición entre modelos de despliegue.

**kubeland** aporta visualización de cargas en Kubernetes. Aunque no ejecuta cambios, su enfoque en mostrar recursos desplegados complementa el ciclo declarativo: ayuda a verificar que las sincronizaciones hayan surtido efecto. La narrativa lo usa como evidencia de que la observabilidad también forma parte de mantener arquitecturas vivas.

### Integración con modelos organizacionales
Las prácticas descritas se apoyan en los marcos organizacionales de capítulos previos. Versionar configuraciones y flujos permite asignar responsabilidades claras a equipos específicos, en línea con los esquemas de roles definidos en la arquitectura de tres contextos. La coordinación entre repositorios y equipos hace que la declaratividad no dependa solo de herramientas, sino de acuerdos de trabajo.

El uso de Git como fuente única de verdad facilita revisiones entre áreas. Los cambios en 3scale-gitops-service o en las definiciones de eventflow pasan por el mismo proceso de revisión que el código de aplicaciones. Esto refuerza la idea de que la gobernanza técnica se sostiene con prácticas compartidas y transparencia sobre quién modifica qué.

La integración también se nota en las migraciones. deploymentconfig-2-deployment encaja en una estructura donde los equipos saben cuándo intervenir y cómo coordinar despliegues progresivos. El modelo organizacional previo permite que estos movimientos ocurran sin depender de héroes individuales y con registro de cada decisión.

### Aprendizajes y líneas abiertas
Un primer aprendizaje es que la declaratividad exige disciplina continua. Mantener arkit8s, eventflow y sus artefactos asociados implica revisar constantemente que las definiciones reflejen la realidad. Sin ese hábito, la arquitectura viva se vuelve estática de nuevo.

Otro hallazgo proviene de las integraciones. Automatizar API con 3scale-gitops-service y coordinar migraciones con deploymentconfig-2-deployment muestran que GitOps puede abarcar capas diversas del stack. Sin embargo, cada incorporación demanda ajustar flujos de revisión y monitoreo para evitar cambios silenciosos.

Quedan líneas abiertas en cómo escalar estas prácticas. kubeland ofrece visibilidad, pero la expansión a más clústeres o equipos requerirá reforzar métricas y alertas para detectar desalineaciones. La narrativa destaca estos retos como preparación para las demos de resiliencia que profundizarán en observabilidad y pruebas controladas.
