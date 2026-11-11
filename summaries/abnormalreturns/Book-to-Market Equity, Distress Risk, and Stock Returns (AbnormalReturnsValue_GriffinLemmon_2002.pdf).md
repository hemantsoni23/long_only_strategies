# Book-to-Market Equity, Distress Risk, and Stock Returns

**John M. Griffin and Michael L. Lemmon (2002).** *Journal of Finance* 57(5), October, 2317–2336. Source: [AbnormalReturnsValue_GriffinLemmon_2002.pdf](../../Finance/AbnormalReturnsValue_GriffinLemmon_2002.pdf). The local file contains the complete 20-page published article, including references; PDF page 1 is printed page 2317. An earlier version was entitled *Does Book-to-Market Equity Proxy for Distress Risk or Mispricing?* This note follows the published version and its numerical tables. No separate appendix is included.

## Why this matters

The central finding is an interaction: the value premium is exceptionally large among firms with high accounting-based distress scores, but it is driven mainly by very low returns on **expensive distressed firms**, rather than unusually high returns on cheap distressed firms. That distinction reconciles two apparently contradictory observations. High book-to-market firms often have weak fundamentals and high average returns, yet firms with high estimated bankruptcy risk can have low average returns. Distress and book-to-market are different classifications, and collapsing either dimension obscures where the anomaly occurs.

The closest empirical tension is between Fama–French and Chen–Zhang evidence associating value stocks with weak fundamentals and Dichev's finding of low returns among firms predicted to be distressed. Griffin and Lemmon cross-classify the two signals, study conventional factor exposures and subsequent fundamentals, and then examine announcement returns and analyst coverage. Their contribution is the conditional decomposition and the supporting evidence on expectations, rather than a newly estimated bankruptcy model or a structural equilibrium solution.

The proposed behavioral mechanism is more specific than simple extrapolation of strong recent earnings. Some high-distress, low-book-to-market firms have poor current profitability while operating in growth-oriented industries. Investors may price their future opportunities as though they will catch up with successful peers, understating the importance of weak current fundamentals. Their subsequent disappointing performance then produces low returns. High capital expenditure, R&D, past stock-price gains, and expensive sales multiples are consistent with this interpretation, but the paper does not directly observe beliefs or estimate a causal response to an exogenous information shock.

The risk comparison is informative but should be stated carefully. An accounting prediction of bankruptcy is not itself a measure of systematic risk. High default probability can coexist with either high or low covariance with marginal utility. The paper shows that the results are hard to reconcile with the simple claim that high book-to-market returns compensate investors for the kind of distress captured by O-score, and with the three-factor model used as a benchmark. It does not establish that every possible distress-related risk channel is absent.

## Universe, formation dates, and O-score

The main universe consists of **nonfinancial NYSE, AMEX, and NASDAQ stocks**, with CRSP monthly returns and nonnegative Compustat book equity, from **July 1965 to June 1996**. Each June the authors rank on the previous December book-to-market equity ratio, June market capitalization, and O-score calculated from the previous December's accounting values. The text's December wording should be preserved in a replication specification: the paper does not give a full treatment of non-December fiscal-year firms or accounting release dates. The calendar lag aims to place accounting information before the return period, but the supplied article is not a point-in-time data dictionary.

O-score is an existing composite accounting model, not a score re-estimated on this return sample. Let $A$ be total assets, $L$ total liabilities, $WC$ working capital, $CL$ current liabilities, $CA$ current assets, $NI$ net income, and $FFO$ funds from operations. Define $I_{L>A}$ as the indicator that liabilities exceed assets and $I_{2loss}$ as the indicator of net losses in both of the last two years. Footnote 5, printed page 2320/PDF page 4, gives

$$
\begin{aligned}
O_t={}&-1.32-0.407\log A_t+6.03\frac{L_t}{A_t}
-1.43\frac{WC_t}{A_t}+0.076\frac{CL_t}{CA_t}\\
&-1.72I_{L>A,t}-2.37\frac{NI_t}{A_t}
-1.83\frac{FFO_t}{L_t}+0.285I_{2loss,t}\\
&-0.521\frac{NI_t-NI_{t-1}}{|NI_t|+|NI_{t-1}|}.
\end{aligned}
$$

