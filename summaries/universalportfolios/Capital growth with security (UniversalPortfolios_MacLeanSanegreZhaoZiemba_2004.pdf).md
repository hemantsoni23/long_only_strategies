# Capital growth with security

Leonard C. MacLean, Rafael Sanegre, Yonggan Zhao, and William T. Ziemba. *Journal of Economic Dynamics & Control* 28 (2004), 937–954. DOI 10.1016/S0165-1889(03)00056-3. Source: [UniversalPortfolios_MacLeanSanegreZhaoZiemba_2004.pdf](../../Finance/UniversalPortfolios_MacLeanSanegreZhaoZiemba_2004.pdf). All 18 pages were read, including the theorem arguments, numerical tables, parameter updating, and references. The journal year is 2004; the copyright line is 2003. References below use printed pages.

## Why this matters

The paper formulates a concrete alternative to reducing Kelly leverage by an arbitrary fraction. Maximize expected log wealth while requiring a terminal wealth floor to be met with a specified probability. Represent the probability constraint by selecting which scenarios must satisfy the floor; optimize the investment policy on that selected set, then search over admissible sets. This separates a difficult combinatorial choice from a family of convex allocation problems.

That decomposition is the main reusable contribution. It makes clear that chance-constrained growth optimization chooses not only positions but also the states in which protection is waived. The authors develop backward scenario elimination, provide a cheaper greedy variant, and illustrate how stronger security requirements move allocation from stocks toward bonds and cash. They also propose a normal random-drift model and Bayesian updating between planning cycles.

Several source claims require qualification before implementation. The factor aggregation proof does not establish the asserted lossless reduction to a small number of funds. Persistent random drifts generate temporal dependence after integrating out the drift. The reported stock/bond/cash example does not fully disclose position restrictions, and some displayed objective values do not reproduce from its own scenario table. These issues do not remove the useful chance-constraint formulation, but they prevent treating every theorem and table as a ready-made validated allocation engine. The note distinguishes the source's claims from direct derivations and arithmetic checks.

## Returns, information, and wealth accounting

There are $m$ risky securities and a cash account. The source assumes no transaction costs or taxes, infinitely divisible assets, limited liability, borrowing and lending at the same rate, and permitted short selling. Let $R_i(t)$ be a risky gross return and $R_0(t)=1+r(t)$ the cash gross return. The allocation fractions are $X(t)=(X_0(t),\ldots,X_m(t))^T$ with

$$
\mathbf1^TX(t)=1.
$$

A policy must use only information available before the return being earned. To avoid the source's shifting time indices, take $X_t$ measurable with respect to the history through $t-1$ and $R_t$ realized during period $t$. Then

$$
W_T=W_0\prod_{t=1}^T R_t^TX_t,
$$

$$
\log(W_T/W_0)=\sum_{t=1}^T\log(R_t^TX_t).
$$

Each gross portfolio payoff must be positive wherever its log contributes to expected utility. Limited liability of the underlying assets alone does not guarantee this for a leveraged or short portfolio. A finite-scenario implementation needs payoff positivity on every modeled path, including paths exempted from the security floor. A model with unbounded lognormal support needs the stronger corresponding almost-sure admissibility condition; scenario feasibility alone cannot establish it.

Equation (5) maximizes average expected log growth,

$$
\max_X\frac1T\sum_{t=1}^T\mathbb E\log(R_t^TX_t).
$$

For a fixed horizon, omitting $1/T$ gives the same optimizer. It does change the units of a reported objective value. The source's preceding prose identifies this with maximizing $\mathbb E[W_T^{1/T}]$. That equivalence is not generally correct: expectation does not commute with the exponential. Also, $W_T^{1/T}$ contains $W_0^{1/T}$, rather than the printed factor $W_0$. The faithful mathematical objective in the optimization equations is expected logarithmic growth.

The introduction calls log utility's absolute risk aversion, $1/W$, essentially zero at ordinary wealth levels. Its numerical size depends on the currency unit. Relative risk aversion is exactly one. Large Kelly positions should be understood through the objective and available return distribution, rather than a unit-dependent claim of approximate risk neutrality.

## Random-drift return model

Let $Y_i(t)=\log P_i(t)$ relative to an initial log-price normalization. The source models increments as

