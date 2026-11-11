# Mutual Fund Separation in Financial Theory—The Separating Distributions

**Stephen A. Ross (1978).** *Journal of Economic Theory* 17, 254–286. Source: [APTFundSeparation_1Ross_1978.pdf](../../Finance/APTFundSeparation_1Ross_1978.pdf). All thirty-three pages were read, including the appendix and the three geometric figures. Equations obscured by text extraction were checked against rendered pages. References below use printed page numbers. This is a distributional characterization theorem, not an empirical test of mutual-fund performance.

## Why this matters and the contribution

Reducing portfolio choice to a small menu of funds is a strong claim. It says that investors with very different risk preferences can disagree about how much of each fund to own while agreeing that securities outside the fund span add nothing useful. Mean-variance theory obtains this reduction under familiar special assumptions, but observing two parameters in a distribution does not establish it.

Ross asks the distributional side of the question: which *joint return distributions* permit a common set of funds to serve every risk-averse expected-utility investor? This differs from characterizing a restricted utility family that separates under arbitrary returns. The paper gives necessary and sufficient conditions for one-fund, two-fund, and weak $k$-fund separation. The canonical structure is a common component plus a few systematic directions plus residual noise whose conditional mean vanishes at the relevant fund payoffs.

The main message is that dependence, attainable factor exposures, and conditional residual means determine separation. Normality is a sufficient example, not the essential concept. Conversely, a generic factor representation or a two-parameter marginal family is insufficient. The theorem explains both why some nonnormal markets retain simple portfolio choice and why apparently tractable specifications fail to do so.

## Portfolio and preference conventions

Let $X=(X_1,\ldots,X_n)'$ be random asset returns and let $e$ be the vector of ones. A portfolio $a$ satisfies $a'e=1$ and pays $a'X$. Short sales are unrestricted, so weights may be negative and combinations of funds are affine combinations, not necessarily convex combinations. A zero-cost direction $\eta$ satisfies $\eta'e=0$.

The main utility class $\mathcal U$ contains increasing, concave functions on the real line. Expected utilities are compared only when well defined. Wealth is suppressed because changing an investor's wealth or scale can be represented within the utility class. The paper excludes degenerate environments by requiring at least one strictly increasing, strictly concave utility with a well-defined attained optimum. Otherwise a market containing two riskless assets with unequal returns could generate unbounded gains and make separation statements artificial.

The larger classes $\mathcal C$ and $\mathcal M$ contain all concave utilities and all increasing utilities, respectively. Dropping monotonicity or dropping concavity changes what “efficient” means and changes the necessary noise restrictions. State-dependent utility is outside the main expected-utility class: investors cannot assign different utility to the same monetary payoff solely because it occurs in a different state.

For $Y\succeq Z$, the paper means $\mathbb E u(Y)\ge\mathbb E u(Z)$ for every $u\in\mathcal U$. Its stochastic-dominance discussion represents an inferior distribution as a downward shift plus conditional mean-zero noise added to a better one, on a suitable coupling. Equality in distribution is not equality of the original random variables on their original probability space. That distinction becomes essential in the necessity proof.

## Strong versus weak separation

Fix $k$ funds $a^1,\ldots,a^k$, each fully invested. Strong separation says that for every outside portfolio $b$, there is a portfolio of the funds that dominates $b$ for *all* utilities in $\mathcal U$. Weak separation says that for every outside portfolio and every utility, a fund portfolio can be found that is at least as good, but its choice may depend on that utility.

The order of quantifiers is the difference. Strong separation supplies one universally preferred replacement for the specified outside portfolio. Weak separation allows different replacements for different investors. Strong implies weak. Ross proves equivalence for one and two funds. The general theorem characterizes weak $k$-fund separation; the paper does not establish a blanket strong/weak equivalence for arbitrary $k$.

The number of funds describes a span. Any alternative basis for the same attainable fund-payoff set provides another separating menu. It does not identify economically unique managers or uniquely optimal individual funds. Separation is useful only when $k<n$, and particularly when $k$ is much smaller than $n$.

## One-fund separation: exact conditional-mean characterization

