# Jackknifing Stock Return Predictions

**Benjamin Chiquoine, Erik Hjalmarsson · 2009 · *Journal of Empirical Finance* 16, 793–803 (doi:10.1016/j.jempfin.2009.07.003) · Source file `Finance/PredictableReturns_ChiquoineHjalmarsson_2009.pdf` · Monte Carlo + monthly S&P 500 total excess returns Feb 1872 – Dec 2005 (Campbell–Thompson data)**

## Claim / contribution

- Predictive regressions of returns on persistent, "endogenous" predictors (valuation ratios) give **upward-biased OLS slopes** (Stambaugh bias). The literature focused on valid *tests*; for forecasting and market timing the *point estimate* is what matters.
- Proposes the **block (Quenouille) jackknife** as a general bias-reduction device. It needs no AR(1) or other DGP assumption for the predictors, handles multiple predictors and overlapping (long-horizon) observations, and is trivial to implement.
- Simulations: jackknife slopes are "virtually unbiased", and for $m=3,4$ subsamples their RMSE is ≤ OLS in the single-regressor case. Empirically, jackknifed forecasts (esp. $m=3$ with Campbell–Thompson restrictions) beat OLS out of sample and give utility gains to a market timer.

## Method

Split the $T$ observations into $m$ **consecutive, non-overlapping** subsamples of length $l$ ($T=ml$). With $\hat\theta_T$ the full-sample and $\hat\theta_{l,i}$ the subsample OLS estimates (Eq. 1):
$$\hat\theta_{jack}=\frac{m}{m-1}\hat\theta_T-\frac{\sum_{i=1}^m\hat\theta_{l,i}}{m^2-m}.$$
If the bias expands as $a/T+O(T^{-2})$, the $O(T^{-1})$ terms cancel and the jackknife bias is $O(T^{-2})$ (Phillips–Yu 2005). Applied to the whole coefficient vector (intercept + slopes).

Illustration with $r_t=\mu+\beta x_{t-1}+u_t$, $x_t=\gamma+\rho x_{t-1}+v_t$, $(u_t,v_t)$ bivariate normal with covariance $\sigma_{uv}$, correlation $\delta$ (Eqs. 2–4):
$$E[\hat\beta_{OLS}-\beta]=-\frac{\sigma_{uv}}{\sigma_v^2}\,\frac{1+3\rho}{T}+O(T^{-2}).$$
For $m=2$: $\hat\beta_{jack}=2\hat\beta_T-\tfrac12(\hat\beta_{T/2,1}+\hat\beta_{T/2,2})$. The leading biases $2\cdot(\cdot)/T$ and $(\cdot)/(T/2)$ cancel (Eqs. 5–7). The paper does not propose a rule for choosing $m$; it evaluates $m=2,3,4$. Larger $m$ lowers variance with little extra bias; simulated RMSE is usually lowest at $m=4$, while empirically $m=3$ is "best on average".

## Monte Carlo evidence (10,000 paths per cell; $\mu=\beta=\gamma=0$, unit innovation variances, intercept estimated)

**Single regressor (Table 1)**, $\rho\in\{0.9,0.95,0.999\}$, $\delta\in\{-0.9,-0.95,-0.99\}$, $T\in\{100,500\}$. Bias (RMSE):

| Case | OLS | $m=2$ | $m=3$ | $m=4$ |
|---|---|---|---|---|
| $T=100,\rho=0.9,\delta=-0.9$ | 0.038 (0.069) | −0.001 (0.074) | −0.002 (0.068) | −0.002 (0.065) |
| $T=100,\rho=0.999,\delta=-0.99$ | 0.053 (0.068) | 0.002 (0.069) | 0.003 (0.057) | 0.004 (0.053) |
| $T=500,\rho=0.999,\delta=-0.99$ | 0.011 (0.014) | 0.000 (0.014) | 0.000 (0.012) | 0.000 (0.011) |

OLS is upward-biased in every cell; $m=2$ removes almost all bias at similar (slightly higher) RMSE; $m=3,4$ reduce RMSE. Fig. 1 (100,000 sims, $T=100,\rho=0.999,\delta=-0.99$): OLS density lies almost entirely right of the truth and is right-skewed; $m=2$ is centred and symmetric; $m=3,4$ are more peaked but slightly off-centre and more skewed — a visible bias–variance trade-off in $m$.

**Economic size of the bias.** Campbell–Yogo scaled slopes are typically 0.1–0.2 (annual) and 0.01–0.02 (monthly). So with 100 annual observations the OLS bias is 20–50% of the parameter, and with 500 monthly observations it can be as large as the parameter itself.

