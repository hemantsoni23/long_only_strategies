# Does Algorithmic Trading Improve Liquidity?

**Authors:** Terrence Hendershott, Charles M. Jones, and Albert J. Menkveld. **Version inspected:** December 3, 2009 manuscript, first draft August 20, 2007; the bundled Internet Appendix is dated December 2, 2009. The local filename's 2010 date should not be used to substitute results from a later published version. **Source:** [LiquidityTrading_Henderschott_2010.pdf](../../Finance/LiquidityTrading_Henderschott_2010.pdf), 59 PDF pages including the appendix. Main-paper page numbers below refer to printed pages; Tables 1–5 occupy PDF pages 27–32 and the appendix begins on PDF page 38.

## Why this matters

Electronic message traffic and liquidity both changed dramatically during the automation of equity markets. Their joint trend does not show that algorithmic trading caused better liquidity: algorithms may simply choose liquid stocks, and volatility, trading volume, and market design change concurrently. This paper's contribution is an identification strategy using the staggered introduction of automated quote dissemination on the NYSE in 2003. It also goes beyond asking whether spreads narrow. The authors separate the compensation retained by liquidity suppliers from adverse-selection losses, and distinguish price discovery through trades from price discovery through quote revisions.

The evidence is strongest for larger stocks. Instrumented algorithmic activity reduces quoted and effective half-spreads, decreases adverse selection, and raises realized spreads over the event window. Thus a customer's lower trading cost can coexist with a supplier's higher measured spread revenue. Faster quote adjustment is the proposed mechanism: public information enters standing prices before someone can exploit a stale quote. The study does not identify the profitability of every algorithm, the cost of executing a complete institutional order, or the welfare effects of contemporary high-frequency trading under stressed conditions.

## What “algorithmic trading” measures

Algorithmic trading here includes computers making order-submission and cancellation decisions, including the execution of an externally chosen parent order. It is broader than automated investment-signal generation, and the data do not label each strategy as market making, arbitrage, or directional speculation.

The proprietary NYSE System Order Data identify electronic messages through SuperDOT: order submissions, cancellations, and trade reports. Specialist quotation messages and manually handled floor-broker orders are excluded. This exclusion matters because the instrument is the introduction of automatic dissemination of the specialist's best quote. Those automatically disseminated quotes are not mechanically added to the message-count numerator used to measure algorithmic activity.

Let $M_{it}$ denote the number of electronic messages for stock $i$ on day $t$, and $D_{it}$ its dollar trading volume. The principal proxy is

$$
A_{it}=-\frac{D_{it}}{100M_{it}}.
$$

It is negative dollar volume per message, measured in hundreds of dollars. More message-intensive trading raises $A_{it}$ toward zero. A change from −18.44 to −17.44 means dollar volume per message falls from \$1,844 to \$1,744. It does not mean algorithmic trading's market share rises by one percentage point.

The normalization removes a major scale difference between active and inactive stocks. The negative reciprocal convention also allows spreads to approach a lower limit as message traffic becomes very high. This functional form is an empirical modeling choice, not a technologically invariant measure of automation. Algorithmic activity can rise because new traders enter, existing algorithms submit and cancel more frequently, or parent orders are divided into smaller pieces. All three mechanisms affect the proxy. Changes in trading volume can affect it even without additional messages, so the appendix separately examines raw messages and volume.

Figure 1 shows large-stock message traffic rising from roughly 35–40 messages per minute in early 2001 to about 250 by late 2005. Their volume per message falls from approximately \$7,000 to \$1,100. These descriptive movements motivate the analysis but do not supply its causal identification.

## Samples, timing, and measured outcomes

The descriptive panel begins in February 2001, after NYSE decimalization, and ends in December 2005. It combines CRSP, TAQ, and the NYSE message data for 943 common stocks present throughout the period, giving 59 monthly observations per stock. Stocks with average prices below \$5 or above \$1,000 are excluded. The balanced-panel requirement selects continuing stocks and is not a survivorship-free reconstruction of the entire exchange.

