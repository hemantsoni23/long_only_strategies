# Hedge Fund Characteristics and Performance Persistence

Manuel Ammann, Otto Huber, and Markus Schmid. August 2010 working-paper version. Source: [HedgeFunds_AmmanHubertShmid_2010.pdf](../../Finance/HedgeFunds_AmmanHubertShmid_2010.pdf), 49 pages, SSRN identifier 1650232. The spelling of the source filename differs from the authors' names; the bibliographic names here follow the title page. PDF and printed page numbers coincide. This note covers the full paper, including the factor dictionary in Appendix A and all eight empirical tables.

## Why this matters

A hedge-fund investor cannot necessarily redeem one manager and subscribe to another every month. Notice periods, redemption schedules, and restrictions on new investments make persistence over six months to several years more relevant than a short-lived ranking effect. The paper asks whether past performance predicts subsequent performance at those horizons, and whether observable fund characteristics improve the selection of persistent winners.

Its distinctive contribution is a two-stage empirical argument. First, panel probit regressions identify characteristics associated with repeated above-median or below-median alpha. Second, portfolios sorted on historical alpha and an additional characteristic test whether that association translates into larger subsequent performance differences. Many characteristics are statistically related to persistence, but only strategy distinctiveness consistently improves the portfolio comparisons over horizons up to two years in this sample.

Strategy distinctiveness is measured by the part of a fund's historical return variation not explained by its peers. It can represent an original investment strategy, but it can also represent idiosyncratic risk, noisy marks, or unusual factor exposures. The paper's crisis and attrition results make that ambiguity economically important. The contribution is therefore a testable manager-selection signal and evidence about its limitations, not a demonstration that low correlation with peers necessarily reveals skill.

The headline improvement—roughly 4% per year for annual rebalancing—is an increase in the difference between selected high and low groups under one risk model. It is neither a guaranteed gain to an investor holding only the selected winners nor a directly investable, cost-adjusted long-short hedge-fund strategy. The actual top-portfolio improvements, comparison model, and units should be kept separate.

## Building the investable-history sample

The baseline merges Lipper/TASS and CISDM over January 1994–December 2008. Live and dead funds are retained, and the analysis begins after both providers started retaining funds that stopped reporting. The authors first remove duplicates within a vendor, including multiple share classes and related onshore/offshore vehicles. They then match across vendors using fund names, strategy classifications, and return correlations. The exact matching thresholds and rule for choosing among duplicate classes are not published, so those operations cannot be reproduced uniquely from the paper alone.

Backfilled returns are removed using the reporting-entry date, known for about 95% of the TASS funds in the sample. For the remaining TASS funds and all CISDM funds, the first twelve observations are dropped. This fallback is a proxy for entry-date information, not a guarantee that every backfilled observation is removed. The paper calculates two distinct backfill diagnostics: the return difference between all observations and the cleaned portfolio is 3.2 basis points monthly; the difference between backfilled and non-backfilled observations is 38 basis points monthly, or 44 basis points over the earlier comparison period. Their denominators differ, so they are not contradictory estimates of the same quantity (p. 8, footnote 2).

Eligibility requires at least 24 non-backfilled monthly returns because rolling alpha and distinctiveness estimates use two years of data. The 36-month persistence analysis requires at least 36 observations. Funds of hedge funds and non-USD funds are excluded. A fund's assets must exceed USD 5 million at least once during its non-backfilled history. The resulting sample contains 4,311 funds with USD 403 billion under management. This last size criterion uses an eventual-history condition as described; a strictly prospective deployment would instead impose a threshold using assets known at the decision date.

The minimum-history rule can select survivors even though dead funds are included. Requiring 36, 48, or 60 observations reduces the sample to 3,366, 2,635, and 2,051 funds. The authors report qualitatively similar conclusions and roughly two to three basis points higher portfolio returns per additional year of required history. Exact treatment of discontinuous histories, vendor revisions, reporting delays, and reappearing funds is not specified. Keeping dead records is necessary for reducing survivorship bias but does not recover returns after a fund stops reporting.

## Desmoothing reported returns

Before risk adjustment, the authors attempt to remove stale-price effects with the Getmansky–Lo–Makarov MA model. Let $R_{i,t}^O$ be a reported return and $R_{i,t}$ a latent economic return. For strategy $s$,

