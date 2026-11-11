# Smoking adjoints: fast Monte Carlo Greeks

Michael Giles and Paul Glasserman, *Risk*, January 2006, pp. 88–92. Source: [AdjointDifferentiation_GilesGlasserman_2006.pdf](../../Finance/AdjointDifferentiation_GilesGlasserman_2006.pdf). PDF pages 1–5 correspond to printed pages 88–92. This note covers the complete article, including its numerical experiment and second-order extension; there is no separate appendix in the supplied file.

## Why this matters

A derivatives book can have one aggregate value but hundreds of risk inputs. Repricing after perturbing every input makes risk production substantially more expensive than valuation. Even a pathwise implementation that avoids repeated pricing may propagate an entire state-by-input sensitivity matrix. Giles and Glasserman show how to reverse the differentiation order: propagate the state forward, then propagate one payoff-gradient vector backward. For one output and many inputs, this removes an entire factor of the state dimension from the general dense calculation.

The contribution is computational. The adjoint and forward pathwise procedures produce the same derivative on each simulated path, subject to arithmetic roundoff and consistent implementation. Adjoint differentiation therefore does not reduce the sampling variance of a fixed pathwise estimator, repair a discontinuous payoff, or eliminate time discretization bias. Its economic value is the ability to calculate more risk sensitivities within a given computation budget. The paper brings a discrete-adjoint construction familiar from computational engineering into Monte Carlo Greeks, develops deltas and model-parameter sensitivities, and demonstrates especially efficient recursions for the Libor market model.

The relevant output count is the number of separately requested scalar values. A portfolio of thousands of trades is one output if only its total gradient is required. Requesting a separate gradient for every trade changes the complexity comparison. Forward differentiation can be preferable when many payoffs depend on the same simulated state but only a few input directions matter. This distinction is more useful than classifying the method simply as faster than finite differences.

## State dynamics and the derivative being estimated

The continuous state is an $m$-dimensional diffusion under the pricing measure, driven by a $d$-dimensional Brownian motion:

$$
d\widetilde X(t)=a(\widetilde X(t))\,dt+b(\widetilde X(t))\,dW(t).
$$

Here $a$ is an $m$-vector and $b$ an $m\times d$ matrix. The scalar function $g$ includes discounting, so the desired value is $E[g(\widetilde X(T))]$. With $h=T/N$, independent standard normal $d$-vectors $Z_{n+1}$, and all random draws held fixed during differentiation, Euler simulation gives

$$
X_{n+1}=X_n+a(X_n)h+b(X_n)Z_{n+1}\sqrt h=:F_n(X_n).
$$

This representation makes the simulation a composition of deterministic maps conditional on the random numbers. Define its one-step Jacobian by

$$
D_{ik}(n)=\delta_{ik}+h\frac{\partial a_i}{\partial x_k}(X_n)
+\sqrt h\sum_{\ell=1}^d\frac{\partial b_{i\ell}}{\partial x_k}(X_n)Z_{n+1,\ell}.
$$

The forward sensitivity matrix is $\Delta_{ij}(n)=\partial X_{n,i}/\partial X_{0,j}$. It obeys $\Delta(0)=I_m$ and

$$
\Delta(n+1)=D(n)\Delta(n),\qquad
\frac{\partial g(X_N)}{\partial X_0}=\nabla g(X_N)^\top\Delta(N).
$$

The pathwise Monte Carlo estimate averages the last expression over paths. Unbiasedness for the derivative of the simulated-model expectation requires interchanging differentiation and expectation. The article refers to smoothness and integrability conditions from Glasserman's book and stochastic-flow differentiability results in Protter. A Lipschitz payoff can be sufficient with suitable dynamics and an almost-sure derivative; continuity alone is not a general guarantee. A digital indicator, for example, does not become a valid ordinary pathwise Greek merely because a simulator can differentiate its code away from the threshold. The derivative of the discretized expectation must also be distinguished from the desired continuous-time derivative.

## Discrete adjoint and proof of equivalence

Initialize a column vector $V_N=\nabla g(X_N)$ and run

$$
V_n=D(n)^\top V_{n+1},\qquad n=N-1,\ldots,0.
$$

The resulting $V_0$ is the entire initial-state gradient. The proof is the chain rule with a different parenthesization:

$$
\nabla g(X_N)^\top D(N-1)\cdots D(0)
=V_0^\top.
$$

No approximation is introduced by this rearrangement. More generally, the invariant $V_n^\top\Delta(n)=V_{n+1}^\top\Delta(n+1)$ establishes equality at every step. It is an especially strong implementation check because it can be tested on individual paths, independently of Monte Carlo sampling error.

