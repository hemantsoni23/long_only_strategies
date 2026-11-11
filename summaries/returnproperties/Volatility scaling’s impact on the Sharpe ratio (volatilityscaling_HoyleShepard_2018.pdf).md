# Volatility scaling’s impact on the Sharpe ratio

**Edward Hoyle and Neil Shephard.** Working paper dated 6 November 2018, SSRN 3279787. **Source:** [Finance/volatilityscaling_HoyleShepard_2018.pdf](../../Finance/volatilityscaling_HoyleShepard_2018.pdf), ten pages including references. Page numbers below are the printed PDF numbers. The library also contains a Man AHL distribution of this work; it is not a separate research contribution.

## Why this matters

Volatility scaling exchanges a fixed exposure for a position proportional to inverse conditional standard deviation. Forecastable volatility makes the resulting conditional risk more stable, but that alone does not establish a higher unconditional Sharpe ratio. Conditional expected returns can move against the scaling rule, and fluctuations in the scaled conditional mean contribute to unconditional variance. This paper isolates both effects in a compact set of moment identities.

Its contribution is an exact decomposition and a useful small-conditional-Sharpe approximation, rather than a new volatility estimator. The decomposition separates a convexity term, which is usually favorable for a positive-return position, from a timing term that depends on the association of expected returns with inverse volatility. Across 142 futures and forward markets, convexity is relatively stable while the timing term is noisy and variable. The evidence supports a diagnostic for understanding a backtest, not a universal guarantee that targeting volatility creates alpha.

There is an important distinction from inverse-variance investment rules. This paper uses $1/\sigma_t$, thereby equalizing conditional variance through time. A mean-variance optimizer with constant conditional expected return instead uses $1/\sigma_t^2$. Their risk paths, turnover, and dependence on very small variance forecasts differ. Neither rule can be substituted for the other in the identities below.

## Information set, excess returns, and the scaling rule

Let $Y_t$ denote the asset's one-period return above its funding cost. An investment can be a long or short position; futures and forward returns should be defined consistently with their unfunded exposure. Let $\mathcal F_{t-1}$ contain information available before the return is earned. The paper permits this information set to include historical high-frequency data or an underlying latent volatility process. Define

$$
\mu_t=E(Y_t\mid\mathcal F_{t-1}),\qquad
\sigma_t^2=\operatorname{Var}(Y_t\mid\mathcal F_{t-1}).
$$

For an implementable strategy, the scaling estimate must be available at formation time. Results stated using a latent true $\sigma_t$ do not automatically hold when it is replaced by a noisy estimate. Assume $\sigma_t>0$ almost surely wherever its reciprocal is used. Finite conditional variance alone does not establish finite inverse-volatility moments.

The unconditional mean and variance are

$$
\mu=E(\mu_t),\qquad
\sigma^2=E(\sigma_t^2)+\operatorname{Var}(\mu_t).
$$

The second expression is the law of total variance. In particular, $\sigma$ is neither $E(\sigma_t)$ nor generally $\sqrt{E(\sigma_t^2)}$. Replacing it with either quantity changes the comparison benchmark. The unscaled Sharpe ratio is $S=\mu/\sigma$, measured at the frequency of $Y_t$.

Write $Y_t=\mu_t+\sigma_t\varepsilon_t$, with conditional mean zero and conditional variance one for $\varepsilon_t$. Independence of shocks and volatility is unnecessary; conditional moment restrictions suffice. The scaled return is $Z_t=Y_t/\sigma_t$. Multiplying $Z_t$ by a positive constant risk target changes its mean and standard deviation proportionally and leaves its Sharpe ratio unchanged. The unit-variance convention is therefore an analytical normalization rather than a proposal to take one hundred percent volatility risk.

Because $\sigma_t$ is known under the conditioning information set,

$$
E(Z_t\mid\mathcal F_{t-1})=\frac{\mu_t}{\sigma_t},\qquad
\operatorname{Var}(Z_t\mid\mathcal F_{t-1})=1.
$$

Conditional variance is constant, but unconditional variance need not equal one. The random conditional mean remains a source of variability. This distinction supplies the denominator correction central to the paper.

## Exact moment decomposition

Theorem 1, pp. 3–4, gives

$$
E(Z_t)=E\left(\frac{\mu_t}{\sigma_t}\right)
=\mu E\left(\frac1{\sigma_t}\right)
+\operatorname{Cov}\left(\frac1{\sigma_t},\mu_t\right),
$$

