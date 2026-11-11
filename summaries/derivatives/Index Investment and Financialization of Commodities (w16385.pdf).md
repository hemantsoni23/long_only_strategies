# Index Investment and Financialization of Commodities

Ke Tang and Wei Xiong, NBER Working Paper 16385, September 2010. [Source PDF](../../Finance/futures/w16385.pdf). This note concerns the supplied 51-page working-paper version, including its thirteen figures and seven tables, rather than a later published revision. After the cover, PDF page numbers are one greater than printed page numbers. There is no separately labeled appendix in this file.

## Why this matters

Commodity diversification depends on how prices move together, not just on whether individual commodities have positive expected returns. A portfolio containing many economically different raw materials can acquire a common financial exposure when investors trade those materials together through indices. Tang and Xiong document a pronounced increase in commodity return dependence after 2004 and ask whether the increase is especially large for commodities included in the GSCI or DJ-UBS indices.

The contribution is a comparison across indexed and off-index commodities, supported by historical sector correlations, Chinese futures markets, trader-position data, and regressions allowing factor exposures to change over time. The central finding is an additional upward trend in indexed non-energy commodities' exposure to oil. It is already visible before the acute financial crisis. The paper also finds larger increases in squared returns for indexed commodities and a reduction in that difference after filtering oil exposure.

These are observations about market integration and risk. They are not an out-of-sample trading strategy, an estimate of the welfare effect of speculation, or a clean causal estimate of how much index investment raised commodity price levels. Index membership is not randomly assigned, the 2004 break is imposed, and index flows are observed only from 2006. The note therefore separates the source's financialization interpretation from the statistical quantities actually estimated.

## Universe and daily return construction

Section I and Table 1 describe 28 US-traded commodity futures series, divided into five sectors. Energy contains WTI crude, heating oil, RBOB gasoline, and natural gas. Grains contain corn, soybeans, Chicago wheat, Kansas wheat, soybean oil, Minneapolis wheat, soybean meal, rough rice, and oats. Softs contain coffee, cotton, sugar, cocoa, lumber, and orange juice. Livestock contains feeder cattle, lean hogs, live cattle, and pork bellies. Metals contain gold, silver, copper, platinum, and palladium. The study uses the commodities active in its historical setting; it is not a contemporary futures-universe specification.

Pinnacle Data supplies daily futures prices and open interest. Bloomberg and Datastream provide financial and macroeconomic series, and Wind provides the Chinese commodity data. Table 1 records the available histories, contract calendars, and 2008 index weights. Dates in that table should be treated as the source's series-start information rather than automatically interpreted as the first trading date of every historical predecessor contract.

An indexed commodity belongs to either GSCI or DJ-UBS. On the table's classification, all four energy commodities and fifteen of the twenty-four non-energy commodities are indexed. The nine off-index non-energy commodities are Minneapolis wheat, soybean meal, rough rice, oats, lumber, orange juice, pork bellies, platinum, and palladium. This classification is a union, not the intersection of the indices. Copper is represented using NYMEX contracts, following DJ-UBS; GSCI uses London copper. London-traded metals and Brent are excluded from the analysis to reduce asynchronous-closing problems.

Several contract exclusions matter. Lean hogs' June contract, introduced in 2002, is omitted because of low open interest. For gold, silver, platinum, and palladium, the authors omit the short contracts described in Table 1's footnote as the current month and next two consecutive months, and use the listed delivery cycles. Those cycles are February, April, June, August, October, and December for gold; March, May, July, September, and December for silver; January, April, July, and October for platinum; and March, June, September, and December for palladium. An implementation that selects the shortest exchange-listed contract without these exclusions will not reproduce the source.

The hypothetical commodity investment holds the first eligible contract until the seventh calendar day of its maturity month and then rolls into the next contract. This deliberately simplifies the actual index convention of rolling 20% per day over the fifth through ninth business days. On a non-roll day, the paper defines

