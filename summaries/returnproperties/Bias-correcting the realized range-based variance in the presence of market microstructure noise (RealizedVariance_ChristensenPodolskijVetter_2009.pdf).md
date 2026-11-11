# Bias-correcting the realized range-based variance in the presence of market microstructure noise

Kim Christensen, Mark Podolskij, and Mathias Vetter. *Finance and Stochastics* 13 (2009), 239–268. DOI: 10.1007/s00780-009-0089-9. Published online January 30, 2009.

Source: [original PDF](../../Finance/RealizedVariance_ChristensenPodolskijVetter_2009.pdf). The supplied file contains 30 article pages and a final reproduction notice. The scanned pages were inspected using OCR and page images; equation and table references below refer to the printed paper.

## Why this matters and what the authors contribute

A high–low price range uses information that is absent from the return between the endpoints of an interval. In a diffusion model, a normalized squared range can estimate variance more accurately than one squared return. Market microstructure noise complicates that advantage: maxima tend to select positive errors and minima negative errors. At the same interval length, an uncorrected realized range can therefore be more biased than realized variance.

The paper derives a correction rather than relying on a historical rescaling of range statistics. Under a two-point independent level-noise model, the observed range is approximately the efficient-price range plus twice the noise amplitude. Estimate that amplitude, subtract it *before squaring*, and normalize by the moments of the appropriate Brownian range functional. The resulting estimator is consistent for integrated variance, has a mixed-Gaussian limit at rate $N^{-1/4}$, and admits an optimal division between the number of intraday intervals and observations within each interval.

The contribution includes the effect of estimating noise, feasible quarticity and integrated-standard-deviation estimators, a simulation study, and a Microsoft transaction-data application. Its strongest distributional result is conditional on a simple noise law. The extensions to uniform noise, rounding, and jumps have different normalizations and weaker conclusions; they are not interchangeable implementations of one universal correction.

## Latent price, observation grid, and volatility assumptions

The latent log price is a continuous Brownian semimartingale,

$$
p_t^*=p_0^*+\int_0^t\mu_u\,du+\int_0^t\sigma_u\,dW_u.
$$

The drift is locally bounded and predictable, and volatility is strictly positive. For the central limit theorems, Assumption (V) imposes a continuous Brownian-semimartingale structure on volatility itself:

$$
\sigma_t=\sigma_0+\int_0^t\mu'_u\,du+
\int_0^t\sigma'_u\,dW_u+\int_0^t\nu'_u\,dB'_u,
$$

where $B'$ is independent of $W$ and the coefficient processes satisfy the stated local regularity conditions. The common $W$ permits leverage between prices and volatility. The paper excludes volatility jumps from this proof framework, while recognizing that more general treatments are possible elsewhere.

Normalize a trading day to $[0,1]$. There are $N+1$ observed log prices at $i/N$, with

$$
p_{i/N}=p^*_{i/N}+\eta_{i/N}.
$$

The noise is independent of the latent price process and independent across observation times. Its mean is zero and variance $\omega^2$. The core Assumption (N) specifies

$$
P(\eta=\omega)=P(\eta=-\omega)=\frac12.
$$

The authors loosely interpret $\omega$ as a half-spread. It is an amplitude in the units of log price, not an observed bid–ask spread measured in currency. Independence must hold down to the observation level used to compute each range. The paper explicitly acknowledges empirical evidence against these assumptions and treats them as an approximation.

The target and nuisance functionals are

$$
IV=\int_0^1\sigma_u^2\,du,
\qquad IQ=\int_0^1\sigma_u^4\,du,
\qquad IS=\int_0^1\sigma_u\,du.
$$

$IS$ is integrated standard deviation, not $\sqrt{IV}$. They coincide for constant volatility over a unit interval, but generally differ. The estimator targets variance; annualized standard deviation requires a subsequent square root and an explicit annualization convention.

## Uncorrected realized variance and realized range

