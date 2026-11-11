# Copulas: Tales and Facts

Thomas Mikosch. Local manuscript dated November 25, 2005, prepared as a discussion paper for *Extremes*. The filename identifies the subsequent 2006 work; the supplied text explicitly says that publication with discussion is forthcoming. [Source PDF](<../../Finance/Copulas/[Mikosch] - Copulas Tales and Facts 2006.pdf>), 13 pages. All pages and references were read; there is no appendix, empirical results table, or data figure. Page numbers below are PDF/manuscript pages.

## Why this matters

A copula separates the specification of marginal distributions from their joint association. That modularity is useful, but it can also encourage a risk analyst to treat the dependence model as if it supplied everything needed for portfolio loss estimation. Mikosch's central objection is that standardizing observations does not remove uncertainty about marginal tails, dependence, temporal dynamics, or high-dimensional estimation. A convenient parametric copula is still a substantive model assumption.

The paper is an argumentative methodological critique, not a new estimator or a comparative forecast study. Its most constructive content is the distinction between a scalar tail-dependence coefficient and a full multivariate tail measure. That distinction matters when an investment question concerns weighted portfolio losses, concentrations of extreme observations, or rare events different from two simultaneous threshold exceedances.

The strength of the article is its insistence on matching a model to the quantity being estimated. Several categorical statements go further than its mathematics supports, however. This note reconstructs the useful definitions and calculations without treating claims that copulas are inherently useless, or cannot describe time dependence, as established theorems. The contemporaneous [Genest–Rémillard discussion](<../../Finance/Copulas/[Genest, Remillard] - Discussion of Copulas Tales and Facts 2006.pdf>) directly contests those claims.

## What is preserved by a copula representation

Let $X=(X_1,\ldots,X_d)$ have joint CDF $H$ and continuous marginal CDFs $F_i$. The source initially assumes inverses on the marginal supports. Put $U_i=F_i(X_i)$; then each $U_i$ is uniform on $(0,1)$, and

$$
C(u_1,\ldots,u_d)=
H(F_1^{-1}(u_1),\ldots,F_d^{-1}(u_d)),
\qquad
H(x)=C(F_1(x_1),\ldots,F_d(x_d)).
$$

The unique copula $C$ together with the marginals determines the full joint law. The copula alone does not determine returns in their original units, their variances, their marginal tail indices, or the distribution of a portfolio's monetary payoff.

Mikosch stresses that Pearson correlations need not be preserved by the probability integral transform. That is correct: correlation is a functional of both marginal magnitudes and association. In contrast, independence and concordance are preserved by strictly increasing coordinate transformations. Kendall's tau and Spearman's rho summarize aspects of this invariant association. They are not complete descriptions of a multivariate law, but neither is Pearson correlation.

For example, multiplying one asset's returns by a positive leverage factor leaves its ranks and copula unchanged while changing the portfolio's risk. This does not show that a rank-based estimate is defective if its target is invariant association. It shows that a rank-based estimate cannot replace the marginal model in a question whose answer depends on leverage. The source's argument becomes most useful when the target functional is made explicit.

The article also distinguishes second-order from stronger process assumptions. A zero-autocorrelation process need not consist of independent observations, and a nonlinear transformation can expose dependence not visible in its covariance function. But an identical measurable transformation of a strictly stationary process remains strictly stationary. Thus the discussion on p. 2 should not be generalized into a claim that marginal standardization necessarily destroys stationarity. Weak stationarity alone is not preserved under arbitrary nonlinear transformations.

Uniform margins are one possible reference scale. The source writes the alternative exponential transform

$$
E_i=-\log(1-F_i(X_i)),
$$

which has unit exponential margins, and mentions normal, Pareto, unit Fréchet, and Gumbel scales. A normal marginal transformation does not make a vector jointly Gaussian. That is a legitimate warning about confusing marginal shape with joint shape; the source's additional description of non-Gaussian vectors with normal margins as pathological is a judgment, not a probabilistic restriction.

Uniform ranks are especially convenient for invariant inference, while Pareto or Fréchet margins make radial tail behavior easier to express. A modeler can choose the coordinate system appropriate to the task and retain inverse transformations. No particular reference scale eliminates the need to estimate unknown marginals.

## Portfolio quantiles: information required and simulation

For weights $w$ and return vector $X$, a signed lower-tail return quantile is

$$
q_p(w^\mathsf{T}X)
=\inf\{z:P(w^\mathsf{T}X\le z)\ge p\}.
$$

Positive loss VaR changes the sign and probability convention appropriately. A copula by itself cannot evaluate this object because the same $C$ can be combined with arbitrarily different marginal scales and tails. Conversely, marginal distributions alone are also insufficient. The question depends on both.

