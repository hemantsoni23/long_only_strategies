# Carry

Ralph S. J. Koijen, Tobias J. Moskowitz, Lasse Heje Pedersen, and Evert B. Vrugt. *Journal of Financial Economics* 127 (2018), 197–225. DOI: 10.1016/j.jfineco.2017.11.002. The source is the published article, including Appendices A–D, rather than an earlier working paper.

Source: [Carry_KoijenMoskowitzPedersenVrugt_2018.pdf](../../Finance/Carry_KoijenMoskowitzPedersenVrugt_2018.pdf). Page references below are printed journal pages; subtract 196 to obtain the PDF page number. All 29 PDF pages were inspected. Equations, the principal portfolio and panel-regression tables, the drawdown figure, and the currency cleaning procedure were also checked visually.

## Why this matters

The paper turns carry from a currency-specific interest-rate strategy into a common measurement framework for assets with very different cash flows and maturities. Carry is the excess return on a position if the relevant spot-price curve remains unchanged during the holding period. It can therefore be measured before trading without fitting a model of expected appreciation. An investor can then ask whether prices offset, leave intact, or amplify that observable component of return.

This separation matters for replication and economic interpretation. A high dividend yield, an upward-sloping yield curve, commodity backwardation, and an option's time decay can all enter a carry calculation, but their units and financing assumptions must agree with the returns subsequently measured. Ranking a ten-year bond's unscaled carry against a one-year bond's unscaled carry confounds the signal with duration. Treating an option's current price as its unchanged future price ignores expiry. The paper's central methodological contribution is to handle these cases within one payoff-based definition.

Its empirical contribution is a broad comparison across nine strategies: global equity indices, global bond levels, global yield-curve slopes, US Treasury maturities, commodities, currencies, US credit, calls, and puts. Carry-ranked portfolios generally earn positive premia; their aggregate has an annualized Sharpe ratio of 1.20 before trading costs. The evidence does not identify a single structural explanation. Downside, liquidity, volatility, and recession exposure account for parts of the returns, while the strongest option results are particularly sensitive to trading costs. The useful research object is the combination of precise measurement, heterogeneous predictive slopes, and common bad-state losses—not a claim that carry is riskless income.

## The return identity and capital convention

At date $t$, let $S_t$ be a spot price and $F_t$ the price of a futures contract delivering the asset at $t+1$. Let $X_t$ be capital allocated per contract, with contract multipliers incorporated consistently, and let $r_t^f$ be its financing-period risk-free rate. Assuming the collateral earns that rate, the futures position has total return $r_t^f+(F_{t+1}-F_t)/X_t$. Its excess return is

$$
r_{t+1}=\frac{F_{t+1}-F_t}{X_t}.
$$

At expiration $F_{t+1}=S_{t+1}$. Carry and the return decomposition are therefore

$$
C_t=\frac{S_t-F_t}{X_t},\qquad
r_{t+1}=C_t+\frac{S_{t+1}-S_t}{X_t}
=C_t+E_t\!\left[\frac{S_{t+1}-S_t}{X_t}\right]+u_{t+1},
$$

where $u_{t+1}=(S_{t+1}-E_tS_{t+1})/X_t$ has conditional mean zero. These are accounting statements, not a model that makes carry equal expected return. Carry is known at formation; expected appreciation is not. The paper usually takes $X_t=F_t$, a fully collateralized position, giving $C_t=S_t/F_t-1$. Doubling leverage doubles both carry and excess return. A prediction coefficient can only be interpreted economically when the predictor and dependent variable use the same capital convention. See equations (2)–(6), pp. 200–201.

The simple identity assumes delivery one period ahead. In the actual data, available futures expiries often differ from one month. The authors interpolate prices to build one-month carry signals but calculate realized returns from actual traded contracts or independently constructed bond returns. A replication must preserve that distinction: returns from a mechanically interpolated contract are not necessarily implementable trading returns.

For a futures contract quoted in foreign currency, let $e_t$ denote US dollars per foreign-currency unit. Appendix C hedges the foreign-exchange exposure of margin capital, not the uncertain futures profit itself. With $X_t=e_tF_t$, dollar excess return is

