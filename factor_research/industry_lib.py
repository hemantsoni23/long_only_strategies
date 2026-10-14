"""
industry_lib.py -- vectorised, reusable machinery for bottom-up industry/sector momentum research.

Same construction as stage18_industry_momentum.py (which stays as the audit trail for the Stage-1 sweep), but
fast enough for placebo / permutation tests and book-level work:

  * labels  : instruments_clean.csv  (Sector_clean 11 buckets, Industry_clean 205 buckets)
  * baskets : monthly, built from member stocks that were U1-eligible at the PRIOR month-end (no look-ahead)
  * group   : a stock reads its Industry_clean basket if that industry has >= min_members live U1 stocks at the
              signal date, otherwise its Sector_clean parent basket
  * factor  : basket trailing L-month return (skip=0 includes the most recent month, skip=1 excludes it)

Group index space: [0, n_ind) = industries, [n_ind, n_ind+n_sec) = sectors.
"""
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
INSTRUMENTS_CSV = os.path.join(os.path.dirname(HERE), 'instruments_clean.csv')


def load_labels(cols, path=INSTRUMENTS_CSV):
    """-> (ind_code, sec_code, ind_names, sec_names); codes are int arrays over `cols`, -1 where unlabelled."""
    inst = (pd.read_csv(path)[['trading_symbol', 'Sector_clean', 'Industry_clean']]
            .dropna(subset=['trading_symbol']).drop_duplicates('trading_symbol', keep='first')
            .set_index('trading_symbol').reindex(cols))
    ind_names = sorted(inst['Industry_clean'].dropna().unique())
    sec_names = sorted(inst['Sector_clean'].dropna().unique())
    ind_code = inst['Industry_clean'].map({n: i for i, n in enumerate(ind_names)}).fillna(-1).astype(int).values
    sec_code = inst['Sector_clean'].map({n: i for i, n in enumerate(sec_names)}).fillna(-1).astype(int).values
    return ind_code, sec_code, ind_names, sec_names


def industry_parent_sector(ind_code, sec_code, n_ind):
    """modal Sector_clean code of each industry's members (industries nest in sectors in this file)."""
    parent = np.full(n_ind, -1, dtype=int)
    for g in range(n_ind):
        s = sec_code[(ind_code == g) & (sec_code >= 0)]
        if len(s):
            parent[g] = np.bincount(s).argmax()
    return parent


def onehot(code, n):
    m = np.zeros((len(code), n))
    ok = code >= 0
    m[np.where(ok)[0], code[ok]] = 1.0
    return m


def basket_returns(code, n, mret, elig_prev, weight=None):
    """Monthly basket returns (T x n) and member counts, using prior-month-end eligibility `elig_prev` (bool T x N)."""
    r = mret.values
    valid = elig_prev.values & ~np.isnan(r)
    w = valid.astype('float64')
    if weight is not None:
        w = w * np.nan_to_num(weight.values, nan=0.0).clip(min=0.0)
    oh = onehot(code, n)
    num = np.nan_to_num(r) * w @ oh
    den = w @ oh
    cnt = valid.astype('float64') @ oh
    with np.errstate(invalid='ignore', divide='ignore'):
        ret = np.where(den > 0, num / den, np.nan)
    return ret, cnt


def effective_codes(ind_code, sec_code, n_ind, n_sec, u1_now, min_members, parent):
    """T x N int codes in the combined [industries | sectors] space; -1 where unlabelled."""
    cnt_now = u1_now.values.astype('float64') @ onehot(ind_code, n_ind)           # T x n_ind live members
    ok = cnt_now >= min_members                                                   # T x n_ind
    T, N = u1_now.shape
    codes = np.full((T, N), -1, dtype=int)
    lab = (sec_code >= 0)
    has_ind = ind_code >= 0
    ok_for = np.zeros((T, N), dtype=bool)
    ok_for[:, has_ind] = ok[:, ind_code[has_ind]]
    sec_idx = np.where(lab, n_ind + sec_code, -1)
    ind_idx = np.where(has_ind, ind_code, -1)
    codes = np.where(ok_for & has_ind[None, :], ind_idx[None, :], sec_idx[None, :])
    codes[:, ~lab & ~has_ind] = -1
    return codes, cnt_now, ok


