# Optimal trade execution and price manipulation in order books with time-varying liquidity

**Authors:** Antje Fruth, Torsten Schöneborn, and Mikhail Urusov. **Source version:** title page dated October 8, 2018, with arXiv stamp `1109.2631v1`, September 12, 2011; the PDF therefore contains differing document and repository dates. **Source file:** `Finance/OptimalExecution_Fruth_2018.pdf`, 42 pages. Page references use the printed/PDF pagination. **Type:** mathematical optimal-execution research with numerical illustrations, not an empirical calibration study.

## Problem and principal innovations

The paper studies how a trader should execute a fixed quantity when order-book depth and resilience change predictably over time. Depth determines how much a market order moves the best quote immediately. Resilience determines how quickly the displaced book replenishes. These are separate functions, so an attractive future trading period can arise from a deeper book, faster replenishment, or a combination of the two. Treating all liquidity variation as a single change of clock misses this distinction.

The first contribution is a two-sided book model in which trading widens the spread. In that model, predictable liquidity variation does not generate profitable round trips or make intermediate trades against the overall execution direction beneficial. The second contribution is a characterization of optimal purchases by a time-dependent boundary separating states in which the investor waits from states in which the investor buys. That boundary can become infinite, meaning no purchase is optimal at that time regardless of remaining quantity relative to current displacement.

The third contribution is a comparison with the apparently similar model that sets the spread to zero. Removing the distinction between bid and ask can introduce pathological strategies: buying to raise the common price and selling when the book becomes deeper, or including intermediate sales in a program whose overall purpose is to buy. The authors derive conditions separating profitable round trips, transaction-triggered manipulation, and ordinary monotone execution.

The comparison demonstrates that an optimal-control solution can be mathematically correct for a misspecified market and still recommend economically artificial trading. The endogenous spread is not a small numerical cost added after optimization; it changes which strategies can exploit the price state. The paper also supplies a constructive discrete-time algorithm, continuous-time existence and uniqueness results under stated regularity conditions, and explicit formulas for several liquidity paths.

## Market primitives and admissible trading

There is one risky asset and a finite horizon $[0,T]$. The investor must purchase $x\ge0$ shares by $T$; selling is symmetric. The investor is risk neutral and uses market orders. The model permits both continuous trading rates and block trades, including initial and terminal impulses. It does not impose a participation cap, discrete lot size, or a maximum instantaneous trade size (pp. 3–7).

Without the large trader, the best ask $A^u_t$ and best bid $B^u_t$ are martingales, with $B^u_t\le A^u_t$. The assumptions include sufficient integrability for expected execution costs and stochastic integration arguments. Bachelier prices, driftless geometric Brownian prices, and suitable jump martingales fit the framework. There is no predictive alpha or risk penalty rewarding early completion; changes in the unaffected price have zero expected timing benefit.

The book is block-shaped: its density is constant with respect to distance from the best quote. If its height is $q_t$, a purchase of $\xi$ shares immediately raises the ask by $\xi/q_t$. The inverse depth is split into constant permanent impact and transient impact,

$$
q_t^{-1}=\gamma+K_t,
$$

where $\gamma$ is the permanent linear-impact coefficient and $K_t>0$ is a deterministic time-varying transient-impact coefficient. Larger $K_t$ means less liquidity. The resilience rate $\rho_t>0$ is deterministic and integrable. Define the decay factor

$$
a(s,t)=\exp\left(-\int_s^t\rho_u\,du\right),\qquad s\le t.
$$

A buy of $\xi$ at time $s$ contributes $[\gamma+K_sa(s,t)]\xi$ to the ask at a later time $t$. Its effect on the bid is $\gamma[1-a(s,t)]\xi$. At the instant of execution, the ask jumps while the bid does not. Later the ask relaxes downward toward its permanent shift while the bid gradually moves upward toward that same shift. A sell has the symmetric effects on the two sides.

This cross-side rule is the important modeling choice. An investor cannot immediately sell at the elevated ask created by its own purchase. The transient part is paid through a wider spread. A zero-spread model would instead make the increased transaction price available on both sides, which can create a spurious benefit from reversing direction.

