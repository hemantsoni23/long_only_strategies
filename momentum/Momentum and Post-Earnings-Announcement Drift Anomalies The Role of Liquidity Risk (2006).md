# Momentum and Post-Earnings-Announcement Drift Anomalies: The Role of Liquidity Risk

**Ronnie Sadka (U. Washington) · 2006 · *Journal of Financial Economics* 80, 309–349 · Source file `Finance/AbnormalReturnsPostEarningMomentum_Sadka_2006.pdf` · NYSE stocks, intraday ISSM (1983–92) + TAQ (1993–Aug 2001); 4,082 firms, 645M trades; asset-pricing tests Mar 1983–Aug 2001 (222 months)**

## Claim / contribution
- Firm-level price impact is split into **permanent-variable ($\lambda$, informational, Kyle-type)** and **transitory-fixed ($\bar\psi$, inventory and order processing)** components, and then aggregated into market-wide liquidity shocks.
- Only unexpected shocks to the aggregate **variable/permanent** component, $LIQ^\lambda$, are priced in momentum and SUE (PEAD) portfolios. The paper reads $LIQ^\lambda$ as shocks to the market-wide ratio of informed to noise trading and to information quality.
- The estimated premium is **≈6.5% p.a.** Liquidity risk "explains 40–80% of the cross-sectional variation" in expected MOM/SUE portfolio returns (adjusted $R^2$).
- The fixed component and the other two components ($\psi$ permanent-fixed, $\bar\lambda$ transitory-variable) are not priced.

## Methodology
**Price-impact model** (Glosten–Harris, extended). Per stock-month with ≥30 trades; trades signed by Lee–Ready with a 5-second quote delay; block (>10k shares) dummies; OLS with serial-correlation correction:
$$m_t=m_{t-1}+\psi[D_t-E_{t-1}D_t]+\lambda[D_tV_t-E_{t-1}(D_tV_t)]+y_t,\qquad p_t=m_t+D_t[\bar\psi+\bar\lambda V_t],$$
$$\Delta p_t=\psi\,\varepsilon_{\psi,t}+\lambda\,\varepsilon_{\lambda,t}+\bar\psi\,\Delta D_t+\bar\lambda\,\Delta(D_tV_t)+\tilde y_t .$$
- Unexpected signed volume comes from an AR(5) on $D_tV_t$ (Eq. 4).
- The expected sign is $E_{t-1}D_t=1-2\Phi(-E_{t-1}[D_tV_t]/\sigma_\varepsilon)$ (Eq. 5).
- Only *unanticipated* order flow moves beliefs, while the transitory costs apply to the full order flow.
- Estimates are winsorized at 1/99% and scaled by beginning-of-month price.

**Diagnostics** (Tables 1–2):
- Scaled averages: permanent variable $4.45\times10^{-7}$ per share, transitory fixed 0.37%, permanent fixed 0.08%.
- The transitory variable component is on average *negative*: the informational share of cost rises with trade size.
- The $\bar\psi$ t-stat is significant for over 90% of stock-months; the $\lambda$ t-stats are centered just above 1, so firm-level $\lambda$ is noisy.
- Cross-sectional correlation with log size: −0.37 ($\lambda$) and −0.53 ($\bar\psi$). Amihud correlates 0.36 with $\bar\psi$ but only 0.15 with $\lambda$. Turnover correlates weakly with both.

**Factors.**
- Aggregate each component as an equal-weighted cross-sectional average, then flip the sign so that negative = illiquidity. Innovations come from Box–Jenkins fits: **$\bar\psi^M$: random walk (0,1,0); $\lambda^M$: ARMA(2,0,1)**. AR(2) shocks (the Pástor–Stambaugh approach) correlate over 0.90 with these and give nearly identical results.
- $LIQ^\lambda$: sd $5.75\times10^{-3}$. Correlations: MKT 0.15, SMB 0.07, HML 0.05. Corr($LIQ^{\bar\psi}$, $LIQ^\lambda$) = 0.20, rising to 0.33 in down markets vs 0.08 in up markets. Correlation with the Pástor–Stambaugh factor is only 0.28 ($LIQ^\lambda$) and 0.14 ($LIQ^{\bar\psi}$).
- Events: both factors capture Oct 1987. $LIQ^\lambda$ takes a negative shock in the Sept 1998 LTCM episode. Tick-size changes (1997) and decimalization (2001) hit mainly the fixed component, which supports the informational reading of $\lambda$.

**Test assets.** Equal-weighted, monthly rebalanced, NYSE:
- 25 MOM portfolios on 12-2 returns.
- 25 SUE portfolios with $SUE_{i,t}=\frac{(E_{i,q}-E_{i,q-4})-c_{i,t}}{s_{i,t}}$, where $c$ and $s$ are the mean and sd of seasonal differences over the prior 8 quarters. Stocks are held up to 4 months after the announcement.
- Tests: two-pass Fama–MacBeth with Shanken correction; GMM on the SDF $d_t=1-\delta'f_t$ with Hansen (1982) and Hansen–Jagannathan (1997) weighting (Bartlett, 4 lags; Jagannathan–Wang p-values).

