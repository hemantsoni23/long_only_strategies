# A Comprehensive Look at Financial Volatility Prediction by Economic Variables

**Authors:** Charlotte Christiansen, Maik Schmeling, Andreas Schrimpf. **Publication:** *Journal of Applied Econometrics* 27 (2012), 956-977. **DOI:** 10.1002/jae.2298. **Source:** [original PDF](../../Finance/VolatilityPrediction_ChristiansenSchmelingSchrimpf_2012.pdf). All 22 source pages were inspected. Printed page numbers equal PDF page numbers plus 955. The article's separate online appendix is not included in the library PDF; its [publisher attachment](https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjae.2298&file=MS%237658_OnlineAppendix_JAE_R2-final.pdf) could not be retrieved during this review. Missing appendix-dependent details are identified below.

## Why this matters

Persistent volatility is easy to forecast relative to an unconditional mean, but that does not establish that economic variables offer useful information beyond yesterday's volatility. This paper asks the incremental question across equities, foreign exchange, bonds, and commodities. It evaluates a broad predictor menu while accounting explicitly for uncertainty about which variables belong in the model. The important empirical finding is that credit conditions, funding stress, and variables related to time-varying risk premia are more reliable predictors than most conventional macroeconomic aggregates.

The contribution has three parts. First, the study uses an unusually long equity sample, beginning in 1926, alongside a common shorter sample across four asset classes. Second, it expands the predictor set to 38 financial and macroeconomic variables rather than selecting a small set ex ante. Third, Bayesian model averaging allows multiple candidate models to contribute to a forecast and treats variable relevance as a posterior inclusion probability. The paper compares this with classical model selection and simple equal-weight forecast combination.

The results are useful for designing a macro-conditioned risk forecast, not for claiming that a particular spread structurally causes volatility. A default spread or TED spread may summarize many common economic forces. Their inclusion probabilities and forecast coefficients identify conditional predictive information given this menu, frequency, and historical sample. They are not causal treatment effects, stable trading thresholds, or a guarantee of future performance.

## What is being forecast

For asset class $i$, let $r_{i,t,d}$ be the continuously compounded daily return on trading day $d$ in month $t$, with $M_t$ trading days. The source calls its dependent variable realized volatility and defines it as

$$
v_{i,t}=\log\sqrt{\sum_{d=1}^{M_t}r_{i,t,d}^{2}}
=\frac12\log\left(\sum_{d=1}^{M_t}r_{i,t,d}^{2}\right).
$$

This is equation (1), printed p. 959. It is log monthly standard deviation, not log variance, annualized percentage volatility, or an option-implied measure. The logarithm makes the distribution more nearly Gaussian and makes standard linear predictive regressions convenient. A one-unit change in its conditional forecast is a multiplicative change in standard deviation, whereas exponentiating a forecast of the log does not automatically deliver the conditional mean of volatility. A deployment requiring a level forecast needs a retransformation rule; the paper's reported scoring is on the logarithmic target.

The long S&P 500 sample runs from December 1926 to December 2010, 1,009 months. The shorter sample is described as January 1983-December 2010 for all four markets. The main text calls this 366 observations, but those endpoints imply 336 calendar months. This is an internal source inconsistency; use the underlying data dates to resolve the count before reproducing the estimation or forecast split.

The four return series are constructed as follows:

| Market | Underlying daily series |
|---|---|
| Equities | S&P 500 daily returns |
| Bonds | Closing-price returns on the CBOT 10-year Treasury-note futures contract, Datastream mnemonic CTYCS00(PS) |
| Commodities | S&P GSCI commodity-index returns |
| Foreign exchange | Daily spot-rate changes of an equally weighted basket of available currencies against the US dollar |

The bond futures avoid having to approximate bond returns from yield changes. For commodities, the authors use the cash index to extend the history before the GSCI futures began trading in 1992. Over 1992-2009, realized-volatility correlation between the index and its futures is 0.97. A researcher should not replace the long index history with a futures history and expect identical targets.

The FX universe is an unbalanced set of 48 currency jurisdictions listed in footnote 7, p. 959, including developed and emerging markets and the euro area. Available currencies are equally weighted each day. This forecasts volatility of an aggregate dollar portfolio; it is not the mean of each bilateral currency's volatility. Taking the volatility after portfolio aggregation includes cross-currency covariance. The correlation of the aggregate measure with major bilateral realized volatilities is 0.73-0.82 except for the yen, where it is 0.33. Individual-currency robustness results are referred to the missing appendix.