**Two regressors (Table 2)**, $A=\mathrm{diag}(a_{11},a_{22})$, return–predictor innovation correlations $\omega_{uv}$, predictor–predictor correlation $\eta_{vv}$. $T=100$, bias (RMSE):

| Design | Coef. | OLS | $m=2$ | $m=3$ | $m=4$ |
|---|---|---|---|---|---|
| $a=(0.999,0.95)$, $\omega=(-0.9,0)$, $\eta=0.4$ (≈ D/P + T-bill) | $\beta_1$ | 0.064 (0.084) | −0.004 (0.085) | −0.004 (0.072) | −0.002 (0.066) |
| | $\beta_2$ | −0.028 (0.068) | −0.001 (0.085) | −0.001 (0.075) | −0.002 (0.071) |
| $a=(0.999,0.95)$, $\omega=(-0.7,-0.7)$, $\eta=0.5$ | $\beta_1$ | 0.038 (0.062) | 0.005 (0.075) | 0.005 (0.064) | 0.007 (0.059) |
| $a=(0.999,0.999)$, $\omega=(-0.9,-0.9)$, $\eta=0.8$ | $\beta_{1,2}$ | 0.035/0.036 (0.093) | 0.002 (0.123) | 0.002/0.003 (0.106/0.105) | 0.003/0.004 (0.100) |

Note: the exogenous second regressor inherits a *negative* OLS bias through its correlation with the first. Jackknifing removes it but raises its RMSE. In the symmetric design, RMSE rises materially (0.093 → 0.100–0.123), which the text calls "only a small increase". At $T=500$ biases are essentially eliminated with RMSE close to OLS.

**Overlapping observations (Table 3):** regress $q$-period sums on $x_t$; $q=10,T=100$ (century of annual data) and $q=12,T=500$ (annual forecasts from monthly data). Bias is reduced but not removed when the overlap is large relative to $T$: at $T=100,\rho=0.999,\delta=-0.99$, OLS bias 0.435 (RMSE 0.523) vs $m=2$ 0.171 (0.515), $m=3$ 0.238 (0.462), $m=4$ 0.286 (0.463). At $T=500,q=12$, same $\rho,\delta$: OLS 0.123 (0.157) vs $m=3$ 0.019 (0.130), $m=4$ 0.024 (0.121). With a large overlap, bias reduction worsens as $m$ rises, because subsample blocks become short relative to $q$.

## Empirical application

**Data.** S&P 500 monthly simple total excess returns (T-bill after 1920, commercial paper before). Predictors in **levels**: D/P, E/P, smoothed E/P (10-yr MA real earnings / real price), B/M, 3-month T-bill (**sign flipped** so all expected slopes are positive), and D/P + T-bill jointly (Ang–Bekaert). Monthly regressions and annual regressions with overlapping monthly observations (Newey–West $t$ for annual).

**In-sample (Table 4, slopes as reported).** Jackknife estimates are generally smaller than OLS, especially for $m>2$. Forecast-sample B/M: monthly OLS 0.18 ($t$=1.96, $R^2$ 0.61%) vs 0.01 / 0.01 / 0.05 for $m=2,3,4$; annual 0.22 vs 0.04 / 0.05 / 0.10. Joint D/P + T-bill (monthly, forecast sample): D/P slope 2.91 (OLS) vs 0.10 / **−1.74** / 0.21 — the $m=3$ estimate flips sign, showing jackknife instability in short blocks. Annual in-sample $R^2$ up to 13.71% (B/M, full sample) and 16.01% (joint).

**Out-of-sample (Table 5).** Expanding-window estimates; forecasts start in 1927 or 20 years after the predictor's first observation (B/M 1946m6; T-bill and joint 1940m1). Benchmark: historical mean using all data back to 1872.
$$R^2_{OS}=1-\frac{\sum_{t=s}^T(r_t-\hat r_t)^2}{\sum_{t=s}^T(r_t-\bar r_t)^2}.$$
Campbell–Thompson restrictions: wrong-sign slopes set to 0; negative premium forecasts set to 0.

| Monthly $R^2_{OS}$ (%) | OLS unr. | $m=3$ unr. | OLS restr. | $m=2$ restr. | $m=3$ restr. | $m=4$ restr. |
|---|---:|---:|---:|---:|---:|---:|
| D/P | −0.66 | −0.62 | 0.16 | 0.44 | 0.33 | 0.36 |
| E/P | 0.12 | 0.31 | 0.24 | 0.46 | 0.37 | 0.38 |
| Smoothed E/P | 0.32 | 0.17 | 0.44 | 0.74 | 0.56 | 0.41 |
| B/M | −0.44 | 0.72 | −0.01 | 0.13 | 0.78 | 0.47 |
| T-bill (−) | 0.54 | −0.29 | 0.58 | −13.75 | 0.84 | −0.10 |
| D/P + T-bill | 0.12 | −1.22 | 0.17 | −9.21 | 1.09 | 0.22 |

