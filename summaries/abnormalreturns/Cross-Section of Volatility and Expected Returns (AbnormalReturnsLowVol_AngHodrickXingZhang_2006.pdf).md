# The Cross-Section of Volatility and Expected Returns — Ang, Hodrick, Xing & Zhang (2006) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | The Cross-Section of Volatility and Expected Returns |
| **Authors** | Andrew Ang (Columbia, NBER); Robert J. Hodrick (Columbia, NBER); Yuhang Xing (Rice); Xiaoyan Zhang (Cornell) |
| **Journal** | *Journal of Finance*, Vol. LXI, No. 1, February 2006, pp. 259–299 |
| **Sample (aggregate vol)** | January 1986 – December 2000 (VIX availability) |
| **Sample (idio vol)** | July 1963 – December 2000 |
| **Universe** | AMEX, NASDAQ, NYSE common stocks; value-weighted quintiles throughout |
| **Key instruments** | ΔVIX (old CBOE VIX on S&P 100, now VXO); mimicking factor FVIX; Coval–Shumway straddle factor STR |
| **Source file** | `Finance/AbnormalReturnsLowVol_AngHodrickXingZhang_2006.pdf` |
| **Drive file_id** | `0B-6kBz0I0dMsSHFwanJUSi11Rlk` |

---

## Questions

1. **Is aggregate volatility risk priced in the equity cross-section?** ICAPM logic (Campbell 1993/96; Chen 2002, where investors hedge shocks to *future market volatility* via precautionary saving), the correlation between volatility spikes and market drops, and coskewness preferences all imply a negative price. Option studies already find one, but they cannot control for size, value, momentum, or liquidity.
2. **How is idiosyncratic volatility, measured relative to FF-3, priced?** If aggregate volatility is an omitted factor orthogonal to FF-3, FF-3 residual volatility should partly reflect volatility betas and thus earn *low* returns. Merton (1987), undiversified-risk arguments, and Barberis–Huang predict the *opposite* (a positive premium), as did earlier evidence (Lintner 1965, Lehmann 1990, Tinic–West 1986, Malkiel–Xu 2002). Those studies used portfolio-level or beta/size-portfolio idiosyncratic risk rather than firm-level sorts.

## Part I: Systematic volatility risk

### Design

- ΔVIX (daily first difference) proxies for volatility innovations. VIX averages 20.5% (sd 7.85%) with AR(1) of 0.94; ΔVIX has sd 2.65% and AR(1) ≈ 0. Caveats: VIX mixes volatility with the volatility risk premium and includes jump risk.
- **Pre-formation regression** (daily data over one month, at least 17 observations):
$$r^i_t = \beta_0 + \beta^i_{MKT}MKT_t + \beta^i_{\Delta VIX}\,\Delta VIX_t + \varepsilon^i_t .$$
SMB and HML are excluded here to limit noise and are controlled for ex post. Stocks are sorted monthly into value-weighted quintiles on $\beta_{\Delta VIX}$ and held for one month.
- **FVIX** (Breeden–Gibbons–Litzenberger / Lamont tracking portfolio): each month, regress daily ΔVIX on the five $\beta_{\Delta VIX}$ quintile excess returns, $\Delta VIX_t = c + b'X_t + u_t$; FVIX $= b'X_t$. Because $b$ is estimated in-month, **FVIX uses future information and is not investable**; it is a device for measuring *ex post* exposure at monthly frequency (monthly ΔVIX is a poor innovation proxy because the conditional mean matters). Correlation with daily ΔVIX is 0.91. Monthly correlations: ΔVIX 0.70, STR 0.83, MKT −0.66, SMB −0.14, HML 0.26, UMD −0.25, Pástor–Stambaugh LIQ −0.40.
- Factor-risk criteria: (i) ex post, full-sample FVIX loadings must line up with the sorts' returns; (ii) the effect must survive characteristic and factor controls.

### Results (Table I and robustness)

