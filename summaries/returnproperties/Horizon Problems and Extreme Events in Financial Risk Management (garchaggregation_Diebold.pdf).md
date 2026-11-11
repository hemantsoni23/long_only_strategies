# Horizon Problems and Extreme Events in Financial Risk Management

Peter F. Christoffersen, Francis X. Diebold, and Til Schuermann, *Federal Reserve Bank of New York Economic Policy Review*, October 1998, pp. 109–118. [Source PDF](../../Finance/garchaggregation_Diebold.pdf). All ten pages, including both charts, endnotes, and references, were read. This is a compact research synthesis with a worked GARCH example and an empirical horizon comparison. Several components draw on the authors' earlier papers rather than originating here.

## Why this matters

A daily risk model and a model of risk over several weeks answer different questions. Multiplying today's conditional standard deviation by the square root of the holding period implicitly freezes a dynamic volatility state. It can substantially exaggerate long-horizon variation and can understate risk when current volatility is unusually low. The paper combines this aggregation argument with a diagnostic based on clustering of interval hits, then argues for more attention to extreme-tail estimation at horizons where the diagnostic detects little persistence.

The empirical claim is narrower than the article's strongest concluding language. For the examined historical returns, dependence of a particular binary hit sequence becomes difficult to detect at longer aggregation intervals. This is not a proof that all conditional variance forecasts become useless after ten days, that returns become independent, or that extreme-value assumptions then hold automatically. Those distinctions matter when translating the paper into risk-system design.

## Three different horizon calculations

Let $r_t$ be a zero-mean daily log return and $R_{t,h}=\sum_{j=1}^{h}r_{t+j}$. With independent, identically distributed returns of finite variance $v$,

$$
\operatorname{Var}(R_{t,h})=hv,
\qquad \operatorname{SD}(R_{t,h})=\sqrt h\sqrt v.
$$

The article uses this as the environment in which square-root scaling is exact. Independence is sufficient, but stronger than necessary for this unconditional variance identity: serially uncorrelated, equal-variance returns also suffice. A covariance-stationary GARCH martingale difference can therefore have exact unconditional variance scaling while its conditional variance forecasts do not scale this way. The practical objection concerns scaling the current conditional volatility, not the algebra of unconditional sums.

For a stationary process with nonzero return autocovariances $\Gamma_k$, the more general identity is

$$
\operatorname{Var}(R_{t,h})=h\Gamma_0+
2\sum_{k=1}^{h-1}(h-k)\Gamma_k.
$$

This reconstructed identity identifies the additional issue created by conditional-mean dynamics. It should not be conflated with the volatility-state problem in the source's zero-mean GARCH example.

Quantiles require distributional assumptions beyond variance addition. With independent centered Gaussian returns, a fixed quantile scales by $\sqrt h$. Independent non-Gaussian returns generally do not preserve this quantile scaling exactly. With a nonzero constant mean, the location scales by $h$, so even the Gaussian result applies to centered quantiles rather than the raw quantile without a drift adjustment. The source's examples of scaling by $\sqrt{10}$ or $\sqrt{252}$ describe historical industry practice, not an empirical estimate of a universal safe conversion.

A third calculation changes the observation frequency itself: aggregate daily returns into nonoverlapping blocks, then describe the variance dynamics observable from that coarser history. This is the Drost–Nijman weak-GARCH calculation used in the article. Its information set differs from a daily-information forecast of a future block. Keeping those objects separate avoids treating every quantity called long-horizon volatility as identical.

## The GARCH example and exact daily-information forecast

The source assumes

$$
r_t=\sigma_t\epsilon_t,\quad
\sigma_t^2=\omega+\alpha r_{t-1}^2+\beta\sigma_{t-1}^2,
\quad \epsilon_t\overset{iid}{\sim}N(0,1),
$$

