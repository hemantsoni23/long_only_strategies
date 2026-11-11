# High frequency trading and the 2008 short-sale ban

**Jonathan Brogaard, Terrence Hendershott, and Ryan Riordan (2017).** *Journal of Financial Economics* 124, 22–42. DOI: 10.1016/j.jfineco.2017.01.008. Source: [original PDF](../../Finance/shortsaleban_hendershott_2017.pdf), all 21 pages including Appendix Figures A1–A3 and Tables A1–A4. Page references are printed journal pages. This note distinguishes published coefficients from their causal interpretation and identifies measurement ambiguities that matter for reproducing them.

## Why this matters

Short sellers are heterogeneous. A reduction in aggregate short selling can worsen liquidity even if removing one particular kind of short seller improves it. The paper uses the September 2008 U.S. short-sale ban to separate high-frequency traders' short sales from other investors' short sales. The estimated effects have opposite signs: the ban-induced component of HFT short selling raises spreads, while non-HFT short selling lowers them.

The methodological contribution is a cross-sectional instrumental-variable design. Rather than assuming the ban affects liquidity only through total short sales, the authors allow the ban itself to enter the liquidity equation. Identification comes from interactions between the ban and pre-existing stock characteristics that differentially affect HFT and non-HFT activity. This is intended to distinguish simultaneous changes in two kinds of trading during an unusually turbulent period.

The mechanism evidence concerns the timing of liquidity demand. HFTs tend to trade aggressively when spreads are narrow and subsequent prices move against their counterparties. That can make resting orders unprofitable, discourage competing liquidity suppliers, and reduce other investors' trading. The empirical result concerns immediacy costs and a particular activity margin in crisis conditions. It does not establish that all HFT activity, all automation, or all short selling reduces welfare in normal markets.

## Sample, treatment, and observable trader types

Nasdaq supplies transaction data covering August 1 through October 31, 2008, plus a separate Regulation SHO short-sale flag file. Transactions have millisecond timestamps, symbol, share quantity, price, buy/sell initiation, and the HFT/non-HFT identity of the liquidity demander and supplier. The dataset covers executions on Nasdaq against displayed and hidden orders. It excludes executions on other venues and off-exchange transactions merely reported through Nasdaq's trade reporting facility.

Nasdaq classifies specialist HFT firms using customer knowledge and trading characteristics such as intraday position crossings, order duration, and order-to-trade ratios. The flag does not identify HFT activity inside large integrated financial institutions. Thus “non-HFT” is a residual classification, not a guarantee that every included trade is manual or slow. Individual HFT identities are unavailable, limiting strategy-level analysis.

The final balanced sample comprises 379 banned stocks and 379 matched non-banned controls, using the matches from Boehmer, Jones, and Zhang. Of the banned stocks, 319 are covered initially and the remainder enter later. The article initially refers to 758 banned stocks when describing received data, but its final counts and regressions clearly use 758 total treated-plus-control stocks. The final-panel definition is the relevant replication target.

The main regulatory ban begins September 19 and ends October 8, 2008. The authors drop the first day because it coincides with triple witching and the TARP announcement, and the last day because of uncertainty about the termination. The pre-ban period is August 1–September 18. Stocks must trade every day of the retained sample. The paper reports 64 trading days after exclusions, but regression counts are 23,877 for banned stocks alone and 47,754 with controls, equal to 379 or 758 times 63. Calendar arithmetic supports 63: the date interval contains 66 weekdays, less the Labor Day market holiday and the two excluded ban dates. No additional loss from the lagged volatility control is needed to explain those counts. The source's statement of 64 trading days remains inconsistent with this reconstruction.

Keep only continuous trading from 09:30 to 16:00 and remove opening and closing crosses. Nasdaq HFT and short-sale records share timestamps and are joined directly. National quotes and liquidity outcomes come from Daily TAQ, with the NBBO constructed using the cited Holden–Jacobsen method. CRSP provides capitalization. Most liquidity outcomes use all-market TAQ transactions and national quotes, whereas explanatory trader activity is measured on Nasdaq. This cross-venue distinction is important to both reconstruction and interpretation.

