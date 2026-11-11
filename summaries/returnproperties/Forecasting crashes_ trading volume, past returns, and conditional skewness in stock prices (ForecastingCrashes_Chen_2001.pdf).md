# Forecasting crashes: trading volume, past returns, and conditional skewness in stock prices

Joseph Chen, Harrison Hong, and Jeremy C. Stein. *Journal of Financial Economics* 61 (2001), pp. 345–381. Source: [ForecastingCrashes_Chen_2001.pdf](../../Finance/ForecastingCrashes_Chen_2001.pdf). The local file contains the complete 37-page published article, including all eight tables and references; there is no separate appendix. Printed page numbers equal PDF page numbers plus 344.

## Why this matters and what is actually forecast

The paper asks whether information available today forecasts the asymmetry of daily stock returns during the next six months. Its main new empirical variable is an increase in a stock's trading turnover relative to its recent trend. Higher abnormal turnover predicts more negative subsequent skewness, controlling for lagged skewness, volatility, capitalization, and three years of past returns. Large prior price increases and larger capitalization also predict more negative skewness.

The title should not be read as a successful forecast of the dates of crashes or negative expected stock returns. The dependent variable is a realized higher moment over a future window. A distribution can become more negatively skewed without its conditional mean falling. A trader also cannot translate a forecast of physical-return skewness directly into an option mispricing without assumptions about risk premia and the distribution already reflected in option prices.

For a quantitative researcher, the useful contribution is a specified predictive panel and a demanding distinction between cross-sectional and aggregate evidence. The firm-level abnormal-turnover coefficient is statistically significant and survives several variations. The aggregate-market coefficient has the same sign and a larger economic scale but is very imprecisely estimated. The paper also translates skewness changes into hypothetical put-price changes; this is a calibration of economic magnitude, not an options backtest.

## Economic mechanism and scope of the theory

The motivating Hong–Stein model has investors with different information or interpretations who are constrained in selling short. An optimistic investor may set the market price while a pessimistic investor stays out of the market. The absence of the pessimist's negative information from the price creates a reservoir of information that becomes revealed when the optimist later receives bad news and withdraws. This can make price declines more abrupt than increases.

Disagreement is not directly observed. Trading volume provides a proxy: greater disagreement is associated with more trading, and the amount of potentially hidden information increases with disagreement. The empirical prediction is therefore that unusually high turnover forecasts more negative skewness. The paper summarizes the model and its assumptions rather than deriving and estimating a new structural equilibrium system. Its regressions are reduced-form tests of one implication, not estimates of private-signal precision or short-sale constraint parameters.

Past returns and size do not follow from the same prediction. The authors discuss stochastic bubbles as one possible reason that large run-ups precede negative skewness. They introduce an ex post disclosure explanation for small firms' greater positive skewness: managers may release good news quickly but reveal bad news more gradually, with greater discretion in less scrutinized firms. These are separate interpretations. The authors explicitly acknowledge the lack of a single theory explaining all three findings and do not claim their evidence uniquely establishes bubbles or discretionary disclosure.

Alternative turnover interpretations remain possible. Turnover may proxy for changing information arrival, liquidity, investment opportunities, or volatility rather than disagreement alone. The controls and robustness exercises address some confounds but provide no randomized or instrumental-variable source of exogenous turnover. The result is predictive association with an economically motivated sign.

## Dataset, universe, and timing

Section 3, pp. 352–359, uses CRSP daily and monthly observations from July 1962 through December 1998 for NYSE and AMEX common stocks. Nasdaq is excluded because its dealer-market trading-volume convention is not directly comparable. Common-stock share codes 10 and 11 exclude instruments such as ADRs, REITs, closed-end funds, and primes/scores. The main regressions retain firms above the 20th-percentile NYSE market-capitalization breakpoint. The smallest quintile is examined separately because illiquidity can make volume a poor measure of disagreement.

The individual-stock observations use nonoverlapping January–June and July–December windows. At each six-month endpoint $t$, construct the predictors using data through that endpoint; construct the dependent skewness measure over the following six months, $t+1$. A history of six six-month return blocks is required for the full specification. Table 5 lists 66 cross-sectional regressions with predictor dates from December 1965 through June 1998. Thus the raw data window is longer than the usable regression date sequence.

Any stock-window with more than five missing daily returns is excluded when constructing daily moments. The article does not provide a complete security identifier list, a vintage of CRSP, a full missing-lag flow chart, delisting-return handling, split-adjustment implementation, or the precise frequency at which the NYSE cutoff is updated. Reproduction should disclose these choices and reconcile the final counts before attributing small coefficient differences to economics.