Let $\Theta_t$ and $\widetilde\Theta_t$ denote cumulative purchases and sales. They are adapted, bounded, nondecreasing, left-continuous processes with right limits, starting at zero. Net terminal acquisition satisfies $\Theta_{T+}-\widetilde\Theta_{T+}=x$. The convention $\Delta\Theta_t=\Theta_{t+}-\Theta_t$ records the trade at time $t$ after the pre-trade state. This matters because the cost of a block includes its own within-book price movement.

Writing $A_t=A^u_t+D_t$ and $B_t=B^u_t-E_t$, the ask displacement is

$$
D_t=D_0a(0,t)+\int_{[0,t)}[\gamma+K_sa(s,t)]\,d\Theta_s-\int_{[0,t)}\gamma[1-a(s,t)]\,d\widetilde\Theta_s.
$$

The bid-side downward displacement $E_t$ swaps purchases and sales in that expression. Initial displacements $D_0,E_0$ are nonnegative. The overall execution cost is purchase expenditure minus sale proceeds, using the average quote traversed by each block:

$$
C=\int_{[0,T]}\left(A_t+\frac{\Delta\Theta_t}{2q_t}\right)d\Theta_t-\int_{[0,T]}\left(B_t-\frac{\Delta\widetilde\Theta_t}{2q_t}\right)d\widetilde\Theta_t.
$$

For a single purchase this is $A_t\xi+\xi^2/(2q_t)$. The half factor is required by integrating through a block-shaped book; charging the entire block at either the initial or final quote would be a different model.

## Manipulation definitions and the reduction to monotone deterministic control

A classical price-manipulation strategy is a zero-net-position round trip with negative expected cost. Transaction-triggered manipulation is broader: a purchase program becomes cheaper when it includes intermediate sales, or a sale program becomes more profitable when it includes intermediate purchases. A model can have the second defect even without a profitable standalone round trip (pp. 7–10).

Proposition 3.4 proves that neither form exists in the dynamic-spread model under the basic assumptions. The proof compares a mixed buy/sell strategy with a pure purchase strategy formed by truncating cumulative purchases once the target is reached. The martingale price component depends only on the net target, the permanent component gives the same lower bound, and the spread/transient terms make reversing direction no cheaper. The economic content is that the trader cannot monetize its own quote displacement without paying the opposite side of the book.

For pure purchases, expected cost decomposes as

$$
\mathbb E[C]=A^u_0x+\frac\gamma2x^2+\mathbb E[J].
$$

The first term is the unaffected initial price times quantity. The permanent linear-impact term depends only on final quantity, not scheduling. All optimization therefore concerns transient cost $J$. Since the remaining coefficients are deterministic, randomizing the trading strategy or adapting it to unaffected martingale fluctuations cannot improve the minimum expected cost. The problem reduces to a deterministic, nondecreasing purchase schedule.

This reduction explains why the absence of a volatility parameter from the optimal schedule is not an oversight. Volatility would matter with risk aversion, a chance constraint, predictive returns, or stochastic liquidity, but none is in this objective. Similarly, the result that permanent impact does not affect timing is specific to linear permanent impact and a fixed terminal quantity. It should not be exported without checking those assumptions.

At an arbitrary starting time $t$, let initial transient displacement be $\delta\ge0$. The reduced state dynamics and cost are

$$
D_s=\delta a(t,s)+\int_{[t,s)}K_ua(u,s)\,d\Theta_u,
\qquad
J(t,\delta,\Theta)=\int_{[t,T]}\left(D_s+\frac{K_s}{2}\Delta\Theta_s\right)d\Theta_s.
$$

The value function $U(t,\delta,x)$ is the infimum of this cost over nondecreasing schedules that buy exactly $x$ shares. The paper first proves that splitting a block into simultaneous pieces leaves cost and final displacement unchanged. This consistency property rules out artificial savings merely from changing the bookkeeping of a trade at the same timestamp (p. 11).

## State scaling and the buy/wait boundary

Because impact is linear in quantity and cost is quadratic, simultaneous scaling of displacement and remaining quantity gives

$$
U(t,a\delta,ax)=a^2U(t,\delta,x).
$$

