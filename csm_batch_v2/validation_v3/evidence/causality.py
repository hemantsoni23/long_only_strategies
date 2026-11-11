"""Prefix-invariance checks of signal, targets, ATR and regime on the actual source."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT));from csm_stock_strategy import CrossSectionalMomentum,load_data
P,V,H,L,O=load_data('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data');start=pd.Timestamp('2013-10-08');end=pd.Timestamp('2025-12-31');p=P.loc[start:end];v=V.reindex(index=p.index,columns=p.columns);h=H.reindex(index=p.index,columns=p.columns);l=L.reindex(index=p.index,columns=p.columns);o=O.reindex(index=p.index,columns=p.columns);del P,V,H,L,O
bench=(1+p.pct_change(fill_method=None).clip(-.5,.5).mean(axis=1).fillna(0)).cumprod();anchor=pd.Timestamp('2014-12-31')
def create(cut):
 px=p.loc[:cut];s=CrossSectionalMomentum(px,v.loc[:cut],h.loc[:cut],l.loc[:cut],o.loc[:cut],benchmark_series=bench.loc[:cut],lookback_months=12,lag_months=1,top_n=30,min_price=10,universe_top_n=1000,max_circuit_days=5,buffer_ratio=.2,use_trailing_stop=False,use_vol_scaled_stop=True,vol_stop_k=4,min_hold_days=5,use_crash_guard=False,vol_target=.2,use_bear_regime_exposure=True,bear_regime_sma_days=150,bear_regime_return_days=63,bear_regime_return_cutoff=-.1,bear_regime_scale=.6,severe_bear_regime_scale=.3,max_weight_per_stock=.05,rebalance_months=2,rank_exit_dynamic=True,rank_exit_drop_frac=.34,rank_exit_floor_frac=.67)
 s.calculate_factors();s.factors=s.factors.loc[anchor:];s.momentum_returns=s.momentum_returns.loc[anchor:];s.get_positions();return s
full=create(end);rows=[]
for cutoff in ['2018-12-31','2020-03-31','2022-12-30','2024-12-31','2025-06-30']:
 c=pd.Timestamp(cutoff);part=create(c);dates=full.factors.index[(full.factors.index<=c)&(full.factors.index>=anchor)];idx=dates.union(part.factors.index[part.factors.index<=c]);a=full.factors.reindex(idx);b=part.factors.reindex(idx);mask_mismatch=int((a.notna()!=b.notna()).to_numpy().sum());adiff=(a-b).abs().to_numpy();fm=float(np.nanmax(adiff)) if np.isfinite(adiff).any() else 0.
 pos_full=full.positions.reindex(idx).fillna(0);pos_part=part.positions.reindex(idx).fillna(0);pdiff=np.abs(pos_full.to_numpy()-pos_part.to_numpy());diffcnt=int((pdiff>1e-12).sum());pmax=float(pdiff.max()) if pdiff.size else 0.
 common=part.atr.index.intersection(full.atr.index);diff=(full.atr.loc[common]-part.atr.loc[common]).abs().to_numpy();ad=float(np.nanmax(diff)) if np.isfinite(diff).any() else 0.
 regime=(full.bear_regime_scale_series.loc[common]-part.bear_regime_scale_series.loc[common]).abs();rd=float(regime.max()) if len(regime) else 0.
 rows.append({'cutoff':cutoff,'monthly_rows':len(idx),'eligible_mask_mismatches':mask_mismatch,'max_factor_difference':fm,'position_cells_changed':diffcnt,'max_position_difference':pmax,'max_atr_difference':ad,'max_regime_difference':rd,'result':'PASS' if mask_mismatch==0 and fm<1e-12 and diffcnt==0 and ad<1e-12 and rd<1e-12 else 'FAIL'})
 print('PREFIX',rows[-1],flush=True);del part,a,b,adiff,diff
pd.DataFrame(rows).to_csv(OUT/'prefix_tests.csv',index=False)
