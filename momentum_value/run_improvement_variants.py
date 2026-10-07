"""Real-engine comparison of candidate improvements, for the ranking document.
Engines are the unmodified live classes; only `csm.factors` (monthly score) and the universe rank band are changed, exactly like run_value_engines.py.
    python3 run_improvement_variants.py elendel zenith quad     -> .cache/impr_<name>.pkl
Variants (per universe band: 'live' and '301-1000'):
  base | q5only | +0.5*resid | +0.5*lowrisk | tight swap (z(tight_close_15)+z(q5)) | +0.5*tight | +0.5*intraday | +0.5*EP | +1.0*EP
Harness factors (factor_research/.cache/state.pkl, month-end trading days) are mapped to the engine's calendar month-ends by as-of lookup."""
import os, sys, pickle, time, importlib, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
FR = '/Users/hemantsoni/Documents/long_only_strategies/factor_research'
sys.path.insert(0, LIVE); sys.path.insert(0, FR)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache'); os.makedirs(OUT, exist_ok=True)
END = '2026-07-16'; LOAD_START = '2001-01-01'
which = sys.argv[1:] or ['elendel', 'zenith', 'quad']
from stage15_fundamental_momentum import build_quarter_table, to_monthly
ele = importlib.import_module('run_csm_elendel_backtest')
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc[LOAD_START:END] if not d.empty else d
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
bench = ele.build_benchmark(prices)
st = pickle.load(open(os.path.join(FR, '.cache', 'state.pkl'), 'rb')); Fh = st['F']; sig = st['sig']
me = prices.resample('ME').last().index
def to_me(name):
    d = Fh[name].reindex(columns=prices.columns)
    return d.reindex(d.index.union(me)).ffill().reindex(me)
HF = {k: to_me(k) for k in ('q5_126', 'q5_189', 'mom_resid_12_1', 'lowvol_126', 'low_ulcer_252', 'tight_close_15', 'intra_over_126')}
q = build_quarter_table(); q = q[q.symbol.isin(prices.columns)].reset_index(drop=True)
Pm = prices.resample('ME').last()
M_ = {k: to_monthly(q, k, me).reindex(columns=prices.columns) for k in ('np_ttm', 'shares')}
EP = (M_['np_ttm'] / (Pm * M_['shares'])).replace([np.inf, -np.inf], np.nan)
zs = lambda d: d.sub(d.mean(axis=1), axis=0).div(d.std(axis=1), axis=0)
def blend(base, add, w):
    e = add.reindex(index=base.index, columns=base.columns).where(base.notna())
    ok = e.notna().sum(axis=1) >= 60
    z = zs(base) + w * zs(e).fillna(0.0)
    return base.where(~ok.reindex(base.index).fillna(False), z)
def masked(x, base):
    return x.reindex(index=base.index, columns=base.columns).where(base.notna())
def variants(base, name):
    q5 = 'q5_189' if name == 'zenith' else 'q5_126'
    v = {'base': base}
    if name != 'quad':
        v['q5only'] = zs(masked(HF[q5], base))
    v['+0.5*resid'] = blend(base, HF['mom_resid_12_1'], 0.5)
    lowrisk = (zs(masked(HF['lowvol_126'], base)) + zs(masked(HF['low_ulcer_252'], base))) / 2
    v['+0.5*lowrisk'] = blend(base, lowrisk, 0.5)
    v['tight swap'] = zs(masked(HF['tight_close_15'], base)) + zs(masked(HF[q5], base))
    v['+0.5*tight'] = blend(base, HF['tight_close_15'], 0.5)
    v['+0.5*intraday'] = blend(base, HF['intra_over_126'], 0.5)
    v['+0.5*EP'] = blend(base, EP, 0.5)
    v['+1.0*EP'] = blend(base, EP, 1.0)
    return v
for name in which:
    if name == 'elendel':
        from csm_elendel_strategy import CSMElendel as S; mod = ele; live = (1, 1000)
    elif name == 'quad':
        q_ = importlib.import_module('run_csm_quad_momentum_backtest'); from csm_quad_momentum_strategy import CSMQuadMomentum as S; mod = q_; live = (500, 1000)
    else:
        zen = importlib.import_module('run_csm_zenith_backtest'); from csm_zenith_strategy import CSMZenith as S; mod = zen; live = (1, 1000)
    out = {}
    for ulab, (lo, hi) in (('live', live), ('301-1000', (301, 1000))):
        if ulab == '301-1000' and name == 'quad':
            lo = 301
        csm = S(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, universe_top_n_min=lo, universe_top_n_max=hi)
        csm.calculate_factors(); base = csm.factors.copy()
        for vn, sc in variants(base, name).items():
            t1 = time.time(); csm.factors = sc; csm.get_positions()
            res = mod.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
            out[(ulab, vn)] = dict(net_returns=res['net_returns'], avg_weight=res['executed_weights'].sum(axis=1).mean(), regime=res['regime'])
            print(f'[{name}|{ulab}|{vn}] {time.time()-t1:.0f}s  CAGR {res["cagr"]*100:.1f}% Sharpe {res["sharpe"]:.2f} MaxDD {res["max_drawdown"]*100:.1f}%', flush=True)
    pickle.dump(out, open(os.path.join(OUT, f'impr_{name}.pkl'), 'wb'), protocol=4)
