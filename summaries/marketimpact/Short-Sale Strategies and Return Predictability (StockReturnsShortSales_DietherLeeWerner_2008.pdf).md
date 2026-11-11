# Short-Sale Strategies and Return Predictability

Karl B. Diether, Kuan-Hui Lee, and Ingrid M. Werner. *Review of Financial Studies* 22(2), 2009, pp. 575–607; advance publication May 9, 2008; DOI 10.1093/rfs/hhn047. [Local source PDF](../../Finance/StockReturnsShortSales_DietherLeeWerner_2008.pdf). The filename's 2008 refers to the advance-publication year, whereas the supplied journal issue is dated 2009. The 33-page PDF contains the article and references, without a separate appendix. PDF page 1 corresponds to journal page 575.

## Why this matters

Daily short-sale flow is a different signal from monthly short interest. A large volume of new short sales can coexist with stable outstanding short interest when positions turn over rapidly. This paper uses regulatory transaction data across trading venues to ask whether short sellers chase declines, supply liquidity, bear temporary risk, or identify stocks that have become overpriced. Its central finding is contrarian: short selling rises after recent price increases, and heavily shorted stocks subsequently underperform lightly shorted stocks.

The contribution is both a dataset and an identification argument. Earlier studies often observed only particular trading systems or monthly positions. These authors aggregate the newly mandated 2005 short-sale records across US reporting venues for NYSE and Nasdaq stocks, then combine portfolio sorts, panel regressions, liquidity controls, and a test of subsequent buying pressure. The results provide evidence of information in executed short-sale flow beyond recent returns and several liquidity proxies.

For an implementer, the distinction between a predictive signal and an executable strategy is crucial. The portfolios earn roughly 1.4% gross abnormal return per month in the one-day specification, but the public data were not released quickly enough to trade the strategy as constructed. The paper also estimates execution costs large enough to erase the gross return. It does not observe covering transactions, trader identities, actual holding periods, or realized short-seller profits. A replication should reproduce the information-content result before making any claim about investable alpha.

## Four mechanisms and their observable predictions

Section 1, PDF page 7, distinguishes four hypotheses. Under short-term overreaction, short sellers increase selling after positive returns and before negative returns. Under voluntary liquidity provision, they meet temporary buying pressure, so short selling should coincide with positive order imbalance and precede both declining buying pressure and negative returns. Under opportunistic risk bearing driven by asymmetric information, shorting should rise when volatility and spreads are high, followed by lower volatility, narrower spreads, and negative returns. Under disagreement, high volatility is instead associated with narrow spreads, because competing liquidity suppliers have dispersed reservation values; convergence should subsequently lower volatility and widen spreads.

These are reduced-form predictions rather than mutually exclusive structural models. A trader can detect mispricing and execute passively, thereby providing liquidity at the same time. In the 2005 environment, short-sale price tests also make the association between short selling and buyer-initiated trades partly mechanical. Controlling for order imbalance therefore does not cleanly separate investor motives.

The authors interpret persistent predictability as evidence that short sellers identify deviations from fundamentals. That is narrower than proving access to private corporate information. Fundamental value is unobserved, the analysis does not randomize short sales, and alternative omitted signals remain possible. The data are consistent with informed contrarian trading; they do not identify the fundamental-value process or establish that short sales themselves cause subsequent price declines.

## Data construction, coverage, and timing

The universe begins with NYSE and Nasdaq National Market common stocks appearing in CRSP at the end of 2004, with share codes 10 or 11 and year-end prices at least \$1. Daily CRSP prices, returns, shares outstanding, and trading volumes cover the 2005 sample. The text describes January 2–December 30, but the tabulated trading sample begins January 3, 2005, the first trading day. Stocks with zero or missing CRSP daily volume are excluded on those days. Where recorded short sales exceed CRSP volume, the authors cap short sales at total volume; dropping those observations instead reportedly leaves results similar.

All self-regulatory organizations reporting short trades are used, including the NYSE, Nasdaq, AMEX, Archipelago, Boston, Chicago, NASD's reporting facility, National Stock Exchange, and Philadelphia. Table 1 reports that the NYSE itself accounts for 76.62% of shorted shares in NYSE-listed stocks. Nasdaq accounts for only 49.55% of shorted shares in Nasdaq-listed stocks, with Archipelago at 22.72% and NSX at 27.01%. Restricting data to the primary listing exchange would therefore lose economically important activity.

