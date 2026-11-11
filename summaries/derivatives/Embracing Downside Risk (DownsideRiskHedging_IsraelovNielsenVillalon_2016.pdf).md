# Embracing Downside Risk

Roni Israelov, Lars N. Nielsen, and Daniel Villalon. *The Journal of Alternative Investments*, Winter 2017, pp. 59–67. The filename carries 2016, but the supplied publication is dated Winter 2017. Source: [DownsideRiskHedging_IsraelovNielsenVillalon_2016.pdf](../../Finance/DownsideRiskHedging_IsraelovNielsenVillalon_2016.pdf), ten PDF pages. All text, nine exhibits, endnotes, and references were inspected; table values and cumulative-return charts were checked visually.

## Why this matters

An investor can separate an asset's return into an insurance-selling component and a protected upside component by adding offsetting option positions. This paper asks which component earned the asset's historical reward. In its equity sample, the covered-call component earned 6.3% annualized arithmetic excess return and the long-call component 1.3%, summing to the index's 7.6%. The long call nevertheless supplied 41% of the index's beta exposure. The difference is attributed to the premium paid for optionality: the protected investor retains upside but transfers much of its expected reward to the insurer.

The authors explicitly describe their novelty as a reframing of the volatility risk premium, not a newly discovered independent premium. They use the same underlying and option data that can instead be organized into long-equity and equity-neutral short-volatility returns. Their decomposition makes the cost of downside protection visible in terms of the return an asset allocator forgoes. Similar comparisons for Treasuries, gold, crude oil, and investment-grade credit broaden the illustration, though their samples and implementation conventions differ.

The result is descriptive historical evidence about systematic option exposures. It is neither an arbitrage nor a claim that a downside hedge has no utility value. A protected payoff may be valuable to an investor facing binding liabilities or a nonlinear loss constraint even if it has a low sample mean. Conversely, a high average premium for selling insurance is not a sizing rule or a guarantee of survival through a crisis.

## Exact decomposition and capital accounting

Start with one unit of an underlying asset and add a long and a short position in the same call. The positions cancel. Group the underlying and short call as the insurer, and the remaining long call as the protected component. In value terms,

$$
S=(S-C)+C.
$$

At option expiry $T$, with strike $K$,

$$
S_T=\min(S_T,K)+(S_T-K)^+.
$$

The insurer retains the asset's downside but sacrifices gains above the strike. The call buyer's loss is limited to its premium, while its upside is uncapped. The paper also gives an equivalent decomposition into a short put and an asset plus protective put. Exact equivalence requires consistent cash, dividend, financing, exercise, and maturity conventions; the visual comparison uses a simplified example.

In Exhibit 1, the initial underlying and strike are both \$100 and the option premium is \$20. Ignoring financing and dividends, call PnL is $(S_T-100)^+-20$, and covered-call PnL is $S_T-100-[(S_T-100)^+-20]$. The insurer's PnL is capped at \$20, and the call's loss is capped at \$20. Their PnLs sum to the underlying's PnL at every terminal price. These are PnL contributions on a common underlying notional. Dividing the call's PnL by its own much smaller premium and then adding that percentage return to a covered-call return would destroy the identity.

For an explicit financed one-period reconstruction, let $B_t$ be the starting underlying notional, $C_t$ the option value, and $r_{f,t}$ the period cash return. Define the long-call contribution as

$$
r_{P,t}=\frac{C_{t+1}-C_t(1+r_{f,t})}{B_t},
$$

using settlement value at expiry. If $r_{S,t}^e$ is the total underlying excess return on the same notional, define $r_{I,t}=r_{S,t}^e-r_{P,t}$. This implements the additivity that the authors require. It is a transparent accounting reconstruction, not a fully disclosed pricing convention from their code. Their note does not give every cash, dividend, margin, or daily normalization convention. Those details matter especially when translating the attribution into independently funded investment products.

## Equity sample and trading mechanics

The equity sample runs from January 1986 through December 2014. The first decade is proxied with S&P 100 returns and options because those options were more liquid; later observations use the S&P 500. The source repeatedly describes the proxy span as 1986–1996, while endnote 2 refers to the S&P 100 “prior to 1996.” It does not resolve the precise handoff date. Reproduction should obtain the authors' series or state an explicit switch date, rather than hide this ambiguity.

