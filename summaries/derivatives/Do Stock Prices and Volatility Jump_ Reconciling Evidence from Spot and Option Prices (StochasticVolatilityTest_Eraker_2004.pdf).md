# Do Stock Prices and Volatility Jump? Reconciling Evidence from Spot and Option Prices

Bjørn Eraker, *The Journal of Finance* 59(3), June 2004, pp. 1367–1403. The local PDF has 38 pages; printed p. 1367 is PDF p. 1. References occupy the last substantive pages; no technical appendix is included.

Source: [StochasticVolatilityTest_Eraker_2004.pdf](../../Finance/StochasticVolatilityTest_Eraker_2004.pdf).

## Why this matters

An option model can fit an implied-volatility surface while implying implausible dynamics for the underlying index or latent variance. Conversely, a return model can explain large historical moves while pricing options badly. Eraker asks whether one parameterized stochastic system can explain both markets simultaneously. Joint estimation is valuable because option prices contain information about current variance and risk-neutral distributions, while underlying returns identify physical dynamics and the difference between physical and pricing measures.

The main empirical distinction is between adding price jumps and adding simultaneous price-and-variance jumps. A price jump alone can explain an isolated crash, but it does not automatically explain why uncertainty and option prices rise sharply on that date. Positive variance jumps allow the system to enter a temporarily high-risk state. State-dependent jump intensity further allows jumps to become more frequent in those states.

The result is qualified. Complex jump specifications barely improve the in-sample average dollar option-pricing error, but substantially improve the time-series residuals. They still fail to explain the rapid decline in variance after the October 1987 peak. Out-of-sample pricing exposes sensitivity to the long-run variance inferred from a short, unusually volatile estimation period. The paper therefore offers a joint diagnostic framework, not a claim that its most elaborate model is structurally correct or uniformly best.

## State variables and nested specifications

Section I models the index level $S_t$ and a nonnegative state $V_t$. Despite the paper's frequent use of the word volatility for $V_t$, the diffusion coefficient is $\sqrt{V_t}$, so $V_t$ has variance units. Under the physical measure $P$, equations (1)–(2) are written

$$
\frac{dS_t}{S_t}=a\,dt+\sqrt{V_t}\,dW_t^S+dJ_t^S,
\qquad
dV_t=\kappa(\theta-V_t)dt+\sigma_V\sqrt{V_t}\,dW_t^V+dJ_t^V,
$$

with $d\langle W^S,W^V\rangle_t=\rho\,dt$. Here $\kappa$ is a mean-reversion coefficient, $\theta$ the mean-reversion target of the diffusion part, $\sigma_V$ the variance diffusion loading, and $a$ the return drift coefficient. With uncompensated jumps, $a$ alone is not the total expected instantaneous arithmetic return. Likewise, $\theta$ need not equal the unconditional mean of $V$ once positive variance jumps are added.

The four specifications impose the following restrictions:

| Model | Price jumps | Variance jumps | Arrival intensity |
|---|---|---|---|
| SV | None | None | Zero |
| SVJ | Normal jump-size law | None | Constant $\lambda_0$ |
| SVCJ | Conditional normal law correlated with variance jump | Positive exponential jump | Constant $\lambda_0$ |
| SVSCJ | Same correlated jump law | Same positive jump law | $\lambda_0+\lambda_1V_t$ |

SV is the Heston square-root variance model. Negative $\rho$ associates downward diffusive price moves with upward variance moves and generates return-distribution asymmetry. SVJ adds a rare tail component with jump-size mean $\mu_y$ and standard deviation $\sigma_y$. Unlike leverage in the diffusion, an isolated SVJ price jump has no direct effect on the variance state.

SVCJ uses a common jump clock and

$$
Z_t^V\sim\operatorname{Exponential}(\text{mean }\mu_V),
\qquad
Z_t^S\mid Z_t^V\sim N(\mu_y+\rho_JZ_t^V,\sigma_y^2).
$$

