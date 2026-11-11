# Aggregate and Firm-Level Measures of Systemic Risk from a Structural Model of Default

**Alexander Reyngold, Ksenia Shnyra, and Roger M. Stein (2015).** *The Journal of Alternative Investments* 17(4), Spring, pp. 58–78. Source: [SystemicRisk_Reyngold_2015.pdf](../../Finance/SystemicRisk_Reyngold_2015.pdf). The PDF is scanned; the text and mathematical definitions were checked against page images. Its last two pages are journal contents/abstracts, not additional sections of this article.

## Why this matters

Equity-price co-movement can reveal common exposures, but equity risk is affected by leverage and may not map directly into common pressure on solvency. This paper proposes applying principal-component analysis to **implied firm asset returns** obtained from a structural credit model. The fraction of variation explained by the first component is the **credit-absorption ratio (CAR)**. Rising CAR is interpreted as concentration of financial firms' credit fundamentals around common drivers.

The paper also proposes firm-level exposure measures from first-component loadings. Its evidence is retrospective: regional CAR series and selected institution examples are aligned with the 2007–2009 crisis and its aftermath. There is no held-out crisis forecast, calibrated systemic-default probability, or structural estimate of contagion. The contribution is a monitoring framework that combines an economically motivated asset-value transformation with statistical concentration measures.

Two replication limits are fundamental. The empirical asset values use a proprietary vendor algorithm not disclosed here. In addition, the firm-loading definition in the equations is not numerically consistent with the scale of the displayed charts under ordinary unit-eigenvector normalization. Both need resolution before claiming an exact implementation.

## Structural credit motivation, with consistent notation

The paper motivates its approach using the Merton model. Let $A_t$ be the market value of firm assets, $D$ the **face value** of zero-coupon debt due after remaining horizon $\tau$, $E_t$ the market value of equity, $r$ the risk-free rate, and $\sigma_A$ asset volatility. Under the physical measure,

$$
\frac{dA_t}{A_t}=\mu_A\,dt+\sigma_A\,dW_t.
$$

Equity at maturity is $(A_T-D)^+$. In the elementary no-dividend Merton pricing model,

$$
E=A\Phi(d_1)-De^{-r\tau}\Phi(d_2),\qquad
d_1=\frac{\log(A/D)+(r+\tfrac12\sigma_A^2)\tau}{\sigma_A\sqrt\tau},\qquad
d_2=d_1-\sigma_A\sqrt\tau.
$$

Equity's asset delta is $\Phi(d_1)$, so its instantaneous volatility obeys

$$
\sigma_E=\frac{A}{E}\Phi(d_1)\sigma_A.
$$

Given $E,\sigma_E,D,r,\tau$, these equations can be solved jointly for $A$ and $\sigma_A$ under a specified calibration convention. A positive-variable numerical solver can work with log parameters; observed equity-volatility estimation and debt mapping must be supplied separately. This is a reconstruction of the elementary model, not the proprietary method used for the paper's numerical results.

The physical default probability under that elementary process is

$$
P(A_T\leq D)=\Phi\left(-\frac{\log(A/D)+(\mu_A-\tfrac12\sigma_A^2)\tau}{\sigma_A\sqrt\tau}\right).
$$

Replacing $\mu_A$ with $r$ gives the risk-neutral probability. These probabilities serve different purposes and should not be conflated.

The source's introductory formulas contain inconsistencies worth correcting explicitly. Its balance-sheet identity $A=D+E$ must use **market debt value** if $A$ and $E$ are market values; face debt used as an option strike is generally different. Its option-pricing $d_1$ uses physical drift $\mu_A$, inconsistent with the risk-neutral pricing PDE immediately preceding it. Its default-probability display includes an intermediate $\Phi(-d_1)$ expression, while the final drift-based expression is a distance-to-default calculation of the form above. These printed expressions cannot all be used as one internally consistent calibration system.

