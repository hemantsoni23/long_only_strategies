# Decay check — pre-registered rules (written BEFORE any result was computed)

Scope: the 8 strategies in `Old_live_strategies/` (read-only, imported not edited):
residual_momentum, csm_absolute, csm_batch, csm_elendel, csm_zenith, csm_quad_momentum, hr_breakout_v2, vcp_v4.
Goal: decide whether each strategy's CORE LOGIC still works as of mid-2026, so decayed ones can be pulled from live.

## Data
Upstox OHLCV, same cleaning as `factor_research/data.py` (+-40%/+300% corporate-action mask), own cache in `decay_check/.cache`.
Broad coverage ends 2026-07-16 -> last complete month = 2026-06. Survivorship caveat applies (only currently-listed names).

## Chunks
Non-overlapping 36-month chunks, ANCHORED BACKWARD from the last usable signal month (so every chunk has equal length and the newest
chunk is genuinely the most recent 3 years, not a stub). Signals earlier than the first full chunk are used only for the full-history baseline.

## Signal-level metrics (the 6 cross-sectional strategies)
Factor = the strategy's own `calculate_factors()` output (universe-filtered), instantiated with the runner/production parameters.
Forward return = month-end close -> month-end close (same convention as the repo's `calculate_ic`). Horizons 1/3/6/12m.
Per chunk x horizon: IC (Spearman) mean, ICIR (mean/std of monthly IC), hit-rate (IC>0), plain t, Newey-West t (lag h-1),
top-N basket excess vs eligible-universe EW (N = strategy top_n), its NW-t and hit-rate, pick-level accuracy (top-N names beating the
cross-sectional median).
PRIMARY horizon = 3m (typical hold of these books). 1m/6m/12m are context, not used for the verdict.

## Event-level metrics (HR breakout, VCP — binary signals, no IC)
Events = entry signal fired AND all of the strategy's own gates passed (universe, trend, regime), de-duplicated (one event per stock per
20 trading days). Outcome = return from next-day open over 5/10/20/40/60 trading days. Two baselines per event:
(a) excess vs equal-weight market, (b) excess vs same-day TREND-GATE-PASSING non-event stocks (isolates the pattern from momentum beta).
t-stats on month-clustered mean excess with NW. PRIMARY horizon = 20 trading days, primary baseline = (b).

## Verdict tests (all computed on the PRIMARY metric = monthly IC at 3m, or monthly mean event excess at 20d)
- T1 LEVEL   : latest-chunk NW-t. >= 2.0 pass; 1.0-2.0 weak; < 1.0 fail.
- T2 TREND   : OLS of the monthly primary series on time over the FULL history, NW SE. "Declining" iff slope < 0 and t <= -2.0.
- T3 HISTORY : percentile of the latest chunk's mean among ALL rolling 36-month windows of the same series (tail risk of calling noise decay).
               <= 10th percentile = unusually bad vs own history; >= 25th = within normal variation.
- T4 REGIME  : regress the series on market regime controls (cross-sectional dispersion z, trailing-12m market return z, trailing-3m market vol z)
               + time. Report the time-slope AFTER controls and the latest-chunk mean of regime-ADJUSTED series (series minus regime part).
               A weak latest chunk is "regime-excused" only if its regime-adjusted mean is >= 25th pct of history AND adjusted slope is not significantly negative.
- T5 PERSIST : number of consecutive most-recent chunks failing T1 (NW-t < 1.0).

Verdict ladder (applied mechanically, in this order):
1. DECAYED       : T1 fail AND T5 >= 2 AND (T2 declining OR T3 <= 10th pct) AND NOT regime-excused.
2. DECAYING      : (T2 declining OR T3 <= 10th pct) AND T1 not pass (weak/fail), not regime-excused.
3. WEAK / REGIME : T1 weak or fail, but regime-excused or T3 >= 25th pct and T2 not declining. Keep, size down, monitor.
4. HEALTHY       : T1 pass and T2 not declining.
(anything else = INCONCLUSIVE; say so, do not force a label.)

## Guard rails
- No change to these rules after seeing results; any post-look change is logged in the report as such.
- The 5 stock-momentum books (absolute, batch, elendel, zenith, quad) share one underlying driver; their agreement is NOT independent evidence.
- Chunk IC is in-sample history, not out-of-sample; the only true OOS is forward paper trading.

