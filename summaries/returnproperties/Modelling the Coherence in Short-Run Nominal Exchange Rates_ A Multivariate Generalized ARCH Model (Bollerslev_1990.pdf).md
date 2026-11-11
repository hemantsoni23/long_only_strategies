# Modelling the Coherence in Short-Run Nominal Exchange Rates: A Multivariate Generalized ARCH Model

Tim Bollerslev, *The Review of Economics and Statistics* 72(3), August 1990, pp. 498–505. Source: [Bollerslev_1990.pdf](../../Finance/Bollerslev_1990.pdf). The nine-page local file includes a JSTOR cover followed by the complete eight-page article. References below use printed pages; PDF page 2 is printed p. 498. All pages were read and the model, likelihood, and parameter tables were checked visually.

## Why this matters

A multivariate risk model must allow asset variances and covariances to change without generating an invalid covariance matrix. Estimating an unrestricted dynamic equation for every covariance quickly becomes expensive and makes positive definiteness difficult to enforce. Bollerslev proposes a parsimonious solution: model each conditional variance separately and hold conditional correlations constant within an estimation period. Covariances still change because the corresponding volatilities change.

The resulting constant-conditional-correlation model separates marginal volatility dynamics from standardized comovement. It permits a simple positive-definiteness condition, a cheaper likelihood, and comparisons of correlation parameters across regimes. The empirical application asks whether European currencies moved more closely together after the European Monetary System, or EMS, began in March 1979. The model fits weekly exchange-rate dependence reasonably well within each subperiod; all ten estimated correlations rise after the EMS starts, especially several pairs involving EMS participants. These are descriptive regime comparisons, not a causally identified policy evaluation or a trading strategy.

## Contribution and exact model

The general setup on pp. 499–500 is

