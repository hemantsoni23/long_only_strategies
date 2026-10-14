# Crestline core signal over time + holding-period diagnosis (2026-10-12)

Definitions fixed in `PREREG_DIAG.md` before any number was computed (one logged definition fix: hold-H horizons 90 -> 100 and 252 -> 240 so H is a multiple of 20 bars).
Code: `crestline_diag.py` (dump), `diag_signal.py`, `diag_hold.py`, `diag_portfolio.py`; outputs `diag_*.csv`, `diag_*_out.txt`, `diag_signal_over_time.png`.
Signal = v2.4's core score on the strategy's own ranking pool, 993 dates on a 5-bar grid, 2006-03..2025-12, forward return from the next open (the strategy's fill), gross of cost. HAC lag = ceil(h/5).

## PART 1 - does the core idea work over time?
**Verdict by the pre-registered rule: WORKING, not decaying.** h=120: 6 of 7 blocks WORKING (IC>0 and t>=2), none broken; h=60: 5 of 7, none broken; IC in the last two full blocks is 99% (h=120) and 89% (h=60) of the first two.

All-sample IC curve (score vs forward return):
| h (bars) | 5 | 10 | 20 | 40 | 60 | 90 | 120 | 180 | 252 |
|---|---|---|---|---|---|---|---|---|---|
| mean IC | .049 | .060 | .073 | .092 | .107 | .117 | .124 | **.125** | .115 |
| ICIR | .36 | .39 | .45 | .59 | .71 | .80 | .84 | **.86** | .83 |
| hit (IC>0) | 68% | 70% | 73% | 77% | 81% | 82% | 83% | 84% | 84% |
| HAC t | 10.7 | 9.1 | 8.1 | 8.0 | 8.0 | 7.3 | 6.6 | 5.6 | 4.8 |
IC and ICIR keep rising to ~120-180 bars (the rank signal is slow), while the t-stat falls with horizon only because fewer independent observations remain.

By 3-year block (signal date), mean IC / HAC t:
| block | h=20 | h=60 | h=120 | h=252 | verdict 60 / 120 |
|---|---|---|---|---|---|
| 2006-03..08 | .098 / 4.3 | .140 / 5.4 | .132 / 4.2 | .082 / 2.5 | W / W |
| 2009..11 | .080 / 2.7 | .103 / 1.9 | .135 / 1.8 | .150 / 1.7 | weak / weak |
| 2012..14 | .100 / 4.3 | .145 / 3.9 | .152 / 2.9 | .151 / 2.5 | W / W |
| 2015..17 | .043 / 2.9 | .068 / 3.5 | .082 / 3.8 | .081 / 2.7 | W / W |
| 2018..20 | .076 / 2.6 | .115 / 2.9 | .135 / 2.5 | .113 / 1.6 | W / W |
| 2021..23 | .060 / 4.4 | .102 / 8.0 | .128 / 8.9 | .113 / 4.1 | W / W |
| 2024..25 (partial) | .045 / 2.2 | .054 / 1.9 | .082 / 2.6 | .121 / 8.9 | weak / W |
Rolling 3-year windows (17) never go negative at 20/60/120 bars; the weakest are 2007-09 and 2020-22 starts (60-bar IC .06-.08) and the strongest 2010 (.18-.23). Both legs behave the same way (HP slightly stronger than TP at 60 bars in 6 of 7 blocks; 2021-23 the exception).

**The catch for a long-only book - the top of the ranking pays less reliably than the IC suggests.** Top-25 excess return vs the pool mean (mean, % per holding period):
| block | h=20 | h=60 | h=120 | top-decile at 60 | long-short decile spread at 60 |
|---|---|---|---|---|---|
| 2006-03..08 | +1.9 | +5.4 | +4.5 | +4.7 | 10.5 |
| 2009..11 | +0.1 | **-0.2** | +1.3 | -0.3 | 0.0 |
| 2012..14 | +1.6 | +3.7 | +4.3 | +3.7 | 7.0 |
| 2015..17 | -0.2 | **-0.6** | **-1.9** | -0.1 | 3.2 |
| 2018..20 | +1.5 | +4.1 | +5.7 | +4.2 | 5.8 |
| 2021..23 | +0.8 | +2.5 | +4.1 | +2.1 | 6.5 |
| 2024..25 | -0.2 | **-0.3** | +1.5 | +0.1 | 3.1 |
In three of seven blocks (2009-11, 2015-17, 2024-25) the IC stays positive and the long-short spread stays positive, but the top-25 / top-decile earns about zero excess over the pool: the rank edge sits in the bottom of the ranking (names to avoid), which a long-only book cannot harvest. All-sample top-25 excess: +0.8% (20 bars, t 3.3), +2.2% (60, t 2.9), +2.9% (120, t 1.8), +2.1% (180, t 0.9), +0.4% (252, t 0.1). The 25-name payoff is regime-dependent even though the signal is not.

**The top basket's excess is front-loaded** (all-sample, a FIXED basket from the signal date): marginal excess per period: 0-20 bars +0.84, 20-40 +0.73, 40-60 +0.66, 60-90 +0.37, 90-120 +0.27, **120-180 -0.79, 180-252 -1.70**. 78% of the 120-bar excess is earned in the first 60 bars; beyond ~120 bars a static basket gives it back. Fresh picks beat old picks after about 4-6 months.

## PART 2 - holding period versus the signal horizon
You were right that the holding is far shorter than the horizon where the signal pays (IC peaks 120-180 bars):
* v2.4 trades (8,939 across six anchors): **median hold 35 trading days, mean 48, capital-weighted 42**; 54% of trades end before 40 days, 70% before 60, only 8% last 120+ days. Volatility stops average 45 days (median 32); rebalance exits 86.
* **Winners are cut.** 24% of entries would have returned > +30% over 120 bars with no stops. Of those, 54% were stopped out before day 60 and 82% before day 120; they realised +30% on average versus +66% held through (**46% captured**). Across trades whose peak gain reached +30%, the exit kept 58% of the peak. The top 10% of trades produce 171% of total net P&L (the rest net negative), so the right tail is the strategy.
* **The stop exits are mostly against the signal's own view.** At the last grid date before a stop exit, 49% of stopped names were still ranked top-25 and 73% top-50. Post-exit excess return vs the pool (exit open -> +K bars): still top-25: +3.5% / +3.5% / +3.1% at K=20/60/120; rank 26-50: +2.4 / +2.2 / +1.1; no longer ranked: -1.0 / -0.4 / -0.9. By exit reason: vol-scaled stop +2.4 / +2.8 / +3.5; peak stop +3.0 / +2.4 / -0.1; rank exit +0.6 / +0.5 / -1.1 (rank exits are about right; the trailing stops exit names that keep outperforming). Some of that is ordinary momentum premium (a fresh top-25 earns +0.8 / +2.2 / +2.9), and the pooled sample overlaps heavily across anchors, so read these as direction, not precision.

**But simply holding longer is not the fix.**
* Return per day invested is already higher WITH the stops: 0.13% per held day vs 0.08 / 0.10 / 0.10% for holding the same entries 20 / 60 / 120 bars with no stops. The stops kill losers early; the drag is that only ~51% of capital is invested at any time (no refill).
* Pure-signal portfolios (top-25, staggered, NO stops, 0.3% costs, window 2006-12..2025): Sharpe vs 6.5% by hold length 20 / 40 / 60 / 100 / 120 / 180 / 240 bars = 0.48 / 0.67 / **0.75** / 0.73 / **0.75** / 0.66 / 0.62; bear-gated (cash when the benchmark is below its SMA200): 0.67 / 0.75 / **0.88** / 0.82 / 0.84 / 0.74 / 0.60. **60-120 bars is the best hold, confirming your reading - but every one of these books has a 46-72% maximum drawdown.** The actual v2.4 (stops + overlay) on the same window: mean of anchors CAGR 17.9%, Sharpe 1.06, MaxDD -25%; staggered six-anchor blend 18.0%, **1.22**, -25% - better risk-adjusted than every pure hold.
* Within the stop family, longer holds buy return with drawdown (TOP_N=15 grid): average hold 37 days -> CAGR 16.0% / Sharpe 0.90 / MaxDD -21%; 41 days (base) -> 17.5 / 0.95 / -25; 55-57 days -> 19.9 / 0.99-1.00 / -30; 90 days (no stops) -> 21.2 / 0.80 / -55.
So the lost money is real (the winner capture numbers), but a blunt wider stop pays for it with drawdown at flat Sharpe. The evidence points to a **discriminating exit**: keep names the signal still ranks highly through ordinary pullbacks, still exit on rank loss or a real breakdown.

## Candidate next-round tests (each needs its own pre-registration; none is run or adopted here)
1. **Signal-aware stop**: suppress or widen the trailing stop while the name's rank is still <= N (or <= 2N); keep the hard breakdown exit.
2. **Immediate re-entry / refill with the same name** when a stopped name is still top-N after a short cooldown (the post-exit +3.5% for still-top-25 names is the prize).
3. **Time- or profit-asymmetric stop width**: tight at entry, wider once the position is up (winners' MFE is 64% on average).
4. **Refill + capacity-aware sizing** so the 49% idle capital works (earlier test: refill +2.8 CAGR, Sharpe flat, MaxDD -8.5 - the signal-aware exit should be tested with and without it).
5. **Bear/low-payoff regime handling for the long-only tail**: the three blocks where the top-25 earned ~0 are the drawdown periods to study (2009-11, 2015-17, 2024-25).

## Limits
In-sample throughout; counterfactuals assume entries as the strategy made them; pool-mean excess is equal-weighted; pre-2020 volume is thin; the last block is partial (long horizons truncated); pooled-anchor trade statistics overlap heavily; certainty is not available - only forward paper trading is out-of-sample.
