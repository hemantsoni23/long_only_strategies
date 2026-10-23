"""Validation battery for the new wrapper strategy (Addendum 4 Part 4). Everything faithful-booked by construction."""
import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine as SE, faithful_replay as FR
IDX = pd.read_parquet('../factor_research/.cache/index_data_close.parquet')['Nifty_500'].dropna().pct_change()
def metrics(r, a='2005-01-01', b=None):
    r = r.loc[a:b] if b else r.loc[a:]; r = r[r.index >= r[r != 0].index.min()]; yrs = len(r) / 252; eq = (1 + r).cumprod(); dd = eq / eq.cummax() - 1
    # avg drawdown depth over >2% episodes
    ep, cur = [], 0.0
    for v in dd.values:
        if v < 0: cur = min(cur, v)
        else:
            if cur < -0.02: ep.append(cur)
            cur = 0.0
    if cur < -0.02: ep.append(cur)
    m12 = (1 + r).rolling(252).apply(np.prod, raw=True) - 1
    cagr = eq.iloc[-1] ** (1 / yrs) - 1; mdd = dd.min()
    return dict(cagr=cagr, sharpe=r.mean() / r.std() * np.sqrt(252), maxdd=mdd, calmar=cagr / abs(mdd) if mdd else np.nan, avg_dd_depth=float(np.mean(ep)) if ep else 0.0, stability=float(m12.std()))
out = {}
base = SE.run(sel='R1'); out['base'] = base; M0 = metrics(base['ret'])
print('BASE', {k: round(v, 3) for k, v in M0.items()}, 'turnover/yr', round(base['turnover'] / (len(base['ret']) / 252), 1), flush=True)
# 1) wrapper bake-off + placebo
rows = []
for sel in ('R1', 'ELEN', 'ZEN', 'BASE'):
    R = SE.run(sel=sel); m = metrics(R['ret']); m.update(name=f'wrapper[{sel}]', trades=len(R['trades'])); rows.append(m); out[f'sel_{sel}'] = R
pl = []
for s in range(100):
    R = SE.run(sel='random', seed=s); m = metrics(R['ret']); pl.append(m)
PL = pd.DataFrame(pl); out['placebo'] = PL
rows.append(dict(name='placebo mean (100 random draws)', **PL.mean().to_dict())); rows.append(dict(name='placebo 95th pct', **PL.quantile(0.95).to_dict()))
pd.DataFrame(rows).to_csv(f'{C.OUT}/aegis_bakeoff.csv', index=False); print(pd.DataFrame(rows).round(3).to_string(), flush=True)
print('R1 Sharpe beats placebo percentile:', (PL.sharpe < M0['sharpe']).mean(), ' CAGR pct:', (PL.cagr < M0['cagr']).mean(), flush=True)
# 2) Stage 3: bands, params, ablations
rows = []
for b in ((1, 500), (1, 1000), (250, 1000), (500, 1500)):
    R = SE.run(band=b); m = metrics(R['ret']); m.update(test=f'band {b}'); rows.append(m)
for k, vals in (('top_n', (16, 24)), ('stop', (0.12, 0.18)), ('trail', (0.16, 0.24)), ('hold_rank', (32, 48))):
    for v in vals:
        kw = {k: v}; R = SE.run(**kw); m = metrics(R['ret']); m.update(test=f'param {k}={v}'); rows.append(m)
ab = {'no extension filter (C1)': dict(ext=False), 'no vol-state gate (C3)': dict(volgate=False), 'no time stop (C4)': dict(timestop=False), 'equal sizing (C5)': dict(risk_size=False),
      'no trend gate (C6)': dict(trend_gate=False), 'no M3 exclusion': dict(m3_excl=False), 'no hard/trail stops': dict(stop=9, trail=9), 'no stops, no time stop': dict(stop=9, trail=9, timestop=False)}
for k, kw in ab.items():
    R = SE.run(**kw); m = metrics(R['ret']); m.update(test='ablation ' + k, turnover_yr=R['turnover'] / (len(R['ret']) / 252)); rows.append(m)