$$
r_{t+1}^{USD}=\frac{e_{t+1}(F_{t+1}-F_t)}{e_tF_t}
=\frac{F_{t+1}-F_t}{F_t}
+\frac{e_{t+1}-e_t}{e_t}\frac{F_{t+1}-F_t}{F_t}.
$$

Carry assumes both underlying and exchange-rate spot prices stay fixed, so it remains $(S_t-F_t)/F_t$. The exchange-rate interaction is second order, but the authors retain it. For unhedged collateral, carry adds the foreign-minus-US short-rate term when the exchange rate stays unchanged. Actual unhedged excess return instead adds $(e_{t+1}/e_t)(1+r_t^{f*})-(1+r_t^f)$ to the futures profit, retaining first-order exchange-rate exposure. Thus the global tests do not simply combine unhedged cash index returns.

## Translating the definition across assets

### Currencies, equities, and commodities

With spot quoted as domestic currency per foreign unit, covered interest parity implies $F_t=S_t(1+r_t^f)/(1+r_t^{f*})$. Thus currency carry is

$$
C_t=\frac{r_t^{f*}-r_t^f}{1+r_t^f}.
$$

The familiar rate differential is a close approximation, but the measured forward discount remains the definition even if covered parity fails. It is therefore preferable to compute from actual spot and forward quotes rather than substituting policy rates.

For an equity index, the one-period futures relation is $F_t=S_t(1+r_t^f)-E_t^Q D_{t+1}$, where $D$ is the dividend cash flow and $Q$ denotes risk-neutral valuation. Carry is

$$
C_t=\left(\frac{E_t^QD_{t+1}}{S_t}-r_t^f\right)\frac{S_t}{F_t}.
$$

This is a forward-looking dividend yield net of financing, not the trailing dividend-price ratio. It changes with local short rates and the upcoming dividend calendar. Equity carry can therefore select different countries in different dividend seasons even when trailing yields are stable. The carry investor holds futures and does not separately collect cash dividends; expected dividends are already reflected in the futures basis.

For commodities, write the convenience yield net of storage cost as $\delta_t$. With $F_t=S_t(1+r_t^f-\delta_t)$, carry is $(\delta_t-r_t^f)/(1+r_t^f-\delta_t)$. This is the basis trade in the paper's empirical universe. Since commodity spot quotes are often unsuitable, carry uses a synthetic spot price extrapolated from the futures curve. The claim of model-free measurement means no expected-return model is estimated; it does not eliminate the operational dependence on curve interpolation and reliable contemporaneous quotes.

### Bonds and maturity-sensitive prices

A security with $\tau$ periods remaining at formation has $\tau-1$ periods left next month. The unchanged object is the price as a function of remaining maturity, not the price of the same calendar-date claim. Let $S_t^\tau$ denote the maturity-$\tau$ spot price and $F_t^\tau$ its one-period futures price. Then

$$
C_t^\tau=\frac{S_t^{\tau-1}}{F_t^\tau}-1.
$$

Holding a bond's price literally constant as it matures would miss its drift toward redemption. For zero-coupon yields $y_t^\tau$ expressed in units consistent with the period count,

$$
S_t^\tau=(1+y_t^\tau)^{-\tau},\qquad
C_t^\tau=
\frac{(1+y_t^\tau)^\tau}
{(1+r_t^f)(1+y_t^{\tau-1})^{\tau-1}}-1.
$$

The exact curve formula, equation (11), is the empirical calculation. Its approximate interpretation is yield minus the short rate plus roll-down:

$$
C_t^\tau\simeq y_t^\tau-r_t^f
-D_t^{mod}(y_t^{\tau-1}-y_t^\tau).
$$

Annual yield quotes and a one-month holding period require consistent conversion; the approximate expression above is written in the paper's one-period notation. One should not insert an annual yield spread as a monthly return.

There is a small printed algebra inconsistency on p. 203. The text defines the forward rate as the gross accumulation ratio $(1+y_t^\tau)^\tau/(1+y_t^{\tau-1})^{\tau-1}$, but equation (12) uses it as a net rate. Defining $1+f_t^{\tau-1,\tau}$ equal to that ratio makes the stated result $C=(f-r^f)/(1+r^f)$ correct. Equation (11) is internally consistent and avoids the ambiguity.