## Main results
**Spreads (Table 3, % per month):**
| | Raw 25−1 (t) | CAPM α (t) | FF3 α (t) |
|---|---|---|---|
| MOM (winners 1.44, losers 0.50) | 1.93 (3.28) | 1.98 (3.32) | 2.22 (3.68) |
| SUE | 0.69 (3.23) | 0.71 (3.27) | 0.76 (3.46) |

**Loadings (Table 4, FF3 + one liquidity factor):**
- MOM on $LIQ^\lambda$: losers −2.47 (t −2.89), winners +1.11 (3.11), **25−1 spread 3.59 (t 3.61)**. Losers act as a hedge against liquidity shocks.
- MOM on $LIQ^{\bar\psi}$: no pattern (25−1 t = 0.32).
- SUE 25−1 on $LIQ^\lambda$: 0.69 (t 1.87), a weaker version of the same pattern.

**Fama–MacBeth premia on $LIQ^\lambda$ (Table 5):**
| Model | MOM: $\gamma_\lambda$ [t], adj $R^2$ | SUE: $\gamma_\lambda$ [t], adj $R^2$ |
|---|---|---|
| CAPM | —, 0.00 | —, 0.21 |
| MKT + $LIQ^\lambda$ | 0.47 [2.21], **0.83** | 1.03 [2.35], **0.60** |
| FF3 | —, 0.86 | —, 0.41 |
| FF3 + $LIQ^\lambda$ | 0.15 **[0.74]**, 0.87 | 0.82 [2.24], 0.62 |
- $LIQ^{\bar\psi}$ is never significant.
- For momentum, FF3 (with a *negative* HML premium, since momentum is stronger among growth stocks) already fits 86%, and $LIQ^\lambda$ is *insignificant* once FF3 is included. Under conditional FF loadings (Grundy–Martin style, Section 4.4) that t-stat rises from **0.74 to 2.50**.
- Economic magnitude = loading spread × premium: **54 bp/mo for MOM (vs 193 bp raw spread) and 57 bp for SUE (vs 69 bp)**, i.e. 6.5% and 6.8% annualized (Pástor–Stambaugh: 7.5%). **Liquidity risk explains a minority of momentum returns but most of PEAD.** The abstract's "substantial part of momentum" should be read in that light.

**GMM (Table 6):**
- $LIQ^\lambda$ is significant in 7 of 8 specifications, with premia of **32–76 bp/mo**.
- Model p-values are mixed. For example, Hansen FF3+$LIQ^\lambda$ on MOM gives p = 0.69, while under HJ weighting the $LIQ^\lambda$ t is only 1.04.

**Robustness**
- 5×5 dependent MOM/$\lambda$ and SUE/$\lambda$ sorts (Tables 7–8):
  - MOM WML FF3 α is 0.89% (t 2.68) in the low-$\lambda$ group and 1.25% (t 3.08) in the high-$\lambda$ group.
  - SUE: 0.80% (t 4.39) and 1.07% (t 4.37).
  - Premia are 40–66 bp/mo in GMM and significant at 10% in the cross-sectional regressions.
- Sorting all NYSE stocks on rolling 60-month $LIQ^\lambda$ betas (Mar 1988–Aug 2001, deciles): high − low = **0.44%/mo (5.3% p.a., t 2.43)**, CAPM α 0.44 (t 2.38), FF3 α 0.51 (t 2.79). No other component's beta sort earns a spread.
- $\psi$ and $\bar\lambda$ factors (ARIMA(0,1,3) and (0,1,1), orthogonalized) are not priced.

## Critical assessment
- **Strengths:** careful microstructure decomposition; the informational vs non-informational split is economically meaningful (tick-size events hit only $\bar\psi$); multiple test designs; an independent beta-sort check.
- **Weaknesses:**
  - The test assets are the anomaly portfolios themselves (25 portfolios, one sort), so high cross-sectional $R^2$ with a nontraded factor is a low bar (Lewellen–Nagel–Shanken critique).
  - Premia on nontraded factors are not returns; their scale is arbitrary.
  - For momentum the key FF3+$LIQ^\lambda$ premium is insignificant unconditionally, and the paper leans on an unreported conditional specification to rescue it.
  - Small sample (~18 years), NYSE only, equal-weighted portfolios.
  - Firm-level $\lambda$ is imprecise (median t ≈ 1).
  - Losers' negative liquidity beta ("volume pulled away from them") is asserted, not modeled.
- The earlier version of this summary presented the Glosten–Harris equation incorrectly (it omitted the expected-order-flow adjustment and mislabeled the terms). It also omitted that liquidity risk accounts for only ~28% (54/193 bp) of the momentum spread.

## Practical relevance for a quant PM
- Momentum and PEAD books carry systematic exposure to *information-asymmetry* liquidity shocks. Winners load positively and losers negatively, so the long-short loses when market-wide adverse selection spikes (e.g. 1998). This is a crowding/stress factor worth including in risk models alongside PS or Amihud-type factors, with which it correlates only weakly.
- A proxy is buildable from TAQ: a monthly cross-sectional average of the Glosten–Harris/Kyle $\lambda$, scaled by price, with ARMA shocks as the factor.
- PEAD's drift is largely compensation for this factor, which argues for sizing PEAD more like a risk premium than pure alpha. Most of momentum's spread remains unexplained.
- Execution: the informational $\lambda$ is the cost component that co-moves with the premium. Trading costs for momentum rise exactly when this risk materializes.
