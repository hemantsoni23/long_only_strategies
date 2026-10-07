"""
stage15c_value_robustness.py -- stress the one surprising result of stage15b: earnings yield (E/P) added to the Elendel score lifts the
top-15 book (Sharpe 1.0 -> 1.6, paired t ~3) in the liquid-1000 universe but not in the top-300.

Checks: (1) definition (EPS/price vs net-profit/market-cap vs sales/mcap vs EBIT/mcap, positive-earnings-only), (2) by calendar year,
(3) by liquidity tier, (4) block-bootstrap of the paired monthly difference, (5) share-count / split sensitivity, (6) what the picks are
(avg E/P, share with negative earnings, size).  Survivorship caveat: only currently listed companies have fundamentals AND prices, so
a cheap-stock effect is flattered (cheap names that later died are missing).  Window 2020-06..~2025-03.
"""
import os
import pickle
import warnings

import numpy as np
import pandas as pd

from data import load_panels
from evaluate import composite, zscore, rank_ic, nw_tstat
from portfolio_lab import topn_book, stats
from stage15_fundamental_momentum import build_quarter_table, to_monthly

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
START = pd.Timestamp('2020-06-01')


def boot_paired(d, B=4000, blk=3, seed=1):
    d = np.asarray(d.dropna()); n = len(d); rng = np.random.default_rng(seed)
    m = []
    for _ in range(B):
        k = int(np.ceil(n / blk)); st = rng.integers(0, n, k)
        idx = ((st[:, None] + np.arange(blk)) % n).ravel()[:n]
        m.append(d[idx].mean())
    m = np.array(m)
    return d.mean(), (m > 0).mean(), np.percentile(m, 5), np.percentile(m, 95)


