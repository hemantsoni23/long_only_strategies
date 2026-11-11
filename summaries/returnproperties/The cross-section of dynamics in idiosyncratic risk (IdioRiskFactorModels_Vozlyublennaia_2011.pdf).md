# The cross-section of dynamics in idiosyncratic risk

**Nadia Vozlyublennaia. Journal of Empirical Finance 18 (2011), 461–473. DOI: 10.1016/j.jempfin.2011.03.001.** Source: [original PDF](../../Finance/IdioRiskFactorModels_Vozlyublennaia_2011.pdf), 13 pages. This note distinguishes the article's empirical findings from several inconsistencies in its tables, prose, and inference formulas. The main object called idiosyncratic risk is a **residual variance**, not a residual standard deviation.

## Why this matters and what the paper contributes

A rising average idiosyncratic variance does not mean that a typical individual firm's risk increases steadily throughout its life. An average can change because the identities and weights of listed companies change, because a subset of firms becomes much riskier, or because many persistent but nontrending individual processes happen to move together. These explanations imply different models for forecasting security-specific risk.

Vozlyublennaia shifts attention from a market-level average to the cross-section of individual firms' risk dynamics. The paper asks how many firms have increasing, decreasing, or statistically insignificant trends; how those classifications relate to changes in earnings, leverage, institutional ownership, size, and prices; and whether apparent trends represent deterministic drift, unit roots, or fractional persistence. Its distinctive empirical result is heterogeneity: substantial groups move in opposite directions, and the majority of apparent ordinary least squares trends do not survive a more persistence-robust trend test.

The characteristics regressions are historical associations constructed from firms' observed lives. They are not a real-time forecasting system. Both the response classification and explanatory characteristic trends generally use information from the full sample available for each firm. The paper supplies no portfolio backtest, risk-forecast holdout, transaction-cost calculation, or causal instrument for changes in institutional ownership.

## Universe and monthly measurement of risk

The core data are CRSP daily stock returns for NYSE, AMEX, and NASDAQ securities from July 1963 through December 2005. The sample contains 21,860 companies with at least two years of monthly risk observations. A firm-month requires at least ten daily return observations. Firm characteristics come from quarterly Compustat and institutional holdings from 13F data; inflation adjustments use the CPI. The article does not provide all share-code filters, delisting treatments, database vintages, or exact security-to-accounting links needed to rebuild the sample count mechanically.

For each stock $i$ in each month $m$, estimate a separate daily Fama–French three-factor regression with an intercept:

$$
r_{i,d}^{m}-r_{f,d}^{m}
=\alpha_i^m+\beta_{i,M}^m(r_{M,d}^{m}-r_{f,d}^{m})
+\beta_{i,S}^m SMB_d^m+\beta_{i,H}^m HML_d^m+e_{i,d}^m.
$$

Then define

$$
IR_i^m=\frac{1}{T_{im}}\sum_{d=1}^{T_{im}}(\widehat e_{i,d}^m)^2.
$$

Equations (1)–(2), p. 463, are explicit about dividing by $T_{im}$, not by residual degrees of freedom. The statistic is not square-rooted or annualized. If returns are recorded as decimals, its units are squared daily decimal returns; changing to percentage returns multiplies the variance by 10,000. The within-month intercept already centers the residuals, subject to estimation precision.

This measurement carries substantial sampling error when only ten to twenty daily observations estimate four coefficients. Relative to a degrees-of-freedom-corrected residual variance, the expected small-sample scaling changes with the month's observation count. The paper does not model that measurement error in the later trend or logit stages. A faithful replication should preserve its definition before experimenting with alternative estimators.

The author reports qualitatively similar, untabulated results with CAPM residuals and a four-factor model including momentum. Quarterly estimation is another robustness check. A comparison of equal-weighted and value-weighted squared-error implementations gives trend t-statistic correlation 99.82%, but the weighting convention is not documented sufficiently to reconstruct this alternative exactly. A high correlation of statistics does not itself establish identical classifications at a significance threshold.

## Individual trend classification

Over the observed life of each security, estimate

$$
IR_{it}=a_{0i}+a_{1i}t+v_{it}.
$$

Define $D_i^{IR}=+1$ for a positive slope significant at 5%, $-1$ for a negative significant slope, and zero otherwise. A zero classification means failure to reject a linear trend, not proof that the risk series is constant. The procedure's power depends on sample length, variance of the residual-variance estimate, and serial dependence. Securities with short and long lives therefore do not face identical statistical detection conditions.

