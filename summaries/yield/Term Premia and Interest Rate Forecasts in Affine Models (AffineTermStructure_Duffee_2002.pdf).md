# Term Premia and Interest Rate Forecasts in Affine Models

Gregory R. Duffee. *The Journal of Finance* 57(1), February 2002, pp. 405–443. Source: [AffineTermStructure_Duffee_2002.pdf](../../Finance/AffineTermStructure_Duffee_2002.pdf), 39 pages. All pages, including the conditional-moment appendix, were read. Printed page $p$ corresponds to PDF page $p-404$.

## Why this matters

A no-arbitrage yield-curve model is useful for forecasting only if its restrictions preserve the sources of predictability in the data. Duffee finds that the standard affine specifications of his period often do worse than holding today's yield unchanged. Their errors are systematically related to the yield-curve slope: when a steep curve predicts high future bond returns, the models underpredict those returns. This occurs in sample as well as in a reserved 1995–1998 holdout.

The paper introduces an “essentially affine” class that lets compensation for interest-rate risk move independently of conditional volatility while retaining affine physical dynamics, affine pricing dynamics, and exponentially affine bond prices. A Gaussian member of that class improves forecasts and largely absorbs the slope's predictive information. Its success comes at the cost of constant conditional volatility. Models with more volatility flexibility achieve higher likelihood values but worse forecasts.

For a quantitative rates process, the lesson is that volatility fit and expected-return fit need separate validation. A model that is attractive for pricing or risk management can be a poor source of duration alpha. Conversely, the best conditional-mean model in these tests is not a complete joint model of yield means, variances, tails, and option prices.

## The empirical restriction driving the model design

Monthly Treasury excess returns are regressed on the previous month-end five-year minus three-month zero-coupon yield spread and on previous-month realized five-year yield volatility. The latter is the square root of the sum of squared daily yield changes during the month. Excess returns subtract the contemporaneous three-month Treasury-bill return. The source is CRSP for bond portfolios and interpolated McCulloch–Kwon/Bliss yields for the term structure.

Table I covers July 1961–December 1998 and reports 449 observations. Volatility does not have statistically significant incremental predictive power, whereas all slope coefficients have heteroskedasticity-adjusted $t$-statistics above 1.75 and half exceed 2.3. For the three-to-four-year portfolio, the monthly mean excess return is 0.074%, while the standard deviation of fitted excess returns is 0.241%. The slope coefficient is 0.187, with $t=2.38$; the volatility coefficient is 0.706, with $t=1.35$. For five-to-ten-year bonds, the corresponding mean and fitted standard deviation are 0.094% and 0.354%, and the slope $t$-statistic is 2.69.

The important feature is the ratio of a small average premium to substantial predictable variation. A forecast premium need not remain positive. A model in which every individual risk compensation is a constant times a nonnegative variance has difficulty reproducing that behavior together with the observed, only moderately skewed yield distribution. This is not a theorem that volatility never predicts Treasury returns. It is evidence for these variables and this sample that a volatility-only channel misses information in the slope.

## Pricing model and the distinction between measures

Let $X_t\in\mathbb R^n$ be the state and $r_t=\delta_0+\delta'X_t$. Under the equivalent martingale measure $Q$,