For US Treasury maturities, capital is proportional to $F_t^\tau D_t^\tau$. Both carry and realized excess return are divided by duration. The same adjustment is applied to credit portfolios. The global slope test asset in each country is a long ten-year bond and short two-year bond, each duration scaled. Its carry is the difference between their scaled carries. A long-short carry trade across these slope positions is distinct from buying the steepest country's unhedged ten-year bond.

### Options

Let $G^j(\tau,K;S_t,\sigma_{t,\tau})$ be a call or put price for strike $K$, maturity $\tau$, spot $S_t$, and maturity-specific implied volatility. Its synthetic futures price is $(1+r_t^f)G^j(\tau,K;S_t,\sigma_{t,\tau})$. Holding the spot and implied-volatility curve fixed gives

$$
C_t^j(\tau,K)=
\frac{G^j(\tau-1,K;S_t,\sigma_{t,\tau-1})}
{(1+r_t^f)G^j(\tau,K;S_t,\sigma_{t,\tau})}-1.
$$

Time decay and movement along the implied-volatility term structure both enter. The paper's approximation uses $\theta=\partial G/\partial\tau$, a derivative with respect to remaining maturity, so its time passage term is $-\theta$. That convention differs from a vendor's calendar-time theta. With vega $\nu$, approximate carry is $[-\theta+\nu(\sigma_{\tau-1}-\sigma_\tau)]/G-r^f$, with theta rescaled to the holding period. The authors use the exact price ratio, not this approximation, in the tests. The article does not fully specify the interpolation of the option surface needed to obtain the shorter-maturity, same-strike price. This is a material replication input, especially near expiry and away from actively quoted strikes.

## Data and construction decisions

The observation frequency is monthly. Table 1 gives instrument-specific starts; it is an unbalanced panel, not a universe available in its entirety at the earliest date. Most asset-class samples end in September 2012; index options end in December 2011.

Global equities include 13 index futures: the US, Canada, UK, France, Germany, Spain, Italy, Netherlands, Sweden, Switzerland, Japan, Hong Kong, and Australia. Earliest return availability is March 1988, while Italy starts April 2004 and Sweden March 2005. Bloomberg supplies spot and the nearest two contracts. The active front-month futures contract supplies daily returns, rolled three days before expiration, which are then aggregated to monthly returns. Only carry uses the synthetic one-month curve. Appendix D reports robustness to dropping each month's first trading day, addressing nonsynchronous settlement, and excluding the DAX, whose underlying is a total-return index. Both checks preserve the qualitative results.

The currency panel begins in November 1983 for the earliest returns. It includes legacy European currencies and subsequently the euro, plus Australia, Canada, Denmark, Japan, New Zealand, Norway, Sweden, Switzerland, and the UK. The US is included as a zero-carry, zero-excess-return reference asset. Table 1 provides the actual roster and start dates; the prose uses differing country counts, so those counts should not replace an instrument-level eligibility table. Spot and one-month forward data use Barclays Bank International before January 1997 and WMR/Reuters thereafter. Some legacy observations begin only in February 1997; euro returns begin February 1999. There are ten exchange-rate pairs after euro introduction.

Appendix D supplies a consequential currency cleaning algorithm. Infer the foreign interest rate from spot, forward, and US one-month LIBOR, then compare it with Bloomberg or Global Financial Data IBOR. A discrepancy greater than 2 percentage points triggers investigation. Consult the alternate BBI/WMR source first, HSBC next, and Thomson Reuters next, accepting a replacement that passes the comparison rather than automatically overwriting genuine extremes. If both default and alternate quotes fail, retain the default under the stated branch. When alternative vendors are absent, inspect quotes one day before and after month end; without an IBOR history, require agreement with another implied-rate source within tolerance. In residual cases where adjacent-day quotes agree but month-end does not, use the prior-day quote. Figure D1 shows that this removes an October 1993 Swedish error while retaining the 1992 banking-crisis extreme. The use of next-day validation is a historical data-cleaning step, not strictly information available at the original month-end execution time.