def trailing(ret, L, skip):
    """ret: T x G monthly returns -> trailing L-month return ending at t (skip=0) or t-1 (skip=1)."""
    logr = np.log1p(np.clip(ret, -0.9, 5.0))
    logr = np.nan_to_num(logr, nan=0.0)
    cum = np.cumsum(logr, axis=0)
    end = np.vstack([np.zeros((1, cum.shape[1])), cum[:-1]]) if skip else cum
    start = np.vstack([np.zeros((L, cum.shape[1])), end[:-L]]) if L > 0 else end
    out = np.expm1(end - start)
    out[:L + (1 if skip else 0), :] = np.nan
    return out


def broadcast(G, codes):
    """G: T x groups; codes: T x N -> T x N values (nan where code<0)."""
    T = G.shape[0]
    idx = np.clip(codes, 0, G.shape[1] - 1)
    out = G[np.arange(T)[:, None], idx]
    return np.where(codes >= 0, out, np.nan)


class IndustryEngine:
    """Holds the heavy monthly inputs once; builds factor frames for any label assignment."""

    def __init__(self, X, sig, U1, min_members=10, dv_window=63):
        self.sig = sig
        self.cols = X.C.columns
        Cm = X.C.ffill().reindex(sig)            # last traded price at each month-end (referee fix: no 5-day cap -> no phantom 0% month for stale names)
        self.mret = Cm.pct_change(fill_method=None)
        self.U1 = U1.reindex(sig).fillna(False)
        self.elig_prev = self.U1.shift(1).fillna(False)
        self.dv = X.DV.rolling(dv_window, min_periods=21).median().reindex(sig).shift(1)
        self.min_members = min_members
        self.ind_code, self.sec_code, self.ind_names, self.sec_names = load_labels(self.cols)
        self.n_ind, self.n_sec = len(self.ind_names), len(self.sec_names)
        self.parent = industry_parent_sector(self.ind_code, self.sec_code, self.n_ind)

    def build(self, L, skip, weighting='eq', granularity='ind', construction='level', ind_code=None, sec_code=None):
        """Factor frame (T x N). ind_code/sec_code let placebo tests inject permuted labels."""
        ic = self.ind_code if ind_code is None else ind_code
        sc = self.sec_code if sec_code is None else sec_code
        n_ind, n_sec = self.n_ind, self.n_sec
        w = self.dv if weighting == 'dv' else None
        ret_ind, _ = basket_returns(ic, n_ind, self.mret, self.elig_prev, w)
        ret_sec, _ = basket_returns(sc, n_sec, self.mret, self.elig_prev, w)
        G = np.hstack([ret_ind, ret_sec])
        tr = trailing(G, L, skip)
        if granularity == 'ind':
            codes, _, _ = effective_codes(ic, sc, n_ind, n_sec, self.U1, self.min_members, self.parent)
        else:
            codes = np.tile(np.where(sc >= 0, n_ind + sc, -1)[None, :], (len(self.sig), 1))
        level = broadcast(tr, codes)
        if construction == 'level':
            return pd.DataFrame(level, index=self.sig, columns=self.cols)
        own = trailing(self.mret.values, L, skip)
        return pd.DataFrame(own - level, index=self.sig, columns=self.cols)

    def loo_monthly(self, code, n, weighting='eq', min_peers=5):
        """Leave-one-out monthly peer return of every stock's own group (T x N): the basket return EXCLUDING the stock itself.
        nan where the stock has no label or fewer than `min_peers` eligible peers that month."""
        r = np.nan_to_num(self.mret.values)
        valid = self.elig_prev.values & ~np.isnan(self.mret.values)
        w = valid.astype('float64')
        if weighting == 'dv':
            w = w * np.nan_to_num(self.dv.values, nan=0.0).clip(min=0.0)
        oh = onehot(code, n)
        num, den = (r * w) @ oh, w @ oh
        cnt = valid.astype('float64') @ oh
        g = np.clip(code, 0, n - 1)
        loo_num = num[:, g] - r * w
        loo_den = den[:, g] - w
        peers = cnt[:, g] - valid
        with np.errstate(invalid='ignore', divide='ignore'):
            out = np.where((loo_den > 0) & (peers >= min_peers) & (code >= 0)[None, :], loo_num / loo_den, np.nan)
        return out

    def build_loo(self, L, skip, weighting='eq', ind_code=None, sec_code=None, min_peers=5):
        """Leave-one-out industry-momentum factor (T x N): trailing L-month compounded LOO peer return; a stock reads its
        Industry_clean LOO peers when that industry has >= min_members live U1 stocks at the signal date, else its
        Sector_clean LOO peers. nan if any month of the window is missing."""
        ic = self.ind_code if ind_code is None else ind_code
        sc = self.sec_code if sec_code is None else sec_code
        loo_i = self.loo_monthly(ic, self.n_ind, weighting, min_peers)
        loo_s = self.loo_monthly(sc, self.n_sec, weighting, min_peers)

        def strict(x):
            logr = np.log1p(np.clip(x, -0.9, 5.0))
            miss = np.isnan(logr).astype('float64')
            cum = np.cumsum(np.nan_to_num(logr), axis=0)
            cm = np.cumsum(miss, axis=0)
            sh = 1 if skip else 0
            endc = np.vstack([np.zeros((sh, cum.shape[1])), cum[:cum.shape[0] - sh]])
            endm = np.vstack([np.zeros((sh, cm.shape[1])), cm[:cm.shape[0] - sh]])
            stc = np.vstack([np.zeros((L, cum.shape[1])), endc[:-L]])
            stm = np.vstack([np.zeros((L, cm.shape[1])), endm[:-L]])
            out = np.expm1(endc - stc)
            bad = (endm - stm) > 0
            out[bad] = np.nan
            out[:L + sh, :] = np.nan
            return out
        ti, ts = strict(loo_i), strict(loo_s)
        cnt_now = self.U1.values.astype('float64') @ onehot(ic, self.n_ind)
        ok = cnt_now >= self.min_members
        has_ind = ic >= 0
        use_ind = np.zeros(ti.shape, dtype=bool)
        use_ind[:, has_ind] = ok[:, ic[has_ind]]
        out = np.where(use_ind, ti, ts)
        return pd.DataFrame(out, index=self.sig, columns=self.cols)

    def group_trailing(self, L, skip, weighting='eq'):
        """T x (n_ind+n_sec) trailing basket returns (for book construction)."""
        w = self.dv if weighting == 'dv' else None
        ret_ind, cnt_ind = basket_returns(self.ind_code, self.n_ind, self.mret, self.elig_prev, w)
        ret_sec, _ = basket_returns(self.sec_code, self.n_sec, self.mret, self.elig_prev, w)
        return trailing(np.hstack([ret_ind, ret_sec]), L, skip), cnt_ind


def permute_within(code, parent_code, rng):
    """Placebo: shuffle Industry_clean labels among stocks WITHIN each Sector_clean (preserves industry sizes and
    the sector composition; destroys which stocks truly belong together inside a sector)."""
    new = code.copy()
    for s in np.unique(parent_code[parent_code >= 0]):
        idx = np.where((parent_code == s) & (code >= 0))[0]
        new[idx] = rng.permutation(code[idx])
    return new


def permute_all(code, rng):
    """Placebo: shuffle labels across ALL labelled stocks (preserves industry sizes, destroys everything else)."""
    new = code.copy()
    idx = np.where(code >= 0)[0]
    new[idx] = rng.permutation(code[idx])
    return new
