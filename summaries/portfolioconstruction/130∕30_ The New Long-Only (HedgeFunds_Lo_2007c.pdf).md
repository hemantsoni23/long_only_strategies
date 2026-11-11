# 130/30: The New Long-Only

Andrew W. Lo and Pankaj N. Patel, *The Journal of Portfolio Management*, Winter 2008, pp. 12–38. [Published source PDF](../../Finance/HedgeFunds_Lo_2007c.pdf), 27 PDF pages. The library also contains an [earlier version](../../Finance/HedgeFunds_Lo_2007.pdf); it is the same research work, not a second independent paper. The filename year 2007 differs from the published issue year 2008. This note follows the published version, including its appendices.

## Why this matters

A 130/30 equity portfolio invests 130% of net capital in long positions and sells short securities worth 30%. Its net equity investment is 100%, but its gross exposure is 160%. Those accounting facts do not determine its beta, volatility, or expected excess return. Lo and Patel propose a transparent, mechanically rebalanced strategy as a benchmark for evaluating managers who use this investment format.

The paper’s contribution is both conceptual and operational. A passive benchmark need not be a static capitalization-weighted basket: it can be a disclosed algorithm without discretionary security selection. The authors provide a concrete monthly strategy using ten public-style valuation and technical signals, an S&P 500 universe, and a commercial risk model and optimizer. The resulting January 1996–September 2007 backtest allows comparisons under the same broad shorting and leverage framework.

In their low-turnover implementation, the annualized arithmetic mean return is 11.76%, compared with 10.50% for the S&P 500. Realized tracking error is 1.83%, giving an information ratio of about 0.69. But the corresponding signal-based long-only portfolio earns 11.56%. Thus the extension’s incremental mean advantage over that closer comparator is only 0.20 percentage points annually in this particular experiment. The 1.26-point advantage over the market cannot all be attributed to permission to short.

## Portfolio accounting and the reason for an integrated benchmark

Let $w_i$ be a signed holding weight relative to net asset value. At rebalancing, a 130/30 portfolio satisfies

$$
\sum_i w_i^+=1.30,\qquad \sum_i w_i^-=0.30,\qquad
\sum_i w_i=1,\qquad \sum_i|w_i|=1.60,
$$

where $w_i^+=\max(w_i,0)$ and $w_i^-=\max(-w_i,0)$. The first two equalities specify actual long and short exposure, not a 30% short limit that the optimizer may leave unused.

If $b$ is the benchmark weight vector, active weights $a=w-b$ sum to zero. For a long-only portfolio, $a_i\ge-b_i$: a small benchmark holding allows only a small negative view. Permitting $w_i<0$ relaxes that restriction. It can allow a negative signal to enter the portfolio and change which long positions are attractive under joint risk constraints.

The exposure identity alone does not imply market neutrality of a separate 30/30 sleeve. An arbitrary decomposition into a long-only book plus a self-financing overlay is an accounting decomposition; it need not reproduce the solution from integrated optimization. The paper accordingly evaluates the full portfolio rather than adding separately optimized long and market-neutral strategies.

A generic factor decomposition illustrates the risk issue:

$$
R_p=\beta_pR_m+\varepsilon_p,\qquad
\operatorname{Var}(R_p)=\beta_p^2\operatorname{Var}(R_m)+\operatorname{Var}(\varepsilon_p)
$$

when the residual is orthogonal to the market. Gross exposure of 1.60 need not create a beta of 1.60. The authors explicitly constrain model beta to one and keep individual active weights narrow. Nevertheless, a unit beta and market-like volatility do not eliminate financing, borrow, recall, or short-squeeze risk.

The economic benefit requires useful return forecasts. Buying 130% of exactly the benchmark and shorting 30% of the same exposures simply reproduces the benchmark before costs. The paper does not establish that the 130/30 format creates return by itself, or that 30% is the optimal short extension for every manager and risk budget.

## Sample and information timing

The simulation runs monthly from January 1996 through September 2007, 141 months. It begins with \$100 million in cash and then uses the preceding month’s portfolio as the initial portfolio for each rebalance. The tradable universe and benchmark are the S&P 500. Signal normalization also uses the broader S&P 1500, which must therefore be distinguished from the investment universe.

