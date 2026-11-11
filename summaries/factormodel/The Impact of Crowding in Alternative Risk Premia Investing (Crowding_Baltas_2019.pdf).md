# The Impact of Crowding in Alternative Risk Premia Investing

Nick Baltas, *Financial Analysts Journal* 75(3), Third Quarter 2019, pp. 89–104, DOI 10.1080/0015198X.2019.1600955. Submitted September 19, 2018; accepted March 20, 2019. The source is the 16-page published article, including its methodological endnotes and references. An earlier June 2018 Goldman Sachs version is mentioned but is not the version summarized here.

Source: [Crowding_Baltas_2019.pdf](../../Finance/Crowding_Baltas_2019.pdf).

## Why this matters

A common crowding indicator need not have the same investment implication for every factor. Baltas distinguishes strategies whose own trading reinforces their signal from strategies whose trading closes the opportunity. Momentum is the main reinforcing example: inflows push winners up and losers down, preserving their ranks. Relative value is the main convergent example: buying cheap assets and selling expensive ones narrows valuation spreads and eventually changes which assets qualify.

The empirical contribution is to apply a signed residual-correlation measure of crowdedness to multiple equity, currency, and commodity strategies, and compare subsequent returns conditional on high versus low crowding. First-year performance differs sharply across states, with negative high-minus-low differences for momentum, low beta, and quality, but positive differences for equity and currency value. Size is a counterexample to the proposed convergence classification.

The evidence is an overlapping historical event study of portfolios frozen at formation. It does not directly observe investor flows, estimate market capacity, isolate a causal effect of crowding, or demonstrate a profitable implementable factor-timing strategy after trading costs.

## Mechanism and hypotheses

“Divergence” denotes a positive-feedback strategy. In momentum, price increases strengthen the winner signal and price decreases strengthen the loser signal. Sufficient inflows can therefore sustain the same long and short holdings. Falling turnover during strong performance is consistent with this mechanism. Without a valuation anchor, the strategy itself does not identify a fundamental stopping point.

“Convergence” denotes a strategy with a natural anchor. For book-to-price value, buying cheap stocks raises their prices and lowers their book-to-price ratios; selling expensive stocks works in the opposite direction. The signal weakens as the trade succeeds. New cheap and expensive assets then replace the old holdings. Faster convergence can create a reason to rebalance more responsively, even if crowding ultimately compresses expected future opportunity.

These are qualitative mechanisms, not a solved price-impact equilibrium. No calibrated flow-to-price coefficient, investor-demand equation, or law for convergence time is estimated. The paper explicitly leaves the long-run disappearance of premia and the consequences of simultaneous forced liquidation outside its main empirical question.

Figures 2 and 4 examine global equity portfolios from December 2005 to April 2018. The construction combines three quarterly rebalanced strategies staggered across the months of a quarter. The contemporaneous relation between rolling annual return and cumulative annual turnover has $R^2=0.60$ and a negative slope for momentum, versus $R^2=0.16$ and a positive slope for value. The momentum association reportedly remains after excluding the pre-2010 period. These are descriptive relationships using overlapping annual observations; they are not independently identified flow shocks.

## Universes, signals, and portfolio construction

Table 1 specifies three asset-class universes:

| Asset class | Sample | Data | Portfolio tails |
|---|---|---|---|
| Global developed-market equities | September 2004–May 2018 | Worldscope and Axioma | Top and bottom deciles |
| 24 S&P GSCI commodities | January 1999–May 2018 | Bloomberg | Top and bottom thirds |
| 26 developed and emerging currencies against USD | January 2000–May 2018 | Bloomberg | Top and bottom thirds |

Equity strategies use book-to-price value, market-capitalization size, return-on-assets quality, low beta relative to MSCI World, and volatility-adjusted momentum. Equity momentum is the residual from a cross-sectional regression of the prior twelve-month return excluding the most recent month on stock volatility estimated over the same interval. This is a cross-sectional signal adjustment, separate from the time-series factor regression used to measure crowding.

Commodity and FX momentum use prior twelve-month returns; the table does not specify the same one-month skip as for equity momentum. Currency value uses purchasing power parity. The exact PPP series, base dates, publication lags, interpolation, and ranking formula are not supplied. Likewise the beta lookback, accounting-release lag for equity fundamentals, detailed equity liquidity filters, treatment of negative book equity, delistings, and historical membership rules are missing.

Each strategy is cash neutral, with equal weights within its long basket and equal weights within its short basket. Commodity tails contain eight assets each. For FX, the prose also describes eight assets per side even though 26 divided into thirds does not give an integer; use the stated eight for a literal reproduction and document the convention. Do not silently assume nine or fractional inclusion.

The commodity list comprises Chicago and Kansas wheat, corn, soybeans, coffee, sugar, cocoa, cotton, live and feeder cattle, lean hogs, WTI and Brent crude, gas oil, heating oil, RBOB gasoline, natural gas, aluminum, LME copper, lead, nickel, zinc, gold, and silver. Currency coverage includes AUD, BRL, CAD, CHF, CLP, offshore CNY, CZK, EUR, GBP, HUF, ILS, INR, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PLN, RUB, SEK, SGD, TRY, TWD, and ZAR against USD.

