---
title: Bitácora de IA
nav_order: 6
---

# Bitácora de uso crítico de Inteligencia Artificial y herramientas

Este registro documenta, de forma transparente, qué herramientas se utilizaron en cada etapa del trabajo, con qué propósito, y con qué resultado, en cumplimiento de las pautas de la cátedra sobre el uso reflexivo de tecnologías. El uso de estas herramientas complementa, no reemplaza, el trabajo intelectual del estudiante: las decisiones de fondo fueron tomadas y validadas por el autor.

## Herramientas por etapa

| Etapa | Herramientas previstas o utilizadas |
| :---- | :---- |
| Definición del problema | Asistentes de IA (Gemini, Claude) para estructurar y discutir el enfoque |
| Recolección y limpieza | API de GitHub, Python (`requests`, `pandas`), Google Trends |
| Modelo y simulación | Python, SimPy, SciPy/NumPy, Matplotlib; asistentes de IA para apoyo de código |
| Documentación | Asistentes de IA para redacción y organización, con revisión del autor |

---

## Registro de interacciones

### Fase de diseño inicial (junio de 2026) - Gemini

* **Objetivo:** validar la viabilidad del TFI, definir el alcance del modelo de colas y esbozar una metodología de calibración para el tiempo de servicio, ademas de ayudarme a redactar la primera versión de la Etapa 1 (delimitación del problema, objetivos y pregunta de investigación) y abstraer el fenómeno al marco de la teoría de colas.
* **Aporte:** ayudó a abstraer el pipeline de GitHub al marco conceptual de la Unidad 5 (entidades, recursos, colas) y a ponderar repositorios candidatos.

**Prompt utilizado** *:*
 
> "A partir de la consigna del TFI de Modelos y Simulación, ayudame a redactar la Etapa 1: delimitar el fenómeno del aumento de Pull Requests generados por IA en proyectos de GitHub, explicar por qué es un problema relevante para un ingeniero en informática, formular al menos dos objetivos y una pregunta de investigación, y encuadrar el problema dentro de un modelo de teoría de colas."
 


* **Reflexión crítica:** la herramienta agilizó la organización de ideas, pero el planteo inicial contenía un supuesto que más tarde resultó no sostenerse con datos (ver entrada siguiente). Esto reforzó la necesidad de no dar por válida ninguna afirmación sin verificación propia.


### Fase de verificación y reformulación (junio de 2026) - Claude

* **Objetivo:** contrastar con datos reales el supuesto de partida y consolidar la metodología.


**Prompts utilizados:**
 
> **1. Exploración y viabilidad del tema.** "Necesito ayuda para definir el tema de mi Trabajo Final Integrador de Modelos y Simulación. Te comparto la consigna y los apuntes de la materia. Mi idea inicial gira en torno al volumen de Pull Requests, commits e issues en GitHub y al impacto de los agentes de IA generativa sobre ese flujo. Quiero un análisis crítico que evalúe la viabilidad del tema, lo relacione con los modelos vistos en la materia y me proponga especificaciones y condiciones concretas para encararlo."
 
> **2. Concreción del modelo.** "Quiero avanzar con la idea sobre GitHub. Explicame en detalle en qué consistiría exactamente el proyecto: qué fenómeno modelaría, qué tipo de modelo de la materia aplica, cuáles serían las entidades, los recursos y las variables clave, y qué datos reales necesitaría obtener."
 
> **3. Planificación de datos y calibración.** "Necesito asistencia para planificar la recolección de datos (Etapa 2) y la simulación (Etapa 4). El repositorio fuente es pandas-dev/pandas. Como la API de GitHub solo expone las fechas de creación y de merge, y no el tiempo de revisión humano puro, mi idea es deducir la tasa de llegadas de los datos reales y calibrar el tiempo de servicio de forma iterativa en SimPy hasta que el tiempo en sistema simulado coincida con el histórico real. ¿Es correcto este enfoque?"
 
