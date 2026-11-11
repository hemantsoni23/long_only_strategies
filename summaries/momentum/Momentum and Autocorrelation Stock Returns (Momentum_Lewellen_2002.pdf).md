# Momentum and Autocorrelation in Stock Returns

**Jonathan Lewellen (MIT Sloan) · 2002 · *Review of Financial Studies* 15(2), 533–563 · Source file `Finance/Momentum_Lewellen_2002.pdf` · CRSP NYSE/AMEX/Nasdaq common stocks, Jan 1941–Dec 1999 (B/M portfolios May 1963–Dec 1999, Compustat, 3-yr history required); mostly value-weighted portfolios, NYSE breakpoints**

## Claim / contribution
1. **Size and B/M portfolios show momentum as strong as individual stocks and industries.** These are 5/10/15 size or B/M portfolios and 9/16/25 size-B/M. They are extremely diversified: on average 347 stocks per size decile, 199 per size-B/M cell, 231 per industry. Their momentum is therefore *macroeconomic*, not firm-specific.
2. Stock, industry and size/B/M momentum are **distinct**: benchmark-adjusting one leaves the others intact.
3. Industry, size and B/M portfolios are **negatively** auto- *and* cross-serially correlated at 1–18 month lags. Momentum arises because the cross-serial (lead-lag) term dominates, not because returns are persistent.
4. The explanation Lewellen favors is **excess covariance** (prices covary more than dividends), from either cross-firm overreaction or a time-varying market risk premium. Firm- or portfolio-specific underreaction is not favored.

## Setup
**Strategy** (Lo–MacKinlay weights on 12-month formation returns, rescaled to \$1 long/\$1 short, held months 1–18):
$$w_{i,t}=\tfrac1N\big(r^{12}_{i,t-1}-r^{12}_{m,t-1}\big),\qquad m=\text{equal-weighted index}.$$
Every asset gets a nonzero weight, which suits 5–25 portfolios and ties profits to autocovariances.