The expected-return inputs are Credit Suisse Quantitative Equity Research composite scores; the risk input is the Barra US Equity Long-Term Risk Model. Portfolio construction uses the MSCI Barra Aegis Portfolio Manager. The authors state that investable-index weights use only information available before each rebalance. Reproducing that claim requires dated constituents, financial-statement availability, contemporaneous analyst forecasts, and historical risk-model files. Applying the recipe to later restated fundamentals or today’s surviving constituents would be a different, biased experiment.

The paper describes commercial data and algorithms in considerable detail, but the PDF is not a complete historical data archive. It does not supply every security-level observation, vendor revision, corporate-action adjustment, missing-value convention, or optimizer-version default. “Transparent” in the proposed benchmark sense should not be confused with a claim that the PDF alone is sufficient to regenerate all weights.

## Signals: the complete family structure

The ten composite factors are equally weighted after within-factor construction. Their ingredients, drawn from Appendix A.1, are as follows.

| Composite | Constituent measurements |
|---|---|
| Traditional value | Price to 12-month forward consensus earnings, trailing 12-month sales, trailing 12-month cash flow, and latest quarterly book value; dividend yield. |
| Relative value | Industry-relative price to trailing sales, trailing earnings, and trailing cash flow; each current industry-relative spread compared with its five-year average. |
| Historical growth | Signed consecutive increases in trailing cash flow and trailing earnings over up to 24 quarters; 12-month change in trailing cash flow; three-year average annual sales and earnings growth; normalized 12-quarter trend slopes in trailing earnings and cash flow. |
| Expected growth | I/B/E/S five-year expected earnings growth; expected fiscal-year-2 versus fiscal-year-1 earnings growth. |
| Profit trends | Signed runs of improvement in receivables plus inventories relative to sales, cash flow relative to sales, and overhead relative to sales; industry-relative receivables plus inventories to sales and sales to assets; overhead to sales and earnings to sales. |
| Accelerating sales | Three- and six-month changes in the annual sales-growth measure; change from one year earlier in the normalized four-quarter sales trend slope. |
| Earnings momentum | Four- and eight-week changes in forward consensus earnings divided by price; last earnings surprise divided by price; standardized unexpected earnings. |
| Price momentum | 52-week price trend slope, distance above the 260-day low, 4/52-week price oscillator, 39-week return, and 52-week volume-price trend; all calculated with a 20-day lag. |
| Price reversal | Five-day and four-week industry-relative returns; five-day signed money flow; 12–26-day MACD less its 10-day signal line; 14-day RSI; 20-day Lane stochastic indicator. |
| Small size | Log market capitalization, the listed “Log of Market Capitalization Cubed” measurement, log stock price, log latest-quarter assets, and log trailing sales. |

Several details are necessary to implement this table. Forward 12-month earnings interpolate FY1 and FY2 forecasts, with FY1 weighted by the fraction of days remaining in the year and FY2 by the complement. Trailing flows sum four quarterly observations. Receivables, inventories, and assets in the relevant ratios use averages of the current and year-earlier quarter. Overhead is sales less cost of goods sold less EBEX, using trailing four-quarter totals.

A signed run starts at the most recent quarter and stops when the direction changes, with a maximum lookback of 24 quarters. Declines in overhead or receivables-plus-inventory ratios count positively; improving cash-flow or earnings measures also count positively. A normalized trend fits a linear slope over the specified quarterly observations and divides it by their average level. This creates practical issues near zero or negative denominators, for which the paper gives no general repair rule.

For accelerating sales, the annual growth measure is the change in trailing sales divided by the absolute value of year-earlier trailing sales; the three- or six-month signal is the change in that measure. The price oscillator is the average price over four weeks divided by its 52-week average, minus one. Five-day money flow sums price times volume with a negative sign on negative-return days and divides by unsigned price times volume over the same window.