Transaction types are `HH`, `HN`, `NH`, and `NN`, where the first letter denotes the liquidity demander and the second the supplier. HFT demand volume combines HH and HN; HFT supply volume combines HH and NH. Total HFT activity is their sum, so a transaction between two HFTs contributes both HFT sides. This differs from the fraction of trades with at least one HFT participant. The analogous conventions apply to non-HFT activity. Short-sale volume counts the identified short-selling side, further split by whether that side supplies or demands liquidity.

For each stock-day, divide the relevant dollar volume by total Nasdaq dollar trading volume. The resulting `RelSS HFT` and `RelSS non-HFT` variables are reported in **percentage points of total volume**, not as the fraction of each group's own trades that are short sales. For example, an increase from 6% to 7% is a one-percentage-point increase in the regressor, not a 1% proportional increase. This unit distinction resolves misleading percentage language in parts of the introductory discussion.

## Measuring liquidity consistently

Let $A$ and $B$ be the prevailing national ask and bid, $M=(A+B)/2$ their midpoint, $P$ the execution price, and $q=+1$ for buyer-initiated trades and $q=-1$ for seller-initiated trades. Equation (1) defines the proportional quoted spread:

$$
QS=\frac{A-B}{M}.
$$

Quoted spreads are time-weighted within day in the main tables. Effective spread is printed in equation (2) as

$$
ES=\frac{|P-M|}{M}.
$$

This is a one-way measure without the conventional factor of two. Do not add the factor of two merely because another microstructure library calls a round-trip measure “effective spread.” Equations (3)–(4) define signed realized spread and price impact at a five-minute mark:

$$
RS_{5m}=q\frac{P-M_{t+5m}}{M},\qquad
PI_{5m}=q\frac{M_{t+5m}-M}{M}.
$$

Their sum is $q(P-M)/M$, equal to the absolute-value effective spread when the trade sign is aligned with execution relative to the midpoint. Transactions inside quotes, locked markets, or sign/timestamp inconsistencies require consistent filtering to preserve that identity. The article refers to the NBBO construction methodology rather than specifying every cleaning rule. Multiply ratios by $10^4$ to express basis points. Effective spreads, realized spreads, and impacts are trade-weighted in the main daily outcomes; summary tables then average stock-days.

The effective-spread normalization is potentially consequential: the printed quoted measure is a full quoted spread while the printed effective measure is one-way. Their relative sizes therefore cannot be attributed exclusively to hidden liquidity. The note retains the equations as published rather than silently changing them to a standard convention. Checking the authors' code would be needed to determine whether the numerical tables implement exactly the printed normalization.

Realized spread is a mark-to-market revenue proxy for the passive side, not its complete profit. It excludes exchange liquidity rebates and does not track actual inventory liquidation, hedges, fees, or financing. Price impact measures short-horizon adverse price movement, not the entirety of information efficiency or social value. These distinctions prevent the mechanism tables from being mistaken for complete HFT profit accounts.

Table 1 gives the descriptive scale. For banned stocks, quoted spreads rise from 30.37 basis points before the ban to 73.66 during it and 74.11 afterward. Effective spreads rise from 22.65 to 55.67 and then 53.60. Controls also deteriorate: quoted spreads are 28.44, 44.08, and 59.20. Market-wide crisis conditions therefore make a simple pre/post comparison inadequate.

Relative HFT short sales fall from 6.37% to 1.01%, then recover to 4.82%; non-HFT short sales fall from 15.19% to 5.55%, then recover to 13.50%. Total HFT participation drops from 23.91% to 15.53%, then returns to 21.72%. The ban largely removes HFT shorting but leaves substantial HFT trading. Market-making exemptions and trading from positive inventories are possible reasons. Figure 1 shows abrupt declines and recovery in activity; Figure 2 shows that spreads remain affected by broader market deterioration after the regulatory event.

## Structural equation and excluded instruments

Let $B_{it}$ equal one when stock $i$ is legally subject to the ban on day $t$, and zero otherwise. This is not merely a common calendar-period dummy because stocks enter the list at different dates. Let $C_i$ contain four fixed pre-treatment characteristics, measured August 1:

1. Natural log market capitalization.
2. Price divided by earnings per share, scaled by 100 in the main-table captions.
3. Book equity divided by market equity.
4. Stock price in dollars.

