# Structural round on v2.4: staggering, vol-sizing, relative-strength exits, capacity walk, weak regimes (2026-10-12)

Protocol `PREREG_STRUCT.md` (fixed before running; two definition fixes to the sizing normalisation were made after unit tests and BEFORE any result, both logged). Code: `make_struct_lab.py` -> `crestline_struct_lab.py` (all switches off == v2.4, bit-exact; `test_struct_lab.py` 7/7 pass incl. truncation/no-look-ahead with every feature on), `experiments_struct.py`, `struct_report.py`, `diag_regime.py`, `exp_struct_combo.py`. Raw: `results_struct_*.csv`, `diag_regime.csv`.
Base B = v2.4 (25 names), 2006-25, cash 6.5%, 6 anchors (12 for the staggering books). Bars: N1 dSh65 >= +0.08, N2 both periods positive, N3 >= 5/6 anchors, N4 MaxDD within 3 pts.

## Verdict: nothing is adopted. v2.4 remains the baseline.
| item | best result | gated verdict |
|---|---|---|
| T1 staggering at constant total names (Q1) | blend K=3xN8 0.81 and K=6xN4 0.56 vs single N24 1.09 | **FAIL** |
| T2 vol-based sizing | VS2 (inverse ATR, clip 0.33-2.0): Sh65 +0.07, MaxDD +1.2 pts better, 5/6, both periods + | below +0.08 (near-miss) |
| T2 combination: VS2 + wide stops | +0.07 vs B, MaxDD -3.5 vs B (fails N4); +0.05 vs wide stops alone | fail |
| T3 relative-strength stop suppression | RS1 -0.05, RS2 -0.03; MaxDD -2.3 / -4.5 | fail |
| T4 capacity-aware candidate walk | Sharpe -0.06 to -0.12 at 1 / 5 / 20 cr; MaxDD -8.6 to -16.5 pts | fail |
| T5 weak regimes | no state variable meets the predict rule | nothing to test |

## T1 Staggering (12 anchors, sub-accounts at 1/K capital, no rebalancing between them)
Single books (mean of 12 anchors, common window 2006-03..2025): N25 Sh65 1.09 / CAGR 18.3 / MaxDD -24.5; N75 1.18; N150 1.15; N24 1.09; N8 0.69; N4 0.41.
Blends of N25 sub-books: K=2 1.19, K=3 1.22, K=4 1.23, K=6 1.24, K=12 1.25; CAGR 18.4 throughout; MaxDD -23.7 -> -23.5 (vs -24.5 single).
* **Q1 (GATED): FAIL.** At constant total names, three 8-name books (blend 0.81) and six 4-name books (0.56) are far below one 24-name book (1.09). Narrow sub-books are individually weak (0.69, 0.41); staggering does lift them (+0.12, +0.15) but cannot buy back the concentration. The names also overlap heavily across anchors (rank persistence), so sub-books are not independent name baskets.
* Q0 (descriptive): staggering N25 beats a single N25 by +0.10 (K=2) to +0.16 (K=12), positive in every group and both periods, MaxDD ~1 pt better, CAGR unchanged: a pure timing-diversification gain, saturating near K=4-6 (+0.14/+0.15).
* Q2 (descriptive): but buying breadth directly takes most of that: K=3 x N25 (1.22) vs single N75 (1.18): +0.04 (fail); K=6 x N25 (1.24) vs single N150 (1.15): +0.09 (pass). Breadth and staggering are substitutes; the best structure found is staggered N25 sub-books (1.23-1.24) vs single N25 (1.09), but it needs K accounts and 25K positions, and its edge over simply running ~75 names is ~+0.04-0.06.
* Note the breadth curve itself: single N25 1.09, N75 1.18, N150 1.15 - it flattens around 75, so the earlier "saturates 25-40" understated the plateau slightly.

## T2 Vol-based sizing (weights x clip(ref/x), reference = typical entrant, mean weight kept at ~1/N)
| | CAGR | Sh65 | dSh65 | P_A / P_B | anchors + | MaxDD |
|---|---|---|---|---|---|---|
| B | 18.83 | 1.13 | | | | -25.45 |
| VS1 ATR (0.5, 1.5) | 18.89 | 1.18 | +0.05 | +.05 / +.05 | 5/6 | -24.39 |
| VS2 ATR (0.33, 2.0) | 19.08 | 1.21 | +0.07 | +.05 / +.09 | 5/6 | -24.27 |
| VS3 stop-width (0.5, 1.5) | 18.56 | 1.14 | +0.01 | +.04 / -.01 | 4/6 | -24.45 |
| VS4 stop-width (0.33, 2.0) | 18.57 | 1.14 | +0.01 | +.04 / -.01 | 4/6 | -24.41 |
| WIDE stops (K 5, clip .15-.35) | 21.32 | 1.15 | +0.02 | +.02 / +.03 | 5/6 | -29.31 |
| VS2 + WIDE | 21.68 | 1.20 | +0.07 | +.03 / +.11 | 6/6 | -28.99 |
Inverse-ATR sizing is a consistent small improvement (both variants positive in both periods, ~1 pt less drawdown) that stops just short of the bar; equal-risk-per-stop sizing does nothing (stop widths are clipped to 10-25%, so they carry little information). Sizing does not make wide stops affordable: the combination still draws down ~29%.