The baseline uses ordinary least squares trend statistics. Newey–West standard errors are checked, and their t-statistics have correlation 97.36% with ordinary least squares t-statistics. The bandwidth and complete threshold-crossing comparison are not reported. The stronger persistence analysis in Section 6 is important precisely because ordinary or short-memory-robust inference can misinterpret long-lived stochastic movements as deterministic trends.

Table 2 reports:

| Window | Number of firms | Increasing | Decreasing | Insignificant |
|---|---:|---:|---:|---:|
| July 1963–December 2005 | 21,860 | 30.92% | 25.38% | 43.70% |
| July 1963–December 1997 | 17,379 | 31.30% | 21.40% | 47.30% |
| January 1998–December 2005 | 9,769 | 12.21% | 46.28% | 41.51% |
| July 1963–December 1975 | 5,747 | 39.29% | 6.32% | 54.39% |
| January 1976–December 1985 | 7,827 | 21.43% | 19.85% | 58.72% |
| January 1986–December 1995 | 10,762 | 31.04% | 18.47% | 50.49% |
| January 1996–December 2005 | 11,700 | 20.38% | 33.00% | 46.62% |

The full-period counts are 6,759 increasing, 5,548 decreasing, and 9,553 insignificant. Subsample counts overlap; adding them does not recover the full universe. The table defines the post-CLMX interval as 1998–2005, although nearby prose refers inconsistently to 1997 or a split at 2001. A replication should use the explicit table dates and record that choice.

Two-year rolling versions show large time variation in the proportions (Figure 1). Figure 2's ratio of rising to falling counts is particularly unstable early in the sample, with a peak above eight; the prose's description of relative constancy should not be interpreted literally. A ratio also becomes unstable mechanically when its denominator is small.

The paper uses candidate break years from earlier literature, including 1966, 1987, 1999, 2001, and 2003. It reports trend classifications for intervals excluding break years, notably 1963–1965, 1967–1986, and 1988–1998; short later intervals are omitted. These are externally motivated subsamples rather than an estimated endogenous break model. The first table label begins in January 1963 despite the stated data beginning in July.

Including seasonally adjusted real GDP in the trend regression changes the full-sample proportions to 14.95% increasing, 22.37% decreasing, and 62.68% insignificant. Adding a time-by-GDP interaction yields positive significant interaction coefficients for 17.84% and negative ones for 33.30%. The time coefficient is then conditional on the GDP level, not an unconditional constant slope. The source does not explain how quarterly GDP is aligned or interpolated to the monthly risk observations, or how real-time revisions are handled.

## Listing composition experiment and its limitation

Section 3.2 tries to distinguish within-firm risk changes from changes in market membership. For each stock classified as having a significant positive or negative trend, replace its risk at all later dates by its initial risk. Stocks with insignificant trends retain their observed risk series. Compute a market average of this modified panel and compare it with the ordinary average; Figure 3 displays their divergence, especially after 1988.

Formally, if $\mathcal S_t$ is the listed universe and $w_{it}$ its averaging weights, the modified input is

$$
\widetilde{IR}_{it}=
\begin{cases}
IR_{i,0},&D_i^{IR}\ne0,\\
IR_{it},&D_i^{IR}=0,
\end{cases}
\qquad
\widetilde{IR}_t=\sum_{i\in\mathcal S_t}w_{it}\widetilde{IR}_{it}.
$$

The exact averaging-weight and initial-valid-month rules need clarification from the original code. More fundamentally, the modified series is not a pure listing-composition series: firms classified as insignificant still fluctuate, and changing weights can contribute if weights are not fixed. Significance classification itself uses future observations relative to early dates. The exercise is a hindsight counterfactual, not an investment signal.

There is also a numerical interpretation error in the article. Page 468 says the modified average's slope is approximately 30% of the ordinary average's slope, then attributes 70% to new listings and 30% to existing firms. Under the idealized interpretation that the modified average isolates composition, those percentages would run the other way. Because the actual procedure freezes only selected firms, even reversing the percentages would not yield a clean additive economic decomposition. The defensible conclusion is that within-firm movements materially affect the market average; the stated 70/30 attribution is not supported unambiguously by the described calculation.

## Characteristics and their trend variables

The characteristics analysis applies a similar time-trend regression to each firm's accounting or market variable, producing two indicators per characteristic: a significantly positive trend and a significantly negative trend. A nonsignificant trend is the omitted category. Table 3 requires at least two consecutive years of monthly risk and quarterly characteristic observations. Complete-case counts vary substantially across characteristics and specifications.

