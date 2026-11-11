# The Persistence and Pricing of Earnings, Accruals, and Cash Flows When Firms Have Large Book-Tax Differences

Michelle Hanlon, *The Accounting Review* 80(1), January 2005, 137–166. [Source PDF](../../Finance/AbnormalReturnsEarningsAccrualsCashFlows_Hanlon_2005.pdf). Page references below use printed pages; PDF page 1 is printed page 137. The complete 30-page supplied article, including footnotes and references, was read. It contains no separate appendix.

## Why this matters

A tax footnote can change an earnings forecast without delivering a profitable stock-selection rule. This paper makes that distinction unusually clearly. Large temporary differences between reported book income and taxable income identify less persistent earnings, including both the accrual and cash-flow components. Yet the market seems to recognize the accrual implications when book income substantially exceeds taxable income. Its larger error in that group concerns cash flows: it discounts their persistence too heavily. When taxable income substantially exceeds book income, the estimated error has the familiar accrual-anomaly direction instead.

For a quantitative investor, the contribution is a conditioning variable for interpreting an accrual signal, not a recommendation simply to short the largest positive book-tax differences. The accounting information changes the mapping from current components to future earnings; the price may already incorporate some of that mapping. Equally important, the results apply to a selected sample of profitable US firms without identified net operating loss carryforwards during 1994–2000. Tax-accounting measurement drives both the signal construction and the sample restrictions.

The novel tests are three related exercises: whether large positive and negative temporary differences predict lower earnings persistence; whether the same relation holds within accruals and cash flows; and whether market-implied component persistence matches realized forecasting coefficients. Prior evidence about accrual mispricing, earnings-response coefficients, and tax-based earnings-quality indicators motivates the study. Those earlier results are not the article's original findings. The paper also contributes a direct comparison of the two signs of book-tax differences and an explicit attempt to remove special-item effects.

## What is measured, and what is not

Financial reporting and tax reporting both contain accruals, but recognize revenues and expenses under different timing rules. A temporary difference reverses: the timing of inclusion differs, while the item ultimately enters both systems. Under the balance-sheet approach of SFAS No. 109, future taxable amounts produce deferred tax liabilities and deferred tax expense; future deductible amounts produce deferred tax assets and deferred tax benefits. A positive deferred expense therefore generally corresponds to book income exceeding taxable income in the current period, conditional on the relevant accounting adjustments.

This is not a comparison of accrual accounting with cash accounting. Nor is a book-tax difference automatically evidence of misreporting. Depreciation methods, reserves, business growth, and tax planning can generate it. Interpreting it as a proxy for managerial discretion requires assumptions about what varies across firms. In particular, discretion over book reporting cannot be isolated if discretion over tax reporting also varies. Hanlon acknowledges the difficulty of separating these explanations.

The analysis focuses on temporary differences, excluding permanent differences from the main proxy. Effective tax rates and statutory-rate reconciliations also incorporate foreign and state rates, credits, tax-exempt income, and other items that do not map cleanly to accrual quality. Some permanent items can nevertheless be informative: the article discusses nondeductible acquired in-process research and development as an example. Excluding permanent differences is a measurement choice, not a claim that they never predict future earnings (pp. 140–142).

Define average total assets as $A_{it}=(TA_{it}+TA_{i,t-1})/2$, with Compustat item 6. Suppress the firm subscript below. The principal variables, all scaled by $A_t$, are

$$
E_t=\frac{PTBI_t}{A_t},\qquad C_t=\frac{CFO_t-XCFO_t+TaxPaid_t}{A_t},\qquad Q_t=E_t-C_t.
$$

Here pre-tax book income is item 170, less minority interest, item 49, when relevant. Operating cash flow is item 308; cash flow due to extraordinary items is item 124; taxes paid in cash are item 317. Thus $C$ is a pre-tax cash-flow measure and $Q$ is pre-tax accruals. This construction uses the cash-flow statement rather than inferring operating accruals from balance-sheet changes, reducing merger-related measurement errors.

The cash tax add-back is deliberate. Substituting current tax expense would double count tax benefits associated with employee stock options under the accounting regime of the sample, overstating pre-tax cash flow and understating accruals. The paper's use of pre-tax quantities also avoids treating those tax benefits as an operating accrual. Replication with later accounting standards would require revalidating that mapping.

