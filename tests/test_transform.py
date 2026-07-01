import math
from datetime import datetime, timezone

from src.transform import parse_timestamp, pr_to_row


def _pr(**overrides) -> dict:
    """PR normalizado de ejemplo (mergeado por defecto)."""
    base = {
        "number": 1,
        "created_at": "2024-03-01T00:00:00Z",
        "merged_at": "2024-03-06T00:00:00Z",
        "closed_at": "2024-03-06T00:00:00Z",
        "author_login": "alice",
        "author_type": "User",
        "merged_by": "maintainer1",
    }
    base.update(overrides)
    return base


def test_parse_timestamp_handles_z_suffix():
    assert parse_timestamp("2024-03-01T00:00:00Z") == datetime(
        2024, 3, 1, tzinfo=timezone.utc
    )


def test_parse_timestamp_returns_none_for_none():
    assert parse_timestamp(None) is None


def test_merged_pr_produces_row():
    row = pr_to_row(_pr())
    assert row is not None
    assert row["is_merged"] is True
    assert row["merged_by"] == "maintainer1"
    assert math.isclose(row["time_in_system_days"], 5.0)


def test_abandoned_pr_is_counted_but_not_merged():
    row = pr_to_row(_pr(merged_at=None, merged_by=None, closed_at="2024-03-03T00:00:00Z"))
    assert row is not None
    assert row["is_merged"] is False
    assert math.isclose(row["time_in_system_days"], 2.0)


def test_open_pr_is_discarded_as_censored():
    # PR aún abierto: sin closed_at. Se descarta (censura por la derecha).
    assert pr_to_row(_pr(merged_at=None, merged_by=None, closed_at=None)) is None
