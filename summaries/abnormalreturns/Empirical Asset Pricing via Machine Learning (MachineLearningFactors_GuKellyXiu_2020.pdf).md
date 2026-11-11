# Empirical Asset Pricing via Machine Learning

**Shihao Gu, Bryan Kelly, Dacheng Xiu · 2020 · *Review of Financial Studies* 33(5), 2223–2273 (doi:10.1093/rfs/hhaa009) · Source file `Finance/MachineLearningFactors_GuKellyXiu_2020.pdf` · CRSP NYSE/AMEX/NASDAQ, Mar 1957 – Dec 2016, ~30,000 stocks (>6,200/month); 94 characteristics × 8 macro predictors + 74 SIC2 dummies; OOS test 1987–2016**

## Claim / contribution

A controlled horse race of the "textbook" ML toolkit (OLS, penalized linear, PCR/PLS, spline GLM with group lasso, random forest, boosted trees, feed-forward nets with 1–5 layers) on the same data, the same chronological splits and the same metric, for measuring **conditional expected excess returns**. Findings:
1. Unregularized OLS on 920 predictors fails; regularization (shrinkage/dimension reduction) makes the large predictor set usable.
2. **Trees and especially neural networks win**; the gain is attributed to **nonlinear interactions** (the additive spline model, which has no interactions, gains nothing over linear).
3. **Shallow beats deep**: performance peaks at 3–4 hidden layers (low signal-to-noise, limited data).
4. All methods agree on a small set of dominant signals: **price trends (reversal, momentum), liquidity, volatility**, then valuation.
5. Economic gains are large: VW long–short decile spread on NN4 forecasts has annualized Sharpe 1.35 (vs 0.61 for OLS-3); NN3 timing of the S&P 500 raises Sharpe from 0.51 to 0.77.

## Setup

