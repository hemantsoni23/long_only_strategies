# On the Impossibility of Informationally Efficient Markets

**Sanford J. Grossman and Joseph E. Stiglitz (1980).** *American Economic Review* 70(3), June, 393–408. Source: [EfficientMarketHypothesis_GrossmanStiglitz_1980.pdf](../../Finance/EfficientMarketHypothesis_GrossmanStiglitz_1980.pdf). All sixteen scanned pages were read visually, including Figure 1, both appendices, technical footnotes, and references. This note uses printed page numbers. The article provides an analytical equilibrium and comparative statics, not an empirical sample, calibrated backtest, or experimental estimate.

## Why this matters and the contribution

If prices reveal all valuable information, a trader can infer it without paying for research. But if nobody researches, the information needed to support those revealing prices is absent. Grossman and Stiglitz make this incentive conflict precise and construct a model in which costly research and only partial revelation coexist.

The innovative component is the joint solution of two markets. For a fixed fraction of informed traders, the asset price must clear supply and demand while conveying information consistent with traders' beliefs. The informed fraction must then adjust until the benefit of learning the private signal equals its cost, or until a boundary with nobody or everybody informed is reached. Supply noise prevents the price from revealing the signal perfectly and thereby supports a private return to information.

The result does not say that prices are arbitrary or that profitable information is free to exploit. It says that equilibrium information production generally requires a residual informational advantage. In the interior solution, that advantage exactly compensates the research cost in expected utility. The price is informative and the asset market clears even though the price does not reveal everything informed traders know.

The model also produces a less obvious result: greater supply noise can attract additional informed traders until equilibrium price informativeness returns to its previous level. This offset holds under specific interior-equilibrium assumptions. Holding the informed fraction fixed gives the opposite immediate effect, so the two comparative statics must be distinguished.

## Primitives, timing, and units

There is a safe asset with date-zero price one and terminal gross payoff $R$. One share of the risky asset costs $P$ and pays

$$
u=\theta+\epsilon.
$$

The predictable component $\theta$ can be observed by paying an information cost. Residual payoff noise $\epsilon$ cannot be observed before investment. The model's tractable case assumes $\theta$, $\epsilon$, and risky-asset supply per capita $x$ are mutually independent normal random variables, with

$$
\mathbb E\theta=\bar\theta,\quad
\mathbb E\epsilon=0,\quad
\mathbb Ex=\bar x,
$$

and positive variances $\sigma_\theta^2,\sigma_\epsilon^2,\sigma_x^2$. Degenerate limits are analyzed separately. Normality permits negative payoffs, prices, and supply realizations; the model does not impose limited-liability equity constraints.

All investors initially have the same utility form $V(W)=-e^{-aW}$ with $a>0$. Their initial wealth depends on safe and risky endowments and the current price. They choose risky holdings without leverage, borrowing, or short-sale constraints. CARA-normal demand is independent of initial wealth, but the information-acquisition utility comparison still requires care because endowment values can be random.

The informed share is $\lambda\in[0,1]$. Informed traders observe $(\theta,P)$; uninformed traders observe $P$ and know the correct price rule and joint distribution. They do not directly observe $x$. Research is chosen before the private signal realization is known. Individual traders take prices and the informational price rule as unaffected by their own decision to acquire information.

For a given $\lambda$, the price is a function $P_\lambda(\theta,x)$. A rational-expectations equilibrium requires that the inference from this function be the same inference used in demands that generate it. The model does not provide a finite-sample learning algorithm or prove convergence from initially misspecified beliefs.

### Information-cost normalization

There is a printed normalization inconsistency worth resolving before implementation. Equation (12a) writes informed terminal wealth as $R(W_0-c)+(u-RP)X_I$, so $c$ is a date-zero cost and its terminal equivalent is $Rc$. But equations (13)–(14) and Appendix (A20) use $e^{ac}$ in the expected-utility ratio, rather than $e^{aRc}$.

To avoid silently mixing conventions, let $\kappa$ denote the terminal-equivalent cost. All acquisition formulas below use $e^{a\kappa}$. Setting $R=1$ and $\kappa=c$ reproduces the source's displayed formulas exactly. For a date-zero cost $c_0$ and general $R$, use $\kappa=Rc_0$. The price and demand formulas retain the stated $R$. This correction is simply the exponential-utility consequence of the budget equation, not a new behavioral assumption.

## Demands and clearing for a fixed informed fraction

