# Optimal Investment Strategies for Controlling Drawdowns

**Sanford J. Grossman and Zhongquan Zhou.** *Mathematical Finance* 3(3), July 1993, 241–276. Source: [Drawdowns_GrossmanZhou_1993.pdf](../../Finance/Drawdowns_GrossmanZhou_1993.pdf), the complete 36-page article including Appendices A–F. Printed pages equal PDF pages plus 240. The model equations, boundary conditions, numerical figures, and computational appendices were inspected visually as well as through text extraction.

## Why this matters

A fixed capital floor and a maximum-drawdown limit are different constraints. With a fixed floor, profits create additional risk capacity without raising the protected amount. With a drawdown limit, new wealth records raise the floor itself. A manager therefore has an incentive to limit risk even at a new high, because part of the next gain becomes permanently protected capital. The paper makes this distinction precise in a continuous-time portfolio problem and derives the resulting optimal policy.

The main explicit result applies when the high-water mark grows at the risk-free rate. Optimal risky dollar holdings are proportional to wealth above the protected high-water mark, but the multiplier differs from ordinary constant-proportion portfolio insurance. The authors also solve the more general case in which the high-water mark grows more slowly than cash, reducing the problem to scalar nonlinear equations. A second contribution is the short-horizon behavior at a new high: expected risky exposure can fall sharply because the floor ratchets upward on favorable Brownian moves.

These are results for a frictionless diffusion model with continuous trading and a hard pathwise constraint. They do not establish that a discretely rebalanced strategy can guarantee a drawdown cap, nor do they demonstrate a profitable trading signal based on market “resistance.” The latter interpretation is a conjecture about equilibrium behavior, explicitly beyond the solved partial-equilibrium model.

## Market, high-water mark, and objective

Use bars for nominal quantities, following Section 1. There is one risky asset with price process

$$
\frac{dP_t}{P_t}=(r+\mu)dt+\sigma dZ_t,
$$

where $r$ is the constant cash rate, $\mu$ the constant excess drift, $\sigma>0$ volatility, and $Z_t$ a Brownian motion. There are no dividends, transaction costs, jumps, borrowing spreads, or exogenous leverage constraints. A predictable risky dollar position $\bar x_t$ generates self-financing wealth

$$
d\bar W_t=r\bar W_tdt+\bar x_t(\mu dt+\sigma dZ_t).
$$

Define a high-water-mark growth rate $\bar\lambda$ and historical initial mark $M_0\geq\bar W_0$:

$$
\bar M_t=\max\left\{M_0e^{\bar\lambda t},\ 
\sup_{0\leq s\leq t}\bar W_s e^{\bar\lambda(t-s)}\right\}.
$$

The investor requires $\bar W_t\geq\alpha\bar M_t$ almost surely at every time, with $0<\alpha<1$. Thus $1-\alpha$ is the maximum permitted drawdown relative to this adjusted mark. For $\bar\lambda=0$ it is the ordinary nominal running wealth maximum. For $\bar\lambda=r$ past records appreciate at the cash rate. Negative $\bar\lambda$ permits old records to decay. The feasible infinite-horizon setup requires $\bar\lambda\leq r$; a guaranteed floor growing faster than the safe asset cannot generally be financed from finite initial capital in this market.

For relative risk aversion $A>0$, $A\neq1$, utility is $U(W)=W^{1-A}/(1-A)$. The objective is

$$
\sup_{\bar x\in\mathcal A}\liminf_{T\to\infty}
\frac{1}{(1-A)T}\log E[\bar W_T^{1-A}],
$$

where admissibility includes well-defined adapted wealth and the pathwise floor constraint. This is a long-run certainty-equivalent growth criterion. It is not expected arithmetic wealth growth, a fixed-horizon Sharpe ratio, or expected logarithmic growth except in the separate log-utility case. When $A>1$, the negative factor $1-A$ reverses inequalities in manipulations of the power moment; preserving it is essential.

Discount by the high-water-mark growth rate:

$$
W_t=e^{-\bar\lambda t}\bar W_t,\quad
x_t=e^{-\bar\lambda t}\bar x_t,\quad
M_t=\max\{M_0,\sup_{s\leq t}W_s\},\quad
\lambda=r-\bar\lambda\geq0.
$$

The transformed problem is

$$
dW_t=\lambda W_tdt+x_t(\mu dt+\sigma dZ_t),\qquad
W_t\geq\alpha M_t.
$$

