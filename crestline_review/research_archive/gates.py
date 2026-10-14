import sys, numpy as np, pandas as pd
def gate_table(df, base="B"):
    b = df[df.variant == base].set_index("offset")
    out = []
    for v, g in df.groupby("variant", sort=False):
        g = g.set_index("offset")
        d = g.sh65 - b.sh65
        p1 = d.mean(); pa = (g.sh65_h1 - b.sh65_h1).mean(); pb = (g.sh65_h2 - b.sh65_h2).mean()
        n_pos = int((d > 0).sum()); dd = g.mdd.mean() - b.mdd.mean()
        out.append(dict(variant=v, CAGR=g.cagr.mean(), Sh0=g.sh0.mean(), Sh65=g.sh65.mean(), dSh65=p1, dPA=pa, dPB=pb, pos=f"{n_pos}/{len(d)}",
                        MDD=g.mdd.mean(), dMDD=dd, expo=g.expo.mean(), turn=g.turn.mean(), sdSh65=g.sh65.std(),
                        P1=p1 >= 0.10, P2=(pa > 0) and (pb > 0), P3=n_pos >= 4, P4=dd >= -3.0))
    t = pd.DataFrame(out)
    t["verdict"] = np.where(t.P1 & t.P2 & t.P3 & t.P4, "CARRY", np.where(t.P1 & t.P2, "interesting", "-"))
    t.loc[t.variant == base, "verdict"] = "base"
    return t
if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    t = gate_table(df)
    pd.set_option("display.width", 250)
    print(t.drop(columns=["P1","P2","P3","P4"]).round(2).to_string(index=False))
