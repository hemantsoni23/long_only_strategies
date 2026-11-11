# A Comprehensive Look at the Empirical Performance of Equity Premium Prediction

Ivo Welch and Amit Goyal. *Review of Financial Studies* 21(4), 2008, 1455–1508; advance access March 17, 2007, DOI 10.1093/rfs/hhm014. Source: [EquityPremium_WelchGoyal_2007.pdf](../../Finance/EquityPremium_WelchGoyal_2007.pdf), 54 pages. This note covers the complete published article, including all tables, plotted prediction-error paths, alternative estimators, and encompassing tests. Page pointers use printed journal pagination. Statements about recent performance refer to the paper's historical endpoint, principally 2005, not to current markets.

## Why this matters and what is new

The central contribution is a common empirical audit of many proposed equity-premium predictors. Earlier studies used different samples, data definitions, horizons, and benchmarks, making apparently conflicting conclusions difficult to interpret. Welch and Goyal put prominent predictors through the same forecast experiment and compare them with a difficult, implementable benchmark: the expanding historical average premium known at the forecast date.

The result is primarily a warning about model stability and experimental design. Most annual and shorter-horizon forecasting models fail to improve on that benchmark, often after looking convincing in sample. Many favorable historical results depend heavily on the 1973–1975 oil-shock period, while the subsequent three decades contribute little or negative forecasting performance. A few long-horizon results remain promising, and the authors reserve judgment on some issuance evidence. Their conclusion is not a theorem that expected returns are constant or that no predictor can ever work.

The paper distinguishes a variable's economic association with returns from its usefulness to a forecaster. An ex-post estimated relation may document corporate financing behavior without supplying a real-time market-timing rule. Likewise, statistically detectable predictability can be too weak to overcome coefficient-estimation noise. Conversely, a small reduction in monthly forecast error can have economic value, but the value depends on portfolio constraints, risk aversion, information availability, and trading costs.

## Forecasting model and benchmark

The baseline one-period forecasting regression is

$$
y_t=\alpha+\beta x_{t-1}+u_t,
$$

where $y_t$ is the equity premium and $x_{t-1}$ is a lagged predictor. Multivariate variants replace the scalar regressor with a vector. In-sample estimates use the whole specified sample. For an out-of-sample forecast, fit the regression using only observations available before the return to be predicted:

$$
\hat y^A_t=\hat\alpha_{t-1}+\hat\beta_{t-1}x_{t-1},
\qquad
\hat y^N_t=\frac{1}{n_{t-1}}\sum_{s\leq t-1}y_s.
$$

$A$ denotes the predictive alternative and $N$ the historical-mean null. Both learn recursively from the expanding history. The paper often calls these “rolling” estimates, but the baseline experiment is not a fixed-length rolling window that discards old observations. Both forecasts must use the same available return history for a fair comparison.

Three sample conventions are explored: begin forecasting twenty years after data become available; begin in 1965 or twenty years after availability, whichever is later; and exclude all observations before 1927 even from estimation. The initial twenty years belong to model estimation, not forecast evaluation. Predictor availability varies, so the evaluation start cannot be identical for every series.

For a five-year target, only fully realized historical five-year returns can enter an estimate at a forecast origin. Future outcomes overlapping the origin must not be treated as already known. The article identifies overlap in its inference and uses five-year cumulative premia; its prose does not enumerate every indexing convention in executable detail, so a reconstruction should explicitly document origin dates and last observable target endpoints rather than infer them from a generic one-step loop.

## Return data and predictor construction

The annual equity premium uses S&P 500 total returns including dividends, with continuously compounded returns in the baseline analyses, less the short-term rate. CRSP supplies month-end data for 1926–2005. Shiller data extend annual and longer-horizon analysis to 1871; reliable monthly total-return analysis begins in the CRSP era, with forecasts based on data from 1927 onward. Most monthly Campbell–Thompson comparisons instead use simple returns to match that study, so their results should not be combined mechanically with the log-return columns.

Before short-term Treasury debt is available, the paper imputes the short rate from commercial paper. A regression estimated over 1920–1971 is