$\rho_J$ is a regression loading with units, not a correlation coefficient constrained to $[-1,1]$. A negative loading links a larger positive variance jump with a more negative price jump. The unconditional price-jump mean is $\mu_y+\rho_J\mu_V$, so the table's $\mu_y$ is not generally the full mean jump. Its unconditional variance also includes $\rho_J^2\mu_V^2$.

SVSCJ makes the common jump intensity affine in variance. Nonnegative intensity over the state space requires suitable parameter restrictions, conventionally nonnegative $\lambda_0$ and $\lambda_1$. The model counters a feature of constant-intensity specifications: when diffusive variance becomes high, a fixed rare-jump component becomes relatively less important. Increasing jump intensity with variance can preserve strong short-maturity skewness in stressed conditions.

There is an important specification ambiguity in the article's notation. It writes normal jumps directly in $dS/S$, while referring to the affine transform of log prices and estimating log-return innovations. Exact proportional arithmetic jumps and normal log jumps are different: under log jumps $Y$, the proportional price change is $e^Y-1$. A production implementation must choose and document one convention, including its compensator and likelihood. The article's shorthand alone does not justify substituting the two globally, especially for crash-sized jumps.

## Physical versus pricing measures

Equations (7)–(9) keep the diffusion loading and jump-law structure but change the pricing drift and the conditional mean of price jumps. A call price is the discounted $Q$-expectation of its payoff. The displayed variance drift under $Q$ is

$$
\kappa(\theta-V_t)+\eta_VV_t
=\kappa\theta-\kappa^QV_t,
\qquad \kappa^Q=\kappa-\eta_V.
$$

Thus $\eta_V$ parameterizes a volatility-risk premium, and $\mu_y^Q$ replaces $\mu_y$ in the conditional price-jump law. The article does not estimate an unrestricted risk-neutral distribution for every jump parameter: it concentrates the price-jump premium in this mean shift.

Two source inconsistencies need explicit treatment. First, the prose on p. 1374 defines $\eta_J=\mu_y^Q-\mu_y$, but Table III reports its opposite. For SVCJ, $\mu_y=-6.062$ and $\mu_y^Q=-7.508$, while reported $\eta_J=+1.446$. This note reports the table's positive premium as the physical-minus-risk-neutral mean difference and retains the two underlying means so the sign convention is unambiguous.

Second, later discussion describes a change in mean-reversion speed with no effect on long-run variance, including a risk-premium effect that vanishes at very long maturity. That does not follow from equation (8) as printed: even without jumps its stationary mean is $\kappa\theta/\kappa^Q$. With constant positive variance jumps, the corresponding mean is $(\kappa\theta+\lambda_0\mu_V)/\kappa^Q$. Holding the stationary mean fixed while changing speed would require changing the intercept too. The numerical pricing implementation is not supplied, so the exact convention behind that discussion cannot be resolved from this PDF.

For state-dependent positive jumps, the physical mean equation provides another useful implementation check:

$$
\frac{dE[V_t]}{dt}=\kappa\theta+\lambda_0\mu_V-(\kappa-\lambda_1\mu_V)E[V_t].
$$

This identity follows directly from the specified intensity and exponential jump mean. A finite stationary first moment requires $\kappa>\lambda_1\mu_V$ in consistent units. Under the printed pricing drift, replace $\kappa$ in the decay coefficient by $\kappa^Q$. These are model-derived checks, not additional empirical estimates reported in the paper.

## Pricing computation and what can be reconstructed

The paper obtains option prices by numerical Fourier inversion of an exponential-affine transform,

$$
E^Q[e^{u\log S_{t+\tau}}\mid S_t,V_t]
=\exp\{A(u,\tau)+B(u,\tau)V_t+u\log S_t\}.
$$

