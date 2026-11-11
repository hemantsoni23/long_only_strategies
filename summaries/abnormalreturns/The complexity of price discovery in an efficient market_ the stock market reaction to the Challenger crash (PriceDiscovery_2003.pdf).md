# The complexity of price discovery in an efficient market: the stock market reaction to the Challenger crash

**Michael T. Maloney and J. Harold Mulherin.** *Journal of Corporate Finance* 9 (2003), pp. 453–479. DOI: 10.1016/S0929-1199(02)00055-X. Source: [PriceDiscovery_2003.pdf](../../Finance/PriceDiscovery_2003.pdf). All 27 pages, including the news chronology in Appendix A and references, were read. Printed page numbers below correspond to PDF page number plus 452.

## Why this matters

The Challenger disaster created a public event with a precisely known time but an uncertain cause. Four major contractors faced possible losses, and the official inquiry took months to establish the mechanical failure. The stock market differentiated Morton Thiokol, the solid-rocket-booster supplier, from the other contractors much sooner. This case lets the authors study not merely whether prices react to news, but how a market combines public observations with dispersed technical knowledge.

The contribution is a detailed event study linking daily prices and volume, intraday transactions, a firm-specific trading halt, potential informed-trading profits, and inferred liquidity provision. Its central result is that rapid and apparently accurate relative valuation can occur without a readily identifiable informed trader or a large measurable trading windfall. Much of the inference develops while the most affected stock is halted and related firms continue trading.

The study does **not** observe the information sets of individual traders or prove that a particular trade identified the faulty O-rings. It establishes price patterns consistent with early recognition of firm-specific culpability, then investigates possible mechanisms without resolving them. That boundary is essential: the familiar claim that “the market solved the crash immediately” compresses a much more qualified empirical argument.

## Event, firms, and information chronology

The four firms are Morton Thiokol, which supplied the solid-fuel boosters; Rockwell International, which built the shuttle and its main engines; Martin Marietta, which manufactured the external fuel tank; and Lockheed, which managed ground support. They form a narrowly chosen set of firms exposed to the same event. The three firms later judged not responsible serve as internal comparisons, although their business exposures and capital structures are not identical.

The key times on **January 28, 1986**, are Eastern Standard Time:

| Time | Event used in the analysis |
|---|---|
| 11:39 a.m. | Challenger explodes |
| 11:47 a.m. | Dow Jones News Wire/Broad Tape reports the explosion |
| 11:52 a.m. | NYSE trading in Morton Thiokol is halted after selling pressure |
| 12:17 p.m. | Lockheed's no-comment response appears on the wire |
| 12:36 p.m. | A 50,000-share Morton Thiokol trade occurs on Nasdaq at \$35 |
| 12:44 p.m. | Morton Thiokol resumes on NYSE with a 200,000-share call auction at \$35 |
| 12:52 p.m. | Rockwell's no-comment response appears on the wire |

The Nasdaq trade and NYSE reopening are distinct events. Treating 12:36 as the NYSE reopening would misalign the paper's liquidity window. The latter runs from the crash at 11:39 through the NYSE resumption at 12:44, encompassing 13 minutes before the formal halt as well as the halt itself.

Appendix A traces how the public explanation developed. News reports discussed possible booster problems in late January, Morton Thiokol faced closer scrutiny by February 3, and cold-weather concerns appeared by February 6–7. Richard Feynman's demonstration of the O-ring material's poor resilience in cold conditions occurred on February 11. The Rogers Commission's report on June 9 identified failure of the seals in a joint of the right solid rocket motor and also criticized decision-making within NASA and Thiokol. Thus the source does not support a literal claim that no public clue existed until June; its comparison is between immediate market differentiation and the much slower investigation and formal conclusion.

The relevant technical knowledge also predates the crash. The paper describes NASA concerns dating to 1982, a July 1985 analyst warning, an October 1985 engineering-conference appeal by Thiokol for help with O-rings, and engineers' recommendation on launch morning to postpone because of the cold. Those facts were not widely incorporated into public securities analysis. The disaster could make previously scattered knowledge newly informative without that knowledge having predicted with certainty that this launch would fail.