Let $\xi$ denote its optimal growth rate. The nominal rate is $\bar\xi=\xi+\bar\lambda$. This distinction prevents a common misreading: the paper's closed-form $\lambda=0$ case corresponds to $\bar\lambda=r$, not generally to a fixed nominal high-water mark. Ordinary nominal drawdown control has $\bar\lambda=0$ and hence $\lambda=r$.

Without drawdown control, the Merton risky fraction is $\mu/(A\sigma^2)$ and nominal certainty-equivalent growth is $r+\mu^2/(2A\sigma^2)$. Appendix A shows that a nondegenerate constant-fraction Merton strategy eventually violates a positive drawdown constraint with probability one. The argument uses independent Brownian increments over repeated intervals, each admitting a sufficiently adverse relative excursion; favorable long-run growth does not eliminate eventual drawdowns.

## State reduction and the record boundary

The natural state is $(W,M)$, not wealth alone. Homogeneity suggests an eigenfunction $V(W,M)=M^{1-A}f(u)$ with $u=W/M\in[\alpha,1]$. Holding $M$ fixed, it should increase and be concave in $W$; holding $W$ fixed, a higher mark tightens the constraint and reduces value.

Away from a new record, $dM=0$. The stationary Bellman equation is

$$
0=\sup_x\left\{-(1-A)\xi V+\lambda W V_W+\mu x V_W
+\frac12\sigma^2x^2V_{WW}\right\}.
$$

Concavity yields the interior optimizer

