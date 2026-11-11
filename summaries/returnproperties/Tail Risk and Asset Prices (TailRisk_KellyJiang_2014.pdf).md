# Tail Risk and Asset Prices

Bryan Kelly and Hao Jiang. *Review of Financial Studies* 27(10), 2014, 2841–2871. DOI: 10.1093/rfs/hhu039. Source: [TailRisk_KellyJiang_2014.pdf](../../Finance/TailRisk_KellyJiang_2014.pdf), complete 31-page published article. Page references below are printed journal pages, so PDF page 1 is page 2841. The separate library file `TailRisk_Kelly_2014.pdf` is Kelly's different paper, *The dynamic power law model*, not an alternate copy of this one. The local published article refers to an Internet Appendix that it does not contain; the appendix in the authors' [NBER working-paper version](https://www.nber.org/papers/w19375.pdf), PDF pages 33–36, was inspected separately, with its version-specific limitations noted below.

## Why this matters

A time series of aggregate returns contains too few crashes to estimate a changing crash distribution accurately at short horizons. Kelly and Jiang use a large cross section instead. Thousands of stocks generate enough unusually negative daily observations in each month to estimate the common shape of their downside tails. This produces a long monthly tail-risk series without requiring options prices, intraday data, or decades of observations in each estimation window.

The key innovation is to distinguish a common **tail-shape** state from volatility. The threshold defining an extreme return changes with the current cross section, while the estimator measures how far observations beyond that threshold extend. A market can become much more volatile without the estimated tail shape deteriorating. Conversely, larger outliers relative to the threshold raise the measure even if typical volatility is unchanged. This distinction explains why the series need not spike in every crisis.

The paper connects this statistic to three empirical objects: the conditional market premium, the cross section of stock expected returns, and the price of option-based crash insurance. It then investigates links to aggregate return moments and real activity. These are reduced-form tests and supporting mechanisms. They do not estimate a fully specified equilibrium utility function, identify a unique structural disaster process, or demonstrate that an implementable trading strategy earns the reported gross returns after costs.

## The dynamic power-law model and its identification

For asset $i$, the lower-tail specification is

$$
P(R_{i,t+1}<r\mid R_{i,t+1}<u_t,\mathcal F_t)
=\left(\frac{r}{u_t}\right)^{-a_i/\lambda_t},
\qquad r<u_t<0.
$$

The positive constant $a_i$ allows different firms to have different baseline tail shapes. The common positive state $\lambda_t$ moves every firm's tail thickness through time. Since $r/u_t>1$, a larger $\lambda_t$ makes the exponent less negative and raises the conditional probability of a very large downside observation. The tail exponent is $a_i/\lambda_t$; the empirical Hill statistic estimates an inverse-exponent scale. Calling both simply “the exponent” can reverse the economic interpretation, so this note uses **tail-risk index** for the increasing-with-fatness statistic.

Only the conditional tail beyond $u_t$ is modeled. The central return distribution is unrestricted. The power law is an approximation operationalized as exact over a chosen extreme region. For simple stock returns, the physical lower bound and the finite threshold make a literal infinite-tail interpretation inappropriate; the empirical procedure is a local tail-shape description, not a claim that losses can exceed the entire stock investment.

Pool daily returns for all eligible stocks in month $t$, choose the fifth percentile $u_t$, and keep the $K_t$ observations below it. The estimator is

$$
\widehat\lambda_t^{Hill}
=\frac{1}{K_t}\sum_{k=1}^{K_t}\log\left(\frac{R_{k,t}}{u_t}\right).
$$

Both numerator and denominator are negative, so their ratio is positive and greater than one. The statistic is not the mean of log **gross** returns, the mean size of a loss, or the fraction of observations below a fixed crash cutoff. Approximately 5% of pooled observations enter by construction, and the logarithm measures their severity relative to that month's boundary.

Under the model, conditional log exceedances have mean $\lambda_t/a_i$. If firms have equal ex ante exceedance probabilities, the expected pooled statistic is

$$
E[\widehat\lambda_t^{Hill}\mid\lambda_t]
=\lambda_t\left(\frac1n\sum_{i=1}^{n}\frac1{a_i}\right).
$$

The multiplier is constant if the distribution of $a_i$ is stable. The level of $\lambda_t$ is therefore not separately identified from this normalization, but its fluctuations can be recovered. Equation (2) supplies an identification argument in expectation, not an assertion that a noisy monthly estimate is perfectly correlated with the latent state in finite samples. Likewise, the main text's description of the exponential “scale” is terminologically loose: $a_i/\lambda_t$ is the rate and $\lambda_t/a_i$ the mean/scale.

The essential restrictions are common tail dynamics, adequate cross-sectional information, suitably weak dependence, and a tail threshold far enough from the distribution's center. If individual tail parameters move independently, or if the mixture of firms with different tail properties changes systematically, variation in the pooled statistic can combine composition effects with the desired common state. High cross-industry correlation supports, but does not prove, the single-state restriction.

## Data preparation and measurement choices

Use CRSP daily common-stock returns for NYSE, AMEX, and NASDAQ, January 1963–December 2010, restricting to share codes 10 and 11. The start date follows the major expansion of CRSP coverage in August 1962. The stock panel is unbalanced and changes size over time. Each month's estimator pools all its daily observations; it does not roll a multi-year return window. Thus a strong autocorrelation in the resulting series cannot be attributed to overlapping monthly tail-estimation samples.

The main methodology removes common return components with Fama–French three-factor regressions and estimates tail risk from the residuals, mitigating cross-sectional dependence. The article says raw-return estimates are very similar. A reproduction must distinguish this residualization from volatility standardization: the primary tail statistic uses **nonstandardized** residual observations rather than dividing every observation by an estimated stock volatility. The article does not fully specify the rolling/full-sample window and minimum daily observations for the preliminary factor regressions. That detail is important for a strictly real-time implementation and cannot be inferred from the later 120-month window used for stock tail betas.

The fifth percentile changes every month. A common multiplicative rescaling of returns and their threshold cancels exactly inside the ratio, illustrating scale invariance. In the empirical panel, heterogeneous changing volatilities need not cancel exactly; the method mitigates volatility contamination rather than making all such effects mathematically impossible. The paper reports similar results with cutoffs from the first through fifth percentiles and with the Gabaix–Ibragimov rank-minus-one-half estimator.

For the volatility-standardized robustness check, the authors winsorize the highest and lowest 10% of estimated volatilities before scaling. This reduces distortions from noisy divisors and from tail events inflating their own volatility estimates. The alternative tail series correlates 90% with the main series and gives qualitatively similar pricing results. The exact volatility-estimation window for this check is not fully described in the article.

The estimated monthly AR(1) coefficient is 0.927. Tail indices computed separately for five Fama–French industries have pairwise correlations of 0.57–0.87; indices for size quintiles correlate 0.38–0.86, all reported significant at $p<0.001$. In the average month 44.8% of firms have at least one daily observation in the pooled tail. The estimator is therefore not generally driven by a tiny fixed set of distressed firms, although observation weights are not equal across firms with different exceedance frequencies.

Figures 1 and 2 illustrate the measurement distinction. The index is roughly flat during the 2007–2009 crisis, while the absolute tail threshold rises sharply along with volatility. The threshold's correlation with monthly realized market volatility is 60%. The authors interpret this as a severe increase in dispersion without an equivalent change in the relative shape of extremes. A risk system should consequently monitor both scale and tail shape; a flat Hill index does not mean small crash losses or a benign market.

## Market-return prediction: information timing and inference

For horizons $h=1,12,36,60$ months, estimate monthly predictive regressions of subsequent CRSP value-weighted market returns on the current tail-risk index, first alone and then with alternative predictors. The reported coefficients are scaled to the change in **annualized** expected excess returns associated with a one-standard-deviation increase in the predictor. These units differ from both the raw monthly slope and an $h$-year cumulative return.

Long-horizon observations overlap. The paper uses Hodrick's overlapping-observation standard errors with lag length equal to the number of months in the horizon. It reports that this gives more conservative inference than several alternatives. An ordinary monthly iid standard error, or treating overlapping five-year outcomes as independent, would misrepresent the uncertainty.

| Forecast horizon | Annualized effect of one SD higher tail risk | Hodrick $t$ | In-sample $R^2$ | Out-of-sample $R^2$ |
|---|---:|---:|---:|---:|
| One month | 4.54 percentage points | 2.08 | 0.7% | 0.3% |
| One year | 4.02 percentage points | 2.04 | 6.1% | 4.5% |
| Three years | 3.65 percentage points | 2.40 | 16.6% | 15.7% |
| Five years | 3.16 percentage points | 2.65 | 20.9% | 20.1% |

Tables 1–3 establish these magnitudes. The much larger long-horizon $R^2$ is consistent with persistent conditional expected returns, but should not be read as an equally large one-month timing edge. Forecast uncertainty, limited independent long-horizon observations, and generated-regressor uncertainty remain relevant.

Comparison predictors include book-to-market, default return and yield spreads, dividend payout and dividend-price ratios, earnings-price, inflation, long-term bond returns and yields, net equity expansion, stock volatility, the term spread, and the Treasury-bill rate. Options-based variance risk premium and risk-neutral moments have shorter samples, beginning in 1990 and 1996 respectively. The dividend-price ratio is the closest broad competitor in the main sample. Tail risk remains informative in bivariate specifications, although its significance weakens beside the long-term yield at longer horizons. Combining tail risk and dividend-price gives in-sample $R^2$ of 37.5% at three years and 53.8% at five years; those are joint-model fits, not tail-only results.

Out-of-sample prediction starts after an initial 120-month training period. Expand the estimation window by one month at each forecast origin and estimate coefficients using only information then available. Compare squared errors to those from a recursively estimated historical mean:

$$
R^2_{OOS}=1-\frac{\sum_t(R_{t+1}-\widehat R_{t+1|t})^2}
{\sum_t(R_{t+1}-\overline R_t)^2}.
$$

The notation is one-step, with horizon-specific outcomes required for the longer tests. Table 3 calls the procedure rolling, but the text explicitly describes an **expanding** window. For $h>1$, a feasible implementation must admit only training observations whose full return horizon has matured by the forecast date. The article's concise algorithm does not spell out every long-horizon alignment or simple-versus-log aggregation convention, so these should be checked against original code rather than improvised as established facts.

The annual, three-year, and five-year tail forecasts pass the Clark–McCracken ENC-NEW test at 5%; the monthly tail forecast does not carry that significance marker. Out-of-sample $R^2$ is negative for many conventional predictors. This is evidence of historical forecast value under the reported experiment, not a post-2010 validation or a certainty that future returns compensate high measured risk.

## Cross-sectional tail exposure is a predictive beta

For each stock estimate

$$
r_{i,s+1}=\mu_i+\beta_i\widehat\lambda_s+e_{i,s+1}
$$

using the most recent 120 months, requiring at least 36 nonmissing return months. Reconstitute quintile portfolios each month using estimated $\beta_i$. Exclude stocks priced below \$5 at formation. The beta is a slope on **lagged tail-risk levels**, not a same-month covariance with tail-risk innovations and not an individual stock's Hill tail exponent. This distinction is central to implementing the paper's signal.

The authors motivate positive predictive beta by the idea that high tail risk raises discount rates and expected future returns more strongly for adversely exposed stocks. Stocks that hedge adverse tail-risk states should have lower required returns. This pricing interpretation is a hypothesis; a predictive slope alone does not directly identify the contemporaneous hedge payoff. Levels are used partly to reduce the influence of measurement error that would be amplified by differencing the estimated index.

Track both equal- and value-weighted portfolio performance over twelve months following formation and separately over one month. Formation and evaluation samples do not overlap for a given cohort. Because twelve-month cohorts are formed monthly, their holding periods overlap; the reported inference uses Newey–West standard errors with twelve lags. Table 4 expresses portfolio returns and alphas in monthly percentage units even in its twelve-month-holding panel. The source does not fully specify every within-cohort weight update and aggregation rule across overlapping cohorts; those mechanics must be matched before expecting exact numbers.

The value-weighted high-minus-low tail-beta portfolio earns 0.35% monthly on average in the twelve-month experiment, with $t=2.15$, approximately 4.2% annualized by multiplying by twelve. Its Fama–French three-factor alpha is 0.45% monthly, $t=3.00$, or 5.4% annualized. The equal-weighted spread averages 0.33% monthly ($t=2.48$), with FF3 alpha 0.33% ($t=2.85$). Average returns and FF3 alphas rise broadly monotonically across the quintiles.

Adding momentum reduces the value-weighted twelve-month FF3 alpha to 0.34% monthly ($t=2.24$); adding the traded Pastor–Stambaugh liquidity factor yields 0.43% ($t=2.93$). In the one-month holding experiment the value-weighted FF3 alpha is 0.46% monthly ($t=2.58$); the equal-weighted alpha is 0.30% ($t=2.22$). These are gross historical spreads. Neither stock trading costs nor short-sale fees and capacity constraints are deducted.

Table 5 independently sorts into four tail-beta groups and four groups for each control characteristic. Size is market equity at formation. Idiosyncratic volatility is the standard deviation of daily FF3 residuals in the prior month. Downside beta uses the prior 120 months but only months when market returns are negative. Coskewness is estimated from a regression on squared market returns. The resulting intersections are held for a year, with four-factor alphas and twelve-lag Newey–West inference.

The spread generally survives these comparisons, but not every subgroup is significant. For example, the smallest-size group's value-weighted four-factor spread is just 0.01% monthly with $t=0.10$, whereas the other size groups have spreads around 0.30–0.34%. Across idiosyncratic-volatility groups value-weighted spreads range from 0.18% to 0.45% monthly. The evidence is therefore broader than one unconditional sort but weaker than uniform independent significance in every controlled cell.

## Options and crash-insurance prices

The option analysis uses OptionMetrics individual-equity puts over 1996–2010. Sort by absolute Black–Scholes delta into five bands: below 0.20, 0.20–0.40, 0.40–0.60, 0.60–0.80, and at least 0.80. These correspond to deep out-of-the-money through deep in-the-money puts. Sell a put with approximately one month to maturity on the first trading day following the monthly expiration and hold to the following expiration; delta hedge each position daily. The return incorporates option value changes, hedge gains or losses, and margin-account interest.

Exclude observations with bid–ask spread below the minimum tick, zero bid, zero open interest, embedded leverage in the top or bottom 1%, or time value below 5%. The last filter is intended to mitigate American early-exercise issues. Exact margin capital conventions, option selection among multiple contracts, daily rehedging transaction costs, and all vendor cleaning details are not reproduced in the article; the unusually large unadjusted option returns cannot be compared directly to unlevered stock returns.

Re-estimate the tail index on the same expiration-to-expiration calendar so lagged tail information does not overlap the next option holding period. Predict each moneyness portfolio's return from the standardized lagged index. Because the options sample is short, estimate one full-sample predictive coefficient for each portfolio; this is not an out-of-sample option-beta sorting exercise.

Table 6 reports a 16.66% **monthly** difference between deep-OTM and deep-ITM delta-hedged short-put returns, $t=3.55$. The corresponding predictive-tail-beta difference is 7.17, $t=2.39$, meaning a one-SD index increase predicts approximately 7.17 percentage points more return on that spread next month. Embedded leverage explains much of the magnitude. Scaling option positions by their elasticity to the underlying reduces the mean spread to 1.07% monthly ($t=2.43$) and its tail predictive coefficient to 0.79 ($t=2.43$). The leverage-adjusted FF3 alpha is 1.04% ($t=2.28$); with momentum and liquidity it falls to 0.73% ($t=1.54$). The last estimate is not conventionally significant.

This links the index to the cost of explicit crash insurance. It does not imply that shorting puts is an inexpensive or low-risk implementation of a tail-risk premium. Capital, leverage, rehedging, and exposure to extreme losses are integral to interpreting these payoffs.

## Evidence on the economic channels

The first proposed channel is aggregation: under appropriate regular-variation and dependence conditions, a portfolio can inherit the heaviest component tail. The paper uses this idea to motivate a relation between common firm-level tail dynamics and market-level risk. It is not a theorem that arbitrary dependent stock tails, including offsetting exposures, always aggregate with the same coefficient. Nor does summing many assets generally preserve every aspect of their entire distribution.

As a test, calculate monthly realized market skewness and kurtosis from daily returns. Regress their leads and lags from −24 to +24 months on contemporaneous tail risk and the current realized moment, dropping the redundant moment control at zero horizon. Higher tail risk predicts more negative skewness, especially beyond a year, and higher future kurtosis. These coarse moment proxies are themselves noisy and do not establish the exact market-tail exponent.

Options provide an independent comparison under the risk-neutral rather than physical measure. Over 1996–2010, correlations of the tail index with S&P 500 risk-neutral skewness and kurtosis are −0.30 ($p=0.02$) and 0.33 ($p=0.01$). The correlation with the S&P put-volatility-smirk slope is −0.17 and insignificant at $p=0.15$; with the average individual-stock smirk it is −0.53 ($p<0.01$). The put/call volume ratio correlation is 0.42 ($p=0.01$), while the variance risk premium correlation is only 0.04 ($p=0.67$). Thus the evidence is specific, not a generic high correlation with every option-implied risk measure.

For option moment and smirk estimates, retain positive-open-interest contracts, calculate statistics at the maturities immediately above and below 30 days, interpolate to a constant 30-day horizon, and average daily estimates within the month. Smirk slopes regress put implied volatility on strike/spot among OTM puts with delta above −0.5. All quoted correlation inference uses twelve-lag Newey–West errors.

The second channel is common uncertainty affecting real investment and hiring. Apply the cross-sectional tail method to Compustat quarterly sales growth beginning in 1975. Average monthly return-tail estimates within quarters. Return tails correlate 0.23 with contemporaneous sales-growth tails ($p=0.024$) and 0.31 with next-quarter sales tails ($p=0.008$), with significance extending up to three quarters. Footnote 30 sets a 7.5% tail cutoff but describes its cross section as annual, while the surrounding procedure pools calendar-quarter reports. This threshold-frequency ambiguity should be resolved from the original data or code for exact replication.

For macro responses, estimate a monthly VAR over July 1963–June 2008 ordered as volatility, tail risk, federal funds rate, log hourly earnings, log CPI, hours, log employment, and log industrial production. Use manufacturing-firm tail risk for manufacturing production/employment. A one-SD tail shock precedes roughly 0.6% production and employment declines within a year, followed by recovery. Quarterly trivariate VARs containing volatility, tail risk, and either gross private domestic or nonresidential fixed investment over 1963Q3–2008Q2 show roughly 2.5–4% investment declines in the subsequent year. Figure 5's bands are **one standard error**, not 95% confidence intervals.

The benchmark volatility shock is a jump in Bloom's extreme-volatility indicator, not a directly comparable one-SD continuous volatility shock. Using raw volatility gives a smaller production response, approximately 0.4%, while leaving the tail response similar. The published article does not give every VAR lag, deterministic-term, and bootstrap setting, referring to Bloom's framework. Ordered VAR responses are evidence consistent with an uncertainty channel; they are not standalone causal identification of an exogenous tail-risk intervention.

## Appendix inspection and reproducibility limits

The [NBER appendix](https://www.nber.org/papers/w19375.pdf) considers unequal exceedance frequencies, factor dependence, heterogeneous volatility, and heterogeneous tail exponents. Its Monte Carlo designs use sample sizes 500, 1,000, and 5,000; factor loadings are zero, one, or $N(1,1)$; volatility multipliers are fixed or uniform on $[0.5,1.5]$ and $[0.1,1.9]$. Results suggest modest incremental distortion relative to independent cases. However, prose specifies a lower 5% tail while Table A1 says upper 2.5%; one prose sample-size reference also disagrees with its table. Random replication count is not supplied. These inconsistencies prevent exact reproduction from this version alone. Simulations support plausibility under their designs, not consistency under arbitrary financial dependence.

The central estimator and empirical workflows are recoverable, but reproducing every table requires the original residualization conventions, return aggregation and overlapping-cohort rules, stock-data filters, option capital accounting, and VAR settings. Changing panel composition and volatility mixture can affect the estimator's scale. The forecast exercise predates 2011 and lacks a current-period validation. The substantive contribution remains a parsimonious cross-sectional measurement strategy that makes dynamic tail shape observable enough to test asset-pricing hypotheses, with suggestive evidence across stocks, options, and fundamentals rather than a uniquely identified structural explanation.