S&P 500 option data are from OptionMetrics, and S&P 100 data from Commodity Systems Inc. The option selection is specified in endnote 2: each day, select the nearest-maturity monthly out-of-the-money call whose strike is nearest the current index level, buy it for the protected component and sell it for the covered-call component, and close the prior day's option position. Daily resetting keeps the exposures near the money. This is distinct from selling one option at month start and holding it passively to expiry.

The paper does not provide the quote timestamp, bid/ask or midpoint convention, stale-price and zero-bid filters, minimum maturity cutoff, expiry-day handling, strike tie-break, dividend treatment, interest-rate series, or missing-option rules for equities. It also does not specify all contract-style adjustments for the historical proxy. These omissions prevent a uniquely specified executable replication despite a clear high-level strategy.

The daily roll incurs significant option trading costs, which endnote 2 explicitly acknowledges. The headline decomposition is therefore not evidence that the displayed gross insurance premium is fully available net of execution. The authors suggest that a basket of one-month options held to expiry with dynamic equity hedging could approximate the same exposure with less option turnover. No exact basket weights, hedge schedule, transaction-cost estimate, or cost-adjusted equivalence test is supplied. That alternative should be treated as an implementation proposal rather than a reproduced result.

Arithmetic excess return is the annualized average daily excess return. Beta, volatility, correlation, and skewness use overlapping 21-day arithmetic returns. The paper does not state all annualization factors, variance conventions, or inference adjustments for overlapping observations. Its reported mean-return $t$ statistics can be transcribed, but their exact estimation cannot be reconstructed from the PDF alone.

## Equity results and an important Sharpe convention

Exhibit 2 reports:

| Quantity | Underlying index | Insurer: covered call | Protected: long call |
|---|---:|---:|---:|
| Arithmetic excess return | 7.6% | 6.3% | 1.3% |
| Geometric excess return | 6.3% | 6.0% | 1.0% |
| Annualized volatility | 15.7% | 9.7% | 7.0% |
| Printed Sharpe ratio | 0.40 | 0.62 | 0.15 |
| $t$ statistic of excess return | 2.6 | 3.6 | 1.0 |
| Beta to the underlying | 1.00 | 0.59 | 0.41 |
| Skewness | −0.9 | −2.2 | −0.1 |

The covered-call and long-call return correlation is 0.75. With rounded inputs, $9.7^2+7.0^2+2(0.75)(9.7)(7.0)$ produces approximately the reported index variance, providing a useful consistency check. Because the two return contributions add to the underlying, their regression betas also add to one. A beta contribution is not the same as the component's standalone variance divided by the index variance; the covariance with the other component matters.

The printed equity Sharpe row is numerically consistent with geometric excess return divided by volatility: $6.3/15.7\approx0.40$, $6.0/9.7\approx0.62$, and $1.0/7.0\approx0.14$ before rounding. In the prose, however, the authors use the conventional arithmetic ratio $7.6/15.7\approx0.48$ for long equity. A replicator must preserve this distinction rather than report the 0.40 and 0.48 figures as competing estimates from one convention. The paper itself cautions that asymmetric payoffs reduce the usefulness of Sharpe comparisons.

The covered call earns approximately 83% of the underlying's arithmetic mean, calculated as $6.3/7.6$, while carrying beta 0.59. Its lower volatility makes its compounded outcome close to the index's in Exhibit 3. That does not mean the cumulative insurer and protected wealth curves add to the index's compounded wealth curve: one-period return contributions are additive, but separately compounded wealth paths generally are not. The chart is an illustration of the long-run consequences of the two return streams, not a terminal payoff decomposition for a single option held throughout 1986–2014.

The long call earns a positive but small mean with $t=1.0$. Its slight negative reported skew does not contradict the convex terminal payoff of an individual call. The experiment repeatedly resets short-dated options and measures aggregated strategy returns; their realized distribution is not the same object as a single fixed-strike expiry payoff. Conversely, the covered call's skew of −2.2 indicates that the higher mean and conventional risk-adjusted performance come with a materially asymmetric loss profile.

## Attributing the premium transfer

