# Energy Commodity Prices: Is Mean-Reversion Dead?

Hélyette Geman, *The Journal of Alternative Investments*, Fall 2005, pp. 31–45. [Source PDF](../../Finance/CommodityPrices_Geman_2005.pdf). The supplied file has sixteen pages: fifteen article pages and a final copyright notice. References below use journal pages; add thirty to the PDF page number. This is a contemporary modeling perspective supported by market charts and industry statistics, not an estimated statistical test of whether mean reversion vanished.

## Why this matters

A model can fit short-lived deviations around a fixed equilibrium and still misprice a long-lived asset when the equilibrium itself changes. Geman uses the 2000–2005 energy-price expansion to question the practice of anchoring oil and natural-gas valuations to a stationary historical price level. She proposes allowing a moving long-run state and stochastic volatility, then discusses the computational compromise required when valuing contracts with repeated volume decisions.

The practically useful question is therefore how to distinguish temporary scarcity, seasonal variation, and persistent changes in the supply cost or demand environment. The paper does not settle that identification problem. It shows why it matters: gas forward curves shift in level while retaining seasonal structure, long-dated oil prices move, and swing-option values depend on the joint evolution of prices across many exercise dates. A fit to a single spot-price path or a terminal option smile cannot establish that the entire dynamic model is adequate.

The title is deliberately stronger than the evidence. No mean-reversion coefficient, unit-root test, structural-break test, estimation error, likelihood comparison, or out-of-sample pricing result is reported. The proposed alternative of mean reversion toward a moving level is explicitly retained. A reader should take away a model-design problem rather than an empirical finding that the speed of mean reversion equals zero.

## Economic evidence and its dates

The article's information set ends in summer 2005. It reports a \$100 January 2000 investment in the Dow Jones–AIG Commodity Total Return Index exceeding \$200 by March 2005, while the energy subindex reaches approximately \$500 by July. These are index-investment values, not changes in a single cash commodity. Futures index returns can contain roll and collateral components, and the paper does not decompose them. Their growth cannot alone identify the stochastic law of spot prices.

The contextual argument combines demand growth with limited immediately available capacity. World oil demand is reported as 82.3 million barrels per day in 2004, up 3.6%; Chinese demand grows 15.4% and accounts for about one-third of the worldwide increment. The opening discussion gives a global demand increase of 2.5 million barrels per day and spare capacity falling from about three million in 2003 to one million in mid-2004. Brent is quoted near \$60 per barrel on July 8, 2005 and \$66.45 on August 18. These are historical observations and source quotations, not current forecasts.

Natural gas provides the principal structural example. Proven reserves rise from 96.39 trillion cubic meters in 1984 to 142.89 in 1994 and 179.53 in 2004. In 2004, the Middle East and Europe/Eurasia account for 40.6% and 35.7% of reserves. Production is reported as 2,101 billion cubic meters in 1994 and 2,691 in 2004; consumption rises from 2,085 to 2,690. Regional mismatch between reserves and demand motivates investment in pipelines, liquefaction, shipping, and regasification.

Exhibit 5 reproduces projected 2001–2030 gas-supply investment of approximately \$3.145 trillion, comprising \$1.731 trillion in exploration/development, \$673 billion in transmission/storage, \$251 billion in LNG, and \$489 billion in distribution. Rounded component totals sum to \$3.144 trillion. These are forecasts cited from the energy outlook, not realized expenditures or model-estimated parameters. The article does not supply the underlying forecasting assumptions or uncertainty intervals.

Its proposed economic mechanism is plausible but not quantified: transport capacity broadens the set of marginal suppliers and connects markets previously separated by geography. The paper reports regasified LNG costs in North America of \$2.50–\$3.50 per million Btu and imported LNG averaging \$5.51 per million Btu. Its component cost ranges are \$0.50–\$1.00 for exploration/production, \$0.80–\$1.20 for liquefaction, \$0.40–\$1.00 for shipping, and \$0.30–\$0.50 for regasification/storage. These ranges do not define a frictionless global arbitrage band: terminal capacity, delivery timing, contractual commitments, and shipping availability also matter. No route-specific trading simulation is presented.

