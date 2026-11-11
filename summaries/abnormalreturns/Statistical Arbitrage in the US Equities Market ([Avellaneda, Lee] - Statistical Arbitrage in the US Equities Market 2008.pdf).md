# Statistical Arbitrage in the US Equities Market — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| Title | Statistical Arbitrage in the U.S. Equities Market |
| Authors | Marco Avellaneda, Jeong-Hyun Lee (Courant Institute, NYU; Finance Concepts SARL) |
| Date / venue | Working paper, June 30, 2008 (published later in *Quantitative Finance* 10(7), 2010) |
| Source file | `Finance/[Avellaneda, Lee] - Statistical Arbitrage in the US Equities Market 2008.pdf` |

## Question
Generalized pairs trading: decompose each stock's return into a systematic part and a residual, model the residual as mean-reverting, and fade large excursions in a market-neutral book. The empirical contribution is to compare how the choice of factors (PCA eigenportfolios vs sector ETFs, fixed vs variable factor count, calendar vs "trading" time) changes the residuals and hence the after-cost PnL, on US stocks with market cap > \$1bn (at trade date), daily EOD data 1996/97–2007, with a close look at August 2007.

## Factor models
Returns $R_i=\sum_{j=1}^m\beta_{ij}F_j+\tilde R_i$; a book $\{Q_i\}$ is market-neutral if $\sum_i\beta_{ij}Q_i=0\ \forall j$, so PnL is $\sum_i Q_i\tilde R_i$. The authors cite ~15 factors (10–20) explaining ~50% of variance in developed markets (Plerou et al. 2002; Laloux et al. 2000).

**PCA.** Standardized returns $Y_{ik}=(R_{ik}-\bar R_i)/\sigma_i$ over $M$ days (correlation window 1 year = 252 days); $\rho=YY^\top/(M-1)$, eigenpairs $(\lambda_j,v^{(j)})$. Eigenportfolio weights $Q_i^{(j)}=v_i^{(j)}/\sigma_i$, factor returns $F_{jk}=\sum_i (v_i^{(j)}/\sigma_i)R_{ik}$ (mutually uncorrelated in sample). Equivalent to modelling
$$\rho_{ij}=\sum_{k=1}^m\lambda_k v_i^{(k)}v_j^{(k)}+\epsilon_{ii}^2\delta_{ij},\qquad \epsilon_{ii}^2=1-\sum_{k}\lambda_k (v_i^{(k)})^2 .$$
Few eigenvalues detach from the bulk — fewer than the number of industries — so the signal/noise boundary is blurred. Two rules: fixed $m=15$, or variable $m$ such that retained eigenvalues explain a target share of the trace (e.g. 55%).

Interpretation: $v^{(1)}$ has (nearly) all positive weights (Krein; a few negatives from commodity/mining names), and its inverse-vol-weighted eigenportfolio tracks the cap-weighted market. Higher eigenvectors show *coherence*: sorted loadings cluster by industry. Table 1 ($v^{(2)}$): long energy/oil & gas (Sunoco, XTO, Apache, Schlumberger…) vs short airlines, regional banks, some consumer names. Table 2 ($v^{(3)}$): long utilities vs short semiconductors. The most heavily loaded names are not necessarily the largest caps, so PCA factors carry no a priori cap bias.

**ETFs.** Multi-ETF regressions give unstable, opposite-sign loadings because ETFs are correlated (fixes: matching pursuit, ridge). The backtests use the simplest version: each stock is regressed on its single sector ETF (15 sectors, Figure 7), $\beta_i=\mathrm{Cov}(R_i,R_{I})/\mathrm{Var}(R_I)$. ETFs are interpretable and traded but cap-weighted.

## Residual model and signal
$$\frac{dS_i}{S_i}=\alpha_i\,dt+\sum_j\beta_{ij}\frac{dI_j}{I_j}+dX_i,\qquad dX_i=\kappa_i(m_i-X_i)\,dt+\sigma_i\,dW_i .$$
Stationary law $N(m_i,\sigma_i^2/2\kappa_i)$; $\sigma_{\mathrm{eq},i}=\sigma_i/\sqrt{2\kappa_i}$, $\tau_i=1/\kappa_i$. Betas and OU parameters are re-estimated daily on a **60-business-day** window ($T_1=60/252$, roughly one earnings cycle), same for all stocks. Only names with $\tau_i<T_1/2$, i.e. $\kappa_i>252/30=8.4$ yr$^{-1}$ (reversion within 30 days), are traded. The working paper says the OU fit is accepted/rejected per stock by goodness of fit but does not spell out the estimator or tests.

2007 distribution of $\tau$ (Table 3, business days): max 30, 75th pct 11, median 7.5, 25th pct 4.9, min 0.5; "fast days" 36%.

s-score $s_i=(X_i-m_i)/\sigma_{\mathrm{eq},i}$, with means recentred cross-sectionally $\tilde m_i=m_i-\frac1N\sum_j m_j$ (removes "model bias"; consistently better in backtests and adopted everywhere). Rules, cutoffs chosen on ETF-factor simulations 2000–2004:
- open long if $s<-1.25$; open short if $s>+1.25$;
- close short if $s<+0.75$; close long if $s>-0.50$ (closing shorts at 0.75 was slightly better than at 0.50).

Positions are **bang-bang**: \$1 of stock against $\beta$ dollars of factor(s) at full size when a signal fires, unwound on the exit signal; this beat continuous adjustment.

