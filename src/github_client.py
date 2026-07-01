"""Cliente de la API GraphQL de GitHub para extraer Pull Requests.

Usa el `search` de GraphQL (que devuelve `mergedBy` inline, evitando una llamada de
detalle por PR) con ventanas mensuales para no superar el tope de 1000 resultados por
búsqueda. Devuelve los nodos crudos (capa bronze); la normalización a la forma que
espera `transform.pr_to_row` se hace con `normalize_node`.
"""
from __future__ import annotations

import calendar
import time
from typing import Callable

import requests

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

_SEARCH_QUERY = """
query($q: String!, $cursor: String) {
  search(query: $q, type: ISSUE, first: 100, after: $cursor) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number
        createdAt
        mergedAt
        closedAt
        author { login __typename }
        mergedBy { login }
      }
    }
  }
  rateLimit { remaining resetAt cost }
}
"""


class GraphQLError(RuntimeError):
    """La API devolvió errores GraphQL (HTTP 200 con bloque `errors`)."""


def check_payload(payload: dict) -> dict:
    """Valida la respuesta GraphQL y devuelve su bloque `data`.

    GraphQL responde HTTP 200 aun ante errores, por lo que hay que inspeccionar
    explícitamente el array `errors`.
    """
    errors = payload.get("errors")
    if errors:
        raise GraphQLError(f"La API de GitHub devolvió errores: {errors}")
    return payload["data"]


def normalize_node(node: dict) -> dict:
    """Mapea un nodo `PullRequest` de GraphQL a la forma que espera `transform`."""
    author = node.get("author") or {}
    merged_by = node.get("mergedBy") or {}
    return {
        "number": node["number"],
        "created_at": node["createdAt"],
        "merged_at": node.get("mergedAt"),
        "closed_at": node.get("closedAt"),
        "author_login": author.get("login"),
        "author_type": author.get("__typename"),
        "merged_by": merged_by.get("login"),
    }


def _request_page(token: str, query: str, cursor: str | None) -> dict:
    """Ejecuta una página de la búsqueda GraphQL y devuelve el bloque `data`.

    Reintenta ante rate limit secundario (403/429) con backoff exponencial.
    """
    headers = {"Authorization": f"bearer {token}"}
    variables = {"q": query, "cursor": cursor}
    body = {"query": _SEARCH_QUERY, "variables": variables}

    for attempt in range(5):
        response = requests.post(
            GITHUB_GRAPHQL_URL, json=body, headers=headers, timeout=30
        )
        if response.status_code in (403, 429):
            time.sleep(2**attempt)
            continue
        response.raise_for_status()
        return check_payload(response.json())

    raise GraphQLError("Se agotaron los reintentos por rate limit de la API de GitHub.")


def fetch_prs_in_month(
    token: str,
    repo: str,
    year: int,
    month: int,
    *,
    request_page: Callable[[str, str, str | None], dict] = _request_page,
) -> list[dict]:
    """Devuelve los nodos crudos de todos los PRs creados en el mes dado.

    `request_page` se inyecta para poder testear la paginación sin tocar la red.
    """
    last_day = calendar.monthrange(year, month)[1]
    query = (
        f"repo:{repo} is:pr "
        f"created:{year}-{month:02d}-01..{year}-{month:02d}-{last_day:02d}"
    )

    nodes: list[dict] = []
    cursor: str | None = None
    while True:
        search = request_page(token, query, cursor)["search"]
        nodes.extend(node for node in search["nodes"] if node)
        page_info = search["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    return nodes
