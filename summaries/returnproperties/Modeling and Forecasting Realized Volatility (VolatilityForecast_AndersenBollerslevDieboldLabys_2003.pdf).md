# Modeling and Forecasting Realized Volatility

**Torben G. Andersen, Tim Bollerslev, Francis X. Diebold, and Paul Labys (2003).** *Econometrica* 71(2), 579–625. Source: [original PDF](../../Finance/VolatilityForecast_AndersenBollerslevDieboldLabys_2003.pdf). The supplied 47-page article was inspected in full, including proofs, tables, figures, and footnotes. Its separately hosted supplemental appendix is referenced but is not included in this file. Page numbers below are printed journal pages.

## Why this matters and what is new

A daily return supplies a poor observation of that day's volatility: a quiet close-to-close return can conceal substantial intraday movement. This paper separates measuring past variation from forecasting future variation. It constructs daily realized covariance matrices from intraday returns, models their dynamics using ordinary time-series methods, and uses the resulting volatility distribution to forecast returns and tail probabilities. The innovation is an integrated measurement, forecasting, and density-evaluation framework grounded in quadratic variation, rather than a new recursion driven only by daily squared returns.

The empirical application concerns Deutschemark/dollar, yen/dollar, and the implied yen/Deutschemark exchange rate. A fractionally integrated vector autoregression for realized log standard deviations competes with daily and intraday GARCH-type models. Its central advantage is the information in the measured state. Long-memory dynamics help, but replacing daily absolute returns with intraday-based realized measures while retaining the same forecasting architecture produces a large improvement. The multivariate component contributes much less than this change of measurement.

The distinction between an ex-post observation and an ex-ante forecast is essential. Today's realized variance is available after today's intraday returns have occurred. It cannot be used as today's advance risk forecast. It can improve tomorrow's forecast by revealing today's volatility more accurately. Similarly, approximate normality of returns divided by their contemporaneous realized standard deviations does not imply normality conditional on yesterday's information: tomorrow's realized variance is still random, producing a non-Gaussian mixture.

## Quadratic variation and conditional risk

Section 2 works with an arbitrage-free vector log-price process on a filtered probability space. Under its integrability assumptions, the process has a special-semimartingale decomposition

$$
p_t=p_0+A_t+M_t,
$$

where $A$ is predictable finite variation and $M$ is a local martingale, both initially zero. Additional square integrability is imposed for conditional covariance results. The continuous and jump components are distinguished. An exactly predictable jump in the finite-variation component cannot create a riskless gain: a simultaneous martingale jump must be able to overturn its sign with positive probability. The commonly used case has a continuous finite-variation drift and potentially unanticipated jumps in the martingale.

For a partition with mesh tending to zero, sums of return outer products converge in probability, uniformly over compact time intervals, to quadratic covariation:

$$
\sum_j(p_{t_j}-p_{t_{j-1}})(p_{t_j}-p_{t_{j-1}})'
\longrightarrow [p,p]_t.
$$

This is a pathwise variability object, not the square of the total period return. With continuous $A$,

$$
[p,p]_t=[M^c,M^c]_t+\sum_{s\le t}\Delta M_s\Delta M_s'.
$$

Thus jumps contribute squared jump sizes to diagonal elements; simultaneous jumps contribute cross-products to covariances. Continuous drift has zero quadratic variation. This general measurement result permits jumps even though the later normal-mixture distributional result does not.

Theorem 1, equation (5), states the exact relationship between conditional return covariance and expected quadratic variation. Write $\Delta_h A=A_{t+h}-A_t$, $\Delta_h M=M_{t+h}-M_t$, and $\Gamma_A=\operatorname{Var}_t(\Delta_h A)$. Then

$$
\operatorname{Var}_t(p_{t+h}-p_t)
=E_t\{[p,p]_{t+h}-[p,p]_t\}
+\Gamma_A+\Gamma_{AM}+\Gamma_{AM}',
$$