## Implementation details fixed before running (added before any result existed)
- Anchor: last signal month T = 2026-05 for every strategy (its 1m forward month, 2026-06, is the last complete month). Chunks = 36 signal months ending T, T-36, ...; earliest partial chunk (<24 months) is dropped from the chunk table but kept in full-history series.
- Min cross-section for an IC month: 20 names. Longer horizons keep the same chunk bounds (n shown; fewer months in the newest chunk, flagged if n<24).
- T2 slope / T4 regression: OLS with Newey-West SE, lag 6 months. Time measured in years.
- T4 controls are ex-ante (known at formation): trailing-12m EW-market return, trailing-63d market vol, cross-sectional dispersion (robust sd of trailing-12m returns of the top-500-by-turnover names). Contemporaneous forward dispersion is a DIAGNOSTIC only, not used in the verdict.
- Top-N for baskets: residual 40, absolute 25, batch 30, elendel/zenith/quad 15 (each strategy's own live top_n / capacity).
- Event strategies: entry = open of the bar after the signal bar (the runner's convention), gap-cancel (>3% gap-up) applied; actual max_positions/stops/cooldowns are NOT applied (events are potential entries); outcome = close[i+h]/open[i]-1.
- Return layer (secondary, only Elendel/Zenith/Quad where faithful daily returns exist in csm_value/output/faithful_engine_returns.csv): chunk CAGR/Sharpe and excess vs EW market; NOT used in the verdict ladder.
- Event series (added before event results were scored): monthly mean excess of that month's events (months without events = missing); rolling-36m windows for T3/T4 require >=50% of months populated (CSM series: 75%); series start = first month whose trailing-12m event count >= 30; NW lag for events = 1; baseline reported both ways, PRIMARY = vs trend-gate peers (T1-T5 ladder applied to both, vs-market shown as the strategy's practical claim).

---
# ADDENDUM 2 (2026-10-19, written before any of the numbers below were computed; triggered by user challenge "breakouts not decaying looks wrong")

Finding that triggered it: the live HR/VCP engines do not charge the exit-day return (weight is 0 on exit day) and size off an inflated running PV, so their CAGR (HR 45%, VCP 42%) is not comparable to the momentum books' faithful numbers. A faithful re-booking from the trade log (drifting positions, exit day charged, gross exposure <= 100%, 0.3% per leg) gives HR 16.7% / VCP 15.6% full-history. All breakout numbers from here on use the faithful re-booking.

## Part B - breakout re-test
B1. Faithful P&L by the same 36m chunks (+ vs Nifty 500 price index), on identical windows as the faithful Elendel/Zenith/Quad series.
B2. Power-matched signal test: monthly cross-sectional rank IC (1/3/6m) of each breakout's own ranking variable (HR: 126d return = its RS lookback, and 30d return = its candidate ranking; VCP: 252d return = its RS lookback) inside (a) its universe, (b) its trend-gate pool. Same chunk / NW machinery as the CSM books.
B3. Ablations through the live engine (faithful re-booked): HR and VCP with (i) no pattern (signal always true, candidates ranked as live), (ii) no regime filter, (iii) no trend gate. Question: which component carries the P&L, and does that component decay?
Verdict rule for B: same T1-T5 ladder on the monthly faithful excess-vs-Nifty500 series is too low-powered (3-year P&L t-stats ~1); I will say so and lean on B2/B3 for the decay call.

## Part C - why the momentum books decayed (diagnostics; no changes to any strategy)
C1. 3m IC by trailing-volatility tercile and by liquidity (63d rupee turnover) tercile, per chunk.
C2. Variant ICs on a common pool: raw 12-1m return, vol-scaled 12-1m (Sharpe style), 52w-high proximity, residual momentum (R3b), per chunk.
C3. Market-state dependence: 3m IC conditional on trailing-12m market return tercile, 63d market vol tercile, and "rebound" months (prior-3m market return < -10% followed by up month).
C4. Top-N vs quintile spread (is it the extreme tail or the whole ranking that decayed).
C5. Overlap: month-end top-N name overlap and rank correlation between books (how independent are the 5 CSM books).

## Part D - improvement candidates (FIXED LIST; success rule fixed now)
I1 raw 12-1m return (no vol scaling) | I2 live Residual composite R3b (z9 + 52w-high) | I3 Zenith composite + R3b (equal z-sum) | I4 each incumbent factor + 52w-high z (equal z-sum) | I5 vol-state gate: take no new risk when trailing-63d market vol z > 1 (evaluated as basket excess in gate-on months vs all months).
Each is evaluated inside the incumbent book's own eligible pool, same top-N, same horizons, vs the incumbent.
Success ("improvement") only if ALL hold: (a) 3m top-N basket excess NW-t higher than incumbent in the latest two chunks combined (2020-06 to 2026-05), (b) full-history basket excess not lower, (c) both halves (signals <= 2016-12 and >= 2017-01) at least as good as incumbent on basket excess, (d) 3m IC not lower in the latest two chunks. Max 2 post-look changes, logged. Improvement ideas that fail are reported as failures.

---
# ADDENDUM 3 (2026-10-19, written before the Quad numbers below were computed; triggered by user: "csm_quad is the updated Absolute/Batch, decayed is wrong, check again")

Facts established from code/blueprint before any new number: (1) the live CSMQuadMomentum signal is the DUAL composite lookbacks (6,12), lag 1 = exactly Batch's (12m+6m) factor; the 3/6/9/12 "quad" signal was retired in the blueprint (sec 4.7). (2) The live runner and the faithful audit both use universe rank band 500-1000 (class default is 1-1000; band 500-1000 was chosen from the user's universe sweep, which is engine-booked). (3) Quad filter_universe is identical to Batch's. So Quad = Batch signal + mid-cap band + execution layer.
Questions: Q1 is the decay specific to the 500-1000 band? Q2 do the user's lookback ideas (3,6) / (3,6,12) / (3,6,9,12) rescue the live band? Q3 does Quad(1-1000) equal Batch (sanity)? Q4 faithful P&L by band.
Fixed config list. Signal level (IC@3m, top-15 basket excess@3m, same chunks, same T1-T5 ladder): bands 1-500, 1-1000, 250-1000, 500-1000 (live), 500-1500, 1000-3000 with lookbacks (6,12); lookbacks (3,6), (3,6,12), (3,6,9,12) on bands 500-1000 and 1-1000. P&L level (live Quad engine, faithful re-booking via csm_value/execution_replay.faithful_net_returns, 0.3% cost, same windows): bands 1-1000, 1-500, 500-1000 with (6,12), plus (3,6) on 500-1000.
Verdict for "Quad decayed is wrong" holds only if the LIVE config (500-1000, (6,12)) passes T1 (latest-chunk NW-t >= 2) or its decline is shown to be regime-excused by the T4 rule. Band/lookback findings are reported as candidate changes, not as a rescue of the live config. No rule changed after seeing results.