$$
R_{i,t}=\log F_{i,t,T_1}-\log F_{i,t-1,T_1},
$$

where $F_{i,t,T_1}$ is the futures price of commodity $i$ at date $t$ for maturity $T_1$. It calls this the excess return on a fully collateralized position, because collateral can separately earn interest. Strictly, the displayed expression is a log price change; the arithmetic fully collateralized futures gain relative to previous notional is $F_t/F_{t-1}-1$. They agree to first order, not exactly.

The roll-day description says that the return incorporates both the futures price change and the ratio between first- and second-month contracts, but does not provide a complete roll-day formula. A roll spread is not itself an instantaneous cash gain when one closes a futures position and opens another. Reproduction requires the original chaining convention, not an assumed back-adjusted continuous series. Missing-price handling, nontrading seventh-calendar-day treatment, contract multipliers, holiday matching, and the exact collateral-account convention are also not supplied as executable rules. These are source limitations, not invitations to silently impose a standard vendor convention.

## Descriptive evidence and alternative mechanisms

For Figure 2, each commodity's daily returns are demeaned and divided by their standard deviation within a one-year rolling window. A regression of one standardized return on another then gives the sample correlation in that window. The figure includes 95% confidence bands. Early oil observations in 1983–1984 are skipped for liquidity concerns, so the oil-pair rolling series begins in 1986 after a year of usable returns. The copper comparison begins in 1990, and the GSCI energy/non-energy comparison begins in 1983.

Before 2004, oil's rolling correlations with soybeans, cotton, and live cattle are generally small. The source reports their rise to approximately 0.6, 0.5, and 0.4 respectively in 2009; copper reaches approximately 0.6. GSCI energy versus non-energy rises from approximately 0.1 in 2004 to above 0.7 in 2009. These are approximate descriptions of rolling plots, not independent estimates at every date: overlapping one-year windows induce substantial dependence across plotted points. The authors say a Forbes–Rigobon volatility adjustment makes no material difference, but do not tabulate the adjusted series or provide its implementation.

To prevent sectors with many contracts from dominating the historical comparison, Figure 3 first forms equally weighted commodity-return indices within each sector, separately for indexed and off-index commodities. It then averages the one-year correlations of the sector pairs with equal weights. A commodity is eligible only after its average daily futures trading value in a calendar year exceeds \$20 million. This threshold is stated in the figure caption and is important for reproducing the historical composition. A real-time implementation would need to clarify whether calendar-year eligibility uses information available at the time.

The indexed and off-index sector correlations are similar and below 0.1 through much of the 1990s and early 2000s. By 2009 they reach approximately 0.5 and 0.2 respectively. Both had reached approximately 0.3 during the 1970s, without the later index/off-index divergence. Thus high commodity correlation is not new in itself; the cross-sectional difference after 2004 is the distinguishing observation.

Growing emerging-market demand is an alternative explanation. GSCI becomes more positively associated with the Morgan Stanley emerging-market equity index and more negatively associated with the US dollar index. Both relations are economically plausible under demand growth, but emerging-market equity returns are not a pure measure of physical commodity demand. They can themselves reflect global financing conditions and common portfolio flows.

The China comparison uses eight matched commodities: heating oil, corn, wheat, soybeans, cotton, sugar, copper, and gold. Available histories begin at different dates, so the composition changes as Chinese contracts appear. Within each country the authors construct sector indices and average cross-sector correlations using matched commodities. The US average rises above 0.5 in the late 2000s, while the Chinese average remains around 0.2 or below rather than showing a comparable sustained rise. The countries' initial averages were near 0.1.

