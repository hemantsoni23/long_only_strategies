"""Shared helpers for the decay check: panels, IC / basket stats, Newey-West, chunking, verdict tests."""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '.cache')
OUT = os.path.join(HERE, 'results')
os.makedirs(OUT, exist_ok=True)

ANCHOR = pd.Period('2026-05', 'M')      # last signal month (its 1m forward = 2026-06, last complete month)
CHUNK = 36
HORIZONS = (1, 3, 6, 12)
PRIMARY_H = 3
MIN_XS = 20


# ───────────────────────── data ─────────────────────────
def load_panels():
    P = {f: pd.read_parquet(os.path.join(CACHE, f'{f}.parquet')).astype('float64')
         for f in ('open', 'high', 'low', 'close', 'volume')}
    n_live = P['close'].notna().sum(axis=1)
    last_ok = n_live[n_live >= 2000].index.max()
    P = {f: d.loc[:last_ok] for f, d in P.items()}
    r = P['close'].pct_change(fill_method=None).clip(-0.5, 0.5)
    P['bench_ret'] = r.mean(axis=1, skipna=True).fillna(0.0)
    P['bench'] = (1 + P['bench_ret']).cumprod()
    return P


def month_end_days(index):
    s = pd.Series(index, index=index)
    return pd.DatetimeIndex(s.groupby(index.to_period('M')).max().values)


def to_period_index(df):
    out = df.copy()
    out.index = pd.PeriodIndex(out.index, freq='M')
    return out[~out.index.duplicated(keep='last')]


# ───────────────────────── stats ─────────────────────────
def nw_t(x, lag):
    """t-stat of the mean of x with Newey-West (Bartlett) long-run variance."""
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    n = len(x)
    if n < 8:
        return np.nan
    e = x - x.mean()
    lrv = e @ e / n
    for k in range(1, min(lag, n - 1) + 1):
        lrv += 2 * (1 - k / (lag + 1)) * (e[k:] @ e[:-k]) / n
    if lrv <= 0:
        return np.nan
    return x.mean() / np.sqrt(lrv / n)


