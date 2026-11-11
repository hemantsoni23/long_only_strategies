# On the Behaviour of Commodity Prices

Angus Deaton and Guy Laroque, *The Review of Economic Studies* 59(1), January 1992, pp. 1–23. [Source PDF](../../Finance/CommodityPrices_Deaton_1992.pdf). The supplied twenty-four-page scan includes a JSTOR cover; journal p. 1 is PDF page 2. The complete article, including the proofs on pp. 19–23, is covered here. This is the published 1992 version, which the acknowledgements describe as substantially rewritten from the 1989 working papers.

## Why this matters

A commodity can be stored for future consumption, but future harvests cannot be borrowed backward in time. That asymmetry creates a nonlinear equilibrium even with risk-neutral competitive inventory holders, independent harvests, and a simple demand curve. Storage supports prices when supply is plentiful and transfers supply into later shortages. Once inventory is exhausted, a bad harvest passes directly into price. The result can be quiet periods interrupted by large positive price spikes, price-dependent volatility, and positive serial dependence without serially correlated production shocks.

Deaton and Laroque turn this mechanism into an explicit stationary rational-expectations price function, prove existence and comparative statics under assumptions broad enough to include linear demand, and compare its implications with thirteen annual commodity-price series. Their evidence is deliberately incomplete. The model generates skewness, fat tails, and the direction of conditional heteroskedasticity, but their numerical specifications do not reproduce the high autocorrelations found in the data. A successful fit to a conditional mean equation does not establish that the full structural storage model generated the observations.

For a quantitative researcher, the paper supplies a useful nonlinear state model and a warning about identification. Prices alone reveal less about inventories, harvest distributions, demand curvature, and storage costs than a two-parameter reduced-form fit might suggest. There is no futures trading strategy, return forecast competition, or investment-performance result in this article.

## State, market clearing, and the storage constraint

Time is discrete, with one market after each harvest. Let $z_t$ be newly available supply, $I_{t-1}$ the inventory carried from the previous period, and $\delta$ the fraction lost in storage. Availability before current consumption and storage is

$$
x_t=z_t+(1-\delta)I_{t-1}.
$$

The producer-consumer sector has continuous, strictly decreasing excess demand $D(p)$, with inverse $P(x)=D^{-1}(x)$. This can incorporate an instantaneous supply response, but the central experiments use an exogenous harvest. Demand randomness can also be absorbed into the net supply shock in the simple additive interpretation. Inventory holders are risk neutral and borrow or lend at a constant numeraire rate $r$. Set $\beta=(1+r)^{-1}$ and $a=\beta(1-\delta)$.

The assumptions underlying the main equilibrium theorem are iid harvests on compact support $[\underline z,\overline z]$; continuous, strictly decreasing demand on its price domain; demand tending to infinity at the lower endpoint of that domain; and a finite positive market-clearing price $P(\underline z)$ at the smallest possible harvest. The lower price-domain endpoint may be negative infinity, allowing linear inverse demand. Carrying inventory is costly in the discounted physical sense, $0<a<1$. The renewal theorem additionally uses $0<\delta<1$ and a condition ensuring storage sometimes occurs. These are not assumptions of Gaussian, unbounded harvests.

Market clearing and competitive storage imply

$$
D(p_t)+I_t=z_t+(1-\delta)I_{t-1}=x_t,
$$

$$
I_t\geq0,\qquad p_t-aE_t[p_{t+1}]\geq0,\qquad I_t\{p_t-aE_t[p_{t+1}]\}=0.
$$

Positive inventory requires equality of current price and the discounted expected sale value of a surviving unit. When expected carry profits are negative, inventory is zero. The aggregate nonnegativity constraint is essential: allowing negative inventories would permit consumption of commodities that have not yet been produced and remove the economically important stockout regime. The model omits a separate nonlinear convenience benefit from holding physical stocks.

A stationary rational-expectations equilibrium is a function $f$ mapping current availability into price, $p_t=f(x_t)$. Inventory is $I(x)=x-D(f(x))$, and the fixed-point equation is

$$
f(x)=\max\left\{aE\left[f\left(z+(1-\delta)\{x-D(f(x))\}\right)\right],P(x)\right\}.
$$