Commodities comprise 24 futures, with earliest returns in February 1980: six energy products, eight agricultural products, three livestock products, and seven metals. The categories include Brent, gasoil, WTI, gasoline, heating oil, natural gas; cotton, coffee, cocoa, sugar, soybeans, Kansas wheat, corn, wheat; lean hogs, feeder cattle, live cattle; and gold, silver, aluminum, nickel, lead, zinc, copper. Appendix D uses the nearest three Bloomberg contracts for curve construction and linear interpolation to a one-month maturity. For LME industrial metals, it uses cash and constant three-month quotes. Realized returns are GSCI excess-return indices, rolled during the fifth through ninth business days of the month. The collateral interest component is excluded.

Global government bonds cover ten countries: US, Australia, Canada, Germany, UK, Japan, New Zealand, Norway, Sweden, and Switzerland. Earliest availability is November 1983. The zero-coupon curves come from Jonathan Wright's data through May 2009, then Bloomberg from June 2009. Each month the ten-year bond is purchased synthetically and next month's nine-year-eleven-month price is interpolated. The same country curves generate duration-scaled ten-year-minus-two-year positions. Where liquid actual bond futures exist, reported correlations with synthetic futures returns exceed 0.95. This is a validation of the proxy, not proof that all synthetic portfolios trade at observed curve prices without cost.

The US Treasury test uses six CRSP maturity buckets, 1–12, 13–24, 25–36, 37–48, 49–60, and 61–120 months, from August 1971 onward. Gurkaynak–Sack–Wright yields provide carry calculations. Table 1 labels representative maturities of one, two, three, five, seven, and ten years; exact mapping of every bucket's duration and yield interpolation requires additional implementation choices. Credit uses eight Barclays corporate indices: intermediate and long maturity crossed with AAA, AA, A, and BAA. Their approximate durations are five and ten years; average maturity and yield are available. The historical data period begins January 1973, with Table 1 returns beginning February 1973.

For calls and puts, use OptionMetrics index options, January 1996–December 2011. The source's selection list includes DJX, NDX, MNX, XMI, SPX, OEX, MID, SML, RUT, and WSX; Table 1 reports nine surviving index groups and does not separately report WSX. Preserve the distinction between the requested universe and observed surviving observations. On the last trading day of each month, select standard-expiry options with 30–60 days remaining. Use two delta groups per index: calls $[0.2,0.4)$ and $[0.4,0.6)$, puts $[-0.4,-0.2)$ and $[-0.6,-0.4)$. Within a group choose highest volume, then highest open interest, then highest price if ties remain. Exclude cases where volume or open interest is zero for contracts required to compute carry. Hold for one month. Calls and puts are separate cross sections; their cash-price returns retain embedded leverage and should not be compared with duration-scaled bonds by raw percentage mean alone.

## Trading rules, timing, and aggregate exposure

At the end of month $t$, rank available instruments within a class by carry. For $N_t$ assets, define

$$
w_{i,t}=z_t\left[\operatorname{rank}(C_{i,t})-\frac{N_t+1}{2}\right],
\qquad
r_{t+1}^{carry}=\sum_iw_{i,t}r_{i,t+1}.
$$

Choose $z_t$ so positive weights sum to one and negative weights sum to minus one. Thus gross exposure is two in the already defined return units, and net exposure is zero. All instruments enter; ranks limit sensitivity to signal outliers. Midranks provide a natural treatment of ties, but a tie convention is not explicitly documented. Carry of the portfolio is $\sum_iw_{i,t}C_{i,t}$ and is nonnegative, strictly positive with genuine cross-sectional dispersion. This property does not force realized return to be positive.

Carry1m uses the latest month-end signal. Carry1–12 averages the most recent twelve signals, including the current one; it smooths dividend and commodity seasonality. Carry2–13 shifts that window back one additional month, separating signal inputs from return-window prices. Securities need sufficient history for these variants; the exact startup treatment with fewer than twelve observations is not fully specified. Monthly rebalancing is common to the portfolio tests.

A separate timing rule buys or shorts each asset according to whether carry exceeds a threshold:

$$
w_{i,t}=z_t[2\mathbf1\{C_{i,t}>\bar C_t\}-1].
$$

Normalize total absolute exposure to two. Thresholds are either zero or the historical average carry across the asset class available up to that point. The rule may be net long or short. It is therefore not the same test as a cross-sectional rank portfolio. The expanding historical mean is implementable using past observations, though precise startup and missing-observation averaging conventions are not supplied.