Given fitted marginals and a simulable copula, the reconstruction is straightforward: draw $U^{(b)}\sim \widehat C$, set $X_i^{(b)}=\widehat F_i^{-1}(U_i^{(b)})$, compute $w^\mathsf{T}X^{(b)}$, and estimate its quantile from repeated draws. This is the Monte Carlo use acknowledged on p. 5. The paper does not supply a chosen portfolio, fitted parameters, simulation count, seed, quantile convention, or runtime comparison.

Its critique of simulation cost is qualitative. The relevant distinction is between numerical error conditional on a fitted model and statistical error in that model. Increasing the number of Monte Carlo draws reduces the former but does not supply missing tail observations or correct an inappropriate copula family. At tail probability $p$, a simulation of size $B$ has only about $Bp$ draws in that tail; this elementary diagnostic is an implementation consequence, not a numerical experiment in the article.

Mikosch suggests that modeling a particular aggregate return series directly may sometimes be more efficient than modeling all constituents. That can be sensible for a fixed portfolio. It is less reusable when weights change, when individual positions require separate pricing, or when one must assess allocations not observed historically. The paper does not compare these alternatives empirically, so it does not establish which forecasts better.

## Estimation: marginal errors and dimensionality

Section 6 identifies three approaches to the marginals: parametric distributions, empirical CDFs, and empirical central distributions combined with fitted generalized-Pareto tails. Each has a different source of approximation error. Parametric fits can miss skewness or tail shape. Empirical CDFs cannot extrapolate beyond observed support. Tail splicing adds threshold selection, tail-parameter uncertainty, and continuity conventions.

In a rank-based fit, pseudo-observations depend on the marginal empirical ranks rather than the original units. An implementation may use $R_{ti}/(n+1)$ to avoid exactly zero or one, but the paper does not prescribe that convention. Ties, censored observations, and discrete default data also require decisions; the source's continuous-margin derivation does not resolve them.

A full parametric likelihood, when densities exist, factors as

$$
\ell(\theta,\eta_1,\ldots,\eta_d)
=\sum_{t=1}^n
\left[
\log c_\theta(F_{1,\eta_1}(X_{t1}),\ldots,F_{d,\eta_d}(X_{td}))
+\sum_{i=1}^d\log f_{i,\eta_i}(X_{ti})
\right].
$$

This expression is supplied here to make the article's estimation discussion executable; it is not a new estimator proposed by Mikosch. Joint maximization and a two-stage marginal-then-copula fit generally have different information matrices. The second stage uses estimated inputs, so uncertainty should not automatically be calculated as if the probability integral transforms were known. Whether joint fitting is more efficient depends on the models, the estimator, and the maintained regularity conditions.

The source argues that separate estimation necessarily incurs much greater uncertainty. That conclusion is not established by an efficiency calculation in the paper. A copula factorization of a fixed parametric joint family does not itself add parameters. Flexibility adds parameters when the analyst replaces a restrictive joint family by freely specified marginals and association. The comparison must hold the model and target fixed before attributing a cost to factorization.

The high-dimensional warning is concrete. The article considers roughly 500 daily observations on 200 assets. An unrestricted correlation matrix has $200(199)/2=19{,}900$ off-diagonal parameters before adding marginal parameters. This calculation does not prove that estimation is impossible—structured, shrinkage, or factor approaches can reduce effective complexity—but it shows why a copula label is not a dimension-reduction method. The paper provides no tested regularizer or sample-size rule.

Its question about error propagation also needs a specified metric. The companion discussion gives the sup-norm bound

$$
\|\widehat H-H\|_\infty
\le \|\widehat C-C\|_\infty
+\sum_{i=1}^d\|\widehat F_i-F_i\|_\infty.
$$

Thus uniform CDF consistency of all pieces implies uniform joint-CDF consistency in fixed dimension. This answers one version of Mikosch's question but does not guarantee small relative error for rare events, stable extreme quantiles, or accurate portfolio expected shortfall. Those are stronger, target-specific requirements.

## The families under criticism

For a decreasing Archimedean generator $\psi$ with $\psi(1)=0$ and, in the strict case, $\psi(0)=\infty$, the article gives

$$
C(u_1,\ldots,u_d)=\psi^{-1}\!\left(\sum_{i=1}^d\psi(u_i)\right).
$$

Complete monotonicity of the inverse generator is a sufficient condition for validity in every dimension. The body on p. 7 says “completely comonotonic,” but its footnote correctly states the alternating-derivative condition

$$
(-1)^k\frac{d^k}{dt^k}\psi^{-1}(t)\ge0.
$$

These are different terms. The formula also changes a summation upper index from $d$ to $n$ in one line without introducing a new dimension; a consistent transcription uses $d$ throughout. These are local textual repairs, not author-issued errata.