The article labels this expression O-score and reports “O-score probability” in Table I. In the logit interpretation the probability is $p_t=\exp(O_t)/(1+\exp(O_t))$. The transformation is monotone, so ranking by the linear score or by this probability gives identical quintiles. It matters when reproducing probability medians such as 19.4%. The displayed formula uses log total assets without specifying an inflation adjustment or units; importing a different Ohlson implementation could shift probabilities even if some cross-sectional rankings remain unchanged. Zero denominators in working-capital or income-change ratios and missing FFO are also not addressed explicitly in the article.

The main portfolio design independently crosses three book-to-market groups, five O-score groups, and two size groups, producing 30 cells. Book-to-market uses 30th and 70th percentile breakpoints. The main tables state that breakpoints are computed using **all securities**, rather than NYSE-only breakpoints. NYSE size quintiles appear in separate robustness and analyst-coverage tests. Confusing these two conventions would substantially change the sample's small/large assignments.

Most reported “size-adjusted” statistics are a simple average of the small- and large-group statistics. They are not residuals from a size regression and not returns relative to a size benchmark. For returns, calculate the annual value-weighted buy-and-hold return in each size cell and average the two cell series. For characteristics, average the relevant small- and large-cell means or medians as stated. The operation is not generally equal to a pooled portfolio's statistic. Return significance is assessed from monthly return series, even when the reported economic magnitudes are annual buy-and-hold returns.

The authors adjust delisting bias using Shumway's method. Later discussion identifies performance-related CRSP delisting codes 500 and 520–584 and notes their average loss of about 30%. The article does not provide a complete implementation rule for each observed versus missing delisting return, month of application, or proceeds reinvestment. Those details affect precisely the high-distress portfolios of greatest interest and should be reconstructed explicitly before testing the headline result.

## What the cross-classification reveals

The overall Spearman correlation between O-score and book-to-market is only **0.052**. The highest O-score quintile includes more low-book-to-market firms than high-book-to-market firms in the reported average cell counts: 104 versus 76. This alone shows why “value” and “distress” cannot be used interchangeably.

Table I, printed page 2321/PDF page 5, provides a revealing four-corner comparison. Size-adjusted characteristics are reported as in the source; returns are prior equal-weighted buy-and-hold percentages, and market capitalizations are in millions of dollars.

| Characteristic | Low distress, low B/M | Low distress, high B/M | High distress, low B/M | High distress, high B/M |
|---|---:|---:|---:|---:|
| O-score probability | 0.001 | 0.001 | 0.194 | 0.087 |
| Book-to-market | 0.341 | 1.424 | 0.267 | 1.651 |
| Prior 12-month return | 24.7% | 8.9% | 36.1% | 0.8% |
| Prior 36-month return | 121.0% | 22.5% | 107.7% | −12.1% |
| Retained-earnings growth | 0.291 | 0.088 | −0.110 | −0.245 |
| Market capitalization | 202 | 103 | 51 | 51 |
| Book liabilities/market equity | 0.097 | 0.457 | 0.596 | 3.431 |
| Return on assets | 0.130 | 0.061 | −0.078 | −0.038 |

High-distress growth firms are therefore not merely ordinary fallen value companies classified as growth by a book-equity write-down. They have the highest prior one-year stock return within the low-book-to-market category, a substantial prior three-year gain, and retained-earnings declines smaller than those of distressed value firms. These comparisons do not prove that book-value erosion is irrelevant, but they reject it as a complete account of their low ratios.

The same firms have low profitability and more leverage than low-distress growth firms, so their low subsequent returns cannot be casually described as those of exceptionally safe businesses. The comparison with distressed value firms is different: their market leverage is much lower because market equity remains expensive. This is a reminder that market-based leverage contains the price whose interpretation is being tested. O-score aggregates accounting dimensions that a single market-leverage sort does not capture.

## Return magnitudes and conventional risk adjustment

Table II, printed page 2323/PDF page 7, reports the following size-adjusted annual value-weighted buy-and-hold percentages. P-values for high-minus-low book-to-market portfolios are calculated from monthly time series; displayed 0.000 denotes rounding, not an exact zero probability.

| Distress quintile | Low B/M | Middle B/M | High B/M | High minus low | p-value |
|---|---:|---:|---:|---:|---:|
| Lowest | 13.28 | 15.76 | 17.15 | 3.87 | 0.068 |
| 2 | 15.58 | 17.33 | 18.83 | 3.25 | 0.022 |
| 3 | 13.05 | 17.38 | 18.54 | 5.49 | 0.000 |
| 4 | 11.61 | 16.80 | 22.23 | 10.62 | 0.000 |
| Highest | 6.36 | 15.98 | 20.80 | 14.44 | 0.000 |

