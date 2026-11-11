# The Good, the Bad & the Ugly of Payment for Order Flow

Hitesh Mittal and Kathryn Berkow, BestEx Research, May 3, 2021. This is a 20-page practitioner research paper, including a one-page appendix, rather than a refereed causal evaluation. [Local source PDF](../../Finance/PaymentForOrderFlow20210503.pdf). Page references below are PDF pages, which agree with the printed page numbers. The analysis concerns the US equity market structure and reporting rules described in 2021; its institutional descriptions should not be read as statements about present rules.

## Why this matters

An execution can improve on the displayed best quote and still be expensive relative to the price that a different market structure would produce. That is this paper's useful research question. Retail wholesalers select a comparatively benign stream of orders, return some of the resulting surplus to customers as price improvement, and pay brokers for routing the stream. The public market then prices liquidity for the remaining, potentially more informed order flow. Comparing retail executions with that public quote holds the benchmark fixed even though segmentation may help determine it.

For a quant evaluating execution quality, the paper contributes three concrete measurements: price improvement available on exchanges inside the displayed national best bid and offer; subsequent signed price movements for exchange and retail-proxy executions; and a volume-weighted counterfactual mixing those flows. It also describes a separate information advantage from observing privately routed orders. The empirical measurements, the extrapolated equilibrium response, and the qualitative competition argument have different evidentiary strength. Treating all three as a demonstrated benefit from banning payment for order flow would overstate the source.

The headline numbers are 24.5% price improvement for five wholesalers, 8.7% on exchanges, and an estimated 25.66% reduction in the quoted spread if retail flow joined exchange flow. The first two measure improvement on one execution divided by the full spread. The third measures a proportional change in the full spread. A strategy researcher must preserve that distinction before converting the results into a one-way execution-cost forecast.

## Economic mechanism and scope

Pages 3–7 explain adverse selection through the liquidity provider's exposure after a fill. A market maker sells to a buyer and loses if the midpoint subsequently rises; it buys from a seller and loses if the midpoint falls. Institutional parent orders can generate continued directional flow through repeated child orders. Short-horizon informed traders may anticipate price changes. Retail orders are characterized as less toxic on average, although the paper's conceptual Figure 1 explicitly permits variation within each investor group.

On an anonymous exchange, liquidity providers cannot simply offer each incoming investor a price based on that investor's identity. They compensate for the mix of flow they expect to receive. A wholesaler that contracts with a retail broker can identify a less adverse selection intensive stream before execution. It can give the customer an execution inside the displayed spread and still retain more expected trading revenue than it would earn against an otherwise comparable exchange order. Part of that surplus can fund payment for order flow, or PFOF, to the broker.

This explanation does not require illegal front-running. The source explicitly rejects that as a general characterization of wholesaling. It also does not imply that every wholesaler execution is optimal. Broker payments, quoted-price improvement, execution probability, inventory costs, and the opportunity to expose an order to competition all matter. Technology, financing, regulatory capital, personnel, and other costs are acknowledged but not estimated in the paper's adverse-selection exercise.

The source identifies Citadel, Virtu, Susquehanna, Two Sigma, and Wolverine as the five wholesalers used in its Rule 605 calculations. Its December 2020 data attribute about half of those five firms' retail flow to Citadel and another 26% to Virtu. These are sample-period descriptions. They are not a census of every retail transaction, especially because the reporting regime then omitted odd-lot orders.

## Define the execution metrics before comparing venues

Let $B_j$ and $A_j$ be the national best bid and offer immediately associated with execution $j$, $S_j=A_j-B_j>0$ the full quoted spread, $M_j=(A_j+B_j)/2$ the midpoint, $P_j$ the execution price, and $v_j$ the number of shares. Let $q_j=+1$ for a marketable buy and $q_j=-1$ for a marketable sell. The paper's price-improvement convention can be written as

$$
I_j=\frac{S_j/2-q_j(P_j-M_j)}{S_j}.
$$

