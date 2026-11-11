# Predicting Global Stock Returns

**Erik Hjalmarsson · Fed Board IFDP No. 933, June 12, 2008 (forthcoming JFQA 2010; the WP contains extra technical material) · Source file `Finance/PredictableReturns_Hjalmarsson_2010.pdf` · Monthly Global Financial Data, 40 markets (24 developed, 16 emerging/frontier), >20,000 obs; UK from 1836, eight others before 1935; samples end ≈2004:5–6**

## Claim / contribution

1. **Econometrics.** Pooling predictive regressions across countries dilutes the Stambaugh (persistent + endogenous regressor) problem *only* with a common intercept. With country fixed effects (FE), within-demeaning creates a second-order bias of order $1/T$ while the standard error shrinks at $1/(T\sqrt n)$ → severe over-rejection. Common global shocks add a further, non-vanishing distortion. Fix: **recursive (forward) demeaning** with the raw regressor as instrument, plus **projection off cross-sectional means of the predictors** (Pesaran-CCE style).
2. **Empirics.** With robust inference, the **short rate (negative) and term spread (positive) are fairly robust predictors in developed markets**; **D/P and E/P show no strong or stable predictability**. Non-robust FE tests would have "found" valuation-ratio predictability in essentially every pooled panel.

## Model

For market $i=1..n$, month $t=1..T$:
$$y_{it}=\alpha_i+\beta_i'x_{i,t-1}+\lambda_i'f_t+u_{it},\qquad x_{it}=x^0_{it}+\Gamma_i'z_t,$$
$$x^0_{it}=A_i x^0_{i,t-1}+v_{it},\quad z_t=A_g z_{t-1}+g_t,\quad A_i=I+C_i/T,\ A_g=I+C_g/T .$$
$y$ = log local-currency excess return over the local short rate; $f_t$ (return) and $g_t$ (predictor) global shocks may be correlated or identical; $u_{it},v_{it}$ contemporaneously correlated (endogeneity), cross-sectionally independent. Assumptions (App. A): $C_i$ iid, independent of everything else; factor loadings iid with fixed means; **rank condition** on the mean predictor loading $\bar\Gamma$ (common predictor trends must be recoverable from cross-sectional averages of $x$); $u$ mds, $v$ linear process, finite 4th moments. Asymptotics are **sequential** $(T\to\infty$ then $n\to\infty)$; joint limits (e.g. under $n/T\to0$) are conjectured, not proved.

## Theory

| Estimator (common $\beta$) | Limit | Comment |
|---|---|---|
| Pooled, common intercept (Thm 1) | $\sqrt n T(\hat\beta-\beta)\Rightarrow N(0,\Omega_{xx}^{-1}\Omega_{ux}\Omega_{xx}^{-1})$ | cross-sectional averaging kills the Stambaugh term; but a common $\alpha$ imposes equal equity premia (and equal mean predictors) across countries — rejected on economic grounds |
| FE (eq. 13) | $T(\hat\beta_{FE}-\beta)\to_p -\Omega_{xx}^{-1}\!\int_0^1\!\!\int_0^r E[e^{(r-s)C_i}]\,ds\,dr\,\omega_{21}$ | incidental-parameter (Nickell-type) bias; vanishes iff $\omega_{21}=0$ |
| Recursive demeaning (Thm 2) | $\sqrt n T(\hat\beta_{RD}-\beta)\Rightarrow N(0,\cdot)$ | no need to know $C_i$ |
| With common factors, pooled/FE (Thm 5) | rate only $T$, nonstandard random limit $\propto\int(\lambda'dB_f)(\Gamma'J_g)$ | FE also keeps the demeaning bias |
| Defactored RD, $\hat\beta^+_{RD}$ (Cor. 1) | $\sqrt n T(\cdot)\Rightarrow MN(0,\cdot)$ | mixed normal ⇒ $t$/Wald tests standard |