and

$$
\operatorname{Var}(Z_t)=1+
\operatorname{Var}\left(\frac{\mu_t}{\sigma_t}\right).
$$

The proof takes conditional expectations first, then applies total variance. Cross terms involving the standardized innovation vanish by its conditional zero mean. The covariance decomposition additionally requires the separate expectations to exist. This qualification matters: integrability of $\mu_t/\sigma_t$ does not by itself guarantee integrability of $1/\sigma_t$ if $\mu_t$ can vanish near low-volatility states. A reconstruction should impose the needed inverse moments rather than infer them from finite return variance.

For $\mu\ne0$, define

$$
\xi_0=E\left(\frac{\sigma}{\sigma_t}\right),\qquad
\xi_1=\operatorname{Cov}\left(\frac{\sigma}{\sigma_t},\frac{\mu_t}{\mu}\right),
$$

$$
\gamma_1=\xi_0+\xi_1
=E\left(\frac{\sigma\mu_t}{\mu\sigma_t}\right),\qquad
\gamma_2=\operatorname{Var}\left(\frac{\sigma\mu_t}{\mu\sigma_t}\right).
$$

Then $E(Z_t)=S\gamma_1$ and $\operatorname{Var}(Z_t)=1+S^2\gamma_2$. The author terminology for $\gamma_1$ is volatility mean exposure. The convexity component $\xi_0$ measures mean leverage when the target risk is set equal to the unscaled unconditional standard deviation. The timing component $\xi_1$ measures whether that leverage is larger when the conditional expected return is relatively attractive.

The definitions are unchanged by multiplying the underlying investment by any fixed nonzero scale, including reversing its sign, provided volatility is transformed as an absolute scale. Its Sharpe ratio does change sign when the position is reversed. This is why an invariant exposure statistic is not by itself an invariant statement about whether the signed Sharpe ratio improves.

Conditional zero-mean innovations also imply

$$
\operatorname{Cov}(\sigma_t^{-1},Y_t)
=\operatorname{Cov}(\sigma_t^{-1},\mu_t).
$$

Thus the timing covariance can be estimated with realized returns instead of estimating the conditional mean separately. This is an identification identity, not a claim of precise estimation: a return contains far more noise than its conditional expectation, and the normalized statistic also divides by the unconditional mean. Likewise,

$$
\operatorname{Var}(Z_t)-1
=\operatorname{Var}(\mu_t/\sigma_t).
$$

That equality concerns the true conditional standard deviation. With an estimated EWMA denominator, the conditional shock variance is not necessarily one, so the sample analogue can depart from the model or even become negative.

## Convexity bound and what it does not prove

Lemma 1, p. 4, applies Jensen's inequality to the convex function $x^{-1/2}$, with $x=\sigma_t^2$:

$$
\xi_0=\sigma E(\sigma_t^{-1})
\ge\frac{\sigma}{\sqrt{E(\sigma_t^2)}}
=\left(1-\frac{\operatorname{Var}(\mu_t)}{\sigma^2}\right)^{-1/2}
\ge1.
$$

The bound is meaningful under the required finite inverse moments. It is stronger than simply noting that inverse volatility is convex in volatility, because the benchmark denominator is unconditional return volatility. A low-volatility state receives a larger notional position than a high-volatility state receives a reduction, in the mean-leverage sense measured here.

The favorable bound is only on $\xi_0$. A negative $\xi_1$ can offset it: expected returns may be high precisely when inverse volatility is low. Even if the combined mean exposure is favorable, the variance of $\mu_t/\sigma_t$ can reduce the Sharpe benefit. The lemma therefore establishes neither guaranteed excess expected return for an arbitrary signed investment nor guaranteed Sharpe improvement.

Compare $Z_t$ with $Y_t/\sigma$, so each has a risk normalization based on the unscaled standard deviation. Their expected-return difference is

$$
E\left(Z_t-\frac{Y_t}{\sigma}\right)
=S(\gamma_1-1)
=S(\xi_0-1)+\operatorname{Cov}(\sigma_t^{-1},\mu_t).
$$

For $S>0$, a positive difference requires $\gamma_1>1$. For $S<0$ that inequality reverses. Equalizing this particular conditional-risk benchmark also does not equalize actual unconditional variance, which remains $1+\operatorname{Var}(\mu_t/\sigma_t)$ for the scaled strategy.

## Exact Sharpe comparison and sign qualification

Theorem 2, p. 5, implies the exact formula

