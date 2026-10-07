"""Prototype portfolio for I6 (RS-gated breakout). 20 slots, equal weight of current equity, entry = close of signal day+1,
exit = close of the day AFTER a close-based stop/trail trigger, 0.3% one-way cost, idle cash at 6%. No parameter tuning: 3 pre-set exit variants x gate on/off."""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from data import load_panels
from factors import Ctx, rmean, rmax, rmin
from portfolio_lab import stats
P = load_panels(); X = Ctx(P); idx = X.C.index
Cf,Hf,Lf,V = X.Cf,X.Hf,X.Lf,X.V
dv = X.DV.rolling(63,min_periods=21).median(); rank = dv.rank(axis=1,ascending=False,method='min')
circ = ((X.H==X.L)&X.H.notna()).astype('float64').rolling(63,min_periods=1).sum()<=5
uni = Cf.notna()&(Cf>20)&(rank<=1000)&circ
s50,s150,s200 = rmean(Cf,50),rmean(Cf,150),rmean(Cf,200)
TT = (Cf>s50)&(s50>s150)&(s150>s200)&(s200>s200.shift(21))&(Cf>=0.75*rmax(Hf,252))&(Cf>=1.3*rmin(Lf,252))
mom6 = (Cf.shift(21)/Cf.shift(126)-1).where(uni); rs = mom6.rank(axis=1,pct=True)
rs_top = rs>=0.75
def fresh(flag,g=10):
    prior = flag.shift(1).astype('float64').rolling(g,min_periods=1).max().fillna(0)>0
    return flag&~prior
brk52 = fresh(Cf>rmax(Cf,252).shift(1)); don55 = fresh(Cf>rmax(Hf,55).shift(1))
SIG = {'52w-high + RS25 + TT': brk52&rs_top&TT&uni, 'Donchian55 + RS25 + TT': don55&rs_top&TT&uni,
       '52w-high (ungated)': brk52&uni}
Cff = X.C.ffill(); r = Cff.pct_change(fill_method=None); r = r.where((r>-0.4)&(r<3.0),0.0).fillna(0.0)
LP = np.log1p(r).cumsum().values   # log price (clean)
bench = P['bench']; bull = (bench>bench.rolling(200,min_periods=150).mean()).reindex(idx).fillna(True).values
rsv = rs.values; T,N = LP.shape; cash_d = 1.06**(1/252)-1
def run(sigdf, stop, trail, gate, slots=20, cost=0.003):
    sg = sigdf.values; eq=1.0; cash=1.0; pos={}; pend=set(); eqs=np.zeros(T); ntr=[]; 
    for t in range(1,T):
        # accrue cash interest
        cash *= (1+cash_d)
        # exits pending from yesterday's trigger -> sell at today's close
        for j in list(pend):
            if j in pos:
                val = pos[j]['sh']*np.exp(LP[t,j]); cash += val*(1-cost); ntr.append(np.exp(LP[t,j]-pos[j]['e'])*(1-cost)/(1+cost)-1); del pos[j]
            pend.discard(j)
        # mark & trigger
        for j,p in pos.items():
            px = np.exp(LP[t,j]); p['pk']=max(p['pk'],px)
            if px<=p['ep']*(1-stop) or px<=p['pk']*(1-trail): pend.add(j)
        # entries: signals of day t-1 -> enter at close t
        if t>=2 and (not gate or bull[t-1]):
            cand = np.where(sg[t-1])[0]
            if len(cand):
                cand = [j for j in cand[np.argsort(-np.nan_to_num(rsv[t-1,cand]))] if j not in pos]
                eqv = cash+sum(p['sh']*np.exp(LP[t,j]) for j,p in pos.items())
                for j in cand:
                    if len(pos)>=slots: break
                    size = eqv/slots
                    if cash < size*(1+cost): break
                    px = np.exp(LP[t,j]); sh = size/px; cash -= size*(1+cost)
                    pos[j]={'sh':sh,'ep':px,'pk':px,'e':LP[t,j]}
        eqs[t] = cash+sum(p['sh']*np.exp(LP[t,j]) for j,p in pos.items())
    s = pd.Series(eqs,index=idx); s = s[s>0]
    return s, np.array(ntr)
rows=[]; monthly={}
for sname,sdf in SIG.items():
    for (stop,trail) in ((0.08,0.15),(0.10,0.20),(0.12,0.25)):
        for gate in (True,False):
            e,ntr = run(sdf,stop,trail,gate)
            m = e.resample('ME').last().pct_change().dropna()
            a=stats(m); h=stats(m[m.index>'2014-12-31'])
            rows.append(dict(signal=sname,stop=stop,trail=trail,gate=gate,cagr=a['cagr'],vol=a['vol'],sharpe=a['sharpe'],maxdd=a['maxdd'],calmar=a['calmar'],cagr_hold=h['cagr'],sharpe_hold=h['sharpe'],maxdd_hold=h['maxdd'],
                trades=len(ntr),win_rate=(ntr>0).mean(),avg_win=ntr[ntr>0].mean(),avg_loss=ntr[ntr<=0].mean(),expectancy=ntr.mean(),payoff=ntr[ntr>0].mean()/abs(ntr[ntr<=0].mean())))
            monthly[(sname,stop,trail,gate)] = m
        print(sname,'done',flush=True)
D = pd.DataFrame(rows); D.to_csv('results/stage14_breakout_sim.csv',index=False,float_format='%.4f')
pd.set_option('display.width',260); pd.set_option('display.max_columns',30)
print(D.round(3).to_string(index=False))
# correlation of the main variant with the control book
S = pd.read_csv('results/stage14_monthly_returns.csv',index_col=0,parse_dates=True)
m = monthly[('52w-high + RS25 + TT',0.10,0.20,True)]; m.index=m.index.to_period('M').to_timestamp('M')
pd.DataFrame({'brk':m}).to_csv('results/stage14_breakout_monthly.csv',float_format='%.6f')
j = pd.concat([m,S['Elendel (control)']],axis=1).dropna(); print('corr with Elendel book:',round(j.corr().iloc[0,1],2),' n=',len(j))
