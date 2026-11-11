# The Statistics of Sharpe Ratios

**Andrew W. Lo.** *Financial Analysts Journal* 58(4), July–August 2002, 36–52. Source: [SharpeRatio_Lo_2002.pdf](../../Finance/SharpeRatio_Lo_2002.pdf), the complete 17-page article including Appendix A. Printed page numbers equal PDF page numbers plus 35. Equations, the scale-factor figure, and the empirical table were inspected in their rendered form. Several printed inconsistencies are identified below rather than propagated into an implementation.

## Why this matters

Two investments with the same reported annualized Sharpe ratio can have very different statistical uncertainty and very different annual risk if their monthly returns have different dependence structures. A high ratio estimated from a short, smooth return history need not be precisely measured. Moreover, multiplying a monthly Sharpe ratio by the square root of twelve can exaggerate annual performance when returns are positively autocorrelated. These are separate problems: uncertainty in an estimator, and conversion of its target across holding periods.

Lo's contribution is to put both problems into a common moment-estimation framework. He derives large-sample inference for a one-period Sharpe ratio, extends it to dependent returns, derives a serial-correlation adjustment for time aggregation, and quantifies the extra estimation error from learning the autocovariances. An illustrative sample of mutual funds and hedge funds shows that the adjustment can change rankings markedly. The paper supplies estimators and asymptotic covariance formulas, not a manager-selection trading rule or a claim that Sharpe ratios capture all relevant risks.

The most reusable result is the holding-period conversion

$$
S(q)=\frac{q}{\sqrt{q+2\sum_{k=1}^{q-1}(q-k)\rho_k}}S,
$$

where $S$ is the one-period Sharpe ratio and $\rho_k$ is the return autocorrelation at lag $k$. This formula is exact for the paper's additive return convention. It is an approximation to the Sharpe ratio of compounded simple returns. Estimating the denominator creates uncertainty that must be included when reporting the annualized ratio's standard error.

## Returns, estimands, and the Gaussian benchmark

For a stationary return process $R_t$, let $\mu=E[R_t]$, $\sigma^2=\operatorname{Var}(R_t)>0$, and let $R_f$ be a fixed one-period risk-free rate. The population ratio and sample estimators are

$$
S=\frac{\mu-R_f}{\sigma},\qquad
\widehat\mu=\frac1T\sum_{t=1}^T R_t,\qquad
\widehat\sigma^2=\frac1T\sum_{t=1}^T(R_t-\widehat\mu)^2,
\qquad
\widehat S=\frac{\widehat\mu-R_f}{\widehat\sigma}.
$$

The variance uses divisor $T$, not $T-1$. The empirical application uses monthly simple total returns and a constant benchmark of $5/12$ percent per month. Treating an observed time-varying risk-free rate as fixed in this derivation would change the estimand. If using a varying benchmark, construct the desired excess-return process explicitly and retain its relevant covariance structure.

Under IID Gaussian returns, the joint asymptotic covariance of the sample mean and variance is

$$
V_\theta=
\begin{pmatrix}
\sigma^2&0\\
0&2\sigma^4
\end{pmatrix},\qquad \theta=(\mu,\sigma^2)'.
$$

With $g(\theta)=(\mu-R_f)/\sigma$ and gradient $a=(1/\sigma,-(\mu-R_f)/(2\sigma^3))'$, the delta method gives

$$
\sqrt T(\widehat S-S)\Rightarrow N(0,V_{\rm G}),\qquad
V_{\rm G}=a'V_\theta a=1+\frac{S^2}{2}.
$$

Thus an estimated standard error is $\sqrt{(1+\widehat S^2/2)/T}$, with the usual asymptotic interval $\widehat S\pm1.96\operatorname{SE}(\widehat S)$. Table 1 reports, for example, standard errors of 0.188 for $S=1.5,T=60$ and 0.303 for $S=3,T=60$. Absolute estimation error increases with the ratio; the relative standard error approaches $1/\sqrt{2T}$ as $|S|$ becomes large in this benchmark.

