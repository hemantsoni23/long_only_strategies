# Consumption, Aggregate Wealth, and Expected Stock Returns in Japan

Chikashi Tsuji, International Journal of Economics and Finance 1(2), August 2009, pp. 123–133. Source: [Consumption, Aggregate Wealth, and Expected Stock Returns in Japan.pdf](<../../Finance/Consumption, Aggregate Wealth, and Expected Stock Returns in Japan.pdf>), eleven pages. This study tests the Japanese counterpart of the consumption–wealth forecasting variable developed in the US literature.

## Why this matters and what the paper adds

The contribution is an international test of whether a macroeconomic predictor transfers across countries. Using quarterly Japan data from 1980Q2 through 2002Q3, Tsuji finds that the estimated consumption–wealth deviation, $cay$, is a weak short-horizon stock-return predictor and generally loses explanatory power when dividend yield is included. Dividend yield has a much stronger long-horizon relationship with subsequent excess returns. A relative short rate, useful in cited US research, has little predictive power here.

The paper also proposes economic explanations involving differences in the timing and volatility of Japanese and US consumption. These explanations use Granger tests and conditional-volatility plots. They are interpretations of aggregate time-series patterns, not identified causal evidence about household preferences or a direct measurement of individual consumption smoothing.

## Theoretical object and estimation

The starting point is a loglinearized intertemporal budget relation linking the consumption–wealth ratio to expected future aggregate-wealth returns less consumption growth. Human capital is unobserved, so labor income proxies for its trend component. If $c_t$, $a_t$, and $y_t$ are log consumption, observed asset holdings, and labor income, and $\omega$ is the average asset share of total wealth, the theoretical deviation is

$
cay_t=c_t-\omega a_t-(1-\omega)y_t.
$

Equation (2) relates this deviation to discounted expected asset and human-capital returns, consumption growth, and a stationary component. A high deviation need not forecast stock returns alone: adjustment can occur through consumption growth or human-capital returns. The stock-return interpretation requires those other terms to be sufficiently stable or suitably correlated with asset-return expectations. This qualification is particularly relevant because the Japanese results strongly relate $cay$ to subsequent consumption growth.

For estimation the paper follows Stock–Watson dynamic least squares, with nondurables-and-services consumption $c_{n,t}$:

$
c_{n,t}=\alpha+\beta_a a_t+\beta_y y_t+
\sum_{i=-8}^{8} b_{a,i}\Delta a_{t-i}+
\sum_{i=-8}^{8} b_{y,i}\Delta y_{t-i}+\epsilon_t.
$

The lead–lag length $k=8$ is specified in Note 4. The estimated trend deviation is defined as

$
\widehat{cay}_t=c_{n,t}-\widehat\beta_a a_t-\widehat\beta_y y_t.
$

The definition does not subtract the estimated intercept. Consequently the level of the variable need not have mean zero; Table 1 reports mean 3.542 and standard deviation 0.012. An intercept in the subsequent predictive regression absorbs a constant shift. Figure 1 separately standardizes the plotted deviation and returns to zero mean and unit variance.

The article does not report the estimated cointegrating coefficients or a full cointegration-test sequence. It does not describe recursive real-time estimation of the deviation. Eight leads of growth and revised macroeconomic data create a serious distinction between this fitted historical predictor and a predictor available to an investor at the forecast date. A reproduction must retain the published full-sample interpretation unless it deliberately implements and labels a real-time extension.

## Data and preprocessing

Consumption is the sum of real household nondurable-goods and services expenditure from the Japanese government, seasonally adjusted using Census X-12. Asset holdings sum the Bank of Japan categories financial assets, personal and financial assets, households. They are deflated by the personal-consumption-expenditure deflator and seasonally adjusted with X-12. Employee compensation from the Japanese government supplies labor income, with the same deflation and seasonal adjustment.

The return universe is the value-weighted Tokyo Stock Exchange First Section portfolio from the Japan Securities Research Institute. Real returns use the consumer price index from the Statistics Bureau. The risk-free series splices yields on traded bonds with repurchase agreements through 1984Q2 and the Bank of Japan's one-month median negotiable time-deposit rate from 1984Q3. The paper explains that the CD series is unavailable earlier. Exact conversion of quoted rates into quarterly log risk-free returns is not fully documented.

