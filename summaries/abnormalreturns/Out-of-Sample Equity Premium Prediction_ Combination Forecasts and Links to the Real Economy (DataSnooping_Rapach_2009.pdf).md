# Out-of-Sample Equity Premium Prediction: Combination Forecasts and Links to the Real Economy

David E. Rapach, Jack K. Strauss, and Guofu Zhou. *Review of Financial Studies*, advance-access article published August 11, 2009, DOI: 10.1093/rfs/hhp063; subsequently published in volume 23 (2010), 821-862. Source: [DataSnooping_Rapach_2009.pdf](../../Finance/DataSnooping_Rapach_2009.pdf). The filename does not describe the actual title. All 42 pages of the supplied advance-access version were read, including the full methodology, seven tables, seven figures, footnotes, and references. There is no separate appendix in this PDF. Page references below use its printed pages 1-42, matching PDF pages; critical equations and tables were visually checked.

## Why this matters

The failure of most individual market-return predictors out of sample does not imply that their information is useless jointly. Rapach, Strauss, and Zhou show that simply averaging forecasts from fifteen univariate predictive regressions can beat the recursively estimated historical equity premium even when almost every individual regression loses to it. The mechanism is primarily stabilization: different predictors emit noisy and sometimes conflicting signals, and averaging reduces that noise while retaining information about changing expected returns.

For 1965:Q1-2005:Q4, the equal-weighted combination has out-of-sample $R^2=3.58\%$ and an annual certainty-equivalent gain of 2.34% relative to an investor using the historical-mean forecast. For 1976:Q1-2005:Q4, when fourteen of fifteen individual forecasts have negative $R^2$, the combination still achieves 1.19% and a 0.57% utility gain. The latter period is the more telling result: diversification improves a collection of individually disappointing forecasts without discovering a new variable.

The paper's second contribution is to connect combined equity-premium forecasts to real activity. They track business-cycle turning points, perform particularly well during low-growth observations, forecast macroeconomic growth when the same variables are recombined for that target, and share structural instabilities with macro relationships. This makes the forecasts economically interpretable. It does not prove that all predictability is compensation for macroeconomic risk or that the identified breaks were known to investors in real time.

## Predictive system and information set

Let $r_{t+1}$ denote the quarterly S&P 500 excess log return and $x_{i,t}$ one of fifteen predetermined predictors. Each model is

$$
r_{t+1}=\alpha_i+\beta_i x_{i,t}+\epsilon_{t+1}.
$$

OLS is reestimated at each forecast origin with an expanding window. At origin $t$, use observations whose returns and lagged predictors are available through that date, estimate $(\widehat\alpha_{i,t},\widehat\beta_{i,t})$, and form

$$
\widehat r_{i,t+1}=\widehat\alpha_{i,t}+\widehat\beta_{i,t}x_{i,t}.
$$

The benchmark is the historical mean available at $t$,

$$
\bar r_{t+1}=\frac1t\sum_{j=1}^t r_j,
$$

with indices understood relative to the available estimation sample. The source's printed expression on p. 6 omits the divisor $1/t$; its repeated description as a historical average and all subsequent reasoning require a mean, not a cumulative sum. The formula above explicitly supplies that normalization.

Forecast combination occurs *after* fitting separate predictive regressions:

$$
\widehat r_{c,t+1}=\sum_{i=1}^{15}\omega_{i,t}\widehat r_{i,t+1},
\qquad\sum_i\omega_{i,t}=1.
$$

It is not an unrestricted regression on all fifteen raw predictors. Separate models remain cheap to estimate, and combination weights are known at the forecast origin. No future realized return is used to select the current weight. Nevertheless, “real time” in this paper mainly refers to recursive estimation and specified release lags; the supplied historical macro series are not a fully reconstructed archive of real-time data vintages.

## Fifteen predictors and sample construction

The quarterly dataset is taken from Welch and Goyal and spans 1947:Q1-2005:Q4, the common period available for the selected variables. Stock returns are continuously compounded S&P 500 total returns, including dividends, less the Treasury-bill rate. A replication should retain the source's return convention rather than mix this log-return target with a simple-return series without adjustment.

