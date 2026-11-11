# Limited Arbitrage in Equity Markets

**Mark Mitchell, Todd Pulvino, and Erik Stafford (2002).** *The Journal of Finance* 57(2), April, 551–584. Source: [Arbitrage_MitchellPulvinoStafford_2002.pdf](../../Finance/Arbitrage_MitchellPulvinoStafford_2002.pdf). All thirty-four pages, eight tables, two figures, footnotes, and references were inspected. Page references below use journal pagination. The local file `Arbitrage_Mitchell_2007.pdf` is an April 2001 working-paper version of this work despite its filename; it is not a separate unsummarized study.

## Why this matters and the contribution

A parent company can trade for less than the market value of its publicly traded subsidiary stake. Buying the parent and shorting the corresponding subsidiary shares seems to acquire the parent's remaining business for a negative price. The relevant implementation question is whether an investor can finance that position, maintain the borrow, and survive until the apparent discrepancy disappears.

The paper studies 82 parent/subsidiary situations during 1985–2000 and separates four obstacles: termination without convergence, uncertainty about the investment horizon, margin-driven liquidation along the path, and stock-borrow frictions. It also examines whether investors have enough observations to learn the return distribution in the first place. The innovation is a transaction-level and calendar-time accounting of these mechanisms, rather than an assertion that the observed price ratio represents riskless profit.

The broad results are that roughly 30% of completed situations fail to converge under the relevant definition, maintenance margin can sharply reduce realized returns, and capital reserved to avoid liquidation lowers returns substantially. Diversification mitigates several risks but does not eliminate financing shocks. News that resolves uncertainty about distributions generates large immediate gains even without an observed change in borrowing conditions. The authors emphasize imperfect information and learning costs as an important explanation for persistent apparent mispricing.

## Defining the stub and constructing the sample

Let $M_P$ be parent equity market value, $M_S$ the market value of the subsidiary stake actually owned by the parent, and $A_O-L_P$ the market value of other parent assets less unconsolidated parent liabilities. The economic stub is

$$
V_{\mathrm{stub}}=M_P-M_S-(A_O-L_P).
$$

The last term is difficult to measure. Rule 1 assumes it is zero and identifies a negative stub if

$$
Q_1=M_S/M_P>1.
$$

Rule 2 substitutes the parent's **unconsolidated book equity**, denoted $B_P$, for that net value and identifies a negative stub if

$$
Q_2=(M_S+B_P)/M_P>1.
$$

Consolidated parent book equity would not implement the stated adjustment. Neither rule captures all off-balance-sheet liabilities or guarantees that book values approximate market values. Tobacco liabilities at Nabisco are an example of omitted economic obligations. Tax liabilities from a distribution can also matter. The paper describes historical tax-treatment considerations but does not estimate every contingent liability.

Sample construction has two stages. First, search SDC for 1985–2000 IPOs where another publicly traded firm owned shares before the offering. Track each pair's ratios from the IPO through December 2000. Second, search the financial press and trade publications for additional extreme relative-value situations during the same period. Include pairs whose ratios exceed one at any point under either rule.

Prices come from CRSP before 2000 and Datastream during 2000. Parent shares outstanding and subsidiary shares owned by the parent come from quarterly company filings. When the reported quantity changes by at least 10%, the authors search news sources for the exact effective date. This hand collection matters because a small error in cross-holdings can create a spurious negative stub or an incorrect hedge ratio.

The result is 70 pairs under Rule 1 and 82 under Rule 2. “Subsidiary” is a convenient label even when the parent owns less than half the voting stock. Table I classifies Rule 1 situations by industry and first negative-stub year. Technology and Internet cases are concentrated late in the sample, but the phenomenon is not confined to the Internet bubble.

The source does not publish a complete machine-readable pair list, filing-vintage archive, or press-search query. It also does not give a fully specified reporting-lag convention for every accounting input or small share-count change. A modern reconstruction should preserve information-availability dates separately from economic effective dates; using later-discovered holdings as if contemporaneously known would introduce look-ahead.

## Signals, positions, and exit events

For either $Q_1$ or $Q_2$, initiate when the ratio exceeds a buy threshold and exit when it falls below the corresponding sell threshold. The tested buy/sell combinations are $1.0/0.8$, $1.25/1.0$, and $1.5/1.0$. The lower exit threshold creates a holding band rather than forcing liquidation at every crossing back through the entry level. Corporate events that terminate the parent/subsidiary link also close the position.

