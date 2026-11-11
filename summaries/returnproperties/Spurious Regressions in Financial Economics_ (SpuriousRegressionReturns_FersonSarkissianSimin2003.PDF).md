# Spurious Regressions in Financial Economics?

Wayne E. Ferson, Sergei Sarkissian, and Timothy T. Simin (2003), *The Journal of Finance* 58(4), 1393–1413. [Source PDF](../../Finance/SpuriousRegressionReturns_FersonSarkissianSimin2003.PDF). All 22 PDF pages were read, including the archive cover, instrument-sampling appendix, and references. The model, calibration footnotes, and consequential rows of Tables I–III were checked visually.

## Why this matters

A return series can have little observable autocorrelation and still produce misleading predictive-regression significance when its latent conditional mean is persistent. Unpredictable return noise hides the persistence from residual diagnostics, while an unrelated persistent predictor can align with the latent mean over a finite sample. Searching across predictors amplifies the problem because persistent candidates are particularly likely to fit those slow fluctuations by chance.

This paper extends the economic relevance of the classic spurious-regression warning from highly persistent levels to noisy asset returns. Its null is not necessarily that returns are completely unpredictable. Returns may be predictable from an unobserved state while the candidate instrument under examination has no predictive content whatsoever. That distinction separates the existence of time-varying expected returns from the validity of the particular variable selected to represent them.

The quantitative contribution is a calibrated simulation design combining stationary latent expected returns, independent candidate predictors, Newey–West standard errors, and selection of the best-fitting univariate predictor. The paper also reexamines 13 historical predictor specifications from nine studies. It does not establish that every such variable is false or that a particular larger critical value is universally appropriate. Its conclusions depend on assumptions about latent predictability, persistence, the candidate universe, and the search process.

## Model, null, and calibration

The analyst estimates

$$
r_{t+1}=\alpha+\delta Z_t+v_{t+1}.
$$

The actual return-generating model is

$$
r_{t+1}=\mu+Z_t^*+u_{t+1},
$$

where $Z_t^*$ is the unobserved deviation of the conditional mean from its unconditional mean, and $u_{t+1}$ is independent unpredictable noise. The latent state and measured predictor follow separate AR(1) processes:

$$
Z_t^*=\rho^*Z_{t-1}^*+\varepsilon_t^*,
\qquad Z_t=\rho Z_{t-1}+\varepsilon_t.
$$

The autoregressive coefficients have magnitude below one. The innovations are Gaussian with a diagonal covariance matrix, and the initial states are drawn independently from their stationary normal distributions. The measured predictor is independent of the latent state and return noise. Consequently the population coefficient on $Z_t$ is zero even when $Z_t^*$ varies substantially over time.

Let $V_* =\operatorname{Var}(Z_t^*)$ and define the latent or true predictability fraction

$$
q=R_*^2=\frac{V_*}{V_*+\sigma_u^2}.
$$

This is the population $R^2$ attainable if the latent conditional mean were observed. It is distinct from the fitted sample $R^2$ on an independent candidate predictor. The latter has zero population counterpart in every null simulation.

The unconditional return mean is calibrated to 0.71% per month, the S&P 500 excess-return mean over 1926–1998. The latent-state variance is fixed at 10% of the historical sample variance of S&P 500 returns in excess of the one-month Treasury bill. For $q>0$, the noise variance follows from

$$
\sigma_u^2=V_*\frac{1-q}{q}.
$$

Thus the total simulated variance matches the historical return variance when $q=0.10$; varying $q$ by changing noise while fixing $V_*$ changes total return variance. One should not describe all rows as matching the same unconditional stock-return variance. The pure-regression experiment gives the measured predictor the same unconditional variance as the latent state. The innovation variances are

$$
\operatorname{Var}(\varepsilon_t^*)=(1-(\rho^*)^2)V_*,
\qquad \operatorname{Var}(\varepsilon_t)=(1-\rho^2)\operatorname{Var}(Z_t).
$$

The mining experiment additionally includes $q=0$, interpreted as pure unpredictable returns with no persistent conditional-mean component. The positive-$q$ formula cannot literally be evaluated there while holding $V_*>0$. A replication must implement a separate zero-signal case; the source does not supply its exact variance-normalization code. Scale does not affect the intercept-regression $t$ or $R^2$ comparisons when applied consistently, but it does affect reported slope units.

The paper focuses on a source of failure distinct from the familiar bias caused by correlation between predictor innovations and future-return innovations. In its independent-instrument design that correlation is absent. The estimated slopes remain centered near zero; the problematic inference comes from their standard errors and, after selection, the distribution of the chosen statistic. Centering alone is not evidence that a selected coefficient is a useful forecast.

