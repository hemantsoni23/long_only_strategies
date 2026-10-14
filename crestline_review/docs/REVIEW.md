# Crestline v2.2 - review and improvement study (2026-10-12)

Subject: `Crestine/crestline_v2_2.py` (untouched). Protocol: `PREREG.md` (fixed before running; two logged post-look items). Code: `make_lab.py` -> `crestline_lab.py` (parity with the original is exact, zero difference),
`runner.py`, `gates.py`, `experiments*.py`. Raw results: `results_singles*.csv`, `results_stack*.csv`, per-run folders in `runs/`.

## 1. What the strategy is

* **Signal = live Zenith's composite**: z(close / 252d-high) + z(share of last 189 days above SMA50), universe = price > 20, liquidity rank 1-1000, <= 5 locked-circuit days in 63.
  Not in Crestline but in live Zenith: Low-MAX exclusion, absolute-momentum gate, Crash Guard, correlation guard, 15% vol target, rebalance-exit buffer, swap-gap.
* **Book**: top 15, equal weight 1/15 fixed at entry (never re-weighted), full rebalance every 60 bars (rank exit at 30), fills at next open, 0.3% per side.
* **Exits**: a stack of four close-based stops (hard 20% from entry, 15% from peak close, volatility-scaled 10-25% from peak close; ATR/RS/trend-break are off) filled at the next open. Slot refill is OFF, so a stopped slot stays empty until the next 60-bar rebalance.
* **Overlay** (benchmark < SMA200 -> x0.6, panic vol -> x0.3) scales **new entries only**; existing positions are never de-risked.
* Booking is honest (fill at open, stop exits at next open). It is NOT the engine-booked convention that inflates the live engines.

## 2. What the published headline hides

| | CAGR | Sharpe rf=0 | MaxDD |
|---|---|---|---|
| File as shipped (2015-25, anchor 0, cash 0%) | 14.4% | 1.34 | -16.0% |
| Same window, same settings, 6 schedule anchors (0,10..50): mean | **10.7%** | **0.98** | **-22.8%** |
| ... range over anchors | 5.9 - 14.4 | 0.58 - 1.34 | -16.0 - -29.3 |

The shipped number is the **best** of the six anchors. A single 60-bar schedule gives 46 rebalances; anchor luck alone moves Sharpe by about +-0.3. Starting in 2015 also hides 2008-09 (-28%) and 2022-23 (-26/-27% intra-year).
Exposure averages only 52% (9.1 of 15 slots) with cash at 0%; 10.7% is not a "50% invested" number you should multiply up.

