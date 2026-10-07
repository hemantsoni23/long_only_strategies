# Downside Risk

**Andrew Ang, Joseph Chen, Yuhang Xing · 2006 · Review of Financial Studies 19(4), 1191–1239 · Source file `Finance/AbnormalReturnsDownsideRisk_AngChenXin_2006.pdf` (NBER WP 11824 version also in `Finance/Downside Risk.pdf`) · Data: CRSP NYSE stocks, daily returns, Jul-1963 – Dec-2001 (451 overlapping 12-month windows); robustness adds AMEX/NASDAQ**

## Claim
Stocks that covary strongly with the market *when the market falls* earn higher average returns. The Fama–MacBeth premium per unit of downside beta is **≈6% p.a.** (0.056–0.069; 0.028 once coskewness is controlled). It is not explained by regular beta, size, B/M, past returns, volatility, coskewness, cokurtosis or Pástor–Stambaugh liquidity beta. The upside-beta *discount* predicted by theory is weak and fragile. Past downside beta predicts next-month returns only after dropping the most volatile stocks.

## Theory: disappointment aversion (Gul 1991)
The certainty equivalent $\mu_W$ solves
$$U(\mu_W)=\frac1K\Big(\int_{-\infty}^{\mu_W}U(W)\,dF(W)+A\int_{\mu_W}^{\infty}U(W)\,dF(W)\Big),\qquad K=\Pr(W\le\mu_W)+A\Pr(W>\mu_W),$$
with power felicity $U(W)=W^{1-\gamma}/(1-\gamma)$ and $0<A\le1$. $A=1$ is CRRA, which is locally mean–variance, so the downside premium is negligible. $A<1$ gives first-order aversion to disappointing outcomes and a kink at an endogenous reference point.
- **Calibration:** two assets, six states, $\gamma=6$, $A=0.8$, $R_f=1.05$. CAPM alpha increases in $\beta^-$ and in $\beta^--\beta$, and decreases in relative upside beta.
- **Coskewness is not a sufficient proxy.** It comes from a Taylor expansion of a non-smooth utility. The appendix gives a calibration where CAPM alpha *rises* with coskewness, contrary to the Taylor-expansion prediction.

## Risk measures
All are computed with daily log excess returns over the same 12-month window as the returns (Bawa–Lindenberg):
$$\beta^-=\frac{\text{cov}(r_i,r_m\mid r_m<\mu_m)}{\text{var}(r_m\mid r_m<\mu_m)},\qquad \beta^+=\frac{\text{cov}(r_i,r_m\mid r_m>\mu_m)}{\text{var}(r_m\mid r_m>\mu_m)},$$
- relative downside beta $\beta^--\beta$, relative upside beta $\beta^+-\beta$;
- coskew $=\dfrac{E[(r_i-\mu_i)(r_m-\mu_m)^2]}{\sqrt{\text{var}(r_i)}\,\text{var}(r_m)}$, cokurt $=\dfrac{E[(r_i-\mu_i)(r_m-\mu_m)^3]}{\sqrt{\text{var}(r_i)}\,\text{var}(r_m)^{3/2}}$.

The market is all NYSE stocks. Cross-sectional correlations: corr($\beta,\beta^-$) = 0.78, corr($\beta,\beta^+$) = 0.76, corr($\beta^-,\beta^+$) ≈ 0.46. Cutoffs at $\mu_m$, $r_f$ or 0 give $\beta^-$ versions correlated above 0.96, with identical results.

**Design.** The main tests are *contemporaneous*: sort on realized loadings over $[t,t+12]$ and measure realized returns over the same window (Black–Jensen–Scholes / Fama–French 1992 logic, higher power with daily data and short windows). Portfolios are equal-weighted NYSE quintiles. Overlapping monthly windows use Newey–West with 12 lags.

## Main results
**Contemporaneous quintile sorts (Table 1, excess return p.a., Q5−Q1):**

| Sort | Q1 | Q5 | Q5−Q1 | t |
|---|---|---|---|---|
| $\beta$ | 3.52% | 13.95% | 10.43% | 4.98 |
| $\beta^-$ | 2.71% | 14.49% | 11.78% | 6.16 |
| $\beta^--\beta$ (β flat: 0.98 → 0.98) | 4.09% | 10.73% | **6.64%** | 7.70 |
| $\beta^+$ | 5.73% | 9.83% | 4.11% | 2.62 |
| $\beta^+-\beta$ | 10.48% | 4.37% | −6.11% | 9.02 |
| $\beta^+-\beta^-$ | 11.35% | 3.55% | −7.81% | 9.03 |

**Fama–MacBeth, 12-month returns on realized loadings (Table 2; 1,080–1,582 stocks/month; regressors winsorized 1/99%):**

| | II | III (+size, B/M, past ret) | IV (+coskew) | V (+vol, coskew, cokurt) | VI (+liq. beta, 1967–) |
|---|---|---|---|---|---|
| $\beta^-$ | 0.069 [7.17] | 0.064 [7.44] | 0.028 [2.68] | 0.062 [6.00] | 0.056 [5.25] |
| $\beta^+$ | −0.029 [4.85] | −0.025 [4.15] | 0.003 [0.22] | 0.020 [2.33] | 0.017 [1.91] |

