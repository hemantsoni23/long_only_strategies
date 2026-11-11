# On the Inefficiency of Bang-Bang and Stop-Loss Portfolio Strategies

**Christian Gollier (1997).** *Journal of Risk and Uncertainty* 14(2), 143–154. [Source PDF](../../Finance/StopLoss_Gollier_1997.pdf). The thirteen-page file contains a JSTOR cover and the complete twelve-page article, including proofs, two portfolio trees, endnotes, and references. Printed page 143 is PDF page 2. This is a theoretical paper; it contains no estimated trading strategy or empirical return comparison.

## Why this matters

Switching an entire portfolio between a risky asset and cash is not generally equivalent to maintaining a diversified allocation through time. Gollier provides two distinct reasons. First, under the additive-return model and exchangeability assumptions used in the paper, calendar switching adds a mean-preserving risk to a constant diversified position. Second, a policy that permanently abandons a positive-premium risky asset after hitting a threshold generally conflicts with a smooth expected-utility objective in the unconstrained dynamic portfolio model.

The important qualification is that the paper also constructs an optimal threshold-related policy. With a kinked terminal utility and binary risky returns, holding a safe reserve and investing the surplus can be optimal. It differs from investing everything in the risky asset and hoping to sell exactly at a floor. The contribution therefore concerns which preferences and trading opportunities justify a policy; it is not an empirical finding that every stop-loss rule loses money or reduces every investor’s welfare.

The closest antecedents are Samuelson’s criticism of temporal diversification and Dybvig’s complete-market inefficiency argument. Gollier extends the first comparison beyond expected utility to preferences respecting second-order stochastic dominance, and develops the stop-loss argument without requiring complete markets. His constructive example shows exactly how nonsmooth preferences change the conclusion.

## The additive-return comparison

Section 2 uses two assets, $X$ and $Y$, over $T$ periods. Return pairs $(x_t,y_t)$ are independent and identically distributed across time, but contemporaneous dependence between $x_t$ and $y_t$ is allowed. Interest is paid at the terminal date and is not compounded. Initial wealth is normalized; the source compares additive terminal payoffs, omitting any common initial-wealth term that has no effect on the dominance ranking.

Choose an integer $k\in\{0,\ldots,T\}$ and let $p=k/T$. Three policies have the same expected payoff:

$$
Z_B=\sum_{t=1}^{k}x_t+\sum_{t=k+1}^{T}y_t,
$$

$$
Z_M=\sum_{t=1}^{T}\left[\xi_t x_t+(1-\xi_t)y_t\right],
\qquad P(\xi_t=1)=p,
$$

$$
Z_D=\sum_{t=1}^{T}\left[px_t+(1-p)y_t\right].
$$

$B$ is scheduled all-or-nothing switching, $M$ random all-or-nothing switching, and $D$ constant diversification. The selection coins in $M$ are independent of the return process. The comparison holds their expected asset exposure fixed; it does not optimize $p$ or compare a timing signal with a matched passive strategy.

For the scheduled strategy, the difference from diversification is

$$
\varepsilon_B=(1-p)\sum_{t=1}^{k}(x_t-y_t)
-p\sum_{t=k+1}^{T}(x_t-y_t).
$$

Conditional on $Z_D$, exchangeability makes the conditional mean of each $x_t-y_t$ the same. Since $(1-p)k-p(T-k)=0$,

$$
E[\varepsilon_B\mid Z_D]=0,\qquad Z_B=Z_D+\varepsilon_B.
$$

Thus the scheduled payoff is a mean-preserving spread of the diversified payoff. For random switching,

$$
\varepsilon_M=\sum_{t=1}^{T}(\xi_t-p)(x_t-y_t).
$$

Conditional on the entire return path, the mean of every term is zero. Iterated expectations imply $E[\varepsilon_M\mid Z_D]=0$. This second argument only needs independent policy randomization in the additive setup; it does not need the full i.i.d. assumption to establish this particular comparison.

Every increasing concave expected-utility function weakly prefers $Z_D$. More generally, a decision criterion that respects mean-preserving second-order stochastic dominance cannot strictly prefer either dominated payoff. A strict welfare improvement requires a genuinely nondegenerate spread and preferences that strictly penalize it. At $p=0$ or $p=1$, the policies coincide; other degeneracies or risk-neutral indifference also need to be excluded before saying every switching policy is strictly inferior.

The conclusion’s language about an absence of serial correlation should be read alongside the actual i.i.d. assumption. Zero autocorrelations alone do not establish the conditional exchangeability used in the scheduled-switching proof. Predictable volatility, changing distributions, or informative switching signals fall outside that proof. Likewise, replacing the additive payoffs by compounded self-financing wealth changes the problem; equations (1)–(9) are not a proof for every such extension.

## The dynamic expected-utility problem

Section 3 changes the setup to a conventional multiperiod wealth recursion with a risk-free asset. Let $p_t$ denote the dollar amount invested in the risky asset, not the risky fraction. If wealth before the period is $z$, next wealth is

