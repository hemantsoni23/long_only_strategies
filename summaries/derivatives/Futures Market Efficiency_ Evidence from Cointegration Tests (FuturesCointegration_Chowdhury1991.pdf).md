# Futures Market Efficiency: Evidence from Cointegration Tests

Abdur R. Chowdhury, The Journal of Futures Markets 11(5), 1991, pp. 577–589. Source: [FuturesCointegration_Chowdhury1991.pdf](../../Finance/FuturesCointegration_Chowdhury1991.pdf), thirteen pages. The study examines copper, lead, tin, and zinc on the London Metal Exchange over July 1971–June 1988.

## Why this matters and the contribution

The paper applies unit-root and residual-cointegration tests to futures-market efficiency rather than run conventional level regressions without checking nonstationarity. Its reported results reject its efficiency restrictions for all four metals. The central methodological improvement is to distinguish co-movement of nonstationary prices from a valid stationary forecasting relation.

The economic conclusion needs qualification. Cointegration is a statement about common stochastic trends, not automatically a proof of a profitable trading strategy or an informational failure. Predictable futures payoffs may reflect risk premiums and costs. The paper itself introduces a risk premium and recognizes that within-market cointegration is necessary rather than sufficient under its proposed efficiency interpretation. Its broader cross-market claim is stronger than the statistical tests alone establish.

## Economic setup and hypotheses

Let $F_{t-j,t}$ be the futures price observed at $t-j$ for delivery at $t$, $S_t$ the maturity spot price, and $I_{t-j}$ the contracting-date information set. With convergence of futures and spot at delivery, equations (1)–(2) express

$
F_{t-j,t}=E[S_t\mid I_{t-j}]-R_{t-j},
$

where $R_{t-j}$ is a risk premium assumed nonnegative in this formulation. A zero premium gives the unbiased-price/martingale restriction; independent identically distributed innovations would impose the stronger random-walk model.

The conventional regression restriction is an intercept of zero and slope one between the earlier futures price and subsequent spot price. The article discusses regression orientations and differences in its equations (3)–(4), whose interpretation depends on the specified left-hand variable. The actual within-market tables use subsequent spot as dependent variable:

$
S_t=a+bF_{t-j,t}+u_t.
$

The study tests whether the level series are $I(1)$, whether a stationary residual combination exists, and whether $(a,b)=(0,1)$. It also tests pairwise cointegration across different metals. The author's interpretation is that cross-metal cointegration implies exploitable predictive content and hence inefficiency. That implication requires more economic restrictions than stationary co-movement alone: common fundamentals, risk compensation, storage relations, and trading frictions can also generate cross-asset relationships.

Within the same metal, a stationary forecast error with unit slope is consistent with prices not drifting arbitrarily apart. However, stationarity permits serial dependence, whereas an unbiased efficient-forecast error under the relevant information set requires the appropriate conditional orthogonality. A stationary but predictable residual is therefore not a complete efficiency test. Conversely, a time-varying risk premium can make expected spot and futures differ without irrational pricing.

## Data and timing

The observations are monthly-average LME spot and three-month futures quotations, aligned with the subsequent spot price when the contract matures. The author uses nonoverlapping observations to avoid mechanically induced dependence from overlapping three-month forecast periods. Early observations, July 1971–June 1979, are taken from Goss's studies; subsequent data come from issues of Metallgesellschaft. The reported estimation count is 64.

The July 1971–June 1988 calendar span contains 204 months, so a simple every-third-month construction would not by itself explain the final count. The exact starting offset, exclusions, and alignment needed to reproduce 64 observations are not supplied. The article also does not give a complete data appendix with price units and every dated observation. A reproduction should not invent those details or silently substitute rolling nearby futures prices for contract-aligned earlier quotes.

The LME quotation convention matters: the paper says three-month delivery is officially quoted and the same particular contract is not officially quoted again until settlement. This differs from treating a sequence of constant-maturity quotes as repeated prices of one fixed contract. Monthly averaging can further blur the precise information timing of an investable signal.

## Econometric procedure

First test each individual spot and futures level for a unit root. The augmented Dickey–Fuller procedure begins with up to 12 lagged differences, following Schwert's suggested length, and removes the longest insignificant lag sequentially until significance is found or all are exhausted. The article does not state the elimination significance threshold or the retained lag for each series. Phillips–Perron statistics use ten autocovariance lags and triangular weights. Additional trend specifications are said to give similar conclusions, but are not tabulated.

The displayed unit-root critical value is $-3.45$ at 5%, taken from a table for 100 observations even though the study reports 64 observations. The specific deterministic-term and sample-size conventions should therefore be checked in any numerical reproduction. One must compare negative statistics in the correct direction: rejection requires a sufficiently negative statistic, not merely a large unsigned coefficient.

