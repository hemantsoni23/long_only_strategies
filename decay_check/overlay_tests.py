"""Addendum 5: add-one tests of momentum-book overlays on Aegis v1.0 + pre-registered forward selection."""
import os, sys, json, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine2 as SE2
def met(r, a='2005-01-01', b=None):
    r = r.loc[a:b] if b else r.loc[a:]; r = r[r.index >= r[r != 0].index.min()]; yrs = len(r) / 252; eq = (1 + r).cumprod(); dd = eq / eq.cummax() - 1
    ep, cur = [], 0.0
    for v in dd.values:
        if v < 0: cur = min(cur, v)
        else:
            if cur < -0.02: ep.append(cur)
            cur = 0.0
    if cur < -0.02: ep.append(cur)
    m12 = (1 + r).rolling(252).apply(np.prod, raw=True) - 1; cagr = eq.iloc[-1] ** (1 / yrs) - 1
    return dict(cagr=cagr, sharpe=r.mean() / r.std() * np.sqrt(252), maxdd=dd.min(), calmar=cagr / abs(dd.min()), avg_dd=float(np.mean(ep)) if ep else 0.0, stab=float(m12.std()))
def full(cfg):
    R = SE2.run(**cfg); r = R['ret']; m = met(r); yrs = len(r[r.index >= '2005-01-01']) / 252
    m['turn'] = R['turnover'] / yrs; hA, hB = met(r, '2005-01-01', '2012-12-31'), met(r, '2013-01-01'); m['shA'] = hA['sharpe']; m['shB'] = hB['sharpe']; m['calA'] = hA['calmar']; m['calB'] = hB['calmar']
    m['sh_l2'] = met(r, '2020-06-01', '2026-06-30')['sharpe']; m['sh_c6'] = met(SE2.run(**{**cfg, 'cost': 0.006})['ret'])['sharpe']; m['cur_dd'] = float((((1 + r[r.index >= '2005-01-01']).cumprod()) / ((1 + r[r.index >= '2005-01-01']).cumprod()).cummax() - 1).iloc[-1])
    return m
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
    return len(why) == 0, '; '.join(why), (sr + cr) / 2, sr, cr
CAND = {'K1 crash guard': dict(crash_guard=True), 'K2 vol target 15%': dict(vol_target=0.15), 'K3 regime leverage': dict(regime_lev=True), 'K4 market trend gate (SMA150)': dict(mkt_gate=True),
        'K5 corr guard': dict(corr_guard=True), 'K6 loss-scaled cooldown': dict(loss_cooldown=True), 'K7 abs-momentum gate': dict(abs_mom=True), 'K8 falling-knife gate': dict(falling_knife=True),
        'K9 inverse-vol sizing': dict(invvol=True), 'K11 ATR chandelier': dict(chandelier=True), 'K12 min-hold 5d': dict(minhold=True), 'K13 quarterly entries': dict(quarterly=True)}
running = {'sel': 'R1'}; base = full(running); log = []; rows = []; adopted = []
print('BASELINE', {k: round(v, 3) for k, v in base.items()}, flush=True)
k10 = full({**running, 'cash_rate': 0.065}); print('K10 cash yield 6.5% (separate):', {k: round(v, 3) for k, v in k10.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd')}, flush=True)
for rnd in range(1, 5):
    res = {}
    for name, kw in CAND.items():
        if name in adopted: continue
        cfg = {**running, **kw}; m = full(cfg); ok, why, score, sr, cr = judge(m, base); res[name] = (ok, why, score, m)
        rows.append(dict(round=rnd, candidate=name, passed=ok, why=why, sharpe_rel=sr, calmar_rel=cr, **m)); print(f'R{rnd} {name:32s} pass={ok!s:5s} CAGR {m["cagr"]*100:5.1f}% Sh {m["sharpe"]:.2f} Cal {m["calmar"]:.2f} MDD {m["maxdd"]*100:5.1f}%  | {why}', flush=True)
    passers = {k: v for k, v in res.items() if v[0]}
    if not passers or len(adopted) >= 3: break
    best = max(passers, key=lambda k: passers[k][2]); adopted.append(best); running = {**running, **CAND[best]}; base = full(running)
    print(f'--> ADOPT {best}; running config now {running}; metrics', {k: round(v, 3) for k, v in base.items() if k in ('cagr', 'sharpe', 'calmar', 'maxdd')}, flush=True)
pd.DataFrame(rows).to_csv(f'{C.OUT}/overlay_addone.csv', index=False); json.dump(dict(adopted=adopted, config={k: (v if not isinstance(v, np.generic) else v.item()) for k, v in running.items()}), open(f'{C.OUT}/overlay_selected.json', 'w'), indent=1, default=str)
print('ADOPTED:', adopted)
