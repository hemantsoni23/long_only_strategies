# What Explains the Dynamics of 100 Anomalies? — Jacobs (2015) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | What explains the dynamics of 100 anomalies? |
| **Author** | Heiko Jacobs (University of Mannheim) |
| **Journal** | *Journal of Banking & Finance* **57**, 65–85, 2015 |
| **DOI** | 10.1016/j.jbankfin.2015.03.006 |
| **Keywords** | Anomalies; investor sentiment; limits to arbitrage; short leg; meta-anomalies |
| **Source file** | `Finance/FactorZoo_Jacobs_2015.pdf` |
| **Drive file_id** | `1mRZSfAv-IT7xFxoRVLW1lJtcJujXIL7k` |

---

## Question

The behavioral account of anomalies has two ingredients: psychology creates mispricing, limits to arbitrage (LTA) keep it alive. The testable time-series implication: anomaly returns should be larger when (market-wide) sentiment is high or arbitrage is constrained. Stambaugh–Yu–Yuan (2012) confirm the sentiment half on 11 anomalies; evidence on LTA dynamics is mixed (Nagel 2012 and reversal; Frazzini–Pedersen find the TED spread predicts BAB with the "wrong" sign; Akbas et al. and Hanson–Sunderam find little role for market-level funding constraints). Jacobs's contribution is breadth: a common universe and methodology for 100 anomalies, and a horse race between market-level sentiment and six market-level LTA proxies.

## Data and construction

- **Universe:** CRSP common stocks with price $\ge \$5$ and market cap above the first NYSE decile at formation (Jegadeesh–Titman 2001 screen). Removes ~50% of firm-months but only a few percent of market cap. Anomalies that exist only in micro/illiquid stocks are excluded by construction.
- **Anomalies:** 100 published long-short, decile-type strategies (rebalanced every 1–12 months, EW and VW), selected if computable from CRSP/Compustat/I/B/E/S at monthly frequency, reported against at least a 3-factor benchmark, and not prominently claimed as a risk premium. >65,500 anomaly-months; samples on average ~20 years longer than the originals (earlier start plus data to 2011).
- **Meta-anomalies:** 20 groups, each an EW average of 2–17 constituents: (1) law-of-one-price (LoOP) violations — 4 settings, partly international, each standardized to mean 0 / sd 1; (2) momentum (17); (3) technical analysis; (4) short-term reversal; (5) long-term reversal; (6) calendar; (7) lead-lag among linked firms; (8) pairs trading; (9) beta; (10) distress; (11) skewness/lottery; (12) differences of opinion; (13) industry; (14) fundamental analysis; (15) net stock issuance/financing; (16) investment/growth; (17) innovation; (18) accruals; (19) dividends; (20) earnings surprises. The "composite" is the EW average of meta-anomalies 2–20; a pooled panel with random effects is the alternative.
- **Dependent variable:** FF3-adjusted return, $\hat a_i + \hat\varepsilon_{i,t}$ from $R_{i,t}=a_i+b_i\,\mathrm{RMRF}_t+s_i\,\mathrm{SMB}_t+h_i\,\mathrm{HML}_t+\varepsilon_{i,t}$.
- **Sentiment:** Baker–Wurgler (2006) index orthogonalized to macro variables (7/1965–12/2010); alternatives: Michigan consumer expectations, Conference Board confidence, AAII survey, all orthogonalized to the same macro variables.
- **LTA proxies (six):** VXO (from 1986), average idiosyncratic volatility (FF3 residual vol from daily data, EW across the universe, from 1926), TED spread, Moody's BAA–AAA spread, average Corwin–Schultz bid-ask spread, Pástor–Stambaugh liquidity (sign-flipped). Average pairwise correlation 0.42 (0.21 for median dummies); VIX–idio vol correlation 0.51. Correlation with sentiment averages 0.10 (0.05 for dummies), none above 0.25 — so the two families make genuinely different predictions. All proxies cluster in 1929–30s, 1987, LTCM/dot-com, 2007–09.
- White standard errors throughout (Newey–West gives similar results).

## Method

Univariate predictive regressions for each meta-anomaly $a$ and proxy $x$:

$$
r^{\mathrm{FF3}}_{a,t}=\alpha_a+\beta_a\,\mathbf 1\{x_{t-1}>\mathrm{med}(x)\}+\varepsilon_{a,t},
$$

so $\alpha$ is the return in low-LTA (or low-sentiment) months and $\beta$ the increment in high months; then continuous $x_{t-1}$, aggregate LTA measures (first PC of 3 or 6 proxies; or average of min–max scaled proxies), and the joint regression

