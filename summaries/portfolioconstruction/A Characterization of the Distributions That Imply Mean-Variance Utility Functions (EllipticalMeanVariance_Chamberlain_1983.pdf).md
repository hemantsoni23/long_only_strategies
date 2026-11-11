# A Characterization of the Distributions That Imply Mean-Variance Utility Functions

Gary Chamberlain, *Journal of Economic Theory* 29, 185–201 (1983). Received 18 March 1980; revised 17 September 1981.

Source: [EllipticalMeanVariance_Chamberlain_1983.pdf](../../Finance/EllipticalMeanVariance_Chamberlain_1983.pdf). All 17 PDF pages, including the proofs, geometric figures, and references, were read. Printed page 185 corresponds to PDF page 1. This is distinct from Chamberlain and Rothschild's 1983 paper on arbitrage and factor structure.

## Why this matters

Mean and variance can be sufficient for portfolio choice for two very different reasons. One can restrict preferences, for example to quadratic utility, or restrict the joint distribution of returns so that every portfolio's full distribution is determined by its two moments. Chamberlain characterizes the second route. The paper identifies exactly which symmetry conditions are required, shows how the answer changes when no riskless asset exists, and derives a stronger mutual-fund separation result than the usual risk-averse-investor formulation.

The result is broader than multivariate normality but much more restrictive than saying that individual asset returns look approximately symmetric. With a riskless asset, a whitened return vector must be spherically symmetric. Without a riskless asset, there is an additional unrestricted component: residual directions need spherical symmetry conditional on that component, while the component itself may have an arbitrary distribution. In an infinite-dimensional setting with unbounded covariance rank, the residual distribution must become a normal scale mixture.

These are exact distributional theorems, not empirical findings that actual markets satisfy the assumptions. Their practical role is to identify which distributional restrictions justify compressing portfolio choice to two moments and which implications follow only after those restrictions have been established. They also warn against importing familiar normal-model geometry into a broader mean–variance model: without a riskless asset, increasing concave utility need not be an increasing function of the portfolio mean.

## Economic setup and the precise sufficiency claim

Let $x\in\mathbb R^n$ be a vector of random asset returns, with $E[x]=\mu$ and covariance matrix $\Sigma$. The finite-dimensional results assume $\Sigma$ is nonsingular and second moments exist. A portfolio payoff is

$$
p=a^\top x+a_0r,
$$

where $r>0$ is the nonrandom payoff of a riskless asset, when one is available. With $e$ the vector of ones, its initial cost is

$$
C(p)=a^\top e+a_0\le B.
$$

Short sales and borrowing are unrestricted. The budget is an inequality, and $B$ may be negative because a person may be borrowing to finance current consumption. Without a riskless asset, the constant term is absent. These assumptions are essential to the opportunity set used in the proofs; the results are not automatically statements about a long-only, fully invested portfolio simplex.

For a particular utility function, one could have equality of expected utility accidentally for two different distributions. Chamberlain's distributional claim is stronger: for every increasing utility function for which expectations are defined, portfolios with equal means and variances give equal expected utility. This is equivalent to those portfolios having the same distribution. Bounded increasing indicator-type functions distinguish distributions, which explains why the claim can be expressed without specifying one investor's curvature.

Thus the central condition is

$$
E[p_1]=E[p_2],\quad\operatorname{Var}(p_1)=\operatorname{Var}(p_2)
\quad\Longrightarrow\quad p_1\overset d=p_2.
$$

It is a condition on all admissible linear combinations of the asset returns, with arbitrary constant shifts when the riskless asset exists. It is not the assertion that the first two moments identify every probability distribution in general.

## Theorem 1: a riskless asset and spherical symmetry

Theorem 1, pp. 187–188, states that the distribution of $a^\top x+c$ is determined by its mean and variance for every $a,c$ if and only if some nonsingular transformation

$$
z=T(x-\mu)
$$

is spherically distributed about zero. Spherical symmetry means

$$
z\overset d=Qz
$$

for every orthogonal matrix $Q$. Equivalently, after removing location and linear covariance shape, the distribution has no preferred direction. In contemporary terminology this is a finite-variance elliptical return family.

