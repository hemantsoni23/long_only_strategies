# Elementary proof that mean–variance implies quadratic utility

D. J. Johnstone and D. V. Lindley, *Theory and Decision* 70, 149–155 (2011); published online 10 February 2010. DOI: 10.1007/s11238-010-9194-7.

Source: [MeanVariance_JohnstoneLindley_2010.pdf](../../Finance/MeanVariance_JohnstoneLindley_2010.pdf). The library also contains a PDF named `MeanVariance_JohnstoneLindley_2011.pdf` of this same published article. The 2010 filename records the online-publication year; it does not identify a separate theoretical result. Page references below use the printed journal pages.

## Why this matters

This short theoretical paper identifies what is being assumed when expected utility is asserted to depend exactly on only the mean and variance of a payoff, without restricting the family of payoff distributions. Quadratic utility is sufficient for that reduction, but the paper's contribution is an elementary argument that it is also necessary. The distinction matters when a portfolio optimizer is advertised as implementing expected-utility preferences. One must say whether the justification comes from the utility function, a restricted distributional family, or an approximation. These are different claims with different domains of validity.

The result does not show that every useful application of mean–variance optimization requires an investor who literally has quadratic utility. It concerns an exact representation of expected utility over an unrestricted class of lotteries with the relevant moments. Restricting feasible returns, for example to a common location-scale family, changes the problem. Approximation can also be useful without being exact. The authors' proof supplies a diagnostic for a foundational claim, rather than a new allocation algorithm or a test of investment performance.

For a quantitative researcher, the useful deliverable is a reproducible sequence of algebraic tests: construct two-outcome lotteries with the same mean and variance; demand that their expected utilities agree as their probabilities vary; differentiate the resulting identity; and solve the induced differential equation for utility. The proof is compact enough to implement symbolically. It also clarifies why randomizing between investments is different from holding a diversified combination of them.

## Proposition, objects, and scope

Let $X$ denote the payoff or final wealth to which a von Neumann–Morgenstern utility function $U$ is applied. Let $\mu=E[X]$ and $\sigma^2=\operatorname{Var}(X)$. The hypothesis is that there is a function $g$ such that

$$
E[U(X)]=g(\sigma,\mu)
$$

for every admissible payoff distribution. In particular, two distributions with the same first two moments must produce the same expected utility. The argument uses differentiability of $U$ and a sufficiently rich domain of two-point lotteries. It is stronger than requiring that one finite collection of traded portfolios happen to receive the same ranking under two criteria.

The conclusion is

$$
U(x)=A+Bx+Cx^2.
$$

Here quadratic includes the linear and constant special cases $C=0$. For economically nontrivial increasing preferences, constant utility is excluded, but it remains an algebraic solution. Utility is a cardinal expected-utility representation only up to a positive affine transformation. The constants in a particular expression therefore require normalization before they can be interpreted or compared across agents.

Sufficiency is immediate:

$$
E[U(X)]=A+B\mu+C(\mu^2+\sigma^2).
$$

Necessity is the main result, proved on pp. 153–154. It says that dependence on the full distribution cannot disappear for arbitrary lotteries merely because a decision maker chooses to report two moments. If utility is nonquadratic, there are distributions with identical moments that it distinguishes, subject to the domain and regularity conditions under consideration.

An important restriction is hidden in the word arbitrary. The proof varies both outcome levels and their probabilities while preserving mean and variance. A market offering only a fixed finite number of distributions need not permit these variations. Similarly, the theorem is not a claim that any two-parameter family must satisfy mean–variance sufficiency. Its hypothesis is about expected utility across a rich distributional domain, not about the number of parameters a statistician puts into a fitted model.

## Reconstructing the two-point proof

Take a lottery that pays $a$ with probability $p$ and $b$ with probability $1-p$, where $0<p<1$. Its moments are

$$
\mu=pa+(1-p)b,\qquad
\sigma^2=p(1-p)(a-b)^2.
$$

Introduce a positive parameter

$$
z=\sqrt{\frac{p}{1-p}},\qquad
p=\frac{z^2}{1+z^2}.
$$

For a prescribed $\mu$ and $\sigma>0$, choose

$$
a=\mu-\frac{\sigma}{z},\qquad
b=\mu+\sigma z.
$$

Direct substitution verifies both moments. As $z$ changes, the lower and upper outcomes and their probabilities change, but the mean and standard deviation do not. This is the precise experimental variation in the proof. It is not a change in risk aversion or an optimization over portfolio weights.

Moment sufficiency requires

$$
\frac{z^2U(\mu-\sigma/z)+U(\mu+\sigma z)}{1+z^2}
=g(\sigma,\mu)
$$

for every $z>0$ for which the outcomes are admissible. The right-hand side is constant with respect to $z$. Differentiate the left-hand side and clear the common denominator to obtain

$$
\frac{2z}{1+z^2}\left[U\left(\mu-\frac{\sigma}{z}\right)-U(\mu+\sigma z)\right]
+\sigma\left[U'\left(\mu-\frac{\sigma}{z}\right)+U'(\mu+\sigma z)\right]=0.
$$

