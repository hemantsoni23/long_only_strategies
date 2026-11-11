# Robust Confidence Intervals for BARRA’s Bias Test of Risk Forecasts

**Gregory Connor, 7 February 2000.** Ten-page technical report on BARRA risk-model quality control. The source credits Scott Scheffler with the original bias test and thanks Nick Herbert for comments.

**Source:** [Connor_  bias test confidence intervals_2000.pdf](<../../Finance/Connor_  bias test confidence intervals_2000.pdf>). All ten pages were read, with the formula and table pages visually checked. References below use PDF/report page numbers.

The library also contains the same ten-page text as [BiasStatistics_Connor_2000.pdf](../../Finance/BiasStatistics_Connor_2000.pdf) and [ConfidenceInterval_Connor_2000.pdf](../../Finance/ConfidenceInterval_Connor_2000.pdf). These are source-file copies of this work, rather than additional papers; normalized full-page extracted text agrees across all three PDFs.

## Why this matters

A risk model can forecast volatility correctly and still produce a realized-to-forecast volatility ratio noticeably different from one in a short evaluation window. A quality-control rule must distinguish genuine calibration error from sampling variability. Connor argues that the conventional normal-return interval can be too narrow when standardized returns have heavy tails, and that noise in the forecasts themselves can create apparent underprediction even when the underlying variance forecast is unbiased.

The report proposes two improvements: use the fourth moment of standardized returns in an asymptotic standard error, or simulate a finite-sample null distribution under an explicit return model. It then adds a stylized model of measurement error in variance forecasts. The central distinction is between bias in the forecast and statistical noise around an unbiased forecast.

The analytical derivation is useful and readily reproducible. The supplied simulation tables, however, contain inconsistencies that prevent treating every printed entry as a validated operational threshold. This note separates the valid formulas, the stated simulation design, the reported numbers, and the checks needed before deploying the tables.

## Statistic, timing, and null hypothesis

For a portfolio, observe returns $r_t$ and volatility forecasts $\sigma_t>0$ for matching periods, $t=1,\ldots,T$. Define standardized outcomes $z_t=r_t/\sigma_t$ and their sample mean $\bar z$. Equation (1) defines the bias statistic as

$$
B_T=\left[\frac1T\sum_{t=1}^T(z_t-\bar z)^2\right]^{1/2}.
$$

The printed denominator is $T$, not $T-1$. That choice matters in finite samples and must be fixed before using a simulated lookup table. Despite its name, the statistic measures dispersion calibration; it is not the sample mean of volatility forecast errors.

The analysis initially assumes zero expected portfolio return and exact risk forecasts, so the standardized outcomes have mean zero and variance one. For genuine forecast validation, the volatility forecast should use information available before the corresponding realized return. The report does not give a particular forecasting lag or model-estimation window because it treats the forecasts as inputs.

Centering by $\bar z$ corrects for a constant standardized mean. Connor notes that this may remove an asset-class premium for excess returns or persistent active performance for active returns. The zero-mean approximation drops this centering term asymptotically. It does not prove that arbitrary time-varying expected returns can be ignored: if the standardized conditional mean changes, its variation can affect the statistic.

If forecast volatility is systematically too high, standardized returns are too small and $B_T$ tends to fall below one. If forecasts are too low, $B_T$ tends to exceed one. Under independence or suitable weak dependence and correct calibration, the law of large numbers gives $B_T\to1$ in probability. A value near one is an aggregate calibration check, not proof that every conditional risk forecast is correct. Errors in different regimes or portfolios can offset.

## Normal-return benchmark

Under IID standard normal $z_t$ and the zero-mean approximation,

$$
B_T^2\approx\frac1T\sum_t z_t^2,\qquad
E[z_t^2]=1,\qquad E[z_t^4]=3.
$$

Therefore $\operatorname{Var}(B_T^2)\approx2/T$. Applying the delta method to the square root at one gives

$$
\sqrt T(B_T-1)\Rightarrow N(0,1/2),\qquad
\operatorname{se}(B_T)\approx\frac1{\sqrt{2T}}.
$$

