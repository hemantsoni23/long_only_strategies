# Who Trades at the Close? Implications for Price Discovery, Liquidity, and Disagreement

**Vincent Bogousslavsky and Dmitriy Muravyev.** Working paper dated December 3, 2020; earlier title: *Should We Use Closing Prices? Institutional Price Pressure at the Close*. [Source PDF](../../Finance/ClosingAuctions_Bogousslavsky_2020.pdf). This note covers the supplied 67-page version, including Appendices A–D and the Internet Appendix. Main-document page numbers coincide with PDF pages; PDF pp. 57–67 contain Internet Appendix pp. IA1–IA11.

## Why this matters

The official closing transaction is a focal benchmark for institutional execution, fund valuation, index construction, and academic return measurement. It need not be the cleanest estimate of a security's contemporaneous value. This paper finds that closing auctions attract substantial liquidity-motivated trading, that the resulting difference between the auction price and the 4 p.m. midpoint is largely temporary, and that using closing transactions can create spurious option-parity violations and ETF mispricing.

The economically relevant comparison is between the official auction price and the final continuous-market midpoint. It measures the additional displacement at the auction, after any price adjustment to auction information earlier in the afternoon. It therefore does not measure the complete price effect of an order whose imbalance was announced before 4 p.m. The paper's finding that the auction itself contributes little lasting information is compatible with auction-related information being incorporated in continuous quotes beforehand.

There is a second, distinct contribution: the authors use the relative allocation of trading to the auction and to the rest of the day to construct a disagreement proxy. A rise in the share traded outside the auction predicts returns. That result is informative about differences in trading motives, but the proposed proxy is not a direct observation of heterogeneous beliefs, and the portfolio evidence is gross of trading costs.

For a quant research pipeline, the paper's most immediate implication is to maintain separate official-close and midpoint series. The official close remains relevant to a closing-price execution mandate. A synchronized midpoint can be more appropriate for cross-asset valuation, microstructure-sensitive daily returns, or measuring an arbitrage discrepancy. Replacing all closes indiscriminately would obscure that distinction.

## Sources, universe, and data construction

The principal stock sample runs from January 2010 through December 2018 and includes NYSE and Nasdaq common stocks. At the beginning of each month, a stock must have a price above \$5 and market capitalization above \$100 million. Observations with missing CRSP returns are removed. The authors exclude crossed quotes, early-closing days, and 76 apparent errors involving discrepancies larger than 10% among auction prices, CRSP closing prices, and relevant midquotes. The full sample has 5,720,876 stock-days, with 1,887 NYSE and 2,946 Nasdaq stocks; their observation shares are 47.59% and 52.41%.

Closing-auction identification is unusually important. Appendix C documents the change from monthly TAQ in 2010–2013 to daily TAQ in 2014–2018, including changes in trade-condition fields. For Nasdaq, the monthly extraction uses the appropriate `@6` condition, and the daily extraction uses `@6` while excluding duplicate `@ M` prints; NYSE uses the closing-auction condition `6`. The implementation also uses listing-exchange information, removes correction and negative-price records, and handles duplicate Nasdaq Q/M records. The supplied appendix is the specification for exact field-level filtering; a modern TAQ schema should not be assumed identical to it. ETF auctions on Arca before July 4, 2014 may consist of several prints that must be summed.

A valid auction print is found for 99.18% of NYSE and 96.01% of Nasdaq stock-days. The auction price agrees with CRSP's closing price on 98.95% of observations overall and more than 99.99% after 2014. The CRSP closing midpoint matches TAQ's 4 p.m. midpoint on 95.80%. The authors generally use CRSP midquotes because they are accessible to a broad research audience, and verify the core findings with TAQ midquotes in 2015–2018. The imperfect match is a data-quality constraint, not a negligible definition issue by assumption.

Size portfolios are formed using market capitalization at the beginning of each year. Ownership variables use beginning-of-month information. Institutional mutual-fund holdings come from Thomson/13F data. A fund is classified as passive when the Fama–French three-factor regression of its holdings-implied return has $R^2>95\%$. That is an operational classification, not a fund-label ground truth. ETF holdings come from CRSP mutual-fund data in 2010–2011 and ETF Global in 2012–2018. These choices determine both classification error and the availability lag that a replication must maintain.

