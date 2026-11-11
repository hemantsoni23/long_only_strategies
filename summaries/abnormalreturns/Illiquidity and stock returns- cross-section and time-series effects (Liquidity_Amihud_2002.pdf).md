# Illiquidity and stock returns: cross-section and time-series effects

Yakov Amihud. *Journal of Financial Markets* 5 (2002), 31–56. Source: [Liquidity_Amihud_2002.pdf](../../Finance/Liquidity_Amihud_2002.pdf). This note covers the complete 26-page article. Page references below use journal pagination; PDF page 1 is journal page 31.

## Why this matters and what is new

An investor buying an illiquid stock requires compensation for the difficulty of subsequently selling it. That familiar cross-sectional argument does not by itself tell us how changes in the liquidity of the whole market affect prices today and expected returns tomorrow. Amihud's central contribution is to separate these two time-series effects. Higher anticipated market illiquidity should raise required future excess returns. An unexpected deterioration in liquidity should reduce current prices, because the deterioration is persistent and raises subsequent required returns. The same innovation can therefore be bad news for today's investor and associated with a higher prospective premium.

The paper makes this argument testable over a long historical sample by introducing a deliberately inexpensive proxy: the daily absolute return divided by dollar trading volume, averaged over a period. It requires daily stock returns and volume rather than transaction records, quotes, or order-book depth. The empirical contribution is consequently both a measurement proposal and a set of cross-sectional and time-series tests. Its evidence concerns NYSE stocks during the 1960s through the 1990s, not a modern high-frequency implementation or a demonstrated trading strategy.

For a quantitative researcher, the distinction between a level premium and a liquidity shock is essential. A regression that associates falling prices with worsening liquidity does not establish that investors prefer illiquid stocks. Conversely, a positive association between lagged illiquidity and subsequent returns does not mean an investor benefits when liquidity unexpectedly evaporates. The paper also finds that the relationship is stronger for smaller stocks, giving a possible explanation for variation in the size effect. It does not estimate a complete equilibrium liquidity-risk model or establish that liquidity alone resolves the equity-premium puzzle.

## Measurement: an average of daily price changes per dollar traded

For stock $i$ in year $y$, let $R_{iyd}$ be the daily return, $VOLD_{iyd}$ daily dollar volume, and $D_{iy}$ the number of available daily observations. Equation (1), p. 34, defines

$$
ILLIQ_{iy}=\frac{1}{D_{iy}}\sum_{d=1}^{D_{iy}}\frac{|R_{iyd}|}{VOLD_{iyd}}.
$$

This is an average of ratios. Dividing an annual absolute return by annual volume, or dividing the sum of daily absolute returns by the sum of volume, gives a different statistic. The paper multiplies the measure by $10^6$ for presentation. A replication must preserve its return and dollar-volume units consistently; changing returns from fractions to percentages introduces another factor of 100.

The interpretation is the magnitude of price movement associated with a dollar of trading activity. It is not a regression coefficient from signed order flow to prices, nor an estimate of the causal impact of submitting an additional order. Volatility enters its numerator, trading intensity enters its denominator, and both respond to information and market conditions. Large price movements with little volume produce high values. Disagreement can generate considerable trading even for modest price changes, whereas common interpretations of news may move prices without comparable volume. These mechanisms qualify its interpretation as a pure trading-cost measure.

The article compares the proxy with intraday estimates of price impact and a fixed-cost spread component using 1984 data. Both coefficients are positive and strongly significant; the regression has $R^2=0.30$ (p. 35). The price-impact slope is 247.9 with absolute $t=13.78$ and the fixed-cost slope is 49.2 with $t=17.33$, under the scaling specified in the source. This supports a liquidity interpretation but leaves considerable unexplained variation. It is validation against other proxies, not proof that the statistic measures all dimensions of liquidity. Spread, depth, resilience, and execution risk need not move proportionately.

The annual cross-sectional average is

$$
AILLIQ_y=\frac{1}{N_y}\sum_{i=1}^{N_y}ILLIQ_{iy}.
$$

For the cross-sectional return regressions the explanatory variable is normalized by that year's average:

$$
ILLIQMA_{iy}=\frac{ILLIQ_{iy}}{AILLIQ_y}.
$$

Despite the label “mean-adjusted,” this is division by the mean, not subtraction. Its yearly cross-sectional mean is one. Normalization separates a stock's relative illiquidity from large secular movements in the aggregate measure; the latter are studied separately in the time-series tests. Cross-sectional coefficients on this normalized variable should not be interpreted as the coefficients on the unnormalized market series.

## Cross-sectional sample and information timing

