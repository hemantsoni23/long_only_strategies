# Discussion of “Copulas: Tales and facts”, by Thomas Mikosch

Christian Genest and Bruno Rémillard (2006). *Extremes* 9, 27–36. DOI: 10.1007/s10687-006-0018-7. Published online November 3, 2006. [Source PDF](<../../Finance/Copulas/[Genest, Remillard] - Discussion of Copulas Tales and Facts 2006.pdf>), 10 pages. All pages, the four-panel Figure 1, the displayed error bound, and references were read. PDF p. 1 is journal p. 27; subsequent page references use PDF numbering.

## Why this matters

This discussion clarifies what copula modeling is intended to estimate. A joint return distribution contains both marginal behavior and association. Some questions, including portfolio loss quantiles, require both. Others, including independence, are invariant to strictly increasing changes of the marginal scales. Treating every dependence question as if it required the full distribution obscures why rank-based inference can be useful.

The authors respond to [Mikosch's critique](<../../Finance/Copulas/[Mikosch] - Copulas Tales and Facts 2006.pdf>) with three concrete arguments. Uniform ranks are a natural coordinate system for invariant inference. Copulas can specify serial as well as contemporaneous dependence. Finally, a deterministic Lipschitz inequality controls the joint-CDF error produced by separately estimated marginals and a copula. That last result directly answers a narrowly formulated version of the claim that good separate fits need not yield a good joint fit.

The paper is a ten-page discussion, not a new trading model, a tail-forecast competition, or a complete estimation manual. Its only numerical design is a 1,000-observation graphical illustration. It cites an existing body of estimation and goodness-of-fit research rather than proving those asymptotic results here. The technical reconstruction below makes its central claims usable without attributing additional experiments or algorithms to the authors.

## The disagreement is partly about the statistical target

Let $X=(X_1,\ldots,X_d)$ have continuous marginal CDFs $F_1,\ldots,F_d$ and joint CDF $H$. Write

$$
H(x_1,\ldots,x_d)=C(F_1(x_1),\ldots,F_d(x_d)).
$$

The copula $C$ is the joint CDF of $U_i=F_i(X_i)$. It describes the association left after removing the individual distributional scales. Under strictly increasing transformations $Y_i=g_i(X_i)$, the marginal CDFs change but the copula does not.

This invariance is not a claim that every statistic of the vector remains fixed. Pearson correlation, covariance, tail-loss magnitudes, and the quantile of a weighted sum can change. Independence, concordance ordering, and the copula remain unchanged. The correct estimator depends on which of those objects is the target.

The authors treat the margins as nuisance parameters when the objective is association. If the objective is a monetary loss distribution, those margins become economically essential. Multiplying all returns by a large positive constant leaves their ranks intact and scales the losses. That observation supports separation of the two tasks; it does not refute estimating the invariant task from ranks.

There is a sigma-algebra interpretation. A strictly increasing invertible transformation of a variable generates the same information as the original variable. Dependence concepts defined through the sigma-algebras can therefore be invariant even when numerical correlations are not. The discussion mentions mixing and correlation-type dependence concepts to emphasize that marginal invariance is not a special trick invented solely for copulas.

For continuous samples without ties, componentwise ranks are maximal invariant statistics under separate increasing transformations: two samples have the same ordering in each coordinate if and only if appropriate increasing coordinate maps can map one set of observed values to the other. An inferential procedure deliberately invariant to those transformations should depend on this ordering information rather than on arbitrary measurement units.

Continuity is a material assumption. With ties, censoring, ordinal observations, or discrete default indicators, ranks and probability transforms require additional conventions, and a joint distribution need not identify a unique copula away from the marginal probability grid. The discussion does not develop those extensions. Its argument should not be imported unchanged into a discrete credit dataset.

## Uniforms, empirical processes, and a practical rank representation

The source connects uniform margins to the familiar empirical-process limit. For iid observations with continuous CDF $F$, the centered empirical CDF process has a Brownian-bridge representation in its limit:

$$
\sqrt n(F_n-F)\ \Rightarrow\ \mathbb B\circ F,
$$

where $\mathbb B$ is a standard Brownian bridge on $[0,1]$. The common probability scale exposes the part of the limit law that is independent of the unknown continuous $F$. This is the authors' theoretical answer to the suggestion that uniforms were chosen merely because a unit square is convenient to plot.

A useful implementation starts with a synchronized $n\times d$ sample, computes each column's ranks $R_{ti}$, and forms pseudo-observations

$$
\widehat U_{ti}=\frac{R_{ti}}{n+1}.
$$

The denominator $n+1$ is an explicit implementation choice here, avoiding endpoints that cause singularities in inverse-normal, inverse-exponential, or copula-density calculations. The paper calls the inputs normalized ranks but does not specify a denominator. The rank-based empirical joint distribution is

$$
C_n(u)=\frac1n\sum_{t=1}^n
\prod_{i=1}^d\mathbf1\{\widehat U_{ti}\le u_i\}.
$$

At finite $n$, this step function has discrete rank-grid margins rather than exactly continuous uniform margins. It is the standard empirical object used to approximate the copula; if a genuine continuous copula is needed for simulation, an interpolation or another construction must be specified separately.

Exponential coordinates are available through $T(u)=-\log(1-u)$. But they do not avoid estimating the probability scale: they generally begin with the same uniforms or normalized ranks and then apply another transformation. Uniform coordinates are bounded and make the independence density constant over the square. Exponential coordinates stretch the upper tail and compress the large mass near the origin. Each can be useful, but they display density differently.

The Brownian-bridge argument should not be read as a complete null distribution for every fitted empirical-copula statistic. Estimated marginal distributions and estimated copula parameters alter the relevant empirical process. Time dependence also changes inference. The paper's references supply the specialized theory; the displayed univariate analogy alone is not a license to use iid critical values on financial time series.

## Reconstructing the four-panel experiment

Figure 1 on PDF p. 7 compares two bivariate models and two coordinate systems. Each model contributes 1,000 observations. The upper pair uses independence. The lower pair uses a Gumbel copula with population Kendall's tau $3/4$. Left panels plot normalized ranks; right panels apply $T(u)=-\log(1-u)$ coordinatewise. The source specifies neither a random seed nor the exact simulation routine or rank normalization, so its precise point locations cannot be recovered.

For a conventional Gumbel parameter $\theta\ge1$,

$$
C_\theta(u,v)=
\exp\left[-\{(-\log u)^\theta+(-\log v)^\theta\}^{1/\theta}\right],
\qquad
\tau=1-\frac1\theta.
$$

Thus the stated $\tau=3/4$ corresponds to $\theta=4$. In Mikosch's reciprocal parameterization, the same model has $\alpha=1/4$. Confusing these parameterizations would produce a different graph and, potentially, an invalid parameter value.

One reproducible simulation construction, derived here rather than specified in the article, uses conditional inversion. Draw independent $U,W\sim\mathrm{Uniform}(0,1)$, set $a=-\log U$, and solve for $V\in(0,1)$ from

$$
W=\partial_1 C_\theta(U,V)
=\frac{C_\theta(U,V)}{U}
\{a^\theta+(-\log V)^\theta\}^{1/\theta-1}a^{\theta-1}.
$$

The right side is the conditional CDF of $V$ given $U$. A bracketed scalar root solve produces each pair. Working with logarithms and excluding exact random endpoints improves numerical stability. For the independence panels, draw $U,V$ independently instead. Rank each simulated column, then generate both plots from the same ranked observations. Using separate random samples for the uniform and exponential panels would unnecessarily confound the coordinate transformation with sampling variation.

The top-left panel is broadly homogeneous. The top-right panel has many observations near zero and fewer large values on either axis, creating a wedge-like visual concentration. The variables nevertheless remain independent: their transformed joint density is the product of two exponential densities. Visual density concentration is not evidence of association.

The lower-left Gumbel panel visibly concentrates toward the diagonal and especially toward the upper-right tail. The lower-right plot places much of its visible point mass near the origin, which can distract from the copula's upper-tail association. The authors argue that the rank plot makes the association easier to interpret. This is a graphical demonstration, not a blinded perception study or a statistically tested claim about how all readers interpret charts.

The population tail coefficients give useful numerical checks of the intended model:

$$
\lambda_U=2-2^{1/\theta}=2-2^{1/4}\approx0.810793,
\qquad \lambda_L=0
$$

for $\theta=4$. These are derived properties of the stated Gumbel model, not estimates reported in the figure. Independence has both coefficients zero. A sample of 1,000 observations cannot by itself establish an asymptotic tail limit; a high empirical threshold leaves few observations from which to estimate a conditional exceedance probability.

The article reports no sample tau, sample Pearson correlation, Monte Carlo standard error, repeated simulations, empirical coverage rate, or forecasting loss. Replicating the model and qualitative visual comparison is possible from the description. Reproducing exact plotted dots or claiming a numerical superiority of one coordinate system is not.

## The joint-CDF error bound and its proof

The most useful displayed result appears on PDF p. 9. Let $\widehat C$ estimate $C$, let $\widehat F_i$ estimate $F_i$, and reconstruct

$$
\widehat H(x)=
\widehat C(\widehat F_1(x_1),\ldots,\widehat F_d(x_d)).
$$

Every copula is Lipschitz with constant one in each coordinate:

$$
|C(u)-C(v)|\le\sum_{i=1}^d|u_i-v_i|.
$$

To see why, change coordinates one at a time. The probability change from altering only coordinate $i$ cannot exceed the uniform marginal probability of the strip between its two thresholds, namely $|u_i-v_i|$. Summing those changes proves the inequality without requiring a copula density or differentiability.

Add and subtract $C(\widehat F_1(x_1),\ldots,\widehat F_d(x_d))$ inside the estimation error. The triangle inequality separates a copula error evaluated at estimated marginal probabilities from the effect of changing the arguments of the true copula. Consequently,

$$
\begin{aligned}
\|\widehat H-H\|_\infty
&\le
\|\widehat C-C\|_\infty
+\sum_{i=1}^d\|\widehat F_i-F_i\|_\infty .
\end{aligned}
$$

The result is deterministic: it applies to realized fits whenever the component sup-norm errors are defined. It does not assume that the marginal estimates are independent of the estimated copula or that they are calculated from separate datasets. A probabilistic consistency conclusion then follows if those errors converge to zero in the chosen probabilistic sense.

The dimension dependence remains visible. If every marginal has error at most $\varepsilon_F$ and the copula error is at most $\varepsilon_C$, the bound is $\varepsilon_C+d\varepsilon_F$, capped trivially by one for two valid CDFs. This can be loose, and it deteriorates as the dimension rises. Fixed-dimensional consistency does not automatically extend to an increasing number of assets without controlling the summed marginal error and copula estimation error.

The metric is also decisive. Joint-CDF sup norm concerns lower-orthant probabilities. It does not immediately give the same bound for every weighted portfolio half-space, density estimate, derivative price, or expected shortfall. Inclusion–exclusion can transfer CDF bounds to rectangular events but may accumulate several errors. Rare-event relative errors can still be large when absolute errors are small.

For example, a joint-event probability of order $10^{-4}$ is not accurately resolved merely because a CDF approximation has absolute error of order $10^{-2}$. Those values are an illustrative scale comparison supplied here, not a numerical case in the paper. Likewise, in a one-dimensional quantile problem, converting CDF error into a quantile error requires local behavior of the density. If the density near the target quantile is very small, a small probability error can produce a large error in return units.

The bound therefore supports modular estimation at the CDF level while leaving difficult risk-functional questions open. It refutes the categorical assertion that successful component fits cannot guarantee any successful joint fit. It does not prove that every two-stage estimator is efficient, that a misspecified copula family fits well, or that an extreme loss estimate is reliable.

## Copulas can specify a serial model

The authors' counterexample to a blanket rejection of copulas for time series is a stationary Markov chain. Let its continuous invariant marginal be $F$, and let the copula of successive states be $C$. Under smoothness sufficient for differentiation,

$$
P(X_{t+1}\le y\mid X_t=x)
=\partial_1C(F(x),F(y)).
$$

This formula follows by differentiating the joint probability with respect to the first marginal probability. On uniform coordinates, define the transition kernel $K(u,[0,v])=\partial_1C(u,v)$. Integrating it against a uniform current state gives

$$
\int_0^1K(u,[0,v])\,du=C(1,v)-C(0,v)=v.
$$

Thus a uniform starting state is invariant; applying $F^{-1}$ produces the desired marginal $F$. The marginal distribution and transition law specify all finite-dimensional distributions of the first-order Markov process. This explicit construction expands the brief argument on p. 5; it is not a financial model fitted in the discussion.

The scope should remain narrow. A bivariate copula of adjacent observations does not specify an arbitrary non-Markov process. Stationarity requires the chosen invariant initialization or a convergence argument. Ergodicity, mixing rates, tail clustering, and estimation uncertainty require additional conditions. A static cross-sectional copula estimated from raw returns also does not automatically become a valid conditional dependence model just because serial copula models exist.

The contribution is a decisive counterexample to impossibility, not a claim that copulas are always the easiest description of dynamics. An analyst can still prefer a direct autoregressive or stochastic-volatility representation when it gives clearer structure or more efficient estimation.

## Model choice, statistical literature, and economic calibration

The discussion traces copulas through earlier work on fixed marginals, association, survival analysis, frailty, extreme values, and rank-based inference. Its purpose is to show that the framework predates its financial popularity and has uses beyond fashionable model labeling. Marshall–Olkin mixture constructions and Oakes's frailty connection provide concrete reasons for considering Archimedean families. They do not imply that any one such family matches a particular asset panel.

For estimation, the authors cite consistency, two-stage efficiency, semiparametric efficiency, and goodness-of-fit work. They explicitly acknowledge that goodness-of-fit techniques were still developing and that some proposals lacked adequate theoretical support. The discussion itself does not provide the assumptions, limiting covariance matrices, or bootstrap algorithms from all those references. A research implementation must read the relevant primary estimation paper before claiming its asymptotic guarantee.

Their model-selection advice is deliberately conventional: use structural properties, diagnostics, cross-validation, and predictive performance. Mathematical tractability can be a legitimate reason to begin with a family, but it does not settle validation. Neither the criticism that a family is convenient nor the defense that it has a probabilistic construction establishes its empirical adequacy.

The paper also gives multi-name credit derivatives as a setting where association and margins may be informed by different observations. That example is not a supplied calibration exercise: it identifies no instrument panel, quote dates, recovery assumptions, pricing measure, estimator, or numerical result. In an actual application, the analyst must determine which instruments identify marginal default probabilities and which identify joint features, and must keep physical probabilities distinct from pricing probabilities. Margins and association cannot be combined from incompatible measures merely because they were estimated separately.

No transaction costs, portfolio holdings, rebalancing rules, financing assumptions, or net returns appear in this source. It provides a methodological argument about distributional modeling, not evidence for a market premium or implementable investment strategy.

## Research implementation and limitations

For an association study, first state the observational unit, synchronization rule, continuity assumptions, and whether the sample is iid or serially dependent. Rank-based diagnostics can then be applied to the appropriate observations or model residuals. For risk prediction, separately fit and assess the original-scale marginal distributions and recombine them with the association model before evaluating the intended payoff.

A minimal reconstruction of the figure should record the seed, $n=1{,}000$, the Gumbel parameterization, simulation method, numerical tolerance, rank denominator, and axis transformations. It should verify that applying the exponential map leaves ranks unchanged and does not create dependence in the independent model. The resulting graphic is a new realization of the stated experiment, not a recovery of the original random draws.

For a model-fit study, the CDF bound suggests reporting marginal fit and copula fit separately, then checking the actual economic functional as an additional target. Good overall lower-orthant fit can coexist with poor extreme-tail calibration. Conversely, a failure of one restricted parametric family is not a failure of the copula representation itself.

The paper's lasting result is a disciplined separation of representation, estimation target, and validation. Association can legitimately be treated as invariant to monotone marginal changes; monetary losses cannot. Copulas provide a coordinate system for that separation, and the Lipschitz inequality makes one part of its error propagation explicit. The article does not remove high-dimensional uncertainty, select a universal family, or supply the data and inferential details needed for a financial forecasting application.
