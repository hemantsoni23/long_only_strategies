# Extreme Correlation of International Equity Markets

François Longin and Bruno Solnik. *Journal of Finance* 56(2), April 2001, pp. 649–676. Source: [ExremeEquityCorrelation_LonginSolnik_2001.pdf](../../Finance/ExremeEquityCorrelation_LonginSolnik_2001.pdf). The filename's spelling is retained exactly. All 28 pages, four tables, four figures, and both appendices were read. Journal page 649 is PDF page 1. The note reconstructs the censored likelihood and distinguishes the paper's dependence parameter from a raw-return Pearson correlation.

## Why this matters

A portfolio can look internationally diversified in ordinary conditions and lose that diversification during a common drawdown. Testing this proposition is harder than comparing correlations computed in calm and volatile subsamples. Selecting observations using realized returns changes the conditional distribution, and therefore changes its correlation even when the original return-generating process has a constant correlation.

The paper's first contribution is to make that selection effect part of the null hypothesis. Its second is to distinguish large negative returns from large positive returns. The empirical result is asymmetric: estimated dependence in negative tails is substantially greater than the Gaussian benchmark, whereas positive-tail behavior is much closer to that benchmark. The relevant pattern is common downside rather than an undifferentiated category of large absolute returns.

The method combines generalized Pareto marginal tails with a parsimonious logistic dependence function and a censored likelihood. It uses all months to estimate probabilities of entering the tails while allowing the non-tail return values themselves to be discarded. That is different from calculating an ordinary sample correlation using only months when both markets cross a threshold.

The paper does not construct a trading strategy or solve an optimal portfolio problem. It supplies evidence that a risk model should reproduce the observed asymmetry. It does not determine how much international diversification an investor should abandon, how to forecast the next crisis, or what risk premium compensates for this dependence.

## Selection changes correlation even under the null

The introductory example is a bivariate normal pair with zero means, unit variances, and unconditional correlation 0.50. Split observations at the median absolute value of the first return, approximately 0.674. Conditional correlation is about 0.21 for the smaller absolute returns and 0.62 for the larger ones. Neither number indicates a change in the underlying correlation parameter; both follow from selection in a distribution whose parameter is fixed at 0.50.

For one-variable conditioning, this can be reconstructed by writing $Y=\rho X+\sqrt{1-\rho^2}\epsilon$, with independent standard-normal $X,\epsilon$. In a selected set $A$ depending on $X$ alone,

$$
\operatorname{Corr}(X,Y\mid A)
=\frac{\rho\sqrt{\operatorname{Var}(X\mid A)}}
{\sqrt{\rho^2\operatorname{Var}(X\mid A)+1-\rho^2}}.
$$

The selection changes the variance of $X$, which mechanically changes the correlation. This derivation is an explanatory reconstruction of the source's example, not a new empirical result.

Signed-tail conditioning is different. For a bivariate Gaussian with correlation strictly between minus one and one, very high joint upper exceedances become asymptotically independent in the extreme-value sense. The paper illustrates decreasing signed-exceedance correlations with a Gaussian pair whose original correlation is 0.80: approximately 0.48, 0.36, 0.24, and 0.14 at thresholds one, two, three, and four standard deviations above the mean. Lower tails have the corresponding symmetric behavior.

Two-sided selection on absolute returns retains both large positive and large negative observations and can produce the opposite pattern. A valid test must fix the conditioning event, centering convention, and statistic before constructing its null distribution. “Correlation in crises” is not a single well-defined estimand without those choices.

## Marginal tails and support

For a return $R$, choose an upper-tail threshold $u$ and tail probability $p=P(R>u)$. Conditional excesses are modeled by a generalized Pareto distribution. With scale $s>0$ and shape $\xi$,

$$
G_u(x)=1-\left(1+\xi\frac{x-u}{s}\right)^{-1/\xi},
\qquad x\geq u,\quad 1+\xi(x-u)/s>0.
$$