$$
\widehat{\text{T-bill rate}}=-0.004+0.886\,\text{commercial-paper rate},
$$

with $R^2=95.7\%$. This equation is used for 1871–1919. Over the overlap period, actual-rate and imputed-rate equity premia correlate 99.8%. Nevertheless, the early benchmark incorporates a retrospectively estimated rate proxy, rather than an observed riskless investment available throughout the nineteenth century.

Annual mean premium and standard deviation are 4.85% and 17.79% for 1872–2005, 6.04% and 19.17% for 1927–2005, and 4.03% and 15.70% for 1965–2005. These are descriptive sample statistics, not assumed constant true parameters.

The main predictors and their constructions are as follows.

| Predictor | Construction and source detail |
|---|---|
| $d/p$ | Log of trailing twelve-month S&P dividends minus log of current price. Dividends come from Shiller through 1987 and S&P thereafter. |
| $d/y$ | Log trailing dividends minus log of lagged price; this differs from $d/p$ through the denominator timing. |
| $e/p$ | Log trailing twelve-month earnings minus log price. Post-1987 monthly earnings are interpolated from S&P quarterly earnings. |
| $d/e$ | Log dividends minus log earnings. |
| $svar$ | Sum of squared daily S&P returns; historical daily data from Schwert, then CRSP. |
| $csp$ | Relative valuation measure of high- versus low-beta stocks from Polk–Thompson–Vuolteenaho; supplied series runs May 1937–December 2002. |
| $b/m$ | Dow Jones Industrial Average book-to-market from Value Line. March–December uses prior-year-end book value; January–February uses book value from two year-ends earlier, divided by current price. |
| $ntis$ | Trailing twelve-month net equity issuance relative to aggregate NYSE capitalization. |
| $eqis$ | Equity issuance divided by total equity-plus-debt issuance, from Baker–Wurgler, extended by the authors for 2005. |
| $tbl$ | Short Treasury yield, using historical NBER data before the FRED three-month secondary-market series. |
| $lty$, $ltr$ | Long government-bond yield and return, from historical NBER and Ibbotson data as specified in Section 1. |
| $tms$ | Long government yield minus Treasury-bill rate. |
| $dfy$ | Baa corporate yield minus Aaa yield. |
| $dfr$ | Long corporate-bond return minus long government-bond return. |
| $infl$ | CPI inflation; monthly use waits an additional month because the information is released afterward. |
| $i/k$ | Aggregate private nonresidential fixed investment divided by aggregate capital, supplied by Cochrane. |

The net-issuance calculation is important enough to preserve explicitly:

$$
\operatorname{NetIssue}_t=\operatorname{Mcap}_t
 -\operatorname{Mcap}_{t-1}(1+\operatorname{vwretx}_t).
$$

The capitalization and ex-dividend value-weighted return refer to NYSE stocks. The source notes that this accounting implicitly treats a delisting return as −100%; using actual delisting returns where available or ignoring delistings does not materially alter its conclusions. The empirical variable is related to, but not identical with, every later total-payout-yield measure. A replication should not silently replace it with a contemporary database field having a similar name.

The article provides these operational definitions but not every raw-data cleaning rule. Its interpolated earnings series, capitalization conventions, exact economic-data vintages, and externally supplied $csp$, $eqis$, and $i/k$ files remain required inputs. Recreating a series from current revised data is a new data vintage, even if the variable label is unchanged.

## Generated predictors, model selection, and information leakage

The consumption–wealth–income ratio is a generated regressor. For log consumption $c$, wealth $a$, and income $z$, its construction estimates a cointegrating equation augmented with leads and lags of differences:

$$
c_t=\alpha+\beta_a a_t+\beta_z z_t
 +\sum_{i=-k}^{k}b_{a,i}\Delta a_{t-i}
 +\sum_{i=-k}^{k}b_{z,i}\Delta z_{t-i}+\epsilon_t.
$$

The fitted ratio is $cay_t=c_t-\hat\beta_a a_t-\hat\beta_z z_t$. Quarterly estimation uses $k=8$ and annual estimation $k=2$. Available quarterly ingredients span 1952Q2–2005Q4; the authors reconstruct annual data to extend the annual series to 1945–2005.

