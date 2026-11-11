# Economic Forces and the Stock Market

Nai-Fu Chen, Richard Roll, and Stephen A. Ross. *Journal of Business* 59(3), July 1986, 383–403. Source: [MacroAssetPricing_ChenRollRoss_1986.pdf](../../Finance/MacroAssetPricing_ChenRollRoss_1986.pdf), 22 PDF pages including the archive cover. The complete source was read using OCR from a repaired scratch copy; the original PDF was preserved. Equations, variable definitions, correlation tables, and all pricing-result tables were checked against rendered pages. References below use printed journal pages.

## Why this matters

The paper attempts to identify the economic content of systematic equity risk. A statistical factor can describe common movements without explaining why investors demand compensation for exposure to it. Chen, Roll, and Ross instead choose observable macroeconomic and nonequity-market variables using an economic argument, estimate stock portfolios' exposures, and ask whether those exposures explain differences in average returns.

Their strongest finding is a distinction between covariance explanation and expected-return explanation. Broad stock indices dominate time-series regressions of stock returns, yet their betas add little pricing information after the selected macroeconomic exposures are included. Industrial-production growth, a low-grade-bond return spread, and a long-bond excess-return measure are more useful in their cross-sectional pricing experiment. Inflation-related exposures matter especially in the inflationary middle subperiod. Consumption growth and oil-price growth do not supply a reliably priced additional exposure.

The innovation is the proposed identification and joint empirical testing of economic factors, not a fully specified general-equilibrium derivation of their prices. The authors do not derive all premium signs from primitives, claim causal exogeneity of macroeconomic series, or establish that the selected list exhausts systematic risk. The resulting model is a research specification for economic exposure measurement and cross-sectional pricing, not a real-time forecast of next month's equity return.

## Economic mechanism and its level of approximation

Section II starts from the shorthand valuation expression $p=E[c]/k$, with $c$ representing cash flows and $k$ a discount rate. Differentiating gives the heuristic return decomposition

$$
\frac{dp}{p}+\frac{c}{p}
 \approx\frac{dE[c]}{E[c]}-\frac{dk}{k}+\frac{c}{p}.
$$

The approximation symbol here makes explicit the paper's footnote: second-order stochastic-calculus terms are ignored. The expression is an intuition for choosing variables, not an exact stochastic return identity for arbitrary dividend dynamics. The expectation is associated with a pricing measure in the source's discussion, rather than automatically the physical probability measure.

Systematic news can affect expected real cash flows, nominal cash flows, discount rates, or the future investment opportunity set. Industrial production proxies changes in productive activity and real cash-flow prospects. Inflation can affect both nominal cash flows and nominal discount rates, as well as relative wealth and relative prices. Interest-rate and bond-return variables proxy changes in discounting and required risk compensation. Consumption supplies an alternative marginal-utility channel.

The paper deliberately does not obtain every innovation as a residual from one large VAR. Such a VAR would tend to use lagged stock returns to forecast macroeconomic variables, indirectly putting equity-market information back into supposedly nonequity factors. The authors prefer simple economic constructions, acknowledging a tradeoff between leaving predictable variation in a factor and introducing error through a misspecified forecasting model.

This choice is consequential. Several proposed “innovations” are realized returns or raw growth rates, not orthogonal forecast residuals. Their interpretation as news is approximate and sometimes rests on auxiliary assumptions. A replicator must preserve the measured variables and separately assess the adequacy of the innovation approximation; relabeling every series as a fully filtered shock would misstate the experiment.

## Definitions, sources, and alignment of the economic factors

Time subscripts refer to the end of a month. Information dated $t-1$ is available at the preceding month-end. Returns dated $t$ accrue during month $t$.

Industrial production is obtained from the *Survey of Current Business*. Let $IP_t$ denote the production flow for month $t$:

$$
MP_t=\log IP_t-\log IP_{t-1},\qquad
YP_t=\log IP_t-\log IP_{t-12}.
$$

Because monthly production is a flow measured over the month, the authors lead monthly production growth by one month in subsequent analysis. They also lead the annual production-growth variable by one year to capture information about future activity reflected in current stock prices. Thus a stock return at $t$ is associated with $MP_{t+1}$ and, where used, $YP_{t+12}$. This alignment is an ex-post measurement design. Those future production observations are not available to an investor at $t-1$.