The causal event panel runs from December 2, 2002 through July 31, 2003: 167 trading days and 1,082 stocks. The price filter is retained. Stocks must have at least 21 transactions on every sample day so that the trade-by-trade VAR can be estimated consistently across the analyses. The authors sort stocks into five market-capitalization groups; Q1 contains the largest and Q5 the smallest. The text does not provide a sufficiently explicit sort-date/reconstitution rule to reconstruct those assignments solely from the PDF. Variables are winsorized at the 0.05th and 99.95th percentiles.

For transaction $k$, let $p_k$ be its price, $b_k$ and $a_k$ the contemporaneous bid and ask, $m_k=(a_k+b_k)/2$, and $q_k\in\{-1,+1\}$ its seller/buyer initiation sign. The paper follows the Lee–Ready signing approach using contemporaneous quotes. A replicator should not silently impose a five-second quote lag merely because that appears in other applications of the method.

The four central proportional half-spread measures are

$$
QS_k=\frac{a_k-b_k}{2m_k},\qquad
ES_k=q_k\frac{p_k-m_k}{m_k},
$$

$$
RS_k(h)=q_k\frac{p_k-m_{k+h}}{m_k},\qquad
PI_k(h)=q_k\frac{m_{k+h}-m_k}{m_k},
$$

where $h$ is five or thirty calendar minutes after the transaction. Multiply each ratio by $10^4$ to obtain basis points. These are half-spreads: doubling is required to compare with an otherwise equivalent quoted full-spread statistic. The accounting identity is

$$
ES_k=RS_k(h)+PI_k(h).
$$

$RS$ approximates the supplier's revenue if the inventory position can be marked or closed at the later midpoint. It is not net profit after fees, infrastructure costs, inventory financing, and actual unwind execution. $PI$ measures the signed subsequent midpoint movement; calling all of it private-information loss requires an interpretation beyond the arithmetic identity.

Daily stock-level observations are share-volume-weighted across NYSE transactions. Monthly figures use a simple average of daily values; size-group figures then average across stocks. Quoted depth is measured at transaction times, share-weighted, in thousands of dollars. This sampling scheme emphasizes states in which trades occur rather than uniformly sampling the entire trading day.

Table 1 reports Q1 mean quoted half-spread 5.19 basis points, effective half-spread 3.63, five-minute realized half-spread 1.21, and price impact 2.42. Average quoted depth is \$71,220 and average price is \$40.01. Q5's quoted and effective half-spreads are 19.89 and 14.50 basis points. The within-stock standard deviation reported for the algorithmic proxy is 4.54, or \$454 per message; this is the table's average within-stock dispersion, not a separately documented Q1-only dispersion.

## The natural experiment and its identifying assumptions

Before autoquote, a specialist had to disseminate an updated quote manually after a better order entered or the best standing order disappeared. Autoquote made dissemination of the new best bid and offer automatic. It reduced delay and the effort necessary for electronic suppliers to maintain current quotes. It did not abolish the specialist's other advantages, make all executions automatic, or convert this historical NYSE into a modern fully electronic market.

Introduction began on January 29, 2003 with six active stocks. More than 200 were covered by March, and the remaining stocks moved on May 27. Figure 4 shows much more staggered exposure among larger stocks; most smaller stocks move together at the end. The schedule was decided in late 2002, with stock activity and specialist receptiveness to technology influencing early adoption. This is predetermined rollout, not randomized assignment.

Define $Z_{it}=1$ from stock $i$'s adoption day onward. The instrument creates cross-stock timing variation after absorbing stock and calendar-day fixed effects. The regression is estimated separately within capitalization quintiles:

$$
L_{it}=\alpha_i+\gamma_t+\beta A_{it}+\delta'X_{it}+\varepsilon_{it}.
$$

$L$ is one liquidity or information outcome. $X$ includes annualized share turnover, daily range-based Parkinson volatility, inverse stock price, and log market capitalization. The first stage replaces the endogenous $A$ with its projection on $Z$, controls, and the same fixed effects. Reported control coefficients in the tables are capitalization-weighted summaries across quintiles; they are not common restrictions imposed in the underlying regressions. Standard errors accommodate cross-sectional and temporal heteroskedasticity and within-stock serial correlation. This description should not be relabeled as two-way stock-and-date clustering without further implementation evidence.

