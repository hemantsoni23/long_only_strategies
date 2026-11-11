# Risk Premia and the VIX Term Structure — Travis L. Johnson (JFQA 2017) — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Author** | Travis L. Johnson (UT Austin, McCombs); based on his Stanford dissertation |
| **Journal** | *Journal of Financial and Quantitative Analysis* 52(6), Dec. 2017, pp. 2461–2490; doi 10.1017/S0022109017000825 |
| **Data** | OptionMetrics SPX options, 1996–2013 (4,445 days); CBOE VIX futures 2004–2013 (2,375 days) |
| **Source file** | `Finance/Risk Premia and the VIX Term Structure (Journal of Financial and Quantitative Analysis, vol. 52, issue 6) (2017).pdf` |

---

## Question and answer in one paragraph

Does the shape of the VIX term structure reflect expected future volatility (the expectations hypothesis, EH) or maturity-specific variance risk premia (VRP)? EH is rejected in all 10 specifications. The second principal component of the VIX² curve, SLOPE, negatively predicts next-day and next-month excess returns of 18 variance assets (synthetic variance swaps, VIX futures, ATM straddles; 6 maturities each). The other five PCs, including LEVEL, add essentially nothing. The paper frames this as the variance analogue of Cochrane–Piazzesi (2005), but with a more conservative factor choice: PC2 is picked informally, not estimated in a first-stage return regression.

## Construction

- **VIX term structure:** CBOE methodology applied at $T=1,2,3,6,9,12$ months, $VIX^2_{T,t}=\frac{2e^{rT}}{T}\sum_i \frac{\Delta K_i}{K_i^2}\,\text{OTM}_t(K_i;t+T)$, which equals $\frac1T E^Q_t\!\int_t^{t+T}\sigma_s^2ds$ for a diffusion.
- **PCA on $VIX^2$** (not vol, because variances aggregate linearly over horizons). Table 1: LEVEL explains 94.89% of variance and SLOPE 4.47%; CURVE and PC4–6 explain 0.30%, 0.15%, 0.12% and 0.07%.
  - SLOPE loadings on $VIX^2_{1,2,3,6,9,12}$: $-0.57,-0.24,-0.01,+0.30,+0.44,+0.58$.
  - The positive loadings dominate. This is deliberate: a zero-sum slope would be negatively correlated with LEVEL, because mean reversion makes the curve invert when vol is high. So SLOPE can be positive on a strictly decreasing curve, and only high-vs-low comparisons are meaningful.
- **Level statistics:** Mean VIX1 is 21.7% vs 22.7% for VIX12 (upward sloping on average). Std is 8.5% vs 6.1%, and the 99th percentile is 54.5% vs 41.5%.
- **Dynamics (Figure 1):** In calm periods SLOPE is high and positively correlated with LEVEL. In crises LEVEL spikes and SLOPE collapses; in 2008 it fell almost 10 SD below its mean. The correlation between the two is zero by construction.
- **Test assets:**
  1. Constant-maturity synthetic variance swaps: daily returns of the VIX replicating OTM-option portfolio, interpolated between the two expiries nearest $T$.
  2. Constant-maturity VIX futures at 1–6 months. The 1-month series has 96% correlation with VXX.
  3. Constant-maturity ATM SPX straddles.
  - Monthly returns compound the daily ones. Pairwise correlations are mostly 0.5–0.8, so the assets carry different risks.
- **Why asset returns rather than implied minus realized variance:** Implied minus realized at maturity $T$ averages premia over the whole horizon to $T$. Returns hold the holding period fixed across maturities and do not depend on a physical-variance model.

## Unconditional premia (Table 2)

| | 1m | 12m |
|---|---|---|
| Var swap, daily mean / ann. Sharpe | −1.36% / −1.44 | −0.08% / −0.29 |
| Var swap, monthly mean | −18.31% | −1.37% |
| VIX futures (1m, 6m), monthly mean | −3.78% (1m) | −2.28% (6m) |
| Straddle, monthly mean | −5.29% | +0.13% |

