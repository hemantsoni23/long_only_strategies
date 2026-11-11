# When Sell-Side Analysts Meet High-Volatility Stocks: An Alternative Explanation for the Low-Volatility Puzzle

Jason C. Hsu, Hideaki Kudoh, and Toru Yamada. Undated manuscript in the supplied 26-page PDF; author affiliations are Research Affiliates/UCLA Anderson and Nomura Asset Management. [Source PDF](../../Finance/When%20Sell-Side%20Analysts%20Meet%20High%20Volatility%20Stocks.pdf). All pages, including references and the appended empirical tables, were read. The forecast calendar, volatility-adjustment equation, analyst-behavior argument, and all main results tables were checked visually. A publication year or journal version is not identified on this supplied manuscript and is not inferred from its references.

## Why this matters

This paper separates two pieces of information in analyst earnings forecasts. Forecasts can be systematically optimistic while still helping identify relatively cheap stocks. The authors find that high-volatility stocks receive more optimistic earnings-growth forecasts, yet stocks with high forward earnings-to-price ratios subsequently earn higher returns. They propose that analysts selectively inflate forecasts where the bias is harder to detect or where a profitable recommendation is likely to protect their reputation.

The empirical contribution is a set of joint patterns in global developed and emerging-market equities: low-volatility portfolios have higher Sharpe ratios; volatility is associated with larger ex post analyst optimism; forward E/P sorts contain return information; and the low-volatility Sharpe-ratio advantage is stronger among low-forward-E/P stocks. These patterns are relevant to combining defensive equity selection with valuation signals and to interpreting consensus forecasts as both information and a potentially biased input.

The proposed analyst mechanism is a narrative model with qualitative incentives. The paper explicitly does not derive a formal repeated-game equilibrium or test its unique predictions against competing explanations. It also does not establish that analyst optimism causes the entire volatility premium. Forecast bias is observed only after actual earnings arrive, and forward E/P itself mechanically contains the forecast whose bias is being studied. Those distinctions are central to using the results responsibly.

## Universe, data, and coverage

The universe is the union of MSCI and FTSE developed- and emerging-market index memberships. Accounting data are from Worldscope, total returns from IDC Exshares, and analyst consensus and actual EPS from I/B/E/S. The return sample is January 1987–December 2011 for developed markets and December 1994–December 2011 for emerging markets. Forecast-bias analyses end in December 2009 because they require subsequent realized earnings for the relevant fiscal periods.

The unrestricted average universe contains 3,308 developed-market stocks and 910 emerging-market stocks. Requiring consensus EPS reduces those averages to 2,846 and 537, respectively. The developed-market covered sample averages 1,138 stocks in North America, 898 in Europe, 596 in Japan, and 214 in Asia Pacific excluding Japan. The analysis also requires reported EPS, so the universe is an analyst-covered subset of listed equities. Observations with negative book value per share are discarded.

The source says all return statistics use excess local returns: stock return less the local three-month interest rate. A global portfolio built by aggregating such local-currency excess returns is not automatically the realized return of an unhedged dollar investor. The paper does not provide a complete currency-conversion, hedging, or financing-account convention. Its emerging-market discussion refers to the unusual currency environment of 1994–1998, but the displayed results should still be described using the source's local-return convention.

The authors report that eliminating stocks without consensus forecasts does not materially alter their findings and that winsorizing outliers has little effect. Neither check is tabulated, and the winsorization thresholds are not specified. These are author-reported robustness claims, not a complete recipe for reproducing the underlying tests.

Important security-level details remain undisclosed: point-in-time membership handling, dead-security inclusion, share-class selection, delisting returns, minimum history for the five-year volatility signal, stale forecasts, and historical accounting release dates. The paper supplies enough to understand the hypothesis and broad construction but not enough to recreate the exact portfolio return series without additional choices.

## Defining forward earnings and optimism

I/B/E/S supplies EPS for the previously completed fiscal year, forecasts for the current fiscal year, and forecasts for the following year. The authors label them FY0, FY1, and FY2. Their Table 1 illustrates a September fiscal-year-end company: at October 2000, FY0 is September 2000, FY1 September 2001, and FY2 September 2002. The prose's informal fiscal-year labels are less precise than the calendar dates in the table; the table gives the safe alignment.

The forward twelve-month consensus EPS is a time-weighted combination of FY1 and FY2 forecasts. The realized twelve-month EPS used later to assess bias uses the same time weights applied to the eventual actual fiscal-year earnings. A generic reconstruction is

