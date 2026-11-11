# Comments on Variance of the IID Estimator in Lo (2002)

**Elmar Mertens, November 2002.** Research comment, University of Basel. Source: [SharpeRatio_Mertens_2002.pdf](../../Finance/SharpeRatio_Mertens_2002.pdf), 17 pages including the complete MATLAB appendix, four numerical tables, and the simulation figure. PDF and printed page numbers coincide. This note concerns Mertens's correction to Lo's IID sampling-variance calculation, a distinct contribution from Lo's original treatment of serial dependence and annualization.

## Why this matters

A Sharpe ratio is an estimated nonlinear function of the mean and volatility. Even when returns are independent over time, its uncertainty depends on the third and fourth moments of the return distribution. Independence does not make the sample mean and sample variance asymptotically uncorrelated when the distribution is skewed. Nor does independence force the sampling variance of the variance estimator to equal its Gaussian value. Ignoring these two facts can make confidence intervals materially too narrow or too wide.

Mertens isolates this error in the opening IID calculation of Lo (2002), gives the corrected asymptotic variance, and shows its quantitative implications using rounded moments of Fama–French factor returns and a lognormal Monte Carlo experiment. This is a correction to an inference formula, not a new portfolio strategy or a claim that the Sharpe ratio completely measures investment risk. It does not remove the need to account for serial dependence in actual fund returns. Its practical contribution is a compact formula that can be implemented directly and used as a diagnostic against a Gaussian shortcut.

The central result is

$$
V_S=1-S\gamma_3+\frac{S^2}{4}(\gamma_4-1)
=1+\frac{S^2}{2}-S\gamma_3+\frac{S^2}{4}(\gamma_4-3),
$$

where $S$ is the population Sharpe ratio, $\gamma_3$ is skewness, and $\gamma_4$ is ordinary kurtosis. The standard error of the estimated Sharpe ratio is approximately $\sqrt{V_S/T}$. $V_S$ itself is the variance of the limiting distribution of $\sqrt T(\widehat S-S)$, not the finite-sample variance of $\widehat S$.

## Estimand, normalization, and assumptions

Let $R_t$ be IID returns, $\mu=E[R_t]$, and $\sigma^2=E[(R_t-\mu)^2]>0$. The risk-free rate $R_f$ is fixed at the return sampling frequency. Define

$$
S=\frac{\mu-R_f}{\sigma},\qquad
\widehat\mu=\frac1T\sum_{t=1}^T R_t,\qquad
\widehat\sigma^2=\frac1T\sum_{t=1}^T(R_t-\widehat\mu)^2,
\qquad
\widehat S=\frac{\widehat\mu-R_f}{\widehat\sigma}.
$$

The denominator uses $T$, as in the paper's moment estimator and MATLAB `std(data,1)`. Replacing it with $T-1$ changes finite-sample values but not the stated first-order asymptotic limit. A faithful numerical reproduction should retain the $T$ convention.

A finite fourth central moment is needed for the joint central limit theorem for the mean and variance. The phrase “any non-normal IID distribution” must be read subject to that moment requirement and a nonzero variance. Heavy-tailed distributions with infinite fourth moment are outside this result even if their mean and variance exist. The derivation also treats the benchmark rate as fixed; an estimated or stochastic benchmark requires applying the calculation to a consistently defined excess-return series or augmenting the joint moment system.

Use ordinary, not excess, kurtosis in the first expression for $V_S$:

$$
\gamma_3=\frac{E[(R_t-\mu)^3]}{\sigma^3},\qquad
\gamma_4=\frac{E[(R_t-\mu)^4]}{\sigma^4}.
$$

If software returns excess kurtosis $\kappa=\gamma_4-3$, the corresponding term is $S^2\kappa/4$ added to $1+S^2/2$. Confusing these conventions introduces a systematic error. All ratios here are at the input data frequency; monthly Sharpe ratios must not be confused with annualized Sharpe ratios when inserted into a formula whose $T$ counts months.

## Derivation through the joint moment estimator

Sections 1–2, pp. 3–6, estimate $\theta=(\mu,\sigma^2)'$ using exactly identified moment conditions

