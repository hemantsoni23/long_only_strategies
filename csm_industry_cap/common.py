"""Shared data loading / metrics for the industry-cap study (same loading path as csm_resid_tilt/compare_to_live.py)."""
import importlib
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from industry_cap_strategies import CSMZenithIndCap, CSMElendelIndCap, CSMZenith, CSMElendel, LIVE   # noqa: E402

ele = importlib.import_module('run_csm_elendel_backtest')
zen = importlib.import_module('run_csm_zenith_backtest')
MODS = {'zenith': zen, 'elendel': ele}
LIVE_CLS = {'zenith': CSMZenith, 'elendel': CSMElendel}
CAP_CLS = {'zenith': CSMZenithIndCap, 'elendel': CSMElendelIndCap}
END = '2026-07-16'


def load_panels():
    prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
    sl = lambda d: d.loc['2001-01-01':END]
    prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
    prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
    bench = ele.build_benchmark(prices)
    return dict(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench)


def run_engine(which, kw, cap_k=None, label_seed=None, quiet=True):
    """cap_k=None -> the unmodified live class; otherwise the cap subclass. Returns (strategy, result dict)."""
    import contextlib, io
    buf = io.StringIO()
    ctx = contextlib.redirect_stdout(buf) if quiet else contextlib.nullcontext()
    with ctx:
        if cap_k is None:
            s = LIVE_CLS[which](**kw)
        else:
            s = CAP_CLS[which](industry_cap_k=cap_k, label_seed=label_seed, **kw)
        s.calculate_factors()
        s.get_positions()
        res = MODS[which].backtest_event_driven(s, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    return s, res


def metrics(r, rf=0.06):
    r = r.dropna()
    eq = (1 + r).cumprod()
    y = len(r) / 252
    dd = (eq / eq.cummax() - 1).min()
    cagr = eq.iloc[-1] ** (1 / y) - 1
    return dict(cagr=cagr, vol=r.std() * np.sqrt(252),
                sharpe=((r - ((1 + rf) ** (1 / 252) - 1)).mean() / r.std()) * np.sqrt(252), maxdd=dd, calmar=cagr / abs(dd))


def boot(d, B=4000, blk=21, seed=7):
    d = np.asarray(d.dropna())
    n = len(d)
    rng = np.random.default_rng(seed)
    k = int(np.ceil(n / blk))
    o = []
    for _ in range(B):
        st = rng.integers(0, n, k)
        o.append(d[((st[:, None] + np.arange(blk)) % n).ravel()[:n]].mean() * 252)
    o = np.array(o)
    return (o > 0).mean()
