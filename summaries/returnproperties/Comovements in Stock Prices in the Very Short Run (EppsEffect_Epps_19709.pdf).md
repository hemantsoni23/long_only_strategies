# Comovements in Stock Prices in the Very Short Run

**Thomas W. Epps (1979).** *Journal of the American Statistical Association* 74(366), 291–298, Applications Section. The source filename has a typographical year, `19709`; the article itself is dated June 1979. Source: [original PDF](../../Finance/EppsEffect_Epps_19709.pdf). This note follows the eight article pages, including all six tables; the PDF's first page is a bibliographic wrapper.

## Why this matters

A covariance matrix estimated from very short returns can make closely related businesses appear almost unrelated. Epps demonstrates this with four US automakers: Ford–GM return correlation is only 0.055 at ten minutes, compared with 0.519 at three hours and 0.645 at three days. The economic exposures have not disappeared merely because the sampling interval is shorter. The measured relation depends on how price observations are formed, when transactions occur, intraday variation in volatility, and the time over which information is reflected in trades.

The paper also distinguishes statistical predictability from a realizable trading profit. A last transaction price can be stale; successive transactions can alternate between the bid and ask; and being able to predict a recorded print does not imply being able to buy or sell at that print. These distinctions are useful both for estimating portfolio risk and for evaluating high-frequency signals. The paper's empirical results concern four stocks in 1971–1972, not a universal numerical correction for modern markets.

Its contribution is an unusually concrete decomposition of the problem. First it documents the relation between measurement interval and contemporaneous correlation. It then examines within-day heterogeneity, own-stock reversals, and cross-stock lagged responses. Finally it constructs two transaction-timing tests intended to separate mechanical recording effects from information adjustment. The conclusion is qualified: some information appears to propagate with delay, but the surviving effects are small and do not establish an implementable strategy for an ordinary investor.

## Data, timestamps, and return construction

The securities are American Motors Corporation, Chrysler, Ford, and General Motors, abbreviated AMC, C, F, and GM. They were selected deliberately because they constituted the main domestic automobile industry, were not highly diversified firms, and were expected to have strongly related longer-period returns. This is an illustrative industry sample, not a random cross-section of equities.

The initial data cover all 125 trading days in the first six months of 1971. The source is F. E. Fitch records of the price and time of every NYSE transaction. The trading day lasts five and a half hours. Epps records prices at 33 ten-minute endpoints, from 10:10 through 15:30 Eastern US time. At a clock time $t$, the recorded observation is the price of the last transaction at or before that time, with transaction times available to the nearest minute. This is previous-transaction sampling, rather than a simultaneous executable quotation for every stock.

Write the sampled log price as $p_{i,t}=\log P_{i,t}$ and the basic change as $r_{i,t}=p_{i,t}-p_{i,t-1}$. The first ten-minute observation on a day is special: it subtracts the previous day's 15:30 closing log price from the current day's 10:10 log price. It therefore contains the overnight change as well as the opening ten minutes. Treating all 33 observations as economically identical ten-minute returns would misrepresent the paper's data.

For the correlations in Table 1, longer-horizon changes are nonoverlapping sums of successive basic log-price changes. A one-hour return, for example, sums six successive ten-minute changes. These sums are formed without adjusting for the fact that the trading day contains 33, rather than a multiple of six, basic intervals. The resulting sequence must be reproduced as defined; replacing it with a new set of within-day clock-hour returns changes the experiment. The paper does not provide source code, a detailed holiday calendar, or an explicit missing-transaction handling algorithm beyond previous-transaction sampling.

For the intraday variance and lag analysis, Epps constructs a different set of observations. Each day is split into six intervals ending at 10:30, 11:30, 12:30, 13:30, 14:30, and 15:30. The 10:30 return starts at the preceding day's 15:30 observation; the remaining five are one-hour returns. Each stock–hour pair is treated as a separate variable observed across days. This avoids imposing constant variance across clock hours. Table 2 and Table 3 use the first-half-1971 sample. Importantly, Table 4 and the subsequent tests and simulations use **the full year 1972**, except where the final trading experiment explicitly splits that year into estimation and evaluation halves. The paper says analogous 1971 regression results were similar, but does not report them.

## The correlation pattern and its statistical meaning

Selected entries of Table 1, p. 291, are reproduced numerically below. The entries are correlations, not percentages.

