import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from gold_overlay import *
from analyze_gold_idle import stitched_metrics, block_boot_delta   # reuse (module import re-runs main body? guard below)
rng = np.random.default_rng(33); HOLD = pd.Timestamp('2015-01-01')
mon = lambda s: ((1 + s).groupby([s.index.year, s.index.month]).prod() - 1)
rows = []; epis = []
for name in ('elendel', 'zenith'):
    payload = pickle.load(open(f'.cache/engine_{name}.pkl', 'rb'))
    idx = payload['executed_weights'].index; w = payload['executed_weights']; net = payload['net_returns'].reindex(idx)
    cash_rate = payload['daily_cash_rate']; cash_w = (1 - w.sum(axis=1)).clip(lower=0)
    eq_part = net - cash_w * cash_rate
    rg, close = daily_gold(idx); gvalid = rg.notna()
    lf = (1 + LIQUID_FUND_ANNUAL) ** (1 / 252) - 1
    reg = payload['regime'].reindex(idx); weak = reg.isin(['BEAR', 'PANIC', 'HIGH_VOL']).astype(float); bearp = reg.isin(['BEAR', 'PANIC']).astype(float)
    drift = (rg[gvalid] - lf).mean(); rgn = rg - drift
    def build(gold_pos_target, gold_ret):
        gp = gold_pos_target.where(gvalid, 0.0).clip(lower=0); gp = np.minimum(gp, cash_w)      # gold can only use idle cash
        idle_ret = ((cash_w - gp) * lf + gp * gold_ret.fillna(0.0)) / cash_w.replace(0, np.nan)
        r = eq_part + (cash_w - gp) * lf + gp * gold_ret.fillna(0.0) - gp.diff().abs().fillna(0) * 0.0015
        return r, gp
    window = gvalid & (idx >= '2003-01-01')
    base, _ = build(pd.Series(0.0, index=idx), rg)           # liquid-fund baseline (fair for both strategies)
    variants = {}
    for cap in (0.05, 0.10, 0.15, 0.20):
        variants[f'cap{int(cap*100)}% always'] = pd.Series(cap, index=idx)
    for cap in (0.10, 0.20, 0.30):
        variants[f'cap{int(cap*100)}% only in BEAR/PANIC/HIGH_VOL'] = weak * cap
        variants[f'cap{int(cap*100)}% only in BEAR/PANIC'] = bearp * cap
    bm = mon(base[window])
    for k, tgt in variants.items():
        for kind, gr in (('real', rg), ('neutral', rgn)):
            r, gp = build(tgt, gr)
            m = stitched_metrics(r[window]); mb = stitched_metrics(base[window])
            a, b = mon(r[window]), bm
            pS, pD, lo, hi = block_boot_delta(a.values, b.values, reps=1500)
            seg = lambda rr, lo_, hi_: stitched_metrics(rr[(rr.index >= lo_) & (rr.index < hi_)])
            ra, rb = r[window], base[window]
            A_, B_ = seg(ra, '2000-01-01', '2011-06-01'), seg(ra, '2015-01-01', '2100-01-01'); A0, B0 = seg(rb, '2000-01-01', '2011-06-01'), seg(rb, '2015-01-01', '2100-01-01')
            rows.append(dict(strategy=name, variant=k, gold=kind, avg_gold_w=gp[window].mean(), cagr=m['cagr'], d_cagr=m['cagr'] - mb['cagr'], sharpe=m['sharpe'], d_sharpe=m['sharpe'] - mb['sharpe'],
                             maxdd=m['maxdd'], d_maxdd=m['maxdd'] - mb['maxdd'], worst_month=m['worst_month'], d_worst_month=m['worst_month'] - mb['worst_month'],
                             dSharpe_A=A_['sharpe'] - A0['sharpe'], dSharpe_B=B_['sharpe'] - B0['sharpe'], dMaxDD_A=A_['maxdd'] - A0['maxdd'], dMaxDD_B=B_['maxdd'] - B0['maxdd'],
                             P_dSharpe_pos=pS, P_dMaxDD_better=pD, base_cagr=mb['cagr'], base_sharpe=mb['sharpe'], base_maxdd=mb['maxdd']))
    # drawdown episodes of the liquid-fund baseline: what did gold do?
    rb = base[window]; eq = (1 + rb).cumprod(); dd = eq / eq.cummax() - 1
    ep = []; in_dd = False
    for d, v in dd.items():
        if v < -1e-9 and not in_dd: start = d; in_dd = True
        if v >= -1e-9 and in_dd:
            seg_ = dd[start:d]; ep.append((seg_.idxmin(), seg_.min(), start, d)); in_dd = False
    if in_dd: seg_ = dd[start:]; ep.append((seg_.idxmin(), seg_.min(), start, dd.index[-1]))
    for trough, depth, s0, e0 in sorted(ep, key=lambda t: t[1])[:6]:
        pk = eq[:trough].idxmax()
        g_ret = (1 + rg[(rg.index > pk) & (rg.index <= trough) & gvalid]).prod() - 1
        idle = cash_w[(cash_w.index > pk) & (cash_w.index <= trough)].mean()
        epis.append(dict(strategy=name, peak=pk.date(), trough=trough.date(), book_dd=depth, days=(trough - pk).days, gold_return_peak_to_trough=g_ret, avg_idle_cash=idle,
                         weak_regime_share=weak[(weak.index > pk) & (weak.index <= trough)].mean()))
R = pd.DataFrame(rows); R.to_csv('results_gold_caps.csv', index=False, float_format='%.4f')
E = pd.DataFrame(epis); E.to_csv('results_gold_drawdown_episodes.csv', index=False, float_format='%.4f')
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_colwidth', 40)
for name in ('elendel', 'zenith'):
    x = R[(R.strategy == name) & (R.gold == 'real')].set_index('variant')
    print(f'\n#### {name.upper()} capped gold from idle cash vs liquid-fund baseline (CAGR {x.base_cagr.iloc[0]:.3f}, Sharpe {x.base_sharpe.iloc[0]:.2f}, MaxDD {x.base_maxdd.iloc[0]:.3f})  -- REAL gold')
    print(x[['avg_gold_w', 'd_cagr', 'd_sharpe', 'd_maxdd', 'd_worst_month', 'dSharpe_A', 'dSharpe_B', 'dMaxDD_A', 'dMaxDD_B', 'P_dSharpe_pos', 'P_dMaxDD_better']].round(3).to_string())
    y = R[(R.strategy == name) & (R.gold == 'neutral')].set_index('variant')
    print(f'  -- NEUTRAL gold (mean return = liquid fund): pure diversification effect')
    print(y[['avg_gold_w', 'd_cagr', 'd_sharpe', 'd_maxdd', 'P_dSharpe_pos', 'P_dMaxDD_better']].round(3).to_string())
print('\n#### Worst drawdowns of the liquid-fund-baseline books and what gold did')
print(E.round(3).to_string(index=False))
