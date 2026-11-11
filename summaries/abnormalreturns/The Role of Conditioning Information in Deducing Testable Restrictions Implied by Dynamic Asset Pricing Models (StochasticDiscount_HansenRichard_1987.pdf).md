# The Role of Conditioning Information in Deducing Testable Restrictions Implied by Dynamic Asset Pricing Models

## Source and scope

**Lars Peter Hansen and Scott F. Richard**, *Econometrica* 55(3), May 1987, pp. 587–613. Original PDF: [StochasticDiscount_HansenRichard_1987.pdf](../../Finance/StochasticDiscount_HansenRichard_1987.pdf).

The complete 30-page file was read, including the mathematical appendix on journal pp. 605–612 and three appended JSTOR linked-reference pages. The conditional representation theorem, frontier decomposition, beta representation, pseudo-pricing construction, and central appendix proofs were checked against images of PDF pp. 8, 11, 13, 14, 16, 24, and 25. This is a theoretical paper: there is no estimated dataset, backtest, numerical experiment, or empirical table to reproduce.

## Why this matters

A portfolio can be mean–variance efficient conditional on investors' information and fail an unconditional mean–variance test. The failure is not necessarily an estimation problem. It can occur with exact population moments because averaging over states changes the optimization problem. Hansen and Richard characterize the portfolios for which efficiency survives that averaging and show how to formulate valid unconditional moment restrictions without assuming that conditional betas can simply be replaced by unconditional betas.

The practical consequence is direct. A regression alpha against a fixed unconditional benchmark may reject a conditional equilibrium model or a manager's conditional efficiency for the wrong reason. Conversely, using unconditional moments is not inherently invalid: Euler equations can be averaged after payoffs and their actual prices have been multiplied by information available at the trading date. The information is retained through the managed payoff space rather than through a naive constant-beta representation.

The paper therefore supports two distinct lessons. Conditional frontier implications require conditioning-aware tests. Conditional pricing equations can yield valid unconditional moments through a sufficiently rich collection of instruments and payoffs. The first is a warning about changing the economic restriction; the second is a constructive route to empirical testing.

## Main contribution and logical scope

The authors begin with a pricing function, rather than deriving one from preferences or technology. Their contribution concerns the passage from that function to observable moment restrictions. Economic models inducing the same pricing function are observationally equivalent using the specified payoff and price data. Other data are needed to distinguish their primitive stories.

The mathematical contribution extends Hilbert-space representation and projection arguments to a setting where portfolio weights and prices are random variables measurable at the investment date. This accommodates changing information without treating current prices as fixed numbers from an outside econometrician's perspective. The conditional Riesz representation then produces two canonical payoff directions that characterize conditional and unconditional mean–variance frontiers.

The analysis allows a restricted marketed payoff space. Mathematical completeness of that space means closure under the chosen convergence notion, not economic completeness of markets. This distinction is essential: a closed space can omit many contingent claims. The unique representing payoff *inside that space* need not be a unique economic SDF across every possible future payoff.

## Probability structure and data interpretation

Let $(\Omega,\mathcal F,P)$ be a probability space. Let $\mathcal G\subseteq\mathcal G_1\subseteq\mathcal F$ denote information at trading and payoff dates. Denote by $I$ and $I_1$ the corresponding measurable random variables. Portfolio payoffs belong to $I_1$; prices and portfolio decision weights belong to $I$.

The introductory data example uses a measure-preserving transformation $S$ and observations $x_t=x\circ S^t$. This gives strict stationarity. Under ergodicity and integrability,

$$
\frac1T\sum_{t=1}^T x_t\longrightarrow E[x]
\quad\text{almost surely}.
$$

Without ergodicity the limit is generally conditional on the invariant sigma algebra. The paper adopts ergodicity for this example to connect population moments to time averages. It does not claim every dynamic asset-pricing process is stationary and ergodic. The later mathematical results do not depend on this particular data-generating construction.