Full-grid realized variance is $RV^N=\sum_{i=1}^N(\Delta p_i)^2$. Under independent noise its bias is $2N\omega^2$, so increasing sampling frequency without correction makes it inconsistent. Sparse realized variance uses only $n\ll N$ returns and reduces the bias to $2n\omega^2$, at the cost of discarding information.

For range estimation, write $N=nm$. Divide the day into $n$ intervals, each containing $m$ elementary increments. With $\Delta=1/n$, the observed range on interval $i$ is

$$
R_i=\max_{0\leq s,t\leq m}
\left(p_{(i-1)/n+t/N}-p_{(i-1)/n+s/N}\right).
$$

Let $W$ be a standard Brownian motion on $[0,1]$ and define

$$
\lambda_{r,m}=E\left[\left(\max_{0\leq s,t\leq m}
(W_{t/m}-W_{s/m})\right)^r\right].
$$

The uncorrected realized range is

$$
RRV^{n,m}=\frac1{\lambda_{2,m}}\sum_{i=1}^nR_i^2.
$$

In the absence of noise, it estimates $IV$, and its $\sqrt n$ asymptotic variance is $\Lambda_m IQ$, where $\Lambda_m=(\lambda_{4,m}-\lambda_{2,m}^2)/\lambda_{2,m}^2$. This decreases from 2 when $m=1$ to approximately 0.4 as $m$ grows. The comparison is with $n$ endpoint returns, not with all $N$ noise-free returns. If prices were observed without noise, full-grid realized variance would still be the natural efficient benchmark. The range's value here is tied to the presence of frictions and the need to aggregate observations.

## Estimating the noise amplitude

Section 3.4 considers two estimators of noise variance. The first is

$$
\widehat{\omega^2}_N=\frac{RV^N}{2N},
\qquad \widehat\omega_N=\sqrt{\widehat{\omega^2}_N}.
$$

It is consistent, but has an efficient-price contribution approximately $IV/(2N)$ in the driftless setting. That bias can be large relative to a small noise variance at the sample sizes relevant to the paper.

The alternative is the negative first-order return autocovariance,

$$
\widetilde{\omega^2}_N=-\frac1{N-1}\sum_{i=1}^{N-1}
\Delta p_i\Delta p_{i+1}.
$$

Without drift, the expected product of successive observed returns is $-\omega^2$, so this alternative avoids the leading efficient-price bias. Under the two-point model the $\sqrt N$ limiting variances of the two noise-variance estimators are $\omega^4$ and $5\omega^4$, respectively. The lower bias therefore comes with greater variance.

The consistency statements apply more broadly than two-point noise, but the displayed variance constants should not be generalized indiscriminately. For independent centered noise with a finite fourth moment, the corresponding leading constants depend on $E\eta^4$; direct expansion gives $E\eta^4$ for the first estimator and $E\eta^4+4\omega^4$ for the second. They reduce to the printed constants when $\eta^2=\omega^2$ almost surely. This is a qualification of the lemmas' wording, not an extension of the range estimator's full central limit theorem to arbitrary noise.

The autocovariance estimate can be negative in finite samples. In the simulation the authors then switch to the nonnegative realized-variance-based estimator before taking a square root. They do not silently use the square root of a negative number or replace every negative estimate by zero. The chosen noise estimator must also match the subsequent variance formula.

## Corrected ranges and their normalization

Define corrected ranges $C_i=R_i-2\widehat\omega_N$. The proposed estimator is

$$
RRV_{BC}^{n,m}=\frac1{\widetilde\lambda_{2,m}}\sum_{i=1}^n C_i^2.
$$

The denominator is not the ordinary Brownian range moment. At high frequency, the observed maximum tends to occur at a positive-noise observation and the minimum at a negative-noise observation. The residual efficient-price range is therefore selected over different random subsets. Equation (3.3) defines

$$
\widetilde\lambda_{r,m}=
E\left[\left|\max_{t:\,\eta_{t/m}=\omega,\;s:\,\eta_{s/m}=-\omega}
(W_{t/m}-W_{s/m})\right|^r\right],
\quad 1\leq s,t\leq m.
$$

