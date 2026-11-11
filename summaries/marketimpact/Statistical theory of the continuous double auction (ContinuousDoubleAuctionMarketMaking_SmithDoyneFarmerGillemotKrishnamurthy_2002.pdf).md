# Statistical theory of the continuous double auction

**Eric Smith, J. Doyne Farmer, László Gillemot, and Supriya Krishnamurthy.** [Source PDF](../../Finance/ContinuousDoubleAuctionMarketMaking_SmithDoyneFarmerGillemotKrishnamurthy_2002.pdf). The supplied manuscript is labeled arXiv:cond-mat/0210475v1, October 22, 2002, but its internal title-page date is February 1, 2008. This note describes that 36-page file, including both technical appendices; it does not assume a later publication has identical equations or figures.

## Why this matters

The paper gives a tractable benchmark for how a continuous limit-order book converts random order flow into liquidity and price fluctuations. Even when every arrival and cancellation is independent and traders have no information or strategic objective, the book can generate a spread, a nonuniform depth profile, highly concave instantaneous price impact, and different short- and long-horizon volatility. These features need not all be attributed to sophisticated trader optimization.

The central quantitative contribution is a dimensional reduction. Five observable order-flow parameters collapse to two dimensionless parameters, of which order-size granularity is often more important than tick size. This identifies the combinations of order flow that should control spread, depth, and diffusion, and supplies a baseline against which empirical deviations can be interpreted. It also reveals a particularly consequential limit: taking individual orders to be infinitesimally small can destroy the mechanism that sustains long-run price diffusion.

The analytical achievement is partial rather than exact. The authors develop mean-field and independent-interval approximations, test them against simulations, and carefully show where correlations make those approximations fail. Their treatment of average price impact is especially useful: the inverse of average cumulative depth is generally not average impact. That distinction persists far beyond this particular zero-intelligence model.

There is no completed empirical out-of-sample trading study in this manuscript, no fitted institutional execution schedule, and no transaction-cost-adjusted strategy return. The paper is a theory and simulation study. Its references to initial London Stock Exchange evidence motivate plausible parameter ranges and future testing; results from subsequent empirical papers should not be imported into this source as if already demonstrated here.

## Market mechanism and stochastic assumptions

The state is a continuous double-auction limit-order book. At any instant, the best bid is $b$, the best ask is $a$, the spread is $s=a-b$, and the midpoint is $m=(a+b)/2$. The price coordinate is logarithmic, so differences approximate proportional price changes. Prices lie on a grid with tick $dp$; using a constant log-price tick is an approximation to the fixed currency tick in many actual markets.

There are five primitive parameters:

| Parameter | Meaning | Dimensions |
|---|---|---|
| $\alpha$ | Limit-order arrival flow per side per unit price | shares / (price × time) |
| $\mu$ | Total market-order arrival flow across buy and sell sides | shares / time |
| $\delta$ | Cancellation hazard for each resting order | 1 / time |
| $\sigma$ | Size of every individual order | shares |
| $dp$ | Minimum price interval | price |

Buy and sell market orders arrive independently, each at rate $\mu/(2\sigma)$ in orders per unit time. Limit buys are placed uniformly at prices below the current ask, and limit sells uniformly above the current bid, at rate density $\alpha/\sigma$ per side. An arriving marketable component is treated as a market order and any resting remainder as a limit order; the model ignores the correlation that such splitting would create. Each existing order is independently canceled at hazard $\delta$, so its lifetime absent execution is exponential with mean $1/\delta$.

The order size is fixed, buy and sell arrivals are symmetric, and the Poisson mechanisms are independent except for their dependence on the current book boundaries. There is no fundamental value, informational signal, inventory utility, strategic cancellation, order-sign persistence, or optimization objective. Price changes arise from changes to the best quotes and from the moving support of new limit orders.