Theorem 1, pp. 261–264, says one-fund separation holds exactly when there are a random payoff $Y$, residuals $\varepsilon_i$, and a portfolio $a$ satisfying

$$
X_i=Y+\varepsilon_i,\qquad
\mathbb E[\varepsilon_i\mid Y]=0,\qquad
a'\varepsilon=0,\qquad a'e=1.
$$

The last two equalities make $a'X=Y$ almost surely. For any other portfolio $b$, conditional expectation gives $\mathbb E[b'X\mid Y]=Y$, so Jensen implies $\mathbb E u(b'X)\le\mathbb E u(Y)$. The residual is unnecessary risk from every concave investor's perspective.

The necessity is more demanding. If $a$ dominates every portfolio, it must dominate $a+\lambda\eta$ for every zero-cost direction $\eta$ and both signs of $\lambda$. Stochastic dominance supplies mean-zero-noise representations of the *distributions* of those alternatives. Appendix Theorem A2 is then needed to conclude that the actual deviation has zero conditional mean given $Y=a'X$. Defining $\varepsilon_i=X_i-Y$ yields the required representation and $a'\varepsilon=0$.

The source's example on pp. 262–263 shows why one distributional comparison is insufficient. Let $Y$ be $1$ or $-1$ with equal probabilities. Conditional on $Y=1$, let a deviation $D$ be $-1$ or $-3$ with equal probabilities; conditional on $Y=-1$, let $D$ be $3$ or $1$. Then $Y+D$ has outcomes $2,0,-2$ with probabilities $1/4,1/2,1/4$, the same distribution as $Y$ plus an independent symmetric $\pm1$ noise. Yet $\mathbb E[D\mid Y]=-2Y$, not zero. The theorem needs comparisons over every scale and direction, not merely that one payoff is distributed as another plus some noise.

All assets in a one-fund-separating market have the same expected return. When variances exist, the separating portfolio is minimum variance: for $b=a+\eta$,

$$
\operatorname{Var}(b'X)=\operatorname{Var}(Y)+\eta'\operatorname{Cov}(\varepsilon)\eta.
$$

Equal means alone do not establish this dominance; the conditional-mean restriction does. Likewise, minimum variance alone is insufficient outside distributions where the residual noise has the required conditional relationship.

Exchangeable returns provide a useful example. If the joint law is invariant under asset permutations, the conditional expectation of each return given their average equals that average. Equal weighting therefore satisfies the theorem, whether or not the joint law is normal or stable. Figure 2 gives a two-state illustration with equally likely states and securities paying $(1,0)$ and $(0,1)$: the equal-weight portfolio pays $1/2$ for sure. State-dependent preferences could favor either pure state claim and would destroy the universal one-fund conclusion.

## Two-fund separation and the domain of conditioning

Theorem 2, pp. 267–270, characterizes weak two-fund separation by

$$
X_i=Y+b_iZ+\varepsilon_i,
\qquad
\mathbb E X_i=\mathbb E Y+b_i\mathbb E Z,
$$

with two fully invested portfolios $a,d$ for which

$$
a'\varepsilon=d'\varepsilon=0.
$$

If the loading vector $b$ is not constant, their loadings must differ; orient the basis so $a'b>d'b$. The crucial residual condition is

$$
\mathbb E[\varepsilon_i\mid Y+\xi Z]=0
\quad\text{for every relevant }\xi\in A.
$$

Here $A$ is determined by factor exposures attainable at utility-optimal portfolios. The theorem describes its interior through the infimum and supremum of those exposures. When expected returns are nonconstant and the factor is oriented consistently with increasing mean return, the upper endpoint is unbounded. Boundary cases are obtained through closure where the required continuity applies.

One must not replace this condition by $\mathbb E[\varepsilon_i\mid Y]=0$, by unconditional uncorrelatedness, or by independence at only one particular efficient portfolio. Investors choose different exposures to $Z$; the conditional restriction has to hold over the relevant range of resulting wealth payoffs.

For an outside portfolio $g$ with exposure $g'b=\xi\in A$, solve

$$
\lambda=\frac{g'b-d'b}{a'b-d'b},\qquad
h=\lambda a+(1-\lambda)d.
$$

Then $h'e=1$, $h'b=g'b$, and $h'\varepsilon=0$. Writing $g=h+\eta$ gives $\eta'e=\eta'b=0$ and

$$
g'X=h'X+\eta'\varepsilon,
\qquad \mathbb E[\eta'\varepsilon\mid h'X]=0.
$$

Thus $h$ dominates $g$. For exposures outside the relevant efficient interval, the proof of strong/weak equivalence uses concavity and the appropriate boundary portfolio. It does not assume that every loading is itself optimal for an increasing utility.

For the class of all concave utilities, including nonmonotone ones, the relevant exposure domain expands to the whole real line when expected returns are unequal. Under increasing concave utility, inefficient low-mean portions of a minimum-variance frontier can be excluded. The appendix notes that the lower endpoint need not be attained: for a nonsingular normal model, the global minimum-variance point is a boundary of the increasing-utility efficient set.

## Necessity and the appendix's role

Suppose every relevant optimum lies on the affine line of two funds. Let

$$
Q=\lambda a'X+(1-\lambda)d'X.
$$

The first-order condition for changing the fund allocation is $\mathbb E[u'(Q)(a'X-d'X)]=0$. This must imply the full collection of security-level first-order conditions $\mathbb E[u'(Q)(X_i-X_j)]=0$ for the admissible increasing concave utilities.

Define $v(Q)=\mathbb E[a'X-d'X\mid Q]$ and $S_i(Q)=\mathbb E[X_i\mid Q]$. Appendix Theorem A1 turns the implication over the class of decreasing nonnegative marginal-utility functions into an almost-sure proportionality:

$$
S_i(Q)-S_1(Q)=b_i v(Q).
$$

The theorem uses a test-function argument: perturb a strictly decreasing admissible function by sufficiently small compactly supported piecewise-linear functions, and then use that these functions separate integrable quantities. The proportionality constant does not depend on the state $Q$. Taking expectations yields linear expected returns, and solving the two fund-payoff equations produces $Y,Z$, and the conditional residual representation.

The technical appendix also supplies continuity and density arguments for the relevant exposure set. Mixing a strictly concave objective with a linear mean-return objective traces a continuous range of optimal mean returns. The attainable mean set for increasing concave utilities is an interval unbounded above; for all concave utilities it extends across the real line. A smooth, strictly curved subclass has the same closure, permitting the first-order-condition argument to reach less regular utilities by approximation.

These are proof ingredients under the paper's existence and integrability framework. They are not an algorithm that guarantees a global optimum for arbitrary heavy-tailed distributions or utilities with undefined expectations. In particular, a heavy-tailed “stable” label does not remove the need for the expectations invoked in the representation to exist.

## Normal returns as a constructive example

Suppose there is a riskless return $r_f$, risky expected-return vector $\mu$, and positive-definite covariance $V$. Let $m=\mu-r_fe$ and assume $m\ne0$. Define

$$
a=\frac{V^{-1}m}{m'V^{-1}m},
\qquad Z=a'(X-r_fe).
$$

Then $\mathbb E Z=1$. The residual vector

$$
\varepsilon=X-r_fe-mZ
$$

has zero mean and zero covariance with $Z$, because

$$
\operatorname{Cov}(X-r_fe,Z)=\frac{m}{m'V^{-1}m},
\qquad
\operatorname{Var}(Z)=\frac1{m'V^{-1}m}.
$$

For jointly normal variables, zero covariance implies independence and hence $\mathbb E[\varepsilon\mid Z]=0$. The return representation is $X_i-r_f=(\mu_i-r_f)Z+\varepsilon_i$. The risky vector $a$ is normalized to unit expected excess return, not necessarily to weights summing to one; cash completes the overall portfolio. This avoids confusing a factor-mimicking position with a fully invested fund.

The Gaussian calculation is a direct instance of the theorem, not its general form. The printed intermediate line on p. 273 says $Y+b_0Z=0$ for the riskless security; before shifting to excess returns it should equal $r_f$. The subsequent excess-return formula is the coherent one used above.

When variances exist more generally, separating portfolios minimize residual dispersion for a given mean, so two independent points spanning the appropriate mean-variance frontier can serve as a basis. But knowing only the mean and covariance of an arbitrary nonnormal return vector does not prove that its mean-variance frontier is optimal for every expected utility. The joint conditional structure remains essential.

## General weak k-fund separation

Theorem 3, p. 277, replaces the single discretionary factor by $k-1$ directions:

$$
X_i=Y+\sum_{j=1}^{k-1}b_{ij}Z_j+\varepsilon_i.
$$

The conditional residual means must vanish given $Y+\xi'Z$ for the relevant optimal-exposure set $A=\{\gamma(u)B:u\in\mathcal U\}$, where $\gamma(u)$ is an optimal portfolio for utility $u$, and each of the $k$ funds must eliminate the residual payoff. Let $F$ have the fund holdings as rows and let $D=[e,B]$. The fund exposures are $FD=[\mathbf1,FB]$. The source requires the ranks of corresponding column submatrices of $D$ and $FD$ to agree; this ensures that the fund menu spans all required combinations of total investment and factor exposure.

The expected-return equation follows by expectation:

$$
\mathbb E X_i=\mathbb E Y+
\sum_{j=1}^{k-1}b_{ij}\mathbb E Z_j.
$$

The printed expected-return line in condition (CK) ends the sum at $k-2$, unlike its own payoff line. Taking expectations makes $k-1$ the consistent upper limit. A reproduction should use the latter and record the source typo.

The theorem makes room for redundant factor descriptions. If fewer independent systematic directions suffice, the effective dimension can be smaller than the nominal count. What matters is attainable payoff and exposure span. The paper gives only a short generalization argument for the theorem and does not supply a full geometric characterization of $A$ when $k>2$; footnote 13 describes pathwise connectedness and extensions of the appendix arguments rather than a closed-form domain.

## Factor pricing, approximate separation, and limits

A generic one-factor model $X_i=\mu_i+b_iZ+\varepsilon_i$ is not enough. Even if residuals can be removed, securities with equal factor exposure could offer different expected returns unless means lie on the required affine loading relation. With residuals identically zero, absence of arbitrage forces that relation. With nonzero residuals, further conditions are needed; writing an algebraic factor model by itself imposes little economic content.

With a riskless asset and two-fund separation, every efficient portfolio is free of residual risk. If investors share the return law and market clearing aggregates their efficient holdings, the market can be selected as the risky separating fund. After normalizing its factor loading to one, the expected-return relation becomes

$$
\mathbb E X_i-r_f=b_i(\mathbb E X_M-r_f).
$$

Where covariances exist and the appropriate residual orthogonality holds, $b_i$ is the usual market beta. The derivation is conditional on separation and equilibrium aggregation. It is not a claim that a market factor estimated from arbitrary data automatically satisfies the theorem.

Section 4 sketches approximate separation when diversified portfolios make residual risk small. It links that intuition to APT but does not derive a finite-universe error tolerance or a bound on utility loss from restricting investors to estimated funds. Such a quantitative approximation cannot be inferred from the exact theorems without additional control of tails, constraints, and estimation error.

To reconstruct a finite-state example, specify state probabilities and all asset payoffs, choose candidate fund holdings, verify unit investment and exposure-spanning identities, and calculate residuals state by state. Group states sharing each relevant fund payoff and compute conditional residual means. Checking only a finite selection of utilities or factor exposures is a diagnostic, not proof of the universal condition for a continuum of exposures. For a parametric continuous model, establish the conditional expectations analytically or identify additional structure, as normality does in the Gaussian example.

The source supplies no historical dataset, return horizon, transaction-cost assumptions, optimizer tolerances, validation sample, or empirical rejection test. Its results are exact statements about known joint distributions. Short-sale restrictions change the feasible replacements; state-dependent utility changes the preference class; and nontraded endowments can change the conditioning wealth variable. Each can invalidate a fund reduction that holds in the model. The practical lesson is to justify the common fund span through conditional payoff structure, rather than treating dimensionality reduction as a consequence of naming a few factors.
