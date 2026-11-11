# The empirical risk-return relation: a factor analysis approach

**Sydney C. Ludvigson and Serena Ng.** *Journal of Financial Economics* 83 (2007), 171–222. Source: [DynamicFactorModels_LudvigsonNg_2007.pdf](../../Finance/DynamicFactorModels_LudvigsonNg_2007.pdf). The local file is a 65-page author manuscript carrying the journal citation; page references below use PDF pages to avoid confusing manuscript and journal pagination. The full text, data appendix, robustness appendix, tables, and figures were inspected, with key numerical tables rendered for verification.

## Why this matters

Empirical estimates of the risk–return tradeoff depend on how expected return and expected risk are measured. Regressing future returns on a few familiar predictors is convenient, but it may omit information used by investors. If the missing information predicts mean returns differently from volatility, the inferred relation between the two conditional moments can change sign. The paper asks whether broad economic and financial panels contain relevant information beyond conventional conditioning variables.

Its contribution is to use estimated common factors as additional predictors of next-quarter market excess returns and realized volatility. Two financial factors are particularly useful for returns: the squared first principal component and the third principal component. A macroeconomic first component helps forecast volatility. With these predictors, the authors find a positive relation between fitted mean and fitted volatility after controlling for their lagged values, even though their unconditional contemporaneous relation is weakly negative.

The central result is therefore more specific than “higher risk always predicts higher returns.” It is a positive partial association between two estimated conditional moments, with substantial lead–lag effects. The fitted mean is not proportional to fitted volatility, and the fitted Sharpe ratio varies considerably over the business cycle. The analysis also distinguishes retrospective estimation of those moments from a recursive forecast exercise, although the latter retains specification-selection and data-vintage limitations.

## Statistical architecture

Let $m_{t+1}$ be next quarter's continuously compounded excess stock-market return, and let $VOL_{t+1}$ be its realized-volatility measure. For a $T\times N$ panel $X$ of transformed and standardized observations,

$$
x_{it}=\lambda_i'f_t+e_{it},
$$

where $f_t$ contains a small number $r$ of latent common factors. The approximate-factor model permits limited residual cross-correlation. One stated restriction bounds the cross-sectional sum of absolute idiosyncratic covariances after division by $N$, so that residual dependence cannot become as pervasive as the common factors.

Estimate the $T\times r$ factor matrix as $\sqrt T$ times the leading eigenvectors of $XX'/(TN)$. Then

$$
\widehat F'\widehat F/T=I_r,\qquad
\widehat\Lambda=X'\widehat F/T,\qquad
\widehat\chi_{it}=\widehat\lambda_i'\widehat f_t.
$$

This is static principal-component extraction from an approximate dynamic factor environment. The implementation does not estimate a separate spectral factorization or a state-space Kalman filter. Dynamic information enters through the time series in the panel and the forecast timing.

The authors extract factors separately from macroeconomic and financial panels. Denote macro components by $F_{jt}$ and financial components by $G_{jt}$. Factors are ordered by eigenvalue. Their signs are arbitrary, and coefficient signs on a single component reverse if its sign convention reverses. Predictions and fitted components do not change. Squared factors and interactions make the choice of principal-component basis important; arbitrary rotations before forming the nonlinear terms generally produce a different forecast specification.

Not every factor explaining a large share of panel variance is useful for forecasting a particular outcome. The predictive regressions therefore select subsets and functions of the estimated factors:

$$
m_{t+1}=a_0+a_F'\widehat F_t+a_G'\widehat G_t+b'Z_t+\varepsilon_{t+1},
$$

$$
VOL_{t+1}=c_0+c_F'\widehat F_t+c_G'\widehat G_t+d'Z_t+u_{t+1}.
$$