Figure 5 compares price levels normalized to 100 at each pair's starting date, retaining local settlement currencies. Heating oil, copper, and soybean cycles are similar, while the text describes weaker Chinese cycles for wheat, corn, and cotton. The supplied figure has a production error: its last two panels both show and label corn, so the claimed cotton panel cannot be independently checked from that figure. The authors state that renminbi appreciation of approximately 20% over 2005–2009 does not remove the observed boom-and-bust patterns. Trade restrictions, transport costs, local policy, quality differences, asynchronous trading, and changing sample composition still make China an imperfect control. The evidence challenges a simple explanation in which Chinese demand alone generates a uniform global commodity cycle; it does not identify index flows by excluding every fundamental demand channel.

The paper also discusses biofuel links, inflation, and common equity-market conditions. Low core-inflation volatility in the 2000s differs from the 1970s experience, but core CPI excludes food and energy. It cannot by itself rule out common commodity-price news. Similarly, the increase in US equity correlation is much stronger during the crisis, whereas several commodity relationships begin changing earlier. This timing helps distinguish mechanisms without establishing a single exclusive cause.

## Index participation and the flow proxy

The CFTC Commodity Index Traders report provides weekly aggregate positions for twelve agricultural and livestock commodities, released on Friday for the preceding Tuesday. The body starts the sample on 3 January 2006; Table 2 instead labels its start 2 January 2006. Both end on 29 October 2009. This one-day labeling discrepancy should be resolved against the original report dates in replication. Energy and metals are absent, so the position evidence does not directly observe the central oil exposure.

Table 2 reports average index-trader long positions of 28.4% of open interest and shorts of 1.6%. Long shares are particularly large in lean hogs, 42.4%, and Chicago wheat, 41.6%. Average commercial positions are 21.4% long and 49.0% short; noncommercial positions are 16.1% long, 11.0% short, and 23.3% classified as spreading. These percentages describe positions relative to open interest, not each category's capital or net exposure after other markets.

With $NL_{i,t}$ denoting net long index positions and $P_{i,t-1}$ the previous week's front-contract price, equation (1) defines

$$
IF_t=\sum_{i=1}^{12}(NL_{i,t}-NL_{i,t-1})P_{i,t-1}.
$$

Using lagged prices avoids counting a pure mark-to-market gain on an unchanged position as new flow. If $NL$ is measured in contract counts and price in currency per physical unit, contract multipliers must also enter to obtain dollars; the compact source formula does not separately display them. Aggregate positions across maturities are valued with front-month prices, and the calculation assumes changes occur during the preceding week. It is a position-change proxy, not directly observed subscriptions to index products.

Figure 8 cumulates this proxy from zero at the start of 2006. It approaches \$20 billion in 2008, falls to roughly minus \$5 billion around March 2009, and then recovers. The agriculture/livestock index moves similarly. This co-movement is descriptive: demand for exposure can respond to price movements, both can respond to fundamentals, and the construction supplies no instrumental variable. Since direct position coverage begins in 2006, it cannot independently date the assumed 2004 structural change.

## Time-varying macro exposures

Equation (2), Section IV.A, fits the standardized GSCI excess-return series to standardized financial controls. Write $D_t=1_{\{t\geq2004\}}$ and $\tau_t=D_t(t-2004)$, with elapsed time measured in years. In compact notation the specification is

$$
R^n_{GSCI,t}=a_0+a_1D_t+\sum_j(b_{j0}+b_{j1}\tau_t)R^n_{j,t}+\epsilon_t.
$$

Daily controls are emerging-market equities, the S&P 500, the JP Morgan Treasury bond index, and the US dollar index. Monthly versions add inflation and changes in the global shipping index used as an economic-activity proxy. Headline and core CPI are tested separately; the joint regression uses core CPI. Variables are normalized by sample mean and standard deviation. The GSCI sample runs from 4 January 1988 to 29 October 2009; a pre-crisis estimation ends at August 2008. Tables use Newey–West standard errors with five lags.

Normalization does not make every regression coefficient a correlation. A constant univariate slope between two standardized variables is a correlation. A partial slope with multiple controls is a standardized partial exposure, and a linearly time-varying slope estimated using full-sample standard deviations need not equal the local correlation at that date. The source often uses correlation language for these slopes; the distinction matters when transferring coefficients to a covariance model.

