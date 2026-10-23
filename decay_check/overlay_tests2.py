"""Addendum 6: user's upgrade list, add-one + plateau + forward selection on Aegis v1.1 (close fills)."""
import os, sys, json, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine2 as SE2
from ovl_metrics import met
def full(cfg):
    R = SE2.run(**cfg); r = R['ret']; m = met(r); yrs = len(r[r.index >= '2005-01-01']) / 252; m['turn'] = R['turnover'] / yrs
    hA, hB = met(r, '2005-01-01', '2012-12-31'), met(r, '2013-01-01'); m['shA'], m['shB'], m['calA'], m['calB'] = hA['sharpe'], hB['sharpe'], hA['calmar'], hB['calmar']
    m['sh_l2'] = met(r, '2020-06-01', '2026-06-30')['sharpe']; m['sh_c6'] = met(SE2.run(**{**cfg, 'cost': 0.006})['ret'])['sharpe']
    e = (1 + r[r.index >= '2005-01-01']).cumprod(); m['cur_dd'] = float((e / e.cummax() - 1).iloc[-1]); m['r25'] = float((1 + r.loc['2025-01-01':]).prod() - 1); return m
def judge(c, b):
    sr, cr = c['sharpe'] / b['sharpe'] - 1, c['calmar'] / b['calmar'] - 1; why = []
    if not (cr >= 0.10 or sr >= 0.05): why.append('a: gain too small')
    if sr < -0.15 or cr < -0.15: why.append('b: Sharpe/Calmar regress >15%')
    if c['stab'] > 1.2 * b['stab']: why.append('b: stability worse >20%')
    if abs(c['avg_dd']) > 1.2 * abs(b['avg_dd']): why.append('b: avg DD depth worse >20%')
    if c['turn'] > 1.25 * b['turn']: why.append('b: turnover +25%')
    if c['shA'] < 0.95 * b['shA'] or c['shB'] < 0.95 * b['shB']: why.append('c: a half regresses >5%')
    if c['sh_l2'] < b['sh_l2']: why.append('d: latest 2 chunks Sharpe lower')
    if c['sh_c6'] < b['sh_c6']: why.append('e: worse at 0.6% cost')
    return why, (sr + cr) / 2, sr, cr
BASE = dict(sel='R1', mkt_gate=True, fill='close')
CAND = {'S1 selector R1+A1': dict(sel='R1A1'), 'S2 selector R1+Ulcer': dict(sel='R1ULC'), 'F1 volgate off': dict(volgate=False), 'F2 gate window 120': dict(mkt_win=120), 'F3 time stop off': dict(timestop=False),
        'F4 stop 12%': dict(stop=0.12), 'P2 vol target 15%': dict(vol_target=0.15), 'P3 band (200,1000)': dict(band=(200, 1000))}
PLATEAU = {'F2 gate window 120': [dict(mkt_win=100), dict(mkt_win=150)], 'F4 stop 12%': [dict(stop=0.10), dict(stop=0.15)], 'P3 band (200,1000)': [dict(band=(150, 1000)), dict(band=(250, 1000))]}
POSTLOOK = {'F1 volgate off', 'F2 gate window 120', 'F3 time stop off', 'F4 stop 12%', 'P3 band (200,1000)'}
running = dict(BASE); base = full(running); rows = []; adopted = []; nlook = 0
print('BASELINE v1.1 close fills', {k: round(float(v), 3) for k, v in base.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd', 'turn', 'r25', 'cur_dd')}, flush=True)
ob = full({**BASE, 'fill': 'open'}); print('v1.1 open fills (as reported before)', {k: round(float(v), 3) for k, v in ob.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd')}, flush=True)
p1 = full({**BASE, 'cash_rate': 0.065}); print('P1 cash 6.5% (separate):', {k: round(float(v), 3) for k, v in p1.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd')}, flush=True)
p1b = full({**BASE, 'cash_rate': 0.04}); print('cash 4%:', {k: round(float(v), 3) for k, v in p1b.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd')}, flush=True)
for rnd in range(1, 5):
    res = {}
    for name, kw in CAND.items():
        if name in adopted: continue
        m = full({**running, **kw}); why, score, sr, cr = judge(m, base)
        if name in PLATEAU and not why:
            for nb in PLATEAU[name]:
                mn = full({**running, **nb})
                if mn['sharpe'] < base['sharpe']: why.append(f'plateau: neighbour {list(nb.values())[0]} Sharpe {mn["sharpe"]:.2f} < running {base["sharpe"]:.2f}')
        res[name] = (not why, '; '.join(why), score, m); rows.append(dict(round=rnd, candidate=name, passed=not why, why='; '.join(why), sharpe_rel=sr, calmar_rel=cr, **m))
        print(f'R{rnd} {name:24s} pass={(not why)!s:5s} CAGR {m["cagr"]*100:5.1f}% Sh {m["sharpe"]:.2f} Cal {m["calmar"]:.2f} MDD {m["maxdd"]*100:5.1f}% cur DD {m["cur_dd"]*100:5.1f}% | {"; ".join(why)}', flush=True)
    passers = {k: v for k, v in res.items() if v[0] and not (k in POSTLOOK and nlook >= 2)}
    if not passers or len(adopted) >= 3: break
    best = max(passers, key=lambda k: passers[k][2]); adopted.append(best); nlook += best in POSTLOOK; running = {**running, **CAND[best]}; base = full(running)
    print(f'--> ADOPT {best}; running {running}; metrics', {k: round(float(v), 3) for k, v in base.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd')}, flush=True)
pd.DataFrame(rows).to_csv(f'{C.OUT}/overlay2_addone.csv', index=False); json.dump(dict(adopted=adopted, running={k: str(v) for k, v in running.items()}), open(f'{C.OUT}/overlay2_selected.json', 'w'), indent=1)
# all-in reference (user's list as pasted; S1 and S2 variants)
for nm, sel in (('ALL-IN with R1+A1', 'R1A1'), ('ALL-IN with R1+Ulcer', 'R1ULC')):
    m = full(dict(sel=sel, mkt_gate=True, fill='close', mkt_win=120, volgate=False, timestop=False, stop=0.12, vol_target=0.15, band=(200, 1000), cash_rate=0.065)); rows.append(dict(round=99, candidate=nm, passed=False, why='reference', **m)); print(nm, {k: round(float(v), 3) for k, v in m.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd', 'shA', 'shB', 'sh_l2', 'r25', 'cur_dd')}, flush=True)
pd.DataFrame(rows).to_csv(f'{C.OUT}/overlay2_addone.csv', index=False); print('ADOPTED:', adopted)