$$
r^{\mathrm{FF3}}_{a,t}=c_a+\beta^{L}_a\,L_{t-1}+\beta^{S}_a\,S_{t-1}+\varepsilon_{a,t},
$$

with $L$ and $S$ standardized to unit variance (8/1965–1/2011, $N=546$). Legs are analyzed separately following Stambaugh et al. (2012).

## Results

**Unconditional.** Every one of the 100 anomalies has a significant FF3 alpha (often smaller than originally reported). Average alpha across groups 2–20: 79 bp/month EW, 70 bp VW — the small EW/VW gap reflects the size/price screens. Momentum, short-term reversal, lead-lag, pairs and earnings surprises exceed 100 bp/month (e.g. momentum 1.13%, t = 9.57; short-term reversal 1.44%, t = 11.04; earnings surprises 1.22%, t = 13.18). The 10th–90th percentile range of monthly returns is several hundred bp for every meta-anomaly. Average pairwise correlation of the 100 FF3-adjusted EW returns: 0.12.

**Sentiment (Tables 1, 2, 7, 8).**
- Average EW anomaly: 63 bp after below-median sentiment vs 95 bp after above-median (VW: 54 vs 85 bp).
- >80% of individual anomalies have the predicted sign, ~40% significant; 10 of the 11 Stambaugh et al. anomalies replicate (accruals is the exception in this universe, but turns positive in their universe).
- Meta level: 17/20 positive on the dummy; significant at 10% (1%) for 8 (5). Strongest for overreaction-type groups — beta (1.03, t = 3.65), differences of opinion (0.84, t = 3.61), skewness (0.72, t = 3.48), net issuance (0.54, t = 3.61); weakest for underreaction-type groups (lead-lag, pairs, innovation, dividends, earnings surprises). Momentum is not significant (0.45, t = 1.28).
- Continuous, standardized: +1 sd lagged BW sentiment predicts +17 bp (EW composite, t = 3.50) and +20 bp (VW, t = 3.95). Alternative orthogonalized sentiment indices give 15–17 bp (t = 1.73–3.00).

**Short-leg asymmetry (Tables 9–10, VW legs, FF3-adjusted).**
- Unconditional alpha: composite long leg +24.5 bp (t = 10.06), short leg −36.4 bp (t = −8.81). Most groups are short-driven (distress: +23 vs −72 bp); only long-term reversal, calendar, pairs, innovation, industry and dividends are long-driven.
- +1 sd sentiment: long leg +2.6 bp (t = 1.14) vs short leg −17.7 bp (t = −3.96). The LTA aggregate moves both legs by 2–3 bp, insignificant. Consistent with Miller (1977): permanent short-sale constraints make overpricing, amplified by sentiment, the dominant mispricing — a mechanism that requires the *level* of LTA but not its variation.

**LTA dynamics, binary (Tables 3–4).**
- LoOP violations respond strongly: above-median bid-ask spread → +0.365 (t = 6.79), roughly 3/4 sd; idio vol → +0.318 (t = 4.96), ~2/3 sd; VIX +0.279 (t = 5.06); illiquidity +0.136 (t = 2.34).
- Short-term reversal, pairs, net issuance and innovation respond to some proxies (e.g. short-term reversal: bid-ask +1.14, t = 4.20; idio vol +1.00, t = 3.73), not consistently across all six.
- Idio vol is the best proxy: 75% of meta-anomalies load positively, 40% significantly; composite +22 bp (t = 2.62) over a 64 bp baseline (~1/3). Other composite increments: VIX +8 bp (t = 0.63), TED +7 bp, credit +9 bp, bid-ask +16 bp (t = 1.92), illiquidity −3 bp.
- Several signs are opposite to theory: technical analysis is weaker in high-LTA states (credit spread −1.09, t = −3.64); momentum's high-VIX increment is −0.37 (t = −0.71) against a 1.25% baseline. Earnings surprises earn 89–128 bp in *low*-LTA states irrespective of proxy.

**LTA dynamics, continuous and aggregate (Tables 5–7).**
- Continuous proxies keep LoOP, short-term reversal and pairs significant, while idio vol loses significance for most groups; composite coefficients are nil (VIX −0.0058, t = −0.58; idio vol 2.0, t = 0.11).
- First PC explains 80% of 3 proxies (1926–2011) and 47% of 6 (1986–2011). One sd of the PC: LoOP +0.61 (t = 12.45), short-term reversal +1.14, pairs +0.61; momentum −0.40 to −0.74 (significant in the 1986+ sample); composite ≈ 0.
- Joint regression: LTA gives 1–5 bp per sd for the composite (t = 0.1–0.8) vs 17–20 bp for sentiment; coefficients are nearly unchanged from the univariate runs. LoOP is the only group with a material $R^2$ (27%); the composite's $R^2$ is ~3%. Momentum (−0.50, t = −2.17) and technical analysis (−0.74, t = −2.67) load *negatively* on aggregate LTA.
- Financial-crisis dummy (2007–09 vs 2005–06 and 2010–11): composite **−52 bp** (t = −2.40), momentum −1.97 (t = −2.07), beta −1.60 (t = −2.69). The period with maximal measured constraints was bad for anomaly returns, not good.