| Predictor | Definition in the supplied article |
|---|---|
| D/P | Log trailing-one-year dividends minus log current S&P 500 price |
| D/Y | Log dividends minus log lagged stock price |
| E/P | Log trailing-one-year earnings minus log current stock price |
| D/E | Log dividends minus log earnings |
| SVAR | Sum of squared daily S&P 500 returns |
| B/M | Dow Jones Industrial Average book value divided by market value |
| NTIS | Twelve-month moving sum of net issues by NYSE stocks divided by their total end-of-year market capitalization |
| TBL | Three-month Treasury-bill secondary-market interest rate |
| LTY | Long-term government bond yield |
| LTR | Long-term government bond return |
| TMS | LTY minus TBL |
| DFY | BAA corporate yield minus AAA corporate yield |
| DFR | Long-term corporate bond return minus long-term government bond return |
| INFL | CPI inflation for all urban consumers |
| I/K | Aggregate private nonresidential fixed investment divided by aggregate capital |

Inflation is lagged an additional period because publication occurs after the period it measures. The main I/K specification uses the contemporaneously dated predictor; an extra-lag robustness test reportedly leaves the conclusions qualitatively unchanged. The article refers to Welch-Goyal for detailed construction and underlying sources, including historical accounting data and quarterly aggregation. It does not provide all series-level vintage, interpolation, and revision rules.

The three forecast evaluation windows are 1965:Q1-2005:Q4, 1976:Q1-2005:Q4, and 2000:Q1-2005:Q4, corresponding to 164, 120, and 24 quarters. The latter two windows overlap the first and each other. They investigate sensitivity to historical regimes rather than supply three independent tests. The 2000-2005 window emphasizes the technology-bubble collapse and is particularly short for estimating utility or forecast accuracy.

Some combination methods need an initial performance record. The authors use the ten years, or forty quarters, preceding each evaluation start as the initial out-of-sample holdout period. For the 1965 evaluation, this means producing preliminary recursive forecasts over 1955-1964. That holdout is used to set combination weights; it is not part of the reported evaluation period. Mean, median, and trimmed-mean rules require no performance fitting, but are evaluated over the same post-holdout interval for comparability.

## Combination algorithms

The mean sets every weight to $1/15$. The median selects the median of the fifteen current forecast values. The trimmed mean discards the highest and lowest current forecasts and averages the remaining thirteen. Median and trimming therefore have time-varying effective weights even though they require no loss-based parameter estimation. None of these methods discards a predictor permanently because it previously looked weak.

The discount mean squared prediction error method (DMSPE) updates

$$
\phi_{i,t}=\sum_{s=m}^{t-1}\theta^{t-1-s}
(r_{s+1}-\widehat r_{i,s+1})^2,
\qquad
\omega_{i,t}=\frac{\phi_{i,t}^{-1}}{\sum_{j=1}^{15}\phi_{j,t}^{-1}}.
$$

It uses $\theta=1$ or $0.9$. With $\theta=1$, all holdout errors receive equal weight. With $\theta=0.9$, older errors are exponentially discounted; a ten-quarter-old squared error gets about 35% of a current one's weight. This method uses inverse individual forecast losses, not a full error-covariance optimizer. The source links it to the classic Bates-Granger special case under uncorrelated forecasting components; actual correlated model errors mean it is not generally the global minimum-MSE combination.

Empirically, DMSPE weights stay relatively near $1/15$. No single predictor maintains dominance for long over the holdout record. The authors also tried a Schwarz-criterion-based combination resembling approximate posterior model probabilities; its weights were unstable and its performance poor. Those complete results are not provided. Thus the preference for simple averaging is supported against several alternatives considered by the authors, but the published tables do not audit every attempted weighting scheme.

A separate robustness variant imposes Campbell-Thompson restrictions on each individual forecast before combining: if an estimated predictive slope has the wrong theoretical sign, set it to zero; if the forecast equity premium is negative, set the forecast to zero. The table reports the mean of these restricted forecasts as “Mean, CT.” These are prior economic restrictions, not estimated risk constraints. The paper does not give a compact sign dictionary for every predictor, so exact implementation requires the cited convention or code.

## Statistical evaluation

The primary score is

$$
R^2_{OS}=1-
\frac{\sum_{t\in\mathcal E}(r_{t+1}-\widehat r_{t+1})^2}
{\sum_{t\in\mathcal E}(r_{t+1}-\bar r_{t+1})^2},
$$

