import pickle, sys, numpy as np, pandas as pd
from evaluate import composite, zscore, rank_ic, nw_tstat, SPLIT
from portfolio_lab import topn_book, book_report
st = pickle.load(open('.cache/state.pkl','rb'))
F, FWD, U = st['F'], st['FWD'], st['U']
ADDS = ['lowvol_126','low_ulcer_252','low_pain_126','hi_3y','intra_over_126','weekly_consist_26','mom_resid_12_1','low_gap_vol_126','season_same_month_5y']
rows=[]
for uname in ['U2_live_trend','U1_liquid1000']:
    mask = U[uname]
    bases = {'ELEN': composite(F,['a3_rs_high','q5_126'],mask), 'ZEN': composite(F,['a1_52wh','q5_189'],mask)}
    for bname, base in bases.items():
        cands = [(f'{bname}',base)]
        for a in ADDS:
            for w in (0.5, 1.0):
                cands.append((f'{bname}+{w}*{a}', zscore(base) + w*zscore(F[a].where(mask))))
        for name, sc in cands:
            r = {'universe':uname,'score':name}
            for h in (1,3,6):
                ic,_ = rank_ic(sc.where(mask), FWD[h].where(mask))
                r[f'ic{h}']=ic.mean(); r[f'icir{h}']=ic.mean()/ic.std(); r[f'hit{h}']=(ic>0).mean()
                if h==3:
                    r['ic3_disc']=ic[ic.index<=SPLIT].mean(); r['ic3_hold']=ic[ic.index>SPLIT].mean()
            bk = topn_book(sc, mask, FWD[1], n=15)
            r.update({k:v for k,v in book_report(bk,name).items() if k!='label'})
            rows.append(r)
        print(uname,bname,'done',flush=True)
df = pd.DataFrame(rows)
df.to_csv('results/stage2_composites.csv', index=False, float_format='%.4f')
