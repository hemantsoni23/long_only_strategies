# Is Momentum an Echo?
**Authors:** Amit Goyal, Sunil Wahal
**Year:** 2015
**Journal/Venue:** Journal of Financial and Quantitative Analysis, Vol. 50, No. 6, pp. 1237-1267
**Source file:** Finance/Momentum_GoyalWahal_2015.pdf

## Question

Novy-Marx (2012) found that in the U.S., WML portfolios sorted on intermediate returns (IR, months $-12$ to $-7$) beat those sorted on recent returns (RR, months $-6$ to $-2$) by up to about 0.5%/month, an "echo" that no behavioral or rational momentum model predicts. Goyal and Wahal ask whether this survives (i) a true out-of-sample test in 37 non-U.S. markets and (ii) a careful look at the U.S. month-by-month term structure. Answer: no general echo; the U.S. result is mostly the short-term reversal leaking into month $-2$, plus the 12-month (Jegadeesh/Heston-Sadka) seasonal effect, plus a month-count asymmetry in Novy-Marx's split.

## Data

- Datastream/Worldscope, 45 MSCI ACWI countries, 1980-2010, live and dead stocks; primary listings, common equity only (text screens remove preferreds, REITs, ETFs, ADRs etc.), USD returns, reversal-spike filter (+300% then -50%), returns >1000% dropped, monthly 1/99% winsorization. Coverage 80-99% of WFE market cap.
- Country tests require $\ge 100$ stocks per country-month, which drops 7 countries (Ireland, Colombia, Czech Republic, Egypt, Hungary, Morocco, Poland) from single-country tests (they remain in regional aggregates), leaving 37.
- U.S.: CRSP/Compustat common stocks, 1927-2010 and 1980-2010; NYSE breakpoints, deciles, price > \$1.
- Local 3-factor models built per country (size split at 75th/25th pct of cap, B/M 30/70), with regional factors constructed consistently with each aggregation scheme.
- Four aggregations: EW countries, VW countries, pooled stocks (requires $\ge 1000$ stocks), pooled "ex-country" (sort on return in excess of local market). Regions: developed, emerging, Americas ex-U.S., Asia, Europe. Japan averages 75% of Asia's weight.

## Baseline

Standard $-12{:}-2$ quintile momentum (VW, 1-month hold): WML significant in 12/22 developed and 2/15 emerging markets; strong in Australia, Canada, Germany, UK (e.g. UK 1.48%/mo, t=3.68); zero in Japan (0.21, t=0.59). Aggregates: developed 0.77 (t=2.75), emerging 0.47 (t=1.98), Europe 1.19 (t=3.85), Asia 0.27 (t=0.87).

## Tests and results

**Single sorts (quintiles; U.S. deciles).** U.S. RR(WML) minus IR(WML): $-0.51\%$ (t=$-2.11$) 1927-2010, close to Novy-Marx's $-0.54\%$ (t=$-2.21$); $-0.62\%$ (t=$-1.71$) 1980-2010. Internationally, no aggregate return difference is significant in any of 5 regions x 4 schemes. In alphas, only VW developed ($-0.60$, t=$-2.06$) and pooled Asia ($-1.01$, t=$-1.98$) show an echo; both vanish without Japan ($-0.15$, t=$-0.60$; $0.02$, t=$0.03$). Across 37 countries only 2 return differences are significant, and both go the *wrong* way for the echo (Australia +1.33, t=2.72; Israel +1.27, t=2.10, i.e. RR better). Japan alone shows an alpha echo ($-0.77$, t=$-1.99$).

**Independent 3x3 double sorts (U.S. 5x5).** Compare $\text{IR(WML)}|\text{RR}_W$ with its mirror $\text{RR(WML)}|\text{IR}_W$; the difference reduces to $X_3 - X_7$ (IR-winner/RR-loser minus RR-winner/IR-loser). U.S. 1980-2010: RR minus IR $-0.75\%$ (t=$-2.48$), alpha $-0.85\%$ (t=$-2.86$). International: VW developed $-0.42$ (t=$-2.12$) and Asia VW/pooled significant, all driven by Japan (VW developed ex-Japan: IR-RR only 0.23 return, 0.28 alpha, insignificant). Countries: 4 significant echoes (Japan, Switzerland, China, Turkey) vs 3 reverse (Australia, Israel, Chile).

