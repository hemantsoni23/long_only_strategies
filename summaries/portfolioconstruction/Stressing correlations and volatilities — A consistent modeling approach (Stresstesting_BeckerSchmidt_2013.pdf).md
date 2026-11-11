# Stressing correlations and volatilities — A consistent modeling approach

**Christoph Becker and Wolfgang M. Schmidt (2013).** *Journal of Empirical Finance* 21, 174–194; available online December 20, 2012. DOI: 10.1016/j.jempfin.2012.12.009. Source: [Stresstesting_BeckerSchmidt_2013.pdf](../../Finance/Stresstesting_BeckerSchmidt_2013.pdf). References below use source equations, tables, appendices, and journal pages.

## Why this matters

A stress scenario that changes each pairwise correlation independently can produce an impossible covariance matrix. Stressing correlations while leaving volatility untouched can also miss the larger part of an equity crisis. This paper constructs volatility and correlation jointly as nonlinear functions of one observable market state: a trailing estimate of market drift. A low historical quantile of that state defines a scenario, and the model supplies a complete positive-definite covariance matrix at that state.

The contribution combines a continuous-time model with memory, a spline parameterization of its Cholesky factor, approximate likelihood estimation, and an observable way to index stress severity. The authors find stressed ten-day VaR about three times a constant-covariance benchmark for a six-stock example and about four times for a twenty-stock example at their 1% setting. Those are model-based scenario comparisons, not validated unconditional loss probabilities or evidence of a universal regulatory multiplier.

## Market state, units, and timing

Daily time is measured in years, with $\Delta t=1/250$. Let $q_{j,k}=\log(S_{j,k}/S_{j,k-1})$ be the daily log return for asset or index $j$. For a trailing window of $n_F$ daily returns, define its sample mean $\bar q_{j,k}$ and unbiased sample variance $s^2_{j,k}$, using divisor $n_F-1$. Equation 11 is conveniently written

$$
F_k=\frac{1}{n}\sum_{j=1}^{n}\left(\frac{\bar q_{j,k}}{\Delta t}+\frac{s^2_{j,k}}{2\Delta t}\right).
$$

The second term adds the diffusion variance correction: under constant geometric-Brownian parameters, mean log return per unit time is $\mu-\sigma^2/2$, so the corrected statistic estimates arithmetic drift. Alternatively, the state is calculated from a single appropriate market index rather than the average of portfolio assets. The principal equity examples use the S&P 500; robustness checks use the Dow Jones Industrials.

This state is an **annualized realized-drift estimate**, not a daily return, cumulative simple return, volatility index, or latent regime probability. Appendix B also considers $\widetilde F$, which omits the half-variance correction and uses only the annualized mean log return.

The memory is estimated by profiling the likelihood over $n_F\in\{2,\ldots,250\}$. Several stock/index pairs show a likelihood peak around 75 business days, which becomes the principal memory choice. This is a fitted sample feature, not a theorem that all markets have a 75-day memory.

When modeling the return from $k-1$ to $k$, the state uses observations through $k-1$. The lag is essential: using today's close to determine today's covariance would introduce future information. A trailing state is observable at a given date, but its fitted mapping and historical quantiles may still use later observations when estimated over a complete sample. Lagging the state alone therefore does not make the reported experiments out of sample.

## Continuous-time model with memory

Let $S_t$ denote the path segment $u\mapsto S(t+u)$ for $u\in[-r,0]$, where $r=n_F\Delta t$ is the memory length. The source's diffusion model is

$$
\frac{dS_i(t)}{S_i(t)}=\mu_i(\theta,S_t)\,dt+\sigma_i(\theta,F(S_t))\,dW_i(t),
\qquad dW_i(t)dW_j(t)=\rho_{ij}(\theta,F(S_t))\,dt.
$$

The dependence on a trailing path makes this a stochastic delay model. Conditional on the path state, the instantaneous covariance is

