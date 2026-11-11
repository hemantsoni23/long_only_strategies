# The Accrual Anomaly: Risk or Mispricing?

**David Hirshleifer, Kewei Hou, and Siew Hong Teoh (2012).** *Management Science* 58(2), 320–335, doi:10.1287/mnsc.1100.1289. Received 13 May 2010, accepted 4 November 2010, published online 15 February 2011, and published in the February 2012 issue. Source: [AccrualAnomaly_HirschleiferHouTeoh_2012.pdf](../../Finance/AccrualAnomaly_HirschleiferHouTeoh_2012.pdf). The filename misspells Hirshleifer; the author spelling above follows the article. All 16 PDF pages, including endnotes and references, are covered here. Printed page 320 is PDF page 1; there is no separate mathematical appendix in this version.

## Why this matters

A factor constructed from a return-predictive characteristic can explain the returns of portfolios sorted on that same characteristic without establishing that investors receive compensation for fundamental risk. The factor loading can simply proxy for the characteristic's mispricing. Hirshleifer, Hou, and Teoh apply the characteristics-versus-covariances logic of Daniel and Titman to operating accruals. They first show that low-accrual stocks share return variation and that an accrual factor improves a conventional factor model. They then separate accrual levels from accrual-factor exposures and ask which actually predicts returns.

The empirical answer favors the characteristic. Conditional on similar size and accrual levels, higher exposure to the accrual factor does not bring higher average returns. Conversely, accrual levels retain strong explanatory power when factor loadings enter cross-sectional regressions. The contribution is this separation, not the discovery of the accrual anomaly, which is attributed to Sloan (1996), nor a new formal theory of limited attention. The paper supplies an empirical discrimination strategy and tests alternatives based on cash-flow-to-price and Campbell–Vuolteenaho news factors.

The behavioral motivation is specific: investors may treat reported earnings as a homogeneous signal even though cash flows are more persistent than accruals. High accruals then produce overoptimistic valuations and low subsequent returns. This does not imply that every accrual is manipulated or unreliable. The accounting characteristic can contain both legitimate working-capital investment and discretionary adjustments; the proposed failure concerns how investors price their persistence. The authors distinguish their study of **accrual levels** from studies asking whether **accrual quality** is priced.

The risk null is also specific enough to test. If a characteristic predicts returns because it identifies a common priced exposure, an appropriate factor-mimicking portfolio should capture that exposure, and variation in loading independent of the characteristic should be rewarded. Failure of that implication is more informative than the usual rejection of an arbitrary benchmark. It still depends on the quality of the mimicking factor, the estimation of time-varying betas, and the adequacy of the conditioning design; it is not a theorem excluding every possible rational model with frictions.

## Sample and accounting construction

The sample is the intersection of CRSP monthly returns and the Compustat industrial annual file for NYSE, AMEX, and NASDAQ firms, with portfolio returns from **July 1967 through December 2005**, or 462 calendar months. At the end of June in year $t$, the accounting variables use fiscal years ending in calendar year $t-1$; returns run from July $t$ through June $t+1$, subject to the December 2005 endpoint. This six-month convention follows Fama and French and is intended to keep accounting information available before the holding period.

Operating accruals use the indirect balance-sheet method throughout the sample, including after cash-flow statements became available. For fiscal year $s$, define current assets $CA_s$, cash $C_s$, current liabilities $CL_s$, short-term debt $D_s$, taxes payable $TP_s$, depreciation and amortization expense $DA_s$, and total assets $A_s$. Equation (1), printed page 323/PDF page 4, is

$$
ACC_s=\frac{(\Delta CA_s-\Delta C_s)-(\Delta CL_s-\Delta D_s-\Delta TP_s)-DA_s}{A_{s-1}}.
$$

The denominator is **lagged**, not average, total assets. Changes are annual accounting differences. Keeping the indirect definition is intended to maintain comparability before and after SFAS 95 in 1988; substituting income minus cash flow from operations after 1988 would be a different signal. A reproduction should retain the stated definition before comparing an alternative construction, since acquisitions, divestitures, and classifications can affect balance-sheet changes.

Size is June market capitalization. Book equity is stockholders' equity, with fallbacks to common equity plus preferred-stock par value or assets minus liabilities, plus deferred taxes and investment tax credit, less preferred-stock book value and postretirement assets. Book-to-market divides this book equity by market capitalization at the previous December year-end. The article does not provide the full Compustat item-code mapping, preferred-stock hierarchy, handling of missing individual components, negative-book-equity rule, link-table filters, exchange/share-code restrictions, or delisting-return convention. These choices must be documented in a reproduction rather than filled in silently from a modern library implementation.