---
# ADDENDUM 4 (2026-10-19, written BEFORE any number below was computed): new strategy from MOMENTUM_SIGNALS_EXPLAINED.md + LESSONS_BREAKOUTS_FOR_MOMENTUM.md

User brief: build ONE more strategy from the signals in MOMENTUM_SIGNALS_EXPLAINED.md / MOMENTUM_FAMILY_BAKEOFF_REPORT.md (no sector rotation). Order: signal battery (IC, ICIR, NW-t, t, horizon, accuracy) -> decay status -> implement -> use the lessons file. Elendel = A3+Q5, Zenith = A1+Q5 with M3 exclusion, so the new book must add information, not rename them.

## Part 1 - Signal battery (all file signals except sector I1)
Signals: A1 52w-high proximity, A2 52w range position, A3 RS-line at high, A4 new-high recency, Q5 trend persistence, Q4 signed trend R2, Q3 Clenow slope*R2, Q1 -ID (frog-in-the-pan), Q2 z(12-1)+z(-ID), R1 residual momentum, V1 up/down volume, V2 volatility contraction, M1 acceleration, M2 1m reversal (sign as defined: -21d return), M3 low-MAX, T1 seasonality; references BASE (dual Sharpe 105/231 daily legs, skip 21d), CTRL (12-1 return). Formulas exactly as in the explained file.
Universe/test: top-1000 by 63d dollar volume (shifted 1 day), price >= 10, <= 5 circuit days/63d; signal at month-end; forward = month-end close to close, h = 1/3/6/12m; chunks = the same 36-month chunks anchored on 2026-05; min 20 names/month (Playbook breadth <8 reported too).
Metrics per signal: IC, ICIR, hit rate, plain t, NW-t (lag h-1) at every horizon (peak horizon = argmax mean IC); top-quintile excess/3m (NW-t), Q5-Q1 spread, monotonicity (5 quintiles, adjacent pairs rising), accuracy (share of top-quintile names and of top-15 names beating the cross-sectional median); corr with BASE; incremental IC / t after rank-residualising on (a) BASE, (b) the live information set ELEN = z(A3)+z(Q5) and ZEN = z(A1)+z(Q5) jointly; per-chunk IC and incremental IC; decay ladder T1-T5 of this file's PREREG on IC@3m.

