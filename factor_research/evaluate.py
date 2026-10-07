"""
evaluate.py -- factor evaluation engine.

Conventions (kept compatible with Old_live_strategies/*_backtest.py calculate_ic):
  * monthly cross-sectional Spearman rank IC, ICIR = mean(IC)/std(IC), hit rate = % months IC>0
  * forward return horizons in months: 1,2,3,6,12   (factor-decay curve = "horizon period")
Added on top (needed because the live books hold only ~15 names):
  * Newey-West t-stat (lag h-1) -- monthly IC at h>1 uses overlapping returns
  * top-quintile / top-decile excess return, top-quintile win-rate vs median, % months top beats market
  * discovery (<=2014) vs holdout (>=2015) split -- rank on discovery, confirm on holdout
  * incremental IC after removing the rank component explained by the live Elendel signal

Execution realism: signal at close of month-end t, entry at close of t+1 (one-day lag, same as the
live system's T+1 fill), exit at close of t+1 after the h-th following month-end.  Forward returns
are built from cleaned daily returns (jump days outside [-40%,+300%] counted as 0; delisted names
stay flat at their last price rather than being dropped).
"""
import numpy as np
import pandas as pd

from factors import rmean, rmax

HORIZONS = (1, 2, 3, 6, 12)
SPLIT = pd.Timestamp('2014-12-31')


# ───────────────────────── forward returns & universes ─────────────────────────
def forward_returns(X, sig, horizons=HORIZONS):
    Cff = X.C.ffill()
    r = Cff.pct_change(fill_method=None)
    r = r.where((r > -0.40) & (r < 3.00), 0.0).fillna(0.0)
    L = np.log1p(r).cumsum()
    idx = X.C.index
    pos = idx.get_indexer(sig)
    entry = pos + 1
    ok = entry < len(idx)
    out = {}
    Lv = L.values
    cols = L.columns
    for h in horizons:
        arr = np.full((len(sig), L.shape[1]), np.nan)
        for k in range(len(sig) - h):
            if ok[k] and ok[k + h]:
                arr[k] = np.expm1(Lv[entry[k + h]] - Lv[entry[k]])
        out[h] = pd.DataFrame(arr, index=sig, columns=cols)
    return out


def build_universes(X, sig):
    Cf = X.Cf
    have = Cf.reindex(sig).notna()
    price_ok = Cf.reindex(sig) > 20
    med_dv = X.DV.rolling(63, min_periods=21).median().reindex(sig)
    rank = med_dv.rank(axis=1, ascending=False, method='min')
    circ = ((X.H == X.L) & X.H.notna()).astype('float64').rolling(63, min_periods=1).sum().reindex(sig) <= 5
    U1 = have & price_ok & (rank <= 1000) & circ
    trend = (Cf > rmean(Cf, 200)).reindex(sig)
    U2 = U1 & trend
    U3 = have & price_ok & (rank <= 300) & circ
    m3 = rmax(X.r, 21).reindex(sig)
    m3r = m3.where(U2).rank(axis=1, pct=True)
    U2z = U2 & (m3r <= 0.8)
    return {'U1_liquid1000': U1, 'U2_live_trend': U2, 'U2z_zenith_univ': U2z, 'U3_top300': U3}


# ───────────────────────── helpers ─────────────────────────
def zscore(df):
    return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)


def nw_tstat(x, lag):
    x = np.asarray(pd.Series(x).dropna(), dtype='float64')
    n = len(x)
    if n < 12:
        return np.nan
    m = x.mean()
    d = x - m
    g0 = (d * d).mean()
    s = g0
    for j in range(1, min(lag, n - 1) + 1):
        w = 1 - j / (lag + 1)
        s += 2 * w * (d[j:] * d[:-j]).mean()
    se = np.sqrt(max(s, 1e-18) / n)
    return m / se


def rank_ic(F, R, min_n=30):
    """row-wise Spearman between F and R on their joint-valid set"""
    valid = F.notna() & R.notna()
    fr = F.where(valid).rank(axis=1)
    rr = R.where(valid).rank(axis=1)
    fm = fr.sub(fr.mean(axis=1), axis=0)
    rm = rr.sub(rr.mean(axis=1), axis=0)
    num = (fm * rm).sum(axis=1)
    den = np.sqrt((fm ** 2).sum(axis=1) * (rm ** 2).sum(axis=1))
    ic = num / den
    return ic.where(valid.sum(axis=1) >= min_n), valid.sum(axis=1)


def cs_corr(A, B, min_n=30):
    ic, _ = rank_ic(A, B, min_n)
    return ic


def winsor_rows(R, lo=0.01, hi=0.99):
    q_lo = R.quantile(lo, axis=1)
    q_hi = R.quantile(hi, axis=1)
    return R.clip(lower=q_lo, upper=q_hi, axis=0)


