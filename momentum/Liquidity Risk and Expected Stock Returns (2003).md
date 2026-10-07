# Liquidity Risk and Expected Stock Returns

**Ľuboš Pástor, Robert F. Stambaugh · 2003 · Journal of Political Economy 111(3), 642–685 · Source file `Finance/AbnormalReturnsMomentum_PastorStambaugh_2003.pdf` (scanned; text obtained by OCR) · CRSP NYSE/AMEX daily data for the liquidity measure (Aug 1962–Dec 1999); NYSE/AMEX/Nasdaq common stocks for pricing tests (1966–1999)**

## Claim / contribution
The paper asks whether market-wide liquidity is a priced state variable. The test is about *systematic* liquidity risk (comovement with aggregate liquidity shocks), not the level of a stock's own liquidity (Amihud–Mendelson). The authors (i) build a monthly aggregate liquidity measure from volume-related daily return reversals and (ii) show that stocks with high betas to its innovations earn higher returns. The top-minus-bottom decile of predicted liquidity betas has a four-factor (FF3 + MOM) alpha of **7.48% p.a. (t = 3.42)** over 1966–1999. The paper also finds that a liquidity-risk spread cuts momentum's alpha roughly in half. This became the standard **PS liquidity factor** used as a control in the momentum and anomaly literature.

## Liquidity measure
For stock $i$ in month $t$, OLS on daily data $d = 1..D$ (requires $D > 15$; price between \$5 and \$1000; volume in \$ millions):
$$r^e_{i,d+1,t} = \theta_{i,t} + \phi_{i,t}\, r_{i,d,t} + \gamma_{i,t}\,\mathrm{sign}(r^e_{i,d,t})\, v_{i,d,t} + \varepsilon_{i,d+1,t},$$
- $r^e$ is the return in excess of the CRSP VW market; $v$ is dollar volume.
- Signed volume proxies order flow. Illiquidity shows up as reversal, so $\gamma<0$, and a larger $|\gamma|$ means lower liquidity.
- Using the excess return to sign volume avoids zero-return days. The lagged total return absorbs non-volume reversals such as tick effects.
- Motivated by Campbell, Grossman & Wang (1993).
- In a simulation with 10,000 stocks, the cross-sectional correlation between the estimated and true liquidity coefficient is 0.98.

**Aggregation.** $\hat\gamma_t = \frac1N\sum_i \hat\gamma_{i,t}$, equal-weighted over NYSE/AMEX stocks ($N$ between 951 and 2,188). The level series is scaled by $m_t/m_1$ (market cap relative to Aug 1962), so it reads as the cost of a \$1m trade in 1962 dollars (≈ \$34m at end-1999). Mean ≈ −0.03 (median −0.02), i.e. a cost of about 2–3%.

**Innovations.** First the differences are scaled:
$$\Delta\hat\gamma_t = \tfrac{m_t}{m_1}\tfrac1{N_t}\sum_i(\hat\gamma_{i,t}-\hat\gamma_{i,t-1}).$$
Then fit
$$\Delta\hat\gamma_t = a + b\,\Delta\hat\gamma_{t-1} + c\,\tfrac{m_{t-1}}{m_1}\hat\gamma_{t-1} + u_t,$$
which is effectively an AR(2) in levels, and set $L_t = \hat u_t/100$. The level series has AR(1) coefficient 0.22. Innovations are needed because expected liquidity changes predict returns.