The coefficient equations and closed expressions are delegated to Duffie–Pan–Singleton and related work. The current PDF does not provide integration cutoffs, tolerances, complex-root conventions, or the actual pricing code. It emphasizes computational efficiency because option prices are recomputed repeatedly within MCMC.

A self-contained implementation can reconstruct the transform after resolving the jump convention. The following is a derivation for the **normal-log-jump interpretation**, rather than a claim that these exact formulas are printed in Eraker. For a joint log-price jump $Y$ and variance jump $Z$, the transform is

$$
M(u,b)=E[e^{uY+bZ}]
=\frac{\exp(u\mu_y^Q+\tfrac12u^2\sigma_y^2)}{1-\mu_V(b+u\rho_J)},
$$

where the moment exists. Let $k_J=M(1,0)-1$ and $G(u,b)=M(u,b)-1-uk_J$. With the proportional price jump $e^Y-1$ and compensator $(\lambda_0+\lambda_1V)k_J$, the generator gives

$$
\partial_\tau A=ur+\kappa\theta B+\lambda_0G(u,B),
$$

$$
\partial_\tau B=\tfrac12(u^2-u)+(\rho\sigma_Vu-\kappa^Q)B+\tfrac12\sigma_V^2B^2+\lambda_1G(u,B),
\qquad A(u,0)=B(u,0)=0.
$$

Set jump terms to zero for SV, set $\mu_V=0$ and remove variance-jump loading for SVJ, and set $\lambda_1=0$ for SVCJ. A dividend yield changes the return drift appropriately. All quantities must first be converted to one consistent return and time unit; the empirical table mixes conventions discussed below.

Given the transform $\Phi(u)$, standard Fourier tail probabilities can be constructed from $\Phi(iu)$ and $\Phi(1+iu)/\Phi(1)$, and the European call follows as spot times the share-measure exercise probability minus discounted strike times the ordinary exercise probability. Verify $\Phi(0)=1$ and the discounted stock martingale condition at $u=1$ before comparing prices. Numerical quadrature convergence and recovery of the no-jump limit are essential checks. This reconstruction makes the method implementable under an explicit convention while preserving the unresolved differences from the published shorthand.

## Observation model and joint posterior

Section II treats option prices as noisy observations of the latent state. For contract $j$,

$$
Y_{t,j}=F(S_t,V_t,\chi_{t,j},\Theta)+\varepsilon_{t,j},
\qquad
\varepsilon_{t,j}=\rho_j\varepsilon_{t-1,j}+u_{t,j},
\qquad u_{t,j}\sim N(0,s_j^2).
$$

$\chi$ includes strike, maturity, and other known pricing inputs. Pricing errors are measured in dollars and are serially dependent within a contract, but independent across contracts. This restriction prevents an unrestricted common pricing-error factor from competing with the latent variance state for cross-sectional price movements. It is a substantive identification restriction, not merely a numerical convenience.

The article also discusses unequal observation times and an Ornstein–Uhlenbeck error model, although the empirical data are daily closing observations. Equation (11) prints a transition variance inconsistent with its stated negative mean-reversion parameter. For $d\varepsilon=\rho_j\varepsilon dt+s_jdW$ and $\rho_j<0$, the correct OU variance over $\Delta$ is $s_j^2(e^{2\rho_j\Delta}-1)/(2\rho_j)$, with conditional mean $e^{\rho_j\Delta}\varepsilon_{\mathrm{previous}}$. The printed expression uses $1-e^{-2\rho_j\Delta}$ instead. An implementation should derive the transition from the stated SDE rather than copy that sign pattern.

The posterior combines the option observation likelihood, underlying/variance transition densities, jump probabilities, jump-size distributions, and parameter priors. Schematic notation is

$$
p(\Theta,V,J,Z\mid S,Y)\propto p(\Theta)p(V_0)
\prod_t p(S_t,V_t\mid S_{t-1},V_{t-1},J_t,Z_t,\Theta)
 p(J_t\mid V_{t-1},\Theta)p(Z_t\mid J_t,\Theta)
