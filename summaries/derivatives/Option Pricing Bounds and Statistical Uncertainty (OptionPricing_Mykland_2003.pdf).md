# Option Pricing Bounds and Statistical Uncertainty

Per A. Mykland. University of Chicago, Department of Statistics, Technical Report 511. The outer cover says September 2001, revised September 2003; the inner manuscript is dated December 2, 2003. This note follows the supplied 68-page file, including its proofs and four final figures.

Source: [OptionPricing_Mykland_2003.pdf](../../Finance/OptionPricing_Mykland_2003.pdf). Page references below use the manuscript's printed pagination: printed page 1 is PDF page 4. This is a theoretical methods paper with one illustrative statistical calibration, not an out-of-sample trading study.

## Why this matters and what is new

An option hedge usually presumes that the model parameters, or at least the volatility law, are known. Estimating that law and then treating the estimate as truth suppresses a distinct risk: the future volatility path may fall outside the region that the data plausibly support. Mykland turns a statistical prediction statement about future paths into a financial solvency statement. The statistician produces a set of paths with specified coverage. The trader constructs a hedge that covers the payoff on every admissible path in that set. The resulting ask price is the least starting capital needed for this conditional superhedge; a corresponding bid comes from the opposite claim.

The innovation is the connection between statistical prediction sets, robust replication, and observable accumulated quadratic variation. It is not the claim that uncertain-volatility superhedging itself is new. Pointwise volatility bounds were already known. Mykland emphasizes bounds on integrated variance, proves a general dual representation under technical conditions, accommodates interest-rate uncertainty and traded bonds, and shows how existing option prices tighten the bounds through static option holdings plus dynamic stock trading.

The distinction between prediction uncertainty and market incompleteness is fundamental. Even in a market that is complete under each individual model, the trader may not know which model is correct. Conversely, an incomplete market can have a completely specified physical probability law. This paper's uncertainty is primarily the first kind, and its robust trading family can deliberately be broader than the family used to fit historical data.

## Basic setup, units, and the coverage guarantee

Let $S_t$ denote a positive continuous stock price and let the bank account be

$$
\beta_t=\exp\left(\int_0^t r_u\,du\right),\qquad \beta_0=1.
$$

A typical local description is $dS_t/S_t=\mu_tdt+\sigma_tdW_t$, with coefficients allowed to be stochastic. Write $V_t^*=V_t/\beta_t$ for discounted wealth. The terminal liability is $\eta$, often $f(S_T)$. The historical information available at inception is denoted here by $\mathcal H$. A prediction set $C$ is selected so that its conditional probability is at least $1-\alpha$, in the frequentist or Bayesian sense appropriate to the inference procedure.

A $C$-superhedge is a strategy with $V_T\geq\eta$ on $C$. The paper allows a super-self-financing strategy: wealth can be withdrawn, but cannot be supplemented by outside funds. Formally it is a self-financing component plus a process whose discounted value is nonincreasing. Subject to admissibility, define

$$
A_0(\eta;C)=\inf\{V_0:V\text{ superhedges }\eta\text{ on }C\},
\qquad B_0(\eta;C)=-A_0(-\eta;C).
$$

If the prediction statement is valid and the hedge exists under the paper's assumptions, then

$$
P(V_T\geq\eta\mid\mathcal H)\geq P(C\mid\mathcal H)\geq1-\alpha.
$$

This is a probability of terminal coverage. It does not bound the loss conditional on failure, guarantee an expected profit, or make $\alpha$ a pricing probability. It is also different from optimizing the successful states as in quantile hedging: here the prediction set is an input, and the trader must cover that set. For an existing book $\eta_0$, the incremental conservative ask for another claim is $A_0(\eta_0+\eta)-A_0(\eta_0)$; adding stand-alone asks generally discards diversification and hedge interaction.

The risk-neutral measures used in the dual calculation assign probability one to $C$. They are computational measures consistent with the trading restrictions. The actual physical or predictive distribution need only assign $1-\alpha$ to $C$. Confusing these two statements would erase exactly the statistical failure risk the paper is designed to expose.

The financial market is frictionless and continuously tradable. No transaction-cost schedule, margin rule, funding spread, jump process, or market-impact model is estimated. Those are material restrictions when translating the terminal guarantee into an implementable strategy.

## From pointwise volatility limits to an integrated-variance budget

Section 3 first relates the proposal to familiar uncertain-volatility hedging. Suppose volatility lies between known functions $\sigma_-(S,t)$ and $\sigma_+(S,t)$ at every instant and the rate is deterministic. A robust value satisfies an HJB equation of the form

