# Comment on Asset Pricing Explorations for Macroeconomics

John Y. Campbell, NBER Macroeconomics Annual 7 (1992), pp. 165–169. Source: [StochasticDiscount_Campbell_1992.pdf](../../Finance/StochasticDiscount_Campbell_1992.pdf), six PDF pages. The scan includes the preceding article's Appendix 2 before Campbell's comment, and the beginning of Philippe Weil's comment after it. Those adjacent passages are not Campbell's contribution.

## Why this matters

Campbell explains both the usefulness and the limits of evaluating macroeconomic asset-pricing models through Hansen–Jagannathan bounds. His central objection is that an apparently successful stochastic discount factor can reflect a fragile transformation of badly measured aggregate consumption. A model must ultimately explain asset prices, cash flows, and their dynamics, not just place a point inside a feasible mean–standard-deviation diagram. This is a methodological comment rather than a new model, dataset, or econometric result.

## What the diagram actually tests

A stochastic discount factor $M$ prices a gross return $R$ when $E[MR]=1$. A collection of observed returns restricts the possible moments of $M$. In the usual return diagram, mean lies on the vertical axis and standard deviation on the horizontal axis. In the discount-factor diagram the axes are reversed: one calculates the smallest feasible standard deviation for each candidate mean. Campbell explains this geometry on printed pp. 166–167.

The reciprocal of a proposed discount-factor mean, $R_f=1/E[M]$, acts as a hypothetical riskless gross return. The tangent from that return to the risky-return opportunity set has the maximal Sharpe ratio. The corresponding line from the origin to the discount-factor boundary has the same slope. Thus, holding $E[M]$ fixed, a dataset with a larger attainable Sharpe ratio requires a more volatile discount factor.

For clarity, the familiar scalar bound can be reconstructed from the pricing equations. Let $m=E[M]>0$ and let $R^e$ be an excess return relative to a priced riskless asset. Then

$
0=E[MR^e]=mE[R^e]+\operatorname{Cov}(M,R^e),
$

so Cauchy–Schwarz gives

$
\frac{\sigma(M)}{m}\geq\frac{|E[R^e]|}{\sigma(R^e)}.
$

Maximizing the right side over admissible excess-return portfolios produces the Hansen–Jagannathan restriction. This equation is an explanatory reconstruction of the geometry discussed in the comment; Campbell does not introduce a new version of the inequality here. Conditions such as positive discount factors and the full vector of pricing restrictions impose additional requirements that a two-moment plot does not exhaust.

Campbell identifies two uses. The first compares return datasets: which presents a larger challenge for an asset-pricing explanation? The second compares models by plotting the moments of their implied discount factors against the common feasible region. A candidate outside is inconsistent with the moment restriction. A point inside passes that necessary check; it need not satisfy every pricing equation or establish that its preference specification is economically credible.

## Two different sources of uncertainty

Sampling uncertainty affects both sides of the comparison. Campbell calls for uncertainty estimates around the empirical boundary and around each model's implied discount-factor moments. If realized discount factors were observed correctly, generalized method of moments would provide a route to moment standard errors. Treating candidate points as known constants while drawing confidence bands only for the frontier is incomplete.

His more substantial concern is that realized discount factors are themselves inferred from imperfect consumption data. Time aggregation, sampling procedures, and price indexes can create errors. Unmeasured quality improvements can distort the real-consumption series. Aggregation can fail more fundamentally: aggregate consumption growth may reflect replacement of older cohorts by richer new cohorts rather than an individual's optimal postponement of consumption. Stockholders and nonstockholders can have systematically different consumption dynamics. Liquidity constraints can disconnect aggregate consumption from the marginal investor's decisions.

Near-optimality is another complication. A statistically detectable departure from the textbook consumption first-order condition can have small utility cost and may arise from small trading or optimization costs. Consequently a statistically precise aggregate series need not measure the theoretical marginal utility that prices securities.

High risk aversion and habit amplify this problem. For illustration, a CRRA discount factor has

$
\log M_{t+1}=\log\beta-\gamma\,\Delta\log C_{t+1}.
$

If observed log consumption differs from true log consumption by $\epsilon_t$, the inferred log discount factor differs by $-\gamma(\epsilon_{t+1}-\epsilon_t)$. This algebra makes Campbell's sensitivity argument concrete; it is not an estimated measurement-error model supplied by the comment. There is no reported calibration for $\gamma$, no estimated error variance, and no numerical sensitivity threshold in this source.

The resulting warning is substantive: finding a nonlinear consumption transformation that clears the bound does not by itself identify the correct utility function. A model can accommodate the diagram while magnifying imperfections in the measured input. Campbell presents a caution about inference, not a proof that consumption-based models are universally unidentifiable.

## Suggested research designs

Campbell suggests longer-horizon applications, where some consumption measurement problems may be less severe; asset-portfolio proxies for consumption at low frequencies; deriving consumption as a function of more measurable state variables; and independent evidence from investment and firm behavior. These are research directions. The comment supplies no particular horizon, proxy portfolio, state-vector specification, or executable estimation design. Longer horizons also change the statistical problem; the text does not establish that they eliminate every type of measurement error.

A useful implementation motivated by this discussion would specify the horizon and test assets before fitting preferences, report uncertainty in model moments as well as return bounds, and vary the consumption measure transparently. Such a design is an implication of the critique, not an empirical exercise performed in this five-page comment. It would still need the full Euler-equation restrictions if the objective were model validation rather than moment screening.

## Return dynamics as an additional target

The broader criticism on printed pp. 168–169 is that the evaluated models take realized-return second moments as given. A macroeconomic model should explain those returns jointly with other aggregate quantities. Campbell summarizes contemporary research as indicating that price changes can be traced to dividend news or expected-return news, with the latter accounting for much of observed price variation. Weak short-horizon return predictability can coexist with this claim: persistent small shifts in expected returns have large effects on current prices.

He also emphasizes the similarity of the broad findings for real returns and excess returns over Treasury bills, and cyclical expected returns that are high late in recessions and low late in expansions. These are his synthesis of existing evidence. The comment contains no fresh estimates, numerical decomposition, sample definition, forecast comparison, or trading strategy supporting an independent re-estimation of those facts.

The modeling implication is a dynamic economy with persistent variation in risk or risk aversion and hence in risk premia. Changing real interest rates alone, with constant premia, are insufficient for that agenda. Campbell favors examining equity as a claim on installed capital in a production economy with investment adjustment costs, rather than relying solely on exchange-economy claims to aggregate consumption. The comment stops at this proposed direction: it gives no production function, adjustment-cost parameters, equilibrium algorithm, or quantitative fit. Its durable contribution is a set of validation requirements that prevents a successful moment diagram from being mistaken for a complete macroeconomic explanation.
