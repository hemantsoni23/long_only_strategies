"""Check that full-data and truncated runs agree before each cutoff.

These are engineering causality checks on previously used data, not a new
out-of-sample performance test.
"""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('live_signal_research',ROOT/'research/csm_value_live_signals/study.py')
live=importlib.util.module_from_spec(spec);spec.loader.exec_module(live)
import run_csm_value_backtest as rb

def run(data,results,end,mode):
    s=live.core.make_strategy(data,results,end)
    if mode!='value':
        s.ranking_mode=mode;s.components=('EP','PROFIT_GROWTH','PULLBACK');s.calculate_factors()
    factors=s.factors.copy();s.get_positions();positions=s.positions.copy()
    r=rb.backtest_event_driven(s,initial_capital=100000,transaction_cost=.003,risk_free_rate=0.)
    return factors,positions,r['net_returns'].copy()

def delta(a,b,zero_absent=False):
    # A symbol whose first usable filing comes after the truncation is absent
    # from the shorter position panel; its pre-filing weight is zero.
    a,b=a.align(b,join='outer',axis=None,fill_value=0.0 if zero_absent else None)
    if not np.array_equal(a.isna().to_numpy(),b.isna().to_numpy()):
        raise AssertionError('Different missing-value locations')
    x=np.abs((a-b).to_numpy());return float(np.nanmax(x)) if np.isfinite(x).any() else 0.0

def main():
    tmp,res,data=live.make_inputs(); checks=[]
    try:
        for mode in ('value','value_growth_pullback'):
            ff,fp,fr=run(data,res,pd.Timestamp('2024-12-31'),mode)
            for cut in ('2022-12-30','2023-12-29'):
                shortf,shortp,shortr=run(data,res,pd.Timestamp(cut),mode)
                # Month-end rows use calendar labels; include a December month
                # only after its final trading session, as both runs do.
                month_end=pd.Timestamp(cut)+pd.offsets.MonthEnd(0)
                diffs={'factor_max_abs':delta(ff.loc[:month_end],shortf),
                       'position_max_abs':delta(fp.loc[:month_end],shortp,zero_absent=True),
                       'daily_return_max_abs':delta(fr.loc[:cut],shortr)}
                if any(v>1e-10 for v in diffs.values()):raise AssertionError((mode,cut,diffs))
                item={'mode':mode,'cutoff':cut,**diffs};checks.append(item)
                print('PREFIX_PASS',json.dumps(item),flush=True)
        (OUT/'prefix_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    finally:tmp.cleanup()

if __name__=='__main__':main()
