# Intra-day Patterns in the Cross-Section of Stock Returns

Steven L. Heston, Robert A. Korajczyk, and Ronnie Sadka. November 5, 2009 manuscript, marked forthcoming in the *Journal of Finance*. [Supplied PDF](../../Finance/PredictableReturns_HestonKorajczykSadka_2009.pdf). Page references below count the PDF cover as page 1; the Internet Appendix is included on PDF pages 45–59.

## Why this matters

A stock that outperforms other stocks during a particular half hour tends to outperform during the same half hour on subsequent trading days. The corresponding winner-minus-loser decile spread averages 3.01 basis points per half hour at a one-day lag, 1.09 basis points at a five-day lag, and 0.42 basis points at a forty-day lag. Returns over intervening, nonmatching half hours typically reverse. The relevant predictor is therefore the combination of a stock's relative return and its position within the trading day, rather than a single undifferentiated short-horizon momentum signal.

The practical distinction is between forecasting transaction-price movements and earning a net trading profit. Same-clock-time continuation survives quote-based returns, controls for other periodic trading variables, and several universe restrictions. Yet portfolios that cross quoted spreads when opening and closing both legs lose money. For an execution desk already required to trade, several basis points of conditional price movement can affect scheduling; for a standalone strategy, those same basis points are insufficient compensation for four spread crossings. The paper supplies evidence for the former use and an explicit obstacle to the latter.

The contribution is empirical. It identifies a sharply localized pattern in the cross-section at daily multiples of intraday lags, distinguishes this from bid–ask reversal, and documents its relation to trading activity and the clock. It does not estimate a structural equilibrium model or establish which investor class causes the effect. The explanation involving recurring execution schedules is plausible and consistent with parts of the evidence, but it is not separately identified.

## Sample and construction of the intraday clock

The principal sample runs from January 2001 through December 2005. The authors match NYSE Trade and Quote data to CRSP and use NYSE-listed common stocks with CRSP share codes 10 or 11, reporting 1,715 firms. Each regular trading day, 9:30 a.m. through 4:00 p.m., contains thirteen nonoverlapping half-hour intervals. Overnight and after-hours returns are outside the primary experiment. The regression and portfolio figures report 16,261 half-hour observations.

Let $t$ index observed half-hour intervals, $i$ index securities, and $r_{i,t}$ be the stock's return during interval $t$. At the standard thirteen-interval daily grid, lag 13 refers to the same half hour one trading day earlier, lag 26 to two days earlier, and lag 65 to five days earlier. Lag 520 corresponds to forty trading days. A faithful implementation should map these lags through a trading calendar and clock-time key; blindly shifting a compressed sequence containing shortened trading sessions or missing intervals may change the meaning. The source reports the overall interval count, while Table IV describes 1,255 observations for an individual time slot. These counts do not multiply to the aggregate count, and the treatment of incomplete days is not fully specified.

The basic returns are transaction-price returns. The quote robustness exercise instead constructs ask-to-ask, bid-to-bid, and midpoint-to-midpoint returns; the cost experiment deliberately buys at the ask and sells at the bid. These are different objects and must not be combined under one generic “return” field. The manuscript does not supply a complete TAQ cleaning specification: trade-condition exclusions, handling of corrected or out-of-sequence trades, exact boundary interpolation, stale quotes, simultaneous timestamps, and corporate-action adjustments require additional implementation decisions. A reproduction should archive those decisions and examine sensitivity, especially because the predecimal results reveal severe outliers.

There is no fitted machine-learning model, train-validation split, or hyperparameter search in the reported portfolio experiment. Signals are lagged and can be constructed at formation, but discovery and evaluation use the same historical sample. Calendar and historical-period splits are robustness checks, not a sealed prospective holdout. “Predictable” in this paper means that past information sorts future observed intraday returns, with the statistical and execution qualifications described below.

## Cross-sectional regression estimator

For every interval $t$ and each historical lag $k$, the authors estimate the cross-sectional regression

$$
r_{i,t}=\alpha_{k,t}+\gamma_{k,t}r_{i,t-k}+u_{i,t}.
$$

The main exercise uses $k=1,\ldots,65$. The reported coefficient is the time-series mean

$$
\bar\gamma_k=\frac{1}{T_k}\sum_t\widehat\gamma_{k,t}.
$$

