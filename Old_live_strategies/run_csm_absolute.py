"""
run_csm_absolute.py — thin runner for the CSM Individual Momentum strategy.

Orchestration only: loads data, cleans the index, slices the load window,
builds a synthetic equal-weight benchmark, instantiates the strategy with the
production parameters, runs the event-driven backtest, then computes metrics,
prints the report, generates trade logs, plots, and IC analysis.

All strategy logic lives in csm_v2.py; all backtest/metrics/report/plot/IC
logic lives in csm_v2_backtest.py. This file calls those module-level functions
(passing the strategy object), not class methods.
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csm_absolute import load_data, IndividualMomentumStrategy
from csm_absolute import monitor_entry_signals, save_entry_signals
from csm_absolute_backtest import (
    backtest_event_driven,
    live_backtest,
    compute_metrics,
    compute_benchmark_metrics,
    print_report,
    print_exit_breakdown,
    get_trade_log,
    generate_detailed_trade_log,
    detect_strategy_breaks,
    print_yearly_returns,
    plot_summary,
    plot_diagnostics,
    calculate_ic,
    plot_ic,
    calculate_realized_ic,
)

# ── Config ──────────────────────────────────────────────────────────────────
# DATA_FOLDER = "/Users/hemantsoni/Documents/output_stocks"
DATA_FOLDER = '/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data'

# Date windows (overridable via main() args)
START_LOAD   = '2019-01-01'   # extra year for SMA200 warmup
END_LOAD     = '2025-12-31'
REPORT_START = '2020-01-01'

# Backtest variant: "event_driven" (corr guard in-loop) | "live" (+ LTP gap filter)
BACKTEST_MODE = "event_driven"

# Strategy parameters (production)
LOOKBACK_MONTHS       = 9
LOOKBACK_SHORT_MONTHS = 4
ATR_PERIOD            = 13
ATR_MULTIPLIER        = 2.0
LAG_MONTHS            = 1
SHARPE_THRESHOLD      = 0.6
CAPACITY_LIMIT        = 25
UNIVERSE_TOP_N        = 1000
LEVERAGE_BULL         = 1.0
LEVERAGE_BEAR         = 0.8
LEVERAGE_PANIC        = 0.5
MIN_PRICE             = 20.0
MAX_CIRCUIT_DAYS      = 8
MAX_WEIGHT_PER_STOCK  = 0.12
STOP_STD_DEVS         = 3.0

# ── A/B toggles (defaults reproduce production behavior) ───────────────────
USE_REBALANCE         = True 
REBALANCE_MONTH       = 3
USE_TRAILING          = True
REENTRY_COOLDOWN_DAYS = 7
RANK_BUFFER           = 1.5 
COOLDOWN_LOSERS_ONLY  = True   
USE_TAKE_PROFIT       = True   
# Backtest engine config
BT_KWARGS = dict(
    initial_capital=100_000,
    transaction_cost=0.003,
    risk_free_rate=0.00,

    # ── Exit stops (tightened — exit-engine sweep) ──────────────────
    hard_stop_from_entry_pct = 0.08,
    hard_stop_from_peak_pct  = 0.12,
    # ── Limit Order Config ──────────────────────────────────────────
    use_limit_orders      = True,
    stop_approach_pct     = 0.02,   
    trail_approach_pct    = 0.03,   
    order_ttl_days        = 4,      
    order_fill_assumption = 'limit_price', 

    # ── Liquid MF Parking (idle cash) ───────────────────────────────
    use_liquid_mf         = True, 
    liquid_mf_annual_rate = 0.0,
)


def main(load_start=None, load_end=None, start_report=None, mode=None, universe=None):
    # 1. Load Data
    print("Loading data...")
    prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)

    if prices.empty:
        print("Error: No data loaded.")
        return

    start_load   = START_LOAD
    end_load     = END_LOAD
    report_start = REPORT_START

    if load_start and load_end and start_report:
        start_load = load_start
        end_load = load_end
        report_start = start_report

    # --- Ensure Data Monotonicity (Fix for KeyError) ---
    # 1. Drop NaT (Crucial for monotonic indexing)
    if prices.index.isna().any():
        prices = prices[prices.index.notna()]

    if volumes.index.isna().any():
        volumes = volumes[volumes.index.notna()]

    if highs.index.isna().any(): highs = highs[highs.index.notna()]
    if lows.index.isna().any(): lows = lows[lows.index.notna()]
    if opens.index.isna().any(): opens = opens[opens.index.notna()]

    # 2. Sort Index
    if not prices.index.is_monotonic_increasing:
        prices = prices.sort_index()

    if not volumes.index.is_monotonic_increasing:
        volumes = volumes.sort_index()

    if not highs.index.is_monotonic_increasing: highs = highs.sort_index()
    if not lows.index.is_monotonic_increasing: lows = lows.sort_index()
    if not opens.index.is_monotonic_increasing: opens = opens.sort_index()

    # 3. Remove Duplicates
    if prices.index.duplicated().any():
        prices = prices[~prices.index.duplicated(keep='last')]

    if volumes.index.duplicated().any():
        volumes = volumes[~volumes.index.duplicated(keep='last')]

    if highs.index.duplicated().any(): highs = highs[~highs.index.duplicated(keep='last')]
    if lows.index.duplicated().any(): lows = lows[~lows.index.duplicated(keep='last')]
    if opens.index.duplicated().any(): opens = opens[~opens.index.duplicated(keep='last')]

    # 4. Final Re-Sort (Safety)
    prices = prices.sort_index()
    volumes = volumes.sort_index()
    highs = highs.sort_index()
    lows = lows.sort_index()
    opens = opens.sort_index()

    prices = prices.loc[start_load:end_load]
    volumes = volumes.loc[start_load:end_load]
    highs = highs.loc[start_load:end_load]
    lows = lows.loc[start_load:end_load]
    opens = opens.loc[start_load:end_load]

    print(f"Prices shape (Filtered): {prices.shape}")
    print(f"Date Range: {prices.index.min()} to {prices.index.max()}")

    # 2. Synthetic Benchmark
    print("Creating Synthetic Benchmark (Universe Equal Weight)...")
    benchmark_price = (1 + prices.pct_change().clip(-.5,.5).mean(axis=1)).cumprod()
    print("Benchmark :- ", benchmark_price)

    # 3. Instantiate Individual Momentum Strategy
    print("Running Production Individual Momentum (Absolute Signal)...")
    csm = IndividualMomentumStrategy(
        prices,
        volumes,
        highs_df             = highs,
        lows_df              = lows,
        opens_df             = opens,
        benchmark_series     = benchmark_price,
        lookback_months      = LOOKBACK_MONTHS,
        lookback_short_months= LOOKBACK_SHORT_MONTHS,
        atr_period           = ATR_PERIOD,
        atr_multiplier       = ATR_MULTIPLIER,
        lag_months           = LAG_MONTHS,
        sharpe_threshold     = SHARPE_THRESHOLD,
        capacity_limit       = CAPACITY_LIMIT,
        universe_top_n       = (universe or UNIVERSE_TOP_N),
        leverage_bull        = LEVERAGE_BULL,
        leverage_bear        = LEVERAGE_BEAR,
        leverage_panic       = LEVERAGE_PANIC,
        min_price            = MIN_PRICE,
        max_circuit_days     = MAX_CIRCUIT_DAYS,
        max_weight_per_stock = MAX_WEIGHT_PER_STOCK,
        stop_std_devs        = STOP_STD_DEVS,
        use_rebalance        = USE_REBALANCE,
        rebalance_months     = REBALANCE_MONTH,
        use_trailing         = USE_TRAILING,
        reentry_cooldown_days= REENTRY_COOLDOWN_DAYS,
        rank_buffer          = RANK_BUFFER,
        cooldown_losers_only = COOLDOWN_LOSERS_ONLY,
        use_take_profit      = USE_TAKE_PROFIT,
    )

    # 4. Calculate Factors & Positions
    csm.calculate_factors()
    positions = csm.get_positions()

    # 5. Event-Driven Backtest
    bt_mode = mode if mode else BACKTEST_MODE
    if bt_mode == "live":
        results = live_backtest(csm, **BT_KWARGS, max_entry_gap_pct=0.02)
    else:
        results = backtest_event_driven(csm, **BT_KWARGS)

    # --- Slice Results for Reporting ---
    print(f"\nSlicing Results to Start strictly on {report_start}...")
    # Sharpe (and TC drag) must be recomputed against the SAME risk-free / cost rates
    # the backtest was actually run with (BT_KWARGS), not a hardcoded assumption.
    results = compute_metrics(results, report_start, risk_free_rate=BT_KWARGS['risk_free_rate'])

    # Benchmark-relative metrics (beta + annualized alpha vs the synthetic EW index)
    results = compute_benchmark_metrics(results, benchmark_price)

    # 6. Trade Logs
    # 6a. Legacy weight-change log (kept for reference)
    trade_log = get_trade_log(csm)
    if not trade_log.empty:
        trade_log = trade_log[trade_log['Date'] >= report_start]
        trade_log.to_csv('csm_trade_log.csv', index=False)
        print(f"\n[Logs] Saved Weight-Change Log to 'csm_trade_log.csv' ({len(trade_log)} rows)")

    # 6b. Detailed per-trade log (entry/exit pairs with P&L, quantity, reason)
    detailed_log = pd.DataFrame()
    report_start_dt = pd.Timestamp(report_start)
    try:
        _full_log = generate_detailed_trade_log(
            csm,
            initial_capital=100_000,
            equity_curve=results['equity_curve'],
        )
        total_before_filter = len(_full_log)
        if not _full_log.empty:
            detailed_log = _full_log[_full_log['Entry_Date'] >= report_start_dt].copy()
            detailed_log.to_csv('csm_detailed_trade_log.csv', index=False)
            print(f"\n[Logs] Saved Detailed Trade Log to 'csm_detailed_trade_log.csv'")
            print(f"       Total trades (all time): {total_before_filter} | "
                  f"After date filter (>= {report_start_dt.date()}): {len(detailed_log)}")
            print("\nSample Trades (first 10):")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 200)
            print(detailed_log.head(10).to_string(index=False))
    except Exception as e:
        print(f"\n[Logs] Warning: Could not generate detailed trade log: {e}")

    # Populate trade-basis metrics in results from the filtered detailed_log
    if not detailed_log.empty:
        dl = detailed_log
        wins        = (dl['PnL_Pct'] > 0).sum()
        losses      = (dl['PnL_Pct'] < 0).sum()
        total_t     = len(dl)

        results['trade_win_rate']     = wins / total_t if total_t > 0 else 0
        results['total_trades_count'] = total_t
        results['avg_trade_return']   = dl['PnL_Pct'].mean()
        results['avg_holding_days']   = dl['Holding_Days'].mean()
        results['best_trade']         = dl['PnL_Pct'].max()
        results['worst_trade']        = dl['PnL_Pct'].min()

        # Payoff Ratio: average winning trade % / average losing trade %
        avg_win_pct  = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].mean()  if wins   > 0 else 0.0
        avg_loss_pct = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().mean() if losses > 0 else 0.0
        results['payoff_ratio']   = avg_win_pct / avg_loss_pct if avg_loss_pct > 0 else float('inf')
        results['avg_win_pct']    = avg_win_pct
        results['avg_loss_pct']   = avg_loss_pct

        # Profit Factor — two variants:
        #   (a) PnL_Pct — equal-weighted (% returns)
        #   (b) PnL_Abs — dollar-weighted (compounded capital)
        gross_wins_pct   = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].sum()
        gross_losses_pct = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().sum()
        results['profit_factor']     = gross_wins_pct / gross_losses_pct if gross_losses_pct > 0 else float('inf')

        gross_wins_abs   = dl.loc[dl['PnL_Abs'] > 0, 'PnL_Abs'].sum()
        gross_losses_abs = dl.loc[dl['PnL_Abs'] < 0, 'PnL_Abs'].abs().sum()
        results['profit_factor_dollar'] = gross_wins_abs / gross_losses_abs if gross_losses_abs > 0 else float('inf')

    # 7. Report
    print_report(results)

    # 7a. Exit breakdown (by reason and outcome)
    print_exit_breakdown(detailed_log)

    # 7b. Break Detection
    detect_strategy_breaks(
        results['executed_weights'],
        results['portfolio_value'],
        min_break_days=14,
        use_liquid_mf=results.get('use_liquid_mf', False),
        liquid_mf_annual_rate=results.get('liquid_mf_annual_rate', 0.0),
    )

    # 8. Visualization
    print_yearly_returns(results['portfolio_value'])

    # 9. Generate Plots (DISABLED — keep the folder clean; re-enable to get PNGs back)
    # bench_slice = benchmark_price.loc[results['equity_curve'].index]
    # plot_summary(csm, benchmark_series=bench_slice)
    # plot_diagnostics(csm)

    # 10. IC / ICIR Analysis
    # (A) Filtered-universe IC  (printed analysis kept; PNG disabled)
    ic_results = calculate_ic(csm, forward_periods=1, method='spearman',
                              report_start=report_start)
    # plot_ic(csm, ic_results, filename='factor_ic.png')  # DISABLED — no factor_ic.png

    # (B) Realized IC (uses detailed trade log)
    if not detailed_log.empty:
        calculate_realized_ic(
            csm,
            trade_log_df = detailed_log,
            method       = 'spearman',
            report_start = report_start,
        )

    return {
        'cagr':results['cagr']*100,
        'drawdown':results['max_drawdown']*100,
        'trade win rate':results['trade_win_rate']*100,
        'calmar':results['calmar'],
        }


def monitor_stocks_signal():
    prices, volumes, highs, lows, opens = load_data("output_stocks")

    my_stocks = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'TVSMOTOR', 'RECLTD', 'BANKBARODA', 'ZOTA', 'VMART']

    benchmark = prices.mean(axis=1)

    signals = monitor_entry_signals(
        stock_list=my_stocks,
        prices_df=prices,
        volumes_df=volumes,
        benchmark_series=benchmark,
        lookback_months=9,
        lag_months=1,
        sharpe_threshold=0.5
    )

    save_entry_signals(signals, 'my_entry_signals.csv')

    enter_now = signals[signals['Signal'] == 'ENTER NOW']
    print(f"\nStocks to buy: {enter_now['Ticker'].tolist()}")


if __name__ == "__main__":
    main()
    # monitor_stocks_signal()