The authors effectively grant the econometrician an infinite time series in order to focus on population identification. Finite-sample covariance estimation, high-dimensional regularization, parameter uncertainty, and the choice of instruments are not solved here. Inference under dependent observations is acknowledged separately, with a reference to the GMM asymptotic framework.

## Conditional payoff geometry

Define the large payoff class

$$
\mathcal P^+=\{p\in I_1:E[p^2\mid\mathcal G]<\infty\ \text{almost surely}\}.
$$

Conditional square integrability need not imply an unconditional finite second moment. For $p,q\in\mathcal P^+$ define

$$
\langle p,q\rangle_{\mathcal G}=E[pq\mid\mathcal G],
\qquad
\|p\|_{\mathcal G}=\sqrt{E[p^2\mid\mathcal G]}.
$$

These are random variables measurable with respect to $\mathcal G$. Conditional convergence means $\|p_j-p\|_{\mathcal G}\to0$ in probability. A conditionally linear marketed space $\mathcal P$ is closed under $w_1p_1+w_2p_2$ for weights $w_1,w_2\in I$. Thus the available information determines the allowed portfolio formation operations.

The four main assumptions are:

1. $\mathcal P$ is a conditionally complete linear subspace of $\mathcal P^+$.
2. Pricing is conditionally value additive: $\pi(w_1p_1+w_2p_2)=w_1\pi(p_1)+w_2\pi(p_2)$.
3. Pricing is conditionally continuous at zero: conditional convergence of payoffs to zero implies convergence of prices to zero in probability.
4. There exists a payoff with a price that is nonzero almost surely, ruling out a locally trivial pricing function.

The continuity assumption makes infinite-dimensional limits economically meaningful: sufficiently small payoffs cannot retain nonvanishing prices. The paper gives sufficient conditions under which positivity of pricing on the entire $\mathcal P^+$ implies continuity. That result is stronger than merely assuming no arbitrage on a finite menu of securities. Assigning finite prices to every conditionally square-integrable claim is a substantive requirement, and the authors explicitly discuss it as such.

Under these assumptions, a unique $p^*\in\mathcal P$ represents the pricing function:

$$
\boxed{\pi(p)=E[pp^*\mid\mathcal G]\quad\text{for every }p\in\mathcal P.}
$$

Its conditional norm is nonzero almost surely. In modern terminology $p^*$ is the payoff-spanned conditional pricing kernel. If pricing is defined on all $\mathcal P^+$, no arbitrage is equivalent to $p^*>0$ almost surely. For a restricted marketed space, one must not automatically infer the same positivity property for the projected representative: positivity of an extension and positivity of its projection are different claims.

## How the representation proof works

Let

$$
\mathcal Z=\{p\in\mathcal P:\pi(p)=0\}
$$

be the zero-price subspace. Conditional continuity makes it closed. Choose the nonzero-price payoff $p_0$ from assumption 4 and project it conditionally onto $\mathcal Z$, obtaining $z_0$. Define

$$
r^*=\frac{p_0-z_0}{\pi(p_0)}.
$$

Conditional value additivity makes its price one, and projection makes it orthogonal to $\mathcal Z$. Any payoff has the decomposition

$$
p=\pi(p)r^*+[p-\pi(p)r^*],
$$

where the bracketed term has zero price. Taking its conditional inner product with $r^*$ gives

$$
E[pr^*\mid\mathcal G]
=\pi(p)E[(r^*)^2\mid\mathcal G].
$$

Hence

$$
p^*=\frac{r^*}{E[(r^*)^2\mid\mathcal G]}.
$$

The denominator cannot vanish on a positive-probability trading-date event because a payoff with unit price cannot be identically zero on that event under conditional linearity. Uniqueness follows by applying the difference of two putative representation functions to the difference of their representing payoffs: the resulting conditional squared norm must be zero.