Table 2's first-stage-style comparisons show the average message rate increasing by 2.135 per minute after adoption, and by 6.286 in Q1. The corresponding coefficient on the normalized $A$ proxy is 0.291 overall and 0.414 in Q1. Q4's normalized-proxy change is small and insignificant, whereas Q5 has a positive significant change; the raw-message result for Q5 is insignificant. The two proxy definitions do not have identical relevance patterns.

A causal interpretation requires more than predetermined dates. Conditional on the included effects and controls, rollout timing must not coincide with otherwise unmodeled liquidity changes. Autoquote must affect the dependent variable through the algorithmic activity represented by $A$, rather than a separate direct channel. Market-wide spillovers and heterogeneous rollout responses must not invalidate the use of the remaining stocks as controls. Activity-based early adoption and changes in the usefulness of publicly displayed quotes make those economically meaningful assumptions.

The authors examine whether poor liquidity before adoption simply reverts toward normal afterward. Daily quoted spreads have an estimated autoregressive coefficient around 0.18, implying rapid rather than persistent mean reversion; forecasts based on pre-event conditions do not explain the spread improvements. This helps with one concern but is not proof of the complete exclusion restriction.

Tables 3 and 5 report first-stage exclusion statistics between 5.88 and 7.32 for five restrictions in their combined specifications. They do not establish uniformly strong identification within every quintile. In particular, many small stocks adopt on the same last date, providing little differential timing after day effects. Large and imprecise Q4/Q5 estimates should not be read as either reliable harm or proof of zero effect.

## Spread and depth results, with economically consistent units

Table 3 Panel A gives the following IV responses to a one-unit increase in $A$. Parentheses contain reported $t$ statistics.

| Outcome | Q1 | Q2 | Q3 |
|---|---:|---:|---:|
| Quoted half-spread, basis points | −0.53 (−3.23) | −0.42 (−2.21) | −0.43 (−1.44) |
| Effective half-spread, basis points | −0.18 (−2.67) | −0.32 (−2.23) | −0.35 (−1.56) |
| Quoted depth, thousands of dollars | −3.49 (−2.51) | −1.43 (−1.16) | −1.99 (−1.07) |

The paper's one-standard-deviation illustration multiplies Q1's quoted-spread coefficient by 4.54, obtaining a 2.41-basis-point reduction, approximately 46% of the 5.19-basis-point mean. This is an economically scaled IV sensitivity, not the average event's measured spread reduction. The reduced-form adoption effect reported in the text is considerably smaller: Q1 quoted half-spreads decline by 0.50 basis points, with $t=-9.18$, and effective half-spreads by 0.17, with $t=-4.33$. Effective-spread reductions for Q2 and Q3 are 0.21 and 0.23. First-stage coefficients from differently controlled tables should not be multiplied mechanically to reproduce these estimates.

Depth falls as quotes improve. At Q1 means, one unit of $A$ reduces quoted depth by about 4.9% and the half-spread by about 10.2%. For an order initially equal to displayed depth, the authors' stylized comparison allows most shares to benefit from the lower spread while a small remainder executes deeper in the book. This suggests an improvement for modest order sizes, but requires an assumption about the undisplayed price schedule.

Panel B estimates effective-spread effects within transaction-size bins: 100–499, 500–1,999, 2,000–4,999, 5,000–9,999, and at least 10,000 shares. Q1 coefficients in the first three bins are −0.12, −0.22, and −0.25 basis points, with $t$ statistics −3.06, −3.25, and −2.76. The two larger bins have smaller, insignificant effects. These are executed transaction sizes. An institutional parent order may generate many such prints, and more slicing can improve per-print statistics without lowering its total execution cost.

## Where the improvement comes from

The five-minute decomposition in Table 3 Panel C is especially informative:

| Response, basis points per unit of $A$ | Q1 | Q2 | Q3 |
|---|---:|---:|---:|
| Realized half-spread | +0.35 | +0.76 | +1.03 |
| Price impact | −0.53 | −1.07 | −1.39 |

