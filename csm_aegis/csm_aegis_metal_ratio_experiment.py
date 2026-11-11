"""Gold/silver relative-value sleeve experiment — not production strategy code.

This evaluates the ETF sleeve in isolation before it is allowed to affect CSM
Aegis.  It is deliberately a long-only *rotation*, not "arbitrage": a true
gold/silver spread trade needs a simultaneous long/short book, borrow/futures
financing, margin, and separate execution assumptions.

Signal:
  z = rolling z-score of log(GOLDBEES / SILVERBEES), measured at a month-end
      close and acted on at the next close.
  z >= +1: hold SILVERBEES (gold rich versus silver); z <= -1: hold GOLDBEES;
  otherwise retain the current metal.  The static ETF unit-price difference
  cancels under the rolling z-score.  All ETF fills use raw close/volume/range
  validation; forward-filled closes are marks only.
"""
import os
import numpy as np
import pandas as pd

from csm_aegis_strategy import CSMAegis, DEFAULT_SECONDARY_ETF_DIR
from csm_aegis_backtest import compute_metrics


METALS = ("GOLDBEES", "SILVERBEES")


def _read_etf(folder, ticker):
    path = os.path.join(folder, f"{ticker}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_csv(path, usecols=["timestamp", "open", "high", "low", "close", "volume"])
    dates = pd.to_datetime(df["timestamp"], errors="raise")
    if getattr(dates.dt, "tz", None) is not None:
        dates = dates.dt.tz_localize(None)  # preserve exchange calendar day; do not UTC-shift it
    df.index = dates.dt.normalize()
    return df.drop(columns="timestamp").apply(pd.to_numeric, errors="coerce").loc[~df.index.duplicated(keep="last")].sort_index()


def _is_fillable(frame, i):
    row = frame.iloc[i]
    return CSMAegis.execution_bar_reason(row.close, row.volume, row.high, row.low, row.close)


def _month_end_mask(index):
    return pd.Series(index, index=index).groupby(index.to_period("M")).transform("max").eq(index).values


def _simulate(frames, mode, lookback=63, z_threshold=1.0, cost=0.003):
    """Run 100%-allocated gold, silver, or scheduled ratio rotation.

    All information at date ``i`` is acted on from date ``i+1``.  A deferred
    switch is retried; the simulator never substitutes a stale close.
    """
    index = frames["GOLDBEES"].index.intersection(frames["SILVERBEES"].index)
    F = {ticker: frames[ticker].reindex(index) for ticker in METALS}
    mark = {ticker: F[ticker].close.ffill() for ticker in METALS}
    log_ratio = np.log(F["GOLDBEES"].close / F["SILVERBEES"].close)
    z = (log_ratio - log_ratio.rolling(lookback, min_periods=lookback).mean()) / log_ratio.rolling(lookback, min_periods=lookback).std()
    month_end = _month_end_mask(index)

    cash, shares, held = 1.0, 0.0, None
    desired, due = "GOLDBEES" if mode == "ratio" else mode.upper(), 0
    rets, held_series, z_series, trades, deferred = np.zeros(len(index)), [], [], [], []

    def sell(i, ticker, reason):
        nonlocal cash, shares, held
        px = F[ticker].close.iat[i]
        gross, fee = shares * px, shares * px * cost
        cash += gross - fee
        trades.append(dict(Date=index[i], Ticker=ticker, Side="SELL", Price=px, Notional=gross, Cost=fee, Reason=reason))
        shares, held = 0.0, None

    def buy(i, ticker, reason):
        nonlocal cash, shares, held
        px = F[ticker].close.iat[i]
        shares = cash / (px * (1 + cost))
        gross, fee = shares * px, shares * px * cost
        cash -= gross + fee
        cash = max(cash, 0.0)
        held = ticker
        trades.append(dict(Date=index[i], Ticker=ticker, Side="BUY", Price=px, Notional=gross, Cost=fee, Reason=reason))

    for i in range(len(index)):
        previous_mark = mark[held].iat[i - 1] if held is not None and i else (mark[held].iat[i] if held is not None else 0.0)
        e0 = cash + shares * previous_mark
        if i >= due:
            if held is None:
                reason = _is_fillable(F[desired], i)
                if reason:
                    deferred.append(dict(Date=index[i], Ticker=desired, Reason=reason, Order_Type="INITIAL_BUY"))
                else:
                    buy(i, desired, "INITIAL_ALLOCATION")
            elif held != desired:
                sell_reason, buy_reason = _is_fillable(F[held], i), _is_fillable(F[desired], i)
                if sell_reason or buy_reason:
                    deferred.append(dict(Date=index[i], Ticker=held if sell_reason else desired, Reason=sell_reason or buy_reason, Order_Type="METAL_ROTATION"))
                else:
                    sell(i, held, "RATIO_ROTATION")
                    buy(i, desired, "RATIO_ROTATION")

        value = cash + (shares * mark[held].iat[i] if held is not None else 0.0)
        rets[i] = value / e0 - 1 if e0 else 0.0
        held_series.append(held or "CASH")
        z_series.append(z.iat[i])

        # Signal after the completed month-end close, execution no sooner than
        # the next session.  The no-trade band prevents ratio whipsaw.
        if mode == "ratio" and month_end[i] and i + 1 < len(index):
            if z.iat[i] >= z_threshold:
                desired, due = "SILVERBEES", i + 1
            elif z.iat[i] <= -z_threshold:
                desired, due = "GOLDBEES", i + 1

    ret = pd.Series(rets, index=index)
    out = compute_metrics(ret, start=index[0])
    out.update(ret=ret, z=pd.Series(z_series, index=index), held=pd.Series(held_series, index=index),
               trades=pd.DataFrame(trades), deferred=pd.DataFrame(deferred), start=index[0], end=index[-1])
    return out


def run_metal_ratio_experiment(etf_data_dir=DEFAULT_SECONDARY_ETF_DIR, lookback=63, z_threshold=1.0, cost=0.003):
    """Return three strictly comparable sleeve results over SILVERBEES history."""
    if not etf_data_dir or not os.path.isdir(etf_data_dir):
        raise FileNotFoundError("Set CSM_AEGIS_ETF_DATA_FOLDER or pass --etf-data-folder.")
    frames = {ticker: _read_etf(etf_data_dir, ticker) for ticker in METALS}
    results = {mode: _simulate(frames, mode, lookback, z_threshold, cost) for mode in ("goldbees", "silverbees", "ratio")}
    rows = []
    for mode, result in results.items():
        rows.append(dict(mode=mode, start=result["start"].date(), end=result["end"].date(), CAGR=result["cagr"], Sharpe=result["sharpe"], MaxDD=result["maxdd"], Calmar=result["calmar"], rotations=max(0, len(result["trades"]) - 1)))
    return results, pd.DataFrame(rows).set_index("mode")