The source's principal definitions are:

- Size is the logarithm of equity market value, with inflation adjustment; price is also inflation adjusted.
- Book equity starts with Compustat item 60 when available, otherwise item 59 plus item 55, otherwise item 44 minus item 54, in that order; add deferred taxes (item 52) and subtract preferred equity (item 55) from the selected base. Book-to-market divides this quantity by equity market value.
- The cash ratio is cash divided by total assets. Leverage is long-term debt divided by assets in the main data description; Table 1's caption instead refers to market value of assets, leaving a definition discrepancy.
- Earnings per share is earnings divided by shares. Earnings variability is a rolling five-year **sample variance**, despite being called volatility; observation requirements and the precise treatment of quarterly histories are not fully supplied.
- Institutional ownership is the fraction held by institutions in 13F data. R&D is scaled by equity market value. Turnover is intended to measure trading relative to listed shares, but its exact aggregation and denominator implementation are not fully specified.

The Compustat item references in Section 2 identify common equity as item 60, cash as 36, total assets as 44, long-term debt as 51, deferred taxes as 52, and preferred equity as 55. Data-frequency alignment, fiscal versus calendar quarters, reporting lags, and restatement vintages remain important missing inputs. The regressions do not claim that quarter-end accounting values were available to trade immediately.

Some descriptive entries in Table 1 are plainly inconsistent: the cash-ratio row gives mean 0.68, standard deviation zero, and both minimum and maximum 4.98. Its blanket statement that almost all characteristics are in millions of dollars also cannot apply to dimensionless ratios or logged size. Those values should not be used as cleaning thresholds or calibration targets.

Table 3 correlations between the signed trend class of risk and that of each characteristic are −0.217 for earnings per share, 0.068 for earnings variability, 0.132 for book-to-market, −0.207 for turnover, 0.119 for cash ratio, −0.300 for institutional ownership, −0.134 for excess return, −0.329 for real price, 0.115 for leverage, 0.127 for R&D, and −0.359 for size. Reported p-values are below 0.0001, but the effective samples differ: institutional ownership has 6,873 firms, R&D 2,766, and several return-based variables approximately 17,173. These are correlations of coarse significance categories, not correlations between the underlying continuous economic variables.

## Multinomial model and interpretation

Let $X_i$ contain all positive- and negative-trend characteristic indicators. The multinomial logit with no significant risk trend as the baseline is

$$
\eta_i^+=b_0^++X_i'b^+,
\qquad
\eta_i^-=b_0^-+X_i'b^-,
$$

$$
p_i^+=\frac{e^{\eta_i^+}}{1+e^{\eta_i^+}+e^{\eta_i^-}},\qquad
p_i^-=\frac{e^{\eta_i^-}}{1+e^{\eta_i^+}+e^{\eta_i^-}},\qquad
p_i^0=\frac{1}{1+e^{\eta_i^+}+e^{\eta_i^-}}.
$$

Estimate the common cross-sectional coefficients by maximizing $\sum_i\sum_{c\in\{+,0,-\}}1\{D_i^{IR}=c\}\log p_i^c$. The superscripts attached to coefficients in the source should not be interpreted as a separate estimable logit coefficient vector for every firm. The observation is the firm, whose lifetime risk and characteristic trends have already been estimated in stage one.

A coefficient $b$ changes the relevant category's odds relative to the insignificant category by $e^b$. It is not a percentage-point probability change. Because both logits can change, even a coefficient's sign alone is not always the sign of the absolute category-probability change. The source's broad language about probabilities is therefore more accurately expressed as relative odds unless all relevant coefficients are considered.

Table 4's first displayed specification gives the following selected coefficients and heteroskedasticity-robust standard errors:

| Characteristic trend indicator | Rising risk versus insignificant | Falling risk versus insignificant |
|---|---:|---:|
| Earnings per share rising | −0.295 (0.055) | 0.210 (0.055) |
| Earnings per share falling | 0.362 (0.062) | −0.451 (0.077) |
| Earnings variance rising | 0.409 (0.051) | −0.683 (0.055) |
| Cash ratio rising | 0.201 (0.063) | −0.192 (0.069) |
| Institutional ownership rising | −0.216 (0.057) | 0.556 (0.054) |
| Institutional ownership falling | 0.449 (0.082) | −0.114 (0.114) |
| Leverage rising | 0.229 (0.056) | −0.376 (0.060) |
| Size falling | 0.805 (0.061) | −0.258 (0.085) |
| Turnover rising | −0.040 (0.052) | 0.794 (0.060) |
| Real price rising | −0.578 (0.084) | 0.439 (0.061) |
| Real price falling | 0.720 (0.062) | −0.286 (0.057) |

