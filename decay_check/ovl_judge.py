import numpy as np, pandas as pd
from ovl_metrics import met
import strategy_engine2 as SE2
def full(cfg):
    R = SE2.run(**cfg); r = R['ret']; m = met(r); yrs = len(r[r.index >= '2005-01-01']) / 252; m['turn'] = R['turnover'] / yrs
    hA, hB = met(r, '2005-01-01', '2012-12-31'), met(r, '2013-01-01'); m['shA'], m['shB'], m['ddA'], m['ddB'], m['cagrA'], m['cagrB'] = hA['sharpe'], hB['sharpe'], hA['maxdd'], hB['maxdd'], hA['cagr'], hB['cagr']
    m['sh_l2'] = met(r, '2020-06-01', '2026-06-30')['sharpe']; m['sh_c6'] = met(SE2.run(**{**cfg, 'cost': 0.006})['ret'])['sharpe']; m['r25'] = float((1 + r.loc['2025-01-01':]).prod() - 1); return m
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
    return why
