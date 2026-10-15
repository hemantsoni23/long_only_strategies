"""
residual_momentum_v2_backtest.py
===================================
Backtest engine for ResidualMomentumV2. Reuses the LIVE backtest engine's metrics/reporting
functions unchanged (imported from Old_live_strategies/residual_momentum_backtest.py --
metrics, print_report, print_yearly_performance, get_trade_log, populate_trade_stats,
print_exit_breakdown, compute_yearly_table, print_turnover_attribution, plot_performance are
all identical to the live engine; only the day-loop simulation itself is extended here).

backtest_event_driven(strat, ...) is a drop-in replacement for the live engine's function of
the same name:
  - If strat.cash_sweep_etf is None, it DELEGATES to the live engine's own
    backtest_event_driven() verbatim -- bit-identical results, zero duplicated risk.
  - If strat.cash_sweep_etf is 'GOLDBEES' or 'SILVERBEES', idle cash is swept into that ETF
    instead of earning the flat `rf` the live engine assumes (see
    residual_momentum_v2_strategy.py's docstring and README.md for the full rationale and
    validated results). Every stock-side cash inflow (a sale, a stop-out) immediately buys
    ETF units at that moment's price; every outflow (a purchase) sells ETF units to fund it.
    There is no separate un-invested currency in this mode -- a deliberate simplification
    (real settlement needs a small T+1/T+2 buffer, not modeled).

Data dependency for the sweep modes: ETF OHLCV from
/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data/{GOLDBEES,SILVERBEES}.csv.
GOLDBEES data starts 2007-03-19; SILVERBEES starts 2022-02-07 -- get_positions(start=...)
must not be called with a `start` earlier than the chosen ETF's own data start, or the price
reindex has nothing to forward-fill from. run_residual_momentum_v2.py enforces this.
"""
import os

import numpy as np
import pandas as pd

_STRAT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Old_live_strategies")
import sys
if _STRAT_DIR not in sys.path:
    sys.path.insert(0, _STRAT_DIR)

from residual_momentum_backtest import (                                    # noqa: E402
    backtest_event_driven as _live_backtest_event_driven,
    metrics, print_report, print_yearly_performance, get_trade_log,
    populate_trade_stats, print_exit_breakdown, compute_yearly_table,
    print_turnover_attribution, plot_performance,
)

DATA_DIR = "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data"
ETF_START_DATE = {
    "GOLDBEES": pd.Timestamp("2007-03-19"),
    "SILVERBEES": pd.Timestamp("2022-02-07"),
}


