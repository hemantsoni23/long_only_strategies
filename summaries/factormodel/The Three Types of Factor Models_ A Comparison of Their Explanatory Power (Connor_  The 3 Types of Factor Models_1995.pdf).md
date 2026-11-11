# The Three Types of Factor Models: A Comparison of Their Explanatory Power

Gregory Connor, *Financial Analysts Journal*, May–June 1995, pp. 42–46. The local PDF contains the complete five-page article and a sixth copyright-notice page. The note compares specified US equity models, rather than proving a universal ranking of all macroeconomic, fundamental, and statistical models.

Source: [Connor_  The 3 Types of Factor Models_1995.pdf](../../Finance/Connor_  The 3 Types of Factor Models_1995.pdf).

## Why this matters

Factor models differ in which part of the return decomposition is observed and which part is estimated. A macroeconomic model supplies factor shocks and estimates stock sensitivities. A fundamental model supplies stock characteristics as exposures and estimates factor returns. A statistical model estimates both from returns. These information requirements matter when exposures change or individual stocks have short histories.

Connor compares explanatory power on a common equity panel. Fundamental and statistical models explain far more return variance than the selected macroeconomic model. The fundamental specification slightly exceeds the five-factor statistical model, largely because it uses a much richer set of external characteristics, particularly 55 industry indicators. The exercise shows the value of external structure, while leaving risk forecasting, economic interpretability, and expected-return prediction as separate questions.

## Common representation and estimation differences

Use the return decomposition $r_{it}=\beta_i^Tf_t+\epsilon_{it}$ as a schematic common language. The paper does not claim that every specification has constant exposures or uses the same estimation routine.

In a macroeconomic model, $f_t$ is an observed vector of macroeconomic shocks or traded return spreads. For each stock, regress its return history on these series to estimate $\beta_i$. A long and stable return history is needed for precise time-series betas, and omitted or poorly measured pervasive shocks remain in residuals.

In a fundamental model, the exposure matrix $B_t$ contains observed characteristics, such as size, book-to-price, dividend yield, and industry membership. Estimate $f_t$ by a cross-sectional regression of stocks' returns on those exposures. The estimated factor return measures the marginal realized return associated with a unit of exposure, conditional on the other included characteristics. It is not simply an unconditional high-minus-low portfolio return. A complete implementation also needs factor normalization, identification constraints, estimation weights, and rules for exposure timing.

A statistical model extracts factors and loadings from the return panel, using principal-components or related factor-analysis methods. The article describes iterative time-series/cross-sectional regression as a common implementation. Rotation changes factor labels while preserving the spanned common-return component: for invertible $H$, $Bf=(BH)(H^{-1}f)$.

The claim that different model types can be rotations of one another is conditional on their capturing the same common-return space without measurement error and with adequate data. It is not proof that an arbitrary chosen set of macro variables equals any selected set of stock characteristics. Nor does the freedom to rotate statistical factors imply that a fitted model automatically identifies the economic mechanism behind returns.

## Sample and specifications

The empirical panel contains 779 high-capitalization US equities with complete monthly return histories from January 1985 through December 1993, 108 months. Securities are drawn from the Barra high-capitalization universe and must have complete histories. This balanced-history restriction can select surviving, seasoned firms; it does not represent a point-in-time investable universe including every entry and exit.

The statistical specification uses five factors. The macroeconomic specification uses five observed series:

- Inflation: change in log CPI.
- Term structure: long-term government-bond-index return minus one-month Treasury-bill return.
- Industrial production: change in log industrial production.
- Default premium: high-yield-bond-index return minus long-term government-bond-index return.
- Unemployment: change in the unemployment rate.

These are the paper's factor definitions. Replacing realized macro changes by separately estimated innovations would be a different model unless documented. The specific series vendor, vintage, release lags, and all return-index details are not supplied here.

The fundamental specification uses 55 industry indicators and twelve Barra risk indexes. The style labels in Table 4 are variability in markets, success, size, trade activity, growth, earnings-to-price, book-to-price, earnings variability, financial leverage, foreign investment, labor intensity, and dividend yield. Industries enter as a group. Definitions and estimation conventions are referred to the 1994 US Equity Model Handbook; the short article does not reproduce all characteristic formulas.

The comparison is therefore intentionally unequal in external data and number of explanatory variables. Five extracted statistical factors should not be described as having been beaten by a fundamental model of the same dimensionality.

## Explanatory-power statistic

Let $v_i$ be total return variance and $s_i^2$ residual variance for stock $i$. Average across the common sample and compute

$$
EP=1-\frac{n^{-1}\sum_i s_i^2}{n^{-1}\sum_i v_i}.
$$

This is a ratio of average variances, not the equally weighted mean of individual-stock $R^2$ values. Higher-variance assets have more influence on the aggregate fit. The article corrects variance estimates for regression degrees of freedom, so adding a variable can yield a zero or negative incremental contribution after the correction.

A factor's incremental power is the difference in this statistic between the augmented and reduced model. For macro and fundamental variables, the tables report both standalone explanatory power and last-added contribution, conditional on all other listed factors. Those are different quantities and do not generally sum to the full-model statistic.

The procedure draws on Connor–Korajczyk's factor-number test: a true omitted factor reduces average specific variance across a broad cross-section, while an extra pseudofactor explains only limited idiosyncratic variation asymptotically. This paper reports descriptive explanatory-power differences, but does not supply all test distributions, standard errors, p-values, or asymptotic assumptions needed to reconstruct a formal significance test for every entry. A positive fitted contribution alone is not a complete statistical rejection of a factor-number hypothesis.

## Numerical findings within each model