Comparator: the faithful replay of live Zenith gives 2015-25 7.9% / Sharpe 0.63 / MaxDD -28.4% (11.5% / 0.92 / -28.4% for 2006-25), return correlation with Crestline 0.63. **Not like for like** (Zenith's stop-fill model is resting-stop; Crestline exits at next open), so "Crestline beats Zenith" is not supported by this study.

## 3. Defects and risks found in the file

1. **Unadjusted splits are booked as real losses (data x code).** The vendor files hold ~680 down-jumps (ratios cluster at 0.5 / 0.2 / 0.1 = bonus and splits) and ~230 up-jumps. The code masks them for ranking (`ca_flag`), but a *held* position still takes the loss: INNOVTEC -89%, CRSL -89%, RANDER -88%, AIRAN -81%, NYSSACORP -78%, WAGEND -75% "hard-stop" exits; 14 hard stops averaged -53% and equalled -16% of total net P&L (2006-25, anchor 0). Momentum buys recent winners, which are the names that split, so this is systematic.
   The bias is against the strategy: back-adjusting (switch `CA_ADJUST`) lifts 2006-25 from 15.6% / Sharpe65 0.79 to **17.5% / 0.95** (anchor mean). Live trading is not hurt (the broker adjusts); the backtest is. Every verdict below was run on both engines and is unchanged.
2. **Capacity is untestable at the shipped capital.** `INITIAL_CAPITAL = 100,000` so the 5%-of-ADV cap never binds; with capital the cap leaves slots unfilled instead of walking down the rank list (section 5).
3. **Overlay is entry-only.** A name bought in a bull stays at full weight through the next bear; the 0.6/0.3 tiers only act on flow. Removing the overlay still costs 11 MaxDD points (X1), so it is doing real work, but a de-risking overlay was not tested.
4. **Idle cash earns 0%.** Backtest cash is 48% of capital on average. At a 6.5% liquid-fund sweep the 2006-25 CAGR is 17.5% vs 14.2% (+3.3 pts). Live must actually sweep it.
5. Fills ignore locked circuits at the open (can't sell a lower-circuit name) and market impact; flat 0.3% only. 0.6% per side takes Sharpe65 from ~0.93 to 0.74 (baseline) - the book trades 270% one-way per year.
6. Pre-2020 volume history is thin, so ADV caps and liquidity ranks are distorted in the early years.

## 4. Where the edge is, and the exit/signal mismatch

* Rank IC rises with horizon: 0.049 (5d), 0.040 (20d), 0.086 (60d), **0.111 (120d, HAC t 5.3)**; 82% of rebalances positive at 60d. The signal is a slow one.
* The exits are fast: 2006-25 trades by holding period (anchor 0, original engine): <=30d 296 trades, 10% win, -9.7% avg, -1.39M P&L; 31-60d 229, 38%, 0%; 61-120d 282, 69.5%, +10.2%; **>120d 134, 91% win, +32.2% avg**, +1.53M. Median stop-out at 43-46 days.
* But the stops are a **risk dial, not an alpha leak**: widening or removing them adds 3-4 CAGR points and costs 12-20 MaxDD points with Sharpe flat or lower (S3/S4/S5). Slot refill: +2.8 CAGR, -8.5 MaxDD, Sharpe flat. There is no free lunch in the stop stack; the colleague can pick a point on the frontier but not escape it.

## 5. Pre-registered single-change results (split-corrected engine, as-traded price floor = primary; 6 anchors; 2006-25; cash 6.5%)

Baseline B: CAGR 17.5%, Sharpe65 0.95 (rf0 1.51), MaxDD -25.3%, exposure 51%. d = change vs B (Sharpe vs rf 6.5%); P_A/P_B = 2006-14 / 2015-25. (Re-run after the price-floor fix described in section 10; verdicts identical to the first corrected run.)

| id | change | CAGR | Sh65 | dSh65 | dP_A | dP_B | anchors + | MaxDD | verdict |
|---|---|---|---|---|---|---|---|---|---|
| G5 | universe ranks 301-1000 | 21.4 | 1.26 | +0.31 | +0.41 | +0.24 | 6/6 | -24.7 | **CARRY** |
| X5 | TOP_N 25 | 18.8 | 1.13 | +0.18 | +0.12 | +0.23 | 6/6 | -25.5 | **CARRY** |
| G3 | + 0.5 x residual momentum | 19.2 | 1.00 | +0.05 | -0.05 | +0.13 | 4/6 | -26.4 | no |
| R1 | slot refill 20d / cooldown 30 | 20.5 | 0.99 | +0.04 | +0.08 | +0.02 | 4/6 | -34.5 | no |
| C2 | full rebalance every 40 bars | 19.3 | 0.99 | +0.04 | -0.01 | +0.08 | 4/6 | -30.5 | no |
| S2 | drop VOL-scaled stop (keep 15% peak) | 19.9 | 0.99 | +0.04 | +0.08 | +0.02 | 5/6 | -29.9 | no |
| G4 | Low-MAX 20% (as live Zenith) | 17.4 | 0.98 | +0.03 | -0.00 | +0.05 | 4/6 | -27.4 | no |
| S3 | wider vol stop 15-35%, peak stop off | 21.1 | 0.98 | +0.03 | +0.09 | -0.01 | 4/6 | -37.8 | no |
| X6 | rank-exit multiple 3 | 17.4 | 0.95 | +0.00 | +0.02 | -0.01 | 5/6 | -25.3 | no |
| X3 | inverse-vol entry sizing (NULL: weights capped at 1/N) | 17.5 | 0.95 | +0.00 | -0.00 | +0.00 | 3/6 | -25.3 | null |
| S1 | drop 15% peak stop | 17.7 | 0.95 | -0.00 | +0.00 | -0.01 | 3/6 | -28.4 | no |
| X2 | no new entries in bear | 16.9 | 0.94 | -0.01 | +0.01 | -0.03 | 3/6 | -24.7 | no |
| S4 | trend-break exit instead of trailing | 20.8 | 0.92 | -0.03 | +0.02 | -0.07 | 3/6 | -38.8 | no |
| R2 | refill every 10d | 20.1 | 0.90 | -0.05 | +0.02 | -0.08 | 2/6 | -40.1 | no |
| X1 | overlay off | 18.0 | 0.89 | -0.06 | -0.12 | -0.01 | 2/6 | -36.6 | no |
| C1 | rebalance every 30 bars | 18.2 | 0.88 | -0.07 | -0.06 | -0.09 | 3/6 | -34.7 | no |
| C3 | rebalance every 90 bars | 15.2 | 0.87 | -0.08 | -0.10 | -0.08 | 2/6 | -23.4 | no |
| S5 | no trailing stops | 21.1 | 0.85 | -0.10 | -0.12 | -0.08 | 1/6 | -46.2 | no |
| G1 | score = trend persistence only | 16.4 | 0.85 | -0.10 | -0.14 | -0.06 | 1/6 | -27.8 | no |
| G2 | score = 52w-high proximity only | 15.4 | 0.81 | -0.14 | -0.24 | -0.07 | 2/6 | -23.3 | no |
| X4 | TOP_N 10 | 16.0 | 0.79 | -0.16 | -0.22 | -0.11 | 1/6 | -28.1 | no |

22 comparisons: roughly one spurious pass is expected at a single gate; two variants pass all four gates together, both with 6/6 anchors and both periods, both in directions that earlier work in this repo had already flagged (universe band 301-1000, `MASTER_RANKING.md` #4; breadth, `SECTOR_STRATEGY_FAILURE_ANALYSIS.md`).

**Breadth dose-response** (post-look #1, B universe): TOP_N 10 / 15 / 25 / 40 -> Sharpe65 0.79 / 0.95 / 1.13 / 1.19, CAGR 16.0 / 17.5 / 18.8 / 18.9, MaxDD -28.1 / -25.3 / -25.5 / -25.1. Monotone and saturating; with G5, 25 -> 40 adds nothing (1.34 -> 1.35).

**Stack rule** (pre-registered): G5 enters. X5 on top of G5 gives +0.08 Sharpe (< +0.10), 5/6 anchors, positive in both periods, MaxDD +0.4 -> **fails P1** (it passed on the first, uncorrected engine). Final stack = G5 alone; G5 + 25 names (ST2) is "interesting, not carried". G5 and X5 overlap: both buy breadth, so their gains are not additive.

**Capacity - the big caveat on G5.** The ADV cap never binds at 1 lakh. With capital (Sharpe65 / exposure; 3 anchors; 1 lakh row = 6-anchor mean):

| capital | B | G5 (301-1000) | ST2 (301-1000, 25 names) |
|---|---|---|---|
| 1 lakh (shipped) | 0.95 / 51% | 1.26 / 49% | 1.34 / 50% |
| 1 cr | 0.66 / 37% | 0.65 / 20% | 0.74 / 24% |
| 5 cr | 0.57 / 27% | 0.37 / 8% | 0.46 / 11% |
| 20 cr | 0.47 / 18% | 0.29 / 2% | 0.29 / 4% |

In 2015-25 alone (P_B) at 1 cr: B 0.65, G5 0.66, ST2 0.71 (vs 0.67 / 0.91 / 0.93 at 1 lakh). **The 301-1000 gain is a sub-1-crore effect; at 5 cr it is worse than the baseline.** Pre-2020 ADV is distorted (point 6 above), so the early-period collapse overstates the problem, but the P_B numbers say the same thing. Breadth (X5) was not separately capacity-tested. Cost stress, 0.6% per side (3 anchors): B 0.76, G5 1.06, ST2 1.17 - ranking unchanged.

## 6. Computed, not gated: staggering the schedule

Equal-weight blend of the six anchor books (six sub-accounts at 1/6 capital; no new parameters), `anchor_report.py`, 2006-25, cash 6.5%:

| | single anchor (mean) Sharpe65 / MaxDD | 6-anchor blend Sharpe65 / MaxDD | blend CAGR |
|---|---|---|---|
| B | 0.95 / -25.3 | **1.09 / -24.1** | 17.3 |
| G5 | 1.26 / -24.7 | **1.47 / -20.5** | 21.2 |
| G5 + 25 names | 1.34 / -24.3 | **1.52 / -21.2** | 21.1 |

+0.14 to +0.21 Sharpe and 1-4 pts less drawdown from timing diversification alone. It is partly just more names (up to ~90 positions), so it is not separable from breadth; it was not gated. (An earlier draft quoted +0.17 to +0.25 from the pre-floor-fix runs.)

## 7. Recommended changes, in order

1. **Make the backtest honest first**: back-adjust corporate-action jumps (or use adjusted data); report results as a distribution over schedule anchors, not anchor 0; show 2006-25 not just 2015-25. Expect ~+1.9 CAGR points and a less lucky headline (10.7% / 0.98 / -22.8% on the colleague's own window, 2015-25).
2. **Stagger the entries** (3-6 tranches offset in time) - biggest measured gain, no new parameters.
3. **Widen to 25 names** (gate-passing, 6/6 anchors, saturates by 25-40).
4. **Sweep idle cash** to a liquid fund (+3.4 pts in backtest terms).
5. **Use the 301-1000 universe only if the book is below ~1 crore**; decide capital first. For larger books the next step is a capacity-aware candidate walk (see 8), not a universe change.
6. Choose the risk point deliberately: refill / wider stops buy ~+3 CAGR for ~9-12 MaxDD points at flat Sharpe. Keep the regime overlay.
7. Do not spend time on: residual-momentum tilt, Low-MAX, faster/slower cadence, single-leg scores, no-entry-in-bear, 10 names.

## 8. Untested ideas (need their own pre-registration)

* Capacity-aware sizing that skips names whose ADV cap is below the minimum ticket and takes the next-ranked name (essential once capital > 1 cr).
* De-risking overlay for existing positions (vol target on the held book, as live Zenith's 15%) instead of entry-only scaling.
* Asymmetric stops: tight in the first ~30 days (10% win-rate bucket) and wider after (trades > 120 days earn +32%).
* Locked-circuit-aware exits and an impact-cost model; 0.3% flat is optimistic at size.

## 9. Limits (state with every number)

No lockbox: 2006-25 is in-sample for everything above; the colleague's parameters were probably tuned on 2015-25. 22 variants tested at one setting each. Survivorship (98 of 5,205 files end before mid-2026). Pre-2020 volume is thin. Back-adjusting also erases any *real* one-day crash > 40% (rare in liquid names). Certainty is not available; only forward paper trading is out-of-sample.

## 10. The fixed baseline (v2.3) - added after the review

`crestline_v2_3.py` (built by `make_lab.py` + `make_v2_3.py`; the colleague's file is untouched) = v2.2 logic + only correctness/realism fixes: split-neutral positions (`CA_ADJUST`), 6.5% idle-cash sweep, 2006 start, `anchor_report.py` for honest reporting; dead `SIZE_BY_VOL` removed. Tests: `test_v2_3.py` (6 checks, all pass): (1) fixes off = v2.2 bit-for-bit (equity and trade log), (2-3) no split-sized trade losses and hard-stop losses are stop-sized after the fix (masked: 6 trades < -60%, avg hard stop -52.9%; adjusted: 0 and -24.5%), (4) defaults = the lab engine used in the study, (5) truncating the sample leaves earlier equity unchanged.
**Bug caught while building it:** the first CA_ADJUST version let the Rs 20 price floor see split-reduced historical prices (back-adjustment uses future splits) - a mild look-ahead that test 5 caught. The floor now uses as-traded (pre-adjustment) prices; remaining truncation difference <= 6e-9 (float noise). All corrected-engine tables in this file were re-run after that fix; no gate verdict changed (largest mean-Sharpe move 0.09, G2).

Fixed-baseline reference (2006-25, cash 6.5%, `anchor_report_v2_3.txt`): per-anchor CAGR 15.7-19.4%, Sharpe65 0.80-1.14, MaxDD -21.1 to -28.8%; mean 17.5% / 0.95 / -25.3%; 6-anchor blend 17.3% / 1.09 / -24.1%. Colleague's window (2015-25, cash 0%): mean 11.6% / Sharpe0 1.05 / MaxDD -23.2% (anchor 0 alone, now split-neutral: 15.1% / 1.39 / -16.0%).

Still NOT fixed (deliberately, unchanged v2.2 behaviour; each is an improvement to pre-register): capacity-aware sizing, locked-circuit / impact fills, entry-only overlay.