The annual growth series is highly autocorrelated because adjacent observations overlap. The authors tried forecasting annual production growth and examining unexpected changes and changes in expectations, but found no improvement over the raw series and dropped those filtered alternatives. Their detailed filtering procedure is not provided; a footnote offers it on request. No implementer should invent its lag order and treat the result as the original specification.

Let $I_t$ be the monthly log change in the CPI, and let $TB_{t-1}$ be the known one-month Treasury-bill return applying to month $t$. Unexpected inflation is

$$
UI_t=I_t-E[I_t\mid\mathcal I_{t-1}].
$$

Expected inflation is derived from the Fisher decomposition

$$
TB_{t-1}=E[RHO_t\mid\mathcal I_{t-1}]
 +E[I_t\mid\mathcal I_{t-1}],
\qquad RHO_t=TB_{t-1}-I_t.
$$

The expected real-rate series is taken from Fama–Gibbons' time-series analysis; expected inflation is the short nominal rate less that expected real rate. The explicitly identified supplied expected-inflation series covers 1953–1978. The article does not reproduce the complete real-rate estimation algorithm or fully document how every later observation is extended. Exact replication therefore requires the original forecasting series or its construction code, not an arbitrary AR model of CPI inflation.

A separate factor measures revisions in expected inflation:

$$
DEI_t=E[I_{t+1}\mid\mathcal I_t]-E[I_t\mid\mathcal I_{t-1}].
$$

This becomes an innovation in the strict martingale-difference sense only with an additional assumption about the evolution of expected inflation. It need not have zero unconditional mean merely because it is a change in an expectation. $UI$ and $DEI$ represent different objects: realization error in current inflation and a revision to next month's expected inflation.

For bond-market factors, define

$$
UPR_t=R^{\mathrm{lowgrade}}_t-R^{\mathrm{longgov}}_t,
\qquad
UTS_t=R^{\mathrm{longgov}}_t-TB_{t-1}.
$$

$UPR$ is a **return spread**, not the Baa–Treasury yield spread. $UTS$ is a long-government-bond excess return over the one-month bill, not a simple long-yield-minus-short-yield level. These distinctions change both the timing and economic interpretation of exposures. The glossary occasionally calls the first series $URP$; the equation and result tables use $UPR$ for the same construction.

Long government returns come from Ibbotson–Sinquefield through 1978 and CRSP for 1979–1983. The glossary's earlier starting date differs from the surrounding prose, another reason to obtain the actual data file. The low-grade nonconvertible corporate-bond series is based on Ibbotson's historical sample and extended through 1983 with a custom portfolio: ten bonds rated below Baa in January 1966, still below Baa in 1978, combined with three remaining bonds from the earlier series. Its maturity is shorter than the long-government series, its ratings change over time, and some constituent bonds are unrated.

The authors interpret the return difference as a proxy for changes in risk compensation. It is not a clean constant-duration credit innovation. Changes in rating standards, maturity mismatch, and the hand-built extension can affect its measured exposure. The exact thirteen bond identifiers, weights, treatment of missing prices, and rebalancing details are not supplied in this paper.

$EWNY$ and $VWNY$ are CRSP equal-weighted and value-weighted NYSE index returns. They are included as competing explanatory variables, rather than used to construct the macroeconomic factors. Consumption growth $CG$ is growth in seasonally adjusted real per-capita consumption excluding durables but including services, constructed from CITIBASE and Census population estimates. It runs January 1959–December 1983 and extends a Hansen-supplied series through 1979. Oil growth $OG$ is the monthly log change in the BLS Producer Price Index for crude petroleum, identified as DRI series 3884. Consumption and oil growth are both led by one month in their pricing tests to address measurement timing and favor their explanatory opportunity.

## Are these measured factors really innovations?

Tables 2–3 provide useful diagnostics rather than proving the innovation assumptions. Their full descriptive sample is explicitly January 1953–November 1983, 371 months. The two equity indices correlate 0.916. Monthly production has only 0.103 correlation with the equal-weighted index and 0.020 with the value-weighted index, consistent with substantial measurement and timing differences between monthly macroeconomic flows and rapidly adjusting asset prices.

The bond factors correlate −0.752 over the full descriptive sample, reaching −0.890 in 1978–November 1983. This is partly mechanical: long-government returns enter $UPR$ with a minus sign and $UTS$ with a plus sign. Inflation revision and inflation surprise correlate 0.378. The high negative bond-factor correlation weakens separate coefficient precision; replacing government bonds with Aaa bonds in $UPR$ improves significance somewhat without changing the qualitative conclusions, according to an unreported robustness exercise.