where $\mathcal E$ is the evaluation interval. Positive values mean lower squared prediction error than the recursive historical mean. This is neither an in-sample regression $R^2$ nor the squared correlation between predictions and returns; it can be negative and penalizes poor calibration.

The historical-mean model is nested in each single-predictor regression, so an ordinary Diebold-Mariano comparison has problematic size and low power. The paper uses the Clark-West adjusted loss differential

$$
f_{t+1}=(r_{t+1}-\bar r_{t+1})^2
-(r_{t+1}-\widehat r_{t+1})^2
+(\bar r_{t+1}-\widehat r_{t+1})^2.
$$

Regress $f$ on a constant and use its $t$ statistic in a one-sided upper-tail normal test. The adjustment compensates for additional estimation noise under a nested-model null. Reported significance stars use this statistic; they are not confidence intervals for the raw $R^2$.

The source applies the test to combinations as well as individual linear models. Median, trimming, and adaptive performance weights are nonlinear forecast procedures, and the simple nested-linear-model justification does not automatically cover every such transformation. The paper reports the resulting tests but gives no dedicated finite-sample simulation for their size under this particular combination design. Together with multiple predictors, weighting rules, and windows, this is a reason to interpret marginal 10% significance cautiously.

Cumulative squared-error differences in Figures 1-2 help locate when gains occur. A rising line means the competing forecast beats the historical mean over that interval; a declining line means it loses. Combination curves are much more stable than individual ones, but are not everywhere increasing. The authors explicitly do not claim dominance over every possible subperiod.

## Investment objective and utility gains

The investor allocates between equities and bills using risk aversion $\gamma=3$. Conditional return variance is estimated from a trailing ten-year window of quarterly returns, rather than from the predictive regression residuals or a separate stochastic-volatility model. The unconstrained mean-variance solution is $\widehat r/(\gamma\widehat\sigma^2)$ and the stock weight is clipped to $[0,1.5]$:

$$
w_t=\operatorname{clip}_{[0,1.5]}
\left(\frac{\widehat r_{t+1}}{\gamma\widehat\sigma^2_{t+1}}\right).
$$

The benchmark investor applies the same variance estimator and constraint to the historical-mean forecast. This isolates the value of the competing mean forecast more cleanly than comparing it with unconditional 100% stocks.

For each realized portfolio, compute

$$
\widehat\nu=\widehat\mu_p-\frac{\gamma}{2}\widehat\sigma_p^2,
\qquad
\Delta=400(\widehat\nu_{forecast}-\widehat\nu_{mean}).
$$

The factor 400 converts a quarterly utility difference in decimal returns to annual percentage points. The paper occasionally says “monthly” in its allocation prose, but the data, ten-year quarterly variance window, forecast dates, and annualization establish the quarterly experiment reported here. A replicator should not silently rebalance a quarterly forecast monthly and claim identical results.

Utility gains are before explicit transaction costs, taxes, borrow/funding spreads, and market impact. The stock allocation may reach 150%, so implementing the leveraged portion requires financing not separately costed. There is no dynamic no-trade region or explicit penalty on turnover. The certainty-equivalent interpretation is conditional on the mean-variance preference approximation, fixed risk aversion, sample moments, and the constraints. The paper reports no uncertainty intervals for utility gains and does not integrate coefficient uncertainty into the weight decision.

## Main forecasting results

Table 1's central combination results are:

| Method | 1965-2005 $R^2_{OS}$ | Annual utility gain | 1976-2005 $R^2_{OS}$ | Annual utility gain | 2000-2005 $R^2_{OS}$ | Annual utility gain |
|---|---:|---:|---:|---:|---:|---:|
| Mean | 3.58% | 2.34% | 1.19% | 0.57% | 3.04% | 2.31% |
| Median | 3.04% | 1.03% | 1.51% | 0.53% | 1.56% | 0.28% |
| Trimmed mean | 3.51% | 2.11% | 1.23% | 0.59% | 2.98% | 2.12% |
| DMSPE, $\theta=1$ | 3.54% | 2.41% | 1.11% | 0.54% | 2.56% | 1.65% |
| DMSPE, $\theta=0.9$ | 3.49% | 2.59% | 1.01% | 0.46% | 2.66% | 1.97% |
| Mean, CT | 3.23% | 1.25% | 1.20% | 0.55% | 2.43% | 1.32% |