Let the scaled temporary book-tax difference be

$$
D_t=\frac{DeferredTaxExpense_t}{0.35A_t}.
$$

Deferred tax expense is the sum of federal item 269 and foreign item 270; if unavailable, total deferred tax expense, item 50, is used. Foreign deferred taxes are included because the earnings measure includes foreign operations. State deferred taxes are excluded when the disaggregated data permit it. Dividing by the sample-period 35% statutory rate converts the tax expense into an estimated underlying income difference. This fixed rate is part of the historical design, not a current-law assumption.

Within each sample year, set $L_t=1$ for the lowest quintile of $D_t$, $P_t=1$ for its highest quintile, and classify the other three quintiles as the small-difference group. These are relative annual ranks; the paper's labels “large negative” and “large positive” describe the tails. They are not universal thresholds in dollars or asset percentages. All financial-statement variables are winsorized at the first and ninety-ninth percentiles. The article does not fully specify the ordering of winsorization, group formation, and every missing-data fallback, so those details should be fixed explicitly in any replication.

## Sample and information clock

The starting panel contains 47,507 firm-years from the CRSP–Compustat intersection in 1994–2000, incorporated in the United States, outside financial services and utilities, with nonmissing assets. The start follows implementation of SFAS No. 109 in 1993, providing a reasonably consistent deferred-tax accounting regime. Sequential exclusions are 22,242 observations missing required regression variables, 6,447 with pre-tax reporting losses, 1,518 with negative current tax expense, and 3,194 with identified net operating losses. The final sample has 14,106 firm-years from 4,048 firms (pp. 144–145).

The positive and negative groups each contain 2,823 firm-years, representing 1,663 and 1,751 firms, respectively. The middle group contains 8,460 firm-years and 3,236 firms. Firm counts overlap because membership changes over time: approximately 76% of firms appearing in the small-difference group also appear in a tail group in at least one sample year. This limits a purely fixed-firm-characteristic explanation but is not a within-firm fixed-effects identification strategy.

The exclusions are economically consequential. Loss carryforwards create deferred tax assets, while valuation allowances can obscure the temporary differences of interest. Excluding identified loss observations makes deferred tax expense more interpretable, but also removes a large and distinctive part of the equity universe. Valuation-allowance effects cannot be eliminated entirely. This is not an unconditional result for distressed companies, banks, foreign issuers, or all public companies.

The return variable is the stock's annual buy-and-hold return, including dividends, less the buy-and-hold return on a size-matched decile portfolio. The text states that accumulation begins four months after fiscal year-end; table captions sometimes say “in the fourth month.” That wording does not settle an exact day convention, which should be documented when implementing. The intended purpose is to leave time for financial-statement dissemination, not to trade on future accounting releases.

For a delisting during the holding period, the study includes the CRSP delisting return and reinvests proceeds in the stock's size-matched portfolio for the rest of the year. Missing delisting returns for performance-related codes 500 and 520–584 are replaced with −35% for NYSE/AMEX and −55% for Nasdaq. This is a substantive correction to survivorship and delisting bias, although it is not an estimate of actual liquidation proceeds for each issuer.

## Forecasting models and interpretation

The baseline pooled OLS model is

$$
E_{t+1}=a+bE_t+u_{t+1}.
$$

The group-interaction specification is

$$
E_{t+1}=a+a_LL_t+a_PP_t+bE_t+b_LE_tL_t+b_PE_tP_t+u_{t+1}.
$$

This is source equations (1)–(2), with notation simplified here. The small-difference group's slope is $b$; tail-group slopes are $b+b_L$ and $b+b_P$. Separate intercepts allow different mean earnings levels. Negative interaction slopes indicate lower conditional persistence relative to the middle group, rather than necessarily negative persistence in levels.

The component model is

$$
E_{t+1}=a+cC_t+qQ_t+u_{t+1},
$$

and its fully interacted version is

$$
E_{t+1}=a+a_LL_t+a_PP_t+cC_t+c_LC_tL_t+c_PC_tP_t+qQ_t+q_LQ_tL_t+q_PQ_tP_t+u_{t+1}.
$$