The paper is not an optimization model of a fund's execution schedule. Its main objects are descriptive regressions, price-discovery statistics, and return-predictive sorts. It specifies no universal trading objective or optimal auction participation rate. Its identifying assumptions concern what kinds of investors select into each period of the trading day and whether the controls adequately separate their motives.

## Growth of auction trading and its relation to ownership

The introduction reports aggregate auction volume of \$15.2 billion per day in 2018, and an increase in aggregate auction share from 3.11% in 2010 to 7.48% in 2018. Table 1 reports a different statistic, the mean stock-day fraction: 4.13% in 2010 and 7.27% in 2018, with a full-sample mean of 5.69%. The mean fraction in the last five continuous-market minutes is 6.96%, while 3:30–3:55 p.m. accounts for 10.90%. The latter intervals have different lengths and should not be compared as per-minute intensities without dividing by their durations.

The discussion around Figure 1 also describes growth from approximately 4% to 11%. That description does not reconcile directly with the introductory aggregate endpoints or the Table 1 stock-day means. The existence of different weighting schemes explains why aggregate and equal-stock averages may differ, but it does not by itself resolve every reported endpoint. A reproduction should reconstruct each series rather than combine the three descriptions into one trend.

Table 2 regresses log turnover in different trading intervals on ownership, calendar events, and controls. The specification includes stock effects, calendar-week or month controls, linear and quadratic time trends, log turnover from 9:30 a.m. to 3:30 p.m. where relevant, volatility measured by average absolute daily return over five days including the current day, lagged return, and lagged month-end size. Standard errors are clustered by stock and date. These are explanatory contemporaneous regressions, not forecasting models with all inputs fixed before trading.

The contrast across intervals is informative:

| Regressor | Auction | Last five minutes | Intraday |
|---|---:|---:|---:|
| ETF ownership | 0.074 (0.004) | 0.037 (0.002) | 0.037 (0.003) |
| Passive mutual-fund ownership | 0.037 (0.005) | 0.006 (0.003) | 0.010 (0.006) |
| Active mutual-fund ownership | −0.005 (0.004) | 0.019 (0.002) | 0.020 (0.004) |
| Russell reconstitution | 2.307 | 0.784 | 0.078 |
| Last trading day of month | 0.869 | 0.322 | 0.008 |
| Third Friday | 0.639 | 0.125 | 0.210 |

Parentheses contain the reported standard errors for the ownership rows. Ownership coefficient magnitudes must be interpreted in the source's ownership units. Their relative pattern, rather than a unit-free elasticity claim, is the most robust reading: auction turnover is particularly sensitive to ETF and passive mutual-fund ownership, whereas active ownership is associated with turnover during the rest of the day.

There is a source interpretation issue for event indicators. With log turnover on the left, a coefficient $b$ implies the multiplicative change $e^b-1$, subject to the usual retransformation qualification. The prose treats 2.307 as approximately 230%, whereas $e^{2.307}-1$ is approximately 904%. Similarly, 0.869 implies approximately 138%, not 87%, and 0.639 implies approximately 89%, not 60%. The table coefficients are retained here; the source's percentage descriptions should not be propagated as exact transformations of them.

The earnings-event profile also differs across intervals. On an announcement date, the auction coefficient is −0.016, compared with 0.083 in the last five minutes and 0.966 intraday; the day after has −0.025, 0.019, and 0.494. Auction participation is comparatively insensitive to the informational event, consistent with liquidity-driven rebalancing. This is a relative trading-motive argument, not proof that all auction traders are uninformed.

Table 3 uses a two-step comparison. First, each stock's turnover sensitivity to ownership is estimated separately across intervals, requiring at least three years of usable data in all intervals. Second, those estimated sensitivities are regressed on interval and investor-type indicators and their interactions. Relative to active ownership, the auction interaction is 0.055 for ETF ownership, $t=7.38$, and 0.068 for passive mutual funds, $t=5.15$. Comparing the auction only with the last five minutes yields 0.034, $t=3.79$, and 0.042, $t=2.37$. The small-stock passive interaction is 0.060 with $t=1.53$, versus 0.051 with $t=2.33$ among large stocks.

