# Capital Investments and Stock Returns

**Sheridan Titman, K. C. John Wei, and Feixue Xie (2004).** *Journal of Financial and Quantitative Analysis* 39(4), December, 677–700. Source: [AbnormalReturnsCapitalInvestments_TitmanXieWei_2004.pdf](../../Finance/AbnormalReturnsCapitalInvestments_TitmanXieWei_2004.pdf). The local PDF has a JSTOR cover followed by the complete 24-page article; PDF page 2 is printed page 677 and PDF page 25 is printed page 700. All pages, endnotes, and references are covered here. There is no separate appendix. The filename's Xie–Wei ordering differs from the published author order used above.

## Why this matters

Firms that raise capital expenditure relative to their own recent sales-scaled investment history subsequently earn lower returns than firms that invest less. The paper tests this with annual accounting signals and monthly stock returns from July 1973 through June 1996. A low-minus-high abnormal-investment portfolio earns **0.168% per month after characteristic adjustment** and **0.192% after a further four-factor adjustment**. The relation persists for several postformation years, is stronger outside the 1984–1989 formation-year takeover period, and tends to be stronger where managers have more discretion through high cash flow or low debt.

The economic argument combines Jensen's free-cash-flow agency problem with investor underreaction. Investment can convey good news about opportunities and financing access, but it can also signal managers' willingness to expand for their own benefit. Investors may initially place too much weight on favorable prospects or managerial presentation and too little on overinvestment. Subsequent operating news reveals the costs. The study's earnings-announcement results are intended to discriminate expectation errors from a smoothly accruing omitted risk premium.

This is an empirical paper, not a calibrated agency model. There is no estimated managerial objective function, optimal investment policy, or causal identification of excessive investment. “Abnormal” means high relative to a simple historical intensity benchmark; it does not mean investment exceeds a model-derived optimum. The contribution is the investment-based return signal, its conditional patterns, and evidence that it is not merely long-run reversal or recent equity issuance under another name.

The authors explicitly retain alternatives in their conclusion. Low required equity returns can induce high investment, so low subsequent returns may be a cause of investment decisions rather than a consequence of bad projects. This can arise from either misvaluation or rational variation in discount rates. A favorable productivity shock could also induce investment while reducing risk. The paper's benchmarks and conditional tests constrain those accounts but do not eliminate them.

## Data, eligibility, and timing

The universe is domestic primary stocks on NYSE, AMEX, and NASDAQ. Closed-end funds, trusts, ADRs, REITs, units of beneficial interest, and other financial institutions are excluded. Monthly returns, prices, and shares come from CRSP; book equity, capital expenditure, sales, cash flow components, and long-term debt come from Compustat. One-month Treasury bills supply the risk-free rate. Financial data cover 1969–1995; return tests cover **July 1973–June 1996**, or 276 months and 23 annual formation cohorts.

A firm needs December $t-1$ and June $t$ prices, fiscal-year $t-1$ book equity, annual sales of at least **\$10 million**, nonnegative book equity, and at least two years on Compustat. The investment signal itself requires four years of accounting history. The initial 58,880 industrial firm-years average 2,560 firms per year. The four-year investment-history requirement reduces the average to 1,902; excluding firms with missing stock returns in the following test year reduces it to 1,725; sales and book-equity restrictions leave about **1,635 firms per year**.

The missing-return exclusion is consequential: the paper excludes a firm for a particular holding year if it has one or more missing monthly returns during that year. This uses information that is not necessarily known at formation and can remove exits or other difficult observations. The paper does not give a detailed delisting-return or terminal-proceeds policy. A historical reproduction should first implement the stated sample to match its tables, then separately test a formation-time eligible universe with explicit exits. It should not describe the published backtest as fully free of look-ahead selection merely because the accounting variables are lagged.

Market capitalization is price times shares. Size uses June $t$ market equity; book-to-market divides fiscal-year $t-1$ book equity by December $t-1$ market equity. Book equity is stockholders' equity plus deferred taxes and investment tax credits when available, minus preferred stock using redemption, liquidation, then par value in that order. Accounting information for fiscal years ending in calendar year $t-1$ is matched with July $t$–June $t+1$ returns. The article does not give a complete CRSP/Compustat linking protocol, original reporting dates, restatement vintage, or all missing-component rules.

## Exact investment signal

Let $CAPX_{i,s}$ be capital expenditure, Compustat item 128, and $SALE_{i,s}$ annual sales. Define expenditure intensity