\prod_{t,j}p(Y_{t,j}\mid V,\Theta,Y_{\mathrm{previous},j}).
$$

The full transition density would require a two-dimensional inversion. Instead, the paper uses a Gaussian Euler transition conditional on jumps. Over interval $\Delta$, the diffusion covariance of log-price and variance innovations is approximately

$$
V_{t-1}\Delta
\begin{pmatrix}1&\rho\sigma_V\\\rho\sigma_V&\sigma_V^2\end{pmatrix}.
$$

The drift must be transformed consistently if coding log prices instead of proportional price increments. A binary jump indicator approximates rare arrivals within an interval; state-dependent probabilities use the preceding variance. At the estimated low daily rates, multiple arrivals are rare, but the binary approximation is not the exact continuous-time Poisson law. Larger gaps require either finer latent-time augmentation or explicit attention to approximation error.

## MCMC procedure and replication gaps

The sampler alternates latent variances, jump indicators, jump sizes, structural parameters, and pricing-error parameters. A variance update uses a Metropolis step because the nonlinear option likelihood makes its conditional posterior nonstandard. The Markov transition part depends on its neighboring states. Jump indicators are sampled by comparing the transition likelihood under jump/no jump, multiplied by the corresponding prior probability and jump-size density. Given the state path, option prices do not depend directly on the realized historical jump indicators or sizes, so those updates exploit the same conditional structure as the returns-only model.

Jump-size updates use conditional distributions described in the cited Eraker–Johannes–Polson paper, including truncation for the positive variance jump. Structural parameters are proposed jointly from a normal proposal centered on the current vector, with covariance estimated in a preliminary run. Joint proposals account for highly correlated parameters and reduce repeated full repricing compared with updating every parameter separately. For equally spaced errors, familiar Gaussian and gamma conditional forms can be used under the appropriate priors; irregular times require Metropolis corrections.

Equation (14)'s compact variance conditional requires care in an implementation with serially correlated option errors. Changing $V_t$ changes the residual for every option observed at $t$, and therefore the conditional likelihood of that contract's next observation as well. Those successor-error factors must be included in an exact conditional, even though the printed expression displays only the current option likelihood and adjacent state transitions. In SVSCJ, changing $V_t$ also affects the next interval's jump probability. Evaluating all dependent factors in the full joint posterior avoids both omissions.

The paper emphasizes the need for proper priors on weakly identified jump means. With very few jump dates, an improper prior can produce an improper posterior. However, this PDF does not enumerate all prior distributions and hyperparameters, chain lengths, burn-in, proposal scaling, acceptance rates, multiple-chain diagnostics, effective sample sizes, positivity treatment, or initial-state priors. It also does not supply the preliminary-run covariance matrix. These are material missing replication inputs. They should be reported by a reproducing researcher, not guessed and presented as the author's settings.

Historical MCMC draws are conditional on the full estimation dataset. They are smoothing draws even when called filtered volatility in the tables. Out-of-sample pricing uses a separate particle-filtering exercise with information only through the preceding day. Confusing those two information sets would create look-ahead bias.

## Data, filtering, and evaluation design

Section III uses CBOE daily closing S&P 500 option prices. To mitigate nonsynchronous option and index closes, the underlying value is backed out through put–call parity, following the cited data study. Observations with option prices below \$1 are excluded because quote discreteness has an outsized relative effect. Bid–ask spreads are unavailable, so the study cannot directly establish that reported mispricing is tradable after spreads and execution costs.

The estimation period is January 1, 1987–December 31, 1990: 1,006 trading days, including the October 1987 crash. The full option database for that period has about 22,500 prices. Computational cost motivates a subsample: randomly choose a contract trading on the first day, retain its recorded observations, and when it is no longer trading choose another available contract, repeating to maintain coverage. The resulting panel contains 3,270 call price observations, not 3,270 independent time-series paths. Table V's counts establish that observation total. The description permits varying cross-sectional size, but does not provide the random seed, selected contract identifiers, or a fully enumerated sampling ledger.

