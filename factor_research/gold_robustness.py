import numpy as np, pandas as pd, warnings, itertools
warnings.filterwarnings('ignore')
from gold_data import *
from portfolio_lab import stats
CASH_M=1.06**(1/12)-1; COST=0.0015
rm = lambda x,w,mp=0.8: x.rolling(w,min_periods=int(w*mp))
gold, vol, I, Ec, cal = load_gold(); sig = L.month_ends(cal); fwd = monthly_fwd_strict(gold,cal,sig)
S = pd.read_csv('results/stage14_monthly_returns.csv',index_col=0,parse_dates=True)
B = S[['Elendel (control)','Zenith','csm_absolute score','Residual mom (live-like)']].mean(axis=1)
def G5(g, pw=126, sw=50, vw=63, vt=0.12, cap=1.0):
    r=g.pct_change(fill_method=None); sma=rm(g,sw).mean()
    ab=(g>sma).where(g.notna()&sma.notna()).astype(float); q5=ab.rolling(pw,min_periods=int(pw*0.8)).mean()
    vol=rm(r,vw).std()*np.sqrt(252); return q5*(vt/vol).clip(upper=cap)
def evaluate(expo_d, fwd, weight_match=True, ref=None):
    e=expo_d.reindex(sig); d=pd.concat([e,fwd],axis=1,keys=['e','r']).dropna(); d=d.loc['2008-03-31':'2026-06-30']
    turn=d.e.diff().abs().fillna(d.e.abs()); net=d.e*d.r+(1-d.e)*CASH_M-COST*turn
    return net, d.e
# reference
ref_net,_ = evaluate(pd.Series(1.0,index=gold.index).where(gold.notna()), fwd)
Bm = B.copy(); Bm.index=Bm.index.to_period('M')
def blend_stats(net, ref_net):
    n=net.copy(); n.index=n.index.to_period('M'); r=ref_net.copy(); r.index=r.index.to_period('M')
    idx=n.index.intersection(r.index).intersection(Bm.dropna().index); n,r,b=n[idx],r[idx],Bm[idx]
    w=min(0.35,0.10*r.std()/n.std()); p=(1-w)*b+w*n; pr=0.9*b+0.1*r
    return w, stats(p), stats(pr), stats(b)
base_net,base_e = evaluate(G5(gold),fwd)
w,sp,sr,sb = blend_stats(base_net,ref_net)
print('G5 default: risk-matched weight %.3f ; blend Sharpe %.3f MaxDD %.3f | B&H@10%% Sharpe %.3f MaxDD %.3f | bucket Sharpe %.3f MaxDD %.3f'%(w,sp['sharpe'],sp['maxdd'],sr['sharpe'],sr['maxdd'],sb['sharpe'],sb['maxdd']))
# ---- 1. parameter neighbourhood ----
rows=[]
for pw,sw,vw,vt in itertools.product((63,126,189),(30,50,100),(42,63,126),(0.10,0.12,0.15)):
    net,e = evaluate(G5(gold,pw,sw,vw,vt),fwd); w,sp,sr,sb = blend_stats(net,ref_net)
    rows.append(dict(pw=pw,sw=sw,vw=vw,vt=vt,w=w,avg_exp=e.mean(),sleeve_sharpe=stats(net)['sharpe'],sleeve_maxdd=stats(net)['maxdd'],sleeve_cagr=stats(net)['cagr'],blend_sharpe=sp['sharpe'],blend_maxdd=sp['maxdd'],dSharpe=sp['sharpe']-sr['sharpe'],dMaxDD=sp['maxdd']-sr['maxdd']))
