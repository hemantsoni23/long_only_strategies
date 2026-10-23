"""
stage24_new_factor_audit.py -- audit of NEW_MOMENTUM_FACTORS_AND_IDEAS.md (gates in NEW_MOMENTUM_AUDIT_PREREG.md).

Steps (each caches to results/ and .cache/):
  python3 stage24_new_factor_audit.py build      # new + control factor frames  -> .cache/stage24_factors.pkl
  python3 stage24_new_factor_audit.py gates      # G1..G5 on U2 (+U1/U3 robustness for G1)
  python3 stage24_new_factor_audit.py mech       # H5 (intraday/overnight cross-persistence), H6 (volume x momentum), year/period splits, correlations
  python3 stage24_new_factor_audit.py calib      # H1 Newey-West calibration with a persistent placebo factor
Nothing in Old_live_strategies/ is touched.
"""
import os, sys, pickle, time, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RES = os.path.join(HERE, 'results'); CACHE = os.path.join(HERE, '.cache')
os.makedirs(RES, exist_ok=True)

from evaluate import (forward_returns, composite, zscore, rank_ic, nw_tstat, winsor_rows, SPLIT)
from portfolio_lab import topn_book, stats

SPLIT_PREOPEN = pd.Timestamp('2010-10-31')   # NSE pre-open call auction introduced Oct-2010


def load_state():
    st = pickle.load(open(os.path.join(CACHE, 'state.pkl'), 'rb'))
    return st['sig'], st['F'], st['FWD'], st['U']


# ═════════════════════════════════════════════════════════════ BUILD
def step_build():
    from data import load_panels
    from factors import Ctx, rmean, rstd, rsum, rmax
    from evaluate_new_momentum_factors import build_new_factors
    t0 = time.time()
    sig, F, FWD, U = load_state()
    P = load_panels(); X = Ctx(P)
    assert (X.C.index.get_indexer(sig) >= 0).all()
    NF = build_new_factors(X, sig)                      # runner's own definitions (audit target)
    Cf = X.Cf; V = X.V

    def at(d): return d.reindex(sig).astype('float32')

    ovn = np.log(X.O / Cf.shift(1)).clip(-0.15, 0.15)
    intr = np.log(X.C / X.O).clip(-0.15, 0.15)
    NF['tot_ret_126_clip'] = at(rsum(intr + ovn, 126))
    NF['tot_ret_252_clip'] = at(rsum(intr + ovn, 252))
    NF['intraday_252'] = at(rsum(intr, 252))
    NF['neg_overnight_252'] = at(-rsum(ovn, 252))
    NF['mom_12_1'] = at(Cf.shift(21) / Cf.shift(252) - 1.0)
    NF['volsurge_21_252'] = at(rmean(V, 21) / rmean(V, 252).replace(0, np.nan))
    NF['volsurge_63_252'] = at(rmean(V, 63) / rmean(V, 252).replace(0, np.nan))
    NF['ldv_63'] = at(np.log(X.DV.rolling(63, min_periods=40).median().replace(0, np.nan)))
    # B4 option B: abnormal-volume up-jump reaction
    adv = rmean(V, 63).shift(1)
    cond = (V > 3 * adv) & (X.r > 0.03)
    jump = X.r.where(cond, 0.0).where(Cf.notna()).rolling(126, min_periods=100).sum()
    NF['jump_react_126'] = at(jump)

    # B7: true quadratic fit on log price, 126d (orthogonal-polynomial closed form, evaluated at month-ends only)
    w = 126
    tau = np.arange(w, dtype='float64'); p1 = tau - tau.mean(); p2 = p1 ** 2 - (p1 ** 2).mean()
    lc = np.log(Cf)
    pos = lc.index.get_indexer(sig)
    N = lc.shape[1]
    beta = np.full((len(sig), N), np.nan); gam = np.full_like(beta, np.nan); r2 = np.full_like(beta, np.nan)
    LV = lc.values
    for k, p in enumerate(pos):
        if p < w:
            continue
        Y = LV[p - w + 1:p + 1]
        ok = ~np.isnan(Y).any(axis=0)
        if not ok.any():
            continue
        Yc = Y[:, ok]; Ym = Yc.mean(axis=0)
        b = (p1 @ (Yc - Ym)) / (p1 @ p1)
        g = (p2 @ Yc) / (p2 @ p2)
        sst = ((Yc - Ym) ** 2).sum(axis=0)
        beta[k, ok] = b; gam[k, ok] = g
        r2[k, ok] = np.where(sst > 0, (b ** 2) * (p1 @ p1) / sst, np.nan)
    cols = lc.columns
    NF['quad_gamma_126'] = pd.DataFrame(gam, index=sig, columns=cols).astype('float32')
    vel = pd.DataFrame(beta * r2, index=sig, columns=cols).astype('float32')
    NF['vel_r2_126'] = vel
    NF['lin_beta_126'] = pd.DataFrame(beta, index=sig, columns=cols).astype('float32')
    pickle.dump(NF, open(os.path.join(CACHE, 'stage24_factors.pkl'), 'wb'))
    print(f'[build] {len(NF)} frames cached in {time.time()-t0:.0f}s: {sorted(NF)}')


