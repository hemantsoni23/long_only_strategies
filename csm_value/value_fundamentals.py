"""
value_fundamentals.py -- point-in-time earnings-yield inputs for the Earnings-Yield strategy.

For every (symbol, period_end) result: filed date, TTM net profit, latest shares outstanding, symmetric yoy growth of the latest quarter's net profit.
A result is usable from its `filed_date`.  Basis rule (causal): for each period use the basis that yields a valid TTM (4 consecutive quarters), preferring consolidated.
Hygiene: results filed > 120 days after period end or out of order are dropped.  `monthly_frame()` maps results onto signal dates (latest filing <= date, expiring after `max_age` days).
"""
import numpy as np
import pandas as pd

FACTS = '/Users/hemantsoni/Documents/upstox_data_folder/pit_harness/cache/facts_quarterly.parquet'


def _feat(g):
    g = g.sort_values('period_end').drop_duplicates('period_end', keep='last')
    grid = pd.date_range(g.period_end.min(), g.period_end.max(), freq='QE')
    g = g.set_index('period_end').reindex(grid)
    npf = g['net_profit']
    o = pd.DataFrame(index=g.index)
    o['filed'] = g['filed_date']
    o['np_ttm'] = npf.rolling(4, min_periods=4).sum()
    o['shares'] = g['shares_out']
    o['sg_np'] = (npf - npf.shift(4)) / ((npf.abs() + npf.shift(4).abs()) / 2).replace(0, np.nan)
    return o


def build_results(path=FACTS, symbols=None):
    f = pd.read_parquet(path)
    if symbols is not None:
        f = f[f.symbol.isin(symbols)]
    out = []
    for (sym, basis), g in f.groupby(['symbol', 'basis']):
        o = _feat(g); o['symbol'] = sym; o['basis'] = basis; o['period_end'] = o.index
        out.append(o.reset_index(drop=True))
    r = pd.concat(out, ignore_index=True)
    r = r[r.filed.notna() & ((r.filed - r.period_end).dt.days.between(0, 120)) & r.np_ttm.notna() & (r.shares > 0)]
    r['pref'] = (r.basis == 'consolidated').astype(int)
    r = r.sort_values(['symbol', 'period_end', 'pref']).drop_duplicates(['symbol', 'period_end'], keep='last')
    r = r.sort_values(['symbol', 'filed'])
    r = r[r.period_end >= r.groupby('symbol').period_end.cummax()]
    return r.drop(columns='pref').reset_index(drop=True)


def monthly_frame(results, col, dates, columns, max_age=140):
    """Wide frame (dates x columns): value of `col` from the latest result filed on/before each date, NaN once older than max_age days."""
    out = {}
    for s, g in results.groupby('symbol'):
        if s not in columns:
            continue
        g = g.sort_values('filed').drop_duplicates('filed', keep='last')
        v = pd.Series(g[col].values, index=pd.DatetimeIndex(g['filed'].values))
        a = pd.Series(g['filed'].values, index=pd.DatetimeIndex(g['filed'].values))
        u = v.index.union(dates)
        vv = v.reindex(u, method='ffill').reindex(dates)
        aa = pd.to_datetime(a.reindex(u, method='ffill').reindex(dates))
        out[s] = vv.where((dates.to_series() - aa).dt.days <= max_age)
    return pd.DataFrame(out, index=dates).reindex(columns=columns)
