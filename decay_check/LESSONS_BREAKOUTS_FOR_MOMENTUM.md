# What the momentum books can learn from the breakout books (HR breakout, VCP)

Written 2026-10-19. Evidence: Notion page "Strategy Decay Check — All 8 Live Strategies (Oct 2026)" (sections 3, 4, 9), code and tables in this folder (`results/`, `PREREG.md` Addenda 2 and 3).
Everything marked **TESTED** has a result in `results/`; everything marked **HYPOTHESIS** has not been tested and needs its own pre-registered test before it goes near live capital.

## 0. Read this first: breakouts are "not decayed", not "good"

- Booked faithfully (positions drift, exit day charged, 0.3% per leg, exposure at most 100%), HR breakout makes **14.8%** and VCP **15.4%** CAGR over 2008-26 (Nifty 500 price index 10.4%). Their own engines say about 42-43%. The engine numbers are not usable. Excess over the index is not statistically significant for either (NW-t 0.8 and 0.7).
- HR's latest 3 years: +22.9% (its best chunk). VCP's: +10.7% (down from 25.4%). Both have had dead chunks (2017-20: HR +2.5%, VCP -3.9%, max drawdown about -44% HR, -33% VCP).
- Capacity is small: capping each position at 5% of 63-day rupee volume cuts HR to about 8% and VCP to about 5% from a Rs 1 crore start. Dropping the 25 biggest winners cuts both to about 11%.
- So the lesson is not "copy the breakout books". It is "copy the specific pieces that the ablations show carry the result, and test them on the momentum books".

## 1. Why they behave differently from the momentum books (TESTED)

| Item | Breakout books | Momentum books | Evidence |
|---|---|---|---|
| What is ranked | Price location: fresh break above a resistance cluster or tight base, near the 52-week high, with an RS filter | Vol-scaled return momentum (Absolute, Batch, Quad); 52w-high + trend persistence (Zenith, Elendel) | 3m IC on a common pool: raw 12-1m return +0.021, vol-scaled 12-1m +0.045, 52w-high proximity +0.078, residual R3b +0.083 |
| When it buys | At the break (entry timing is part of the signal) | Month-end rank, can be days or weeks after the move | HR with the pattern removed: 14.8% -> 3.8% CAGR (ablation) |
| Market regime | HR: benchmark SMA-50 streak filter. VCP: same | Crash guard, vol target, bear leverage | HR without regime filter: 14.8% -> 7.9%. VCP without it: 15.4% -> **18.3%** (the filter hurts VCP) |
| Trend gate | EMA 50/150/200 alignment, 52w band, RS top 25% (HR); Minervini template (VCP) | SMA-200 and absolute-momentum gate | HR without trend gate: 14.8% -> 8.6%. VCP: 15.4% -> 12.4% |
| Exits | Chandelier / trailing stop, hard -15%, time stop (HR 45d if below -5%), stale exit (VCP 60d if below +5%) | Rank-decay exits, hard stops, crash guard | Not separately tested (see section 3, E4) |
| Sizing | Risk-based: weight = 1% / stop distance, clamped 2%-15% (HR), 2%-20% (VCP) | Inverse-vol, 5% cap, vol target | Not separately tested (see section 3, E5) |

Where the momentum books lost their edge (TESTED, same diagnostics): the decay is concentrated in the high-volatility and least-liquid names, high market-volatility months wipe out IC for Absolute and Batch, V-shaped rebound months hurt Residual/Zenith/Elendel, and the top-quintile spread shrank from about +1.3% to +2.4% per 3 months before 2020 to +0.2% to +0.9% now.

## 2. Transplant candidates, ranked by evidence

### T1. Move the ranking toward price location and residual momentum (TESTED, strongest)
- Add the residual-momentum composite R3b (market-beta-removed 9m momentum + 52w-high proximity) to the Absolute, Batch, Elendel (and test Zenith) ranking.
- Result (top-N basket excess per 3 months, full history | latest 6 years): Absolute 1.24% | 0.59% -> 2.25% | 1.88%; Batch 1.02% | -0.30% -> 2.09% | 1.22%; Elendel 2.02% | 2.66% -> 3.02% | 3.01%. Passes the pre-registered rule for Absolute, Batch, Elendel; Zenith fails one criterion (latest-6-year IC), Quad is not rescued.
- Why it plausibly works: it is the same idea the breakouts use (where is the stock relative to its own recent range, net of market move), and it stays positive in illiquid names where raw momentum went to zero.
- Caveat: in-sample, same history used to pick the candidate, and all four wins share the R3b ingredient. Needs a forward paper test.