The continuous limit at $\xi=0$ is $1-\exp[-(x-u)/s]$. Positive $\xi$ gives a power tail; negative $\xi$ gives the finite upper endpoint $u-s/\xi$. Negative shape does not mean the distribution has no probability beyond the selected threshold; it means the remaining tail ends at a finite point.

The exponent in printed equation (1), page 652, lacks the required minus sign. Equation (5) and the intended probability interpretation use $-1/\xi$, as written here. The positive exponent would make the alleged CDF negative for a positive shape and a positive excess. A numerical implementation must also enforce support rather than blindly raise a negative base to a fractional power.

The upper portion of the unconditional marginal CDF is

$$
F_i(x)=1-p_i\left(1+\xi_i\frac{x-u_i}{s_i}\right)^{-1/\xi_i},
\qquad x\geq u_i,
$$

with $F_i(u_i)=1-p_i$. Below $u_i$ only the probability of being below the threshold is retained. Its density above the threshold is

$$
f_i(x)=\frac{p_i}{s_i}
\left(1+\xi_i\frac{x-u_i}{s_i}\right)^{-1/\xi_i-1}.
$$

The lower tail is handled by reversing signs, so losses become positive extremes. This transformation should be applied consistently to returns, thresholds, and interpretation of the final reported sign. The empirical thresholds in the paper are deviations from each country's sample mean, not common raw-return cutoffs or common volatility multiples.

Extreme-value theory motivates the GPD approximation under the appropriate domain-of-attraction and dependence conditions. It does not assert that every finite-threshold financial tail is exactly GPD. Also, the paper's broad statement that GARCH tails have $\xi<0.5$ requires parameter and moment restrictions: finite second moments correspond to that inequality for a regularly varying GPD tail; it is not automatic for every GARCH specification.

## Logistic dependence and the meaning of its reported correlation

For transformed marginal coordinates $z_i=-1/\log F_i(x_i)>0$, the source uses the logistic exponent function

$$
D_\alpha(z_1,z_2)
=\left(z_1^{-1/\alpha}+z_2^{-1/\alpha}\right)^\alpha,
\qquad 0<\alpha\leq1.
$$

The bivariate CDF on the modeled upper-tail region is

$$
H(x_1,x_2)=\exp[-D_\alpha(z_1,z_2)].
$$

At $\alpha=1$, $H=F_1F_2$, so the coordinates are independent. As $\alpha$ tends to zero, the construction approaches complete positive dependence. The symmetric logistic family permits one positive dependence parameter and is a modeling choice, not a uniquely determined multivariate implication of extreme-value theory. It does not represent negative tail association or arbitrary directional asymmetry within a fitted pair. Lower and upper tails are fitted separately to permit the main sign asymmetry.

The paper reports

$$
\rho_L=1-\alpha^2
$$

as its correlation of extremes. This is a dependence reparameterization associated with the logistic extreme-value model. It should not be equated without qualification to Pearson correlation of raw exceedance returns with arbitrary GPD margins. Pearson correlation changes under nonlinear marginal transformations, whereas $\alpha$ is a copula parameter. The familiar $1-\alpha^2$ correlation identity belongs to the standardized Gumbel-margin representation. A raw-return correlation requires integrating the fitted marginal transforms and may not exist when second moments do not exist.

This distinction matters for replication of the Gaussian comparison. Estimate the same dependence statistic from simulated Gaussian samples as from the observed samples, or explicitly document a different mapping. Comparing an ordinary Gaussian conditional Pearson correlation directly to a logistic copula parameter can compare different estimands. The article calls both quantities correlation without fully documenting the simulation-to-parameter mapping, so exact replication of that part requires care beyond copying the numerical labels.

For interpretation, the logistic upper-tail-dependence coefficient is $\chi=2-2^\alpha$. This relation follows by evaluating the copula on equal high marginal quantiles; it is a useful derived diagnostic, not a statistic tabulated in the paper. It confirms that $\alpha<1$ represents asymptotic dependence in this family, while Gaussian dependence with any nonperfect correlation has $\chi=0$. At finite thresholds a Gaussian sample can nevertheless produce a positive fitted dependence parameter.

