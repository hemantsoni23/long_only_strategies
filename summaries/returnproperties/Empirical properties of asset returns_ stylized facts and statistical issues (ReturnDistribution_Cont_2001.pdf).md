# Empirical properties of asset returns: stylized facts and statistical issues

**Rama Cont (2001).** *Quantitative Finance* 1, 223–236. Source: [ReturnDistribution_Cont_2001.pdf](../../Finance/ReturnDistribution_Cont_2001.pdf). This note covers the full 14-page article. Page references below use journal pagination.

## Why this matters

A return model can fit a histogram and still fail almost every economically relevant time-series diagnostic. Cont assembles a set of empirical restrictions that recur across instruments and markets, explains their mathematical implications, and identifies statistical obstacles to testing them. The contribution is a synthesis and a model-evaluation agenda, rather than a new fitted stochastic process or a trading strategy. Its strongest message is that volatility dependence, marginal tail behavior, sampling frequency, and estimation uncertainty have to be considered together.

For an implementation team, the paper is useful as a specification for a diagnostic suite. A Gaussian independent-return benchmark misses heavy tails and volatility clustering. A heavy-tailed independent model repairs the marginal distribution but still misses the dependence of absolute returns. A conditionally Gaussian volatility model may reproduce clustering while leaving heavy tails in its standardized residuals. A multivariate model that matches contemporaneous correlations can still misrepresent joint losses. These are different failures, and a single likelihood, kurtosis estimate, or in-sample fit does not separate them.

The source draws on many studies and illustrates selected features with its own plots. It does not supply a unified dataset, code, or one experimental protocol that generated every numerical statement. The equations and procedures below make its diagnostics implementable; explicit implementation choices beyond those reported are identified as such. Several printed mathematical expressions also require correction before use.

## Object of analysis and the role of the sampling clock

For price $S(t)>0$, the basic observation is the log return over interval $\Delta$,

$$
r(t,\Delta)=\log S(t+\Delta)-\log S(t).
$$

Log returns add across adjacent intervals. Simple returns instead compound, so their tail and moment calculations should not be silently substituted for the log-return calculations in the article. The sampling interval is part of the definition of the random variable, not an innocuous display setting. The source discusses intraday through monthly behavior; a distributional fit at five minutes is not a distributional fit at one month.

Calendar time is only one possible clock. Trading activity, transaction count, or volume can define alternative operational times, and predictable intraday activity patterns can be removed before measuring dependence. Such transformations can change observed stationarity and volatility persistence. They must therefore be recorded as preprocessing, rather than presented as neutral ways of revealing a uniquely defined underlying series.

Cont emphasizes that economic time series are not automatically stationary or ergodic. Pooling observations across changing regimes can manufacture heavy unconditional tails or long-looking dependence. Conversely, long memory does not itself establish non-ergodicity. A reproducible diagnostic should specify the interval on which stationarity is being treated as an approximation and check whether conclusions survive changes in that interval. The source does not prescribe an optimal break detector or rolling-window length.

The effective information in a dataset can be far smaller than the number of recorded ticks. Five years of daily data provide only about a thousand observations, and tail events form a small subset of those. Serial dependence further limits precision. Treating a long high-frequency file as millions of independent draws creates confidence intervals that can be much narrower than justified.

## The empirical restrictions

Section 3 collects eleven recurring properties. They should be read as approximate empirical regularities, with asset-class and time-scale qualifications, rather than universal axioms.

| Property | Operational meaning and qualification |
|---|---|
| Little linear autocorrelation | Raw returns typically have weak autocorrelation beyond very short intervals; microstructure effects matter below roughly 15–20 minutes. |
| Heavy unconditional tails | Return distributions contain many more extreme observations than a Gaussian benchmark; reported tail indices are often between approximately 2 and 5. |
| Gain/loss asymmetry | Large equity declines and advances need not have the same distribution; the same asymmetry is less evident in exchange rates. |
| Aggregational Gaussianity | As the return horizon increases, the central distribution becomes more Gaussian-looking. This is a finite-horizon observation, not evidence that all relevant moments exist. |
| Intermittency | Periods of low activity alternate with bursts of large fluctuations. |
| Volatility clustering | Large absolute returns tend to be followed by large absolute returns, even when signed-return autocorrelation is small. |
| Conditional heavy tails | Standardization by an estimated volatility process does not necessarily produce Gaussian residuals. |
| Slow decay in volatility dependence | Correlations of absolute returns can remain positive for long lags, often approximating a power decay. |
| Leverage effect | Negative returns tend to precede increased volatility, with a directional time asymmetry. |
| Volume/volatility association | Measures of trading activity and return variability are positively related. |
| Asymmetry across time scales | Coarse-scale volatility is often more informative about subsequent fine-scale volatility than the reverse relation. |

