# Dynamic Portfolio Optimization with Transaction Costs: Heuristics and Dual Bounds

**Authors:** David B. Brown and James E. Smith. **Publication:** *Management Science* 57(10), October 2011, pp. 1752–1770. **DOI:** 10.1287/mnsc.1110.1377. **Source:** `Finance/OptimalTrading_BrownSmith_2011.pdf`, 19 PDF pages. References below give journal pages, with PDF page where helpful. **Type:** computational portfolio-optimization research with mathematical bounds and simulated experiments.

## Contribution and why the upper bound matters

The paper addresses a practical obstacle in dynamic portfolio choice: transaction costs make the current vector of holdings a state variable. A frictionless investor can rebalance freely, so current wealth and market conditions often suffice. With costly trading, two investors with the same wealth and forecasts can optimally act differently because one already holds the desired assets and the other would have to pay to acquire them. The resulting dynamic program becomes prohibitively large even with a modest number of assets.

Brown and Smith contribute inexpensive trading heuristics and a way to assess how much performance those heuristics might leave unrealized. Their principal heuristics use a frictionless value function as an approximation, but incorporate current trading costs and a limited representation of future holding benefits. The strongest results come from a modified one-step policy and a rolling buy-and-hold policy. Neither attempts to solve the complete high-dimensional dynamic program.

The more distinctive methodological contribution is the dual bound. An investor with perfect knowledge of all future returns provides an upper bound, but normally an absurdly generous one. The paper penalizes the use of advance information so the resulting clairvoyant optimization remains tractable while producing a much tighter upper bound. Comparing a feasible heuristic's expected utility with this bound measures the remaining room for improvement within the specified model.

That qualification is essential. A small duality gap is evidence that the heuristic nearly solves the assumed stochastic control problem. It is not evidence that the return model is accurate, that transaction costs are correctly calibrated, or that realized future investment performance will match the simulated certainty equivalent. The paper evaluates optimization quality under controlled assumptions, rather than reporting an out-of-sample trading backtest.

## Portfolio state, cash accounting, and objective

Time is discrete, $t=0,\ldots,T$, with $n$ risky assets and one cash asset. Risky-asset gross returns are $r_{t+1,i}\ge0$ and the risk-free gross return $r_f$ is constant. The vector $x_t$ contains monetary risky-asset holdings before trading; $c_t$ is cash. A trade vector $a_t$ contains monetary purchases when positive and sales when negative. Transaction costs $\kappa(a_t)$ are nonnegative, convex, and zero for a zero trade (journal p. 1754; PDF p. 3).

The state equations are