The paper calls daily returns log changes in price. Its baseline series subtracts the daily log change in the value-weighted CRSP market index from the stock's daily log change. It also considers returns in excess of the Treasury-bill rate and beta-adjusted returns. The precise beta-estimation window and shrinkage or lag convention for the beta-adjusted version are not specified in the article. The baseline is reproducible without importing an assumed beta procedure.

A further distinction concerns dividends: the source's verbal description is price changes, while a CRSP implementation can choose return fields with or without distributions. The note preserves the stated log-return construction but does not invent an undocumented field choice. Similarly, the six-month cumulative return variable is not given an explicit compounding equation. A replication must record whether it uses summed log returns or geometrically compounded simple returns and match the source's tables.

## Constructing the dependent variables

Let $x_{id}$ be stock $i$'s daily market-adjusted log return on day $d$ of window $t$. Demean within the whole six-month window: $r_{id}=x_{id}-\bar x_{it}$. With $n$ usable daily observations, Eq. (1), p. 353, is

$$
\mathrm{NCSKEW}_{it}
=-\frac{n(n-1)^{3/2}\sum_d r_{id}^3}
{(n-1)(n-2)\left(\sum_d r_{id}^2\right)^{3/2}}.
$$

The leading minus sign makes larger values indicate greater negative skewness. The finite-sample adjustment is part of the source definition. Scaling by the cube of volatility allows comparisons across stocks with different variances. Using log returns also makes a lognormal price process a natural zero-skewness benchmark for log changes. Simple percentage returns mechanically have more positive skewness and a different relation to volatility; the authors report that substituting them does not overturn the main predictive coefficients.

The alternative DUVOL statistic avoids third powers. Split days into $D=\{d:r_{id}<0\}$ and $U=\{d:r_{id}>0\}$ with counts $n_d,n_u$. The printed Eq. (2), p. 354, reads

$$
\mathrm{DUVOL}_{it}
=\log\left[
\frac{(n_u-1)\sum_{d\in D}r_{id}^2}
{(n_d-1)\sum_{d\in U}r_{id}^2}
\right].
$$

There is a source inconsistency: the prose and table captions call DUVOL the log ratio of down-day to up-day **standard deviations**, but this displayed formula is a log ratio of variance-like quantities. A standard-deviation ratio would insert a factor one-half. Also, the displayed sums retain returns centered around the full-window mean rather than separate up/down means. This note gives the printed formula exactly and flags the ambiguity; it cannot identify the authors' unprovided implementation from the prose alone.

Uniformly halving both the dependent DUVOL and its lag would preserve the lag coefficient and $t$-statistics under a consistent linear rescaling, while halving coefficients on other regressors. Re-centering each sign group instead is not merely a constant rescaling and can alter the result. Reproduction should retain both candidate definitions for diagnosis and use Table 1's level and dispersion statistics to identify the intended scale. Windows with insufficient up or down observations or zero quadratic sums require an explicit missing-value rule, which the source does not supply.

These are noisy realized statistics, not direct estimates of a complete conditional return density. A few extreme days can strongly influence NCSKEW. The authors choose a six-month window partly to reduce high-moment measurement noise; the motivating theory does not uniquely specify that horizon. Shifted nonoverlapping calendars reportedly give similar results.

## Predictor definitions and estimating equation

Monthly turnover is shares traded divided by shares outstanding. TURNOVER is its mean across the current six-month window. DTURNOVER subtracts the mean monthly turnover over the preceding 18 months. With window endpoint month $m$, an explicit implementation of that stated timing is

$$
\mathrm{DTURNOVER}_{i,m}
=\frac16\sum_{j=0}^{5}\mathrm{TURN}_{i,m-j}
-\frac1{18}\sum_{j=6}^{23}\mathrm{TURN}_{i,m-j}.
$$

The current six months plus the prior 18 months form a 24-month data footprint. This is consistent with the article's explanation of the market-crash exclusion. The source describes the operation verbally rather than printing these indices; the equation here makes that timing explicit. Turnover enters as a fraction, so 0.01 means one percentage point of monthly turnover, not one share or one annual turnover unit.

SIGMA is the daily-return standard deviation during the current six-month period. LOGSIZE is log market capitalization at the endpoint. RET consists of six successive, nonoverlapping six-month cumulative return variables: the current window and five preceding windows, covering 36 months. In the baseline and beta-adjusted skewness regressions, these past returns are market-adjusted; in the Treasury-bill-excess version they are excess returns. A beta-adjusted dependent moment does not imply the lagged RET variables were also beta-adjusted.