The report writes normal distributions using the second argument as a standard deviation, rather than the variance convention common in statistical notation. The expressions here use explicit standard errors to avoid that ambiguity.

Approximating the 97.5th standard-normal percentile 1.96 by 2 yields the traditional interval

$$
1\pm\sqrt{\frac2T}.
$$

For 60 monthly observations, the simple standard error is about 0.0913 and the interval is approximately [0.8174, 1.1826]. For 12 observations it is much wider, approximately [0.5918, 1.4082]. These are null acceptance bands for a statistic under calibration, although the source calls them confidence intervals. Constructing a confidence interval for an unknown multiplicative risk-calibration parameter requires a further inversion step.

With IID Gaussian observations and estimated mean, an exact finite-sample benchmark follows from the definition:

$$
TB_T^2\sim\chi^2_{T-1}.
$$

Thus the central 95% acceptance interval for the printed statistic is $[\sqrt{\chi^2_{T-1,.025}/T},\sqrt{\chi^2_{T-1,.975}/T}]$. If one instead uses sample variance with denominator $T-1$, replace the denominator in both endpoints accordingly. If the true zero mean is imposed rather than estimated, the chi-square degrees of freedom also change. These alternatives are close in large samples but appreciably different for one year of monthly data.

The unsquared statistic has a downward Jensen bias even if its squared version is unbiased. For the source’s centered, denominator-$T$ definition,

$$
E[B_T]=\sqrt{\frac2T}\frac{\Gamma(T/2)}{\Gamma((T-1)/2)}.
$$

This derived expression is an independent check on simulation output. It equals about 0.93594 for $T=12$, 0.98744 for $T=60$, and 0.99750 for $T=300$ under exact normality. A degrees-of-freedom correction removes the variance estimator’s bias, but does not remove the square-root statistic’s entire finite-sample bias.

## Fourth-moment correction

Let $\kappa=E[z_t^4]$ denote the raw fourth moment of zero-mean, unit-variance standardized returns. Normality corresponds to $\kappa=3$; excess kurtosis is $e=\kappa-3$. For independent observations,

$$
\operatorname{Var}(z_t^2)=\kappa-1,
$$

and equation (8), p. 4, gives

$$
\operatorname{se}(B_T)\approx\frac{\sqrt{\kappa-1}}{2\sqrt T},\qquad
B_T\approx N\left(1,\frac{\kappa-1}{4T}\right),
$$

where the normal distribution in this display uses variance as its second argument. The normal-return formula is recovered by setting $\kappa=3$. A plug-in estimate is the average fourth power of standardized outcomes under the stated null, with any centering and small-sample convention documented.

The width ratio relative to the conventional normal band is $\sqrt{(\kappa-1)/2}=\sqrt{(e+2)/2}$. With excess kurtosis one, the asymptotic band is about 22.5% wider; with excess kurtosis five, about 87.1% wider. The correction therefore becomes economically relevant before tails become extremely heavy.

This adjustment needs a finite fourth moment and a central limit theorem for squared standardized outcomes. It does not make the procedure robust to arbitrary infinite-variance squared returns or unmodeled serial correlation. With persistent squared standardized returns, a natural extension would replace $\kappa-1$ by their long-run variance,

$$
\Omega=\sum_{j=-\infty}^{\infty}\operatorname{Cov}(z_t^2,z_{t-j}^2),\qquad
\operatorname{se}(B_T)\approx\frac{\sqrt\Omega}{2\sqrt T}.
$$

That HAC-style expression is an implementation extension derived from the same delta argument, not an estimator specified or tested in this report. Connor’s explicit Monte Carlo experiment uses independent mixture draws. Estimating kurtosis in a short sample can itself be unstable, especially when one or two observations dominate the fourth moment.

## Finite-sample mixture-of-normals experiment

The proposed simulation uses a zero-mean mixture of two normal distributions. Each month comes from the high-variance component with probability 20% and the low-variance component with probability 80%. Relative component variances are calibrated to achieve chosen excess kurtosis while maintaining unit unconditional variance. This stylizes occasional high-volatility months without assuming the overall return distribution is normal.

