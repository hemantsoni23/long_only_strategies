# Correlations and Volatilities of Asynchronous Data

**Patrick Burns, Robert Engle, and Joseph Mezrich (1998).** UC San Diego Discussion Paper 97-30R, April 1998 cover, March 1998 manuscript date. Source: [original PDF](../../Finance/VolatilityAsynchronous_BurnsEngleMezrich_1998.pdf), all 17 pages including formulas, diagnostic tables, figures, and references. This is the supplied working-paper version. Printed page numbers are one less than PDF page numbers. The separate 1997 appendix containing the detailed covariance parameterization is not included; the local alternative filename contains the same 17-page version.

## Why this matters

A portfolio combining Tokyo, European, and New York stocks is commonly valued using each market's most recent closing price. Those prices describe different instants. A New York afternoon shock belongs to today's U.S. return but tomorrow's European or Japanese return. Combining them as simultaneous observations creates artificial lead-lag predictability, attenuates many measured contemporaneous correlations, and changes short-horizon portfolio risk. The apparent diversification benefit can partly be a timing artifact.

The paper's contribution is to estimate all asset values at a common information time, including assets whose markets have already closed. It calls the resulting log-price estimates synchronized prices and their changes synchronized returns. A vector moving-average model captures the reassignment of news across accounting days; a multivariate GARCH model describes the changing innovation covariance. The framework delivers both common-time risk and the risk of returns actually recorded at disparate closing times.

Synchronization here is a statistical mark, not a new tradable closing price. Knowing that New York news predicts tomorrow's London opening does not imply a strategy can buy London at its already unavailable closing price. The paper's ADR example makes the distinction concrete: a long New York ADR and short matching Tokyo stock can show spurious accounting P&L as the markets update in sequence, even when their contemporaneous economic values closely offset. Execution at different times still creates risk when establishing or unwinding the hedge.

This is primarily a valuation and covariance-estimation paper. It does not report realized trading profits, optimal portfolio performance, transaction costs, or an out-of-sample VaR backtest. Its empirical evidence demonstrates substantial changes in estimated correlations and volatilities and assesses in-sample residual diagnostics. Those are useful findings but should not be inflated into proof of a universally accurate risk engine.

## Information times and what is being estimated

Let $t$ denote a common daily reference time, typically the New York close, and $t_j\le t$ the most recent recorded close for market $j$. Let $\mathcal I_t$ contain all recorded prices observed by that reference time. The synchronized log-price is defined as

$$
\widehat p_t^j=E[\log S_t^j\mid\mathcal I_t].
$$

If market $j$ is observed at $t$, the estimate equals its observed log-price. For an earlier closing market, prices subsequently observed elsewhere help estimate its unobserved current value. Under the maintained assumption that changes after the common-time value are unpredictable, the same conditional log-price is the expectation of the next recorded log-price:

$$
\widehat p_t^j=E[\log S_{t_j+1}^j\mid\mathcal I_t].
$$

This equality depends on the absence of an intervening predictable drift or appropriate removal of that drift. It is not a statement that the next realized price will equal today's estimate. The remaining conditional variance describes uncertainty until the next observation, which matters for an asynchronous hedge unwind.

The paper's unbiasedness language concerns logarithms. In general, $\exp(E_t[\log S])\ne E_t[S]$. If conditional log-price uncertainty is Gaussian with variance $v$, the level-price conditional mean would instead include the factor $\exp(v/2)$. This Jensen correction is a mathematical qualification of using log-price forecasts for level-valued portfolios; the manuscript does not implement a detailed level-price valuation adjustment. Likewise, a weighted sum of asset log returns approximates a portfolio simple return only under the usual small-return or continuously rebalanced interpretation.

The introduction illustrates a four-hour gap between the London and New York closes and a roughly 17.5-hour interval between a New York close and the following opening. These are the historical examples used to motivate timing, not a complete date-specific trading-hours database. A faithful data reconstruction must handle local holidays and daylight-saving differences. The paper does not provide those calendars or a comprehensive treatment of days when only some markets trade.

