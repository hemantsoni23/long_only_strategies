# Stock Market Volatility: Identifying Major Drivers and the Nature of Their Impact

**Authors:** Stefan Mittnik, Nikolay Robinzonov, Martin Spindler. **Publication:** *Journal of Banking & Finance* 58 (2015), 1-14. **DOI:** 10.1016/j.jbankfin.2015.04.003. The earlier working-paper title was *Boosting the Anatomy of Volatility*. **Source:** [original PDF](../../Finance/VolatilityPrediction_MittnickRobinzonov_2015.pdf). The source filename spells the first author's name differently from the paper. **Scope inspected:** all 14 PDF pages, including the algorithm, simulation, and horizon-specific response plots in Appendices A-C. Page references below are both printed and PDF pages.

## Why this matters

Volatility models often explain persistence exceptionally well while saying little about which observable economic conditions make risk rise. This paper asks whether a large menu of macroeconomic and financial predictors can improve monthly equity-volatility forecasts and yield interpretable response functions. Its distinctive move is to combine variable selection and nonlinear functional estimation through componentwise boosting. Each update uses one predictor and one threshold, so the final model can be decomposed into separate effects of VIX, the TED spread, past realized variance, and other variables.

The innovation is not a new volatility estimator or a structural theory of financial crises. It is a forecast architecture that selects predictors, identifies regimes in their effects, and changes those relationships with the prediction horizon. An explicit comparison separates the value of extra information from the value of nonlinear modeling. Exogenous information helps at short horizons; nonlinear responses become more useful at three to six months. That distinction matters for a risk team deciding whether better data or a more flexible model is the main missing ingredient.

The empirical claim is narrower than a deployable risk system. The study concerns monthly S&P 500 volatility over a short history, includes the financial crisis, and evaluates statistical forecasting loss. It does not produce a trading strategy, calibrate tail probabilities in actual market data, or measure net investment returns. Its selected variables are predictive associations, not identified causal policy instruments.

## Return model and additive variance architecture

Let $P_t$ denote price and $y_t=\log(P_t/P_{t-1})$ the logarithmic return. The theoretical specification in equation (1), p. 3, is

$$
y_t=\exp(\eta_t/2)\epsilon_t,\qquad \epsilon_t\overset{iid}{\sim}N(0,1),
$$

$$
\eta_t=\beta_0+f_{time}(t)+f_{yr}(n_t)+f_{month}(m_t)
+\sum_{j=1}^{s}f_j(y_{t-j})
+\sum_{k=1}^{q}\sum_{j=1}^{p}f_{k,j}(x_{k,t-j}).
$$

Here $\eta_t$ is log conditional variance; conditional standard deviation is $\exp(\eta_t/2)$. The economic predictors $x_{k,t-j}$ and return lags must be available when forecasting. The deterministic functions allow a trend and year/month effects. The paper writes an $r=s+qp+4$ dimensional predictor vector, including the constant and three deterministic terms. In the empirical application it reports 84 candidate predictors, with two lags of its 40-variable menu plus deterministic terms.

Each component is a piecewise constant univariate function:

$$
f_k(z)=\sum_{j=1}^{J_k}c_{kj}\mathbf 1\{z\in R_{kj}\}.
$$

The disjoint intervals $R_{kj}$ partition the observed predictor domain. Their boundaries and response levels are learned. The model is additive across predictors: nonlinear effects within one variable are allowed, but general interactions between two different predictors are not automatically represented. For example, a TED effect can be nonlinear without being allowed to change specifically when VIX is high. Calling the model a general multivariate tree ensemble would obscure this restriction.

The elementary learner is a stump, a tree with two terminal regions. Successive updates can reuse the same variable with different split points. The sum of these stumps yields a multi-step response curve even though each update is simple. The authors use conditional-inference trees: candidate splits maximize the absolute standardized difference between group means. They favor trees because abrupt volatility responses and boundary behavior are more natural for steps than for high-order splines. Bounded step responses also avoid the mechanical explosive extrapolation that can arise from a multiplicative autoregressive coefficient, although that is not a general proof of stationarity for an estimated, evolving risk system.

A change $\Delta\eta$ multiplies variance by $e^{\Delta\eta}$ and standard deviation by $e^{\Delta\eta/2}$. This factor-of-two distinction is essential when interpreting the plotted partial effects. Neither a coefficient nor a step height in log variance is itself a percentage change in volatility.

## Objective, gradient, shrinkage, and stopping

Under the stated Gaussian return model, omit additive constants in the negative log likelihood and minimize average loss

$$
L(y_t,\eta_t)=\tfrac12\left(\eta_t+y_t^2e^{-\eta_t}\right).
$$