## T3 Relative-strength information (stock vs equal-weight index) as exit input
Suppressing the trailing stops while RS is within 5% / 10% of its post-entry peak makes things worse (Sharpe -0.05 / -0.03, MaxDD -2.3 / -4.5): market-relative strength does not separate "noise" stops from real ones either.

## T4 Capacity (the most decision-relevant table in this round)
v2.4 baseline by book size (ADV cap 5% of 63-day median traded value, 25 names):
| capital | CAGR | Sh65 | P_A / P_B Sh65 | MaxDD | exposure |
|---|---|---|---|---|---|
| 1 lakh (shipped) | 18.8% | 1.13 | 1.42 / 0.90 | -25.5% | 51% |
| 1 cr | 13.9% | 0.86 | 0.97 / 0.79 | -18.4% | 39% |
| 5 cr | 11.2% | 0.70 | 0.74 / 0.68 | -12.5% | 29% |
| 20 cr | 9.3% | 0.57 | 0.60 / 0.55 | -9.2% | 21% |
**The performance in every earlier table is the small-book number.** From 1 lakh to 5 cr the strategy loses about 7.6 CAGR points; even in 2015-25 alone Sharpe falls 0.90 -> 0.68. Pre-2020 volume is thin so the early years overstate the loss, but the 2015-25 column says the same.
The capacity walk (candidates from rank <= 3N or 6N, skip names whose cap < 0.5/N) lifts exposure (39 -> 51% at 1 cr; 29 -> 47-50% at 5 cr) and CAGR (+0.9 to +1.9), but the extra names come from deeper in the ranking and the drawdown rises 9-16 pts, so Sharpe falls at every size (-0.06 to -0.12; 1 cr: 0.86 -> 0.79-0.80). The cash that the ADV cap leaves idle is acting as a risk buffer; filling it with rank 26-150 names is not free.

## T5 Weak-payoff regimes
No market-state variable predicts the top-25 payoff by the pre-set rule (|Spearman| >= 0.15, HAC |t| >= 3, same sign in both halves). Closest: 21-bar benchmark volatility percentile (rho -0.17, t -2.6, same sign both halves: top-25 pays less after high-vol periods) and breadth (t 2.4, positive); none of bench-above-SMA200, 126-bar market return, drawdown from high, dispersion is close. So the three weak blocks (2009-11, 2015-17, 2024-25) are not forecastable with these variables, and the conditional entry-scaling test was not run, as pre-registered.
Context: weak blocks are NOT bear markets. 2015-17 was a strong bull (88% of dates above the SMA200; EW market +26%/yr) with top-25 excess -0.6%; 2009-11 (+20%/yr) -0.2%; 2024-25 (+9%/yr) -0.4%. The best blocks include the 2006-08 crash (market -14%/yr, excess +5.4%) and 2018-20 (-6%/yr, +4.1%). The long-only top-25 earns its premium in choppy/falling markets and gives it up in broad rallies where the pool as a whole rises - a pattern consistent with a defensive quality-of-trend selection, but this was not tested here.

## What to take from three rounds of structural tests
* v2.4 is on a flat optimum: breadth plateaus near 25-75 names, stops/overlay set the risk level, rank-based and RS-based exits add nothing, capacity walks add risk, sizing adds ~+0.05-0.07.
* The remaining measurable items are small and mutually compatible but individually below the bar: inverse-ATR sizing (+0.05..+0.07, lower drawdown), panic percentile 0.90 (+0.04, MaxDD -3.8 pts better), staggered sub-books (+0.04..+0.15 depending on the breadth comparator), higher breadth (N75 +0.09 in this 12-anchor sample). A pre-registered PACKAGE test of these (post-look: it uses information from the results) would be the only legitimate way to see whether they add up; this has not been run.
* The decision that matters most is not a parameter: it is the capital the book will run at. The strategy's return drops from ~19% to ~11% between a lakh-scale and a ~5 crore book on this liquidity model.

## Limits
In-sample 2006-25, no lockbox; ~35 comparisons across this round (expect ~2 spurious single-gate passes); pre-2020 volume thin; stagger needs K sub-accounts; capacity results use a 5%-of-ADV rule, flat 0.3% costs and no market impact, so real large-book numbers are likely worse.
