"""Agregados de calibración (capa gold) derivados del CSV silver.

Este módulo NO hace I/O ni grafica: recibe un ``DataFrame`` silver (una fila por PR
cerrado, con el esquema que escribe ``src.extract_prs``) y devuelve los parámetros y
tablas que alimentan el modelo M/M/c de la Etapa 4 (λ, fracción de abandono, revisores
activos c y la distribución objetivo del tiempo en sistema). La persistencia y los
gráficos viven en ``src.aggregate_gold``.
"""
from __future__ import annotations

import pandas as pd


def daily_arrival_counts(df: pd.DataFrame) -> pd.DataFrame:
    """PRs creados por día, ordenados por fecha. Columnas: ``date``, ``count``."""
    created = pd.to_datetime(df["created_at"], utc=True).dt.date
    counts = created.value_counts().sort_index()
    return pd.DataFrame({"date": counts.index, "count": counts.to_numpy()})


def arrival_rate_per_day(df: pd.DataFrame, window_days: int) -> float:
    """Tasa de llegadas λ = nº de PRs / días de la ventana de observación."""
    return len(df) / window_days


def abandonment_probability(df: pd.DataFrame) -> float:
    """Fracción de PRs cerrados sin merge (``is_merged == False``)."""
    return float((~df["is_merged"]).mean())


def merges_per_reviewer(df: pd.DataFrame) -> pd.Series:
    """Conteo de merges por cuenta ``merged_by`` (solo mergeados), orden desc.

    Base para estimar el número de revisores activos (parámetro c).
    """
    merged = df.loc[df["is_merged"], "merged_by"].dropna()
    return merged.value_counts()


def active_reviewers(merges: pd.Series, threshold: float) -> tuple[int, list[str]]:
    """Revisores activos: cuentas con al menos ``threshold`` merges.

    Descarta la cola de cuentas con aportes esporádicos, que no representan capacidad
    de revisión sostenida (Etapa 4, §4.5). Devuelve (c, cuentas retenidas).
    """
    retained = merges[merges >= threshold]
    return len(retained), list(retained.index)


def time_in_system_merged(df: pd.DataFrame) -> pd.Series:
    """Tiempo en sistema (días) de los PRs mergeados: la distribución objetivo.

    La calibración de μ (Etapa 4) valida contra esta distribución, no contra el
    promedio. Se excluyen los abandonados, cuyo tiempo no es tiempo de servicio.
    """
    return df.loc[df["is_merged"], "time_in_system_days"].reset_index(drop=True)


def _summarize_series(series: pd.Series) -> dict:
    return {
        "mean": float(series.mean()),
        "median": float(series.median()),
        "p25": float(series.quantile(0.25)),
        "p75": float(series.quantile(0.75)),
        "std": float(series.std()),
        "min": float(series.min()),
        "max": float(series.max()),
    }


def summarize_params(df: pd.DataFrame, threshold: float, window_days: int) -> dict:
    """Reúne los parámetros escalares de calibración en un dict serializable."""
    merges = merges_per_reviewer(df)
    c, retained = active_reviewers(merges, threshold)
    n_merged = int(df["is_merged"].sum())

    return {
        "window_days": window_days,
        "n_arrivals": int(len(df)),
        "n_merged": n_merged,
        "n_abandoned": int(len(df) - n_merged),
        "arrival_rate_per_day": arrival_rate_per_day(df, window_days),
        "abandonment_probability": abandonment_probability(df),
        "threshold": threshold,
        "active_reviewers_c": c,
        "active_reviewer_accounts": retained,
        "time_in_system": _summarize_series(time_in_system_merged(df)),
    }
