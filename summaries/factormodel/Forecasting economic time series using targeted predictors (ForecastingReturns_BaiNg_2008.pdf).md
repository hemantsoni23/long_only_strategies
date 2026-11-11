# Forecasting economic time series using targeted predictors

Jushan Bai and Serena Ng. *Journal of Econometrics* 146 (2008), 304–317. DOI: 10.1016/j.jeconom.2008.08.010.

Source: [ForecastingReturns_BaiNg_2008.pdf](../../Finance/ForecastingReturns_BaiNg_2008.pdf), 14 PDF pages. Page references below use the printed journal pagination. Despite the library filename, the main forecasting application is inflation, followed by four real economic series. This note covers the article, its tables, and its data appendix.

## Why this matters

A factor explaining much of the variation in a large predictor panel need not explain the particular variable being forecast. Bai and Ng therefore select variables using their relationship with the target before extracting principal components. Their important contribution is this ordering of operations: supervised selection, followed by dimension reduction, followed by a small forecasting regression. The selected panel changes with the forecast target, horizon, and estimation date.

The paper also separates two routes to nonlinear forecasts. One can construct factors from original and squared predictors, or estimate ordinary linear factors and add their squares to the forecasting regression. Those procedures impose different restrictions. The empirical gains are strongest for some medium-horizon inflation forecasts; neither selecting variables nor adding nonlinear terms uniformly wins in every subsample.

For implementation, the distinction between selection and prediction is essential. The LARS or elastic-net procedure usually supplies a ranking of candidate series. The principal forecast uses principal components of the first 30 ranked series, rather than the sparse regression's fitted value or its BIC-selected number of nonzero coefficients. This retains the variance reduction of a factor model while making its inputs relevant to the target.

## Forecasting problem and information set

Let $X_t=(X_{1t},\ldots,X_{Nt})'$ contain stationary transformations of the monthly predictors. The benchmark approximate factor representation is

$$
X_t=\Lambda F_t+e_t.
$$

There are $N=132$ predictors. The common factors capture shared variation, while the idiosyncratic components can contain weak dependence. Principal components estimate the space spanned by the factors; rotations and normalizations are absorbed by the forecasting coefficients. With observations arranged as an $N\times T$ matrix, the time-series factor estimates are proportional to the leading eigenvectors of $X'X$. The paper demeans and standardizes data before extracting components. It retains the first ten estimated factors as candidates for the forecast regression.

For a horizon $h$, the direct forecast equation is

$$
y_{t+h}^{h}=\alpha'W_t+\beta(L)'\widehat f_t+\epsilon_{t+h},
$$

where $W_t$ includes an intercept and autoregressive information, $\widehat f_t$ is a selected subset of the first ten components, and $\beta(L)$ permits factor lags. BIC chooses the forecasting specification. The stated maximum lag is six when the sample permits, otherwise four; the article does not state a mechanical sample-size boundary for that reduction or every detail of the subset-search implementation.

In the inflation exercise, let $p_t$ denote log CPI, to avoid confusing the price level with the transformed forecast target. Define monthly annualized inflation and its change as

$$
\pi_t=1200(p_t-p_{t-1}),\qquad z_t=\pi_t-\pi_{t-1}.
$$

The dependent variable is

$$
y_{t+h}^{h}=\frac{1200}{h}(p_{t+h}-p_t)-\pi_t.
$$

Thus the forecast is for the change from current monthly annualized inflation to the average annualized inflation over the next $h$ months. Adding $\pi_t$ to the predicted dependent variable recovers the predicted future average inflation. The scaling yields annualized percentage points when logs are unscaled. Treating the target as the log CPI level, an ordinary one-month return, or cumulative unannualized inflation would reproduce a different exercise.

The authors assume log CPI is integrated of order two. Their four additional targets—personal income, retail sales, industrial production, and employment—are treated as having log levels integrated of order one. For them the dependent variable is $1200(p_{t+h}-p_t)/h$ and the autoregressive increment is $1200(p_t-p_{t-1})$.