### T2. Entry freshness / extension filter (HYPOTHESIS, supported by two separate pieces of evidence)
- HR's ablation says timing at the break is worth about 11 points a year. The old Quad blueprint (sec 4.6) found that entries in their first month in the entry zone averaged +0.5% to +1.0% while entries aged 5+ months averaged -0.9% to -1.8%, but its staleness gate was neutral out of sample.
- Proposal: for a momentum entry, require it to be within X% of the 52-week high and not already up more than Y% in the last month; skip names that are late in the move. Evaluate as basket excess conditional on extension, on the same chunks.
- Pre-registered test to write before running: X in {5%, 10%}, Y in {20%, 30%}; success rule as in `PREREG.md` Addendum 2 part D.

### T3. A market-volatility state gate (HYPOTHESIS with partial evidence)
- 3m IC in the top tercile of 63-day market volatility: Absolute +0.015, Batch -0.005, versus +0.058 to +0.075 otherwise. In those months (about 11%) the top-N basket underperformed its universe for Absolute (-1.4%), Batch (-2.2%, t -2.7), Elendel (-1.5%), Zenith (-2.7%).
- HR supports a regime filter (worth 7 points); VCP contradicts it (costs 3 points). So the gate must be tested per book, not assumed. The live books already have a crash guard keyed to the 95th percentile of benchmark vol; this would be a lower, softer threshold (reduce new entries, not exit).
- Caveat: only about 30 gate-off months with overlapping returns; the vol z-score used full-sample mean and standard deviation (mild look-ahead), so use an expanding window in the real test.

### T4. Time stop and stale-exit on momentum holdings (HYPOTHESIS)
- HR exits positions held 45+ days that are below -5%; VCP exits 60-day positions up less than 5%. Momentum books hold until rank decay or a hard stop. The old Quad blueprint's V4 time stop (30 trading days, below +3%) helped in-sample and was about neutral out of sample.
- Test as an exit overlay on faithful-booked momentum trade logs (same replay used for HR/VCP in `faithful_replay.py`).

### T5. Risk-based sizing (HYPOTHESIS, no evidence yet)
- Breakouts size each trade as 1% risk divided by stop distance. Momentum books use inverse-vol with a 5% cap. A faithful replay of the momentum trade logs with risk-based weights is cheap to run and would show whether it matters. Note the breakout books run 10 positions at up to 15-20% each, which drives their -33% to -44% drawdowns; do not copy the concentration.

### T6. Trade-log hygiene (not a signal idea, but the biggest lesson)
- The HR and VCP engines had the same exit-day booking problem as the Elendel family. Any new idea above should be judged only on faithful booking (`faithful_replay.py`, or `csm_value/execution_replay.py` for the CSM engines), never on engine CAGR.

## 3. Proposed experiments (to be pre-registered in PREREG.md before running)

| ID | Idea | Where | Metric | Pass rule |
|---|---|---|---|---|
| E1 | R3b added to ranking (done, T1) | Absolute, Batch, Elendel, Zenith pools | Top-N basket excess, IC | Already run; needs forward paper test |
| E2 | Extension / freshness filter | Same pools, then faithful P&L | Basket excess conditional on extension; faithful CAGR/Sharpe by chunk | Latest-6-year basket t higher, full-history not lower, both halves at least as good |
| E3 | Soft vol-state gate with expanding z-score | Same pools | Basket excess gate-on vs all | Same rule; and no worse drawdown |
| E4 | Time-stop / stale-exit overlay | Faithful replay of CSM trade logs | Faithful CAGR, Sharpe, max drawdown by chunk | Better Sharpe in latest 2 chunks and both halves |
| E5 | Risk-based sizing | Faithful replay | Same | Same |
Rules for all: faithful booking, 0.3% per leg, same 36-month chunks anchored on 2026-05, report failures, at most 2 post-look changes logged.

## 4. What NOT to take from the breakout books
- Their engine returns (42-43% CAGR). They are an accounting artifact.
- VCP's regime filter (costs about 3 points a year in the faithful ablation).
- Their concentration: 10 positions at up to 15-20% each gave drawdowns of -33% to -44%.
- The assumption of unlimited capacity: both live in small and mid caps, and returns fall sharply once position size is limited to a share of daily volume.

## 5. CSM Quad: what it is, and what the re-check found (TESTED)