- Restricted $m=3$ beats OLS for every monthly predictor. Unrestricted, no $m$ dominates, and $m=2$ blows up for the T-bill models (−13.74%, −10.50%).
- Annual (restricted): mixed. B/M 1.39 → 5.83 ($m=3$), T-bill 7.47 → 9.45, joint 7.87 → 10.40 (12.94 at $m=2$). But smoothed E/P 7.85 → 4.23 (OLS better); D/P best at $m=2$ (7.73 vs OLS 5.63).

**Portfolio choice (Table 6).** Mean–variance investor, $\gamma=3$, weight $\alpha_t=\frac1\gamma E_t r_{t+1}/\mathrm{Var}_t r_{t+1}$:
- Predictive: $\hat\alpha_t=(\hat\mu+\hat\beta x_t)/(\gamma\hat\sigma_u^2)$, $\hat\sigma_u^2$ = residual variance over a **5-year rolling window**.
- Benchmark: $\bar\alpha_t=\bar r_t/(\gamma\bar\sigma_r^2)$, $\bar\sigma_r^2$ = 5-year rolling return variance.
- Weights clipped to $[0,1.5]$. Gains are in % annualized expected return (certainty-equivalent; interpretable as the maximum fee).

| Monthly utility gain vs hist. mean (%/yr) | OLS restr. | $m=2$ | $m=3$ | $m=4$ |
|---|---:|---:|---:|---:|
| D/P | −0.43 | 0.50 | 0.08 | 0.03 |
| E/P | 0.37 | 0.65 | 0.63 | 0.71 |
| Smoothed E/P | −0.26 | −0.07 | 0.38 | 0.08 |
| B/M | −0.71 | −0.64 | 0.38 | 0.20 |
| T-bill (−) | 1.67 | 2.11 | 2.22 | 1.75 |
| D/P + T-bill | −0.65 | 0.50 | 0.89 | 2.47 |

Monthly: $m=3$ beats OLS in every case (restricted and unrestricted), with typical improvements of 50–100 bp/yr. OLS timing gains over the historical mean are often negative and rarely above 50–60 bp. Jackknife gains are comparable to Campbell–Thompson's fully theory-restricted forecasts. Annual: weaker (restricted $m=3$: D/P −0.30, B/M −0.03, smoothed E/P 0.03 vs OLS 0.52; T-bill 1.89 vs 1.53).

## Critical assessment

- **Convincing:** a simple, assumption-light correction whose bias removal is clear in simulation; the finding that better point estimates matter more for OOS use than test size; the portfolio translation shows economically meaningful differences at monthly frequency.
- **Fragile:**
  - Bias reduction ≠ MSE reduction. With multiple highly persistent endogenous predictors, or long overlaps, RMSE can rise (0.093 → 0.123 at $m=2$).
  - The choice of $m$ is unresolved and results are $m$-sensitive (sign flip of the joint D/P slope at $m=3$; $m=2$ catastrophes for T-bill forecasts). Recommending $m=3$ is an ex-post choice across the reported table.
  - The good results rely on Campbell–Thompson restrictions; unrestricted jackknife forecasts are often worse.
  - No standard errors for $R^2_{OS}$ differences or utility gains (no Clark–West/DM tests); a single market, US, pre-2006 sample; no costs.
  - The cancellation argument assumes a common bias expansion across blocks; structural breaks across the 130-year sample (e.g. in D/P dynamics) violate this, and block estimates then differ for economic rather than finite-sample reasons.
  - Implementation details (treatment of $T$ not divisible by $m$, handling of overlapping observations at block boundaries) are unspecified.

## Practical relevance for a quant PM

- A drop-in fix for any time-series forecasting regression with a persistent regressor (valuation, yield, spread timing): fit on the full window plus $m$ contiguous sub-windows and combine with the jackknife weights. No AR model for the predictor is needed and it works with several regressors.
- Pair with economic-sign and non-negativity restrictions and with shrinkage. Report results across $m$ rather than picking one; check stability of signs across blocks.
- Expect gains mainly at monthly frequency and short overlaps; for long-horizon overlapping regressions, keep blocks long relative to the horizon.