A causal reconstruction must distinguish current predictors from completed forecast targets. At origin $t$, $X_t$ may be included in factor estimation if genuinely observed, but a training regression observation with origin $s$ is usable only when $s+h\leq t$. Screening variables on future target observations would contaminate the entire factor construction. This restriction applies separately at every horizon.

## Hard targeting

Section 3.1, p. 306, gives a particularly simple selection procedure. For each candidate series $i$, regress the horizon target on $W$ and that series alone. In origin notation,

$$
y_{s+h}^{h}=a_i'W_s+b_iX_{is}+u_{i,s+h}.
$$

The empirical screening controls contain a constant and four autoregressive lags. Record the absolute $t$ statistic for $b_i$, rank the predictors by that statistic, and retain those exceeding a chosen threshold $\tau$. Estimate principal components from the retained panel and fit the BIC-selected forecast regression using those components.

Equivalently, residualize both the dependent variable and each predictor against $W$. If $M_W=I-W(W'W)^{-1}W'$, the screen is based on the regression of $M_Wy$ on $M_WX_i$. This is a conditional marginal test: it controls for the autoregression, but not for the other candidate macro predictors. Consequently many highly correlated series can pass together. Selection frequency measures how often an observable survives the screen; it does not measure its unique contribution after all selected variables are included.

The main reported thresholds are 1.28, 1.65, and 2.58. Their numerical values should be preserved, but the article's description of them as two-tailed 10%, 5%, and 1% normal critical values is inaccurate. Approximately, they correspond to two-sided 20%, 10%, and 1% levels. Moreover, overlapping multi-month targets create serially dependent regression disturbances, and the article does not fully specify the covariance estimator used for these screening statistics. It is safest to treat these as operational screening cutoffs rather than fully documented nominal-size tests.

The paper also mentions a Holm-style multiple-testing alternative, but does not report its forecast results. The principal tables therefore do not demonstrate familywise-error control across 132 screens. A replication should first reproduce the raw cutoffs, with any multiplicity correction identified as an additional experiment.

## Nonlinearity: expanded inputs versus squared factors

For squared principal components, or SPC, augment the predictor vector to include original variables and their squares:

$$
X_t^*=\begin{pmatrix}X_t\\X_t\odot X_t\end{pmatrix},\qquad X_t^*=\Phi J_t+\eta_t.
$$

This produces 264 input columns before targeting. PCA is linear in the augmented variables but nonlinear in the original predictors. The resulting factors enter a linear forecasting regression. This differs from estimating factors using only squared predictors, which would primarily target a second-moment structure; the latter is not the forecasting method evaluated here.

The alternative called $PC^2$ estimates ordinary factors first and then includes their componentwise squares:

$$
y_{t+h}^{h}=\alpha'W_t+\beta_1'\widehat F_t+\beta_2'(\widehat F_t\odot\widehat F_t)+\epsilon_{t+h}.
$$

Squaring a linear combination generates cross-products as well as squares, with coefficients constrained by the factor loadings. SPC and $PC^2$ therefore span different predictor spaces. A third construction, quadratic principal components using all cross-products $X_iX_j$, was investigated in an earlier version but omitted because it was computationally burdensome and did not notably improve on SPC.

The tables additionally label hard-screened variants TPC, TSPC, TSTPC, and $TPC^2$. TPC is clearly PCA on the selected linear predictors. The descriptions of the two targeted expanded-panel variants do not completely specify the nesting of the linear and squared-variable screens, and the discussion of $TPC^2$ is not fully consistent with the predictor counts in Table 3. These labels can be reported as the authors' results, but an exact reimplementation should resolve their original code conventions rather than silently equating the variants. The unambiguous TPC and LARS-ordered linear/expanded-panel methods already implement the central contribution.

For any expanded-panel implementation, document whether squaring occurs before or after standardizing the original series and whether each expanded column is then standardized anew. Although the span of a complete linear-plus-square regression can be invariant to some affine transformations, PCA weighting is not. The paper states that data are demeaned and standardized before PCA, without fully documenting every preprocessing stage of the expansion.

## Soft targeting and elastic-net ranking

Hard thresholding tests variables separately and changes the selected panel discontinuously near the cutoff. The alternative uses joint penalized regression. With the autoregressive controls unpenalized, a coherent objective is

$$
\min_{\alpha,b}\ \|y-W\alpha-Xb\|_2^2+\lambda_1\|b\|_1+\lambda_2\|b\|_2^2.
$$

Here the design matrix has observations in rows, unlike the earlier factor-model convention. One can first project $y$ and $X$ off $W$ and solve for $b$ on the residualized data. This makes the treatment of the controls explicit. LASSO sets $\lambda_2=0$; positive $\lambda_2$ stabilizes estimation with correlated predictors and allows a useful path when the number of variables exceeds the early sample length.

For orthogonal columns of unit squared norm, LASSO reduces to the familiar coordinatewise rule

$$
\widehat b_j=\operatorname{sign}(b_j^{OLS})(|b_j^{OLS}|-\lambda_1/2)_+.
$$

This formula is not valid coordinatewise for a correlated macro panel. More generally, active coefficients satisfy

$$
X_j'(y-X\widehat b)=\frac{\lambda_1}{2}\operatorname{sign}(\widehat b_j)+\lambda_2\widehat b_j.
$$

The article's broad statement that LASSO shrinkage does not depend on predictor correlations is therefore only appropriate in the orthogonal special case. Likewise, its generic oracle-property wording should not be read as a theorem establishing selection consistency for this dependent macro panel. No new theorem proves oracle forecasting performance for the full targeted-PCA pipeline.

The elastic-net objective can be written as LASSO on augmented data. The printed construction is

$$
X^+=\frac{1}{\sqrt{1+\lambda_2}}\begin{pmatrix}X\\\sqrt{\lambda_2}I\end{pmatrix},\qquad y^+=\begin{pmatrix}y\\0\end{pmatrix},\qquad \gamma=\frac{\lambda_1}{\sqrt{1+\lambda_2}}.
$$

There is a normalization issue in the subsequent coefficient-rescaling statement. With exactly this $X^+$, its LASSO coefficient $b^{++}$ equals $\sqrt{1+\lambda_2}$ times the minimizer of the unrescaled elastic-net objective. Removing the usual additional ridge shrinkage would therefore give $\sqrt{1+\lambda_2}b^{++}$, not $(1+\lambda_2)b^{++}$ as printed. This is an algebraic clarification, not an empirical correction reported by the authors. It does not change the ordering of variables under a common positive rescaling, which is the main object used for their factor forecasts.

## LARS algorithm and final forecast construction

Section 4.3 gives the least-angle regression path. Starting with fitted values $\widehat\mu=0$, compute correlations $c=X'(y-\widehat\mu)$, their largest absolute value $C$, and an active set $K$ attaining that maximum. Use signs $s_j=\operatorname{sign}(c_j)$ to construct the signed active design $X_K=(s_jX_j)_{j\in K}$. Define

$$
G_K=X_K'X_K,\quad A_K=(\mathbf1'G_K^{-1}\mathbf1)^{-1/2},\quad w_K=A_KG_K^{-1}\mathbf1,\quad u_K=X_Kw_K.
$$