Price versus total-return treatment, futures roll conventions, FX carry inclusion, financing, collateral remuneration, trading costs, and short-borrow charges are not fully specified. The reported long–short returns should therefore be treated as source-defined research returns, not readily executable net performance.

## Reconstructing the CoMetric

At each week $t$, rank assets on the chosen signal and select that week's long and short baskets. For every selected asset $i$, regress its historical weekly returns on an intercept and an asset-class factor set:

$$
r_{i,\tau}=a_i+\sum_j\beta_{ij}F_{j,\tau}+\epsilon_{i,\tau},
\qquad \tau\in\mathcal W_t.
$$

The estimation window is 52 weeks for most strategies and $5\times52=260$ weeks for value. This longer value window is motivated by its connection with long-run reversal. Each week's current basket is evaluated using historical residual returns; the procedure is not simply correlating an already rebalanced factor-return series.

Equity factors are MSCI World, size, value, and momentum. Omit the factor being investigated: momentum crowding controls for market, size, and value; value crowding controls for market, size, and momentum. The source's sentence describing value residuals in Figure 5 is abbreviated, but Endnote 8 explicitly supplies this exclusion convention. For quality and low beta, neither is one of those four factors, so the indicated base model retains the listed controls.

Commodity factors are the GSCI commodity index and carry. FX factors are the dollar index, carry, and momentum, again excluding the factor under study where applicable. The paper does not fully specify construction of every factor return, currency conversion, or weighting used for the control portfolios.

Assign $s_{i,t}=+1$ for long-basket assets and $-1$ for short-basket assets. If there are $N$ assets in each basket, there are $2N$ assets and $N(2N-1)$ unordered pairs. Equation 2 is

$$
C_t=\frac{\sum_{i<j}s_{i,t}s_{j,t}
       \operatorname{Corr}_{\mathcal W_t}(\epsilon_i,\epsilon_j)}
       {N(2N-1)}.
$$

Thus $N$ in this denominator is the number per leg, not the total number of selected assets. Equivalently use $2/[M(M-1)]$ with $M=2N$. Within-leg correlations enter positively. Cross-leg correlations enter with a negative sign, so a long basket moving up when the short basket moves down raises the indicator. This captures both common buying and common selling rather than measuring only one side's residual correlation.

A high value is interpreted as excess comovement consistent with synchronous investor positioning. It is a proxy, not an observed amount invested. OLS makes residuals orthogonal to included regressors within the estimation sample; it does **not** imply that different assets' residuals must be mutually uncorrelated. The article's statement that residual cross-correlations should theoretically vanish therefore requires an additional complete-factor-model assumption. Omitted common fundamentals or sector risks can also raise $C_t$.

Figure 5 shows persistent variation rather than a mechanically rising industry-wide crowding trend. Endnote 12 reports five-year-window mean CoMetrics of 1.42% for momentum and 3.23% for value, with time-series standard deviations 0.59% and 0.66%, respectively. These are correlation-scale quantities: 1.42% means 0.0142, not a factor return. Top-only and bottom-only crowding indicators have correlations of 0.51 for momentum and 0.43 for value. Using either leg separately reportedly gives broadly similar findings, but detailed robustness tables are not shown.

## Event-study design and inference

For each strategy, classify the top 20% of weekly $C_t$ observations as high crowding and the bottom 20% as low crowding. Form each event portfolio using the ranks at that event, then hold those original positions for up to two years. The long-horizon curves deliberately do not update factor membership as ranks evolve. A current crowding signal may say something about today's holdings without predicting the return of a continuously reconstituted factor.

Average the subsequent buy-and-hold paths separately by crowding state. Tables 2–3 show first-month, first-six-month, first-year, and second-year returns. Figures 6 and 8 add 95% confidence bands; significance uses Newey–West heteroskedasticity- and autocorrelation-robust errors. Stars indicate 5% and 1% two-sided significance, respectively.

The HAC lag length, exact regression design for high-minus-low inference, missing-data treatment, and return aggregation conventions are not given. Weekly events with multi-year holding periods overlap extensively. Nominal event counts are not numbers of independent observations, and persistence of the crowding state further concentrates effective information in a few episodes.

The percentile thresholds appear to classify the historical sample as a whole; an expanding or rolling ex ante threshold rule is not specified. Therefore the published event study is not an out-of-sample timing simulation. Endnote 10 requires at least 1.5 years of subsequent performance and says event selection ends 1.5 years before the sample ends, although figure captions describe selection through May 2018. Full two-year returns for the latest eligible events would require an additional convention. These inconsistencies should be resolved before claiming an exact replication.

## Main numerical evidence

The following values reproduce first-year columns of the published tables. High and Low are average source-defined buy-and-hold returns. H–L is the table's reported difference in percentage points, and the t-statistics are given in the discussion.