$$
\widehat E_{i,t}^{12}=w_{i,t}\widehat E_{i,t}^{FY1}
+(1-w_{i,t})\widehat E_{i,t}^{FY2},
$$

$$
E_{i,t}^{12}=w_{i,t}E_i^{FY1}+(1-w_{i,t})E_i^{FY2}.
$$

Here $w_{i,t}$ is the fraction of the forward twelve-month interval belonging to FY1. The source describes time weighting but does not provide an exact day-count, month-end, or fiscal-rollover formula. Using months remaining to fiscal year-end divided by twelve is a reasonable implementation interpretation, not a verified description of original code.

EPS alone is not comparable across share prices or share counts. The paper scales earnings changes by book value per share, $BPS$, and calls the earnings-level ratio an ROE measure. In its notation the subscript $t-1$ on book value refers to the prior fiscal year, not the preceding month. The forecast and realized earnings-growth variables are

$$
\widehat g_{i,t}=\frac{\widehat E_{i,t}^{12}-E_{i,t}^{past12}}{BPS_{i,t}},
\qquad
 g_{i,t}^{real}=\frac{E_{i,t}^{12}-E_{i,t}^{past12}}{BPS_{i,t}}.
$$

These are changes in earnings scaled by book equity. They are not conventional percentage growth rates relative to previous earnings. The distinction avoids pathological growth ratios when earnings change sign, but it also changes the meaning of a displayed “6% growth forecast.” It means six percentage points of the book-equity-scaled earnings measure, not a 6% increase from last year's EPS.

Define positive optimism as

$$
B_{i,t}=\widehat g_{i,t}-g_{i,t}^{real}
=\frac{\widehat E_{i,t}^{12}-E_{i,t}^{12}}{BPS_{i,t}}.
$$

This convention matches the positive “Growth Forecast Bias” entries in Table 3 and the explicit definition on p. 12. Page 9 instead defines forecast error as realized minus forecast earnings, the opposite sign. The note distinguishes those two conventions rather than carrying the source's sign ambiguity into the formulas.

Forward earnings yield is

$$
FE/P_{i,t}=\frac{\widehat E_{i,t}^{12}}{P_{i,t}}.
$$

The forecast is observable at formation, subject to actual database availability; the realized bias $B_{i,t}$ is not. A deployable strategy could use volatility or a historically trained bias predictor, but could not sort on the future forecast error in Table 3. The paper does not estimate a separate out-of-sample model that predicts $B$ or demonstrate the performance of a forecast explicitly debiased using such a model.

## Volatility adjustment and portfolio formation

At each month-end, total stock-return volatility is measured from the previous sixty months. To reduce country, sector, size, and value differences, the source estimates the cross-sectional regression in equation (1):

$$
\log(Vol_i)=\beta_1Size_i+\beta_2BP_i
+\sum_j\gamma_jSD_{ij}+\sum_k\delta_kCtry_{ik}+\varepsilon_i.
$$

The dependent variable is *log volatility*, confirmed visually; extraction can obscure the logarithm. $Size_i$ is described as preceding-month market capitalization, $BP_i$ as book-to-price, $SD$ as the ten GICS sector indicators, and $Ctry$ as country indicators. The source does not state that $Size$ is itself logged, so replacing it with log capitalization is an unverified specification change. The intercept and redundant dummy treatment must also be made explicit in code.

Stocks are ranked on residual $\varepsilon_i$. This is a characteristic-adjusted total-volatility signal. It is not the standard deviation of residual daily returns from a time-series factor model, and should not be renamed idiosyncratic volatility in the Ang et al. sense. An asset can have a high time-series residual volatility but a modest cross-sectional residual after controlling for its country or sector's typical volatility.

The portfolios are deciles for developed markets and quintiles for emerging markets. Monthly sorting is described, but exact constituent weighting, execution timing, and the holding-period aggregation convention are insufficiently specified. The prose refers to annualized buy-and-hold returns, while the result tables label “Arithmetic Mean % p.a.” The tables support annualized arithmetic excess-return comparisons; they do not establish a geometric CAGR.

Regressing out characteristics before ranking does not impose exact portfolio neutrality. OLS residuals are orthogonal to included regressors in the regression sample and weighting convention; a nonlinear decile sort need not have identical country weights, market capitalization, or B/P across deciles. The source says these characteristics are similar, not identical. Table 2's developed-market B/P varies from 47.0 in the lowest-volatility decile to 36.7 in the highest, and the emerging second quintile has B/P 95.6 versus 63.0 in the first. Those visible differences should temper claims of complete neutrality.