The appendix establishes the needed conditional projection theorem rather than assuming it. It first shows that conditional Cauchy sequences are Cauchy in probability, uses a subsequence and Borel–Cantelli argument to construct the limit, and controls the conditional norm by Minkowski's inequality. For projection, it starts with ordinary $L^2$ projection on an unconditionally closed subspace. If a better conditional approximation existed on a known event, switching to it only on that event would improve the unconditional objective, a contradiction. Payoffs without finite unconditional second moment are handled by measurable rescaling. These steps explain why ordinary Hilbert-space intuition survives even though the conditional norm is random-valued.

## Two canonical directions and the conditional frontier

The return set consists of unit-price payoffs,

$$
\mathcal R=\{r\in\mathcal P:\pi(r)=1\}.
$$

The minimum conditional second-moment return is

$$
r^*=\frac{p^*}{E[(p^*)^2\mid\mathcal G]}.
$$

It is conditionally orthogonal to every zero-price payoff. Every return is $r^*+z$ for $z\in\mathcal Z$. Orthogonality immediately proves

$$
E[r^2\mid\mathcal G]
=E[(r^*)^2\mid\mathcal G]+E[z^2\mid\mathcal G]
\ge E[(r^*)^2\mid\mathcal G].
$$

The paper next excludes conditional risk neutrality by assuming a zero-price payoff with a conditional mean nonzero almost surely. Apply the representation theorem to the conditional expectation functional on $\mathcal Z$. It produces a unique $z^*\in\mathcal Z$ such that

$$
E[zz^*\mid\mathcal G]=E[z\mid\mathcal G]
\quad\text{for every }z\in\mathcal Z.
$$

Thus

$$
E[(z^*)^2\mid\mathcal G]=E[z^*\mid\mathcal G],
\qquad 0<E[z^*\mid\mathcal G]\le1.
$$

The upper bound follows from nonnegative variance. Define the residual subspace

$$
\mathcal N=\{z\in\mathcal Z:E[z\mid\mathcal G]=0\}.
$$

Then every return can be expressed as

$$
r=r^*+wz^*+n,
\qquad w\in I,\quad n\in\mathcal N,
$$

with the three components conditionally orthogonal in the second-moment inner product. Orthogonality here is not the same as zero conditional covariance between $r^*$ and $z^*$: their conditional means generally are nonzero.

For a prescribed conditional mean $\mu_c\in I$, choose

$$
w^*=\frac{\mu_c-E[r^*\mid\mathcal G]}{E[z^*\mid\mathcal G]}.
$$

The unique minimum conditional second-moment return at that mean is

$$
r_c=r^*+w^*z^*.
$$

The residual $n$ adds second moment without changing mean or price, so it is discarded. This is a conditional two-fund theorem, with weights that may depend on the state. The terminology “frontier” includes the full minimum-variance locus; it does not by itself assert that every point lies on the upper economically efficient branch for a monotone mean–variance preference.

## Unconditional efficiency and the omitted-information result

Restrict to $\mathcal P_2=\{p\in\mathcal P:E[p^2]<\infty\}$ and assume at least one return has a finite unconditional second moment. Then $r^*$ and $z^*$ are unconditionally square integrable. Iterated expectations give

$$
E[zz^*]=E[z]
$$

for zero-price, square-integrable $z$. Define the unconditional zero-mean residual subspace by requiring only $E[n_0]=0$, which is a weaker condition than $E[n\mid\mathcal G]=0$. For an unconditional target mean $\mu_u$, the minimum-variance return is

$$
\boxed{r_u=r^*+cz^*,\qquad
c=\frac{\mu_u-E[r^*]}{E[z^*]}.}
$$

The coefficient $c$ is a real constant. The canonical payoff directions themselves can be dynamic managed payoffs; “constant coefficient” does not mean fixed weights in the original primitive assets.

Every unconditional frontier return is consequently on the conditional frontier at its own conditional mean. The converse fails: a conditional-frontier return with a nonconstant coefficient $w$ will generally have an avoidable unconditional component. The paper identifies precisely the condition, under its nondegeneracy assumptions: $r^*+wz^*$ is on the unconditional frontier if and only if $w$ is constant almost surely.

One can make the loss explicit. For a given conditional-frontier return set

