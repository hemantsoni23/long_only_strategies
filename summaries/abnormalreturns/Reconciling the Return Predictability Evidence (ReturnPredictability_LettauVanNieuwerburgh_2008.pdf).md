# Reconciling the Return Predictability Evidence

**Martin Lettau, Stijn Van Nieuwerburgh · 2008 · *Review of Financial Studies* 21(4), 1607–1652 (doi 10.1093/rfs/hhm074) · Source file `Finance/ReturnPredictability_LettauVanNieuwerburgh_2008.pdf` · Annual CRSP VW (NYSE/AMEX/NASDAQ) 1926/27–2004; S&P 500 earnings/dividends (Haver) 1946–2004; book-to-market (Vuolteenaho) 1927–1999 extended by clean surplus**

## Claim

The four puzzles of D/P predictability — slope instability, weak OOS performance, disappearance of in-sample evidence in the late 1990s, and near-unit-root persistence — are all explained by **shifts in the steady-state mean of valuation ratios** (from permanent changes in long-run growth $\bar g$ and/or required return $\bar r$). Removing the shifting mean yields a strong, stable in-sample return predictor that satisfies the present-value restriction. In real time, however, the adjusted ratio does not beat the historical mean, and the binding problem is **estimating the size (level) of a new regime mean, not dating the break**.

## Framework

Baseline: $r_{t+1}-\bar r=\kappa_r(dp_t-\overline{dp})+\tau^r_{t+1}$, $\Delta d_{t+1}-\bar g=\kappa_d(dp_t-\overline{dp})+\tau^d_{t+1}$, with $\overline{dp}=\log(e^{\bar r}-e^{\bar g})-\bar g$, $\rho=(1+e^{\overline{dp}})^{-1}$. Allowing martingale steady states ($E_t\bar r_{t+j}=\bar r_t$, $E_t\bar g_{t+j}=\bar g_t$, $E_t\overline{dp}_{t+j}=\overline{dp}_t$), Appendix B gives
$$dp_t=\overline{dp}_t+E_t\sum_{j\ge1}\rho_t^{j-1}\big[(r_{t+j}-\bar r_t)-(\Delta d_{t+j}-\bar g_t)\big],$$
so $dp_t$ = nonstationary mean + stationary deviation; only $dp_t-\overline{dp}_t$ is a well-defined predictor. (Martingale assumptions for $\bar r,\bar g$ and the nonlinear $\overline{dp}$ are mutually inconsistent in general; Appendix C builds a risk-neutral model with a bounded-martingale $Q_t$, $P/D=Q_t-1$, where they hold approximately.) The authors stress that "permanent" and "extremely persistent" are indistinguishable in finite samples.

**Adjustment.** Model $\overline{dp}_t$ as piecewise constant with Bai–Perron breaks (autocorrelation-robust, 5% trimming); $\widetilde{dp}_t=dp_t-\widehat{\overline{dp}}_{\text{regime}(t)}$ (eq. 8).

## In-sample evidence

**Breaks in log D/P (Table 2).** One break: 1991, $\Delta\overline{dp}=-0.86$ (log units, i.e. level ×0.42); two breaks: 1954 (−0.37) and 1994 (−0.78). sup-$F$(0,1)=13.7, sup-$F$(0,2)=23.9 (p<1%); sup-$F$(1,2)=9.64 (10% not 5%); BIC and LWZ choose 2; 2 vs 3 not rejected. (Table legend reverses the star ordering — "***" is labeled 10%.) A bootstrap and a Monte Carlo AR(1) cannot reproduce the fat left tail of the $dp$ distribution; a real-time recursive bootstrap (Fig. 4) puts $dp$ in the 2.5% tail by 1958 and 1994 and near-certainly non-stationary 1995–99 — breaks detectable without hindsight.

| $dp$ series | AC(1) | AC(2) | ADF p | s.d. |
|---|---:|---:|---:|---:|
| Unadjusted | 0.91 | 0.81 | 0.586 | 0.42 |
| 1 break | 0.77 | 0.55 | 0.038 | 0.26 |
| 2 breaks | 0.61 | 0.23 | 0.010 | 0.20 |

**Return regressions (Table 1, GMM on OLS moments, NW 4 lags; s.e. in parentheses).**