$$
Z_i(t)=\pi_i+\delta_i\epsilon_i(t),
$$

where conditional innovations are independent standard normal and the persistent drift vector has prior

$$
\pi\sim N(\mu,\Gamma),\qquad
\Delta=\operatorname{diag}(\delta_1^2,\ldots,\delta_m^2).
$$

Conditional on $\pi$,

$$
Y(t)\mid\pi\sim N(t\pi,t\Delta),
$$

while integrating out the random drift gives

$$
Y(t)\sim N(t\mu,t\Delta+t^2\Gamma).
$$

The quadratic time component reflects uncertainty about a drift that persists across periods. It is not the variance of a model that independently redraws the drift at each date. In particular,

$$
\operatorname{Cov}(Z_t,Z_s)=\Gamma,\qquad t\ne s,
$$

under the persistent-drift construction. Thus the source's statement that increments are intertemporally independent is valid conditional on the drift, not marginally under the distribution it displays. Redrawing independent drifts every period would instead produce cumulative covariance $t(\Delta+\Gamma)$.

The factor representation writes $\Gamma=\Lambda\Lambda^T$, with $p<m$ latent normal factors, and

$$
Y(t)=t\mu+t\Lambda U+\sqrt t\,\xi,
$$

where $U\sim N(0,I_p)$, $\xi$ is independent with covariance $\Delta$, and the marginal covariance agrees with the expression above. This is a model of log prices and their latent uncertainty. It does not automatically identify traded mutual funds that span the arithmetic gross returns of every original security.

## Terminal security and period-loss security

Let $w$ be a desired terminal wealth floor, $w^*=w/W_0$, and $1-\alpha$ the required success probability. The central chance-constrained problem is

$$
\max_X\sum_{t=1}^T\mathbb E\log(R_t^TX_t)
$$

$$
\text{subject to}\quad
\Pr\left(\sum_{t=1}^T\log(R_t^TX_t)\ge\log w^*\right)\ge1-\alpha.
$$

This is equation (7). The floor is on terminal wealth; it allows interim losses and recovery. It also permits outcomes in the failure set to be arbitrarily severe subject to wealth positivity. Increasing the penalty for very large shortfalls requires another risk measure or constraint.

The source's alternative drawdown measure requires all one-period wealth ratios to exceed a chosen $b\in[0,1]$ with sufficient joint probability:

$$
\Pr(R_t^TX_t\ge b\text{ for every }t=1,\ldots,T)\ge1-\alpha.
$$

This is a joint period-loss limit, not a floor relative to the running wealth maximum. Repeated losses of fraction $1-b$ can still compound into a much larger cumulative decline. If $b=(w/W_0)^{1/T}$, the event of satisfying all period floors implies terminal wealth at least $w$. Therefore its success probability is no greater than the terminal-floor success probability, explaining why it can be a stronger requirement.

The paper also defines an incomplete lower mean $\int_0^{w_\alpha}u\,dH_T(u)$, where $H_T(w_\alpha)=\alpha$ in a continuous case. This is a partial expectation of wealth, not a conditional expected shortfall unless divided by the relevant tail probability and transformed into the intended loss convention. The subsequent computations concentrate on the two chance constraints; they do not optimize that tail-severity measure.

## Disjunctive formulation

Let $\Omega$ be the path space and let $\mathcal A_\alpha$ contain measurable sets with probability at least $1-\alpha$. For each fixed $A\in\mathcal A_\alpha$, solve an inner problem requiring

$$
\sum_{t=1}^T\log(R_t(\omega)^TX_t(\omega))\ge\log w^*
\qquad\text{for all }\omega\in A.
$$

The expected-log objective still averages over all paths, including $\Omega\setminus A$. The outer problem selects the set giving the largest inner optimal value. This is equivalent to the chance constraint: any feasible policy has a sufficiently large success set, and any policy satisfying floors on such a set satisfies the probability condition.

For a fixed finite scenario set and fixed admissible policy parametrization, the objective is concave and each floor is a superlevel set of a concave sum of log-affine payoffs. Budgets and nonanticipativity are linear restrictions. The inner problem is therefore convex on the positive-payoff domain. The outer subset choice creates nonconvexity. The equivalence does not make the entire chance-constrained problem convex.

