"""Run the recovered historical CSM Batch backtest against the live core.

The live strategy module is deliberately read-only. This runner supplies the
configuration and accounting convention recovered from the report headed
``CSM BATCH — PERFORMANCE REPORT``:

* load 2001-01-01 through 2012-12-31; report 2003-01-01 onward;
* 15 names, monthly rebalance, ATR trailing stops, 5-day stop grace period;
* 15% volatility target, 0.3% one-way costs, and zero cash yield.

The recovered copy of the original ``output_stocks`` snapshot lives in
``Documents/testing/strategies/data``.  Its ``ZEEMEDIA`` file has an unadjusted
2007 corporate-action discontinuity that was absent from the historical active
universe, so historical-parity runs explicitly exclude that ticker before
benchmark, signal, and backtest calculations.
"""

from __future__ import annotations

import argparse
import contextlib
import os
import pickle
from pathlib import Path
from typing import Iterator

import pandas as pd

from live_csm_batch_strategy import CrossSectionalMomentum, load_data
from csm_batch_backtest import (
    backtest_event_driven,
    calculate_ic,
    calculate_realized_ic,
    get_trade_log,
    plot_ic,
    plot_performance,
    populate_trade_stats,
    print_report,
    print_yearly_performance,
    slice_results,
)


# HISTORICAL_DATA_FOLDER = Path("/Users/hemantsoni/Documents/testing/strategies/data")
HISTORICAL_DATA_FOLDER = Path("/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data")
DEFAULT_LOAD_START = "2000-01-01"
DEFAULT_LOAD_END = "2025-12-31"
DEFAULT_REPORT_START = "2003-01-01"
DEFAULT_RISK_FREE_RATE = 0.0

# The historical source universe did not contain this ticker.  The recovered
# Yahoo snapshot does, but its 2007-01-10 bar falls from 227.83 to 5.02 and
# creates a synthetic -94.46% trade.  Removing it restores the archived report
# exactly without touching the live strategy core or mutating source data.
HISTORICAL_EXCLUDED_TICKERS = {
    "ZEEMEDIA": "unadjusted 2007 corporate-action discontinuity",
}

# This is the report supplied for recovery. It is a validation signature, not
# a performance promise for a different data snapshot.
ARCHIVED_REPORT_SIGNATURE = {
    "cagr": 21.04,
    "max_drawdown": -13.17,
    "ann_volatility": 8.75,
    "trade_count": 1672,
}


def _load_cached_panels(cache_path: Path):
    """Load the five OHLCV panels used by the reproduction workspace.

    A cache is intentionally opt-in: it is useful for fast diagnostics, but it
    is not silently substituted for the historical ``output_stocks`` snapshot.
    """
    with cache_path.open("rb") as fh:
        panels = pickle.load(fh)
    if not isinstance(panels, (tuple, list)) or len(panels) != 5:
        raise ValueError(
            f"{cache_path} is not a CSM OHLCV cache; expected "
            "(prices, volumes, highs, lows, opens)."
        )
    if any(not isinstance(panel, pd.DataFrame) for panel in panels):
        raise ValueError(f"{cache_path} contains non-DataFrame OHLCV panels.")
    return tuple(panels)


def _resolve_data_source(
    data_folder: str | os.PathLike[str] | None,
    data_cache: str | os.PathLike[str] | None,
):
    if data_folder and data_cache:
        raise ValueError("Pass either data_folder or data_cache, not both.")

    if data_cache:
        cache_path = Path(data_cache).expanduser().resolve()
        if not cache_path.is_file():
            raise FileNotFoundError(f"OHLCV cache not found: {cache_path}")
        return _load_cached_panels(cache_path), f"cache:{cache_path}", False

    selected = Path(
        data_folder
        or os.environ.get("CSM_BATCH_DATA_DIR")
        or HISTORICAL_DATA_FOLDER
    ).expanduser()
    if not selected.is_dir():
        raise FileNotFoundError(
            "Historical CSM Batch data was not found at "
            f"{selected}. The archived report used {HISTORICAL_DATA_FOLDER}. "
            "Pass data_folder=..., --data-folder ..., or set CSM_BATCH_DATA_DIR."
        )
    panels = load_data(str(selected))
    return panels, f"folder:{selected.resolve()}", selected.resolve() == HISTORICAL_DATA_FOLDER


