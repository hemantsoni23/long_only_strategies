# Asset Pricing Models and Financial Market Anomalies

Doron Avramov and Tarun Chordia. *Review of Financial Studies* 19(3), 2006, 1001-1040. DOI: 10.1093/rfs/hhj025. Source: [AssetAnomalies_AvramovChordia_2006.pdf](../../Finance/AssetAnomalies_AvramovChordia_2006.pdf). All 40 pages were read, including all nine tables, the factor-loading figure, methodological footnotes, and references. There is no separate technical appendix in this source. Journal page $p$ is PDF page $p-1000$; equations and principal tables were checked visually.

## Why this matters

A characteristic can forecast stock returns because it predicts risk exposure, because it forecasts compensation for risk, or because the pricing model leaves a predictable residual. A constant-beta factor regression cannot reliably distinguish those possibilities. Avramov and Chordia build stock-level conditional betas from firm size, book-to-market, and aggregate business conditions, then test whether familiar characteristics still explain returns after that risk adjustment.

Their central finding has three parts. Conditional Fama-French betas largely remove the size and book-to-market effects in individual stocks. Turnover and momentum remain significant, even with traded liquidity and momentum factors and substantially more flexible betas. Momentum loses its positive residual association only when an explicitly time-varying alpha, driven by business-cycle variables, is also removed. That final result identifies predictable model misspecification; it does not establish a rational risk explanation for momentum.

For a quantitative equity process, the paper is useful as a decomposition framework. It shows why a factor loading, a stock characteristic, and a forecasting signal with similar names are not interchangeable. A portfolio can have zero exposure to a traded momentum factor and still retain characteristic-based momentum predictability. It also warns against calling an anomaly “explained” merely because a factor prices a small set of sorted portfolios: the restriction can fail at the security level.

This is an in-sample asset-pricing study. Full-sample first-pass estimation uses future observations when constructing historical risk-adjusted returns. No executable portfolio optimization, transaction-cost budget, or out-of-sample alpha strategy is evaluated. The results concern model adequacy for selected characteristics under a specified estimation framework.

## Conditional pricing model and testable restrictions

The starting point is a conditional $K$-factor representation for stock $j$:

$$
R_{jt}=E_{t-1}[R_{jt}]+\sum_{k=1}^K\beta_{jk,t-1}f_{kt}+e_{jt},
$$

where $f_{kt}$ is the unanticipated component of factor $k$ and $\beta_{jk,t-1}$ is its predetermined conditional loading. Exact pricing imposes

$$
E_{t-1}[R_{jt}]-R_{Ft}
=\sum_{k=1}^K\beta_{jk,t-1}\lambda_{k,t-1}.
$$

Writing $F_{kt}=f_{kt}+\lambda_{k,t-1}$, the realized factor return combines its innovation and conditional premium. For traded excess-return factors, the risk-adjusted return is

$$
R^*_{jt}=R_{jt}-R_{Ft}-\sum_k\widehat\beta_{jk,t-1}F_{kt}.
$$

The procedure assumes the conditional zero-beta return equals the risk-free rate and the factor's premium is its expected excess return. These are substantive pricing restrictions. One cannot insert an arbitrary nontraded macro innovation directly into this calculation with coefficient one on its realized value and still retain the same interpretation.

Each month, the authors regress adjusted returns on an intercept and stock characteristics:

$$
R^*_{jt}=c_{0t}+\sum_{m=1}^M c_{mt}Z_{mj,t-1}+\eta_{jt},
\qquad
\widehat c_t=(Z_{t-1}'Z_{t-1})^{-1}Z_{t-1}'R^*_t.
$$

The reported estimates are time averages of the cross-sectional coefficients, with Fama-MacBeth inference modified for estimated betas. Under exact conditional pricing, these characteristics should not forecast adjusted returns. The practical reported test is whether their average coefficients are zero. Failure to reject the average does not establish exact pricing in every state, and a low average cross-sectional adjusted $R^2$ does not rule out constant pricing errors unrelated to these characteristics.

Using risk-adjusted returns as the dependent variable follows Brennan, Chordia, and Subrahmanyam and Shanken. It addresses an errors-in-variables problem associated with placing estimated betas on the right-hand side of the second pass. It does not make the first-pass estimates error-free. Standard errors receive the Shanken correction and the heteroskedasticity-permitting Jagannathan-Wang correction. The latter can produce larger absolute $t$ statistics than conventional Fama-MacBeth or Shanken results; it is not an automatic inflation of uncertainty in every application.

The paper does not print complete sandwich-matrix formulas for either correction. An exact replication needs those antecedents or the original code. Substituting naive stock-level OLS standard errors would be a different test and would ignore the time dimension through which characteristic rewards are assessed.

## Beta parameterization and estimation

For one factor and one aggregate state variable $z$, the most important parameterization is

$$
\beta_{j,t-1}=b_{j1}+b_{j2}z_{t-1}
+(b_{j3}+b_{j4}z_{t-1})Size_{j,t-1}
+(b_{j5}+b_{j6}z_{t-1})BM_{j,t-1}.
$$

The implemented firm quantities are logs of market capitalization and book-to-market. Each stock and each factor has its own coefficients. The cross-sectional attributes thus enter the loading function, while their slopes can themselves change with aggregate conditions.

Substituting this expression into a one-factor regression yields a linear estimation problem:

$$
\begin{aligned}
r_{jt}={}&\alpha_j+b_{j1}r_{mt}+b_{j2}z_{t-1}r_{mt}
+b_{j3}Size_{j,t-1}r_{mt}\\
&+b_{j4}z_{t-1}Size_{j,t-1}r_{mt}
+b_{j5}BM_{j,t-1}r_{mt}
+b_{j6}z_{t-1}BM_{j,t-1}r_{mt}+u_{jt}.
\end{aligned}
$$

For multiple factors, create the corresponding interaction block for every factor. The first-pass OLS regression includes an intercept and is fitted over the stock's available full-sample history. Risk-adjusted return is then $\widehat\alpha_j+\widehat u_{jt}$, not just the residual. Removing the constant alpha would mechanically remove part of the cross-sectional pricing error the test is intended to detect.

Four nested loading specifications appear throughout the tables: constant beta; beta linear in Size and BM; beta linear in the default spread; and the full interaction specification above. Common aggregate scaling has a familiar unconditional multifactor interpretation. Firm-specific scaling does not create common additional factors: $Size_{j,t-1}F_t$ differs across $j$. Treating it as one universal factor return would erase the article's principal methodological distinction.

The default spread is the main business-cycle indicator. The tables describe it as the yield differential between BBB- and AAA-rated bonds; some prose uses Moody's BAA terminology. These should be reconciled to the actual data series in replication. Default yield spread used to scale betas is separate from the default *return* spread used among the factor-mimicking base assets.

Economic motivation comes from Gomes-Kogan-Zhang: size relates to risk from growth options, and book-to-market to risk from existing projects. This motivates the interaction form but does not derive the empirical six-coefficient beta law as a structural identity. Correct conditional-beta modeling can improve pricing; misspecified conditional dynamics can also worsen it. The paper tests a finite economically motivated set rather than estimating unrestricted true risk exposures.

## Models and nontraded-factor construction

The model menu includes the CAPM; Fama-French market, SMB, and HML; Fama-French plus a traded Pastor-Stambaugh liquidity proxy; Fama-French plus winners-minus-losers (WML); Fama-French plus both liquidity and WML; a market-plus-labor-income model motivated by Jagannathan-Wang; and a linear consumption CAPM evaluated quarterly.

The liquidity factor is a long-short traded portfolio: value-weighted returns of stocks with high sensitivity to Pastor-Stambaugh liquidity minus those with low sensitivity. It is not the nontraded innovation in aggregate liquidity itself. WML is the momentum factor from Kenneth French. The paper treats WML as an empirical benchmark without asserting a theoretical risk foundation.

For consumption and labor income, factor-mimicking portfolios are required. The unconditional regression is

$$
f_t=a+b'B_t+\xi_t,
$$

and the conditional version adds $c'z_{t-1}$. The mimicking payoff used in either case is $\widehat a+\widehat b'B_t$; the predictive state term is not retained as a contemporaneous traded payoff. The eight base assets are six Fama-French size/value portfolios, a BAA-minus-AAA bond return spread, and a long-Treasury-minus-three-month-bill return spread. The paper reports robustness to other choices from these assets plus industry portfolios, but does not tabulate all the alternatives.

Labor income is monthly total personal income less dividends, normalized by the U.S. population. The stated growth construction compares adjacent two-month sums of that series, $(L_{t-1}+L_{t-2})/(L_{t-2}+L_{t-3})$. Whether represented as this gross ratio or minus one changes the intercept rather than its innovation with an intercept present; a replicator should preserve the author's original convention. Consumption is only available quarterly, so the consumption CAPM uses 150 quarters from 1964:Q3 through 2001:Q4.

Mimicking-portfolio estimation adds its own errors and spanning assumptions. A weak consumption mimicker may fail to capture the relevant consumption risk even if a richer consumption-based model is true. The source argues that no systematic directional bias should follow and reports robustness across base assets. Its rejection is of these tested linear implementations, not every consumption model.

## Universe, screens, and signal timing

The main sample is common stocks on NYSE, AMEX, and NASDAQ. The data section and tables specify July 1964-December 2001, 450 months; the introduction says August 1964. The 450-month table definition is the internally consistent replication target. NASDAQ enters only in January 1983 because its CRSP trading volume is unavailable before November 1982.

A stock needs current return and the previous 36 months of returns, size and month-$t-2$ turnover, and sufficient Compustat accounting data for prior-year book-to-market. The first two Compustat years for each firm are excluded to reduce survival bias; results are said to be robust to this exclusion. Quarterly tests require at least 36 observations, making their effective seasoned-stock requirement much longer. Minimum-history sensitivity from 20 to 72 months is reported; the full 72-point requirement matters particularly for the most flexible model.

There are 7,875 different stocks and an average of 2,871 per month, or 1,818 when limited to NYSE-AMEX. These are screened cross-sections rather than all tradable U.S. securities. Requiring past history excludes young firms. The source does not give a complete treatment of delisting returns, stale prices, zero turnover, negative book equity before logarithms, or every missing-accounting-data rule. Those omissions matter when converting the framework into code.

Book-to-market from the end of year $t-1$ is assigned from July of year $t$ through June of year $t+1$. Ratios are winsorized at the 0.5th and 99.5th percentiles before logs. SIZE is log capitalization in billions of dollars; BM is log book-to-market. NYTURN and NASDTURN are separate log share-turnover characteristics because NASDAQ reported volume can include interdealer trades. The cross-sectional specification also includes a NASDAQ dummy.

Firm characteristics are demeaned within the cross-section and lagged two months in the implemented cross-sectional regressions. The equations use generic $t-1$ notation for predetermined information; the empirical data section's two-month convention is the one to follow for the actual tables. Quarterly regressions lag attributes two months from the beginning of the return quarter. Momentum is split into cumulative returns over months 2-3, 4-6, and 7-12 before the current return period, omitting the most recent month. This separation tests multiple parts of the momentum horizon, rather than a single trailing-year total return.

The mean monthly excess return is 0.85% for the combined universe and 0.76% for NYSE-AMEX. Mean capitalization is \$0.87 billion and \$1.38 billion respectively. Average turnover is 4.40% for NYSE-AMEX and 8.73% for NASDAQ; respective medians are 2.94% and 4.58%. These descriptive differences help explain the exchange split in the liquidity test.

## Core numerical findings

All reported cross-sectional slope coefficients below are the article's displayed values multiplied by 100 relative to the underlying regression coefficient. Thus a displayed SIZE coefficient -0.047 means about -0.047 percentage points of monthly adjusted return per unit log size, not -4.7% per month. Momentum regressors remain in return units rather than being logged. Unless otherwise stated, $t$ statistics are Jagannathan-Wang corrected and the sample includes NASDAQ.

The raw excess-return cross-sectional regression in Table 1 has adjusted $R^2=5.18\%$. Size's coefficient is -0.164 ($t=-3.51$), BM 0.177 (3.35), NYTURN -0.092 (-1.82), and RET7-12 0.846 (6.07). These are baseline associations before factor adjustment.

The CAPM hardly changes the picture. Table 2's constant-beta model has SIZE -0.155 ($t=-3.34$), BM 0.183 (3.80), and RET7-12 0.822 (6.44). Under the full conditional loading, those values are -0.141 (-3.14), 0.136 (3.02), and 0.858 (7.25). NYTURN remains -0.113 (-3.22), NASDTURN -0.187 (-2.60), and the average adjusted cross-sectional $R^2$ declines only from 4.42% to 4.26%. Conditional market beta alone does not absorb the anomalies.

Table 3 delivers the main improvement:

| Characteristic | Constant FF3 coefficient | Constant FF3 $t$ | Fully conditional FF3 coefficient | Conditional $t$ |
|---|---:|---:|---:|---:|
| SIZE | -0.099 | -3.74 | -0.047 | -1.93 |
| BM | 0.096 | 2.88 | 0.008 | 0.31 |
| NYTURN | -0.123 | -3.62 | -0.115 | -4.08 |
| NASDTURN | -0.106 | -2.39 | -0.087 | -2.07 |
| RET2-3 | 0.639 | 2.75 | 0.859 | 3.78 |
| RET4-6 | 0.755 | 4.45 | 0.902 | 5.77 |
| RET7-12 | 0.742 | 5.95 | 0.768 | 7.38 |

Average adjusted $R^2$ falls from 2.43% to 2.23%. Much of the improvement over CAPM comes from adding the factors themselves; loading dynamics then remove the remaining size/value slopes. SIZE at -1.93 is near the conventional 5% boundary, so “explained” here should be understood as failing that significance criterion, not as an estimated zero effect. Among NYSE-AMEX stocks, the fully conditional size and BM $t$ statistics are -0.63 and 0.12; adjusted $R^2$ falls from 2.62% to 2.26%.

Conditioning only on the default spread is insufficient. Conditioning on Size and BM is more effective, with the interaction with the cycle particularly useful for the full universe. Adding firm attributes to beta is not mathematically guaranteed to erase the same attributes from residual-return regressions: the CAPM counterexample in Table 2 demonstrates this directly. Nevertheless, full-sample fitting and additional flexibility mean it is a model-comparison result, not an identification of the economic source of value returns.

Figure 1 plots average conditional market, SMB, and HML loadings, which vary considerably. The correlation of recession status with average market beta is 0.19 and with SMB beta 0.30, both reported significant. NBER dates are used descriptively, not as a contemporaneously available trading signal. Changing cross-sectional composition may contribute to average-beta dynamics in addition to within-firm exposure changes; the figure alone does not separate them.

Adding liquidity in Table 4 brings fully conditional adjusted $R^2$ to 2.03% for the combined universe and 1.99% for NYSE-AMEX. But NYTURN remains -0.109 with $t=-4.38$ and NASDTURN -0.119 with $t=-3.76$. A factor for sensitivity to liquidity shocks does not absorb a characteristic proxying liquidity level. The authors also try a high-minus-low turnover factor and report worse performance, without a full alternative table.

Adding WML in Table 5 leaves RET2-3, RET4-6, and RET7-12 at 0.754, 0.717, and 0.666 in the fully conditional combined sample, with $t=3.21,5.31,6.72$. Average adjusted $R^2$ is 2.06%. NASDAQ turnover loses significance under this model, but NYSE-AMEX turnover remains significant. Thus the broad conclusion about turnover has an exchange-specific qualification: not every turnover slope is significant in every augmented specification.

The market-plus-labor-income model performs worse than FF3 for these characteristics. Its fully conditional combined-sample adjusted $R^2$ is 3.99%, versus 4.20% unconditionally. SIZE remains significant at -0.106 ($t=-2.65$) and BM at 0.137 (3.33). In the NYSE-AMEX subset it can absorb size but not value. Human-capital inclusion is therefore only a partial improvement.

The quarterly consumption CAPM performs poorly. Table 7 reports adjusted $R^2$ values from 14.90% to 18.98%, and the fully conditional specification still has strongly significant size, value, turnover, and lagged-return coefficients. Size even reverses sign. The magnitudes are quarterly and arise under a different factor construction; directly comparing them with monthly slopes would be misleading. The reported $cay$-scaled versions also fail at the individual-stock level, but those tests are not tabulated.

The most flexible five-factor version adds both liquidity and WML and conditions betas on size, value, turnover, trailing-twelve-month return, and their interactions with default spread. This means up to ten loading terms per factor. Table 8 reduces adjusted $R^2$ to 1.55%, the lowest reported. Yet NYTURN is -0.079 ($t=-3.98$), RET2-3 0.772 (4.15), RET4-6 0.669 (6.04), and RET7-12 0.542 (7.34). NASDTURN is -0.043 with $t=-1.89$, again weaker than its NYSE counterpart. Greater conditional flexibility improves aggregate fit without removing momentum.

## Time-varying alpha: what changes in the dependent variable

The final experiment augments the FF3 time-series model with an additive business-cycle component:

$$
r_{jt}=\alpha_{j0}+\alpha_{j1}'BC_{t-1}
+\beta_{j,t-1}'FF_t+u_{jt},
$$

where $BC$ contains dividend yield, default spread, term spread, and the three-month Treasury-bill yield. Betas retain the earlier conditional parameterization. The second pass now uses

$$
\widetilde R^*_{jt}=\widehat\alpha_{j0}+\widehat u_{jt}
=r_{jt}-\widehat\beta_{j,t-1}'FF_t-\widehat\alpha_{j1}'BC_{t-1}.
$$

This is a different economic object from the earlier adjusted return. It removes a forecastable alpha component as well as factor payoffs. Treating Table 9 as simply a more successful risk model would conceal the key distinction.

In the fully conditional column, momentum slopes become -0.423 for RET2-3, -0.095 for RET4-6, and 0.370 for RET7-12, with corrected $t=-1.21,-0.40,1.89$. The positive momentum associations are no longer significant at the usual 5% level. However, SIZE becomes -0.285 ($t=-10.36$), BM -0.175 (-4.29), NYTURN -0.311 (-10.05), and NASDTURN -0.787 (-15.79). Average adjusted $R^2$ is 2.37%, higher than the conditional FF3 residual-return regression's 2.23%. The operation is a decomposition of where momentum predictability lies, not a uniform improvement in exact pricing.

The article is explicit that macro-sensitive alpha does not prove compensation for risk. An omitted factor could cause it, but time-varying mispricing or another predictive mechanism could also do so. Establishing an omitted rational factor would require a priced payoff or SDF restriction beyond this regression. Business-cycle covariance of alpha is evidence about systematic timing, not the missing economic identification.

Using default spread alone removes shorter-horizon momentum more effectively than the months 7-12 component. Robustness to quarterly frequency, the NYSE-AMEX-only universe, CAPM, and FF3 plus liquidity is reported qualitatively, without full tables. The continuing negative turnover slope suggests it differs from momentum's macro-linked component, but the authors' suggestion that liquidity is largely a market-design phenomenon remains an interpretation rather than a demonstrated exclusion of aggregate conditions.

## Interpreting the statistical comparison

The cross-sectional slopes are average characteristic rewards after each model's risk subtraction. A failure of a size slope under constant FF3 followed by insignificance under conditional FF3 is evidence that the chosen exposure dynamics account for that particular average association. It is not a joint likelihood-ratio test of the entire asset-pricing system. The article does not provide a single family-wise test covering all characteristics, factor menus, loading specifications, exchange subsets, frequencies, and additional unreported conditioning choices.

The average cross-sectional adjusted $R^2$ is useful but informal. All second-pass regressions have the same right-hand-side characteristics, which controls one dimension of model complexity. Their dependent variables nevertheless differ because each first-pass model subtracts a different fitted risk component. Consequently, the numerator and denominator of cross-sectional $R^2$ both change. A lower residual-characteristic $R^2$ should be read together with slope magnitudes, corrected uncertainty, and the economic definition of the residual, rather than as an invariant out-of-sample loss score.

The factor-mimicking calculation has a related distinction. Maximizing correlation with a nontraded state variation makes the fitted portfolio useful for spanning that variation, but it does not itself identify the state price. The test assumes the mimicking factor can enter the exact traded-factor pricing representation. If the asset basis misses important consumption or labor-income risks, its empirical failure combines that spanning limitation with the substantive model restriction. Conversely, adding enough return-based factors can improve fit without identifying a consumption mechanism.

Several printed details deserve an audit before automated extraction. Table 2's fully scaled combined-sample intercept is positive 0.340 while its displayed $t$ statistics are negative, an internal sign inconsistency. Table notes often cite Shanken (1990), whereas the methodological discussion attributes the estimated-beta standard-error correction to Shanken (1992). The introductory August sample start conflicts with the July start and 450-month count used throughout the tables. None of these ambiguities changes the main size/value/momentum comparison above, but they should not be silently propagated into a replication specification. Original regression output would be required to resolve the intercept discrepancy; the source does not establish its corrected value.

## What a faithful replication would do

Construct the screened panel and point-in-time characteristics first, preserving exchange-specific turnover and the accounting lag. Build each model's traded factor series and, separately, the nontraded-factor mimickers. Fit the stock-specific full-sample interaction regressions exactly as described, retaining intercepts. For each month, compute realized adjusted returns using that month's factor realizations and predetermined characteristics. Demean the cross-sectional characteristics, include the NASDAQ dummy, and estimate the monthly second-pass slopes. Average them through time and reproduce both estimated-beta standard-error corrections. Only then compare the model columns and the time-varying-alpha decomposition.

This sequence reproduces the paper's *in-sample diagnostic*. A forecasting implementation would require rolling or expanding first-pass coefficients, point-in-time macro vintages, and different inference. The authors say that a handful of random checks did not change conclusions when addressing look-ahead, but this is not a comprehensive out-of-sample validation. Short histories relative to the largest interaction model also require explicit rank and numerical-conditioning checks; no regularization, ridge penalty, or shrinkage tuning is part of the reported method.

No portfolio weights are optimized, so there is no turnover of the investment strategy, leverage limit, capacity calculation, borrow assumption, or net trading return to reconstruct. The turnover variable is a stock characteristic, not strategy turnover. Statistically significant adjusted-return slopes therefore cannot be converted directly into monetizable factor-neutral alpha without a separate portfolio and execution study.

## Assessment and source map

The durable result is the separation between characteristic-related beta variation and predictable residual returns. Security-level conditional FF3 exposures can account for size/value patterns missed by fixed loadings; simply including factors named liquidity and momentum does not ensure they span those characteristic effects. The time-varying-alpha experiment then locates momentum's association in a macro-predictable part of residual returns while exposing other remaining pricing errors.

The strongest limitations are full-sample fitting, generated mimicking portfolios, incomplete reporting of several robustness exercises, and a dependence on a finite set of nonlinear loading specifications. Absence of a significant average slope is not proof of a true equilibrium model, and the reemergence of strong size/value slopes after macro-alpha removal shows why the dependent variable must always be stated with the result.

Equations (1)-(8), pp. 1008-1010, define conditional pricing, adjusted returns, and beta interactions. Equations (9)-(10), pp. 1011-1012, define mimicking portfolios. Pages 1012-1015 provide screens and transformations. Tables 2-8, pp. 1017-1033, compare risk models; Figure 1 is on p. 1022. Equation (11) and Table 9, pp. 1034-1036, contain the macro-alpha decomposition.

The direct antecedents are Brennan, Chordia, and Subrahmanyam (1998), “Alternative Factor Specifications, Security Characteristics, and the Cross-Section of Expected Stock Returns”; Shanken (1992), “On the Estimation of Beta-Pricing Models”; Jagannathan and Wang (1998), “An Asymptotic Theory for Estimating Beta-Pricing Models Using Cross-Sectional Regression”; Gomes, Kogan, and Zhang (2003), “Equilibrium Cross-Section of Returns”; and Chordia and Shivakumar (2002), “Momentum, Business Cycle and Time-Varying Expected Returns.” The separate Avramov-Chordia 2006 article “Predicting Stock Returns” is a related portfolio study, not another title for this paper.
