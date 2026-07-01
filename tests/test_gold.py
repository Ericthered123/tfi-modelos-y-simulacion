import math

import pandas as pd

from src.gold import (
    abandonment_probability,
    active_reviewers,
    arrival_rate_per_day,
    daily_arrival_counts,
    merges_per_reviewer,
    summarize_params,
    time_in_system_merged,
)


def _silver(rows: list[dict]) -> pd.DataFrame:
    """Arma un DataFrame silver mínimo a partir de filas parciales.

    Completa las columnas faltantes con valores neutros para que las funciones
    puras reciban el esquema esperado.
    """
    columns = {
        "number": 0,
        "created_at": "2024-03-01T00:00:00Z",
        "merged_at": None,
        "closed_at": "2024-03-02T00:00:00Z",
        "merged_by": None,
        "author_login": "alice",
        "author_type": "User",
        "time_in_system_days": 1.0,
        "is_merged": False,
    }
    return pd.DataFrame([{**columns, **row} for row in rows])


def test_daily_arrival_counts_groups_by_creation_date():
    df = _silver(
        [
            {"created_at": "2024-03-01T08:00:00Z"},
            {"created_at": "2024-03-01T20:00:00Z"},
            {"created_at": "2024-03-02T10:00:00Z"},
        ]
    )
    counts = daily_arrival_counts(df)
    assert list(counts["count"]) == [2, 1]
    assert str(counts["date"].iloc[0]) == "2024-03-01"


def test_arrival_rate_per_day_is_count_over_window():
    df = _silver([{}, {}, {}, {}])  # 4 llegadas
    assert math.isclose(arrival_rate_per_day(df, window_days=2), 2.0)


def test_abandonment_probability_is_share_not_merged():
    df = _silver(
        [
            {"is_merged": True},
            {"is_merged": True},
            {"is_merged": True},
            {"is_merged": False},
        ]
    )
    assert math.isclose(abandonment_probability(df), 0.25)


def test_merges_per_reviewer_counts_only_merged_sorted_desc():
    df = _silver(
        [
            {"is_merged": True, "merged_by": "maint_a"},
            {"is_merged": True, "merged_by": "maint_a"},
            {"is_merged": True, "merged_by": "maint_b"},
            {"is_merged": False, "merged_by": None},  # abandonado, no cuenta
        ]
    )
    merges = merges_per_reviewer(df)
    assert list(merges.index) == ["maint_a", "maint_b"]
    assert list(merges.values) == [2, 1]


def test_active_reviewers_retains_accounts_at_or_above_threshold():
    merges = pd.Series({"maint_a": 10, "maint_b": 4, "maint_c": 1})
    count, retained = active_reviewers(merges, threshold=4)
    assert count == 2
    assert set(retained) == {"maint_a", "maint_b"}


def test_time_in_system_merged_filters_to_merged_prs():
    df = _silver(
        [
            {"is_merged": True, "time_in_system_days": 5.0},
            {"is_merged": True, "time_in_system_days": 3.0},
            {"is_merged": False, "time_in_system_days": 99.0},  # abandonado, excluido
        ]
    )
    series = time_in_system_merged(df)
    assert sorted(series.tolist()) == [3.0, 5.0]


def test_summarize_params_reports_calibration_scalars():
    df = _silver(
        [
            {"is_merged": True, "merged_by": "maint_a", "time_in_system_days": 2.0},
            {"is_merged": True, "merged_by": "maint_a", "time_in_system_days": 4.0},
            {"is_merged": False, "merged_by": None, "time_in_system_days": 1.0},
        ]
    )
    params = summarize_params(df, threshold=2, window_days=3)

    assert params["n_arrivals"] == 3
    assert params["n_merged"] == 2
    assert params["n_abandoned"] == 1
    assert math.isclose(params["arrival_rate_per_day"], 1.0)
    assert math.isclose(params["abandonment_probability"], 1 / 3)
    assert params["active_reviewers_c"] == 1
    assert math.isclose(params["threshold"], 2)
    assert params["window_days"] == 3
    # El resumen del tiempo en sistema se calcula solo sobre mergeados.
    assert math.isclose(params["time_in_system"]["mean"], 3.0)
    assert math.isclose(params["time_in_system"]["min"], 2.0)
    assert math.isclose(params["time_in_system"]["max"], 4.0)