Brownian motion and the independent random signs are simulated jointly for this calibration. The absolute value is important for odd moments because the restricted maximum can be negative. The calibration is independent of the numerical value of $\omega$; only the random labels enter. Notice also the $1,\ldots,m$ indexing in this normalization, compared with $0,\ldots,m$ in the observed range definition. A faithful implementation should retain the source's convention and record any endpoint modification.

The paper estimates these moments with 1,000,000 replications. For each replication, simulate a Brownian path on the $m$-step grid, draw independent equiprobable signs, find the maximum Brownian value among positive labels and the minimum among negative labels, and take the appropriate absolute power of their difference. If one label set is empty, the paper excludes that evaluation when averaging the normalization. The probability that a specified sign is entirely absent is $2^{-m}$; the probability that either sign is absent is $2^{1-m}$. It uses $m\geq10$ to limit this problem.

Table 2 provides useful calibration checks:

| $m$ | Ordinary $\lambda_{2,m}$ | Corrected $\widetilde\lambda_{1,m}$ | $\widetilde\lambda_{2,m}$ | $\widetilde\lambda_{4,m}$ | $\widetilde\Lambda_m$ |
|---|---:|---:|---:|---:|---:|
| 10 | 1.846 | 0.981 | 1.213 | 3.063 | 1.082 |
| 30 | 2.179 | 1.252 | 1.796 | 5.348 | 0.658 |
| 100 | 2.427 | 1.410 | 2.215 | 7.450 | 0.519 |
| 300 | 2.564 | 1.490 | 2.447 | 8.782 | 0.467 |
| 900 | 2.653 | 1.534 | 2.580 | 9.587 | 0.440 |
| 23,400 | 2.748 | 1.581 | 2.725 | 10.521 | 0.416 |

These are Monte Carlo approximations, not exact constants. A replicator should generate unrounded values with a recorded seed rather than expect three-decimal entries to reproduce all original estimates. As $m\to\infty$, both normalizations converge to the ordinary continuous Brownian-range moments $\lambda_r$.

Subtracting $2\widehat\omega$ may make some $C_i$ negative. The prescribed estimator squares that signed residual. Truncating $C_i$ at zero is a different estimator and is not part of the theoretical construction.

## Consistency, limit distribution, and optimal partition

Theorem 3.3 gives consistency as both the number of intervals $n$ and observations per interval $m$ increase. Intuitively, the observed range's noise component approaches $2\omega$, while the estimated subtraction approaches the same quantity. The remaining normalized squared ranges aggregate the efficient-price variation.

For the central limit theorem, set

$$
n=c\sqrt N,\qquad m=c^{-1}\sqrt N.
$$

Theorem 3.4 additionally represents the independent noise signs using increments of a Brownian motion independent of the efficient-price process, placing all components in a filtration suitable for stable convergence. Under Assumption (V),

$$
N^{1/4}(RRV_{BC}^{n,m}-IV)
\ \Longrightarrow_{\mathrm{stable}}\ \operatorname{MN}(0,V_c),
$$

with

$$
V_c=\frac{\Lambda IQ}{c}+\frac{H_c^2\omega^2}{4},
\qquad
H_c=4\sqrt c\frac{\lambda_1}{\lambda_2}IS,
\qquad \Lambda=\lim_{m\to\infty}\widetilde\Lambda_m.
$$

The first term is efficient-price range variation. The second is uncertainty from estimating the common noise amplitude. Ignoring that second term would understate uncertainty even if the bias subtraction were approximately correct. Stable mixed-Normal convergence keeps the variance random through $IQ$ and $IS$.

Minimizing this conditional variance gives

$$
c^*=\frac{\sqrt{\Lambda IQ}}
{2(\lambda_1/\lambda_2)\omega IS},
\qquad
V_{c^*}=4\frac{\lambda_1}{\lambda_2}\sqrt\Lambda\,\omega IS\sqrt{IQ}.
$$

