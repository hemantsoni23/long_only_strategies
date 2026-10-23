# Pre-registration — audit of `NEW_MOMENTUM_FACTORS_AND_IDEAS.md` (written 2026-10-20, before any new test was run)

What had been seen before this file was written: the runner's own outputs (`results/new_factors_*.csv`, `master_new_factors_summary.csv`),
the prior catalog (`results/factor_catalog.csv`) and the prior write-ups (FINDINGS, MASTER_RANKING, IDEA_ROADMAP, MOMENTUM_LITERATURE_PLAYBOOK).
What had NOT been seen: any decile/tail table for the new factors, any control comparison (plain 12-1 vs the "improved" version), any add-on book
for the new factors, any comparison against the TRUE Elendel/Zenith composites, the Newey-West calibration, the Lou-Polk-Skouras cross-persistence table.

Scope: research only. Nothing in `Old_live_strategies/` is touched; no strategy is built. Code: `stage24_new_factor_audit.py`.

## Factors under test (specs frozen here)
| id | name | spec |
|---|---|---|
| B1 | quiet_mom_12_1 | runner definition: (C[-21]/C[-252]-1) / (1 + clip(SMA21(V)/SMA252(V), 0.2, 5)) |
| B1c | mom_12_1 | control for B1: same numerator, no volume term |
| B1v | volsurge_21_252 (sign as-is) | the volume term alone, so the sign of its effect is known |
| B2 | delta_beta_252 | runner definition (beta_up - beta_down, clip ±3) |
| B2m | mom_12_1 + lambda*Delta-beta | z-blend, lambda in {0.5, 1.0} (the doc's own blend, never run by the runner) |
| B3 | intra_over_126 / 252 | runner definition |
| B3c | tot_ret_252_clip | sum of clipped (intraday + overnight) log returns: the "no-decomposition" control for B3 |
| B6 | ulcer_mom_252 | runner definition |
| B6c | mom_12_1 and mom_12_1_sharpe | controls for B6 |
| B7 | trend_accel_63 (runner) and quad_gamma_126 (true OLS quadratic coefficient on log price, 126d, scaled) | doc's formula was a quadratic fit; runner used a slope difference |
| B4 | jump_react_126 | doc "Option B": sum of returns on days with V > 3 x SMA63(V) and ret > +3% over 126d |
Blueprint 5 (factor momentum) and the SUE half of Blueprint 4 are NOT re-run: already tested (stage15/17), recorded in MASTER_RANKING.

Universe for gates: `U2_live_trend` (the pool the live books rank). `U1_liquid1000` and `U3_top300` reported as robustness only.
Baselines: TRUE Elendel = z(a3_rs_high)+z(q5_126); TRUE Zenith = z(a1_52wh)+z(q5_189) (the runner used q5_126 alone and called it Elendel).

## Gates (a factor must pass all to be "worth a real-engine test"; fixed now)
* **G1 signal**: IC(3m) in U2 with NW-t >= 3.0 on the full sample AND positive in discovery (<=2014) and holdout (>=2015) with holdout NW-t >= 2.0.
* **G2 increment**: IC of the factor's rank residualised on TRUE Elendel (and, separately, TRUE Zenith) rank, U2, 3m: mean > 0 with NW-t >= 2.0 for BOTH baselines. (The guide states this hurdle; the runner never computed it.)
* **G3 control**: for B1, B2m, B6, B3, B7 the "improved" version must beat its plain control (mom_12_1 or tot_ret_252_clip) on IC(3m) in U2 by a paired-month test with |t| >= 2 in the improving direction; otherwise the added transformation is not what carries the result.
* **G4 tail**: top-decile mean excess return over 3m (U2, winsorised 1/99, vs cross-sectional mean) > 0 with NW-t >= 2.0 and positive in both halves. (A 15-name book lives in the tail; FINDINGS §3 and the industry study both died here.)
* **G5 book**: using `portfolio_lab.topn_book` (top-15, monthly, 0.3%/side, the same proxy book as stage2/3), z(base)+w*z(factor), w in {0.5, 1.0}, base in {TRUE Elendel, TRUE Zenith}, U2: the tilted book must beat the un-tilted base on Sharpe in discovery AND holdout at BOTH weights, for at least one base. A factor that fails G5 is not carried to engine tests. (Same rule that cut industry tilt at Stage 2.)
Kill rule: failing G4 or G5 -> "IC-only, do not build". Failing G1 -> "not a signal here".

## Harness checks (descriptive, not gates)
* H1 Newey-West calibration at h = 3, 6, 12: false-positive rate of |t| >= 3 using a synthetic placebo factor with realistic rank persistence (rank AR(1) rho 0.9) against the real forward returns, 300 draws. If the false-positive rate at h=12 is > 1%, the guide's t >= 3 hurdle is miscalibrated at long horizons and a non-overlapping-sample t is reported instead.
* H2 Runner label audit: corr_elendel / inc_ic in the runner vs the same quantities against TRUE Elendel.
* H3 Doc-claim table: every numeric claim in the doc (correlation ranges, IC, t, drawdown) compared with the measured value.
* H4 Multiple testing: number of factor variants examined on this panel (111 prior + this study) stated next to every t.
* H5 Lou-Polk-Skouras cross-persistence: IC of past intraday/overnight sums against FUTURE intraday-only and overnight-only returns (3m), plus pre/post 2010-10 (NSE pre-open call auction start) split, to see whether B3 is the paper's mechanism or an artefact.
* H6 Lee-Swaminathan 2D sort: 12-1 momentum quintile x volume tercile, 3m/6m/12m forward excess, three different volume definitions (surge 21/252, 63/252, dollar-volume rank).

## Post-look rule
Any change made after seeing results is logged at the bottom of this file with the reason.

## Post-look log
(empty at time of writing)

* **Post-look #1 (2026-10-20)** — after seeing G5: `quiet_mom_12_1` passed G5 at w=0.5 (both bases) but failed at w=1.0, so it is a strict fail but the closest call. Added a *placebo* (`stage24b_quiet_placebo.py`): replace the volume-surge term by a within-month permutation of itself (same distribution, no information) and compare book Sharpe deltas. Purpose: separate "volume information" from "any heavy-tailed denominator reshuffles the top 15". Not a gate; cannot rescue a G-fail, only explain it.
* **Post-look #2** — data-quality sanity check on open prices (mean overnight/intraday return per stock by liquidity tier), prompted by H5 persistence ICs of 0.3-0.4 (t 30-45), which are too large to be ordinary return predictability.