where $\Gamma_{AM}=E_t[A_{t+h}(\Delta_h M)']=\operatorname{Cov}_t(\Delta_h A,\Delta_h M)$. The second equality uses the martingale property and measurability of $A_t$. The proof decomposes the return, identifies its drift and martingale covariances, and applies the martingale quadratic-variation identity. Off-diagonal identities follow by polarization of the variances of sums of martingales.

If the drift increment is conditionally independent of martingale innovations, the cross terms vanish. If its path over the forecast interval is already determined by time-$t$ information, its variance vanishes too, leaving

$$
\operatorname{Var}_t(p_{t+h}-p_t)
=E_t\{[p,p]_{t+h}-[p,p]_t\}.
$$

This is not a universal identity with no drift restrictions. The paper argues that the extra terms are small at daily or weekly horizons: under regular local scaling, drift variance is order $h^2$, martingale variance order $h$, and the covariance is bounded at order $h^{3/2}$. Its numerical illustration contrasts a 1% daily standard deviation with a 0.1% daily mean: the squared mean is only one hundredth of variance. These arguments justify approximation in the intended application; they do not establish a uniform bound for arbitrary drift processes or long horizons.

## When the normal-mixture interpretation is valid

For continuous sample paths, the paper writes

$$
dp_s=\mu_s\,ds+\sigma_s\,dW_s,
\qquad \Omega_s=\sigma_s\sigma_s',
$$

so that quadratic variation over $[t,t+h]$ is integrated covariance $\int_t^{t+h}\Omega_sds$. Theorem 2 additionally assumes that the within-period drift and volatility paths are independent of the Brownian innovation process over that interval. Conditional on those paths,

$$
p_{t+h}-p_t\mid\{\mu_s,\sigma_s\}_{s=t}^{t+h}
\sim N\left(\int_t^{t+h}\mu_sds,\int_t^{t+h}\Omega_sds\right).
$$

Given the paths, the stochastic integral is a Gaussian vector with its covariance determined by the integrated loadings. One must not use a random time-change argument to claim this conditional normality without the independence condition. A stochastic time change can itself depend on the driving Brownian path.

The authors use negligible short-horizon drift and approximately lognormal realized volatility to motivate a lognormal-normal mixture. This distributional step is stronger than the quadratic-variation measurement theorem. Contemporaneous return-volatility dependence, leverage, or price jumps can invalidate the exact mixture representation even when realized variance remains a useful risk measure. Lagged return effects on later volatility are compatible with the framework. Its empirical diagnostics assess whether the stronger approximation is adequate for these currencies, rather than prove it for all assets.

Table I illustrates the distinction. Raw daily DM/dollar and yen/dollar returns have kurtoses 5.28 and 6.64, whereas returns standardized by realized volatility have kurtoses 2.57 and 2.66. The equally weighted portfolio's kurtosis falls from 5.81 to 2.61. These are near-Gaussian, somewhat platykurtic results, not exact normality. Raw squared returns show marked serial dependence, while standardized squared returns largely do not. The daily return standard deviations are approximately 0.700% and 0.692% in the estimation sample.

## Data and construction of the measured state

The raw data are all indicative interbank DM/dollar and yen/dollar bid-ask quotes displayed on Reuters FXFX from December 1, 1986 through June 30, 1999, supplied by Olsen & Associates. They contain several million observations, averaging roughly 4,500 quotes per day for the mark and 2,000 for the yen. Indicative quotes are not executable transactions. Strategic quoting, stale quotes, and spread conventions can affect very short return intervals.

The chosen sampling interval is thirty minutes. Preliminary microstructure analysis motivates this balance between more observations and contamination at higher frequencies. For each half-hour timestamp, the authors linearly interpolate the logarithmic average of bid and ask quotes from the immediately preceding and following ticks, then difference these log prices. Interpolation uses the surrounding ticks to measure an historical interval; it is not a rule for placing a trade at a price known before the following tick arrives. The article does not list every quote-screening threshold or discarded holiday.

Returns are expressed in the market convention of domestic currency per dollar, with the cross rate yen per Deutschemark. Exclude Friday 21:00 GMT through Sunday 21:00 GMT and specified inactive holiday periods. Each retained full trading day supplies 48 half-hour returns. The resulting panel has 3,045 days, divided into 2,449 estimation days, December 1, 1986–December 1, 1996, and 596 evaluation days, December 2, 1996–June 30, 1999. Preserve the authors' trading calendar rather than applying modern weekday counts to these totals.

Let $x_{tj}$ be the two-dimensional half-hour return on day $t$. The realized covariance matrix is

$$
V_t=\sum_{j=1}^{48}x_{tj}x_{tj}'=R_t'R_t.
$$

No demeaning or division by 48 is used: the target is total daily quadratic variation. For a multiday interval, sum the corresponding daily matrices. The matrix is positive semidefinite by construction and positive definite if the two return columns are linearly independent. Generally, with 48 intraday observations, more than 48 asset columns cannot yield a full-rank daily matrix. Even below that limit, synchronization, stale prices, and numerical near-collinearity matter.

The three variance series used in forecasting are $v_{t1}$ for DM/dollar, $v_{t2}$ for yen/dollar, and $v_{t3}$ for the implied yen/DM cross rate. Triangular consistency gives cross-rate returns $x_{tj,2}-x_{tj,1}$ and

$$
v_{t3}=v_{t1}+v_{t2}-2v_{t12},
\qquad v_{t12}=\frac{v_{t1}+v_{t2}-v_{t3}}2.
$$

This allows all modeled coordinates to be positive variances, whose logarithms are convenient. It does not mean three independent currency risks exist: there are two underlying return coordinates. For a half-and-half portfolio the realized variance is $v_{t1}/2+v_{t2}/2-v_{t3}/4$. Use this covariance-aware expression, not the average of individual standard deviations.

## Fractional dynamics and estimation

Define log realized standard deviation, not log variance, as $y_{ti}=\tfrac12\log v_{ti}$. Table II reports means of −0.554, −0.572, and −0.637 and standard deviations 0.405, 0.419, and 0.388, with returns measured in percent. Changing to decimal returns shifts the intercepts but not dynamic coefficients. Log-volatility kurtoses are 3.29, 3.44, and 3.04, much closer to Gaussian values than the level-volatility distributions.

The Geweke–Porter-Hudak log-periodogram estimates of fractional integration are 0.387, 0.413, and 0.430. The calculation uses the lowest $m=\lfloor T^{4/5}\rfloor=514$ frequencies; the reported asymptotic standard error is $\pi/\sqrt{24m}=0.028$. A multivariate restriction produces common $d=0.401$ and reported equality-test $p=0.510$. Separate residual-based checks give fractional orders 0.356, 0.424, and 0.393 after projecting each series on the others, providing no persuasive evidence of fractional cointegration. Those checks are heuristic, as the paper acknowledges.

The forecasting model, equation (15), is

$$
\Phi(L)(1-L)^{0.401}(y_t-\mu)=\epsilon_t,
\qquad \Phi(L)=I-\Phi_1L-\cdots-\Phi_5L^5.
$$

Fit the fractionally differenced series with an unrestricted trivariate VAR(5), by OLS equation by equation. Innovations are modeled as jointly Gaussian white noise for density forecasting. Five lags cover one trading week; both AIC and BIC favor one lag, but the authors choose five conservatively. No signed returns, interest differentials, or activity covariates enter the maintained model. The estimated VAR roots lie outside the unit circle and residual portmanteau tests do not reject whiteness.

For implementation, the fractional filter can be computed recursively: $a_0=1$, $a_k=a_{k-1}(k-1-d)/k$, with $(1-L)^d=\sum_{k\ge0}a_kL^k$. This is an algebraic implementation of the reported model, not a supplied software routine. Its truncation, presample values, mean treatment, and startup discard must be documented because they affect finite-sample matches. The paper does not print the complete fitted coefficient matrices, filter truncation, or numerical initialization settings.

Forecast the transformed VAR recursively, invert the fractional filter using the observed past and forecast future terms, and recover log-volatility forecasts. A Gaussian forecast $y_{t+h,i}\sim N(m_{h,i},s_{h,i}^2)$ implies mean variance $E_t[v_{t+h,i}]=\exp(2m_{h,i}+2s_{h,i}^2)$ and mean standard deviation $E_t[\sqrt{v_{t+h,i}}]=\exp(m_{h,i}+s_{h,i}^2/2)$. These identities make the transformation bias explicit. Simply exponentiating a log forecast yields a median, and taking the square root of mean variance yields a different quantity. Footnote 34 says Taylor bias adjustments yield almost identical reported forecast regressions; it does not make the transformations mathematically interchangeable.

A second implementation issue is covariance validity. Arbitrary forecasts of three positive variances do not automatically satisfy the triangle restrictions needed for the recovered two-by-two matrix to be positive definite. A simulation-based density implementation must check this. The article's final discussion proposes modeling Cholesky factors to guarantee positive definiteness more generally, but that is a proposed extension rather than the fitted model in the tables. Projecting invalid matrices or truncating Gaussian draws would be an additional rule that must be disclosed.

## Forecast experiment and comparators

All model parameters in the reported comparison tables are estimated using the 2,449-day initial sample; the out-of-sample period updates observed inputs while keeping those estimates fixed. In-sample forecast evaluation begins December 1, 1987 and uses 2,223 observations after startup. That exercise uses parameters estimated through 1996 and is explicitly in-sample. The held-out 596-day experiment is the relevant genuine forecast test. One paragraph's repeated “1996” start year for GARCH conflicts with the clearly specified 1986–1996 estimation interval in the data section and every table caption; use the latter.

The comparators isolate different sources of improvement:

- VAR-ABS uses the same long-memory VAR architecture on daily log absolute returns, replacing the intraday realized proxy.
- AR-RV uses separate fifth-order autoregressions for the fractionally differenced realized series, removing cross-series predictive interactions.
- Daily GARCH(1,1) is estimated by quasi-maximum likelihood. Reported persistence parameters are 0.986, 0.968, and 0.990.
- RiskMetrics uses exponentially weighted daily return cross-products with decay 0.94, equivalent to a zero-intercept integrated GARCH filter.
- Daily FIEGARCH(1,$d$,0) allows stationary long memory in log conditional variance.
- Intraday FIEGARCH is fitted after dividing each half-hour return by its interval's sample root-mean-square return and applying an AR(1) filter to reduce microstructure-induced autocorrelation.

For intraday deseasonalization, estimate $s_j^2=T^{-1}\sum_t x_{tj}^2$ and use $x_{tj}/s_j$. The sampling frequency, seasonal adjustment, and serial-correlation filtering are integral parts of this comparator. The article does not reproduce all FIEGARCH estimates, optimizers, or convergence tolerances. Its referenced supplemental appendix contains further specifications and sensitivity cases, which cannot be reconstructed from the current PDF alone.

The main evaluation regresses realized standard deviation on an intercept and one or two forecasts. At one day,

$$
\sqrt{v_{t+1,i}}=b_0+b_1\widehat s^{RV}_{t+1|t,i}
+b_2\widehat s^{other}_{t+1|t,i}+u_{t+1,i}.
$$

Ten-day evaluation replaces the dependent variable by $\sqrt{\sum_{j=1}^{10}v_{t+j,i}}$ and sums forecast variances before taking their square root. It does not sum daily standard deviations. Overlapping ten-day outcomes use heteroskedasticity and serial-correlation robust errors through lag nine, with unweighted covariance sums. One-day regressions use heteroskedasticity-robust errors. The authors warn that these conventional standard errors omit model-parameter estimation uncertainty and may be too small.

The regression $R^2$ measures ex-post explanatory association after a fitted calibration line. It is not an out-of-sample MSPE reduction against a historical mean and is not sufficient by itself to establish forecast dominance under every loss. Intercept zero and slope one, as well as incremental forecast coefficients, are separate diagnostics.

## Numerical findings and their boundaries

The following entries are single-forecast regression $R^2$ values from Tables III.B and III.D, without claiming every ranking is favorable to VAR-RV.

| Model | One-day DM/dollar | One-day yen/dollar | One-day yen/DM | Ten-day DM/dollar | Ten-day yen/dollar | Ten-day yen/DM |
|---|---:|---:|---:|---:|---:|---:|
| VAR-RV | .249 | .329 | .355 | .197 | .278 | .293 |
| VAR-ABS | .028 | .115 | .119 | .011 | .183 | .215 |
| AR-RV | .246 | .338 | .344 | .195 | .279 | .293 |
| Daily GARCH | .096 | .297 | .300 | .082 | .263 | .328 |
| RiskMetrics | .097 | .266 | .286 | .056 | .211 | .299 |
| Daily FIEGARCH | .037 | .373 | .263 | .013 | .218 | .244 |
| Intraday FIEGARCH | .266 | .380 | .404 | .152 | .228 | .225 |

Intraday FIEGARCH exceeds VAR-RV in one-day $R^2$ for all three currencies, and daily GARCH exceeds it for ten-day yen/DM. The favorable conclusion is therefore systematic competitiveness, parsimony, and calibration, not universal numerical superiority. VAR-ABS's poor performance is strong evidence for improved volatility measurement. AR-RV's near equality shows that cross-variable lag coefficients provide limited extra value.

For one-day VAR-RV forecasts, the DM/dollar calibration intercept is 0.021 with standard error 0.049 and slope 0.987 with standard error 0.092. Yen/dollar has intercept −0.006, standard error 0.110, and slope 1.085, standard error 0.151. Yen/DM has intercept −0.047, standard error 0.101, and slope 1.146, standard error 0.143. These are compatible with the reference calibration. By comparison, intraday FIEGARCH's yen/DM slope is 1.455 with standard error 0.217 and intercept −0.231 with standard error 0.150: higher correlation need not mean correctly scaled forecasts.

The in-sample long-memory component explains roughly half of log-volatility variation; the subsequent VAR explains only about 2% of the remaining variation. Small marginal explanatory power does not mean the VAR is unnecessary: it removes residual serial dependence and captures modest cross-rate predictability. Figure 6's selected episodes illustrate better assessment of the current level and subsequent mean reversion. They are illustrations, not a separately randomized or comprehensive performance test.


## Explicit forecast recursion and density construction

The fitted model can be implemented without treating fractional differencing as a black box. The following equations are an algebraic reconstruction of equation (15), not an additional empirical specification. Let $z_t=(1-L)^d(y_t-\mu)$ and let $\widehat\Sigma_\epsilon$ be the VAR residual covariance. At forecast origin $t$, form future transformed forecasts recursively as $\widehat z_{t+h|t}=\sum_{k=1}^{5}\widehat\Phi_k\widetilde z_{t+h-k}$, where $\widetilde z_s$ is observed when $s\le t$ and forecast otherwise. This separation ensures that the recursion never reads a transformed future observation.

The inverse fractional coefficients satisfy $c_0=1$ and $c_j=c_{j-1}(j-1+d)/j$. Therefore $y_s-\mu=\sum_{j\ge0}c_jz_{s-j}$. At each future date, split this sum into terms with observed $z$ and terms with forecast $z$. The slowly decaying coefficients explain why presample and truncation choices can matter even when the VAR itself has only five lags. Re-estimating the mean using the held-out sample would change the forecasting experiment; retain the estimation-sample mean throughout.

Forecast uncertainty requires propagation through both filters. Let $\Psi_0=I$ and $\Psi_j=\sum_{k=1}^{\min(5,j)}\Phi_k\Psi_{j-k}$ be the VAR impulse-response matrices, and define $G_j=\sum_{l=0}^jc_l\Psi_{j-l}$. Conditional on fixed estimated parameters, the log-volatility forecast-error covariance at horizon $h$ is

$$
\Sigma_y(h)=\sum_{j=0}^{h-1}G_j\Sigma_\epsilon G_j'.
$$

For two horizons $h$ and $k$, the cross-covariance is

$$
\operatorname{Cov}_t(y_{t+h}-\widehat y_{t+h|t},y_{t+k}-\widehat y_{t+k|t})
=\sum_{l=1}^{\min(h,k)}G_{h-l}\Sigma_\epsilon G_{k-l}'.
$$

These expressions are useful for reconstructing the joint future volatility path. Simulating each horizon independently would discard this dependence, giving the wrong distribution for a ten-day sum even if every individual day's marginal variance were correct. The same caveat applies to simulating each currency independently: residual covariance and lagged cross-effects both enter portfolio risk.

For a single currency and one-day horizon, the mixture CDF has a particularly direct expression. If log standard deviation is conditionally $N(m,s^2)$, then

$$
F_t(x)=\int_{-\infty}^{\infty}\Phi(xe^{-y})\frac{1}{s}\phi\!\left(\frac{y-m}{s}\right)dy,
$$

where $\Phi$ and $\phi$ are standard normal CDF and density. Quadrature over a standard-normal variable, $y=m+sz$, avoids numerical problems from integrating over very large or very small variance levels. With $s=0$ this reduces exactly to a normal CDF with standard deviation $e^m$, providing a useful unit test. A nonzero return-mean forecast would enter by replacing $x$ with its deviation from that mean.

For portfolios, generate joint log-variance draws, exponentiate, recover the currency covariance, and calculate $w'Vw$ before integrating the conditional Gaussian return distribution. Check covariance admissibility on every draw. The issue is structural: positivity of three scalar variances does not guarantee a valid covariance triangle. Any rejection, projection, or constrained-factor alternative changes the predictive distribution and must be recorded. These procedures give a transparent reconstruction of the model's forecast objects; they do not supply the missing numerical choices or reproduce unpublished supplemental results by assumption.

## Return densities, quantiles, and practical reproduction

For a univariate return with negligible conditional mean, a concrete implementation of the proposed mixture is to integrate $N(0,e^{2y})$ over the conditional Gaussian distribution of future log standard deviation. This integrates variance uncertainty rather than substituting its expectation into a single normal density. Portfolio density calculations additionally require the joint covariance distribution and consistent cross-rate reconstruction. Numerical quadrature or Monte Carlo would implement the integration, but the article does not provide enough numerical settings to claim one unique replication algorithm.

For each realized return, evaluate the predictive CDF to obtain $z_t=F_{t|t-1}(r_t)$. A correctly specified continuous conditional density implies iid uniform probability integral transforms. Uniformity tests marginal coverage; autocorrelations of centered $z_t$ and its square test selected forms of temporal misspecification. Neither a visually uniform histogram nor nonrejection in a small tail sample proves the entire conditional density correct.

Table IV reports out-of-sample lower-tail exceedance fractions. At nominal 1% and 5%, DM/dollar gives 0.5% and 4.5%, yen/dollar 1.9% and 5.5%, and the equal-weight portfolio 1.0% and 4.2%. At the nominal 99th percentile the empirical CDF values are 99.0%, 99.3%, and 100.0%, respectively. The portfolio therefore has no observed upper-1% exceedance in this sample. These are broadly useful calibration results with noticeable finite-sample variation, not exact quantile matching. Figure 7 and reported Ljung–Box tests detect no relevant serial dependence in the displayed PIT diagnostics.

A lognormal distribution is not closed under summation, so a multiday variance assembled from daily lognormals is not itself exactly lognormal. The paper reports similar supplemental results with inverse-Gaussian mixtures but does not supply that appendix here. A modern reproduction should simulate the joint daily volatility path for multiday density forecasts rather than silently impose aggregation identities that the lognormal model lacks.

To reconstruct the study, first reconcile quote cleaning, half-hour interpolation, trading-day boundaries, exclusions, and the 3,045-day count. Verify realized-matrix identities and Table I–II moments. Then fix the estimation/evaluation split, reproduce fractional filtering and VAR residual diagnostics, and compare fixed-parameter forecasts with identical information cutoffs. Evaluate levels, calibration, and encompassing results before density tails. Preserve any unresolved holiday list, initialization, coefficient, or quadrature choice in the replication record. The paper establishes the value of high-frequency information for lower-frequency risk measurement and prediction; it does not supply a tradable strategy, transaction-cost model, or a blanket guarantee that the same normal-mixture approximation works for equity leverage and jump risks.
