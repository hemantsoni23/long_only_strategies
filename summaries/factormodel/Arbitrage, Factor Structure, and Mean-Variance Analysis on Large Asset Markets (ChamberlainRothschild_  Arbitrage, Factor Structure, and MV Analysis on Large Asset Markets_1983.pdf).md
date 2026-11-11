# Arbitrage, Factor Structure, and Mean-Variance Analysis on Large Asset Markets

Gary Chamberlain and Michael Rothschild. *Econometrica* 51(5), September 1983, 1281–1304. The source is a 24-page image scan; the statements and equations in this note were checked against the rendered pages, including the proofs in Sections 3–5.

Source: [original PDF](../../Finance/ChamberlainRothschild_%20%20Arbitrage,%20Factor%20Structure,%20and%20MV%20Analysis%20on%20Large%20Asset%20Markets_1983.pdf). Page numbers below are printed journal pages.

## Why this matters

The paper supplies a foundation for using principal components and approximate factor models in asset pricing. Its central distinction is between an exact model with mutually uncorrelated stock-specific disturbances and an approximate model whose residual covariance has uniformly bounded eigenvalues. The latter permits economically plausible local dependence while still ensuring that sufficiently dispersed portfolios can diversify residual risk.

Two arguments are developed separately. First, restrictions against asymptotic arbitrage give a well-defined mean–variance geometry in a market with countably many assets, even without assuming factors. Second, a covariance sequence with finitely many unbounded eigenvalues has a unique common covariance component under additional regularity. Combining the arguments yields approximate linear pricing in factor loadings, with a quantitative bound on the sum of squared pricing errors.

The result is stronger than saying that factors explain much return variance but weaker than saying that every asset is priced exactly. It does not establish the CAPM, identify an economic market portfolio, or make individual principal components structural risk factors. It provides an existence and approximation theorem in population moments. There is no empirical dataset, fitted regression, numerical forecast experiment, trading strategy, transaction-cost analysis, or finite-sample statistical test in this paper.

## Market definition and the meaning of a limiting portfolio

The market contains assets $x_1,x_2,\ldots$, each with finite second moment. Prices have already been fixed and normalized: one unit of initial investment purchases the random payoff $x_i$. Thus $x_i$ is a payoff per unit cost; one should not silently replace it with a zero-cost excess return when interpreting the cost functional or the riskless payoff.

A finite portfolio has payoff

$$
p=\sum_{i=1}^N\alpha_i x_i,
\qquad C(p)=\sum_{i=1}^N\alpha_i.
$$

Short sales are allowed, so weights can be negative. There are no leverage, financing, liquidity, or transaction-cost constraints. Let $\mathcal F_N$ be the linear span of the first $N$ assets and $\mathcal F=\bigcup_N\mathcal F_N$. The asset means and covariance matrix are

$$
\mu_N=E[x_N],
\qquad \Sigma_N=\operatorname{Cov}(x_N),
\qquad x_N=(x_1,\ldots,x_N)'.
$$

Every finite $\Sigma_N$ is assumed nonsingular. This makes a finite portfolio's coefficients uniquely determined by its payoff and ensures that the cost functional is well defined. A zero-variance nonzero finite portfolio is ruled out at this stage; a riskless asset may nevertheless emerge as a limit of increasingly diversified portfolios.

Embed payoffs in $L^2(P)$, with inner product and norm

$$
(p,q)=E[pq]=\operatorname{Cov}(p,q)+E[p]E[q],
\qquad \|p\|^2=E[p^2].
$$

The closure $\overline{\mathcal F}$ contains random payoffs approximable in mean square by finite portfolios. The limit is a payoff-space object: it does not necessarily have an ordinary absolutely summable infinite vector of holdings. Confusing convergence of payoffs with convergence of all portfolio weights would bypass a major part of the argument.

Two standard Hilbert-space facts do the work. Projection onto a closed subspace gives a unique least-squares decomposition. A continuous linear functional has a unique representing element through the inner product. Expectation is automatically continuous in this norm; continuity of *cost* requires an economic restriction.

## The paper's no-arbitrage assumptions

Section 3.1, p. 1287, uses two sequential restrictions. For any sequence of finite portfolios $p_N$:

$$
\operatorname{Var}(p_N)\to0,\quad C(p_N)\to0
\quad\Longrightarrow\quad E[p_N]\to0.
$$

This is Condition A.i. It excludes portfolios becoming riskless and costless while retaining a nonzero expected payoff. Because positions can be reversed, a negative nonzero limiting mean is also exploitable. The restriction concerns a sequence of approximate opportunities; it is stronger and more relevant here than inspecting only exact finite-market arbitrage.

Condition A.ii says

$$
\operatorname{Var}(p_N)\to0,\quad C(p_N)\to1,
\quad E[p_N]\to a
\quad\Longrightarrow\quad a>0.
$$

An approximately riskless payoff costing one must have a positive limiting payoff. If its payoff were nonpositive, shorting it would generate resources today without a compensating positive obligation later. The authors motivate these conditions through the unbounded positions some risk-averse investors would otherwise demand. They do not invoke a complete general-equilibrium model with a fully specified utility distribution.

A.ii implies continuity of cost. If $\|p_N\|\to0$ but $C(p_N)$ did not approach zero, a subsequence would have costs bounded away from zero in absolute value. Divide its payoffs by their costs. The rescaled portfolios cost one, while their second moments and means approach zero, contradicting A.ii. This is Proposition 1, p. 1288.

Cost therefore extends uniquely and continuously from finite portfolios to $\overline{\mathcal F}$. Riesz representation produces $m,c\in\overline{\mathcal F}$ satisfying

$$
E[p]=(m,p),\qquad C(p)=(c,p).
$$

The representing payoff $c$ prices attainable payoffs through an inner product. The paper's mean–variance assumptions alone should not be read as proving all the positivity and statewise properties of a modern strictly positive stochastic discount factor. The result being used here is continuity on the attainable $L^2$ payoff space.

## Mean–variance efficiency and a bounded reward-to-risk slope

Theorem 1 states that the projection of any payoff $q$ onto the span of $m$ and $c$ has the smallest variance among all attainable limit portfolios with the same mean and cost. Write this projection as $p^0$ and let the orthogonal remainder be $r=q-p^0$. Since $r$ is orthogonal to both representers, it changes neither expected payoff nor cost. At fixed mean, minimizing the second moment is equivalent to minimizing variance, and Pythagoras gives

$$
\operatorname{Var}(q)-\operatorname{Var}(p^0)=\|r\|^2\ge0.
$$

The mean–variance minimum-variance set is therefore contained in a subspace of dimension at most two. This does not assume that the market's exogenous aggregate portfolio lies on that frontier. It also does not require a factor model.

Define the maximum absolute mean per unit standard deviation for a nonzero zero-cost portfolio:

$$
\delta=\sup_{p\in\mathcal F,\ C(p)=0}
\frac{|E[p]|}{\sqrt{\operatorname{Var}(p)}}.
$$

The same value is obtained in the appropriate closure. Under Conditions A it is finite. To construct the maximizing direction, remove from $m$ its projection onto $c$:

$$
h=m-\frac{(m,c)}{(c,c)}c.
$$

If $h\ne0$, it has zero cost and positive variance and achieves $\delta=|E[h]|/\sqrt{\operatorname{Var}(h)}$. If $h=0$, all zero-cost portfolios have zero mean and $\delta=0$. This is Corollary 1. The payoff $h$ is the efficient direction for changing expected payoff without changing investment cost.

For two minimum-variance portfolios $p,q$ of the same cost, their difference lies in that direction, so

$$
|E[p]-E[q]|=\delta\sqrt{\operatorname{Var}(p-q)}.
$$

The variance is that of the *difference*, not the difference of the two variances. This qualification matters when translating the geometric statement into efficient-frontier formulae.

A usable finite-dimensional construction follows in Proposition 3. Let $\mathbf1_N$ denote the vector of ones. Then

$$
\delta_N^2=
\min_a(\mu_N-a\mathbf1_N)'\Sigma_N^{-1}
(\mu_N-a\mathbf1_N),
$$

with minimizer

