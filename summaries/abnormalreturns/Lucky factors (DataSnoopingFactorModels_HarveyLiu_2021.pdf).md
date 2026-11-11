# Lucky Factors

**Campbell R. Harvey, Yan Liu · 2021 · *Journal of Financial Economics* 141(2), 413–435 (doi:10.1016/j.jfineco.2021.04.014; earlier titles "How many factors?", "Incremental factors") · Source file `Finance/DataSnoopingFactorModels_HarveyLiu_2021.pdf` (article-in-press, 23 pp.) · 14 (and 56) candidate factors; individual US stocks with ≥36 months of data, Jan 1968 – Dec 2012 (540 months)**

## Claim / contribution

- Factor selection depends on (i) the testing approach (time-series/panel vs cross-sectional), (ii) the test portfolios, and (iii) multiple testing. The paper proposes a **bootstrap, stepwise selection test for incremental factors** in panel (time-series) regressions. It works on **individual stocks** (no portfolio sorts, $N>T$ allowed, no residual covariance inversion) and controls the family-wise error rate via a White (2000) / Romano–Wolf "reality check" on the **best** candidate.
- Key idea: impose the null "candidate adds no cross-sectional explanatory power" **in sample** by shifting the candidate's mean only, keeping all its time-series properties.
- Findings: the **market is by far the most important factor** (it is not knocked out, unlike in Fama–MacBeth tests). Equal-weighted errors select **mkt + SMB + HML**; value-weighted errors select **mkt + QMJ** (profitability group). Everything else (momentum, BAB, liquidity, investment, …) adds nothing significant.
- Spanning-test "alpha" is not the same as usefulness: **Berkshire Hathaway**'s excess return (≈20% p.a. 1965–2019) has an FF5 alpha of 10.6% p.a. ($t$=12.3) as a "factor", yet does not help explain the cross-section.

## Method

Baseline and augmented time-series regressions for each stock $i$:
$$R_{it}-R_{ft}=a_i+b_i'F_t+e_{it},\qquad R_{it}-R_{ft}=a_i^{+}+b_i^{+\prime}F_t+b_{i2}^{+}f_{2t}+e^{+}_{it}.$$
Taking expectations, $E(R_i-R_f)=a_i+b_i'E(F)$: a factor with $E(f)=0$ keeps its $R^2$ and slopes but has zero effect on intercepts.

**Null imposition (orthogonalization).** Project the candidate on the baseline factors, $f_{2t}=\delta_0+\delta_1'F_t+\varepsilon_t$, and define the pseudo-factor
$$f^{*}_{2t}\equiv f_{2t}-\delta_0=\delta_1'F_t+\varepsilon_t .$$
Then, exactly in sample, $a_i^{+}=a_i$ and $b^+_{i1}+b^+_{i2}\delta_1=b_{i1}$ (Eqs. 7–9), and $E(f^*_2)=\delta_1'E(F)$: its premium is fully explained by its baseline exposures. With no baseline factor this is simple demeaning. (Predictive-regression and Fama–MacBeth adaptations are in the online appendix.)

**Test statistics** ($s_i$ = s.e. of the **baseline** intercept, used for both models so the statistic is exactly 0 under the in-sample null):
$$SI^{m}_{ew}=\frac{\frac1N\sum_i(|a^+_i|-|a_i|)/s_i}{\frac1N\sum_i|a_i|/s_i},\qquad SI^{med}_{ew}=\frac{\mathrm{med}(|a_i^+|/s_i)-\mathrm{med}(|a_i|/s_i)}{\mathrm{med}(|a_i|/s_i)},$$
$$SI^{m}_{vw}=\frac{\sum_t\sum_i\frac{me_{i,t}}{ME_t}(|a^+_i|-|a_i|)/s_i}{\sum_t\sum_i\frac{me_{i,t}}{ME_t}|a_i|/s_i}.$$
Negative = improvement (e.g. −0.206 = 20.6% reduction in the median scaled absolute intercept). Scaling by $s_i$ ~ information-ratio logic, downweights noisy stocks, and makes the statistic closer to pivotal (Hall–Wilson). Scaled statistics had ~15% more power than unscaled ones in simulation. The median is used for individual stocks for robustness.

**Bootstrap.** Resample time periods (same draws for all stocks and all candidates, preserving cross-sectional and cross-candidate dependence). Compute each orthogonalized candidate's statistic, record the **minimum** across candidates, and compare the realized minimum with this distribution → multiple-test p-value. Add the winner if $p<5\%$, re-orthogonalize the rest against the new baseline, repeat; stop when the best candidate fails. Baseline and candidate lists must be fixed ex ante. Stocks need ≥36 observations in the original or bootstrapped sample (unbalanced panel allowed). Block bootstrap is a robustness check (online appendix).