For $\delta>0$, define $y=x/\delta$ and $V(t,y)=U(t,1,y)$. Then $U(t,\delta,x)=\delta^2V(t,x/\delta)$. This reduces a three-variable value function to time and a single state ratio. The zero-displacement state is treated by continuity or an alternative scaling, since literal division by zero is not valid (pp. 11–12).

A purchase of $\xi$ changes the state from $(\delta,x)$ to $(\delta+K_t\xi,x-\xi)$. Thus trading lowers $x/\delta$, while waiting allows resilience to reduce $\delta$ and increase that ratio. The boundary $c(t)$ separates a buy region $x/\delta>c(t)$ from a wait region below it. When the boundary is finite and the current state is above it, the trade that moves exactly to the boundary is

$$
\xi^*=\frac{x-c(t)\delta}{1+K_tc(t)}.
$$

Below the boundary, the optimal immediate trade is zero. At the terminal time, $c(T)=0$ and all remaining shares must be purchased. The boundary need not decline smoothly toward maturity. Anticipated improvements in liquidity can make waiting more attractive later, and entire intervals can have $c(t)=\infty$.

The paper proves several useful structural properties before solving the problem. Cost is nondecreasing in remaining quantity, initial displacement, illiquidity, and the starting time, and nonincreasing in resilience. It is never optimal to finish the entire program strictly before the deadline: moving a sufficiently small amount of the final early block to $T$ benefits from some resilience while adding only a second-order block cost. This statement depends on the absence of risk aversion and predictive price drift (pp. 15–16).

A strong sufficient waiting condition compares the residual impact of a trade now with the immediate impact of trading later. If

$$
K_sa(s,t_2)>K_{t_2}\quad\text{for every }s\in[t_1,t_2),
$$

then buying anywhere in $[t_1,t_2)$ is suboptimal. Later liquidity improves enough to dominate any benefit from having already allowed a trade's impact to decay. With smooth inputs, $K'_t+\rho_tK_t<0$ is a local sufficient condition for an infinite boundary at time $t$ (pp. 17 and 36).

## Constructive discrete-time solution

For trading times $0=t_0<\cdots<t_N=T$, let $K_n=K_{t_n}$ and $a_n=a(t_n,t_{n+1})$. Trades $\xi_n\ge0$ sum to the target and obey

$$
D_{n+1}=a_n(D_n+K_n\xi_n),\qquad
J=\sum_{n=0}^N\left(D_n+\frac{K_n}{2}\xi_n\right)\xi_n.
$$

The normalized terminal value is $V_N(y)=y+K_Ny^2/2$. Backward dynamic programming gives

$$
V_n(y)=\min_{0\le\xi\le y}\left\{\xi+\frac{K_n}{2}\xi^2+a_n^2(1+K_n\xi)^2V_{n+1}\left(\frac{y-\xi}{a_n(1+K_n\xi)}\right)\right\}.
$$

The authors transform the control from trade size to the post-trade ratio $\eta=(y-\xi)/(1+K_n\xi)$ and define

$$
L_n(\eta)=\frac{1+2K_na_n^2V_{n+1}(\eta/a_n)}{(1+K_n\eta)^2}.
$$

This function decreases until a unique minimizer $c_n$, then increases, allowing $c_n=\infty$. The optimal post-trade ratio is $\min(y,c_n)$, and the original-state trade is the boundary formula above. Theorem 6.1 establishes unique optimal execution on any finite grid and shows that the normalized value function is continuously differentiable and piecewise quadratic (pp. 18–21).

An implementable recursion starts at the terminal quadratic, finds the minimum of $L_n$ on the nonnegative half-line, and sets

$$
V_n(y)=
\begin{cases}
\big[(1+K_ny)^2L_n(c_n)-1\big]/(2K_n),&y>c_n,\\
a_n^2V_{n+1}(y/a_n),&y\le c_n.
\end{cases}
$$

The piecewise-quadratic representation allows analytical derivative tests within segments, rather than requiring an unrestricted grid over both displacement and quantity. A numerical implementation must allow a minimum at infinity; imposing an arbitrary finite upper state bound can turn a genuine waiting interval into a spurious small purchase. It must also preserve the distinct terminal block instead of treating $T$ as just another interior step.

