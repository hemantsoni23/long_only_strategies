"""Examine as-of strategy coverage and filing features of actual logged entries."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'csm_value'))
import fundamentals_loader as fl

prices=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data')
symbols={p.stem for p in prices.glob('*.csv')}
res=fl.load_results(symbols=symbols)
print('RESULTS',len(res),'COMPANIES',res.symbol.nunique(),flush=True)
nse=pd.read_csv(ROOT/'csm_value/data/nse_monthly_prices.csv',usecols=['datetime','symbol'],parse_dates=['datetime'])
dates=pd.DatetimeIndex(sorted(nse.datetime.unique()));dates=dates[(dates>='2019-01-01') & (dates<='2026-11-04')]
cols=sorted(set(res.symbol)&set(nse.symbol)); fields=['np_ttm','sg_np','shares_adj','period_end','oneoff_share']
frames={col:fl.monthly_frame(res,col,dates,cols,max_age=140) for col in fields}
result=[]
for date in dates:
 available=frames['np_ttm'].loc[date].notna(); positive=frames['np_ttm'].loc[date]>0;growth=frames['sg_np'].loc[date]>0
 ep=available & positive & growth
 result.append({'date':date,'fresh_ttm':int(available.sum()),'positive_profit':int((available&positive).sum()),
                'positive_growth':int(ep.sum()),'fresh_on_nse':int((available & pd.Series(nse[nse.datetime==date].symbol.isin(cols).to_numpy(), index=nse[nse.datetime==date].symbol).reindex(cols,fill_value=False)).sum())})
cov=pd.DataFrame(result); cov.to_csv(OUT/'monthly_strategy_coverage.csv',index=False)
print('COVERAGE_YEAR_MEDIAN'); print(cov.groupby(cov.date.dt.year)[['fresh_ttm','positive_profit','positive_growth','fresh_on_nse']].median().to_string())
tr=pd.read_csv(ROOT/'csm_value/output/csm_value_ey_trade_log.csv',parse_dates=['Entry_Date','Exit_Date']); tr=tr[(tr.Entry_Date>='2019-06-03') & (tr.Entry_Date<='2026-11-04')].copy()
month_days={d.to_period('M'):d for d in dates}
tr['signal_month']=tr.Entry_Date.map(lambda d: (d-pd.offsets.MonthEnd(1)).to_period('M'))
tr['signal_date']=tr.signal_month.map(month_days)
records=[]
for t in tr.itertuples():
 if pd.isna(t.signal_date) or t.Ticker not in cols: continue
 info={f:getattr(frames[f], 'at')[t.signal_date,t.Ticker] for f in fields}
 records.append({'symbol':t.Ticker,'entry':t.Entry_Date,'exit':t.Exit_Date,'signal':t.signal_date,
                 'pnl_pct':t.PnL_Pct,'ep':t.EP_At_Entry, **info})
r=pd.DataFrame(records);r.to_csv(OUT/'trade_fundamental_inputs.csv',index=False)
print('TRADE_ONEOFF_SHARE (trailing other-income + positive exceptional, divided by trailing PBT; excludes nonpositive PBT)')
for yr,g in r.groupby(r.entry.dt.year):
 good=g[g.oneoff_share.notna()]; print(yr,'trades',len(g),'computable',len(good),'median',round(good.oneoff_share.median(),3),'above_50pct',int((good.oneoff_share>.5).sum()),'above_100pct',int((good.oneoff_share>1).sum()))
print('RECENT_SPECIAL_EXAMPLES'); print(r[(r.symbol.isin(['DEVIT','INDIANHUME','ZUARI','PFC'])) & (r.entry>='2025-01-01')][['symbol','entry','signal','period_end','ep','np_ttm','oneoff_share','pnl_pct']].to_string(index=False))
raw=pd.read_csv(OUT/'filings_inventory.csv'); raw['filed_parsed']=raw.filed.map(fl._parse_filed);raw['end_parsed']=pd.to_datetime(raw.end);raw['lag']=(pd.to_datetime(raw.filed_parsed)-raw.end_parsed).dt.days
for group,g in raw[(raw.group=='main') & (raw.year>=2025)].groupby('submission_type',dropna=False):
 print('FILING_LAGS',group,'count',len(g),'median',round(g.lag.median(),1),'over120',int((g.lag>120).sum()),'unique_symbols_over120',g.loc[g.lag>120,'symbol'].nunique())
print('REVISION_LATE_EXAMPLES');print(raw[(raw.group=='main')&(raw.year>=2025)&(raw.submission_type=='Revision')&(raw.lag>120)][['symbol','basis','end','filed','lag']].head(15).to_string(index=False))