Two versions distinguish different information sets. $cayp$ uses full-sample construction coefficients but recursively estimates the subsequent forecasting regression. It therefore retains future information in the predictor itself. $caya$ reestimates the construction using data only through the current origin $s$, with estimation rows ending at $s-k$ so that the lead terms do not pass beyond available data. It then forms the current ratio with those estimated coefficients. Reestimating only the final forecasting regression is insufficient to make a generated regressor genuinely recursive.

The “kitchen sink” fits the available ordinary predictors jointly, excluding $cay$. The “model selection” procedure considers all $2^K$ subsets of its candidate variables and selects, at each origin, the model with the lowest accumulated prediction error up to that date. It is a sequential forecast-error selection rule rather than a one-time full-sample best-subset regression. Exact treatment of collinear combinations, incomplete series, ties, and initialization is not spelled out as code in the article. A literal reproduction requires the accompanying dataset and implementation conventions.

The monthly $cay3$ variant uses the three ingredients directly in the return forecast rather than imposing the estimated cointegrating combination. Its estimated predictive coefficients need not resemble the cointegrating coefficients. The paper treats this as a distinct model and tests the consequences of delays in public availability.

## Forecast accuracy, significance, and a printed formula defect

Let $e^N_t=y_t-\hat y^N_t$ and $e^A_t=y_t-\hat y^A_t$. Unadjusted out-of-sample fit and the RMSE gain are

$$
R^2_{\rm OOS}=1-\frac{\operatorname{MSE}_A}{\operatorname{MSE}_N},
\qquad
\Delta\operatorname{RMSE}=\sqrt{\operatorname{MSE}_N}-\sqrt{\operatorname{MSE}_A}.
$$

Positive values mean the predictive model improves on the historical mean. Negative $R^2$ is entirely meaningful outside a fitted-sample projection: the alternative forecasts worse than the benchmark.

The tables generally report degrees-of-freedom-adjusted $\bar R^2$, which can be negative even when raw MSE improves slightly. The printed adjustment in equation (6), p. 1461, is defective: taken literally, it subtracts nearly $1-R^2$ and would turn a tiny positive raw fit into a number near −1. That is inconsistent with the article's own examples. The conventional adjustment consistent with those examples is

$$
\bar R^2=1-(1-R^2)\frac{T-1}{T-k}
 =R^2-(1-R^2)\frac{k-1}{T-k},
$$

where $k$ counts estimated coefficients including the intercept. This is a mathematical correction for implementation, not a claim that the printed equation says it. The source's example of $cay3$, raw fit around 0.0040 becoming adjusted fit −0.0034 after three extra degrees of freedom, supports this interpretation. Preserve raw MSEs in a replication so the unambiguous economic comparison remains available regardless of reporting convention.

For overlap order $h$, the MSE-F statistic is

$$
\operatorname{MSE\!F}=(T-h+1)
 \frac{\operatorname{MSE}_N-\operatorname{MSE}_A}{\operatorname{MSE}_A}.
$$

Here $h=1$ for nonoverlapping one-period targets. Forecast encompassing uses

$$
\operatorname{ENC}=\frac{T-h+1}{T}
 \frac{\sum_{t=1}^T[(e^N_t)^2-e^N_t e^A_t]}{\operatorname{MSE}_A}.
$$

The benchmark is nested in the predictive model, so standard nonnested forecast-comparison distributions are inappropriate under the null. The paper uses bootstrap critical values for most specifications, with one-sided out-of-sample tests and two-sided in-sample tests. Stars indicate 90%, 95%, and 99% levels. A significant negative adjusted fit can coexist with a positive raw improvement or with a test that detects a nonzero predictive coefficient after accounting for estimation noise; significance is not itself proof of economically useful forecasting.

## Bootstrap and diagnostic design

For each scalar predictor, the null data-generating system is

$$
y_{t+1}=\alpha+u_{1,t+1},\qquad
x_{t+1}=\mu+\rho x_t+u_{2,t+1}.
$$