- **What it is:** the live CSMQuadMomentum signal is the DUAL composite (6m and 12m Sharpe, lag 1), the same factor as CSM Batch. The 3/6/9/12 "quad" signal was retired in the blueprint (sec 4.7) after losing head-to-head to the dual. Quad(universe 1-1000) reproduces Batch's factor exactly (maximum difference 0.0 on every cell). So Quad = Batch signal + mid-cap universe band (rank 500-1000, picked from the engine-booked universe sweep) + execution layer (resting stops, loss-scaled cooldown, rebalance buffer, liquid-fund parking in V3 tests).
- **It is not an upgrade of the signal.** What the blueprint credits for Quad's good engine numbers is execution features (liquid-fund parking about +5 points, cooldown, exit buffer), not the ranking.
- **Signal by universe band (6,12 lookbacks), 3m IC latest 3 years (NW-t):** 1-500 +0.018 (0.9); 1-1000 +0.017 (1.0); 250-1000 +0.026 (1.7); **500-1000 live +0.006 (0.3)**; 500-1500 +0.029 (2.0); 1000-3000 +0.059 (3.8, micro-cap, only from 2011, not tradable at size). The decay is not unique to the live band, but the live band is the weakest of the liquid ones.
- **Lookbacks:** adding the shorter legs makes the live band worse. 3m IC latest 3 years in 500-1000: (6,12) +0.006; (3,6) **-0.024**; (3,6,12) -0.002; (3,6,9,12) +0.007. In 1-1000: (6,12) +0.017; (3,6) -0.010; (3,6,12) +0.011; (3,6,9,12) +0.020. The 3m leg is the weakest, as the blueprint found.
- **Faithful P&L, latest 3 years / 2008-26 (engine claims 13-25% in the latest chunk and 26-35% overall):** live 500-1000: **-6.4%** / 7.2%; 1-1000: +0.8% / 6.3%; 1-500: +3.2% / 6.6%; 250-1000: -0.9% / 6.3%; 500-1500: +2.4% / 5.1%; live band with (3,6): -5.2% / 8.2%. Nifty 500 price index: +12.1% / 10.4%. No band or lookback gets a faithful latest-chunk return above 3.2%.
- **Verdict on the live config:** DECAYED stands (IC NW-t 0.3 for two chunks, 1.7th percentile of its own history, faithful latest-chunk return -6.4%). Changing the band or the lookbacks does not rescue it. If the Batch factor is kept anywhere, Quad is redundant with it.
- **What I could not show:** that the decay is purely signal rather than partly the execution layer. The faithful stop-fill assumption (resting stops) matters about 6 points for Zenith and was not varied here for Quad.

## 6. Files
- `PREREG.md` Addendum 2 (breakouts, momentum diagnosis, improvements) and Addendum 3 (Quad).
- `faithful_replay.py`, `breakout_backtest.py`, `breakout_checks.py`, `analyze_b1.py`, `analyze_c.py`, `analyze_d.py`, `quad_variants.py`, `analyze_quad.py`, `quad_pnl.py`.
- Tables: `results/b1_pnl_chunks.csv`, `b3_ablations.csv`, `b4_stress_faithful.csv`, `c1_ic_terciles.csv`, `c2_variants.csv`, `c3_state.csv`, `c4_quintiles.csv`, `c5_overlap.csv`, `d_improvements.csv`, `d_volgate.csv`, `q_chunks.csv`, `q_verdicts.csv`, `q_pnl_chunks.csv`.

## 7. Result of putting the lessons to work (CSM Aegis, 2026-10-19; full report in `csm_aegis/CSM_AEGIS_REPORT.md`)
Strategy: residual momentum (R1) selector + low-MAX exclusion + the wrapper below, faithful-booked. Full-history 24.4% CAGR, Sharpe 1.30, max drawdown -57%; random picks through the same wrapper: 11.3% / 0.68.
| Lesson | Tested effect (CAGR points, baseline minus ablated) |
|---|---|
| T1 price-location / residual selector | +13 vs placebo (strong) |
| Close-based hard + trailing stops | +8.8 (largest wrapper piece; max drawdown -57% vs -48% without) |
| Trend gate | +2.3 (avoids a -65% drawdown) |
| T5 risk-based sizing | +1.0 (small) |
| M3 exclusion | +0.8 |
| T2 extension filter | +0.4 (negligible) |
| T4 time stop | -0.4 (negligible) |
| T3 market-vol gate | -1.2 (does not help; drop in v1.1, same as VCP's regime filter) |
Also: the 3m decay ladder flags A1/A3/Q4 as decaying, but at their peak horizon (6-12m) A1, A2, A3, Q5, Q4, R1 are all healthy. Capacity is the binding constraint (5%-of-volume cap: 16% from Rs 1 crore, 6.6% from Rs 25 crore). Since Jan 2025 the strategy is -24% (index +4%, placebo -19.5%).

## 8. Reverse direction: momentum-book overlays tested on Aegis (2026-10-19)
Of 13 overlays from the momentum books, only the Residual strategy's market trend gate (EW index vs SMA-150, exit all and no entries at month-end) passed the pre-registered rule: max drawdown -57% -> -37%, Sharpe 1.30 -> 1.41, CAGR 24.4% -> 22.9%. Near misses: Crash Guard (fails latest-chunk Sharpe), vol targeting (turnover +26%). Clear failures: abs-momentum gate, falling-knife gate, ATR chandelier, min-hold, quarterly entries. See `csm_aegis/CSM_AEGIS_REPORT.md` section 11.