An investor with conditional payoff mean $\mu_I$ and variance $v_I$ maximizes a conditional certainty equivalent

$$
RW_0+X(\mu_I-RP)-\frac a2X^2v_I.
$$

The optimal holding is $(\mu_I-RP)/(av_I)$. Thus informed demand is equation (8),

$$
X_I(P,\theta)=\frac{\theta-RP}{a\sigma_\epsilon^2},
$$

because knowing $\theta$ leaves only residual variance $\sigma_\epsilon^2$. Uninformed demand is

$$
X_U(P)=\frac{\mathbb E[u\mid P]-RP}{a\operatorname{Var}(u\mid P)}.
$$

For every state $(\theta,x)$, market clearing requires

$$
\lambda X_I(P_\lambda,\theta)
+(1-\lambda)X_U(P_\lambda)=x.
$$

This equation cannot be solved by inserting unconditional moments into uninformed demand: doing so would discard the information in prices. The endogenous conditional moments are the central feature of the model.

For $\lambda>0$, define the signal encoded in price,

$$
w_\lambda=\theta-k_\lambda(x-\bar x),
\qquad k_\lambda=\frac{a\sigma_\epsilon^2}{\lambda}.
$$

Theorem 1 shows that an equilibrium price is affine and strictly increasing in $w_\lambda$. Hence observing the price is informationally equivalent to observing this noisy signal. The source proves existence of this equilibrium; it does not classify every conceivable nonlinear equilibrium price rule.

Write $V_w=\sigma_\theta^2+k_\lambda^2\sigma_x^2$. Gaussian conditioning gives

$$
\mu_U(w)=\mathbb E[u\mid w]
=\bar\theta+\frac{\sigma_\theta^2}{V_w}(w-\bar\theta),
$$

$$
v_U=\operatorname{Var}(u\mid w)
=\sigma_\epsilon^2+\sigma_\theta^2
-\frac{\sigma_\theta^4}{V_w}.
$$

The last numerator is the square of the variance $\sigma_\theta^2$. Losing that square would change both dimensions and the information value.

An implementable version of Appendix (A10) is

$$
P_\lambda(\theta,x)=
\frac{\lambda w_\lambda/(a\sigma_\epsilon^2)
+(1-\lambda)\mu_U(w_\lambda)/(av_U)-\bar x}
{R[\lambda/(a\sigma_\epsilon^2)+(1-\lambda)/(av_U)]}.
$$

Substitute $\theta=w_\lambda+k_\lambda(x-\bar x)$ into informed demand to verify clearing. The supply-shock term cancels the realized supply on the right side, leaving exactly this price formula. Its slope in $w$ is positive because all precision weights and the posterior-mean slope are positive. That positivity validates the inference that price and $w$ reveal the same information.

When $\lambda=0$, use the separate boundary price

$$
P_0(x)=\frac{\bar\theta-a x(\sigma_\theta^2+\sigma_\epsilon^2)}{R}.
$$

This price reveals supply but no information about the independent risky payoff. Substituting $\lambda=0$ into the expression for $k_\lambda$ would be meaningless; the boundary must be handled explicitly.

## Measuring information and valuing research

For $\lambda>0$, the price signal is unbiased for $\theta$ conditional on $\theta$, with noise variance

$$
\operatorname{Var}(w_\lambda\mid\theta)
=\frac{a^2\sigma_\epsilon^4\sigma_x^2}{\lambda^2}.
$$

Define the dimensionless ratios from equations (16a)–(16b):

$$
m=\frac{a^2\sigma_\epsilon^4\sigma_x^2}
{\lambda^2\sigma_\theta^2},\qquad
n=\frac{\sigma_\theta^2}{\sigma_\epsilon^2}.
$$

Then price informativeness about the privately observed component is

$$
\rho_{P,\theta}^2=\frac1{1+m}.
$$

This is not the squared correlation with total payoff $u$. The latter still contains irreducible $\epsilon$ noise. Likewise, $n$ measures the quality of private information: $\operatorname{Corr}(\theta,u)^2=n/(1+n)$. A fully revealed private signal need not be a perfectly predicted terminal payoff.

For fixed $\lambda$, more supply noise reduces price informativeness. More informed participation reduces the signal noise because informed aggregate demand responds more strongly to $\theta$. Greater absolute risk aversion or residual payoff variance weakens that response and makes supply shocks harder to distinguish from information.

