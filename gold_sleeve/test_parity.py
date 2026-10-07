"""Parity test: GoldSleevePV must reproduce the research series (factor_research/results/gold_rules_monthly.csv, rule G5) exactly,
and be near-identical when run standalone on the raw ETF file (own trading calendar)."""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'factor_research'))
from gold_sleeve_strategy import GoldSleevePV, load_etf_close
from gold_data import load_gold

ETF_FOLDER = '/Users/hemantsoni/Documents/upstox_data_folder/etf_ohlcv_data'
research = pd.read_csv(os.path.join(HERE, '..', 'factor_research', 'results', 'gold_rules_monthly.csv'), index_col=0, parse_dates=True)
ref = research['G5 persistence x vol-target']

# (a) research calendar (Nifty trading days, ffill limit 5)
gold_cal, *_ = load_gold()
sa = GoldSleevePV(gold_cal); bt = sa.backtest()   # full chain (same start as the research run), compared on common months
j = pd.concat([bt.net_return, ref], axis=1, keys=['class', 'research']).dropna()
print('(a) research calendar: months compared', len(j), '| max abs diff', float((j['class'] - j['research']).abs().max()))
assert len(j) >= 150 and (j['class'] - j['research']).abs().max() < 1e-6, 'PARITY FAILED on research calendar'   # research csv is stored with 6 decimals

# (b) standalone on the raw ETF file (gold's own trading days)
raw = load_etf_close(os.path.join(ETF_FOLDER, 'GOLDBEES.csv'))
sb = GoldSleevePV(raw); bt2 = sb.backtest()
k = pd.concat([bt2.net_return, ref], axis=1, keys=['standalone', 'research']).dropna()
print('(b) standalone file : months compared', len(k), '| max abs diff %.4f | mean abs diff %.5f | corr %.4f' % ((k.standalone - k.research).abs().max(), (k.standalone - k.research).abs().mean(), k.corr().iloc[0, 1]))
m1, m2 = GoldSleevePV.metrics(k.standalone), GoldSleevePV.metrics(k.research)   # same months
print('    standalone CAGR %.3f Sharpe %.3f MaxDD %.3f  | research CAGR %.3f Sharpe %.3f MaxDD %.3f' % (m1['cagr'], m1['sharpe'], m1['max_drawdown'], m2['cagr'], m2['sharpe'], m2['max_drawdown']))
assert k.corr().iloc[0, 1] > 0.98 and (k.standalone - k.research).abs().max() < 0.03, 'standalone run drifts from research'
assert abs(m1['sharpe'] - m2['sharpe']) < 0.05 and abs(m1['cagr'] - m2['cagr']) < 0.01, 'standalone metrics drift from research'
# (c) gap handling: no month in the 2011-01..2014-12 gap is ever used
used = bt2.index[(bt2.index > '2011-01-31') & (bt2.index < '2014-12-01')]
print('(c) months inside the data gap that were used:', len(used)); assert len(used) == 0
print('ALL PARITY CHECKS PASSED')