The long equity target has mean $-3.27$, standard deviation 0.52, and first three autocorrelations 0.78, 0.70, and 0.64. In the short sample, first-order autocorrelations are 0.66 for FX, 0.58 for bonds, 0.71 for stocks, and 0.77 for commodities. Pairwise target correlations are much smaller: FX-bonds 0.34, FX-stocks 0.25, FX-commodities 0.03, bonds-stocks 0.32, bonds-commodities 0.04, and stocks-commodities 0.48 (Table I). These numbers motivate both the autoregressive controls and separate asset-class models.

## Predictor menu and information set

The full design contains 38 economic variables; the long equity sample uses 13 with sufficiently long histories. The complete abbreviations, transformations, sources, and availability flags are relegated to Appendix Table A.1/IA.1. The local article supplies the following economically important definitions, but not a complete stand-alone dataset recipe for all 38 columns.

Equity predictors include log dividend-price and earnings-price ratios, market excess returns, Fama-French size and value factors, a short-term reversal factor, and S&P 500 turnover. Past market returns capture the negative return/future-volatility association. Valuation ratios proxy for risk premia and leverage-related state changes; turnover may proxy for disagreement or uncertainty. These interpretations need not be exclusive.

Bond predictors include the Treasury-bill rate, the term spread, and the Cochrane-Piazzesi bond-premium factor based on forward rates. Currency predictors include average forward discount, a dollar risk factor, and a carry-trade factor. The average forward discount summarizes interest-rate differentials against the United States rather than being a realized FX-volatility statistic.

Credit and liquidity inputs include the BAA-minus-AAA corporate yield spread, the three-month LIBOR-minus-Treasury-bill TED spread, aggregate FX bid-ask spreads, and the Pastor-Stambaugh equity-liquidity measure. General macro inputs include inflation, industrial production, money growth, housing starts, capacity utilization, and business-cycle indicators. Several growth series are considered at monthly and annual frequencies.

All economic predictors enter with a one-month lag in the baseline regression. That timing avoids direct contemporaneous fitting, but the main PDF does not establish a complete real-time-vintage and release-lag policy for every macro series. Revised data and unavailable month-end releases remain potential differences between the historical experiment and a live forecast. Nor should coefficients in the tables be interpreted as percentage-point sensitivities without confirming the appendix's normalization. The note reports coefficients in the source's tabulated units and leaves unverified scaling explicit.

## Regression family and model uncertainty

For a candidate model $M_j$, the baseline predictive equation is

$$
v_{i,t}=a_j+\sum_{\ell=1}^{L}\rho_{j,\ell}v_{i,t-\ell}
+\beta_j'z_{j,t-1}+u_{j,t}.
$$

Here $z_j$ selects a subset of the economic predictors. The main specification uses one volatility lag; robustness adds the second and third lags. The pure autoregression is the benchmark, so any incremental explanatory power must survive a persistence control. The paper counts $2^{39}=549,755,813,888$ candidate specifications when the 38 economic variables and the first volatility lag are treated as potential inclusions. This is why it uses stochastic model-space exploration instead of enumerating the entire set.

For data $D$, posterior model weights are

$$
w_j=p(M_j\mid D)=\frac{p(D\mid M_j)p(M_j)}{\sum_m p(D\mid M_m)p(M_m)},
$$

with marginal likelihood

$$
p(D\mid M_j)=\int p(D\mid M_j,\beta_j)p(\beta_j\mid M_j)\,d\beta_j,
$$

where the displayed integral suppresses other nuisance parameters. Forecasts are combined using these posterior weights. A coefficient absent from a model is zero when calculating an unconditional model-averaged coefficient. The posterior inclusion probability for variable $k$ is

$$
PIP_k=\sum_j w_j\mathbf1\{k\in M_j\}.
$$

The prior inclusion probability is 0.5. Independent inclusion at this value gives equal prior probability to all models, but it does not give equal probability to all model sizes: intermediate sizes have many more distinct models. A posterior probability above 0.5 means the data have increased the variable's inclusion probability relative to this prior. It does not correspond to a frequentist significance level.

The baseline in-sample search uses 500,000 MC3 draws with 50,000 burn-in draws. MC3 means Markov-chain Monte Carlo model composition, a chain moving through model specifications rather than just sampling coefficients in a single regression. The short description in the local PDF does not give the proposal kernel, coefficient prior and hyperparameters, exact marginal-likelihood formula, convergence diagnostics, or the full bootstrap algorithm. Those details reside in the unavailable online appendix. Writing an arbitrary Zellner prior or a guessed transition kernel into the replication recipe would change the method without evidentiary support.

Model-averaged standard deviations include model uncertainty. Therefore the reported Bayesian coefficient-to-standard-deviation ratios should not be read as classical regression t-statistics. The uncertainty associated with variable inclusion can remain substantial even when the variable appears in a high-ranking individual model.

## Classical selection and forecast combinations

