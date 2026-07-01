# CLAUDE.md - Contexto del proyecto

## Qué es este proyecto

TFI de la materia Modelos y Simulación (Ingeniería en Informática, UNNOBA), de Eric Doyle.
Modela el pipeline de revisión de Pull Requests del repositorio `pandas-dev/pandas` como un
sistema de colas (M/M/c) mediante simulación de eventos discretos, para estudiar su saturación
frente al aumento de contribuciones y evaluar estrategias de mitigación.

Para el detalle completo, leer los archivos del portafolio en la raíz:
`etapa1_problema.md`, `etapa2_3_datos.md`, `etapa4_modelo.md`, `etapa5_documentacion.md`.

## Encuadre metodológico (decisiones ya tomadas, respetar)

- El fenómeno del aumento de contribuciones por IA se modela como un ESCENARIO DE ESTRÉS sobre un
  modelo calibrado con datos reales, NO como un contraste histórico medido. Motivo: la exploración
  preliminar mostró que el volumen de PRs de `pandas` es estable o decreciente (ver etapa2_3_datos.md).
- No inventar datos ni afirmaciones. Toda evidencia externa debe verificarse contra fuentes reales.
- La tasa de llegadas (lambda) se mide de los datos reales. El tiempo de servicio (mu) NO es observable
  y se calibra iterativamente.
- Al calibrar, anclar el número de revisores (c) con una estimación de revisores activos derivada de
  los datos (cuentas distintas que mergean), y validar contra la DISTRIBUCIÓN completa del tiempo en
  sistema, no solo contra el promedio. Reportar la utilización (rho) del escenario base.
- Para el tiempo de servicio usar distribuciones positivas (triangular, lognormal o gamma), NUNCA normal
  (puede dar valores negativos, que no tienen sentido para una duración).

## Stack técnico

- Python 3.
- SimPy (simulación de eventos discretos).
- requests (consultas a la API de GitHub).
- pandas (estructuración y limpieza).
- SciPy / NumPy (ajuste de distribuciones y cálculo).
- Matplotlib (visualización).

## Comandos

Entorno virtual y dependencias (ajustar según se avance):

    python3 -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install simpy requests pandas scipy numpy matplotlib

## Estructura de trabajo sugerida

- `data/`      : datasets crudos y limpios (CSV).
- `src/`     : script de extracción y modelo de simulación.
- `charts/`   : salidas de la simulación.
- Archivos `*.md` de la raíz: portafolio (sitio Jekyll, no tocar su formato sin motivo).

Nota Jekyll: para que el sitio de GitHub Pages no procese el código, agregar los directorios de código
al `exclude` en `_config.yml` (por ejemplo: `exclude: [".venv", "src", "data", "charts", "reference"]`).

## Material de referencia de la cátedra (local, NO versionado)

En la carpeta `reference/` (local, incluida en `.gitignore`, no se sube al repo) están los apuntes de
las unidades de la materia y la consigna oficial del TFI. Es material del profesor: se puede consultar
cuando haga falta, pero NUNCA se commitea ni se publica.

Los archivos más relevantes para este trabajo:
- La consigna del TFI: usarla para verificar el cumplimiento de los requisitos al completar el portafolio.
- Apuntes de la Unidad 5 (colas y modelos en Arena): notación y conceptos del modelo principal.
- Apuntes de la Unidad 2 (generación de números aleatorios): ajuste y validación de distribuciones.

## Convenciones y límites importantes

- SEGURIDAD: el token de la API de GitHub va en una variable de entorno local (por ejemplo
  `GITHUB_TOKEN`), NUNCA hardcodeado en el código ni commiteado al repo. En `.gitignore` ya están
  excluidos `.venv`, `reference/` y los archivos con credenciales (`.env`, `*.token`, `*.key`, etc.).
- APRENDIZAJE: este es un trabajo académico que el autor debe entender y defender. Explicar el código
  que se escribe, proponer opciones y dejar explícitas las decisiones de modelado en manos del autor. No
  resolver el trabajo de forma autónoma sin que el autor dé su confirmación y entienda la decisión que se toma.
- TRANSPARENCIA: registrar en `bitacora_ia.md` los prompts y el uso de IA, ya que es un criterio de
  evaluación de la cátedra.
- IDIOMA: el contenido del portafolio se escribe en español.
- Cambiar una variable por vez en los escenarios de simulación (base, estrés, mitigaciones).
- LICENCIAS: el repo usa doble licencia. El código (p. ej. `src/`) es MIT (`LICENSE.md`); el contenido
  del portafolio (los `.md` de texto y los gráficos de `charts/`) es CC BY 4.0 (`LICENSE-CONTENT.md`).
  Al crear archivos nuevos, respetar esta distinción y no mezclar código con texto bajo la misma licencia.