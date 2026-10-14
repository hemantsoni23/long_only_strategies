import sys, pandas as pd, runner
BASE = dict(START_DATE="2006-01-01", CASH_RATE_ANNUAL=0.065)
def V(**kw): return dict(BASE, **kw)
NOTRAIL = dict(USE_PEAK_STOP=False, USE_VOL_SCALED_STOP=False)
VARIANTS = {
 "B":  V(),
 "R1": V(USE_SLOT_REFILL=True, REFILL_FREQ_DAYS=20, REFILL_COOLDOWN_DAYS=30),
 "R2": V(USE_SLOT_REFILL=True, REFILL_FREQ_DAYS=10, REFILL_COOLDOWN_DAYS=20),
 "S1": V(USE_PEAK_STOP=False),
 "S2": V(USE_VOL_SCALED_STOP=False),
 "S3": V(USE_PEAK_STOP=False, VOLSTOP_K=4.0, VOLSTOP_MIN_PCT=0.15, VOLSTOP_MAX_PCT=0.35),
 "S4": V(**NOTRAIL, USE_TREND_BREAK_STOP=True),
 "S5": V(**NOTRAIL),
 "C1": V(REBALANCE_FREQ_DAYS=30), "C2": V(REBALANCE_FREQ_DAYS=40), "C3": V(REBALANCE_FREQ_DAYS=90),
 "G1": V(SCORE_W_HP=0.0), "G2": V(SCORE_W_TP=0.0), "G3": V(RESID_W=0.5), "G4": V(M3_EXCL_Q=0.2),
 "G5": V(UNIVERSE_TOP_N_MIN=301),
 "X1": V(USE_OVERLAY=False), "X2": V(BEAR_NO_ENTRY=True), "X3": V(SIZE_BY_VOL=True),
 "X4": V(TOP_N=10), "X5": V(TOP_N=25), "X6": V(EXIT_RANK_MULT=3.0),
}
OFFS = [0, 10, 20, 30, 40, 50]
if __name__ == "__main__":
    df = runner.sweep(VARIANTS, OFFS, workers=5)
    df.to_csv("results_singles.csv", index=False)
    print("done", len(df))
