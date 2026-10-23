"""Noise floor for Addendum 8: drop a random 4% of the baseline pool each month (seeded) and see how far Sharpe / Calmar / MaxDD move by chance."""
import os, sys, numpy as np, pandas as pd
from addendum8 import *
base = CSMAegis.from_preset("v1.2", *P).calculate_factors()
orig = base.filter_universe
rows = []
for seed in range(12):
    rng = np.random.default_rng(seed); drop = {k: rng.random(len(base.cols)) < 0.04 for k in range(len(base.me))}
    S = CSMAegis.from_preset("v1.2", *P).calculate_factors()
    f0 = S.filter_universe
    S.filter_universe = (lambda k, with_counts=False, f0=f0, drop=drop: (lambda e: (e & ~drop[k]) if not with_counts else (e[0] & ~drop[k], e[1]))(f0(k, with_counts)))
    res = BT.backtest_event_driven(S, log_rejects=False); m = met(res["ret"]); m["seed"] = seed; rows.append(m)
    print(seed, f"CAGR {m['cagr']:.3f} Sh {m['sharpe']:.2f} Calmar {m['calmar']:.2f} DD {m['maxdd']:.3f}", flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(HERE, "results", "addendum8_noise.csv"), index=False)
print(d[["cagr", "sharpe", "calmar", "maxdd"]].describe().round(3).to_string())
# halves + exposure for the candidates
for name, kw in (("baseline", {}), ("I1", dict(cash_rate=0.065)), ("U6b", dict(liq_mode="tradability_log")), ("I2", dict(vol_gate=False))):
    S = CSMAegis.from_preset("v1.2", *P, **kw).calculate_factors(); res = BT.backtest_event_driven(S, log_rejects=False); r = res["ret"]
    A, B = met(r, "2005-01-01", "2012-12-31"), met(r, "2013-01-01")
    print(name, "avg expo", round(float(res["expo"][res["expo"].index >= "2005-01-01"].mean()), 3), "A cagr/dd/calmar", round(A["cagr"], 3), round(A["maxdd"], 3), round(A["calmar"], 2), "B", round(B["cagr"], 3), round(B["maxdd"], 3), round(B["calmar"], 2))