- All 18 assets have positive $\beta_{VIX}$ and negative alpha in the Ang et al. (2006) regression $r_i-r_f=\alpha_i+\beta_{i,MKT}(r_M-r_f)+\beta_{i,VIX}\Delta VIX_1+\epsilon$.
- The premium shrinks with maturity (as in Dew-Becker et al. 2017 and Eraker–Wu 2014), and the relation between $\beta_{VIX}$ and the premium is nonlinear.

## Expectations hypothesis (Table 3)

If there are no jumps, $E^Q_t(VIX^2_{m,t+k})=VIX^2_{k+m,t}+\frac{k}{m}(VIX^2_{k+m,t}-VIX^2_{k,t})$. EH adds a constant premium $a$ and implies slope $b=1$ in regressions of realized decay ($VIX^2_{m,t+k}-VIX^2_{k+m,t}$) or change ($VIX^2_{m,t+k}-VIX^2_{m,t}$) on the EH-implied move. Tests use $(k,m)\in\{(1,1),(1,2),(3,3),(3,6),(3,9)\}$, with Newey–West lags equal to 1.5× the overlap.

- **Decay regressions:** $\hat b$ ranges from −0.30 to +0.32.
- **Change regressions:** $\hat b$ ranges from 0.23 to 0.65. EH is rejected everywhere (p ≤ 4.6%).
- **Controlling for current $VIX^2_m$:** the control loads at about −0.25 to −0.51 (mean reversion), and $\hat b$ becomes negative or insignificant, e.g. 0.064 and 0.001 in the quarterly change regressions.
- **Reading:** The curve's apparent forecasting power is just a noisy proxy for mean reversion, so its shape must reflect time-varying risk premia. (Mixon 2007 reached the same conclusion with BS implied vols.)

## Single-factor tests (Table 4)

The regression is $r_{i,t+1}-r_f=a_i+PC_t\lambda_i+\epsilon$, with PCs scaled to unit SD. A $\chi^2$ test checks that every $\lambda$ except SLOPE is zero.

- **SLOPE coefficient:** negative in 36/36 regressions (3 assets × 6 maturities × 2 horizons) and significant in 33. The single-factor null is rejected in only 8/36, mostly because of PC5 (0.12% of curve variance), whose sign is inconsistent.
- **Next-day effect sizes** (per 1 SD of SLOPE): variance swaps −55 to −60 bps at 1–3 months and −19 bps at 12 months. Straddles −37 bps (1m) to −15 bps (12m). VIX futures −31 bps (1m).
- **Next-month SLOPE-only adjusted $R^2$:**
  - VIX futures: 6.2–16.5%.
  - Straddles: 3.8–12.1%.
  - Variance swaps: 1.0–9.5%.
  - Daily $R^2$ is ≤ 1.6%.
- **Out of sample:** OOS $R^2$ excludes overlapping observations, so it uses both past and future data and is not a real-time test. SLOPE-only OOS $R^2$ beats the 6-PC model in 33/36 cases, because the full model overfits collinear predictors. For next-month straddles it is 2.3–10.4%.

## Economic magnitude and nonlinearity (Table 5)

- **Next-day high-minus-low SLOPE quintile spread:** 29–181 bps. Variance swaps −0.72% to −1.81%, VIX futures −0.29% to −0.83%, straddles −0.40% to −1.09%. All are significant except 6-month VIX futures.
- **Next-month spread:** 7.4%–36.4% in the introduction; Table 6's extremes run from −8.25% to −36.67%. All 18 assets are significant at 1%.
- **Nonlinear shape:** The relation is mild across quintiles 2–5 and concentrated in the bottom quintile. There, 17 of 18 assets have *positive* mean excess returns (10 significant). For example, 12-month straddles earn about +29–30 bps/day, and 3-month variance swaps +0.60%/day. The VRP changes sign: when the curve is most inverted relative to normal, owning variance was rewarded.

## Robustness (Tables 6–7)