def load_factors():
    sig, F, FWD, U = load_state()
    NF = pickle.load(open(os.path.join(CACHE, 'stage24_factors.pkl'), 'rb'))
    ALL = dict(F); ALL.update(NF)       # runner/new frames take precedence (they are the audit target) ...
    for k in ('a3_rs_high', 'q5_126', 'a1_52wh', 'q5_189'):
        ALL[k] = F[k]                   # ... except the live-baseline legs, which must stay the original definitions
    return sig, ALL, FWD, U


# ═════════════════════════════════════════════════════════════ helpers
def ic_series(Fm, R, min_n=30):
    ic, _ = rank_ic(Fm, R, min_n)
    return ic.dropna()


def tstat(x, h):
    return nw_tstat(x, max(h - 1, 0))


def nonoverlap_t(ic, h):
    """mean over the h possible month-offsets of the plain t-stat on every h-th monthly IC"""
    ts = []
    for off in range(h):
        s = ic.iloc[off::h].dropna()
        if len(s) > 8 and s.std() > 0:
            ts.append(s.mean() / (s.std() / np.sqrt(len(s))))
    return float(np.mean(ts)) if ts else np.nan


def resid_ic(Fm, base, R):
    """IC (vs R) of factor percentile-rank after cross-sectional residualisation on base percentile-rank"""
    fp = Fm.rank(axis=1, pct=True); bp = base.rank(axis=1, pct=True)
    fz = fp.sub(fp.mean(axis=1), axis=0); bz = bp.sub(bp.mean(axis=1), axis=0)
    beta = (fz * bz).sum(axis=1) / (bz ** 2).sum(axis=1)
    resid = fz.sub(bz.mul(beta, axis=0))
    ic, _ = rank_ic(resid, R)
    return ic.dropna()


def decile_excess(Fm, R, q=0.9):
    valid = Fm.notna() & R.notna()
    Rw = winsor_rows(R.where(valid))
    ex = Rw.sub(Rw.mean(axis=1), axis=0)
    pct = Fm.where(valid).rank(axis=1, pct=True)
    return ex.where(pct > q).mean(axis=1).dropna()


def split_means(s):
    return s[s.index <= SPLIT].mean(), s[s.index > SPLIT].mean()


def cs_rank_corr(A, B, mask):
    ic, _ = rank_ic(A.where(mask), B.where(mask))
    return ic.mean()


# ═════════════════════════════════════════════════════════════ GATES
CANDIDATES = [
    # (id, name, control, kind)
    ('B1', 'quiet_mom_12_1', 'mom_12_1'),
    ('B1', 'volsurge_21_252', None),
    ('B2', 'delta_beta_252', None),
    ('B3', 'intra_over_126', 'tot_ret_126_clip'),
    ('B3', 'intra_over_252', 'tot_ret_252_clip'),
    ('B3', 'intraday_252', 'tot_ret_252_clip'),
    ('B3', 'neg_overnight_252', 'tot_ret_252_clip'),
    ('B6', 'ulcer_mom_252', 'mom_12_1'),
    ('B6', 'low_ulcer_252', None),
    ('B7', 'trend_accel_63', None),
    ('B7', 'quad_gamma_126', None),
    ('B7', 'convex_mom', 'vel_r2_126'),
    ('B4', 'jump_react_126', None),
    # controls reported for reference
    ('ctl', 'mom_12_1', None), ('ctl', 'mom_12_0', None), ('ctl', 'tot_ret_252_clip', None), ('ctl', 'vel_r2_126', None),
    ('ctl', 'mom_12_1_sharpe', None),
]
BLENDS = [('B2m', f'mom12_1+{l}*dbeta', 'mom_12_1', 'delta_beta_252', l, 'mom_12_1') for l in (0.5, 1.0)]


