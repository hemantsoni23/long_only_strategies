"""
pead_fundamentals.py -- point-in-time earnings events for the PEAD strategy.

Source : NSE XBRL quarterly results (`facts_quarterly.parquet` from upstox_data_folder/pit_harness/cache; columns symbol, basis, period_end, filed_date, eps, net_profit,
         revenue, ebit ...).  A result is usable only from its `filed_date`.
Output : one row per (symbol, period_end) with the signals known on the filing date:
           sue_eps   (EPS_q - EPS_q-4) / std(previous 4-8 seasonal EPS differences)      -- standardised unexpected earnings (Chan-Jegadeesh-Lakonishok)
           dm_ebit   EBIT margin minus its value 4 quarters earlier
           sg_np     symmetric yoy net-profit growth
Basis rule (causal): for each period use the basis that yields a valid SUE, preferring consolidated when both do. Each basis keeps its own history (a company that starts
consolidated reporting uses standalone SUE until the consolidated series has enough quarters).  No count of future quarters is used.
Hygiene: results filed more than 120 days after the period end, or out of order (an older period filed after a newer one), are dropped.
"""
import numpy as np
import pandas as pd

FACTS = '/Users/hemantsoni/Documents/upstox_data_folder/pit_harness/cache/facts_quarterly.parquet'


def _seasonal_surprise(x):
    d4 = x - x.shift(4)
    sd = d4.shift(1).rolling(8, min_periods=4).std()
    return d4 / sd.where(sd > 0)


def _sym_growth(a, b):
    return (a - b) / ((a.abs() + b.abs()) / 2).replace(0, np.nan)


def _features(g):
    g = g.sort_values('period_end').drop_duplicates('period_end', keep='last')
    grid = pd.date_range(g.period_end.min(), g.period_end.max(), freq='QE')
    g = g.set_index('period_end').reindex(grid)
    o = pd.DataFrame(index=g.index)
    o['filed'] = g['filed_date']
    rev = g['revenue'].replace(0, np.nan)
    o['sue_eps'] = _seasonal_surprise(g['eps'])
    o['dm_ebit'] = g['ebit'] / rev - (g['ebit'] / rev).shift(4)
    o['sg_np'] = _sym_growth(g['net_profit'], g['net_profit'].shift(4))
    return o


def build_events(facts=None, path=FACTS, symbols=None):
    f = pd.read_parquet(path) if facts is None else facts
    if symbols is not None:
        f = f[f.symbol.isin(symbols)]
    out = []
    for (sym, basis), g in f.groupby(['symbol', 'basis']):
        o = _features(g)
        o['symbol'] = sym; o['basis'] = basis; o['period_end'] = o.index
        out.append(o.reset_index(drop=True))
    ev = pd.concat(out, ignore_index=True)
    ev = ev[ev.filed.notna() & ((ev.filed - ev.period_end).dt.days.between(0, 120))]
    ev['pref'] = (ev.basis == 'consolidated').astype(int)
    ev['has_sue'] = ev.sue_eps.notna().astype(int)
    ev = (ev.sort_values(['symbol', 'period_end', 'has_sue', 'pref']).drop_duplicates(['symbol', 'period_end'], keep='last'))
    ev = ev.sort_values(['symbol', 'filed'])
    ev = ev[ev.period_end >= ev.groupby('symbol').period_end.cummax()]            # drop out-of-order late filings
    return ev.drop(columns=['pref', 'has_sue']).sort_values('filed').reset_index(drop=True)