**Contrast with GRS:** GRS tests whether the augmented model is exactly true (almost always rejects, needs $N<T$, implies extreme tangency weights). This test assumes the baseline and asks whether the candidate *significantly reduces* pricing errors, so misspecified models can be compared.

## Data

14 factors (Jan 1968 – Dec 2012, limited by Pástor–Stambaugh): mkt, smb, hml, rmw, cma (FF5), mom, skew (Harvey–Siddique), psl, roe and ia (HXZ), qmj, bab, gp (Novy-Marx), civ (common idiosyncratic volatility). Factor series come from the original authors. Annual means (Table 1): mkt 5.2% ($t$=2.17), smb 2.2% (1.32), hml 4.8% (3.08), mom 8.1% (3.54), roe 6.8% (5.09), ia 5.7% (5.76), qmj 4.8% (3.74), bab 10.5% (5.98); nine of 14 have $t>3$. Clusters: cma–ia 0.90, hml–cma 0.71, rmw–qmj 0.76, roe–qmj/rmw 0.68. Extended set: 56 factors (adding 42 of Ehsani–Linnainmaa's 52). About 20,000 firms, average life ≈10 years.

## Results — individual stocks

**Equal weighting (Table 2, median statistic, 14 candidates):**

| Step (baseline) | Best candidate | $SI^{med}_{ew}$ | Single-test p | Multiple-test 5th pct | Multiple-test p |
|---|---|---:|---:|---:|---:|
| none | mkt | −0.206 | 0.001 (5th pct −0.095) | −0.147 | **0.002** |
| mkt | smb | −0.062 | 0.032 | −0.057 | **0.039** |
| mkt+smb | hml | −0.040 | 0.011 | −0.027 | **0.018** |
| mkt+smb+hml | (best remaining) | — | — | −0.017 | 0.932 → stop |

- With the **mean** statistic, the market is selected ($SI^m_{ew}=-0.192$, p=0.004), but smb's multiple-test p is 0.071 and hml's 0.122. The FF3 result therefore depends on using the median.
- civ is individually strong without a baseline (−0.130, single p 0.031) but loses to the market.
- Momentum, roe, qmj and ia **increase** errors (e.g. roe +0.187, qmj +0.358 with no baseline; mom +0.089 after mkt).
- Cumulative reduction relative to baseline: 20.6% + (1−0.206)·6.2% = 4.9% + 3.0% = **28.5%**. Most pricing error remains.

**Value weighting (Table 3):**

| Step | Best | $SI^m_{vw}$ | Multiple-test p |
|---|---|---:|---:|
| none | mkt | −0.444 | <0.001 (5th pct −0.258) |
| mkt | **qmj** | −0.149 | **0.004** (rmw −0.146, bab −0.088, roe −0.079) |
| mkt+qmj | bab | −0.026 | 0.637 → stop |

Cumulative: 44.4% + (1−0.444)·14.9% = 8.3% → **52.7%**, about double the equal-weighted figure. HML would give only 3.8% after mkt under VW. QMJ represents a profitability group (qmj/rmw/roe); combining correlated factors into composites does not help (online appendix).

**56 candidates (Tables 4–5):** same final models (EW: mkt, smb, hml; VW: mkt, qmj). Extra EW candidates with negative statistics after mkt: cp, ep, em, ssi, lsi, maxr. VW candidates after mkt: ag, noa, ssi, lsi, tef, fage, lr (all small, ~−0.01).

**Why the market survives here but not in Fama–MacBeth:** panel regressions let asset-specific intercepts absorb omitted-factor/mispricing components. Example: A and B both earn 10%, betas 1 and 2, market premium 5%. A cross-sectional regression gives a zero slope (CAPM "rejected"); the panel approach sees intercepts fall for both (A keeps a 5% alpha, B zero). Using FF 49 industry portfolios, neither smb nor hml is selected (online appendix), so test assets still matter.

**Conditional extension (Table 6, pooled regression with characteristic ranks × factors; SEs clustered by month and FF49 industry):** size×smb −0.911 ($t$=−33.60), btm×hml 1.198 (33.82), size×mkt −0.289 (−16.64), btm×mkt −0.168 (−7.40); mkt 0.893 (58.09); $R^2$ 0.180. Time-varying loadings clearly matter; this estimator differs from the main unconditional stock-by-stock regressions.

## Simulation (Appendix A)

- Setup: balanced panel of 2,732 firms × 240 months (1993–2012). True model = mkt + candidate, with empirical betas and bootstrapped empirical residuals. The candidate is $f^A_t=A\alpha_f+\beta_m mkt_t+\varepsilon_{f,t}$ with $A\in\{0,0.5,1,1.5,2\}$ ($A=0$ gives size). 1,000 simulations each.
- Benchmarks: unconditional beta-decile sort (full-sample betas) and conditional beta sort (5-year rolling betas, 1-year hold), tested by the long–short $t$-stat.

Power at $A=1$ (mean / median statistic vs conditional / unconditional beta sort):

| Factor | $T=240$ | $T=480$ | $T=480$ size-adjusted (Table A.4) |
|---|---|---|---|
| roe | 0.517 / 0.441 vs 0.377 / 0.309 | 0.801 / 0.721 vs 0.536 / 0.525 | 0.904 / 0.830 vs 0.642 / 0.598 |
| qmj | 0.671 / 0.608 vs 0.576 / 0.552 | 0.952 / 0.946 vs 0.825 / 0.879 | 0.998 / 1.000 vs 0.993 / 1.000 |
| bab | 0.600 / 0.587 vs 0.375 / 0.463 | 0.737 / 0.683 vs 0.591 / 0.603 | 0.812 / 0.793 vs 0.680 / 0.740 |
| cma | 0.534 / 0.469 vs 0.321 / 0.337 | 0.817 / 0.788 vs 0.612 / 0.749 | 0.847 / 0.833 vs 0.590 / 0.745 |

The proposed tests are roughly correctly sized (beta sorts under-reject owing to errors-in-variables). Power is ~10 pp above conditional beta sorts at $T=240$. Average power at $T=480$ is 83% across the five factors, vs ~76% for Jegadeesh et al.'s EIV-corrected FM test with 684 months (not like-for-like). Individual stocks give power similar to the FF25 portfolios. The real sample has ≈1.8× the simulated firm-months.

## Critical assessment

- **Convincing:**
  - Clean, exact in-sample null that separates time-series fit from pricing contribution.
  - Multiple-testing control over the candidate family.
  - Feasible with $N\gg T$.
  - Explicit about economic weighting.
  - Clear reconciliation of the "market is dead in cross-sectional tests" puzzle.
- **Fragile / caveats:**
  - Conclusions depend on the loss function: median vs mean (SMB/HML fail under the mean) and EW vs VW (FF3 vs mkt+QMJ). The weighting should be fixed in advance.
  - "Useful" means reducing |alpha|/s.e. given the in-sample premium (panel view: premium = factor mean). A factor with the right premium but mismatched betas can raise errors (momentum).
  - FWER control covers one step; the sequential path, the choice of candidate family, the sample and the factor constructions are not simulated jointly. Profitability factors are post-2015 discoveries backtested to 1968 (acknowledged).
  - Constant betas over a stock's life for unconditional tests; iid time resampling in the main bootstrap (block bootstrap only in the appendix).
  - Large residual pricing error remains (~70% EW, ~47% VW), so the selected models are "least bad", not correct.
- **Source inconsistencies:**
  - The Table A.3 caption says "size-adjusted", but Table A.4 is the size-adjusted one.
  - The text says power "well above 70%" at $T=480$, while the BAB median statistic is 0.683.
  - Table 4 (56 factors) reproduces Table 2's Panel B multiple-test values exactly (0.071/0.039), and its Panel A multiple-test 5th percentile (−0.136) is *less* stringent than with 14 factors (−0.147), contrary to the stated tougher hurdle.
  - Minor bracket typos in Tables 3–5.

## Practical relevance for a quant PM

- For risk-model/benchmark design, the market factor carries most cross-sectional pricing content for individual stocks. Beyond it, size/value (small-cap-weighted universes) or a profitability/quality factor (cap-weighted universes) are the only robust additions among the classics.
- To vet a new factor: fix the baseline (e.g. mkt + qmj) and a candidate list, subtract the candidate's baseline alpha, bootstrap months jointly, and require the best candidate to beat the max-statistic distribution. Report the % reduction in scaled |alpha| rather than standalone alpha/Sharpe.
- High-Sharpe strategies (momentum, BAB, even BRK) can be excellent portfolio additions (spanning) yet poor pricing factors. Keep the two questions separate when deciding what goes into an attribution model versus the alpha book.
