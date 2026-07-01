---
title: Etapas 2 y 3 - Datos
nav_order: 3
---

# Etapas 2 y 3: Recolección, estructuración y limpieza de datos

> Esta sección presenta la metodología de obtención y preparación de datos, junto con la exploración preliminar ya realizada. Las tablas finales y las capturas del entorno de trabajo se incorporarán durante la fase de ejecución.

## 2.1. Fuente de datos

La fuente principal es un **repositorio digital abierto**: el repositorio `pandas-dev/pandas` alojado en GitHub. Los datos se obtienen de la **API de GitHub**, que expone, para cada Pull Request, los campos necesarios para reconstruir la dinámica del sistema de colas.

Se evalúan dos vías de extracción, ambas válidas según la consigna:

1. **API GraphQL de GitHub mediante un script en Python** (vía elegida). Permite obtener, por PR y en una sola consulta paginada, los campos `created_at`, `merged_at`, `closed_at`, el autor y su tipo de cuenta, y —de forma *inline*— la cuenta que realizó el merge (`mergedBy`). Se optó por GraphQL antes que por REST precisamente por esto último: REST no expone `mergedBy` en el listado de PRs y exigiría una llamada de detalle por cada PR (miles de peticiones), mientras que GraphQL lo devuelve junto al resto con 100 PRs por página. La autenticación se realiza con un token personal del estudiante, en su propio entorno.
2. **GH Archive consultado mediante BigQuery** (alternativa). Un conjunto de datos público que registra todos los eventos públicos de GitHub, útil para reconstruir tasas de llegada agregadas a lo largo del tiempo.

Como **fuente complementaria de contexto** se utiliza **Google Trends** para evidenciar el crecimiento del interés en herramientas de generación de código por IA (por ejemplo, "Copilot", "Cursor", "AI coding agent"). Este dato respalda la **premisa** del trabajo —que la generación de contribuciones asistida por IA creció y se popularizó en el período—; **no es una entrada del modelo** ni se mide sobre `pandas`. Su rol es sostener la relevancia y actualidad del escenario de estrés analizado (ver [Etapa 1](etapa1_problema.md)).

## 2.2. Variables a recolectar

| Campo | Uso en el modelo |
| :---- | :---- |
| `created_at` | Marca de llegada del PR a la cola |
| `merged_at` / `closed_at` | Marca de salida (atendido o abandonado) |
| Tiempo total en sistema (derivado) | Distribución objetivo para la calibración |
| Autor y tipo de cuenta | Caracterización del origen de los PRs: identifica cuentas registradas como bot (`user.type`), como contexto descriptivo del dataset |
| Revisores que mergean | Estimación del número de revisores activos (parámetro c) |

> **Nota sobre el tipo de cuenta.** La API solo permite identificar cuentas registradas como *bot*; **no** permite distinguir el código asistido por IA que ingresa a través de cuentas humanas. Por eso este campo se usa como contexto descriptivo del origen de los PRs, no como variable del modelo, en coherencia con el encuadre de la [Etapa 1](etapa1_problema.md), donde el aumento atribuible a la IA se trata como escenario de estrés y no como una magnitud medida.

## 2.3. Exploración preliminar (datos reales ya obtenidos)

Antes de fijar la metodología, se realizó una exploración del volumen histórico de PRs creados por año en `pandas`, consultando la API de búsqueda de GitHub. El resultado:

| Año | PRs creados |
| :---- | :---- |
| 2019 | 3452 |
| 2020 | 5333 |
| 2021 | 4101 |
| 2022 | 3475 |
| 2023 | 4108 |
| 2024 | 2548 |
| 2025 | 1977 |

**Interpretación.** El volumen de PRs en `pandas` no muestra el aumento sostenido en la era de la IA que cabría suponer; al contrario, es estable y luego decreciente, con su máximo en 2020. Este hallazgo es metodológicamente importante: confirma que la hipótesis de un aumento de llegadas atribuible a la IA no puede validarse empíricamente en este repositorio maduro, y justifica el encuadre adoptado, modelar el crecimiento de llegadas como un **escenario de estrés** sobre un modelo calibrado, y no como un contraste histórico medido. El año 2020, como período real de alta carga, queda disponible como caso de validación adicional del comportamiento del modelo.

## 2.4. Ventana temporal de calibración y validación

De la exploración anterior se desprende una decisión metodológica: qué período usar para calibrar el modelo. Se adoptan dos ventanas, ambas definidas por la fecha de creación (`created_at`) del PR:

* **Base de calibración: PRs creados durante 2024.** Es el período reciente más adecuado por dos motivos. Primero, representa el régimen actual de bajo volumen del repositorio, coherente con el encuadre de escenario de estrés. Segundo, y decisivo: a la fecha de análisis los PRs de 2024 tuvieron más de un año para resolverse, de modo que la **censura por la derecha** —PRs todavía abiertos, sin fecha de cierre— es prácticamente nula. Esto importa porque la limpieza descarta los PRs sin cierre (paso 2 de §3.1): una ventana demasiado reciente sesgaría la distribución del tiempo en sistema hacia los PRs que cierran rápido, subestimando el tiempo de servicio al calibrar. Con 2024 ese sesgo es despreciable.
* **Validación: PRs creados durante 2020.** El año de máxima carga histórica (5333 PRs), reservado como caso independiente para comprobar que el modelo calibrado reproduce también un régimen de alta demanda, y no solo el punto en el que se lo calibró.

## 3.1. Estructuración y limpieza

Una vez recolectados los datos crudos, la preparación seguirá estos pasos:

1. **Unificar formatos:** convertir todas las marcas temporales a un formato y zona horaria consistentes.
2. **Eliminar errores, duplicados y entradas incompletas:** descartar PRs sin fecha de cierre o con datos inconsistentes.
3. **Derivar variables:** calcular el tiempo total en sistema (cierre menos creación) y clasificar cada PR como humano o automático según el tipo de autor.
4. **Estructurar la base:** organizar los registros en un `DataFrame` de pandas, exportable a hoja de cálculo, con una fila por PR y las columnas necesarias para el análisis.
5. **Preparar para el análisis:** dejar la estructura lista para ajustar distribuciones (Etapa 4) y para categorizar, de ser necesario, con apoyo de IA o por medios propios.

## 3.2. Herramientas de esta etapa

* **Python** con la biblioteca `requests` (consultas a la API) y `pandas` (estructuración y limpieza).
* **SciPy / NumPy** para el posterior ajuste de distribuciones a los datos limpios.
* Hoja de cálculo para la inspección y presentación tabular.

> **Pendiente de ejecución:** tablas completas de datos recolectados y procesados, fragmentos del script de extracción, y capturas del entorno de trabajo.

---
[ ↩ Volver al índice principal](index.md)