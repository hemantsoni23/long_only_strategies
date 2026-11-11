# The Intended and Collateral Effects of Short-Sale Bans as a Regulatory Tool

Terrence Hendershott, Ethan Namvar, and Blake Phillips. *Journal of Investment Management* 11(3), Third Quarter 2013, pp. 5–13. [Source PDF](../../Finance/shortsaleban_hendershott_2013.pdf). All nine pages were read, including both figures, endnotes, and references. Printed page numbers equal PDF page numbers plus four. This is a research synthesis in the journal's Insights section, not a new structural model or a single unified event-study dataset.

## Why this matters

Restrictions on shorting a stock can alter the cost of hedging options, supplying convertible financing, creating inverse ETF shares, and transferring credit exposure. A portfolio that appears diversified by instrument can therefore retain a common dependence on stock-borrow availability. This article's contribution is to organize evidence on those connected effects of the 2008 short-sale ban, distinguish the policy's intended outcomes from its collateral costs, and retain the uncertainty about the unobserved no-ban counterfactual.

The paper finds substantial evidence of worse liquidity and slower information incorporation. Evidence that bans successfully sustained prices or restored confidence is less clear, particularly in the United States, where support for financial institutions and TARP announcements coincided with the restrictions. A reduction in measured short positions is not sufficient evidence of improved price discovery, lower volatility, or better capital allocation.

For a researcher, the article functions as a map of mechanisms and empirical inputs. Its numerical results come largely from the cited studies, not from one newly estimated model. The appropriate implementation is an evidence ledger that preserves each study's market, sample, normalization, comparator, and source version. Pooling the headline numbers as if they were independent estimates of one treatment effect would lose the paper's central distinction between direct restrictions and transmission through hedging markets.

## Policy event, objectives, and interpretation

The focal U.S. restriction operated from September 19 through October 8, 2008 and targeted financial-sector stocks. The source also discusses the international 2008 bans and European restrictions during the 2011 sovereign-debt crisis. It identifies two intended effects: restraining speculative or manipulative short-selling pressure, and supporting investor confidence. These are different hypotheses. Lower short interest directly addresses the first instrument, while confidence is latent and must be inferred imperfectly from prices or volatility.

The policy does not remove every way to obtain negative exposure. Derivatives-market-maker exemptions, put options, CDS protection, and the particular rules governing intermediaries can allow exposure to move between markets. The relevant treatment is therefore not simply a binary indicator attached to an issuer. It includes which transactions are restricted, which entities are exempt, what hedges remain feasible, and whether participants expect the exemptions to persist.

The article's introduction associates Lehman's bankruptcy announcement with September 19. Its substantive event analysis consistently uses September 19 as the ban's start. A separate source in the library, [Battalio, Mehran, and Schultz, p. 3](../../Finance/shortsaleban_battalioSchultz.pdf), dates the Chapter 11 filing to September 15. The ban window should not be moved to resolve this introductory chronology error.

The economic assessment implicitly balances avoided harm from a possible destabilizing feedback against trading, informational, and financing costs. The source does not assign probabilities to a prevented systemic collapse, estimate a social objective function, or solve a policy optimization problem. Its conclusion explicitly allows that unobservable benefits could in principle outweigh measured costs. Consequently, its evidence does not furnish a numerical threshold at which a regulator should impose or lift a ban.

## Outstanding shorts: what Figure 1 measures

Figure 1, printed p. 7, plots the value-weighted average percentage of float sold short during 2008 for banned and nonbanned stocks in the CRSP universe, supplied by Harris, Namvar, and Phillips. This is an outstanding-position measure. It is neither daily short-sale volume nor a direct count of traders expressing negative information.

A natural reconstruction would define, for group $g$,

$$
\operatorname{SI}_{g,t}
=\sum_{i\in g}w_{i,t}\frac{\operatorname{ShortShares}_{i,t}}
{\operatorname{Float}_{i,t}},
\qquad
\sum_{i\in g}w_{i,t}=1.
$$