Thus a buy at the offer or a sell at the bid has $I_j=0$, and a midpoint execution has $I_j=1/2$. A buy inside a ten-cent spread, one cent below the offer, has $I_j=0.10$. This is an improvement relative to crossing the quote, divided by the full spread. It is not the proportion of the half-spread saved. The associated one-way midpoint cost is

$$
C_j=q_j(P_j-M_j)=S_j(1/2-I_j),
$$

and the conventional effective spread is $2C_j$. Figure 4 on page 8 makes the full-spread denominator explicit. This accounting is necessary because the paper sometimes uses the more conversational phrase “spread saved.”

For a retained set of executions, the source uses a share-weighted average of individual improvement ratios:

$$
\overline I=\frac{\sum_jv_jI_j}{\sum_jv_j}.
$$

This average is not generally equal to total dollar improvement divided by total spread dollars. A researcher should calculate both if the intended objective is actual trading expenditure. Differences in stock price, spreads, share volume, and venue mix can change the relation between them.

The wholesalers' 24.5% figure comes from December 2020 Rule 605 reports, restricted to market orders and marketable limit orders. Zero-improvement executions are included. The authors remove negative-improvement observations for both wholesalers and exchanges, attributing many to out-of-order consolidated trade reporting. Approximately 4% of shares in the 605 reports are removed by this rule. This cleaning choice is consequential: the retained average describes zero-or-positive improvement after exclusion, not an unconditional execution-quality statistic. The PDF does not establish that every removed negative observation was a reporting artifact.

The exchange benchmark uses TAQ executions during December 7–11, 2020. Each trade is matched with the prevailing NBBO; trades are separated into exchange and off-exchange categories. Negative improvement is excluded and positive or zero improvement is share weighted. The one-week TAQ window is not identical to the full-month wholesaler-report window. The source says results vary little across weeks but provides neither a time-series sensitivity table nor uncertainty bands to support that assertion quantitatively.

A complete replication needs the archived Rule 605 records, TAQ trade and quote data, security mappings, exchange identifiers, timestamps, trade-condition filters, correction handling, and a trade-direction rule. The supplied PDF does not provide executable code or all these conventions. In particular, locked or crossed quotations, ambiguous trade sides, stale quotes, and how close timestamps are resolved require explicit implementation choices. Filling these gaps silently can materially change an intraday comparison.

## Hidden liquidity and the observed improvement results

The NBBO does not summarize every executable price. Hidden exchange orders can rest inside it, and the paper's historical reporting setup excludes odd-lot quotes from the displayed national benchmark. Midpoint liquidity in alternative trading systems supplies another possible execution opportunity. Pages 8–10 argue that using only the displayed quote therefore overstates the incremental value of wholesaling.

Figure 5 reports 24.5% for the five wholesalers and 8.7% for exchange executions. Their difference is 15.8 percentage points of the full spread. It is not a 15.8% relative reduction in an investor's total trading cost. Reweighting exchange stock-level improvement by retail share volumes from the five wholesalers produces 7.9%, rather than 8.7% (page 9, footnote 12). This alternative addresses part of the security-composition mismatch but does not compare the same orders randomly routed to different venues.

Figure 3 also separates the frequency of receiving any improvement from its magnitude. Wolverine has a high frequency but a much smaller average improvement than the other displayed wholesalers. Counting improved orders alone can therefore rank execution providers differently from measuring their economic value. The chart gives approximate bar heights rather than a numeric firm-level data table; the aggregate 24.5% is the reproducible printed headline.

The appendix on page 20 directly addresses the odd-lot mismatch. Wholesaler 605 statistics exclude odd lots under the reporting requirements discussed in the paper, whereas the primary exchange calculation includes them:

| Execution group | Improvement including odd lots | Excluding odd lots |
|---|---:|---:|
| Exchanges | 8.7% | 8.2% |
| All off-exchange TAQ executions | 17.9% | 17.8% |
| S&P 100 group, exchanges | 8.7% | 8.2% |
| S&P 500 group, exchanges | 10.1% | 9.5% |
| Russell 1000 group, exchanges | 10.7% | 10.1% |
| Russell 2000 group, exchanges | 10.2% | 9.6% |