All five unrestricted combination $R^2$ values are significant at 1% over 1965-2005. Over 1976-2005, the median is significant at 5% and the other four at 10%. Over 2000-2005, the median is significant at 10% and the other four at 5%. Equal-weight averaging is therefore competitive with more adaptive weights; the source does not identify a consistently best method across all economic and statistical metrics.

The individual models provide essential context. Over 1965-2005, only D/P, D/Y, E/P, LTR, and I/K have positive $R^2$; the first four are at most 0.36%, while I/K reaches 1.44%. SVAR is -12.97%, TMS -2.96%, and TBL -2.78%. Yet thirteen of fifteen individual models have positive utility gains. A mean-squared-error loser can still improve constrained portfolio decisions because allocation utility weights forecast mistakes differently.

Over 1976-2005, only NTIS has positive $R^2$, at 0.10% and insignificant. SVAR is -22.47%, TBL -7.31%, TMS -7.24%, and D/Y -6.22%. Only six individual predictors have positive utility gains. Combination's positive but smaller gains in this interval are therefore the cleanest evidence that it does more than select a single strong model.

Over 2000-2005, D/P and D/Y have $R^2$ of 10.32% and 10.40%, with utility gains of 12.96% and 12.98%; I/K has 8.96% and 9.13%. Combination deliberately dilutes those ex-post winners. This illustrates the cost of robustness: it can lose to the best individual predictor selected after seeing the period, while outperforming a feasible benchmark consistently across periods. The source does not show that an investor could have selected those winners beforehand.

CT restrictions have little effect on combination $R^2$, but their utility effect is not always negligible. In the long sample, mean combination utility falls from 2.34% to 1.25%. Aggregation already moderates extreme predictions; imposing constraints first can remove useful variation that a portfolio rule would otherwise handle. The table should be read metric by metric rather than reducing this exercise to “restrictions do not matter.”

## Why averaging works: encompassing and variance reduction

Forecast encompassing asks whether adding forecast $j$ to forecast $i$ helps in a convex combination:

$$
\widehat r^*=(1-\lambda)\widehat r_i+\lambda\widehat r_j,
\qquad0\leq\lambda\leq1.
$$

The null $\lambda=0$ says $i$ encompasses $j$. With forecast errors $u_i,u_j$, define $d_t=(u_{i,t}-u_{j,t})u_{i,t}$. The modified Harvey-Leybourne-Newbold statistic used on p. 18 is

$$
MHLN=\frac{P-1}{P}\frac{\bar d}{\sqrt{\widehat V(\bar d)}},
\qquad
\widehat V(\bar d)=P^{-1}\widehat\phi_0,
$$

where $\widehat\phi_0$ is the sample second moment around $\bar d$, and significance uses a $t_{P-1}$ distribution. Table 2 is oriented by **column forecast encompassing row forecast**. Reversing that orientation reverses the interpretation.

Every individual predictor fails to encompass at least three others at the paper's chosen significance levels. D/P largely encompasses related valuation ratios but not most other forecast families. Combination forecasts fail to reject encompassing of the individual forecasts and of each other. These results support information diversity; they do not prove exact encompassing, and the many pairwise tests are not accompanied by a full family-wise correction.

Table 3 explains why averaging has room to stabilize forecasts. D/P and D/Y forecasts correlate 0.95; D/P and E/P 0.88. In contrast, D/P with TBL is -0.80, with LTY -0.84, and with SVAR only 0.05. NTIS and DFR forecasts have small correlations with many others. This is correlation of the *recursive forecasts*, not simply correlation of raw predictors or forecast errors.

For combination weights $w$, forecast variance is $w'\Sigma_{\widehat r}w$. Diversification reduces it when cross-forecast correlations are sufficiently low. But lower variance alone is not sufficient: the relevant exact decomposition is

$$
MSPE=(E[\widehat r]-E[r])^2+
\operatorname{Var}(\widehat r)+\operatorname{Var}(r)
-2\operatorname{Cov}(\widehat r,r).
$$