Within low-book-to-market stocks, moving from the lowest to highest distress group reduces annual return by **6.92 percentage points**, p = 0.001. The corresponding difference is 0.22 points for middle-book-to-market, p = 0.963, and 3.65 points for high-book-to-market, p = 0.088. Hence most of the widening value premium comes from the growth leg. The 6.36% return of distressed growth is slightly below the sample risk-free return according to the text; it is not a negative nominal return.

The highest-distress value spread is 13.56% among small firms and 15.33% among large firms, compared with 4.32% and 3.42% in the lowest-distress group. The distressed growth legs return 8.10% and 4.62%, respectively. “Large” here means the upper half under the main all-security split; it should not be translated into an institutional large-cap universe. In separate NYSE-size-quintile checks, distressed growth returns are 8.2%, 7.1%, and 4.2% in the first three quintiles, so the effect is not confined to the very smallest stocks.

The factor test regresses monthly value-weighted portfolio excess returns on the Fama–French market, SMB, and HML factors:

$$
r_{g,t}=\alpha_g+\beta_{M,g}(R_{M,t}-R_{f,t})
+\beta_{S,g}SMB_t+\beta_{H,g}HML_t+\varepsilon_{g,t}.
$$

Table III, printed page 2326/PDF page 10, uses postranking exposures over the full July 1965–June 1996 sample. Distressed growth is not assigned low conventional exposure. For small firms its market, SMB, and HML loadings are 1.05, 1.61, and 0.09; for large firms they are 1.26, 0.76, and −0.44. In the low-distress growth group the corresponding triples are 0.92, 1.12, −0.29 and 0.92, −0.10, −0.42. Size and market exposure generally increase with O-score.

The distressed-growth alphas are **−0.73% per month**, t = −3.73, for small firms and **−0.87%**, t = −4.42, for large firms. Their simple average is −0.80% monthly, or −9.6% under the article's linear annualization. That is distinct from compounding −0.8% for twelve months and from an annual buy-and-hold abnormal return. Distressed value has small/large alphas of 0.11% and −0.40%, neither statistically significant. The factor rejection is thus concentrated where the descriptive return evidence points.

The NYSE-size-quintile robustness yields distressed-growth intercepts of −0.78%, −0.81%, and −0.83% in the first three groups, with t-statistics −4.51, −3.40, and −2.77. The last two alphas remain negative but have limited power because there are few firms. Full-sample unconditional FF3 exposures are a benchmark, not an exhaustive account of state-dependent disaster or liquidity risk. The study does not fit conditional betas, an SDF, or a structural default-payoff model.

## Subsequent fundamentals and announcement evidence

Figure 1, printed page 2328/PDF page 12, follows size-adjusted median return on assets over five years before and after formation. In low-distress firms, growth has persistently higher profitability than value, matching the familiar Fama–French pattern. In the highest-distress quintile the ordering reverses: low-book-to-market firms have lower profitability than high-book-to-market firms throughout the surrounding period. The graph shows a recovery after a formation-year earnings trough, but no transition to the superior profitability one might expect from their expensive valuations.

Performance-related delisting incidence reinforces the distinction. During the following year, 6.58% of distressed growth firms and 5.28% of distressed value firms are delisted for performance reasons. This is evidence that the former are not simply lower-default businesses. It is not a direct estimate of systematic risk, and survival and missing-accounting-data rules matter for the long event-time profitability profiles. The article does not provide cohort counts at each horizon or a decomposition of survivor and exit effects.

For the expectations test, use quarterly Compustat announcement dates from **July 1971 through June 1996**. Measure a stock's three-day return around the announcement, from day −1 through +1, and subtract the announcement-window return benchmark formed from middle-40%-book-to-market firms in the same size decile and quarter. Average the four quarterly abnormal announcement returns in the following holding year and multiply by four. Thus the published “annualized” numbers summarize roughly twelve announcement days; they are not full-year abnormal returns or a continuously rebalanced event strategy.

Table IV, printed page 2330/PDF page 14, reports:

| Distress quintile | Equal-weighted growth announcement return | Equal-weighted value announcement return | Equal-weighted value spread | Value-weighted value spread |
|---|---:|---:|---:|---:|
| Lowest | −1.27% | 0.87% | 2.14% | 0.16% |
| 2 | −0.43% | 0.81% | 1.24% | 0.11% |
| 3 | −0.85% | 1.38% | 2.23% | 0.14% |
| 4 | −1.07% | 1.63% | 2.70% | 1.23% |
| Highest | −1.12% | 2.27% | 3.39% | 2.14% |

The highest-distress equal-weighted spread has p rounded to 0.000. Its value-weighted counterpart has p = **0.063**, so the stronger significance claim does not extend uniformly across weighting conventions. Within the growth group, moving from low to high distress changes equal-weighted announcement return by only 0.15 points, p = 0.782. The rising announcement spread is mainly associated with more positive value announcements, not progressively worse growth announcements. This nuance matters because the full-year return result is mainly driven by growth underperformance.

Announcement concentration is consistent with expectation correction but not uniquely diagnostic. Earnings releases may carry more information for distressed firms, or distressed firms may preannounce or postpone bad news. The authors explicitly discuss both possibilities and report greater variation in announcement spacing among high-O-score firms. A strict reproduction must specify how missing quarters, unusual announcement intervals, overlapping windows, and multiple announcements are handled. Those details are not fully given.

## Analyst coverage and the nature of the growth story

IBES coverage supplies an information-environment proxy. Residual coverage equals the number of analysts following a firm minus the mean analyst count in its NYSE size quintile. It is a within-size adjustment, not a residual from the main return model. Low-book-to-market firms are covered by analysts at rates of 60% in the lowest-distress group and 35% in the highest; the corresponding high-book-to-market figures are 65% and 52%. High-distress growth also has the lowest residual coverage in the reported comparisons.

There is a source-date discrepancy to preserve. Footnote 13 states that the section uses ranking years from **1976 onward**, when IBES becomes available. Table V's caption instead gives returns from **July 1981 through June 1996**. The table's numerical results should therefore be associated with its stated 1981–1996 window, while the broader coverage discussion may use the earlier availability window. The article does not explain the five-year difference, and exact replication needs that clarification rather than a silently chosen date.

Table V independently crosses five NYSE size groups, three book-to-market groups, and three residual-coverage groups. In the lowest-coverage category, value-minus-growth annual returns decline across size quintiles from 16.49%, 12.55%, and 7.74% to 5.23% and 5.97%. In the highest-coverage category they are 8.86%, 2.57%, 4.97%, 3.53%, and −2.64%. The small/low-coverage growth leg earns only 3.20%, versus 19.69% for its value counterpart. The large/high-coverage growth and value legs return 17.13% and 14.49%, producing the −2.64% spread with p = 0.591.

Mean analyst counts make the economic size of this contrast concrete: low-coverage cells range from 0.00 analysts in the smallest group to 8.59 in the largest; high-coverage cells range from 2.83 to 29.74. A low residual-coverage label therefore means different absolute attention across size groups. In unreported joint tests, both O-score and coverage retain incremental explanatory power. These are complementary conditioning variables, not evidence that analyst coverage causally corrects mispricing; coverage itself responds to investor demand, business complexity, and expected firm performance.

Table VI, printed page 2334/PDF page 18, further characterizes the expensive distressed firms. Their median sales growth is 15.7%, compared with 20.5% for low-distress growth and 2.8% for distressed value. Sales/assets is only 0.86, yet market equity/sales is 2.84, versus 2.36 for low-distress growth and 0.26 for distressed value. Their capital expenditure/assets is 0.079, the highest displayed firm-level cell, and R&D/assets is 0.015. R&D is high relative to most cells but slightly below the 0.017 of low-distress growth; the table does not support calling it uniquely highest. Missing R&D is explicitly coded zero.

The industry comparisons use Fama–French's 48 industries and median industry characteristics. Distressed growth belongs to industries with sales growth 11.6%, capital expenditure/assets 0.075, and R&D/assets 0.015. These support the claim that the firms retain a growth-industry identity despite their weak own earnings. Because medians and industry aggregations are nonlinear, the firm-level 15.7% sales-growth median should not be naively compared with 11.6% to infer a precise matched-firm industry residual. The proposed story concerns valuations and weak earnings jointly, not a mechanically identified industry-adjusted growth shortfall.

## The interaction as a replication estimand