def main():
    st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
    sig, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
    P = load_panels(); C = P['close']; V = P['volume']
    q = build_quarter_table(); q = q[q.symbol.isin(C.columns)].reset_index(drop=True)
    Cm = C.ffill().reindex(sig)
    M = {k: to_monthly(q, k, sig).reindex(columns=C.columns) for k in ('eps_ttm', 'np_ttm', 'rev_ttm', 'ebit_ttm', 'shares', 'equity')}
    mcap = Cm * M['shares']
    V1 = {
        'ep_eps': M['eps_ttm'] / Cm,
        'ep_np': M['np_ttm'] / mcap,
        'sp_rev': M['rev_ttm'] / mcap,
        'ebit_p': M['ebit_ttm'] / mcap,
    }
    V1 = {k: v.replace([np.inf, -np.inf], np.nan) for k, v in V1.items()}
    V1['ep_np_pos'] = V1['ep_np'].where(V1['ep_np'] > 0)
    V1['bp'] = (M['equity'] / mcap).replace([np.inf, -np.inf], np.nan)
    dv = (C * V).rolling(63, min_periods=21).median().reindex(sig)
    liq_rank = dv.rank(axis=1, ascending=False, method='min')

    pd.set_option('display.width', 250, 'display.max_columns', 40)
    mask0 = U['U1_liquid1000']
    common = mask0.copy()
    for k in ('ep_eps', 'ep_np', 'sp_rev', 'ebit_p'):
        common &= V1[k].notna()
    common = common.where(common.sum(axis=1) >= 60, False)
    base = composite(F, ['a3_rs_high', 'q5_126'], common)
    b0 = topn_book(base, common, FWD[1], n=15)
    print(f'common mask: avg names/month {common[common.index>=START].sum(axis=1).replace(0,np.nan).mean():.0f}')

    # (1) IC + books by definition
    rows = []
    for k, S in V1.items():
        m = common & S.notna() if k in ('ep_np_pos', 'bp') else common
        base_k = composite(F, ['a3_rs_high', 'q5_126'], m)
        b_base = topn_book(base_k, m, FWD[1], n=15)
        r = {'var': k, 'n': float(m[m.index >= START].sum(axis=1).replace(0, np.nan).mean())}
        for h in (1, 3, 6, 12):
            ic, _ = rank_ic(S.where(m), FWD[h].where(m)); ic = ic[ic.index >= START].dropna()
            if len(ic) >= 12:
                r[f'ic{h}'] = ic.mean(); r[f'hit{h}'] = (ic > 0).mean(); r[f't{h}'] = nw_tstat(ic, h - 1)
        for w in (0.5, 1.0):
            sc = zscore(base_k) + w * zscore(S.where(m))
            bk = topn_book(sc, m, FWD[1], n=15)
            bb = bk[bk.index >= START]; b = b_base[b_base.index >= START]
            d = (bb['net'] - b['net']).dropna()
            s1, s0 = stats(bb['net']), stats(b['net'])
            r[f'w{w}_sharpe'] = s1['sharpe']; r[f'w{w}_base'] = s0['sharpe']; r[f'w{w}_cagr'] = s1['cagr']
            r[f'w{w}_d_pm'] = d.mean() * 100; r[f'w{w}_d_t'] = d.mean() / (d.std() / np.sqrt(len(d)))
        rows.append(r)
    print('\n=== (1) value definitions (U1, same names for each; ep_np_pos & bp use own coverage)')
    print(pd.DataFrame(rows).round(3).to_string(index=False))

    # (2)-(4) on ep_np (shares-based, split-robust) and ep_eps, w=0.5
    for vk in ('ep_np', 'ep_eps'):
        S = V1[vk]
        sc = zscore(base) + 0.5 * zscore(S.where(common))
        bk = topn_book(sc, common, FWD[1], n=15)
        a = bk[bk.index >= START]; b = b0[b0.index >= START]
        d = (a['net'] - b['net']).dropna()
        yr = pd.DataFrame({'combo': (1 + a['net']).groupby(a.index.year).prod() - 1,
                           'base': (1 + b['net']).groupby(b.index.year).prod() - 1,
                           'ew_mkt': (1 + b['ew_mkt']).groupby(b.index.year).prod() - 1})
        yr['delta'] = yr['combo'] - yr['base']
        print(f'\n=== (2) calendar-year returns, base vs base+0.5*{vk}')
        print((yr * 100).round(1).to_string())
        mu, pgt0, lo, hi = boot_paired(d)
        print(f'(4) paired monthly diff mean {mu*100:.2f}%  P(>0)={pgt0:.3f}  90% CI [{lo*100:.2f}, {hi*100:.2f}]  n={len(d)}')

    # (3) liquidity tiers
    print('\n=== (3) liquidity tiers (63d median traded value rank)  [ep_np, w=0.5]')
    S = V1['ep_np']
    for lab, lo_, hi_ in (('rank 1-300', 0, 300), ('rank 301-600', 300, 600), ('rank 601-1000', 600, 1000), ('rank 1-600', 0, 600)):
        m = common & (liq_rank > lo_) & (liq_rank <= hi_)
        m = m.where(m.sum(axis=1) >= 40, False)
        base_k = composite(F, ['a3_rs_high', 'q5_126'], m)
        bb0 = topn_book(base_k, m, FWD[1], n=15)
        bk = topn_book(zscore(base_k) + 0.5 * zscore(S.where(m)), m, FWD[1], n=15)
        a = bk[bk.index >= START]; b = bb0[bb0.index >= START]
        d = (a['net'] - b['net']).dropna()
        ic, _ = rank_ic(S.where(m), FWD[3].where(m)); ic = ic[ic.index >= START].dropna()
        print(f"{lab:<14} names~{m[m.index>=START].sum(axis=1).replace(0,np.nan).mean():4.0f}  EP IC3 {ic.mean():+.3f} (t {nw_tstat(ic,2):.1f})  "
              f"Sharpe base {stats(b['net'])['sharpe']:.2f} -> combo {stats(a['net'])['sharpe']:.2f}   CAGR {stats(b['net'])['cagr']*100:.0f}% -> {stats(a['net'])['cagr']*100:.0f}%   paired t {d.mean()/(d.std()/np.sqrt(len(d))):.2f}")

    # (6) what does the combo pick?
    sc = zscore(base) + 0.5 * zscore(V1['ep_np'].where(common))
    picks_ep, picks_neg, picks_rank, base_ep, base_rank = [], [], [], [], []
    for d_ in sc.index[sc.index >= START]:
        s = sc.loc[d_].dropna()
        if len(s) < 60:
            continue
        top = s.nlargest(15).index; bt = base.loc[d_].dropna().nlargest(15).index
        e = V1['ep_np'].loc[d_]
        picks_ep.append(e[top].median()); base_ep.append(e[bt].median()); picks_neg.append((e[top] < 0).mean())
        picks_rank.append(liq_rank.loc[d_][top].median()); base_rank.append(liq_rank.loc[d_][bt].median())
    print(f'\n(6) picks: median E/P combo {np.nanmean(picks_ep):.3f} vs base {np.nanmean(base_ep):.3f};  share loss-making {np.nanmean(picks_neg):.1%};'
          f'  median liquidity rank combo {np.nanmean(picks_rank):.0f} vs base {np.nanmean(base_rank):.0f}')


if __name__ == '__main__':
    main()
