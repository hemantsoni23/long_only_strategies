"""
industry_breadth_strategy_v1.py
==================================
Sector-Breadth-Divergence Rotation -- Event-Driven Backtest, INDUSTRY_CLEAN
granularity (~202 raw buckets, ~23 eligible/day within the real tradeable
universe -- see industry_granularity_check.py). Ported from
sector_breadth_strategy_v1.py, which used the coarser Sector_clean (11
buckets). Untagged stocks are simply excluded (92% coverage among eligible
tradeable names already, per the coverage check -- not worth a fallback).

Frozen beta re-fit at this granularity: BETA_MOM_DISP = 0.590 (R^2=0.206),
from industry_breadth_ic_test.py's pooled OLS on the IS window. This does
NOT equal the Sector_clean beta (0.531) -- the relationship between breadth
and momentum+dispersion is granularity-specific and was re-estimated, not
carried over.

Position structure (N_SECTORS=4, STOCKS_PER_SECTOR=2, 8 total slots) is
kept IDENTICAL to the Sector_clean version so any performance difference is
attributable to the granularity switch alone, not a confounded parameter
change. (Industry_clean IC diagnostics also validated top-8 sector entries
as a reasonable alternative given ~23 buckets are typically eligible --
worth testing as a robustness variant later, not swapped in here.)

Original module docstring (still applies):
-----------------------------------------------------------------------
Hypothesis (validated in sector_breadth_ic_test.py / industry_breadth_ic_test.py,
IS window 2003-2012): sector-level PARTICIPATION/BREADTH (% of constituents
confirming the trend) carries real predictive information beyond what price-return momentum
already captures. Rather than rank sectors by how much the index has moved
(colleague's sector_factor_strategy v4-v6: 126d momentum + 21d dispersion),
rank them by a breadth composite, then ORTHOGONALIZE it against the
momentum+dispersion factor via a single pooled-OLS residual so a high score
means "breadth says more than momentum already does here" -- not just
"breadth that happens to also have decent momentum" (raw correlation was
+0.42-0.46; the residual is ~0).

Frozen parameter: BETA_MOM_DISP = 0.531, R^2=0.226, fit once by pooled OLS
(breadth ~ mom_disp) over the IS window only in sector_breadth_ic_test.py.
NEVER re-estimated here or on OOS data -- treat as a config constant, same
discipline as any other frozen hyperparameter.

Stock-level factor is deliberately NOT price-return momentum either (that's
CSM's and the colleague's stock-level factor already): rank eligible,
trend-gated stocks within top sectors by TREND PERSISTENCE -- the % of the
last 126 trading days spent above their own SMA200. Same "breadth of
confirmation" idea one level down: consistency of trend, not magnitude.

Universe / sector construction / stop mechanics / benchmark-regime gate all
intentionally mirror sector_factor_strategy_v6.py's proven plumbing --
that's data-hygiene and risk-management infrastructure, not the hypothesis,
so reusing it doesn't reintroduce the correlated-trades problem this
strategy exists to avoid.

Scope: this is the FIRST backtest of a brand-new idea -- a performance read,
not a live-readiness claim. STRATEGY_VALIDATION_PLAYBOOK.md's 8 stages are
the gate that comes AFTER a strategy has real backtest numbers to evaluate,
not before.

Backtest window: 2003-01-01 -> 2012-12-31 (in-sample only, per this shop's
IS/OOS convention). Indicators are computed on the full loaded price history
so 200d/252d/126d rolling windows are warm by 2003-01-01; no trade opens
before that date and none after 2012-12-31.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "HR_breakout"))
from hr_breakout_v2 import load_data  # noqa: E402

DATA_FOLDER     = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
INSTRUMENTS_CSV = os.path.join(REPO_ROOT, "instruments_clean.csv")
SYMBOL_COL      = "trading_symbol"
SECTOR_COL      = "Industry_clean"
OUT_DIR         = os.path.dirname(__file__)

BACKTEST_START = pd.Timestamp("2003-01-01")
BACKTEST_END   = pd.Timestamp("2012-12-31")

# ══════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════

MIN_STOCKS_SECTOR = 8
UNIVERSE_TOP_N     = 1000
MIN_PRICE          = 10.0
MAX_CIRCUIT_DAYS   = 5
CA_DROP_THRESH     = 0.40
CA_GAIN_THRESH     = 3.00

# Sector ranking (breadth-divergence)
SMA_SLOW_WIN       = 200
HI_LO_WIN          = 252
HI_LO_MIN_PERIODS  = 200
NET_HI_LO_SMOOTH   = 21
SECTOR_MOM_PERIOD  = 126
DISPERSION_WINDOW  = 21
BETA_MOM_DISP      = 0.590     # FROZEN (Industry_clean fit) -- see module docstring, do not re-fit
RANK_SMOOTH_WINDOW = 10        # 10d rolling mean on div_resid before ranking -- churn-reduction fix,
                                # same shape as colleague's v4->v5 change (see build_sector_rank docstring)

N_SECTORS          = 4
N_SECTORS_EXIT     = 5

# Stock selection (trend persistence)
SMA_FAST           = 50
TREND_PERSIST_WIN  = 126
STOCKS_PER_SECTOR      = 2
STOCKS_PER_SECTOR_EXIT = 4
MAX_POSITIONS      = N_SECTORS * STOCKS_PER_SECTOR

# Regime
BENCH_SMA_PERIOD   = 50
BENCH_STREAK_MAX   = 5

# Sizing / rebalance
REBALANCE_EVERY    = 5         # trading days (~weekly)

# Stops
ATR_PERIOD         = 14
ATR_MULTIPLIER     = 2.5
STOP_LOSS_PCT      = 0.15

WARMUP_DAYS        = 280       # covers 252d hi/lo + 21d thrust smoothing


# ══════════════════════════════════════════════════════════════════════════
# UNIVERSE / SECTOR CONSTRUCTION  (proven plumbing, reused as-is)
# ══════════════════════════════════════════════════════════════════════════

def build_sector_membership(prices, instruments_csv, min_stocks=MIN_STOCKS_SECTOR):
    inst = pd.read_csv(instruments_csv).dropna(subset=[SYMBOL_COL, SECTOR_COL])
    ticker_sector = dict(zip(inst[SYMBOL_COL], inst[SECTOR_COL]))
    members = {}
    for ticker, sector in ticker_sector.items():
        if ticker in prices.columns:
            members.setdefault(sector, []).append(ticker)
    members = {s: m for s, m in members.items() if len(m) >= min_stocks}
    print(f"[industry_breadth_v1] {len(members)} sectors qualify: {sorted(members.keys())}")
    return members


def build_universe_mask(prices, volumes, highs, lows):
    prev_close = prices.shift(1)
    price_ok = prev_close >= MIN_PRICE
    dvol = (prices * volumes).rolling(63, min_periods=21).mean().shift(1)
    dvol_rank = dvol.rank(axis=1, ascending=False, method="min")
    dvol_ok = dvol_rank <= UNIVERSE_TOP_N
    if not highs.empty and not lows.empty:
        circuit_count = (highs == lows).rolling(63, min_periods=1).sum().shift(1)
        circuit_ok = circuit_count <= MAX_CIRCUIT_DAYS
    else:
        circuit_ok = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    return (price_ok & dvol_ok & circuit_ok).fillna(False)


def build_sector_index(prices, members):
    daily_ret = prices.pct_change(fill_method=None)
    bad_tick = (daily_ret < -CA_DROP_THRESH) | (daily_ret > CA_GAIN_THRESH)
    daily_ret = daily_ret.where(~bad_tick)
    sector_ret = pd.DataFrame({s: daily_ret[m].mean(axis=1, skipna=True) for s, m in members.items()})
    sector_price = (1 + sector_ret.fillna(0)).cumprod()
    return sector_price, daily_ret


# ══════════════════════════════════════════════════════════════════════════
# SECTOR FACTOR: BREADTH-DIVERGENCE  (the hypothesis)
# ══════════════════════════════════════════════════════════════════════════

def build_breadth_composite(prices, members, universe_mask):
    sma200 = prices.rolling(SMA_SLOW_WIN, min_periods=150).mean()
    above_200 = (prices > sma200)
    roll_hi = prices.rolling(HI_LO_WIN, min_periods=HI_LO_MIN_PERIODS).max()
    roll_lo = prices.rolling(HI_LO_WIN, min_periods=HI_LO_MIN_PERIODS).min()
    new_hi = (prices >= roll_hi)
    new_lo = (prices <= roll_lo)

    b1_dict, b2_dict, n_dict = {}, {}, {}
    for sector, tickers in members.items():
        tickers = [t for t in tickers if t in prices.columns]
        elig = universe_mask[tickers]
        n_elig = elig.sum(axis=1).replace(0, np.nan)
        n_dict[sector] = n_elig

        above_200_elig = above_200[tickers].where(elig)
        b1_dict[sector] = above_200_elig.sum(axis=1) / n_elig

        net_hi_lo = (new_hi[tickers].astype(float) - new_lo[tickers].astype(float)).where(elig)
        net_hi_lo_frac = net_hi_lo.sum(axis=1) / n_elig
        b2_dict[sector] = (net_hi_lo_frac.rolling(NET_HI_LO_SMOOTH, min_periods=NET_HI_LO_SMOOTH).sum()
                            / NET_HI_LO_SMOOTH)

    B1 = pd.DataFrame(b1_dict)
    B2 = pd.DataFrame(b2_dict)
    n_elig_df = pd.DataFrame(n_dict)
    valid = n_elig_df >= MIN_STOCKS_SECTOR
    B1, B2 = B1.where(valid), B2.where(valid)

    breadth = (B1.rank(axis=1, pct=True) + B2.rank(axis=1, pct=True)) / 2.0
    return breadth


def build_mom_disp_composite(sector_price, daily_ret, members):
    mom = sector_price.pct_change(SECTOR_MOM_PERIOD, fill_method=None)
    daily_dispersion = pd.DataFrame(
        {s: daily_ret[m].std(axis=1, skipna=True) for s, m in members.items()}
    )
    dispersion = daily_dispersion.rolling(DISPERSION_WINDOW).mean()
    return (mom.rank(axis=1, pct=True) + dispersion.rank(axis=1, pct=True)) / 2.0


def build_sector_rank(prices, members, universe_mask, sector_price, daily_ret):
    """
    div_resid = breadth - BETA_MOM_DISP * mom_disp (frozen beta), then
    10d-smoothed before ranking -- same fix colleague's v4->v5 applied to
    their raw composite (churn was the problem there too). Not independently
    IC-re-tested at this granularity; the backtest itself (real forward P&L)
    is the direct test of whether cutting churn helps, which is what this
    change targets: SECTOR_RANK_DECLINE exits were 372 vs Sector_clean's 240,
    and weekly sector-set churn was 37.8% of slots vs 27.7%.
    """
    breadth = build_breadth_composite(prices, members, universe_mask)
    mom_disp = build_mom_disp_composite(sector_price, daily_ret, members)
    sector_rank_raw = breadth - BETA_MOM_DISP * mom_disp
    sector_rank = sector_rank_raw.rolling(RANK_SMOOTH_WINDOW, min_periods=RANK_SMOOTH_WINDOW).mean()
    return sector_rank, breadth, mom_disp


# ══════════════════════════════════════════════════════════════════════════
# STOCK FACTOR: TREND PERSISTENCE
# ══════════════════════════════════════════════════════════════════════════

def build_stock_factors(prices):
    sma_fast = prices.rolling(SMA_FAST, min_periods=SMA_FAST).mean()
    sma_slow = prices.rolling(SMA_SLOW_WIN, min_periods=150).mean()
    trend_ok = (prices > sma_fast) & (prices > sma_slow)

    above_slow = (prices > sma_slow).astype(float)
    persistence = above_slow.rolling(TREND_PERSIST_WIN, min_periods=TREND_PERSIST_WIN).mean()

    return sma_slow, trend_ok, persistence


def build_atr(prices, highs, lows):
    highs_ff = highs.ffill() if not highs.empty else prices
    lows_ff = lows.ffill() if not lows.empty else prices
    prev_close = prices.shift(1)
    tr = (highs_ff - lows_ff).abs()
    tr = tr.combine((highs_ff - prev_close).abs(), np.maximum)
    tr = tr.combine((lows_ff - prev_close).abs(), np.maximum)
    return tr.rolling(ATR_PERIOD, min_periods=ATR_PERIOD).mean()


# ══════════════════════════════════════════════════════════════════════════
# REGIME (benchmark = equal-weight across all qualifying sector indices)
# ══════════════════════════════════════════════════════════════════════════

def compute_regime(sector_price):
    bench = sector_price.mean(axis=1, skipna=True)
    bench_sma = bench.rolling(BENCH_SMA_PERIOD, min_periods=30).mean()
    below = (bench < bench_sma).shift(1).fillna(False).astype(int)
    streak = below.rolling(BENCH_STREAK_MAX, min_periods=BENCH_STREAK_MAX).sum()
    bench_ok = (streak < BENCH_STREAK_MAX).fillna(True)
    return bench_ok.reindex(sector_price.index).fillna(True)


# ══════════════════════════════════════════════════════════════════════════
# EVENT-DRIVEN POSITION GENERATION + TRADE LOG
# ══════════════════════════════════════════════════════════════════════════

def rank_sector_stocks(idx, sector, members, persistence, universe_mask, trend_ok):
    tickers = members[sector]
    elig_row = universe_mask.iloc[idx]
    trend_row = trend_ok.iloc[idx]
    rank_row = persistence.iloc[idx]
    pool = [t for t in tickers
            if elig_row.get(t, False) and trend_row.get(t, False) and pd.notna(rank_row.get(t, np.nan))]
    pool.sort(key=lambda t: rank_row[t], reverse=True)
    return pool


def run_backtest(prices, opens, sector_rank, members, universe_mask,
                  sma_slow, trend_ok, persistence, bench_ok, atr):
    dates = prices.index
    n = len(dates)
    all_stocks = list(prices.columns)
    opens_ff = opens.ffill() if not opens.empty else prices.shift(1)
    open_proxy = prices.shift(1)

    start_i = dates.searchsorted(BACKTEST_START)
    end_i = dates.searchsorted(BACKTEST_END, side="right")

    position_list = []
    active = {}     # ticker -> {entry_date, entry_price, peak_price, sector}
    trade_log = []

    for i in range(start_i, end_i):
        date = dates[i]
        idx = i - 1
        to_exit = {}

        # ── Daily: fixed stop + ATR trailing stop ──
        for ticker, h in active.items():
            prev_close = prices.iloc[idx].get(ticker, np.nan)
            if pd.isna(prev_close):
                continue
            h["min_price"] = min(h.get("min_price", h["entry_price"]), prev_close)
            h["peak_price"] = max(h.get("peak_price", h["entry_price"]), prev_close)
            h["max_price"] = h["peak_price"]

            fixed_stop = h["entry_price"] * (1.0 - STOP_LOSS_PCT)
            atr_val = atr.iloc[idx].get(ticker, np.nan)
            atr_stop = (h["peak_price"] - ATR_MULTIPLIER * atr_val
                        if pd.notna(atr_val) and atr_val > 0 else -np.inf)
            effective_stop = max(fixed_stop, atr_stop)

            if prev_close <= effective_stop:
                to_exit[ticker] = "ATR_STOP" if atr_stop >= fixed_stop else "STOP_LOSS"

        is_rebalance_day = ((i - start_i) % REBALANCE_EVERY == 0)
        if is_rebalance_day:
            sector_row = sector_rank.iloc[idx].dropna().sort_values(ascending=False)
            top_sectors_exit = list(sector_row.index[:N_SECTORS_EXIT])

            # Sector rank decline
            for ticker, h in active.items():
                if ticker in to_exit:
                    continue
                if h["sector"] not in top_sectors_exit:
                    to_exit[ticker] = "SECTOR_RANK_DECLINE"

            # Stock rank decline within still-qualifying sector
            for ticker, h in active.items():
                if ticker in to_exit:
                    continue
                sector = h["sector"]
                pool = rank_sector_stocks(idx, sector, members, persistence, universe_mask, trend_ok)
                if ticker not in pool[:STOCKS_PER_SECTOR_EXIT]:
                    to_exit[ticker] = "STOCK_RANK_DECLINE"

        # ── Execute exits at T+1 open ──
        for ticker, reason in to_exit.items():
            h = active.pop(ticker)
            exit_open = float(opens_ff.at[date, ticker]) if ticker in opens_ff.columns else np.nan
            if pd.isna(exit_open) or exit_open <= 0:
                exit_open = float(open_proxy.at[date, ticker]) if ticker in open_proxy.columns else np.nan
            exit_close = float(prices.at[date, ticker]) if ticker in prices.columns else np.nan
            trade_log.append({
                "Ticker": ticker, "Sector": h["sector"],
                "Entry_Date": h["entry_date"], "Entry_Price": round(h["entry_price"], 4),
                "Exit_Date": date, "Exit_Price": round(exit_open, 4) if pd.notna(exit_open) else np.nan,
                "Close_At_Exit": round(exit_close, 4) if pd.notna(exit_close) else np.nan,
                "Exit_Reason": reason,
                "MAE_Pct": round((h["min_price"] / h["entry_price"] - 1) * 100, 2),
                "MFE_Pct": round((h["max_price"] / h["entry_price"] - 1) * 100, 2),
            })

        # ── New entries: only on rebalance days, only if regime OK ──
        if is_rebalance_day and i >= WARMUP_DAYS and bool(bench_ok.iloc[idx]):
            sector_row = sector_rank.iloc[idx].dropna().sort_values(ascending=False)
            top_sectors_entry = list(sector_row.index[:N_SECTORS])

            for sector in top_sectors_entry:
                if sector not in members:
                    continue
                slots = MAX_POSITIONS - len(active)
                if slots <= 0:
                    break
                pool = rank_sector_stocks(idx, sector, members, persistence, universe_mask, trend_ok)
                sector_held = [t for t, h in active.items() if h["sector"] == sector]
                free_in_sector = STOCKS_PER_SECTOR - len(sector_held)
                candidates = [t for t in pool[:STOCKS_PER_SECTOR] if t not in active][:max(0, free_in_sector)]
                for ticker in candidates:
                    if len(active) >= MAX_POSITIONS:
                        break
                    entry_px = float(opens_ff.at[date, ticker]) if ticker in opens_ff.columns else np.nan
                    if pd.isna(entry_px) or entry_px <= 0:
                        entry_px = float(open_proxy.at[date, ticker]) if ticker in open_proxy.columns else np.nan
                    if pd.isna(entry_px) or entry_px <= 0:
                        continue
                    active[ticker] = {
                        "entry_date": date, "entry_price": entry_px,
                        "peak_price": entry_px, "min_price": entry_px, "max_price": entry_px,
                        "sector": sector,
                    }

        weight_per_slot = 1.0 / MAX_POSITIONS
        curr_weights = pd.Series({t: weight_per_slot for t in active},
                                  dtype=float).reindex(all_stocks, fill_value=0.0)
        curr_weights.name = date
        position_list.append(curr_weights)

    # ── Close remaining positions at end of data ──
    last_date = dates[end_i - 1]
    for ticker, h in list(active.items()):
        exit_close = float(prices.at[last_date, ticker]) if ticker in prices.columns else np.nan
        trade_log.append({
            "Ticker": ticker, "Sector": h["sector"],
            "Entry_Date": h["entry_date"], "Entry_Price": round(h["entry_price"], 4),
            "Exit_Date": last_date, "Exit_Price": round(exit_close, 4) if pd.notna(exit_close) else np.nan,
            "Close_At_Exit": round(exit_close, 4) if pd.notna(exit_close) else np.nan,
            "Exit_Reason": "END_OF_DATA",
            "MAE_Pct": round((h["min_price"] / h["entry_price"] - 1) * 100, 2),
            "MFE_Pct": round((h["max_price"] / h["entry_price"] - 1) * 100, 2),
        })

    positions_df = pd.DataFrame(position_list, index=dates[start_i:end_i]).fillna(0.0)
    trade_log_df = pd.DataFrame(trade_log)
    return positions_df, trade_log_df


# ══════════════════════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════════════════════

def compute_portfolio_returns(positions_df, prices):
    stock_ret = prices.pct_change(fill_method=None).reindex(positions_df.index)
    port_ret = (positions_df.shift(1) * stock_ret).sum(axis=1)
    return port_ret.fillna(0.0)


def compute_metrics(port_ret, rfr_annual=0.0):
    equity = (1 + port_ret).cumprod()
    n_years = len(port_ret) / 252.0
    cagr = equity.iloc[-1] ** (1 / n_years) - 1 if n_years > 0 else np.nan

    ann_ret = port_ret.mean() * 252
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = (ann_ret - rfr_annual) / ann_vol if ann_vol > 0 else np.nan

    running_max = equity.cummax()
    drawdown = equity / running_max - 1.0
    max_dd = drawdown.min()
    calmar = cagr / abs(max_dd) if max_dd < 0 else np.nan

    win_days = (port_ret > 0).sum()
    total_days = (port_ret != 0).sum()
    win_rate = win_days / total_days if total_days > 0 else np.nan

    return dict(CAGR=cagr, Sharpe=sharpe, Calmar=calmar, MaxDD=max_dd,
                AnnVol=ann_vol, WinRateDaily=win_rate), equity, drawdown


def yearly_breakdown(port_ret):
    yearly = port_ret.groupby(port_ret.index.year).apply(lambda r: (1 + r).prod() - 1)
    return yearly


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("Loading OHLCV data...")
    prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)

    members = build_sector_membership(prices, INSTRUMENTS_CSV)
    universe_mask = build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = build_sector_rank(prices, members, universe_mask,
                                                        sector_price, daily_ret)
    sma_slow, trend_ok, persistence = build_stock_factors(prices)
    atr = build_atr(prices, highs, lows)
    bench_ok = compute_regime(sector_price)

    print(f"\nRunning backtest {BACKTEST_START.date()} -> {BACKTEST_END.date()} "
          f"(IN-SAMPLE ONLY)...")
    positions_df, trade_log_df = run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr)

    port_ret = compute_portfolio_returns(positions_df, prices)
    metrics, equity, drawdown = compute_metrics(port_ret)
    yearly = yearly_breakdown(port_ret)

    print(f"\n{'='*70}\nPERFORMANCE  (2003-2012 IN-SAMPLE)\n{'='*70}")
    for k, v in metrics.items():
        if k in ("CAGR", "MaxDD", "AnnVol", "WinRateDaily"):
            print(f"  {k:15s}: {v*100:+.2f}%")
        else:
            print(f"  {k:15s}: {v:.3f}")

    print(f"\n  Total trades: {len(trade_log_df)}")
    if not trade_log_df.empty:
        print(f"\n  Exit reason breakdown:")
        print(trade_log_df["Exit_Reason"].value_counts().to_string())
        print(f"\n  Avg MAE/MFE by exit reason:")
        print(trade_log_df.groupby("Exit_Reason")[["MAE_Pct", "MFE_Pct"]].mean().round(2).to_string())

    print(f"\n  Yearly returns:")
    for yr, ret in yearly.items():
        print(f"    {yr}: {ret*100:+.2f}%")

    # ── Save outputs ──
    trade_log_df.to_csv(os.path.join(OUT_DIR, "industry_breadth_trades_v1.csv"), index=False)
    pd.DataFrame([metrics]).to_csv(os.path.join(OUT_DIR, "industry_breadth_results_v1.csv"), index=False)
    yearly.to_csv(os.path.join(OUT_DIR, "industry_breadth_yearly_v1.csv"))

    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    ax[0].plot(equity.index, equity.values)
    ax[0].set_title("Sector Breadth-Divergence v1 -- Equity Curve (IS 2003-2012)")
    ax[0].set_yscale("log")
    ax[1].fill_between(drawdown.index, drawdown.values * 100, 0, color="red", alpha=0.4)
    ax[1].set_title("Drawdown (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "industry_breadth_equity_v1.png"), dpi=100)
    print(f"\nSaved trade log, results, yearly breakdown, and equity plot to {OUT_DIR}")


if __name__ == "__main__":
    main()
