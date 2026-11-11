# Dissecting Characteristics Nonparametrically — Detailed Quantitative Research Notes

**Authors:** Joachim Freyberger (Wisconsin), Andreas Neuhierl (Olin), Michael Weber (Chicago Booth) | **Venue:** *Review of Financial Studies* 33(5), 2326–2377 (2020; online 2019), DOI 10.1093/rfs/hhz123 | **JEL:** C14, C52, C58, G12  
**Source file:** `Finance/[Review of Financial Studies vol. 33 iss. 5] Freyberger, Joachim_ Neuhierl, Andreas_ Weber, Michael_ Karolyi, - Dissecting Characteristics Nonparametrically (2019) [10.1093_rfs_hhz123] - libgen.li.pdf` (text extract; Tables 5, 8, 9 not legible in it, so some table-level numbers below are limited to what the text reports)

---

## Question

Cochrane's (2011) "multidimensional challenge": which of the hundreds of published characteristics provide *incremental* information about expected returns, conditional on the others? Sorts suffer the curse of dimensionality; Fama–MacBeth / linear panels impose linearity, are outlier-sensitive, and have no formal selection. Harvey–Liu–Zhu's $t>3$ still leaves ~150 predictors. FNW propose nonparametric selection and estimation jointly, and treat this as a "first step" before mapping survivors to factors or an SDF.

## Model

Target $m_t(c)=\mathbb{E}[R_{it}\mid C_{it-1}=c]$. Impose additivity (avoids the curse of dimensionality; rates do not deteriorate with $S$) and rank-transform each characteristic cross-sectionally to $\tilde C_{s,it-1}\in[0,1]$:

$$R_{it}=\sum_{s=1}^{S}\tilde m_{ts}(\tilde C_{s,it-1})+\varepsilon_{it},\qquad \tilde m_{ts}(\tilde c)\approx\sum_{k=1}^{L+2}\beta_{tsk}\,p_k(\tilde c).$$

$p_k$ are quadratic spline basis functions with $L$ intervals, knots at quantiles — the lowest order with continuous derivative. A constant spline is exactly a portfolio sort with $L$ bins, so this is a smooth multivariate generalisation of sorts ($L=10$ knots ≈ 11 portfolios). Ranks make results outlier-robust and measure relative, not nominal, size.

**Adaptive group LASSO** (Huang–Horowitz–Wei 2010). Step 1:

$$\tilde\beta_t=\arg\min_b\sum_{i=1}^{N}\Big(R_{it}-\sum_{s}\sum_{k}b_{sk}p_k(\tilde C_{s,it-1})\Big)^2+\lambda_1\sum_{s=1}^{S}\Big(\sum_{k=1}^{L+2}b_{sk}^2\Big)^{1/2},$$

so a whole function $\tilde m_s$ is set to zero (i.e. constant) at once. $\lambda$ chosen by the Yuan–Lin (2006) grouped BIC. Step 2 reweights the group penalties using step-1 estimates, because step 1 over-selects unless an irrepresentable-type condition holds (Meinshausen–Bühlmann; Zou) — the simulations show it does not hold in these data. Functions are identified only up to constants; plots normalise each to integrate to zero. Interactions are possible only if pre-specified (they add size × characteristic pseudo-features).

## Data

CRSP/Compustat US common stocks (NYSE/Amex/Nasdaq), July 1965–June 2014, 1,629,155 firm-months; fiscal-year $t-1$ accounting used for returns July $t$–June $t+1$; ≥2 years of Compustat history (backfill bias). 62 characteristics in Hou–Xue–Zhang groups: past returns ($r_{2-1},r_{6-2},r_{12-2},r_{12-7},r_{36-13}$), investment, profitability, intangibles, value, trading frictions (size, turnover, vol, spread, SUV, etc.).