Annual production growth has first-order autocorrelation 0.9615. Monthly production has first-order autocorrelation −0.0990 but a very large twelfth-order autocorrelation of 0.8030. Its adjusted 24-lag Box–Pierce statistic is 632.9. Thus it is not defensible to describe $MP$ as statistically white noise simply because its first-order autocorrelation is modest. Oil growth has first-order autocorrelation 0.4088, and real consumption growth −0.2458. These values document limits to the raw-series innovation approximation.

The paper suggests that predictable contamination creates an errors-in-variables problem that reduces loading precision and significance. That is a motivation rather than a general theorem about the sign of bias in every multivariate generated-regressor setting. Correlated measurement errors can redistribute coefficients across factors in more complicated ways. For a modern implementation, filtering and inference choices should be recorded as extensions rather than silently substituted for the published raw or economically constructed series.

## Two-pass cross-sectional pricing experiment

Equation (12) is the main time-series model:

$$
R_{pt}=a_p+b_{p,MP}MP_t+b_{p,DEI}DEI_t
 +b_{p,UI}UI_t+b_{p,UPR}UPR_t+b_{p,UTS}UTS_t+e_{pt},
$$

with the production factor aligned using the lead convention already described. Other specifications add annual production, one equity index, consumption, or oil. Each loading is a partial exposure from a simultaneous regression, unless a deliberately asymmetric market-index test specifies otherwise.

The assets are 20 equal-weighted portfolios formed by firm size, measured as the market value of the constituent firms at the beginning of a test period. Sorting on size is intended to spread average returns, exploiting the known size pattern to improve cross-sectional discrimination. The paper reports that sorting on market beta or residual variance failed to spread subsequent returns adequately. Price-level sorts produced less dispersion and weaker individual macro-factor significance. Thus the selected test assets are not incidental to the reported strength of the results.

At the start of each annual test cycle, use the previous five years, or 60 monthly observations, to estimate portfolio exposures. Hold those exposure estimates fixed for the next twelve monthly cross sections. Each month regress realized portfolio returns on an intercept and the estimated exposure vector:

$$
R_{pt}=\lambda_{0t}+\hat b_p'\lambda_t+\eta_{pt},\qquad p=1,\ldots,20.
$$

Repeat exposure estimation for the next year. For each factor, average its monthly cross-sectional coefficient and test the mean against zero using the time-series variation of these coefficients. In ordinary notation the historical statistic is

$$
t_j=\frac{\bar\lambda_j}{s(\hat\lambda_{jt})/\sqrt T}.
$$

A monthly coefficient combines the factor's expected premium with the realized common surprise in that month. Averaging attempts to isolate the premium. If the measured factor has a nonzero predictable component, this interpretation requires corresponding care about centering and the maintained pricing relation.

Portfolio grouping reduces individual return noise and estimated-exposure error, but it does not make the first-pass betas known. The article does not apply a later estimated-beta correction, report HAC standard errors, or provide a complete finite-sample distribution accounting for every generated macroeconomic regressor. The published t-statistics should therefore be treated as the reported historical inference under the maintained procedure.

The source's endpoint descriptions are internally inconsistent. Descriptive statistics end in November 1983, several source series are said to end in 1983, and the full-period market-beta experiment is described as 1958–1983. Yet Tables 4–7 label their pricing periods 1958–84 or 1964–84, with final subperiod 1978–84. This note retains those table labels when reporting their estimates and does not invent a precise 1984 end month or observation count. The original data or code is needed to resolve that discrepancy.

Nor does the paper fully specify portfolio membership identifiers, all listing and missing-return eligibility rules, exact historical construction of portfolio returns for newly reformed size groups, or the number of stocks in each group. These are material replication inputs. A reasonable contemporary implementation can document choices, but cannot claim those choices were uniquely determined by the article.

## Core estimates and their scale

Table 4's heading states “Percent per Month × 10.” Accordingly, a displayed coefficient of 13.589 corresponds to 1.3589% per month per unit loading in that factor's normalization. It is not the return on a unit-volatility factor portfolio, and multiplying a loading by a rescaled factor changes the numerical price inversely. T-statistics are dimensionless and unchanged by a consistent positive rescaling.

The five-factor specification without annual production is Table 4B:

| Factor | Full-period displayed coefficient | Monthly percentage-point equivalent | t-statistic |
|---|---:|---:|---:|
| Monthly industrial production, $MP$ | 13.589 | 1.3589 | 3.561 |
| Expected-inflation change, $DEI$ | −0.125 | −0.0125 | −1.640 |
| Unexpected inflation, $UI$ | −0.629 | −0.0629 | −1.979 |
| Bond risk-premium proxy, $UPR$ | 7.205 | 0.7205 | 2.590 |
| Long-bond excess return, $UTS$ | −5.211 | −0.5211 | −1.690 |
| Intercept | 4.124 | 0.4124 | 1.361 |

Monthly production and the bond risk-premium proxy are the clearest full-period results. Inflation surprise is near the conventional two-sided 5% boundary, while expected-inflation changes and the term-structure proxy are weaker. The evidence is differentiated across factors; saying every selected variable is equally strongly priced would overstate the table.

Adding annual production in Table 4A gives it coefficient 4.341 with t-statistic 0.538. It is insignificant in every subperiod. Removing it barely changes the other variables, supporting the reduced five-factor specification used for most comparisons.

The middle period, 1968–1977, is especially informative. In Table 4B, $MP$ is 16.966 with t=2.638, $DEI$ −0.245 with t=−3.215, $UI$ −1.353 with t=−3.320, $UPR$ 12.717 with t=2.852, and $UTS$ −13.142 with t=−2.554. In the final labeled subperiod, production's t-statistic is 1.588, the two inflation statistics are −0.552 and −0.274, and the bond-spread statistics are 0.221 and −0.149. The authors note that this final period is shorter, but it also does not independently provide strong evidence of stable premia.

The signs are interpreted as plausible hedging prices rather than formally derived restrictions. Production exposure earns a positive premium because stocks that perform poorly when productive activity is weak are undesirable. Negative compensation for the long-bond excess-return exposure is consistent with assets that gain when long real rates decline providing a hedge against deteriorating future investment opportunities. This interpretation must keep the sign of a bond **return** separate from the sign of a yield change. Positive long-bond returns ordinarily accompany falling yields, not rising yields.

## Competition with market indices

In the symmetric specification, macro factors and the market index enter the same first-pass regression and the same subsequent cross sections. Table 4C adds $EWNY$: its displayed premium is 5.021 with t=1.218, while production remains 14.009 with t=3.774 and $UPR$ 8.130 with t=2.855. Table 4D instead adds $VWNY$: the market premium is −2.403 with t=−0.633, while production is 11.756 with t=3.054 and $UPR$ 8.274 with t=2.972. The macroeconomic results survive the direct comparison better than the market's independently priced contribution.

Table 5 then deliberately favors market-beta information. Panel A uses ordinary single-index market betas alone. The market premium is 14.527, or 1.4527% per month on the Table 4 scale, with t=2.356 over the full labeled period. Thus the market can appear priced when competing exposures are omitted.

Panel B combines these single-index market betas with macro betas estimated jointly among the macro variables. These are not the same market betas as in the symmetric specification. The market premium becomes −9.989 with t=−2.014, while production and $UPR$ remain positive with t-statistics 3.153 and 3.355. A negative significant market coefficient in this augmented regression does not supply evidence for a positive standalone CAPM premium.

Panel C gives the market index an additional advantage by estimating its beta using a full testing-period multiple regression, described in the text as 1958–1983, and then using that estimate in the monthly cross sections. Macro betas retain their earlier rolling estimation design. This deliberately uses ex-post information for the market exposure and must not be described as a feasible investor procedure. The market coefficient becomes 11.507 with t=1.189, still insignificant, while production, inflation, and bond factors retain useful pricing associations.

These outcomes contrast with time-series explanatory power. The equal-weighted market's average first-pass t-statistics range from 11.7 to 29.9 across the size portfolios. The largest nonmarket statistic is only about 3.4 before including an index and about 2.5 afterward. High contemporaneous correlation among large equity aggregates does not imply that their exposure differences identify the cross section of expected returns.

The authors acknowledge a joint-hypothesis limitation: macro factors might improve measurement of the true aggregate-wealth portfolio, account for assets missing from an equity index, or correlate with errors in market-beta estimates. The comparison therefore challenges the sufficiency of the observed NYSE index in this experiment, not every theoretically possible market portfolio.

## Consumption, oil, and source inconsistencies

The consumption-beta null is written as $E[R]-r\mathbf1=b_c k$, where risk aversion suggests $k>0$. The alternative adds macro exposures: $E[R]-r\mathbf1=b_c k+Bq$. The null requires the added premium vector $q$ to vanish. Because consumption data begin in 1959 and five years are needed to estimate exposures, the pricing test begins in 1964. Consumption and macro betas are estimated simultaneously, with consumption growth led one month.