If the parent owns $N_S^{\mathrm{held}}$ subsidiary shares and has $N_P$ shares outstanding, the share hedge ratio is

$$
h=N_S^{\mathrm{held}}/N_P.
$$

Buy one parent share and short $h$ subsidiary shares. This removes the indirect subsidiary share exposure embedded in that parent share, leaving exposure to the residual parent business and to events affecting the link. It is not a generic equal-dollar long-short position. The hedge ratio changes when ownership or outstanding shares change; a faithful reconstruction must process corporate actions as well as prices.

The calendar-time strategy enters at the market close on the threshold day and remains invested through the close on the resolution day. The paper does not impose a next-day execution lag. That is the reported convention; an implementable replication should separately examine whether prices and filings used to trigger the trade were available before the assumed fill. The paper's close-based accounting does not establish executable volume at every closing price.

A parent/subsidiary pair can generate multiple trades when the ratio repeatedly crosses the thresholds. Consequently, the 70 or 82 *situations* are different units from the 110–130 or other counts of *investments* in the holding-period tables. Convergence also has table-specific definitions: Table II classifies whether mispricing is eliminated at situation termination, whereas Table III calls an investment converged when its ratio is lower at termination than at entry. Those samples should not be interchanged.

## Capital, leverage, and daily balance-sheet accounting

The study reports returns on capital committed, not profit divided by a negative or near-zero net purchase price. Its example buys a parent share at \$26.25 and shorts 0.7154 subsidiary shares at \$48. Initial equity at 50% of both gross legs is

$$
E_0=0.5(26.25+0.7154\times48)=30.2946.
$$

The short proceeds are collateral, not freely available profit that makes the trade capital-free. The full strategy marks long positions, short liabilities, cash, collateral proceeds, and margin loans daily. In schematic accounting notation,

$$
E_t=L_t+C_t+S_t^{\mathrm{collateral}}-H_t-D_t,
$$

where $L_t$ is long market value, $H_t$ is the current short liability, $C_t$ is additional cash, and $D_t$ is margin borrowing. Short collateral is distinct from the changing liability to repurchase the stock. Daily equity changes include price gains, financing, distributions, trading costs, and corporate-action cash flows.

The three leverage designs answer different questions:

- **Textbook leverage:** initial equity equals 50% of long plus short market values, but subsequent maintenance-margin requirements are ignored.
- **Regulation T leverage:** the same initial capital, with maintenance equity of 25% of long value and 30% of short value under the historical exchange/self-regulatory rules used in the paper. Margin calls are met by partial liquidation, not external capital injections.
- **Conservative leverage:** choose enough initial capital that no trade in the relevant full-sample strategy ever receives a margin call. This is explicitly an ex post construction and cannot be selected by a real investor with only prior information.

The historical short-stock maintenance exceptions are 100% of market value for prices from \$2.50 to \$5.00 and \$2.50 per shorted share below \$2.50. Brokers can require more than the minimums. These are the paper's historical simulation rules, not a statement of current brokerage requirements.

Absent low-price exceptions, a useful reconstruction of the maintenance test is $E_t\ge0.25L_t+0.30H_t$. If it fails, reduce exposure until the requirement is restored, charging trading costs as positions are closed. For the portfolio simulation the authors liquidate selected positions randomly. They do not publish a random seed or complete selection algorithm. Footnote 18 states that a fortunate liquidation choice preserved Creative Computers/Ubid just before a 46.2% portfolio rebound. This makes the exact realized simulation path sensitive to an undocumented input.

The model counts reserve capital from the outset. Allowing new collateral only after adverse price moves, without including that available capital in the denominator when no call occurs, would overstate returns. Conversely, forced liquidation can sometimes prevent further losses; its effect is path dependent rather than mechanically negative in every deal.

## Return measurement, financing conventions, and benchmarks

For individual trades, short holding periods are not naively compounded into extraordinary annual rates. If a trade ends within a year, proceeds are assumed reinvested risk-free for the remaining part of a one-year horizon. Longer holding periods are annualized. Table IV reports annualized holding-period returns *in excess of the comparable risk-free holding-period return*. Its caption assumes the risk-free rate on short proceeds.