The classical alternative first screens each candidate in a regression containing that predictor and lagged volatility. Only predictors with an absolute t-statistic greater than two survive. All subsets of this reduced set can then be evaluated, and the models are ranked by BIC. Tables IV-V report the three best models, their adjusted and unadjusted $R^2$, and HAC inference using Newey-West standard errors with Andrews' automatic lag selection.

This screening is a computational simplification, not equivalent to the full-space Bayesian model average. Model selection after screening adds uncertainty that a single reported coefficient's conventional t-statistic does not fully describe. For a valid out-of-sample reproduction, screening must be repeated using only data in the current estimation window.

The forecasting comparison includes six approaches: the single best model by BIC, by AIC, or by adjusted $R^2$; analytically evaluated BMA after trimming predictors; BMA using MC3; and equal weighting of the evaluated models' forecasts. The latter combines models, not raw predictors. Equal weighting does not require the posterior probabilities to be well estimated and provides a useful reference for the value of elaborate Bayesian weights.

For computational reasons the out-of-sample MC3 search uses only 1,000 draws at each origin, versus 500,000 in-sample. That is a material algorithmic difference. Posterior rankings from the long in-sample chain are not themselves the real-time forecast weights. An implementation should save and assess Monte Carlo stability by origin rather than infer that the two versions are computationally interchangeable.

## What the in-sample estimates say

For long-sample equities, Table II reports:

| Predictor | Inclusion probability | Posterior mean | Posterior SD |
|---|---:|---:|---:|
| Lagged log volatility | 1.00 | 0.617 | 0.027 |
| Default spread | 1.00 | 0.117 | 0.014 |
| Market return | 1.00 | -0.051 | 0.011 |
| Earnings-price ratio | 0.97 | -0.037 | 0.012 |
| Short-term reversal return | 0.89 | -0.030 | 0.015 |

The composite pseudo-$R^2$ is 0.645 against 0.606 for the AR(1) benchmark, an increase of 3.9 percentage points. The mechanism suggested by the signs is higher volatility after greater credit stress, lower market returns, and high valuations. The negative coefficient on reversal-strategy returns is interpreted cautiously: returns to liquidity provision may be followed by easing stress at the monthly horizon. This is not the same claim as a contemporaneous relation between daily reversal profits and stress.

Adding volatility lags does not remove the central financial predictors. In Table VI, the three autoregressive coefficients are 0.456, 0.178, and 0.102; their inclusion probabilities are 1.00, 1.00, and 0.93. Market returns, default spreads, and short-term reversal retain probabilities 1.00, 1.00, and 0.99, with posterior means $-0.065$, 0.077, and $-0.041$. Earnings-price relevance falls to a 0.48 probability. The composite pseudo-$R^2$ becomes 0.665 compared with the higher-order autoregressive benchmark's 0.632.

Short-sample results in Table III differ by asset. FX selects average forward discount with probability 0.99, annual M1 growth 0.93, annual inflation 0.84, TED 0.77, monthly industrial-production growth 0.69, and housing starts 0.58. Its pseudo-$R^2$ rises from 0.433 to 0.545. Thus the general conclusion that pure macro variables are weak has an important exception in the currency aggregate.

For bonds, turnover has probability 0.95 and a negative coefficient, default spreads 0.86 with a positive coefficient, and term spreads 0.73 with a positive coefficient. TED ranks among the top eight but its probability is only 0.29. It would overstate the table to call TED a strongly included predictor in every asset class. Bond fit rises from 0.335 to 0.433.

For short-sample equities, dividend-price, TED, and default spreads have probabilities 0.96, 0.92, and 0.92. Their posterior means are $-0.119$, 0.070, and 0.095. Fit increases from 0.507 to 0.591. For commodities, the leading economic probabilities are more diffuse: turnover 0.67, Cochrane-Piazzesi 0.60, and the Treasury-bill rate 0.55. Their Bayesian t-ratios are modest, consistent with greater model uncertainty. Commodity fit increases from 0.597 to 0.659.

## Out-of-sample design and inference

Models are estimated recursively with an expanding window. At each origin, reestimate the regressions, redo the applicable search or screening, produce the next month's forecast, reveal the next observation, and expand the training sample. Long equity evaluation starts separately in January 1937, January 1957, and January 1977. The multi-asset short-sample forecasts begin in February 1993 following roughly ten years of initialization. Forecasts are one month ahead; the paper avoids overlapping multi-month horizons in its principal Bayesian exercise and refers quarterly-horizon checks to the appendix.

The key statistics are

$$
U=\sqrt{\frac{\sum e_{M,t}^{2}}{\sum e_{AR,t}^{2}}},\qquad
R^2_{OOS}=1-\frac{\sum e_{M,t}^{2}}{\sum e_{AR,t}^{2}}=1-U^2.
$$