The paper uses the equivalent Theil decomposition and notes that predictive correlations are weak, making the variance and bias components especially important. The mean combination has lower forecast variance than all individual models and a squared bias near the smallest of theirs. Relative to the historical mean it has modestly more variance but much lower squared bias. This is empirical evidence from the same evaluation sample, not a universal theorem that averaging must beat the mean.

## Relation to the kitchen-sink regression

The unrestricted multivariate regression on all fifteen predictors has $R^2_{OS}$ of -19.35%, -35.50%, and -2.29% across the three windows. Combining forecasts and combining information are thus empirically very different even though both use the same variable list.

Demean the training observations, let $X$ collect predictors, and let $y$ be demeaned returns. The unrestricted slope estimator is $(X'X)^{-1}X'y$. Replacing $X'X$ with its diagonal yields the vector of univariate regression slopes $\widehat\beta_i$, but the resulting forecast is

$$
\widehat r^D=\bar r+\sum_i\widehat\beta_i(x_i-\bar x_i),
$$

which is still not the mean combination. The latter is

$$
\widehat r^C=\bar r+\frac1N\sum_i\widehat\beta_i(x_i-\bar x_i)
=\frac1N\sum_i(\widehat\alpha_i+\widehat\beta_i x_i).
$$

Thus equal averaging is representable as a restricted multivariate forecast whose slopes equal the marginal slopes divided by $N$. It shrinks the aggregate signal toward the training mean and avoids unstable inversion of the full predictor covariance. It is not ordinary ridge regression and does not shrink the unrestricted multivariate coefficients by a universal scalar.

The paper also notes collinearity. The actual predictor list contains relationships such as D/E = D/P - E/P and TMS = LTY - TBL, subject to consistent construction. Hence exact or near linear dependencies are a practical implementation issue, not only a theoretical possibility. The PDF does not fully document which redundant columns are dropped or how a singular kitchen-sink design is solved. Reproducing the negative kitchen-sink numbers requires that numerical convention; the forecast-combination formulas themselves remain well-defined.

## Links to macroeconomic conditions

Figure 6 aligns the mean combination forecast with six NBER recessions. Forecasts generally fall during expansions and rise around recessions, with prominent peaks near the troughs of the deeper 1970s/early-1980s contractions. These are descriptive comparisons using ex-post recession dates. The paper does not trade a contemporaneously observed NBER recession indicator.

The forecast for quarter $t$, formed earlier, correlates with realized quarter-$t$ growth. Table 4 gives mean-combination correlations of 0.28 with real GDP growth, 0.35 with real profit growth, and 0.34 with real net cash-flow growth, all significant at 1%. DMSPE with $\theta=0.9$ gives 0.34, 0.36, and 0.36. Positive correlations with *subsequent* growth are compatible with elevated risk-premium forecasts near recession troughs followed by recovery. They should not be mislabeled contemporaneous evidence that high realized GDP growth directly raises risk aversion.

Good, normal, and bad states are defined ex post by the top, middle, and bottom thirds of realized growth rates, separately for GDP, profits, and cash flow. At one quarter, mean combination $R^2$ is 1.82%, 1.71%, and 6.17% across GDP growth terciles. For profit growth the corresponding values are 2.87%, -1.03%, and 7.94%. Cash-flow growth differs: 5.44%, 2.17%, and 4.63%, so the highest gain is in the good tercile. “Especially bad growth” describes the dominant pattern, not every sorting variable.

Four-quarter forecasts use a direct regression of $r_{t+1}+\cdots+r_{t+4}$ on current predictors, with recursive estimation and a horizon-matched historical-mean benchmark. Overlapping targets require autocorrelation adjustment, for which Newey-West is used. Mean combination overall $R^2$ is 8.19%; GDP terciles yield 3.07%, 3.63%, and 11.58%, while profit terciles yield 0.93%, 4.89%, and 14.72%. The longer-horizon gain is not four independent quarterly successes: targets overlap and the effective information differs.

The same predictors are then used to forecast macro growth through

$$
y_{t+1}=\zeta_i+\eta_i y_t+\lambda_i x_{i,t}+\upsilon_{t+1}.
$$

An AR(1) with $\lambda_i=0$ is the benchmark. Individual ARDL forecasts are combined by the same rules. In 1965-2005, mean-combination one-quarter $R^2$ values relative to AR are 4.48% for GDP, 2.65% for profits, and 3.08% for cash flow. Four-quarter values are 10.08%, 7.51%, and 12.05%. In 1976-2005 the one-quarter values are 3.47%, 2.02%, and 1.65%; the cash-flow gain is not conventionally significant. This provides a more direct forecasting link to the economy than visual turning-point alignment, while retaining the macro-vintage limitation.

## Structural instability analysis

For break detection, the macro model omits lagged $y$ to mirror the equity-return regression and instead allows serially correlated disturbances:

$$
y_{t+1}=\zeta_i+\lambda_i x_{i,t}+\upsilon_{t+1}.
$$

Bai-Perron tests use 1947:Q3-2005:Q4, a maximum of eight breaks, and a minimum regime length of 10% of the sample. The UDmax and WDmax(10%) tests first assess no breaks against one to eight; sequential $F(l+1\mid l)$ tests select the number; break locations and regime parameters are then estimated. The complete sequential statistics and regime coefficients are not printed.

Both initial tests indicate breaks for fourteen of fifteen GDP-predictor models. Dates cluster around the early 1950s, mid-1970s, and 1980s. For D/P, estimated dates are 1953:Q2, 1959:Q2, 1966:Q1, 1975:Q1, 1985:Q3, and 1999:Q4. These are fitted break dates using the complete sample, not dates a trading system detected prospectively.

The authors apply Chow tests to equity-premium regressions at the corresponding macro break dates. Ten of the fourteen predictors with significant initial macro break tests also show significant equity-regression breaks. D/P's Chow statistic is 44.87, D/Y's 44.20, and SVAR's 26.84, each marked significant at 1%. D/E and I/K do not show significant corresponding equity breaks. Shared breaks support an economic connection and motivate combining unstable models, but cannot by themselves identify causation or establish a particular optimal adaptation rule.

## Replication limits and research assessment

The paper supplies a complete high-level recursive forecasting algorithm, weight formulas, portfolio constraint, principal evaluation windows, and extensive numerical evidence. Exact reproduction still needs the historical predictor files and transformations, the timing of quarterly data releases and revisions, CT sign conventions, effective first regression observations, covariance/standard-error choices, the singular-design convention for kitchen-sink OLS, and precise translation of log-return forecasts into realized portfolio arithmetic. No code or forecast series is embedded in the PDF.

The portfolio gains are gross of explicit trading costs, lack confidence intervals, and cover overlapping historical evaluation windows ending in 2005. The break and growth-tercile analyses are explanatory, not live conditioning rules. Forecast combination also inherits the selection of fifteen variables from an established literature, so it is not immune to the historical model-selection process merely because weights are simple.

The robust conclusion is narrower and useful: averaging weak, differently noisy aggregate-return forecasts can reduce estimation and instability costs enough to beat a constant-mean benchmark. The paper shows this statistically and economically in its sample and gives plausible macroeconomic structure to the resulting forecast. It supports keeping a simple forecast average as a demanding baseline for more elaborate timing models. It does not establish that every combination, every future period, or every macro risk model will deliver positive net investment value.

## Source map and bibliography

Pages 5-10 give recursive estimation, combination, Clark-West inference, and utility. Pages 10-17 and Table 1 define data and primary results. Pages 18-26, Tables 2-3, and Figures 3-5 explain encompassing, stabilization, and the multivariate-regression interpretation. Pages 27-33 and Tables 4-6 connect forecasts to growth; pages 34-37 and Table 7 cover structural breaks.

The main comparison is Welch and Goyal (2008), “A Comprehensive Look at the Empirical Performance of Equity Premium Prediction.” Bates and Granger (1969), “The Combination of Forecasts,” supplies the combination lineage; Stock and Watson (2004) supplies DMSPE weighting; Campbell and Thompson (2008) motivates the historical benchmark, restrictions, and utility comparison; Clark and West (2007) supplies adjusted nested-model inference; Bai and Perron (1998, 2003) supplies the break framework. This article is distinct from Neely, Rapach, Tu, and Zhou's later comparison of economic and technical predictors, despite similar opening words in their titles.
