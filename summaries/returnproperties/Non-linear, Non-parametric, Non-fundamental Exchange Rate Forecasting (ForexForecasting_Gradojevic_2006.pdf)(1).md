# Non-linear, Non-parametric, Non-fundamental Exchange Rate Forecasting

**Authors:** Nikola Gradojevic and Jing Yang. **Publication:** *Journal of Forecasting* 25 (2006), 227–245. **DOI:** 10.1002/for.986. **Source:** [ForexForecasting_Gradojevic_2006.pdf](../../Finance/ForexForecasting_Gradojevic_2006.pdf). Page references below use printed journal pages; PDF page 1 is page 227. This note covers the entire 19-page source, including its seven empirical tables and methodological qualifications.

## Why this matters

The central question is whether yesterday's information about who bought and sold currency helps forecast tomorrow's exchange-rate change once the relation is allowed to be nonlinear. Gradojevic and Yang combine Canadian dollar order flows with interest-rate and oil-price changes in small feedforward neural networks. Their strongest result is 71.56% directional accuracy for a network with separately identified customer, domestic interbank, and foreign-institution flows, against 54.88% for their random-walk benchmark in a 225-observation recursive evaluation. The corresponding reduction in mean squared prediction error is much smaller, approximately 4.60%.

This distinction matters for replication. A model can improve the sign of numerous small movements while barely reducing squared error, and neither statistic establishes an executable trading profit. The paper estimates changes in the **real** Canadian/US exchange rate, uses a proprietary bank-reporting dataset, and reports no transaction-cost-adjusted strategy. Its contribution is evidence about forecasting with disaggregated microstructure information, rather than a complete currency trading system.

The useful research design is a nested comparison: aggregate versus disaggregated order flow, linear versus nonlinear mapping, and fixed fitted models evaluated over a test block versus models re-estimated before each forecast. The published numerical evidence favors the nonlinear mapping, especially with flow disaggregation and daily updating. However, missing network settings, inconsistent descriptions of sample boundaries and weekly targets, and the treatment of validation prevent exact reproduction from the PDF alone. Those limitations should be treated as constraints on the evidence, not filled with invented hyperparameters.

## Contribution and economic mechanism

Traditional exchange-rate models emphasize macroeconomic quantities that move slowly or are measured infrequently. Microstructure models emphasize the information conveyed by trading and inventory adjustment. This paper's innovation is to combine a small macroeconomic feature set with order-flow composition through neural networks, using roughly a decade of daily Canadian/US observations rather than a short contemporaneous price-impact sample.

The proposed mechanism is that customer and institutional transactions contain heterogeneous information about desired portfolios and future fundamentals. Dealers learn from those transactions, and inventory adjustment or gradual information aggregation can transmit yesterday's flow into later prices. Positive net purchases of US dollars are intuitively associated with depreciation of the Canadian dollar when the quote is Canadian dollars per US dollar. Figure 1, page 232, shows cumulative aggregate flow and the real exchange-rate level moving together, plus a shorter comparison involving interbank flow in December 1999–February 2000.

That figure motivates the variables but is not a causal identification strategy. Cumulative variables can co-move without providing useful lagged forecasts, and exchange rates can themselves influence order flow. The subsequent predictive models use lagged flows and changes in exchange rates. Their estimated signs need not equal the positive contemporaneous association suggested by the figure. Indeed, several reported lagged-flow coefficients are negative.

The source does not claim a new neural-network architecture. Logistic and hyperbolic-tangent units, backpropagation, and validation-based early stopping are standard tools used to make the economic comparison. Nor does a universal approximation result establish that the fitted network is correctly specified, optimally trained, or predictive in a new regime. The paper assumes early stopping yields a sufficiently well-behaved response estimate; it does not prove consistency for its particular finite-sample procedure.

## Data, units, and transformations

The core dataset consists of 2,230 observations described in the main text as daily data from January 1990 through June 2000. The Figure 1 axis instead begins March 5, 1990, and Table I labels its sample January 1990 through July 2000. These are unresolved source differences. A replication needs the actual dated data file, including missing days and alignment rules; the date range alone cannot reconstruct the observation index.

Order flows come from the Bank of Canada's Daily Foreign Exchange Volume Report, organized through the Canadian Foreign Exchange Committee. Six major Canadian commercial banks account for approximately 83% of Canadian/US dollar transactions in the coverage description. Another 4% occurs within Canada outside those banks, and 13% in the United States and the rest of the world. Thus the observations capture an important segment, not all global trading in the pair.