The negative gradient used as the working response is

$$
u_t=-\frac{\partial L}{\partial\eta_t}
=\tfrac12\left(y_t^2e^{-\eta_t}-1\right).
$$

This is equation (3), p. 3. When squared returns exceed the current variance estimate, the gradient is positive and the fitted log variance is pushed upward; when they fall below it, the reverse occurs. This gives a direct check on the sign in an implementation. Ordinary squared-error boosting of raw returns would solve a different problem.

Appendix A, pp. 8-9, supplies the algorithm:

1. Initialize the fitted log variance to the logarithm of the sample variance of returns. The sample-variance denominator is $T-1$, and the sample mean is removed for initialization.
2. At iteration $m$, evaluate the negative gradient at the current fitted log variances.
3. Separately fit a stump to the gradient using each candidate predictor. Select the predictor whose fitted learner best matches the gradient in residual sum of squares.
4. Update only that component, using a shrinkage fraction $\nu$:

$$
\widehat\eta^{[m]}=\widehat\eta^{[m-1]}+\nu\widehat f^{[m]}_{k_m}.
$$

5. Continue until the validation-selected stopping iteration. Sum all retained updates for each predictor to recover its partial response function.

Shrinkage reduces the greediness of a single update and lets correlated predictors remain competitive over the path. The authors describe $\nu$ values between 0.01 and 0.3 as generally safe and say the particular value mainly affects computing time. They do not supply a uniquely documented empirical step size or maximum iteration count in this PDF; these are replication inputs to recover, not parameters to invent.

Stopping is central regularization, not merely a convergence tolerance. For each of 25 bootstrap resamples, draw observations uniformly with replacement, fit the boosting path on the included observations, and evaluate loss on omitted observations. Roughly 64% of observations appear in a bootstrap training sample. Choose the iteration minimizing average validation loss across resamples. The appendix motivates this resampling through conditional independence of observations given their predictors.

For financial time series, that independence needs scrutiny: overlapping target construction, persistent predictors, or residual dependence can make randomly omitted observations easier to predict than a truly future block. A blocked or forward validation design would be a useful additional experiment, but it would be a modification to the authors' procedure. It should not be silently substituted in a claimed replication. The paper cites the R `mboost` implementation, version 2.2-2, but does not provide a frozen software environment, random seed, full fitting script, or tree-control settings.

## Data, target construction, and predictor definitions

The data span December 1989 through December 2010, 253 monthly observations. The market is the S&P 500. The empirical target is monthly log realized variance, constructed from daily log returns $r_{t,d}$:

$$
LRVar_t=\log\left(\sum_{d=1}^{M_t}r_{t,d}^{2}\right),
$$

where $M_t$ is the number of trading days in month $t$ (equation (4), p. 5). This is the log of variance, not the log of its square root. With decimal daily returns, the plotted series ranges roughly from $-8$ to $-3$. Annualization or percentage-return scaling changes the level and must be handled consistently when reproducing losses.

Table 1, p. 4, is the principal data dictionary. It groups the predictors as follows:

| Group | Variables and transformations |
|---|---|
| Equity conditions | Log dividend-price and earnings-price ratios based on trailing 12-month sums; market excess return; SMB and HML; short-term reversal; S&P 500 turnover; monthly S&P log return; VIX; log realized variance and its change |
| Rates and bonds | Three-month Treasury bill rate; that rate minus its 12-month average; long-term government bond return; long-term yield minus its 12-month average; long-minus-short yield spread; recursively estimated Cochrane-Piazzesi factor |
| Currency factors | Dollar risk-factor return; aggregate average forward discount |
| Liquidity and credit | BAA-minus-AAA default spread; average FX bid-ask spread; Pastor-Stambaugh liquidity factor; LIBOR-minus-Treasury TED spread |
| Macro conditions | Monthly and year-on-year log growth in CPI, industrial production, and M1; change in housing starts; monthly and annual growth in new orders for consumer goods/materials; annual log change in CRB spot commodity index; capacity utilization; employment change; Michigan sentiment change; consumer-confidence change; Philadelphia Fed diffusion index; Chicago purchasing-managers barometer; ISM PMI change |

The text also identifies MSCI world returns as an equity predictor, and an MSCI response appears in Appendix C, although this is not clearly aligned with the 40-variable count in the extracted Table 1. A replication should reconcile the actual source columns against the table, text, and appendix labels rather than assume that enumerating the table alone exactly reconstructs the design matrix.