$$
\Sigma(\theta,x)=D_\sigma(\theta,x)\rho(\theta,x)D_\sigma(\theta,x)=C(\theta,x)C(\theta,x)'.
$$

The market state drives the full covariance, while independent Brownian innovations can be used through the factor $C$. This is a common **state variable**, not a one-factor return model with only one source of stochastic return risk.

Proposition 1 gives sufficient existence and uniqueness-in-law conditions: the drift composed with the exponential map is locally Lipschitz on log-path space with a linear-growth bound; volatility, correlation, and the state composed with the exponential map are locally Lipschitz in their stated domains; volatilities are bounded; and the correlation matrix is positive definite at all relevant parameter/state values. With a strictly positive continuous initial price path, the proposition yields an adapted solution with positive paths and unique distribution. Bounded drifts additionally imply a finite expected supremum of squared prices on finite horizons. The paper refers the complete proofs to Becker–Schmidt (2010); it does not prove every step in this article.

Lemma 1 adds uniform Lipschitz assumptions on the drift and Cholesky terms, including squared terms, together with bounded volatility and the growth condition. It then shows that the conditional correlation of log returns over a shrinking interval converges almost surely to the instantaneous $\rho_{ij}(\theta,F(S_t))$. Consequently, identifying that instantaneous quantity with daily return correlation is an approximation justified as the interval becomes small, not an exact equality at a finite daily interval.

## Parameterizing covariance without invalid pairwise combinations

For each lower-triangular position, use a cubic spline $h_{ij}(x)$ through common, equally spaced state knots $\xi_1,\ldots,\xi_{n_{cov}}$. Each entry has its own values at those knots. Equation 13 defines

$$
C_{ij}(x)=\begin{cases}h_{ij}(x),&i>j,\\h+|h_{ii}(x)|,&i=j,\\0,&i<j,\end{cases}
\qquad h=0.0001.
$$

The absolute value is inside the diagonal construction, and $h$ is added outside it. Thus every diagonal of $C$ is strictly positive. The factor is nonsingular, and $CC'$ is positive definite. Recover asset volatilities and correlations by

$$
\sigma_i(x)=\sqrt{\sum_{a\leq i}C_{ia}(x)^2},\qquad
\rho_{ij}(x)=\frac{\sum_a C_{ia}(x)C_{ja}(x)}{\sigma_i(x)\sigma_j(x)}.
$$

This ensures a jointly coherent matrix rather than a collection of independently fitted bivariate correlations. A positive diagonal floor does not impose an equally large floor on every covariance eigenvalue or ensure favorable conditioning for every fitted parameter vector.

The knots cover the observed state range. The paper does not specify the spline boundary conditions, extrapolation rule, or a globally bounded extension outside that range. These are important both for replicating results and for applying the continuous-time proposition's boundedness assumptions. A cubic spline on an observed interval should not automatically be assumed to satisfy all global conditions when extrapolated.

The primitive number of spline ordinates implied by this construction is $n_{cov}n(n+1)/2$, plus $n$ constant drift parameters when jointly estimated. The printed parameter-count expression $n_{cov}n(n+3)/2$ does not generally equal that count. A reconstruction should allocate parameters from the actual triangular entries and separately identify drifts rather than rely on the printed count.

Because the entries of a Cholesky factor depend on asset ordering, restricting them to a finite spline family can also make fitted approximation behavior order dependent. The source does not report an asset-order sensitivity study. It assumes constant drifts in the empirical work, stating that covariance estimates were insensitive to alternative drift specifications; it does not disclose all those sensitivity estimates.

## Approximate likelihood and estimation procedure

The exact transition density of the delay diffusion is unavailable. Appendix A.1 approximates daily log returns with an Euler Gaussian density. For state $F_{k-1}$, write

$$
a_{i,k}=\left(\mu_i-\tfrac12\Sigma_{ii}(F_{k-1})\right)\Delta t,\qquad
H_k=\Delta t\,\Sigma(F_{k-1}).
$$