The list is intentionally broader than the behavior of second moments. A model can have zero return autocorrelations while exhibiting strong nonlinear predictability. This is compatible with unpredictability of the conditional mean and does not, by itself, establish a profitable directional strategy.

The paper does not give a complete empirical replication for volume or cross-scale asymmetry. These are documented literature findings included in the constraint set. Reproducing them requires selecting particular volume definitions, non-overlapping horizons, lead/lag conventions, and markets, none of which should be attributed to this article without an additional source.

## Heavy tails, moments, and why kurtosis is unstable

A useful tail characterization is the moment index

$$
\kappa=\sup\{q>0:E|r|^q<\infty\}.
$$

For regularly varying tails, the survival probability has the form

$$
P(|r|>x)\sim L(x)x^{-\alpha},\qquad x\to\infty,
$$

where $L$ varies slowly. Positive moments below $\alpha$ exist and those above $\alpha$ do not; the boundary requires separate examination. The survival probability, rather than the cumulative distribution converging to one, is the object intended by the tail expression around equation (13).

Cont reports evidence consistent with finite return variance and tails substantially heavier than Gaussian tails. This excludes stable laws with index strictly below two as a literal full-distribution description when finite variance is accepted. It does not establish an exact universal cubic law or uniquely choose between all heavy-tailed parametric families. Tail behavior is difficult to distinguish over a limited empirical range, particularly when volatility changes through time.

Table 1 reports five-minute increments for S&P 500 futures, USD/DEM, and USD/CHF. The mean-to-standard-deviation ratios are approximately 0.003, 0.002, and 0.002; skewness is −0.40, −0.11, and −0.10; excess kurtosis is 15.95, 74, and 60. These are sample statistics. The paper also displays very small nominal intervals under independence assumptions, but warns that the assumptions supporting conventional inference are inappropriate in this setting. A kurtosis of 74 is not a precisely estimated population parameter merely because it was calculated from many intraday observations.

The moment hierarchy explains the issue. Estimating a second moment requires that moment to exist; conventional variance formulas for its sampling error require a fourth moment. A fourth-moment estimator has much stronger uncertainty requirements, often involving an eighth moment. When an underlying tail index is near or below these thresholds, the empirical statistic can be dominated by a few observations. Dependence creates an additional problem even when the moments exist.

Figure 3 illustrates stabilization of the empirical second moment for five-minute S&P 500 futures returns over 1991–1995. Figure 4 uses simulated Student-$t$ observations with four degrees of freedom to demonstrate instability of the empirical fourth moment. For that distribution the fourth moment is infinite. The illustration should not be described as ordinary noisy convergence to a finite kurtosis. It shows why a finite sample can report a numerical higher moment even when there is no finite population quantity for it to estimate.

A practical replication would examine running moment estimates and their sensitivity to removing a small number of extreme observations. That is a diagnostic, not permission to delete economically meaningful crashes. Winsorized results concern a transformed distribution and must be labeled accordingly. Similarly, standardizing returns using a fitted conditional scale tests a different question from estimating the raw unconditional tail.

### Separating a sharp center from an extreme tail

Figure 2 compares a kernel density estimate of 30-minute S&P 500 futures changes with a Gaussian density. The empirical curve has a sharper center as well as heavier tails. A good tail approximation need not describe the center, and a visually convincing central density fit need not extrapolate to rare losses. The article therefore treats density fitting and extreme-value estimation as complementary questions rather than interchangeable exercises.

Cont argues that a flexible marginal family should distinguish location, overall scale, tail decay, and left/right asymmetry. That motivates at least four adjustable characteristics in a general asymmetric specification. This is a modeling recommendation, not a theorem that four estimated parameters identify the return-generating mechanism. The review mentions Student, generalized hyperbolic, normal inverse Gaussian, and truncated-stable alternatives, but does not estimate them all on a common holdout sample or declare a universally superior family.

