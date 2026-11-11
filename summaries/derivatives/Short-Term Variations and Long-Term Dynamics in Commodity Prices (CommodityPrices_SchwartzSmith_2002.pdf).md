# Short-Term Variations and Long-Term Dynamics in Commodity Prices

Eduardo Schwartz and James E. Smith, *Management Science* 46(7), July 2000, pp. 893–911. [Source PDF](../../Finance/CommodityPrices_SchwartzSmith_2002.pdf). Despite the historical filename's 2002 suffix, the supplied nineteen-page document is the published 2000 article. Its complete text and mathematical appendix are covered below. Journal page numbers equal PDF page numbers plus 892.

## Why this matters

Commodity projects often have cash flows much longer lived than the disturbances dominating today's spot price. A model that assigns all spot volatility to permanent uncertainty can substantially misrepresent a long-lived investment; a model that makes every shock temporary misses changes in long-run value. Schwartz and Smith separate log spot price into a mean-reverting deviation and a stochastic equilibrium level. This representation produces tractable futures prices, European option prices, exact Gaussian state transitions, and a two-dimensional real-option problem.

The innovation is primarily a useful factorization, not a new distributional family relative to Gibson–Schwartz. The authors prove exact equivalence with that earlier stochastic-convenience-yield model under a linear transformation of states and parameters. The new coordinates clarify what long-maturity futures identify, why physical expected returns remain uncertain, and when a one-factor approximation for long-lived cash flows is defensible. There is no explicit production or inventory equilibrium: “equilibrium price” is the economic interpretation of a latent permanent component.

## Physical dynamics and exact transitions

Let $S_t>0$ denote spot price and write

$$
\log S_t=\chi_t+\xi_t,
$$

where $\chi_t$ is the temporary log-price deviation and $\xi_t$ the equilibrium *log* level. Their physical dynamics are

$$
d\chi_t=-\kappa\chi_t\,dt+\sigma_\chi\,dW_{\chi,t},\qquad d\xi_t=\mu_\xi\,dt+\sigma_\xi\,dW_{\xi,t},
$$

$$
dW_{\chi,t}\,dW_{\xi,t}=\rho\,dt.
$$

Here $\kappa>0$, volatilities are nonnegative, and $|\rho|\leq1$. The factors are not independent unless $\rho=0$. The deviation's conditional half-life is $\log2/\kappa$; the equilibrium price $e^{\xi_t}$ is geometric Brownian motion. The full spot process is therefore not stationary when the permanent factor is stochastic, even though one of its components mean reverts.

For horizon $h$, define $b_h=e^{-\kappa h}$ and

$$
Q(h)=\begin{pmatrix}
\sigma_\chi^2(1-b_h^2)/(2\kappa)&\rho\sigma_\chi\sigma_\xi(1-b_h)/\kappa\\
\rho\sigma_\chi\sigma_\xi(1-b_h)/\kappa&\sigma_\xi^2h
\end{pmatrix}.
$$

The exact transition is Gaussian with mean $(b_h\chi_t,\xi_t+\mu_\xi h)'$ and covariance $Q(h)$. It follows directly by integrating the OU equation and the Brownian equation against their correlated innovations. This exact transition should be used in a filter or simulator; Euler time discretization is unnecessary.

Let

$$
v_S(h)=\frac{\sigma_\chi^2}{2\kappa}(1-b_h^2)+\sigma_\xi^2h+\frac{2\rho\sigma_\chi\sigma_\xi}{\kappa}(1-b_h).
$$

Then $\log S_{t+h}$ has conditional mean $b_h\chi_t+\xi_t+\mu_\xi h$ and variance $v_S(h)$, so

$$
E_t[S_{t+h}]=\exp\{b_h\chi_t+\xi_t+\mu_\xi h+\tfrac12v_S(h)\}.
$$

The half-variance adjustment is exact, not a small-volatility approximation. Far into the future, the log expected spot price approaches a straight line with intercept $\xi_t+\sigma_\chi^2/(4\kappa)+\rho\sigma_\chi\sigma_\xi/\kappa$ and slope $\mu_\xi+\sigma_\xi^2/2$. This effective long-run expected-price intercept differs from the current equilibrium log level. Permanent-factor uncertainty eventually dominates forecast variance, whose leading growth term is $\sigma_\xi^2h$.

The appendix derives the same covariance by taking a discrete-time limit. Several intermediate printed expressions on p. 911 have slips: a sum from zero through $n-1$ has numerator $1-\phi^n$, not $1-\phi^{n-1}$, and its squared counterpart uses $1-\phi^{2n}$; the bottom-right covariance term is $n\Delta t\sigma_\xi^2$, not $n\Delta t\sigma_\chi^2$. The main continuous-time covariance in equation (3) is correct. These are direct algebraic corrections to the supplied printing, not changes to the model.