Higher noise favors fewer, longer intervals and more observations within each interval. Using the autocovariance noise estimator multiplies its contribution by five, so the optimal $c$ is divided by $\sqrt5$, and the minimized variance is multiplied by $\sqrt5$. This change is necessary in the simulation, which primarily uses that estimator.

For constant volatility, the paper prints numerical coefficients 1.4972 and 3.3479 multiplying $\omega\sigma^3$. The symbolic formulas should be preferred for reproduction. Substituting the continuous Brownian-range moments $\lambda_1=\sqrt{8/\pi}$, $\lambda_2=4\log2$, and $\Lambda=9\zeta(3)/(4\log2)^2-1$ yields approximately 1.46933 and 3.28552 instead. These are derived arithmetic checks; the source does not explain the difference between its printed approximations and those limiting moments.

Remark 3.7 also discusses a finite-$m$ covariance correction involving $\kappa_m$, a joint moment of the restricted Brownian range and the noise-variance statistic. Its limit is zero, but the authors report better finite-sample inference when retaining the finite-$m$ contribution. The expression and sign should be implemented with care: the main estimator uses $R_i-2\widehat\omega$, while Lemma A.1 and the subsequent appendix expansion print the opposite sign for the linear noise-estimation error. The limiting covariance vanishes, leaving the main first-order variance unchanged, but blindly combining the printed expansion and a finite-$m$ correction is unsafe. This note retains the main estimator's definition and flags the discrepancy rather than inventing an undocumented implementation choice.

## Feasible inference and an implementation sequence

The paper estimates the nuisance functionals from the same corrected ranges:

$$
\widehat{IQ}=\frac n{\widetilde\lambda_{4,m}}\sum_{i=1}^nC_i^4,
\qquad
\widehat{IS}=\frac1{\widetilde\lambda_{1,m}\sqrt n}\sum_{i=1}^n|C_i|.
$$

Both have the necessary scaling because a corrected range is of order $n^{-1/2}$. Substitute them, the appropriate noise estimate, and the chosen $c$ into the variance formula. The ordinary variance-estimation standard error is $N^{-1/4}\sqrt{\widehat V_c}$. The paper favors a log transformation for finite-sample inference. A corresponding approximate interval for $IV$ is

$$
RRV_{BC}\exp\left(\pm1.96\frac{N^{-1/4}\sqrt{\widehat V_c}}{RRV_{BC}}\right).
$$

This requires a positive estimate. Taking square roots of the endpoints gives a positive interval for $\sqrt{IV}$. Alternatively, equation (5.1) uses the direct delta-method variance $V_c/(4IV)$ for $N^{1/4}(\sqrt{RRV_{BC}}-\sqrt{IV})$. The empirical figure uses that direct square-root construction, so it should not be described as the log interval without qualification.

A reproducible implementation should estimate noise, select a pilot partition, calibrate the finite-grid moments, estimate $IQ$ and $IS$, update the proposed optimal partition if desired, and record the final integer $n,m$. The paper provides the objective and formulas but does not fully specify the pilot, iteration, rounding, or leftover-observation rules required to turn the oracle optimum into a unique software algorithm. The simulation's $m\geq10$ constraint can bind, and the empirical study deliberately overrides the theoretical optimum. These decisions should appear in saved diagnostics alongside $N$, the noise estimate, the range components, and the variance estimate.

## Simulation design and finite-sample evidence

Section 4 simulates a lognormal stochastic-volatility model,

$$
dp_t^*=\sigma_t\,dW_t,
\qquad d\log\sigma_t^2=\theta(\xi-\log\sigma_t^2)dt+\gamma\,dB_t,
$$

with independent Brownian motions. The parameters are $(\theta,\xi,\gamma)=(0.032,-0.631,0.115)$, initial log price is zero, and initial log variance is $\xi$. There are 1,000,000 Euler replications at each $N\in\{100,200,300,450,600,900,1200,1500\}$. Independent two-point noise is added with **variance** $\omega^2=0.002$, as printed on page 255. Reading 0.002 as the amplitude would materially change the experiment.