Uniform placement on infinite half-lines implies infinitely many far-away orders and an infinite total limit-arrival rate across the entire mathematical domain. The model is used locally: the book is never globally empty, far-away density balances placements and cancellations, and prices are studied in a frame moving with the quotes. A simulation necessarily uses a representation or boundary treatment that approximates that construction. The empirical validity of uniform placement far from the market is not assumed to be realistic.

The authors report qualitative robustness to some thin-tailed variation in order sizes and to replacing exponential cancellation times with fixed lifetimes. They do not provide a full numerical table establishing universality under all such alternatives, and they explicitly allow that heavy tails could matter. This is a compact null model, not a claim that the five parameters exhaust actual market behavior.

## Dimensional reduction and exact far-book balance

Using shares, price, and time as basic dimensions gives the characteristic scales

$$
N_c=\frac{\mu}{2\delta},\qquad
p_c=\frac{\mu}{2\alpha},\qquad
 t_c=\frac{1}{\delta}.
$$

The two independent dimensionless parameters are

$$
\epsilon=\frac{\sigma}{N_c}=\frac{2\delta\sigma}{\mu},
\qquad
\eta=\frac{dp}{p_c}=\frac{2\alpha dp}{\mu}.
$$

Thus $\epsilon$ is order-size granularity relative to the number of shares processed during a characteristic cancellation time; $\eta$ is the tick relative to the characteristic price scale. Dimensionless size and price are $\hat N=N/N_c$ and $\hat p=p/p_c$. Density $n(p)$ measured in shares per unit price has normalized form $\hat n=n\delta/\alpha$.

Far from the quotes, executions are negligible. Placement at rate density $\alpha$ balances cancellation at rate density $\delta n$, giving the exact asymptotic result

$$
n(\infty)=\frac{\alpha}{\delta}.
$$

The characteristic scales are not arbitrary fitted parameters. They follow from the specified arrival and cancellation rates. A scaling collapse compares simulations with the same $\epsilon$ and $\eta$ after changing their dimensional rates. Figure 2, for example, holds $\alpha=0.5$, $\sigma=1$, and zero tick while changing $(\delta,\mu)$ through $(0.001,0.2)$, $(0.002,0.4)$, and $(0.004,0.8)$. All have $\epsilon=0.01$, and their normalized depth profiles collapse.

Tables III–IV state the main dimensional predictions:

$$
s\sim\frac{\mu}{\alpha}f(\epsilon,\eta),\qquad
\frac{dn}{dp}\sim\frac{\alpha^2}{\mu\delta}g(\epsilon,\eta),
$$

$$
D\sim\frac{\mu^2\delta}{\alpha^2}
\times\text{a dimensionless function of }(\epsilon,\eta).
$$

The proportionality notation leaves dimensionless constants and functions to be determined. It does not fix a universal spread constant by dimensional analysis alone. One passage on p. 12 writes $p_c=\mu/\alpha$, inconsistent with Table II's $\mu/(2\alpha)$. This note consistently uses Table II. The factor of two must also be checked when comparing this paper's $\epsilon$ with later formulations that define granularity differently.

## What the simulations show

The normalized book shape depends strongly on $\epsilon$. At relatively large granularity, such as $\epsilon=0.2$, depth near the midpoint is substantial and impact is closer to linear. Around $\epsilon=0.02$, the near-market depth is roughly linear over part of its range, suggesting square-root-like impact when integrated and inverted. At $\epsilon=0.002$ or below, the depth profile becomes more convex near the market, and instantaneous impact can be strongly concave. These regimes are illustrated in Figs. 3–7; the numerical boundaries are descriptions of the simulated examples, not sharp phase transitions.

Instantaneous impact is measured by asking how the midpoint would change if a given number of shares swept the frozen book, holding other events fixed. The actual stochastic process uses fixed-size orders, but the simulated book can be queried with hypothetical order sizes to construct an impact curve. This is not the permanent impact of an executed parent order, nor an optimal schedule that allows the book to replenish between child orders.

