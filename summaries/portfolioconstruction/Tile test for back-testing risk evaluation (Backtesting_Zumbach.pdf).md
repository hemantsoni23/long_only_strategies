# Tile test for back-testing risk evaluation

Gilles Zumbach, Edgelab, July 27, 2020, arXiv:2007.12431v1. This note covers all 22 PDF pages, including the benchmark experiments and all empirical figures. There is no separate appendix in the supplied version.

Source: [Backtesting_Zumbach.pdf](../../Finance/Backtesting_Zumbach.pdf).

## Why this matters

A risk model can produce an acceptable exception count over twenty years while systematically understating risk during a crisis and overstating it afterward. Pooling the whole sample hides the timing error. Zumbach proposes counting probability-integral-transform outcomes in a grid over both time and probability. Excess variation across cells reveals local distributional failures and slow adaptation to volatility changes.

The second contribution is more subtle. A rolling empirical distribution feeds realized observations back into future forecasts. This produces slight negative dependence in transformed outcomes, making their long-window counts look more uniform than independent uniforms. A naive reference distribution can therefore flatter an empirical forecasting method. The paper builds algorithm-specific Gaussian random-walk benchmarks to reproduce that rolling-window effect and overlapping forecast horizons.

This is a univariate density-forecast diagnostic. It is not a portfolio risk aggregator, a measure of the money lost when a forecast is wrong, or a proof that a non-rejected forecasting algorithm is correct.

## Transforming sequential forecasts

For each origin $t$, construct the ex ante return CDF $\widehat F_t$ using information available at $t$, then observe the return over the selected risk horizon $h=\Delta T$. The transformed observation, called a “probtile,” is

$$
z_t=\widehat F_t(r_{t,t+h}).
$$

With a correct continuous conditional CDF and one-step non-overlapping observations, the transforms have the iid uniform property. This is stronger than a uniform pooled histogram: it requires the conditional calibration and dynamics to be right. With daily observations of $h$-day returns, neighboring outcomes overlap for $h>1$, and even correctly modeled transforms are dependent. The reference experiment must preserve this overlap.

Finite empirical CDFs introduce discrete ranks, and price discreteness creates atoms. Exact continuous-uniform claims require corresponding qualifications. The paper handles these practical features with simulated benchmarks and, for illiquid stocks, exclusion of central probability cells. It does not prescribe a universal randomized PIT or a detailed tie-interpolation convention.

Figures 1–3 motivate the procedure using UBS stock over approximately 2002–2020. The paper compares a rolling two-year raw-return distribution with volatility-adjusted historical innovations. The former responds slowly to the financial crisis and the 2020 shock, producing clusters of extreme or central transforms. The latter adapts faster. Figure 1 plots annualized percentage units for returns and risk bands; these axes should not be mistaken for unannualized daily loss magnitudes.

## Exact tile statistic

Partition calendar time from sample start to end into $T_t$ equally long intervals and probability into $T_z$ equal bins. There are $T=T_tT_z$ tiles. Each business-day outcome occupies one time column and one probability bin. Holidays mean that columns need not contain exactly the same number of observations.

For time column $j$, count the number of valid outcomes $N_j$. Under uniformity, each probability bin has expected count $\mu_j=N_j/T_z$. Let $n_{jk}$ be the observed count in probability bin $k$. The statistic is

$$
S=\sigma_{\delta n}
 =\sqrt{\frac1{T_tT_z}\sum_{j=1}^{T_t}\sum_{k=1}^{T_z}
      (n_{jk}-N_j/T_z)^2}.
$$

This is the root mean squared departure of counts from their column-specific expectations, with divisor $T$, not an unbiased sample standard deviation using $T-1$. Replacing $N_j$ by a global average can create artificial departures through holidays or missing data.

At $T_t=1$, the statistic tests the pooled probability histogram. More time divisions test local calibration over shorter intervals. Dynamic failures that average out over the whole history can then produce large $S$. The test retains only the aggregate dispersion for a given grid, however: distinct serial patterns can share the same counts. It is not a complete test of every aspect of serial independence.

As a useful implementation check, under independent uniform transforms and fixed column sizes, multinomial counts give the following derived identity:

$$
E[S^2]=\frac{N}{T_tT_z}\left(1-\frac1{T_z}\right),
\qquad N=\sum_jN_j.
$$

The paper uses Monte Carlo rather than this moment to calibrate rejection. The identity does not apply unchanged after censoring cells or when overlap and adaptive empirical forecasts induce dependence.

The chosen grids fix $T_z=8$ and increase $T_t$ in a geometric progression with ratio $\sqrt2$. Grids range from one full-history column down to short columns retaining at least roughly two points per tile. The figures use tile duration in years on the horizontal axis: short durations are on the left, long durations on the right. The source does not specify the exact rounding rule converting the geometric sequence to integer column counts or every endpoint convention for probability bins.

For low-liquidity and low-price stocks, zero returns and tick increments concentrate transforms around 0.5. The author proposes censoring tiles around this region, using identical censoring in observations and simulations. The exact number of censored bins and adjusted normalization are not specified. Reproducing the reported principal index and FX experiments does not require inventing a stock-censoring policy; replicating the auxiliary stock robustness exercise does require resolving it.