$$
A_t+rSA_S-rA+\frac12S^2\max_{\sigma\in[\sigma_-,\sigma_+]}\{\sigma^2A_{SS}\}=0,
\qquad A(S,T)=f(S).
$$

Positive gamma selects the upper volatility; negative gamma selects the lower. Delta trading then generates enough wealth under all admissible volatility paths. For a convex European claim and a constant upper limit, this gives the Black–Scholes price evaluated at the upper variance.

An instantaneous envelope can be much more restrictive than necessary. A brief volatility spike does not require the whole option life to be priced at that spike. Mykland instead uses a prediction interval for total quadratic variation,

$$
\Xi^-\leq\int_0^T\sigma_u^2\,du\leq\Xi^+.
$$

Here $\Xi$ is total variance, not volatility and not annualized variance. For constant volatility, $\Xi=\sigma^2T$. The paper sometimes calls an implied $\Xi$ an implied volatility; a reproduction must preserve the squared units. An analogous interval can be imposed on the integrated short rate $R=\int_0^Tr_u\,du$.

Define a generalized Black–Scholes expectation with independent scalar arguments:

$$
\mathcal B(S,R,\Xi;f)=e^{-R}E\left[f\left(S\exp\{R-\Xi/2+\sqrt{\Xi}Z\}\right)\right],
\qquad Z\sim N(0,1).
$$

For a call with strike $K$,

$$
\mathcal B=S\Phi(d_1)-Ke^{-R}\Phi(d_2),\quad
 d_1=\frac{\log(S/K)+R+\Xi/2}{\sqrt{\Xi}},\quad d_2=d_1-\sqrt{\Xi}.
$$

For a known integrated rate and convex payoff, the upper integrated-variance limit produces a conservative ask. An upper rate limit also works for calls because their value is increasing in that argument. That qualification matters: increasing convex payoffs alone do not automatically imply increasing discounted value in $R$. For example, a positive constant payoff decreases with $R$. The call case has the required sign; a general payoff must be checked through $\mathcal B_R$ rather than inheriting a blanket monotonicity claim.

## The hedge spends remaining variance rather than calendar time

Given initial budgets $\Xi_0$ and $R_0$, define the remaining budgets

$$
\Xi_t=\Xi_0-[\log S]_t=\Xi_0-\int_0^t\sigma_u^2\,du,
\qquad R_t=R_0-\int_0^tr_u\,du.
$$

The hedge value is $A_t=\mathcal B(S_t,R_t,\Xi_t;f)$. Hold $\mathcal B_S$ shares and put the residual value into the money-market account. The identities

$$
\mathcal B_\Xi=\tfrac12S^2\mathcal B_{SS},\qquad
-\mathcal B_R=\mathcal B-S\mathcal B_S
$$

make the Itô terms cancel:

$$
dA_t=\mathcal B_S\,dS_t+r_t(A_t-S_t\mathcal B_S)\,dt.
$$

Thus, until the relevant budget is exhausted, the strategy is self-financing. At maturity, unused nonnegative variance has value for a convex payoff; that residual optionality provides the superhedge. With exact interest integration and upper variance $\Xi^+$, the terminal construction dominates a convex payoff whenever realized variance remains within the budget. It need not be an exact replication, because unused variance usually leaves surplus wealth.

The argument is pathwise once the quadratic-variation restriction is fixed. The drift $\mu_t$, the speed of variance mean reversion, and the market price of volatility risk do not enter this stock hedge. They enter the statistical construction of the prediction interval, or the comparison with traded prices, rather than the cancellation itself.

There is a useful implementation interpretation. An unexpectedly volatile early month reduces remaining variance immediately, even if little calendar time has elapsed. A quiet month leaves a larger variance reserve. The strategy therefore does not repeatedly replace the original uncertainty budget with an unrelated freshly calibrated Black–Scholes volatility. Doing that would change the coverage problem and invalidate the original guarantee unless a new sequential statistical argument were supplied.

Some displayed algebra in the source has inconsistent argument ordering and signs. In particular, the residual rate bracket displayed around equation (3.13) does not cancel with the preceding derivative identity as printed. The self-financing equation above follows directly from Itô's formula and the stated identities and is the consistent form to implement. Discount factors must likewise remain in discounted withdrawal terms. These are transcription/algebra clarifications, not changes to the model.

## Statistical calibration and the paper's numerical illustration

