# Interest rate risk in low-volatility strategies

David Blitz, Bart van der Grient, and Pim van Vliet. Robeco research white paper, June 2014. [Source PDF](../../Finance/AbnormalReturnsVolatility_Vliet_2014.pdf). All nine PDF pages were read, including the concluding disclosures; the empirical exhibits on PDF pages 3–5 were checked visually. The substantive analysis occupies approximately six pages, so this note focuses on its complete evidence rather than adding a longer model that the authors did not supply.

## Why this matters

Low-volatility equities can behave partly like bonds. An investor who already owns government duration may therefore acquire more interest-rate exposure when moving an equity allocation toward low-volatility stocks. Blitz, van der Grient, and van Vliet ask whether this exposure explains the strategy's historical risk-adjusted advantage, whether an enhanced stock-selection process reduces it, and whether the exposure persists over longer horizons.

Their answer is qualified: low-volatility strategies have greater bond sensitivity than the broad equity market, but neutralizing the incremental sensitivity in a long U.S. history leaves most of their Sharpe-ratio advantage intact. A strategy combining low volatility with valuation and momentum has somewhat less bond sensitivity than a generic low-volatility strategy. In a shorter global sample, rolling three-year alpha has a weaker association with bond returns than rolling one-year alpha, particularly for the enhanced strategy.

These findings address exposure attribution and portfolio construction. They do not establish that future rate increases will produce a particular loss, that all low-volatility products share a stable duration, or that bond hedging can be implemented at the historical cost implied by a frictionless return overlay. The document is also research from the manager of one of the strategies being compared. Its useful numerical comparisons coexist with substantial undisclosed implementation detail.

## What “bond-like” means in this setting

The paper discusses several possible connections between low-risk stocks and bonds. Mature, stable businesses can have relatively predictable cash flows. Discount-rate changes can move their valuations in the same direction as bond prices. Changes in risk aversion can also produce common demand for defensive equities and government bonds. Higher-volatility equities may resemble options on firm assets, with different rate sensitivities. The paper draws on these intuitions and related literature; it does not estimate a structural cash-flow-duration model or decompose the observed covariance among these mechanisms.

The measured exposure is a regression sensitivity to a government-bond return series. It is not a yield duration in years. A beta of 0.57 means a 1-percentage-point movement in the bond factor is associated with a 0.57-point movement in the equity strategy under the regression definition. It does not mean a one-point increase in yields lowers the strategy by 0.57%. Mapping a bond return to a yield change additionally requires the factor's duration, convexity, coupon carry, and yield-curve movement.

The equity market itself has positive bond beta in the long U.S. sample. Consequently the first hedge experiment removes only the exposure beyond that of the market. It is a comparison at equal bond sensitivity, not a construction with zero interest-rate risk. This is essential for interpreting the table: the hedged low-volatility portfolios still have bond beta 0.34.

## The long U.S. comparison

The first experiment uses U.S. equity history from January 1929 through December 2010. The generic low-volatility signal uses volatility over the preceding three years. The enhanced variant, called “Low vol+,” combines low volatility with valuation and momentum information. It resembles the authors' Conservative Equities approach but is simplified to accommodate the long historical sample. The paper does not provide a complete stock-selection formula, signal weights, constituent count, or optimization problem.

The bond factor is a 50/50 combination of Ibbotson intermediate-term and long-term government-bond return series. Exhibit 1 reports the following annual figures:

| Portfolio | Excess return | Volatility | Bond beta | Equity beta | Sharpe ratio |
|---|---:|---:|---:|---:|---:|
| Equity market | 5.2% | 19.0% | 0.34 | 1.00 | 0.28 |
| Low vol | 6.2% | 14.2% | 0.57 | 0.67 | 0.44 |
| Low vol+ | 8.5% | 14.6% | 0.51 | 0.66 | 0.58 |
| Low vol, bond exposure matched to market | 5.8% | 13.9% | 0.34 | 0.66 | 0.42 |
| Low vol+, bond exposure matched to market | 8.2% | 14.4% | 0.34 | 0.65 | 0.57 |

The source footnote says excess returns above the risk-free rate are computed on a compounded basis. The displayed Sharpe ratios are consistent, to rounding, with those annual excess-return figures divided by annual volatility. A replication should reproduce the paper's convention before comparing these ratios with a conventional annualized arithmetic-mean Sharpe ratio. The table does not provide arithmetic means separately, estimation standard errors, or confidence intervals for differences in Sharpe ratios.

