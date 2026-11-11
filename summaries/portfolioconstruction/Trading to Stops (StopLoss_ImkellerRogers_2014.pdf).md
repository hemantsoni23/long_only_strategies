# Trading to Stops

Nora Imkeller and L. C. G. Rogers, *SIAM Journal on Financial Mathematics* 5, 2014, pp. 753–781, DOI 10.1137/130911706. Published December 16, 2014. This note covers the complete 29-page article, including the excursion calculations, numerical tables, and Appendices A–B. Page references below use the printed journal pagination.

Source: [StopLoss_ImkellerRogers_2014.pdf](../../Finance/StopLoss_ImkellerRogers_2014.pdf).

## Why this matters

A stop rule is inseparable from what happens after it triggers. Selling and immediately re-entering the same opportunity, abandoning it for a new one, and retaining winners while replacing losers create different economic problems. Imkeller and Rogers show that the optimal lower stop, take-profit level, and value of trailing stops depend strongly on this choice and on uncertainty about expected returns.

The paper supplies explicit joint transforms of the time and gain at exit for several Brownian stop rules. These transforms reduce repeated trading to a renewal calculation. It then introduces uncertain drift, compares several replacement policies, and evaluates simple time-sloping barriers against a Bayesian optimal-stopping benchmark. Under its illustrative parameters, simple fixed barriers with slopes recover much of the value of a more complicated state-dependent rule.

This is a theoretical and numerical study of a particular discounted utility-of-realized-gains objective. It does not backtest stop orders in market data, establish that stop losses improve arbitrary investment strategies, or model gaps, slippage, bankruptcy, market impact, and execution latency.

## The economic objective and its assumptions

The position has initial value $Y_0$ and additive gain

$$
X_t=Y_t-Y_0=\mu t+\sigma W_t.
$$

Volatility $\sigma$ is known and constant. Initially drift $\mu$ is also known; later it is drawn once for a fund from a specified prior. Arithmetic Brownian motion permits negative values and uses absolute rather than proportional gains. A stop distance of 0.02 is in the model's gain units; it is not intrinsically a 2% drawdown of a changing portfolio.

The wealthy investor consumes the realized gain net of fixed cost $c$ whenever the position is closed. The capital base is then reinvested immediately, and the same rule is applied to rebased increments. Negative gains require resources from outside the modeled position. Bankruptcy and finite-wealth admissibility are excluded.

Let $T_n$ be successive exit times with $T_0=0$. The objective is

$$
\phi=E\left[\sum_{n\ge0}e^{-\rho T_{n+1}}
 U\big(Y_{T_{n+1}}-Y_{T_n}-c\big)\right],
\qquad U(x)=1-e^{-\gamma x}.
$$

Here $\rho>0$ is discounting and $\gamma>0$ absolute risk aversion. The model rewards timely realization because gains cannot be consumed until exit. It sums utility of successive realized increments, rather than applying utility once to terminal wealth or to total discounted consumption. That choice is central to its conclusions about frequent profit-taking.

With known drift and a repeated fixed stopping rule $T$, strong Markov and stationary-increment properties give

$$
\phi=\frac{E[e^{-\rho T}U(X_T-c)]}{1-E[e^{-\rho T}]}.
$$

Write the joint transform as $L(\rho,\gamma)=E[e^{-\rho T-\gamma X_T}]$. Then

$$
\phi=\frac{L(\rho,0)-e^{\gamma c}L(\rho,\gamma)}
 {1-L(\rho,0)}.
$$

These identities require finite expectations and a denominator away from zero. Arbitrarily rapid repeated stopping is not a harmless numerical limit, especially with a fixed cost. The corresponding unrestricted repeated-stopping problem satisfies the renewal Bellman equation

$$
\bar\phi=\sup_\tau E[e^{-\rho\tau}\{U(X_\tau-c)+\bar\phi\}].
$$

For known constant drift, time homogeneity motivates stationary stopping regions. This is not a justification for fixed barriers once the posterior drift depends on elapsed time and observed gains.

## Stop families and transform inputs

The four families use $a,b>0$ and the running maximum $M_t=\sup_{0\le s\le t}X_s$:

| Rule | Exit condition |
|---|---|
| Fixed lower and upper stops | $X_t=-a$ or $X_t=b$ |
| Trailing lower stop plus fixed take-profit | $M_t-X_t=a$ or $X_t=b$ |
| Trailing stop alone | $M_t-X_t=a$ |
| Converging stop | $(1+\varepsilon)M_t-X_t=a$, $\varepsilon>0$ |

