"""
stage21_industry_loo_signal.py -- PHASE 1 of the industry-momentum book research: is the signal real once the stock's OWN return
is removed from its industry basket (leave-one-out), and does it pass the project's own pre-registered signal gate?

Why: stage18's baskets include the stock itself (weight 1/N), so part of its IC could just be the stock's own momentum.
other_momentum_ideas/industry_pond_research.py already used leave-one-out (LOO); this closes the same gap here, with the same
halves (2003-2012 / 2013-2026), Newey-West lag h-1, and placebo logic.

PRE-REGISTERED (written before the first run of this file)
  signal    LOO industry momentum, equal-weighted, Industry_clean (>=10 live U1 stocks, else Sector_clean), L in {1,3,6} months,
            skip 0; plus L=3 skip 1.  >=5 eligible peers required.  Reference: the stage18 full-basket winner (L3 skip0).
  universes U1_liquid1000, U3_top300, U7_midsmall_301_1000, U2_live_trend
  horizons  1/3/6/12 months (signal at month-end close, entry next close - evaluate.py convention)
  GATE G1   for the primary cell (LOO, L3 skip0) on U1 and on U7, horizon 3m AND 6m:
              (a) IC > 0 and NW-t >= 3 in BOTH halves (<=2012-12-31 and >=2013-01-01)
              (b) NW-t >= 2 in the 2015+ holdout
              (c) global-label-shuffle placebo: |NW-t| < 2 and real IC above the 95th percentile of the null
              (d) within-sector label shuffle: real IC above the 95th percentile of the null (industry labels add information
                  beyond the 11 sectors)
              (e) Playbook 2.6: top-2-year share of cumulative signed IC <= 50%; Playbook 2.3: >= 80% monotonic adjacent
                  decile pairs
  If G1 fails the LOO industry signal is closed at stock level and no book is built.
"""
import os
import pickle
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import load_panels                                                   # noqa: E402
from evaluate import rank_ic, nw_tstat, winsor_rows                             # noqa: E402
from factors import Ctx                                                        # noqa: E402
from industry_lib import IndustryEngine, permute_all, permute_within           # noqa: E402

RESULTS = os.path.join(HERE, 'results')
os.makedirs(RESULTS, exist_ok=True)
HALF_A_END = pd.Timestamp('2012-12-31')
HOLD_START = pd.Timestamp('2015-01-01')
HORIZONS = (1, 3, 6, 12)
N_PLACEBO = 60

st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
sig, U, FWD = st['sig'], st['U'], st['FWD']
UN = pickle.load(open(os.path.join(HERE, '.cache', 'extra_universes.pkl'), 'rb'))
UNIV = {'U1': U['U1_liquid1000'], 'U3': U['U3_top300'], 'U7': UN['U7_midsmall_301_1000'], 'U2trend': U['U2_live_trend']}

X = Ctx(load_panels())
eng = IndustryEngine(X, sig, U['U1_liquid1000'])

FACTORS = {
    'full_L3_skip0 (stage18 winner)': eng.build(L=3, skip=0),
    'LOO_L1_skip0': eng.build_loo(1, 0),
    'LOO_L3_skip0': eng.build_loo(3, 0),
    'LOO_L6_skip0': eng.build_loo(6, 0),
    'LOO_L3_skip1': eng.build_loo(3, 1),
}
PRIMARY = 'LOO_L3_skip0'


def ic_row(fr, mask, h):
    ic, _ = rank_ic(fr.where(mask), FWD[h].where(mask))
    ic = ic.dropna()
    a, b, hold = ic[ic.index <= HALF_A_END], ic[ic.index > HALF_A_END], ic[ic.index >= HOLD_START]
    lag = max(h - 1, 0)
    return ic, dict(ic=ic.mean(), icir=ic.mean() / ic.std(), hit=(ic > 0).mean(), t=nw_tstat(ic, lag), ic_A=a.mean(), t_A=nw_tstat(a, lag),
                    ic_B=b.mean(), t_B=nw_tstat(b, lag), ic_hold=hold.mean(), t_hold=nw_tstat(hold, lag), n=len(ic))


def decile_monotonic(fr, mask, h=3):
    F = fr.where(mask)
    R = winsor_rows(FWD[h].where(mask & F.notna()))
    pct = F.rank(axis=1, pct=True)
    dec = np.minimum((pct * 10).values, 9.999).astype(float)
    out = np.full((len(F), 10), np.nan)
    Rv = R.values
    for i in range(len(F)):
        d, r = dec[i], Rv[i]
        ok = np.isfinite(d) & np.isfinite(r)
        if ok.sum() < 100:
            continue
        di = d[ok].astype(int); rr = r[ok]
        for j in range(10):
            if (di == j).any():
                out[i, j] = rr[di == j].mean()
    m = np.nanmean(out, axis=0)
    spread = out[:, 9] - out[:, 0]
    return int((np.diff(m) > 0).sum()), m, nw_tstat(pd.Series(spread).dropna(), h - 1)


def top2_share(ic):
    by = ic.groupby(ic.index.year).sum()
    tot = by.sum()
    return float(by.nlargest(2).sum() / tot) if tot > 0 else np.nan


rows = []
ic_store = {}
for fname, fr in FACTORS.items():
    for uname, mask in UNIV.items():
        for h in HORIZONS:
            ic, r = ic_row(fr, mask, h)
            r.update(factor=fname, universe=uname, h=h)
            rows.append(r)
            ic_store[(fname, uname, h)] = ic