This is described as a difference-in-differences comparison, but there is no randomized or externally assigned passive-ownership shock. Ownership, liquidity, and investor selection may be jointly determined. The evidence supports a systematic association between passive holdings and close concentration; it does not by itself identify the causal effect of a marginal dollar moving from active to passive management.

## Auction displacement, spreads, and the scale of the effect

Let $C_{i,t}$ denote the official auction price and $M_{i,t}^{16:00}$ the closing midpoint. The signed deviation is

$$
d_{i,t}=\log\left(\frac{C_{i,t}}{M_{i,t}^{16:00}}\right).
$$

Most magnitude statistics use $10^4|d|$ in basis points. Table 4 has 5,578,901 usable observations. Mean absolute deviation is 8.12 basis points and the median is 4.21. Mean deviation declines sharply with size: 20.60 basis points in the smallest quintile, 8.99, 5.49, 3.97, and 2.66 in the largest. The unconditional standard deviation is 15.91 basis points. The 95th, 99th, and 99.9th percentiles are 26.80, 63.13, and 195.22 basis points. The mean is therefore not an adequate description of auction risk in the tails.

The authors decompose displacement into a direction-appropriate half-spread and the residual movement beyond the relevant quote. For a close above the midpoint, the quote reference is the ask; for a close below it, the bid. An auction clearing inside the prevailing spread has negative residual impact under this decomposition. This is why the small-stock mean of 20.60 basis points can consist of a 22.19-basis-point half-spread and approximately −1.60 basis points of residual impact. For large stocks, the corresponding terms are 1.47 and 1.19 basis points, summing to 2.66. Overall they are 7.56 and 0.55 basis points; median residual impact is zero in every size group.

Thus the 8.12-basis-point headline is not all incremental market impact beyond executable continuous quotes. For smaller stocks, a substantial part is bid–ask location. For large stocks with tight spreads, the auction can move beyond the continuous quote by an economically nontrivial amount.

The paper also defines a deviation ratio as a 20-day average absolute auction displacement divided by a 20-day average absolute intraday return. Table 4's caption uses the 9:45 a.m.–3:30 p.m. intraday interval, while the text gives 9:45 a.m.–3:45 p.m. This discrepancy must be resolved in code. The reported mean ratio is 5.01%, declining from 8.68% for small stocks to 3.41% for large stocks. Its 99th percentile is 22.58% overall and 12.10% among large stocks.

Table 5 explains absolute deviation using log auction turnover, log intraday turnover, log spread, realized volatility from 3:00–3:55 p.m. and 9:30 a.m.–3:00 p.m., price, exchange, and trend controls. The dependent variable is winsorized at 0.05%, and the paper compares stock-effect and date-effect specifications with two-way clustering. In the stock-effect specification, the auction-turnover coefficient is 0.88 basis points per unit log turnover, standard error 0.05; it is 1.43 for small stocks and 0.65 for large stocks. Under date effects the overall coefficient is only 0.03 and insignificant, with −0.43 for small stocks and 0.36 for large stocks. Within-stock time-series and within-day cross-sectional associations are therefore not interchangeable.

The source prose says a 1% turnover increase generates 0.88 basis points more deviation. For a level-on-log regression, a 1% increase corresponds instead to approximately $0.88\times0.01=0.0088$ basis points. The reported coefficient should be retained while correcting the interpretation explicitly. A unit increase in log turnover is a much larger change than one percent.

At the market level the authors compute the absolute value of the capitalization-weighted *signed* deviation, $|\sum_i w_{i,t}d_{i,t}|$. This is not the weighted average of individual absolute deviations. It averages 0.93 basis points, corresponding to roughly \$3 billion of aggregate market value, and reaches about 12 basis points on August 11, 2011. Internet Appendix Table IA.3 associates larger aggregate displacement with reconstitution, month boundaries, and expiration. For example, the Russell coefficient is 1.4845 basis points, standard error 0.770, significant only at the 10% level; last-month-day and expiration coefficients are 0.5604 and 0.2509. Netting across stocks makes the aggregate statistic small relative to individual-stock displacement without making the latter irrelevant to a portfolio.

## Reversal and price discovery

