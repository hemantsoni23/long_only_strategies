# Competitive Storage and Commodity Price Dynamics

Angus Deaton and Guy Laroque, *Journal of Political Economy* 104(5), October 1996, pp. 896–923. [Source PDF](../../Finance/CommodityPrices_Deaton_1996.pdf). All twenty-nine PDF pages were read visually, including the identification proof and references; the first page is a JSTOR cover. Journal p. 896 corresponds to PDF page 2. This paper incorporates empirical material from the authors' 1991 manuscript and refers to their distinct 1995 econometric paper for fuller computational documentation. It is also distinct from their 1992 study, *On the Behaviour of Commodity Prices*.

## Why this matters

Storage converts a sequence of supply and demand shocks into a nonlinear price process. A low price induces inventories, which support current demand and transmit today's abundance into future supply. A stockout removes that connection. This mechanism can create serial correlation even if the primitive shocks are independent. The important empirical question is whether it creates enough persistence at economically plausible carrying costs.

Deaton and Laroque estimate the equilibrium price function rather than testing only a few conditional-moment restrictions. Their fitted IID-shock models produce first-order price correlations of 0.192–0.416, while the actual annual correlations are 0.621–0.895. Allowing the underlying shocks themselves to be persistent improves fit, but the estimated persistence must already be high. Storage then contributes mainly conditional heteroskedasticity, with a relatively small contribution to persistence except at economically implausible carrying-cost boundaries.

This matters for interpreting commodity risk and forecasting. A model may reproduce asymmetric spikes and low-price smoothing yet fail to explain the duration of price movements. Observing inventory smoothing is not enough to attribute persistent prices to inventory. The paper also demonstrates an identification limit: with only prices and linear demand, the scale and location of the primitive shock cannot be separately recovered from demand parameters. A numerical optimizer cannot resolve that observational equivalence.

## Primitive economy and equilibrium restrictions

Time is annual in the empirical application. Let $z_t$ be an exogenous net-supply state. In the absence of inventories, price is $P(z_t)$. The authors call $z_t$ a harvest, but allow it to combine supply and demand shocks; negative values under normalization should therefore not be interpreted as negative physical agricultural production.

The empirical inverse-demand function is linear:

$$
P(z)=a+bz,\qquad b<0.
$$

The primitive process is stationary and first-order Markov, with transition distribution

$$
\Phi(z,Z)=\Pr(z_{t+1}\le Z\mid z_t=z).
$$

The two specifications are IID shocks and an autoregressive alternative, written initially as

$$
z_{t+1}-\mu=\rho(z_t-\mu)+\sigma\varepsilon_{t+1},
\qquad E(\varepsilon_{t+1}\mid z_t)=0,
\quad\operatorname{Var}(\varepsilon_{t+1}\mid z_t)=1.
$$

The innovations have compact support. The autoregressive equation's innovation scale and the stationary scale of $z_t$ are different objects; for the exact stationary AR(1), the latter variance is $\sigma^2/(1-\rho^2)$. A numerical discrete-state approximation must specify which scale it normalizes.

Let $I_t\ge0$ be inventory held at the end of $t$, $r$ the constant real interest rate, and $\delta$ the fraction physically lost over one period. Available supply before consumption and new inventory is

$$
x_t=z_t+(1-\delta)I_{t-1}.
$$

Risk-neutral competitive holders compare the cost of buying a unit today with its depreciated expected resale value. Define $\beta=(1-\delta)/(1+r)$. Their complementarity conditions are

$$
p_t-\beta E_t[p_{t+1}]\ge0,\qquad
I_t\ge0,\qquad
I_t\{p_t-\beta E_t[p_{t+1}]\}=0.
$$

When there are no stocks carried forward, all current availability is consumed and the price is $P(x_t)$. With positive stocks, the expected gross price increase must cover interest and physical loss. Combining the two regimes gives the source's Equation (5):

$$
p_t=\max\{\beta E_t[p_{t+1}],P(x_t)\}.
$$

