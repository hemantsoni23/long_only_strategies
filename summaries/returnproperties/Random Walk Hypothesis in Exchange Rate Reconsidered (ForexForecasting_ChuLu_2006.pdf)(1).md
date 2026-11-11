# Random Walk Hypothesis in Exchange Rate Reconsidered

**Chia-Shang J. Chu and Hsin-Min Lu. Journal of Forecasting 25 (2006), 275–290. DOI: 10.1002/for.988.**

**Source:** [ForexForecasting_ChuLu_2006.pdf](../../Finance/ForexForecasting_ChuLu_2006.pdf), complete sixteen-page article, equations (1)–(13), Tables I–IX, four figures, and references. Page pointers below refer to printed pages. No separate appendix or executable code is included.

## Why this matters

The paper constructs a currency predictor from the changes in a hypothetical international equity allocation. Its proposed capital movement intensity, or CMI, index uses observable stock returns and exchange/forward rates rather than proprietary customer order flow. The intended mechanism is that changing expected investment opportunities induce cross-border reallocations, which contain information about subsequent exchange-rate movements.

The innovation is the complete chain from rolling return estimates to portfolio targets, from changes in those targets to generated regressors, and from those regressors to one-month currency forecasts. It is not a new portfolio optimizer or a structural market-clearing model. The authors explicitly describe the investor as hypothetical; they do not establish that actual investors follow this allocation rule or that the index measures observed dollar flows.

Results are strongest for Germany in the bilateral specification. Several countries show lower forecast errors, but evidence for Japan is weak after allowing for specification search. There are important qualifications to the headline claim of beating a random walk: the actual benchmark is an autoregression in exchange-rate changes, window lengths are selected using forecasting results, and some tables conflict with the accompanying prose. These distinctions should be preserved in a replication.

## Returns, currency conventions, and the assumed hedge

There are $N$ equity markets, with country $N$ designated domestic. Write $\widetilde R_{j,t+1}$ for a foreign market's local-currency simple holding return and $S_{j,t}$ for domestic currency per unit of foreign currency. An unhedged domestic investor earns

$$
R_{j,t+1}=(1+\widetilde R_{j,t+1})\frac{S_{j,t+1}}{S_{j,t}}-1,
\qquad j=1,\ldots,N-1,
$$

while $R_{N,t+1}=\widetilde R_{N,t+1}$ (equation 1). This return contains both the foreign equity movement and the currency movement, including their product. Simply adding the two percentage returns would be an approximation.

The empirical construction uses a fully hedged portfolio to avoid forecasting spot exchange rates inside the predictor. Denote by $F_{j,t}^{(t+1)}$ the one-month forward delivery rate known at time $t$. The assumed expected domestic return is

$$
\widehat R_{j,t+1|t}=(1+\widehat{\widetilde R}_{j,t+1|t})\frac{F_{j,t}^{(t+1)}}{S_{j,t}}-1.
$$

This writes equation (3) with an explicit information timestamp. The paper introduces the forward vector at time $t$ but labels the forward in that equation with $t+1$; the executable interpretation must be the delivery rate agreed using information available at $t$, not next month's observed forward quote. Forward premia affect the allocation even when spot forecasts are absent.

There is also a hedging idealization. Converting the entire uncertain terminal equity value at a predetermined forward rate is not what a fixed-notional forward on the initial investment guarantees. Such a hedge normally leaves currency exposure on the uncertain equity gain or loss. The paper assumes a fully hedged return for its hypothetical allocation, without specifying an implementable dynamic or contingent-notional hedging program. A reproduction should implement the displayed predictor assumption while keeping it separate from a claim that the associated portfolio can be traded exactly at those returns.

The bilateral home countries are Taiwan, Japan, Germany, and Singapore, each paired with the United States. Thus appreciation of the dollar is a rise in the domestic-currency-per-dollar quote. In the trilateral exercise the home country changes to the United States, while forecast targets remain yen per dollar and mark per dollar. Foreign-asset conversion for a U.S. investor requires the reciprocal of those target quotes. Failing to distinguish allocation-currency conversion from the dependent variable's quote orientation can reverse signs in the three-country implementation.