A trailing exit can occur at a positive gain after a rise; “lower-side” exit therefore need not mean a negative realized profit. Converging stops reduce the allowable drawdown as the maximum increases. The trade must end before the maximum can exceed $a/\varepsilon$.

For a given drift and transform discount parameter, let $-\alpha<0<\beta$ be the roots of

$$
\tfrac12\sigma^2 z^2+\mu z-\rho=0,
\qquad
\alpha=\frac{\mu+\sqrt{\mu^2+2\rho\sigma^2}}{\sigma^2},
\quad
\beta=\frac{-\mu+\sqrt{\mu^2+2\rho\sigma^2}}{\sigma^2}.
$$

The roots must be recomputed when $\rho$ or $\mu$ changes, including during integration over a drift prior. At zero discount or zero drift, formulas with vanishing denominators require continuous limits rather than direct floating-point substitution.

## Fixed barriers: exact calculation and proof logic

For fixed stops, solve the killed-generator ODE

$$
\tfrac12\sigma^2 f''+\mu f'-\rho f=0
$$

on $[-a,b]$. Boundary values $f(-a)=e^{\gamma a}$ and $f(b)=e^{-\gamma b}$ produce $L$ by optional sampling at the exit. The result, Equation 3.5, is

$$
L_1(\rho,\gamma)=
\frac{e^{\gamma a}(e^{\beta b}-e^{-\alpha b})
 +e^{-\gamma b}(e^{\alpha a}-e^{-\beta a})}
 {e^{\alpha a+\beta b}-e^{-\alpha b-\beta a}}.
$$

The partial transform for upper-barrier exit $H$ is

$$
L_H(\rho,\gamma)=
\frac{(e^{\alpha a}-e^{-\beta a})e^{-\gamma b}}
 {e^{\alpha a+\beta b}-e^{-\alpha b-\beta a}}.
$$

Subtract it from the total transform to obtain the lower-exit contribution. These partial expectations are discounted quantities, not ordinary exit probabilities unless evaluated at zero discount and zero utility-transform argument.

Differentiating $L_1$ in $\rho$ at $(0,0)$ gives mean cycle duration. With $k=2\mu/\sigma^2$,

$$
E[T]=\frac{b(e^{ka}-1)-a(1-e^{-kb})}
 {\mu(e^{ka}-e^{-kb})}.
$$

The driftless limit is $ab/\sigma^2$. Numerically stable exponential differences or rescaling are important for large barriers; otherwise cancellation near zero drift and overflow at distant stops can contaminate the optimization.

Proposition 2 studies $a\to\infty$ with $b$ fixed. If $\gamma>\alpha$, the repeated objective tends to negative infinity. The discounted weight of a far loss decays approximately as $e^{-\alpha a}$, but its negative exponential utility grows as $e^{\gamma a}$. If $\alpha>\gamma$ and $b>c$, every finite lower barrier is inferior to taking it to negative infinity. Appendix A proves this comparison through positivity and convexity of an exponential expression, ultimately using Jensen's inequality.

The proposition does not cover every boundary case, particularly equality of the exponents. It explains why a known sufficiently favorable drift often gives no finite lower stop under this objective. It is not a theorem that investors who know expected returns should accept unlimited losses under all wealth constraints and utility specifications.

## Trailing barriers through excursions

For the process $X-M$, excursions below zero are indexed by increases in the running maximum. Introduce an independent exponential killing clock of rate $\rho$ to represent discounting. An excursion either reaches drawdown $a$ before killing or is killed first. Excursion intensities give an explicit transform without solving a two-state free-boundary PDE.

Define

$$
D=e^{\alpha a}-e^{-\beta a},\qquad
n_B=\frac{\alpha+\beta}{D},
\qquad
\nu=\frac{\beta e^{\alpha a}+\alpha e^{-\beta a}}{D}.
$$

For trailing lower plus fixed upper stops,

$$
L_2(\rho,\gamma)=e^{-(\nu+\gamma)b}
 +\frac{n_Be^{\gamma a}}{\nu+\gamma}
  [1-e^{-(\nu+\gamma)b}].
$$

