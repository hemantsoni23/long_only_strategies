# How Useful Are Aggregate Measures of Systemic Risk?

**Harry Mamaysky (2016).** *The Journal of Alternative Investments*, Spring, pp. 13–32. Source: [SystemicRisk_Mamaysky_2016.pdf](../../Finance/SystemicRisk_Mamaysky_2016.pdf). References below use the article's equations and exhibits. The final PDF page is a reproduction notice, with no additional research content.

## Why this matters

An indicator that rises during a famous crisis may simply repackage information already visible in market prices. Mamaysky proposes evaluating systemic-risk indicators by their **incremental** ability to predict changes in VIX and US unemployment after controlling for current and lagged VIX, investment-grade credit spreads, and, for unemployment, its own history. This replaces a search for an indicator that anticipated one exceptional crisis with regressions on more frequently varying stress outcomes.

The novel constructive result is the **tail proportion**: the fraction of individual firms whose conditional tail-loss measures exceed a fixed threshold. It outperforms cross-sectional averages in the reported tests, particularly for financial firms. These tests are in sample and use simplified versions of established indicators. They do not demonstrate reliable real-time crisis warnings or establish that the original, fully specified measures are useless.

## Data, universe construction, and information timing

All data come from Bloomberg. Two global stock universes are used:

| Universe | Number of firms | Selection rule |
|---|---:|---|
| FINS | 103 | Financial-sector firms with capitalization above USD 30 billion on October 7, 2014, **or** above USD 21 billion on January 1, 2000. Sector membership uses 2014 ICB or 2000 GICS classifications. |
| GLOBALS | 174 | Firms of any sector above USD 75 billion on October 7, 2014, **or** above USD 53 billion on January 1, 2000. |

The older thresholds approximately deflate the later ones using a stated 2.4% average CPI rate over 14.5 years. These are unions of historical snapshots, not a point-in-time investable universe updated each date. In particular, a 2014 capitalization rule can introduce future-dependent selection into earlier observations. The source does not provide a complete security list, treatment of mergers/delistings, share-class selection, or security-level identifiers sufficient to rebuild the exact panels.

Capitalization distributions as of December 18, 2015 are geographically concentrated. US firms account for 42.9% of FINS capitalization and 56.7% of GLOBALS; China accounts for 18.4% and 8.8%, respectively. Those percentages describe the universes, not weights assigned to the equal-weighted indicator aggregates.

Stock and associated index returns are **overlapping five-business-day returns in local currency**. Each stock is mapped to the country index of its exchange of listing. Exhibit 4 gives the full mapping, including S&P 500 for the US, FTSE 100 for the UK, Shanghai Composite for China, Nikkei 225 for Japan, DAX for Germany, Hang Seng for Hong Kong, KOSPI/KRX 100 for South Korea, and Taiwan's index for Taiwan. The other listed mappings cover Russia, Mexico, Brazil, India, Spain, France, Switzerland, Italy, Australia, Canada, Belgium, Saudi Arabia, Singapore, Netherlands, Denmark, Sweden, Norway, Qatar, and Ireland. Listing country rather than incorporation determines the conditional market return.

The credit control is Bloomberg's generic, on-the-run five-year Markit CDX North America Investment Grade spread, in basis points. The VIX is the standard index. Unemployment is the BLS seasonally adjusted total unemployment rate. Predictive regressions run from November 2004, when the CDX series begins, through December 2015. Earlier observations are needed to initialize the rolling indicators.

The paper does not specify simple versus logarithmic return construction, dividend/corporate-action adjustments, precise close synchronization, monthly sampling of daily controls, unemployment release delays, or use of unrevised historical vintages. Local-currency weekly returns reduce some asynchronous-close problems but do not eliminate them. Real-time forecasting would need explicit release-calendar and vintage handling; contemporaneous reference-month unemployment is not necessarily known on the date a forecast is made.

## Common estimation choices

