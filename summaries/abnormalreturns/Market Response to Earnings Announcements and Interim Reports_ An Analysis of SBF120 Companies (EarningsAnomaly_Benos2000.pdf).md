# Market Response to Earnings Announcements and Interim Reports: An Analysis of SBF120 Companies

Alexandros Benos and Michael Rockinger, *Annals of Economics and Statistics / Annales d'Économie et de Statistique*, no. 60, October–December 2000, 151–175. [Source PDF](../../Finance/EarningsAnomaly_Benos2000.pdf). The supplied file has a JSTOR cover followed by the 25-page article; printed page 151 is PDF page 2. All 26 supplied pages, including the French abstract, footnotes, and references, were read. There is no separate appendix.

## Why this matters

An earnings announcement is more than a signed EPS number. This study of French large and medium capitalization firms shows that prices distinguish profitability, improvement over the prior year, and performance against analyst expectations. It also finds that price volatility settles more quickly than volume, and volume more quickly than trade counts. Those separate clocks matter for execution around earnings: a market may have incorporated most of the price information while participants are still rebalancing positions.

The study's main limitation is also a useful research lesson. Its trading data are intraday, but its announcement data generally identify only the calendar day. Most firms report outside trading hours, and the authors cannot reliably distinguish a morning release from an evening release. Thus an apparent delayed response can partly reflect uncertain event alignment. Pre-announcement activity can suggest leakage or rumors, but cannot establish misconduct from these data alone.

The original contribution is an early intraday examination of earnings disclosure on the Paris Bourse, including a comparison of annual earnings announcements and semiannual interim reports. The authors combine transaction records, I/B/E/S earnings information, and manually recovered Reuters announcement dates. They extend a managerial earnings-threshold hypothesis by asking whether the market's response itself follows the same hierarchy. The theoretical discussions of adverse selection, heterogeneous beliefs, and earnings management come from earlier work; this paper's new evidence is descriptive and nonparametric, not a newly estimated structural market model.

## Historical market and reporting environment

During the 1995–1997 observation period, the Paris Bourse was a centralized electronic limit-order market. The NSC or Super-CAC system became operative in June 1995. Trading opened with a uniform-price call at 10:00 and the regular session ran to 17:00. Orders could be entered or modified from 08:30, with an indicative opening price. Continuous trading followed price and time priority. The authors describe contemporary changes in order types, minimum trade size, and negotiated block-trade rules to establish that the mechanism differs from the US settings used for comparison (pp. 154–155).

A historical naming detail matters: an order locally called a “market” order could convert into a limit order at the best opposing quote, whereas an *à tout prix* order walked the book to obtain execution. The paper also describes all-or-nothing and stop orders. These are descriptions of the sample-period system, not instructions for current French trading. A closing call was introduced for the Continu B segment in May 1996 and later extended, another reason not to assume a single unchanged auction regime throughout every comparison.

Annual accounts and interim reports were governed by different disclosure requirements and were not standardized versions of the same information package. Annual reports included consolidated accounts and definitive earnings. Some companies issued provisional annual earnings early in the year. Semiannual disclosures required commentary and sales and earnings figures but were less comparable in treatment of dilution, goodwill, EPS, and share count. Quarterly disclosures generally concerned sales rather than a complete quarterly earnings report. The distinction helps explain why an annual-versus-interim comparison is about both timing and content.

The regulator encouraged prompt releases outside trading hours. Most firms announced before the morning open or after the close; exceptional intraday announcements could trigger trading suspension. Distribution could occur by fax through a press agency, broker, or analyst. The absence of a single standardized timestamped public tape is not incidental: it directly limits the event study. The article's institutional account is historical and should not be read as a statement of current disclosure law.

## Sample formation and coverage

The study follows disclosures made during 1995–1997, associated with fiscal years 1994–1996, for firms that belonged to the SBF120. That universe includes the CAC40 and trades in the First Market monthly-settlement compartment. To limit index-membership survivorship, the authors collect information on firms that entered or left the index and on merged firms. Each year's starting universe therefore contains more than 120 names rather than a fixed end-period constituent list.