The source states value weighting but does not provide the constituent list, float vendor, exact value-weight definition, rebalancing convention, or observation calendar. This expression formalizes the described statistic; it is not a fully specified algorithm recovered from the figure.

Both series begin near 5% and end near 4%. The nonbanned series rises to roughly 7% close to the September event; the banned series also reaches approximately 7% around the crisis and has an earlier summer peak. The figure should be used for its broad comovement and decline, rather than treating every prose approximation as an exact dated observation.

The main inference is limited: short positions declined in targeted stocks, but also across the broader market. The authors explicitly find no clear abnormal reduction unique to banned stocks relative to the rest of the market. Deleveraging, changes in borrowing supply, risk limits, or marketwide demand can affect both groups. A before/after fall within the banned group does not isolate a ban effect.

The derivative-substitution evidence is mixed. Battalio and Schultz find a comparable option-to-stock volume ratio for banned stocks and controls before and during the intervention, which does not support a large migration into options on that measure. Other studies find different price effects for optionable and nonoptionable stocks. Those observations are not logically equivalent: a stable volume ratio can coexist with changed marginal demand, altered prices, or reduced transaction capacity.

## Price effects, optionability, and confidence

Figure 2, also on printed p. 7, reproduces Harris and coauthors' evidence on stocks with and without traded options. The figure reports ban-period price-inflation annotations of 12.8% for nonoptionable stocks and 1.6% for optionable stocks. The source's prose describes the latter as negligible. The annotation is a reported ban-period effect; it should not be read as the absolute height of the plotted cumulative-difference line at the end date.

The economic interpretation is that an alternative venue for negative exposure may limit cash-equity overpricing when direct shorting is constrained. But optionability is not randomly assigned. Optionable firms tend to differ in size, liquidity, investor base, and other characteristics. The nine-page review does not reproduce the full factor-analytic model, controls, standard errors, or construction of the plotted cumulative differences. Exact replication requires the underlying Harris study and data.

For broader price effects, the review reports two U.S. findings. Boehmer, Jones, and Zhang find roughly 5% relative price improvement for banned stocks against matched controls. Harris and coauthors estimate 10–12% price inflation with a factor-analytic model. These are different estimators with potentially different baselines; averaging them into a “7.5%–8.5% effect” would be unjustified.

The authors discuss two obstacles to causal attribution. TARP-related news was expected to benefit many of the same financial firms. Also, a temporary ban-induced price distortion should tend to unwind after the restriction ends, yet post-ban reversal is not uniform. Harris finds correction primarily among stocks with negative pre-ban performance. Boehmer and coauthors find an initial correction that reverses the next day. The paper therefore acknowledges a sustained confidence effect as an alternative interpretation, rather than asserting that every U.S. price rise is mechanical overvaluation.

International evidence is offered as a partial way around the U.S. policy coincidence. The review describes Beber and Pagano's study of the United States and twenty-nine other countries, emphasizing that price increases associated with bans outside the United States reversed afterward. Different country dates and policies provide additional variation, but do not by themselves make treatment exogenous: crisis severity, bank exposure, and policy choice can remain correlated. The review does not give a unified identification strategy that removes those concerns.

Volatility is another imperfect confidence proxy. The paper reports Boehmer and coauthors' finding that the proportional intraday price range was 3.43 percentage points greater for banned stocks, compared with a negligible pre-ban group difference. This is a range statistic, not annualized volatility, variance, or a 3.43% multiplicative increase. Lioui's separate results are described as a broader spread of volatility across the market. The source does not supply coefficient tables or estimation settings for either volatility analysis.

## Liquidity and information incorporation

The clearest quantitative contrasts concern equity execution costs. From Boehmer, Jones, and Zhang, the review reports:

| Measure | Banned stocks: before → during | Controls: before → during | Derived change difference |
|---|---:|---:|---:|
| Effective spread | 42 → 145 bp | 35 → 57 bp | 81 bp |
| Standardized five-minute price impact | 33 → 76 bp | 30 → 48 bp | 25 bp |

The last column is arithmetic from the reported group numbers:

$$
(145-42)-(57-35)=81,
\qquad
(76-33)-(48-30)=25.
$$

These simple differences are not claimed to be the underlying papers' fully controlled treatment coefficients. They have no standard errors in this review. In particular, they should not be substituted for a multivariate effective-spread estimate from another version of the same research.

The effective spread measures the cost of executing relative to a quote reference; five-minute impact attempts to capture subsequent price adjustment. Their exact trade-sign rule, quote timestamp, normalization, and averaging weights are not given here. A high-frequency reproduction must recover those definitions from the cited study rather than assuming that all measures called “effective spread” are operationally identical.

For information incorporation, Beber and Pagano regress weekly stock returns on the national market return and examine residual autocorrelation. The reported median autocorrelation is larger for banned stocks, consistent with slower adjustment to information. A reconstruction starts with

$$
r_{i,t}=a_i+b_i r_{m(i),t}+e_{i,t},
\qquad
\rho_i(1)=\operatorname{Corr}(e_{i,t},e_{i,t-1}).
$$

The article does not state the full estimation window, minimum observations, missing-week treatment, or inference procedure. The signal is economically suggestive, but departures from a random walk can also reflect changing expected returns, asynchronous measurement, or other omitted dynamics. A residual-autocorrelation comparison is not a direct observation of fundamental value.

Ni and Pan's evidence adds a cross-market dimension: during the ban, negative information in options and CDS markets becomes more predictive of equities. The review interprets this as delayed incorporation into cash-stock prices. No lag coefficients, precise forecasting horizon, sampling frequency, or out-of-sample trading exercise are supplied. It is therefore evidence about relative information flow, not a ready-made derivatives-to-equity alpha.

## Options and transfers between investors

A stock-short restriction can raise option trading costs because the option intermediary's hedge becomes uncertain or costly. For a dealer holding an option with positive equity delta $\Delta$, the usual first-order hedge requires a stock position near $-\Delta$. If that short is infeasible, the same option position carries more residual directional risk or requires another imperfect hedge. This is an accounting explanation of the source's mechanism, not a calibrated dealer-control model estimated in the paper.

Battalio and Schultz's cited study estimates an additional \$505 million paid by liquidity-demanding option investors through wider bid–ask spreads. Grundy, Lim, and Verwijmeren find more frequent put–call-parity violations during the ban, while higher trading costs limit the profits available from exploiting them. A larger observed parity gap does not imply a larger executable arbitrage if the necessary stock hedge or funding leg is restricted.

This section's heading refers to an increase in option prices, but much of its quantified evidence concerns spreads. Those should be kept separate. A wider spread can increase the cost to a buyer and reduce the proceeds to a seller without identifying a unique change in the frictionless option value.

For cash-equity wealth transfers, Harris and coauthors estimate \$2.3–4.9 billion transferred between buyers and sellers due to inflated prices. The source calls this conservative, but the number remains dependent on the estimated distortion and transaction quantities. It is not additive without qualification to every spread-based cost number: transaction costs, transfers, and allocative welfare losses are different accounting objects. The review supplies no common framework that nets them into a single welfare total.

## Short covering, convertible issuance, and ETF creation

The article proposes that a ban can discourage existing shorts from covering because investors fear being unable to reopen their positions. Removing some short-covering demand could then deepen temporary declines. It notes four intraday S&P 500 declines of 4–8% during the ban. It does not estimate the amount of covering that would have occurred without the restriction or identify a causal contribution to those declines.

One sentence in the short-covering discussion refers to locking in profits “by selling short.” Closing a short requires buying shares back; the intended mechanism concerns retaining an existing short because future reopening is uncertain. The economic interpretation should follow that balance-sheet logic, not treat an additional short sale as a closing purchase.

Convertible arbitrage supplies a more concrete hedge connection. A long convertible is commonly paired with a short position in the issuer's stock. Constraining the stock hedge can reduce demand for the bond and thereby restrict the issuer's financing. The review cites estimates that convertible-arbitrage funds account for about 75% of the convertible market and that a one-standard-deviation increase in hedge-fund flows corresponds to a 38.6% increase in capital supply to convertible issuers. These are cited results, not parameters of a structural model estimated here.