## Part 2 - Qualification and composition rule (fixed now)
A signal is a BUILDING BLOCK iff ALL: (Q1) full-history IC@3m NW-t >= 3.0; (Q2) ladder verdict not DECAYING/DECAYED and latest-chunk IC NW-t >= 1.0; (Q3) incremental t vs (ELEN+ZEN) >= 2.0 over full history and incremental IC in the latest 6 years > 0.
Role: SELECTOR if top-quintile excess NW-t >= 2.0 and monotonicity >= 0.8; otherwise FILTER/TIMING.
Composite: selector score = equal-weight z-sum of at most 3 selectors, greedy by latest-6-year incremental t, dropping any with rank-corr > 0.85 to an already chosen one. If no signal qualifies as selector: the book's selector is the single best signal passing Q1+Q2 only and the result is labelled "not distinct". Distinctness check: mean monthly top-20 Jaccard vs Elendel and vs Zenith live holdings <= 0.35, else reported "not distinct".

## Part 3 - Strategy template (parameters fixed now; NO tuning)
Monthly rebalance on month-end signals, trade next trading-day open; entry gap-up cancel 3%. Pool: top-1000 dvol, price >= 20, circuit <= 5, close > SMA200 (C6). Selection: top 20 by selector score, hold until rank > 40 or exit rule. Exits: hard stop 15% below entry and trail 20% below peak, both CLOSE-based triggering an exit at NEXT open (executable; resting-stop fill is a sensitivity only); time stop: held >= 45 calendar days and below -5%. Sizing (C5): weight = 1% / stop distance (15%) = 6.7%, clamped [3%, 8%], gross <= 100%. Costs 0.3% per leg, cash 0% (6.5% shown separately). Faithful booking: positions drift, entry day open->close, exit day prev close->fill, charged.
Lesson components, each ablated leave-one-out: C1 extension filter (skip entries with close > 1.25 x SMA50), C2 coil timing from V2 if V2 qualifies as filter (enter only if ATR%/own 126d median <= 1.0), C3 market-vol-state gate (no NEW entries when benchmark 63d vol is above its expanding 85th percentile, needs 5y history), C4 time stop, C5 risk-based sizing (vs equal 5%), C6 SMA200 trend gate.

## Part 4 - Validation gates (from STRATEGY_VALIDATION_PLAYBOOK.md, numbers as printed there)
Stage 2: L0 and L3 NW-t >= 2.0, monotonic pairs >= 80%, breadth-excluded months <= 15%, top-2-year share of signed IC <= 50% (flag), equal- vs value-weighted IC flag. Stage 3: universe band sweep (1-500, 1-1000, 250-1000, 500-1500): Sharpe range <= 0.35, any band Sharpe > 0; parameter +/-20% (top_n 16/24, stop 12/18%, trail 16/24%, hold-rank 32/48): Sharpe swing <= 0.4; ablation scorecard with the five metrics (Sharpe, Calmar, return stability, avg drawdown depth, cost-adjusted return) and Playbook regression limits. Stage 4: bidirectional split A (2003-2012 IS / 2013- OOS) and B (reversed): OOS/IS Sharpe >= 60%, OOS Sharpe > 0, OOS IC NW-t >= 1.5. Because nothing is tuned, "IS" is descriptive; failing either direction = not validated. Stage 5: exit diagnostics per reason, >= 30 trades per bucket, END_OF_PERIOD < 5%. Stages 6-8 (paper, deploy, monitoring) are NOT run here; the report lists them as outstanding.
Extra (my additions, fixed now): placebo = 50 random selections from the same eligible pool with identical exits/sizing/filters (the signal must beat the placebo Sharpe 95th percentile, else the edge is the wrapper not the signal); faithful stress: costs 0.6%/1.0% per leg, ADV-capped capacity at Rs 1/5/25 cr start, resting-stop vs next-open exit; Nifty 500 comparison by chunk; all in the same 36-month chunks.
Accept rule for calling the strategy "worth paper-trading": passes Stage 2, Stage 3, Stage 4 both directions, beats placebo at 95%, faithful full-history Sharpe >= 0.8 AND latest-chunk faithful return > 0, and distinctness check passed. Failures are reported plainly. Max 2 post-look changes, each logged below.

