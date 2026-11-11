# Hedge Funds: Pricing Controls and the Smoothing of Self-Reported Returns

Gavin Cassar and Joseph Gerakos. October 2009 working paper, Wharton Financial Institutions Center 09-43 and Chicago Booth IGM Working Paper 45. Source: [HedgeFunds_CassarGerakos2009.pdf](../../Finance/HedgeFunds_CassarGerakos2009.pdf). The local PDF has 59 pages, including two institutional covers, references, two appendices, one six-panel figure, and nine tables. Printed page 1 corresponds to PDF page 4. Numerical findings below follow the displayed tables where this draft's narrative disagrees with them.

## Why this matters and what is new

A smooth hedge-fund return series can reflect slow-moving economic prices, stale marks, deliberate reporting choices, or a combination. Serial correlation alone cannot identify which explanation applies. That distinction matters for investors estimating volatility, allocating capital, or interpreting a manager's apparently stable Sharpe ratio. It also matters for researchers: removing serial correlation mechanically is not the same as identifying false accounting.

The paper contributes unusually direct information about the valuation process. Rather than inferring discretion from domicile or strategy alone, the authors observe who supplies prices for portfolio holdings, who prices those holdings, who calculates and reports net asset value, and whether auditors and administrators have recognized industry reputations. They connect these controls to three return-smoothing statistics and to the distribution of reported returns near zero. The central empirical finding is that the source and initial determination of individual-position prices are more informative about smoothing than the later aggregation and reporting of NAV.

The design is observational. It establishes conditional associations in a selected sample of funds that underwent due diligence. It does not randomly assign pricing controls, observe the true executable value of every holding, or demonstrate intentional misreporting fund by fund. The authors' preferred interpretation is that less verifiable inputs facilitate discretion, alongside a larger role for underlying asset illiquidity. The statistical evidence supports that interpretation but does not uniquely identify it.

## Sample construction and the information actually observed

The starting material is 427 proprietary hedge-fund due-diligence reports prepared by HedgeFundDueDiligence.com, or HFDD, during 2003–2007. Investors commissioned these investigations. The investigations included interviews and visits, discussions with service providers, and examination of organizational and offering documents, audited statements, and public records. They are richer than self-declared database fields, but their availability is conditional on investor interest and the commissioning process. This is not a random census of hedge funds.

The authors match the reports to returns in Lipper-TASS, Hedge Fund Research, and CISDM. When a fund appears in multiple databases, returns are taken first from TASS, next HFR, and finally CISDM; overlapping series are not treated as different funds. They require at least 12 monthly returns and convergence of the smoothing estimation. Ten funds with sufficient histories fail the convergence condition. The final sample contains 260 funds: 158 from TASS, 72 from HFR, and 30 from CISDM. Return observations span July 1990–January 2009, substantially wider than the report dates (Section 2, PDF pp. 16–20).

The distinction between the report date and the return-history window is essential. Main specifications use the available fund history and assume that investment style and pricing controls remain constant over it. They are not a prospective test that uses only controls known before the first return observation. The authors argue that strategy changes often lead to a new fund and pricing procedures are embedded in offering documents, but they do not supply a time series of changes in each fund's controls. A later before/after exercise tests part of this assumption.

A replication must resolve inconsistent descriptive text. Section 2.1 says the mean fund has 66 months of returns, whereas Table 3 reports a mean of 79.996, median 72, standard deviation 36.868, and quartiles 56 and 97.5 months. The note uses Table 3 for the numerical distribution without silently harmonizing the two statements. Raising the minimum history to 18 months leaves 259 funds, and raising it to 24 leaves 256; the authors report quantitatively similar results.

Ten harmonized styles are used: convertible arbitrage, emerging markets, equity market neutral, event driven, fixed-income arbitrage, global macro, long/short equity, multi-strategy, funds of funds, and miscellaneous. Appendix A gives the database-specific mapping. Important non-obvious mappings include CISDM capital-structure, merger, option-arbitrage, and event-driven multi-strategy categories into event driven; CISDM relative-value multi-strategy into multi-strategy; and CISDM's separate “Multi Strategy” category into funds of funds. The last decision is justified from overlapping funds' TASS/HFR classifications. Miscellaneous combines dedicated short bias, commodity-pool operators, managed futures, long-only equity, Regulation D, sector, single-strategy, and systematic labels. Replacing this mapping with modern vendor categories would change the controls.

