"""Pre-registered study (factor_research/INDUSTRY_CAP_PREREG.md): per-industry name cap inside the live Zenith / Elendel engines.  python3 run_industry_cap_study.py"""
import os
import pickle
import numpy as np
import pandas as pd
from common import load_panels, run_engine, metrics, boot, HERE
from industry_cap_strategies import industry_labels

OUT = os.path.join(HERE, 'output'); os.makedirs(OUT, exist_ok=True)
WINDOWS = {'2005+': ('2005-01-01', '2026-07-16'), '2015+': ('2015-01-01', '2026-07-16')}
NPLACEBO = 5
kw = load_panels()
lab = industry_labels()
lines = []
def say(s=''):
    print(s, flush=True); lines.append(s)

def binding(strategy, k):
    """months in which the BASE book holds more than k names of one industry, and the excess names."""
    pos = strategy.positions
    months = excess = 0
    for d, row in pos.iterrows():
        held = row[row > 0].index
        if len(held) == 0:
            continue
        g = pd.Series([lab.get(t) for t in held]).dropna().value_counts()
        ex = int((g - k).clip(lower=0).sum())
        months += ex > 0
        excess += ex
    n = int((pos.sum(axis=1) > 0).sum())
    return months / max(n, 1), excess / max(months, 1), n

store = {}
for which in ('zenith', 'elendel'):
    sb, rb = run_engine(which, kw, cap_k=None)
    base = rb['net_returns']; store[(which, 'base')] = base
    runs = {}
    for k in (2, 3):
        s, r = run_engine(which, kw, cap_k=k); runs[f'K={k}'] = r['net_returns']
        if k == 2:
            frac_months, avg_excess, nm = binding(sb, 2)
            changed = int(((sb.positions > 0) != (s.positions.reindex_like(sb.positions) > 0)).any(axis=1).sum())
            bind = (frac_months, avg_excess, nm, changed)
    for sd in range(NPLACEBO):
        s, r = run_engine(which, kw, cap_k=2, label_seed=100 + sd); runs[f'placebo{sd}'] = r['net_returns']
    store.update({(which, k): v for k, v in runs.items()})

    say(f'\n=== {which.upper()}  (native runs, current engine code, 0.3% cost)')
    say(f'  cap K=2 binds in {bind[0]*100:.0f}% of invested months (avg {bind[1]:.1f} excess names when binding); {bind[3]} of {bind[2]} invested months have a different holdings set')
    verdict = {}
    for wn, (a, b) in WINDOWS.items():
        mb = metrics(base.loc[a:b])
        say(f'  {wn:<6} {"base":<10} CAGR {mb["cagr"]*100:5.1f}%  vol {mb["vol"]*100:4.1f}%  Sharpe {mb["sharpe"]:5.2f}  MaxDD {mb["maxdd"]*100:6.1f}%  Calmar {mb["calmar"]:4.2f}')
        for k, r in runs.items():
            m = metrics(r.loc[a:b]); d = r.loc[a:b] - base.loc[a:b]
            corr = r.loc[a:b].corr(base.loc[a:b])
            s = (f'  {wn:<6} {k:<10} CAGR {m["cagr"]*100:5.1f}%  vol {m["vol"]*100:4.1f}%  Sharpe {m["sharpe"]:5.2f}  MaxDD {m["maxdd"]*100:6.1f}%  Calmar {m["calmar"]:4.2f}'
                 f'  | dCAGR {100*(m["cagr"]-mb["cagr"]):+5.1f} dSharpe {m["sharpe"]-mb["sharpe"]:+.2f} dMaxDD {100*(m["maxdd"]-mb["maxdd"]):+5.1f}pt corr {corr:.3f}')
            if k == 'K=2':
                s += f'  P(better) {boot(d):.2f}'
            say(s)
            verdict[(wn, k)] = (m['cagr'] - mb['cagr'], m['sharpe'] - mb['sharpe'], m['maxdd'] - mb['maxdd'])
    # gates
    P1 = all(verdict[(w, 'K=2')][1] >= 0 for w in WINDOWS)
    P2 = all(verdict[(w, 'K=2')][0] >= -0.01 for w in WINDOWS)
    P3 = all(verdict[(w, 'K=2')][2] >= 0 for w in WINDOWS) and verdict[('2005+', 'K=2')][2] >= 0.02
    plac = np.median([verdict[('2005+', f'placebo{i}')][1] for i in range(NPLACEBO)])
    P4 = verdict[('2005+', 'K=2')][1] > plac
    P5 = bind[0] >= 0.10
    say(f'  GATES  P1 Sharpe>=0 both windows: {"PASS" if P1 else "FAIL"} | P2 dCAGR>=-1pt both: {"PASS" if P2 else "FAIL"} | P3 dMaxDD>=0 both & >=+2pt in 2005+: {"PASS" if P3 else "FAIL"} '
        f'| P4 beats placebo median dSharpe ({plac:+.2f}) in 2005+: {"PASS" if P4 else "FAIL"} | P5 binds>=10% of months: {"PASS" if P5 else "FAIL (inconclusive)"}')
    say(f'  OVERALL {which}: {"ALL PASS" if all([P1, P2, P3, P4, P5]) else "NOT ALL PASS"}')
    yr = pd.DataFrame({'base': base, 'K=2': runs['K=2']}).loc['2003':]
    yy = (1 + yr).groupby(yr.index.year).prod() - 1
    say('  year-by-year K=2 minus base (pts): ' + '  '.join(f'{y}:{v:+.1f}' for y, v in ((yy['K=2'] - yy['base']) * 100).items()))

open(os.path.join(OUT, 'industry_cap_study.txt'), 'w').write('\n'.join(lines) + '\n')
pickle.dump(store, open(os.path.join(OUT, 'industry_cap_returns.pkl'), 'wb'))
