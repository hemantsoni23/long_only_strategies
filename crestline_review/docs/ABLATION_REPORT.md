# Crestline v2.3 - ablation and parameter study (2026-10-12)

Protocol: `PREREG_ABLATION.md` (fixed before running). Code: `ablation.py`, `ablation_report.py`, `joint.py`, `joint2.py`. Raw: `results_ablation.csv`, `ablation_table.csv`, `ablation_report.txt` (every grid, full tables), `results_joint*.csv`.
79 variants x 6 schedule anchors, 2006-25, cash 6.5%, INITIAL_CAPITAL 1 lakh. Base (v2.3): CAGR 17.5%, Sharpe vs 6.5% 0.95 (rf0 1.51), MaxDD -25.3%, exposure 51%, turnover 280%/yr.

## Headline
**Only one parameter change survives the pre-registered rules: TOP_N 15 -> 25** (v2.4). Every other base value sits on a plateau or on a pure return-vs-drawdown slope. This is a result, not a failure: the colleague's parameters are reasonable apart from breadth, and there is no hidden "best setting" to find by knob-turning. Further gains must come from structure (next round), not tuning.

## 1. What each component contributes (leave-one-out; negative dSh65 = the component helps)
| removed | dSh65 | dCAGR | dMaxDD | reading |
|---|---|---|---|---|
| all three stops | **-0.15** | +3.7 | **-29.9** | stops are essential (MaxDD -55% without) |
| HP (52w-high) leg | -0.10 | -1.1 | -2.6 | needed |
| TP (trend persistence) leg | -0.14 | -2.1 | +2.0 | needed |
| overlay (bear + panic) | -0.06 | +0.5 | -11.3 | worth ~11 MaxDD pts, almost all from the BEAR tier (-8.0); panic tier -2.3 |
| rank exit | -0.02 | -0.8 | 0.0 | nearly irrelevant |
| **hard stop (20%)** | **0.00** | 0.00 | 0.00 | **dead code: identical to base on every metric** (a position that loses 20% from entry has always already tripped a trailing stop) |
| 15% peak stop | 0.00 | +0.2 | -3.1 | barely binds |
| vol-scaled stop | +0.04 | +2.4 | -4.7 | then the 15% peak stop does the job; less protection, more return |
| price floor (Rs 20) | +0.08 (6/6) | +0.9 | 0.0 | removing it helps - gain comes from low-priced, likely illiquid names (capacity-free) |
| liquidity band (rank <= 1000) | +0.25 (6/6; P_A -0.01, P_B +0.45) | +3.0 | -0.1 | same: micro-cap gains that need the real book size |
| circuit filter | +0.05 | +0.4 | +0.6 | mixed (P_A +0.18, P_B -0.03) |

**The "stop stack" is really one stop**: a trailing stop from peak close at min(15%, clip(2.5 x ATR%, 10%, 25%)), i.e. 10-15% for almost every name. The hard stop can be deleted without changing anything; the peak and vol stops overlap. (Simplification candidate for the next round, not a performance gain.)

## 2. Sensitivity map (Sharpe range across the pre-set grid; where base sits)
| parameter | base | Sh65 range | shape | note |
|---|---|---|---|---|
| HP_WINDOW | 252 | 0.93-0.95 | **flat** | irrelevant between 126 and 378 |
| EXIT_RANK_MULT | 2 | 0.88-0.96 | flat for >= 2 | 1.0-1.5 worse (-0.04 to -0.07) |
| HARD_STOP_PCT | 0.20 | 0.93-0.95 | **dead** | 0.25/0.30 identical to base; 0.10 slightly worse |
| PEAK_STOP_PCT | 0.15 | 0.90-0.95 | flat >= 0.15; 0.10 lowers MaxDD by 4 pts at -0.05 Sharpe | risk dial |
| PANIC_SCALE | 0.3 | 0.93-0.95 | flat Sharpe; MaxDD -24.2 (0.0) to -27.6 (1.0) | |
| BENCH_SMA | 200 | 0.94-0.97 | flat | 100-150 marginally better, not significant |
| BEAR_SCALE | 0.6 | 0.91-0.95 | plateau <= 0.6; **0.45 / 0.3 keep Sharpe, cut MaxDD 1.7 / 2.0 pts** | risk dial |
| VOLSTOP_K / clip | 2.5 / (0.10, 0.25) | 0.91-1.00 | **monotone slope**: wider = +2.4 CAGR, -4.5 MaxDD, Sharpe +0.04..+0.05 | risk dial (fails A1) |
| REBALANCE_FREQ | 60 | 0.84-0.99 | hump 40-60; 40 gives +1.8 CAGR for -5.3 MaxDD; >= 90 loses | risk dial |
| PANIC_PCTL | 0.95 | 0.95-1.00 | 0.90: Sharpe +0.04, MaxDD +3.5 pts (P_A +0.10, P_B +0.01, 5/6) - best "free" risk reducer, below the +0.08 bar | candidate for next round |
| TP_LOOKBACK | 189 | 0.84-1.08 | **peaky**: 126 best (+0.13), 63 +0.02, >= 252 clearly worse (-0.10) | gain disappears once breadth is fixed (below) |
| TP_SMA_WINDOW | 50 | 0.84-1.09 | monotone: shorter better; 20 is the EDGE of the grid | gain disappears once breadth is fixed |
| TOP_N | 15 | 0.79-1.19 | **monotone, saturating** 10 -> 15 -> 25 -> 40 | adopted 25 |
| MIN_PRICE | 20 | 0.86-1.00 | lower = better | capacity-driven |
| UNIVERSE_TOP_N_MAX | 1000 | 0.93-1.11 | larger = better in P_B only (fails A2) | capacity-driven |
| MAX_CIRCUIT_DAYS | 5 | 0.91-0.97 | flat | |
| COST_ONE_WAY (info) | 0.3% | 0.86-1.02 | each 0.15% per side = ~0.07-0.09 Sharpe, ~1 CAGR pt | book turns 280%/yr |