Both equity variants materially reduce volatility and equity beta. The enhanced variant earns more than the generic variant while having similar total volatility. The incremental bond beta is $0.57-0.34=0.23$ for generic low volatility and $0.51-0.34=0.17$ for the enhanced approach. Thus the enhancement removes approximately 26% of the generic strategy's *incremental* bond exposure, calculated as $0.06/0.23$. It removes only about 11% of its absolute bond beta, $0.06/0.57$. These are different denominators and answer different questions.

The table's hedge uses short bond overlays of 23% and 17%, respectively, to match the market's bond sensitivity. Let $r_p^e$ be an equity strategy's excess return and $r_B^e$ the excess return of the bond factor. A financing-consistent idealization of the experiment is

$$
r_{p,h}^e=r_p^e-h r_B^e,
\qquad h=\beta_{p,B}-\beta_{M,B}.
$$

If beta is measured against the same bond factor, its value after the overlay is $\beta_{p,B}-h$. The use of excess bond returns here explicitly includes the financing leg of the short position. Shorting a total-return bond series without accounting for cash proceeds would not be the same return calculation. This notation is a reconstruction of the hedge logic, not a fully specified futures strategy in the paper.

The historical return cost of removing incremental bond sensitivity is small relative to the reported equity advantage: 0.4 percentage points per year for generic low volatility and 0.3 points for the enhanced variant. Volatility falls slightly as well. Their reported Sharpe ratios decline from 0.44 to 0.42 and from 0.58 to 0.57, while the market's ratio is 0.28. On this experiment, the extra bond exposure is insufficient to account for most of the superior ratio.

This conclusion is narrower than saying interest rates do not matter. It says a particular historical return overlay preserves most of a particular historical risk-adjusted advantage. A beta estimated over the entire 1929–2010 sample is an ex post attribution tool. The document does not show how a live investor would estimate and update the hedge using only past data, whether the overlay beta remains stable during rate shocks, or what return is lost after trading and financing costs.

## The global one-year and three-year comparison

The second experiment covers June 1988 through September 2013. It compares Robeco Conservative Equities with the MSCI World Minimum Volatility strategy and relates their rolling alpha to U.S. government-bond returns. Conservative Equities was launched in September 2006 and the MSCI minimum-volatility index in April 2008. Most of the displayed 25-year history therefore predates launch and is simulated. The source combines backtested and live history without separately reporting their regression slopes.

The charts use one-factor alpha rather than simply raw equity return minus bond return. However, the exact market benchmark and all calculation conventions needed to reproduce the rolling alpha are not laid out. In particular, the charts for the 36-month horizon do not fully specify whether every plotted return and alpha has been annualized or aggregated cumulatively. Their axes and fitted coefficients should not be silently converted into a three-year cumulative forecast.

For the twelve-month charts, the printed fitted lines, with returns expressed in decimal units, are

$$
\alpha_{\mathrm{CE},12}=0.0316+0.4689r_{B,12},
$$

$$
\alpha_{\mathrm{MV},12}=-0.0004+0.5528r_{B,12}.
$$

Both slopes are positive. The enhanced strategy's slope is about 15% smaller than the minimum-volatility index's slope. As a dimensional illustration, a 10-percentage-point movement in the plotted bond return corresponds to a fitted alpha difference of 4.689 percentage points for Conservative Equities and 5.528 points for the minimum-volatility index. Those are changes along historical fitted lines, not predicted losses from a specified future rate increase.

The corresponding thirty-six-month fitted lines are

$$
\alpha_{\mathrm{CE},36}=0.0412+0.1196r_{B,36},
$$

$$
\alpha_{\mathrm{MV},36}=-0.0005+0.3208r_{B,36}.
$$

The decline in slope is especially large for Conservative Equities: its three-year slope is approximately 63% below that of the generic index. The source interprets this as evidence that interest-rate effects become less important for longer-term performance and that valuation and momentum help limit the exposure.

