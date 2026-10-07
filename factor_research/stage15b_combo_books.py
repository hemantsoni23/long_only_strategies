"""
stage15b_combo_books.py -- do fundamentals add to the price-momentum book? (follows stage15_fundamental_momentum.py)

1. Independent double sort: price score (Elendel base) tercile x fundamental composite tercile -> mean 3m excess return per cell.
2. Top-15 equal-weight books on the SAME dates and SAME covered universe (names with fundamental data):
     base            = Elendel composite (a3_rs_high + q5_126)
     base + w*FUND   = z(base) + w*z(FUND)       w = 0.5, 1.0
     gate            = base ranking restricted to names with FUND > median
     FUND alone, EP alone
   Paired monthly difference vs base (t-stat) is the headline, not the absolute CAGR.
FUND (pre-declared, the CJL/Novy-Marx family): z(sue_eps) + z(surge_rev) + z(dm_ebit) + z(ear3), fresh-or-not as in stage15.
FUND2 (selected AFTER seeing stage15 -> optimistic): z(sg_np) + z(dm_ebit) + z(ear3).
Window 2020-06 .. last signal with fundamentals (~2025-03): ~58 months, one regime.  Treat as a screen, not proof.
"""
import os
import pickle
import warnings

import numpy as np
import pandas as pd

from evaluate import composite, zscore, rank_ic, nw_tstat, winsor_rows
from portfolio_lab import topn_book, stats

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
START = pd.Timestamp('2020-06-01')
HOLD = pd.Timestamp('2023-01-01')


def zs(S, mask):
    return zscore(S.where(mask))


def book_row(name, bk, base_bk=None):
    bk = bk[bk.index >= START]
    r = {'book': name, 'n': len(bk)}
    st = stats(bk['net'])
    r.update({k: st.get(k) for k in ('cagr', 'vol', 'sharpe', 'maxdd')})
    r['turnover'] = bk['turnover'].mean()
    r['hit_vs_mkt'] = (bk['net'] > bk['ew_mkt']).mean()
    for tag, sl in (('a', bk.index < HOLD), ('b', bk.index >= HOLD)):
        s2 = stats(bk[sl]['net']) if sl.sum() >= 24 else {}
        r[f'sharpe_{tag}'] = s2.get('sharpe', np.nan)
    if base_bk is not None:
        b = base_bk[base_bk.index >= START]
        d = (bk['net'] - b['net']).dropna()
        r['d_mean_pm'] = d.mean() * 100
        r['d_t'] = d.mean() / (d.std() / np.sqrt(len(d))) if len(d) > 5 and d.std() > 0 else np.nan
    return r


def main():
    st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
    sig, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
    S = pickle.load(open(os.path.join(HERE, '.cache', 'stage15_sigs.pkl'), 'rb'))
    pd.set_option('display.width', 250, 'display.max_columns', 40)
    allrows, sortrows = [], []
    for un in ('U1_liquid1000', 'U2_live_trend', 'U3_top300'):
        mask0 = U[un]
        fund_ok = S['sue_eps'].notna() & S['dm_ebit'].notna() & S['ear3'].notna() & S['surge_rev'].notna()
        mask = mask0 & fund_ok.reindex(columns=mask0.columns, fill_value=False)
        ok_dates = mask.sum(axis=1) >= 60
        mask = mask.where(ok_dates, False)
        base = composite(F, ['a3_rs_high', 'q5_126'], mask)
        FUND = zs(S['sue_eps'], mask) + zs(S['surge_rev'], mask) + zs(S['dm_ebit'], mask) + zs(S['ear3'], mask)
        FUND2 = zs(S['sg_np'], mask) + zs(S['dm_ebit'], mask) + zs(S['ear3'], mask)
        EP = zs(S['ep_ttm'], mask)

        # 1. double sort (3m excess)
        pb = base.where(mask).rank(axis=1, pct=True)
        for fname, FS in (('FUND', FUND), ('FUND2', FUND2), ('EP', EP)):
            pf = FS.where(mask).rank(axis=1, pct=True)
            R = winsor_rows(FWD[3].where(mask))
            ex = R.sub(R.mean(axis=1), axis=0)
            cells = {}
            for i, (lo, hi) in enumerate(((0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.01))):
                for j, (lo2, hi2) in enumerate(((0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.01))):
                    m = (pb > lo - (lo == 0) * 1e-9) & (pb <= hi) & (pf > lo2 - (lo2 == 0) * 1e-9) & (pf <= hi2)
                    v = ex.where(m).mean(axis=1)
                    v = v[v.index >= START].dropna()
                    cells[(i, j)] = (v.mean() * 100, len(v))
            row = {'universe': un, 'fund': fname}
            for (i, j), (v, n) in cells.items():
                row[f'P{i + 1}F{j + 1}'] = v
            row['F_spread_in_priceTop'] = row['P3F3'] - row['P3F1']
            row['F_spread_in_priceBot'] = row['P1F3'] - row['P1F1']
            row['P_spread_in_fundTop'] = row['P3F3'] - row['P1F3']
            sortrows.append(row)

        # 2. books
        b0 = topn_book(base, mask, FWD[1], n=15)
        allrows.append({'universe': un, **book_row('BASE elendel (covered names)', b0)})
        cands = {
            'base+0.5*FUND': zscore(base) + 0.5 * zscore(FUND),
            'base+1.0*FUND': zscore(base) + 1.0 * zscore(FUND),
            'base+1.0*FUND2 (post-hoc)': zscore(base) + 1.0 * zscore(FUND2),
            'base+0.5*EP': zscore(base) + 0.5 * zscore(EP),
            'base+1.0*EP': zscore(base) + 1.0 * zscore(EP),
            'base+0.5*FUND+0.5*EP': zscore(base) + 0.5 * zscore(FUND) + 0.5 * zscore(EP),
            'FUND alone': FUND, 'FUND2 alone (post-hoc)': FUND2, 'EP alone': EP,
        }
        medf = FUND.where(mask).median(axis=1)
        cands['gate: base | FUND>median'] = base.where(FUND.gt(medf, axis=0))
        for k, sc in cands.items():
            bk = topn_book(sc, mask, FWD[1], n=15)
            allrows.append({'universe': un, **book_row(k, bk, b0)})
        # market reference
        ref = b0[b0.index >= START]['ew_mkt']
        print(f'{un}: EW-market monthly mean {ref.mean()*100:.2f}%  ann {((1+ref).prod()**(12/len(ref))-1)*100:.1f}%', flush=True)
    ds = pd.DataFrame(sortrows); ds.to_csv(os.path.join(HERE, 'results', 'stage15b_double_sorts.csv'), index=False, float_format='%.3f')
    db = pd.DataFrame(allrows); db.to_csv(os.path.join(HERE, 'results', 'stage15b_books.csv'), index=False, float_format='%.4f')
    print('\n=== double sorts: mean 3m excess return % (P=price-terciles low->high, F=fund-terciles low->high)')
    print(ds.round(2).to_string(index=False))
    print('\n=== top-15 books (covered names, 2020-06+)')
    print(db.round(3).to_string(index=False))


if __name__ == '__main__':
    main()
