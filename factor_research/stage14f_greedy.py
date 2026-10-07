import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from portfolio_lab import stats
CASH_M=1.06**(1/12)-1; HOLD=pd.Timestamp('2014-12-31')
S = pd.read_csv('results/stage14_monthly_returns.csv',index_col=0,parse_dates=True).loc[:'2026-06-30']
S = S.join(pd.read_csv('results/stage14_breakout_monthly_aligned.csv',index_col=0,parse_dates=True),how='left')
S = S.rename(columns={'I6 breakout sim (52w-high+RS25+TT, stop10/trail20, gate)':'I6 breakout (RS25+TT, sim)'})
BUCKET=['Elendel (control)','Zenith','csm_absolute score','Residual mom (live-like)']
CANDS=['I1 tight+persist (mid/small)','I6 breakout (RS25+TT, sim)','Gold buy&hold','X1 asset rotation (ensemble of 24 configs)','I3 low-risk (top250)','I2 resid+persist (top250)','I4 intraday+ulcer (top250)','I0 persistence only (q5_126)']
D = S.loc['2008-04-30':,BUCKET+CANDS].dropna()
B = D[BUCKET].mean(axis=1)
def ps(r):
    a=stats(r); h=stats(r[r.index>HOLD]); return dict(cagr=a['cagr'],vol=a['vol'],sharpe=a['sharpe'],maxdd=a['maxdd'],calmar=a['calmar'],cagr_hold=h['cagr'],sharpe_hold=h['sharpe'],maxdd_hold=h['maxdd'])
cur = B.copy(); w_each = 0.15; chosen=[]; rows=[dict(step=0,added='(live-like bucket)',**ps(cur))]
avail=list(CANDS)
for step in range(1,6):
    best=None
    for c in avail:
        p=(1-w_each)*cur+w_each*D[c]; s=ps(p)
        score = s['sharpe']+0.5*s['calmar']
        if best is None or score>best[0]: best=(score,c,p,s)
    prev=ps(cur)
    gain = (best[3]['sharpe']-prev['sharpe'])+0.5*(best[3]['calmar']-prev['calmar'])
    if gain<0.02: break
    cur=best[2]; avail.remove(best[1]); chosen.append(best[1]); rows.append(dict(step=step,added=best[1],**best[3]))
G=pd.DataFrame(rows); G.to_csv('results/stage14_greedy.csv',index=False,float_format='%.4f')
pd.set_option('display.width',250); print(G.round(3).to_string(index=False))
# pre-specified sleeve blend for the roadmap (weights fixed, not optimised)
w = {'bucket':0.55,'I1 tight+persist (mid/small)':0.15,'I6 breakout (RS25+TT, sim)':0.10,'Gold buy&hold':0.10,'I3 low-risk (top250)':0.10}
blend = w['bucket']*B + sum(v*D[k] for k,v in w.items() if k!='bucket')
print('\nspec blend 55% bucket/15% I1/10% breakout/10% gold/10% low-risk:', {k:round(v,3) for k,v in ps(blend).items()})
print('bucket alone:', {k:round(v,3) for k,v in ps(B).items()})
print('corr matrix of sleeves:'); print(pd.concat([B.rename('bucket'),D[CANDS]],axis=1).corr().round(2).iloc[0].to_dict())
