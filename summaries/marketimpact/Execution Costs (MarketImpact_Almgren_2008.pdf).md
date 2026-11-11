# Execution Costs

**Author:** Robert Almgren  
**Publication:** *Encyclopedia of Quantitative Finance* entry; dated 17 December 2008 (5 pages)  
**Source file:** Finance/MarketImpact_Almgren_2008.pdf

## Scope

A short encyclopedia note laying out how an investment process should handle execution costs, in the order they should be built (reverse chronological for a single trade): **post-trade measurement -> optimal trading -> pre-trade estimation**. Its quantitative core is a restatement of the Almgren--Thum--Hauptmann--Li (2005) impact model.

Definitions: execution cost = value difference between an ideal and the actual trade, typically average fill price (including commissions and fees) minus a benchmark, signed so positive = loss. Direct costs (commissions, taxes, fees) are predictable and usually left out of quantitative analysis; indirect costs (market impact, price motion from volatility) are harder to measure and the most improvable. Unexecuted shares must be assigned a value. Equity language is used because measurement there is most developed.

## Post-trade reporting

- **Benchmarks.** Arrival price (quote when the order reaches the desk) gives Perold's (1988) implementation shortfall. Interval VWAP filters out most volatility and so is popular for judging execution *quality*, but does not correspond to an investment goal. A post-trade price (e.g. the close) completes the before/during/after view.
- **Cost vs. decision quality.** Example: decision assumes purchase at yesterday's close of \$50, fill at \$50.25 -> 25 cents/share cost; if the stock closes at \$51 the trade was still good. Costs can be negative (price falls during a buy, or with a close benchmark). Single-order forecasts are dominated by volatility.
- **Aggregation.** Weight cents/share costs by shares, bp costs by dollar value, so the aggregate reflects portfolio value change. Report the size-weighted standard deviation alongside the mean: with SD 25 bp over 100 independent trades the mean has a standard error of 2.5 bp, so a 1--2 bp change is noise. The SD does not behave well under subdivision.
- **Subdivision dependence.** Arrival-price aggregates are not invariant to how blocks are split: 100,000 shares bought over the day against the open, vs. 40,000 in the morning plus 60,000 against a midday arrival price, give different (lower, in the example) reported cost. VWAP or a fixed-time benchmark (close) avoids this; which is right depends on the investor's goals.
- **Limits and incomplete trades.** A buy at \$50 limited to \$50.05 caps impact at 5 cents but may fill little. Marking unfilled shares at the close is the obvious rule but "far too stringent" and blind to why trading stopped; there is no simple rule, and reporting must reflect the whole investment process.
- Compare realized with pre-trade forecasts, per order and per portfolio, both to find bad executions and to keep the model calibrated.

## Optimal trading

- Primary objective: reduce mean cost (market impact plus uncaptured short-term alpha); secondary: reduce cost variance, which adds to investment risk (Engle--Ferstenberg 2007). Best execution is also a regulatory requirement.
- Seek liquidity in **space** (all venues, dark pools, block crossing; see Hasbrouck 2007 on US structure) and in **time** (slower trading lets counterparties arrive; absent significant short-term drift, slower is cheaper on average).
- Pressure to trade fast comes from anticipated drift and volatility (Alford--Jones--Lim 2003 quote on the impact/opportunity-cost trade-off). Portfolio schedules must account for correlations and may need to stay neutral to an index or factor throughout; schedules may adapt to observed liquidity.
- Mean--variance optimal schedules and expected-cost-optimal schedules under drift look alike: front-loaded, then slowing (Figure 1, from Almgren--Chriss 2000). The decisive variable is the **effective duration** $T_{\text{eff}}$ of a linear approximation to the trajectory -- minutes, hours or days -- and choosing it requires an at least approximate cost model.

## Pre-trade estimation

