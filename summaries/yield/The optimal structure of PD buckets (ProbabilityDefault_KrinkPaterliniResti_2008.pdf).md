# The optimal structure of PD buckets

Thiemo Krink, Sandra Paterlini, and Andrea Resti. *Journal of Banking & Finance* 32 (2008), 2275–2286. DOI: 10.1016/j.jbankfin.2007.12.042. Received 5 August 2007, accepted 31 December 2007, available online 15 January 2008. Source: [original PDF](../../Finance/ProbabilityDefault_KrinkPaterliniResti_2008.pdf). All 12 pages were read, including Appendix A on differential evolution and Appendix B's full 15-bucket results. Page references below use journal pagination; PDF page 1 is p. 2275.

## Why this matters

A model can assign a different probability of default to every borrower, but an internal rating system often compresses these probabilities into a finite number of grades. The paper asks where the grade boundaries should be placed. Its object is the information loss created by replacing an individual PD with a pooled bucket PD. The number of buckets is fixed in advance at seven or fifteen; it does not jointly select the number and location of grades.

The authors propose constrained minimization of either squared PD error or squared loan-pricing error. They compare these methods with equal-population buckets and a simple mapping to external ratings. The distinctive economic argument is that pooling can overprice good borrowers within a grade and underprice bad ones. Better borrowers may move away and weaker ones may concentrate their borrowing at the bank. The pricing-error objective is therefore intended as a proxy for adverse-selection risk.

The empirical result is that constrained error-based boundaries substantially reduce the model's pricing distortion relative to the two simple baselines. Minimizing pricing error has only a small advantage over minimizing PD error when all obligors have equal weight, but a larger advantage when low-PD borrowers are assigned large exposures. Boundary performance is also examined using 2002–2005 observations while keeping 2001 thresholds fixed.

The evidence concerns a specified pricing function evaluated on estimated PDs. There are no observed customer departures, acceptance decisions, realized loan profits, or causal estimates of adverse selection. The work does not test which model predicts defaults best. It assumes that the individual PD estimates supplied by Moody's/KMV are the starting risk measurements and studies how their compression changes a downstream calculation.

## Inputs, partition, and feasible rating systems

Let $p_i$ denote borrower $i$'s individual one-year PD, $E_i$ exposure when available, and $b(i)$ its assigned bucket. For $K$ grades choose ordered boundaries $0=t_0<t_1<\cdots<t_{K-1}<t_K=1$, and assign contiguous intervals in PD space. Ties at a boundary need a consistent rule. Let $\bar p_b$ be the pooled PD associated with bucket $b$. The paper describes it as a mean of the individual PDs, subject to a minimum of 0.03%.

For unweighted squared PD error, the unconstrained within-bucket minimizer is the arithmetic mean. With exposure weighting it would be the exposure-weighted mean if the representative PD itself were freely optimized. However, the paper does not fully document how pooled PDs are computed in every weighted experiment or how that computation interacts with the floor. This is an implementation detail to recover from code or document explicitly, not an invitation to silently replace the source's reported pooled PDs by a preferred convention.

The baseline constraints are a pooled PD of at least 3 basis points, no more than 35% of customers in any bucket, and at least 1% of customers in each bucket. The first comes from the historical regulatory context; the 35% threshold was in a preliminary Basel proposal and is retained by the authors as a formal concentration restriction even though the final version did not retain that exact hard cap. These are the experiment's historical rules, not a statement of current regulation.

When exposures are introduced, the 35% concentration limit is imposed on total exposure share rather than customer count. The source explicitly changes that upper constraint; it does not say that the 1% minimum-count condition is also replaced by an exposure condition. A reimplementation should preserve this asymmetry unless it is deliberately testing a different feasible set.

The two objective families are

$$
L_{PD}=\sum_b\sum_{i\in b}(\bar p_b-p_i)^2,
\qquad
L_{PD,E}=\sum_b\sum_{i\in b}E_i(\bar p_b-p_i)^2,
$$

and

$$
L_r=\sum_b\sum_{i\in b}[r(\bar p_b)-r(p_i)]^2,
\qquad
L_{r,E}=\sum_b\sum_{i\in b}E_i[r(\bar p_b)-r(p_i)]^2.
$$