All percentages here use the full NBBO spread denominator. The 17.9% off-exchange statistic is not the 24.5% retail-wholesaler statistic: the former includes other off-exchange activity. Figure 7 describes the index groups as the S&P 100 and the remaining larger index constituents, implying disjoint liquidity buckets rather than four independent overlapping universes. An implementation needs constituent dates and the exact membership hierarchy, which the PDF does not supply as files.

Price buckets in the appendix show exchange improvement rising from 5.9% for stocks priced below one dollar to 14.8% in the \$500–\$1 million bucket. Excluding odd lots leaves 5.9% at the bottom and 12.6% at the top. The intermediate including/excluding pairs are 6.6/6.6 for \$1–5, 6.9/6.8 for \$5–10, 8.3/8.1 for \$10–50, 11.0/10.5 for \$50–100, and 12.4/11.3 for \$100–500. Odd-lot treatment matters more in expensive shares, but the exchange improvement does not disappear after their removal.

Retail trading also differs by security composition. Figure 7 puts over 37% of the sampled retail shares in the Russell 2000 bucket, compared with about 30% of total-market shares. The retail series there includes both marketable flow and limit orders, while total-market volume includes retail activity. It is not a comparison of retail with a mutually exclusive institutional sample.

The authors additionally report that their own algorithms obtain midpoint executions roughly 10% of the time when sending immediate-or-cancel orders to ATSs before accessing exchanges. This is an operational observation, not a disclosed retail-routing experiment. Its sample, conditional execution probabilities, selection policy, fees, latency cost, and opportunity cost are absent. It motivates another execution route but cannot simply be added to the 8.7% benchmark as a guaranteed saving.

## Signed markouts and the counterfactual spread calculation

Pages 11–13 measure adverse selection with the midpoint change after subsequent transactions. A convenient positive-cost convention, opposite to the negative values plotted in the source, is

$$
D_j(k)=q_j\frac{M_{j+k}-M_j}{S_j}.
$$

An incoming buy followed by a rising midpoint gives $D_j(k)>0$, a loss for its passive seller. An incoming sell followed by a falling midpoint also gives positive cost for the passive buyer. The index $k$ counts later trades in the stock, not seconds. Thirty trades represent a longer clock-time exposure in less active securities. The paper uses this as a proxy for an inventory horizon after the plotted average price movement approximately levels off; it does not estimate actual inventory holding periods.

For exchange executions, the central calculation uses round-lot executions at the NBBO during continuous trading. Figure 8 shows adverse selection growing with the horizon and reaching 60.64% of the contemporaneous full spread after 30 trades. The curve continues changing slightly beyond 30, so “levels off” is an approximation. A footnote says these adverse-selection calculations use earlier TAQ results from August 2020, whereas the volume inputs use December 2020. The calculation is thus assembled from different periods, rather than a single synchronized panel.

TAQ does not label every off-exchange trade as retail. The authors identify off-exchange sub-penny executions, excluding midpoint executions, as a retail proxy. Their example is a price such as \$10.0122. This relies on the routing and pricing distinctions described in the source. It misses retail executions without fractional-price improvement and may not capture the distribution of all retail orders. It should be replicated as a classification rule and stress tested, rather than treated as observed investor identity.

For Russell 3000 stocks, Figure 10 reports 30-trade retail-proxy adverse selection of 11.92% of the spread, compared with 60.64% for the exchange group. This large descriptive difference supports the view that the privately routed stream is less toxic. It does not by itself identify what either group's markout would be after routing changes.

Figure 9 adds cross-sectional evidence: adverse selection measured in price basis points differs greatly across liquidity groups, around 0.8 basis points for the S&P 100 and 6.1 for the Russell 2000 at the cited horizon, while normalization by the spread makes the curves more similar. Its “all trades” comparison is not an identical sample to the at-NBBO round-lot series in Figure 8. More fundamentally, similarity across liquidity buckets is not a causal elasticity estimate. The step from these plots to a one-for-one proportional response of spreads to toxicity is an assumption of the counterfactual.