with $\omega>0$, $\alpha,\beta\ge0$, and $\delta=\alpha+\beta<1$. Its worked example uses $\omega=1$, $\alpha=0.10$, and $\beta=0.85$. The variance scale is arbitrary; the example is not calibrated in percentage-return units to a specified security. The stationary variance is $\bar v=\omega/(1-\delta)=20$.

The normal-innovation fourth moment exists here because

$$
3\alpha^2+2\alpha\beta+\beta^2=0.9225<1.
$$

The unconditional return kurtosis, needed for aggregation, is

$$
\kappa=3\frac{1-\delta^2}{1-\delta^2-2\alpha^2}
=3.774193548\ldots.
$$

This is not the innovation kurtosis three. Confusing the two changes the aggregated parameters.

For comparison with frozen-state scaling, a direct daily-information derivation gives

$$
E_t[\sigma_{t+j}^2]=\bar v+\delta^{j-1}(\sigma_{t+1}^2-\bar v),
$$

and, because future returns are conditionally uncorrelated,

$$
\operatorname{Var}_t(R_{t,h})=
 h\bar v+(\sigma_{t+1}^2-\bar v)\frac{1-\delta^h}{1-\delta}.
$$

These formulas are reconstructed from the source model, not printed empirical results. Frozen-state scaling substitutes $h\sigma_{t+1}^2$. The coefficient on the current deviation is therefore $h$ under scaling but $(1-\delta^h)/(1-\delta)$ under the model. At $h=90$ and $\delta=0.95$, the latter is about 19.8022 rather than 90. High current variance produces an overstatement; low current variance produces an understatement. The scaling rule is not uniformly conservative.

For example, if the next daily variance is 40, the correct daily-information 90-day variance is approximately 2196.04, versus the scaled 3600. If it is 10, the corresponding values are approximately 1601.98 and 900. These are explicitly calculated examples, not observations in Chart 1. They also show why saying long-horizon fluctuations disappear must be interpreted with care: current-state effects remain in a finite-horizon forecast even as their relative importance shrinks.

## Reconstructing the weak-GARCH aggregation

Endnote 3 says that references to GARCH in the aggregation discussion mean **weak GARCH**. Its variance recursion is a best linear predictor of squared returns using the relevant past returns and their squares. It need not equal the complete nonlinear conditional expectation, and standardized low-frequency errors need not remain independent or Gaussian.

Let $Y_{h,k}$ be the sum of $h$ successive nonoverlapping daily returns. The aggregated recursion is

$$
H_{h,k}=\omega_h+\alpha_hY_{h,k-1}^2+\beta_hH_{h,k-1}.
$$

The source gives

$$
\omega_h=h\omega\frac{1-\delta^h}{1-\delta},
\qquad \alpha_h=\delta^h-\beta_h.
$$

Write $C=\alpha-\beta\alpha\delta$. Its remaining formulas are

$$
a_h=h(1-\beta)^2+
\frac{2h(h-1)(1-\delta)^2(1-\beta^2-2\beta\alpha)}{(\kappa-1)(1-\delta^2)}
+\frac{4(h-1-h\delta+\delta^h)C}{1-\delta^2},
$$

$$
b_h=C\frac{1-\delta^{2h}}{1-\delta^2},
\qquad
Q_h=\frac{a_h\delta^h-b_h}{a_h(1+\delta^{2h})-2b_h},
\qquad
\frac{\beta_h}{1+\beta_h^2}=Q_h.
$$

Select the solution satisfying $|\beta_h|<1$. For $|Q_h|<1/2$ a numerically convenient expression is

$$
\beta_h=\frac{2Q_h}{1+\sqrt{1-4Q_h^2}},
$$

with $\beta_h=0$ at $Q_h=0$. The denominator of the final term in $a_h$ is $1-\delta^2$, and the quadratic denominator ends in $-2b_h$; both were checked visually. Replacing these by superficially similar expressions changes the result. Finite fourth moments and the appropriate symmetry conditions are part of the underlying aggregation result, beyond the elementary second-moment stationarity restriction.

For the source parameters and $h=90$, direct evaluation gives approximately

