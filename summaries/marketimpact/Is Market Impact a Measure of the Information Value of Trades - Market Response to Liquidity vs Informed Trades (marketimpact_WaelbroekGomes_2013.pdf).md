# Is Market Impact a Measure of the Information Value of Trades? Market Response to Liquidity vs Informed Trades

**Authors:** C. Gomes and H. Waelbroeck, Portware LLC. **Source:** `Finance/marketimpact_WaelbroekGomes_2013.pdf`, 46-page working-paper version, SSRN abstract 2291720. The local filename labels the work 2013; the provided first page does not print a version date. References below use PDF/printed pages. **Type:** empirical research on institutional metaorders, information, and price reversion.

## Research question and distinctive contribution

The paper separates two statements that are often combined under the term market impact: an order moves prices while it is being executed, and some of that displacement remains after execution ends. Using institutional order-management-system records, the authors compare trades labeled as cash-flow transactions with other institutional trades. The cash-flow label identifies orders generated to invest inflows or fund outflows, providing an unusually direct proxy for lower-information trading rather than relying only on stock characteristics or inferred trade motives.

Their main finding is that cash-flow trades and other trades have statistically similar impact shape and scale during execution, once trading difficulty is taken into account, but sharply different subsequent price paths. Cash-flow impact largely reverses within two to five days. Other trades, on average, reverse only enough to bring the post-reversion price close to the average execution price. The latter pattern is compatible with fair pricing, the hypothesis that implementation shortfall equals the persistent displacement for each size of institutional metaorder.

The distinction supports a mixed interpretation of market impact. Anonymous order-book interaction can generate similar contemporaneous price pressure for trades with different motives. Later prices can nevertheless reflect differences in the information underlying those trades. The authors conclude strongly that persistent impact reflects information rather than a mechanical permanent effect of arbitrary trades. The evidence supports differential reversion by motive; it does not by itself prove that every uninformed trade in every market has exactly zero long-run causal effect.

The study also tests how metaorder characteristics relate to departures from fair pricing. New positions, Nasdaq stocks, and orders combining several portfolio managers are associated with greater post-reversion gains for the institution. Trading after favorable intraday momentum, adding to improve an existing position's average entry price, and trading large-cap names are associated with gains for liquidity providers instead. These are conditional average associations with very low explanatory power, not a high-accuracy classification system for informed trading.

## Economic framework and testable restrictions

The theoretical discussion contrasts information-based pricing models with mechanical order-book models (pp. 2–8). In information models, a transaction changes beliefs about future value. In mechanical models, the order consumes available liquidity and can move the reference price even if the order has no special information. Both classes can produce concave impact, so observing a square-root curve during execution does not distinguish them well.

Fair-pricing theory, associated with Farmer, Gerig, Lillo, and Waelbroeck, considers investors reacting to a shared signal whose orders are aggregated and executed over time. Competition leads to order sizes for which expected average execution price matches the price after reversal. For a metaorder-size survival distribution with exponent $\beta$, the model predicts impact exponent $\delta=\beta-1$. With $\beta=1.5$, impact is square root in size, peak impact is 1.5 times average execution shortfall, and one-third of peak impact reverses.

The relationship follows directly if the marginal execution-price displacement is proportional to $q^{\beta-1}$ as cumulative quantity $q$ is executed:

$$
\frac{I_{\mathrm{peak}}(Q)}{I_{\mathrm{avg}}(Q)}
=\frac{Q^{\beta-1}}{Q^{-1}\int_0^Q q^{\beta-1}\,dq}=\beta.
$$

This formula links the shape of the execution path with the ratio of endpoint to average cost. It does not independently establish what happens after trading stops. Fair pricing adds the restriction that the post-reversion displacement equals the average cost.

The paper distinguishes unconditional breakeven from fair pricing. Breakeven requires zero mean mark-to-market trading profit after reversion across the aggregate sample. Fair pricing requires that result conditional on trade size or difficulty. A mixture of profitable and unprofitable size groups can satisfy unconditional breakeven while violating fair pricing. Accordingly, the empirical work examines both overall averages and size-related bins.