Then the approximate conditional density is $q_k\mid\mathcal F_{k-1}\approx N(a_k,H_k)$. Up to constants, its log likelihood is

$$
\ell(\theta)=-\frac12\sum_{k=1+n_F}^{N}\left\{\log\det H_k+(q_k-a_k)'H_k^{-1}(q_k-a_k)\right\}.
$$

This is an approximation to the continuous-time likelihood. A long sample does not by itself remove a finite daily-discretization error. The authors explicitly acknowledge potentially severe Euler bias at large step sizes.

To reduce matrix-inversion cost, equation A.5 maximizes the sum of all bivariate Gaussian log likelihoods. Each pair uses the appropriate two-dimensional mean and covariance submatrix **from the single joint parameterization**. Pair likelihoods are not fitted independently and later pasted into a correlation matrix. Shared parameters and the Cholesky construction maintain joint validity.

The source describes a reduction from cubic to quadratic matrix-dimension scaling in likelihood evaluation. That is not a guarantee that the entire optimization, whose parameter count also grows quadratically, has a fixed quadratic runtime. It additionally recommends fitting nested subportfolios of 2, 3, 4, … assets and using earlier parameter estimates to initialize the next larger fit.

For each candidate memory, profile the joint composite objective over the spline and drift parameters, then choose the memory with the largest maximized objective. The exact optimization algorithm, starts, convergence tolerances, numerical derivative conventions, and treatment of different numbers of available observations across memories are not reported. Holding the evaluation sample fixed across memory candidates is a sensible reconstruction choice, but it is not an explicitly documented implementation detail of the published study.

Appendix A.2 sketches confidence intervals for the Gaussian likelihood formulation. Individual conditional scores have conditional mean zero under the stipulated model; their sum is a martingale. A Taylor expansion around the estimator, a martingale central limit theorem, and suitable information convergence produce an asymptotically normal estimator. Technical conditions are omitted and a full proof is expressly outside the article's scope. These results should not be represented as a fully proved confidence theory for every fitted composite likelihood, selected memory, and exact delay diffusion. Composite-likelihood uncertainty generally requires attention to cross-pair score dependence rather than blindly using an ordinary likelihood Hessian.

Table A.7 supplies a concrete two-asset parameter example, Colgate–Exxon, January 1990–November 2010, with four annualized state knots −0.996, −0.412, 0.171, and 0.754. Spline ordinates, expressed as decimals rather than the table's percentages, are:

| Entry | Knot 1 | Knot 2 | Knot 3 | Knot 4 |
|---|---:|---:|---:|---:|
| $h_{11}$ | 0.500 | 0.329 | 0.222 | 0.255 |
| $h_{21}$ | 0.655 | 0.123 | 0.039 | 0.0546 |
| $h_{22}$ | 0.545 | 0.297 | 0.197 | 0.211 |

These are Cholesky spline parameters, not directly three volatilities or pair correlations. At the first knot, for example, $h_{11}$ has a reported 95% interval of 0.424–0.577 and $h_{21}$ 0.519–0.791. The displayed confidence bands are fitted parameter/function uncertainty, not prediction intervals for future returns.

## Simulation check of estimation

Appendix A.1 simulates four assets for twenty years, with 75-day memory, constant drifts 0.1, and eight spline discretization points for re-estimation. It generates daily prices using an Euler scheme with **2,000 additional substeps per day** to reduce simulation discretization bias. The prescribed factor functions are

$$
C_{ij}(x)=\frac{2}{\pi}\arctan\{\sin(i+j)+0.9x\},\quad i>j,
$$

$$
C_{ii}(x)=0.001+\left|\frac{2}{\pi}\arctan\sqrt{|2i+0.9x|}\right|,
\qquad C_{ij}(x)=0\quad(i<j).
$$

The simulation's diagonal floor 0.001 differs from the fitted parameterization's stated $h=0.0001$; it should not be silently equated with it. Figures A.8–A.9 visually show recovery of prescribed dependence curves and the 75-day memory. No distribution over repeated simulation errors, coverage frequencies, random seed, or full initialization history is supplied. This is a useful numerical example, not a general finite-sample unbiasedness result.

## Stress scenarios and VaR calculation

After fitting the model, obtain the empirical lower $\alpha$ quantile $f_\alpha$ of historical state observations and evaluate $\Sigma(f_\alpha)$. This simultaneously changes volatilities and correlations while maintaining positive definiteness. It is a conditional scenario indexed by the historical frequency of a low drift state. An estimated empirical quantile is not a proof that the future state distribution is stationary or that the scenario has an exactly known probability.

For portfolio weights $\gamma$, annualized conditional variance is $v_\alpha=\gamma'\Sigma(f_\alpha)\gamma$. For initial value $V_0=\$100$, the paper computes the following ten-day loss quantity:

$$
\operatorname{VaR}^{stress}_\alpha=V_0\left[1-\exp\left\{\Phi^{-1}(\alpha)\sqrt{\frac{10}{250}}\sqrt{v_\alpha}\right\}\right].
$$

The constant-covariance comparator substitutes a separately estimated constant $\Sigma^{const}$. Portfolio weights are equal in the scenario examples. The formula omits drift and freezes the selected covariance for the horizon. It is not an exact simulation of the delay diffusion with an evolving market state. Nor is a weighted sum of arbitrary lognormal asset prices automatically a single lognormal portfolio. This is the article's variance-based lognormal-style VaR approximation.

The same $\alpha$ selects both the stress-state quantile and the conditional return quantile. These are conceptually different probabilities. Their joint occurrence cannot be assigned probability $\alpha$ or $\alpha^2$ without specifying the relevant joint process. The result should be labeled a stressed conditional loss scenario rather than an unconditional calibrated VaR forecast.

### Six-stock example

Tables 1–2 use January 2004–November 2010 data, with 75-day S&P memory. Annualized volatilities at the median and the 5% stress state are:

| Asset | Median state | 5% stress state |
|---|---:|---:|
| Microsoft | 19.6% | 51.7% |
| Walmart | 16.8% | 30.5% |
| General Electric | 20.1% | 60.5% |
| Pfizer | 21.2% | 34.6% |
| Exxon | 20.2% | 40.7% |
| Bank of America | 28.5% | 135.6% |

Many correlations rise: Microsoft–Exxon from 33.2% to 62.0%, Pfizer–Exxon from 29.9% to 63.3%, and Microsoft–Bank of America from 23.9% to 58.3%. But not all do: Walmart–Bank of America falls from 37.4% to 13.6%, and GE–Bank of America from 70.7% to 54.7%. Thus consistency means a jointly valid state-dependent matrix, not a rule that every correlation must increase in a crisis. The stressed table also prints Walmart–GE as 41.0% in one direction and 41.1% in the other, a minor rounded-table asymmetry; the fitted covariance model itself is symmetric.

Figure 3 reports a stressed-to-constant VaR ratio near three at the 1% setting. The median-state table is not the constant-model denominator, so it cannot be used interchangeably with that denominator. Figure 4 gives a ratio near four for twenty stocks: Apple, American Express, AT&T, Bank of America, Boeing, Chevron, Citigroup, Coca-Cola, Exxon, Ford, GE, JPMorgan, Johnson & Johnson, McDonald's, Merck, Microsoft, Pfizer, Procter & Gamble, Walmart, and Walt Disney. Exact fitted parameters for these larger examples are not provided.

## Comparison of covariance models using portfolios

Section 6 compares the state model with mean-reverting DCC-GARCH, a constant covariance, and 30- and 90-day moving averages. Ten large US stocks define all $\binom{10}{4}=210$ four-stock subsets: AT&T, Coca-Cola, Exxon, Ford, GE, Johnson & Johnson, Microsoft, JPMorgan, Procter & Gamble, and Walmart.

For a predicted daily covariance $H_k$ and a fixed vector $\mu$ of assumed expected excess returns, weights solve

$$
\min_w w'H_kw\quad\text{subject to}\quad w'\mu=\mu_0,
\qquad
w_k=\frac{H_k^{-1}\mu}{\mu'H_k^{-1}\mu}\mu_0.
$$

There is no stated long-only, gross-exposure, or full-investment constraint. Residual capital $1-\mathbf1'w$ is invested in or borrowed at the risk-free rate. With $\mu=\mathbf1$, the constraint fixes risky-asset weight sum to $\mu_0$ and corresponds to a scaled minimum-variance strategy. With $\mu=(1,0,0,0)'$, the first stock is held for the assumed return and the others serve as hedges. These vectors are evaluation devices, not estimated alpha forecasts.

The comparison uses January 1997–January 2004 and January 2004–November 2010. The models are estimated on the respective datasets and evaluated by realized portfolio volatility within those periods. There is no documented independent chronological holdout, rolling refit schedule, or trading-cost adjustment. A footnote notes that the comparator models use simple returns because the weighted portfolio-return formula is exact for simple returns; the state model originates in log returns. That distinction deserves preservation in replication.

| Period and strategy | DCC | Constant | 30-day average | 90-day average | State model |
|---|---:|---:|---:|---:|---:|
| 1997–2004 minimum variance | 22.0% | 22.3% | 23.1% | 22.2% | 21.9% |
| 1997–2004 hedge | 29.0% | 29.1% | 30.7% | 29.4% | 28.9% |
| 2004–2010 minimum variance | 17.5% | 17.3% | 17.8% | 17.3% | 16.6% |
| 2004–2010 hedge | 18.4% | 18.3% | 19.3% | 18.4% | 17.9% |

These are annualized realized volatilities averaged across subsets. The state model beats DCC in 67.1% of minimum-variance subsets and 74.8% of hedge subsets in the first period; corresponding later-period proportions are 94.8% and 98.6%. Overlapping subsets share most stocks and historical observations, so these win proportions are not 210 independent tests. No standard errors for average differences or costs of the unconstrained hedges are supplied. The numerical advantage is especially small in the first period, about 0.1 percentage point relative to DCC in each strategy.

## Robustness, interpretation, and remaining inputs

Appendix B varies spline knots from four to eight. The six-stock stressed loss at 1% ranges from \$26.9 to \$31.0 per \$100; at 5% it ranges from \$14.0 to \$18.2. This supports broad stability of a large stress effect, not numerical invariance. At 1%, changing memory among 30, 60, 75, 90, 120, and 250 days, using corrected or uncorrected drift and S&P or Dow Jones, gives ratios from 2.53 to 3.17. The effect is smaller at less severe settings: the full reported 10% range is 1.17–1.69.

The authors acknowledge that AIC and BIC strongly favor multivariate GARCH for general covariance dynamics. Their argument favors an interpretable state for stress scenario design, not universally superior statistical fit. Figures 5–6 compare fitted volatility to **DCC estimates used as a proxy**, not observable true volatility. A latent Ornstein–Uhlenbeck factor improves some fit, but the paper's conclusion that it adds little during severe stress rests on selected graphical examples. A full latent-factor specification, MCMC implementation, and formal severe-state test are not supplied.

A faithful reconstruction still needs exact price series and adjustment conventions, trading calendars, knot boundary rules, optimizer settings, empirical-quantile conventions, full fitted parameters, DCC implementation details, risk-free returns, return-target normalization, portfolio ordering, and evaluation/rebalancing conventions. No source code or complete data package accompanies the supplied PDF. The asymptotic and simulation discussions do not fill those empirical gaps.

The principal usable idea is to map an observable stress state into a complete covariance matrix through a common parameterization, keeping scenario severity and matrix validity explicit. The quantitative findings show how much a constant full-sample covariance can understate this model's severe-state loss estimate. They do not establish future coverage of the reported VaR, eliminate idiosyncratic or liquidity risk, or demonstrate an implementable net-of-cost portfolio advantage outside the estimation samples.