## The low-volatility return evidence

Table 2, through December 2011, gives the following annualized results:

| Market and portfolio | Excess return | Portfolio volatility | Average constituent volatility | Sharpe ratio | Market beta |
|---|---:|---:|---:|---:|---:|
| Developed, lowest-volatility decile | 6.6% | 11.7% | 21.8% | 0.56 | 0.71 |
| Developed, highest-volatility decile | 4.2% | 24.2% | 65.3% | 0.17 | 1.44 |
| Emerging, lowest-volatility quintile | 7.4% | 16.3% | 34.1% | 0.45 | 0.72 |
| Emerging, highest-volatility quintile | 9.0% | 25.5% | 69.4% | 0.35 | 1.11 |

Developed-market low volatility earns 2.4 percentage points more per year at less than half the portfolio volatility of the high-volatility decile. Returns are not monotonic across every decile, but the high-risk extreme performs poorly relative to its risk. Emerging-market low volatility does *not* have the higher raw excess return: 7.4% is below 9.0%. Its Sharpe ratio is higher because the volatility reduction is proportionately larger. The middle emerging quintile has the largest reported return, 12.7%, and Sharpe ratio, 0.53.

Thus the global statement supported by these tables is stronger for risk-adjusted performance than for an inverse raw-return slope. “Low volatility outperforms everywhere” would blur two different comparisons. The source reports stronger emerging-market evidence after excluding 1994–1998, but does not tabulate the return spread or its uncertainty for that subperiod.

The table provides no standard errors for these return differences, no test comparing Sharpe ratios, and no long–short return volatility. One cannot calculate a spread's Sharpe ratio from the difference between the two individual Sharpe ratios because the covariance of the legs is missing. Likewise, comparing 0.56 with 0.17 describes the point estimates but does not provide a significance level for their difference.

## Volatility and ex post forecast bias

Table 3 ends in December 2009 to allow future earnings realization. In developed markets, the lowest-volatility decile has forecasted book-scaled earnings growth of 2.53%, actual growth of 0.42%, and optimism of 2.11%. The highest-volatility decile has forecast growth of 8.03%, actual growth of 1.17%, and optimism of 6.86%. The high-minus-low optimism gap is therefore 4.75 percentage points on the paper's book-equity scale.

The forecast spread is much larger than the realized-growth spread: 5.50 points versus 0.75 points. Average ROE variability rises from 4.4 to 32.7, while portfolio return volatility rises from 11.9% to 24.0%. The table establishes that the volatile group has more variable earnings and a larger average forecast error; it does not determine whether analysts knowingly created the error or were themselves overoptimistic.

Emerging-market results are directionally similar but weaker and less monotonic. Forecasted growth is 4.50% in the lowest-volatility quintile and 6.50% in the highest, actual growth 1.27% and 1.73%, and optimism 3.23% and 4.78%. The optimism gap is 1.55 points. Average ROE variability is 6.3 versus 15.3. The second quintile's bias, 3.03%, is below that of the first, so this is a broad cross-sectional pattern rather than strict monotonicity.

Trailing and forward earnings yields also vary across volatility groups. For developed markets, trailing E/P declines from 7.4% to 2.0%, and forward E/P from 7.7% to 5.9%. For emerging markets, forward E/P is 10.6% in the lowest-volatility group and 11.8% in the highest. These differences motivate the joint volatility/forward-E/P sorts and caution against assuming that volatility's return association has been isolated from every valuation dimension.

No bias-regression coefficients, sampling errors, or formal mediation estimate are reported in Table 3. The source's claim is therefore a documented descriptive relation plus an interpretation. Overlapping forward twelve-month earnings and common macroeconomic shocks can create dependence across monthly observations; a statistical test of bias differences would need to account for that dependence and for repeated firms.

## The analyst-behavior argument

The authors imagine an analyst with private estimates of expected earnings growth $\widehat g_{i,t}$ and its uncertainty $\widehat\sigma_{i,t}$. The analyst publishes $G_{i,t}$ instead. Three qualitative incentives affect the choice: optimism helps investment-banking or brokerage relationships; detectable inflation threatens credibility; and distorting an otherwise useful valuation recommendation can harm clients and the analyst's reputation.

The proposed behavior is

$$
G_{i,t}=\widehat g_{i,t}+k\widehat\sigma_{i,t},\qquad k>0.
$$