def composite(F, names, mask, extra_mask=None):
    parts = [zscore(F[n].where(mask)) for n in names]
    s = parts[0]
    for p in parts[1:]:
        s = s + p
    return s


def ic_stats(ic, h, tag=''):
    ic = ic.dropna()
    if len(ic) < 12:
        return {}
    mu, sd = ic.mean(), ic.std()
    return {f'ic{tag}_{h}': mu, f'icir{tag}_{h}': mu / sd if sd > 0 else np.nan,
            f'hit{tag}_{h}': (ic > 0).mean(), f't{tag}_{h}': nw_tstat(ic, max(h - 1, 0))}


# ───────────────────────── per-factor evaluation ─────────────────────────
def evaluate_factor(name, F, mask, FWD, base_rank=None, horizons=HORIZONS, detail=True):
    """F: monthly factor frame (dates x tickers); mask: universe bool frame; FWD: {h: fwd return frame}"""
    Fm = F.where(mask)
    row = {'factor': name}
    row['avg_n'] = float(Fm.notna().sum(axis=1).mean())
    ic_store = {}
    quint = {}
    for h in horizons:
        R = FWD[h].where(mask)
        ic, n = rank_ic(Fm, R)
        ic_store[h] = ic
        row.update(ic_stats(ic, h))
        d = ic[ic.index <= SPLIT]; o = ic[ic.index > SPLIT]
        row.update(ic_stats(d, h, '_disc')); row.update(ic_stats(o, h, '_hold'))
        if detail and h in (1, 3, 6, 12):
            valid = Fm.notna() & R.notna()
            Rv = R.where(valid)
            Rw = winsor_rows(Rv)
            ex = Rw.sub(Rw.mean(axis=1), axis=0)
            pct = Fm.where(valid).rank(axis=1, pct=True)
            top = pct > 0.8; top10 = pct > 0.9; bot = pct <= 0.2
            med = Rv.median(axis=1)
            t20 = ex.where(top).mean(axis=1); b20 = ex.where(bot).mean(axis=1); t10 = ex.where(top10).mean(axis=1)
            beat = (Rv.gt(med, axis=0)).where(top & valid).mean(axis=1)
            ok = t20.notna()
            row[f'top20_ex_{h}'] = t20[ok].mean()
            row[f'top10_ex_{h}'] = t10[ok].mean()
            row[f'bot20_ex_{h}'] = b20[ok].mean()
            row[f'spread_{h}'] = (t20 - b20)[ok].mean()
            row[f'top20_winmed_{h}'] = beat[ok].mean()
            row[f'top_beats_mkt_{h}'] = (t20[ok] > 0).mean()
            if h in (3, 12):   # annualised-ish top-quintile edge for readability
                row[f'top20_ex_ann_{h}'] = (1 + t20[ok].mean()) ** (12 / h) - 1
    # peak horizon
    icm = {h: row.get(f'ic_{h}', np.nan) for h in horizons}
    iciri = {h: row.get(f'icir_{h}', np.nan) for h in horizons}
    row['peak_h_ic'] = max(icm, key=lambda k: (icm[k] if np.isfinite(icm[k]) else -9))
    row['peak_h_icir'] = max(iciri, key=lambda k: (iciri[k] if np.isfinite(iciri[k]) else -9))
    # calendar-year consistency @3m
    ic3 = ic_store[3].dropna()
    if len(ic3):
        yr = ic3.groupby(ic3.index.year).mean()
        row['yrs_pos_ic3'] = (yr > 0).mean()
        row['n_years'] = len(yr)
    # signal persistence (turnover proxy)
    if len(Fm) > 3:
        ac = cs_corr(Fm, Fm.shift(-1))
        row['rank_autocorr_1m'] = ac.mean()
    # orthogonality to live Elendel composite + incremental IC
    if base_rank is not None:
        bc = cs_corr(Fm, base_rank)
        row['corr_elendel'] = bc.mean()
        fp = Fm.rank(axis=1, pct=True)
        bp = base_rank.rank(axis=1, pct=True)
        rho = cs_corr(Fm, base_rank)
        fz = fp.sub(fp.mean(axis=1), axis=0)
        bz = bp.sub(bp.mean(axis=1), axis=0)
        beta = (fz * bz).sum(axis=1) / (bz ** 2).sum(axis=1)
        resid = fz.sub(bz.mul(beta, axis=0))
        for h in (1, 3, 6):
            R = FWD[h].where(mask)
            ic_r, _ = rank_ic(resid, R)
            row[f'inc_ic_{h}'] = ic_r.mean()
            row[f'inc_icir_{h}'] = ic_r.mean() / ic_r.std() if ic_r.std() > 0 else np.nan
    return row, ic_store