The paper's opening section labels these expressions as applying to IID returns alone. That is too broad. For general IID returns with finite fourth moment, the off-diagonal element is $\nu_3=E[(R_t-\mu)^3]$, and the lower-right element is $\nu_4-\sigma^4$. Consequently,

$$
V_{\rm IID}=1-S\gamma_3+\frac{S^2}{4}(\gamma_4-1),\qquad
\gamma_j=\frac{E[(R_t-\mu)^j]}{\sigma^j},\quad j=3,4.
$$

This qualification follows directly from the article's own general moment matrix in equation (A27); it is also the subject of the separate local Mertens comment. Zero skewness and Gaussian kurtosis recover the opening formula, even without full normality. Independence alone does not imply asymptotic independence of the sample mean and variance. The Gaussian formula should therefore be presented as a benchmark, not a universal IID inference rule.

Lo decomposes Gaussian estimator variance into a mean-estimation share $1/(1+S^2/2)$ and a variance-estimation share $(S^2/2)/(1+S^2/2)$. At $S=0.25$, about 97% comes from the mean; at $S=2$, the mean share is 33.3%; at $S=3$, it is 18.2%. This decomposition has no covariance term only under the stated moment restrictions. In a skewed distribution, separating contributions without the cross term is misleading.

## Dependent returns: a reproducible GMM calculation

For the one-period ratio, form the two-dimensional moment vector

$$
h_t(\theta)=
\begin{pmatrix}
R_t-\mu\\
(R_t-\mu)^2-\sigma^2
\end{pmatrix}.
$$

Solving its sample mean equal to zero gives the same ordinary sample mean and variance. The point estimator has not changed. What changes is its asymptotic covariance. The population moment Jacobian is $H=-I$, and the long-run covariance is