$$
S_\sigma=
\frac{E(\mu_t/\sigma_t)}{\sqrt{1+\operatorname{Var}(\mu_t/\sigma_t)}}
=\frac{S\gamma_1}{\sqrt{1+S^2\gamma_2}}.
$$

For a positive unconditional Sharpe ratio, the necessary and sufficient condition for $S_\sigma\ge S$ is

$$
\gamma_1\ge\sqrt{1+S^2\gamma_2}.
$$

**Source qualification:** the paper presents this inequality without explicitly restricting the sign of $S$. Dividing its preceding identity by a negative $S$ reverses the inequality. Accordingly, for $S<0$, the condition is $\gamma_1\le\sqrt{1+S^2\gamma_2}$. If $S=0$, the normalized $\gamma$ variables are undefined and the direct expectation formula must be used. A zero unconditional mean can still yield a nonzero scaled mean through the timing covariance. These are algebraic qualifications of the stated comparison, not additional empirical findings.

Expanding the denominator for small $a=S^2\gamma_2=\operatorname{Var}(\mu_t/\sigma_t)$ gives

$$
S_\sigma\approx S\gamma_1\left(1-\frac12S^2\gamma_2\right)
\approx S\gamma_1.
$$

The relevant small quantity is the variance of the conditional Sharpe ratio at the return frequency. A small daily unconditional Sharpe ratio alone is insufficient if $\gamma_2$ is extremely large. Daily and annual Sharpe ratios must not be mixed in this expansion. Annualizing a daily sample Sharpe is a presentation operation; substituting the annual number into a daily-frequency approximation changes its correction by the annualization factor.

## Two informative special cases

If $\mu_t=\mu$ is constant, the timing covariance vanishes and

$$
S_\sigma=
\frac{S\xi_0}{\sqrt{1+\mu^2\operatorname{Var}(\sigma_t^{-1})}}.
$$

For positive $S$, the convexity gain raises the expected scaled return, but it must exceed the denominator penalty to improve Sharpe. The usual intuition is correct locally: low conditional volatility means a high conditional Sharpe ratio when the expected return is fixed, and inverse volatility increases exposure there. The exact expression also identifies the failure mode. An extreme inverse-volatility distribution can create enough variation in the scaled conditional mean to outweigh the gain.

If $\mu_t=c\sigma_t$, the conditional Sharpe ratio is constant. Then $Z_t=c+\varepsilon_t$ in conditional-moment terms, so

$$
S_\sigma=c,\qquad
S=\frac{cE(\sigma_t)}{\sqrt{E(\sigma_t^2)+c^2\operatorname{Var}(\sigma_t)}},
$$

$$
\gamma_1=\frac{\sigma}{E(\sigma_t)}\ge1,\qquad \gamma_2=0.
$$

Scaling weakly increases the absolute value of Sharpe. For $c<0$ it makes the signed Sharpe more negative, which should not be described as better performance for the same long position. This special case illustrates that a homogeneous conditional reward-to-risk ratio does not imply the same unconditional Sharpe for a mixture of different risk scales.

## Empirical construction

Section 4 uses daily data over 1988–2017 for 142 futures and foreign-exchange forward markets. A market must have at least ten years of data. The categories contain 22 agricultural contracts, 14 bonds, 40 currencies, eight energy contracts, 29 equities, 14 metals, and 15 short-rate contracts. The observation histories consequently differ across markets; cross-sectional summaries are not necessarily based on identical calendars.

The volatility proxy is the square root of an EWMA of past squared returns:

$$
\widehat\sigma_t^2=0.94\widehat\sigma_{t-1}^2+0.06Y_{t-1}^2.
$$

The paper calls this a 12-day half-life; $\log(1/2)/\log(0.94)$ is approximately 11.2 observations, so the coefficient is the precise reproducible specification. No contemporaneous return belongs in the denominator for $Y_t$. The recursion assumes a zero conditional mean for estimating the second moment and is described as an integrated GARCH model. The source does not report initialization, burn-in, market identifiers, contract rolls, forward tenor, pricing times, holiday alignment, or the exact cash/funding construction for every instrument.