The information at issue is explicitly short-term information associated with the timing of a decision. The authors do not test whether the portfolio manager's months- or years-long investment thesis is profitable. An order can have no short-term mark-to-market profit after impact and still earn a positive return over a much longer holding period. Nor is zero marked profit equivalent to zero round-trip trading cost, because eventual liquidation requires another execution.

Mechanical-model predictions overlap numerically with fair pricing over the available uncertainty range. The paper discusses an alternative model predicting impact exponents around 0.55 to two-thirds and about 25% reversal in one parameter region. The data cannot cleanly reject that degree of reversal in favor of exactly one-third for ordinary trades. The stronger discriminating observation is the much deeper reversal of the labeled cash-flow subset.

## Data origin and construction of metaorders

The original records come from institutional clients' order management systems and were supplied to study portfolio-manager alpha profiles and execution scheduling. They include portfolio-manager identifiers, order identifiers, creation times, and usually timestamps, prices, and quantities for partial fills. Most managers' orders have a cash-flow flag supplied by the portfolio-management system. Some managers lack this flag, so the “other” category may contain unlabeled cash-flow trades (p. 9).

A raw OMS order is not necessarily the right economic unit. A manager can split a decision into blocks, or several managers within one firm can react to shared research. The market sees their combined anonymous flow. The authors therefore merge orders in the same stock and direction when the same manager places them on the same or consecutive open-market days. Orders from different managers at the same firm are merged if placed within 60 minutes of one another, counting only open-market time. Cash-flow orders are combined only with other cash-flow orders (pp. 9–10).

These rules permit metaorders to span multiple days and multiple portfolio managers, but only within a firm. The aggregation is intended to approximate the persistent flow perceived by market participants. It cannot observe the full market-wide metaorder if managers at other firms react to the same signal. This missing component later matters for interpreting momentum and multi-manager effects.

The OMS often resets the original requested quantity to the amount actually filled. Consequently, unfilled-share information is unreliable. The study analyzes executed metaorders rather than the full intended trading decision, including missed or canceled opportunities. The source later provides an example of a limit-constrained manager whose small partial fills are excluded by the size filter, producing a selection effect in measured performance.

The constructed sample initially contains 129,944 metaorders above 1% of average daily volume, from 112 portfolio managers or strategies at several large asset managers, covering July 2009 through March 2012. Approximately one-quarter are labeled cash flows. Further filters retain duration of at least five minutes, participation below 50%, initial price at least \$1, and annualized volatility at most 200%. The retained sample comprises 27,591 cash-flow trades and 87,658 other trades, a total of 115,249 observations (pp. 11–12).

Average daily volume is a trailing 30-day average of regular-hours share volume. Volatility is based on the preceding 90 days of close-to-close returns and expressed as an annualized percentage. Spread is the average nonzero bid-ask difference at the start and end, in basis points; if both observations are crossed, a nearby metaorder's spread is substituted. These conventions affect both the difficulty normalization and the regression covariates.

## Descriptive differences and comparability

Cash-flow and other trades are not naturally matched samples. The median cash-flow size is 2.2% ADV, compared with 5.1% for other orders; means are 4.7% and 15.1%. Median shares executed are 8,167 versus 61,100. Mean execution duration is 4.41 hours for cash flows and 6.01 hours for other orders, with medians 3.28 and 4.38 hours. Mean participation is 6% versus 13% (Table 1).

The stocks also differ. Cash-flow trades have median ADV 285,000 shares, compared with 984,000 for other trades, and median spread 12.04 versus 6.65 basis points. Mean annualized volatility is 39.61% versus 35.84%. Thus cash-flow trades are typically smaller and more patient, but often occur in less liquid stocks. Comparing raw average shortfalls alone would conflate trading motive with these differences.

The authors address comparability by scaling difficulty with volatility and square root of relative size, using beta-adjusted returns, and running regressions with stock and order controls. They do not claim a randomized experiment or a fully matched causal design. Differences in asset-manager composition, cash-flow tagging, urgency, order handling, and latent information can remain after the reported controls.

## Return measurement and continuing-order adjustment

