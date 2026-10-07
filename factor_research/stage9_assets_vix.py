import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
import index_lab as L
from evaluate import nw_tstat, SPLIT
from scipy.stats import spearmanr
pd.set_option('display.width',250); pd.set_option('display.max_columns',50); pd.set_option('display.max_rows',100)
I,Ec,Ev,cal = L.prep(); sig = L.month_ends(cal)
vix = I['India_VIX']
liq = Ec['LIQUIDBEES']
cm_default = (1+L.CASH_ANNUAL)**(1/12)-1

# ======== A. Asset-class dual momentum: Nifty50 / Midcap100 / Smallcap100 / Gold ========
gold = Ec['GOLDBEES']
AC = pd.DataFrame({'Nifty50':I['Nifty_50'],'Midcap100':I['NIFTY_MIDCAP_100'],'Smallcap100':I['NIFTY_SMLCAP_100'],'Gold':gold})
AC = AC.loc['2006-01-01':]
FW = L.fwd_returns(AC, cal, sig, (1,3,6))
cash1 = L.fwd_returns(pd.DataFrame({'c':liq}), cal, sig, (1,))[1]['c'].fillna(cm_default)
cash1[cash1.index<'2007-06-30'] = cm_default
Fd = L.asset_factors(AC)
F = {n:f.reindex(sig) for n,f in Fd.items()}
start = pd.Timestamp('2008-03-31')   # gold ETF history + 12m warmup
F = {n:f.loc[start:] for n,f in F.items()}
tab = L.ic_table(F, FW, min_n=4)
tab.to_csv('results/stage9_asset_ic.csv', float_format='%.4f')
print('--- asset-class cross-sectional IC (N=4 assets)'); print(tab[['ic_1','hit_1','t_1','ic_3','hit_3','t_3','ic_6','hit_6','n_months']].round(3).sort_values('ic_3',ascending=False).to_string())
rows=[]
ew = FW[1].loc[start:].mean(axis=1)
for fac in ['mom_6_1','mom_12_1','sharpe_6_1','q5_126','mom_3_0','hi_252']:
    for k in (1,2):
        for gate in ('none','abs>cash'):
            ab=None
            if gate=='abs>cash':
                m12 = (AC/AC.shift(252)-1).reindex(sig)
                cash12 = (liq/liq.shift(252)-1).reindex(sig).fillna(L.CASH_ANNUAL)
                ab = m12.gt(cash12, axis=0)
            b = L.run_book(F[fac], FW[1], k=k, cost=0.001, abs_filter=ab, cash_m=cash1)
            b = b[b.index>=start]
            s=L.stats(b['net']); sd=L.stats(b['net'][b.index<=L.SPLIT]); sh=L.stats(b['net'][b.index>L.SPLIT])
            rows.append(dict(factor=fac,k=k,gate=gate,cagr=s['cagr'],vol=s['vol'],sharpe=s['sharpe'],maxdd=s['maxdd'],calmar=s['calmar'],sharpe_disc=sd['sharpe'],sharpe_hold=sh['sharpe'],cagr_hold=sh['cagr'],turn=b['turn'].mean(),
                             hit_vs_ew=(b['net']>ew.reindex(b.index)).mean(), hit_vs_cash=(b['net']>cash1.reindex(b.index)).mean()))
AB = pd.DataFrame(rows); AB.to_csv('results/stage9_asset_books.csv',index=False,float_format='%.4f')
print('EW 4 assets:',{k:round(v,3) for k,v in L.stats(ew[ew.index>=start]).items()})
for c in AC: print(c, {k:round(v,3) for k,v in L.stats(FW[1][c][FW[1].index>=start]).items() if k in('cagr','vol','sharpe','maxdd')})
print(AB.round(3).to_string(index=False))