def _slice_panel(panel: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    return panel.loc[start:end] if not panel.empty else panel


def _apply_historical_exclusions(panels):
    """Return a non-mutating historical-universe view of all OHLCV panels."""
    prices = panels[0]
    excluded = sorted(set(prices.columns).intersection(HISTORICAL_EXCLUDED_TICKERS))
    if not excluded:
        return tuple(panels), excluded
    return tuple(panel.drop(columns=excluded, errors="ignore") for panel in panels), excluded


def _build_benchmark(prices: pd.DataFrame) -> pd.Series:
    """Equal-weight daily-return benchmark used by the recovered runner."""
    returns = prices.pct_change(fill_method=None).clip(-0.5, 0.5)
    return (1.0 + returns.mean(axis=1, skipna=True).fillna(0.0)).cumprod()


def _accounting_mode(mode: str | None) -> str:
    if mode is None or mode in {"event_driven", "historical", "legacy", "parity"}:
        return "historical"
    if mode == "modern":
        return "modern"
    raise ValueError(
        "mode must be one of event_driven, historical, legacy, parity, or modern"
    )


@contextlib.contextmanager
def _in_output_dir(output_dir: str | os.PathLike[str] | None) -> Iterator[None]:
    """Keep optional CSV/plot artifacts out of an arbitrary caller directory."""
    if output_dir is None:
        yield
        return

    destination = Path(output_dir).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    original = Path.cwd()
    try:
        os.chdir(destination)
        yield
    finally:
        os.chdir(original)


def _print_signature_check(results: dict, detailed_log: pd.DataFrame) -> None:
    """Show the compact parity check needed to identify the recovered harness."""
    observed = {
        "cagr": results["cagr"] * 100,
        "max_drawdown": results["max_drawdown"] * 100,
        "ann_volatility": results["ann_volatility"] * 100,
        "trade_count": len(detailed_log),
    }
    print("\n── Archived-report parity check ─────────────────")
    for key, target in ARCHIVED_REPORT_SIGNATURE.items():
        value = observed[key]
        if key == "trade_count":
            print(f"  {key:<16}: observed {value:>8d} | archived {target:>8d}")
        else:
            print(f"  {key:<16}: observed {value:>8.2f}% | archived {target:>8.2f}%")


def main(
    load_start: str | None = None,
    load_end: str | None = None,
    start_report: str | None = None,
    mode: str | None = None,
    universe: int | None = None,
    *,
    data_folder: str | os.PathLike[str] | None = None,
    data_cache: str | os.PathLike[str] | None = None,
    output_dir: str | os.PathLike[str] | None = None,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
    apply_historical_exclusions: bool = True,
    generate_artifacts: bool = False,
    generate_ic: bool = False,
):
    """Run CSM Batch without modifying ``live_csm_batch_strategy.py``.

    ``mode='historical'`` (the default) uses the recovered report's booking
    convention. ``mode='modern'`` keeps the newer corrected booking convention
    while retaining the same historical signal configuration.
    """
    start_load = load_start or DEFAULT_LOAD_START
    end_load = load_end or DEFAULT_LOAD_END
    report_start = start_report or DEFAULT_REPORT_START
    accounting_mode = _accounting_mode(mode)

    panels, source_label, is_historical_snapshot = _resolve_data_source(
        data_folder, data_cache
    )
    if apply_historical_exclusions:
        panels, excluded_tickers = _apply_historical_exclusions(panels)
    else:
        excluded_tickers = []
    prices, volumes, highs, lows, opens = (
        _slice_panel(panel, start_load, end_load) for panel in panels
    )
    if prices.empty:
        raise ValueError("No price rows remain after applying the load window.")

    print("Loading CSM Batch data...")
    print(f"  Source       : {source_label}")
    print(f"  Prices shape : {prices.shape}")
    print(f"  Date range   : {prices.index.min().date()} → {prices.index.max().date()}")
    if excluded_tickers:
        reasons = "; ".join(
            f"{ticker} ({HISTORICAL_EXCLUDED_TICKERS[ticker]})"
            for ticker in excluded_tickers
        )
        print(f"  [Data] Historical parity exclusion: {reasons}")
    if not is_historical_snapshot:
        print(
            "  [Parity notice] This is not the archived output_stocks snapshot; "
            "the archived performance signature is expected to differ."
        )

    benchmark_series = _build_benchmark(prices)
    csm = CrossSectionalMomentum(
        prices_df=prices,
        volumes_df=volumes,
        highs_df=highs,
        lows_df=lows,
        opens_df=opens,
        benchmark_series=benchmark_series,
        # Recovered 2003–2012 report configuration.
        lookback_months=12,
        lag_months=1,
        top_n=15,
        min_price=20.0,
        universe_top_n=universe or 1000,
        max_circuit_days=5,
        buffer_ratio=0.20,
        atr_period=14,
        atr_multiplier=3.0,
        atr_multiplier_high_vol=2.0,
        hard_stop_from_entry=0.15,
        hard_stop_from_peak=0.20,
        stop_slippage_pct=0.003,
        use_trailing_stop=True,
        stop_cooldown_days=20,
        min_hold_days=5,
        use_crash_guard=True,
        crash_guard_cooldown=10,
        corr_guard_threshold=0.8,
        vol_target=0.15,
        max_weight_per_stock=0.05,
        rebalance_months=1,
        rank_exit_dynamic=False,
    )
    csm.calculate_factors()
    csm.get_positions()

    with _in_output_dir(output_dir):
        results = backtest_event_driven(
            csm,
            initial_capital=100_000,
            transaction_cost=0.003,
            risk_free_rate=risk_free_rate,
            accounting_mode=accounting_mode,
        )
        results = slice_results(results, report_start, risk_free_rate=risk_free_rate)

        detailed_log = get_trade_log(csm)
        if not detailed_log.empty:
            detailed_log = detailed_log[
                detailed_log["Entry_Date"] >= pd.Timestamp(report_start)
            ].copy()
            detailed_log.to_csv("csm_batch_detailed_trade_log.csv", index=False)
            print(
                "[Logs] csm_batch_detailed_trade_log.csv "
                f"({len(detailed_log)} trades from {pd.Timestamp(report_start).date()})"
            )
        populate_trade_stats(results, detailed_log)

        print_report(results, historical_style=accounting_mode == "historical")
        print_yearly_performance(results["portfolio_value"])
        _print_signature_check(results, detailed_log)

        if generate_artifacts:
            benchmark_slice = benchmark_series.reindex(results["equity_curve"].index).ffill()
            plot_performance(results, benchmark_slice)
        if generate_ic:
            ic_results = calculate_ic(
                csm,
                forward_periods=1,
                method="spearman",
                report_start=report_start,
                per_component=True,
            )
            plot_ic(csm, ic_results, filename="factor_ic_batch.png")
            calculate_realized_ic(csm, method="spearman", report_start=report_start)

    return {
        "cagr": results["cagr"] * 100,
        "drawdown": results["max_drawdown"] * 100,
        "avg_drawdown": results["avg_drawdown"] * 100,
        "trade win rate": results["trade_win_rate"] * 100,
        "calmar": results["calmar"],
        "trade_count": len(detailed_log),
        "results": results,
        "trade_log": detailed_log,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--data-folder", help="Directory containing per-symbol OHLCV CSV files")
    source.add_argument("--data-cache", help="Pickle of (prices, volumes, highs, lows, opens)")
    parser.add_argument("--load-start", default=DEFAULT_LOAD_START)
    parser.add_argument("--load-end", default=DEFAULT_LOAD_END)
    parser.add_argument("--report-start", default=DEFAULT_REPORT_START)
    parser.add_argument("--universe", type=int, default=None, help="Liquidity universe size")
    parser.add_argument(
        "--risk-free-rate",
        type=float,
        default=DEFAULT_RISK_FREE_RATE,
        help="Annual cash yield as a decimal; historical report uses 0.0",
    )
    parser.add_argument(
        "--include-zeemedia",
        action="store_true",
        help="Disable the recovered historical universe exclusion for ZEEMEDIA",
    )
    parser.add_argument(
        "--mode",
        choices=("historical", "modern"),
        default="historical",
        help="Historical report booking or corrected modern booking",
    )
    parser.add_argument("--output-dir", help="Directory for CSV and optional plot artifacts")
    parser.add_argument("--artifacts", action="store_true", help="Write performance plots")
    parser.add_argument("--ic", action="store_true", help="Run and write IC diagnostics")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    main(
        load_start=args.load_start,
        load_end=args.load_end,
        start_report=args.report_start,
        mode=args.mode,
        universe=args.universe,
        data_folder=args.data_folder,
        data_cache=args.data_cache,
        output_dir=args.output_dir,
        risk_free_rate=args.risk_free_rate,
        apply_historical_exclusions=not args.include_zeemedia,
        generate_artifacts=args.artifacts,
        generate_ic=args.ic,
    )
