# Etapa 1: Definición del Problema

## 1. El Fenómeno Estocástico a Estudiar
El volumen de contribuciones en repositorios públicos (*Open Source*) está creciendo de manera acelerada debido a la automatización de la creación de Pull Requests (PRs) mediante bots y agentes de IA. Mientras que la tasa de generación de código es masiva y automatizada, la fase de revisión y merge sigue dependiendo de un recurso estrictamente limitado: **los mantenedores humanos**.

Este desajuste configura un escenario ideal para la **Teoría de Colas**. Cuando la utilización de los revisores humanos se aproxima al 100%, la cola de PRs acumulados y los tiempos de permanencia en el sistema crecen de forma desproporcionada, arriesgando el colapso del repositorio.

## 2. Caso de Estudio Seleccionado
Se seleccionó como fuente digital el repositorio oficial de la librería **Pandas (`pandas-dev/pandas`)** debido a su gran volumen de actividad histórica y la clara presencia de interacciones entre humanos y automatizaciones.

## 3. Pregunta de Investigación
> *"¿Cómo ha variado la utilización y el tiempo de espera en el sistema de colas del repositorio Pandas al contrastar el periodo pre-IA (2021) frente al auge de automatización post-IA (2024), y qué impacto tendría la implementación de políticas de mitigación automatizadas sobre dicho sistema operativo?"*

## 4. Objetivos del Proyecto
* **Objetivo Principal:** Modelar y simular mediante eventos discretos (SimPy) el pipeline estocástico de revisión de PRs de Pandas para identificar el punto crítico de colapso del equipo mantenedor.
* **Objetivos Específicos:**
  1. Extraer parámetros reales de la API de GitHub para configurar distribuciones de llegadas ($\lambda$).
  2. Construir una "Línea Base" con datos de 2021 para validar que la simulación abstracta represente fielmente el comportamiento histórico equilibrado.
  3. Resolver la falta de datos crudos del tiempo de servicio puro ($\mu$) mediante una metodología de **Calibración y Ajuste Iterativo**.
  4. Simular escenarios de mitigación (Toma de Decisiones bajo Riesgo) como la adición de revisores o la inclusión de filtros algorítmicos.

---
[↩ Volver al Índice Principal](index.md)