Theorem 2 compares optimal ex ante utilities of acquiring versus not acquiring information. It assumes individual risky endowments are independent of $(u,\theta,x)$, preventing the trader's own endowment from supplying extra information about aggregate supply. The source emphasizes this restriction in footnote 9. Dropping it requires conditioning on that additional information, and the simple utility-ratio formula need not survive.

With that assumption and the terminal-cost convention above,

$$
\frac{\mathbb E[V(W_I)]}{\mathbb E[V(W_U)]}
=e^{a\kappa}
\sqrt{\frac{\sigma_\epsilon^2}{v_U}}
\equiv\gamma(\lambda).
$$

Both expected utilities are negative. A ratio below one therefore means the informed trader has *higher*, less negative utility and research is attractive. A ratio above one favors remaining uninformed. Ignoring this sign reverses the acquisition decision.

Appendix B derives the ratio by integrating the optimized exponential utility over the private signal conditional on the price. The conditional Gaussian quadratic produces a square-root variance ratio through the noncentral chi-square moment-generating function. The terms reflecting the common price-conditioned investment opportunity cancel between informed and uninformed utilities. The result depends on residual uncertainty and research cost, not on an assumed realized alpha difference.

## Endogenous participation and a complete solution procedure

In an interior equilibrium, $\gamma(\lambda)=1$. As $\lambda$ increases, uninformed posterior variance falls, the informational advantage shrinks, and $\gamma$ increases. Theorem 3 establishes a unique overall equilibrium within the monotone informational price systems considered in the paper.

The boundary decisions are essential:

- If $\gamma(0)\ge1$, no research is worthwhile and $\lambda^*=0$.
- If $\gamma(1)\le1$, information remains worthwhile even with universal participation and $\lambda^*=1$.
- Otherwise there is a unique $\lambda^*\in(0,1)$ solving $\gamma(\lambda^*)=1$.

Weak inequalities include indifference at a boundary. For the zero-information case,

$$
\gamma(0)=\frac{e^{a\kappa}}{\sqrt{1+n}}.
$$

For an interior solution, let $g=e^{2a\kappa}-1$. Equations (18)–(19) become

$$
m^*=\frac{g}{n-g},\qquad
1-\rho_{P,\theta}^2=\frac{g}{n}.
$$

This requires $n>g$. Recover the informed fraction from its definition:

$$
\lambda^*=a\sigma_\epsilon^2
\sqrt{\frac{\sigma_x^2}{\sigma_\theta^2m^*}}.
$$

This expression is derived directly from the source's ratios. It is usable only if the result lies strictly between zero and one; a value above one indicates the universal-information boundary, not an admissible percentage greater than 100%. Near $g=0$ or $n=g$, use the boundary logic or a stable scalar root calculation rather than divide blindly by a vanishing quantity.

To reconstruct the model, specify $R,a,\kappa,\bar\theta,\bar x$ and the three variances. Solve participation using the boundary tests and interior equation. For any realized state, calculate $w$, its posterior moments, the equilibrium price, and both demands. Check the market-clearing residual numerically. A simulated experiment additionally draws independent normal $\theta,\epsilon,x$ and computes wealth under the same cost convention. The source supplies no parameter calibration, random seed, sample size, or empirical goodness-of-fit test.

As a constructed numerical check, set $R=1$, $a=1$, $\kappa=0.2$, $\sigma_\epsilon^2=1$, $\sigma_\theta^2=4$, and $\sigma_x^2=0.25$. The implied values are $g=0.4918247$, $m^*=0.1401939$, $\lambda^*=0.6676909$, $v_U=1.4918247$, and $\rho_{P,\theta}^2=0.8770438$. The utility ratio is one. Means can be chosen separately to evaluate price levels. These numbers validate the equations; they are not reported results or estimated market parameters in the paper.

## Comparative statics and the roles of boundaries

Theorem 4 is explicitly about an interior equilibrium. Its informativeness formula shows that reducing research cost or risk aversion, or improving private information quality $n$, makes the price more informative. These changes need not have the same effect on the number of researchers.

For example, increasing supply-noise variance at fixed private-information quality raises the value of becoming informed. More people acquire information. Since $m^*=g/(n-g)$ is independent of $\sigma_x^2$, participation adjusts so that equilibrium price informativeness is unchanged. From the expression for $\lambda^*$, the informed fraction rises in proportion to the supply standard deviation while other inputs remain fixed and the solution stays interior. Once $\lambda=1$, this exact offset cannot continue.