Section 3.4, printed page 15, uses a stochastic-volatility specification associated with Jacquier, Polson, and Rossi. The logarithm of variance follows an Ornstein–Uhlenbeck process,

$$
d\log\sigma_t^2=(a+b\log\sigma_t^2)dt+c\,dW_t,
$$

whose discrete transition is Gaussian and can be written $\log\sigma_{t+1}^2=\alpha+\beta\log\sigma_t^2+\gamma\varepsilon_{t+1}$. A posterior predictive distribution for integrated variance provides its upper quantiles. The example concerns a one-year at-the-money call with $S_0=K=100$, a known continuously compounded rate of 5%, and initial log variance set at its long-run mean. The lower total-variance bound is zero.

| Predictive coverage | Upper total standard deviation $\sqrt{\Xi^+}$ | Conservative call value |
|---|---:|---:|
| 50% | 0.168 | 9.19 |
| 80% | 0.187 | 9.90 |
| 90% | 0.202 | 10.46 |
| 95% | 0.217 | 11.03 |
| 99% | 0.257 | 12.54 |

The prices are in the same monetary units as the spot and strike. Increasing coverage from 50% to 99% raises the budgeted standard deviation by 8.9 percentage points and the ask by 3.35 units. These are predictive-uncertainty prices, not an estimated option-market bid–ask spread.

The paper does not supply the posterior parameter draws, complete daily sample, exact estimation dates, simulation seed, integration mesh, or quantile Monte Carlo error required to recreate the variance quantiles independently. A reader can reconstruct the pricing transformation from the reported quantiles; reproducing the upstream statistical calibration requires the cited estimation study or new explicitly documented choices. Nor does this example demonstrate realized 95% hedge success in a held-out sample. It illustrates how a predictive distribution would enter the method.

In a new implementation, the parameter estimation window, treatment of parameter uncertainty, initial variance filtering, forecast horizon, and quantile definition all belong in the inference stage. A plug-in predictive distribution conditional on estimated parameters can understate uncertainty relative to one integrating parameter uncertainty; the exact quantile effect depends on the fitted distribution. The paper's framework allows either a frequentist or Bayesian construction but does not make an inaccurate prediction region accurate merely by converting it into a hedge.

## Quadratic variation is observable only in an ideal limit

The conceptual attraction of integrated variance is that it is linked to the realized path:

$$
[\log S]_t=\lim_{\max\Delta t_i\to0}\sum_i(\Delta\log S_{t_i})^2.
$$

The paper discusses a discretely sampled realized-variance approximation with error of order $O_p(\Delta t^{1/2})$, compared with a slower $O_p(\Delta t^{1/4})$ rate for certain spot-volatility estimates. This supports using accumulated variance as the trading state. The orders require the continuous-process and regularity setting; they are not universal guarantees for noisy tick data.

Discretization creates two distinct errors: estimating the variance budget consumed and executing the delta hedge only at discrete times. Bid–ask bounce and market microstructure can make increasing sampling frequency harmful. Neither a noise-robust estimator nor a transaction-cost-aware optimal rebalancing interval is specified. Consequently, a practical reproducer should report the discrete hedge shortfall distribution separately from predictive coverage. It would be incorrect to label an empirically estimated variance interval plus a daily hedge an exact realization of the continuous-time theorem.

Section 2 also describes a backup strategy. Maintain a capital reserve relative to a conservative superhedge; follow a preferred strategy while its discounted deficit to the conservative value stays within the reserve; switch when the deficit reaches the threshold. Under continuity and costless switching, this converts the conservative hedge into an exit mechanism. It does not protect against an unmodeled price jump over the threshold, failed execution, or an already breached prediction set.

## Duality, admissibility, and why the proof needs more than no arbitrage

Sections 4–5 supply the general justification. Let $\mathcal Q_C$ contain admissible martingale measures under which discounted traded assets are martingales and $C$ holds almost surely. Every superhedge must cost at least

$$
\sup_{Q\in\mathcal Q_C}E_Q[\eta/\beta_T].
$$

The difficult direction is showing that a single admissible trading strategy attains, or suitably approaches, this worst-case expectation across the model family. A collection of model-by-model hedges would not suffice if the trader does not observe the true model.

Theorem 5.1 is stated on a canonical continuous-path space, with fixed initial prices, absolutely continuous log bank-account paths, and absolutely continuous quadratic covariations satisfying boundedness restrictions in the construction. The payoff is continuous as a path functional in the specified topology, has a uniform lower bound of the form $-K\beta_T$, and satisfies the necessary expectation bounds. The prediction set must be closed in a measure-compatible sense: weak limits of admissible laws concentrating on the set must still concentrate on it. It also must admit at least one relevant martingale law.