The extra return-history condition applies to test portfolios: a stock must have at least 24 monthly returns during the preceding five years. This is not stated as a requirement for constructing the basic factor itself, which uses nonmissing size and accruals. Imposing the history filter everywhere would change factor composition and could alter the relationship between the factor and the test assets.

## The accrual factor and its mean–variance role

Each June, independently sort eligible firms into two size groups at the NYSE median and three accrual groups at the NYSE 30th and 70th percentiles. The six intersections are small or big crossed with low, middle, or high accruals. Compute value-weighted monthly returns for each intersection during the next holding year. The factor is

$$
CMA_t=\tfrac12(R_{S/L,t}+R_{B/L,t})-\tfrac12(R_{S/H,t}+R_{B/H,t}).
$$

CMA here means **conservative minus aggressive accruals**. It is the specific accrual factor defined in this article; the label alone is insufficient to identify a dataset. Equal weighting across size legs and value weighting within legs are both essential. It is not an equal-weighted low-minus-high stock portfolio.

The market excess return, SMB, and HML are obtained from Kenneth French's data library. The market is the value-weighted NYSE/AMEX/NASDAQ return minus the one-month Treasury-bill rate. Table 1, printed page 324/PDF page 5, reports monthly percentage returns:

| Factor | Mean | Standard deviation | t-statistic of mean | Monthly Sharpe ratio |
|---|---:|---:|---:|---:|
| Market excess return | 0.45 | 4.56 | 2.12 | 0.099 |
| SMB | 0.20 | 3.30 | 1.32 | 0.061 |
| HML | 0.45 | 3.04 | 3.19 | 0.148 |
| Accrual CMA | 0.27 | 1.70 | 3.45 | 0.159 |

The small-stock accrual spread is 0.34% per month and the big-stock spread 0.20%. The underlying small low/middle/high portfolios return 1.31%, 1.39%, and 0.97%; the big counterparts return 0.95%, 1.00%, and 0.75%. Those are raw portfolio returns, whereas the market row is an excess return and the long–short factors require no subtraction of the risk-free rate. This distinction matters when verifying the table.

CMA's correlations with the market, SMB, and HML are −0.17, −0.17, and 0.18. A cash-flow-to-price factor has correlation 0.91 with HML but only 0.16 with CMA, according to an unreported calculation described in the text. Correlations with the term spread, Treasury-bill rate, corporate default spread, and monthly industrial-production growth are each reported below 0.10. These findings describe limited overlap with selected proxies, not proof that no macroeconomic risk is present.

Let $\bar f$ and $\widehat\Omega$ be sample factor means and covariances. The ex post tangency weights are proportional to $\widehat\Omega^{-1}\bar f$, normalized to sum to one. Using market, SMB, and HML gives weights 0.27, 0.17, and 0.56 and a monthly Sharpe ratio of 0.25. Adding CMA gives approximately 0.18, 0.12, 0.31, and 0.40, with mean 0.35%, standard deviation 1.18%, and Sharpe ratio 0.30. Rounding makes the displayed weights sum to 1.01.

This calculation shows that accrual returns occupy a valuable direction in the sample covariance matrix. It is not a real-time allocation rule. Means, covariances, and weights are all estimated using the same full sample; the authors explicitly acknowledge upward bias in ex post Sharpe ratios. There are no constraints, transaction costs, covariance regularization, turnover penalties, or out-of-sample weights. The reported 40% weight is a normalization across factor payoffs, not a claim that 40% of a practical investor's unlevered capital should be allocated to an accrual stock portfolio.

## First-stage evidence: common variation and apparent pricing success

To form test assets, the authors use independent NYSE 33rd and 67th percentile breakpoints for both size and accruals, producing nine value-weighted portfolios. The test assets therefore differ from the six portfolios underlying CMA. Stocks need the 24-of-60-month return history. For each portfolio they estimate the three-factor and augmented four-factor regressions

$$
R_{i,t}-R_{f,t}=a_i+b_i(R_{M,t}-R_{f,t})+s_iSMB_t+h_iHML_t+\varepsilon_{i,t},
$$

$$
R_{i,t}-R_{f,t}=a_i+b_i(R_{M,t}-R_{f,t})+s_iSMB_t+h_iHML_t+c_iCMA_t+\varepsilon_{i,t}.
$$

