"""Actual v3 baseline parity and history-truncation causality checks."""
import sys,copy
from pathlib import Path
import numpy as np,pandas as pd
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
import csm_stock_backtest_v3 as bt
P,V,H,L,O=bt.load_data(bt.DATA_FOLDER);start=pd.Timestamp('2015-01-01');end=pd.Timestamp('2025-12-31');p=P.loc[start-pd.Timedelta(days=450):end];v=V.reindex_like(p);h=H.reindex_like(p);l=L.reindex_like(p);o=O.reindex_like(p);del P,V,H,L,O
anchor=start-pd.offsets.MonthEnd(1)
def create(c):
 sub=p.loc[:c];data=dict(prices=sub,volumes=v.reindex_like(sub),highs=h.reindex_like(sub),lows=l.reindex_like(sub),opens=o.reindex_like(sub))
 s=bt.build_csm(data=data);s.factors=s.factors.loc[anchor:];s.momentum_returns=s.momentum_returns.loc[anchor:];s.get_positions();return s
full=create(end);run=bt.run_backtest(full);ref=pd.read_csv(OUT/'late_universe_equity.csv',index_col=0,parse_dates=True).iloc[:,0];eq=bt.slice_to_report_window(run,'2015-01-01','2025-12-31',bt.INITIAL_CAPITAL)['equity_curve'];ref=ref.reindex(eq.index);diff=float((ref-eq).abs().max());
pos=pd.read_parquet(OUT/'late_universe_positions.parquet').reindex_like(full.positions);d=np.abs(pos.to_numpy()-full.positions.to_numpy());n=int((d>1e-12).sum());pd.DataFrame([{'equity_max_abs_diff':diff,'position_cells_changed':n,'passed':diff<1e-10 and n==0}]).to_csv(OUT/'actual_strategy_parity.csv',index=False)
print('PARITY',diff,n,flush=True)
rows=[]
for cutoff in ['2018-12-31','2020-03-31','2022-12-30','2024-12-31','2025-06-30']:
 c=pd.Timestamp(cutoff);part=create(c);ix=full.factors.index[(full.factors.index<=c)&(full.factors.index>=anchor)].union(part.factors.index[part.factors.index<=c]);x=full.factors.reindex(ix);y=part.factors.reindex(ix);mask=int((x.notna()!=y.notna()).to_numpy().sum());raw=(x-y).abs().to_numpy();fd=float(np.nanmax(raw)) if np.isfinite(raw).any() else 0.;px=full.positions.reindex(ix).fillna(0);py=part.positions.reindex(ix).fillna(0);pc=int((abs(px.to_numpy()-py.to_numpy())>1e-12).sum());ix2=full.atr.index.intersection(part.atr.index);raw=(full.atr.loc[ix2]-part.atr.loc[ix2]).abs().to_numpy();ad=float(np.nanmax(raw)) if np.isfinite(raw).any() else 0.
 rows.append({'cutoff':cutoff,'mask_mismatches':mask,'max_factor_difference':fd,'position_cells_changed':pc,'max_atr_difference':ad,'result':'PASS' if mask==0 and fd<1e-12 and pc==0 and ad<1e-12 else 'FAIL'});print('PREFIX',rows[-1],flush=True);del part,x,y,px,py,raw
pd.DataFrame(rows).to_csv(OUT/'prefix_tests.csv',index=False)