The endnotes report average weekly issuance proceeds of \$944 million during the first half of 2008 and \$20 million during the ban, with issuance frequency falling from nearly three per week to only one issue during the ban. The drop in reported proceeds is approximately 97.88%, calculated as $1-20/944$. The comparison is striking, but the review does not isolate the effect of the ban from the concurrent collapse in financial-market funding. It also reports that financial firms represented an estimated 65% of the \$60 billion of convertible issuance in the first eight months of 2008. This concentration helps explain the market's exposure to restrictions on financial-sector shares.

Inverse ETFs reveal an operational version of the same problem. The source discusses the Rydex Inverse 2x S&P Select Sector Financial ETF and ProShares products whose trading was temporarily halted. Even where formal exemptions existed, swap intermediaries were less willing to hedge by shorting financial shares. Constrained creation of new ETF shares allowed secondary-market prices to separate from the value of their underlying exposure.

The reported example is a 16% premium for ProShares UltraShort Financials, ticker SKF, on September 19. The endnote says end-of-day ProShares values were used. With market price $P$ and reported portfolio value per share $N$, the relevant premium is

$$
\pi=\frac{P-N}{N}.
$$

A 16% premium is not a 16% increase in underlying asset value or a guaranteed short-ETF profit. The same creation, hedging, or borrow restrictions that permit the premium may obstruct its arbitrage. Reproduction needs synchronized market prices and NAV or portfolio values, the creation status, and the historical instrument terms. The review gives the event figure but not that complete dataset.

## CDS migration and the unmeasured policy alternative

Buying CDS protection can substitute imperfectly for negative exposure to a financial firm. The source cites Courtney's finding that CDS spreads for banned issuers were abnormally high relative to controls and later reverted, with stronger effects for issuers that had higher pre-ban short interest. It also cites Ni and Pan's evidence that derivatives led the restricted equity market in incorporating negative information.

Higher protection demand, changes in default risk, funding pressure, and counterparty risk can all affect CDS spreads. The review does not supply a model separating these components. Calling the observed increase “price inflation” describes the cited interpretation; it should not be taken as a measured pure demand shock or a directly tradable basis mispricing.

The eighth collateral channel is the opportunity cost of adopting a poorly targeted policy. The authors argue that attention devoted to short-sale bans might displace interventions aimed more directly at the crisis's funding problems. They do not identify the alternative policy, estimate its counterfactual outcome, or attach a dollar value to this channel. It remains a policy argument rather than an empirical result.

## What can be reconstructed from this source

The source supports a market-by-market event ledger: the ban dates and exemptions; outstanding-short-interest paths; optionability-specific price effects; equity spreads and five-minute impact; residual-return autocorrelation; option execution costs; convertible issuance; ETF premiums; and CDS-to-equity information flow. Each row needs its own source study, units, comparator, and statistical design.

It does not support recreating those studies from this PDF alone. Missing inputs include restricted-security histories, trade and quote data, float and short-interest series, option chains and timestamps, CDS quotes and contract conventions, issuance records, ETF price/NAV files, model coefficients, and inference settings. The endnotes give a few useful numerical details but are not a methodological appendix. There is no common portfolio experiment, transaction-cost-adjusted strategy return, or out-of-sample forecasting test.

Several printed endnote callouts are offset from their apparent content: the numbered notes about intraday declines, financial-firm issuance, convertible proceeds, and ETF end-of-day values appear one position later than the corresponding body markers suggest. The underlying statements can be matched by their wording. The figures and endnote values above were checked visually rather than assigning content solely from the superscript number.

The practical use is to stress-test the feasibility of linked positions when a hedge instrument becomes restricted. Measured price support is uncertain, observed execution and financing frictions are substantial, and alternative markets only partly preserve the original opportunity set. The paper's final caveat remains essential: the crisis outcome without the ban is not observed, so a comprehensive welfare verdict requires assumptions beyond the evidence summarized here.