Here $Z_t$ contains observed conditioning variables. The paper considers component squares, products, and alternative lag specifications, chooses parsimonious models with BIC, and also reports adjusted $R^2$. The latent factor count is selected separately with Bai–Ng panel information criteria; eight factors are retained from each panel. The exact exhaustive menu of all nonlinear candidates and the detailed BIC normalization are not supplied, so reproducing the displayed final models is easier than reproducing every step of the specification search.

The asymptotic motivation relies on both $N,T\to\infty$, with $\sqrt T/N\to0$ for the cited factor-augmented regression inference. Under the required regularity conditions, regression coefficients are $\sqrt T$ consistent and asymptotically normal, and first-order coefficient inference can proceed as if the factors were observed. Fitted conditional means have an error rate governed by the smaller of $\sqrt N$ and $\sqrt T$. These results do not erase finite-sample model-selection uncertainty or justify ordinary inference under arbitrary weak-factor, highly persistent, or structurally unstable designs.

## Return and volatility measurement

The return target is the CRSP value-weighted market index covering NYSE, Amex, and Nasdaq, expressed as a log return in excess of a three-month Treasury bill return. The paper's realized-volatility measure uses daily excess returns within a quarter:

$$
VOL_t=\left[\sum_{k\in t}(R_{s,k}-\overline R_s)^2\right]^{1/2},
$$

where $R_{s,k}$ is the daily market return less an implied daily three-month Treasury bill yield, and $\overline R_s$ is the full-sample daily mean. There is no division by the number of days in this formula and no stated annualization. Thus $VOL_t$ is on a quarterly cumulative-return volatility scale, rather than an average daily standard deviation. A faithful replication must document the daily yield-conversion convention because the paper does not fully specify its compounding and day-count details.

The distinction between variance and volatility is important. The square root is taken before the quarterly predictive regression. The fitted object is

$$
\sigma_t=\widehat E_t[VOL_{t+1}],
$$

not directly $\sqrt{\widehat{\operatorname{Var}}_t(m_{t+1})}$. Even if summed squared high-frequency returns estimate integrated variance well, taking square roots is nonlinear. The paper's broad language about unbiased realized volatility should not be read as an exact finite-sample claim that expected square-root realized variance equals conditional standard deviation. Daily sampling also retains measurement error relative to an ideal continuously observed process.

The conditional mean is

$$
\mu_t=\widehat E_t[m_{t+1}].
$$

The time subscript labels the conditioning date, not the realization date. In the main analysis, both are fitted using full-sample estimates, including full-sample principal components. These are smoothed retrospective estimates of conditional-moment variation. They are not real-time forecasts available to an investor in quarter $t$.

## Data construction and source inconsistencies

The principal in-sample period is 1960Q1–2002Q4, 172 quarterly observations before regression-specific lag losses. The macro panel has 209 series from the DRI–Global Insight Basic Economics Database. Appendix A.1 lists every series mnemonic and transformation code. The codes used are 1 for no transformation, 2 for first difference, 4 for log level, and 5 for first difference of the log. Apply the listed code series by series, then standardize before extracting factors.

The macro categories cover exports and imports, consumption, price indexes, fixed investment, output and income, sales and orders, employment and hours, compensation and labor costs, capacity utilization, housing, composite indexes, and other indicators. Some transformations that might look unusual, such as first differences of rates or logged survey measures, are explicitly prescribed in that appendix. Substituting a modern generic transformation codebook would change the panel. The appendix even lists the same final-sales mnemonic twice, at positions 112 and 113; a replication must decide whether this was an actual duplicate input or a documentation error using original data/code rather than silently deduplicating it.

The financial panel includes dividend and price growth, dividend–price and price–earnings ratios, Treasury yields and spreads, corporate yields, default spreads, market/size/value/momentum factors, the Cochrane–Piazzesi bond predictor, the consumption–wealth residual $cay$, a small-stock value spread, industry portfolio returns, and size/book-to-market portfolio returns. Portfolios with missing observations during the selected sample are omitted.