**Properties of the measure.**
- Largest drops: Oct 1987, Nov 1973 (oil embargo), Sep 1998 (LTCM/Russia), May 1970, Oct 1997 (Asian crisis).
- $\mathrm{corr}(L_t, \text{market}) = 0.36$: 0.52 in down months vs 0.03 in up months.
- $\mathrm{corr}(L_t,\cdot)$: SMB 0.23, HML −0.12, MOM 0.01. The level series has correlation −0.57 with within-month market volatility.
- **Flight to quality** (Table 1): in the 14 months with $L_t$ at least 2σ below zero, stock–bond correlations turn negative (e.g. −0.387 with minus the change in the T-bill rate vs 0.092 in other months). The volume-change/return correlation flips to −0.360 (p = 0.002).
- Commonality: odd- vs even-size-decile liquidity changes have correlation 0.56 (t = 14.2).
- **Specification sensitivity:** the 23 alternative versions of the regression (total vs excess returns, return vs sign) have innovation correlations with the baseline of −0.47 to 0.80, averaging 0.21. Value-weighted aggregation has correlation 0.77 and loses the crisis spikes and the flight-to-quality pattern. The authors keep the equal-weighted, sign-based version on these grounds.

## Pricing tests
**Liquidity beta.** In a regression that also contains the three Fama–French factors,
$$r_{i,t} = \beta^0_i + \beta^L_i L_t + \beta^M_i MKT_t + \beta^S_i SMB_t + \beta^H_i HML_t + \epsilon_{i,t}.$$

**Predicted betas.** $\beta^L_{i,t} = \psi_0 + \psi' Z_{i,t-1}$, where $Z$ contains:
- historical $\beta^L$ (60-month window, at least 36 months);
- average $\hat\gamma_{i}$ and log dollar volume over the past 6 months;
- 6-month cumulative return and volatility;
- log price and log shares outstanding.

$\psi$ is estimated each year-end by pooled panel regression on FF3-purged returns (Shanken 1990 style), using only data available at the time. The innovations $L_t$ are also re-estimated each year, so there is no look-ahead. Historical beta is the dominant predictor (scaled coefficient 2.30, t = 9.97).

**Portfolios.** Decile sorts at each year-end, held 12 months, Jan 1966–Dec 1999, about 187 stocks per decile. Post-ranking liquidity beta of 10−1 = 8.23 (t = 2.37).

**Characteristics of the 10−1 spread (Table 3).**
- The high-beta decile holds *larger* stocks (VW average \$14.28bn vs \$2.83bn) and is slightly more liquid.
- Loadings: MKT −0.30, SMB −0.65, HML −0.40 (growth tilt), MOM +0.11 (winner tilt).

**Alphas of 10−1 (% p.a., t-stats in parentheses):**

| | CAPM | FF3 | FF3+MOM |
|---|---|---|---|
| VW, 1966–99 | 6.40 (2.54) | 9.23 (4.29) | **7.48 (3.42)** |
| VW, 1966–82 | 1.34 (0.36) | 8.50 (2.77) | 6.21 (1.95) |
| VW, 1983–99 | 11.39 (3.36) | 10.74 (3.53) | 9.49 (3.12) |
| EW, 1966–99 | 8.23 (4.12) | 10.49 (6.50) | 7.66 (4.95) |

- VW four-factor alphas by decile: decile 1 −5.11 (t = −3.12), decile 10 +2.36 (t = 2.06). **Most of the spread comes from the low-liquidity-beta short leg.**
- GRS rejects joint zero alphas at 1% for the full period (VW and EW, all three models).

**GMM premium using all 10 deciles** ($E[r]=B\lambda_F+\beta^L\lambda_L$; $\lambda_L$ is not equal to $E[L]$ because $L$ is not traded):
- $\lambda_L$ = 0.91 (t = 2.92) with 3 traded factors, 0.78 (t = 2.43) with 4.
- Implied 10−1 premium $(\beta^L_{10}-\beta^L_1)\lambda_L$ = 9.63% (3 factors) and 7.56% (4 factors); EW 11.06% and 8.56%. These are close to the portfolio alphas. The traded factors contribute less than 2% p.a.

