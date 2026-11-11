# Performance Bounds and Suboptimal Policies for Multi-Period Investment

Stephen Boyd, Mark T. Mueller, Brendan O’Donoghue, and Yang Wang. *Foundations and Trends in Optimization* 1(1), 2014, 1–72. DOI: 10.1561/2400000001. [Source PDF](../../Finance/OptimalTrading_BoydMuellerOdonoghueWang_2014.pdf). All 75 supplied PDF pages were read, including appendices A–E and references. Page references below are printed pages; printed page 1 is PDF page 4.

## Why this matters

A dynamic trading policy may perform better than several convenient alternatives without being close to the best feasible policy. This monograph provides a way to measure that distance. It constructs a lower bound on the minimum expected cost of a multi-period portfolio problem, then compares the bound with simulated costs of feasible policies. If the difference is small, the policy is nearly optimal for the specified model. The bound is also useful when the difference is large: it limits how much improvement is possible, while making clear that the current heuristic has not been certified as close to optimal.

The contribution combines a linear stochastic-control formulation in dollar positions, quadratic underestimators of value functions obtained through semidefinite programming, and fast online policies derived from those approximations. Dynamic programming, convex portfolio optimization, approximate dynamic programming, and model predictive control are prior methods. The specific investment contribution is their combination with a computable performance certificate under nonquadratic costs and portfolio restrictions, demonstrated on 30-asset, 100-decision simulations.

The paper does not propose an alpha signal or test an investment anomaly. Its experiments are synthetic and use known, fixed return distributions. There are no market-sample dates, historical security universe, train/test split, or realized execution dataset. Its formal guarantee is conditional on the return model and cost specification. A small optimization gap says nothing by itself about forecast accuracy or whether the modeled opportunity exists in markets.

Several printed formulas need explicit reconciliation before implementation. The most consequential is a sign inconsistency between the inequality convention in appendix D and its final semidefinite condition. The simulation description also contains incompatible volatility ranges. This note distinguishes the mathematically reconstructed algorithm from the publication's reported results; it does not assert that the authors' software used the printed errors.

## State, timing, cash accounting, and objective

At the beginning of periods $t=0,\ldots,T$, the state $x_t\in\mathbb R^n$ contains each asset's dollar value at a reference price, which may be the midpoint. Negative entries are short positions. A trade $u_t\in\mathbb R^n$ is positive for a purchase and negative for a sale, also measured in reference-price dollars. The post-trade position is $y_t=x_t+u_t$. Gross cash put into the portfolio is $\mathbf1^Tu_t$; costs are additional cash outflows.

The position is held through the next return realization:

$$
x_{t+1}=R_{t+1}y_t,\qquad R_{t+1}=\operatorname{diag}(r_{t+1}),\qquad t=0,\ldots,T-1.
$$

Here $r_{t+1}$ is a vector of gross returns, so a value of 1.01 represents a 1% simple return. The trade at $t$ cannot depend on that future realization. Returns are independent across periods, with known, potentially time-varying distributions, means $\bar r_t$, and covariance matrices $\Sigma_t$. Cross-asset correlation within each period is allowed. The formal independence assumption excludes return momentum, mean reversion, and state-dependent volatility dynamics such as GARCH. The abstract's reference to arbitrary time-varying distributions does not remove this assumption.

A Markov policy is $u_t=\phi_t(x_t)$. Given the independent exogenous return process and the stated objective, history need not be included separately in the state. The initial position $x_0$ is fixed. A cash asset may be included, but it is unnecessary because external cash entering and leaving the portfolio is tracked directly. This is not automatically a self-financing wealth-maximization problem with a fixed initial capital budget. For example, a total-value floor can force a new cash injection after a loss. A mandate that cannot accept such injections needs additional modeling.

Let $\mathcal C_t$ be the nonempty closed convex set of allowed post-trade positions, and $\psi_t(x,u)$ a closed convex transaction/position cost. The stage cost is

$$
\ell_t(x,u)=\mathbf1^Tu+\psi_t(x,u)+I_{\mathcal C_t}(x+u),
$$

where the indicator is zero on the set and positive infinity outside it. The optimization is

$$
J^*=\inf_{\phi_0,\ldots,\phi_T}E\left[\sum_{t=0}^{T}\ell_t(x_t,\phi_t(x_t))\right].
$$

