# Better than the original? The relative success of copycat funds

Marno Verbeek and Yu Wang. *Journal of Banking & Finance* 37 (2013), 3454–3471. DOI: 10.1016/j.jbankfin.2013.04.024. Source: [BestIdeas_VerbeekWang_2013.pdf](../../Finance/BestIdeas_VerbeekWang_2013.pdf). This note follows the published 18-page PDF, including Appendix A; page references are PDF pages unless journal pages are specified.

## Why this matters

A portfolio disclosure can transfer part of an active manager's research to an investor who pays substantially less for portfolio management. But three quantities must be separated: the performance of the manager's actual fund, the performance of a stale disclosed stock portfolio, and the performance of a feasible copycat after its own trading and operating costs. Verbeek and Wang build all three and ask when copying succeeds. Their contribution is a large-sample, implementable-delay comparison, together with a way to measure whether disclosed holdings represent what a fund actually does between reports.

The central finding is relative, not an assertion that copied funds beat passive benchmarks. Across 3,046 US equity mutual funds over 1985–2008, simulated copycats have broadly comparable net performance to their target funds under the paper's cost assumptions. Copying successful managers captures some return persistence but loses part of their advantage. Copycats of managers with more representative disclosures do better relative to their targets. Fees explain much of the average equivalence; trades and decisions absent from disclosed snapshots explain important differences across funds.

The experiment is useful for designing holdings-based strategies and for studying the costs of disclosure. It does not observe actual copycat investors, estimate market equilibrium after widespread copying, or establish that disclosure rules reduce incumbent shareholders' realized welfare.

## Sample, identifiers, and information timing

The sample combines the CRSP survivorship-bias-free mutual fund database, Thomson Financial/CDA stock holdings, CRSP stock returns, and the MFLINKS fund identifiers. It runs from January 1985 through December 2008. Appendix A supplies the selection procedure for actively managed US domestic equity funds. A reproducer should retain the historical objective-code rules from that appendix rather than substitute a present-day fund classification. The screening also allows missing objective codes when the remaining criteria identify eligible funds.

Funds must average more than 80% and less than 105% of assets in stocks, have at least ten stock positions, and have at least \$5 million in assets. Observations before the fund's reported inception, missing fund names, and identified index funds are excluded. Name screens include INDEX, INDE, INDX, INX, IDX, S&P, ISHARES, DOW JONES, and MSCI; the authors also inspect and exclude additional unsuitable funds. Approximately 92% of the target sample is linked to holdings. These filters reduce incubation and inappropriate-fund problems but do not amount to a fully automated classification recipe: the manual exclusions are not delivered as a reusable list in the PDF.

Multiple share classes are handled by selecting the class with the longest valid history over the sample, breaking ties using the lowest CRSP identifier. They are not combined into an asset-weighted fund return. More than 90% of funds with multiple share classes are covered by this representative-class procedure. Because “longest history” is determined over the entire sample, this is an ex post data-construction choice. It should be retained for exact replication and replaced by a point-in-time rule in a prospective trading exercise.

The average fund has approximately \$875.7 million in assets, versus a median of \$107.5 million. Average reported turnover is 91.58% annually and the median is 67%; average stock allocation is 95.06%. The expense-ratio distribution has mean approximately 1.3% and median 1.2%. These are cross-sectional descriptive statistics, whereas the performance tables average across funds and then over time; their expense and turnover aggregates need not be identical.

Most important is the distinction between the holdings date and the date outsiders can use the holdings. The paper assumes every portfolio becomes available 60 days after its reporting date. The Thomson reporting date identifies the portfolio snapshot; its database vintage date is not treated as the actual public disclosure timestamp. Copycats therefore trade on a uniform assumed delay, not on observed filing-by-filing release times. The baseline follows each newly eligible disclosure and otherwise leaves the stock quantities unchanged. A semiannual alternative ignores intervening reports until the required six-month spacing is reached; with the assumed two-month release delay, holdings can then be eight months old.

