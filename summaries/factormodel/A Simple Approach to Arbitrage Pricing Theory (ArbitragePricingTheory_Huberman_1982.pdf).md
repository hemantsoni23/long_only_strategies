# A Simple Approach to Arbitrage Pricing Theory

**Gur Huberman (1982).** *Journal of Economic Theory* 28, 183–191. Source: [ArbitragePricingTheory_Huberman_1982.pdf](../../Finance/ArbitragePricingTheory_Huberman_1982.pdf). All nine PDF pages, including both theorems, the risk-free-asset corollary, counterexamples, and references, were read. Page references below are printed journal pages. This is a theoretical paper, with no empirical sample or estimated trading performance.

## Why this matters

A cross-sectional factor regression is often interpreted as evidence that diversification forces every security onto a common pricing line. Huberman supplies a short mathematical argument for a more qualified conclusion. If residual risks are sufficiently diversifiable and a particular asymptotic arbitrage is excluded, the *sum* of squared deviations from factor pricing is uniformly bounded. The average error consequently shrinks as the asset universe expands. That result does not imply an economically small error for every asset in a finite universe.

The innovation is the proof construction and its separation from preference assumptions. Project expected returns onto the span of a constant and factor loadings. The orthogonal residual is simultaneously a zero-cost, factor-neutral portfolio and a measure of pricing disagreement. If its squared length becomes unbounded, a carefully chosen scale makes expected profit diverge while profit variance vanishes. The contradiction establishes approximate factor pricing without introducing utility into that step. A separate discussion then shows why equilibrium and absence of this asymptotic arbitrage are not automatically equivalent.

The resulting distinction is useful when building factor-neutral portfolios: residual expected returns can have a clean algebraic interpretation without supplying a feasible, low-risk trading opportunity after financing constraints, estimation error, and model misspecification are introduced.

## Economy, portfolios, and the precise no-arbitrage assumption

For each economy size $n$, the return vector is

$$
X^{(n)}=E^{(n)}+B^{(n)}F^{(n)}+\varepsilon^{(n)}.
$$

Here $E^{(n)}\in\mathbb R^n$ contains expected returns; $B^{(n)}$ is an $n\times k$ loading matrix; and the factor count $k$ remains fixed as $n$ grows. Equations (2.1)–(2.4), p. 186, assume

$$
\mathbb E F_j^{(n)}=0,\qquad
\mathbb E\varepsilon_i^{(n)}=0,\qquad
\mathbb E[\varepsilon_i^{(n)}\varepsilon_j^{(n)}]=0\quad(i\ne j),
$$

and a common finite bound $\operatorname{Var}(\varepsilon_i^{(n)})\le\bar\sigma^2$ for every asset and economy. The crucial restriction is uniformity: a different, arbitrarily large bound for each $n$ would not support the proof.

Residuals need not be independent or normally distributed. The formal listed assumptions do not require independence between factors and residuals either; the constructed portfolio eliminates the factor term identically. Calling the loadings covariances or regression betas requires the additional normalization and orthogonality used in an empirical factor model. The theorem itself takes a specified loading matrix and decomposition as primitives.

A portfolio $d^{(n)}$ consists of dollar allocations, allowed to be negative. With $\mathbf1$ the vector of ones, a zero-initial-cost portfolio satisfies $\mathbf1'd^{(n)}=0$. Its terminal profit is

$$
Z_n=d^{(n)\prime}X^{(n)}.
$$

The paper calls every such zero-cost position an “arbitrage portfolio,” even when its realized profit is risky. That terminology must be separated from the stronger definition of an arbitrage *opportunity*. The latter is a subsequence of zero-cost portfolios satisfying

$$
\mathbb E Z_{n_\ell}\longrightarrow+\infty,
\qquad
\operatorname{Var}(Z_{n_\ell})\longrightarrow0.
$$

This is an asymptotic condition across expanding economies. It is not the usual finite-market assertion that a single zero-cost payoff is nonnegative in every state and positive with positive probability. Finite portfolios in the sequence can lose money. There are no short-sale limits, gross-exposure caps, margin requirements, or transaction costs in this definition.

The nonstationary model permits an existing asset's mean and loading to change when the economy expands. Its pricing coefficients therefore may depend on $n$. “Stationary” later in the paper means that cross-economy means and loadings for previously included assets remain fixed; it does not mean that a time series has been tested for stationarity.

## Projection and the constructive proof

Let $D_n=[\mathbf1,B^{(n)}]$. Orthogonally project $E^{(n)}$ onto its column space:

$$
E^{(n)}=\rho_n\mathbf1+B^{(n)}\gamma_n+c_n,
\qquad D_n'c_n=0.
$$