$$
R_{i,t}^O=\theta_{s,0}R_{i,t}+\theta_{s,1}R_{i,t-1}+\theta_{s,2}R_{i,t-2},\qquad
\sum_{j=0}^{2}\theta_{s,j}=1.
$$

The economic model imposes weights in $[0,1]$ and serially uncorrelated latent returns. The paper estimates an MA(2) by maximum likelihood for each strategy using Stata. It normalizes the conventional MA coefficients by $1+a_1+a_2$, producing $(\theta_0,\theta_1,\theta_2)=(1,a_1,a_2)/(1+a_1+a_2)$. Importantly, footnote 8 says the individual weight bounds are **not imposed during estimation**; they are used as a specification check. One should not substitute constrained estimation and claim it is the published method.

Given nonzero $\theta_{s,0}$, algebraic inversion gives the reconstruction

$$
\widehat R_{i,t}=\frac{R_{i,t}^O-\widehat\theta_{s,1}\widehat R_{i,t-1}-\widehat\theta_{s,2}\widehat R_{i,t-2}}{\widehat\theta_{s,0}}.
$$

This is a useful implementation equation derived from the source model, not a separately printed algorithm. The paper does not supply the fitted strategy weights, the likelihood initialization, the first two reconstructed returns, the exact strategy-series construction used for the MA estimation, or the date window over which weights are estimated. Small current weights or noninvertible estimates can make recursion unstable. For a real-time extension, estimate the weights using training data only and record boundary failures; that restriction is not documented for the original full-sample analysis.

Desmoothing can remove mechanical persistence caused by marking, but it is model dependent. Genuine predictable economic returns and changing liquidity violate the simple assumptions. The authors recognize that the procedure itself may affect persistence and rerun their portfolio analyses on reported returns, finding broadly unchanged conclusions in unreported tables (p. 31). Those results are supportive, but the raw-versus-desmoothed coefficients and complete diagnostics are unavailable.

## Two risk models and their factor selection

Fund alpha is estimated by OLS in rolling 24-month windows. In explicit notation, for a selected factor vector $f_{s,t}$ one may write the excess-return version as

$$
\widehat R_{i,t}-r_{f,t}=\alpha_{i,\tau}+\beta_{i,\tau}'f_{s,t}+\epsilon_{i,t},\qquad t=\tau-23,\ldots,\tau.
$$

The intercept is expressed in monthly percentage points. The source discusses excess-return and zero-investment factor conventions but does not print a single complete regression equation resolving every input transformation. A replication must maintain the same risk-free convention for the dependent variable and factors; subtracting the risk-free rate twice would change alpha.

The first model, called SW, selects factors at the strategy-index level. Construct an equally weighted index of funds in each strategy, run a forward stepwise procedure over the entire sample with constant coefficients, add a candidate significant at 5%, and remove an existing factor if it no longer meets the 10% retention threshold jointly with the others. Stop when no addition qualifies or seven factors have been selected. Use the resulting factor set for every fund in that strategy throughout the sample, while estimating fund-level coefficients in rolling windows. The paper does not specify tie-breaking, all intermediate paths, or missing-factor handling.

The source repeatedly refers to a pool of 23 candidates, while Appendix A's named components do not unambiguously reconcile to that count. It lists five equity indices—MSCI World ex USA, emerging markets overall, emerging-market Latin America, emerging-market Asia, and Russell 3000—two bond return indices, Baa and TED spread variables, a dollar index, VIX, SMB, HML, momentum, four S&P option-return series, four asset-class trend-following series, commodities, REITs, and convertible bonds. Counting these separately gives 25; a footnote additionally lists a short-rate trend-following series. The precise selection pool therefore requires the authors' data. The final selected sets in Table 1, however, are explicit and permit a replication conditional on those sets.

The option factors use ATM calls and puts, calls at 107.5% moneyness, and puts at 92.5% moneyness. Prices are Black–Scholes based on historical implied volatility, realized dividend yields, and interest rates. The 7.5% out-of-the-money choices are intended to capture tail-risk exposures while avoiding almost redundant near-ATM factors. Maturity, option rolling rules, volatility-surface choice, dividend timing, and exact return normalization are not supplied. VIX's precise transformation is also insufficiently described: a label “VIX” does not by itself identify a tradable volatility excess return.