$$
CE_{i,s}=\frac{CAPX_{i,s}}{SALE_{i,s}}.
$$

Equation (1), printed page 680/PDF page 5, defines the signal used at June formation year $t$ as

$$
CI_{i,t-1}=\frac{CE_{i,t-1}}{(CE_{i,t-2}+CE_{i,t-3}+CE_{i,t-4})/3}-1.
$$

The denominator averages **three expenditure-to-sales ratios**, rather than dividing aggregate past expenditure by aggregate sales. The latest intensity is compared with that average. Zero means unchanged intensity; a value of 0.5 means expenditure intensity is 50% above the past-three-year mean. The signal can increase because capital spending rises, sales fall, or both. It is therefore not pure capital growth and should not be equated with total-asset growth, investment/assets, or a residual from a Tobin's-q regression.

The economic benchmark assumes normal capital spending grows proportionately with sales. This removes a simple scale effect, but firms with unstable sales or very low prior expenditure can have extreme ratios. The source does not specify a zero-denominator rule, winsorization of the signal, or treatment of missing/negative expenditure components. Those choices matter when replicating quintile boundaries and the interaction regressions.

The authors report qualitative robustness to using the difference between current intensity and its three-year average, current intensity alone, a five-year historical mean, unscaled expenditure, and assets rather than sales as deflator. Those alternatives are described without numerical tables. They suggest the finding is not unique to one exact ratio but do not establish equality of effect sizes or prove that denominator effects are harmless.

## Portfolio construction and two layers of adjustment

Each June sort eligible stocks into five CI quintiles in ascending order and retain membership from July through the following June. Within each quintile compute value-weighted monthly returns. The low-minus-high spread averages the bottom two quintiles and subtracts the average of the top two:

$$
S_t=\frac12(R_{1,t}+R_{2,t})-\frac12(R_{4,t}+R_{5,t}).
$$

The middle quintile is omitted. The paper describes this as a \$1 long and \$1 short position across the two low and two high portfolios. This scaling is not the unhalved sum of four portfolio returns, and it differs from a bottom-minus-top quintile strategy.

The first benchmark is the Daniel–Grinblatt–Titman–Wermers style characteristic match. Sort the common-stock universe into five size groups using June NYSE size breakpoints. Within each size group split stocks into book-to-market quintiles. Within each of the resulting 25 groups split again into quintiles on prior-year returns measured through May, skipping June to reduce bid–ask and short-horizon reversal effects. The result is 125 annually rebalanced, value-weighted benchmark portfolios. Only the initial size split is explicitly NYSE-breakpoint based; the subsequent splits are conditional equal-count sorts.

For stock $i$ assigned to benchmark cell $h(i,t)$, equation (2) is

$$
R^{CH}_{i,t}=R_{i,t}-R_{h(i,t),t}.
$$

Average these stock-level adjusted returns with the test portfolio's value weights. The resulting $AR_{p,t}$ is already a return relative to a characteristic benchmark, not a raw stock return minus the Treasury-bill rate. The second adjustment estimates

$$
AR_{p,t}=\alpha_p+\beta_{H,p}HML_t+\beta_{S,p}SMB_t
+\beta_{M,p}(R_{M,t}-R_{f,t})+\beta_{P,p}PR1YR_t+\varepsilon_{p,t}.
$$

This regression is fitted to **characteristic-adjusted** returns. Regressing raw excess returns on four factors would estimate a different object. The tables label its intercept “FF Alpha,” although the specification includes the momentum factor and is described as Carhart's four-factor model. The article describes PR1YR as high-minus-low prior-year return groups split at 50%, skipping the formation month. Exact replication should obtain or reconstruct that definition rather than automatically substitute a modern factor series whose construction differs.

A characteristic-adjusted spread need not equal the raw low-minus-high stock portfolio. Algebraically it also contains the negative of the long leg's benchmark exposure and the positive of the short leg's benchmark exposure. Therefore 0.168% is a residual performance statistic, not a directly reported net return on a two-leg implementable trade. The second regression removes remaining linear factor exposure; it does not turn the statistic into a cost-inclusive arbitrage return.