Smaller cost is better; negative cost is positive net revenue. A deterministic discount factor may be incorporated in stage costs. Risk penalties can be virtual internal charges, so the objective then represents risk-adjusted cost, not solely realized cash expenditure. There are $T+1$ trading decisions but only $T$ intervening return realizations. The last decision can impose liquidation, $y_T=0$, or another fixed terminal portfolio.

The paper assumes the required expectations exist and does not establish general existence and boundedness conditions. This matters when cash can be injected freely and profitable positions can grow without sufficient risk, impact, or position limits. Convexity alone does not guarantee a finite optimum or an attained minimizer.

## The cost and constraint families

The dollar-state formulation preserves linear dynamics and makes many practical restrictions convex. Position bounds are $x_t^{\min}\leq y_t\leq x_t^{\max}$; long-only means $y_t\geq0$. Sector exposures have $s_t^{\min}\leq F_ty_t\leq s_t^{\max}$, with exact neutrality imposed by linear equalities. A total-value floor is $\mathbf1^Ty_t\geq v_t^{\min}$. Proportional holdings limits remain linear when written $y_t\leq\alpha_t\mathbf1^Ty_t$.

A short-position limit relative to net portfolio value is

$$
\mathbf1^T(y_t)_-\leq\eta_t\mathbf1^Ty_t,\qquad (y)_-=\max(-y,0).
$$

For positive net value this implies short/long exposure at most $\eta/(1+\eta)$ and gross/net leverage at most $1+2\eta$. Thus the experiment's $\eta=0.3$ is a 30% short/net limit and a 1.6 gross/net limit, not gross leverage of 0.3. At $\eta=0$ the condition is long-only. Another permitted restriction directly caps $\|y_t\|_1$ relative to externally specified assets under management.

A concentration limit can cap the sum of the $p$ largest positions by a fraction of net value. The sum of largest entries is convex and has a polyhedral epigraph. Risk restrictions include $y_t^T\Sigma_{t+1}y_t\leq\gamma_t$, with $\gamma_t$ in squared dollars, and the scale-relative condition

$$
\|\Sigma_{t+1}^{1/2}y_t\|_2\leq\delta_t\mathbf1^Ty_t.
$$

The latter is a second-order-cone constraint, with dimensionless $\delta_t$. Intersecting variance constraints from multiple candidate covariance matrices gives a convex robust risk limit. More general expected convex loss measures also fit the abstract convex formulation, but their evaluation can require simulation or additional approximation; they are not automatically covered by the simplest quadratic matrix construction.

Transaction and position costs can combine proportional trading costs $\kappa_t^T|u_t|$, asymmetric buy/sell rates, quadratic impact $s_t^T u_t^2$, convex three-halves-power impact, piecewise-linear order-book costs, short fees $c_t^T(y_t)_-$, and risk penalties. A variance penalty is $\lambda_ty_t^T\Sigma_{t+1}y_t$, with $\lambda_t$ measured in inverse dollars; a standard-deviation penalty has a dimensionless rate.

Because trades are dollar values, $\kappa$ must be a cost fraction per dollar traded. The text describes it as a half-spread; dimensional consistency requires a relative half-spread when prices and $u$ are in dollars. Quadratic impact coefficients have inverse-dollar units. These costs represent contemporaneous execution costs. The authors explicitly exclude multi-period price impact: trading does not alter future return distributions or create a transient-impact state.

Fixed fees for any nonzero trade, minimum nonzero holdings, integer lots, and volume discounts can be nonconvex and fall outside the core formulation. Quadratic costs with only affine equality constraints form the exactly soluble quadratic case. Quadratic plus convex piecewise-linear costs and affine inequalities are QP-representable. Quadratic risk constraints generally require conic optimization rather than an ordinary QP. This distinction determines which online solver can actually execute the policy.

## Exact dynamic programming and the two tractable cases

Set $V_{T+1}=0$. The Bellman recursion and optimal action are

$$
V_t(x)=\inf_u\left\{\ell_t(x,u)+E[V_{t+1}(R_{t+1}(x+u))]\right\},
$$

$$
\phi_t^*(x)\in\arg\min_u\left\{\ell_t(x,u)+E[V_{t+1}(R_{t+1}(x+u))]\right\},\qquad J^*=V_0(x_0).
$$

