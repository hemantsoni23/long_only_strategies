# Uncovering Hedge Fund Skill from the Portfolio Holdings They Hide

Vikas Agarwal, Wei Jiang, Yuehua Tang, and Baozhong Yang. *The Journal of Finance* 68(2), 2013, 739–783. DOI: 10.1111/jofi.12012. Source: [BestIdeas_AgarwalJiangTangYang_2013.pdf](../../Finance/BestIdeas_AgarwalJiangTangYang_2013.pdf). This note covers all 45 pages of the published article, including Appendices A and B. Journal page numbers equal PDF page numbers plus 738. The separately distributed Internet Appendix was also inspected in the [authors' Columbia-hosted manuscript](https://drupalgsb-dev.cc.columbia.edu/sites/default/files-efs/pubfiles/6037/Hedge_fund_skill.pdf), PDF pages 61–78; numerical main results below follow the supplied published article.

## Why this matters

Public institutional-holdings databases do not necessarily show everything an institution owned at a reported quarter-end. A manager can seek confidential treatment and disclose selected positions later through an amendment. Omitting those delayed positions can omit the very investments about which a manager has the most valuable information. This paper reconstructs that missing portion directly from SEC filings and asks which hedge funds hide positions, which stocks they hide, how their holdings evolve, and how the hidden stocks subsequently perform.

The distinctive contribution is therefore both a data reconstruction and an economic test. Confidential positions are not inferred from a statistical residual or a survey response: they are identified in amendments that reveal previously withheld quarter-end holdings. Their subsequent returns can be evaluated from the original economic holdings date, before outsiders could observe them. This creates a test of the manager's information, not an immediately available public trading signal.

The evidence is consistent with confidential treatment protecting long-lived information and the associated cost of revealing a trading program. Hidden positions take longer to build, frequently involve takeover targets, and outperform ordinary disclosed holdings under several return benchmarks. The paper cannot completely separate informed trading from price-impact protection, nor does it identify the causal return a manager gains solely because confidentiality was granted. These distinctions are essential when translating the results into portfolio research.

## Institutional setting and data reconstruction

During the study's historical period, the Form 13F regime covered qualifying institutional managers with at least \$100 million in specified securities. Ordinary holdings were due within 45 days after quarter-end. Confidential treatment could delay disclosure, commonly for up to a year, and amendments eventually exposed the withheld positions after expiration or denial. These are the rules described for the sample, not a statement of current legal requirements.

The authors collect original Form 13F-HR and amended Form 13F-HR/A filings from EDGAR for March 1999–June 2007. They distinguish an amendment adding previously confidential holdings from a restatement correcting a prior filing. The amendment's checkbox and filing content matter: treating all restatements as hidden positions would create false observations. A hidden holding can be an entirely omitted stock or an increment to a partially disclosed position. In the latter case, the confidential amount is the subsequently revealed additional holding rather than the original position counted again.

Automated collection and parsing are combined with manual handling; the automated procedure processes approximately 91% of filings. The initial collection contains 3,315 institutions, 53,296 original filings, and 1,857 confidential filings. Table I reports denials for about 15.1% of these confidential filings. The analysis excludes ordinary filings more than 180 days late and confidential disclosures no later than 45 days or more than 1,505 days after quarter-end. Its final classification tables contain 52,272 original filings from 3,134 institutions and 1,554 confidential filings from 232 institutions. A reproducer must reconcile the various collection and analysis counts rather than assume all reported tables use the initial universe.

The hedge-fund unit is a management company filing an institutional report, not an individual hedge fund with a separately observed NAV. The authors identify pure-play or predominantly hedge-fund managers, excluding broad conglomerates whose hedge-fund activity cannot be isolated from banks or mutual funds. Classification draws on fund directories, web material, news, Thomson categories, and manual verification. Appendix B explains why Thomson's broad “other” category cannot simply be equated with hedge funds and how historical institution-type errors are corrected. Some firms previously assigned a reliable pre-1997 type can be restored; unresolved cases receive manual attention.

The resulting hedge-fund group contains 942 institutions and 14,002 ordinary filings. Of these institutions, 106 make 870 confidential filings. Hedge funds therefore account for roughly 30% of institutions but 56% of confidential filings. Conditional on a hedge fund using confidentiality, the hidden positions average 33.8% of its total disclosed-plus-confidential portfolio value, with median 23.7%. Mean hidden stock count is 77.2 but median only seven, indicating substantial skewness. Mean hidden portfolio value is about \$743 million, versus median \$156.4 million.

The data gap in standard holdings products is large: more than 90% of confidential holdings are missing from Thomson in the authors' checks. Appendix A examines 55 confidential Stark positions; 53 are absent from Thomson and 39 concern takeover targets. This example illustrates why a manager can appear to have an unremarkable or incomplete public portfolio while its omitted positions are economically central.

A stricter Form ADV-based classification produces 781 hedge-fund institutions, requiring substantial pooled-investment or high-net-worth activity together with performance-based compensation. It excludes 161 institutions the authors regard as legitimate hedge-fund managers, so it is a sensitivity check rather than their preferred definition. A separate match to five voluntary hedge-fund databases identifies strategy information for 450 institutions. These matches support the economic characterization but do not turn the complete sample into a survivorship-free panel of individual fund NAVs.

## Economic mechanism and the appendix model

The main article's mechanism starts from the cost of revealing an informed trading strategy. If prices have not yet incorporated a manager's information after the normal reporting delay, revealing the position can accelerate price discovery, encourage copying, or worsen execution while the manager is still accumulating. A manager liquidating a position for liquidity reasons can also benefit from privacy without possessing favorable information about the stock's future return. Consequently, confidentiality alone does not imply positive expected alpha; acquisitions and dispositions require separate examination.

The Internet Appendix formalizes this with one risk-neutral informed trader, independent Gaussian noise trades, a Gaussian terminal value, and a competitive market maker observing aggregate order flow. Confidentiality lasts until period $n_d-1$ in an $N$-period market. Before disclosure, optimal trades are linear in private value minus public price; under disclosure, the trader adds independent noise to conceal information, except in the terminal period. Backward induction joins a no-disclosure phase to the disclosure equilibrium. Expected profit is $\Pi_{n_d}=\sigma_u^2\sum_n\lambda_n$, where $\lambda_n$ is price impact. Apply when $\Pi_{n_d}-\Pi_1>c/Pr$, with exogenous application cost $c$ and approval probability $Pr$. The gain scales with prior information uncertainty. The model reveals trades, not incomplete quarterly positions, and omits competing front-runners. See appendix equations (1)–(14) and proof for the complete recursion. This provides comparative statics, not an empirically calibrated trading strategy. [Author-hosted Internet Appendix](https://drupalgsb-dev.cc.columbia.edu/sites/default/files-efs/pubfiles/6037/Hedge_fund_skill.pdf).

The empirical implications are more specific than “private positions do well.” More information-intensive institutions should seek confidentiality more often; information-sensitive stocks should be more likely to be withheld; hidden acquisitions should be built over longer intervals; and prematurely revealing still-informative positions should move prices. Each prediction is examined with a different unit of observation and a different source of selection.

## Institution-level models

Equations (1)–(4), journal pages 756–757, relate confidentiality to institution-quarter characteristics. Let $D_{jq}$ indicate whether institution $j$ has any confidential holding in quarter $q$. Let $CF_{jq}$ be confidential value divided by the total value of ordinary and confidential holdings. The probit and left-censored Tobit specifications are

$$
\Pr(D_{jq}=1\mid X_{jq})=\Phi(X_{jq}'\beta+\lambda_q),
$$

$$
CF^*_{jq}=X_{jq}'\gamma+\lambda_q+\omega_{jq},\qquad
CF_{jq}=\max(CF^*_{jq},0).
$$

Quarter dummies absorb common time effects. Standard errors are heteroskedasticity-adjusted and clustered by filing institution. The Tobit is left-censored at zero; the equation does not impose an upper censoring point at one, despite the observed outcome being a fraction. It is not a fractional logit.

Reported average partial effects help interpret coefficients. For a continuous probit regressor, the APE is $\beta_k\overline{\phi(X'\beta+\lambda)}$. For the Tobit observed outcome, it is $\gamma_k\overline{\Phi((X'\gamma+\lambda)/\sigma_\omega)}$, not the coefficient on the latent outcome alone. These effects are evaluated over the sample covariate distribution rather than at an arbitrarily selected representative institution.

Covariates include log age since first appearance in Thomson, log stock-portfolio value, turnover, portfolio concentration, return, absolute flow, and risk. Turnover is the smaller of purchases and sales divided by average portfolio value across adjacent quarter-ends; holdings changes are valued using quarter-average prices. Concentration is the Herfindahl sum of squared portfolio weights. Monthly holdings-imputed returns assume stocks are held from the previous quarter-end. Portfolio volatility uses twelve months; idiosyncratic volatility uses residuals from a four-factor regression over 36 months, as specified in the table and variable definition.

Absolute flow is the portfolio-value change net of return appreciation, divided by previous value. Reproduction requires care here: the text defines its portfolio-return variable as an average monthly return during the quarter, whereas the value-change calculation spans quarter-ends. A consistent implementation should use the compounded quarterly holding return for that adjustment, explicitly identifying this as a clarification rather than assuming the printed monthly definition can be inserted unchanged. The resulting flow proxy is also a change in the reported stock portfolio, not necessarily actual investor subscriptions and redemptions to all strategies of the management company.

Table II uses 12,845 institution-quarter observations. The unconditional probability of confidentiality is 3.39%; the mean confidential-value share is 1.21%. Bigger portfolios, higher turnover, greater concentration, larger absolute flows, and greater idiosyncratic risk predict confidentiality. Moving from the first to the third quartile of the characteristic distribution raises the predicted probability by approximately 2.7 percentage points for portfolio size, 3.2 points for turnover, 0.9 point for concentration, 0.7 point for idiosyncratic volatility, and 0.3 point for absolute flow. These are large relative to a 3.4% baseline, but they are conditional associations using contemporaneous institution characteristics, not a demonstrated prospective forecasting strategy.

## Stock-level selection into secrecy

Equation (5) estimates a logit for whether a held stock is confidential at the institution-stock-quarter level. The main variants contain quarter and Fama–French ten-industry dummies, with standard errors clustered at the institution. The sample approaches 1.75 million holdings observations; about 2.2% are confidential. Multiple positions in the same stock held by different institutions remain distinct observations.

Stock size is quarter-end capitalization. Book-to-market comes from the previous fiscal year-end. Past return is prior twelve-month return adjusted for the CRSP value-weighted market. Analyst coverage counts analysts producing forecasts or recommendations. The liquidity measure averages the square root of absolute daily return divided by dollar volume, following the paper's Hasbrouck-style variant; it is not simply the unsquared standard Amihud ratio. Stock volatility and four-factor idiosyncratic volatility use 36 monthly returns. Financial distress is indicated by distance to default below 1.64, with construction delegated to the cited structural-default method.

The takeover indicator identifies an announced target in the preceding four quarters whose transaction is not yet complete. SDC supplies 4,726 control-seeking deals announced during 1998–2007, of which approximately 86% complete. The use of announced, incomplete transactions distinguishes merger-arbitrage opportunities from a hindsight list of all firms eventually acquired. The authors also examine future targets and do not find that unannounced future target status drives the result.

Descriptively, confidential stocks have mean capitalization of about \$7.781 billion, versus \$16.883 billion for ordinary positions; medians are \$1.375 billion and \$2.477 billion. Mean analyst coverage is 14.31 versus 16.26. Distressed stocks comprise 21.4% versus 14.5%; announced takeover targets 7.5% versus 4.1%. Annualized stock volatility is 0.515 versus 0.442, and idiosyncratic volatility 0.451 versus 0.388.

These averages should not be indiscriminately described as significant. The past-return difference, 17.6% versus 12.9%, has $t=1.63$; the illiquidity difference, 0.094 versus 0.089, has $t=0.85$. In the multivariable logit, the illiquidity coefficient is negative, around −2.044 with $t=-26.94$, while the takeover coefficient is approximately 0.945 with $t=22.64$. The reported takeover APE is about 1.96 percentage points. Smaller capitalization and lower analyst coverage remain associated with secrecy, but individual proxies do not all support an undifferentiated “more illiquid stocks are hidden” story. Distress is not uniformly significant after conditioning on the other characteristics.

## Are confidential positions still being built?

Table IV follows split-adjusted quarter-end share counts during the confidentiality interval and compares hidden positions with the same funds' contemporaneous ordinary positions. The sample includes 37,204 confidential stock positions and approximately 97,723 ordinary positions. Initial position size relative to shares outstanding is similar, 0.30% versus 0.28%, with an insignificant difference. The substantial distinction is subsequent trading.

Total absolute quarter-to-quarter share changes average 0.96% of shares outstanding for hidden positions, versus 0.34% for ordinary positions; the difference has $t=3.77$. Maximum position minus initial position averages 0.25% versus 0.09% of shares outstanding, $t=3.03$. Time from initial position to maximum averages 2.58 quarters versus 0.93, with a reported difference of 1.66 quarters and $t=2.95$.

When scaled by the initial position, total trading is 14.77 times initial size for confidential positions and 5.55 for ordinary ones. The table reports *maximum minus initial* as 6.55 versus 3.03 times initial size. The prose's description of 6.55 as maximum position itself is imprecise: the corresponding maximum-to-initial ratio would be 7.55 if calculated from the same observations. This distinction prevents a one-unit normalization error in replication.

These statistics observe quarter-end changes, not every execution. Trades that reverse within a quarter are invisible, and a large total-change ratio can reflect a small initial denominator. Nevertheless, the longer accumulation horizon supports the slow-building mechanism. Of the confidential positions, 27,306, or 73.4%, are disclosed after liquidation. Among the remaining 9,898, about 79.3% show no additional acquisition in the next quarter. Thus disclosure tends to follow completion of the relevant trading program, consistent with privacy being valuable while the trade remains active.

## Measuring hidden-position performance

The return tests start from the original economic quarter-end rather than the later public disclosure date. They value-weight stocks inside the reported holdings portfolio and evaluate subsequent stock returns. Carhart alpha is estimated using daily stock-portfolio returns and market, size, value, and momentum factors. This is an equity-holdings evaluation, not a regression of whole hedge-fund NAV on a hedge-fund factor model.

The second benchmark assigns stocks to DGTW characteristic portfolios. Stocks are sorted into $5\times5\times5$ portfolios using size, book-to-market, and momentum; June assignments and the matched characteristic portfolio are used through the relevant evaluation period. Subtract benchmark returns at the stock level and aggregate using holding values. Factor alpha and characteristic-adjusted return are different estimands and have different units in the tables.

Confidential filings are grouped by disclosure delay and evaluated at horizons of 2, 3, 4, 5, 6, 9, and 12 months. The shorter bins correspond to filings still confidential through the designated horizon and disclosed before the next threshold. Portfolio-level results are aggregated within institutions. A crucial ambiguity remains: the text and Table V caption describe ordinary holdings paired by institution and period, yet the original-filing counts in each horizon are close to all 14,000 ordinary hedge-fund filings, compared with only 24–309 confidential filings in the alpha rows. The PDF does not fully reconcile these denominators. A reproduction should inspect both the conditional matched benchmark and the reported broad original-holdings aggregate.

Table V reports the following confidential-minus-ordinary differences:

| Horizon | Daily four-factor alpha, basis points | $t$ | DGTW horizon return | $t$ |
|---|---:|---:|---:|---:|
| 2 months | 2.57 | 3.02 | 5.26% | 6.78 |
| 3 months | 2.31 | 2.22 | 1.71% | 2.39 |
| 4 months | 1.59 | 2.05 | 0.74% | 0.93 |
| 5 months | 1.21 | 1.04 | 3.67% | 2.58 |
| 6 months | 1.88 | 2.68 | 2.47% | 2.46 |
| 9 months | 1.31 | 1.72 | 4.57% | 2.83 |
| 12 months | 2.05 | 3.11 | 7.51% | 4.27 |

Multiplying daily alpha by 252 gives arithmetic annualized differences ranging from 3.04% to 6.48%, with 5.17% at twelve months. The 5.26% two-month DGTW result is the return over that two-month horizon, not an annual figure; its reported simple annualization is 31.56%. Conversely, the twelve-month DGTW value is already annual. Mixing these units would exaggerate or understate the comparison.

Confidential cohorts differ across horizons. These rows are not seven observations of the same fixed portfolio followed through time, so the changing estimates do not alone trace a single alpha-decay function. Statistical significance is also not uniform: the five-month daily-alpha difference is insignificant, and the four-month DGTW difference is insignificant.

Panel B supplies a common three-month comparison across 870 confidential and 14,002 ordinary filings, with returns annualized and then averaged over institution-quarter portfolios. Value-weighted raw returns are 19.97% versus 13.00%, a 6.98-point difference with $t=2.65$. DGTW returns are 6.37% versus 1.39%, a 4.99-point difference with $t=2.63$. Equal-weighted DGTW returns are 5.52% versus 2.02%, a 3.50-point difference with $t=1.82$. This makes clear that the magnitude and precision vary with the stock and institution aggregation method.

## Acquisition, disposition, and robustness

The authors classify a position as acquisition-motivated when its split-adjusted shares increase from the previous quarter and disposition-motivated when they fall. Unchanged positions, 5.4% of observations, use the following quarter's change as a tie-break. Overall 80.7% are acquisitions and 19.3% dispositions. The future-quarter tie-break is acceptable for an explanatory classification but is look-ahead information for any proposed real-time trading signal.

Acquisitions drive the consistent return evidence. At twelve months, their confidential-minus-ordinary alpha is 1.54 basis points daily, or 3.88% annualized, with $t=2.25$; their DGTW difference is 7.06%, $t=3.95$. Dispositions have a twelve-month annualized alpha difference of 1.29%, $t=0.57$, and DGTW difference of 2.94%, $t=1.42$. At nine months, disposition differences are negative: −7.27% annualized alpha and −6.00% annualized DGTW. Concealing a sale can protect execution even when the concealed stock is not an attractive long investment.

The published article reports sensitivity to an alternative hedge-fund list, forward-looking trade classification, exclusion of stocks accompanied by reported call or put positions, different institution types, and removal of unusually frequent confidential filers Caxton and D. E. Shaw. Those checks generally preserve the main acquisition and hedge-fund conclusions. The options check addresses an obvious concern but cannot observe all short positions, swaps, or other offsetting exposures.

An appendix unit check resolves a published-text problem: the option-exclusion alpha differences described as 2.48% and 1.64% are **daily basis points**, not percentages; their annualized equivalents are 6.24% and 4.13%. [Internet Appendix, Table IA.III](https://drupalgsb-dev.cc.columbia.edu/sites/default/files-efs/pubfiles/6037/Hedge_fund_skill.pdf).

The authors characterize quarter-end holdings returns as potentially conservative if unobserved interim trades add value. That is conditional, not an automatic lower-bound theorem: unsuccessful interim trades, offsetting derivative losses, or different actual execution prices could change the sign. Starting return measurement at the beginning of the holding quarter strengthens results but introduces look-back bias, since the final portfolio was not necessarily held then. The main quarter-end convention avoids that particular error.

## Denial and the price response to forced disclosure

Section V first estimates a probit for denial among institutions that requested confidentiality. Depending on controls, the regression has 713 or 629 filings and unconditional denial probability near 22% or 19.4%. Filing characteristics include the number of previous requests, prior denial frequency, confidential stock count as a share of total holdings, confidential value, its fraction of total portfolio value, and average ownership of confidential stocks. Because confidential value and its fraction are highly collinear with scale, not all are included simultaneously.

Past denial frequency is a strong predictor. Moving from no previous denials to a 50% historical denial frequency increases the predicted denial probability by approximately 27 percentage points. Prior denials are also associated with faster review, roughly ten fewer days per prior denial in the stated duration analysis. This gives confidentiality a dynamic reputational cost, although the model does not establish which missing legal facts cause each rejection. Larger funds are not uniformly more likely to be denied, and different measures of confidential exposure have different signs after controls.

The event study focuses on relatively quick denials: disclosure occurs 45–180 days after the original quarter-end. It compares 66 denied confidential filings with 197 nondenied filings disclosed within similar delay bounds. These are broadly comparable timing groups, not randomly assigned paired events. The event date is the amendment's public filing date, not the private date of the SEC's decision.

For each stock, estimate a market model using the equally weighted CRSP index and daily returns from event days −300 through −91. Apply Scholes–Williams beta adjustment for nonsynchronous trading. Aggregate stock abnormal returns equally within each filing and then average across filing events. Test mean cumulative abnormal returns with the two-sided Patell statistic and the fraction of positive filing returns with a generalized sign test.

Quickly denied filings have mean CARs of 0.54% over $[-1,+1]$, 0.97% over $[-2,+2]$, and 1.19% over $[-5,+5]$, with Patell statistics 2.42, 2.61, and 2.18. Positive-event fractions are 63.6%, 63.6%, and 62.1%. Nondenied filings have CARs 0.39%, 0.30%, and 0.52%, none individually significant in the reported tests.

These findings support information remaining in the holdings at premature disclosure. But “significant in one group and insignificant in another” is not itself a statistically significant group difference. The table does not report a formal difference-in-CAR test, and denial is related to past institutional behavior and filing characteristics. Forced disclosure therefore supplies suggestive event evidence, not a clean randomized instrument for confidentiality's causal benefit.

## Reproduction boundaries and practical implications

The central data product should retain both economic and public-information clocks: institution, original quarter-end, original filing date, confidential amendment date, denied status, split-adjusted stock identity, originally disclosed shares, and subsequently revealed additional shares. Build the complete portfolio before computing confidential-value shares or turnover. Keep classification provenance for every institution and a clear distinction between added confidential holdings and corrections. Aggregate stock positions to the institutional manager only after eliminating duplicate report records.

The study cannot be fully regenerated from a commercial holdings download alone. It needs historical filing text, amended position reconciliation, manual institution classifications, acquisition histories, and the paper's matched-sample conventions. Precise handling of all identifier changes, failed parses, multiple amendments, missing returns, and default-distance estimation is not contained in executable form in the PDF. In particular, the unexplained performance-table denominators should remain a documented uncertainty until author data or code resolve them.

The investment implication is about measuring skill and understanding the information set. A manager's visible 13F portfolio may understate both its research-intensive exposures and its concentration. The hidden portfolio's retrospective alpha is evidence that the omitted information matters, but it cannot be bought at the old quarter-end once the amendment finally appears. A prospective strategy would need a separate announcement-date test, actual release timing, post-disclosure holding rules, and costs. For manager evaluation, complete amended holdings are valuable; for copying, their delayed arrival is the central constraint.