$$
c=\frac{E[wz^*]}{E[z^*]},\qquad
n_0=(w-c)z^*.
$$

It has $E[n_0]=0$ and is unconditionally orthogonal to $z^*$ because

$$
E[(w-c)(z^*)^2]
=E[(w-c)E[z^*\mid\mathcal G]]
=E[(w-c)z^*]=0.
$$

It is also orthogonal to $r^*$. The two returns $r^*+wz^*$ and $r^*+cz^*$ have the same unconditional mean, while their variance difference is

$$
E[((w-c)z^*)^2]\ge0.
$$

This derivation is a useful implementation form of the paper's geometry. It shows the exact second-moment penalty from state-dependent movement along the conditional frontier when the objective is unconditional mean–variance efficiency.

## A conditionally risk-free return can be unconditionally inefficient

Suppose a unit payoff is marketed and pricing has no arbitrage. Its price is $E[p^*\mid\mathcal G]$, so the risk-free gross return is

$$
r_f=\frac{1}{E[p^*\mid\mathcal G]}.
$$

It is known at the trading date but may vary across dates or states. In this case

$$
z^*=1-
\frac{E[r^*\mid\mathcal G]}{E[(r^*)^2\mid\mathcal G]}r^*,
$$

and

$$
r_f=r^*+r_fz^*.
$$

The preceding characterization implies that this risk-free return lies on the unconditional frontier if and only if it is constant almost surely. Its conditional variance is zero, but its unconditional variance includes variation in the conditional mean. There is no contradiction: the unconditional optimization compares strategies across those varying investment opportunities, while conditional optimization treats the current state as known.

The example is more informative than merely saying that betas vary. It shows that even the asset that is safest at every decision date can fail unconditional frontier efficiency. The distinction concerns the investment objective and the available managed return space, not necessarily a failure of rational pricing.

## Beta representations and their exclusions

A conditional reference return $r_\beta$ provides a single-beta representation when its conditional variance is nonzero and there is a trading-date measurable intercept $a$ such that

$$
E[r\mid\mathcal G]-a
=\frac{\operatorname{Cov}(r_\beta,r\mid\mathcal G)}
{\operatorname{Var}(r_\beta\mid\mathcal G)}
\{E[r_\beta\mid\mathcal G]-a\}
$$

for every marketed return. If a risk-free return exists, it supplies the intercept. Under the paper's assumptions, a reference return exists precisely when it lies on the conditional frontier and is not the conditional global minimum-variance return. Writing $r_\beta=r^*+wz^*$, the excluded coefficient is

$$
v(\mathcal G)=\frac{E[r^*\mid\mathcal G]}
{1-E[z^*\mid\mathcal G]}.
$$

The no-arbitrage condition rules out the relevant zero denominator. The appendix verifies the forward direction through conditional moment calculations. For the reverse direction, a residual $n$ outside the two canonical directions would contribute variance without the covariance/mean relation required of all returns; the assumed beta representation forces that residual to vanish. The minimum-variance exclusion is substantive because a beta-pricing representation cannot use the same degeneracy to price a return with a different conditional mean.

The unconditional analogue replaces conditional expectations with unconditional ones and requires a constant coefficient $c$, excluding

$$
c=\frac{E[r^*]}{1-E[z^*]}.
$$

A standard regression test therefore assesses unconditional frontier efficiency of the reference return. A conditional CAPM-like model may imply only conditional efficiency of aggregate wealth or a consumption-related portfolio. There is no general reason those implications coincide. Omitting some securities from the regression may weaken the test, but does not generally repair the mismatch in the economic restriction being tested.

An auxiliary covariance decomposition makes the issue familiar:

$$
\operatorname{Cov}(r_i,r_\beta)
=E[\operatorname{Cov}(r_i,r_\beta\mid\mathcal G)]
+\operatorname{Cov}(E[r_i\mid\mathcal G],E[r_\beta\mid\mathcal G]).
$$

Meanwhile the average conditional premium involves products of state-dependent betas and premiums. The unconditional covariance ratio need not equal the appropriate average beta, and products do not commute with expectations. This is intuition for the formal theorem, not an alternative set of sufficient assumptions.