The daily inputs are CRSP NYSE observations from 1963–1996 for monthly return regressions during 1964–1997. There are 408 return months. Characteristics are measured in calendar year $y-1$ and used throughout all twelve months of year $y$. This annual freezing is important: the paper does not estimate each month's characteristics using its contemporaneous return or a rolling window ending in that month.

The eligibility rules in Section 2 are as follows. A stock must have more than 200 days of return and volume data in the characteristic year, remain listed at that year's end, have a year-end price greater than \$5, and have year-end market capitalization available. The capitalization requirement excludes certain securities without the required data. The extreme upper and lower one percent of the annual illiquidity distribution are discarded. Sample sizes vary from approximately 1,061 to 2,291 stocks across months.

A return must be observed in the test month, but the construction is intended to retain delisting outcomes rather than condition on survival through the end of the test year. Footnote 9 discusses use of CRSP returns and delisting returns, retaining losses of 100 percent where recorded. Missing delisting returns receive a loss of 30 percent for the listed performance-related delisting codes: 500, 520, 551–573, 574, 580, and 584. A reproduction should implement the paper's historical convention explicitly and document how contemporary CRSP return fields map into it, rather than silently apply a modern default delisting adjustment.

The remaining characteristics are measured with the same annual lag:

- **Size:** the logarithm of year-end market capitalization.
- **Beta:** a Scholes–Williams market beta assigned through ten size portfolios. Stocks are sorted into size groups at year-end, the groups' daily returns over that year are formed, and each stock receives its group's estimated beta against the equally weighted market return. This reduces noisy individual beta estimation but also makes beta and size mechanically related. The paper cites the estimator rather than restating every computational convention.
- **Volatility:** the standard deviation of daily stock returns, with percentage scaling as used in the tables. This helps determine whether the illiquidity coefficient merely captures return variability in the proxy's numerator.
- **Dividend yield:** the sum of annual cash dividends divided by the year-end stock price.
- **Prior returns:** $R100$, the return over the last 100 trading days of the previous year, and $R100YR$, the return over the preceding part of that year. These control for return continuation at two nonoverlapping horizons.

The two prior-return variables are not the modern conventional twelve-minus-one-month momentum signal. A faithful implementation should reproduce the trading-day partition. The article does not provide executable rules for every complication in daily compounding, missing volume, corporate-action adjustment, or historical exchange-code transitions. Such decisions must be recorded as replication choices rather than attributed to the author.

Table 1, p. 38, summarizes yearly distributions. The mean annual illiquidity measure is 0.337 under the paper's scaling, and its average cross-sectional standard deviation is 0.512. The mean annual skewness is 3.095, consistent with a long right tail even after screening. Mean capitalization is \$792.6 million, average daily-return volatility is 2.08 percent, and mean dividend yield is 4.14 percent. Illiquidity and log size have correlation approximately $-0.614$; illiquidity and daily volatility have correlation about 0.278. These relationships explain the need to distinguish liquidity from familiar stock characteristics.

## Cross-sectional estimator and findings

Each month's regression has the form

$$
R_{imy}=k_{0,my}+\sum_j k_{j,my}X_{ji,y-1}+u_{imy}.
$$

The reported coefficients are time-series averages of the monthly estimates, with inference based on their variation across months, following the Fama–MacBeth approach. The basic specification includes beta, normalized illiquidity, and the two prior-return variables. The expanded specification adds log size, daily volatility, and dividend yield. Weighted least-squares checks are mentioned as qualitatively similar, but the principal displayed estimates are the monthly cross-sectional results.

The central Table 2 numbers, p. 41, are:

| Specification and sample | Mean coefficient on $ILLIQMA$ | Absolute $t$ |
|---|---:|---:|
| Basic, all 408 months | 0.162 | 6.55 |
| Basic, excluding January | 0.126 | 5.30 |
| Basic, 1964–1980 | 0.216 | 4.87 |
| Basic, 1981–1997 | 0.108 | 5.05 |
| Expanded controls, all months | 0.112 | 5.39 |
| Expanded controls, excluding January | 0.103 | 4.91 |
| Expanded controls, 1964–1980 | 0.135 | 3.69 |
| Expanded controls, 1981–1997 | 0.088 | 4.56 |

Monthly returns use percentage units. Thus the basic coefficient is about 0.162 percentage point per month for a one-unit increase in normalized illiquidity, conditional on included controls. It is not a return per dollar of trading cost. In the expanded specification the coefficient falls, but remains positive and statistically significant. Persistence outside January and in both subperiods is an important qualification to an explanation based entirely on seasonal small-stock returns.

