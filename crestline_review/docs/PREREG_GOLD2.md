# Gold / silver adoption under conservative accounting - pre-registration (written 2026-10-13, BEFORE any number of this round)

Instruction (user): do not credit idle cash with 6.5% while developing the strategy - it inflates results. Gold/silver ETFs must be ADAPTED as the way idle capital is deployed.
Consequence: new primary accounting = idle cash earns **0%**, metric = **Sharpe with rf = 0 (Sh0)**, plus CAGR, MaxDD, Calmar. The previous gold round (PREREG_GOLD.md, liquid-fund baseline) is superseded for decisions; it is kept as context. Its results informed the variant list below (post-look - stated openly): the earlier round showed trend gating deepens drawdowns, bear-only gold is unstable, a 10% cap is neutral.
Base = `crestline_v2_4.py` with CASH_RATE_ANNUAL = 0, 6 anchors, 2006-25, book sizes 1 lakh / 1 cr / 5 cr / 20 cr (idle share ~49 / 61 / 71 / 79% - recomputed at 0%). G0' = all idle cash earns 0%.

## Honesty about gold's return (the new danger)
Against a 0% baseline almost any gold holding looks good, and gold's usable sample (2007-10, 2015-25) returned ~17%/yr in INR. So every sleeve variant is evaluated under gold-return scenarios, set by re-centring the daily gold/silver return series to a target annual return R* over the usable days (shape and correlation unchanged):
REAL (sample, no change) | FULL-HISTORY (gold's 2007-03 -> 2025-12 point-to-point CAGR, which includes the unobserved 2011-14 years; computed from the data) | **8%** (the planning scenario: ~half of the real sample, a haircut for a one-bull-market sample) | 4% | 0%.
Silver uses the same target R* (it is more volatile and has only 3.9 years of data, so a target is safer than its 35% sample).
**All gates below are evaluated under the 8% planning scenario; REAL numbers are reported for reference only and never gate.** A break-even table (the lowest R* at which each variant still beats G0') is reported.

## Sleeve mechanics (as in PREREG_GOLD.md, exact post-processing of the engine's daily output - same engine, only the cash rate changes)
Weight in a metal at day t = idle fraction at the close of t-1 x multiplier m_t (signals use data to the close of t-1); remaining idle cash earns 0%; 2% dead band; cost 0.15% one way (stress 0.30%); forced down immediately if idle falls below the held weight; zero in the 2011-14 gap and for 200 valid days after any gap; no forward fill.
Signals: S_sma = ETF close > its 200-day SMA; S_per = share of the last 126 days above the 50-day SMA >= 0.5 (windows touching missing data are invalid).
| id | rule |
|---|---|
| H1 | all idle cash in gold, no timing (m = 1) |
| H2 | half of idle cash in gold, no timing (m = 0.5) |
| H3 | gold, m = S_sma |
| H4 | gold, m = S_per |
| H5 | gold, m = S_sma x (1.0 if engine regime BEAR or PANIC else 0.5) (more gold in bad regimes) |
| H6 | gold + silver: from the date silver is valid, each metal gets idle x 0.5 x its own S_sma; before that gold gets idle x S_sma |
| H7 | gold, m = S_sma, total gold capped at 10% of equity |
Silver alone (2022-02..2025) is reported descriptively.

## Gates (per book size, vs G0' at the same size, under the 8% scenario)
* K1 dSh0 >= +0.08; K2 dSh0 > 0 in BOTH periods (P_A = 2006-14, effective 2007-10; P_B = 2015-25); K3 > 0 in >= 5 of 6 anchors; K4 mean MaxDD no more than 3 pts worse than G0'; K5 at R* = 4%: dSh0 > 0; K6 at 0.30% cost: dSh0 >= +0.05.
Selection: among variants passing K1-K6 at the most book sizes (at least 3 of 4), choose the highest mean dSh0 at 8%; ties -> lower turnover. If none passes at >= 3 sizes, the gold sleeve is NOT adopted as specified and the fallback is reported. No parameter is tuned after seeing results.

## Phase 2 (only for the selected rule): native engine implementation (`crestline_v2_5.py`: the sleeve trades inside the engine loop, funded by idle cash, ETF sold at the open to fund stock entries) with a parity test against this post-processing (daily returns correlation >= 0.999 and CAGR within 0.3 pt), then the same robustness set: cost x2, 2015-25 alone, staggered blend, scenario table 0/4/8/full-history/real.

## Re-check of earlier decisions under cash 0%
Only an information item (no re-opening): v2.4's TOP_N=25 versus 15 at cash 0% and the baseline anchor distribution, plus the 0%-cash headline numbers that replace the 6.5% ones in every summary from now on.

## Caveats stated in advance
One gold bull market in the data; 2011-14 unobserved; silver 3.9 years; ~28 sleeve cells; taxes on ETF churn not modelled; capacity: a 20 cr book puts Rs ~16 cr in gold - it must be spread over GOLDBEES / GOLDIETF / SETFGOLD / HDFCGOLD (~Rs 12-65 cr/day each); in-sample, no lockbox.

## Post-look change log
* Outcome of the 7-variant round (gates K1-K6 at the 8% scenario): NO variant passed at any book size. Large weights (H1, H3-H6: 20-54% of equity) add +2.0..+3.8 CAGR pts but lower Sh0 by 0.07-0.20 and deepen MaxDD; H2 (half of idle) and H7 (10% cap) are positive (+0.03..+0.06 Sh0, Calmar +0.03..+0.09) but under the +0.08 bar. The gates are NOT loosened. My text said the fallback would be "reported" without defining it; the user's standing instruction is to adopt gold/silver ETFs, so the fallback is the POST-LOOK #1 sizing study below.
* POST-LOOK #1 (fixed now, before running): the weight is the decision, timing was already shown not to help. Grid of total metal weight caps w (share of equity) {2.5, 5, 7.5, 10, 15, 20, 25, 30, 40, 100}% , UNTIMED: metal weight = min(idle fraction at the previous close, w); same mechanics/costs; scenarios 4% / 8% / FULL / REAL; four book sizes, 6 anchors.
  Recommended weight w* = the LARGEST w such that, at ALL four book sizes under the 8% scenario: dSh0 >= 0, dCalmar >= 0, dMaxDD >= -3 pts, dSh0 > 0 in both periods; AND under the 4% scenario dSh0 >= -0.03 (limited harm if gold disappoints). If no w qualifies, no sleeve is recommended.
  At w*, three comparisons (descriptive + one gate): (a) trend-gated version (m = S_sma, same cap) vs untimed; (b) bear-tilted version (cap 2w* in BEAR/PANIC, w*/2 otherwise) vs untimed - gate for keeping the tilt: dSh0 >= +0.03 vs untimed, both periods positive, >= 5/6 anchors; (c) gold-only vs 50/50 gold/silver split from silver availability (descriptive).
  This is a documented selection rule, NOT a pass of K1-K6, and must be described that way.
* Phase 2 outcome: native `crestline_v2_5.py` built for the post-look rule output (untimed, w* = 25%). Parity vs post-processing: daily corr 0.9993-0.9995 and CAGR within -0.06..+0.18 pt - inside the pre-registered bars - but ONLY after two fixes found by tests: (1) scenario re-centring made arithmetic like the post-processing; (2) ETF fills moved from the open to the previous close because the vendor's ETF opening prints are biased (GOLDBEES overnight +109%/yr, intraday -87%/yr; open fills showed +0.4..+0.6 CAGR that did not exist). Fixes (1)-(2) were made before any v2.5 headline number was recorded.
* Cap choice: the pre-registered rule says 25%; the analyst's after-the-fact recommendation is 20% (not part of the rule).