The calendar-time portfolio uses a different short-rebate assumption: 3% per year. Extra cash earns the risk-free rate, margin borrowing costs the risk-free rate plus 50 basis points, and direct trading costs are \$0.05 per share in the 1980s and \$0.04 thereafter. Monthly returns compound daily portfolio returns. The Creative Computers/Ubid worked example separately assumes no interest on collateral or short proceeds. There is an internal ambiguity: although Table IV's caption specifies a risk-free short rebate, footnote 14 on p. 567 says subsequent full-sample analyses use 3%. The calendar-time convention is clear; exact replication of the individual-trade table should test both rebates or obtain clarification rather than silently resolve the conflict. The worked example's zero-interest convention remains separate.

At entry, no more than 20% of portfolio equity is assigned to one deal. This can leave substantial cash when few opportunities exist. It is an *initial allocation* limit, not a rule that continuously rebalances every position back to 20%. Rebalance only for threshold entries/exits, terminating events, and margin calls. Footnote 17 says 20% was initially chosen as reasonable and subsequently happened to maximize full-sample portfolio returns; this is not an out-of-sample validation of that choice.

Performance regressions use monthly excess returns and the Fama–French market, size, and value factors:

$$
R_{p,t}-R_{f,t}=\alpha+\beta_M(R_{M,t}-R_{f,t})
+s\,SMB_t+h\,HML_t+u_t.
$$

The paper reports coefficients and $t$ statistics but does not specify a HAC lag selection or a multiple-testing correction for the six rule/threshold strategies. Alpha annualization in Table V is arithmetic, $12\alpha$, not a compounded annual return. Months available differ across Rule 1 strategies; reproduce the table's reported observation counts rather than assuming every row uses all 192 months.

## Fundamental risk and uncertain duration

At December 31, 2000, 66 of the 70 Rule 1 situations had terminated. Mispricing was eliminated in 48 and not eliminated in 18: failure frequency 27.3%. For Rule 2, 77 of 82 had terminated, with 50 eliminations and 27 failures: 35.1%. The remaining four and five are unresolved, not successful trades. The common “30%” summary approximates these completed-situation results.

Table II's Rule 1 breakdown includes 12 successful distributions and 15 cases where price changes alone remove the discrepancy. Acquisitions account for 14 of the 18 adverse terminations; parent delistings account for the other four. A parent can pledge subsidiary shares against debt and subsequently fail, leaving creditors rather than the parent shareholders with the apparent asset backing. The economic link on which the hedge depends is therefore contingent.

Cordant/Howmet illustrates acquisition risk. Cordant owned 84.6 million Howmet shares and had 36.7 million own shares, implying roughly 2.31 Howmet shares per parent share. On November 12, 1999, Cordant's offer for minority Howmet shares drove Howmet up \$3.69 while Cordant rose only \$0.63. The hedged position lost about 25% in one day under the paper's initial-capital convention. Subsequent events could reverse losses, but continuing to hold required resources and information unavailable from a simple negative-stub identity.

For Rule 1 with thresholds $1.0/0.8$, Table III reports 110 investments, mean duration **236.3 trading days**, median 92, interquartile range 29–274, and range 1–2,796. Restricting to 79 converged investments reduces the mean to 176.5 and median to 74. Rule 2's baseline has 130 investments, mean 309.7, median 155.5, and maximum 2,818 trading days.

The horizon itself is a risk input. The paper illustrates that a fixed 15% holding-period gain becomes an annualized return of about 47% over 92 trading days, 238% over 29 days, or 14% over 274 days. These numbers approximately use a 252-trading-day year. They explain sensitivity to duration; the one-year reinvestment convention prevents those explosive short-trade annualizations from dominating the reported mean. Even among eventually converged investments, risk-free investing would have done better in roughly 10% under Rule 1 and nearly 25% under Rule 2.

## Margin risk in the case study and full sample

Creative Computers carved out 20% of Ubid on December 4, 1998 and announced an intended distribution of the remainder after at least six months. To allow for initial shorting difficulty, the worked example starts on December 9. The hedge shorts about 0.72 Ubid shares per parent share. The apparent stub was then about negative \$28 million, with an anticipated six-month return around 45% under initial-margin leverage.