Mikosch constructs independent variables with CDFs $G_i(x)=\exp[-\psi(F_i(x))]$ and rewrites the joint CDF as

$$
H(x)=\psi^{-1}\!\left[-\log\left\{\prod_iG_i(x_i)\right\}\right].
$$

This identity does not make the original $X_i$ independent. A nonlinear transformation of a joint CDF value is not the same as separate coordinate transformations of independent random variables. The useful modeling criticism is that a simple Archimedean family imposes a restrictive form of association, often exchangeable across coordinates. The identity alone does not demonstrate that such dependence is artificial. The companion discussion points to mixture and shared-frailty constructions as substantive interpretations.

For a Gaussian copula with correlation matrix $\Sigma$,

$$
C_\Sigma(u)=\Phi_\Sigma(\Phi^{-1}(u_1),\ldots,\Phi^{-1}(u_d)).
$$

For a Student copula with degrees of freedom $\nu$,

$$
C_{\Sigma,\nu}(u)=
t_{\Sigma,\nu}(t_\nu^{-1}(u_1),\ldots,t_\nu^{-1}(u_d)).
$$

The copula is obtained from an elliptical parent distribution but is not itself an elliptical distribution on the original unbounded scale. Combining it with arbitrary marginals does not generally produce an elliptical return vector. When $\nu\le2$, the Student parent lacks finite covariance; $\Sigma$ should then be understood as its standardized dispersion parameter, not a Pearson correlation matrix estimated from nonexistent population second moments.

The source uses the centered elliptical representation $X=RAS$, where $S$ is uniform on the Euclidean unit sphere, $R\ge0$ is independent of $S$, and $AA^\mathsf{T}=\Sigma$. It emphasizes the common radial shock and restrictions on the directions of extreme observations. That is an important structural limitation, but saying the dependence is entirely determined by covariances would be too strong. The radial distribution matters, and Student degrees of freedom affect tail association even at a fixed dispersion matrix. Moreover, a nonspherical $A$ can concentrate probability in preferred directions; “no pronounced directions” is not a general theorem without qualifications on that matrix.

The Gumbel family is parameterized here as in the source:

$$
C_\alpha(u)=
\exp\left[-\left\{\sum_{i=1}^d(-\log u_i)^{1/\alpha}\right\}^{\alpha}\right],
\qquad0<\alpha\le1.
$$

At $\alpha=1$ it gives independence; the limit $\alpha\downarrow0$ approaches complete positive dependence. It is both Archimedean and an extreme-value copula. With standard Gumbel margins $\Lambda(x)=\exp[-e^{-x}]$, substitution gives

$$
C_\alpha(\Lambda(x_1),\ldots,\Lambda(x_d))
=\exp\left[-\left\{\sum_i e^{-x_i/\alpha}\right\}^{\alpha}\right].
$$

Page 4 omits the outer negative sign in one definition of the Gumbel CDF; p. 8 supplies the valid expression used above. The printed positive-sign expression would exceed one and cannot be a CDF.

The paper argues that extreme-value distributions require a block-maximum generating mechanism and criticizes their use for ordinary daily returns. A more precise distinction is between a mechanistic justification, an asymptotic tail approximation, and a convenient working distribution. A model family can be empirically useful outside the literal mechanism that originally motivated it. The source supplies no data comparison proving that an extreme-value copula must fail for daily returns. Its warning is best interpreted as a demand for justification and validation of the imposed tail structure.

## Tail dependence is a summary, not a complete tail model

For equally distributed variables with right endpoint $x_F$, the upper-tail coefficient is

$$
\lambda_U=\lim_{z\uparrow x_F}P(Y>z\mid X>z),
$$

when the limit exists. With different continuous marginals, comparable probability levels give

$$
\lambda_U
=\lim_{u\uparrow1}
\frac{1-2u+C(u,u)}{1-u}.
$$

The copula formulation is useful precisely because it compares marginal quantile exceedances rather than equal numerical thresholds in unlike units. Lower-tail dependence is analogously $\lambda_L=\lim_{u\downarrow0}C(u,u)/u$.

Mikosch's key point is that $\lambda_U$ is only one limiting conditional probability. It does not specify the joint distribution at practical thresholds, the speed of convergence to the limit, the loss magnitudes after an exceedance, or every direction in which a large portfolio loss can occur. A matrix of pairwise tail coefficients likewise generally fails to identify a multivariate tail law.

For the bivariate Gumbel family above, $C_\alpha(u,u)=u^{2^\alpha}$, giving the derived value $\lambda_U=2-2^\alpha$. It ranges from zero at independence to one in the complete-dependence limit. That computation is a useful check of the parameterization, not a model-selection criterion. It does not imply that two families with the same coefficient have equivalent finite-threshold loss probabilities.

