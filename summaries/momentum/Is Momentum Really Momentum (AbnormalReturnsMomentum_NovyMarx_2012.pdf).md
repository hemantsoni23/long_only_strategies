# Is Momentum Really Momentum?

**Robert Novy-Marx · 2012 · Journal of Financial Economics 103, 429–453 · Source file `Finance/AbnormalReturnsMomentum_NovyMarx_2012.pdf` · CRSP all stocks Jan 1926–Dec 2010 (strategies from 1927); plus FF49 industries, 25 size/BM portfolios, 23 MSCI country indices, 31 commodity futures, 19 currencies**

## Claim / contribution
The profitability of "12–2" momentum comes mainly from performance **12 to 7 months** before formation ($r_{12,7}$), not from the recent 6 to 2 months ($r_{6,2}$). The lag profile of return predictability rises with lag up to 12 months and then drops off a cliff — "more like an echo than momentum". This contradicts the standard reading of momentum as short-lag positive autocorrelation, and hence the behavioral (BSV 1998, Hong–Stein 1999, DHS/HS 1999) and rational (Johnson 2002, Sagi–Seasholes 2007) models built to generate it. Practically: a large-cap, value-weighted 12–7 quintile strategy earned almost 10% p.a. (1927–2010), which weakens capacity and trading-cost critiques (Korajczyk–Sadka 2004; Lesmond–Schill–Zhou 2004).

## Setup
- $r_{n,m}$ = cumulative return from $n$ to $m$ months (inclusive) before formation; $\mathrm{MOM}_{n,m}$ = winner-minus-loser (WML) on $r_{n,m}$. US stock strategies use NYSE-breakpoint deciles, value-weighted, **one-month holding period**; the author's UMD replication has > 99% correlation with French's UMD.
- "Recent" = 6–2 (5 months), "intermediate" = 12–7 (6 months) — the two halves of the conventional 12–2 window. Using a 5-month intermediate window (first 5 months of the prior year) gives qualitatively identical results.
- Fama–MacBeth (FM): $r^j_t = b_0 + b_{12,7} r^j_{12,7} + b_{6,2} r^j_{6,2} + b_{1,0} r^j_{1,0} + b_{ME}\ln ME^j + b_{BM}\ln BM^j + e^j_t$; regressors winsorized at 1%/99%.
- Spanning tests: regress a test strategy on explanatory strategies; the intercept t-stat measures the information ratio (IR) relative to them.

## Main results

**1. Single-lag term structure (Fig. 1, $\mathrm{MOM}_{\ell,\ell}$, $\ell = 1..15$, Apr 1927–Dec 2010).** Mean WML *increases* with lag through 12, then collapses. Lag-1 WML is −1.04% (VW) / −2.82% (EW) per month (short-term reversal). Volatility *falls* with lag, consistent with mean-reverting stochastic volatility (sorting on big movers selects temporarily high-vol stocks). So the Sharpe-ratio profile slopes up even more steeply than the return profile. Gaussian-kernel "quintile-like" sorts (Fig. 2): the $r_{12,7}$–return relation is strong and roughly linear; the $r_{6,2}$ relation is weaker and confined to the tails. Both long and short sides contribute roughly equally, contradicting Hong, Lim & Stein (2000).

**2. Fama–MacBeth (Table 1; slopes × 10², t-stats in brackets).**

| Sample | $b_{12,7}$ | $b_{6,2}$ | $b_{12,7}-b_{6,2}$ | $b_{1,0}$ |
|---|---|---|---|---|
| 1927–2010 | 1.07 [5.72] | 0.49 [1.88] | 0.58 [2.47] | −7.77 [−20.9] |
| 1927–68 | 1.21 [3.70] | 0.62 [1.40] | 0.60 [1.46] | −9.44 |
| 1969–2010 | 0.93 [5.17] | 0.36 [1.32] | 0.57 [2.42] | −6.10 |
| 1927–47 | 1.29 [2.12] | −0.97 [−1.23] | 2.26 [3.11] | −11.9 |
| 1948–68 | 1.14 [4.54] | **2.20 [6.00]** | −1.06 [−3.08] | −6.93 |
| 1969–89 | 1.24 [5.29] | 0.37 [1.00] | 0.88 [2.96] | −8.18 |
| 1990–2010 | 0.61 [2.26] | 0.36 [0.87] | 0.25 [0.69] | −4.02 |

$b_{12,7}$ is stable and significant in every 21-year subsample. $b_{6,2}$ swings: negative before WWII, huge in 1948–68 (the era that shaped momentum lore), insignificant afterwards. Rolling 10-year FM (Fig. 3) confirms this.

**3. Factor regressions (Table 2, decile WML, %/month).**

| | Mean | CAPM α | FF3 α | FF4 α | UMD β |
|---|---|---|---|---|---|
| $\mathrm{MOM}_{12,7}$ | 1.20 [5.79] | 1.36 [6.64] | 1.56 [8.07] | **0.54 [3.78]** | 0.99 [30.4] |
| $\mathrm{MOM}_{6,2}$ | 0.67 [2.88] | 0.99 [4.61] | 1.16 [5.54] | −0.05 [−0.37] | 1.18 [37.2] |