| Measurement interval | AMC–Chrysler | Chrysler–Ford | Chrysler–GM | Ford–GM |
|---|---:|---:|---:|---:|
| 10 minutes | 0.001 | −0.014 | 0.007 | 0.055 |
| 20 minutes | 0.009 | 0.017 | 0.026 | 0.118 |
| 40 minutes | 0.006 | 0.041 | 0.040 | 0.197 |
| One hour | −0.043 | 0.023 | 0.065 | 0.294 |
| Two hours | 0.029 | 0.112 | 0.129 | 0.383 |
| Three hours | 0.031 | 0.361 | 0.518 | 0.519 |
| One day | −0.067 | 0.342 | 0.442 | 0.571 |
| Two days | −0.020 | 0.336 | 0.449 | 0.572 |
| Three days | −0.098 | 0.334 | 0.542 | 0.645 |

AMC is weakly related to the other manufacturers even at longer horizons. The clearest result is therefore the convergence toward low short-interval correlations among Chrysler, Ford, and GM, not a claim that every pair has a large daily correlation. Nor are all correlation sequences monotonically increasing at every horizon. The economically striking observation is the general decline below roughly three hours.

Epps gives a simple aggregation argument to identify what must fail for correlation to depend on horizon. Suppose two zero-mean stationary series $x_t,y_t$ have contemporaneous covariance $\gamma_{xy}(0)$ but no nonzero-lag own or cross covariances. For nonoverlapping $k$-period sums,

$$
X_t^{(k)}=\sum_{a=0}^{k-1}x_{t-a},\qquad
Y_t^{(k)}=\sum_{a=0}^{k-1}y_{t-a},
$$

we obtain $\operatorname{Cov}(X^{(k)},Y^{(k)})=k\gamma_{xy}(0)$ and variances $k\gamma_x(0),k\gamma_y(0)$. Correlation is consequently independent of $k$. The empirical horizon dependence indicates that stationarity, absence of lagged dependence, or both are unsuitable assumptions.

A useful explicit expansion of the same argument is

$$
\operatorname{Cov}(X_t^{(k)},Y_t^{(k)})
=\sum_{a=0}^{k-1}\sum_{b=0}^{k-1}\operatorname{Cov}(x_{t-a},y_{t-b}).
$$

This expansion is explanatory algebra, not an additional estimated model in the article. It makes clear why lagged cross-stock responses enter long-horizon contemporaneous covariance, and why own-stock serial covariance also changes the denominator of a correlation. A shorter horizon can remove economically relevant shared movement from the contemporaneous covariance without removing it from the full lead–lag system.

## Intraday heterogeneity and regression design

Table 2 reports variances multiplied by $10^4$. Ford's variance is 0.34 at the overnight-to-10:30 interval, then 0.28, 0.19, 0.10, 0.10, and 0.16 across the five following hours. GM's corresponding values are 0.27, 0.20, 0.13, 0.08, 0.09, and 0.15. For Chrysler they are 1.28, 1.39, 0.66, 0.59, 0.58, and 0.72; for AMC, 2.25, 3.10, 2.02, 1.93, 1.93, and 2.02. For every stock the 11:30-ending return has the greatest variance among the five purely intraday hours, followed by a midday decline and a later rise.

Thus removing the overnight interval does not produce a constant-variance hourly process. Epps suggests reduced lunchtime trading as an explanation, but does not identify it causally. Normal-theory likelihood-ratio tests of equality of the five hourly variances give small tail probabilities; the paper explicitly cautions that log-price changes may violate normality. These tests support a descriptive pattern, not a fully specified seasonal volatility model.

Table 3 contains correlations across the five intraday hours, separately by stock and clock time. Tests are two-sided at the 10% level. The paper uses the distributional transformation $(1+r)/(1-r)$ and an $F(n-2,n-2)$ reference under zero correlation, following its cited source, and ignores dependence among the many correlation tests. A modern reproduction should distinguish reproducing this historical procedure from replacing it with a preferred contemporary inference method.

Among same-stock correlations one hour apart, 13 of 16 are negative. Among cross-stock correlations at that separation, 33 of 48 are positive. The direction suggests own-stock reversal alongside industry information transmitted across stocks. This is a descriptive sign pattern; the paper does not supply a multiple-testing-adjusted joint interpretation for Table 3.

