---
title: Inicio
nav_order: 1
---

# Portafolio Digital: Trabajo Final Integrador (TFI)

* **Asignatura:** Modelos y Simulación
* **Carrera:** Ingeniería en Informática (UNNOBA)
* **Estudiante:** Eric Doyle

---

## Presentación del proyecto

Este portafolio registra, de forma transparente y cronológica, el proceso de investigación, modelado y simulación desarrollado para el TFI de la materia.

El proyecto estudia la **saturación del pipeline de revisión de Pull Requests (PRs) en proyectos de código abierto**. El fenómeno de fondo es un desajuste de capacidades: la irrupción de la IA generativa y de los agentes automáticos abarató y aceleró enormemente la *generación* de contribuciones de código, mientras que la *revisión e integración* de ese código sigue dependiendo del esfuerzo cognitivo de un número limitado de mantenedores humanos. Cuando la tasa de llegada de contribuciones crece y la capacidad de revisión permanece fija, el sistema se comporta como una cola que tiende a la saturación.

El trabajo modela ese pipeline como un **sistema de colas (M/M/c)** mediante **simulación de eventos discretos**, lo calibra con datos reales del repositorio `pandas-dev/pandas`, y lo utiliza para localizar el punto en que el sistema colapsa y para evaluar estrategias de mitigación.

> **Estado actual del proyecto:** fase de diseño y planificación. La Etapa 1 (definición del problema) y la justificación documentada están completas. Las Etapas 2 a 5 están definidas a nivel de metodología (qué se hará y cómo); sus resultados se incorporarán durante la fase de ejecución.

---

## Índice de navegación

* [Etapa 1: Definición del problema y objetivos](etapa1_problema.md)
* [Etapas 2 y 3: Recolección y limpieza de datos](etapa2_3_datos.md)
* [Etapa 4: Formulación del modelo e implementación de la simulación](etapa4_modelo.md)
* [Etapa 5: Documentación del proceso y conclusiones](etapa5_documentacion.md)
* [Bitácora de uso crítico de IA y herramientas](bitacora_ia.md)

---

## Mapa de cumplimiento de la consigna

La siguiente tabla relaciona cada requisito de la consigna oficial con la sección del portafolio que lo aborda y su estado.

| Requisito de la consigna | Sección del portafolio | Estado |
| :---- | :---- | :---- |
| Datos de la asignatura y del estudiante | Esta página (inicio) | Completo |
| Presentación del problema | Etapa 1 | Completo |
| Definición del problema, objetivos y pregunta de investigación | Etapa 1 | Completo |
| Justificación del interés del fenómeno (con evidencia) | Etapa 1 | Completo |
| Recolección de datos digitales | Etapas 2 y 3 | Diseño completo, ejecución pendiente |
| Estructuración y limpieza de datos | Etapas 2 y 3 | Diseño completo, ejecución pendiente |
| Tablas con datos recolectados y procesados | Etapas 2 y 3 | Exploración preliminar incluida, tablas finales pendientes |
| Descripción del modelo y de la simulación | Etapa 4 | Completo (diseño); implementación pendiente |
| Archivos de simulación, gráficos y resultados | Etapa 4 | Pendiente de ejecución |
| Prompts utilizados con IA y otras herramientas | Bitácora | En curso |
| Capturas de pantalla de entornos, código y planillas | Bitácora y Etapas 2 a 4 | Pendiente de ejecución |
| Informe final, conclusiones y reflexión crítica | Etapa 5 | En curso |

---

## Uso de herramientas tecnológicas

De acuerdo con la consigna, el trabajo integra herramientas tecnológicas con criterio y de forma transparente. El detalle de qué herramienta se usó en cada etapa, los prompts completos, las capturas y la reflexión crítica correspondiente se registran en la [Bitácora de uso crítico de IA y herramientas](bitacora_ia.md).