The portfolio variables are categorical typical numbers of holdings—1–39, 40–99, 100–199, 200–999, and at least 1,000—and typical holding durations of days, weeks, months, quarters, or years. They describe ordinary investment positions, not investor redemption terms. Table 1 reports 42% with fewer than 40 positions, 35% with holding periods classified as years, and 83% domiciled offshore. Long/short equity is the largest style at 29%; event driven accounts for 15%. A later narrative calls event driven the largest style, but its 38 funds make it the largest style selected for that particular within-style exercise, not the largest category overall.

## Separating four layers of valuation control

The source-of-prices classification is based on the least objective source available to the fund in the main analysis. This captures the margin on which discretion can operate even if most assets have transparent prices. Table descriptions occasionally call it the primary source, so exact coding requires the HFDD records; the main text's least-objective rule is the clearest stated construction.

The five categories are exchange quotes, OTC quotes, dealer quotes, model-based prices, and manager-provided prices. Exchange prices are the omitted, most objective comparison category. Dealer quotes can be externally generated yet discretionary in their selection: a manager may seek a favorable quote among counterparties. Model prices require judgments about inputs and assumptions. Manager-provided values offer the most direct scope for discretionary marking. These are categories, not a numerical rank imposed in the regressions.

Table 1 gives shares of 32% exchange, 5% OTC, 36% dealer, 11% model based, and 16% manager provided. Several nearby prose percentages differ by about one point. The table is therefore the reference for these figures. Conditional frequencies reveal why strategy controls are necessary: 92% of convertible-arbitrage funds use dealer quotes, while 88% of equity-market-neutral funds use exchange quotes (Table 2).

A separate classification records who actually prices positions. “Manager only” means no external oversight. “Collaborative” means manager and an outside administrator work together. “Administrator only” means outside services perform the pricing. “Dual/triple entity” means at least one internal and one external source price the positions separately; HFDD views this as the most stringent arrangement, and it is the omitted category. Table 1 shares are approximately 20%, 12%, 60%, and 9%, with rounding.

The NAV-manager indicator asks whether the manager participates in setting and reporting aggregate NAV to investors. It is distinct from the source of the individual marks entering that calculation. An administrator can accurately sum values that already contain discretion. Finally, two indicators identify auditors and administrators absent from Institutional Investor's Alpha survey rankings of hedge-fund service providers. All sample funds are audited; the comparison is reputation among providers, not audit versus no audit. Table 1 reports 14% with manager involvement in NAV, 23% with an unranked auditor, and 68% with an unranked administrator. The narrative contains slightly different NAV and auditor percentages.

## The smoothing model and its assumptions

The first dependent variable is the estimated first-order monthly autocorrelation, $\widehat\rho_{i,1}$, of each fund's reported returns. The other two come from the Getmansky–Lo–Makarov moving-average representation. Suppress the fund subscript and write latent economic returns as $R_t=\mu+\eta_t$. Reported returns are

$$
R_t^O=\sum_{j=0}^{k}\theta_j R_{t-j},\qquad \sum_{j=0}^{k}\theta_j=1.
$$

The empirical model sets $k=2$, assumes independent Gaussian innovations $\eta_t\sim N(0,\sigma_\eta^2)$, and estimates the demeaned process by maximum likelihood:

$$
X_t=R_t^O-\mu=\theta_0\eta_t+\theta_1\eta_{t-1}+\theta_2\eta_{t-2}.
$$

For implementation it is useful to distinguish ordinary MA coefficients from normalized economic weights. If software estimates $X_t=\epsilon_t+a_1\epsilon_{t-1}+a_2\epsilon_{t-2}$, the normalization described in the paper is

$$
(\theta_0,\theta_1,\theta_2)=\frac{(1,a_1,a_2)}{1+a_1+a_2}.
$$

This resolves the text's reuse of the symbol theta for pre- and post-normalization estimates. Software sign conventions must match the plus signs above. The local paper does not identify the optimizer, starting values, exact versus conditional likelihood, treatment of gaps, or invertibility restrictions. Those choices are necessary for exact numerical replication and particularly relevant to the ten convergence failures. A denominator close to zero makes the transformation unstable.

The current-return weight $\widehat\theta_0$ measures the proportion of a current economic innovation recognized immediately. It is not the fraction of each realized reported return that can literally be assigned to the current month: lagged shocks may offset it. The third statistic is

$$
\widehat\xi=\widehat\theta_0^2+\widehat\theta_1^2+\widehat\theta_2^2.
$$