**Robustness.**
- Sorting on *historical* betas only (at least 5 years of data, 1968–99): 10−1 beta 5.99 (t = 1.88); alphas CAPM 4.66 (2.36), FF3 4.15 (2.08), 4-factor 4.87 (2.38). $\lambda_L$ = 0.80 (t = 1.77) and 1.04 (t = 1.76). Weaker but consistent. EW historical-beta sorts lose significance.
- Size sort: only the smallest deciles have significant positive liquidity betas. The smallest decile's four-factor alpha (> 3% p.a., t ≈ 2.3) is more than covered by its implied liquidity premium (3.7–4.1%).
- Stock-level $\hat\gamma_{i,t}$ is too noisy to sort on. The measure works only in aggregate.

## Momentum link (Section IV)
Ex-post tangency portfolios (monthly Sharpe ratio, SR):

| Universe | Max SR | Weights |
|---|---|---|
| FF3 | 0.22 | — |
| FF3 + MOM | 0.33 | MOM 20.85% |
| FF3 + LIQ$^E$ (EW spread) | 0.40 | — |
| FF3 + MOM + LIQ$^V$ | 0.37 | LIQ$^V$ 15.6% vs MOM 11.9% |
| FF3 + MOM + LIQ$^E$ | 0.42 | MOM falls to 6.5%; LIQ$^E$ 25.6% |

Alpha of MOM (EW 12–2 decile spread), % p.a.:

| Regressors | 1966–99 | 1966–82 | 1983–99 |
|---|---|---|---|
| FF3 | 16.30 (4.85) | 21.65 (4.53) | 11.10 (2.29) |
| FF3 + LIQ$^V$ | 13.89 (4.09) | 19.46 (4.04) | 8.03 (1.63) |
| FF3 + LIQ$^E$ | **8.41 (2.55)** | 16.11 (3.35) | **−1.29 (−0.28)** |

MOM loads strongly on the traded spreads: 0.26 (t = 3.41) on LIQ$^V$ and 0.75 (t = 7.77) on LIQ$^E$. However, MOM's beta on the *nontraded* $L_t$ is only 6.9 (t = 1.3), and it is negative in 1983–99. The authors therefore decline to claim that liquidity risk explains momentum. In their words it is "tantalizing" but inconclusive.

## Critical assessment
**Convincing:**
- Careful out-of-sample construction: betas and innovations are re-estimated annually with no look-ahead.
- Economically large, significant alphas in both halves of the sample (the four-factor VW alpha is borderline in 1966–82, t = 1.95).
- The innovations behave like a crisis and flight-to-quality indicator.

**Fragile / caveats:**
- The measure is admittedly ad hoc and fragile to specification: alternatives have an average correlation of only 0.21 with the baseline, and the value-weighted version differs materially.
- Individual $\gamma$ estimates are pure noise, and the factor is equal-weighted, so it reflects smaller-stock liquidity.
- The alpha is driven by the short leg (low-beta stocks), and the characteristic-based beta prediction partly blends in size, volatility and price.
- The pre-1983 VW CAPM alpha is insignificant.
- Nasdaq volume is overstated relative to NYSE/AMEX, which the authors acknowledge (results are similar without Nasdaq in the beta-prediction regression).
- The "halves momentum's alpha" result relies on the EW traded spread, not on the $L_t$ beta. It is a spanning result, not a risk explanation.

**Typos / OCR notes:** the abstract rounds the four-factor alpha to 7.5%. Several tables in the scan are rotated; numbers above were checked against the text or re-OCR'd.

## Practical relevance for a quant PM
- The PS innovation series (maintained by the authors, not in this PDF) is a useful liquidity-crisis state variable and a factor for risk decomposition. Expect momentum, small-cap and short-volatility books to lose together when $L_t$ drops.
- Low-liquidity-beta stocks earn strongly negative alphas. This is a candidate short-side screen, or a reason to control liquidity beta when judging anomaly alphas.
- When evaluating a momentum sleeve, test spanning against a traded liquidity-risk spread. The standalone alpha of EW momentum shrinks sharply post-1983 once it is included.
- Implementation detail: estimate $\gamma$ on excess returns with sign-based order flow, aggregate by equal weight, scale by market cap, and use AR residuals rather than levels.
