# Higher risk, lower returns: What hedge fund investors really earn

**Ilia D. Dichev and Gwen Yu. Working paper, March 4, 2009.** The source covers **1980–2006** and predates any later published revision.

**Source:** [HedgeFundsReturns_DichevYu_2009.pdf](../../Finance/HedgeFundsReturns_DichevYu_2009.pdf), 49 PDF pages, including both appendices, Figure 1, and Tables 1–9. References below use PDF pages unless a section or table is specified.

## Why this matters

A fund can have an excellent compounded return while most of its investors earn substantially less. The difference arises when capital arrives after good performance, when the fund becomes too large to exploit earlier opportunities, or when withdrawals occur before a recovery. Dichev and Yu measure this distinction directly: the return on a fund's unit value is a time-weighted investment return, whereas the return on the sequence of investor contributions and distributions is a money-weighted internal rate of return.

The contribution is both a measurement change and an empirical finding. In their CISDM sample, the aggregate portfolio's annual buy-and-hold return is **14.54%**, but its dollar-weighted return is **10.67%**. At the individual-fund level, mean returns are **9.99%** and **6.42%**, respectively. The authors also examine dispersion across funds and randomly assembled portfolios, finding materially greater dispersion of money-weighted outcomes over realistic portfolio sizes.

The distinction is valuable for allocator evaluation: a manager's reported record does not answer what happened to capital actually entrusted to that manager. It is equally important not to overinterpret the result. The paper's money-weighted return is calculated from aggregate fund assets and inferred net flows, not from a panel of named investors' account statements. Its dispersion measure is cross-sectional dispersion of lifetime annualized returns, not a directly estimated time-series volatility of an investor's wealth. Its evidence about return chasing is associative rather than a structural identification of irrationality or negative forecasting skill.

## Cash-flow accounting and timing

Let $A_t$ be end-of-month assets under management, measured as investors' equity rather than gross levered positions. Let $r_t$ be the fund's reported monthly return, net of fees. Define signed distributions from the investor's perspective:

$$
D_t=A_{t-1}(1+r_t)-A_t.
$$

Positive $D_t$ means net money leaves the fund for investors; negative $D_t$ means investors contribute new money. Equation (1), PDF p. 9, is an accounting residual: changes in net assets not explained by the return are assigned to net capital flows. AUM must therefore be measured on the same investor-equity and fee basis as returns. Subtracting fees again would double-count them.

The convention effectively places flows at the end of the month after the return accrues on beginning assets. Daily subscriptions and redemptions are not observed. If substantial flows occur within a month, the inferred value can differ from actual cash transfers because the new capital earns some of that month's return. The authors choose monthly rather than annual measurement to reduce this timing problem, but do not have exact transaction dates.

The monthly dollar-weighted return $q$ solves

$$
-A_0+\sum_{t=1}^T\frac{D_t}{(1+q)^t}+\frac{A_T}{(1+q)^T}=0.
$$

The final NAV is treated as a hypothetical liquidating distribution at the sample endpoint. It is added **in addition to** the final month's distribution $D_T$. This is an observed-NAV valuation convention, not evidence that every investor could withdraw that amount immediately at the stated value.

The corresponding annualized measures are

$$
R_{DW}=(1+q)^{12}-1,
\qquad
R_{BH}=\left[\prod_{t=1}^T(1+r_t)\right]^{12/T}-1.
$$

The latter is the return of a passive position held over the measured fund history, assuming returns can be reinvested as represented by the NAV series. It is not the arithmetic average of monthly returns. Differences between annualized IRRs should be reported in percentage points per year rather than as percentage changes in wealth.

Multiple IRR roots are possible when distributions repeatedly change sign. Footnote 3 says that **11 of 7,190 funds** have more than one root yielding a monthly return with absolute value below 100%. For those funds the authors select the root described as closest in absolute value to the buy-and-hold return. Exact root-search intervals, tolerance, treatment of complex roots, and the operational meaning of that closest-root rule are not supplied. A replication should preserve all admissible roots and document the choice; blindly accepting the first numerical solver result is insufficient.

## The weighting identity and what it proves

Substituting the asset-flow identity into the IRR equation and telescoping the asset terms gives equations (3)–(4):

$$
\sum_{t=1}^T\frac{A_{t-1}}{(1+q)^t}(q-r_t)=0.
$$

For positive assets and $q>-1$, define