This timing is substantially more realistic than buying the quarter-end portfolio before disclosure, but it is still a maintained approximation. Actual early and late filings, trading intraday after release, and provider-processing delays are not separately modeled.

## Constructing the copycat return

Let $N_{ji,t-s}$ be the number of shares of stock $i$ in fund $j$'s latest publicly usable snapshot. Let $P_{i,t-1}$ be the price at the end of the preceding month, with share quantities adjusted for stock splits. The disclosed stock portfolio's current weights are

$$
\widetilde w_{ji,t-1}
=\frac{N_{ji,t-s}P_{i,t-1}}
{\sum_k N_{jk,t-s}P_{k,t-1}}.
$$

The monthly gross stock return is

$$
GR_{jt}=\sum_i\widetilde w_{ji,t-1}R_{it}.
$$

This distinction is operationally important: the copycat holds a fixed number of shares between eligible reports, so portfolio weights drift with prices. It does not rebalance monthly back to the last reported percentage weights. At a new disclosure it adjusts to the newly disclosed quantities, with the paper assuming the same assets under management as the copied fund for trading-cost calculations.

The simulated complete fund also retains the target's nonstock allocations from CRSP. Bonds and preferred stock receive a Barclays/Lehman aggregate bond index return; cash and other assets receive the Treasury-bill return. Nonstock assets account for less than 5% on average but matter for a like-for-like return comparison. Omitting cash would inadvertently give the copycat additional equity exposure, especially during market downturns.

Actual fund gross return is reconstructed by adding one-twelfth of the annual expense ratio to reported monthly net return. This is gross of operating expenses, not gross of the actual fund's transaction costs, which remain inside reported NAV returns. By contrast, the copycat's initial holdings return is before its modeled trading costs. The appropriate comparison with reconstructed target gross return therefore subtracts copycat trading costs first. The different meanings of “gross” should be preserved in any replication tables.

## Trading-cost and expense model

Section 2 applies an empirical trade-cost model estimated in earlier work. Predicted cost is a percentage of the dollar value traded. For purchases,

$$
c^{buy}=1.098+0.336I_{NASDAQ}+0.092\,TradeSize
-0.084\ln(MarketCap)+\frac{13.807}{Price}.
$$

For sales,

$$
c^{sell}=0.979+0.058I_{NASDAQ}+0.214\,TradeSize
-0.059\ln(MarketCap)+\frac{6.537}{Price}.
$$

$MarketCap$ is measured in thousands of dollars; $Price$ is stock price; and $TradeSize$ is trade value relative to stock market capitalization. The coefficients cannot be safely applied after silently changing the capitalization unit. The text describes relative trade size but does not provide an implementation-level assurance about fraction-versus-percent scaling for every imported input; this should be reconciled with the cited original cost model before code is finalized.

Trades are inferred from changes between successive disclosed holdings. Dollar trading costs are divided by the preceding stock portfolio's value, and the paper winsorizes both predicted trade costs and resulting asset-based costs at the 1% tails. Costs for a disclosure interval are allocated across the number of months since the previous disclosure. Consequently, reported monthly net returns smooth the cost of rebalancing over an interval rather than deducting every dollar at its execution date. Reproducing that convention matters for monthly risk-adjusted returns even when total interval cost is similar.

The target fund and copycat are assumed to have the same scale for the market-impact calculation. Fund flows, funding of the rebalance, and exact trade execution prices are not separately reconstructed. No explicit nonnegative floor for cost predictions is specified. The trade-cost coefficients derive from an earlier trading environment and are used throughout a long sample, so improvements in commissions, spreads, and electronic trading are only imperfectly captured by the changing stock inputs.

