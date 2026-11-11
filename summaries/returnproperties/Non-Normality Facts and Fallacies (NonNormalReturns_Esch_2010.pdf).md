# Non-Normality Facts and Fallacies

David N. Esch, *Journal of Investment Management* 8(1), first quarter 2010, pp. 49–61. Source: [NonNormalReturns_Esch_2010.pdf](../../Finance/NonNormalReturns_Esch_2010.pdf). The full 13-page file was inspected, including the three figures, two simulation tables, and references. Printed page numbers are used below.

## Why this matters

A rejection of normality in a histogram of historical returns does not identify the model that should replace a Gaussian forecast. The histogram combines observations from different volatility states, economic conditions, and possibly different expected returns. A model can have conditionally Gaussian innovations and still imply a highly non-Gaussian unconditional return distribution. Conversely, fitting a flexible unconditional distribution does not establish that its tail forecasts or portfolio decisions will survive outside the estimation sample.

Esch's contribution is a methodological critique of the inference that observed nonnormality automatically invalidates normal components in investment models. He organizes the argument around conditional versus marginal distributions, estimation error in higher moments, the limitations of scalar tail summaries, systematic shocks, and transformations. This is a conceptual practitioner article with illustrative simulations, not a new estimator accompanied by an investment backtest. Its most useful lesson is to evaluate the whole predictive model and decision problem. Several stronger claims, especially about copulas and investor preferences, require qualifications that this note makes explicit.

## The modeling distinction at the center of the paper

Sections 2 and 7–9 distinguish a normal distribution for an observed variable from normal building blocks inside a larger model. A mathematical reconstruction of that distinction is

$$
R_t\mid X_t,\theta\sim N\bigl(\mu(X_t,\theta),\sigma^2(X_t,\theta)\bigr).
$$

Here $X_t$ is information or a latent state and $\theta$ is a parameter vector. Integrating over states gives

$$
p(r\mid\theta)=\int p(r\mid x,\theta)p(x\mid\theta)\,dx.
$$

This mixture need not be normal. Integrating additionally over parameter uncertainty gives a posterior predictive distribution,

$$
p(r_{t+1}\mid\mathcal D_t)=\int p(r_{t+1}\mid\theta,\mathcal D_t)p(\theta\mid\mathcal D_t)\,d\theta.
$$

These equations formalize the paper's discussion; Esch does not estimate either specification. The first mixes economic states. The second mixes uncertain parameter values. Those are different sources of dispersion and should not be conflated when interpreting a forecast or designing a simulation.

A particularly transparent reconstruction sets $R=\sqrt V Z$, where $Z\sim N(0,1)$ is independent of positive random variance $V$. Provided the relevant moments exist,

$$
E[R^2]=E[V],\qquad E[R^4]=3E[V^2],\qquad
\frac{E[R^4]}{E[R^2]^2}=3\frac{E[V^2]}{E[V]^2}\geq3.
$$

Random volatility alone generates unconditional excess kurtosis even though every conditional return distribution is normal. Equality requires constant $V$. Introducing state-dependent means or asymmetric state probabilities can create skewness as well. The construction establishes possibility, not an empirical claim that Gaussian mixtures adequately describe every asset or every tail probability.

The same logic applies to regression. If $Y=X\beta+\varepsilon$ and the conditional residual is normal, an irregular distribution of regressors can make the marginal distribution of $Y$ nonnormal. Testing the histogram of $Y$ then tests a different hypothesis from conditional normality of $\varepsilon$. A replication-oriented analysis should specify exactly which variable, conditioning set, horizon, and probability law a normality statement concerns.

## Mean–variance decisions and the role of approximation

Section 2 argues that mean–variance optimization is often useful as an approximation to expected-utility maximization. It need not be defended by asserting exact Gaussian unconditional returns. To make this precise, let terminal wealth be $W=\bar W+\Delta W$ with $E[\Delta W]=0$. A second-order expansion gives

$$
E[U(W)]\approx U(\bar W)+\frac12U''(\bar W)\operatorname{Var}(W).
$$