The first term is the upper-exit partial transform. The integral behind the second term averages the gain $y-a$ at the first sufficiently deep excursion occurring while the running maximum is $y<b$. This decomposition is the essential excursion-theory mechanism; $\nu$ is a rate in maximum/local-time space, not calendar time.

Letting $b\to\infty$ gives trailing-only transform

$$
L_3(\rho,\gamma)=\frac{n_Be^{\gamma a}}{\nu+\gamma}.
$$

With $k=2\mu/\sigma^2$ and $m=k/(e^{ka}-1)$, the reported mean duration for the mixed rule is

$$
E[T]=\frac{\sigma^2}{2\mu^2}(e^{ka}-1-ka)(1-e^{-mb}).
$$

Remove the final factor for trailing-only. Its zero-drift limit is $a^2/\sigma^2$. These formulas allow independent duration checks alongside the utility calculation.

For converging stops, replace drawdown distance $a$ by $d(x)=a-\varepsilon x$ when the running maximum is $x$. Define $n_B(x)$ and $\nu(x)$ by the preceding formulas with $a$ replaced by $d(x)$. The discounted survival factor in maximum space is

$$
\overline F(x)=\exp\left[-\int_0^x\nu(s)\,ds\right]
 =e^{-\beta x}
 \left[\frac{1-e^{-(\alpha+\beta)(a-\varepsilon x)}}
 {1-e^{-(\alpha+\beta)a}}\right]^{1/\varepsilon}.
$$

Then

$$
L_4(\rho,\gamma)=\int_0^{a/\varepsilon}
 e^{-\gamma[(1+\varepsilon)x-a]}n_B(x)\overline F(x)\,dx.
$$

Equation 3.23 rewrites this using incomplete beta functions. The integral representation suffices to implement the method with endpoint-aware quadrature. The paper does not tabulate this family separately in the main comparison. Its limiting-rule description should not substitute for direct checking: $\varepsilon\to0$ with fixed $a$ gives trailing-only, not a finite fixed take-profit barrier.

## Uncertain drift and three replacement policies

For a fund, drift is constant but unknown, with prior distribution $m(d\mu)$. The main numerical priors are normal, mean $\mu_0=0.15$ and standard deviation $\sigma_\mu=0.3$ or 0.7. Volatility remains 0.3. The prior includes negative-drift funds; stopping can limit the damage from selecting one.

For any fixed rule define

$$
A(\mu)=E^\mu[e^{-\rho T}U(X_T-c)],\quad
B(\mu)=E^\mu[e^{-\rho T}],
$$

and upper/lower partial discount factors $B_H(\mu)$ and $B_L(\mu)$, with $B=B_H+B_L$. All are obtainable from the transforms and their partial versions.

Policy A always re-enters the same fund after exit. Conditional on its true drift, every cycle has the same drift. Average the conditional repeated value:

$$
\bar\phi_A=\int\frac{A(\mu)}{1-B(\mu)}m(d\mu).
$$

Policy B draws an independent new fund from the original prior after every exit. Every cycle begins anew, so

$$
\bar\phi_B=\frac{\int A(\mu)m(d\mu)}
 {1-\int B(\mu)m(d\mu)}.
$$

The expectation of a ratio in A cannot be replaced by the ratio of expectations in B. They describe different opportunities, not different integration approximations.

Policy C keeps the same fund after upper-side exit but draws a new independent fund after lower-side exit:

$$
\bar\phi_C=
\frac{\displaystyle\int\frac{A(\mu)}{1-B_H(\mu)}m(d\mu)}
 {\displaystyle1-\int\frac{B_L(\mu)}{1-B_H(\mu)}m(d\mu)}.
$$

A high-quality fund can then generate repeated take-profit cycles without being discarded. This selection-and-retention opportunity is the principal reason C can dominate B. For a trailing-plus-upper rule, replacement follows which barrier triggers, even if the trailing exit realizes a gain.

The A–C rules optimize barrier parameters under the prior but do not continuously adjust the rule using the full posterior. The option to sample independent funds with the same attractive prior after every abandonment is assumed, not estimated from the investment-manager universe. Availability, capacity, search cost, and correlations across candidate funds are not modeled.

## Bayesian benchmark and numerical scheme

Policy D refreshes the fund after exit as B does, but allows unrestricted stopping based on learning. The normal prior has variance $\sigma^2/\tau_0$, giving posterior