## Post-look change log (Addendum 4)
1. [after the signal battery, before any strategy run] The fallback sentence "single best signal passing Q1+Q2" did not define "best". Clarified: highest latest-chunk IC@3m NW-t among Q1+Q2 passers. Battery outcome: only M3 passed Q1-Q3 (role: filter, as the explained file says); V2 failed Q2 (latest-chunk NW-t 0.2) so component C2 (coil) is DROPPED; no selector passed Q3, so the fallback applies; R1 (residual momentum, latest-chunk NW-t 4.2, HEALTHY) wins. Result is labelled NOT DISTINCT at the signal level (R1 corr with BASE 0.87).
2. [before any strategy run] Added supplementary wrapper bake-off: identical wrapper (Part 3, no tuning) with selector in {R1 (chosen), ELEN = z(A3)+z(Q5), ZEN = z(A1)+z(Q5), BASE}. Purpose: does the lessons wrapper by itself improve books built on existing signals. Placebo is run for the chosen selector only.

---
# ADDENDUM 5 (2026-10-19, written BEFORE any overlay result): adding momentum-book logic from Old_live_strategies to CSM Aegis v1.0

User brief: "add things from our momentum strategies that can help improving results". Frozen baseline = Aegis v1.0 (Addendum 4, unchanged). Source = overlays actually present in Old_live_strategies code (batch/zenith/quad/residual/absolute), ported with the books' own default parameters, NOT tuned. Take-profit / crystallisation is excluded because the Quad blueprint graveyard already measured it at -14 pp CAGR.