- **Subsamples:** The spreads shrink but stay significant after excluding 2008–09 or dropping the bottom 5% of SLOPE days. For example, straddle spreads fall from −1.09% to −0.94% at 1m and from −0.40% to −0.35% at 12m. SLOPE still predicts at $t+2$.
- **Naive slope definition:** $VIX^2_{12}-VIX^2_1$ still predicts but more weakly, because it is 68% negatively correlated with LEVEL. The author suggests $2VIX^2_{12}-VIX^2_1$ as a better simple proxy.
- **Incremental tests (next day, Table 7):** SLOPE survives controls for own lagged return (measurement error or reversal), a 21-day crash dummy, $VIX^2_1$, implied-minus-expected variance (Drechsler–Yaron style, using a 5-minute realized-variance forecast), model-free implied skewness, Hu–Pan–Wang NOISE and broker-dealer leverage. It stays significant for all straddles, 5 of 6 variance swaps and the 1–2 month VIX futures.
  - Implied-minus-expected variance is itself an incremental negative predictor for 11 of 18 assets.
  - $VIX^2_1$ is insignificant or positive, which confirms LEVEL does not predict.
  - Post-crash premia, if anything, get smaller.
- **Equity returns:** Untabulated tests show SLOPE does not predict equity returns, even though it correlates positively with implied minus expected variance. The equity predictability found with the VIX curve by Bakshi et al. (2011) and Feunou et al. (2014) comes from other PCs.

## Trading illustration (Figure 2)

- **Setup:** Real-time PCA with a 1996–1999 training period. Buy 30-day straddles when SLOPE is in its historical bottom quintile; otherwise short them with 20% Reg-T margin. Daily rebalancing, 2000–2013.
- **Result:** Terminal wealth is 4.8× that of always-short, or +11.9% per year.
- **Caveats:**
  - Returns use mid quotes, so they overstate what is achievable.
  - A large share of the gain comes from being long in late 2008.

## Puzzles posed

1. LEVEL does not predict VRP, contrary to Heston-type models, Bakshi–Madan, ICAPM/Merton, Martin (2013) and Campbell et al. (2017).
2. Unconditional premia are largest at short maturities, yet conditional premia are largest when short-dated variance is *cheap* relative to long-dated variance, i.e. the curve is steep.
3. The VRP flips sign in the lowest SLOPE quintile, which requires large time variation in either exposure to variance risk or its price.

Possible explanations the author leaves open: a variance risk factor outside Bollerslev–Tauchen–Zhou / Drechsler–Yaron, or non-risk channels such as demand pressure (Gârleanu–Pedersen–Poteshman 2009) or mispricing.

## Assessment

- **Convincing:**
  - The EH rejection is clean.
  - Consistent signs across 36 regressions on three asset families with different construction and noise; the VIX futures are traded separately from the options behind SLOPE, which rules out a shared-measurement-error artifact.
  - Rotation-invariant: untabulated tests using the raw 6-tenor curve give the same result, and restricted-model OOS $R^2$ beats the unrestricted model.
- **Fragile:**
  - Only 18 years of data, dominated by 2008. The action sits in the bottom SLOPE quintile, a regime of a few crisis episodes, and the sign flip rests on a handful of crashes.
  - Daily $R^2$ is tiny and the next-month tests use heavily overlapping data (Newey–West with 32 lags).
  - The baseline uses full-sample PCA loadings.
  - Synthetic variance swaps are noisy, and the trading test uses mid prices and daily straddle turnover. Real bid–ask spreads, especially for long straddles in stress, would eat a lot of the 29–181 bps/day.
  - VIX futures only begin in 2004.
- **Practical relevance:**
  - SLOPE is a timing signal for short-vol programs: size by LEVEL/risk budget, time with SLOPE. The actionable rule is regime-like — de-risk or flip long when the curve is abnormally inverted given its level — rather than a linear tilt.
  - The recommended low-cost proxy is $2VIX^2_{12}-VIX^2_1$. A simple VIX-minus-VIX1 spread (e.g., VIX3M/VIX) mixes in LEVEL.
  - In practice, check that the low-SLOPE effect survives execution costs and post-2013 data (e.g., Feb 2018 and March 2020), which this paper does not cover.
