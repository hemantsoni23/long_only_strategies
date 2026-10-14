# Next-round exit / re-entry tests on v2.4 (2026-10-12)

Protocol `PREREG_EXITS.md` (fixed before running). Code `make_exits_lab.py` -> `crestline_exits_lab.py` (all switches off == v2.4, bit-exact; monitor grid alone also exact; `test_exits_lab.py` 8/8 pass, incl. truncation/no-look-ahead with the new mechanisms on), `experiments_exits.py`, `exits_report.py`, `exits_rf.py`. Raw: `results_exits*.csv`, `exits_table.csv`.
13 variants x 6 anchors, 2006-25, cash 6.5%. Base B = v2.4: CAGR 18.83%, Sharpe vs 6.5% 1.13, MaxDD -25.45%, exposure 51%, mean hold 70 calendar days, winner capture 58% of MFE.

## Result: nothing passes. All rank-aware / profit-aware exits are risk-dial moves.
| variant | change | CAGR (d) | Sh65 (d) | P_A / P_B | anchors + | MaxDD (d) | mean hold | capture of MFE | verdict |
|---|---|---|---|---|---|---|---|---|---|
| SA1 | suppress trailing stops while rank <= 25; cata 25% | 20.6 (+1.7) | 1.15 (+0.02) | +.08 / -.04 | 4/6 | -30.1 (-4.6) | 89 d | 57% | risk-dial |
| SA2 | rank <= 50; cata 25% | 21.8 (+3.0) | 1.16 (+0.03) | +.04 / +.01 | 4/6 | -32.9 (-7.4) | 104 d | 56% | risk-dial |
| SA3 | rank <= 25; cata 35% | 20.3 (+1.5) | 1.12 (-0.01) | +.07 / -.07 | 3/6 | -30.2 (-4.7) | 90 d | 57% | risk-dial |
| SA4 | rank <= 50; cata 35% | 21.7 (+2.9) | 1.13 (0.00) | +.02 / -.03 | 3/6 | -34.1 (-8.7) | 106 d | 56% | risk-dial |
| RE1 | re-buy stopped names, rank <= 25, cooldown 5 | 19.0 (+0.2) | 1.02 (-0.12) | -.08 / -.14 | 0/6 | -34.4 (-8.9) | 68 d | 57% | worse |
| RE2 | cooldown 10 | 19.7 (+0.9) | 1.09 (-0.04) | .00 / -.08 | 1/6 | -32.0 (-6.6) | 69 d | 58% | worse |
| RE3 | rank <= 50, cooldown 10 | 19.6 (+0.7) | 1.03 (-0.11) | -.03 / -.16 | 0/6 | -37.3 (-11.9) | 66 d | 58% | worse |
| PW1 | widen x1.5 once +15% | 21.3 (+2.5) | 1.18 (+0.04) | +.12 / -.02 | 6/6 | -30.4 (-5.0) | 88 d | 56% | risk-dial |
| PW2 | x2.0 once +15% | 22.2 (+3.4) | 1.15 (+0.02) | +.09 / -.04 | 4/6 | -33.7 (-8.3) | 99 d | 55% | risk-dial |
| PW3 | x1.5 once +30% | 20.7 (+1.9) | 1.18 (+0.05) | +.10 / .00 | 6/6 | -28.9 (-3.4) | 80 d | 56% | risk-dial (closest) |
| PW4 | x2.0 once +30% | 21.8 (+2.9) | 1.18 (+0.05) | +.08 / +.03 | 5/6 | -31.9 (-6.4) | 86 d | 56% | risk-dial |
| PN1 | PANIC_PCTL 0.90 | 19.0 (+0.1) | 1.18 (+0.04) | +.11 / .00 | 5/6 | -21.7 (+3.8) | 70 d | 58% | below the +0.08 bar |
| RF | + slot refill (20d, cooldown 30) | 22.5 (+3.6) | 1.19 (+0.05) | +.14 / -.01 | 4/6 | -34.0 (-8.5) | - | - | fails (MaxDD) |
Adoption rule needed dSh65 >= +0.08, both periods positive, >= 5/6 anchors, MaxDD within 3 pts, a mechanism check, and family consistency. No variant reaches +0.08; none of the SA/PW variants also meets the MaxDD limit with the anchor count.

## What this tells us
1. **The mechanism worked, the payoff did not.** SA and PW do what they were built to do: mean hold 70 -> 80-106 days, CAGR +1.5 to +3.4 pts. But MaxDD worsens by 3.4-8.7 pts, Sharpe moves at most +0.05, and the capture ratio (realised / peak gain) does NOT improve (58% -> 55-57%) because a longer hold also gives back more from a higher peak. Every one of these sits on the same return-vs-drawdown line as plain wider stops: +0.3 to +0.56 CAGR points per MaxDD point (SA 0.32-0.40, PW 0.41-0.56, refill 0.43, wider vol stop 0.53). **There is no discriminating exit in this signal's rank.**
2. **Why the rank does not discriminate.** The score is a slow function of price (proximity to the 252-day high, share of 189 days above SMA50). A name that has fallen 10-15% from its peak is usually still ranked top-25, so "still top-25" is mostly a statement that the stock is still a winner. Post-exit 60-bar excess for stop-exited names: top-25 group mean +3.5% (median +2.9%) vs +1.8-2.2% for lower ranks, but the downside tails are the same: 10th percentile -23.5% vs -21%, 18% fall a further 15%+ vs the pool (16-18% for lower ranks). Rank buys a little more upside, not less downside, so keeping the position through the stop keeps both.
3. **Immediate re-entry loses** (Sharpe -0.04 to -0.12, MaxDD -6.5 to -12): buying back 5-10 bars after a stop catches the same two-sided distribution again, plus costs. The +3.5% average rebound is not a tradable edge at stop-exit timing.
4. **Refill still does not help** with 25 names (+3.6 CAGR, Sharpe +0.05, MaxDD -8.5): the idle 49% of capital is not free money.
5. **The only variant that moved risk-adjusted quality is the one that cuts risk**: PANIC_PCTL 0.90 (volatility-percentile trigger for the 0.3x panic scaling): Sharpe +0.04, MaxDD -25.5 -> -21.7, Calmar 0.74 -> 0.87, 5/6 anchors, P_A +0.11, P_B 0.00. It missed the pre-set bar twice (ablation and here, same +0.04), so it is a replicated near-miss, not an adoption. A loosened bar would have to be pre-registered separately.

## Conclusion for the holding-period question
The evidence now says the short holds are largely the price of the drawdown control, not an exit-design mistake that a signal filter can fix: a fixed top-25 basket stops adding excess after ~120 bars, longer-holding stop variants buy return with proportional drawdown, and the rank carries no downside information at the point of the stop. Remaining routes to capture more of the winners must come from outside the exit rule:
* diversification in time (staggered tranches, measured earlier at +0.14 to +0.21 Sharpe and 1-4 pts less drawdown), which lets the same stops run with a smoother portfolio;
* a different information source for exits (e.g. relative strength vs the benchmark/industry, volume, earnings-event timing) rather than the entry score itself;
* position-level risk sizing (smaller weight in higher-vol names) so wider stops cost less drawdown.
None of these is tested yet.

## Limits
In-sample 2006-25, no lockbox, capacity-free at 1 lakh; 13 variants compared; the monitor grid is 5 bars so ranks are up to 4 bars stale at a decision; risk-dial efficiency numbers are descriptive.