This is an explanatory reconstruction, not an error bound supplied by Esch. Its accuracy depends on the utility function, the scale and support of wealth changes, and the contribution of omitted higher-order terms. It may perform poorly near bankruptcy, for strongly nonlinear payoffs, or when tail events dominate expected utility. Existence of the necessary moments is also a prerequisite.

Operationally, a mean–variance portfolio problem can be written as maximizing $w'\mu-\lambda w'\Sigma w/2$ subject to budget and trading constraints. Esch emphasizes that practical constraints and estimation uncertainty make the simple framework valuable. The paper does not specify an asset universe, risk-aversion coefficient, covariance estimator, transaction-cost function, or constraints for a new numerical application. It therefore supplies a modeling argument rather than a ready-to-run allocation strategy.

The discussion also favors averaging over possible parameter realizations instead of treating an estimated mean and covariance as known. Esch cites Michaud's resampled optimization as an example. No comparative experiment in this paper establishes its dominance over Bayesian optimization, shrinkage, robust optimization, or a conventional constrained benchmark. The author's affiliation with New Frontier Advisors and the favorable discussion of its optimizer are relevant context when distinguishing an advocated practice from evidence produced here.

## Parsimony and the actual source of estimation risk

Section 3 treats complexity as a finite-information problem. Historical observations may be numerous in calendar time but offer little stable information about expected returns, tail shapes, or regime transitions. Extending the sample increases its nominal size while potentially adding stale observations from a different data-generating process. Adding parameters can improve in-sample fit while worsening prediction.

The paper invokes penalized model selection and the principle of trading fit against complexity. It does not estimate information criteria or report a cross-validation exercise. Its strongest defensible claim is conditional: a more flexible model needs evidence that its extra flexibility captures stable signal. Complexity is not intrinsically harmful, and a parsimonious but systematically wrong model can also fail badly.

For reproduction of the argument, three uncertainties should be kept separate. Sampling uncertainty concerns the estimates conditional on a model. Specification uncertainty concerns whether the model captures the relevant mechanism. Temporal instability concerns whether parameters or mechanisms change. Replacing a Gaussian family with a skewed family addresses only some specification questions; it does not automatically resolve the other two. This distinction is an interpretation of Esch's argument rather than a taxonomy estimated in the article.

## Higher moments: definitions, sensitivity, and reported simulation evidence

Section 4 illustrates the instability of sample skewness and kurtosis even under a normal population. With sample central moments $m_k=n^{-1}\sum_{i=1}^n(x_i-\bar x)^k$, common uncorrected statistics are

$$
g_1=\frac{m_3}{m_2^{3/2}},\qquad b_2=\frac{m_4}{m_2^2}.
$$

The normal population has skewness zero and kurtosis three. Kurtosis here is ordinary kurtosis, not excess kurtosis. Different finite-sample bias corrections change the sampling distributions, especially at small $n$. The article does not state the exact estimator formulas used to produce its tables, so the expressions above are a transparent candidate implementation rather than a certified reconstruction of the original code.

Tables 1–2 on p. 54 report quantiles across simulated standard-normal samples at sizes 20, 40, 60, 90, 135, 200, 300, 450, 667, and 1,000. Selected central 95% ranges are:

| Sample size | Skewness, 2.5% to 97.5% | Kurtosis, 2.5% to 97.5% | Median kurtosis |
|---:|---:|---:|---:|
| 20 | −0.949 to 0.939 | 1.736 to 4.628 | 2.549 |
| 60 | −0.601 to 0.603 | 2.115 to 4.283 | 2.802 |
| 200 | −0.339 to 0.334 | 2.441 to 3.748 | 2.933 |
| 1,000 | −0.155 to 0.149 | 2.723 to 3.328 | 2.985 |

At $n=20$, the reported 0.5% and 99.5% kurtosis quantiles are 1.595 and 5.919. At $n=1,000$, they remain 2.647 and 3.480. Thus a visually noticeable departure of a sample moment from its population value is not by itself evidence of a nonnormal population. The opposite inference is also invalid: these tables do not show that empirically observed departures of arbitrary magnitude can be dismissed as sampling noise.