Inputs at minimum: shares $X$, daily volume $V$ (historical or same-day), effective duration $T$; for cross-sectional normalization, volatility $\sigma$ and possibly market cap, exchange/country; optionally expected short-term alpha and algorithm used. Nearest-neighbour or "supervised learning" (Poggio--Smale 2003) is impractical because the input space is too high-dimensional to find similar past trades, which argues for a parametric regression with standard significance tests.

Almgren et al. (2005) model, with arrival mid $S_{\text{pre}}$, average execution price $S_{\text{exec}}$, and $S_{\text{post}}$ shortly after completion (lagged to let transients dissipate). For a buy (signs reversed for sells):

$$I=\log\frac{S_{\text{post}}}{S_{\text{pre}}}\approx\frac{S_{\text{post}}-S_{\text{pre}}}{S_{\text{pre}}},\qquad J=\log\frac{S_{\text{exec}}}{S_{\text{pre}}}\approx\frac{S_{\text{exec}}-S_{\text{pre}}}{S_{\text{pre}}},$$

$$I=\gamma\,\sigma\,\frac{X}{V}+\text{noise},\qquad J=\frac{I}{2}+\eta\,\sigma\left(\frac{X}{VT}\right)^{\beta}+\text{noise},$$

with $T$ a fraction of the trading day, so $X/(VT)$ is the participation rate; the $1/2$ is the fraction of post-trade impact paid on the order itself; $\gamma,\eta$ are constant across stocks. Linear permanent impact is theoretically convenient and fit the 2005 data reasonably, though the note concedes other recent studies question it. Spread and market cap were not significant in US equities. Calibration is two-step (permanent first, testing linearity; then temporary for $\beta,\eta$), with residuals checked against volatility. Result: $\beta\approx0.6$, described as "roughly compatible" with square-root models (Barra 1997); trades of a few percent of ADV over several hours cost "tens of basis points".

Stated limitations: (1) $R^2$ of a few percent at best -- single-trade prediction is poor; (2) impact vs. alpha is not identified (did the price rise because of the buying, or was the buying a correct forecast?); (3) models fit on small trades perform poorly on large ones despite claiming universality. Users should critically evaluate, recalibrate and extend; the model is still very useful for pre-trade planning, scheduling and post-trade evaluation.

## Notes against the source paper

- The permanent-impact formula here omits the 2005 paper's liquidity factor $(\Theta/V)^{1/4}$ (shares outstanding over ADV), so the published $\gamma=0.314$ is not directly usable in the simplified formula; for a typical large cap with $\Theta/V\approx100$ the implied coefficient is about $0.314\times100^{1/4}\approx1.0$. The 2005 values are $\eta=0.142$, $\beta=0.6$.
- Here $\beta\approx0.6$ is called "roughly compatible" with the square root, whereas the 2005 paper reports rejecting $\beta=1/2$ at 95%. Both statements are fair: the difference is statistically detectable yet economically modest.
- Sanity check on "tens of bp", using the 2005 coefficients (own arithmetic): $\sigma=2\%$, $X/V=3\%$ over $T=0.3$ day (participation 10%), $\Theta/V=100$: temporary $0.142\times0.1^{0.6}\times200\text{ bp}\approx7$ bp; permanent $I\approx1.0\times0.03\times200\approx6$ bp, of which half is paid; total $J\approx10$ bp. "Tens of bp" therefore fits higher-volatility names, larger sizes, or faster execution better than a typical large-cap case.

## Assessment

A clear, compact framing rather than new research. Most valuable parts for a quant PM: the aggregation rules (share vs. dollar weighting, always report size-weighted SD and the standard error), the non-invariance of arrival-price aggregates to order splitting, the emphasis on $T_{\text{eff}}$ as the first-order scheduling decision, and the frank statement of the model's three weaknesses. It is thin on anything beyond the permanent/temporary split: transient/propagator impact (Bouchaud et al. 2004) and the Lillo--Farmer--Mantegna master curve are mentioned only as "more subtle" models; there is no treatment of cross-impact, of non-equity markets, or of a principled rule for valuing unfilled shares. The calibration is the 2001--2003 Citigroup US large-cap sample and should be re-estimated on one's own fills.