The main prose repeatedly says 172 financial series, but Table 1, Tables 2–3, and the numbered data appendix support 159. The appendix ends at financial series 159 and explicitly lists retained size/book-to-market cells. Therefore 159 is the best-documented implemented panel dimension, while 172 is a conflicting headline count. Appendix table footnotes introduce further inconsistencies, describing 208 financial or 159 macro series. These should not replace the detailed 209-macro/159-financial tables without the authors' dataset.

The observed predictors have the following intended definitions. $cay$ is the cointegrating residual among log real per-capita consumption, asset wealth, and labor income. The log dividend–price ratio is formed from the CRSP market series and trailing dividends. $RREL$ is the three-month bill yield minus its trailing four-quarter average. $YIELD$ is a one-year Treasury yield. $DEF$ is the BAA minus AAA corporate yield. The main discussion defines a ten-year minus one-year term spread, while Table 2 defines ten-year minus three-month; both spreads are in the financial data list. The financial appendix also reverses the default-spread label as AAA minus BAA. For displayed Table 2 replication, use its stated BAA-minus-AAA and ten-year-minus-three-month conventions, while recording the conflict.

These inconsistencies affect exact data recreation, not merely citation formatting. They are especially important because duplicating an input changes PCA weighting, reversing a predictor changes coefficient signs, and adding or removing portfolio columns can change the ordering of weaker components.

## The selected forecasting models

The preferred conditional-mean model, MOD1, uses $cay_t$, $G_{1t}^2$, and $G_{3t}$:

$$
\widehat\mu_t\simeq-0.001+1.822\,cay_t+0.011\,G_{1t}^2+0.019\,G_{3t}.
$$

These are the more precise coefficients reported in Tables 7–8; factors have the PCA normalization above and returns are decimal quarterly log excess returns. Coefficients are not portable to rescaled factors or to percentage-return units. The raw in-sample $R^2$ is 0.170 and adjusted $R^2$ is approximately 0.16. In Table 2, the factor-square and third-factor Newey–West $t$ statistics are 3.88 and 3.13, and the $cay$ statistic is 3.94. The selected BIC is reported as −2.11.

The two financial predictors alone explain about 9% of next-quarter return variation on the adjusted measure. By comparison, $cay$ alone explains about 8%, while the dividend–price ratio alone explains about 1%. Their combined explanatory power is therefore not simply the same information entering three times. Adding lagged realized volatility and conventional rate/spread predictors does not remove the marginal financial-factor contribution in the reported specifications.

MOD2 adds the interaction $F_{3t}F_{6t}$ to MOD1. The paper uses this as an alternative fitted mean when testing the risk–return relation; it reports adjusted $R^2$ near 0.17 and BIC −2.10. Broader interactions can raise reported fit to roughly 18–19%, but do not beat MOD1 under the BIC penalty. Some prose rounds this to 20%. These figures are in-sample fit following a specification search, not returns earned or out-of-sample $R^2$.

The preferred parsimonious volatility model, SPEC1, uses the log dividend–price ratio, the one-year yield, the first macro factor, and current realized volatility:

$$
\widehat\sigma_t\simeq-0.106-0.036(d_t-p_t)+1.152\,YIELD_t
+0.005\,F_{1t}+0.347\,VOL_t.
$$

Tables 7–8 give raw $R^2=0.386$ and adjusted $R^2=0.371$. Table 3 gives Newey–West statistics approximately −6.718, 3.592, 4.015, and 4.706 for these four slopes. A slightly larger model also includes $F_{6t}$, with adjusted fit around 0.39 and BIC −4.49, versus −4.48 for the parsimonious specification. SPEC2 omits the macro factor and keeps the three financial predictors.

The model is linear in the displayed predictors and does not enforce positivity of the volatility forecast. Imposing a floor, fitting logs, or applying a Jensen correction would be a model extension. Similarly, negative fitted expected returns are allowed; the authors observe them in the sample rather than truncating them to zero.

## Economic interpretation of the selected components