These are objectives over the partition. They do not estimate PDs from default outcomes. If pricing differs across borrowers for reasons other than PD, the notation must be expanded to $r_i(p)$; the experiment holds LGD constant and thus avoids this heterogeneity.

## Pricing formula and economic units

A one-year unit loan charges interest rate $r_i$ if the borrower survives. In default it recovers $1-LGD_i$ of principal. Equating the expected payoff with the cost of funding by debt and equity gives

$$
(1+r_i)(1-p_i)+(1-LGD_i)p_i
=(1+r_d)(1-C_i)+(1+r_e)C_i,
$$

so

$$
r(p_i)=\frac{r_d+LGD_i p_i+(r_e-r_d)C(p_i)}{1-p_i}.
$$

$C(p_i)$ is required capital per unit exposure, $r_d$ the debt funding rate, and $r_e$ the cost of equity. The denominator recognizes that contractual interest is received only on surviving loans in this simplified payoff. Expected loss and the equity funding premium both increase the required lending rate. There are no operating expenses, prepayment, collateral liquidation delays, taxes, or transaction costs in the pricing equation.

The experiments use $r_d=3.375\%$, taken from the December 2001 12-month euro Libor observation, equity premium $r_e-r_d=8\%$, a one-year loan maturity, and flat LGD of 45%. The latter is stated in the concluding discussion. The funding-rate date is an input choice, not the beginning of a return backtest.

Equation (4) prints the capital function as

$$
C(p)=1.06\,LGD\left[
\Phi\!\left(\frac{\Phi^{-1}(p)-\rho\Phi^{-1}(0.001)}{\sqrt{1-\rho^2}}\right)-p\right],
$$

with a PD-dependent $\rho$ in the footnote,

$$
\rho(p)=0.12\frac{1-e^{-50p}}{1-e^{-50}}
+0.24\left(1-\frac{1-e^{-50p}}{1-e^{-50}}\right).
$$

The printed main formula uses $\rho$ as a factor loading, whereas the footnote supplies the familiar 0.12–0.24 correlation-style quantity. This is a convention requiring verification for exact replication. A correlation parameter $R$ would enter the corresponding conditional-normal expression through $\sqrt R$ and $\sqrt{1-R}$. The PDF does not state whether the actual computation used the literal printed combination or a square-root conversion. The equations above preserve the source; the alternate interpretation is a diagnostic issue, not an official correction. A numerical reproduction should declare its convention and test whether it matches reported pricing-error totals.

The squared-error tables use an unusual scale: they multiply a squared rate measured in decimal units by 10,000 and label the result “basis points.” Thus a reported value $m=0.29$ corresponds to decimal-rate MSE $0.29/10{,}000$, and an RMS rate error of $\sqrt{0.29/10{,}000}\approx0.005385$, or about 53.9 ordinary rate basis points. It is not a 0.29-basis-point pricing error and not an average absolute error. Similarly, 0.64 corresponds to 80 ordinary basis points of RMS rate error.

The pricing transformation determines where extra resolution is valuable. Locally, $r(\bar p_b)-r(p_i)\approx r'(p_i)(\bar p_b-p_i)$, so the rate objective behaves like a PD-error objective weighted by $[r'(p_i)]^2$, and additionally by $E_i$ in the exposure case. This first-order interpretation is derived here; it explains why monetary weighting and the slope of the pricing function change the optimal allocation of buckets.

## Optimizer and baselines

Strategy (a) chooses approximately equal numbers of obligors per grade. Strategy (b) uses boundaries obtained halfway between selected Moody's historical default rates. Its six internal boundaries are 0.032%, 0.071%, 0.189%, 0.848%, 2.935%, and 9.585%. Strategies (c) and (d) minimize constrained PD error and constrained pricing error, respectively, using differential evolution (DE). With exposure data, strategy (a*) instead gives approximately equal total exposure to each grade.

The source's Table 1 repeats the label Baa three times, and the nearby text says a borrower with a 5% PD would be assigned to Aa. The listed thresholds contradict that example: 5% lies between 2.935% and 9.585%, while Aa lies around 0.032%–0.071%. The notes retain the numeric thresholds as the implementable benchmark without propagating the mislabeled illustrative rating claim.

