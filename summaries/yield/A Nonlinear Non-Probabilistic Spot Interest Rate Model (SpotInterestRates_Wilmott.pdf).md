# A Nonlinear Non-Probabilistic Spot Interest Rate Model

**D. Epstein and P. Wilmott (1999).** *Philosophical Transactions of the Royal Society of London A* 357, 2109–2117. Source: [SpotInterestRates_Wilmott.pdf](../../Finance/SpotInterestRates_Wilmott.pdf). All 11 PDF pages are covered: nine article pages plus JSTOR front and reference-link pages. The source is a methodological exposition with one illustrative path figure and three qualitative comparison tables; it contains no empirical calibration, backtest, or numerical pricing table.

## Why this matters

The paper replaces a fully specified probability law for the short rate with a set of admissible rate paths. It values a contract by its worst and best discounted cash flows over that set. This produces valuation intervals and makes the value of a hedge depend on the portfolio it offsets. It is useful when uncertainty about the interest-rate model is economically material and a single calibrated price conceals that uncertainty.

The distinctive mechanism is a smooth bounded representative rate surrounded by a band containing the actual short rate. The representative rate has bounded speed; the actual rate can jump and oscillate inside its surrounding band. Worst-case valuation then satisfies a first-order nonlinear equation. The nonlinearity comes from selecting adverse rate movements and discounting according to the signs of the portfolio's sensitivity and value.

This is not a statistical demonstration that distribution-free bounds are tight or profitable. Wide admissible path sets can produce unusably wide intervals, and an observed path outside the set invalidates the asserted protection. The authors themselves distinguish a model being difficult to reject from its being useful. The paper summarizes an approach developed more fully in their earlier work, rather than supplying all numerical algorithms and calibration evidence here.

## The admissible path set

Let $r_t$ be the representative short rate and $\rho_t$ the actual rate, denoted $r'$ in the source. The restrictions are

$$
r^-\le r_t\le r^+,
\qquad c^-\le\dot r_t\le c^+,
\qquad |\rho_t-r_t|\le\varepsilon.
$$

The representative path is absolutely continuous with bounded derivative; the actual path need not be smooth or continuous. A practical continuous-time definition still requires measurability and integrability of $\rho$ so that money-market discounting exists. There is no assigned probability of any permitted jump or oscillation and no covariance matrix or diffusion volatility.

The source gives illustrative band endpoints of 3% and 20% and an allowed annual rise or fall of 4 percentage points. The derivative restriction is on the level of the annualized rate, not a 4% proportional growth rate. With decimal annual rates and time in years, these examples correspond to $r^-=.03$, $r^+=.20$, and $c^-=-.04$, $c^+=.04$. The width $\varepsilon$ has rate units; it is not an annualized standard deviation and is not scaled by the square root of a time step.

The level bounds apply to the representative rate as written. The actual rate can lie between $r^--\varepsilon$ and $r^++\varepsilon$. If the intended application also imposes hard bounds on the actual rate, intersect the tube with those bounds explicitly; that changes the pricing operator near its edges. Similarly, a representative path at $r^-$ cannot move downward, and one at $r^+$ cannot move upward. State constraints must be enforced in the numerical controls.

Figure 1, on PDF page 4, illustrates increases, jumps, rapid daily alternation, quiet periods, and Brownian-looking segments within the tube. It is a constructed example, not an estimated historical rate series. Its horizontal span is approximately five time units and its vertical axis is percentage rate. Visual resemblance to a Brownian path does not make the model a diffusion: no probabilistic law or quadratic-variation parameter has been introduced.

The current representative rate is a state input. Observing an actual rate only locates that representative rate within a band unless an additional filtering or selection rule is supplied. The source does not estimate that rule, the band width, or the path constraints from data.

## Lower and upper values as control problems

For deterministic dated cash flows $q_i$ at $T_i$, define the lower value at state $(r,t)$ as

$$
\underline V(r,t)=\inf_{(r_\cdot,\rho_\cdot)\in\mathcal A(r,t)}
\sum_{i:T_i>t}q_i\exp\left(-\int_t^{T_i}\rho_s\,ds\right),
$$

where $\mathcal A(r,t)$ is the admissible path set. Replacing the infimum by a supremum defines $\overline V$. This formulation makes precise the paper's worst/best-value interpretation; the source derives its differential equation through a local worst-increment argument.