$$
\omega_t(q)=\frac{A_{t-1}}{(1+q)^t},\qquad
W(q)=\sum_t\omega_t(q).
$$

Then

$$
q=\frac{\sum_t\omega_t(q)r_t}{W(q)}.
$$

This is an exact fixed-point identity: money weighting is an arithmetic weighted average of monthly returns with weights proportional to discounted beginning assets. The weights themselves depend on the unknown IRR, so the formula is not a one-pass estimator obtained by substituting raw AUM weights.

It explains why the same fund return series can produce different investor outcomes under different capital histories. Returns earned while much capital is exposed receive greater effective weight. It does **not** make the gap from geometric buy-and-hold return identical to a single simple covariance. Geometric compounding, discounting, and the path of assets all matter. A correlation with past returns can generate an ex post gap without establishing that investors possessed, or lacked, useful information about future returns.

Appendix A makes the mechanism transparent. An initial **\$1,000**, a subsequent **\$2,000 contribution**, and returns of +100% followed by −50% give final wealth **\$2,000**. Buy-and-hold return is zero, but the per-period IRR solves $-1000-2000/(1+q)+2000/(1+q)^2=0$, giving about **−26.8%**. Reversing the return order leaves the fund's compounded return unchanged while final wealth becomes **\$5,000**, giving about **44.9%**. These are two-period examples, not annual hedge-fund estimates.

The level of aggregation changes the relevant flows. A sale between two investors cancels in the fund's aggregate capital account even though it affects their separate IRRs. Fund-level dollar-weighted returns therefore describe the aggregate account represented by net flows. They are not an arithmetic average, median, or necessarily the return of a randomly selected individual investor.

## Source data, inclusion rules, and coverage growth

The paper uses the **CISDM database** from 1980 through 2006. The start date avoids even thinner early coverage. The principal inclusion requirement is at least **ten monthly distributions** over a fund's life, meaning sufficient AUM and return information to infer those flows. The full sample includes **7,190 entities**: **3,749 hedge funds proper**, **1,483 funds of funds**, and **1,958 commodity vehicles**, split into **910 commodity pool operators** and **1,048 commodity trading advisors** in the aggregate tables.

All returns are net of fees, and the underlying return and flow calculations use monthly observations. The source does not provide a complete data-cleaning program for missing AUM, duplicated share classes, currency conversions, discontinuous reporting, backfilled periods, or terminal values for discontinued funds. Inclusion of inactive funds helps with survivorship, but it is not equivalent to observing every fund that ever existed or every final liquidation loss.

Coverage expands from **17 funds** with approximately **\$885 million** in 1980 to **3,207 funds** with approximately **\$560.9 billion** in 2006. Hedge funds proper expand from four funds and **\$591.6 million** to 1,691 funds and **\$307.0 billion**. This growth makes the difference between equal weighting across years and capital weighting economically important, but it also means the early index rests on a very small and potentially selected set of reporters.

Table 2 reports all-vehicle annual return averages of **19.8% for 1980–1992** and **11.1% for 1993–2006**; corresponding hedge-fund-only figures are **22.5%** and **12.8%**. Far more capital is present during the later, lower-return years. The descriptive table's full-period mean, **15.3%**, should not be confused with the aggregate compounded buy-and-hold estimate of **14.54% in Table 5**. The prose loosely calls the former compounded, but the two reported summaries are different; the exact Table 5 compounded result is the appropriate benchmark for the main IRR comparison.

Scaled-flow conventions differ across analyses. Table 8 explicitly uses monthly distributions divided by beginning AUM. Table 9 and Figure 1 use the sum of six monthly distributions divided by the average of beginning and ending AUM. Table 1's Orbis displayed ratios are consistent with average endpoint assets, despite prose describing beginning assets. For example, the 1991 distribution of approximately **−\$78.3 million**, divided by the mean of **\$98.6 million** and **\$210.3 million**, gives the printed **−50.70%**. Reusing one denominator everywhere would fail to reproduce the source.

## The Orbis case as a reconciliation example

Table 1 follows the Orbis Optimal Fund from an initial 1990 asset value of **\$98.6 million** to approximately **\$3.978 billion** in 2005. Returns are strong in the early 1990s, weaker in several subsequent years, strong again in 2000–2002, and more modest afterward. Contributions tend to follow the strong periods.

