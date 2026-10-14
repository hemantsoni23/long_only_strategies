import pandas as pd, runner
from experiments import VARIANTS, OFFS
import experiments2 as e2
CA = dict(CA_ADJUST=True)
singles = {k: dict(v, **CA) for k, v in VARIANTS.items()}
full = {k: dict(v, **CA) for k, v in e2.full.items()}
part = {k: dict(v, **CA) for k, v in e2.part.items()}
if __name__ == "__main__":
    a = runner.sweep(singles, OFFS, workers=5); a.to_csv("results_singles_ca.csv", index=False)
    b = runner.sweep(full, OFFS, workers=5)
    c = runner.sweep(part, [0, 20, 40], workers=5)
    pd.concat([b, c]).to_csv("results_stack_ca.csv", index=False)
    print("done")