The expectation integrates over next period's independent harvest. The current unknown $f(x)$ appears inside current consumption as well as outside the expectation; this is an implicit equation, not an ordinary explicit Bellman update. In the paragraph before equation (7), the source calls the $x_t$ iid. The model and the equation require iid $z_t$; availability $x_t$ contains endogenous inherited inventory and is generally serially dependent.

## Equilibrium theorem and economic implications

Theorem 1, pp. 6–7, establishes a unique equilibrium in the class of nonnegative, continuous, nonincreasing price functions. Define

$$
p^*=aE[f(z)].
$$

Then $f(x)=P(x)$ whenever $P(x)\geq p^*$, and $f(x)>P(x)$ whenever $P(x)<p^*$. The price function is strictly decreasing wherever positive. Inventory is strictly increasing in availability in the storage region. The maximum equilibrium price equals $P(\underline z)$, the maximum no-storage price; storage changes the frequency and shape of high-price outcomes rather than increasing the attainable maximum.

The appendix proves this by constructing an operator $T$. Given a prospective next-period function $g$, solve for current $q$ from

$$
q=\max\{aE[g(z+(1-\delta)(x-D(q)))],P(x)\}.
$$

The expected continuation value is nonincreasing in $q$: a larger current price lowers current consumption, increases carryover, and lowers the next price under a decreasing $g$. Subtracting $q$ therefore gives a strictly decreasing root problem. This yields a unique current price, continuity, monotonicity, and an order-preserving operator. On the bounded function class anchored at $f(\underline z)=P(\underline z)$, the appendix obtains

$$
\|Tg_1-Tg_2\|_\infty\leq a\|g_1-g_2\|_\infty.
$$

Since $a<1$, successive implicit updates converge uniformly to the unique fixed point. This contraction concerns the properly defined implicit operator, not automatically every numerical shortcut used later.

The price dynamics have two regimes. When $p_t\geq p^*$, inventory is zero and $p_{t+1}=f(z_{t+1})$: next period's distribution no longer depends on the current price. When $p_t<p^*$, carry arbitrage implies

$$
p_{t+1}=a^{-1}p_t+\eta_{t+1},\qquad E_t[\eta_{t+1}]=0.
$$

Together,

$$
E[p_{t+1}\mid p_t]=a^{-1}\min(p_t,p^*).
$$

The slope below the threshold exceeds one, because expected appreciation must compensate inventory holders for interest and physical loss. This locally explosive slope is compatible with a stationary overall process: the upper branch is flat and recurrent stockouts reset the dynamics. Replacing the model with a globally linear AR(1) loses precisely that mechanism.

If inverse demand is convex, the equilibrium price function is convex, and conditional price variance is nondecreasing in the current price. More inventory buffers next period's harvest shock; at a stockout, the conditional variance reaches a plateau because the next state is simply the new harvest. Appendix Lemma 4 makes the argument explicit. For fixed carryover $I$, differentiation of $\operatorname{Var}[f(z+(1-\delta)I)]$ is proportional to $\operatorname{Cov}(f,f')$. A decreasing convex $f$ has increasing derivative, making this covariance nonpositive. Inventory falls as current price rises, producing the stated positive price/variance relation. At nondifferentiable points the appropriate implication is monotonicity rather than a everywhere-defined classical derivative.

Theorem 3 supplies comparative statics. Increasing the discount factor raises the equilibrium price, cutoff, and inventory demand. A first-order stochastic increase in harvest supply lowers them. With convex inverse demand, a mean-preserving spread in harvests raises price and inventory demand. The proof uses preservation of convexity and order under the implicit operator, then takes its fixed-point limit. These statements compare policies at the same availability; they do not alone establish a monotone change in every unconditional statistic, such as the stockout frequency or unconditional price variance.

## Renewal and a repair to the appendix's auxiliary-process argument

Theorem 2 adds positive depreciation and $P(\overline z)<aE[P(z)]$, ruling out permanent absence of storage. Inventories then have bounded limiting support and stockouts recur, so prices have a regenerative or renewal structure. The inventory recursion and the upper bound on price imply

$$
I_t\leq(1-\delta)I_{t-1}+\overline z-\underline z.
$$

Thus the limiting inventory bound is $(\overline z-\underline z)/\delta$. A stockout eliminates the inherited state, and the iid next harvest starts a new cycle. This regeneration explains why positive conditional autoregression within the storage region need not imply a random walk.