- Pre-formation $\beta_{\Delta VIX}$ runs from −2.09 (Q1) to +2.18 (Q5). The **5−1 raw spread is −1.04%/month**, the CAPM alpha spread −1.15%, and the FF-3 alpha spread −0.83%. All are significant at 1%, and joint alpha tests reject. Q5 has a mean of 0.60% and an FF-3 alpha of −0.53% (t −2.88).
- Next-month betas are nearly flat (−0.033 to 0.018): conditional betas are noisy. Full-sample post-formation FVIX betas (FF-3 + FVIX regression) run from −5.06 to 8.07, jointly p < 0.001.
- **Formation window:** longer windows weaken the effect. With 3 months, the Q5 FF-3 alpha is −0.37 (t −1.62); with 12 months, −0.24 (t −1.04). Turnover of the 1-month sort exceeds 70%. The timely conditional beta is what matters.
- **Innovation model:** AR(1) innovations give a 5−1 of −1.08 (FF-3 −0.90); BIC-selected AR(11) gives −0.81 (−0.66).
- **Small growth:** excluding the FF smallest-growth cell cuts the 5−1 to −0.63 (t −3.30) and the FF-3 alpha to −0.44 (t −1.79, insignificant). DGTW size/B/M characteristic matching gives −0.90 (t −3.59), or −0.64 excluding small growth (t −3.75). Small growth stocks explain part, not all.
- **Double sorts:** controlling for liquidity beta gives a 5−1 of −0.68 (FF-3 −0.55, t −2.15); volume gives −0.72 (FF-3 −0.58); past 12-month return gives −0.89 (FF-3 −0.74). FVIX-beta monotonicity survives each control.

### Price of volatility risk (Table V)

Fama–MacBeth on 25 portfolios double-sorted on past $\beta_{MKT}$ and then $\beta_{\Delta VIX}$, with full-sample betas and errors-in-variables-robust t-stats:

| Spec | $\lambda$ (%/month) | t |
|---|---|---|
| FF-3 + FVIX | −0.080 | −2.49 |
| FF-3 + STR (1986–95) | −0.194 | −2.32 |
| + UMD | −0.082 | −2.39 |
| + UMD + LIQ | −0.071 | −2.02 |

MKT, SMB, and HML premia are imprecise, and SMB and HML are negative in this period. **Accounting check:** ex post FVIX beta spread 13.13 × (−0.080) = −1.05%, essentially the whole −1.04% raw spread.

