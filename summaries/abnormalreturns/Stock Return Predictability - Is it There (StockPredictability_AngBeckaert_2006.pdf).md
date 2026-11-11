# Stock Return Predictability: Is it There?

**Authors:** Andrew Ang and Geert Bekaert. **Source:** *Review of Financial Studies* 20(3), 2007, pp. 651–707; advance publication July 6, 2006. DOI: 10.1093/rfs/hhl021. **Original file:** `Finance/StockPredictability_AngBeckaert_2006.pdf`. Page references below use journal pagination; the first PDF page is journal page 651.

## Research question and contribution

This paper asks which familiar valuation signals actually predict stock returns once inference, sample dependence, cash-flow predictability, and the distinction between short and long horizons are treated together. Its principal result is that the short interest rate and dividend yield jointly predict excess stock returns at short horizons, while evidence for long-horizon predictability is substantially weaker. A high dividend yield is more informative after controlling for the short rate. The short rate enters negatively: a higher rate forecasts a lower subsequent equity premium. Dividend yields alone do not provide a robust, universal long-horizon forecasting relation.

The innovation is methodological and economic. First, the authors compare overlapping-return standard errors and show through simulations that commonly used alternatives can reject a no-predictability null far too often. Second, they estimate comparable models in several countries and test restrictions that pool information internationally. Third, they construct an exact nonlinear present-value model, with stochastic discount rates, interest rates, and dividend growth, that reproduces much of the observed behavior. This supplies a coherent environment in which to examine test size, power, small-sample bias, and the economic sources of valuation variation.

The paper also separates the forecasting of returns from forecasting dividends, earnings, and interest rates. A valuation ratio is an equilibrium outcome; interpreting it solely as an expected-return signal can obscure information about its numerator. Earnings yields contribute particularly useful information about subsequent cash flows when combined with dividend yields. The findings therefore do not establish that valuation is uninformative. They narrow down the horizons, conditioning variables, and economic outcomes for which the evidence is persuasive.

## Data construction and samples

The long US sample uses S&P Composite prices, total returns, dividend yields, and earnings yields from the *Security Price Index Record*, June 1935 through December 2001. Comparable UK FT Actuaries and German CDAX observations run from June 1953 through December 2001 and come from Global Financial Data. These experiments use quarterly observations and three-month Treasury bill rates. The authors separately examine US samples beginning in 1952, after the Treasury–Federal Reserve Accord, and ending in 1990, before the unusually low dividend yields of the late 1990s. These sample changes materially affect significance and are part of the substantive evidence.

A second dataset contains monthly MSCI indices for the US, UK, France, and Germany from February 1975 through December 2001. Prices, total returns, dividend yields, and earnings yields are in local currency; short rates are one-month EURO rates obtained from Datastream. The international exercise is consequently a comparison of domestic equity premia, not a test of dollar-converted returns or an implementable currency-hedged global strategy. The quarterly and monthly samples differ in provider, frequency, coverage, and rate instrument, so their differences should not be attributed to frequency alone.

Returns are continuously compounded. Dividend and earnings predictors are logarithms of trailing-year payouts divided by price. For quarterly data, let

$$
D_t^4=\sum_{j=0}^{3}D_{t-j}.
$$

The observed dividend-growth series is growth in this rolling annual dividend total:

$$
g_t^{d,4}=\log\left[\frac{D_t^4/P_t}{D_{t-1}^4/P_{t-1}}\frac{P_t}{P_{t-1}}\right].
$$

The monthly construction uses twelve months. This smooths seasonality, but it also creates dependence between adjacent growth observations. A quarterly change in a trailing-year total must not be treated as growth in dividends paid during one isolated quarter. The distinction becomes essential when the structural model is estimated from latent quarterly dividend growth.

Table 1 documents the persistence that makes inference difficult. In the long US sample, annualized mean excess returns are 7.49%, return volatility is 16.84%, the average short rate is 4.09%, and average dividend and earnings yields are 4.03% and 7.68%. The first-order autocorrelations of US dividend yields and short rates are approximately 0.9504 and 0.9548. Annual dividend-growth volatility is 6.58%, compared with 15.72% for earnings growth. UK and German dividends are substantially more volatile, despite broadly comparable return variability. International pooling therefore adds information but imposes potentially consequential economic restrictions.