The first implication is straightforward: if earnings uncertainty rises with stock-return volatility, a fixed standardized inflation $k$ produces larger absolute optimism for volatile stocks. If investors insufficiently adjust for the bias, those stocks can become overvalued and subsequently underperform. The second idea is that an analyst can retain useful relative valuation information despite upward-biased levels, particularly when recommendations are expressed through forward E/P.

The source describes utility as increasing in $G-\widehat g$, decreasing in $(G-\widehat g)/\widehat\sigma$, and decreasing in the distortion of the forecast-implied earnings yield. It does not specify a functional form, feasible action set, investor learning rule, analyst discount factor, equilibrium beliefs, or market-clearing price equation. There is no derived first-order condition proving that $k$ is constant, no existence proof, and no estimated $k$. A half-standard-deviation example earlier in the paper is illustrative, not a calibrated parameter.

The detection argument also needs a statistical distinction. The manuscript discusses the average forecast error divided by realized earnings variability. That is a standardized mean error, not by itself a conventional $t$-statistic. Under independent errors, inference for a sample mean uses a standard error proportional to $1/\sqrt T$; with overlapping or dependent forecast horizons, a long-run variance estimator is needed. This observation does not invalidate the intuition that noisier earnings make individual errors less informative, but it prevents treating the displayed heuristic as a completed detection test.

Several explanations remain observationally compatible with the reported pattern: analysts may extrapolate rather than strategically conceal optimism; volatile firms may issue guidance differently; growth opportunities may affect both errors and volatility; or forecast coverage and survival selection may matter. The authors acknowledge that they do not develop discriminating tests. The note therefore treats the strategic-inflation mechanism as a hypothesis organizing the facts.

## Forward E/P contains return information

Table 4 sorts on forward E/P, using the forecast-bias sample ending in December 2009. Developed-market low and high deciles have annualized arithmetic excess returns of 4.87% and 10.82%, a difference of 5.95 points. Their portfolio volatilities are 25.71% and 22.49%, with Sharpe ratios 0.19 and 0.48. Intermediate deciles are not perfectly ordered: the second and third have returns near 2%, below the first.

The monthly Fama–French three-factor alphas are −0.15%, $t=-0.69$, for the lowest decile and 0.25%, $t=1.39$, for the highest. The seventh, eighth, and ninth deciles have alphas 0.17%, 0.21%, and 0.28%, with $t=2.18,2.20,2.58$. Thus several high-yield groups have significant positive alphas, but the extreme high-E/P decile itself does not at a conventional 5% two-sided level. The top decile's market, size, and value loadings are 1.25, 0.66, and 0.57.

Emerging-market low and high quintiles earn 9.06% and 18.63% per year, a difference of 9.57 points, with Sharpe ratios 0.35 and 0.73. The highest quintile's monthly alpha is 0.57%, $t=2.56$, versus 0.23%, $t=0.70$, for the lowest. The second quintile earns only 0.94% annually and has alpha −0.34%, $t=-2.78$. These nonmonotonic results make the high-end premium more precise than a claim that every step up in forward E/P improves returns.

The factor regressions are reported with market, SMB, and HML exposures, but the supplied manuscript does not fully specify the regional/global factor construction or standard-error method. It also does not report the significance of the high-minus-low alpha difference. Subtracting point estimates is valid arithmetic; subtracting two $t$-statistics or assuming independent portfolio errors is not a valid spread test.

Bias rises with forward E/P too. Developed-market optimism is 1.59% in the low decile and 7.02% in the high; emerging-market optimism is 1.28% and 6.23%. The authors interpret this as analysts being more willing to inflate forecasts for stocks whose eventual returns are likely to satisfy clients. But sorting on forecast E/P mechanically selects the forecast numerator, which also enters forecast-minus-actual bias. A positive association can arise partly from that shared component. Establishing strategic intent requires more than the unconditional relation.

Forward E/P is also a valuation characteristic. Positive alpha against a three-factor benchmark does not by itself prove private analyst skill, because omitted profitability, quality, earnings persistence, or other information could explain the residual. The evidence supports usefulness of the combined public forecast/price ratio in this historical design; it does not uniquely allocate that usefulness to analyst private information rather than price or other fundamental features.

## Double sorts and what the interaction shows

The authors conduct unconditional double sorts, forming five-by-five developed-market portfolios and three-by-three emerging-market portfolios on volatility and forward E/P. Unconditional means that the two classifications are formed independently and their intersections held; this differs from ranking volatility separately inside each E/P group. The number of stocks in cells consequently varies. Table 5 shows values from roughly 76 to 241 in the developed cells and 81 to 125 in the emerging cells, labeled “Number of Observations” without a fully explicit time-aggregation definition.

