"""
run_csm_absolute_gold_silver.py
================================
Second attempt at the gold/silver question. run_csm_batch_strategy_gold_silver.py
(CrossSectionalMomentum / csm_batch_*) showed that forcing GOLDBEES/SILVERBEES to
compete in a top_n=30 RANK contest against ~480 equity candidates each month wastes
their diversification value: they almost never out-rank India's best momentum
small/midcaps on raw dual-Sharpe score (SILVERBEES: 0 trades across ~4y of
eligibility; GOLDBEES: 4 trades across 13y). That's the wrong mechanism for an
asset whose value proposition is LOW CORRELATION, not "highest momentum score in
the market."

This uses IndividualMomentumStrategy (csm_absolute.py) instead, whose selection
mechanism is structurally different:

  csm_batch (CrossSectionalMomentum)        csm_absolute (IndividualMomentumStrategy)
  ─────────────────────────────────         ──────────────────────────────────────────
  Forced top_n=30: ALWAYS fills 30          Absolute gate: dual-Sharpe > 0.6 AND
  slots from whoever ranks highest —        positive 9m return. A name enters on ITS
  a name only gets in by beating            OWN momentum quality — no forced contest
  ~470 other candidates for a spot.         unless > capacity_limit (25) candidates
                                             clear the gate on the SAME day.

Because the gate is absolute rather than a forced rank contest, GOLDBEES/SILVERBEES
get an independent shot at entering whenever THEIR OWN trend clears the bar — including
periods when equity momentum is scarce (few names clearing 0.6 Sharpe), which is
exactly the low-correlation/diversification scenario the pitch is about. Whether
that actually shows up in the numbers, rather than just in theory, is what this
script tests.

Important caveat this construction does NOT fix: leverage_bear/leverage_panic
throttle the WHOLE portfolio — gold/silver included — off the EQUITY benchmark's
SMA200 regime. So during an equity bear market, any held gold/silver position also
gets scaled down, even though that is precisely when a low/negatively-correlated
hedge is most valuable. Merging into one universe and reusing the engine unchanged
does not decouple gold/silver's sizing from the equity regime signal — see the
report at the bottom of this run for whether that materially matters here.

No changes to csm_absolute.py / csm_absolute_backtest.py / run_csm_absolute.py.
Same "merge into universe" data-plumbing as the batch experiment: load
GOLDBEES/SILVERBEES, concat onto the equity panels, run the SAME engine with the
SAME production parameters run_csm_absolute.py uses. Runs an equity-only baseline
and an equity+ETF treatment back to back with identical params/date range, then
prints an A/B diff plus gold/silver-specific attribution (selection frequency,
trades, P&L share, correlation to the equity benchmark).

Data sources
------------
Equity : /Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data
         (same path run_csm_absolute.py already uses — no stale-path issue here,
         unlike run_csm_batch_strategy.py's hardcoded output_stocks/.)
ETF    : /Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data
         Default tickers: GOLDBEES, SILVERBEES.

Outputs are suffixed per-variant so they never collide with run_csm_absolute.py's
own csm_trade_log.csv / csm_detailed_trade_log.csv.
"""

import os

import numpy as np
import pandas as pd

from csm_absolute import load_data, IndividualMomentumStrategy
from csm_absolute_backtest import (
    backtest_event_driven,
    compute_metrics,
    compute_benchmark_metrics,
    print_report,
    print_exit_breakdown,
    get_trade_log,
    generate_detailed_trade_log,
    detect_strategy_breaks,
    print_yearly_returns,
    calculate_ic,
    calculate_realized_ic,
)

EQUITY_DATA_FOLDER  = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
ETF_DATA_FOLDER     = "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data"
DEFAULT_ETF_TICKERS = ["GOLDBEES", "SILVERBEES"]

# Date windows — identical to run_csm_absolute.py's production defaults.
START_LOAD   = '2019-01-01'   # extra year for SMA200 warmup
END_LOAD     = '2025-12-31'
REPORT_START = '2020-01-01'