# ======== B. VIX contrarian / re-entry study ========
print('\n--- VIX study (2009+)')
vp = vix.rolling(504,min_periods=252).apply(lambda x: (x[-1]>=x).mean(), raw=True)   # trailing 2y percentile
vsp = vix/vix.rolling(252,min_periods=126).median()
vch = vix/vix.shift(21)-1
sig_v = {'vix_pctile_2y':vp,'vix_over_median':vsp,'vix_chg_21d':vch}
tgt = {'Nifty_50':I['Nifty_50'],'Nifty_500':I['Nifty_500'],'MIDCAP100':I['NIFTY_MIDCAP_100'],'SMLCAP100':I['NIFTY_SMLCAP_100']}
FWv = L.fwd_returns(pd.DataFrame(tgt), cal, sig, (1,3))
rows=[]
for a in tgt:
    for sname, s in sig_v.items():
        x = s.reindex(sig)
        for h in (1,3):
            y = FWv[h][a]; ok = x.notna()&y.notna()&(x.index>=pd.Timestamp('2010-06-30'))
            ic = spearmanr(x[ok],y[ok]).correlation
            d = pd.DataFrame({'x':x[ok],'y':y[ok]})
            # hit: top-quintile (high VIX) vs rest -> P(fwd>0)
            q = d.x.quantile(0.8); hi = d[d.x>=q]; lo = d[d.x<q]
            # NW t of IC via block annual
            rows.append(dict(asset=a,signal=sname,h=h,ts_ic=ic,n=int(ok.sum()),mean_fwd_hiVIX=hi.y.mean(),mean_fwd_rest=lo.y.mean(),p_up_hiVIX=(hi.y>0).mean(),p_up_rest=(lo.y>0).mean(),n_hi=len(hi)))
V = pd.DataFrame(rows); V.to_csv('results/stage9_vix_study.csv',index=False,float_format='%.4f')
print(V.round(3).to_string(index=False))

# ======== C. Factor-index regime table ========
FI = {'Momentum30(N200)':'Nifty200Momentm30','LowVol30(N100)':'NIFTY100_LowVol30','Quality30(N200)':'NIFTY200_QUALTY30','Alpha50':'NIFTY_Alpha_50','Alpha30(N200)':'Nifty200_Alpha_30','AlphaLowVol':'NIFTY_AlphaLowVol','Value20(N50)':'Nifty50_Value_20','Quality30(N100)':'NIFTY100_Qualty30','Midcap150Mom50':'NiftyM150Momntm50'}
FIdf = pd.DataFrame({k:I[v] for k,v in FI.items() if v in I})
base = I['Nifty_500']
FWf = L.fwd_returns(pd.concat([FIdf, base.rename('Nifty500')],axis=1), cal, sig, (1,3))
bull = (base>base.rolling(200,min_periods=150).mean()).reindex(sig)
vixhi = (vix>vix.rolling(252,min_periods=126).median()).reindex(sig)
dd = (base/base.rolling(252,min_periods=200).max()-1).reindex(sig)
rows=[]
for k in FIdf.columns:
    ex = (FWf[1][k]-FWf[1]['Nifty500'])
    ok = ex.notna()
    for reg,mask in [('all',pd.Series(True,index=sig)),('bull',bull),('bear',~bull),('VIX>median',vixhi),('VIX<=median',~vixhi),('mkt DD>10%',dd<-0.10)]:
        m = ok & mask.reindex(ex.index).fillna(False)
        e = ex[m]
        rows.append(dict(index=k,regime=reg,n=len(e),mean_excess_m=e.mean(),hit_beats_n500=(e>0).mean(),t=e.mean()/(e.std()/np.sqrt(len(e))) if len(e)>5 else np.nan, start=FIdf[k].first_valid_index().date()))
FR = pd.DataFrame(rows); FR.to_csv('results/stage9_factor_index_regimes.csv',index=False,float_format='%.4f')
print('\n--- factor index excess vs Nifty500 (monthly)')
print(FR.pivot(index='index',columns='regime',values='mean_excess_m').round(4).to_string())
print(FR.pivot(index='index',columns='regime',values='hit_beats_n500').round(3).to_string())