The study uses spot transactions. It distinguishes:

| Symbol | Counterparty category | Inclusion |
|---|---|---|
| $CC_t$ | Resident and nonresident nonfinancial commercial customers | Included |
| $CD_t$ | Canadian non-dealer financial institutions | Excluded: unavailable before 1994 |
| $FD_t$ | Foreign financial institutions, including FX dealers | Included |
| $IB_t$ | Domestic interbank counterparties, including chartered banks, credit unions, investment dealers, and trust companies | Included |

Aggregate flow is $A_t=CC_t+IB_t+FD_t$. The data description first calls the underlying flows trading amounts in Canadian dollars, then defines order flow as the difference between the “number” of purchases and sales. The PDF does not resolve whether the supplied regressor is signed monetary volume or signed transaction count, nor the scaling unit. Because coefficients depend directly on that unit, a reproducer should obtain the data dictionary rather than infer units from the coefficient magnitudes.

Let $S_t$ be the nominal CAD-per-USD exchange rate and let $P_t^{US}$ and $P_t^{CA}$ denote consumer price indices. A conventional real quote compatible with this orientation is $Q_t=S_tP_t^{US}/P_t^{CA}$, with $q_t=\log Q_t$ and daily target $y_t=q_t-q_{t-1}$. This formula is an explicit reconstruction of the described CPI adjustment; the paper says it uses the two countries' CPIs but does not print the exact transformation or interpolation rule. It also does not explain how monthly CPI release dates, revisions, or daily carry-forward values are handled. A real-time experiment must use only information available at each forecast date.

The two macroeconomic inputs are the change in the Canada-minus-US nominal 90-day commercial-paper rate differential, denoted $\Delta d_t$, and the daily change in the logarithm of the crude-oil closing price after deflation by US CPI, denoted $\Delta o_t$. Oil is quoted in US dollars. The exact oil series, commercial-paper data identifiers, closing-time alignment, holiday calendar, and interest-rate units are not given. These choices matter because a one-day predictor can inadvertently incorporate prices observed after the exchange-rate measurement.

Although the prose says all variables are considered in first differences, the displayed forecasting equations use $CC_t$, $IB_t$, and $FD_t$ directly. Daily signed flow is already a period quantity; it is not the cumulative-flow series plotted in Figure 1. Table I rejects a unit root in those daily flow levels. The most literal implementation of the empirical equations therefore uses daily flows without an additional first difference. This is a documented interpretation of inconsistent prose, not a claim that the original code has been recovered.

The full-sample augmented Dickey–Fuller statistics support differencing the macroeconomic level variables. For real exchange rates, interest-rate differentials, and oil prices, the reported level statistics are respectively −0.84, −1.48, and −2.42, compared with a 1% critical value of −3.43. Their changes have statistics −34.31, −19.90, and −31.35. Flow-level statistics are −25.31 for commercial clients, −23.43 for foreign institutions, and −31.12 for interbank flow. Lag counts differ across tests, ranging from one to ten; the lag-selection procedure is not supplied. These tests address unit roots, not stability of the conditional forecasting relation.

## Forecasting models and information sets

The daily versions of the two network specifications can be written cleanly as

$$
\widehat y_t=f_\theta(\Delta d_{t-1},\Delta o_{t-1},A_{t-1})
$$

and

$$
\widehat y_t=g_\psi(\Delta d_{t-1},\Delta o_{t-1},CC_{t-1},IB_{t-1},FD_{t-1}).
$$

These are ANN 1 and ANN 2. The paper refers to four- and six-variable datasets because it includes the target in the count; the networks have **three and five input neurons**, respectively. Neither specification includes lagged exchange-rate changes as a separate input. This distinction prevents an unintended autoregressive extension during reconstruction.

The source generalizes the input lag to $j\in\{1,7\}$ and calls the latter a one-week-ahead forecast. Yet it retains $\Delta q_t$ notation, while its random-walk equation is $q_t=\alpha_0+q_{t-j}+\gamma_t$. It does not explicitly state whether the weekly target is a seven-period cumulative change, a one-period change forecast seven periods ahead, or a calendar-week change after resampling. Seven observations also need not be one business week. The much larger weekly RMSE is consistent with a longer-horizon target, but this is not sufficient to settle the definition. Weekly reproduction requires resolving that target alignment before any model is trained.