The reported annualized buy-and-hold return is **11.32%**, compared with a dollar-weighted return of **8.10%**, a **3.22-point** gap. The comparable S&P 500 buy-and-hold figure is **10.85%**. This example shows how the relative ranking can reverse depending on whether the question is about the fund's unit-value history or the capital-flow-weighted account.

Annual rows are an illustration; the empirical calculations use monthly inputs. One should not expect an IRR calculated solely from the selected annual table to reproduce the monthly-timed result exactly. Nor does comparing Orbis IRR with an index time-weighted return alone provide a risk-adjusted performance test. The paper later constructs an index counterfactual using hedge-fund capital-flow patterns to make the timing comparison more informative.

## Individual-fund outcomes and the meaning of risk

Table 3 computes a lifetime annualized buy-and-hold return and IRR for each fund, then describes the cross-sectional distribution. The full-sample results are:

| Statistic | Buy-and-hold | Dollar-weighted |
|---|---:|---:|
| Mean | 9.99% | 6.42% |
| Standard deviation across funds | 15.52% | 19.86% |
| First percentile | −31.12% | −64.12% |
| Tenth percentile | −1.60% | −6.97% |
| Median | 9.26% | 6.99% |
| Ninetieth percentile | 22.41% | 19.44% |
| Ninety-ninth percentile | 54.43% | 53.10% |

The mean gap is **3.57 points**, and the median gap **2.27 points**. The lower tail separates much more sharply than the upper tail. The first-percentile gap is **33 points**. This is evidence that poor capital-weighted outcomes are not confined to a small reduction in otherwise uniformly successful returns.

The table reports $p<0.001$ for differences in means, standard deviations, and medians. The stated procedures are simple $t$ tests, a chi-squared test for standard deviation, and a Wilcoxon median test. Exact variance-test implementation is not given. The authors justify simple inference partly by low common exposure and the average fund life of roughly six years within the long calendar sample, but these arguments do not guarantee independence or normality. Common styles, overlapping histories, and heavy tails can affect conventional standard errors.

The measured “higher risk” is greater dispersion across fund-level lifetime outcomes. Funds have different inception dates and horizons, some much shorter than the 10–15 years the authors regard as desirable for a meaningful money-weighting comparison. It is not valid to plug **19.86%** into a one-year portfolio optimizer as if it were a homogeneous annual conditional volatility estimate. The paper explicitly uses the cross section because the available history is too short to estimate a meaningful time series of long-horizon IRRs.

An ex post sort on buy-and-hold performance produces increasing gaps from **1.12 points in the bottom quintile** to **8.85 points in the top quintile**. Top-quintile means are **27.89% buy-and-hold** and **19.04% dollar-weighted**. The “star fund” result is economically large, but the stars are selected using their full realized history, so this is not an implementable contemporaneous selection signal. The authors deliberately avoid comparing within-quintile volatilities because sorting on buy-and-hold returns mechanically restricts their dispersion but not IRR dispersion.

Active funds, numbering **2,932**, have means of **12.76% and 9.07%**; inactive funds, numbering **4,258**, have **8.07% and 4.62%**. The gap remains in both groups. Hedge funds proper have means **11.44% and 7.27%**. Funds of funds have a smaller mean gap, **8.80% versus 7.59%**, but a striking dispersion contrast: **7.10% versus 18.89%**. This is compatible with an extra layer of capital timing at the fund-of-funds level, but the article does not identify that mechanism causally or track underlying holdings.

## Random portfolios and diversification

Table 4 constructs **1,000 random portfolios** for each size **5, 10, 20, and 100 funds**, excluding funds of funds. Each constituent must have at least ten monthly distributions. Buy-and-hold portfolio returns are value-weighted; dollar-weighted returns are calculated from the aggregated capital account rather than averaged constituent IRRs.

| Funds in portfolio | Mean BH | Mean DW | Cross-portfolio SD, BH | Cross-portfolio SD, DW |
|---|---:|---:|---:|---:|
| 5 | 11.13% | 9.33% | 6.93% | 13.58% |
| 10 | 11.78% | 9.74% | 5.00% | 6.62% |
| 20 | 12.46% | 9.73% | 4.18% | 5.47% |
| 100 | 14.37% | 10.64% | 3.89% | 3.46% |

Diversification greatly reduces cross-portfolio dispersion for both metrics. Money-weighted dispersion remains higher for 5–20 funds, but is actually **lower** at 100 funds in the table. The result should not be summarized as a universal ordering at every level of diversification.