Difference in means is 0.54%/month [2.21]. Both strategies have negative market and HML loadings (FF3 HML β: −0.64 and −0.44), which inflate FF3 alphas. Adj. R² with UMD is 0.560 (12–7) vs 0.665 (6–2).

**4. Spanning against FF3 + the other strategy (Table 3).** Full sample: 12–7 α = 1.24 [6.62]; 6–2 α = 0.65 [3.18]. So **both** have significant IRs over the full sample. The asymmetry is in the subperiods. 12–7 is significant in all four quarters. 6–2 is significant only in 1948–68 (0.93 [3.89]) and is insignificant late (1969–2010: 0.15 [0.58]) even though its raw mean then is 0.80 [2.80], because it covaries strongly with 12–7 (loading 0.53 [10.8]). Late-sample raw means: 12–7 1.42 [6.01] vs 6–2 0.80 [2.80]. Trailing 10-year Sharpe of 12–7 is never negative. Since Nasdaq entered CRSP, 6–2's Sharpe ratio has been below 60% of 12–7's.

**5. Independent 5×5 double sorts (Tables 4–6, VW, NYSE quintiles).** Return spreads along $r_{12,7}$ are roughly twice those along $r_{6,2}$.
- Full sample: intermediate-winner/recent-loser minus recent-winner/intermediate-loser = 0.58%/month [2.81]; FF4 α 0.60 [2.87]. FF4 prices the recent-sorted spreads but not the intermediate ones.
- Late sample (1969–2010): the 12–7 spreads conditional on $r_{6,2}$ quintile are 1.07–1.30 [3.67–6.35]. The 6–2 spreads conditional on $r_{12,7}$ are 0.26–0.49 [0.97–1.93], and GRS cannot reject that they are jointly zero ($F_{5,498}=0.837$, p = 52.4%). Recent-winner/intermediate-loser underperforms recent-loser/intermediate-winner by 0.81%/month [3.38] (FF4: 1.08 [4.61]). The RMS excess return of the 25 portfolios is 0.52%/month, falling to 0.15 relative to FF3 + $\mathrm{MOM}_{12,7}$. RMS of the conditional 12–7 spreads is 1.02 vs 0.35 for the conditional 6–2 spreads. The 6–2 conditional strategies have FF3+MOM12,7 alphas that are jointly zero ($F_{5,494}=0.449$, p = 81.4%).
- Puzzle: intermediate-neutral 6–2 strategies load on $\mathrm{MOM}_{12,7}$ (average loading > 1/3; mean rolling 10-year loading > 0.25 after the mid-1940s, Fig. 5), even when they hold no stocks in common with 12–7. So the comovement is not mechanical.

**6. Size (Table 7, quintile WML within NYSE size quintiles, %/month).** The large quintile averages 337 firms and 77.9% of market cap (average cap $4.7bn).

| | Small | 2 | 3 | 4 | Large |
|---|---|---|---|---|---|
| $\mathrm{MOM}^i_{12,7}$ full | 0.83 [5.17] | 0.85 | 1.00 | 0.87 | **0.82 [4.66]** |
| $\mathrm{MOM}^i_{6,2}$ full | 0.53 [2.99] | 0.73 | 0.52 | 0.53 | **0.24 [1.25]** |
| $\mathrm{MOM}^i_{12,7}$ late | 1.09 | 1.02 | 1.05 | 0.89 | 0.91 [4.20] |
| $\mathrm{MOM}^i_{6,2}$ late | 1.08 | 1.01 | 0.62 | 0.50 | 0.16 [0.68] |
| 6–2 α vs FF3+12–7, late | 0.52 [2.72] | 0.46 [2.31] | 0.20 | 0.03 | −0.12 [−0.54] |

RMS spread across size quintiles: 0.88 (12–7) vs 0.53 (6–2). Late in the sample, recent momentum survives only in the two smallest quintiles (< 5% of cap). Equal-weighting micro-caps kills 6–2 (0.09%/month vs 0.53 VW) but hurts 12–7 less (0.56 vs 0.83). The smallest 10% of stocks (0.14% of cap) show no momentum.

**7. Other asset classes (tertile sorts, top/bottom 30%, EW across assets).**

| Universe (sample) | 12–7 mean | 6–2 mean | SR 12–7 / 6–2 | α(12–7 \| 6–2) | α(6–2 \| 12–7) |
|---|---|---|---|---|---|
| FF49 industries (1927–2010) | 0.57 [4.93] | 0.27 [2.19] | 0.54 / 0.24 | 0.47 [4.42] | 0.04 [0.39] |
| 25 size–BM styles (1927–2010) | 0.42 [3.79] | 0.12 [0.98] | 0.41 / 0.11 | 0.41 [3.73] | 0.09 [0.70] |
| 23 country indices (1971–2010) | 0.93 [5.17] | 0.43 [2.16] | 0.82 / 0.36 | 0.80 [4.69] | 0.07 [0.39] |
| 31 commodities (1966–Nov 2008) | 1.18 [4.06] | 0.39 [1.33] | 0.62 / 0.20 | 1.14 [3.94] | 0.28 [0.94] |
| 19 currencies (Nov 1984–Aug 2007) | 0.57 [4.15] | 0.36 [2.43] | 0.84 / 0.35 | 0.48 [3.58] | 0.06 [0.41] |