An orthogonal projection exists even if columns of $D_n$ are linearly dependent. The fitted vector and residual are unique, although individual factor-price coefficients may not be. Numerically, a QR or singular-value decomposition is preferable to inverting a potentially singular normal-equation matrix.

The residual portfolio has three relevant properties:

$$
\mathbf1'c_n=0,\qquad B^{(n)\prime}c_n=0,
\qquad c_n'E^{(n)}=c_n'c_n.
$$

The first makes it self-financing in this dollar-allocation convention. The second cancels common factors. The third follows because the fitted component is orthogonal to the residual. Writing $S_n=\|c_n\|^2$, a scaled position $d_n=a_nc_n$ therefore has

$$
Z_n=a_nS_n+a_nc_n'\varepsilon^{(n)},
\quad \mathbb E Z_n=a_nS_n,
\quad \operatorname{Var}(Z_n)\le\bar\sigma^2a_n^2S_n.
$$

Suppose $S_n$ were unbounded. There would then be a subsequence along which $S_n\to\infty$. Select any $p\in(-1,-1/2)$ and set

$$
a_n=S_n^p=\|c_n\|^{2p}.
$$

Expected profit equals $S_n^{1+p}$, which diverges because $1+p>0$. Its variance is bounded by $\bar\sigma^2S_n^{1+2p}$, which vanishes because $1+2p<0$. This is exactly the prohibited arbitrage opportunity. Equations (2.14)–(2.18), pp. 187–188, are the full mechanism.

The introductory example uses $p=-3/4$. With this choice, expected profit is $S_n^{1/4}$ and variance is at most $\bar\sigma^2S_n^{-1/2}$. The scale itself decreases; the portfolio still produces growing mean profit because the aggregate residual signal grows faster. This construction does not require equal weights, a fixed gross notional, or each portfolio holding to become small. It exploits orthogonality and the quadratic variance bound, rather than invoking diversification as an unexplained slogan.

## What the two pricing theorems establish

Theorem 1, p. 187, concludes that a finite constant $A$, independent of $n$, exists such that

$$
\sum_{i=1}^n
\left(E_i^{(n)}-\rho_n-\sum_{j=1}^kB_{ij}^{(n)}\gamma_{j,n}\right)^2
\le A.
$$

The coefficients can vary with the economy. The theorem gives no numerical value for $A$. It also does not identify which observed factors should enter $B$, how many observations are needed to estimate it, or a confidence interval for any pricing error.

Two direct implications clarify “approximately linear.” The cross-sectional root-mean-square pricing error is at most $\sqrt{A/n}$. For any fixed tolerance $\epsilon>0$, the number of assets whose absolute error exceeds $\epsilon$ is at most $A/\epsilon^2$, so their fraction is at most $A/(n\epsilon^2)$. These inequalities are deductions from the theorem, not empirical estimates reported by Huberman.

A fixed exceptional asset may nevertheless retain a large error as more assets enter. For example, a square-summable error sequence can contain a single large first component and zeros thereafter. Thus a vanishing average error does not establish accurate pricing of a specified large company. This is the key gap between aggregate asymptotic APT results and finite-economy, asset-by-asset pricing bounds.

Theorem 2, p. 188, strengthens the form of the conclusion when $E_i$ and $B_{ij}$ do not change across economies. There is one common coefficient vector such that

$$
\sum_{i=1}^{\infty}
\left(E_i-\rho-\sum_{j=1}^kB_{ij}\gamma_j\right)^2<\infty.
$$

The proof uses finite-dimensional compactness. The rank of the growing design matrix is a nondecreasing integer bounded by $k+1$, so it eventually stabilizes. Choose independent columns and eliminate redundant coefficient directions. On that identified coordinate space, define $H_n$ as coefficient vectors with first-$n$ squared error no larger than the common bound $A$. The sets are nonempty, closed, bounded, and nested: $H_{n+1}\subseteq H_n$. Their intersection is nonempty, providing coefficients that work for all asset prefixes.

The printed proof has a self-referential sentence about the “first” independent columns being combinations of themselves. The operative step is to express the *remaining* columns through the chosen independent columns; otherwise the asserted compactness would fail in unidentified coefficient directions. This is a clarification of the linear algebra, not an additional financial assumption.

In the stationary case, square summability also implies that the individual errors tend to zero along the asset index. It still does not force the error of each already existing asset to become zero, nor provide a finite-universe tolerance.

## Adding a traded risk-free asset

Suppose a risk-free investment has return $r_{0,n}$. The risky positions no longer have to sum to zero on their own because a position in cash finances their net cost. Project the excess-mean vector onto factor loadings only:

$$
E^{(n)}-r_{0,n}\mathbf1=B^{(n)}\gamma_n+c_n,
\qquad B^{(n)\prime}c_n=0.
$$

