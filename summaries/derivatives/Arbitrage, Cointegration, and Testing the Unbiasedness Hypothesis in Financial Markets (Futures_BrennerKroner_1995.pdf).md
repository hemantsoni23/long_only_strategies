# Arbitrage, Cointegration, and Testing the Unbiasedness Hypothesis in Financial Markets

Robin J. Brenner and Kenneth F. Kroner, *Journal of Financial and Quantitative Analysis* 30(1), March 1995, pp. 23–42. [Source PDF](../../Finance/futures/Futures_BrennerKroner_1995.pdf). The supplied PDF has a JSTOR cover followed by the twenty article pages; article p. 23 is PDF p. 2. References below use printed article pages.

## Why this matters

A futures price incorporates the financing and benefits or costs of carrying the underlying asset. It is consequently dangerous to interpret the futures–spot basis as either a forecast of the spot return or a pricing error without specifying those carrying terms. This paper connects the cash-and-carry identity to cointegration. A stationary carry term ties log spot and log forward prices together with a unit long-run coefficient. A nonstationary carry term must normally enter the long-run relation explicitly. The economically relevant system can therefore have three variables even when the trading problem initially appears to involve only spot and futures.

The practical contribution is a framework for choosing the variables in a forecasting or hedging model before estimating its time-series parameters. It also distinguishes no-arbitrage pricing from the stronger hypothesis that a forward price is an unbiased forecast of the subsequent spot price. A rejection of an unbiasedness regression is not automatically evidence of an exploitable arbitrage or irrational forecasting. The paper's currency-versus-commodity comparison is useful precisely because financing differentials, storage costs, and convenience yields have different stochastic properties.

Several printed signs and several broad statistical interpretations require qualification. This note reconstructs the identities directly and identifies corrections separately from the authors' claims. The most robust result is the carry-adjusted stationary relation. Neither arbitrary nonstationary carry nor cointegration alone determines all cointegrating vectors, causal adjustment coefficients, or the slope of a conditional-mean regression.

## Model, timing, and the cost of carry

Let $S_t$ be the spot price, $f_{t\mid t-k}$ the forward delivery price quoted at time $t-k$ for delivery at $t$, and $F_{t\mid t-k}$ the corresponding futures price. These are contract prices, not the market value of an already initiated forward position. The horizon $k$ is fixed across observations in the basic argument. Define $s_t=\log S_t$, $\ell_{t\mid t-k}=\log f_{t\mid t-k}$, and $d_{t\mid t-k}=\log D_{t\mid t-k}$, where $D$ is the gross carry multiplier.

The spot process in Eq. (1), p. 25, is

$$
dS_t=\mu S_t\,dt+S_t\sum_{i=1}^{n}\gamma_i\,dW_{i,t},\qquad \sigma^2=\sum_{i=1}^{n}\gamma_i^2.
$$

The Brownian factors are independent, and the coefficients are constant. Itô's formula gives

$$
s_t-s_{t-k}=mk+\varepsilon_{t,k},\qquad m=\mu-\frac{\sigma^2}{2},\qquad \varepsilon_{t,k}=\sum_i\gamma_i(W_{i,t}-W_{i,t-k}).
$$

For an individual horizon, $\varepsilon_{t,k}$ is normal with mean zero and variance $k\sigma^2$. Thus $μ$ in the stochastic differential equation is the instantaneous proportional price drift; the log-return drift is $m$. The source's prose sometimes calls $μ$ the mean continuously compounded return, but its own Eq. (2) uses the correct Itô adjustment.

For currency contracts, $S$ is domestic currency per unit of foreign currency. Let $P^d_{t\mid t-k}$ and $P^f_{t\mid t-k}$ be domestic and foreign zero-coupon bond prices, each paying one unit of its own currency at maturity. Covered interest parity gives

$$
f_{t\mid t-k}=S_{t-k}\frac{P^f_{t\mid t-k}}{P^d_{t\mid t-k}}=S_{t-k}D_{t\mid t-k}.
$$

If the continuously compounded yields are $r^d$ and $r^f$, then $d=k(r^d-r^f)$. This is an identity between contemporaneous tradable prices, not a statement about the physical expectation of the future exchange rate. Domestic borrowing, foreign investment, and a forward currency sale replicate the relevant future payment.