Exhibit 5 fixes the following settings:

| Indicator family | Return horizon | Rolling calculation window | Tail probability | Loss threshold | Additional setting |
|---|---:|---:|---:|---:|---|
| MES, CoVaR-like, CoRisk | 5 business days | 125 business days | 10% | 3% | Cross-sectional aggregation as defined below |
| Absorption ratio | 5 business days | 500 business days | — | — | Top 10 principal components |
| Turbulence | 5 business days | 750 business days | — | — | Average of 21 recent daily calculations |

The 125 observations are overlapping weekly returns, so they are not 125 independent weekly shocks. A 10% empirical tail uses roughly a dozen observations before considering overlap and missing data. The source does not specify quantile interpolation, ties, minimum tail counts, or every missing-data rule for the tail measures.

For the covariance-based indicators, the article first drops dates with fewer than 25% of observations available, then drops securities missing more than 10% of observations on retained dates. Within each rolling covariance window it uses only dates with a complete return vector. This seeks stable security composition. Exact prefilter sample boundaries and resulting retained counts are not provided; applying availability filters over the full history also differs from an online rule.

## Indicator definitions: preserve the direction of conditioning

Let $r_i$ be stock $i$'s weekly return, $I_i$ its associated country-index weekly return, and $Q^i_{0.10}$ and $Q^{I_i}_{0.10}$ their empirical tenth percentiles over the prior 125 business days. Conditional means below use that same window.

**MES** asks how a firm performs when its market is distressed:

$$
MES_i(t)=-\widehat E_t[r_i\mid I_i<Q^{I_i}_{0.10}].
$$

**The CoVaR-like measure** reverses the conditioning direction:

$$
CoVaR_i(t)=-\widehat E_t[I_i\mid r_i<Q^i_{0.10}].
$$

The second expression is a conditional **mean**, not a value-at-risk quantile and not necessarily the original CoVaR or delta-CoVaR. The author explicitly acknowledges the naming compromise. These simplified measures aim to retain conditioning direction while making inputs comparable across indicators. Conclusions about them cannot automatically be transferred to all original implementations.

**CoRisk** measures conditional stock-to-stock losses:

$$
CoRisk_{j\mid i}(t)=-\widehat E_t[r_j\mid r_i<Q^i_{0.10}],\quad i\ne j.
$$

Create a directed edge $i\to j$ when this conditional expected loss exceeds $\theta=0.03$. Aggregate network density is

$$
CoRisk(t)=\frac{1}{N(N-1)}\sum_{i=1}^{N}\sum_{j\ne i}\mathbf1\{CoRisk_{j\mid i}(t)>0.03\}.
$$

An edge is therefore a thresholded conditional-loss relationship, not proof that firm $i$ causally transmits a shock to $j$. Common shocks can generate both directions. The article repeatedly uses causal language for directions of conditioning; statistical conditionality alone does not identify intervention effects.

The paper also describes a quantile-regression alternative. Regress the $p$th return quantile of $j$ on $i$'s return, obtain $\widehat a_p,\widehat b_p$, and calculate

$$
-\{\widehat a_p+\widehat b_pQ^i_p-Q^j_p\}.
$$

This compares the predicted conditional quantile at a distressed $i$ with $j$'s unconditional quantile. The author says the qualitative results are largely unchanged, but does not display the alternative tables. Those claims are reported robustness statements, not independently inspectable numerical results in this PDF.

## Aggregation: average, dispersion, and tail proportion

For MES and the CoVaR-like measure, the article compares the equal-weighted cross-sectional mean, cross-sectional standard deviation, and proportion above 3%. For MES,

$$
MES(t)=\frac{1}{N}\sum_iMES_i(t),\qquad
MES_{PT}(t)=\frac{1}{N}\sum_i\mathbf1\{MES_i(t)>0.03\}.
$$