## Why weak residual autocorrelation can conceal the problem

The following calculation is derived from the source’s model to expose the mechanism. For $h\ge1$,

$$
\operatorname{Corr}(r_{t+1},r_{t+1-h})=q(\rho^*)^h.
$$

At $q=0.10$ and $\rho^*=0.98$, the first return autocorrelation is only 0.098, despite the extreme persistence of the conditional mean. Under the no-relationship null, the regression disturbance contains this persistent state plus large white noise. Residual-autocorrelation tests may therefore select only a few HAC lags.

More directly, the slope score is proportional to $Z_t(r_{t+1}-\mu)$. Independence between candidate and return processes implies

$$
\operatorname{Cov}\{Z_t(r_{t+1}-\mu),Z_{t-h}(r_{t+1-h}-\mu)\}
=\operatorname{Var}(Z)\,V_*\,(\rho\rho^*)^h.
$$

Relative to the zero-lag score variance, the exact population long-run variance multiplier in this stationary model is

$$
1+2q\sum_{h=1}^{\infty}(\rho\rho^*)^h
=1+\frac{2q\rho\rho^*}{1-\rho\rho^*}.
$$

For $q=0.10$ and $\rho=\rho^*=0.98$, it is approximately 5.8505. This calculation explains why many individually small autocovariances can matter in aggregate. It is not a derivation of the paper’s finite-sample Newey–West critical value: estimating residuals, choosing a finite lag, kernel weighting, and random denominator error all matter there.

If $\rho^*=0$, the persistent-latent-mean mechanism disappears even when the measured predictor is very persistent. Likewise, if $q=0$, there is no such signal component to align with. Selection across many regressions can still create a pure data-mining problem in both cases. Therefore the proposition “this candidate has zero slope” must not be silently equated with the stronger proposition “the return has no persistent conditional mean under any information set.”

## Estimation and the finite-sample experiment

Every candidate is evaluated in an OLS regression with an intercept. The source uses Newey–West standard errors with a data-dependent lag choice. It computes residual autocorrelations for lags 1–12 and compares their magnitudes with $2/\sqrt T$. The selected lag is the smallest cutoff beyond which no inspected higher-order residual autocorrelation is significant. A reproducible interpretation is the largest significant lag among those 12, or zero if none is significant. Boundary and finite-sample scaling conventions should be declared, since source code is not provided.

A standard implementation of the named estimator, written here explicitly, uses $x_t=(1,Z_t)'$, fitted residual $\hat v_{t+1}$, scores $s_t=x_t\hat v_{t+1}$, and

$$
\hat Q=T^{-1}\sum_t x_tx_t',\qquad
\hat\Gamma_h=T^{-1}\sum_{t=h+1}^{T}s_ts_{t-h}'.
$$

With chosen lag $H$, Bartlett weights give

