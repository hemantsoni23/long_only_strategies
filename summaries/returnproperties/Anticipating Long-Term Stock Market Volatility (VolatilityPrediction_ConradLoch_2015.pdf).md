# Anticipating Long-Term Stock Market Volatility

Christian Conrad and Karin Loch, *Journal of Applied Econometrics* 30 (2015), 1090–1114; first published online in 2014. DOI: [10.1002/jae.2404](https://doi.org/10.1002/jae.2404).

Source: [VolatilityPrediction_ConradLoch_2015.pdf](../../Finance/VolatilityPrediction_ConradLoch_2015.pdf), 25 PDF pages. The discussion below follows the published paper, especially Sections 2–4 and Tables II–V. Selected numerical details were also checked against the publisher's [supplementary appendix](https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjae.2404&file=jae2404-sup-0001-supplementary.pdf). The online appendix was accessible as extracted text, but its downloadable/renderable PDF was unavailable in this environment; full visual verification of its tables was therefore not possible.

## Why this matters and what is new

A daily volatility model can react rapidly to recent market shocks while saying little about the economic conditions that will sustain volatility over the next several quarters. This paper separates those functions. Daily asymmetric GARCH dynamics describe short-lived departures from a slowly changing variance level. Quarterly macroeconomic variables determine that level through a parsimonious distributed-lag filter. The empirical question is whether economic conditions contain information about longer-horizon equity volatility beyond the information in past realized variance.

The basic GARCH-MIDAS decomposition is inherited from earlier research. The authors' distinctive contributions are their systematic treatment of the timing of macroeconomic effects, their use of flexible rather than necessarily declining lag weights, and their feasible use of professional forecasts in a two-sided filter. A two-sided statistical filter ordinarily looks into the future. Here, observed future macroeconomic outcomes are replaced by forecasts that existed at the prediction date. This provides a concrete way to distinguish a variable that leads volatility from one that merely moves with it.

Their evidence supports a countercyclical long-run variance component: deteriorating activity, weak housing, declining sentiment, and an unfavorable term spread are associated with greater future volatility. The largest gains generally occur at longer horizons. However, the sample contains only 44 out-of-sample quarters, real-time publication timing is imperfectly aligned, and better mean squared error does not imply well-calibrated forecast levels. The contribution is an economically interpretable forecasting architecture, with promising but qualified empirical support.

## Return model and normalization

Let $r_{i,t}$ be the daily equity return on trading day $i$ of quarter $t$. The model is

$$
r_{i,t}=\mu+\sqrt{\tau_t g_{i,t}}Z_{i,t},\qquad E[Z_{i,t}]=0,\qquad E[Z_{i,t}^2]=1.
$$

The innovations are independent and identically distributed with the stated moments; the source does not impose Gaussianity as the true distribution. Gaussianity is the working density used in quasi-maximum-likelihood estimation. Here $\tau_t>0$ is the quarter-specific daily variance level, while $g_{i,t}$ is a dimensionless daily multiplier. The daily conditional variance is their product. The paper uses an asymmetric GARCH recursion:

$$
g_{i,t}=1-\alpha-\beta-\frac{\gamma}{2}
+\left[\alpha+\gamma\mathbf 1\{r_{i-1,t}-\mu<0\}\right]
\frac{(r_{i-1,t}-\mu)^2}{\tau_t}
+\beta g_{i-1,t}.
$$

The last observation of the preceding quarter supplies the lag at a quarter boundary. A program must handle that boundary explicitly rather than reset the daily multiplier to one every quarter. With symmetric unit-variance innovations, the persistence parameter is $p=\alpha+\beta+\gamma/2$. The intercept normalizes the stationary GARCH component to mean one when the long-run scale is held fixed. This normalization identifies the level of $\tau_t$ separately from the level of $g_{i,t}$.

The stated stationarity restriction is $p<1$, with positive basic ARCH and GARCH coefficients. For a numerical implementation, positivity also requires that the coefficient multiplying a negative squared innovation remain nonnegative, so $\alpha+\gamma\geq0$. These are variance-recursion restrictions; they do not make the macroeconomic process stationary automatically. Nor should the fixed-scale unit-mean argument be read as a proof that every finite-sample quarterly average of $g$ is exactly one.

Negative returns can raise subsequent variance more than positive returns of the same magnitude through $\gamma$. The paper does not infer this asymmetry from a causal identification design. It is a conditional-distribution specification intended to prevent ordinary daily leverage effects from being incorrectly attributed to macroeconomic predictors.

## The quarterly MIDAS component

For a single quarterly predictor $X_t$, the one-sided specification is

$$
\log\tau_t=m+\theta\sum_{k=1}^{K}\phi_k(\omega_1,\omega_2)X_{t-k},\qquad K=12.
$$

The normalized beta weights are

$$
\phi_k=\frac{u_k^{\omega_1-1}(1-u_k)^{\omega_2-1}}
{\sum_{j=1}^{K}u_j^{\omega_1-1}(1-u_j)^{\omega_2-1}},
\qquad u_k=\frac{k}{K+1}.
$$

Thus three years of macroeconomic history are compressed into one weighted index, using two shape parameters rather than 12 unrestricted lag coefficients. Positivity of variance follows from exponentiation. Normalizing the weights to sum to one makes $\theta$ the change in log daily variance associated with a one-unit shift in every included lag of $X$.

The restricted filter fixes $\omega_1=1$ and uses declining weights. The unrestricted filter estimates both shape parameters and can place the largest weight several quarters into the past. This distinction is economically central. If housing conditions or the term spread anticipate volatility, forcing the newest observation to receive the largest weight can obscure their predictive relationship. The authors compare restricted and unrestricted filters using likelihood-ratio evidence and information criteria, not a separate coefficient at each lag.

Because predictors have different units, raw $\theta$ magnitudes cannot rank their economic importance. Annualized growth rates are measured in percentage points, whereas the National Activity Index is a standardized activity measure and the term spread is a yield difference. For example, a housing coefficient of approximately $-0.0173$ means that a one-percentage-point increase in the weighted growth measure multiplies the daily variance level by $\exp(-0.0173)$, about 0.983. That calculation is a direct interpretation of the model, not a separately estimated response or causal elasticity.

Setting $\theta=0$ produces an ordinary asymmetric GARCH model with a constant long-run variance scale. A benchmark instead uses quarterly realized variance as the MIDAS predictor. A combined model includes both the realized-variance filter and a macroeconomic filter. Separate coefficients and lag-weight parameters matter: appending an unweighted macroeconomic variable to a realized-variance regression is not the same model.

## Making a two-sided filter feasible

An unrestricted historical filter can reveal that volatility responds with delay to a macroeconomic variable. Conversely, volatility may anticipate economic conditions. To allow this, the paper adds present and future values to the long-run component. The conceptual form is

$$
\log\tau_t=m+\theta\left[
\sum_{k=1}^{12}\phi_k X_{t-k}
+\sum_{k=-3}^{0}\phi_k\widetilde X_{t-k\mid t-1}
\right].
$$

The weight notation here follows the paper's calendar indexing. In code, beta weights must be normalized over the full ordered set of included observations, using positive grid locations. One must not substitute negative calendar lags directly into fractional powers in the beta-density formula. The feasible filter has up to 16 positions: 12 historical quarters and four forward-looking entries corresponding to the current quarter and three future quarters.

Three versions distinguish information from hindsight. The infeasible version uses realized future economic outcomes and is a diagnostic upper-information case, not a tradable forecast. A time-series-forecast version substitutes forecasts from an autoregression of order four with seasonal dummies. The survey version substitutes median forecasts from the Philadelphia Survey of Professional Forecasters, available at $t-1$. An additional specification uses survey nowcasts for the historical inputs as well, avoiding a mixture of subsequently observed historical outcomes and survey expectations.

The usual maximum lead is three quarters. Convergence difficulties require two leads for certain specifications, including some GDP and corporate-profit cases indicated in Table IV. Those exceptions should be reproduced rather than silently forcing the same dimension on every model. For early missing four-quarter survey forecasts, footnote 4 instead estimates $X^{SPF}_{t+4\mid t}$ from seasonal dummies and $X^{SPF}_{t+4-i\mid t}$ for $i=1,\ldots,4$, using available observations. These regressors are lower-horizon forecasts from the same survey vintage, not lagged realized macroeconomic values from the AR(4) used for time-series scenarios. Predicted values fill the missing survey entries. The exact filling decisions should be recorded as part of the data vintage, because they change the effective information source.

The survey is therefore not merely another contemporaneous regressor. It changes which economic path the MIDAS filter sees. A successful feasible two-sided model means that expectations about the path of the economy carry information relevant to the slow variance component. It does not demonstrate that realized future macroeconomic variables were available to investors.

## Data, transformations, and information dates

Daily S&P 500 returns run from January 2, 1969 to December 30, 2011: 10,852 daily observations and 172 quarters. The main estimation exercise uses daily returns from 1973Q1 through 2010Q4, with quarterly predictors beginning in 1970Q1 to supply the three-year MIDAS history. Observations from 1969 also support the autoregressive constructions used for uncertainty measures.

The economic variables are real GDP, industrial production, unemployment, housing starts, nominal corporate profits after tax, real personal consumption, the GDP deflator, the Chicago Fed National Activity Index, the ISM new-orders index, Michigan consumer sentiment, and the term spread between the ten-year Treasury yield and the three-month Treasury bill rate. Monthly or daily input series are aggregated to quarterly averages where appropriate.

GDP, industrial production, housing starts, corporate profits, consumption, and the deflator enter as annualized quarter-over-quarter changes:

$$
\Delta X_t=100\left[\left(\frac{X_t}{X_{t-1}}\right)^4-1\right].
$$

This is not four times a log difference, although that approximation may be close for small changes. Unemployment and consumer sentiment enter as first differences. The activity index, new orders, and term spread enter in levels. A replication must match these transformations, since substituting year-over-year growth would alter both the lag interpretation and the measured predictive relationship.

First-release observations are used where available, drawing on Philadelphia Fed and St. Louis Fed data. This improves realism relative to using fully revised histories. Nevertheless, the paper explicitly recognizes a publication-timing issue: some first releases for quarter $t-1$ occur during quarter $t$. Treating the whole $X_{t-1}$ vector as available at the boundary can therefore use information not yet known at the actual forecast time. First-release data and a strictly implementable real-time panel are different objects. A modern reproduction should create a release-date calendar and report the effect of delaying unavailable observations.

Survey forecasts are available for GDP, industrial production, unemployment, housing starts, corporate profits, and the GDP deflator. The paper uses survey medians and distinguishes nowcasts from forecasts one through four quarters ahead. Survey disagreement is later represented by interquartile ranges. The historical median and the disagreement measure are not interchangeable: the former predicts the mean economic path, while the latter measures dispersion across respondents.

Returns are reported in percentage units. Consequently, daily and quarterly variance are in squared percentage-return units. The quarterly realized-variance input used in the MIDAS benchmark is the sum of squared daily S&P 500 returns within the quarter (Section 3, printed p. 1094). It is not built from intraday observations. The out-of-sample evaluation proxy is different: it sums daily realized variances computed from five-minute returns over the quarter (Section 4.3 and Table V). Both quantities are variances rather than standard deviations, but they use different observation frequencies and measurement procedures. A replication must construct the daily-return benchmark input and the intraday evaluation proxy separately.

## Estimation and forecasting mechanics

Parameters are estimated by Gaussian quasi-maximum likelihood, jointly over the return mean, daily GARCH dynamics, long-run intercept, predictor coefficient, and beta-weight parameters. Apart from constants, the objective minimizes

$$
\sum_{t}\sum_i\left[
\log(\tau_tg_{i,t})+
\frac{(r_{i,t}-\mu)^2}{\tau_tg_{i,t}}
\right].
$$

Robust standard errors follow the Bollerslev–Wooldridge approach. These allow some conditional-distribution misspecification, but do not eliminate finite-sample identification problems in flexible lag weights. The main paper notes that a complete general asymptotic theory for its macro-driven specification is not supplied; simulation evidence provides support rather than a theorem establishing all properties of the estimator.

For a quarter with $N$ trading days and a fixed forecast long-run scale, the conditional expected GARCH multiplier mean-reverts geometrically:

$$
E(g_i)=1+p^{i-1}(g_1-1).
$$

The resulting forecast of quarterly return variance is

$$
\widehat{RV}=\widehat\tau\left[
N+(g_1-1)\frac{1-p^N}{1-p}
\right].
$$

The first day's conditional multiplier incorporates the most recent return information. If it is already one, the quarterly forecast reduces to $N\widehat\tau$. This formula sums daily variances. Taking daily square roots and then summing would target a different quantity. The geometric sum should be evaluated carefully when $p$ is close to one to avoid numerical cancellation.

For horizons beyond the next quarter, the long-run component is held at its one-step forecast rather than generated from a fully specified joint macroeconomic forecasting system. This simplifying convention contributes to the interpretation of the exercise: it evaluates the persistence and usefulness of the current slow variance signal. It does not fully simulate the future path of macroeconomic conditions and future daily shocks.

The forecast evaluation estimates models using 1973Q1–1998Q4 returns and predictors from 1970Q1. Quarterly forecast targets cover 2000Q1–2010Q4, 44 quarters, at horizons of one through four quarters. These are forecasts of the variance in the target quarter, not cumulative variance over the entire intervening horizon. The source's reported setup does not fully specify every numerical initialization and optimizer setting, or provide a sufficiently explicit re-estimation calendar to justify inventing a daily or quarterly rolling estimation scheme.

The evaluation proxy uses five-minute intraday S&P 500 data from the Oxford–Man realized library. Forecasts are assessed with mean squared error relative to the realized-variance MIDAS benchmark and Mincer–Zarnowitz regressions of realized variance on a constant and the forecast. Robust inference accompanies those regressions. Giacomini–White tests assess predictive-performance differences. A rolling 500-observation window used in daily forecast comparison graphs is an evaluation window; it should not automatically be interpreted as the model's estimation-window length.

## What the fitted model says about economic timing

Table II gives strong evidence that the slow variance level is countercyclical. In restricted one-sided models, the real-GDP coefficient is $-0.0803$ with standard error 0.0251; industrial production is $-0.0434$ (0.0133); unemployment is $0.5689$ (0.1865); corporate-profit growth is $-0.0187$ (0.0053); and the National Activity Index is $-0.3085$ (0.0728). These are conditional associations within separate models, not partial effects from one regression containing every variable.

Housing illustrates why the weight shape matters. Its restricted coefficient is $-0.0159$, and its variance-ratio measure is 14.39%. The unrestricted filter produces a coefficient of $-0.0173$ (0.0047), shape parameters 2.8071 and 4.8430, and a variance ratio of 21.85%. The likelihood-ratio p-value is 0.0007. Consumer sentiment similarly gains from a flexible filter: its variance ratio rises from 6.55% to 12.63%, with a likelihood-ratio p-value of 0.0005.

For the term spread, the unrestricted coefficient is $-0.2443$ (0.0458), with shape parameters 4.2018 and 6.2756. The resulting lag distribution peaks around five quarters into the past. That is evidence that the economically relevant timing is not concentrated at the most recent quarter. The unrestricted filter's variance ratio is 15.94%, versus 14.32% for the restricted filter; the likelihood-ratio p-value is 0.0463.

The GDP-deflator results are much weaker. The restricted coefficient 0.0269 has standard error 0.0259 and a variance ratio below 1%. The unrestricted fit uses very large shape parameters, approximately 114 and 197, concentrating the weight on a narrow lag region. Its coefficient is only weakly significant and its variance ratio is 2.10%. This is a warning against equating a highly concentrated fitted lag shape with a stable economic finding.

Equation (9) uses the variance ratio

$$
VR(X)=\frac{\widehat{\operatorname{Var}}(\log\tau_t^X)}{\widehat{\operatorname{Var}}(\log(\tau_t^{RV}g_t^{RV}))}.
$$

The denominator is the log total expected quarterly variance from the **same restricted GARCH-MIDAS-RV benchmark for every candidate model**; $g_t^{RV}$ is its quarterly expected short-run multiplier in the paper's notation. It is not each candidate model's own fitted total variance. Reported values multiply this ratio by 100 to express it as a percentage. It is a descriptive measure of component variation, not an ordinary regression $R^2$, a causal fraction of uncertainty explained, or an orthogonal variance decomposition. Combined models can have much higher ratios: housing with realized variance reaches 27.34%, corporate profits roughly 37%, and the term spread roughly 31–33%. Those larger in-sample components do not establish better forecasts.

Feasible expectations improve some component estimates substantially. The industrial-production variance ratio rises from 7.57% in the one-sided model to 15.26% with survey expectations. Unemployment rises from 6.02% to 15.62%. Housing, which already has a strong historical leading relationship, rises only from 21.85% to 22.81%. This heterogeneity is useful: expectations matter most when the historical macroeconomic series does not already provide the relevant forward-looking information.

## Forecast results and their uncertainty

Table V reports the following MSE ratios relative to the GARCH-MIDAS realized-variance benchmark. Values below one favor the macroeconomic model; parentheses contain the reported predictive-comparison p-values.

| Predictor and filter | One quarter | Two quarters | Three quarters | Four quarters |
|---|---:|---:|---:|---:|
| Housing, one-sided | 0.76 (0.32) | 0.76 (0.09) | 0.75 (0.07) | 0.76 (0.06) |
| Housing, two-sided | 0.74 (0.28) | 0.76 (0.10) | 0.74 (0.08) | 0.75 (0.07) |
| Industrial production, two-sided | 0.76 (0.20) | 0.84 (0.08) | 0.84 (0.04) | 0.85 (0.04) |
| Unemployment, two-sided | 0.99 (0.93) | 0.86 (0.06) | 0.86 (0.02) | 0.87 (0.02) |
| Corporate profits, one-sided | 0.83 (0.56) | 0.79 (0.10) | 0.78 (0.05) | 0.79 (0.04) |
| Consumer sentiment, one-sided | 0.56 (0.21) | 0.78 (0.10) | 0.81 (0.08) | 0.84 (0.10) |
| Term spread, one-sided | 1.19 (0.71) | 0.85 (0.15) | 0.80 (0.06) | 0.77 (0.04) |

The distinction between estimated magnitude and statistical precision is important. Consumer sentiment's one-quarter ratio of 0.56 is a large estimated loss reduction, yet its p-value is 0.21. A much smaller four-quarter reduction for industrial production has stronger reported evidence. Losses are volatile, the sample is small, and horizon-specific predictability differs.

The term spread is particularly informative about horizon dependence. It is worse than the benchmark at one quarter but has an MSE ratio of 0.77 at four quarters. Its four-quarter Mincer–Zarnowitz regression has an intercept of $-161.57$ (standard error 80.35), slope 4.47 (1.69), and $R^2$ of 27.49%. The realized-variance benchmark at that horizon has $R^2$ of only 1.06%, but the macroeconomic forecast's slope is far from the ideal value one. Better variation tracking and better raw MSE do not imply unbiased, correctly scaled forecasts.

The supplementary combined-model results reinforce a distinction already made in the main text: adding realized variance to a macroeconomic component is not uniformly beneficial. For example, the combined corporate-profit model has one-quarter MSE ratio 3.22 and four-quarter ratio 1.56; the combined housing model has ratios 0.89 and 0.87. These appendix figures are supporting diagnostics, not a different evaluation design.

The rolling daily comparisons indicate that advantages vary over time and become more pronounced at longer horizons and during the financial crisis. This makes economic sense for a slow component, but it also limits the claim of stable unconditional dominance. A production forecast should be assessed across regimes rather than validated solely on an average containing 2008–2009.

## Robustness and a disciplined reproduction

The paper also considers principal components of the predictor panel, macroeconomic uncertainty, survey disagreement, pre-crisis estimation, monthly inputs, and simpler predictive regressions. Activity-related information dominates the first principal component, while the term spread is prominent in another. These combinations do not uniformly outperform the strongest individual predictors. Estimated uncertainty from squared autoregressive residuals is generally weak; survey disagreement, especially about unemployment, is more informative. A corporate-profit uncertainty result has a counterintuitive sign, illustrating that dispersion measures are not interchangeable structural risk variables.

Simple regressions of log realized volatility on its own lag and one macroeconomic observation show little incremental explanatory power. Adding the estimated long-run component can work better. That comparison supports the value of distributed lags and nonlinear filtering, although the fitted component is a generated regressor and should not be treated as a directly observed economic variable without accounting for estimation.

A faithful implementation should first reproduce the transformations and exact sample alignment, then the restricted one-sided fits, and only then the flexible and survey-based versions. Numerical checks should include weight normalization, positivity, continuity of the daily recursion across quarters, likelihood agreement under the nested constant-scale model, and forecasts in the limit where the daily multiplier equals one. Those checks test the model's meaning rather than merely whether an optimizer returns a number.

Several inputs remain insufficiently documented for exact numerical reproduction: full optimizer settings, starting-value selection, the treatment of all calendar irregularities, all data-vintage retrieval details, and a complete operational publication calendar. The paper's first-release convention should be reproduced as one experiment, with a strictly release-timed variant reported separately. The latter is an extension, not a correction silently folded into the published results.

The research takeaway is that macroeconomic information is most useful when embedded in a model that permits economically meaningful timing and separates persistent variance from daily shocks. The practical limitation is that the most persuasive long-horizon findings come from a short crisis-containing evaluation and do not establish a ready-to-trade allocation rule. Position sizing, risk limits, transaction costs, and utility gains are not evaluated here; a volatility forecast would require those additional decisions before becoming an investment strategy.