def ols_nw(y, X, lag):
    """OLS y ~ X (X includes constant) with Newey-West SE. Returns beta, se, t."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    Xe = X * e[:, None]
    S = Xe.T @ Xe / n
    for l in range(1, min(lag, n - 1) + 1):
        G = Xe[l:].T @ Xe[:-l] / n
        S += (1 - l / (lag + 1)) * (G + G.T)
    V = n * XtXi @ S @ XtXi
    se = np.sqrt(np.diag(V))
    return b, se, b / se


def summarize(x, h):
    """mean, std, icir, hit, t, nw_t, n for a monthly series x at horizon h (NW lag h-1)."""
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 6:
        return dict(n=n, mean=np.nan, std=np.nan, ir=np.nan, hit=np.nan, t=np.nan, nw_t=np.nan)
    m, s = x.mean(), x.std()
    return dict(n=n, mean=m, std=s, ir=m / s if s > 0 else np.nan, hit=(x > 0).mean(),
                t=m / (s / np.sqrt(n)) if s > 0 else np.nan, nw_t=nw_t(x, max(h - 1, 0)))


# ───────────────────────── cross-sectional engine ─────────────────────────
def _rank_rows(a):
    return pd.DataFrame(a).rank(axis=1).values


def xs_stats(F, R, top_n):
    """F, R: month x stock DataFrames on the SAME index/columns (period index). Returns per-month Series:
    ic (Spearman), exc (top-N basket mean fwd return minus eligible-universe mean), acc (share of top-N names beating the median),
    n (cross-section size)."""
    F = F.reindex(columns=R.columns)
    idx = F.index.intersection(R.index)
    F, R = F.loc[idx], R.loc[idx]
    mask = F.notna().values & R.notna().values
    f = np.where(mask, F.values, np.nan)
    r = np.where(mask, R.values, np.nan)
    n = mask.sum(axis=1)
    fr, rr = _rank_rows(f), _rank_rows(r)
    fc = fr - np.nanmean(fr, axis=1, keepdims=True)
    rc = rr - np.nanmean(rr, axis=1, keepdims=True)
    with np.errstate(invalid='ignore', divide='ignore'):
        ic = np.nansum(fc * rc, axis=1) / np.sqrt(np.nansum(fc ** 2, axis=1) * np.nansum(rc ** 2, axis=1))
    # top-N basket (descending factor)
    desc = pd.DataFrame(f).rank(axis=1, ascending=False, method='first').values
    top = (desc <= top_n) & mask
    univ_mean = np.nanmean(r, axis=1)
    top_mean = np.where(top, r, np.nan)
    with np.errstate(all='ignore'):
        exc = np.nanmean(top_mean, axis=1) - univ_mean
        med = np.nanmedian(r, axis=1, keepdims=True)
        acc = np.nansum(np.where(top, (r > med).astype(float), np.nan), axis=1) / np.maximum(top.sum(axis=1), 1)
    ok = n >= MIN_XS
    out = pd.DataFrame({'ic': ic, 'exc': exc, 'acc': acc, 'n': n}, index=idx)
    out.loc[~ok, ['ic', 'exc', 'acc']] = np.nan
    return out


def fwd_returns(close, h):
    """month-end close -> month-end close, h months forward, indexed by signal month (period)."""
    mp = to_period_index(close.ffill().resample('ME').last())
    # drop the incomplete last month (data ends mid-month): keep only months <= ANCHOR+1
    mp = mp.loc[:ANCHOR + 1]
    return (mp.shift(-h) / mp - 1)


def chunk_bounds(first_month, last_month=ANCHOR, size=CHUNK, min_len=24):
    """List of (label, start, end) backward-anchored 36-month chunks; partial earliest chunk kept only if >= min_len."""
    out = []
    end = last_month
    while True:
        start = end - (size - 1)
        if start < first_month:
            if (end - first_month).n + 1 >= min_len:
                start = first_month
            else:
                break
        lab = f"{start.strftime('%Y-%m')}→{end.strftime('%Y-%m')}"
        out.append((lab, start, end))
        end = start - 1
        if start == first_month:
            break
    return out[::-1]


def chunk_table(series_by_h, first_month, tag_cols=('ic', 'exc')):
    """series_by_h: {h: DataFrame(ic, exc, acc, n)}. Returns long DataFrame with per chunk x h x metric stats."""
    rows = []
    bounds = chunk_bounds(first_month) + [('ALL', first_month, ANCHOR)]
    for lab, s, e in bounds:
        for h, d in series_by_h.items():
            dd = d.loc[s:e]
            for col in tag_cols:
                st = summarize(dd[col], h)
                st.update(chunk=lab, start=str(s), end=str(e), h=h, metric=col,
                          acc=dd['acc'].mean() if col == 'exc' else np.nan)
                rows.append(st)
    return pd.DataFrame(rows)


# ───────────────────────── regime controls ─────────────────────────
def regime_controls(P):
    """Monthly ex-ante controls at signal month t (data through t): mkt12, mktvol3, disp12 (z-scored over full sample)."""
    close = P['close']
    me = month_end_days(close.index)
    bench = P['bench']
    mkt12 = bench.pct_change(252)
    vol63 = P['bench_ret'].rolling(63).std() * np.sqrt(252)
    tv = (close * P['volume']).rolling(63, min_periods=45).median()
    r12 = close.ffill().pct_change(252, fill_method=None)
    disp = {}
    for d in me:
        if d not in r12.index:
            continue
        top = tv.loc[d].dropna().nlargest(500).index
        x = r12.loc[d, top].dropna()
        if len(x) >= 100:
            q = x.quantile([0.25, 0.75])
            disp[d] = (q.iloc[1] - q.iloc[0]) / 1.349
    disp = pd.Series(disp)
    C = pd.DataFrame({'mkt12': mkt12.reindex(me), 'mktvol3': vol63.reindex(me), 'disp12': disp.reindex(me)})
    C.index = pd.PeriodIndex(C.index, freq='M')
    C = C[~C.index.duplicated(keep='last')]
    C = (C - C.mean()) / C.std()
    return C


# ───────────────────────── verdict tests ─────────────────────────
def rolling_window_means(x, size=CHUNK, min_cov=0.75):
    """mean of every `size`-calendar-month window ending at each month (needs >= 0.75*size obs). x: Series on period index."""
    x = x.dropna()
    if x.empty:
        return pd.Series(dtype=float)
    full = pd.period_range(x.index.min(), x.index.max(), freq='M')
    xf = x.reindex(full)
    cnt = xf.notna().rolling(size).sum()
    m = xf.rolling(size, min_periods=1).mean()
    return m[cnt >= int(min_cov * size)]


def verdict_tests(x, controls, first_month, h, min_cov=0.75):
    """x: monthly primary series (period index). Returns dict with T1..T5 + final verdict."""
    x = x.dropna()
    x = x.loc[first_month:ANCHOR]
    bounds = chunk_bounds(x.index.min())
    full_bounds = [b for b in bounds if (b[2] - b[1]).n + 1 >= CHUNK]  # full 36m chunks only for T5 persistence
    nwl = max(h - 1, 0)
    last = bounds[-1]
    xl = x.loc[last[1]:last[2]]
    t1 = nw_t(xl, nwl)
    # T5 persistence
    nw_by_chunk = [nw_t(x.loc[b[1]:b[2]], nwl) for b in bounds]
    persist = 0
    for v in nw_by_chunk[::-1]:
        if np.isnan(v) or v < 1.0:
            persist += 1
        else:
            break
    # T2 trend (years)
    yrs = np.array([(p - x.index[0]).n / 12.0 for p in x.index])
    X = np.column_stack([np.ones(len(x)), yrs])
    b, se, t = ols_nw(x.values, X, 6)
    slope, slope_t = b[1], t[1]
    # T3 history percentile
    rw = rolling_window_means(x, min_cov=min_cov)
    pct = float((rw <= rw.iloc[-1]).mean()) if len(rw) > 5 else np.nan
    # T4 regime-adjusted
    C = controls.reindex(x.index)
    ok = C.notna().all(axis=1)
    xa, Ca, ya = x[ok], C[ok], yrs[ok.values]
    X2 = np.column_stack([np.ones(len(xa)), ya, Ca.values])
    b2, se2, t2 = ols_nw(xa.values, X2, 6)
    reg_part = Ca.values @ b2[2:]
    adj = xa - reg_part
    adj_last = adj.loc[last[1]:last[2]].mean()
    rw_adj = rolling_window_means(adj, min_cov=min_cov)
    pct_adj = float((rw_adj <= rw_adj.iloc[-1]).mean()) if len(rw_adj) > 5 else np.nan
    adj_slope, adj_slope_t = b2[1], t2[1]
    # in a market-regime sense: how much of latest-chunk shortfall vs full mean is regime-explained?
    short_raw = xl.mean() - x.mean()
    short_adj = adj_last - adj.mean()
    declining = (slope < 0) and (slope_t <= -2.0)
    excused = (not np.isnan(pct_adj)) and pct_adj >= 0.25 and not (adj_slope < 0 and adj_slope_t <= -2.0)
    t1_state = 'pass' if t1 >= 2.0 else ('weak' if t1 >= 1.0 else 'fail')
    unusual = (not np.isnan(pct)) and pct <= 0.10
    normal = (not np.isnan(pct)) and pct >= 0.25
    if t1_state == 'fail' and persist >= 2 and (declining or unusual) and not excused:
        verdict = 'DECAYED'
    elif (declining or unusual) and t1_state != 'pass' and not excused:
        verdict = 'DECAYING'
    elif t1_state in ('weak', 'fail') and (excused or (normal and not declining)):
        verdict = 'WEAK / REGIME'
    elif t1_state == 'pass' and not declining:
        verdict = 'HEALTHY'
    else:
        verdict = 'INCONCLUSIVE'
    return dict(latest_chunk=last[0], latest_mean=xl.mean(), full_mean=x.mean(), n_latest=len(xl),
                T1_nw_t=t1, T1=t1_state, T2_slope_per_yr=slope, T2_t=slope_t, T2_declining=declining,
                T3_pct=pct, T4_adj_latest=adj_last, T4_adj_full=adj.mean(), T4_pct_adj=pct_adj,
                T4_adj_slope=adj_slope, T4_adj_slope_t=adj_slope_t, T4_excused=excused,
                shortfall_raw=short_raw, shortfall_after_regime=short_adj,
                T5_persist=persist, verdict=verdict)