The text and Table 1 describe 1,481 NYSE and 2,372 Nasdaq stocks. Table 2 prints 2,373 Nasdaq stocks in its full-sample column; that one-stock discrepancy is unresolved by the supplied PDF. The principal tests exclude Regulation SHO pilot stocks, whose price-test rules changed during the year, leaving 1,079 NYSE and 2,001 Nasdaq stocks. Most portfolio and regression analyses further require lagged price at least \$5. This is not a study estimating the causal effect of the SHO pilot; that is separate work by the same authors.

The regulatory records contain short-trade ticker, price, size, time, listing market, and a nominal exempt/nonexempt flag. The exemption flag cannot reliably identify market makers because contemporaneous relief from marking requirements made it unreliable. Trade size also does not reliably identify institutional versus retail activity when institutions split orders. The absence of purchase-to-cover flags prevents direct computation of individual short positions' profits.

TAQ supplies effective spreads and daily order imbalance, with buys and sells classified using Lee–Ready. CRSP and Compustat supply market capitalization, turnover, and book-to-market. Institutional ownership comes from Thomson 13-F data, and put-option availability is obtained through the Options Clearing Corporation. Portfolio subsample classifications use prior-month size, lagged accounting information, and previous-quarter ownership rather than contemporaneous future-known characteristics.

The underlying regulatory files, merged security identifiers, intraday cleaning code, quote-matching conventions, and portfolio holdings are not included. A modern reconstruction must retain historical security membership and corporate actions, document delistings and missing returns, and specify the precise TAQ trade-direction and spread aggregation conventions. The paper cites the standard methods but does not supply every low-level data-processing choice.

## Variables and the flow-versus-stock distinction

For stock $i$ on trading day $t$, define daily relative short selling

$$
s_{it}=\mathrm{relss}_{it}=\frac{Q^{\mathrm{short}}_{it}}{Q^{\mathrm{total}}_{it}}.
$$

Use a fraction in regressions unless a table explicitly reports percent. Table 1's averages are 23.89% for NYSE stocks and 31.33% for Nasdaq stocks; the corresponding medians are 23.96% and 31.72%. These are averages of stock-level ratios, not necessarily ratios of total shorted shares to total market shares. The short-selling fraction is less skewed than raw shares or trade counts, motivating its use as the principal signal.

Monthly short interest is an outstanding stock, whereas $Q^{\mathrm{short}}$ is new activity. The basic accounting identity is

$$
S_{m+1}-S_m=\sum_{t\in m}Q^{\mathrm{short}}_t-\sum_{t\in m}Q^{\mathrm{cover}}_t.
$$

Equation (1) on PDF page 12 decomposes covering into current- and prior-month cohorts under simplified common holding periods. It is an illustration, not an estimated holding-period model. The text's numerical example has 682,000 shares sold short during a 22-day month, while outstanding short interest rises only from 4,000 to 8,000. Covering must then total 678,000 shares. It does not follow that each new short was covered that same day. High gross flow and small changes in positions are compatible with many holding-period distributions.

Past return $R^{(5)}_{it}$ covers days $t-5$ through $t-1$, from the close of $t-6$ to the close of $t-1$. The contemporaneous return is $r_{it}$. Daily imbalance is

$$
O_{it}=100\frac{Q^{\mathrm{buy}}_{it}-Q^{\mathrm{sell}}_{it}}{Q^{\mathrm{total}}_{it}},
\qquad O^+_{it}=\max(O_{it},0).
$$

Imbalance and effective spread are in percentage units in the printed regressions. Intraday volatility is the dimensionless range $\sigma_{it}=(H_{it}-L_{it})/H_{it}$, not a standard deviation or annualized volatility. Recent shorting and range are five-day averages. Turnover is shares traded relative to shares outstanding. The lagged positive-imbalance variable is described in Table 3 as applying the positive-part rule to the five-day average imbalance; it is not automatically the average of the five daily positive parts.

An implementation ambiguity concerns turnover. Page 15 says that lagged turnover enters in logarithms, while Table 3 labels and defines the row as average turnover itself; later return regressions also describe turnover without a logarithm. The PDF does not resolve this difference. Replicate both variants and state the chosen transformation instead of pretending the printed specification is uniquely executable.

## Response to recent returns

Table 3 estimates stock and calendar-day fixed-effect regressions separately for the two listing markets. The baseline is

$$
s_{it}=a_i+d_t+\beta R^{(5)}_{it}+u_{it}.
$$

The expanded regression adds contemporaneous return, effective spread, contemporaneous and lagged positive imbalance, lagged shorting, current and lagged intraday range, and lagged turnover. Standard errors cluster in both stock and calendar date, addressing serial dependence within stocks and common shocks across stocks. The return-response sample is January 10–December 30, 2005, with nonpilot stocks and lagged price at least \$5.

