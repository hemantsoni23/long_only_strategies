import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from scipy.stats import spearmanr
from gold_data import *
from evaluate import nw_tstat
from data import load_panels
gold, vol, I, Ec, cal = load_gold(); sig = L.month_ends(cal)
g = gold.copy()                      # gap stays NaN
r = g.pct_change(fill_method=None)
rm = lambda x,w,mp=0.8: x.rolling(w,min_periods=int(w*mp))
feat = {}
feat['tsmom_12_1'] = g.shift(21)/g.shift(252)-1
feat['tsmom_6_1'] = g.shift(21)/g.shift(126)-1
feat['tsmom_3_0'] = g/g.shift(63)-1
feat['tsmom_1m'] = g/g.shift(21)-1
feat['dist_sma200'] = g/rm(g,200).mean()-1
feat['dist_sma100'] = g/rm(g,100).mean()-1
feat['persist_q5_126'] = (g>rm(g,50).mean()).where(g.notna()&rm(g,50).mean().notna()).astype(float).rolling(126,min_periods=100).mean()
feat['hi_252'] = g/rm(g,252).max()
feat['dd_from_peak_126'] = g/rm(g,126).max()-1
feat['sharpe_6_1'] = feat['tsmom_6_1']/rm(r,126).std()
feat['ker_126'] = (g-g.shift(126))/rm(g.diff().abs(),126).sum()
feat['lowvol_63'] = -rm(r,63).std()
feat['vol_ratio_21_126'] = -(rm(r,21).std()/rm(r,126).std())
# cross-asset context (all known at t)
N5 = I['Nifty_500']; b200 = N5/rm(N5,200).mean()-1
feat['eq_stress_sma200'] = -b200                          # higher = more equity stress
feat['eq_dd_252'] = -(N5/rm(N5,252).max()-1)
P = load_panels(); bench=P['bench'].reindex(cal).ffill()
feat['eq_breadth_neg'] = None
vix = I['India_VIX']; feat['vix_pctile_2y'] = vix.rolling(504,min_periods=252).apply(lambda x:(x[-1]>=x).mean(),raw=True)
gs = I['Nifty_GS_10Yr']; feat['bond_mom_6_0'] = gs/gs.shift(126)-1
feat['eq_mom_6_0_neg'] = -(N5/N5.shift(126)-1)
feat = {k:v for k,v in feat.items() if v is not None}
fwd1 = monthly_fwd_strict(g,cal,sig)
fwd3 = pd.Series([ (g.reindex(cal).values[cal.get_indexer([sig[k+3]])[0]+1]/g.reindex(cal).values[cal.get_indexer([sig[k]])[0]+1]-1) if k+3<len(sig) and cal.get_indexer([sig[k+3]])[0]+1<len(cal) else np.nan for k in range(len(sig))], index=sig)
rows=[]
for n,f in feat.items():
    x = f.reindex(sig)
    for h,y in ((1,fwd1),(3,fwd3)):
        d = pd.concat([x,y],axis=1,keys=['x','y']).dropna(); d=d.loc['2008-03-31':'2026-06-30']
        if len(d)<60: continue
        ic = spearmanr(d.x,d.y).correlation
        # annual-block IC series for stability
        yr = d.groupby(d.index.year).apply(lambda t: spearmanr(t.x,t.y).correlation if len(t)>=6 else np.nan).dropna()
        # NW t via sign test: regress rank-corr using HAC on standardized ranks
        xr=d.x.rank(); yr_=d.y.rank(); xs=(xr-xr.mean())/xr.std(); ys=(yr_-yr_.mean())/yr_.std()
        prod=xs*ys; t=nw_tstat(prod.values, max(h-1,0)+1)
        top = d[d.x>=d.x.quantile(0.5)].y.mean(); bot=d[d.x<d.x.quantile(0.5)].y.mean()
        rows.append(dict(signal=n,h=h,n=len(d),ts_ic=ic,t_nw=t,yrs_pos=(yr>0).mean(),mean_fwd_hi_half=top,mean_fwd_lo_half=bot,p_up_hi=(d[d.x>=d.x.quantile(0.5)].y>0).mean(),p_up_lo=(d[d.x<d.x.quantile(0.5)].y>0).mean()))
T=pd.DataFrame(rows); T.to_csv('results/gold_eda_signals.csv',index=False,float_format='%.4f')
pd.set_option('display.width',250); pd.set_option('display.max_rows',100)
print(T[T.h==1].sort_values('t_nw',ascending=False).round(3).to_string(index=False))
print(); print(T[T.h==3].sort_values('t_nw',ascending=False).round(3).to_string(index=False))
