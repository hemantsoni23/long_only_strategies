# The Restrictions on Predictability Implied by Rational Asset Pricing Models

**Chris Kirby · 1998 · *Review of Financial Studies* 11(2), 343–382 · Source file `Finance/PredictableReturns_Kirby_1998.pdf` (JSTOR scan; Tables 1, 2, 4 are image-only and were read via OCR) · Monthly excess returns on 10 NYSE size deciles, Jul 1963–Dec 1991 ($T=342$); 5 instruments**

## Claim

Any admissible SDF pins down the **intercept, slopes and $R^2$** of a predictive regression, because an instrument-scaled position is itself a traded (managed) payoff that must be priced. This turns "is predictability rational?" into a direct GMM/Wald test comparing OLS coefficients with model-implied coefficients. Empirically, size-decile returns are **too predictable** for consumption-based models (power, Abel habit, Epstein–Zin), log utility, and constant-price-of-risk CAPM/FF3; constant-beta CAPM and especially constant-beta FF3 match much better — but largely because they inherit the (possibly data-mined) predictability of the factor returns. The cross-sectional *pattern* (small firms more predictable) is nonetheless consistent with rational pricing.

## The restriction

With $E[m_tR_t\mid\mathcal F_{t-1}]=1$ for all assets, excess return $r_t$, normalized $\tilde m_t=m_t/E[m_t]$ and any $z_{t-1}\in\mathcal F_{t-1}$: $E[\tilde m_t r_t z_{t-1}]=0$ and $E[r_t]=-\mathrm{Cov}(\tilde m_t,r_t)$, hence (eq. 8)
$$\mathrm{Cov}(r_t,z_{t-1})=-\mathrm{Cov}\big(\tilde m_t,\ r_t(z_{t-1}-\mu_z)\big).$$
The LHS is the expected payoff of a strategy holding $(z_{t-1}-\mu_z)$ units of the asset; predictability is rational only if that managed payoff carries matching systematic risk. Constant $m$ ⇒ no predictability; risk aversion does not by itself imply predictability.