Other predictors are log dividend yield $d-p$, a dividend–earnings or payout variable $d-e$, and the relative risk-free rate, defined as the current short rate minus its backward 12-month moving average. Additional controls include the ten-year government yield less the short rate, $TRM$, and the long-term Nikkei Bond Index yield less the ten-year government yield, $DEF$.

The prose's construction of $d-e$ refers to the log dividend yield minus log earnings, whereas the notation and table labels call it a dividend–earnings/payout ratio. Those are not automatically identical. Exact series definitions should be checked before replicating that control. Series vintages, X-12 options, population normalization, missing-data treatments, and end effects are also not given. Financial and macroeconomic transformations use different deflators as reported; replacing both by one index would be a change to the design.

The common sample contains 90 quarterly dates before allowing for forecast-horizon losses and estimation requirements. Table 1 reports quarterly log excess-return mean $-0.001$, standard deviation $0.113$, skewness $-1.261$, and kurtosis $5.788$. The contemporaneous correlation of excess returns with $cay$ is $-0.001$, compared with correlations of $0.483$ between $cay$ and dividend yield and $0.418$ between $cay$ and the payout variable. These are descriptive correlations, not forecast coefficients.

## Forecast regressions and inference

The short-horizon regression is OLS of next-quarter log real or excess return on an intercept and lagged predictors. The long-horizon specification sums subsequent log excess returns:

$
\sum_{j=1}^{H}(r_{t+j}-r_{f,t+j})=a_H+b_H^\top z_t+u_{t,H},
\qquad H\in\{1,2,3,4,8,12,16\}.
$

Consumption-growth versions replace the left side by total or nondurable consumption growth over the same horizon. This is a cumulative log outcome, not an average quarterly return. Coefficient growth across horizons must be read in that light.

All displayed return-regression and VAR $t$ statistics are Newey–West corrected. The bandwidth, finite-sample convention, and exact treatment of overlapping horizons are not specified. Long-horizon outcomes share many quarters, so their effective information is much smaller than a count of overlapping observations suggests. The source gives conventional 5% and 10% significance stars, not a small-sample bootstrap or a multiple-horizon correction.

There is no forecast holdout, expanding-window comparison against the historical mean, or utility-based asset allocation. The reported adjusted $R^2$ values measure in-sample fit. Calling them out-of-sample forecasting gains or net strategy performance would overstate the experiment.

## Main short-horizon outcomes

In Table 2, the real-return regression on $cay$ alone has slope 1.748, $t=1.660$, and adjusted $R^2=0.023$. For excess returns, the analogous slope is 1.815, $t=1.682$, and adjusted $R^2=0.025$, marked significant at 10% only. Including lagged excess return leaves slope 1.817 but $t=1.659$ and adjusted $R^2=0.013$.

Dividend yield alone has excess-return slope 0.063, $t=2.067$, and adjusted $R^2=0.039$. With both $cay$ and dividend yield, their slopes are 0.989 and 0.048, with $t$ statistics 0.828 and 1.469, and adjusted $R^2=0.035$. Thus neither variable is conventionally significant in that particular joint quarterly regression, although dividend yield is stronger in the wider set of comparisons. It would be inaccurate to say dividend yield is significant in every joint specification.

The broad specification with lagged return, $cay$, dividend yield, payout ratio, relative short rate, term spread, and default spread has adjusted $R^2=-0.009$. Its $cay$ slope is 1.679 with $t=1.141$, and dividend-yield slope 0.030 with $t=0.746$. Adding predictors does not create strong quarterly evidence.

## Horizon dependence and joint regressions

Table 3's univariate cumulative excess-return regressions report:

| Horizon, quarters | $cay$ slope | $t$ | Adjusted $R^2$ | Dividend-yield slope | $t$ | Adjusted $R^2$ |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1.813 | 1.681 | .025 | .063 | 2.065 | .038 |
| 4 | 8.746 | 2.380 | .168 | .260 | 2.791 | .189 |
| 8 | 14.752 | 3.203 | .241 | .512 | 3.786 | .376 |
| 12 | 18.420 | 2.766 | .252 | .766 | 5.070 | .557 |
| 16 | 25.714 | 3.154 | .317 | 1.028 | 7.139 | .715 |