The distinction between probability density and survival-tail exponents also matters operationally. If a sufficiently regular density behaves as $f(x)\propto x^{-(1+\alpha)}$, its survival probability behaves as $P(r>x)\propto x^{-\alpha}$. Regressing a log density and a log exceedance count therefore does not estimate the same slope without a one-unit adjustment. The source's moment-index discussion concerns the latter tail index. An implementation that compares reported exponents must record which object was fitted and whether the positive and negative tails were pooled.

Aggregation provides a separate diagnostic. One can form a longer-horizon log return by summing consecutive shorter-horizon returns, then compare standardized densities across horizons. But normalization by an empirical standard deviation does not make the observations independent, and overlapping long returns share observations mechanically. A nearly Gaussian-looking center at a monthly horizon can coexist with poorly estimated rare tails and persistent conditional variance. It cannot validate square-root-of-time tail-risk scaling without assumptions on dependence and the full loss distribution.

The source’s figures are illustrative rather than a complete reproducibility archive. In particular, the kernel and bandwidth for Figure 2 are not specified in the accompanying discussion, and quoted descriptive statistics draw on referenced studies. These omissions prevent exact numerical density reproduction from the article alone; they do not prevent implementing the distinction between central shape, tail decay, and temporal aggregation.

## Extreme-value estimation, with corrected formulas

Section 4.2 develops block extremes as a way of focusing on the tails. Partition the series into $N$ non-overlapping blocks of $n$ observations and compute a maximum in each block. For the loss tail, apply the same construction to negative returns so that the maxima represent losses. The independent-sample extreme-value theorem states that, if suitable normalizing sequences exist, normalized maxima converge as the block size $n$ tends to infinity to a generalized extreme-value law.

Writing $z=(x-\mu)/s$, with $s>0$, the distribution is

$$
H_\xi(z)=\exp\{-(1+\xi z)^{-1/\xi}\},\qquad 1+\xi z>0,
$$

and the continuous limit at $\xi=0$ is $\exp(-e^{-z})$. Positive $\xi$ corresponds to the Fréchet heavy-tail case and gives the power-tail relationship $\alpha=1/\xi$. Negative $\xi$ gives a finite upper endpoint in the Weibull domain; zero gives the Gumbel domain. Domain-of-attraction conditions remain necessary: merely naming a finite endpoint does not prove convergence to a particular extreme-value law.

For block maxima $x_i$, maximum likelihood uses

$$
\ell(\mu,s,\xi)=\sum_{i=1}^N\left[-\log s-\left(1+\frac1\xi\right)\log u_i-u_i^{-1/\xi}\right],
\qquad u_i=1+\xi\frac{x_i-\mu}{s}>0.
$$

This corrects a sign in the exponent of the last term of the printed equation (12), on p. 228. Differentiating the displayed GEV distribution produces $u_i^{-1/\xi}$, not $u_i^{1/\xi}$. Equation (8) also prints a limit in $x$ where the theorem concerns increasing block size. These are implementation-relevant corrections, not alternative model choices.

The article quotes shape estimates around 0.2–0.4 for several financial series. Through $\alpha=1/\xi$, those particular values imply indices around 2.5–5. They should not be conflated with the wider 2–5 range reported across the literature. The paper’s broad statement concerning the asymptotic regularity of GEV likelihood estimators should not replace a check of the relevant regularity conditions, particularly near endpoint cases.

The bias/variance tradeoff is intrinsic. Larger blocks improve the asymptotic approximation but leave fewer maxima. Smaller blocks provide more observations but may not resemble the limiting distribution. Serially clustered extremes also violate a literal independent-block argument unless dependence conditions or a suitable correction are established. The paper supplies neither a universal block length nor a complete dependence-adjusted uncertainty procedure. A faithful implementation should report results across plausible block lengths and explain its treatment of clustered extremes, rather than fabricate a single recommended setting.

The VaR discussion is an application of tail probabilities, not a worked portfolio backtest. A portfolio loss quantile requires a horizon, tail probability, return convention, and sign convention. Multiplying log returns directly by wealth is only an approximation to wealth changes; exact simple-return losses use the exponential transformation. These conventions become material in the extreme tail.

## Nonlinear temporal dependence

For $q>0$, define

