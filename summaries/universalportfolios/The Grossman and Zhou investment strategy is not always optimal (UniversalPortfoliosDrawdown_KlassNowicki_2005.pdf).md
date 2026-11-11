# The Grossman and Zhou investment strategy is not always optimal

Michael J. Klass and Krzysztof Nowicki. *Statistics & Probability Letters* 74 (2005), 245–252. DOI 10.1016/j.spl.2005.04.060. Source: [UniversalPortfoliosDrawdown_KlassNowicki_2005.pdf](../../Finance/UniversalPortfoliosDrawdown_KlassNowicki_2005.pdf). All eight supplied pages, including the proof and references, were read. Page references below use printed journal pages.

## Why this matters

A portfolio rule derived for continuous rebalancing need not remain optimal when trades occur at discrete dates. Klass and Nowicki establish this point for an economically attractive drawdown policy: protect a fraction of the running wealth maximum in cash and apply the unconstrained growth-optimal risky fraction to the remaining cushion. Their counterexample respects the wealth floor at every decision date, has independent identically distributed returns, uses one risky asset and cash, and has an interior unconstrained Kelly fraction. The failure therefore cannot be attributed to forecasting, estimation error, multiple assets, leverage, or violation of the constraint.

The improvement is particularly revealing. Increase the risky allocation only on the first step after reaching a new wealth maximum; otherwise retain the original rule. In the constructed market this increases the long-run logarithmic growth rate for every strictly positive, nontrivial protection fraction. The argument relies on the overshoot above a previous maximum. Continuous diffusion paths reach a barrier continuously; a discrete return can jump past it. The value of the overshoot changes the appropriate allocation at the beginning of a new excursion.

This is a counterexample to extrapolating a continuous-time solution. It does not invalidate Grossman and Zhou's original continuous-time theorem and does not solve the general discrete-time drawdown-constrained allocation problem. The paper's contribution is an explicit distribution and a rigorous, feasible perturbation with strictly positive marginal growth benefit. There is no empirical strategy backtest, return forecast, fitted parameter, transaction-cost analysis, or claim that the modified policy is globally optimal.

## Market, objective, and benchmark rule

Let $F_t$ be wealth and $M_t=\sup_{s\le t}F_s$ its running maximum. A drawdown constraint with protection fraction $\lambda\in[0,1]$ is

$$
F_t\ge\lambda M_t.
$$

The source also discusses the stronger interest-adjusted floor

$$
F_t\ge\lambda\sup_{s\le t}F_s e^{r(t-s)}.
$$

Discounting wealth and the risky asset by the deterministic bank account converts that second formulation to a zero-interest problem. The analysis thereafter sets the cash return to one per period. Its growth criterion is the long-run logarithmic rate, expressed through either an almost-sure lower limit or the corresponding expected-log formulation discussed in the introduction. The regenerative construction below establishes an almost-sure rate using a ratio of expectations under finite cycle moments.

In the continuous-time comparison, the risky price is

$$
S_t=S_0\exp(at+\sigma B_t).
$$

Here $a$ is the drift of log price, not the arithmetic expected-return drift. The unconstrained long-only Kelly fraction is

$$
p^*=\left(\frac12+\frac{a}{\sigma^2}\right)^+\wedge1.
$$

For an interior solution, the corresponding growth rate is $(p^*)^2\sigma^2/2$; at $p^*=1$ it is $a$. The protected-cushion policy sets aside $\lambda M_t$ and invests fraction $p^*$ of the remaining wealth in the risky asset. At a record, the risky amount is $p^*(1-\lambda)M_t$. Below that record, it is $p^*(F_t-\lambda M_t)$. A new high resets the protected amount upward. This policy is the object extrapolated to discrete time, rather than a constant risky fraction of total wealth.

Now take independent identically distributed nonnegative, nonconstant risky gross returns $X_1,X_2,\ldots$ and define

