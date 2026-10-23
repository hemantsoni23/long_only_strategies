import os, sys, pickle, warnings, itertools
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine2 as SE2, faithful_replay as FR
from ovl_metrics import met
IDX = pd.read_parquet('../factor_research/.cache/index_data_close.parquet')['Nifty_500'].dropna().pct_change()
V11 = dict(sel='R1', mkt_gate=True, fill='close'); V12 = dict(sel='R1ULC', mkt_gate=True, fill='close', mkt_win=120, vol_target=0.15)
cache = {}
def run(cfg):
    k = str(sorted(cfg.items()))
    if k not in cache: cache[k] = SE2.run(**cfg)
    return cache[k]
def row(name, cfg):
    R = run(cfg); r = R['ret']; m = met(r); m['test'] = name; m['turn'] = R['turnover'] / (len(r[r.index >= '2005-01-01']) / 252)
    for lab, (a, b) in {'A': ('2005-01-01', '2012-12-31'), 'B': ('2013-01-01', None)}.items(): h = met(r, a, b); m['sh' + lab] = h['sharpe']; m['cal' + lab] = h['calmar']; m['mdd' + lab] = h['maxdd']
    m['r25'] = float((1 + r.loc['2025-01-01':]).prod() - 1); e = (1 + r[r.index >= '2005-01-01']).cumprod(); m['cur_dd'] = float((e / e.cummax() - 1).iloc[-1]); return m
rows = [row('v1.1 close fills', V11), row('v1.2 candidate (window120 + R1+Ulcer + vol target 15%)', V12), row('v1.1 OPEN fills (earlier reported)', {**V11, 'fill': 'open'}), row('v1.2 candidate OPEN fills', {**V12, 'fill': 'open'})]
# leave-one-out of the three adoptions
rows += [row('v1.2 without window120 (150)', {**V12, 'mkt_win': 150}), row('v1.2 without Ulcer (R1)', {**V12, 'sel': 'R1'}), row('v1.2 without vol target', {k: v for k, v in V12.items() if k != 'vol_target'})]
# plateau / sensitivity of each adopted element
for w in (100, 120, 150, 180, 200): rows.append(row(f'v1.2 gate window {w}', {**V12, 'mkt_win': w}))
for t in (0.12, 0.15, 0.20, 0.25): rows.append(row(f'v1.2 vol target {t}', {**V12, 'vol_target': t}))
for b in ((1, 500), (1, 1000), (250, 1000), (500, 1500)): rows.append(row(f'v1.2 band {b}', {**V12, 'band': b}))
for k, vals in (('top_n', (16, 24)), ('stop', (0.12, 0.18)), ('trail', (0.16, 0.24)), ('hold_rank', (32, 48))):
    for v in vals: rows.append(row(f'v1.2 param {k}={v}', {**V12, k: v}))
for name, kw in (('v1.2 no vol-state gate C3', dict(volgate=False)), ('v1.2 no time stop', dict(timestop=False)), ('v1.2 no M3', dict(m3_excl=False)), ('v1.2 no trend gate C6', dict(trend_gate=False)), ('v1.2 no hard/trail stops', dict(stop=9, trail=9))): rows.append(row(name, {**V12, **kw}))
for name, kw in (('stress cost 0.6%', dict(cost=0.006)), ('stress cost 1.0%', dict(cost=0.010)), ('stress delay 1d', dict(delay=1)), ('stress delay 2d', dict(delay=2)), ('stress cash 6.5% (separate)', dict(cash_rate=0.065)), ('stress cash 4% (separate)', dict(cash_rate=0.04)),
                 ('stress ADV cap Rs1cr', dict(adv_frac=0.05, C0=1e7)), ('stress ADV cap Rs5cr', dict(adv_frac=0.05, C0=5e7)), ('stress ADV cap Rs25cr', dict(adv_frac=0.05, C0=2.5e8))): rows.append(row(name, {**V12, **kw}))
T = pd.DataFrame(rows); T.to_csv(f'{C.OUT}/v12_validation.csv', index=False); pd.set_option('display.width', 250)
print(T[['test', 'cagr', 'sharpe', 'calmar', 'maxdd', 'shA', 'shB', 'calA', 'calB', 'r25', 'cur_dd', 'turn']].round(3).to_string(), flush=True)
# placebo with identical overlays (random picks; Ulcer/window/vol target all applied)
pl = [met(SE2.run(sel='random', seed=s, mkt_gate=True, fill='close', mkt_win=120, vol_target=0.15)['ret']) for s in range(100)]; PL = pd.DataFrame(pl); PL.to_csv(f'{C.OUT}/v12_placebo.csv', index=False)
m12 = rows[1]; print('placebo (same overlays) mean CAGR %.3f Sharpe %.2f Calmar %.2f | v1.2 %.3f %.2f %.2f | beaten: Sharpe %.2f CAGR %.2f Calmar %.2f' % (PL.cagr.mean(), PL.sharpe.mean(), PL.calmar.mean(), m12['cagr'], m12['sharpe'], m12['calmar'], (PL.sharpe < m12['sharpe']).mean(), (PL.cagr < m12['cagr']).mean(), (PL.calmar < m12['calmar']).mean()), flush=True)
# chunks
r11, r12 = run(V11)['ret'], run(V12)['ret']; ch = []
for nm, rr in (('v1.1', r11), ('v1.2', r12)): t = FR.chunk_stats(rr, pd.Period('2008-06', 'M') - 1, IDX); t['v'] = nm; ch.append(t)
CH = pd.concat(ch); CH.to_csv(f'{C.OUT}/v12_chunks.csv', index=False)
for v in ('cagr', 'sharpe', 'maxdd'): print(CH.pivot(index='v', columns='chunk', values=v).round(3).to_string())
yr = lambda rr: ((1 + rr[rr.index >= '2005-01-01']).groupby(rr[rr.index >= '2005-01-01'].index.year).prod() - 1)
Y = pd.DataFrame({'v1.1': yr(r11), 'v1.2': yr(r12)}); Y.to_csv(f'{C.OUT}/v12_yearly.csv'); print((Y * 100).round(1).T.to_string())
pickle.dump(dict(r11=r11, r12=r12, exp=run(V12)['expo'], mult=run(V12)['mult']), open(f'{C.CACHE}/v12_series.pkl', 'wb'))
print('avg multiplier when invested %.2f ; avg gross exposure %.2f' % (run(V12)['mult'][run(V12)['expo'] > 0].mean(), run(V12)['expo'][run(V12)['expo'] > 0].mean()))
tl = run(V12)['trades']; print(tl.groupby('reason').pnl_pct.agg(['size', 'mean']).round(2).to_string())