At the terminal date the continuation term is zero, so no additional return draw is needed. The Bellman operator is monotone: increasing a continuation function pointwise cannot decrease the minimized objective. It also preserves convexity because affine composition, expectation, addition, and partial minimization preserve convexity. The resulting value functions are convex, but ordinarily cannot be represented or computed tractably in many dimensions.

For implementation, use one consistent quadratic convention:

$$
h(x)=\frac12x^TPx+p^Tx+c,\qquad P\succeq0.
$$

Appendix A implies

$$
E[h(Ry)]=\frac12y^T\{P\circ(\Sigma+\bar r\bar r^T)\}y
+(p\circ\bar r)^Ty+c,
$$

where $\circ$ is the elementwise product. Only the first two return moments enter. The quadratic term remains positive semidefinite by the Schur product theorem. Higher return moments can still matter for a nonquadratic policy's realized performance; this exact expectation result applies to quadratic continuation functions.

In the exactly quadratic case, adding stage cost and minimizing over trades subject to affine equalities preserves quadratic value functions. Write the action-dependent objective as $\frac12u^TCu+x^TBu+c_u^Tu$ plus terms independent of $u$, and equality $Fx+Gu=h$. The necessary and sufficient KKT system, assuming feasibility and an attained minimum, is

$$
\begin{bmatrix}C&G^T\\G&0\end{bmatrix}
\begin{bmatrix}u\\\nu\end{bmatrix}
=\begin{bmatrix}-B^Tx-c_u\\h-Fx\end{bmatrix}.
$$

A nonsingular system gives an affine action $u=J_tx+k_t$. With a singular system, a pseudoinverse produces a solution only when the right side is in its range; the existence assumption is essential. Substituting the affine action updates the quadratic value coefficients. This supplies a backward algorithm rather than a discretization of the state space.

Appendix B prints the lower right-hand side as $-h-Fx$ even though its stated constraint is $Fx+Gu=h$. The formula above follows directly from that constraint. Likewise the publication writes quadratics as one half of a homogeneous block form with bottom-right coefficient $q$, which gives constant $q/2$, but p. 29 expands the objective with constant $q$. Using $c$ and bottom-right entry $2c$ throughout avoids that factor-of-two ambiguity. These are explicit reconciliations, not silent changes to the source.

The second exact case permits arbitrary convex post-trade costs but no cost depending separately on $u$. Write $\psi_t(y_t)$ and collect cash flows across time. With $\bar r_{T+1}=0$ as a terminal bookkeeping convention,

$$
J=-\mathbf1^Tx_0+\sum_{t=0}^T E\left[(\mathbf1-\bar r_{t+1})^Ty_t+\psi_t(y_t)+I_{\mathcal C_t}(y_t)\right].
$$

Each date is then an independent single-period convex optimization over $y_t$. If $y_t^*$ minimizes that date's objective, rebalance fully by $u_t=y_t^*-x_t$. The ability to reset positions without trading cost removes the intertemporal coupling. This result depends on the stated cash-flow and constraint structure; it is not a general theorem that every frictionless multi-period utility problem is myopic.

## Constructing a certified lower bound

Choose convex quadratic functions $W_t$ and set $W_{T+1}=0$. Enforce Bellman inequalities

$$
W_t(x)\leq\inf_u\{\ell_t(x,u)+E[W_{t+1}(R_{t+1}(x+u))]\}.
$$

Backward monotonicity then proves $W_t\leq V_t$ and hence $J^{lb}=W_0(x_0)\leq J^*$. The condition must hold for every feasible state-action pair, not merely along sample trajectories. This global aspect distinguishes the certificate from a regression fit to simulated value targets.

For a feasible policy with true expected cost $J^\pi$,

$$
J^{lb}\leq J^*\leq J^\pi,\qquad 0\leq J^\pi-J^*\leq J^\pi-J^{lb}.
$$

The last difference is an upper bound on suboptimality. Since the experiments estimate $J^\pi$ by Monte Carlo, their displayed gaps inherit sampling uncertainty. A rigorous confidence statement about the gap must include that uncertainty and the numerical feasibility tolerance of the semidefinite solution.

The matrix construction is most transparent with quadratic stage costs. Let $z=(x,u,1)$ and represent $\psi=\frac12z^TH_\psi z$, with blocks $A,B,C,a,b,d$. Let $W_t(x)=\frac12x^TPx+p^Tx+c$ and next-period coefficients $P^+,p^+,c^+$. Define

