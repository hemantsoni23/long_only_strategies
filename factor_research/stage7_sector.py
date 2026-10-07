import numpy as np, pandas as pd
import index_lab as L
pd.set_option('display.width',250); pd.set_option('display.max_columns',50); pd.set_option('display.max_rows',100)
I,Ec,Ev,cal = L.prep(); sig = L.month_ends(cal)
SECT = ['Nifty_Bank','Nifty_IT','Nifty_Pharma','Nifty_FMCG','Nifty_Auto','Nifty_Metal','Nifty_Energy','Nifty_Infra','Nifty_PSU_Bank','Nifty_Pvt_Bank',
        'Nifty_Fin_Service','Nifty_Media','Nifty_MNC','Nifty_PSE','Nifty_CPSE','Nifty_Commodities','Nifty_Consumption','Nifty_Realty','Nifty_Serv_Sector']
C = I[SECT]; bench = I['Nifty_500']
F_daily = L.asset_factors(C, bench=bench)
F = {n: f.reindex(sig) for n, f in F_daily.items()}
FWD = L.fwd_returns(C, cal, sig, (1,3,6))
# restrict to dates where >=12 sectors have data
cnt = C.reindex(sig).notna().sum(axis=1)
ok = cnt[cnt>=12].index
F = {n: f.loc[ok] for n,f in F.items()}
tab = L.ic_table(F, FWD, min_n=10)
tab.to_csv('results/stage7_sector_ic.csv', float_format='%.4f')
cols=['ic_1','icir_1','hit_1','t_1','ic_3','icir_3','hit_3','t_3','ic_6','icir_6','hit_6','ic_disc_3','ic_hold_3','n_months','avg_n']
print(tab.sort_values('icir_3',ascending=False)[cols].round(3).to_string())
# books
mkt1 = L.fwd_returns(I[['Nifty_500']], cal, sig, (1,))[1]['Nifty_500']
ew = FWD[1].loc[ok].mean(axis=1)
sma200 = (C > L.rm(C,200).mean()).reindex(sig)
rows=[]
for fac in ['mom_6_1','mom_12_1','sharpe_6_1','q5_126','hi_252','rs_6_1','low_ulcer_126','lowvol_126','mom_3_0']:
    for k in (3,):
        for filt in (False, True):
            b = L.run_book(F[fac], FWD[1], k=k, cost=0.001, abs_filter=sma200 if filt else None)
            b = b[b.index>=pd.Timestamp('2005-01-31')]
            s = L.stats(b['net']); sd=L.stats(b['net'][b.index<=L.SPLIT]); sh=L.stats(b['net'][b.index>L.SPLIT])
            rows.append(dict(factor=fac,k=k,trend_filter=filt,cagr=s['cagr'],vol=s['vol'],sharpe=s['sharpe'],maxdd=s['maxdd'],calmar=s['calmar'],sharpe_disc=sd['sharpe'],sharpe_hold=sh['sharpe'],cagr_hold=sh['cagr'],turn=b['turn'].mean(),
                             hit_vs_ew=(b['net']>ew.reindex(b.index)).mean()))
bk = pd.DataFrame(rows); bk.to_csv('results/stage7_sector_books.csv',index=False,float_format='%.4f')
ewb = ew[ew.index>=pd.Timestamp('2005-01-31')]; print('EW sectors:',{k:round(v,3) for k,v in L.stats(ewb).items()})
m = mkt1[mkt1.index>=pd.Timestamp('2005-01-31')]; print('Nifty500 B&H:',{k:round(v,3) for k,v in L.stats(m).items()})
print(bk.round(3).to_string(index=False))