The joint daily regression in Table 3(A) reports the following baseline exposure and annual post-2004 trend, with t-statistics in parentheses.

| Factor | Pre-crisis baseline | Pre-crisis trend | Full-sample baseline | Full-sample trend |
|---|---:|---:|---:|---:|
| Emerging-market equities | 0.00 (0.14) | 0.06 (5.00) | 0.01 (0.21) | 0.06 (5.63) |
| S&P 500 | −0.06 (−2.80) | −0.01 (−0.89) | −0.07 (−3.20) | 0.03 (3.15) |
| Treasury bonds | −0.06 (−3.06) | −0.01 (−0.88) | −0.05 (−2.70) | −0.03 (−2.38) |
| US dollar | −0.01 (−0.60) | −0.13 (−6.43) | −0.02 (−0.91) | −0.07 (−4.91) |

Joint daily $R^2$ increases from 3.59% in the pre-crisis sample to 10.82% in the full sample. The emerging-market and dollar trends are present before the acute crisis, while positive equity and more negative bond exposure are more evident when the crisis is included. Univariate emerging-market trends are 0.07 before the crisis and 0.10 in the full sample; the univariate S&P trend changes from approximately zero to 0.09. These differences show how controls change the interpretation.

The monthly joint regression has $R^2$ of 18.11% before the crisis and 25.92% for the full sample. Its full-sample global-activity baseline coefficient is 0.29 with t-statistic 3.27, but the additional trend is only 0.01 with t-statistic 0.30. Core inflation's joint trend is 0.03 with t-statistic 0.63. A blanket statement that inflation trends are insignificant would nevertheless be inaccurate: the univariate full-sample headline-inflation trend is 0.10 with t-statistic 2.97 in Table 3(B). The evidence supports a distinction between particular specifications, not dismissal of every inflation association.

## Indexed versus off-index exposure to oil

Equation (3) pools all twenty-four non-energy commodities. Let $I_i$ equal one for an indexed commodity and zero otherwise, and let $X_{j,t}^n$ denote the four standardized daily financial controls. The fitted model is

$$
R^n_{i,t}=\alpha+(\beta_{0i}+\beta_1\tau_t+\beta_2\tau_t I_i)R^n_{oil,t}
+\sum_j(\gamma_{j0i}+\gamma_{j1}\tau_t+\gamma_{j2}\tau_t I_i)X^n_{j,t}+\epsilon_{i,t}.
$$

Commodity-specific baseline slopes allow different initial economic links. The intercept is common in the printed specification; one should not replace it with commodity fixed intercepts without labeling that change. Off-index oil exposure grows at annual rate $\beta_1$ after 2004; indexed exposure grows at $\beta_1+\beta_2$. The index-specific increment $\beta_2$ is the main statistic. Figure 12 makes clear that the break changes the slope of exposure, rather than imposing a discrete exposure jump.

The panel sample is 2 January 1998–29 October 2009, and the pre-crisis panel ends in August 2008. Some captions repeat the earlier GSCI regression's 1988 start even while stating 1998 elsewhere. Table 4's numerical panel headings and the body identify 1998 as the relevant panel start. This note retains that distinction rather than combining a twenty-one-year GSCI time series with an eleven-year commodity panel.

| Sample and controls | Off-index trend $\beta_1$ | Additional indexed trend $\beta_2$ | $R^2$ |
|---|---:|---:|---:|
| Pre-crisis, no controls | 0.06 (10.48) | 0.02 (3.55) | 2.13% |
| Pre-crisis, controls | 0.04 (8.21) | 0.02 (2.61) | 4.64% |
| Full sample, no controls | 0.05 (15.14) | 0.02 (5.01) | 5.04% |
| Full sample, controls | 0.03 (8.81) | 0.02 (4.26) | 7.98% |