For a fixed path, discounted cash-flow valuation is linear. Taking an infimum over paths makes the lower functional concave, positively homogeneous for nonnegative scale, and superadditive:

$$
\underline V(X+Y)\ge\underline V(X)+\underline V(Y),
\qquad \overline V(X)=-\underline V(-X).
$$

The separate worst paths for $X$ and $Y$ need not be compatible. Offsetting exposures can therefore narrow the combined portfolio's interval. Equality may hold for contracts whose worst path is shared; nonlinearity does not imply a strict diversification benefit for every portfolio.

These are valuation bounds conditional on the admissible set. A lower value is not an expected price, a confidence limit, or a quantile. Nor is its gap from an upper value automatically the bid–ask spread observed in a market. The interval is a consequence of the specified uncertainty; trading costs and quotation conventions are separate inputs.

## Deriving and interpreting the nonlinear equation

Between cash-flow dates, dynamic programming gives

$$
0=V_t+\min_{c\in[c^-,c^+],\ \rho\in[r-\varepsilon,r+\varepsilon]}
\{cV_r-\rho V\}.
$$

Away from the state boundaries, the controls separate. Define

$$
c(x)=\begin{cases}c^-,&x\ge0,\\c^+,&x<0,\end{cases}
\qquad
 e(x)=\begin{cases}\varepsilon,&x\ge0,\\-\varepsilon,&x<0.\end{cases}
$$

The source's equation (3.3) is therefore

$$
V_t+c(V_r)V_r-[r+e(V)]V=0.
$$

Equivalently, $V_t+\min(c^-V_r,c^+V_r)-rV-\varepsilon|V|=0$. The sign of $V_r$ chooses the adverse slope of the representative rate, while the sign of $V$ chooses the adverse discount rate. A positive continuation value is discounted at the highest permissible actual rate. A negative continuation value is made more negative in present value by the lowest permissible actual rate. Applying the positive-value discount rule to a liability would reverse the adverse direction.

At zero value or zero sensitivity, the relevant product vanishes, so the tie-breaking convention has no effect on the Hamiltonian. At a level boundary, replace the unconstrained interval for $c$ by its inward-pointing feasible subset. The source does not supply explicit boundary conditions or a convergence analysis; an implementation cannot safely extrapolate the unconstrained equation beyond the allowed band.

Upper values solve the corresponding maximization problem. In the source's notation, reverse the choices of $c$ and $e$. For a signed portfolio, compute both sides coherently; summing separate contract upper and lower prices generally loses the portfolio effect.

The equation is first-order nonlinear hyperbolic, rather than the second-order diffusion equation of a Brownian short-rate model. Smooth solutions can develop kinks when the adverse controls switch. A monotone dynamic-programming or viscosity-solution-compatible discretization is more appropriate than assuming global differentiability. The absence of a second derivative is structural: the representative rate has bounded speed, and the shadowing band enters through adverse discounting rather than a diffusion variance.

## Dated cash flows and continuous rate-dependent payments

A known payment $q$ at date $T$ produces the jump condition

$$
V(r,T^-)=V(r,T^+)+q.
$$

This is source equation (5.1). Assemble a coupon-bond portfolio into one dated cash-flow schedule and apply all same-date payments before solving backward to the previous date. Pricing each bond separately and adding its worst value need not equal the worst value of the aggregate signed schedule.

The paper notes that vanilla swaps can be decomposed into bond cash flows. That statement presumes the contractual floating-rate and reset conventions needed for the usual decomposition; it does not identify every term rate with the instantaneous representative rate. For caps and floors, the source explicitly proposes approximating the relevant short-period reference rate by $r$ and then imposing a state-dependent payment jump. That approximation should be recorded, especially for long accrual periods or payments fixed before their settlement date. A separate observed fixing may have to be carried as a state variable.

A range note paying, for example, \$1 per qualifying day depends on the actual reference rate. The source says a payment source term can be added. If the cash-flow rate is $y(\rho,t)$, the coherent lower-value equation is the derived joint-control expression

$$
V_t+\min_{c,\rho}\{cV_r-\rho V+y(\rho,t)\}=0.
$$

The same $\rho$ must determine discounting and the range payment. One cannot independently choose the worst discount rate and the smallest range payment if those choices require different actual rates. For discrete daily observation, use dated jumps with the same joint minimization instead of treating a dollar-per-day payment as a currency-per-year rate without conversion. Observation calendars, range endpoints, and any fixing-to-payment delay are absent from the paper's example.

