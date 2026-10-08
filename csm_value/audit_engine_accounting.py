"""Does the engine's same-day-weight x same-day-return accounting inflate the LIVE strategies' backtests as well?  (read-only use of Old_live_strategies)
    python3 audit_engine_accounting.py            -> output/audit_engine_accounting.txt"""
import os, sys, importlib, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'; sys.path.insert(0, LIVE)
from execution_replay import faithful_net_returns
ele = importlib.import_module('run_csm_elendel_backtest')
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2026-07-16']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens); bench = ele.build_benchmark(prices)
def metrics(r, a, b):
    r = r.loc[a:b].dropna(); eq = (1 + r).cumprod(); y = (r.index[-1] - r.index[0]).days / 365.25; dd = eq / eq.cummax() - 1
    return (eq.iloc[-1] ** (1 / y) - 1) * 100, r.mean() / r.std() * np.sqrt(252), dd.min() * 100
lines = []
SAVE = {}
for name in ('elendel', 'zenith', 'quad'):
    if name == 'elendel':
        from csm_elendel_strategy import CSMElendel as S; mod = ele; lo = 1
    elif name == 'quad':
        q_ = importlib.import_module('run_csm_quad_momentum_backtest'); from csm_quad_momentum_strategy import CSMQuadMomentum as S; mod = q_; lo = 500
    else:
        z_ = importlib.import_module('run_csm_zenith_backtest'); from csm_zenith_strategy import CSMZenith as S; mod = z_; lo = 1
    csm = S(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, universe_top_n_min=lo, universe_top_n_max=1000)
    csm.calculate_factors(); csm.get_positions()
    res = mod.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    rate = ((1 + csm.liquid_mf_annual_rate) ** (1 / 252) - 1) if csm.use_liquid_mf else 0.0
    net, info = faithful_net_returns(csm, res, 0.003, rate)
    SAVE[name + '_engine'] = res['net_returns']; SAVE[name + '_faithful'] = net
    for w, (a, b) in {'2003-2026': ('2003-01-01', '2026-07-16'), '2015+': ('2015-01-01', '2026-07-16'), '2019-06..2025-06': ('2019-06-03', '2025-06-30')}.items():
        e, f = metrics(res['net_returns'], a, b), metrics(net, a, b)
        lines.append(f'{name:<8} {w:<17} engine CAGR {e[0]:5.1f}% Sharpe {e[1]:.2f} MaxDD {e[2]:6.1f}%  |  execution-faithful CAGR {f[0]:5.1f}% Sharpe {f[1]:.2f} MaxDD {f[2]:6.1f}%  (difference {f[0]-e[0]:+.1f} pt)')
    meta = pd.DataFrame(csm.position_metadata); st = meta[meta.Exit_Reason == 'STOP_HIT']
    lines.append(f'{name:<8} stops: {len(st)} of {len(meta)} trades; entries adjusted {info["entries_adjusted"]}, exits adjusted {info["exits_adjusted"]}')
    print('\n'.join(lines[-4:]), flush=True)
pd.DataFrame(SAVE).to_csv(os.path.join(HERE, 'output', 'faithful_engine_returns.csv'))
open(os.path.join(HERE, 'output', 'audit_engine_accounting.txt'), 'w').write('\n'.join(lines) + '\n')