The regional and technological discussion is a motivation for changing price states. It is not evidence that the particular stochastic differential equations later displayed are identified by those industry numbers. There are also internal presentation problems in peripheral outlook tables: Exhibit 6 prints a 1990 world production total of 3,070 while its listed regional values sum to 2,013 and the “Others” row is blank. The text on p. 35 prints \$16 billion of annual total capital expenditure in the third projected decade while separately assigning \$68 billion to exploration/development in that decade. These figures should not be silently repaired or used as a calibrated input without checking their original source.

## What the forward-curve exhibits actually show

Exhibits 7–10 plot the first fifteen gas contracts on selected June and December dates. The June panels cover 1995–2000 and 2000–2005; the December panels cover 1995–2000 and 2000–2004. Comparing the same calendar month helps expose the seasonal pattern, but these are selected annual snapshots, not a complete panel used in a statistical regression.

The June 2005 curve lies around seven at the nearby end and has a visible winter hump above eight before declining toward the longer contracts. December 2000 instead shows a nearby price close to ten falling toward five farther out. These approximate readings from the charts demonstrate two different movements: a temporary front-end spike and a broader change in the level of the curve. The PDF provides no underlying price table, contract settlement convention, timestamp, exact units on every graph, or procedure for handling delivery-calendar changes.

Exhibits 13–14 show daily front-month gas and crude-oil prices from approximately January 2003 to August 2005. Both have appreciable fluctuations during the upward movement; the oil series rises from the low thirties toward the upper sixties. A front-month continuous series is not a fixed-maturity claim: rolling introduces a further construction choice. The source does not document its roll rule or any back adjustment.

Exhibit 15 plots the twenty-ninth-contract price minus the first-contract price from late 1995 into 2005. The spread is usually negative, with positive episodes after September 2001 and near the sample endpoint. This is an absolute price spread, not an annualized percentage carry return. The contract-number separation need not equal a constant exact time to maturity for every observation.

Geman interprets these positive episodes as evidence of uncertainty affecting long-dated prices and proposes the long-term oil price as a useful state variable. That is an economic interpretation, not an identified risk-premium decomposition. A slope can move because of expected future scarcity, current convenience yield, storage costs, financing, or priced risk. The sign of the observed spread does not uniquely reveal which component changed, and a higher long-dated futures price does not establish the sign of the expected excess return from buying that contract.

## Price dynamics: fixed versus moving equilibrium

The paper reviews several inherited models before proposing a richer specification. A geometric Brownian motion satisfies

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t.
$$

With constant coefficients, $E[S_{t+h}\mid S_t]=S_te^{\mu h}$ and $\operatorname{Var}(\log S_{t+h}\mid S_t)=\sigma^2h$. These are exact consequences of the model, not estimates in the article. A visually rising sample path is compatible with this law, but also with a mean-reverting law whose equilibrium has risen or whose initial price is below equilibrium.

The reviewed additive Ornstein–Uhlenbeck process,

$$
dX_t=\kappa(a-X_t)dt+\sigma\,dW_t,
$$

has conditional mean $a+(X_t-a)e^{-\kappa h}$ and conditional variance $\sigma^2(1-e^{-2\kappa h})/(2\kappa)$. It is Gaussian and can be negative. Using it for a log price rather than a price avoids negative prices. The source also recalls square-root diffusions; their nonnegativity should be distinguished from strict positivity. For $dX=\kappa(a-X)dt+\sigma\sqrt X\,dW$, the familiar sufficient boundary condition $2\kappa a\ge\sigma^2$, with positive initial value, prevents zero from being reached. Positive parameter names alone do not establish that condition.

The source's first positive-price mean-reverting example on p. 41 is

$$
dS_t=\kappa(b-\log S_t)S_tdt+\sigma S_t\,dW_t.
$$

Itô's formula gives

