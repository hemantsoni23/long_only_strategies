import pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from gold_overlay import daily_gold, pv_fraction, LIQUID_FUND_ANNUAL
from analyze_gold_idle import stitched_metrics, block_boot_delta
LF = (1 + LIQUID_FUND_ANNUAL) ** (1 / 252) - 1
mon = lambda s: ((1 + s).groupby([s.index.year, s.index.month]).prod() - 1)
rows = []
for name in ('elendel', 'zenith', 'quad'):
    p = pickle.load(open(f'.cache/engine_{name}.pkl', 'rb')); w = p['executed_weights']; idx = w.index
    net = p['net_returns'].reindex(idx); cr = p['daily_cash_rate']; cash_w = (1 - w.sum(axis=1)).clip(lower=0)
    eng = net + cash_w * (LF - cr)                       # engine with idle cash in the liquid fund (fair baseline)
    rg, close = daily_gold(idx); gv = rg.notna(); window = gv & (idx >= '2003-01-01'); pvf = pv_fraction(idx, close).fillna(0)
    bh = rg.fillna(0.0); pv = pvf * rg.fillna(0.0) + (1 - pvf) * LF
    base = stitched_metrics(eng[window]); bm = mon(eng[window])
    for lab, sleeve in (('static 10% buy&hold gold', bh), ('static 10% persistence-vol gold', pv)):
        for wgt in (0.05, 0.10):
            r = (1 - wgt) * eng + wgt * sleeve; m = stitched_metrics(r[window]); pS, pD, lo, hi = block_boot_delta(mon(r[window]).values, bm.values, reps=1500)
            rows.append(dict(strategy=name, sleeve=lab, weight=wgt, base_cagr=base['cagr'], base_sharpe=base['sharpe'], base_maxdd=base['maxdd'], d_cagr=m['cagr'] - base['cagr'], d_sharpe=m['sharpe'] - base['sharpe'],
                             d_maxdd=m['maxdd'] - base['maxdd'], P_dSharpe_pos=pS, P_dMaxDD_better=pD, corr_with_book=np.corrcoef(sleeve[window].fillna(0), eng[window].fillna(0))[0, 1]))
R = pd.DataFrame(rows); R.to_csv('results_static_sleeve_real_engines.csv', index=False, float_format='%.4f')
pd.set_option('display.width', 220); print(R.round(3).to_string(index=False))
