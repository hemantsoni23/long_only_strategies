# Investor Flows and the 2008 Boom/Bust in Oil Futures (Singleton 2012) — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Title (PDF)** | Investor Flows and the 2008 Boom/Bust in Oil Prices |
| **Author** | Kenneth J. Singleton (Stanford GSB) |
| **Date / venue** | Working paper, April 27, 2012 (grew out of a survey for the Air Transport Association of America; later published in *Management Science*, 2014) |
| **Source file** | Finance/CrudeOilFutures_Singleton_2012.pdf (the PDF text of the regression Tables 3–5 did not extract; coefficients below are those quoted in the text) |
| **Sample** | Weekly, 12 Sep 2006 – 12 Jan 2010; NYMEX WTI futures of 1–36 months; CFTC Commodity Index Trader (CIT) reports |

## Question and claim

Did investor flows, not just supply and demand fundamentals, move crude oil futures prices during the 2008 boom and bust? The paper makes two arguments:

- **Conceptual.** Standard storage and representative-agent models (Hamilton 2009; Pirrong 2009) and the OECD case against speculation (Irwin–Sanders 2010) rule out, by assumption, learning under imperfect information, differences of opinion and limits to arbitrage. Those are exactly the channels that can produce drift, booms and busts.
- **Empirical.** 13-week growth in imputed index-investor long positions and in hedge-fund ("managed money") spread positions predicts 1- and 4-week oil futures excess returns. This holds after controlling for US and emerging-market equity returns, dealer funding, open interest, the average basis and lagged returns. The effect appears to run through risk-premium or information channels rather than convenience yield.

## Framework

Without stock-outs, storage equilibrium gives $S_t = \mathbb{E}^Q_t\big[e^{-\int_t^T (r_s - C_s)\,ds} S_T\big]$ and $F^T_t = \mathbb{E}^Q_t[S_T]$, with $C$ the net convenience yield. With the risk premium defined as $RP^T_t = \mathbb{E}^P_t[S_T/S_t] - \mathbb{E}^Q_t[S_T/S_t]$ and $r$, $C$ roughly constant over $[t,\tau]$:

$$
\frac{\mathbb{E}^P_t[S_\tau] - S_t}{S_t} - y^\tau_t(\tau - t) \;\approx\; RP^\tau_t - C_t(\tau - t).
$$

Expected excess returns therefore mix convenience yield and a time-varying premium. Storage models in the Deaton–Laroque tradition set $RP \equiv 0$; Singleton cites Fama–French (1987), Gorton–Hayashi–Rouwenhorst (2007), Basu–Miffre and Hong–Yogo as evidence against that. Implications:
- Spot prices embed expectations of future activity.
- Futures and swap demand can move spot prices without anyone taking delivery. This rebuts the OECD claim that index investors "would have to take delivery" to affect cash prices.
- Premia move with the risk-bearing capacity of intermediaries.

**Heterogeneous beliefs.** In a rational-expectations equilibrium with private information, agents learn from prices, which eliminates aggregate drift (Banerjee–Kaniel–Kremer 2009). In a differences-of-opinion equilibrium agents disagree about how to interpret public data, which generates volume, volatility and, when others' beliefs are uncertain, learning from prices and drift. In a Buraschi–Whelan-type economy with signals $dI^j_t$ on an unobserved growth factor $g_t$ and $\log S_t = \rho_0 + \rho_g g_t$, the short rate and the subjective convenience yields $C^j_t$ depend on wealth-weighted consensus beliefs and on the dispersion of beliefs $\Psi_t$. Dispersion is therefore a source of premium variation separate from fundamentals. This part is a sketch borrowed from the term-structure literature, not a model estimated in the paper.

**Supporting facts on disagreement.**
- Oil forecasts are noisy: EIA/IEA revisions, poor non-OECD inventory data, vague OPEC production figures.
- The cross-forecaster dispersion of Consensus Economics one-year oil forecasts comoves positively with the WTI price level (Figure 2).
- Dispersion predicts future realized volatility (Garman–Klass and Yang–Zhang 20-day estimators, Jan 2000–Jan 2010; adjusted $R^2$ 11% and 7%).
- Oil-forecast dispersion relative to world-GDP-forecast dispersion was unusually high in 2008 (Figure 3).

A high price together with high disagreement is hard to square with a mean-reverting rational-expectations benchmark, where extreme prices should produce consensus on reversal.

## The inventory argument