Appendix A describes DE's Rand/1/Exp operator. For target candidate $x_j$, select three distinct other candidates, form a mutant $y=x_m+F(x_k-x_l)$, apply exponential crossover with the target, and retain the trial if its fitness improves. Iterate for a fixed budget and report the best candidate. In this application a natural vector consists of the $K-1$ boundaries, but the paper does not disclose its exact encoding, sorting or repair rule, treatment of ties, or constraint penalty.

Population size, mutation factor, crossover probability, number of generations, random seeds, number of restarts, stopping criterion, and computational time are not provided. The claim that DE needs little parameter tuning does not replace those missing reproducibility inputs. DE is a heuristic and the results are not accompanied by global optimality certificates.

Standard unconstrained k-means is discussed as a predecessor and used in a limited comparison, not as the main constrained optimizer. The relevant distinction is that ordinary k-means does not directly enforce these occupancy and exposure constraints. It does not imply that DE is the only algorithm capable of solving this one-dimensional segmentation problem. A researcher can also construct exact dynamic-programming benchmarks over sorted PDs when segment costs and constraints depend only on a contiguous segment; that is an extension beyond the paper's implementation.

## Data and timing

The main data are year-end 2001 Moody's/KMV expected default frequencies for public and private European firms. For public firms EDFs are described as coming from asset value, asset volatility, and debt; for private firms the source uses financial ratios together with listed-peer information. The authors do not reestimate those models. The reported PD range is 0.02%–20%, mean 5.5%, and median approximately 3.1%.

There are internal count discrepancies. The narrative says more than 150,000 observations, Table 2 totals 109,354, and the main time-persistence and portfolio calculations use 109,350. No sample-selection reconciliation is supplied. It would be misleading to invent an exclusion rule explaining the four-observation difference or the much larger narrative number.

Table 2 covers 17 countries. The UK contributes 27,343 observations, France 19,486, Italy 15,051, Spain 12,540, Sweden 7,909, Belgium 6,636, Norway 4,058, Denmark 3,115, Netherlands 3,063, Finland 2,675, Germany 2,673, Portugal 1,789, Greece 1,749, Ireland 495, Austria 446, Switzerland 191, and Luxembourg 135. The displayed national mean PDs include 3.1% for Germany and 6.9% for Portugal; the prose's claim that the range starts with Ireland at 3.4% overlooks Germany's lower tabulated value.

The decile table shows the right-skewed distribution. Successive PD intervals in percent are 0.02–0.4, 0.4–1.0, 1.0–1.5, 1.5–2.2, 2.2–3.1, 3.1–4.4, 4.4–6.5, 6.5–10.8, 10.8–15.5, and 15.5–20. Their average PDs are 0.2, 0.7, 1.2, 1.9, 2.6, 3.7, 5.3, 8.4, 13.5, and 17.5%. These are descriptive bins, not the optimized rating buckets.

For persistence, the 2001 boundaries are kept fixed and applied to available EDFs in each year 2002–2005. Pooled PDs are recalculated each year. Firms can enter and leave; the panel is not restricted to survivors observed in every year. Counts are 100,114 in 2002, 92,659 in 2003, 99,343 in 2004, and 72,835 in 2005. Mean PD is 5.7%, 5.0%, 4.7%, and 3.7%, respectively. This tests boundary portability as the risk mix and sample composition change. It is not a fixed 2001 prediction of future realized defaults, and it uses each later year's PD inputs to recalculate grade representatives.

## Main seven-bucket results

Table 4 gives the following thresholds and representative PDs. All entries in the first two rows are percentages, with six internal boundaries and seven pooled values.

