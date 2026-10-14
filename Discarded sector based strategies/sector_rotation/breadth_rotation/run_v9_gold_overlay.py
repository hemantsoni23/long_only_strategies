"""
run_v9_gold_overlay.py
=========================
Ports run_csm_absolute_etf_overlay.py's architecture onto v9: an ADDITIVE
POST-HOC OVERLAY, not a merged universe. v9 (sector_breadth_strategy_v9.py)
runs completely UNMODIFIED -- same call, same production config. Gold gets
a shot only at capital v9's own equity engine left unallocated that day,
sized to NEVER exceed that residual, using its OWN standalone signal (no
competition with sectors/stocks for a slot -- the exact failure mode the
reference file's first two attempts hit).

GOLD-ONLY for this pass: SILVERBEES has zero price history before
2022-02-07 (no IS-window data at all), and GOLDBEES itself starts
2007-03-19 (missing ~4 years of the 2003-2012 IS window). Both facts are
handled by construction, not truncation -- gold's signal is NaN before its
data exists, `qualifies` correctly evaluates False, so it naturally
contributes nothing pre-2007 without needing to shrink the reporting
window. Full gold+silver test deferred to the OOS pass (2013-2025), where
silver at least partially participates.

Concretely, each day:
    equity_w_sum(t) = v9's own positions_df.sum(axis=1)        [unmodified,
                        already regime-aware via leverage/corr/vol-scale]
    residual(t)      = max(0, 1 - equity_w_sum(t))
    gold_target(t)   = 1.0 if gold's OWN monthly dual-Sharpe momentum factor
                       clears sharpe_threshold AND has positive absolute
                       return (evaluated standalone), else 0
    gold_weight(t)   = gold_target(t) scaled down (never up) to fit inside
                       residual(t) -- MAX_ETF_SLEEVE_TOTAL=1.0, uncapped,
                       matching the reference file's default
    blended_ret(t)   = v9_stock_return(t) + gold_weight(t) * gold_return(t)
                       (v9's compute_portfolio_returns() already implies 0%
                       on unallocated capital -- nothing to back out before
                       adding gold's contribution, unlike the csm_absolute
                       engine which explicitly modeled a cash/RFR leg)

No transaction cost modeled on the gold sleeve -- v9's own equity returns
(compute_portfolio_returns) aren't cost-adjusted either anywhere in this
session's work, so leaving gold cost-free keeps the A/B comparison on the
same basis rather than introducing a new, asymmetric convention for one
sleeve only.

RESULT (IS 2003-2012, gold-only): v9 alone CAGR=17.14%/Sharpe=1.334/
Calmar=0.863/MaxDD=-19.86% -> v9+gold CAGR=19.54%/Sharpe=1.410/
Sortino=1.213/Calmar=1.020/MaxDD=-19.16% -- first Calmar >1.0 this session,
and MaxDD improved ALONGSIDE CAGR (not traded off against it). Gold sleeve
active 381/2497 days (15.3%), avg weight when active 57.95%, 19 distinct
holding stretches. Improvement is concentrated entirely in 2008 (+13.74pp),
2009 (+6.52pp), 2010 (+2.61pp) -- zero diff every other year (no gold data
pre-2007; signal simply didn't qualify in 2011-2012) -- consistent with
gold's low-correlation role kicking in exactly during equity stress, not a
scattered/lucky effect.

NOT YET DONE: add SILVERBEES back in (has data from 2022, so only usable
once testing moves to OOS); run this overlay against OOS (2013-2025) once
v9 itself clears Playbook Stage 4.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v9 as S

ETF_DATA_FOLDER = "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data"
ETF_TICKERS = ["GOLDBEES"]   # silver deferred to the OOS pass -- see module docstring

# Standalone dual-Sharpe momentum gate for the ETF sleeve -- same construction
# as run_csm_absolute_etf_overlay.py's compute_etf_overlay_signal(), ported
# directly rather than reusing v9's own sector-level factor (breadth-
# divergence needs many constituents to measure "breadth of confirmation";
# it doesn't mean anything applied to a single instrument like gold).
ETF_LOOKBACK_MONTHS       = 9
ETF_LOOKBACK_SHORT_MONTHS = 4
ETF_LAG_MONTHS            = 1
ETF_SHARPE_THRESHOLD      = 0.6
ETF_ATR_PERIOD            = 13
ETF_ATR_MULTIPLIER        = 2.0

MAX_ETF_SLEEVE_TOTAL = 1.0   # uncapped, matches the reference file's default


# ══════════════════════════════════════════════════════════════════════════
# ETF DATA LOADING
# ══════════════════════════════════════════════════════════════════════════

def load_etf_data(folder_path, tickers):
    price_list, high_list, low_list = [], [], []
    for ticker in tickers:
        path = os.path.join(folder_path, f"{ticker}.csv")
        if not os.path.exists(path):
            print(f"Warning: ETF file not found, skipping: {path}")
            continue
        df = pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")
        df.index = df.index.tz_localize(None)
        df = df[~df.index.duplicated(keep="last")]
        price_list.append(df["close"].rename(ticker))
        high_list.append(df["high"].rename(ticker))
        low_list.append(df["low"].rename(ticker))

    def _build(lst):
        return pd.concat(lst, axis=1).sort_index() if lst else pd.DataFrame()

    prices, highs, lows = _build(price_list), _build(high_list), _build(low_list)
    print(f"Loaded {len(price_list)}/{len(tickers)} ETF(s) from {folder_path}: {list(prices.columns)}")
    if not prices.empty:
        for t in prices.columns:
            first_valid = prices[t].first_valid_index()
            print(f"  {t}: data from {first_valid.date()}")
    return prices, highs, lows


# ══════════════════════════════════════════════════════════════════════════
# ETF OVERLAY SIGNAL -- standalone dual-Sharpe momentum + self-scaling stop
# ══════════════════════════════════════════════════════════════════════════

def compute_etf_overlay_signal(etf_prices, etf_highs, etf_lows):
    """Monthly dual-Sharpe momentum gate, applied standalone to the ETF
    universe -- no ranking, no capacity competition with equities. Every
    ETF that clears (factor > sharpe_threshold AND positive absolute
    return) qualifies; with only one ticker (gold) here, a qualifying day
    just gets full target weight (1.0, later scaled down to fit residual).
    A per-ETF ATR chandelier (built from the ETF's OWN volatility) forces
    the sleeve flat for the rest of the calendar month if breached.
    Returns a daily target-weight DataFrame, already lagged 1 trading day.
    """
    monthly_prices = etf_prices.resample("ME").last()
    monthly_ret = monthly_prices.pct_change(fill_method=None)

    ret_long = (monthly_prices.shift(ETF_LAG_MONTHS) / monthly_prices.shift(ETF_LAG_MONTHS + ETF_LOOKBACK_MONTHS)) - 1
    vol_long = monthly_ret.rolling(ETF_LOOKBACK_MONTHS).std().shift(ETF_LAG_MONTHS) * np.sqrt(12)
    factor_long = ret_long / vol_long.replace(0, np.nan)

    ret_short = (monthly_prices.shift(ETF_LAG_MONTHS) / monthly_prices.shift(ETF_LAG_MONTHS + ETF_LOOKBACK_SHORT_MONTHS)) - 1
    vol_short = monthly_ret.rolling(ETF_LOOKBACK_SHORT_MONTHS).std().shift(ETF_LAG_MONTHS) * np.sqrt(12)
    factor_short = ret_short / vol_short.replace(0, np.nan)

    factor = ((factor_long + factor_short) / 2.0).clip(-5.0, 5.0)
    qualifies = (factor > ETF_SHARPE_THRESHOLD) & (ret_long > 0)

    tickers = list(etf_prices.columns)
    monthly_w = pd.DataFrame(0.0, index=factor.index, columns=tickers)
    for d in factor.index:
        q = qualifies.loc[d].fillna(False)
        names = [t for t in tickers if bool(q.get(t, False))]
        if names:
            monthly_w.loc[d, names] = 1.0 / len(names)   # equal-split if >1 qualifies

    daily_target = monthly_w.reindex(etf_prices.index, method="ffill").shift(1).fillna(0.0)

    prev_c = etf_prices.shift(1)
    tr = np.maximum(etf_highs - etf_lows,
                     np.maximum((etf_highs - prev_c).abs(), (etf_lows - prev_c).abs()))
    atr = tr.rolling(ETF_ATR_PERIOD, min_periods=max(1, ETF_ATR_PERIOD // 2)).mean()

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
                stop_level = peak - ETF_ATR_MULTIPLIER * _atr
                if px < stop_level:
                    stopped_this_month = True
                    final_weight.at[date, ticker] = 0.0

    return final_weight, factor, qualifies


# ══════════════════════════════════════════════════════════════════════════
# RESIDUAL CAPITAL SIZING + RETURN BLENDING
# ══════════════════════════════════════════════════════════════════════════

def apply_residual_cap(etf_raw_weight, equity_positions_df, max_etf_sleeve_total=MAX_ETF_SLEEVE_TOTAL):
    """Scale the ETF sleeve's raw target DOWN (never up) so it never exceeds
    the capital v9's own equity engine left unused that day."""
    equity_w_sum = equity_positions_df.sum(axis=1)
    residual = (1.0 - equity_w_sum).clip(lower=0.0).clip(upper=max_etf_sleeve_total)

    etf_raw_weight = etf_raw_weight.reindex(equity_positions_df.index).fillna(0.0)
    etf_raw_sum = etf_raw_weight.sum(axis=1)

    scale = pd.Series(0.0, index=etf_raw_sum.index)
    mask = etf_raw_sum > 1e-9
    scale[mask] = (residual[mask] / etf_raw_sum[mask]).clip(upper=1.0)

    etf_weight = etf_raw_weight.mul(scale, axis=0)
    return etf_weight, residual


def blend_returns(equity_port_ret, etf_weight, etf_prices):
    """v9's compute_portfolio_returns() already implies 0% on unallocated
    capital (nothing added for the residual) -- so unlike the csm_absolute
    engine, there's no pre-existing cash-return leg to back out first."""
    idx = equity_port_ret.index
    etf_weight = etf_weight.reindex(idx).fillna(0.0)
    etf_prices = etf_prices.reindex(idx).ffill()
    etf_daily_ret = etf_prices.pct_change(fill_method=None).reindex(idx).fillna(0.0)
    etf_gross_ret = (etf_weight * etf_daily_ret).sum(axis=1)
    return equity_port_ret + etf_gross_ret, etf_gross_ret


# ══════════════════════════════════════════════════════════════════════════
# REPORTING
# ══════════════════════════════════════════════════════════════════════════

def print_comparison(equity_metrics, blended_metrics):
    print(f"\n{'='*80}\nA/B COMPARISON  --  v9 equity-only (unmodified)  vs  v9 + gold residual-fill overlay\n{'='*80}")
    rows = [
        ("CAGR (%)", equity_metrics["CAGR"] * 100, blended_metrics["CAGR"] * 100),
        ("Sharpe", equity_metrics["Sharpe"], blended_metrics["Sharpe"]),
        ("Sortino", equity_metrics["Sortino"], blended_metrics["Sortino"]),
        ("Calmar", equity_metrics["Calmar"], blended_metrics["Calmar"]),
        ("Max Drawdown (%)", equity_metrics["MaxDD"] * 100, blended_metrics["MaxDD"] * 100),
        ("Ann. Volatility (%)", equity_metrics["AnnVol"] * 100, blended_metrics["AnnVol"] * 100),
        ("Monthly Win Rate (%)", equity_metrics["WinRateMonthly"] * 100, blended_metrics["WinRateMonthly"] * 100),
    ]
    print(f"\n{'Metric':<24}{'v9 Equity-Only':>18}{'v9 + Gold':>14}{'Diff':>12}")
    print("-" * 68)
    for label, b, t in rows:
        print(f"{label:<24}{b:>18.3f}{t:>14.3f}{(t - b):>12.3f}")


def summarize_gold_sleeve(etf_weight, etf_prices, tickers):
    etf_ret = etf_prices.pct_change(fill_method=None).reindex(etf_weight.index).fillna(0.0)
    print(f"\n{'-'*80}\nGOLD OVERLAY SLEEVE -- summary (full IS backtest window, 2003-2012)\n{'-'*80}")
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


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("Loading OHLCV data + building v9 factors (unmodified)...")
    prices, volumes, highs, lows, opens = S.load_data(S.DATA_FOLDER)
    members = S.build_sector_membership(prices, S.INSTRUMENTS_CSV)
    universe_mask = S.build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = S.build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = S.build_sector_rank(prices, members, universe_mask,
                                                          sector_price, daily_ret)
    sma_slow, trend_ok, persistence, stock_quality = S.build_stock_factors(prices)
    atr = S.build_atr(prices, highs, lows)
    bench_ok, is_panic, leverage = S.compute_regime(sector_price)
    stock_daily_ret, stock_vol = S.build_stock_vol(prices)
    falling_knife = S.build_falling_knife_gate(prices)

    print(f"\n{'#'*70}\n#  BASELINE: v9 equity-only (unmodified, same call as its own main())\n{'#'*70}")
    positions_df, trade_log_df = S.run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr,
        is_panic, leverage, stock_daily_ret, stock_vol,
        falling_knife=falling_knife, stock_quality=stock_quality,
    )
    equity_port_ret = S.compute_portfolio_returns(positions_df, prices)
    equity_metrics, equity_equity, equity_dd, equity_monthly = S.compute_metrics(equity_port_ret)
    print(f"  v9 alone: CAGR={equity_metrics['CAGR']*100:+.2f}%  Sharpe={equity_metrics['Sharpe']:.3f}  "
          f"Calmar={equity_metrics['Calmar']:.3f}  MaxDD={equity_metrics['MaxDD']*100:.2f}%")

    print(f"\n{'#'*70}\n#  GOLD OVERLAY: residual-capital-driven sleeve\n{'#'*70}")
    etf_prices, etf_highs, etf_lows = load_etf_data(ETF_DATA_FOLDER, ETF_TICKERS)
    etf_prices = etf_prices.reindex(prices.index).ffill()
    etf_highs = etf_highs.reindex(prices.index).ffill()
    etf_lows = etf_lows.reindex(prices.index).ffill()

    etf_weight_raw, gold_factor, gold_qualifies = compute_etf_overlay_signal(etf_prices, etf_highs, etf_lows)
    etf_weight, residual = apply_residual_cap(etf_weight_raw, positions_df)

    # Slice to v9's own backtest window (2003-2012) for the blend/report --
    # positions_df/equity_port_ret are already scoped to that window.
    etf_weight_bt = etf_weight.reindex(equity_port_ret.index).fillna(0.0)

    blended_ret, gold_gross_ret = blend_returns(equity_port_ret, etf_weight_bt, etf_prices)
    blended_metrics, blended_equity, blended_dd, blended_monthly = S.compute_metrics(blended_ret)
    print(f"  v9 + gold: CAGR={blended_metrics['CAGR']*100:+.2f}%  Sharpe={blended_metrics['Sharpe']:.3f}  "
          f"Calmar={blended_metrics['Calmar']:.3f}  MaxDD={blended_metrics['MaxDD']*100:.2f}%")

    print_comparison(equity_metrics, blended_metrics)
    summarize_gold_sleeve(etf_weight_bt, etf_prices, ETF_TICKERS)

    yr_equity = S.yearly_table(equity_port_ret, equity_equity)
    yr_blended = S.yearly_table(blended_ret, blended_equity)
    print(f"\n{'='*80}\nYEARLY RETURNS  --  v9 alone vs v9+gold\n{'='*80}")
    print(f"{'Year':<8}{'v9 Alone':>12}{'v9+Gold':>12}{'Diff':>10}")
    for yr in yr_equity.index:
        a = yr_equity.loc[yr, "Return"] * 100
        b = yr_blended.loc[yr, "Return"] * 100
        print(f"{yr:<8}{a:>11.2f}%{b:>11.2f}%{(b-a):>9.2f}%")

    out = os.path.join(os.path.dirname(__file__), "v9_gold_overlay_returns.csv")
    pd.DataFrame({"equity_only": equity_port_ret, "blended": blended_ret,
                  "gold_weight": etf_weight_bt["GOLDBEES"], "gold_gross_ret": gold_gross_ret}).to_csv(out)
    print(f"\nSaved daily blended return series to {out}")


if __name__ == "__main__":
    main()
