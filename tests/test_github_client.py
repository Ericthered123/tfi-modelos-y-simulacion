import pytest

from src.github_client import (
    GraphQLError,
    check_payload,
    fetch_prs_in_month,
    normalize_node,
)


def test_normalize_node_maps_graphql_fields():
    node = {
        "number": 123,
        "createdAt": "2024-03-01T00:00:00Z",
        "mergedAt": "2024-03-06T00:00:00Z",
        "closedAt": "2024-03-06T00:00:00Z",
        "author": {"login": "alice", "__typename": "User"},
        "mergedBy": {"login": "maintainer1"},
    }
    assert normalize_node(node) == {
        "number": 123,
        "created_at": "2024-03-01T00:00:00Z",
        "merged_at": "2024-03-06T00:00:00Z",
        "closed_at": "2024-03-06T00:00:00Z",
        "author_login": "alice",
        "author_type": "User",
        "merged_by": "maintainer1",
    }


def test_normalize_node_handles_null_author_and_merged_by():
    # Cuentas eliminadas o PR sin merge: author / mergedBy pueden venir null.
    node = {
        "number": 7,
        "createdAt": "2024-03-01T00:00:00Z",
        "mergedAt": None,
        "closedAt": "2024-03-02T00:00:00Z",
        "author": None,
        "mergedBy": None,
    }
    row = normalize_node(node)
    assert row["author_login"] is None
    assert row["author_type"] is None
    assert row["merged_by"] is None


def test_check_payload_returns_data_when_ok():
    assert check_payload({"data": {"search": {}}}) == {"search": {}}


def test_check_payload_raises_on_graphql_errors():
    # GraphQL responde HTTP 200 aun con errores: hay que mirarlos explícitamente.
    with pytest.raises(GraphQLError):
        check_payload({"data": None, "errors": [{"message": "boom"}]})


def test_fetch_prs_in_month_follows_cursor_across_pages():
    pages = {
        None: {
            "search": {
                "pageInfo": {"hasNextPage": True, "endCursor": "CURSOR1"},
                "nodes": [{"number": 1}, {"number": 2}],
            }
        },
        "CURSOR1": {
            "search": {
                "pageInfo": {"hasNextPage": False, "endCursor": None},
                "nodes": [{"number": 3}],
            }
        },
    }
    calls = []

    def fake_request_page(token, query, cursor):
        calls.append(cursor)
        return pages[cursor]

    nodes = fetch_prs_in_month(
        "tok", "pandas-dev/pandas", 2024, 1, request_page=fake_request_page
    )

    assert [n["number"] for n in nodes] == [1, 2, 3]
    assert calls == [None, "CURSOR1"]  # arrancó sin cursor y siguió el endCursor
