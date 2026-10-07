"""Value x momentum on the REAL live engines (Old_live_strategies untouched).

Hook: after `csm.calculate_factors()` the engine's monthly score `csm.factors` is replaced by
        z(base score) + w * z(E/P)           (E/P missing -> 0 = neutral; on dates with < 60 E/P values the base score is left unchanged)
and the unmodified `get_positions()` / `backtest_event_driven()` run as usual (same stops, regimes, vol target, 0.3% cost).
E/P = TTM net profit / (price x latest shares_out), point-in-time (quarter usable from its filed_date, expires after 140 days).
Fundamentals exist 2019-02 .. ~2025-06, so variants equal the baseline outside that window; compare only inside it.

    python3 run_value_engines.py elendel quad zenith
"""
import os, sys, pickle, time, importlib, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
FR = '/Users/hemantsoni/Documents/long_only_strategies/factor_research'
sys.path.insert(0, LIVE); sys.path.insert(0, FR)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache'); os.makedirs(OUT, exist_ok=True)
END = '2026-07-16'; LOAD_START = '2001-01-01'
which = sys.argv[1:] or ['elendel', 'quad', 'zenith']
VARIANTS = [('base', None, 0.0), ('np_w0.5', 'ep_np', 0.5), ('np_w1.0', 'ep_np', 1.0), ('eps_w0.5', 'ep_eps', 0.5)]

from stage15_fundamental_momentum import build_quarter_table, to_monthly
ele = importlib.import_module('run_csm_elendel_backtest')
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc[LOAD_START:END] if not d.empty else d
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
bench = ele.build_benchmark(prices)

q = build_quarter_table(); q = q[q.symbol.isin(prices.columns)].reset_index(drop=True)
me = prices.resample('ME').last().index
Pm = prices.resample('ME').last()
M = {k: to_monthly(q, k, me).reindex(columns=prices.columns) for k in ('np_ttm', 'eps_ttm', 'shares')}
EP = {'ep_np': (M['np_ttm'] / (Pm * M['shares'])).replace([np.inf, -np.inf], np.nan),
      'ep_eps': (M['eps_ttm'] / Pm).replace([np.inf, -np.inf], np.nan)}
print('E/P coverage by year (avg names/month):', EP['ep_np'].notna().sum(axis=1).groupby(me.year).mean().round(0).to_dict(), flush=True)

zs = lambda d: d.sub(d.mean(axis=1), axis=0).div(d.std(axis=1), axis=0)

def blend(base, ep, w):
    if w == 0:
        return base
    e = ep.reindex(index=base.index, columns=base.columns).where(base.notna())
    ok = e.notna().sum(axis=1) >= 60
    z = zs(base) + w * zs(e).fillna(0.0)
    return base.where(~ok.reindex(base.index).fillna(False), z)

def run(name):
    if name == 'elendel':
        from csm_elendel_strategy import CSMElendel as S; mod = ele
    elif name == 'quad':
        q_ = importlib.import_module('run_csm_quad_momentum_backtest'); from csm_quad_momentum_strategy import CSMQuadMomentum as S; mod = q_
    else:
        zen = importlib.import_module('run_csm_zenith_backtest'); from csm_zenith_strategy import CSMZenith as S; mod = zen
    csm = S(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench,
            universe_top_n_min=(500 if name == 'quad' else 1), universe_top_n_max=1000)
    csm.calculate_factors()
    base_factors = csm.factors.copy()
    out = {}
    for tag, ep, w in VARIANTS:
        t1 = time.time()
        csm.factors = blend(base_factors, EP[ep] if ep else None, w)
        csm.get_positions()
        res = mod.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
        out[tag] = dict(net_returns=res['net_returns'], executed_weights=res['executed_weights'], regime=res['regime'],
                        cagr=res['cagr'], sharpe=res['sharpe'], max_drawdown=res['max_drawdown'])
        print(f'[{name}:{tag}] {time.time()-t1:.0f}s  full-sample CAGR {res["cagr"]*100:.2f}%  Sharpe {res["sharpe"]:.2f}  MaxDD {res["max_drawdown"]*100:.1f}%', flush=True)
    pickle.dump(out, open(os.path.join(OUT, f'value_{name}.pkl'), 'wb'), protocol=4)

for n in which:
    run(n)
