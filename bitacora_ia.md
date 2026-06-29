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

* **Objetivo:** validar la viabilidad del TFI, definir el alcance del modelo de colas y esbozar una metodología de calibración para el tiempo de servicio.
* **Aporte:** ayudó a abstraer el pipeline de GitHub al marco conceptual de la Unidad 5 (entidades, recursos, colas) y a ponderar repositorios candidatos.
* **Reflexión crítica:** la herramienta agilizó la organización de ideas, pero el planteo inicial contenía un supuesto que más tarde resultó no sostenerse con datos (ver entrada siguiente). Esto reforzó la necesidad de no dar por válida ninguna afirmación sin verificación propia.

### Fase de verificación y reformulación (junio de 2026) - Claude

* **Objetivo:** contrastar con datos reales el supuesto de partida y consolidar la metodología.
* **Aporte y proceso:**
  1. Se midió, con la API de GitHub, el volumen de PRs por año en `pandas`. Los datos mostraron un volumen estable o decreciente, contradiciendo el supuesto inicial de un aumento atribuible a la IA en ese repositorio.
  2. A partir de ese hallazgo, se reformuló el proyecto: de "demostrar un aumento histórico" a "calibrar un modelo con datos reales y estresarlo para hallar el umbral de saturación". El fenómeno de la IA pasó a ser la motivación documentada y el escenario simulado, no una afirmación empírica sobre el repositorio.
  3. Se verificó, una por una, una lista de afirmaciones externas sobre el fenómeno. Se confirmaron las referidas a GitHub (función de límite de PRs y estadística de crecimiento) y a curl; se corrigió un dato sobre Godot que no coincidía con las fuentes; y se descartaron varias afirmaciones por falta de fuente primaria.
* **Reflexión crítica:** el episodio más valioso del proceso fue descubrir que una creencia inicial no resistía el contraste con los datos. La IA fue útil para acelerar la búsqueda y el análisis, pero requirió verificación estricta: una de las herramientas presentó información mezclando datos reales, datos mal etiquetados y afirmaciones sin respaldo. La validación contra fuentes confiables fue indispensable y es una práctica que se mantiene para todo el trabajo.

---

## Material pendiente de incorporar

De acuerdo con la consigna, se agregarán a esta bitácora:

* Los prompts completos utilizados con los asistentes de IA, con sus respuestas.
* Capturas de pantalla de las interacciones y de los entornos de trabajo.
* Los fragmentos de código generados con apoyo de IA, indicando qué se adaptó o corrigió.

---
[ ↩ Volver al índice principal](index.md)