Tick-by-tick transaction prices and volumes, together with contemporaneous order-book information, come from the SBF BDM database. The main analysis uses continuous-market transactions and discards the opening call transaction. I/B/E/S International supplies market capitalization, annual EPS, and monthly analyst forecasts. The consensus is a median of forecasts. Forecasts cover the current fiscal year and two future years, although the principal surprise uses the current year's forecast made in the month before release.

The French I/B/E/S convention matters. The source states that consensus EPS generally adds back goodwill amortization, excludes extraordinary items, and does not account for dilution. It distinguishes that consensus treatment from analyst-by-analyst forecasts. A replication should match actual and expected earnings on that same basis rather than substitute a modern reported-EPS field. The paper does not provide a universal adjustment bridge across accounting data vendors.

Announcements are dated using Reuters Business Briefing, with I/B/E/S updates and, from late 1996, tentative exchange schedules used as corroboration. Exchange schedules can differ by one or two days from Reuters and were not binding. Reuters preserved dates but not a usable history of exact release hours. A tentative 1995 calendar suggests roughly 10% of firms reported in the morning, but this is not a complete firm-event time classification.

Several exclusions are necessary. Firms absent from the French I/B/E/S database are removed rather than combined with different vendors. Some stocks lack continuous-trading data for 1995 because they still traded in a twice-daily fixing segment; their relevant annual events are dropped. Recently listed companies may lack a control-period history. Other firms have missing annual or interim dates. The resulting matched panel has 276 annual earnings events and 261 interim events. Annual event counts by year are 89, 95, and 92; interim counts are 85, 92, and 84 (pp. 156–158).

Market values range from 824 million French francs to 97 billion francs, with median 6.7 billion and mean 15 billion. “Small” therefore means small relative to this major-company universe, not the full population of French microcaps. Several analyses use fewer events: the main annual surprise/return table contains 267, while the descriptive surprise table has 106, 112, and 113 companies by year. These differing coverage bases should be preserved rather than forcing every result onto the 276-event sample.

## Four definitions of news

The paper uses four measures, source equations (1)–(4), page 159. Rewriting subscripts to separate the fiscal-year comparison from the announcement-month price:

$$
SM_0=EPS_y,
$$

$$
SM_1=\frac{EPS_y-EPS_{y-1}}{P_{m-1}},\qquad SM_2=\frac{EPS_y-FY1_{m-1}}{P_{m-1}},
$$

$$
SM_3=100\log\left(\frac{S_{\tau}}{S_{\tau-1}}\right).
$$

Here $m$ is the announcement month, $FY1_{m-1}$ is the preceding month's median analyst forecast, and $P_{m-1}$ is I/B/E/S's adjusted monthly average price. $S_{\tau}$ and $S_{\tau-1}$ bracket the overnight reaction around the disclosure. The source notation uses $t$ both in its month description and in the year-to-year EPS expression; the intended comparison for $SM_1$ is the prior year's earnings, not the prior month's EPS.

$SM_0$ tests whether the firm is profitable. $SM_1$ tests whether it sustains recent earnings performance. $SM_2$ tests whether it meets analyst expectations. The latter is price-scaled unexpected earnings, not a standardized surprise divided by historical earnings volatility. The authors lack sufficient EPS history to estimate that volatility reliably and avoid a percentage earnings-change denominator because zero EPS would make it undefined.

The previous-month forecast is deliberately used because I/B/E/S consensus is usually released before the eighteenth of the month; choosing the contemporaneous monthly observation could inadvertently use information released after the earnings event. This lag protects against one specific hindsight problem but makes the forecast potentially stale. The study does not model within-month forecast revisions or management guidance between consensus measurement and release.

$SM_3$ is a realized price response, not an ex ante earnings signal. Sorting on it guarantees a strong separation of the price paths at the sorting interval. Its use is particularly important for interim reports, for which comparable analyst forecast surprises are unavailable. These portfolios can describe behavior conditional on large price changes, but their event-time jump cannot be counted as a gain earned by a trader who identifies the portfolio only after the jump.