The SD version is the standard deviation across firm-level measures on that date. Analogous definitions apply to CoVaR. These yield six measures, plus CoRisk, absorption ratio, and turbulence: **nine indicators** in total.

Tail proportion is a bounded breadth statistic: the share of firms with estimated conditional average weekly losses exceeding 3%. It is not the share of stocks that actually lost 3% today, a 3% probability threshold, or an empirical daily default frequency. A rising fraction can reveal broadening exposure while the cross-sectional mean changes modestly.

The source motivates tail proportion as sensitivity to dispersion or outliers. That interpretation is not a general mathematical identity: the fraction above a fixed threshold can change with the mean, dispersion, or shape of the cross section, and dispersion changes need not raise the fraction at every threshold. The measure also discards severity beyond 3%. A firm at 3.1% and one at 20% both contribute one.

The threshold is described as arbitrary, with optimal calibration left for future work. Applying the same 3% threshold to a conditional index loss and a conditional single-stock loss does not impose equal economic stringency, because stocks are generally more volatile. This is one possible reason MES tail proportion performs better than CoVaR tail proportion. The source supplies no independent threshold-selection sample or a broad published sensitivity grid.

## Covariance-based measures

For a covariance matrix with eigenvalues $\lambda_1\geq\cdots\geq\lambda_N\geq0$, the absorption ratio is

$$
AR(t)=\frac{\sum_{a=1}^{10}\lambda_a(t)}{\sum_{a=1}^{N}\lambda_a(t)}.
$$

It measures the share of total return variance explained by ten principal components, using a 500-business-day window. It lies between zero and one when total variance is positive. The article says its denominator differs from an asset-variance denominator in the original methodology. For a complete ordinary covariance decomposition, however, the sum of all eigenvalues equals the trace, which is also the sum of individual asset variances. That substitution alone is algebraically equivalent, not a new boundedness property. Missing-data handling or other implementation changes may still matter.

Turbulence averages 21 squared Mahalanobis distances:

$$
T(t)=\frac{1}{21}\sum_{s=t-20}^{t}(r_s-\mu_s)'\Sigma_s^{-1}(r_s-\mu_s).
$$

At each $s$, the mean and covariance use a 750-business-day window of weekly return vectors; $r_s$ is the final observation associated with that calculation. This is squared distance, with neither a square root nor an explicit division by the number of securities. The 21-day smoothing is an additional choice intended to reduce noise compared with an unsmoothed series. The source does not specify treatment of singular matrices or covariance regularization.

Equation 2's printed turbulence expression uses $r(t)$ in its right-hand vector while its left-hand vector uses $r(s)$. The surrounding explanation describes the return at each successive window endpoint, supporting the symmetric squared-distance construction above. The discrepancy should be recognized rather than treated as a nonsymmetric quadratic-form definition.

## What the indicators already share with market prices

Exhibits 6–9 show substantial contemporaneous overlap. In FINS, correlations with VIX are 0.81 for average MES, 0.83 for average CoVaR, 0.74 for CoRisk, 0.63 for MES tail proportion, 0.72 for CoVaR tail proportion, 0.33 for absorption ratio, and 0.69 for turbulence. VIX and CDX correlate 0.86. Average MES and average CoVaR correlate 0.97.

In GLOBALS, average MES and VIX correlate 0.84, CoVaR and VIX 0.82, and the two average tail measures again correlate 0.97. High contemporaneous correlation is not by itself proof that an indicator lacks incremental forecast information, but motivates explicit controls. Conversely, a low correlation does not guarantee usefulness: absorption ratio's different time-series behavior does not translate into the desired positive predictive loading.

The time-series exhibits show absorption ratio tracking slow factor-concentration regimes, staying elevated after the crisis despite calmer VIX. Turbulence is more VIX-like before and during 2008–2009 and less so later. The tests therefore assess a particular forecasting use, not every potential interpretation of those indicators.

## Forecasting experiment and baseline

