"""
stage19_industry_tilt_proxy.py -- additive-tilt proxy-book test for the Stage-1 industry-momentum
winner, modeled exactly on stage2_composites.py.

Stage-1 winner carried forward (see results/stage18_industry_momentum.csv, FINDINGS.md entry):
    indmom_level_ind_eq_L3_skip0  -- Industry_clean (with Sector_clean fallback), equal-weighted,
    additive ("level") construction, 3-month formation, no skip.  Across all 4 universes: t_3/t_6
    in 3.5-8.3, same-sign discovery/holdout IC everywhere, corr_elendel only 0.21-0.30 (vs 0.6-0.68
    for every sector factor tried before), inc_ic_3/inc_ic_6 clearly positive everywhere.
    L1/L6/L12 no-skip variants also cleared the Stage-1 bar but are not carried forward here --
    "prefer the simplest among winners", not a second open search.

This stage does NOT re-open the factor search: only the one named winner above is tested, at
pre-set tilt weights (0.3, 0.5, 1.0), against the two live composite scores (ELEN, ZEN).

Gate to Stage 3: the tilted proxy book must beat the un-tilted base on Sharpe in BOTH the
discovery (<=2014) and holdout (>=2015) sub-periods, and not materially worsen MaxDD.
"""
import os
import pickle

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
from evaluate import composite, zscore, rank_ic, SPLIT          # noqa: E402
from portfolio_lab import topn_book, book_report                 # noqa: E402

WINNER = 'indmom_level_ind_eq_L3_skip0'
WEIGHTS = (0.3, 0.5, 1.0)

st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
F, FWD, U = st['F'], st['FWD'], st['U']
IND = pickle.load(open(os.path.join(HERE, '.cache', 'stage18_industry_factors.pkl'), 'rb'))
indmom = IND[WINNER]

rows = []
for uname in ('U1_liquid1000', 'U2_live_trend'):
    mask = U[uname]
    bases = {'ELEN': composite(F, ['a3_rs_high', 'q5_126'], mask),
             'ZEN': composite(F, ['a1_52wh', 'q5_189'], mask)}
    for bname, base in bases.items():
        cands = [(bname, base)]
        for w in WEIGHTS:
            cands.append((f'{bname}+{w}*{WINNER}', zscore(base) + w * zscore(indmom.where(mask))))
        for name, sc in cands:
            r = {'universe': uname, 'score': name}
            for h in (1, 3, 6):
                ic, _ = rank_ic(sc.where(mask), FWD[h].where(mask))
                r[f'ic{h}'] = ic.mean(); r[f'icir{h}'] = ic.mean() / ic.std(); r[f'hit{h}'] = (ic > 0).mean()
                if h == 3:
                    r['ic3_disc'] = ic[ic.index <= SPLIT].mean(); r['ic3_hold'] = ic[ic.index > SPLIT].mean()
            bk = topn_book(sc, mask, FWD[1], n=15)
            r.update({k: v for k, v in book_report(bk, name).items() if k != 'label'})
            rows.append(r)
        print(uname, bname, 'done', flush=True)

df = pd.DataFrame(rows)
df.to_csv(os.path.join(HERE, 'results', 'stage19_industry_tilt_proxy.csv'), index=False, float_format='%.4f')

pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
show = ['universe', 'score', 'sharpe_disc', 'sharpe_hold', 'maxdd_disc', 'maxdd_hold',
        'cagr_disc', 'cagr_hold', 'turnover', 'ic3', 'ic3_disc', 'ic3_hold']
print(df[show].round(3).to_string(index=False))

# ───────────────────────── gate check ─────────────────────────
print('\n[stage19] gate check: tilted must beat its own base on Sharpe in BOTH disc and hold, MaxDD not materially worse')
for uname in df.universe.unique():
    for bname in ('ELEN', 'ZEN'):
        d = df[df.universe == uname]
        base_row = d[d.score == bname].iloc[0]
        for w in WEIGHTS:
            name = f'{bname}+{w}*{WINNER}'
            tr = d[d.score == name]
            if tr.empty:
                continue
            tr = tr.iloc[0]
            ok_disc = tr['sharpe_disc'] > base_row['sharpe_disc']
            ok_hold = tr['sharpe_hold'] > base_row['sharpe_hold']
            dd_ok = tr['maxdd_disc'] >= base_row['maxdd_disc'] - 0.03 and tr['maxdd_hold'] >= base_row['maxdd_hold'] - 0.03
            verdict = 'PASS' if (ok_disc and ok_hold and dd_ok) else 'fail'
            print(f"  {uname:<16} {name:<28} sharpe_disc {base_row['sharpe_disc']:.2f}->{tr['sharpe_disc']:.2f}  "
                  f"sharpe_hold {base_row['sharpe_hold']:.2f}->{tr['sharpe_hold']:.2f}  "
                  f"maxdd_disc {base_row['maxdd_disc']:.2f}->{tr['maxdd_disc']:.2f}  "
                  f"maxdd_hold {base_row['maxdd_hold']:.2f}->{tr['maxdd_hold']:.2f}  [{verdict}]")
