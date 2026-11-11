# Econometric Evaluation of Asset Pricing Models

Lars Peter Hansen, John Heaton, and Erzo G. J. Luttmer. *Review of Financial Studies* 8(2), 1995, pp. 237–274.

Source: [AssetPricing_HansenHeatonLuttmer_1995.pdf](../../Finance/AssetPricing_HansenHeatonLuttmer_1995.pdf). The local file has 39 pages: a JSTOR cover followed by the 38-page article. Printed page numbers are used below; add one to the article-relative page for the PDF location. The library's `AssetPricingEvaluation_Hansen_1995.pdf` is another wrapper of this same article, not a separate work. The entire article and Appendices A–C were inspected.

## Why this matters

Asset-pricing models can fail as exact descriptions and still differ substantially in economic usefulness. A rejection probability does not measure the magnitude of the adjustment required to make a proposed stochastic discount factor price securities correctly. Nor does a large sample guarantee that a visually compelling minimum-volatility frontier is precisely estimated. This paper supplies statistical foundations for two complementary assessments: the distance from a proposed discount factor to the set of admissible discount factors, and the minimum volatility any admissible discount factor must possess.

The innovation is an inference framework that accommodates short-sale restrictions and proportional transaction costs. It separates statistical uncertainty in an optimized bound from uncertainty in the multipliers that construct that bound. The former often has a simple normal limit even when the latter is complicated by inequality constraints. This distinction is useful when comparing misspecified models, testing a model's implied first two discount-factor moments, or asking whether additional securities materially tighten a pricing restriction.

This is a methodological paper. It does not estimate an equity premium, report an investment backtest, or select a winning empirical factor model. Its applications are procedures rather than tables of fitted results. The numerical inputs for an implementation must come from a separately specified dataset and model. Treating the paper as an empirical demonstration would invent evidence it does not contain.

## Payoffs, prices, information, and admissibility

Let $x$ be an $n$-vector of next-period payoffs and $q$ the corresponding vector of prices at the time the positions are chosen. Prices may be random: they can reflect information known at trade time. Let $m$ be a stochastic discount factor and let $\mathcal F$ denote that information. Frictionless conditional pricing implies $q=E(mx\mid\mathcal F)$. The paper works primarily with the unconditional restrictions $Eq=E(mx)$, which are necessary consequences of conditional pricing, not a claim that unconditional tests exhaust all conditional restrictions.

Conditioning information can enter by multiplying payoffs and prices by instruments measurable at the trading date. Such transformations must preserve timing. A realized future return is not an admissible trading-date instrument. If a security is subject to a short-sale restriction, multiplying its payoff by a signed instrument can also change the feasible portfolio set; the transformed assets and restrictions must be constructed consistently rather than imported mechanically from frictionless GMM.

Partition the securities into $k$ unrestricted and $\ell$ short-sale-constrained components. Feasible portfolio weights belong to

$$
C=\mathbb R^k\times\mathbb R_+^\ell,
\qquad n=k+\ell.
$$