The pooled main regression is

$$
\mathrm{NCSKEW}_{i,t+1}
=a_t+b_1\mathrm{NCSKEW}_{it}+b_2\mathrm{SIGMA}_{it}
+b_3\mathrm{LOGSIZE}_{it}+b_4\mathrm{DTURNOVER}_{it}
+\sum_{j=0}^{5}c_j\mathrm{RET}_{i,t-j}+u_{i,t+1}.
$$

Time dummies absorb common period-level shifts. There are no firm fixed effects in the reported baseline. The specification is estimated on the assembled panel, not in a rolling training/validation/test architecture. The predictor timing is forward-looking in the legitimate forecasting sense, but the coefficient estimates and reported fit are in sample. No hyperparameter search or out-of-sample prediction score is supplied.

The tables say $t$-statistics are adjusted for heteroskedasticity and serial correlation. The article does not give a fully reproducible covariance-estimator formula, kernel, bandwidth, or detailed clustering choice. One should not silently describe these as a particular modern two-way clustered estimator. Its separate Fama–MacBeth exercise offers a useful check based on the time series of cross-sectional coefficients.

## Main firm-level results

Table 2, p. 360, reports 51,426 observations. In the baseline, DTURNOVER has coefficient 0.437 and $t=3.839$. A one-percentage-point increase in detrended monthly turnover therefore predicts an increase of 0.00437 in the dimensionless NCSKEW measure, holding the included controls fixed. The corresponding coefficients are 0.364 with $t=3.175$ under beta-adjusted returns and 0.364 with $t=3.329$ under Treasury-bill-excess returns.

| Baseline predictor | Coefficient | Reported $t$ |
|---|---:|---:|
| Lagged NCSKEW | 0.053 | 7.778 |
| Daily SIGMA | −4.566 | −7.180 |
| LOGSIZE | 0.037 | 11.129 |
| DTURNOVER | 0.437 | 3.839 |
| RET, current six months | 0.218 | 10.701 |
| RET, previous six months | 0.082 | 4.296 |
| RET, two blocks back | 0.103 | 5.497 |
| RET, three blocks back | 0.054 | 2.830 |
| RET, four blocks back | 0.062 | 3.403 |
| RET, five blocks back | 0.071 | 3.759 |

All six return-lag coefficients are positive. The strongest is the most recent window, but information beyond a conventional one-year momentum horizon remains associated with future skewness. The coefficient on size means large stocks are more negatively skewed, conditional on the other variables. The negative volatility coefficient concerns conditional future skewness; it does not imply that increasing volatility reduces downside risk in dollars.

The baseline $R^2$ is 0.030, compared with 0.031 for beta-adjusted returns and 0.082 for excess returns. Statistical significance across a large panel coexists with low firm-level explanatory power. The larger excess-return fit can reflect common-market components absent from market-adjusted returns; it is not evidence that the turnover signal alone predicts 8.2% of skewness variation.

Table 1 provides useful construction checks. Across the broad firm sample, mean NCSKEW is −0.262, versus +0.268 for the market; mean DUVOL is −0.190 versus +0.172. Thus individual stocks tend toward positive skewness while the market tends toward negative skewness. NCSKEW and DUVOL have contemporaneous correlation 0.875. Their autocorrelations are only 0.047 and 0.090, while SIGMA's is 0.715. Predicting a noisy third moment is very different from predicting persistent volatility.

The average individual-stock skewness in a portfolio need not equal the skewness of portfolio returns, because the latter includes cross-asset co-moments. The paper notes a correlation of only about 0.22 between such measures across 25 size/book-to-market portfolios. This prevents a mechanical inference from the firm-level panel to market crashes.

## Robustness and interpretation of stability

Table 3, pp. 364–365, tests distinct concerns. Truncating extreme NCSKEW observations at three cross-sectional standard deviations within a time period leaves a turnover coefficient of 0.375 with $t=3.729$. Using raw turnover instead of detrended turnover gives 0.761 with $t=7.685$, on 52,229 observations. The caption incorrectly locates the undetrended specification in column 3; the table headings and entries place it in column 2.

Adding two further lagged volatility terms produces a DTURNOVER coefficient of 0.411 with $t=3.459$. Replacing lagged volatility with fitted future volatility produces 0.387 with $t=3.410$. The fitted-volatility first stage regresses next-window volatility on current and two lagged volatility measures, size, turnover, and all six return blocks. Its fitted value is a generated regressor; the article does not give a separate out-of-sample fitting protocol or a full generated-regressor inference adjustment.