def load_etf_prices(etf_name):
    path = os.path.join(DATA_DIR, f"{etf_name}.csv")
    df = pd.read_csv(path, usecols=["timestamp", "open", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_localize(None).dt.normalize()
    df = df.drop_duplicates("timestamp").set_index("timestamp").sort_index()
    return df["open"], df["close"]


def backtest_event_driven(strat, aum=5e8, fixed_bps=15, impact_k=500, capadv=0.25, slc=10,
                          rf=0.06, breaker_adv_cap=0.05, breaker_cost_bps=75, stagger=False):
    """Drop-in replacement for the live engine's backtest_event_driven(). Requires
    strat.positions already set. Returns (net_returns, turnover) exactly like the live
    engine; when a sweep is active, strat.cash_sweep_frac (the swept ETF's daily fraction
    of total equity) is also stashed on `strat` for inspection, mirroring how the live
    engine stashes strat.turnover_by_adv_tier."""
    etf_name = getattr(strat, "cash_sweep_etf", None)
    if etf_name is None:
        return _live_backtest_event_driven(strat, aum=aum, fixed_bps=fixed_bps, impact_k=impact_k,
                                           capadv=capadv, slc=slc, rf=rf,
                                           breaker_adv_cap=breaker_adv_cap,
                                           breaker_cost_bps=breaker_cost_bps, stagger=stagger)

    etf_open, etf_close = load_etf_prices(etf_name)
    WT = strat.positions
    if WT.index.min() < ETF_START_DATE[etf_name]:
        raise ValueError(
            f"cash_sweep_etf={etf_name!r} needs positions starting no earlier than "
            f"{ETF_START_DATE[etf_name].date()} (that ETF's own data start); got positions "
            f"from {WT.index.min().date()}. Call strat.get_positions(start=...) with a later "
            f"date, or set cash_sweep_etf=None.")

    net, turnover, etf_frac = _simulate_with_sweep(
        strat, WT, aum, fixed_bps, impact_k, capadv, slc, breaker_adv_cap, breaker_cost_bps,
        etf_open, etf_close)
    strat.cash_sweep_frac = etf_frac
    return net, turnover


def _simulate_with_sweep(strat, WT, aum, fixed_bps, impact_k, capadv, slc,
                         breaker_adv_cap, breaker_cost_bps, etf_open, etf_close):
    """Same execution mechanics as the live engine's _simulate() (fills, breaker slicing,
    ADV caps, drift band, ATR exit), with the `cash` float replaced by ETF shares -- see
    this module's docstring. strat.position_metadata (the trade log) is NOT populated by
    this path; use the equity-only backtest_event_driven() (cash_sweep_etf=None) first if
    you need the per-trade log, then this one for the swept equity curve -- both read the
    same strat.positions, so the trade log is identical either way."""
    days, close, opn, tv, atr = strat.days, strat.close, strat.opn, strat.tv, strat.atr
    low, high = strat.low, strat.high
    cff = close.ffill()
    adv = tv.rolling(21, min_periods=10).median()
    pos = days.searchsorted(WT.index, side="right")
    fills = {days[p]: t for t, p in zip(WT.index, pos) if p < len(days)}
    start = min(fills)
    idx = days[days >= start]
    cols = close.columns
    band = strat.drift_band
    brk = strat.breaker
    atrk = strat.atr_k

    etf_o = etf_open.reindex(idx, method="ffill")
    etf_c = etf_close.reindex(idx, method="ffill")
    if etf_o.isna().any() or etf_c.isna().any():
        raise ValueError("ETF price series has gaps over the simulated window after ffill -- "
                         "check ETF_START_DATE / the CSV's own coverage.")

    shares = pd.Series(0.0, cols)
    peak = pd.Series(np.nan, cols)
    pending_exit = pd.Series(0.0, cols)
    etf_sh = float(aum) / float(etf_o.iloc[0])
    eq = pd.Series(index=idx, dtype=float)
    etf_val_series = pd.Series(index=idx, dtype=float)
    tot = 0.0

    for d in idx:
        c = cff.loc[d]
        o = opn.loc[d].where(opn.loc[d] > 0).fillna(c)
        eo, ec = float(etf_o.loc[d]), float(etf_c.loc[d])

        if pending_exit.any():
            max_sell = (breaker_adv_cap * adv.loc[d] / o).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            sell = pending_exit.clip(upper=max_sell)
            sell_val = sell * o
            cost_brk = float((sell_val * breaker_cost_bps / 1e4).sum())
            etf_sh += (float(sell_val.sum()) - cost_brk) / eo
            shares -= sell
            pending_exit = (pending_exit - sell).clip(lower=0.0)

        if d in fills:
            t = fills[d]
            w = WT.loc[t]
            mk = o
            still_pending = pending_exit[pending_exit > 0]
            if len(still_pending):
                px_now = mk.loc[still_pending.index]
                val = still_pending * px_now
                cost_fin = val * breaker_cost_bps / 1e4
                etf_sh += (float(val.sum()) - float(cost_fin.sum())) / eo
                shares.loc[still_pending.index] -= still_pending
                pending_exit.loc[still_pending.index] = 0.0

            pre_reb_shares = shares.copy()
            V = etf_sh * eo + float((shares * mk).sum())
            cur_w = (shares * mk) / V
            tgt = w.copy()
            if band > 0:
                hr = (cur_w > 1e-9) & (tgt > 1e-9) & ((tgt - cur_w).abs() <= band)
                tgt = tgt.where(~hr, cur_w)
            tgt_sh = ((tgt * V) / mk).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            dsh = tgt_sh - shares
            csh = (capadv * adv.loc[t] / mk).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            dsh = dsh.clip(lower=-csh, upper=csh)
            tval = dsh.abs() * mk
            cost = float((tval * (fixed_bps / 1e4
                           + impact_k / 1e4
                           * (tval / adv.loc[t]).replace([np.inf, -np.inf], np.nan).fillna(0.0)
                           / slc)).sum())
            net_buy_value = float((dsh * mk).sum()) + cost
            etf_sh -= net_buy_value / eo
            shares = shares + dsh
            tot += float(tval.sum())

            fresh = dsh[(pre_reb_shares.reindex(dsh.index).fillna(0.0).abs() < 1e-9) & (dsh > 0)]
            fresh_mask = pd.Series(False, index=peak.index)
            if len(fresh):
                fresh_mask.loc[fresh.index] = True
            peak = peak.mask(fresh_mask, mk)
            topped_up = ~fresh_mask & (dsh > 0)
            peak = peak.mask(topped_up & ((mk > peak) | peak.isna()), mk)

        held = shares != 0
        peak = peak.mask(held & ((c > peak) | peak.isna()), c)

        if brk is not None:
            triggered = held & (c < peak * (1 - brk)) & (pending_exit == 0)
            if triggered.any():
                pending_exit += shares.where(triggered, 0.0)
        if atrk is not None:
            ex = held & (c < peak - atrk * atr.loc[d])
            if ex.any():
                liq = float((shares * c)[ex].sum())
                etf_sh += (liq - abs(liq) * (fixed_bps / 1e4)) / ec
                shares = shares.mask(ex, 0.0)

        etf_val = etf_sh * ec
        eq.loc[d] = etf_val + float((shares * c).sum())
        etf_val_series.loc[d] = etf_val

    net = eq.pct_change().dropna()
    etf_frac = (etf_val_series / eq).reindex(net.index)
    yrs = len(net) / strat.trading_days
    turnover = tot / eq.mean() / yrs
    return net, turnover, etf_frac