$$
\omega_{90}=1782.20094,\quad
\alpha_{90}=0.009523569,\quad
\beta_{90}=0.000364796.
$$

Their sum is $0.95^{90}\approx0.009888365$, and their implied unconditional variance is 1800, as required. The square root of that variance is approximately 42.4264. This is a root-mean-square scale, not a claim that the mean of conditional standard deviations is exactly 42.4264.

Chart 1 compares a highly variable scaled daily standard deviation with a nearly flat 90-day weak-GARCH standard deviation. Its upper panel has roughly 9,000 daily positions on the horizontal axis, while the lower has about 100 aggregated positions. Those are different sampling frequencies, not 9,000 versus 100 equally spaced daily forecasts. The chart is illustrative; no seed, burn-in, path values, or initialization is supplied. The reported visual result is consistent with the very small aggregated persistence above, but the exact plotted path cannot be reproduced from the article alone.

As $h$ grows, the aggregated coefficients tend toward zero under the stated stationary finite-moment model. This mathematical limit does not identify a universal finite cutoff. The source also emphasizes model risk: the best-fitting daily approximation, once aggregated, need not be the best approximation at the target horizon. Correctly manipulating a misspecified model does not remove that misspecification.

## Interval hits as a diagnostic

For a proposed interval $[L_{t|t-1}(p),U_{t|t-1}(p)]$, define

$$
I_t=\mathbf1\{Y_t\in[L_{t|t-1}(p),U_{t|t-1}(p)]\}.
$$

The source codes an inside-interval observation as one. Unconditional coverage requires $E[I_t]=p$. Conditional coverage relative to an information set $\mathcal F_{t-1}$ requires $E[I_t\mid\mathcal F_{t-1}]=p$. Correct average coverage alone permits long runs of misses in volatile periods and long runs of hits in tranquil periods.

If the information set consists only of the entire previous hit history, constant conditional success probability is equivalent to an iid Bernoulli($p$) hit sequence. The forward implication follows by factorizing the joint probability sequentially; the reverse follows from independence. This equivalence is about the binary sequence and its own history. It does not establish independence of the underlying returns or adequacy with respect to additional observed predictors.

The application uses a constant interval within each horizon. Clustering of hits then indicates that the probability of landing in that interval changes predictably with past hits. Under a stable centered scale-family interpretation, this is evidence about variance dynamics. Without those restrictions, predictable changes in means, skewness, or tail shape can also change hit probabilities at constant variance. Conversely, a variance process can vary while the probability inside one chosen interval remains fixed. Thus the test is a useful diagnostic, not an omnibus equivalence between no hit dependence and no volatility predictability.

The first statistic is the number of runs,

$$
R=1+\sum_{t=2}^{n}\mathbf1\{I_t\ne I_{t-1}\}.
$$

Too few runs indicate clustering. The source refers to an exact finite-sample distribution and a first-order Markov alternative. An implementable reconstruction conditions on the observed counts $n_1$ and $n_0$. Under exchangeability, all $\binom n{n_1}$ binary orderings with these counts are equally likely. For nonzero counts,

$$
P(R=2k\mid n_1,n_0)=
\frac{2\binom{n_1-1}{k-1}\binom{n_0-1}{k-1}}{\binom n{n_1}},
$$

$$
P(R=2k+1\mid n_1,n_0)=
\frac{\binom{n_1-1}{k}\binom{n_0-1}{k-1}+
\binom{n_1-1}{k-1}\binom{n_0-1}{k}}{\binom n{n_1}}.
$$

Set invalid combinatorial terms to zero and handle an all-one or all-zero sequence separately. A lower-tail test uses $P(R\le R_{obs})$ for positive clustering. A two-sided test requires an explicit extremeness convention and is different. The article does not provide its exact tail-counting implementation; the chart and discussion emphasize positive persistence. These formulas are a reconstruction of the cited runs method, not supplied code or confirmation of the original P-value convention.