The excluded instruments are $Z_{it}=B_{it}C_i$. HFT activity is expected to react especially to size and relative tick size, proxied by price. Non-HFT short activity is expected to react to fundamental valuation ratios. Fixed August 1 characteristics avoid defining treatment exposure with variables already changed by the ban. Their main effects are absorbed by stock fixed effects.

For each endogenous activity measure $T^k_{it}$, estimate a first stage of the form

$$
T^k_{it}=a_i^k+d_t^k+Z_{it}'\pi_k+\delta_kB_{it}
+X_{it}'\theta_k+u^k_{it}.
$$

The baseline second stage is

$$
Y_{it}=a_i+d_t+\beta_H\widehat T^H_{it}
+\beta_N\widehat T^N_{it}+\delta B_{it}+X_{it}'\theta+\epsilon_{it},
$$

where $T^H$ is relative HFT short sales, $T^N$ relative non-HFT short sales, and $Y$ is quoted spread, effective spread, or its logarithm. This should be estimated as proper 2SLS or an equivalent IV procedure with a consistent instrument matrix and IV covariance estimator, not naive OLS standard errors on fitted first-stage values.

Controls include current price, current log capitalization, previous-day stock volatility measured from one-second returns, contemporaneous XLF financial-sector ETF volatility, and, in the matched sample, the interaction of XLF volatility with banned-stock membership. Lagged individual volatility avoids directly controlling with a variable jointly determined with the current spread. Contemporaneous sector volatility is treated as external to an individual stock's liquidity. Stock and date effects are reported throughout.

There is an unresolved algebraic issue in this reported specification. A common daily XLF volatility series is collinear with a complete set of date effects. In the banned-only sample its banned-stock interaction is also the same series. Nevertheless, tables report both daily effects and a separate XLF coefficient. A faithful implementation with fully saturated date dummies must absorb or drop common daily controls; recovering the authors' separate coefficient requires clarification of their actual fixed-effect normalization or implementation. The identified activity coefficients can still be estimated after removing redundant columns, but this is not evidence that the printed table is uniquely reproducible as written.

## Identification assumptions and inference

The ban itself is an included control, allowing a direct level effect on liquidity. Exclusion instead requires that, conditional on controls and fixed effects, the ban's differential effect by August size, valuation, and price affects spreads through the instrumented trading measures. This is substantially stronger than saying the characteristics were measured before the ban. Other crisis interventions, financial distress, or information shocks could affect large and small or high- and low-book-to-market firms differently at the same time.

Firm effects remove time-invariant differences; day effects remove common daily changes; the ban control removes a common treated-state level effect. None automatically removes a time-varying liquidity shock proportional to a pre-existing characteristic. The authors explicitly discuss TARP and changing financial-sector information as potential violations. The matched sample and volatility controls are intended to mitigate, rather than logically eliminate, those concerns.

Inference uses standard errors clustered by stock and date for the reported panel coefficients. The paper also describes first-stage relevance tests, Sanderson–Windmeijer conditional underidentification/weak-identification diagnostics, Kleibergen–Paap and Cragg–Donald diagnostics, and Hansen–Sargan overidentification checks using HAC calculations with five-day lags. It reports rejection of weak/underidentification at 5% and no evidence of misspecification, but does not print all diagnostic statistics or exact numerical standard errors for the main coefficient tables. A replication should report those missing diagnostics rather than infer their values from significance stars. Nonrejection of an overidentification test cannot establish the exclusion restriction.

The approach identifies the activity changed by this regulatory intervention. It is a local treatment-effect interpretation, not the effect of arbitrarily increasing every HFT strategy. Different shorting-dependent strategies may differ from inventory-based or liquidity-supplying strategies that continue through the ban. Crisis-period variation may also place greater weight on adverse selection than normal-market variation.

## First stages and principal spread results

Table 3 reports a −1.42 coefficient on ban interacted with log capitalization for relative HFT short selling in both banned-only and matched samples. The corresponding non-HFT coefficients, −0.18 and −0.17, are not significant. A one-unit increase in log capitalization therefore predicts a 1.42-percentage-point larger HFT short-sale decline during treatment, conditional on the other terms. The price interaction is positively significant for HFTs, while the book-to-market interaction is approximately zero for them.