Phillips–Perron and KPSS tests are both reported. For US valuation yields, neither a unit-root null nor a stationarity null is decisively rejected in the relevant tests. This is weak discrimination, not evidence that both models are true or that stationarity has been established. UK and German yields provide clearer evidence of stationarity. In the shorter dataset, large French earnings-growth observations around May 1983–May 1984 inflate measured volatility: excluding them reduces the estimate from 58.68% to about 33%. This is one reason to inspect cash-flow construction and outliers rather than treating international earnings measurements as homogeneous.

## Predictive regressions and overlapping-horizon inference

For a horizon of $k$ observations, define the annualized average log excess return

$$
\widetilde y_{t+k}=\frac{h}{k}\sum_{j=1}^{k}(y_{t+j}-r_{t+j-1}),
$$

where $h=4$ for quarterly observations and $h=12$ for monthly observations. The regression is

$$
\widetilde y_{t+k}=\alpha_k+\beta_k'z_t+\epsilon_{t+k,k},
$$

with $z_t$ containing log dividend yield, the annualized short rate, or additional log earnings yield. Scaling the dependent variable and interest rate consistently is necessary to reproduce reported coefficients. The authors examine individual horizons and joint restrictions across one quarter, one year, and five years, or one month, one year, and five years.

Overlapping observations cause adjacent $k$-period residuals to share underlying returns. Under a null of no predictability and serially uncorrelated one-period innovations, that produces an MA($k-1$) error structure. Ordinary regression standard errors are consequently inappropriate. The paper compares Newey–West, robust Hansen–Hodrick, and Hodrick's 1992 covariance estimator. Newey–West calculations use $k+1$ lags. The robust Hansen–Hodrick construction uses the overlap window; its non-positive-semidefinite cases require a specified fallback, described in Appendix A. These implementation decisions are part of the experiment rather than interchangeable labels for a generic robust standard error.

Hodrick's estimator reorganizes the covariance calculation around one-period innovations and sums of lagged regressors. With $x_t=(1,z_t')'$, write $Z=E[x_tx_t']$. The covariance of the asymptotic distribution of $\sqrt{T}(\widehat\theta-\theta)$ is

$$
Z^{-1}SZ^{-1}.
$$

A core building block, suppressing the annualization adjustment, is

$$
w_{t,k}=\epsilon_{t+1,1}\sum_{i=0}^{k-1}x_{t-i},\qquad
\widehat S=\frac{1}{T}\sum_t w_{t,k}w_{t,k}'.
$$

The method estimates the overlap covariance through backward sums of predictors multiplied by one-step innovations, rather than directly estimating a long sequence of noisy autocovariances of overlapping residuals. Annualization factors must be restored in an actual implementation. Hodrick and robust Hansen–Hodrick coincide at the one-period horizon. The attractive size properties demonstrated here concern the maintained return null; they do not authorize the same calculation for any forecasting equation with persistently autocorrelated one-step errors.

Joint horizon tests stack the relevant regression moments and include their cross-horizon covariances. International pooling allows country-specific intercepts but imposes common predictor slopes. Its covariance accounts for contemporaneous cross-country dependence. Overidentification tests assess whether these slope restrictions are consistent with the data; rejection is a warning that a precise pooled coefficient may summarize incompatible country relationships. With $N$ countries and $K$ coefficients including the intercept, the number of slope restrictions is $(N-1)(K-1)$.

## Return forecasting results

Table 2 makes clear why a broad claim about dividend yields requires qualification. In the full 1935–2001 US sample, univariate dividend-yield slopes are 0.1028 at one quarter, 0.1128 at one year, and 0.1028 at five years. Their Hodrick $t$-statistics are 1.824, 2.030, and 1.364. A joint test across horizons has a $p$-value of 0.587. Ending the sample in 1990 instead produces a joint $p$-value of 0.014. The striking change is evidence of sample sensitivity, even though the predictor's economic sign remains familiar.