def step_gates():
    sig, ALL, FWD, U = load_factors()
    out = []
    ic_store = {}
    for uname in ('U2_live_trend', 'U1_liquid1000', 'U3_top300'):
        mask = U[uname]
        R3 = FWD[3].where(mask)
        elen = composite(ALL, ['a3_rs_high', 'q5_126'], mask)
        zen = composite(ALL, ['a1_52wh', 'q5_189'], mask)
        # frames incl. blends
        frames = {}
        for gid, name, ctl in CANDIDATES:
            if name == 'convex_mom':
                frames[name] = zscore(ALL['vel_r2_126'].where(mask)) + zscore(ALL['quad_gamma_126'].where(mask))
            else:
                frames[name] = ALL[name].where(mask)
        for gid, name, f1, f2, lam, ctl in BLENDS:
            frames[name] = zscore(ALL[f1].where(mask)) + lam * zscore(ALL[f2].where(mask))
        meta = {name: (gid, ctl) for gid, name, ctl in CANDIDATES}
        for gid, name, f1, f2, lam, ctl in BLENDS:
            meta[name] = (gid, ctl)
        for name, Fm in frames.items():
            gid, ctl = meta[name]
            row = dict(universe=uname, id=gid, factor=name, control=ctl, avg_n=Fm.notna().sum(axis=1).mean())
            ic3 = ic_series(Fm, R3)
            ic_store[(uname, name)] = ic3
            d, o = ic3[ic3.index <= SPLIT], ic3[ic3.index > SPLIT]
            row.update(ic3=ic3.mean(), icir3=ic3.mean() / ic3.std(), t3=tstat(ic3, 3), ic3_disc=d.mean(), ic3_hold=o.mean(),
                       t3_hold=tstat(o, 3), t3_disc=tstat(d, 3))
            for h in (6, 12):
                ich = ic_series(Fm, FWD[h].where(mask))
                row[f'ic{h}'] = ich.mean(); row[f't{h}_nw'] = tstat(ich, h); row[f't{h}_nonoverlap'] = nonoverlap_t(ich, h)
            if uname == 'U2_live_trend':
                # G2 increment vs TRUE baselines
                for bn, base in (('elen', elen), ('zen', zen)):
                    ri = resid_ic(Fm, base, R3)
                    row[f'inc_ic3_{bn}'] = ri.mean(); row[f'inc_t3_{bn}'] = tstat(ri, 3)
                    row[f'corr_{bn}'] = cs_rank_corr(Fm, base, mask)
                # runner's (mislabelled) baseline for H2
                q5 = composite(ALL, ['q5_126'], mask)
                row['corr_q5only'] = cs_rank_corr(Fm, q5, mask)
                ri = resid_ic(Fm, q5, R3); row['inc_ic3_q5only'] = ri.mean(); row['inc_t3_q5only'] = tstat(ri, 3)
                # G3 paired vs control
                if ctl is not None:
                    cF = (zscore(ALL[ctl].where(mask)) if ctl in ALL else None)
                    ic_c = ic_series(cF, R3)
                    diff = (ic3 - ic_c).dropna()
                    row['ctl_ic3'] = ic_c.mean(); row['g3_diff'] = diff.mean(); row['g3_t'] = tstat(diff, 3)
                # G4 tail
                t10 = decile_excess(Fm, R3, 0.9); t20 = decile_excess(Fm, R3, 0.8)
                dd, hh = split_means(t10)
                row.update(top10_ex3=t10.mean(), top10_t=tstat(t10, 3), top10_disc=dd, top10_hold=hh, top20_ex3=t20.mean(), top20_t=tstat(t20, 3))
                # standalone book
                bk = topn_book(Fm, mask, FWD[1])
                n = bk['net']; sd, sh, sa = stats(n[n.index <= SPLIT]), stats(n[n.index > SPLIT]), stats(n)
                row.update(book_sharpe=sa.get('sharpe'), book_sharpe_disc=sd.get('sharpe'), book_sharpe_hold=sh.get('sharpe'),
                           book_cagr=sa.get('cagr'), book_turn=bk['turnover'].mean())
            out.append(row)
        print(f'[gates] {uname} frames done', flush=True)
        if uname == 'U2_live_trend':
            # G5 add-on books
            g5 = []
            bases = {'elen': elen, 'zen': zen}
            base_stats = {}
            for bn, base in bases.items():
                bk = topn_book(base, mask, FWD[1]); n = bk['net']
                base_stats[bn] = (stats(n[n.index <= SPLIT]).get('sharpe'), stats(n[n.index > SPLIT]).get('sharpe'), stats(n).get('sharpe'))
                g5.append(dict(base=bn, factor='(base alone)', w=0, sharpe_disc=base_stats[bn][0], sharpe_hold=base_stats[bn][1], sharpe_all=base_stats[bn][2],
                               turnover=bk['turnover'].mean()))
            for name, Fm in frames.items():
                if meta[name][0] == 'ctl' and name not in ('mom_12_1', 'tot_ret_252_clip'):
                    continue
                for bn, base in bases.items():
                    for w in (0.5, 1.0):
                        sc = zscore(base) + w * zscore(Fm)
                        bk = topn_book(sc, mask, FWD[1]); n = bk['net']
                        sdd, shh, saa = stats(n[n.index <= SPLIT]).get('sharpe'), stats(n[n.index > SPLIT]).get('sharpe'), stats(n).get('sharpe')
                        b0 = base_stats[bn]
                        g5.append(dict(base=bn, factor=name, w=w, sharpe_disc=sdd, sharpe_hold=shh, sharpe_all=saa,
                                       d_disc=sdd - b0[0], d_hold=shh - b0[1], d_all=saa - b0[2], turnover=bk['turnover'].mean(),
                                       beats_both=bool(sdd > b0[0] and shh > b0[1])))
                print(f'[G5] {name} done', flush=True)
            pd.DataFrame(g5).to_csv(os.path.join(RES, 'stage24_g5_books.csv'), index=False, float_format='%.4f')
    df = pd.DataFrame(out)
    df.to_csv(os.path.join(RES, 'stage24_gates_raw.csv'), index=False, float_format='%.4f')
    pickle.dump(ic_store, open(os.path.join(CACHE, 'stage24_ic_store.pkl'), 'wb'))
    print('[gates] saved')