The main return table permits a useful difference-in-differences description, although it is not a causal difference-in-differences design. Write $\mu_{d,v}$ for the size-adjusted average annual return in distress group $d$ and valuation group $v$. The difference between the extreme-distress value spreads is

$$
(\mu_{H,H}-\mu_{H,L})-(\mu_{L,H}-\mu_{L,L})
=14.44-3.87=10.57\text{ percentage points}.
$$

Equivalently, it is the value firms' high-minus-low distress difference, 3.65 points, minus the growth firms' −6.92-point difference. This identity isolates the interaction from the unconditional value premium and gives a precise target for a replication. It also prevents an incorrect reading that high distress lowers returns for all valuation groups: the table has nearly no distress-return difference in the middle group and a positive, weakly significant difference in value.

Inference on 10.57 points cannot be obtained by subtracting or comparing the separate cell p-values. Construct the monthly portfolio that is long distressed value and low-distress growth, and short distressed growth and low-distress value, with the same small/large averaging as the source. Its time series supplies the covariance among all four cells. The annual buy-and-hold contrast remains the reported economic magnitude; a test based on the monthly interaction portfolio is an inferential counterpart, not automatically the same compounded investment payoff. The source does not tabulate a standard error for this particular 10.57-point contrast.

The nonnegative-book-equity restriction also defines the estimand. Some severely distressed firms with negative equity are excluded, so the evidence describes distress within the retained accounting universe. Reinstating those firms requires a valuation classification other than an ordinary positive book-to-market rank and would be a new experiment. This boundary matters when translating the result into a production distress screen: a model designed to predict all bankruptcies and a conditional return test among positive-book firms need not use the same eligible population.

## Robustness, implementation, and limits

Using Altman's Z-score produces the same qualitative interaction: the most distressed low-book-to-market portfolio earns 5.95% and its value counterpart 17.87%. The article reports a 0.62 rank correlation between its distress measures but does not provide the full Z-score implementation and sign convention; ranking “highest distress” must be aligned carefully because raw Altman scores normally run in the opposite direction. A simple market-leverage sort does not reproduce the O-score pattern: the book-to-market spread is smallest in the highest-leverage group.

Removing firms with less than five years on CRSP preserves the result, arguing against a pure recent-IPO effect. The prior gains of distressed growth also work against a conventional positive-momentum explanation of its subsequent underperformance. The authors examine exchange subsamples, formation periods 1965–1979 and 1980–1995, industry-adjusted book-to-market, market regimes, and positive/negative GNP-change periods. In each qualitative check the value spread is largest at high O-score. High-distress value beats growth in 62.4% of sample months, compared with 55.6% in low distress. Across the four reported market-movement regimes, the high-distress value spreads are 22.99%, 10.47%, 24.47%, and 4.05%. Exact regime boundaries and complete subsample tables are not supplied.

For reproduction, the first milestones are the 30 cell counts and Table I medians, followed by the annual return matrix and monthly FF3 intercepts. Preserve the main all-stock breakpoints and the separate NYSE-quintile checks. Store firm membership, formation weights, monthly wealth evolution, and delisting adjustments so that annual buy-and-hold returns are not accidentally replaced by annually compounded monthly rebalanced returns. Reconcile the announcement benchmark construction and the IBES date discrepancy before attempting to match those tables. No stock-level dataset, code, full Compustat mapping, accounting-date filter, or standard-error bandwidth is supplied.

For investment use, this is a conditioning result about where expensive stocks perform poorly, not a demonstrated net short strategy. The vulnerable firms are often small, weakly covered, and financially fragile; their borrow availability, fees, recall risk, spreads, impact, and tail returns are not measured. The paper gives no turnover, capacity, margin, short-rebate, or market-neutral portfolio optimization. A robust implementation would compare excluding distressed expensive firms from a long book with shorting them, since those actions have different frictions and risk budgets. Such a comparison would be new work, not a reported conclusion.

The evidence supports a narrow but useful statement: book-to-market and accounting distress interact, and the joint expensive-distressed category has returns and earnings outcomes that standard distress-premium intuition and unconditional FF3 do not explain. The announcement and attention results make systematic valuation error plausible, while the missing risk dimensions, endogenous coverage, finite sample, and multiple explored splits leave room for competing accounts. The study is most useful for designing conditional value tests and for avoiding the assumption that a high default score automatically identifies a high expected equity return.