- Cross-sectional SD of $\beta^-$ is 0.74, so a 2σ move is worth $2\times0.069\times0.74=10.2\%$ p.a.
- Controls: coskewness is −0.188 [4.59] in VI (2σ ≈ 7.1% p.a.). Realized volatility is strongly negative (−8.4 [10.7] in regression I).
- The upside discount appears only in II–III, and $\beta^+$ flips to *positive* in V–VI. Liquidity beta is insignificant.

**Downside beta vs coskewness (Table 3, 5×5 double sorts):**
- $\beta^-$ spread controlling for coskewness: 7.55% p.a. [4.16]. The spread is largest in the most negatively coskewed quintile (14.64%) and insignificant in the highest (2.10%, t = 1.32).
- Coskewness spread controlling for $\beta^-$: −6.22% [8.17].
- The two are distinct: coskewness loads on market *volatility* in both tails, while $\beta^-$ conditions only on declines.

**Robustness (Table 5, $\beta^-$ Q5−Q1 p.a.):**

| Variant | Q5−Q1 | t |
|---|---|---|
| Excluding the smallest size quintile | 8.34% | 4.54 |
| 2-year weekly betas (24-month returns) | 22.27% | 4.96 |
| Value-weighted | 7.14% | 3.30 |
| All NYSE/AMEX/NASDAQ | 15.24% | 5.57 |
| Non-overlapping calendar years | 12.46% | 3.51 |

For relative $\beta^-$ the value-weighted spread is 3.99% [3.06]. A Scholes–Williams-type nonsynchronous-trading correction does not change the results.

**FF25 portfolios (Table 6, GMM SDF).** Adding $r_m^-=\min(r_m,\mu_m)$ to the CAPM or FF3 SDF is significant. The J-difference test rejects CAPM (χ² = 3.85, p = 0.05) and FF3 (χ² = 9.49, p ≈ 0.00) in favour of including downside market risk.

## Predictability (the investable part)
- **Persistence.** 12-month autocorrelation is 0.675 for $\beta$, 0.435 for $\beta^-$ and only 0.082 for relative $\beta^-$.
- **Determinants of future relative $\beta^-$** (Table 7): higher for small, high-vol and high-ROE stocks, and for **past winners** (past-return coefficient 0.052, t = 4.85). The past-winner effect links the paper to momentum-crash risk. Utilities have lower downside exposure.
- **Unconditional sort on past $\beta^-$ (Table 8):**
  - The realized $\beta^-$ spread shrinks to 0.80, vs 1.72 in the contemporaneous sort.
  - Next-month returns are 0.59% (Q1) to 0.84% (Q4) per month, but Q5 falls back to 0.70%. The Q5−Q1 spread of 0.11% (t = 0.60) is **not significant**.
  - Past coskewness does predict returns (−0.28%/mo, t = 2.76), but not through future $\beta^-$.
- **Excluding the top past-volatility quintile** (3.9% of market cap; average vol 61% vs 36% for all stocks; $\beta^-$ autocorrelation 25.8%):
  - Q5−Q1 is **0.34%/mo [2.31]** and Q4−Q1 is 0.25% [2.28].
  - Size/B/M-adjusted Q5−Q1 is 0.44% [3.36].
  - Adding momentum, coskewness or liquidity controls gives 0.32%, 0.36% and 0.30% (t = 2.15–2.71).
  - A volatility × past-$\beta^-$ double sort averages 0.31% [3.14]; the spread is insignificant only in the top-vol quintile.
- **Mechanism:** $\beta^-=\rho^-\sigma_i^-/\sigma_m^-$. High $\beta^-$ driven by high $\sigma_i^-$ runs into the Ang–Hodrick–Xing–Zhang low-return-to-high-vol effect, and noisy estimates in volatile names destroy predictability.

## Critical assessment
- **The ~6% "premium" is a contemporaneous risk–return relation, not a tradable spread.** Sorting on *realized* $\beta^-$ partly selects stocks that did badly in down markets and well otherwise. The authors argue this is not mechanical, but the investable version is much smaller: ~0.3–0.44%/mo on a restricted universe, with simple t-stats of about 2–3.
- **Sensitive to coskewness controls.** The $\beta^-$ coefficient falls from 0.064 to 0.028 when coskewness enters (regression IV), though it rebounds with volatility and cokurtosis added.
- **Equal weighting and small caps.** Main results are EW on NYSE. VW spreads are smaller (7.1% vs 11.8%), and the "all stocks" universe inflates them.
- **Weak upside evidence.** The theory's upside discount is not robust. Excluding the high-vol quintile is ex post motivated, though it covers little market cap.
- **Transcription inconsistency:** the text says the past relative-$\beta^-$ coefficient in Table 7 regression I is 0.077, but the table prints 0.007.
- **Sample ends in 2001** (no 2008). No transaction costs.

## Practical relevance for a quant PM
- **Risk diagnostic.** Estimate $\beta^-$ and relative $\beta^-$ from 12 months of daily data (or 2 years of weekly) for positions and factor portfolios. Momentum/winner portfolios carry positive relative downside beta, one reason momentum crashes in down, rebounding markets.
- **Alpha signal.** Past $\beta^-$ is a weak standalone predictor. Use it only after removing the top-volatility quintile or orthogonalising to volatility, and expect ~3–5% p.a. gross long–short, largely overlapping with low-vol/BAB and coskewness exposures.
- **Portfolio construction.** Beta-neutral is not downside-neutral. Constraining $\sum_i w_i(\beta_i^--\beta_i)$ reduces left-tail market exposure, and the downside risk premium is what you give up for that protection.