## Risk adjustment and the futures curve

The model assumes constant reductions in the physical drifts:

$$
d\chi_t=(-\kappa\chi_t-\lambda_\chi)dt+\sigma_\chi dW^Q_{\chi,t},\qquad d\xi_t=\mu_\xi^Qdt+\sigma_\xi dW^Q_{\xi,t},
$$

where $\mu_\xi^Q=\mu_\xi-\lambda_\xi$, and the diffusion covariance is unchanged. Under the pricing measure, the temporary factor reverts to $-\lambda_\chi/\kappa$, not zero. These $\lambda$ parameters are drift adjustments in the units of the respective log factors; they are not automatically standardized Brownian market prices of risk.

For time to maturity $h$, the futures price is the pricing-measure expected terminal spot:

$$
\log F_t(t+h)=b_h\chi_t+\xi_t+A(h),
$$

$$
A(h)=\mu_\xi^Qh-\frac{\lambda_\chi}{\kappa}(1-b_h)+\tfrac12v_S(h).
$$

Forward and futures prices coincide under deterministic interest rates, or the source's stated independence condition. Option and project valuation additionally require discounting; a risk-free rate is not itself needed to fit this particular futures-price expression. It would be incorrect to infer from that parameterization that discounting is irrelevant to all commodity claims.

The physical expected-price/futures-price ratio obeys

$$
\log\frac{E_t[S_{t+h}]}{F_t(t+h)}=\frac{\lambda_\chi}{\kappa}(1-b_h)+\lambda_\xi h.
$$

Thus short-run risk adjustment changes the asymptotic intercept, while long-run risk adjustment changes the asymptotic slope. This is a log ratio of expected levels, not a forecast of the expected log return on futures margin capital.

The instantaneous variance rate of a fixed-delivery futures log price with remaining tenor $h$ is

$$
v_F(h)=b_h^2\sigma_\chi^2+\sigma_\xi^2+2b_h\rho\sigma_\chi\sigma_\xi.
$$

Its volatility is $\sqrt{v_F(h)}$. The source occasionally calls the variance expression “volatility”; the square root is needed for the percentage-per-square-root-year quantities in the figures. At long maturities the volatility tends to $\sigma_\xi$. For the positive estimated correlations it declines with tenor, but monotone decline is not a universal theorem for arbitrary negative $\rho$. The covariance rate between two contracts is obtained by replacing the squared loading with $b_{h_1}b_{h_2}$ and the cross term with $(b_{h_1}+b_{h_2})\rho\sigma_\chi\sigma_\xi$. This gives a directly implementable two-factor hedge covariance matrix.

## European options and consequential printing errors

Consider an option expiring at $u$ on a futures contract delivering at $T\geq u$, with valuation date zero. The pricing-measure variance of $\log F_u(T)$ is

$$
v(u,T)=e^{-2\kappa(T-u)}\frac{\sigma_\chi^2}{2\kappa}(1-e^{-2\kappa u})+\sigma_\xi^2u+2e^{-\kappa(T-u)}\frac{\rho\sigma_\chi\sigma_\xi}{\kappa}(1-e^{-\kappa u}).
$$

This equals the integrated fixed-contract variance over the option's life, $\int_0^u v_F(T-s)ds$. The log mean must be

$$
m(u,T)=\log F_0(T)-\tfrac12v(u,T).
$$

Equivalently, expanding the states gives

$$
m(u,T)=e^{-\kappa T}\chi_0+\xi_0+\mu_\xi^Qu+A(T-u)-e^{-\kappa(T-u)}(1-e^{-\kappa u})\lambda_\chi/\kappa.
$$

The expansion printed on p. 898 drops the last term even though it is present in the previously stated pricing-measure mean of $\chi_u$. Including it restores the martingale identity $E^Q[F_u(T)]=F_0(T)$. The source's variance formula and the resulting Black-form call formula remain valid when expressed in terms of the current futures price.

With $s=\sqrt{v(u,T)}$, $d_1=\log(F_0(T)/K)/s+s/2$, and $d_2=d_1-s$, the correct prices at a constant risk-free rate $r$ are

$$
C=e^{-ru}\{F_0(T)N(d_1)-KN(d_2)\},
$$

$$
P=e^{-ru}\{KN(-d_2)-F_0(T)N(-d_1)\}.
$$