Table I gives estimation-sample mean strike/spot 0.98, mean maturity 50.33 days, mean price \$10.4833, and mean implied volatility 20.2%. Corresponding standard deviations are 0.05, 37.60 days, \$7.425, and 7.8 percentage points. Out-of-sample means are 0.99, 45.91 days, \$17.88, and 14%, with standard deviations 0.06, 44.27 days, \$23.13, and 6 percentage points. Table I's first-period label says 1987–1991, while the explicitly stated estimation endpoint is December 1990; the latter controls the timing interpretation here.

The evaluation period is January 1, 1991–March 1, 1996. Section III says 36,890 observations, but Section IV.C and Table VI give **35,890**, and the table's maturity and moneyness counts sum to that number. This note uses the internally tabulated count and flags the discrepancy. Structural parameters remain fixed at estimation-period values. Each evaluation day's variance estimate uses information available through $t-1$, according to both the text and Figure 3 caption; same-day option prices must not be used to recalibrate it.

The particle count, proposal mechanism, resampling rule, initialization, return/option update sequence, and variance-point-estimate convention are not reported. Neither are complete interest-rate/dividend inputs, put–call matching rules, maturity day-count conventions, all arbitrage filters, or handling of missing closes. These limit exact replication of the quoted errors.

A separate returns-only benchmark uses 5,307 S&P 500 observations from January 1970–December 1990. It estimates physical parameters with the earlier MCMC method and prices options under simplifying risk-premium assumptions. It is not a clean experiment varying only the inclusion of options: its return history is much longer than the joint-estimation sample.

## Estimated parameters and unit checks

Table III uses daily time and returns scaled by 100. Selected posterior means are:

| Parameter | SV | SVJ | SVCJ | SVSCJ |
|---|---:|---:|---:|---:|
| $\theta$ | 1.933 | 1.652 | 1.353 | 0.943 |
| $\kappa$ | 0.019 | 0.019 | 0.023 | 0.023 |
| $\kappa^Q$ | 0.009 | 0.011 | 0.011 | 0.006 |
| $\eta_V$ | 0.010 | 0.009 | 0.013 | 0.017 |
| $\rho$ | −0.569 | −0.586 | −0.582 | −0.542 |
| $\sigma_V$ | 0.220 | 0.203 | 0.163 | 0.137 |
| $\lambda_0$ | — | 0.002 | 0.002 | 0.002 |

In SV, $\sqrt{252\theta}$ is about 22% annualized volatility. With variance jumps that conversion of $\theta$ alone omits their contribution to mean variance. For SVCJ, the reported $\mu_V=1.638$, $\rho_J=-0.693$, $\sigma_y=3.630$, $\mu_y=-6.062$, and $\mu_y^Q=-7.508$ describe the jump law. The respective posterior standard deviations are 0.790, 0.096, 1.106, 2.274, and 0.932.

The jump rate of about 0.002 per trading day means roughly two arrivals per 1,000 days, or about 0.5 per 252-day year. Such rare events explain why option data do not precisely identify physical jump means: current option prices depend on the pricing-measure mean, whereas the physical mean is informed by few historical latent jump realizations.

The state-dependent coefficient requires a special unit warning. Table III prints $\lambda_1=1.298$ while its caption says returns are multiplied by 100. Substituting percent-squared variance $V=9$ for a 3% daily standard deviation would imply an absurd daily intensity above 11. The text instead says intensity is about 0.003. That statement is consistent with $0.002+1.298(0.03)^2\approx0.00317$, meaning decimal-return variance for this coefficient, or an effective coefficient $1.298\times10^{-4}$ when variance is in percent-squared units. The conversion is an inference from the numerical example; it is not clearly labeled in the table.