## Index amortizing rate swaps

An index amortizing rate swap adds the outstanding principal $P$ as a state. Between reset dates $P$ is constant. At a reset, a payment based on the current reference rate is exchanged and principal becomes $g(r)P$, where $g$ is the specified amortization multiplier. The source initially takes $\varepsilon=0$ and writes

$$
V(r,P,t_i^-)=V(r,g(r)P,t_i^+)+(r-r_f)P.
$$

Its terminal condition is $V(r,P,T)=(r-r_f)P$. Here $r_f$ is the fixed rate. For annualized rates and a reset interval with accrual fraction $\Delta_i$, an implementation needs the factor $\Delta_i$ in the interest payment unless it is already absorbed into the source's period-rate convention. The printed formulas do not specify that convention. Payment occurs on the pre-amortization principal, followed by the state reset.

Although the source calls principal deterministic, it is deterministic only conditional on the realized path and reset rule. Its future value is path dependent because the future reference rates are uncertain. Introducing $P$ makes that dependence explicit rather than averaging it away.

If $P\ge0$ and all payments and reset rules scale linearly in $P$, the similarity reduction $V(r,P,t)=P H(r,t)$ removes the principal dimension. For $\varepsilon=0$ the reset becomes

$$
H(r,t_i^-)=g(r)H(r,t_i^+)+(r-r_f)\Delta_i,
$$

with the accrual factor included here as an explicit implementation convention. Positive homogeneity of the worst-case operator preserves this reduction despite nonlinearity. It does not follow for arbitrary fixed fees, nonlinear principal caps, or signed principal scaling.

For $\varepsilon>0$, if the actual rate drives both amortization and interest, a consistent extension minimizes the combined reset expression over the same $\rho\in[r-\varepsilon,r+\varepsilon]$. The source says the band case is more complicated but gives no explicit reset formula. That omission must not be replaced by silently evaluating payment at one adverse rate and amortization at another.

## Static hedging and what market-price matching means

The authors propose holding traded contracts statically alongside the target, then optimizing the combined portfolio value after paying for the hedge. A useful precise reconstruction is

$$
L(X)=\sup_{\theta}\left\{\underline V\left(X+\sum_j\theta_jY_j\right)-C(\theta)\right\},
$$

where $Y_j$ is the complete cash-flow stream of hedge $j$, $\theta_j$ its position, and $C(\theta)$ its time-zero executable cost. This formula describes a lower acquisition value. A corresponding upper sale value is $-L(-X)$ with the appropriate trading-cost convention. The source refers to earlier papers for the detailed optimization rather than printing this objective.

With bid and ask quotes, $C(\theta)=\sum_j[\theta_j^+a_j-\theta_j^-b_j]$, where $\theta_j^+=\max(\theta_j,0)$ and $\theta_j^-=\max(-\theta_j,0)$. Position constraints, shorting restrictions, and available trade sizes should be included. Treating both sides as a single mid-price assumes executable frictionless trading.

The article argues that a traded contract can be hedged one-for-one with itself and hence matches its market price. Exact cancellation explains the mechanism: when $X=Y_k$, choosing $\theta_k=-1$ leaves no future cash flow and realizes the executable sale price of that instrument in the lower-value objective. With a single frictionless price and no model-consistent arbitrage, the bound can coincide with that price. With a bid–ask spread, the corresponding acquisition and sale bounds need not collapse to one number.

The stronger claim that optimization always yields valid exact market matching requires consistency of quotes, the admissible path set, and the allowed trades. If the model declares a traded portfolio to have a guaranteed value exceeding its purchase cost, scalable unconstrained positions can make the optimization unbounded. Self-cancellation alone does not prove that another hedge cannot exploit such an inconsistency. Market matching through static trades is also not evidence that the path constraints predict future rates correctly.

This framework uses static offsets rather than continuous delta hedging in the nontraded short rate. It can still require cash-account financing and specified treatment of intermediate payments. Guarantee language applies only while the path restrictions, contract settlement assumptions, and access to the assumed financing remain valid.

## Bond options require contingent portfolio states

A bond option is harder than a direct short-rate payment because the value of the underlying bond is itself an interval-valued portfolio object. The source avoids simply inserting one chosen bond price into a conventional option formula.