The simulation samples from the historical universe. It does not establish that every sampled combination was simultaneously available, open to new investment, or feasible given minimum investments and liquidity restrictions. The source does not fully specify whether sampling is without replacement within each portfolio, how staggered fund histories are aligned, or the random seed. These are material reproduction inputs. The authors' characterization of 5–20 funds as realistic is an interpretation, not an estimated optimal number of managers.

## Aggregate portfolios and the index counterfactual

The aggregate calculation first forms value-weighted monthly fund returns. A reconstruction with matched available assets uses beginning-equity weights,

$$
r_t^P=\frac{\sum_iA_{i,t-1}r_{it}}{\sum_iA_{i,t-1}}.
$$

It compounds these returns for the buy-and-hold measure. For the dollar-weighted measure, it aggregates initial assets, monthly signed flows, and final assets and solves one portfolio IRR. Entry, exit, and the treatment of a fund's first or last recorded NAV must be reconciled explicitly; otherwise changes in database membership can masquerade as investor capital flows. The source does not provide its complete entry/exit accounting code.

Table 5 gives **14.54% versus 10.67%** for all 7,190 vehicles, a reported **3.86-point** gap, with bootstrap $p=0.036$. For hedge funds proper the values are **16.41% versus 12.04%**, gap **4.38 points**, $p=0.023$. Funds of funds have **13.23% versus 9.45%**, $p=0.077$; CPOs **9.56% versus 6.94%**, $p=0.109$; CTAs **12.82% versus 9.25%**, $p=0.098$. Thus not every subgroup gap is significant at 5%, despite uniformly positive point estimates.

By investment type, equity-only portfolios have **15.87% versus 11.70%**, bonds **13.46% versus 7.72%**, and other portfolios **13.52% versus 8.93%**. Their reported gap-test $p$ values are **0.028, 0.001, and 0.012**. The displayed investment-type counts sum to 7,191 rather than 7,190, a minor source reconciliation issue for category assignment.

The S&P benchmark has **13.23% buy-and-hold** and **12.08% money-weighted** when combined with hedge-fund investor capital-flow patterns. The latter exceeds the aggregate hedge-fund IRR by **1.41 points**, reversing the time-weighted ranking. Exact implementation must specify whether the counterfactual preserves absolute cash flows or proportional flow patterns and how feasibility is handled if withdrawals exceed counterfactual wealth; the paper describes the same capital-flow patterns but does not supply full code.

This comparison is an opportunity-cost illustration, not proof of negative risk-adjusted alpha for every strategy. A broad equity index and a market-neutral or option-like hedge fund bear different risks. Nor is it valid simply to subtract the average IRR gap from an unrelated study's regression alpha: the samples, weights, risk exposures, and estimands differ.

## Bootstrap design and its maintained null

Appendix B holds the ordered sequence of **scaled capital flows** fixed and randomly shuffles the observed return sequence against it. For each shuffled sequence, the authors rebuild implied absolute flows and ending assets, solve a pseudo-IRR, and repeat **1,000 times**. The observed dollar-weighted return is compared with this null distribution, which is intended to remove the historical association between flow timing and returns.

If scaled flow is $d_t=D_t/A_{t-1}$, the reconstruction is

$$
A_t^*=A_{t-1}^*(1+r_{\pi(t)}-d_t),\qquad D_t^*=d_tA_{t-1}^*.
$$

If instead the scale uses average beginning and ending assets, the consistent recursion is different:

$$
A_t^*=A_{t-1}^*\frac{1+r_{\pi(t)}-d_t/2}{1+d_t/2}.
$$

These formulas are derived implementation identities. The appendix does not fully specify which scaled-flow denominator is used in the bootstrap, whether shuffling is with replacement, the treatment of infeasible negative assets, the seed, or whether the displayed $p$ value uses a one- or two-sided empirical tail. Reproduction should resolve these choices rather than silently label an arbitrary implementation exact.

Unrestricted shuffling removes serial order, including volatility clustering and structural changes in return distributions. It is therefore a test under an exchangeability-style randomization assumption, not automatically robust to all hedge-fund dependence simply because it is called a bootstrap. A block or regime-conditioned procedure would be an additional robustness experiment, not the published design.

## Characteristics, timing, and reported exceptions