Copycat operating expenses are fixed at 20 basis points per year, motivated by a low-cost index-fund comparison. That is a scenario assumption, not an estimated feasible expense ratio for every bespoke fund-sized copycat. A small account with a large number of positions, data fees, taxes, or execution constraints could face a very different cost budget. Conversely, copying at much smaller scale might reduce market impact relative to the same-AUM simulation. The authors check copycat sizes of 25%, 50%, 75%, and 100% of target assets and report return differences only in the second decimal place when expressed as percentages. This establishes limited size sensitivity within their cost formula, rather than empirical proof that capacity is unimportant under another execution model.

## Average performance and disclosure frequency

Tables 2–4 distinguish raw holdings returns, trading costs, and operating expenses. Average annual actual fund net return is 10.33%, copycat gross return 11.44%, and copycat net return 10.52%; the market return is 11.35%. Average copycat trading cost is approximately 0.64% annually. The fund-expense aggregate in the performance calculation is about 1.26%, compared with the copycat's assumed 0.20%.

The monthly paired-return comparisons give a sharper decomposition:

| Copycat minus actual fund comparison | Monthly difference | $t$-statistic |
|---|---:|---:|
| Gross holdings return versus reconstructed fund gross return | −0.010% | −1.19 |
| Copycat after trading costs versus fund gross return | −0.070% | −5.54 |
| Copycat net of trading costs and expenses versus fund net | +0.020% | 1.67 |
| Copycat net of expenses but ignoring its trading costs versus fund net | +0.073% | 6.15 |

The evidence is not that copycats trade better than managers. They lose on the comparison after modeled trading costs and before operating fees. Their large fee saving approximately offsets that loss. The final mean advantage has only marginal statistical support, while equivalence remains economically plausible. Annual compounded figures need not equal twelve times these average monthly paired differences.

Quarterly copying yields about 11.44% annual gross return, versus 11.34% under semiannual copying. Estimated trading costs rise from approximately 0.54% to 0.64%. Thus both schedules earn about 10.74% after trading costs but before the copycat's operating expense. The gross improvement from more frequent updating is 0.11 percentage point per year with $t=2.39$; additional cost is 0.10 point with $t=21.48$; the difference after trading costs is only 0.01 point with $t=0.13$. Faster disclosure has information value, but that value is largely consumed by extra turnover in this experiment.

## Measuring whether holdings represent the fund

The second innovation is a representation measure, called tracking error, designed to capture how well disclosed holdings explain actual fund behavior. It is not simply the distance between portfolio weights and a market index. Each disclosed stock is mapped to a characteristic benchmark following the DGTW approach: a June-sorted $5\times5\times5$ set of size, industry-adjusted book-to-market, and momentum portfolios. Industry adjustment uses the Fama–French 48-industry classification.

At a ranking month $t$, the method uses the disclosed snapshot dated $t-2$ to build a style return series. It holds the snapshot's benchmark composition fixed while looking back across five months, $t,t-1,\ldots,t-4$. Tracking error is the standard deviation of the differences between actual fund returns and these holdings-implied style returns. In simplified notation,

$$
TE_{jt}=\operatorname{sd}_{k=0,\ldots,4}
\left(R^{fund}_{j,t-k}
-\sum_iw^{snapshot}_{ji,t-2}R^{style(i)}_{t-k}\right).
$$

The text's description of fixed snapshot weights should govern the interpretation; the printed weight indices in the equation are not a complete implementation specification. Five observations produce a noisy fund-level statistic. It also combines several mechanisms: hidden interim trading, within-style stock selection, changing cash, return volatility, and genuinely unrepresentative quarter-end holdings. High $TE$ is evidence of a discrepancy, not a direct measurement of window dressing or misconduct.

Funds are ranked into deciles in February, May, August, and November and portfolio performance is measured over the following three months. Membership remains fixed until the next quarterly rank, while a constituent copycat can update its holdings when a new disclosure becomes usable. Using month $t$ returns in the statistic means the sort must occur after those returns are known. This is an end-of-month design, not a signal available at the start of that same month.

## What predicts unrepresentative disclosures?