$$
a_N=\frac{\mathbf1_N'\Sigma_N^{-1}\mu_N}
{\mathbf1_N'\Sigma_N^{-1}\mathbf1_N}.
$$

The corresponding zero-cost maximizing direction is proportional to $\Sigma_N^{-1}(\mu_N-a_N\mathbf1_N)$. The values $\delta_N$ are nondecreasing as more assets become available and converge to $\delta$. Enlarging the opportunity set cannot reduce the best attainable zero-cost reward-to-risk ratio.

These are population formulas. Plugging noisy sample means and a nearly singular sample covariance into them can greatly exaggerate a finite-sample ratio; the theorem does not supply a bias correction or a regularization parameter.

## When a riskless asset exists in the closure

A riskless limit portfolio is a nonzero constant payoff in $\overline{\mathcal F}$. Under Conditions A it has nonzero cost and can be normalized to cost one. Its payoff is a positive constant $\rho$. Any two such cost-one payoffs must coincide, because their difference is costless and riskless. The positivity refers to the gross payoff per unit investment, not necessarily a positive net interest rate.

When this payoff exists, the efficient frontier in mean–standard-deviation space satisfies

$$
|E[p]-\rho|=\delta\sqrt{\operatorname{Var}(p)}
$$

for cost-one minimum-variance portfolios. The two branches are straight rays; economically efficient investors interested in higher mean at a given risk select the relevant upper branch.

Proposition 2 supplies a sharp covariance characterization. Under Conditions A, there is *no* riskless limit asset if and only if some $\varphi>0$ satisfies

$$
\Sigma_N-\varphi\mathbf1_N\mathbf1_N'\succeq0
\qquad\text{for every }N.
$$

Such a common covariance component imposes a variance floor proportional to squared cost:

$$
\alpha'\Sigma_N\alpha\ge\varphi(\alpha'\mathbf1_N)^2.
$$

Hence a cost-one portfolio cannot have variance tending to zero. Conversely, if no riskless asset exists, covariance itself can be used as a Hilbert-space inner product on the attainable closure. The cost representer in that geometry generates precisely such an equicorrelated covariance component.

Positive exposure to some common shock is insufficient to prevent asymptotic riskless investment. The example on p. 1291 has odd assets $x_i=a+\beta f+v_i$ and even assets $x_i=f+v_i$, with $a>0$, $0<\beta<1$, and mutually uncorrelated zero-mean residuals of uniformly bounded variance. Invest $1/N$ in each of the first $N$ odd assets and $-\beta/N$ in each of the first $N$ even assets. Factor exposure cancels, cost is $1-\beta$, and the residual payoff converges in mean square to zero. The limiting constant payoff is $a$, giving a cost-one riskless payoff $a/(1-\beta)$. Different exposures make hedging possible even though every asset moves positively with the common factor.

## Approximate factor structure and pricing-error control

A strict factor structure writes

$$
x_i=\mu_i+\sum_{k=1}^K\beta_{ik}f_k+v_i,
$$

where factors have zero mean and identity covariance, are uncorrelated with residuals, and residuals are mutually uncorrelated with uniformly bounded variances. Its covariance decomposition is $\Sigma_N=B_NB_N'+D_N$, with $D_N$ diagonal.

The approximate structure replaces diagonality by bounded residual eigenvalues:

$$
\Sigma_N=B_NB_N'+R_N,
\qquad R_N\succeq0,
\qquad \sup_N\lambda_{\max}(R_N)=\overline\lambda<\infty.
$$

The rows of $B_N$ must be nested: a given asset's loading does not change merely because more assets are added. Arbitrary unrelated low-rank fits for each $N$ do not meet this definition. It also matters that residual matrices are positive semidefinite, not just bounded signed errors.

For a portfolio with coefficient vector $\alpha_N$, residual variance is bounded by

$$
\alpha_N'R_N\alpha_N\le\overline\lambda\|\alpha_N\|_2^2.
$$

Thus residual risk vanishes for sequences whose Euclidean weight norm tends to zero. Equal weights have squared norm $1/N$; a highly concentrated or heavily leveraged portfolio need not. This is the sense of diversification that connects covariance structure to pricing.

A simple permitted dependence pattern has residual variance $\varphi_1$, covariance $\varphi_2$ between adjacent assets, and zero covariance for more distant pairs. Subject to positive semidefiniteness, its eigenvalues are uniformly bounded, so it qualifies as approximate despite requiring an increasing number of factors to force a strictly diagonal residual covariance. This is the practical advantage over the strict model.

Theorem 3, pp. 1295–1296, combines the approximate structure with Conditions A. There exist fixed coefficients $\tau_0,\tau_1,\ldots,\tau_K$ such that

$$
\sum_{i=1}^{\infty}
\left(\mu_i-\tau_0-\sum_{k=1}^K\tau_k\beta_{ik}\right)^2
\le\overline\lambda\delta^2.
$$

If a riskless payoff $\rho$ exists, the intercept can be set to $\rho$. Without it, an intercept is still present but is not automatically an observed Treasury return. The coefficients are risk-premium coordinates in a chosen loading basis; rotating factors changes their coordinates while preserving fitted means.

The bound means that pricing errors are square summable. For any fixed positive threshold, only finitely many assets can have absolute error above that threshold. It also implies average squared pricing error among the first $N$ assets is at most $\overline\lambda\delta^2/N$. It does *not* force the error of every named asset to be zero, rule out a finite collection of persistent anomalies, or provide a universal numerical error bound independent of the residual spectrum and frontier slope.

A concise reconstruction of the proof clarifies the mechanism. For a finite cross-section, regress the population mean vector on an intercept and $B_N$ in ordinary Euclidean distance. Let $a_N$ be the residual vector. Orthogonality gives $\mathbf1_N'a_N=0$, $B_N'a_N=0$, and $\mu_N'a_N=\|a_N\|_2^2$. Use $a_N$ as portfolio weights. It costs zero, has no factor exposure, expected payoff $\|a_N\|_2^2$, and variance at most $\overline\lambda\|a_N\|_2^2$. The reward-to-risk bound $\delta$ therefore requires $\|a_N\|_2^2\le\overline\lambda\delta^2$. Otherwise this residual-mean portfolio would violate the bounded frontier slope.

The paper's matrix proof reaches this bound through inverse-covariance inequalities and a projection matrix. The remaining subtlety is obtaining *one* coefficient vector for the infinite sequence. A sufficiently large fixed submatrix with full column rank bounds the finite regression coefficients; a convergent subsequence then supplies common limiting coefficients, and the bound passes to every finite initial subset. If the intercept is already in the factor-loading span, redundant columns are removed rather than inverting a singular normal matrix. This compactness step explains why nesting matters.

## Eigenvalue characterization and the scope of uniqueness

An approximate structure with at most $K$ common directions implies that the $(K+1)$st eigenvalue of $\Sigma_N$ is uniformly bounded. The argument uses a rank bound: $B_NB_N'$ has rank at most $K$, so the first residual eigenvalue bounds the $(K+1)$st total eigenvalue. This is Proposition 4.

The converse in Theorem 4 requires three conditions, beyond positive definiteness of each finite matrix:

$$
\lambda_{K,N}\to\infty,
\qquad \sup_N\lambda_{K+1,N}<\infty,
\qquad \inf_N\lambda_{N,N}>0.
$$

Eigenvalues are in descending order. Because covariance matrices are nested principal submatrices, the relevant leading eigenvalue sequences are nondecreasing. The conditions say exactly $K$ directions diverge, the remainder stay bounded above, and no covariance direction collapses toward zero uniformly across expanding markets. An arbitrary factor decomposition with redundant or nonpervasive columns need not have exactly $K$ diverging eigenvalues; the minimal pervasive dimension is the relevant one.

Let $t_{j,M}$ be a unit eigenvector of the $M$-asset population covariance. Form loadings from its scaled entries, $\sqrt{\lambda_{j,M}}t_{j,M}$, and retain the first $N$ rows in a matrix $B_{N,M}$. For each fixed $N$, Theorem 4 proves

$$
B_{N,M}B_{N,M}'\longrightarrow B_NB_N'
\qquad(M\to\infty).
$$

The limiting covariance decomposition has residual eigenvalues bounded by $\sup_N\lambda_{K+1,N}$. If another nested $K$-column loading sequence and bounded positive-semidefinite residual sequence give the same total covariance, their common covariance and residual covariance are identical. This is uniqueness of $B_NB_N'$, not uniqueness of individual columns, signs, rotations, or eigenvectors when leading eigenvalues have multiplicities.

Finite principal-component reconstructions change as the cross-section grows and are not themselves nested. Theorem 3′ gives a finite-$N$ pricing approximation based on those reconstructions, with coefficients that can depend on $N$. Theorem 4 is what justifies moving from such moving approximations to a stable limiting common covariance. The limit is entrywise on every fixed finite block; the theorem does not state that a growing full-matrix error vanishes in unqualified operator norm.

## Proof architecture behind the principal-component result

The proof constructs the space of well-diversified limit portfolios. A seminorm records the limiting Euclidean norm of finite portfolio coefficient vectors. Under the spectral separation and lower-eigenvalue bound, its zero set is a $K$-dimensional subspace. These are limits obtainable with coefficient norm approaching zero while common risk remains.

Project each asset onto that subspace and choose an orthonormal factor basis for it. The projection coefficients are factor loadings. The orthogonal residual portfolio has variance bounded by the $(K+1)$st eigenvalue bound times its coefficient norm squared, yielding the required residual covariance bound.

Normalized principal-component portfolios span approximating subspaces. Their projection operators converge to the projection onto the diversified subspace. Covariances between projected individual assets therefore converge, giving the fixed-block Gram-matrix limit above. This route avoids an unnecessary assertion that arbitrarily normalized eigenvectors must each converge individually.

For uniqueness, apply the normalized leading-eigenvector portfolios to any proposed alternative covariance decomposition. Bounded residual eigenvalues make the alternative residual contribution vanish after division by diverging leading eigenvalues. The surviving loading transformation tends to an orthogonal transformation, so both decompositions produce the same common covariance. Lemma 2, used for the diversified-subspace construction, is quoted from Chamberlain's related work; the paper does not reproduce every proof of that supporting lemma. A formal verification from primitive Hilbert-space assumptions must consult that dependency.

## Generalized principal components and an implementation reading

The final result addresses the objection that ordinary PCA depends on using the identity as its metric. Let $\Omega_N$ be a nested positive-definite metric sequence with eigenvalues bounded above and bounded away from zero uniformly in $N$. Solve

$$
\Sigma_Ns_{j,N}=\theta_{j,N}\Omega_Ns_{j,N},
\qquad s_{j,N}'\Omega_Ns_{k,N}=\mathbf1\{j=k\}.
$$

The covariance-scale loading vectors are $\sqrt{\theta_{j,N}}\Omega_Ns_{j,N}$, not the generalized eigenvectors alone. With these scaled vectors, the finite-block common covariance converges to the same limit as ordinary PCA. The proof whitens using a nested triangular transformation, bounds generalized eigenvalues by ordinary eigenvalues times the metric's uniform bounds, and invokes the preceding uniqueness result.

This is an asymptotic robustness statement under controlled metrics. It does not say every finite-sample normalization gives identical loadings, or permit a metric with vanishing eigenvalues or exploding condition number. Correlation-matrix PCA requires checking whether the variance-based rescaling satisfies those uniform conditions. Conventional factor analysis is related through a residual-variance metric, but its normality-based likelihood machinery is not needed for the population approximate-factor result.

A computational exploration can estimate nested covariance matrices, examine leading and residual eigenvalues as the universe expands, reconstruct common covariance from scaled eigenvectors, and compare fixed-asset blocks across expansions and admissible metrics. One can then estimate mean/loadings relations and inspect pricing residuals. These are applications suggested by the theory, not an empirical protocol implemented in the article. Choosing sample dates, universe, covariance estimator, number of factors, sampling corrections, and out-of-sample tests requires additional assumptions and design.

The most consequential limitations are therefore clear. The theory presumes population second moments and unrestricted signed portfolios; ignores costs and trading restrictions; requires large-market limits with explicit spectral regularity; and permits nonzero individual pricing errors. Within that domain it explains why weakly correlated residuals can coexist with approximate factor pricing, why PCA can recover a stable common covariance, and why a common covariance model alone neither proves exact pricing nor identifies an economically unique set of factors.
