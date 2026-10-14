"""
sector_factor_strategy_v4.py
==============================
Basic Sector-Factor Strategy — Event-Driven Backtest (v4)

Copy of sector_factor_strategy_v3.py with ONE change: sector ranking is
swapped from plain 126-day sector momentum to an equal-weight percentile-
rank composite of Mom_126 + Dispersion_21 (21d-average cross-sectional
return dispersion within the sector). Driven by
sector_factor_library_ic_test.py (14-factor sector-level IC library) and
sector_factor_correlation_test.py (pairwise redundancy check): Dispersion_21
had the lowest correlation with Mom_126 of any strong factor tested (0.28,
vs 0.69 for Avg_Constituent_RS_126 and 0.53 for Breadth_SMA200, both of
which turned out to be largely re-detecting momentum), and the Mom_126 +
Dispersion_21 composite's ICIR beat BOTH individual components at the 63d
and 126d horizons (e.g. 126d: composite 0.589 vs Mom_126 alone 0.573 vs
Dispersion_21 alone 0.465) -- genuine complementary information, not
redundant averaging. Stock rank, universe, regime, entry modes, exits,
and sizing are all unchanged from v3.

Also adds START_DATE / END_DATE so the strategy can be backtested over a
specific window without losing indicator warmup: factors are always
computed on the FULL loaded price history, and only the positions/prices
fed into compute_performance() are sliced to the requested window -- so
a rolling SMA200 or 252d high near the start of the window still has its
correct lookback, and the reported equity curve/metrics reflect only the
requested period.

Universe : top-N dVol (63d avg) | min price ₹10 | circuit ≤5/63d
Regime   : benchmark (equal-weight universe) above its own SMA200
Sectors  : equal-weight index per Sector_clean tag | ranked by an equal-
           weight percentile blend of 126d return and 21d-avg return
           dispersion | take top N_SECTORS
Stocks   : within top sectors, rank members by RANK_SMOOTH_WINDOW-day
           rolling average of proximity to 52w high (close / 252d high)
           | require Price > SMA50 > SMA200 | take top STOCKS_PER_SECTOR
Entry    : trend gate always required, plus one of four configurable modes
           (trend_only / breakout / momentum / breakout_momentum) -- all
           four are run and compared in one pass
Exits    : sector rank decline | stock rank decline (checked weekly)
           trend failure (close < SMA200) | fixed stop loss (checked daily)
Sizing   : equal weight, 1 / max_positions
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hr_breakout_v2 import load_data


# ══════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════

DATA_FOLDER     = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
SCRIPT_DIR      = os.path.dirname(__file__)
INSTRUMENTS_CSV = os.path.join(SCRIPT_DIR, "..", "..", "instruments_clean.csv")
SYMBOL_COL      = "trading_symbol"
SECTOR_COL      = "Sector_clean"

# Backtest reporting window -- factors still use the FULL loaded history for
# lookback (see module docstring); these only slice what gets reported.
# Format "YYYY-MM-DD", or None for open-ended (full available history).
START_DATE = "2015-01-01"
END_DATE   = "2025-12-31"

MIN_STOCKS_SECTOR = 8          # min constituents for a sector to qualify for index construction
UNIVERSE_TOP_N     = 1000        # top-N tradeable stocks by 63d avg dollar volume
MIN_PRICE          = 10.0
MAX_CIRCUIT_DAYS   = 5
CA_DROP_THRESH     = 0.40       # single-day drop >40% -> bad tick, excluded from return calcs
CA_GAIN_THRESH     = 3.00       # single-day gain >300% -> bad tick, excluded from return calcs

N_SECTORS          = 3
STOCKS_PER_SECTOR  = 2
MAX_POSITIONS       = N_SECTORS * STOCKS_PER_SECTOR
REBALANCE_EVERY     = 5         # trading days (~weekly) for rank-decline checks + new entries
STOP_LOSS_PCT       = 0.12
SMA_FAST            = 50
SMA_SLOW            = 200
SECTOR_MOM_PERIOD   = 126
DISPERSION_WINDOW   = 21        # rolling window for cross-sectional return dispersion (sector rank component)
BENCH_SMA_PERIOD    = 50        # regime SMA period (HR/VCP convention, distinct from stock-level SMA_SLOW)
BENCH_STREAK_MAX    = 5         # block new entries only if benchmark stayed below its SMA for ALL of the last N days
HIGH_52W_PERIOD      = 252      # stock rank factor: proximity to N-day high
HIGH_52W_MIN_PERIODS = 200
RANK_SMOOTH_WINDOW   = 10       # rolling mean on the rank factor to reduce rank churn
BREAKOUT_WINDOW     = 20
MOM_WINDOW          = 20
WARMUP_DAYS         = 260

ENTRY_MODES = ["momentum"]


# ══════════════════════════════════════════════════════════════════════════
# SECTOR / UNIVERSE CONSTRUCTION
# ══════════════════════════════════════════════════════════════════════════

def build_sector_membership(prices, instruments_csv, symbol_col=SYMBOL_COL,
                             sector_col=SECTOR_COL, min_stocks=MIN_STOCKS_SECTOR):
    inst = pd.read_csv(instruments_csv).dropna(subset=[symbol_col, sector_col])
    ticker_sector = dict(zip(inst[symbol_col], inst[sector_col]))

    members = {}
    for ticker, sector in ticker_sector.items():
        if ticker in prices.columns:
            members.setdefault(sector, []).append(ticker)
    members = {s: m for s, m in members.items() if len(m) >= min_stocks}

    stock_sector = {t: s for s, ts in members.items() for t in ts}
    print(f"[sector_factor] {len(members)} sectors qualify (>= {min_stocks} stocks), "
          f"{len(stock_sector)} stocks tagged.")
    return members, stock_sector


def build_sector_index(prices, members):
    """Equal-weight sector index, CA-guarded so one bad tick can't corrupt the index.
    Also returns the guarded daily returns -- reused by build_sector_rank_composite()
    for the dispersion component, so both stay consistent with the same bad-tick mask.
    """
    daily_ret = prices.pct_change(fill_method=None)
    bad_tick = (daily_ret < -CA_DROP_THRESH) | (daily_ret > CA_GAIN_THRESH)
    daily_ret = daily_ret.where(~bad_tick)

    sector_ret = pd.DataFrame({s: daily_ret[m].mean(axis=1, skipna=True) for s, m in members.items()})
    sector_price = (1 + sector_ret.fillna(0)).cumprod()
    return sector_price, daily_ret


def build_sector_rank_composite(sector_price, daily_ret, members):
    """Equal-weight percentile-rank blend of 126d sector momentum and 21d-average
    cross-sectional return dispersion -- validated by sector_factor_library_ic_test.py
    + sector_factor_correlation_test.py (see module docstring for the numbers).
    """
    mom126 = sector_price.pct_change(SECTOR_MOM_PERIOD, fill_method=None)

    daily_dispersion = pd.DataFrame(
        {s: daily_ret[m].std(axis=1, skipna=True) for s, m in members.items()}
    )
    dispersion = daily_dispersion.rolling(DISPERSION_WINDOW).mean()

    composite = (mom126.rank(axis=1, pct=True) + dispersion.rank(axis=1, pct=True)) / 2.0
    return composite


def build_universe_mask(prices, volumes, highs, lows):
    prev_close = prices.shift(1)
    price_ok   = prev_close >= MIN_PRICE

    dvol      = (prices * volumes).rolling(63, min_periods=21).mean().shift(1)
    dvol_rank = dvol.rank(axis=1, ascending=False, method="min")
    dvol_ok   = dvol_rank <= UNIVERSE_TOP_N

    if not highs.empty and not lows.empty:
        circuit_count = (highs == lows).rolling(63, min_periods=1).sum().shift(1)
        circuit_ok = circuit_count <= MAX_CIRCUIT_DAYS
    else:
        circuit_ok = pd.DataFrame(True, index=prices.index, columns=prices.columns)

    return (price_ok & dvol_ok & circuit_ok).fillna(False)


# ══════════════════════════════════════════════════════════════════════════
# STOCK-LEVEL FACTORS
# ══════════════════════════════════════════════════════════════════════════

def build_stock_factors(prices):
    sma_fast = prices.rolling(SMA_FAST, min_periods=SMA_FAST).mean()
    sma_slow = prices.rolling(SMA_SLOW, min_periods=SMA_SLOW).mean()
    trend_ok = (prices > sma_fast) & (sma_fast > sma_slow)

    # Stock rank factor: proximity to 52w high, not own momentum -- validated
    # stronger within top-ranked sectors by stock_signal_ic_test.py. v3 adds a
    # rolling mean (v2 used the raw daily ratio, which churned the weekly
    # top-2 ranking too much -- see module docstring).
    hi_52w = prices.rolling(HIGH_52W_PERIOD, min_periods=HIGH_52W_MIN_PERIODS).max()
    rank_factor_raw = prices / hi_52w.replace(0, np.nan)
    rank_factor = rank_factor_raw.rolling(RANK_SMOOTH_WINDOW, min_periods=1).mean()

    breakout_hi = prices.shift(1).rolling(BREAKOUT_WINDOW).max()
    breakout_signal = prices > breakout_hi

    mom_signal = prices.pct_change(MOM_WINDOW, fill_method=None) > 0

    return sma_slow, trend_ok, rank_factor, breakout_signal, mom_signal


# ══════════════════════════════════════════════════════════════════════════
# EVENT-DRIVEN POSITION GENERATION
# ══════════════════════════════════════════════════════════════════════════

def rank_sector_stocks(idx, sector, members, rank_factor, universe_mask, trend_ok):
    tickers  = members[sector]
    elig_row = universe_mask.iloc[idx]
    trend_row = trend_ok.iloc[idx]
    rank_row = rank_factor.iloc[idx]

    pool = [t for t in tickers
            if elig_row.get(t, False) and trend_row.get(t, False) and pd.notna(rank_row.get(t, np.nan))]
    pool.sort(key=lambda t: rank_row[t], reverse=True)
    return pool


def get_positions(prices, opens, sector_rank, members, universe_mask,
                   sma_slow, trend_ok, rank_factor, breakout_signal, mom_signal,
                   bench_ok, entry_mode):
    dates = prices.index
    n = len(dates)
    all_stocks = list(prices.columns)
    opens_ff = opens.ffill() if not opens.empty else prices.shift(1)
    open_proxy = prices.shift(1)

    position_list = []
    active = {}     # ticker -> {entry_date, entry_price, sector}
    trade_log = []

    for i, date in enumerate(dates):
        if i == 0 or i < WARMUP_DAYS:
            position_list.append(pd.Series(0.0, index=all_stocks, name=date))
            continue

        weight_per_slot = 1.0 / MAX_POSITIONS
        curr_weights = pd.Series({t: weight_per_slot for t in active},
                                  dtype=float).reindex(all_stocks, fill_value=0.0)
        curr_weights.name = date

        idx = i - 1
        to_exit = {}   # ticker -> reason

        # ── Daily checks: stop loss + trend failure ─────────────────────
        for ticker, h in active.items():
            prev_close = prices.iloc[idx].get(ticker, np.nan)
            if pd.isna(prev_close):
                continue
            if prev_close <= h["entry_price"] * (1.0 - STOP_LOSS_PCT):
                to_exit[ticker] = "STOP_LOSS"
                continue
            sma_val = sma_slow.iloc[idx].get(ticker, np.nan)
            # if pd.notna(sma_val) and prev_close < sma_val:
            #     to_exit[ticker] = "TREND_FAILURE"

        # ── Weekly checks: sector / stock rank decline ───────────────────
        is_rebalance_day = (i % REBALANCE_EVERY == 0)
        if is_rebalance_day:
            sector_row = sector_rank.iloc[idx].dropna().sort_values(ascending=False)
            top_sectors = list(sector_row.index[:N_SECTORS])

            for ticker, h in active.items():
                if ticker in to_exit:
                    continue
                sector = h["sector"]
                if sector not in top_sectors:
                    to_exit[ticker] = "SECTOR_RANK_DECLINE"
                    continue
                top_in_sector = rank_sector_stocks(idx, sector, members, rank_factor,
                                                    universe_mask, trend_ok)[:STOCKS_PER_SECTOR]
                if ticker not in top_in_sector:
                    to_exit[ticker] = "STOCK_RANK_DECLINE"

        # ── Apply exits (fill at today's open) ────────────────────────────
        for ticker, reason in to_exit.items():
            h = active.pop(ticker)
            exit_px = opens_ff.iloc[i].get(ticker, np.nan)
            if pd.isna(exit_px) or exit_px <= 0:
                exit_px = open_proxy.iloc[i].get(ticker, np.nan)
            ret_pct = (exit_px / h["entry_price"] - 1.0) * 100 if pd.notna(exit_px) else np.nan
            trade_log.append({
                "Ticker": ticker, "Sector": h["sector"],
                "Entry_Date": h["entry_date"], "Entry_Price": round(h["entry_price"], 4),
                "Exit_Date": date, "Exit_Price": round(exit_px, 4) if pd.notna(exit_px) else np.nan,
                "Exit_Reason": reason,
                "Return_Pct": round(ret_pct, 2) if pd.notna(ret_pct) else np.nan,
                "Holding_Days": (date - h["entry_date"]).days,
            })
            curr_weights[ticker] = 0.0

        # ── New entries (rebalance days only, regime + open slots) ───────
        if is_rebalance_day and bool(bench_ok.iloc[idx]) and len(active) < MAX_POSITIONS:
            sector_row = sector_rank.iloc[idx].dropna().sort_values(ascending=False)
            top_sectors = list(sector_row.index[:N_SECTORS])

            held_by_sector = {}
            for h in active.values():
                held_by_sector[h["sector"]] = held_by_sector.get(h["sector"], 0) + 1

            for sector in top_sectors:
                if len(active) >= MAX_POSITIONS:
                    break
                slots = STOCKS_PER_SECTOR - held_by_sector.get(sector, 0)
                if slots <= 0:
                    continue

                ranked = rank_sector_stocks(idx, sector, members, rank_factor, universe_mask, trend_ok)
                for ticker in ranked:
                    if slots <= 0 or len(active) >= MAX_POSITIONS:
                        break
                    if ticker in active:
                        continue

                    if entry_mode == "breakout" and not breakout_signal.iloc[idx].get(ticker, False):
                        continue
                    if entry_mode == "momentum" and not mom_signal.iloc[idx].get(ticker, False):
                        continue
                    if entry_mode == "breakout_momentum" and not (
                        breakout_signal.iloc[idx].get(ticker, False) and mom_signal.iloc[idx].get(ticker, False)
                    ):
                        continue
                    # trend_only: no extra gate beyond rank_sector_stocks' trend_ok filter

                    entry_px = opens_ff.iloc[i].get(ticker, np.nan)
                    if pd.isna(entry_px) or entry_px <= 0:
                        entry_px = open_proxy.iloc[i].get(ticker, np.nan)
                    if pd.isna(entry_px) or entry_px <= 0:
                        continue

                    active[ticker] = {"entry_date": date, "entry_price": entry_px, "sector": sector}
                    curr_weights[ticker] = weight_per_slot
                    slots -= 1

        position_list.append(curr_weights)

    positions_df = pd.DataFrame(position_list, index=dates).fillna(0.0)
    trades_df = pd.DataFrame(trade_log)
    return positions_df, trades_df


# ══════════════════════════════════════════════════════════════════════════
# PERFORMANCE METRICS
# ══════════════════════════════════════════════════════════════════════════

def compute_yearly_table(equity):
    """Per-calendar-year return and worst drawdown (using the all-time running peak)."""
    drawdown = equity / equity.cummax() - 1.0
    yearly_last = equity.groupby(equity.index.year).last()
    yearly_prev = yearly_last.shift(1)
    yearly_prev.iloc[0] = equity.iloc[0]
    yearly_ret = (yearly_last / yearly_prev - 1.0) * 100
    yearly_dd = drawdown.groupby(drawdown.index.year).min() * 100
    return pd.DataFrame({
        "Year": yearly_last.index,
        "Return_%": yearly_ret.round(2).values,
        "Max_DD_%": yearly_dd.round(2).values,
    })


def compute_avg_drawdown(equity):
    """Average trough of each distinct peak-to-trough drawdown episode."""
    drawdown = equity / equity.cummax() - 1.0
    in_dd = drawdown < 0
    episode_id = (~in_dd).cumsum()
    troughs = drawdown[in_dd].groupby(episode_id[in_dd]).min()
    return round(troughs.mean() * 100, 2) if len(troughs) else 0.0


def compute_performance(positions_df, prices, trades_df):
    daily_ret = prices.pct_change(fill_method=None)
    bad_tick = (daily_ret < -CA_DROP_THRESH) | (daily_ret > CA_GAIN_THRESH)
    daily_ret = daily_ret.where(~bad_tick, 0.0)

    port_ret = (positions_df * daily_ret.reindex(columns=positions_df.columns)).sum(axis=1)
    equity = (1 + port_ret).cumprod()

    n_days = len(equity)
    total_return = equity.iloc[-1] - 1.0
    years = n_days / 252.0
    cagr = equity.iloc[-1] ** (1.0 / years) - 1.0 if years > 0 else np.nan
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = (port_ret.mean() * 252) / ann_vol if ann_vol > 0 else np.nan
    drawdown = equity / equity.cummax() - 1.0
    max_dd = drawdown.min()
    calmar = cagr / abs(max_dd) if max_dd < 0 else np.nan

    if not trades_df.empty:
        rets = trades_df["Return_Pct"].dropna()
        wins  = rets[rets > 0]
        losses = rets[rets <= 0]
        win_rate = len(wins) / len(rets) * 100 if len(rets) else np.nan
        profit_factor = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else np.nan
        avg_trade = rets.mean()
        avg_hold = trades_df["Holding_Days"].mean()
        n_trades = len(trades_df)
    else:
        win_rate = profit_factor = avg_trade = avg_hold = np.nan
        n_trades = 0

    metrics = {
        "Total_Return_%": round(total_return * 100, 2),
        "CAGR_%": round(cagr * 100, 2),
        "Ann_Vol_%": round(ann_vol * 100, 2),
        "Sharpe": round(sharpe, 2) if pd.notna(sharpe) else np.nan,
        "Max_DD_%": round(max_dd * 100, 2),
        "Avg_DD_%": compute_avg_drawdown(equity),
        "Calmar": round(calmar, 2) if pd.notna(calmar) else np.nan,
        "Win_Rate_%": round(win_rate, 2) if pd.notna(win_rate) else np.nan,
        "Profit_Factor": round(profit_factor, 2) if pd.notna(profit_factor) else np.nan,
        "Avg_Trade_%": round(avg_trade, 2) if pd.notna(avg_trade) else np.nan,
        "Avg_Holding_Days": round(avg_hold, 1) if pd.notna(avg_hold) else np.nan,
        "Num_Trades": n_trades,
    }
    yearly_df = compute_yearly_table(equity)
    return metrics, equity, yearly_df


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("Loading price data...")
    prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)
    prices = prices.ffill()

    members, stock_sector = build_sector_membership(prices, INSTRUMENTS_CSV)
    sector_price, daily_ret_masked = build_sector_index(prices, members)
    sector_rank = build_sector_rank_composite(sector_price, daily_ret_masked, members)
    universe_mask = build_universe_mask(prices, volumes, highs, lows)
    sma_slow, trend_ok, rank_factor, breakout_signal, mom_signal = build_stock_factors(prices)

    # Regime gate (HR/VCP convention): block new entries only when the
    # benchmark has been below its SMA for ALL of the last BENCH_STREAK_MAX
    # days -- a single recovery day unblocks entries immediately, unlike a
    # plain "above SMA" check which blocks on any single bad day.
    bench_price = sector_price.mean(axis=1)
    bench_sma = bench_price.rolling(BENCH_SMA_PERIOD, min_periods=30).mean()
    bench_below = (
        (bench_price < bench_sma)
        .shift(1)
        .fillna(False)
        .infer_objects(copy=False)
        .astype(int)
    )
    rolling_sum = bench_below.rolling(BENCH_STREAK_MAX, min_periods=BENCH_STREAK_MAX).sum()
    bench_ok = (rolling_sum < BENCH_STREAK_MAX).fillna(True)
    bench_ok = bench_ok.reindex(bench_price.index).fillna(True)

    metrics_rows = []
    equity_curves = {}
    all_trades = []
    all_yearly = []

    for mode in ENTRY_MODES:
        print(f"\nRunning entry_mode = {mode} ...")
        positions_df, trades_df = get_positions(
            prices, opens, sector_rank, members, universe_mask,
            sma_slow, trend_ok, rank_factor, breakout_signal, mom_signal,
            bench_ok, entry_mode=mode,
        )

        # Slice to the requested reporting window (factors above already used
        # full history for lookback -- this only narrows what gets measured).
        period_prices    = prices.loc[START_DATE:END_DATE]
        period_positions = positions_df.loc[START_DATE:END_DATE]
        if not trades_df.empty:
            start_ts = pd.Timestamp(START_DATE) if START_DATE else prices.index.min()
            end_ts   = pd.Timestamp(END_DATE) if END_DATE else prices.index.max()
            period_trades = trades_df[
                (trades_df["Exit_Date"] >= start_ts) & (trades_df["Exit_Date"] <= end_ts)
            ]
        else:
            period_trades = trades_df

        metrics, equity, yearly_df = compute_performance(period_positions, period_prices, period_trades)
        metrics["Entry_Mode"] = mode
        metrics_rows.append(metrics)
        equity_curves[mode] = equity
        if not period_trades.empty:
            period_trades = period_trades.copy()
            period_trades.insert(0, "Entry_Mode", mode)
            all_trades.append(period_trades)
        yearly_df.insert(0, "Entry_Mode", mode)
        all_yearly.append(yearly_df)
        print(f"  {metrics}")

    cols = ["Entry_Mode", "Total_Return_%", "CAGR_%", "Ann_Vol_%", "Sharpe", "Max_DD_%", "Avg_DD_%",
            "Calmar", "Win_Rate_%", "Profit_Factor", "Avg_Trade_%", "Avg_Holding_Days", "Num_Trades"]
    results_df = pd.DataFrame(metrics_rows)[cols]

    out_csv = os.path.join(SCRIPT_DIR, "sector_factor_results_v4.csv")
    results_df.to_csv(out_csv, index=False)
    print(f"\nSaved results -> {out_csv}\n")
    print(results_df.to_string(index=False))

    if all_trades:
        trades_out = pd.concat(all_trades, ignore_index=True)
        trades_csv = os.path.join(SCRIPT_DIR, "sector_factor_trades_v4.csv")
        trades_out.to_csv(trades_csv, index=False)
        print(f"Saved trades  -> {trades_csv}")

    yearly_out = pd.concat(all_yearly, ignore_index=True)
    yearly_csv = os.path.join(SCRIPT_DIR, "sector_factor_yearly_v4.csv")
    yearly_out.to_csv(yearly_csv, index=False)
    print(f"Saved yearly  -> {yearly_csv}")
    print("\nYearly Return % by Entry Mode:")
    print(yearly_out.pivot(index="Year", columns="Entry_Mode", values="Return_%").to_string())
    print("\nYearly Max DD % by Entry Mode:")
    print(yearly_out.pivot(index="Year", columns="Entry_Mode", values="Max_DD_%").to_string())

    bench_period = bench_price.loc[START_DATE:END_DATE]
    bench_norm = bench_period / bench_period.iloc[0]
    plot_equity_curves(equity_curves, bench_norm,
                        os.path.join(SCRIPT_DIR, "sector_factor_equity_v4.png"))


def plot_equity_curves(equity_curves, bench_norm, out_png):
    fig, ax = plt.subplots(figsize=(11, 6))
    for mode, eq in equity_curves.items():
        ax.plot(eq.index, eq.values, label=mode, linewidth=1.4)
    ax.plot(bench_norm.index, bench_norm.values, label="Sector-avg benchmark",
            color="black", linestyle="--", linewidth=1.0, alpha=0.6)
    ax.set_yscale("log")
    ax.set_ylabel("Equity (log scale)")
    ax.set_title("Sector-Factor Strategy v4 (Mom_126 + Dispersion_21 sector rank) — Equity Curve by Entry Mode")
    ax.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()
    print(f"Saved chart   -> {out_png}")


if __name__ == "__main__":
    main()