The vector $u_K$ is equiangular to the signed active columns. With $a=X'u_K$, move fitted values along $u_K$ until another variable reaches the common absolute correlation:

$$
\widehat\mu_{new}=\widehat\mu+\widehat\gamma u_K,
$$

$$
\widehat\gamma=\min_{j\notin K}^{+}\left\{\frac{C-c_j}{A_K-a_j},\frac{C+c_j}{A_K+a_j}\right\}.
$$

The superscript $+$ means take only positive admissible step lengths. LARS progressively admits variables; a LASSO modification also drops active coefficients at zero crossings to enforce the sign condition. Singular active Gram matrices, exact ties, numerical tolerances, and drop/re-entry ranking conventions require software choices not fully supplied in the paper.

The BIC along the selection path is

$$
BIC(k)=\log(\widehat\sigma_k^2)+k\frac{\log T}{T}.
$$

The minimizing $k^*$ is used in one direct forecast variant. The principal factor method instead takes the first 30 ranked predictors, regardless of $k^*$, extracts candidate factors, and selects the final forecasting equation by BIC. Thirty is an experience-based fixed choice in the paper, not the result of a reported optimality theorem or nested validation search.

The comparisons are: ordinary PCA on all 132 series; SPC on all 264 expanded series; hard-targeted factor forecasts; LA(PC), meaning PCA on the first 30 jointly ranked linear predictors; LA(SPC), using 30 ranked candidates from the expanded panel; and direct regressions using the first five or first $k^*$ ranked predictors without PCA. The direct predictors are used in their nonstandardized form in the final forecast. The methods section and predictor-count table specify five fixed predictors, although several forecast-table headers print LA(10). That discrepancy must be retained in any attempt to reproduce the published cells.