For Q1, $t=3.52$ for realized spread and $t=-3.56$ for impact. Their sum is −0.18, agreeing with the effective-spread response. The thirty-minute Q1 estimates, +0.33 and −0.51, imply the same net change. Thus the conclusion is not an artifact of choosing only a five-minute marking horizon.

The authors interpret the higher realized spread as temporary rents to algorithmic liquidity suppliers who are relatively early adopters. Faster updating reduces being picked off; reduced losses more than compensate for narrower transaction spreads. In the longer descriptive series, realized spreads subsequently decline, which is consistent with competitive entry dissipating those rents. The identities of the suppliers and their entry decisions are not observed well enough to make this a direct causal test of that competition story.

Table 4 shows Q1 specialist participation falling by 0.59 percentage point per unit of $A$, with $t=-2.22$. Trades per minute increase by 0.58, with $t=2.60$, and average transaction size falls by \$2,040, with $t=-4.64$. These results fit a shift toward more electronic, smaller transactions. They do not show that aggregate investor turnover necessarily rises: turnover coefficients vary across groups. Several printed significance stars are difficult to reconcile with the caption's nominal cutoffs, so the reported coefficient and $t$ statistic are preferable to translating stars into stronger confidence claims.

## Reconstructing the price-discovery analysis

The Hasbrouck analysis uses transaction time separately for each stock-day. Let $r_k$ be the log change in the quote midpoint from transaction $k-1$ to $k$, and let $q_k$ be signed order flow. Estimate

$$
r_k=\sum_{j=1}^{10}\alpha_j r_{k-j}
+\sum_{j=0}^{10}\beta_jq_{k-j}+\epsilon_{rk},
$$

$$
q_k=\sum_{j=1}^{10}\gamma_jr_{k-j}
+\sum_{j=1}^{10}\phi_jq_{k-j}+\epsilon_{qk}.
$$

Current order flow enters the return equation. This ordering makes its residual orthogonal to the order-flow innovation. Invert the system to a vector moving-average representation

$$
\begin{pmatrix}r_k\\q_k\end{pmatrix}
=\begin{pmatrix}a(L)&b(L)\\c(L)&d(L)\end{pmatrix}
\begin{pmatrix}\epsilon_{rk}\\\epsilon_{qk}\end{pmatrix}.
$$

The permanent midpoint response to a unit order-flow innovation is $b(1)=\sum_{j\geq0}b_j$. Efficient-price innovation variance per transaction is

$$
\sigma_w^2=a(1)^2\sigma_r^2+b(1)^2\sigma_q^2.
$$

These are squares of cumulative impulse responses, not sums of squared individual responses. The first term is trade-unrelated variance; the second is trade-related variance. Multiply each variance by the day's transaction count to express it on a daily basis, then take square roots for the reported daily standard-deviation outcomes. Multiplying a standard deviation directly by transaction count would be wrong.

Use these estimated daily outcomes in the IV framework, preserving the table's specification distinction. Table 5's caption excludes all four control variables from the Hasbrouck volatility-component regressions in Panel B: turnover, volatility, inverse price, and log capitalization. Stock and calendar-day effects remain. Panel A's permanent-impact regressions include all four controls. The main text instead says the component regressions use the same controls; that statement conflicts with the caption and the absence of control coefficients in Panel B. A reconstruction following the table should omit those controls and document the discrepancy.

Q1's long-run trade impact declines by 0.54 basis point per unit of $A$, with $t=-3.50$. Q2 and Q3 estimates are −1.21 and −1.44. Q1 trade-related daily standard deviation falls by 0.22 percentage point, with $t=-2.62$, while non-trade-related standard deviation rises by 0.12 percentage point, with $t=2.48$. Q2's corresponding estimates are −0.26 and +0.13. Scaling the Q1 decline by 4.54 gives approximately one percentage point of daily trade-related standard deviation, a large sensitivity relative to the observed level.