Lower theta-zero and lower concentration $\xi$ generally indicate more spreading of economic shocks over reporting dates. Under independent latent innovations,

$$
\operatorname{Var}(R_t^O)=\sigma_\eta^2\xi,\qquad
\rho_m=\frac{\sum_{j=0}^{2-m}\theta_j\theta_{j+m}}{\xi},\quad m=1,2.
$$

Autocorrelations beyond lag two are zero in this model. Mean preservation follows from the weights summing to one. Variance reduction additionally requires appropriate smoothing weights: for nonnegative weights summing to one, $1/3\leq\xi\leq1$. Merely requiring the sum to equal one does not imply $\xi\leq1$. The source does not state an empirical nonnegativity constraint in this paper, so out-of-range estimates should be reported rather than forced into an accounting interpretation.

For positive mean excess return and consistently defined returns, the population Sharpe ratio becomes $SR^O=SR/\sqrt\xi$. The paper's displayed formula uses mean return without an explicit risk-free subtraction. It is best interpreted as the same risk-adjusted ratio under a common zero or already-subtracted benchmark. The inequality that smoothing increases the signed Sharpe ratio also assumes a nonnegative numerator; for negative mean returns reduced volatility makes the ratio more negative. These qualifications are mathematical conditions, not additional empirical findings.

Appendix B supplies a simulation illustration rather than a fitted fund model. Generate 100 independent monthly Gaussian returns with mean 1% and standard deviation 2.5%, then smooth with weights $(0.7,0.2,0.1)$. Here $\xi=0.54$, implying population standard-deviation scaling $\sqrt{0.54}\approx0.735$ and Sharpe scaling about 1.361. The particular sample changes standard deviation from 2.234% to 1.634%, the reported ratio from 0.387 to 0.526, and lag-one correlation from −0.049 to 0.262. Means are 0.864% and 0.866%; finite-sample endpoints explain why estimated means need not be identical. The source does not supply its seed or initialization, so one should reproduce the distributional mechanism rather than promise those exact simulated realizations.

## Estimation pipeline and baseline statistics

Estimate all three measures separately for each eligible fund, winsorize their cross-sectional tails, then use them as outcomes in fund-level regressions. An unresolved source discrepancy is that Section 2.5 states the 0.5th and 99.5th percentiles, while Table 3 states the 1st and 99th. A defensible replication should run both and label them explicitly, rather than asserting which generated the tables without code.

Table 3 reports mean lag-one correlation 0.247 with standard deviation 0.196; mean theta-zero 0.767 with standard deviation 0.194; and mean concentration 0.694 with standard deviation 0.301. The main text instead gives correlation mean 0.250 and standard deviation 0.300. Median values in the table are 0.223, 0.739, and 0.595. The Pearson correlations across funds are −0.838 between serial correlation and theta-zero, −0.757 between serial correlation and concentration, and 0.960 between the two MA measures. Thus the outcomes provide different summaries of largely related information, not three independent replications of the hypothesis.

For outcome $Y_i$ in this set, reconstruct the cross-sectional specification as

$$
Y_i=\alpha+S_i'\beta+P_i'\gamma+H_i'\delta+\lambda O_i+C_i'\pi+u_i.
$$

Here $S_i$ contains style indicators; $P_i$ position-count indicators; $H_i$ holding-duration indicators; $O_i$ the offshore indicator; and $C_i$ the pricing-control indicators. The omitted baseline categories are miscellaneous style, 1–39 positions, days, exchange quotes, and dual/triple pricing. An intercept is included. Table 5 excludes $C_i$. Table 6 adds price sources, position pricers, NAV involvement, auditor ranking, and administrator ranking individually in columns 1–5, then jointly in column 6. Each specification has 260 funds. Tables report OLS standard errors and conventional significance levels but do not specify a robust or clustered covariance estimator.

This two-stage procedure treats estimated smoothing measures as observed dependent variables. Footnote 10 argues against the need for joint GMM, citing 72 months and an autocorrelation standard error of 0.014. That number resembles $1/72$, whereas the basic white-noise autocorrelation standard error is approximately $1/\sqrt{72}=0.118$. Serial dependence complicates the correct variance further. Consequently, the footnote does not justify dismissing first-stage uncertainty. A fund-history bootstrap with appropriate temporal dependence would be a useful extension, but is not part of the reported results.

## What the estimates show