## Pseudo-prices and valid unconditional moment restrictions

Assume additionally $E[(p^*)^2]<\infty$. For square-integrable marketed payoffs define

$$
\pi^*(p)=E[\pi(p)]=E[pp^*].
$$

The new function has real-valued prices, is a continuous linear functional in ordinary $L^2$, and inherits no arbitrage from the original function on the relevant payoff space. The same $p^*$ represents both conditional pricing and pseudo-pricing.

This provides an unconditional test of a proposed model kernel: compare the sample counterparts of $E[pp^*]$ and the **average actual price** $E[\pi(p)]$. It does not reinterpret every expected price as an actual tradable constant price. For example, the pseudo-risk-free return $1/E[p^*]$ differs from the actual known-at-trading-date return $1/E[p^*\mid\mathcal G]$. An asset with pseudo-price one need not have actual price one in every state.

To use information, form $w(\mathcal G)p$ and its actual price $w(\mathcal G)\pi(p)$. Their unconditional restriction is

$$
E\{w(\mathcal G)[pp^*-\pi(p)]\}=0.
$$

These are the instrumented Euler equations used in GMM. Weights may depend only on information available at purchase, and the resulting products must satisfy the integrability requirements. A predictive variable observed only at payoff time cannot be slipped into the instrument vector while retaining the same economic argument.

The additional square-integrability assumption is not invariant to every numeraire change. If prices are divided by a positive trading-date variable $w$, the representative becomes $p^*/w$, which may lose its unconditional second moment. Conversely, appropriate rescaling can restore integrability. Thus an apparently technical $L^2$ requirement also constrains how prices are denominated. It is not enough to check that each return series has a sample variance.

## What information is lost, and where

Suppose two pricing functions have square-integrable representatives $p^*$ and $q^*$ and agree on pseudo-prices for every payoff in $\mathcal P_2$. Choose the admissible payoff $p=p^*-q^*$. Then

$$
E[(p^*-q^*)^2]=0,
$$

so the representatives and conditional pricing functions agree almost surely. Therefore averaging prices does not by itself destroy identification when the entire appropriate managed payoff space is retained.

The practical restriction is that researchers test only a finite subset. On a smaller closed subspace, distinct kernels can have the same projection and identical tested moments. The difference can live in orthogonal directions never examined. A zero alpha on 25 portfolios, for example, need not establish correct pricing of all instrument-scaled securities. More instruments may expose omitted directions, but this theoretical paper does not quantify the finite-sample cost of enlarging the test system.

The concluding APT discussion makes a parallel point. A conditional factor structure or restriction on the number of diverging covariance eigenvalues need not survive unconditional averaging. Conversely, assumptions on unconditional covariance may fail under state-dependent portfolio formation. This does not disprove APT; it shows that the primitive asset space, conditioning set, and allowed trading strategies must be specified before importing a covariance restriction into a dynamic model.

## Finite-asset reconstruction and verification

