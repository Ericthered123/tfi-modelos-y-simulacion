"""Orquestador de la capa gold: destila el silver en agregados de calibración.

Lee el CSV silver de un año (`data/clean/prs_{year}.csv`), computa los parámetros del
modelo M/M/c con `src.gold` y escribe la capa gold: tablas en `data/gold/` y gráficos
descriptivos en `charts/`. No toca la red. Uso:

    python -m src.aggregate_gold --year 2024
    python -m src.aggregate_gold --year 2024 --threshold 20

`--threshold` es el umbral de merges para contar una cuenta como revisor activo
(estimación de c, Etapa 4 §4.5). Si se omite, se usa `_DEFAULT_THRESHOLD`; es una
decisión de modelado ajustable.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin display: solo escribe PNG
import matplotlib.pyplot as plt
import pandas as pd

from src import gold

_ROOT = Path(__file__).resolve().parents[1]
_CLEAN_DIR = _ROOT / "data" / "clean"
_GOLD_DIR = _ROOT / "data" / "gold"
_CHARTS_DIR = _ROOT / "charts"

# Umbral de merges para contar una cuenta como revisor activo (parámetro c). El corte
# en 10 se apoya en una discontinuidad real de la distribución 2024: 8 cuentas core con
# >= 22 merges y una cola esporádica de <= 7. Ver Etapa 4 §4.5. Ajustable con --threshold.
_DEFAULT_THRESHOLD = 10.0


def _window_days(year: int) -> int:
    """Días de la ventana de llegadas: el año calendario completo del silver."""
    return (date(year + 1, 1, 1) - date(year, 1, 1)).days


def _plot_time_in_system(series: pd.Series, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(series, bins=60, color="#4C72B0", edgecolor="white", linewidth=0.3)
    ax.set_title("Distribución del tiempo en sistema (PRs mergeados) — 2024")
    ax.set_xlabel("Tiempo en sistema (días)")
    ax.set_ylabel("Cantidad de PRs")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _plot_daily_arrivals(counts: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(pd.to_datetime(counts["date"]), counts["count"], color="#55A868", linewidth=1)
    ax.set_title("Llegadas diarias de PRs — 2024")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("PRs creados por día")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _plot_merges_per_reviewer(merges: pd.Series, threshold: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(range(len(merges)), merges.to_numpy(), color="#C44E52")
    ax.axhline(
        threshold,
        color="black",
        linestyle="--",
        linewidth=1,
        label=f"umbral activo = {threshold:.1f}",
    )
    ax.set_title("Merges por cuenta (revisores) — 2024")
    ax.set_xlabel("Cuentas ordenadas por nº de merges")
    ax.set_ylabel("Merges realizados")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def build_gold(year: int, threshold: float | None = None) -> dict:
    """Computa y persiste la capa gold para un año. Devuelve los parámetros escalares."""
    silver_path = _CLEAN_DIR / f"prs_{year}.csv"
    if not silver_path.exists():
        raise SystemExit(
            f"No existe el silver {silver_path}. Corré antes `python -m src.extract_prs "
            f"--year {year}`."
        )

    _GOLD_DIR.mkdir(parents=True, exist_ok=True)
    _CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(silver_path)
    merges = gold.merges_per_reviewer(df)
    if threshold is None:
        threshold = _DEFAULT_THRESHOLD

    window_days = _window_days(year)
    params = gold.summarize_params(df, threshold=threshold, window_days=window_days)

    # Tablas gold.
    gold.daily_arrival_counts(df).to_csv(
        _GOLD_DIR / f"daily_arrivals_{year}.csv", index=False
    )
    time_in_system = gold.time_in_system_merged(df)
    df.loc[df["is_merged"], ["number", "time_in_system_days"]].to_csv(
        _GOLD_DIR / f"time_in_system_merged_{year}.csv", index=False
    )
    merges.rename_axis("merged_by").rename("merge_count").to_csv(
        _GOLD_DIR / f"merges_per_reviewer_{year}.csv"
    )
    (_GOLD_DIR / f"params_{year}.json").write_text(
        json.dumps(params, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Gráficos descriptivos.
    _plot_time_in_system(time_in_system, _CHARTS_DIR / f"hist_time_in_system_{year}.png")
    _plot_daily_arrivals(
        gold.daily_arrival_counts(df), _CHARTS_DIR / f"daily_arrivals_{year}.png"
    )
    _plot_merges_per_reviewer(
        merges, threshold, _CHARTS_DIR / f"merges_per_reviewer_{year}.png"
    )

    return params


def _print_summary(year: int, params: dict) -> None:
    tis = params["time_in_system"]
    print(f"Capa gold {year} generada → data/gold/ y charts/")
    print(f"  Llegadas (n)          : {params['n_arrivals']}")
    print(f"  Mergeados / abandonados: {params['n_merged']} / {params['n_abandoned']}")
    print(f"  λ (PRs/día)           : {params['arrival_rate_per_day']:.3f}")
    print(f"  Prob. de abandono     : {params['abandonment_probability']:.3f}")
    print(
        f"  Revisores activos (c) : {params['active_reviewers_c']} "
        f"(umbral ≥ {params['threshold']:.1f} merges)"
    )
    print(
        f"  Tiempo en sistema      : media {tis['mean']:.2f} d, mediana "
        f"{tis['median']:.2f} d, máx {tis['max']:.2f} d"
    )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Genera la capa gold (agregados de calibración) desde el silver."
    )
    parser.add_argument("--year", type=int, required=True, help="Año a agregar (ej. 2024)")
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help=f"Umbral de merges para revisor activo (c). Por defecto, {_DEFAULT_THRESHOLD}.",
    )
    args = parser.parse_args()

    params = build_gold(args.year, args.threshold)
    _print_summary(args.year, params)


if __name__ == "__main__":
    main()