# Strategy parameters — identical to run_csm_absolute.py's production config,
# used UNCHANGED for both variants so the A/B diff isolates the ETFs' effect.
STRATEGY_KWARGS = dict(
    lookback_months       = 9,
    lookback_short_months = 4,
    atr_period             = 13,
    atr_multiplier         = 2.0,
    lag_months             = 1,
    sharpe_threshold       = 0.6,
    capacity_limit         = 25,
    universe_top_n         = 1000,
    leverage_bull          = 1.0,
    leverage_bear          = 0.8,
    leverage_panic         = 0.5,
    min_price              = 20.0,
    max_circuit_days       = 8,
    max_weight_per_stock   = 0.12,
    stop_std_devs          = 3.0,
    use_rebalance          = True,
    rebalance_months       = 3,
    use_trailing           = True,
    reentry_cooldown_days  = 7,
    rank_buffer            = 1.5,
    cooldown_losers_only   = True,
    use_take_profit        = True,
)
BT_KWARGS = dict(
    initial_capital           = 100_000,
    transaction_cost          = 0.003,
    risk_free_rate             = 0.00,
    hard_stop_from_entry_pct  = 0.08,
    hard_stop_from_peak_pct   = 0.12,
    use_limit_orders          = True,
    stop_approach_pct         = 0.02,
    trail_approach_pct        = 0.03,
    order_ttl_days            = 4,
    order_fill_assumption     = 'limit_price',
    use_liquid_mf             = True,
    liquid_mf_annual_rate     = 0.0,
)


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING / MERGING
# ══════════════════════════════════════════════════════════════════════════════

def load_etf_data(folder_path, tickers):
    """Load specific ETF CSVs and return them in the same 5-DataFrame shape as
    csm_absolute.load_data(), so they can be pd.concat'ed straight onto the
    equity panels. The ETF files differ from the equity ones only in the index
    column name ('timestamp' vs 'datetime') and in carrying an explicit +05:30
    offset on every row (always midnight IST — the trading day, same as the
    equity files' bare dates)."""
    price_list, volume_list, high_list, low_list, open_list = [], [], [], [], []

    for ticker in tickers:
        path = os.path.join(folder_path, f"{ticker}.csv")
        if not os.path.exists(path):
            print(f"Warning: ETF file not found, skipping: {path}")
            continue
        df = pd.read_csv(path, parse_dates=['timestamp'], index_col='timestamp')
        df.index = df.index.tz_localize(None)
        df = df[~df.index.duplicated(keep='last')]

        price_list.append(df['close'].rename(ticker))
        volume_list.append(df['volume'].rename(ticker))
        high_list.append(df['high'].rename(ticker))
        low_list.append(df['low'].rename(ticker))
        open_list.append(df['open'].rename(ticker))

    def _build(lst):
        if not lst:
            return pd.DataFrame()
        return pd.concat(lst, axis=1).sort_index()

    prices, volumes, highs, lows, opens = (
        _build(price_list), _build(volume_list),
        _build(high_list), _build(low_list), _build(open_list),
    )
    print(f"Loaded {len(price_list)}/{len(tickers)} ETF(s) from {folder_path}: "
          f"{list(prices.columns)}")
    return prices, volumes, highs, lows, opens


def merge_panels(equity_panels, etf_panels):
    """Concat ETF OHLCV panels onto the equity ones, column-wise, aligning on
    the union of trading dates (NaN where one side has no data — identical to
    how load_data() already handles staggered listing dates within equities)."""
    merged = []
    for eq_df, etf_df in zip(equity_panels, etf_panels):
        if etf_df.empty:
            merged.append(eq_df)
        elif eq_df.empty:
            merged.append(etf_df)
        else:
            merged.append(pd.concat([eq_df, etf_df], axis=1).sort_index())
    return tuple(merged)


def _clean_index(df):
    """Mirrors run_csm_absolute.py's defensive index cleaning (dropna/sort/dedupe)."""
    if df.empty:
        return df
    if df.index.isna().any():
        df = df[df.index.notna()]
    if not df.index.is_monotonic_increasing:
        df = df.sort_index()
    if df.index.duplicated().any():
        df = df[~df.index.duplicated(keep='last')]
    return df


# ══════════════════════════════════════════════════════════════════════════════
# ONE VARIANT: instantiate → factors → positions → backtest → report
# ══════════════════════════════════════════════════════════════════════════════