Reported uncertainty is posterior uncertainty, not a frequentist standard error. For SVSCJ, $\eta_V$ has posterior mean 0.017, standard deviation 0.007, and printed interval [0.003, 0.033]. Its table-sign jump premium has mean 6.367, standard deviation 0.842, and interval [4.472, 8.117]. The analogous SVJ and SVCJ jump-premium intervals include zero. The article calls intervals 99% credible intervals but the surrounding description identifies 1st and 99th percentiles, which span 98% probability; one should preserve their stated endpoints without assuming the coverage label is exact.

Returns-only estimates are smaller in variance-of-variance: $\sigma_V=0.108$, 0.079, and 0.058 for SV, SVJ, and SVCJ, compared with 0.220, 0.203, and 0.163 jointly. Sample differences and information differences both matter. The returns-only SVCJ jump loading is 0.312 with standard deviation 1.459, far less precisely determined than the joint estimate of −0.693.

## Option-pricing results

Table V's mean absolute errors are in dollars and are averaged across posterior draws; they are not minima of a daily least-squares calibration. Across all 3,270 estimation observations, SV, SVJ, SVCJ, and SVSCJ have errors of \$0.47, \$0.47, \$0.46, and \$0.46. Extra jump flexibility therefore contributes only about a cent in the rounded aggregate table.

The short-maturity category shows a larger distinction: below one month, errors are \$0.42, \$0.42, \$0.39, and \$0.36. At one to two months the most complex model is worse, with \$0.51 versus SV's \$0.48. Beyond six months the values are \$0.56, \$0.58, \$0.55, and \$0.52. Figure 2 shows broadly similar implied-volatility curves, with residual problems in short and medium maturities under high or average spot variance, and long maturities under low spot variance.

The error denomination matters. Dollar errors weight contracts differently from relative-price or implied-volatility errors. The paper argues that quote discreteness and approximately similar dollar errors across maturity/moneyness cells support its choice, but acknowledges that model rankings could change under a different correctly specified error likelihood. Merely changing the plotted evaluation metric is not equivalent to re-estimating with a different likelihood and heteroskedasticity structure.

Out-of-sample Table VI gives:

| Maturity | SV | SVJ | SVCJ | SVSCJ |
|---|---:|---:|---:|---:|
| Less than 1 month | 0.32 | 0.34 | 0.33 | 0.45 |
| 1–2 months | 0.46 | 0.45 | 0.43 | 0.55 |
| 2–3 months | 0.40 | 0.40 | 0.43 | 0.58 |
| 3–6 months | 0.67 | 0.84 | 1.06 | 0.50 |
| More than 6 months | 2.10 | 2.36 | 2.84 | 0.50 |
| All | 0.56 | 0.61 | 0.67 | 0.51 |

All entries are dollars per quoted option price unit. The prose accidentally calls values such as 0.51 “cents”; the table's dollar label is decisive. SVSCJ's aggregate advantage is driven particularly by longer maturities. It is worse in all three shortest maturity groups, so an unqualified statement that it prices options best would obscure the central tradeoff.

Long-run variance estimated during 1987–1990 is too high for the quieter evaluation period. The latter's annualized realized volatility is 15.3%, with spot/implied volatility occasionally around 5–7%. The smaller $\kappa^Q$ in SVSCJ reduces the pull toward the high estimated long-run level over the maturities studied. Figure 3 shows errors for longer contracts growing as the evaluation period progresses.

As a diagnostic, adjusting the long-run level to match historical 15% volatility reduces SVCJ's aggregate error to \$0.36 and its below-one-month error to \$0.22. The detailed supplementary results are not in this PDF. The author explicitly treats such adjustments as model diagnostics rather than a valid unchanged-parameter structural forecasting exercise. No data-driven live recalibration rule is established by that experiment.