The central reversal regression relates next-morning midpoint returns to auction displacement:

$$
\log\left(\frac{M_{i,t+1}^{9:45}}{C_{i,t}}\right)
=a_i+b\,d_{i,t}+c\,R_{i,t}^{15:55\to16:00}+u_{i,t+1}.
$$

The last-five-minute control is optional, corporate actions and dividends are handled, and inference clusters by stock and date. A coefficient near −1 indicates that the auction displacement is largely reversed in expectation by the next morning. It does not mean the next-morning stock return has little fundamental uncertainty.

Table 6's baseline $b$ is −0.845, standard error 0.028. It is −0.849 for small stocks and −1.096 for large stocks. With the last-five-minute control, the corresponding values are −0.872, −0.888, and −1.088. A spread-adjusted version produces −0.910 overall and −0.969 for large stocks; with the extra return control, the estimates are −0.949 and −0.985. By comparison, the unadjusted last-five-minute return coefficient is −0.186 overall, −0.285 among small stocks, and −0.175 among large stocks. The distinctive result is the near-complete mean reversal of the final auction displacement, not a claim that all late-afternoon returns reverse identically.

The regression's overall explanatory power is low, about 0.6% in the baseline. A high reversal slope on a small, noisy explanatory variable can coexist with low return predictability in a variance-explained sense. This qualification matters when translating the result into a risk budget.

As another measurement exercise, the authors compare variances of daily close-to-close returns and daily midpoint-to-midpoint returns. Stocks need at least 500 observations in the relevant size group, and returns are winsorized at 0.05%. The mean stock-level variance ratio is 1.014, rising to 1.045 among small stocks and falling to 1.003 among large stocks. For equal- and value-weighted portfolios, the ratios are 1.037 and 1.012. Closing-price noise thus affects both idiosyncratic and common return measurement, although the average magnitude differs substantially across constructions.

The weighted price-contribution statistic assigns each interval a portion of the 3:30 p.m.–next-day 9:45 a.m. return:

$$
WPC_k=\sum_i\frac{|R_i|}{\sum_j|R_j|}\frac{r_{i,k}}{R_i},
$$

where $r_{i,k}$ is stock $i$'s return in interval $k$ and $R_i$ is its total return over the broad window. Returns are winsorized at 0.005%, and both an auction and a next-morning quote must be available. Five-minute intervals are used before the close. Because individual interval contributions can be negative or exceed their eventual total, this is a signed price-contribution measure, not a nonnegative probability decomposition.

Table IA.5 gives full-sample contributions of 0.029 for the final five minutes, only 0.003 for the auction, and 0.840 for the overnight interval. For large stocks they are 0.016, 0.001, and 0.902. Spread adjustment drives the auction contribution close to zero. Small stocks have a somewhat larger auction contribution, 0.006, but it remains small relative to 0.784 overnight.

The imbalance-release analysis compares NYSE's historical 3:45 p.m. release with Nasdaq's 3:50 p.m. release, using the sample through September 2018. NYSE's relative contribution at 3:45 p.m. rises by 0.010 for small stocks and 0.004 for large stocks, followed by relative reductions at 3:50 p.m. of 0.011 and 0.007. This supports some incorporation of auction-related information before the auction. The incremental NYSE auction contribution is −0.003 for small stocks and an insignificant 0.001 for large stocks. The empirical message is therefore narrower than “closing-auction information never informs prices.”

To separate temporary auction pressure from compensation for overnight risk, the authors study post-close trades, skipping the first ten minutes to avoid guaranteed-close executions. For large stocks with eligible trades, regressions using post-close VWAPs produce reversal slopes of −0.510, −0.465, and −0.434 in the reported windows, with standard errors 0.062, 0.050, and 0.048. Spread-adjusted slopes are −0.458, −0.378, and −0.346. Samples differ across windows; the text's description of intervals and the increase in observation counts require care, so these coefficients should not be read as a clean within-stock time path. Their common implication is that substantial reversal can occur before the next regular opening, consistent with a segmented auction liquidity premium rather than exclusively overnight fundamental risk.

## Venue differences and changing liquidity at the open

