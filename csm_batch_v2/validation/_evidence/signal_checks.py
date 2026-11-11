"""Recalculate playbook IC ladders, horizon, quintiles and liquidity bands."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
from csm_stock_strategy import CrossSectionalMomentum,load_data
window=sys.argv[1];p,v,h,l,o=load_data('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data');latest=p.index.max()
start,report_start,end={'early':('2000-01-03','2001-01-01','2012-12-31'),'late':('2011-10-09','2013-01-01',str(latest.to_period('M').to_timestamp('M').date()))}[window]
p=p.loc[start:end];v=v.reindex(index=p.index,columns=p.columns);h=h.reindex(index=p.index,columns=p.columns);l=l.reindex(index=p.index,columns=p.columns);del o
s=CrossSectionalMomentum(p,v,h,l,min_price=10,universe_top_n=2000,max_circuit_days=5);s.calculate_factors()
m=p.resample('ME').last();r=m.pct_change(fill_method=None);fl=((m.shift(1)/m.shift(13)-1)/(r.rolling(12).std().shift(1)*np.sqrt(12))).clip(-5,5);fs=((m.shift(1)/m.shift(7)-1)/(r.rolling(6).std().shift(1)*np.sqrt(12))).clip(-5,5);f=(fl+fs)/2
price=m.shift(1)>10;dvol=(p*v).rolling(63,min_periods=21).median().shift(1).resample('ME').last().reindex(m.index);rank=dvol.rank(axis=1,ascending=False,method='min');liq=rank<=1000
eligible=s.factors.notna().reindex(index=m.index,columns=m.columns,fill_value=False)
masks={'L0_raw':f.notna(),'L1_price':f.notna()&price,'L2_liquidity':f.notna()&price&liq,'L3_tradeable':eligible&liq}
masks['L4_positive']=masks['L3_tradeable']&(s.momentum_returns.reindex(index=m.index,columns=m.columns)>0)
masks['L5_top30']=masks['L4_positive']&(s.factors.reindex(index=m.index,columns=m.columns).where(masks['L3_tradeable']).rank(axis=1,ascending=False,method='first')<=30)
for n in [100,250,500,750,1000,1500]:masks[f'band_0_{n}']=eligible&(rank<=n)
for a,b in [(500,1000),(1000,1500),(1000,2000)]:masks[f'band_{a}_{b}']=eligible&(rank>a)&(rank<=b)
# HAC retains empty calendar months as gaps; positive serial correlation is not silently compressed.
def nw(series,lag):
 if len(series)==0:return np.nan
 series=series.reindex(pd.date_range(series.index.min(),series.index.max(),freq='ME'));x=series.to_numpy(dtype=float);valid=np.isfinite(x);n=int(valid.sum())
 if n<lag+3:return np.nan
 avg=np.nanmean(x);e=np.where(valid,x-avg,0);v=np.dot(e,e)/n
 for j in range(1,lag+1):v+=2*(1-j/(lag+1))*np.dot(e[j:],e[:-j])/n
 return avg/np.sqrt(v/n) if v>0 else np.nan
summary=[];series_rows=[];quints=[];compare=[]
for horizon in [1,3,6,12]:
 fw=m.shift(-horizon)/m-1;fwd_ff=m.ffill().shift(-horizon)/m-1
 dates=[d for d in m.loc[report_start:end].index if d+pd.offsets.MonthEnd(horizon)<=pd.Timestamp(end)]
 for name,mask in masks.items():
  ic={};ic_ff={};spread={};qrows=[];weighted=[];sizes=[];added=0
  for dt in dates:
   valid=mask.loc[dt]&f.loc[dt].notna()&fw.loc[dt].notna()&np.isfinite(fw.loc[dt]);sizes.append(int(valid.sum()))
   if valid.sum()<8:continue
   x=f.loc[dt,valid].rank();y=fw.loc[dt,valid].rank();z=x.corr(y)
   if not np.isfinite(z):continue
   ic[dt]=z;series_rows.append({'window':window,'rung':name,'horizon':horizon,'date':dt,'ic':z,'names':int(valid.sum())})
   if name in ['L0_raw','L3_tradeable']:
    alt=mask.loc[dt]&f.loc[dt].notna()&fwd_ff.loc[dt].notna()&np.isfinite(fwd_ff.loc[dt])
    if alt.sum()>=8:
     ic_ff[dt]=f.loc[dt,alt].corr(fwd_ff.loc[dt,alt],method='spearman');added+=int((alt&~valid).sum())
   if name=='L3_tradeable':
    q=pd.qcut(f.loc[dt,valid].rank(method='first'),5,labels=False,duplicates='drop');means=fw.loc[dt,valid].groupby(q).mean().reindex(range(5));qrows.append(means);spread[dt]=means.iloc[4]-means.iloc[0]
    w=dvol.loc[dt,valid].clip(lower=0).fillna(0);total=w.sum()
    if total>0:
     w=w/total;mx=(x*w).sum();my=(y*w).sum();den=np.sqrt(((x-mx)**2*w).sum()*((y-my)**2*w).sum());weighted.append(((x-mx)*(y-my)*w).sum()/den if den>0 else np.nan)
  I=pd.Series(ic,dtype=float); sd=I.std();ys=I.groupby(I.index.year).sum() if len(I) else pd.Series(dtype=float)
  row={'window':window,'rung':name,'horizon':horizon,'months':len(I),'total_months':len(dates),'excluded_pct':100*sum(n<8 for n in sizes)/len(dates) if dates else np.nan,'mean_ic':I.mean(),'icir':I.mean()/sd if sd>0 else np.nan,'nw_t':nw(I,horizon),'median_names':np.median(sizes) if sizes else np.nan}
  if name=='L3_tradeable' and qrows:
   qmean=pd.DataFrame(qrows).mean();row.update({'quintile_increasing':int((qmean.diff().iloc[1:]>0).sum()),'spread_nw_t':nw(pd.Series(spread,dtype=float),horizon),'weighted_liquidity_ic':np.nanmean(weighted),'top2_year_share_pct':ys.nlargest(2).sum()/ys.sum()*100 if ys.sum()>0 else np.nan})
   for i,val in enumerate(qmean):quints.append({'window':window,'horizon':horizon,'quintile':i+1,'mean_return_pct':val*100})
  if name in ('L0_raw','L3_tradeable') and ic_ff:
   common=I.index.intersection(pd.Series(ic_ff).index);raw_mean=I.loc[common].mean();ff_mean=pd.Series(ic_ff).loc[common].mean();compare.append({'window':window,'rung':name,'horizon':horizon,'common_months':len(common),'raw_ic':raw_mean,'ffill_ic':ff_mean,'difference':ff_mean-raw_mean,'added_symbol_months':added})
  summary.append(row);print('RESULT',window,name,horizon,row['mean_ic'],row['nw_t'],flush=True)
coverage=masks['L3_tradeable'].loc[report_start:end].sum(axis=1)
hist=p.notna().cumsum().shift(1).resample('ME').last().reindex(m.index);S=masks['L3_tradeable'].loc[report_start:end]
meta=pd.DataFrame([{'window':window,'start':report_start,'end':end,'months':len(coverage),'below8':int((coverage<8).sum()),'below8_pct':float((coverage<8).mean()*100),'mean_names':coverage.mean(),'median_names':coverage.median(),'min_names':coverage.min(),'eligible_symbol_months':int(S.sum().sum()),'under252':int(((hist.loc[S.index]<252)&S).sum().sum())}])
for name,data in [('summary',summary),('monthly_ic',series_rows),('quantiles',quints),('ffill',compare)]:pd.DataFrame(data).to_csv(OUT/f'{window}_signal_{name}.csv',index=False)
meta.to_csv(OUT/f'{window}_signal_breadth.csv',index=False)
print('DONE',window,flush=True)