For each metaorder, the arrival benchmark is the midpoint at the start of its first segment; the end benchmark is the midpoint at the last fill of its final segment. Realized shortfall uses the average execution price. Returns are signed so that price movement in the trade direction is positive. The study measures arrival-to-close returns on the completion day and one, two, five, and ten trading days afterward.

Subsequent orders in the same stock and firm can bias these post-trade returns. About 80% of metaorders have later add-ons, which are more likely to continue the same direction and occur after an improved price. Restricting the sample to orders without add-ons would both discard most observations and introduce selection. The authors instead subtract estimated effects of the subsequent buy and sell quantities (pp. 10–11).

The calibrated impact function is

$$
\operatorname{impact}(Q)=2.8\,\sigma_{\mathrm{ann},\%}\sqrt{Q/\mathrm{ADV}},
$$

in basis points, with annualized volatility entered in percentage units. The factor 2.8 is chosen so average predicted impact equals mean realized shortfall in the sample. This calibration is a modeling input to the subsequent-flow correction; it is not a structural parameter estimated separately for every order.

Let $Q_B^{(t)}$ and $Q_S^{(t)}$ denote cumulative subsequent buy and sell shares through the measurement date. The paper's positive-reversion convention is

$$
\operatorname{Reversion}_t=\epsilon\left[10{,}000\log\left(\frac{P_{\mathrm{end}}}{P_{\mathrm{close},t}}\right)+\operatorname{impact}(Q_B^{(t)})-\operatorname{impact}(Q_S^{(t)})\right].
$$

The trade sign multiplies the entire bracket, including the buy/sell impact adjustment. Visual inspection of the source equation confirms this detail. The impact function is applied separately to cumulative buys and cumulative sells, not to their net quantity and not simply summed across square roots of every child order. A faithful reproduction must preserve this nonlinear aggregation rule.

This adjustment is consequential and assumption dependent. It attributes subsequent observed flow according to a square-root model calibrated to shortfall, without separately observing the counterfactual price path. It cannot remove trades at unobserved firms. The paper therefore reports results without the adjustment in Appendix B, allowing the reader to see how much of the fair-pricing result depends on continuing-flow attribution.

## Market adjustment and primary average results

The beta adjustment subtracts the stock's beta times the S&P 500 move over the relevant window. For shortfall, it subtracts one-half of the signed beta-scaled start-to-end market return, assuming execution is uniform and market drift approximately linear. For peak impact and subsequent close returns, it subtracts the full beta-scaled market move over the full benchmark window (p. 13). The PDF explains the logic but does not provide a complete beta-estimation protocol or a released implementation.

The primary numerical contrast is substantial:

| Beta-adjusted measure, basis points | Cash-flow trades | Other trades |
|---|---:|---:|
| Average shortfall | 24.01 | 34.85 |
| Peak impact | 27.26 | 48.18 |
| Completion-day close | 15.35 | 41.92 |
| One day later | 10.00 | 38.16 |
| Two days later | 7.85 | 34.49 |
| Five days later | 0.89 | 32.22 |
| Ten days later | -13.43 | 33.02 |

For other trades, arrival-to-price displacement at two days is 34.49 basis points, within 0.36 basis points of the 34.85 shortfall. The difference has bootstrap standard error 1.12 basis points and is not statistically significant. At five and ten days, differences from shortfall are -2.62 and -1.83 basis points, also not significant at the reported threshold. This is the central unconditional breakeven evidence (Table 2b, pp. 13–14).

Cash-flow trades instead lose marked value after completion. Their five-day arrival-to-price displacement is only 0.89 basis points, so almost all the initial price displacement has disappeared while the 24.01-basis-point execution shortfall remains a cost. Their marked profit relative to execution is -23.12 basis points, standard error 3.09. At ten days the price has moved beyond the initial benchmark in the opposite direction, giving -37.44 basis points relative to shortfall, standard error 4.27.

More than complete reversal does not imply the original trade mechanically created a negative terminal price effect. It may reflect reversal of other firms' earlier correlated cash-flow trades or common market conditions. The authors use it as evidence against a positive permanent mechanical component for the labeled sample, while acknowledging the broader aggregation problem.