One step in the printed proof on p. 22 requires correction. It defines an auxiliary recursion $J_t=(1-\delta)J_{t-1}-D(p^*)+z_t$ and states that its limiting distribution is that of $[z-D(p^*)]/\delta$. With independent, nondegenerate harvests, the stationary law instead involves the discounted sum

$$
J_\infty\overset{d}{=}\sum_{k=0}^{\infty}(1-\delta)^k\{z_{-k}-D(p^*)\}.
$$

The printed expression has the same mean when that mean exists, but generally a different variance and distribution. This is an algebraic correction derived here, not an erratum cited by the authors. The renewal conclusion can be supported without that identity. Since $p^*<P(\underline z)$, decreasing demand implies $D(p^*)>\underline z$. There is positive probability of harvests below $D(p^*)$ by a fixed positive amount. A sufficiently long run of such harvests drives the auxiliary recursion below zero from the bounded inventory region. Independent repeated blocks make eventual occurrence almost sure. Actual nonnegative inventory must therefore hit zero first. This repairs the relevant stockout argument while preserving the theorem's bounded-support and iid qualifications.

## Numerical solution and stationary-distribution calculation

The authors calculate the price function on a grid of 100 availability points. They initialize from no-storage inverse demand, integrate expectations numerically, and linearly interpolate between grid points. The exact implicit iteration is equation (12). For speed, their implemented update replaces the current iterate inside the demand term on the right-hand side by the previous iterate, eliminating a subsidiary root-finding loop. They report convergence in practice, usually in 5–200 iterations, but do not provide a theorem that this modified explicit iteration retains the contraction bound. Each historical iteration took about one minute on a 386-based machine running GAUSS.

The availability range sometimes required trial simulations. For a modern reconstruction, one should specify the integration rule, grid endpoints, boundary behavior, convergence tolerance, and the discrepancy from a finer grid; these numerical details are not fully supplied. Solving the implicit scalar equation by a bracketed root method is a transparent alternative, but would be an implementation choice rather than the exact reported shortcut.

Given a price policy, simulation is straightforward:

$$
p_t=f(x_t),\qquad x_{t+1}=(1-\delta)\{x_t-D(f(x_t))\}+z_{t+1}.
$$

The source initializes inventory at zero and describes the resulting initial state as coming from the invariant distribution. More precisely, this starts a regeneration cycle; it does not generally draw a random-time state from the unconditional invariant law. A burn-in or a direct invariant draw is still needed when stationary sampling rather than cycle sampling is intended.

To avoid relying entirely on long simulations, the paper also discretizes the state transition. If equally spaced grid points are $x_i$ with spacing $h$, define a column-stochastic matrix by

$$
T_{ij}=\Pr\left(x_i-h/2\leq z+(1-\delta)\{x_j-D(f(x_j))\}\leq x_i+h/2\right).
$$

These probabilities are differences of the harvest distribution function. The normalized eigenvector satisfying $T\pi=\pi$ supplies approximate invariant masses. The same masses mapped through $f$ give the price distribution; combining them with transition probabilities yields autocorrelations and moments. Endpoint-bin treatment must preserve total probability. A reproducible implementation should disclose how this is done, since the article's interior-bin formula alone does not specify it.

## Calibration experiments and what they fail to match

Table 2, p. 11, studies five parameterizations. Linear inverse demand is $P(x)=A+Bx$, with harvests normal with mean 100 and standard deviation 10. The low-dispersion case has $A=200$, $B=-1$, $r=0.056$, and $\delta=0.05$; the high-dispersion case has $A=600$, $B=-5$, $r=0.05$, and $\delta=0$. Their no-storage price coefficients of variation are 0.10 and 0.50. The second case matches a Williams–Wright specification and serves as a numerical cross-check. It also lies outside the positive-depreciation statement of Theorem 2; the article discusses extensions to zero depreciation under additional lower-price restrictions.