$$
K=P^+\circ(\Sigma+\bar r\bar r^T),\qquad k=p^+\circ\bar r.
$$

The Bellman residual $F(x,u)=\mathbf1^Tu+\psi(x,u)+E[W_{t+1}(R(x+u))]-W_t(x)$ has matrix

$$
H_F=\begin{bmatrix}
A+K-P&B+K&a+k-p\\
B^T+K&C+K&b+\mathbf1+k\\
(a+k-p)^T&(b+\mathbf1+k)^T&d+2(c^+-c)
\end{bmatrix}.
$$

For a post-trade quadratic constraint $g_i(y)=\frac12[y;1]^TG_i[y;1]$, let $\widetilde G_i$ be its matrix after substituting $y=x+u$. A sufficient condition for $F\geq0$ whenever $g_i\leq0$ is

$$
H_F+\sum_i\lambda_i\widetilde G_i\succeq0,
$$

with $\lambda_i\geq0$ for inequality constraints and unrestricted multipliers for equality constraints. Indeed, global nonnegativity of $F+\sum_i\lambda_i g_i$ implies $F\geq-\sum_i\lambda_i g_i\geq0$ on the feasible set. This is the S-procedure. With multiple constraints it is generally sufficient, not necessary, and therefore introduces conservatism in addition to the restriction to quadratic underestimators.

The source's appendix C uses constraints $f_i\geq0$ and correctly subtracts their multiplier matrices. Appendix D switches to $g_i\leq0$ but equation (D.1) retains the subtractive sign. For its stated convention, that is not a valid sufficient condition. A scalar counterexample is $g(y)=y^2-1\leq0$ and $F(y)=y^2-1$: $F-g=0$ passes the printed matrix condition with multiplier one, yet $F(0)=-1$. The additive form above follows from the elementary implication and should be used if constraints retain appendix D's sign convention. This does not establish how the published numerical code represented constraints.

The offline SDP maximizes $W_0(x_0)$ over all quadratic coefficients and multipliers, subject to these LMIs at every date and $P_t\succeq0$. All coefficients enter affinely, and the initial-state objective is linear in them. Piecewise-linear costs can be represented using epigraph variables, after which the same nonnegativity construction applies in the enlarged decision vector. For example, $v\geq u$, $v\geq-u$ represents $|u|$ in a minimized positive-cost epigraph. The value function remains a function of $x$, not the auxiliary variables. Arbitrary convex functions without a suitable finite representation need further approximation; the basic displayed LMI should not be claimed as a universal exact encoding.

## From the bound to a trading policy

Approximate dynamic programming replaces the unavailable $V_{t+1}$ by the computed quadratic $W_{t+1}$ while retaining the actual stage costs and constraints:

$$
\phi_t^{ADP}(x)\in\arg\min_u\left\{\ell_t(x,u)+E[W_{t+1}(R_{t+1}(x+u))]\right\}.
$$

Equation (5.1) in the supplied PDF prints the continuation subscript $t$ rather than $t+1$ despite the exact Bellman recursion and the statement that exact value functions recover optimality. The displayed policy here follows the Bellman timing. At each online step, compute the quadratic continuation coefficients from the stored next-date matrix and return moments, solve the constrained convex problem, execute its trade, observe the new state, and repeat. Terminal liquidation must be included explicitly.

For QP-representable stage costs this is a small parametric QP. Under the usual existence and selection conditions, its solution is piecewise affine in the current position. Enumerating every polyhedral region can work for very small portfolios, but region counts grow rapidly; the paper suggests roughly five assets as a practical range for explicit region enumeration. Solving the QP online avoids storing that full partition.

Proportional costs create a no-trade region. Suppose the smooth part of the objective at $u=0$ has gradient $g(x)$, and buy/sell costs are $\kappa_+^Tu_++\kappa_-^Tu_-$. With no additional constraints and smooth remaining terms, zero trade is optimal precisely when

$$
-g(x)\in[-\kappa_-,\kappa_+].
$$

Here $g$ includes the continuation gradient $Kx+k$. If this marginal-value map is continuous and its range intersects the rectangle's interior, the no-trade set has nonempty interior. This is a conditional statement, not a guarantee that every constrained problem has a substantial no-trade region. With active position constraints, the relevant normal-cone contribution must also enter the optimality condition. The appendix proposes checking this criterion first and skipping the solver when zero trade is optimal, reducing average computation but not worst-case latency.