## Empirical design and data

Daily returns and trading volume come from the **S&P Daily Stock Price Record**. The estimation window is **October 28, 1985–January 27, 1986**, described as the three months before the event. Intraday transaction observations come from **Francis Emory Fitch price sheets**. News-wire and press records establish the timeline, while the **Invest/Net Insider Trading Monitor**, accessed through Dialog, is used to search reported insider transactions. Value Line, Moody's, broker commentary, and later news reports support business-exposure and loss comparisons.

For daily variable $z$—either return or volume—the Table 1 comparison can be reconstructed as

$$
Z_i=\frac{z_{i,\mathrm{event}}-\bar z_{i,\mathrm{pre}}}{s_{i,\mathrm{pre}}}.
$$

The return table prints positive magnitudes for negative return deviations. A signed calculation would be negative. This is a descriptive standardized deviation relative to pre-event daily variability, not the usual standard error of a sample mean, and not a multivariate factor-model abnormal return. The paper does not supply the exact daily vectors, standard-deviation divisor, or an event-induced-variance correction.

The authors argue that the exogenous, sharply timed crash avoids much of the event-date ambiguity and endogenous announcement selection common in corporate studies. The narrow intraday window also reduces sensitivity to an asset-pricing benchmark. These advantages do not eliminate all identification problems: a single event has no randomized counterfactual, the comparison firms have different exposures, and aggregate market news may still affect longer holding periods.

For implementation, preserve exchange identifiers, timestamps, trade sizes, transaction prices, and any corrections to reported order. The paper sometimes analyzes NYSE-only trades and sometimes uses a Nasdaq transaction to describe price discovery. Those populations must not be merged silently. It provides tables and figures rather than the complete transaction file or executable code, so exact reconstruction requires obtaining the cited historical records.

## Daily reaction: one firm stands apart

Table 1, printed p. 456, reports:

| Firm | Event-day return | Prior daily mean | Prior daily standard deviation | Absolute return $Z$ | Event volume, thousand shares | Prior mean volume, thousand shares | Volume $Z$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Morton Thiokol | −11.86% | 0.21% | 1.86% | 6.49 | 1,739.9 | 100.5 | 27.57 |
| Lockheed | −2.14% | 0.07% | 1.36% | 1.63 | 667.5 | 347.9 | 2.00 |
| Martin Marietta | −3.25% | 0.14% | 1.79% | 1.89 | 446.2 | 199.9 | 1.80 |
| Rockwell | −2.48% | 0.06% | 1.79% | 1.42 | 563.2 | 221.2 | 2.92 |

Thiokol's return deviation is roughly six and a half pre-event standard deviations, while the other three are below two. Its volume is over 17 times the prior daily mean. The volume standard deviations underlying the final column are respectively 59.5, 159.4, 136.5, and 117.1 thousand shares. These observations establish an unusually large relative reaction for Thiokol; they do not by themselves identify the exact information that caused it.

The intraday evidence adds timing. Table 2's 11:30-to-noon returns for Lockheed, Martin Marietta, and Rockwell are −5.82%, −3.18%, and −5.76%; Thiokol has no noon price because it is halted. At 12:36, its \$35 trade is about 6.04% below the table's 11:30 price of \$37.25. By 1:00 p.m., the reported price is \$34.38. The other firms initially fall and then recover substantially, whereas Thiokol continues declining.

Different passages use different reference prices. Table 4's pre-crash-to-minimum declines are −5.05% for Lockheed, −8.51% for Martin Marietta, and −6.12% for Rockwell, with minima at \$44.625, \$32.250, and \$32.625. Those are not the same intervals or prices as Table 2's 11:30/noon snapshots. The prose around Table 2 blends some of these numbers, so a replication should use each table's explicit timestamps and price definitions rather than combine the percentages.