| Quantity | Equal-count (a) | External mapping (b) | PD objective (c) | Pricing objective (d) |
|---|---|---|---|---|
| Internal boundaries | 0.64, 1.43, 2.43, 3.93, 6.92, 14.03 | 0.03, 0.07, 0.19, 0.85, 2.94, 9.58 | 1.74, 3.86, 6.55, 9.93, 13.58, 17.02 | 1.42, 3.48, 6.25, 9.83, 13.65, 17.13 |
| Pooled PDs | 0.31, 1.02, 1.90, 3.11, 5.21, 10.19, 16.72 | 0.03, 0.06, 0.13, 0.50, 1.78, 5.32, 15.00 | 0.81, 2.68, 5.03, 8.06, 11.79, 15.37, 18.67 | 0.66, 2.33, 4.67, 7.83, 11.78, 15.44, 18.76 |
| Sum of squared pricing errors | 6.97 | 15.55 | 3.23 | 3.17 |
| Scaled mean squared pricing error | 0.64 | 1.42 | 0.30 | 0.29 |

The rate objective reduces the displayed MSE by about 55% against equal-count bucketing and about 80% against mapping, using the rounded table values. Its gain over the PD objective is small in this unweighted sample. Both optimized methods devote relatively few grades to low-PD firms and more to high-PD firms, where rate distortion is larger. Figure 1 makes the associated customer concentration visible; the constraints prevent the low-PD bucket from absorbing an arbitrarily large share.

For fifteen buckets, Table 5 reports squared-error sums of 1.70, 0.69, and 0.67 for (a), (c), and (d), and scaled MSEs of 0.16, 0.06, and 0.06. External mapping is omitted because the chosen scale has only seven buckets. Appendix B.1 gives all thresholds. The pricing-objective boundaries in percent are 0.56, 1.29, 2.15, 3.15, 4.31, 5.64, 7.16, 8.84, 10.65, 12.50, 14.21, 15.68, 17.12, and 18.83. Its pooled values are 0.28, 0.92, 1.70, 2.63, 3.70, 4.94, 6.35, 7.95, 9.70, 11.57, 13.42, 14.99, 16.37, 17.87, and 19.76%.

The result that more buckets reduce compression error is expected. The practical issue is the tradeoff against enough observations per grade to assess calibration. The paper fixes seven and fifteen to illustrate two systems; it does not quantify the estimation variance of grade PDs or optimize that bias–variance tradeoff.

## Persistence with fixed 2001 boundaries

Table 6's seven-grade scaled MSEs are:

| Year | Equal count | Mapping | PD objective | Pricing objective |
|---|---:|---:|---:|---:|
| 2001 | 0.64 | 1.42 | 0.30 | 0.29 |
| 2002 | 0.68 | 1.44 | 0.30 | 0.29 |
| 2003 | 0.60 | 1.24 | 0.29 | 0.27 |
| 2004 | 0.55 | 1.08 | 0.28 | 0.27 |
| 2005 | 0.42 | 0.82 | 0.26 | 0.24 |

For fifteen grades, equal-count error is 0.16, 0.16, 0.14, 0.13, and 0.10 from 2001 to 2005. The PD-objective error is 0.06 in every reported year; the pricing-objective error is 0.06 through 2004 and 0.05 in 2005. Rounding limits conclusions about small differences.

Optimized boundaries retain their advantage without annual threshold refitting. Their error does not rise as a conventional out-of-sample statistic might because the distribution moves toward lower PDs, making the rate function easier to approximate over the realized sample. The authors acknowledge that a worsening PD mix could increase errors. There is no explicit crisis-period test, constant-composition comparison, or reweighting decomposition separating economic improvement from sample entry and exit. The findings support stability in this particular 2001–2005 sequence, not invariance to arbitrary credit cycles.

## Exposure weighting and the strongest comparison

The KMV data contain no loan exposures, so the authors assign them synthetically to match aggregate shares from the Basel Committee's 2005–2006 survey. Borrowers with $p_i\le0.2\%$ receive exposure 32.1 euros, those with $0.2\%<p_i<0.8\%$ receive 9.4 euros, and those with $p_i\ge0.8\%$ receive one euro. The groups are 4.7%, 12.5%, and 82.8% of customers but 42.97%, 33.44%, and 23.59% of exposure. The total is approximately 383,633 euros for the 109,350-obligor sample.

This transparent weighting scheme intentionally makes low-PD names economically dominant. It is not observed borrower-level exposure data, and the future-dated survey is used to construct a retrospective 2001 scenario. It should not be described as a historically executable 2001 decision rule using only contemporaneous information.

