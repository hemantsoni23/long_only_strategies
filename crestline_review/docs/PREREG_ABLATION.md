# Crestline v2.3 - ablation and parameter study: pre-registration (written 2026-10-12, BEFORE any run)

Subject: `crestline_v2_3.py` (fixed baseline). Base = its defaults (2006-25, cash 6.5%, CA_ADJUST, TOP_N 15, rebalance 60, universe ranks 1-1000, INITIAL_CAPITAL 1 lakh).
Every variant runs at the 6 schedule anchors {0,10,..,50}; all statistics are anchor means. Gating metric = Sharpe vs rf 6.5% ("Sh65"); CAGR, rf0 Sharpe, MaxDD, exposure, turnover shown.
Periods: P_A = 2006-2014, P_B = 2015-2025.

## Part 1 - component ablation (leave one out; what does each piece contribute?)
hard stop off | 15% peak stop off | vol-scaled stop off | all three stops off | rank exit off (EXIT_RANK_MULT=50) | bear scaling off (BEAR_SCALE=1) | panic scaling off (PANIC_SCALE=1) | overlay off |
price floor off (MIN_PRICE=0) | liquidity band off (UNIVERSE_TOP_N_MAX=5000) | circuit filter off (MAX_CIRCUIT_DAYS=63) | HP leg off | TP leg off.
Reported as contribution = base - variant. No selection happens here; it is a map of what matters.

## Part 2 - one-at-a-time parameter sweeps (fixed grids; base value in bold; nothing is added after seeing results)
| parameter | grid |
|---|---|
| TOP_N | 10, 20, 25, 30, 40, **15** |
| EXIT_RANK_MULT | 1.0, 1.5, 3, 4, **2** |
| REBALANCE_FREQ_DAYS | 30, 40, 50, 75, 90, 120, **60** |
| HP_WINDOW (min periods = 0.8 x) | 126, 189, 378, **252** |
| TP_LOOKBACK (min periods = 0.8 x) | 63, 126, 252, 315, **189** |
| TP_SMA_WINDOW (min periods = 0.8 x) | 20, 100, 150, **50** |
| HARD_STOP_PCT | 0.10, 0.15, 0.25, 0.30, **0.20** |
| PEAK_STOP_PCT | 0.10, 0.20, 0.25, 0.30, **0.15** |
| VOLSTOP_K | 1.5, 2.0, 3.5, 5.0, **2.5** |
| vol-stop clip (MIN, MAX) | (0.08,0.20), (0.12,0.30), (0.15,0.35), (0.20,0.40), **(0.10,0.25)** |
| BEAR_SCALE | 0.3, 0.45, 0.8, 1.0, **0.6** |
| PANIC_SCALE | 0.0, 0.15, 0.5, 1.0, **0.3** |
| PANIC_PCTL | 0.80, 0.90, 0.98, **0.95** |
| BENCH_SMA | 100, 150, 250, **200** |
| MIN_PRICE | 10, 50, 100, **20** |
| UNIVERSE_TOP_N_MAX | 500, 750, 1500, **1000** |
| MAX_CIRCUIT_DAYS | 2, 10, **5** |
| COST_ONE_WAY (information only, never adopted) | 0.0015, 0.005 |

## Adoption rule for a changed value (all must hold, vs base)
* A1: mean dSh65 >= +0.08 (stricter than the +0.10-without-plateau used earlier, because ~70 values are compared; expect ~3 spurious single-gate passes)
* A2: dSh65 > 0 in BOTH P_A and P_B (mean over anchors)
* A3: dSh65 > 0 in >= 5 of 6 anchors
* A4: mean MaxDD no more than 3 pts worse than base
* A5 (plateau): the adjacent grid value(s) on the same side also have dSh65 >= 0 (a spike with worse neighbours is treated as noise, not adopted)
Values passing A1-A4 but failing A5 are "spike - not adopted". Values that raise CAGR but fail A1 are listed as RISK-DIAL moves (return up, drawdown up, Sharpe flat) - never adopted as improvements.
If several values of one parameter pass, take the one closest to base (smallest move).

## Joint step (fixed now)
Adopted values (max 5, ordered by dSh65) are added one at a time; an addition stays only if the stack still passes A1-A4 against the previous stack. The final set is then checked with: cost x2 (0.6% per side), cash 0%, the 2015-25 window alone, and the 6-anchor staggered blend. No further tuning after the joint step; any change is logged below.

## Sensitivity deliverable (no selection involved)
For each parameter: Sh65 range across the grid and whether base sits on a plateau, a slope, or a peak. This, not a single "best" value, is the main output.

## Caveats stated in advance
* No lockbox; all of 2006-25 is in-sample. A1-A5 reduce, not remove, the winner's curse; expect adopted gains to shrink out of sample.
* INITIAL_CAPITAL stays 1 lakh, so liquidity-sensitive parameters (TOP_N_MAX, MIN_PRICE, circuit filter, TOP_N) are tested capacity-free. They must be re-checked at the real book size before going live.
* Survivorship and thin pre-2020 volume as before.

## Post-look change log
* Rule application (mechanical, no discretion): TOP_N 25, 30 and 40 all pass A1-A5; 25 is taken (smallest move). TP_SMA_WINDOW=20 and TP_LOOKBACK=126 pass. Joint-step order by dSh65: TOP_N=25 (+0.18), TP_SMA_WINDOW=20 (+0.14), TP_LOOKBACK=126 (+0.13).
* Not adopted although attractive: universe-band / price-floor removals (UNIVERSE_TOP_N_MAX=1500 fails A2 in P_A; liq_band_off, price_floor_off, MIN_PRICE=10 are capacity-free gains from illiquid/low-priced names - need the real book size first).
* Observation, not acted on: TP_SMA_WINDOW=20 is the EDGE of its grid and the slope is monotone (20 > 50 > 100); a shorter window was not in the fixed list, so it is NOT tested here.
* Joint step outcome so far: S1 (TOP_N=25) passes (+0.18, 6/6). S2 (+TP_SMA_WINDOW=20) vs S1: +0.01, 3/6 -> fails A1, DROPPED. My first S3 run stacked TP_LOOKBACK=126 on top of the dropped S2 - that is not the rule; the correct S3' = S1 + TP_LOOKBACK=126 is run and judged vs S1. (The S2->S3 numbers are kept in results_joint.csv as information only.)