For Table 4, define $r_{i,h,d}$ as the log-price change for stock $i$ in the interval ending at hour label $h$ on day $d$, where $h=10$ denotes the 10:30 interval. For each stock and each $h=11,\ldots,15$, estimate a separate regression

$$
r_{i,h,d}=a_{i,h}+\sum_{j\in\{A,C,F,G\}}\sum_{s=10}^{h-1}
 b_{i,h;j,s}r_{j,s,d}+u_{i,h,d}.
$$

This compact notation reconstructs the equations described on pp. 293–294. The 11:30 regression has four regressors, the 12:30 regression eight, and the 15:30 regression twenty, plus an intercept in each case. There are twenty regressions overall. All predictors precede the dependent interval; the design does not regress a current return on a simultaneously observed return in another stock. Intercepts are estimated but omitted from the displayed table.

Table 4 shows slope coefficients, individual 10% significance marks, joint $F$-test probabilities for all slopes, and unadjusted $R^2$. Most salient coefficients concern the immediately preceding hour. To summarize these, the article averages corresponding coefficients across the five clock-hour models using **inverse standard errors**, not inverse variances, as weights. The resulting own-stock coefficients are −0.30 for AMC, −0.16 for Chrysler, −0.07 for Ford, and −0.06 for GM. Positive weighted cross effects include Chrysler's preceding return in the AMC equation, 0.20, and GM's preceding return in the AMC equation, 0.25. These averages describe the estimated system; they are not coefficients of one pooled stationary vector autoregression.

## Competing mechanisms

The paper discusses three distinct sources of dependence, plus a possible block-trade contribution.

**Bid–ask transaction bounce.** If a market sell prints at the bid and the next transaction is a market buy at the ask, the observed transaction return reverses even when both quotations remain unchanged. Limit-order queues create temporary barriers within which transaction prices move. Negative serial dependence in prints can therefore coexist with unpredictable executable quotations. An investor buying after a downtick generally pays the ask, not the previous bid print, and selling later generally receives the bid. The apparent reversal is not automatically a capturable gain.

**Delayed information adjustment.** Information may reach traders at different times. If multiple trades must exhaust a limit-order queue before a quote changes, information can produce different adjustment delays across securities. Alternatively, traders may specialize in one or a few manufacturers, so news arrives through different trading decisions. The order of adjustment need not be fixed: different stocks can lead on different occasions. The paper's supporting fund-holdings evidence covers 49 mutual funds holding automobile shares during 1968–1972: 28 held one automobile stock, 15 held two, six held three, and none held all four. This supports specialization as plausible, but net holdings do not identify all underlying trades or prove the mechanism.

**Asynchronous last-transaction sampling, called the Fisher effect here.** All quotations could react immediately to common information, while the first subsequent trade occurs in only one stock before a sampling cutoff. The remaining stocks then appear to react in the next interval because their recorded last transactions were stale. This creates positive lagged cross-stock dependence without genuine quotation predictability. Information arriving at 11:25, followed by a GM trade before 11:30 and other manufacturers' trades after 11:30, is the paper's illustrative timing pattern.

**Block-trade reversals.** Large transactions can temporarily displace prices and subsequently reverse. Such events near sampling boundaries could generate additional negative serial dependence. The paper proposes this as a possible contributor and does not estimate a separate block-trade model.

The distinction matters for identification: a regression on prints alone cannot discriminate delayed economic adjustment from asynchronous observation. Epps lacks hourly bid and ask quotations and therefore uses indirect timing tests.

## Two tests designed to remove mechanical dependence

The first test retains the same last-to-last return definition and regression structure, but selects days separately for each dependent stock and hour. A day is eligible when that stock was the **last of the four to trade in the preceding hour**. Under the simultaneous-quotation-adjustment explanation, its preceding recorded price should then incorporate information at least as recent as that incorporated in the other stocks' preceding observations. Other stocks' lagged returns should lose their incremental predictive ability if asynchronous recording alone caused the relation.

Table 5 reports the resulting regressions and tests whether the cross-stock, rather than every, slope is zero. Sample sizes are small: for example, the four 11:30 equations use 26, 42, 18, and 47 observations. One late-day regression has too few degrees of freedom to estimate all twenty slopes, so only the preceding 14:30 returns are used in that case. The broad results are consistent with mechanical asynchrony explaining much of the cross-predictability, but they are not decisive. Forty-two of sixty immediately preceding-hour cross-stock coefficients remain positive. Selection also sacrifices power and may eliminate observations informative about real delayed adjustment. Failure to reject is therefore not evidence that all information adjusts instantaneously.