The intercept removes the cross-sectional average return in each regression; it does not by itself remove heterogeneous market betas. The Fama–MacBeth statistic divides $\bar\gamma_k$ by the estimated standard error of its time-series mean. The authors report no significant serial correlation in the coefficient series and use simple statistics. An independent reproduction should still inspect dependence at intraday and daily seasonal lags before treating the large number of half hours as independent information. The paper does not provide a familywise or false-discovery adjustment across the many lags, times of day, universes, and auxiliary regressions.

Table I, PDF page 30, reports a strongly negative immediate-lag estimate of −5.35 with $t=-59.22$. Coefficients at the daily multiples are positive: 1.19 at lag 13 ($t=18.22$), 0.79 at lag 26 ($t=12.45$), 0.70 at lag 39 ($t=11.54$), 0.58 at lag 52 ($t=9.62$), and 0.63 at lag 65 ($t=10.57$). Figure 1 shows the same spikes against a predominantly negative short-lag background.

The source is inconsistent about coefficient scaling. Its discussion calls the displayed estimates basis points, whereas Figure 1's caption explicitly describes the coefficients “in percent.” Under the caption's convention, the displayed 1.19 means a dimensionless regression slope of 0.0119: a one-percentage-point lagged return difference predicts a 1.19-basis-point current-return difference. It does not mean a 1.19-basis-point portfolio return independent of signal magnitude. This note follows that dimensional interpretation while recording the wording conflict; the portfolio tables separately and explicitly report returns in basis points.

The Internet Appendix's Table AI, PDF page 46, estimates all 65 lagged returns jointly in each cross-section. Daily spikes remain: the reported lag-13 coefficient is 1.05 with $t=22.68$, lag 26 is 0.71 with $t=12.62$, lag 39 is 0.59 with $t=12.22$, lag 52 is 0.49 with $t=11.69$, and lag 65 is 0.38 with $t=8.93$. This rules out the simple explanation that each daily spike merely proxies for an omitted nearby lag in the univariate specification. It is still an empirical projection, without a causal interpretation or a structural restriction on expected returns.

## Portfolio algorithm and gross magnitudes

For a specified lag, rank stocks by their past return during the corresponding historical half hour, split them into ten equally populated groups, equal-weight stocks within each group, and hold the portfolios for the current half hour. Re-form the portfolios every half hour. The continuation spread is the top decile minus the bottom decile; it has one unit long and one unit short, rather than a fully invested long-only exposure. No volatility target, turnover penalty, borrowing constraint, or joint optimizer is applied to these gross-return portfolios.

Writing $W_{k,t}$ and $L_{k,t}$ for the winner and loser sets,

$$
R^{\mathrm{cont}}_{k,t}
=\frac{1}{|W_{k,t}|}\sum_{i\in W_{k,t}}r_{i,t}
-\frac{1}{|L_{k,t}|}\sum_{i\in L_{k,t}}r_{i,t}.
$$

For the nondaily benchmark, the signal averages returns over intervals preceding the same-day multiple rather than using just the matching half hour. A source inconsistency matters here: the main prose and repeated table captions say that the first-day nondaily signal uses lags 1–12, but table row labels say lags 2–12. Later daily blocks are labeled 14–25, 27–38, 40–51, and 53–64. A replication should implement both first-day variants and explicitly identify which matches the authors' results; excluding lag 1 can materially reduce bid–ask reversal. It should not silently reconcile the discrepancy by changing the stated design.

Table III, PDF page 32, gives the following all-interval spreads. Numbers are basis points per half-hour holding period; parentheses contain reported $t$ statistics.

| Lookback block | Same-clock-time winner minus loser | Nondaily winner minus loser |
|---|---:|---:|
| One day | 3.01 (22.15) | −4.67 (−28.16) |
| Two days | 1.97 (15.01) | −0.92 (−6.57) |
| Three days | 1.36 (10.75) | −0.62 (−4.62) |
| Four days | 1.26 (10.01) | −0.34 (−2.60) |
| Five days | 1.09 (8.70) | −0.06 (−0.49) |

The first-day daily spread combines a bottom-decile return of −1.35 basis points ($t=-6.18$) with a top-decile return of 1.66 basis points ($t=7.93$). The nondaily bottom decile instead earns 3.16 basis points and the top decile loses 1.51 basis points. Thus the continuation and reversal results involve both tails, although the intermediate deciles are not perfectly monotone in every row.