The authors use the autocovariance estimate of noise variance, switching to the realized-variance estimate if it is negative, and choose the optimal partition subject to $m\geq10$. The constraint is often binding for small $N$. The source does not supply random seeds, complete integer partition rules, or a fully specified pilot procedure for the latent quantities in the optimum. The formulas and parameterization permit a substantive reproduction, but not bit-for-bit recovery of the simulation.

Table 3 reports empirical distributions of standardized statistics. Its columns headed 0.5%, 2.5%, and so forth contain probabilities evaluated at the corresponding Normal critical values, rather than numerical quantiles of a standard Normal variable. This interpretation follows from their values and is necessary for coverage calculations, despite the caption's loose reference to simulated quantiles.

At $N=100$, the infeasible standardized statistic has mean 0.346 and standard deviation 1.221; its probability below the nominal 2.5% critical value is 0.003, and below the nominal 97.5% value 0.898. Thus the implied central 95% coverage is about 89.5%. Estimating the variance changes the skewness: the feasible untransformed statistic has mean −0.062, standard deviation 1.171, and corresponding probabilities 0.068 and 0.999, implying about 93.1% coverage with pronounced tail imbalance.

The feasible log statistic improves the approximation. At $N=100$ its mean and standard deviation are 0.142 and 1.073, with probabilities 0.028 and 0.958 at the 2.5% and 97.5% thresholds. At $N=1500$ they are 0.006 and 1.002, and those probabilities are 0.023 and 0.973, giving about 95.0% central coverage. These are finite-sample results for this calibration, not guarantees for arbitrary noise or sparse datasets.

Figure 2 compares RMSE with uncorrected range, sparse realized variance, optimally sampled realized variance, and finite-sample-adjusted TSRV. The TSRV uses regularly allocated shifted subgrids, with $K^*=(12\omega^4/IQ)^{1/3}N^{2/3}$; typical $K$ ranges from about three to eight. The corrected range has the lowest plotted RMSE for $N\geq300$, while uncorrected range deteriorates sharply with frequency. No numerical table of those RMSE curves is provided, so exact improvement percentages should not be manufactured from the graph. The comparison reflects both the faster rate than original TSRV and the favorable match between the simulated noise and the range estimator's assumption.

## Microsoft data, choices, and results

The empirical sample consists of Microsoft transactions from TAQ, January 2, 2003 through December 31, 2004. The paper says the data were screened for outliers using standard filters, but does not provide a complete trade-condition list, timestamp aggregation rule, exact session boundaries, retained-day count, or the precise mapping from irregular trades to the theoretical equal grid. These are missing replication inputs.

Noise variance is estimated separately each day by averaging the realized-variance-based estimate over 60 shifted grids of one-minute returns. This departs from using every tick because noise dependence is visible at the finest frequencies. The comparison TSRV is the dependent-noise version from a referenced paper, implemented with $J=300$ for five-minute subsampling and an area adjustment. The article's self-contained description is not a full specification of that external comparator.

A signature plot for corrected range is approximately flat down to one or two minutes, then begins to rise. The model-optimal interval would be only 30–45 seconds. The authors choose two minutes instead, explicitly sacrificing the formal optimum because the correction may be misspecified at finer scales. This is a central empirical result: the procedure's best theoretical frequency is not automatically its most credible empirical frequency.

Table 1 gives daily-estimator summary statistics in the source's reported scale; the table does not explicitly label a conversion to decimal squared log-return units, so the numbers below preserve that scale.

| Estimator | Mean | Time-series standard deviation | Lag-one autocorrelation |
|---|---:|---:|---:|
| All-tick realized variance | 12.019 | 7.615 | 0.369 |
| Two-minute realized variance | 1.946 | 1.297 | 0.701 |
| Five-minute realized variance | 1.681 | 1.309 | 0.636 |
| Thirty-minute realized variance | 1.372 | 1.305 | 0.510 |
| Two-minute uncorrected range | 3.234 | 1.694 | 0.702 |
| Two-minute corrected range | 1.685 | 0.853 | 0.381 |
| Five-minute corrected range | 1.624 | 0.887 | 0.569 |
| Five-minute adjusted dependent-noise TSRV | 1.684 | 1.366 | 0.668 |