These are reported slopes per unit of the log predictor. A one-standard-deviation change in $cay$ is about .012, not one whole unit. For example, the eight-quarter univariate slope implies about .177 cumulative log excess return for that predictor displacement, calculated from the table, not an expected annual arithmetic return.

Including both predictors weakens $cay$ markedly. At $H=8$, its slope is 6.936 with $t=1.821$, compared with dividend-yield slope .408 and $t=2.809$, adjusted $R^2=.409$. At $H=12$, $cay$ has slope 4.419 and $t=1.095$, while dividend yield has slope .694 and $t=4.502$. At $H=16$, $cay$ has $t=.729$ and dividend yield $t=5.744$. In the four-predictor specification $cay$ retains evidence at eight quarters, slope 11.373 and $t=2.503$, and weaker evidence at twelve quarters, slope 7.226 and $t=1.683$.

The printed final column of Table 3 has visibly displaced or inconsistent entries in several lower rows, including a purported adjusted $R^2$ of 3.085 for the relative-rate regression. An adjusted $R^2$ above one is incompatible with the ordinary intercept regression described. The note therefore does not use that cell as a valid fit measure or silently repair it. The univariate and two-predictor figures quoted above occupy clearly aligned rows.

Consumption results help explain why the budget identity need not translate into equity prediction. For total consumption growth, the $cay$ slope is $-.344$ at one quarter, $t=-3.918$, and $-.567$ at four quarters, $t=-3.114$. For nondurable growth it is $-.302$ at one quarter, $t=-4.284$, and $-.616$ at four quarters, $t=-5.024$. Negative consumption-growth forecasting relationships are strong at short horizons, while their longer-horizon significance weakens.

## VAR and proposed macroeconomic explanation

The paper estimates first-order VARs in excess returns, relative short rate, dividend yield, and payout ratio, then adds $cay$ as a fifth variable. In the return equation of the four-variable VAR, dividend yield has slope .061 and $t=1.973$, with adjusted $R^2=.011$. Adding $cay$ yields a $cay$ slope 1.448 with $t=1.041$ and adjusted $R^2=.012$. The enlarged system therefore supplies little incremental one-step return evidence.

The interpretation section compares quarterly growth in real GDP, nondurables-and-services consumption, and investment in Japan and the US over the same stated common sample. With one lag, Japanese GDP Granger-predicts consumption, $F=15.009$, printed $p=.000$, while consumption does not significantly predict GDP, $F=2.570$, $p=.113$. Japanese investment predicts GDP, $F=6.113$, $p=.015$. In the US, consumption predicts GDP, $F=19.881$, printed $p=.000$, while GDP does not significantly predict consumption, $F=2.347$, $p=.129$. Two-lag results broadly support the consumption-timing contrast.

These rejections concern lagged predictive content in the specified systems. A printed .000 is rounded, not an exact zero probability. The tests do not establish that one country's economy is structurally caused by investment and another by consumption, nor that this alone explains the difference in stock-return coefficients. Common shocks, measurement, and the chosen lag structure remain possible alternatives.

Figure 2 displays conditional consumption volatilities estimated using an EGARCH model and shows Japanese consumption as more volatile. The paper interprets this as weaker consumption smoothing. It does not report the EGARCH order, full equation, estimates, innovation distribution, or a statistical test comparing preferences. The figure's date axis also extends beyond the common return-test sample. A higher aggregate volatility can reflect shocks and aggregation as well as preferences, so the behavioral explanation is suggestive rather than identified.

## Reproduction and research use

The paper provides enough structure to reconstruct the forecasting exercise but not exact data vintages or code. The crucial workflow is to assemble and transform the stated Japanese series, estimate the eight-lead/eight-lag DLS trend relation, construct the defined deviation, lag predictors correctly, form cumulative log outcomes for each horizon, and reproduce OLS and first-order VAR tables with an explicitly stated HAC convention. Revisions, seasonal-adjustment endpoints, and fitted cointegration coefficients must be kept separate from any real-time extension.

Its strongest lesson is that a US macro-financial predictor requires country-specific validation. In this Japanese historical sample, dividend yield dominates most $cay$ comparisons and the relative short rate contributes little. The larger long-horizon fit is not evidence of an implementable return premium without genuinely available predictor vintages, suitable overlapping-data inference, stability checks, and a separate out-of-sample evaluation.