def run_variant(name, prices, volumes, highs, lows, opens, benchmark_price, report_start):
    print("\n" + "#" * 70)
    print(f"#  VARIANT: {name}   (universe: {prices.shape[1]} tickers)")
    print("#" * 70)

    csm = IndividualMomentumStrategy(
        prices, volumes,
        highs_df         = highs,
        lows_df          = lows,
        opens_df         = opens,
        benchmark_series = benchmark_price,
        **STRATEGY_KWARGS,
    )
    csm.calculate_factors()
    csm.get_positions()

    results = backtest_event_driven(csm, **BT_KWARGS)

    print(f"\nSlicing Results to Start strictly on {report_start}...")
    results = compute_metrics(results, report_start, risk_free_rate=BT_KWARGS['risk_free_rate'])
    results = compute_benchmark_metrics(results, benchmark_price)

    # Legacy weight-change log (kept for reference, mirrors run_csm_absolute.py)
    trade_log = get_trade_log(csm)
    if not trade_log.empty:
        trade_log = trade_log[trade_log['Date'] >= report_start]
        trade_log.to_csv(f'csm_absolute_{name}_trade_log.csv', index=False)

    # Detailed per-trade log (entry/exit pairs with P&L)
    report_start_dt = pd.Timestamp(report_start)
    detailed_log = pd.DataFrame()
    try:
        full_log = generate_detailed_trade_log(
            csm, initial_capital=100_000, equity_curve=results['equity_curve'],
        )
        if not full_log.empty:
            detailed_log = full_log[full_log['Entry_Date'] >= report_start_dt].copy()
            log_path = f'csm_absolute_{name}_detailed_trade_log.csv'
            detailed_log.to_csv(log_path, index=False)
            print(f"\n[Logs] {log_path}  ({len(detailed_log)} trades from {report_start_dt.date()})")
    except Exception as e:
        print(f"\n[Logs] Warning: Could not generate detailed trade log: {e}")

    # Populate trade-basis metrics — identical block to run_csm_absolute.py's main()
    if not detailed_log.empty:
        dl = detailed_log
        wins    = (dl['PnL_Pct'] > 0).sum()
        losses  = (dl['PnL_Pct'] < 0).sum()
        total_t = len(dl)

        results['trade_win_rate']     = wins / total_t if total_t > 0 else 0
        results['total_trades_count'] = total_t
        results['avg_trade_return']   = dl['PnL_Pct'].mean()
        results['avg_holding_days']   = dl['Holding_Days'].mean()
        results['best_trade']         = dl['PnL_Pct'].max()
        results['worst_trade']        = dl['PnL_Pct'].min()

        avg_win_pct  = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].mean()       if wins   > 0 else 0.0
        avg_loss_pct = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().mean() if losses > 0 else 0.0
        results['payoff_ratio'] = avg_win_pct / avg_loss_pct if avg_loss_pct > 0 else float('inf')
        results['avg_win_pct']  = avg_win_pct
        results['avg_loss_pct'] = avg_loss_pct

        gross_wins_pct   = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].sum()
        gross_losses_pct = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().sum()
        results['profit_factor'] = gross_wins_pct / gross_losses_pct if gross_losses_pct > 0 else float('inf')

        gross_wins_abs   = dl.loc[dl['PnL_Abs'] > 0, 'PnL_Abs'].sum()
        gross_losses_abs = dl.loc[dl['PnL_Abs'] < 0, 'PnL_Abs'].abs().sum()
        results['profit_factor_dollar'] = gross_wins_abs / gross_losses_abs if gross_losses_abs > 0 else float('inf')

    print_report(results)
    print_exit_breakdown(detailed_log)
    detect_strategy_breaks(
        results['executed_weights'],
        results['portfolio_value'],
        min_break_days=14,
        use_liquid_mf=results.get('use_liquid_mf', False),
        liquid_mf_annual_rate=results.get('liquid_mf_annual_rate', 0.0),
    )
    print_yearly_returns(results['portfolio_value'])

    # Plots intentionally skipped — mirrors run_csm_absolute.py (disabled by default).

    ic_results = calculate_ic(csm, forward_periods=1, method='spearman', report_start=report_start)
    if not detailed_log.empty:
        calculate_realized_ic(csm, trade_log_df=detailed_log, method='spearman', report_start=report_start)

    metrics = {
        'cagr':             results['cagr'] * 100,
        'sharpe':           results['sharpe'],
        'sortino':          results['sortino'],
        'calmar':           results['calmar'],
        'max_drawdown':     results['max_drawdown'] * 100,
        'avg_drawdown':     results.get('avg_drawdown', np.nan) * 100,
        'ann_volatility':   results['ann_volatility'] * 100,
        'trade_win_rate':   results['trade_win_rate'] * 100,
        'monthly_win_rate': results['win_rate'] * 100,
        'beta':             results.get('beta', np.nan),
        'alpha':            results['alpha'] * 100 if pd.notna(results.get('alpha', np.nan)) else np.nan,
        'total_trades':     results['total_trades_count'],
        'pct_time_in_cash': results.get('pct_time_in_cash', np.nan) * 100,
    }
    return {'csm': csm, 'results': results, 'detailed_log': detailed_log, 'metrics': metrics}