If both variables appear $I(1)$, estimate a level regression $X_t=c+dY_t+u_t$. Then test the estimated residual for a unit root using an ADF-type regression of residual differences on a lagged residual level and lagged residual differences. Rejecting the residual unit-root null supports cointegration. Because the residual is estimated, the test uses Engle–Granger critical values, here $-3.17$ at 5%, rather than an ordinary regression $t$ distribution.

The economic property of cointegration is invariant to which variable is normalized as dependent, but finite-sample Engle–Granger test statistics need not be identical across regression orientations. The paper's statement that the tests are symmetrical should be read with that qualification. Reversed within-market regressions are said to produce qualitatively similar results; their numerical tables are not printed.

Finally, the paper follows Stock's method for the joint intercept/slope restriction. The reported statistic is compared with a chi-squared distribution with two degrees of freedom. Complete covariance calculations and adjustment implementation are not provided. Because most within-market pairs fail the preceding cointegration test, treating those later restrictions as routine inference inside an established cointegrating regression is itself a concern.

## Reported unit-root and cross-market results

Table I does not reject a unit root for any of the eight levels. ADF statistics range from $-.967$ for tin spot to $-2.414$ for zinc futures. The corresponding Phillips–Perron statistics are also insufficiently negative, ranging from $-1.088$ to $-2.910$. Tests on first differences are said to reject a unit root, although the statistics are omitted. The author therefore treats all prices as $I(1)$; failure to reject in levels is not a proof of their true integration order.

Table II reports residual ADF statistics for cross-metal spot-price pairs:

| Pair | Residual ADF |
|---|---:|
| Copper–lead | -7.20 |
| Copper–tin | -5.12 |
| Copper–zinc | -4.12 |
| Lead–tin | -4.10 |
| Lead–zinc | -6.71 |
| Tin–zinc | -3.66 |

All exceed the reported 5% rejection threshold in the negative direction. Table III reports cross-metal futures statistics of $-1.61$, $-4.12$, $-4.41$, $-4.95$, $-1.94$, and $-3.77$ in the same pair order. Thus copper–lead and lead–zinc do not reject no cointegration, while the other four futures pairs do. These are pairwise full-sample tests without a multiple-comparison adjustment or an out-of-sample forecasting exercise.

Some estimated cross-metal slopes are negative, and the tables' level-regression $R^2$ values are high. The source explicitly cautions that those fit measures do not have their usual interpretation with $I(1)$ variables. They should not be treated as return-prediction performance or a reason to skip residual diagnostics.

## Same-metal spot–futures results

Table IV estimates subsequent spot on earlier futures and reports:

| Metal | Intercept | Futures slope | Residual ADF |
|---|---:|---:|---:|
| Copper | -12.160 | 2.313 | -3.10 |
| Lead | -2.773 | 1.965 | -2.03 |
| Tin | 246.112 | 11.305 | -.91 |
| Zinc | 18.607 | .788 | -1.35 |

None rejects no cointegration at the table's 5% threshold of $-3.17$. Copper is described as rejecting at 10% but not 5%. The large slope deviations, particularly tin's 11.305, are reported estimates, not hedge ratios recommended for trading. Without stationary residuals, ordinary precision interpretations of those level coefficients are especially hazardous.

Table V's joint $(a,b)=(0,1)$ statistics are 12.19 for copper, 15.33 for lead, 8.96 for tin, and 17.04 for zinc. All exceed the 5% chi-squared critical value of 5.99. All except tin exceed the 1% value of 9.21. The paper interprets this as biased futures prediction and rejection of efficiency. It does not estimate the risk premium that could contribute to bias or report a net-of-cost trading rule exploiting the deviations.

## Reproduction boundaries and takeaways

To reproduce the published sequence, obtain the actual nonoverlapping dated prices, maintain maturity alignment, run the two families of univariate unit-root tests, estimate each displayed bivariate relationship, test estimated residuals with appropriate nonstandard critical values, and implement the exact joint restriction procedure. Retained ADF lags, price units, missing observations, and covariance corrections remain source-code or author-data requirements.

The small sample limits power, particularly for long-run relationships and structural changes. Neither an absence of detected cointegration nor the presence of cross-metal cointegration is by itself an investor's profit calculation. The study supplies an historically important nonstationarity-aware diagnostic and evidence against its stated unbiasedness restrictions. A stronger present-day claim about informational efficiency would need an explicit expected-return or risk-premium model, careful timing, robustness to breaks and specifications, and a separate costed out-of-sample exercise.