For an applied implementation, let $Y$ be a vector of terminal payoffs with trading-date price vector $q$, and let $M=E[YY'\mid\mathcal G]$ be nonsingular. The conditional payoff-spanned representative is

$$
p^*=q'M^{-1}Y,
$$

because $E[Yp^*\mid\mathcal G]=q$. Let $\mu=E[Y\mid\mathcal G]$. Then

$$
r^*=\frac{q'M^{-1}Y}{q'M^{-1}q},
$$

and the zero-price expectation direction is

$$
z^*=\mu'M^{-1}Y-
\frac{q'M^{-1}\mu}{q'M^{-1}q}\,q'M^{-1}Y.
$$

These expressions are a finite-dimensional reconstruction of the paper's projection results. They require the portfolio span generated by the available conditional weights and should not be described as a separate empirical estimator supplied by the authors.

A useful verification checks $\pi(r^*)=1$, $\pi(z^*)=0$, $E[r^*z^*\mid\mathcal G]=0$, and $E[(z^*)^2\mid\mathcal G]=E[z^*\mid\mathcal G]$. One can then construct both frontier families and verify the nonnegative variance gap for a varying conditional coefficient. These identities detect mistakes in using second moments versus covariances, in normalizing prices, or in treating a random target mean as a fixed target.

The paper supplies no calibration from which a numerical performance result can be recreated. A demonstration needs an explicit state distribution, conditional payoff moments, prices, and tradability/information conventions. A real-data test additionally needs timestamped instruments, dependence-robust inference, and a rule for estimating conditional moments. Those are missing empirical inputs, not gaps in the paper's population theorem.

Its durable contribution is the exact distinction between conditional pricing, conditional efficiency, unconditional efficiency, and unconditional instrumented moments. A researcher can average the correct pricing equation; they cannot generally average a conditional frontier claim and expect an ordinary constant-beta regression to test the same proposition.

## A finite-state demonstration of the frontier distinction

The following analytical example is constructed to make the theorem testable in a small program; it is not a calibration or numerical example reported by the authors. Suppose the trading-date state is $A$ or $B$, each with probability one half. In either state there are two equally likely terminal outcomes. Assume complete contingent trading conditional on the current state and use a positive conditional pricing representative with values

| Trading state | Two terminal values of $p^*$ | $E[p^*\mid\mathcal G]$ | $E[(p^*)^2\mid\mathcal G]$ |
|---|---|---:|---:|
| $A$ | $(0.5,1.5)$ | $1$ | $1.25$ |
| $B$ | $(0.4,0.8)$ | $0.6$ | $0.4$ |

Define conditional prices by $\pi(Y)=E[p^*Y\mid\mathcal G]$. Positivity of $p^*$ ensures that nonnegative nonzero contingent payoffs have positive conditional prices. The formulas above then give

$$
r^*\bigm|A=(0.4,1.2),\qquad z^*\bigm|A=(0.6,-0.2),
$$

$$
r^*\bigm|B=(1,2),\qquad z^*\bigm|B=(0.4,-0.2).
$$

A direct two-outcome calculation verifies conditional unit price for $r^*$, zero price for $z^*$, and their conditional orthogonality. In the two states, respectively, $E[z^*\mid\mathcal G]$ is $0.2$ and $0.1$, and equals the conditional second moment of $z^*$.

The risk-free return is $1$ in state $A$ and $5/3$ in state $B$. It has zero conditional variance in either state and unconditional mean $4/3$. Its canonical frontier coefficient is therefore $w_A=1$ and $w_B=5/3$, which varies with the current state. The unconditional frontier return with the same unconditional mean instead uses

$$
c=\frac{E[wz^*]}{E[z^*]}=\frac{11}{9}.
$$

The theorem's variance-gap formula gives

$$
\operatorname{Var}(r_f)-\operatorname{Var}(r^*+cz^*)
=\frac12\left(-\frac29\right)^2(0.2)
+\frac12\left(\frac49\right)^2(0.1)
=\frac{2}{135}>0.
$$

Indeed, the varying risk-free return has unconditional variance $1/9$, whereas the constructed unconditional-frontier return has variance $13/135$. Both have the same unconditional mean and conditional price one. The improvement does not eliminate risk within each trading state: it reallocates the pattern of payoffs across the full unconditional experiment, which is exactly the objective being optimized.

A short verification can enumerate the four equally likely terminal outcomes, calculate conditional means by state, and calculate unconditional moments over all four observations. It should not replace the varying risk-free return by one constant average return, because doing so changes the payoff and erases the effect under study. Nor should it assume that the constant canonical coefficient $11/9$ corresponds to constant holdings in primitive securities. The canonical directions themselves depend on the state.

This example also clarifies the empirical interpretation. An investor who knows the current state may sensibly choose the locally riskless investment, while an unconditional mean–variance comparison judges that strategy using variation in opportunities across states. The discrepancy is a consequence of different objectives and information conditioning. It is not an arbitrage or a contradiction of the conditional pricing equations.