The first financial component explains 65.7% of the standardized financial panel's variance; the first eight explain 83.1%. The first macro component explains 24.5%, and the first eight 64.9%. Financial factor one has first-order autocorrelation −0.032, financial factor three 0.166, and macro factor one 0.672. The strongest selected financial predictors therefore are not nearly unit-root level series. Other components are more persistent, including second components with autocorrelation around 0.8.

The squared first financial component explains almost 80% of contemporaneous squared market-return variation and about 40% of realized-volatility variation. The authors call it a volatility factor. It is not the same measured object as $VOL_t$, and the name does not imply that it is a structural volatility innovation.

The third financial component is strongly associated with the Fama–French market, size, and value factors. A contemporaneous regression on those three factors has adjusted fit about 86%; adding the risk-free rate raises it to about 96%. The reported three-factor slopes are approximately 0.052 on the market, −0.322 on SMB, and −0.404 on HML, under the authors' factor sign convention. This motivates the “risk premium factor” label. It does not prove the component is uniquely priced or that the cross-sectional and time-series regressions identify the same causal mechanism.

The first macro component explains 73% of contemporaneous manufacturing-output variation and is called a real factor. The interpretation is deliberately broad: a principal component aggregates correlated real-activity measures rather than representing one directly observable economic state. The central empirical claim is incremental forecast information, not a structural labeling theorem.

## Estimating the risk–return relation

After constructing the fitted moments, estimate

$$
\mu_t=\delta+\beta_1\sigma_t+\beta_2\sigma_{t-1}
+\alpha\mu_{t-1}+\gamma m_{t-1}+\epsilon_t,
$$

with variants omitting $m_{t-1}$ or all lags. Every regression includes an intercept. The coefficient $\beta_1$ describes a partial contemporaneous association after the included lags are controlled for. It is not itself a correlation coefficient and is not automatically a coefficient of relative risk aversion. In particular, the conventional intertemporal pricing relation often uses conditional variance, whereas this regression uses fitted expected realized volatility.

Table 4, row 1, using MOD1 and SPEC1 without lagged actual return, estimates $\beta_1=1.40$ with $t=4.80$, $\beta_2=-1.46$ with $t=-7.67$, and $\alpha=0.62$ with $t=10.03$. Adjusted fit is 0.41. Including $m_{t-1}$ gives $\beta_1=1.07$ ($t=4.14$), $\beta_2=-1.18$, $\alpha=0.71$, and $\gamma=-0.11$ ($t=-3.40$), with adjusted fit 0.46.

The nearly offsetting positive current-volatility and negative lagged-volatility coefficients indicate that volatility changes, not just its persistent level, matter to this conditional regression. The algebra can be written as $\beta_1\Delta\sigma_t+(\beta_1+\beta_2)\sigma_{t-1}$, showing why a near-zero or negative unconditional association can coexist with a positive contemporaneous partial slope. This rewriting is an interpretation of the estimated reduced form, not an independently estimated structural equation.

Without lag controls, Table 4 reports a slope of −0.05 with $t=-0.14$ for MOD1/SPEC1. Figure 3 reports a contemporaneous fitted-moment correlation of −2.6%. Both indicate a weak negative unconditional relation, statistically far from the strong negative or positive relation one might infer from a selected partial regression alone. Alternative mean/volatility specifications retain positive conditional slopes around 1.00–1.40 with $t$ statistics above four.

The two-stage least-squares version instruments current fitted volatility using $\mu_{t-1}$, $\mu_{t-2}$, $\sigma_{t-1}$, $\sigma_{t-2}$, $m_{t-1}$, and $VOL_{t-1}$. Table 4 row 13 reports current-volatility coefficient 2.22 ($t=4.86$), lag-volatility coefficient −2.15 ($t=-5.53$), and lag-mean coefficient 0.68. This checks sensitivity to contemporaneous regression endogeneity under the maintained instrument restrictions, but no separate weak-instrument or structural exclusion validation is supplied.