A simple accounting example clarifies what the signal controls. Suppose the last three capital-expenditure/sales ratios are 0.05, 0.05, and 0.05, so their mean is 0.05. If the latest ratio is 0.075, then $CI=0.50$. The same signal results whether expenditure rises by 50% at unchanged sales or unchanged expenditure is divided by sales one-third lower. This is not a flaw in the definition: both are unusually high expenditure intensity relative to the firm's history. It does mean that interpreting every high-CI observation as expansion requires checking the numerator and denominator separately. The paper's alternative deflators are relevant robustness checks, but their untabulated status leaves the size of this distinction unresolved.

The two benchmark layers also have a precise algebraic interpretation. Let $R_{p,t}$ denote the raw test-portfolio return and $B_{p,t}$ its value-weighted sum of matched benchmark returns. Then $AR_{p,t}=R_{p,t}-B_{p,t}$. Under identical regression dates and factor regressors, linearity of ordinary least squares gives

$$
\hat\alpha(AR_p)=\hat\alpha(R_p)-\hat\alpha(B_p).
$$

Thus the table's second-stage intercept is the raw portfolio's factor intercept relative to the factor intercept of the composite characteristic benchmark. It need not equal the raw portfolio's four-factor alpha. This identity is a useful code check and makes clear why applying a risk-free subtraction a second time or substituting a different benchmark portfolio changes the result. Likewise, a unit-capital implementation of the residual trade would have to finance and execute the benchmark hedge as well as the CI legs. The statistical adjustment is valid as a performance comparison without assuming that those extra transactions are free.

## Main return evidence, persistence, and takeover period

Tables 1–2, printed pages 684–686/PDF pages 9–11, give the main monthly results. All numbers below are percentage points per month.

| CI portfolio | Characteristic-adjusted mean | Four-factor intercept |
|---|---:|---:|
| Lowest | 0.042 | −0.012 |
| 2 | 0.083 | 0.119 |
| 3 | 0.055 | 0.058 |
| 4 | −0.083 | −0.103 |
| Highest | −0.127 | −0.173 |
| Low-two minus high-two | **0.168** | **0.192** |

The spread's mean t-statistic is 2.91 and its four-factor alpha t-statistic 3.25. Its median adjusted return is 0.119%. The average high-investment leg underperforms by about 0.105% per month, while the low-investment leg outperforms by about 0.062%, so the effect is asymmetric. Except for the lowest quintile, mean adjusted returns decrease with CI. Wilks' Lambda tests reject equality across the five portfolio means, F = 2.08, p = 0.026, and across factor-adjusted means, F = 4.68, p = 0.001. Kruskal–Wallis tests also reject equal medians.

Table 1's distribution column labeled standard deviation is printed as 0.009 for the spread while means, quartiles, and extremes are shown in percentage units. Taken literally as 0.009 percentage points, it is incompatible with an interquartile range from −0.462% to 0.779%. It appears to use decimal-return scaling in that column. The paper does not explain the mismatch; use the underlying series to resolve it and do not calculate a Sharpe ratio from the printed column without checking units.

Postformation annual spread returns average 2.02%, 2.26%, 1.91%, 1.85%, and 1.64% in years one through five, with t-statistics 2.86, 2.88, 2.46, 2.10, and 1.81. Year six is reported as 1.05% and insignificant. The fifth-year result is weaker than the earlier years under a conventional two-sided 5% rule. Successive horizons use fewer formation cohorts because the sample ends in June 1996; they are not five independent same-sample estimates. The source reports a five-year cumulative figure of 8.10%, t = 2.55, but its displayed cohort “cumulative” values match sums of annual columns: for 1973, −0.95 + 9.22 + 2.65 + 5.79 + 8.60 is about 25.31%, compared with printed 25.32%. This should be reconciled before interpreting the cumulative column as fully compounded wealth.

The takeover split is defined as **formation years 1984–1989**, corresponding to monthly returns **July 1984–June 1990**. Outside that interval the CI spread earns 0.277% characteristic-adjusted and 0.312% after four-factor adjustment, the latter with t = 4.42. During the interval the corresponding values are −0.144% and −0.124%, both insignificant in their means. The non-takeover minus takeover differences are 0.421% and 0.436% monthly. All six annual first-year spreads for formation years 1984–1989 are negative; outside them, 15 of 17 are positive.

The authors associate this reversal with hostile takeovers disciplining or acquiring overinvesting firms. That is a plausible interpretation of a striking historical split, but the dates were examined together with the return pattern, and no firm-level takeover treatment or instrument is used. Changes in discount rates, industries, credit conditions, and selection may also differ across those years. The paper's sign-frequency argument assumes an appropriate null for annual signs; persistence and the chosen partition complicate a simple independent 50–50 calculation.