$$
W'=z(1+y_t)+p_tR_t,\qquad R_t=x_t-y_t.
$$

Here $y_t$ is deterministic and $R_t$ is the excess return. Terminal consumption equals terminal wealth. The Bellman recursion in equation (10) is

$$
v_{t-1}(z)=\max_{p_t}E\!\left[v_t\left(z(1+y_t)+p_tR_t\right)\right],
\qquad v_T=u.
$$

The feasible positions and utility domain must permit the local variations used below. The paper’s analytical arguments concern the standard divisible-portfolio problem, without discrete investment sizes, transaction charges, or imposed stop barriers. State-dependent borrowing constraints or nonconvex controls cannot be added while retaining the theorem without further analysis.

At a regular interior optimum, the first-order condition is

$$
E\!\left[R_t v_t'\left(z(1+y_t)+p_tR_t\right)\right]=0.
$$

The issue is what happens to continuation utility after future portfolio choices are optimized. Smooth, concave terminal utility does not by itself mean that every imaginable maximization problem has a smooth, concave value function. Gollier establishes the relevant inheritance properties in this particular portfolio problem, using the linear wealth transition and its regularity assumptions.

## Why concavity survives dynamic optimization

The envelope derivative is

$$
v_{t-1}'(z)=(1+y_t)E[v_t'(W')].
$$

Differentiate the first-order condition with respect to wealth:

$$
\frac{\partial p_t}{\partial z}
=-(1+y_t)\frac{E[R_tv_t''(W')]}{E[R_t^2v_t''(W')]}.
$$

Substitution into the second envelope derivative yields a transparent version of equations (13)–(15):

$$
v_{t-1}''(z)=(1+y_t)^2\left[
E[v_t''(W')]-\frac{\{E[R_tv_t''(W')]\}^2}{E[R_t^2v_t''(W')]}
\right].
$$

For $a=-v_t''(W')\geq0$, Cauchy–Schwarz gives $\{E[aR_t]\}^2\leq E[a]E[aR_t^2]$. The bracket is therefore nonpositive when its denominator is well defined. Backward induction preserves concavity. This derivation requires the usual integrability, differentiability, and nondegenerate interior first-order condition; flat or constrained cases need the corresponding weak or boundary argument.

The result does not say that the entire shape of risk preferences is preserved. Linear absolute risk tolerance gives the familiar strong simplifications associated with HARA utility, but decreasing absolute risk aversion need not pass through dynamic optimization. The source explicitly notes that a wealthier investor can sometimes choose a smaller risky dollar position even if terminal utility has decreasing absolute risk aversion.

The paper also discusses why nonconvex controls change the conclusion. If a risky project is available only in a fixed indivisible size, optimizing whether to accept it can create local convexity in the value of future opportunities. That is a different decision problem from continuously adjusting a traded position.

## Why an all-cash stopping region conflicts with smooth preferences

At a zero risky position, smooth increasing continuation utility gives

$$
\left.\frac{\partial}{\partial p}E[v_t(z(1+y_t)+pR_t)]\right|_{p=0}
=v_t'(z(1+y_t))E[R_t].
$$

If the conditional expected excess return is positive and a small positive position is feasible, the derivative is positive. Remaining entirely in cash is not optimal. This is the local reason a stop-loss rule that permanently switches to cash, or a lock-in rule that does so after reaching a target, fails in the smooth unconstrained model. It is not a claim that the investor must remain fully invested, maintain the same risky fraction, or ignore changes in the investment opportunity set.

In the paper’s terminology, differentiable utility has second-order risk aversion: the local risk premium for a small zero-mean exposure is of second order in its size. At a concave kink, left and right marginal utilities differ, producing first-order sensitivity to small risk. This use of “second-order” concerns local risk-premium scaling; it should not be confused with the stochastic-dominance comparison earlier in the paper.

To see the kink’s effect directly, let the continuation utility slopes at safe next wealth be $a$ from the left and $b$ from the right, with $a\geq b$. The right derivative with respect to a small positive risky position is

$$
aE[R_t\mathbf1_{\{R_t<0\}}]+bE[R_t\mathbf1_{\{R_t>0\}}].
$$

It can be negative despite $E[R_t]>0$. Downside increments receive the larger marginal-utility weight. This is a precise mechanism for zero exposure at a reference wealth level. A regulatory floor, contractual liability, or discrete liquidation rule would introduce other mechanisms, but they are not equivalent to the paper’s smooth expected-utility assumptions.

## Constructive solution with a utility kink

Section 4 sets the safe return to zero and assumes binary risky returns: $x_-<0$ with probability $\pi$, and $x_+>0$ with probability $1-\pi$, with positive mean. Terminal utility is

$$
u(z)=\begin{cases}
z-D,&z<D,\\
\kappa(z-D),&z\geq D,
\end{cases}\qquad 0<\kappa<1.
$$

The reference level $D$ creates a downward kink in marginal utility. The source allows the limiting case $\kappa=0$ in its initial description, but the logarithmic horizon formula requires a limiting treatment there. The concave utility can also represent expected after-tax wealth with a marginal tax rate $1-\kappa$ above an exemption, as the paper’s endnote observes.

For a sufficiently short remaining horizon, equation (19) gives the optimal risky dollar position:

$$
p^*(z)=\begin{cases}
(D-z)/x_+,&z<D,\\
(z-D)/(-x_-),&z\geq D.
\end{cases}
$$

Below the target, a favorable return lands exactly at $D$. Above it, an unfavorable return lands exactly at $D$. At $D$, the position is zero. The solution is tied to the binary return support; with a continuous return distribution, the continuation value is generally no longer piecewise linear and the closed form does not follow.

In remaining-horizon notation, let $V_n$ denote value with $n$ periods still to invest and $V_0=u$. When the finite optimum exists, define

$$
A=\pi\frac{x_+-x_-}{x_+},\qquad
B=(1-\pi)\frac{x_+-x_-}{-x_-}.
$$

Then

$$
V_n(z)=\begin{cases}
A^n(z-D),&z<D,\\
\kappa B^n(z-D),&z\geq D.
\end{cases}
$$

This simply reindexes equation (20), including its upper-branch factor $\kappa$. Conditional on being below $D$, the positive outcome reaches the kink and the negative branch carries the lower slope forward. Above $D$, the negative outcome reaches the kink and the positive branch carries the upper slope. That explains both coefficient recursions without a numerical optimizer.

The condition for a finite positive optimum is

$$
n<K,\qquad
K=\frac{\log\kappa}{\log\left(\frac{-\pi x_-}{(1-\pi)x_+}\right)}.
$$

Positive expected excess return puts the ratio inside the denominator logarithm between zero and one. The condition ensures that the marginal utility penalty for sufficiently large risky positions outweighs their positive expected return. The source states unbounded demand beyond the threshold; the knife-edge equality case is not resolved in its proposition and should not be silently assigned to either strict regime. Unboundedness is a consequence of the unrestricted borrowing/position environment, not a recommendation to lever a strategy.

## The two portfolio trees

Figures 1 and 2 use $x_+=-x_-=1$ and $D=1$. In Figure 1, initial wealth is 2. The optimal allocation holds 1 safely and invests the remaining 1. A loss leaves the reserve of 1 and stops further exposure; a win creates wealth 3, consisting of 1 safe and 2 risky. Subsequent wins raise the risky stake to 4 and then 8, while the safe reserve stays at 1. This protects the floor through ex ante position sizing, not through an assumed ability to liquidate a fully invested portfolio after a discrete jump.

Figure 2 starts with zero wealth. The initial risky stake is 1, financed by borrowing. A win produces wealth 1 and ends trading. A loss leaves wealth $-1$, after which the risky stake becomes 2 and the cash balance becomes $-3$; another loss leads to wealth $-3$, a risky stake of 4, and cash $-7$. This is a doubling-after-loss strategy with an explicit finite-horizon utility justification under the stated parameter restriction. It does not offer a riskless profit: losses remain possible at the terminal date, and sufficient credit is assumed.

There is a sign error in the prose below equation (20): for wealth below $D$, the discussion refers to investing $z-D$. Equation (19) and Figure 2 require the positive quantity $(D-z)/x_+$, which becomes $D-z$ when $x_+=1$. The formula and illustrated borrowing strategy, rather than that sentence, determine the reconstruction.

As a derived numerical check, choose $\pi=0.4$, $x_-=-1$, $x_+=1$, and $\kappa=0.25$. Then $K\simeq3.419$, so the stated bounded policy applies for one, two, or three remaining periods. For initial wealth 2, three consecutive wins produce terminal wealth 9; any loss stops the process at wealth 1. The probabilities are $0.6^3=0.216$ and $0.784$. Expected terminal utility is $0.216\times0.25\times8=0.432$, agreeing with $\kappa B^3(z-D)=0.25(1.2)^3$. These numbers are an explicitly constructed check, not a reported calibration or empirical result.

## Reproduction and scope

The dominance proof can be reproduced analytically from the coupling equations; a simulation is unnecessary to establish it. A numerical illustration should use identical return draws for both policies, preserve the i.i.d. pair structure for scheduled switching, and compare terminal distributions or expected concave utilities at the same $p$. A favorable sample average from a randomly generated timing policy would not overturn the distributional theorem.

For the kinked-utility example, exact binary enumeration supplies a stronger check than a coarse wealth grid: initialize the terminal utility, recurse over the two outcomes, and verify that the candidate position places one outcome at the kink. Report the horizon threshold, borrowing assumptions, and any imposed position bounds. A finite grid can falsely turn an unbounded optimization into a finite optimum at its maximum grid point.

No sample dates, market universe, estimated risk premium, transaction costs, slippage, or inference procedure are provided because the paper does not conduct an empirical experiment. Its results do not settle the value of stops in a model with serial dependence, changing expected returns, financing frictions, contractual loss limits, or organizational incentives. The durable distinction is between an arbitrary all-or-nothing exit rule and a portfolio policy derived from preferences, feasible trades, and the distribution of future opportunities.
