"""gold_overlay.py -- redirect the engine's IDLE CASH into gold, as a post-processing step on the live engine's executed weights.

Why post-processing is exact: in _run_backtest_core the stock decisions (stops, Crash Guard, vol/corr scaling, regime leverage) use
only the equity book's own returns -- cash never feeds back. The engine's return line is
        net = gross_eq + cash_w * daily_cash_rate - |dW| * cost,   cash_w = clip(1 - sum(executed_weights), 0)
so replacing `daily_cash_rate` by an idle-cash return (and charging cost on changes in the gold position) is identical to
re-running the loop with a different cash leg.
"""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'gold_sleeve'))
from gold_sleeve_strategy import GoldSleevePV, load_etf_close

ETF_FOLDER = '/Users/hemantsoni/Documents/upstox_data_folder/etf_ohlcv_data'
LIQUID_FUND_ANNUAL = 0.065


def daily_gold(index):
    """gold daily return on the engine's calendar; NaN where it cannot be trusted (missing price, or a return that spans the data gap)."""
    c = load_etf_close(os.path.join(ETF_FOLDER, 'GOLDBEES.csv'))
    r = c.pct_change(fill_method=None)
    span = c.index.to_series().diff().dt.days
    r[span > 5] = np.nan                                     # first observation after a gap: return spans the gap
    r = r.reindex(index)
    return r, c


def pv_fraction(index, close):
    """persistence x vol target exposure from the validated sleeve, applied with a 2-day delay (decide at month-end close, trade next close)."""
    s = GoldSleevePV(close); s.calculate_signals()
    t = s.month_end_exposure.dropna()
    d = pd.Series(np.nan, index=index)
    pos = index.get_indexer(t.index)
    ok = pos >= 0
    d.iloc[pos[ok]] = t.values[ok]
    return d.ffill().shift(2)


def idle_cash_variants(payload, gold_cost=0.0015, neutral_annual=LIQUID_FUND_ANNUAL):
    w = payload['executed_weights']; idx = w.index
    net = payload['net_returns'].reindex(idx)
    cash_rate = payload['daily_cash_rate']
    cash_w = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    eq_part = net - cash_w * cash_rate                       # equity P&L net of stock trading costs (engine's own)
    rg, close = daily_gold(idx)
    gvalid = rg.notna()
    lf = (1 + neutral_annual) ** (1 / 252) - 1               # liquid-fund daily rate
    bear = payload['regime'].reindex(idx).isin(['BEAR', 'PANIC']).astype(float)
    badvol = payload['regime'].reindex(idx).isin(['BEAR', 'PANIC', 'HIGH_VOL']).astype(float)
    pvf = pv_fraction(idx, close).fillna(0.0)
    # neutral gold: same vol/correlation/timing structure, mean return forced to the liquid-fund rate (no free lunch from gold's sample drift)
    drift = (rg[gvalid] - lf).mean()
    rg_neutral = rg - drift

    def build(f, gold_ret, base_cash):
        f = f.where(gvalid, 0.0).clip(0, 1)                  # no gold exposure when gold data are unusable (gap) -> falls back to base cash
        idle_ret = (1 - f) * base_cash + f * gold_ret.fillna(0.0)
        gold_pos = cash_w * f
        cost = gold_pos.diff().abs().fillna(0.0) * gold_cost
        return eq_part + cash_w * idle_ret - cost, gold_pos

    one = pd.Series(1.0, index=idx)
    V = {}
    V['V0 engine default (idle cash at engine rate)'] = (net, pd.Series(0.0, index=idx))
    V['V0b idle cash in liquid fund 6.5% (fair baseline)'] = build(pd.Series(0.0, index=idx), rg, lf)
    V['V1 idle cash -> gold, always'] = build(one, rg, cash_rate)
    V['V2 idle cash -> gold when market weak (BEAR/PANIC)'] = build(bear, rg, cash_rate)
    V['V3 idle cash -> gold when weak (BEAR/PANIC/HIGH_VOL)'] = build(badvol, rg, cash_rate)
    V['V4 idle cash -> gold x persistence-vol exposure'] = build(pvf, rg, cash_rate)
    V['V5 weak market AND persistence-vol (gold only if gold is trending)'] = build(bear * pvf, rg, cash_rate)
    # controls: neutralised gold (same mean as liquid fund). Baseline for these is V0b.
    V['N1 [neutral gold] idle -> gold, always'] = build(one, rg_neutral, lf)
    V['N2 [neutral gold] idle -> gold when weak (BEAR/PANIC)'] = build(bear, rg_neutral, lf)
    V['N4 [neutral gold] idle -> gold x persistence-vol'] = build(pvf, rg_neutral, lf)
    # V2/V3 vs the liquid-fund baseline need the liquid-fund as the non-gold cash too:
    V['W2 weak market -> gold, else liquid fund'] = build(bear, rg, lf)
    V['W1 always gold (rest of idle in liquid fund) = V1 with liquid-fund fallback'] = build(one, rg, lf)
    meta = dict(cash_w=cash_w, gvalid=gvalid, bear=bear, badvol=badvol, pvf=pvf, drift_daily=drift, rg=rg, lf=lf)
    return V, meta