- Industries vs UMD: 12–7 keeps α 0.22 [2.54]; 6–2 α is −0.13 [−1.50].
- Last-month (1–0) momentum exists in all of these markets: industries 0.38 [3.61], styles 0.52, countries 0.43, commodities 1.39 [4.47], FX 0.48.
- Including month 1 (a 6–1 window) never makes the recent signal span 12–7, but in commodities 6–1 does have a significant IR vs 12–7 (0.89 [2.91]). For commodities, the ex-post MVE combination is about 50/50 12–7 and 1–0 (the two are nearly orthogonal).
- FX: carry (0.93%/month [6.92]) does not explain 12–7 currency momentum. Hedged vs unhedged country-index tests indicate index, not currency, momentum.
- 12–7 and 6–2 correlations: 39.9% (US stocks), 37.1% (industries), 6.2% (styles).
- These markets have no 12-month (Heston–Sadka) seasonal and no January effect, which is evidence against those explanations.

**8. Robustness vs known effects (Section 6).**
- *12-month effect* (Table 13; size- and industry-adjusted-BM-hedged deciles): $\mathrm{MOM}_{12,12}$ and $\mathrm{MOM}_{11,7}$ each have independent IRs; $\mathrm{MOM}_{6,2}$ has α 0.10 [0.45] vs both.
- *Earnings momentum* (Table 14, 1973–2010, SUE = latest quarterly earnings minus the average of the prior 4 quarters, scaled by assets): SUE barely moves $b_{12,7}$ (1.02 → 0.98) but pushes $b_{6,2}$ to 0.23 [0.81]. The gap $b_{12,7}-b_{6,2}$ rises to 0.78 [3.06]. Within SUE deciles, 6–2 quintile WML averages 0.20%/month (GRS cannot reject zero), while 12–7 averages 0.91, significant in every decile.
- *Capital-gains overhang / disposition* (Frazzini 2006 measure, EW, Apr 1980–Aug 2002): GML earns 0.86 [3.44] but is spanned by 12–2 (α −0.15) and 12–7 (α −0.05). GML spans 6–2 (α 0.02) but not the reverse. Within overhang quintiles, EW 12–2 earns 1.44–1.94%/month vs 1.37 unconditionally. GML conditional on past returns earns only through terrible Januaries, which supports a tax-loss explanation for momentum's January losses (Appendix, Table A1).
- *Consistency* (Grinblatt–Moskowitz 2004 consistent-winner indicator: positive in ≥ 8 of 11 months): it works because consistent winners are big winners with low realized volatility. Adding a big-winner dummy and $\sigma_{12,2}$ halves its coefficient to insignificance (0.16 [1.60]). All consistency variables matter only in 1969–2010. $b_{12,7}-b_{6,2}$ stays at about 0.53–0.58, significant.

## Critical assessment
- **Convincing:** consistent pattern across FM, spanning, double sorts, size buckets and five nearly independent asset classes; stable over 84 years; the robustness section rules out the obvious confounds (12-month seasonal, SUE, overhang, consistency).
- **Caveats:**
  - The "echo" is a descriptive lag profile with no mechanism. A later paper (Goyal & Wahal 2015, "Is Momentum an Echo?") finds the 12–7 dominance does not generalize to 37 international stock markets, so the cross-sectional US-equity result may be partly sample-specific.
  - The late-sample 6–2 insignificance relies on spanning against a factor that is itself estimated in-sample.
  - One-month holding periods and no transaction costs, although the large-cap results mitigate the cost concern.
  - Currency data stop in 2007 and commodity data in 2008, so both miss the 2009 momentum crash.
- **Paper inconsistencies:** the text says $b_{6,2}$ is "significantly positive" in 1990–2010, but Table 1 shows t = 0.87. Table 4's caption says the sample ends Dec 2008 while the text says 2010. In Section 3.3 the late-sample comparison says "performed well over the *second* half of the preceding year" where the first half is meant. Many minus signs are lost in the PDF text layer; signs above follow the paper's narrative.

## Practical relevance for a quant PM
- A standard 12–1/12–2 signal effectively overweights the least informative months. Weighting the months 12–7 more heavily improves Sharpe ratios, and this matters most in large caps, where 6–2 is dead.
- A 12–7 sleeve adds about 0.5%/month of FF4 α beyond UMD, so a risk model that treats UMD as "the" momentum factor understates this exposure.
- Cross-asset trend books: 12–7 dominates 6–2 everywhere. The strongest short-horizon effect is 1-month continuation in commodities (and to a lesser extent industries, styles, countries and FX); there, combine 12–7 with 1–0 rather than using 6–1.
- Backtest hygiene: samples starting in the 1950s overstate recent-horizon momentum.