If local depth were deterministically linear in distance from the quote, cumulative depth would be quadratic and its inverse would be a square root. The simulated mean curves are more general: their local power exponent changes with order size and granularity, and can fall near 0.2 in the low-granularity regime. The model therefore gives a structural reason for concavity without asserting a single exact square-root law over every scale.

Impact is very noisy. Its standard deviation can be comparable to or larger than its mean. This variability comes from the random gaps in the book and is not represented by a deterministic impact curve alone. The distinction becomes especially consequential in a granular, thin book, where a modest order can occasionally cross a large gap.

The spread distribution has a mode away from zero, but at zero tick has nonzero density near zero. Its mean depends less strongly on granularity than the local depth profile and short-time volatility do. The numerical figures, dimensional units, and source's factor-of-two inconsistency counsel against treating any visually estimated intercept as a universal calibrated constant.

For volatility, let

$$
V(\tau)=\operatorname{Var}[m(t+\tau)-m(t)].
$$

In low-granularity simulations, the initial slope of $V(\tau)$ is large, while its long-horizon slope is much smaller. The source reports approximate simulation scalings

$$
D_{\mathrm{short}}\sim\frac{\mu^2\delta}{\alpha^2}\epsilon^{-1/2},
\qquad
D_{\mathrm{long}}\sim\frac{\mu^2\delta}{\alpha^2}\epsilon^{1/2}.
$$

The exponents are empirical descriptions of the simulation behavior, not fully derived exact results with supplied universal constants. The price increments are negatively correlated: initial movements tend to be partly reversed as the book evolves. At long enough lags, typically of order tens of market-order arrival times in the illustrated cases, variance again grows approximately linearly. The anomalous short-horizon behavior is not evidence for a permanently subdiffusive asymptotic power law in the same parameter regime.

The continuum limit is subtle. At fixed macroscopic order-flow scales, the reported long-run diffusion coefficient approaches zero as $\epsilon\to0$, whereas the short-time expression increases. These statements concern different limiting time scales. Interchanging the small-order and short-time limits loses the finite-order fluctuations that the model is trying to retain. A deterministic fluid approximation can therefore give misleading volatility even if it describes average far-book density.

For a newly submitted limit order, the model also estimates the probability of execution before cancellation, $\Gamma(p)$, and the time to execution conditional on a fill. The distance $p$ is measured from the initial midpoint. At low $\epsilon$, near-market execution probabilities approach one; at $\epsilon=0.2$, even orders inside the quoted region can have a meaningful cancellation-before-fill probability. The probability curves cross at distances of order $p_c$, and far-away execution and conditional waiting time respond differently to granularity. These are conditional queue-dynamics statistics under exogenous cancellation, not optimal placement policies. The conditional time omits orders that never fill.

Increasing the normalized tick from zero toward one raises the mean spread by approximately half a tick in the examples, reduces measured instantaneous impact, and suppresses some small-granularity short-time fluctuations. Granularity generally matters more than tick over the tested ranges. None of these simulations establishes the welfare-optimal tick in a real market with strategic queueing and heterogeneous traders.

## Coordinates, conservation, and why the reference frame matters

Two descriptions of the book are used. In price coordinates, $n(p)$ describes the density at a specified distance from a reference quote or midpoint. In order coordinates, the cumulative order count is inverted to obtain the price of successive orders. With unit-size orders, let $x_k$ be the price gap between adjacent orders in that ranking; $x_0$ is the spread. The same symbol $N$ is used in the source for cumulative size and for order indexing in different sections, so unit conversions are essential when comparing formulas.

A frame centered on the bid differs from a frame centered on the midpoint. When a quote changes, all coordinate labels shift even though most resting orders have not moved in absolute price. Those coordinate shifts correlate with the book configuration: a large empty gap makes a large shift more likely when the best order is removed. Ignoring that dependence is the main obstacle to an exact simple mean-field equation.

