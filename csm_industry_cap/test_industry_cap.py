"""P0 parity: with K=0 the cap subclasses must reproduce the unmodified live engines exactly (positions and net returns).  python3 test_industry_cap.py"""
import time
import numpy as np
from common import load_panels, run_engine

kw = load_panels()
for which in ('zenith', 'elendel'):
    t = time.time()
    s0, r0 = run_engine(which, kw, cap_k=None)
    s1, r1 = run_engine(which, kw, cap_k=0)
    dp = float(np.abs(s0.positions.fillna(0).values - s1.positions.reindex_like(s0.positions).fillna(0).values).max())
    dr = float(np.abs(r0['net_returns'].values - r1['net_returns'].reindex(r0['net_returns'].index).values).max()) if len(r0['net_returns']) == len(r1['net_returns']) else float('nan')
    print(f'{which}: max|d positions| = {dp:.3e}   max|d net returns| = {dr:.3e}   len {len(r0["net_returns"])} vs {len(r1["net_returns"])}   ({time.time()-t:.0f}s for 2 runs)')
    assert dp == 0.0 and dr == 0.0, 'PARITY FAILED'
print('P0 PARITY PASS')