The prose on p. 5 lists excess kurtosis values 0, 0.5, 1, and 5; Table 1 additionally contains 2. The table’s sample lengths are 12, 24, 36, 48, 60, 120, 180, 240, and 300 months. Connor reports 10,000 simulations per sample case and more than 50 million simulated returns overall. Central 90%, 95%, and 99% interval endpoints are tabulated.

The report does not print component variances, but they can be derived. Let the high-state probability be $p=0.2$, with variances $v_H$ and $v_L$, and let $\Delta=v_H-v_L$. Unit unconditional variance and the fourth moment of a normal mixture imply

$$
v_L=1-p\Delta,\qquad v_H=1+(1-p)\Delta,\qquad
e=3p(1-p)\Delta^2.
$$

Thus $\Delta=\sqrt{e/[3p(1-p)]}$. The resulting variance pairs are approximately (0.79588, 1.81650) at excess kurtosis 0.5; (0.71132, 2.15470) at one; (0.59175, 2.63299) at two; and (0.35450, 3.58199) at five. These are variances, so square-root them when scaling standard normal draws. They are reconstructed calibration inputs consistent with the stated model, not separately published estimates.

For every simulation, draw a component indicator independently for each month, draw its normal outcome, compute the same declared bias statistic as in the data, and store it. Sort the 10,000 statistics and extract quantiles. The random seed, quantile interpolation convention, exact centering treatment, and actual program are not provided. Consequently, reproductions should report Monte Carlo uncertainty rather than expect every rounded endpoint to match exactly.

Selected Table 1 central 95% bands show the reported tail effect:

| Excess kurtosis | T = 12 | T = 60 | T = 300 |
|---:|---:|---:|---:|
| 0 | [0.590, 1.417] | [0.824, 1.181] | [0.920, 1.080] |
| 0.5 | [0.570, 1.468] | [0.807, 1.210] | [0.914, 1.090] |
| 1 | [0.552, 1.521] | [0.793, 1.225] | [0.904, 1.101] |
| 2 | [0.524, 1.581] | [0.768, 1.256] | [0.887, 1.113] |
| 5 | [0.435, 1.731] | [0.688, 1.336] | [0.853, 1.152] |

These are source-reported intervals, not newly validated quantiles. They support the qualitative conclusion that tail thickness broadens the sampling distribution and makes it asymmetric in short samples.

## Forecast measurement error changes the null

The first analysis treats forecast volatility as exactly correct each month. Section 4 considers a weaker null in which the forecast contains measurement error. A ratio of independent estimated variances has an F-type distribution; because the reported statistic averages period-specific standardized outcomes and then takes a square root, it is not itself simply an F variate.

To express the stated model unambiguously, distinguish true volatility $\sigma_t$ from forecast $\hat\sigma_t$ and define $V_t=\hat\sigma_t^2/\sigma_t^2$. The intended variance-estimation specification on p. 8 is

$$
60V_t\sim\chi^2_{60},
$$

independent of the corresponding return shock. If $r_t=\sigma_t z_t$, the realized standardized outcome becomes $z_t/\sqrt{V_t}$. A reproduction must also state whether the forecast errors are independent over time; the text motivates independent numerator and denominator error but supplies no rolling-window dependence model.

This model has $E[V_t]=1$: variance forecasts are unbiased. Nevertheless, the inverse variance is convex, so

$$
E[V_t^{-1}]=\frac{60}{58}>1.
$$

With independent correctly standardized returns and an appropriate law of large numbers, the squared bias statistic tends to $60/58$, and the statistic itself tends to approximately 1.01710. Thus an apparent upward calibration ratio can arise solely from dividing by noisy unbiased variance estimates. Unbiased variance, unbiased volatility, and unbiased inverse variance are different properties.

The report says the correction primarily raises the upper rejection threshold and can otherwise generate false evidence of underforecasting. Selected Table 2 bands are:

| Excess kurtosis as labeled | T = 12 | T = 60 | T = 300 |
|---:|---:|---:|---:|
| 0 | [0.595, 1.534] | [0.844, 1.265] | [0.959, 1.147] |
| 1 | [0.556, 1.658] | [0.820, 1.328] | [0.942, 1.173] |
| 2 | [0.527, 1.715] | [0.791, 1.344] | [0.928, 1.184] |
| 5 | [0.607, 1.527] | [0.850, 1.265] | [0.963, 1.148] |

The final row is reproduced to expose a source problem, not endorse it: its near-normal widths contradict the expected direction of the large increase in kurtosis. The discrepancy cannot be repaired just by choosing a different random seed.

## Material source inconsistencies

Several checks are required before using the printed lookup tables in model governance.

First, Table 1’s rows labeled “average value” do not match the stated statistic under the normal null. They give 0.813, 0.925, and 0.967 at 12, 60, and 300 months, respectively. The exact means for equation (1) are approximately 0.93594, 0.98744, and 0.99750. A denominator-$T-1$ correction would move the means slightly upward, not down to the printed values. Their meaning or computation is unresolved in the supplied report.

Second, the normal-case interval endpoints look closer to a degrees-of-freedom-adjusted statistic than to the denominator-$T$ equation. At $T=12$, the exact central 95% interval for the printed equation is approximately [0.56390, 1.35154], whereas the table reports [0.590, 1.417]. This suggests a convention mismatch, although without code it does not identify its exact cause.

Third, the p. 8 claim that 60-degree variance-estimation noise gives a relative volatility standard deviation of 0.0645 conflicts with the delta method. Under the stated chi-square model the approximate value is $1/\sqrt{2\times60}=0.0913$. The number 0.0645 corresponds to approximately 120 degrees of freedom under that calculation. It is not possible to know from the PDF which specification generated Table 2.

Fourth, Table 2’s panel labeled excess kurtosis five is strikingly close to its normal panel and narrower than the panels for excess kurtosis one and two. The report does not explain this reversal. The panel should be treated as unresolved numerical output rather than an operational heavy-tail interval.

Fifth, the p. 7 prose briefly says intervals are “too wide” while its argument concerns conventional intervals being too narrow. Its interpolation footnote also mislabels an upper endpoint as lower and reverses distance weights. For endpoints $a$ at $T_0$ and $b$ at $T_1$, correct linear interpolation is $(1-w)a+wb$ with $w=(T-T_0)/(T_1-T_0)$. Interpolation cannot fix an inconsistent underlying table.

These checks do not invalidate the fourth-moment derivation or the inverse-variance measurement-error mechanism. They do limit numerical reuse of the historical tables until the simulation is rerun under fully specified conventions.

## Replication and practical interpretation

A transparent implementation should begin by fixing the statistic: centered versus known-zero mean, denominator $T$ versus $T-1$, active versus excess returns, forecast horizon, and information lag. It should first reproduce the exact Gaussian chi-square benchmark. Only then should it add the mixture distribution, confirming unit variance and target fourth moment numerically, and finally the independent forecast-error model with a declared number of degrees of freedom.

For each stage, store the mean, variance, and central quantiles of the statistic and compare them with analytical limits. Report a seed and a quantile convention. Use the same centering and denominator in the real evaluation and simulations. If the real model uses overlapping estimation windows or returns show persistent standardized squared shocks, dependence must be modeled or estimated; independent draws no longer reproduce that null.

The report supplies no portfolio-return dataset, actual BARRA model specification, empirical rejection rate, cross-portfolio multiple-testing correction, or code. Its results are a proposed calibration framework with stylized simulation evidence. A value outside a correctly constructed interval is evidence against the chosen null, which includes both risk calibration and distributional assumptions. It does not automatically identify a specific factor-model defect.

The substantive lesson is that risk-forecast evaluation needs its own uncertainty model. Heavy tails affect the variance of squared standardized returns; finite samples affect the shape and centering of the statistic; and noisy denominators can create systematic upward ratios. These mechanisms should be reproduced directly, with the documented source discrepancies resolved, before turning the bias statistic into a pass/fail rule.