Power simulations add the fitted term $\beta x_t$ to the return equation. Full-sample OLS estimates provide the model parameters and paired residuals. Draw the residual pair together with replacement, preserving contemporaneous correlation between return innovations and predictor innovations. Recursively generate the predictor using its autoregressive coefficient. Select an initial observation from a randomly chosen actual date. The paper uses 10,000 bootstrap series and repeats the relevant estimation and forecast procedure on each.

Drawing predictor and return residuals separately would destroy the correlation responsible for important finite-sample predictive-regression effects. Resampling raw dates independently would destroy predictor persistence. The stated bootstrap preserves a fitted first-order dependence structure; it does not accommodate arbitrary changing persistence or structural breaks simply because it is called a bootstrap.

The procedure is not applied uniformly. No bootstrap is used for $cayp$, which incorporates ex-post construction information; $caya$ changes its construction each period; and the kitchen sink is omitted for computational burden. Those models use cited asymptotic critical values where provided. No critical values are calculated for the model-selection procedure. Consequently not every displayed comparison has the same inferential foundation.

The authors report both unconditional power and power conditional on observing in-sample significance. For book-to-market, the former is 42% and the latter 67% in the first annual evaluation design. Their argument is that a forecasting model already promoted as an in-sample success should survive an out-of-sample diagnostic. This is an interpretation of the testing sequence, not a proof that all out-of-sample tests dominate in-sample tests under a correctly specified stable alternative.

Cumulative squared-error-difference plots provide a separate stability diagnostic:

$$
D_\tau=\sum_{t\leq\tau}[(e^N_t)^2-(e^A_t)^2].
$$

An upward segment favors the predictor; a downward segment favors the historical mean. These paths reveal whether apparent success arises steadily, in a few unusual episodes, or only before the model's practical evaluation period. The in-sample curves use full-sample fitted coefficients and therefore are diagnostic hindsight curves, not feasible trading records. The paper also reports CUSUMQ instability rejections for all monthly models and most annual models, while not printing the individual statistics.

## Annual findings: better fitted models can forecast worse

Table 1 and Figures 1–2 compare annual forecasts through 2005. The following values are percentages of adjusted explanatory power. Out-of-sample evaluation begins twenty years after the relevant data start.

| Predictor | Full-sample in-sample $\bar R^2$ | Out-of-sample $\bar R^2$ | RMSE gain, percentage points per year |
|---|---:|---:|---:|
| Dividend–price | 0.49 | −2.06 | −0.11 |
| Dividend yield | 0.91 | −1.93 | −0.10 |
| Earnings–price | 1.08 | −1.78 | −0.08 |
| Book-to-market | 3.20 | −1.72 | −0.01 |
| Investment/capital | 6.63 | −1.77 | +0.07 |
| Net equity expansion | 8.15 | −5.07 | −0.26 |
| Equity share in issuance | 9.15 | +2.04 | +0.30 |
| Kitchen sink | 13.81 | −139.03 | −5.97 |
| $cayp$, ex-post construction | 15.72 | +16.78 | +1.61 |
| $caya$, recursive construction | Not a fixed IS model | −4.33 | −0.14 |
| Sequential model selection | Not a fixed IS model | −22.50 | −1.69 |

The positive investment/capital RMSE gain with negative adjusted fit is a degrees-of-freedom issue, not contradictory raw MSE evidence. The severe kitchen-sink deterioration illustrates coefficient-estimation and model-instability costs: adding predictors can increase fitted explanatory power while dramatically worsening forecasts.

For 1976–2005, annual out-of-sample adjusted fits are −15.14% for dividend–price, −20.79% for dividend yield, −5.98% for earnings–price, −29.31% for book-to-market, −18.02% for investment/capital, −8.63% for net issuance, and −15.33% for equity's share in issuance. These subperiod statistics evaluate the overall model's residuals or recursive predictions on that subset; they do not refit an entirely new in-sample regression only on the last thirty years.

Equity's issuance share is the strongest ordinary annual exception over the full evaluation, but much of its favorable performance occurs around the oil shock. It does not maintain that advantage during the last thirty years. The distinction between documenting corporate financing decisions and supplying an external investor's forecasting tool is particularly relevant here.

