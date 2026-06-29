---
title: Etapas 2 y 3 - Datos
nav_order: 3
---

# Etapas 2 y 3: Recolección, estructuración y limpieza de datos

> Esta sección presenta la metodología de obtención y preparación de datos, junto con la exploración preliminar ya realizada. Las tablas finales y las capturas del entorno de trabajo se incorporarán durante la fase de ejecución.

## 2.1. Fuente de datos

La fuente principal es un **repositorio digital abierto**: el repositorio `pandas-dev/pandas` alojado en GitHub. Los datos se obtienen de la **API de GitHub**, que expone, para cada Pull Request, los campos necesarios para reconstruir la dinámica del sistema de colas.

Se evalúan dos vías de extracción, ambas válidas según la consigna:

1. **API REST de GitHub mediante un script en Python** (vía preferida). Permite obtener, por PR, los campos `created_at`, `merged_at`, `closed_at`, el autor y su tipo (humano o bot), y la cantidad de comentarios de revisión. La autenticación se realiza con un token personal del estudiante, en su propio entorno.
2. **GH Archive consultado mediante BigQuery** (alternativa). Un conjunto de datos público que registra todos los eventos públicos de GitHub, útil para reconstruir tasas de llegada agregadas a lo largo del tiempo.

Como fuente complementaria de contexto (tendencias de búsqueda), se prevé usar **Google Trends** para evidenciar el crecimiento del interés en herramientas de generación de código por IA (por ejemplo, "Copilot", "Cursor", "AI coding agent").

## 2.2. Variables a recolectar

| Campo | Uso en el modelo |
| :---- | :---- |
| `created_at` | Marca de llegada del PR a la cola |
| `merged_at` / `closed_at` | Marca de salida (atendido o abandonado) |
| Tiempo total en sistema (derivado) | Distribución objetivo para la calibración |
| Autor y tipo de autor | Distinción entre contribuciones humanas y automáticas |
| Revisores que mergean | Estimación del número de revisores activos (parámetro c) |

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