> **4. Verificación de evidencia externa.** "Encontré información sobre casos de proyectos de código abierto desbordados por contribuciones de IA (Godot, curl, Coolify, Rust) y sobre una reacción oficial de GitHub. ¿Conviene sumar esta evidencia a la justificación del problema? Verificá si las afirmaciones son confiables antes de usarlas."
 
> **5. Reestructuración del portafolio.** "Reestructurá y mejorá el portafolio digital. El objetivo es que el profesor vea con claridad la idea y lo que se va a hacer, y que el portafolio demuestre que cumple apropiadamente con la consigna definida por la cátedra, además de poder servir como documentacion."


* **Aporte y proceso:**
  1. Se midió, con la API de GitHub, el volumen de PRs por año en `pandas`. Los datos mostraron un volumen estable o decreciente, contradiciendo el supuesto inicial de un aumento atribuible a la IA en ese repositorio.
  2. A partir de ese hallazgo, se reformuló el proyecto: de "demostrar un aumento histórico" a "calibrar un modelo con datos reales y estresarlo para hallar el umbral de saturación". El fenómeno de la IA pasó a ser la motivación documentada y el escenario simulado, no una afirmación empírica sobre el repositorio.
  3. Se verificó, una por una, una lista de afirmaciones externas sobre el fenómeno. Se confirmaron las referidas a GitHub (función de límite de PRs y estadística de crecimiento) y a curl; se corrigió un dato sobre Godot que no coincidía con las fuentes; y se descartaron varias afirmaciones por falta de fuente primaria.


**Reflexión crítica:** el episodio más valioso del proceso surgió del prompt 3. Al verificar el supuesto con datos reales de la API de GitHub, se descubrió que el volumen de PRs de `pandas` era estable o decreciente, lo que invalidaba el contraste histórico planteado y obligó a reformular el enfoque del informe hacia un escenario de estrés sobre un modelo calibrado. En el prompt 4, la verificación una por una mostró que la información de respaldo era una mezcla: algunos datos eran reales (GitHub, curl), uno estaba mal etiquetado (Godot) y otros carecían de fuente, por lo que se descartaron. En conjunto, la IA fue útil para acelerar el análisis, pero requirió validación estricta y correcciones por parte del autor en cada paso.



### Fase de implementación de la extracción (julio de 2026) - Claude Code

* **Objetivo:** ejecutar las Etapas 2 y 3 (recolección y limpieza): con las decisiones de modelado ya fijadas, construir el script de extracción de PRs de `pandas-dev/pandas` desde la API de GitHub y obtener los datasets base (2024) y de validación (2020).

**Prompts utilizados (sesión de trabajo asistido con Claude Code, parafraseados):**

> **1. Cierre riguroso de las decisiones de modelado antes de programar.** "Antes de escribir una línea de código, verificá con profundidad si ya estamos en condiciones de implementar y si queda alguna decisión de modelado pendiente, cruzándolo contra la consigna oficial del TFI. Para cada recomendación que me hagas, preguntate si es realmente lo más apropiado y preciso en vez de darme la razón. Ayudame a fijar, una por una: la ventana temporal de calibración y de validación; la unidad de tiempo; cómo estimar el número de revisores activos; cómo modelar el abandono de PRs; el supuesto sobre las llegadas; la distribución del tiempo de servicio; la disciplina de la cola; los parámetros de la corrida de simulación; y qué rol darles al tipo de cuenta (bot/humano) y a Google Trends." — De este intercambio, y de repreguntar por la precisión de cada respuesta, surgió: ventana 2024 (base) y 2020 (validación), elegida por sobre 2025 para minimizar la censura por la derecha en la distribución del tiempo en sistema; tiempo en días; `c` anclado en las cuentas de `merged_by` por encima de un umbral de actividad; abandono modelado como tiempo de paciencia (lo más realista); llegadas Poisson a verificar contra los interarribos reales; tiempo de servicio lognormal/gamma elegido por bondad de ajuste; cola FIFO; y warm-up + horizonte + réplicas + intervalo de confianza para las corridas. Una repregunta explícita ("¿de verdad conviene sacar Google Trends?") hizo que el asistente **revirtiera** su recomendación inicial: se conservó Google Trends como evidencia de contexto de la premisa (no como entrada del modelo), y el tipo de cuenta quedó como dato meramente descriptivo, dado que la API no distingue el código asistido por IA que ingresa a través de cuentas humanas.

