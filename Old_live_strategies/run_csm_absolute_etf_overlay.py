"""
run_csm_absolute_etf_overlay.py
================================
Third attempt at the gold/silver question — and a different architecture from
the first two, per explicit feedback that both were wrong:

  run_csm_batch_strategy_gold_silver.py   : merged GOLDBEES/SILVERBEES into the
                                             SAME top_n=30 RANK contest as equities.
                                             They almost never out-ranked India's
                                             best momentum smallcaps (SILVERBEES:
                                             0 trades in ~4y of eligibility).
  run_csm_absolute_gold_silver.py         : merged them into the SAME absolute-
                                             gate universe (capacity_limit=25).
                                             They DID get selected this time, but
                                             the equity-tuned 8%/12% hard stops
                                             (built for fast smallcap breakouts)
                                             cut gold's slower trend short, and
                                             their footprint was too small to
                                             move the needle either way.

Both of those treat gold/silver as "another stock" competing for a portfolio
slot. That's not where their value is. The point of a LOW-CORRELATION asset is
capital that would otherwise sit idle — this file targets exactly that capital:

  1. The equity strategy's OWN leverage regime (leverage_bull=1.0 / bear=0.8 /
     panic=0.5) already throttles how much of the book gets deployed. Whatever
     it does NOT deploy — whether from the regime cut, or simply too few
     qualifying momentum candidates that day — is "residual" capital.
  2. Gold/silver get a shot at exactly that residual, gated by THEIR OWN
     absolute momentum signal (same dual-Sharpe formula/threshold as the main
     strategy, applied standalone — no competition with equities for a slot).
  3. If neither ETF has a signal either, the residual still falls back to
     Liquid MF parking — same as the current strategy's behavior on a break.

This is an ADDITIVE POST-HOC OVERLAY, not a merged universe: the equity leg is
run through IndividualMomentumStrategy / backtest_event_driven completely
UNMODIFIED (same call as run_csm_absolute.py, same production parameters). Its
own executed_weights already correctly reflect the bull/bear/panic regime — the
residual gap (1 − equity_weight) is read directly off that, so the regime logic
is inherited for free rather than re-implemented. The ETF sleeve's own exit is
an ATR chandelier computed from the ETF's OWN volatility (self-scaling), not the
equity-calibrated fixed-percentage stops that hurt the previous attempt.

No changes to csm_absolute.py / csm_absolute_backtest.py / run_csm_absolute.py.

Concretely, each day:
    residual(t)   = max(0, 1 − equity_weight_sum(t))          [already regime-aware]
    etf_target(t) = inverse-vol split across ETFs whose OWN monthly dual-Sharpe
                    factor clears sharpe_threshold AND has positive absolute
                    return (same gate as the main strategy, evaluated standalone)
    etf_weight(t) = etf_target(t) scaled down (never up) to fit inside residual(t)
    still-idle(t) = max(0, 1 − equity_weight(t) − etf_weight(t))
                    -> Liquid MF if BOTH sleeves are at zero, else RFR (0%)
                    (mirrors "if we still get a break after trying ETFs, park
                    in liquid" from the brief)

Data sources
------------
Equity : /Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data  (same as
         run_csm_absolute.py)
ETF    : /Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data
         Default tickers: GOLDBEES, SILVERBEES.

Tunable at the top of this file: MAX_ETF_SLEEVE_TOTAL caps how much of the
residual the ETF sleeve is allowed to claim (default 1.0 = no extra cap beyond
the residual itself — a full break can go 100% into ETFs if their signal is on).
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
    print_yearly_returns,
    detect_strategy_breaks,
)

EQUITY_DATA_FOLDER  = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
ETF_DATA_FOLDER     = "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data"
DEFAULT_ETF_TICKERS = ["GOLDBEES", "SILVERBEES"]

# Date windows — identical to run_csm_absolute.py's production defaults.
START_LOAD   = '2019-01-01'
END_LOAD     = '2025-12-31'
REPORT_START = '2020-01-01'

# How much of the residual (unused equity capital) the ETF sleeve may claim.
# 1.0 = no extra cap — a full equity break can go 100% into ETFs if their own
# signal is active. Lower this (e.g. 0.3) to keep the sleeve as a smaller,
# more conservative top-up instead of a full cash substitute.
MAX_ETF_SLEEVE_TOTAL = 1.0

# Strategy parameters for the EQUITY leg — identical to run_csm_absolute.py's
# production config, run completely unmodified.
STRATEGY_KWARGS = dict(
    lookback_months        = 9,
    lookback_short_months  = 4,
    atr_period              = 13,
    atr_multiplier          = 2.0,
    lag_months              = 1,
    sharpe_threshold        = 0.6,
    capacity_limit          = 25,
    universe_top_n          = 1000,
    leverage_bull           = 1.0,
    leverage_bear           = 0.8,
    leverage_panic          = 0.5,
    min_price               = 20.0,
    max_circuit_days        = 8,
    max_weight_per_stock    = 0.12,
    stop_std_devs           = 3.0,
    use_rebalance           = True,
    rebalance_months        = 3,
    use_trailing            = True,
    reentry_cooldown_days   = 7,
    rank_buffer             = 1.5,
    cooldown_losers_only    = True,
    use_take_profit         = True,
)
BT_KWARGS = dict(
    initial_capital            = 100_000,
    transaction_cost           = 0.003,
    risk_free_rate              = 0.00,
    hard_stop_from_entry_pct   = 0.08,
    hard_stop_from_peak_pct    = 0.12,
    use_limit_orders           = True,
    stop_approach_pct          = 0.02,
    trail_approach_pct         = 0.03,
    order_ttl_days             = 4,
    order_fill_assumption      = 'limit_price',
    use_liquid_mf              = True,
    liquid_mf_annual_rate      = 0.0,
)


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

def load_etf_data(folder_path, tickers):
    """Load specific ETF CSVs. The files differ from the equity ones only in
    the index column name ('timestamp' vs 'datetime') and an explicit +05:30
    offset on every row (always midnight IST — the trading day)."""
    price_list, high_list, low_list = [], [], []
    for ticker in tickers:
        path = os.path.join(folder_path, f"{ticker}.csv")
        if not os.path.exists(path):
            print(f"Warning: ETF file not found, skipping: {path}")
            continue
        df = pd.read_csv(path, parse_dates=['timestamp'], index_col='timestamp')
        df.index = df.index.tz_localize(None)
        df = df[~df.index.duplicated(keep='last')]
        price_list.append(df['close'].rename(ticker))
        high_list.append(df['high'].rename(ticker))
        low_list.append(df['low'].rename(ticker))

    def _build(lst):
        return pd.concat(lst, axis=1).sort_index() if lst else pd.DataFrame()

    prices, highs, lows = _build(price_list), _build(high_list), _build(low_list)
    print(f"Loaded {len(price_list)}/{len(tickers)} ETF(s) from {folder_path}: {list(prices.columns)}")
    return prices, highs, lows


def _clean_index(df):
    """Mirrors run_csm_absolute.py's defensive index cleaning."""
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
# ETF OVERLAY SIGNAL — standalone absolute momentum gate + self-scaling stop
# ══════════════════════════════════════════════════════════════════════════════