$$
\hat S=\hat\Gamma_0+
\sum_{h=1}^{H}\left(1-\frac{h}{H+1}\right)(\hat\Gamma_h+\hat\Gamma_h'),
\qquad
\widehat{\operatorname{Var}}(\hat\beta)=T^{-1}\hat Q^{-1}\hat S\hat Q^{-1}.
$$

This formula makes the usual Newey–West interpretation implementable; the paper does not print its internal matrix computation or specify an optional finite-sample multiplier. The slope standard error is the square root of the second diagonal element. When reproducing the historical regressions, Table I’s final column should also be preserved: it distinguishes NW entries from MA-labelled covariance corrections, despite the prose’s broad description of HAC estimation.

The pure spurious-regression experiment sets $\rho=\rho^*$ and uses $T=66$ and $824$, the extreme observation counts in the historical examples. The persistence grid is $0,0.5,0.9,0.95,0.98,0.99$; the latent $q$ grid is $0.001,0.005,0.01,0.05,0.10,0.15$. Each cell uses 10,000 replications; the authors state that 50,000 yields similar results.

They record the average slope, the 97.5th percentile of the signed HAC $t$ statistic, and the 95th percentile of fitted $R^2$. In the symmetric null design, the positive 97.5th-percentile cutoff serves a two-sided 5% slope test. It is not a one-sided 5% cutoff. The $R^2$ test is an upper-tail 5% comparison. These distinctions also apply when the statistic belongs to the predictor selected by the mining rule.

## Pure-regression results and historical benchmarks

At latent predictability $q=0.10$, Table II reports:

| Common persistence | $t$ cutoff, $T=66$ | $R^2$ cutoff, $T=66$ | $t$ cutoff, $T=824$ | $R^2$ cutoff, $T=824$ |
|---:|---:|---:|---:|---:|
| 0 | 2.2847 | 0.0600 | 1.9862 | 0.0047 |
| 0.5 | 2.3702 | 0.0622 | 2.0320 | 0.0049 |
| 0.9 | 2.8408 | 0.0847 | 2.3758 | 0.0084 |
| 0.95 | 2.9329 | 0.0882 | 2.7342 | 0.0125 |
| 0.98 | 2.9043 | 0.0823 | 3.6356 | 0.0220 |
| 0.99 | 2.7843 | 0.0766 | 4.4528 | 0.0316 |

The fit cutoffs are fractions: 0.0220 means 2.20% of return variance, not a 2.20% return. At $T=824$, $q=0.10$, and persistence 0.98, a slope magnitude near 2 is inadequate; the simulated two-sided cutoff is 3.6356. At persistence 0.99 and $q=0.15$, that cutoff reaches 4.9151. The small-sample rows are not monotone at every parameter value, so these are simulated calibrations rather than a proven monotonicity law.

The source’s 13 historical regressions are summarized below. The dates are transcribed as displayed; monthly dates are written YYYY-MM. Table I’s fit column is described as adjusted $R^2$ in the surrounding text, while its header uses $R^2$. This distinction matters when comparing it with theoretical cutoffs derived for ordinary unadjusted fit.

| Predictor and study | Displayed period | $T$ | Lag-1 persistence | Slope $t$ | Reported fit |
|---|---|---:|---:|---:|---:|
| One-month bill yield, Breen et al. | 1954-04–1986-12 | 393 | 0.97 | −3.58 | 0.023 |
| Two-minus-one-month bill spread, Campbell | 1959-06–1979-08 | 264 | 0.32 | 2.38 | 0.025 |
| Six-minus-one-month bill spread, Campbell | Same | 264 | 0.15 | 2.13 | 0.025 |
| Lagged two-month minus current one-month bill return, Campbell | Same | 264 | 0.08 | 2.67 | 0.063 |
| All-corporate minus AAA yield, Fama | 1953-01–1987-12 | 420 | 0.97 | 1.46 | 0.005 |
| Dividend yield, Fama–French | 1927-01–1986-12 | 720 | 0.97 | 1.36 | 0.007 |
| AAA minus one-month bill yield, Fama–French | 1926-01–1986-12 | 732 | 0.92 | 2.16 | 0.007 |
| Below-BAA corporate yield, Keim–Stambaugh | 1928-02–1978-12 | 611 | 0.95 | 0.75 | 0.002 |
| Below-BAA minus bill yield, Keim–Stambaugh | Same | 611 | 0.97 | 1.48 | 0.007 |
| Dow book-to-market, Kothari–Shanken | 1927–1992, annual | 66 | 0.66 | 2.63 | 0.078 |
| Consumption–wealth–income variable, Lettau–Ludvigson | 1952Q4–1998Q4, quarterly | 184 | 0.79 | 2.58 | 0.057 |
| Dow book-to-market, Pontiff–Schall | 1926-02–1994-09 | 824 | 0.97 | 2.16 | 0.012 |
| S&P book-to-market, Pontiff–Schall | 1951-04–1994-09 | 552 | 0.98 | 1.03 | 0.001 |

The table contains annual and quarterly settings despite the prose’s broad monthly-data description. Some printed period/count pairs also need original-data reconciliation: for example, June 1959 through August 1979 contains 243 calendar months, not the displayed 264, and April 1951 through September 1994 contains 522, not 552. A faithful simulation comparison uses the reported $T$ as the paper does; reconstructing the historical data requires resolving these discrepancies rather than silently inventing observations.

Panel C calibrates $T$ and persistence to each historical row and fixes latent $q=0.10$. The term-spread row has simulated $t$ and fit cutoffs 2.3947 and 0.0103, above the reported 2.16 and 0.007. The Pontiff–Schall Dow book-to-market row has cutoffs 3.1612 and 0.0173, above 2.16 and 0.012. For the bill-yield row, $|t|=3.58$ remains above 3.2521, while fit 0.023 falls below 0.0311. Conclusions can therefore differ across the two statistics.

The paper reports that 7 of the 17 statistics previously regarded as significant lose significance after this adjustment. There are 26 statistics in total, comprising two statistics for each of 13 regressions; 17 is the significant subset. Neither count means seven separate studies are disproved. The interpretation remains conditional on the assumed latent signal strength and persistence.

## Data mining: candidate universe and selection rule

For mining, extend the measured state to $L$ independent AR(1) candidate instruments. The latent state is independent of every candidate. The analyst fits all $L$ univariate regressions and selects the one with the highest sample $R^2$. This is not a multivariate regression with $L$ regressors, and it is not selection of the largest HAC $t$ statistic. HAC standard errors differ across candidates, so those two selection criteria need not pick the same series.

The source calibrates the candidate persistence and unconditional variances using a randomly chosen pool of 500 economic series. In the appendix, the starting universe consists of 10,866 monthly series from the historical Economagic site after stated exclusions. The exclusions remove certain foreign-rate/country headings, highly granular building-permit and employment series, fine CPI categories, and international-energy data. The authors randomly draw 600 candidates, exclude mixed-frequency and extremely sparse series, and take the first 500 remaining. Thus “randomly sample 500” in the main text abbreviates a draw-and-filter procedure.

An augmented Dickey–Fuller test with a constant and no time trend fails to reject a unit root for 361 of those series; the authors replace them by first differences. The appendix does not give the exact ADF lag-selection rule, test level, observation endpoints, or list of retained series. The resulting pool has mean first-order autocorrelation about 0.15 and median about 0.02, compared with median 0.95 for the published instruments. These are calibration inputs, not a direct estimate of latent expected-return persistence.

Before simulation, the source adjusts each estimated AR coefficient using

$$
\tilde\rho=\hat\rho+\frac{1+3\hat\rho}{T}.
$$

The calibrated instruments are randomly ordered once and permanently assigned indices. Searching $L$ variables means using the first $L$ instruments from that fixed order, so nested search sizes preserve their candidate composition. The simulation reproduces their marginal variances and persistence, while imposing independence across instruments and from the latent state.

The low-persistence specification sets $\rho^*=0.15$ and uses the original calibrated candidate distribution. For the high-persistence specification, $\rho^*=0.95$ and a piecewise linear map moves the candidate median from 0.02 to 0.95 while preserving the minimum $-0.571$ and maximum $0.999$:

$$
f(\rho)=
\begin{cases}
0.95+(\rho-0.02)\dfrac{0.95+0.571}{0.02+0.571},&\rho<0.02,\\
0.95+(\rho-0.02)\dfrac{0.999-0.95}{0.999-0.02},&\rho\ge0.02.
\end{cases}
$$

The coefficients here are autocorrelations, so 0.95 means 95% persistence, not a return. Each simulated innovation variance is reset to $(1-\rho_i^2)\operatorname{Var}(Z_i)$ after choosing the relevant persistence. The source separately says that $L=1$ uses measured persistence 0.15, while the high-persistence discussion describes the transformed candidate distribution. The precise handling of this singleton case is not fully resolved without the original simulation code; it should be made explicit in a reproduction.

The appendix also describes a pairwise correlation matrix for the original 500 instruments, using overlapping observations and substituting an average correlation where overlap is absent. That matrix is not the innovation covariance used for the independent-regressor results in Table III. Importing it would change the experiment. Moreover, pairwise estimated and imputed correlations need not define a positive-semidefinite matrix without further treatment; the paper supplies no such treatment for this auxiliary object.

## Mining results: persistence and search reinforce one another

Table III uses $L=1,5,10,25,50,100,250$, the same two sample sizes, and latent $q$ from zero to 0.15. With $\rho^*=0.15$, increasing latent $q$ changes the critical values little. Searching many predictors still raises the required cutoff, but there is little interaction with persistence. At $T=824$ and $q=0.10$, the $t$ cutoffs rise from 2.0115 for one candidate to 3.8041 for 250; the fitted-$R^2$ cutoffs rise from 0.0047 to 0.0168.

At latent persistence 0.95, the interaction is substantial. The following rows use $T=824$ and $q=0.10$:

| Candidates $L$ | Critical signed-$t$ upper 97.5th percentile | Critical selected $R^2$, 95th percentile |
|---:|---:|---:|
| 1 | 2.6274 | 0.0113 |
| 5 | 3.6661 | 0.0216 |
| 10 | 4.0003 | 0.0264 |
| 25 | 4.5660 | 0.0331 |
| 50 | 4.9129 | 0.0374 |
| 100 | 5.2567 | 0.0421 |
| 250 | 5.6937 | 0.0482 |

At $T=66$ and high persistence, raising $q$ from zero to 0.15 changes the $L=1$ cutoff from 2.3446 to 2.8484, but changes the $L=250$ cutoff from 5.2493 to 6.2563. At $T=824$ and $L=250$, the corresponding change is from 3.8103 to 6.0420. Data mining worsens the consequences of latent persistence, and latent persistence worsens the consequences of data mining.

These selected slope distributions remain approximately centered at zero because the search chooses high fit without fixing a favorable coefficient sign. A mean selected slope near zero therefore does not mean the selection process is harmless. Large positive and negative fitted coefficients can cancel across simulations while producing excessive apparent significance in either direction.

Panel E reports the smallest candidate count large enough that the simulated cutoff exceeds each historical statistic. Under source-calibrated persistence, most thresholds are at most ten candidates. The main exception is the fit statistic for Campbell’s lagged two-month bill-return instrument: with its persistence set to 0.08, the required count exceeds 500. With latent persistence instead fixed at 0.95, the count falls to ten. Its slope-$t$ threshold is much smaller, illustrating again that significance conclusions depend on the statistic.

The paper’s statement that all examined regressions are consistent with mining among only ten candidates refers to the high-persistence scenario. It is not a distribution-free ten-test adjustment or proof about the actual historical number of attempted specifications. The source motivates the search as collective research activity, but the simulation directly models only a particular fixed candidate set and selection rule.

## HAC lag sensitivity and what is not a cure

Simply increasing the maximum lag inspected does not monotonically improve the finite-sample inference. For $T=66$, $q=0.10$, and common persistence 0.98, increasing the inspected residual-autocorrelation range from 12 to 36 changes the simulated critical $t$ from about 2.9 to about 4.8. The estimated standard error becomes noisier, thickening the statistic’s tails. In the historical comparison, the number of previously significant statistics rendered insignificant rises from seven to nine of 17.

At much larger samples and very long bandwidths, the paper reports improvement: with $T=5000$ and 240 lags, the critical value in a $q=0.10$, persistence-0.98 example is 2.23. This is evidence about one larger-sample configuration, not a recommendation to use 240 lags generally. A fixed maximum of 12 lags cannot satisfy an asymptotic condition requiring the bandwidth to grow indefinitely; conversely, increasing it aggressively in a short sample can degrade precision. Both facts can hold at once.

Similarly, taking $T=824$ does not automatically eliminate finite-sample distortion. For high persistence the estimated critical values can be greater than those at $T=66$. This does not prove that a correctly specified, consistently estimated stationary procedure fails asymptotically. The observed comparison uses the paper’s particular truncated, residual-selected HAC estimator and finite parameter grid.

## Replication sequence and missing inputs

A faithful computational experiment first fixes $T$, latent variance, $q$, persistence parameters, and candidate count. It draws stationary initial states, then independent Gaussian innovations, generates the latent and candidate AR paths, and generates next-period returns. Timing is critical: $Z_t$ predicts $r_{t+1}$; replacing it with a contemporaneous or shifted series changes the experiment.

For each replication, fit the candidate regressions with intercepts and calculate their ordinary sample fits. If mining is enabled, retain the regression with the largest fit, then retain *that regression’s* HAC $t$ statistic and slope. For pure regression, retain the sole candidate. After 10,000 independent replications, compute mean slopes, positive signed-$t$ 97.5th percentiles, and fit 95th percentiles. The empirical percentile interpolation convention and random seed should be recorded. A separate symmetry check can justify use of the positive cutoff for a two-sided test.

For historical comparisons, calibrate the reported sample size and persistence for each row and keep all dates, frequencies, and fit definitions visible. For mining, recreate the candidate sampling, differencing, bias adjustment, ordering, and high-persistence transformation before running the return simulations. Adjusted and unadjusted $R^2$ rank same-size univariate regressions identically, but they have different numerical thresholds; that distinction cannot be ignored when matching Table I to simulated cutoffs.

The source does not provide the 500-series list, download vintage, exact historical return variance, underlying observations, all original-data transformations, ADF implementation details, random seed, percentile convention, or HAC finite-sample normalization. It also leaves the zero-signal normalization and singleton high-persistence treatment incompletely specified. The model mechanism and principal critical-value comparisons can be reconstructed from the paper; exact numerical reproduction of every table cannot be certified from these inputs alone.

The design assumes Gaussian homoskedastic innovations, stationary AR(1) states, independent candidate predictors, and a search for the best univariate fit. Real candidate signals can share economic trends, be revised after inspection, or arise from searches over horizons, samples, transformations, and portfolio definitions. Those changes alter the effective search distribution. The source does not quantify them, transaction costs, or implementable out-of-sample portfolio utility.

The appropriate research conclusion is therefore specific. Weak observed return autocorrelation is insufficient protection against a persistent-latent-mean specification error; a HAC label is insufficient protection against a poorly estimated long-run variance; and conventional significance of the selected candidate does not account for how it was chosen. The paper supplies a transparent way to stress those three issues jointly, while preserving the distinction between time variation in expected returns and reliable identification of the instrument that captures it.
