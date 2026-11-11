# Anomalies and Market Efficiency
**Authors:** G. William Schwert
**Year:** 2003
**Journal/Venue:** Handbook of the Economics of Finance (Constantinides, Harris, Stulz eds.), Ch. 15
**Source file:** Finance/AbnormalReturnsReview_Schwert_2003.pdf

## Thesis

An anomaly is only defined relative to a model of normal returns (Fama 1970: every efficiency test is a joint test), and it is only economically meaningful if an efficient trader could profit from it net of costs (Jensen 1978). Schwert's contribution is a set of out-of-sample replications: he re-estimates the headline regressions of famous anomaly papers on data before and after the original sample, and finds that most attenuate or vanish after publication. Two readings are left open and not separated: (i) the original result was a selection/data-snooping artifact (Lo-MacKinlay 1990), or (ii) practitioners traded it away. The one clear exception is momentum.

## Replications (all t-stats heteroskedasticity-consistent)

**Size (Table 1).** Jensen's alpha of the DFA US 9-10 Small Company fund (launched 1981, mimics Banz 1981) vs. CRSP VW:
$$R_{it}-R_{ft}=a_i+b_i(R_{mt}-R_{ft})+e_{it}.$$
1982-2002: $a=0.20\%$/mo ($t=0.67$), $b=1.03$; subperiods 1982-87 $-0.19\%$ ($t=-0.44$), 1988-93 $0.38\%$ ($0.80$), 1994-2002 $0.35\%$ ($0.66$). No reliable small-cap alpha after publication, though alternatively the small-cap premium was simply smaller post-1982.

**Turn of the year (Table 2).** Daily $R_{1t}-R_{10t}$ (CRSP NYSE decile 1 minus decile 10) on a dummy for the first 15 calendar days of January:
| Period | $a_J$ (daily) | t |
|---|---|---|
| 1962-1979 (Reinganum sample) | 0.815% | 7.14 |
| 1980-1989 | 0.433% | 4.55 |
| 1990-2001 | 0.565% | 5.37 |
Roughly halved but still reliably positive -- this is the one calendar effect that survives in CRSP data. Yet Booth and Keim (2000) find no January effect in the DFA 9-10 fund (1982-1995): its screens (price >= \$2, cap >= \$10m, IPO age >= 1 yr) remove the stocks that generate it. The effect lives in the lowest-priced, least liquid names, i.e. it is likely a microstructure/illiquidity phenomenon, not an implementable one. Roll's (1983) tax-loss selling is the candidate mechanism.

**Weekend (Table 3).** $R_t=a_0+a_W\,\text{Weekend}_t+e_t$, Dow Jones indices 1885-1927, S&P composite thereafter:
| Period | $a_W$ | t |
|---|---|---|
| 1885-1927 | -0.13% | -4.96 |
| 1928-1952 | -0.30% | -6.45 |
| 1953-1977 (French 1980) | -0.23% | -8.86 |
| 1978-2002 | -0.05% | -1.37 |
Strong in pre-sample data (so not pure snooping), gone after 1978; weekend mean $a_0+a_W\approx 0$. Schwert knows of no practitioner who traded it, so the "arbitraged away" story is harder to invoke here.

**Value.** Ball (1978): a stable, cheaply observable characteristic earning "abnormal" returns more likely signals a misspecified CAPM than inefficiency, since it would be trivially arbitrageable. Fama-French (1993, 1996) three-factor intercepts
$$R_{it}-R_{ft}=a_i+b_i(R_{mt}-R_{ft})+s_i\,SMB_t+h_i\,HML_t+e_{it}$$
are insignificant for size, B/M, D/P, E/P, C/P and sales-growth sorts (exception: small low-B/M growth stocks, negative intercept). Out-of-sample support predates publication: Davis-Fama-French (2000) find a similar value premium 1929-1963 (where size is subsumed by value) and reject Daniel-Titman's characteristics-over-covariances result outside its sample; Fama-French (1998) find it in 13 countries 1975-1995. But post-publication, the DFA US 6-10 Value fund (from 1994), which would have had CAPM alpha of about 0.5%/mo over 1963-1991, earns $a=-0.22\%$/mo ($t=-0.59$), $b=0.82$, 1994-2002. So value, like size, did not deliver to the vehicle built to harvest it.

**Momentum (Table 4).** UMD (returns over months -2 to -13), CAPM and FF3 alphas for 1927-1964, 1965-1989 (Jegadeesh-Titman sample), 1990-2001, and 1927-2001: CAPM alpha about 1%/mo with t between 2.7 and 7.0; the smallest estimate is in the JT sample and the largest in the post-publication period; FF3 alphas are larger than CAPM alphas and all reliably positive. DeBondt-Thaler long-term reversal, by contrast, is absorbed by FF3 (losers resemble small distressed firms). Lewellen (2002) finds momentum in size/B/M portfolios, which argues against firm-level behavioral stories. Schwert's verdict: persistent, possibly "predictable variation in risk premiums not yet understood."

**Short rates / inflation (Table 5).** $R_{mt}=a+gX_t+e_t$, monthly 1831-2002, $X_t=R_{ft}$ or a rolling-120-month ARMA(1,1) forecast of PPI/CPI inflation. Coefficient on $R_{ft}$: $-5.56$ ($t=-2.57$) in Fama-Schwert's 1953-1971 sample, $-3.96$ ($t=-4.58$) 1831-1925, $-1.14$ ($t=-1.08$) 1972-2002, $+0.11$ 1926-1952. Negative in almost every period, but weak after publication. Since the standard "market premium = $R_m-R_f$" model implies $g=1$, even $-1.14$ rejects it ($t=-2.03$). Expected-inflation proxies predict worse than the rate itself, so the rate effect is not an inflation effect outside 1953-1971. Interpretation: a slowly time-varying equity premium, not an exploitable anomaly.

