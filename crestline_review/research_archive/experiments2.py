import pandas as pd, runner
from experiments import V, VARIANTS
G5 = dict(UNIVERSE_TOP_N_MIN=301)
full = {
 "B0":   dict(START_DATE="2006-01-01", CASH_RATE_ANNUAL=0.0),
 "ST2":  V(**G5, TOP_N=25),
 "PL1a": V(TOP_N=40),
 "PL1b": V(**G5, TOP_N=40),
 "B15":  dict(START_DATE="2015-01-01", CASH_RATE_ANNUAL=0.0),
 "G5_15":  dict(START_DATE="2015-01-01", CASH_RATE_ANNUAL=0.0, **G5),
 "ST2_15": dict(START_DATE="2015-01-01", CASH_RATE_ANNUAL=0.0, **G5, TOP_N=25),
}
part = {}
for tag, kw in [("B", {}), ("G5", G5), ("ST2", dict(**G5, TOP_N=25))]:
    for cap, n in [(1e7, "c1"), (5e7, "c2"), (2e8, "c3")]:
        part[f"{tag}_{n}"] = V(INITIAL_CAPITAL=cap, **kw)
    part[f"{tag}_cost6"] = V(COST_ONE_WAY=0.006, **kw)
if __name__ == "__main__":
    a = runner.sweep(full, [0, 10, 20, 30, 40, 50], workers=5)
    b = runner.sweep(part, [0, 20, 40], workers=5)
    pd.concat([a, b]).to_csv("results_stack.csv", index=False)
    print("done")
