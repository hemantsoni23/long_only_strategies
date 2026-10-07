"""GoldIdleCashOverlay.apply() must reproduce the analysis (results_final_gold_idle.csv, candidate C1, drift 1.0, cost 0.15%) for every strategy."""
import pickle, sys
import numpy as np, pandas as pd
from gold_idle_cash import GoldIdleCashOverlay
from analyze_gold_idle import stitched_metrics
ref = pd.read_csv('results_final_gold_idle.csv')
ok_all = True
for name in ('elendel', 'zenith', 'quad'):
    p = pickle.load(open(f'.cache/engine_{name}.pkl', 'rb'))
    ov = GoldIdleCashOverlay(cap=0.10, mode='weak')
    out = ov.apply(p['executed_weights'], p['net_returns'], p['regime'], p['daily_cash_rate'])
    win = out.gold_valid & (out.index >= '2003-01-01')
    m = stitched_metrics(out.net_return[win])
    r = ref[(ref.strategy == name) & (ref.variant.str.startswith('C1')) & (ref.mult.astype(str) == '1.0') & (ref.cost == 0.0015)].iloc[0]
    d = {k: abs(m[k] - r[k]) for k in ('cagr', 'sharpe', 'maxdd')}
    ok = all(v < 6e-5 for v in d.values()); ok_all &= ok
    print(f'{name:8s} overlay CAGR {m["cagr"]:.4f} Sharpe {m["sharpe"]:.4f} MaxDD {m["maxdd"]:.4f} | analysis {r.cagr:.4f} {r.sharpe:.4f} {r.maxdd:.4f} | max diff {max(d.values()):.2e} -> {"OK" if ok else "FAIL"}')
    # structural checks
    assert (out.gold_weight <= 0.10 + 1e-12).all() and (out.gold_weight <= out.idle_cash_weight + 1e-12).all(), 'cap / idle constraint violated'
    assert (out.gold_weight[~out.gold_valid] == 0).all(), 'gold held on a day with unusable gold data'
    assert (out.gold_weight[~out.regime.isin(['BEAR', 'PANIC', 'HIGH_VOL'])] == 0).all(), 'gold held outside weak regimes'
    off = GoldIdleCashOverlay(mode='off').apply(p['executed_weights'], p['net_returns'], p['regime'], p['daily_cash_rate'])
    assert (off.gold_weight == 0).all()
print('LIVE RULE CHECK:', GoldIdleCashOverlay().target_gold_weight(0.55, 'BEAR'), GoldIdleCashOverlay().target_gold_weight(0.55, 'BULL'), GoldIdleCashOverlay().target_gold_weight(0.04, 'PANIC'))
assert GoldIdleCashOverlay().target_gold_weight(0.55, 'BEAR') == 0.10 and GoldIdleCashOverlay().target_gold_weight(0.55, 'BULL') == 0.0 and GoldIdleCashOverlay().target_gold_weight(0.04, 'PANIC') == 0.04
print('ALL OVERLAY PARITY / CONSTRAINT CHECKS PASSED' if ok_all else 'PARITY FAILED'); sys.exit(0 if ok_all else 1)