These reproduce equations (3)–(4). The pre-specified accrual hypothesis is $q_L<0$ and $q_P<0$. There is no directional ex ante hypothesis for $c_L$ or $c_P$. The cash-flow result is therefore informative but should not be represented as a separately predicted finding.

Table 3 estimates total-earnings persistence at 0.678, with adjusted $R^2=0.267$. Allowing group differences gives the middle group a slope of 0.742; the negative interaction is −0.100, $t=-4.560$, and the positive interaction −0.212, $t=-7.990$. The implied tail slopes are 0.642 and 0.530. The difference between tail interactions has $F=15.01$, $p=0.0001$. Adjusted $R^2$ increases only to 0.272. The economically meaningful slope variation should not be confused with a large increase in overall predictive fit.

Table 4 estimates the full-sample cash-flow slope at 0.752 and accrual slope at 0.490, with equality rejected at $p=0.0001$. In the interacted model, the middle group's cash-flow and accrual slopes are 0.806 and 0.557. The negative-group adjustments are −0.083 and −0.115, producing slopes of 0.723 and 0.442. The positive-group adjustments are −0.167 and −0.187, producing approximately 0.639 and 0.370. The table of separate-group pricing estimates reports the latter accrual coefficient as 0.371, a rounding-level difference. Tail differences have $p=0.0044$ for cash flows and $p=0.0393$ for accruals.

These coefficients concern next-year earnings per unit of current scaled component. They are not estimates of the persistence of the component in its own autoregression. The distinction matters when forecasting cash flow itself or constructing a valuation model.

Figure 1 uses the 9,560 observations with two prior and two subsequent years of data. The positive-difference group shows a rise in accruals around formation and a pronounced subsequent fall. It is a descriptive event-time pattern conditioned on future data availability, not an independently implementable trading portfolio. The caption appears to print operating-cash-flow item 108, whereas the model text and variable tables consistently specify item 308; the latter is the coherent implementation input, and the discrepancy should be retained in a replication log.

The descriptive statistics help distinguish component composition from persistence. Table 1's average current earnings are 0.132 of assets, versus average next-year earnings of 0.093; average current cash flow is 0.143 and accruals −0.010. These are means in a sample screened for current profitability, so the fall in average future earnings is not itself an unbiased estimate of aggregate earnings deterioration. Current earnings are selected to be positive, while the subsequent realization need not satisfy the same selection rule. Mean and median accruals are negative, partly reflecting depreciation, so the sign of an accrual alone cannot identify poor quality.

Temporary differences are not simply another ranking of total accruals. Their Pearson correlation with pre-tax accruals is −0.0083, with $p=0.3227$ in Table 1. The positive and negative groups can therefore contain similar aggregate accrual levels while differing in how tax and book rules generate those amounts. Cash flows and accruals are strongly negatively correlated, approximately −0.6285, which is also expected mechanically when they sum to earnings. Interpreting two component coefficients requires retaining that identity rather than treating cash flow and accruals as unrelated signals.

A numerical illustration clarifies the group model. Consider current scaled cash flow of 0.15 and accruals of 0.02. Using the rounded Table 4 coefficients, the middle-group forecast is about 0.1180 of assets. The negative-group forecast is about 0.1143, and the positive-group forecast about 0.0983, after including each group's intercept adjustment. These are calculations from reported coefficients, not additional observed portfolio results. Their purpose is to show that the group classification changes the entire conditional forecast, including cash-flow persistence, rather than merely deducting the book-tax difference from earnings.

This illustration is not an out-of-sample accuracy test. The article does not report forecast RMSE, predictive log scores, a holdout period, or a transaction rule tied to those estimated earnings forecasts. The small improvement in adjusted $R^2$ shows that statistical slope differences can coexist with modest aggregate prediction gains. A forecasting application would need to estimate coefficients only from earlier observations and retain the model's sample restrictions; importing pooled 1994–2000 coefficients into a strategy formed in 1994 would use future evidence.

Industry composition is checked descriptively rather than absorbed through fixed effects: no industry accounts for more than 17% of any group, and representation is broadly similar. Positive-difference firms have lower current effective tax rates, consistent with at least some tax planning, while negative-difference firms have higher sales and net-operating-asset growth. These observations help interpret possible mechanisms but do not render group assignment random. The interaction slopes remain vulnerable to omitted business-model characteristics, temporary operating shocks, and the nonlinear effects of profitability selection.