| Strategy | High | Low | Reported H–L | H–L t-statistic |
|---|---:|---:|---:|---:|
| Equity momentum | −5.91% | 6.86% | −12.78 pp | −9.12 |
| Equity low beta | −20.11% | 8.74% | −28.85 pp | −8.41 |
| Equity quality | −4.74% | 8.72% | −13.47 pp | −5.14 |
| FX momentum | −1.05% | 1.38% | −2.44 pp | −3.07 |
| Commodity momentum | −3.21% | 2.32% | −5.53 pp | −2.92 |
| Equity value | 5.45% | −11.61% | 17.05 pp | 11.78 |
| Equity size | 3.55% | 7.67% | −4.12 pp | −2.12 |
| FX value | 5.04% | 1.32% | 3.72 pp | 5.86 |

All five first-year divergence H–L differences are significant at 1% in the source. The equity-size difference is significant at 5% and has the opposite direction to the simple convergence hypothesis. Equity value and FX value support the positive convergence association.

The divergence effect is not immediate. First-month H–L values are −0.57 pp for equity momentum, −2.66 for low beta, −0.72 for quality, −0.04 for FX momentum, and −0.31 for commodity momentum, all statistically insignificant. At six months the reported differences are −6.83, −17.36, −7.80, −1.26, and **+0.51** pp, respectively. The first four are significant at 1%; commodity momentum is not. Thus the broad prose claim that all divergence strategies underperform over six months to a year needs a horizon qualification: commodity momentum's six-month difference is positive and insignificant, while its annual difference is negative and significant.

For convergence strategies, first-month H–L is +1.54 pp for equity value, approximately zero for size, and +0.33 pp for FX value. Only equity value is significant there. Six-month high and low returns are 5.85% and −5.71% for equity value, 2.19% and 4.76% for size, and 2.72% and 0.94% for FX value. The reported corresponding differences are +11.56, −2.58, and +1.78 pp; size is insignificant, with t-statistic −1.58, while both value differences are significant at 1%.

Second-year differences mostly weaken. Table 2 reports H–L of +1.63 pp for equity momentum, −16.25 for low beta, −0.76 for quality, −1.43 for FX momentum, and −0.18 for commodity momentum. Only low beta and FX momentum are significant at 5%. Table 3 reports +0.54 pp for equity value, −7.41 for size, and +1.29 for FX value; size alone is significant, at 1%. These results do not establish a permanently higher or lower expected return conditional on one initial crowding measurement.

## Numerical discrepancies and reproducibility gaps

Several second-year table differences are not the arithmetic difference of the displayed High and Low means, beyond rounding. Equity momentum has 1.42% versus −0.52%, whose subtraction is 1.94 pp, but H–L is printed as 1.63 pp. Equity value has −4.64% versus −6.91%, implying 2.27 pp, but the table gives 0.54 pp. The PDF does not explain a different weighting or sample selection for these differences. Preserve the reported values as reported, without using them as arithmetic identities or inventing a compounding explanation.

Reported event counts also need clarification. The tables give 173 events in each high and low equity divergence state, 248 for FX momentum, and 260 for commodity momentum; value counts are 111 for equities and 186 for FX. These are difficult to reconcile with 20% of weekly observations over the stated dates, especially after lookback and forward-performance exclusions. The article does not supply a calendar or alternative sampling rule resolving that issue. The counts should be documented as printed rather than reverse-engineered into an undocumented sample.

A reproduction should therefore separate three levels of success: implementing the stated signed-correlation indicator, reproducing qualitative conditional-return patterns on a documented dataset, and exactly matching published tables. The third requires missing data and methodological details, not merely coding the displayed equations.

## Investment interpretation and limits

The article motivates different risk treatment for divergence and convergence strategies. If crowded divergence portfolios have greater forward volatility, reducing their exposure can help; convergent value opportunities may instead improve as common buying accelerates valuation adjustment. The source cites volatility-management literature and describes related volatility patterns as unreported results. It does not publish an evaluated CoMetric-to-position-sizing rule, optimal thresholds, live turnover, or net risk-parity comparison.

The low-beta and quality classifications rely partly on their links with corporate leverage, profitability, and low risk. They are conceptual extensions of the momentum mechanism, not directly estimated feedback coefficients. Size's negative first-year H–L is a meaningful failure of the simple convergence prediction, not a result to discard because it is inconvenient.

Residual comovement can reflect shared fundamentals, omitted factors, changing asset membership, or macro regimes as well as trading crowding. Conditioning on it does not establish that investor inflows caused subsequent returns. A tradable extension would need point-in-time fundamentals, a defined threshold-estimation window, explicit execution lags, cost and financing assumptions, and a genuinely subsequent evaluation period. None is supplied as a completed strategy test here.

The substantive takeaway is that a blanket rule to avoid every crowded factor is not supported by these results. The sign and horizon of the association depend on the strategy's signal mechanics. That insight is useful for designing diagnostics and hypotheses, while the published table and sampling inconsistencies set practical limits on exact replication from the PDF alone.