The payoff space is the cone $P=\{a'x:a\in C\}$. The pricing restrictions are

$$
Eq^n-E(mx^n)=0,
\qquad Eq^s-E(mx^s)\geq0.
$$

An overpriced security can be consistent with equilibrium when the investor cannot short it. Underpricing of an asset one can buy is not justified by that restriction. This is why the inequality direction matters. Write the restrictions compactly as $Eq-E(mx)\in C^*$, with the convention

$$
C^*=\{z:a'z\geq0\ \text{for every }a\in C\}
=\{0\}^k\times\mathbb R_+^\ell.
$$

The sentence following source equation (5), printed p. 241, calls the constrained coordinates of this dual cone “negative.” That conflicts with equation (4), the economic interpretation, and the subsequent maximization first-order conditions. The nonnegative convention above is the consistent reconstruction of the model, not an alternative economic assumption.

Bid–ask spreads can be represented by two artificial securities: buying the original payoff at its ask price, and buying its negative at minus its bid price. Impose nonnegative positions in both. The resulting constraints encode the distinction between buying and selling; one cannot remove them and still claim to model the spread. This construction also explains why an ordinary payoff covariance matrix can be singular without making the frictional problem meaningless: opposite payoffs have different effective prices.

The baseline assumptions on pp. 241–242 are substantive. Payoffs have finite second moments and prices finite first moments. Every nonnegative feasible payoff that is positive with positive probability must have strictly positive expected price; a zero payoff cannot have negative expected price. These are no-arbitrage restrictions on the attainable cone and expected-price system. They imply existence of a nonnegative square-integrable discount factor. The analysis does not require that every admissible factor be strictly positive in every state.

The no-redundancy assumption is also stated jointly in payoffs and prices: if two feasible coefficient vectors produce the same payoff almost surely and the same expected cost, they must coincide. Without frictions this implies nonsingularity of $E(xx')$. With transaction costs, payoff duplication by itself is not the relevant redundancy criterion. These restrictions are used to obtain existence, boundedness, and identification in the finite-dimensional optimization problems.

## The specification-error distance and its finite-dimensional solution

Let $y\in L^2$ be a proposed discount factor, potentially misspecified. Let $M$ be the square-integrable factors satisfying the pricing equalities and inequalities, and $M_+=\{m\in M:m\geq0\}$. Define

$$
\delta^2=\min_{m\in M}E(y-m)^2,
\qquad
\delta_+^2=\min_{m\in M_+}E(y-m)^2.
$$

The metric is the root-mean-square correction in discount-factor units. Requiring nonnegativity shrinks the feasible set, so $\delta_+\geq\delta$. Zero distance has an exact interpretation: the proxy already belongs to the relevant admissible set. A positive distance measures misspecification relative to the selected securities and restrictions; it does not establish misspecification for every conceivable financial claim.

Although the primal optimization chooses an entire random variable, the conjugate problems choose only $n$ multipliers. Source equations (8)–(9), p. 243, give

$$
\delta^2=\max_{a\in C}\left\{Ey^2-E(y-x'a)^2-2a'Eq\right\},
$$

$$
\delta_+^2=\max_{a\in C}\left\{Ey^2-E[(y-x'a)_+^2]-2a'Eq\right\},
\qquad z_+=\max(z,0).
$$

The first is a concave quadratic program. The second is concave and continuously differentiable in its squared positive-part criterion, although its derivative is not everywhere differentiable. At optimizers $a_0$ and $a_+$, the nearest admissible factors are

$$
m_0=y-x'a_0,
\qquad m_+=(y-x'a_+)_+.
$$

Their pricing residuals lie in $C^*$ and satisfy complementary slackness:

$$
a'\{Eq-E(mx)\}=0.
$$

Thus unrestricted positions price with equality, constrained positions can have nonnegative pricing slack, and a strictly positive constrained multiplier can occur only at a binding pricing restriction. This is the appropriate numerical optimality check. A solver's successful status without verification of these relationships is weak evidence of a correct implementation.

In the frictionless, nonpositive-restricted case, put $H=E(xx')$ and $e=E(xy)-Eq$. The solution and minimized distance reduce to

$$
a_0=H^{-1}e,
\qquad \delta^2=e'H^{-1}e.
$$

This expression shows the economic weighting implicit in the distance. It is not an arbitrary efficient-GMM weighting matrix estimated from the long-run covariance of pricing errors. Replacing $H^{-1}$ with a different matrix changes the criterion and its interpretation. The underlying payoff second moment, rather than the covariance after demeaning, is required.

The nearest random variable is unique because of the squared-distance projection, but multiplier uniqueness is a separate question. In the nonnegative problem some states are clipped to zero, potentially removing information about coefficients. Assumption 1.4 imposes nonsingularity of the second-moment matrix of binding-security payoffs restricted to the states where the optimal discount factor is positive. Securities with strictly slack inequalities have zero multipliers and should not be included blindly in that identification matrix.

There is a second printed problem in equation (13), p. 245. The correct binding-asset relation, following directly from $E(x^*m_+)=Eq^*$, is

$$
Eq^*=E[x^*y\,1_{\{m_+>0\}}]
-E[x^*x^{*'}1_{\{m_+>0\}}]\,b.
$$

The printed first expectation omits $x^*$, producing a scalar where a vector is needed. The expression here explicitly restores it. Identification requires the indicated matrix to be nonsingular; merely having many observations is insufficient if the positive-factor states do not span the binding assets.

## Volatility frontiers and admissible means

Set $y=0$. The minimized distance is then the minimum second moment of a discount factor. At a specified mean $\mu$, the minimum standard deviation is

$$
\sigma_{\min}(\mu)
=\sqrt{\min E(m^2)-(\mu)^2}.
$$

The mean restriction must be imposed in the minimization. It is not legitimate to compute an unrestricted second-moment bound and subtract an arbitrary squared mean afterward. If a freely traded unit payoff is available, its expected price identifies $Em$. Otherwise augment $x$ with a constant one and augment its expected price with $\mu$; the added portfolio coordinate is unrestricted. Solve the expanded problem at each mean assignment.

Under nonnegativity, no-arbitrage also restricts feasible means. The lower and upper bounds are

$$
\lambda_0=-\inf\{a'Eq:a\in C,\ a'x\geq-1\ \text{a.s.}\},
$$

$$
\nu_0=\inf\{a'Eq:a\in C,\ a'x\geq1\ \text{a.s.}\}.
$$

If no feasible portfolio dominates the unit payoff, set $\nu_0=+\infty$. A hypothetical mean outside the admissible range cannot be reconciled with the augmented nonnegative-pricing problem. Interior means are the clean setting for finite frontier calculations; behavior at endpoints can be irregular.

These bounds have simple sample linear-programming counterparts: replace $Eq$ by the average price and impose the payoff inequality at every observed date. The upper sample bound may be finite even when its population counterpart is infinite, for example when an observed limited-liability payoff never reaches zero in a finite sample. This is not evidence that the true upper bound is finite. Proposition 2.3 proves that the estimated upper bound diverges when the population value is infinite, while finite upper and lower bounds are consistently estimated.

Pointwise frontier consistency does not automatically give a globally accurate graph near arbitrage endpoints. Convexity strengthens the result to uniform convergence on compact subsets of the admissible interior. The authors also formulate convergence of the entire feasible mean–standard-deviation region using Hausdorff distance, which allows nearby points to differ in both coordinates. For an unbounded mean range a truncated version of that distance is needed. The distinction matters when a numerical graph appears unstable vertically near a boundary although the feasible sets themselves are close.

## Sampling assumptions and uncertainty in the optimized distance

The observations $(x_t,q_t,y_t)$ form a stationary, ergodic sequence. These assumptions support laws of large numbers; they do not by themselves establish a central limit theorem. Write $E_T$ for the sample average and define the per-observation objective

$$
\phi_t(a)=y_t^2-(y_t-x_t'a)^2-2a'q_t,
$$

or, with nonnegativity,

$$
\phi_{+,t}(a)=y_t^2-(y_t-x_t'a)_+^2-2a'q_t.
$$

Maximize their averages over $C$, then take square roots to estimate the distances. Population and sample criteria are concave. Appendix A proves consistency by using local uniform convergence on compact sets together with tail behavior that keeps maximizing coefficients bounded. It does not simply assume a compact multiplier search box. Along directions exposing negative payoffs the criterion eventually declines quadratically; other feasible directions decline at least linearly through their positive expected costs.

For asymptotic normality the authors impose joint central limit conditions on the objective and the pricing-error vector, as in Assumptions 2.2–2.3. Let $\Omega_\phi$ be the long-run variance of $\phi_t(a_0)$, or its positive-part counterpart. When the population distance is strictly positive,

$$
\sqrt T(\widehat\delta-\delta)
\ \Rightarrow\ N\left(0,\frac{\Omega_\phi}{4\delta^2}\right).
$$

For the squared distance the variance is simply $\Omega_\phi$. The central result is that replacing the population optimizer by an estimated optimizer has no first-order effect on the optimized criterion. Concavity bounds the extra term by a centered sample pricing error times the multiplier estimation error. The former has a central limit scale and the latter vanishes, so their product is negligible.

One can therefore estimate uncertainty by applying a heteroskedasticity-and-autocorrelation-consistent long-run variance estimator to the scalar objective series evaluated at the estimated optimum. An ordinary sample variance is appropriate only under additional restrictions eliminating serial dependence. The paper cites spectral methods, including Newey–West and Andrews; it does not prescribe a particular kernel, bandwidth, prewhitening option, or finite-sample correction. Those choices must be reported by a reproducing researcher.

Short-sale constraints do not generally complicate this positive-distance value-function limit, even though they can complicate the coefficient limit. For the positive-part problem the theorem normally requires the additional uniqueness/rank assumption. Appendix B shows an important exception: if prices are constant, all optimal multiplier vectors produce the same objective random variable, so value-function inference can survive nonunique multipliers. Random instrument-scaled prices cannot automatically claim that exception.

At $\delta=0$, the displayed normal approximation is invalid. The denominator vanishes, the first-order objective variation degenerates, and the distance has a different limiting distribution. The paper explicitly warns of this boundary. In the elementary frictionless fixed-proxy case, the quadratic form $T\widehat\delta^2$ can be reconstructed from the central limit theorem for pricing errors as a weighted Gaussian quadratic form. It is not generically a standard chi-square unless its covariance and normalization have the required relationship. That observation is a derivation from the special case, not an additional universally stated test in this article.

## Testing moments, comparing models, and diagnosing securities

To test a proposed model's volatility restriction, suppose its discount factor $m_t$ is observed or constructed. Add a unit payoff whose random price is $m_t$, so its expected price is the model's mean. Set the proxy in the second-moment-bound calculation to zero and subtract $m_t^2$ from the per-observation criterion. For example, without positivity the criterion becomes

$$
\psi_t(a)=-(a'x_t)^2-2a'q_t-m_t^2,
$$

with the augmented $x_t,q_t$. With positivity replace $(a'x_t)^2$ by $(-a'x_t)_+^2$. The maximized population value is the minimum required second moment minus the model's second moment. The null is that this value is nonpositive. A positive value means the model is insufficiently volatile at its own mean.

The implementation uses a one-sided normal test and the conservative boundary value zero for the composite null. Sampling error in the model's mean and second moment is included through the constructed objective series. If these moments can instead be calculated numerically to effectively arbitrary accuracy, insert their fixed values rather than treating simulated draws as observed data. If they are estimated by a finite simulation, the variance must include simulation error; it cannot be obtained solely from the asset-return series. No universal simulation length or random-number design is specified here.

A parametric proxy $y(\beta)$ can be fitted by minimizing its distance over a compact parameter set. The estimator is a minimum over $\beta$ of a maximum over pricing multipliers, not a simultaneous minimization over both. At a strictly positive pseudo-true distance and under suitable identification, moment, and smoothness conditions, the optimized value again has an envelope-type central limit result. The parameters describe the closest member of a possibly misspecified family under this particular metric, rather than necessarily recovering a literal structural truth.

For two nonnested families, test equality of their minimized distances using the central limit distribution of their difference. Their estimated objective series are correlated because they use the same data. Estimating two variances separately and adding them while ignoring their covariance is therefore incorrect. The paper sketches this comparison by analogy with nonnested likelihood analysis; it does not supply a finite-sample model-selection threshold or claim that a statistically smaller distance proves economic correctness.

Multipliers identify securities responsible for tightening a bound. To test whether a subset of assets adds information, test whether its multipliers are zero. Directly comparing the full and restricted optimized bounds can produce a degenerate first-order distribution under the null. In the frictionless regular case a Wald test on selected multiplier coordinates avoids that degeneracy.

The equivalent region-subset formulation uses $n$ moment restrictions with a $k$-parameter discount factor built from a smaller payoff vector, including a constant. With a prescribed mean, an appropriately weighted GMM overidentification test has $n-k$ degrees of freedom. Estimating the mean as an additional parameter reduces the degrees of freedom by one. These counts assume the stated rank and regularity conditions; they are not a license to use ordinary chi-square inference at an inequality boundary.

## Multiplier inference and the kink

Without market frictions the sample multiplier solves

$$
E_T[x_t(y_t-x_t'\widehat a)-q_t]=0,
$$

or the positive-part version. Let $g_t=x_tm_t-q_t$ at the population optimum. For the unconstrained-sign problem define $H=E(xx')$; for the positive-part problem define

$$
H_+=E[xx'1_{\{y-x'a_+>0\}}].
$$

If the relevant matrix is nonsingular and $\Omega_g$ is the long-run covariance of $g_t$, the asymptotic covariance of $\sqrt T(\widehat a-a)$ is $H^{-1}\Omega_gH^{-1}$ or $H_+^{-1}\Omega_gH_+^{-1}$. Estimate both the matrix and the long-run covariance using the fitted factor and the same sample alignment.

The source's equation (46), printed p. 258, places a minus sign before the inverse matrix in the influence representation. Linearizing equation (42) or (43) gives $0\approx E_Tg-H(\widehat a-a)$, hence the coefficient is positive:

$$
\sqrt T(\widehat a-a)
=H^{-1}\sqrt T E_Tg+o_p(1).
$$

The sign correction leaves the displayed marginal sandwich covariance unchanged, but matters for influence functions and joint cross-covariances. This note uses the algebraically consistent representation and flags the source discrepancy explicitly.

For the positive-part moment equation, Assumption 4.1 excludes probability mass exactly at $y-x'a_+=0$. Without it the derivative can fail to be well behaved. Appendix C bounds the local differentiation error by an integrable multiple of $|x|^2$ and shows that its modulus tends to zero almost surely away from the kink. This supplies stochastic differentiability despite the nonsmooth primitive function. It does not justify differentiating through an atom at the threshold.

If $y$ depends on estimated $\beta$, stack the pricing equations with

$$
E\left[\frac{\partial y(\beta)}{\partial\beta}
\{y(\beta)-(y(\beta)-x'a)_+\}\right]=0.
$$

A joint Jacobian and long-run covariance yield the parameter covariance. Treating fitted $\beta$ as fixed when reporting multiplier or structural-parameter errors discards a genuine first-order channel, even though it disappears from the regular optimized-value limit.

With short-sale constraints, strictly slack pricing coordinates have multiplier estimates equal to zero with probability approaching one. For the remaining binding coordinates, an interior multiplier can have a normal limit. A multiplier on the cone boundary instead has a projected-Gaussian type limit. The paper only sketches that distributional extension; it does not deliver a universal plug-in chi-square procedure for all frictional subset tests. Estimated solvency cones are also outside the main fixed-cone results because their own approximation error must be accounted for.

## A reproducible implementation and its limits

A reconstruction should first declare the holding period, quote convention, payoff units, instruments, and trade-time information. Then construct $x_t,q_t$, the cone, and the proxy using a common sample. A return normalized to price one is admissible, but combining normalized returns with unnormalized prices is not. Bid and ask series require the artificial-security expansion. Remove genuine payoff-and-price redundancies before attempting to invert moment matrices.

Next check finite sample feasibility and solve the unconstrained-sign and nonnegative versions separately. Record objective values, multiplier vectors, pricing residuals, complementary-slackness errors, positive-state frequencies, and matrix condition numbers. For a volatility frontier, augment the unit payoff for every requested mean and solve the sample arbitrage-bound linear programs first. Never replace infeasibility by a plotted zero volatility.

Finally choose inference for the question actually asked: a positive misspecification distance, a volatility-moment inequality, a nonnested model comparison, or an asset-subset test. Use a serial-dependence estimator appropriate to the observation process and record its tuning. Inspect whether the distance is near zero, whether a multiplier is at a boundary, and whether clipping leaves a nearly singular identification matrix. These diagnostics distinguish numerical failure from a failure of the regular asymptotic approximation.

The source supplies no asset universe, sample dates, cost estimates, calibration constants, optimizer tolerance, bandwidth, or simulation seed to copy. Its empirical content consists of implementable estimands and statistical results, not an undisclosed backtest. A faithful application must supply those missing choices openly. Its practical contribution is to make economic discrepancy measurable and uncertainty interpretable without pretending that market frictions, model misspecification, and sampling error are the same phenomenon.
