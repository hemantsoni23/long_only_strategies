"""Re-test of the earlier 'E/P tilt' on the live engines with UNIT-CONSISTENT market caps (csm_value/fundamentals_loader: shares restored to today's units to match the split-adjusted prices).
The earlier runs (run_value_engines.py / run_improvement_variants.py) multiplied adjusted prices by raw filed share counts, which leaks future splits/bonuses.  python3 rerun_ep_tilt_corrected.py"""
import os, sys, importlib, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'; sys.path.insert(0, LIVE); sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/csm_value')
import fundamentals_loader as fl
ele = importlib.import_module('run_csm_elendel_backtest')
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2025-06-30'] if not d.empty else d
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens); bench = ele.build_benchmark(prices)
me = prices.resample('ME').last().index; Pm = prices.resample('ME').last()
res = fl.load_results(symbols=list(prices.columns))
npttm = fl.monthly_frame(res, 'np_ttm', me, prices.columns); sh_adj = fl.monthly_frame(res, 'shares_adj', me, prices.columns)
EP = (npttm / (Pm * sh_adj)).replace([np.inf, -np.inf], np.nan)
zs = lambda d: d.sub(d.mean(axis=1), axis=0).div(d.std(axis=1), axis=0)
def blend(base, ep, w):
    e = ep.reindex(index=base.index, columns=base.columns).where(base.notna()); ok = e.notna().sum(axis=1) >= 60
    return base.where(~ok.reindex(base.index).fillna(False), zs(base) + w * zs(e).fillna(0.0))
def metrics(r, a, b):
    r = r.loc[a:b]; eq = (1 + r).cumprod(); y = (r.index[-1] - r.index[0]).days / 365.25; dd = eq / eq.cummax() - 1
    return eq.iloc[-1] ** (1 / y) - 1, r.mean() / r.std() * np.sqrt(252), dd.min()
def boot(d, B=3000, blk=21, seed=3):
    d = np.asarray(d.dropna()); n = len(d); rng = np.random.default_rng(seed); k = int(np.ceil(n / blk)); o = []
    for _ in range(B):
        s = rng.integers(0, n, k); o.append(d[((s[:, None] + np.arange(blk)) % n).ravel()[:n]].mean() * 252)
    return (np.array(o) > 0).mean()
W = ('2019-06-03', '2025-06-30')
for name in ('zenith', 'quad', 'elendel'):
    if name == 'elendel':
        from csm_elendel_strategy import CSMElendel as S; mod = ele; lo = 1
    elif name == 'quad':
        q_ = importlib.import_module('run_csm_quad_momentum_backtest'); from csm_quad_momentum_strategy import CSMQuadMomentum as S; mod = q_; lo = 500
    else:
        zen = importlib.import_module('run_csm_zenith_backtest'); from csm_zenith_strategy import CSMZenith as S; mod = zen; lo = 1
    csm = S(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, universe_top_n_min=lo, universe_top_n_max=1000)
    csm.calculate_factors(); base = csm.factors.copy(); out = {}
    for tag, w in (('base', 0.0), ('+0.5*EP', 0.5), ('+1.0*EP', 1.0)):
        csm.factors = blend(base, EP, w) if w else base; csm.get_positions()
        out[tag] = mod.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)['net_returns']
    b = metrics(out['base'], *W)
    for tag in ('base', '+0.5*EP', '+1.0*EP'):
        c, s, d = metrics(out[tag], *W)
        extra = '' if tag == 'base' else f'  dCAGR {100*(c-b[0]):+5.1f}pt dSharpe {s-b[1]:+.2f}  P(better) {boot(out[tag].loc[W[0]:W[1]] - out["base"].loc[W[0]:W[1]]):.2f}'
        print(f'[{name:<7}] {tag:<8} CAGR {c*100:5.1f}% Sharpe(rf0) {s:4.2f} MaxDD {d*100:6.1f}%{extra}', flush=True)