NYSE auctions have larger final auction-to-midpoint deviations than Nasdaq auctions after controls. In Table 5, the large-stock stock-effect coefficient is approximately 0.94 basis points, with standard error 0.16; relative to the 2.66-basis-point large-stock mean, that is a meaningful difference. A date-effect version gives approximately 1.04 basis points. The exchange difference does not appear in the same form before the imbalance announcements, and the paper connects it to institutional auction design and participation.

This is not equivalent to a statement that NYSE has larger total impact from the first imbalance announcement onward. The benchmark here is the final midpoint. Venue changes and cross-sectional comparisons also do not randomly separate floor information, access, fee, and allocation rules. Appendix A describes the institutional setting but contains a D-order deadline inconsistent with the main text, 3:59:25 versus 3:59:50 p.m. Its description of the later NYSE cutoff change also differs from other historical accounts. These historical details should be checked against source exchange notices before a timestamp-sensitive replication.

The study links rising close concentration to a decline in opening liquidity. Its balanced sample has 333 of the largest stocks present throughout the period; 92% of observations are in the S&P 500. Regressions include stock effects, year indicators, calendar controls, price, capitalization, and volatility, plus intraday turnover in liquidity regressions. In the first fifteen minutes, turnover falls roughly 21–22%, spreads widen by about 10 basis points, and depth declines roughly 63%; the log-depth coefficient is near −1. Conditional volatility increases approximately 5–6%.

Those opening trends are potentially important to an execution scheduler: moving rebalancing demand toward the close can change where liquidity is available during the day. The balanced-panel evidence is still not a causal estimate of passive investing's effect on the open. It selects survivors, covers a changing market structure, and contains simultaneous trends in volatility and activity. A scheduler cannot take the average trend as a stock-specific optimal allocation rule.

## Disagreement proxy: construction and validation

The proposed daily disagreement proxy is

$$
D_{i,t}=-\frac{V^{\mathrm{auction}}_{i,t}}{V^{\mathrm{total}}_{i,t}},
\qquad -1\le D_{i,t}\le0.
$$

A larger value, closer to zero, means less trading is concentrated at the auction. The intuition is that benchmark rebalancing has a relatively predictable auction component, whereas greater disagreement induces more discretionary trading during the day. This interpretation requires auction rebalancing demand to be sufficiently stable, and intraday rebalancing to covary with it in an appropriate way. A numerator change caused by index reconstitution, month-end flows, or auction-specific liquidity can also change $D$ without any change in beliefs.

Weekly values average the daily ratios. They are not the ratio of aggregate weekly auction volume to aggregate weekly total volume. Mean weekly $D$ is −0.0655, with standard deviation 0.0431. The return-predictive signal is a change in this weekly measure relative to its prior-month average:

$$
\Delta D_{i,w}=D_{i,w}-\overline D_{i,\text{prior month}}.
$$

Its mean is −0.0007 and standard deviation 0.0306. The exact prior-month construction matters; replacing it by a one-week lag changes the signal.

The proxy is positively correlated with idiosyncratic volatility (0.276), log trading volume (0.237), analyst forecast dispersion (0.171), and social-media disagreement (0.067). Weekly regressions include price and size controls and week effects, clustering by stock and week. Joint coefficients on analyst and social disagreement are 0.0194, $t=9.0$, and 0.0085, $t=12.2$. The joint sample is only 252,657 stock-weeks, compared with more than one million in broader tests, so coverage changes accompany the additional validation variables.

The proxy is persistent: coefficients relating its level to the next week and to four weeks ahead are about 0.41 and 0.31 with stock and week effects. It predicts next-period volume strongly and volatility more weakly, and rises around earnings. These are useful convergent-validity tests, but they do not prove that auction share isolates disagreement independently of attention, liquidity demand, or information arrival.

## Return prediction, inference, and the limits of the trading claim

The predictive sample contains 1,084,222 stock-weeks over 447 weeks. Returns use CRSP and delisting adjustments following the referenced Shumway procedure. The authors skip one day between measuring the signal and measuring subsequent returns. Controls include prior-month idiosyncratic volatility from the Fama–French–Carhart four-factor model, momentum over months six through one, prior-month reversal, log capitalization, CAPM beta, Amihud illiquidity, and an attention/visibility measure. Visibility is high when current volume lies above the 90th or below the 10th percentile of the preceding 49-day distribution. Variables are winsorized at 0.05%. Panel regressions include week effects with stock/week clustering; Fama–MacBeth estimates are a robustness check.