Numbers in parentheses are source t-statistics. On the printed precision, the additional indexed trend is 0.02 standardized slope units per year in every specification. Multiplying by five yields an additional exposure of 0.10 after five years under the imposed trend. This is a calculation from rounded coefficients, not a ten-percentage-point increase in every commodity's literal local correlation. The model also imposes a common incremental trend within each group, which can conceal heterogeneous responses.

With controls, the emerging-market exposure trend is 0.02 for off-index commodities in both samples; its additional indexed trend is approximately zero before the crisis and −0.01 in the full sample, with full-sample t-statistic −1.88. The additional dollar trend is −0.02 before the crisis, t-statistic −2.47, and −0.01 in the full sample, t-statistic −1.41. The particularly consistent incremental association in these tables is with oil.

Table 4(B) repeats the controlled oil comparison within more economically similar groups. The soybean complex is especially informative because soybeans and soybean oil are indexed while soybean meal is not. Its additional indexed trend is 0.06 before the crisis, t-statistic 2.90, and 0.04 in the full sample, t-statistic 3.08. Grain-sector increments are 0.04 with t-statistics 3.21 and 3.08. Softs have 0.02 with t-statistics 1.56 and 2.11; livestock has 0.01 with 0.35 before the crisis and 0.03 with 2.91 afterward; metals have 0.03 with 2.08 and 0.02 with 1.80. Thus positive point estimates are widespread, but neither pre-crisis softs nor full-sample metals clears a conventional two-sided 5% threshold. Describing every non-livestock result as significant would overstate the table.

The economic hypothesis is that investors allocate across indexed contracts together, while other traders have limited capacity to absorb those flows. Oil's heavy index weight can then create shared exposure. However, index inclusion also depends on production and liquidity. Those characteristics can affect the response to global shocks independently of index trading. Similar pre-2004 average correlations do not establish parallel counterfactual trends, and the paper does not use index-entry events or random assignment. Controls can also absorb part of the financialization channel rather than exclusively remove confounders. The authors acknowledge possible excessive controlling; the remaining coefficient cannot be read as a uniquely identified causal treatment effect.

## Lag, spot, and curve checks

Less liquid off-index contracts may respond to common information with a delay. Equation (4) therefore adds one and two lags of oil return, each with a commodity-specific baseline coefficient and the same two post-2004 trends. Denote the lag-one additional indexed trend $\beta_5$ and lag-two increment $\beta_8$. The relevant sum of incremental distributed-lag exposures is

$$
B_{index}=\beta_2+\beta_5+\beta_8.
$$

This sum is a long-run regression response to oil returns in the specified distributed-lag model. It is not automatically a Pearson correlation, particularly with serially correlated regressors and other controls. Table 5 tests whether the sum is positive. Contemporaneous increments remain approximately 0.02. The lag-one increment is approximately zero before the crisis but −0.01 in the full sample, with t-statistics −2.87 without controls and −2.99 with controls. Lag-two increments round to zero.

The reported one-sided test statistics for the sum are 8.07 and 3.43 in the pre-crisis sample without and with controls, and 3.35 and 1.48 in the full sample. Against the source's one-sided 5% critical value of 2.71, the final fully controlled specification does not reject. The table labels this an F-test for a one-sided inequality; replication needs the signed coefficient sum together with the stated one-sided Wald convention, rather than treating an unsigned F statistic as automatically directional. Extra lags and weekly regressions are said to give similar conclusions, but their full estimates are not supplied. The evidence reduces the simple stale-price explanation, while the full-sample controlled lag test is a real qualification to the robustness claim.

For spot returns, Table 6(A) uses sixteen non-energy commodities: corn, soybeans, Chicago and Kansas wheat, soybean oil, Minneapolis wheat, oats, cotton, sugar, live cattle, lean hogs, gold, silver, copper, platinum, and palladium. The controlled panel gives an additional indexed trend of 0.03 in both samples, with t-statistics 2.96 and 4.43. The off-index trend falls from 0.03, t-statistic 2.83, to approximately zero, t-statistic 0.17, when the crisis is included. This suggests that the documented dependence is not confined to the mechanical construction of futures roll returns, subject to the quality and timing of the spot series.