The basic illiquidity coefficient is positive in 259 of 408 months, has a median of 0.135, and low reported serial correlation of about 0.08. A positive mean is therefore not equivalent to a positive realized premium in every month. In the expanded full-sample specification, beta's coefficient is 0.217 with $t=0.64$, log size has coefficient $-0.134$ with $t=3.50$, daily volatility has coefficient $-0.179$ with $t=1.90$, and dividend yield has coefficient $-0.048$ with $t=3.36$. These are partial associations under a particular characteristic set, not separately identified causal effects.

Book-to-market is deliberately omitted; the paper discusses earlier evidence concerning its relevance in NYSE samples and outside January. Consequently, the result should not be described as an illiquidity premium established after controlling for a full modern factor set. Likewise, this regression is not a long–short portfolio backtest. No implementable trading schedule, realized execution-cost series, capacity calculation, or net-of-cost Sharpe ratio is reported.

## Time-series mechanism and estimation

Section 3 begins from persistence in market illiquidity. Write $x_y=\log AILLIQ_y$ and fit

$$
x_y=c_0+c_1x_{y-1}+v_y.
$$

Expected log illiquidity is $c_0+c_1x_{y-1}$. This is an expectation of a logarithm; it should not silently be replaced by the logarithm of expected level illiquidity, which differs under uncertainty. If required excess returns increase with expected illiquidity, the lagged market variable predicts higher prospective compensation. A positive innovation $v_y$ raises future expected illiquidity when persistence is positive and should lower contemporaneous prices, holding cash-flow expectations fixed.

The tested return equation is

$$
R_{M,y}-R_{f,y}=g_0+g_1x_{y-1}+g_2v_y+w_y,
$$

with predicted signs $g_1>0$ and $g_2<0$. The market return is the equally weighted NYSE return. The annual risk-free rate is the one-year Treasury-bill yield at the beginning of the year. The annual market-liquidity construction excludes the highest one percent of stock illiquidity observations; this differs from the two-sided trimming described for the cross-sectional exercise and should not be homogenized without disclosure.

The annual autoregression uses 1963–1996 liquidity observations. The initial estimates are $\hat c_0=-0.200$, $\hat c_1=0.768$, and $R^2=0.53$. Because autoregressive persistence is downward biased in small samples, the author applies Kendall's correction,

$$
\hat c_1^{\,adj}=\hat c_1+\frac{1+3\hat c_1}{T},
$$

obtaining 0.869 and adjusting the intercept accordingly. The unexpected-liquidity series is calculated from the adjusted autoregression. The source does not spell out the adjusted intercept's exact computational formula, so a replication should state its chosen implementation and test sensitivity to it.

This correction matters because the liquidity innovation is negatively correlated with stock returns; the usual persistent-predictor finite-sample problem can bias the lagged predictor's estimated coefficient upward. Including the innovation and correcting persistence is the paper's response to that problem. The reported simulation indicates that residual bias is about four percent of the estimated effect under its experiment, not that every predictive regression using this proxy becomes unbiased.

There is a further practical distinction between this explanatory decomposition and a live forecast. The current year's innovation is unavailable at the start of that year. The autoregression is estimated over the historical sample rather than presented as a sequential, expanding-window forecasting exercise. The full return regression therefore cannot be traded as if every regressor were known ex ante. A real forecasting test would estimate parameters using only past information and evaluate the lagged-information component separately.

## Annual results and size exposure

Table 3, p. 46, estimates annual returns over 1964–1996. For the market, the lagged log-illiquidity coefficient is 10.226 and the unexpected-liquidity coefficient is $-23.567$. Newey–West absolute $t$ statistics are 2.74 and 4.11 respectively; $R^2=0.512$. The intercept is 14.740, reflecting the specification and units rather than a standalone estimate of an invariant equity premium.

For scale, a ten-percent increase in a level corresponds to $\log(1.10)\approx0.09531$. Multiplying by the reported slopes gives about 0.975 percentage point for the lagged-level association and $-2.246$ percentage points for a contemporaneous innovation of that log magnitude. These are calculations from fitted coefficients, not causal intervention estimates or independent forecasts.

The size-portfolio results are particularly informative:

| NYSE size decile | Lagged illiquidity slope | Unexpected illiquidity slope |
|---|---:|---:|
| 2 | 15.230 | -28.021 |
| 4 | 11.609 | -24.397 |
| 6 | 9.631 | -20.780 |
| 8 | 7.014 | -18.549 |
| 10, largest | -0.447 | -14.416 |