For each business-day horizon $h$, the VIX regression is estimated daily:

$$
VIX_{t+h}-VIX_t=a_h+\sum_{l=0}^{2}\{b^{V}_{h,l}VIX_{t-21l}+b^{C}_{h,l}CDX_{t-21l}\}+\varepsilon_{t,h}.
$$

There are current values and one- and two-month lags, where a month is approximated by 21 business days. For unemployment, estimate monthly for calendar-month horizon $m$:

$$
U_{t+m}-U_t=\alpha_m+\sum_{l=0}^{2}\{c^U_{m,l}U_{t-l}+c^V_{m,l}VIX_{t-l}+c^C_{m,l}CDX_{t-l}\}+\eta_{t,m}.
$$

Each horizon gets a separately fitted regression. The dependent variables are changes in index/rate **levels**, not log changes, recession indicators, or losses on a portfolio. The unemployment charts express the monthly horizon on a business-day-equivalent axis, explaining maxima at multiples of 21.

Each augmented regression adds one contemporaneous systemic-risk indicator $SRI_t$, with coefficient $d_h$ or $d_m$; it does not add all nine jointly or automatically add their lags. Information value is

$$
IV_{SRI}(h)=R^2_{augmented}(h)-R^2_{baseline}(h).
$$

These are unadjusted, **in-sample** $R^2$ values. They cannot decrease when a regressor is added to nested OLS on the same observations. An increase is not itself an out-of-sample forecast improvement or a significance test. Identical sample masks are necessary for the nonnegative nested-regression comparison; precise missing-data masks by horizon are not supplied.

The author also records the fraction of tested horizons for which the added indicator has a positive coefficient significant at 10% or 5%. Positive signs are economically preferred because higher indicators are intended to signal future stress. A negative predictor may improve $R^2$ while failing that directional interpretation. The figures' third-column headers indicate $t$-values, despite prose referring to plotted coefficient loadings; their vertical scale should not be used as an estimated economic effect size without clarification.

Newey–West standard errors use ten lags. Exhibit 11 specifies ten **days** for daily VIX; Exhibit 12 specifies ten **months** for monthly unemployment. Long-horizon dependent changes overlap extensively, so a fixed short bandwidth, particularly ten days for horizons of hundreds of days, requires sensitivity analysis. The article supplies neither a horizon-dependent bandwidth study nor a multiple-horizon testing correction. It expressly states that no formal test of $IV$ was performed.

The baseline VIX regression's displayed $R^2$ rises from under 10% at short horizons toward 60% at long horizons. Unemployment's baseline explanatory power rises toward roughly 70% and then varies around that level. These are sample fits to overlapping changes, not the fraction of future stress that a deployed model is known to predict.

## Results for financial firms

Exhibits 15–16 report maximum information value and its horizon. The values below are **percentage points of $R^2$**, so 13.5 means an increase of 0.135, not a relative 13.5% improvement in a pre-existing $R^2$.

| FINS indicator | VIX maximum IV, pp | Horizon, business days | VIX horizons positive/significant at 5% | Unemployment maximum IV, pp | Horizon, business-day equivalent | Unemployment horizons positive/significant at 5% |
|---|---:|---:|---:|---:|---:|---:|
| CoRisk | 11.3 | 235 | 53% | 8.5 | 378 | 67% |
| MES mean | 4.6 | 345 | 41% | 0.4 | 231 | 0% |
| MES SD | 1.2 | 435 | 8% | 0.1 | 273 | 0% |
| MES tail proportion | 13.5 | 235 | 96% | 17.8 | 420 | 79% |
| CoVaR mean | 2.5 | 345 | 20% | 2.3 | 105 | 0% |
| CoVaR SD | 10.5 | 135 | 94% | 1.8 | 252 | 0% |
| CoVaR tail proportion | 11.3 | 235 | 51% | 8.4 | 378 | 58% |
| Absorption ratio | 4.6 | 135 | 0% | 0.7 | 189 | 0% |
| Turbulence | 3.9 | 365 | 55% | 0.9 | 504 | 4% |