The $cay$ contrast is a direct information-set result: full-sample construction produces substantial apparent predictive success, while recursive construction fails to beat the historical mean. It does not mean that all consumption–wealth economic reasoning is disproved. It means that the implementable estimation experiment is materially different from one in which an agent already knows long-run full-sample coefficients.

## Five-year evidence and overlapping observations

Table 2 uses overlapping five-year premia. Investment/capital has in-sample adjusted fit 33.99%, out-of-sample fit 12.99%, and an RMSE gain of 3.39 percentage points per five-year period. Its last-thirty-year out-of-sample fit is 28.00%. Recursive $caya$ also improves five-year RMSE by 2.50 percentage points, with adjusted fit 9.10%.

The investment/capital result is driven importantly by predictions before the 2000 market collapse. A forecast made in 1997 for 1998–2002 predicts a premium of −0.01, compared with the historical mean's +0.31 and an eventual realization of −0.23. A 1999 forecast for 2000–2004 is −0.07, versus +0.34 for the benchmark and −0.25 realized. These are cumulative five-year premium units, not annualized percentage-point forecasts.

Dividend–price remains negative out of sample. The term spread can improve five-year RMSE by about 2.77 percentage points when estimation begins in 1927 and evaluation in 1965, but its result reverses under an earlier 1947 evaluation start. The kitchen sink and sequential model selection perform particularly badly.

The authors explicitly treat the long-horizon successes as tentative. Overlapping targets reuse the same market episodes, so several apparently correct forecasts before a crash do not represent independent successful predictions. Bootstrap significance does not create additional independent decades of data. The practical inference is to preserve these candidates for further genuinely new observations, not to regard five-year forecasting as settled.

## Monthly constraints, portfolio utility, and release timing

Section 5 compares simple-return forecasts with Campbell–Thompson restrictions. Negative predicted premia are truncated at zero. If an estimated slope has the wrong theory-implied sign, the model can revert to the unconditional historical mean. The sign rule has little effect for most predictors, while truncation has large effects: dividend-yield forecasts are truncated in 54.2% of months, $csp$ in 44.7%, and dividend–price in 32.3%.

The monthly Table 3 caption specifies December 1927–December 2004 for its main comparison, with shorter $csp$ and $cay3$ histories, whereas other monthly tables and discussion use observations through 2005. Reproduce each table's date convention separately. This source inconsistency is material for small forecasting gains and should not be hidden by describing every monthly exercise as one identical sample.

After restrictions, adjusted out-of-sample fits include 0.30% for equity issuance share, 0.25% for the short rate, 0.21% for the term spread, 0.17% for dividend–price, and 0.15% for $csp$. Many others remain negative, including earnings–price, book-to-market, net issuance, and $cay3$. The latter has a positive raw RMSE gain of 0.0088 percentage points per month, or 0.88 basis points, but adjusted fit −0.34%.

The utility comparison assumes power utility with risk-aversion coefficient $\gamma=3$, no negative equity position following premium truncation, and a maximum equity allocation of 150% of wealth. The natural small-return mean–variance approximation is $w_t\approx\hat\mu_t/(\gamma\hat\sigma_t^2)$, clipped to the stated bounds; this formula explains the economics but is an approximation, not an exact allocation equation printed in this article. The source refers to Campbell–Thompson for the detailed utility implementation and does not fully specify the variance-estimation window or all numerical optimization conventions. Those inputs must be recovered before claiming an exact recreation of the CEV column.

Reported certainty-equivalent gains over the historical-mean strategy are approximately 14.40 basis points per month for the term spread, 13.67 for equity issuance share, 9.53 for the short rate, 6.12 for $csp$, 6.10 for $cay3$, and 1.53 for net issuance. Dividend–price loses about 10 basis points per month despite positive restricted forecast fit. Forecast-error improvement and utility improvement measure different objects.

