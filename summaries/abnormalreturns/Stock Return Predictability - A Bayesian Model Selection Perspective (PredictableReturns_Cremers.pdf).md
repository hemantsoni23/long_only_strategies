# Stock Return Predictability: A Bayesian Model Selection Perspective

**K. J. Martijn Cremers · 2002 · *Review of Financial Studies* 15(4), 1223–1249 · Source file `Finance/PredictableReturns_Cremers.pdf` (JSTOR copy) · Monthly S&P 500 excess returns (CRSP), Jan 1954–Dec 1998, $T=540$; 14 candidate predictors (Basic Economics database)**

## Claim

Selecting one "best" predictive regression ignores model uncertainty and is the source of the famous in-sample/out-of-sample disconnect. Bayesian model averaging (BMA) over all $2^{14}=16{,}384$ linear models, with priors calibrated to economically interpretable beliefs (prior expected $R^2$, residual variance, and expected number of predictors), shows: (i) the data strongly lower the probability of "no predictability" even for a skeptic; (ii) a stable core of ~6 variables (liquidity, credit spread, T-bill level and change, Fed funds–bill spread, January) gains support, while lagged returns, dividend yield and inflation lose it; (iii) the BMA forecast beats the constant model out of sample — **by a tiny margin** — whereas the models picked by adjusted $R^2$/AIC/BIC/FIC/PIC and even the modal posterior model do worse than the constant.

## Method

Each model $M$ (subset of $k_M$ predictors plus a constant, all variables standardized to mean 0 / variance 1):
$$y=Z_M\beta_M+\varepsilon,\quad \varepsilon\sim N(0,\sigma^2 I_T).$$