$$
dX_t=[c^Q-K^QX_t]dt+\Sigma S_t\,dW_t^Q,
\qquad
(S_t)_{ii}=\sqrt{\alpha_i+\beta_i'X_t},
$$

where $c^Q=(K\theta)^Q$. Each variance must remain nonnegative throughout the admissible state space. Those restrictions constrain both boundary drift and permitted factor interactions. They cannot be replaced by checking a finite observed history alone.

The zero-coupon price is $P(X_t,\tau)=\exp[A(\tau)-B(\tau)'X_t]$, so the yield is

$$
y_t(\tau)=\frac{-A(\tau)+B(\tau)'X_t}{\tau}.
$$

For completeness, substituting this ansatz into the pricing equation gives the following derived Riccati system, consistent with Duffee's sign convention:

$$
A'=-\delta_0-B'c^Q+\frac12\sum_i\alpha_i(\Sigma'B)_i^2,
\qquad
\frac{dB}{d\tau}=\delta-(K^Q)'B-\frac12\sum_i\beta_i(\Sigma'B)_i^2,
$$

with $A(0)=0$ and $B(0)=0$. The first prime in $A'$ denotes maturity differentiation; transposes on vectors are explicit from context. This is an implementation restatement, not an additional empirical result in the paper.

The state-price deflator satisfies $d\pi_t/\pi_t=-r_tdt-\Lambda_t'dW_t$ under the physical measure $P$. Hence physical drift is $c^Q-K^QX_t+\Sigma S_t\Lambda_t$. Bond volatility is $-B(\tau)'\Sigma S_t$, and expected instantaneous excess return is

$$
e_{t,\tau}=-B(\tau)'\Sigma S_t\Lambda_t.
$$

A factor can therefore affect a bond price through its effect on risk compensation even if it does not forecast future short rates under $P$. This is central to the later interpretation of twist shocks.

## Completely and essentially affine compensation

The completely affine restriction is $\Lambda_t=S_t\lambda_1$. Then $S_t\Lambda_t=S_t^2\lambda_1$ is affine in $X_t$, as is $\Lambda_t'\Lambda_t$. Physical dynamics remain affine, but the compensation attached to each Brownian shock has a fixed sign and is proportional to a variance. A Gaussian model under this restriction has constant expected instantaneous excess returns.

Duffee preserves the useful affine product while allowing the price-of-risk vector itself to be more flexible. Define a diagonal matrix $S_t^-$ by

$$
(S_t^-)_{ii}=
\begin{cases}
(\alpha_i+\beta_i'X_t)^{-1/2},&\inf_{X\text{ admissible}}(\alpha_i+\beta_i'X)>0,\\
0,&\text{otherwise}.
\end{cases}
$$

The essentially affine specification is

$$
\Lambda_t=S_t\lambda_1+S_t^-\lambda_2X_t.
$$

If a variance can approach zero anywhere in the admissible state space, its inverse term is disabled even if the boundary is inaccessible along an ordinary sample path. This ensures that the additional price of risk does not explode near zero variance. The product $S_tS_t^-=I^-$ is a diagonal selector, so the physical drift remains affine. The variance of the log deflator need no longer be affine; exponential-affine bond pricing does not require that extra restriction.

In the canonical $A_m(n)$ normalization, $\Sigma=I$, the first $m$ states are nonnegative variance factors, their corresponding $\alpha_i$ are zero, and other variances have constant term one plus nonnegative combinations of those factors. The first $m$ rows of $\lambda_2$ are zero; its remaining $(n-m)n$ entries create the extension. For $m=n$, there is no extension of this form. For $m=0$, all Gaussian risk prices can depend on every state.

This is the paper's new model class and principal contribution. Affine pricing itself, the older completely affine class, and the empirical expectations-hypothesis failure are background. Duarte's semi-affine alternative adds a constant to $S_t\lambda_1$; it can change signs but still ties variation to volatility, and usually makes physical dynamics nonaffine. Duffee's extension is different because it keeps tractable conditional physical moments.

## Why the older restriction fails

In a one-factor square-root model, let $r_t=\delta_0+x_t$, $dx_t=\kappa(\theta-x_t)dt+\sigma\sqrt{x_t}dW_t$, and $\Lambda_t=\lambda_1\sqrt{x_t}$. Expected excess return is proportional to $x_t$. For a positive mean premium,

$$
\frac{E[e_{t,\tau}]}{\sqrt{\operatorname{Var}(e_{t,\tau})}}
=\frac{\theta}{\sqrt{\operatorname{Var}(x_t)}}.
$$

Duffee sets this ratio to 0.3, representative of Table I, and matches a short-rate mean of 5.5% and standard deviation of 2.9%. This forces $\theta=0.87\%$ and $\delta_0=4.63\%$. The model then forbids short rates below 4.63%, whereas observed three-month yields ranged from about 0.6% to 16%. Inverting those observed yields produces negative states in more than 40% of monthly observations. Making the state admissible throughout the observed range instead forces the premium mean-to-standard-deviation ratio above 1.6.

The argument isolates a real tradeoff: to combine a nonnegative premium with a mean much smaller than its standard deviation, the latent state must be strongly positively skewed, leaving little room for below-average yields. Multifactor models can cancel premiums of opposite signs at a particular maturity. Cancellation at every maturity is much harder when different factors are needed for level, slope, and curvature. Duffee explicitly presents the long-maturity single-dominant-factor reasoning as practical intuition rather than a universal impossibility theorem for all affine parameterizations.

A two-factor example reinforces the mechanism. A Gaussian short rate and an independent square-root factor under $P$ reduce to Vasicek pricing under completely affine compensation. Under essentially affine compensation, the square-root factor affects the price of the Gaussian shock, hence the pricing-measure short-rate dynamics and bond prices. It remains irrelevant for the physical short-rate path. This separates a premium shock from a short-rate-expectation shock without giving up tractability.

## Data, state extraction, and objective

The main monthly zero-coupon yield panel spans January 1952–December 1998, with maturities from three months to ten years. McCulloch–Kwon data are used through February 1991, and the Bliss extension thereafter. Their overlapping series use different filters and do not exactly agree, so reproducing the splice matters. The estimation sample ends in December 1994; January 1995–December 1998 is held out.

Three yields, at six months, two years, and ten years, are exact observations of the model. Three-month, one-year, and five-year yields have serially uncorrelated measurement errors with constant covariance $CC'$. Correlated cross-sectional errors are permitted through the Cholesky factor $C$. The three-month yield is not an exact anchor because of its idiosyncratic behavior.

Let $Y_t=H_0+H_1X_t$ be the exact-yield vector. Candidate parameters imply $\widehat X_t=H_1^{-1}(Y_t-H_0)$, and every implied state must satisfy the admissible-space constraints. The quasi-likelihood treats the transition as Gaussian with the exact affine conditional mean and covariance, adds a Gaussian measurement-error likelihood, and includes the transformation Jacobian:

$$
\ell_t(\Theta)=\log f_X(\widehat X_t\mid\widehat X_{t-1};\Theta)-\log|\det H_1|+\log f_\varepsilon(\varepsilon_t;\Theta).
$$

The estimate maximizes $\sum_t\ell_t(\Theta)$. Physical stationarity is imposed through positive eigenvalues of the mean-reversion matrix in the paper's implementation, and the initial likelihood uses unconditional moments. For Gaussian models this is exact Gaussian likelihood; for square-root or hybrid models the conditional normal distribution is a quasi-likelihood approximation, not the true transition density.

The admissible-state constraint is imposed explicitly. A generic Gaussian pseudo-density alone assigns positive density to invalid negative variance states and would not enforce it. In contrast, matching simulated moments without fitting each observed curve can produce parameters whose implied historical states violate the model's state space, a concern illustrated using earlier Dai–Singleton estimates.

## Conditional moments and optimization

The affine physical process is $dX_t=(K\theta-KX_t)dt+\Sigma S_t dW_t$. Its conditional mean is

$$
E_t[X_{t+h}]=\theta+e^{-Kh}(X_t-\theta).
$$

Its covariance can be computed without pretending the diffusion is Gaussian:

$$
V_t(h)=\int_0^h e^{-K(h-u)}\Sigma\operatorname{diag}\{\alpha+\beta E_t[X_{t+u}]\}\Sigma'e^{-K'(h-u)}du.
$$

This expression follows from the affine instantaneous covariance and the martingale representation of the state innovation. Appendix equations (A1)–(A11) diagonalize $K$, integrate entrywise, and transform back. It is exact for the first two moments, even though using those moments in a normal density is only QML. Repeated-eigenvalue limits must be handled when denominators such as $d_j+d_k-d_i$ vanish; stable integral or matrix-exponential routines avoid cancellation.

The optimization is substantial rather than a single local fit. Random parameter vectors are drawn from diagonal-covariance normal distributions with plausible means and variances; infeasible draws are rejected; feasible candidates are improved with a simplex search and then NPSOL. The process continues until 1,000 completed local optimizations. The paper does not publish the full random-start distributions, random seed, numerical tolerances, or all unrestricted parameter estimates. Those omissions prevent bit-for-bit replication from the article alone.

Parsimonious preferred specifications drop parameters with absolute $t$-statistics no greater than one, with one volatility parameter set to one rather than zero. Seven parameters are removed from each selected essentially affine model and five from the selected completely affine model. The preferred $A_1(3)$ restrictions formally reject at $p=0.013$; Duffee attributes this in part to unstable numerical derivatives for $\kappa_{32}$. This should remain a qualification, not be converted into a clean statistical endorsement of that restricted model.

## Specification tests and model selection

The score conditions of QML are treated as exactly identified GMM moments. Restrictions on $\lambda_2$ are tested with a score-moment quadratic form using the unrestricted covariance weighting matrix. The corresponding degrees of freedom are $n(n-m)$. A separate test adds three moments requiring six-month-ahead forecast errors for six-month, two-year, and ten-year yields to be uncorrelated with the formation-date five-year minus three-month slope. Overlapping forecasts require serial-correlation adjustment; the implementation uses Newey–West with eight lags.

Table II illustrates the conflict between objective and intended use:

| Unrestricted model | Parameters | QML | Slope-error test $p$ |
|---|---:|---:|---:|
| Completely affine $A_0(3)$ | 19 | 15,171.94 | 0.006 |
| Completely affine $A_1(3)$ | 23 | 15,380.31 | below 0.001 as printed |
| Completely affine $A_2(3)$ | 24 | 15,395.74 | 0.019 |
| Completely affine $A_3(3)$ | 25 | 15,396.34 | below 0.001 as printed |
| Essentially affine $A_0(3)$ | 28 | 15,196.45 | 0.596 |
| Essentially affine $A_1(3)$ | 29 | 15,392.47 | 0.001 |
| Essentially affine $A_2(3)$ | 27 | 15,396.04 | 0.010 |

The Gaussian essentially affine model alone passes the forecast-information test comfortably. The preferred version has 21 parameters, QML 15,190.68, and $p=0.694$. Additional volatility factors improve the likelihood while restricting the premium dynamics that matter for forecasting. Failure to reject is not proof of complete forecast efficiency: the added moments test only the specified slope relationship at the selected horizon and maturities.

## Forecast design and numerical results

Models fitted through 1994 forecast yields at fixed maturities six months, two years, and ten years at horizons three, six, and twelve months. This is a constant-maturity yield forecast, not the realized price of an aging bond. The random-walk benchmark predicts $y_{t+h}(\tau)=y_t(\tau)$. The OLS benchmark regresses the fixed-maturity yield change on an intercept and the current slope, using only the training sample, and applies those coefficients to holdout observations.

The holdout uses $48-h$ monthly forecasts for a horizon of $h$ months: 45, 42, and 36 overlapping errors. It is a fixed-parameter holdout, not a recursively reestimated experiment. Its small effective sample, especially at twelve months, limits conclusions about stable outperformance across regimes.

Table VIII's preferred-model values are:

| Maturity / horizon | Random walk | OLS | Completely affine $A_2$ | Essentially affine $A_0$ | Essentially affine $A_1$ |
|---|---:|---:|---:|---:|---:|
| 6 months / 3 months | 0.298 | 0.298 | 0.350 | 0.281 | 0.284 |
| 2 years / 3 months | 0.499 | 0.511 | 0.523 | 0.457 | 0.450 |
| 10 years / 3 months | 0.484 | 0.498 | 0.485 | 0.469 | 0.453 |
| 6 months / 6 months | 0.400 | 0.413 | 0.548 | 0.365 | 0.385 |
| 2 years / 6 months | 0.652 | 0.675 | 0.711 | 0.566 | 0.560 |
| 10 years / 6 months | 0.669 | 0.693 | 0.669 | 0.636 | 0.606 |
| 6 months / 12 months | 0.484 | 0.523 | 0.778 | 0.421 | 0.455 |
| 2 years / 12 months | 0.762 | 0.787 | 0.879 | 0.600 | 0.606 |
| 10 years / 12 months | 0.815 | 0.829 | 0.811 | 0.738 | 0.698 |

These are the printed RMSE entries. The captions say yields are measured in decimal form but omit an explicit scaling factor for these entries. Their magnitudes are economically consistent with percentage-point yield errors, so 0.600 would correspond to 60 basis points under that interpretation; this unit conversion is inferred, not silently attributed to an unambiguous caption. Relative comparisons do not depend on the common scaling.

For two-year yields at twelve months, the Gaussian preferred model lowers RMSE from 0.762 to 0.600, a derived 21.3% reduction. For six-month yields at twelve months the reduction is 13.0%. OLS generally fails to improve on the holdout random walk even though it must weakly improve the in-sample sum of squared errors. The Gaussian model beats both benchmarks in all nine cases, but it does not beat the one-volatility-factor model in every cell. The latter is particularly competitive for ten-year holdout yields.

In sample, the preferred Gaussian RMSE for the ten-year yield at twelve months is 1.009 versus 1.109 for the random walk and 1.018 for OLS. The completely affine preferred value is 1.131. The completely affine models' failure is therefore not merely a holdout accident or the penalty for estimating too many parameters.

## Residual predictability and economic interpretation

Forecast-error regressions explain why some RMSE comparisons matter. In Table VII, the preferred completely affine model's twelve-month ten-year forecast error has a slope coefficient of −0.507 with $t=-4.52$. The preferred Gaussian coefficient is −0.101 with $t=-0.92$. In the holdout, however, the Gaussian twelve-month ten-year error still has slope coefficient −0.730 with $t=-2.52$. The source therefore contains an explicit exception to the broad claim that the Gaussian model absorbs slope predictability.

Figures 1–3 compare factor shock responses and fitted instantaneous expected returns. The Gaussian model's two-year expected excess return has mean 1.25% per year and standard deviation 3.09% per year. The essentially affine one-volatility-factor model has 1.90% and 1.85%; the completely affine two-volatility-factor model has 0.79% and 0.41%. These are time-series statistics of conditional instantaneous expected returns, not realized return volatilities or forecast Sharpe ratios.

In the Gaussian interpretation, level shocks change expected short rates almost permanently, with a half-life above eleven years, and affect premiums little. Slope shocks affect short rates and premiums over a business-cycle scale, with a reported four-year half-life for their short-rate effect. Twist shocks mainly affect required excess returns, with a half-life below three months. Calling the last a “flight to quality” is an economic interpretation of fitted latent dynamics, not an identified causal event study.

The one-volatility-factor model makes the level factor the volatility driver. Admissibility then prevents other factors from freely changing its risk price. The slope-to-level-risk-price channel available in the Gaussian model is lost. The preferred completely affine model produces relatively small, persistently positive premiums that move with short rates, often in the wrong direction relative to the yield slope.

## Printed formula checks and replication limits

Several printed equations require care. Equation (12b) has a plus sign on $\Sigma I^-\lambda_2$ even though equations (6), (10), and (11) imply

$$
K=K^Q-\Sigma[\operatorname{diag}(\lambda_1)\beta+I^-\lambda_2].
$$

This is a derived correction verified against the physical-drift convention. Equation (20)'s text defines $H_0$ using $A/\tau$, whereas equation (4) requires $-A/\tau$. Appendix equation (A10) visibly multiplies the first variance term by the long-run-mean sum; equation (A8) and direct integration require addition. Implementing the conditional covariance integral above avoids that typographical error. These issues are in the printed source, not merely extraction artifacts, and do not establish that the author's actual estimation code contained the errors.

A serious replication needs the original interpolated yield panel, splice rule, exact observation dates, complete model normalizations, parameter constraints under both measures, and numerical optimizer settings. The article does not publish every unrestricted estimate or executable code. A modern extension should retain the original holdout as a historical replication and use a separately labeled rolling or expanding evaluation for subsequent data. Model selection and parameter pruning must occur within each training window.

The source provides no transaction-cost model, holdings, leverage rule, funding assumption, or portfolio objective. Turning yield forecasts into a strategy requires aging-bond pricing, carry and roll-down, risk constraints, turnover, and uncertainty-aware position sizing. RMSE improvements alone do not quantify attainable trading returns. The strongest supported claim is that allowing risk compensation to vary independently of volatility is empirically important for affine yield forecasts, and that the likelihood ranking alone does not reveal which model forecasts best.

## Bibliographic and source map

Duffee, Gregory R. (2002), “Term Premia and Interest Rate Forecasts in Affine Models,” *Journal of Finance* 57(1), 405–443. Model construction: pp. 407–415, equations (1)–(17). Failure mechanism: pp. 416–418. Data, QML, optimization, and GMM tests: pp. 419–423. Parameters and forecasts: Tables II–IX, pp. 424–433. Factor interpretations: Figures 1–3 and pp. 434–439. Exact conditional moments: Appendix, pp. 439–442. Bibliography: pp. 442–443. Related studies are described here as positioned by the supplied source rather than independently verified external evidence.