rows.insert(0, dict(test='BASELINE', turnover_yr=base['turnover'] / (len(base['ret']) / 252), **M0))
S3 = pd.DataFrame(rows); S3.to_csv(f'{C.OUT}/aegis_stage3.csv', index=False); print(S3.round(3).to_string(), flush=True)
# 3) stress
rows = []
for name, kw in (('cost 0.6%/leg', dict(cost=0.006)), ('cost 1.0%/leg', dict(cost=0.010)), ('resting stop fills', dict(resting_stop=True)), ('cash earns 6.5%', dict(cash_rate=0.065)),
                 ('ADV cap 5%, start Rs1cr', dict(adv_frac=0.05, C0=1e7)), ('ADV cap 5%, start Rs5cr', dict(adv_frac=0.05, C0=5e7)), ('ADV cap 5%, start Rs25cr', dict(adv_frac=0.05, C0=2.5e8)),
                 ('entry gap cancel off', dict(gap_cancel=9))):
    R = SE.run(**kw); m = metrics(R['ret']); m.update(test=name); rows.append(m)
pd.DataFrame(rows).to_csv(f'{C.OUT}/aegis_stress.csv', index=False); print(pd.DataFrame(rows).round(3).to_string(), flush=True)
# 4) Stage 4 bidirectional split
r = base['ret']; rows = []
for name, (isa, isb), (osa, osb) in (('Split A', ('2005-01-01', '2012-12-31'), ('2013-01-01', None)), ('Split B', ('2013-01-01', None), ('2005-01-01', '2012-12-31'))):
    mi, mo = metrics(r, isa, isb), metrics(r, osa, osb)
    rows.append(dict(split=name, IS_sharpe=mi['sharpe'], OOS_sharpe=mo['sharpe'], sharpe_ratio=mo['sharpe'] / mi['sharpe'], IS_calmar=mi['calmar'], OOS_calmar=mo['calmar'], calmar_ratio=mo['calmar'] / mi['calmar'],
                     IS_cagr=mi['cagr'], OOS_cagr=mo['cagr'], cagr_ratio=mo['cagr'] / mi['cagr'], IS_mdd=mi['maxdd'], OOS_mdd=mo['maxdd'], mdd_ratio=mo['maxdd'] / mi['maxdd']))
S4 = pd.DataFrame(rows); S4.to_csv(f'{C.OUT}/aegis_stage4.csv', index=False); print(S4.round(3).T.to_string(), flush=True)
# 5) chunk P&L vs Nifty and vs live faithful books
R = pd.read_csv('/Users/hemantsoni/Documents/long_only_strategies/csm_value/output/faithful_engine_returns.csv', index_col=0, parse_dates=True)
series = {'AEGIS(R1)': base['ret'], 'wrapper[ELEN]': out['sel_ELEN']['ret'], 'wrapper[ZEN]': out['sel_ZEN']['ret'], 'wrapper[BASE]': out['sel_BASE']['ret'], 'live Elendel': R['elendel_faithful'], 'live Zenith': R['zenith_faithful'], 'live Quad': R['quad_faithful']}
rows = []
for k, s in series.items():
    t = FR.chunk_stats(s, pd.Period('2008-06', 'M') - 1, IDX); t['strategy'] = k; rows.append(t)
CH = pd.concat(rows); CH.to_csv(f'{C.OUT}/aegis_chunks.csv', index=False)
print(CH.pivot(index='strategy', columns='chunk', values='cagr').round(3).to_string()); print(CH.pivot(index='strategy', columns='chunk', values='sharpe').round(2).to_string()); print(CH.pivot(index='strategy', columns='chunk', values='maxdd').round(2).to_string())
print(CH[CH.strategy == 'AEGIS(R1)'][['chunk', 'bench_cagr', 'excess_nw_t']].round(3).to_string())
pickle.dump({k: v for k, v in out.items() if k in ('base', 'placebo')}, open(f'{C.CACHE}/aegis_out.pkl', 'wb'))