The IEA-style test ("if speculators drive prices, stocks must rise") is too simple:
- **The US commercial crude inventory–price relation is unstable** (Figure 4 regressions of price on inventories):
  - 4/2002–11/2004: slope −0.10 (t = −2.60)
  - 11/2004–7/2007: +0.36 (t = 11.97, $R^2$ = 0.51)
  - 7/2007–5/2008: −0.28 (t = −1.98)
  - 5/2008–10/2009: −0.89 (t = −8.28)
- **The data are incomplete:** emerging-market strategic reserves were being built and are missing or unreliable.
- **Theory gives no unambiguous sign:** Pirrong (2009) shows time-varying volatility can produce either sign; Dvir–Rogoff (2010) show trend growth in demand can make storage amplify demand shocks.

Inventories do rise when the curve is in contango (M2−M4 spread, 2004–2009, Figure 5). From 2007 onward, changes in curve slope *led* changes in inventories, consistent with expectations-driven storage.

## Measuring flows

- **IIP13:** 13-week change in imputed index long positions in WTI (millions of contracts). CIT reports cover index traders in 12 agricultural markets only, so oil positions are imputed via S&P GSCI / DJ-UBS weights (Verleger 2007; Masters 2008). Validation: the correlation with barrel-equivalent positions of the iShares S&P GSCI Commodity-Indexed Trust (from its SEC filings) is 0.85 (Figure 6). Sources of error: swap-dealer netting understates index exposure, scaling up small agricultural weights amplifies noise, and positions are valued at the near-contract price. Even conservative estimates (Stoll–Whaley 2009) show index positions doubling from 2006 to mid-2008 and falling by about half by early 2009.
- **MMS13:** 13-week change in managed-money *spread* positions (unsigned long/short pairs along the curve), the largest component of open interest in the period.
- **Controls:**
  - RSP$_n$, REM$_n$: $n$-week S&P 500 and MSCI Emerging Asia returns
  - REPO$_n$: change in primary-dealer overnight Treasury repo positions, a measure of balance-sheet capacity (Etula 2010; Adrian–Moench–Shin)
  - OI13: 13-week change in open interest
  - AVB$_n$: change in the average basis across maturities $\{1,3,6,9,\dots,24\}$ months, with $B_i(t) = (F^{T_i}_t / S_t)^{1/(T_i - t)} - 1$ (Hong–Yogo; the sign is opposite to the M2−M4 spread)
  - the lagged own return

Correlations: IIP13–OI13 0.56, MMS13–OI13 0.45; AVB1 is nearly orthogonal to REPO1, IIP13, MMS13 and OI13 (−0.15, −0.05, −0.05, −0.08).

## Empirical design

$$
ER^{m}_{t+n}(n) = \mu_{nm} + \Pi_{nm} X_t(n) + \Psi_{nm}\, ER^{m}_t(n) + \varepsilon_{t+n},\qquad n \in \{1, 4\}\ \text{weeks}.
$$

Here $ER^m$ is the unfunded (no T-bill) roll-adjusted return on the generic $m$-month contract. Predictors are scaled by their standard deviations, so $\Pi$ is the percentage return response to a 1-SD move. Standard errors are Newey–West with 5 lags. The CIT data were released only from 2007, so a significant $\Pi$ is read as flows impacting prices, not as a strategy traders could have run. Under stationarity, the 13-week-flow / short-horizon-return projection is equivalent to testing whether flows move prices over 13 weeks (Hodrick 1992). **Weekly** flow changes have little predictive power, as in most prior studies, which the author attributes to high-frequency noise.

## Results

**Moments (Table 2).** One-week excess return means rise and volatilities fall with maturity: 1m mean 0.03%, std 6.49%; 24m 0.17%, 4.32%; 36m 0.20%, 4.14%. Four-week std is 12.7% at 1m and 8.6% at 24m. IIP13 has mean 3.81 and SD 8.42; MMS13 mean 0.14, SD 4.44; OI13 SD 9.98.

**Correlations (Table 1).** Contemporaneous correlations of the one-week return with REM1 are 0.40–0.51 and with AVB1 −0.13 to −0.40. Lagged REM1 and REPO1 flip sign (−0.09 to −0.21), while lagged IIP13 (≈0.25) and MMS13 (0.13–0.19) remain positive.

**Predictive regressions (Tables 3–4, as quoted in the text).**

| 1-SD shock | ER1M, 1 week | ER1M, 4 weeks |
|--|--|--|
| IIP13 | +2.32% | +8.27% |
| MMS13 | +1.62% | +4.29% |
| OI13 | negative, not significant | −4.34% |
| REM | −1.69% (REM1) | positive (REM4) |
| REPO | −1.69% (REPO1) | not significant |
| AVB | −2.10% (AVB1) | not significant |