Table 6 estimates panel regressions of the tracking-error measure on manager characteristics, with time fixed effects and standard errors clustered by fund. Predictors are aligned with each snapshot date. Past performance is the Carhart alpha estimated from the preceding twelve months of net returns; another specification adds its square. New money growth is the preceding three months' change in assets net of return appreciation, assuming flows occur at period-end. Market volatility is the standard deviation of the value-weighted CRSP market return over the same five-month interval used in the representation measure. The Active Share observations cover 1990Q1–2006Q4, limiting specifications that require that input.

The model can be written as $TE_{jq}=X_{jq}'\beta+\tau_q+u_{jq}$. Its table identifies time effects; the phrase “fixed effect panel regressions” does not justify silently adding an unreported fund fixed effect in an exact reconstruction. Fund-clustered uncertainty accommodates within-fund dependence but is different from controlling for fund-specific intercepts.

The linear specification associates higher tracking error with better past performance, more turnover, higher expenses, more volatile markets, higher Active Share, and a larger return-gap measure. Reported coefficients include 0.09 on past performance, 0.02 on turnover, 0.03 on expenses, 0.08 on market volatility, and 0.14 on Active Share, with respective test statistics 5.20, 2.61, 3.78, 17.65, and 2.25. The table reports statistics as $z$ rather than ordinary finite-sample $t$ statistics. Its $R^2$ is 23.15%; the alternative including squared performance reports 21.79%, which should not be interpreted as a nested-regression improvement without establishing identical observations and controls.

Fund age and new money growth have negative coefficients: older funds and funds receiving more money have more representative holdings conditional on the other regressors in this table. That sign should govern interpretation even though parts of the surrounding discussion suggest experienced managers may conceal their activity. The return-gap sign ambiguity described below also affects this regression. These are correlates of the representation statistic, not direct causal estimates of window dressing; the statistic itself includes volatility, legitimate interim trades, and stock-selection residuals.

## Results conditional on representation and manager skill

In Table 7, the most representative decile has actual fund net return of 0.94% per month and copycat return of 0.99%. The paired advantage is about 0.05% with $t=5.46$. For the least representative decile, the corresponding returns are 0.82% and 0.80%, with paired difference −0.03% and $t=-0.72$. Differences in displayed averages reflect rounding and the precise paired sample. The least-minus-most-representative spread in the relative advantage is −0.08% monthly, $t=-2.40$.

Trading costs help explain the result: they rise from approximately 0.03% monthly in the most representative group to 0.12% in the least representative group. Carhart adjustment produces a copycat-minus-target alpha of +0.05% in the most representative decile, $t=4.59$, versus −0.02%, $t=-0.60$, in the least representative group. The relative-alpha spread is −0.07% with $t=-1.89$, weaker than the raw relative-return spread. A researcher should not label every result significant at the conventional two-sided 5% level.

Table 8 sorts by the preceding twelve months' average market-adjusted performance. Subtracting the same market return from each fund does not change the cross-sectional ordering when all have identical observation windows. The previous losers subsequently return approximately 0.56% monthly while their copycats return 0.66%; the paired copycat advantage is 0.09%, $t=3.23$. Previous winners subsequently return 1.12% while their copycats earn 1.02%; copying costs about 0.11%, $t=-3.79$, relative to the target.

Thus raw winner-minus-loser persistence is 0.56% monthly in actual funds, $t=2.18$, but only 0.36% among copycats, $t=1.36$. A copycat of a previous winner can outperform most other fund categories in raw return while still failing to deliver positive factor alpha. The winner copycat's Carhart alpha is −0.17% monthly, $t=-1.82$, versus approximately −0.04% for the actual winner; the relative alpha is −0.13%, $t=-4.75$. The persistence that survives in copied stocks is partly exposure to rewarded or persistent styles, especially momentum.

