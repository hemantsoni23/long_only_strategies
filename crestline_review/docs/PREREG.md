# Crestline v2.2 review - pre-registration (written 2026-10-12, BEFORE any variant was run)

Subject: `Crestine/crestline_v2_2.py` (colleague's strategy; never edited). Lab copy = `crestline_lab.py`, built by `make_lab.py` with exact-string patches; parity with the original is exact
(`review_parity.py`: identical equity curve, max abs diff 0.0). Only the baseline run on 2015-2025 had been seen when this was written.

## Accounting / window
* Crestline's own booking is kept (signal at close, fill at next open, stops checked on close and filled at next open, 0.3% one-way). Nothing is changed in the engine.
* Evaluation window 2006-01-01 -> 2025-12-31 (data starts 2000; the original 2015 start is also reported). Sub-periods: P_A = 2006-2014, P_B = 2015-2025.
* Idle cash earns 6.5% (liquid-fund sweep, as Zenith's `use_liquid_mf`) in all variants; `B` is the baseline under that same accounting. The cash-0% numbers for B are reported too.
  Gating metric = Sharpe vs rf 6.5%. rf=0 Sharpe, CAGR and MaxDD are shown alongside.
* Schedule luck: every variant runs at 6 anchor offsets {0,10,20,30,40,50} of the 60-bar schedule; all gates use means/counts over the 6 offsets.

## Single-change variants vs B (fixed list; nothing is added after seeing results)
| id | change |
|---|---|
| R1 | USE_SLOT_REFILL=True, REFILL_FREQ_DAYS=20, REFILL_COOLDOWN_DAYS=30 (the file's own settings) |
| R2 | slot refill, REFILL_FREQ_DAYS=10, REFILL_COOLDOWN_DAYS=20 |
| S1 | PEAK_STOP off (VOL-scaled + hard stay) |
| S2 | VOL-scaled stop off (PEAK 15% + hard stay) |
| S3 | PEAK off; VOLSTOP_K=4, min 15%, max 35% (wider) |
| S4 | all trailing stops off; TREND_BREAK on (SMA100, 3 closes); hard stop 20% stays |
| S5 | all trailing stops off (hard 20% + rank exits only) |
| C1/C2/C3 | REBALANCE_FREQ_DAYS = 30 / 40 / 90 |
| G1 | score = TP only (SCORE_W_HP=0) |
| G2 | score = HP only (SCORE_W_TP=0) |
| G3 | + 0.5 x residual momentum 12-1 (definition identical to `csm_resid_tilt`) |
| G4 | Low-MAX filter as live Zenith (drop top 20% by 21d max daily return) |
| G5 | universe liquidity ranks 301-1000 (UNIVERSE_TOP_N_MIN=301) - capacity-flagged |
| X1 | regime overlay off |
| X2 | no new entries while benchmark < SMA200 (BEAR_NO_ENTRY) |
| X3 | entry weight proportional to 1/ATR% (SIZE_BY_VOL) |
| X4 / X5 | TOP_N = 10 / 25 |
| X6 | EXIT_RANK_MULT = 3 |

21 single comparisons -> expect ~1 spurious pass at any single-gate level; the multi-part gate below is what counts.

## Gate for "carry forward" (all four on the 6-offset means, vs B)
* P1: mean Sharpe(rf 6.5%) improves by >= +0.10
* P2: improvement > 0 in BOTH P_A and P_B (mean over offsets)
* P3: improvement > 0 in >= 4 of the 6 offsets
* P4: mean MaxDD no worse than 3 points deeper than B
"Interesting, not carried" = P1 and P2 pass but P3 or P4 fails. Anything else = no evidence.

## Stack rule (fixed now)
Carried singles are ranked by mean dSharpe and added to a stack one at a time, in that order; an addition is kept only if the new stack passes P1-P4 against the PREVIOUS stack. Maximum 4 additions.
Final stack gets: cost stress (0.6% one-way), the P_A/P_B/2015-25 split, cash-0% accounting, correlation with faithful Zenith (`csm_value/output/faithful_engine_returns.csv`), and a stop-fill/slippage note.
Post-look changes to this list are not allowed; if one is made it is logged in the table below.

## Caveats stated in advance
* No lockbox exists. 2006-2025 is in-sample for every number here; only forward paper trading is out-of-sample.
* Survivorship (only 98 of 5,205 price files end before mid-2026) flatters everything; volume history before ~2020 is thin (liquidity ranks/ADV caps distorted).
* The colleague's parameters (stop widths, 60-bar cadence, 15 names) were probably tuned on 2015-2025, which biases against finding improvements on that window and toward finding them in 2006-2014.

## Post-look change log
* PL-1 (post-look #1 of max 2): TOP_N dose-response - TOP_N=40 alone and with G5, added after seeing TOP_N 10/15/25 move monotonically (X4 -0.19, X5 +0.16). Checks saturation only; it is not used to choose a winner unless the stack rule says so.
* Planned-but-unlisted ANALYSES (no change to any strategy spec): capacity check (INITIAL_CAPITAL 1 cr / 5 cr / 20 cr, because at the file's 1 lakh the 5%-of-ADV cap never binds), cost 0.6%, cash-0% accounting, original 2015-start window. Result note: X3 (inverse-vol sizing) is a NULL variant by construction - entry weights are capped at 1/TOP_N so equal weight is always binding; it is not evidence about vol-sizing.
* PL-2 (post-look #2 of 2, ENGINE CORRECTION not a strategy change): the vendor data holds ~680 unadjusted down-jumps (ratios cluster at 0.5/0.2/0.1 = bonus/splits) and ~230 up-jumps. v2.2 masks these cells for ranking but a position HELD through one books the split as a real loss
  (INNOVTEC -89%, CRSL -89%, AIRAN -81%, WAGEND -75% 'hard-stop' exits; 14 hard stops = -16% of total net P&L in the 2006-2025 baseline). Switch CA_ADJUST back-adjusts prices (and divides volume) at every flagged jump instead of masking.
  The ENTIRE fixed variant list above and the stack rule are re-run unchanged on the corrected engine; the corrected engine is the primary verdict, the uncorrected numbers are kept for reference. No post-look changes remain.
* PL-2b (engine correction, found by test 5 while building v2.3): the MIN_PRICE floor now uses as-traded (pre-adjustment) prices under CA_ADJUST, because back-adjustment uses future splits. All CA tables re-run; gate verdicts unchanged.