The actual study avoids fixing a complete elementary calibration algorithm, writing implied asset value generically as a function of observable equity, volatility, debt, and rates. Endnote 1 identifies a Vasicek–Kealhofer implementation with extensions for financial firms' service franchises as well as investment portfolios. Financial-statement inputs are public in principle, but access to the exact monthly implied-asset series and the vendor's stabilization and estimation procedures is not reproduced by the Merton equations alone.

## From absorption ratio to credit-absorption ratio

For a matrix of centered observations, PCA decomposes a symmetric covariance or correlation matrix into orthonormal eigenvectors and nonnegative eigenvalues $\lambda_1\geq\cdots\geq\lambda_m$. The ordinary absorption ratio retains a fixed number $k$ of components:

$$
AR_k=\frac{\sum_{j=1}^{k}\lambda_j}{\sum_{j=1}^{m}\lambda_j}.
$$

The reviewed Kritzman approach uses broad market or industry indices, roughly 500 daily observations, and $k\approx m/5$. This paper instead selects financial institutions, uses monthly implied **asset** returns, works with a 36-month rolling window, and retains only the first component.

The algorithm explicitly standardizes the estimated covariance matrix:

$$
R_t=D_t^{-1/2}\widehat\Sigma_tD_t^{-1/2},\qquad D_t=\operatorname{diag}(\widehat\Sigma_t).
$$

PCA is then performed on $R_t$, giving

$$
CAR_t=\frac{\lambda_{1,t}}{\sum_{j=1}^{m_t}\lambda_{j,t}}.
$$

For a valid unit-diagonal correlation matrix, the denominator is $m_t$, the number of firms actually included. Thus the operational measure is a fraction of **standardized-return variance**, rather than raw dollar-asset variance or the variance of an asset-value-weighted financial system. Rankings determine the selected cohort; they do not turn PCA into asset-size weighting.

A high CAR means one statistical direction explains much of the standardized co-movement. It does not say what that direction economically represents, how likely its adverse realization is, or whether firms are close to default. Correlations are unchanged by adding return means or scaling marginal volatility, so CAR alone discards substantial information relevant to default probability. Two systems can have identical CAR and very different capitalization or distance to default.

For intuition, an equal-correlation matrix of $m$ firms with positive pairwise correlation $\rho$ has $\lambda_1=1+(m-1)\rho$, so $CAR=\rho+(1-\rho)/m$. This is an illustrative algebraic consequence, not a fitted model in the article. It shows why CAR is a concentration indicator rather than a default probability. High common positive and negative movements can both increase co-movement; PCA does not impose an adverse sign.

## Data and cohort construction

The authors receive monthly implied asset values from Moody's Analytics and currency data from OANDA. The raw sample contains 9,611 financial firms with at least one observation from January 2002 through September 2012, spanning 129 months. Financial firms include banks, investment banks, insurers, and broker-dealers under the vendor's classification. Dropping firms with fewer than 30 nonmissing observations over the full sample leaves 7,756.

For each month, implied asset values are converted to US dollars for size comparison. Firms are ranked anew by contemporaneous asset size, and the largest 50 are selected separately for the US, Europe, and the world. This accommodates growing or shrinking firms rather than imposing a single end-of-sample top-50 list. Results for top-20 cohorts are described as similar but are not displayed in detail.

Selection uses contemporaneous rankings, but the full-sample 30-observation screen can still depend on future availability. The source does not list firms by date, specify every jurisdiction/region classification, explain parent/subsidiary consolidation, or give a tie policy. It also does not unambiguously state whether returns are formed in local currency before conversion for ranking or from converted asset values. Currency conversion solely for ranking and currency conversion before return calculation can produce different co-movements.

The global cohort overlaps the regional cohorts. Exhibit 9 describes a shift from approximately 60% European and 35% US firms initially toward approximately 50% European, 30% US, and 20% other-region firms. These are firm counts, not shares of asset value. Regional/global CAR differences therefore combine changing constituents with changing dependence; they are not independent regional experiments.

