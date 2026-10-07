"""Final, pre-declared candidate set for 'idle cash -> gold' on the three live-chassis momentum strategies.
Baseline for every comparison = idle cash in a 6.5% liquid fund (what a sensible live implementation does anyway)."""
import os, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from gold_overlay import daily_gold, LIQUID_FUND_ANNUAL
from analyze_gold_idle import stitched_metrics, block_boot_delta
rng = np.random.default_rng(77)
LF = (1 + LIQUID_FUND_ANNUAL) ** (1 / 252) - 1
mon = lambda s: ((1 + s).groupby([s.index.year, s.index.month]).prod() - 1)
yr = lambda s: ((1 + s).groupby(s.index.year).prod() - 1)

CANDIDATES = {   # name: (cap or None for uncapped, regimes in which gold is allowed)
    'U  all idle -> gold in weak markets (uncapped)': (None, ('BEAR', 'PANIC', 'HIGH_VOL')),
    'C1 cap 10% in weak markets':                      (0.10, ('BEAR', 'PANIC', 'HIGH_VOL')),
    'C2 cap 20% in weak markets':                      (0.20, ('BEAR', 'PANIC', 'HIGH_VOL')),
    'C3 cap 10% always':                               (0.10, ('BULL', 'BEAR', 'PANIC', 'HIGH_VOL')),
    'C4 cap 10% weak markets, BEAR/PANIC only':        (0.10, ('BEAR', 'PANIC')),
}
rows, yrows = [], []
for name in ('elendel', 'zenith', 'quad'):
    p = pickle.load(open(f'.cache/engine_{name}.pkl', 'rb'))
    w = p['executed_weights']; idx = w.index; net = p['net_returns'].reindex(idx); cr = p['daily_cash_rate']
    cash_w = (1 - w.sum(axis=1)).clip(lower=0); eq_part = net - cash_w * cr
    rg, _ = daily_gold(idx); gv = rg.notna(); reg = p['regime'].reindex(idx)
    drift = (rg[gv] - LF).mean(); window = gv & (idx >= '2003-01-01')

    def run(cap, regs, mult=1.0, cost=0.0015):
        rgm = rg - (1 - mult) * drift
        allowed = reg.isin(regs).astype(float)
        tgt = cash_w * allowed if cap is None else np.minimum(cash_w, cap) * allowed
        gp = np.minimum(tgt.where(gv, 0.0), cash_w)
        r = eq_part + (cash_w - gp) * LF + gp * rgm.fillna(0.0) - gp.diff().abs().fillna(0) * cost
        return r, gp
    base, _ = run(0.0, ())
    default_m = stitched_metrics(net[window]); base_m = stitched_metrics(base[window])
    rows.append(dict(strategy=name, variant='(engine default idle cash)', mult='-', cost=0, cagr=default_m['cagr'], sharpe=default_m['sharpe'], maxdd=default_m['maxdd'], calmar=default_m['calmar']))
    rows.append(dict(strategy=name, variant='BASELINE idle cash in 6.5% liquid fund', mult='-', cost=0, cagr=base_m['cagr'], sharpe=base_m['sharpe'], maxdd=base_m['maxdd'], calmar=base_m['calmar']))
    bm = mon(base[window])
    for vn, (cap, regs) in CANDIDATES.items():
        for mult in (1.0, 0.5, 0.0):
            for cost in ((0.0015, 0.003) if (vn.startswith('C1') and mult == 1.0) else (0.0015,)):
                r, gp = run(cap, regs, mult, cost); m = stitched_metrics(r[window])
                pS, pD, lo, hi = block_boot_delta(mon(r[window]).values, bm.values, reps=1500)
                seg = lambda rr, a, b: stitched_metrics(rr[(rr.index >= a) & (rr.index < b)])
                A1, B1_ = seg(r[window], '2000', '2011-06-01'), seg(r[window], '2015', '2100'); A0, B0 = seg(base[window], '2000', '2011-06-01'), seg(base[window], '2015', '2100')
                rows.append(dict(strategy=name, variant=vn, mult=mult, cost=cost, avg_gold_w=gp[window].mean(), pct_days_gold=(gp[window] > 0.005).mean(),
                                 cagr=m['cagr'], sharpe=m['sharpe'], maxdd=m['maxdd'], calmar=m['calmar'], d_cagr=m['cagr'] - base_m['cagr'], d_sharpe=m['sharpe'] - base_m['sharpe'],
                                 d_maxdd=m['maxdd'] - base_m['maxdd'], d_calmar=m['calmar'] - base_m['calmar'], d_worst_month=m['worst_month'] - base_m['worst_month'],
                                 dSharpe_A=A1['sharpe'] - A0['sharpe'], dSharpe_B=B1_['sharpe'] - B0['sharpe'], dMaxDD_A=A1['maxdd'] - A0['maxdd'], dMaxDD_B=B1_['maxdd'] - B0['maxdd'],
                                 P_dSharpe_pos=pS, P_dMaxDD_better=pD, dSharpe_lo=lo, dSharpe_hi=hi))
                if vn.startswith('C1') and mult == 1.0 and cost == 0.0015:
                    dy = yr(r[window]) - yr(base[window]); cnt = r[window].groupby(r[window].index.year).size()
                    for y_, v in dy.items():
                        if cnt[y_] > 100: yrows.append(dict(strategy=name, year=y_, d_return=v, base=yr(base[window])[y_], cand=yr(r[window])[y_]))
R = pd.DataFrame(rows); R.to_csv('results_final_gold_idle.csv', index=False, float_format='%.4f')
Y = pd.DataFrame(yrows); Y.to_csv('results_final_gold_idle_years.csv', index=False, float_format='%.4f')
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_colwidth', 48)
for name in ('elendel', 'zenith', 'quad'):
    x = R[R.strategy == name]
    b = x[x.variant.str.startswith('BASELINE')].iloc[0]; d0 = x[x.variant.str.startswith('(engine')].iloc[0]
    print(f'\n######## {name.upper()}   engine-default CAGR {d0.cagr:.3f} Sharpe {d0.sharpe:.2f} MaxDD {d0.maxdd:.3f} | LIQUID-FUND baseline CAGR {b.cagr:.3f} Sharpe {b.sharpe:.2f} MaxDD {b.maxdd:.3f} Calmar {b.calmar:.2f}')
    c = x[x.variant.str.match(r'^(U|C)')]
    print(c[['variant', 'mult', 'cost', 'avg_gold_w', 'd_cagr', 'd_sharpe', 'd_maxdd', 'd_calmar', 'd_worst_month', 'dSharpe_A', 'dSharpe_B', 'dMaxDD_A', 'dMaxDD_B', 'P_dSharpe_pos', 'P_dMaxDD_better']].round(3).to_string(index=False))
print('\n#### C1 (cap 10% in weak markets) - calendar-year difference vs liquid-fund baseline (percentage points)')
pv = Y.pivot(index='year', columns='strategy', values='d_return') * 100
print(pv.round(2).to_string()); print('share of years >= 0:', (pv >= -0.005).mean().round(2).to_dict(), ' worst year:', pv.min().round(2).to_dict())