For curve shape the authors define

$$
S_{i,t}=\frac{\log F_{i,t,T_2}-\log F_{i,t,T_1}}{T_2-T_1},
$$

then fit the daily changes using equation (5):

$$
\Delta S_{i,t}=\alpha+(\beta_{0i}+\beta_1\tau_t+\beta_2\tau_t I_i)\Delta S_{oil,t}+\epsilon_{i,t}.
$$

Unlike the return panel, this printed equation does not display standardized variables or the financial-control block. The maturity-time unit and all preprocessing details for slope changes are not fully specified. Table 6(B) reports off-index trends 0.01 and 0.00 with t-statistics 1.30 and 0.08, and incremental indexed trends 0.00 and −0.01 with t-statistics −0.65 and −0.50. There is no significant increase in slope-change association. That is narrower than proving that index investment had no effect on curve levels, carry returns, or curve volatility. Spreading trading pressure across maturities through arbitrage is a plausible interpretation, not separately estimated behavior.

## Squared-return evidence on volatility transmission

Figure 13 shows one-year rolling annualized daily volatility for oil, the GSCI non-energy excess-return index, and world equities. Oil rises from roughly 30% to near 60% during 2008, but had reached comparably high levels around the Gulf War. Non-energy volatility had stayed near 10% for much of the 1990s and early 2000s and rises toward 27% in the crisis. The unusual feature is the broad non-energy increase, not the existence of a large oil-volatility episode.

For the formal test in Section V, each commodity's daily return is centered using its whole-sample mean and divided by its own pre-2004 standard deviation. Let $Z_{i,t}$ denote this normalized return, and let $1_{y,t}$ mark calendar year $y$. Equation (6) is

$$
Z_{i,t}^2=a_{0i}+\sum_{y=2004}^{2009}b_y1_{y,t}+\sum_{y=2004}^{2009}c_yI_i1_{y,t}+\epsilon_{i,t}.
$$

The commodity-specific intercept absorbs the baseline normalized second moment. The $b_y$ coefficients are off-index year effects; $c_y$ is the additional indexed effect. The Table 7 caption has a small notation slip, printing $c_{05}$ beside the 2004 interaction, while the body and results row use $c_{04}$. The equation above uses the intended year matching.

These are effects on squared normalized returns, hence in units of the pre-2004 variance scale, not changes in annualized standard deviation or percentage-point volatility. Because centering uses one whole-sample mean, the annual conditional second moment also includes any annual mean shift relative to that mean. With small daily drifts this distinction may be modest, but it is not an exact variance identity.

The authors repeat the squared-return regression after filtering financial controls and then after also filtering oil. For each commodity, equation (7) regresses returns on an intercept, a post-2004 intercept shift, and factor exposures of the form $b_0+b_1\tau_t$. Factors are emerging-market equities, the S&P 500, Treasury bonds, the dollar, core CPI inflation, and the change in the shipping index; the last specification adds oil. Monthly inflation and shipping observations are held constant within each month. This is an in-sample explanatory projection with contemporaneous variables, not a real-time forecast filter. The exact treatment of residual scaling should be checked against code, which is not supplied, before reproducing the table.

Table 7's additional indexed second-moment effects are:

| Year | Raw returns | After financial/macro controls | After controls and oil |
|---|---:|---:|---:|
| 2004 | 0.34 (3.55) | 0.26 (2.84) | 0.25 (2.74) |
| 2005 | 0.09 (1.26) | 0.07 (1.07) | 0.06 (0.93) |
| 2006 | 0.54 (4.63) | 0.45 (4.44) | 0.38 (4.06) |
| 2007 | 0.25 (3.35) | 0.17 (2.35) | 0.14 (1.93) |
| 2008 | 0.68 (3.42) | 0.43 (2.55) | 0.24 (1.59) |
| 2009 | 0.37 (2.88) | 0.22 (1.90) | 0.14 (1.29) |