For a storable commodity, replace the foreign yield by the negative of net storage cost. Writing $c$ for storage cost less convenience yield, expressed as an annualized continuously compounded rate, yields $d=k(r^d+c)$. For an equity with known dividend yield $q$, the corresponding expression is $d=k(r^d-q)$. The signs matter: storage raises the forward price, whereas dividends and convenience benefits lower it. Rates and horizons must use compatible units.

The commodity equality requires the ability to implement the relevant carry and reverse-carry trades. Footnote 4, p. 26, explicitly acknowledges that low inventories and difficulty shorting the physical commodity can invalidate the frictionless equality. A low futures price can then coexist with a high spot price without an executable reverse-carry arbitrage. The source presents this as an alternative explanation for commodity evidence. A modern application must also distinguish a measurable storage expense from an imputed convenience yield; the latter is often obtained from the same basis that it is supposed to explain.

For futures, Eq. (4) invokes the stochastic-interest-rate framework of Amin and Jarrow:

$$
F_{t\mid t-k}=S_{t-k}D_{t\mid t-k}\exp(Q_{t\mid t-k}).
$$

Here $Q$ is an adjustment for marking to market. The paper assumes the volatility/correlation conditions needed by that pricing result and treats $Q$ as nonstochastic at fixed horizon. It depends on the relevant spot and interest-rate volatilities and tends to zero as $k$ tends to zero. Brenner and Kroner do not reproduce its general closed form. Consequently, their paper is not by itself a numerical implementation specification for a stochastic-rate futures convexity adjustment. If an application makes $Q$ stochastic and nonstationary, it must become an additional component of the long-run relation rather than silently remain in the intercept.

## The stationary relation and its proof

Combining the spot increment with the forward carry identity gives

$$
s_t-\ell_{t\mid t-k}=mk-d_{t\mid t-k}+\varepsilon_{t,k}.
$$

For futures the same substitution gives

$$
s_t-\log F_{t\mid t-k}=mk-d_{t\mid t-k}-Q_{t\mid t-k}+\varepsilon_{t,k}.
$$

This second equation is a derived correction to the printed Eq. (6b), p. 28. The printed expression puts $+Q$ inside a bracket multiplied by $k$, although Eqs. (4)–(5b) define the log futures price with an additive $+Q$. Subtracting that price necessarily gives $-Q$, without an extra factor $k$. With deterministic fixed-horizon $Q$, the error changes an intercept and does not overturn the stationary-versus-nonstationary argument.

Assume that $s_t$ and the contract-price series are $I(1)$ and that $d$ is $I(0)$. Their difference is then stationary, so the bivariate cointegrating vector is $(1,-1)$. The source's Appendix, pp. 39–40, proves this by writing the linear combination as a constant plus stationary carry and stationary noise. Replacing either series by a fixed lead or lag adds only a finite sum of stationary increments, leaving the cointegrating relation intact. The conclusion is about fixed offsets, not an unrestricted changing-maturity construction.

If carry is itself $I(1)$, the algebra instead supplies

$$
s_t-\ell_{t\mid t-k}+d_{t\mid t-k}=mk+\varepsilon_{t,k}.
$$

For the ordered system $(s,\ell,d)$, the vector is $(1,-1,+1)$. This is the vector in the Proposition and Appendix. The discussion on p. 34 prints $(1,-1,-1)$; that sign is inconsistent with both the carry identity and the stated proof. The trivariate relation requires all three components to have the integration orders being claimed. It is not meaningful to describe an already stationary forward series as an $I(1)$ component merely because the spot and carry series are individually integrated.

Two restrictions on the interpretation are consequential. First, the source says that failure of cointegration between $s$ and $d$ with vector $(1,-1)$ ensures that $\ell=s+d$ retains a stochastic trend. The cancellation to exclude is actually a stationary *sum*, corresponding to $(1,+1)$. For example, $d=-s+u$ with stationary $u$ makes $\ell=u$ stationary, even though $s-d$ is nonstationary. This is a derived algebraic counterexample to the printed noncancellation condition, not an empirical assertion about observed financing rates.