$$
\Omega=\sum_{j=-\infty}^{\infty}E[h_t h_{t-j}'].
$$

Under the joint central limit theorem, $\sqrt T(\widehat\theta-\theta)\Rightarrow N(0,\Omega)$ and the Sharpe-ratio variance is $V=a'\Omega a$. This incorporates autocorrelation of returns, autocorrelation of squared returns, and lagged cross-covariances between returns and squared returns. Zero autocorrelation of returns alone does not remove volatility dependence or make the IID standard error appropriate.

Appendix A imposes stationarity and ergodicity, interior identification, differentiability and moment conditions, plus weak-dependence conditions sufficient for the GMM central limit theorem. Stationarity by itself is not enough. Finite second moments of $h_t$ require finite fourth moments of returns; long-run covariance convergence and the relevant law of large numbers are additional requirements. Structural breaks, nonergodic processes, and sufficiently persistent dependence fall outside an automatic application of these formulas.

Estimate $\Omega$ with the Bartlett-weighted Newey–West construction in equations (A12)–(A14):

$$
\widehat\Gamma_j=\frac1T\sum_{t=j+1}^T
h_t(\widehat\theta)h_{t-j}(\widehat\theta)',\qquad
\widehat\Omega=\widehat\Gamma_0+
\sum_{j=1}^{m}\left(1-\frac{j}{m+1}\right)
(\widehat\Gamma_j+\widehat\Gamma_j').
$$

Then $\widehat V=\widehat a'\widehat\Omega\widehat a$ and $\operatorname{SE}(\widehat S)=\sqrt{\widehat V/T}$. The empirical table uses bandwidths $m=3$ and $m=6$ months. These bandwidths concern the covariance of the moment process; they are not the eleven return autocorrelations needed to form an annual point estimate.

The first line of printed p. 48 states $m/T\to\infty$ as the consistency condition. This is an error and conflicts with the preceding requirement $m\ll T$. The usual growing-bandwidth logic requires $m\to\infty$ and $m/T\to0$, with further rate and dependence conditions. The fixed values three and six are finite-sample choices used by the author, not a proof of consistency across increasing sample sizes.

## Time aggregation and the effect of serial correlation

Define the additive $q$-period return as $R_t(q)=\sum_{j=0}^{q-1}R_{t-j}$ and its benchmark as $qR_f$. Stationarity gives

$$
B_q=\operatorname{Var}[R_t(q)]
=q\sigma^2+2\sum_{k=1}^{q-1}(q-k)\gamma_k,
\qquad \gamma_k=\operatorname{Cov}(R_t,R_{t-k}),
$$

and therefore $S(q)=q(\mu-R_f)/\sqrt{B_q}$. Each lag-$k$ covariance appears $q-k$ times in the off-diagonal variance sum. Dividing $B_q$ by $\sigma^2$ yields the headline autocorrelation adjustment.

When all the relevant autocorrelations vanish, the multiplier reduces to $\sqrt q$. IID sampling is sufficient for this **point-estimate target relationship**, but not necessary: a dependent yet uncorrelated process also has the same additive variance scaling. Its inference can still require a long-run covariance estimator. The article sometimes describes independence as the necessary condition; the exact covariance identity clarifies the weaker requirement.

For compounded simple returns, the exact return is $\prod_{j=0}^{q-1}(1+R_{t-j})-1$, which is not the additive sum. Its moments require more information than these autocovariances. The author explicitly ignores compounding for convenience. Log returns add exactly, but a log-return Sharpe ratio is a different object from a simple-return Sharpe ratio. An implementation should label which target it reports instead of silently switching conventions.

For the illustrative AR(1) process $R_t-\mu=\rho(R_{t-1}-\mu)+\varepsilon_t$, with $|\rho|<1$ and IID innovations, $\rho_k=\rho^k$. The scale factor becomes

$$
\eta(q)=\sqrt q\left[
1+\frac{2\rho}{1-\rho}
\left(1-\frac{1-\rho^q}{q(1-\rho)}\right)
\right]^{-1/2}.
$$

At $q=12$, Table 2 gives 4.17 for $\rho=-0.2$, 3.46 for zero, and 2.88 for $\rho=0.2$. Positive AR(1) dependence raises long-horizon variance and lowers the scale factor; negative dependence does the reverse. The factor is 2.12 for $\rho=0.5$, compared with 5.69 for $\rho=-0.5$. These are scale multipliers, not Sharpe ratios or percentage returns.

The prose at the top of printed p. 42 reverses which Figure 1 curves lie above and below the zero-correlation curve. The equation and Table 2 have the correct direction. More generally, the sign of the first autocorrelation alone cannot determine the adjustment: all $q-1$ weighted autocorrelations matter, and they may have different signs.

## Estimating the aggregated ratio and its uncertainty

The parameter vector now contains $q+1$ components:

$$
\theta_q=(\mu,\sigma^2,\gamma_1,\ldots,\gamma_{q-1})'.
$$

In addition to the mean and variance moments, include $(R_t-\mu)(R_{t-k}-\mu)-\gamma_k$ for every $k=1,\ldots,q-1$. Equation (A17) uses

$$
\widehat\gamma_k=\frac1T\sum_{t=k+1}^T
(R_t-\widehat\mu)(R_{t-k}-\widehat\mu),\qquad
\widehat\rho_k=\widehat\gamma_k/\widehat\sigma^2.
$$

Thus the denominator remains $T$, not $T-k$, and all covariances use the full-sample mean. Replacing these by independently demeaned lagged subsamples changes finite-sample results. Form $\widehat B_q$ and $\widehat S(q)=q(\widehat\mu-R_f)/\sqrt{\widehat B_q}$.

A convenient way to implement the gradient, algebraically equivalent to the intended Appendix A formulas, is

$$
\frac{\partial S(q)}{\partial\mu}=\frac q{\sqrt{B_q}},\qquad
\frac{\partial S(q)}{\partial\sigma^2}
=-\frac{q^2(\mu-R_f)}{2B_q^{3/2}},\qquad
\frac{\partial S(q)}{\partial\gamma_k}
=-\frac{q(q-k)(\mu-R_f)}{B_q^{3/2}}.
$$

These are partial derivatives in a parameterization using **autocovariances**, not autocorrelations. Holding $\rho_k$ fixed while differentiating with respect to $\sigma^2$ would produce a different derivative and would not match the specified moment vector. Equation (A24)'s printed summation begins at $k=2$ in its denominator, omitting lag one; that lower limit must be one, consistently with $B_q$ and neighboring equations.

Estimate the long-run covariance of the augmented moment vector with the same Bartlett procedure and use its quadratic form with this gradient. The result is $\operatorname{SE}[\widehat S(q)]=\sqrt{\widehat V_q/T}$. It is generally wrong to multiply the monthly robust standard error by the estimated annualization multiplier: that omits estimation error in the multiplier and its covariance with the monthly ratio.

For exact software reconstruction, the article supplies the autocovariance normalization but no code resolving every initial-lag boundary convention in the augmented HAC matrix. One transparent implementation computes point moments using the full-sample formulas, evaluates lagged moment vectors on the common block $t=q,\ldots,T$, centers that block when computing its HAC covariance, and documents the resulting boundary choice. This is an asymptotically equivalent implementation choice for fixed $q$, not a claim about the author's undisclosed code. Report whether the covariance denominator uses the original $T$ or the common-block count; the difference can matter in a short sample.

Useful implementation checks follow directly from the model. Setting $q=1$ must recover the two-moment estimator. Setting all autocovariances to zero must recover the $\sqrt q$ point scaling. Numerical finite differences of $q(\mu-R_f)/\sqrt{B_q}$ should match the analytical gradient. A nonpositive estimated $B_q$ or materially negative quadratic-form variance indicates a failed covariance construction or numerical problem and should not be hidden by taking an absolute value.

## Why the more general estimator can be noisier

Even if the true autocovariances are zero, estimating them adds sampling noise. Under IID returns with finite fourth moment, Appendix A gives

$$
V_{\rm robust}(q)
=q\left[1-S\gamma_3+\frac{S^2}{4}(\gamma_4-1)\right]
+qS^2\sum_{j=1}^{q-1}\left(1-\frac jq\right)^2.
$$

The first bracket measures mean and variance uncertainty. The final term is the cost of estimating autocovariances that happen to be zero. The factor $q$ multiplying the first bracket is present in equation (A32), printed p. 50, but missing from main-text equation (25), p. 42. The appendix expression is consistent with the preceding derivatives and the Gaussian special case.

For IID Gaussian returns, divide this variance by the variance of the estimator that imposes zero autocorrelation:

$$
\frac{V_{\rm robust}(q)}{V_{\rm imposed\ IID}(q)}
=1+\frac{2\sum_{j=1}^{q-1}(1-j/q)^2}{1+2/S^2},\qquad
V_{\rm imposed\ IID}(q)=q(1+S^2/2).
$$

Table 3 reports a variance ratio of 3.34 at $S=1,q=12$, and 1.78 at $S=0.5,q=12$. A variance ratio of 3.34 means a standard-error ratio of approximately 1.83, not 3.34. Robustness is useful when its assumptions are needed, but it is not free precision.

Lo suggests the Ljung–Box statistic $Q_{q-1}=T(T+2)\sum_{k=1}^{q-1}\widehat\rho_k^2/(T-k)$ as a diagnostic for whether to estimate the correlation adjustment. The conventional reference is $\chi^2_{q-1}$ under the relevant null regularity conditions. Failure to reject is not proof of independence, and the plain reference distribution is not automatically robust to arbitrary conditional heteroskedasticity. The paper does not analyze post-selection coverage when a diagnostic first chooses which Sharpe estimator to report. A researcher should separate that proposed diagnostic from a guaranteed inferential procedure.

## Empirical design and numerical results

The application is illustrative, not a representative census. The mutual-fund sample comprises the ten largest funds as of February 11, 2001, with CRSP monthly total returns from their individual start dates through June 2000. Histories range from 102 to 450 observations. Selection by a later size ranking can create selection effects; the paper does not attempt a survivorship-neutral reconstruction.

The hedge-fund sample contains twelve funds from Altvest, with monthly returns through December 2000 and at least five years of history. They were deliberately selected to span conventional annualized Sharpe ratios from approximately one to five. Fund names are withheld, and classifications are those supplied by Altvest, not independently verified. This privacy choice prevents an exact security-level reproduction from the article alone. Reported sample lengths range from 72 to 139 months. The paper does not provide the return files, detailed fee conventions, backfill filters, or a dead-fund inclusion rule.

Compute monthly Sharpe ratios using the constant $5/12$ percent monthly benchmark; report the usual $\sqrt{12}$ annualization and the autocorrelation-adjusted annual ratio. Use eleven return autocorrelations for the latter, the $Q_{11}$ diagnostic, and augmented HAC bandwidths three and six for standard errors. All return means and volatilities in Table 4 are percentages per month; Sharpe ratios and standard errors are dimensionless at their stated frequency.

The mutual funds exhibit modest serial dependence: $Q_{11}$ p-values range from 13.2% to 80.2%. Fidelity Magellan has the largest absolute first autocorrelation, 12.4%; its annual ratio changes from 0.73 to 0.66. Washington Mutual Investors changes from 0.60 to 0.65. Vanguard 500 Index changes from 0.72 to 0.85, with robust standard error 0.26 at bandwidth three. Its approximate 95% interval is 0.33–1.36. The source's footnote mentions a 16.0% p-value for Washington Mutual, whereas Table 4 reports 22.8%; the table is used here.

Selected hedge-fund rows show the economic scale:

| Fund style | Months | First autocorrelation | Usual annual ratio | Adjusted annual ratio | Adjusted SE, bandwidth 3 |
|---|---:|---:|---:|---:|---:|
| Convertible/option arbitrage | 104 | 42.6% | 4.35 | 2.99 | 1.04 |
| Relative value | 97 | 25.9% | 4.06 | 3.38 | 1.16 |
| Mortgage-backed securities | 96 | 42.0% | 4.03 | 2.44 | 0.53 |
| Risk arbitrage A | 90 | −4.9% | 3.25 | 3.83 | 0.87 |
| Long–short equities | 138 | −20.2% | 3.19 | 2.32 | 0.35 |
| Multistrategy B | 139 | 49.0% | 1.96 | 1.17 | 0.25 |

For the mortgage-backed fund, the naive annual ratio exceeds the adjusted ratio by about 65%, calculated relative to 2.44. For convertible/option arbitrage, the analogous overstatement is about 45%. Risk arbitrage A moves in the opposite direction and becomes the highest adjusted-ratio fund in this sample. Long–short equities illustrates why the first autocorrelation alone is insufficient: its first lag is negative, but subsequent positive dependence still produces a lower adjusted annual ratio.

Seven of the twelve hedge funds have $Q_{11}$ p-values below 5%. Across all twelve, first autocorrelations range from −20.2% to 49.0%; adjusted annual standard errors at bandwidth three range from 0.25 to 1.16. Bandwidth-six values are generally similar. This limited bandwidth comparison is reassuring for the reported example, but it is not a comprehensive sensitivity study over kernels, tail behavior, structural changes, or database biases.

## Interpretation and limits

The adjustment changes both levels and rankings, but a changed rank does not establish a statistically significant difference between funds. Such a comparison requires the joint covariance of their estimators, including cross-fund return dependence; marginal standard errors alone are insufficient. Likewise, significance relative to a fixed cash benchmark is not evidence of abnormal performance relative to a suitable factor model.

High serial correlation may reflect stale marks, illiquid holdings, smoothing, or genuine dynamics. The estimator incorporates its statistical effect but does not identify the underlying mechanism or establish whether the reported returns were attainable. Manager selection, trading costs, capacity, and liquidation constraints are outside the empirical design. An adjusted ratio can therefore remain economically misleading if the observed return series fails to represent realizable investor payoffs.

The paper's lasting operational lesson is to report the return frequency, aggregation convention, benchmark, covariance assumptions, and uncertainty together. Its robust moment framework makes that possible. Reliable use also requires correcting the printed IID qualification, bandwidth limit, omitted aggregation factor, and derivative index identified above, and recognizing that large-sample inference cannot manufacture information absent from a short or selectively reported history.