This is an equilibrium restriction with no separate risk premium, transaction cost, capacity constraint, or inventory financing friction. The commodity cannot be borrowed from future production, which explains $I_t\ge0$. A model allowing stock borrowing or negative inventories would change the kink that drives the analysis.

## Policy function and state transition

Under the stated continuity, monotonicity, compact-support and positive-carry conditions, the authors use the unique nonnegative equilibrium price function $f(x,z)$, decreasing in availability. The principal requirements include observing the current harvest and availability, and $r+\delta>0$. They refer to earlier existence results and extensions rather than reproving them here; a unique invariant distribution of the resulting state process is additionally assumed.

Consumption is $P^{-1}(p)=(p-a)/b$. The inventory policy and next availability are

$$
I(x,z)=x-P^{-1}(f(x,z)),
$$

$$
x_{t+1}=(1-\delta)I(x_t,z_t)+z_{t+1}.
$$

Consequently the equilibrium fixed point is

$$
f(x,z)=\max\left\{
\beta\int f\left(z'+(1-\delta)[x-P^{-1}(f(x,z))],z'\right)
\Phi(z,dz'),\ P(x)
\right\}.
$$

The price on the right also determines current consumption and thus next period's stocks. This is not a linear autoregression fitted directly to observed prices. Each candidate parameter vector requires solving an equilibrium function before evaluating its statistical fit.

For each $z$, there is a threshold availability $x^*(z)$ and associated price $p^*(z)$. Below that availability, equivalently above the threshold price, storage is zero. Above the threshold availability, storage is positive and price exceeds the no-storage price $P(x)$. Both price and inventory policies kink at the boundary.

If a larger current harvest shifts the next-harvest distribution upward in first-order stochastic dominance, the price function also falls with current harvest conditional on availability. Current abundance then signals future abundance and reduces the incentive to carry stocks. The source describes an opposite-direction conjecture for negatively autocorrelated shocks but expressly does not prove it. That conjecture is not needed for the fitted positive-persistence results.

For positive inventories,

$$
E[p_{t+1}\mid p_t,z_t]=\frac{1+r}{1-\delta}p_t.
$$

At a stockout, the conditional expectation is instead the expected price when next availability is just the next harvest. With IID shocks, the threshold is constant and the conditional-mean restriction becomes

$$
m(p)=E[p_{t+1}\mid p_t=p]
=\frac{1+r}{1-\delta}\min\{p,p^*\}.
$$

Here consistency requires $p^*=\beta E[f(z)]$. The mean forecast rises proportionately with price below the threshold and is flat above it. For convex inverse demand, including the linear specification, the IID model also implies conditional variance increasing with current price: low inventories provide less protection against subsequent adverse shocks. These are much sharper predictions than a generic claim of mean reversion.

## Identification and the appendix proof

Proposition 1 concerns an exact invariance, not approximate numerical collinearity. Start with a normalized economy and transform its shock and availability coordinates by

$$
\widetilde z=\mu+\sigma z,\qquad
\widetilde x=\mu+\sigma x,\qquad \sigma>0.
$$

Use transformed inverse demand

$$
\widetilde P(u)=a-\frac{b\mu}{\sigma}+\frac b\sigma u,
$$

and the correspondingly transformed Markov kernel. Then $\widetilde P(\mu+\sigma x)=P(x)$. Define

$$
\widetilde f(\mu+\sigma x,\mu+\sigma z)=f(x,z),\qquad
\widetilde I(\mu+\sigma x,\mu+\sigma z)=\sigma I(x,z).
$$

The appendix checks both equilibrium equations. Consumption transforms as $\widetilde P^{-1}(p)=\mu+\sigma P^{-1}(p)$, hence

$$
\widetilde x-\widetilde P^{-1}(p)=\sigma[x-P^{-1}(p)].
$$

The next availability transforms as

$$
\widetilde z'+(1-\delta)\widetilde I
=\mu+\sigma[z'+(1-\delta)I].
$$

Substituting into the continuation expectation and changing variables in the kernel reproduces the original price equation. Uniqueness then identifies the transformed policies with the new economy's equilibrium. With correspondingly transformed initial states, the entire price path is unchanged, while inventory quantities scale by $\sigma$.

Only price observations therefore cannot separately identify shock location and scale together with the demand intercept and slope. Normalizing the driving process removes redundant parameters; it does not empirically establish a particular harvest unit or mean. Physical inventory or quantity observations would provide additional information absent from this exercise.

There is a printed parenthesis slip in Equation (13), p. 906. Its intermediate expression places $(1-\delta)$ outside $(I_{t-1}+z_t)$. The definitions and appendix require $\sigma[(1-\delta)I_{t-1}+z_t]+\mu$, which equals $\sigma x_t+\mu$. The expression above is the derived correction; depreciation applies to carried inventory, not to the current harvest.

## Data and empirical target

The sample comprises annual average prices for twelve commodities from 1900 through 1987, obtained from the World Bank commodity division: cocoa, coffee, copper, cotton, jute, maize, palm oil, rice, sugar, tea, tin, and wheat. The series are price indexes deflated by a U.S. consumer-price index. The article does not provide an exact index-base convention or a machine-readable data archive. Bananas, present in the earlier research, are omitted because the authors cannot obtain sensible results.

There are eighty-eight annual observations and eighty-seven one-year transitions before any unavailable-data adjustment; the paper describes no further filtering rule. A U.S. CPI is used because a long industrial-country consumption-price index is unavailable. This choice can affect apparent persistence and structural stability. The annual averaging also separates these observations from end-of-period prices in the theoretical state equation.

The authors acknowledge commodity cartels, changes in supply and demand, and the doubtful interpretation of an annual harvest for metals. Stationary net-demand shocks over this long sample are a maintained simplification supported mainly by the absence of an obvious deterministic trend. No structural-break model is estimated. The results therefore reject a particular parsimonious explanation of these price series, not every possible inventory model.

The main statistical targets are the first two conditional moments of next year's price given this year's price. Inventory and the primitive harvest are not observed by the econometrician. Their absence becomes particularly important in the dependent-shock specification.

## IID estimation: a reconstructable computational sequence

For an IID primitive shock, price is a monotone function $f(x)$ of a single state. After solving the fixed point, invert the observed price to obtain $x=f^{-1}(p)$. The conditional transition is

$$
p_{t+1}=f\left((1-\delta)[f^{-1}(p_t)-P^{-1}(p_t)]+z_{t+1}\right).
$$

Integrating this transition yields conditional mean $m_\theta(p)$ and variance $s_\theta(p)$. The authors fit these moments with a Gaussian pseudo-likelihood. In a consistently normalized implementation, maximize

$$
\mathcal L(\theta)=\sum_{t=1}^{T-1}\ell_t(\theta),\qquad
\ell_t=-\frac12\left[\log(2\pi)+\log s_\theta(p_t)
+\frac{[p_{t+1}-m_\theta(p_t)]^2}{s_\theta(p_t)}\right].
$$

Conditional normality is not a claim of the economic model. The criterion rewards small forecast errors and small, correctly allocated conditional variances. Under correct conditional moments and suitable identification/regularity, quasi-likelihood can remain consistent despite nonnormal conditional distributions. The price-function kink makes exact-density likelihood less convenient; the moment criterion avoids explicitly evaluating the density transformation's Jacobian.

The numerical setup fixes $r=0.05$. It approximates a standard normal shock using ten equally likely nodes

$$
z\in\{\pm1.755,\pm1.045,\pm0.677,\pm0.386,\pm0.126\}.
$$

These are conditional means of ten equiprobable normal bins. The displayed rounded nodes have mean zero but variance 0.9590502, not exactly one. That is a finite discretization effect: reproducing the source's node calculation and rescaling it to exact unit variance are different numerical specifications. The original program is needed to establish whether extra unprinted normalization was applied.

The estimated unconstrained parameters are mapped to economically constrained quantities through

$$
a=\theta_1,\qquad b=-e^{\theta_2},\qquad
\delta=-0.05+e^{\theta_3}.
$$

This imposes $b<0$ and $\delta>-r$. It allows negative physical depreciation, so feasibility for the numerical equilibrium does not ensure economic plausibility. Actual IID estimates are positive. A general implementation must also enforce the domain needed for positive surviving inventory; the printed transform alone does not impose $\delta\le1$.

Initialize $f_0(x)=\max\{P(x),0\}$, substitute the current approximation into the right side of the fixed-point equation, and iterate to convergence. Functions are tabulated on an equally spaced availability grid and interpolated by cubic splines. The minimum grid point is the smallest harvest, −1.755. For positive depreciation, the authors use the finite bound $1.755/\delta$ to guide the upper endpoint. They choose a grid before estimation using trial parameter values and report some trial and error in establishing adequate support.

The article does not state the number of grid points, convergence tolerances, optimizer, starting values, extrapolation rule, monotonicity safeguards for splines, or differentiation steps. These are consequential because inversion requires a usable monotone policy and optimization repeatedly changes the region near the kink. No author-code output is supplied to resolve them.

For robust inference, use scores $g_t=\partial\ell_t/\partial\theta$ and Hessian $H=\partial^2\mathcal L/\partial\theta\partial\theta'$, producing $H^{-1}(\sum_tg_tg_t')H^{-1}$ with a common likelihood normalization. The printed Equations (17)–(19) are inconsistent if read literally: (17) sets $2\log L=\sum\log l_t$, while (18) differentiates $\log l_t$ for the scores but $\log L$ for the Hessian. That mixed scaling would multiply the conventional covariance by four. The normalization above is a derived implementation clarification, not an assertion that the authors' unprovided code used the inconsistent factors. Reported table standard errors are retained as printed.

## IID results: persistence is far too small

Table 1 reports the following fitted depreciation and actual versus model-implied first-order price autocorrelation. Depreciation is a fraction per year, while correlations are dimensionless.

| Commodity | Fitted $\delta$ | Reported SE | Actual correlation | Fitted-model correlation |
|---|---:|---:|---:|---:|
| Cocoa | 0.116 | 0.04 | 0.834 | 0.298 |
| Coffee | 0.139 | 0.02 | 0.804 | 0.242 |
| Copper | 0.069 | 0.02 | 0.838 | 0.392 |
| Cotton | 0.169 | 0.03 | 0.884 | 0.192 |
| Jute | 0.096 | 0.05 | 0.713 | 0.302 |
| Maize | 0.059 | 0.03 | 0.756 | 0.356 |
| Palm oil | 0.058 | 0.03 | 0.730 | 0.416 |
| Rice | 0.147 | 0.06 | 0.829 | 0.224 |
| Sugar | 0.177 | 0.03 | 0.621 | 0.264 |
| Tea | 0.123 | 0.04 | 0.778 | 0.230 |
| Tin | 0.148 | 0.05 | 0.895 | 0.256 |
| Wheat | 0.130 | 0.03 | 0.863 | 0.259 |

For completeness, the fitted $(a,b)$ pairs are cocoa $(.162,-.221)$, coffee $(.263,-.158)$, copper $(.545,-.326)$, cotton $(.642,-.312)$, jute $(.572,-.356)$, maize $(.635,-.636)$, palm oil $(.461,-.429)$, rice $(.598,-.336)$, sugar $(.643,-.626)$, tea $(.479,-.211)$, tin $(.256,-.170)$, and wheat $(.723,-.394)$. They are normalized price/shock-coordinate parameters, not dollar prices or directly interpretable physical demand elasticities.

The storage model materially reduces variability relative to its no-storage counterfactual, yet does not generate observed persistence. For example, the fitted cocoa no-storage dispersion is roughly twice the actual dispersion. This separates smoothing in variance from explaining autocorrelation.

The cost-covering growth restriction fails in a second way. At the fitted cocoa depreciation, positive stocks require expected one-year price growth factor $1.05/(1-.116)=1.1878$. The earlier direct GMM estimate of the corresponding low-price slope is only 1.025, with reported SE 0.14. For cotton, the fitted factor is 1.2635 versus the direct estimate 1.013, SE 0.05. The authors report this direction of discrepancy across all twelve goods. These comparisons should use the exact ratio, not the rough approximation $1+r+\delta$ when depreciation is appreciable.

Their threshold-buying diagnostic asks whether observed low prices subsequently rise enough to cover carrying costs. With a cutoff at the sample median and total costs of at least 5% annually, the strategy loses over the sample for all goods except cocoa, coffee, and maize; at the upper-quartile cutoff, it loses for all twelve. This is a model-consistency check, not an executable futures backtest. It excludes a separate risk premium and assumes the trader's information is the modeled price information.

Figure 1 makes the failure visible for cotton. The IID-storage forecast becomes nearly flat whenever price exceeds the stockout threshold, while actual high prices remain persistent. A linear AR(1), though itself imperfect at rapid declines from peaks, tracks that high-price dependence much better.

## Autocorrelated shocks and hidden-state integration

With dependent harvests, $(x_t,z_t)$ is Markov but the observed price alone need not be. A given price can arise from several availability/harvest pairs. It is therefore incorrect to invert $p_t$ to one unique two-dimensional state or to treat the hidden harvest as observed.

The source computes the invariant joint distribution of the state process and uses it to weight all states compatible with the observed price. In conditional-distribution notation, if $\pi(dx,dz\mid f(x,z)=p)$ is the model-implied stationary distribution conditional on price, then the required first moment is

$$
m(p)=\int\!\int f\big((1-\delta)I(x,z)+z',z'\big)
\Phi(z,dz')\,\pi(dx,dz\mid p).
$$

Compute the second raw moment by replacing $f$ with $f^2$, then subtract $m(p)^2$ to obtain variance. Averaging conditional variances alone would omit the between-hidden-state variance. The numerical handling of conditioning on a continuous price, stationary weights, interpolation, and state-grid transitions is delegated primarily to the companion 1995 paper.

The paper still fits $E[p_{t+1}\mid p_t]$ and $\operatorname{Var}(p_{t+1}\mid p_t)$ rather than exploiting the whole observed price history. It explicitly acknowledges that earlier prices can add information in the dependent model. This is not a full nonlinear filtering likelihood. Any new inference procedure for this reduced-information criterion must consider serial dependence in its score rather than automatically borrowing the IID-case covariance formula.

A simulation first establishes what storage *can* do. A ten-state harvest chain is constructed to have a specified autocorrelation; the source does not print its transition matrix. For each configuration, 2,000 observations are simulated from zero inventories and the first 100 are discarded. The remaining 1,900 prices yield a sample first-order correlation. Figure 2 uses $a=.2$, $b=-.5$, and depreciation ranging from .025 to one. At zero harvest correlation and low depreciation, storage can raise price correlation above .5. As harvest persistence grows, the additional increase becomes smaller. This is an illustrative parameter experiment, not the fit to the twelve observed series.

Figures 3–4 use $a=.2$, $b=-.2$, $\delta=.05$, and harvest correlation .5. Integrating over unobserved harvest smooths the individual-state kinks. At high persistence, the resulting conditional mean becomes closer to a linear AR(1); inventory remains more visible in the conditional variance.

## Dependent-model estimates and fit decomposition

The numerical optimization is difficult. The authors report the highest criterion values they located, not certified global optima, and could not obtain useful standard errors for the dependent model. Their companion Monte Carlo evidence is summarized by one revealing case: with true $\rho=.5$, one hundred replications give mean estimated persistence .40 and standard deviation .25. This is substantial finite-sample uncertainty.

The fitted dependent-model persistence and depreciation from Table 3 are:

| Commodity | $\rho$ | $\delta$ |
|---|---:|---:|
| Cocoa | .837 | .083 |
| Coffee | .833 | .036 |
| Copper | .751 | −.046 |
| Cotton | .945 | .010 |
| Jute | .741 | .053 |
| Maize | .720 | −.050 |
| Palm oil | .864 | −.050 |
| Rice | .889 | .027 |
| Sugar | .626 | .112 |
| Tea | .918 | .232 |
| Tin | .918 | .046 |
| Wheat | .785 | .051 |

The table's −.050 entries are rounded boundary values; the transform enforces a strict lower bound greater than −.05. Negative depreciation for copper, maize, and palm oil is not a plausible physical loss rate. Near $\delta=-r$, the carry wedge approaches zero, permitting very large inventories. These boundary fits cannot be presented as ordinary evidence of realistic profitable storage.

Table 2 compares log pseudo-likelihoods evaluated through the dependent-model machinery:

| Commodity | IID + storage | AR without storage | AR + storage | Same full-model parameters, constant variance |
|---|---:|---:|---:|---:|
| Cocoa | 123.6 | 117.6 | 141.6 | 124.4 |
| Coffee | 109.9 | 110.2 | 131.2 | 119.7 |
| Copper | 75.0 | 73.2 | 103.1 | 82.2 |
| Cotton | 33.9 | 69.6 | 79.0 | 74.6 |
| Jute | 42.0 | 47.2 | 53.3 | 49.2 |
| Maize | 30.6 | 22.2 | 46.2 | 27.9 |
| Palm oil | 24.1 | 17.3 | 58.9 | 19.3 |
| Rice | 22.0 | 55.9 | 61.0 | 59.4 |
| Sugar | −15.1 | −28.9 | −3.90 | −23.5 |
| Tea | 67.0 | 99.8 | 102.5 | 100.5 |
| Tin | 106.1 | 149.5 | 152.3 | 150.5 |
| Wheat | 22.0 | 50.0 | 53.2 | 50.2 |

The last column replaces the fitted conditional variance function by its sample average while holding the other full-model parameters fixed. It is a diagnostic, not a separately reoptimized homoskedastic model. Much of the full-model improvement disappears, indicating that state-dependent variance accounts for a large part of the fit gain.

The no-storage AR comparison is implemented in this table using estimated AR parameters and $\delta=.9$, which approximates the relevant no-storage fit; the theoretical experiment with $\delta=1$ eliminates surviving inventory exactly. These two constructions should not be conflated. The source notes approximation differences when comparing the separate programs.

Twice a pseudo-log-likelihood difference does not have the ordinary likelihood-ratio chi-square law here, even for nested specifications. The paper expressly warns against that inference. No p-values or standard errors should be manufactured from these criterion differences. Nor do the negative values for sugar signal a problem by themselves: density-based criterion levels depend on units and normalization.

## Interpretation and replication limits

The fitted explanation is persistent fundamentals plus a storage buffer, not weakly persistent fundamentals amplified enough to reproduce all observed persistence. When a price disturbance is expected to persist for many years, smoothing it requires large, costly inventories held for a long time. Modest short-term smoothing is then rational, and its strongest observable effect can be lower variance when availability is high.

The inference that demand shocks may be more plausible than independent weather shocks is an economic interpretation conditional on the primitive model. The article does not identify a separate demand series or estimate a structural supply-and-demand system. Cartels, changing technology, heterogeneous storage costs, risk aversion, long-run trends, and time aggregation remain possible reasons why this specification fails.

A faithful reconstruction needs the original twelve price-index histories and deflator, the discrete Markov transition construction and normalization, availability grids, spline and stationary-distribution algorithms, optimizer settings and starting values, convergence checks, and code for integrating hidden states conditional on price. It should reproduce the IID policy kink, the scale/location invariance, the threshold conditional mean, the published criterion comparisons, and their sensitivity to discretization before making new economic claims.

The article's strongest result is a disciplined failure of an intuitively appealing mechanism at its fitted parameters. It also supplies a reusable workflow: solve equilibrium, derive observable conditional moments, estimate only identifiable parameters, inspect implied unconditional dynamics, and distinguish economically sensible fits from solutions obtained by collapsing the carrying-cost wedge.