The article's strongest wording—that the coefficient is not a genuine extreme-value concept—reflects its preferred definition of extremes, encompassing magnitude and direction. The mathematically sound claim is narrower: a copula-only scalar cannot replace the full marginal-and-angular tail specification required for many risk functionals. Asymptotic independence, $\lambda_U=0$, also does not mean independence at all finite thresholds.

## Multivariate regular variation and the alternative rare-event calculation

Section 8.2 provides the principal constructive framework. Fix a norm and a reference set $B=\{x:\|x\|>1\}$. For sets $A$ bounded away from the origin, assume

$$
\nu_B(A)=
\lim_{u\to\infty}
\frac{P(X\in uA)}{P(\|X\|>u)}
$$

exists at appropriate continuity sets and defines a nontrivial tail measure. The article denotes this measure by $\lambda_B$; $\nu_B$ here avoids confusing it with the scalar coefficient. Its homogeneity is

$$
\nu_B(tA)=t^{-\beta}\nu_B(A),\qquad t>0,
$$

for tail index $\beta>0$. This formulation describes many rare-event regions, including half-spaces relevant to a linear portfolio, rather than just a simultaneous exceedance quadrant.

In polar coordinates, regular variation is equivalent to a radial tail law and an angular probability measure $G$ on the unit sphere:

$$
\lim_{u\to\infty}
\frac{P(\|X\|>tu,\ X/\|X\|\in S)}
{P(\|X\|>u)}
=t^{-\beta}G(S).
$$

Here $G$ is the limiting conditional distribution of direction given a large norm, and the boundary of $S$ must carry no limiting mass. The choice of norm changes the angular representation; the underlying rare-event probability must remain expressed in consistent coordinates. If margins have different tail orders, transformations or a nonstandard regular-variation formulation may be required before treating all coordinates with one radial scaling.

Equation (8.5) proposes

$$
P(X\in tuA)
\approx t^{-\widehat\beta}\widehat\nu_B(A)
\frac1n\sum_{j=1}^n\mathbf1\{\|X_j\|>u\}.
$$

Its ingredients are an estimated tail index, an estimated tail measure or angular distribution, a threshold, and the observed radial exceedance frequency. The paper does not choose a tail-index estimator, threshold-selection algorithm, smoothing method for $G$, dependence correction, or uncertainty interval. It explicitly acknowledges that estimating directions in high dimension is difficult and requires substantial tail data.

A reconstruction would select the risk event $A$ first, choose the norm and marginal standardization, examine radial and angular stability over thresholds, estimate the required tail functional, and evaluate the extrapolation at $tu$. For a portfolio loss $w^\mathsf{T}X>x$, the relevant region is a half-space with sign conventions fixed in advance. Estimating only pairwise diagonal exceedances may miss the combinations of coordinates that enter that half-space.

The article distinguishes an extreme-value distribution from a distribution in its maximum domain of attraction. Ordinary observations need not themselves be maxima for the latter condition to justify asymptotic tail analysis. It also shows that a copula domain-of-attraction statement,

$$
C(u_1^{1/n},\ldots,u_d^{1/n})^n
\longrightarrow C_\infty(u),
$$

can be expressed as a conventional maximum-domain-of-attraction result after transforming to unit Fréchet margins. The equivalence is useful. Calling one language redundant does not prove that it lacks inferential or expository value.

## Time dependence and the evidential boundary

Sections 9–10 criticize fitting static, often iid, copulas to financial observations with conditional heteroskedasticity, serial dependence, and changing distributions. A contemporaneous joint model fitted to raw returns does not automatically model these temporal features. The paper notes that even marginal distributions of familiar nonlinear time-series models can be analytically difficult, so deriving all their finite-dimensional copulas need not simplify the problem.

The sweeping claim that copulas cannot describe stochastic processes is nevertheless false as a universal statement. As the contemporaneous discussion notes, a stationary first-order Markov chain with continuous marginal $F$ can be specified through $F$ and the copula of successive observations. With a differentiable copula, the conditional transition CDF is $\partial_1C(F(x),F(y))$. This is a constructive counterexample; it does not imply that every complex financial process is best modeled that way.

The article supplies no financial dataset, estimation calendar, training/test split, forecast horizon comparison, benchmark loss, transaction costs, or statistically estimated performance improvement. Its 200-assets/500-observations example is a dimensionality illustration, not a fitted experiment. Its equations reconstruct distributions and rare-event approximations; they do not furnish a production-ready tail estimator with verified coverage.

For research use, preserve three lessons: specify which dependence property and which risk functional are the targets; propagate marginal and association-model uncertainty together; and validate dynamics and tails where the intended decision is sensitive. These lessons support copula model scrutiny without requiring the paper's broader dismissal of copula methods. The distinction between criticism, proven identity, asymptotic assumption, and empirical evidence is essential to reading this particular source accurately.