For example, a falling size trend is associated with approximately $e^{0.805}=2.24$ times the odds of rising rather than insignificant risk, holding the other indicators fixed. Rising institutional ownership has odds multipliers of approximately 0.806 and 1.744 for the rising and falling categories respectively. These are derived transformations of reported coefficients, not new estimates.

The general pattern links deteriorating earnings, shrinking size, falling prices, and reduced institutional participation with rising idiosyncratic variance. But shared full-period trends, simultaneous determination, omitted firm conditions, and generated classification error prevent a causal interpretation. The robust standard errors do not propagate uncertainty from the first-stage trend estimates; no bootstrap of both stages or industry-cluster design is supplied.

The turnover interpretation in the prose is reversed relative to Table 4: its positive 0.794 coefficient raises the odds of **falling** risk relative to no significant trend. It does not support the sentence saying that increasing turnover makes declining risk less likely. The rising-risk turnover coefficient is small and insignificant. This discrepancy should be retained as a source limitation rather than silently repeating the verbal claim.

## Robustness, changing samples, and initial conditions

The high-price group contains securities whose inflation-adjusted price exceeds \$5 in at least 70% of observations; the others are the low-price group. This is a full-history classification, not a current-price sort. The author finds many relations similar across these groups and after omitting price or turnover indicators individually. Separate R&D specifications have different coverage and should not be compared as though all estimates used the same companies.

Table 5 also splits the CLMX and post-CLMX periods, firms listed by 1998 versus later entrants, and shorter versus longer observed lives. Exact cutoffs for the lifetime split are not sufficiently specified. Temporal robustness is weaker than a blanket stability claim would suggest. For example, the falling-risk coefficient on rising institutional ownership is 0.302 in the CLMX subsample but −0.988 in the post-CLMX subsample. Earnings and size effects also change. These differences may reflect structural change, smaller samples, or power and selection changes; the source does not isolate which.

Section 5 asks whether initial risk predicts the subsequent trend classification. The reported binary-logit slopes on initial $IR$ are −83.232, standard error 8.64, for rising risk and 58.344, standard error 5.97, for falling risk; the intercepts are −0.715 and −1.152. The displayed equations misleadingly put a binary dummy on the left. In a logit interpretation the left side is log odds, not the realized zero–one outcome. The baseline is a nonsignificant trend; treatment of opposite-sign observations in each binary regression is not fully specified, although a multinomial robustness check is reported.

Lower starting risk is associated with subsequent increases and higher starting risk with subsequent decreases. This fits mean reversion, but using the initial observation both to measure starting risk and to help estimate its subsequent slope also creates mechanical dependence. Measurement error and regression to the mean are alternative explanations to an economic selection story. Coefficient magnitudes cannot be transported across different variance units.

Annual delisting logits are also estimated, with next-period delisting as the outcome and risk as a predictor. Their coefficient series are only described, not tabulated. The author finds no convincing evidence for changing market tolerance of risk. Without the series, uncertainty, delisting-type controls, or a clear mapping from acquisition and failure exits to investor preferences, this is a limited diagnostic rather than an identified test of risk tolerance.

## Deterministic trends versus stochastic persistence

The final analysis restricts to 8,578 stocks with at least ten consecutive years of monthly risk observations. This longer-lived sample is materially different from the original 21,860-firm panel. It applies the Vogelsang PS1 trend test, intended to be robust to stationary or integrated disturbances, and augmented Dickey–Fuller tests with and without a trend. The ADF specification uses four lags; two-lag results are said to be similar.

The source's equations (6)–(7) display a trend and lagged dependent variable with a serially dependent error. They do not specify enough of the PS1 construction, tuning, or critical-value implementation to rebuild the statistic from these equations alone. A replication must obtain the cited test procedure and document its exact implementation. Rejecting a zero deterministic trend is different from estimating a significant slope under ordinary least squares.

Table 6 makes that distinction quantitative. Ordinary least squares classifies 2,893 firms as increasing, 2,596 as decreasing, and 3,089 as insignificant in this long-history sample. The persistence-robust test instead identifies 448 positive trends (5.22%), 635 negative trends (7.40%), and 7,495 insignificant trends (87.38%). Of the 2,893 ordinary positive classifications, only 445 remain positive under PS1; of the 2,596 negative classifications, 628 remain negative. The source prose's 28.54% and 22.94% figures describe individual off-diagonal cells, not the complete ordinary-trend totals.