# ═════════════════════════════════════════════════════════════ MECHANISM TESTS
def step_mech():
    from data import load_panels
    from factors import Ctx, rsum
    sig, ALL, FWD, U = load_factors()
    P = load_panels(); X = Ctx(P)
    out_lines = []

    def P_(s=''):
        print(s, flush=True); out_lines.append(s)

    # ---- H5: intraday/overnight cross-persistence
    Cf = X.Cf
    ovn = np.log(X.O / Cf.shift(1)).clip(-0.15, 0.15).fillna(0.0)
    intr = np.log(X.C / X.O).clip(-0.15, 0.15).fillna(0.0)
    idx = X.C.index; pos = idx.get_indexer(sig); entry = pos + 1; ok = entry < len(idx)

    def fwd_sum(S, h):
        L = S.cumsum().values
        arr = np.full((len(sig), S.shape[1]), np.nan)
        for k in range(len(sig) - h):
            if ok[k] and ok[k + h]:
                arr[k] = L[entry[k + h]] - L[entry[k]]
        return pd.DataFrame(arr, index=sig, columns=S.columns)

    h = 3
    FI, FO = fwd_sum(intr, h), fwd_sum(ovn, h)
    FT = FWD[3]
    PI = ALL['intraday_252']; PO = -ALL['neg_overnight_252']       # PO = +sum(overnight)
    P_('=== H5. Past intraday/overnight (252d sums) vs FUTURE 3m components (rank IC, NW t)  [Lou-Polk-Skouras-style cross-persistence]')
    rows = []
    for uname in ('U1_liquid1000', 'U2_live_trend', 'U3_top300'):
        m = U[uname]
        for pn, pf in (('past_intraday', PI), ('past_overnight', PO), ('intra_over_252', ALL['intra_over_252']), ('tot_ret_252', ALL['tot_ret_252_clip'])):
            for fn, fr in (('fut_intraday', FI), ('fut_overnight', FO), ('fut_total', FT)):
                ic = ic_series(pf.where(m), fr.where(m))
                pre = ic[ic.index <= SPLIT_PREOPEN]; post = ic[ic.index > SPLIT_PREOPEN]
                rows.append(dict(universe=uname, past=pn, future=fn, ic=ic.mean(), t=tstat(ic, h), ic_pre2010=pre.mean(), ic_post2010=post.mean(),
                                 t_post=tstat(post, h), n_pre=len(pre), n_post=len(post)))
    h5 = pd.DataFrame(rows); h5.to_csv(os.path.join(RES, 'stage24_h5_intraday_overnight.csv'), index=False, float_format='%.4f')
    P_(h5.round(3).to_string(index=False))

    # ---- period / year split for key factors
    P_('\n=== Pre/post 2010-10 (NSE pre-open call auction) and by calendar year, IC(3m), U2 and U3')
    store = pickle.load(open(os.path.join(CACHE, 'stage24_ic_store.pkl'), 'rb'))
    rows = []
    for fn in ('intra_over_252', 'intra_over_126', 'delta_beta_252', 'quiet_mom_12_1', 'ulcer_mom_252', 'trend_accel_63', 'quad_gamma_126', 'jump_react_126', 'mom_12_1', 'tot_ret_252_clip'):
        for un in ('U2_live_trend', 'U3_top300'):
            ic = store.get((un, fn))
            if ic is None: continue
            pre = ic[ic.index <= SPLIT_PREOPEN]; post = ic[ic.index > SPLIT_PREOPEN]
            yr = ic.groupby(ic.index.year).mean()
            rows.append(dict(factor=fn, universe=un, ic_pre=pre.mean(), ic_post=post.mean(), t_post=tstat(post, 3),
                             yrs_pos=(yr > 0).mean(), best_year_share=(yr.clip(lower=0).max() / yr.clip(lower=0).sum()),
                             ic_2019_26=ic[ic.index >= '2019-01-01'].mean(), t_2019_26=tstat(ic[ic.index >= '2019-01-01'], 3)))
    ps = pd.DataFrame(rows); ps.to_csv(os.path.join(RES, 'stage24_period_split.csv'), index=False, float_format='%.4f')
    P_(ps.round(3).to_string(index=False))

    # ---- H6: Lee-Swaminathan 2D sort: momentum quintile x volume tercile (independent sorts)
    P_('\n=== H6. 12-1 momentum quintile x volume tercile, mean 3m / 6m excess return (%), universes U1 (broad) and U2 (live pool)')
    rows = []
    for uname in ('U1_liquid1000', 'U2_live_trend'):
        m = U[uname]
        mom = ALL['mom_12_1'].where(m)
        for vn in ('volsurge_21_252', 'volsurge_63_252', 'ldv_63'):
            vol = ALL[vn].where(m)
            rm = mom.rank(axis=1, pct=True); rv = vol.rank(axis=1, pct=True)
            mq = np.ceil(rm * 5).clip(1, 5); vt = np.ceil(rv * 3).clip(1, 3)
            for hh in (3, 6, 12):
                R = FWD[hh].where(m & mom.notna() & vol.notna())
                ex = winsor_rows(R).sub(winsor_rows(R).mean(axis=1), axis=0)
                cell = {}
                for q in (1, 5):
                    for v in (1, 2, 3):
                        s = ex.where((mq == q) & (vt == v)).mean(axis=1).dropna()
                        cell[(q, v)] = s
                for q in (1, 5):
                    diff = (cell[(q, 1)] - cell[(q, 3)]).dropna()      # low-volume minus high-volume
                    rows.append(dict(universe=uname, volvar=vn, h=hh, mom_quintile=q,
                                     V1_low=cell[(q, 1)].mean() * 100, V2=cell[(q, 2)].mean() * 100, V3_high=cell[(q, 3)].mean() * 100,
                                     V1_minus_V3=diff.mean() * 100, t=tstat(diff, hh),
                                     disc=diff[diff.index <= SPLIT].mean() * 100, hold=diff[diff.index > SPLIT].mean() * 100))
    h6 = pd.DataFrame(rows); h6.to_csv(os.path.join(RES, 'stage24_h6_volume_momentum.csv'), index=False, float_format='%.4f')
    P_(h6.round(2).to_string(index=False))

    # ---- what are these factors really? mean cross-sectional rank correlations (U2)
    P_('\n=== Correlation map (mean cross-sectional Spearman, U2) of the candidates with known factors')
    m = U['U2_live_trend']
    known = ['mom_12_1', 'mom_12_0', 'mom_12_1_sharpe', 'a1_52wh', 'q5_126', 'lowvol_252', 'low_ulcer_252', 'low_beta_252', 'down_resilience_252',
             'up_capture_252', 'tot_ret_252_clip', 'ldv_63']
    cand = ['quiet_mom_12_1', 'delta_beta_252', 'intra_over_252', 'intraday_252', 'neg_overnight_252', 'ulcer_mom_252', 'trend_accel_63', 'quad_gamma_126',
            'vel_r2_126', 'jump_react_126']
    cm = pd.DataFrame({k: {c: cs_rank_corr(ALL[c], ALL[k], m) for c in cand} for k in known})
    cm.to_csv(os.path.join(RES, 'stage24_corr_map.csv'), float_format='%.3f')
    P_(cm.round(2).to_string())
    open(os.path.join(RES, 'stage24_mech_log.txt'), 'w').write('\n'.join(out_lines))