**Fama-MacBeth.**
$$R_{it}-R_{ft}=\gamma_0+\gamma_1\ln ME_{i,t-1}+\gamma_2\ln BM_{i,t-1}+\gamma_3R_{i,t-1}+\gamma_4R_{i,t-2:t-6}+\gamma_5R_{i,t-7:t-12}+\varepsilon_{it}$$
(NW 3 lags, coefficients x100). U.S. $\gamma_4-\gamma_5$: $-0.27$ (t=$-1.15$) 1927-2010 and $-0.02$ (t=$-0.07$) 1980-2010, so even in the U.S. the characteristic-controlled echo is weak. Asia shows IR > RR (e.g. VW $-1.14$, t=$-2.56$), again Japan; Americas ex-U.S. shows the reverse (EW +1.11, t=2.52). Robustness: large stocks only (top 25% cap) and decile sorts give no robust echo; deciles strengthen the reverse effect in Australia ($-1.29$, t=1.90) and Canada ($-1.58$, t=2.26), Japan unchanged (0.90, t=1.86).

Cross-country explanations fail: Hofstede individualism (U.S. 91) cannot explain it since Australia (90) and UK (89) have no echo.

## The U.S. term structure: where the "echo" comes from

Lag-by-lag regressions (Jegadeesh 1990 plus size and B/M):
$$R_{it}-R_{ft}=\gamma_0+\sum_{k=1}^{12}\gamma_k R_{i,t-k}+\gamma_{13}\ln ME_{i,t-1}+\gamma_{14}\ln BM_{i,t-1}+\varepsilon_{it}.$$
1927-2010 raw coefficients (x100): $\gamma_1=-6.78$, $\gamma_2=-0.34$ (t=$-1.26$; 3-factor-adjusted $-0.55$, t=$-2.29$), $\gamma_3..\gamma_{11}$ all positive (0.63-1.83), $\gamma_{12}=1.88$ (t=7.73), the largest. So month $-2$ carries residual reversal and month $-12$ a seasonal kick. Subperiods: $\gamma_2$ strongly negative in 1927-47 and 1969-89, near zero otherwise; $\gamma_{12}$ weakens in 1990-2010, which explains why Novy-Marx's own FM echo drops to 0.25 (t=0.69) in that period.

**55 definitions, Romano-Wolf.** With months $-12..-2$ there are 55 contiguous (IR, RR) splits. Differences in *sums* of $\gamma_k$ are mechanically monotone in the month-count gap (under a flat term structure, more months = larger sum). Novy-Marx's split (IR 6 lags [12,7] vs RR 5 lags [6,2]) is significant in sums (2.31, bootstrap 10%/conventional t=2.73) but not in *averages* (0.21, t=1.27): his echo largely reflects IR using one more month. Averages favor IR in all 55 definitions, many surviving the Romano-Wolf stepwise FWE bootstrap (Politis-Romano stationary bootstrap, B=10,000), but every RR definition contains month $-2$ and every IR definition contains month $-12$.

**Excluding month $-2$** (45 definitions using $-12..-3$, still deliberately keeping $-12$ in IR): virtually no IR > RR in averages; e.g. IR [12,8] vs RR [7,3]: $-0.12$ raw (t=$-0.68$), $-0.16$ 3-factor. The few significant exceptions all hinge on month $-12$.

**Tradable check.** IR = $-12..-8$, RR = $-7..-3$ (5 months each). U.S. single sort: return difference 0.34% (t=1.40), 3-factor alpha 0.23% (t=0.98; the introduction quotes 0.24%). Double sort: 0.37% (t=1.91), alpha 0.23% (t=1.20). International FM variants that drop $-2$ and/or $-12$ show no echo; with both removed, Europe actually favors RR (e.g. pooled ex-country 1.07, t=3.20).

## Conclusion

No robust echo outside the U.S. (Japan being the only consistent exception); inside the U.S. the IR advantage is explained by (a) reversal spilling into month $-2$, (b) the 12-month seasonal effect, (c) unequal window lengths. The open puzzle shifts from momentum to why short-term reversal extends to month $-2$; liquidity/inventory stories seem too short-lived, overreaction stories are not horizon-specific enough to test.

## Assessment

- Convincing: out-of-sample geography plus four aggregation schemes; the sums-vs-averages point and the lag-by-lag decomposition are the real contribution and are simple enough to replicate. Handling the specification search with Romano-Wolf is appropriate.
- Fragile: many international nulls have wide standard errors (country WMLs have t-stats of 1-2 even for plain momentum), so "no evidence of an echo" is partly low power; the Japan exclusions are ad hoc, though the direction of results is consistent. The 1980-2010 U.S. FM result shows that even the U.S. echo is weak after controlling for characteristics, so the evidence is mostly about portfolio sorts.
- Practical: for a signal builder, the message is not "use IR" but model the lag profile: skip month $-1$ and consider down-weighting or skipping month $-2$; month $-12$ is a separate seasonal signal (Heston-Sadka) and should not be credited to momentum. Equal-weighting months within a window is a neutral benchmark against which "echo" claims should be judged.

Related: [[Is Momentum Really Momentum (AbnormalReturnsMomentum_NovyMarx_2012.pdf)]] (Novy-Marx, the echo paper).