The paper's numerical mixture uses exchange volume $V_E=113.21$ billion shares and retail-wholesaler volume $V_R=53.14$ billion shares, with $a_E=0.6064$ and $a_R=0.1192$ for the two normalized adverse-selection measures:

$$
a_{\mathrm{mix}}=\frac{V_Ea_E+V_Ra_R}{V_E+V_R}=0.4507654.
$$

Under the assumed proportional spread response,

$$
\delta=1-\frac{a_{\mathrm{mix}}}{a_E}=0.2566533.
$$

This independently evaluated arithmetic reproduces the printed 45.08% mixed adverse selection and approximately 25.66% spread decline. Retail volume is 46.94% of the exchange volume, but only about 31.94% of the combined counterfactual flow. Confusing these two denominators overstates the mixing effect. Figure 11 places the five wholesalers at 21.9% of total market volume, on-exchange continuous trading at 46.7%, exchange auctions at 7.5%, and other off-exchange trading at 23.8%.

The mixture holds flow volumes and group characteristics fixed, combines normalized quantities across securities, and assumes the new flow reaches the relevant public liquidity providers without changing its information content. It does not model wholesalers' exchange hedges, inventory adjustment, routing substitution, changes in order submission, commissions, or endogenous entry. It also does not estimate the constant or slope of a spread-cost regression. A credible policy simulation would need to track those mechanisms and avoid double counting any existing exchange volume induced by wholesale activity.

## A necessary conversion to one-way investor costs

The statement that a 25.66% quote-spread decline eclipses the roughly 15% incremental price improvement does not follow directly from the printed quantities. This is a dimensional qualification derived here from Figure 4's convention, not an official correction or an estimate of the true equilibrium effect.

Consider a common old spread $S$ and a midpoint that does not move. At 24.5% improvement, current wholesale execution costs $0.255S$ relative to the midpoint. Suppose the new exchange spread is $(1-\delta)S$ and exchange price improvement remains 8.7% of that new spread. Then

$$
C_W=(0.5-0.245)S=0.255S,
\qquad
C_E^{\mathrm{new}}=(0.5-0.087)(1-\delta)S.
$$

At the paper's $\delta=0.2566533$, this gives $C_E^{\mathrm{new}}\approx0.3070S$, above $0.255S$. Under these deliberately simple assumptions, exchange execution becomes cheaper only when

$$
\delta>1-\frac{0.255}{0.413}\approx38.26\%.
$$

If instead the absolute exchange improvement stays fixed at $0.087S$ of the old spread, the threshold is 31.6%, still above 25.66%. These examples show why an actual retail-cost prediction requires a joint model for spreads, midpoint locations, inside-spread liquidity, and execution prices. They do not refute the claim that public spreads could narrow or establish that current wholesaling is optimal. Other changes, including additional competition and midpoint access, could change the outcome. The PDF's mixture alone does not quantify them.

The source's final retail-discount analogy is rhetorical rather than a calibrated welfare calculation. Avoid replacing transaction-level costs with that analogy, and avoid multiplying a share-weighted average percentage by total dollar turnover without retaining the relevant stock-level spreads.

## Private information, concentration, and limit-order incentives

Pages 14–17 propose a second channel beyond removal of benign marketable flow. Wholesalers observe private retail orders, including limit orders later routed to exchanges, and institutional immediate-or-cancel inquiries sent to their electronic liquidity provider programs. Even an unfilled inquiry may reveal part of a larger trading program. A firm using those observations can improve its quotes when the expected price move is favorable and withdraw when it is unfavorable. Other passive traders may then face a worse residual mix of executions.