Conservation supplies a useful constraint. In a bid-centered stationary description of one side, the total placement excess over cancellation balances market-order removals:

$$
\frac{\mu}{2}=\int_0^\infty[\alpha-\delta n_b(p)]\,dp.
$$

Both sides have units of shares per unit time. Defining a normalized density $\psi$ so that $\epsilon\psi=\hat n$ converts this to

$$
\int_0^\infty[1-\epsilon\psi(\hat p)]\,d\hat p=1.
$$

A midpoint-centered version includes the supply allowed inside the spread and gives a right side $1-E[\hat s]/2$. The source moves between densities and finite-bin occupancies, so its summation notation must be interpreted with the appropriate tick/bin width. The physical conservation equation is an indispensable check on those conversions.

The authors explicitly test the mean-field factorization

$$
P(\{n(p)\})\approx\prod_p P(n(p)).
$$

It works well for the illustrated midpoint-centered book at $\epsilon=0.2$, marginally at 0.02, and poorly at 0.002. In a bid-centered frame, independence performs poorly even in regimes where the midpoint approximation looks reasonable. This is direct evidence that a closure's usefulness depends on both the regime and the coordinate system, not just the apparent simplicity of independent primitive arrivals.

## Master equation and the diffusion approximation

For a bin of width $dp$, let $\pi(n,p)$ be the probability it contains $n$ shares, where $n$ is a multiple of $\sigma$. The master equation accounts for four types of transitions: limit arrivals add $\sigma$ at rate $\alpha(p)dp/\sigma$; cancellations remove $\sigma$ at rate proportional to the existing number of orders; market orders remove the first reachable order, with effective rate $\mu(p)/(2\sigma)$; and changes in the reference quote shift the bin coordinates.

Away from the zero-occupancy boundary, the local components have the form

$$
\partial_t\pi(n,p)=\frac{\alpha(p)dp}{\sigma}[\pi(n-\sigma,p)-\pi(n,p)]
$$

$$
\quad+\frac{\delta}{\sigma}[(n+\sigma)\pi(n+\sigma,p)-n\pi(n,p)]
+\frac{\mu(p)}{2\sigma}[\pi(n+\sigma,p)-\pi(n,p)]
+\mathcal S[\pi].
$$

The market-removal term needs its zero-occupancy boundary correction; it cannot remove an order from an empty bin. The operator $\mathcal S$ shifts the coordinate using distributions $P_+(\Delta p)$ and $P_-(\Delta p)$. Treating those shifts as independent of the occupancy being shifted is the approximation, not an exact property of the process.

Introduce the generating function

$$
G(z,p)=\sum_{n\ge0}z^{n/\sigma}\pi(n,p),
\qquad G(1,p)=1,\quad G(0,p)=\pi(0,p),
$$

$$
\partial_zG(1,p)=\frac{E[n(p)]}{\sigma}.
$$

With symmetric shifts and a second-order expansion in their size, define the Fokker–Planck coefficient $D=\sum_{\Delta p}P(\Delta p)(\Delta p)^2$ in the source's convention. This is a coefficient in a diffusion operator; factors of two must be checked before identifying it with a measured variance-growth slope. In the small-bin limit, a bin is either empty or holds one order, so $E[n]=\sigma[1-\pi(0,p)]$. Equation (27) becomes

$$
\frac{\alpha(p)dp}{\delta}
=\left[\frac{\mu(p)}{2\delta\sigma}+1-
\frac{D}{\delta}\frac{d^2}{dp^2}\right]E[n(p)].
$$

Market orders are screened by nearer resting orders. Under factorization, the probability that no nearer order prevents reaching normalized distance $\hat p$ is

$$
\phi(\hat p)=\exp\left[-\int_0^{\hat p}\psi(u)\,du\right],
\qquad \phi'=-\psi\phi.
$$

In the midpoint frame this is also used as the probability that the half-spread reaches at least that distance. Setting $\beta=D/(\delta p_c^2)$ gives the normalized mean equation