These are substantive conditions. A discontinuous digital payoff or a pathological prediction event is not automatically covered by merely writing down the supremum. Quadratic variation itself is delicate as a function on the continuous-path space. Proposition 5.2 explains how to formulate common prediction events so that their intended quadratic-variation interpretation is valid under the individual laws. The bookkeeping of rate signs and covariance-coordinate dimensions in this draft should not be copied mechanically.

Admissibility excludes doubling strategies and uncontrolled negative wealth. The stochastic-integral gains require predictable integrands and appropriate local square integrability; negative parts must satisfy the paper's uniform-integrability restrictions over stopping times, or suitable lower-bound conditions. In this setting a super-self-financing discounted wealth process is a supermartingale under every relevant martingale measure. Optional decomposition then connects the supermartingale envelope to tradable gains and a nonincreasing withdrawal process.

The proof proceeds by penalizing payoffs outside the prediction region, controlling the relevant families of laws, taking weak limits, and using closedness to keep limiting mass on the prediction set. One then obtains a supermartingale envelope and an admissible decomposition, with the lower credit bound retained. The bounded-coefficient restrictions support compactness arguments before the class is expanded. The result is not an assertion that unrestricted worst-case expectations always have a dynamically attainable hedge.

The inference family $\Theta$ and trading family $\mathcal Q$ need not coincide. A parametric volatility law can yield a prediction interval, after which trading protects all continuous paths within that interval in a larger class. Conditional nesting assumptions connect the future laws from the statistical model with the permissible trading models. Frequentist coverage must hold over the declared parameter class; posterior coverage instead depends on the prior and likelihood. These two guarantees should be labeled separately.

## Interest-rate uncertainty and the value of a traded zero-coupon bond

Section 6 distinguishes knowing a bond price from merely imposing a bound on the future integrated short rate. If only the stock and bank account can be traded, separate intervals for $\int r$ and $\int\sigma^2$ permit considerable adversarial dependence. A point estimate of the discount factor cannot be substituted without changing the opportunity set.

If a zero-coupon bond $\Lambda_t$ maturing at one unit at $T$ is traded, choose it as numeraire. The relevant underlying becomes $F_t=S_t/\Lambda_t$, and the relevant uncertainty is the quadratic variation of $\log F$. Suppose

$$
\Xi^{*,-}\leq[\log(S/\Lambda)]_T\leq\Xi^{*,+}.
$$

For a convex European payoff, the ask becomes $\mathcal B(S_0,-\log\Lambda_0,\Xi^{*,+};f)$. At time $t$, use the residual forward-variance budget and the current bond price. The stock holding is $\mathcal B_S$; the bond holding is the residual wealth divided by $\Lambda_t$, equivalently $-\mathcal B_R/\Lambda_t$. This last minus sign follows from $d(-\log\Lambda)$ and the identity above; the surrounding source prose near equation (6.18) is inconsistent about it.

Stock variance alone is not sufficient when the bond is volatile. The forward variance contains bond variance and stock–bond covariance. The Ornstein–Uhlenbeck interest-rate example in the paper takes independent rate and stock Brownian shocks and discusses a negligible rate-risk adjustment approximation. Then Gaussian integrated-rate uncertainty can be summarized by its mean and variance. This is an illustration under special assumptions, not a justification for omitting rate–equity dependence in general.

For nonconvex payoffs, the robust problem can be expressed as optimal stopping of a unit-volatility geometric Brownian motion. Let $d\widetilde S_u=\widetilde S_udW_u$, with $\widetilde S_0=S_0$, in variance time. With the bond numeraire, maximize $E[\Lambda_0 f(\widetilde S_\tau/\Lambda_0)]$ over stopping times $\tau$ between the lower and upper forward-variance budgets. This resembles an American exercise problem, but the economic claim remains European: stopping represents the adversarial choice of the accumulated variance clock. Convexity puts the optimum at the upper endpoint; concavity reverses that preference. Separate rate and stock-variance intervals lead to an additional scalar minimization over a static bond holding and a maximization over allowable integrated rates.

## Existing options tighten the interval: an implementable two-call construction

Theorem 7.1 gives the general static/dynamic decomposition. If $p$ traded claims with terminal payoffs $f_i$ have current values $V_0^{(i)}$, the augmented ask for $f_0$ is