> **2. Planificación y construcción de la extracción con TDD y arquitectura de datos por capas (medallion).** "Frená y hagamos primero el planning de la extracción; recién después programamos, y con TDD. Elegí la mejor vía para consultar la API de GitHub y organizá los datos con una lógica de *medallion architecture* liviana." — Se acordó usar la **API GraphQL** (su búsqueda devuelve `mergedBy` de forma inline y evita miles de llamadas de detalle por PR) con ventaneo mensual para no superar el tope de 1000 resultados por consulta, y una **arquitectura de datos por capas al estilo medallion**, en carpetas planas y sin framework pesado: *bronze* (`data/raw/`, el JSON crudo tal como lo devuelve la API), *silver* (`data/clean/`, un CSV por PR ya limpio y con el criterio de censura aplicado) y *gold* (los agregados de calibración, pendientes para la etapa siguiente). Como *bronze* guarda el crudo completo, cualquier campo adicional puede re-derivarse sin volver a consultar la API. Sobre ese plan, aprobado por el autor, se implementó con enfoque TDD la transformación pura, el cliente GraphQL (paginación por cursor y manejo de errores y de rate limit) y el orquestador CLI; se validó con un smoke test de un mes y luego con las corridas completas de 2024 y 2020, cuyos totales coincidieron exactamente con la exploración preliminar. El autor revisó el plan y el código, y validó los resultados de cada corrida antes de avanzar.

* **Aporte y proceso:**
  1. Se implementó, con enfoque TDD (tests primero), un módulo de transformación pura, un cliente GraphQL con paginación por cursor y manejo de errores/rate limit, y un orquestador CLI. Diez tests en verde.
  2. Un smoke test de un solo mes validó el supuesto clave (que GraphQL devuelve `mergedBy` inline) antes de la corrida completa.
  3. Se extrajeron 2547 PRs cerrados de 2024 y 5333 de 2020; los totales coincidieron exactamente con la exploración preliminar previa, y la censura resultó prácticamente nula en 2024, confirmando la elección de ventana.
  4. La IA detectó y corrigió dos errores propios: un patrón de `.gitignore` que habría excluido `.env.example`, y un fallo de codificación (cp1252) en la consola de Windows.

* **Reflexión crítica:** el asistente aceleró el diseño y la escritura del código, pero las decisiones de modelado no se delegaron: se discutieron y validaron una por una, y en un caso (Google Trends) el autor repreguntó y la recomendación se revirtió tras reconsiderarla. El código generado se revisó y se cubrió con tests; los resultados de la extracción se contrastaron contra datos ya conocidos (la tabla de exploración) antes de darlos por válidos. Se sostuvo la regla de que los resultados ajustan el texto, y no al revés.


### Fase de implementación de la capa gold (julio de 2026) - Claude Code

* **Objetivo:** ejecutar la primera parte de la Etapa 4 (agregados de calibración): destilar el CSV *silver* en los parámetros que alimentan el modelo M/M/c —tasa de llegadas λ, fracción de abandono, número de revisores activos `c` y la distribución objetivo del tiempo en sistema— construyendo la capa *gold* de la arquitectura medallón, sin todavía ajustar distribuciones ni simular.

**Prompts utilizados (sesión de trabajo asistido con Claude Code, parafraseados):**