$$
\widehat\mu(t,x)=\frac{\tau_0\mu_0+x}{\tau_0+t},
\qquad v_t=\frac{\sigma^2}{\tau_0+t}.
$$

In the observation filtration,

$$
dX_t=\widehat\mu(t,X_t)\,dt+\sigma d\widehat W_t.
$$

Time and current gain are sufficient statistics for the drift posterior. A new fund resets time, gain, and prior. The benchmark used for comparison with $\sigma_\mu=0.3$ has $\tau_0=\sigma^2/\sigma_\mu^2=1$.

Starting $\bar\phi_0=0$, solve repeated one-cycle stopping problems

$$
\bar\phi_{n+1}=\sup_\tau E[e^{-\rho\tau}
 \{U(X_\tau-c)+\bar\phi_n\}].
$$

For each iteration, set payoff $g_n(x)=U(x-c)+\bar\phi_n$ and solve the obstacle problem

$$
V\ge g_n,\qquad
V_t+\tfrac12\sigma^2V_{xx}+\widehat\mu(t,x)V_x-\rho V\le0,
$$

with equality in the continuation region. Return $V(0,0)$ as the next repeated value. Appendix B uses Crank–Nicolson in time and a three-point spatial generator, with policy improvement to determine stop versus continue nodes. The discrete generator must be checked to have the needed Markov-generator sign structure; an arbitrary central-difference grid does not automatically preserve it under strong drift.

The numerical horizon is truncated at a sufficiently large $\overline T$; terminal values equal stopping payoff. Spatial boundaries absorb, forcing exit there. The actual horizon, grid limits and spacings, convergence tolerances, integration tolerances, and optimizer search bounds are not reported. Therefore the four-decimal benchmark is a reported numerical result, not a value that can be replicated exactly from a fully specified grid in the PDF.

Appendix B supplies an argument for finiteness of the iteration using a linear-utility upper comparison. Its final explicit ODE and characteristic roots are written for constant drift, whereas the filtered generator is time dependent. That step should not be treated as a complete general convergence or numerical-error proof for every Bayesian prior. Grid refinement, domain enlargement, and fixed-point residual checks remain necessary in an implementation.

## Numerical experiment and reported values

All principal examples use $\sigma=0.3$, $\gamma=2.5$, fixed exit/reinvestment cost $c=0.0005$, and discount rate $\rho=0.1$. There is no dataset or estimated historical sample. Units of time must be kept consistent with drift, volatility, and discounting; the tables report model-time durations rather than business-day trade counts.

For known drift $\mu=0.15$, fixed stops and trailing-plus-upper stops both optimize at $a=\infty$, $b=0.0184$, value 4.1553, and mean duration 0.1224. Trailing-only optimizes at $a=0.0894$, value 0.5314, duration 0.0983. The optimized deterministic exit-time rule has value 0.8724 and duration 0.3780. The latter is a useful column-reading check: 0.8724 is the objective, not the selected time.

With uncertain drift, the fixed-barrier results are:

| Replacement policy | Drift SD | Lower distance $a$ | Upper distance $b$ | Objective | Mean cycle time |
|---|---:|---:|---:|---:|---:|
| A: same fund | 0.3 | 0.2159 | 0.0470 | 0.8416 | 0.0998 |
| A: same fund | 0.7 | 0.0837 | 0.0559 | 0.4410 | 0.0475 |
| B: refresh every exit | 0.3 | 0.0191 | 0.3409 | 1.4071 | 0.0804 |
| B: refresh every exit | 0.7 | 0.0083 | 0.3426 | 4.8955 | 0.0338 |
| C: refresh only lower exit | 0.3 | 0.3620 | 0.0239 | 6.8525 | 0.0370 |
| C: refresh only lower exit | 0.7 | 0.2020 | 0.0213 | 20.216 | 0.0125 |

These objective values are discounted utility sums, not annual returns, Sharpe ratios, or terminal wealth multipliers. In particular value 20.216 does not mean a 2,021.6% return.

Under A, greater uncertainty lowers value and tightens the loss barrier. Mixed trailing-plus-upper values are 0.8398 and 0.4223 for the two prior standard deviations, slightly below fixed barriers. Trailing-only values are 0.2397 and −0.4264. The negative value means that this restricted rule can be unattractive relative to not undertaking the investment; it is not proof that an investor must choose a loss-making policy.

