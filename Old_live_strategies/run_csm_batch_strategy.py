"""
run_csm_batch_strategy.py
=========================
Runner for the CSM Batch Strategy (CrossSectionalMomentum).

Thin orchestrator (mirrors run_csm_stock_backtest.py): loads data, builds the
benchmark, instantiates the strategy CORE (csm_batch_strategy), runs the
event-driven backtest engine (csm_batch_backtest), slices results to the
reporting window, and prints the performance report.

Split layout:
  • csm_batch_strategy.py  — strategy CORE (factors, universe, positions, exits)
  • csm_batch_backtest.py  — backtest engine, metrics, reporting, IC, plots
  • run_csm_batch_strategy.py (this file) — orchestration only

NEW metrics vs the original report:
  • Avg / Mean Drawdown (time-average underwater depth)
  • Yearly table pairing each year's return with that year's worst drawdown
"""

import pandas as pd

from csm_batch_strategy import load_data, CrossSectionalMomentum
from csm_batch_backtest1 import (
    backtest_event_driven,
    slice_results,
    get_trade_log,
    populate_trade_stats,
    print_report,
    print_exit_breakdown,
    print_yearly_performance,
    plot_performance,
    calculate_ic,
    plot_ic,
    calculate_realized_ic,
)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main(load_start=None, load_end=None, start_report=None, mode=None, universe=None):
    # ── 1. Load Data ─────────────────────────────────────────────────────────
    data_folder = '/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data'
    print("Loading data...")
    prices, volumes, highs, lows, opens = load_data(data_folder)

    if prices.empty:
        print("Error: No data loaded.")
        return

    start_load   = '2012-01-01'   # Extra year for SMA200 warmup
    end_load     = '2025-12-31'
    report_start = '2013-01-01'   # Report period (after warmup)

    if load_start and load_end and start_report:
        start_load = load_start
        end_load = load_end
        report_start = start_report

    prices  = prices.loc[start_load:end_load]
    volumes = volumes.loc[start_load:end_load]
    if not highs.empty: highs = highs.loc[start_load:end_load]
    if not lows.empty:   lows   = lows.loc[start_load:end_load]
    if not opens.empty:  opens  = opens.loc[start_load:end_load]

    print(f"Prices shape : {prices.shape}")
    print(f"Date range   : {prices.index.min().date()}  →  {prices.index.max().date()}")

    # ── 2. Benchmark ─────────────────────────────────────────────────────────
    # Use equal-weight average of DAILY RETURNS then cumulate — much better than
    # a price average which is biased toward highest-priced stocks.
    print("Building equal-weight benchmark...")
    benchmark_series = (1 + prices.pct_change(fill_method=None)
                                .clip(-0.5, 0.5)
                                .mean(axis=1, skipna=True)
                                .fillna(0.0)).cumprod()

    # ── 3. Instantiate Strategy ───────────────────────────────────────────────
    csm = CrossSectionalMomentum(
        prices_df            = prices,
        volumes_df           = volumes,
        highs_df             = highs,
        lows_df              = lows,
        opens_df             = opens,
        benchmark_series     = benchmark_series,
        # Factor
        lookback_months      = 12,
        lag_months           = 1,
        # Universe
        top_n                = 30,
        min_price            = 20.0,
        universe_top_n       = (universe or 1000),    # dynamic liquidity top-N
        max_circuit_days     = 5,       # circuit-breaker filter
        buffer_ratio         = 0.20,    # hysteresis: entry≤top_n, exit≤top_n×1.2
        # Stops
        atr_period           = 14,
        atr_multiplier       = 3.0,
        atr_multiplier_high_vol = 2.0,  # tighter chandelier when benchmark vol is elevated
        hard_stop_from_entry = 0.15,    # entry hard stop: −15% from entry
        hard_stop_from_peak  = 0.20,    # peak hard stop (trailing only): −20% from peak
        stop_slippage_pct    = 0.003,
        use_trailing_stop    = False,   # KEPT switch: True adds the ATR chandelier + peak-hard trail
        stop_cooldown_days   = 20,      # block re-entry N days after a stop on the same ticker
        min_hold_days        = 0,       # stop cannot fire in first N days of a trade
        # Risk overlays
        use_crash_guard      = True,    # → 100% cash during extreme benchmark vol (no leverage)
        crash_guard_cooldown = 10,      # trading days to wait after panic clears
        corr_guard_threshold = 0.8,     # portfolio/avg-stock vol ratio → scale book to 50%
        vol_target           = 0.13,    # de-lever when realised vol > target (Calmar lever)
        # Position sizing
        max_weight_per_stock = 0.05,    # max 5% per stock
        rebalance_months     = 3,       # quarterly rebalance
        # Exit: DYNAMIC rank-decay — anti-overfit (thresholds are FRACTIONS of top_n)
        rank_exit_dynamic    = True,    # cut a held name whose rank decays past a top_n-relative band
        rank_exit_drop_frac  = 0.33,    # ≈ drop≥10 ranks at top_n=30, but scale-free
        rank_exit_floor_frac = 0.67,    # ≈ rank>20 at top_n=30
    )

    # ── 4. Calculate Factors & Positions ─────────────────────────────────────
    csm.calculate_factors()
    csm.get_positions()

    # ── 5. Backtest (event-driven) ────────────────────────────────────────────
    results = backtest_event_driven(
        csm,
        initial_capital  = 100_000,
        transaction_cost = 0.003,   # 0.3% one-way: realistic for Indian direct-market access
        risk_free_rate   = 0.0,     # idle cash earns RFR (CSM runs ~60-70% invested)
    )

    # ── 6. Slice to reporting period ──────────────────────────────────────────
    print(f"\nSlicing results to {report_start}...")
    results = slice_results(results, report_start, risk_free_rate=0.0)

    # ── 7. Trade log from position_metadata (v3-style) ──────────────────────
    report_start_dt = pd.Timestamp(report_start)
    detailed_log = pd.DataFrame()
    try:
        _full_log = get_trade_log(csm)
        if not _full_log.empty:
            detailed_log = _full_log[
                _full_log['Entry_Date'] >= report_start_dt
            ].copy()
            detailed_log.to_csv('csm_batch_detailed_trade_log.csv', index=False)
            print(f"\n[Logs] csm_batch_detailed_trade_log.csv  "
                  f"({len(detailed_log)} trades from {report_start_dt.date()})")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 220)
            print("\nSample Trades (first 5):")
            print(detailed_log.head(5).to_string(index=False))
    except Exception as e:
        print(f"\n[Logs] Warning: Trade log failed: {e}")

    # ── Populate trade-basis metrics from the filtered log ───────────────────
    populate_trade_stats(results, detailed_log)

    # ── 8. Performance Report (incl. Avg/Mean DD) ─────────────────────────────
    print_report(results)

    # ── 8b. Granular exit breakdown (TRAILING/REBALANCE/CRASH_GUARD × WIN/LOSS)
    print_exit_breakdown(detailed_log)

    # ── 9. Yearly Returns + Yearly Drawdown (NEW) ─────────────────────────────
    print_yearly_performance(results['portfolio_value'])

    # ── 10. Visualisation ─────────────────────────────────────────────────────
    bench_slice = benchmark_series.reindex(results['equity_curve'].index).ffill()
    plot_performance(results, bench_slice)

    # ── 11. IC / ICIR Analysis ────────────────────────────────────────────────
    # (A) Filtered-universe IC: does the factor rank universe-eligible stocks?
    #     For a pure top-N strategy this is the primary IC measure.
    ic_results = calculate_ic(
        csm,
        forward_periods = 1,
        method          = 'spearman',
        report_start    = report_start,
        per_component   = True,
    )
    plot_ic(csm, ic_results, filename='factor_ic_batch.png')

    # (B) Realized IC: within the held portfolio, did higher factor score
    #     correctly predict better trade outcome?
    calculate_realized_ic(csm, method='spearman', report_start=report_start)

    return {
        'cagr':results['cagr']*100,
        'drawdown':results['max_drawdown']*100,
        'avg_drawdown':results['avg_drawdown']*100,
        'trade win rate':results['trade_win_rate']*100,
        'calmar':results['calmar'],
    }


if __name__ == "__main__":
    main()