## The vector moving-average representation

Collect close-to-close accounting log returns into a $J$-vector $R_t$, ordered consistently across matrices. The model, equation (5), is

$$
R_t=\epsilon_t+M\epsilon_{t-1},
\qquad E_{t-1}[\epsilon_t]=0,
\qquad \operatorname{Var}_{t-1}(\epsilon_t)=H_t.
$$

The vector MA(1) is motivated by markets whose daily closing times are separated by less than one day: news is reassigned between adjacent accounting returns. Serially uncorrelated innovations need not be contemporaneously uncorrelated, and their covariance can be time-varying. $M$ is a matrix of lagged innovation effects, not a regression matrix on raw lagged returns.

That distinction is essential for implementation. Given parameters and an initial innovation, filter recursively with $\epsilon_t=R_t-M\epsilon_{t-1}$. Regressing $R_t$ directly on $R_{t-1}$ and calling the coefficient $M$ estimates a different model. Stable recovery of innovations generally requires an invertible MA representation and a controlled initialization. The paper does not give a burn-in rule or the initialization used in likelihood estimation.

Closing order suggests restrictions but does not generally make $M$ triangular in an arbitrary ordering. The authors emphasize that timing restrictions on first-order return correlations do not translate mechanically into corresponding coefficient zeros when innovations are correlated. In an ideal efficiently priced last-closing market, its row of $M$ is zero. Empirically, serial correlation within some index series motivates diagonal coefficients as well, possibly reflecting stale constituent prices.

The synchronized mark adds the predictable next accounting return to the observed log-price. Consequently,

$$
\widehat p_t=p_t+M\epsilon_t,
\qquad
\widehat R_t=\widehat p_t-\widehat p_{t-1}
=R_t+M\epsilon_t-M\epsilon_{t-1}
=(I+M)\epsilon_t.
$$

The adjustment transfers a news effect between dates. Summing over a sample yields

$$
\sum_{t=1}^T(\widehat R_t-R_t)=M(\epsilon_T-\epsilon_0).
$$

Thus sample mean differences are boundary terms divided by sample length. They need not be exactly zero in finite samples, but they do not accumulate like a permanent change in expected return. This telescoping identity is more precise than treating synchronization as an alpha adjustment.

Conditional synchronized covariance is

$$
C_t^{sync}=(I+M)H_t(I+M)'.
$$

It is positive semidefinite when $H_t$ is positive semidefinite. Strict positive definiteness additionally requires $I+M$ to be nonsingular, a qualification not spelled out when the article attributes it solely to positive-definite $H_t$. The fitted sparse matrix is not near the obvious singular case, but the general mathematical condition matters for a reusable implementation.

## Unconditional covariance and the long-horizon connection