Adding the latest available book-to-market ratio yields a book-to-market coefficient of −0.020 with $t=-3.808$ and a turnover coefficient of 0.455 with $t=3.848$, on 48,630 observations. Glamour stocks thus appear more negatively skewed conditional on the other regressors. The exact accounting publication lag and data linkage are not detailed enough to recover a point-in-time book-to-market panel without further choices.

Using DUVOL as the dependent variable and its own lag gives a DTURNOVER coefficient of 0.202 with $t=4.346$, current-return coefficient 0.142 with $t=15.810$, lagged DUVOL coefficient 0.096 with $t=16.627$, and $R^2=0.067$. This is evidence that the result does not depend solely on cubing a small number of extreme returns, subject to the definition issue above.

Table 4 splits by NYSE size quintiles. The turnover coefficients from largest to smallest are 0.404, 0.637, 0.551, 0.264, and 0.079, with respective $t$-statistics 1.812, 2.450, 2.554, 1.391, and 1.072. The weakest effect is in the smallest firms, consistent with the concern that trading frictions contaminate turnover there. It is inaccurate to say the coefficient is individually significant in every retained quintile. The tiny-stock specification also reverses the volatility coefficient and has a weak current-return coefficient, reinforcing the difference in measurement and population.

Table 5, pp. 368–369, estimates the same cross-sectional equation separately on 66 six-month dates and averages the coefficients. The average turnover coefficient is 0.532 with a serial-correlation-adjusted $t=3.981$. Decade-specific averages are 0.565 in the late 1960s, 0.592 in the 1970s, 0.486 in the 1980s, and 0.497 in the 1990s; their $t$-statistics are 2.280, 2.549, 1.372, and 2.326. Stable sign and similar scale across decades support the finding, but the 1980s subsample is not individually significant. There are 9, 20, 20, and 17 dates in these four groups.

Analyst coverage is a separate test of the ex post disclosure hypothesis. Table 6 uses December 1976–December 1998 I/B/E/S coverage, adding log one plus the number of analysts at the endpoint. On 40,688 observations, its coefficient is 0.019 with $t=4.059$ for NCSKEW and 0.006 with $t=3.288$ for DUVOL. Size remains positive and significant; turnover remains 0.504 with $t=3.504$ for NCSKEW. Fewer analysts are associated with more positive skewness conditional on size. Coverage is endogenous, so this does not prove discretionary disclosure caused the pattern.

## Aggregate-market experiment

Section 5 and Table 7, pp. 370–373, use value-weighted NYSE–AMEX market returns in excess of Treasury bills. The regressors mirror the firm specification, excluding size and time dummies. Each observation still forecasts a future six-month skewness window, but the endpoints now advance monthly, producing overlapping observations. Standard errors are adjusted for serial correlation, with the exact correction again not fully documented.

The main market regression has 401 usable observations. An alternative excludes observations whenever NCSKEW, DUVOL, SIGMA, or DTURNOVER draws on October 1987. Because detrended turnover uses 24 months, this removes 30 observations, leaving 371. It is not equivalent to dropping a single October 1987 row, nor is it a general exclusion of all regression variables containing that month: the footnote specifically names these four constructed variables.

For NCSKEW, turnover's coefficient is 6.002 with $t=0.262$ in the full sample and 9.349 with $t=0.828$ in the exclusion sample. For DUVOL the estimates are 6.324 with $t=0.704$ and 9.462 with $t=1.148$. None is statistically persuasive. A large point estimate divided by a very large standard error is not a reliable market-timing signal.

Past market returns show firmer evidence. The most recent six-month coefficient is 2.647 with $t=4.147$ for full-sample NCSKEW and 1.809 with $t=4.406$ excluding the crash observations. The six lag coefficients are positive throughout the four specifications, though not all individually significant. Full-sample $R^2$ values are 0.265 for NCSKEW and 0.304 for DUVOL, falling only modestly in the exclusion samples. These fits combine all predictors and overlapping windows.

The authors also examine NYSE volume data beginning in 1928 from Gallant–Rossi–Tauchen, originally from the S&P Security Price Record. Those data measure shares traded without shares outstanding, so the exercise uses detrended raw volume rather than actual turnover. The source describes similar findings but does not provide a complete additional table or implementation details. It should not be merged silently with the main turnover sample.

## Economic magnitude through a hypothetical option model

Section 6, pp. 374–378, uses a stochastic-volatility calibration adapted from Das–Sundaram. The source writes log price $p_t$ and variance $V_t$ as