The reported elastic-net ridge penalties are $\lambda_2=0.25,0.5,1.5$. LARS and LASSO rankings gave similar results in the authors' experiments, so the displayed soft-targeting results use LARS with elastic-net augmentation. They do not select the penalty by ordinary random cross-validation, which would be inappropriate for this expanding time-series exercise in any case.

## Data, estimation windows, and scoring

The monthly predictor panel runs from January 1960 to December 2003, 528 observations before transformations. The data are associated with the Stock–Watson macro dataset, primarily Global Insight's Basic Economics database with some Conference Board series. The appendix gives names, mnemonics, transformations, and fast/slow designations for many series: production, employment, hours, housing, orders, money, equity-market variables, yields, and spreads. The supplied table does not settle a complete machine-readable 132-column vintage, including all price-series inputs referenced in the text.

The initial estimation period uses roughly ten years, with transformed observations beginning in March 1960. Forecasting then proceeds monthly with an expanding window and horizons 1, 6, 12, and 24 months. Predictor selection, factor estimation, and final regression estimation are repeated as the origin advances. For a 12-month forecast ending in December 2003, the final origin is December 2002.

Appendix Tables A.1–A.2 describe forecast windows beginning in March 1970, 1980, or 1990 and ending in December 1980, 1990, 2000, or 2003, including overlapping combined windows. Main forecast tables instead use labels such as 70.1–80.1 and 70.1–03.9. These are not identical date conventions. Exact first/last evaluated origins and the treatment of endpoints must be reconciled with original data/code. The repeated 24-month full-sample rows also do not independently resolve the endpoint discrepancy.

The benchmark is an autoregression with four lags. Crucially, the paper abbreviates **relative mean squared error** as RMSE. It is not root mean squared error:

$$
R_h=\frac{\sum_t(y_{t+h}^{h}-\widehat y_{t+h|t}^{h})^2}{\sum_t(y_{t+h}^{h}-\widehat y_{AR(4),t+h|t}^{h})^2}.
$$

Values below one beat AR(4) in sample-average squared forecast loss. Comparisons between methods use ratios of these entries. An entry of 0.60 represents a 40% MSE reduction from the benchmark, not a 40% reduction in root error. The tables report neither standard errors for these ratios nor a full forecast-comparison inference exercise accounting for overlapping horizons and specification search.

This is a pseudo-out-of-sample evaluation using the available historical dataset. The paper does not provide a complete real-time release calendar, vintage database, ragged-edge treatment, missing-value algorithm, or publication-delay adjustment. A live inflation forecast cannot assume all observations dated $t$ were released at $t$. These omissions are material when converting the method to production, rather than merely reproducing a historical statistical comparison.

## Principal numerical findings

Table 3 shows how much the selected panel changes with the horizon. In the full printed sample row, hard targeting at 1.65 retains on average 57.757 variables at one month, 63.003 at six months, 80.634 at twelve months, and 87.418 at twenty-four months. By contrast, the BIC-selected direct LARS model with $\lambda_2=0.5$ averages 2.231, 7.038, 12.769, and 15.119 predictors. The prose's statement that the twelve-month count is below ten does not describe that full-sample row. The factor forecasts always use 30 ranked inputs in the soft-selection variant.