For dense unstructured maps, multiplying two $m\times m$ matrices costs $O(m^3)$ per step, whereas multiplying a transposed matrix by a vector costs $O(m^2)$. The full forward Jacobian therefore costs $O(Nm^3)$ against $O(Nm^2)$ for one adjoint. The state simulation and terminal payoff evaluation are additional costs. If only one initial-state direction is required, a forward tangent vector also costs $O(Nm^2)$; the full-matrix comparison should not be applied to that case.

Backward evaluation needs the forward path states and the random draws, or equivalent cached/reproducible information, at each step. The article proposes storing the current path, rather than all Monte Carlo paths simultaneously. State storage is $O(Nm)$, with extra storage for shocks and reusable intermediates depending on implementation. The paper does not develop checkpointing or quantify memory use. It also mentions a pragmatic hybrid: approximate only the terminal payoff gradient by finite differences, then propagate it adjointly. That preserves the saving from avoiding repeated state simulation but introduces the terminal finite-difference error and its tuning problem.

## Parameters entering every transition

For a vector of model parameters $\theta$, write $F_n(X_n,\theta)$ and let $B(n)=\partial F_n/\partial\theta$ at fixed $X_n$. With an initial state independent of $\theta$, the forward parameter Jacobian satisfies

$$
\Theta(0)=0,\qquad \Theta(n+1)=D(n)\Theta(n)+B(n).
$$

Unrolling the recursion and applying the same adjoint yields the complete parameter gradient:

$$
\nabla_\theta g(X_N)=\sum_{n=0}^{N-1}B(n)^\top V_{n+1}.
$$

The time index is essential: $B(n)$ changes the next state, so its contribution uses $V_{n+1}$, not $V_n$. The same $V$ used for deltas produces vegas; separate backward recursions for each volatility parameter are unnecessary. In an implementation with direct dependence of the payoff or initial state on $\theta$, the chain rule additionally contributes $\partial_\theta g$ and $(\partial_\theta X_0)^\top V_0$. These are extensions of the stated formula, whose assumptions set those terms to zero.

This formula computes sensitivity to the parameters supplied to the simulator. Sensitivity to market quotes would also require differentiating the calibration map from quotes to those parameters. No such calibration derivative or implied-volatility-surface construction is supplied in this article.

## Libor market model: exploiting the actual computation

Let $T_1,\ldots,T_{m+1}$ be tenor dates and $\delta_i=T_{i+1}-T_i$. The rate $L_i(t)$ applies to $[T_i,T_{i+1})$ and is frozen after its fixing date $T_i$. Set $\eta(t)$ by $T_{\eta(t)-1}\le t<T_{\eta(t)}$. The article uses the pricing-measure dynamics

$$
\frac{dL_i(t)}{L_i(t)}=\mu_i(L(t))\,dt+\sigma_i(t)^\top dW(t),\qquad
\mu_i(L)=\sum_{j=\eta(t)}^i\frac{\sigma_i^\top\sigma_j\,\delta_jL_j}{1+\delta_jL_j}.
$$

The volatility vector follows a time-to-maturity parametrization, $\sigma_i(t)=\sigma_{i-\eta(t)+1}(0)$. The example uses state-independent volatilities; a state-dependent volatility skew would add derivatives to both the drift and diffusion and invalidate an unchanged use of the simplified formulas below.

The simulation applies Euler to log rates, producing the multiplicative step

$$
L_i^+=L_i\exp\left[(\mu_i-\tfrac12\|\sigma_i\|^2)h+\sigma_i^\top Z\sqrt h\right],\qquad i\ge\eta.
$$

For settled rates $L_i^+=L_i$. Define the cumulative vector

$$
S_i=\sum_{j=\eta}^i\frac{\sigma_j\delta_jL_j}{1+\delta_jL_j},\qquad \mu_i=\sigma_i^\top S_i.
$$

Updating $S_i$ cumulatively evaluates all drifts in $O(md)$ operations, or $O(m)$ when the factor count is fixed. The dense Jacobian need never be formed. With $q_j=\delta_j/(1+\delta_jL_j)^2$, its active entries can be written compactly as

$$
D_{ij}=\mathbf 1_{\{i=j\}}\frac{L_i^+}{L_i}
+\mathbf 1_{\{\eta\le j\le i\}}L_i^+h\,\sigma_i^\top\sigma_jq_j.
$$

Settled rows instead contain the corresponding unit row. Thus the active block is lower triangular. The forward update for each input column $k$ is

$$
\Delta_{ik}^+=\frac{L_i^+}{L_i}\Delta_{ik}
+L_i^+h\,\sigma_i^\top\sum_{j=\eta}^i\sigma_jq_j\Delta_{jk}.
$$