The global carry factor first scales each asset-class strategy to 10% annual volatility using its full-sample standard deviation, then averages the scaled returns. This prevents option price returns from dominating bonds. It uses future observations in volatility normalization and is consequently a descriptive historical combination, not a completely out-of-sample sizing rule. Equal stand-alone volatilities also do not imply equal marginal contributions to portfolio risk when correlations differ. A live reconstruction should report the original full-sample result separately from a lagged-volatility version with an explicitly chosen estimation window; the latter is an extension, not the published specification.

## Portfolio evidence and explanatory regressions

Table 2 reports the following annualized percentage means and volatilities. The mean is arithmetic; it is not a compound growth forecast.

| Carry1m strategy | Mean % | Volatility % | Sharpe ratio |
|---|---:|---:|---:|
| Global equity indices | 9.58 | 10.48 | 0.91 |
| Global ten-year bond levels | 3.85 | 7.45 | 0.52 |
| Global ten-year-minus-two-year slopes | 0.68 | 0.66 | 1.03 |
| US Treasury maturities | 0.46 | 0.67 | 0.68 |
| Commodities | 11.22 | 18.78 | 0.60 |
| Currencies | 5.29 | 7.80 | 0.68 |
| Credit | 0.24 | 0.52 | 0.47 |
| Calls | 63.55 | 171.51 | 0.37 |
| Puts | 178.90 | 99.30 | 1.80 |
| Global carry factor | 7.18 | 5.96 | 1.20 |

The raw option percentages reflect the denominator of an option-price investment, not return on a fully specified dealer margin account. The duration-scaled bond percentages have the opposite denominator effect. The aggregate equal-volatility passive benchmark has mean 2.80%, volatility 6.99%, and Sharpe 0.40. Global carry's monthly skewness is −0.03, but its reported excess kurtosis is 5.40. Near-zero skewness therefore does not imply Gaussian tails or absence of severe losses.

The evidence is heterogeneous. Equity carry beats the comparable historical dividend-yield strategy's Sharpe 0.36; commodity carry equals the basis strategy by construction. Global bond-level carry's Sharpe 0.52 is below the passive bond benchmark's 0.74. The source prose overgeneralizes when discussing near-universal superiority; the table is the correct quantitative reference. For carry1–12 the global Sharpe is 1.12, with equity 0.58, Treasury 0.78, commodity 0.65, and put 1.52. Appendix B's one-month-skipped version gives global 1.10, equity 0.44, commodity 0.58, and put 1.39. The aggregate result survives skipping a month, but the equity decline is economically meaningful.

Regional aggregation is another robustness test: equities, bonds, and currencies are collapsed to North America, UK, continental Europe, Asia, and New Zealand/Australia before ranking. Commodities are collapsed to agriculture/livestock, metals, and energy. The coarser portfolios retain positive Sharpe ratios, including 0.54 for equities and 0.44 for currencies. This suggests the effect is not exclusively very fine within-region selection.

Spanning tests regress carry portfolio returns on portfolios constructed from familiar predictors using the same rank methodology, then reverse the regression. Equity carry has monthly alpha 0.77% with $t=4.36$ against trailing dividend yield; their return correlation is only 9.0%. Bond-level carry is highly correlated with the yield-spread strategy, 94.4%, and has only 0.05% monthly alpha with $t=1.22$. Carry is not independently significant in every such comparison. Credit carry has monthly alpha 0.02%, $t=2.96$, while put carry has 14.29%, $t=6.84$, in its original leveraged units against short volatility. In reverse regressions the familiar predictors' intercepts are insignificant. Failure to reject an intercept is evidence compatible with spanning, not a proof of exact population spanning.

Table 8 adds passive class returns, value, cross-sectional momentum, and time-series momentum. Class-specific value/momentum factors are used for equities, bonds, commodities, and currencies; bond factors proxy for slope and Treasuries. Credit and options use global diversified factors from the referenced studies. The global carry factor retains monthly alpha 0.51% with $t=6.74$. Equity alpha remains 0.82% with $t=4.71$; commodity alpha falls to 0.64% with $t=2.57$. Credit's full-model alpha has $t=1.70$, so a statement that every expanded-model alpha is conventionally significant would be too strong. Exact source factor files and generic inference settings for all these time-series regressions are not reproduced in the article.