The put displayed on p. 899 instead uses $-F_0N(d_1)+KN(d_2)$, the negative of the call's bracket. It fails nonnegativity and put–call parity. The expression above is a derived correction checked against the payoff expectation and $C-P=e^{-ru}(F_0-K)$, not a verbatim transcription. The annualized option volatility is $s/\sqrt u$, distinct from the instantaneous volatility of the underlying futures. Figure 3 compares them when $u=T$; the option averages the contract's changing exposure as delivery approaches.

## Exact equivalence to stochastic convenience yield

Let $X=\log S$ and $\delta$ be convenience yield in the Gibson–Schwartz coordinates:

$$
dX=(\mu-\delta-\tfrac12\sigma_1^2)dt+\sigma_1dW_1,\qquad d\delta=\kappa(\alpha-\delta)dt+\sigma_2dW_2,
$$

with correlation $\rho_{12}$. Set

$$
\chi=(\delta-\alpha)/\kappa,\qquad \xi=X-(\delta-\alpha)/\kappa.
$$

The yield-dependent drift cancels from $d\xi$. The corresponding parameters are

$$
\sigma_\chi=\sigma_2/\kappa,\quad \mu_\xi=\mu-\alpha-\tfrac12\sigma_1^2,\quad \sigma_\xi^2=\sigma_1^2+\sigma_2^2/\kappa^2-2\rho_{12}\sigma_1\sigma_2/\kappa,
$$

$$
\rho=\frac{\rho_{12}\sigma_1-\sigma_2/\kappa}{\sigma_\xi},\qquad \lambda_\chi=\lambda/\kappa,\qquad \lambda_\xi=\mu-r-\lambda/\kappa.
$$

Here $\lambda$ is the yield drift adjustment in the earlier model. In degenerate cases with zero permanent volatility, the correlation formula is undefined and the covariance representation should be used instead. Both models price the same claims under the corresponding pricing measure. The advantage is interpretability and convenient approximation, not an additional source of risk relative to the original two-factor model.

There is also a parameter redundancy in the yield representation. Shifting $r$, $\delta$, $\alpha$, and $\mu$ together by a constant preserves the relevant drift differences and spot/futures dynamics. The separate absolute values are not all determined by a fitted price process. An externally specified discount rate is still needed for discounted claims.

## Filtering and likelihood: a dimension-consistent implementation

Take $x_j=(\chi_j,\xi_j)'$ and interval $\Delta_j$. The exact physical transition is

$$
x_j=c_j+G_jx_{j-1}+w_j,\quad c_j=(0,\mu_\xi\Delta_j)',\quad G_j=\operatorname{diag}(e^{-\kappa\Delta_j},1),\quad w_j\sim N(0,Q(\Delta_j)).
$$

For observed log futures prices $y_j$ at remaining maturities $h_{ij}$, write

$$
y_j=d_j+H_jx_j+v_j,\qquad (d_j)_i=A(h_{ij}),\qquad (H_j)_{i,\cdot}=(e^{-\kappa h_{ij}},1).
$$

Measurement errors have covariance $V$, are serially uncorrelated Gaussian, and are treated as separate from state innovations. They may represent asynchronous quotes, reporting noise, or model discrepancy. The article describes its measurement matrix as $n\times2$ but transposes it in equations where that would be dimensionally incompatible. The $H_j$ convention above makes every operation explicit.

Given posterior mean $m_{j-1}$ and covariance $C_{j-1}$, calculate

$$
a_j=c_j+G_jm_{j-1},\quad R_j=G_jC_{j-1}G_j'+Q(\Delta_j),
$$

$$
e_j=y_j-d_j-H_ja_j,\quad B_j=H_jR_jH_j'+V,\quad K_j=R_jH_j'B_j^{-1},
$$

$$
m_j=a_j+K_je_j,\qquad C_j=R_j-K_jB_jK_j'.
$$