The derivatives of the outcome locations are $\sigma/z^2$ and $\sigma$, respectively. Keeping those terms is essential: changing $z$ changes more than the probability weight. Treating outcomes as fixed while differentiating would prove a different and incorrect statement.

Set $z=1$. The lottery now has equal probabilities and outcomes $\mu-\sigma$ and $\mu+\sigma$. For $\mu>0$, set $\sigma=\mu$, so that one outcome is zero and the other is $2\mu$. The identity reduces to

$$
U(0)-U(2\mu)+\mu\left[U'(0)+U'(2\mu)\right]=0.
$$

For negative $\mu$, use $\sigma=-\mu$ and rearrange; the same relationship results. With $x=2\mu$ this becomes

$$
\frac{x}{2}U'(x)-U(x)=-\frac{x}{2}U'(0)-U(0).
$$

This first-order differential equation is the central reduction. All distributional complexity has been converted into a restriction on a scalar function of wealth. For $x\ne0$, divide and use the integrating factor $x^{-2}$:

$$
\frac{d}{dx}\left[x^{-2}U(x)\right]
=-x^{-2}U'(0)-2x^{-3}U(0).
$$

Integration gives

$$
U(x)=U(0)+xU'(0)+Cx^2.
$$

Thus the only possible shape is quadratic. Substitution into the original two-point equation verifies that it is independent of $z$, and substitution into general expected utility establishes sufficiency whenever the relevant moments exist.

### A detail needed for a complete reconstruction

The differential equation is solved away from zero. On a domain containing both positive and negative wealth, integration by itself initially permits separate constants $C_+$ and $C_-$ on the two half-lines. Mere differentiability at zero does not force those curvatures to be identical. The original, stronger two-point identity supplies the missing restriction. This paragraph makes explicit a completion of the proof; it is not a separate result claimed by the authors.

Set $\mu=0$ and retain arbitrary $\sigma>0$. For the piecewise quadratic expression, expected utility is

$$
U(0)+\sigma^2\frac{C_-+C_+z^2}{1+z^2}.
$$

Its independence of $z$ implies $C_-=C_+$. The linear terms cancel because the lottery has mean zero. Consequently the original hypothesis yields one quadratic utility function across the entire domain. A reconstruction confined to a positive wealth interval can instead center the algebra at a suitable interior reference wealth; it must still ensure that all lotteries used remain inside that interval.

This also explains why checking only the equal-probability case is insufficient. The $z=1$ specialization obtains a useful differential restriction, but the original condition holds for the whole family. A faithful proof preserves that stronger condition when checking the solution, including its behavior across a reference point.

## Probability mixtures and the older argument

The paper revisits the reasoning associated with Markowitz, Mossin, and Baron on pp. 150–152. Its organizing idea is what the authors call Buridan's axiom: if an investor is indifferent between two lotteries, then the investor is indifferent between either lottery and a randomized selection between them. Under expected utility this follows from linearity in probabilities.

Let investment $A$ pay a constant $\mu_0$, and let investment $B$ have mean $\mu_1$ and variance $\sigma_1^2$. A probability mixture chooses all of $A$ with probability $\alpha$ and all of $B$ otherwise. The resulting moments are

$$
\mu=\alpha\mu_0+(1-\alpha)\mu_1,
$$

$$
\sigma^2=(1-\alpha)\sigma_1^2+
\alpha(1-\alpha)(\mu_1-\mu_0)^2.
$$

The second term is the variance of the conditional mean. It is not optional. Omitting it treats uncertainty about which investment is selected as if it did not exist.

If $\Delta=\mu_1-\mu_0\ne0$, define

$$
\rho=\frac12\left(\frac{\sigma_1^2}{\Delta}+\Delta\right).
$$

Eliminating $\alpha$ yields

$$
\sigma^2+\left[\mu-(\mu_0+\rho)\right]^2=\rho^2.
$$

Thus randomized mixtures trace an arc of a circle in the standard-deviation–mean plane. They do not generally trace the line segment joining the two original moment pairs. Only the feasible arc corresponding to $0\le\alpha\le1$ is generated. If $\Delta=0$, the division defining $\rho$ is unavailable and the original moment equations should be used directly.

If $A$ and $B$ are indifferent, expected utility makes their probability mixtures indifferent as well. The circle is then part of an indifference locus. Expanding the circle with $k=\mu_0+\rho$ gives

$$
\sigma^2+\mu^2-2k\mu+k^2-\rho^2=0.
$$

When $k\ne0$, it can be represented as a level set of

$$
\mu-c(\sigma^2+\mu^2),\qquad c=\frac{1}{2k}.
$$

The coefficient printed next to equation (4) on p. 152 does not agree with this expansion: the displayed circle requires the reciprocal expression above. This note uses the algebraically reconstructed coefficient. For $k=0$, do not divide by $k$; the circle instead has a constant second moment. These details affect the background geometry, not the later two-point proof's conclusion.