The source attributes each component's equity premium using its beta times the underlying's sample excess mean:

$$
\mu_I=\beta_I\mu_S+\pi_V,\qquad
\mu_P=\beta_P\mu_S-\pi_V,\qquad
\beta_I+\beta_P=1.
$$

For equities, $0.59\times7.6\%=4.484\%$ and $0.41\times7.6\%=3.116\%$. Adding approximately 1.8 percentage points to the insurer and subtracting them from the protected component gives 6.3% and 1.3% after rounding. Thus, most of the call's beta-implied equity reward is transferred to the insurer through the option premium. This attribution is based on sample betas and sample average returns. It is not a structural proof that the residual is exclusively one priced risk under every model.

The traditional alternative decomposition in Exhibit 5 separates long equity from equity-neutral short volatility. It reports 7.6% mean and 15.7% volatility for long equity, versus 1.8% mean and 2.9% volatility for short volatility, yielding arithmetic Sharpe ratios around 0.48 and 0.62. The source does not supply a complete daily hedging algorithm for independently recreating that short-volatility series. Its role here is to show that the insurer/protected framing reorganizes a familiar economic premium.

Exhibit 4 compares implied and subsequently realized volatility. The reported volatility premium is positive 88% of the time and averages 3.4 annualized volatility percentage points. This is not a 3.4% option-strategy return. The exhibit's average is defined as

$$
\sqrt{\operatorname{mean}(\mathrm{VIX}_t^2)}
-\sqrt{\operatorname{mean}(RV_{t,t+1\mathrm{month}})},
$$

where realized variance is based on daily closing returns over the concurrent subsequent month. It is not simply the mean daily difference between VIX and realized standard deviation, nor the mean variance spread. The chart shows substantial negative realized-premium episodes around October 1987 and the 2008 crisis. The aggregate positive premium is therefore compensation earned while accepting losses in especially adverse states, rather than a stable carry receipt without tail exposure. The supplied note does not describe the complete historical volatility-index splice used for its earliest observations.

The economic explanation invokes investor preference for positive skew and downside protection, plus the unattractive obligations accepted by option writers. Demand can raise option prices relative to a benchmark without such a premium. The article cites demand-based pricing models but does not estimate a utility function, investor demand curve, or equilibrium supply elasticity. Its statement that absent a volatility premium the components would earn rewards proportional to beta is an explanatory benchmark, not a general theorem obtained from equality of implied and realized volatility alone in every stochastic-volatility or jump model.

## Other asset classes

The Treasury and commodity results use data from AQR, Bloomberg, and CME Group. Tables describe annualized arithmetic means and volatilities; beta and volatility are computed from overlapping 21-day returns. The paper does not reproduce a separate complete option selection and futures-roll protocol for each market. The equity endnote gives the most explicit daily selection rule, but extending it to each futures contract requires decisions about expiry matching, contract multiplier, roll date, and collateral return.

| Market and sample | Underlying mean / vol. | Insurer mean / vol. | Protected mean / vol. | Insurer / protected beta |
|---|---|---|---|---|
| 10-year Treasury, 1986–2014 | 4.1% / 6.4% | 2.5% / 3.4% | 1.6% / 3.3% | 0.50 / 0.50 |
| Gold, 1986–2014 | 2.1% / 15.4% | 2.1% / 7.9% | 0.0% / 8.5% | 0.48 / 0.52 |
| Crude oil, 1987–2014 | 9.9% / 32.2% | 5.8% / 17.1% | 4.1% / 16.6% | 0.51 / 0.49 |
| Investment-grade CDX, July 2007–June 2015 | 1.0% / 2.4% | 1.8% / 1.9% | −0.8% / 1.3% | 0.66 / 0.34 |

For Treasuries, both components receive about 2.05% beta-attributed bond premium before the transfer. Approximately 0.5 percentage points annually move from the protected to the insurer component. The resulting insurer share is about 62% of mean return despite about half of the beta contribution. The prose calls this half of bond variance; in an additive return decomposition, the corresponding covariance-based variance contribution agrees with beta times total variance, rather than with standalone component variance. Printed Sharpe ratios are 0.64, 0.77, and 0.47 for underlying, insurer, and protected exposure. Rounded means and volatilities do not reproduce every entry exactly.