## Filtering and smoothing

The proposed asset return is monthly log change,

$$
r_{i,t}=\log\frac{A_{i,t}}{A_{i,t-1}}.
$$

The authors remove individual observations with an asset-return jump greater than 50%, retaining the rest of the firm's history. The explanatory example concerns an **increase** above 50%; it does not clearly specify an absolute-value filter that also removes equally large losses. Nor does it reconcile a “50%” cutoff with log-return units: $r>0.5$ and an arithmetic increase above 50%, $r>\log(1.5)$, differ. A replication must disclose this ambiguity rather than invent symmetric winsorization.

Next the asset-return series are smoothed with a backward-looking moving average before estimating dependence. The article emphasizes the direction of the average but does not clearly provide its window length in the algorithm. The explicit 12-month smoothing of **firm loadings**, described below, is a different operation and should not silently be reused as the asset-return smoothing length.

Within each trailing 36-month window, a firm must have at least 30 nonmissing observations to enter the calculation. An endnote reports similar results with thresholds of 15 or five, but more missing correlations. The source does not fully specify the pairwise/listwise covariance rule, imputation, handling of a newly selected firm, or whether ineligible top-50 firms are replaced with the next eligible firms. The actual matrix size can therefore differ from the nominal selected cohort size.

The stated interval $t-36,\ldots,t$ contains 37 monthly endpoints, whereas the prose calls the window 36 months. An implementation should define explicitly whether it uses 36 returns, 37 price levels, or another convention. The displayed CAR series begin around 2005, consistent with needing a multi-year initialization history from 2002. Repeated references to “September 31, 2012” are invalid calendar dates; the defensible source period is simply **through September 2012**.

## PCA does not require an invertible sample matrix

The paper expresses a preference for full-rank covariance so eigenvectors are orthogonal. A symmetric positive-semidefinite matrix admits orthonormal eigenvectors even when singular. With 50 variables and only 36 complete monthly return observations, a centered ordinary sample covariance has rank at most 35. Thus full column rank is impossible in that nominal design, but the leading eigenvalue ratio remains well defined when total variance is positive.

Missing data create a separate problem. A matrix assembled from pairwise correlations may be indefinite, even if each pair has many overlapping observations. A 30-of-36 availability screen alone does not prove positive semidefiniteness. The article gives no complete repair rule, minimum-eigenvalue diagnostics, or shrinkage specification. One should distinguish mathematically harmless zero eigenvalues in a valid sample matrix from negative eigenvalues caused by inconsistent covariance estimation.

Appendix A reviews PCA with $X'X=n\Sigma$ and an orthogonal transformation $Z=XQ$, yielding $\operatorname{Cov}(Z)=Q'\Sigma Q=\Lambda$. Its intermediate algebra includes an extra $1/n$ factor after substituting the covariance definition; the standard identity above is the consistent one. The factor does not change eigenvalue *ratios* if applied uniformly, but it matters for interpreting eigenvalues and loadings.

## A precise reconstruction of the aggregate algorithm

Given the unavailable vendor series or a separately disclosed replacement model, the reconstruction is:

1. Obtain dated asset values and the inputs/model version used to estimate them. Preserve the data vintage rather than assume revised values were historically available.
2. Form monthly log asset returns, with an explicit currency convention. Apply a documented interpretation of the jump filter and a disclosed trailing smoothing window.
3. At month $t$, rank financial firms by the required US-dollar asset values within each region, select the nominal cohort, and apply a stated eligibility/replacement policy.
4. Collect the defined trailing return window, enforce the minimum-observation rule, and estimate a valid covariance/correlation matrix using a declared missing-data method.
5. Sort eigenvalues in descending order and calculate the leading-eigenvalue share using the actual matrix dimension. Retain eigenvalues, eigenvectors, firm identities, and sample counts for diagnostics.
6. Roll forward monthly and separate changes due to cohort membership from changes in covariance where possible.