| Sample / regressor | $\kappa_r$ | $R^2$ | $\kappa_d$ | excess-return $\kappa$ |
|---|---:|---:|---:|---:|
| 1927–2004 raw | 0.094 (0.046) | 3.8% | 0.005 (0.037) | 0.113 |
| 1927–1991 | 0.235 (0.065) | 8.7% | 0.014 | 0.295 |
| 1992–2004 | 0.235 (0.134) | 19.9% | 0.035 | 0.241 |
| 1927–2004, 1 break | 0.235 (0.058) | 10.0% | 0.019 (0.047) | 0.282 |
| 1927–1954 / 1955–1994 / 1995–2004 | 0.510 / 0.383 / 0.532 | 16.3 / 24.0 / 54.6% | 0.037 / 0.142 / 0.226 | — |
| 1927–2004, 2 breaks | 0.455 (0.081) | 22.3% | 0.124 (0.073) | 0.441 |

- The full-sample slope is far *below* every subsample slope: pooling regimes with different means attenuates $\kappa_r$ (errors-in-variables from the mean shift). Chow p-values: 0.038 → 0.875 (1 break) and 0.003 → 0.918 (2 breaks).
- Raw-sample inference is marginal: asymptotic p 4.1% vs bootstrap 6.8%; Stambaugh bias +0.021 (0.094 → 0.115). Adjusted: bootstrap p 1.11% (1 break), 0.00% (2 breaks); bias 0.019 and 0.013 — small because $\widetilde{dp}$ is much less persistent.
- Rolling 30-year $\kappa_r$ ranges 0–0.5 raw ($R^2$ 0–34%, peak 1982); adjusted it stays ≈0.3 (1 break) or ≈0.4 (2 breaks), $R^2$ up to 40%.
- Dividend growth remains essentially unpredictable (the D/P can't reveal expected growth if it co-moves with expected returns).

**Other ratios (Tables 3–4).** E/P breaks 1990 (−0.67) or 1953/1994; B/M 1953/1990; D/E (payout) shows no significant break (sup-$F$ 5.6, >10%). With a 1991 split (1946–2004) $\Delta dp=-0.81=\Delta ep(-0.63)+\Delta de(-0.18)$: >3/4 of the D/P shift is an E/P shift, so **payout policy is not the main story**. Ex-NASDAQ D/P: breaks 1992 (−0.75) or 1954/1995; dividend growth of ex-NASDAQ firms unchanged (5.45% vs 5.46%). Repurchase-adjusted D/P (Boudoukh et al. from 1971; no SEO/IPO netting) prefers 3 breaks 1957/1973/1990.

| Predictor | raw $\kappa_r$ [$R^2$] | 1 break | 2 breaks | 3 breaks |
|---|---|---|---|---|
| $ep$ (1946–2004) | 0.119 [10.4%] | 0.214 [19.0%] | 0.216 [18.5%] | — |
| $bm$ | 0.070 [3.0%] | 0.255 [15.4%] | 0.308 [18.8%] | — |
| $dp^{nas}$ | 0.110 [4.3%] | 0.250 [10.5%] | 0.417 [18.2%] | — |
| $dp^{rep}$ | 0.191 [7.9%] | 0.282 [12.6%] | 0.361 [16.1%] | 0.576 [25.0%] |

**Economic magnitude (Table 6).** With $\bar g$ fixed, the 1991 D/P shift (−0.835) means $\bar r$ fell 8.86% → 6.29% (−2.6pp); two breaks: 9.83% → 8.16% → 6.07%. With $\bar r$ fixed: $\bar g$ 5.00% → 7.54% (two breaks 4.07/5.68/7.76%). E/P implies a similar −2.47pp in $\bar r$. These are accounting bounds, not identified decompositions. Timing matches Pástor–Stambaugh (2001) equity-premium breaks.

## Out-of-sample (Section 5, Table 5; 20-year initial window, expanding, one-year-ahead, errors in annual log return)

Pure OOS re-estimates Bai–Perron dates *and* means each year using data to $T'$ (sup-$F$ at 10%, BIC or LWZ), rebuilds $\widetilde{dp}$, regresses, and forecasts. "Random walk" = recursive historical mean return. Two pseudo-OOS diagnostics: ex-post (full-sample) Perron adjustment; and a Hamilton AR(1) regime model with full-sample regime means (2 states: −3.148, −4.044; 3 states: −2.958, −3.302, −4.078; stay-probabilities >0.9) using smoothed or real-time (filtered) state probabilities, $\widetilde{dp}^H_t=dp_t-\sum_s p_{s,t}\mu_s$. Filtered probabilities cross 50% around 1995 (2-state) and 1960/1996 (3-state).

| Forecast | MAE | RMSE |
|---|---:|---:|
| Historical mean | 0.1338 | 0.1605 |
| Raw $dp$ | 0.1411 | 0.1685 |
| Real-time Perron, sup-$F$ | 0.1350 | 0.1661 |
| Real-time Perron, LWZ | 0.1391 | 0.1680 |
| Real-time Perron, BIC | 0.1370 | 0.1646 |
| Ex-post Perron, 1 / 2 breaks | 0.1309 / 0.1158 | 0.1558 / 0.1421 |
| Hamilton smoothed, 1 / 2 breaks | 0.1286 / 0.1100 | 0.1543 / 0.1340 |
| Hamilton filtered (real-time dates, full-sample means), 1 / 2 breaks | 0.1330 / 0.1243 | 0.1590 / 0.1512 |

Real-time adjustment beats raw D/P (which is ~1%/yr worse than the mean, confirming Goyal–Welch) but **not** the historical mean. Knowing regime *levels* while learning dates in real time is enough to beat it → mean-estimation error is the bottleneck (e.g. a break detected in 2001 and dated 1995 leaves six observations to estimate the new mean). Simulated OOS (Table 5, panels 2–3, 2-break DGP): RW RMSE 0.1525–0.1533, raw $dp$ 0.1516–0.1555, ex-post adjusted 0.1334–0.1336.

## Present-value system and long horizons (Section 6)

With tilde = deviation from regime steady state: $\tilde r_{t+1}=\kappa_r\widetilde{dp}_t+\tau^r$, $\Delta\tilde d_{t+1}=\kappa_d\widetilde{dp}_t+\tau^d$, $\widetilde{dp}_{t+1}=\phi\widetilde{dp}_t+\tau^{dp}$, with
$$\kappa_r-\kappa_d=1-\rho\phi,\qquad \rho\tau^{dp}=\tau^d-\tau^r,$$
so a stationary ratio must forecast returns or growth. Annualized $H$-year slopes: $\kappa_{r}(H)=\frac{\kappa_r}{H}\frac{1-\phi^H}{1-\phi}$ (same for $\kappa_d$) — the whole horizon profile has two free parameters. Joint GMM (identity first stage; NW HAC with 4 lags for $H=1$, 5 lags for $H\in\{1,3,5\}$); $\bar r$ adjusted for the break (choice of $\bar r$ vs $\bar g$ immaterial).

| Table 7 | $\kappa_d$ | $\kappa_r$ (s.e.) | $\phi$ | PV violation | moment violation |
|---|---:|---:|---:|---:|---:|
| $H=1$, raw | 0.005 | 0.094 (0.046) | 0.945 | −0.046 | — |
| $H=1$, 1 break | 0.019 | 0.235 (0.055) | 0.813 | 0.004 | — |
| $H=1$, 2 breaks | 0.124 | 0.455 (0.079) | 0.694 | −0.001 | — |
| $H\in\{1,3,5\}$, raw | 0.021 | 0.068 (0.038) | 0.990 | 0.189 | 0.205 |
| $H\in\{1,3,5\}$, 1 break | 0.012 | 0.210 (0.043) | 0.834 | 0.076 | 0.085 |
| $H\in\{1,3,5\}$, 2 breaks | 0.080 | 0.409 (0.078) | 0.697 | 0.100 | 0.144 |

Raw univariate OLS slopes violate the PV constraint and, once long-horizon moments are imposed, raw return predictability becomes *insignificant* with $\phi=0.99$ (unit root not rejectable). With adjusted $dp$, model-implied and OLS slope term structures line up almost exactly for $H=1..10$ (Fig. 7). "Violation" columns are RMSE-type discrepancies, not p-values (caption wording is loose).

## Structural Monte Carlo (Section 7, Appendices D–E)

Expected growth $z_t$ and expected return $x_t$ are AR(1) with common root $\phi$; $\eta_{t+1}=\epsilon_{t+1}+\frac{\rho}{1-\rho\phi}(\zeta_{t+1}-\xi_{t+1})$; $dp_t-\overline{dp}=(x_t-z_t)/(1-\rho\phi)$; $\kappa_r=(1-\rho\phi)\frac{\sigma_\xi^2-\chi}{\sigma_\xi^2+\sigma_\zeta^2-2\chi}$, $\kappa_d=-(1-\rho\phi)\frac{\sigma_\zeta^2-\chi}{\sigma_\xi^2+\sigma_\zeta^2-2\chi}$. Five reduced-form moments vs six structural parameters $(\phi,\sigma_\zeta,\sigma_\xi,\sigma_\epsilon,\chi,\lambda)$ → identification by fixing $V_z=\sigma_\zeta^2/(\sigma_\xi^2+\sigma_\zeta^2-2\chi)=0.3$ ("not sensitive", no grid shown). $\rho=0.9616$; one-break $\Theta=(0.8344, 0.0182, 0.0355, 0.1371, 0.0004, -0.0005)$; two-break $(0.6974, 0.0293, 0.0635, 0.1339, 0.0014, -0.0012)$. 10,000 reps of 178 draws, 100 burn-in, mean shifts added at the historical break dates to create "unadjusted" series; 74 usable observations for $H\le5$; population $R^2$ from a 100,000-period run.

| Table 8, $\kappa_r$ at $H=1/3/5$ | slopes | $R^2$ (%) |
|---|---|---|
| 2 breaks — true | 0.456 / 0.330 / 0.249 | 20.7 / 37.0 / 38.8 |
| Sim., raw $dp$ | 0.128 / 0.089 / 0.064 | 6.2 / 11.5 / 12.8 |
| Data, raw $dp$ | 0.087 / 0.095 / 0.071 | 2.4 / 8.1 / 9.2 |
| Sim., adjusted | 0.483 / 0.340 / 0.249 | 21.4 / 37.5 / 38.6 |
| Data, adjusted | 0.442 / 0.355 / 0.231 | 20.7 / 37.4 / 30.8 |
| 1 break — true / sim adj. / data adj. ($H=1$) | 0.222 / 0.264 / 0.220 | 8.9 / 10.5 / 8.6 |

A DGP with $\kappa_r\approx0.46$ and ignored mean shifts reproduces the weak raw-D/P evidence in the data; small-sample upward bias of the adjusted slope is modest (0.042 one-break, 0.027 two-break at $H=1$).

## Critical assessment

- **Convincing:** the subsample-vs-full-sample slope pattern is a clean signature of mean shifts; break dates coincide across D/P, E/P, B/M, ex-NASDAQ and match independent equity-premium break evidence; the PV-consistent GMM is a nice discipline check.
- **Fragile:** all in-sample gains use full-sample break dates *and* means (look-ahead); number of breaks (1, 2 or 3) is weakly identified and chosen per series; 78 annual observations; ADF/Chow on data-selected breaks are overstated. The pure OOS test fails — the paper's own evidence shows the predictor is not exploitable in real time, and no costs/utility are evaluated.
- **Inconsistencies/typos:** Table 2 star legend reversed; "volatility of the adjusted series is only half as large as for the adjusted series" (should be unadjusted); first OOS forecast "1946" vs forecasting period 1947–2004; Appendix D calls the unequal-root $dp$ process ARMA(1,1) though a difference of two AR(1)s with distinct roots is generically ARMA(2,1); Table 8 caption says parameters come from pre-break estimation whereas Appendix E uses full-sample break-adjusted VECM; Appendix C leaves $\kappa$'s value blank; text says adjusted $ep$ slope ".215 in both cases" vs table 0.214/0.216.

## Practical relevance for a quant PM

- Valuation-ratio timing signals should be measured **relative to a regime/slow-moving mean**, not the full-sample mean — but the mean must be learned, and that is where real-time value is lost. Practical routes: Bayesian/shrinkage updating of regime means, Hamilton filters with priors on levels, or de-trending with long rolling means, and always compare to the recursive historical mean.
- A low full-sample D/P slope and apparent "death" of predictability can be a mean-shift artifact; check subsample slopes and Chow tests before discarding a signal.
- Imposing the Campbell–Shiller identity across horizons is a cheap diagnostic: if univariate OLS slopes violate $\kappa_r-\kappa_d=1-\rho\phi$, the predictor is likely contaminated by a nonstationary component.