Instead, the spread widened abruptly. Reported equity losses were 26% through December 18 and then 84%, 91%, and 63% on the next three trading days, with repeated margin calls. The stub reached about negative \$766 million. Although the remaining position subsequently returned roughly 150% as the shares converged to the June 7, 1999 distribution, the full leveraged investment lost about 99%. Figure 1 shows both the price divergence and the sequence of liquidation dates.

The text on p. 567 once calls the pre-convergence December date “1999”; the figure and surrounding chronology make **December 1998** the consistent date. The paper estimates that reserving \$4.53 extra cash per \$1 of long position would have avoided the calls, earning 8.7% over the investment instead of the 45.9% available in the no-maintenance counterfactual. That comparison prices insurance against the path through the return denominator.

Table IV's central full-sample results are:

| Rule 1 buy/sell | Investments | Textbook mean excess return | Maintenance-margin mean | Conservative mean | Margin-call frequency under maintenance |
|---|---:|---:|---:|---:|---:|
| 1.00/0.80 | 110 | 18.5% | 12.7% | 2.6% | 23.6% |
| 1.25/1.00 | 75 | 21.6% | 13.8% | 2.8% | 26.7% |
| 1.50/1.00 | 39 | 24.2% | 10.1% | 4.0% | 38.5% |

These are annualized individual-investment excess returns, not monthly alphas. At the baseline threshold, ignoring maintenance raises the mean from 12.7% to 18.5%, approximately 46% relative to the maintenance result. The roughly 50% headline is therefore a comparative return increase, not a 50-percentage-point alpha.

In the baseline converged-only sample, textbook, maintenance, and conservative mean excess returns are 28.6%, 23.1%, and 8.2%. Even with convergence known ex post, 11.4% of maintenance-margin investments underperform the risk-free comparison, and 16.5% receive margin calls. This isolates path and horizon risk from eventual nonconvergence, but the converged-only sample is a hindsight diagnostic, not a tradable selection rule.

The table includes minimum excess returns around −104%. Such figures do not, by themselves, establish negative net asset value: a total return of −100% minus a 4.1% risk-free return is an excess return of −104.1%. Do not truncate excess returns at −100% or infer an insolvency convention from those minima. Figure 2 separately and explicitly allows negative equity in its no-maintenance counterfactual; that convention should not be generalized to every individual-trade calculation.

## Calendar-time results and diversification

Table V reports the following monthly alphas in percentage points:

| Rule | Buy/sell | Alpha | t statistic | Months | Arithmetic annualized alpha |
|---|---|---:|---:|---:|---:|
| 1 | 1.00/0.80 | 0.825 | 1.60 | 186 | 9.9% |
| 1 | 1.25/1.00 | 1.241 | 2.17 | 172 | 14.9% |
| 1 | 1.50/1.00 | 0.514 | 0.78 | 168 | 6.2% |
| 2 | 1.00/0.80 | 0.021 | 0.06 | 192 | 0.2% |
| 2 | 1.25/1.00 | 0.745 | 1.54 | 192 | 8.9% |
| 2 | 1.50/1.00 | 0.391 | 0.61 | 192 | 4.7% |

Only the Rule 1 $1.25/1.0$ result is conventionally significant on its reported individual $t$ statistic. Its market coefficient is −0.173 ($t=-1.18$), size coefficient −0.137 ($t=-0.78$), and value coefficient 0.264 ($t=1.19$); adjusted $R^2$ is 0.052. The low factor explanatory power and noisy alpha estimates do not establish a universal risk-free anomaly.

Figure 2 is explicitly the **no-maintenance-margin** path, allowing equity to become negative. It is not the investable constrained portfolio plotted without qualification. The ending value is \$16.9 per initial dollar without maintenance requirements versus \$9.8 with them. A later episode in which 11 of 15 spreads widened together shows why holding several related trades need not eliminate financing risk.

Table VI's 1986–2000 pure-strategy annual returns average 22.0%, with 24.8% annualized volatility and Sharpe ratio 0.676. The market comparison is 14.4%, 15.4%, and 0.592; merger arbitrage is 10.5%, 5.8%, and 0.914. The pure strategy loses 14.2% in 1998 and gains 77.4% in 2000, illustrating substantial variation hidden by the mean.

