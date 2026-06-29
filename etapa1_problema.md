# Etapa 1: Definición del problema

## 1. El fenómeno a estudiar

En los proyectos de software de código abierto, las contribuciones llegan principalmente en forma de Pull Requests (PRs): propuestas de cambio que un mantenedor debe revisar, validar e integrar (mergear) o rechazar.

La irrupción de la IA generativa y de los agentes automáticos modificó profundamente una de las dos mitades de este proceso. **Generar** una contribución de código se volvió rápido y barato: una persona o un bot pueden producir múltiples PRs en poco tiempo. En cambio, **revisar** esa contribución no se aceleró, porque depende del esfuerzo cognitivo de un recurso escaso y fijo: los mantenedores humanos.

Este desajuste configura un problema clásico de **Teoría de Colas**. Los PRs son entidades que llegan a una tasa creciente (λ), esperan en una cola, y son atendidos por un número limitado de revisores (c) a una tasa de servicio (μ) que no escala con la demanda. A medida que la utilización de los revisores se aproxima al 100%, la cola de PRs acumulados y el tiempo de permanencia en el sistema crecen de forma desproporcionada.

**¿A quién afecta y cuándo?** Afecta a los mantenedores de proyectos abiertos, que reportan agotamiento (burnout), y a la comunidad que depende de ese software, ya que la saturación retrasa la integración de contribuciones legítimas. Es un fenómeno actual: las primeras reacciones públicas y las medidas técnicas para contenerlo se concentran entre 2025 y 2026 (ver Justificación).

## 2. Por qué interesa analizar este fenómeno

Como futuro ingeniero en informática, el fenómeno me resulta relevante por tres motivos. Primero, toca directamente la sostenibilidad del ecosistema de software libre, del que depende buena parte de la infraestructura digital moderna. Segundo, es un caso donde la IA, una tecnología que suele presentarse solo por sus beneficios, produce un efecto secundario medible y problemático. Tercero, es un sistema que se deja modelar con las herramientas de la materia, lo que permite pasar de la opinión a la cuantificación.

### Justificación documentada

A diferencia de una motivación hipotética, este fenómeno está respaldado por hechos públicos y verificables ocurridos entre 2025 y 2026:

* **Reacción oficial de la plataforma.** En junio de 2026, GitHub incorporó una función que permite a los mantenedores limitar la cantidad de PRs abiertos simultáneos de usuarios sin permiso de escritura, presentada explícitamente como una respuesta al volumen creciente de contribuciones, muchas generadas por IA, que desbordan las colas de revisión. Según cifras de la propia GitHub, los PRs mergeados en toda la plataforma pasaron de unos 25 millones por mes en enero de 2023 a más de 90 millones, un aumento de aproximadamente 3,6 veces.

* **Caso curl.** El proyecto curl, mantenido por un equipo pequeño de voluntarios, cerró a comienzos de 2026 su programa de recompensas por errores en HackerOne debido a la avalancha de reportes de baja calidad generados por IA. Su mantenedor, Daniel Stenberg, documentó que alrededor del 20% de las entradas de 2025 eran "AI slop" y que la proporción de reportes genuinos cayó a alrededor del 5%. El caso ilustra con precisión el mecanismo de este trabajo: generar un reporte con IA es casi gratis, pero validarlo sigue costando el mismo tiempo humano.

* **Caso Godot.** Los mantenedores del motor de videojuegos de código abierto Godot reportaron sentirse desbordados y desmoralizados por los PRs generados por IA, con miles de PRs abiertos a la vez. Su propuesta de solución es conseguir más fondos para contratar más revisores, es decir, aumentar la capacidad del recurso, exactamente una de las palancas que este trabajo simula.

* **Otros casos documentados.** El fenómeno no es aislado: se reportaron incidentes equivalentes en Node.js (un PR generado por IA de gran extensión que motivó una petición formal de la comunidad), Ghostty (cierre de contribuciones externas), tldraw (suspensión de la recepción de PRs) y en el equipo de seguridad de Django, entre otros.