Drift-adjusted score $s_{\mathrm{mod},i}=s_i-\alpha_i\tau_i/\sigma_{\mathrm{eq},i}$ (a built-in momentum tilt, since $\alpha$ is roughly the slope of a 60-day moving average). With $\alpha\sim15$ bp, $\tau\sim7$ days and $\sigma_{\mathrm{eq}}\sim300$ bp, the shift is about 0.3 s-units; the same cutoffs work and the effect is minor (backtests not shown).

## Backtest design
Daily re-estimation and rebalancing, fills at that day's close. PnL: $E_{t+\Delta t}=E_t+E_t r\Delta t+\sum_i Q_{it}R_{it}-(\sum_i Q_{it})r\Delta t+\sum_i Q_{it}D_{it}/S_{it}-\sum_i|Q_{i,t+\Delta t}-Q_{it}|\epsilon$, with $\epsilon=5$ bp per trade (10 bp round trip), no long/short rate spread, no borrow cost. Position size $Q_{it}=\Lambda_t E_t$, $\Lambda_t$ set for about 2+2 leverage (e.g. 2/100 for 100 longs and 100 shorts), updated only on new positions, modulated by sector for ETF books. Synthetic-ETF books add a daily S&P 500 futures beta hedge. Sharpe $=(\mu-r)/\sigma$ annualized.

## Results
| Strategy | Period | Result |
|---|---|---|
| PCA-based (average) | 1997–2007 | Sharpe 1.44 |
| PCA-based (average) | 2003–2007 | Sharpe 0.9 |
| ETF-based (synthetic before 2002) | 1997–2007 | Sharpe 1.1, similar decay after 2002 |
| Actual ETFs | 2003–2007 | average Sharpe 0.6 |
| Actual ETFs + trading time | 2003–2007 | Sharpe 1.51 |

- **Synthetic vs actual ETFs (2002–07):** actual ETFs outperform strongly; the authors' explanation is that traded ETFs carry better price information.
- **15-PCA vs actual ETFs (2002–07):** 15-PCA outperforms significantly.
- **Variable PCA:** the number of eigenvectors needed for 55% of variance varies over time roughly between 10 and 30 and moves inversely with the VIX. It is low in late 2002 and summer 2007 (variance concentrates in a few modes) and high in 2004–06. 55% PCA is comparable to but slightly worse than 15-PCA, and better than 45% or 65%. At 75% the book loses steadily, because residuals are too small relative to costs. One factor (CAPM-like) gives weak mean reversion, high residual vol and poor Sharpe.
- **Trading time:** returns are rescaled by volume, $\hat R_t=R_t\,\langle\delta V\rangle/(V_{t+\Delta t}-V_t)$, where $\langle\delta V\rangle$ is trailing average daily volume (motivated by price change per share traded). Low-volume moves are amplified and high-volume moves damped, so the book fades low-volume dislocations and respects high-volume prints. This improves ETF strategies "unequivocally", bringing them level with 15-PCA and 55% PCA. PCA strategies gain little.
- **August 2007:** performance was flat or slightly negative in 1H07, then a sharp drawdown in early August and recovery in about 10 days. PCA books drew down about 5% and ETF books about 10%. The backtest nearly tracks the Khandani–Lo contrarian simulation once leverage is matched (KL 4+4; here 2+2). Technology and Consumer Discretionary were hit harder than Financials and Real Estate. The authors read this as support for the unwinding (liquidity-shock) story rather than a fundamental financials shock.

## Authors' interpretation of the factor-count result
Mean reversion works best when ~50% of variance is explained by few factors. If the "true" factor count is large (>25), 15 factors under-defactor and residuals still contain systematic moves. If many factors are used, residual variance and hence opportunity shrink below transaction costs. So the best configurations are 15 ETFs, 15-PCA or ~55% variable PCA.

## Critical assessment
- **Convincing:** the structural points are robust and still useful. (i) Residualize before fading. (ii) There is an interior optimum in factor count, driven by the trade-off between residual signal and costs (1 factor and 75% truncation both fail). (iii) PCA residuals are roughly industry-neutral without explicit constraints. (iv) The August 2007 reproduction of Khandani–Lo from an independent strategy design.
- **Fragile:**
  - Cutoffs were calibrated on 2000–2004, inside the evaluation period, so there is no clean out-of-sample test.
  - Signals are computed from the close and executed at the same close.
  - A flat 5 bp is optimistic for 1997–2001, which is before decimalization and is the period that drives the high full-sample Sharpe. The post-2002 decay (PCA 0.9, ETF 0.6) is the more relevant figure.
  - No borrow costs, market impact, capacity, turnover or holding-period statistics are reported.
  - Most results appear only as figures, with no standard errors on Sharpe differences.
  - Universe construction and survivorship handling (\$1bn at trade date) are not documented.
  - The OU estimation and goodness-of-fit filter are not specified in this version.
- **Practical relevance (PM/researcher):**
  - This is a clean baseline for residual reversal: 60-day betas, PCA on a 1-year correlation matrix, an s-score with $|s|>1.25$ entry and asymmetric exits, and bang-bang sizing.
  - Two additions are cheap to test: volume-scaled returns (trading time) and cross-sectional demeaning of $m_i$.
  - The number of eigenvalues needed for a fixed share of variance is a usable regime and crowding diagnostic.
  - August 2007 shows that residual-reversal books share a common unwind risk regardless of the factor model. Diversifying across factor definitions does not protect against crowding.
  - Natural extensions not tested here: correlation-matrix cleaning (RMT/shrinkage) before PCA, and walk-forward adaptive cutoffs.
