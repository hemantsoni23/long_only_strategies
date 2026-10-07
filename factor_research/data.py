"""
data.py -- load the Upstox OHLCV universe into aligned daily panels and cache them.

Cleaning mirrors Old_live_strategies/run_csm_elendel_backtest.py exactly so research
conclusions transfer to the live book:
  * duplicate dates dropped (keep last), non-positive prices -> NaN
  * corporate-action mask: any day with a close-to-close move outside [-40%, +300%] is
    NaN'd across O/H/L/C (un-adjusted splits / bonus / bad prints)
  * benchmark = equal-weight index of all stocks (daily returns clipped to +-50%)
"""
import glob
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd

DATA_DIR = '/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data'
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache')
FIELDS = ('open', 'high', 'low', 'close', 'volume')


def _read_one(path):
    sym = os.path.basename(path)[:-4]
    try:
        df = pd.read_csv(path, usecols=['datetime', 'open', 'high', 'low', 'close', 'volume'],
                         parse_dates=['datetime'], index_col='datetime')
    except Exception:
        return sym, None
    df = df[~df.index.duplicated(keep='last')]
    for c in ('open', 'high', 'low', 'close'):
        df[c] = df[c].mask(df[c] <= 0)
    return sym, df.astype('float64')


def _build_panels():
    files = sorted(glob.glob(os.path.join(DATA_DIR, '*.csv')))
    print(f'[data] reading {len(files)} files ...')
    with Pool(8) as p:
        res = p.map(_read_one, files, chunksize=64)
    res = [(s, d) for s, d in res if d is not None and len(d)]
    panels = {}
    for f in FIELDS:
        panels[f] = pd.DataFrame({s: d[f] for s, d in res}).sort_index()
    # drop junk calendar days (holiday placeholder rows trade almost nothing)
    n_live = panels['close'].notna().sum(axis=1)
    keep = n_live >= 30
    for f in FIELDS:
        panels[f] = panels[f].loc[keep]
    # corporate-action / glitch mask
    ret = panels['close'].pct_change(fill_method=None)
    bad = (ret < -0.40) | (ret > 3.00)
    print(f'[data] corporate-action mask: {int(bad.to_numpy().sum())} cells')
    for f in ('open', 'high', 'low', 'close'):
        panels[f] = panels[f].mask(bad)
    return panels


def load_panels(refresh=False):
    """Return dict of float32 DataFrames: open/high/low/close/volume + 'bench' (Series)."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    paths = {f: os.path.join(CACHE_DIR, f'{f}.parquet') for f in FIELDS}
    if not refresh and all(os.path.exists(p) for p in paths.values()):
        panels = {f: pd.read_parquet(p) for f, p in paths.items()}
    else:
        panels = _build_panels()
        for f, p in paths.items():
            panels[f].astype('float32').to_parquet(p)
        panels = {f: pd.read_parquet(p) for f, p in paths.items()}
    panels = {f: df.astype('float64') for f, df in panels.items()}
    # trailing rows carry only a handful of late-updating symbols -> cut at last full-coverage day
    n_live = panels['close'].notna().sum(axis=1)
    last_ok = n_live[n_live >= 2000].index.max()
    panels = {f: df.loc[:last_ok] for f, df in panels.items()}
    r = panels['close'].pct_change(fill_method=None).clip(-0.5, 0.5)
    panels['bench_ret'] = r.mean(axis=1, skipna=True).fillna(0.0)
    panels['bench'] = (1 + panels['bench_ret']).cumprod()
    return panels


if __name__ == '__main__':
    P = load_panels(refresh=True)
    c = P['close']
    print(c.shape, c.index.min().date(), c.index.max().date())
    n = c.notna().sum(axis=1)
    print(n.resample('YE').last().to_string())