## 3. Adoption and joint step (pre-registered rules A1-A5, then stack rule)
Single-parameter passes: TOP_N 25/30/40, TP_SMA_WINDOW 20, TP_LOOKBACK 126. Taken in order of gain (TOP_N smallest move = 25):
| step | dSh65 | P_A / P_B | anchors + | dMaxDD | dCAGR | kept? |
|---|---|---|---|---|---|---|
| B -> TOP_N 25 | **+0.18** | +0.12 / +0.23 | 6/6 | -0.2 | +1.3 | **yes** |
| + TP_SMA_WINDOW 20 | +0.01 | +0.05 / -0.01 | 3/6 | +0.9 | +0.3 | no |
| + TP_LOOKBACK 126 (on the kept stack) | +0.05 | +0.04 / +0.06 | 3/6 | +0.3 | +1.0 | no |
The two window changes looked good alone but were mostly the same effect as breadth (they lift turnover and rotate into more names); on top of 25 names they add nothing reliable.

**Final: v2.4 = v2.3 with TOP_N = 25.** 2006-25: CAGR 17.5 -> 18.8%, Sharpe65 0.95 -> 1.13, MaxDD -25.3 -> -25.5%, turnover 280 -> 272%/yr.
Robustness of the change (vs the same-setting v2.3): cost 0.6%/side +0.17 (5/6 anchors); cash 0% +0.15 (5/6); 2015-25 window alone +0.11 (5/6 anchors; Sharpe 0.77 -> 0.87, CAGR 15.1 -> 15.6%, MaxDD -20.1 -> -16.6%; cash 6.5%). The gain is smaller in 2015-25 (+0.11) than over the whole sample (+0.18) - expect less out of sample.

## 4. Things this study does NOT settle
* Capacity: the lower-price / wider-band / liquidity-off gains (+0.08 to +0.25) are real in this panel but come from illiquid names and are untestable at 1 lakh. They need capacity-aware sizing at the real book size (open since the review; capital still unknown).
* TOP_N = 25 has not been separately capacity-tested; a 25-name book makes each ticket smaller, which should help, but that is a hypothesis.
* Tuning stops/overlay changes the risk level, not the quality: use the risk-dial rows (wider vol stop, rebalance 40, bear scale 0.45, panic percentile 0.90) to pick drawdown tolerance AFTER the structural round.
* All in-sample; 79 variants compared (expect ~3-4 spurious single-gate passes - consistent with the two window passes that vanished in the stack). No lockbox.

## 5. Suggested next round (needs its own pre-registration, now on v2.4)
1. Capacity-aware sizing (walk down the rank list when the ADV cap binds) at an explicit book size - unlocks or kills the micro-cap gains above.
2. De-risking overlay on HELD positions (bear tier is worth 8 MaxDD pts but only acts on new entries today).
3. Staggered tranches (blend measured +0.14..+0.21 Sharpe, -1..-4 MaxDD earlier).
4. Simplify the stop to one trailing stop (hard stop is dead, peak/vol overlap) and test a time-asymmetric width.
5. Panic percentile 0.90 as a candidate drawdown reducer; shorter TP SMA windows (<20) only if re-registered.