There are limits to that interpretation. Rolling twelve-month observations overlap for eleven months, and rolling thirty-six-month observations overlap for thirty-five months. The number of plotted points is therefore much larger than the number of independent horizon observations. The authors themselves caution about the limited independent evidence at the longer horizon. No standard errors, confidence bands, adjusted $R^2$, or formal test of the slope difference is reported. It is not possible to infer from the supplied charts that the slopes differ significantly, that the three-year slope is stable, or that a one-year rate-induced loss reliably reverses over the next two years.

The positive intercepts for Conservative Equities and near-zero intercepts for the minimum-volatility index are also descriptive regression quantities. They do not isolate manager skill from differences in valuation, momentum, construction, benchmark, or simulated-history choices. The comparison suggests a useful design hypothesis—an enhanced defensive equity strategy need not carry exactly the same rate exposure as a mechanical minimum-volatility index—but leaves its independent attribution unresolved.

## Stock selection versus a duration overlay

The authors favor managing tactical interest-rate views through instruments such as futures or swaps rather than distorting the defensive stock portfolio. They argue that removing interest sensitivity through equity selection alone risks giving up desirable low-volatility characteristics. The empirical hedge table supports the feasibility of reducing incremental exposure while retaining most historical performance. It does not prove the stronger claim that completely eliminating rate sensitivity is impossible without damaging the strategy.

A stock-selection constraint and a derivative overlay change different parts of the portfolio. A sector or stock exclusion may change equity beta, valuation, profitability, diversification, and expected turnover along with rate sensitivity. An overlay changes the exposure to the chosen bond instrument and introduces its own financing, collateral, and basis risks. Whether one is preferable depends on the investment mandate and on which notion of rate exposure is being targeted.

The source does not supply a futures contract, swap maturity, yield-curve bucket, DV01 target, roll schedule, margin rule, collateral return, or stress-test scenario. Nor does it quantify the cross-currency basis between a global equity portfolio and a U.S. government-bond hedge. A full implementation would have to decide whether to neutralize a regression beta, parallel-shift duration, key-rate sensitivities, or a stress loss. The paper estimates the first concept; it does not establish their equivalence.

The enhanced portfolio incorporates valuation and momentum, with sentiment and additional forward-looking risk information discussed as relevant design elements. Their exact formulas and contribution to the rate-beta reduction are not identified. One cannot recover the 0.51 bond beta by taking a published generic low-volatility portfolio and adding an arbitrary value or momentum score. The observed reduction belongs to the specific, incompletely disclosed construction in the source.

## Replication boundary and interpretation

The minimum inputs for reproducing the first experiment are the U.S. point-in-time equity universe, total returns and delisting treatment, the three-year volatility signal, stock ranking and weighting rules, rebalance schedule, valuation and momentum definitions, cash return, and the two Ibbotson bond series. The paper identifies the historical span, volatility lookback, broad enhancement categories, and bond mix, but not the complete remaining pipeline. Its result is reproducible in principle only with additional methodology or author data.

The global experiment additionally requires the exact backtest and live return series, their splice dates and fee conventions, benchmark returns for the alpha regressions, and the rolling-horizon aggregation convention. Legal disclosure language about gross or net performance cannot substitute for a table-specific statement of whether a particular strategy series includes management fees and transaction costs. No turnover-based capacity analysis or explicit cost model accompanies the reported comparisons.

There is no training/validation split, hyperparameter search, statistical learning model, or out-of-sample hedge calibration in this short paper. The long U.S. sample and shorter global product comparison answer complementary questions but do not form a formal held-out design. All quoted performance is historical and the global history is mostly simulated. The paper's numerical contribution is nevertheless useful: the bond-beta difference can be measured, a common-factor overlay can be specified, and the claim that low-volatility performance is entirely a disguised bond allocation fails in the reported U.S. comparison.

## Source map and bibliography

Blitz, David, Bart van der Grient, and Pim van Vliet (June 2014), “Interest rate risk in low-volatility strategies,” Robeco research white paper. The opening pages explain the exposure mechanisms; Exhibit 1 on PDF page 3 contains the 1929–2010 U.S. comparison and hedge results; the rolling twelve- and thirty-six-month global scatterplots are on PDF pages 4–5; the remaining substantive discussion addresses enhancement and portfolio implementation. PDF pages 8–9 contain distribution and legal disclosures. The source has no technical appendix or additional numerical tables beyond the supplied exhibits.