Table 6's printed consumption coefficients are 0.68 (t=0.108) for 1964–84, −0.485 (t=−0.659) for 1964–77, and 1.173 (t=0.998) for 1978–84. None is significant. The text nevertheless says the consumption signs are negative and wrong in general. That statement conflicts with the displayed positive full-period and final-subperiod entries. The defensible conclusion is lack of significant independent pricing evidence in the table; a uniform negative-sign conclusion is not supported by the printed numbers. A second small inconsistency is a positive printed middle-period $DEI$ coefficient paired with a negative t-statistic. This note does not silently choose an unverified sign for that cell.

The other factor estimates remain broadly similar after adding consumption. Full-period production is 14.964 with t=3.800; $UPR$ is 8.813 with t=2.584; unexpected inflation is −0.846 with t=−2.250. Measured aggregate consumption is therefore not sufficient to subsume these exposures in the test. Measurement error, aggregation across goods, and time-varying betas remain possible explanations; the result is not a rejection of every marginal-utility pricing model.

Table 7 adds one-month-led oil-price growth. Its full-period coefficient is 2.930 with t=0.996. The early subperiod gives 4.955 with t=1.978, but 1968–1977 gives only 1.038 with t=0.251, and the final subperiod 2.738 with t=0.303. Thus the period surrounding OPEC's increased influence does not show a separately priced oil exposure in these size portfolios.

Oil's inclusion weakens production's independent significance while strengthening the two bond factors. In the full-period regression, production's t-statistic falls to 1.406, $UPR$ rises to 4.294, and $UTS$ becomes −2.770. This can reflect overlapping economic information or coefficient redistribution. It does not imply that oil news has no effect on any individual industry or that oil prices never move the market; the test asks about a distinct cross-sectional expected-return price after other exposures are controlled.

## Exposure units and the meaning of a factor premium

For implementation, suppose a measured factor is rescaled from $F_j$ to $aF_j$. Its first-pass loading changes from $b_{pj}$ to $b_{pj}/a$, so its cross-sectional price must change from $\lambda_j$ to $a\lambda_j$ to preserve fitted returns. The economically relevant fitted contribution $b_{pj}\lambda_j$ is invariant. This is why one cannot rank the importance of industrial production and inflation by comparing their printed premium magnitudes without accounting for their scales and exposure dispersion.

The sign of a loading is also distinct from the sign of its premium. A portfolio with negative exposure to a positively priced production factor receives a negative contribution from that factor in the fitted expected-return equation. Whether this portfolio is a useful hedge depends on the other exposures and on estimation error. The paper estimates a simultaneous cross-sectional relation; it does not assert that every stock has a positive production loading or that one factor's premium alone determines its total expected return.

## Reproduction priorities and interpretation limits

A faithful pipeline should first reconstruct the raw series and record their observation, release, and alignment dates. Maintain the historical leads as part of the pricing-measurement exercise, while flagging them explicitly as unavailable for real-time forecasts. Construct the two bond return spreads from matched return units, not yields. Reproduce the correlation and seasonal-autocorrelation tables before interpreting any measured variable as an innovation.

Then recover size-portfolio membership and the five-year first-pass windows, estimate exposures jointly for each specified model, and freeze them for the following twelve monthly cross sections. Save each monthly coefficient series and its time-series standard error. Reproduce the symmetric market comparison separately from the two asymmetric market-beta experiments; mixing their first-pass exposure definitions would invalidate the intended comparison.

There is no portfolio optimization objective, transaction-cost model, risk-aversion calibration, or trading rule to reproduce. The estimands are exposure prices and their historical significance. Full economic implementation would additionally need a model of conditional expected factors, parameter uncertainty, changing exposures, and feasible hedging portfolios. Those extensions are not delivered by a table of unconditional cross-sectional premia.

The strongest limitations are the selected size-portfolio cross section, incomplete innovation filtering, substantial bond-factor collinearity, generated inflation expectations, and unresolved data-vintage and endpoint details. The paper neither conducts a comprehensive multiple-testing correction nor provides an untouched external validation sample. Its contribution remains substantial: it supplies a concrete economic vocabulary and an implementable two-pass framework for asking which kinds of news are associated with priced equity exposures, while demonstrating that strong time-series market comovement and successful cross-sectional pricing are different empirical achievements.