Some gains reflect an equity-heavy allocation in a sample where equities did well. Equity-issuance and term-spread strategies hit the 150% cap in roughly 56% and 59.3% of months. Raising risk aversion to 7.48, which approximately equalizes the historical attractiveness of stock and riskless investments in the authors' comparison, reduces the issuance-share gain from 13.67 to 8.74 basis points. This is a sensitivity calculation, not a universally calibrated preference parameter.

Release delays are decisive for $cay3$. Immediate availability gives a restricted RMSE gain of +0.88 basis points and a CEV gain of +6.10 basis points per month. A one-month delay changes them to −1.62 and −11.82 basis points; a two-month delay gives −1.11 and −9.80. Its macroeconomic components are publicly released with a delay of roughly one to two months. Using observation dates instead of availability dates can therefore reverse the practical conclusion.

Reported portfolio gains are not comprehensive net-of-cost backtests. Net issuance requires about 4.6 percentage points of additional monthly turnover for a CEV gain of only 1.53 basis points. The authors discuss cost benchmarks but do not impose one unified historical execution model across all strategies. Leverage funding, futures implementation, and changing transaction costs remain additional implementation inputs.

## Alternative estimators and combining forecasts

Longer-memory dividend and earnings ratios are tested across one-, five-, and ten-year constructions and several horizons. Among 90 combinations, 27 are in-sample significant; only five have positive statistically significant out-of-sample performance, two only at the 90% level. None supplies robust post-oil-shock success. The experiment illustrates that additional specification search creates more opportunities for favorable isolated results.

Stambaugh and Lewellen coefficient corrections address persistent predictors and correlated innovations. Monthly autoregressive coefficients are very high for many ratios: approximately 0.9989 for dividend payout, 0.9927 for dividend–price, and 0.9879 for earnings–price. Corrections can change significance substantially without improving practical forecasts. Once coefficients are adjusted away from their OLS values, fitted $R^2$ and coefficient-test significance need not move together. The article does not restate the full correction algorithms; exact implementation requires those cited methodological sources rather than an invented shortcut.

Encompassing combines forecasts as $(1-\lambda)\hat y^N+\lambda\hat y^A$. An ex-post optimum can always choose $\lambda=0$, so its squared-error performance cannot be worse than the null. This is not evidence that a forecaster knew the optimal weight. The paper therefore also recursively estimates $\lambda$ using past forecast outcomes. Although the discussion calls the construction a convex combination, the reported table permits negative weights and values above one; a replication must not silently constrain $\lambda$ to [0,1].

For annual equity issuance, the first evaluation's ex-post weight is 0.67 and ex-post RMSE gain 0.3917 percentage points, but the recursive-weight gain is −0.0564. Dividend–price gives an ex-post gain of 0.0084 and recursive gain of −0.2583. The first three combination observations are initialized with favorable perfect foresight, a disclosed choice that slightly favors the combination procedure. Learned shrinkage still does not reliably solve the forecasting problem in these data.

## What a reproducing researcher should preserve

Build an origin-by-origin forecast ledger with each predictor value, its release date, the estimation sample endpoint, estimated coefficients, constrained and unconstrained predictions, realized target, and both squared errors. Keep generated-predictor estimation inside this chronological loop. For long-horizon targets, maintain an explicit availability flag for complete outcomes. Preserve raw MSE and unadjusted fit alongside adjusted reporting measures, and separate log-return, simple-return, annual, monthly, and five-year experiments.

Next reproduce error-difference paths, not only terminal averages. A model whose advantage is concentrated in one episode raises a different stability question from a model with repeated gains across many periods. Do not delete the oil shock merely because it is influential: the authors acknowledge that it could not have been identified as an ignorable special episode in advance. Instead report the full sample and the disclosed subperiod sensitivity.

Finally, distinguish statistical nonrejection from usefulness and distinguish recursively estimated parameters from genuinely new model validation. The predictor list was itself selected from previously published work on much of the same history. Thus these are pseudo-out-of-sample parameter forecasts, not a pristine untouched test of the entire research-selection process. The historical mean is also an estimated, evolving forecast, not an assumption that investors never learn. The paper's durable contribution is this stricter standard of comparison and information accounting; its historical verdict remains bounded by the examined variables, methods, and sample endpoints.