$$
dp_t=a\,dt+\sqrt{V_t}\,dW_{1t},\qquad
dV_t=\kappa(\theta-V_t)\,dt+\eta\sqrt{V_t}\,dW_{2t},
\qquad d\langle W_1,W_2\rangle_t=\rho\,dt.
$$

Here $\rho$ controls return asymmetry. The thought experiment begins with symmetric log returns, holds the other parameters fixed, and changes $\rho$ enough to match the regression-implied change in daily skewness. The article refers to Eq. (21) of Das–Sundaram for the skewness mapping; it does not reproduce that formula, the option-pricing integrator, or its numerical tolerances.

The displayed constant log-price drift is also not by itself a complete risk-neutral option specification. For a conventional non-dividend-paying asset, risk-neutral log drift contains $r-V_t/2$. A physical skewness regression plus the two displayed diffusions does not specify variance-risk compensation or the full change of measure. The paper's values are best read as a particular calibrated economic metric imported from the cited model, not an independently identified no-arbitrage option-price forecast. An exact reproduction needs the referenced mapping and pricing conventions.

For individual stocks, set current and long-run variance to 0.16, corresponding to 40% annual volatility, with $\kappa=1$, $\eta=0.4$, initial price 100, interest rate zero, and maturity half a year. The standard deviation of DTURNOVER in the retained firm sample is 0.042. A two-standard-deviation increase therefore changes predicted NCSKEW by $2(0.042)(0.437)=0.0367$, rounded to 0.037. The source maps this to changing $\rho$ from zero to −0.38.

Table 8 Panel A gives put prices at strike 70 of 1.197 and 1.438, a reported 20.14% increase. Black–Scholes implied volatilities rise from 40.33% to 42.50%. At strike 80 prices rise from 3.044 to 3.297; at strike 100 they decrease slightly from 11.082 to 10.994. Changing skewness redistributes option value across strikes; it is not a uniform increase in all put prices.

For the market experiment, current and long-run variance are 0.04, or 20% annual volatility; other parameters remain the same. Market DTURNOVER has standard deviation 0.005. Using the highly uncertain turnover coefficient rounded to 6.00, the two-standard-deviation shock gives NCSKEW change 0.06 and an implied $\rho$ change from zero to −0.33. At strike 85, the put price rises from 0.859 to 1.070, a reported 24.66%, and implied volatility from 20.36% to 21.84%. The magnitude is conditional on the chosen coefficient and model; its statistical uncertainty is not propagated into a confidence band for the price change.

Past returns imply larger illustrative effects. A 40% individual-stock run-up changes predicted NCSKEW by about 0.087 and is mapped to $\rho=-0.920$, raising the strike-70 put from about 1.20 to 1.73, or 44.86%. In the market calibration, a run-up of only 7% already requires approximately $\rho=-0.978$. The article interprets the inability to encode still larger effects with $|\rho|\leq1$ as motivation for jumps. More narrowly, the chosen fixed-parameter diffusion cannot span the entire empirical skewness range; this is not a theorem that every pure diffusion is inadequate.

## Reimplementation priorities and practical limits

A first faithful implementation should reconstruct the baseline panel before adding any modern modeling choices. Match security filters, window dates, missing-observation rules, daily log-return centering, turnover's 24-month footprint, the six separate return lags, and the 51,426-observation regression. Reconcile the Table 1 moments and the DUVOL scale before comparing regression coefficients. Then reproduce the robustness table, size splits, and 66-date Fama–MacBeth averages with explicitly documented covariance estimation.

A separate market implementation should build monthly advancing six-month windows and trace every predictor's source dates before applying the October 1987 exclusion. This avoids either retaining contaminated constructed observations or deleting a much broader sample than the authors describe. The 401/371 counts are important checks, but matching them does not establish that the unspecified error estimator has been recovered.

For a genuinely prospective forecast, fit coefficients only using observations whose outcome windows have finished by the training date, then evaluate on later periods. This is a suggested extension, not a result in the article. Overlap means that random row splits can leak nearby future-return windows across training and evaluation. The source offers no such validation, transaction-cost model, portfolio construction rule, hedge rebalancing schedule, or option-trading performance.

The supported research takeaway is that abnormal trading activity and past appreciation contain information about future return asymmetry, especially across individual stocks, while aggregate-turnover evidence remains weak. The paper supplies a useful empirical design and a clear economic question. Its remaining reproducibility limits are concentrated in data-field conventions, DUVOL's conflicting definition, covariance estimation, and the imported option-pricing calculation; those should be resolved before claiming exact replication or an investable crash forecast.
