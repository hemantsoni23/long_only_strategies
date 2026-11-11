# Realized Range Volatility Forecasting: Dynamic Features and Predictive Variables

Massimiliano Caporin and Gabriel G. Velo, *International Review of Economics & Finance* 40 (2015), 98–112; available online February 26, 2015. DOI: [10.1016/j.iref.2015.02.021](https://doi.org/10.1016/j.iref.2015.02.021).

Source: [VolatilityPrediction_CaporinVelo_2015.pdf](../../Finance/VolatilityPrediction_CaporinVelo_2015.pdf), all 15 PDF pages. Central references are Sections 2–5, Equations 8–15, and Tables 1–7. The paper refers to an additional appendix available from the authors or an earlier working-paper version; that appendix is not attached to this local PDF. The earlier SSRN download could not be retrieved during preparation of this note. Consequently, unreported coefficient tables and implementation settings have not been reconstructed from guesses.

## Why this matters and what the paper contributes

High-frequency data can improve daily volatility measurement, but better measurement alone does not settle the forecasting model. Daily volatility may react differently to negative returns, to unusually high recent volatility, and to economy-wide financial stress. A forecasting method can also have fat-tailed innovations and time-varying forecast uncertainty without necessarily producing better point forecasts.

The paper separates these issues in a common empirical design. It constructs a noise-corrected, jump-robust realized range measure, models its logarithm using heterogeneous autoregressive dynamics, adds return and volatility asymmetries, and then compares normal versus normal-inverse-Gaussian innovations and constant versus GARCH-type conditional error variance. Finally, it asks whether market, credit, and financial-system variables contribute beyond a stock's own volatility history.

Its innovation is this structured comparison and its evidence about which elements actually improve forecasts. The range estimator, HAR model, asymmetric GARCH recursion, and non-Gaussian density are drawn from prior literature. The main empirical lesson is that enriching the conditional mean with asymmetric responses and selected financial variables matters more for one-day point forecasts than making the residual distribution more elaborate. That is a useful model-building distinction: a better likelihood fit and a better point forecast need not select the same specification.

The results concern 16 selected U.S. equities and an evaluation period dominated by the financial crisis and its aftermath. They do not establish universal superiority for all stocks, all volatility targets, or all horizons. In particular, the logarithmic target and the distinction between integrated variance and jump variation should be retained when transferring the model to another application.

## The object being measured

Start with a continuous efficient log-price process

$$
dp_s=\mu_s\,ds+\sigma_s\,dW_s.
$$

Its daily integrated variance is $IV_t=\int_{t-1}^{t}\sigma_s^2ds$. A conventional realized variance, constructed from squared intraday returns, converges to this quantity under suitable ideal sampling assumptions. The associated limiting variance depends on integrated quarticity $IQ_t=\int_{t-1}^{t}\sigma_s^4ds$, with asymptotic scale $2IQ_t$ for the standard realized-variance estimator.

Range estimators exploit the high and low price within each intraday block. Let $S_{t,i}$ be the high-minus-low log-price range in block $i$, and let $\lambda_{2,m}$ be the second moment of the corresponding standardized Brownian range observed at $m$ grid points. The basic estimator is

$$
RRV_t=\frac1{\lambda_{2,m}}\sum_{i=1}^{n}S_{t,i}^{2}.
$$

Under the ideal continuous-price model, its asymptotic variance is a constant $\Lambda_m$ times integrated quarticity. The limiting constant approaches approximately 0.4 as within-block sampling becomes dense, compared with 2 for ordinary realized variance. This is an efficiency comparison under particular assumptions about the efficient price and observation scheme. Market microstructure noise and jumps can invalidate a naive use of the uncorrected formula.

The range moments depend on the exact sampling arrangement. A block's reported high and low, a range reconstructed from transaction prices, and a range calculated from sparsely sampled closing prices do not generally have identical finite-sample distributions. The theoretical normalization is therefore part of the data definition, not an arbitrary multiplicative constant to be absorbed casually into a forecast regression.

## Noise correction and jump robustness

The observed log price is modeled as an efficient price plus independent, identically distributed measurement noise with mean zero and variance $\omega^2$. At very high frequency, squared returns can be used to estimate the noise level through

$$
\widehat\omega^2=\frac{RV_N}{2N},
$$

where $N$ is the number of high-frequency return increments. The high-low range is inflated because maxima tend to contain positive noise and minima negative noise. The correction subtracts approximately twice the estimated noise standard deviation from each range.

With appropriately adjusted Brownian-range moments $\widetilde\lambda_{j,m}$, the noise-corrected range variance has the form

$$
RRV_t^{BC}=\frac1{\widetilde\lambda_{2,m}}
\sum_i(S_{t,i}-2\widehat\omega)^2.
$$

The paper's forecasting target is based on the noise-corrected bipower range estimator, which also removes the asymptotic contribution of isolated jumps:

$$
B_t=\frac1{\widetilde\lambda_{1,m}^{2}}
\sum_{i=1}^{n-1}
\left|S_{t,i}-2\widehat\omega\right|
\left|S_{t,i+1}-2\widehat\omega\right|.
$$

This is Equation 10 in the paper. Products of adjacent ranges play the role of bipower variation. The absolute values matter after noise correction: a corrected range can be negative even though the original range is nonnegative. Squaring every corrected range instead would produce a different estimator with different jump behavior.

The adjusted moments embody assumptions about the noise at extrema. The source refers to prior methodological work for their detailed construction. It does not provide all the simulation constants, random seeds, or exact grid settings needed to reproduce every daily estimate directly from the PDF. These omissions affect exact numerical replication, even though the structure of the estimator is clear.

A central conceptual qualification follows. A jump-robust bipower measure targets the continuous integrated-variance component, whereas the full quadratic variation of a jump process also includes squared jumps. The paper sometimes describes realized measures broadly as quadratic-variation estimators. For risk management, a forecast of the continuous component should not be presented as a complete forecast of jump-inclusive total risk without an additional jump model.

The correction also rests on a simple noise process. Serially correlated noise, price discreteness, changing bid-ask spreads, and irregular observation times can alter its behavior. The paper does not establish robustness to every such feature. A fresh implementation should inspect the proportion of negative corrected ranges and the stability of the final positive daily measure, while treating any truncation or alternative noise estimator as a documented departure from the published procedure.

## Sample and target transformation

The data comprise one-minute open, high, low, and closing prices from Tick Data for 16 NYSE stocks: BA, BAC, C, CAT, FDX, HON, HPQ, IBM, JPM, KFT, PEP, PG, T, TWX, TXN, and WFC. The period is January 5, 2004 through June 29, 2012, with 2,139 trading days. The intraday window is 9:30 a.m.–4 p.m. U.S. market time.

This is a selected, relatively small universe rather than a full-market panel with explicit historical membership rules. The paper does not fully document adjustment for all corporate actions, symbol changes, stale observations, missing minutes, or exceptional sessions. Those choices are particularly relevant for range measures because a single bad high or low can influence a day's estimate much more than an ordinary closing-price return.

The fitted response is

$$
h_t=\log B_t.
$$

Calling $h_t$ log volatility should not obscure the fact that the underlying range estimator is variance-like. A log variance is twice the corresponding log standard deviation when both are derived from the same positive variance estimate. A reproduction should keep the paper's numerical transformation and scaling, rather than switching between the two descriptions without adjusting coefficients and forecast losses.

Table 1 illustrates considerable heterogeneity in the stocks' risk: annualized average volatility ranges from approximately 17.09 for PepsiCo to 49.27 for Citigroup in the reported percentage convention. Financial stocks are prominent in the high-risk portion of the sample. These descriptive figures motivate common financial-stress predictors but do not establish that the model's effectiveness is homogeneous across assets.

## Conditional-mean specification

Define the five-day and 22-day means of log realized variance:

$$
\overline h_{t-1}^{(5)}=\frac15\sum_{j=1}^{5}h_{t-j},\qquad
\overline h_{t-1}^{(22)}=\frac1{22}\sum_{j=1}^{22}h_{t-j}.
$$

The basic HAR conditional mean combines the latest observation with these averages. The extended form can be written

$$
h_t=a+b_dh_{t-1}+b_w\overline h_{t-1}^{(5)}
+b_m\overline h_{t-1}^{(22)}
+\delta_s I_{t-1,s}h_{t-1}
+\gamma R_{t-1}+\gamma_-R_{t-1}^{-}
+u_t,
$$

where $R_{t-1}$ is the daily close-to-close log return and $R_{t-1}^{-}=R_{t-1}\mathbf1\{R_{t-1}<0\}$. The signed return and its negative part permit different slopes for positive and negative returns. For a positive return the slope is $\gamma$; for a negative return it is $\gamma+\gamma_-$. A negative coefficient on the negative-part regressor raises the predicted log variance after a negative return.

The volatility-asymmetry indicator compares the latest variance level with its historical average:

$$
I_{t-1,s}=\mathbf1\left\{B_{t-1}>\frac1s\sum_{j=1}^{s}B_{t-j}\right\}.
$$

The paper considers windows of 5, 10, 22, 44, and 66 days and a full-history version using the observations available up to the relevant date. The comparison is in variance levels, while the interacted lag in the regression is logarithmic. Comparing $h_{t-1}$ with an average of logarithms would define a different regime boundary. The exact inclusion of the latest observation in the threshold average should follow the source's indexing consistently.

The HAR structure approximates persistent dynamics using a restricted autoregression through lag 22. It is often motivated by heterogeneous trading horizons, but those coefficients do not by themselves identify heterogeneous investor populations. Similarly, the threshold is an empirical regime indicator, not an identified structural transition between economic states.

The final comparison uses six mean specifications. Model I is an AR(1); model II is ordinary HAR; model III adds the full-history volatility interaction, the signed return, and its negative part; model IV adds both return terms without the volatility interaction; model V includes only the negative-return term beyond HAR; and model VI adds the five-day volatility interaction and the negative-return term. Some prose labels are imprecise, so the explicit model definitions and table captions should govern implementation.

## Conditional uncertainty and innovation distributions

Write the residual as $u_t=\sqrt{v_t}\epsilon_t$, where the standardized innovation has mean zero and variance one. The paper compares constant error variance, GARCH(1,1), and asymmetric GJR-GARCH(1,1):

$$
v_t=\omega+\beta v_{t-1}+\alpha u_{t-1}^{2}
+\phi u_{t-1}^{2}\mathbf1\{u_{t-1}<0\}.
$$

Here $v_t$ is the variance of the error in forecasting log realized variance. It is not the stock's return variance $B_t$. Confusing these layers would result in applying a volatility-of-volatility recursion directly to asset returns, which is a different model.

The innovation is either Gaussian or standardized normal-inverse-Gaussian, abbreviated NIG. The latter permits skewness and heavy tails. The paper does not provide a full stand-alone implementation of the standardized NIG density or every numerical constraint used in estimation. A reproduction must select a parameterization, verify its mean and variance normalization, and record it; library parameter names alone are not sufficient because conventions differ.

For positivity of the GJR recursion, one normally requires $\omega>0$, $\beta\geq0$, $\alpha\geq0$, and $\alpha+\phi\geq0$. A finite unconditional error variance additionally depends on

$$
\beta+\alpha+\phi E\left[\epsilon_t^2\mathbf1\{\epsilon_t<0\}\right]<1.
$$

The last expectation equals one half under a symmetric standardized innovation, but need not equal one half under a skewed NIG distribution. This is a mathematical implementation implication of the model, not an extra restriction documented numerically in the paper. Blindly using the symmetric persistence formula for every fitted NIG model could misstate stability.

Six means, three variance specifications, and two innovation distributions give 36 models. Adding the selected external predictors to each creates another 36. The distinction between the mean and density matters for evaluation: changing the residual density can improve likelihood and prediction intervals while leaving the conditional-mean forecast nearly unchanged. The paper primarily tests point forecasts, so it does not comprehensively evaluate the potential benefits of NIG tails for density forecasting.

## External predictors and their selection

The authors first study common movement in the 16 log realized-variance series. The first principal component explains about 75% of their joint variation. They regress this component on financial and macroeconomic variables to identify candidate predictors. This PCA exercise is exploratory; the forecast equations subsequently use selected observable variables rather than forecasting only the first principal component.

The initial set contains 13 regressors derived from nine economic series: daily, weekly, and monthly S&P 500 returns; market-volume changes; log VIX; daily, weekly, and monthly returns on the Dow Jones–UBS commodity index; changes in the log dollar index; the BAA-minus-AAA corporate yield spread; the ten-year-minus-three-month Treasury spread; the effective-minus-target federal funds rate; and an index of U.S. bank credit-default-swap spreads.

The selected subset retains S&P 500 returns at three horizons, volume, log VIX, the corporate credit spread, and bank CDS. Thus it contains seven columns, even though these correspond to fewer economic categories. All forecasting regressors are lagged relative to the target day. Concurrent regressions are also shown as explanatory comparisons and must not be confused with feasible forecasts.

Table 2 reports adjusted $R^2$ of 0.78617 for the full lagged predictor set and 0.77176 for the reduced lagged set. The corresponding contemporaneous values are 0.79573 and 0.78117. The small decrease on reducing the lagged set supports parsimony in this exploratory exercise, but these are in-sample common-component regressions, not out-of-sample forecast gains for each stock.

The lagged reduced regression includes a monthly S&P return coefficient of approximately $-16.33$ with standard error 4.998. Credit-spread and bank-CDS coefficients are approximately 3.000 and 1.772, with reported partial measures of explanatory contribution 0.328 and 0.282. Their units reflect the source's predictor definitions and the scaling of the principal component, so these numbers should not be read as universal volatility elasticities. PCA signs are arbitrary until an orientation is fixed. There is also a sign inconsistency between the prose and the full table's term-spread entry; the numerical table should not be silently changed to match the narrative.

The substantive mechanism is straightforward: market declines, implied risk, and credit stress summarize common conditions that a single stock's lagged realized variance may not fully capture. The statistical design does not identify causal transmission. VIX and credit spreads may incorporate information jointly with equity volatility rather than provide exogenous shocks to it.

## Estimation and genuine forecast timing

The models are estimated stock by stock. In-sample comparisons use the full data period to study coefficient significance, likelihood improvements, and model complexity. The point-forecast exercise uses a fixed four-year rolling estimation window, re-estimated each day. Forecasts span January 2, 2008 through June 29, 2012, giving 1,134 one-day predictions. The total of 2,139 observations implies about 1,005 observations before the evaluation period; an implementation should resolve the trading-calendar mapping explicitly rather than equate four years to exactly 1,000 days.

The forecast origin is the end of day $t-1$. It uses realized-range history, returns, and financial variables known by that point to predict $h_t$. Each rolling refit should rebuild lagged means within a consistent historical buffer and preserve the intended threshold history. In particular, a full-history threshold and a threshold recalculated solely inside the rolling estimation window are different procedures. The source does not specify every such boundary convention, so it should be treated as an unresolved reproduction input.

The candidate specifications and external-predictor menu are motivated by full-sample exploratory analysis. The forecast test is out of sample with respect to rolling parameter fitting, but model-menu selection is not presented as a fully nested historical selection exercise. A new study should distinguish reproducing the published menu from selecting it afresh at each historical date. The latter would assess the additional uncertainty introduced by feature selection.

The numerical optimizer, complete starting values, convergence tolerances, NIG parameter bounds, and every treatment of failed fits are not given in the attached paper. These details can matter for 72 repeated nonlinear fits per stock and day. A practical reproduction should log convergence and apply a declared fallback procedure rather than discard inconvenient forecast dates.

## Evaluation and results

The forecast evaluation replaces latent volatility with the realized measure and uses squared-error comparisons. The paper's notation identifies the modeled series as $h_t=\log B_t$. Consequently, a faithful implementation should explicitly state whether loss is computed on that logarithmic scale. The attached PDF does not supply a complete level-retransformation rule. Exponentiating a conditional mean of $h_t$ does not generally give the conditional mean of $B_t$; under Gaussian log errors a variance correction is needed, and under NIG errors the relevant exponential moment must exist.

Diebold–Mariano comparisons use a Newey–West estimate of the long-run variance of loss differences. In the reported comparisons with HAR, positive statistics favor the row model. The model-confidence-set procedure uses range and semiquadratic statistics, with results considered at 10% and 25% thresholds. Survival means that a model has not been excluded from the set under that procedure; it does not assign a posterior probability of being best. Exact resampling settings are not fully documented in the main PDF.

The authors invoke robustness properties of certain forecast losses when volatility is measured with error. Such results must be applied on the relevant scale. An unbiased noisy proxy for a variance level does not automatically remain unbiased after taking logs. Therefore, theoretical loss robustness for variance-level proxies cannot simply be transferred to logarithmic comparisons without additional assumptions.

Return asymmetry is useful in sample. Negative-return terms are significant across the 16 stocks, whereas the additional unrestricted signed-return effect is significant for fewer stocks. Volatility-threshold terms are individually less uniformly significant, although joint comparisons can favor models that contain them. More flexible residual distributions and conditional variance equations improve likelihood fits, but that alone does not determine one-step mean accuracy.

Table 3 illustrates the point-forecast benefit of mean extensions. Model III with constant Gaussian residual variance has comparison statistics of 3.02 for Boeing, 2.62 for Caterpillar, 1.96 for IBM, 2.38 for Texas Instruments, and 2.49 for Wells Fargo. Model VI with GARCH variance and NIG innovations gives 3.60 for Boeing, 3.26 for Caterpillar, 3.08 for IBM, and 2.83 for Wells Fargo. In contrast, corresponding improvements for FedEx and Citigroup can be weak, with statistics around 0.46 and 0.97 in that latter specification.

At least one asymmetric model improves on HAR for 13 of the 16 stocks in the paper's reported comparisons. Only seven stocks exhibit improvement across all the relevant variance/distribution families. These are heterogeneous results, not evidence that one fixed extension dominates for every asset. Table 4 excludes basic HAR from the confidence set for nine stocks at 25% and five stocks at 10%.

When the mean specification is held fixed at HAR, changing only the variance equation and innovation distribution produces much less separation: for 15 of 16 stocks, all six such variants remain in the confidence set. That is the clearest evidence for the paper's modeling priority. The extra parameters in a sophisticated residual law may be useful for other purposes, but their one-day point-forecast benefit is limited in this experiment.

Adding the selected financial variables improves comparisons against bare HAR. For the macro-augmented ordinary HAR with constant Gaussian error variance, reported statistics include 2.85 for Boeing, 2.40 for Honeywell, 2.30 for IBM, 2.55 for JPMorgan, 2.18 for Kraft, and 2.18 for PepsiCo. These compare a richer information set with the baseline, so they do not isolate the benefit of external information after every asymmetry has already been included.

Table 6 makes that stricter comparison by adding predictors to the same mean/variance family. Gains are more selective. For model III with GJR variance and NIG innovations, adding external variables gives statistics of 2.14 for Boeing, 2.88 for PepsiCo, 2.11 for Procter & Gamble, and 2.13 for Time Warner, but $-1.15$ for Wells Fargo. The authors summarize meaningful incremental gains for roughly seven of the 16 stocks.

Table 7's confidence sets likewise show external predictors are useful without making them uniformly necessary. Models without them are excluded for seven stocks at 10% and nine at 25%. At least one augmented model survives for every stock, but that is weaker than saying every augmented specification is superior. Wells Fargo retains a strong unaugmented model, while Procter & Gamble more clearly favors the augmented family.

The tables mainly report test statistics and confidence-set values rather than a complete set of raw RMSE levels. They therefore do not support a numerical claim such as a universal 20% reduction in forecast error. Statistical separation, economic magnitude, and trading value are distinct questions. The paper does not evaluate a portfolio strategy, turnover, transaction costs, or risk-budget utility.

## Reproduction priorities and limits

The first replication priority is measurement. Construct and archive the daily corrected bipower range series, its logarithm, the estimated noise level, and the observation counts. Verify that corporate-action handling and session definitions are consistent across price ranges and close-to-close returns. Because the estimator uses extrema, data cleaning should be specified before inspecting forecast performance.

The second priority is separating mean effects from uncertainty effects. Reproduce ordinary HAR and the two main asymmetric alternatives, III and VI, under the same target, sample, and loss. Only then add the GARCH/GJR residual layer and NIG density. This sequence permits an observed improvement to be attributed to a changed conditional mean or information set rather than to simultaneous changes throughout the model.

The third priority is reproducing the external predictor timing and units. The paper's selected menu is concrete, but release times, holiday alignment, data-source vintages, and the construction of the bank-CDS index require additional documentation. Contemporary closing data from different markets may not all be available at the same New York timestamp. Any deployment should enforce an actual information cutoff rather than rely only on matching calendar dates.

The empirical scope remains narrow: 16 stocks, one market, a one-day horizon, and an evaluation concentrated on 2008–2012. No inference here establishes robustness to later market microstructure, a wider universe, or a different risk target. The noise model and jump correction are assumptions, not guarantees that the target is error-free. The missing appendix and undocumented numerical settings also limit exact reconstruction.

The paper's transferable insight is a disciplined allocation of modeling effort. For point forecasts of log realized range variance, a concise asymmetric mean and a carefully timed set of market and credit indicators can add more than an elaborate residual distribution. For density forecasts or tail-risk decisions, the ranking could change; those applications require their own loss functions and validation rather than extrapolating the point-forecast results.