## Censored likelihood: an implementable form

There are seven fitted parameters for each country pair and each sign/threshold specification:

$$
\vartheta=(p_1,p_2,s_1,s_2,\xi_1,\xi_2,\alpha).
$$

Every month falls into one of four regions according to whether each return exceeds its own threshold. If neither exceeds, its contribution is $H(u_1,u_2)$. If only the first exceeds, it contributes $\partial_1H(x_1,u_2)$. If only the second exceeds, it contributes $\partial_2H(u_1,x_2)$. If both exceed, it contributes the joint density $\partial_{12}H(x_1,x_2)$. Do not discard the first three regions: they contain information about occurrence probabilities and joint non-exceedance.

A convenient reconstruction avoids the sign and derivative-notation ambiguities in Appendix 2. Define

$$
a_i=-\log F_i(x_i),\qquad q_i=\frac{f_i(x_i)}{F_i(x_i)},
\qquad h(a_1,a_2)=(a_1^{1/\alpha}+a_2^{1/\alpha})^\alpha.
$$

Then $H=e^{-h}$, $da_i/dx_i=-q_i$, and, with $A=a_1^{1/\alpha}+a_2^{1/\alpha}$,

$$
h_i=A^{\alpha-1}a_i^{1/\alpha-1},
$$

$$
h_{12}=\frac{\alpha-1}{\alpha}
A^{\alpha-2}a_1^{1/\alpha-1}a_2^{1/\alpha-1}.
$$

Thus the four likelihood pieces are

$$
L_{00}=e^{-h},\qquad L_{10}=e^{-h}h_1q_1,
\qquad L_{01}=e^{-h}h_2q_2,
$$

$$
L_{11}=e^{-h}(h_1h_2-h_{12})q_1q_2.
$$

For a censored coordinate evaluate its $a_i$ at $u_i$ and omit its density/Jacobian factor. These expressions are derivatives of the stated CDF, not a different likelihood. At independence they reduce respectively to $(1-p_1)(1-p_2)$, $f_1(x_1)(1-p_2)$, $(1-p_1)f_2(x_2)$, and $f_1(x_1)f_2(x_2)$, providing straightforward unit checks.

Maximize the sum of log contributions subject to $0<p_i<1$, $s_i>0$, $0<\alpha\leq1$, and all observed support restrictions. Use log-domain evaluation and an explicit $\xi\to0$ branch to avoid cancellation. The authors first fit each marginal separately, then initialize the bivariate maximization from the marginal estimates and sample unconditional correlation. The PDF does not specify optimization software, stopping tolerances, Hessian method, failed-start handling, or regularization near the independence boundary.

Appendix 2 assumes independence across time and fixed thresholds independent of returns and time. This is stronger than the broad introductory discussion of dependent-process extreme-value limits. Serially dependent monthly tail occurrences and thresholds selected from the same data can affect uncertainty. The reported standard errors do not document an adjustment for those issues; a block bootstrap or threshold-selection bootstrap would be an additional robustness analysis, not the published method.

## Dataset and threshold selection

The data are monthly MSCI equity-index returns for the United States, United Kingdom, France, Germany, and Japan, January 1959 through December 1996: 456 months. The study fits four pairs, each containing the United States. It does not fit all ten country pairs or a single five-dimensional covariance model. Detailed index construction is referred to an earlier Longin–Solnik article. Currency denomination, dividend treatment, index-vintage changes, and missing-value handling are not fully specified in this PDF and must be recovered before claiming exact replication.

The fixed threshold offsets from each market's empirical mean are 0, 3, 5, 8, and 10 percentage points, applied separately above and below the mean. Return scale is therefore percentage points: a 5% offset is five points in the tabulated scale. If returns are coded as decimals, scale parameters and thresholds must be divided by 100 while shape and dependence parameters stay unchanged.

