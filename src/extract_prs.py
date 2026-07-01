"""Orquestador de extracción de PRs de `pandas-dev/pandas`.

Recorre los 12 meses de un año, guarda el JSON crudo (bronze) por mes y escribe un
CSV limpio (silver) con una fila por PR cerrado. Uso:

    python -m src.extract_prs --year 2024
    python -m src.extract_prs --year 2020

Requiere `GITHUB_TOKEN` en el entorno (o en un archivo `.env`; ver `.env.example`).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from src.github_client import fetch_prs_in_month, normalize_node
from src.transform import pr_to_row

REPO = "pandas-dev/pandas"
_ROOT = Path(__file__).resolve().parents[1]
_RAW_DIR = _ROOT / "data" / "raw"
_CLEAN_DIR = _ROOT / "data" / "clean"

_CSV_COLUMNS = [
    "number",
    "created_at",
    "merged_at",
    "closed_at",
    "merged_by",
    "author_login",
    "author_type",
    "time_in_system_days",
    "is_merged",
]


def _load_token() -> str:
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit(
            "Falta GITHUB_TOKEN. Copiá .env.example a .env y completá el token, "
            "o exportá la variable en la shell."
        )
    return token


def extract_months(token: str, year: int, months: list[int]) -> pd.DataFrame:
    """Extrae, persiste el crudo y devuelve las filas limpias de los meses dados."""
    _RAW_DIR.mkdir(parents=True, exist_ok=True)
    _CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    total_nodes = 0
    for month in months:
        nodes = fetch_prs_in_month(token, REPO, year, month)
        total_nodes += len(nodes)

        raw_path = _RAW_DIR / f"prs_{year}_{month:02d}.json"
        raw_path.write_text(json.dumps(nodes, indent=2), encoding="utf-8")

        for node in nodes:
            row = pr_to_row(normalize_node(node))
            if row is not None:  # descarta censurados (sin fecha de cierre)
                rows.append(row)
        print(f"  {year}-{month:02d}: {len(nodes)} PRs")

    frame = pd.DataFrame(rows, columns=_CSV_COLUMNS)
    # Un mes suelto (smoke test) va a un CSV aparte para no pisar el del año completo.
    suffix = "" if len(months) == 12 else f"_{months[0]:02d}"
    csv_path = _CLEAN_DIR / f"prs_{year}{suffix}.csv"
    frame.to_csv(csv_path, index=False)

    discarded = total_nodes - len(frame)
    print(
        f"Año {year} ({len(months)} mes/es): {total_nodes} PRs recolectados, "
        f"{len(frame)} cerrados escritos, {discarded} descartados por censura → {csv_path}"
    )
    return frame


def main() -> None:
    # La consola de Windows usa cp1252 por defecto y no puede imprimir caracteres
    # como "→" o acentos; forzamos UTF-8 para que el resumen no rompa.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Extrae PRs de pandas-dev/pandas.")
    parser.add_argument("--year", type=int, required=True, help="Año a extraer (ej. 2024)")
    parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        metavar="1-12",
        help="Extraer un solo mes (para el smoke test). Por defecto, el año completo.",
    )
    args = parser.parse_args()

    months = [args.month] if args.month else list(range(1, 13))
    token = _load_token()
    extract_months(token, args.year, months)


if __name__ == "__main__":
    main()
