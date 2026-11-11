"""Exploratory 2024–25 versus 2021–23 L3-IC change, monthly HAC lag 3."""
from pathlib import Path
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent;d=pd.read_csv(P/'signal_late_series.csv',parse_dates=['date']);d=d[(d.rung=='L3_tradeable')&(d.horizon==3)].set_index('date').ic.sort_index().loc['2021-01-01':];dates=pd.date_range(d.index.min(),d.index.max(),freq='ME');y=d.reindex(dates).to_numpy();valid=np.isfinite(y);z=(dates>=pd.Timestamp('2024-01-01')).astype(float);X=np.column_stack([np.ones(len(y)),z]);inv=np.linalg.inv(X[valid].T@X[valid]);beta=inv@(X[valid].T@y[valid]);u=np.where(valid,y-X@beta,0);xu=X*u[:,None];V=xu.T@xu
for j in range(1,4):G=xu[j:].T@xu[:-j];V+=(1-j/4)*(G+G.T)
se=np.sqrt((inv@V@inv)[1,1]);r={'prior':'2021–2023','prior_months':int((valid&(z==0)).sum()),'prior_ic':float(np.mean(y[valid&(z==0)])),'recent':'2024–2025','recent_months':int((valid&(z==1)).sum()),'recent_ic':float(np.mean(y[valid&(z==1)])),'difference':float(beta[1]),'hac_t_difference':float(beta[1]/se)};pd.DataFrame([r]).to_csv(P/'signal_recent_posthoc.csv',index=False);print(r)
