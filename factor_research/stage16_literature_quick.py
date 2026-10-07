"""stage16 -- two cheap literature checks.
 (A) Barroso/Santa-Clara & Daniel/Moskowitz style exposure scaling applied to the REAL engine daily returns (post-processing):
     own-vol targeting (126d), and a 'crash state' rule (market 24m return < 0 AND market 63d vol in its top 25%) -> half exposure.
     The engines already have regime scaling + 20% vol target + Crash Guard, so only the INCREMENT is of interest.
 (B) Balvers-Wu: 12-1 momentum + long-run (t-60m .. t-12m) reversal, IC and incremental IC vs Elendel composite (price only)."""
import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold')
from gold_idle_cash import GoldIdleCashOverlay
from data import load_panels
from evaluate import composite, zscore, rank_ic, nw_tstat
HERE = os.path.dirname(os.path.abspath(__file__)); M = GoldIdleCashOverlay.metrics
P = load_panels(); bench = P['bench']; br = P['bench_ret']

print('=== (A) exposure scaling on engine daily returns (2005+), liquid-fund 6.5% on de-levered part')
lf = (1.065) ** (1 / 252) - 1
mkt24 = bench / bench.shift(504) - 1
mvol = br.rolling(63).std().shift(1); mvol_hi = mvol > mvol.expanding(504).quantile(0.75).shift(1)
crash_state = ((mkt24.shift(1) < 0) & mvol_hi)
for name in ('elendel', 'zenith', 'quad'):
    p = pickle.load(open(f'/Users/hemantsoni/Documents/long_only_strategies/momentum_gold/.cache/engine_{name}.pkl', 'rb'))
    r = p['net_returns']; r = r.loc['2005-01-01':]
    sig = r.rolling(126).std().shift(1) * np.sqrt(252)
    out = {'engine as is': r}
    for tgt in (0.12, 0.15):
        s = (tgt / sig).clip(upper=1.0).fillna(1.0)
        out[f'own-vol target {tgt:.0%} (de-lever only)'] = r * s + (1 - s) * lf
    s2 = pd.Series(np.where(crash_state.reindex(r.index).fillna(False), 0.5, 1.0), index=r.index)
    out['crash state -> 50% exposure'] = r * s2 + (1 - s2) * lf
    out['crash state frequency'] = None
    print(f'\n{name.upper()}   (crash-state days: {s2.eq(0.5).mean():.0%})')
    mb = M(r)
    for k, v in out.items():
        if v is None: continue
        m = M(v)
        print(f"  {k:<40} CAGR {m['cagr']*100:5.1f}%  vol {m['vol']*100:5.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['max_drawdown']*100:6.1f}%  worstMonth {m['worst_month']*100:5.1f}%")

print('\n=== (B) long-run reversal (Balvers-Wu) — price-only, IC at 3m / 6m / 12m')
st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb')); sig_, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
Cf = P['close'].ffill()
def at(d): return d.reindex(sig_)
rev60_12 = -(at(Cf.shift(252)) / at(Cf.shift(1260)) - 1)           # losers of the prior 4y (t-60m..t-12m)
rev36_12 = -(at(Cf.shift(252)) / at(Cf.shift(756)) - 1)
dist_3y_hi = -(at(Cf) / Cf.rolling(756, min_periods=500).max().reindex(sig_) - 1)    # far below 3y high = "cheap" in price terms
for un in ('U1_liquid1000', 'U3_top300'):
    mask = U[un]; base = composite(F, ['a3_rs_high', 'q5_126'], mask)
    for nm, S in (('rev_60_12', rev60_12), ('rev_36_12', rev36_12), ('far_from_3y_high', dist_3y_hi)):
        row = [nm, un]
        for h in (3, 6, 12):
            ic, _ = rank_ic(S.where(mask), FWD[h].where(mask)); ic = ic.dropna()
            row += [f'IC{h} {ic.mean():+.3f} (t {nw_tstat(ic,h-1):+.1f}, hit {np.mean(ic>0):.0%})']
        bc, _ = rank_ic(S.where(mask), base.where(mask))
        row += [f'corr_elendel {bc.mean():+.2f}']
        print('  ' + ' | '.join(row))
