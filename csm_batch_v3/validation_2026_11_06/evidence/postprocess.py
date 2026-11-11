"""Derive year-concentration diagnostics from saved daily runs."""
from pathlib import Path
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent
def load(name):return pd.read_csv(P/name,index_col=0,parse_dates=True).iloc[:,0]
def metrics(r,years=None):
 r=r.dropna();equity=(1+r).cumprod();eq0=pd.concat([pd.Series([1.],index=[r.index[0]-pd.Timedelta(days=1)]),equity]);years=years if years else (r.index[-1]-r.index[0]).days/365.25;cagr=(equity.iloc[-1]**(1/years)-1)*100 if years>0 else np.nan;dd=(eq0/eq0.cummax()-1).min();return {'cagr_pct':cagr,'sharpe':r.mean()/r.std()*np.sqrt(252) if r.std()>0 else np.nan,'maxdd_pct':dd*100,'calmar':cagr/100/abs(dd) if dd<0 else np.nan}
r=load('late_universe_baseline_returns.csv');base_sharpe=r.mean()/r.std()*np.sqrt(252);base=metrics(r);rows=[]
for year in sorted(r.index.year.unique()):
 part=r[r.index.year!=year];m=metrics(part,years=len(part)/252);yearret=(1+r[r.index.year==year]).prod()-1;rows.append({'removed_year':year,'removed_year_return_pct':yearret*100,'remaining_days':len(part),'sharpe':m['sharpe'],'delta_sharpe':m['sharpe']-base_sharpe,'calmar':m['calmar'],'cagr_tradingyear_pct':m['cagr_pct'],'maxdd_pct':m['maxdd_pct']})
pd.DataFrame(rows).to_csv(P/'leave_one_year_out.csv',index=False)
byyear=np.log1p(r).groupby(r.index.year).sum();total=byyear.sum();pd.DataFrame([{'years':len(byyear),'top1_year':int(byyear.idxmax()),'top1_share_pct':100*byyear.max()/total if total>0 else np.nan,'top2_share_pct':100*byyear.nlargest(2).sum()/total if total>0 else np.nan,'total_log_growth':total}]).to_csv(P/'year_concentration.csv',index=False)
print('BASE',base,'YEAR CONCENTRATION',pd.read_csv(P/'year_concentration.csv').to_dict('records'))
# Repeat the same fixed-return leave-one-year-out diagnostic for 2005–2014.
r=load('early_sweep_returns.csv');early_base=r.mean()/r.std()*np.sqrt(252);rows=[]
for year in sorted(r.index.year.unique()):
 part=r[r.index.year!=year];m=metrics(part,years=len(part)/252);yearret=(1+r[r.index.year==year]).prod()-1;rows.append({'removed_year':year,'removed_year_return_pct':yearret*100,'remaining_days':len(part),'sharpe':m['sharpe'],'delta_sharpe':m['sharpe']-early_base,'calmar':m['calmar'],'cagr_tradingyear_pct':m['cagr_pct'],'maxdd_pct':m['maxdd_pct']})
pd.DataFrame(rows).to_csv(P/'early_leave_one_year_out.csv',index=False)
yearly=np.log1p(r).groupby(r.index.year).sum();total=yearly.sum();pd.DataFrame([{'years':len(yearly),'top1_year':int(yearly.idxmax()),'top1_share_pct':100*yearly.max()/total if total>0 else np.nan,'top2_share_pct':100*yearly.nlargest(2).sum()/total if total>0 else np.nan,'total_log_growth':total}]).to_csv(P/'early_year_concentration.csv',index=False)