## Does price appreciation reinforce or offset carry?

For each asset class the panel model is

$$
r_{i,t+1}=a_i+b_t+cC_{i,t}+\epsilon_{i,t+1}.
$$

Estimate versions with neither fixed effect, only asset effects, only time effects, and both. Standard errors are clustered by time. Asset effects remove persistent differences in instrument means; time effects remove common month-specific returns. A zero coefficient is consistent with expected appreciation cancelling carry. A coefficient of one means appreciation itself is unpredictable by carry in the regression. Values between zero and one indicate partial offset; values above one imply reinforcement. These are statements about conditional linear projections, not universal nonlinear relationships.

With both fixed effects, Table 4 reports:

| Class | $c$ | $t$ against zero |
|---|---:|---:|
| Equities | 1.22 | 4.18 |
| Global bond levels | 1.44 | 3.08 |
| Global bond slopes | 0.81 | 4.91 |
| Treasuries | 0.45 | 2.65 |
| Commodities | 0.01 | 0.13 |
| Currencies | 1.09 | 2.69 |
| Credit | 1.46 | 2.01 |
| Calls | 0.16 | 0.77 |
| Puts | 0.60 | 4.16 |

The printed discussion says bond slopes exceed one, but every bond-slope estimate in Table 4 is below one; 0.81 is the both-effects estimate. This note follows the table. Commodities and calls fail to reject zero despite profitable rank portfolios in Table 2. Rank weighting, passive cross-sectional differences, nonlinearities, and commodity seasonality make those distinct tests. Moreover, the listed $t$ statistics test zero, not one; a coefficient of 1.44 does not by itself establish statistically significant amplification of carry.

Timing against the expanding historical mean produces Sharpe ratios 0.75 for equities, 0.69 for bond levels, 0.75 for commodities, 0.53 for currencies, and 0.96 for puts. Calls are the exception at −0.14. The global timing factor's Sharpe is 0.94, versus 0.93 when comparing carry with zero. Zero-threshold rules can approximate passive long or short positions where carry rarely changes sign. The historical-mean comparison is therefore a more discriminating timing test, although the aggregate volatility scaling remains retrospective.

## Turnover and transaction costs

Equation (25) defines monthly turnover as

$$
TO_t=\frac14\sum_i\left|w_{i,t-1}(1+r_{i,t})-w_{i,t}\right|.
$$

The divisor accounts for two-sided trading and the strategy's gross exposure of two. Reported annual turnover is twelve times the monthly average. Reproduce this definition rather than replacing it with a cash-account turnover convention; futures and duration-scaled returns make capital accounting especially important.

Carry1m annual turnover is 6.2 for equities, 3.6 for commodities, 1.1 for currencies, and 6.4 for puts. Averaging twelve signals reduces these to 1.4, 1.1, 0.5, and 5.6 respectively. Smoothing does little to eliminate the need to replace short-dated options. Costs for non-credit, non-option assets come from Bollerslev and coauthors' cited estimates; the paper tests one, two, and five multiples of the half-spread. The complete instrument-level spread inputs are not supplied here. Credit has no net-cost estimates.

At one half-spread, equity carry's Sharpe falls from 0.91 to 0.90, bond levels from 0.52 to 0.51, slope carry from 1.03 to 0.93, Treasuries from 0.68 to 0.63, commodities from 0.60 to 0.58, and currencies from 0.68 to 0.67. At five half-spreads they remain 0.82, 0.49, 0.55, 0.39, 0.53, and 0.63 respectively. These estimates support cost resilience for the liquid non-option strategies at the assumed size and spreads; they do not model unlimited capacity.

OptionMetrics closing bid-ask spreads sharply change the option conclusion. At one half-spread, call carry's Sharpe becomes −0.77 and put carry's falls from 1.80 to 0.42. At two half-spreads, put carry becomes −0.67. Smoothed put carry is 0.20 after one half-spread and −0.82 after two. The authors argue closing quotes are conservative because option trading continues after the equity close and spreads widen. That possible bias does not justify presenting gross option Sharpe ratios as demonstrated realizable profits. Margin, funding, exercise, assignment, and scalable execution costs require separate modeling.

