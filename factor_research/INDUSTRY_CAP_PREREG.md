# Pre-registration: per-industry name cap inside the live Zenith / Elendel engines (written 2026-10-12, before any run)

## Question
FINDINGS §8.4 found that the ~10-12 pt MaxDD reduction of the industry-led book came from "at most 2 names per industry + positive-trend filter", not from ranking hot industries,
and §7 Stage 2 suggests the failed score-tilt concentrated names in one industry. Does simply **capping names per `Industry_clean` inside the unmodified live engines** reduce drawdown
without giving up return? This is a constraint, not a signal: scores, universe, gates, hysteresis, sizing, stops, Crash Guard, regime leverage and costs are untouched.

## Design (fixed now)
* Engines: `CSMZenith` and `CSMElendel` from `Old_live_strategies/` (imported, never edited), current working-tree code (includes the user's 2026-10-09 fixes), 0.3% cost, event-driven backtest via the live runners' own `backtest_event_driven`.
  Base = same engine, cap off, run natively in this study (cached older runs are NOT used).
* Cap: at most **K = 2** names per `Industry_clean` label (primary). Names with no industry label are **uncapped** (each its own group). Implemented through the engine's existing D4 hook
  (`sector_cap_frac`, `_get_sector_map`) for Zenith; Elendel borrows Zenith's `get_positions` (identical code apart from the D4 block) - parity test below proves this changes nothing at cap off.
  `sector_cap_frac = 0.13` -> `ceil(0.13 * 15) = 2`.
* Sensitivity (reported, NOT selectable): K = 3 (`0.2`). Also a **placebo**: same cap applied to industry labels randomly permuted across the labelled tickers (sizes preserved), 5 draws, to separate "industry meaning" from "any grouping constraint".
* Windows: 2005-01-01+ and 2015-01-01+ on daily net returns (as in `csm_resid_tilt/compare_to_live.py`). Metrics: CAGR, vol, Sharpe (rf 6%), MaxDD, Calmar; block-bootstrap P(better) on daily excess (21-day blocks).
* Diagnostics: % of months in which the cap binds, mean names displaced per binding month, return correlation to base, per-year delta.

## Gates (per engine, judged independently; all must hold)
* **P0 parity**: with the cap off, the subclass (and for Elendel the borrowed `get_positions`) reproduces the unmodified engine's positions and net returns exactly (max abs diff 0).
* **P1 Sharpe**: dSharpe >= 0 in BOTH windows.
* **P2 return**: dCAGR >= -1.0 pt in BOTH windows.
* **P3 drawdown**: dMaxDD >= 0 in BOTH windows and >= +2.0 pt in the 2005+ window (positive = shallower).
* **P4 not an artifact**: real-label cap must beat the median of the 5 placebo draws on dSharpe in 2005+ (if the placebo does as well, the effect is "any constraint", reported as such).
* **P5 binds**: cap binds in >= 10% of months (otherwise the test is vacuous, reported as INCONCLUSIVE rather than PASS).
Kill rule: failing P1 or P2 in either window -> the cap is not adopted for that engine. No tuning of K, labels or fallback after looking. K = 3 and placebo results can only inform, never replace the primary.

## Trial counter
Primary trials: 2 (engines) x K=2. Sensitivity: 2 x K=3. Placebo: 2 x 5. No other search. Outcome section appended below after the run.

## Outcome (run 2026-10-12; csm_industry_cap/output/industry_cap_study.txt; P0 parity PASS: positions and net returns identical to the unmodified engines at K=0)
Cap K=2 binds in ~50% of invested months (avg ~1.7 excess names), but the cap barely changes anything: return correlation to base 0.983-0.985.
| engine / window | dCAGR | dSharpe | dMaxDD (pt, + = shallower) | P(better) |
|---|---|---|---|---|
| Zenith 2005+ | -0.5 | -0.02 | +0.1 | 0.21 |
| Zenith 2015+ | -1.2 | -0.08 | -0.5 | 0.08 |
| Elendel 2005+ | -0.6 | -0.03 | -2.9 | 0.21 |
| Elendel 2015+ | +0.5 | +0.03 | -4.3 | 0.67 |
K=3: all deltas within -0.7..+0.0 pt CAGR, MaxDD -2.1..0.0. Placebo (shuffled industry labels, 5 draws) does as well as the real labels (dSharpe median -0.00 / -0.01), i.e. the cap is not industry-specific.
Gates: Zenith P1 FAIL, P2 FAIL, P3 FAIL, P4 FAIL, P5 PASS; Elendel P1 FAIL, P2 PASS, P3 FAIL, P4 FAIL, P5 PASS. **Verdict: the per-industry cap does NOT help either live engine (kill rule fired; Elendel MaxDD actually gets worse).**
Interpretation: the drawdown benefit seen in the standalone book came from its own construction (staggered tranches, ~57 names, positive-trend filter, vol target), not from the cap; the live engines' stops, Crash Guard and regime
leverage already do that job. Trials used: 2 primary, 2 sensitivity, 10 placebo.