The second diagnostic assumes a first-order Markov transition matrix with $\pi_{ij}=P(I_t=j\mid I_{t-1}=i)$. Its nonunit eigenvalue is

$$
S=\pi_{11}-\pi_{01}.
$$

Estimate $\widehat\pi_{ij}=n_{ij}/(n_{i0}+n_{i1})$, where $n_{ij}$ counts consecutive transitions, and then compute $\widehat S$. Under first-order independence both rows have the same success probability and $S=0$. Positive $S$ describes persistence; negative $S$ describes alternation. A zero estimate alone does not rule out dependence at longer lags, and a first-order Markov restriction is required for the eigenvalue to summarize the entire transition behavior.

The source obtains null reference bands for $S$ through simulation-based resampling. A reproducible implementation must specify whether it permutes fixed-count hit sequences or simulates Bernoulli sequences, whether thresholds are reestimated in each resample, the number of repetitions, and the handling of an empty transition row. Those details are absent. A 95% null envelope around zero is also not automatically a confidence interval for an unrestricted population persistence parameter.

## The empirical horizon comparison

The worked data are 6,327 daily observations on the Dow Jones Composite Index from January 1, 1974 through April 2, 1998. The index contains 65 major stocks: 30 industrials, 20 transportation stocks, and 15 utilities. The paper aggregates to nonoverlapping $h$-day returns for each $h=1,\ldots,20$ and uses an interval of plus or minus two standard deviations at that horizon. The standard deviation is horizon specific; the interval is constant over time within a horizon. The resulting coverage probability need not be the same across horizons or equal Gaussian 95.45% coverage.

The article does not give the underlying data file, treatment of holidays and incomplete final blocks, price-versus-total-return convention, sample-standard-deviation divisor, or precise demeaning convention. An interval centered at zero versus a sample mean can change hits. The analysis is a historical diagnostic using constant estimated thresholds, not a described rolling real-time forecasting strategy.

Chart 2 reports a jagged pattern. At very short horizons, roughly up to a week, the runs test strongly rejects independence and the Markov eigenvalue is positive. Intermediate horizons have alternating rejections and nonrejections. Above approximately three weeks, the plotted eigenvalues are small or negative and the runs test finds no positive clustering. The article's discussion of the Dow sample is more cautious than a rule that all predictability ends exactly on day ten.

The chart supplies no numerical table of P-values, transition counts, or confidence limits. Exact values should not be inferred from line thickness. Its qualitative result is that evidence for persistence declines with aggregation, not that a smooth monotonic relationship is observed at every horizon. The source also summarizes earlier results for equity, foreign-exchange, and bond returns in the United States, United Kingdom, Germany, and Japan, using ten days as a rough rule of thumb. Those additional asset-level datasets and test outputs are not reproduced in this article.

Loss of power is an essential qualification. If 6,327 daily observations are divided into complete nonoverlapping blocks, only 1,265 five-day, 632 ten-day, 421 fifteen-day, or 316 twenty-day observations remain. These counts are calculated from the reported sample size under that explicit truncation convention. The interval-hit process has even fewer observations outside its central band. Confidence bands widen in the chart. A failure to reject at longer horizons can reflect weak information as well as genuinely weaker dynamics.

The twenty horizon tests are related, and the source supplies no simultaneous confidence band or multiple-testing adjustment. Changing the aggregation start date can change which extreme observations share a block. Nonoverlapping aggregation avoids the mechanical overlap of rolling returns, but does not prove that blocks are independent. Nor does a full-sample standard-deviation estimate make this a conventional out-of-sample forecast comparison.

The authors' recommendation to devote less attention to volatility forecasting at long horizons is therefore a research interpretation of the displayed evidence. It is not a demonstrated optimal allocation of modeling effort or an economic cost-benefit calculation. No portfolio, hedge, capital constraint, utility function, transaction cost, or realized risk-management loss is evaluated.

## Extreme-value estimation: useful structure, strong assumptions

The paper proposes investigating the tails directly when long-horizon volatility forecasts appear less useful. Its specific tail model is regular variation:

$$
P(X>x)=\ell(x)x^{-\alpha},\qquad \alpha>0,
$$

where $\ell$ is slowly varying, meaning $\ell(cx)/\ell(x)\to1$ for each fixed $c>0$. For financial losses, use an appropriate positive loss variable, such as $X=-R$ in the lower return tail. Applying logarithms to signed returns without this transformation is invalid. The source writes an upper-tail model; downside use requires that explicit sign convention.

This is the heavy-tail setting of the method discussed here, not the whole of extreme-value theory. It excludes Gaussian tails. The article mentions non-Gaussian stable laws with stability index below two as examples, but the regular-variation family is broader and also permits tail exponents above two. Existence of second or fourth moments must be checked separately when combining tail estimates with the earlier variance calculations.

For descending positive observations $X_{(1)}\ge\cdots\ge X_{(n)}$, its displayed estimator is

$$
\widehat\alpha=
\left[\frac1m\sum_{i=1}^{m}\log X_{(i)}-\log X_{(m)}\right]^{-1}.
$$

The threshold observation is included and contributes zero to the sum of log ratios. Some implementations instead use $k$ strict exceedances over $X_{(k+1)}$ and divide by $k$. The finite-sample conventions differ; reproducing the printed formula requires retaining the source's indexing rather than silently substituting a software default.

To make the proposed tail extrapolation explicit, choose threshold $u$ with empirical exceedance probability $\widehat p_u$. Approximating the slowly varying component as constant beyond $u$ gives

$$
\widehat P(X>x)=\widehat p_u(x/u)^{-\widehat\alpha},
\qquad
\widehat q_{1-p}=u(\widehat p_u/p)^{1/\widehat\alpha},
\quad p<\widehat p_u.
$$

These formulas are derived from the tail model, not numerical estimates reported in the paper. If $u=X_{(m)}$ in a sample without ties, there are $m-1$ strict exceedances; whether to use $(m-1)/n$ or the asymptotically equivalent $m/n$ must be recorded. Ties and threshold selection require further decisions.

The article invokes consistency and asymptotic normality under iid sampling and suitable growth of $m$. The familiar intermediate-order requirement is $m\to\infty$ with $m/n\to0$; centered normal inference additionally depends on controlling second-order tail bias. Neither a threshold selector nor a second-order model is supplied. Too small a tail sample produces variance; too low a threshold contaminates the tail approximation. An extrapolated hundred-year event probability is especially sensitive to the fitted exponent and to assumptions about time aggregation and independence.

There is no empirical Hill estimate, selected $m$, tail plot, quantile estimate, standard error, or tail-backtesting result in this paper. Its tail section offers a methodology and a warning, not a completed extreme-risk calibration. More daily observations do not create more independent historical regimes, and the authors explicitly caution against pretending that a short history precisely identifies a once-in-a-century event. Their comparison with the number of nonoverlapping century-length intervals is a warning about information content, not an exact effective-sample-size theorem for a specified tail estimator.

Finally, weak dependence in a central interval-hit sequence does not establish iid tail observations. Dependence may remain in signs, magnitudes, or more extreme thresholds. The transition from the horizon tests to iid EVT is therefore an additional modeling judgment. A replication should report it as such, retain the full return series, test tail-clustering sensitivity, and show how results vary with threshold and horizon.

## Reimplementation boundary

The model-based portion is reconstructable from the stated parameters and equations, including the distinction between daily-information forecasts and weak-GARCH aggregation. The historical hit experiment requires the original return data and several unreported threshold and resampling choices. The EVT proposal requires a tail definition and estimation design that are not supplied at all. None of these missing items should be filled by presenting invented chart values or tail-risk estimates as the authors' results.

The paper supports matching a model to the horizon and information set of the decision, checking forecast adequacy directly, and treating tail extrapolation as an assumption-sensitive statistical exercise. Its strongest general statements about a ten-to-fifteen-day boundary go beyond what nonrejection in the displayed tests alone can establish.
