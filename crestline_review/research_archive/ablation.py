"""Part 1 (component ablation) + Part 2 (one-at-a-time sweeps) on crestline_v2_3.py. Fixed lists per PREREG_ABLATION.md."""
import os, json, sys, pandas as pd
import anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
def mp(w): return int(round(w * 0.8))
V = {"base": {}}
# Part 1
for k, o in {"hard_off": dict(USE_HARD_STOP=False), "peak_off": dict(USE_PEAK_STOP=False), "volstop_off": dict(USE_VOL_SCALED_STOP=False),
             "all_stops_off": dict(USE_HARD_STOP=False, USE_PEAK_STOP=False, USE_VOL_SCALED_STOP=False),
             "rank_exit_off": dict(EXIT_RANK_MULT=50.0), "bear_scale_off": dict(BEAR_SCALE=1.0), "panic_scale_off": dict(PANIC_SCALE=1.0), "overlay_off": dict(USE_OVERLAY=False),
             "price_floor_off": dict(MIN_PRICE=0.0), "liq_band_off": dict(UNIVERSE_TOP_N_MAX=5000), "circuit_filter_off": dict(MAX_CIRCUIT_DAYS=63),
             "HP_leg_off": dict(SCORE_W_HP=0.0), "TP_leg_off": dict(SCORE_W_TP=0.0)}.items():
    V[f"abl|{k}"] = o
# Part 2
def add(p, vals, fn=lambda v: {}):
    for v in vals: V[f"{p}={v}"] = fn(v)
add("TOP_N", [10, 20, 25, 30, 40], lambda v: dict(TOP_N=v))
add("EXIT_RANK_MULT", [1.0, 1.5, 3.0, 4.0], lambda v: dict(EXIT_RANK_MULT=v))
add("REBALANCE_FREQ_DAYS", [30, 40, 50, 75, 90, 120], lambda v: dict(REBALANCE_FREQ_DAYS=v))
add("HP_WINDOW", [126, 189, 378], lambda v: dict(HP_WINDOW=v, HP_MIN_PERIODS=mp(v)))
add("TP_LOOKBACK", [63, 126, 252, 315], lambda v: dict(TP_LOOKBACK=v, TP_MIN_PERIODS=mp(v)))
add("TP_SMA_WINDOW", [20, 100, 150], lambda v: dict(TP_SMA_WINDOW=v, TP_SMA_MIN_PERIODS=mp(v)))
add("HARD_STOP_PCT", [0.10, 0.15, 0.25, 0.30], lambda v: dict(HARD_STOP_PCT=v))
add("PEAK_STOP_PCT", [0.10, 0.20, 0.25, 0.30], lambda v: dict(PEAK_STOP_PCT=v))
add("VOLSTOP_K", [1.5, 2.0, 3.5, 5.0], lambda v: dict(VOLSTOP_K=v))
for lo, hi in [(0.08, 0.20), (0.12, 0.30), (0.15, 0.35), (0.20, 0.40)]: V[f"VOLSTOP_CLIP=({lo},{hi})"] = dict(VOLSTOP_MIN_PCT=lo, VOLSTOP_MAX_PCT=hi)
add("BEAR_SCALE", [0.3, 0.45, 0.8, 1.0], lambda v: dict(BEAR_SCALE=v))
add("PANIC_SCALE", [0.0, 0.15, 0.5, 1.0], lambda v: dict(PANIC_SCALE=v))
add("PANIC_PCTL", [0.80, 0.90, 0.98], lambda v: dict(PANIC_PCTL=v))
add("BENCH_SMA", [100, 150, 250], lambda v: dict(BENCH_SMA=v, BENCH_SMA_MIN_PERIODS=mp(v)))
add("MIN_PRICE", [10.0, 50.0, 100.0], lambda v: dict(MIN_PRICE=v))
add("UNIVERSE_TOP_N_MAX", [500, 750, 1500], lambda v: dict(UNIVERSE_TOP_N_MAX=v))
add("MAX_CIRCUIT_DAYS", [2, 10], lambda v: dict(MAX_CIRCUIT_DAYS=v))
add("COST_ONE_WAY", [0.0015, 0.005], lambda v: dict(COST_ONE_WAY=v))
if __name__ == "__main__":
    jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
    print(len(V), "variants,", len(jobs), "runs", flush=True)
    with ThreadPoolExecutor(5) as ex:
        dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
    rows = [dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]
    pd.DataFrame(rows).to_csv("results_ablation.csv", index=False); print("done")