The indicator formulation in equation (9) can be read as introducing $0\le\theta(\omega)\le1$ with

$$
\theta(\omega)\left[\sum_t\log(R_t^TX_t)-\log w^*\right]\ge0,
\qquad\mathbb E\theta\ge1-\alpha.
$$

Any positive weight must lie on a successful path. Consequently a feasible indicator can always be chosen by setting weight one on successful paths. An optimal weight need not uniquely be zero or one; the valid statement is existence of an indicator representation. The printed equation has misplaced comparison notation, so the signed-surplus formulation above makes the intended algebra explicit.

A scenario-tree implementation must attach decisions to information nodes. Two paths sharing the same observed history must use the same decision at that history. Giving every complete path an independent sequence of allocations would allow hindsight. Conversely, restricting to one vector per calendar date is a deterministic allocation schedule, generally a smaller policy class. The article's tables supply only one vector per date and do not list complete node-dependent policies, so the implementation class should be documented rather than inferred from the word multistage.

## Backward scenario elimination

The source approximates one-period distributions using equal-probability regions and one sampled representative point per region. This produces $I$ equally weighted complete scenarios. An admissible success set must contain at least $I-k$ paths, where

$$
k=\lfloor I\alpha\rfloor.
$$

Begin with all path-floor constraints imposed. The method assumes this initial inner problem is feasible; an infeasible all-scenarios target requires a separate initialization or feasibility search, which the paper does not supply.

At each solved inner problem, identify its active path-floor constraints. Create child problems by deleting one active constraint at a time. Solve all children, repeat until at most $k$ constraints have been deleted, or stop a branch when none is active, and select the best surviving objective. The search concerns omitted floor constraints, not omitted paths in the objective or deleted return observations.

The reason to branch on active constraints is that relaxing only constraints that are slack at an optimum cannot produce a strict improvement while retaining all the binding restrictions under the convex inner formulation. Any strict improvement from relaxing the floor system must eventually remove an obstructing active restriction. The source's Theorem 3 states this as an intersection property. Its printed proof on p. 947 contains incompatible set statements: it simultaneously places the active set inside the optimal retained set and asserts a nonempty intersection with its complement. The branching rationale above is the useful optimization argument, with strict improvement and feasibility qualifications made explicit; the contradictory printed line should not be copied as a proof.

If there are $r\ge2$ active alternatives at each stage, exhaustive branching can require approximately $\sum_{j=1}^kr^j$ inner solves. The greedy variant evaluates the $r$ candidate one-step deletions, keeps only the child with highest expected log wealth, and repeats, using at most roughly $rk$ solves. It can discard a branch whose value improves later. The authors claim equivalence with exhaustive branching if there is at most one active constraint at every stage, and say their numerical example has that property.

A practical implementation should preserve active-set tolerances, objective tolerances, duplicate-subset detection, and the final list of waived scenarios. Those details are not given in the article. For a small $I$, exhaustive subset enumeration supplies an independent check; for a large $I$, the greedy outcome is a heuristic unless a separate bound or structural argument establishes optimality.

## Claims about fund reduction and path independence

Theorem 1 claims investors are indifferent between all $m$ securities and cash plus $p<m$ risky funds. The proof constructs a rectangular allocation map $q=AX$ from squared factor loadings, showing that it preserves the budget sum. It then uses a generalized inverse and substitutes $X=A^-q$ to conclude equality of portfolio returns.

The missing step is consequential. From $q=AX$, one obtains $A^-q=A^-AX$, which need not equal the original $X$ for a rank-reducing map. Preserving sums of portfolio weights does not establish $R^TX=R^TA^-AX$ in every state. Idiosyncratic components and nonlinear exponentiation of factor-driven log returns are not removed by this identity. The stated assumptions do not supply the required exact payoff spanning. A replication should therefore retain the full return vector unless an independently justified traded-fund representation is imposed. The source's factor covariance structure may still be useful for estimation and scenario generation.