Table 6 forms annually rebalanced size terciles using **previous-year average AUM**. Small, medium, and large funds have mean sizes approximately **\$9.2 million, \$37.3 million, and \$276.9 million**. Their BH/DW returns are **21.43/17.66%, 17.38/13.29%, and 15.92/11.52%**. Return levels decline with size, while the gaps remain about 3.8–4.4 points. This supports robustness across size categories, not a causal capacity estimate.

The fee exercise uses only **1,762 funds**. The table notes specify sorting on estimated **dollar amounts** of total fees, not simply the contractual management-fee percentage. Incentive fees are estimated from monthly positive returns, with zero incentive fee in negative months; asset fees are percentages of beginning AUM. High-water-mark and hurdle mechanics are not fully modeled in that approximation. Low-fee-dollar portfolios have BH/DW **22.49/14.85%**, compared with **14.65/10.62%** for high-fee-dollar portfolios, but this sort is strongly related to fund size. It should not be interpreted as a clean experiment in fee rates.

Contractual restrictions do not produce uniformly significant results. Closed funds are an explicit exception: **12.39% BH and 13.87% DW**, a reversed gap of **−1.48 points**, $p=0.636$. Funds without lockups have **20.41/11.21%**, while funds with lockups have **15.85/12.92%**; the gap tests have $p=0.082$ and $0.208$. Leverage groups have similar DW returns, **11.90% without leverage** and **11.95% with leverage**, and the leveraged group's gap is not significant at 5% ($p=0.117$). The paper's broad prose about reliable differences should be read alongside these table-level exceptions.

Tables 7–8 sort annually using the previous **three years of monthly data**, requiring at least **two years**. This leaves **2,828 hedge funds**. High return-volatility funds have BH/DW **17.96/12.30%**, gap **5.66 points**, versus **13.08/9.79%**, gap **3.29 points**, for low-volatility funds. The middle group's gap is only 2.16 points and not significant at 5%; the relation is not strictly monotone.

Flow volatility gives the sharper pattern. Low, medium, and high groups have BH/DW **14.45/11.61%, 14.91/11.74%, and 18.03/9.67%**. The high group's **8.36-point** gap has $p=0.029$. Its mean monthly scaled-flow volatility is **44.32%**, versus **4.26%** for the low group, and its funds are smaller on average. Greater apparent time-weighted success coexists with substantially worse capital-weighted outcomes.

## Evidence about the mechanism and limits of inference

Table 9 computes fund-level Pearson correlations between scaled distributions and past or future returns. Because contributions are negative distributions, the past-return means **−0.219, −0.175, and −0.146** over one-, two-, and three-year horizons indicate capital follows good past performance. Future-return correlations are much smaller and positive, **0.041, 0.038, and 0.032**, consistent with inflows preceding weaker subsequent returns. Available fund counts decline with the horizon, so these are not identical samples.

The flow measure sums six monthly distributions and scales by average endpoint assets. Past and future returns compound monthly observations over the specified surrounding years. Exact handling of overlapping windows and correlation-sample minimums is not fully supplied. Figure 1 instead labels its correlations **Spearman**, groups the 7,190 funds into 100 portfolios ranked on the BH–DW gap, and reports fitted slopes **−0.20%** and **0.14%** per portfolio-rank step, with $R^2$ **29.6%** and **19.1%**. Pearson Table 9 and Spearman Figure 1 should not be merged into one statistic.

The authors interpret the stronger past relation as return chasing being the principal driver. Capacity dilution and fee extraction are proposed explanations for the weaker future relation. The data do not separately identify these channels, and a historical money-weighting gap is not itself a causal estimate of an investor's avoidable timing mistake. Changes in opportunities, optimal scale, liquidity needs, or information arriving after returns can produce flows correlated with the measured record.

The sample stops in 2006. The authors argue that subsequent crisis losses would widen the gap because assets had grown before the downturn. That is a conjecture about omitted years, not a measured result here; the exact change depends on subsequent returns, flows, defaults, and valuation treatment. A faithful summary should not import a crisis estimate from a different version.

The paper's durable result is that capital exposure over time materially changes the answer to “what did investors earn?” Replication requires the full asset-and-return panel, consistent flow timing, careful IRR root handling, and transparent entry/exit treatment. Interpretation additionally requires keeping aggregate money-weighted experience, manager investment skill, and cross-sectional lifetime dispersion separate. These distinctions make the findings useful without converting a measurement result into a stronger causal or risk-adjusted claim than the source supports.