There is a source inconsistency over the opening price. The $SM_3$ definition calls the first post-announcement transaction the opening trade, but the data section excludes the call-auction trade, and footnote 20 states that overnight returns use the first continuous-market transaction rather than the auction opening price. The latter is the explicit implemented convention for returns, but exact reconstruction of every $SM_3$ observation requires resolving the wording and event-day alignment.

## Descriptive evidence on expectations

Table 1 reports that 71.70%, 66.07%, and 76.99% of companies increased EPS in 1995, 1996, and 1997, respectively. Median price-scaled earnings changes are approximately 0.71%, 0.39%, and 0.56%. In contrast, only 31.30%, 24.11%, and 30.09% beat the analyst consensus. Median $SM_2$ is −0.49%, −0.55%, and −0.33% of price. Positive earnings growth therefore coexists with systematic disappointment relative to analysts' forecasts.

Absolute forecast errors are larger for small firms. Median absolute $SM_2$ for the largest capitalization quartile is 0.58%, 0.54%, and 0.44%, versus 0.94%, 1.10%, and 0.89% for the smallest. Reported one-sided Mann–Whitney p-values are 0.01, 0.04, and 0.00, the last being rounded rather than literally zero. These are differences in absolute error; combined with negative median surprises they are consistent with stronger forecast problems in smaller firms, but do not by themselves isolate an optimism coefficient conditional on coverage or other firm characteristics.

For the 267 annual events in Table 2, 149 have positive two-day returns and 118 negative returns. Of 67 top-quartile surprise events, 46 have positive returns and 21 negative. Of 65 bottom-quartile events, 30 have positive returns and 35 negative. Thus good surprises more clearly shift the sign frequency, while bad surprises can produce a strongly negative average through the magnitude of losses even when positive and negative signs occur almost equally often. The study uses upper and lower surprise quartiles rather than zero as its primary good/bad threshold because forecast optimism makes the distribution asymmetric.

## Event clock, control sample, and abnormal quantities

The main event window contains eight trading days, with seven continuous-trading hours per day. For price analysis an additional overnight interval is inserted for each day. Thus return charts have eight event-time intervals per trading day, whereas volume and trade-count charts have seven; the two horizontal axes are not interchangeable. The article initially describes 56 trading hours, then uses the added overnight intervals in return plots. A replication must preserve this distinction when mapping the apparently different hour cutoffs in the tests.

Hourly returns use transactions as near as possible to the start and end of the hour. The prose also says to remove the first and last transaction of each subperiod; it does not give a fully explicit algorithm reconciling that deletion with endpoint selection. If only one transaction occurs, the return uses the previous transaction on the same day. No-trade hours are omitted from relevant control calculations. Handling the first trade of the day, a no-trade previous hour, and deletion when very few trades occur needs a documented convention.

For every event, a separate control interval estimates normal behavior. Take two consecutive disclosure dates approximately six months apart, divide their gap into three subperiods, and center a twenty-day window in the middle third. If one of the two dates is unavailable, the fallback is a twenty-day window either 55 days before the interim date or 65 days after the annual date. The description does not fully specify calendar-versus-trading-day conventions for those offsets.

This control can lie after the event and therefore is an ex post benchmark, not a tradable conditional expectation available before disclosure. It is designed to be far enough from announcements to avoid contamination while reflecting changing company scale, splits, and mergers. Footnote 13 reports qualitatively similar results from some alternative common control intervals but materially different results when the control window moves closer to the event. Benchmark sensitivity is therefore established by the authors themselves.

For firm-event $i$ and hour-of-day $h$, a natural reconstruction of the plotted return adjustment is

$$
AR_{i,t}=r_{i,t}-\bar r^{control}_{i,h(t)},\qquad CAR_{g,T}=\sum_{t\leq T}\frac{1}{|g|}\sum_{i\in g}AR_{i,t}.
$$