For gold, the call receives 52% beta but earns 0.0% rounded excess return. Its approximately 1.1% beta-implied reward is offset by the premium transfer. The insurer earns the entire 2.1% rounded underlying mean. The Sharpe row is 0.13, 0.27, and 0.00. For crude oil, the protected component retains appreciable reward: approximately 4.9% beta-implied mean falls to 4.1% after an approximately 0.8-point transfer. The corresponding Sharpe row is 0.31, 0.34, and 0.25. Exhibit 8's first-column subheading mistakenly says “Gold,” but its title, beta row, discussion, and values identify the market as crude oil; the note follows those consistent identifiers.

These differences are informative. The asymmetry is not equally large in all assets. The authors suggest that equity losses represent worse economic states for many investors than bond losses because equity risk dominates typical portfolios. That interpretation is plausible within their framework, but the paper supplies no direct estimation of investor consumption exposure or marginal utility across the different asset classes.

## Credit uses a different experiment

The credit example is materially less comparable to the daily-marked equity, bond, and commodity exercises. It uses options on investment-grade CDX from July 2007 through June 2015. Earlier data are unavailable, and the endpoint is extended to maximize the short usable history. Prices before 2013 are considered less reliable, with discrepancies across sources; the authors select J.P. Morgan price data and cite Markit as another source in the exhibit.

Returns are measured between option maturity dates, not calendar month ends. They use entry prices and terminal expiry values rather than daily marks. Rebalancing is monthly, and positions are not delta hedged between rebalances. If a new at-the-money option is unavailable after an expiry, the strategy holds nothing until one becomes available. Beta and volatility use these monthly returns, and the excess mean is annualized from monthly observations. Exact idle-period cash conventions and all CDX pricing details remain unspecified.

The protected credit component has a negative sample mean of −0.8%, whereas the insurer earns 1.8% and the underlying 1.0%. Printed Sharpe ratios are −0.59, 0.95, and 0.42 respectively. Using the rounded beta and mean data, the transfer is about $1.8\%-0.66(1.0\%)=1.14$ percentage points a year, matching $0.34(1.0\%)-(-0.8\%)$. That calculation is a derived attribution check, not an additional precision estimate from the authors.

The exceptionally large asymmetry may reflect 2008–2009, which occupies a substantial portion of this short series. Expiry-only measurement also omits interim mark-to-market drawdowns and margin pressures that can dominate the experience of an insurance seller. No confidence intervals or robust hypothesis tests accompany these cross-asset tables. The evidence supports a common qualitative pattern but does not establish statistically equal premia or rank their population magnitudes precisely.

## Reimplementation and limits of the allocation conclusion

A useful replication must first construct additive daily PnL contributions on common underlying notionals, preserving every option selection and financing decision. It should verify that insurer plus protected contribution equals the underlying excess return at each observation before computing sample means. It should then calculate the documented overlapping-return statistics, maintain separate arithmetic and geometric conventions, and reproduce the beta-times-mean attribution. Credit requires its own maturity-to-maturity calendar rather than being forced into the daily procedure.

To assess an investable strategy, a further layer must include executable bid/ask prices, turnover, futures rolls, margin, collateral rates, contract liquidity, gap losses, and funding capacity. The source acknowledges significant daily option costs but does not provide these inputs or net results. A cost-aware replication should report them as new work. Its performance would not be a direct transcription of the exhibits.

The authors conclude that reducing an asset allocation may often be preferable to repeatedly purchasing options when downside exposure is too large. This comparison is natural under an average-return/volatility objective: linear de-risking avoids paying an option premium. It is not universal under objectives that value an explicit payoff floor, convexity during sudden crashes, or protection of a liability threshold. A smaller linear position and a protected nonlinear position have different state-contingent payoffs even when their volatility is matched.

The source also favors capturing insurance premia for investors able to bear the adverse states, while explicitly leaving risk sizing to another article. The reproducible finding is the historical division of gross reward and beta across option-based components. The broader research implication is to evaluate protection in units of premium paid, reward surrendered, and crisis payoff delivered, and to evaluate insurance selling in units of tail loss and funding demand as well as conventional Sharpe ratio.
