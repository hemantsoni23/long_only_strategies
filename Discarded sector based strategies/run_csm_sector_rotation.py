"""
run_csm_sector_rotation.py
===========================
Thin orchestrator for the CSM Sector Rotation strategy: loads OHLCV data + the
sector map, builds the equal-weight benchmark, instantiates the strategy CORE
(csm_sector_rotation_strategy), runs the event-driven backtest engine
(csm_sector_rotation_backtest), and prints the performance report.

Split layout:
  • csm_sector_rotation_strategy.py  — strategy CORE (sector timing, stock factors, universe, positions, exits)
  • csm_sector_rotation_backtest.py  — backtest engine, metrics, reporting, trade log
  • run_csm_sector_rotation.py (this file) — orchestration only
"""

import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from csm_sector_rotation_strategy import load_data, load_sector_map, CSMSectorRotation
from csm_sector_rotation_backtest import (
    backtest_event_driven,
    get_trade_log,
    print_report,
    print_exit_breakdown,
)


def main(load_start=None, load_end=None, start_report=None, universe=None,
         top_n=None, sector_top_k=None):
    # ── 1. Load Data ─────────────────────────────────────────────────────────
    data_folder   = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
    sector_csv    = "/Users/hemantsoni/Documents/final_momentum_strategies/New_momentum_strategy/instruments_clean.csv"

    print("Loading data...")
    prices, volumes, highs, lows, opens = load_data(data_folder)
    sector_map = load_sector_map(sector_csv)

    if prices.empty:
        print("Error: No data loaded.")
        return

    start_load   = '2001-01-01'   # extra year for SMA200 + sector-momentum warmup
    end_load     = '2025-12-31'
    report_start = '2003-01-01'

    if load_start and load_end and start_report:
        start_load, end_load, report_start = load_start, load_end, start_report

    prices  = prices.loc[start_load:end_load]
    volumes = volumes.loc[start_load:end_load]
    if not highs.empty: highs = highs.loc[start_load:end_load]
    if not lows.empty:  lows  = lows.loc[start_load:end_load]
    if not opens.empty: opens = opens.loc[start_load:end_load]

    print(f"Prices shape : {prices.shape}")
    print(f"Date range   : {prices.index.min().date()}  ->  {prices.index.max().date()}")

    # ── 2. Benchmark ─────────────────────────────────────────────────────────
    print("Building equal-weight benchmark...")
    benchmark_series = (1 + prices.pct_change(fill_method=None)
                                .clip(-0.5, 0.5)
                                .mean(axis=1, skipna=True)
                                .fillna(0.0)).cumprod()

    # ── 3. Instantiate Strategy ───────────────────────────────────────────────
    csm = CSMSectorRotation(
        prices_df            = prices,
        volumes_df           = volumes,
        highs_df              = highs,
        lows_df                = lows,
        opens_df                = opens,
        benchmark_series         = benchmark_series,
        sector_map               = sector_map,
        # Sector-timing layer
        sector_lookback_months       = 12,
        sector_lookback_short_months = 6,
        sector_lag_months            = 1,
        sector_top_k                 = (sector_top_k or 4),
        # Stock-level factor (identical to csm_batch)
        lookback_months      = 12,
        lag_months            = 1,
        # Universe
        top_n                = (top_n or 30),
        min_price            = 20.0,
        universe_top_n       = (universe or 1000),
        max_circuit_days     = 5,
        buffer_ratio         = 0.20,
        # Stops
        atr_period           = 14,
        atr_multiplier       = 3.0,
        atr_multiplier_high_vol = 2.0,
        hard_stop_from_entry = 0.15,
        hard_stop_from_peak  = 0.20,
        stop_slippage_pct    = 0.003,
        use_trailing_stop    = False,
        stop_cooldown_days   = 20,
        min_hold_days        = 5,
        # Risk overlays
        use_crash_guard      = True,
        crash_guard_cooldown = 10,
        corr_guard_threshold = 0.8,
        vol_target           = 0.13,
        # Position sizing
        max_weight_per_stock = 0.05,
        rebalance_months     = 1,
        # Exit: dynamic rank-decay
        rank_exit_dynamic    = True,
        rank_exit_drop_frac  = 0.33,
        rank_exit_floor_frac = 0.67,
    )

    # ── 4. Calculate Factors & Positions ─────────────────────────────────────
    csm.calculate_factors()
    csm.get_positions()

    # ── 5. Backtest (event-driven) ────────────────────────────────────────────
    backtest_event_driven(
        csm,
        initial_capital  = 100_000,
        transaction_cost = 0.003,
        risk_free_rate   = 0.0,
    )

    # ── 6. Trade log ───────────────────────────────────────────────────────
    report_start_dt = pd.Timestamp(report_start)
    detailed_log = pd.DataFrame()
    try:
        _full_log = get_trade_log(csm)
        if not _full_log.empty:
            detailed_log = _full_log[_full_log['Entry_Date'] >= report_start_dt].copy()
            out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'csm_sector_rotation_trade_log.csv')
            detailed_log.to_csv(out_path, index=False)
            print(f"\n[Logs] {out_path}  ({len(detailed_log)} trades from {report_start_dt.date()})")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 220)
            print("\nSample Trades (first 5):")
            print(detailed_log.head(5).to_string(index=False))
    except Exception as e:
        print(f"\n[Logs] Warning: Trade log failed: {e}")

    # ── 7. Performance Report ─────────────────────────────────────────────
    print_report(csm)
    print_exit_breakdown(detailed_log)

    r = csm.results
    return {
        'cagr'          : r['cagr'] * 100,
        'sharpe'        : r['sharpe'],
        'calmar'        : r['calmar'],
        'max_drawdown'  : r['max_drawdown'] * 100,
        'avg_hold_days' : detailed_log['Holding_Days'].mean() if not detailed_log.empty else float('nan'),
    }


if __name__ == "__main__":
    main()