$$
\inf_{\lambda\in\mathbb R^p}\left\{A_0\left(f_0-\sum_{i=1}^p\lambda_if_i\right)+\sum_{i=1}^p\lambda_iV_0^{(i)}\right\}.
$$

The positions in the auxiliary options are static; the residual is hedged dynamically in the underlying and, where available, the bond. This is more informative than assuming every model in an uncertainty band can ignore already observed option prices. It also makes quote feasibility part of the exercise: incompatible prices and variance limits can imply conditional arbitrage.

For two calls at strikes $K_1<K_2$, a known rate $r$, and a convex target payoff, Algorithm 7.1 is explicit. Work with discounted strikes $K_i'=e^{-rT}K_i$ and the unit-volatility martingale $\widetilde S$. First invert Black–Scholes prices to obtain total implied variances $\Xi_i^{\rm impl}$. If the first is smaller, retain $\Xi_1=\Xi_1^{\rm impl}$ and increase the second stopping threshold $\Xi_2$ until the second call's value matches its observed price when variance time stops at the first hit of $K_1'$ after $\Xi_1$, or at $\Xi_2$, whichever comes first. Reverse the roles if the second implied variance is smaller. Equal implied variances require no threshold adjustment.

The final stopping time is the minimum of $\Xi^+$, the first hit of $K_1'$ after $\Xi_1$, and the first hit of $K_2'$ after $\Xi_2$. Price the target as its discounted payoff expectation at this stopping time. The thresholds satisfy $\Xi_i\geq\Xi_i^{\rm impl}$; conditional no-arbitrage also requires them not to exceed $\Xi^+$. Merely checking that the two raw implied variances lie inside the initial band is not the entire feasibility check.

Equations (7.12)–(7.18) evaluate the intermediate stopped expectations with ordinary and bivariate Gaussian distribution functions, exploiting barrier-option identities. The bivariate correlation is $\sqrt{\Xi/\widetilde\Xi}$ for the two variance times. Alternatively, a numerical implementation can solve the unit-volatility stopping problem, but a naive discrete monitoring grid misses barrier hits and biases the result. The paper cites first-passage simulation corrections; it does not supply a mesh, tolerance, or executable implementation. Root-finding for the second threshold must be combined with stable normal-CDF routines and feasibility checks.

The proof observes that the residual payoff is convex except at the two auxiliary strikes. Away from those kink locations, the martingale has a submartingale payoff and continuation is preferred. The only interior stopping candidates are therefore the strikes, with activation thresholds determined by matching the two quoted prices. The Snell envelope yields the threshold structure and monotonicity gives the calibration solution.

Figures 7.1–7.4 use $S_0=100$, $T=1$, $r=0.05$, traded strikes 100 and 160, initially both with implied standard deviation 0.20. Target strikes include 110, 120, 130, and 140. Figure 7.2 varies the upper total standard deviation over 0.25, 0.40, and 0.50. Interpolated upper prices correspond to much lower implied volatilities than pricing the target directly at the largest permitted variance. As the variance ceiling tends to infinity, the bound approaches the static convexity bound between the two calls. For an intermediate strike $K_0$, its cost is $wV_0^{(1)}+(1-w)V_0^{(2)}$, with $w=(K_2-K_0)/(K_2-K_1)$. Figures 7.3–7.4 raise the second option's implied volatility; the activation threshold rises faster, and the minimum feasible variance ceiling rises with it. These are constructed illustrations, not market estimates.

## What to reproduce and what the method cannot promise

A faithful reproduction has four separable outputs: a documented prediction interval with its coverage interpretation; a continuous-time conservative price and hedge; an auxiliary-option feasibility/calibration calculation if quotes are used; and a discrete execution experiment that measures implementation error. Combining them into one reported backtest return hides which component succeeds or fails.

Section 8 contrasts the decoupled prediction method with restricting trading to the original statistical model and with superhedging over a confidence or credible set of probability laws. The first can be cheaper but inherits more model structure. The second is not generally ordered relative to the prediction-set approach because the corresponding model families need not be nested. Mykland does not establish a universal efficiency ranking.

The strongest practical takeaway is that the uncertainty object should be observable and auditable during the option's life. A cumulative variance budget can be monitored and translated into a changing hedge. Its price is deliberately conservative conditional on a chosen prediction event. The most serious limits are misspecified statistical coverage, discontinuous returns, unavailable continuous trading, noisy variance measurement, and losses outside the event. Existing option quotes can substantially reduce excessive conservatism, but only after ensuring that the quoted contracts, variance restrictions, and rate assumptions are mutually compatible.