Here $U$ is Theil's relative RMSE. It is below one when the macro-finance model beats the autoregression. A five-percent $R^2_{OOS}$ is a five-percent reduction in squared forecast error, not five percent of total volatility explained and not an investment return.

The authors use a model-based wild bootstrap imposing no incremental economic predictability because standard nested-model asymptotics do not directly account for model search and forecast combination. The reported one-sided bootstrap p-value is the fraction of simulated Theil statistics below the observed statistic. They also report Giacomini-White statistics and GLS Mincer-Zarnowitz tests of zero intercept and unit forecast slope. These answer different questions: lower average loss does not establish calibration, and failure to reject calibration does not establish economically useful performance.

## Numerical forecast evidence

For the long equity sample, Table VIII gives the following $R^2_{OOS}$ values:

| Forecast start | BIC | AIC | Adjusted-$R^2$ selection | Analytical BMA | MC3 BMA | Equal weights |
|---|---:|---:|---:|---:|---:|---:|
| 1937 | 5.9% | 6.2% | 5.9% | 6.9% | 6.8% | 7.4% |
| 1957 | 1.9% | 2.3% | 2.7% | 3.1% | 2.9% | 4.1% |
| 1977 | 5.3% | 5.4% | 5.8% | 5.4% | 5.3% | 5.4% |

Equal weights do particularly well for the first two starts; no method dominates all periods. For the 1937 start its Theil statistic is 0.962, its GW statistic 3.52, and its MZ p-value 0.35. For the 1957 start, its GW statistic falls to 1.70 even though the bootstrap p-value is printed as 0.00. Printed zero is rounding, not proof that the event has zero probability. The disagreement in apparent strength across tests should be retained.

For the short sample, Table IX reports:

| Market | BIC | AIC | Adjusted-$R^2$ selection | Analytical BMA | MC3 BMA | Equal weights |
|---|---:|---:|---:|---:|---:|---:|
| FX | 10.2% | 11.2% | 9.7% | 7.9% | 6.5% | 11.2% |
| Bonds | 6.1% | 8.1% | 6.1% | 7.6% | 5.4% | 9.0% |
| Stocks | 0.4% | 6.6% | 7.8% | 4.8% | -2.0% | 5.6% |
| Commodities | 5.8% | 9.6% | 10.8% | 11.3% | 5.8% | 8.5% |

These values disprove a blanket claim that BMA always helps: MC3 BMA loses to AR(1) for short-sample equities, with $U=1.010$ and bootstrap p-value 0.49. Equal-weight FX forecasts improve squared loss by 11.2% but fail the MZ calibration test at the displayed precision. Analytical BMA commodities has the strongest reported GW statistic in that panel, 3.34. Higher-order autoregressive benchmarks reduce the short-sample success further, according to the article's discussion of appendix results.

Figure 3 accumulates benchmark squared errors minus model squared errors. An upward segment means the economic model is gaining ground locally; the level reflects all preceding gains and losses. The long equity BMA performs poorly in the late 1990s/early 2000s and better during the 2007-2009 crisis. A favorable full-period statistic therefore conceals economically important variation in reliability.

## Replication boundary and practical interpretation

A defensible reconstruction should preserve the logarithmic target, one-month horizon, full training-window model search, and the distinction between the 13-variable long sample and 38-variable shorter sample. It should reconcile the short-sample count, obtain the appendix's exact transformations and Bayesian priors, and document forecast-origin information availability. A minimal validation sequence is to reproduce target autocorrelations, AR benchmark fits, long-sample posterior inclusion rankings, and then Table VIII/IX relative losses. Matching only the final $R^2$ would not verify that the same method had been implemented.

The local PDF cannot settle all replication inputs. The online appendix contains prior and MC3 details, predictor data definitions, and the wild-bootstrap recipe. Its publisher URL and the linked [JAE data archive](https://qed.econ.queensu.ca/jae/datasets/christiansen001/) were located, but the appendix fetch returned a forbidden response and the archive was unavailable during this inspection. These limitations concern exact reproduction; they do not prevent reading the source's main equations, tables, figures, and conclusions.

The practical lesson is to treat financial conditions as incremental risk information while maintaining an autoregressive benchmark and simple combination alternative. Default and funding spreads repeatedly survive controls, but their importance is conditional on asset class and historical regime. In the study, elaborate posterior weighting is not consistently better than equal weighting. Better forecasting loss also does not by itself determine a leverage rule, a portfolio hedge, or an option price. No costs, turnover, leverage constraints, realized utility, or investment-capacity calculation is supplied. Those decisions require explicitly matching the forecast's logarithmic monthly object to the intended economic loss.