MES tail proportion is strongest across both outcomes. Its high positive-significance fraction is broader evidence than a favorable single horizon, but the horizons are strongly dependent and were examined within the same sample. The fractions are not independent replication counts.

Average MES contributes almost no VIX information before approximately 250 business days, then improves somewhat at longer horizons; it contributes virtually nothing to unemployment. CoVaR SD performs well for VIX, so the result is not simply that every unthresholded aggregate fails. Absorption ratio's maximum $R^2$ increase comes without positive significant loadings, illustrating why statistical fit and the intended stress interpretation need separate assessment.

The best financial-universe VIX horizon, 235 business days, is roughly eleven trading months. Unemployment maxima at 378 or 420 business-day equivalents correspond to 18 or 20 months under the paper's 21-day conversion. The broad “one to one-and-a-half years” characterization should not obscure those actual reported horizons.

## Results for the broader universe

Exhibits 17–18 generally show weaker incremental performance. MES tail proportion remains the leading measure: its maximum IV is 12.2 percentage points for VIX at 305 business days, and 9.1 points for unemployment at 399 business-day equivalents, with 73% and 58% of horizon coefficients positive and significant at 5%.

GLOBALS CoVaR SD reaches 7.2 points for VIX at 115 days, with 76% positive/significant at 5%; CoVaR tail proportion reaches 6.2 at 305 days, with 31%. CoRisk's VIX maximum is only 2.1 points, and its unemployment maximum 2.2 points with no positive coefficients significant at 5%. The conclusion's general praise for CoRisk therefore applies much more clearly to FINS than GLOBALS.

For unemployment in GLOBALS, CoVaR tail proportion reaches 2.6 points but has no positive significant coefficients at either displayed level; average CoVaR's maximum is 4.1 points, also without positive significance. Larger maximum $R^2$ alone is not sufficient for the author's preferred signal. Comparing universes suggests that financial-firm information is particularly relevant in this sample, but the period contains the 2008–2009 financial crisis, and the universes differ in more than just sector membership. This is not a controlled test of a universal financial-sector advantage.

## Interpretation, validation gaps, and reproduction boundary

The paper's strongest methodological point is the benchmark: evaluate an aggregate warning indicator against simple observable information, rather than celebrate its contemporaneous crisis spike. The tail-proportion result suggests that breadth above a loss threshold can preserve information discarded by averaging. The study does not identify the economic mechanism of that advantage, optimize the threshold on an independent sample, or establish a policy rule for acting on the signal.

Several limits prevent treating the reported maxima as deployed forecasting performance. Models, horizons, and thresholds are evaluated in the same historical sample; horizon selection makes a maximum an optimistic summary; long changes overlap; information sets may not respect real-time unemployment availability; and universe/filter selection may use future information. Only one major global financial crisis lies in the regression period. No expanding-window or held-out forecast errors, crisis classification accuracy, economic utility, intervention costs, or false-alarm policy is reported.

An exact replication still needs security identifiers and histories, adjustments and missing-value masks, price-return conventions, index mappings at changes of listing, quantile/tie rules, stock counts for each calculation, covariance conditioning, monthly observation dates, CDX roll treatment, unemployment vintages, and the precise horizon grid. The source describes enough to reconstruct the principal statistics and regressions, but not enough to guarantee the same numerical exhibits.

The negative findings are also conditional on the test. An aggregate indicator may explain crisis propagation afterward, identify vulnerable individual institutions, or predict a rare crisis while adding little to ordinary VIX or unemployment changes. Mamaysky acknowledges those uses and the loss of cross-sectional information through aggregation. The defensible conclusion is that many simplified aggregate measures add limited in-sample information beyond basic market controls in this dataset, while thresholded MES breadth is a promising candidate for further real-time validation.