# ═════════════════════════════════════════════════════════════ NW CALIBRATION
def step_calib(ndraw=200, rho=0.9, seed=7):
    sig, ALL, FWD, U = load_factors()
    m = U['U2_live_trend']
    rng = np.random.default_rng(seed)
    shape = m.shape
    res = {h: [] for h in (3, 6, 12)}
    res_no = {h: [] for h in (6, 12)}
    Rm = {h: FWD[h].where(m) for h in res}
    for d in range(ndraw):
        # persistent placebo: AR(1) over months per stock, so rank autocorrelation ~ rho
        eps = rng.standard_normal(shape)
        x = np.empty(shape); x[0] = eps[0]
        for k in range(1, shape[0]):
            x[k] = rho * x[k - 1] + np.sqrt(1 - rho ** 2) * eps[k]
        Fm = pd.DataFrame(x, index=m.index, columns=m.columns).where(m)
        for h in res:
            ic = ic_series(Fm, Rm[h])
            res[h].append(tstat(ic, h))
            if h in res_no:
                res_no[h].append(nonoverlap_t(ic, h))
        if (d + 1) % 50 == 0:
            print(f'[calib] {d+1}/{ndraw}', flush=True)
    rows = []
    for h in res:
        t = np.array(res[h])
        rows.append(dict(h=h, n_draws=ndraw, rho=rho, nw_t_mean=t.mean(), nw_t_sd=t.std(), fp_rate_abs_t_ge_2=(abs(t) >= 2).mean(),
                         fp_rate_abs_t_ge_3=(abs(t) >= 3).mean(),
                         nonoverlap_t_sd=(np.std(res_no[h]) if h in res_no else np.nan),
                         nonoverlap_fp_ge_2=((abs(np.array(res_no[h])) >= 2).mean() if h in res_no else np.nan)))
    df = pd.DataFrame(rows); df.to_csv(os.path.join(RES, 'stage24_h1_nw_calibration.csv'), index=False, float_format='%.4f')
    print(df.round(3).to_string(index=False))


if __name__ == '__main__':
    step = sys.argv[1] if len(sys.argv) > 1 else 'build'
    {'build': step_build, 'gates': step_gates, 'mech': step_mech, 'calib': step_calib}[step]()