The influence mechanism is elementary but consequential. Cubing and taking fourth powers of centered observations give extreme realizations disproportionately large influence. A model fitted to these statistics may effectively calibrate its tail parameters to very few events. Sampling uncertainty in those parameters then enters any optimized allocation based on them. Esch does not quantify that downstream portfolio error in this article.

A reproducible qualitative experiment draws independent $N(0,1)$ samples separately for every listed $n$, computes a clearly declared pair of moment estimators for each draw, and tabulates the same quantiles. To reproduce the exact printed values one would also need the number of Monte Carlo repetitions, random-number generator, seed, quantile interpolation convention, and estimator bias corrections. Those inputs are absent. The tables are normal-null reference illustrations, not distributions calibrated to serially dependent or heteroskedastic financial returns.

## Changing skewness or kurtosis changes the rest of the distribution

Figures 1–2, pp. 52–53, show illustrative density families with lower moments held fixed. In Figure 1, increasing positive skewness shifts the mode and much of the displayed density leftward; rare positive outcomes compensate so that the mean remains unchanged. In Figure 2, higher kurtosis coincides with a sharper central peak and heavier tails while variance is fixed. The exact family and numerical parameter values underlying the curves are not supplied, so the figures cannot be regenerated exactly from the article alone.

The valid general point is a moment constraint: changing tail probability or magnitude while holding mean and variance fixed requires compensating changes elsewhere. A tail modification cannot be evaluated as though the remainder of the distribution were automatically unchanged. Nevertheless, the particular movement of the mode shown in these figures is not a universal theorem implied solely by an increase in a standardized third or fourth moment. Many distributions share the same first four moments, and their central mass can be arranged differently.

Esch connects these examples to relative-performance pressure on investment managers. A strategy with positive skewness may earn less in ordinary periods in exchange for rare large gains. That can be unattractive to a manager facing short evaluation horizons. This is an economic consideration, not a proof that every rational investor dislikes positive skewness at fixed mean and variance. The appropriate preference ranking depends on utility, horizon, liabilities, and the full distributions being compared. The article does not estimate a compensation or fund-termination model.

## Tail summaries and the return-versus-loss convention

Section 5 discusses conditional value at risk, also called expected shortfall. A critical implementation detail is which tail is being averaged. For a loss variable $L$, a continuous-distribution convention is

$$
\operatorname{ES}_{\alpha}(L)=E[L\mid L\geq\operatorname{VaR}_{\alpha}(L)].
$$

For returns $R$, downside risk concerns the lower tail or the upper tail of $L=-R$. At atoms or quantile ties, a quantile-integral definition or explicit partial weighting is needed. A code implementation should declare the sign convention and treatment of ties rather than translating the paper's example mechanically.

The example on p. 55 compares two samples of 100 returns. Both have five observations of +15%. The remaining 95 observations are −10% in the first sample and +10% in the second. The mean of the five largest returns is +15% in both cases, while the second sample is plainly better under increasing utility. The overall sample means, calculated from the printed inputs, are −8.75% and +10.25%.

This example establishes that an upper-tail return average does not summarize the entire distribution. It does not demonstrate a failure of conventional downside expected shortfall to distinguish these two samples: their worst-return tails differ. The substantive broader warning survives the convention problem. A single tail mean cannot generally represent all features relevant to expected utility, and equal tail means can mask different dispersion within the selected tail. Equally, mean and variance are also incomplete summaries. Choosing a risk measure is a decision-specific modeling choice, not a contest for a scalar that captures every property of a distribution.

The article does not fit a generalized Pareto tail, select a threshold, estimate a tail index, or provide an extreme-value model comparison. Its remarks about extreme-value analysis are cautions about combining the tail and center coherently and about the cost of risk reduction. They should not be reported as empirical evidence that extreme-value methods underperform.

## Systematic shocks and rising correlations