Figure 1 normalizes intraday prices to the opening price on January 28. Figure 2 normalizes later closing prices to January 27 and plots the Dow Jones index alongside the four firms. The latter figure extends through late March and shows Thiokol's relative loss persisting while the other firms track or outperform the market. Although its caption says three-month movements, the plotted post-event span is roughly two months. The evidence is persistence over that displayed interval, not a formal permanent-impact estimate over all future time.

## Was the size of the loss economically plausible?

Thiokol's approximately 12% decline represents about **\$200 million** in equity value. The authors ask whether its larger NASA exposure alone could explain why it fell more. NASA sales shares are reported as 18.23% for Thiokol, 8.53% for Lockheed, 10.95% for Martin Marietta, and 11.86% for Rockwell. They argue that a common program-delay shock proportional to those exposures would suggest a Thiokol decline around 4.5%, not 12%.

This is a rough proportional-exposure comparison, not a fitted cash-flow valuation model. Revenue shares do not automatically translate one-for-one into equity sensitivities: margins, operating leverage, debt, contract terms, and future opportunities can differ. It weakens a simple common-delay explanation but does not mathematically exclude every such explanation.

The ex post accounting of firm-specific losses is more direct. The paper lists approximately \$7 million in settlements, \$10 million in forfeited retainers, and \$409 million of repair/redesign work performed without profit. Applying an assumed 10% margin gives about \$40 million in forgone profit on that work. Withdrawal from bidding for a \$1.5 billion next-generation booster contract is assigned another \$150 million of potential lost profit. The total is roughly \$207 million, close to the event-day equity loss.

The \$150 million figure is undiscounted and treats a forgone opportunity using a simple margin assumption; the source explicitly acknowledges its rough nature. It does not estimate the probability of winning the contract absent the crash, the timing of cash flows, taxes, or discount rates. The match supports the plausibility of a reputational/future-business component. It is not an exact demonstration that investors forecast every later expense correctly on January 28.

## Search for informed traders

Reported insider records show no Thiokol insider trade on the crash day. The nearest cited sale is 5,000 shares by a divisional officer on February 24, and the largest sale in the following year is by the chairman on August 7. Neither can explain the initial price adjustment. The source also finds no abnormal stock-price, volume, or short-interest pattern around earlier launches and no pre-launch short sale in Thiokol on the disaster day.

Absence from this database is not proof that no knowledgeable person traded. Engineers and lower-level employees need not appear in the covered reporting category; informed parties could communicate to others, trade related firms, or fail to report. The paper raises these possibilities but does not establish them. It also records that Martin Marietta's president acquired 30,000 shares that day through option exercise, with unknown intraday timing, rather than a documented market purchase.

Table 3 lists Thiokol's NYSE trades from 11:40 through 11:52. A 3,200-share downtick at 11:48 follows the 11:47 news flash; 16,200 shares trade at \$37.125 at 11:49, and 10,000 at \$37 at 11:51. Further trades at \$37 occur before the halt. Tick direction is used as a clue to likely selling pressure, not as an observed identifier of a trader's knowledge or an infallible trade-signing algorithm.

The source estimates avoided losses by comparing sale proceeds before the halt with the value of the same shares at the \$35 NYSE reopening price:

$$
G_{\mathrm{avoid}}=\sum_{k\in\mathcal T}q_k(p_k-35).
$$

It reports **\$113,575** for 52,500 shares, or **\$83,825** after excluding uptick trades. A direct table check reveals a boundary discrepancy: all ten printed rows total 53,200 shares and imply \$115,237.50. Omitting the first 700-share transaction at 11:40 exactly recovers 52,500 and \$113,575. The text does not explain that exclusion. A reproducing implementation should disclose it rather than claim the reported amount uses every listed post-crash trade.

The 200,000-share reopening auction could not avoid the \$2 fall from the last pre-halt price, representing \$400,000 of repricing for that block. The point is that a large valuation adjustment need not be accompanied by equally large realized gains to a trader who successfully sold at the old price. Halted trading itself limits such execution opportunities.