Univariate decile sorts (EW, Table 3): 31 characteristics have hedge returns >5%/yr, 13 >10%, 36 have $t>2$; FF3 alphas barely change this (e.g. SUV $\alpha=21.88\%$, $t=11.59$; $r_{2-1}$ $-26.48\%$, $t=-8.99$; DTO $13.08\%$, $t=8.37$; Investment $-11.85\%$, $t=-6.74$; LME $-15.30\%$, $t=-5.53$).

## Results

**Selection (Table 5).** Baseline (all stocks, full sample, 20 knots) selects **13 of 62**: change in shares outstanding (ΔShrout and ΔSO), investment, size (LME), turnover, adjusted profit margin, $r_{2-1}$, $r_{12-2}$, $r_{12-7}$, closeness to 52-week high, return on cash (ROC), SUV, total volatility. In-sample EW top-minus-bottom-decile Sharpe **>3**. With 15 knots BEME, NOA and $r_{36-13}$ are added; 25 knots gives the same set. Number selected moves from 16 (10 knots) to 12 (30 knots) — more knots raise the penalty. Above the NYSE 10th size pctile, S2P enters; above the 20th, momentum is replaced by $r_{6-2}$ and only **9** characteristics survive, in-sample Sharpe **2.25**. Subsamples: 11 selected pre-1991, 14 after. Across all cuts, **41 of 62 are never selected**; only 3 are selected in every cut. Most consistent: ΔShrout, short-term reversal, momentum, 52-week high, ROC, SUV, total vol. Across specifications the paper's own summary is "9 to 16" characteristics.

Figures 1–2: DTO, idiosyncratic vol, IVC and NOA have univariate hedge returns of roughly 13%, 3%, 8%, 9% but flat conditional functions. Size is *stronger* conditionally than unconditionally (cf. Asness et al. 2018, "control your junk"); reversal and 52-week high are monotone both ways. Authors read issuance, past-return and 52-week-high effects as likely mispricing, some others possibly risk.

**Size interactions (Table 6).** Adding 61 size interactions (123 features) selects 25 (in-sample SR 3.33); about half are interactions; ROC and size-in-levels drop out. Above the q10/q20 cutoffs only $r_{2-1},r_{6-2},r_{12-2}$ × size survive (9–15 selected, SR 2.48–3.13) — interactions matter mainly among small stocks, which the authors take as reassuring for size-split multivariate regressions.

**Linear benchmark (Table 7).** Linear adaptive LASSO (same two-step machinery, BIC) selects **24** on raw characteristics (in-sample SR 1.47), **35** on ranks (2.52); Green–Hand–Zhang FDR selects **32** (1.64). Linear picks up 8 of the NP 13 plus BEME, E2P, Spread, etc. Mechanism: when true $m_s$ is curved, a linear model recruits correlated proxies to approximate curvature.

**Time variation (Figs. 6–9).** 120-month rolling estimation on the selected set: conditional size effect significant throughout; momentum shows the financial-crisis loser rebound (Daniel–Moskowitz crash); reversal and issuance effects vary over time. Consistent with the paper's motivation from McLean–Pontiff (58% post-publication decline).

**Out of sample (Table 8).** Selection once on 1965–1990 with **10 knots** (both models); then 10-year rolling estimation (first window Jan 1981–Dec 1990), monthly 1-month-ahead forecasts, EW long top 10% / short bottom 10%, Jan 1991–2014.

| | NP (11 selected) | Linear (30 selected) |
|---|---|---|
| OOS Sharpe | **2.75** | 1.06 |
| After costs | **1.56** (avg cost 1.71%/month) | 0.29 (1.54%/month) |
| Lewellen slope (realised on predicted) | 0.78 | about half |
| Cross-sectional $R^2$ | ~2% | >30% lower |