## Monte Carlo calibration

For a selected grid and forecast methodology, simulate 500 reference paths and compute $S^{(1)},\ldots,S^{(500)}$. Form their empirical CDF $G_{MC}$. The reported upper-tail diagnostic is

$$
p=1-G_{MC}(S_{emp}).
$$

Large empirical count dispersion produces a small $p$. The example threshold is 5%. An empirical $p$ from only 500 paths has a raw resolution of about 0.002 and meaningful Monte Carlo uncertainty; a plotted zero means no simulated statistic exceeded it under the implementation, not mathematical impossibility. A production implementation can use a finite-simulation correction, but must disclose that as a change from the source's raw empirical-CDF formula.

Equation 2 averages these diagnostics over instruments: $\bar p=n^{-1}\sum_a p_a$. The text calls individual and average values probabilities that a methodology is correct. That interpretation is not statistically valid. A p-value is a tail probability under a specified null, not a posterior model probability, and the average is not a generally calibrated joint p-value. Instruments are correlated and grids are strongly dependent. Treat the average as descriptive unless a joint reference distribution is explicitly constructed.

For a one-day horizon, the simplest benchmark draws independent uniforms on the same observation calendar. For longer horizons and rolling-window forecasts, the paper instead starts with independent standard-normal daily returns. Form normalized moving sums

$$
y_t^{(h)}=\frac1{\sqrt h}\sum_{\ell=1}^{h}\epsilon_{t+\ell},
\qquad \epsilon_t\sim N(0,1).
$$

These have standard-normal marginals and overlap-induced dependence. All generated forecasts must use only returns available at their origin; inserting part of a future overlapping outcome into its own trailing sample would create look-ahead bias.

Three benchmarks differ in the CDF used for mapping the out-of-sample return:

| Benchmark | Mapping | Required raw sample length for $N$ transformed outcomes |
|---|---|---:|
| 1 | Fixed standard-normal CDF of $y_t^{(h)}$ | $N+h-1$ |
| 2 | Empirical CDF of 500 trailing daily returns, applied to normalized $h$-day outcome | $N+500+h-1$ |
| 3 | Empirical CDF of 500 trailing $h$-day returns, with matching scale | $N+500+2(h-1)$ |

Benchmark 1 is appropriate for a fixed parametric distribution. Benchmark 2 mirrors a rolling daily return or innovation distribution. Benchmark 3 mirrors a rolling distribution constructed at the actual risk horizon. At $h=1$, benchmarks 2 and 3 coincide; benchmark 1 reduces to independent uniforms. At longer horizons all must retain the overlap induced by daily sampling.

These are simplified constant-volatility Gaussian experiments, not full simulations of every estimated LM-ARCH or RiskMetrics model. Their calibration reproduces selected algorithmic features. It should not be assumed to give an exact universal null distribution for every actual financial return law or every estimation procedure.

## Why the adapted benchmark changes results

Suppose an unusually large positive observation arrives. Once it enters the trailing empirical sample, it raises the probability rank assigned to that part of the distribution. Future ordinary outcomes then receive slightly smaller ranks. The corresponding argument holds in the opposite tail and around the center. The rolling sample introduces a weak return toward an evenly occupied probability histogram.

This does not imply better independent forecasting. It is a mechanical dependence effect. On long time tiles, it can substantially reduce count dispersion relative to iid uniforms. Thus values near one under the simple benchmark may signal too little dispersion for that benchmark, rather than excellent predictive information.

The benchmark study uses $N=5,052$ business-day outcomes, $T_z=8$, and $T_t$ from 1 to 256, with intermediate geometric grids. At the finest grid, the expected tile count is about $5052/(8\times256)=2.47$. Figure 5 uses four time columns, approximately five years per column. Benchmark 2's count-dispersion distribution lies markedly below benchmark 1's, with little overlap in their central mass. The plot is a folded empirical CDF, not an estimated probability density: it displays $G$ below 0.5 and $1-G$ above 0.5.

Figures 6–7 show that differences grow when tile durations approach and exceed the 500-day trailing memory, roughly two years. Risk horizons of 1, 2, 5, 10, and 30 days are investigated. The author reports the scale of Monte Carlo fluctuations increasing roughly as $h^{0.25}$ to $h^{0.3}$ in the studied settings, slower than a square-root heuristic. These are numerical observations, not an analytical effective-sample-size theorem. Overlapping data are useful only because their dependence is represented in the benchmark; they do not create independent observations.

The test used for rejection is upper tailed. Consistently near-one p-values could also indicate incompatibility with an iid reference through unusually small dispersion, but the paper's standard rejection rule does not formally reject that side. A two-sided extension would need its own definition and calibration.

## Forecast methodologies being compared

Raw historical-return methods use the previous 500 daily observations. One variant scales daily returns by $\sqrt h$; the other constructs historical returns directly over $h$ days. Their forecast volatility is effectively based on equal weights over the trailing window. A large shock retains the same weight until it abruptly leaves the sample, potentially creating an echo in the forecast.