## Hypothetical purchases of the other contractors

The next exercise estimates what a person who knew the other firms were not responsible might have earned by buying during their declines. It accumulates the actual trades from the start of each decline through its minimum and then matches the accumulated quantity against trades at the end of the day. For Rockwell, for example, 49,900 shares purchased during the decline are matched to the last 49,900 shares traded that day.

| Firm | Accumulation interval | Trades | Shares | Acquisition cost | Same-day return | Next-day return | One-month return |
|---|---|---:|---:|---:|---:|---:|---:|
| Lockheed | 11:45–11:58 | 21 | 37,100 | \$1,697,825 | 0.41% | 1.06% | 22.10% |
| Martin Marietta | 11:53–12:06 | 25 | 32,300 | \$1,098,575 | −0.62% | −2.61% | 17.61% |
| Rockwell | 11:46–11:55 | 18 | 49,900 | \$1,688,025 | 1.39% | 3.46% | 11.96% |

The total reported same-day profit is \$23,625, or 0.53%, compared with a 1.13% rise in the Dow Jones index over the day. Selling at the following day's close produces a reported \$47,887, a little over 1%, versus a 1.3% two-day Dow increase. Longer holding periods produce larger gains but expose the position to unrelated market risk. Small dollar differences when summing rounded table entries should not be treated as additional empirical precision.

This is an ex post profit-accounting exercise, not an implementable strategy backtest. The buying window ends at the realized minimum, which is not known in real time. It assumes the hypothetical investor can take the recorded trades at their recorded prices without altering the path. It does not deduct a separately modeled spread, commission, or impact cost. The results describe the scale of gains embedded in those transactions, with hindsight, and help explain why the authors cannot easily identify an exceptionally profitable informed-trading operation.

## Liquidity during Thiokol's halt

For the 11:39–12:44 window, Table 5 reports 233,800 Lockheed shares in 101 trades, 176,000 Martin Marietta shares in 85 trades, and 290,400 Rockwell shares in 120 trades. Trading continues in all three despite substantial price declines. Most transactions have no price change; most nonzero changes are one tick, then **one-eighth of a dollar**, rather than today's decimal penny tick.

Tables 6 and 7 examine the full day's relationship between transaction size and price changes. For each firm, no-change trades are the most frequent category, followed generally by one-tick moves. Across the 40 listed largest trades, seven (17.5%) move price by more than one tick. Three firms have exactly two such trades out of ten, so the source's description of fewer than 20% for each stock is not literally correct. Apart from Thiokol's reopening auction, none of those largest trades moves price by more than two ticks. Large size and large price impact are therefore only loosely related in this case.

Some exceptional Lockheed trades appear out of sequence. Table 6's notes and the prose describe sharp reversals around 3:03 p.m., and the authors suspect recording-order problems. The source does not provide a universal cleaning algorithm; a reconstruction should preserve documented corrections and test how alternative ordering affects tick classification. Treating every apparent price jump as information without checking sequencing would overstate the evidence.

The authors do not observe specialist identities or inventories. Instead, they define a hypothetical liquidity provider as buying the full quantity of each downtick trade and selling the full quantity of each uptick trade. Zero-change trades are excluded. Let signed inventory increments be $h_k=q_k$ on downticks, $h_k=-q_k$ on upticks, and zero otherwise. Starting from zero incremental inventory,

$$
I_t=\sum_{k\le t}h_k,
\qquad
C_t=-\sum_{k\le t}h_kp_k,
\qquad
\Pi_T=C_T+I_Tp_T.
$$

Here $p_T$ is the final observed price before Thiokol resumes, whether or not that last trade changes price. This reconstructs incremental mark-to-market P&L under the authors' classification, not an actual specialist's account. Bid–ask quotes, customer direction, preexisting inventory, hedges, and dealer identities are unavailable.

Table 8 gives:

| Firm | Classified liquidity trades | Classified shares | Net cash flow | Ending inventory value | Net P&L |
|---|---:|---:|---:|---:|---:|
| Lockheed | 46 | 119,300 | −\$2,839,813 | \$2,820,313 | −\$19,500 |
| Martin Marietta | 46 | 121,600 | \$1,822,925 | −\$1,722,350 | \$100,575 |
| Rockwell | 42 | 134,400 | \$2,027,063 | −\$2,060,400 | −\$33,338 |

The reported combined P&L is **\$47,737**. The capital requirement is approximately \$6.7 million, defined as the sum of absolute maximum inventory positions across the three stocks, without applying margin offsets. The authors report a total transaction value around \$11.8 million. This is a short-window inventory-support exercise, not an annual return strategy, and annualizing its gain would be highly misleading. There is a one-trade classification discrepancy: Table 5 lists 101 Lockheed trades, of which 54 have no price change, implying 47 nonzero-change trades rather than Table 8's 46. The other two firms' counts reconcile. Raw transactions would be needed to identify the additional exclusion or boundary convention.

Several printed arithmetic conventions need separation. The 134 classified trades total **375,300 shares**, whereas **700,200** is the volume of all 306 trades in Table 5. The prose combines 700,200 with 134 and obtains 6.8 cents per share. Dividing the same P&L by classified liquidity shares instead gives approximately **12.72 cents per share**; profit per classified trade is about **\$356**. Both denominators can be described, but they answer different questions. The prose also prints Rockwell inventory as −\$2,080,400 in one place; Table 8's −\$2,060,400 is the value consistent with its cash flow and P&L, subject to rounding.

The source compares the cross-firm standard deviation of the three P&Ls, \$73,646, with their total profit. This is not a conventional portfolio Sharpe ratio: it combines a sum across firms with cross-sectional dispersion and does not estimate a repeated time-series risk distribution. The defensible conclusion is modest observed dollar gains under a stylized liquidity classification, not a precisely estimated risk-adjusted dealer return.

## Interpretation, limitations, and a replication plan

The price evidence supports rapid relative differentiation. Thiokol alone experiences the early NYSE halt, a much larger daily decline, exceptional volume, and a sustained loss broadly compatible with later costs. The other contractors recover much of their initial losses. These patterns are consistent with markets using dispersed technical knowledge to infer culpability before the official investigation finishes.

The mechanism remains underidentified. Public awareness of the crash is clear; private understanding of the O-rings is plausible; the identity, communication, and exact trades of knowledgeable agents are not observed. Market makers might infer from order flow, telephone contacts, other firms' trading, or the halt itself. The paper discusses those channels as possibilities, not separately estimated causal effects. An initial fall followed by recovery in the other firms may reflect rational uncertainty being resolved, rather than a proven behavioral overreaction.

For a faithful replication, first recreate the news and exchange timeline; then assemble the exact four daily series and the pre-event comparison window; reproduce Table 1's standardized deviations; reconstruct exchange-specific transaction sequences and the two normalized price figures; calculate potential informed-sale and related-firm purchase profits with explicit window endpoints; and finally apply the tick-based liquidity inventory rule. Each stage should retain a reconciliation between printed and recomputed quantities, particularly the 700-share exclusion and the liquidity-volume denominator.

Further tests would need additional data: quotes and order submissions to classify initiators, specialist records to observe actual inventory, account identifiers to connect trades with information, and a broader set of comparable accidents to assess generality. The current study supplies none of those. Its internal controls and precise timing are strengths, but a memorable single case cannot estimate the average speed or accuracy of market price discovery across all events.

The most transferable research implication is to follow related securities during a firm-specific halt. No trade in the halted stock does not mean no learning about its value. Price discovery can proceed through the stocks still trading, order imbalances, and the informational content of the halt. That insight also explains why firm-specific halts and market-wide circuit breakers need separate analysis. The paper's achievement is to document this interconnected process while candidly leaving the identity of its information suppliers unresolved.