Second, $I(1)$ carry prevents the unit spread $s-\ell$ from being stationary, but it does not rule out every bivariate cointegrating vector. If $d=a s+u$ at aligned dates, with stationary $u$ and $a\ne-1$, then $\ell=(1+a)s+u$. The two prices are cointegrated with vector $(1,-1/(1+a))$, although carry is nonstationary when $a\ne0$. Fixed timing offsets only add stationary increments. To obtain the stronger claim that spot and forward prices have no bivariate cointegration, carry must introduce a stochastic trend independent of the spot trend, or the model must impose an equivalent rank condition. The paper often moves from nonstationary carry to the stronger conclusion without stating that condition.

The Brownian innovation also needs a sampling qualification. The source calls the $k$-period noise independent across observations. This holds for nonoverlapping intervals, but overlapping forecasts share Brownian increments. With unit-spaced observations and integer $k$, the covariance at lag $j$, for $0\le j<k$, is $\sigma^2(k-j)$. A serial-correlation test that ignores this overlap can reject a perfectly valid forecasting model. Stationarity survives; independence does not.

## What the market comparison actually predicts

Currency carry depends on an interest-rate *difference*. It can be stationary when both interest rates are stationary or when their common stochastic trend cancels with a unit coefficient. Commodity carry depends on financing plus net storage cost. The source argues that a persistent interest rate or convenience yield makes this sum more likely to have a stochastic trend. For equities the relevant stationary candidate is interest rate less dividend yield. These are conditional implications, not immutable classifications of asset classes. Correlated components can cancel; stationary components can be very persistent; finite-sample unit-root tests have limited power.

The authors use fixed-maturity contracts because the derivation holds $k$ constant. For a single expiring contract, both time to delivery and the variance of the future spot innovation shrink. A front-contract roll produces another timing pattern. These complications prevent a direct application of the paper's constant-horizon stationary-error specification. They do not establish a general theorem that every varying-maturity series is incapable of cointegration. A researcher must describe interpolation, roll dates, delivery locations, and any predictable maturity-dependent variance before interpreting a rejection.

Tables 1–3 summarize previous studies. They are not new estimates produced from a common database, and they do not provide standard errors or a harmonized testing protocol. Their contrasts cannot be treated as a controlled cross-market experiment.

Table 1, p. 31, lists no detected cointegration for every reported commodity row. Baillie and Myers use daily 1981–1982 data: the estimated second vector elements are −0.970 for beef, −0.926 coffee, −1.058 corn, −0.624 cotton, −1.337 gold, and −0.280 soybeans. Bessler and Covey report −1.040 for cattle using daily 1985–1986 observations. Chowdhury's quarterly July 1974–June 1988 entries are −2.313 copper, −1.965 lead, −11.305 tin, and −0.788 zinc. Schroeder and Goodwin's daily 1975–1989 live-hog study reports no coefficient in this table and tests years separately, finding no cointegration in virtually every year. The commodity entries use futures, denoted by capital F.

Table 2, p. 32, is predominantly currency forwards, denoted by lower-case f. It is essential to distinguish Y from the question mark: the latter means cointegration was not tested, not that it was established. Earlier regressions include coefficients well away from −1, such as −0.729 for one Canadian subsample and −0.830 for France in Edwards. Among explicit tests, Baillie and Bollerslev's daily March 1980–January 1985 sample finds cointegration for seven currencies, with second elements from −1.011 to −0.848. Hakkio and Rush's monthly July 1975–October 1986 results are −0.990 for the UK and −0.970 for Germany. Copeland's daily 1976–1990 estimates range from −1.001 to −0.996 for five currencies. Lai and Lai's monthly July 1973–December 1989 estimates range from −1.002 to −0.994. Kroner and Sultan's weekly February 1985–February 1990 futures estimates are −0.993 UK, −1.000 Germany, −1.000 Switzerland, −0.994 Japan, and −1.010 Canada. These examples substantiate the tendency toward a unit relationship without converting that tendency into an exact population restriction.

## Four unbiasedness tests

The economic hypothesis combines rational expectations with a zero risk premium or an appropriate risk-neutrality assumption. It is stronger than absence of arbitrage. Moreover, a level-price statement $E_t[S_{t+k}]=f_{t+k\mid t}$ differs from $E_t[s_{t+k}]=\ell_{t+k\mid t}$. Under lognormality, the difference is a Jensen adjustment of half the conditional log variance. A pricing expectation under a martingale measure is also not automatically the physical forecasting expectation. The paper's log-linear tests therefore need to be interpreted as their particular joint nulls, rather than as universal tests of financial-market efficiency.