A lower value-function approximation need not yield a near-optimal policy everywhere. The SDP emphasizes the bound at the specified $x_0$, while the induced policy visits many states. The paper offers no general small-gap theorem. Performance evaluation against the computed bound is therefore an essential part of using the policy, rather than a redundant final check.

## Model predictive control and its computational tradeoff

Certainty-equivalent MPC replaces future returns by their means and solves a deterministic planning problem from the current state:

$$
\min_{z_\tau,v_\tau}\sum_{\tau=t}^{T}\ell_\tau(z_\tau,v_\tau),\qquad
z_t=x_t,\quad z_{\tau+1}=\operatorname{diag}(\bar r_{\tau+1})(z_\tau+v_\tau).
$$

Execute only $v_t$, then replan after observing the next state. MPC is thus a feedback policy, even though each planning problem uses a single deterministic return path. Risk penalties and constraints can still contain covariance estimates; replacing stochastic dynamics by means does not delete all risk terms. It does omit the effect of uncertainty on the continuation plan and future adaptation.

A generic dense solve can scale cubically in the remaining horizon, while exploiting block structure reduces the leading operation count to order $(T-t)n^3$ per decision. Over an entire horizon that is order $T^2n^3$, compared with order $Tn^3$ for quadratic ADP after offline synthesis. These are scaling descriptions, not guaranteed wall-clock times for every solver or constraint family.

Truncated MPC looks ahead $M$ periods and adds a terminal approximation $W_{t+M}(z_{t+M})$. A better terminal approximation can permit shorter lookahead. Near the true terminal date, the remaining original problem and its liquidation constraint must be used. This creates a continuum between greater offline value-function work and greater online planning work.

MPC readily accepts revised forecasts by replacing the mean-return inputs at each solve. The formally analyzed ADP policy may require a new SDP when return moments change. The authors explicitly state that adapting to real-time signals is outside the formal model; repeatedly inserting revised forecasts is a practical heuristic, not an extension of the original bound to an unspecified joint signal-return process.

## The synthetic experiment and a replication obstacle

All five examples have $n=30$, $T=99$, zero initial holdings, and zero terminal post-trade holdings. They share an iid multivariate lognormal return process:

$$
\log r_t\sim N(\mu,\widetilde\Sigma),\qquad
\bar r_i=\exp(\mu_i+\widetilde\Sigma_{ii}/2),\qquad
\Sigma_{ij}=\bar r_i\bar r_j(\exp(\widetilde\Sigma_{ij})-1).
$$

To generate correlation, draw an $n\times n$ matrix $Z$ of independent standard normals, form $Y=ZZ^T+\zeta\mathbf1\mathbf1^T$, and normalize $Y$ to unit diagonal. Choose positive $\zeta$ so off-diagonal correlations span approximately $-0.3$ to $+0.9$. Draw log means independently from $N(0,0.03^2)$. The reported gross means range from 0.95 to 1.08.

The volatility recipe is internally inconsistent. Printed p. 39 says log-return standard deviations are drawn uniformly from $[0,0.01]$, then says resulting simple-return standard deviations range from 0.03 to 0.10. With the stated mean range, the lognormal identity implies a maximum simple-return standard deviation of $1.08\sqrt{\exp(0.01^2)-1}\approx0.0108$. The two ranges cannot both describe the same draws. The text could have meant a different upper bound or a variance rather than a standard deviation, but neither repair is specified. Exact reproduction requires the original realized covariance or an authoritative correction, along with the random seed and chosen $\zeta$, none of which are supplied here. The simulations below are therefore reported findings, not independently reproduced numbers.

For the quadratic case, costs are $s^Tu^2+\lambda y^T\Sigma y$, with no nonterminal restrictions. The other four cases add $c^Ty_-+\kappa^T|u|$. The coefficient $\lambda$ is 0.5; asset-specific $s_i,\kappa_i,c_i$ are drawn uniformly from $[0,1]$, $[0,0.1]$, and $[0,0.05]$. The restrictions are, respectively, none; long-only; short/net limit $\eta=0.3$; and neutrality to the two eigenvectors associated with the largest eigenvalues of $\Sigma$. All parameters remain constant through the horizon apart from terminal liquidation.