$$
y_t=E[y_t\mid\mathcal F_{t-1}]+\varepsilon_t,\qquad
E[\varepsilon_t\mid\mathcal F_{t-1}]=0,\qquad
E[\varepsilon_t\varepsilon_t'\mid\mathcal F_{t-1}]=H_t.
$$

The vector $y_t$ contains $N$ observed series and $\mathcal F_{t-1}$ is available information through the previous period. The covariance matrix $H_t$ must be positive definite almost surely. Writing its entries as $h_{ij,t}$, the defining restriction is

$$
h_{ij,t}=\rho_{ij}\sqrt{h_{ii,t}h_{jj,t}},\qquad i\ne j.
$$

Thus $\rho_{ij}$ is constant through time inside a fitted model. It is the conditional correlation, not the covariance and not generally the unconditional sample correlation of raw returns. This distinction is the main identification and interpretation issue in the paper.

A convenient normalized implementation sets $S_t=\operatorname{diag}(\sqrt{h_{11,t}},\ldots,\sqrt{h_{NN,t}})$ and uses a correlation matrix $R$ with unit diagonal:

$$
H_t=S_tRS_t.
$$

Strictly positive marginal variances and $R\succ0$ are sufficient and necessary for positive definiteness of $H_t$ under this representation. Checking each pairwise correlation lies between −1 and 1 is insufficient: the full matrix must be positive definite. A Cholesky parameterization followed by diagonal normalization is a possible numerical implementation; it is not the particular constraint code reported by the author.

The paper itself uses a scale-unrestricted representation $h_{ii,t}=\omega_i\sigma_{it}^2$, with $D_t=\operatorname{diag}(\sigma_{1t},\ldots,\sigma_{Nt})$ and

$$
H_t=D_t\Gamma D_t,\qquad \Gamma_{ij}=\rho_{ij}\sqrt{\omega_i\omega_j}.
$$

This decomposition is only unique up to scale. The distinction matters when profiling the likelihood: a sample covariance of standardized residuals estimates the unrestricted $\Gamma$, whereas an arbitrary fixed-unit-diagonal correlation matrix cannot simply be replaced by an unconstrained sample covariance without treating scales consistently.

For the exchange-rate application, the mean is constant and each variance follows a GARCH(1,1):

$$
y_{it}=\mu_i+\varepsilon_{it},\qquad
h_{ii,t}=\omega_i+\alpha_i\varepsilon_{i,t-1}^2+\beta_i h_{ii,t-1}.
$$

Together with the correlation restriction this is equation (8), printed p. 501. There are five means, fifteen marginal variance parameters, and ten pairwise correlations, hence 30 parameters in the five-currency system. The variance specification uses only the series' own lagged squared innovation and variance. It does not contain explicit cross-currency shock spillovers, asymmetric news effects, or a separate correlation recursion.

For positive variances, the conventional sufficient restrictions are $\omega_i>0$, $\alpha_i\geq0$, and $\beta_i\geq0$, with positive starting values. A finite unconditional variance additionally requires $\alpha_i+\beta_i<1$ under unit-variance standardized innovations. That last restriction is not imposed uniformly in the reported estimates: the pre-EMS Italian-lira estimate exceeds one. A replication that forces covariance stationarity will therefore solve a different constrained problem and cannot reproduce Table 2 exactly.

## Likelihood, profiling, and numerical estimation

Under conditional normality, the joint log likelihood apart from initialization is

$$
\ell(\theta)=-\frac{TN}{2}\log(2\pi)-\frac12\sum_{t=1}^T\left[\log|H_t|+\varepsilon_t'H_t^{-1}\varepsilon_t\right].
$$

Using $H_t=D_t\Gamma D_t$ and $\widetilde\varepsilon_t=D_t^{-1}\varepsilon_t$ yields

$$
\ell(\theta)=-\frac{TN}{2}\log(2\pi)-\frac T2\log|\Gamma|-\sum_{t=1}^T\log|D_t|-\frac12\sum_{t=1}^T\widetilde\varepsilon_t'\Gamma^{-1}\widetilde\varepsilon_t.
$$

Only one dense matrix inversion is needed per likelihood evaluation, since $\Gamma$ is fixed across dates. The diagonal operations remain date-specific. The author notes that with 30 parameters, numerical first derivatives, and 333 observations, a simple implementation reduces matrix inversions per iteration from 10,323 to 31. This counts likelihood evaluations for numerical derivatives, not a universal complexity bound for all optimizers.

Conditional on the standardized residual vectors in the scale-unrestricted representation, the maximizing matrix is

$$
\widehat\Gamma=\frac1T\sum_{t=1}^T\widetilde\varepsilon_t\widetilde\varepsilon_t'.
$$

Its normalized entries recover the estimated correlations. Positive definiteness requires the residual vectors to span the relevant dimension; in a nondegenerate sample with sufficiently many observations this is the usual case. Substitution profiles out $N(N+1)/2$ covariance parameters and gives the concentrated likelihood in equation (7). The Jacobian term $-\sum_t\log|D_t|$ remains essential. Dropping it would favor arbitrary changes in residual scaling and would not estimate the proposed model.

The estimation method is the Berndt–Hall–Hall–Hausman algorithm with numerical first derivatives. The paper warns that the information matrix is not block diagonal between volatility and covariance parameters. Standard errors therefore require derivatives of the full likelihood even if the concentrated likelihood is used during optimization. Fitting independent univariate GARCH models and then calculating a residual correlation matrix can be a useful starting procedure, but it is not automatically identical to joint maximum likelihood.

Conditional Gaussianity is an approximation, particularly because exchange-rate arrangements impose bounds on some cross rates. The author cites quasi-maximum-likelihood results: if the first two conditional moments are correct and suitable regularity conditions hold, a Gaussian criterion can consistently estimate the parameters under nonnormality, but conventional information-matrix standard errors need modification. A modern robust covariance implementation should state the sandwich estimator used. The article does not provide the full numerical derivative scheme, convergence tolerance, starting parameters, variance initialization, or source code.

## Data and experimental design

The observations are interbank closing spot exchange rates on Wednesdays, obtained from the *International Monetary Markets Yearbook* and supplied by Frank Diebold. The five currencies are the German mark (DM), French franc (FF), Italian lira (IL), Swiss franc (SF), and British pound (BP), each against the U.S. dollar. The full interval is July 1973 through August 1985.

The transformed dependent variable is

$$
y_{it}=100\log\left(\frac{s_{it}}{s_{i,t-1}}\right).
$$

Consequently, means are weekly log-percentage changes and conditional variances are in squared percentage units. The sign interpretation of the reported positive EMS means corresponds to European-currency depreciation against the dollar. A data reconstruction must retain the source quotation direction rather than assume that all downloaded exchange rates use the same convention.

The main EMS sample starts in the third week of March 1979 and ends in the second week of August 1985, with 333 weekly observations. The pre-EMS sample covers July 1973 through March 1979, with 299 observations. Germany, France, and Italy are EMS participants in the comparison; Switzerland and Britain are not. Both subperiods use the same five-dimensional specification so that correlations and volatility parameters can be compared.

The design contains no training/validation split, rolling forecast, portfolio formation, rebalancing rule, cost assumption, or investment-performance metric. All parameter and diagnostic results are fitted within the respective sample. The alternative October 1979 break and yen-numeraire exercise are specification comparisons, not independent forecast validation. The paper also does not enumerate the exact date vector, holiday replacement convention, data-cleaning exclusions, or initial weekly price used to form the first return. Those omissions prevent a guaranteed numerical reproduction from a modern vendor file alone.

Before fitting volatility, the author checks the simple constant-drift random-walk description of spot rates. Phillips–Perron unit-root/no-trend statistics range from 1.999 for FF to 3.937 for BP, below the cited 10% critical value of 5.34. A Newey–West-type variance estimate uses truncation lag ten; nearby lag choices give similar results. The largest 20-lag Ljung–Box statistic for mean residuals is 23.203, below the 95% chi-square critical value 31.410. These failures to reject support a parsimonious mean equation but do not prove market efficiency or independence.

## Parameter estimates and their units

The following values reproduce the point estimates in Tables 1–2 on p. 503. The persistence sum is calculated here from the printed coefficients.

| Period | Currency | $\mu$ | $\omega$ | $\alpha$ | $\beta$ | $\alpha+\beta$ |
|---|---|---:|---:|---:|---:|---:|
| EMS | DM | 0.174 | 0.120 | 0.036 | 0.919 | 0.955 |
| EMS | FF | 0.255 | 0.027 | 0.017 | 0.975 | 0.992 |
| EMS | IL | 0.298 | 0.340 | 0.152 | 0.685 | 0.837 |
| EMS | SF | 0.180 | 0.055 | 0.061 | 0.930 | 0.991 |
| EMS | BP | 0.171 | 0.110 | 0.086 | 0.879 | 0.965 |
| Pre-EMS | DM | −0.073 | 0.043 | 0.042 | 0.921 | 0.963 |
| Pre-EMS | FF | 0.013 | 0.210 | 0.151 | 0.699 | 0.850 |
| Pre-EMS | IL | 0.020 | 0.028 | 0.527 | 0.626 | 1.153 |
| Pre-EMS | SF | −0.114 | 0.056 | 0.127 | 0.851 | 0.978 |
| Pre-EMS | BP | 0.070 | 0.226 | 0.112 | 0.675 | 0.787 |

The EMS mean standard errors are 0.079, 0.095, 0.070, 0.083, and 0.080 in the listed currency order. For the EMS intercepts $\omega$, the standard errors are 0.085, 0.020, 0.112, 0.041, and 0.071. For $\alpha$, they are 0.085, 0.008, 0.038, 0.015, and 0.033; for $\beta$, 0.047, 0.011, 0.081, 0.023, and 0.047. These are the printed asymptotic values, including the large DM $\alpha$ standard error.

The prose on p. 501 says all variance parameters are individually significant at 5%, but the printed table does not support that blanket statement under ordinary estimate/standard-error comparisons. For example, the EMS DM $\alpha$ estimate 0.036 with standard error 0.085 does not pass a conventional two-sided normal test. This discrepancy was checked against the page image. It does not negate the much stronger joint evidence of time-varying variance; it limits what should be claimed about individual coefficients.

For currencies with persistence below one, the implied unconditional variance is $\omega/(1-\alpha-\beta)$. Calculated from rounded printed estimates, the EMS values are approximately 2.667, 3.375, 2.086, 6.111, and 3.143 squared percentage units. These are derived values, not additional source estimates, and are especially sensitive to rounding when persistence is close to one. The pre-EMS Italian estimate has no finite unconditional variance under this moment calculation; plugging it mechanically into the fraction would produce a negative number with no variance interpretation. Footnote 9 explicitly recognizes the exception while noting that conditional moments remain well-defined.

## Correlation changes: main empirical result

All ten conditional-correlation estimates rise in the EMS sample:

| Pair | Pre-EMS estimate (SE) | EMS estimate (SE) | Increase |
|---|---:|---:|---:|
| DM–FF | 0.607 (0.041) | 0.932 (0.008) | 0.325 |
| DM–IL | 0.425 (0.043) | 0.886 (0.013) | 0.461 |
| FF–IL | 0.441 (0.046) | 0.876 (0.017) | 0.435 |
| DM–SF | 0.714 (0.029) | 0.917 (0.010) | 0.203 |
| FF–SF | 0.517 (0.049) | 0.866 (0.019) | 0.349 |
| IL–SF | 0.336 (0.063) | 0.816 (0.021) | 0.480 |
| DM–BP | 0.443 (0.050) | 0.674 (0.032) | 0.231 |
| FF–BP | 0.488 (0.046) | 0.676 (0.034) | 0.188 |
| IL–BP | 0.345 (0.055) | 0.622 (0.040) | 0.277 |
| SF–BP | 0.305 (0.069) | 0.635 (0.035) | 0.330 |

The largest absolute increase is IL–SF, a pair containing a non-EMS currency, so the result is not simply an EMS-members-only effect. Nevertheless, DM's correlation increases with FF and IL exceed its increases with SF and BP, and BP has the lowest correlations with the other currencies in the later period. The evidence is consistent with additional comovement among EMS members superimposed on a broad increase in European-currency coherence.

Because all rates share a dollar numeraire, common dollar movements can contribute materially to their comovement. Re-estimation against the Japanese yen leaves the qualitative findings unchanged. The article reports that robustness conclusion without a corresponding full coefficient table, so it supports direction rather than exact numerical replication of the yen case. The author also notes that increased Italian monetary and fiscal discipline could explain some results without requiring heightened coordination among all EMS members.

## Diagnostics and what they test

A raw squared-residual Ljung–Box statistic of 113.020 for BP at 20 lags provides clear motivation for volatility dynamics despite weak linear return autocorrelation. In the multivariate model, the reported likelihood-ratio statistic against absence of conditional heteroskedasticity is 117.028, evaluated by the paper against a chi-square distribution with ten degrees of freedom. Against zero cross-currency correlations, the LR statistic is 1,911.078 with ten degrees of freedom. Both overwhelmingly reject the simple restrictions under the stated reference distributions. Boundary and identification issues can matter for formal GARCH null testing; the source does not develop a specialized finite-sample correction.

After fitting, the AR(1)/MA(1) LM statistic is 8.459 on five degrees of freedom, at the 0.867 cumulative fractile, hence an upper-tail probability about 0.133. The LM statistic for extending GARCH(1,1) to GARCH(1,2) is 7.669, at the 0.825 fractile of chi-square five, hence about 0.175 in the upper tail. Neither rejects at 5%.

Twenty-lag Ljung–Box tests on squared standardized residuals are 27.612, 6.133, 26.318, 22.276, and 22.942 for DM, FF, IL, SF, and BP. All fall below the cited 5% threshold. Products of standardized residuals are also checked: their portmanteau statistics range from 16.681 to 28.062. This last diagnostic directly addresses omitted dynamics in cross moments under constant conditional correlation.

The raw SF–BP residual product has a statistic of 101.496, compared with 23.700 after volatility standardization. That contrast is the clearest diagnostic demonstration of what the model does: it explains dynamic covariance through changing scales while leaving standardized dependence comparatively stable. A constant correlation assumption should be tested on standardized cross products, not by demanding that raw cross products be serially uncorrelated.

The paper additionally runs residual-based conditional-moment regressions, obtaining variance-equation F statistics 1.793, 0.366, 1.369, 1.350, and 0.572, all below the stated $F_{6,326}$ 5% critical value 2.13. The largest covariance-equation statistic is 1.797, below the $F_{8,324}$ critical value 1.97. These diagnostics support descriptive adequacy in the chosen sample; they do not establish the correlation restriction at other frequencies or across future crises.

## Break comparisons and replication limits

The maximized EMS and pre-EMS log likelihoods are −1,969.969 and −2,032.052. Dividing instead at October 1979, when U.S. monetary operating procedures changed, gives −2,134.305 and −1,887.265. Twice the difference between the sums is 39.098 in favor of the March split. These are nonnested break specifications, so this difference is evidence from comparative fit, not automatically a conventional chi-square LR test.

A separate test of one constant parameter vector over the entire twelve years against a March 1979 break gives LR 388.110, evaluated against chi-square 30. That establishes strong evidence against the pooled constant-parameter specification under the paper's framework. It does not identify the EMS as the sole cause or estimate an optimal break date. The source explicitly leaves formal break-date analysis for later research.

To reconstruct the study, assemble the Wednesday panel, reproduce the two exact subperiod counts, use the common currency ordering, jointly fit the 30-parameter model in each period, retain the pre-EMS nonstationary-in-second-moment Italian solution if reproducing the original estimates, and calculate standardized residual and cross-product diagnostics. Record initialization, numerical constraints, convergence, quotation direction, and standard-error method as additional implementation choices because the paper does not specify them fully. The comparison should preserve identical data treatment across regimes and across dollar and yen numeraires.

The enduring contribution is an economical covariance architecture and its likelihood treatment. The empirical result shows how it separates stronger cross-currency coherence from higher marginal volatility. Its principal limitation is equally clear: constant conditional correlation is a restriction to assess, not a structural law. No result in the article guarantees that the same restriction will support accurate portfolio tail risk, asset pricing, or forecasting outside the historical weekly exchange-rate samples.