For necessity, whiten the returns so that $E[z]=0$ and $\operatorname{Cov}(z)=I$. For any orthogonal $Q$ and any vector $b$, both $b^\top z$ and $b^\top Qz$ can be written as a risky portfolio plus a constant. They have equal mean zero and equal variance $b^\top b$. The assumed moment sufficiency therefore gives equality of their distributions for every $b$. Equality of all scalar projections identifies the multivariate distribution, so $z$ and $Qz$ have the same law. That is spherical symmetry.

For sufficiency, represent a spherical vector as

$$
z=RU,
$$

where $R\ge0$ is its radius and $U$ is independent of $R$ and uniform on the unit sphere in $\mathbb R^n$. At a zero radius, the direction can be assigned independently without affecting $z$. Rotation invariance gives

$$
b^\top U\overset d=\lVert b\rVert U_1.
$$

Every linear portfolio is therefore distributed as a location plus a scalar multiple of the same one-dimensional random variable $RU_1$. Its mean gives the location, and its variance gives the magnitude of the scale. The scale's sign is irrelevant because the projection is symmetric. Hence equal moments imply equal laws.

A convenient simulation normalization is $E[R^2]=n$, because $E[UU^\top]=I/n$. Then $x=\mu+LRU$, with $LL^\top=\Sigma$, has covariance $\Sigma$. Normality is one radial choice, not the only one. One can also use a common random volatility multiplier times a standard multivariate normal vector, provided the multiplier has a finite second moment and is scaled correctly.

The dependence qualification matters. Non-Gaussian spherical components are generally dependent even when their covariances vanish. The paper discusses earlier arguments in which independence, together with the relevant symmetry and finite variance, singles out normality. It does not say that arbitrary independent nonnormal assets yield mean–variance sufficiency. A shared radial shock is precisely a way to obtain nonnormal but suitably dependent returns.

## Theorem 2: removing the riskless asset changes the answer

Without a riskless asset, arbitrary constant shifts are unavailable. If $\mu\ne0$, Theorem 2, pp. 188–189, characterizes the condition by a nonsingular transform of the uncentered vector:

$$
Tx=\begin{pmatrix}m\\z\end{pmatrix},
$$

where $z\in\mathbb R^{n-1}$ is spherically symmetric about zero conditional on the scalar $m$. The marginal distribution of $m$ is unrestricted apart from the required moments and nondegeneracy. Conditional symmetry does not require $m$ and the residual radius to be independent.

To see necessity constructively, first whiten the covariance and rotate the transformed mean into the first coordinate. Then

$$
E[Tx]=(\tau,0,\ldots,0)^\top,\qquad
\operatorname{Cov}(Tx)=I,
$$

with $\tau\ne0$. Rotating only the last $n-1$ coordinates leaves every scalar portfolio's mean and variance unchanged. The same projection argument as before proves that the joint law of $(m,z)$ is unchanged by $(m,z)\mapsto(m,Qz)$. This is exactly spherical symmetry of the conditional law of $z$ given $m$.

For sufficiency, write a payoff as

$$
p=\delta_1m+\delta_2^\top z.
$$

Conditional spherical symmetry implies $E[z\mid m]=0$, hence $\operatorname{Cov}(m,z)=0$. Let $\operatorname{Var}(m)=\theta_1$ and $\operatorname{Cov}(z)=\theta_2I$. The two moments are

$$
E[p]=\delta_1E[m],\qquad
\operatorname{Var}(p)=\theta_1\delta_1^2+\theta_2\lVert\delta_2\rVert^2.
$$

They identify $\delta_1$ and the norm of the residual loading. Conditional rotational invariance makes the residual loading's direction irrelevant, so those quantities determine the full payoff distribution. One can represent $z=RU$, where $U$ is uniform on the residual sphere and independent of $(m,R)$, while the radius $R$ may depend on $m$.

If $\mu=0$, the special first component is unnecessary. The necessary and sufficient condition becomes spherical symmetry of $Tx$ for a nonsingular $T$. All portfolio means are then zero. A coding implementation must branch on this case rather than divide by $E[m]$.

A simple two-asset example explains the additional freedom. After normalization, take $E[x]=(1,0)^\top$ and covariance $I$. The moments of $a_1x_1+a_2x_2$ identify $a_1$ and $|a_2|$. If the conditional distribution of $x_2$ given $x_1$ is symmetric about zero, the missing sign does not matter. Nothing in this argument forces the distribution of $x_1$ itself to be normal or symmetric.

## Utility geometry: what does and does not follow

The finite-dimensional characterizations yield a common representation

$$
p\overset d=\beta_1m+\beta_2z_0,
$$