Let $T_0$ be option expiry and $T$ the underlying bond maturity. First solve two continuation portfolios backward from the last relevant payment to $T_0$: one with non-exercise, $U(r,T_0)$, and another with exercise, $W(r,T_0)$. The exercise branch includes the strike outflow at $T_0$ and all subsequent cash flows of the acquired bond, together with existing hedge positions. For a holder who controls exercise, the expiry condition is

$$
V(r,T_0)=\max\{U(r,T_0),W(r,T_0)\}.
$$

Solve backward from that condition to the valuation date. The maximization represents an exercise decision after observing the relevant expiry state; the subsequent adverse-path calculation applies to each remaining branch. A short option cannot be handled by giving the writer the holder's favorable exercise choice. Its bound must use the appropriate opposite-position or game formulation.

The source's final article page states that $n$ bond options require $2^n$ functions to represent all exercise combinations in the direct construction. Text extraction renders this as “2n”; the printed exponent is important. This is an exponential branch count, not linear scaling. Contract structure may permit reductions, but the article provides no general efficient algorithm. Different expiries and mutually dependent exercise decisions require careful state organization.

## A reproducible numerical scheme and analytic checks

The paper gives no grid or solver tolerances. A direct implementation can use backward dynamic programming: discretize time and the representative-rate band, enumerate admissible next representative states respecting the slope constraints, discount the next-step value using feasible actual rates, and select the minimum or maximum. Use interpolation that preserves monotonicity. Apply payment and amortization jumps at their exact contractual dates rather than smearing them over the time grid.

For cash flows independent of the actual rate, an interior short-step lower update has the form

$$
V(r,t)\approx\min_{c,\rho}
 e^{-\rho\Delta t}V(r+c\Delta t,t+\Delta t),
$$

subject to state feasibility. This is a first-order discretization, not an exact formula for a time-varying rate over a finite step. Rate-dependent payments must enter inside the same minimization. Compare successively finer grids and test constant-rate, zero-band, and sign-reversed contracts. A solver should also reproduce positive homogeneity and the inequality between separate and combined worst-case values.

For a positive unit payment after horizon $H$, the adverse representative path is the fastest permitted rise until the upper band is reached; the favorable path is the fastest permitted fall until the lower band is reached. With current state $r_0$ and constant $c^-\le0\le c^+$,

$$
\underline P=\exp\left[-\int_0^H\{\min(r_0+c^+s,r^+)+\varepsilon\}\,ds\right],
$$

$$
\overline P=\exp\left[-\int_0^H\{\max(r_0+c^-s,r^-)-\varepsilon\}\,ds\right].
$$

These are derived validation formulas for a simple claim, not prices reported in the article. They assume the actual-rate tube is not additionally clipped. For a negative unit payment the bounds reverse by sign. If both derivative bounds are zero and $\varepsilon=0$, both reduce to $e^{-r_0H}$. Even a positive bond can have a wide interval when the allowed slopes, band, or horizon are large; allowing unusual paths is not a free robustness improvement.

## Evidence, limitations, and appropriate interpretation

Tables 1 and 2 list the authors' criticisms of conventional stochastic models: distributional assumptions, unstable parameters, curve fitting, tractability-driven choices, uncertain cross-maturity relationships, linearity, and unique prices. Table 3 contrasts those features with their path-set approach. These tables are qualitative arguments, not measured comparisons. Their broad characterization of traditional models should not be mistaken for a theorem that every stochastic-rate model has normally distributed increments or cannot incorporate jumps, spreads, or uncertain parameters.

There is no estimated failure frequency for the admissible band, no sample period, no market quote panel, and no comparison of realized hedge errors. The source gives illustrative rate constraints but no fitted $\varepsilon$, current representative state, amortization schedule, range-note calendar, caplet accrual convention, or executable hedge universe. Those are necessary inputs for a numerical reproduction of a particular transaction. The referenced earlier work may contain additional methods, but they are not results reproduced from this PDF.

The defensible conclusion is that a specified uncertainty set generates coherent nonlinear valuation bounds and creates scope for portfolio-level static hedging. It exchanges probability-model risk for uncertainty-set risk, wider prices, and potentially substantial computational cost. Its robust guarantee is conditional on what the model forbids; difficulty in rejecting a broad set of possible paths does not establish either market accuracy or economic usefulness.
