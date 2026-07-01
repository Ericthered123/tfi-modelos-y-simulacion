"""Transformación pura de PRs crudos (API) a filas limpias para el análisis.

Este módulo NO hace I/O de red: recibe PRs ya normalizados (dicts) y devuelve
las filas listas para el CSV `silver`, aplicando el criterio de censura.
"""
from __future__ import annotations

from datetime import datetime

_SECONDS_PER_DAY = 86_400


def parse_timestamp(value: str | None) -> datetime | None:
    """Convierte un timestamp ISO 8601 de la API (con sufijo `Z`) a datetime UTC."""
    if value is None:
        return None
    return datetime.fromisoformat(value)


def pr_to_row(pr: dict) -> dict | None:
    """Deriva la fila limpia de un PR normalizado.

    Devuelve ``None`` si el PR no tiene fecha de cierre (aún abierto): se descarta
    para evitar el sesgo de censura por la derecha en la distribución del tiempo en
    sistema (ver Etapa 2, §2.4 del portafolio).
    """
    created = parse_timestamp(pr["created_at"])
    closed = parse_timestamp(pr["closed_at"])
    if closed is None:
        return None

    merged = parse_timestamp(pr["merged_at"])
    time_in_system_days = (closed - created).total_seconds() / _SECONDS_PER_DAY

    return {
        "number": pr["number"],
        "created_at": pr["created_at"],
        "merged_at": pr["merged_at"],
        "closed_at": pr["closed_at"],
        "merged_by": pr["merged_by"],
        "author_login": pr["author_login"],
        "author_type": pr["author_type"],
        "time_in_system_days": time_in_system_days,
        "is_merged": merged is not None,
    }