Take risky holdings $a_nc_n$ and risk-free holding $-a_n\mathbf1'c_n$. This combined portfolio has zero cost, and its profit is $a_nc_n'(X^{(n)}-r_{0,n}\mathbf1)$. The same mean and variance calculations apply. The corollary on p. 189 gives

$$
\sum_{i=1}^n
\left(E_i^{(n)}-r_{0,n}-\sum_jB_{ij}^{(n)}\gamma_{j,n}\right)^2\le A.
$$

The intercept is now the observed risk-free return, rather than an unrestricted cross-sectional constant. Setting an estimated intercept equal to cash in the original theorem without adding the traded asset would skip an economically meaningful step. A corresponding fixed-coefficient result applies to the stationary model.

## Why convergence in probability does not settle utility

The asymptotic arbitrage definition implies that profit tends to positive infinity in probability. For any fixed $M$, once $\mathbb E Z_n>M$, Chebyshev's inequality gives

$$
\Pr(Z_n\le M)\le
\frac{\operatorname{Var}(Z_n)}{(\mathbb E Z_n-M)^2}\longrightarrow0.
$$

A suitably chosen subsequence has almost-sure divergence as well. Neither statement alone guarantees that every expected-utility investor finds the sequence attractive: extremely unlikely losses can receive enormous marginal disutility.

The two examples on p. 190 make this precise. For integer $n\ge2$, let $Z_n$ equal $0,n,2n$ with probabilities $n^{-3},1-2n^{-3},n^{-3}$. Its mean is $n$ and variance is $2/n$. With $u(x)=-1/x$ for positive wealth and $u(x)=-\infty$ for nonpositive wealth, expected utility is negative infinity at every $n$ because zero occurs with positive probability.

For a finite-valued utility example, let $Z_n$ equal $-n,n,3n$ with the same probabilities, and take $u(x)=-e^{-x}$. Its mean is again $n$, and variance is $8/n$. However,

$$
\mathbb E u(Z_n)=
-\frac{e^n}{n^3}
-\left(1-\frac{2}{n^3}\right)e^{-n}
-\frac{e^{-3n}}{n^3}\longrightarrow-\infty.
$$

The printed inequality on p. 190 uses $-n^3e^n$; the probability calculation requires $-e^n/n^3$. The corrected expression preserves the intended divergence and counterexample. Both variances above are direct calculations supplied here to make the examples reproducible.

Huberman consequently keeps two logical steps separate. No asymptotic arbitrage implies approximate factor pricing under the stated return structure. Deriving no asymptotic arbitrage from equilibrium requires additional restrictions on preferences and admissibility. The discussion mentions bounded-below utility and suitable uniform integrability as ways to control rare losses, while leaving a general preference characterization outside the paper.

## Reconstructing the argument numerically

A faithful numerical illustration starts with a specified sequence of expected returns, loading matrices, and residual covariance matrices; it does not estimate them from a historical dataset supplied by this paper. For each $n$, calculate the orthogonal projection, retain $c_n$, and verify the financing and factor-neutrality residuals to numerical tolerance. Evaluate $S_n$, $a_nS_n$, and the exact variance $a_n^2c_n'\Sigma_{\varepsilon,n}c_n$. Compare the latter with $\bar\sigma^2a_n^2S_n$ under the diagonal residual covariance assumption.

To illustrate the contradiction, design a sequence with growing $S_n$ and use $p=-3/4$. To illustrate compatibility with no forced contradiction, choose bounded $S_n$. Such examples demonstrate the proof's scaling; they are not tests that an actual market violates APT. In the risk-free variant, include the financing position explicitly and verify the combined dollar allocation sums to zero.

A finite estimated residual vector has sampling noise. Using it both to define holdings and to claim positive expected profit mechanically creates in-sample alignment. The theorem contains no estimator, train/test division, signal lag, rebalancing schedule, or realized-return inference procedure. Any empirical application must supply those choices separately and must test whether residual covariance remains controlled as the universe expands.

Pairwise uncorrelated residuals can be replaced in the variance step by a uniform spectral-norm bound on their covariance matrices; that is a mathematical extension of the proof, not the assumption stated in this paper. If omitted common risks make the largest residual covariance eigenvalue grow rapidly, the variance bound supporting arbitrage can disappear. A growing factor count also falls outside the fixed-$k$ stationary compactness argument.

The practical takeaway is an exact accounting of what asymptotic no-arbitrage buys: bounded aggregate pricing disagreement under diversifiable residual risk. It supplies neither a finite-stock fair-value certificate nor a costless implementation of the residual portfolio. The utility examples explain why those missing qualifications cannot be repaired merely by reporting a high signal-to-noise ratio.
