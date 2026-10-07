"""Portfolio view: do the upgrades help the 3-engine portfolio, and how correlated are the variants with the live engines?  python3 blend_check.py"""
import os, sys, pickle
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold')
from gold_idle_cash import GoldIdleCashOverlay
M = GoldIdleCashOverlay.metrics
D = {n: pickle.load(open(os.path.join(HERE, '.cache', f'impr_{n}.pkl'), 'rb')) for n in ('elendel', 'zenith', 'quad')}
R = lambda n, u, v: D[n][(u, v)]['net_returns'].loc['2005-01-01':]
live = {n: R(n, 'live', 'base') for n in D}
cfgs = {
 'live trio (equal weight)': {n: live[n] for n in D},
 'A: resid-tilt Elendel+Zenith, Quad tight-swap': {'elendel': R('elendel','live','+0.5*resid'), 'zenith': R('zenith','live','+0.5*resid'), 'quad': R('quad','live','tight swap')},
 'B: all three on 301-1000, base scores': {n: R(n,'301-1000','base') for n in D},
 'C: 301-1000 + resid(Z,E) + tight swap(Q)': {'elendel': R('elendel','301-1000','+0.5*resid'), 'zenith': R('zenith','301-1000','+0.5*resid'), 'quad': R('quad','301-1000','tight swap')},
 'D: live Elendel+Quad, Zenith 301-1000+resid': {'elendel': live['elendel'], 'zenith': R('zenith','301-1000','+0.5*resid'), 'quad': live['quad']},
}
print('window 2005+  (engine idle cash earns what the engines assume: Elendel/Quad 0%, Zenith 6.5%)')
for k, c in cfgs.items():
    b = pd.concat(c, axis=1).mean(axis=1)
    for w in ('2005-01-01', '2015-01-01'):
        m = M(b.loc[w:]); print(f"  {k:<48} from {w[:4]}: CAGR {m['cagr']*100:5.1f}%  vol {m['vol']*100:4.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['max_drawdown']*100:6.1f}%")
print('\ndaily-return correlation of selected variants with the three live engines (2015+)')
cor = pd.DataFrame({f'live_{n}': live[n] for n in D})
for lab, (n, u, v) in {'Elendel+0.5resid': ('elendel','live','+0.5*resid'), 'Zenith+0.5resid': ('zenith','live','+0.5*resid'), 'Zenith 301-1000': ('zenith','301-1000','base'),
                       'Quad tight swap': ('quad','live','tight swap'), 'Elendel 301-1000 tight swap': ('elendel','301-1000','tight swap'), 'Quad 301-1000 tight swap': ('quad','301-1000','tight swap')}.items():
    x = R(n, u, v); print(f'  {lab:<30}', '  '.join(f'{c}: {x.loc["2015":].corr(cor[c].loc["2015":]):.2f}' for c in cor))
print('\nlive engines among themselves:', {f'{a}-{b}': round(live[a].loc['2015':].corr(live[b].loc['2015':]), 2) for a, b in (('elendel','zenith'), ('elendel','quad'), ('zenith','quad'))})
