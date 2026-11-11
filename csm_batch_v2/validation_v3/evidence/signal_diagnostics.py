"""Actual dual-momentum signal: IC/ICIR/t/NW, horizons, accuracy and time decay."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
from csm_stock_strategy import CrossSectionalMomentum,load_data
window=sys.argv[1];P,V,H,L,O=load_data('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data')
start,end={'early':('2005-01-01','2014-12-31'),'late':('2015-01-01','2025-12-31'),'playbook_early':('2001-01-01','2012-12-31'),'playbook_late':('2013-01-01',str(P.index.max().to_period('M').to_timestamp('M').date()))}[window]
load_start=pd.Timestamp(start)-pd.Timedelta(days=450);p=P.loc[load_start:end];v=V.reindex(index=p.index,columns=p.columns);hi=H.reindex(index=p.index,columns=p.columns);lo=L.reindex(index=p.index,columns=p.columns);del P,V,H,L,O
s=CrossSectionalMomentum(p,v,hi,lo,min_price=10,universe_top_n=2000,max_circuit_days=5,top_n=30);s.calculate_factors()
m=p.resample('ME').last();monthly_ret=m.pct_change(fill_method=None);L12=m.shift(1)/m.shift(13)-1;L6=m.shift(1)/m.shift(7)-1;v12=(monthly_ret.rolling(12).std().shift(1)*np.sqrt(12)).replace(0,np.nan);v6=(monthly_ret.rolling(6).std().shift(1)*np.sqrt(12)).replace(0,np.nan)
f_long=(L12/v12).clip(-5,5);f_short=(L6/v6).clip(-5,5);factor=(f_long+f_short)/2
price=m.shift(1)>10;dvol=(p*v).rolling(63,min_periods=21).median().shift(1).resample('ME').last().reindex(m.index);liqrank=dvol.rank(axis=1,ascending=False,method='min');rank1000=liqrank<=1000
circ=(hi==lo).shift(1).rolling(63,min_periods=1).sum().resample('ME').last().reindex(m.index).fillna(0)<=5
age=p.notna().cumsum().shift(1).resample('ME').last().reindex(m.index)>=252
base=s.factors.notna().reindex(index=m.index,columns=m.columns,fill_value=False);tradeable=base&rank1000
masks={'L0_long':f_long.notna(),'L0_short':f_short.notna(),'L0_composite':factor.notna(),'L1_price':factor.notna()&price,'L2_liquidity_circuit_age':factor.notna()&price&rank1000&circ&age,'L3_tradeable':tradeable,'L4_positive_momentum':tradeable&(L12>0)}
ordinal=factor.where(tradeable).rank(axis=1,ascending=False,method='first');masks['L5_top30']=masks['L4_positive_momentum']&(ordinal<=30)
for n in [100,250,500,750,1000,1500]:masks[f'band_0_{n}']=base&(liqrank<=n)
for a,b in [(500,1000),(1000,1500),(1000,2000)]:masks[f'band_{a}_{b}']=base&(liqrank>a)&(liqrank<=b)
# The long and short component IC are calculated using those components, not the composite.
def lag_series(x):
 if not len(x):return np.array([],dtype=float)
 if isinstance(x,pd.Series) and isinstance(x.index,pd.DatetimeIndex):x=x.reindex(pd.date_range(x.index.min(),x.index.max(),freq='ME'))
 return np.asarray(x,dtype=float)
def nw(x,lag):
 x=lag_series(x);valid=np.isfinite(x);n=int(valid.sum())
 if n<lag+3:return np.nan
 avg=np.nanmean(x);e=np.where(valid,x-avg,0);lr=np.dot(e,e)/n
 for j in range(1,lag+1):lr+=2*(1-j/(lag+1))*np.dot(e[j:],e[:-j])/n
 return avg/np.sqrt(lr/n) if lr>0 else np.nan
def nw_ols_delta(series,cutoff,lag=3):
 if not len(series):return (np.nan,np.nan)
 all_dates=pd.date_range(series.index.min(),series.index.max(),freq='ME'); y=series.reindex(all_dates).to_numpy();valid=np.isfinite(y); indicator=(all_dates>=pd.Timestamp(cutoff)).astype(float);X=np.column_stack([np.ones(len(y)),indicator]);Xv=X[valid];yv=y[valid]
 if len(yv)<10 or len(np.unique(indicator[valid]))<2:return (np.nan,np.nan)
 try:
  inv=np.linalg.inv(Xv.T@Xv);beta=inv@(Xv.T@yv);u=np.where(valid,y-np.nan_to_num(X@beta),0);xu=X*u[:,None];S=xu.T@xu
  for j in range(1,lag+1):G=xu[j:].T@xu[:-j];S+=(1-j/(lag+1))*(G+G.T)
  var=inv@S@inv;se=np.sqrt(var[1,1]);return float(beta[1]),float(beta[1]/se) if se>0 else np.nan
 except np.linalg.LinAlgError:return (np.nan,np.nan)
rows=[];series=[];quint=[];compar=[];monthly_acc=[]
for hz in [1,3,6,12]:
 forward=m.shift(-hz)/m-1;fwd_ff=m.ffill().shift(-hz)/m-1;dates=[d for d in m.loc[start:end].index if d+pd.offsets.MonthEnd(hz)<=pd.Timestamp(end)]
 for name,mask in masks.items():
  signal=f_long if name=='L0_long' else (f_short if name=='L0_short' else factor)
  ic={};spreads={};qmeans=[];weight_ic=[];ff_ic={};sizes=[];n_added=0
  for dt in dates:
   valid=mask.loc[dt]&signal.loc[dt].notna()&forward.loc[dt].notna()&np.isfinite(forward.loc[dt]);sizes.append(int(valid.sum()))
   if valid.sum()<8:continue
   xx=signal.loc[dt,valid].rank();yy=forward.loc[dt,valid].rank();rho=xx.corr(yy)
   if not np.isfinite(rho):continue
   ic[dt]=float(rho);series.append({'window':window,'rung':name,'horizon':hz,'date':dt,'ic':rho,'n':int(valid.sum())})
   if name in ('L0_composite','L3_tradeable'):
    alt=mask.loc[dt]&signal.loc[dt].notna()&fwd_ff.loc[dt].notna()&np.isfinite(fwd_ff.loc[dt])
    if alt.sum()>=8:ff_ic[dt]=signal.loc[dt,alt].corr(fwd_ff.loc[dt,alt],method='spearman');n_added+=int((alt&~valid).sum())
   if name=='L3_tradeable':
    vals=forward.loc[dt,valid];q=pd.qcut(signal.loc[dt,valid].rank(method='first'),5,labels=False,duplicates='drop');means=vals.groupby(q).mean().reindex(range(5));qmeans.append(means);spreads[dt]=means.iloc[4]-means.iloc[0]
    weight=dvol.loc[dt,valid].clip(lower=0).fillna(0);total=weight.sum()
    if total>0:
     weight=weight/total;xm=(xx*weight).sum();ym=(yy*weight).sum();den=np.sqrt(((xx-xm)**2*weight).sum()*((yy-ym)**2*weight).sum());weight_ic.append(((xx-xm)*(yy-ym)*weight).sum()/den if den else np.nan)
    pick=valid&masks['L5_top30'].loc[dt];pr=forward.loc[dt,pick]; pool=vals
    if len(pr):monthly_acc.append({'window':window,'date':dt,'horizon':hz,'n_selected':len(pr),'pool_n':len(pool),'selected_return':pr.mean(),'pool_return':pool.mean(),'top_excess':pr.mean()-pool.mean(),'stock_above_pool_median_pct':100*(pr>pool.median()).mean(),'stock_positive_pct':100*(pr>0).mean()})
  I=pd.Series(ic,dtype=float);std=I.std();N=len(I);years=I.groupby(I.index.year).sum() if N else pd.Series(dtype=float)
  rec={'window':window,'rung':name,'horizon':hz,'n_months':N,'eligible_months':len(dates),'mean_ic':I.mean(),'icir':I.mean()/std if std>0 else np.nan,'t_stat':I.mean()/std*np.sqrt(N) if std>0 else np.nan,'nw_t':nw(I,hz),'positive_ic_pct':100*(I>0).mean() if N else np.nan,'median_names':np.median(sizes) if sizes else np.nan,'average_names':np.mean(sizes) if sizes else np.nan,'months_lt8_pct':100*sum(x<8 for x in sizes)/len(dates) if dates else np.nan,'months_lt30_pct':100*sum(x<30 for x in sizes)/len(dates) if dates else np.nan}
  if name=='L3_tradeable' and qmeans:
   av=pd.DataFrame(qmeans).mean();rec.update({'monotone_pairs':int((av.diff().iloc[1:]>0).sum()),'spread_mean_pp':100*pd.Series(spreads).mean(),'spread_nw_t':nw(pd.Series(spreads,dtype=float),hz),'weighted_liquidity_ic':np.nanmean(weight_ic),'top2_year_share_pct':100*years.nlargest(2).sum()/years.sum() if years.sum()>0 else np.nan})
   for qno,x in enumerate(av):quint.append({'window':window,'horizon':hz,'quantile':qno+1,'mean_return_pct':100*x})
  if len(ff_ic):
   FF=pd.Series(ff_ic,dtype=float);common=I.index.intersection(FF.index);compar.append({'window':window,'rung':name,'horizon':hz,'n':len(common),'raw_ic':I.loc[common].mean(),'ffill_ic':FF.loc[common].mean(),'extra_observations':n_added})
  rows.append(rec);print('IC',window,name,hz,'n',N,'mean',rec['mean_ic'],'NW',rec['nw_t'],flush=True)
# Time decay is distinct from forward-horizon decay; same L3 3m definition by years and fixed chunks.
allS=pd.DataFrame(series);l3=allS[(allS.rung=='L3_tradeable')&(allS.horizon==3)].copy();l3['date']=pd.to_datetime(l3.date);I=l3.set_index('date').ic.sort_index();acc=pd.DataFrame(monthly_acc)
if len(acc):acc['date']=pd.to_datetime(acc.date)
years=[]
for yr,g in I.groupby(I.index.year):
 at=acc[(acc.horizon==3)&(acc.date.dt.year==yr)];years.append({'year':yr,'months':len(g),'mean_ic':g.mean(),'icir':g.mean()/g.std() if g.std()>0 else np.nan,'t_stat':g.mean()/g.std()*np.sqrt(len(g)) if g.std()>0 else np.nan,'nw_t':nw(g,3),'positive_ic_pct':(g>0).mean()*100,'top30_above_median_pct':at.stock_above_pool_median_pct.mean(),'top30_positive_pct':at.stock_positive_pct.mean(),'top30_excess_pct':at.top_excess.mean()*100})
chunks=[]
for first in range(int(start[:4]),int(end[:4])+1,3):
 last=min(first+2,int(end[:4]));a=I.loc[f'{first}-01-01':f'{last}-12-31'];at=acc[(acc.horizon==3)&(acc.date.dt.year>=first)&(acc.date.dt.year<=last)];chunks.append({'period':f'{first}-{last}','months':len(a),'mean_ic':a.mean(),'icir':a.mean()/a.std() if a.std()>0 else np.nan,'nw_t':nw(a,3),'positive_ic_pct':(a>0).mean()*100 if len(a) else np.nan,'top30_above_median_pct':at.stock_above_pool_median_pct.mean(),'top30_excess_pct':at.top_excess.mean()*100})
cutoff=f'{int(end[:4])-2}-01-01';recent=I.loc[cutoff:];prior=I.loc[:str(pd.Timestamp(cutoff)-pd.Timedelta(days=1))];delta,dtstat=nw_ols_delta(I,cutoff,3)
decay=pd.DataFrame([{'window':window,'prior_months':len(prior),'prior_ic':prior.mean(),'recent_start':cutoff,'recent_months':len(recent),'recent_ic':recent.mean(),'recent_nw_t':nw(recent,3),'difference':delta,'difference_nw_t':dtstat}])
acc3=acc[acc.horizon==3].copy();accS=acc3.set_index('date').top_excess if len(acc3) else pd.Series(dtype=float)
accuracy=pd.DataFrame([{'window':window,'months':len(acc3),'average_selected':acc3.n_selected.mean(),'stock_above_pool_median_pct':acc3.stock_above_pool_median_pct.mean(),'stock_positive_pct':acc3.stock_positive_pct.mean(),'top30_excess_pct':accS.mean()*100,'top30_excess_nw_t':nw(accS,3)}])
coverage=tradeable.loc[start:end].sum(axis=1);breadth=pd.DataFrame([{'window':window,'months':len(coverage),'median':coverage.median(),'mean':coverage.mean(),'below8_pct':100*(coverage<8).mean(),'below30_pct':100*(coverage<30).mean()}])
band_breadth=[]
for name,mask in masks.items():
 if not (name.startswith('band_') or name=='L3_tradeable'):continue
 counts=mask.loc[start:end].sum(axis=1);band_breadth.append({'window':window,'band':name,'months':len(counts),'mean':counts.mean(),'median':counts.median(),'min':counts.min(),'below8_pct':100*(counts<8).mean(),'below30_pct':100*(counts<30).mean()})
pd.DataFrame(band_breadth).to_csv(OUT/f'signal_{window}_band_breadth.csv',index=False)
for name,data in [('summary',rows),('series',series),('quintiles',quint),('ffill',compar),('accuracy_monthly',monthly_acc),('years',years),('chunks',chunks)]:pd.DataFrame(data).to_csv(OUT/f'signal_{window}_{name}.csv',index=False)
decay.to_csv(OUT/f'signal_{window}_decay.csv',index=False);accuracy.to_csv(OUT/f'signal_{window}_accuracy.csv',index=False);breadth.to_csv(OUT/f'signal_{window}_breadth.csv',index=False)
print('DECAY',decay.to_string(index=False));print('ACCURACY',accuracy.to_string(index=False));print('DONE',window,flush=True)