The five statistical factors explain 39.0% of the chosen variance measure. Their sequential additions are 29.0, 3.5, 3.1, 1.8, and 1.7 percentage points. The sum differs from the displayed total by 0.1 point because of rounding. The first extracted component dominates, but the later factors still add material descriptive fit.

The macroeconomic model explains 10.9%. Its individual contributions are:

| Factor | Alone | Added last to other four |
|---|---:|---:|
| Inflation | 1.3% | 0.0 pp |
| Term structure | 1.1% | 7.7 pp |
| Industrial production | 0.5% | 0.3 pp |
| Default premium | 2.4% | 8.1 pp |
| Unemployment | −0.3% | 0.1 pp |

The large last-added contributions of the term and default spreads, relative to their standalone values, illustrate interactions and overlapping explanatory information. It would be wrong to rank their usefulness solely by the standalone column. Inflation's standalone fit largely disappears after conditioning on the others. The negative unemployment-alone statistic reflects the degrees-of-freedom correction, rather than literal negative unadjusted explained sum of squares.

The fundamental model explains 42.6%. Industry indicators alone explain 16.3% and add 18.0 percentage points when entered after the twelve styles. Each style's standalone and conditional contribution is shown below.

| Style | Alone | Added last |
|---|---:|---:|
| Variability in markets | 4.3% | 0.9 pp |
| Success | 2.8% | 0.8 pp |
| Size | 1.4% | 0.6 pp |
| Trade activity | 1.4% | 0.5 pp |
| Growth | 3.0% | 0.4 pp |
| Earnings-to-price | 2.2% | 0.6 pp |
| Book-to-price | 1.5% | 0.6 pp |
| Earnings variability | 2.5% | 0.4 pp |
| Financial leverage | 0.9% | 0.5 pp |
| Foreign investment | 0.7% | 0.4 pp |
| Labor intensity | 2.2% | 0.5 pp |
| Dividend yield | 2.9% | 0.4 pp |

The industry block is particularly important, but its contribution is an aggregate over 55 indicators rather than one scalar factor comparable to a single style. None of these explanatory-power numbers is a return premium or factor Sharpe ratio.

## Reading the cross-model table correctly

Table 5's diagonal row gives the base-model fit. Its off-diagonal entries are resulting combined explanatory-power levels, despite prose describing them as “additional” power. Treating the printed 43.0% as a 43-percentage-point increase over the macro model would be incorrect.

| First model | First-model EP | Add macro | Add statistical | Add fundamental |
|---|---:|---:|---:|---:|
| Macroeconomic | 10.9% | — | 31.0% | 43.0% |
| Statistical | 39.0% | 38.2% | — | 45.6% |
| Fundamental | 42.6% | 42.4% | 44.8% | — |

Thus macro factors add no positive corrected fit to the statistical or fundamental models: their combined values are 0.8 and 0.2 percentage points lower than the respective baselines. This is the quantitative basis for the article's statement that their marginal explanatory power is zero. It does not mean the reported numerical differences are exactly zero.

Combining statistical and fundamental information raises fit to 44.8% or 45.6%, depending on estimation order. Macro-first followed by statistical gives 31.0%, while statistical-first followed by macro gives 38.2%. The asymmetry shows that these are order-dependent modeling procedures rather than the unique fit of a single, fully specified joint regression space. The short article does not give enough implementation detail to reproduce every order effect exactly.

The fundamental model's 42.6% exceeds the five-factor statistical model's 39.0% by 3.6 percentage points. The explanation offered is greater external information and dimensionality, especially industry classifications. This does not contradict the optimality of principal components within a fixed-rank return-only approximation: the compared fundamental specification has a much larger information set and different restrictions.

## Reconstruction and missing inputs

A faithful study should first reproduce the balanced 779-stock panel, use the same 108 monthly observations for every model, and disclose return and variance-centering conventions. It should preserve the exact macro definitions and obtain the historical fundamental-model descriptors and identification rules. Estimate the five statistical factors with the source's factor-analysis method rather than silently substituting a modern shrinkage covariance or a different number of components.

For each fitted model, retain residuals and actual regression degrees of freedom, calculate the cross-sectional average residual variance, and form the ratio above. For a last-added factor contribution, refit the appropriate reduced model; do not infer it from one coefficient or from that factor's standalone fit. For industries, remove or add the whole indicator block together.

The article lacks full formulas for its statistical-factor extraction, exposure weighting, model-combination algorithm, characteristic definitions, data alignment, and exact variance corrections in every stage. These omissions limit exact reproduction from this PDF alone. The paper does not specify portfolio construction, transaction costs, rebalancing, hyperparameter validation, or a future return test because those are not the experiment it performs.

## Interpretation and limits

The result is about describing common historical return variation. A model can fit contemporaneous returns well yet forecast covariance poorly, estimate expected returns badly, or produce fragile optimized portfolios. The study does not establish that a fundamental risk model dominates every macro model for stress testing or economic scenario interpretation; the author explicitly recognizes theoretical consistency and intuitive appeal as reasons to use macroeconomic factors.

Similarly, no incremental fit from the chosen macro variables does not prove that their risks are absent, that all macroeconomic shocks are captured, or that a unique rotation from characteristics to economic betas has been found. The article leaves that mapping to future research. Omitted shocks, measurement noise, estimation error, and the chosen sample can affect the comparison.

The useful research lesson is to compare factor systems through both their information inputs and the residual common variation they leave behind. This paper provides a concrete historical comparison and a reusable fit statistic, while its limited specification and in-sample descriptive criterion prevent the rankings from becoming universal investment recommendations.