where the conditional distribution of $z_0$ given $m$ is symmetric and $\beta_2\ge0$. The coefficients are determined by the payoff's moments. In the riskless case, $m$ can be taken constant; without it, $m$ is generally random.

For concave utility, $g(\beta_1,\beta_2)=E[u(\beta_1m+\beta_2z_0)]$ is concave in the coefficients. Symmetry and concavity also make it nonincreasing in residual scale $\beta_2$ at fixed $\beta_1$. Pair positive and negative residual realizations and apply concavity to see why spreading those symmetric outcomes lowers expected utility.

However, increasing the coefficient of the risky common component is not a pure upward translation. It also magnifies adverse realizations of that component. Thus increasing concave utility does not guarantee that $g$ increases in $\beta_1$, or that expected utility increases in mean when expressed in mean–standard-deviation coordinates without further assumptions.

Page 190 gives a simple example. Let $m$ equal 3 or $-1$ with probabilities one half each, and let $u(p)=\min(p+3,0)$. This utility is concave and nondecreasing. Then $E[u(m)]=0$, but $E[u(5m)]=-1$, although $E[5m]>E[m]$. The function has a flat upper region; the example does not require strict monotonicity. It shows the failure of the unrestricted monotonicity assertion used in some conventional frontier arguments.

The paper also constructs a failure of quasiconcavity in mean–standard-deviation coordinates. Let an independent residual $z$ equal $1$ or $-1$ with probability $\theta$ each and zero otherwise. Both $m$ and $-m$ have standard deviation 2 and expected utility zero under the same utility. A zero-mean payoff $p^*=\sqrt{2/\theta}\,z$ also has standard deviation 2, but has negative expected utility if $\theta<2/9$. The midpoint in the two-moment plane is therefore worse than the two endpoints. This does not contradict concavity in portfolio payoffs or in the coefficient pair: the map from coefficients to moments is nonlinear.

## Theorem 3: infinitely many assets and normal mixtures

The large-market theorem, pp. 191–194, considers an infinite sequence of returns. Every ordinary portfolio is a finite linear combination of that sequence. Covariance matrices of finite initial segments may now be singular, allowing an actual riskless asset, but their ranks must be unbounded as the number of assets grows. Simply adding redundant copies of a few assets does not meet this assumption.

Under this condition, moment sufficiency holds if and only if there are common latent variables $m,v,y$ such that $y$ conditional on $(m,v)$ is standard normal and every portfolio satisfies

$$
p\overset d=\beta_1m+\beta_2vy,
$$

with

$$
\beta_1=\frac{E[p]}{E[m]},\qquad
\beta_2=\left(\frac{\operatorname{Var}(p)-\beta_1^2\operatorname{Var}(m)}{E[v^2]}\right)^{1/2}.
$$

If $E[m]=0$, all portfolio means are zero and $\beta_1$ can be set to zero. The representation is distributional for each payoff. It must not be interpreted as saying that all actual portfolio payoffs on the original probability space are simultaneously pathwise combinations of two random variables. Such a pathwise interpretation would contradict unbounded covariance rank.

The key geometric lemma is that if $U^{(n)}$ is uniform on the unit sphere in $\mathbb R^n$, then

$$
\sqrt n\,U^{(n)}_1\Rightarrow N(0,1).
$$

To prove it, normalize a vector of independent standard normals by its Euclidean length. The squared length divided by $n$ converges to one, while its first coordinate remains standard normal. The direction's scaled first coordinate therefore converges to that normal coordinate. This is a statement about high-dimensional spherical geometry, not a central limit theorem for arbitrary dependent asset returns.

The full proof adds several important steps. Complete the linear portfolio space under the mean-square norm to include limit portfolios. Expected payoff is a continuous linear functional, so its Riesz representer supplies a distinguished portfolio $m$. Apply Gram–Schmidt to form an orthogonal sequence consisting of $m$ and zero-mean, unit-variance residual portfolios. Extend moment sufficiency to limits by approximating portfolios in mean square and matching their moments before passing to a distributional limit.

Finite vectors of these residual coordinates are conditionally spherical given $m$, hence invariant under permutations. Their squared coordinates form an exchangeable sequence. The average squared radius converges to a latent nonnegative quantity $v^2$. The uniform-sphere lemma then turns each residual projection into a common random scale times a standard normal. Combining it with the common component yields the stated representation. This sequence of arguments explains why finite-dimensional spherical laws are broader than the laws consistently extendable to arbitrarily many independent directions of risk.