# ══════════════════════════════════════════════════════════════════════════════
# A/B COMPARISON
# ══════════════════════════════════════════════════════════════════════════════

def compare_variants(baseline, treatment, etf_tickers):
    print("\n" + "=" * 70)
    print("  A/B COMPARISON  —  equity-only  vs  equity + gold/silver ETFs  (csm_absolute)")
    print("=" * 70)

    bm, tm = baseline['metrics'], treatment['metrics']
    rows = [
        ('CAGR (%)',               'cagr'),
        ('Sharpe',                 'sharpe'),
        ('Sortino',                'sortino'),
        ('Calmar',                 'calmar'),
        ('Max Drawdown (%)',       'max_drawdown'),
        ('Avg Drawdown (%)',       'avg_drawdown'),
        ('Ann. Volatility (%)',    'ann_volatility'),
        ('Trade Win Rate (%)',     'trade_win_rate'),
        ('Monthly Win Rate (%)',   'monthly_win_rate'),
        ('Beta (vs equity bench)', 'beta'),
        ('Alpha (%/yr)',           'alpha'),
        ('Total Trades',           'total_trades'),
        ('Pct Time in Cash (%)',   'pct_time_in_cash'),
    ]
    print(f"\n{'Metric':<26}{'Equity-Only':>16}{'+Gold/Silver':>16}{'Diff':>12}")
    print("-" * 70)
    for label, key in rows:
        b, t = bm.get(key, np.nan), tm.get(key, np.nan)
        diff = (t - b) if (pd.notna(b) and pd.notna(t)) else np.nan
        print(f"{label:<26}{b:>16.3f}{t:>16.3f}{diff:>12.3f}")

    # ── Gold/silver-specific attribution (within the treatment run) ─────────
    print("\n" + "-" * 70)
    print("  GOLD/SILVER CONTRIBUTION  (inside the +ETF run)")
    print("-" * 70)

    csm, results, log = treatment['csm'], treatment['results'], treatment['detailed_log']
    ew = results['executed_weights']
    total_pnl_abs = log['PnL_Abs'].sum() if not log.empty else np.nan

    for ticker in etf_tickers:
        if ticker not in ew.columns:
            print(f"\n{ticker}: not present in the merged universe (file missing?)")
            continue

        col       = ew[ticker]
        held_days = int((col > 1e-6).sum())
        pct_days  = held_days / len(col) * 100 if len(col) else 0.0
        avg_wt    = col[col > 1e-6].mean() * 100 if held_days else 0.0

        t_log     = log[log['Ticker'] == ticker] if not log.empty else pd.DataFrame()
        n_trades  = len(t_log)
        win_rate  = (t_log['PnL_Pct'] > 0).mean() * 100 if n_trades else np.nan
        pnl_abs   = t_log['PnL_Abs'].sum() if n_trades else 0.0
        pnl_share = (pnl_abs / total_pnl_abs * 100) if total_pnl_abs and pd.notna(total_pnl_abs) else np.nan
        avg_hold  = t_log['Holding_Days'].mean() if n_trades else np.nan

        corr = np.nan
        if ticker in csm.prices.columns and csm.benchmark is not None:
            etf_ret   = csm.prices[ticker].pct_change(fill_method=None)
            bench_ret = csm.benchmark.pct_change(fill_method=None)
            corr = etf_ret.reindex(bench_ret.index).corr(bench_ret)

        print(f"\n{ticker}:")
        print(f"  Held {held_days}/{len(col)} trading days in the report window ({pct_days:.1f}%), "
              f"avg executed weight when held: {avg_wt:.2f}%")
        print(f"  Trades: {n_trades}  |  Win rate: {win_rate:.1f}%  |  Avg holding days: {avg_hold:.1f}")
        print(f"  P&L contribution: Rs.{pnl_abs:,.0f}  ({pnl_share:.2f}% of total strategy P&L)")
        print(f"  Daily-return correlation vs equity benchmark: {corr:.2f}")
        if n_trades:
            print(f"  Exit reasons: {t_log['Exit_Reason'].value_counts().to_dict()}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # ── 1. Load equity universe ──────────────────────────────────────────────
    print("Loading equity data...")
    eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens = load_data(EQUITY_DATA_FOLDER)
    if eq_prices.empty:
        print("Error: No equity data loaded.")
        return

    # ── 2. Load gold/silver ETF data and merge onto the equity panels ───────
    print("Loading gold/silver ETF data...")
    etf_prices, etf_volumes, etf_highs, etf_lows, etf_opens = load_etf_data(
        ETF_DATA_FOLDER, DEFAULT_ETF_TICKERS
    )
    combo_prices, combo_volumes, combo_highs, combo_lows, combo_opens = merge_panels(
        (eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens),
        (etf_prices, etf_volumes, etf_highs, etf_lows, etf_opens),
    )

    # ── 3. Defensive index cleaning — mirrors run_csm_absolute.py's main() ──
    eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens = (
        _clean_index(eq_prices), _clean_index(eq_volumes), _clean_index(eq_highs),
        _clean_index(eq_lows), _clean_index(eq_opens),
    )
    combo_prices, combo_volumes, combo_highs, combo_lows, combo_opens = (
        _clean_index(combo_prices), _clean_index(combo_volumes), _clean_index(combo_highs),
        _clean_index(combo_lows), _clean_index(combo_opens),
    )

    def _clip(df):
        return df.loc[START_LOAD:END_LOAD] if not df.empty else df

    eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens = (
        _clip(eq_prices), _clip(eq_volumes), _clip(eq_highs), _clip(eq_lows), _clip(eq_opens)
    )
    combo_prices, combo_volumes, combo_highs, combo_lows, combo_opens = (
        _clip(combo_prices), _clip(combo_volumes), _clip(combo_highs), _clip(combo_lows), _clip(combo_opens)
    )

    added = [c for c in combo_prices.columns if c in DEFAULT_ETF_TICKERS]
    print(f"Equity-only universe   : {eq_prices.shape}")
    print(f"+ETF combined universe : {combo_prices.shape}  (added: {added})")

    # ── 4. Benchmark — EQUITY-ONLY in both runs (crash-guard / regime signal,
    #    not the tradeable universe; must stay identical across the A/B pair).
    print("Creating synthetic equal-weight equity benchmark...")
    benchmark_price = (1 + eq_prices.pct_change().clip(-.5, .5).mean(axis=1)).cumprod()

    # ── 5. Run both variants ─────────────────────────────────────────────────
    baseline = run_variant(
        "equity_only", eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens,
        benchmark_price, REPORT_START,
    )
    treatment = run_variant(
        "equity_gold_silver", combo_prices, combo_volumes, combo_highs, combo_lows, combo_opens,
        benchmark_price, REPORT_START,
    )

    # ── 6. Diff ───────────────────────────────────────────────────────────────
    compare_variants(baseline, treatment, DEFAULT_ETF_TICKERS)

    return {'equity_only': baseline['metrics'], 'equity_gold_silver': treatment['metrics']}


if __name__ == "__main__":
    main()