A probability mixture is also different from a portfolio holding $\alpha$ of one asset and $1-\alpha$ of another simultaneously. The latter payoff is a weighted sum, whose variance depends on covariance and on squared weights. The mixture selects one whole payoff distribution. It has the between-means variance term above and does not require a joint return realization for the unselected asset. Confusing the two operations can make an apparent criticism of mean–variance theory rest on the wrong feasible set.

The authors' preferred proof avoids relying on the geometry to establish necessity. It starts directly from the assertion that expected utility is a function only of the two moments. Its value is this directness: a researcher can inspect exactly which family of lotteries and which regularity condition force the conclusion.

## Economic interpretation and limits

For quadratic utility, risk aversion corresponds to $C<0$, since $U''(x)=2C$. Increasing utility additionally requires $B+2Cx>0$ on the relevant wealth range. A concave quadratic therefore has a finite satiation point and eventually assigns lower utility to greater wealth. An everywhere increasing, globally defined quadratic on the whole real line cannot also be strictly concave. This is a substantive limitation of the exact unrestricted-distribution justification, not a numerical instability that a better optimizer removes.

There are several ways a practical model can avoid imposing that global preference shape, but each changes the claim. A restricted wealth domain can remain below the satiation point. A restricted distributional family can make first and second moments sufficient without forcing utility to be quadratic. A local Taylor approximation can discard higher-order terms when they are small. The paper addresses exact necessity in the unrestricted setting; it does not estimate how accurate a local approximation is in actual security data.

Nor should expected quadratic utility be silently identified with a fixed mean-minus-variance score. Normalizing $A=0$, $B=1$, and $C=-c$ gives

$$
E[U(X)]=\mu-c\mu^2-c\sigma^2.
$$

The $\mu^2$ term is part of the exact expression. Replacing it by $\mu-\lambda\sigma^2$ with fixed $\lambda$ changes the preference representation. The latter objective can have another justification, such as a certainty equivalent under particular utility and distributional assumptions, but that justification must be stated independently. Along a fixed-mean comparison the difference may disappear; over an entire efficient frontier it generally does not.

The theorem is also not a statement about an empirical risk premium, optimal leverage, the accuracy of estimated covariances, or an asset-pricing regression. It contains no sample of securities, trading dates, portfolio rebalancing rule, transaction costs, or out-of-sample evaluation. Adding those elements would create a new application beyond the paper. Its practical contribution is to make the logical foundation of such an application explicit before those implementation choices are made.

## Reproduction checks

A symbolic reproduction needs only differentiation, substitution, and verification of an identity. First verify that the parameterized two-outcome family has the claimed moments. Then differentiate its expected utility with respect to $z$, specialize to equal probabilities, solve the differential equation, and substitute the solution back into the unspecialized expression. If the domain crosses zero, include the common-curvature check. Finally verify the general expectation formula using $E[X^2]=\mu^2+\sigma^2$.

A small numerical diagnostic can supplement the symbolic derivation. The following is an independently constructed illustration, not a numerical result reported in the article. Set $\mu=1$ and $\sigma=1$. At $z=1$, the lottery pays 0 or 2 with probabilities one half each. At $z=2$, it pays 0.5 with probability 0.8 and 3 with probability 0.2. Both have mean 1 and variance 1. Their second moments are both 2. Hence their expected quadratic utilities are both $A+B+2C$, regardless of the chosen quadratic coefficients.

For cubic utility $U(x)=x^3$, expected utilities differ: the first lottery gives 4, while the second gives 5.5. This is a direct witness that equal first and second moments need not determine expected utility for a nonquadratic function. It does not establish the general theorem by itself; the general result comes from requiring equality across the whole two-point family and solving the resulting functional restriction.

A researcher can also test the mixture geometry numerically using the law of total variance. Use the original mixture equations to calculate a sequence of points and check the circle residual. This guards against two distinct errors: replacing a probability mixture by a weighted portfolio, and using the incorrectly transcribed coefficient in a rearranged circle equation. No stochastic simulation or fitted parameters are needed for either check.

## Takeaways

The novel component is the necessity proof, not the familiar fact that a quadratic expectation uses only two moments. The proof works because it changes distributional shape while holding those moments fixed. It needs a rich lottery domain and differentiability; it cannot be transferred automatically to a restricted collection of feasible portfolios.

For implementation, preserve the precise objective being represented. Exact expected quadratic utility includes the squared mean. Respect the wealth domain on which the utility is increasing. Distinguish probability mixtures from simultaneous holdings. When a model instead invokes normality, a common location-scale family, or a Taylor expansion, describe that alternative justification explicitly and assess its own limitations.

The paper provides a rigorous conceptual check on mean–variance claims, rather than evidence that a particular allocation process will succeed or fail. Its strongest practical use is at the specification stage: it tells the reproducing researcher which assumptions must be visible before an expected-utility interpretation can be accepted.