The last diagnostic is a useful extension, not an analysis reported by the authors. The paper supplies the broad algorithm but does not resolve enough input choices to guarantee exact numerical reproduction.

## Firm-level exposures and a normalization problem

The text defines the loading $\gamma_{i,t}$ as the $i$th element of the first eigenvector $q_{1,t}$, whose norm is one in Appendix A. It then averages its absolute value over twelve months:

$$
\widetilde\gamma_{i,t}=\frac{1}{12}\sum_{s=t-11}^{t}|\gamma_{i,s}|.
$$

Absolute values avoid arbitrary eigenvector sign flips. They also remove whether a firm moves with or against the component. If the first two eigenvalues are close, rotations or swaps of the leading direction can destabilize individual coordinates even if aggregate concentration changes little. The article does not report eigengaps, component alignment, or handling of firms leaving the cohort during the smoothing window.

The source interprets these elements as partial correlations controlling for other firms. That is not the ordinary meaning of eigenvector coordinates. For standardized returns and component score $z_1=Xq_1$, the **ordinary** correlation with variable $i$ is

$$
\operatorname{Corr}(X_i,z_1)=\sqrt{\lambda_1}\,q_{i1}.
$$

This differs from $q_{i1}$ and is not a partial correlation conditional on the other variables. It is a plausible alternative meaning of “loading,” but the paper does not explicitly adopt this normalization in its definition.

The distinction is numerically material. In a valid correlation matrix,

$$
1=R_{ii}=\sum_j\lambda_jq_{ij}^{2}\geq\lambda_1q_{i1}^{2},\qquad |q_{i1}|\leq\lambda_1^{-1/2}.
$$

For example, a 50-firm CAR of 0.6 implies $\lambda_1=30$ and bounds every unit-eigenvector element by about 0.183. The source's Dexia and Lloyds charts show smoothed “loadings” around 0.8–1.0 in high-CAR periods. Those cannot be interpreted as the defined raw unit-eigenvector elements under that matrix construction. Correlation-normalized loadings could have that scale, but silently replacing the formula would invent an undocumented implementation. Both the definition and scale discrepancy must remain visible.

Equation 11 further defines a scaled score $\widetilde\gamma^s_{i,t}=CAR_t\widetilde\gamma_{i,t}$. The authors interpret it as combining aggregate fragility with individual exposure. Neither factor is a calibrated event probability, so their product is not a probability that a firm defaults or experiences a systemic event. The charts show similar broad shapes for scaled and unscaled versions, with differences when CAR is low.

## Aggregate empirical evidence

Exhibits 1–4 align regional series with retrospective crisis events. Approximate chart levels, not machine-readable reported estimates, indicate the following patterns:

| Cohort | Reported/visible behavior | Interpretation supported by the design |
|---|---|---|
| Europe | Rises during 2005–2006 toward approximately 0.6–0.65, stays high into the crisis, and falls markedly during 2009–2010. | Common standardized asset-return variation increased before major public crisis events. |
| US | Falls toward roughly 0.2 around 2006–2007, then rises sharply toward approximately 0.5–0.55 around 2008–2009 and remains elevated afterward. | The timing of concentration differs from Europe. |
| Global | Rises during 2005–2006 toward approximately 0.5, exhibits a 2007 plateau, then declines after the crisis toward roughly 0.25. | A changing global cohort yields a different concentration path from either region. |

The authors relate European movements to lending growth and financial integration, and US movements to subprime losses and crisis events. European CAR visually resembles nonfinancial lending growth more than the US series resembles US commercial/industrial lending. These are proposed retrospective explanations. There is no estimated transmission model demonstrating that lending policy caused a CAR movement or that CAR caused later defaults.