Appendix 1 selects additional thresholds through a Monte Carlo calibration:

1. For each Student-$t$ degree of freedom $k=1,\ldots,10$, simulate 1,000 independent series of length 456. Its tail index is $1/k$.
2. For tail counts from approximately 1% to 20% of 456, estimate the tail index for every simulated series and compute its mean squared error relative to $1/k$.
3. Select $n^*(k)$ minimizing that MSE. The reported examples are 64 exceedances for $k=1$ and 25 for $k=5$.
4. On the actual return series, estimate the tail index using each candidate $n^*(k)$. Choose the candidate whose estimate is statistically closest to $1/k$, using the p-value of that equality test. Translate its chosen count into an observed order-statistic threshold.

This calibrates a threshold for estimating a marginal tail index under Student reference models, not necessarily the threshold minimizing error in joint dependence or portfolio loss. Seeds, integer rounding, tie rules, and the exact finite-sample standard-error calculation for the matching test are unreported.

The displayed MSE decomposition on page 672 contains a centering error. The correct identity is

$$
\frac1S\sum_s(\widehat\xi_s-\xi)^2
=(\overline\xi-\xi)^2
+\frac1S\sum_s(\widehat\xi_s-\overline\xi)^2.
$$

The printed second term instead centers at the truth, double-counting squared bias. A replication should minimize the left-hand MSE or the correctly decomposed expression; the PDF does not establish which expression the authors' code used.

The chosen negative offsets are −6.12% for the US, −9.68% UK, −8.38% France, −7.84% Germany, and −8.53% Japan. Corresponding negative-tail counts are 25,16,18,16,16. Positive offsets are +7.21% US, +6.70% UK, +9.90% France, +9.01% Germany, and +10.27% Japan. The US positive tail uses 18 observations. The country-specific thresholds should not be replaced by a common 5% quantile without changing the experiment.

## Numerical results and the appropriate null

The reported optimal-threshold dependence estimates are:

| Pair | Negative-tail $\rho_L$ (SE) | Positive-tail $\rho_L$ (SE) | Finite-Gaussian LR p-value, negative | Finite-Gaussian LR p-value, positive |
|---|---:|---:|---:|---:|
| US–UK | 0.578 (0.121) | 0.226 (0.120) | 0.032 | 0.434 |
| US–France | 0.652 (0.103) | 0.116 (0.105) | <0.001 | 0.405 |
| US–Germany | 0.482 (0.124) | 0.078 (0.104) | 0.018 | 0.390 |
| US–Japan | 0.311 (0.117) | 0.077 (0.099) | 0.077 | 0.675 |

These are the final rows of Tables I–IV. Negative-tail dependence exceeds positive-tail dependence in all four pairs; their cross-pair averages are approximately 0.505 and 0.124. The article reports that the difference is significant at 5% for UK, France, and Germany. For UK the calculation assumes independent upper- and lower-tail estimates and gives $t=2.066$, p=0.039. That independence is an assumption, not something implied merely because the selected tail observations are disjoint.

For US–UK, the ordinary unconditional correlation is 0.519. Negative-tail fitted dependence is 0.530 at the mean threshold, 0.579 at −3%, 0.553 at −5%, 0.600 at −8%, and 0.676 at −10%. The prose on page 666 incorrectly attaches 0.553 to −10%; Table I and Figure 1 place it at −5%. The tendency increases toward the far negative tail but is not monotone at every intermediate threshold.

Positive-tail US–UK estimates are 0.415,0.353,0.360,0.293,0.189 at 0,+3,+5,+8,+10%. The finite-Gaussian benchmark described in the text is approximately 0.51,0.44,0.39,0.29,0.21. Thus the positive-tail estimates approach that benchmark, while downside estimates depart upward. Figures 1–4 depict this comparison for all four pairs; they are threshold-response plots, not time-series forecasts of future correlation.