Returns-only parameter estimates produce Table VII aggregate errors of \$0.58, \$0.46, and \$0.54 for SV, SVJ, and SVCJ. They improve the two jump models relative to their unadjusted joint-estimation errors, but not SV, whose joint error is \$0.56. For short maturities the returns-only errors are \$0.34, \$0.25, and \$0.28. Neither these comparisons nor the adjusted-level diagnostic establishes a cost-adjusted option strategy; transaction costs, hedge P&L, and executable quotes are not tested.

## Time-series residuals and remaining misspecification

The latent path is checked against its own diffusion loading. Table VIII forms residual variance increments after removing drift and inferred jumps and dividing by $\sqrt{V_{t-1}}$. Their dispersion should match $\sigma_V$. The reported values are 0.202, 0.198, 0.151, and 0.134, with posterior standard deviations 0.005, 0.004, 0.005, and 0.007. These are broadly near Table III's loading estimates, although not literally equal.

The table caption calls the calculation a mean squared error while reporting values on the standard-deviation scale. To compare with $\sigma_V$, take the square root of the mean squared standardized increment; comparing the unrooted mean square with $\sigma_V$ would be dimensionally wrong. This diagnostic uses full posterior path draws. A posterior-mean path is smoother and can spuriously suggest too little variance-of-variance.

The decisive residual comparison is Table IX:

| Statistic | SV | SVJ | SVCJ | SVSCJ |
|---|---:|---:|---:|---:|
| Return residual skewness | −1.891 | −0.692 | −0.129 | 0.138 |
| Return residual kurtosis | 20.352 | 7.223 | 3.959 | 3.757 |
| Variance residual skewness | 2.487 | 2.045 | −0.300 | −0.446 |
| Variance residual kurtosis | 27.758 | 19.256 | 6.017 | 5.616 |

These are ordinary kurtosis values, whose Gaussian benchmark is 3. Correlated jumps greatly reduce the return-tail mismatch and the huge positive variance residual associated with October 1987. SV and SVJ need variance shocks around ten standard deviations to explain that episode. Simultaneous jumps are more readily recognized because both index and option-implied variance move sharply on the same date.

Yet volatility-jump models cannot generate negative variance jumps. The rapid post-crash decline must be assigned to diffusion or mean reversion, leaving large negative residuals. SVCJ's return-kurtosis interval is [3.563, 4.620] and its variance-kurtosis interval [4.337, 7.700]; both remain above 3 at their printed lower endpoints. The more elaborate models improve fit without passing a claim of exactly Gaussian innovations.

These are posterior summaries of fitted historical residuals, not a complete posterior-predictive test with an independently simulated reference distribution for each statistic. Parameter and state estimation, finite-sample uncertainty, and the concentration of extreme behavior around one crash all matter when interpreting a nominal residual moment as evidence against the model.

## What a reproduction should establish

A credible reproduction would first fix the unit system, jump convention, compensator, and risk-premium sign. It would then reproduce the option panel and parity adjustment, retain the actual contract sampling ledger, and implement the full posterior with all serial-error and state-dependent jump terms. Priors, latent-state constraints, chain diagnostics, quadrature accuracy, and particle-filter settings must be supplied explicitly because the source omits them.

Validation should separate three outputs: posterior-averaged in-sample option errors; genuinely lagged out-of-sample prices under fixed structural parameters; and historical return/variance residual diagnostics. Report errors by maturity and moneyness before aggregating, because the leading model's advantage reverses across horizon groups. Preserve both latent-path draws and posterior means so path roughness is not accidentally removed before checking $\sigma_V$.

The economic finding is that options and returns jointly constrain different aspects of risk. Rare jumps may be essential for explaining market discontinuities even when their effect on average option-price error is small. The principal unresolved feature is variance dynamics across regimes: a single stationary factor with positive jumps struggles to fit both the spike and fast reversal of a crisis, and the subsequently lower term structure. Multifactor variance or state-dependent mean reversion is a motivated extension suggested by these diagnostics, not an extension estimated and validated in this paper.