$$
\frac{\alpha(p)}{\alpha(\infty)}
=\left[\phi+\epsilon\left(1-\beta\frac{d^2}{d\hat p^2}\right)\right]\psi.
$$

The midpoint geometry makes the effective placement term $1+\phi$, leading to Eq. (37):

$$
1+\phi=-\left[\phi'
+\epsilon\left(1-\beta\frac{d^2}{d\hat p^2}\right)(\log\phi)'\right].
$$

Boundary conditions are $\phi(0)=1$, $\phi(\infty)=0$, and $\epsilon\psi(\infty)=1$. The approximate local boundary condition uses the average shift size, $\langle\Delta\hat p\rangle\psi'(0)-\psi(0)\approx0$. The shift distributions are determined self-consistently from the spread-tail approximation:

$$
\beta=\frac{4}{\epsilon}\int_0^\infty x^2\phi(x)\,dx,
\qquad
\langle\Delta\hat p\rangle=
\frac{\int_0^\infty x\phi(x)\,dx}{\int_0^\infty\phi(x)\,dx}.
$$

Numerically solving these coupled equations gives a useful depth approximation in intermediate regimes. It is not an exact solution. In particular, the diffusion term can transport apparent resting-order density through the midpoint, even though the true midpoint lies in an empty spread at every instant. The resulting solution violates the global conservation condition. The authors attribute some apparent agreement to compensating approximation errors.

Appendix B extends the finite-bin generating-function solution perturbatively in the shift term, with normalization imposed order by order. The expansion assumes its formal series is meaningful; it is not a general proof of convergence. Taking the small-bin limit recovers the operator form above. The appendix therefore supports the derivation and exposes the approximation rather than establishing an exact invariant distribution.

## Correlated-shift correction and its unresolved global error

To improve the midpoint neighborhood, the authors condition addition and removal events on the current ask and enumerate their contributions to positive and negative shifts. Appendix B's Tables VII–X distinguish whether a changed order lies before or beyond a given reference point. This produces a nonlocal source correction $S$ in

$$
\frac{\alpha(p)}{\alpha(\infty)}=(\phi+\epsilon)\psi-S.
$$

A second-order expansion gives

$$
S(\hat p)=\mathcal R(\hat p)\psi(\hat p)
+\mathcal P(\hat p)\psi'(\hat p)
+\epsilon\beta(\hat p)\psi''(\hat p),
$$

with coefficients defined by integrals of the spread-tail function and its shifts in Eqs. (B30)–(B37). They are not additional parameters fitted independently to a simulated depth curve. Their role is to approximate the correlation between a book configuration and the coordinate shift it causes.

This correction enforces $S(0)=0$ and therefore gives the midpoint intercept

$$
\psi(0)=\frac{2}{1+\epsilon}.
$$

The corresponding finite-density interpretation agrees with simulations. Attempting the analogous bid-frame argument would give $1/(1+\epsilon)$, which the simulations do not support. The contrast again shows that frame choice and factorization are substantive assumptions.

The correction still does not satisfy $\int S\,d\hat p=0$, the global conservation requirement. At low granularity, one can obtain a reasonable local mean depth while the implied spread cumulative distribution remains inaccurate because correlated occupancy fluctuations are not captured. The paper explicitly acknowledges sacrificing global conservation to improve the local boundary behavior. A practitioner should not use this approximation as a fully calibrated joint distribution of spreads, gaps, depth, and fills.

## Independent interval approximation

The alternative analytic method works with gaps $x_k$ between consecutive orders. Set order size to one, and at finite tick prohibit depositing on an already occupied price site. This simplification allows a closed description of changes in a gap when an adjacent order is removed or a new order is inserted inside it.

For the spread, a best-order cancellation or market order expands the spread by a neighboring gap. A new limit order inside the spread contracts it. The corresponding expected change, prior to moment closure, is represented by

$$
\frac{dx_0}{dt}=(x_1+x_{-1})\left(\delta+\frac{\mu}{2}\right)
-\alpha dp\,x_0(x_0-1),
$$

where the $x$ variables in this discrete representation count ticks. To close the equations, the authors approximate second moments by a common ratio $a$, so that $E[x_k^2]\approx aE[x_k]^2$, and factor the required mixed moments. The $a$ in this section is a moment-ratio parameter, not the best ask.

Let $\hat x_k=dp\,E[x_k]/p_c$. The stationary recursion begins with

$$
(1+\epsilon)\hat x_1
=\frac a2\hat x_0(\hat x_0-\eta),
$$

and for subsequent gaps takes the form

$$
(1+k\epsilon)\hat x_k=
\frac a2\hat x_{k-1}(\hat x_{k-1}-\eta)
+\hat x_{k-1}\sum_{i=0}^{k-2}(\hat x_i-\eta).
$$

At large order index, $\hat x_\infty=\epsilon+\eta$. Defining the total excess gap as

$$
S_\infty=\sum_{i\ge0}(\hat x_i-\hat x_\infty),
$$

the recursion implies $S_\infty=1+(1-a/2)\epsilon$. Exact conservation requires $S_\infty=1$, fixing $a=2$. Thus the closure constant is constrained by conservation, not selected by fitting a spread. Table VI's simulation values are approximately 1, 1, 0.998, and 1 for the illustrated granularity values 0.66, 0.2, 0.04, and 0.02.

A computational solution guesses $\hat x_0$, iterates the recursion, and adjusts the guess until the gaps converge to $\epsilon+\eta$. This is a shooting method for the stationary mean gaps. Setting $a=2$ resembles an exponential-gap second-moment relation, which is plausible far from the market but not uniformly accurate near the spread: the first gap distributions can look more Gaussian. Figure 23 makes that mismatch visible.

The approximation predicts mean spread slightly below the simulated value and captures its parameter dependence. Mean gaps, depth, and impact agree quantitatively better at large granularity than at small granularity. If $k$ unit orders are consumed, the estimated midpoint impact is

$$
\frac{E[\Delta m]}{p_c}\approx\frac12\sum_{j=1}^k\hat x_j.
$$

The factor one-half is because the ask moves while the bid initially stays fixed. Reconstructing depth as inverse mean gap at a cumulative mean-gap location is another approximation; it does not exactly reproduce the midpoint profile or its conservation relation. Figures 25–29 compare these quantities directly with simulation and show the deterioration in the low-granularity regime.

The authors also consider nonuniform placement with a power-law shape proportional to $\Delta_0^\beta/(\Delta+\Delta_0)^\beta$, where $\Delta$ is distance from the quote and $\Delta_0$ controls the near-quote shoulder. The rate amplitude still needs dimensional specification. For $\beta>1$, the finite integrated supply may be insufficient for some parameter choices and the interval equations can lack a stationary solution. This is suggestive of book depletion under such a modified model, not a validated theory of real-market crashes.

## Why average depth cannot simply be inverted

Appendix A derives the effect of book fluctuations on mean impact. For one book realization, cumulative volume $\omega$ is monotone in price, and its inverse determines the distance required to execute a specified quantity. But averaging and inversion do not commute:

$$
E[N^{-1}(\omega)]\ne(E[N])^{-1}(\omega).
$$

The price reference matters. A sweep changes the ask by the full distance between consumed orders, while the midpoint changes by half that amount if the bid stays fixed. Including the initial half-spread in the price coordinate changes the intercept of the inverse function. Appendix A therefore works with a consistently defined cumulative volume and reference quote before comparing averages.

Locally approximate cumulative volume as

$$
\omega(p,t)=a(t)+b(t)p+\frac{c(t)}{2}p^2.
$$

Its inverse on the appropriate branch is

$$
p(\omega,t)=\frac{-b(t)+\sqrt{b(t)^2+2c(t)[\omega-a(t)]}}{c(t)}.
$$

Write the random coefficients as their means plus zero-mean fluctuations. A second-order expansion gives

$$
E[p(\omega)]\approx p(\omega;\bar\theta)
+\frac12\sum_{r,s}
\frac{\partial^2p}{\partial\theta_r\partial\theta_s}
\operatorname{Cov}(\theta_r,\theta_s),
\qquad \theta=(a,b,c).
$$

The required coefficient combinations are obtained from derivatives of $E[\omega]$ and $E[\omega^2]$. Although $\operatorname{Var}(b)$ and $\operatorname{Cov}(a,c)$ cannot be identified separately from those moments, their coefficients in the inverse expansion coincide, so their sum suffices. Equations (A15)–(A20) supply the derivatives explicitly. Figure 31 shows that inverting mean cumulative depth understates mean impact, while adding the second-order fluctuation correction brings the prediction much closer for $\epsilon=0.2$, 0.02, and 0.002.

There is also a useful distributional result. For monotone cumulative depth and a consistent coordinate convention, impact quantiles can be related to inverse depth quantiles with the complementary probability. The median is particularly simple: the inverse of the median cumulative-depth curve gives median impact under the stated monotonicity relation. With discrete ticks and jumps, quantile and generalized-inverse conventions must be fixed. This is a statement about distributions of monotone random functions, not a license to invert their means.

## Reproducibility, interpretation, and limits

The paper gives the stochastic events, parameter dimensions, scaled regimes, approximate equations, and many simulation comparisons, enough to reconstruct the conceptual experiment. It does not provide a complete modern replication package specifying every random seed, burn-in, simulation length, numerical boundary, integration tolerance, or Monte Carlo standard error. Most plots establish qualitative or approximate quantitative agreement without formal confidence bands. Reproducing exact curves therefore requires numerical choices that should be disclosed as new implementation choices.

No stock universe, sample dates, fee schedule, transaction-cost model, train/test split, or forecast re-estimation window belongs to the paper's main numerical experiment. Those are absent because the experiment is a synthetic auction process. Mentioned empirical order-size ranges and preliminary LSE comparisons should not be treated as a hidden backtest. The claim of no free parameters means that the five inputs are observable in principle; it does not mean every approximation or parameter-estimation procedure is uniquely fixed in actual market data.

The baseline has economically significant omissions. Real order placement clusters near quotes and round numbers; cancellation depends on age, distance, inventory, and information; sizes are dispersed; signs are persistent; and participants respond strategically to queue position and expected fills. The model's negative return autocorrelation is partly a consequence of independent order flow. Introducing persistent order signs could offset that mean reversion, but doing so adds structure outside the solved benchmark. Volatility clustering and endogenous changes in participation are also not generated by merely holding the five Poisson parameters constant.

The most reusable results are the dimensional scale separation, the sensitivity to finite order size, the explicit conservation checks, the frame-dependent failure of factorization, and the distinction between mean impact and inverse mean depth. The paper does not demonstrate that zero-intelligence assumptions are literally true. It demonstrates which nontrivial market properties can emerge from the matching institution and finite-order mechanics alone, and identifies the correlations that a richer theory must explain.

## Source map

Model and prior literature: pp. 2–5. Dimensions and parameter reduction: pp. 5–8, Tables I–IV. Simulation phenomenology: pp. 8–14, Figs. 2–14. Coordinates, conservation, and independence tests: pp. 15–18. Master equation and mean-field theory: pp. 19–23, Eqs. (14)–(44). Independent-interval recursion and comparisons: pp. 24–28, Eqs. (45) onward and Figs. 23–30. Conclusions: p. 29. Impact inversion and quantiles: Appendix A, pp. 29–32. Generating-function expansion and correlated-shift corrections: Appendix B, pp. 32–35, including Eqs. (B21)–(B37). References extend through p. 36.