The unit-root columns report 128 stocks, 1.50%, without a deterministic trend and 96, 1.12%, with one. ADF tests have a unit-root null: a nonrejection cannot establish that a unit root is present, and a small nonrejection fraction is not a proof that all other series are simple short-memory processes. The article's phrase “significant unit root” is statistically imprecise. Power, structural changes, and fractional integration remain relevant alternatives.

## Long-memory exercise and an inference correction

Because fitting required individual attention to starting values and convergence, long-memory estimation is reported for only ten randomly selected stocks, one from each size decile. Their identifiers, seed, and full optimization settings are absent. This small exercise cannot establish the prevalence of long memory across the original universe.

The parametric model is ARFIMA(12,$d$,0), which can be written

$$
\Phi_{12}(L)(1-L)^d(IR_t-\mu)=\varepsilon_t.
$$

Maximum likelihood estimates are compared with local Whittle estimates using bandwidths $m=T^k$, with $k=0.5,0.6,0.75,0.8$. A standard local Whittle reconstruction minimizes

$$
Q(d)=\log\!\left[\frac1m\sum_{j=1}^{m}\omega_j^{2d}I(\omega_j)\right]
-\frac{2d}{m}\sum_{j=1}^{m}\log\omega_j,
\qquad \omega_j=\frac{2\pi j}{T},
$$

where $I$ is the periodogram. The original article names the estimator but does not give this objective, bandwidth rounding, detrending, optimization bounds, or initialization. These specifications therefore describe an explicit conventional implementation, not recovered original code.

Under the usual local Whittle asymptotic assumptions, $\sqrt m(\widehat d-d)$ has variance $1/4$, giving standard error $1/(2\sqrt m)$. Footnote 25 instead prints variance $4/m$ and standard error $2/\sqrt m$, four times the conventional standard error. Table 7's numbers are consistent with that inflated formula. This correction is independently corroborated by the implementation paper [Baum, Hurn, and Lindsay, “Local Whittle estimation of the long-memory parameter”](https://journals.sagepub.com/doi/10.1177/1536867X20953569), Section 2. The applicable asymptotic assumptions still need checking, particularly outside the stationary range; one should not simply replace reported p-values mechanically.

The ten sample lengths range from 121 to 396 months. Maximum likelihood estimates of $d$ include 0.893 (standard error 0.341), 0.082 (0.202), 0.723 (0.303), 0.900 (0.156), and 0.385 (0.141). With bandwidth $T^{0.8}$, the ten local Whittle estimates range from 0.283 to 0.573. Estimates can be very sensitive: security 2 has maximum-likelihood $d=0.082$, but local Whittle $d=0.987$ at bandwidth $T^{0.5}$ and 0.435 at $T^{0.8}$.

For $0<d<1/2$, fractional integration gives covariance-stationary long memory; for $1/2\le d<1$, the process is nonstationary but can remain mean reverting in the usual fractional sense. The paper groups the entire interval $(0,1)$ under long memory. Failure to reject $d=0$ or $d=1$ at a stricter significance level does not demonstrate that the process is stationary or has a unit root. Given the small selected sample, convergence difficulties, bandwidth sensitivity, and standard-error discrepancy, the evidence is suggestive of persistence rather than a calibrated model-selection result.

## Reimplementation boundary and takeaway

The core empirical pipeline is reproducible in structure: build within-month residual variances; estimate lifetime and rolling trend classes; merge explicitly timed firm characteristics; classify their trends; estimate multinomial relative odds; then repeat trend and persistence tests on the long-history subset. Preserve variance units, the minimum daily and monthly counts, table-specific samples, and the distinction between a statistical nonsignificance category and no economic change.

Exact replication requires additional information on security filters, daily risk-free conversion, factor vintages, missing histories, quarterly alignment, characteristic formulas, institutional coverage, weighting of market averages, Newey–West tuning, complete-case logit counts, PS1 implementation, and the identities and settings of the ten long-memory series. The source's composition percentages, turnover prose, some descriptive cells, and local Whittle uncertainty should not be adopted uncritically.

The most useful finding is that individual risk histories contain heterogeneous, persistent rises and falls that a market average hides. The substantially smaller number of robust deterministic trends argues for modeling persistence and firm heterogeneity before extrapolating linear trends indefinitely. The characteristics associations may guide model design, but converting them into a forecasting or portfolio claim requires a separate, strictly historical training-and-validation experiment that the paper does not provide.