A limiting riskless asset is defined by a sequence of portfolios with expected payoff tending to $r>0$ and variance tending to zero. In that case $\operatorname{Var}(m)=0$, and the representation simplifies to

$$
p\overset d=E[p]+\sqrt{\frac{\operatorname{Var}(p)}{E[v^2]}}\,vy.
$$

The definition is about mean-square convergence of payoffs; it does not separately impose a unit-price or bounded-cost condition on that sequence. Its role in the proof is to remove randomness from the common mean component. It should not be casually equated with an empirically observed cash instrument without checking the economic normalization.

For the canonical zero-mean residual $vy$, the characteristic function has the form

$$
\psi(t)=E\left[e^{-t^2v^2/2}\right].
$$

Thus $g(\lambda)=\psi(\sqrt{2\lambda})$ is the Laplace transform of a nonnegative mixing variable. The paper expresses the equivalent complete-monotonicity condition: $g(0)=1$ and $(-1)^kg^{(k)}(\lambda)\ge0$ for positive $\lambda$ and all relevant derivative orders. This characterizes the normal scale-mixture structure. Symmetry alone is insufficient for infinite-dimensional extendability, and finite second moments remain part of the portfolio framework.

## Strong two-fund separation without a concavity restriction

Section 2 defines strong separation as follows. There are two fixed funds such that every portfolio can be replaced by a combination of those funds at no greater cost and with no lower expected utility, simultaneously for all utility functions in the chosen class. The replacement coefficients depend on the portfolio being replaced, while the funds do not depend on the investor's utility.

Chamberlain proves a geometric proposition: two fixed funds can match any portfolio's mean and variance at no greater cost. Under the distributional characterizations, matching the moments matches the entire payoff law. Expected utilities are then equal whenever defined, so the result applies even without concavity. This is stronger than showing that risk-averse investors reject a zero-mean residual noise term.

For implementation, avoid confusing the scalar latent $m$ above with the weight vector denoted $m$ in the paper's separation proof. Here call the two weight vectors

$$
b=\Sigma^{-1}\mu,\qquad d=\Sigma^{-1}e,
$$

and use the covariance inner product $\langle a,c\rangle=a^\top\Sigma c$. With a riskless asset, define $f=d-b/r$. If $f\ne0$, use the riskless asset and the risky fund $f^\top x$. For a given payoff $p=a^\top x+a_0r$, choose

$$
y_2=-\sqrt{\frac{\operatorname{Var}(p)}{\langle f,f\rangle}},\qquad
y_1=\frac{E[p]-y_2f^\top\mu}{r},
$$

and set $p^*=y_1r+y_2f^\top x$. The moments agree by construction. The cost difference is

$$
C(p)-C(p^*)=\langle a,f\rangle+
\sqrt{\langle a,a\rangle\langle f,f\rangle}\ge0
$$

by Cauchy–Schwarz. If $f=0$, cost is proportional to mean, so a nonzero risky direction can supply the desired variance at equal cost after adjusting the riskless holding. The sign convention $y_2\le0$ depends on how the second fund is oriented; it is not an invariant claim that investors must short the market.

Without a riskless asset and with $\mu\ne0$, remove the projection of $d$ onto $b$:

$$
\eta=\frac{\langle d,b\rangle}{\langle b,b\rangle},\qquad
f=d-\eta b.
$$

The funds are $b^\top x$ and $f^\top x$. They are uncorrelated, and the second has zero mean. Match the original payoff using

$$
y_1=\frac{E[p]}{\langle b,b\rangle},\qquad
y_2=-\sqrt{\frac{\operatorname{Var}(p)-y_1^2\langle b,b\rangle}{\langle f,f\rangle}}.
$$

The variance residual is nonnegative because it is the squared covariance norm after projecting the original weights onto $b$. Let $a_2=a-y_1b$. Orthogonality gives

$$
C(p)-C(p^*)=\langle a_2,f\rangle+
\sqrt{\langle a_2,a_2\rangle\langle f,f\rangle}\ge0.
$$

If $f=0$, choose another nonzero covariance-orthogonal direction to match variance; the mean match already fixes cost. Zero-mean or lower-dimensional degenerate cases require separate handling rather than dividing by zero. The formulas above describe the nondegenerate construction used in the proof.