$$
C_q(k)=\operatorname{Corr}(|r_{t+k}|^q,|r_t|^q).
$$

Sections 5.1–5.2 distinguish $C_q$ from the ordinary autocorrelation of signed returns. In many reported series, $C_1$ decays slowly, with approximate power-law behavior $C_1(k)\propto k^{-\beta}$ and $\beta$ around 0.2–0.4. An exponential-decay model can mimic such a shape over a finite interval, so a log-log plot alone cannot establish genuine asymptotic long memory.

The familiar Taylor effect means dependence can be stronger for absolute returns than for squared returns, with the maximum over powers often near $q=1$. It is a comparative empirical statement, not a theorem that every dataset’s maximizing exponent must equal one. A reproducible diagnostic evaluates a fixed grid of exponents and lags, reports its search range, and distinguishes an observed maximum from a statistically significant difference.

Moment conditions become more stringent as $q$ increases. Defining the variance of $|r|^q$ requires $E|r|^{2q}<\infty$. Squared-return autocorrelation therefore relies on a fourth moment, while absolute-return autocorrelation requires a second moment. This provides a substantive reason to prefer the latter when the fourth moment is doubtful. It does not eliminate sampling uncertainty or automatically justify Gaussian standard errors.

Cont also considers transforms such as $\log(1+r^2)$ and bounded functions. These can reduce the domination of a few extreme observations and test whether nonlinear dependence persists under transformations with different tail sensitivity. Figure 8 uses S&P 500 futures observations from 1991–1995. Dependence in a bounded transform cannot be dismissed as merely an artifact of estimating an infinite fourth moment.

A related logarithmic statistic concerns correlations of $\log|r|$. Exact zero returns require a specified treatment; adding an arbitrary small constant changes the result and is an implementation choice. An approximate logarithmic decay reported over a finite range does not imply a globally valid formula at arbitrarily large lags.

The common representation $r_t=\sigma_t\epsilon_t$ is useful but introduces latent objects. Observed absolute or squared returns can be studied without specifying a volatility model; an estimated $\sigma_t$ depends on the chosen filtering procedure. A claim that residual tails remain heavy should specify whether the scale was estimated using only information available before the return, because smoothing with future information can alter the residual distribution.

## Leverage and directional asymmetry

A convenient statistic is

$$
L(k)=\operatorname{Corr}(r_{t+k}^2,r_t).
$$

With this convention, positive $k$ asks whether a signed return predicts future squared returns. The stock-return leverage pattern is negative at positive lags and much weaker when the order is reversed. This is not inconsistent with the algebraic symmetry of covariance: reversing the time order while keeping the two different transformations attached to their original roles is a different statistic.

The word leverage should not be treated as proof of a unique balance-sheet mechanism. Several economic or statistical mechanisms can produce an asymmetric return/volatility relationship. The paper reports the pattern as a model restriction and notes differences across asset classes. It does not estimate a structural causal coefficient identifying one mechanism.

For implementation, use an explicit lead/lag convention, demean consistently, and specify whether the variance proxy covers the following day, an overlapping interval, or an intraday block. Overlap can generate dependence mechanically. The source does not provide a universal lag cutoff or an optimal trade based on this statistic.

## Cross-sectional dependence and extreme co-movement

Section 6 examines the limitations of empirical covariance and correlation matrices. If $\Sigma$ is the covariance matrix and $D$ contains marginal standard deviations, the correlation matrix is

$$
R=D^{-1}\Sigma D^{-1}.
$$

Volatility variation can change covariance while leaving correlation comparatively stable, and correlation itself can change. These effects should be separated when comparing regimes. A factor decomposition can identify broad common movements, but its residual correlation structure still needs assessment.

The paper discusses a study of 406 NYSE stocks in which the largest eigenvalue represents a market component, a further small collection of eigenvalues contains visible structure, and much of the remaining spectrum resembles a random-matrix benchmark. The article does not supply all the sample construction and threshold details needed to reproduce that study. Resemblance to a noise benchmark is not proof that every smaller component is economically useless, nor does it establish a unique optimal covariance-cleaning rule.

For losses, a more direct object is

$$
P(r_i<-x\mid r_j<-y).
$$