A running prefix sum costs $O(md)$ per column, so all forward deltas cost $O(m^2d)$ per step. This is already better than a generic dense matrix product and is the appropriate forward comparator.

For the adjoint, form backward suffix sums $A_i=\sum_{j=i}^m L_j^+V_j^+\sigma_j$. Then

$$
V_i=\frac{L_i^+}{L_i}V_i^++hq_i\sigma_i^\top A_i,\qquad i\ge\eta,
$$

with $V_i=V_i^+$ for settled indices. All deltas now cost $O(md)$ per time step. Reusing $L_i^+/L_i$ and reciprocal denominators from the forward simulation avoids unnecessary exponential evaluations and divisions. This reuse, rather than the dimension count alone, helps explain the reported small runtime overhead.

For vegas, take the derivative with respect to the current $d$-vector $\sigma_j(t)$. The contribution accumulated at a step is

$$
\left(hS_j-h\sigma_j+\sqrt h Z\right)L_j^+V_j^+
+h\frac{\delta_jL_j}{1+\delta_jL_j}A_j.
$$

The first term differentiates the $j$th rate's diffusion, its negative half-variance drift, and its outer volatility in $\sigma_j^\top S_j$; the second differentiates every downstream $S_i$ containing $\sigma_j$. This includes the second contribution to the diagonal drift derivative and avoids a common factor-of-two omission. The suffix sums $A_j$ are already available from delta propagation. Add this vector to the initial-volatility bucket $j-\eta(t)+1$. Consequently the model's entire delta-plus-vega calculation retains $O(md)$ work per step.

The printed text on p. 91 bounds the volatility-bucket index using $N-\eta(nh)+1$, even though $N$ denotes time steps and $m$ denotes rates in the general setup. The valid active-rate range follows from $j\le m$ and is $1\le j-\eta+1\le m-\eta+1$. A general implementation should use the actual tenor dimension rather than silently identify it with the number of simulation steps.

The discounted caplet example is

$$
g=\left[\prod_{i=1}^m\frac{1}{1+\delta_iL_i(T_i)}\right]\delta_m\max\{0,L_m(T_m)-K\}.
$$

Frozen rates retain the fixing history, making this a terminal-state function. Its terminal gradient must differentiate the discount product as well as the intrinsic payoff. Ignoring the discount-factor derivatives computes a different Greek. The simulation grid should contain fixing dates; the article allows unequal step sizes to ensure this. More general path-dependent cash flows require an augmented state or adjoint contributions at their payment/evaluation dates, neither of which is worked out in this short paper.

## Second derivatives and the payoff boundary

Let $\Gamma_{ijk}(n)=\partial^2X_{n,i}/(\partial X_{0,j}\partial X_{0,k})$ and $E_{i\ell r}(n)=\partial^2F_{n,i}/(\partial X_{n,\ell}\partial X_{n,r})$. The second-order state recursion is

$$
\Gamma_{ijk}(n+1)=\sum_\ell D_{i\ell}(n)\Gamma_{\ell jk}(n)
+\sum_{\ell,r}E_{i\ell r}(n)\Delta_{\ell j}(n)\Delta_{rk}(n).
$$

For a fixed pair $(j,k)$, write the second sum as a vector $C^{jk}(n)$. Since $\Gamma^{jk}(0)=0$, the payoff Hessian entry becomes

$$
\frac{\partial^2g}{\partial X_{0,j}\partial X_{0,k}}
=\sum_{n=0}^{N-1}V_{n+1}^\top C^{jk}(n)
+\Delta_{\cdot j}(N)^\top\nabla^2g(X_N)\Delta_{\cdot k}(N).
$$

This is the same inhomogeneous-recursion reduction as the vega calculation. One still needs the first-order forward sensitivities and the local second derivatives of the transition. The article gives an $O(Nm^3)$ overall operation count for its adjoint-assisted second-order construction, versus an additional factor $m$ for carrying the full second-order state tensor forward. It does not claim that a full Hessian costs the same as a gradient.

Vanilla option payoffs ordinarily fail to be twice differentiable. Treating a call's second derivative as zero almost everywhere discards the moving exercise boundary and does not produce its gamma. The authors explicitly say their gamma expression requires replacing the payoff by a smooth approximation and identify the issue as ongoing research. The paper supplies neither a smoothing kernel nor a smoothing-bias/variance study. Its successful delta and vega timing experiment is therefore not evidence of a completed unbiased vanilla-gamma implementation.

## Numerical experiment and what was measured