NP hedge returns are almost twice as large with lower SD; turnover slightly higher. Cross-checks: NP applied to the linear model's 30 characteristics still beats linear by a wide margin; linear applied to NP's 11 gives the same Sharpe as linear on its own 30 — so both over-selection and missing nonlinearity cost performance; on the same 11 characteristics NP's Sharpe is **~2.5×** linear. OOS from 1973 gives similar conclusions. Excluding stocks below the NYSE 10th/20th pctile, NP Sharpe falls to ~1 and linear to ~0.10; after costs both become small or negative. Costs: DeMiguel et al. (2016) proportional model $\kappa_{it}=y_t z_{it}$, $y_t$ from 3.3 (1980) linearly to 1 (2002+), $z_{it}=0.006-0.0025\,me_{it}$ (ranked size) — applied ex post, not in portfolio construction. Rolling annual re-selection (26-year window, frozen 12 months, Table 9): NP selects 14.13 on average vs 26.58 for linear, similar OOS Sharpe; NP's selected set is visibly more stable over time (Figs. 10–11).

**Simulations (Section 3).** DGP: the 13 baseline characteristics are "true," $g_s$ = fifth-order polynomials fitted to (normalised) data, residuals resampled within FF48 industry × random-period cells (preserving heteroskedasticity and cross-sectional dependence), 500 reps, NP estimated on ranks with 20 knots.

| Method | Avg # selected (true = 13), nonlinear DGP | Linear DGP |
|---|---|---|
| Adaptive group LASSO (NP) | **12.99** | 10.98 |
| Group LASSO (1-step) | 16.89 | 15.58 |
| Linear adaptive LASSO | 29.36 | 12.60 |
| Linear LASSO | 47.72 | 16.77 |
| FDR (GHZ) | 27.30 | 10.45 |
| $t>3$ | 26.40 | 10.64 |
| $t>2$ | 33.75 | 14.15 |

OOS prediction (2013–14, Table 10), $R^2$ relative to the true model: nonlinear DGP — adaptive group LASSO 88.6%, all linear methods ≤58% with ~3× RMSPE; linear DGP — NP 93.6% vs linear 97–99.9%. So allowing nonlinearity costs little when the truth is linear and gains a lot when it is not. Tuning: AIC selects 14.59, standard BIC 12.97, **10-fold CV selects 56.34** (useless for selection); knots 10–25 give 12.94–13.03; spline order 0/2 good (13.08/12.99), order 1/3/4 over-select (15.55–16.63); OOS deteriorates at 25 knots.

## Assessment

- **Convincing:** the like-for-like OOS comparison (same selection machinery, same characteristic sets swapped) cleanly separates over-selection from functional-form error; the calibrated simulation with block-resampled residuals is a template worth copying for validating any selector. The finding that linear $t$/FDR screens over-select by ~2× when effects are nonlinear and correlated is the main practical message for signal governance.
- **Fragile:** the 62 inputs are publication-selected, so absolute Sharpes are inflated (authors stress relative comparisons). Results are EW and microcap-driven: above the NYSE 20th percentile after costs, neither model survives. The simulation "truth" is the paper's own empirical selection, which favours the method. Additivity rules out learned interactions; "selected" is not risk vs mispricing. Selection counts depend on knot choice through the penalty (16 → 12 from 10 to 30 knots).
- **For a PM:** expect ~10–15 incremental characteristics, not dozens; many popular anomalies (idio vol, NOA, IVC, DTO, OA, plain ROA/ROE, beta) are subsumed by issuance, reversal/momentum, 52-week high, SUV, total vol, size. Use grouped penalties on flexible (ranked, spline) transforms; use BIC-type criteria, not CV, for selection; check the Lewellen slope for calibration; and put costs inside the optimiser, since the ex-post haircut shows the EW decile implementation is not tradable at scale.
- **Literature:** extends Lewellen (2015) and Green–Hand–Zhang (2017) with nonlinear selection; complements latent-factor approaches (IPCA, Kozak–Nagel–Santosh) that reduce dimension via factors rather than selecting characteristics.