> **Nota sobre el encuadre metodológico.** Este trabajo no afirma que la IA haya disparado, de forma medible, la tasa de llegadas de un repositorio puntual. La exploración preliminar de datos (ver [Etapas 2 y 3](etapa2_3_datos.md)) muestra que en un proyecto maduro como `pandas` el volumen de PRs es estable o decreciente. La atribución directa del aumento de volumen a la IA es, además, intrínsecamente difícil, porque buena parte del código asistido por IA ingresa a través de cuentas humanas. Por eso el fenómeno se aborda como un **escenario de estrés sobre un modelo calibrado con datos reales**: se valida el modelo en un régimen sano y luego se incrementa la tasa de llegadas para localizar el umbral de saturación. La evidencia documentada arriba justifica que ese escenario es plausible y de relevancia actual, no imaginario.

## 3. Objetivos del proyecto

**Objetivo principal:** Construir y validar, con datos reales, un modelo de simulación de eventos discretos del pipeline de revisión de PRs del repositorio `pandas`, y utilizarlo para identificar el umbral de llegadas que satura al equipo mantenedor y para evaluar estrategias de mitigación.

**Objetivos específicos:**

1. Extraer de la API de GitHub la tasa de llegadas real (λ) y la distribución del tiempo total en sistema (desde la creación hasta el merge) de `pandas` para un período base.
2. Calibrar el modelo, ajustando el tiempo de servicio y el número de revisores hasta reproducir la distribución real observada, anclando el número de revisores con una estimación de revisores activos derivada de los propios datos, y reportar la utilización resultante para confirmar que la base se encuentra en un régimen sano.
3. Estresar el modelo aumentando progresivamente la tasa de llegadas, para localizar el punto de saturación (utilización cercana a 1) y caracterizar cómo crecen la cola y el tiempo de espera.
4. Evaluar escenarios de mitigación (sumar revisores, incorporar un filtro automático de dos etapas, y limitar la cantidad de PRs concurrentes, esta última inspirada en la función real lanzada por GitHub) y medir su efecto sobre el umbral de colapso.

## 4. Pregunta de investigación

> A partir de un modelo de colas M/M/c calibrado y validado con datos reales del pipeline de revisión de PRs del repositorio `pandas`, ¿qué magnitud de aumento en la tasa de llegadas lleva la utilización de los revisores cerca del 100% y dispara el tiempo de permanencia en el sistema, y en qué medida políticas de mitigación como sumar revisores o incorporar filtros automáticos posponen o evitan ese colapso?

## 5. Fuentes

* GitHub Blog, "Limit open pull requests for users without write access" (changelog, 17 de junio de 2026): https://github.blog/changelog/2026-06-17-limit-open-pull-requests-for-users-without-write-access/
* GitHub Blog, "How pull request limits are cutting down the noise" (incluye la estadística de 25M a 90M de PRs mensuales): https://github.blog/open-source/maintainers/how-pull-request-limits-are-cutting-down-the-noise/
* InfoWorld, "GitHub eyes restrictions on pull requests to rein in AI-based code deluge on maintainers" (febrero de 2026): https://www.infoworld.com/article/4127156/github-eyes-restrictions-on-pull-requests-to-rein-in-ai-based-code-deluge-on-maintainers.html
* The New Stack, "cURL's Daniel Stenberg: AI slop is DDoSing open source": https://thenewstack.io/curls-daniel-stenberg-ai-is-ddosing-open-source-and-fixing-its-bugs/
* Cybernews, "Curl bug bounty AI security reports, Daniel Stenberg": https://cybernews.com/security/curl-bug-bounty-ai-security-reports-daniel-stenberg/
* Daniel Stenberg, "Death by a thousand slops" (blog, julio de 2025): https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/
* The Register, "Godot maintainers struggle with 'demoralizing' AI slop PRs": https://www.theregister.com/2026/02/18/godot_maintainers_struggle_with_draining/
* SoftwareSeni, "Curl Bug Bounty Shutdown and the Open-Source Incidents That Proved the Problem Is Real" (recopilación de casos): https://www.softwareseni.com/curl-bug-bounty-shutdown-and-the-open-source-incidents-that-proved-the-problem-is-real/

*Nota: las fuentes fueron verificadas de forma individual; los detalles del proceso de verificación se documentan en la [Bitácora](bitacora_ia.md).*

---
[↩ Volver al índice principal](index.md)