The first test asks whether spot and the earlier contract price are cointegrated with the appropriate unit vector. Stationary forecast errors make this a necessary condition for log unbiasedness when the prices are integrated. It is not sufficient: a stationary nonzero mean error or a stationary predictable risk premium is compatible with cointegration. Under the paper's constant-drift spot model, nonstationary carry makes the unit forward forecast error nonstationary. That conclusion depends on the maintained conditional-mean model as well as carry pricing.

The second test estimates a level regression,

$$
s_{t+k}=\alpha+\beta\ell_{t+k\mid t}+e_{t+k},
$$

and considers $(\alpha,\beta)=(0,1)$ plus residual restrictions. Write $d=\bar d+\eta$. The structural identity is

$$
s_{t+k}=(mk-\bar d)+\ell_{t+k\mid t}+(\varepsilon_{t+k,k}-\eta_{t+k\mid t}).
$$

Thus the unit slope can coexist with a nonzero intercept and a serially correlated residual. The printed Eq. (10) has the minus sign on $\eta$; nearby prose and Eq. (11) switch to a plus sign. The minus sign follows directly from subtracting carry. Persistence in $\eta$ can induce persistence in forecast errors. Deterministic carry is sufficient for eliminating this channel, but not necessary: independent white-noise carry can also produce a serially uncorrelated residual under suitable joint assumptions.

The regression's integrated regressors create nonstandard inference. A superconsistent cointegrating coefficient is not a license to use ordinary independent-observation t statistics. Endogeneity, residual serial dependence, overlapping horizons, deterministic terms, and the method used to estimate the cointegrating vector still matter. The paper does not supply a universal finite-sample correction or a recommended lag-selection algorithm.

The third test differences prices, regressing $\Delta s_t$ on the change in the rolling forward-price series. The authors emphasize that differencing alone can discard a stationary equilibrium error. Their proposed regression, Eq. (12), is

$$
\Delta s_t=\alpha+\beta\Delta\ell_{t\mid t-1}+\delta(\ell_{t-1\mid t-2}-s_{t-1})+e_t.
$$

They state the unbiasedness restrictions $(\alpha,\beta,\delta)=(0,1,1)$. The identity motivating this specification, with stationary one-period carry, is

$$
\Delta s_t=m-\bar d+\Delta\ell_{t\mid t-1}+(\ell_{t-1\mid t-2}-s_{t-1})+\varepsilon_t-\eta_{t\mid t-1}.
$$

This explains why an equilibrium term belongs in a general dynamic specification. However, its residual contains current carry and need not be orthogonal to the regressors. The coefficients of an accounting identity are not automatically the coefficients of an OLS conditional projection. In the maintained constant-drift Brownian spot model, every regressor known at $t-1$ has zero predictive coefficient for $\Delta s_t-m$ under the model filtration. The source's claim of downward omitted-variable bias relative to a structural coefficient of one therefore requires attention to the simultaneous carry innovation, not just the missing equilibrium term. A valid empirical implementation should specify a conditional dynamic model, lagged information set, and innovation orthogonality explicitly.

If carry is integrated, Eq. (13) instead includes both $\Delta d$ and the lagged carry-adjusted equilibrium error. This is the appropriate dimensional lesson: the additional stochastic trend cannot be eliminated by differencing just the two prices. The paper's conclusion that no unbiasedness restrictions can hold is tied to its constant expected spot growth and nonstationary carry, not a general impossibility theorem for commodity expectations under every model.

The fourth test is the forward-premium regression,

$$
\Delta s_{t+1}=\alpha+\beta(\ell_{t+1\mid t}-s_t)+e_{t+1}.
$$

Under log unbiasedness the familiar restriction is $(\alpha,\beta)=(0,1)$. Under the paper's spot model, $\Delta s_{t+1}=m+\varepsilon_{t+1}$, while the regressor is time-$t$ carry. If that information is adapted to the Brownian filtration, the population predictive slope is zero. This does not emerge from no-arbitrage alone; it follows from imposing a constant physical conditional spot drift while allowing a stochastic carry differential. Footnote 12 acknowledges the asymmetry: assigning the primitive diffusion to the forward price instead reverses the proposed direction of adjustment.