The cited providers are Shiller, Fama-French, CRSP, CBOE, Goyal-Welch, Cochrane-Piazzesi, Lustig and coauthors, Menkhoff and coauthors, Pastor-Stambaugh, and Datastream. Both the first and second lag of predictor variables enter the candidate set. Lagged log variance and its change capture persistence and state dependence. Deterministic seasonal candidates are allowed. The PDF does not provide a complete release-calendar or vintage protocol for macroeconomic data. One-month lagging of a revised series is not the same as using the value that was actually known at that date.

## Forecast experiment and an important source ambiguity

The evaluation uses a rolling window of 153 months and produces 100 forecasts, reestimating each month. Separate direct models are estimated for horizons $h=1,\ldots,6$. In horizon-specific notation,

$$
\eta_{t+h}=\beta_{0,h}+\text{known calendar effects}
+\sum_{j=0}^{s-1}f_{j,h}(y_{t-j})
+\sum_k\sum_{j=0}^{p-1}f_{k,j,h}(x_{k,t-j}).
$$

This direct design avoids having to forecast every macro predictor six months ahead. It also permits the selected predictors and response curves to differ with horizon. The target is the variance of the month at $t+h$, not the accumulated variance over the next $h$ months. Direct training pairs must be aligned so the realized outcome was observed by the fitting date; otherwise the exercise would inadvertently use future targets.

Two source inconsistencies prevent an exact date-for-date replication from this PDF alone. Section 3.2 states June 2002-September 2010, while footnote 13 states August 2002-December 2010 and observation indices 154-253. The latter dates match 100 months; the former description does not transparently match the same count. Also, the theoretical model and likelihood are written for returns with latent conditional variance, whereas the empirical discussion says realized variance is used and evaluates predicted log realized variance. Footnote 13 abbreviates the realized target as $RV$ while comparing it with the fitted log-variance quantity.

The note therefore preserves both the theoretical likelihood and the explicitly defined empirical target, without asserting an undocumented change of loss. A faithful implementation needs the original code to determine exactly how realized variance replaces or supplements squared returns in fitting and how each forecast is transformed before scoring. Treating $LRVar$ as a zero-mean Gaussian return and applying the displayed return-variance likelihood to it would be an unjustified reconstruction.

The benchmarks are GARCH(1,1) and exponential GARCH(1,1). Their multi-step forecasts are recursive; the boosting forecasts are direct. The authors tried nonrecursive GARCH forecasts using frequency-compatible data and report that these performed poorly, without tabulating them. GARCH has no equivalent macro menu in this comparison. The separate four-model exercise described below is consequently more informative for attributing the improvement than the headline comparison alone.

## Numerical forecast results

Table 2, p. 6, reports the following mean squared prediction errors on the study's log-variance forecasting scale:

| Horizon, months | GARCH | EGARCH | Boosting | Reduction versus GARCH, calculated |
|---:|---:|---:|---:|---:|
| 1 | 0.588 | 0.753 | 0.527 | 10.4% |
| 2 | 0.927 | 0.903 | 0.712 | 23.2% |
| 3 | 1.025 | 1.107 | 0.770 | 24.9% |
| 4 | 1.122 | 1.526 | 0.742 | 33.9% |
| 5 | 1.029 | 1.331 | 0.664 | 35.5% |
| 6 | 1.353 | 1.432 | 0.927 | 31.5% |

The final column is $100(1-MSE_{boost}/MSE_{GARCH})$, computed from the rounded source values. It is not a return gain or an absolute change in market volatility. Boosting has lower average loss at all horizons, and the authors say all three approaches are virtually unbiased; fewer extreme errors explain the difference.

The modified Diebold-Mariano test follows Harvey-Leybourne-Newbold. Its stated one-sided alternative favors boosting. Against GARCH the p-values are 0.275, 0.060, 0.009, 0.001, 0.002, and 0.006 across the six horizons. Against EGARCH they are 0.075, 0.107, 0.035, 0.001, 0.010, and 0.038. Thus the numerical advantage at one month is not robustly significant against GARCH; it would be inaccurate to claim statistically decisive superiority at every horizon.

The Giacomini-White p-values against GARCH are 0.137, 0.219, 0.027, 0.010, 0.006, and 0.014. Against EGARCH they are 0.132, 0.347, 0.056, 0.002, 0.012, and 0.053 (Table 3). The two tests support the strongest evidence in the middle and longer monthly horizons. Some significance stars in the printed table do not exactly align with rounded p-values, so the numerical p-values are the safer quantities to retain. Alternative absolute-error scoring reportedly preserves the ranking; detailed values are not supplied.

## Separating information from nonlinear response