The final SW factor sets are:

| Strategy | Factors in Table 1 |
|---|---|
| Convertible arbitrage | CS High Yield II; investment-grade ML convertible bonds; Russell 3000; MSCI emerging markets |
| Dedicated short bias | S&P ATM call; Russell 3000; HML; SMB; momentum |
| Emerging markets | Momentum; MSCI emerging markets; dollar-index spot |
| Equity market neutral | Momentum; S&P 92.5% put; S&P 107.5% call; CS High Yield II; stock trend following |
| Event driven | S&P 92.5% put; CS High Yield II; SMB; S&P ATM call; MSCI emerging markets; HML; stock trend following |
| Fixed-income arbitrage | CS High Yield II; change in Baa spread |
| Global macro | Change in three-month TED spread; Citi world government bonds; MSCI emerging markets; currency trend following; momentum |
| Long/short equity | Russell 3000; SMB; MSCI emerging markets; momentum; stock trend following; MSCI World ex US; world REITs |
| Managed futures | Currency trend following; Citi world government bonds; bond trend following; S&P GS commodities; momentum; commodity trend following |
| Multi-strategy | MSCI emerging markets; world REITs; stock trend following; VIX; SMB |

The three spread conventions should not be conflated. Appendix A defines the SW Baa variable using the monthly change in a 30-year corporate-versus-government yield spread, while the FH comparator uses ten-year Treasury yield and Baa-versus-ten-year Treasury spread changes. Table 1 labels the SW TED variable as a change in the three-month TED spread.

The second model is the Fung–Hsieh seven-factor model, FH: bond, currency, and commodity primitive trend-following returns; S&P 500 monthly total return; a small-minus-large equity spread; change in the ten-year Treasury constant-maturity yield; and change in the Moody's Baa-minus-ten-year-Treasury spread. The text allows either Wilshire small-minus-large or Russell 2000-minus-S&P 500 as the size spread without identifying the final choice. The model labels therefore do not eliminate all implementation ambiguity.

A useful fit check selects SW factors on January 1994–June 2001 and evaluates July 2001–December 2008. Strategy-level average $R^2$ is 0.666 with first-half selection versus 0.724 with second-half selection; FH yields 0.507. These are index-level fits, not individual-fund predictive alphas. They show that the selected exposures retain explanatory power, but the main persistence tables still use full-sample-selected factor sets. That fit exercise does not convert the entire selection pipeline into a strictly out-of-sample investment experiment.

## Strategy distinctiveness and other characteristics

For each fund, regress its previous 24 monthly returns on an intercept and the equally weighted index of its self-declared strategy. Let the resulting fit be $R_{i,\tau}^2$. Define the unstandardized distinctiveness score and its within-strategy standardized version as

$$
D_{i,\tau}=1-R_{i,\tau}^2,\qquad
SDI_{i,\tau}=\frac{D_{i,\tau}-\overline D_{s,\tau}}{\operatorname{sd}_{j\in s}(D_{j,\tau})}.
$$

Standardization prevents a naturally heterogeneous strategy from dominating the high-distinctiveness group. A one-unit increase in standardized SDI is one within-strategy standard deviation, not a one-percentage-point reduction in fit. The paper does not specify whether a fund is excluded from its own peer index, how strategy changes are handled, or every missing-history rule. These details matter for small categories.

SDI measures unexplained variance, not unexplained expected return. It cannot distinguish skill from random idiosyncratic risk by construction. In a single-index regression with an intercept, raw $D=1-\rho^2$ also treats strong negative and positive correlations symmetrically. An alternative score in the paper is $1-\rho$, which ranges from zero to two and behaves differently for negative correlations. Other robustness versions use the most highly correlated strategy index, the SW factor model, or both the self-declared strategy and an all-fund index. The description of the last alternative calls it “r-square” rather than one minus r-square, leaving a sign convention to clarify before reproducing that robustness test.

Monthly dollar net flow is

$$
F_{i,t}=A_{i,t}-A_{i,t-1}(1+r_{i,t}),
$$