The baseline coefficients on five-day returns are 0.371 for NYSE stocks ($t=24.10$) and 0.215 for Nasdaq ($t=26.07$). A 10% prior return therefore corresponds to 0.0371 and 0.0215 increases in the short-selling fraction: 3.71 and 2.15 percentage points. With the full controls, coefficients fall to 0.159 ($t=15.71$) and 0.130 ($t=19.84$), but remain strongly positive. This attenuation is evidence that liquidity-related conditions explain some association, without explaining it all.

Contemporaneous return coefficients are 0.828 and 0.578. Lagged-short-flow coefficients are 0.513 and 0.428, showing substantial persistence. Positive current imbalance is positively associated with shorting in both markets. Current range is also positive, while the spread coefficient is only marginal in the NYSE specification ($t=1.67$) and stronger on Nasdaq ($t=7.96$). The source's broad risk-bearing interpretation should be read with this difference in significance.

Dummy specifications identify past-return quintiles. Relative to the middle quintiles, NYSE losers have 2.1 percentage points less shorting and winners 2.7 more; Nasdaq differences are minus 1.7 and plus 2.2 points. Winner-minus-loser differences are consequently 4.8 and 3.9 percentage points. The pattern is inconsistent with a simple aggregate story of short sellers mechanically intensifying after declines.

Table 4 pools markets and repeats the response regression across stock types. The past-return slope is 0.223 for small stocks versus 0.466 for large stocks; the reported small-minus-large difference is −0.242, with $t=-11.06$, allowing for rounding. Growth versus value, low versus high ownership, and no-put versus put groups all have strong positive slopes, but their differences are not significant. The size result fits easier shorting in large stocks; the paper does not directly observe loan availability for each daily trade.

## Portfolio construction and the gross return evidence

For each market and date $t$, form short-selling quintiles using the nonpilot sample, then construct value-weighted portfolios from stocks whose close on $t-1$ is at least \$5. The ordering matters: the table notes compute the breakpoints before applying the portfolio price filter. The long side is the lowest short-flow quintile and the short side the highest. Portfolios are rebalanced daily.

Skip day $t+1$ and measure the return on day $t+2$, partly to avoid bid–ask bounce and immediate reversal effects in daily close data. For longer horizons, hold cohorts over days $t+2$ through $t+5$ and combine overlapping cohorts using the Jegadeesh–Titman approach. That interval contains four return days. Some later prose and the Table 6 caption call it a five-day holding period, but the explicit day labels and Table 5 identify four invested days. A faithful implementation should use the stated dates and document the inconsistency.

The primary abnormal-return benchmark is one of 25 value-weighted size–book-to-market portfolios. NYSE breakpoints are formed in June 2004 and June 2005, with lagged book equity and prior-December market equity for the book-to-market ratio. All eligible CRSP common stocks are assigned to the resulting portfolios; the benchmarks also impose lagged price at least \$5 and are rebalanced annually. For a stock assigned to benchmark $b(i,t)$, the characteristic-adjusted daily return is $r_{it}-r_{b(i,t),t}$. Value-weight those adjusted returns within each signal portfolio.

Table 5 reports the following daily abnormal returns. All figures are percentage points per day, not cumulative returns over the whole interval:

| Market and return window | Low short flow | High short flow | Low minus high | HAC t-statistic |
|---|---:|---:|---:|---:|
| NYSE, $t+2$ | 0.026 | −0.037 | 0.063 | 2.932 |
| Nasdaq, $t+2$ | 0.022 | −0.042 | 0.064 | 2.521 |
| NYSE, overlapping $t+2$–$t+5$ | 0.028 | −0.014 | 0.042 | 2.264 |
| Nasdaq, overlapping $t+2$–$t+5$ | 0.032 | −0.023 | 0.055 | 2.480 |

The one-day short-flow quintile means decline monotonically from low to high in both markets. In the longer NYSE series, the middle quintiles are not strictly monotonic, although the low-minus-high difference remains positive. Newey–West standard errors use five lags. The reported portfolio period is January 3–December 28, 2005, with subsequent return observations drawn from the available year-end data; implementation needs to handle final cohorts without extending beyond observed prices.

Multiplying the daily long–short results by 22 trading days gives the paper's approximate monthly numbers: 1.386% and 1.408% for the one-day NYSE and Nasdaq strategies, 0.924% and 1.210% for the longer strategies. These are linear monthly equivalents of sample daily averages, not independently estimated monthly returns, and not geometric compounding. Figure 1 plots daily average returns for holding windows of one through four days, with confidence bands; it does not plot cumulative investor wealth.

