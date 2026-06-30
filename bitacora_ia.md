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



---

## Material pendiente de incorporar

De acuerdo con la consigna, se agregarán a esta bitácora:

* Los prompts completos utilizados con los asistentes de IA, con sus respuestas.
* Capturas de pantalla de las interacciones y de los entornos de trabajo.
* Los fragmentos de código generados con apoyo de IA, indicando qué se adaptó o corrigió.

---
[ ↩ Volver al índice principal](index.md)