**Dividend yield (Table 6, Fig. 1).** $r(t,t+T)=a+d\,Y(t)+e$, annual, $Y=D(t)/P(t-1)$ or $D(t)/P(t)$, $T=1..4$ years overlapping, HAC t-stats. 1927-1986 (Fama-French 1988) with $D(t)/P(t-1)$: $d=5.25$ ($t=3.03$, $R^2=0.07$) at $T=1$ up to $12.55$ ($t=4.54$, $R^2=0.12$) at $T=4$. 1872-1926 and full 1872-2000: no $t$ above 2, $R^2\approx 0$. Market-timing test: holding stocks only when the 1927-86 model predicts a return above the bill rate turns \$1,000 in 1872 into about \$2.2m by 1999 vs. about \$6.7m buy-and-hold; after 1990 the model always said "bills," missing the 1990s.

## Investor returns and limits to arbitrage

- **Individuals:** Odean (1999; 10,000 discount-brokerage accounts, 1987-93) and Barber-Odean: stocks bought underperform stocks sold, even before costs. The anomaly is that they reliably pick FF3 underperformers; a hint is that they sell recent winners, i.e. trade against momentum.
- **Closed-end fund discounts:** predict fund returns (Thompson 1978); Pontiff (1995) shows the excess return comes from discount mean-reversion, not underlying assets; Lee-Shleifer-Thaler tie discounts to small-stock sentiment. Pontiff (1996): discount magnitude correlates with arbitrage cost proxies.
- **Mutual funds:** gross returns consistent with CAPM, net below it (Malkiel 1995, survivorship-free); persistence is explained by stock momentum (Carhart 1997) except "cold hands." Hedge funds: nonlinear, dynamic exposures (Fung-Hsieh 1997) make standard alpha measures unreliable.
- **IPOs:** \$1,000 rolled monthly into IPOs at offer price from 1960 would be over \$533 x $10^{33}$ by 2001 vs. about \$74,000 in CRSP VW -- evidence that allocation (institutional priority, spinning) and anti-flipping rules, not prices, carry the "anomaly." IPO initial returns are strongly autocorrelated (Lowry-Schwert 2002) but not timeable.
- **Limits to arbitrage:** Shleifer-Vishny (1997) agency frictions; the JFE 2002 special issue (short-sale constraints, lending market, synchronization risk, constrained arbitrageurs) generally finds anomaly magnitude increasing in trading costs.

## Long-horizon event returns

Long-run CAR/BHAR tests have poor specification and power (Barber-Lyon 1997, Kothari-Warner 1997, Mitchell-Stafford 2000); small monthly model errors compound over 3-5 years (Fama 1998); calendar-time portfolio regressions are preferred. Specific points:
- IPO/SEO underperformance (Ritter 1991, Loughran-Ritter 1995) concentrates in small low-B/M firms -- the same FF3 failure cell (Brav-Gompers); leverage reduction after SEOs lowers risk (Eckbo-Masulis-Norli 2000); Schultz's (2003) "pseudo market timing": if issuance responds to past prices, standard long-run measures find spurious underperformance even under rational pricing.
- **Bidders (Schwert 1996, Fig. 3):** 790 NYSE/Amex first bidders 1975-1991, market model estimated on days -379 to -127. CAR drifts to about -8% a year after the bid, but the drift disappears when the estimated intercept $a_i$ is set to zero: bidders had abnormally high pre-bid returns, which the estimation-window alpha extrapolates. A clean example of selection bias in the benchmark, not post-event mispricing. Mitchell-Stafford: EW acquirer portfolios show negative 3-year FF3 alpha, VW do not.

## Implications

- **Asset pricing:** FF3 absorbs size and value, but MacKinlay (1995) notes the implied HML premium is implausibly large -- a linear fit to an anomaly is not an equilibrium model. Behavioral models (BSV, DHS, Barberis-Shleifer) explain known facts but have produced few new refutable predictions. Excess-volatility tests (Shiller) are explicitly set aside as tests of a valuation model rather than of tradable mispricing.
- **Corporate finance:** size as illiquidity proxy (Amihud-Mendelson 1986) -- though a vanished size effect is awkward for that story; B/M is simultaneously read as distress risk, growth options (Smith-Watts), and agency/Tobin's Q (Morck-Shleifer-Vishny), so it cannot support normative advice; slow post-event drift, given the noise in long-run returns, is no basis for timing financing decisions.

## Assessment

- **Convincing:** the out-of-sample protocol, especially extending samples backward (weekend 1885-, rates 1831-, dividend yield 1872-). Backward extension distinguishes snooping (weak before and after) from arbitrage (strong before, weak after): the weekend effect is strong pre-1953 and fades later, pointing to a real effect that decayed; dividend yield is weak in 1872-1926, pointing to sample dependence.
- **Fragile:** size and value post-publication evidence rests on two DFA funds and 8-20 years of monthly data; t-stats of 0.6-0.8 cannot reject alphas of several tenths of a percent per month either. Fund returns embed implementation choices (screens, costs), so they test implementable, not paper, anomalies -- appropriate for Jensen's criterion but conflating decay with implementation drag. Value's later history (weak 2007-2020) fits Schwert's skepticism; momentum's 2009 crash shows its persistence came with tail risk he does not discuss.
- **For a quant PM:** (1) treat the publication date as a structural break and haircut in-sample alphas (cf. McLean-Pontiff 2016, which formalizes this); (2) check where an effect lives (the January effect sits in sub-\$2 illiquid stocks); (3) beware estimation-window alpha and conditioning on past returns in event studies; (4) predictive-regression significance at long horizons with overlapping data says little about timing-strategy P&L.