## Candidates (add-one on v1.0; each defined exactly)
- K1 Crash Guard (batch/zenith/quad): benchmark (EW universe) 21d vol lagged 1d above its expanding 95th percentile (min 126d) -> exit ALL positions at next open (reason CRASH_GUARD), block entries while in panic and for 10 trading days after it clears; afterwards re-enter the names of the last month-end target set (the books keep targets through the guard) at the next open.
- K2 Vol targeting (residual/quad): exposure multiplier = min(1, 15% / ex-ante 63d annualised vol of the CURRENT holdings' past returns), recomputed daily, applied only when 5 days passed since the last change or it moved > 5% (the books' throttle), 0.3% cost on the traded change.
- K3 Regime leverage (zenith): multiplier 0.6 when the EW benchmark is below its SMA-200, 0.5 in panic (K1's panic flag), min of the two.
- K4 Market trend gate (residual): at month-end, if the EW benchmark is below its SMA-150: exit all (reason MKT_GATE) and take no entries.
- K5 Corr guard (batch): if 21d vol of the current portfolio / weighted average 21d stock vol > 0.8, multiplier 0.5.
- K6 Loss-scaled re-entry cooldown (zenith/quad): after a LOSING stop exit (entry or trail stop) block that ticker for clip(20 x |loss%| / 10, 10, 60) calendar days.
- K7 Absolute-momentum gate (batch family): 12m return (skip 1m) must be > 0 at month-end.
- K8 Falling-knife gate (batch family): previous month's return >= -15%.
- K9 Inverse-vol sizing (batch/residual, adapted): weight = clip(5% x pool-median 21d vol / own 21d vol, 3%, 8%) instead of 1%/15% risk sizing.
- K10 Liquid-fund yield on idle cash 6.5% (quad blueprint). Mechanical; reported separately because it depends on the vehicle actually used.
- K11 ATR chandelier (elendel/zenith family): trailing stop = peak close - clip(3 x ATR14 (Wilder, lagged 1d), 12%, 30% of peak) replacing the fixed 20% trail.
- K12 Min-hold (batch family): entry/trail stops cannot fire in the first 5 trading days.
- K13 Quarterly entries (quad blueprint V5 low-turnover lever): new entries only at Jan/Apr/Jul/Oct month-ends; exits stay monthly.

## Metrics and adoption rule (fixed now)
Per run: the five Playbook metrics (Sharpe, Calmar, return stability = std of trailing-12m returns, average drawdown depth over >2% episodes, turnover) plus CAGR, max drawdown; Sharpe and Calmar in the two halves (2005-2012, 2013-2026), Sharpe over the latest two chunks (2020-06 to 2026-06), and results at 0.6% cost per leg.
A candidate PASSES iff ALL: (a) Calmar >= +10% relative OR Sharpe >= +5% relative vs the running config; (b) neither Sharpe nor Calmar regresses more than 15% overall (Playbook), stability/avg drawdown depth not worse by more than 20%, turnover not up more than 25%; (c) Sharpe in EACH half is no worse than 5% below the running config; (d) latest-two-chunk Sharpe >= the running config's; (e) at 0.6% cost per leg Sharpe is still >= the running config at 0.6%.
Procedure: forward selection. Rank passers by the mean of their relative Sharpe and Calmar gains; add the best; re-test every remaining candidate on top of the new running config with the same rule; stop when none passes or after 3 additions. Multiple testing (13 candidates) is managed by criteria (c)-(e) and by re-validating the final config (Stage 3 bands/params, Stage 4 both splits, placebo with identical overlays, stress). No other tuning. Max 2 post-look changes, logged below.
K10 is excluded from selection and reported as a standalone line.

## Post-look change log (Addendum 5)
(none yet)
(Addendum 5 outcome, no post-look changes: forward selection adopted K4 only; K3 passed round 1 but lost to K4 on score and failed round 2; K1 and K2 are near misses documented in CSM_AEGIS_REPORT.md section 11.)

---
# ADDENDUM 6 (2026-10-21, written BEFORE any result): user's "recommended upgrades" list for Aegis v1.1

User pasted a list (R1+52w-high selector; R1+Ulcer selector; volgate off; market-gate window 120; time stop off; stop 12%; cash yield 6.5%; vol target 15%; band (200,1000)).
Pre-test review (facts, not results): (1) Evidence for "R1+Ulcer" cites `blend_intra_ulcer` from the factor scan; that blend is intra_over_252 + low_ulcer_252, and the audit (NEW_MOMENTUM_FACTORS_AUDIT.md) says every intraday/overnight factor is suspect because the data's `open` field is not a tradable price; it is not the pasted R1+Ulcer formula. (2) Evidence for "R1+52w-high" is the T1 test on the Absolute/Batch/Elendel pools with R3b, not on Aegis's own R1 selector. (3) Market-gate window 120, stop 12%, band (200,1000), volgate off and time stop off are read off sensitivity/ablation tables I printed, i.e. post-look; "time stop 0% win rate" is mechanical (it only exits positions already below -5%). (4) Vol target 15% already failed the turnover criterion in Addendum 5 (it also cost 2.9 points of CAGR).
Data caveat checked by me before running (open vs prior close averages +0.31%/day, +87%/yr overnight in the top-500 vs +14%/yr close-to-close): all new tests use CLOSE fills (orders decided at one close, filled at the next close; no open field, no gap-cancel). Baseline = Aegis v1.1 with close fills (CAGR 21.6%, Sharpe 1.33, Calmar 0.58, MaxDD -37.5%). Open-fill numbers are shown alongside.

## Candidates (each add-one on the running config)
S1 selector z(R1)+z(A1) ; S2 selector z(R1)+z(-Ulcer252) (Ulcer = RMS of close/rolling-252d-max-close - 1 over 252d; formula of factor_research/evaluate_new_momentum_factors.py) ; F1 volgate off ; F2 market-gate window 120 ; F3 time stop off ; F4 stop 12% ; P2 vol target 15% (Addendum 5 definition) ; P3 band (200,1000) ; P1 cash 6.5% (mechanical, reported separately, never selected).
Parameter candidates (F2, F4, P3) additionally need a PLATEAU: Sharpe better than the running config in BOTH halves, and the two neighbouring settings (window 100 and 150; stop 10% and 15%; band (150,1000) and (250,1000)) each have Sharpe >= the running config's. Otherwise it is an isolated spike and fails.
Signal candidates (S1, S2) get the full battery first: IC/ICIR/NW-t at 1/3/6/12m, top-quintile excess and accuracy, monotonicity, correlation with R1 and with the live books' top-20 overlap, decay ladder at 3m and 6m, in the strategy pool (L4) and the tradeable universe (L3).
Adoption rule and forward selection exactly as Addendum 5 (criteria a-e vs the running config, max 3 additions, rank by mean of relative Sharpe and Calmar gains). Because F1-F4 and P3 are post-look, at most 2 post-look items may be adopted (Playbook), the best two by score.
Reference run (not a candidate): "all-in" = every item the user listed applied together (S1 or S2 as the user's formula, window 120, stop 12%, volgate off, time stop off, vol target 15%, band (200,1000), cash 6.5%), shown to make the interaction/over-fitting cost visible.
Final config re-validated: Stage 3 (bands/params), Stage 4 both directions, placebo with identical overlays, stress; report 2025-26.

## Post-look change log (Addendum 6)
(none yet)
Post-look change #1 (Addendum 6): after the pre-registered forward selection adopted F2 (window 120), S2 (R1+Ulcer) and P2 (vol target), I ran an out-of-sample test of the selection procedure itself (procedure_oos.py): choose using one half, test on the other. Only F2+S2 were chosen from 2005-12 and transferred to 2013-26 (Sharpe 1.32 -> 1.40, Calmar 0.57 -> 0.68, MaxDD -37.5% -> -29%, CAGR 21.2% -> 19.6%); the 2013-26 selection (volgate off, stop 12%) did not transfer to 2005-12 (Sharpe 1.328 -> 1.329). P2 was not chosen from either half. Decision: v1.2 = v1.1 + F2 + S2 + close fills; P2 stays an OPTIONAL risk dial labelled in-sample only. (This exclusion of P2 is post-look change #1 of 2.)
(Addendum 6 outcome: pre-registered forward selection adopted F2, S2, P2; after the procedure out-of-sample test only F2+S2 kept (post-look #1). S1, F1, F3, F4, P3 not adopted. Details in CSM_AEGIS_REPORT.md section 12.)

---
# ADDENDUM 7 (2026-10-21, written BEFORE any result): "R3b composite in band (200,1000) improves CAGR and lowers max drawdown" (user hypothesis)

Baseline = Aegis v1.2 (R1+Ulcer, market gate 120d, close fills): CAGR 24.2%, Sharpe 1.69, Calmar 0.83, MaxDD -29.0% (decay_check/results/v12a_validation.csv).
Hypothesis as stated by the user: replace the selector by the R3b composite and use universe band (200,1000); expected: higher CAGR AND lower max drawdown.
Two readings of "R3b composite", both tested: (R3b-pasted) z(R1)+z(close/252d high) = S1 ; (R3b-live) the Residual strategy's own composite (z of 9m vol-scaled residual momentum + z of 52w-high ratio, computed over its top-1000 turnover universe; cached in .cache/r3b1000.pkl). Selector candidates are evaluated in band (200,1000), in band (1,1000), and with the v1.2 Ulcer selector in band (200,1000) as the band-only control.
Runs: [R1ULC,(200,1000)] [S1,(1,1000)] [S1,(200,1000)] [R3B,(1,1000)] [R3B,(200,1000)]; the pre-registered success test for the hypothesis = the run improves BOTH CAGR and MaxDD vs baseline, AND passes the Addendum-5 criteria (a)-(e) vs the baseline, AND for the band: neighbours (150,1000) and (250,1000) have Sharpe >= baseline's, AND the result holds in both halves (2005-12 and 2013-26) separately on Sharpe and MaxDD. Adoption of any run additionally needs the out-of-sample procedure check used in Addendum 6 (choose on one half, evaluate on the other) not to contradict it. No other parameter touched.
Post-look change log (Addendum 7): (none yet)

(Addendum 7 outcome, no post-look changes: the hypothesis is half right. Band (200,1000) lifts CAGR by about 4-5 points (R1+Ulcer 28.0%, R1+52wH 29.5% vs 24.2%) with a plateau at 150 and 250 and gains in both halves, but MaxDD does not fall (-29.0% -> -29.5% / -29.9%). Composite in 200-1000 fails stability and latest-two-chunks Sharpe; band-only fails stability; the Residual book's own R3b is worse than R1+Ulcer. Not adopted as the default; shipped as the opt-in preset v1.2_high_return. Details in CSM_AEGIS_REPORT.md section 13.)


---
# ADDENDUM 8 (2026-10-21, written BEFORE any result): second "improvement + universe-filter" list for Aegis v1.2

User pasted (a) four improvements and (b) six OHLCV universe filters. Facts checked before running (not results):
- The quoted yearly figures (2008 -15.6% / MaxDD -18.3%, 2020 DD -12.9%, 2025 DD -11.7%, 2021 +82.4%) match output/yearly_returns_v1_2.csv.
- "Dropping the vol gate adds +1.2pp CAGR / +0.04 Sharpe": the table says +0.9pp (25.1% vs 24.2%) and +0.04. That candidate (F1) was already run in Addendum 6 and not adopted. Re-run here on the v1.2 baseline for completeness, not as a new look.
- ATR sizing: with RiskPct 1% and stop clipped to [8%, 18%], weight = 1%/stop lies in [5.6%, 8%] (12.5% before the 8% cap). The text's "3-4% for volatile names" cannot occur; the 3% floor never binds. Tested exactly as written.
- hold_rank=48 was already in the Stage-3 table: turnover 5.9x vs 6.1x (-3%), not -15-20%. Tested at 50 and 60.
- Cash yield is mechanical (reported, never selected, never tested for signal value). Avg exposure is 0.88 and the cash is idle only when below max gross, so expect well under +1.5-2.5pp.
- The pasted tradability code does not shift by one day (the default dv63 rank does) and z-scores raw rupee floors (heavy-tailed: a few mega-caps dominate z). I shift by one day in all variants and test the raw version exactly as pasted plus a log-floor variant.

Baseline = Aegis v1.2 (module defaults), faithful, 0.3%/leg, close fills.

## Part 1 candidates (add-one on baseline)
I1 cash_rate 0.065 (reported separately). I2 vol_gate off. I3 ATR stops + risk sizing (atr_stops=True, 3.0 x ATR14/close clipped [0.08,0.18]; trail unchanged). I4 hold_rank 50 and 60.
## Part 2 candidates (replace or add to the liquidity step; band stays (1,1000) unless stated; add-one on baseline)
U1 20th-percentile 63d rupee turnover, rank top-1000 (floor20). U1b same measure as an absolute filter >= Rs 25 lakh on top of the dv63 band. U2 Amihud capacity rank top-1000. U3 continuity >= 0.95 over 126d (volume>0 and high>low). U4 volume CV (63d) <= 1.8. U5 Corwin-Schultz 21d spread, drop worst 15% of the band. U6 composite z(floor)+0.5 z(Amihud)+0.5 z(continuity) top-1000 as pasted, and U6b with log floor.
For every Part 2 run also report: pool size, share of baseline pool names kept, Rs 5cr capacity-stress (adv_fraction 5%) CAGR.

## Rules
Adoption: criteria (a)-(e) of Addendum 5 vs baseline (ovl_judge.judge, same thresholds), plus both-halves check; at most 2 adoptions in total, ranked by mean of relative Sharpe and Calmar gain; parameter items (I4) additionally need neighbours (hold_rank 40/50/60 and 32) not worse than baseline on Sharpe. Because every item here is post-look for the baseline (the user list was assembled after viewing the v1.2 outputs), at most 2 can be adopted and each needs the Addendum-6 style procedure OOS check (choose on 2005-12, test 2013-26, and the reverse). A filter that raises CAGR only by removing the same liquid names that band (200,1000) removed is flagged as the band effect, not a new finding (compare against R1+Ulcer in band (200,1000): CAGR 28.0%, Sharpe 1.88, MaxDD -29.9%, which is NOT a baseline: it is shown for reference).
Post-look change log (Addendum 8): (none yet)

(Addendum 8 outcome, no post-look changes: cash 6.5% on idle cash +2.7 pts CAGR (avg exposure is 0.65, not 0.88), mechanical, enabled operationally, default stays 0. Vol gate off, ATR stops/sizing, hold_rank 50/60 fail the gain threshold. Of six OHLCV liquidity filters, five fail; the composite as pasted fails, the log-floor variant passes the judge but lies inside the noise envelope from 12 random 4%-pool-drop runs (Sharpe 1.55-1.71, MaxDD -31.4 to -26.0), so not adopted. Details in CSM_AEGIS_REPORT.md section 14.)