Unadjusted returns tell a similar qualitative story but differ in level. Cash-flow shortfall is 27.22 basis points and peak impact 33.66; other-trade shortfall is 33.24 and peak impact 44.95. Beta adjustment is especially important for cash-flow orders because their unadjusted prior momentum is much larger, approximately 46 basis points versus 12 for other orders, but becomes about 10 versus 11 basis points after adjustment. The market component therefore explains much of that initial difference.

## Duration-dependent reversion and fair pricing by difficulty

Longer executions require a longer observation window before comparison with the average fill price. For non-cash-flow trades, the authors form four duration groups: less than half a day, half a day through two days, two through five days, and above five days. Sample sizes are 34,384, 45,393, 6,456, and 1,425 (Table 3).

Average beta-adjusted shortfalls in these groups are 22.72, 37.73, 66.33, and 93.54 basis points. Peak impacts are 30.43, 51.88, 95.67, and 143.75. The endpoint closest to the average execution price generally occurs later for longer executions. The study uses next-day close for the shortest group, day two for the second, day five for the third, and day ten for the longest when constructing its fair-pricing tests (pp. 15–18).

This is an empirically motivated convention, not an exact estimated law that reversion time equals execution duration in every case. For trades longer than five days, the mean displacement remains 18.78 basis points above shortfall at day two and 10.43 at day five, but the standard errors, 11.8 and 15.4 respectively, are too large to reject zero. At day ten the difference is -0.37 with standard error 18.4. Failure to reject at the earlier horizons therefore need not mean reversion was already complete.

The fair-pricing graph groups orders by expected shortfall from the calibrated impact model, combining volatility and relative size into trading difficulty. Average observed shortfall and duration-appropriate post-reversion return track one another across the displayed groups. The authors cannot reject equality within any difficulty range. That is stronger than a single pooled mean, but it remains a conditional test using broad bins and data-selected observation conventions.

For cash flows, the corresponding graph shows much deeper reversal. Most difficulty groups have little remaining impact; in an intermediate difficulty region roughly 30–60 basis points, some residual displacement remains, but the institution still loses a sizable fraction of its execution cost. The longest-duration cash-flow groups are small: only 1,293 observations at two to five days and 142 above five days. Appendix A consequently contains large errors and does not support uniformly precise motive comparisons in those tails.

## Deviations from fair pricing

The regression outcome is the liquidity provider's beta-adjusted marked profit, defined as shortfall minus post-reversion arrival return. Positive coefficients mean that the institution loses more to liquidity providers; negative coefficients mean the institution retains more marked profit. This sign convention is the reverse of discussing the portfolio manager's own P&L and must be kept explicit (pp. 19–22).

Regressors include square root of relative size, volatility, spread, market-capitalization indicators, buy direction, Nasdaq listing, aggregation across multiple portfolio managers, trade-origin categories, and signed beta-adjusted intraday momentum before order arrival. Trade-origin categories use the preceding three months of the firm's orders. A new trade has no prior same-manager metaorder in that stock; price-improvement trades add in the same direction at a better price; profit-taking and stop-loss labels represent other relationships to earlier positions.

For non-cash-flow trades, the multi-manager coefficient is -12.98 basis points, standard error 2.61; Nasdaq is -9.98, standard error 2.97; and new trade is -8.18, standard error 3.09. Price improvement is +7.43, standard error 2.99; large cap is +8.57, standard error 3.77. Momentum has coefficient +0.15 with standard error 0.02 in the paper's basis-point scaling. Relative size is not significant in this group, consistent with fair pricing holding across difficulty after other controls.

For cash flows, the square-root-size coefficient is +71.69, standard error 36.1, indicating larger liquidity-provider gains for larger cash-flow transactions. The numerical scale depends on expressing relative size as the paper does; it is not a per-percentage-point coefficient without conversion. Cash-flow profit-taking and stop-loss coefficients are negative and significant, while most other controls are not statistically distinguished from zero.