The unexpected-liquidity response becomes steadily less negative with size. The predictive slope declines as size increases, but the largest-decile estimate is slightly negative and statistically indistinguishable from zero: its Newey–West absolute $t$ is 0.14. This is a useful correction to reading the verbal hypothesis as if every observed predictive slope were strictly positive. The data support a relative size gradient more clearly than a universally positive estimate.

The proposed explanation combines a common discount-rate effect with a flight toward relatively liquid securities. Large stocks may still fall when aggregate liquidity deteriorates, yet fall less because they become more attractive relative to small stocks. The paper's portfolio regressions do not independently identify these mechanisms; they provide evidence consistent with the joint explanation. Odd-numbered size portfolios give qualitatively similar results, according to the source.

## Monthly tests and bond-yield controls

Monthly illiquidity averages the daily absolute-return/dollar-volume ratios across stocks and then across days. This aggregation order should be preserved, especially with an unbalanced daily panel. Its estimated autoregression has intercept 0.313, persistence 0.945, $R^2=0.89$, and adjusted persistence 0.954. The monthly return equation adds a January dummy and uses the one-month Treasury-bill rate:

$$
R_{M,m}-R_{f,m}=g_0+g_1x_{m-1}+g_2v_m+g_3J_m+w_m.
$$

Table 4, p. 49, reports $g_1=0.712$, $g_2=-5.520$, and $g_3=5.280$, with heteroskedasticity-consistent absolute $t$ statistics 2.12, 4.42, and 4.20. The fit is much lower than annually, $R^2=0.144$. The robust monthly standard errors are described as White heteroskedasticity corrections; they should not be mislabeled Newey–West as in the annual table.

The text describes 408 months during 1963–1996 and six 68-month robustness blocks. Table 4 instead labels its estimation period 1964–1996, whereas Table 5 labels 1963–1996. This is an internal sample-date ambiguity. A faithful reproduction should report its usable observations after lagging, attempt both stated conventions, and avoid asserting a uniquely established monthly row count from the article. Across the six reported blocks the lagged coefficients are all positive, averaging 0.871, and innovation coefficients all negative, averaging $-7.089$. The paper does not show that every individual block coefficient is significant.

To address alternative business-cycle information, the expanded equation includes lagged corporate default and Treasury term spreads:

$$
DEF_m=Y_{BAA,m}-Y_{AAA,m},\qquad TERM_m=Y_{long,m}-Y_{3m,m}.
$$

The source is Basic Economics. Table 5, p. 51, gives a lagged illiquidity coefficient of 0.715 with robust $t=2.18$ and an innovation coefficient of $-5.374$ with robust $t=4.39$. The default-spread coefficient is 1.193 with robust $t=2.39$; the term-spread coefficient is 0.281 with robust $t=1.70$. The latter is weaker than a blanket assertion that all predictors are strongly significant would suggest. $R^2$ rises to 0.161. Size gradients remain broadly similar after adding these controls.

## Reproduction boundaries and practical interpretation

A reconstruction should first reproduce annual stock-level diagnostics and Table 2 before attempting the aggregate regressions. The annual panel should retain the precise filters, annual characteristic freezing, two-sided trimming, delisting treatment, and portfolio-beta procedure. The aggregate analysis should use its separately stated trimming and weighting conventions, retain level and log units explicitly, estimate persistence, construct corrected innovations, and match the appropriate annual or monthly standard errors. Table coefficients provide much stronger debugging targets than matching only the final positive or negative signs.

Several inputs remain incompletely reported: exact handling of zero or missing dollar volume, every return-adjustment convention, the adjusted autoregressive intercept implementation, the Newey–West bandwidth, and a fully reconciled monthly sample calendar. There is also no code, transaction-level validation throughout the full sample, or modern out-of-sample test. These omissions limit exact numerical replication without additional decisions.

The most consequential economic limitation is joint determination. Falling prices, rising volatility, declining volume, and reduced liquidity often occur together, and the proxy mechanically uses both returns and dollar volume. The empirical design controls for several competing explanations but is not an instrumented liquidity intervention. Its expected-versus-unexpected separation relies on a parsimonious autoregressive representation and on a discount-rate argument conditional on cash-flow expectations. Different dynamics or simultaneous cash-flow news could change that decomposition.

The robust takeaway is a disciplined research architecture: distinguish relative stock illiquidity, aggregate anticipated illiquidity, and innovations in aggregate illiquidity; keep their information timing separate; and examine differential exposure across securities. The paper establishes economically interpretable historical associations and a practical long-history proxy. Turning those associations into a strategy requires a separate causal or forecasting argument, point-in-time estimation, and trading-cost and capacity analysis that this article does not supply.
