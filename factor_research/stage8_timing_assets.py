import numpy as np, pandas as pd
import index_lab as L
from data import load_panels
from factors import rmean
from evaluate import nw_tstat, SPLIT
from scipy.stats import spearmanr
pd.set_option('display.width',250); pd.set_option('display.max_columns',50); pd.set_option('display.max_rows',100)
I,Ec,Ev,cal = L.prep(); sig = L.month_ends(cal)

# ---------- breadth from the stock panel ----------
P = load_panels(); Cf = P['close'].ffill(limit=5)
sma200 = rmean(Cf,200); sma50 = rmean(Cf,50)
valid = (Cf>20) & sma200.notna()
b200 = ((Cf>sma200)&valid).sum(axis=1)/valid.sum(axis=1)
v50 = (Cf>20)&sma50.notna(); b50 = ((Cf>sma50)&v50).sum(axis=1)/v50.sum(axis=1)
b200 = b200.reindex(cal).ffill(); b50 = b50.reindex(cal).ffill()
vix = I['India_VIX']

# ---------- cash ----------
liq = Ec['LIQUIDBEES']
cash_fwd = L.fwd_returns(pd.DataFrame({'c':liq}), cal, sig, (1,))[1]['c']
cm_default = (1+L.CASH_ANNUAL)**(1/12)-1
cash_fwd = cash_fwd.fillna(cm_default)
cash_fwd[cash_fwd.index < '2007-06-30'] = cm_default

# ---------- Part A: equity timing ----------
ASSETS = ['Nifty_50','Nifty_500','NIFTY_MIDCAP_100','NIFTY_SMLCAP_100','Nifty50_TR_2x_Lev']
A = I[ASSETS]
FW = L.fwd_returns(A, cal, sig, (1,3))
def sig_frame(name, asset_close):
    C = asset_close
    if name=='sma200': return (C > C.rolling(200,min_periods=150).mean()), (C/C.rolling(200,min_periods=150).mean()-1)
    if name=='sma50_200': return (C.rolling(50).mean() > C.rolling(200,min_periods=150).mean()), (C.rolling(50).mean()/C.rolling(200,min_periods=150).mean()-1)
    if name=='tsmom12': m=C/C.shift(252)-1; return (m>0), m
    if name=='near_high10': h=C/C.rolling(252,min_periods=200).max(); return (h>0.90), h
    if name=='breadth200_gt50': return (b200>0.5), b200
    if name=='breadth50_gt50': return (b50>0.5), b50
    if name=='vix_below_median': med=vix.rolling(252,min_periods=126).median(); return (vix<med), -(vix/med)
    if name=='vix_falling': m=vix.rolling(21).mean(); return (vix<m), -(vix/m)
    if name=='rv21_below_median':
        rv=C.pct_change().rolling(21).std(); med=rv.rolling(252,min_periods=126).median(); return (rv<med), -(rv/med)
    raise KeyError(name)
SIGS = ['sma200','sma50_200','tsmom12','near_high10','breadth200_gt50','breadth50_gt50','vix_below_median','vix_falling','rv21_below_median']
rows=[]
for a in ASSETS:
    C = A[a]
    ret1 = FW[1][a]
    start = C.first_valid_index() + pd.Timedelta(days=365)
    votes = {}
    for s in SIGS + ['vote_sma200_breadth_vix','vote_sma200_breadth']:
        if s=='vote_sma200_breadth_vix':
            on = (sig_frame('sma200',C)[0].astype(int)+sig_frame('breadth200_gt50',C)[0].astype(int)+sig_frame('vix_below_median',C)[0].astype(int))>=2; cont=None
        elif s=='vote_sma200_breadth':
            on = (sig_frame('sma200',C)[0].astype(int)+sig_frame('breadth200_gt50',C)[0].astype(int))>=1; cont=None
            on = (sig_frame('sma200',C)[0] & sig_frame('breadth200_gt50',C)[0]) | (sig_frame('sma200',C)[0]) ; on=sig_frame('sma200',C)[0]&sig_frame('breadth200_gt50',C)[0]
        else:
            on, cont = sig_frame(s, C)
        if s.startswith('vix') or s.startswith('vote') and 'vix' in s:
            st_ = max(start, vix.first_valid_index()+pd.Timedelta(days=365))
        else: st_=start
        on_m = on.reindex(sig).astype(float)
        idx = [d for d in sig if d>=st_ and d in ret1.index and pd.notna(ret1[d])]
        o = on_m.loc[idx]; r = ret1.loc[idx]; c = cash_fwd.loc[idx]
        # strategy: ON -> asset, OFF -> cash ; cost 0.05% each side on switch
        sw = o.diff().abs().fillna(0)
        net = o*r + (1-o)*c - 0.0005*sw*2
        bh = r
        stt = L.stats(net); sbh = L.stats(bh)
        d1,d2 = net.index<=SPLIT, net.index>SPLIT
        row = dict(asset=a, signal=s, start=idx[0].date(), pct_on=o.mean(), cagr=stt['cagr'], vol=stt['vol'], sharpe=stt['sharpe'], maxdd=stt['maxdd'], calmar=stt['calmar'],
                   bh_cagr=sbh['cagr'], bh_maxdd=sbh['maxdd'], bh_sharpe=sbh['sharpe'],
                   dd_cut=stt['maxdd']-sbh['maxdd'], sharpe_disc=L.stats(net[d1])['sharpe'] if d1.sum()>24 else np.nan, sharpe_hold=L.stats(net[d2])['sharpe'] if d2.sum()>24 else np.nan,
                   switches_per_yr=sw.sum()/(len(sw)/12))
        # accuracy: P(r>cash | ON), P(r<cash | OFF), balanced
        exc = r-c
        row['acc_on'] = (exc[o==1]>0).mean() if (o==1).any() else np.nan
        row['acc_off'] = (exc[o==0]<0).mean() if (o==0).any() else np.nan
        row['balanced_acc'] = np.nanmean([row['acc_on'],row['acc_off']])
        row['mean_exc_on'] = exc[o==1].mean(); row['mean_exc_off'] = exc[o==0].mean()
        if cont is not None:
            cm_ = cont.reindex(sig).loc[idx]
            ok = cm_.notna()
            ic = spearmanr(cm_[ok], r[ok]).correlation
            # rolling-year IC series for ICIR (annual blocks)
            yr = pd.DataFrame({'x':cm_[ok],'y':r[ok]}); yr['yr']=yr.index.year
            yic = yr.groupby('yr').apply(lambda g: spearmanr(g.x,g.y).correlation if len(g)>=8 else np.nan).dropna()
            row.update(ts_ic1=ic, ts_ic_yr_mean=yic.mean(), ts_icir_yr=yic.mean()/yic.std() if yic.std()>0 else np.nan, ts_yrs_pos=(yic>0).mean())
        rows.append(row)
T = pd.DataFrame(rows); T.to_csv('results/stage8_timing.csv',index=False,float_format='%.4f')
c=['asset','signal','start','pct_on','cagr','bh_cagr','maxdd','bh_maxdd','sharpe','bh_sharpe','calmar','sharpe_disc','sharpe_hold','balanced_acc','acc_on','acc_off','ts_ic1','ts_yrs_pos','switches_per_yr']
for a in ASSETS:
    print('=====',a); print(T[T.asset==a][c].round(3).to_string(index=False))