**Peso caveat (the authors').** FVIX returned 134% in October 1987 and 33.6% in August 1998. At −0.08%/month the cumulative FVIX premium over 180 months is only −14.4%, so *one more* August-1998-sized spike would flip its sign. Power-law crash frequencies suggest about three large crashes would be expected in such a sample. The sample thus may contain *fewer* spikes than agents expected, which makes the estimated price too negative. The −1% p.a. estimate "must be interpreted with caution."

## Part II: Idiosyncratic volatility

**Definition:** $\mathrm{ivol}_{i} = \sqrt{\mathrm{var}(\varepsilon_{i,d})}$ from daily FF-3 regressions over the formation window. Strategies are L/M/N (estimation / wait / hold, months), value-weighted; the base case is 1/0/1. Using CAPM residuals instead gives quintile returns correlated above 0.99 with the FF-3 versions.

### Table VI (1963–2000, monthly %)

| Quintile | Total vol: mean / FF-3 α | Ivol: mean / FF-3 α | Ivol mkt share |
|---|---|---|---|
| 1 | 1.06 / 0.03 | 1.04 / 0.04 | 53.5% |
| 3 | 1.22 / 0.12 | 1.20 / 0.08 | 11.9% |
| 4 | 0.99 / −0.17 | 0.87 / −0.32 | 5.2% |
| 5 | 0.09 / −1.16 (t −6.85) | **−0.02 / −1.27 (t −7.68)** | 1.9% |
| 5−1 | −0.97 (t −2.86) / −1.19 (t −5.92) | **−1.06 (t −3.10) / −1.31 (t −7.00)** | |

The relation is flat to mildly increasing through Q3 and then collapses; the anomaly lives in Q4–Q5. High-ivol stocks are small with high B/M, so FF-3 predicts *higher* returns and risk adjustment deepens the puzzle.

### Controls (Table VII, 5−1 FF-3 α, %/month)

| Control | 5−1 α (t) |
|---|---|
| NYSE only | −0.66 (−4.85) |
| Size (averaged over size quintiles) | −1.04 (−5.69) |
| B/M | −0.80 (−2.90) |
| Leverage | −1.23 (−7.61) |
| PS liquidity beta | −1.08 (−7.98) |
| Volume | −1.22 (−8.04) |
| Turnover | about −1.2 to −1.5, t > 8 |
| Bid–ask spread | −1.19 (−6.95) |
| Coskewness | −1.38 (−5.02) |
| Analyst dispersion (1983–2000) | −0.39 (−2.09) |

The ivol effect is **not a micro-cap effect**. Within size quintiles, 5−1 alphas are −0.55 (smallest, t −1.84), −1.91, −1.61, −0.86, and −0.26 (largest, t −1.74): it is concentrated in size quintiles 2–4 (about 21% of market cap) and insignificant in both extremes. Analyst dispersion absorbs much of it in the covered (larger-firm) universe. Conversely, controlling for ivol makes the Diether–Malloy–Scherbina dispersion effect insignificant (−0.36, t −1.47).

### Momentum (Table VIII)

Controlling for past 1-, 6-, and 12-month returns gives 5−1 alphas of −0.66, −1.10, and −1.22. The effect appears in every momentum quintile but is strongly asymmetric: −2.25 among losers and −0.48 among winners. Conversely, momentum is symmetric in low-ivol stocks (loser/winner α −0.41/+0.45) but skewed toward very negative loser returns at high ivol. Shorting high-ivol losers is the sharpest version of both anomalies.

### Aggregate volatility does not explain it (Table IX, 1986–2000)

Controlling for $\beta_{\Delta VIX}$, the 5−1 alpha is −1.19 (t −4.72), versus −1.31 unconditionally. Ex post FVIX loadings rise with ivol only in the three lowest $\beta_{\Delta VIX}$ quintiles, so aggregate volatility exposure explains at most a sliver.

### Horizons and subsamples (Tables X–XI)

- 1/1/1: 5−1 alpha −0.88 (t −4.63), so it is not a same-month measurement artifact. 1/1/12: −0.67; 12/1/1: −1.12; 12/1/12: −0.77. No long-horizon reversal into a positive premium, and not driven by short-term events such as earnings announcements.
- By decade: −1.00 (1963–70), −0.77 (1970s), −2.23 (1980s), −1.55 (1990s).
- NBER expansions −1.25 (t −6.55), recessions −1.79.
- Stable months (lowest 20% |market return|) −1.71; volatile months −0.89. The anomaly is strongest in calm markets, which argues against a bear-market or crash-peso story.

## Assessment

- **Convincing:**
  - The ivol result is robust: firm-level sorts, value weighting, many controls, all decades, formation/holding variations, and t-stats of 5–10. It overturned the prior "positive idiosyncratic risk premium" literature.
  - The ΔVIX sort's full spread is matched by $\lambda \times \Delta\beta_{FVIX}$, a clean internal-consistency check for Part I.
- **Fragile:**
  - Part I rests on 15 years with two volatility spikes. The price of risk is small, peso-sensitive, and uses a non-investable, in-sample mimicking factor.
  - The ΔVIX sort weakens substantially with 3–12 month betas and is partly explained by small growth stocks and liquidity. A negative price of volatility risk is plausible, but this is weak evidence for its magnitude.
  - The ivol short leg is only about 2% of market cap and sits in names with high idiosyncratic risk, likely short-sale frictions, and high one-month signal turnover. The paper reports gross alphas with no costs. The analyst-dispersion result hints at a Miller (1977) disagreement/short-constraint channel, which the paper does not pursue.
  - Later work (not in this paper) debated whether the effect is driven by one-month return reversal, lottery demand, or microstructure. The paper's 1/1/1 and 12/1/1 results partly address this.
- **Practical relevance for a quant PM:**
  - Treat the two results separately. (i) Volatility beta is a candidate risk-model factor with a hedging interpretation (positive-FVIX-beta names outperform in volatility spikes). Measure it on a short, timely window, and do not expect a reliable premium to harvest. (ii) Residual volatility is a negative expected-return characteristic, strongest among losers and mid-caps and weak among the largest stocks. It is best used as a short-side or avoidance screen, or as an input to a multivariate characteristic model.
  - Ivol is correlated with size, momentum, and dispersion signals, so residualize against them. Longer estimation windows (12/1/1) retain most of the alpha at much lower turnover.
  - "Low volatility" is not one knob: low systematic volatility beta and low residual volatility are empirically distinct.