Table II and Figure 2 extend the individual daily-lag strategies to forty days. The spread is 0.93 basis points at lag 130 ($t=7.58$), 0.59 at lag 260 ($t=4.99$), 0.33 at lag 390 ($t=2.84$), and 0.42 at lag 520 ($t=3.67$). Persistence to forty days does not mean every intervening daily multiple is individually significant: lag 338 produces 0.05 basis points with $t=0.39$, for example. Nor are these numbers returns from continuously holding one position for forty days. Each row uses a different historical signal to forecast a new half-hour return.

Multiplying 3.01 basis points by thirteen intervals and approximately 252 trading days would produce a misleading annual opportunity estimate. It assumes repeated deployment without costs, crowding, financing, position limits, or compounding conventions and ignores the fact that signals overlap across days and securities. The paper's relevant economic unit is the half-hour spread, not an advertised annualized net Sharpe ratio.

## Time of day and microstructure

The opening and closing intervals account for a large part of the gross pattern. Table IV, PDF page 33, reports first-day daily spreads of 11.48 basis points in 9:30–10:00 ($t=12.58$), 8.42 basis points in 15:30–16:00 ($t=14.90$), and 1.75 basis points on average over the eleven intervening slots ($t=14.06$). At five days the corresponding values are 4.98, 3.50, and 0.52 basis points, with the middle-of-day average still significant at $t=4.35$.

This is not exclusively an opening or closing anomaly. Conversely, one should not interpret the positive pooled middle-of-day result as a guarantee that every individual slot and lag is positive. At five days the third half-hour slot has a reported spread of −0.68 basis points with $t=-1.27$. Figure 4 and Appendix Figure A3 display the concentration around matching clock times separately for opening, closing, and pooled middle intervals.

Transaction-price reversal can arise because trades alternate between bid and ask even when the latent efficient price is unchanged. Figure 3, PDF page 40, repeats the cross-sectional regressions using three quote-based return definitions. Continuation at daily multiples persists. Reversal beyond the immediately previous half hour largely disappears, while the first-lag negative coefficient remains. The authors interpret this as evidence of liquidity resiliency lasting more than thirty but less than sixty minutes. The interval aggregation supports that approximate bracket, not a precisely measured continuous-time recovery duration.

Table V, PDF page 34, has two additional checks that must be distinguished. Its first column restricts stocks to prices above \$5 at the preceding month-end **and value-weights** using market capitalization at the end of the preceding calendar year. This joint change yields 1.93 basis points at lag 13 ($t=10.34$), declining to 0.97 at lag 65 ($t=5.58$). It does not isolate the price filter while holding weighting constant. The second column retains stocks averaging at least ten trades per half hour during the preceding calendar month and keeps equal weighting. About 80% of firms pass this activity filter; spreads are 2.45 basis points at lag 13 ($t=18.44$) and 0.94 at lag 65 ($t=7.63$).

Size sorts use three equally populated groups based on preceding-calendar-year market capitalization, followed by the return-decile sort within each size group. Table VI and Appendix Table AV show first-day continuation of 5.16 basis points for small firms ($t=16.71$), 2.20 for medium firms ($t=14.47$), and 1.88 for large firms ($t=12.43$). Small stocks' opening spread is 20.43 basis points, versus 9.36 and 6.67 for medium and large stocks. At the close the values are 11.98, 7.08, and 8.38. The anomaly is stronger among small firms but does not disappear among the largest third of this NYSE universe.

## What happens when positions cross spreads

Table VII and Appendix Table AVI replace transaction-price returns with executable quote-side approximations. For a long position, return is from the interval's first quoted ask to its last quoted bid. For a short position, the source uses the negative return from the first quoted bid to the last quoted ask. In notation,

$$
R^{L}_{i,t}=\frac{B^{\mathrm{last}}_{i,t}}{A^{\mathrm{first}}_{i,t}}-1,
\qquad
R^{S}_{i,t}=-\left(\frac{A^{\mathrm{last}}_{i,t}}{B^{\mathrm{first}}_{i,t}}-1\right).
$$

The short convention is the paper's return normalization; actual broker cash-flow and margin accounting should be specified separately. Continuation buys winners and shorts losers, while the nondaily cost table reverses its gross-table sign and implements the contrarian trade, buying losers and shorting winners. Missing this sign switch would incorrectly describe the cost experiment.

Only firms whose initial relative quoted spread is no greater than ten basis points are included in each interval. The authors report similar qualitative results for five- and twenty-five-basis-point thresholds. Even with this restriction, first-day continuation earns −23.78 basis points for small stocks ($t=-28.37$), −18.58 for medium stocks ($t=-49.79$), and −13.25 for large stocks ($t=-46.50$). The large-stock closing result, where the gross effect is substantial, is still −5.84 basis points ($t=-8.96$). The continuation cells remain negative across the tabulated days and time partitions, although some noisy opening-cell estimates are not individually significant.