Let $\Omega=E[\epsilon_t\epsilon_t']$ under covariance stationarity. The accounting contemporaneous and lag-one covariance matrices are

$$
\Gamma_0=\Omega+M\Omega M',\qquad
\Gamma_1=E[R_tR_{t-1}']=M\Omega.
$$

The synchronized covariance satisfies

$$
\Gamma^{sync}=(I+M)\Omega(I+M)'
=\Gamma_0+\Gamma_1+\Gamma_1'.
$$

This is a multivariate version of correcting nonsynchronous observations using lead-lag covariance. A direct sample estimator uses the average of $R_tR_t'+R_tR_{t-1}'+R_{t-1}R_t'$, with appropriate centering if nonzero means are modeled. Unlike a Gram matrix, this lag-corrected estimate is not guaranteed positive semidefinite in a finite sample. A covariance matrix suitable for portfolio optimization therefore needs either the model-based construction or an explicitly documented regularization step.

The adjustment does not necessarily increase every variance or covariance. Its difference from accounting covariance is $M\Omega+\Omega M'$, which can be indefinite. The paper's empirical tendency toward higher volatilities and correlations reflects the signs of the fitted lead-lag effects; it is not a matrix-order theorem valid for arbitrary MA coefficients. This also explains why a corrected hedge need not always require a larger position even though many observed cross-country correlations rise.

For $k$ future synchronized returns, martingale-difference orthogonality removes conditional cross-time covariance. Define $H_{t+j|t}=E_t[H_{t+j}]$. Then equation (10) gives

$$
C^{sync}_{t,k}=(I+M)\left(\sum_{j=1}^kH_{t+j|t}\right)(I+M)'.
$$

For accounting returns, the known $M\epsilon_t$ contributes to the conditional mean rather than forecast variance. Summing the MA representation gives

$$
\sum_{j=1}^kR_{t+j}
=M\epsilon_t+(I+M)\sum_{j=1}^{k-1}\epsilon_{t+j}+\epsilon_{t+k},
$$

and hence

$$
C^{acc}_{t,k}=H_{t+k|t}
+(I+M)\left(\sum_{j=1}^{k-1}H_{t+j|t}\right)(I+M)'.
$$

The two covariance forecasts differ only in how the final day's still-unrecorded news is treated. Their difference per day generally becomes small as the horizon grows under bounded/stationary forecast variances. Equality at every finite horizon does not follow. The printed equation (12) has $k-1$ on the upper limit of its left-hand return sum, inconsistent with its right-hand terminal $H_{t+k|t}$ and the preceding two-day example. The formula above uses the consistent $k$-day sum and derives it explicitly.

For a fixed portfolio-weight vector $w$, forecast variance is $w'C_{t,k}w$ and correlation is $C_{ij}/\sqrt{C_{ii}C_{jj}}$. Correlation of a multiday aggregate must be formed after summing the covariance matrices, not by averaging daily correlations. A Gaussian VaR quantile would additionally impose a distributional assumption; the paper's covariance formulas alone do not determine arbitrary tail quantiles.

## Fitted return matrix and its orientation

The application uses seven indices ordered CAC, DAX, FTSE, Milan, Nikkei, S&P 500, and Toronto. Equation (13) displays $M'$, deliberately so that a row identifies the predicting market and a column the predicted market. Transposing that displayed matrix incorrectly is a substantial replication error. Its reported nonzero elements are summarized below in the displayed, predictor-to-response orientation.

| Predictor innovation | Predicted accounting return | Coefficient |
|---|---|---:|
| CAC | DAX, Milan, Nikkei | .08, .09, .07 |
| FTSE | DAX, Milan, Nikkei | .11, .08, .10 |
| Milan | Milan | .21 |
| Nikkei | CAC, DAX, FTSE | −.01, −.05, −.03 |
| S&P 500 | CAC, DAX, FTSE, Milan, Nikkei | .29, .49, .28, .27, .28 |
| Toronto | Toronto | .21 |

All remaining displayed entries are zero. There are sixteen nonzero MA coefficients. The S&P row of $M$ itself is zero, although the S&P row of the displayed transpose has the largest predictive coefficients. All coefficients have reported $t$ ratios above three except the three negative Nikkei effects and the CAC-to-Nikkei coefficient .07. Complete individual standard errors are not printed here.

The Nikkei negative coefficients warrant interpretation as estimated residual dynamics, not a reversal of clock time. They are small and statistically weaker. Milan and Toronto's .21 diagonal coefficients show that a timing model of cross-market closures alone is not the full empirical story: stale index components and other own-return predictability can matter. The authors acknowledge that the selected MA structure could be enriched based on remaining residual dependence.

## Covariance dynamics and a material source limitation

The covariance model is described as a component-form BEKK-type multivariate GARCH with leverage terms. $Q_t$ is the permanent component, $H_t-Q_t$ the transitory component, and $\eta_t=\min(\epsilon_t,0)$ componentwise. There are three component matrix terms, $K=3$, with all matrices seven by seven. Eighty covariance parameters plus sixteen MA parameters are estimated, for 96 total.

The rendered equation (14) is problematic as a complete recursion. In the notation printed in the PDF, its first line is

$$
H_t=\sum_{k=1}^K\left\{
A_k'[\epsilon_{t-1}\epsilon_{t-1}'-Q_t]A_k
+B_k'[H_{t-1}-Q_t]B_k
+C_k'[\eta_{t-1}\eta_{t-1}'-\tfrac12Q_{t-1}]C_k
\right\},
$$