The period duration and actual security identities are not specified because this is an artificial control benchmark. A 10% proportional cost upper bound and the stated return means should not be interpreted as a calibrated daily equity market. The cost terms were chosen to contribute materially to the objective, testing the optimization method rather than estimating realistic market capacity.

## Reported performance, uncertainty, and economic interpretation

Table 7.1 reports total expected cost over the 100 decisions in the model's dollar units. ADP means use 50,000 paths per example; MPC means use 5,000. Table 7.2 reports standard deviations of total path cost, not standard errors of the estimated mean.

| Case | Lower bound | ADP mean | MPC mean | ADP path SD | MPC path SD |
|---|---:|---:|---:|---:|---:|
| Quadratic | -450.1 | -450.0 | -444.3 | 30.9 | 40.3 |
| Unconstrained, full costs | -132.6 | -131.9 | -130.6 | 9.6 | 9.9 |
| Long-only | -41.3 | -41.0 | -40.6 | 7.1 | 7.2 |
| Leverage limit | -87.5 | -85.6 | -84.7 | 9.8 | 9.9 |
| Sector neutral | -121.3 | -118.9 | -117.5 | 8.9 | 9.9 |

For the quadratic problem, the bound is the exact optimum and ADP is the exact optimal policy. The 0.1 difference is consistent with simulation error: $30.9/\sqrt{50000}\approx0.138$. MPC's mean standard error is $40.3/\sqrt{5000}\approx0.570$. For the four nonquadratic cases, ADP mean standard errors derived from the table are approximately 0.043, 0.032, 0.044, and 0.040; MPC mean standard errors are about 0.140, 0.102, 0.140, and 0.140. Independent paths justify these standard-error calculations; the paper also reports repeating simulations with different seeds and agreement to roughly three significant figures.

The nonquadratic ADP gaps to the bound are 0.7, 0.3, 1.9, and 2.4 cost units. Relative to the magnitude of the bound these are about 0.53%, 0.73%, 2.17%, and 1.98%. These percentages are calculations from the displayed table, not annual returns or Sharpe improvements. The largest corresponding MPC gap is 3.8 in the sector-neutral case. All policies have strongly negative expected cost in these examples, but their objective includes a risk charge and permits external funding. Calling the numbers investment returns would require a capital denominator and cash-flow convention absent from the experiment.

Table 7.3 shows why simpler approximations can fail. Ignoring trading costs when constructing a policy yields realized full-cost objectives of $2.1\times10^6$, 864.5, 4525, and $2.1\times10^6$ for the unconstrained, long-only, leverage, and sector-neutral cases. The corresponding cost-free lower bounds are -4405, -70.6, -241.4, and -4391. Using value functions from the relaxed quadratic problem gives the common bound -450.1, but realized costs 59.2, 162.3, 219.5, and 75.6. All these policy objectives exceed zero, whereas never trading is feasible and costs zero. They are worse than inactivity under the specified risk-adjusted objective. This comparison demonstrates the danger of ignoring future nonquadratic costs; it does not establish dominance over every alternative ADP architecture.

Table 7.4 makes the economics visible. In the leverage-limited case, average per-decision gross cash flow is -2.03, with risk cost 0.54, quadratic trading cost 0.35, short fee 0.18, and proportional trading cost 0.11. Their rounded sum is about -0.85, consistent with total cost -85.6 over 100 decisions. Mean long and short positions are 52.66 and 12.03; mean gross exposure is 64.7. Ratios of average exposures need not equal average leverage ratios. In the unconstrained full-cost case, the corresponding gross flow is -3.82 and the four cost components are 0.29, 1.03, 0.96, and 0.22. All modeled costs matter.

Figure 7.3 shows funds being committed during roughly the first 12 steps, revenue being extracted thereafter, and complete liquidation at the end. The leverage ratio commonly reaches its 0.3 limit. Trading costs are elevated during initial construction and final liquidation; risk charges rise as exposure is accumulated and fall as it is unwound. The histogram in Figure 7.1 spreads on both sides of the lower bound: that bound constrains expected cost, not every realized sample path. Favorable individual paths can produce costs below it without contradicting the theorem.

## Robustness experiments and computational evidence