The distinction between two nulls is essential. An asymptotic null sets extreme Gaussian dependence to zero. A finite-threshold null simulates Gaussian returns with means and covariance equal to sample estimates and uses the expected statistic at the actual threshold. For US–UK at −5%, the asymptotic LR statistic is 73.143, whereas the finite-threshold LR statistic is only 5.243, p=0.022. The corresponding signed Wald statistics are 7.681 and 2.236, with the latter p=0.025. Ignoring finite-threshold Gaussian dependence vastly exaggerates the rejection.

At the optimal thresholds, Japan is a material qualification: the negative-tail finite-Gaussian LR p-value is 0.077 and the Wald p-value 0.131. It is not a 5% rejection there. At −10%, however, the Japanese-pair LR p-value is 0.007 and Wald p-value 0.032. At +3%, the German positive-tail test rejects with LR p=0.029, whereas its more extreme positive-tail specifications do not. The broad conclusion is supported primarily by the pattern across high signed thresholds; it should not be restated as every negative specification rejecting and every positive specification accepting.

The tables label their signed z-like statistics “W test”; they are not already squared chi-square Wald statistics. The independence null $\rho_L=0$ is also a parameter boundary. Conventional asymptotic LR and Wald reference laws require care there, and the article does not supply a separate boundary-calibrated bootstrap. The finite-threshold reference can be interior, but its simulated benchmark and estimated Gaussian parameters add uncertainty that is not fully documented.

## Limits of the interpretation and a replication sequence

The marginal shape estimates are imprecise. For example, Table I's −10% US shape estimate is 0.672 with SE 0.697; such a point estimate would not have a finite second moment if taken literally as a complete GPD tail. This reinforces why the fitted dependence index should not be casually interpreted as a precisely estimated raw-return covariance. The authors themselves avoid strong conclusions about the signs of the tail indices.

Large thresholds leave very few extremes and only a subset are simultaneous. The censored likelihood extracts information from all four event categories, but cannot create observations absent from the data. Using many thresholds and four pairs also creates multiple-testing and selection considerations not addressed by a simultaneous confidence procedure in the paper.

The finding concerns joint signed tails in a historical monthly distribution. “Bear market” here is an interpretation of large negative observations, not an independently estimated persistent state available before the return is realized. The evidence therefore does not prove that an ex ante volatility signal is useless, nor identify a causal driver of correlation. It rejects some symmetric benchmarks and constrains useful joint return models.

The authors discuss constant-correlation GARCH and asymmetric GARCH simulations as inadequate to reproduce their pattern. The PDF provides no complete calibration or simulation output for those claims. They should not be converted into a theorem rejecting every possible multivariate GARCH model. Regime-switching models can potentially match the asymmetry, but their portfolio consequences depend on their full dynamics, risk aversion, and transition probabilities, none estimated here.

To reproduce the main analysis, first recover the precise monthly index definitions and align all 456 dates. Center each series using the full-sample mean used by the original design. Fit the two marginal tails and then the seven-parameter censored model for each pair, sign, and fixed threshold. Verify support, likelihood contributions, boundary solutions, and the independence special case. Repeat with the Monte Carlo-selected country-specific thresholds, preserving the selection procedure.

Next generate the Gaussian comparison using the same marginal units, selection events, and dependence estimator. Report simulation size and Monte Carlo error, which are missing from the PDF's finite-null description. Reproduce the tabulated parameter estimates, standard errors, likelihood-ratio comparisons, and signed Wald statistics before considering robustness to serial dependence or threshold selection. Those later checks should be identified as extensions.

The practical result is a specification target: a joint equity model should permit much stronger common downside than common upside without mistaking conditioning artifacts for changing structural correlation. The paper's tail-model approach makes that question estimable, while its short sample of extremes, dependence-family restriction, and several implementation ambiguities limit how literally its numerical parameters should be used for portfolio sizing.