Omitting factors changes the picture. Using a $cay$-only fitted mean and the conventional volatility specification produces an unconditional slope −0.48 with $t=-2.54$. Its conditional slope is initially positive, 0.23, but becomes −0.10 and insignificant when lagged actual returns are added. This is the clearest evidence that the selected financial-factor information matters for the robustness of the inferred relation.

## Business-cycle behavior and the fitted Sharpe ratio

Figures 1–4 show fitted moments with NBER recession shading. Expected returns rise in all seven sample recessions and mostly range between approximately −4% and 8% per quarter, with some larger observations. Fitted volatility has substantial low-frequency variation and is high or rising in many recessions, but does not follow an identical cyclical pattern. The late-1990s divergence contributes to the weak unconditional correlation.

The ratio $\mu_t/\sigma_t$ is countercyclical, with marked spikes around the 1970–1971 and 1990–1991 recessions. It is a quarterly fitted-moment ratio, not an annualized realized Sharpe ratio of a traded strategy. Figure 4 also includes negative values. Because numerator and denominator are estimated, their ratio can amplify uncertainty; the paper does not provide a complete simultaneous confidence band for that ratio or an implementable leverage policy.

## Recursive out-of-sample experiment

The recursive test focuses on the two financial predictors $G_{1t}^2,G_{3t}$ for returns. It removes $cay$ both as a separate predictor and from the financial panel because its cointegrating coefficients were estimated over the full sample. Return forecasts are compared with a recursively estimated constant-mean benchmark. Volatility SPEC1 is compared with an AR(1) benchmark.

At each origin, reconstruct standardized panels and principal components using observations available through that origin, reestimate forecast regressions, and predict the next quarter. For a causally implemented forecast at origin $t$, the regression may include only pairs $(z_s,y_{s+1})$ for which $s+1\leq t$. The paper's shorthand about running regressions “through $t$” must be aligned with this outcome-availability constraint; otherwise the training set would include the very outcome being forecast. Factor estimates at the endpoint can use $X_t$ if that panel is assumed observed.

The source lists initial estimation periods ending in 1975Q1, 1985Q1, and 1995Q1, with first forecasts for the respective second quarters. Table 6 labels the forecast samples as beginning in the first quarters. It ends all forecast evaluations in 2003Q2, beyond the 2002Q4 endpoint described for the in-sample panels. Thus exact replication requires an extended dataset and a date convention clarifying whether table labels denote the first origin or first target.

The reported MSE ratios and encompassing statistics are:

| Initial-origin label | Return MSE ratio | Return ENC-NEW | Volatility MSE ratio | Volatility ENC-NEW |
|---|---:|---:|---:|---:|
| 1975Q1 | 0.918 | 11.56 | 0.902 | 16.58 |
| 1985Q1 | 0.911 | 7.69 | 0.821 | 9.75 |
| 1995Q1 | 0.786 | 5.97 | 0.706 | 10.04 |

All six encompassing tests are marked significant at 1% or better. The respective 95% asymptotic critical values are 2.79, 1.90, 1.03 for returns and 3.46, 4.35, 1.28 for volatility. The Clark–McCracken ENC-NEW null is that the restricted benchmark encompasses the larger model. It is a nested-forecast test, not a generic two-sided normal test of equal MSE.

The final-window ratios imply 21.4% lower return MSE and 29.4% lower volatility MSE. They do not mean equally large reductions in root-MSE; the corresponding root ratios are square roots of the displayed ratios. No transaction costs, turnover, or portfolio return is evaluated.

The recursive estimation is meaningful evidence beyond a purely in-sample regression, but its interpretation has limits. The predictor form was selected after examining the full historical sample; the exercise does not nest a completely new BIC search at every origin. The macro data are historical revised observations, not real-time vintages. Omitting $cay$ reduces one explicit source of look-ahead but does not convert revised macro-based volatility forecasts into a fully real-time experiment. Table 6's volatility footnote also prints $VOL_{t-1}$ where the main SPEC1 definition uses $VOL_t$ to predict $VOL_{t+1}$; the main model and figure description support the latter convention.