$$
d\log S_t=\kappa\left(b-\frac{\sigma^2}{2\kappa}-\log S_t\right)dt+\sigma\,dW_t.
$$

Thus $b$ is not the stationary mean of the log price; that mean is $b-\sigma^2/(2\kappa)$. The long-run mean price is $\exp\{b-\sigma^2/(4\kappa)\}$ under this constant-coefficient specification. These corrections follow from the displayed SDE and distinguish a drift target from an unconditional price mean. They are not additional empirical results attributed to Geman.

The second example has level reversion with proportional noise, $dS_t=\kappa(b-S_t)dt+\sigma S_t\,dW_t$. It has a different distribution and boundary structure from log-OU. Interchanging them merely because both have positive prices changes conditional variance, tails, and long-horizon valuation.

Equation (5), p. 39, combines a reverting log-price drift, an evolving equilibrium state, and stochastic variance. Preserving its printed parameter reuse, write $V_t=\sigma_t^2$:

$$
\begin{aligned}
dS_t&=\kappa(L_t-\log S_t)S_tdt+\sqrt{V_t}S_t\,dW_t^1,\\
dL_t&=\mu L_tdt+\eta L_t\,dW_t^2,\\
dV_t&=a(b-V_t)dt+\eta\sqrt{V_t}\,dW_t^3.
\end{aligned}
$$

The three Brownian motions are pairwise correlated. Their correlation matrix must be positive semidefinite to define a joint simulation. The paper gives no numerical coefficients, correlation matrix, estimation procedure, or market-price-of-risk specification. It uses the same $\eta$ in the last two equations; introducing different volatilities would be an extension, not a faithful transcription.

Here $L_t$ enters the *log-price* drift, even though the text describes it economically as a long-term level. After transforming the first equation,

$$
d\log S_t=\left[\kappa(L_t-\log S_t)-\frac12V_t\right]dt+\sqrt{V_t}\,dW_t^1.
$$

The instantaneous target for log-price drift is therefore $L_t-V_t/(2\kappa)$, and it evolves with both equilibrium and variance. Because $L_t$ itself follows a geometric diffusion, the joint process need not have a stationary distribution. The model accommodates local pullback without requiring a constant unconditional long-run price. It is an illustrative proposal, not a solved affine futures-pricing model or an estimated replacement for the fixed-level alternatives.

Seasonality is removed through Equation (6), $S_t=e^{\gamma_t}S_t^{\rm observed}$, where $\gamma_t$ is deterministic. This direction matters: observed price is $e^{-\gamma_t}S_t$ under the printed convention. The function, calendar basis, normalization, and estimation window are not supplied. It should not be replaced by the opposite sign without redefining the seasonal function.

## Convenience yield, probability measures, and calibration

Equation (2) gives the constant-carry relation

$$
F_t(T)=S_t\exp\{(r-y)(T-t)\},
$$

where $y$ is convenience yield net of storage cost. This simple expression assumes the relevant carry rates are fixed over the interval. It should not be used unchanged after declaring $y$ an arbitrary stochastic state. Under deterministic time-dependent carry the corresponding exponent is an integral, and under stochastic convenience yield the forward price generally requires conditional valuation.

The reviewed Gibson–Schwartz specification, Equation (3), is explicitly under the physical measure: spot follows geometric Brownian motion and convenience yield is OU, with correlated shocks. Its drift parameters cannot simply be inserted into a pricing expectation. The source separately assumes no relevant interest-rate/commodity dependence when identifying forwards with futures. A precise sufficient condition is deterministic interest rates, or the required factorization under the pricing measure; merely setting an instantaneous Brownian correlation to zero in an arbitrary coupled model does not guarantee that factorization.

For swing valuation, Geman recommends reducing the number of stochastic factors and using local volatility. Equation (8), under the pricing measure, has the structure

$$
dS_t=(r-y)S_tdt+\sigma(S_t)S_t\,dW_t^{Q}.
$$