The raw off-index baseline increases are 1.45 in 2008, t-statistic 10.80, and 0.78 in 2009, t-statistic 8.59. Their earlier effects are 0.25, −0.09, −0.01, and −0.07 for 2004–2007. The crisis therefore affects both groups; indexed commodities experience an additional increase relative to their normalized baselines. Removing oil reduces the 2008 incremental effect from 0.43 to 0.24 and makes it statistically weak under the reported standard errors. This is consistent with shared oil exposure, but projection residuals do not identify a causal fraction of variance transmitted from oil. Joint shocks or an omitted common factor can produce the same attenuation.

The three regressions have $R^2$ of 4.5%, 3.2%, and 2.6%. Low $R^2$ is unsurprising for daily squared returns, but emphasizes the large unexplained component. The standard errors again use five Newey–West lags. A pooled commodity panel also has contemporaneous cross-commodity dependence. The paper does not provide enough covariance-estimator detail to certify how date clustering is handled. A modern replication should report its handling explicitly and assess date-clustered or block-bootstrap inference as additional robustness, rather than assuming the published t-statistics already cover every form of panel dependence.

## What can be reconstructed, and what remains open

A faithful recreation starts with individual futures contracts and the Table 1 eligible-delivery rules, preserves the study's index/off-index classification, and reconstructs the source's roll convention. It next builds one-year rolling descriptive measures, applies the sector-weighting and liquidity rules, and estimates the two distinct samples: the longer GSCI time series and the 1998–2009 individual-commodity panel. The 2004 time trend must be measured in years, with commodity-specific baseline slopes and the printed common versus commodity-specific intercept choices retained. Newey–West lag length is five in the reported tables. The pre-crisis and full-sample results should be stored separately, since several conclusions change when the financial crisis enters.

The paper provides no random seed, simulation calibration, training/validation split, or portfolio optimization objective because its empirical design is explanatory rather than algorithmic prediction. It does not report transaction costs, margin requirements, financing spreads, turnover, or net strategy returns. Using the findings to reduce commodity allocation would require an additional investment objective, forward-looking covariance estimates, and uncertainty about whether the historical regime persists. Nothing in these regressions establishes a profitable timing rule from observable index flows.

Unresolved replication inputs include the exact roll-day return chain, eligible-contract selection around delivery, price and calendar cleaning, historical membership changes if any, liquidity-threshold timing, residual normalization in Table 7, and panel covariance implementation. The overlapping rolling graphs and numerous related specifications are not independent replications, and the supplied tables do not adjust inference for the full set of comparisons. The source's positive association between index membership and rising common exposure is substantial; its causal attribution is necessarily more conditional than the word “financialization” alone suggests.

## Source map and bibliography

Tang, Ke, and Wei Xiong. 2010. *Index Investment and Financialization of Commodities*. NBER Working Paper 16385, September. The supplied source identifies this working-paper version; all numerical results above refer to it.

The data and return construction are in Sections I–II, especially printed pp. 7–10 and Table 1 on p. 41. Mechanisms, Chinese comparisons, and the position-flow proxy are on pp. 10–19; equation (1) is on p. 13. Equation (2) and Table 3 supply the time-series design and estimates. Equation (3), Figure 12, and Table 4 define the indexed/off-index slope comparison. Equation (4) and Table 5 address lagged oil effects. Equation (5) and Table 6 distinguish spot returns from curve slopes. Equations (6)–(7), Figure 13, and Table 7 contain the squared-return analysis. Figures 1–13 and Tables 1–7 occupy printed pp. 33–50 and were read together with their captions and the main text. The figure duplication, caption date conflicts, variance-unit distinction, and limits of causal interpretation above are observations from this source inspection, not corrections claimed to come from a published erratum.