Using each asset’s own loss quantile makes thresholds comparable across scales. For example, if $q_i$ is the positive magnitude of a selected lower-tail cutoff, the conditioning event is $r_j<-q_j$. Mixing a negative return quantile with an additional minus sign would reverse the event, so an implementation must state its convention.

Zero Pearson correlation does not imply independent extreme losses. Conversely, a finite-threshold conditional exceedance frequency does not prove nonzero asymptotic tail dependence as the threshold moves to the endpoint. At a 99% threshold, the conditioning sample contains roughly one observation in a hundred before accounting for dependence. This scarcity is central to uncertainty, especially when many asset pairs are examined. The source points toward multivariate extreme-value methods and copulas but does not provide a fitted multivariate extreme-loss model.

## Path regularity and multiscaling: what is and is not established

Section 7 asks whether a stochastic process reproduces the irregularity of observed paths, rather than only distributions at a single horizon. A local Hölder description compares a function near $t_0$ with a polynomial $P$:

$$
|f(t)-P(t-t_0)|\le K|t-t_0|^h.
$$

The polynomial has degree below $h$. The local exponent describes the best such approximation, while the singularity spectrum $D(\alpha)$ is the Hausdorff dimension of times with exponent $\alpha$.

Two statements on p. 232 require care. For fractional Brownian motion with Hurst parameter $H$, the familiar local regularity is $H$, not the printed reciprocal $1/H$. Also, reaching exponent one does not by itself prove differentiability: a Lipschitz cusp is a counterexample. These corrections matter if the paper is used to validate simulated paths.

Structure functions estimate scaling of absolute return moments,

$$
E|r(t,\Delta)|^q\propto\Delta^{\zeta(q)}.
$$

For a monofractal fractional Brownian benchmark, $\zeta(q)=qH$ where the moment exists. A nonlinear empirical curve motivates a multifractal description. Under the relevant multifractal formalism, the connection is

$$
\zeta(q)=\inf_\alpha\{q\alpha+1-D(\alpha)\}.
$$

Recovering a spectrum through a Legendre transform requires conditions; in general the transform can describe a concave envelope rather than uniquely reconstruct arbitrary local geometry. Sample paths observed on a finite grid do not reveal the limiting spectrum without estimation error.

The source reports approximately inverted-parabolic spectra over a range of exponents around 0.3–0.9, with a maximum near 0.55–0.6, while stressing that apparent multifractal behavior can be spurious. A smooth deterministic function can produce misleading finite-sample scaling estimates. Similarly, a fitted spectrum cannot prove that a financial price process has no jumps: rare jumps can be missed or obscured at the observed resolution.

Replication requires a declared range of time scales, aggregation convention, moment orders, minimum observations per scale, and treatment of intraday seasonality. Positive high-order moments may not exist under the estimated tail behavior; negative moments create separate difficulties near zero returns. The article provides the conceptual framework, not a complete estimator with all these tuning choices fixed.

## A source-grounded diagnostic workflow and its limits

An implementation based on this paper should first define instruments, price adjustments, trading sessions, and sampling clocks. It should then form consistently aligned returns at several horizons; inspect marginal asymmetry and tails; examine running second and higher moments; compare raw-return and transformed-return dependence; calculate directional leverage statistics; and assess both ordinary and extreme cross-asset dependence. Path-scaling analysis belongs after the team has established that its chosen moment orders and scales are meaningful.

For each proposed model, simulate data with the same observation scheme and sample length, then recompute the same diagnostics. Comparing finite-sample distributions of diagnostics is more informative than comparing a single fitted parameter with a stylized numerical range. This is an implementation implication of the article, not an experiment performed and reported in it. There is no specified simulation count, fitting objective, model-selection penalty, or forecasting holdout in the source.

The most useful acceptance criterion is multidimensional. A candidate should reproduce the features relevant to its intended use without relying on incompatible moment assumptions. A short-horizon execution model may need microstructure behavior that a monthly asset-allocation model can omit. A tail-risk model needs dependence in extreme losses that a mean-return model may not identify. Matching one stylized fact is evidence about one aspect of adequacy, not validation of an investment decision.

The review establishes a disciplined starting point and several important reasons why common summary statistics can mislead. It does not provide expected trading profits, transaction-cost estimates, or a claim that statistical predictability in volatility transfers directly into net alpha. The practical payoff is a more demanding and reproducible test of the assumptions underneath a quantitative model.