$$
H_t(\theta)=
\begin{pmatrix}
R_t-\mu\\
(R_t-\mu)^2-\sigma^2
\end{pmatrix},\qquad
\frac1T\sum_t H_t(\widehat\theta)=0.
$$

The population Jacobian is $D=E[\partial H_t/\partial\theta']=-I$. The off-diagonal derivative in the second row averages to zero because $E[R_t-\mu]=0$. Consequently, under IID sampling the asymptotic covariance of $\widehat\theta$ is simply

$$
V_\theta=E[H_tH_t']
=\begin{pmatrix}
\sigma^2&\nu_3\\
\nu_3&\nu_4-\sigma^4
\end{pmatrix},\qquad
\nu_j=E[(R_t-\mu)^j].
$$

The covariance between the two moment estimators is therefore governed by $\nu_3$. The variance of the second moment estimator is governed by $\nu_4-\sigma^4$. Zero skewness removes the former; Gaussian kurtosis makes the latter $2\sigma^4$. IID sampling alone does neither.

For $g(\theta)=(\mu-R_f)/\sigma$, the gradient with respect to mean and **variance** is

$$
a=\nabla g=
\begin{pmatrix}
1/\sigma\\
-(\mu-R_f)/(2\sigma^3)
\end{pmatrix}.
$$

The delta method gives

$$
\sqrt T(\widehat S-S)\Rightarrow N(0,a'V_\theta a).
$$

Expanding the quadratic form yields a mean-estimation term of one, a cross term $-(\mu-R_f)\nu_3/\sigma^4=-S\gamma_3$, and a variance-estimation term $S^2(\gamma_4-1)/4$. This directly establishes the stated formula. A useful equivalent derivation writes the first-order influence function as

$$
\psi_t=Z_t-\frac S2(Z_t^2-1),\qquad
Z_t=\frac{R_t-\mu}{\sigma}.
$$

Then $V_S=E[\psi_t^2]$. This representation is an implementation aid derived from the paper's gradient calculation: it makes the cross term and nonnegativity transparent and avoids separately manipulating several powers of volatility.

The first line on p. 4 prints $S^2(\gamma_3-1)/4$. That subscript is a typographical error: it must be $\gamma_4$. The second line of equation (2), the preceding matrix derivation, and the appendix code use the correct fourth moment. Implementing the first line literally would even fail to reproduce the normal-distribution benchmark.

The Gaussian expression $1+S^2/2$ is recovered when skewness is zero and ordinary kurtosis is three. Normality is sufficient, but the first-order calculation only needs the corresponding third- and fourth-moment restrictions; it does not characterize the entire distribution as Gaussian.

## Interpreting the correction

For a positive Sharpe ratio, negative skewness raises estimator variance. Positive excess kurtosis also raises it. Positive skewness lowers the covariance contribution and can offset excess kurtosis. These sign statements require attention to the sign of $S$: with a negative Sharpe ratio, the skewness effect reverses. It is therefore too broad to say that left skew always increases uncertainty regardless of the estimand.

The difference from the Gaussian variance is

$$
\Delta V=-S\gamma_3+\frac{S^2}{4}(\gamma_4-3).
$$

With positive skewness and positive excess kurtosis, the nonzero crossover is $S=4\gamma_3/(\gamma_4-3)$. The paper's rounded HML moments imply a crossover at $8/15\approx0.533$; SMB implies $8/21\approx0.381$. These numbers are derived from the reported moments. They explain why the Gaussian approximation overstates uncertainty near the observed small positive factor Sharpe ratios but understates it for sufficiently high hypothetical Sharpe ratios.

At $S=0$, $V_S=1$ regardless of skewness and kurtosis, within the stated regularity conditions. At very large $|S|$, the kurtosis term dominates. Those are asymptotic properties of this ratio estimator; they do not imply that small-Sharpe investments are economically desirable or that heavy tails become unimportant to their losses.

## Reproducing Tables 1–4

Appendix A.1 supplies the actual table-building code. It uses simple monthly factor returns covering 1926–2001, loaded from a local file named `ffmonthly`. The columns are market excess returns, SMB, and HML. The document does not include that data file, its precise vintage, the starting month within 1926, or the underlying factor-construction database. Thus the rounded inputs printed in the tables are sufficient to reproduce the displayed formulas, while exact reproduction of their estimation from original returns requires an archival data file.

Compute each sample Sharpe ratio as the sample mean divided by the population-normalized sample standard deviation; the factor portfolios are treated with a zero benchmark in this calculation. Round these Sharpe ratios to two decimal places. The reported values are 0.12 for RMRF, 0.11 for HML, and 0.06 for SMB. The code adds their sorted values to the hypothetical grid $0.50,0.75,\ldots,3.00$.

The sample-size grid is $T\in\{12,24,36,48,60,125,250,500\}$. Compute skewness and ordinary kurtosis from sample central moments using divisor $T$, and then **round each to the nearest integer** before constructing the tables. This is a significant replication detail: the captions' extreme moments are rounded sensitivity inputs, not full-precision moment estimates.

The moment pairs are:

| Table | Distribution calibration | Skewness | Ordinary kurtosis | Excess kurtosis |
|---|---|---:|---:|---:|
| 1 | Gaussian benchmark | 0 | 3 | 0 |
| 2 | RMRF | 0 | 11 | 8 |
| 3 | HML | 2 | 18 | 15 |
| 4 | SMB | 2 | 24 | 21 |

For every grid point, calculate $\operatorname{ASE}=\sqrt{V_S/T}$. The last column in Tables 2–4 is

$$
100\frac{\operatorname{ASE}_{\rm Gaussian}}
{\operatorname{ASE}_{\rm calibrated}}.
$$

It is a ratio of **standard errors**, not variances, a coverage probability, or a signed percentage difference. It does not depend on $T$ because both standard errors have the same $T^{-1/2}$ factor.

Selected reported values at $T=60$ demonstrate both directions of the correction:

| Sharpe ratio | Gaussian ASE | RMRF-moment ASE | HML-moment ASE | SMB-moment ASE |
|---|---:|---:|---:|---:|
| 0.06 | 0.129 | 0.130 | 0.122 | 0.123 |
| 0.11 | 0.129 | 0.131 | 0.118 | 0.119 |
| 0.12 | 0.130 | 0.131 | 0.117 | 0.119 |
| 0.50 | 0.137 | 0.165 | 0.133 | 0.155 |
| 1.00 | 0.158 | 0.242 | 0.233 | 0.281 |
| 3.00 | 0.303 | 0.626 | 0.744 | 0.883 |

At each factor's own Sharpe ratio, the Gaussian-to-corrected standard-error ratios are 98.60% for RMRF, 110.00% for HML, and 105.46% for SMB. At a hypothetical Sharpe ratio of 3, they fall to 48.38%, 40.67%, and 34.30%, respectively. The source's introductory language about discrepancies of up to roughly 70% should be interpreted with this explicit ratio convention. For example, a standard-error ratio of 34.30% corresponds to a variance ratio of about 11.76%; these are very different statements.

The high-Sharpe rows do not claim that the Fama–French factors themselves had Sharpe ratios of 3. They hold the rounded distributional shape parameters fixed while varying the signal-to-noise ratio. This is a sensitivity exercise, not a ranking of observed strategies.

## Monte Carlo experiment and code-level qualifications

Appendix A.2.1 generates gross returns $G=\exp(X)$ with $X\sim N(0.12,0.25^2)$ and estimates the Sharpe ratio of net returns $G-1$ against a zero benchmark. The observation count per replication is $T=500$. Raw moments of gross returns are

$$
E[G^j]=\exp\!\left(0.12j+\frac{0.25^2j^2}{2}\right).
$$

From these, obtain the net mean, variance, third and fourth central moments. Direct substitution into the paper's formulas gives approximately $\mu=0.16329$, $\sigma=0.29543$, $S=0.55272$, $\gamma_3=0.77825$, and $\gamma_4=4.09593$. The corrected standard error at $T=500$ is about 0.04016, versus 0.04802 under the Gaussian shortcut. These are calculations from the stated inputs, not additional reported empirical estimates.

For each simulated sample, calculate its net mean and standard deviation with divisor $T$, then form the ratio. Compare the histogram with a normal density centered at the theoretical Sharpe ratio using the corrected asymptotic standard error, and with the Gaussian-shortcut density. Figure 1, p. 13, shows the corrected density fitting the histogram more closely, while the Gaussian shortcut is visibly too dispersed. It is a visual comparison; the paper does not report formal goodness-of-fit or confidence-interval coverage tests.

Two discrepancies in the supplied code matter for reproducibility. First, the printed lognormal code sets the number of replications to $N=200$, whereas Figure 1's caption says $N=10{,}000$. The publication does not reconcile the two. Use 10,000 to target the stated figure design and record this choice; do not claim that the appendix script, unchanged, reproduces that figure.

Second, the code stores gross returns in `R` but sets `mu = mean(R)-1`. Its later line `dR = R-mu` consequently centers the gross returns around the **net** mean, leaving a shift of one. Correct sample central moments require `R-mean(R)` or, equivalently, `(R-1)-mu`. This bug affects the subsequent sample-skewness and sample-kurtosis diagnostics. The plotted theoretical standard errors were computed earlier from analytical population moments, and the Sharpe estimates use a correctly netted mean and shift-invariant standard deviation; the bug therefore does not invalidate the main formula or automatically invalidate the displayed histogram.

The helper functions `lognmoment` and `histfit3` are not included, and no random seed is reported. Their roles can be reconstructed from the moment identity and density comparison, but the exact histogram-bin implementation and random realization cannot be recovered from the PDF alone.

## Other experiments supplied but not tabulated

Appendix A.2.2 gives code for $R=0.15+0.3\,t_{100}$, with $T=250$ observations and $N=1{,}000$ replications. Population variance is $0.3^2\,100/98$, skewness is zero, and ordinary kurtosis is $3+6/96$. The variance correction is consequently modest in this particular design; the script is not an experiment with a very heavy-tailed low-degree-of-freedom Student distribution. The code requires a `tmoment` helper that is not reproduced.

Appendix A.2.3 uses an IID bootstrap of annual RMRF returns, despite the monthly returns used for the table calibrations. It sets $N=10{,}000$, uses the data length as $T$, and calls `bootstrp` with an external `sharperatio` function and zero benchmark. A commented alternative would use monthly data. These alternatives must not be conflated. The data file and helper implementation are absent; no numerical results from these two additional experiments are tabulated.

The Student and bootstrap plotting calls center the Gaussian-shortcut comparison at the empirical mean of simulated Sharpe ratios, whereas the corrected comparison uses the population or empirical-distribution target. That distinction can conceal mean bias in a visual comparison and should be preserved or explicitly changed in a replication. None of these simulations reports a trading rule, transaction costs, portfolio turnover, or an out-of-sample investment test.

## Implementation boundaries and takeaways

For an IID application, estimate $\widehat S$, $\widehat\gamma_3$, and $\widehat\gamma_4$ consistently at one frequency and form $\widehat V_S$. An asymptotic 95% interval is $\widehat S\pm1.96\sqrt{\widehat V_S/T}$. In a substantive application, retain unrounded moments; integer rounding is only a requirement for reproducing Mertens's printed sensitivity tables. An influence-function variance computed from sample centered observations offers an algebraic cross-check on the plug-in expression.

A finite-sample normal interval can still be inaccurate when $T$ is small, volatility is nearly zero, sample fourth moments are unstable, or rare losses are absent from the observed history. The paper does not solve those problems. In particular, estimating a very large kurtosis from one short series is itself uncertain; the asymptotic formula is not a guarantee of conservative inference.

For serially dependent returns, replace the IID covariance of the moment vector with its long-run covariance. Mertens states this general GMM structure in Section 2, but does not supply a new serial-correlation estimator or an annualization procedure. Applying the IID correction to smoothed monthly hedge-fund returns without addressing their dependence would repair only one part of the problem.

The useful lesson is precise: Lo's Gaussian IID formula requires Gaussian third- and fourth-moment restrictions, while independence alone permits an additional skewness covariance term and a kurtosis variance term. The direction of the error is economically relevant and not uniformly conservative. A reproducible implementation should recover the normal benchmark, respect the sign of the Sharpe ratio, use the stated kurtosis convention, and distinguish a standard-error ratio from a variance ratio.