The short rate changes the picture most clearly at short horizons. In the 1952–2001 US sample, the one-quarter bivariate regression has a short-rate coefficient of −2.1623, with $t=-2.912$, and a dividend-yield coefficient of 0.1362, with $t=2.152$. Joint significance has $p=0.003$. Holding log dividend yield fixed, a one-percentage-point increase in the annualized short rate corresponds to roughly a 2.16-percentage-point reduction in the forecast annualized premium over the next quarter. This is a conditional regression interpretation, not an identified causal effect of monetary policy.

At one year the corresponding short-rate and dividend-yield coefficients are −1.4433 and 0.1313, and the joint $p$-value is 0.041. At five years the coefficients are −0.4829 and 0.0774, and joint significance disappears, with $p=0.714$. The effect of the short rate decays more rapidly with horizon than a simple one-factor persistent-rate story would suggest. That motivates a model with more than one state variable driving discount rates.

The shorter monthly US sample gives a related pattern. At one month, the bivariate short-rate coefficient is −2.4358, with $t=-2.388$, while the dividend-yield coefficient is 0.1364, with $t=1.626$; joint $p=0.057$. At five years, the joint $p$-value is 0.857. Replacing the short rate by a detrended rate and accommodating the October 1979–October 1982 monetary-policy episode do not eliminate the basic short-horizon finding. However, these checks do not convert a predictive association into a stable real-time policy rule.

Table 3 supplies international evidence. Pooling the US, UK, and Germany over 1953–2001 yields a one-quarter short-rate coefficient of −1.958 and dividend-yield coefficient of 0.1600, with $t$-statistics −2.927 and 2.626. Joint $p=0.001$, and the pooling overidentification $p$-value of 0.133 does not reject common slopes. Joint significance remains at one year, with $p=0.008$, and disappears at five years, with $p=0.637$.

The four-country monthly dataset is less clean. At one month, pooled coefficients are −1.8161 on the short rate and 0.1640 on dividend yield, with joint $p=0.031$. But the pooling test has $p=0.016$, rejecting equality of slopes across countries. At twelve and sixty months, joint $p$-values are 0.229 and 0.699. Thus the international data reinforce short-horizon information, while simultaneously showing that an identical forecasting rule across markets is too restrictive in some samples.

## Cash flows and interest rates

Dividend yields can move because expected returns change, because expected dividend growth changes, or because both change. Table 4 therefore predicts dividend growth separately. In the long US sample beginning in 1935, dividend yield does not forecast growth meaningfully. Beginning in 1952 produces positive univariate slopes: 0.0251 at one quarter, with $t=2.476$, and 0.0259 at one year, with $t=2.503$. This is the opposite of the simple intuition that a high dividend yield mechanically signals low future growth, and it is not robust across specifications or markets.

Adding the short rate to the 1952–2001 US quarterly regression gives a short-rate coefficient of 0.3541, with $t=2.191$, and dividend-yield coefficient of 0.0188, with $t=1.599$. Long-sample international pooling instead produces a strongly negative dividend-yield relation, but the equality restrictions are rejected at $p<0.001$. The monthly dataset supplies little robust dividend-growth predictability from dividend yield alone. These conflicting findings are a central reason the authors resist assigning a universal cash-flow interpretation to dividend yields.

Table 5 examines whether dividend yields forecast interest rates. Estimated signs are generally positive, but evidence is weak: the US 1952–2001 one-quarter coefficient is 0.0171, with $t=0.202$, while the short international pooled coefficient is 0.0594, with $t=1.525$. Because interest-rate forecast errors themselves are persistent, the one-step regressions use a Cochrane–Orcutt adjustment. The paper does not report standard errors at longer horizons where residual persistence and overlap jointly complicate inference. This deliberate distinction prevents the favorable return-regression covariance results from being applied outside their assumptions.

## Exact nonlinear present-value model

The structural contribution provides an economic laboratory for these empirical patterns. Let gross equity return be

$$
Y_{t+1}=\frac{P_{t+1}+D_{t+1}}{P_t},\qquad
\delta_t=\log E_t[Y_{t+1}].
$$