$$
R(p,X)=1+p(X-1),\qquad 0\le p\le1.
$$

The unconstrained fraction maximizes

$$
p^*\in\arg\max_{0\le p\le1}\mathbb E\log R(p,X).
$$

For the counterexample $0<p^*<1$, and strict concavity gives a unique optimum. Its first-order condition is

$$
\mathbb E\frac{X-1}{1+p^*(X-1)}=0.
$$

This is an expectation under the actual return probabilities. It is not a risk-neutral pricing condition. Nonnegative $X$ and a risky fraction below one ensure positive cushion wealth even if the risky asset has a total loss.

## Regeneration at record wealth

Normalize wealth at the start of a cycle to one and hold its protected component $\lambda$ in cash. Let

$$
Q_n=\prod_{j=1}^n[1+p^*(X_j-1)],\qquad
\tau=\inf\{n\ge1:Q_n>1\}.
$$

Before this first strict crossing, wealth is

$$
F_n=\lambda+(1-\lambda)Q_n\le1.
$$

It remains at least $\lambda$, so the old running maximum is protected. At the crossing, wealth exceeds one; the next cycle starts from this new maximum. Its multiplicative wealth gain is

$$
Y=\lambda+(1-\lambda)Q_\tau.
$$

Independence of future returns gives independent identically distributed cycle pairs $(Y_j,\tau_j)$. When $\mathbb E|\log Y|<\infty$ and $0<\mathbb E\tau<\infty$, the strong law yields the cycle-time growth rate

$$
G_0=\frac{\mathbb E\log[\lambda+(1-\lambda)Q_\tau]}{\mathbb E\tau}.
$$

This is equation (3), p. 247. Both numerator and denominator matter. Maximizing an expected log gain per completed excursion while ignoring how long that excursion lasts does not generally maximize growth per unit of calendar time. The counterexample is designed to make the cycle length locally unchanged, so the derivative can be evaluated without omitting this issue.

An elementary boundary counterexample precedes the interior construction. If $X\ge1$ almost surely with a positive chance of a strict gain, all wealth can be invested in the risky asset without ever drawing down. Protecting a positive cash fraction unnecessarily reduces growth from $\mathbb E\log X$ to $\mathbb E\log[\lambda+(1-\lambda)X]$. The main construction is stronger because its risky asset can lose everything and its unconstrained optimum lies strictly inside the allowable interval.

## The perturbation and why it stays feasible

At the start of each new record cycle, use risky fraction $p^*+\varepsilon$ of the cushion. On every later step of that cycle, revert to $p^*$. Define

$$
Q_{n,\varepsilon}=[1+(p^*+\varepsilon)(X_1-1)]
\prod_{j=2}^n[1+p^*(X_j-1)]
$$

and let $\tau^\varepsilon$ be its first strict crossing above one. Take $\varepsilon>0$ small enough that $p^*+\varepsilon<1$. Then every cushion factor stays positive, and the same protected cash amount enforces the drawdown floor until the crossing. Once a new high is reached, the floor is reset. The perturbation therefore changes the allocation rule without weakening protection.

The new objective is

$$
G(\varepsilon)=
\frac{\mathbb E\log[\lambda+(1-\lambda)Q_{\tau^\varepsilon,\varepsilon}]}{\mathbb E\tau^\varepsilon}.
$$

Assume the unperturbed log factors lie on a lattice of spacing $\delta>0$. The paper proves, on pp. 248–249, that

$$
0<\varepsilon<(1-p^*)(1-e^{-\delta})
\quad\Longrightarrow\quad
\tau^\varepsilon=\tau^0
$$

path by path. If the first return exceeds one, both cycles end on the first step. If the first return is no greater than one, the perturbation reduces the cushion relative to the original path, so it cannot cross earlier. At the original crossing, however, $Q_{\tau^0}\ge e^\delta$, while