The maximum **in-sample** Sharpe combination assigns 41% to stub trades and 59% to the market, producing mean 17.5%, volatility 12.3%, and Sharpe 0.992. Combining 15% stub trades with 85% merger arbitrage produces 12.3%, 6.0%, and 1.163. These weights are selected using the full sample. The source compounds monthly returns into annual returns and annualizes monthly volatility by $\sqrt{12}$; it does not use the cross-year standard deviation of the fifteen annual observations as its volatility estimator.

The hybrids treat strategies as separate funds. Allowing collateral sharing could further change liquidation behavior, but that benefit is an argument in the discussion rather than a fully specified and tested cross-margin simulation.

## Borrow costs, buy-ins, and news about resolution

Ameritrade loan data cover December 1998–October 2000. They reflect rates received by institutions borrowing the broker's shares, and may overrepresent hard-to-borrow securities because easy shares could be sourced internally elsewhere. Under Rule 1 at threshold one, 24 of 28 relevant firms appear in the data; six of those 24 have negative rebates and three experience partial buy-ins. Thus 25% and 12.5% refer to covered firms in this limited interval, not the entire 1985–2000 sample.

Table VII's most negative observed annual rebates are −40% for Stratos Lightwave and −30% for Palm. Across the listed firms, the median minimum rebate is 1% and mean −1.5%. Excluding the two extremes leaves minima ranging from −8% to 6%. A negative rebate charges the short seller interest rather than paying it.

For Methode/Stratos, the paper's July–December 2000 example earns 21.1% before the −40% annual rebate and approximately −0.6% after it. The important mechanism is rate multiplied by an uncertain holding period. A seemingly prohibitive annual borrow cost may be acceptable if convergence occurs quickly, while a moderate cost can exhaust a small spread over a long horizon. Buy-in risk is different: the position can be closed irrespective of willingness to pay the rate, and availability shocks may coincide across trades.

The event study collects announcements from the *Wall Street Journal* and Dow Jones News Retrieval about intended distributions, dates, and IRS approval of tax-free treatment. Three-day windows surround the news. Mean tests use standard errors of the mean; median tests use Wilcoxon signed ranks.

For 16 parent/subsidiary pairs, aggregating each pair's announcements, the net long-short mean return is 8.29% ($t=3.25$), median 9.39% ($p=0.0097$). Parent and subsidiary mean reactions are 6.17% and −2.25%. For nine firms already announcing distribution intent in the prospectus, the net mean is 8.71% ($t=2.03$), showing that later resolution news matters even when a distribution was previously contemplated.

Treating announcements separately yields 25 net-position observations, mean 5.30% ($t=3.11$), and median 3.31% ($p=0.0021$); subsidiary returns are available for 24. Among six announcements with Rule 1 still indicating a negative stub, net mean return is 11.37% ($t=2.29$), and the median ratio falls from 1.11 to 1.01. The small samples and repeated events limit precision. The source does not fully spell out the within-pair aggregation and every net-position capital normalization needed to independently reproduce all event-study entries.

## Reproduction priorities and limits of the evidence

A replication should first reconstruct the ownership ledger, separate the two mispricing rules, and label all termination events before calculating returns. Implement the three threshold pairs and distinguish unique situations from repeated investments. Build a daily self-financing balance sheet with explicit collateral, interest, distributions, fees, margin calls, and short-borrow availability. Reproduce individual-trade and portfolio financing conventions separately. Preserve the reported same-close timing as one specification and test a lagged executable version as a separately labeled extension.

The essential missing inputs are the full hand-collected holdings/event dataset, detailed filing availability conventions, exact partial-liquidation and random selection rules, seeds, daily interest day-count choices, and complete treatment of corporate-action edge cases. Bid-ask spread and market-impact costs are not separately calibrated; the stated per-share costs should not be assumed to capture them for illiquid carve-outs. The limited loan-data interval cannot supply historical borrow rates or availability for every trade.

The paper compares several rules and thresholds without a held-out validation period. Conservative leverage, converged-only samples, and optimal hybrid weights use future information intentionally as diagnostics. They should not be presented as ex ante investment policies. Estimated alpha is imprecise in five of six strategies, and the study does not prove that all negative stubs are irrational once hidden liabilities are valued.

The result is nevertheless a concrete account of why price discrepancies can persist. A correct directional valuation does not supply a convergence date, a guarantee of the corporate link, or financing through interim losses. Reimplementation requires modeling those contractual and balance-sheet details with the same care as the spread itself.
