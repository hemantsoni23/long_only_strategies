"""Yearly decomposition of the frozen winner and baseline, through 2024."""
import json
import tempfile
from pathlib import Path

import pandas as pd

import study
import fundamentals_loader as fl
import run_csm_value_backtest as rb

OUT=Path(__file__).resolve().parent

def main():
    frozen=json.loads((OUT/'frozen_selection.json').read_text())
    with tempfile.TemporaryDirectory(prefix='csm_value_pre2025_') as tmp:
        syms=study.stage_fundamentals(Path(tmp))
        results=fl.load_results(symbols=syms,directory=tmp)
        data=list(study.load_ohlcv(syms));data.append(rb.load_nse_monthly_prices(symbols=syms).loc[:study.CUTOFF])
        s=study.make_strategy(data,results,study.CUTOFF);base=s.factors.copy();signals=study.overlays(s)
        output=[]
        for name in dict.fromkeys(('baseline',frozen['selected'])):
            s.factors=study.candidate_factors(base,signals,name);s.get_positions()
            res=rb.backtest_event_driven(s,initial_capital=100000,transaction_cost=.003,risk_free_rate=0.)
            daily=res['net_returns'];weights=res['executed_weights'];turnover=res['turnover']
            for year in range(2019,2025):
                first=max(pd.Timestamp(f'{year}-01-01'),pd.Timestamp(study.IS_START))
                last=pd.Timestamp(f'{year}-12-31');part=daily.loc[first:last]
                if part.empty:continue
                m=rb.window_metrics(daily,str(first.date()),str(last.date()))
                output.append({'candidate':name,'year':year,'total_return':float((1+part).prod()-1),
                               'max_drawdown':float(m['max_drawdown']),
                               'turnover':float(turnover.loc[first:last].sum()),
                               'average_exposure':float(weights.loc[first:last].sum(axis=1).mean())})
        (OUT/'yearly_diagnostics.json').write_text(json.dumps(output,indent=2)+'\n')
        print('YEARLY',json.dumps(output),flush=True)

if __name__=='__main__':main()