## Rolling Bayes–Stein estimates

At each date $t$, use $g$ monthly observations, from $t-g+1$ through $t$. Let $\bar r_t$ be the vector of sample means of local equity returns and $\widehat\Omega_t$ their sample covariance matrix. The source sets $k$ equal to the number of variables, corresponding to the number of assets in this construction. Equations (4)–(8) define

$$
\widehat V_{t+1}=\frac{g-1}{g-k-2}\widehat\Omega_t,
\qquad
\bar r_t^{\min}=\frac{\mathbf1'\widehat V_{t+1}^{-1}\bar r_t}
{\mathbf1'\widehat V_{t+1}^{-1}\mathbf1},
$$

$$
p_t=\frac{k+2}{k+2+g(\bar r_t-\bar r_t^{\min}\mathbf1)'\widehat V_{t+1}^{-1}
(\bar r_t-\bar r_t^{\min}\mathbf1)},
$$

$$
\widehat{\widetilde R}_{t+1|t}=(1-p_t)\bar r_t+p_t\bar r_t^{\min}\mathbf1.
$$

The shrinkage target is the estimated mean return of the global minimum-variance portfolio, not the arithmetic average across markets. The matrix inflation factor affects the shrinkage intensity even though a common scaling of $\widehat V$ cancels from the target mean. For an invertible positive-definite covariance and $g>k+2$, the displayed $p_t$ lies between zero and one. All reported window choices satisfy that denominator restriction for two or three assets.

The implementation uses the rolling sample covariance in the optimizer rather than fitting a multivariate conditional-volatility model. The authors motivate this choice by persistence in stock-market volatility and their focus on changes in expected returns. Persistence alone does not prove that covariance changes are unimportant for portfolio weights, especially when a small eigenvalue makes inversion sensitive. That is a limitation of the chosen proxy, not a reason to replace its covariance model without labeling the change.

An exact replication still needs the original return scaling and the sample-covariance convention. Scaling returns from decimals to percentage points scales means and covariances differently; with the same numerical risk-aversion coefficient, the optimizer's active positions will change. Covariance singularity handling, regularization, and extreme-weight truncation are not specified. Adding a ridge, a long-only restriction, or a leverage cap would generate a different CMI series.

The paper describes $\widehat\Omega_t$ using local stock returns and substitutes it for the conditional covariance in the allocation problem. It does not fully reconcile this with the currency-converted, forward-hedged expected return vector. Multiplying local returns by deterministic forward/spot ratios would also transform their covariance. Preserve the reported local-covariance construction as the baseline, and identify a consistently converted covariance as a sensitivity variant rather than quietly changing the original method.

## Portfolio targets and the CMI index

The investor solves equation (2):

$$
\max_w\quad w'\widehat u_{t+1|t}-\frac{\lambda}{2}w'\widehat\Omega_t w,
\qquad \mathbf1'w=1,
\qquad\lambda=2.
$$

Here $\widehat u$ contains the hedged domestic expected returns above. The only displayed constraint is full investment. Short positions and leverage are therefore allowed by the mathematical problem; this is not a simplex-constrained allocation. The negative-exponential-utility/normal-return motivation is a modeling justification, not an empirical verification of Gaussian equity returns.

For nonsingular $\widehat\Omega_t$, the optimizer has the closed form

$$
w^*_{t+1|t}=\frac1\lambda\widehat\Omega_t^{-1}
(\widehat u_{t+1|t}-\eta_t\mathbf1),
\qquad
\eta_t=\frac{\mathbf1'\widehat\Omega_t^{-1}\widehat u_{t+1|t}-\lambda}
{\mathbf1'\widehat\Omega_t^{-1}\mathbf1}.
$$

This solution follows from the budget-constrained first-order conditions; it is supplied here to make the stated optimization reproducible. The Hessian is $-\lambda\widehat\Omega_t$, so positive definiteness and positive risk aversion give a unique maximum. It is useful to verify the budget residual and first-order residual numerically at every date, rather than relying only on an optimizer's success flag.

The CMI vector is the change between successive optimal target weights:

$$
H_{t+1|t}=w^*_{t+1|t}-w^*_{t|t-1}.
$$

Because both targets sum to one, the full vector sums to zero. Only $N-1$ components can enter a regression with an intercept without exact dependence among all components. Equation (10) prints an $N-1$-component vector while subtracting full $N$-vectors; in code, form the complete difference and then select the designated nonredundant components.

The word “movement” needs a precise interpretation. A target-weight change does not equal the trade needed to rebalance a portfolio whose weights drifted with realized returns. The latter would compare the new target with post-return holdings. Nor does CMI incorporate investor wealth, subscriptions, redemptions, or heterogeneous investor demand. It is a generated reallocation-intention proxy. Its conservation property is in portfolio-weight units, not a balance-of-payments identity in dollars.

A positive CMI component means a larger target allocation to that market. It need not mean that actual aggregate capital entered it, or that any observed currency effect is caused by those trades. The predictor can work because it summarizes stock-return information correlated with currencies even if the literal capital-flow mechanism is incomplete.

## Currency regression and the actual benchmark

Let $x_t=\log S_t$ for the relevant forecast target. The main equation is

$$
\Delta x_{t+1}=\alpha_0+\alpha_1\Delta x_t+
\sum_{i=1}^{N-1}\beta_i h_{i,t+1|t}+\varepsilon_{t+1}.
$$

The comparator called “random walk” is

$$
\Delta x_{t+1}=\alpha_0+\alpha_1\Delta x_t+\varepsilon_{t+1}.
$$

An unrestricted AR(1) in changes is not a pure random walk in levels. A random walk with drift would additionally set $\alpha_1=0$, while a driftless random walk would set both coefficients to zero. The reported comparison tests the incremental value of CMI relative to the autoregressive benchmark actually estimated. The paper does not provide a separate complete forecast table for those two literal random-walk benchmarks.

CMI is generated with historical rolling estimates, so each historical regressor must be computed using its own information set. Recomputing all old targets with the latest window or using future fitted mean returns would leak information. Regression coefficients are themselves estimated in a separate rolling window of length $l=48$ months. There are therefore two distinct windows: $g$ generates CMI, while $l$ estimates its currency relationship.

## Dataset, timeline, and tuning

All inputs come from Datastream. Monthly spot exchange rates are daily averages within the month; one-month forward rates are end-of-period observations. Stock returns are one-month holding returns on major indexes: S&P 500, Taiwan Weighted Stock Index, Nikkei 225, and the stated weighted indexes for Singapore and Germany. The German code is given as `TOTMKBD`. Full series identifiers, dividend treatment, forward conventions, missing-data rules, and treatment of Germany after euro adoption are not supplied.

The Taiwan raw sample is November 1990–June 2001, 128 observations. Tables I and VI use January 1992–June 2001, 114 observations, for all regressions. Longer CMI windows, notably Germany's 24 months, require earlier equity data than that Taiwan start if the first tabulated regression date is to be retained. The article does not enumerate each country's raw starting date and complete usable-row mask; the Taiwan date should not be applied blindly to every input series.

The first stated forecast origin is April 1996, predicting May 1996. Both windows roll forward thereafter through the sample. May 1996–June 2001 gives 62 potential monthly forecast targets, assuming no omitted rows. That count is a calendar reconstruction, not a separately published count of effective forecast errors. A replication should export the actual origin/target list and check its endpoint treatment.

The bilateral selected $g$ values are 6 for Taiwan, 6 for Japan, 24 for Germany, and 11 for Singapore. Trilateral yen forecasts use 11 and mark forecasts 16. These choices came from extensive experimentation, including maximization of forecasting performance; they are not parameters selected only in the initial training period. The paper acknowledges data snooping and applies White's reality check. The resulting evaluation is more qualified than a completely untouched holdout experiment.

Monthly average spot quotes create another timing issue. A complete month's average is available only after the month ends. Pairing it with the month-end forward is possible at that point, but it does not describe execution at the month's average spot rate. Statistical forecasting dates and tradable entry prices must remain separate.

## Bilateral results

Table I reports statistically significant CMI slopes in all four country pairs. The fit measure is called adjusted $R^2$ in the prose but labeled $R^2$ in the table. Preserve that labeling ambiguity when comparing results.

| Home country | Benchmark fit | CMI fit | CMI slope | Standard error | $g$ |
|---|---:|---:|---:|---:|---:|
| Taiwan | 0.103 | 0.157 | 0.0011 | 0.00038 | 6 |
| Japan | 0.120 | 0.230 | 0.0012 | 0.00030 | 6 |
| Germany | 0.091 | 0.418 | 0.0020 | 0.00026 | 24 |
| Singapore | 0.075 | 0.161 | 0.0014 | 0.00038 | 11 |

Germany's lagged-change coefficient rises from 0.311 to 0.439 after adding CMI, while the fit increases markedly. These are in-sample relationships using a tuned generated regressor. Conventional coefficient standard errors alone do not account for every aspect of generated-predictor estimation and model search.

Out-of-sample results in Tables II–III are:

| Country | Benchmark RMSE | CMI RMSE | Benchmark MAE | CMI MAE | DM statistic | Reported one-sided $p$ |
|---|---:|---:|---:|---:|---:|---:|
| Taiwan | 0.0169 | 0.0161 | 0.0110 | 0.0102 | 2.153 | 0.015 |
| Japan | 0.0296 | 0.0279 | 0.0241 | 0.0205 | 1.458 | 0.070 |
| Germany | 0.0229 | 0.0194 | 0.0188 | 0.0154 | 2.321 | 0.010 |
| Singapore | 0.0190 | 0.0184 | 0.0118 | 0.0109 | 1.669 | 0.048 |

The errors are in log exchange-rate-change units. The implied RMSE reductions are approximately 4.7%, 5.7%, 15.3%, and 3.2%, respectively, calculated from the rounded table entries. MSE reductions are different because the ratios must be squared. Germany supplies the largest error reduction; Japan's lower errors are not significant at the displayed 5% DM threshold.

For the CMI forecasts, the Henriksson–Merton/Cumby–Modest timing statistics are 1.404/1.410 for Taiwan, 2.40/3.06 for Japan, 4.431/3.23 for Germany, and 1.81/1.83 for Singapore. The latter three pairs are starred at 5%; Taiwan is not. These timing tests concern different aspects of forecasts from squared-error comparison, explaining why Japan can pass them while failing the DM criterion. The paper cites the original tests rather than supplying complete computational definitions and finite-sample settings.

The DM loss differential is explicitly

$$
d_t=(100e_t^{B})^2-(100e_t^{CMI})^2,
\qquad e_t^m=\widehat{\Delta x}_t^m-\Delta x_t.
$$

Positive average $d_t$ favors CMI. The factor 100 is a numerical rescaling; under a consistently computed standard error it does not change the DM statistic. A standard implementation divides $\sqrt{P}\bar d$ by the square root of an estimated long-run variance of $d_t$. The article does not specify its exact long-run-variance estimator or bandwidth. Figures 1–4 show heterogeneous monthly gains and losses, including large spikes of both signs; average improvement does not mean that the model wins in every month.

## Specification search and the reality-check evidence

The reported search spans integer $g=6,\ldots,24$. The stationary bootstrap uses parameter $q=0.36$ and 1,000 bootstrap samples. Under the usual convention in which $q$ is a block-restart probability, this corresponds to expected block length $1/q\approx2.78$ observations. The article calls it a smoothing parameter and does not provide the complete resampling code, seed, centering formula, or treatment of all other tried specifications.

White's test is intended to compare the best model in a specified family with the benchmark while accounting for selection. A transparent implementation would retain the aligned loss-differential vector for every candidate and resample its time rows jointly, preserving cross-model dependence. This describes the required structure of a reality check, not an assertion that the paper publishes every algorithmic choice needed to reproduce its p-values.

Tables IV–V appear to accumulate the candidate family as the window range expands. At the final $g=24$ row, their adjusted p-values are 0.044 for Taiwan, 0.098 for Japan, 0.027 for Germany, and 0.008 for Singapore, matching the prose's overall bilateral conclusion. The tables do not explicitly define the family represented by each intermediate row, so that interpretation should be verified against original code. In particular, a row labeled 6 is not automatically a fully adjusted test over all nineteen windows.

Adjusted and naive values sometimes differ sharply. Germany's selected $g=24$ row gives 0.027 versus 0.001; Taiwan's $g=6$ row gives 0.004 for both, while its final-row adjusted value is 0.044. The search-adjusted evidence is consequently less uniform than a presentation of only the selected-window naive p-values would suggest. The reality check addresses the recorded candidate family, not unspecified experiments, choice of countries, predictor design, risk aversion, or every preprocessing decision.

## Trilateral results and source inconsistencies

For the U.S.–Japan–Germany portfolio, two nonredundant indices enter each forecast. In the printed equations, $\beta_1$ multiplies the German index and $\beta_2$ the Japanese index. Equation (13), for the mark target, nevertheless prints the lagged yen change as its autoregressive predictor. Its benchmark coefficients match the bilateral mark equation. This is an unresolved printed regressor inconsistency; replacing the lagged yen with the lagged mark may be plausible, but must be labeled a reconstruction until code confirms it.

Table VI's yen equation has CMI coefficients −0.00031 (standard error 0.00022) on Germany and −0.0025 (0.00044) on Japan. The mark equation has −0.0014 (0.00022) on Germany and −0.00048 (0.00043) on Japan. Only the own-country reallocation index is significant. Reported fits rise to 0.313 and 0.331, respectively. These negative coefficients coexist with positive bilateral coefficients because the home investor and selected weight components change; they should not be compared without reconstructing conventions.

The yen RMSE falls from 0.0296 to 0.0274 and MAE from 0.0241 to 0.0188. The mark RMSE falls from 0.0229 to 0.0212 and MAE from 0.0188 to 0.0167. Timing statistics are significant for both CMI models: 4.63/4.71 for yen and 2.79/2.70 for mark. Table VIII reports DM statistics 0.607, $p=0.28$, for yen and 1.729, $p=0.04$, for mark.

Table IX prints the yen $g=11$ DM statistic as −0.607, in conflict with the positive 0.607 in Table VIII. Its adjusted reality-check p-value is 0.209, compared with naive 0.013; the final-family row gives 0.280. Either way, the source does not establish robust yen improvement. For mark, the selected $g=16$ row has adjusted p=0.073, although the final-family rows 23–24 have 0.026. Thus a blanket claim that the selected mark specification passes every 5% criterion is too strong. The distinction between a family-level finding and evidence for a particular selected window matters.

## Reproduction priorities and practical interpretation

The essential reconstruction is feasible: recover the historical inputs and quote conventions; compute rolling local moments and Bayes–Stein means; convert expected returns using time-$t$ forward rates; solve the budget-only portfolio; difference successive targets; fit the rolling 48-month currency regression; and evaluate common one-month forecast origins for all nineteen CMI windows. Keep the benchmark definition and return scaling explicit. Save intermediate targets, CMI values, coefficients, and loss vectors so differences can be localized.

Exact numerical agreement additionally needs the complete Datastream identifiers and vintages, start-date masks, covariance conversion convention, numerical treatment of singular matrices, regression timing, the mark equation's disputed lag, and full DM/reality-check settings. The paper reports no portfolio PnL, bid–ask costs, financing costs, turnover, capacity, or utility gains from trading its currency forecasts. Lower forecast error therefore remains a statistical result, not a demonstrated net investment return.

The strongest useful idea is that a mechanically reconstructed allocation demand can summarize joint equity/currency information. Its weakest interpretation would be to call target-weight differences actual capital flows or treat a searched specification as an untouched trading rule. A follow-on experiment should freeze construction choices using a training period, retain literal random-walk and autoregressive benchmarks, and test subsequent vintages chronologically. That is an extension needed to assess deployability, rather than a result already delivered by the article.