The discrete proof is constructive and supports the continuous-time result, but the paper does not give a universal discretization-error rate. Refining the time grid and verifying cost convergence is therefore an appropriate implementation check. Uniqueness on a finite grid does not justify assuming unrestricted smooth-input continuous-time uniqueness without its additional condition.

## Continuous-time existence and uniqueness

With merely bounded measurable $K$, a minimizing schedule need not exist. The paper gives a deliberately pathological example: $K_t=1$ at rational times and $K_t=2$ at irrational times, with constant resilience. Trading on increasingly fine rational grids approaches the value of the constant-$K=1$ problem, but no admissible schedule attains the required continuous trading component at that cheaper coefficient. This illustrates why regularity assumptions matter (p. 22).

Continuity of positive $K$ suffices for existence. The proof takes a minimizing sequence of monotone cumulative purchases, uses Helly compactness to extract a weakly convergent subsequence, and proves continuity of execution cost under that convergence. Terminal mass is retained, so a limiting terminal block is not accidentally lost. The continuous-time value function also has the buy/wait structure, obtained by passing from the discrete recursion to its limit (pp. 24–27).

Uniqueness follows under a stronger condition. If $K$ is absolutely continuous with derivative $K'_t$ and

$$
K'_t+2\rho_tK_t>0\quad\text{almost everywhere},
$$

the cost is strictly convex in the schedule. A useful identity makes the reason transparent:

$$
J(t,\delta,\Theta)=\frac12\left[\frac{D_{T+}^2}{K_T}-\frac{\delta^2}{K_t}+\int_t^T\frac{K'_s+2\rho_sK_s}{K_s^2}D_s^2\,ds\right].
$$

Positive weighting of squared displacement provides convexity. This identity includes jumps correctly; ignoring block-trade terms would generally spoil it. Appendix A supplies the integration-by-parts convention for the left-continuous cumulative trading processes used in the proofs.

The existence and structural theorems have broader scope than the closed-form examples. A continuous liquidity path can be handled by the discrete algorithm even when the sufficient smoothness and monotonicity conditions for explicit formulas fail. Conversely, a finite numerical optimizer returning an answer for discontinuous inputs does not prove the corresponding continuous-time infimum is attained.

## Zero-spread comparison and classical manipulation

The alternative model has one common bid/ask price $S^u_t+D_t$ and signed cumulative trading $X_t$, so buys and sells directly affect the same state:

$$
D_t=\delta a(0,t)+\int_{[0,t)}K_sa(s,t)\,dX_s.
$$

The schedule may have either sign, is of finite variation, and ends at $X_{T+}=x$. The cost retains the quadratic block convention. For this section the authors assume twice continuously differentiable $K$ and continuously differentiable resilience (pp. 27–28).

Manipulation is defined from zero initial displacement in the zero-spread model. With a nonzero known displacement, even a conventional resilient common-price model can offer a predictable reversion trade. That differs from the dynamic-spread setting, where nonnegative initial ask and bid dislocations do not provide the same opportunity to transact at the favorable side of a single displaced price.

If $K'_t+2\rho_tK_t<0$ at some time, a sufficiently short buy-then-sell round trip has negative cost. For one share bought at $t$ and sold at $t+\varepsilon$, cost is

$$
\frac{K_t+K_{t+\varepsilon}}2-K_ta(t,t+\varepsilon).
$$

Its first-order expansion is $\varepsilon(K'_t/2+\rho_tK_t)$, negative under the stated condition. The future book becomes deeper quickly enough that liquidation at the elevated common price is profitable. Rapidly rising illiquidity does not produce the symmetric pathology.

Because the profitable round trip can be multiplied by an arbitrary size and superimposed on any target program, the infimum of cost becomes $-\infty$. There is no finite optimal strategy. This is a model-consistency failure, not a prediction of unlimited real-world profit. Position limits could numerically bound the exploit while leaving the underlying misspecification intact (pp. 29–30).

## Explicit zero-spread optimum and transaction-triggered manipulation

Suppose instead that $K'_t+2\rho_tK_t>0$ everywhere. Define

$$
f_t=\frac{K'_t+\rho_tK_t}{K'_t+2\rho_tK_t},\qquad
C=\frac{f_0}{K_0}+\int_0^T\frac{f'_t+\rho_tf_t}{K_t}\,dt+\frac{1-f_T}{K_T},\qquad
\lambda=\frac{x+\delta/K_0}{C}.
$$

The normalization $C$ is strictly positive. The unique optimal signed schedule consists of an initial impulse, an interior rate, and a terminal impulse:

$$
\Delta X_0=\lambda\frac{f_0}{K_0}-\frac\delta{K_0},\qquad
dX_t=\lambda\frac{f'_t+\rho_tf_t}{K_t}\,dt,\qquad
\Delta X_T=\lambda\frac{1-f_T}{K_T}.
$$

The corresponding interior displacement is $D_t=\lambda f_t$, and the post-terminal displacement is $\lambda$. The formulas automatically integrate to the required final quantity. They arise by rewriting the cost as a quadratic functional of displacement, finding the stationary path under the quantity constraint, and showing every nonzero perturbation adds a strictly positive quadratic term (pp. 30–35).

Starting from $\delta=0$, there is no profitable standalone round trip under this positivity condition. Nevertheless, transaction-triggered manipulation occurs if and only if $f_0<0$ or $f'_t+\rho_tf_t<0$ somewhere. For a positive purchase target, the first condition makes the optimal initial trade a sale; the second creates an interior selling interval. The terminal coefficient remains positive because $f_T<1$.

When these signs are nonnegative, the zero-spread optimum is a pure purchase strategy and can also solve the dynamic-spread problem, provided initial displacement is not too high. The explicit dynamic-spread boundary is

$$
c(t)=\frac1{f_t}\left[\int_t^T\frac{f'_s+\rho_sf_s}{K_s}\,ds+\frac{1-f_T}{K_T}\right],\qquad t<T,
$$

with $c(T)=0$. A zero $f_t$ can produce an infinite boundary. For the explicit schedule starting at zero, the source requires $\delta\le x/c(0)$ so that its initial impulse is nonnegative. A state below the buying threshold instead requires waiting; blindly applying the signed formula would violate the dynamic-spread problem's proven monotonicity.

## Numerical illustrations and exact benchmark cases

The paper contains deterministic examples rather than estimation on market data. Figure 4 uses $T=1$, ten intervals, target $x=100$, zero initial displacement, and resilience $\rho=2$ or $10$. It compares three illiquidity paths: $K_t=0.7$, $K_t=1-0.6t$, and $K_t=1-2.4(t-0.5)^2$. The last has a relatively shallow book in the middle and deeper books at the endpoints. At low resilience the optimal schedule can avoid much of the middle interval; at high resilience, replenishment supports more distributed trading. These parameters are sufficient to reconstruct the qualitative experiment using the recursion (pp. 22–23).

For constant $K_t=\kappa$ and constant $\rho$, both models produce the familiar schedule

$$
\Delta\Theta_0=\Delta\Theta_T=\frac{x}{\rho T+2},\qquad
\frac{d\Theta_t}{dt}=\frac{x\rho}{\rho T+2}.
$$

The boundary is $c(t)=[1+\rho(T-t)]/\kappa$ for $t<T$, then jumps to zero at maturity. With $T=1$, $\rho=2$, and $x=100$, this means 25 shares initially, 50 shares spread uniformly through the interval, and 25 at the end. This numerical breakdown follows directly from the source formula. The schedule does not depend on the scale $\kappa$ when initial displacement is zero, although total costs and the state boundary do.

For exponential illiquidity $K_t=\kappa e^{\nu\rho t}$, the sign regimes become especially clear. When $\nu\ge-1$, neither model requires intermediate counter-direction trades. At $\nu=-1$, all shares are optimally purchased at $T$. When $-2<\nu<-1$, the zero-spread model has transaction-triggered manipulation, while the dynamic-spread model waits until $T$. For $\nu<-2$, the zero-spread model has profitable round trips and unbounded-below cost. The degenerate boundary $\nu=-2$ is not covered by the strict inequalities in the cited theorem and should not be classified by substitution into singular formulas (pp. 37–38).

The source also treats straight-line illiquidity $K_t=\kappa+mt$, requiring $m>-\kappa/T$. Neither manipulation form occurs under the explicit shared-solution condition $m\ge-2\rho\kappa/(3+2\rho T)$. Transaction-triggered manipulation occurs in the zero-spread model between that threshold and $-2\rho\kappa/(1+2\rho T)$; more negative admissible slopes produce classical manipulation. For part of the intermediate range, the dynamic-spread solution has no closed form in the paper and must be approximated numerically. The appendices verify the sufficient wait-until-terminal condition rather than filling that gap with an unsupported formula.

## Reproduction, applicability, and limitations

A reproduction should begin with the finite-grid model because its dynamics, cost, and terminal constraint are explicit. For each candidate schedule, independently compute cost from the original sum and, where smooth-input assumptions apply, compare with the displacement-based identity. Recover the constant-liquidity benchmark, check that trades sum to the target, and confirm nonnegative trades in the dynamic-spread model. For the zero-spread formulas, inspect initial and interior signs and compare the two-trade round-trip cost with the theoretical threshold.

The main missing ingredient for deployment is calibration, not mathematics. The paper supplies no estimates of depth or resilience from actual order-book data, no out-of-sample cost comparison, and no statistical uncertainty for its illustrative paths. The book is block-shaped, liquidity paths are known, and impact decays exponentially with one time-dependent recovery rate. It excludes stochastic liquidity shocks, alpha decay, inventory risk aversion, cross-asset effects, exchange fees, execution constraints, and strategic reactions outside the specified resilience mechanism.

The valuable practical insight is that depth and replenishment should be modeled separately and that a realistic treatment of both sides of the book is essential when allowing signed trades. A fitted optimizer that recommends sales during a buy program deserves a model-consistency check before being interpreted as a sophisticated execution insight. Within its assumptions, the paper provides a rigorous monotone execution policy and a reproducible numerical method; outside those assumptions, its thresholds serve as diagnostics and benchmarks rather than universal prescriptions.

## Additional diagnostics from the paper's examples

Figure 5 isolates transaction-triggered manipulation using $T=1$, $\rho=2$, $x=100$, and $\delta=0$, with $K_t=\sin(2.5t)+0.1$ in one case and $K_t=\sin(10t)+4$ in the other. The diagnostic plots show $K$, $K'+2\rho K$, and $f'+\rho f$, alongside the cumulative signed optimal position. The positive convexity coefficient can coexist with a negative trading-rate numerator. Consequently, the cumulative position can decline partway through a buy program, and in the second example can even become negative temporarily. This is a concrete demonstration that checking only whether a round trip has nonnegative cost is weaker than checking whether the optimal target execution remains monotone.

The corresponding test in the dynamic-spread model must be performed on the two quote processes, not by taking the signed solution and simply charging a constant spread afterward. The no-manipulation proof changes the feasible economic comparison: an intermediate sale receives the bid, whose response to previous buys differs from the ask's response. A post hoc fee might discourage some trades but would not reproduce the book dynamics that underpin Proposition 3.4.

The paper's state ratio also distinguishes an execution boundary from a standard portfolio no-trade band. Here the investor has a fixed remaining purchase obligation, and $x/\delta$ compares that obligation with current self-induced quote displacement. The waiting region does not express satisfaction with a long-run portfolio allocation. It expresses the value of letting existing impact decay or of reaching a more favorable future liquidity period. At the deadline the obligation remains binding, which explains the boundary's terminal jump and final block.

For constant inputs, increasing resilience shifts more of the quantity into continuous replenishment trading and reduces the two endpoint blocks. As $\rho T$ becomes small, each endpoint approaches half the total quantity; as it becomes large, each endpoint becomes small and interior trading dominates. These limiting conclusions follow from the explicit benchmark formula and provide useful checks on an implementation. They are not claims that actual markets permit arbitrarily high replenishment at a known deterministic rate. If observed depth or resilience estimates imply unrealistic endpoint blocks, the model needs execution-capacity constraints or a richer liquidity process before its schedule is operationally usable.

When testing sampled liquidity paths, derivative-based criteria require an interpolation convention. Piecewise-constant estimates have jumps and do not satisfy the smooth zero-spread theorem as stated; the finite-grid recursion remains the directly specified problem for such inputs.
