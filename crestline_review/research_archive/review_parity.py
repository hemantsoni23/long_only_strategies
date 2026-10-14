import os, numpy as np, pandas as pd, runner
d = runner.run({}, 0)
a = pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
b = pd.read_csv("/private/tmp/claude-501/-Users-hemantsoni-Documents-long-only-strategies/22c8d8c3-09cd-462d-8bb0-69ed232ee312/scratchpad/cl/crestline_v2_2_output/equity_curves.csv", index_col=0, parse_dates=True).iloc[:, 0]
print("lab vs original: identical =", np.allclose(a.values, b.values, rtol=0, atol=1e-6), " max abs diff", float(np.abs(a - b).max()), " n", len(a))