These regressions explain very little individual variation: $R^2$ is 0.002 for cash flows and 0.009 for other trades. The large sample allows statistically significant group means despite almost all order-level P&L remaining unexplained. A reader should not translate these associations into a deterministic trading recommendation or infer that exchange listing itself causes information advantage.

The paper offers plausible mechanisms rather than separately tested structural explanations. Multi-manager orders may reflect shared internal research, or unobserved contemporaneous demand elsewhere. Prior momentum may identify an institution arriving late to a broader market-wide metaorder, after earlier participants have captured the advantage. Price-improvement trades can add capital to a previous thesis after the market has moved against it. Each story is compatible with the signs, but the data do not uniquely select among them.

## Impact shape during execution

The authors compare peak impact with expected average shortfall from the square-root difficulty model. With a square-root trajectory, peak impact should be about 1.5 times expected average cost. Bins contain at least 200 cash-flow observations and at least 600 other observations. The cash-flow and other curves are statistically indistinguishable, and both are compatible with the 1.5 line (pp. 23–24).

This comparison explains why raw mean peak impacts differ even though the paper concludes the impact mechanisms look similar during execution. Cash-flow orders and other orders have different size, volatility, and liquidity distributions. The relevant test compares impact at similar modeled difficulty rather than comparing their unconditional average peaks. The data do not rule out nearby power exponents, so “consistent with square root” is more accurate than “proves an exact one-half exponent.”

Appendix D removes the above-1%-ADV cutoff when examining distributions. Durations beyond one day have an approximate survival-tail exponent 1.8, corresponding to density exponent 2.8. Spikes at multiples of 390 minutes reflect preferences for opening and closing execution times. Non-cash-flow sizes normalized by ADV have an approximate tail exponent 1.5, extending to orders several times daily volume; cash-flow sizes are better described by a lognormal distribution over roughly 0.01% to 70% ADV.

Raw shares do not show the same clean distribution because stock liquidity varies. The authors also note that the manager sample is dominated by a few large firms, so it is not an unbiased sample of the distribution of institutional sizes. The similarity of execution impact across motives despite different size distributions is one reason they emphasize the coexistence of mechanical execution pressure and informational post-trade behavior.

## Robustness, identification limits, and implications

Appendix B quantifies the importance of continuing-order adjustments. Without them, other trades have beta-adjusted arrival returns of 41.76, 45.74, and 49.74 basis points at two, five, and ten days. Relative to the same 34.85 shortfall, these imply marked profits of 6.91, 10.89, and 14.89 basis points. The adjusted values are much closer to breakeven. Fair pricing for this subset therefore depends materially on how persistent subsequent trading is attributed, while the loss on cash flows remains visible with either convention.

Appendix C partitions observations by random groups, quarter, market volume, and size. It cannot reject breakeven in the displayed subgroups. However, the standard deviation of group-average liquidity-provider profit is 3.33 basis points for random groups and 7.74 for quarters, compared with 4.50 and 7.63 for small and large trades partitioned by volume. The larger temporal variation shows that naive random resampling can understate uncertainty associated with common market regimes. The source uses bootstrap errors but does not fully document a modern clustered resampling implementation.

Replication requires licensed OMS records with motive tags and manager/firm identifiers, fill-level data, quote and benchmark histories, and a complete account of aggregation and correction choices. It must preserve separate cash-flow aggregation, the open-market-time gap rule, the nonlinear correction of continuing buys and sells, and the duration-dependent endpoint mapping. Missing cash-flow flags, unreliable unfilled quantities, unavailable other-firm flow, and unspecified beta-estimation details are the principal barriers to exact reproduction and causal interpretation.

For portfolio construction, the paper warns that short-term information value may be consumed by implementation cost. A position marked at the average fill price after reversal has not generated a free trading gain, and closing it will add costs. For execution research, the useful conclusion is to estimate contemporaneous impact and post-trade information separately. An execution algorithm can face similar immediate liquidity costs for informed and cash-flow demand even though the correct longer-horizon benchmark differs substantially. The evidence supports this distinction more strongly than it supports any universal permanent-impact fraction or exact structural exponent.