## What prices imply about persistence

For each group separately, the Mishkin system jointly estimates the forecasting equation and a return equation. For aggregate earnings,

$$
R_{t+1}=\alpha+\beta(E_{t+1}-a-b^*E_t)+\epsilon_{t+1}.
$$

For earnings components,

$$
R_{t+1}=\alpha+\beta(E_{t+1}-a-c^*C_t-q^*Q_t)+\epsilon_{t+1}.
$$

The starred coefficients represent persistence reflected in prices under this earnings-surprise return model; unstarred coefficients come from the simultaneous forecasting equation. The article uses iterative generalized nonlinear least squares. Rational-pricing restrictions are $b^*=b$, or $c^*=c$ and $q^*=q$. Likelihood-ratio statistics are compared with a chi-squared distribution with degrees of freedom equal to the number of restrictions (pp. 146–147, Table 5).

The identifying interpretation requires the earnings forecasting specification and return-surprise relation to be adequate. Omitted predictable returns, correlated omitted earnings components, or misspecified error structure can contaminate the apparent expectation coefficients. The paper notes contemporary concerns about applying Mishkin tests in accounting data. It does not supply optimization starting values, convergence tolerances, or a complete error-covariance implementation. Its pooled estimates also use multiple future years; they are not rolling forecasts a trader could have estimated in real time.

For total earnings, Table 5A reports the following market-implied versus realized slopes: negative group 0.699 versus 0.642, $p=0.4617$ for equality; middle group 0.533 versus 0.742, $p=0.0002$; positive group 0.272 versus 0.530, $p=0.0375$. Thus the largest positive differences are associated with an estimated market expectation about half the realized persistence. The finding is underestimation, even though their actual persistence is lower than the middle group's.

Table 5B provides the more useful decomposition:

| Group | Actual cash-flow slope | Price-implied cash-flow slope | Actual accrual slope | Price-implied accrual slope |
|---|---:|---:|---:|---:|
| Full sample | 0.752 | 0.482 | 0.490 | 0.700 |
| Large negative differences | 0.723 | 0.589 | 0.442 | 0.831 |
| Small differences | 0.806 | 0.521 | 0.557 | 0.726 |
| Large positive differences | 0.639 | 0.231 | 0.371 | 0.416 |

For the full sample, cash-flow equality has $p=0.0001$ and accrual equality $p=0.0011$. In the negative group, accrual equality has $p=0.0196$ while cash-flow equality has $p=0.3003$. In the middle group, both are rejected, at $p=0.0001$ and $p=0.0218$. In the positive group, cash-flow equality has $p=0.0032$ and the source reports accrual equality with likelihood-ratio statistic 0.000 and $p=1.0000$.

That last printed test is striking because the displayed unrestricted accrual coefficients are 0.416 and 0.371, not exactly equal. Their difference is small relative to the price-implied coefficient's asymptotic standard error of 0.156, so nonrejection is credible; the exact zero statistic cannot be reconstructed from the table alone. It should be quoted as the source's reported test rather than converted into proof of exact equality. Joint equality of both component coefficients is rejected in every group, including the positive group, where $p=0.0001$.

The asymmetry admits at least two readings: investors use positive book-tax differences as an earnings-quality warning, or the types of accruals generating those differences are easier to price. The design cannot distinguish these mechanisms. It also cannot justify interpreting a failure to reject as evidence that every accrual is correctly priced.

## Return regressions and the economic magnitude

A complementary test restricts the universe to December year-end firms so return windows coincide and accounting information is intended to be available before portfolio formation. There are 7,497 firm-years: 1,401 negative, 4,432 middle, and 1,664 positive. Each year the regression relates subsequent size-adjusted returns to scaled-decile ranks of accruals, log market equity, log book-to-market, beta, earnings-to-price, and the prior annual size-adjusted return:

$$
R_{t+1}=\beta_0+\beta_Qr(Q_t)+\beta_Sr(\log MVE_t)+\beta_Br(\log BM_t)+\beta_\beta r(Beta_t)+\beta_Er(EP_t)+\beta_Mr(R_t)+e_{t+1}.
$$

