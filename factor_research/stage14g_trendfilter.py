import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from stage14_roadmap import *
from factors import rmean
P = load_panels(); X = Ctx(P)
trend = (X.Cf > rmean(X.Cf,200)).reindex(sig)
HOLD = pd.Timestamp('2014-12-31')
SETS = {'Elendel (control)':(['a3_rs_high','q5_126'],'U1_liquid1000'),
        'I1 tight+persist (mid/small)':(['tight_close_15','q5_126'],'U7_midsmall_301_1000'),
        'I1 tight+persist (liquid)':(['tight_close_15','q5_126'],'U1_liquid1000'),
        'I2 resid+persist (top250)':(['mom_resid_12_1','q5_126'],'U4_top250'),
        'I3 low-risk (top250)':(['lowvol_126','low_ulcer_252'],'U4_top250'),
        'I4 intraday+ulcer (top250)':(['intra_over_252','low_ulcer_252'],'U4_top250'),
        'I0 persistence only (q5_126)':(['q5_126'],'U1_liquid1000')}
rows=[]; ser={}
for nm,(c,u) in SETS.items():
    for tag,mk in (('no trend filter',allU[u]),('with SMA200 filter (live-style)',allU[u]&trend)):
        sc = composite(F,c,mk) if len(c)>1 else F[c[0]].where(mk)
        bk = topn_book(sc,mk,FWD[1],n=15); out,_=chassis(bk['gross'],bk['turnover'])
        out=out.dropna(); a=stats(out); h=stats(out[out.index>HOLD])
        rows.append(dict(idea=nm,universe_filter=tag,avg_names=float(mk.sum(axis=1).mean()),cagr=a['cagr'],sharpe=a['sharpe'],maxdd=a['maxdd'],cagr_hold=h['cagr'],sharpe_hold=h['sharpe'],maxdd_hold=h['maxdd'],turnover=bk['turnover'].mean()))
        ser[(nm,tag)] = out
T = pd.DataFrame(rows); T.to_csv('results/stage14_trendfilter_check.csv',index=False,float_format='%.4f')
pd.set_option('display.width',250); print(T.round(3).to_string(index=False))
# paired comparison vs control under the live-style filter
ctrl = ser[('Elendel (control)','with SMA200 filter (live-style)')]
for nm in SETS:
    if nm.startswith('Elendel'): continue
    x = ser[(nm,'with SMA200 filter (live-style)')]; j=pd.concat([x,ctrl],axis=1).dropna(); j=j[j.index>='2008-04-30']
    d=((j.iloc[:,0]-CASH_M).mean()/j.iloc[:,0].std()-(j.iloc[:,1]-CASH_M).mean()/j.iloc[:,1].std())*np.sqrt(12)
    jh=j[j.index>HOLD]; dh=((jh.iloc[:,0]-CASH_M).mean()/jh.iloc[:,0].std()-(jh.iloc[:,1]-CASH_M).mean()/jh.iloc[:,1].std())*np.sqrt(12)
    print(f'{nm:34s} dSharpe vs control (live-style filter): full {d:+.2f}  holdout {dh:+.2f}  corr {j.corr().iloc[0,1]:.2f}')