$$
\frac{Q_{\tau^0,\varepsilon}}{Q_{\tau^0,0}}
=1+\varepsilon\frac{X_1-1}{1+p^*(X_1-1)}
\ge1-\frac{\varepsilon}{1-p^*}>e^{-\delta}.
$$

It must therefore still exceed one at that same date. The strict lattice gap prevents an arbitrarily small allocation change from delaying the crossing. This is an exact finite-perturbation statement on the displayed interval, not merely a claim that the expected stopping time has zero derivative.

Holding the stopping time fixed now gives

$$
G'(0)=\frac{D}{\mathbb E\tau},
$$

$$
D=(1-\lambda)\mathbb E\left[
\frac{Q_\tau(X_1-1)}{[\lambda+(1-\lambda)Q_\tau][1+p^*(X_1-1)]}
\right].
$$

This is equation (5), p. 250. The derivative contains the end-of-cycle overshoot as well as the first-period return. The Kelly first-order condition alone does not force it to vanish because the additional overshoot weight is correlated with that return.

## Explicit two-outcome market

Choose any $\delta>0$ and set

$$
p^*=1-e^{-\delta},\qquad
a=\frac{e^{2\delta}-e^{-\delta}}{1-e^{-\delta}},
$$

$$
\Pr(X=a)=\gamma=
\frac{e^\delta(e^\delta-1)}{e^{2\delta}-e^{-\delta}},
\qquad \Pr(X=0)=1-\gamma.
$$

These expressions give $a>1$, $0<\gamma<1$, and $0<p^*<1$. At the Kelly fraction, the cushion gross return is exactly $e^{2\delta}$ on a gain and $e^{-\delta}$ on a loss. Its log increments are therefore $+2\delta$ and $-\delta$. Substituting these probabilities and payoffs into the first-order condition verifies that the specified $p^*$ is the interior log optimum.

The first crossing above zero in the cumulative log-cushion walk ends at either $\delta$ or $2\delta$. Write

$$
\Pr(Q_\tau=e^{2\delta})=q,\qquad
\Pr(Q_\tau=e^\delta)=1-q.
$$

The source's renewal argument yields

$$
q=\gamma+(1-\gamma)(1-q)q,
$$

$$
q=\frac{-\gamma+\sqrt{4\gamma-3\gamma^2}}{2(1-\gamma)}.
$$

The first term represents an immediate upward step. After an initial downward step, reaching the larger final overshoot requires first recovering to the appropriate intermediate level with the smaller overshoot and then making another larger overshoot. Both are fresh copies of the same ladder process. The admissible quadratic root lies strictly between zero and one.

A compact derivation makes the strict growth improvement transparent. Define

$$
Z=\frac{X_1-1}{1+p^*(X_1-1)},\qquad
h(y)=\frac{y}{\lambda+(1-\lambda)y}.
$$

The Kelly condition is $\mathbb EZ=0$. If the first outcome is a gain, $Q_\tau=e^{2\delta}$. Every smaller final overshoot occurs following an initial loss, for which $Z=-e^\delta$. Hence

$$
\mathbb E[Z h(Q_\tau)]
=e^\delta(1-q)[h(e^{2\delta})-h(e^\delta)].
$$

Since

$$
h'(y)=\frac{\lambda}{[\lambda+(1-\lambda)y]^2}>0
$$

for $0<\lambda<1$, it follows that

$$
G'(0)=\frac{(1-\lambda)e^\delta(1-q)}{\mathbb E\tau}
\left[
\frac{e^{2\delta}}{\lambda+(1-\lambda)e^{2\delta}}
-\frac{e^\delta}{\lambda+(1-\lambda)e^\delta}
\right]>0.
$$

This is a reconstruction of the source's final positivity argument, using its first-order condition and overshoot distribution. It establishes that for every fixed $\lambda\in(0,1)$ there is a sufficiently small positive perturbation that improves growth. It does not state that every perturbation below the stopping-time threshold improves growth, or that one perturbation size works uniformly for every protection fraction.