## Error correction, persistence, and the evidence table

The paper rewrites the one-period system as

$$
s_t=m+s_{t-1}+\varepsilon_t,\qquad \ell_{t+1\mid t}=\bar d+s_t+\eta_{t+1\mid t}.
$$

Define $z_{t-1}=\ell_{t\mid t-1}-s_{t-1}-\bar d=\eta_{t\mid t-1}$. Algebra gives

$$
\Delta\ell_{t+1\mid t}=m-z_{t-1}+\varepsilon_t+\eta_{t+1\mid t}.
$$

The authors interpret this as error-correction loadings $(\gamma_s,\gamma_f)=(0,-1)$. The first is consistent with their constant-drift spot assumption. The second is an innovation-regression loading only with additional restrictions on carry. If centered carry follows $\eta_{t+1\mid t}=\rho\eta_{t\mid t-1}+u_t$, with $u_t$ a genuine innovation, the conditional adjustment loading becomes $\rho-1$. Hence a persistent stationary carry process with $\rho=0.9$ produces a loading of −0.1, not −1. This derived example is particularly relevant because persistent carry is one of the paper's central explanations for persistent bases. The algebra with a coefficient −1 remains true, but its residual then includes a predictable component.

Table 3, p. 38, summarizes reported $\gamma_s$ estimates rather than providing a new estimation exercise. Fama's nine entries are all negative: Belgium −1.580, Canada −0.870, France −0.870, Italy −0.510, Japan −0.290, Netherlands −1.430, Switzerland −1.140, UK −0.900, and Germany −1.320. The accompanying text says all reject a unit coefficient, whereas zero would be rejected only once using the reported standard errors. Kroner and Sultan's five entries are −0.300 Canada, 0.260 UK, −0.070 Switzerland, 0.130 Japan, and 0.310 Germany. Their zero restriction is rejected only once, and the source reports that their forward adjustment coefficients never reject −1.

The table's notation requires care. A star under $\gamma_s=0$ means *insignificantly different from zero*; a star under $\gamma_s<1$ means significantly less than one. These are not the same direction of hypothesis-test outcome. The caption prints a spot-minus-forward regressor, whereas Eqs. (9), (15), and (16) use the forward-minus-spot orientation. The reported Fama discussion and unit null follow the latter convention. Any numerical replication must return to the original cited study and verify its orientation instead of changing signs based solely on this caption. Standard errors, exact significance levels for every entry, and all original controls are not reproduced here.

## Reconstructing an application and the limits of this source

A replicable implementation begins with synchronized spot and contract quotes for the same deliverable asset, currency convention, and fixed horizon. It then constructs financing, dividend, storage, and convenience terms with the same compounding and horizon convention. Testing proceeds on the prices and carry jointly: establish plausible integration orders, test the economically implied vector, allow additional common trends, and specify deterministic components before fitting a dynamic system. A carry estimate mechanically backed out of the same futures price cannot serve as independent confirmation of the carry identity.

For forecasting, the information set must stop at the forecast origin. Realized spot at delivery is the target; a contemporaneous delivery-date forward quote is not a substitute. Holdout forecasts should distinguish the level-price objective from log-price objectives and include a no-change benchmark. For hedging, the long-run relation can motivate an equilibrium regressor, but the actual minimum-variance position also requires conditional return covariances, contract multipliers, and a holding period. No hedge ratio, rebalancing rule, transaction-cost model, or out-of-sample performance gain is estimated in this paper.

The supplied source contains its Proposition, Appendix proof, three literature-summary tables, and references. It does not contain a new raw dataset, sample construction code, simulation design, optimized hyperparameters, or original confidence intervals. Reproducing the table entries as econometric results requires the cited papers and their data. The contribution that can be reconstructed from this source alone is the cost-of-carry mapping, the associated stationary linear combinations, and the consequences of imposing different conditional-mean assumptions. The sign repairs and counterexamples above delimit those consequences while preserving the useful central insight: a basis is an economic carrying term before it is a forecasting signal.