with capital entering at month end. Missing assets inside a series are linearly interpolated; leading and trailing values are extended backward and forward from the nearest reported value. Annual relative flow aggregates the previous twelve monthly flows and divides by assets one year earlier, then winsorizes at the 1% tails. Equation 5 uses a malformed reversed-index summation; its prose supports a lagged sum such as $\sum_{j=1}^{12}F_{i,t-j}/A_{i,t-12}$. The precise endpoint convention needs clarification. Interpolation can use information unavailable contemporaneously, so a production signal should not simply inherit this historical-data treatment.

Other regressors are log assets, log age in months, log notice days, log redemption days, a closed-to-new-investment indicator, management fee, and incentive fee. When inception is unknown, age is the number of reported months. A redemption frequency coded “other” receives 1,048 trading days, described as four years. Handling of zero-day terms before logging is not reported. Manager personal investment and average leverage are added in robustness tests but sharply reduce available observations. Fees are contract characteristics, not an additional fee layer deducted by these regressions.

## Defining persistence and estimating the probit models

A winner has alpha above the cross-sectional median; a loser has alpha below it. For two successive non-overlapping evaluation periods of length $H$, the outcomes are $WW$, $LL$, and $WWLL=WW+LL$. A fund that is not a repeated winner receives zero in the WW regression, including a repeated loser; the WW sample is not restricted only to prior winners. This matters when interpreting probabilities.

A transparent representation is