Each rank runs from zero to one. Beta uses a regression of monthly raw stock returns on the value-weighted market over the preceding 60 months, requiring at least 15 observations. The prior-return control captures momentum. Annual coefficients are averaged over seven years; the reported $t$ statistic uses the dispersion of those seven coefficients. This is a Fama–MacBeth-style calendar-year inference procedure, not a pooled firm-year standard error.

Table 6 gives an accrual coefficient of −0.038 for the full sample, $t=-2.496$, $p=0.046$. The negative group is −0.035, $p=0.102$; the middle group −0.038, $p=0.072$; and the positive group −0.041, $p=0.159$. The paper describes the first as approximately a 4% annual accrual-strategy return. The normalized rank coefficient permits a zero-investment regression-weighted interpretation; it is not literally the return of an equal-weighted bottom-minus-top decile portfolio.

These figures impose an important restraint on the narrative. The positive group's point estimate is not economically smaller than the other groups. Its lack of significance comes with a noisy estimate and only seven annual observations. Similarly, the text describes the negative group's evidence as marginal at 10%, while the printed $p=0.102$ is just above that threshold. Neither comparison establishes that the positive group's trading opportunity is zero or significantly different from the other groups. Transaction costs, borrow availability, portfolio turnover, and capacity are not measured, so the reported return is not a net implementable alpha.

## Robustness, measurement limits, and replication priorities

Special items are the most revealing robustness exercise. Replacing pre-tax earnings with operating earnings after depreciation, item 178, removes special items. Because associated deferred tax effects cannot be cleanly separated, Hanlon assumes all special items generate book-tax differences and subtracts them from the classification measure. Under this adjustment the accrual interactions remain negative, −0.096 for the negative group and −0.075 for the positive group; cash-flow interactions are −0.068 and −0.100. Magnitudes fall, showing that transitory items explain part of the original association.

A separate exclusion is less supportive. Removing observations with absolute special items above 1% of average assets eliminates approximately 2,900 observations. The positive-group accrual interaction becomes −0.040 with $p=0.274$. The paper acknowledges both the weakened result and the possibility that the excluded firms also manage other accounts. A faithful reading therefore cannot describe the special-item evidence as uniformly robust (p. 161, footnote 29).

Hand collection of tax-footnote balance changes for 60 firm-years reinforces the measurement problem: only 27 reconcile exactly to deferred tax expense. Mergers, discontinued operations, and extraordinary items can change deferred tax balances outside the relevant income-statement amount. Positive differences often reflect depreciation and other property-related items, followed by bad-debt reserves, pensions, miscellaneous categories, and investment-related differences. Negative differences often reflect reserves and accruals, miscellaneous items, and depreciation. The small diagnostic sample supports plausible mechanisms, not a quantified decomposition of the full panel's return effects.

Using prior-year assets as a common denominator tests whether growth in scaling assets creates apparent mean reversion. The positive-group accrual effect survives in levels, while the negative-group effect becomes insignificant. Rank regressions with that denominator recover both effects. The author interprets this as evidence that lagged assets are noisier; alternative sensitivity to scaling and outliers remains a valid practical concern. Adding an ROE interaction yields a coefficient of −0.428 and leaves the main qualitative inferences unchanged.

An additional decomposition treats $D_t$ as a discretionary-accrual proxy and $Q_t-D_t$ as the remainder. The forecasting slopes are 0.747 on cash flows, 0.481 on the remaining accruals, and 0.402 on book-tax differences. Equality of the latter two is rejected at $p=0.0005$. Calling the components “discretionary” and “nondiscretionary” is an interpretation of a proxy, not an observed managerial decision. A broader sensitivity sample including losses and estimated total differences contains 29,101 firm-years; its annual return regressions do not find a significant book-tax-difference association.

A useful replication should first reproduce the selected historical panel and its accounting identities, then separate three questions: forecasting gains from group-dependent persistence, correctness of the market-expectation model, and net returns from a fully specified portfolio. Point-in-time statement availability, restatements, exact annual return start dates, winsorization order, missing tax components, and return-regression ranking conventions require explicit implementation decisions beyond what is printed. Modern tax rates or accounting conventions should be studied as a new extension, not silently substituted into the historical definitions. The strongest source-supported conclusion is that temporary tax differences contain information about future earnings composition, while their stock-return implications depend on which component investors already understand.