For the daily benchmark, the displayed random walk includes a drift $\alpha_0$. Its forecast of the next change is therefore an estimated constant, not identically zero. This matters for direction accuracy: a driftless random walk has zero forecast changes and, under the paper's strict-positive product rule, would not generate the reported 54.88% hit rate. The drift estimation window and updating convention are not fully detailed.

LM 2 is the ordinary linear counterpart of ANN 2, with an intercept and separate coefficients on the five predictors. LM 1 is intended to be the aggregate-flow counterpart of ANN 1, as shown by Table II. However, Equation (15), page 237, prints $IB_{t-j}$ where the table uses aggregate flow. A replicator should report this discrepancy and test the table-consistent aggregate-flow specification rather than silently treating the two as identical.

The networks have one or two hidden layers: three layers including input and output, or four layers including two hidden layers. Hidden-node counts vary between three and five. Hidden activation functions are logistic,

$$
\sigma(z)=\frac{1}{1+e^{-z}},
$$

or hyperbolic tangent. The output layer has one linear neuron, allowing either positive or negative predicted changes. A one-hidden-layer implementation has the form $\widehat y=b_0+\sum_{h=1}^{H}v_h\sigma(b_h+w_h'x)$. This is a transparent representation of the described architecture, not a recovered fitted equation.

Training uses feedforward backpropagation and stops when error on the validation set begins increasing. All data used for the ANN are normalized to $[-1,1]$. The exact affine scaling formula, whether extrema come from training data or the entire sample, the chosen hidden-layer configuration for each reported model, learning rate, initialization distribution, random seeds, number of restarts, epoch limit, and validation patience are not reported. No final weights or software implementation are provided. The prose acknowledges constant-learning-rate difficulties and uses early stopping rather than a theoretically specified declining matrix learning rate.

A faithful methodological reconstruction can select a network from the disclosed architecture family using only training and validation observations. It cannot claim to reproduce the exact published network. In particular, fitting the normalization on the final test sample would use future extrema; that must be avoided in a new experiment even though the source is unclear about its original practice.

## The two evaluation experiments

The paper's evaluation is easier to understand when its two experiments are kept separate. They use overlapping information and should not be combined as independent evidence.

First, the authors fit on the initial 2,005 observations and forecast a remaining block of 225. They then add ten observations to the estimation sample and shrink the terminal testing block by ten, producing 18 RMSE comparisons with test sizes 225, 215, and so on down to 55. Within each block the fitted model is not re-estimated before every forecast. Lagged input observations can nevertheless change across dates in that block. This is a series of expanding-estimation, shrinking-test comparisons, not a fixed-size rolling window and not 18 independent holdouts.

For direction statistics, analogous test sizes run from 225 down to five in steps of five. Table V reports averages across those evaluations. Consequently its average percentage is not necessarily the hit rate of one single chronological sequence with each date counted once. Later observations receive repeated representation in overlapping test blocks.

The general methodological description states that training, validation, and testing proportions remain 6:3:1 throughout the recursive experiment. That cannot be literally reconciled with a fixed 2,230-observation endpoint and successively shrinking test sets without an additional rule. An initial split of 60% training, 30% validation, and 10% testing is understandable; the allocation of the growing estimation portion between training and validation thereafter is not specified. Chronological allocation should be maintained in a reconstruction, but the chosen update rule must be disclosed as an assumption.

Second, Table VI evaluates a daily recursive one-step-ahead procedure: re-estimate using observations available before each target date, forecast that date, add the newly observed target, and repeat across 225 testing observations. The text says the initial estimation sample has 2,006 observations while still leaving 225 out of a total of 2,230. This is an off-by-one inconsistency, distinct from the earlier clearly stated 2,005-plus-225 split. The actual target-date index is needed to settle it. The important methodological difference is that the second experiment updates the model before each individual forecast.

Network architecture selection is described as experimentation, and the text says the repeated forecasts led to model selection. It does not document a fully separate outer holdout untouched by architecture and feature choices. Early stopping protects against excessive fitting within a selected architecture; it does not by itself correct repeated searches over architectures or evaluation conventions. There is no reported multiple-model data-snooping adjustment or independent later sample.

## Loss functions and inference

For forecast errors $e_t=y_t-\widehat y_t$, use

$$
\operatorname{MSPE}=\frac{1}{M}\sum_{t=1}^M e_t^2,
\qquad
\operatorname{RMSE}=\sqrt{\operatorname{MSPE}}.
$$

Page 236 incorrectly describes MSPE as the square root of RMSE. The numerical tables support the conventional definition above: the daily benchmark RMSE $1.4321\times10^{-3}$ squared is approximately $2.0509\times10^{-6}$, the benchmark MSPE in Table VI. A reproducer should implement the conventional squared-error definition and explicitly record this source correction.

Directional accuracy is the fraction of observations for which $y_t\widehat y_t>0$. Exact zeros are counted as failures by the displayed indicator. Multiplying by 100 gives the reported percentages. This loss treats every correct sign equally, irrespective of the subsequent movement's magnitude, and does not represent a profit-weighted objective.

The Diebold–Mariano statistic is $\overline d/\sqrt{\widehat\Omega_d/M}$ for a loss or performance differential $d_t$. The paper uses its sample variance as the long-run variance estimate because the reported Table VI forecasts are one step ahead. One-step forecasting alone does not guarantee serially independent loss differences, particularly with overlapping expanding estimation and persistent market conditions. A replication should reproduce the reported variance convention, then separately examine dependence-robust inference. Such an extension must not be presented as the original test.

The authors use two-sided standard-normal critical values approximately 1.64 at 10% and 2.58 at 1%. Directional comparisons yield positive statistics for improved hit rates, while squared-error comparisons yield negative statistics for reduced errors. The source does not provide confidence intervals for individual model hit rates or losses.

## Quantitative findings

Table II shows extremely weak linear explanatory power in the initial estimation sample: $R^2$ is 0.0021 and 0.0049 for the daily aggregate and disaggregated models, and 0.0050 and 0.0055 for the weekly versions. Thus the predictive claim does not rest on explaining a large fraction of daily variance with a linear regression.

For daily LM 2, the estimated interest-rate-change coefficient is $-1.89\times10^{-4}$ with standard error $2.5\times10^{-4}$; the oil coefficient is −0.0087 with standard error 0.0065. Flow coefficients are $1.33\times10^{-7}$ for commercial clients, $-1.015\times10^{-7}$ for interbank flow, and $-3.86\times10^{-7}$ for foreign institutions, with standard errors $1.28\times10^{-7}$, $1.69\times10^{-7}$, and $8.98\times10^{-8}$. The foreign-institution coefficient is the clearest daily linear signal. These are predictive associations in the source's unspecified flow units, not causal price-impact estimates.

Representative block-forecast errors illustrate the scale of improvements:

| Target/evaluation block | Random walk | LM 1 | ANN 1 | LM 2 | ANN 2 |
|---|---:|---:|---:|---:|---:|
| Daily, 225 targets, RMSE $\times10^{-3}$ | 1.4321 | 1.4364 | 1.4270 | 1.4331 | 1.4216 |
| Daily, 145 targets, same units | 1.3381 | 1.3464 | 1.3238 | 1.3388 | 1.3337 |
| Daily, 55 targets, same units | 1.4168 | 1.4202 | 1.4070 | 1.4156 | 1.4155 |
| Weekly, 225 targets, RMSE $\times10^{-2}$ | 0.3457 | 0.3461 | 0.3458 | 0.3460 | 0.3448 |
| Weekly, 55 targets, same units | 0.3882 | 0.3894 | 0.3878 | 0.3895 | 0.3868 |

These are Tables III–IV, pages 239–240. For the initial daily block, ANN 2 reduces RMSE by about 0.73%, calculated from the reported values. ANN 1 occasionally outperforms ANN 2; disaggregation is not uniformly superior under every block and loss. Likewise, the initial weekly ANN 1 error slightly exceeds the random walk. The broad prose claim of consistent superiority should be read against these individual entries.

Table V averages directional percentages over overlapping block evaluations:

| Horizon | Random walk | LM 1 | ANN 1 | LM 2 | ANN 2 |
|---|---:|---:|---:|---:|---:|
| Daily | 54.88% | 57.18% | 60.14% | 58.75% | 61.81% |
| Weekly | 56.26% | 54.90% | 56.15% | 55.28% | 58.04% |

The daily ANN 2 advantage over the benchmark is 6.93 percentage points. Its weekly advantage is only 1.78 points; ANN 1 is slightly below the weekly benchmark. Thus the conclusion's statement about at least a 3% advantage at both horizons is not supported as a blanket percentage-point comparison with the random walk.

The stronger results arise from daily re-estimation in Table VI:

| Measure | Random walk | ANN 1 | ANN 2 |
|---|---:|---:|---:|
| Correct direction | 54.88% | 67.56% | 71.56% |
| Direction DM statistic versus benchmark | — | 4.0063 | 5.7107 |
| MSPE, $\times10^{-6}$ | 2.0509 | 2.0036 | 1.9566 |
| Squared-error DM statistic | — | −1.6841 | −1.7730 |

The ANN 2 directional improvement is 16.68 percentage points, while its MSPE reduction is approximately 4.60%; ANN 1's corresponding improvements are 12.68 points and 2.31%. Direction tests meet the reported 1% criterion. Squared-error tests meet 10%, not 5%, under the stated two-sided normal approximation. Strong evidence under one loss should not be transferred to the other.

## Sign imbalance and ancillary evidence

The sample predominantly contains positive exchange-rate changes. To examine that imbalance, the authors compute separate correct-positive and correct-negative fractions, defining “positive” relative to the estimation-sample mean change rather than zero. These are different classification targets from the ordinary sign rule and should not be interpreted as the conditional components of Table VI's 71.56% without matching the experiment and threshold.

For the initial 225-observation block, Table VII reports daily mean-centered positive/negative success rates of 42.98%/48.08% for ANN 1 and 38.02%/67.31% for ANN 2. Without centering, the corresponding rates in parentheses are 89.43%/2.05% and 80.49%/36.27%. Weekly centered rates are 57.02%/41.44% and 53.04%/56.36%. The uncentered weekly positive rate is 98.39% for both networks, with negative rates only 0.99% and 2.97%.

These results show why an overall direction score can be misleading in an imbalanced sample. They do not establish uniformly high skill on both sides of a centered target. In particular, daily ANN 2's centered positive and negative rates differ considerably. A new evaluation should retain the source's statistics while also reporting the complete confusion matrix, majority-sign baseline, and target threshold fixed using training data.

The paper separately estimates a 30-day forward-bias regression using CANSIM data from January 1994 through May 2002. The slope of future spot change on the forward premium is −0.432875 with reported $t=-3.449215$; the intercept is 0.000525 with $t=2.937104$, and $R^2=0.010$. This exercise motivates excluding forwards from the main feature set. It uses a different sample and is not an input or an out-of-sample validation of the neural networks. Also, a minimum delivery tenor of 30 days does not itself imply that a forward quote cannot be observed daily; the source's explanation should not be generalized into that market-data claim.

## Reconstruction procedure and limits

A disciplined implementation would first obtain the dated CFEC spot-flow categories and metadata, reproduce the target and macroeconomic transformations, and resolve the source's unit and calendar discrepancies. It would align all predictors to the information actually available before the target observation, including publication lags for CPI. It would then establish the daily 2,005/225 split explicitly and specify the training/validation allocation inside each estimation window.

Next, fit the drift benchmark and both linear models, and search only the disclosed small network family using validation data. Fit scaling on training observations, store the inverse target transformation, preserve random seeds, and record every selected architecture and early-stopping epoch. Reproduce the overlapping-block experiments separately from the 225 single-step forecasts, using identical target dates across models. For weekly results, obtain clarification of the target before comparing errors.

Finally, compute conventional MSPE and RMSE, the exact strict-sign hit rule, the paper's DM statistic, and the centered conditional sign rates. Report extensions such as robust long-run variances, a later untouched test period, alternative flow units, and transaction-cost-aware nominal-currency trading as new analyses. No portfolio construction, leverage, spread, carry, execution latency, or rebalancing rule is specified by the original paper.

The substantive takeaway is that disaggregated order-flow information combined with a nonlinear mapping can improve daily directional forecasts in this particular dataset, and model updating materially changes the result. The paper does not establish a universal 72% currency forecasting rate, identify causal effects of each customer category, or provide sufficient detail to recreate the exact trained networks. Its strongest reusable contribution is the comparative experimental structure and the emphasis on transaction composition; its strongest unresolved requirement is access to the original data and estimation protocol.