For $x_{t-1}=(1,z_{t-1}')'$, $G=E[x_{t-1}x_{t-1}']$:
$$b_u=G^{-1}E[x_{t-1}r_t]\quad\text{(OLS)},\qquad b_r=-G^{-1}\mathrm{Cov}(\tilde m_t,\ r_tx_{t-1})\quad\text{(eq. 13)},$$
so $b_u-b_r=G^{-1}E[\tilde m_t r_t x_{t-1}]$ = transformed pricing errors of the original and managed payoffs (intercept included). Implied $R^2$ (eq. 15): $R_r^2=\sigma_{\tilde m, rz}'\Sigma_{zz}^{-1}\sigma_{\tilde m,rz}/\sigma_r^2$ with $\sigma_{\tilde m,rz}=\mathrm{Cov}(\tilde m_t,r_t(z_{t-1}-\mu_z))$ — "the only value of the population $R^2$ consistent with rational pricing". Each candidate SDF therefore yields its own linear forecasting model. Appendix A: the Hansen–Jagannathan bound and HJ distance are quadratic forms in $b_u,b_r$; the distance diagnostic (eq. 30) is $\hat d=[(\hat b_u-\hat b_r)'\hat G\hat\Sigma_{ix}^{-1}\hat G(\hat b_u-\hat b_r)]^{1/2}$, $\Sigma_{ix}=E[r_{it}^2x_{t-1}x_{t-1}']$; unlike $\chi^2$ statistics it does not reward a volatile SDF. Hansen–Singleton (1983) (CRRA + lognormality) and Ferson–Harvey (1991) variance ratios are special/partial cases.

## Candidate SDFs

- Power: $m_t=\frac{1}{1+\delta}(C_t/C_{t-1})^{-\gamma}$, $\gamma\in\{5,25,50\}$ (real returns, per-capita real nondurables).
- Abel habit: $m_t=\frac{1}{1+\delta}(C_t/C_{t-1})^{-\gamma}/(C_{t-1}/C_{t-2})^{1-\gamma}$.
- Epstein–Zin: $m_t=\big[\frac{1}{1+\delta}(C_t/C_{t-1})^{\rho-1}\big]^{\alpha/\rho}R_{mt}^{-(1-\alpha/\rho)}$; $\rho=-0.25$ with $\alpha\in\{-0.125,-0.5,-0.75\}$ (high EIS) and $\rho=-4$ with $\alpha\in\{-2,-8,-12\}$ (low EIS), i.e. $\alpha/\rho\in\{0.5,2,3\}$. $\alpha=0$ ⇒ log utility $m_t=1/R_{mt}$ (no consumption data, no free parameters).
- Conditional CAPM: $m_t=1-\lambda_{m,t-1}r_{mt}$, $\lambda_{m,t-1}=E[r_{mt}\mid\mathcal F]/E[r_{mt}^2\mid\mathcal F]$ — tested (i) with **constant price of risk** $\lambda$ (predictability from time-varying covariances), (ii) with **constant beta** $\beta_i=E[r_ir_m]/E[r_m^2]$ ⇒ $b_{i,r}=\beta_i b_m$ (predictable component proportional to the market's; not an SDF representation, so no HJ distance).
- FF3 analogues: $m_t=1-\lambda'f_t$, $f=(r_m,r_s,r_o)$; constant betas ⇒ $b_{i,r}=\beta_{im}b_m+\beta_{is}b_s+\beta_{io}b_o$. Kirby treats FF3 as a *diagnostic* for CAPM pricing errors (size/B/M proxy for any omitted risk; Berk 1995), not a structural model.

## Data and estimation

Instruments: $xrew_{t-1}$ (lagged excess return on EW NYSE), $jan_t$, $term_{t-1}$ (1-month holding return on 90-day bill minus 30-day bill — a return spread, not a yield slope), $prem_{t-1}$ (Baa–Aaa), $xdiv_{t-1}$ (S&P dividend yield minus 30-day bill return). Market = VW NYSE minus 30-day bill; SMB/HML-type mimicking portfolios per FF (1993).

Table 1 (monthly): decile 1 mean 0.00900, s.d. 0.0739, $\rho_1=0.128$, $\rho_{12}=0.215$; decile 10 mean 0.00348, s.d. 0.0429, $\rho_1=-0.002$; market 0.00419 / 0.0452; consumption growth 1.00096 / 0.0073 ($\rho_1=-0.377$); $prem$ and $xdiv$ highly persistent ($\rho_1$ 0.966 and 0.912; $\rho_{12}$ 0.607 and 0.480).

GMM, exactly identified per portfolio, e.g. for $m=1/R_m$ (eq. 26): $h_t=\big(m_t-\mu_m;\ (r_{it}-x_{t-1}'b_u)x_{t-1};\ [-r_{it}(m_t-\mu_m)-\mu_m x_{t-1}'b_r]x_{t-1}\big)$ (13 parameters); constant-beta systems replace the first moment with $(r_{it}-\beta_i r_{mt})r_{mt}$ and the last block with $(\beta_i r_{mt}-x_{t-1}'b_r)x_{t-1}$, so beta estimation error is accounted for. Wald test $W=T(\hat b_u-\hat b_r)'(\Omega_{\Delta b})^{-1}(\hat b_u-\hat b_r)\sim\chi^2_6$ per portfolio, $\chi^2_{60}$ jointly (full cross-portfolio covariance). HAC: Andrews (1991) quadratic-spectral kernel with AR(1)-plug-in bandwidth $1.3221(\hat\alpha T)^{1/5}$. Asymptotically equivalent to the overidentification test; an (unreported-detail) bootstrap says the Wald test is mildly conservative and better-behaved than the J-test.

## Results

Unrestricted $R^2$ (nominal) deciles 1→10: 20.3, 18.1, 16.1, 14.3, 14.0, 13.0, 12.3, 10.7, 10.1, 9.3% (real: 20.3→9.4%); most OLS slopes have $|t|>2$ (Harvey 1989 pattern).

| Model | Restricted $R^2$ (dec. 1 / dec. 10) | Individual tests | HJ distance (range) | Joint $W$ (df 60) | $p$ | Joint HJ |
|---|---|---|---|---:|---:|---:|
| Power / habit / Epstein–Zin (all parameter settings) | <1% everywhere | restricted slopes ≈ flat | similar to log (power, $\gamma$=5: 0.251–0.337) | — | — | — |
| Log utility (Table 2) | 0.0 / 0.1% | all reject ($W$ 35.2–75.0) | 0.242 (d10) – 0.328 (d4) | 149.7 | 0.000 | 0.484 |
| Const.-price CAPM (Table 3) | 0.2–0.3% | all reject | 0.239 – 0.320 | 173.1 | 0.000 | 0.481 |
| Const.-price FF3 (Table 4) | 4.5 / 0.6% | all reject ($W$ 27.7–52.8) | 0.228 – 0.294 | 224.5 | 0.000 | 0.474 |
| Const.-beta CAPM (Table 5) | 6.2 / 10.3% | most reject; d8 p=0.499, d9 p=0.938, d10 p=0.022 | n/a | 76.0 | 0.080 | n/a |
| Const.-beta FF3 (Table 6) | 15.6 / 9.3% | 8/10 reject at 5% (d4 p=0.073, d9 p=0.077) | n/a | 62.5 | 0.39 | n/a |

- Consumption-based failures are about *too little* implied predictability, not just statistical rejection: increasing $\gamma$ to 50 or decoupling EIS from risk aversion leaves restricted slopes near zero. Kirby argues predictability is a key driver of the usual Euler-equation rejections. Log utility fails equally, so consumption-data problems are not the explanation.
- Pricing errors (HJ distance, unrestricted–restricted gap) line up with size — a clue that the errors reflect omitted risk if pricing is rational.
- Constant-beta CAPM gets the cross-section **backwards**: restricted $R^2$ rises with size (6.2% → ~10%) while actual predictability falls (20% → 9%). Constant-beta FF3 restricted $R^2$: 15.6, 15.6, 15.4, 14.7, 14.2, 13.8, 12.6, 12.2, 11.1, 9.3% — reproduces the gradient and removes the size pattern in errors; joint test passes (though most individual tests still reject, with no multiple-testing adjustment).

## Interpretation and caveats

- **Inherited predictability:** in constant-beta models $b_{i,r}=\sum_k\beta_{ik}b_k$ takes factor predictability as given. If the market's predictability were due to (collective) data mining, contemporaneously correlated portfolios would still "rationally" inherit it — so choosing the market as a factor before the predictability literature does not make the test conservative (contra Ferson–Korajczyk 1995). Same logic undermines "international evidence confirms U.S. predictability" (Foster–Smith–Whaley). The real question is whether a model explains **cross-sectional differences** in predictability, which FF3 constant-beta does reasonably.
- It also explains why time-varying betas add little (Ferson–Harvey, Ferson–Korajczyk <10%): any model with the market as a factor captures much predictability with constant betas.
- Any rejection is a joint test of efficiency and the SDF; the maintained frictionless setting ignores costs and constraints; in-sample only (no OOS or trading evaluation); persistent instruments ($prem$, $xdiv$) make the 342 observations less informative than they appear; fixed $jan$ dummy technically violates stationarity (strong mixing suffices).
- Minor source inconsistencies: text says constant-beta CAPM restricted $R^2$ peaks at "10.3% for deciles 9 and 10" but Table 5 shows 10.0% for decile 9; Appendix B lists a VW NYSE index while the instrument is the EW excess return; Appendix A calls the uncentered $E[r^2xx']$ a "covariance matrix".

## Practical relevance for a quant PM

- A clean way to ask whether a timing signal is "risk": regress on the signal, then compare with the coefficients implied by a candidate SDF (or factor model with constant betas) — the gap is the pricing error of the signal-managed portfolio.
- When a factor model "explains" a timing strategy's returns via constant betas, check whether it merely passes through the factor's own predictability; the informative test is the cross-sectional gradient of predictability (e.g. small vs large caps).
- Size-decile monthly predictability from standard instruments is large in-sample (9–20% $R^2$) and not explained by consumption-based or constant-price-of-risk models.