**Recursive demeaning (eqs. 14–15).** $y^{dd}_{it}=y_{it}-\frac{1}{T-t+1}\sum_{s=t}^T y_{is}$, $x^{dd}_{i,t-1}$ analogously on the lagged regressor (forward means, i.e. only data dated $\ge t$). Estimate
$$\hat\beta_{RD}=\Big(\sum_{i,t}x_{i,t-1}\,x^{dd\prime}_{i,t-1}\Big)^{-1}\sum_{i,t}x_{i,t-1}\,y^{dd}_{it},$$
using the *un-demeaned* $x_{i,t-1}$ as instrument; $u^{dd}_{it}$ depends only on future shocks, so it is orthogonal to $x_{i,t-1}$. Forward demeaning induces MA structure in residuals, handled by a panel HAC: $\hat\Omega_{ux}=\frac1n\sum_i\frac1{T^2}\sum_t\sum_s(\hat u^{dd}_{it}x_{i,t-1})(\hat u^{dd}_{is}x_{i,s-1})'$ (i.e. country-clustered scores). Cost: some efficiency loss vs an infeasible bias-corrected/fully-modified FE that would need the $C_i$.

**Defactoring (eq. 24).** $H_t=\frac1n\sum_i x_{i,t-1}$, $M_H=I-H(H'H)^{-1}H'$; premultiply each country's $Y_i$ and $X_{i,-1}$ by $M_H$, then apply FE or RD. Only predictor means are used (not mean returns, unlike Pesaran 2006): since $y$ is $I(0)$ and $x$ near-$I(1)$, $T^{-1/2}(\bar y,\bar x)$ would be asymptotically singular for $\beta\ne0$. Removing factors from the regressors suffices for mixed normality.

**Heterogeneous slopes** ($\beta_i=\beta+\eta_i$, Thm 3): if $\eta_i\perp x$, pooled estimators converge to $E\beta_i$ but only at rate $\sqrt n$ (the $\eta_i'x_{i,t-1}$ term dominates residuals); if correlated, they converge to the Phillips–Moon long-run average $\beta_{LRA}=E[\Omega_{xx,i}]^{-1}E[\Omega_{yx,i}]$, not $E\beta_i$. $t$-tests are self-standardizing, so no prior knowledge of homogeneity is needed.

**Slope-homogeneity test** (Swamy/Pesaran): weighted FE $\hat\beta_{WFE}$ with weights $1/\hat\omega_{11i}$; $S=\sum_i(\hat\beta_i-\hat\beta_{WFE})'\big(\sum_t x_{i,t-1}x_{i,t-1}'/\hat\omega_{11i}\big)(\hat\beta_i-\hat\beta_{WFE})$; $\psi=\sqrt n\,(n^{-1}S-\mu_Z)/\sigma_Z\Rightarrow N(0,1)$, reject for $\psi>1.65$. $\mu_Z$ depends on the $C_i$: evaluated at the average of median-unbiased $C_i$ (DF-GLS inversion à la Campbell–Yogo); $\sigma_Z$ replaced by the sample s.d. of country contributions. Not proved asymptotically exact; $\mu_Z$ values "available on request"; not adjusted for common factors.

## Monte Carlo ($T=100$, $n=20$, 10,000 reps, $C_i\sim U[-20,-2]$, $\alpha_i\sim N(0.005,0.005^2)$, nominal 5% two-sided)

Rejection rates under $\beta=0$ (Table 1), by corr$(u,v)=\delta$:

| Estimator | $\delta=0$ | $-0.4$ | $-0.7$ | $-0.95$ |
|---|---:|---:|---:|---:|
| A. no factor: FE | 0.078 | 0.177 | 0.379 | 0.563 |
| A. no factor: RD | 0.069 | 0.071 | 0.071 | 0.074 |
| B. factor ignored: FE | 0.430 | 0.503 | 0.559 | 0.604 |
| B. factor ignored: RD | 0.353 | 0.348 | 0.356 | 0.347 |
| C. factor removed: FE$^+$ | 0.026 | 0.065 | 0.157 | 0.284 |
| C. factor removed: RD$^+$ | 0.029 | 0.031 | 0.039 | 0.052 |

Factor DGP: $f_t=g_t\sim N(0,1)$, loadings $N(-1,1/2)$ (returns) and $N(1,1/2)$ (predictor), innovations scaled by $2^{-1/2}$. Ignoring a common factor is as damaging as ignoring endogeneity — even at $\delta=0$ the RD test rejects 35%. RD retains "decent" power (Fig. 1).

Homogeneity test (Table 2, $\beta_i=\beta+\tau\xi_i$, $\xi_i\sim N(0,1)$): size 1.4–1.6% (0.7–0.9% with factors) — conservative; power ≈44–45% (32–37%) at $\tau=0.05$, >91% at $\tau=0.1$. Low power against small heterogeneity with $n=20$.

## Data

GFD total-return indices, D/P (trailing 12m dividends / price), E/P (the text literally says "price divided by the latest 12 months of earnings" — a typo given the $e-p$ label and positive expected sign), short rate (3m T-bill, else private discount/interbank), long rate (10y govt or nearest), term spread = log(long) − log(short). All regressions monthly in logs. MSCI classification as of Feb 2008; "emerging" = emerging + frontier (Argentina, Brazil, Chile, Hungary, India, Israel, Jordan, Malaysia, Mauritius, Mexico, Philippines, Poland, South Africa, Taiwan, Thailand, Turkey). War gaps (France, Germany, Japan, UK) and Spain's missing dividends 1968–1983 → separate segments with separate intercepts, so panel "n" can exceed the number of countries. Interest-rate regressions start ≥1952 (US Fed-peg convention; author notes most countries deregulated much later, ~1980s). Unbalanced-panel adjustments are "available upon request" — not in the paper.

## Main results (Table 3, pooled; one-sided 5% robust test = $t^+_{RD}$; CY$_{sig}$ = # of country series significant by Campbell–Yogo 90% CI)

| Panel | n | obs | $\psi$ | $t_{FE}$ (naive) | $\hat\beta^+_{RD}$ | $t^+_{RD}$ | CY$_{sig}$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| E/P Global | 38 | 13,610 | 2.234 | 4.079 | 0.002 | 1.126 | 5 |
| E/P Developed | 23 | 10,151 | 1.399 | 2.866 | −0.001 | −0.802 | 2 |
| E/P Emerging | 16 | 3,518 | −1.638 | 6.252 | 0.011 | **2.438** | 4 |
| D/P Global | 46 | 20,594 | 2.485 | 3.352 | 0.001 | 0.628 | 6 |
| D/P Global 1950– | 41 | 14,947 | 1.905 | 4.742 | 0.002 | **2.334** | 7 |
| D/P Developed | 30 | 17,001 | 1.733 | 2.149 | 0.000 | −0.344 | 2 |
| D/P Developed 1950– | 25 | 11,354 | 1.263 | 4.583 | 0.002 | **2.402** | 3 |
| D/P Emerging | 16 | 3,593 | 1.156 | 2.814 | 0.005 | **1.658** | 4 |
| Short rate Developed | 23 | 11,468 | 1.341 | −4.164 | −0.958 | **−4.494** | 8 |
| Short rate Emerging | 16 | 3,792 | 1.846 | 0.604 | 0.107 | 0.484 | 3 |
| Term spread Developed | 23 | 10,784 | 1.368 | 3.869 | 1.685 | **2.809** | 10 |
| Term spread Emerging | 12 | 2,264 | 0.612 | 0.353 | −0.159 | −0.712 | 2 |

- **Homogeneity** ($\psi>1.65$): rejected for every global panel; among developed only for full-history D/P (disappears post-1950); among emerging only for the short rate → report developed/emerging separately.
- **Naive vs robust:** for valuation ratios naive $t_{FE}$ is 2–6 in every panel; robust tests mostly insignificant. For rates (less endogenous) FE and RD agree — as Campbell–Yogo found for the US.
- **E/P:** post-1950 only 4 of 38 country regressions significant (Argentina, Jordan, South Africa, UK). **D/P:** country significance scattered (post-1950 Australia, Chile, post-WWII Japan, Jordan, Mexico, Taiwan, UK, post-1950 US).
- **Short rate (developed):** negative in 20/23, beyond 1 s.e. in 15, CY-significant in 8 (Canada, Germany, Netherlands, New Zealand, Portugal, Spain, Switzerland, US). **Term spread:** CY-significant in 10/23 (Canada, France, Germany, Italy, Netherlands, New Zealand, Norway, Spain, Switzerland, US), 14 beyond 1 s.e. Emerging rate results insignificant (erratic rate regimes, e.g. Argentina).
- Coefficient units are log-variable units; in-sample monthly $R^2$ of individual rate regressions ≈1% (e.g. US short rate 1.03%, Spain 1.46%; US term spread 1.26%, Spain 1.97%).

**Stability (Fig. 2, developed expanding windows, a country enters after 5 years).** With RD$^+$: short-rate coefficient significant over the whole plotted period; term spread hovers around zero until late 1970s, consistently significant only after 1993; D/P and E/P show no stable predictability (D/P looks *weaker* over time than in the full-sample table). Country plots (Figs. 3–4): coefficients stabilize after ~1980, at or below zero for the short rate, except Japan.

## Out-of-sample (Table 5)

Countries with ≥40 years; 20-year initial window, expanding re-estimation, one-month-ahead forecasts vs the country's recursive historical mean; $R^2_{OS}=1-\sum(y-\hat y)^2/\sum(y-\bar y)^2$. **Uses ordinary FE pooled slopes (not RD$^+$**, because forward demeaning is unsuitable for forecasting) vs own-country OLS slopes; country intercepts kept.

| $100R^2_{OS}$ | own slope | pooled slope |
|---|---:|---:|
| US, short rate | −1.134 | 0.902 |
| Germany, short rate | −0.141 | 0.702 |
| Spain, short rate | 0.093 | 2.970 |
| Japan, short rate | −0.355 | −0.948 |
| Sweden, short rate | −0.894 | −1.898 |
| US, term spread | −0.544 | 0.557 |
| Italy, term spread | −0.213 | 0.546 |
| Spain, term spread | 1.939 | 1.775 |
| US, E/P | 0.435 | 0.570 |

- Short rate: of 5 CY-significant countries, pooled $R^2_{OS}>0$ in 3 (own-slope only Spain); among 10 with $|t|>1$ and right sign, pooled positive in 6 vs own-slope 1.
- Term spread: pooled $R^2_{OS}>0$ in all 7 CY-significant countries and 9/10 with $t>1$; own slope 4/7 and 5/10.
- E/P: the 3 CY-significant countries (South Africa, UK, US) are positive under both; D/P mostly negative.
- Campbell–Thompson sign restrictions are said to strengthen results "substantially" but are not reported.

## Critical assessment

- **Convincing:** the Monte Carlo makes the two failure modes (FE demeaning bias; ignored common factors) vivid and the fix simple; rate-variable evidence is consistent across pooled, country, expanding-window and OOS views.
- **Fragile/caveats:** sequential asymptotics only; homogeneity test is heuristic (plug-in $C_i$, simulated moments not tabulated) and low-powered; unbalanced-panel algorithm undisclosed; pre-deregulation interest rates may not be market rates; the OOS exercise evaluates biased FE slopes, not the proposed estimator, and selecting countries by full-sample CY significance is look-ahead — the in-sample/OOS association is descriptive only. Gains are tiny ($R^2_{OS}$ ≲1%, one case ≈3%) and no trading/utility metrics are given. Pooling can hurt individual countries (Japan, Sweden, UK).
- **Typos:** E/P definition inverted in the data section.

## Practical relevance for a quant PM

- In any cross-country (or cross-asset) panel of persistent predictors, **don't trust FE $t$-stats with country intercepts** — size can be 38–56% at nominal 5% for $\delta\in[-0.7,-0.95]$ (typical of D/P, E/P). Use forward-demeaned IV + projection on cross-sectional mean predictors, or at least cluster by date and by country.
- **Shrink country slopes toward the pooled (developed) estimate** for rate-based timing signals; it beats own-country OLS OOS in most cases. Keep developed and emerging separate.
- Valuation ratios as monthly country timing signals: weak and unstable internationally; short rate / term spread are the better-supported (still low-$R^2$) conditioning variables.