If these traded excess-return factors span expected returns, the intercepts are zero and each factor's risk premium is its own mean return. A significant loading establishes comovement conditional on the other regressors. It does not by itself establish a positive price for that exposure.

Table 2, printed page 326/PDF page 7, gives the following compact comparison. Returns and alphas are percentage points per month; the final column is a dimensionless loading.

| Size/accrual group | Mean excess return | FF3 alpha | FF3+CMA alpha | CMA loading |
|---|---:|---:|---:|---:|
| Small/low | 0.89 | 0.05 | −0.07 | 0.42 |
| Small/middle | 0.88 | 0.05 | 0.05 | −0.02 |
| Small/high | 0.54 | −0.29 | −0.24 | −0.14 |
| Medium/low | 0.76 | 0.05 | 0.03 | 0.10 |
| Medium/middle | 0.77 | 0.05 | 0.11 | −0.23 |
| Medium/high | 0.52 | −0.17 | −0.04 | −0.46 |
| Big/low | 0.46 | 0.09 | −0.09 | 0.68 |
| Big/middle | 0.51 | 0.11 | 0.17 | −0.23 |
| Big/high | 0.27 | −0.08 | 0.09 | −0.61 |

The low-minus-high accrual return difference averages 26 basis points across size groups. FF3 leaves a 24-basis-point alpha difference, with probability 0.03% for equality of the average low- and high-accrual intercepts. Its Gibbons–Ross–Shanken joint test of nine zero intercepts has probability 0.01%. Adding CMA reduces the average low-minus-high intercept difference to 2 basis points, with equality-test probability 27.41%. Eight of nine CMA loadings have absolute t-statistics above two, and six exceed six. The factor captures a real common component of realized returns.

Yet the augmented model still fails the joint zero-alpha test, with GRS probability 0.10%. Small/high accrual has alpha −0.24%, t = −2.91, and big/middle accrual has alpha 0.17%, t = 3.05. Thus removal of the *monotone accrual spread* is not equivalent to pricing all nine assets. The authors correctly keep these claims separate. More importantly, even a perfect fit on accrual-sorted assets would not distinguish a risk factor from a return factor whose loading tracks mispricing.

Alternative benchmarks do not explain the original spread. Decomposing the market into expected returns, discount-rate news, and cash-flow news using the Campbell–Vuolteenaho series increases the low-minus-high intercept difference to 30 basis points, probability 0.01%. Replacing HML with the CFO/Price factor leaves 25 basis points, probability 0.02%; adding that factor to FF3 also fails. The news series were supplied by Vuolteenaho. The paper describes their four-state VAR inputs but does not reproduce the entire factor-generation algorithm, parameters, and historical input data, so the supplied series or a separately documented reconstruction is required for exact replication.

## The decisive design: hold characteristics fixed, vary exposure

Within each of the nine size/accrual groups, estimate each stock's preformation CMA loading from the four-factor regression over the previous 60 months, requiring at least 24 observations. Split the group into low, middle, and high loading terciles using the 33rd and 67th percentile cutoffs. This creates 27 value-weighted test portfolios. The outer size/accrual breakpoints are NYSE-based; the text describes the inner loading split within each group and does not give a separate NYSE-only inner-breakpoint rule, so a reproduction should state that choice explicitly.

The sort is intended to hold size and accruals approximately fixed while producing persistent variation in exposure. For example, small/low-accrual stocks have almost unchanged accrual values across the loading terciles, while postformation CMA loadings rise from 0.15 to 1.06. Big/low-accrual portfolios rise from 0.02 to 1.41. The preformation exposures are much more dispersed than the realized postformation exposures, demonstrating estimation noise and shrinkage, but the postformation spread remains substantial.

Under factor pricing, high-loading stocks should earn a higher expected return after conditioning on the other factor exposures. Under the proposed characteristic-based explanation, the loading does not add a premium once accruals are held fixed. Across the nine groups, low-loading portfolios earn 0.65% average monthly excess return and high-loading portfolios 0.53%. The direction is opposite to the positive CMA premium's naive loading prediction.

For each size/accrual cell $g$, form the characteristic-balanced spread

$$
D_{g,t}=R_{g,H_c,t}-R_{g,L_c,t},
\qquad D_t=\frac19\sum_{g=1}^{9}D_{g,t}.
$$

Regress these spread returns directly on the four factors, without subtracting the risk-free rate again. Table 4, printed page 330/PDF page 11, shows eight of nine intercepts negative, four individually significant at conventional two-sided levels, and a GRS probability of 0.01% for the nine-spread system. The combined portfolio is the central result:

| Statistic for combined high-loading minus low-loading spread | Estimate | t-statistic |
|---|---:|---:|
| Mean return, % per month | −0.12 | −1.07 |
| Four-factor alpha, % per month | −0.25 | −2.65 |
| Market loading | 0.08 | 3.50 |
| SMB loading | 0.01 | 0.18 |
| HML loading | −0.23 | −6.98 |
| CMA loading | 0.73 | 13.46 |

The adjusted regression $R^2$ is 0.34. The 0.73 CMA loading is large and precisely measured after formation; failure to earn a positive return cannot simply be dismissed as a sort that failed to create exposure. Using the rounded factor means, the model-implied mean is approximately $0.08(0.45)+0.01(0.20)-0.23(0.45)+0.73(0.27)=0.132$ percent per month. Actual return of −0.12% then leaves approximately −0.252%, matching the reported alpha. This arithmetic makes the source of the rejection transparent: the model predicts compensation that the characteristic-balanced portfolio does not receive.

The zero raw mean is not a perfect standalone behavioral restriction if other factor exposures remain nonzero. Here the spread has a meaningful negative HML loading and positive market loading. The four-factor alpha and the corresponding three-factor comparison are therefore more informative than treating “characteristic-balanced” as “risk-neutral.” The paper reports that FF3 intercepts for these spreads are close to zero, consistent with CMA failing to add a priced direction conditional on the conventional factors. Nonrejection of the raw zero mean is supportive but not proof of a unique psychological mechanism.

## Cross-sectional regressions and beta measurement

The Fama–MacBeth tests estimate a cross-sectional regression every month and average the slopes over time. In schematic form,

$$
R_{i,t}=\gamma_{0,t}+\gamma_{A,t}ACC_{i,t-1}
+\gamma_{C,t}\hat c_{i,t-1}+\gamma_{Z,t}'Z_{i,t-1}+u_{i,t}.
$$

The notation $t-1$ here means information available before the return, with annually refreshed accounting variables and rolling beta estimates as specified in the paper. Portfolio regressions use the 27 test portfolios, their value-weighted accruals, and portfolio factor loadings estimated over the previous 60 months. Firm regressions add log size, log book-to-market, CFO/Price, the previous month's return, cumulative months −12 through −2, and cumulative months −36 through −13. These are distinct reversal, momentum, and long-horizon reversal controls.

Rather than use noisy individual betas in the firm regressions, the authors assign each stock the betas of its size/accrual/preformation-loading portfolio. This shrinks estimated exposures toward a more precisely estimated group mean. It reduces individual measurement error but also assigns common exposures to heterogeneous firms; it does not make beta measurement error disappear or independently identify a structural risk exposure.

Table 5, printed page 331/PDF page 12, contains the key nested comparisons:

| Regression | Accrual slope (t) | CMA-loading slope (t) |
|---|---:|---:|
| Portfolio returns on CMA loading only | — | 0.1414 (1.66) |
| Portfolio returns on accruals only | −1.5943 (−4.16) | — |
| Portfolio returns on both | −1.4323 (−3.01) | 0.0138 (0.13) |
| Portfolio returns on both plus FF3 betas | −1.4602 (−4.09) | 0.0023 (0.03) |
| Portfolio returns with market-news betas | −1.6135 (−4.29) | −0.0140 (−0.15) |
| Firm returns on CMA loading only | — | 0.2453 (2.72) |
| Firm returns on accruals only | −1.2151 (−6.37) | — |
| Firm returns on both | −1.0443 (−5.45) | 0.1296 (1.39) |
| Firm returns, characteristics and FF3 betas included | −0.8319 (−5.11) | 0.0657 (0.99) |
| Firm returns, characteristics and news betas included | −0.8633 (−5.13) | 0.0551 (0.78) |

The table uses percentage-return units, while accruals are scaled by assets. A 0.10 accrual difference multiplied by −1.4602 corresponds to about −0.146 percentage points per month in that regression, not −14.6%. These are partial linear slopes, not returns on a decile strategy with a fixed risk budget. Cross-sectional regressions also place more influence on small firms than the value-weighted portfolio tests; agreement across the two designs is useful precisely because their implicit weights differ.

## What is identified by the conditional test

The regression logic can be expressed through residualization. Within a monthly cross-section, project the estimated CMA loading on accruals and the other included characteristics, and call the residual $\tilde c_i$. Likewise residualize returns against those controls to obtain $\tilde R_i$. The partial loading coefficient is