Section 3.3 and Figure 2 form a controlled comparison of four boosted models. L0 uses linear learners and only return history; T0 uses stump learners and only return history; L1 adds exogenous predictors to the linear architecture; T1 adds them to the tree architecture. The linear versions omit deterministic seasonal components, another detail to retain when interpreting this as an ablation.

The 100 squared forecast errors for each horizon are shown as boxplots rather than as a full numerical table. Both L1 and T1 improve markedly on models using only past returns. L1 performs best at one and two months. T1 dominates at longer horizons, while the linear model's performance falls back toward the weaker models beyond about four months. It follows that the tree representation is not unconditionally superior: the flexibility is most useful when the relationship between current economic conditions and later volatility is nonlinear.

The graphs and discussion do not establish that every selected threshold is precisely estimated. Boosting shrinks coefficients and performs selection simultaneously. The authors explicitly acknowledge that conventional significance inference for their selected components is unavailable in this analysis. The shapes are exploratory descriptions of the fitted forecast, not a set of independently tested structural breakpoints.

## Selected drivers and response magnitudes

Across horizons, the algorithm retains a relatively small number of inputs, reported as six to nine. VIX is important at every horizon. Lagged realized variance matters for forecasts up to five months. VIX, realized variance, the TED spread, and new orders are among the few variables whose fitted functions predict decreases as well as increases; most other selected macro inputs mainly flag higher volatility.

At the six-month horizon, the selected variables are VIX, TED, annual new-orders growth, HML, and CRB returns; VIX enters with both lags, TED, orders, and HML with their first lags, and CRB with its second lag. Appendix C shows the complete horizon-specific partial-response plots. Their vertical axes are contributions to log variance, conditional on the fitted additive representation, and should not be mistaken for standalone forecasts.

For first-lag VIX, a split near 17 separates a roughly $-0.40$ contribution from a roughly $+0.25$ contribution. Relative to a zero contribution, these correspond to standard-deviation multipliers $e^{-0.40/2}\approx0.82$ and $e^{0.25/2}\approx1.13$. Moving between the two regimes is a larger change, $e^{0.65/2}\approx1.38$; this last number is an interpretation of the reported levels, not an additional estimate. Second-lag VIX has a smaller low-regime contribution, about $-0.15$, or a 7% standard-deviation reduction.

TED values below approximately 0.01 have a slightly negative fitted effect. Values around 0.011-0.014 imply approximately 17% higher standard deviation, and values above 0.014 about 28% higher standard deviation, as described on p. 7. Retain the decimal-rate scale: 0.014 is 1.4 percentage points, or 140 basis points. The underlying plots are estimates with sparse observations in extremes, and the paper supplies no confidence intervals for those thresholds.

Large declines in consumer-goods/materials orders predict higher future volatility, while moderate changes have little estimated effect. These patterns are consistent with funding stress and deteriorating economic demand preceding financial uncertainty. They do not isolate whether TED has an independent causal influence or stands in for other correlated crisis variables.

## Simulation, implementation checks, and limits

Appendix B constructs 400 observations with six independent $U[-0.5,0.5]$ predictors and Gaussian shocks. The true log variance is

$$
\eta_t=0.1+2x_{1,t}+2x_{2,t}\mathbf1_{[0.1,0.5]}(x_{2,t})
-0.6\mathbf1_{[-0.5,-0.2]}(x_{3,t}),
$$

with zero effects for predictors four through six. Linear learners are assigned to the linear and irrelevant inputs; tree learners to the second and third inputs. The deliberately stepwise fit to the second, locally linear function tests whether a misspecified learner can still approximate the response. The reported estimate of the first slope is 1.463 rather than 2, illustrating shrinkage bias, while all three irrelevant slopes remain zero. The estimated central 95% conditional interval covers 95.75% of the simulated observations. These are illustrative finite-sample results, not formal market-tail calibration.

A replication should first reproduce this controlled example, verifying the gradient sign, the log-variance/standard-deviation conversion, and exclusion of null variables. It should then reconcile the empirical target ambiguity, exact 100 forecast origins, deterministic columns, predictor count, and release timing before judging success by Table 2. Store component paths and split thresholds at each rolling origin so a final full-sample picture cannot be confused with the forecast actually available at an earlier date.

The economic takeaways are concrete: retain a strong persistence benchmark, measure the incremental information in option-implied and funding-stress variables, and let functional flexibility compete by horizon. The main failure modes are small effective sample size, crisis sensitivity, correlated-variable substitution, unstable thresholds in sparse tails, macro-data revisions, and an inadequately separated validation period. No transaction costs, turnover, portfolio constraints, or utility gains are estimated. Those require a separate decision problem even if the forecasting improvement is reproduced.