The experiment in printed p. 92 uses one simulation step per quarterly Libor interval: $h=\delta=0.25$ years. Initial forward rates are all 5%, volatilities all 20%, and there is one Brownian factor. The test output is the value of a portfolio of 15 swaptions: five underlying swap tenors of 1, 2, 5, 7, and 10 years crossed with strikes of 4.5%, 5.0%, and 5.5%. All options have the same expiry in a given run; expiry ranges from $N=1$ to $80$ quarters. The rate curve must extend beyond option expiry through the longest underlying swap, so state dimension and expiry-step count are conceptually distinct.

Figure 4 compares the cost of all deltas, and all deltas plus vegas, relative to portfolio valuation cost. Its vertical axis is runtime ratio, not a pricing error or variance ratio. Approximate visual readings at $N=80$ are around 12 for forward deltas and 35 for forward deltas plus vegas, against roughly 1.5 for the two nearly coincident adjoint curves. At shorter maturities the forward curves start around 4 and 11 and rise approximately linearly; the adjoint curves remain approximately flat. These are graph readings, not tabulated precise benchmarks. The article's prose separately states that the additional sensitivity work can cost less than the original valuation; this should not be conflated with claiming a complete price-plus-Greeks run costs less than a price-only run.

The authors report a per-input forward cost of approximately 10% of portfolio valuation for a delta and 20% for a vega. Relative to central differences, which require two perturbed valuations per input before possible reuse, they describe the forward pathwise method as 10–20 times more efficient. This is a computational comparison within their implementation. The adjoint saves more when all inputs are requested because it does not pay that separate forward-column cost for every input. Adding vegas has almost no visible effect on adjoint runtime because the same backward variables and suffix sums serve both calculations.

There is no historical data universe, training window, return forecast, transaction-cost backtest, or statistical significance test. This is a synthetic model benchmark. The article omits the number of simulated paths, hardware and compiler details, timing repetitions and standard errors, exact portfolio notionals, and a complete swaption-payoff implementation. It provides no table of estimated prices or Greeks. Consequently its asymptotic operation counts and recurrence identities are reproducible from the paper, but the precise wall-clock curve is not fully reconstructable from the supplied information. Quarterly time steps are part of the benchmark; their valuation or sensitivity accuracy is not assessed by a grid-refinement experiment.

## Implementation sequence and scope of validation

For each independent path, first simulate rates, freezing settled components and caching states, shocks, growth factors, reciprocal denominators, and any payoff information. Evaluate the scalar portfolio payoff and its full terminal gradient. Run backward through the same time grid, accumulating parameter contributions with $V_{n+1}$ before overwriting it, then updating the adjoint. Average initial-state and parameter gradients across paths. Estimate Monte Carlo uncertainty from the cross-path sample covariance of the gradient vectors; the paper's algebra does not supply a numerical standard error automatically.

A meaningful correctness check compares adjoint and forward pathwise gradients on identical shocks. Agreement verifies the reorganization, not the legitimacy of exchanging expectation and differentiation. A common-random-number finite-difference check can then detect missing direct-payoff or calibration contributions, with a range of bump sizes to distinguish truncation error from sampling noise. A time-step convergence study addresses the separate discretization question. These are implementation checks derived from the estimator structure, not additional experiments reported by the authors.

The general theorem from algorithmic differentiation cited on p. 91 bounds reverse-mode arithmetic complexity by a small constant multiple of the original computation; the text quotes a factor of four. This does not promise a factor-four wall-clock limit for arbitrary software, memory traffic, externally coded payoffs, calibration routines, or heterogeneous output requests. The actual LMM saving relies on preserving its cumulative-sum structure. Forming every dense Jacobian and multiplying it afterward would forfeit much of that advantage.

The article's durable result is the adjoint identity and its careful realization in a structured financial simulator. It leaves payoff regularity, continuous-time accuracy, model calibration, and risk-output granularity as explicit responsibilities of the application.

## Source map

Printed pp. 88–89 introduce the estimator, Euler map, interchange condition, forward Jacobian, and LMM dynamics (equations 1–8). Printed p. 90 proves the discrete-adjoint relationship (equations 9–10) and displays the direction of data flow. Printed p. 91 gives model-parameter sensitivities (equations 11–12), efficient LMM reverse recursions, and the payoff Hessian decomposition (equation 13). Printed p. 92 completes the gamma discussion and contains the full numerical design, Figure 4, and references. Important antecedents named in the source are Glasserman and Zhao (1999) for forward LMM Greeks, Giles and Pierce (2000) for adjoints, Griewank (2000) for algorithmic differentiation, and Glasserman (2004) for pathwise regularity. Those works were not separately read for this note.