The other three cases use $P(x)=x^{-\rho}$ and $\log z\sim N(0,\sigma^2)$, with $r=0.056$ and $\delta=0.05$. The pairs $(\rho,\sigma)$ are $(1,0.10)$, $(1,0.50)$, and $(5,0.10)$. Normal or lognormal distributions are truncated at five standard deviations in the numerical implementation to fit the compact-support theory. Before truncation, the exact no-storage lognormal coefficient of variation is $\sqrt{\exp(\rho^2\sigma^2)-1}$, while the paper's $\rho\sigma$ is a small-dispersion approximation. For $\rho\sigma=0.5$, the exact value is about 0.533, explaining the table's 0.53 entries.

| Statistic | Linear low | Linear high | Isoelastic (1,.10) | Isoelastic (1,.50) | Isoelastic (5,.10) |
|---|---:|---:|---:|---:|---:|
| Stockout probability | .82 | .16 | .82 | .24 | .24 |
| First autocorrelation | .08 | .48 | .08 | .33 | .29 |
| Second autocorrelation | .01 | .31 | .01 | .16 | .14 |
| Third autocorrelation | .00 | .22 | .00 | .09 | .08 |
| Skewness | .43 | 1.99 | .61 | 3.41 | 3.15 |
| Excess kurtosis | −.29 | 5.50 | .17 | 24.22 | 16.43 |

Greater dispersion of no-storage prices creates more opportunities for profitable inventory smoothing. Storage occurs only about 18 percent of the time in the low-dispersion cases but 84 percent in the high-dispersion linear case. Convex demand produces particularly large skewness and excess kurtosis. Figures 3–4 illustrate how inventory purchases remove much of the low-price tail while occasional stockout/poor-harvest combinations retain a sparse high-price tail. Figure 5 uses $\rho=8$, $\sigma=0.1$, positive depreciation, and a 200-period simulation to show the alternation between quiet prices and sharp spikes.

The empirical benchmark is annual average-price indices for 1900–1987, supplied by the World Bank Commodities Division and deflated by the U.S. consumer price index. The thirteen series are bananas, cocoa, coffee, copper, cotton, jute, maize, palm oil, rice, sugar, tea, tin, and wheat. There are 88 annual price observations before lag losses. Table 1 reports first autocorrelations ranging from .62 for sugar to .91 for bananas; second autocorrelations range from .39 to .82. All first autocorrelations exceed .60. The largest simulated first autocorrelation in Table 2 is only .48.

Other empirical moments vary considerably. Sugar's coefficient of variation is .60, skewness 1.49, and excess kurtosis 3.08. Palm oil has skewness 3.24 and excess kurtosis 16.52. Bananas have coefficient of variation .17 and excess kurtosis −.98. The “persistence” column uses a normalized zero-frequency spectral-density measure with a 40-year Bartlett window, not simply the first autocorrelation. It is .52 for bananas and below .30 for all other series. The coexistence of high short-lag correlation with low estimated long-run persistence motivates a nonlinear mean-reverting account but does not itself prove stationarity.

The simulation diagnostics compare samples of 2,000 periods with Wilcoxon two-sample statistics. Some high-dispersion cases reject pooling even across such long realizations; the authors attribute this to rare large spikes and slow empirical stabilization. Their narrative also mentions splitting a simulated series into halves, whereas Table 2's note describes two independent 2,000-period simulations for each reported number. Exact replication must distinguish those designs. In addition, a conventional iid Wilcoxon reference distribution is not automatically valid for serially dependent prices. The reported rejections are informative about the difficulty of naive simulation diagnostics, not a proof that the invariant law differs between runs.

## Reduced-form estimation and its identification limits

The empirical estimator avoids repeated structural solution inside a full likelihood. Define $\gamma=a^{-1}$ and $\theta=(\gamma,p^*)$. Residuals and instruments are

$$
u_t(\theta)=p_t-\gamma\min(p_{t-1},p^*),\qquad w_t=(1,p_{t-1},p_{t-2},p_{t-3})'.
$$

Under the model, the residual is a conditionally mean-zero innovation, though heteroskedastic. The source minimizes

$$
Q(\theta)=u(\theta)'W(W'W)^{-1}W'u(\theta),
$$

using a Newton-type method with almost-everywhere derivatives around the kink. If $p^*$ exceeds every lagged observed price, the criterion is locally flat in $p^*$ and the threshold is not identified. Starting values and treatment of this flat region are consequential but are not exhaustively specified.

With $J=\partial u/\partial\theta'$ and $A=W(W'W)^{-1}W'$, its heteroskedastic sandwich covariance can be written