Section 6 argues that a dominant common shock can raise measured correlations without eliminating idiosyncratic diversification benefits. A reconstruction uses $R_i=\beta_iF+e_i$, with $F$ orthogonal to residuals and pairwise uncorrelated residuals. Then

$$
\operatorname{Corr}(R_i,R_j)=\frac{\beta_i\beta_j\sigma_F^2}{\sqrt{(\beta_i^2\sigma_F^2+\sigma_i^2)(\beta_j^2\sigma_F^2+\sigma_j^2)}}.
$$

If the factor variance grows while residual variances and nonzero betas remain fixed, this correlation approaches the sign of $\beta_i\beta_j$. For similarly signed exposures it approaches one. Residual correlation can remain zero throughout. This algebra explains the mechanism proposed in the paper without requiring a change in the innovation distribution.

The qualification is economically important: factoring out a common shock does not remove it from portfolio wealth. An investor with a large common exposure may still need to change risk even if residual correlations are stable. Nor does the model prove that residual dependence remains stable in every crisis. Esch reports no crisis dataset, estimated factor model, residual-correlation table, or statistical test for his stronger empirical assertions. His continued preference for diversification follows from an assumption that investors lack reliable information supporting concentrated bets; it is not a universal optimality result for all constraints or liabilities.

## Gaussian copulas: retain the warning, qualify the mathematical claim

Section 8 correctly warns that nonlinear marginal transformations generally do not preserve Pearson correlations or Gaussian conditional-moment formulas. It goes further in suggesting that transformation to nonnormal margins invalidates copula analysis. That stronger statement does not follow. The following mathematical construction clarifies the distinction; it is this note's verification rather than a method estimated by Esch.

Let $Z\sim N_d(0,C)$, with correlation matrix $C$, and set $U_i=\Phi(Z_i)$ and $X_i=F_i^{-1}(U_i)$ for continuous marginal distributions $F_i$. Each $X_i$ has the specified marginal, and the joint distribution is

$$
P(X_1\leq x_1,\ldots,X_d\leq x_d)=\Phi_C\bigl(\Phi^{-1}(F_1(x_1)),\ldots,\Phi^{-1}(F_d(x_d))\bigr).
$$

This is a valid probability model. Its latent-normal correlation matrix is generally not the Pearson correlation matrix of $X$. Gaussian regression formulas apply in the latent coordinates, and probabilities must be transformed consistently when returning to the observed coordinates. Mistaking one correlation for the other or carrying a linear conditional expectation through a nonlinear inverse transformation is an implementation error; the existence of nonnormal margins is not itself such an error.

The paper offers no new CDO pricing experiment or comparison of joint-default predictions. Its claim that copula calculations contributed to crisis losses is commentary supported by cited literature, not a result demonstrated here. The useful implementation warning is to validate dependence, marginal distributions, and extreme joint events separately rather than assuming that a calibrated correlation matrix establishes all three.

## What can be reimplemented and what remains unproved

The directly reproducible content consists of the normal-sample moment experiment, the printed tail-summary counterexample, and the mechanisms involving mixtures, common factors, and transformations. The article's quantitative evidence does not include an investment universe, historical trading dates, forecast horizon, formation and holding rules, transaction costs, turnover, out-of-sample scores, or uncertainty estimates for a portfolio comparison. None should be supplied as though they were original inputs.

A useful research application is therefore a controlled model comparison with an explicitly chosen predictive target. Keep data, information timing, constraints, and evaluation dates fixed; compare a conditional Gaussian baseline with a justified extension; propagate estimation uncertainty; inspect both central and tail calibration. Such an experiment would test the article's recommendations, not replicate an experiment already performed by its author.

Esch makes the strongest case when distinguishing a model's components from its marginal output and when demonstrating finite-sample uncertainty in higher moments. The article is weaker where it turns those cautions into broad preference claims or criticism of entire model families. Its practical value is the demand for an explicit mechanism and a demonstrable predictive benefit before adding complexity. It does not establish that normal models are universally adequate, that nonnormal models are uniformly overfit, or that historical tail losses can be ignored.
