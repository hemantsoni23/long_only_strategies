# Mean–Variance and Expected Utility: The Borch Paradox

David Johnstone and Dennis Lindley, Statistical Science 28(2), 2013, pp. 223–237. DOI 10.1214/12-STS408. Source: [MarkowitzBorchParadox_JohnstoneLindley_2013.pdf](../../Finance/MarkowitzBorchParadox_JohnstoneLindley_2013.pdf), sixteen-page electronic reprint, arXiv:1306.2728v1, June 12, 2013. PDF pagination differs from the journal pagination; pointers below refer to the PDF and numbered sections.

## Why this matters and the contribution

The paper revisits Borch's claim that rational mean–variance indifference curves cannot exist. It explains why this claim is too broad, while preserving the important warning that mean and variance cannot represent every rational preference over every possible return distribution. Its contributions are a reconstruction of Borch's counterexample, an account of Baron's rebuttal, and an axiomatic argument based on probability mixtures that reveals where unrestricted two-moment rankings break down.

The practical relevance is about the domain of a decision model. Exact mean–variance sufficiency under restricted utility or distribution classes is different from approximate usefulness for ordinary portfolios. A model can be useful without claiming universal preference representation. Conversely, visually plausible risk–return indifference curves need not correspond to any coherent expected-utility function on the proposed domain.

This source is mathematical and historical. It supplies no original market dataset, fitted portfolio, return forecast, or experimental performance table. Reproduction means reconstructing examples and logical arguments, not inventing a backtest.

## Expected utility and the two-moment reduction

An investment is a probability distribution over payoffs $X$. Expected-utility theory ranks it by $E[u(X)]$, derived from preference axioms including completeness, transitivity, continuity, and independence under probability mixing. Increasing utility represents preference for more money; concavity represents risk aversion. Expected utility by itself does not impose increasing utility, a distinction relevant to quadratic satiation.

Mean–variance analysis instead reduces each opportunity to $(\sigma,\mu)$, with $\mu=E[X]$ and $\sigma^2=\operatorname{Var}(X)$. Investors typically prefer a higher mean at fixed standard deviation and lower standard deviation at fixed mean. The efficient frontier removes opportunities dominated in this two-coordinate sense. Choosing among remaining points requires a preference representation as well as a feasible set.

A common careless step is to assume that any smooth convex set of drawn curves supplies a valid expected-utility representation. The paper shows why the underlying payoff distributions, permissible utility functions, and allowed operations on investments determine whether that is possible. The two-moment compression is not logically free.

## Borch's construction and its correct interpretation

Suppose an investor says two distinct moment pairs $(\mu_1,\sigma_1^2)$ and $(\mu_2,\sigma_2^2)$ are indifferent solely by virtue of their moments. Construct binary lotteries sharing a payoff $x$ with probability $1-p$ but paying $y_1$ and $y_2$ respectively with probability $p$. If $y_2>y_1$ and $p>0$, any increasing utility strictly favors the second lottery: one outcome improves and no outcome worsens.

For nondegenerate parameter differences, equations (1)–(4) give one construction:

$
x=\frac{\sigma_1\mu_2-\sigma_2\mu_1}{\sigma_1-\sigma_2},\qquad
p=\frac{(\mu_1-\mu_2)^2}{(\mu_1-\mu_2)^2+(\sigma_1-\sigma_2)^2},
$

$
y_i=\mu_i+\sigma_i\frac{\sigma_1-\sigma_2}{\mu_1-\mu_2},\qquad i=1,2.
$

For each lottery, substitution into $\mu_i=py_i+(1-p)x$ and $\sigma_i^2=p(1-p)(y_i-x)^2$ verifies the desired moments. The displayed formula assumes the denominators are nonzero; boundary cases require separate treatment rather than division by zero. If one nevertheless requires indifference between the constructed lotteries, increasing utility requires $y_1=y_2$, contradicting distinct moment pairs in the intended construction.

The paper's numerical example is especially transparent. Lottery A pays 25 or -5 with equal probability, giving mean 10 and variance 225. Lottery B pays 45 or -5 with equal probability, giving mean 20 and variance 625. B has both higher mean and higher variance, but it also dominates A outcome by outcome. A preference for higher variance compensation does not justify indifference between these particular lotteries.

The correct conclusion is not that no distributions with those moment pairs could ever be indifferent. It is that an investor cannot be indifferent between every imaginable pair of distributions having those moments while also consistently preferring more to less. Some distribution pairs on a chosen domain can have equal expected utility; arbitrary replacement by a different distribution with the same moments is the invalid universal step.

The source also prints an alternative construction using sums of standard deviations. Its two displayed upper-outcome signs do not generally reproduce both specified means. For the numerical values above, the common point is 13.75 and probability $1/17$; the printed second outcome would give the wrong second mean. This note relies on the verified original branch and the explicit numerical example, not that unverified alternative formula. The issue is in the PDF equation, not merely extraction.