The ability to underspend is crucial. A same-law payoff at lower cost remains feasible under $C(p)\le B$. If an application imposes equality spending, position bounds, margin limits, or short-sale restrictions, the replacement may cease to be admissible. The theorem does not promise a two-fund implementation under those added constraints.

## Frontier geometry, borrowing, and the Ross connection

When the two no-riskless funds can be normalized to unit cost, write their means as $\tau>0$ and zero and their variances as $s_1^2,s_2^2$. Their covariance is zero. On the equality-budget slice $y_1+y_2=B$, mean is $M=y_1\tau$ and variance is

$$
V=(s_1^2+s_2^2)\left[\frac M\tau-
\frac{Bs_2^2}{s_1^2+s_2^2}\right]^2+
\frac{B^2s_1^2s_2^2}{s_1^2+s_2^2}.
$$

The minimum-variance point has $M/\tau=Bs_2^2/(s_1^2+s_2^2)$, while the $y_2=0$ point has $M/\tau=B$. Figures 1 and 2, pp. 197–198, show why the relative ordering reverses when $B$ becomes negative. For positive investment, feasible interior-budget combinations can improve on parts of the equality-budget curve. For negative investment, the relevant two-fund branch can include points to the left of the minimum-variance point.

The borrowing example on pp. 196–197 uses independent $x_1\in\{3,-1\}$ and $x_2\in\{4,-4\}$, each outcome equally probable, with $B=-1$. The equality-budget minimum-variance payoff is $p_a=-0.8x_1-0.2x_2$, with mean $-0.8$ and variance 3.2. The alternative $p_b=-x_1$ has lower mean $-1$ and higher variance 4, yet its worst outcome is $-3$, versus $-3.2$ for $p_a$. Under $u(p)=\min(p+3,0)$, $p_b$ has expected utility zero and $p_a$ has negative expected utility. Hence mean–variance coordinates do not carry the usual “higher mean and lower variance is always preferred” interpretation throughout this broader class.

Finally, the paper connects its distributions to Ross's separating-distribution condition. After a suitable canonical transformation, let the residual coordinates be $z_i$ and their average $\bar z$. Conditional spherical symmetry implies conditional exchangeability, including after conditioning on $(m,\bar z)$. Therefore

$$
E[z_i\mid m,\bar z]=\bar z,
$$

so each residual $z_i-\bar z$ has zero conditional mean. For concave utility, conditional Jensen's inequality makes the payoff using the common component and residual average at least as desirable as one retaining the extra residual terms. This provides a direct explanation of ordinary risk-averse separation. It is conceptually distinct from the earlier same-distribution, lower-cost construction, which does not need concavity.

## Reconstructing and using the results

There is no empirical dataset, estimation window, backtest, cost calibration, or numerical performance comparison in this paper. Its outputs are equivalence theorems, a limiting representation, explicit fund constructions, and counterexamples. A replication should verify those mathematical claims rather than invent trading results.

A finite-dimensional simulation check can draw spherical directions by normalizing independent Gaussian vectors, select a radial law with finite second moment, and transform by a covariance factor. With a riskless asset, construct several different loading vectors with equal covariance norm and adjust constants to equalize means. Their empirical payoff distributions should agree up to Monte Carlo error. Without a riskless asset, draw an arbitrary common component, let the residual radius depend on it if desired, and keep residual direction uniform. Equal common-component coefficients and equal residual loading norms then provide the corresponding matched-moment comparisons.

Such checks illustrate sufficiency, not necessity. Testing a handful of rotations or projections in finite data cannot establish exact spherical symmetry for all directions. Moreover, whitening with an estimated covariance introduces estimation error not studied by Chamberlain. An applied researcher needs separate statistical methods to assess those restrictions and their stability.

The main implementation lesson is to preserve the opportunity set and the quantifiers. Theorems about all linear combinations with free shorting and a budget inequality are stronger and differently scoped than a statement about observed long-only portfolios. The availability of a riskless asset determines whether the entire centered distribution must be spherical or whether a conditionally symmetric residual structure suffices. And the infinite-market result concerns compatible distributions across unbounded dimensions, not a guarantee that diversification turns arbitrary returns into normal returns.

Under the stated conditions, mean and variance summarize a portfolio's entire law, and two fixed funds can reproduce that law at no greater cost. Outside those conditions, a two-moment optimizer may still be a useful approximation, but this paper's exact justification no longer applies.