$$
x_{t+1}=r_{t+1}\odot(x_t+a_t),\qquad
c_{t+1}=r_f\left(c_t-\mathbf1'a_t-\kappa(a_t)\right),\qquad
w_t=\mathbf1'x_t+c_t.
$$

The componentwise product $\odot$ applies each asset return to its own post-trade holding. Costs are deducted from cash when the trade occurs, before the risk-free return is earned. Ignoring this accounting detail or deducting costs only from final utility would change feasibility and compounding.

The numerical work uses symmetric proportional costs,

$$
\kappa(a_t)=\delta\sum_{i=1}^{n}|a_{t,i}|.
$$

The general formulation permits different buy and sell rates, quadratic costs, or other convex cost functions. It does not directly cover fixed ticket fees, concave volume discounts, or nonconvex portfolio restrictions under the same convexity guarantees. The transactions in the numerical experiment are monthly rebalancing decisions; there is no intraday order-book execution state.

The investor maximizes expected utility of terminal marked wealth, $\mathbb E[U(w_T)]$, with nondecreasing concave $U$. The experiments use constant-relative-risk-aversion utility,

$$
U(w)=\frac{w^{1-\gamma}}{1-\gamma},\qquad\gamma>0,
$$

with logarithmic utility as the limiting case $\gamma=1$. The reported parameter cases all have $\gamma>1$. Terminal wealth is marked at market rather than liquidated net of a final sale cost. The authors explain that liquidation value could be used, but that would change the numerical answers.

Most experiments prohibit short risky positions and borrowing:

$$
x_t+a_t\ge0,\qquad c_t-\mathbf1'a_t-\kappa(a_t)\ge0.
$$

A separate experiment permits signed positions subject to gross leverage,

$$
\sum_i|x_{t,i}+a_{t,i}|\le l\left(\mathbf1'x_t+c_t-\kappa(a_t)\right).
$$

The broad assumption is a closed convex set of post-trade holdings that remains feasible if cash is increased. These conditions preserve convexity and support the relaxations used later.

## Predictability and the exact dynamic program

A Markov state $z_t$ contains observable predictors of future returns. Conditional on $z_t$, next-period returns and next-period state are independent of earlier history, though they may be jointly dependent on each other. The exact state is therefore $(x_t,c_t,z_t)$, with terminal value $V_T(x,c,z)=U(\mathbf1'x+c)$ and recursion

$$
V_t(x,c,z)=\max_{a\in\mathcal A_t(x,c)}\mathbb E\left[V_{t+1}\left(r_{t+1}\odot(x+a),r_f[c-\mathbf1'a-\kappa(a)],z_{t+1}\right)\mid z_t=z\right].
$$

The value is concave in holdings and cash, and the one-period optimization is a concave maximization over a convex feasible set. The challenge is the number of states, not a lack of local convexity. With 100 grid points for each holding and cash, plus 20 predictor states, three risky assets already imply two billion states per date. Ten risky assets without a predictor would require $100^{11}=10^{22}$ grid points (journal p. 1755).

The frictionless model sets $\kappa=0$ and reduces the financial state to wealth. Let $V_t^f(w,z)$ denote its value. For power utility and homogeneous constraints,

$$
V_t^f(w,z)=\frac{w^{1-\gamma}}{1-\gamma}\psi_t(z).
$$

Only the predictor-state function $\psi_t$ needs to be stored. The frictionless value is an upper bound for the costly problem because removing costs enlarges feasible possibilities and raises wealth. It also supplies the continuation-value approximation used by the heuristics.

The frictionless policy is not necessarily myopic. If next-period returns and the next predictor state are correlated, the investor may hedge against changes in future opportunities. When they are conditionally independent, the recursion factors and a one-period utility maximization suffices. The paper retains this distinction so predictable-return experiments include intertemporal opportunity effects rather than merely changing a static mean vector every month.

## Heuristic policies and their different biases

The cost-blind policy follows the allocation fractions recommended by the frictionless model, while actual simulation still deducts transaction costs. It is a benchmark for the error of treating rebalancing as free. When forecasts or target weights move substantially, this policy can trade aggressively to capture benefits smaller than their implementation costs. The simulation must maintain the stated cash feasibility while moving toward target fractions; frictionless dollar holdings cannot simply be copied without allowing for cost payments.

The one-step policy pays current costs but uses the frictionless continuation value:

$$
a_t^{\mathrm{OS}}\in\arg\max_{a\in\mathcal A_t(x_t,c_t)}\mathbb E\left[V_{t+1}^f\left(r_{t+1}'(x_t+a)+r_f[c_t-\mathbf1'a-\kappa(a)],z_{t+1}\right)\mid z_t\right].
$$

This objective remains concave in the current trade. It requires solving one convex problem at every visited simulation state, but avoids storing a holdings-dependent value function. The high-dimensional expectation still needs numerical integration.

The unmodified one-step policy tends to trade too little. By assuming costless adjustment next period, it understates the lasting benefit of paying once to move closer to a desirable portfolio now. An investor may gain from an improved position for several future months, while the one-step approximation sees only the current month before free future rebalancing erases the disadvantage of waiting (journal pp. 1756–1757).

The modified one-step policy reduces the cost appearing in the decision objective by a divisor. The main experiments divide by $\min(6,T-t)$, interpreting the benefit of adjustment as lasting approximately six months, with truncation near the terminal date. This is an approximation to continuation value, not an actual fee reduction. Realized wealth and cash constraints still use the true transaction costs. The divisor is a tuning parameter and is not derived as a universal optimal horizon.

The rolling buy-and-hold policy instead assumes the chosen post-trade holdings cannot be changed for $h$ periods. It optimizes

$$
\mathbb E\left[V_{t+h}^f\left((r_{t+h}\odot\cdots\odot r_{t+1})'(x_t+a)+r_f^h[c_t-\mathbf1'a-\kappa(a)],z_{t+h}\right)\mid z_t\right],
$$

with the horizon truncated appropriately at the terminal date. The main experiments use $h=6$ months. In actual simulation the investor re-solves next month, so the policy is a rolling approximation rather than a binding commitment to hold for six months. This captures a longer-lived benefit from rebalancing while keeping each decision a convex problem.

These policies have different approximation errors. Cost blind overvalues small adjustments; one step undervalues persistent position benefits; rolling buy-and-hold overstates the inability to adapt within its artificial horizon. Tuning the divisor or horizon balances these effects. A better value of a heuristic's internal objective does not guarantee a better realized policy under the original model, which is why external simulation and upper bounds are needed.

## Information relaxation and valid upper bounds

A feasible policy is nonanticipative: its time-$t$ trade can depend on observed returns and states only through time $t$. The dual construction removes that restriction and lets the optimizer inspect the whole future path. For a realized path $(r,z)$, it chooses the entire trade sequence $a$ subject to the original pathwise portfolio constraints. A penalty $\pi(a,r,z)$ charges for use of the extra information (journal pp. 1757–1758).

Dual feasibility means

$$
\mathbb E[\pi(\alpha(r,z),r,z)]\le0
$$

for every feasible nonanticipative policy $\alpha$. Because the penalty is subtracted, a legitimate policy is not disadvantaged in expectation. Therefore

$$
\sup_{\alpha\ \mathrm{nonanticipative}}\mathbb E[U(w_T(\alpha))]
\le\mathbb E\left[\max_{a\in\mathcal A(r)}\{U(w_T(a,r))-\pi(a,r,z)\}\right].
$$

The bound is evaluated by drawing return/state paths, solving one deterministic inner optimization per path, and averaging its optimal value. With a penalty convex in the trade sequence, terminal utility minus penalty remains concave, so the inner problem is tractable. A zero penalty gives ordinary perfect foresight and is valid but typically much too loose.

The duality result concerns expected values under the stated probability law. A finite Monte Carlo estimate has sampling error and can occasionally lie slightly below the estimated feasible-policy value. The authors report such tiny negative estimated gaps and interpret them as sampling variation, not a violation of weak duality. An implementation should preserve common random paths and estimate the uncertainty of the gap itself.

## Two penalty families

The first family uses approximate continuation values. For a generating function $g_t$ depending on decisions through time $t$, form the martingale-difference penalty

$$
\pi(a,r,z)=\sum_t\left[g_t(a,r,z)-\mathbb E\{g_t(a,\widetilde r,\widetilde z)\mid\mathcal F_t\}\right].
$$

If the exact continuation value is used, the construction can produce an exact bound. But direct substitution of a concave approximate value function creates positive and negative curvature terms in the penalized objective, potentially destroying convexity. The authors avoid that problem by linearizing the approximate continuation value around trades from a fixed feasible heuristic.

For proportional costs, buys and sells are represented separately so the resulting penalty is linear in those components. The gradient combines the derivative of the frictionless value with derivatives of future wealth with respect to past trades. For a purchase in asset $i$ at time $\tau$, that wealth derivative is the product of subsequent risky gross returns minus the compounded cash opportunity cost including the purchase fee. The analogous sale derivative uses the sale-cost convention. Conditional expectations determine the penalty weights once per simulated path, rather than requiring reintegration at every inner-optimizer iteration (journal p. 1759).

One version uses the modified one-step continuation approximation; another uses the rolling buy-and-hold continuation. Linearization affects bound tightness, but the conditional-centering construction is what supplies dual feasibility. A heuristic's continuation approximation need not be an exact value function to generate a valid centered penalty.

The second family is the paper's new gradient-based construction. Suppose an approximating problem with terminal wealth $\widehat w_T$ has a known optimal nonanticipative policy $\widehat\alpha^*$ and a convex feasible set containing the original problem's feasible policies. A penalty can be formed from the pathwise utility gradient at that policy:

$$
\widehat\pi(a,r,z)=\nabla_a U\left(\widehat w_T(\widehat\alpha^*(r,z),r)\right)'\left[a-\widehat\alpha^*(r,z)\right].
$$

The expected first-order optimality condition for the approximate problem makes this dual feasible. It is not generally valid to take an arbitrary unoptimized policy, attach its terminal gradient, and claim an upper bound. Optimality for the chosen approximate wealth function and inclusion of feasible sets are the crucial theorem assumptions (journal pp. 1759–1761).

The frictionless gradient penalty uses zero-cost wealth and the frictionless optimal policy. Its inner bound is pathwise no larger than the corresponding frictionless utility, so it must improve upon or equal the simple no-cost upper bound. The paper also studies a modified gradient construction based on a lower-dimensional approximate problem with fees on post-trade positions rather than on changes in positions. The chosen position fee is the proportional trade fee divided by the number of periods. Full details of these constructions and proofs are assigned to the separate online appendix; exact implementation must verify the theorem's feasibility conditions rather than infer them solely from this description.

## Numerical experiment design

All main simulations start with normalized wealth one entirely in cash, use monthly decisions, and evaluate 1,000 sample paths. The factorial settings are horizons of 6, 12, 24, and 48 months; symmetric transaction-cost rates of 0.5%, 1%, and 2%; and relative risk aversion 1.5, 3, and 8. Most cases prohibit shorts and borrowing. These costs are material portfolio-rebalancing frictions, not a calibration to modern liquid-equity per-trade spreads (journal pp. 1761–1762).

The first return model has three risky size-sorted equity portfolios, one dividend-yield predictor, and jointly Gaussian innovations in log returns and predictor dynamics:

$$
\begin{pmatrix}\log r_{t+1}\\z_{t+1}\end{pmatrix}
=\begin{pmatrix}a_r+b_rz_t\\a_z+b_zz_t\end{pmatrix}
+\begin{pmatrix}e_{t+1}\\v_{t+1}\end{pmatrix}.
$$

It is based on Lynch's 1927–1996 estimates, uses inflation-adjusted returns, starts at neutral predictor $z_0=0$, and has monthly risk-free gross return 1.00042. Predictor values are approximated on 19 grid points, with three Gaussian quadrature points per risky asset, giving $3^3\times19=513$ joint outcomes. The quadrature matches the relevant moments of log returns through fifth order as described in the paper.

The second model has ten risky indices and no predictor: five equity indices, three bond indices, a real-estate index, and a one-to-five-year Treasury index. Log returns are independent over time with multivariate Gaussian innovations. Parameters are estimated from monthly data for 1981–2006; returns are nominal and risk-free monthly gross return is 1.0048. A Stroud cubature formula uses $2^{10}+2(10)=1,044$ points to approximate the joint normal distribution with fifth-degree moment accuracy.

A key design choice is that simulation draws use the same discrete return distributions as the dynamic programs, heuristic expectations, and penalty expectations. Thus the reported bound comparisons are internally consistent for the discretized model. They do not certify the optimum of the unbounded continuous Gaussian model merely because the quadrature matches several moments.

The provided PDF does not contain the numerical coefficient vectors, covariance matrices, transition probabilities, or all supplementary result tables. It points to a separate online appendix, absent from the local source files inspected for this summary. Those inputs are required for exact numerical replication. The complete experimental architecture can be reconstructed from the article; exact published numbers cannot be reproduced responsibly by inventing missing calibration parameters.

## Performance measures and uncertainty

For each policy and bound, the authors estimate expected terminal utility and convert it to an annualized certainty-equivalent gross return $R_{\mathrm{CE}}$ satisfying

$$
\widehat\mu=U\left(w_0R_{\mathrm{CE}}^{T/12}\right).
$$

Reported percentage returns are $100(R_{\mathrm{CE}}-1)$. A dual upper bound in utility transforms monotonically into an upper bound on certainty-equivalent return. This is a risk-adjusted performance metric under the chosen utility, not the ordinary average return.

Turnover is average monthly absolute traded monetary value divided by the normalized initial wealth, $T^{-1}\sum_t\sum_i|a_{t,i}|$. It is not normalized by contemporaneous wealth each month. In a buy-and-hold policy starting from cash, initial investment alone therefore contributes roughly $1/T$ to monthly turnover, even if there is no subsequent rebalancing.

The simulation uses frictionless terminal utility as a control variate because its expected value is known from the previously solved frictionless dynamic program. This greatly reduces uncertainty when costly and frictionless outcomes are highly correlated. Standard errors of certainty equivalents and gaps are obtained using the delta method. Very small errors establish precision for the assumed distribution, not robustness to estimating the underlying return parameters (journal p. 1764).

## Main results and the size of the remaining optimization gap

In the three-asset predictable-return model at twelve months, the modified one-step and rolling buy-and-hold policies consistently outperform cost-blind and unmodified one-step policies. At risk aversion 3 and 1% transaction costs, cost blind delivers a 1.40% annualized certainty equivalent and one step 1.65%, compared with 3.20% for modified one step and 3.21% for rolling buy-and-hold. The best upper bound is 3.43%, giving a 0.22-percentage-point gap. The no-cost upper bound is 3.99%, while unpenalized perfect foresight gives 46.39%, illustrating the importance of a meaningful information penalty (Table 2, journal p. 1765).

At lower risk aversion 1.5 and 2% costs, cost blind falls to -2.74% and one step earns only 0.51%, effectively remaining in cash. The two stronger heuristics earn about 5.03%; the best bound is 5.32%. Monthly turnover is around 40% of initial wealth for cost blind, zero for unmodified one step, and roughly 6.6%–6.7% for the stronger policies. Their advantage comes from avoiding both excessive rebalancing and excessive inaction.

Across the twelve-month three-asset cases, gaps range from 0.09 to 0.29 percentage points, averaging 0.19. At 48 months, the mean gap is 0.32 and the worst is 0.62, for low risk aversion and high costs. Higher cost and lower risk aversion generally make the approximation harder. The rolling and modified one-step policies perform similarly, while different penalty families supply the best bound in different cases.

The ten-asset model without predictability is often easier despite having more assets. Target allocations do not respond to a changing predictor, so avoiding frequent small rebalances can be nearly optimal. At risk aversion 1.5 and 1% costs, both strong heuristics and the best bound are 12.50% to reported precision. At risk aversion 3 and 1% costs, the best heuristic is 10.79% and the best bound 10.81%, a 0.02-point gap (Table 3).

There are exceptions. At risk aversion 8 and 2% costs, the cost-blind policy initially has the best heuristic value, 7.19%, while the modified and rolling policies are about 7.15% and 7.14%. The best bound is 7.71%, leaving 0.52 points. This case shows that an intuitively cost-aware heuristic is not uniformly superior without tuning.

Changing horizons or divisors improves those difficult cases. In the ten-asset high-risk-aversion example, a twelve-month rolling horizon raises the feasible certainty equivalent to 7.61% and gives a 7.64% bound, reducing the gap to 0.03 points. In the hardest long-horizon predictable-return case, tuning reduces the gap from 0.62 to about 0.47 points. The bound helps distinguish a poor heuristic from a merely loose certificate, although the authors acknowledge both can sometimes be improved (journal pp. 1766–1768).

## Leverage, computation, and practical limits

The leverage experiment uses ten assets, twelve months, risk aversion 3, 1% costs, and gross-exposure limits from one to five. At leverage five, rolling buy-and-hold earns about 13.15%, the best bound is 13.61%, and the reported gap is 0.47 points after rounding. Cost blind earns 9.72%; the frictionless upper bound is 18.33%. Greater feasible leverage increases optimal opportunity but also magnifies the effect of trading and approximation errors.

The source explicitly warns that leverage results depend on discretization. Under the original unbounded lognormal return model with the chosen power utility, borrowing or shorting can create a positive probability of terminal outcomes with infinitely negative utility, so the continuous model would not recommend them. The finite return grid removes those extreme outcomes and can make leveraged positions attractive. This is a substantive model difference, not a negligible numerical approximation (footnote on journal p. 1768).

The code used Matlab and MOSEK on one processor of a 2.55 GHz Core 2 Quad machine with 3.25 GB RAM. Most evaluation time went to the heuristics because each path and month requires a convex problem with high-dimensional expectations. The dual calculation solves one deterministic problem per path, with roughly $nT$ or $2nT$ trade variables and precomputed penalty weights. Although full simulation evaluation can take many minutes, generating a single current recommendation requires only one heuristic solve and is reported to take a fraction of a second on that hardware.

The reusable contribution is a disciplined computational workflow: specify a realistic convex portfolio model; solve a simpler continuation problem; construct feasible trading policies; evaluate them on shared paths; and pair them with valid information-relaxation bounds. A small gap can justify stopping optimization work rather than adding complexity that cannot materially improve the model's objective. It does not justify stopping model validation. Return estimation error, state misspecification, transaction-cost uncertainty, discretized tail behavior, and terminal liquidation assumptions remain outside the optimization certificate and must be assessed separately before practical use.

## Checks needed to reproduce a trustworthy bound

The first reproduction check is exact agreement between the probability model used for decision-time expectations and the model used to generate test paths. Conditional centering only gives the intended zero-mean penalty when it uses the correct conditional law. Mixing a quadrature-based conditional expectation with draws from a different continuous distribution can introduce a nonzero expected penalty. A plausible-looking numerical upper value would then lose the stated certificate unless that approximation error were separately controlled.

The second check is pathwise portfolio accounting. Every heuristic must pay the full actual fee, respect the post-cost cash or leverage constraint, and use only information available at its decision date. The modified one-step fee reduction belongs only in its approximate objective. Conversely, the dual optimizer is deliberately allowed future information, but it must retain the original pathwise trading constraints and subtract the specified penalty. Accidentally relaxing both information and an undocumented portfolio constraint would produce a different, generally weaker bound.

The third check concerns optimization direction. A feasible solution of the inner maximization provides a lower value than its true maximum, so it is not by itself sufficient to certify an upper bound for the original policy problem. The deterministic inner problems need solutions with controlled optimality error; if numerical tolerances matter relative to a gap of a few basis points, that error should be added conservatively. The paper's convex construction makes this feasible, which is one reason it linearizes penalties rather than retaining a difficult nonconcave objective.

Finally, selecting the best policy and smallest bound from several tuning values on the same simulation paths introduces a selection issue for reported finite-sample uncertainty. The article's comparisons remain informative, but a fresh common-path evaluation after tuning would separate policy selection from final measurement. This is a replication improvement suggested by the experimental design, not an additional experiment reported by the authors.
