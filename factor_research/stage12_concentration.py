import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from data import load_panels
from evaluate import composite, SPLIT
from portfolio_lab import topn_book, stats
st = pickle.load(open('.cache/state.pkl','rb')); F,FWD,U,sig = st['F'],st['FWD'],st['U'],st['sig']
UN = pickle.load(open('.cache/extra_universes.pkl','rb')); allU = dict(U); allU.update(UN)
P = load_panels(); b = P['bench']
bull = (b > b.rolling(200,min_periods=150).mean()).reindex(sig).fillna(True)
cash_m=(1.06)**(1/12)-1
PK = {'LIVE_elendel':['a3_rs_high','q5_126'],'P4_resid+persist':['mom_resid_12_1','q5_126'],'P6_tight+persist':['tight_close_15','q5_126'],'csm_abs_score':['csm_abs_dual_sharpe'],'P2_low_risk':['lowvol_126','low_ulcer_252']}
rows=[]
for u in ['U1_liquid1000','U7_midsmall_301_1000']:
    m=allU[u]
    for pn,c in PK.items():
        sc=composite(F,c,m) if len(c)>1 else F[c[0]].where(m)
        for n in (8,10,15,25):
            bk=topn_book(sc,m,FWD[1],n=n)
            net=bk['net']
            gate=np.where(bull.reindex(net.index).values,1.0,0.5)
            g=gate*net+(1-gate)*cash_m
            # vol-target overlay: exposure = min(1, 20%/trailing-6m annualised vol of the book's own net returns), lagged one month
            rv=net.rolling(6).std().shift(1)*np.sqrt(12)
            ex=(0.20/rv).clip(upper=1.0).fillna(1.0)
            v=ex*net+(1-ex)*cash_m
            gv=np.minimum(gate, ex.values)*net + (1-np.minimum(gate,ex.values))*cash_m
            for tag,s_ in (('plain',net),('sma200_gate50',g),('voltarget20',v),('gate+voltarget',gv)):
                s=stats(s_); sh=stats(s_[s_.index>SPLIT])
                rows.append(dict(universe=u,pack=pn,n=n,overlay=tag,cagr=s['cagr'],vol=s['vol'],sharpe=s['sharpe'],maxdd=s['maxdd'],calmar=s['calmar'],sharpe_hold=sh['sharpe'],cagr_hold=sh['cagr'],maxdd_hold=sh['maxdd'],turnover=bk['turnover'].mean()))
d=pd.DataFrame(rows); d.to_csv('results/stage12_concentration_overlays.csv',index=False,float_format='%.4f')
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
for u in ['U1_liquid1000','U7_midsmall_301_1000']:
    x=d[(d.universe==u)&(d.overlay.isin(['plain','gate+voltarget']))]
    print('=====',u); print(x.pivot_table(index=['pack','overlay'],columns='n',values=['cagr','maxdd','sharpe']).round(3).to_string())
