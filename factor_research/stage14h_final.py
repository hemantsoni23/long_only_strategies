import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from stage14_roadmap import *
from factors import rmean
rng = np.random.default_rng(11)
HOLD = pd.Timestamp('2014-12-31')
P = load_panels(); X = Ctx(P); trend = (X.Cf > rmean(X.Cf,200)).reindex(sig)
S = pd.read_csv('results/stage14_monthly_returns.csv',index_col=0,parse_dates=True).loc[:'2026-06-30']
S = S.join(pd.read_csv('results/stage14_breakout_monthly_aligned.csv',index_col=0,parse_dates=True),how='left')
S = S.rename(columns={'I6 breakout sim (52w-high+RS25+TT, stop10/trail20, gate)':'I6 breakout (RS25+TT, sim)'})
# I1 as it would be implemented on the live chassis (SMA200 universe filter)
m = allU['U7_midsmall_301_1000'] & trend
bk = topn_book(composite(F,['tight_close_15','q5_126'],m),m,FWD[1],n=15); i1,_ = chassis(bk['gross'],bk['turnover'])
S['I1 tight+persist (mid/small, live-style filter)'] = i1.set_axis(i1.index.to_period('M').to_timestamp('M'))
BUCKET=['Elendel (control)','Zenith','csm_absolute score','Residual mom (live-like)']
I1c='I1 tight+persist (mid/small, live-style filter)'; BR='I6 breakout (RS25+TT, sim)'; GD='Gold buy&hold'; I3='I3 low-risk (liquid)'
S['I3 low-risk (top250, no trend filter)'] = S['I3 low-risk (top250)']
I3c='I3 low-risk (top250, no trend filter)'
D = S.loc['2008-04-30':, BUCKET+[I1c,BR,GD,I3c]].dropna()
B = D[BUCKET].mean(axis=1)
def ps(r):
    a=stats(r); h=stats(r[r.index>HOLD]); return dict(cagr=a['cagr'],vol=a['vol'],sharpe=a['sharpe'],maxdd=a['maxdd'],calmar=a['calmar'],cagr_hold=h['cagr'],vol_hold=h['vol'],sharpe_hold=h['sharpe'],maxdd_hold=h['maxdd'])
W = {GD:0.10, I1c:0.15, I3c:0.10, BR:0.10}
rows=[dict(step='Live-like bucket only (4 books)',**ps(B))]
used=0; cur=None
for k,w in W.items():
    used+=w
    p = (1-used)*B + sum(W[j]*D[j] for j in list(W)[:list(W).index(k)+1])
    rows.append(dict(step=f'+ {k} ({int(w*100)}%)',**ps(p)))
G=pd.DataFrame(rows); G.to_csv('results/stage14_final_blend_steps.csv',index=False,float_format='%.4f')
final = (1-used)*B + sum(W[j]*D[j] for j in W)
def block_boot(a, f, reps=3000, blk=6):
    n=len(a); out=[]
    for _ in range(reps):
        idx=[]
        while len(idx)<n:
            s=rng.integers(0,n); L_=min(rng.geometric(1/blk),n); idx.extend([(s+k)%n for k in range(L_)])
        out.append(f(a[np.array(idx[:n])]))
    return np.array(out)
arr = np.column_stack([B.values, final.values])
shd = lambda a: ((a[:,1]-CASH_M).mean()/a[:,1].std()-(a[:,0]-CASH_M).mean()/a[:,0].std())*np.sqrt(12)
bs = block_boot(arr, shd)
ddd = lambda a: (((1+a[:,1]).cumprod()/np.maximum.accumulate((1+a[:,1]).cumprod())-1).min()) - (((1+a[:,0]).cumprod()/np.maximum.accumulate((1+a[:,0]).cumprod())-1).min())
bd = block_boot(arr, ddd, reps=1500)
print('final blend dSharpe: point %.3f  90%% CI [%.3f, %.3f]  P>0 %.3f'%(shd(arr),np.percentile(bs,5),np.percentile(bs,95),(bs>0).mean()))
print('final blend dMaxDD: point %.3f  90%% CI [%.3f, %.3f]  P(better) %.3f'%(ddd(arr),np.percentile(bd,5),np.percentile(bd,95),(bd>0).mean()))
pd.set_option('display.width',250); print(G.round(3).to_string(index=False))
# planning ranges: Sharpe haircut 0.5x-0.8x of the 2015+ Sharpe; CAGR ~ rf + S*vol - vol^2/2 ; maxDD x1.25..1.5
rows=[]
for nm,col in (('I1 tight+persist (mid/small, live-style filter)',I1c),('I6 breakout (RS25+TT, sim)',BR),('I3 low-risk (top250, no trend filter)',I3c),('Gold buy&hold',GD),('Live-like bucket',None)):
    r = (B if col is None else S[col]).dropna(); a=stats(r); h=stats(r[r.index>HOLD])
    lo,hi = 0.5*h['sharpe'], 0.8*h['sharpe']; v=h['vol']
    cg = lambda s: 0.06 + s*v - v*v/2
    rows.append(dict(idea=nm,cagr_full=a['cagr'],sharpe_full=a['sharpe'],maxdd_full=a['maxdd'],cagr_hold=h['cagr'],sharpe_hold=h['sharpe'],vol_hold=v,maxdd_hold=h['maxdd'],
                     plan_sharpe_lo=lo,plan_sharpe_hi=hi,plan_cagr_lo=cg(lo),plan_cagr_hi=cg(hi),plan_dd_lo=a['maxdd']*1.25,plan_dd_hi=a['maxdd']*1.5))
PL = pd.DataFrame(rows); PL.to_csv('results/stage14_planning_ranges.csv',index=False,float_format='%.4f'); print(PL.round(3).to_string(index=False))
fh = ps(final); bh = ps(B)
print('blend hold sharpe %.3f vs bucket %.3f ; planning delta sharpe +%.2f..+%.2f'%(fh['sharpe_hold'],bh['sharpe_hold'],0.5*(fh['sharpe_hold']-bh['sharpe_hold']),0.8*(fh['sharpe_hold']-bh['sharpe_hold'])))
pickle.dump(dict(final=final,B=B,D=D),open('.cache/stage14_final.pkl','wb'))