For mean misspecification, the authors keep the nominal policy and run ten additional parameter perturbations, each with 5,000 paths. The log-return mean changes to $\mu+\delta$, with each $\delta_i$ uniform on $[-0.003,0.003]$. Some near-zero means change sign. Table 7.5 gives the worst mean cost among these ten scenarios: -425.1 for the quadratic case, -123.4 unconstrained, -38.2 long-only, -80.3 leverage-limited, and -110.8 sector-neutral, versus nominal values -450.0, -131.9, -41.0, -85.6, and -118.9. This is a finite random sensitivity exercise, not a worst-case guarantee over all distributions or all allowed perturbations. The nominal bound need not remain valid when moments change.

For distributional shape, log returns are drawn from a mixture: probability 0.8 uses $N(\mu_1,\widehat\Sigma)$ and probability 0.2 uses $N(\mu_2,10\widehat\Sigma)$. Parameters are selected to match the original gross-return mean and covariance. The paper does not give the realized mixture parameters or a unique moment-matching algorithm. Average return kurtosis rises from 3.1 to 8.8. Across 5,000 paths, reported costs become -450.6, -132.0, -41.0, -85.5, and -118.8, nearly unchanged from nominal. Because first two moments are held fixed, the computed quadratic bound remains unchanged under the independent-return assumptions. Similar mean performance does not prove unchanged tail risk, liquidation stress, or drawdowns; those statistics are not reported.

Computation used a 3.4 GHz Intel Xeon running Linux. CVX with SeDuMi solved the long-only bound SDP, whose transformed form had 474,100 variables and 59,096 constraints, in about 24 minutes. The online ADP QP is reported as 30 variables and 30 constraints before conversion, or 90 variables and 122 constraints in standard form. A CVXGEN custom solver took about 300 microseconds, making a 100-step path about 30 milliseconds. Fifty thousand paths took around 25 minutes serially or slightly over three minutes on eight cores. These are historical, instance-specific implementation measurements.

The initial long-only MPC problem had 18,243 variables and 9,052 constraints after conversion. A specialized ADMM solver took about 88 milliseconds, compared with over three minutes using the general CVX route. Later MPC problems shrink with the remaining horizon. Solver accuracy, warm starts, stopping tolerances, and detailed generated instances are not fully specified, so the timings do not establish a portable latency guarantee. They do substantiate the computational division: expensive offline synthesis can support fast repeated online optimization and millions of simulation solves.

## What a faithful reimplementation must preserve

A reconstruction should keep the cash-flow signs, gross-return convention, decision count, terminal liquidation, and full stage costs consistent across bound construction and policy evaluation. It should use the corrected sign convention for semidefinite multipliers and a single quadratic constant normalization. The equality KKT system should be verified on a nonzero target, since a zero terminal target would hide its printed sign error. Before interpreting a numerical SDP result as a certificate, check positive-semidefinite residuals and the underlying Bellman residual on diagnostic feasible points; sampling is useful for finding mistakes but cannot replace the global certificate.

Simulation should draw returns only after the action, record every cost component and constraint residual, and evaluate all policies against the same economic objective. The exact quadratic case and zero-trade policy provide useful consistency checks. Report path dispersion separately from uncertainty in mean performance and distinguish numerical tolerance from statistical error. Exact replication of the published tables additionally needs the missing realized model inputs and resolution of the volatility contradiction.

The main limitation is model scope. There is no formal endogenous price impact over time, signal-learning process, funding-risk state, market-calibrated capacity curve, or empirical forecast estimation. The performance bound is powerful precisely because it is a bound for a clearly specified stochastic-control problem. Applying it to a live strategy requires that the live problem be represented with comparable fidelity; otherwise the certificate can be mathematically correct and economically uninformative.

## Source map

The dollar-state model and constraints are in chapter 2, pp. 9–21. Exact dynamic programming and the no-transaction-cost reduction are in chapter 3, pp. 22–26. Bellman bounds, quadratic ADP, and MPC occupy chapters 4–6, pp. 27–37. Experimental design and all reported numbers are in chapter 7, pp. 38–49, especially Tables 7.1–7.6 and Figures 7.1–7.3. Appendices A–B, pp. 55–58, supply quadratic expectation and elimination; appendices C–D, pp. 59–62, supply the S-procedure and LMI construction; appendix E, pp. 63–64, derives the no-trade region. The caveats above refer to the supplied 2014 publication, not to a subsequently corrected implementation.