With seven grades, Table 8 reports pricing-error sums of 74.72 for equal-exposure bucketing, 16.09 for mapping, 7.49 for the PD objective, and 6.56 for the pricing objective. Their exposure-weighted scaled MSEs are 1.95, 0.42, 0.20, and 0.17. The approximately 15% gain of (d) over (c), using rounded MSEs, is substantially larger than in the unweighted experiment. Mapping improves relative to the naive strategy because its fine low-PD resolution now aligns better with where exposure is concentrated.

The optimized weighted boundaries in percent are:

| Boundary | PD objective | Pricing objective |
|---|---:|---:|
| 1 | 0.16 | 0.17 |
| 2 | 0.63 | 0.63 |
| 3 | 3.21 | 2.04 |
| 4 | 6.72 | 5.66 |
| 5 | 11.41 | 10.85 |
| 6 | 15.95 | 15.78 |

The pricing objective's pooled PDs are 0.09%, 0.39%, 1.30%, 3.50%, 7.83%, 13.71%, and 17.74%. Its middle boundaries differ visibly from the PD-only partition. Footnote 23 reports that unconstrained k-means gives an exposure-weighted mean error of 0.34 on the same scale and puts more than 80% of clients in the first bucket. That shows why evaluating objective value without the grade-composition constraints would be incomplete.

Appendix B.2 gives the fifteen-grade weighted results: pricing-error sums 15.47, 1.40, and 1.01, and scaled mean errors 0.403, 0.037, and 0.026 for equal exposure, PD objective, and pricing objective. The sum-based improvement from 1.40 to 1.01 is about 27.9%, consistent with the text's 28% statement. Using rounded means would yield a slightly different percentage. The source accidentally points to Table 9 when discussing these fifteen-grade exposure results; the actual detailed table is B.2.

The weighted pricing-objective thresholds in B.2 are 0.16, 0.41, 0.84, 1.72, 2.75, 3.96, 5.39, 7.07, 8.93, 10.97, 13.03, 14.90, 16.60, and 18.56%. Its pooled PDs are 0.09, 0.29, 0.62, 1.27, 2.22, 3.32, 4.62, 6.17, 7.95, 9.90, 12.01, 14.04, 15.73, 17.44, and 19.64%. These rounded published vectors are useful reproduction targets, but exact boundary equality cannot be expected without the underlying PD sample and optimizer settings.

## Quality-mix experiments and statistical interpretation

To test different portfolio qualities, the authors create portfolios of 10,935 borrowers, ten percent of the baseline sample. They split the original data at the sample-average PD and take a fraction $x$ from the better-than-average group and $1-x$ from the worse group. For each $x=30\%,40\%,50\%,60\%,70\%$, they generate ten portfolios and report mean errors and standard deviations across those ten samples.

Table 9's unweighted seven-grade mean errors are:

| Better-quality share | Equal count | Mapping | PD objective | Pricing objective |
|---|---:|---:|---:|---:|
| 30% | 0.445 | 2.607 | 0.380 | 0.377 |
| 40% | 0.495 | 2.370 | 0.370 | 0.399 |
| 50% | 0.523 | 2.068 | 0.360 | 0.356 |
| 60% | 0.631 | 1.733 | 0.343 | 0.303 |
| 70% | 0.713 | 1.414 | 0.304 | 0.297 |

The 40% row is an important exception: the pricing-objective result is worse than the PD-objective result on the pricing metric, and its reported standard deviation is 0.033 versus 0.002 for the PD approach. At 60%, the pricing approach's standard deviation is also comparatively large, 0.034. The paper's broad prose about superiority should not erase these cells. If both methods share the same feasible set and the rate objective is globally minimized, evaluating a PD-optimal feasible partition under that objective provides an upper bound on the achievable minimum. A worse rate-objective outcome suggests heuristic optimization variability, an implementation difference, or reporting inconsistency; the source does not isolate the cause.

