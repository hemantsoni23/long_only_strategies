# Investor Inattention and the Market Impact of Summary Statistics

Thomas Gilbert, Shimon Kogan, Lars Lochstoer, and Ataman Ozyildirim, *Management Science* 58(2), February 2012, 336–350, DOI 10.1287/mnsc.1110.1475. Source: [15-page library PDF](<../../Finance/InvestorInattention_Kogan_2012.pdf>), together with the complete 19-page [author-hosted online appendix, July 27, 2011](https://faculty.washington.edu/gilbertt/docs/Gilbert_Kogan_Lochstoer_Ozyildirim_Investor%20Inattention%20and%20the%20LEI_Appendix_2011.pdf). Main-paper references use printed pages; appendix references use its own page numbers and A-equation labels.

## Why this matters

The paper isolates a recurring, scheduled release whose inputs and construction are already public: the Conference Board's U.S. Leading Economic Index, or LEI. It documents equity-price movement in the direction of the release before and during the announcement, followed by reversal. The innovation is to distinguish two forms of inattention. Investors who merely delay processing existing information can create gradual adjustment, but investors who mistake repackaged information for an additional independent signal can create overreaction and subsequent correction.

The replication target is therefore a sequence of conditional price responses, not simply a positive announcement coefficient. The paper combines an explicit heterogeneous-beliefs model, intraday aggregate equity and Treasury futures data, stock-level cross-sectional tests, and matched volatility/volume comparisons. Its advertised trading return requires extra care: the tables are regression-response estimates, and a response to a standardized shock is not automatically the realized mean of a sign-based strategy.

## Why the LEI is treated as stale information

The ten historical components are manufacturing weekly hours, initial unemployment claims, manufacturers' new orders for consumer goods/materials, vendor delivery performance, nondefense capital-goods orders, building permits, S&P 500 prices, real M2, the ten-year Treasury–federal-funds spread, and consumer expectations. The main text names the Conference Board expectations index, while the component-response exercise in Table 5 labels a University of Michigan sentiment series. An exact reconstruction must reconcile historical component definitions and release series rather than assume these labels identify the same data.

Appendix equation (A.1) describes weighted symmetric percentage changes:

$$
\Delta LEI_t=\sum_{i=1}^{10}\sigma_i\,200\frac{X_{i,t}-X_{i,t-1}}{X_{i,t}+X_{i,t-1}},\qquad
\sigma_i=\frac{1/\operatorname{SD}_i}{\sum_j1/\operatorname{SD}_j}.
$$

Here the appendix uses $t$ partly as a release-date label; the economic reference month precedes release. A production implementation must retain both labels. Inverse-volatility standardization prevents the most variable component from dominating. The appendix is a compact description, not a complete vintage-by-vintage index-production codebook: the historical estimation windows for standardization, treatment of rate/diffusion components, and exact revision implementation require the referenced Conference Board methodology.

Before January 2001, releases in month $t$ refer to $t-2$ and use the complete component set. Thereafter, releases refer to $t-1$, with roughly seven available components and estimates for the missing inputs. The missing series are consumer-goods/materials orders, nondefense capital-goods orders, and the consumption deflator used for M2. The appendix specifies autoregressive estimation using two lags, with current CPI included in the deflator estimate when already available. Thus the claim of predictability concerns reproducing the publisher's rule with real-time information, not forecasting the later realized macroeconomic data perfectly.

All relevant inputs or their rule-based estimates are available before the event; the latest relevant component release is no later than 8:30 a.m. on the previous trading day. The paper uses original released LEI values rather than revised history. This vintage distinction is essential: a modern revised index is not a valid substitute for the information available to the proposed trader.

## A reconstructible three-date equilibrium

The appendix has a risky claim paying independent normal dividends $d_t\sim N(0,D)$, where $D=\sigma_d^2$, with terminal ex-dividend price $p_3=0$. Trading occurs at dates 1 and 2 after current dividends and signals are observed. A risk-free asset pays zero interest, discounting is absent, and risky-asset supply is set to zero. The masses of attentive and inattentive investors are $m$ and $1-m$, with positive CARA risk-aversion coefficients $a_A,a_I$. They maximize one-period expected utility myopically.

The mean-variance demand implied by this normal/CARA setup is

$$
x_{j,t}=\frac{E_j[p_{t+1}+d_{t+1}\mid\mathcal I_{j,t}]-p_t}{a_j\operatorname{Var}_j(p_{t+1}+d_{t+1}\mid\mathcal I_{j,t})},\qquad
mx_{A,t}+(1-m)x_{I,t}=0.
$$

The appendix's initial inline demand formula omits $a_j$; its subsequent clearing equations include it. The expression above follows those equations. For arbitrary conditional means $\mu_A,\mu_I$ and variances $V_A,V_I$, clearing gives a risk-tolerance/precision-weighted average of means, with weights $m/(a_AV_A)$ and $(1-m)/(a_IV_I)$. This formula provides a direct numerical solution at each date.

At date 1, the actual signal is $s_1=d_3+\epsilon_1$, with independent noise variance $E=\sigma_\epsilon^2$. Date 2 repeats it exactly: $s_2=s_1$. Define

$$
\kappa_1=\frac{D}{D+E},\qquad \kappa_2=\frac{D}{2D+E}.
$$

One signal implies posterior mean $\kappa_1s_1$ and variance $\kappa_1E$. Two conditionally independent signals would imply mean $\kappa_2(s_1+s_2)$ and variance $\kappa_2E$. In the actual data-generating model the second signal is not independent; that false assumption is precisely the inattentive investors' mistake.

With all investors attentive, both prices equal $\kappa_1s_1$. The intervening dividend remains risky, but zero net supply and common beliefs leave no trade motivated by disagreement. No additional information arrives with the duplicate signal, so there is no average stale-release response or subsequent correction.

In the delayed-processing model, inattentive investors ignore the first signal and do not infer it from prices. At date 2 they learn it, so $p_2=\kappa_1s_1$. At date 1 the attentive mean is $\kappa_1s_1$ and variance $D$, whereas inattentive investors use mean zero and variance $D+\kappa_1^2(D+E)$. Therefore

$$
p_1=\frac{\kappa_1s_1}{1+B},\qquad
B=\frac{(1-m)a_AD}{ma_I[D+\kappa_1^2(D+E)]}.
$$

For $0<m<1$, positive variances, and positive news, price underreacts initially and rises to the common-information value upon rerelease. There is no expected subsequent reversal. Risk aversion and the unpredictable intervening dividend prevent attentive investors from taking unlimited positions that eliminate the delay.

In the double-counting model, both groups observe $s_1$, but inattentive investors treat $s_2$ as a fresh independent signal and believe other investors share their interpretation. The attentive understand the actual signal duplication and the other group's error. At date 2 their respective means are $\kappa_1s_1$ and $2\kappa_2s_1$, with variances $\kappa_1E$ and $\kappa_2E$. Equation (A.19) clears these demands without further simplification.

For the displayed solution the authors set $1/(a_A\kappa_1E)=1/(a_I\kappa_2E)=1$. This means $a_I=(\kappa_1/\kappa_2)a_A$ and fixes the demand scale. Let $q=m\kappa_1+2(1-m)\kappa_2$. Then $p_2=qs_1$, with $q>\kappa_1$ if inattentive investors are present.

At date 1, attentive investors forecast $qs_1$ with payoff variance $D$. Inattentive investors forecast $\kappa_2(1+\kappa_1)s_1=\kappa_1s_1$, using variance $D+\kappa_2^2(1+\kappa_1)E$. Define

$$
u_A=\frac{m}{a_AD},\qquad
u_I=\frac{1-m}{a_I[D+\kappa_2^2(1+\kappa_1)E]}.
$$

Directly solving equations (A.23)–(A.24) yields the convenient equivalent expression

$$
p_1=\frac{u_Aq+u_I\kappa_1}{u_A+u_I}s_1.
$$

For positive news and interior population shares, $0<\kappa_1s_1<p_1<p_2$. Expected terminal payoff is still $\kappa_1s_1$, so the final expected price change is negative. Negative news reverses the price-difference signs. This supplies an implementable mechanism for initial overshooting, further stale-release movement, and eventual reversal without fitting any structural parameters to the empirical regressions.

Several printed appendix expressions need care. Equation (A.26) drops a multiplying $s_1$ that appears in adjacent equations. Its simplified coefficient also fails to agree with (A.23)–(A.24) under the stated normalization, so the weighted-mean formula is used instead. Equation (A.29) gives the wrong sign for the final correction after positive news, and (A.31) contains corresponding sign/conditioning inconsistencies. The ranking (A.28), the clearing equations, and the economic discussion establish the correction unambiguously. The weighted-mean reconstruction above avoids propagating those typographical defects. The appendix also discusses a variant where inattentive investors learn from lagged prices but mistake the price-implied signal and public rerelease for independent information. That variant requires consistent price conjectures; it is not the same as fully rational inference from prices.

The model is stylized: Gaussian dividends and zero-supply prices can be negative, so its clean implications are conditional price differences and ordering. It is not a calibrated positive-price futures-return process. The investor share, risk aversion, and signal variances are not estimated from the LEI dataset.

## Data, exclusions, and event clock

The main sample runs from February 1997 to February 2009, starting with the February 4, 1997 release after the LEI moved to an intraday 10:00 a.m. announcement. The Conference Board supplies original values and release dates. Of 146 releases, 30 are excluded for simultaneous 10:00 announcements of new home sales, factory orders, construction spending, the ISM manufacturing index, or the federal-funds target. All exclusions occur in the first four years. The remaining 116 events are the core sample.

Tick Data provides five-minute futures open/high/low/close observations. For each day, the authors select an on-the-run contract and construct returns from that day's contract. The text does not specify an executable contract-selection and rollover rule. The instruments are S&P 500 futures and two-, five-, ten-, and thirty-year Treasury futures. Individual stocks use TAQ and CRSP; beta portfolios include only stocks in the S&P 500 at the announcement date, avoiding a present-day-constituent universe.

The three equity intervals are: 10:00 a.m. on the previous trading day to immediately before release; the five-minute release interval, exactly 9:59:59–10:04:59; and 10:05 a.m. on the event date through 16:00 on the next trading day. The last interval was chosen ex post because reversal persisted into the next day. This is an explicit design limitation, not an independently prespecified holding period. The source labels times EST; implementation should align them to historical New York trading clocks and daylight-saving conventions rather than apply a fixed UTC offset blindly.

Let $z_t$ be the release change minus Bloomberg's median analyst forecast, normalized using the sample surprise dispersion; the descriptive table centers the full-sample series at zero and scales it to unit standard deviation. Returns are log returns expressed in percent. For each interval $i$, equation (1) is

$$
R_{t,i}=\gamma_i+\delta_i z_t+\varepsilon_{t,i}.
$$

A coefficient .045 means 4.5 basis points for a one-standard-deviation positive surprise, not 4.5% and not necessarily an unconditional return. Standard errors are heteroskedasticity corrected; stock-level cross-sectional results additionally cluster by announcement date. Analyst forecast timestamps are unavailable. The authors report that forecasts often arrive a week or more beforehand, so a surprise relative to that forecast can be predictable with later public components.

## Main results and a trading-return qualification

Table 2 reports the following aggregate regression slopes in percentage points per standardized surprise; parentheses contain standard errors:

| Instrument | Before release | Five-minute release | After release | Total response | Reported strategy response |
|---|---:|---:|---:|---:|---:|
| S&P 500 | .261 (.152) | .045 (.019) | −.347 (.119) | −.041 (.200) | .652 (.205) |
| 2-year Treasury | −.007 (.010) | −.005 (.002) | .025 (.016) | .013 (.017) | .037 (.021) |
| 5-year Treasury | −.013 (.027) | −.013 (.004) | .070 (.040) | .044 (.043) | .096 (.054) |
| 10-year Treasury | −.020 (.044) | −.021 (.006) | .101 (.059) | .060 (.068) | .143 (.082) |
| 30-year Treasury | −.039 (.076) | −.032 (.009) | .089 (.085) | .019 (.111) | .160 (.123) |

For equities, preannouncement significance is only at 10%, announcement significance at 5%, and reversal at 1%. The total is indistinguishable from zero. Announcement $R^2$ is 6.7%; the reported strategy-response regression has $R^2=10.5\%$. Treasury announcement slopes are negative and significant at 1%, but preannouncement effects are insignificant and reversal evidence is weaker. The thirty-year strategy response is not statistically significant. This is qualified cross-market corroboration, not equally strong evidence in every instrument.

The stated equity strategy takes a position in the surprise's direction at 10:00 the previous day, reverses that position at 10:05 on release day, and closes at the next day's end. Positive news therefore entails buy one, sell two, buy one in unit-exposure terms. The authors report approximately 65 basis points gross per event and 7.8% annually. They estimate costs using SPY's average seven-basis-point quoted spread at the relevant times: four one-way units at half spread imply 14 basis points per event, leading to about 6% annually. They do not observe futures execution costs directly.

There is an unresolved reporting distinction. The table labels its entries as slopes on standardized surprise, and the aggregate .652 coefficient closely equals $.261+.045-(-.347)$. For the signed fixed-exposure strategy, event log-P&L would instead be approximately $\operatorname{sign}(z_t)(R_{pre,t}+R_{ann,t}-R_{post,t})$. Its sample mean cannot be recovered from a slope alone; it depends on the realized surprise magnitudes and residuals. Under an ideal centered linear model it involves $E|z_t|$, not necessarily one. The paper's annual number should therefore be retained as an author-reported extrapolation, not independently verified performance from the available table.

A faithful replication should compute the event-by-event signed strategy directly using point-in-time component reconstruction, retain zero-surprise treatment explicitly, and report actual event frequency. The 116 retained events over roughly twelve years also differ from a blanket twelve-trades-per-year extrapolation. Margin capital, collateral yield, financing, roll costs, price impact, and implementable futures bid/ask fills are not specified. Full-sample normalization is acceptable for an explanatory regression but must be replaced by a historical rule if it determines a live trading threshold.

## Cross-sectional and time-varying tests

Market betas come from daily CRSP data in the preceding year. Each event's contemporaneous S&P 500 universe is sorted into beta quintiles. Returns equally weight stocks trading in both the first and last minute of an interval; multiple trades within a minute are averaged, and nonpositive prices are removed. For the announcement interval the initial stock-price minute starts at 9:58 to accommodate transaction timestamp errors. This differs deliberately from the futures clock.

The highest-beta quintile has before/announcement/after slopes .613, .101, and −.681, with strategy response 1.505; the lowest has .166, .037, and −.103, with strategy response .323. The reported strategy-response difference is about 117 basis points and significant at 1%. Stock interval samples differ because a firm must have all required endpoints to enter total/strategy regressions; consequently individual interval slopes need not add exactly to those columns. The larger response among high-beta stocks is consistent with traders treating the LEI as aggregate news, but does not estimate individual traders' beliefs.

Within the top-beta quintile, the authors sort again into five prior-year volatility groups. Strategy-response slopes rise from 1.098 (.447) to 1.999 (.786); the high-minus-low difference is .891 (.423), significant at 5%. Announcement-response slopes rise from .086 to .107, but the .021 (.021) difference is not significant. Higher background risk is consistent with costly arbitrage; volatility is a proxy, not a measured constraint on arbitrage capital.

The second conditioning variable is a lagged monthly measure from Tetlock's firm-news data. Daily cross-sectional regressions relate returns on days 2–5 after firm news to announcement returns and their interaction with textual staleness, along with controls. The negative monthly average interaction coefficient measures stronger reversal after stale firm news. The LEI test uses the previous month's measure $S_{t-1}$, standardized to unit variance:

$$
R_{t,i}=\alpha_i+\beta_{0i}S_{t-1}+\beta_{1i}z_t+\beta_{2i}S_{t-1}z_t+\epsilon_{t,i}.
$$

In Table 3, the announcement interaction is .017 (.020), statistically insignificant; the strategy-response interaction is .512 (.236), significant at 5%. Baseline surprise slopes are .033 (.015) and .574 (.211). The interpretation is stronger responses when a separate stale-news bias measure is high. The underlying textual dataset and full first-stage control specification are delegated to Tetlock. His data omit the last two months of the LEI sample, whereas the table caption repeats the full 116-event description; the exact usable regression count needs raw-data verification.

## Volatility, volume, and robustness

Announcement dates are matched to the day one week later unless that day contains another important release, in which case the authors choose the day following the LEI release. Five-minute returns on both days are scaled by the matched nonannouncement day's volatility during the relevant hour. Expected five-minute returns are set to zero. The text forms interval variance estimates $T^{-1}\sum_t\widetilde R_{it}^2$ and describes a Levene-type comparison, while Table 6 describes regressions of log standard-deviation ratios on a constant with White standard errors. These descriptions do not completely identify one common estimator; both should be checked in reproduction rather than assumed identical.

For 10:00–10:05, Table 6 gives a volatility log-ratio .261 (.083) and volume log-ratio .067 (.023). For the 34 events with surprises at least one standard deviation from the mean, these are .387 (.156) and .110 (.044). If interpreted literally as log ratios, exponentiation gives about 29.8% and 6.9% increases for the full-sample volatility and volume measures. The article's prose calls the volatility increase approximately 25–26%, using the log-point approximation. The exact transformed number and the approximation should not be conflated. Volume remains modestly elevated in the next three reported intervals; preannouncement comparisons are insignificant.

Appendix Table A.I replaces median forecasts with zero expected change, the historical mean available at the time, a one-year moving average, and the previous release's change. S&P announcement slopes are .045, .029, .030, .040, and .041 respectively, with standard errors .019, .016, .015, .015, and .015. Median-forecast slopes are .048 (.022) and .049 (.023) in the two 58-event halves. Restricting to nonzero median-forecast surprises gives .056 (.023); large surprises give .091 (.038). These checks support the sign and timing across expectation proxies, while subgroup selection and normalization remain part of the design.

Table A.II pools six five-minute response intervals from 10:00 to 10:30, includes six lagged returns and five lagged surprise effects, and has 696 observations. Errors are adjusted for heteroskedasticity, date clustering, and six autocorrelation lags as described in the appendix. The contemporaneous median-forecast surprise coefficient is .045 (.018). The subsequent five coefficients are −.008, −.018, −.013, −.014, and −.012, all insignificant. Thus the documented reversal is not concentrated in the next few minutes; the longer post-event interval is material.

Initial component-release tests find equity responses to unemployment claims and M2, and Treasury responses to these and vendor-performance information. Many other component tests are insignificant, with identification weakened by subheadline status, simultaneous releases, and thin premarket trading. This evidence is not a complete component-by-component demonstration that every input had already been incorporated into prices.

## What a reproducible implementation still needs

The source supports the equilibrium equations and the event-study architecture, but not a turnkey executable strategy. Essential missing inputs include historical index-production vintages and weights, the exact autoregression estimation windows, analyst forecast snapshots, event exclusions, contract-roll selection, TAQ cleaning details, the first-stage textual-bias data, and the raw signed strategy P&L. The announcement/postannouncement design is observational, with an ex-post reversal window and numerous subgroup tests; no common multiple-testing adjustment or truly held-out strategy validation is reported.

The substantive finding is a temporary response to scheduled repackaging of existing information, with a reversal pattern more consistent with double counting than with simple delayed processing within the authors' models. That interpretation is stronger when coupled with the stale-news conditioning test and the arbitrage-risk comparison, but those tests do not directly observe cognition or establish unique causation. The paper's model, regression response, and claimed tradable return are related objects that must remain distinct in any reconstruction.
