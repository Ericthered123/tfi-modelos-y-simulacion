---
title: Etapa 4 - Modelo
nav_order: 4
---

# Etapa 4: Formulación del modelo e implementación de la simulación

> Esta sección describe el diseño del modelo y el plan de simulación. La implementación, los gráficos y los resultados se incorporarán durante la fase de ejecución.

## 4.1. Tipo de modelo

El fenómeno se representa con un **modelo de colas** del tipo **M/M/c** (llegadas y servicio modelados como procesos estocásticos, con c servidores), implementado mediante **simulación de eventos discretos (DES)**. El enfoque DES permite, además, relajar el supuesto exponencial del tiempo de servicio cuando los datos lo justifiquen, usando distribuciones más adecuadas para esfuerzos humanos (por ejemplo, lognormal o gamma, que evitan valores negativos).

## 4.2. Componentes del sistema

| Concepto de Teoría de Colas | Representación en el modelo |
| :---- | :---- |
| Entidad | Un Pull Request |
| Llegada (λ) | PRs creados por unidad de tiempo (estimado de datos reales) |
| Recurso o servidor (c, μ) | Los mantenedores que revisan, capacidad limitada |
| Cola | PRs abiertos esperando revisión |
| Tiempo de servicio | Esfuerzo de revisar y mergear un PR |
| Salida (atendida) | PR mergeado |
| Salida (reneging) | PR cerrado sin merge: la entidad abandona la cola |

## 4.3. Variables y parámetros

| Parámetro | Origen | Rol |
| :---- | :---- | :---- |
| Tasa de llegadas (λ) | Medido de datos reales | Entrada del modelo y variable de los escenarios de estrés |
| Número de revisores (c) | Estimado de los datos | Capacidad del recurso, palanca de mitigación |
| Tasa de servicio (μ) | Calibrado | Velocidad de revisión por revisor |
| Probabilidad de abandono | Estimado de los datos | Fracción de PRs que se cierran sin merge |

## 4.4. Reglas del sistema

1. Los PRs llegan según un **proceso de Poisson** con la tasa λ estimada de los datos (unidad de tiempo: **días**). El supuesto de llegadas exponenciales se **verifica contra los interarribos reales** antes de adoptarlo.
2. La cola se atiende con disciplina **FIFO**: si hay un revisor libre, el PR entra en revisión; si no, espera en la cola por orden de llegada.
3. El tiempo de revisión (servicio) sigue la distribución positiva calibrada (ver §4.5).
4. Cada PR tiene un **tiempo de paciencia** propio: si su espera en cola supera ese umbral antes de ser atendido, abandona el sistema sin merge (*reneging*). La distribución de paciencia se calibra para reproducir la fracción de PRs cerrados sin merge observada en los datos.
5. Al terminar la revisión, el PR sale del sistema como mergeado.

## 4.5. Metodología de calibración

El tiempo total en sistema observable en los datos es la suma del tiempo de espera más el tiempo de servicio, y ambos no son separables a partir de la API. Por eso el tiempo de servicio no se mide de forma directa, sino que se calibra:

1. Se fija la tasa de llegadas λ a partir de los datos del período base (PRs creados en 2024; ver [Etapas 2 y 3](etapa2_3_datos.md), §2.4).
2. Se ancla el número de revisores c con una estimación de revisores **activos**: a partir de las cuentas que figuran como autoras del merge (`merged_by`) en el período, se examina la distribución de merges por cuenta y se retienen las cuentas activas (por encima de un umbral justificado), descartando la cola de cuentas con aportes esporádicos que no representan capacidad de revisión sostenida.
3. Se propone una distribución de tiempo de servicio —se ajustan como candidatas **lognormal** y **gamma**, eligiendo la de mejor bondad de ajuste (por ejemplo, prueba de Kolmogórov-Smirnov o log-verosimilitud)— y se ajustan sus parámetros hasta que la **distribución completa** del tiempo en sistema simulado (no solo su promedio) reproduzca la distribución real observada. La validación del tiempo en sistema se realiza sobre los **PRs mergeados** (cuyo tiempo = espera + servicio); la **fracción de PRs abandonados** se valida por separado, como segundo objetivo de la calibración.
4. Se reporta la utilización resultante (ρ) para verificar que el escenario base se encuentra en un régimen sano (ρ cómodamente menor a 1).

Este procedimiento es coherente con el principio, recogido en los apuntes de la cátedra, de que una simulación debe validarse contra el comportamiento del sistema real antes de usarse para extrapolar.

## 4.6. Escenarios a simular

**Parámetros comunes de la corrida.** Para que los resultados sean estadísticamente fiables, cada escenario se corre con: un **período de calentamiento** (*warm-up*) de 90 días que se descarta para eliminar el transitorio inicial; un **horizonte** de 5 años simulados de régimen por réplica; **30 réplicas independientes** con semillas distintas; y el reporte de cada métrica como **media con intervalo de confianza del 95 %**. La semilla base se fija para garantizar la reproducibilidad. (Son valores propuestos, ajustables si la estabilización de las métricas lo requiere.)

Siguiendo la sugerencia de la consigna de cambiar una variable a la vez:

* **Escenario base:** parámetros reales calibrados. Sirve para validar el modelo.
* **Escenario de estrés:** aumento progresivo de λ para localizar el punto de saturación (ρ cerca de 1) y observar el crecimiento desproporcionado de la cola y del tiempo de espera.
* **Mitigación 1:** aumentar el número de revisores (c).
* **Mitigación 2:** incorporar un filtro automático de primera etapa que descarta un porcentaje de PRs de baja calidad antes de la revisión humana (modelo de dos etapas).
* **Mitigación 3:** limitar la cantidad de PRs concurrentes por contribuyente, inspirada en la función real lanzada por GitHub en junio de 2026; equivale a una política de control de admisión a la cola.

## 4.7. Métricas de salida

* Tiempo promedio en sistema (tiempo hasta el merge).
* Largo promedio de la cola (PRs abiertos acumulados).
* Utilización de los revisores (ρ).
* Fracción de PRs abandonados sin merge.

## 4.8. Herramientas de esta etapa

* **Python** como lenguaje base.
* **SimPy** para la simulación de eventos discretos.
* **SciPy / NumPy** para el ajuste de distribuciones y el cálculo numérico.
* **Matplotlib** para la visualización de resultados.

> **Pendiente de ejecución:** código de la simulación, gráficos de cola y tiempo de espera por escenario, y tabla comparativa de mitigaciones.

---
[ ↩ Volver al índice principal](index.md)