## Baron's rebuttal: quadratic utility and support restrictions

On an unrestricted class of distributions, exact dependence of expected utility on only the first two moments implies a quadratic utility form under the conditions discussed in the paper. Write an increasing-region, concave quadratic as

$
u(x)=2ax-x^2,\qquad
E[u(X)]=2a\mu-(\mu^2+\sigma^2)=a^2-(\mu-a)^2-\sigma^2.
$

Its mean–standard-deviation indifference curves are circles centered at $(0,a)$. Such curves exist algebraically. The problem is that $u'(x)=2(a-x)$ becomes negative above $a$. A higher payoff can then reduce utility. That is a limitation of the underlying quadratic preference when applied outside its increasing region, not an arithmetic inconsistency unique to a mean–variance restatement.

Baron's defense restricts the admissible payoff support to $X\leq a$ before reducing distributions to moments. Merely imposing $E[X]<a$ is insufficient: a distribution can have a mean below $a$ and still assign positive probability to a payoff above it. Figure 3 illustrates this with equally likely payoff pairs. Parts of an apparent indifference contour outside the lower-left region can rank a pair with both outcomes higher as equally good, violating preference for money.

The condition must therefore constrain all possible outcomes, not just a portfolio's mean. If the economic problem genuinely permits very high payoffs, excluding them solely to protect quadratic utility is an economically consequential restriction. The paper does not present it as a universally plausible assumption about all investments.

## The probability-mixture argument

The authors formulate a continuity–monotonicity–finiteness requirement for a merit function $g(\sigma,\mu)$ defined over the whole half-plane $\sigma\geq0$. It is continuous, strictly increasing in mean, strictly decreasing in risk, and permits any finite increase in risk to be compensated by a sufficiently large finite increase in mean. They combine this with Buridan's axiom: if two lotteries are indifferent, randomizing between them must also be indifferent. This follows from the expected-utility independence axiom.

A probability mixture chooses one entire lottery at random. It is different from dividing wealth between two assets. If lottery 0 is selected with probability $\alpha$ and lottery 1 otherwise, then

$
\mu_\alpha=\alpha\mu_0+(1-\alpha)\mu_1,
$

$
\sigma_\alpha^2=\alpha\sigma_0^2+(1-\alpha)\sigma_1^2+
\alpha(1-\alpha)(\mu_1-\mu_0)^2.
$

The final term is variance caused by which lottery is chosen. There is no covariance term between jointly held asset payoffs because the operation is selection, not simultaneous portfolio holding. The formula follows from conditional expectation and the law of total variance and does not require independent underlying asset payoffs.

Begin with a risk-free point $A=(0,\mu_0)$ and a risky point $C=(\sigma_1,\mu_1)$ indifferent to it. Finiteness and continuity supply such a compensation point with $\mu_1>\mu_0$. Eliminating $\alpha$ from the mixture moments gives equation (7):

$
\sigma^2+[\mu-(\mu_0+\rho_0)]^2=\rho_0^2,\qquad
\rho_0=\frac12\left[\frac{\sigma_1^2}{\mu_1-\mu_0}+(\mu_1-\mu_0)\right].
$

Buridan forces indifference along the connecting circular arc. Negative standard deviations are inadmissible, and the upper quarter of the right semicircle would have both a higher mean and less risk than its endpoint, so monotonicity rejects it as an indifference arc.

The proof then extends the admissible lower quarter-circle by considering additional vertical lines at fixed risk. Any alternative compensation point would induce another circle intersecting the original and create two indifferent points at the same standard deviation but different means. That contradicts strict monotonicity in mean. Beyond the circle's maximal standard deviation, globally extending the compensation requirement creates further contradictory rankings, illustrated by the rectangle in Figure 2.

The conclusion is that the stated axioms cannot support an unrestricted global ranking by only mean and standard deviation. One must restrict the domain or weaken a premise. The circle is not a universal risk-preference curve for every investor, and the contradiction is not evidence that every finite mean–variance optimization problem is irrational. The proof's force comes from the whole-half-plane and mixture-closure requirements.

## Normal distributions and why the restriction helps

If all admissible distributions belong to a fixed location–scale family, their means and variances can identify the entire family member. Expected utility may then be expressed as a function of those moments for many utilities. For normally distributed payoffs and constant-absolute-risk-aversion utility $u(x)=1-\exp(-\kappa x)$,

$
E[u(X)]=1-\exp[-\kappa\mu+\kappa^2\sigma^2/2],\qquad \kappa>0.
$

Indifference is equivalent to $\mu-\kappa\sigma^2/2$ constant: straight lines in the variance–mean plane and parabolas in the standard-deviation–mean plane. This does not contradict the mixture-circle argument, because the domain assumptions differ. A probability mixture of normals is generally not normal. Applying the normal expected-utility formula to the mixture's first two moments would be invalid.

The Chipman–Baron defense exploits divisible assets. A conventional portfolio payoff $\alpha X+(1-\alpha)Y$ has, by concavity,