The correction nearly halves the two-minute range mean, bringing it close to the five-minute realized-variance and TSRV means. Its time-series standard deviation is smaller, but that is not itself a direct estimate of measurement error because true daily volatility also varies. Its correlation with five-minute realized variance is 0.696 and with the adjusted TSRV 0.686; different estimates are not interchangeable merely because their sample averages agree.

Figure 3 displays annualized standard-deviation estimates and 95% intervals for July 2004. Corrected range intervals are usually narrower than those for five-minute realized variance, while uncorrected range estimates often sit above the intervals. Both quarticity estimates used for these confidence bands are calculated at a conservative thirty-minute interval, which reduces noise contamination but increases sampling error. The source gives no TSRV intervals because its referenced dependent-noise implementation lacked a feasible variance estimator there. The figure therefore does not establish that corrected range has narrower valid intervals than every competing noise-robust estimator.

## Extensions: different noise laws require different estimators

For finite-support noise with unknown ordered support points and probabilities, Section 3.7 proposes moment identification and subtraction of the estimated support width. Estimating many support points requires high-order moments and a nonlinear system; the authors warn that tiny empirical moments and large systems make this difficult. This is not a distribution-free correction.

For uniform noise on $[-\nu,\nu]$, estimate $\nu$ by $\sqrt{3\widehat{\omega^2}}$ and subtract $2m\widehat\nu/(m+2)$ from each range. Under $n=O(N^{2/3-\delta})$ and $m=O(N^{1/3+\delta})$, the *unnormalized* sum of corrected squared ranges converges to $IV/3$. It must be multiplied by three to estimate $IV$. Theorem 3.10 proves consistency only; no central limit theorem is established for this extension. The factor $1/3$ arises because extreme noise locations select approximately uniform points within a block, whose expected Brownian separation is one third of its length.

For rounded prices, the requirement is that measurement accuracy $\alpha_N=o(n^{-1/2})$. The ordinary range normalization then remains consistent because rounding changes a block range by at most order $\alpha_N$. This is a joint asymptotic restriction on precision and partition size; fixed coarse ticks do not satisfy it merely because the observation count increases.

For finite-activity price jumps, define corrected range bipower variation

$$
RBV_{BC}^{n,m}=\frac1{\widetilde\lambda_{1,m}^2}
\sum_{i=1}^{n-1}|C_i|\,|C_{i+1}|.
$$

It converges to continuous $IV$, whereas corrected squared range converges to $IV+\lambda_2^{-1}\sum J_i^2$. Consequently, $\lambda_{2,m}(RRV_{BC}-RBV_{BC})$ estimates the sum of squared jumps. The jump coefficient differs from ordinary realized variance's coefficient of one. The paper leaves the calibrated noise-robust jump-test distribution to future research; consistency alone does not supply a significance test.

## Proof mechanism and practical boundary

The appendix separates the corrected statistic into the efficient-price restricted-range term, a term linear in noise-amplitude estimation error, and a quadratic remainder. The linear term is negligible for consistency but contributes at the $N^{1/4}$ inference scale. A joint stable central limit theorem for the range statistic and the noise estimate produces the two variance contributions. Conditional symmetry and Brownian sign reversal eliminate a potential leading drift/leverage bias; leverage is permitted by the model even though the simulation uses independent price and volatility Brownian motions.

The main empirical discipline is to validate the assumed noise correction before using its optimal partition or confidence bands. The paper itself does this by moving away from the theoretical optimum when the corrected signature plot rises. The method is most convincing when its noise law, calibration constants, partition, and uncertainty calculation are all made explicit. Its range-information advantage is substantial in the supplied experiments, but the source does not demonstrate universal robustness to price discreteness, dependent noise, endogenous sampling, or arbitrary extreme observations.