The technical-indicator conventions for volume-price trend, MACD, RSI, and Lane’s indicator are delegated to a cited reference. Likewise, the phrase describing the cubed market-capitalization variable does not unambiguously specify whether the cube is inside or outside the logarithm; exact code is needed. The general relative-value description refers to industry medians and mentions book ratios, while the detailed appendix lists sales, earnings, and cash-flow ratios. A faithful implementation should use the detailed listed inputs and document the remaining vendor definition rather than silently choose between prose variants.

Value ratios are inverted, except dividend yield, so that high values correspond to a favorable signal. Price-reversal and size measures are multiplied by −1. Two profit-trend levels—industry-relative receivables plus inventories to sales and overhead to sales—are also negated. These orientation changes must precede interpreting a high composite score as high expected return.

## Normalization and forecast scaling

For a constituent measurement $x_i$ on a given date, the paper centers on its capitalization-weighted S&P 500 mean but scales by dispersion across S&P 1500 companies. In compact notation,

$$
\mu_{500}=\sum_{i\in500}b_i x_i,\qquad
s_{1500}^2\propto\sum_{i\in1500}(x_i-\mu_{500})^2,\qquad
z_i=\frac{x_i-\mu_{500}}{s_{1500}}.
$$

The squared deviations are not capitalization weighted. The source does not specify the divisor convention in that standard deviation, hence the proportionality notation rather than an invented exact denominator.

The algorithm first computes these scores. It excludes observations with $|z_i|>10$ from the estimation sample, recomputes the center and scale, and then renormalizes the original full sample using the revised values. Exclusion from estimating moments does not mean permanently removing the company from the investment universe.

For each composite, constituent scores are capped at −10 and 10 and averaged equally. That average is normalized by the same two-step procedure. For each S&P 500 stock, the final signal is the equal-weighted average of its ten composite scores:

$$
q_i=\frac1{10}\sum_{k=1}^{10}z_{ik}^{\rm composite}.
$$

The optimizer’s expected-return input is this score with a return multiplier of 0.0100. Scores are therefore not literal realized monthly excess returns. Their scaling interacts with risk aversion and transaction-cost penalties; replacing scores by ranks or rescaling them without adjusting the optimizer changes the selected portfolio.

## Optimization: settings and mathematical interpretation

The benchmark and universe are both the contemporaneous S&P 500. Base value is net value, cash contribution is zero, and the optimization type is long-short. Long exposure has minimum and maximum 130%; short exposure has minimum and maximum 30%. Model beta has a hard lower and upper bound of one. General holding bounds are benchmark weight plus or minus 0.40 percentage points, or 40 basis points:

$$
b_i-0.004\le w_i\le b_i+0.004.
$$

Interpreting the display value 0.40 as a decimal weight of 40% would radically change the experiment. This restriction permits short positions mainly where benchmark weights are sufficiently small.

The source sets risk aversion to 0.0075 and the AS-CF ratio to one. Expected risk-free return, benchmark and market premiums, and expected benchmark or market surprises are all zero within the optimizer. The return-distribution display uses mean zero, 24 bins, and a 5% probability level, with the −100% truncation option unchecked. These interface settings are not a statement that the backtest deducts zero financing cost or estimates a 5% VaR constraint.

A useful conceptual representation is to maximize forecast active return less a risk penalty and a trading-cost penalty, subject to the exposure and holding restrictions:

$$
\max_w\left\{\widehat\alpha'w-\lambda\mathcal R(w,b,\widehat\Sigma)-\eta\mathcal T(w,w^{\rm initial})\right\}.
$$

This equation is a reconstruction of the economic structure, not the published mathematical objective of the proprietary optimizer. The PDF supplies interface values but does not define how the software maps 0.0075 to a covariance penalty or implements all long-short constraints. Replacing it with an arbitrary quadratic program and treating its output as exact replication would be unwarranted.

The three turnover cases are particularly easy to misread. The appendix leaves all hard turnover and trade-limit boxes unchecked. Instead, it changes the transaction-cost penalty:

| Case name | Cost entered in optimization | Cost multiplier |
|---|---:|---:|
| Approximately 15% annual turnover | 0.25% one way | 12.0000 |
| Approximately 100% annual turnover | 0.25% one way | 0.7500 |
| Unconstrained turnover | 0% | 1.0000 |

Thus 15% and 100% are approximate turnover outcomes, not hard annual ceilings. The 15% case reaches 16.2% in 2000. The unconstrained optimizer ignores trading costs while its reported investable return subsequently pays them. The transaction-cost multipliers shape portfolio choice; they are not the actual costs deducted from the simulated return.

Market impact is turned off; tax costs, advanced constraints, and special penalties are disabled. Crossovers between long and short positions are allowed. There are no additional minimum holding or trading thresholds. These choices describe the experiment, not universally harmless implementation assumptions.

## Return and cost accounting

Let $S_{i,t-1}$ be signed shares held for month $t$, $P_{i,t-1}$ their initial prices, and $R_{it}$ the monthly total returns. The source’s Equation (1) is

$$
R_{pt}=\sum_i\frac{P_{i,t-1}S_{i,t-1}}{\sum_jP_{j,t-1}S_{j,t-1}}R_{it}-TC_t-SC_t,
$$

$$
TC_t=0.0025\times2\times1.6\times U_t,
\qquad
SC_t=0.30\times\frac{0.0075}{12}=0.0001875.
$$

Here $U_t$ is the optimizer’s one-way turnover divided by the total absolute value of initial positions. The factor two converts one-way turnover to the two-sided trading amount; 1.6 converts its gross-exposure denominator to net capital. Using a turnover already measured against net capital would double-count that conversion.

The financing deduction is 1.875 basis points per month, or 22.5 basis points per year under arithmetic addition. It represents the assumed spread between the short rebate and leverage borrowing cost. It is deducted outside the optimizer. A monthly turnover of 1% adds 0.8 basis points of trading cost; annual turnover of 15% would add 12 basis points annually under the printed formula. Actual turnover varies, so those figures are illustrative rather than a claim that every year has identical cost.

Transaction cost is set to zero for the initial January 1996 formation. Annual turnover figures also exclude that initial formation month. The perfect-foresight index assumes zero transaction costs throughout and zero shorting costs. These conventions favor the simulated indices relative to a fully funded implementation that pays initial execution and faces security-specific borrowing costs.

The long-only comparison sets exposure to 100% long and zero short while retaining the relevant construction settings. Its gross-to-net conversion is one and it has no short-spread deduction; one should not mechanically apply the 1.6 leverage factor to that portfolio.

## Results, units, and comparisons

Exhibit 1 reports arithmetic monthly mean returns multiplied by 12, and annualized standard deviations. Sharpe ratios use an assumed constant annual risk-free rate of 5%. The full-sample figures are:

| Portfolio | Annualized mean | Annualized SD | Sharpe | Maximum drawdown |
|---|---:|---:|---:|---:|
| 130/30, about 15% turnover, net costs | 11.76% | 15.22% | 0.44 | −44.9% |
| Same low-turnover portfolio, gross costs | 12.07% | 15.22% | 0.46 | −44.5% |
| 130/30, about 100% turnover, net costs | 14.25% | 15.15% | 0.61 | −36.5% |
| 130/30, unrestricted turnover, net costs | 14.08% | 15.10% | 0.60 | −35.4% |
| Perfect-foresight 130/30, no costs | 127.98% | 18.01% | 6.83 | −2.9% |
| S&P 500 | 10.50% | 14.68% | 0.37 | −44.7% |

For the principal case, $(11.76-5)/15.22=0.444$ verifies the reported Sharpe ratio. Its arithmetic excess return over the market is 1.26 percentage points. The source computes realized tracking error directly from monthly net active returns as 1.83%, giving $1.26/1.83=0.689$.

These realized statistics differ from the annualized tracking-error forecasts returned each month by Barra and shown in Exhibits 3, 6, 7, A2, and A3. Averaging model risk forecasts is not the same calculation as the sample standard deviation of realized active returns. Neither quantity should be silently substituted for the other.

Exhibit 4 lists monthly returns and geometrically compounded calendar-year returns. For example, the principal 130/30 case returns 26.7% in 1998 versus 28.6% for the S&P 500, −23.0% versus −22.1% in 2002, and 13.8% versus 15.8% in 2006. It does not outperform every year. The 2007 annual table cells are January–September year-to-date returns, whereas the 2007 column in Exhibit 1 annualizes the average of those nine monthly returns.

The short side has negative standalone returns in every displayed year except 2002. That observation does not measure its incremental contribution to the integrated solution: it permits different long holdings and offsets risk. Conversely, the diversification explanation does not prove that every short is worthwhile after costs; that requires the counterfactual joint portfolio calculation.

Exhibit 5 reports correlations in percent. The principal portfolio’s correlation with the S&P 500 is 99%, and its correlation with the CS/Tremont all-funds index is 52%, versus 50% for the S&P 500. These confirm that the product behaves predominantly like a large-cap equity allocation, not a market-neutral hedge fund. Equity-index correlations extend through September 2007, while the other-market and hedge-fund panels end in August.

The unrestricted strategy turns over roughly 350% annually, compared with the low-turnover case’s 6.2%–16.2% range over full displayed years. Its slightly lower net mean than the 100% case is consistent with higher implementation costs. The paper does not provide a formal statistical test establishing an optimal turnover penalty. The low-turnover portfolio typically holds approximately 270 long names and 150 short names; the broad diversification is an outcome of the tight active-weight bounds and universe, not evidence of independent bets.

Appendix A.3 is essential to attribution. The same signals and comparable settings in a long-only format produce about 9% annual turnover, an annualized mean of 11.56%, volatility of 14.91%, Sharpe 0.44, and maximum drawdown −43.3%. It already exceeds the market’s mean by 1.06 points. The 130/30 low-turnover case exceeds it by just 0.20 points, with somewhat higher volatility. Since turnover and feasible exposures change together, this is not a perfectly isolated causal estimate of the effect of shorting.

## The perfect-foresight comparator is not an attainable forecast

The look-ahead index replaces the forecast score with the stock’s realized one-month-forward return minus the S&P 500 return. It is deliberately noninvestable. The displayed series also has no turnover restriction and pays neither trading nor shorting costs. Its enormous arithmetic mean, 127.98% annually, cannot be compared with net investable returns as if both faced the same information and cost conditions.

The authors describe the look-ahead result as an upper bound on available alpha. More precisely, it is their perfect-information optimizer benchmark. An algorithm maximizing a risk-penalized objective need not maximize realized return alone. Moreover, different penalties and cost conventions change the comparison set. Establishing a mathematical upper bound on net return would require explicitly maximizing that same net-return objective over a common feasible set; the paper does not present such a proof. The series is useful as an opportunity diagnostic, with that qualification.

## Interpretation and replication limits

The strategy’s repeatable signals may capture compensated risks or widely available return patterns. The authors therefore resist interpreting its excess return as proprietary manager skill. A manager benchmarked against this index would have to add value beyond the disclosed rule, not merely exploit the permission to short or the same public-style signals.

A serious replication should archive each month’s universe, point-in-time constituent inputs, score transformations, risk file, initial holdings, optimized holdings, model beta, constraint violations, turnover denominator, and cost deductions. It should separately reproduce Exhibit 1’s arithmetic annualization, Exhibit 4’s geometric annual returns, the risk model’s forecasts, and the realized information ratio. The printed monthly tables provide rounded cross-checks but cannot recover all security-level trades.

Remaining dependencies include commercial historical score and risk data, optimizer scaling and conventions, exact technical-indicator definitions, missing and negative accounting inputs, analyst-release timing, corporate actions, and short-stock availability. The fixed 0.75% spread and zero market-impact assumption suppress important variation in financing and capacity. Management fees and taxes are not incorporated as investor-specific costs. No confidence interval or formal sampling test accompanies the headline information ratio, and the period ends before the subsequent full financial crisis.

The durable result is a benchmark-design principle supported by a worked historical construction: mechanical, disclosed dynamic strategies can be useful comparators for similarly constrained managers. The backtest illustrates possible benefits and costs of relaxing long-only restrictions; it does not establish universal dominance of 130/30 portfolios or an unconditional optimal amount of leverage.