The binary log walk has bounded increments and strictly positive mean. Its expected first ascending-ladder time is finite; for this construction it can also be recovered from Wald's identity:

$$
\mathbb E\tau=\frac{1+q}{3\gamma-1}.
$$

The identity uses expected cumulative log gain $\delta(1+q)$ and expected one-step log gain $\delta(3\gamma-1)$. These moment conditions justify the regenerative growth calculation rather than leaving finiteness of the cycle denominator implicit.

## A reproducible numerical check

The paper provides an analytical counterexample rather than a numerical table. The following values are derived here to make the construction testable. Choose $\delta=\log2$ and $\lambda=1/2$. Then

$$
p^*=1/2,\quad a=7,\quad \gamma=4/7,\quad q=2/3,\quad \mathbb E\tau=7/3.
$$

The risky asset pays gross seven with probability $4/7$ and zero otherwise; the unperturbed cushion pays gross four or one-half. The benchmark cycle gain is $5/2$ for the larger overshoot and $3/2$ for the smaller. Thus

$$
G(0)=\frac{(2/3)\log(5/2)+(1/3)\log(3/2)}{7/3}
\approx0.31972094
$$

in natural-log wealth units per discrete period, and $G'(0)=4/105\approx0.03809524$ per unit change in the cushion allocation. This is not an annual return or a calibration to traded assets.

For $0<\varepsilon<1/4$, cycle durations remain identical. The three joint cases needed for exact evaluation have probabilities $4/7$, $2/21$, and $1/3$: immediate gain, initial loss with eventual large overshoot, and initial loss with eventual small overshoot. Their perturbed cushion terminal values are respectively $4+6\varepsilon$, $4(1-2\varepsilon)$, and $2(1-2\varepsilon)$. Applying $\lambda+(1-\lambda)Q$ and averaging its logarithm gives $G(0.01)\approx0.32006631$, a strictly positive increase. A simulation should match this calculation, preserve the protected cash subaccount, and count every elapsed period rather than treating each record cycle as one time unit.

## Source qualifications and boundaries of the result

The scanned formulas contain slips that should not be propagated into code. On p. 251 the reintroduced product defining $Q_n$ prints $1+p^*+p^*X_j$; consistency with every preceding definition and the $+2\delta,-\delta$ construction requires $1-p^*+p^*X_j$. The last expanded algebraic substitution on p. 252 also prints inconsistent exponential signs in several denominators. The preceding identity is safely checked directly as $\gamma(a-1)=(1-\gamma)e^{3\delta}$ from the Kelly first-order condition. The positivity reconstruction above avoids relying on the malformed substitution. These are derived consistency corrections, not a claimed published erratum.

The paragraph on p. 250 saying that $D$ is negative for sufficiently small perturbations should be read alongside its actual calculation: under the bounded one-step-up condition (6), the terminal overshoot is constant, so $D=0$ at zero; strict concavity makes the finite perturbation worse. A derivative defined at zero does not itself vary with the perturbation. Constant overshoots remove the covariance mechanism that drives the successful counterexample.

The floor is guaranteed in the stated discrete model with nonnegative risky gross returns, no borrowing beyond the allowed fraction, and a protected zero-interest cash account. Brokerage failures, margin obligations, costs taken from the protected account, and trading between observation dates are outside that model. The risky payoff is deliberately extreme. The proof establishes nonuniversality; it does not measure the loss from discretizing a realistic diffusion or tell a manager how often to trade.

The reusable conclusion is precise: an unconstrained Kelly fraction applied to a protected cushion is not automatically the discrete-time optimum. Record-state transitions and overshoot distributions are part of the control problem. A proposed implementation must optimize or verify its actual discrete dynamics, including the opportunity to alter risk at new highs, rather than invoking a continuous-time growth theorem as a substitute for that analysis.