Non-HFT short sales respond significantly to the P/E and book-to-market interactions: coefficients are 0.53 for scaled P/E and 0.77 or 0.75 for book-to-market. Their positive signs indicate smaller declines for high-ratio firms relative to the common negative ban effect. The instruments need not be individually exclusive to one trader group; what matters is sufficient independent first-stage variation to separate their coefficients.

The reduced-form spread regression in Table 2 finds the ban's size interaction lowers quoted spreads by 12.60 basis points per unit of log capitalization. Combining a larger fall in HFT shorting with a smaller spread increase motivates a harmful HFT liquidity effect. Book-to-market variation gives the corresponding direction for beneficial non-HFT shorting. The IV analysis combines all four instruments rather than simply dividing one selected reduced-form coefficient by one first-stage coefficient.

The principal Table 4 estimates, in basis points of spread per **one-percentage-point** increase in relative short-sale volume, are:

| Outcome and sample | HFT short sales | Non-HFT short sales |
|---|---:|---:|
| Quoted spread, banned only | +9.54 | −5.17 |
| Quoted spread, with controls matched by stock | +9.61 | −5.20 |
| Effective spread, banned only | +7.96 | −3.42 |
| Effective spread, matched sample | +8.03 | −3.51 |

HFT coefficients in these level specifications are significant at 1%; non-HFT coefficients are significant at 10%. The similar point estimates across sample constructions are useful robustness evidence, although they share the same identifying assumptions.

Log-spread specifications preserve the signs but imply much smaller local magnitudes. For quoted spread, the HFT coefficient is 0.03 in the banned-only sample and 0.02 with controls; non-HFT coefficients are −0.07. For effective spread, HFT coefficients are 0.04 and non-HFT coefficients −0.08. A coefficient of 0.03 means approximately 3% higher spread for a one-percentage-point increase in the activity share, with exact change $e^{0.03}-1\approx3.05\%$. At a 50-basis-point starting spread this is about 1.5 basis points, far below the 9.54-basis-point linear estimate. Functional-form sensitivity is therefore economically important, not a minor numerical detail.

Table 5 replaces HFT short sales with total HFT activity while retaining non-HFT short sales. Banned-only level coefficients are +8.03 for quoted spread and +6.75 for effective spread, with matched estimates +7.99 and +6.72. Non-HFT coefficients remain negative, but several level estimates are not statistically significant. It would overstate the table to claim every non-HFT result is significant. The total-HFT estimate remains tied to activity shifted by the short-sale restriction.

## Mechanism: trading into narrow spreads and adverse price moves

Table 6 uses August data, before the ban, and Nasdaq-only trades for which trader type can be identified. Nasdaq trades are matched to TAQ in a 100-millisecond window, selecting the first compatible match when multiple TAQ records qualify. The authors report 99% match within five milliseconds. This step is distinct from the direct HFT/SHO join.

Aggressive HFT trades pay an average effective spread of 8.29 basis points, versus 12.90 for aggressive non-HFT trades. Passive counterparties to HFT demand realize spreads of −3.24 basis points after ten seconds, −5.47 after one minute, and −6.24 at the longest reported horizon. Against non-HFT demand, those values are +2.68, −1.03, and −2.66. The surrounding prose and caption identify the last horizon as five minutes, but the table's column heading says “Ten-minutes.” This is a genuine labeling discrepancy; the note follows the repeated five-minute description while preserving the uncertainty.

HFTs supplying liquidity have a positive ten-second realized spread of +1.83, falling to −1.84 and −3.48 at longer marks. Non-HFT liquidity suppliers have negative marks at all reported horizons: −1.13, −3.90, and −4.82. Among short sales specifically, aggressive HFTs pay 7.37 basis points and leave passive counterparties with a −3.50-basis-point ten-second realized spread, compared with +0.97 against aggressive non-HFT short sales.

These observations are consistent with HFTs selecting moments when displayed liquidity is cheap relative to the next price movement. They do not reveal a unique private-information channel: rapid response to public signals can generate the same adverse selection for slower resting orders. Nor do negative marked spreads demonstrate negative total profits after exchange rebates or inventory management.

Table 7 decomposes the aggregate IV effect. For banned-only stocks, a one-point increase in relative HFT shorting raises effective spread by 7.96 basis points, split into +6.07 realized spread and +1.89 price impact. The matched split is +6.11 and +1.91. The larger realized-spread component suggests that reduced competition or altered timing of liquidity supply accompanies the direct adverse-selection effect. It is not inconsistent with negative realized spreads on individual trades against HFTs: the first calculation concerns equilibrium average spreads as participation changes, whereas Table 6 conditions on selected counterparties and trade times.

