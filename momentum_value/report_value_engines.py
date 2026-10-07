"""Compare engine variants (z(base)+w*z(E/P)) with the unmodified engine inside the fundamentals window.
    python3 report_value_engines.py"""
import os, sys, pickle
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold')
from gold_idle_cash import GoldIdleCashOverlay
M = GoldIdleCashOverlay.metrics
W0, W1 = '2019-06-01', '2025-06-30'
lines = []
def say(s=''):
    print(s); lines.append(s)

def boot(d, B=4000, blk=21, seed=3):
    d = np.asarray(d.dropna()); n = len(d); rng = np.random.default_rng(seed); out = []
    k = int(np.ceil(n / blk))
    for _ in range(B):
        st = rng.integers(0, n, k); idx = ((st[:, None] + np.arange(blk)) % n).ravel()[:n]
        out.append(d[idx].mean() * 252)
    out = np.array(out); return (out > 0).mean(), np.percentile(out, 5), np.percentile(out, 95)

for name in ('elendel', 'zenith', 'quad'):
    p = os.path.join(HERE, '.cache', f'value_{name}.pkl')
    if not os.path.exists(p):
        say(f'[{name}] missing'); continue
    D = pickle.load(open(p, 'rb'))
    base = D['base']['net_returns'].loc[W0:W1]
    say('\n' + '=' * 118); say(f' {name.upper()}   window {W0}..{W1}  ({len(base)/252:.1f} yrs)'); say('=' * 118)
    mb = M(base)
    for tag, d in D.items():
        r = d['net_returns'].loc[W0:W1]; m = M(r); dd = r - base
        s = f"  {tag:<10} CAGR {m['cagr']*100:5.1f}%  vol {m['vol']*100:5.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['max_drawdown']*100:6.1f}%  Calmar {m['calmar']:5.2f}"
        if tag != 'base':
            pg, lo, hi = boot(dd)
            s += f"  | dCAGR {100*(m['cagr']-mb['cagr']):+5.1f}pt dSharpe {m['sharpe']-mb['sharpe']:+.2f} dMaxDD {100*(m['max_drawdown']-mb['max_drawdown']):+5.1f}pt  boot P(d>0)={pg:.2f} 90%CI of ann.excess [{lo*100:+.1f},{hi*100:+.1f}]%"
        say(s)
    for tag in ('np_w0.5', 'np_w1.0'):
        r = D[tag]['net_returns'].loc[W0:W1]
        yr = ((1 + r).groupby(r.index.year).prod() - (1 + base).groupby(base.index.year).prod()) * 100
        say(f'  {tag} year delta (pts): ' + '  '.join(f'{y}:{v:+.1f}' for y, v in yr.items()))
    w = D['np_w0.5']['executed_weights'].loc[W0:W1].sum(axis=1).mean(); wb = D['base']['executed_weights'].loc[W0:W1].sum(axis=1).mean()
    say(f'  mean invested weight: base {wb:.0%}  np_w0.5 {w:.0%}')
open(os.path.join(HERE, 'value_engines_report.txt'), 'w').write('\n'.join(lines) + '\n')