## Earnings-announcement returns

The event study uses Compustat quarterly announcement dates and market-adjusted daily returns over three days centered on each release. Within each CI group, equally weight stock event returns for each quarter and sum four quarterly event averages for each postformation year. For comparison, equally weight individual annual returns obtained by compounding twelve monthly **market-adjusted** returns. This differs both in benchmark and weighting from the main value-weighted characteristic-adjusted tests. Daily characteristic benchmarks were unavailable, which the authors give as the reason for using the market adjustment.

Table 3, printed page 689/PDF page 14, reports:

| Postformation year | Spread event return | Spread annual return | Event/annual ratio | Non-takeover event return | Takeover event return |
|---|---:|---:|---:|---:|---:|
| 1 | 0.792% | 3.330% | 23.78% | 1.099% | −0.079% |
| 2 | 0.542% | 3.450% | 15.71% | 0.856% | −0.295% |
| 3 | 0.460% | 3.225% | 14.26% | 0.834% | −0.475% |
| 4 | 0.358% | 3.056% | 11.72% | 0.808% | −0.693% |
| 5 | 0.334% | 2.671% | 12.50% | 0.769% | −0.608% |

The full-sample event spread is significant in the first three years. Outside takeover years it remains positive across all five; during takeover years it is negative and insignificant. In year one the five event-return levels decline from 1.941% to 1.207%, 0.931%, 0.813%, and 0.751%. These are positive market-adjusted event returns for every quintile: the finding is that high investors receive relatively less favorable announcement returns, not that every high-investment announcement has a negative average return.

Roughly one quarter of the first-year spread occurs in about twelve announcement-window trading days, which is consistent with expectation correction. It does not prove that the rest is unrelated to information or that announcement risk is constant. Firms' scheduled disclosures can concentrate both fundamental risk and information processing. Missing announcements, overlapping windows, and quarterly coverage rules are not fully documented, and the switch of benchmark means that the ratio cannot simply be applied to the main 0.168% monthly spread.

## Investment discretion: cash flow, debt, and interactions

The cash-flow variable is operating income before depreciation minus interest expense, taxes, preferred dividends, and common dividends, divided by total assets. It measures internally available cash after these payouts; it is not a direct cash-flow-statement CFO series. Split firms at the annual median and then form five CI quintiles separately within each half. Define each half's CI spread as before, and subtract the low-cash-flow spread from the high-cash-flow spread.

Table 4, printed page 691/PDF page 16, shows all-sample characteristic-adjusted spreads of 0.078% for low cash flow and 0.227% for high cash flow; their 0.149% difference is not significant. Four-factor alphas are 0.059% and 0.256%; their **0.197% difference is only marginally significant at 10%**. Outside takeover years the corresponding alphas are 0.164% and 0.368%, a 0.204% difference, again marginal. The pattern supports greater investment sensitivity when internal resources are abundant, but “significant in one group and not the other” should not substitute for the weaker direct difference test.

The debt variable is labeled debt-to-assets, but its actual definition is

$$
DA_{i,t-1}=\frac{LTD_{i,t-1}}{LTD_{i,t-1}+ME_{i,t-1}},
$$

where $LTD$ is long-term debt and $ME$ is market equity. The denominator is not book total assets. The paper does not fully specify the market-equity date in this subsection; it should be made explicit in code. Form low/high DA halves at the median and CI quintiles within each. The agency argument predicts a larger CI spread among low-debt firms because debt may constrain discretionary investment.

Table 5, printed page 693/PDF page 18, gives low/high-debt adjusted spreads of 0.225% and 0.099%, a high-minus-low difference of −0.126% that is insignificant. Their factor alphas are 0.286% and 0.080%, a difference of **−0.206%**, marginally significant at 10%. Outside takeover years the alphas are 0.417% and 0.187%, difference −0.231%. Thus the cash-flow and debt stories have the expected directions, but the portfolio evidence on differential effects is less decisive than the overall investment effect.

The Fama–MacBeth analysis estimates monthly regressions with CI and its interactions with high-cash-flow and high-debt indicators. The joint model is

$$
Y_{i,t}=\lambda_{0,t}+\lambda_{1,t}CI_{i,t-1}
+\lambda_{2,t}CI_{i,t-1}DCF_{i,t-1}
+\lambda_{3,t}CI_{i,t-1}DDA_{i,t-1}+e_{i,t}.
$$

