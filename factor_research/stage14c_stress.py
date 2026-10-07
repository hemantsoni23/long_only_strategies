import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from stage14_roadmap import *
from assets import load_indices
S = pd.read_csv('results/stage14_monthly_returns.csv', index_col=0, parse_dates=True).loc[:'2026-06-30']
raw = pickle.load(open('.cache/stage14_raw_books.pkl','rb'))
HOLD = pd.Timestamp('2014-12-31')
pd.set_option('display.width',260); pd.set_option('display.max_columns',40)
FIN = ['Elendel (control)','I1 tight+persist (mid/small)','I1 tight+persist (liquid)','I2 resid+persist (liquid)','I2 resid+persist (top250)','I3 low-risk (top250)','I4 intraday+ulcer (top250)']
# ---- cost sensitivity ----
rows=[]
for nm in FIN:
    bk = raw[nm]
    for c in (0.003,0.005,0.0075,0.010):
        out,_ = chassis(bk['gross'], bk['turnover'], cost=c)
        a = stats(out.dropna()); h = stats(out[out.index>HOLD].dropna())
        rows.append(dict(idea=nm,cost_one_way=c,cagr=a['cagr'],sharpe=a['sharpe'],maxdd=a['maxdd'],cagr_hold=h['cagr'],sharpe_hold=h['sharpe'],turnover=bk['turnover'].mean()))
CS = pd.DataFrame(rows); CS.to_csv('results/stage14_cost_sensitivity.csv',index=False,float_format='%.4f')
print('--- cost sensitivity (chassis applied)')
print(CS.pivot(index='idea',columns='cost_one_way',values='sharpe').round(2).to_string())
print(CS.pivot(index='idea',columns='cost_one_way',values='cagr').round(3).to_string())
# ---- capacity ----
P = load_panels(); X = Ctx(P)
dv = X.DV.rolling(63,min_periods=21).median().reindex(sig)
rows=[]
for nm in FIN:
    comps,u = IDEAS[nm]; m = allU[u]; sc = make_score(comps,m).where(m); r1 = FWD[1].where(m)
    parts={a:[] for a in (5,10,25,50,100)}
    for d in sc.index:
        s = sc.loc[d].dropna(); s = s[r1.loc[d].reindex(s.index).notna()]
        if len(s)<60: continue
        pick = s.nlargest(15).index; adv = dv.loc[d, pick].astype(float)
        for aum in parts: parts[aum].extend(((aum*1e7/15)/adv).replace([np.inf],np.nan).dropna().values)
    row={'idea':nm}
    for aum,v in parts.items():
        v=np.array(v); row[f'med_%ADV_{aum}cr']=np.median(v)*100; row[f'pct_pos_gt5%ADV_{aum}cr']=(v>0.05).mean()
    rows.append(row)
CAP = pd.DataFrame(rows).set_index('idea'); CAP.to_csv('results/stage14_capacity.csv',float_format='%.4f')
print('\n--- capacity: median position as % of 63d median daily traded value; share of positions >5% ADV'); print(CAP.round(3).to_string())
# ---- survivorship partial check ----
last = P['close'].apply(lambda s: s.last_valid_index())
ended = pd.Series(last < pd.Timestamp('2026-06-01'))
ended.index = P['close'].columns
print('\nsymbols that stop trading before 2026-06:', int(ended.sum()), 'of', len(ended))
rows=[]
for nm in ['Elendel (control)','I1 tight+persist (mid/small)','I2 resid+persist (liquid)','I3 low-risk (liquid)']:
    comps,u = IDEAS[nm]; m = allU[u]
    for tag,mk in (('all names',m),('excluding delisted',m & ~ended.reindex(m.columns).values[None,:])):
        bk = topn_book(make_score(comps,mk),mk,FWD[1],n=15)
        out,_ = chassis(bk['gross'],bk['turnover']); a=stats(out.dropna())
        rows.append(dict(idea=nm,universe=tag,cagr=a['cagr'],sharpe=a['sharpe'],maxdd=a['maxdd']))
SV = pd.DataFrame(rows); SV.to_csv('results/stage14_survivorship_check.csv',index=False,float_format='%.4f'); print(SV.round(3).to_string(index=False))
# ---- VIX spike override on the live-like bucket ----
I = load_indices()['close']; vix = I['India_VIX'].dropna()
vp = vix.rolling(504,min_periods=252).apply(lambda x:(x[-1]>=x).mean(),raw=True)
vps = vp.reindex(pd.date_range(vp.index.min(),vp.index.max())).ffill().reindex(sig)
BUCKET=['Elendel (control)','Zenith','csm_absolute score','Residual mom (live-like)']
def with_gate(bk, mode, cost=0.003):
    net = bk['gross']-2*cost*bk['turnover']
    base_g = pd.Series(np.where(bull.reindex(net.index).values,1.0,0.5),index=net.index)
    hi = (vps.reindex(net.index)>=0.8).fillna(False)
    if mode=='vix_override': g = pd.Series(np.where(hi,1.0,base_g),index=net.index)
    elif mode=='vix_boost':  g = pd.Series(np.where(hi & ~bull.reindex(net.index).values, 1.0, base_g),index=net.index)
    else: g = base_g
    rv = net.rolling(6).std().shift(1)*np.sqrt(12); ex=(0.20/rv).clip(upper=1).fillna(1)
    expo = np.minimum(g,ex)
    return expo*net+(1-expo)*CASH_M-cost*expo.diff().abs().fillna(0)
rows=[]
for mode in ('gate','vix_override'):
    B = pd.concat([with_gate(raw[n],mode) for n in BUCKET],axis=1).mean(axis=1)
    B = B[(B.index>='2010-06-30')&(B.index<='2026-06-30')]
    a=stats(B); rows.append(dict(rule=mode,cagr=a['cagr'],vol=a['vol'],sharpe=a['sharpe'],maxdd=a['maxdd'],calmar=a['calmar'],months=len(B)))
hi_months = int(((vps>=0.8)&(~bull)).sum())
print('\n--- VIX override on the bucket (2010-06+); months with VIX top-20% AND market below SMA200:', hi_months)
print(pd.DataFrame(rows).round(3).to_string(index=False))
pd.DataFrame(rows).to_csv('results/stage14_vix_override.csv',index=False,float_format='%.4f')