$$
\Pr(WW_{i,\tau}^{(H)}=1\mid x_{i,\tau})=
\Phi(c+\gamma'x_{i,\tau}+d_{s(i)}+d_\tau),
$$

with analogous regressions for LL and WWLL, strategy and time indicators, and $H=12,24,36$ months in Table 2. The reported coefficients are probit-index coefficients, not marginal changes in probability. For a continuous variable the marginal effect is $\phi(\cdot)\gamma_j$ and depends on the observation.

The paper states both that alphas use rolling 24-month regressions and that persistence is measured over non-overlapping six- to 36-month periods. It does not fully specify how the sequence of rolling alphas is aggregated into every period-ranking statistic. If one compares two rolling intercepts less than 24 months apart, their underlying regression observations overlap even though the evaluation labels refer to different periods. Similarly, a seven-factor model cannot be estimated freely from only six observations. A replication must resolve this mapping rather than interpret “six-month alpha” as an independently estimated seven-factor six-observation intercept. This is a material reproducibility limit, not proof that the authors implemented the naive overlapping alternative.

Table 2's 12-month specification uses 111,646 fund-months and 2,734 funds. The 24- and 36-month samples shrink to 82,978/2,099 and 44,300/1,219. SDI coefficients for WW are 0.166, 0.151, and 0.118, with reported statistics 39.636, 30.603, and 17.188. LL coefficients are −0.178, −0.159, and −0.130. In the combined WWLL outcome the opposing effects mostly cancel. This demonstrates why combining persistence of success with persistence of failure can conceal economically relevant differences.

Larger size, greater relative inflows, longer notice and redemption periods, closed status, and higher management fees are positively associated with repeated winners; age is negatively associated. Incentive fees are significant for winner persistence only at twelve months. The p. 18 sentence saying a negative coefficient on log assets implies smaller winners is inconsistent with Table 2, where the twelve-month log-assets coefficient is **positive 0.028**. The negative age coefficient is −0.069. The table supports larger and younger funds, not smaller funds, conditional on these covariates.

Pseudo-$R^2$ values remain modest: 2.50% for twelve-month WW and 2.55% for LL, increasing to 3.26% and 4.05% at 36 months. Reported classification accuracy uses a 50% probability threshold; 69.73% correct for twelve-month WW is not meaningful without comparison to the base-rate classifier. The main probit table does not describe fund-clustered inference. Unreported alternatives include linear panels with fund-clustered standard errors and Fama–MacBeth regressions with heteroskedasticity/autocorrelation-consistent errors. Their qualitative similarity does not supply the missing robust probit statistics or correct automatically for all repeated-window dependence.

## Alpha regressions and what their intercepts do not establish

Table 3 regresses monthly fund alpha on characteristics, with strategy/time indicators and fund-clustered Huber–White standard errors. In the full specification, one standardized SDI unit is associated with 0.227 monthly percentage points of SW alpha, statistic 5.900, and 0.122 points of FH alpha, statistic 4.492. Size and relative flows are also positive. Log notice days is significant; log redemption days is not significant in either full-model column, despite a stronger claim in the surrounding text.

These regressions explain only about 3% of alpha variation. An additional specification combines notice and redemption days and changes the regression constant from 0.492 to −0.330 for SW and from 0.511 to −0.739 for FH. The paper interprets this as alpha disappearing after controlling for illiquidity. More narrowly, the **conditional intercept at the omitted categories and zero-valued covariates** changes. Different samples are also used: 191,691 observations without the combined restriction variable versus 156,960 with it. A constant from these characteristic regressions is not automatically the mean attainable fund alpha after a causal liquidity adjustment. The source's strong interpretation should therefore be kept distinct from what the coefficient directly measures.

## Portfolio construction and the principal evidence

For each horizon $H\in\{6,12,24,36\}$, rank eligible funds by historical $H$-month alpha into quintiles. Within each quintile, split at the median trailing 24-month SDI, producing ten groups. Evaluate subsequent performance over the next non-overlapping $H$ months and repeat the sorting after each holding period. The portfolios are equally weighted; the paper describes calculating each constituent's alpha and averaging those alphas. This is not always equivalent to estimating alpha on an investable portfolio return series, especially with strategy-specific factors and differing histories. For a fund that disappears, alpha is estimated only until it becomes defunct (p. 22, footnote 18).

The exact initial rebalance date, treatment of ties, intra-period weight drift, replacement of disappearing holdings, observation weighting across fund-periods, and ranking-alpha aggregation are not fully specified. Table 4 uses standard tests of differences in means, with no described HAC or multiple-testing correction. One should reproduce its reported statistics separately from a more conservative inference extension.

The main SW results, in monthly percentage points, are:

| Horizon | Alpha-only top minus bottom | Top-alpha/high-SDI minus bottom-alpha/low-SDI | Additional spread |
|---|---:|---:|---:|
| 6 months | 2.80 | 3.10 | 0.30 |
| 12 months | 2.29 | 2.62 | 0.33 |
| 24 months | 1.61 | 1.80 | 0.19 |
| 36 months | 0.99 | About 0.93 from displayed cells; prose 0.92 | Negative |

The first three added spreads annualize arithmetically to 3.60, 3.96, and 2.28 percentage points. These are not compound annual returns. At twelve months the top-alpha group's average SW alpha is 1.39% monthly; its high-SDI half is 1.70% and its low-SDI half 1.07%. Thus selecting the high-SDI half instead of the entire top group adds about **0.31 monthly percentage points** to that long-only selection. The 0.33-point headline comparison also changes the bottom comparison group. The high-minus-low SDI difference within the top quintile is reported as 0.64 with statistic 2.58, allowing for rounding of the constituent means.

FH gives materially smaller additional spreads: approximately 0.11, 0.07, and 0.07 monthly points at six, twelve, and 24 months. At twelve months the top FH group is 1.57%, its high-SDI half 1.69%, and the bottom low-SDI group −0.70%, giving a two-way spread of 2.39% versus 2.32% for alpha alone. Hence the broad result has some cross-model support, while the claimed economic improvement is sensitive to the risk model.

The alpha-only extreme spreads are statistically significant at 1% throughout the main table, but most within-quintile high-versus-low SDI differences are insignificant. A significant extreme alpha spread is not itself a significance test for the incremental benefit of adding SDI. At 36 months the top SW high-SDI group earns 0.61% versus 0.76% for low SDI; FH gives 0.67% versus 0.99%, the latter difference significant at 1%. The additional distinctiveness sort ceases to help at the longest horizon.

## Robustness, missing returns, and the crisis

Reversing the sort order—SDI first, then historical alpha—gives a twelve-month SW extreme spread of 2.69%. Dividing SDI into terciles with FH sorting gives 2.50%. Deciles, alternative SDI definitions, and reported rather than desmoothed returns reportedly preserve the broad conclusions. Other characteristics, including flows, size, and liquidity restrictions, fail to improve the portfolio results consistently even when they are highly significant in the earlier panels. Thus statistical association is explicitly tested against an economically stronger selection requirement.

Median-based portfolios in Table 6 reduce the influence of extreme estimated alphas. The SW alpha-only annual-horizon spread is 1.84%; adding SDI produces roughly 2.28% from rounded table cells, compared with the prose's 0.43-point incremental estimate. Ranking by alpha's t-statistic rather than its level reduces the alpha-only spread to 1.59%, and the SDI increment to about 0.09 monthly points. This is consistent with some apparent distinctiveness capturing noisy or risky alpha estimates. The table caption refers to a standard t-test for differences in medians without describing its sampling construction; exact inference for that variant requires clarification.

Attrition is lower among historical winners and higher among high-SDI funds. In Table 5, the top-alpha/low-SDI group loses 7.1% of funds annually, whereas bottom-alpha/high-SDI loses 20.0%. Top-alpha/high-SDI attrition is 10.1%, versus 15.1% for bottom-alpha/low-SDI. Pure high/low SDI groups have rates of approximately 13.2% and 10.6% in the narrative. These facts support both a skill interpretation and concern about greater idiosyncratic risk.

A back-of-envelope calculation says disappearing funds would need an annualized alpha as low as −126.3% to erase the pure-SDI advantage under the authors' assumptions. This is a hypothetical extrapolation about missing **alpha**, not an observed loss or a bounded simple investment return. It assumes a particular relation between unreported outcomes and group attrition and does not recover delisting returns. Missing return data can still matter if losses differ systematically by group or arrive in ways the annualized approximation does not capture.

Raw-return evidence is considerably weaker than alpha evidence. In Table 7, annual effective-return differences from alpha-free historical-return sorts are significant mainly at the six-month horizon. Alpha-only terminology should not be carried into this raw-return comparison: the portfolios here are sorted on past cumulative returns. One-way top-minus-bottom annual return spreads are 10.25%, 4.06%, 5.17%, and −2.08% at the four horizons. The twelve- and 24-month spreads are not statistically significant. The two-way annual raw-return spreads cited in the narrative are 11.12%, 5.26%, and 6.94% through two years. These are annual effective returns, unlike monthly regression intercepts.

The crisis exercise is particularly informative. Using TASS alone, 1,164 funds are ranked on September 2007–August 2008 performance and evaluated over September 2008–June 2009. Table 8 continues to separate historical extreme alpha groups, but high SDI no longer improves the selection. Pure-SDI SW alpha is −0.18% monthly for high SDI versus +0.15% for low SDI, a −0.33-point difference with statistic −1.90. Within the top SW-alpha quintile, high SDI earns 0.69% against 1.22% for low SDI, difference −0.53 and statistic −2.15. This is consistent with distinctiveness exposing investors to adverse idiosyncratic or omitted risks during stress.

Table 8 itself alternates between “average” and “median” in its caption and describes a median-difference t-test. The underlying aggregation therefore needs confirmation before treating it as exactly the same estimator as Table 4. The stated 24-month SDI also requires history preceding the twenty-two-month crisis-focused data description; the paper does not spell out that history's construction. Excluding 2008 or extending the broader sample with TASS through June 2009 reportedly leaves the main long-sample result similar, but the detailed outputs are not shown.

## What can be reconstructed and what still requires the authors' code

The source gives the main sample filters, strategy factor sets, regression-selection thresholds, SDI formula, four holding horizons, two-way sort order, and many numerical benchmarks. A researcher can implement a close variant and test the economic hypothesis. Exact reproduction still requires vendor snapshots and deduplication rules; the smoothing estimates and initialization; factor construction, particularly option and volatility returns; precise alignment of rolling alphas with formation/evaluation periods; historical availability of fund characteristics; the rebalance calendar; and how fund-level alphas are pooled and tested.

A stricter prospective experiment would freeze factor selection and smoothing parameters using past data, form every signal from information actually reported by the decision date, avoid future asset-threshold screening and backward interpolation, and explicitly model closed funds, notice periods, redemption restrictions, and missing liquidation returns. It would also use inference robust to overlapping estimated alphas and common fund shocks, and reserve a genuinely untouched evaluation period after choosing SDI. Those are improvements to the design, not procedures established by the paper's reported tables.

The paper's most useful result is that a simple peer-fit statistic adds information to historical alpha rankings over one to two years, but much less under the FH comparator and not in the crisis exercise. Distinctiveness is therefore a candidate manager-screening feature whose risks and data timing must be examined, rather than a universal quality score. The separation between probit significance, portfolio separation, raw returns, and implementable investor profit is central to using the findings responsibly.