**Priors.** Independent inclusion probability $p$: $\pi(M)=p^{k_M}(1-p)^{14-k_M}$; $E[k]=14p$; $\pi(\text{no predictability})=(1-p)^{14}$. Zellner $g$-prior $\beta_M\mid\sigma^2\sim N\!\big(0,\ \sigma^2\varphi (Z_M'Z_M)^{-1}\big)$ (proper, so model probabilities are well defined); $\sigma^2\sim IG(s_0^2,T)$ with $E\sigma^2=Ts_0^2/(T-2)$.

**Posteriors.** $\beta_M\mid y,\sigma^2\sim N\!\big(\tfrac{\varphi}{1+\varphi}\hat\beta^{OLS}_M,\ \sigma^2\tfrac{\varphi}{1+\varphi}(Z_M'Z_M)^{-1}\big)$ — scalar shrinkage of OLS (e.g. ×1/2 for $\varphi=1$, ×16/17 for $\varphi=16$), an extra regularizer beyond averaging. $\sigma^2\mid y\sim IG(s_{1,M}^2,2T)$,
$$s_{1,M}^2=\frac{1}{2T}\Big[Ts_0^2+\mathrm{SSE}_M+\tfrac{1}{1+\varphi}\hat\beta_M'Z_M'Z_M\hat\beta_M\Big].$$
Model weight (eq. 10): $P(M\mid y)\propto \pi(M)\,(1+\varphi)^{-k_M/2}\,(s_{1,M}^{2})^{-T}$ — prior × dimension penalty × fit. (The printed exponent in eq. 10 is garbled/ambiguous — $s^{-T}$; the conjugate algebra with shape-$T$ posterior implies $(s^2_{1,M})^{-T}$. Eq. 6 for $\mathrm{Var}(\sigma^2)$ also looks misprinted; the standard value is $2T^2s_0^4/[(T-2)^2(T-4)]$.) Posterior inclusion probability of $x_j$ = sum of weights of the $2^{13}$ models containing it; BMA forecast $\hat y=\sum_M w_M z_M'\tfrac{\varphi}{1+\varphi}\hat\beta_M$.

**Calibrating $\varphi$** (key contribution). Choose $\varphi$ so that the prior-predictive $E[R^2]=1-E\big[\sigma^2/(\sigma^2+\beta'V_x\beta)\big]$ (simulate $k\sim\text{Bin}(14,p)$, $\sigma^2$, $\beta$; $V_x$ = sample covariance) hits a target:

| Investor | $E[R^2]$ | $E[\sigma^2]$ | $p$ → calibrated $\varphi$ |
|---|---:|---:|---|
| Skeptic | 1% | 0.99 | 0.05→3.25, 0.10→2.25, 0.20→1.25, 0.25→1.00 |
| Confident | 12% (≈ average of the literature) | 0.92 | 0.25→16, 0.50→7, 0.75→3.5, 0.95 (tables: 0.90)→2.5 |

Larger $p$ at fixed $E[R^2]$ ⇒ smaller $\varphi$ (many small effects vs few large ones). Larger $\varphi$ acts as a model-size penalty in this dataset (footnote 9). Results said robust to $E[\sigma^2]$ changes of a few points.

## Data

14 predictors: excess return lagged 1 and 2 months; January dummy; S&P dividend yield; S&P earnings yield; NYSE volume / NYSE price level ("liquidity"); BAA–AAA credit spread; 3m T-bill yield and its change; 10y–3m term spread; Fed funds–3m bill "yield spread"; PPI finished-goods yoy inflation and its change; industrial-production yoy growth (the three macro series lagged one extra month). Mean excess return 0.36%/month, s.d. 4.17%. AR(1): earnings yield 99.04%, D/P 98.91%, T-bill 98.42%, credit 97.35%, volume/price 96.43%. Largest |correlations| with next-month returns: yield spread −15.2%, inflation −13.8%, ΔT-bill −12.2%, IP −11.9%, T-bill −11.6%. Earnings yield correlates 92.7% with Vol/P (possible collinearity penalty); D/P's max correlation with any other predictor is 6.1%.

## In-sample results

**No-predictability probability (Table 3).**

| $E[R^2]$, $p$ | prior $P(M_0)$ | posterior $P(M_0)$ | post/prior of predictability |
|---|---:|---:|---:|
| 1%, 0.05 | 48.77% | 2.27% | 1.91 |
| 1%, 0.10 | 22.88% | 0.385% | 1.29 |
| 1%, 0.20 | 4.40% | 0.0417% | 1.05 |
| 12%, 0.25 | 1.78% | 0.000705% | 1.02 |

(The table's "posterior:prior odds" are probability ratios, not Bayes factors. The prose line that the skeptic's "belief in no predictability [is] considerably strengthened by the data" contradicts the table — it is weakened.)

**Fit and size (Tables 4–5).** Posterior-weighted $R^2$: skeptic 5.79 / 6.90 / 8.16 / 8.60% (vs prior 1%); confident 9.53 / 11.0 / 11.5 / 11.7% (vs prior 12%). Posterior expected model size: skeptic 0.70→2.57, 1.40→3.59, 2.80→5.18, 3.50→6.84; confident 3.50→6.17, 7→9.03, 10.5→11.84, 12.6→13.17. Classical selectors pick 11 (adj. $R^2$), 10 (AIC), 3 (BIC), 5 (FIC, PIC) variables — adj. $R^2$ and AIC behave like a *confident* Bayesian.

**Posterior inclusion probabilities (Table 6, %).**

| Variable | skeptic $p$=.05 | .25 | confident $p$=.25 | .90 |
|---|---:|---:|---:|---:|
| January | 60.21 | 61.45 | 71.19 | 98.82 |
| Yield spread (FF–bill) | 33.17 | 45.29 | 36.75 | 93.77 |
| ΔT-bill | 32.51 | 67.57 | 85.49 | 99.89 |
| Credit spread | 25.60 | 66.44 | 88.39 | 99.68 |
| T-bill | 25.48 | 49.01 | 69.45 | 98.92 |
| ΔInflation | 24.12 | 38.21 | 20.87 | 85.71 |
| Vol/P | 18.94 | 52.36 | 66.46 | 96.99 |
| Term spread | 4.98 | 38.02 | 62.00 | 99.17 |
| Earnings yield | 8.14 | 33.08 | 25.45 | 87.38 |
| Dividend yield | 3.99 | 24.32 | 11.88 | 87.85 |
| Inflation | 3.82 | 22.29 | 10.65 | 84.02 |
| ExRet$_{-1}$ | 2.84 | 24.10 | 18.27 | 95.85 |

Skeptic winners (posterior > prior for all $p$): Vol/P, credit, T-bill, ΔT-bill, yield spread, ΔInflation, January (the paper says both "six" and "seven"). Confident: ΔInflation swapped for term spread. D/P posterior < prior for every $p$. Posterior/prior inclusion ratios range 12.04 (January) to 0.54 (ExRet$_{-1}$) at $p=0.05$ and compress toward 1 as $p$ rises — discrimination vanishes for confident priors; the author suspects overfitting of persistent, possibly nonstationary regressors (the persistent term spread rises while the low-persistence January and ΔInflation fall as $p$ increases). Modal posterior model at $p=0.05$ contains only the yield spread and January.

## Out-of-sample (Table 8)

Five non-overlapping 5-year forecast blocks (300 months, ≈1974–1998), each estimated on the preceding 20 years; BMA uses posterior-mean $\beta$, classical winners use OLS. Metrics in standardized-return units.

| Forecaster | RMSE | MAD | Bias |
|---|---:|---:|---:|
| Constant (unconditional) | 1.093 | 0.818 | 0.072 |
| BMA, skeptic ($p$ = .05/.25/.50/.75) | 1.080 / 1.080 / 1.078 / 1.078 | 0.809–0.812 | 0.098–0.109 |
| BMA, confident ($p$ = .25/.50/.75/.90) | 1.084 / 1.080 / 1.076 / 1.076 | 0.796–0.830 | 0.031–0.124 |
| Modal model, skeptic | 1.096–1.170 | 0.819–0.907 | |
| Modal model, confident | 1.102–1.175 | 0.817–0.914 | |
| Adj. $R^2$ / AIC / BIC / FIC / PIC | 1.123 / 1.121 / 1.096 / 1.112 / 1.112 | 0.819–0.833 | |

Best BMA RMSE 1.076 vs 1.093 ⇒ MSE reduction $1-(1.076/1.093)^2\approx3.1\%$ (OOS $R^2\approx3\%$ on standardized returns). Every classical "best" model is worse than the constant (in-sample evidence overwhelming, OOS none — confirms Bossaerts–Hillion 1999). BMA beats its own modal model in every case. MAD and bias of BMA are sometimes worse than the constant. Note the skeptic OOS columns use $p$ = 0.05, 0.25, 0.50, 0.75 — different from the in-sample skeptic grid and without a stated recalibration of $\varphi$. The text's "mean squared error of adj. $R^2$ is about 3% higher" is the RMSE gap (1.123/1.093 ≈ +2.7%); the MSE gap is ≈5.6%.

## Critical assessment

- **Strong:** clean, transparent conjugate BMA; the calibration of $\varphi$ through prior $E[R^2]$ is a genuinely useful device that makes "skeptic vs believer" explicit; the modal-model vs average comparison isolates the value of carrying model uncertainty.
- **Weak:** fixed-regressor Gaussian likelihood with near-unit-root predictors (Stambaugh bias ignored — acknowledged); homoskedastic, constant coefficients within 20-year windows; the 14 variables were chosen *because* the literature found them (data snooping is only minimized conditional on the list); only 5 re-estimations; no economic evaluation (Sharpe, utility, costs); standardization details per window unspecified. Numerous label inconsistencies: $p$=0.95 vs 0.90, $E[\sigma^2]$ 0.99 (text) vs 0.98 (Table 4), sample end "1/1998" in Table 2 vs Dec 1998 in text, the skeptic adj.-$R^2$ of 4.79% at $p$=0.25 (below the 7.27% at $p$=0.20) looks like a misprint.

## Practical relevance for a quant PM

- For a many-candidate timing model, **average over specifications with a $g$-prior and explicit $R^2$ target** instead of stepwise/AIC selection; this is essentially ridge-like shrinkage plus inclusion uncertainty and is cheap for ≤20 candidates (enumerate) or via MC³ beyond.
- Calibrate the prior to a *skeptical* monthly $R^2$ (~1%); the posterior still moves toward several percent in-sample, but expect OOS gains of only a few percent of MSE.
- Rate/credit/liquidity variables dominate valuation ratios and lagged returns in 1954–1998 monthly S&P data; January seasonality is the single most robust inclusion.
- Posterior inclusion probability ≠ economic importance; check signs, forecast contributions and stability before trading.
