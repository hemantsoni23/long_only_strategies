"""B1: faithful P&L by identical 36m chunks for Elendel/Zenith/Quad (existing faithful series) and HR/VCP (faithful re-booking), vs Nifty 500 price."""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, faithful_replay as F
IDX = pd.read_parquet('../factor_research/.cache/index_data_close.parquet')['Nifty_500'].dropna().pct_change()
R = pd.read_csv('/Users/hemantsoni/Documents/long_only_strategies/csm_value/output/faithful_engine_returns.csv', index_col=0, parse_dates=True)
series = {k: R[f'{k}_faithful'].astype(float) for k in ('elendel', 'zenith', 'quad')}
for w in ('hr', 'vcp'):
    d = pickle.load(open(f'{C.CACHE}/bt_{w}_cy0.0.pkl', 'rb')); series[w + '_faithful'], _ = F.replay(d['trades']); series[w + '_engine'] = d['net']
first = pd.Period('2008-06', 'M') - 1                      # common window start: signals from 2008-06 (all six strategies live)
rows = []
for k, r in series.items():
    t = F.chunk_stats(r, first, IDX); t['strategy'] = k; rows.append(t)
D = pd.concat(rows); D.to_csv(f'{C.OUT}/b1_pnl_chunks.csv', index=False)
pd.set_option('display.width', 220)
print(D.pivot(index='strategy', columns='chunk', values='cagr').round(3).to_string())
print(D.pivot(index='strategy', columns='chunk', values='sharpe').round(2).to_string())
print(D.pivot(index='strategy', columns='chunk', values='excess_nw_t').round(2).to_string())
print(D[D.strategy=='hr_faithful'][['chunk','bench_cagr']].to_string())