This formula expresses the caption's comparison with corresponding control-interval returns; exact compounding versus cumulation into plotted price levels is not fully specified. It is not a market-model abnormal return and does not remove contemporaneous market or industry news. The authors explicitly decline to investigate long-horizon drift because they lack the data for the more sophisticated benchmark they consider necessary.

Volatility is an absolute hourly price change or return, displayed in percentage terms, rather than the standard deviation of intrahour returns. Volume is the amount traded during an hour, and trading intensity is the number of trades. Figures compare event quantities with average control values for the corresponding hour, using percentage deviations for volume and intensity and differences for volatility. The text alternates between share volume and value of trades without a complete monetary-volume formula; that unit choice should be checked in the underlying BDM implementation.

Control-sample box plots omit hours without transactions, average over the twenty control days, then summarize cross-sectionally. Whiskers mark the tenth and ninetieth percentiles, boxes the twenty-fifth and seventy-fifth, and the internal bar the median. These are distribution summaries, not confidence intervals. Significance shading in event bars indicates nonparametric test levels; no family-wise multiple-testing correction across the many hours is reported.

## Price response and the hierarchy of thresholds

Figures 1A–1B sort equal-weight portfolios on overnight $SM_3$. The authors describe less than 0.7% pre-event drift and a large mechanically selected jump at hour zero. For annual events, favorable-price-reaction portfolios show roughly 1.1% further drift over the next two days; adverse-reaction portfolios have an approximately −2.2% drift. Interim events show about 1.1% positive drift but little additional negative drift after the initial adverse jump. These are source-reported approximate chart magnitudes, not estimates accompanied by standard errors or net transaction-cost calculations.

Figure 2 uses the analyst forecast error for annual reports. It shows no significant pre-announcement drift by that classification. For unfavorable surprises, the prose reports approximately −0.4% in the first trading hour after announcement and another −0.2% across the next fifteen intervals, with good surprises increasing more gradually. Including overnight intervals, the source reports about +1.1% for the favorable group and −2.5% for the worst group. The text's references to “trading hours,” overnight inclusion, and different start points are not perfectly aligned, so those totals should not be mechanically summed into a reconstructed portfolio payoff.

Figures 3A–3C apply nested conditioning. The first split is profitable versus loss-making firms. Among 267 annual events, 21 report losses and 246 profits. Loss firms experience a pronounced decline that begins before the event and totals approximately −2.4% over eight days. Positive EPS alone produces little average reaction. This first result is based on a small loss-event group and cannot distinguish anticipatory public information from private leakage.

Among the 246 profitable observations, 60 have falling EPS and 186 rising EPS. Falling but positive earnings are associated with approximately −1.2% from the day before the announcement through three days after. Rising earnings generate only about +0.06% from announcement through day three. Finally, within profitable firms with rising EPS, the upper versus lower forecast-surprise quartiles show about +1.0% and −0.8% responses. Meeting the first two thresholds therefore does not eliminate the role of analyst expectations.

The authors interpret this hierarchy as evidence that the market is not fooled by earnings management. The data more directly establish conditional price patterns. They do not identify manipulated observations, estimate discretionary accruals, or compare managers facing exogenous threshold incentives. Nested sample selection also means the penalty magnitudes refer to different firm groups and sometimes different event windows. A formal claim that the market applies lexicographic decision rules would require stronger tests than visually comparing these conditional means.

## Adjustment of volatility, volume, and trade counts

Figure 4A shows the familiar U-shaped normal intraday absolute-return pattern. Figures 4B–4C show significant excess volatility around the overnight interval and first two trading hours after disclosure for both annual and interim reports. Annual events also have a late-day significant volatility increase at the 5% level. The authors suggest overseas investors could contribute because the US market opens late in the French session, but they do not identify investor nationality in the transactions.

The comparison with a four-hour response in an earlier US study is suggestive, not a controlled cross-market experiment. The historical periods, event timestamps, sample composition, and volatility definitions differ. In this paper, uncertain morning-versus-evening announcement timing also makes a precise “two-hour price discovery” conclusion fragile. The short-lived excess absolute-return response is nevertheless a clear descriptive feature of the plotted data.