df = pd.DataFrame(rows)
df.to_csv(os.path.join(RESULTS, 'stage21_loo_signal.csv'), index=False, float_format='%.5f')

pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
print('\n=== IC by factor / universe / horizon  (A = <=2012, B = >=2013, hold = 2015+) ===')
show = ['factor', 'universe', 'h', 'ic', 'icir', 't', 'ic_A', 't_A', 'ic_B', 't_B', 'ic_hold', 't_hold']
print(df[df.h.isin([3, 6])][show].round(3).to_string(index=False))

# ───────── decile / concentration diagnostics for the primary cell ─────────
print('\n=== Playbook 2.3 (decile monotonicity, h=3) and 2.6 (top-2-year share of signed IC) for', PRIMARY, '===')
diag = []
for uname in ('U1', 'U7', 'U3', 'U2trend'):
    mono, means, sp_t = decile_monotonic(FACTORS[PRIMARY], UNIV[uname], 3)
    ic3 = ic_store[(PRIMARY, uname, 3)]
    ic6 = ic_store[(PRIMARY, uname, 6)]
    diag.append(dict(universe=uname, mono_pairs_of_9=mono, spread_top_minus_bottom_pct=(means[9] - means[0]) * 100, spread_nw_t=sp_t,
                     top2_share_h3=top2_share(ic3), top2_share_h6=top2_share(ic6)))
    print(uname, 'decile mean fwd 3m (%):', np.round(means * 100, 2))
dd = pd.DataFrame(diag); print(dd.round(3).to_string(index=False))
dd.to_csv(os.path.join(RESULTS, 'stage21_loo_diagnostics.csv'), index=False, float_format='%.4f')

# ───────── placebos for the primary cell ─────────
rng = np.random.default_rng(2026)
null_glob, null_within = [], []
for i in range(N_PLACEBO):
    ind_g, sec_g = permute_all(eng.ind_code, rng), permute_all(eng.sec_code, rng)
    f = eng.build_loo(3, 0, ind_code=ind_g, sec_code=sec_g)
    null_glob.append({(u, h): ic_row(f, UNIV[u], h)[1] for u in ('U1', 'U7') for h in (3, 6)})
    f = eng.build_loo(3, 0, ind_code=permute_within(eng.ind_code, eng.sec_code, rng))
    null_within.append({(u, h): ic_row(f, UNIV[u], h)[1] for u in ('U1', 'U7') for h in (3, 6)})
print('\n=== Placebos (LOO_L3_skip0): real vs %d global shuffles and %d within-sector shuffles ===' % (N_PLACEBO, N_PLACEBO))
pl_rows = []
for u in ('U1', 'U7'):
    for h in (3, 6):
        real = df[(df.factor == PRIMARY) & (df.universe == u) & (df.h == h)].iloc[0]
        g_ic = np.array([d[(u, h)]['ic'] for d in null_glob]); g_t = np.array([d[(u, h)]['t'] for d in null_glob])
        w_ic = np.array([d[(u, h)]['ic'] for d in null_within]); w_t = np.array([d[(u, h)]['t'] for d in null_within])
        pl_rows.append(dict(universe=u, h=h, real_ic=real.ic, real_t=real.t,
                            glob_mean_ic=g_ic.mean(), glob_p95_ic=np.quantile(g_ic, .95), glob_max_abs_t=np.abs(g_t).max(), glob_p=(g_ic >= real.ic).mean(),
                            within_mean_ic=w_ic.mean(), within_p95_ic=np.quantile(w_ic, .95), within_p=(w_ic >= real.ic).mean(),
                            within_mean_t=w_t.mean()))
pl = pd.DataFrame(pl_rows); print(pl.round(4).to_string(index=False))
pl.to_csv(os.path.join(RESULTS, 'stage21_loo_placebo.csv'), index=False, float_format='%.5f')

# ───────── gate verdict ─────────
print('\n=== GATE G1 (primary cell %s) ===' % PRIMARY)
ok_all = True
for u in ('U1', 'U7'):
    for h in (3, 6):
        r = df[(df.factor == PRIMARY) & (df.universe == u) & (df.h == h)].iloc[0]
        p = pl[(pl.universe == u) & (pl.h == h)].iloc[0]
        a = (r.ic > 0) and (r.t_A >= 3) and (r.t_B >= 3)
        b = r.t_hold >= 2
        c = (p.glob_max_abs_t < 2) and (r.ic > p.glob_p95_ic)
        d = r.ic > p.within_p95_ic
        dg = dd[dd.universe == u].iloc[0]
        e = (dg.top2_share_h3 <= 0.5 if h == 3 else dg.top2_share_h6 <= 0.5) and (dg.mono_pairs_of_9 >= 8)
        print(f'{u} h={h}: (a) halves t_A={r.t_A:.1f} t_B={r.t_B:.1f} -> {a} | (b) hold t={r.t_hold:.1f} -> {b} | (c) global placebo -> {c} '
              f'| (d) within-sector placebo -> {d} | (e) top2 share {dg.top2_share_h3 if h == 3 else dg.top2_share_h6:.2f}, mono {int(dg.mono_pairs_of_9)}/9 -> {e}')
        ok_all &= bool(a and b and c and d and e)
print('G1 VERDICT:', 'PASS' if ok_all else 'FAIL (see which sub-gate failed above; do NOT relax thresholds)')
