# Factor Momentum and the Momentum Factor

**Sina Ehsani · 2017 (SSRN 3014521 working paper, July 16 2017; later developed into Ehsani & Linnainmaa, JF 2022) · Source file `Finance/Momentum_Ehsani_2017.pdf` · Data: 22 anomaly factors (15 US Jul-1963–Dec-2015; 7 global ex-US Jul-1990–Dec-2015) from French, AQR and Pástor–Stambaugh libraries; monthly raw (not vol-scaled) returns**

## Claim
1. Anomaly/factor returns are positively autocorrelated. Time-series and cross-sectional momentum *across factors* earns significant profits, driven mainly by own-autocovariance.
2. The persistence sits mostly in the **short (Low) leg** of anomalies.
3. Fama–MacBeth characteristic slopes are equally persistent.
4. Stock momentum (UMD) is largely an aggregation of factor autocovariance. A diversified factor-TS portfolio spans UMD, but UMD does not span it.
5. UMD crashes coincide with widespread negative factor autocorrelation.

## Data
- **US (15):** AC, BAB, CMA, CFP, EP, HML, LTREV, LIQ (from 1968), NSI, QMJ, RMW, RVAR (FF3 residual variance), SMB, STREV, UMD.
- **Global ex-US (7):** BAB, CMA, HML, QMJ, RMW, SMB, UMD.
- Where only portfolios exist, each factor is built as the average of the top 3 minus the bottom 3 deciles.
- Mean monthly factor returns range from 0.03% (global SMB) to 0.84% (BAB). Average pairwise correlation is 0.08.
- Both UMDs are excluded from the factor-momentum strategies, leaving 20 test assets.

## Factor-level predictability
- **Pooled TS regression** $r^f_t=\alpha_k+\beta_k r^f_{t-k}$ (×100, time-clustered SEs): $\beta_1=11.82$ (t = 2.98). Lags 2–10 are small; the slope rises again at lag 11 (4.99, t = 2.11) and lag 12 (4.31). Mildly negative coefficients at lags 13–15.
- **Cross-sectional FM of factor returns on lagged factor returns:** $\gamma_1=19.10$ (t = 8.37). Slopes are positive through lag 16 and U-shaped over lags 1–12 (lag 11: 9.96, t = 4.10). Each monthly cross-section has only 22 observations.
- **Pooled regression on the indicator $\mathbf 1\{\bar r^f_{t-12,t-1}>0\}$:** intercept 0.04% (insignificant), slope 0.51% (t = 4.40). Factors earn their premium only after a positive year. After a negative year they earn ≈0, and 8 anomalies earn a negative premium.

## Strategies ($k=12$, $h=1$; Table 4A)

| | Passive (EW) | TS$_L$ | TS | TS$_W$ | XS$_L$ | XS | XS$_W$ |
|---|---|---|---|---|---|---|---|
| Mean %/mo | 0.35 | 0.02 | 0.35 | **0.52** | 0.11 | 0.23 | **0.60** |
| SD %/mo | 1.15 | 1.84 | 1.23 | 1.35 | 1.54 | 1.12 | 1.64 |
| Sharpe (ann.) | 1.05 | 0.04 | 0.99 | **1.33** | 0.25 | 0.71 | 1.27 |

- Definitions: $TS=\frac1F\sum_f\text{sgn}(\bar r^f_{-T})r^f_t$ and $XS=\frac1F\sum_f\text{sgn}(\bar r^f_{-T}-\bar r_{-T})r^f_t$. The $W$ and $L$ variants hold only the long side (winners) or only the losers.
- TS$_W$ − Passive = 0.17%/mo (t = 4.44). The long–short TS is no better than passive, because shorting past losers earns ~0.
- For comparison, the market Sharpe over the same period is 0.39.
- **Horizons (Jegadeesh–Titman overlapping portfolios):**
  - XS {1,1}: 0.31%/mo (t = 5.98), decaying to 0.06% (t = 1.23) at {1,2}.
  - TS {1,1}: 0.36% (t = 6.65); TS {12,1}: 0.34% (t = 7.05).
  - TS stays significant for holding periods up to about 9–12 months. There is no short-term reversal at the factor level.