The article proposes inferring convenience yield from the current forward curve and local volatility from vanilla options. It supplies neither a calibrated surface nor an inversion algorithm. A constant $y$ and a time-homogeneous function $\sigma(S)$ cannot generally reproduce an arbitrary seasonal forward curve and an arbitrary option surface across maturities.

For a practical extension with deterministic rates, use time-dependent carry and local volatility. If $F_0(T)$ is differentiable, choosing $r(T)-y(T)=\partial_T\log F_0(T)$ matches the initial curve in a multiplicative diffusion with the appropriate martingale/integrability conditions. A function $\sigma(T,S)$ provides the time flexibility needed for general vanilla calibration. These are implementation requirements derived from the proposed direction, not procedures executed in this article. Matching each terminal distribution still does not guarantee the correct conditional transitions for repeated-exercise claims.

## Reconstructing the swing-option decision problem

Equation (1) sets daily volume limits $x\le q_t\le y$ and lifetime limits $A\le\sum_{t=0}^{H}q_t\le B$, with each unit purchased at a fixed price $k$. The bounds may be expressed relative to a reference volume, such as 90% and 110%. If $A=B$, total volume is fixed but its timing can remain optional. Other contractual limits may constrain exercise days or the interval between swings.

The source identifies cumulative consumption as a necessary state. Let $Q$ be volume already taken and $n$ the number of remaining delivery dates including today. The feasible current-volume set, for constant daily bounds, is

$$
\mathcal A_n(Q)=
\left[\max\{x,A-Q-(n-1)y\},\,
\min\{y,B-Q-(n-1)x\}\right].
$$

An empty interval means the state cannot satisfy the contract. This derived expression is important in a numerical implementation: independently clipping a volume to daily limits does not ensure that the terminal obligation can still be met.

For a buyer who can value a delivered unit at the current market price, a discounted payoff is the sum of $q_t(S_t-k)$. A Bellman reconstruction under a chosen pricing measure is

$$
V_n(s,Q)=\sup_{q\in\mathcal A_n(Q)}
\left\{q(s-k)+E^Q\left[D_{t,t+1}V_{n-1}(S_{t+1},Q+q)\mid S_t=s\right]\right\}.
$$

At expiry, feasible completed volume has zero continuation value; infeasible volume is forbidden or receives the specified contractual penalty. This is a reconstruction of the control problem, not an equation or numerical experiment printed by Geman. The objective must change if consumption utility, resale restrictions, make-up rights, take-or-pay penalties, or delivery costs differ from that mark-to-market interpretation.

A one-factor tree needs both price and cumulative-volume grids. A richer model adds the equilibrium and variance states, increasing the continuation-value problem substantially. Least-squares Monte Carlo replaces conditional expectations with regressions, but requires separately specified basis functions, exercise constraints, simulation size, and validation. The paper references tree, discrete-forest, and Monte Carlo approaches without providing those settings or reporting a timed accuracy comparison. Its computational preference for local volatility is therefore a reasoned design judgment, not a measured speed/accuracy frontier.

## What remains unestablished

The paper offers no replicable empirical competition between fixed mean reversion, moving equilibrium, and geometric Brownian motion. Exact replication of even its charts needs index identifiers and return conventions, futures settlement histories, maturity maps, continuous-contract rules, calendar dates, units, and source vintages. There is no training/validation split, trading rule, leverage policy, cost-adjusted portfolio result, or uncertainty interval to reconstruct.

A rigorous use of its ideas would separate three tasks: estimate physical price dynamics, calibrate risk-neutral derivative prices, and solve the contract's control problem. The source motivates all three but does not complete any joint estimation. Using a pricing fit as proof of a physical trend, or treating rising futures prices as a measured positive risk premium, would conflate distinct questions.

The historical evidence supports the need to stress persistent movements in the equilibrium level and the shape of the curve. It does not justify abandoning temporary mean reversion or selecting a stochastic model solely because its drift resembles the most recent price path. For long-lived energy assets and swing books, the valuable contribution is this explicit sensitivity to state choice, seasonality, and computational dimension, together with a clear warning against assuming that a historical price anchor remains fixed.