Theorem 2 claims that the optimal policy depends on current wealth rather than the entire path, within a planning block whose distribution is held fixed. Its proof forms a path-weighted Lagrangian with multipliers on the selected security scenarios, then argues that averaging removes history dependence. General terminal path weights do not imply that their successive conditional-density ratios depend only on the newest observation. In addition, the marginal independence used in that argument conflicts with the persistent random drift above.

A wealth-only state can be justified in specific known-iid models with suitable dynamic formulations. With Bayesian learning, the posterior return-law parameters are generally also state variables; with pathwise floors on a chosen scenario set, remaining obligations can matter as well. The article explicitly separates updating between planning blocks from optimization within a block, but does not fully establish the advertised state reduction under all its displayed assumptions. The safe implementation is to retain nonanticipative scenario-tree decisions and explicitly declare any further policy restriction.

## Stock, bond, and cash illustration

The application uses annual returns from Data Resources, Inc. for 1980–1990: the S&P 500, Salomon Brothers Bond Index, and U.S. Treasury bills. Cash is normalized to gross return one and the other means adjusted relative to it. Table 1 reports stock and bond gross-return means of 1.0875 and 1.0375, standard deviations 0.1236 and 0.0597, and correlation 0.32. These are illustrative calibration inputs, not forecast estimates validated on a later sample. The paper gives no detailed index construction, missing-data treatment, estimation divisor, or accounting for taxes and costs.

The discretization partitions the two-dimensional return distribution at its centroid along principal axes and selects representatives intended to approximate the moments. Table 2 supplies all four one-period scenarios:

| Scenario | Stock gross return | Bond gross return | Cash | Probability |
|---:|---:|---:|---:|---:|
| 1 | 0.950 | 1.015 | 1.000 | 0.25 |
| 2 | 1.065 | 1.100 | 1.000 | 0.25 |
| 3 | 1.085 | 0.965 | 1.000 | 0.25 |
| 4 | 1.250 | 1.070 | 1.000 | 0.25 |

The planning horizon is three years, giving $4^3=64$ equally likely paths under independent scenario draws. The table's standard deviations closely reflect sample-style rather than population-style four-point dispersion, so a replication should not infer an exact moment match from the representative points. The points themselves are the complete discrete inputs and should be used directly for reproducing the illustration.

Table 3 specifies an annual secured multiplier $a$ and imposes terminal wealth at least $a^3$ from initial wealth one. It varies $a$ from 0.95 to 0.999 and success probability from zero to 0.99. Selected reported allocations, in stock/bond/cash order, are:

| $a$ | Success probability | Period 1 | Period 2 | Period 3 | Printed objective (%) |
|---:|---:|---|---|---|---:|
| 0.95 | 0.99 | (1,0,0) | (0.492,0.508,0) | (0.492,0.508,0) | 19.6 |
| 0.97 | 0.99 | (1,0,0) | (0.333,0.667,0) | (0.333,0.667,0) | 18.2 |
| 0.99 | 0.95 | (1,0,0) | (0.867,0.133,0) | (0.867,0.133,0) | 19.4 |
| 0.99 | 0.99 | (0.456,0.544,0) | (0.270,0.730,0) | (0.270,0.730,0) | 12.7 |
| 0.999 | 0.99 | (0.270,0.730,0) | (0.008,0.020,0.972) | (0.008,0.020,0.972) | 5.27 |

Unconstrained rows put all wealth in stocks and print 23.7. The displayed tendency is toward more bonds and cash as protection tightens, often later in the horizon. The allocations are reported source results; the qualifications below prevent treating every row as an independently reproduced optimum.

For the joint period-loss condition, Table 4 varies $b$ from 0.96 to 0.999 and labels success levels 0, 50, 75, and 100 percent. At $b=0.97$ and 75% security it reports all stocks in period one and (0.692,0.308,0) in periods two and three, with objective 21.3. Requiring 100% security uses that mixed allocation in every period, with objective 20.1. At $b=0.999$ and 100% security it reports (0.105,0.284,0.611) each period and objective 5.84. The period-one-loss floor is stronger than the terminal floor when comparably specified, so the shift toward secure assets has a clear economic interpretation.

## Numerical consistency and missing restrictions

The printed 23.7 can be identified from the supplied scenarios: three times the average one-period stock log return is approximately 0.237304. Thus it is 100 times cumulative expected log growth over three periods, rather than 23.7% annual growth. The annual expected log growth is approximately 0.0791013; exponentiating the three-year expected log produces a 26.7826% geometric wealth increase. Those are distinct quantities.