The Gaussian innovation log likelihood is $-\tfrac12\sum_j[n_j\log(2\pi)+\log\det B_j+e_j'B_j^{-1}e_j]$. Repeated filtering inside numerical optimization estimates the seven model parameters and measurement-error parameters. The source restricts $V$ to a diagonal matrix with maturity-specific variances, uses GAUSS's maxlik routine, and restarts from multiple initial values. Prior state means and covariances are based on observed sample means/covariances; it reports limited sensitivity to alternative priors, but does not supply their exact construction or all optimizer tolerances and constraints.

Two noiseless contracts with distinct tenors and $\kappa>0$ identify both states conditional on parameters because their loading rows are linearly independent. Very similar tenors can still be numerically ill-conditioned. With only noiseless weekly spot prices, the Enron parameter example gives asymptotic standard deviations 0.07995 for each log state. The errors are perfectly negatively correlated because their sum is the observed log spot price. This is roughly eight percent *one-standard-deviation* uncertainty in each level, not an eight-percent confidence interval. Increasing observation frequency to hourly barely changes that illustrative uncertainty.

If the current state has covariance $C_0$, future state covariance is $Q(h)+G_hC_0G_h'$. Forecasting should add this filtering uncertainty to process uncertainty. Parameter uncertainty is a further layer, absent from the conditional Gaussian formulas. Conversely, with very informative cross-sectional futures observations, the posterior approaches the precision-weighted least-squares fit $(H'V^{-1}H)^{-1}H'V^{-1}(y-d)$. This is the connection to fitting today's curve directly; it requires nonsingular relevant matrices or an appropriate exact-observation treatment.

## Samples, estimates, and fit

The first data set contains 259 weekly observations of five NYMEX crude-oil futures prices, approximately 1, 5, 9, 13, and 17 months to maturity, from January 2, 1990 through February 17, 1995. Prices came from Knight-Ridder Financial. The second contains 163 observations of ten proprietary Enron forward prices from January 15, 1993 through May 16, 1996, at approximately 2, 5, and 8 months and 1, 1.5, 2, 3, 5, 7, and 9 years. The article refers to Schwartz (1997) for more detailed data descriptions. It does not provide the raw curves, exact maturity-selection/roll rules, quote-time conventions, or missing-observation filters.

Table 2, p. 903, reports the following estimates; parentheses contain standard errors. Rates are annualized in the model's year time scale.

| Parameter | NYMEX futures | Enron forwards |
|---|---:|---:|
| $\kappa$ | 1.49 (.03) | 1.19 (.03) |
| $\sigma_\chi$ | 28.6% (1.0%) | 15.8% (.9%) |
| $\lambda_\chi$ | 15.7% (14.4%) | 1.4% (8.2%) |
| $\mu_\xi$ | −1.25% (7.28%) | −3.86% (7.28%) |
| $\sigma_\xi$ | 14.5% (.5%) | 11.5% (.6%) |
| $\mu_\xi^Q$ | 1.15% (.13%) | 1.61% (.12%) |
| $\rho$ | .300 (.044) | .189 (.096) |

The implied half-lives are about 5.58 and 6.99 months, respectively. The estimated Enron instantaneous spot volatility is about 21.23 percent, versus long-horizon volatility 11.5 percent. Different sample periods and maturity coverage mean the two parameter sets are not an isolated test of the effect of adding long-dated contracts.

Measurement-error standard deviations for NYMEX maturities are .042, .006, .003, .000, and .004 in log-price units. For Enron they are .027, .006, .000, .002, .000, .005, .014, .032, .043, and .055. Some fitted variances lie on the zero boundary. A singular $V$ need not make the innovation covariance singular, but blindly applying formulas that require $V^{-1}$ would fail. Near-zero measurement variance also makes conditional state uncertainty tiny by assumption and fitted weighting; it is not proof that the latent economic states are observed without model error.

Table 3 reports NYMEX mean absolute log-price errors .0314, .0035, .0020, .0000, and .0028. Enron errors at the ten maturities are .0207, .0049, .0000, .0019, .0000, .0040, .0121, .0276, .0318, and .0332. Thus the worst average errors are about three log percentage points at the shortest NYMEX tenor and far end of the Enron curve. They are in-sample curve-fit errors, not out-of-sample forecasts. Figure 4's Gulf War episode shows estimated spot exceeding \$40 per barrel while the equilibrium level reaches only about \$25, illustrating the temporary/permanent decomposition rather than validating a causal attribution.

## Identification, model comparisons, and forecast interpretation

The physical equilibrium drift and short-run risk premium are estimated imprecisely. A futures cross section strongly constrains pricing-measure quantities but does not directly reveal physical expected spot prices. Holding $\mu_\xi^Q$ fixed removes $\mu_\xi$ from pricing formulas. Moreover, the transformation

$$
\lambda_\chi\mapsto\lambda_\chi+\Delta,\quad \chi_t\mapsto\chi_t-\Delta/\kappa,\quad \xi_t\mapsto\xi_t+\Delta/\kappa
$$

preserves the pricing-measure spot process and futures curve. It does not preserve the same zero-mean physical OU specification without changing the physical interpretation. A sufficiently informative long time series can help estimate physical parameters; the paper's point is weak precision over these samples, not total impossibility of physical identification from every conceivable price history.