**Robustness.** Unchanged under: winsorizing; VW (slightly weaker); market-only adjustment (raw returns give mixed results); piecewise-linear specifications; quarterly data, alternative lags, contemporaneous proxies; levels vs changes; linear trend, 25-year subsamples, excluding the crisis, post-publication dummy (McLean–Pontiff); alternative LTA proxies (Amihud, Hu–Pan–Wang noise, aggregate short-interest changes, LoOP itself as a proxy, shadow-bank/broker-dealer and hedge-fund-index variables, LIBOR, term spread); macro controls; PCA of the anomalies themselves; including small stocks (the composite LTA coefficient rises only ~3 bp EW / 10 bp VW). The sentiment effect is similar in high- and low-LTA periods.

**Anomaly-level arbitrage activity (Table 11).** For the 96 anomalies in groups 2–20, (i) the short-minus-long difference in cross-sectional short-interest rank (NYSE/AMEX, Compustat) and (ii) the average turnover rank of the legs are aggregated to the meta level; monthly changes are regressed on contemporaneous VIX, TED and bid-ask. The short-interest differential is positive on average (except lead-lag and innovation), so arbitrageurs do trade these strategies, yet virtually all coefficients are insignificant. Market-level constraint proxies do not track the capital actually deployed in each anomaly.

## Interpretation

Jacobs's reading: the variation of sentiment together with the *base level* of LTA — mainly permanent short-sale constraints — explains the survival of anomalies. Month-to-month fluctuations in market-wide LTA matter only for near-arbitrage, liquidity-provision strategies (LoOP, short-term reversal, pairs). An alternative he acknowledges: sentiment could itself proxy for noise-trader risk, a form of LTA.

## Limitations

- These are predictive correlations; the macro proxies may simply mismeasure constraints that bind at the anomaly or stock level (borrow cost, recall risk, the arbitrageurs' own funding). The paper's own Table 11 points this way.
- The screen deliberately removes the micro-cap segment where both sentiment and LTA effects are known to be strongest; the results describe the investable universe, not the whole literature.
- The meta-anomaly averages can mask heterogeneity inside a group (17 momentum variants are not independent strategies).
- LTA proxies have different start dates (VIX only from 1986), so cross-proxy comparisons mix samples; the median-split dummies discard information.
- BW sentiment is persistent and a known source of spurious-regression concern; the paper relies on breadth across anomalies (as Stambaugh et al. 2014 do via simulation) and alternative indices rather than a formal correction.
- Replications are approximate (the author says as much), and the anomaly set is conditioned on publication.

## Assessment

- **Convincing:** the asymmetry. Across a broad, investable universe, sentiment predicts anomaly returns almost entirely through the short leg (−17.7 bp/sd, t ≈ 4) with a negligible long-leg effect; this replicates Stambaugh–Yu–Yuan out of sample on ~9x as many anomalies. The null for LTA dynamics holds across six proxies, PCA and composite measures, specification changes, and the joint regression.
- **Fragile:** the idio-vol result (it disappears in continuous form) and any single meta-anomaly × proxy cell — with 20 × 6 regressions, a few significant cells are expected by chance. Momentum's negative loading on LTA and the crisis dummy are consistent with momentum-crash evidence, but rest on few episodes.
- **For a quant PM:**
  1. Sentiment is a short-book risk variable, not a gross-exposure timing signal: with an $R^2$ of about 3% for the composite, it modulates the expected return of the short leg rather than justifying large dynamic swings. It is also strongest precisely when borrow is scarcest in the names being shorted.
  2. "Add anomaly risk when VIX/TED/credit spreads spike" is supported only for liquidity-provision strategies (reversal, pairs, near-arbitrage). For momentum, technical and beta-type strategies the point estimates go the other way, and the 2007–09 dummy is −52 bp/month for the composite.
  3. The unconditional premium (~65–80 bp/month FF3 alpha in this universe, before costs) dominates both overlays in magnitude: level ≫ sentiment timing ≫ LTA timing.
  4. Because market-level stress proxies do not move anomaly-level short interest or turnover, crowding and capital measures must be built at the strategy level (e.g. short-interest differentials between legs, borrow fees), not borrowed from macro funding indicators. This is also the author's suggested research direction.

---

*Scholar batch_2026-09-23_2 | Paleologo-style notes*