The four developed-market corner portfolios illustrate the interaction:

| Volatility / forward E/P | Annual excess return | Annual volatility | Sharpe ratio | Forecast bias |
|---|---:|---:|---:|---:|
| Low / low | 5.2% | 12.4% | 0.42 | 0.7% |
| High / low | 3.6% | 31.4% | 0.11 | 1.9% |
| Low / high | 8.3% | 13.1% | 0.63 | 4.2% |
| High / high | 13.0% | 29.1% | 0.45 | 8.6% |

The low-volatility advantage is a Sharpe-ratio advantage in both E/P groups, but high-volatility/high-E/P stocks have higher raw returns than low-volatility/high-E/P stocks. The proportional Sharpe decline from low to high volatility is about 74% in the low-E/P group and 29% in the high-E/P group. These percentages are ratios of rounded point estimates, not statistical interaction coefficients.

Emerging-market low-E/P corners have returns 5.8% and 9.0%, volatilities 15.0% and 34.6%, and Sharpe ratios 0.39 and 0.26. High-E/P corners have returns 10.2% and 16.7%, volatilities 16.8% and 30.6%, and ratios 0.61 and 0.55. The Sharpe decline is approximately one-third in the low-E/P group and roughly one-tenth in the high-E/P group. The high-volatility/low-E/P emerging cell actually has less reported forecast bias, 0.7%, than the low-volatility/low-E/P cell, 1.0%; the analyst-bias gradient is not universal within every conditional slice.

Table 6's developed low-volatility/high-E/P corner has alpha 0.31 with $t=2.75$, while high-volatility/high-E/P has 0.32 with $t=1.20$. The low-volatility/low-E/P corner has 0.10, $t=0.85$, and high-volatility/low-E/P −0.20, $t=-0.70$. These entries follow the monthly-percent convention of the preceding factor tables, though Table 6 omits a repeated unit label. The table does not show a strictly monotonic alpha surface. In emerging markets, corresponding corner alphas are 0.33, 0.27, 0.20, and 0.03, with $t=1.93,1.01,1.23,0.05$.

The joint evidence supports combining volatility and valuation when evaluating defensive stocks. It does not justify replacing return targets with a ranking of individual portfolio Sharpe ratios without accounting for covariance, leverage, and constraints. Nor does it show that the proposed analyst channel is sufficient to generate every observed interaction.

## Reimplementation and unresolved inputs

A faithful reconstruction would first build historical membership and accounting/forecast snapshots, align FY1/FY2 forecasts with fiscal dates, and calculate the available sixty-month volatility signal at each formation date. It would then fit the cross-sectional log-volatility adjustment, form the stated portfolio sorts, and calculate monthly local excess returns before applying the paper's annualization and factor regressions. Future actual EPS would enter a separate evaluation dataset for bias, with the return signal dataset kept free of those outcomes.

The exact portfolio weighting, fiscal interpolation convention, factor definitions, common-currency treatment, missing-data filters, and standard-error method remain necessary inputs. The manuscript does not disclose a transaction-cost or stock-borrow model, and it does not report turnover, capacity, implementation shortfall, or performance after management fees. It also lacks a formal chronological training/validation split and a frozen out-of-sample bias-correction rule. Its empirical comparisons are historical portfolio sorts rather than a validated forecasting system.

The source's most useful distinction is between forecast accuracy and investment usefulness. An optimistic forecast can still carry relative information, and a high forecast earnings yield need not be equivalent to a low-bias forecast. The supplied evidence documents those coexistences. Strategic analyst inflation and investor underadjustment are plausible explanations, but they remain hypotheses because the research does not observe private forecasts, estimate the strategic objective, or identify an exogenous change in analyst incentives.

## Source map and bibliography

Hsu, Jason C., Hideaki Kudoh, and Toru Yamada, “When Sell-Side Analysts Meet High-Volatility Stocks: An Alternative Explanation for the Low-Volatility Puzzle,” supplied undated manuscript. Motivation and related literature: pp. 1–8. Forecast calendar and standardization: Table 1, pp. 8–10. Volatility residualization: equation (1), p. 11. Bias definition and analyst incentives: pp. 12–14. Forward E/P and joint sorts: pp. 14–17. References: pp. 18–21. Numerical results: Tables 2–6, pp. 22–26. The sign reconciliation, shared-numerator concern, and statistical qualifications in this note are analytical distinctions made from the supplied definitions and tables, not additional empirical tests.
