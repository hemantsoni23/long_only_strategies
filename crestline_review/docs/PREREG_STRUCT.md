# Structural round: staggering, vol-sizing, relative-strength exits, capacity walk, weak regimes - pre-registration (written 2026-10-12, BEFORE any run)

Base B = `crestline_v2_4.py` defaults (TOP_N 25, 2006-25, cash 6.5%, CA_ADJUST, INITIAL_CAPITAL 1 lakh). New mechanisms live in `crestline_struct_lab.py` (generated from the exits lab; every switch default OFF must reproduce v2.4 bit-exactly - tested).
Statistics: anchor means (schedule offsets), Sharpe vs 6.5% (Sh65) as the gating metric; P_A = 2006-14, P_B = 2015-25. "N1-N4" below = the same adoption bars as the exits round:
N1 dSh65 >= +0.08; N2 positive in BOTH periods; N3 positive in >= 5 of 6 anchors (or all groups for blends); N4 mean MaxDD no more than 3 pts worse.

## T1 Staggering (post-processing of independent anchor runs = K separate sub-accounts of 1/K capital; no engine change)
12 anchors {0,5,...,55}. Blend = mean of the sub-account equity curves over the common window (no rebalancing between sub-accounts). Groups of K evenly spaced anchors: K=2 {0,30},{5,35},..; K=3 {0,20,40},{5,25,45},..; K=4; K=6 {0,10..50},{5,15..55}; K=12 all.
Books: N25 (v2.4), N75, N150 (breadth-matched singles), N24, N8, N4 (names-matched; MAX_ENTRY_PCT lifted to 1.0 for N8 and N4 so 1/N is not clipped at 10%).
* Q1 (the structural question, GATED): does staggering help at CONSTANT total names? blend(K=3, N8) and blend(K=6, N4) vs single N24. Pass = N1-N4 with all groups positive, for K=3 AND K=6.
* Q2 (descriptive): blend(K, N25) vs single N25*K for K=3, 6 (is staggering worth anything once breadth is bought directly?).
* Q0 (descriptive): blend(K, N25) vs single N25 for K = 2, 3, 4, 6, 12 (the earlier +0.14..+0.21).

## T2 Volatility-based sizing (entry weight = (1/N) x clip(ref / x, lo, hi); ref = pool median of x at the signal bar; weights capped only by the ADV rule and 10% per name)
| id | x | clip (lo, hi) |
|---|---|---|
| VS1 | ATR% | (0.5, 1.5) |
| VS2 | ATR% | (0.33, 2.0) |
| VS3 | stop width = clip(2.5 ATR%, 10%, 25%) (equal risk per stop) | (0.5, 1.5) |
| VS4 | stop width | (0.33, 2.0) |
Single-variant gate N1-N4 vs B; family rule: >= 2 of 4 pass else "isolated"/not adopted; take the smallest move (VS1 < VS3 < VS2 < VS4 in that order).
Fixed combination (run regardless): best-by-dSh65 of VS1-VS4 + wide stops (VOLSTOP_K 5, clip (0.15, 0.35)), judged vs B with N1-N4 AND vs "wide stops alone" (does sizing make wide stops affordable?).
"Wide stops alone" = VOLSTOP_K 5, clip (0.15,0.35) is also run (known: CAGR +2.4, MaxDD -4.5 at TOP_N 15).

## T3 Relative-strength exit information (a source that is not the entry score)
RS = stock close / equal-weight benchmark; RS drawdown = 1 - RS / (peak RS since entry). While RS drawdown < threshold the PRICE trailing stops (peak, vol) are suppressed (the fall is market-driven); a catastrophic 25% trailing stop stays; hard stop stays.
RS1: threshold 5%. RS2: threshold 10%. N1-N4 + mechanism (mean hold up >= 10%, capture of MFE up >= 3 pts); family rule >= 2 of 2 else isolated.

## T4 Capacity-aware candidate walk
At each entry the candidate list extends to rank <= depth x N and skips names whose ADV cap (5% of 63-day median traded value) is below 0.5/N of equity; the first N-held slots are filled from what remains. Sizes still min(1/N, ADV cap).
Capital levels (INITIAL_CAPITAL): 1 cr, 5 cr, 20 cr. For each: B vs CW3 (depth 3) vs CW6 (depth 6). N1-N4 vs B at the SAME capital on the full window; P_B (2015-25) reported separately because pre-2020 volume is thin and distorts caps.

## T5 Weak-payoff regimes (descriptive first)
State variables at each signal date (5-bar grid): bench above SMA200 (0/1); bench 126-bar return; bench drawdown from its 252-bar high; cross-sectional dispersion (std of 60-bar returns in the pool); breadth (share of pool above SMA50); bench 21-bar realised vol (expanding percentile).
Outcome: top-25 excess return vs pool at 60 bars. Rule: a variable "predicts" if |Spearman| >= 0.15, HAC |t| >= 3, same sign in both halves (2006-14, 2015-25).
If at least one variable predicts: ONE conditional follow-up test (pre-registered here): scale NEW entries by 0.5 whenever the variable is in its adverse tercile (expanding terciles, no look-ahead), judged by N1-N4 vs B. If none predicts, the regime is reported as unforecastable with these variables and nothing is tested.
Also reported: strategy return/MaxDD by 3-year block and the three weak blocks' market context.

## Combination (only if >= 1 item passes): the adopted items are combined in the fixed order T1 > T2 > T3 > T4 > T5 and kept only if the stack still passes N1-N4 vs the previous stack; robustness (cost x2, cash 0%, 2015-25 only) on the final stack.

## Caveats stated in advance
In-sample 2006-25, no lockbox. ~30 comparisons in this round (expect ~2 spurious single-gate passes). Staggered K sub-accounts need K accounts (or tranche accounting) live. Pre-2020 volume is thin: capacity numbers are indicative. Post-look changes are logged below.

## Post-look change log
* Definition fix BEFORE any run (found by test 2 of test_struct_lab.py, mean entry weight was +11% above 1/N): the vol-sizing multiplier is rescaled so its pool-average is 1 (ref = pool-median / pool-mean of the clipped multiplier), so gross exposure per entry stays ~1/N and the test is about allocation, not leverage.
* Definition fix 2, still BEFORE any run: normalising to the POOL left mean entry weight +9% above 1/N (entrants are lower-vol than the pool). The reference is now the current top-N ranked names, rescaled so their average multiplier is 1.