Under the maintained pricing relation and transversality condition, the price-dividend ratio satisfies the exact present-value representation

$$
\frac{P_t}{D_t}=E_t\left[\sum_{i=1}^{\infty}\exp\left(-\sum_{j=0}^{i-1}\delta_{t+j}+\sum_{j=1}^{i}g^d_{t+j}\right)\right].
$$

The model's cash-flow and interest-rate state is

$$
X_t=\begin{pmatrix}r_t\\g_t^d\end{pmatrix}
=\mu+\Phi X_{t-1}+\varepsilon_t,\qquad
\varepsilon_t\sim N(0,\Sigma).
$$

The log conditional expected gross return follows

$$
\delta_t=\alpha+\xi'X_t+\varphi\delta_{t-1}+u_t,\qquad
u_t\sim N(0,\sigma^2),
$$

with independent state and discount-rate innovations. This specification can produce risk-premium movements associated with observed states and additional persistent discount-rate variation. Because the valuation ratio and realized return are nonlinear functions of the states, an observable linear VAR is generally only an approximation. Conditional heteroskedasticity can arise endogenously even though primitive innovations are Gaussian with constant variances.

The price-dividend ratio has an exponential-affine series solution,

$$
\frac{P_t}{D_t}=\sum_{i=1}^{\infty}\exp(a_i+b_i'X_t+c_i\delta_t).
$$

Let $e_2=(0,1)'$ and $v_i=e_2+b_i+c_i\xi$. The coefficient recursions are

$$
a_{i+1}=a_i+c_i\alpha+\frac12c_i^2\sigma^2+v_i'\mu+\frac12v_i'\Sigma v_i,
$$

$$
b_{i+1}'=v_i'\Phi,\qquad c_{i+1}=\varphi c_i-1.
$$

Initial conditions are $a_1=e_2'\mu+e_2'\Sigma e_2/2$, $b_1'=e_2'\Phi$, and $c_1=-1$. These recursions are a reproducible alternative to a log-linear pricing approximation, subject to convergence and numerical truncation of the infinite sum.

Two null models and three alternatives isolate different sources of predictability. Null 1 holds total expected gross returns constant. Null 2 sets $\delta_t=\alpha+r_t$, making the conditional expectation of the scaled gross return $Y_{t+1}/\exp(r_t)$ equal to $\exp(\alpha)$. That is not identical to a constant expected log excess return: Jensen's inequality and state-dependent return variance matter. Nor is expected arithmetic excess return exactly constant, since it equals $\exp(r_t)[\exp(\alpha)-1]$. The definition of the null must therefore match the return transformation used in simulation.

Alternative 1 makes discount rates exogenous and persistent; Alternative 2 makes them a contemporaneous function of the short rate and dividend growth; Alternative 3 combines state dependence, persistence, and an independent shock. These are disciplined reduced-form specifications of expected returns, not a full consumption-based derivation of investor preferences or a monetary-policy model.

## Structural estimation and numerical replication

Appendix E describes simulated method of moments on US quarterly data from January 1952 through December 2001. Estimation proceeds in two stages. The first fits the short-rate and latent dividend-growth dynamics. The restriction $\Phi_{12}=0$ prevents dividend growth from Granger-causing the short rate. The short-rate AR(1) is estimated first. Remaining cash-flow parameters match the first two moments of observed rolling annual dividend growth and selected covariances with current and lagged rates and dividend growth. Four-quarter lags are used to avoid the mechanically induced dependence at the first three lags of rolling annual payouts. The weighting calculation uses Newey–West with four lags.

The estimated quarterly state parameters in Table 6 are approximately

$$
\mu=\begin{pmatrix}0.0010\\0.0053\end{pmatrix},\qquad
\Phi=\begin{pmatrix}0.9263&0\\-0.0078&0.5489\end{pmatrix},
$$

and the lower-triangular innovation loading matrix is

$$
\Sigma^{1/2}=\begin{pmatrix}0.0026&0\\0.0036&0.0171\end{pmatrix}.
$$

A replicator must simulate latent quarterly dividend payments and then reconstruct trailing annual dividends. Directly using observed rolling dividend growth as the latent state would change both persistence and shock variance. The fitted latent quarterly growth standard deviation is approximately 0.0173, compared with 0.0156 for the smoothed observed measure.

The second stage holds state parameters fixed and estimates discount-rate parameters using twelve moments. The observable vector contains log excess returns, the trailing annual dividend-price ratio, and their squares. These four outcomes are interacted with a constant, the lagged short rate, and lagged observed dividend growth. Estimation matches simulated and observed moments; the relevant equations are moment differences, not a literal claim that the raw positive squared moments equal zero.

Alternative 3 estimates $\alpha\approx-0.000988$, $\varphi=0.9298$, $\xi_r=0.0007$, $\xi_g=0.0014$, and $\sigma=0.005024$, all in quarterly units. Table 6 scales $\alpha$ and $\sigma$ by 100, which must be reversed before simulation. Alternative 1 estimates persistence 0.9816 and innovation standard deviation 0.001751. Alternative 2 assigns a much stronger negative coefficient, approximately −2.0454, to the short rate and a small dividend-growth coefficient of 0.0041.

Only Alternative 3 passes the reported overidentification assessment comfortably, with $p=0.1332$. Alternative 1 has $p=0.0101$, and both nulls and Alternative 2 are rejected at the reported precision. Population calculations use 100,000 simulated observations, while finite-sample experiments use 10,000 replications at sample lengths of 104, 200, or 267 quarters. The article does not supply a fully specified random seed, initialization, burn-in, and pricing-series truncation rule; those choices must be documented in any new reproduction. Expected cumulative log returns are approximated using simulated projections on fourth-order polynomials in the underlying states and discount rate.

## What the fitted model explains

Table 7 shows why constant discount-rate specifications are inadequate. The observed dividend-yield standard deviation is about 0.0114, compared with 0.0010 under Null 1 and 0.0031 under Null 2. Their return volatilities are also too low. Alternative 3 produces dividend-yield volatility 0.0115, excess-return volatility 0.0811 versus observed 0.0779, and dividend-yield autocorrelation 0.9596 versus observed 0.9548. Its quarterly mean excess return, 0.0068, is lower than the observed 0.0153; the latter has a standard error of 0.0057. Good matching of persistence and variances does not mean every mean or regression coefficient is matched exactly.

The model's variance exercise holds one state fixed at its mean, recomputes valuation variation, and measures the reduction relative to the unrestricted model. In Alternative 3, the reported contributions to price-dividend variation are 22.21% for the short rate, 6.89% for dividend growth, and 61.32% for the excess discount rate. The total discount-rate measure is 92.95%. These are overlapping counterfactual decompositions with covariance effects; the total-discount component contains interest-rate effects. They should not be presented as mutually independent variance shares or directly identified empirical causal percentages.

Adding the short rate improves how closely the linear forecast tracks the model's true conditional expected return. In Alternative 3, the correlation at one quarter rises from 0.7859 for the univariate dividend-yield forecast to 0.8654 for the bivariate forecast. At one year the figures are 0.7710 and 0.8297; at five years, 0.7976 and 0.8165. Table 8 also shows that matching unconditional moments does not force the empirical regression coefficients: the model's one-quarter bivariate short-rate slope is about −1.0737, against the sample estimate −2.1623. Structural plausibility should therefore be evaluated across moments and sampling uncertainty, not inferred from a single favorable fit.

## Finite-sample size, bias, and power

The simulation results are especially important for interpreting long-horizon significance. At a nominal 5% level with 104 quarterly observations, the univariate five-year test rejects 33.8% of the time using Newey–West and 37.3% using robust Hansen–Hodrick, compared with 4.7% using Hodrick. With 267 quarters, corresponding rates are 18.8%, 18.6%, and 3.9%. The false-positive problem remains substantial even in a long historical sample. At a one-quarter horizon all three methods are much closer to nominal size.

Hodrick inference is not uniformly exact. Some one-quarter bivariate tests are modestly oversized in short samples, while joint tests can be conservative: bivariate joint rejection rates across horizons are around 1.0–1.3% under a nominal 5% null. Consequently a nonrejection by such a joint test is not automatically strong evidence for the null. The paper appropriately studies power as well as size.

Small-sample bias also depends on the full nonlinear system. It is not generally valid to assume every dividend-yield coefficient has the familiar positive univariate bias. Under the scaled-return null, the 104-quarter bivariate short-rate and dividend-yield biases are approximately +0.3469 and −0.0339. With 267 quarters they are +0.1435 and −0.0264. These directions oppose the observed negative short-rate and positive dividend-yield slopes, so the observed bivariate relation cannot simply be dismissed using the usual single-predictor bias argument.

Size-adjusted power favors short horizons. Under Alternative 3 with 104 quarters, univariate dividend-yield power is 56.6% at one quarter and 15.9% at five years. Bivariate dividend-yield power is 62.8% and 19.8%, respectively. With 267 quarters, these rise to 95.9% and 62.0% univariately and 97.1% and 68.2% bivariately. Power to detect the short-rate coefficient remains lower—29.2% at one quarter in the 267-quarter experiment—so the results do not imply that all economically important coefficients can be estimated precisely.

Pooling increases power, but the simulation preserves dependence. It uses separate country state innovations and discount-rate shocks correlated at 0.80, generating equity-return correlation around 0.535. Four countries with 104 quarters produce approximately 73.9% power for the five-year univariate dividend-yield test and 76.7% for the corresponding bivariate coefficient, compared with much lower single-country values. These calculations explain why international evidence is useful. Their force is conditional on the calibrated cross-country structure and valid pooling restrictions; actual rejections of equal slopes cannot be ignored.

## Earnings, payout dynamics, and interpretation

Earnings yields add little robust return forecasting in Table 13. The positive dividend-yield and negative earnings-yield pattern associated with earlier payout-ratio work is strongest in the US sample ending in 1990. Once the short rate is included, its negative short-horizon coefficient remains the more stable finding. An isolated significant earnings-yield coefficient at a long horizon does not establish a successful joint model: for example, one short-sample pooled five-year coefficient has $t=-2.370$, while the joint predictor test has $p=0.321$.

Cash-flow results are more informative. In the 1935–2001 US one-quarter dividend-growth regression, dividend yield enters at −0.1897 and earnings yield at +0.2328, with $t$-statistics −2.724 and 3.175 and joint $p=0.002$. Adding the short rate gives coefficients −0.2694, +0.3132, and −0.9766 on dividend yield, earnings yield, and the rate, with joint $p=0.001$. The short international pooled monthly dividend-growth regression similarly has dividend-yield and earnings-yield coefficients −0.0792 and +0.0695, with joint $p=0.002$.

Earnings growth typically exhibits the opposite signs: a positive dividend-yield coefficient and negative earnings-yield coefficient. Because payout-ratio growth is dividend growth minus earnings growth, the combined findings connect valuation ratios to future payout adjustment. Dividend smoothing, earnings mean reversion, and common price movements are possible mechanisms. The paper does not identify one unique mechanism or estimate a complete structural model of earnings, dividends, and payout choice. Its two-state cash-flow model therefore explains less than the entire set of earnings results.

The authors also report a recursive post-1964 US forecasting exercise in which the bivariate model improves short-horizon root-mean-squared error relative to a historical-mean benchmark, but not long-horizon performance. This is corroborative rather than a fully documented trading result: the paper does not provide a comprehensive cost-aware portfolio backtest or enough numerical out-of-sample detail to reconstruct a claimed investment profit directly.

The actionable research implication is to condition valuation forecasts on interest rates, preserve the distinction between gross, arithmetic excess, and log excess returns, and treat long-horizon standard errors as a substantive modeling choice. A reproduction should compare countries individually before imposing pooled slopes, build trailing payouts consistently, and separate evidence about return forecasts from evidence about cash-flow forecasts. The structural variance decomposition and power experiments support these choices within a calibrated model. They do not establish that the estimated premium relation is invariant across later monetary regimes, payout policies, or market structures.