Under B, short lower distances rapidly remove poor funds, while distant profit barriers let good draws run. Mixed-rule values are 1.3431 and 4.1695; trailing-only gives 1.3354 and 4.1224. Increased dispersion in the available drift distribution can increase value because replacement selectively abandons poor draws and exploits good ones. This result depends on the assumed repeatable opportunity set and is not a general argument that parameter uncertainty is beneficial.

Under C, the investor can take profits repeatedly in a good fund. The lower barrier is much farther away to avoid mistakenly abandoning that opportunity; the upper barrier is much closer to realize utility promptly. Mixed-rule values, 6.8539 and 20.231, only slightly exceed fixed barriers. The A and C strategies do not share the same post-exit behavior as the D benchmark, so C's larger value is not evidence of outperforming an unrestricted optimum for the same admissible problem.

## Sloping barriers and comparison with optimal stopping

For a common slope $q$, use lower and upper boundaries $-a+qt$ and $b+qt$. For a trailing rule define $\widehat M_t=\sup_{s\le t}(X_s-qs)$ and use lower boundary $\widehat M_t-a+qt$. Subtracting the linear trend, $Z_t=X_t-qt$, turns these into the earlier stationary boundaries for a process with drift $\mu-q$.

The transform identity is

$$
L_X(\rho,\gamma)=L_Z(\rho+\gamma q,\gamma).
$$

Two changes are necessary: shift drift to $\mu-q$ and shift the discount argument to $\rho+\gamma q$. For the denominator transform $L_X(\rho,0)$ only the drift changes. Forgetting either distinction produces a different objective. Negative slopes can require checking transform existence rather than assuming all shifted parameters lie in the originally nonnegative domain.

Known-drift optimization selects $q=0$. Under A with drift SD 0.3, the fixed-barrier slope is 0.0347 and value rises only from 0.8416 to 0.8426. Under B, optimal parameters are $a=0.0345$, $b=0.2944$, and $q=0.4949$, giving value 1.5976 versus 1.4071 without slope. This is the reported approximately 13.5% increase in **utility objective**, not investment return.

The Bayesian D benchmark is 1.6770. The common-slope fixed rule reaches approximately 95.3% of that value, a derived ratio. The mixed trailing rule improves much less, from 1.3431 to 1.3519. A common upward slope moves both barriers upward and is only a simple approximation to the curved posterior-optimal region.

Allowing distinct slopes gives $a=0.0324$, $b=1.1400$, lower slope $q_L=0.4198$, and upper slope $q_H=-1.4532$, with value 1.6305. This is about 97.2% of the reported benchmark and about 2.1% above the common-slope value, both derived comparisons. The barriers converge and force a finite review; Figure 8 shows their close visual fit to the optimal region. The separate-slopes transform derivation is referred to Imkeller's thesis rather than provided completely in this article, limiting standalone analytic replication of that extension.

For C, common-slope fixed stops use $a=0.4181$, $b=0.0192$, and $q=0.1212$, raising value from 6.8525 to 6.9719, approximately 1.7%. The corresponding mixed-rule value is 6.9721. Here simple fixed and trailing rules are economically almost indistinguishable under the chosen criterion.

## Reproduction sequence and practical limits

Begin by reproducing the known-drift transforms and their limiting durations; then verify $L(0,0)=1$ for finite almost-sure exits and that upper plus lower partial transforms equal the total. Optimize barriers using stable exponentials and explicit large-barrier limits. Integrate conditional quantities over the drift prior before forming the correct A, B, or C renewal expression. Test sensitivity to tail quadrature, because exponential utility weights adverse drifts heavily.

For D, reproduce the posterior process, obstacle solver, and repeated-value iteration with independent domain and grid refinement. Compare simple rules with the benchmark under the same refresh policy and prior. Report numerical error and integration settings rather than borrowing the source's precision without supporting convergence evidence. If simulation is used as a separate check, account for Brownian boundary crossing between time steps; otherwise discretization can falsely improve stops by missing crossings.

The study's principal insight is that uncertainty and post-exit selection, rather than a stop level alone, explain its benefits. Stops protect against choosing a persistently poor opportunity, while the ability to retain or replace funds governs the optimal take-profit behavior. Results depend on additive diffusion, constant unknown drift, continuous monitoring, known volatility, fixed costs, infinite horizon, and access to independent replacement opportunities. Price jumps, changing drift regimes, finite capital, taxes, proportional costs, shorting restrictions, and execution gaps would require a new model and new optimization.