$$
x^*=-\frac\mu{\sigma^2}\frac{V_W}{V_{WW}}
=-\frac\mu{\sigma^2}\frac{f'(u)}{f''(u)}M.
$$

At the lower boundary, nonzero diffusion exposure would immediately create a positive probability of breaching the floor. The admissible boundary policy therefore has $x=0$. At $u=1$, the running maximum can increase. Since it has finite variation, its contribution to Itô's formula is $V_MdM$, with no quadratic-variation term. Optimality imposes

$$
V_M(M,M)=0\quad\Longleftrightarrow\quad f'(1)=(1-A)f(1).
$$

This is the economically important record-boundary condition. Starting at a record with nonzero risky exposure, the expected increase of the running maximum over a short interval is of order $\sqrt h$, while ordinary drift terms are of order $h$. A strictly negative $V_M$ term would dominate the local Bellman balance. Moreover, $dM$ is supported only where $W=M$, so setting $V_M=0$ there removes the entire Stieltjes integral along a path. It does not mean that the floor is irrelevant; it determines the value function and optimal risk multiplier.

The authors explicitly treat the early Bellman derivation as heuristic and later verify the constructed solution. They do not rely on an unproved exchange of an infinite-horizon limit and expectation to establish optimality. This separation between finding a candidate and verifying it is an important part of the paper's argument.

## Explicit solution when the adjusted cash drift is zero

For $\lambda=0$, the reduced equation is

$$
0=-(1-A)\xi f(u)-\frac{\mu^2}{2\sigma^2}
\frac{[f'(u)]^2}{f''(u)}.
$$

A power solution has $f(u)=c(u-\alpha)^\beta$, where the lower-boundary policy fixes the shift at $\alpha$ and the record condition gives

$$
\beta=(1-A)(1-\alpha),\qquad
D=1-\beta=\alpha+(1-\alpha)A.
$$

Equations (2.20)–(2.22) and Theorem 4.2 give

$$
x_t^*=k(W_t-\alpha M_t),\qquad
k=\frac\mu{\sigma^2D},\qquad
\xi=\frac{\mu^2}{2\sigma^2}\frac{1-\alpha}{D}.
$$

The risky fraction is $\pi(u)=k(1-\alpha/u)$. For $\mu>0$ it increases with the distance above the floor and reaches $k(1-\alpha)$ at a record. A positive cash position is not imposed separately; sufficiently attractive opportunities can produce leverage. For negative $\mu$, the sign of the risky position reverses under the same unconstrained market assumptions. If $\mu=0$, the risky investment problem degenerates to safe investment and formulas dividing by $\mu$ should not be used.

The boundary initialization needs care. When $\lambda=0$ and $W_0=\alpha M_0$, the only feasible exposure at the floor is zero and transformed wealth remains there. Its transformed growth rate is zero. The positive growth expression above describes an initially positive cushion, $W_0>\alpha M_0$. The optimal diffusion preserves a positive cushion at every finite time from such an initial state. An implementation should not assign the interior long-run value to an absorbing zero-cushion initialization.

For a fixed protected amount $K$ in the corresponding discounted problem, ordinary CPPI uses $x=(\mu/(A\sigma^2))(W-K)$. Drawdown control instead replaces $A$ in the multiplier with $D=\alpha+(1-\alpha)A$. This is a convex combination of original risk aversion and logarithmic risk aversion one. The multiplier on the cushion may rise or fall relative to fixed-floor CPPI depending on whether $A$ exceeds one. Total risky exposure is nevertheless below the unconstrained Merton exposure because only the cushion is invested.

Specifically, the ratio of the drawdown-constrained risky fraction to Merton's is

$$
\frac{\pi(u)}{\mu/(A\sigma^2)}
=\frac{A(1-\alpha/u)}{D}\in[0,1].
$$

The growth-rate ratio in the zero-adjusted-cash problem is $\xi_\alpha/\xi_0=A(1-\alpha)/D$. Tighter protection lowers attainable growth. The proportional sacrifice is less pronounced when risk aversion is already high; an investor already taking little risk gives up less by adding the constraint. This comparison concerns the risky growth component, not total nominal growth after adding the cash-rate transformation.

## Exact wealth representation and simulation

Section 2.5 and Appendix C express the policy through a regulated Brownian motion. Define

$$
b=k\mu-\frac12k^2\sigma^2,\qquad a=k\sigma,
$$

$$
L_t=\max\left\{0,\sup_{0\leq s\leq t}
\left[\log\!\left(\frac{W_0/M_0-\alpha}{1-\alpha}\right)+bs+aZ_s\right]\right\}.
$$

Then

$$
M_t=M_0e^{(1-\alpha)L_t},
$$

$$
W_t=\alpha M_0e^{(1-\alpha)L_t}
+(W_0-\alpha M_0)e^{-\alpha L_t+bt+aZ_t}.
$$

Equivalently,

$$
u_t=\alpha+(W_0/M_0-\alpha)e^{bt+aZ_t-L_t}.
$$

The regulator keeps $u_t\leq1$ while the positive exponential cushion ensures $u_t>\alpha$ at finite times for a strictly positive initial cushion. Appendix C verifies both that the constructed $M_t$ really is the running maximum of constructed wealth and that the wealth process satisfies the self-financing SDE. Merely positing a convenient increasing process as a floor would not suffice.

These equations give a better benchmark for simulation than an unconstrained Euler step followed by ad hoc clipping. Exact continuous-time behavior depends on the running supremum between observation times. A grid-only maximum underestimates that supremum and therefore the floor ratchet; a Brownian-bridge maximum treatment or mesh-refinement analysis is needed for accurate discretization. Those are implementation consequences of the formula, not numerical procedures reported in the paper.

The power-moment growth argument uses the fact that $W_t/M_t$ stays between $\alpha$ and one, so wealth and its maximum have the same exponential moment-growth rate up to bounded multiplicative constants. With $\beta=(1-A)(1-\alpha)$, moments of the Brownian maximum lead to the candidate rate. Section 4 supplies the upper-bound verification, rather than treating the constructed feasible policy alone as proof of global optimality.

## Expected exposure near a new high

For $\lambda=0$ and $\mu>0$, the interior instantaneous drift of $\pi(u)$ is

$$
\lim_{h\downarrow0}\frac{E[\pi_{t+h}-\pi_t\mid u_t=u]}h
=k\alpha\frac{u-\alpha}{u^2}
\left[k\mu-k^2\sigma^2\frac{u-\alpha}{u}\right],\quad u<1.
$$

It is positive exactly when $\beta<\alpha/u$. In particular, it is positive sufficiently close to the lower floor for every $A>0$. It is positive throughout the interior if $A\geq1$ or $\alpha\geq0.5$. This does not imply that the strategy deliberately increases risk following a price decline: its current risky fraction remains increasing in $u$. The statement concerns its conditional expected subsequent change under the stochastic model.

At $u=1$, the regulator contributes a negative term of order $\sqrt h$, which dominates the $O(h)$ interior drift. Consequently both the expected fraction and the expected dollar amount invested in the risky asset fall over a sufficiently short interval starting from a record. The limits in state and time cannot be interchanged. A derivative valid for a fixed interior $u<1$ does not capture the record-boundary effect by simply setting $u=1$ afterward.

Appendix D makes this calculation reproducible. Define $v=\log(1-\alpha)-\log(u-\alpha)\geq0$, so $u=\alpha+(1-\alpha)e^{-v}$. The reflected process for $v$ has drift $-b$, diffusion magnitude $|a|$, and lower barrier zero. For $\mu>0$, hence $a>0$, its transition tail is

$$
P(v_{t+h}>z\mid v_t=v)
=\Phi\!\left(\frac{-z+v-bh}{a\sqrt h}\right)
+e^{-2bz/a^2}
\Phi\!\left(\frac{-z-v+bh}{a\sqrt h}\right),\quad z\geq0.
$$

Integrating $k[1-\alpha/(\alpha+(1-\alpha)e^{-z})]$ against this transition distribution yields the conditional expected future risky fraction. Subtract its current value to obtain the change. This form also preserves the $k\alpha$ coefficient that is absent from the first integral in the final printed display of Appendix D; the preceding expectation in that appendix establishes the required coefficient.

Figures 2.1–2.2 use $\lambda=0$, $\alpha=0.7$, $A=2$, $\mu=0.06$, and $\sigma=0.2$. They plot **percentage changes in the risky fraction**, $100E[\pi_{t+h}/\pi_t-1\mid u_t=u]$, not portfolio returns. The daily horizon is $h=0.004$ and the caption's monthly horizon is $h=0.088$; replacing the latter with $1/12$ would change the published setup. The curves exhibit a small positive interior expected change and a sharp negative move near the record. No market data or statistical estimation is involved in these figures.

## Slower high-water-mark growth: the numerical solution

For $\lambda>0$, cash grows faster than the protected mark between records. Cash interest can rebuild a depleted cushion, so the optimal policy is no longer a constant multiple of that cushion. Let

$$
Q=\frac{\mu^2}{2\sigma^2},\qquad y(u)=\frac{f'(u)}{f''(u)}<0.
$$

Differentiating the reduced Bellman equation gives equation (3.8):

$$
Qy(u)y'(u)+[(1-A)\xi+Q-\lambda]y(u)-\lambda u=0.
$$

The boundary conditions are $y(\alpha)=0$ and $\xi-\lambda=-Qy(1)$. For a trial growth rate $\xi$, define $B=(1-A)\xi+Q-\lambda$, $D_B=\sqrt{B^2+4Q\lambda}$, and

$$
\theta_1=\frac{-B-D_B}{2Q}<0,\qquad
\theta_2=\frac{-B+D_B}{2Q}>0,\qquad
\delta=-\frac B{D_B}.
$$

Equations (3.9)–(3.12) give

$$
|y(u)-\theta_1u|^{1-\delta}
|y(u)-\theta_2u|^{1+\delta}=C,
\qquad
C=(-\theta_1\alpha)^{1-\delta}(\theta_2\alpha)^{1+\delta}.
$$

Insert $y(1)=-(\xi-\lambda)/Q$ to obtain a scalar equation for $\xi$. A useful search range supplied in Section 3.2 is

$$
\frac{Q(1-\alpha)}{\alpha+(1-\alpha)A}
\leq\xi-\lambda\leq\frac QA.
$$

After finding the growth rate, solve the implicit equation separately for every desired $u$, selecting the negative branch $\theta_1u<y(u)\leq0$. The risky wealth fraction is

$$
\pi(u)=-\frac\mu{\sigma^2}\frac{y(u)}u.
$$

For a stable reconstruction, solve the logarithm of the implicit product rather than multiplying fractional powers. At each $u>\alpha$, the residual is positive at $y=0$ and tends to negative infinity as $y$ approaches $\theta_1u$ from above, allowing a bracketed scalar solve. Set the endpoint $y(\alpha)=0$ explicitly. This algorithm is a numerical implementation of the published equations; the article does not provide source code, stopping tolerances, interpolation choices, or a grid specification.

Appendix E gives an equivalent construction in terms of the risky fraction and establishes uniqueness on its admissible positive-exposure branch for $\mu>0$. Its transformed product function decreases on that branch, while the right-hand side falls as $u$ rises. Thus $\pi(u)$ increases with $u$ and vanishes at the floor. A generic nonlinear solver allowed to search every absolute-value branch could return an economically inadmissible solution; branch selection is part of reconstructing the method.

## Numerical illustrations and log utility

Figure 3.1 holds $A=2$, $\mu/\sigma=0.3$, and $\alpha=0.7$. The plotted quantity is $\xi-\lambda=\bar\xi-r$, the growth premium over cash, not total nominal growth. Its lower endpoint is approximately 0.010385 and its unconstrained upper bound is 0.0225 per year. Relaxing mark growth relative to cash improves the attainable premium, particularly near $\lambda=0$.

For the Figure 3.2 inputs $\mu=0.06$, $\sigma=0.2$, $A=2$, and $\alpha=0.7$, solving the published scalar equations gives the following numerical cross-checks. These are recomputed values, not a table printed in the source:

| $\lambda$ | Growth premium $\xi-\lambda$ | Risky fraction at a new high |
|---:|---:|---:|
| 0 | 0.010385 | 0.346154 |
| 0.001 | 0.012109 | 0.403634 |
| 0.0101 | 0.016808 | 0.560277 |
| 0.02 | 0.018854 | 0.628464 |
| 0.04 | 0.020783 | 0.692760 |

The unconstrained Merton fraction is 0.75. Figure 3.2's horizontal axis is $1-\alpha/u$, the cushion as a fraction of current wealth, **not** the drawdown $1-u$. The curves approach the Merton benchmark as the floor becomes less restrictive. Mislabeling that axis would reverse how one interprets risk capacity.

For logarithmic utility, Section 3.1 instead maximizes $\liminf_T T^{-1}E[\log W_T]$. Set the relative value function to $I(W,M)=\log M+h(u)$. The record condition becomes $h'(1)=1$, and $y=h'/h''$ satisfies

$$
Qyy'+(Q-\lambda)y-\lambda u=0.
$$

The same implicit construction works with $B=Q-\lambda$, independent of the unknown growth rate. Solve for $y(u)$ first, then obtain log growth $\vartheta=\lambda-Qy(1)$. At $\lambda=0$, $y=-(u-\alpha)$, $\pi(u)=(\mu/\sigma^2)(1-\alpha/u)$, and $\vartheta=Q(1-\alpha)$. Log utility is treated separately because the power-utility normalization is singular at $A=1$.

## Verification, limitations, and implementation consequences

For $\lambda>0$, the authors reconstruct

$$
f(u)=\frac1{1-A}\exp\!\left[
\int_\alpha^u\frac{(1-A)\xi}{\lambda v-Qy(v)}\,dv\right].
$$

The denominator is bounded away from zero on the state interval because $\lambda>0$, $v\geq\alpha$, and $y\leq0$. The resulting value function has the required sign, concavity, Bellman equality under the proposed policy, and bounded comparability with power utility. Applying Itô's formula to its discounted process yields an upper bound for every admissible strategy and equality for the candidate. The running-maximum term vanishes by the record condition. These properties verify the long-run optimality claim and the asymptotic growth rate of finite-horizon value functions; they do not assert that the stationary policy is exactly optimal at every finite horizon.

Theorem 4.2 obtains the zero-adjusted-cash result by continuity from positive $\lambda$, combined with the feasible policy's explicit lower bound. Appendix F handles the sign differences between $A<1$ and $A>1$. The verification statements rely on the candidate's admissibility and the stochastic-integral expectations used in the argument; a finite-grid trading rule is a different admissibility problem.

No empirical estimation or historical backtest appears in the paper. The numerical inputs are illustrative constants. There are no transaction-cost estimates, out-of-sample windows, market universes, fitted forecasts, or statistical confidence intervals to reconstruct. The main evidence is analytical: a solved diffusion control problem, verification arguments, and numerical evaluation of its equations.

For practical implementation, the hard guarantee is the most fragile assumption. Jumps, trading delays, finite rebalancing intervals, bid–ask spreads, financing limits, and estimation error can all invalidate it. A period-by-period exposure rule must model losses between trades and report realized floor breaches; clipping wealth afterward is not a self-financing guarantee. The model also assumes a stable excess drift and volatility, an infinite horizon, and a fixed investor risk preference. It does not optimize the drawdown threshold itself or determine when a manager should be fired.

The contribution remains useful precisely because it identifies what the high-water mark changes. Risk capacity depends on both wealth and the protected record; the floor's ratchet changes the optimal multiplier; cash growth relative to the mark creates an additional recovery mechanism; and a record boundary has a distinct short-horizon effect. Those mechanisms can guide extensions, provided the continuous-time theorem and the assumptions of a tradable implementation remain clearly separated.