## Decompositions
**Linear XS** (Lo–MacKinlay), with $\Omega_T=E[(r_{-T}-\mu)(r_t-\mu)']$:
$$E[\pi^{XS}]=\tfrac{F-1}{F^2}\text{Tr}\,\Omega_T-\tfrac1{F^2}(\mathbf 1'\Omega_T\mathbf 1-\text{Tr}\,\Omega_T)+\sigma^2_\mu .$$
Premium 0.21%/mo (t = 3.49), made up of auto-cov **+0.24**, cross-cov **−0.07** (factor cross-autocovariances are positive, which hurts XS) and mean dispersion +0.05.

**Linear TS**:
$$E[\pi^{TS}]=\tfrac1F\sum_f\text{Cov}(r^f_{-T},r^f_t)+\tfrac1F\sum_f(\mu^f)^2 .$$
Premium 0.41%/mo (t = 4.65) = auto-cov 0.25 + mean² 0.16. TS beats XS because it does not pay the cross-covariance term.

**Leg-level TS**, with $r^f=r^{H}-r^{L}$, on 12 anomalies using decile 10 and decile 1:
$$E[\pi^{TS}]=\tfrac1N\sum_f\big[\text{Cov}(r^H_{-T},r^H_t)+\text{Cov}(r^L_{-T},r^L_t)-\text{Cov}(r^H_{-T},r^L_t)-\text{Cov}(r^L_{-T},r^H_t)+(\mu^H-\mu^L)^2\big].$$

| Term | Contribution to the 0.74%/mo premium (t = 3.22) |
|---|---|
| Low-leg autocovariance | **0.35** (positive for all 12 anomalies) |
| Past High → future Low (negative lead–lag) | 0.13 |
| Mean² | 0.18 |
| High-leg autocovariance | 0.08 |
| Past Low → future High | 0.00 |

The persistent mispricing is on the short side, consistent with short-sale constraints (Miller 1977) and Stambaugh–Yu–Yuan (2012).

## Fama–MacBeth slope persistence
- Monthly single-characteristic FM regressions on standardized characteristics.
- Pooled regression of $\gamma_{c,t}$ on its 12-month mean: $b=0.43$ (t = 3.89).
- On the indicator $\mathbf 1\{\bar\gamma_{-T}>0\}$: $b=0.38$ (t = 4.16), intercept 0.06 (t = 0.67). A characteristic prices the cross-section next month only if it priced it over the past year.
- Lag profile: continuation through lag 12 (spike at lags 11–12), reverting from lag 13.

## Linking factor momentum to UMD
With $R_{s,t}=\sum_f\beta^f_s r^f_t+\varepsilon_{s,t}$ and no factor/residual lead–lags, stock-level XS momentum decomposes as
$$E[\pi^{Mom}]=\sum_f\text{Cov}(r^f_{-T},r^f_t)\,\sigma^2_{\beta^f}+\sum_{f\neq g}\text{Cov}(r^f_{-T},r^g_t)\,\text{Cov}(\beta^g,\beta^f)+\tfrac1N\sum_s\text{Cov}(\varepsilon_{s,-T},\varepsilon_{s,t})+\sigma^2_\eta .$$
Factor autocovariance drives stock momentum in proportion to the cross-sectional dispersion of betas. Under FF5 (Appendix B), the cross term is negligible.

**Correlations with UMD (Table 7).** Raw factors are roughly uncorrelated with UMD. Autocovariance-conditioned returns $\bar r^f_{t-12,t-2}\cdot r^f_t$ (skipping the most recent month) are strongly correlated:
- HML: −0.17 → 0.46
- RVAR: 0.20 → 0.67
- QMJ: 0.24 → 0.57
- Diversified (average of 20 factors): **0.04 → 0.66** (Fisher z = 13.58)

19 of 20 correlations rise. The exceptions are global BAB, RMW and SMB, where the increase is insignificant or negative. Conditioned returns remain mutually uncorrelated (average 0.09), so there is no common component.

**Diversification caveat.**
- HML's correlation with UMD is −0.57 after an HML loss year and +0.23 otherwise.
- HML earns 0.45%/mo after positive years vs 0.15% (t = 0.71) after negative years.
- Value hedges momentum mainly when value itself earns nothing.

**Spanning momentum deciles (Table 9, Jul-1964–Dec-2015):**

| Model | Mean abs. α | GRS F | 10−1 α (t) |
|---|---|---|---|
| CAPM | 0.25 | 5.59 | 1.48 (5.26) |
| FF3 + UMD | 0.12 | 3.72 | 0.34 (3.01) |
| FF3 + factor-TS (0.35%/mo) | **0.11** | **3.23** | 0.42 (1.94) |

- Pairwise spanning: $TS=0.22_{[5.67]}+0.18\,UMD$ and $UMD=-0.06_{[-0.42]}+2.18\,TS$. Factor-TS subsumes UMD's mean, while UMD leaves about 2/3 of the TS premium unexplained.
- The TS model has lower $R^2$ (0.79–0.88) than FF3 + UMD.

**Crashes (Section 5.2).**
- The aggregate autocorrelation index is the cross-sectional mean of $\rho^f_{Auto,t}\approx(\bar r^f_{-T}r^f_t-\mu^2)/(\sigma^2/\sqrt{11})$. Its correlation with UMD is 0.68.
- UMD moments by regime:

| Regime (index sign) | Mean %/mo | SD | Skew | Kurtosis |
|---|---|---|---|---|
| Positive | 2.42 | 3.20 | 0.80 | 7.94 |
| Negative | −1.69 | 4.43 | −2.53 | 16.60 |
| Full sample | – | 4.27 | −1.37 | 13.58 |

- A one-SD (0.76) move in the index goes with +2.87% UMD (t = 22.44).
- Probit for UMD bottom-decile months: marginal effect of the index −14.96 pp per unit (pseudo-R² 0.37). For top-decile booms: +14.67.

**Sentiment (Section 6).**
- Pooled regression: high sentiment (Baker–Wurgler, above median) adds +0.27%/mo (t = 2.84) and positive past-year return adds +0.49% (t = 4.19). The two are distinct predictors.
- In low sentiment, past winners minus past losers = 0.71%/mo (t = 4.79). Winner factors earn ≈0.50% regardless of sentiment.

## Critical assessment
- **Robust core:** the factor-TS results are simple, use public data, and are large relative to the passive benchmark. The indicator regressions (premium only after a positive year) are the most useful practical finding.
- **Contemporaneous crash analysis.** The autocorrelation index at $t$ uses $r^f_t$, so it is a *contemporaneous* decomposition of month-$t$ returns, not an ex-ante crash predictor. The regime moments, the 0.68 correlation and the probit pseudo-R² are partly mechanical. The paper does not provide an out-of-sample crash forecast.
- **Spanning claims:** similar to UMD, not dominant. Factor-TS reduces GRS modestly (3.72 → 3.23); the 10−1 α is 0.42 vs 0.34 (less significant only because of the larger SE) and $R^2$ is lower. "Explains the momentum premium" rests on the pairwise spanning regressions.
- **Small cross-section.** XS on 20 correlated factors, with each FM cross-section having only 7–22 observations. Many anomalies are closely related (HML/CFP/EP; CMA/NSI).
- **Short-leg result** uses only 12 anomalies with decile portfolios. The Low legs are small, illiquid, high-vol stocks, where microstructure effects could inflate autocovariance. The claim that 20–30%-of-CRSP portfolios rule out firm-level stories is argued, not tested.
- **Loose ends:**
  - The long–short TS gains nothing over passive (0.35 vs 0.35); the benefit comes entirely from dropping losers.
  - Raw returns are used, so high-vol factors (RVAR SD 5.07) dominate the equal weights.
  - Minor internal inconsistency: the positive-regime UMD stats (2.42/3.20 monthly) imply an annual Sharpe of ≈2.6, not the reported 2.43.
  - No transaction costs, no out-of-sample period.

## Practical relevance for a quant PM
- **Factor timing that works on public data:** hold factors with positive trailing 12-month (or 1-month) returns and drop, rather than short, the losers. Expect a ~0.17%/mo improvement over equal-weight factor exposure, with better Sharpe.
- **Momentum is partly factor TS.** A multi-factor book running factor momentum already carries much of UMD's exposure. Correlations between UMD and factor-timed sleeves are ~0.66, not ~0.
- **Residual momentum must remove many factors.** Residuals estimated against FF3 alone still contain factor autocovariance, so use a broad factor model.
- **Diversification is regime-dependent.** Value/quality diversify momentum mainly when they are themselves in drawdown.
- **Crash monitoring:** widespread negative factor autocorrelation is the fingerprint of UMD crashes. Combine it with Daniel–Moskowitz bear-market/high-vol state variables for anything forecastable.