This is a stronger implementation warning than simply observing high turnover. The experiment directly crosses the displayed sides of the spread for both legs. It still omits commissions, fees or rebates, impact, queue priority, failed fills, locate availability, borrow charges, and execution delays. Quote prices are therefore a stylized execution bound, not guaranteed fills. A passive strategy might avoid some spread costs, but its fill selection and inventory exposure are not tested here.

Gross and net tables also use different filters. Subtracting their means and dividing by four is not an exact estimate of a common one-way spread cost for an identical portfolio. The authors' rough four-to-seven-basis-point one-way-cost discussion should be read as an economic illustration. For preexisting buy or sell orders, the possible benefit is improved timing conditional on the stock's recent same-clock-time relative performance; the paper does not optimize a schedule subject to a participation limit or show realized implementation shortfall savings.

## Risk, volume, volatility, and order flow

Appendix Table AVII, PDF page 52, regresses the portfolio spreads on the equal-weighted market return, together with thirteen leads and thirteen lags of that market return. Thus there are 27 market-return regressors plus an intercept. The leads help diagnose nonsynchronous-trading exposure in an ex post risk adjustment; they are not inputs available to a live return forecast. The first-day continuation intercept is 3.03 basis points ($t=22.33$), almost identical to the raw 3.01. Nondaily reversal becomes −4.65 basis points ($t=-28.26$). Market adjustment of this form therefore explains little of the reported pattern, but it is not a comprehensive intraday factor model.

The trading-variable analysis repeats lagged cross-sectional regressions for volume, volatility, quoted spread, and order imbalance. Volume is shares traded and enters as the logarithm of its ratio to the preceding interval's volume. Volatility is the absolute half-hour return, likewise transformed by a log ratio. Relative spread is quoted ask minus bid divided by the quote midpoint, measured from the first quote in the interval, and also enters in log changes. Zero volume and zero absolute returns make these logarithms undefined; the source does not fully document their treatment.

The figure captions define imbalance as buyer-initiated volume minus seller-initiated volume divided by their sum, and use its first difference. Some prose describes net signed shares without stating this normalization. The normalized caption definition is the clearest operational specification, but a reproduction should record that ambiguity. Trade direction uses a Lee–Ready-style classification without the original five-second quote delay.

Figure 5, PDF page 42, restricts initial relative spreads to at most twenty-five basis points. Changes in volume and volatility show clear daily periodicity. Spread changes do not display the same regular sequence of daily spikes, and order-imbalance changes provide weaker evidence. This qualifies the abstract and introductory wording that groups bid–ask spreads with other periodic variables: the later discussion and the plotted spread panel do not support equally strong spread periodicity. Appendix Figure A1 extends volume-change periodicity through forty days.

Return regressions then add lagged changes in these variables at the same lag as the return predictor. The daily return coefficient survives. This means the chosen lagged linear controls fail to absorb the effect; it does not prove that trading activity or inventory dynamics play no causal role. Noisy measurements, nonlinear responses, contemporaneous flow, or omitted investor heterogeneity can remain relevant.

The authors split trades below 1,000 shares from trades of at least 1,000 shares and construct separate volume and imbalance measures. Figure 6 and Appendix Figure A2 again leave daily return predictability after controlling for both groups. Trade size is an imperfect investor-type proxy, especially when institutional orders are split into small executions. The results cannot establish that individual investors, institutions, or algorithms uniquely generate the pattern.

## Calendar, index membership, frequency, and historical regimes

Appendix Table AVIII shows positive first-day continuation on each weekday: the all-interval mean ranges from 2.62 basis points on Tuesdays to 3.44 on Wednesdays. Nondaily reversal ranges from −3.51 on Thursdays to −6.14 on Mondays. Appendix Table AIX reports positive first-day continuation in every calendar month, from 1.70 basis points in March to 3.82 in January; November is 3.80 with $t=7.80$, not a 7.80-basis-point return. Later-lag monthly estimates are less uniformly significant.

Turn-of-month days mean the first and last trading days of each month. Appendix Table AX reports first-day daily continuation of 1.95 basis points on those days ($t=4.50$), compared with 3.12 elsewhere ($t=21.81$). The pattern is therefore not generated exclusively by month-end or month-start trading, though magnitudes differ and the smaller subgroup has less precision.