Innovation methods write

$$
r_{t+1}=\mu_e(t)+\sigma_e(t)\epsilon_{t+1},
\qquad \widehat\epsilon_{t+1}=
 \frac{r_{t+1}-\mu_e(t)}{\sigma_e(t)}.
$$

The conditional scale changes over time while the standardized innovation distribution is assumed comparatively stable. The parametric specifications set $\mu_e=0$. Their cases are original RiskMetrics '94 with exponentially weighted volatility and normal innovations; long-memory ARCH with a Student distribution standardized to unit variance and six degrees of freedom; and LM-ARCH with normal innovations. Six degrees of freedom performs slightly better here than the five used in the cited original LM-ARCH methodology.

The historical-innovation version uses a rolling empirical CDF of 500 standardized innovations and multiplies the resulting scenarios by the current volatility forecast. It is studied both with daily innovations and with innovations constructed at the actual horizon. Although the structural location forecast is zero, an empirical innovation sample can have a nonzero mean. Thus historical innovations can also capture persistent location differences omitted by centered parametric innovations.

The exact LM-ARCH kernel, its parameter values, initialization and multiday conditional-variance recursion are referred to earlier work rather than reproduced here. Likewise the RiskMetrics decay setting is not numerically specified in this PDF. These are missing inputs for an independent recreation of all reported forecast paths; conventional settings should not be silently presented as this paper's exact configuration.

## Empirical design and findings

The main index sample contains ten major stock-index series, January 1, 1993 to April 29, 2020, with 6,614 observations. The FX sample contains six major exchange rates against USD, January 1, 1990 to May 4, 2020, with 7,654 observations. The source does not provide the full instrument lists, data vendor, price-field definitions, corporate-action conventions, holiday alignment, or exact training/burn-in treatment. It reports corroboration on commodity indexes and Swiss stocks without equivalent detailed results or sample definitions.

At one day, Figure 4 compares raw historical returns and historical innovations against iid uniforms. Raw returns are rejected at most time scales; innovations look implausibly good on long tiles. Figure 8 repeats the comparison using the rolling-sample benchmark. Historical returns are then strongly rejected across the displayed index series and tile durations, including full-history tiles; the artificially near-one results for innovations disappear. Historical innovations remain materially better, but adapted-benchmark p-values often become small.

Figures 9–10 compare four model rows for indexes and FX, with the fixed benchmark on the left and the method-adapted benchmark on the right. Original RiskMetrics and centered Student LM-ARCH have poor long-scale diagnostics in many series. The paper attributes part of the shortcoming to fixed centered innovation distributions that cannot reflect instrument-specific features such as equity drift. That explanation is plausible but not separately identified by these aggregate tile statistics.

The text says historical innovations cannot be rejected for most series. This should be read narrowly against the plotted grid and chosen threshold: the adapted panels contain many values near zero, especially for long index tiles. The figures support relative improvement, not universal acceptance at every duration. Exact p-value tables and a familywise rejection rule are absent, so neither exact cross-grid rejection counts nor adjusted significance can be reconstructed reliably from the plots alone.

At ten days, Figures 11–12 add the direct-horizon versions of raw returns and empirical innovations. The clearest improvement is empirical innovations constructed at ten days. For indexes, the daily-innovation variant frequently has weak diagnostics outside the shortest tiles, while direct-horizon innovations retain a broader range of non-negligible p-values. FX shows the same relative ranking, with remaining low values in the adapted benchmark. Direct-horizon raw returns improve some longer-scale comparisons but retain failures at short durations.

No return premium, Sharpe ratio, VaR currency error, or ES error is reported. Plot heights are benchmark tail diagnostics, and should not be converted into percentage improvements in economic risk estimation. The paper also does not give a comprehensive power comparison under a prespecified menu of alternative data-generating processes, despite describing the test as powerful.

## Interpretation and replication priorities

The reproducible core is straightforward: generate properly timed CDF forecasts; compute transforms; count them by time column and probability bin; center using each column's valid observation count; calculate the displayed root mean square; and compare it with a reference experiment matching the horizon and rolling estimation mechanism. Publish a p-value curve across grids rather than selecting only the most favorable duration.

Important unresolved choices are empirical-CDF interpolation and ties, time-grid rounding, exact calendars, LM-ARCH settings, censoring, forecast initialization, and finite-Monte-Carlo tail handling. A careful study would retain tile residual maps to identify the dates and probability regions behind a large aggregate statistic, and accompany them with marginal histograms and serial-dependence diagnostics as the author suggests.

Two broad statements in the paper require restraint. Heteroskedasticity alone does not prove a return process lacks every form of stationarity; a stationary GARCH process can have changing conditional variance. Nor does changing conditional distributions make conditional forecast scoring intrinsically invalid. These distinctions do not remove the useful argument that slow raw-return windows can miss current risk dynamics.

The durable takeaway is to test local calibration and to model the statistical effects of the forecasting algorithm itself. An adapted benchmark is essential to interpreting this paper's comparisons, but its p-values remain conditional diagnostics under simplified reference assumptions, not probabilities that a model is true.