The return-gap test asks whether interim decisions add value beyond disclosed holdings. There is a sign inconsistency in the source: Section 5.2 gives the economic definition as actual fund return minus passive holdings-implied return, whereas the Table 9 caption reverses the wording. The economically consistent reading, used here, is that a higher gap indicates more value added outside the static snapshot. Low-gap funds have copycat net return approximately 1.06% against 0.94% actual, a paired advantage of 0.11%, $t=4.21$. High-gap funds have copycat return 0.93% against 1.09% actual, a disadvantage of 0.16%, $t=-5.15$. A replicator should verify the original code or cited return-gap series before choosing a sign convention.

The Active Share extension uses an externally supplied series for 1990Q1–2006Q4. Active Share is one-half the sum of absolute deviations from benchmark stock weights; it measures stock selection away from the benchmark, not interim trading directly. Copying low-Active-Share funds produces a relative net advantage of about 0.07% monthly, $t=4.90$; copying high-Active-Share funds produces −0.03%, $t=-0.91$. High-minus-low copycat Carhart alpha is −0.22% monthly, $t=-2.12$. The source discusses some three-factor numbers alongside tables displaying Carhart results; those should not be interchanged.

These tests identify different reasons to avoid interpreting a holdings portfolio as the full skill of its manager. Return gap captures activity beyond snapshots, representation captures return differences from reported styles, and Active Share captures benchmark deviation. None alone is a sufficient statistic for all manager abilities. The paper's conclusion favors copying successful managers whose disclosures are representative, but it does not present a fully validated, jointly optimized double-sort strategy combining every favorable characteristic.

## The 2004 reporting change

The paper also compares performance before and after the May 2004 move toward mandatory quarterly disclosure. The full-sample mean net copycat advantage rises from approximately 0.01% to 0.04% per month; the reported change is 0.02% after unrounded calculation, $t=1.26$. Therefore the average relative-return improvement is not statistically clear in the unrestricted sample. The standard deviation of the return difference falls from 0.22% to 0.07%, and the holdings-representation statistic falls from 1.83% to 1.21%, with a difference of −0.62 percentage point and $t=-12.07$.

Among 1,601 funds present in both subperiods, relative net return rises from −0.02% to +0.04%, with an unrounded difference of +0.05%, $t=3.37$. Among 241 funds already reporting at least 3.5 times a year, it rises from −0.03% to +0.03%, a +0.06% change with $t=2.74$. The standard deviation also falls for both groups. Improvements among already frequent reporters make the result difficult to attribute exclusively to reporting frequency.

These are before-and-after comparisons, not a randomized policy experiment. Conditioning on survival changes the estimand; market structure, funds, volatility, costs, and other disclosures also change through time. The evidence supports better tracking after 2004, but it does not isolate a clean causal welfare effect of the rule.

## Reproduction priorities and interpretation limits

An implementation should maintain separate records for economic fund identity, selected share class, holdings date, assumed availability date, split-adjusted share quantities, stock return, style benchmark, and fund-level cash and bond allocations. The return engine should first reproduce gross holdings returns, then introduce trading costs, then expenses. Matching only the final net return can hide offsetting errors in timing and cost units. The quarterly ranking engine should be separate from the disclosure-driven rebalance engine, because their clocks differ.

The most consequential missing inputs are the complete manual exclusion list, actual filing dates, exact handling of all CRSP delisting and missing-return cases, the original trade-size scaling, and detailed cash/flow treatment in a same-AUM rebalance. These are not grounds to invent convenient defaults and label them the authors' procedure. A new implementation should document its own choices and show how results change with actual disclosure dates, more conservative operating expenses, and contemporaneous cost estimates.

The study establishes that public holdings contain considerable economic information, while the manager's undisclosed decisions and fee structure determine how much copying can recover. Its practical lesson is to measure the entire information-and-cost chain. A stale low-fee replica can match an expensive fund without matching the fund's gross skill, and matching an active fund does not imply beating a passive alternative.