Appendix Table AXI partitions the portfolios by S&P 500 membership. First-day continuation is 2.19 basis points for index stocks and 3.28 for nonmembers. Index constituents have a particularly pronounced close: 9.42 basis points in the final interval versus 0.98 in the middle intervals. Their nondaily all-interval reversal is only −0.72, versus −5.58 for nonmembers. These observations are consistent with differences in index-related execution but membership is correlated with size and liquidity; this is not a causal index-inclusion experiment.

Figure 7 uses five-minute intervals, 78 per regular day, with daily lags at multiples of 78 through 390. Its actual sample is January 2004 through December 2005, with 39,244 intervals, rather than the entire five-year main sample. Daily spikes remain at this finer resolution. The different sample and noisier individual coefficients prevent treating it as a clean frequency change with every other feature fixed.

Table VIII compares tick regimes: January 1, 1993–June 23, 1997, with eighth-dollar ticks and 14,190 intervals; June 24, 1997–December 31, 2000, with sixteenth-dollar ticks and 11,506 intervals; and decimal trading in 2001–2005. Raw first-day spreads are 2.88 basis points ($t=4.90$), −10.30 ($t=-0.84$), and 3.01 ($t=22.15$), respectively. The middle regime contains extreme estimates, including 69.61 basis points at the three-day lag with $t=1.31$, exposing substantial outlier sensitivity.

The winsorized panel clips portfolio returns at the first and ninety-ninth percentiles within calendar months. Its caption says the distribution is across all strategies, while the discussion is less explicit about pooling, so both the clipping population and thresholds need confirmation. Winsorized first-day spreads are 2.28, 3.43, and 2.90 basis points, with $t$ statistics 15.22, 18.27, and 22.89. Five-day values are 0.69, 1.12, and 1.13. This supports a historical pattern but not a monotone increase in economic magnitude with algorithmic trading. Clipping realized returns is also a statistical robustness transformation, not a trading rule that could have removed adverse observations in real time.

## Reimplementation priorities and limits

The core experiment is reproducible in structure: build a point-in-time NYSE common-stock universe, create a clean regular-session intraday calendar, maintain separate trade and quote returns, generate matching-clock-time and nondaily signals, rank within the chosen universe, and retain interval-level portfolio returns and cross-sectional coefficients. Reproduce the gross tables before adding filters, then reproduce quote-return diagnostics and the spread-crossing experiment using their actual distinct weighting and eligibility rules. Preserve the long and short legs separately so that signs, costs, and capital normalization are auditable.

Three specification ambiguities deserve explicit variants: first-day nondaily lags 1–12 versus 2–12; imbalance in normalized versus unnormalized units; and monthly winsorization within each strategy versus pooling strategies. Calendar treatment, TAQ condition filters, and zero-log observations require further data-engineering choices. None should be represented as a documented author setting when the PDF does not supply it.

For a new research implementation, daily block resampling or serial-dependence-robust inference, an untouched later-period evaluation, and economically realistic fills would be useful extensions. Those are proposed checks, not results reported by the authors. The supplied paper gives no post-2005 stability evidence, capacity curve, portfolio-level drawdown history, complete turnover accounting, or executable net strategy. Its durable finding is a clock-specific conditional pattern in cross-sectional price changes, accompanied by unusually direct evidence that a naive aggressive trading strategy cannot capture it after spreads.

## Source record and related work

Heston, S. L., R. A. Korajczyk, and R. Sadka (2009), *Intra-day Patterns in the Cross-Section of Stock Returns*, supplied November manuscript. The entire 59-page file, including Internet Appendix Tables AI–AXI and Figures A1–A3, was read. The main regression and portfolio design is on PDF pages 6–13; implementation and microstructure checks on pages 13–19; periodic trading variables and robustness on pages 19–27; Tables I–VIII on pages 30–37; Figures 1–7 on pages 38–44; appendix evidence on pages 46–59. Critical table and figure pages were visually inspected in addition to text extraction.

The manuscript's methodological references include Fama and MacBeth (1973) for averaging cross-sectional slopes, Dimson (1979) for lead–lag market-risk adjustment, and Lee and Ready (1991) for trade-direction inference. Those works explain the statistical building blocks; this note's numerical statements and source qualifications are grounded in the supplied Heston–Korajczyk–Sadka file rather than in separate re-estimates of those references.