Table 9's $\Delta D$ coefficient is 0.012 for the next week, $t=3.1$, and 0.033 for the next month, $t=4.7$. Multiplying the monthly coefficient by the signal standard deviation gives $0.033\times0.0306\approx0.00101$, or about 10.1 basis points of fitted monthly return per one-standard-deviation signal change. This calculation is an interpretation of the reported regression units, not the decile spread return.

The monthly coefficient is 0.055, $t=5.0$, for observations within ten days of an earnings announcement and 0.023, $t=2.7$, otherwise. A prospective use of that split requires an announcement calendar known at signal formation; the paper's retrospective event classification is not itself evidence that all such dates were available without revision.

Table 10 sorts on $\Delta D$. The equal-weight high-minus-low spread earns approximately 12 basis points over a week and 33 basis points over a month. Six-factor alpha, using market, size, value, momentum, profitability, and investment factors, is approximately 12 and 34 basis points, with $t$-statistics 3.3 and 4.9. Annualizing the monthly alpha gives roughly 4.2% compounded. The monthly long-leg alpha is approximately 38 basis points versus 4 for the low-signal leg. Newey–West standard errors use six lags to accommodate the overlapping return structure.

Internet Appendix Table IA.8 shows the monthly coefficient survives removal of visible stocks (0.034, $t=4.4$), the least liquid decile (0.025, $t=3.4$), high utilization (0.032, $t=4.6$), expensive borrow (0.030, $t=4.3$), and high volatility (0.030, $t=4.1$). The 2014-onward coefficient is 0.033, $t=3.9$. These screens limit some alternative explanations. A borrow-fee screen below 1% per year is not the same as deducting realized borrow fees from the portfolio. The level of $D$ is not the principal return predictor; its change is.

A material source inconsistency affects the claim that the auction provides a uniquely useful disagreement proxy. Table 9's last specifications include a corresponding last-five-minute measure. Its weekly coefficient is 0.011, $t=2.9$, and monthly coefficient 0.031, $t=4.3$, alongside significant auction-based coefficients. The prose on p. 28 says the pre-close measure is not significant weekly and is barely significant monthly. The table does not support that description. The 3:30–3:55 p.m. measure is indeed insignificant, but the last-five-minute comparison cannot be dismissed on the printed estimates. Any claim of unique auction superiority needs reconciliation of table and text.

The portfolio exercise does not supply turnover, spread crossing, price impact, financing, borrow-availability, or capacity-adjusted results. There is no complete walk-forward hyperparameter-selection protocol or net execution simulation. The skipped day reduces immediate timing contamination, but does not eliminate trading costs or establish out-of-sample selection robustness. The result is a promising empirical relation and a hypothesis about trading motives, not a fully specified deployable strategy.

## Options: which apparent parity violations disappear?

Appendix D.1 and Table IA.9 apply the closing-price comparison to option-implied stock values. OptionMetrics observations cover 2010–2017. Filters require bids above \$0.10, valid implied volatility and delta, maturities of 15–90 days, and near-the-money calls with delta from 0.4 to 0.6. Calls and puts are paired by strike and expiry. Dividend cash flows come from CRSP and discounting uses LIBOR.

The synthetic stock value is

$$
IS=C^{\mathrm{option}}-P^{\mathrm{option}}
+Ke^{-rT}+PV(\mathrm{dividends}).
$$

The implied bid uses call bid minus put ask; the implied ask uses call ask minus put bid. The authors take medians over eligible pairs within a stock-day. To remove persistent discrepancies related to early exercise, borrowing, and other departures from the simple parity calculation, they subtract the prior ten-day average difference between the implied midpoint and the actual stock closing price; when unavailable, that correction is set to zero. This is an empirical adjustment to an American-option setting, not a claim of exact frictionless European parity.