The unconditional comparisons in Table 4 are economically substantial. Manager-provided pricing has mean $(\rho_1,\theta_0,\xi)=(0.326,0.682,0.569)$, compared with exchange pricing $(0.139,0.867,0.836)$. Dealer quotes yield $(0.311,0.706,0.613)$ and model-based prices $(0.268,0.747,0.661)$. OTC quotes produce $(0.174,0.876,0.846)$. Exchange and OTC thus need not rank identically across all measures; the prose's claimed single ordering overstates the table.

Manager-only position pricing has theta-zero 0.732 and concentration 0.632, versus 0.843 and 0.825 for dual/triple pricing. The minus signs attached to these concentration values in the narrative are typographical errors: a sum of squared real weights cannot be negative, and Table 4 prints positive values. Its significance markers for several position-pricer comparisons are at 10%, weaker than some narrative claims of 5%. NAV involvement and ranked-provider comparisons do not display significant differences in the table.

The joint Table 6 estimates provide the most useful effect sizes:

| Pricing category, relative to omitted category | Serial correlation coefficient (SE) | Theta-zero coefficient (SE) | Concentration coefficient (SE) |
|---|---:|---:|---:|
| Manager-provided versus exchange | 0.141 (0.049) | −0.195 (0.049) | −0.307 (0.078) |
| Model-based versus exchange | 0.082 (0.046) | −0.110 (0.046) | −0.165 (0.073) |
| Dealer versus exchange | 0.081 (0.037) | −0.125 (0.037) | −0.196 (0.059) |
| OTC versus exchange | 0.073 (0.059) | −0.031 (0.059) | −0.059 (0.094) |
| Manager-only versus dual/triple | 0.036 (0.051) | −0.087 (0.051) | −0.161 (0.081) |

Manager-provided coefficients are significant at 1% for all three outcomes. Dealer effects reach 5% for serial correlation and 1% for the other two. Model effects are weaker for serial correlation, significant at 10%, and significant at 5% for theta and concentration. OTC effects are not statistically significant in these joint specifications, contrary to the narrative's broad claim that every alternative source significantly exceeds exchange-based smoothing.

The theta-zero estimate of −0.195 is a 19.5-percentage-point difference in the estimated immediate-recognition weight, conditional on included characteristics. It is not a 19.5% reduction in the fund's actual return, nor a fraud probability. The prose cites 17.9 points, which does not match the displayed full specification. Manager-only position pricing is associated with additional smoothing in the theta and concentration regressions, but not significantly in the serial-correlation regression. Collaborative and administrator-only coefficients are not individually significant once price sources and the other controls enter jointly.

The coefficients on manager involvement in NAV, unranked auditors, and unranked administrators remain insignificant. The point estimates are small and mixed in direction. This is evidence that these particular indicators do not add much explanation of monthly smoothing in this sample. It does not show that audits never improve annual accounts, independent administrators never detect fraud, or provider quality has no value.

Table 5 baseline $R^2$ values are 0.243, 0.177, and 0.140 for correlation, theta-zero, and concentration. The full Table 6 models give 0.284, 0.258, and 0.228, respectively. The incremental explanatory shares are therefore **4.1, 8.1, and 8.8 percentage points**. These reproduce the abstract's overall range; some main-text values, including a 7.3-point concentration increment, do not match the tables. Full-model adjusted $R^2$ values are 0.198, 0.169, and 0.135, reflecting the cost of numerous regressors in a modest cross section.

These increments are not a decomposition assigning 8.8% of all smoothing to fraud and the remainder to illiquidity. The controls overlap, omitted liquidity characteristics may correlate with pricing choices, and unexplained variation remains large. They quantify added linear explanatory power, not causally identified variance components.

## Robustness and the separate near-zero distribution test

The authors report within-position-count and within-holding-duration comparisons. Manager involvement and dealer sources continue to be associated with smoothing at the 10% level for the reported relevant categories, although detailed estimates are not supplied. Within event-driven funds, Table 7 shows manager-provided theta-zero 0.615 versus model-based 0.932 and exchange-based 0.837. There are only 38 funds, no OTC group, and small cells. This mitigates broad style confounding without holding security-level liquidity fixed.