$
u(\alpha X+(1-\alpha)Y)\geq\alpha u(X)+(1-\alpha)u(Y).
$

Taking expectations shows that the weighted portfolio is at least as desirable as random selection between the two assets for a risk-averse investor, when both constructions are feasible on the relevant joint payoff space. Strict preference needs nondegeneracy in addition to strict concavity; equality can occur for identical payoffs. The paper sometimes states the comparison strictly, so this qualification matters.

Joint normality is preserved by linear portfolios. Under divisibility and the relevant concavity assumptions, one can focus on those portfolios rather than the inferior probability mixtures. This is a domain-based reconciliation, not a proof that individual real-world stocks are normal. Latent legal, regulatory, and business regimes can themselves create mixture distributions even without an explicitly purchased randomized asset.

The source further notes that arbitrary attractive-looking indifference curves under normality need not come from an underlying utility. Under appropriate growth and integrability conditions, the expected-utility surface obeys the heat-equation relation

$
\frac{1}{\sigma}\frac{\partial V}{\partial\sigma}
=\frac{\partial^2 V}{\partial\mu^2}.
$

This constrains the surface rather than granting free choice of any convex curves. Normal-distribution utility integrals also require convergence; a growth bound must be considered relative to the variance range on which the expectation is evaluated.

## Stochastic dominance and a source qualification

First-order stochastic dominance of A over B is expressed by $F_A(x)\leq F_B(x)$ for all thresholds, with strict inequality somewhere for strict dominance. It implies preference for A for all increasing utilities under the necessary integrability conditions. Second-order dominance for increasing concave utilities is expressed by

$
\int_{-\infty}^{z}[F_B(x)-F_A(x)]\,dx\geq0\quad\text{for every }z.
$

Borch's binary example has first-order dominance, so eliminating dominated opportunities before an approximate mean–variance selection avoids that particular counterexample. This screening does not turn every remaining distribution into a two-moment object or rank every incomparable pair.

Section 8's assertion that second-order dominance necessarily entails a smaller standard deviation is not correct for arbitrary unequal-mean distributions. A simple independent check is A paying one or three equally, versus B paying zero for certain. A first-order, hence second-order, dominates B, but has standard deviation one versus zero. A mean-preserving comparison supports stronger dispersion conclusions; the unrestricted assertion should not be imported into a screening algorithm. The reliable criterion is the distributional/integrated-CDF condition, not a blanket variance inequality.

More generally, moment summaries can suggest dominance but do not replace checking distributions over a stated domain. A restriction that exactly characterizes normal distributions can make moment comparisons decisive within that family; that is a different claim from sufficiency over all distributions sharing a few moments.

## CAPM derivation and interpretation

The final substantive section shows how the mean–variance representation makes portfolio-level risk contributions visible. An investor holds a market risky portfolio with weight $w_M$ and a risk-free position. A small purchase $\delta$ of asset $j$, financed from the risk-free asset, changes expected return by $\delta(\mu_j-r_f)$ and variance, to first order, by $2w_M\delta\operatorname{Cov}(r_j,r_M)$. Adding to the market instead changes mean by $\delta(\mu_M-r_f)$ and variance by $2w_M\delta\operatorname{Var}(r_M)$.

At an appropriate interior optimum, equality of marginal mean–risk tradeoffs gives

$
\mu_j=r_f+\frac{\operatorname{Cov}(r_j,r_M)}{\operatorname{Var}(r_M)}(\mu_M-r_f).
$

The conceptual insight is that an asset's covariance contribution to the held portfolio matters, rather than standalone variance alone. A hedge asset can be valuable despite a low expected return. The paper also rewrites the equation in payoff-price form and discusses common beliefs and preferences behind equilibrium interpretation.

Although the prose invokes a no-arbitrage intuition, the CAPM relationship requires the relevant portfolio-optimality and equilibrium assumptions. No arbitrage alone does not imply that every asset's expected return is linear in market beta. The introductory suggestion that each asset must exceed the risk-free expected return is likewise not general for hedge assets; the later discussion itself recognizes exceptions. The derivation should be read as conditional mean–variance equilibrium logic rather than an assumption-free pricing theorem.

## What to reconstruct and the limits of the result

The core reproducible objects are the two verified binary lotteries, quadratic utility's increasing-support restriction, total-variance formula for a randomized mixture, its circular moment locus, normal/CARA expectation, and the distinction between probability mixing and linear diversification. Each can be checked algebraically without market data. The heat-equation condition and global contradiction additionally require their stated domain and regularity assumptions.

The paper's historical review does not supply a finite error tolerance under which a practical mean–variance portfolio approximates an arbitrary expected-utility optimum. It concerns foundations and exact representation; that question is related to, but distinct from, empirical approximation studies. Its strongest takeaway is to state what distributions and choices are admitted before reducing them to two moments. That preserves the insight of mean–variance portfolio analysis without claiming an unrestricted preference theory that Borch's examples and the mixture argument rule out.