Table 8 instruments HFT demand-side and supply-side short sales separately, together with non-HFT short sales. HFT demand coefficients are +9.38 or +10.80 on quoted spread and +9.91 or +11.04 on effective spread. Supply coefficients are positive but statistically insignificant: quoted +9.76 or +7.97, effective +5.31 or +3.90. Thus the most precise evidence points to aggressive HFT trading; failure to reject the supply coefficient does not establish that liquidity provision is harmless. Treating demand and supply as separate strategies is itself an assumption because firms cannot be tracked individually.

## Non-HFT participation, appendices, and welfare limits

Table 9 uses the log of non-HFT **non-short** dollar volume as the outcome. Excluding their short sales avoids mechanically treating the ban's direct restriction of those sales as reduced ordinary participation. The coefficient on instrumented HFT relative short sales is −0.04 in both samples, significant at 10% for banned-only and 5% with controls. A one-percentage-point rise in the HFT short-sale share is associated with approximately 4% lower non-HFT non-short volume; the exact semilog change is $e^{-0.04}-1\approx-3.92\%$.

Appendix Table A4 instruments spreads directly with the characteristic-by-ban variables and finds negative effects on non-HFT volume: quoted-spread coefficients −0.37 or −0.36 and effective-spread coefficients −0.42 or −0.41, with spread regressors expressed in percent. These are not coefficients per basis point. The result supports a link between immediacy costs and activity but inherits the exclusion assumptions of the instruments.

Appendix Figures A1–A2 show daily cross-sectional spread-characteristic coefficients changing during the ban: size becomes more negatively associated with log spreads and book-to-market shifts downward, then partially reverses. Figure A3 plots the ordinary non-HFT volume difference. These plots show timing consistency but are not independent randomization evidence.

Tables A1–A3 remove the time-varying controls while retaining the ban and stock/date effects. The level HFT short-sale effect remains approximately +9.44 to +9.45 basis points for quoted spreads and +7.77 to +7.78 for effective spreads. Log quoted-spread coefficients lose significance. Total-HFT level effects remain positive. The appendix changes the stated P/E scaling from division by 100 to division by 10,000; pure rescaling of an excluded instrument should not alter a correctly estimated IV coefficient, but it does alter its printed first-stage coefficient and must be recorded.

The authors argue that lost non-HFT trading can mean lost gains from trade. They do not estimate demand curves, reservation values, or a numerical welfare loss. Wider spreads can partly be transfers between impatient and patient traders, and information incorporated into prices can have benefits outside immediate execution costs. Restrictions on aggressive HFT trades might also impair inventory management and thereby reduce passive supply. The policy implications therefore remain qualified even if the estimated liquidity effect is accepted.

## What an independent implementation still needs

Reproduction requires licensed Nasdaq trader flags, transaction-level short indicators, TAQ, CRSP, accounting characteristics, dated ban membership, and the original matched-stock list. The paper reports academic access under a nondisclosure agreement, not an unrestricted downloadable raw dataset. The supplied PDF does not identify every ticker match, HFT-classification threshold, missing-fundamental rule, or treatment of negative P/E values. Those omissions prevent a byte-identical reconstruction from the article alone.

A disciplined implementation would first reproduce activity shares and sample counts, audit timestamp matching and spread accounting identities, and then construct fixed August 1 interactions with exact stock-specific treatment dates. It would estimate banned-only and matched 2SLS models with appropriate two-way clustered covariance, explicitly handle columns absorbed by fixed effects, and publish first-stage rank and strength diagnostics. Mechanism tests should use the separate pre-ban Nasdaq-only sample and disclose the ambiguous final markout horizon. These are concrete checks of the reported design rather than additional empirical findings.

The substantive finding is a conditional causal claim: the HFT activity suppressed by the 2008 ban appears to raise immediacy costs, with aggressive liquidity demand the clearest channel, while other short-selling activity appears beneficial. The unusual crisis window, residual trader classification, cross-venue measurement, functional-form dependence, and unresolved printed conventions limit how directly that result can be transported to another market or period.