$$
\hat\gamma_C=\frac{\sum_i\tilde c_i\tilde R_i}{\sum_i\tilde c_i^2}.
$$

The unconditional positive loading slope can disappear because its predictive content lies in the portion correlated with accruals. That is exactly the distinction the nested regressions seek. The triple sorts approximate a related comparison through narrow characteristic cells, while preserving a sizeable realized loading spread. Neither design requires that accruals and CMA exposures be uncorrelated in the full universe; their correlation is the reason an unconditional factor regression is insufficient.

A useful falsification criterion is not merely a positive t-statistic on CMA in a return regression. Conditional loading variation must earn the premium implied by the model, and the characteristic should not add incremental expected return once relevant exposures are controlled. Conversely, the behavioral account is challenged if characteristic-balanced loading spreads earn reliably positive returns consistent with their exposures. The observed −0.25% alpha is therefore a test of a quantitative expected-return restriction, not simply an absence of significance in a noisy beta coefficient.

The high-Sharpe-ratio argument is separate from this conditional test. For a positive-mean stochastic discount factor $m$, the Hansen–Jagannathan restriction bounds attainable Sharpe ratios by $\sigma(m)/E[m]$. Adding CMA raises the sample maximum and hence the volatility requirement for any candidate discount factor that prices these payoffs. This restriction concerns all admissible SDFs for the maintained payoff set; connecting it to a particular coefficient of risk aversion requires an additional preference and consumption model. The article's discussion treats that requirement as economically demanding. The characteristics-versus-covariances results supply the more direct evidence on its proposed accrual-factor explanation.

## Robustness, limitations, and reproduction priorities

The authors address the main beta-noise objection in three ways: persistent postformation loading spreads, portfolio beta assignment, and alternative estimation windows. A 60-month window centered around formation yields the same qualitative conclusion, reportedly more strongly. Because that window includes future returns, it is a diagnostic of exposure measurement, not a tradable forecast construction. Controlling for momentum also preserves the conclusions. These additional results are described without full tables; they should not be assigned invented magnitudes or p-values.

Accrual ranks are not completely transient. About 40% of firms in an extreme accrual quintile remain there next year, compared with 90% for size, 65% for book-to-market, and 25% for prior 12-month returns. This weakens the claim that accrual mean reversion necessarily makes all estimated loadings useless. It does not rule out economically relevant conditional betas or nonlinear risks. Nor does a high realized Sharpe ratio alone logically refute rational pricing: the Hansen–Jagannathan implication is a demanding stochastic-discount-factor volatility requirement, conditional on valid returns and the relevant investment opportunity set.

A faithful replication should first reproduce the accounting identity, the six factor portfolios, and the nine test portfolios, then the 27 exposure-sorted portfolios. Preserve the difference between 30/70 factor breakpoints and 33/67 test-asset breakpoints. Verify the contemporaneous factor-regression units and retain both preformation and postformation betas. Compute the characteristic-balanced returns before fitting models; averaging intercepts from separately estimated portfolios should agree with the intercept of an equally weighted combined return series when sample windows and regressors are identical. That equality is a useful implementation check rather than a separate economic result.

For the GRS tests, save the joint residual covariance and factor mean/covariance estimates, the exact common month set, and the degrees-of-freedom convention. For the cross-sectional tests, record the monthly cross-section, intercept treatment, return units, outlier handling, and standard-error procedure. The paper reports time-series t-statistics but does not supply code, a HAC-lag specification, observation counts by year, or a complete missing-variable policy. Contemporary replication should report conventional results matching the article and label alternative inference or cleaning decisions separately.

All portfolio returns are gross of trading and financing frictions. There is no borrow-cost estimate, short availability filter, spread or market-impact model, turnover table, capacity analysis, or post-2005 holdout. The high-accrual side drives much of the decline between middle and high groups, so short-side feasibility matters. The authors note that mean CMA return declines from 0.29% before the Sloan-publication division to 0.22% afterward, while monthly volatility rises from 1.62% to 1.95%. They interpret this as consistent with growing arbitrage activity and crowding, but do not identify that mechanism causally or establish present-day profitability.

For portfolio research the strongest lesson is methodological. A characteristic factor can be an effective risk-control instrument because it captures return comovement even when its estimated exposure is not a rewarded source of expected return. Conversely, neutralizing the characteristic itself may remove the forecast one intended to exploit. The paper supports keeping the accrual signal and its return-covariance exposure conceptually distinct, testing each conditional on the other, and evaluating any implemented forecast after the costs and constraints omitted from the published tests.