Some other table entries do not match the same arithmetic. Under Table 4's fixed allocation (0.538,0.462,0) for all three dates, the supplied scenarios give approximately 18.0977 in cumulative log-percentage units, whereas the $b=0.98$, 100% row prints 16.1. The latter is close to the 16.0846 obtained from the distinct (0.385,0.615,0) allocation in the next block. Table 3's $a=0.99$, 95% row gives approximately 22.6936 from its three displayed allocation vectors, versus printed 19.4. These are direct checks of the reported fixed vectors, not corrected results from rerunning the optimization. An undisclosed state-dependent policy would require more information than the tables provide.

There is also a constraint mismatch. At $a=0.95$, an all-stock policy has every one-period multiplier at least 0.95 under Table 2, so terminal wealth is at least $0.95^3$ on all 64 paths. It already satisfies the displayed weak terminal-floor inequality at 99% confidence, yet the table shifts toward bonds. Clarifying a different target, strict-versus-weak convention, or unstated constraint would require additional implementation material.

Finally, all stocks cannot be the unconstrained optimum in this finite model if unrestricted cash borrowing is truly allowed. The feasible constant vector (1.2,0,−0.2) has positive payoff in all four scenarios, minimum 0.94, and expected log return about 0.0931808 per period, exceeding the all-stock 0.0791013. The all-stock directional derivative toward cash-financed leverage is about 0.0716856, also positive. A long-only/no-borrowing restriction would help explain the reported Kelly corner, but the source's market assumptions explicitly permit borrowing and short selling. The missing restriction should be recorded, not silently invented.

There are no standard errors, confidence intervals, prospective tests, or sensitivity grids for estimation uncertainty. Chance probabilities are exact only for the selected finite scenario model. With 64 equal paths, probabilities move in units of 1/64; they are not finely resolved estimates of real-world tail risk.

## Bayesian rebalancing between planning blocks

For a block of length $T$, define $\bar Y_T=Y(T)/T$, $\Delta_T=T\Delta$, and $\Sigma_T=T\Delta+T^2\Gamma$. The normal-model posterior is

$$
\pi\mid Y(T)\sim N(m_T,V_T),
$$

$$
m_T=\mu+(I-\Delta_T\Sigma_T^{-1})(\bar Y_T-\mu),
$$

$$
V_T=\frac1{T^2}(I-\Delta_T\Sigma_T^{-1})\Delta_T.
$$

These equations (13)–(14) agree with the usual normal update. For example, $I-\Delta_T\Sigma_T^{-1}=T^2\Gamma\Sigma_T^{-1}$, so the posterior gain weights the observed block-average log return relative to prior uncertainty. When the relevant matrices are invertible, the covariance also equals $(\Gamma^{-1}+T\Delta^{-1})^{-1}$. Matrix order must be preserved; scalar shrinkage intuition does not authorize commuting covariance matrices.

The source proposes factor analysis of an empirical increment covariance, a low-rank-plus-diagonal reconstruction, and shrinkage either toward a cross-asset grand mean or toward the previous block's posterior. It then recomputes a plan for the next block. This is a proposed estimation procedure, not a backtested rolling allocation in the numerical section.

Its covariance time scales need clarification. A sample covariance of within-block increments conditional on a fixed latent drift estimates innovation covariance $\Delta$, whereas $\Sigma_T$ is cumulative log-price covariance including drift uncertainty. Identifying an unscaled increment covariance with $\Sigma_T$ and its diagonal residual with $\Delta_T$ is not justified by the displayed stochastic model alone. The paper gives no complete statistical design establishing these identifications, number-of-factors selection, or uncertainty estimates.

For reimplementation, the well-defined core is expected-log optimization with explicit terminal or joint period floors, a declared nonanticipative decision class, positive-payoff constraints, and an outer scenario-selection search. The original paper provides enough information to reconstruct this structure and its small scenario illustration. Its fund-reduction proof, policy-state reduction, undisclosed trading restrictions, and inconsistent numerical rows require independent resolution before its reported optimality claims are used in a production allocation process.