A reconstruction computes, separately by market, the unscaled mean $\bar Y$, standard deviation $s_Y$, inverse forecasts $q_t=1/\widehat\sigma_t$, and scaled returns $Z_t=q_tY_t$. Using mutually consistent empirical-moment conventions, form $\widehat\xi_0=s_Y\bar q$ and $\widehat\xi_1=(s_Y/\bar Y)\widehat{\operatorname{Cov}}(q_t,Y_t)$. Then $\widehat S\widehat\gamma_1$ estimates the scaled mean; compare it with $\widehat S_\sigma=\bar Z/s_Z$. The covariance identity makes a separate predictive regression for $\mu_t$ unnecessary.

With population-style sample covariance and standard-deviation definitions, $\widehat S\widehat\gamma_1=\bar Z$ is an algebraic identity. Dividing by $s_Z$ yields the observed scaled Sharpe by construction. The right-hand plots in Figures 1–2, which add that denominator, are therefore principally consistency checks. The left-hand plots test the useful approximation that the standard deviation of the scaled position is close enough to one. They are not independent tests that the EWMA equals true conditional volatility.

Figures 1–2 plot the results by market and asset category. The plotted adjusted and observed Sharpe statistics track closely, including the change relative to the unscaled Sharpe. The study does not report a root-mean-square approximation error, formal cross-sectional significance test, or a held-out tuning exercise. It also does not establish that all markets improve: the plots include decreases and negative Sharpe ratios.

## Numerical results and their interpretation

Table 1, p. 8, reports the following cross-market distributions. The standard deviations describe dispersion across markets, not standard errors of an average estimate.

| Statistic | Mean | Median | Cross-market SD | 10th percentile | 90th percentile |
|---|---:|---:|---:|---:|---:|
| $\gamma_1$ | 1.33 | 1.08 | 2.20 | 0.63 | 1.77 |
| $\xi_0$ | 1.36 | 1.26 | 0.30 | 1.16 | 1.64 |
| $\xi_1$ | −0.03 | −0.20 | 2.21 | −0.88 | 0.52 |

The covariance of the two components across markets is −0.07 and their correlation is −0.11. The convexity component is consistently above one in these descriptive results. The timing component is much noisier, with cross-sectional dispersion more than seven times that of convexity. The median timing component is negative even though its average is near zero.

By category, mean $\gamma_1$ is 1.99 for agriculture, 1.07 for bonds, 1.46 for currencies, 1.04 for energy, 1.18 for equities, 0.93 for metals, and 1.04 for short rates. Corresponding medians are 1.00, 1.06, 1.33, 1.00, 1.16, 0.99, and 0.99. The agricultural mean of 1.99 therefore does not describe a typical contract; its median is 1.00. Likewise, a mean exposure ratio should not be read as a portfolio-level Sharpe improvement.

Mean convexity components are 1.21, 1.29, 1.44, 1.22, 1.35, 1.24, and 1.68 in that same order. Mean timing components are 0.78, −0.21, 0.02, −0.17, −0.16, −0.31, and −0.63. Rounding explains small differences between sums of displayed components and displayed $\gamma_1$. The median timing component is negative in every category. The authors emphasize that conditional-mean effects are difficult to estimate reliably.

An additional implication of the normalization is that assets with small sample mean returns can have unstable $\gamma_1$ and $\xi_1$ even if their unnormalized covariance is modest. The source does not report an exclusion or stabilization rule for near-zero means. A faithful replication should retain the direct Sharpe difference and the unnormalized mean/covariance alongside these ratios, flagging near-zero denominators. Imposing an undisclosed winsorization would change Table 1.

## Replication limits and practical use

The note's core contribution is reproducible from return data and a documented volatility filter. A robust implementation should check information timing, zero or near-zero forecasts, inverse-moment sensitivity, moment normalization, and annualization. These checks are implementation consequences of the model; the paper does not prescribe clipping thresholds or an optimal volatility floor. Such constraints would define a different strategy and should be analyzed separately.

The empirical study does not model transaction costs, margin calls, borrowing spreads, leverage caps, execution delays, or market impact. Its conclusion explicitly defers cost mitigation to future work. It also provides no public complete contract-level data appendix or simulation-based uncertainty assessment. The finite sample supports the accuracy of a descriptive approximation for the examined histories, rather than a universal out-of-sample theorem.

The practical use is to diagnose where a scaling benefit comes from. A favorable convexity contribution may be almost entirely offset by the covariance of exposure and expected returns. A higher scaled mean need not imply a higher Sharpe once scaled-mean variance is included. Finally, a good result under true conditional volatility can weaken under forecast error or financing constraints. Keeping those three distinctions explicit makes this compact decomposition useful for evaluating an actual strategy rather than treating risk stabilization as automatic return enhancement.
