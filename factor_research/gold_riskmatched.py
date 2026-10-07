import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from portfolio_lab import stats
rng = np.random.default_rng(5); CASH_M=1.06**(1/12)-1
N = pd.read_csv('results/gold_rules_monthly.csv',index_col=0,parse_dates=True); E = pd.read_csv('results/gold_rules_exposure.csv',index_col=0,parse_dates=True)
S = pd.read_csv('results/stage14_monthly_returns.csv',index_col=0,parse_dates=True)
B = S[['Elendel (control)','Zenith','csm_absolute score','Residual mom (live-like)']].mean(axis=1)
N.index=N.index.to_period('M'); B.index=B.index.to_period('M'); B=B.reindex(N.index); ok=B.notna(); N,B=N[ok],B[ok]
segA=N.index<=pd.Period('2010-12'); segB=N.index>=pd.Period('2015-01')
v0 = N['G0 buy&hold'].std()
def blend(x,w): return (1-w)*B+w*x
base = stats(B)
rows=[]
ref = blend(N['G0 buy&hold'],0.10); refs=stats(ref)
for k in N.columns:
    w = min(0.30, 0.10*v0/N[k].std())
    p = blend(N[k],w); s=stats(p)
    sa,sb = stats(p[segA]), stats(p[segB]); ra,rb = stats(ref[segA]), stats(ref[segB])
    # bootstrap P(blend Sharpe > reference B&H@10%)
    arr=np.column_stack([p.values,ref.values]); n=len(arr); d=[]
    for _ in range(2500):
        idx=[]; 
        while len(idx)<n:
            st=rng.integers(0,n); Lb=min(rng.geometric(1/6),n); idx.extend([(st+j)%n for j in range(Lb)])
        a=arr[np.array(idx[:n])]; d.append(((a[:,0]-CASH_M).mean()/a[:,0].std()-(a[:,1]-CASH_M).mean()/a[:,1].std())*np.sqrt(12))
    d=np.array(d)
    rows.append(dict(rule=k,weight_riskmatched=w,sleeve_vol=N[k].std()*np.sqrt(12),blend_cagr=s['cagr'],blend_sharpe=s['sharpe'],blend_maxdd=s['maxdd'],blend_calmar=s['calmar'],
        dSharpe_vs_BH10=s['sharpe']-refs['sharpe'],dMaxDD_vs_BH10=s['maxdd']-refs['maxdd'],P_beats_BH=(d>0).mean(),
        dSharpe_A=sa['sharpe']-ra['sharpe'],dSharpe_B=sb['sharpe']-rb['sharpe'],dMaxDD_A=sa['maxdd']-ra['maxdd'],dMaxDD_B=sb['maxdd']-rb['maxdd']))
R=pd.DataFrame(rows).set_index('rule'); R.to_csv('results/gold_riskmatched.csv',float_format='%.4f')
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
print('bucket alone: Sharpe %.3f MaxDD %.3f CAGR %.3f | B&H gold @10%%: Sharpe %.3f MaxDD %.3f CAGR %.3f'%(base['sharpe'],base['maxdd'],base['cagr'],refs['sharpe'],refs['maxdd'],refs['cagr']))
print(R.round(3).to_string())