As a benchmark robustness check, Table 6 estimates daily three-factor and four-factor regressions:

$$
r_{pt}-r_{ft}=\alpha_p+\beta_p(r_{Mt}-r_{ft})+s_pSMB_t+h_pHML_t+m_pUMD_t+\varepsilon_{pt},
$$

omitting $UMD$ in the three-factor version. The daily risk-free rate compounds over the month's trading days to the one-month Treasury bill rate. For the self-financing low-minus-high series, the risk-free terms cancel between legs. Daily four-factor long–short alphas are 0.069% for NYSE and 0.061% for Nasdaq at $t+2$, with t-statistics 3.043 and 2.601. For the longer overlapping strategy they are 0.045% and 0.050%, with t-statistics 2.366 and 2.721. Corresponding three-factor alphas are 0.065/0.060% for one day and 0.042/0.049% for the longer window. Predictability therefore does not depend solely on the characteristic benchmark.

## Subsamples and predictive regressions

Table 7 intersects short-flow quintiles with size and book-to-market terciles, institutional-ownership groups, and put availability. Market capitalization uses prior-month values and NYSE breakpoints; ownership groups use previous-quarter fractions at or below 33% and above 67%. The low-minus-high daily adjusted returns are 0.053% for small stocks ($t=2.800$), 0.062% for large ($t=1.763$), 0.068% for growth ($t=2.068$), 0.058% for value ($t=2.186$), 0.038% for low ownership ($t=0.966$), and 0.066% for high ownership ($t=2.326$). No-put and put stocks produce 0.056% ($t=1.964$) and 0.064% ($t=2.453$).

The adjoining prose says the magnitude is greater for small than large stocks, but the printed table shows the opposite. The significance is stronger for small stocks, which is a different statement. This note follows the table and does not infer a monotonic size effect in achievable profits. Similarly, the no-put t-statistic is borderline at conventional two-sided 5% thresholds, so “all except two groups are significant” should not be treated as a precise finite-sample testing statement.

Table 8 predicts the individual stock return on day $t+2$ from date-$t$ short flow and other controls:

$$
100r_{i,t+2}=a_i+d_t+b\,s_{it}+cR^{(5)}_{it}+\gamma^\top Z_{it}+e_{i,t+2}.
$$

Here the left side is percent return; $Z$ contains the selected spread, positive imbalance, range, and turnover controls. Stock and day fixed effects remain, with standard errors clustered by both dimensions. The regression table is headed daily returns, not the characteristic-adjusted portfolio return. The fixed effects and controls supply its conditional comparison; one should not substitute portfolio abnormal returns as its dependent variable without changing the test.

The baseline short-flow coefficients are −0.427 for NYSE ($t=-6.75$) and −0.325 for Nasdaq ($t=-8.28$). A 0.10 increase in the short-flow fraction predicts −0.0427 and −0.0325 percentage points on day $t+2$, or −4.27 and −3.25 basis points. The paper's monthly equivalents are approximately −0.94% and −0.72%. With prior returns and all liquidity controls, coefficients remain −0.342 ($t=-5.26$) and −0.229 ($t=-5.87$). Positive imbalance independently predicts lower future returns; range does not significantly predict returns in the full specifications.

The nonlinear specifications replace continuous flow and past return with extreme-quintile dummies. Low-flow coefficients are 0.083 and 0.108 percentage points, while high-flow coefficients are −0.071 and −0.043. The implied low-minus-high differences are 0.154 and 0.151 percentage points. The prose calls these positive differences “high minus low”; the table's signs establish that low minus high is the consistent orientation. These conditional dummy differences are not the same estimates as the value-weighted portfolio returns.

The source also reports similar conclusions from regressions that replace stock fixed effects with lagged market capitalization, book-to-market, and longer-horizon momentum, and from Fama–MacBeth regressions with HAC inference. It does not supply the full additional coefficient tables. Those statements are robustness reports, not results independently reconstructable from the PDF alone.

## Residual short flow and the test of liquidity provision

The authors attempt to remove the part of short selling associated with contemporaneous buying pressure. For each stock, they regress short flow on positive imbalance, then use

$$
e^{\mathrm{short}}_{it}=s_{it}-\widehat\alpha_i-\widehat\beta_iO^+_{it}
$$

as the predictor in the return regressions. Equations (4)–(5) and Table 9 print the estimation index as $t=1,\ldots,-22$, which is not a valid ordered sample definition. The intended rolling-window interpretation appears to be 22 preceding trading days. A transparent reconstruction would estimate on $u=t-22,\ldots,t-1$ and evaluate the residual on day $t$, but that is an implementation assumption, not a verified correction to author code. Including day $t$, using available early-year histories, or imposing a minimum-observation rule could change the result. The PDF does not resolve these details.