$$
\widehat{\operatorname{Var}}(\hat\theta)=(J'AJ)^{-1}J'A\widehat D A J(J'AJ)^{-1},
$$

where $\widehat D=\operatorname{diag}(\hat u_t^2)$. The source's overidentification statistic is

$$
OID=\hat u'W(W'\widehat D W)^{-1}W'\hat u,
$$

which it compares with chi-square on two degrees of freedom. A methodological qualification is needed: its estimator uses the initial $(W'W)^{-1}$ weighting, while the statistic uses the heteroskedastic efficient weighting. For a generally inefficient GMM estimate, this raw residual-moment quadratic does not automatically have the standard chi-square law with moments minus parameters degrees of freedom. Efficient reestimation or a correctly projected moment-covariance test is needed for that general claim. The reported finite-sample rejection rates should therefore be retained as results of the stated procedure, rather than promoted to a universally valid test calibration.

Table 3 draws 500 independent samples of 100 observations from the high-variance linear model. True $\gamma=1.050$ is estimated on average as 1.055, with empirical dispersion .022 and average estimated standard error .023. True cutoff 114.2 is estimated on average as 112.6, with dispersion 8.79 and average estimated standard error 13.00. The OID statistic averages 2.64 with dispersion 2.25, versus the nominal chi-square-two mean and standard deviation of 2. Its rejection rate is 9.8 percent at a nominal 5 percent and 1 percent at nominal 1 percent. The mean Durbin–Watson statistic is 1.99 with dispersion .14. These experiments expose imperfect test calibration despite favorable parameter recovery under the maintained model.

In the actual data, Table 4 estimates $\gamma$ from .995 for palm oil to 1.090 for sugar; the other eleven estimates are just above one. None is significantly different from one. Selected estimates are bananas 1.004 (.02), coffee 1.040 (.07), jute 1.046 (.04), and sugar 1.090 (.14). The effective annual carry wedge is $\gamma-1=(r+\delta)/(1-\delta)$, not exactly $r+\delta$ except as a small-rate approximation. Demand and harvest parameters are not separately estimated.

The fraction of prices above the estimated cutoff ranges from .01 for palm oil to .23 for sugar. Copper, maize, tin, and palm oil have at most seven percent, leaving roughly six or fewer observations to identify the upper branch. Palm oil's cutoff estimate 1.426 has standard error 2.81 in the arbitrary underlying index units. The authors regard its single influential spike as particularly problematic. Reported OID values exceed the conventional approximately 5.99 five-percent chi-square-two threshold for cotton (10.9), jute (8.17), and rice (6.37); the paper prints 5.89 for that threshold. Cotton and rice also have low Durbin–Watson values, 1.21 and 1.43. These diagnostics do not uniformly agree, and the earlier size distortion limits their literal significance interpretation.

Finally, squared-residual regressions strongly reject homoskedasticity for all thirteen commodities, and log absolute residuals rise with log lagged price. The article does not tabulate the individual variance-test statistics or slope estimates, so their magnitudes cannot be reconstructed. It finds no clear variance plateau above the cutoff, where observations are scarce. Matching the conditional mean plus the direction of heteroskedasticity remains weaker than matching the structural transition density: a threshold autoregression with arbitrary innovations can satisfy the same conditional mean while having very different spikes, skewness, and autocorrelations.

## What a faithful extension must preserve

The paper's core model has exogenous iid harvests, no advance harvest information, no separate convenience service, constant financing/storage parameters, and one post-harvest market each period. It does not use observed inventory quantities in estimation. Relaxing those features may improve persistence, but changes the state space and often removes the price-only Markov representation. A replication should first recover the fixed-point policy, transition matrix, five numerical parameterizations, and exact reduced-form estimator before adding persistent supply, demand trends, or risk aversion.

The source supplies no code, random seeds, numerical tolerances, detailed commodity-index construction, or observation-level data. It also does not report forecast windows, validation samples, portfolio rules, turnover, or costs. Its contribution is a structurally motivated explanation of nonlinear commodity-price behavior, accompanied by unusually clear evidence that the simplest version has not solved the persistence problem. The equilibrium proofs are on pp. 19–23; numerical construction and distributions on pp. 9–14; GMM design and estimates on pp. 14–18; and the final limitations on p. 19.