Charts comparing CAR with median asset returns and a smoothed VIX show different trajectories. This establishes that the series are not identical; it does not establish incremental predictive value after controlling for their histories. The authors report Granger tests at 2, 3, 4, 5, 6, 9, and 12 months: no evidence from VIX to US CAR, some from US CAR to VIX near six months, and short-horizon bidirectional precedence between US asset returns and CAR. Full specifications, coefficients, test statistics, sample counts, and multiple-lag corrections are not shown. The paper correctly cautions that Granger precedence is not structural causation.

Historical comparisons with the original absorption ratio suggest an earlier CAR rise in this crisis sample. The comparisons change assets, frequency, window length, standardization, and number of retained components together. They therefore cannot isolate the benefit of the structural asset transformation or prove its superiority to an otherwise matched equity-return measure.

## Selected institution examples

The authors choose Freddie Mac, Dexia, and Lloyds to illustrate firm-level exposure paths. They acknowledge that other firms were harder to interpret and that a systematic evaluation is needed. No rule for selecting examples, all-firm outcome table, false-positive rate, or survival analysis is supplied.

Freddie Mac's plotted score rises from low levels during 2006–2007, peaks again around 2009, falls below roughly 0.1 around 2011, and turns upward in 2012. Dexia's score rises from around 0.5 in 2005 to near 1 by 2007 and remains high into 2009. Lloyds rises from roughly 0.4 to around 0.8 before/through the crisis, falls around 2009–2010, then rises again toward 2012. These are chart-scale descriptions, subject to the normalization problem above; they are not default probabilities.

The authors connect the paths to mortgage exposures, sovereign debt, public support, restructuring, and later portfolio problems. Those narratives are background drawn from contemporaneous reporting, not separately estimated effects. Some numerical prose does not match its charts: Dexia is described as eventually approaching zero, while the displayed unscaled curve ends near 0.45; Lloyds is described as falling below 0.2, while the unscaled chart's trough is around 0.38. Scaling, different series, or another explanation may reconcile them, but none is documented clearly. Precise event chronology and public-support figures in the narratives also need independent source checking before using them to calculate warning lead times.

The supported result is that selected revised-data score paths rose before or during several institutions' difficulties. It is not a demonstrated real-time ranking of all institutions' future losses or systemic contributions.

## Sensitivity and limits

Exhibit 10 retains two through five components. The cumulative share necessarily rises when additional nonnegative eigenvalues are included. The regional curves preserve much of their broad shape, while the global curve becomes flatter, already noticeably so at two components. The authors retain one because they want a sensitive common-factor concentration measure within finance, not because an independent forecast test selects it.

A genuine risk can spread across two similarly important components. In that case first-component CAR can fall even though concentration in the leading two components remains high. The source explicitly recognizes this failure mode. A leading eigenvalue share alone cannot distinguish disappearance of common risk from redistribution across several common directions.

The data limitations are unusually consequential. The authors acknowledge financial-statement restatements, reportedly affecting less than 0.6% of observations, and an early methodology revision that caused asset values to be recalculated for the **entire** history. Trailing smoothing avoids direct use of future return observations, but does not make revised historical inputs point-in-time. Consequently the retrospective warning patterns cannot be assumed available to a contemporary analyst.

The evidence covers only about a decade, dominated by one interconnected crisis episode. No confidence bands for CAR, sampling uncertainty for firm scores, formal crisis-prediction accuracy, or independent crisis validation is supplied. Fifty variables estimated from a heavily smoothed 36-month window yield substantial estimation and dependence issues, particularly with changing membership. CAR observes co-movement rather than actual bilateral counterparty exposures, common holdings, margin calls, or liquidity capacity. Solvency-related interpretation may transfer poorly to a crisis driven primarily by other constraints.

The framework is reconstructible as a class of monitoring measures: infer asset values under a disclosed model, build a valid rolling correlation matrix, and track its leading variance share and clearly normalized firm loadings. Exact reproduction of the supplied study requires the vendor's data vintage and algorithm, smoothing length, filtering and covariance conventions, dated cohorts, and a correction to the loading definition/scale. Without those inputs, a new implementation should be presented as a transparent variant rather than as the exact published CAR series.