The evidence supports a redistribution of information incorporation toward quote revisions. “Trade-related” does not logically mean all information was private: trading against a stale quote after public news also creates a trade-associated price move. Nor does higher non-trade-related volatility automatically mean a less efficient market. It can reflect prices responding sooner to news that otherwise would have entered through transactions.

## What the appendix contributes

The Internet Appendix checks an alternative spread decomposition, instrument measurement error, possible mechanical consequences of quote dissemination, and a simple economic mechanism.

In the Lin–Sanger–Booth decomposition, let $s$ be effective half-spread, $\lambda$ the coefficient relating midpoint changes to signed trades, and $\delta$ the probability that successive trade signs agree. The persistent-order-flow part is $(2\delta-1)s$, the adverse-selection part is $\lambda$, and the remaining fixed component is

$$
f=s-\lambda-(2\delta-1)s.
$$

Estimate $\lambda$ from midpoint changes on trade signs and sign persistence from a first-order trade-sign regression. Table IA-6 gives Q1 responses of +0.26 basis point for the fixed component, −0.26 for adverse selection, and −0.18 for persistence. They add to the −0.18 effective-spread response and corroborate the main finding using a different decomposition.

The measurement-error argument requires two orthogonality conditions. If measured $A=A^*+u$ and the true structural effect is $\beta A^*$, the observed-data error is $\varepsilon-\beta u$. IV consistency therefore requires the instrument to be orthogonal to both the economic error and proxy error. The appendix repeats one covariance condition typographically; reproducing that repetition would omit the substantive second restriction. Autoquote changing message intensity in ways unrelated to the intended latent activity can violate it.

A stale disseminated quote can bias both trade signs and measured spreads. The appendix considers whether merely displaying a new inside order sooner mechanically produces the findings. Some simple stale-midpoint mechanisms predict the wrong effective-spread or adverse-selection direction. Similar results at five and thirty minutes also make a brief replenishment delay less persuasive. These checks narrow the alternatives without proving that every direct dissemination channel is absent.

Table IA-4 shows spread reductions with raw message traffic as the instrumented activity variable, supporting a role for messages rather than only volume normalization. Table IA-5 removes turnover from the controls: Q1 quoted and effective coefficients remain negative, −0.67 and −0.23. Robustness is not uniform across all groups; Q5's quoted coefficient becomes positive, 4.52 with $t=2.04$, reinforcing caution about small-stock inference.

The appendix's two-step model offers intuition rather than a fitted structural estimate. Fundamental value follows two symmetric increments of size $\epsilon$. Human dealers face monitoring cost $c$; a customer's noninformational valuation differs by $\theta$, with $2c>\theta$ and $\epsilon>\theta$. Without interim monitoring, competitive human quotes are wide enough to avoid losses to informed terminal trading. An algorithm that observes the first value movement cheaply can improve the appropriate quote, attract additional mutually beneficial trades, and update publicly displayed prices before another transaction. Imperfect competition permits it to retain some benefit. This construction explains why narrower spreads, higher supplier revenue, and more non-trade price discovery can occur together, but provides no estimate of a modern algorithm's monitoring cost or optimal latency expenditure.

## Replication boundaries and implications

A faithful replication needs the proprietary message records, TAQ transaction and quote records, CRSP identifiers and capitalization data, and the individual stock adoption dates. The PDF supplies the broad schedule but not a complete machine-readable stock-date treatment map. It also does not fully specify every trade-condition filter, handling of tied timestamps or crossed markets, quintile assignment date, treatment of end-of-day future-midpoint horizons, or numerical safeguards for unstable daily VARs. Those choices must be documented rather than invented as reported author settings.

The panel design estimates the response to automation encouraged by this particular exchange change. Its most persuasive finding concerns large NYSE stocks in early 2003. It does not establish that every increase in message traffic is beneficial, that effects remain unchanged in fragmented modern markets, or that algorithms will continue supplying liquidity during crises. For execution research, the useful discipline is to examine spreads, depth, adverse selection, and complete-order costs separately. For market design, the result suggests that making standing quotes easier to keep current can improve observed trading terms and shift information into prices without requiring a trade, subject to the identifying assumptions and historical scope above.