Models 1 and 2 omit one interaction each. Crucially, Table 6 describes $Y$ as the individual characteristic-adjusted return multiplied by the firm's market-value share **within its CI rank**, and then multiplied by 1,000. This is an unusual weighted dependent variable, not ordinary stock returns estimated by value-weighted least squares. Replacing it with WLS changes the objective and coefficients. The top and bottom 1.5% of observations by the adjusted-return variable are excluded; the article does not clarify every ordering detail between weighting and trimming.

For all years, the joint coefficients are $\lambda_1=-0.95$ (t = −2.76), $\lambda_2=-0.73$ (t = −2.04), and $\lambda_3=0.38$ (t = 1.25). Outside takeover years they are −1.25 (−2.85), −0.81 (−1.79), and 0.46 (1.20); during takeover years they are −0.07 (−0.18), −0.49 (−1.03), and 0.17 (0.37). The independent cash-flow effect is stronger than the independent debt effect. Because the model omits standalone DCF and DDA terms, it restricts conditional groups to share an intercept at CI = 0. The interaction interpretation should be evaluated under that maintained restriction rather than assumed to be a fully flexible conditional-mean comparison.

## Reversal, issuance, and replication concerns

Past five-year raw stock returns rise across CI quintiles from 81.53% to 114.50%, 132.85%, 145.64%, and 153.77%. To test whether investment merely proxies for long-term reversal, independently cross five past-return groups with five CI groups. Table 7 reports a positive average CI spread of 0.159% per month for all years and 0.285% outside takeover years, while the corresponding past-return spreads are 0.093% and 0.152% and insignificant. The takeover CI average is −0.179%. Three-year prior-return sorts and sequential sorts reportedly preserve the result.

Some Table 7 aggregates require clarification: the displayed all-years CI row spreads average about 0.205%, not the stated 0.159%, and the reported PR-spread aggregate likewise does not equal the simple average of the displayed row. The caption says averages of the five spreads, so unreported weighting or a table error must be resolved with underlying series. The caption also prints a holding interval ending in June $t-1$, inconsistent with the rest of the paper's July $t$–June $t+1$ design. These issues do not justify substituting new numbers for the reported findings, but they prevent exact table replication from the printed aggregates alone.

The issuance exclusion removes firms that issued new equity in any of the preceding five years. Table 8, printed page 698/PDF page 23, reports a CI spread of 0.186% monthly after characteristic adjustment, t = 3.34, and 0.208% after factor adjustment, t = 3.43. Outside takeover years these rise to 0.299% and 0.336%; during takeover years they are −0.133% and −0.126%. Thus the investment effect is not confined to recent issuers in this sample. The paper does not provide an issuance database identifier or detailed classification of IPOs, SEOs, and other equity transactions, which is needed to reproduce the exclusion.

A replication should first match the eligibility waterfall and CI distribution, then the 125 benchmarks, monthly adjusted quintile returns, factor regressions, and takeover calendar mapping. Keep raw returns, characteristic residuals, factor residual-plus-intercept series, and event returns in separate fields. The median “alpha series” in the tables means estimated alpha plus each regression residual, not a series of rolling intercept estimates. Preserve that definition when reproducing Wilcoxon and Kruskal–Wallis tests. The article does not specify code, full factor series provenance, covariance corrections for long-horizon overlap, portfolio weight-drift details, or sparse-cell rules.

For implementation, none of the reported returns includes transaction costs, borrow fees, short recalls, financing, slippage, market impact, or a capital constraint. Annual signal refresh does not imply zero turnover inside a value-weighted or benchmark-hedged strategy. Four-year accounting history and the sales floor also exclude young firms, limiting transfer to modern asset-light growth universes. The modest 0.168% monthly residual spread is especially sensitive to what must actually be traded to neutralize its benchmark exposures.

The defensible research conclusion is that this historical capital-expenditure-intensity signal predicts returns beyond the specified size, value, momentum, reversal, and issuance controls. Cash-flow, debt, takeover, and announcement patterns make the overinvestment-underreaction account coherent. They do not identify investment as the causal source of low returns or prove that a modern net strategy remains profitable. The signal is a useful building block for conditional investment research, with its sample-selection rule, benchmark construction, unusual regression weighting, and source-table inconsistencies treated as part of the replication problem.
