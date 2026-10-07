"""Live engines (unmodified) on liquidity tiers BELOW their live universe: Hong-Lim-Stein 'bad news travels slowly' / GJM size effects.
    python3 run_universe_engines.py elendel zenith quad   -> .cache/univ_<name>.pkl ; prints metrics + capacity of the held names."""
import os, sys, pickle, time, importlib, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
sys.path.insert(0, LIVE)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache'); os.makedirs(OUT, exist_ok=True)
END = '2026-07-16'; LOAD_START = '2001-01-01'
which = sys.argv[1:] or ['elendel', 'zenith', 'quad']
TIERS = {'live': None, 'r1001_1500': (1001, 1500), 'r1001_2000': (1001, 2000), 'r301_1000': (301, 1000), 'r1_2000': (1, 2000)}
ele = importlib.import_module('run_csm_elendel_backtest')
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc[LOAD_START:END] if not d.empty else d
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
bench = ele.build_benchmark(prices)
adv = (prices * volumes).rolling(63, min_periods=21).median().shift(1)
def metrics(r, rf=0.06):
    r = r.dropna(); eq = (1 + r).cumprod(); yrs = len(r) / 252
    return dict(cagr=eq.iloc[-1] ** (1 / yrs) - 1, vol=r.std() * np.sqrt(252), sharpe=((r - ((1 + rf) ** (1 / 252) - 1)).mean() / r.std()) * np.sqrt(252), maxdd=(eq / eq.cummax() - 1).min())
for name in which:
    if name == 'elendel':
        from csm_elendel_strategy import CSMElendel as S; mod = ele; live = (1, 1000)
    elif name == 'quad':
        q_ = importlib.import_module('run_csm_quad_momentum_backtest'); from csm_quad_momentum_strategy import CSMQuadMomentum as S; mod = q_; live = (500, 1000)
    else:
        zen = importlib.import_module('run_csm_zenith_backtest'); from csm_zenith_strategy import CSMZenith as S; mod = zen; live = (1, 1000)
    res_all = {}
    for tag, rng in TIERS.items():
        lo, hi = live if rng is None else rng
        t1 = time.time()
        csm = S(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, universe_top_n_min=lo, universe_top_n_max=hi)
        csm.calculate_factors(); csm.get_positions()
        res = mod.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
        w = res['executed_weights']; r = res['net_returns']
        # capacity: for each held name-day, ADV; a position of X rupees is 5% of ADV when X = 0.05*ADV  => book size = min over names of 0.05*ADV/weight (10th pct of days)
        held = w.where(w > 0.005)
        cap = (0.05 * adv.reindex(w.index) / held).stack()
        res_all[tag] = dict(net_returns=r, regime=res['regime'], avg_weight=w.sum(axis=1).mean(), cap_p10=cap.quantile(0.10) / 1e7, cap_p50=cap.median() / 1e7)
        m = metrics(r.loc['2005-01-01':]); mh = metrics(r.loc['2015-01-01':])
        print(f'[{name}:{tag}] {time.time()-t1:.0f}s  2005+: CAGR {m["cagr"]*100:.1f}% Sharpe {m["sharpe"]:.2f} MaxDD {m["maxdd"]*100:.1f}% | 2015+: CAGR {mh["cagr"]*100:.1f}% Sharpe {mh["sharpe"]:.2f} MaxDD {mh["maxdd"]*100:.1f}% | '
              f'capacity@5%ADV (10th pct / median) Rs {res_all[tag]["cap_p10"]:.1f} / {res_all[tag]["cap_p50"]:.1f} cr  invested {res_all[tag]["avg_weight"]:.0%}', flush=True)
    pickle.dump(res_all, open(os.path.join(OUT, f'univ_{name}.pkl'), 'wb'), protocol=4)
