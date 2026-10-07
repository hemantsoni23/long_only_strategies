"""Table of real-engine variants vs the unmodified live engine.  python3 report_improvements.py"""
import os, sys, pickle
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold')
from gold_idle_cash import GoldIdleCashOverlay
M = GoldIdleCashOverlay.metrics
def boot(d, B=3000, blk=21, seed=5):
    d = np.asarray(d.dropna()); n = len(d); rng = np.random.default_rng(seed); k = int(np.ceil(n / blk)); out = []
    for _ in range(B):
        st = rng.integers(0, n, k); idx = ((st[:, None] + np.arange(blk)) % n).ravel()[:n]; out.append(d[idx].mean() * 252)
    return (np.array(out) > 0).mean()
WINS = {'2005+': ('2005-01-01', '2026-07-16'), '2015+': ('2015-01-01', '2026-07-16'), 'fund 2019-06..2025-06': ('2019-06-01', '2025-06-30')}
rows = []
for name in ('elendel', 'zenith', 'quad'):
    p = os.path.join(HERE, '.cache', f'impr_{name}.pkl')
    if not os.path.exists(p): continue
    D = pickle.load(open(p, 'rb'))
    live = D[('live', 'base')]['net_returns']
    for (u, v), d in D.items():
        r = d['net_returns']
        for wn, (a, b) in WINS.items():
            if 'EP' in v and wn != 'fund 2019-06..2025-06': continue
            if 'EP' not in v and wn == 'fund 2019-06..2025-06' and v != 'base': continue
            m = M(r.loc[a:b]); ml = M(live.loc[a:b]); mb = M(D[(u, 'base')]['net_returns'].loc[a:b])
            rows.append(dict(engine=name, universe=u, variant=v, window=wn, cagr=m['cagr'] * 100, sharpe=m['sharpe'], maxdd=m['max_drawdown'] * 100,
                             d_sharpe_vs_samebase=m['sharpe'] - mb['sharpe'], d_cagr_vs_samebase=(m['cagr'] - mb['cagr']) * 100,
                             d_sharpe_vs_live=m['sharpe'] - ml['sharpe'], d_cagr_vs_live=(m['cagr'] - ml['cagr']) * 100,
                             P_gt0_vs_samebase=boot(r.loc[a:b] - D[(u, 'base')]['net_returns'].loc[a:b]) if v != 'base' else np.nan,
                             invested=d['avg_weight']))
df = pd.DataFrame(rows); df.to_csv(os.path.join(HERE, 'improvement_variants.csv'), index=False, float_format='%.4f')
pd.set_option('display.width', 250, 'display.max_columns', 30, 'display.max_rows', 500)
for name in df.engine.unique():
    for wn in WINS:
        s = df[(df.engine == name) & (df.window == wn)]
        if s.empty: continue
        print(f'\n=== {name.upper()}  window {wn}'); print(s.drop(columns=['engine', 'window']).round(3).to_string(index=False))