## Bootstrap inference

The first bootstrap treats the estimated factors as observed regressors. Fit separate AR(1) models to conditioning variables, preserve their cross-sectional residual dependence by resampling residual vectors, initialize with observed starting values, and generate synthetic regressor paths. Outcomes are then generated either under a no-predictability null, by resampling deviations from an unconditional mean, or under the fitted predictive model, by resampling its residuals. Refit the forecasting regression in each of 10,000 replications.

The second bootstrap additionally reestimates factors. Decompose the standardized panel into $\widehat\Lambda\widehat F'+\widehat E$, fit an AR(1) to each idiosyncratic residual series, resample innovation vectors across dates, and generate $\widetilde E$. Add these simulated residuals to the fitted common component, producing a new panel, and rerun PCA. Other observed predictors are bootstrapped through their AR(1) models. Outcomes are generated under the fitted alternative or the no-predictability null and regressions are reestimated.

This second procedure perturbs the panel's residual component around its fitted common path; it is not a fully unrestricted bootstrap of every structural feature of the latent factor process. In the volatility equation, lagged dependent variables require recursive outcome generation with additive resampled disturbances. A garbled expression in Table 7's note should not be interpreted as multiplying the lagged outcome by the residual. Neither procedure explicitly reruns the complete nonlinear model-selection search, so the confidence intervals are conditional on the selected specification rather than comprehensive post-selection intervals.

Table 8 gives 95% alternative-bootstrap intervals of [0.004,0.017] for the squared-factor coefficient, [0.007,0.032] for the third-factor coefficient, and [0.802,2.835] for $cay$. The adjusted return $R^2$ interval is [0.060,0.284], while under the no-predictability null it is [−0.017,0.039]. For volatility, the adjusted $R^2$ interval is [0.189,0.702] under the alternative versus [−0.021,0.044] under the null. The wide alternative interval makes clear that forecast strength is not estimated with great precision even though the null fit is much smaller.

The Wald statistic for joint insignificance of the two financial predictors is 16.87. Its null-bootstrap 95% interval is [0.052,7.651] in Table 8; the prose rounds or misprints the lower endpoint as 0.52. The table is the reference for this numerical value. Bootstrap support concerns the underlying mean and volatility regressions. It should not be described as a complete joint-pipeline correction for every generated-moment risk–return slope in Table 4.

## Information timing robustness and remaining limits

Appendix A.2 reextracts financial factors without $cay$, lags macro predictors by another quarter, and constructs a version using only financial variables. The pure-financial factors alone yield adjusted return fit around 0.08; adding current $cay$ gives 0.15, and using its extra lag gives 0.14. The extra-lag real macro factor has a $t$ statistic about 1.80 and $p\approx0.074$, losing 5% significance while retaining 10% significance.

The risk–return partial slope remains positive in these checks. Table A3 reports values 1.35, 1.07, and 1.15 for its three versions, with statistics 4.62, 4.86, and 5.50. The wholly financial version therefore preserves the qualitative sign without requiring contemporaneously released macro observations. It does not prove that the information set is complete or that the relationship is invariant to every alternative specification.

Exact reproduction still needs the original panel and release/aggregation conventions, resolution of the inconsistent financial dimension, the extended observations through 2003Q2, the Newey–West bandwidth, PCA sign alignment rules, and the complete candidate-model list. The source supplies detailed macro transformations and many financial definitions, but it does not supply these missing choices with sufficient precision to claim a bit-for-bit replication.

The useful research lesson is to estimate mean and risk using broad information, inspect the timing of both, and distinguish unconditional association from a partial relation after lag controls. The paper provides evidence that a few financial components and a real-activity component improve those estimates in this sample. It does not establish a universal structural risk-aversion parameter, an unbiased forecast of conditional standard deviation, or a cost-adjusted market-timing strategy.
