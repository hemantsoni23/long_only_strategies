"""Decision-grade evaluation of every idea on a common chassis.
Outputs (results/stage14_*.csv): monthly return series, core stats, bootstrap, cost/capacity, portfolio marginal value."""
import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from data import load_panels
from factors import Ctx
from evaluate import composite, SPLIT
from portfolio_lab import topn_book, stats
import index_lab as L

st = pickle.load(open('.cache/state.pkl','rb')); F,FWD,U,sig = st['F'],st['FWD'],st['U'],st['sig']
UN = pickle.load(open('.cache/extra_universes.pkl','rb')); allU = dict(U); allU.update(UN)
P = load_panels(); b = P['bench']
bull = (b > b.rolling(200,min_periods=150).mean()).reindex(sig).fillna(True)
CASH_M = 1.06**(1/12)-1
PER = lambda idx: idx.to_period('M')

IDEAS = {   # name: (components, universe)
 'Elendel (control)':      (['a3_rs_high','q5_126'], 'U1_liquid1000'),
 'Zenith':                 (['a1_52wh','q5_189'], 'U1_liquid1000'),
 'csm_absolute score':     (['csm_abs_dual_sharpe'], 'U4_top250'),
 'Residual mom (live-like)':(['mom_resid_12_1'], 'U1_liquid1000'),
 'I0 persistence only (q5_126)': (['q5_126'], 'U1_liquid1000'),
 'I1 tight+persist (mid/small)': (['tight_close_15','q5_126'], 'U7_midsmall_301_1000'),
 'I1 tight+persist (liquid)':    (['tight_close_15','q5_126'], 'U1_liquid1000'),
 'I2 resid+persist (liquid)':    (['mom_resid_12_1','q5_126'], 'U1_liquid1000'),
 'I2 resid+persist (top250)':    (['mom_resid_12_1','q5_126'], 'U4_top250'),
 'I3 low-risk (liquid)':         (['lowvol_126','low_ulcer_252'], 'U1_liquid1000'),
 'I3 low-risk (top250)':         (['lowvol_126','low_ulcer_252'], 'U4_top250'),
 'I4 intraday+ulcer (top250)':   (['intra_over_252','low_ulcer_252'], 'U4_top250'),
 'I7 anchor+pain (liquid)':      (['hi_3y','low_pain_126'], 'U1_liquid1000'),
}

def make_score(comps, mask):
    return composite(F, comps, mask) if len(comps)>1 else F[comps[0]].where(mask)

def book(name, cost=0.003, n=15):
    comps, u = IDEAS[name]; m = allU[u]
    bk = topn_book(make_score(comps, m), m, FWD[1], n=n, cost=cost)
    return bk

def chassis(gross, turnover, cost=0.003, gate=True, vt=True, lag_idx=None):
    """gross: monthly gross book return. Applies costs, then SMA200 gate (50% in bear) and 20% vol target (lagged), with cost on exposure changes."""
    net = gross - 2*cost*turnover
    if not (gate or vt): return net, pd.Series(1.0,index=net.index)
    g = pd.Series(np.where(bull.reindex(net.index).values,1.0,0.5), index=net.index) if gate else pd.Series(1.0,index=net.index)
    if vt:
        rv = net.rolling(6).std().shift(1)*np.sqrt(12)
        ex = (0.20/rv).clip(upper=1.0).fillna(1.0)
    else: ex = pd.Series(1.0,index=net.index)
    expo = np.minimum(g, ex)
    out = expo*net + (1-expo)*CASH_M - cost*expo.diff().abs().fillna(0)
    return out, expo

if __name__ == '__main__':
    series = {}; raw = {}
    for nm in IDEAS:
        bk = book(nm)
        out,_ = chassis(bk['gross'], bk['turnover'])
        series[nm] = out; raw[nm] = bk
    # ---- index/ETF ideas (pre-specified ensembles, no best-of selection) ----
    I,Ec,Ev,cal = L.prep(); isig = L.month_ends(cal)
    AC = pd.DataFrame({'Nifty50':I['Nifty_50'],'Midcap100':I['NIFTY_MIDCAP_100'],'Smallcap100':I['NIFTY_SMLCAP_100'],'Gold':Ec['GOLDBEES']}).loc['2006-01-01':]
    FW = L.fwd_returns(AC, cal, isig, (1,))
    Fd = {n:f.reindex(isig) for n,f in L.asset_factors(AC).items()}
    start = pd.Timestamp('2008-03-31')
    liq = Ec['LIQUIDBEES']; cash1 = L.fwd_returns(pd.DataFrame({'c':liq}),cal,isig,(1,))[1]['c'].fillna(CASH_M); cash1[cash1.index<'2007-06-30']=CASH_M
    m12 = (AC/AC.shift(252)-1).reindex(isig); cash12=(liq/liq.shift(252)-1).reindex(isig).fillna(0.06); absf = m12.gt(cash12,axis=0)
    cfg=[]
    for fac in ['mom_6_1','mom_12_1','sharpe_6_1','q5_126','mom_3_0','hi_252']:
        for k in (1,2):
            for gate in (False,True):
                bk = L.run_book(Fd[fac].loc[start:], FW[1], k=k, cost=0.001, abs_filter=absf if gate else None, cash_m=cash1)
                cfg.append(bk['net'][bk.index>=start])
    X1 = pd.concat(cfg,axis=1).mean(axis=1)
    series['X1 asset rotation (ensemble of 24 configs)'] = X1
    series['Gold buy&hold'] = FW[1]['Gold'].loc[start:]
    SECT = ['Nifty_Bank','Nifty_IT','Nifty_Pharma','Nifty_FMCG','Nifty_Auto','Nifty_Metal','Nifty_Energy','Nifty_Infra','Nifty_PSU_Bank','Nifty_Pvt_Bank','Nifty_Fin_Service','Nifty_Media','Nifty_MNC','Nifty_PSE','Nifty_CPSE','Nifty_Commodities','Nifty_Consumption','Nifty_Realty','Nifty_Serv_Sector']
    Cs=I[SECT]; Fs={n:f.reindex(isig) for n,f in L.asset_factors(Cs,bench=I['Nifty_500']).items()}; FWs=L.fwd_returns(Cs,cal,isig,(1,))
    sma=(Cs>L.rm(Cs,200).mean()).reindex(isig)
    cs=[]
    for fac in ['mom_6_1','mom_12_1','sharpe_6_1','q5_126','hi_252','low_ulcer_126','lowvol_126','mom_3_0','rs_near_high']:
        for filt in (False,True):
            bk=L.run_book(Fs[fac].loc['2005-01-31':],FWs[1],k=3,cost=0.001,abs_filter=sma if filt else None)
            cs.append(bk['net'])
    series['X4 sector rotation (ensemble of 18 configs)'] = pd.concat(cs,axis=1).mean(axis=1)
    S = pd.DataFrame({k:v.rename(k).set_axis(PER(v.index)) for k,v in series.items()})
    S.index = S.index.to_timestamp('M')
    S.to_csv('results/stage14_monthly_returns.csv', float_format='%.6f')
    pickle.dump(raw, open('.cache/stage14_raw_books.pkl','wb'))
    print(S.shape, S.index.min(), S.index.max())