The second test uses all available days but changes the dependent variable. Instead of the return between the last transactions in successive hours, it uses the difference between the log prices of the **first and last trades within the dependent hour**. The lagged predictors remain the earlier-hour last-to-last changes. When quotes adjust simultaneously, a common price change before the first current-hour trade should already be incorporated in that first price; the within-hour dependent return excludes it. The construction also removes the shared boundary transaction responsible for the simplest bid–ask-bounce explanation of own-stock reversal.

Table 6 shows that negative own effects and positive cross effects persist, though they weaken substantially. The inverse-standard-error weighted own coefficients become −0.03, −0.10, −0.02, and −0.02 for AMC, Chrysler, Ford, and GM respectively. Compared with Table 4, AMC's own reversal in particular shrinks sharply. Cross effects also contract: the weighted GM-to-AMC slope is 0.11 rather than 0.25. Most individual equations have modest explanatory power; Table 6's unadjusted $R^2$ values range from about 0.01 to 0.18.

Epps reports that aggregating the twenty regression significance tests by Fisher's procedure yields significance at the 0.001 level **if the regressions are treated as independent**; a similar statement applies to the twenty cross-stock tests. Because they share stocks, days, and overlapping information, independence is a material assumption, not an established property. The source does not supply a dependence-robust aggregate test. The defensible conclusion is evidence of weak residual lagged relationships under these sampling controls, rather than an exact estimate of the speed of efficient-price adjustment.

## Trading experiment and practical limits

For a limited out-of-sample check, coefficients of the second-test regressions are estimated on the first half of 1972 and used to forecast returns in the second half. A position of 100 shares is opened at the first recorded trade in an hour and closed at its last recorded trade whenever the predicted change exceeds a tolerance. The tolerances are zero, one eighth, one quarter, or three eighths of a dollar. Because the statistical regressions use log-price changes while these thresholds are in price dollars, an implementation needs a price conversion; the article does not spell out the exact conversion and rounding convention.

Before transaction costs, these rules generally generate small positive profits. The highest example cited is about \$23 per trade for Chrysler at a quarter-dollar threshold. The detailed trade counts, full distribution of outcomes, and complete simulation tables are not included; the article offers further details on request. There is no reported modern Sharpe ratio, capacity estimate, drawdown analysis, or uncertainty interval for that profit.

The execution assumption is explicitly suspect. A trader cannot generally guarantee execution at the first and last historical prints, nor know in advance which transaction will be the last in an hour. Spreads, commissions, latency, and short-sale arrangements are not fully modeled. Epps concludes that costs would make these rules unprofitable for nonmembers of the exchange, while leaving open small opportunities for specialists or floor traders. The evidence should therefore be read as an economic scale check on residual predictability, not a production trading backtest.

Finally, the paper finds that predictive influence does not seem to last much beyond one hour. Comparable ten-minute within-interval regressions using only the immediately preceding ten-minute returns show no detectable explanatory power. Epps interprets the limited evidence as suggesting an average response lag longer than ten minutes. This is a tentative inference from low-powered tests and particular timing constructions; it does not identify a point-valued latency parameter.

## Reproduction priorities and takeaways

A faithful replication should first rebuild transaction timestamps, the previous-trade sampling rule, and the overnight interval exactly. It should separately reproduce Table 1's nonoverlapping aggregation and the clock-hour panels used in Tables 2–6. Mixing those constructions would obscure the reason for the different experiments. The 1971 descriptive sample, 1972 regressions, and 1972 half-year forecasting split must remain distinct.

Next, estimate each stock–hour equation with its expanding set of earlier-hour predictors, retain the reported intercepts even though the table omits them, and match the historical significance and inverse-standard-error averaging conventions before introducing robustness alternatives. For the timing tests, record the identity of the last trader before each boundary and the first and last transaction prices inside each dependent hour. The publication leaves same-minute timestamp ties, exceptional days, and some missing-data details unspecified; these require documented choices, not assumptions attributed to Epps.

The general lesson is that correlation is a property of a return measurement system as well as of the underlying securities. More frequent observations can yield less contemporaneous correlation because shared movement is spread across recorded time. Residual print predictability is a separate question from quotation predictability, and both are separate from net trading profitability. The paper provides a small, transparent empirical framework for keeping those questions distinct.
