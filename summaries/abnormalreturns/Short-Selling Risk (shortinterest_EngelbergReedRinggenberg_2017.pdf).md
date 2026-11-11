# Short-Selling Risk

Joseph E. Engelberg, Adam V. Reed, and Matthew C. Ringgenberg. Accepted January 21, 2017; subsequently published in *The Journal of Finance* 73(2), April 2018, pp. 755–786. [DOI and publication record](https://doi.org/10.1111/jofi.12601).

**Source:** [shortinterest_EngelbergReedRinggenberg_2017.pdf](../../Finance/shortinterest_EngelbergReedRinggenberg_2017.pdf), a 63-page accepted manuscript. All source-page references below refer to that manuscript, including its tables, figures, and endnotes. The publisher lists a separate Internet Appendix; it is not embedded in this file, and attempts to retrieve it returned an access error. Its robustness results are identified below as claims reported by the article, not independently inspected appendix evidence.

## Why this matters

The cost of maintaining a short position is uncertain even when today's stock-loan fee is known. A lender may raise the fee, withdraw available shares, or recall a loan before the anticipated price correction occurs. Two apparently identical short opportunities can therefore have different attractiveness because their future lending conditions have different uncertainty. A strategy that subtracts the current fee from an expected stock return treats an important state variable as fixed.

The paper's main innovation is empirical measurement of this dynamic constraint. It constructs a forecast of lending-fee variability, called **ShortRisk**, and relates it to subsequent stock returns, price delay, option-implied mispricing, and short-sale activity. The distinctive prediction is that lending uncertainty matters more for arbitrage positions expected to remain open longer. The option setting supplies an observable horizon through expiration dates, which ordinary stock-return anomalies generally lack.

The strongest unconditional portfolio result is a 1.08% monthly gross return spread and a 0.80% monthly Fama–French five-factor alpha for buying low-ShortRisk stocks and shorting high-ShortRisk stocks. The result is concentrated in micro and small companies. The value-weighted large-stock alpha is approximately zero. These findings support a limits-to-arbitrage interpretation, but they do not establish that a trader can earn the reported alpha after paying the very borrowing risks and costs that motivate the paper.

## Economic mechanism and what is actually modeled

The authors draw on models of equilibrium stock lending and constrained arbitrage rather than estimate a new structural equilibrium. A short seller must borrow shares, post collateral, pay a fee while the loan remains open, and close or refinance the position if lending conditions deteriorate. A recall and a sharp fee increase can be alternative manifestations of the same shortage of lendable stock. Treating them as unrelated independent risks would miss this common mechanism.

A longer horizon exposes the position to more opportunities for adverse changes in loan conditions. The paper therefore predicts less shorting, more persistent overpricing, and poorer price efficiency when future lending conditions are uncertain, especially for positions with distant expected convergence dates. The empirical risk measure is a forecast of fee variability. It is not a directly estimated probability of recall, a distribution of realized short-sale profits, or a structural investor risk-aversion parameter.

There is also an adverse covariance mechanism. If a stock rises sharply, a short seller is already losing money. If loan fees simultaneously rise or loan supply contracts, the financing environment worsens at the same time. The paper examines this association separately from the ShortRisk portfolio sorts. Its evidence is observational: it does not instrument an exogenous change in lending uncertainty or randomly assign investors different recall risks.

## Data, coverage, and exclusions

The main panel combines Markit securities-lending data with CRSP, Compustat, NYSE TAQ Regulation SHO short-sale records, OptionMetrics, and SEC failures-to-deliver data. Markit collects data from beneficial owners, hedge funds, investment banks, lending agents, and prime brokers. The contributors are believed to cover most U.S. equity loans, but the file is not a census of every bilateral lending contract.

The stated sample runs from July 1, 2006 through December 31, 2011 and includes approximately 4,500 U.S. equities and 220,000 firm-month observations before specification-specific losses. Non-U.S. companies, ADRs, and ETFs are excluded. Stocks priced below \$5 or with market capitalization below \$10 million are dropped, and a firm must have at least 50 nonmissing days in a year. The article does not fully specify how this annual eligibility rule is implemented in real time; requiring observations later in the same year can matter for a prospective trading reconstruction.

The lending variables are defined as follows. **Short Interest** is the quantity of borrowed shares divided by shares outstanding. **Loan Supply** is shares actively available for lending, also divided by shares outstanding. **Utilization** is shares borrowed divided by lendable supply. **Loan Fee** is the share-weighted average fee across outstanding loans, expressed in annual basis points. **New Loan Fee** is the corresponding weighted fee for loans initiated over the preceding day. **Loan Length** is the weighted number of days for which transactions have been open.

Table I shows substantial skewness. Mean loan supply is 18.56% of shares outstanding, mean short interest is 4.43%, and median short interest is 2.18%. The median annual fee is 11.57 basis points, but the mean is 85.13 and the 99th percentile is 1,479.29. Median loan age is 65 days and mean age is 81.46 days. A low median fee does not imply negligible exposure for expensive-to-borrow stocks held for several months. The mean of each firm's own 99th-percentile fee is 301.42 basis points, compared with 6.75 at the corresponding first percentile, documenting substantial within-stock variation.

Failures to deliver are outstanding unsettled balances, not counts of newly failed trades. The authors record zero when the SEC does not report a balance below the stated 10,000-share disclosure threshold. Consequently, a recorded zero can mean an unreported small balance. Mean failed shares are 0.36% of shares outstanding and the median is zero. A replication must preserve this censoring convention and verify the disclosure rules applicable to the historical data vintage.

For options, the sample excludes contracts with bid–ask spreads above 50%, absolute log moneyness above 0.5, or nonpositive implied volatility. Remaining maturities are greater than six and less than 181 days. The short-sale data exclude canceled and invalid trades. Book equity is shareholder equity less preferred stock plus deferred taxes and investment tax credits, with shareholder-equity fallbacks to common plus preferred equity and then assets less liabilities. Fama–French factors and NYSE size breakpoints come from Kenneth French's data library; the mispricing score comes from Stambaugh, Yu, and Yuan.

## Constructing ShortRisk

Section II.C first computes the natural logarithm of each stock's variance of daily outstanding-loan fees over the preceding twelve months. Denote the intended transformed series by

$$
v_{i,t}=\log\left(\widehat{\operatorname{Var}}\{f_{i,d}:d\text{ in the trailing annual window at }t\}\right).
$$

The article's displayed equation abbreviates the dependent variable as $\operatorname{Var}(LoanFee_{i,t+1})$, although the prose specifies a log variance. The note uses $v$ to keep that distinction visible. A negative ShortRisk value can therefore be meaningful on the transformed scale; it does not imply a negative physical variance. Table I gives a ShortRisk mean of 4.04, median 3.63, standard deviation 3.00, first percentile −0.92, and 99th percentile 12.11.

The forecasting model is an OLS panel with firm fixed effects:

$$
v_{i,t+1}=a_i+\beta_1 V^{new}_{i,t}
+\beta_2 V^{util}_{i,t}+\beta_3 T^{new}_{i,t}
+\beta_4 T^{util}_{i,t}+\gamma'Z_{i,t}+u_{i,t+1}.
$$

The fitted value is ShortRisk. The four named lending predictors measure variation in new-loan fees, log variation in utilization, and upper-tail measures of the two series. The additional characteristics in the full specification are lagged fee risk; log one plus failed shares as a proportion of shares outstanding; log turnover; log relative bid–ask spread; log market capitalization; log monthly daily-return volatility; an indicator for a dividend that month; an IPO in the preceding 90 days; and listed options. Table II uses standard errors clustered by firm and date.

The full model contains 162,657 observations and reports $R^2=0.97$. The lagged fee-risk coefficient is 0.9100, with $t=65.42$. The coefficients on new-fee variation and utilization variation are 0.0611 and 0.0151, with $t=5.42$ and $t=3.39$. The new-fee tail measure is weakly positive, while the utilization-tail coefficient is not significant. Failed deliveries, turnover, relative spread, and return volatility have positive coefficients. The IPO indicator is 0.1533 with $t=2.06$, and listed options is −0.0434 with $t=-2.47$. The dividend indicator is not significant in the displayed table, despite imprecise surrounding prose that conflates the dividend and IPO statements.

The high fit should not be interpreted as forecasting an independent future year's lending shocks with 97% accuracy. The baseline target is described as a trailing annual variance updated monthly, so adjacent targets share most of their underlying daily observations. Persistence and overlapping windows can explain much of the fit. The paper does not provide an independently held-out forecasting evaluation, a rolling coefficient-estimation schedule, or a complete initialization rule for the earliest observations.

### Definition problems that affect reproduction

Several details in this accepted manuscript cannot be reconciled by transcription alone:

- The main data section correctly defines utilization as borrowing divided by lending supply, while Section II.C describes the inverse ratio in words. The ordinary borrowing-to-supply definition is the coherent economic interpretation, but the inconsistency should be checked against original code.
- New-fee variation is described as a variance, whereas utilization variation is explicitly a log variance. The exact transformation of every predictor is not consistently documented across prose and labels. Silently logging all four variables would impose an unreported specification.
- The tail measures are called normal-distribution 99th percentiles. For a normal variable, that quantile is $\mu+2.33\sigma$. Endnote ix instead prints $\mu+2.33\operatorname{Var}$, using a 250-trading-day window. The latter is dimensionally inconsistent with a quantile. The intended quantile and the printed formula should be treated as separate replication branches until code or a correction resolves them.
- The manuscript alternates between new-loan and outstanding-loan fees when describing the tail-fee input. It also does not specify the treatment of zero sample variances before taking logs.

These are material input choices because the fitted score is used repeatedly as a generated regressor. An implementation should retain the source labels, state its interpretation explicitly, and compare sensitivity to plausible alternatives rather than claiming exact reproduction from the PDF alone.

## Portfolio experiment and its limits

Each month, the authors sort stocks into quintiles using the previous month's ShortRisk and hold equal-weighted portfolios for one month. The low-risk and high-risk portfolios earn reported average monthly returns of +0.58% and −0.49%, respectively. The displayed low-minus-high spread is 1.08%, with $t=9.55$; the slight difference from subtracting rounded endpoint numbers is ordinary rounding.

Next, stocks are first sorted into short-interest quintiles and then into ShortRisk quintiles within each group. This conditional sorting separates the risk measure from the familiar association between high short interest and low future returns. The five conditional low-minus-high return spreads range from 0.63% to 1.19% monthly. These are separate within-short-interest experiments, not an independent two-way sort with common unconditional risk breakpoints.

Table IV regresses portfolio excess returns on the Fama–French market, SMB, HML, RMW, and CMA factors. The all-stock low-minus-high alpha is **0.80% monthly**, with $t=7.71$, corresponding to the article's simple annualization of 9.6%. The low- and high-risk leg alphas are +0.22% and −0.58%. The manuscript's conclusion separately says 75 basis points; the note uses the displayed 80-basis-point table result and records the discrepancy.

The conditional five-factor result has an important exception: in the **lowest short-interest quintile**, the low-minus-high alpha is −0.19% with $t=-0.65$. The other four conditional alphas are positive and significant: 1.15%, 1.17%, 0.64%, and 0.80%. Thus the factor-adjusted effect is not significant in every short-interest group, even though the raw return spreads are.

Size splits use NYSE breakpoints: micro below the 20th percentile, small from the 20th to below the 50th percentile, and big at or above the 50th percentile. Within each size group the authors sort on ShortRisk and form value-weighted portfolios. These groups represent approximately 44%, 31%, and 25% of sample stocks. Their raw spreads are 1.04%, 0.65%, and 0.24%; the corresponding five-factor alphas are 0.88%, 0.38%, and **−0.02%**. The large-stock alpha has $t=-0.14$. This is a strong qualification for capacity and generality.

These are gross research portfolios. The article does not supply a net-of-borrow-fee, net-of-execution-cost strategy with observed recalls, margin calls, financing charges, or feasible position sizes. Nor does it establish that all fitted-score coefficients and firm effects were estimated only with information available at each historical formation date. Sorting on lagged predictor values alone does not eliminate look-ahead if the mapping from predictors to risk was fitted with later outcomes.

## Cross-sectional return regressions

Table V runs 63 monthly Fama–MacBeth cross-sectional regressions with the subsequent month's buy-and-hold excess return as the outcome:

$$
r^e_{i,t+1}=\alpha_t+b_t ShortRisk_{i,t}
+c_t SI_{i,t}+d_t'X_{i,t}+\epsilon_{i,t+1}.
$$

Controls include log market-to-book, lagged log capitalization, log idiosyncratic volatility, log closing relative spread, recent returns, current loan fee, and loan supply. The actual table contains both $Return_t$ and $Return_{t-1}$ in the expanded specifications, even though the shorter textual description emphasizes only one lag. End-of-month short interest is borrowed shares divided by shares outstanding.

Idiosyncratic volatility is the monthly standard deviation of daily residuals from a three-factor model. Endnote xiii says the factor regression uses daily observations from the **entire sample period**. This is appropriate to record as the authors' research construction, but a real-time replication should also estimate betas with a trailing or expanding historical window and report how the result changes.

The baseline ShortRisk coefficient is −0.0013 with $t=-4.31$. Multiplying by its standard deviation of 3 yields approximately −0.0039 in decimal returns, or **−39 basis points per month**. In the fuller specification the coefficient is −0.0008 with $t=-2.80$, implying approximately −24 basis points for the same score change. The table title calls the dependent variable percentage returns, but the article's own economic interpretation is consistent with these coefficient calculations in decimal-return units. Unit reconciliation is necessary before using the coefficients numerically.

The final specification adds the Stambaugh–Yu–Yuan score, an aggregate of eleven anomalies that excludes short-selling anomalies, and its interaction with ShortRisk. The interaction is −0.0039 with $t=-2.74$. The ShortRisk main effect becomes +0.0013, so its conditional slope is $0.0013-0.0039MISP$, not a constant negative coefficient in this interacted model. The article interprets the interaction as stronger future underperformance for stocks that are both overpriced and risky to short. Its reported movement from joint median to joint 90th-percentile values lowers the next month's return by 22 basis points. Exact replication requires the score's original scale and vintage, rather than an arbitrary normalized rank.

The bootstrap documentation is inconsistent: Table V says 500 block-bootstrap replications, whereas endnote xiv says 200. The note also reports qualitatively unchanged results using Newey–West standard errors with three lags. Neither the precise bootstrap block construction nor all first-stage re-estimation details are supplied. Because ShortRisk is generated, a rigorous reconstruction should propagate first-stage estimation uncertainty and document whether it refits the score within every bootstrap draw.

## Price efficiency experiment

For each stock-year, estimate weekly returns on the contemporaneous CRSP value-weighted market return and four weekly lags:

$$
r_{i,w}=a+\beta r_{M,w}+\sum_{j=1}^{4}\delta_j r_{M,w-j}+e_{i,w}.
$$

The principal delay measure compares the full regression's fit with a restricted regression excluding all lagged market returns:

$$
D1=1-\frac{R^2_{\delta_1=\cdots=\delta_4=0}}{R^2_{full}}.
$$

Larger values mean lagged market information contributes more explanatory power. The manuscript also defines $D2=\sum_{j=1}^{4}|\delta_j|/(|\beta|+\sum_{j=1}^{4}|\delta_j|)$, but Table VI reports $D1$. This printed $D2$ has no additional lag-index weighting; a researcher should not substitute a differently weighted delay statistic without labeling the change.

The annual panel regresses delay on ShortRisk, loan supply, and controls, with year fixed effects. Expanded controls include failures to deliver, log capitalization, log volume relative to shares outstanding, spread, listed options, and current loan fee. Annual means are used for the indicated lending and market variables. Fee is divided by 100 in this table's scaling. The fullest specifications contain 14,904 firm-years and have $R^2=0.30$.

The ShortRisk coefficient is 0.0072 in column 2 and 0.0070 in column 3, with $t=7.32$ and $t=6.72$. The article's economic calculation is

$$
\frac{0.0072\times3.00}{0.32}=0.0675.
$$

Thus a one-standard-deviation score increase corresponds to a roughly **6.8% increase relative to mean delay**, not 6.8 percentage points of stock returns. The absolute delay change is about 0.0216. Loan supply is negatively related to delay. The result is consistent with lending uncertainty slowing incorporation of information, but contemporaneous annual aggregation and omitted firm conditions limit a causal interpretation. Inference uses a stated 200-replication block bootstrap.

## Options identify an expected convergence horizon

The paper measures put–call disparity as the log ratio of observed stock price to the synthetic stock price implied by matched options. Positive disparity indicates that stock is expensive relative to its synthetic counterpart. In the frictionless European, no-dividend illustration, the synthetic price is $C-P+Ke^{-r\tau}$; this equation explains the economic comparison but is not a complete implementation recipe for the paper's U.S. option sample. Dividends, early exercise, bid–ask selection, and rates require conventions that the manuscript largely delegates to the cited methodology.

A short-stock/long-synthetic-stock trade has an identifiable convergence horizon at option expiration. To align the uncertainty measure with that horizon, the authors reestimate fee-variance forecasting regressions for successive future windows: days 1–30, 31–60, 61–90, and so on. The resulting horizon-specific forecast is matched to an option's expiration window. This differs from mechanically multiplying the baseline annual trailing variance by time to maturity. The text does not fully resolve whether a given construction represents a terminal bucket's variability or cumulative variability over the whole holding period; that detail should be obtained from implementation code.

Table VII estimates firm- and date-fixed-effect regressions of disparity or short-sale volume on ShortRisk, months to expiration, and their interaction. Controls vary by column and include current loan fee, option bid–ask spread, stock spread, short interest, and, for the volume equations, put–call disparity. The disparity sample contains about 5.05 million observations; the short-volume sample has about 1.40 million. Multiple option observations can correspond to the same stock-day short-volume outcome, so option-level weighting and bootstrap blocks matter for reproduction.

In disparity column 3, the coefficients on maturity, ShortRisk, and their interaction are 0.0122, −0.0348, and 0.0303. The interaction has $t=18.13$. Consequently, the conditional risk slope is $-0.0348+0.0303H$, where $H$ is months to expiration. It becomes positive above approximately 1.15 months; the result should not be described as an unconditionally positive ShortRisk main effect at every maturity.

Using the article's mean disparity of 0.46, score quartiles of 1.54 and 5.38, and maturity quartiles of two and five months, the three displayed terms imply relative contributions of approximately 13.9% and 149.7% of mean disparity. These are scaled contributions from selected regression terms, with other terms held aside. They are not complete fitted conditional means or experimentally identified percentage treatment effects. The table's disparity scaling should also be checked before equating its units with an unscaled log-price ratio.

For short volume, column 6 gives maturity −0.0006, ShortRisk −0.0636, and interaction −0.0055, with interaction $t=-3.57$. Using the stated unconditional volume mean of 2.26, the same quartile combinations give approximately **−5.14% and −21.82%** relative contributions. This closely reproduces the text's 5.1% and 21.7% descriptions. Endnote xix prints different coefficients, which do not reproduce its high-quartile percentage; the displayed table is the consistent basis for the calculation. Column 4's noninteracted score coefficient, −0.0763, is only significant at the 10% level, with $t=-1.74$, although the interaction evidence is stronger.

There is another scaling ambiguity: Table I describes short volume using a log-one-plus transformation and a factor of 100, whereas Table VII describes shares shorted as a fraction of shares outstanding and labels the outcome in percent. Exact coefficient reproduction requires settling that discrepancy. The article does not directly observe which short trades implement the specific option arbitrage, so the results associate aggregate short activity with the proposed opportunity and horizon.

## Adverse stock moves and lending conditions

Figures 2 and 3 sort stocks daily into 50 bins by their preceding 20-trading-day return. Loan fees are elevated at both return extremes, and lending supply is lower toward the extremes. The prose reports a mean fee of 236 annual basis points among the top 2% past-return stocks, compared with the sample mean near 85, and loan supply near 12% compared with about 18%. These are descriptive levels; they do not control for all differences between extreme-return and ordinary stocks.

Table VIII instead uses top- and bottom-decile past-return indicators, month-year effects, and optionally firm effects. In the within-firm fee regression, bottom- and top-decile indicators are 0.1337 and 0.0953 in the table's fee scaling, interpreted in the text as about 13 and 10 annual basis points. In the supply regression, the top-decile coefficient is −0.7117, a reduction of about 0.71 percentage points of shares outstanding; the bottom-decile coefficient is small and insignificant once firm effects are included. The regressions cluster standard errors by firm and date.

The relevant mechanism is that a rising stock can both hurt the short position and reduce access to affordable borrowing. It is not enough to simulate stock-return risk independently of financing risk. These regressions establish covariation, however, and do not identify the structural direction of causality between price movements, investor disagreement, and lending conditions.

## Replication priorities and practical interpretation

A useful implementation should first reproduce the lending-variable definitions and their summary statistics, keeping annual fee units, percentage holdings, and transformed variances distinct. It should then implement each documented ShortRisk interpretation transparently, estimate the first-stage panel, and save both fitted values and the information cutoff used to create them. A separate prospective version should fit parameters and firm effects using only historical observations and should make eligibility and accounting-data availability point-in-time.

The next stage should reproduce the unconditional, short-interest-conditional, and size-conditional portfolios, including the weak large-cap result; the Fama–MacBeth models; the annual delay regressions; and finally the horizon-matched option regressions. This order isolates whether discrepancies arise from the risk score, portfolio construction, or the more complicated option joins. Report gross performance separately from a feasible cost model and retain sensitivity to fee spikes, recalls, collateral, turnover, and capacity.

The manuscript leaves unresolved several inputs needed for an exact independent reproduction: pre-sample lending history and the initial annual windows; zero-variance treatment; transformations and tail formulas; estimation-window timing; bootstrap blocks and repetitions; precise option pricing conventions; duplicate stock-day weighting; and all security-identifier and missing-data rules. Its Internet Appendix reportedly verifies alternative risk measures, including historical fee variance, but those appendix tables were not accessible for this note. The article supports a strong research hypothesis about dynamic lending constraints; it does not supply a turnkey trading specification or a fully identified causal model. The essential takeaway is to model uncertain future borrowing conditions jointly with the expected duration and stock-price risk of a short position.