To address a skill interpretation, the paper estimates each fund's lifetime alpha using eight Fung–Hsieh factors: S&P 500 returns, small-minus-large equity returns, bond-, currency-, commodity-, and stock-index trend-following factors, a bond-market factor, and a credit-spread factor. Table 8 shows monthly alpha 0.00545 for manager-provided prices versus 0.00833 for exchange prices; manager-only and dual/triple values are 0.00916 and 0.00809. The patterns do not support a simple story in which more skill leads investors to permit more opacity. They do not conclusively rule out skill confounding, since alpha is itself estimated from the reported return series and depends on the risk model.

Adding domicile indicators for countries with at least ten funds reportedly leaves the main results materially unchanged. Replacing the least-objective-source category with indicators for every source the fund uses also produces similar unreported results. Neither exercise supplies new causal variation.

Table 9 recomputes smoothing before and after the due-diligence report, requiring at least twelve observations in the relevant segment. Samples are 161 before and 222 after. Before the report, position-pricer coefficients are insignificant. Afterward, manager-provided source coefficients are 0.187 for correlation, −0.280 for theta-zero, and −0.481 for concentration, all significant at 1%. Manager-only position pricing has −0.117 on theta-zero at 10% and −0.248 on concentration at 5%. This is not a treatment-effect estimate of due diligence: sample composition and histories differ, and the paper does not estimate a controlled pre/post intervention. One printed Table 9 entry, administrator-only concentration after the report, is positive 0.165; it should not be silently turned negative to fit the overall narrative.

Section 5 pools monthly reported returns and asks whether small gains are unusually frequent and small losses unusually scarce. The displayed bin-width rule is

$$
h=1.364\,a\,\min\{s,Q/1.340\}\,N^{-1/5},\qquad a=0.776,
$$

where $s$ is sample standard deviation, $Q$ interquartile range, and $N$ the number of pooled return observations. A Gaussian kernel supplies expected bin counts, which are compared with actual counts using an asymptotic normal approximation attributed to the de Moivre–Laplace theorem. The normal reference sets the smoothing constant; it does not establish that hedge-fund returns themselves are Gaussian.

Figure 1 displays the entire sample and each price-source group. In the pooled sample both excess small positives and missing small negatives are significant at 5%. Dealer and manager-provided groups exhibit both features, generally at 1%, except excess small positives for the manager group at 10%. Exchange, OTC, and model groups show excess small positives at 5% but no statistically significant shortage of small negatives at 10%. The latter distinction is stronger evidence than claiming every group with positive-return clustering manipulates losses.

Exact replication still requires bin origin, kernel bandwidth implementation, expected-count construction, treatment of exactly zero returns, and any correction for estimated density or dependent fund-months. These are not fully specified. Under fixed independent-bin probabilities a standardized count would use $(n_b-Np_b)/\sqrt{Np_b(1-p_b)}$, but pooled hedge-fund observations share market shocks and within-fund dependence; that formula alone is not a complete valid inference procedure here. Histograms by typical holdings and durations reportedly show similar jumps, which weakens a simple liquidity explanation but cannot eliminate all economic alternatives.

## Reproduction boundaries and practical interpretation

The executable research design is: obtain the proprietary controls and matched histories; apply the stated vendor precedence and Appendix A map; retain qualifying convergent funds; estimate the MA model and autocorrelation; run both documented winsorization variants; reproduce Tables 3–6 using the exact omitted categories; then perform within-style, domicile, pre/post, source-recoding, and near-zero distribution checks. Preserve every convergence failure and missing-data decision in an audit trail. The paper supplies no trading strategy, portfolio rebalancing rule, transaction-cost model, or out-of-sample alpha target, so none should be invented.

The largest barriers to exact reproduction are unavailable HFDD records and matching identifiers, missing estimation settings, unclear timing of provider rankings, and the draft's internal discrepancies. Return-database selection and backfilled histories are also material: the paper does not describe an entry-date backfill purge comparable to a prospective investment backtest. The full-history constant-control assumption makes the estimates descriptive of funds and their recorded structures, rather than a clean forecasting exercise.

For an allocator, the supported lesson is to examine the chain by which individual marks enter NAV. A well-known administrator at the end of that chain cannot, by itself, make discretionary source values objective. For a quantitative researcher, the useful innovation is combining statistical smoothing diagnostics with directly observed valuation mechanisms. Neither a high autocorrelation nor an unranked provider proves misconduct; conversely, insignificant reputation coefficients do not validate reported prices. The strongest finding is the conditional association between less verifiable price inputs and delayed recognition of economic innovations, with independent distributional evidence around zero that is suggestive but inferentially less fully specified.