## Risk explanations, source qualifications, and reproducibility limits

The 36 cross-strategy monthly correlations are mostly small; 24 are positive and ten significantly positive at 5%. Small unconditional correlations coexist with shared prolonged drawdowns. Appendix A defines drawdown using cumulative sums of excess returns, not compounded wealth:

$$
D_t=\sum_{s=1}^{t}r_s-\max_{u\le t}\sum_{s=1}^{u}r_s.
$$

The largest episodes identified are August 1972–September 1975, March 1980–June 1982, and August 2008–February 2009. The early sample contains fewer available strategies, so it cannot establish that the later option and global-equity strategies experienced the same 1970s shocks. The figure associates losses with a GDP-weighted regional recession indicator. Its caption also normalizes inverse-volatility weights to sum to one, whereas Section 3.4 scales each strategy to 10% then averages. Those are different overall scaling conventions; avoid equating the figure's drawdown magnitude mechanically with Table 2's aggregate capital base. The appendix's claim that the recession indicator is lower during drawdowns is also at odds with its description of recession peaks; the dates and plotted association are safer evidence than that sentence.

Downside exposure is tested two ways. Henriksson–Merton regressions use the local passive benchmark and add $\max(0,-r_{m,t})$. A positive coefficient on that term is a payoff that rises when markets fall, so signs must be interpreted using the actual regressor. The second approach estimates a full-sample CRSP-market beta and a conditional beta in low-market-return states, then prices them in Fama–MacBeth regressions. The main text defines the low state as $r_m<\mu-\sigma$, while Table 10's caption says one standard deviation below zero. This unresolved threshold difference matters for exact replication. The caption's broad 10%-volatility statement also does not clearly reconcile with Panel A's very large raw option intercepts; avoid mixing those intercept units with Panel B's normalized alphas.

The conditional downside model estimates a positive downside-risk price, 0.017 with $t=4.89$, but a negative market-risk price, −0.019 with $t=-2.65$. It explains some bond, commodity, and option means while leaving significant equity, slope, Treasury, currency, and credit alphas. The result is mixed evidence for the mechanism, not a uniform rejection of every risk-based model.

Liquidity shocks are the first principal component of the market and funding liquidity variables from Asness and coauthors, available January 1987–July 2011. Volatility risk is measured with changes in VXO, whose history starts January 1986. Table 11 scales strategy returns to 10% annual volatility and multiplies reported exposures by 100. Currency carry loads positively on liquidity shocks, 2.19 with $t=3.01$, and negatively on VXO changes, −0.15 with $t=-4.46$. Treasury carry instead has positive volatility loading 0.10 with $t=2.37$. That sign reversal is an important obstacle to a single undifferentiated liquidity/volatility explanation.

Fama–MacBeth estimated risk prices are 0.16 for liquidity, $t=3.53$, and −2.28 for volatility, $t=-2.65$. Significant residual alphas remain: equities 0.71% monthly, slope 0.61%, Treasuries 0.94%, and puts 0.70%. Credit's residual is significantly negative, −0.31%, not a positive unexplained premium. These prices and alphas are conditional on measured proxies, factor scaling, the sample, and the chosen small set of test portfolios. They do not identify household marginal utility or prove an arbitrage.

A reproducible implementation should retain an instrument/date ledger, raw and cleaned quotes, exact expiry and roll calendars, capital denominators, point-in-time signals, contract eligibility, and both gross and net portfolio series. Reconcile the exact Table 1 starts and the published definitions before fitting risk explanations. The article gives much of the required structure but leaves some essentials to cited datasets: option-surface construction, credit and Treasury interpolation details, all transaction-cost inputs, some standard-error conventions, and full liquidity-factor construction. Report these as missing inputs rather than silently adopting contemporary vendor defaults. Separate corrections to printed inconsistencies from extensions such as prospective risk scaling, alternative cost models, or additional post-2012 data.

The evidence supports carry as a broadly useful ex-ante characteristic whose economic meaning depends on maturity, financing, and position size. It also supplies a demanding set of replication targets: profitability across several liquid markets, weak incremental evidence in certain classes, costly options implementation, and common recession losses despite modest monthly correlations. An explanation that fits only the currency carry trade has not yet explained those joint facts.