Figures 1–2 are not forecasts from the unmodified maximum-likelihood physical drifts. Footnote 9 fixes $\mu_\xi=3\%$, producing an Enron long-run drift premium near 1.4 percent while largely preserving the other estimates. Figure 2 additionally sets $\lambda_\chi=5\%$ and shifts the states to preserve spot and futures prices. On May 16, 1996, the illustrated states $\chi_0=.119$ and $\xi_0=2.857$ imply spot approximately \$19.61 and equilibrium price \$17.41. The expected equilibrium price grows at approximately 3.66–3.67 percent after the lognormal correction. The displayed upper and lower forecast curves are 90th and 10th percentile pointwise bands, not parameter-confidence bands or simultaneous path coverage.

Table 4 compares the two-factor model with geometric Brownian motion and a geometric OU model. Their log likelihoods are, respectively, 5140, 3860, and 4331 for NYMEX, and 6182, 4995, and 5574 for Enron. The two-factor gains over GBM and OU are 1280 and 809 in the first sample, 1187 and 608 in the second. Conventional likelihood-ratio statistics would be twice these gains. The source invokes a chi-square-three comparison, but zero factor volatility places the null on a parameter boundary and can leave correlation or other parameters unidentified; ordinary regular chi-square theory is not automatic. The enormous in-sample fit improvements remain descriptive evidence for both curve movements, without requiring an exact nominal test probability.

Footnote 10 allows a state-dependent short-run premium, so physical and pricing-measure reversion rates differ. Enron estimates are $\kappa^Q=1.19$ (.03) and physical $\kappa=1.79$ (.87). Their difference −.60 suggests one sign for premium dependence, but the physical-rate uncertainty prevents a firm sign conclusion. Neither the baseline nor this extension supplies an out-of-sample trading test, transaction costs, or a demonstrated return-prediction edge.

## Hypothetical development options

The long-lived project costs \$800,000 to develop, starts production after three years, initially produces 5,000 barrels annually, and declines exponentially at five percent annually. The short-lived project costs \$40,000, starts immediately at 1,000 barrels annually, and declines at forty percent. Both have perpetual production after startup, no operating costs, royalties, or taxes, and a perpetual option to wait. Valuation uses Enron parameters and a five-percent risk-free discount rate.

For development cost $I$, lag $L$, initial production $q_0$, and decline rate $d$, the immediate-exercise value can be reconstructed as

$$
J(\chi,\xi)=-I+\int_L^\infty e^{-rs}q_0e^{-d(s-L)}E^Q_{\chi,\xi}[S_s]ds.
$$

The perpetual development option satisfies the discrete decision-time equation

$$
V(x)=\max\{J(x),e^{-r\Delta}E_x^Q[V(x_{\Delta})]\}.
$$

The authors use $\Delta=.1$ year and 35 grid points for each state, giving 1,225 states. They formulate the dynamic program as a linear program and solve it with CPLEX. A reconstruction can impose $V\geq J$ and $V\geq e^{-r\Delta}PV$ and minimize a positive weighted sum of state values. Grid endpoints, transition discretization, tail treatment, and integration tolerances are not fully specified, preventing exact numerical replication from the text alone. Infinite production value is finite here because discount plus decline exceeds the asymptotic pricing-measure expected-price growth rate.

Figure 5 shows the short-lived option depends strongly on both states. With a positive 70-percent deviation, its exercise threshold is about \$23 for the equilibrium price; with negative deviations, it is not exercised below \$40 equilibrium price. The long-lived project's immediate-exercise net value becomes positive around \$13 equilibrium price, but optimal exercise waits until about \$30, with little sensitivity to temporary deviations. Waiting value cannot be summarized by current NPV alone.

These thresholds are outputs of hypothetical projects, not empirical investment recommendations. Long construction lags and slow depletion suppress the influence of today's transitory deviation. A reduced long-run model should therefore use permanent-factor volatility, about 11.5 percent in the Enron estimates, rather than the roughly 21-percent spot volatility. This is an approximation tailored to the cash-flow horizon, not an exact license to drop the short factor from every long-maturity derivative.

The paper's practical package is thus unusually complete: a tractable transition law, a curve-pricing relation, a filtering likelihood, evidence on weak physical identification, and a real-option application. Its limits are also specific: constant Gaussian diffusions, no jumps or volatility smile, no explicit storage equilibrium, a low-rank curve model that leaves systematic end-of-curve errors, and incomplete raw-data/numerical implementation inputs. The stochastic-growth-rate extension mentioned in the conclusion is not developed in the supplied article and should not be attributed a reproducible specification here.