> **1. Acotar el alcance de la capa gold antes de programar.** "Continuemos con el TFI construyendo ahora la capa *gold* del pipeline de datos —la de los agregados de calibración— sobre los CSV *silver* ya extraídos. Antes de escribir código, definamos con precisión qué debe producir esta capa y respetemos el mismo enfoque que veníamos usando: funciones puras con TDD, decisiones de modelado explícitas y en mis manos, y sin resolver el trabajo de forma autónoma." — Sobre esa base se fijó, mediante preguntas explícitas, el alcance de la capa: computar y persistir los parámetros de calibración (λ, fracción de abandono, estimación de `c`, y la serie del tiempo en sistema de los mergeados como distribución objetivo) más tablas y gráficos descriptivos, dejando el ajuste estadístico de distribuciones y la simulación para más adelante; cubrir solo el año 2024 (ventana de calibración) y reservar 2020 (validación) para una iteración posterior; y generar gráficos básicos de inspección. Se replicó el patrón ya usado en la extracción: funciones puras testeadas (TDD) separadas del orquestador que hace I/O y gráficos.

> **2. Decisión del umbral de revisores activos (`c`).** [surgió durante la implementación, no como prompt inicial] — Al correr la agregación, el criterio automático por defecto (retener las cuentas con merges por encima del promedio) resultó degenerado: como una sola cuenta (`mroeschke`) concentra el 76,6% de los merges de 2024, el promedio se dispara y da `c=1`, que no representa la capacidad de revisión real. El asistente lo señaló en lugar de dejar pasar el default, y presentó la distribución completa de merges por cuenta (13 cuentas) con varios cortes posibles. El autor eligió el umbral de ≥10 merges → **`c=8`**, apoyado en una discontinuidad real de los datos (8 cuentas "core" con ≥22 merges frente a una cola esporádica de ≤7 merges); ese corte quedó fijado y documentado en el código como decisión de modelado ajustable.

* **Aporte y proceso:**
  1. Se implementó con TDD un módulo de cálculo puro (`src/gold.py`) —λ, fracción de abandono, merges por cuenta, revisores activos según umbral y distribución del tiempo en sistema de los mergeados— y un orquestador CLI (`src/aggregate_gold.py`) que persiste la capa *gold* (`data/gold/`) y tres gráficos descriptivos (`charts/`). Siete tests nuevos; diecisiete en verde en total.
  2. Los agregados se contrastaron contra lo ya conocido del dataset: 2547 llegadas (coincide con el *silver*), λ ≈ 6,96 PRs/día, fracción de abandono 0,218, y una distribución del tiempo en sistema fuertemente asimétrica a derecha (mediana 0,71 d, media 6,68 d, cola hasta 766 d), coherente con las candidatas lognormal/gamma y no con una normal.
  3. Se detectó un hueco preexistente de configuración: el `_config.yml` de Jekyll no excluía los directorios de código y datos; se agregó `exclude` para `.venv`, `src`, `data`, `tests` y `reference`, dejando `charts/` publicable.

* **Reflexión crítica:** el aporte más valioso de la sesión no fue el código sino frenar un valor automático incorrecto: el umbral por defecto para `c` habría fijado en silencio `c=1`. Al exponer la distribución real y sus alternativas, la decisión de modelado quedó en manos del autor y anclada en una característica genuina de los datos, no en una regla estadística ciega. Se mantuvo la separación entre lógica pura e I/O, la cobertura con tests, y la regla de que los datos ajustan el texto y no al revés.

---

## Material pendiente de incorporar

De acuerdo con la consigna, se agregarán a esta bitácora:

* Los prompts completos utilizados con los asistentes de IA, con sus respuestas.
* Capturas de pantalla de las interacciones y de los entornos de trabajo.
* Los fragmentos de código generados con apoyo de IA, indicando qué se adaptó o corrigió.

---
[ ↩ Volver al índice principal](index.md)