These should be compared with return std devs of 6.49% (1 week) and 12.7% (4 weeks).
- REM1, IIP13 and MMS13 stay significant at all maturities, with responses declining in maturity.
- Dropping (REPO, IIP13, MMS13) causes a large fall in adjusted $R^2$ for the average 1–12m return.
- With the flows included, **OI13 is negative**, the opposite of Hong–Yogo; without them it is positive and insignificant.
- The lagged own return is only marginally significant (weak reversal), and flows survive adding more lags, contrary to Stoll–Whaley's daily-data conclusion.
- In barrels: +1 million barrels of index position moves the 3m contract by 2.2 bp over 1 week and 9.3 bp over 4 weeks, and the 12m contract by 1.8 bp and 8.1 bp.
- A 1% REM1 shock gives −26/−30 bp next week (3m/12m) but +34/+31 bp over 4 weeks. The impulse response turns positive in week 2 and peaks in week 3: overshooting, then continuation.
- The negative REPO effect is consistent with Etula (dealer funding ease lowers required premia); it is significant at 1 week and gone at 4 weeks.
- The negative AVB effect at 1 week and insignificance at 4 weeks align with Fama–French (1987) and Hong–Yogo.
- **Robustness:** Cushing inventory changes have only a weak negative effect on the front month. 3-month Baltic Dry growth adds 2–3% of $R^2$ with marginal significance and does not displace the flows.

**Figure 7 (timing).** IIP13 and the 4-week average front return both turned down in spring 2008, *before* the July price peak. IIP13 went sharply negative after the peak, and renewed index inflows in late 2008 led the recovery in futures returns.

**Spot-vs-futures gap.** Projecting $S_{t+4} - F^{t+4}_t$ on $X_t$ gives adjusted $R^2$ = 0.39. **Only IIP13 and MMS13 are significant**; AVB (the convenience-yield proxy), OI13 and REM4 are not. Singleton reads this as flows working through futures-curve risk premia and maturity-habitat effects rather than spot-market convenience yield.

**Curve-slope returns (Table 5).** Returns on long-far / short-near positions are more predictable beyond the 6-month point. MMS13 is the precise predictor, with a **negative** loading: more hedge-fund spreading goes with near outperforming far. This is consistent with trading around the "Goldman roll" (Mou 2011), but it extends well past the roll segment: it is significant for 12m−6m and 24m−12m, and even for 3m−1m MMS13 is the only significant predictor (loading 0.28%, $R^2$ = 0.06). IIP13 is mostly insignificant for slope returns. AVB1 predicts all weekly spread returns; AVB4 does not predict monthly ones.

## Critical assessment

- **Strengths.** The paper gives a coherent argument for why flow effects need not show up in inventories, and it controls for the usual suspects (basis, open interest, equity, funding). The spot-vs-futures-gap test and the spread-return evidence are more informative than the level regressions because they try to separate channels. It is also a useful caution against dismissing flow effects on the basis of daily Granger tests.
- **Fragility — sample.** About 3.3 years of weekly data (≈170 observations) centred on a single boom and bust. Regressors are overlapping 13-week changes and the 4-week returns overlap, with Newey–West at only 5 lags. Standardized effects of 8% per SD on a 12.7%-vol return imply very large in-sample $R^2$, a classic small-sample, persistent-regressor setting. Later work on longer and post-2010 samples (e.g. Hamilton–Wu; Irwin–Sanders) largely failed to find comparable predictive power for index positions, so treat the magnitudes as episode-specific.
- **Fragility — measurement.** IIP13 is imputed from agricultural CIT positions scaled by index weights. As Stoll–Whaley note, imputed positions partly move with past prices. The control is only the $n$-week lagged return, not the 13-week return, so IIP13 may partly proxy for intermediate-horizon oil momentum. MMS13 is unsigned, which makes its positive level effect hard to interpret structurally.
- **Identification.** Predictability is not causality. Flows could respond to the same news or disagreement that drives premia, and the paper is explicit that it cannot separate price pressure, learning and correlated beliefs. The differences-of-opinion theory motivates the regressions but generates no tested restrictions.
- **Practical relevance for a quant PM.** Treat institutional positioning (index AUM, managed-money spreads) as a state variable for oil *risk*: flow-driven drift, curve-slope pressure around rolls, and funding-sensitive premia. Do not treat it as a stable alpha signal. The robust takeaways are qualitative: open interest is uninformative without knowing whose positions drive it; hedge-fund spread activity affects curve shape along the whole curve; and dealer balance-sheet capacity matters at weekly horizons.