Figure 5 shows a different normal volume profile: the largest share of daily volume occurs late in the session, with a midday trough. Event volume is elevated throughout the announcement day. On the following day, the first and last hours remain clearly elevated, while intermediate hours are often significant only at 10%. Trade counts remain unusually high for still longer, extending beyond the second post-event day. Visual inspection confirms that volume and intensity use seven-hour trading-day axes, unlike the overnight-augmented price figures.

The authors interpret persistent counts after volume normalizes as smaller investors reacting after institutions. That is plausible if institutions trade larger size and individuals smaller size. But the dataset does not directly label investor type, and splitting institutional orders into small executions can produce the same pattern. A falling average trade size is evidence about the transaction distribution, not proof of delayed retail learning or unequal access. Their conclusion appropriately motivates a later trade-size or investor-identity study.

## Cumulative nonparametric tests and their limits

Table 3 uses one-sided two-sample Mann–Whitney tests on cumulative excess quantities. The leakage comparison focuses on firms with absolute announcement-day $SM_3$ above the median. Pre-event cumulative volume and trade counts run through the twenty-eighth trading-hour index, while volatility runs through the thirty-first index, reflecting the different overnight clock. For bad-versus-good news and small-versus-large firms, the full event window is used.

The annual-event leakage row reports statistics −1.90 for volume, 1.45 for trading intensity, and 2.81 for volatility. The table marks intensity at 10% and volatility at 1%, with no positive-volume rejection. Interim statistics are −1.60, 1.98, and 3.50, with intensity marked at 5% and volatility at 1%. The negative volume statistics should not be called evidence of excess volume merely because their absolute values may be large; the test is directional.

For adverse versus favorable overnight reactions, annual-event statistics are −1.28 for volume, 2.10 for intensity, and 1.82 for volatility. Interim figures are −0.27, 1.41, and 2.75. The source marks positive intensity and volatility differences, with stronger volatility evidence for interim reports, but not greater volume. As the conditioning variable is itself a realized return, these tests establish asymmetry conditional on price response more directly than asymmetry conditional on an independent accounting-news instrument.

For small versus large capitalization, annual statistics are 3.19 for volume, 1.51 for intensity, and 0.64 for volatility. Interim figures are −1.52, −0.32, and 0.56, none marked significant. The annual intensity entry is labeled 5%, while a standard normal one-sided interpretation of 1.51 would imply a p-value around 0.066. Likewise the 2.10 intensity entry is labeled 1%, although its usual normal one-sided p-value is about 0.018. The article does not provide exact rank-test sample sizes or a sufficiently detailed standardization to reconcile these labels. These are reported table markings, not independently verified p-values.

Repeated firms, clustered earnings dates, and multiple comparisons across hours and outcomes can affect uncertainty. Nonparametric ranks avoid a normality assumption about the raw observations but do not automatically handle dependence. The paper does not report firm clustering, calendar clustering, or a randomization design. Its leakage interpretation is also limited by missing release hours, other corporate news, and control-window sensitivity. The stronger claim that managers deliberately leak bad news to accommodate institutions is explicitly presented by the authors as conjecture.

## Reconstructing the study without overstating it

The reproducible core is a matched firm-event panel, four distinct news definitions, an event-specific twenty-day benchmark, hour-matched deviations, equal-weight conditional price paths, and directional rank comparisons. Implementing it requires additional decisions on timestamps, opening transactions, sparse hourly trades, volume units, event-calendar offsets, and exact test standardization. Those omissions should remain visible in a replication report instead of being replaced with modern defaults and attributed to the authors.

The study contains no optimizer, cost-calibrated trading rule, out-of-sample validation, or capacity estimate. Its statement that short post-announcement drift appears unprofitable after costs is qualitative; no spread, commission, or market-impact subtraction is presented. The gross charts therefore support neither a guaranteed arbitrage nor a rigorous proof of semi-strong efficiency. What the source establishes most usefully is that the definition of earnings news and the measurement of market response both matter: profitability, growth, and consensus surprises reveal different price patterns, while prices and trading activity adjust on different observed timescales.