Among 2,500,777 stock-days, the closing transaction lies outside the implied option bid–ask interval 117,245 times, or 4.69%. Replacing the transaction by the midpoint leaves 107,041 violations: a net decline of 10,204, or 8.7%. There are 23,322 original violations that disappear and 13,118 newly introduced violations, so the net improvement is not equivalent to eliminating all old discrepancies. Among 264,664 observations with auction displacement exceeding 10 basis points, violations decline from 8,489 to 6,499, approximately 23%.

The implied-stock-minus-actual-close discrepancy predicts overnight returns with coefficient 0.124, $t=9.0$, or 0.0845, $t=5.2$, with controls. Using the stock midpoint instead reduces those values to 0.0284, $t=1.8$, and 0.0156, $t=1.5$. The text and table differ on whether the morning endpoint is 9:35 or 9:45 a.m.; Table IA.9 states 9:45. This result suggests part of apparent option-market forecasting power reflects noisy closing stock prices. It does not establish that every option signal is spurious or that every quoted parity discrepancy was an executable arbitrage.

## ETFs: correcting both sides of the valuation ratio

Appendix D.2 distinguishes an ETF's own closing-price displacement from displacement in the constituent prices used to calculate its NAV. Average absolute auction deviations are 1.68 basis points for QQQ and 1.83 for SPY, compared with 3.63 across the nine sector ETFs considered. SPY's average half-spread is only 0.29 basis points while its residual auction impact is 1.54. Tight continuous spreads therefore do not ensure an undistorted official close.

For SPY in 2018, the authors reconstruct a midpoint NAV from precise SPDR shares-outstanding and NAV data, daily ETF Global constituent holdings, and CRSP checks. Holdings mismatches are manually reconciled, cash is treated as a security, and liabilities are backed out from constituent closing values minus official total net assets. The result is checked against semiannual financial statements. The midpoint NAV replaces each constituent's closing transaction by its midpoint while retaining the reconstructed liabilities per ETF share.

Across 250 observations, mean absolute $\log(\text{ETF price}/NAV)$ is 2.50 basis points. Replacing only the ETF price with its midpoint lowers the mean to 1.59. Replacing both the ETF price and the constituent prices in NAV lowers it to 1.03. The total reduction is $1-1.03/2.50=58.8\%$. The corresponding 95th percentiles fall from 7.35 to 4.80 to 2.75 basis points. The reported pairwise differences are statistically strong, with $t$-statistics −6.91, −10.76, and −8.79 for the three comparisons.

This is a carefully reconstructed single-ETF, single-year exercise, not evidence that every ETF premium falls by 58.8%. It also highlights why simply replacing the ETF closing price while leaving constituent closing prices unchanged only partially addresses the problem. An apparent discrepancy involving auction-clearing prices on both sides is exposed to uncertain auction prices and fills; it cannot automatically be locked in as an arbitrage.

## Assessment and source map

The paper's strongest contribution is a coherent set of measurement results linking auction participation, temporary final-price displacement, and apparent cross-market valuation anomalies. Its disagreement proxy adds an interesting return-prediction application, but rests on stronger assumptions about stable rebalancing motives and is weakened by the unresolved last-five-minute comparison. Neither the ownership regressions nor the opening-liquidity trends establish a clean causal effect of passive investing.

For reproduction, the essential unresolved inputs are the conflicting intraday denominator window for the deviation ratio, the exact post-close VWAP window construction, the option-return morning endpoint, historical order deadlines, and the Table 9 text/table discrepancy. Source log-coefficient percentage interpretations also require correction. These issues do not justify discarding all reported evidence; they identify the places where an implementation should preserve the raw definitions and verify code before claiming exact numerical replication.

Sample and ownership methods are on pp. 6–12 and Appendix C, pp. 51–52. Volume regressions are Tables 1–3, pp. 40–42. Deviation and reversal evidence is Tables 4–6, pp. 43–45; price discovery and post-close evidence also use Tables IA.4–IA.6, PDF pp. 60–63. Disagreement definitions and predictive tests are on pp. 23–29, Tables 8–10, pp. 47–49, and Tables IA.7–IA.8, PDF pp. 64–65. Option and ETF construction is in Appendix D, pp. 53–56, with Tables IA.9–IA.10, PDF pp. 66–67. All findings summarized here refer to the supplied December 2020 manuscript, rather than assuming later versions have identical tables or conclusions.
