import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine2 as SE2, faithful_replay as FR
from overlay_tests import met
IDX = pd.read_parquet('../factor_research/.cache/index_data_close.parquet')['Nifty_500'].dropna().pct_change()
V = dict(sel='R1', mkt_gate=True); B = dict(sel='R1')
def row(name, cfg):
    R = SE2.run(**cfg); m = met(R['ret']); m['test'] = name; m['turn'] = R['turnover'] / (len(R['ret'][R['ret'].index >= '2005-01-01']) / 252); return m, R
rows = []
m11, R11 = row('v1.1 (K4)', V); m10, R10 = row('v1.0', B); rows += [m10, m11]
# K4 window sensitivity and near-miss stacks (not tuned; sensitivity only)
import strategy_engine2 as S2
X = S2.extras(); orig = X['sma150'].copy(); bench = pd.Series(X['bench'])
for w in (120, 180):
    X['sma150'] = bench.rolling(w).mean().values; m, _ = row(f'K4 window {w}d', V); rows.append(m)
X['sma150'] = orig
for name, kw in (('v1.1 + K1 crash guard (near miss)', dict(crash_guard=True)), ('v1.1 + K2 vol target (near miss)', dict(vol_target=0.15)), ('v1.1 + K10 cash 6.5%', dict(cash_rate=0.065)), ('v1.1 + K1 + K2', dict(crash_guard=True, vol_target=0.15))):
    m, _ = row(name, {**V, **kw}); rows.append(m)
# Stage 3
for b in ((1, 500), (1, 1000), (250, 1000), (500, 1500)): m, _ = row(f'band {b}', {**V, 'band': b}); rows.append(m)
for k, vals in (('top_n', (16, 24)), ('stop', (0.12, 0.18)), ('trail', (0.16, 0.24)), ('hold_rank', (32, 48))):
    for v in vals: m, _ = row(f'param {k}={v}', {**V, k: v}); rows.append(m)
for k, kw in {'without K4 (=v1.0)': dict(mkt_gate=False), 'no extension C1': dict(ext=False), 'no vol-state gate C3': dict(volgate=False), 'no time stop C4': dict(timestop=False), 'equal sizing C5': dict(risk_size=False),
              'no trend gate C6': dict(trend_gate=False), 'no M3': dict(m3_excl=False), 'no hard/trail stops': dict(stop=9, trail=9)}.items():
    m, _ = row('ablation ' + k, {**V, **kw}); rows.append(m)
for name, kw in (('cost 0.6%', dict(cost=0.006)), ('cost 1.0%', dict(cost=0.010)), ('resting stop', dict(resting_stop=True)), ('delay 1d', dict(delay=1)), ('delay 2d', dict(delay=2)), ('cash 6.5%', dict(cash_rate=0.065)),
                 ('ADV cap Rs1cr', dict(adv_frac=0.05, C0=1e7)), ('ADV cap Rs5cr', dict(adv_frac=0.05, C0=5e7)), ('ADV cap Rs25cr', dict(adv_frac=0.05, C0=2.5e8))):
    m, _ = row('stress ' + name, {**V, **kw}); rows.append(m)
T = pd.DataFrame(rows); T.to_csv(f'{C.OUT}/v11_validation.csv', index=False); pd.set_option('display.width', 250); print(T[['test', 'cagr', 'sharpe', 'calmar', 'maxdd', 'avg_dd', 'stab', 'turn']].round(3).to_string(), flush=True)
# Stage 4
r = R11['ret']; s4 = []
for name, (ia, ib), (oa, ob) in (('Split A', ('2005-01-01', '2012-12-31'), ('2013-01-01', None)), ('Split B', ('2013-01-01', None), ('2005-01-01', '2012-12-31'))):
    mi, mo = met(r, ia, ib), met(r, oa, ob); s4.append(dict(split=name, IS_sharpe=mi['sharpe'], OOS_sharpe=mo['sharpe'], sharpe_ratio=mo['sharpe'] / mi['sharpe'], calmar_ratio=mo['calmar'] / mi['calmar'], cagr_ratio=mo['cagr'] / mi['cagr'], mdd_ratio=mo['maxdd'] / mi['maxdd']))
S4 = pd.DataFrame(s4); S4.to_csv(f'{C.OUT}/v11_stage4.csv', index=False); print(S4.round(3).to_string(), flush=True)
# placebo with the same gate
pl = [met(SE2.run(sel='random', seed=s, mkt_gate=True)['ret']) for s in range(100)]; PL = pd.DataFrame(pl); PL.to_csv(f'{C.OUT}/v11_placebo.csv', index=False)
print('v1.1 placebo mean CAGR %.3f Sharpe %.2f | v1.1 %.3f / %.2f | beats %.2f of draws on Sharpe, %.2f on CAGR | Calmar beats %.2f' % (PL.cagr.mean(), PL.sharpe.mean(), m11['cagr'], m11['sharpe'], (PL.sharpe < m11['sharpe']).mean(), (PL.cagr < m11['cagr']).mean(), (PL.calmar < m11['calmar']).mean()), flush=True)
# chunks + recent
ch = FR.chunk_stats(r, pd.Period('2008-06', 'M') - 1, IDX); ch0 = FR.chunk_stats(R10['ret'], pd.Period('2008-06', 'M') - 1, IDX); ch['v'] = 'v1.1'; ch0['v'] = 'v1.0'; CH = pd.concat([ch0, ch]); CH.to_csv(f'{C.OUT}/v11_chunks.csv', index=False)
print(CH.pivot(index='v', columns='chunk', values='cagr').round(3).to_string()); print(CH.pivot(index='v', columns='chunk', values='sharpe').round(2).to_string()); print(CH.pivot(index='v', columns='chunk', values='maxdd').round(2).to_string())
w = lambda rr, a, b: (1 + rr.loc[a:b]).prod() - 1
for nm, rr in (('v1.0', R10['ret']), ('v1.1', r)): 
    e = (1 + rr[rr.index >= '2005-01-01']).cumprod(); print(nm, '2025-01..2026-07: %.3f' % w(rr, '2025-01-01', '2026-07-31'), ' 2024: %.3f' % w(rr, '2024-01-01', '2024-12-31'), ' current DD %.3f' % (e / e.cummax() - 1).iloc[-1], ' avg exposure %.2f' % R11['expo'][R11['expo'] > 0].mean() if nm == 'v1.1' else '')
yr = (1 + r[r.index >= '2005-01-01']).groupby(r[r.index >= '2005-01-01'].index.year).prod() - 1; yr0 = (1 + R10['ret'][R10['ret'].index >= '2005-01-01']).groupby(R10['ret'][R10['ret'].index >= '2005-01-01'].index.year).prod() - 1
pd.DataFrame({'v1.0': yr0, 'v1.1': yr}).to_csv(f'{C.OUT}/v11_yearly.csv'); print(pd.DataFrame({'v1.0': yr0, 'v1.1': yr}).round(3).T.to_string())
tl = R11['trades']; print(tl.groupby('reason').pnl_pct.agg(['size', 'mean']).round(2).to_string())
pickle.dump(dict(r11=R11['ret'], r10=R10['ret']), open(f'{C.CACHE}/v11_series.pkl', 'wb'))