**Lo–MacKinlay decomposition** ($\Omega=E[(r_{t-1}-\mu)(r_t-\mu)']$):
$$E[\pi_t]=\frac{N-1}{N^2}\operatorname{tr}(\Omega)\;-\;\frac1{N^2}\big[\iota'\Omega\iota-\operatorname{tr}(\Omega)\big]\;+\;\sigma^2_\mu .$$
The three terms are Auto (+ if own autocovariance > 0), Cross (+ if cross-serial covariances < 0) and Means. For 12-month formation, $\Omega_k=E[(r^{12}_t-\mu^{12})(r_{t+k}-\mu)']$ and the last term becomes $\sigma_{\mu^{12},\mu}$.
**Identity (Eq. 7):** with $s_{i,t}=r_{i,t}-r_{m,t}$, $E[\pi_t]=\frac1N\sum_i\operatorname{cov}(s_{i,t-1},s_{i,t})+\sigma_\mu^2$. Momentum *is* persistence of asset-specific returns by construction. Finding such persistence therefore says nothing about underreaction versus excess covariance.

**Models.** Prices are split as $p_t=q_t+z_t$ with $q_t=\mu+q_{t-1}+\varepsilon_t$ (dividend news, $\operatorname{cov}\varepsilon=\Sigma$), so $r_t=\mu+\varepsilon_t+\Delta z_t$.
| Model | Temporary component | Lag-1 autocov | Momentum profit |
|---|---|---|---|
| Random walk | $z=0$ | 0 | $\sigma^2_\mu$ (small) |
| Underreaction | $z_t=-\delta\varepsilon_t-\delta^2\varepsilon_{t-1}-\dots$ | $\delta\frac{1-\delta}{1+\delta}\Sigma$ (positive) | $\delta\frac{1-\delta}{1+\delta}\big[\tfrac1N\operatorname{tr}\Sigma-\tfrac1{N^2}\iota'\Sigma\iota\big]+\sigma^2_\mu>0$ |
| Cross-firm overreaction | $\Sigma=\sigma^2I$; $z_t=\phi z_{t-1}+B\varepsilon_t$, $B=b(\iota\iota'-I)$, $0<b<1$ | $\sigma^2(\phi-1)\big[B+\tfrac{1}{1+\phi}BB\big]$, everywhere **negative** | Eq. (20): closed form in $b,\phi,N$, positive for $0<b<1$ (own reversal outweighed by stronger negative cross-serial terms) |
| Time-varying risk premium | $z_t=x_t\beta$, $x_t$ AR(1) with coefficient $\phi$ and autocov $\gamma_x<0$ of $\Delta x$; $\theta=\operatorname{cov}(\varepsilon_t,\xi_t)>0$ | $\gamma_x\beta\beta'+(\phi-1)\beta\theta'$, negative | $\gamma_x\sigma^2_\beta+(\phi-1)\sigma_{\beta\theta}+\sigma^2_\mu$; positive only if premium-sensitive assets (high $\beta_i$) have cash flows weakly tied to the premium (low $\theta_i$), e.g. through duration differences |

The two excess-covariance models give the same autocorrelation pattern: negative autos, negative cross-serials, momentum > 0. Telling them apart runs into the joint-hypothesis problem.

## Main results
**Table 2: raw momentum, % per month (t), selected post-formation months**
| Assets | m1 | m3 | m7 | m11 | m17 | Cum. first 6m (t) |
|---|---|---|---|---|---|---|
| Individual stocks | 0.500 (3.08) | 0.800 (5.03) | 0.098 | −0.333 (−2.61) | −0.508 (−4.51) | 3.55% (4.02) |
| 15 industries VW | 0.741 (6.62) | 0.497 | 0.327 (3.07) | 0.023 | −0.138 | 3.04% (4.75); EW 3.65% (5.62) |
| 5 size VW | 0.509 (4.65) | 0.341 | 0.446 (4.06) | 0.212 | 0.288 (2.64) | 2.56% (4.16); EW 3.02% |
| 10 B/M VW | 0.434 (3.54) | 0.382 | 0.272 | 0.223 | 0.154 | 2.14% (2.99); EW 4.61% (5.97) |
| 25 size-B/M VW | 0.799 (5.60) | 0.542 | 0.438 | 0.150 | 0.100 | 3.23% (4.18); EW 3.93% (4.93) |
- Stock and industry momentum lasts 7–9 months, then reverses. Size and B/M momentum decays slowly and is often significant through month 18.
- Coarse and fine sorts give nearly identical profits (5 vs 15 size, 5 vs 10 B/M, 9 vs 25 size-B/M), consistent with no idiosyncratic content.
- Sharpe ratio = $t/\sqrt T$: $t=4$ implies SR ≈ **0.15** monthly for the full sample and **0.19** post-1963, vs 0.18 for the CRSP VW index (1941–99).

**Table 3: benchmark-adjusted profits** (same weights):
- Stocks, first 6m: industry-adjusted **2.90%** ($t$=3.71), size-B/M-adjusted **3.69%** ($t$=4.69), vs 3.55% raw.
- Industries adjusted for size or size-B/M: VW m1 0.660 ($t$=6.37).
- Size and size-B/M portfolios, industry-adjusted: VW 5-size m1 0.453 ($t$=4.72); 25 size-B/M m1 0.711 ($t$=6.41).
- Industry significance drops slightly; size and B/M significance rises. Momentum exists at both micro and macro level.

**Table 4: serial correlations** (average over lags 1–18 of corr(12m past return, monthly return), VW; bootstrap tests):
- Almost all entries are negative, and about half are significant.
- Average auto −0.04, average cross −0.05 (SE ≈ 0.025 for industry/size, 0.033 for B/M).
- Industry: corr(annual, return 2 months later) −0.005 → −0.064 by month 10. Size and B/M reach ≈ −0.07 by month 10–11.
- Size-quintile autos are most negative for Q3/Q4 (−0.05/−0.07). Big stocks strongly predict the others: Big → Small = −0.10, and none of 5,000 bootstrap draws is that negative.

**Table 5: slope of monthly return on own lagged 12m return**
- Negative beyond month 1; month 1 is positive, attributed to weekly lead-lag.
- Size average: −0.007 (m2) → −0.019 (m10), SE ≈ 0.008. Industry average: −0.003 (m2) → −0.017 (m10), SE ≈ 0.007.
- Estimates are U-shaped in the lag, whereas profits decline monotonically.
- Economic size: annual σ is 20–25%, so a 2σ year with slope −0.01 moves the next month's expected return by 40–50 bp.
- Cumulative slopes, 6m/12m: size −0.043/−0.135; industry −0.023/−0.104; size-B/M −0.044/−0.112. The downward small-sample bias is ≈ −0.002.

**Table 6: Lo–MacKinlay decomposition** (industries, bootstrap SEs Auto 2.66, Cross 2.56, Means 0.11, Total 0.37; units scale with position size):
| Month | Auto | Cross | Means | Total |
|---|---|---|---|---|
| 1 | 2.49 | 0.85 | 0.15 | 3.49 |
| 3 | −2.51 | 4.80 | 0.14 | 2.43 |
| 9 | −4.22 | 5.08 | 0.13 | 0.99 |
| 13 | −6.70 | 5.92 | 0.12 | −0.66 |
- 5 size portfolios, m3: Auto −3.99, Cross +5.11, Total 1.25. 9 size-B/M, m3: −5.35 / +6.75 / 1.83.
- After m1, Auto always *reduces* profit and Cross always supplies it.
- Means contribute only 0.11–0.15 for industries, contrary to Conrad–Kaul (1998), whose stock-level estimates are noisy.
- Small-sample bias is ≈ −0.50 (Auto) and +0.41 (Cross) for industry/size, and −0.77/+0.66 for size-B/M. Bootstrap SEs are *smaller* than LM asymptotic SEs (unexplained); GARCH bootstrap changes SEs by under 5%.

**Against portfolio-specific underreaction plus market reversal**
- If reversals came from the market, own autocorrelation would scale with $R^2_i$ (Eq. 26). $R^2_i$ runs from 0.64 (small) to 0.98 (big), yet the big quintile's autocorrelation is the second closest to zero (difference vs Q4 significant at 1.8%).
- Cross-serial rows should be proportional to market correlations; they are not.
- Table 7: market-adjusted returns are positively autocorrelated (size 0.08, B/M 0.06, industry 0.02, or 0.05 over the first 12 lags). They are also predicted by the lagged *market* return (significantly negative for size Q1–Q4, positive for Q5), which is consistent with excess covariance.

**Table 8: Fama–French three-factor model**
- Momentum *in the FF factors themselves* (weights ∝ past 12m factor return): m1 0.61% ($t$=3.68), first 6m **2.60%** ($t$=2.81).
- On FF3 residuals (formation and holding, full-sample betas), 6m profit falls:
  - size quintiles 2.56 → **0.60%** (still significant, $t$=2.42);
  - B/M quintiles 2.45 → **0.47%**;
  - 25 size-B/M 3.23 → **0.40%**;
  - industries only 3.04 → **2.46%** ($t$>4).
- FF3 absorbs size/B/M momentum but not industry momentum.

## Critical assessment
- **Convincing:** the Lo–MacKinlay accounting (negative autos with positive profits), the diversification argument, and the Eq. 7 point that "residual persistence ≠ underreaction."
- **Fragile or limited:**
  - The excess-covariance models are illustrative and too loose to predict the *pattern* of cross-serial correlations. Lewellen admits they cannot be separated from each other.
  - Nothing is said directly about individual-stock momentum.
  - B/M samples are short (1963–99).
  - FF3 absorbing size/B/M momentum is close to mechanical, since portfolio $R^2$ ≈ 95%. It relocates the puzzle to factor momentum rather than explaining it.
  - No trading costs.
- **Internal inconsistencies:** the B/M VW 6m profit is 2.14% for deciles in Section 1 and 2.45% for quintiles in Section 3.5. The 9 size-B/M 6m profit is 3.43% ($t$=4.11), while the 3.23% figure is for 25 portfolios; older summaries swapped these. Several equations (20, 25) render ambiguously in the extracted text.
- **In hindsight:** this is an early statement of the *factor momentum* view later formalized by Ehsani–Linnainmaa and Arnott et al. The FF-factor momentum row in Table 8 is a direct precursor.

## Practical relevance for a quant PM
- Momentum lives at several layers (stock residual, industry, characteristic/factor) with different decay. Stock and industry momentum turns negative after about 12 months; size/B/M momentum stays positive up to 18 months. Set horizons and holding periods per layer, and do not assume a stock-momentum sleeve is orthogonal to factor exposure.
- Risk-model implication: characteristic-portfolio returns are negatively auto- and cross-autocorrelated at 1–18 months, with big caps leading. A 12-month lookback on factors carries a slow mean-reversion component that i.i.d. risk models ignore.
- A useful diagnostic for any momentum sleeve: compute the Auto/Cross/Means split. Cross-dominated profits imply exposure to common-shock reversals, which is crash-relevant when the market reverses.
- Evaluate factor-adjusted momentum by sorting on *residuals* (as in Table 8), not by regressing WML on factors, because WML loadings are time-varying (footnote 14).
