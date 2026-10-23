"""Addendum 8: user's second improvement list (Part 1 improvements, Part 2 OHLCV liquidity filters) on Aegis v1.2, through the product module."""
import os, sys, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "csm_aegis"))
from csm_aegis_strategy import CSMAegis, load_data
import csm_aegis_backtest as BT
from ovl_metrics import met
from ovl_judge import judge
DATA = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"; CACHE = os.path.join(HERE, ".cache")
P = load_data(DATA, cache_dir=CACHE)

def run(name, **kw):
    S = CSMAegis.from_preset("v1.2", *P, **kw).calculate_factors()
    res = BT.backtest_event_driven(S, log_rejects=False); r = res["ret"]; m = met(r)
    yrs = len(r[r.index >= "2005-01-01"]) / 252; m["turn"] = res["turnover"] / yrs if "turnover" in res else np.nan
    hA, hB = met(r, "2005-01-01", "2012-12-31"), met(r, "2013-01-01")
    m.update(shA=hA["sharpe"], shB=hB["sharpe"], ddA=hA["maxdd"], ddB=hB["maxdd"], cagrA=hA["cagr"], cagrB=hB["cagr"])
    m["sh_l2"] = met(r, "2020-06-01", "2026-06-30")["sharpe"]; m["r25"] = float((1 + r.loc["2025-01-01":]).prod() - 1)
    S.transaction_cost = 0.006; m["sh_c6"] = met(BT.backtest_event_driven(S, log_rejects=False)["ret"])["sharpe"]; S.transaction_cost = 0.003
    S.adv_fraction, S.initial_capital = 0.05, 5e7; m["cagr_5cr"] = met(BT.backtest_event_driven(S, log_rejects=False)["ret"])["cagr"]; S.adv_fraction, S.initial_capital = None, 1.0
    pools = [S.filter_universe(k) for k in range(len(S.me)) if S.me[k] >= pd.Timestamp("2005-01-01")]
    m["pool"] = float(np.mean([p.sum() for p in pools])); m["test"] = name
    m["_pools"] = pools
    return m

if __name__ == "__main__":
    cfgs = [("baseline v1.2", {}),
            ("I1 cash 6.5%", dict(cash_rate=0.065)),
            ("I2 vol gate off", dict(vol_gate=False)),
            ("I3 ATR stops+sizing", dict(atr_stops=True)),
            ("I4 hold_rank 50", dict(hold_rank=50)), ("I4 hold_rank 60", dict(hold_rank=60)), ("I4 hold_rank 32", dict(hold_rank=32)),
            ("U1 floor20 top1000", dict(liq_mode="floor20")), ("U1b floor20 >= 25L", dict(liq_mode="floor20_abs")),
            ("U2 Amihud top1000", dict(liq_mode="amihud")), ("U3 continuity>=0.95", dict(liq_mode="continuity")),
            ("U4 vol CV<=1.8", dict(liq_mode="cvvol")), ("U5 CS spread drop 15%", dict(liq_mode="cs_spread")),
            ("U6 tradability (pasted)", dict(liq_mode="tradability")), ("U6b tradability log-floor", dict(liq_mode="tradability_log"))]
    rows, base_pool = [], None
    for name, kw in cfgs:
        m = run(name, **kw); pools = m.pop("_pools")
        if base_pool is None: base_pool = pools
        m["kept_vs_base"] = float(np.mean([(a & b).sum() / max(b.sum(), 1) for a, b in zip(pools, base_pool)]))
        rows.append(m); print(name, f"CAGR {m['cagr']:.3f} Sh {m['sharpe']:.2f} DD {m['maxdd']:.3f} pool {m['pool']:.0f} kept {m['kept_vs_base']:.2f}", flush=True)
        pd.DataFrame(rows).to_csv(os.path.join(HERE, "results", "addendum8_runs.csv"), index=False)
    d = pd.DataFrame(rows); b = d.iloc[0].to_dict()
    d["why_fail"] = [("; ".join(judge(r, b)) if i else "") for i, r in enumerate(d.to_dict("records"))]
    d.to_csv(os.path.join(HERE, "results", "addendum8_runs.csv"), index=False)