and its second line is

$$
Q_t=\sum_{k=1}^K\left\{
R_k'[Q_{t-1}-\widehat\Omega]R_k
+F_k'[\epsilon_{t-1}\epsilon_{t-1}'-H_t]F_k
\right\}.
$$

These lines lack the level terms ordinarily needed to define the named permanent and transitory components, and the second includes contemporaneous $H_t$ on its right-hand side. For example, setting all coefficient matrices to zero gives $H_t=Q_t=0$, not a positive unconditional covariance. The displayed formulas therefore cannot simply be treated as an ordinary, fully specified positive-definite GARCH recursion. This note records the source faithfully rather than silently adding constants, replacing indices, or inventing a repaired fitted model.

The paper refers the nonzero covariance restrictions, coefficient estimates, standard errors, and $t$ ratios to the appendix of Burns, Engle, and Mezrich (1997). That appendix is absent from both local 17-page copies. Even if one supplied a plausible conventional component-GARCH correction, it would not identify the authors' 80-parameter sparse specification. Reproducing their exact dynamic covariance figures consequently requires that additional source or original code. The synchronization algebra and unconditional comparisons remain reproducible independently of this missing specification.

The stated estimation criterion, equation (15), is Gaussian conditional log likelihood up to constants:

$$
\ell=-\frac12\sum_t\{\log|H_t|+\epsilon_t'H_t^{-1}\epsilon_t\}.
$$

The paper says an efficient genetic algorithm maximizes it, but supplies no population size, mutation/crossover settings, numerical tolerances, initialization, or boundary constraints. A practical implementation should use Cholesky solves instead of explicit inverses, reject nonpositive covariance candidates, verify MA invertibility, and use multiple starts. Those are numerical safeguards implied by the problem, not reported settings of the original exercise.

## Empirical design and numerical evidence

The fitted G7 model uses July 1987–October 1996, deliberately retaining the 1987 crash because it contains important correlation information. Most descriptive comparisons use January 2, 1990–October 3, 1996. The paper does not identify a downloadable vendor series, exact index versions, dividend treatment, currency conversion, complete alignment rules, or observation counts. One should not assume all indices are dollar-denominated total-return series merely because they are combined in an international application.

Tables I, II, and IV compare ordinary daily correlations, five-trading-day correlations, and synchronized daily correlations. Weekly returns reduce the fractional importance of closing-time differences but do not eliminate them. Their agreement with synchronized estimates is a useful diagnostic rather than an independent observed truth for same-time daily covariance.

| Pair | Accounting daily | Five-day | Synchronized daily |
|---|---:|---:|---:|
| S&P–Nikkei | .146 | .298 | .298 |
| S&P–FTSE | .330 | .495 | .530 |
| S&P–DAX | .248 | .408 | .482 |
| S&P–CAC | .286 | .447 | .441 |
| CAC–DAX | .597 | .663 | .703 |
| Milan–FTSE | .273 | .373 | .381 |
| S&P–Toronto | .557 | .634 | .565 |

The S&P–Toronto comparison is an informative exception: synchronized daily correlation is only slightly above ordinary daily correlation, while weekly correlation is appreciably higher. Synchronization is not an operation forcing every daily correlation to equal a weekly estimate. Differences can arise from dynamics, finite-sample variation, and remaining model limitations.

Table III supports the timing mechanism through lagged correlations. Previous S&P returns correlate .208 with current CAC, .306 with DAX, .267 with FTSE, .246 with Milan, and .223 with Nikkei. Own lagged correlations are .201 for Milan and .260 for Toronto. The matrix orientation is again predictor rows and response columns. These values describe observable lead-lag associations; they do not demonstrate available execution prices at the lagged market's close.

Table V shows almost unchanged annualized means but altered annualized volatilities. CAC volatility rises from 17.49% to 18.23%, DAX from 16.80% to 18.76%, FTSE from 12.42% to 13.16%, Milan from 18.47% to 22.50%, Nikkei from 23.14% to 23.87%, and Toronto from 8.54% to 9.97%. S&P remains 11.35%, consistent with its zero synchronized adjustment as the reference market. Milan's increase is about 21.8% in relative standard-deviation terms, so describing every change as economically negligible would be misleading.

The means change by at most a few hundredths of an annual percentage point in this table. For example, DAX moves from 5.75% to 5.73% and Nikkei from −8.59% to −8.61%. These small boundary differences accord with the telescoping identity. They do not establish unbiased level-price forecasts or prove that model estimation error is zero.

Figures 1–2 display conditional correlation term structures and thirty-day constant-horizon series. At the final date, October 3, 1996, Milan correlations with FTSE and S&P rise from short-horizon values toward long-run levels; the FTSE curve overshoots before reverting. Over the full estimation period, thirty-day DAX–Milan correlations range roughly .25–.60, while DAX–S&P is generally around .40–.60 apart from the crash period. These are plotted approximate ranges, not precise extrema supplied in a data table.


## Two-market derivation and an implementation check

A two-market specialization makes the timing adjustment concrete. Let market E close early and market L close late, with only the late-market innovation predicting the next early-market accounting return. In that ordering set

$$
M=\begin{pmatrix}0&m\\0&0\end{pmatrix},
\qquad
\Omega=\begin{pmatrix}v_E&c\\c&v_L\end{pmatrix}.
$$

This is an illustrative restriction of the model, not a separately fitted result. The accounting covariance is

$$
\Gamma_0=\begin{pmatrix}v_E+m^2v_L&c\\c&v_L\end{pmatrix},
$$

whereas synchronization gives

$$
\Gamma^{sync}=\begin{pmatrix}v_E+2mc+m^2v_L&c+mv_L\\c+mv_L&v_L\end{pmatrix}.
$$

The late market is unchanged because it already closes at the reference time. The early-market covariance with the late market receives the omitted $mv_L$ term, but its own variance changes by $2mc$. If contemporaneous innovation covariance is zero, synchronization can raise cross-market correlation without changing either marginal variance. If $c$ is negative, early-market variance can fall. These cases isolate the algebraic mechanism behind the more complex empirical table and show why “stale prices always understate every variance” is too strong.

The example also clarifies a hedge calculation. For a unit long position in E hedged with $h$ units short L, minimizing contemporaneous variance gives $h^*=C_{EL}/C_{LL}$. The accounting estimate is $c/v_L$ in this example, while synchronized risk gives $c/v_L+m$. This difference is a common-time risk correction, not proof that the correction can be executed at both observed closes. If the intended liquidation time is asynchronous, use the appropriate accounting-horizon covariance instead of applying the synchronized coefficient mechanically.

For a software check, simulate mean-zero innovations with a known positive-definite $\Omega$, generate the MA returns, and recover synchronized returns from both $(I+M)\epsilon_t$ and the difference of corrected log marks. They should agree to numerical precision. The sample cumulative-return discrepancy should equal $M(\epsilon_T-\epsilon_0)$ exactly for the same initialized innovation path. A large persistent discrepancy indicates a time-index or transpose error rather than sampling uncertainty.

Next compare empirical covariances with the two analytical matrices. The direct lag-covariance correction should approach the synchronized matrix as the simulated sample grows, while a finite-sample corrected matrix can still have a negative eigenvalue. That is a property of the direct estimator, not a reason to alter the theoretical identity. A PSD projection applied to a finite-sample matrix should be recorded separately from the original lag correction.

In actual data, distinguish a market holiday from an observed zero return. Carrying forward a closed market's price and treating it as a fresh synchronized observation can artificially depress its variance and create extra lags. The one-lag timing approximation is most natural when all relevant information delays remain within an ordinary trading day. Multi-day closures can require richer observation timing or a larger state representation; the supplied paper does not estimate that extension.

Finally, parameter estimation uncertainty is absent from the simple covariance transformations. Conditional on fitted $M$ and $H$, the formulas are exact within the model, but uncertainty about those fitted objects remains. The weak Nikkei coefficients, covariance-model selection, and missing parameter restrictions matter when comparing portfolios with small apparent risk differences. The paper's residual checks do not quantify that additional source of uncertainty, and its displayed transformed correlations should not be read as error-free measurements of an observable common-time price process.

## Diagnostics, uncertainty, and implementation scope

Standardized innovations are $\widetilde\epsilon_t=H_t^{-1/2}\epsilon_t$. A correct conditional mean/covariance specification implies mean zero and identity conditional covariance, but the matrix square-root convention must be fixed because componentwise diagnostics can depend on its orientation. The paper does not specify whether its implementation used a symmetric or triangular whitening transformation.

Table VI.a's diagonal sample covariance entries range from 0.969820 for DAX to 1.032501 for Toronto. The largest displayed off-diagonal magnitudes are around .06. The identity test is $\chi^2=41.85$ on 28 degrees of freedom, with $p=.0448$. Although the authors call the matrix close to identity, the joint null is rejected at 5%. Numerical closeness and formal nonrejection are different assertions.

The dynamic tests use rank autocorrelations and cross-correlations with 15 lags, motivated as more robust to outliers than ordinary correlation tests. A reference 5% critical value is approximately 25. Table VI.b has five of 49 level-residual entries above this threshold, including S&P-to-DAX 44.07 and CAC-to-FTSE 41.56. Table VI.c has six of 49 squared-residual entries above it, indicating residual variance predictability; DAX-to-Toronto is 34.313 and DAX-to-S&P 30.89. Table VI.d has four of 49 leverage entries above the threshold, including CAC-to-DAX 29.215 and CAC-to-Milan 28.44.

Table VI.e tests autocorrelation of cross-products of standardized residuals. The Nikkei–CAC entry is 34.3772 and CAC–S&P 25.1769, so both exceed the stated cutoff. Directly counting the displayed dynamic tables gives 5+6+4+2=17 exceedances among 49+49+49+21=168 entries. The prose instead says 16 of 169. This is a minor reporting inconsistency, but the exact aggregate claim should not be repeated as if verified.

The model was selected by examining these same diagnostics. Consequently, nominal test sizes after specification search are uncertain, a limitation the authors explicitly acknowledge. Multiple related tests also mean individual rejections require context. More importantly, all these results are in-sample: no chronological held-out parameter estimation and forecast evaluation is reported. A modern risk implementation should separately assess residual calibration and portfolio loss forecasts on data unavailable during specification selection.

A reproduction can start with the fully specified MA synchronization layer: align historical close times, order assets, filter innovations, apply the displayed transposed matrix correctly, and verify the boundary identity and Table IV–V comparisons. Exact replication of the dynamic 96-parameter model must wait for the missing covariance appendix and correction of equation (14). Using a different positive-definite covariance model is a legitimate extension if labeled as such. The broad takeaway survives that limitation: stale closing marks mix different information sets, and common-time valuation requires both an estimate of unobserved current values and an honest accounting of the uncertainty that remains until markets reopen.