def compute_etf_overlay_signal(etf_prices, etf_highs, etf_lows,
                                lookback_months, lookback_short_months, lag_months,
                                sharpe_threshold, atr_period, atr_multiplier):
    """
    Monthly dual-Sharpe momentum gate (same formula as
    IndividualMomentumStrategy.calculate_factors()), applied standalone to the
    ETF universe only — no ranking, no capacity competition. Every ETF that
    clears (factor > sharpe_threshold AND positive absolute return) qualifies
    and gets sized by inverse-vol among qualifiers.

    A per-ETF ATR chandelier (built from the ETF's OWN ATR, not a fixed
    equity-calibrated percentage) forces the sleeve flat for the rest of the
    calendar month if breached — addressing the mismatched-stop finding from
    run_csm_absolute_gold_silver.py, where fixed 8%/12% equity stops cut
    gold's slower trend short.

    Returns a daily target-weight DataFrame, already lagged 1 trading day
    (no lookahead) — same convention the main engine uses.
    """
    monthly_prices = etf_prices.resample('ME').last()
    monthly_ret = monthly_prices.pct_change(fill_method=None)

    ret_long = (monthly_prices.shift(lag_months) / monthly_prices.shift(lag_months + lookback_months)) - 1
    vol_long = monthly_ret.rolling(lookback_months).std().shift(lag_months) * np.sqrt(12)
    factor_long = ret_long / vol_long.replace(0, np.nan)

    ret_short = (monthly_prices.shift(lag_months) / monthly_prices.shift(lag_months + lookback_short_months)) - 1
    vol_short = monthly_ret.rolling(lookback_short_months).std().shift(lag_months) * np.sqrt(12)
    factor_short = ret_short / vol_short.replace(0, np.nan)

    factor = ((factor_long + factor_short) / 2.0).clip(-5.0, 5.0)
    qualifies = (factor > sharpe_threshold) & (ret_long > 0)

    daily_vol = etf_prices.pct_change(fill_method=None).rolling(21).std().shift(1)
    monthly_vol = daily_vol.resample('ME').last().reindex(factor.index)

    tickers = list(etf_prices.columns)
    monthly_w = pd.DataFrame(0.0, index=factor.index, columns=tickers)
    for d in factor.index:
        q = qualifies.loc[d].fillna(False)
        names = [t for t in tickers if bool(q.get(t, False))]
        if not names:
            continue
        vols = monthly_vol.loc[d, names].fillna(0.02).replace(0, 0.02)
        inv = 1.0 / vols
        monthly_w.loc[d, names] = inv / inv.sum()

    daily_target = monthly_w.reindex(etf_prices.index, method='ffill').shift(1).fillna(0.0)

    prev_c = etf_prices.shift(1)
    tr = np.maximum(etf_highs - etf_lows,
                     np.maximum((etf_highs - prev_c).abs(), (etf_lows - prev_c).abs()))
    atr = tr.rolling(atr_period, min_periods=max(1, atr_period // 2)).mean()

    final_weight = daily_target.copy()
    for ticker in tickers:
        peak = np.nan
        stopped_this_month = False
        cur_month_key = None
        for date in etf_prices.index:
            month_key = (date.year, date.month)
            if month_key != cur_month_key:
                cur_month_key = month_key
                stopped_this_month = False
                peak = np.nan

            tgt = daily_target.at[date, ticker] if date in daily_target.index else 0.0
            if tgt <= 1e-9:
                continue
            if stopped_this_month:
                final_weight.at[date, ticker] = 0.0
                continue

            px = etf_prices.at[date, ticker] if date in etf_prices.index else np.nan
            if pd.isna(px) or px <= 0:
                continue
            peak = px if (pd.isna(peak) or px > peak) else peak

            _atr = atr.at[date, ticker] if date in atr.index else np.nan
            if pd.notna(_atr) and _atr > 0:
                stop_level = peak - atr_multiplier * _atr
                if px < stop_level:
                    stopped_this_month = True
                    final_weight.at[date, ticker] = 0.0

    return final_weight, factor, qualifies


# ══════════════════════════════════════════════════════════════════════════════
# RESIDUAL CAPITAL SIZING + RETURN BLENDING
# ══════════════════════════════════════════════════════════════════════════════

def apply_residual_cap(etf_raw_weight, equity_weights, max_etf_sleeve_total=1.0):
    """Scale the ETF sleeve's raw target DOWN (never up) so it never exceeds
    the capital the equity leg actually left unused that day. equity_weights
    already reflects the bull/bear/panic leverage regime AND any candidate
    shortfall — the regime logic is inherited for free, not re-derived here."""
    equity_w_sum = equity_weights.sum(axis=1)
    residual = (1.0 - equity_w_sum).clip(lower=0.0).clip(upper=max_etf_sleeve_total)

    etf_raw_weight = etf_raw_weight.reindex(equity_weights.index).fillna(0.0)
    etf_raw_sum = etf_raw_weight.sum(axis=1)

    scale = pd.Series(0.0, index=etf_raw_sum.index)
    mask = etf_raw_sum > 1e-9
    scale[mask] = (residual[mask] / etf_raw_sum[mask]).clip(upper=1.0)

    etf_weight = etf_raw_weight.mul(scale, axis=0)
    return etf_weight, residual


def blend_returns(equity_raw_results, etf_weight, etf_prices, transaction_cost):
    """Swap out the cash return the UNMODIFIED equity engine already added for
    idle capital, and replace it with the ETF sleeve's actual return (net of
    its own transaction cost) plus whatever's still unfilled after both
    sleeves — which now only falls back to Liquid MF if BOTH are at zero."""
    idx = equity_raw_results['executed_weights'].index
    etf_weight = etf_weight.reindex(idx).fillna(0.0)
    etf_prices = etf_prices.reindex(idx).ffill()

    etf_daily_ret = etf_prices.pct_change(fill_method=None).reindex(idx).fillna(0.0)
    etf_gross_ret = (etf_weight * etf_daily_ret).sum(axis=1)
    etf_turnover  = etf_weight.diff().abs().sum(axis=1).fillna(0.0)
    etf_txn_cost  = etf_turnover * transaction_cost

    equity_w_sum = equity_raw_results['executed_weights'].sum(axis=1)
    etf_w_sum    = etf_weight.sum(axis=1)

    daily_rfr = (1.0 + equity_raw_results['risk_free_rate']) ** (1.0 / 252) - 1.0
    use_lmf   = equity_raw_results.get('use_liquid_mf', False)
    lmf_rate  = equity_raw_results.get('liquid_mf_annual_rate', 0.0)
    daily_lmf = (1.0 + lmf_rate) ** (1.0 / 252) - 1.0

    # Cash return the ORIGINAL (equity-only) engine already baked into
    # net_returns — must be backed out before adding the ETF-fill return.
    cash_w_orig    = (1.0 - equity_w_sum).clip(lower=0.0)
    is_idle_orig   = equity_w_sum < 1e-6
    cash_rate_orig = pd.Series(daily_rfr, index=idx)
    if use_lmf:
        cash_rate_orig[is_idle_orig] = daily_lmf
    cash_ret_original = cash_w_orig * cash_rate_orig

    # Cash return on whatever's STILL unfilled after equity + ETF sleeve.
    remaining_cash_w = (1.0 - equity_w_sum - etf_w_sum).clip(lower=0.0)
    is_fully_idle    = (equity_w_sum + etf_w_sum) < 1e-6
    cash_rate_new    = pd.Series(daily_rfr, index=idx)
    if use_lmf:
        cash_rate_new[is_fully_idle] = daily_lmf
    cash_ret_new = remaining_cash_w * cash_rate_new

    blended_net_ret = (equity_raw_results['net_returns'] - cash_ret_original
                        + etf_gross_ret - etf_txn_cost + cash_ret_new)
    return blended_net_ret, etf_gross_ret, etf_txn_cost


def compute_metrics_from_returns(net_returns, report_start, risk_free_rate=0.0, initial_capital=100_000.0):
    """Same metric formulas as compute_metrics()/​_run_event_backtest(), applied
    to an arbitrary blended daily-return series instead of a strategy object."""
    ret = net_returns.loc[report_start:]
    eq  = (1.0 + ret).cumprod()
    eq  = eq / eq.iloc[0] * initial_capital

    n_years = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr    = (eq.iloc[-1] / eq.iloc[0]) ** (1.0 / n_years) - 1.0 if n_years > 0 else 0.0
    ann_vol = ret.std() * np.sqrt(252)

    daily_rfr = (1.0 + risk_free_rate) ** (1 / 252) - 1.0
    excess    = ret - daily_rfr
    sharpe    = np.sqrt(252) * excess.mean() / ret.std() if ret.std() > 0 else 0.0

    dn     = ret.clip(upper=0.0)
    dndev  = np.sqrt((dn ** 2).mean())
    sortino = np.sqrt(252) * ret.mean() / dndev if dndev > 0 else 0.0

    rmax   = eq.cummax()
    dd     = eq / rmax - 1.0
    max_dd = dd.min()
    avg_dd = dd.mean()
    calmar = cagr / abs(max_dd) if max_dd != 0 else 0.0

    mret     = eq.resample('ME').last().pct_change().dropna()
    win_rate = (mret > 0).mean()

    return {
        'equity_curve': eq, 'net_returns': ret, 'cagr': cagr, 'sharpe': sharpe,
        'sortino': sortino, 'calmar': calmar, 'max_drawdown': max_dd,
        'avg_drawdown': avg_dd, 'ann_volatility': ann_vol, 'win_rate': win_rate,
    }


# ══════════════════════════════════════════════════════════════════════════════
# REPORTING
# ══════════════════════════════════════════════════════════════════════════════

def print_comparison(equity_results, blended_metrics):
    print("\n" + "=" * 70)
    print("  A/B COMPARISON  —  equity-only (unmodified)  vs  equity + gold/silver residual-fill overlay")
    print("=" * 70)
    rows = [
        ('CAGR (%)',            equity_results['cagr'] * 100,          blended_metrics['cagr'] * 100),
        ('Sharpe',               equity_results['sharpe'],              blended_metrics['sharpe']),
        ('Sortino',              equity_results['sortino'],             blended_metrics['sortino']),
        ('Calmar',               equity_results['calmar'],              blended_metrics['calmar']),
        ('Max Drawdown (%)',     equity_results['max_drawdown'] * 100,  blended_metrics['max_drawdown'] * 100),
        ('Avg Drawdown (%)',     equity_results.get('avg_drawdown', float('nan')) * 100, blended_metrics['avg_drawdown'] * 100),
        ('Ann. Volatility (%)',  equity_results['ann_volatility'] * 100, blended_metrics['ann_volatility'] * 100),
        ('Monthly Win Rate (%)', equity_results['win_rate'] * 100,      blended_metrics['win_rate'] * 100),
    ]
    print(f"\n{'Metric':<26}{'Equity-Only':>16}{'+ETF Overlay':>16}{'Diff':>12}")
    print("-" * 70)
    for label, b, t in rows:
        print(f"{label:<26}{b:>16.3f}{t:>16.3f}{(t - b):>12.3f}")


def summarize_etf_sleeve(etf_weight, etf_prices, report_start, tickers):
    etf_weight = etf_weight.loc[report_start:]
    etf_ret = etf_prices.pct_change(fill_method=None).reindex(etf_weight.index).fillna(0.0)

    print("\n" + "-" * 70)
    print("  ETF OVERLAY SLEEVE — per-ticker summary (report window)")
    print("-" * 70)
    for t in tickers:
        if t not in etf_weight.columns:
            continue
        w = etf_weight[t]
        active_days = int((w > 1e-6).sum())
        pct_days = active_days / len(w) * 100 if len(w) else 0.0
        avg_w = w[w > 1e-6].mean() * 100 if active_days else 0.0
        contrib_pct_pts = (w * etf_ret[t]).sum() * 100

        is_on = w > 1e-6
        n_stretches = int((is_on & ~is_on.shift(1).fillna(False)).sum())

        print(f"\n{t}:")
        print(f"  Active {active_days}/{len(w)} days ({pct_days:.1f}%), avg weight when active: {avg_w:.2f}%")
        print(f"  Distinct holding stretches: {n_stretches}")
        print(f"  Return contribution (sum of daily weight x return): {contrib_pct_pts:+.2f} pct-pts")

    total_w = etf_weight.sum(axis=1)
    print(f"\nCombined sleeve: active (any ETF) on {int((total_w > 1e-6).sum())}/{len(total_w)} days "
          f"({(total_w > 1e-6).mean() * 100:.1f}%), avg combined weight when active: "
          f"{total_w[total_w > 1e-6].mean() * 100 if (total_w > 1e-6).any() else 0.0:.2f}%")


def compare_break_periods(equity_results, etf_weight_sliced, blended_equity_curve, report_start):
    print("\n" + "=" * 70)
    print("  IDLE-PERIOD ('BREAK') COMPARISON  —  before vs after the ETF overlay")
    print("=" * 70)

    print("\n--- BEFORE: equity-only (unmodified) ---")
    detect_strategy_breaks(
        equity_results['executed_weights'], equity_results['portfolio_value'],
        min_break_days=14,
        use_liquid_mf=equity_results.get('use_liquid_mf', False),
        liquid_mf_annual_rate=equity_results.get('liquid_mf_annual_rate', 0.0),
    )

    print("\n--- AFTER: equity + ETF overlay combined ---")
    combined_weights = equity_results['executed_weights'].add(etf_weight_sliced, fill_value=0.0)
    combined_weights = combined_weights.reindex(blended_equity_curve.index).fillna(0.0)
    detect_strategy_breaks(
        combined_weights, blended_equity_curve,
        min_break_days=14,
        use_liquid_mf=equity_results.get('use_liquid_mf', False),
        liquid_mf_annual_rate=equity_results.get('liquid_mf_annual_rate', 0.0),
    )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("Loading equity data...")
    eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens = load_data(EQUITY_DATA_FOLDER)
    if eq_prices.empty:
        print("Error: No equity data loaded.")
        return

    print("Loading gold/silver ETF data...")
    etf_prices, etf_highs, etf_lows = load_etf_data(ETF_DATA_FOLDER, DEFAULT_ETF_TICKERS)

    eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens = (
        _clean_index(eq_prices), _clean_index(eq_volumes), _clean_index(eq_highs),
        _clean_index(eq_lows), _clean_index(eq_opens),
    )

    def _clip(df):
        return df.loc[START_LOAD:END_LOAD] if not df.empty else df

    eq_prices, eq_volumes, eq_highs, eq_lows, eq_opens = (
        _clip(eq_prices), _clip(eq_volumes), _clip(eq_highs), _clip(eq_lows), _clip(eq_opens)
    )
    print(f"Equity universe: {eq_prices.shape}")

    # Align ETF panels to the equity trading calendar.
    etf_prices = etf_prices.reindex(eq_prices.index).ffill()
    etf_highs  = etf_highs.reindex(eq_prices.index).ffill()
    etf_lows   = etf_lows.reindex(eq_prices.index).ffill()

    print("Creating synthetic equal-weight equity benchmark...")
    benchmark_price = (1 + eq_prices.pct_change().clip(-.5, .5).mean(axis=1)).cumprod()

    # ── 1. Baseline: UNMODIFIED equity strategy, unchanged files/params ─────
    print("\n" + "#" * 70)
    print("#  BASELINE: equity-only IndividualMomentumStrategy (unmodified)")
    print("#" * 70)
    csm = IndividualMomentumStrategy(
        eq_prices, eq_volumes,
        highs_df=eq_highs, lows_df=eq_lows, opens_df=eq_opens,
        benchmark_series=benchmark_price,
        **STRATEGY_KWARGS,
    )
    csm.calculate_factors()
    csm.get_positions()
    raw_results = backtest_event_driven(csm, **BT_KWARGS)

    equity_results = compute_metrics(dict(raw_results), REPORT_START, risk_free_rate=BT_KWARGS['risk_free_rate'])
    equity_results = compute_benchmark_metrics(equity_results, benchmark_price)
    print_report(equity_results)
    print_yearly_returns(equity_results['portfolio_value'])

    # ── 2. ETF overlay signal + residual-capacity sizing ────────────────────
    print("\n" + "#" * 70)
    print("#  ETF OVERLAY: residual-capital-driven gold/silver sleeve")
    print("#" * 70)
    etf_weight_raw, _factor, _qualifies = compute_etf_overlay_signal(
        etf_prices, etf_highs, etf_lows,
        lookback_months=STRATEGY_KWARGS['lookback_months'],
        lookback_short_months=STRATEGY_KWARGS['lookback_short_months'],
        lag_months=STRATEGY_KWARGS['lag_months'],
        sharpe_threshold=STRATEGY_KWARGS['sharpe_threshold'],
        atr_period=STRATEGY_KWARGS['atr_period'],
        atr_multiplier=STRATEGY_KWARGS['atr_multiplier'],
    )
    etf_weight, residual = apply_residual_cap(
        etf_weight_raw, raw_results['executed_weights'], max_etf_sleeve_total=MAX_ETF_SLEEVE_TOTAL,
    )

    blended_net_ret, etf_gross_ret, etf_txn_cost = blend_returns(
        raw_results, etf_weight, etf_prices, transaction_cost=BT_KWARGS['transaction_cost'],
    )
    blended_metrics = compute_metrics_from_returns(
        blended_net_ret, REPORT_START, risk_free_rate=BT_KWARGS['risk_free_rate'],
    )

    # ── 3. Report ─────────────────────────────────────────────────────────────
    print_comparison(equity_results, blended_metrics)
    summarize_etf_sleeve(etf_weight, etf_prices, REPORT_START, DEFAULT_ETF_TICKERS)
    compare_break_periods(
        equity_results, etf_weight.loc[REPORT_START:], blended_metrics['equity_curve'], REPORT_START,
    )

    return {
        'equity_only': {
            'cagr': equity_results['cagr'] * 100, 'sharpe': equity_results['sharpe'],
            'calmar': equity_results['calmar'], 'max_drawdown': equity_results['max_drawdown'] * 100,
        },
        'equity_plus_etf_overlay': {
            'cagr': blended_metrics['cagr'] * 100, 'sharpe': blended_metrics['sharpe'],
            'calmar': blended_metrics['calmar'], 'max_drawdown': blended_metrics['max_drawdown'] * 100,
        },
    }


if __name__ == "__main__":
    main()
