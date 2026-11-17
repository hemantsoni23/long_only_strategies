"""Exploratory second fundamental dimensions with live-strategy signals.

All historical windows and ideas have been examined already. These outputs
are research, not an independent validation or automatic production change.
"""
import gc
import json
from pathlib import Path

import study as live

OUT=Path(__file__).resolve().parent
BASE_RANK=live.rank_value
CANDIDATES=('value','growth_elendel','growth_q5','quality_elendel',
            'growth_anti_elendel','anti_q5','growth_only')

def rank_new(base,signals,name):
    if name=='value':return base.copy()
    valid=base.notna()
    rank=lambda x:live.cross_rank(x,valid).fillna(.5)
    value=rank(base);growth=rank(signals['growth'])
    q5=rank(signals['q5']);a3=rank(signals['a3']);tech=(a3+q5)/2
    quality=rank(-signals['oneoff'])
    if name=='growth_elendel':score=.55*value+.20*growth+.25*tech
    elif name=='growth_q5':score=.55*value+.20*growth+.25*q5
    elif name=='quality_elendel':score=.55*value+.20*quality+.25*tech
    elif name=='growth_anti_elendel':score=.55*value+.20*growth+.25*(1-tech)
    elif name=='anti_q5':score=.75*value+.25*(1-q5)
    elif name=='growth_only':score=.75*value+.25*growth
    else:raise ValueError(name)
    return score.where(valid)

def main():
    live.rank_value=rank_new
    tmp,results,data=live.make_inputs()
    try:
        all_periods={}
        for label,end,start in [('development',live.core.IS_END,live.core.IS_START),
                                ('previously_examined',live.core.CUTOFF,live.core.TEST_START)]:
            s=live.core.make_strategy(data,results,end);base=s.factors.copy();mom=s.momentum_returns.copy();signals=live.calc_signals(s)
            rows=[]
            for name in CANDIDATES:
                row=live.evaluate(s,base,mom,signals,name,start,str(end.date()));rows.append(row)
                print(label.upper(),json.dumps(row),flush=True)
            all_periods[label]=rows
            if label=='development':
                winner=max(rows,key=lambda r:(r['calmar'],r['sharpe'],r['candidate']=='value'))['candidate']
                frozen={'candidates':list(CANDIDATES),'selected':winner,'selection':'development Calmar then Sharpe',
                        'development':rows,'warning':'All historical periods and related signals previously researched; exploratory comparison only.'}
                (OUT/'exploratory_frozen.json').write_text(json.dumps(frozen,indent=2)+'\n')
                print('FROZEN',winner,flush=True)
            del s,base,mom,signals;gc.collect()
        (OUT/'exploratory_mix_results.json').write_text(json.dumps({**frozen,**all_periods},indent=2)+'\n')
        print('DONE',flush=True)
    finally:tmp.cleanup()

if __name__=='__main__':main()