This is a plausible selection mechanism, but the PDF provides no structural equilibrium or identified estimate of its contribution to spreads. Its policy conclusion that information asymmetry reduces competition is stronger than the direct empirical evidence. Observing private flow can coexist with price discovery and competition; measuring the net effect requires a comparison that the paper does not implement.

Figure 12 illustrates concentration using ten Russell 2000 stocks in which Citadel's retail executions are large relative to exchange continuous-session volume. The reported range is 69%–188%. Ratios above 100% are possible because the denominator is a different venue's volume; they are not shares of total market volume. The chart's second series uses total market volume and is correspondingly smaller. Reading the two denominators interchangeably would turn the concentration argument into an arithmetic impossibility.

The closest statistical check appears in footnote 18 on page 16. Fifty-four Russell 2000 stocks, approximately 3%, had a wholesaler exceeding 20% of total stock volume in December. Their average quoted spread was 88 basis points, versus 63 where no wholesaler exceeded that threshold. The authors report a statistically significant two-sample t-test but supply no test statistic, p-value, uncertainty interval, or controls. They expressly acknowledge that other stock characteristics are not held fixed. Illiquidity may attract particular routing patterns as well as result from them, so this comparison is not causal evidence of a 25-basis-point concentration penalty.

For retail limit orders, the mechanism differs from that for marketable orders. The paper describes nonmarketable orders being sent to exchanges, sometimes through wholesalers, where they face more toxic counterparties and potentially lower fill rates. The source says about 13.7% of retail execution volume in its December wholesaler reports consisted of limit orders. It does not provide a matched sample estimating fill probability, queue position, adverse selection, or opportunity cost for those retail limit orders. A conclusion about their net execution quality remains a hypothesis requiring order-level data.

The proposed reforms include limiting PFOF or wholesale participation, introducing more order-level competition, and making venue rules more homogeneous. Those are recommendations, not backtested strategies or evaluated interventions. The paper discusses fractional pricing, displayed quote protection, and routing in broad terms; even internally, its page 7 wording shifts between restrictions on order prices and execution prices. The measurement logic should be taken from the explicit sample definitions, without using this discussion as a comprehensive legal specification.

## Reproduction plan and evidentiary limits

A useful first implementation would reproduce the historical descriptive tables before simulating a rule change. Archive the five December 2020 Rule 605 files, obtain TAQ for December 7–11 and the August period used for markouts, and fix constituent membership and stock-price buckets. Reconstruct quotes, identify aggressor sides, retain venue and lot-size flags, and report the percentage of data removed by every filter. Calculate improvement both with all valid observations and with the paper's negative-improvement exclusion. Preserve share-weighted ratios and dollar-weighted costs as separate outputs.

Next calculate markout curves at the displayed trade-count horizons for exchange-at-NBBO round lots and for the off-exchange fractional-price retail proxy. Specify whether later trades count across all venues, and how trading-day boundaries are handled; the PDF does not provide those details. Reproduce the liquidity-group curves, distinguish their samples, and inspect security-level variation rather than only aggregate means. Cluster or resample at an appropriate stock-day level if estimating uncertainty, because trade observations are strongly dependent. Such inference would extend the paper, which supplies no confidence intervals for the main estimates.

Finally, reproduce the volume-weighted mixture as an accounting benchmark and introduce explicit counterfactual assumptions one at a time. Recalculate one-way costs using the full-spread convention, permit inside-spread liquidity to change, model fees and commissions, and test whether the flow proxy's toxicity remains stable across securities and time. Public-market spread narrowing, a retail execution benefit, broker revenue loss, and total welfare are separate outcomes. This source is most useful for formulating those measurements and exposing benchmark endogeneity; its aggregate mixture is insufficient to settle all of them.

All 20 supplied pages, including the appendix and source footnotes, were read. Critical visual checks covered the title, Figures 1–12, the mixture equation and percentage calculation, and the appendix tables. Raw TAQ records, archived reporting files, code, security lists, and a full equilibrium response are absent from the local source. No performance, statistical confidence, or regulatory effect beyond what the PDF supports is inferred here.