P=pd.DataFrame(rows); P.to_csv('results/gold_g5_neighbourhood.csv',index=False,float_format='%.4f')
print('\nneighbourhood (81 combos) vs B&H @10%% (risk-matched blends):')
print(P[['sleeve_sharpe','sleeve_maxdd','sleeve_cagr','avg_exp','w','dSharpe','dMaxDD']].describe().loc[['min','25%','50%','75%','max']].round(3).to_string())
print('share of combos with dSharpe>0: %.2f ; dMaxDD>0: %.2f ; both: %.2f'%((P.dSharpe>0).mean(),(P.dMaxDD>0).mean(),((P.dSharpe>0)&(P.dMaxDD>0)).mean()))
for col in ('pw','sw','vw','vt'): print(col, P.groupby(col)[['dSharpe','dMaxDD','sleeve_maxdd']].mean().round(3).to_dict('index'))
# ---- 2. placebo: circularly shift the monthly exposure series ----
rng=np.random.default_rng(3)
e0 = G5(gold).reindex(sig); d0 = pd.concat([e0,fwd],axis=1,keys=['e','r']).dropna().loc['2008-03-31':'2026-06-30']
E=d0.e.values; R=d0.r.values; n=len(E); idx=d0.index
def run_shift(k):
    e=np.roll(E,k); turn=np.abs(np.diff(np.r_[e[0],e])); net=e*R+(1-e)*CASH_M-COST*turn; return pd.Series(net,index=idx)
real = pd.Series(E*R+(1-E)*CASH_M-COST*np.abs(np.diff(np.r_[E[0],E])),index=idx)
w,sp,sr,sb = blend_stats(real,ref_net)
res=[]
for k in range(6,n-6):
    sn=run_shift(k); ww,spp,_,_ = blend_stats(sn,ref_net)
    res.append((k,spp['sharpe'],spp['maxdd'],stats(sn)['maxdd'],stats(sn)['sharpe']))
Rr=pd.DataFrame(res,columns=['shift','blend_sharpe','blend_maxdd','sleeve_maxdd','sleeve_sharpe'])
print('\nPLACEBO (%d circular shifts of the real exposure path; same average exposure & persistence, no alignment with gold):'%len(Rr))
print('real  : blend Sharpe %.3f  blend MaxDD %.3f  sleeve MaxDD %.3f  sleeve Sharpe %.3f'%(sp['sharpe'],sp['maxdd'],stats(real)['maxdd'],stats(real)['sharpe']))
print('shifts: blend Sharpe median %.3f [5%%-95%% %.3f..%.3f] ; blend MaxDD median %.3f [%.3f..%.3f]'%(Rr.blend_sharpe.median(),*Rr.blend_sharpe.quantile([.05,.95]),Rr.blend_maxdd.median(),*Rr.blend_maxdd.quantile([.05,.95])))
print('P(shifted >= real): blend Sharpe %.2f ; blend MaxDD (shallower) %.2f ; sleeve MaxDD %.2f ; sleeve Sharpe %.2f'%((Rr.blend_sharpe>=sp['sharpe']).mean(),(Rr.blend_maxdd>=sp['maxdd']).mean(),(Rr.sleeve_maxdd>=stats(real)['maxdd']).mean(),(Rr.sleeve_sharpe>=stats(real)['sharpe']).mean()))
Rr.to_csv('results/gold_g5_placebo.csv',index=False,float_format='%.4f')
# ---- 3. other gold ETFs (same rule, same params) ----
rows=[]
for t in ['GOLDBEES','GOLD1','SETFGOLD','HDFCGOLD']:
    g=Ec[t]; f=monthly_fwd_strict(g,cal,sig); net,e=evaluate(G5(g),f); ref,_=evaluate(pd.Series(1.0,index=g.index).where(g.notna()),f)
    s=stats(net); rb=stats(ref); rows.append(dict(etf=t,months=len(net),g5_cagr=s['cagr'],g5_sharpe=s['sharpe'],g5_maxdd=s['maxdd'],bh_cagr=rb['cagr'],bh_sharpe=rb['sharpe'],bh_maxdd=rb['maxdd']))
print('\nsame rule on other gold ETFs:'); print(pd.DataFrame(rows).round(3).to_string(index=False))
