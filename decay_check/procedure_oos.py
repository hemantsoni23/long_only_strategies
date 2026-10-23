"""Out-of-sample test of the SELECTION PROCEDURE: choose overlays using one half of history only, evaluate the chosen set on the other half."""
import os, sys, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine2 as SE2
from ovl_metrics import met
BASE = dict(sel='R1', mkt_gate=True, fill='close')
CAND = {'S1': dict(sel='R1A1'), 'S2': dict(sel='R1ULC'), 'F1': dict(volgate=False), 'F2': dict(mkt_win=120), 'F3': dict(timestop=False), 'F4': dict(stop=0.12), 'P2': dict(vol_target=0.15), 'P3': dict(band=(200, 1000))}
PLAT = {'F2': [dict(mkt_win=100), dict(mkt_win=150)], 'F4': [dict(stop=0.10), dict(stop=0.15)], 'P3': [dict(band=(150, 1000)), dict(band=(250, 1000))]}; POST = {'F1', 'F2', 'F3', 'F4', 'P3'}
cache = {}
def R(cfg):
    k = str(sorted(cfg.items()))
    if k not in cache: cache[k] = SE2.run(**cfg)
    return cache[k]
def win(cfg, a, b):
    r = R(cfg)['ret']; return met(r, a, b), R(cfg)
def sel_metrics(cfg, a, b, sub):
    m, Rr = win(cfg, a, b); m['sh_c6'] = met(R({**cfg, 'cost': 0.006})['ret'], a, b)['sharpe']; m['turn'] = Rr['turnover'] / (len(Rr['ret'].loc[a:b]) / 252)
    m['s1'] = met(Rr['ret'], *sub[0])['sharpe']; m['s2'] = met(Rr['ret'], *sub[1])['sharpe']; m['l3'] = met(Rr['ret'], sub[2][0], sub[2][1])['sharpe']; return m
def judge(c, b):
    sr, cr = c['sharpe'] / b['sharpe'] - 1, c['calmar'] / b['calmar'] - 1; why = []
    if not (cr >= 0.10 or sr >= 0.05): why.append('a')
    if sr < -0.15 or cr < -0.15 or c['stab'] > 1.2 * b['stab'] or abs(c['avg_dd']) > 1.2 * abs(b['avg_dd']) or c['turn'] > 1.25 * b['turn']: why.append('b')
    if c['s1'] < 0.95 * b['s1'] or c['s2'] < 0.95 * b['s2']: why.append('c')
    if c['l3'] < b['l3']: why.append('d')
    if c['sh_c6'] < b['sh_c6']: why.append('e')
    return why, (sr + cr) / 2
out = []
for name, (a, b), sub, (oa, ob) in (('select on 2005-2012, test on 2013-2026', ('2005-01-01', '2012-12-31'), (('2005-01-01', '2008-12-31'), ('2009-01-01', '2012-12-31'), ('2010-01-01', '2012-12-31')), ('2013-01-01', None)),
                                    ('select on 2013-2026, test on 2005-2012', ('2013-01-01', None), (('2013-01-01', '2019-12-31'), ('2020-01-01', None), ('2023-07-01', None)), ('2005-01-01', '2012-12-31'))):
    running = dict(BASE); base = sel_metrics(running, a, b, sub); adopted = []; nlook = 0
    for rnd in range(4):
        res = {}
        for k, kw in CAND.items():
            if k in adopted: continue
            m = sel_metrics({**running, **kw}, a, b, sub); why, sc = judge(m, base)
            if k in PLAT and not why:
                for nb in PLAT[k]:
                    if sel_metrics({**running, **nb}, a, b, sub)['sharpe'] < base['sharpe']: why.append('plateau')
            res[k] = (not why, sc)
        passers = {k: v for k, v in res.items() if v[0] and not (k in POST and nlook >= 2)}
        if not passers or len(adopted) >= 3: break
        best = max(passers, key=lambda k: passers[k][1]); adopted.append(best); nlook += best in POST; running = {**running, **CAND[best]}; base = sel_metrics(running, a, b, sub)
    mo, _ = win(running, oa, ob); m0, _ = win(BASE, oa, ob); mi, _ = win(running, a, b); mi0, _ = win(BASE, a, b)
    out.append(dict(procedure=name, adopted=','.join(adopted) or '(none)', IS_sharpe_v11=mi0['sharpe'], IS_sharpe_new=mi['sharpe'], OOS_sharpe_v11=m0['sharpe'], OOS_sharpe_new=mo['sharpe'], OOS_calmar_v11=m0['calmar'], OOS_calmar_new=mo['calmar'],
                    OOS_cagr_v11=m0['cagr'], OOS_cagr_new=mo['cagr'], OOS_mdd_v11=m0['maxdd'], OOS_mdd_new=mo['maxdd']))
    print(out[-1], flush=True)
pd.DataFrame(out).to_csv(f'{C.OUT}/procedure_oos.csv', index=False)