Table 10 repeats the quality-mix experiment with exposures, the same relative exposure allocation, and total exposure set to 1,000 euros. The displayed mean errors for the PD and pricing objectives are respectively 25.917 versus 22.357 at 30%, 25.473 versus 21.487 at 40%, 23.876 versus 19.967 at 50%, 20.891 versus 18.142 at 60%, and 18.081 versus 16.095 at 70%. Naive and mapping means are much larger: at 30% they are 145.421 and 62.564; at 70% they are 196.140 and 38.629. The pricing-objective standard deviations are 0.150, 0.066, 0.119, 0.086, and 0.066 across the five mixes.

These Table 10 values are printed under a mean-squared-error-in-basis-points heading, yet their scale is far above Table 8's weighted means. The paper does not provide an explicit calculation reconciling the normalizations across tables. A replication should compute and report the raw weighted sum, total exposure, weighted mean, and the 10,000 scale factor separately. It should not divide or relabel the published cells based on an unverified conjecture.

The reported standard deviations measure variability across ten constructed portfolios, potentially mixed with optimizer randomness. They are not standard errors of realized economic returns or calibration tests against actual defaults. There are no formal hypothesis tests, paired confidence intervals for objective differences, or multiple-comparison adjustments. The strongest evidence is the large and repeated compression-error reduction relative to the simple baselines under the specified model.

## Reimplementation and limitations

To reproduce the study, obtain the same EDF vintages, resolve eligibility and count discrepancies, and retain the original PD values before rounding. Fix the pricing convention, flat LGD, rates, floor, and pooled-PD calculation. Sort by PD, implement contiguous buckets, and define boundary ties consistently. Evaluate each partition by computing its pooled PDs, customer shares, exposure shares where relevant, and both objective functions. Record violations explicitly rather than allowing infeasible candidates to compete through an arbitrary undocumented penalty.

Run the seven- and fifteen-grade equal-count baselines and seven-grade mapping baseline before optimization. For DE, archive the candidate encoding, mutation and crossover parameters, population, random seeds, iteration budget, repair procedure, and best feasible value by iteration. Use multiple starts and compare the pricing-optimal candidate with the PD-optimal candidate scored under the pricing objective. The anomaly in Table 9 makes this particularly useful: the latter is a feasible incumbent that the rate optimizer should never lose.

A deterministic comparison can precompute segment costs on the sorted unique PD grid. For a fixed pooled-PD rule, each candidate interval has a count, exposure total, representative PD, and objective contribution. Dynamic programming can minimize the sum over exactly $K$ contiguous intervals while enforcing interval-local bounds. Repeated PD values should remain together unless the experiment explicitly permits splitting identical risk estimates. This algorithmic suggestion is a researcher extension, not a claim about the authors' original solver.

For the temporal experiment, save the 2001 boundaries, reassign each later year's available names, and recompute pooled values without moving the thresholds. Report both the later objective and occupancy violations: boundaries that satisfy 2001 concentration constraints need not satisfy them after the population changes. The article reports objective persistence but not a complete later-year constraint audit. A separate test can keep the pooled PDs fixed as well, but that is a different question and should not replace the published exercise.

For weighting, apply the exact three-region exposure schedule and retain the distinction between equal-count and equal-exposure benchmarks. For quality mixtures, specify sampling with or without replacement, the threshold used to define better quality, whether each draw receives a newly optimized partition, and random seeds. These details are not all documented. Report sampling uncertainty separately from optimization variability by repeating optimization on a fixed sample as well as changing samples.

Economically, the rate-error loss is symmetric in overpricing and underpricing. Actual customer response may be asymmetric and depend on competitors, switching costs, credit limits, relationship depth, and access to other lenders. Heterogeneous LGD and maturity could change the preferred allocation of grades, and synthetic exposure weights omit single-name concentrations within a PD region. The source identifies flat LGD and its simplified exposure construction as limitations.

The paper establishes that grade design is a consequential approximation problem and that the loss function should match its use. It does not establish that the proposed buckets maximize realized loan-book profit or minimize actual adverse selection. A credible deployment would need observed exposures, borrower-level costs and recoveries, stable vintage definitions, an explicit validation framework, and tests of customer response. Within the supplied evidence, constrained pricing-aware bucketing is a well-motivated way to reduce a measurable model-implied distortion, especially when exposure sizes vary systematically with risk.
