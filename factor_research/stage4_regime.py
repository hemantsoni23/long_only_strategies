import pickle, numpy as np, pandas as pd
from data import load_panels
from evaluate import composite
from portfolio_lab import topn_book
from factors import FAMILY
st = pickle.load(open('.cache/state.pkl','rb')); F,FWD,U,sig = st['F'],st['FWD'],st['U'],st['sig']
P = load_panels(); b = P['bench']
bull = (b > b.rolling(200,min_periods=150).mean()).reindex(sig).fillna(False)
mom6 = (b/b.shift(126)-1).reindex(sig)
print('months bull/bear:', int(bull.sum()), int((~bull).sum()))
ics = pickle.load(open('.cache/ic_series.pkl','rb'))
rows=[]
for (u,n),d in ics.items():
    if u!='U1_liquid1000': continue
    r={'factor':n,'family':FAMILY.get(n,'LIVE')}
    for h in (1,3):
        s=d[h].dropna(); bb=bull.reindex(s.index)
        r[f'ic{h}_bull']=s[bb].mean(); r[f'ic{h}_bear']=s[~bb].mean()
        r[f'ic{h}_bear_t']=s[~bb].mean()/(s[~bb].std()/np.sqrt((~bb).sum()))
    rows.append(r)
d=pd.DataFrame(rows).set_index('factor'); d.to_csv('results/stage4_regime_ic.csv',float_format='%.4f')
pd.set_option('display.width',250); pd.set_option('display.max_rows',200)
print(d.sort_values('ic3_bear',ascending=False).head(25).round(3).to_string())
# book returns by regime
mask=U['U1_liquid1000']
res=[]
for n in ['a3_rs_high','q5_126','lowvol_126','low_pain_126','low_ulcer_252','mom_resid_12_1','hi_3y','tight_close_15','intraday_126_clip','low_downvol_252']:
    bk=topn_book(F[n],mask,FWD[1])
    bb=bull.reindex(bk.index)
    res.append(dict(book=n, bull_net_m=bk.net[bb].mean(), bear_net_m=bk.net[~bb].mean(), bear_mkt_m=bk.ew_mkt[~bb].mean(), bull_mkt_m=bk.ew_mkt[bb].mean(),
                    bear_hit_vs_mkt=(bk.net[~bb]>bk.ew_mkt[~bb]).mean(), bear_worst=bk.net[~bb].min()))
print(pd.DataFrame(res).round(4).to_string(index=False))