**Model.** $r_{i,t+1}=E_t(r_{i,t+1})+\epsilon_{i,t+1}$, $E_t(r_{i,t+1})=g^\star(z_{i,t})$, with $g^\star$ common across stocks and time (pooled panel). Baseline features
$$z_{i,t}=x_t\otimes c_{i,t},\qquad P=94\times(8+1)+74=920,$$
$c_{i,t}$ = 94 characteristics (61 annual, 13 quarterly, 20 monthly; based on Green–Hand–Zhang), $x_t$ = constant + 8 Welch–Goyal predictors (dp, ep, bm, ntis, tbl, tms, dfy, svar). Motivation: if $\beta_{i,t}=\theta_1 c_{i,t}$ and $\lambda_t=\theta_2 x_t$, then $E_t r_{i,t+1}=\beta_{i,t}'\lambda_t=z_{i,t}'\mathrm{vec}(\theta_1'\theta_2)$ — the linear Kronecker model nests a conditional beta-pricing model; nonlinear $g$ generalizes it.

**Data handling.** Characteristics are ranked cross-sectionally each month and mapped to $[-1,1]$; missing values set to the cross-sectional median. Publication lags: monthly characteristics ≤1 month, quarterly ≥4 months, annual ≥6 months. Sample deliberately **includes** price < \$5, share codes other than 10/11, and financials (authors say results are "qualitatively identical and quantitatively unchanged" if filtered).

**Sample splitting.** Training 1957–1974 (18 yrs), validation 1975–1986 (12 yrs), test 1987–2016 (30 yrs). Refit **annually**: training window expands by one year, validation is a rolling 12-year window, the model then forecasts the next 12 months. No k-fold CV (temporal ordering preserved).

**Loss.** Pooled equal-weighted MSE over stock-months; "+H" variants use Huber loss
$$H(x;\xi)=\begin{cases}x^2,&|x|\le\xi\\ 2\xi|x|-\xi^2,&|x|>\xi\end{cases}$$
(reported for OLS, ENet, GLM, GBRT, where it helps).

**Methods.**
- OLS (all 920) and **OLS-3** (size, B/M, 12-month momentum; Lewellen-style benchmark).
- Elastic net: penalty $\lambda(1-\rho)\sum|\theta_j|+\tfrac12\lambda\rho\sum\theta_j^2$ ($\rho=0$ lasso, $\rho=1$ ridge), accelerated proximal gradient.
- PCR (unsupervised components) vs PLS (components chosen by covariance with returns).
- "GLM": additive second-order spline expansion per predictor with **group lasso** (no interactions).
- Random forest (bagged, feature-subsampled trees) and gradient-boosted trees (shallow trees, learning-rate shrinkage).
- NN1–NN5: fully connected, ReLU, widths 32 / 32-16 / 32-16-8 / 32-16-8-4 / 32-16-8-4-2 (geometric pyramid rule). Regularization: $\ell_1$ weight penalty, Adam learning-rate shrinkage, **early stopping** on validation loss, **batch normalization**, and an **ensemble over random seeds**. Hyperparameter grids are in the Internet Appendix (not in this PDF).

**Metric.**
$$R^2_{oos}=1-\frac{\sum_{(i,t)\in\mathcal T_3}(r_{i,t+1}-\hat r_{i,t+1})^2}{\sum_{(i,t)\in\mathcal T_3} r_{i,t+1}^2},$$
benchmarked against a **zero** forecast (not demeaned). Using historical means instead inflates $R^2$ by roughly 3 pp (OLS-3 becomes 3.74%/month) because historical mean returns are such noisy forecasts. Model comparisons: modified **Diebold–Mariano** test on the time series of cross-sectionally averaged squared-error differences $d_{12,t}$ (avoids treating correlated stocks as independent), with Newey–West s.e.; Bonferroni for 12 comparisons gives a one-sided critical value of 2.64.

## Main results

**Stock-level $R^2_{oos}$ (%), Table 1 (monthly) and Table 2 (annual):**

| | OLS+H | OLS-3+H | PLS | PCR | ENet+H | GLM+H | RF | GBRT+H | NN1 | NN2 | NN3 | NN4 | NN5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Monthly, all | −3.46 | 0.16 | 0.27 | 0.26 | 0.11 | 0.19 | 0.33 | 0.34 | 0.33 | 0.39 | **0.40** | 0.39 | 0.36 |
| Monthly, top 1,000 | −11.28 | 0.31 | −0.14 | 0.06 | 0.25 | 0.14 | 0.63 | 0.52 | 0.49 | 0.62 | **0.70** | 0.67 | 0.64 |
| Monthly, bottom 1,000 | −1.30 | 0.17 | 0.42 | 0.34 | 0.20 | 0.30 | 0.35 | 0.32 | 0.38 | 0.46 | 0.45 | 0.47 | 0.42 |
| Annual, all | −34.86 | 2.50 | 2.93 | 3.08 | 1.78 | 2.60 | 3.28 | 3.09 | 2.64 | 2.70 | 3.40 | **3.60** | 2.79 |

(Table 1/2 are images in the PDF; values read by OCR, consistent with the text: 0.16, 0.11, 0.27/0.26, 0.19, 0.34/0.33, NN1 0.33, NN3 0.40, top-1,000 trees/NNs 0.52–0.70.) Subsample fits use the full-panel model. Nonlinear gains are **larger among big stocks**, arguing against a pure microcap/illiquidity story. Annual $R^2$ is roughly an order of magnitude larger than monthly.

**Model complexity (Fig. 3):** ENet selects <5 features in the first decade of the test period, 20–40 after 2000; PCR uses 20–40 components; PLS 3–6 components (often none early on); RF average depth 1–5; GBRT uses ~30 → 50 distinct characteristics.

**Diebold–Mariano (Table 3; positive = column beats row):** all regularized models beat OLS (≈3.3, Bonferroni-significant). NN3 vs OLS-3: 2.13; NN4 vs OLS-3: 2.36; NN3 vs ENet: 2.07; NN4 vs GLM: 2.68 (only NN-vs-linear comparison surviving Bonferroni besides vs OLS). Trees vs linear: at best marginal. **NN vs trees: insignificant** (e.g. NN3 vs RF 0.37). Neural nets are the best point estimate but not statistically distinguishable from trees.

**Variable importance** (drop in $R^2$ when a predictor is set to zero, averaged over refits and normalized; also sum-of-squared-partial-derivatives for NNs). Four groups dominate across all models: price trends (mom1m, mom12m, chmom, indmom, maxret, mom36m — 5 of the top 7), liquidity (turn, SD_turn, mvel1, dolvol, ill, zerotrade, baspread), risk (retvol, idiovol, beta, betasq), then valuation/fundamentals (ep, sp, agr, nincr). Rankings are stable across refits; five simulated placebo characteristics land among the least important. Most accounting variables are unimportant (at annual horizon, sic2 becomes important). Macro (Table 4): all models rate **aggregate book-to-market** important and **svar** unimportant; linear models favour dfy/tbl, nonlinear models tms and ntis.

**Marginal and interaction effects (NN3, Figs. 6–8):** expected return decreasing in size and volatility, increasing in momentum, ~zero in accruals. Penalized linear models find no size or volatility effect. Moving from median to 20th size percentile adds ≈2.4% p.a. ($0.002\times12\times100$); median to 80th volatility percentile subtracts ≈3.0% p.a. Short-term reversal is linear and strongest in small stocks, concave in large stocks (occurring mainly after positive prior-month returns); momentum and low-volatility are strongest in large stocks; size × accruals shows no interaction. Size effect stronger when aggregate bm is high and ntis low; low-vol effect strongest when valuations and issuance are high.

**Portfolio forecasts (bottom-up, $\hat r^p_{t+1}=\sum_i w^p_{i,t}\hat r_{i,t+1}$; Table 5, monthly $R^2_{oos}$ %):**

| | OLS-3 | PLS | PCR | ENet | GLM | RF | GBRT | NN1 | NN2 | NN3 | NN4 | NN5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S&P 500 | −0.22 | −0.86 | −1.55 | 0.75 | 0.71 | 1.37 | 1.40 | 1.08 | 1.13 | **1.80** | 1.63 | 1.17 |
| SMB | 0.81 | 2.09 | 0.39 | 1.72 | 2.36 | 0.57 | 0.35 | 1.40 | 1.16 | 1.31 | 1.20 | 1.27 |
| HML | 0.66 | 0.50 | 1.21 | 0.46 | 0.84 | 0.98 | 0.21 | 1.22 | 1.31 | 1.06 | 1.25 | 1.24 |
| UMD | −0.90 | −1.09 | −0.47 | 0.47 | −0.37 | 1.37 | −0.25 | −0.56 | −0.26 | 0.19 | 0.27 | 0.35 |

NN3–NN5 are positive for all 30 portfolios (S&P 500, SMB/HML/RMW/CMA/UMD and 24 size-double-sorted components); GLM positive for 22/30. Note the text says regularized linear methods "fail to outperform" constant forecasts of the S&P 500, yet ENet+H has +0.75% in the table. Replicated portfolios correlate >0.99 (S&P), 0.99/0.97/0.95/0.99/0.96 (SMB/HML/RMW/CMA/UMD) with originals. Annual bottom-up S&P $R^2$ for NN3: 15.7%.

**Market timing.** Campbell–Thompson mapping $SR^\star=\sqrt{(SR^2+R^2)/(1-R^2)}$: S&P 500 buy-and-hold 0.51 → 0.71 (NN3). Actual Campbell–Thompson timing strategy (positions scale with forecasts; max 50% leverage, no shorting for long-only portfolios; unconstrained for long–short factors) gives S&P Sharpe 0.77 (+0.26) for NN3 (Table 6). Long–short factors are harder to time; **no method beats static UMD**.

**Prediction-sorted decile portfolios (Table 7, VW, monthly %, annualized SR):**

| Model | H−L mean | SD | SR |
|---|---:|---:|---:|
| OLS-3+H | 0.94 | 5.33 | 0.61 |
| ENet+H | 0.60 | 5.37 | 0.39 |
| PCR | 1.22 | 4.82 | 0.88 |
| RF | 1.62 | 5.75 | 0.98 |
| GBRT+H | 0.99 | 4.22 | 0.81 |
| NN1 | 1.81 | 5.34 | 1.17 |
| NN3 | 2.12 | 6.13 | 1.20 |
| **NN4** | **2.26** | 5.80 | **1.35** |

NN predicted and realized decile returns match closely except in the extremes. NN4's H−L earns 27.1% p.a. with 20.1% volatility. Equal-weighted NN4: SR 2.45; excluding stocks below the NYSE 20th size percentile: 1.69. Lewellen's 7- and 15-predictor OLS improve on OLS-3 but lose to trees/NNs. Short legs are essentially flat after 2000 (Fig. 9).

**Risk and costs (Table 8, 10−1 spreads):**

| | OLS-3 VW | RF VW | NN3 VW | NN4 VW | NN4 EW |
|---|---:|---:|---:|---:|---:|
| FF5+Mom α (%/mo) | 0.39 (t=2.76) | 1.20 (3.95) | 1.52 (4.92) | **1.76 (6.00)** | 3.08 (12.28) |
| $R^2$ vs FF5+Mom (%) | 78.60 | 13.43 | 20.84 | 20.47 | 11.57 |
| Information ratio | 0.54 | 0.77 | 0.96 | 1.18 | 2.40 |
| Max DD (%) | 69.60 | 52.27 | 30.84 | 51.78 | 14.72 |
| Worst month (%) | 24.72 | 26.21 | 30.84 | 33.03 | 9.01 |
| Turnover (%/mo) | 58.20 | 133.87 | 123.50 | 126.81 | 114.17 |

Max DD is computed on cumulative **log** returns; turnover is $\frac1T\sum_t\sum_i|w_{i,t+1}-w_{i,t}(1+r_{i,t+1})/(1+\sum_j w_{j,t}r_{j,t+1})|$ (reference points: short-term reversal spread 172.6%, size spread 22.9%). NN turnover 110–130%/month. FF3 and FF5 OOS tangency Sharpe ratios are ≈0.8 and ≈1.3 (Kelly–Pruitt–Su), so large alphas vs these models are unsurprising.

**Meta-strategies:** equal-weighted average of the 11 methods' long–short portfolios: stock-level $R^2$ 0.43%, EW SR 2.49, VW SR 1.33. Selecting the best-validation model each year (NN3 11×, NN1 7×, GBRT 6×, NN2 5×, NN4 1×): $R^2$ 0.45% (insignificantly above the best NN), SR 2.42 EW / 1.23 VW.

## Critical assessment

- **Convincing:** strict chronological out-of-sample design; zero-forecast $R^2$ benchmark; DM tests that respect cross-sectional dependence; consistency across stock, portfolio and strategy levels; importance rankings robust to placebo features.
- **Caveats:**
  - Differences among trees and nets are statistically insignificant; "NN best" is a point-estimate ranking. The best model depends on the criterion (NN3 for $R^2$, NN4 for VW Sharpe and annual $R^2$).
  - Gains come largely from **short-horizon price-trend and liquidity signals**, with 110–130% monthly turnover; no transaction costs, borrow constraints or impact are modeled. VW NN4 still has a 33% worst month and ~52% log drawdown.
  - The characteristic set, macro set and architectures were chosen with hindsight of the literature; the OOS split removes estimation look-ahead, not research-design snooping.
  - Pooled equal-weighted loss emphasises small stocks, even though portfolios are VW; the loss and the portfolio objective differ.
  - Median imputation plus rank transform discards level information and may create artificial clusters.
  - Variable importance measures are predictive sensitivities with correlated inputs, not causal attributions. Nonlinear risk vs mispricing interpretation is left open.
  - Minor inconsistency: text says regularized linear models fail to beat constant S&P forecasts, but ENet+H shows +0.75%.

## Practical relevance for a quant PM

- Establishes realistic magnitudes: a good monthly stock-level $R^2$ is ≈0.3–0.4% (0.7% for large caps); benchmark against zero, not the historical mean.
- Recipe: rank-normalize characteristics, interact with a few macro states, use an expanding train / rolling validation / annual refit, ensemble over seeds and model classes (the simple average of methods is nearly as good as the best single model and more robust).
- Expect most of the lift to come from nonlinear interactions of momentum/reversal, size, liquidity and volatility. That makes the edge turnover-heavy; evaluate net of costs and with a large-cap-only universe before production.
- Bottom-up aggregation gives usable market and factor timing signals (S&P), but factor momentum (UMD) timing does not work.