Table 1 confirms horizon-dependent relevance. At the 1.28 hard cutoff, 17.4% of original predictors are selected in more than 80% of one-month estimation windows, compared with 50.8% at twelve months. Tightening the cutoff to 2.58 leaves only 2.3% in that high-frequency inclusion bin at one month. Short-horizon marginal rankings emphasize interest rates; at longer horizons real M2, housing, and labor-market variables become more prominent. Joint rankings include the federal funds rate, bond yields, help-wanted measures, and housing variables. This is evidence about selected forecasting inputs, not structural causal identification.

The following entries reproduce the main full-row comparisons, using $\lambda_2=0.25$ for the LARS variants:

| Horizon, months | PC | SPC | LA(PC) | LA(SPC) | Direct fixed-count column | Direct $k^*$ |
|---|---:|---:|---:|---:|---:|---:|
| 6 | 0.670 | 0.623 | 0.609 | 0.587 | 0.660 | 0.712 |
| 12 | 0.609 | 0.597 | 0.570 | 0.517 | 0.592 | 0.754 |
| 24 | 0.523 | 0.540 | 0.464 | 0.562 | 0.646 | 0.683 |

Sources: Tables 5–7, pp. 313–314. At twelve months, LA(SPC) reduces MSE by about $1-0.517/0.609=15.1\%$ relative to PC. The corresponding root-error reduction is approximately 7.9%. At twenty-four months, however, LA(PC) is better than LA(SPC). The source's broad claim that LA(SPC) is systematically best at all three longer horizons is not supported by Table 7. Nonlinear expansion is useful selectively, not mechanically.

At one month, gains are smaller. Table 4's full row gives PC 0.979 and SPC 0.961. With the middle hard cutoff and $\lambda_2=0.5$, TPC is 0.960, TSPC 0.938, LA(PC) 0.950, and LA(SPC) 0.936. These differences are numerical loss comparisons; the paper does not supply uncertainty intervals establishing their significance. Several methods also perform poorly in early high-inflation subsamples.

For twelve-month forecasts of the four additional targets, Table 8 fixes the hard threshold at 1.65 and $\lambda_2=0.25$ without further target-specific tuning. Full-row PC versus best reported comparison is 0.817 versus 0.716 for personal income (SPC); 0.726 versus 0.668 for retail sales (direct $k^*$); 0.551 versus 0.498 for industrial production (LA(SPC)); and 0.696 versus 0.609 for employment (LA(PC)). This demonstrates that the best compression choice depends on the target. Direct selected predictors can be competitive for income and sales, while factor averaging is more valuable for production and employment.

Failures are informative. In the 1990s industrial-production row, PC is 1.055, TPC 1.327, LA(PC) 1.423, and LA(SPC) 1.340; only the displayed untargeted SPC entry, 0.974, is below one. Thus not every subsample supports the prose's strongest universal comparisons. A replication should preserve the full table of outcomes rather than evaluating success only at the best full-sample configuration.

## Reimplementation and limits

A faithful first implementation should recover the historical panel and transformations, build horizon-specific completed targets, rerun the screen or LARS ordering within each expanding window, extract and normalize factors using only that window, choose the final regression with BIC, and score identical forecast origins against AR(4). Record selected variables, factor counts, lags, training endpoints, and forecast errors at every origin. Separately implement PC, SPC, TPC, LA(PC), LA(SPC), and the direct fixed-five/$k^*$ controls. This separates input selection from nonlinear expansion and from factor averaging.

Several details prevent claiming exact numerical replication from the PDF alone: the original data vintage, full 132-series matrix, all transformation and missing-data rules, release timing, precise BIC subset search, cutoff-label discrepancies, fixed-five versus LA(10) table headings, and the targeting order in the TSPC/TSTPC variants. Table 2 also labels its hard thresholds 1.28, 1.96, and 2.32 rather than the main tables' 1.28, 1.65, and 2.58. These inconsistencies are source limitations, not grounds for inventing hidden settings.

The paper establishes a useful forecasting architecture and supplies substantial comparative evidence. It does not show that principal components should always be targeted, that a selected macro series is a causal driver, or that its forecasts translate into trading profits after costs. The practical lesson is to regard factor extraction as part of a target-specific estimation pipeline, then validate that whole pipeline at genuinely available information dates. The amount of shared predictor variance retained is an intermediate statistic; forecast loss on the intended target remains the objective.