Scaling total payoff variance upward while holding $n$ fixed also attracts information production without changing interior price informativeness. A fall in research cost increases both informativeness and participation until the all-informed boundary is reached. Positive research cost can be low enough for everybody to buy information without the price becoming perfectly revealing, because nonzero supply noise remains.

Improving the signal while holding total payoff variance fixed has an ambiguous participation effect. More precise private information makes research more useful, but also causes informed demand to transmit that information more effectively to the uninformed. The paper's footnote 8 derives the threshold separating these effects. In the notation above, an equivalent threshold is

$$
\bar n=g+\sqrt{g^2+g}.
$$

For interior solutions with $g<n<\bar n$, participation rises as $n$ rises; above $\bar n$, it falls. This expression follows by solving the source's threshold equation. Informativeness rises in both regions. Reporting only an increase in research quality and asserting that more investors must become informed would miss this endogenous free-riding effect.

## The impossibility limits and thin trading

Theorem 5 analyzes the discontinuity at perfect revelation. With no supply noise and positive research cost, any positive informed fraction makes price fully reveal $\theta$. Research then has no incremental information value. With nobody informed, however, research is profitable when

$$
e^{a\kappa}<\sqrt{1+n}.
$$

Under that condition neither a positive informed fraction nor zero information is an equilibrium. If information is too expensive to satisfy the inequality, the no-information boundary can remain an equilibrium. Thus the no-noise nonexistence statement is conditional, not a claim that every costly-information economy lacks any equilibrium.

Perfect private information, $\sigma_\epsilon^2=0$, is another singular case. The informed investor would know the payoff exactly, and any unpriced advantage can generate unbounded demand under unconstrained trading. At positive informed participation, the clearing price must reveal that information; at zero participation, acquiring it is attractive. This is the model's stronger perfect-information nonexistence result, not a limit to evaluate by mechanically dividing by zero in demand.

For positive but vanishing supply noise, interior participation approaches zero while the informativeness ratio remains fixed. The exact zero-noise economy has a discontinuous acquisition incentive. A limiting sequence of equilibria is therefore not an equilibrium at the limiting primitives. The distinction is central to the paper's argument.

Section III examines trading volume arising from differences in beliefs, holding preferences fixed. Its object is aggregate informed net trade $T=\lambda(X_I-x)$, not modern gross exchange turnover. Using the affine price and demand formulas makes $T$ an affine function of independent normal $\theta$ and $x$, so its mean and variance can be computed directly; equations (22)–(24) give the expanded expressions.

The mean and variance of this trade measure vanish as participation approaches the relevant no-information or all-information limits, as private information becomes arbitrarily precise, and along the vanishing-noise limit discussed in the proof. When beliefs are nearly identical, gains from entering a market can be small. The authors suggest that fixed operating costs could then make the market too thin to function, but do not estimate those costs or solve an exchange-entry model. Heterogeneous endowments and preferences can create other reasons to trade that this exercise deliberately deemphasizes.

## Implications and limits for a reproducing researcher

The model supplies an equilibrium mechanism for information rents, not a license to label every return anomaly an informational inefficiency. Informed and uninformed traders are equal in expected utility at an interior acquisition equilibrium after research costs, although their portfolios and information differ. Their comparison is not automatically equality of Sharpe ratios, arithmetic expected returns, or net dollar profits.

The result relies on common rational inference, Gaussian signals and supply, CARA preferences, known distributional parameters, price-taking acquisition, and unconstrained positions. A firm's private endowment, a second informative security, heterogeneous costs, or a binding leverage constraint changes the information or demand system. The model's single common signal observed by informed traders is also different from a market in which every analyst receives a distinct signal.

Section IV argues that adding more securities can reveal additional state information and undermine information rents. Its discussion of a binary claim illustrates the conflict between completing markets and sustaining costly information production. It should not be read as a general proof that all real derivative markets must disappear: the conclusion depends on the stylized information and market-creation assumptions.

The authors explicitly leave the social optimum of information collection unresolved. Private incentives to acquire information, informativeness of equilibrium prices, and welfare gains from information are separate objects. The reproducible core is the sequence of conditional inference, risk-bearing demand, clearing, and acquisition indifference. A quantitative extension should preserve that sequence and state which assumptions it relaxes, rather than impose a fixed informed fraction while claiming the paper's endogenous equilibrium conclusions.