The economic attribution is deliberately aggressive: every component correlated with imbalance is treated as liquidity provision. It can also remove informed passive trades and the mechanical effect of the historical uptick rule. Hence the residual is not a pure observed measure of private information, and the fitted component is not proof of an uninformed liquidity strategy.

Table 9's baseline residual-flow coefficient is −0.226 for NYSE ($t=-3.13$) and −0.225 for Nasdaq ($t=-5.14$). With full controls it is −0.147 ($t=-2.01$) and −0.158 ($t=-3.65$). Negative predictive content survives this orthogonalization, although it is weaker. The source's prose says the high-residual-flow dummy is insignificant in both markets; the table actually gives −0.042 with $t=-2.64$ for NYSE and −0.015 with $t=-0.89$ for Nasdaq. The table supports non-significance only in the latter case. The reported low-versus-high F-tests are not tabulated.

Section 8 then checks a sharper implication of mechanical liquidity provision. If short sellers mainly absorb a temporary buying-pressure shock, high current shorting should precede subsiding buying pressure. Table 10 instead predicts higher future signed imbalance. The coefficient on current short flow in the $O_{i,t+2}$ regression is 12.700 for NYSE ($t=19.54$) and 3.917 for Nasdaq ($t=6.66$). After adding current imbalance it remains 9.881 ($t=13.85$) and 2.495 ($t=4.34$). For example, a ten-percentage-point increase in the short-flow fraction predicts 0.9881 percentage points more NYSE imbalance in the controlled regression.

The table also splits future imbalance into a nonnegative buy component and the absolute magnitude of negative imbalance. The negative coefficients for the latter must be read as less sell-side imbalance magnitude, not as a negative signed imbalance prediction. These results weaken the particular explanation that predictable price declines arise mechanically because buying pressure disappears. They do not imply that short sellers never supply liquidity, nor exclude pressure dynamics occurring at other horizons.

## Execution costs and what the evidence can support

The paper's own transaction-cost calculation is unfavorable to a naive implementation. It assumes effective half-spreads around 30 basis points, 20% turnover in each of the two legs daily, and 22 trading days monthly. The stated monthly turnover is $0.20\times2\times22=8.8$, giving $0.003\times8.8=0.0264$, approximately 2.7% execution cost per month before commissions. This is an illustrative turnover convention, not a reconstruction from actual portfolio trades. The source labels it a five-day strategy despite the four-day invested window discussed earlier; retain the explicit assumptions when reproducing the arithmetic.

Borrowing costs are cited at 3.98% annually, about 0.326% monthly, from a different study of below-median-size stocks. The authors say this likely overstates average borrowing costs for their value-weighted, broader portfolios. The number is not an estimate from matched loans for the strategy's actual short positions. Financing, recalls, locate availability, price-test constraints, market impact, and partial fills are not modeled in a complete net-return backtest.

Passive orders might reduce paid spreads, but their fills and adverse selection would differ from the reported close-to-close portfolio returns. A researcher cannot subtract a lower assumed fee while keeping all positions and entry prices unchanged. More decisively, page 30 states that short-sale data were not available at a frequency permitting the reported strategy to be traded. The one-day skip is a statistical design choice, not evidence that the aggregate signal was public before entry. Any live study requires actual release timestamps or a different contemporaneously available feed.

Other limitations include the single-year sample, the absence of trader-level motives and covering trades, and conditioning on executed short sales rather than unmet demand to short. The results say little about stocks where borrowing constraints prevented a trade from appearing at all. High gross short-sale volume does not establish that constraints are unimportant for every security. The descriptive growth-stock pattern is also not uniform: Table 1 reports Nasdaq high-book-to-market shorting above low-book-to-market shorting, despite the general prose emphasizing growth stocks.

For replication, the decisive sequence is to validate venue coverage and the daily denominator, preserve information timing, reconstruct the one-day skip and overlapping portfolios, reproduce both benchmark approaches, implement two-way clustered panel inference, and explicitly choose the unresolved turnover and residual-window conventions. Report gross predictive returns separately from the cost model. The paper supplies strong evidence that 2005 executed short flow contains short-horizon information, but it does not supply a frictionless, publicly tradeable 1.4%-per-month strategy.

All 33 source pages, including references, were read. Visual checks covered the title, all ten tables, Figure 1, the position-accounting equation, factor specifications, rolling-residual equation, and transaction-cost calculation. The table-versus-prose discrepancies above were checked against the rendered original pages; they are source qualifications, not official author errata.
