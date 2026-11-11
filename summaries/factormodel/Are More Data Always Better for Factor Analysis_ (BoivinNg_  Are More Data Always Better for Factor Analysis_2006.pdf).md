# Are More Data Always Better for Factor Analysis?

**Jean Boivin & Serena Ng · 2006 · *Journal of Econometrics* 132, 169–194 (doi:10.1016/j.jeconom.2005.01.027) · Source file `Finance/BoivinNg_  Are More Data Always Better for Factor Analysis_2006.pdf` · Two Monte Carlo designs + 12-month-ahead recursive forecasts from the Stock–Watson panel of 147 U.S. monthly series, 1959:1–1998:12 (evaluation 1971:1–1997:12)**

## Claim / contribution

More series can yield **worse** principal-component (PC) factors and diffusion-index forecasts. Two mechanisms: (i) cross-correlated (and heteroskedastic/noisy) idiosyncratic errors, which violate the "weak dependence" that large-$N$ theory relies on; (ii) **oversampling** — the factor that forecasts the target is dominant in a small panel but dominated in a larger one. Empirically, factors from as few as 33–46 pre-screened series, or from all 147 series reweighted by residual properties, match or beat the standard 147-series factors. First paper to study the finite-sample PC estimator with realistic cross-correlated errors (115 of 147 series have a residual correlation > 0.5 with some other series).

## Setup

$$
X_{it}=\lambda_i^{0\prime}F_t^0+e_{it}=\chi_{it}+e_{it},\qquad \Sigma_X=\Sigma_\chi+\Omega .
$$

Diffusion-index forecast: $\hat y_{t+1}=\hat\beta_0+\hat\beta_1'\hat F_{t,N}+\sum_{j=1}^p\hat\gamma_jy_{t-j+1}$. Its excess error over AR($p$) splits into the generated-regressor cost $[\hat\sigma^2_{\hat\epsilon}-\hat\sigma^2_{\epsilon,0}]$ and the gain from observed factors $[\hat\sigma^2_{\epsilon,0}-\hat\sigma^2_p]$; only the first depends on $N$. PC: $\hat F^j_t=N^{-1/2}\sum_i X_{it}v_{ij}$, $\hat\lambda_{ij}=\sqrt N v_{ij}$, $v_j$ the $j$-th eigenvector of $\hat\Sigma_X$. Consistency (Stock–Watson, Bai–Ng) needs stationary errors, non-trivial loadings and weak serial/cross correlation; with $\sqrt T/N\to0$ the estimated factors can be treated as known (Bai–Ng 2003).

**Why more $N$ can hurt — three toy arguments.**
- Heterogeneous noise: adding $N_2$ obs with variance $\sigma_2^2>\sigma_1^2$ to $N_1$ obs raises the variance of an equal-weighted mean iff $(N_1\sigma_1^2+N_2\sigma_2^2)/N^2>\sigma_1^2/N_1$.
- Duplication: with one factor and equal loadings, $\hat F_{t,N}=F_t+N^{-1}\sum_ie_{it}$. If $N_1$ series are included twice ($N=2N_1$), $\mathrm{var}(\hat F_{t,N})=\sigma^2/N_1$ — no gain.
- PC vs. ML: for fixed $N$ and diagonal $\tilde\Omega$, the ML loadings are eigenvectors of $\tilde\Omega^{-1/2}\hat\Sigma_X\tilde\Omega^{-1/2}$; PC equals ML only for scalar $\Omega$, so PC loses precision the more heteroskedastic/correlated the errors are.

## Monte Carlo 1: noisy and cross-correlated errors

Target $y_{t+1}=\sum_{j=1}^r\beta_jF^0_{jt}+\epsilon_{t+1}$ with $R^2=\kappa_y$; i.i.d. factors, loadings $\sim N(1,1)$; $N=N_1+N_2+N_3$:

$$
N_1:\ e_{it}=\sigma_1u_{it};\quad N_2:\ e_{it}=\sigma_2u_{it}\ (\sigma_2>\sigma_1);\quad N_3:\ e_{it}=\sigma_3\tilde e_{it},\ \tilde e_{it}=u_{it}+\sum_{j=1}^C\rho_{ij}u_{jt},
$$

$\rho_{ij}\sim U[0.05,0.7]$ linking each $N_3$ series to $C$ series of the clean group ($N_3$ errors can also be mutually correlated); $\tilde e$ rescaled to unit variance and $\sigma_3=\sigma_1$ so correlation is not confounded with noise; $\kappa_3=0.01$, $N_3=n_3N_1$. True $r=1,2,3$, estimated $k=1,2,3$. Grid: 3 $N_1$ × 5 $N_2$ × 10 $(N_3,C)$ × 9 $(\kappa_1,\kappa_2,\kappa_y)$ = **12,150 configurations × 1,000 replications**. $T$ is not reported.

Diagnostics:

$$
S_{F,F^0}=\frac{\mathrm{tr}\big(F^{0\prime}\hat F(\hat F'\hat F)^{-1}\hat F'F^0\big)}{\mathrm{tr}(F^{0\prime}F^0)},\quad
S_{y,y^0}=1-\frac{\sum_t(\hat y_{F^0}-\hat y_{\hat F})^2}{\sum_t\hat y_{F^0}^2},\quad
S_{\beta,\hat\beta}=\frac{\sum_t(y_{F^0}-\hat y_{\hat F})^2}{\sum_t y_{F^0}^2}\ (\text{"msey"}),
$$

plus data descriptors $\bar R^2=N^{-1}\sum_iR_i^2$ (common-component share), $R_q=R^2_{.9N}-R^2_{.1N}$ (dispersion), and $\hat\tau^*=N^{-1}\max_i\sum_j|\hat\tau_{ij}|$ as a sample proxy for the Chamberlain–Rothschild bound (largest eigenvalue of $\Omega$ ≤ max absolute row sum), which should be small and falling in $N$.

**Response surface (Table 1)** — dependent variables ×100, robust t-stats in parentheses; regression $R^2$ = .8449 / .6232 / .7184:

| Regressor | $100S_{F,F^0}$ | $100S_{y,y^0}$ | $100\,$msey |
|---|---:|---:|---:|
| $N_1$ | 0.874 (18.4) | 1.172 (20.1) | −1.214 (25.3) |
| $N_2$ / $N_2^2$ | 1.925 / −0.088 | 1.983 / −0.089 | −1.862 / 0.083 |
| $N_3$ / $N_3^2$ | −0.483 / 0.007 | −0.663 / 0.008 | 0.689 / −0.009 |
| $C$ | −0.333 (16.8) | −0.655 (25.8) | 0.649 (30.1) |
| $\hat\tau^*$ / $\hat\tau^{*2}$ | −86.5 / 180.7 | −90.4 / 358.4 | 134.4 / −309.6 |
| $\bar R^2$ / $\bar R^{2\,2}$ | 145.4 / −49.5 | 171.3 / −105.6 | −187.6 / 94.5 |
| $R_q$ / $R_q^2$ | −12.1 / −22.0 | 18.8 / −62.6 | −32.2 / 68.3 |
| $(r-k)>0$ (too few factors) | −21.9 (100.9) | −2.2 | 1.9 |
| $(k-r)>0$ (too many) | 14.4 | 6.9 | −8.2 |
| $r$ | −7.06 | 2.18 | 2.64 |

Ranges across configurations: $S_{F,F^0}$ .04–.991 (mean .603), $S_{y,y^0}$ .071–.99 (mean .740), msey .072–.964 (mean .458).

Findings: clean series always help; noisy series help at first and then hurt; $N_3$, $C$ and $\hat\tau^*$ all lower factor precision and forecast quality (+.01 in $\hat\tau^*$ lowers $100S_F$ and $100S_y$ by ≈ .86 and .90); higher $\bar R^2$ helps, higher dispersion $R_q$ hurts factor precision; under-estimating $k$ is very costly, over-estimating is not.

Paper slips: (a) the text says "a **small** $S_{F,F^0}$ indicates a small discrepancy" — by the formula and the rest of the paper, *large* $S_F$ means better recovery; (b) the $N_2$ turning point is given as $1.925/.088\approx22$, but for $aN_2+bN_2^2$ the maximum is at $a/(2|b|)\approx 11$; (c) "basis points" is used loosely for units of the ×100 statistics.

## Monte Carlo 2: oversampling (strict factor model, no cross-correlation)

$F_{mt}=0.5F_{m,t-1}+u_{mt}$, $m=1,2$; targets $y^A_{t+1}=\beta^AF_{1t}+\epsilon^A$, $y^B_{t+1}=\beta^BF_{2t}+\epsilon^B$ with equal $\beta$ and noise (equal predictability). Five series types: $N_1$: $0.8F_1$; $N_2$: $0.6F_2$; $N_3$: $0.4F_1+0.1F_2$; $N_4$: $0.1F_1+0.4F_2$; $N_5$: pure noise; error variances $1-\sum\lambda^2$ (interpretation: $F_1$ real, $F_2$ nominal; $N_1$ output/employment, $N_2$ prices, $N_3$ rates, $N_4$ stocks).

Selected Table 2 results (r = 2):

| Case | $N_1..N_5$ | $N$ | $k$ | $S_F$ | MSE $y^A$ | MSE $y^B$ |
|---|---|---:|---:|---:|---:|---:|
| 1 | 20,0,0,0,0 | 20 | 1 | 0.488 | 0.173 | 1.084 |
| 2 | 0,20,0,0,0 | 20 | 1 | 0.464 | 0.991 | 0.284 |
| 3 | 20,20,0,0,0 | 40 | 1 | 0.499 | 0.222 | 1.070 |
| 3 | 20,20,0,0,0 | 40 | 2 | **0.944** | 0.185 | 0.300 |
| 4 | 0,20,20,0,0 | 40 | 2 | 0.870 | 0.414 | 0.299 |
| 8 | 20,20,0,40,0 | 80 | 1 | 0.501 | 0.825 | 0.579 |
| 9 | 20,20,20,40,0 | 100 | 2 | 0.955 | 0.186 | 0.251 |
| 10 | 20,20,0,0,40 | 80 | 2 | 0.942 | 0.187 | 0.304 |
| 14 | 20,20,20,40,40 | 140 | 2 | 0.954 | 0.186 | 0.252 |

- With $k\ge r$, 40 informative series already give $S_F=.944$; 100 series only .955; adding 40 pure-noise series (case 10) slightly lowers it (.942).
- The factor space estimated depends on the panel: from $N_1$ alone one PC suffices for $y^A$; from $N_2$ alone one PC suffices for $y^B$ (0.284). In the mixed panel, $y^B$ needs two factors (1.070 → 0.300), and is always forecast worse than $y^A$ despite equal predictability, because more estimated factors add sampling noise. Adding $N_3$ to $N_1$ or to $N_2$ raises the relevant target's MSE relative to using the pure group alone.
- Implication: the number of factors that best describes $X$ (e.g. Bai–Ng IC) can understate the number needed to forecast a $y$ driven by non-dominant factors.

## Empirical application

Targets (12-month horizon): IP, real personal income less transfers, real manufacturing & trade sales, nonfarm payrolls (logs treated as $I(1)$); CPI, PCE deflator, core CPI, PPI finished goods (logs $I(2)$). Direct forecasts

$$
\hat y^h_{t+h\mid t}=\hat\beta_0+\hat\beta_1'\hat F_{t,N}+\sum_{j=1}^{4}\hat\gamma_jz_{t-j+1},\qquad y^h_{t+h}=100(y_{t+h}-y_t),\ z_t=100h(y_t-y_{t-1}),
$$

$p=4$ fixed, up to 6 factors, number chosen by Stock–Watson BIC with $\omega=0.001$ (usually 2); no factor lags (difference from Stock–Watson). Sample starts 1959:3–1970:1, re-estimated monthly ("rolling" in the paper's wording). Data: 13 groups; the panel is unbalanced in content (e.g. IPUT: $R^2_i$ = .01 with 3 factors, .08 with 6; PMEMP ≈ .8). Residual cross-correlation (full-sample 6-factor model): IPCD and IPCN most correlated with IPC (.66, .69), FSPCOM–FSNCOM .99; $\sum_j|\hat\tau_{ij}|$ has mean 14.62, s.d. 5.10 (average |correlation| ≈ .1); strongest in IP (group 1) and manufacturing/orders series.

**Weighting / screening rules** (first-step residual covariance $\hat\Omega$ from a 6-factor model; 3-factor robustness). Full FGLS is infeasible ($\hat\Omega$ has rank $N-k$), and the eigenvectors of $\hat\Sigma_X-\hat\Omega$ span the same space as $\hat\Sigma_X$, so they minimize a diagonally weighted criterion $W(k)=(NT)^{-1}\sum_iw_{iT}\sum_te_{it}^2$ (i.e. PCA on $x_{it}\sqrt{w_{iT}}$):
- **SWa**: $w_i=1/\hat\Omega_{ii}$ (heteroskedasticity; as in Jones 2001).
- **SWb**: $w_i=\big(N^{-1}\sum_j|\hat\Omega_{ij}|\big)^{-1}$ (cross-correlation).
- **Rule 1**: drop every series that is some other series' most-correlated residual partner (within a mutual pair keep the higher $R_i^2$) → 71 series. **Rule 2**: also drop second-most-correlated partners → 33. **1c/2c**: same with recursively estimated $\hat\Omega_t$ (real-time feasible; Rules 1/2 use full-sample information).
- **Group factors**: Real (60 series: groups 1–4, 13), Nominal (46: FX, rates, money/credit, prices), Volatile/leading (41: housing, inventories, orders, stock prices). Rule A: 3 real factors; B: 3 nominal; C: 3 volatile; D: first real + first nominal + first volatile.

**Table 3 — forecast errors relative to AR(4) (loss metric not specified beyond "forecast errors"), 6-factor first step, 1971:1–1997:12** (<1 = better than AR(4); "Real"/"Nominal" = averages over *all* real / nominal series among the 147):

| Rule | N | IP | Pers. inc. | Mfg&trade | Payrolls | **Real avg** | CPI | PCE defl. | Core CPI | PPI | **Nominal avg** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SW | 147 | 0.632 | 0.906 | 0.580 | 0.919 | 0.759 | 0.734 | 0.832 | 0.843 | 0.825 | 0.808 |
| 1 | 71 | 0.756 | 1.006 | 0.694 | 0.986 | 0.860 | 0.745 | 0.833 | 0.827 | 0.837 | 0.810 |
| 2 | 33 | 0.615 | 0.835 | 0.576 | 0.867 | 0.723 | 0.740 | 0.843 | 0.844 | 0.818 | 0.811 |
| 1c | 71 | 0.661 | 0.819 | 0.620 | 0.872 | 0.743 | 0.771 | 0.874 | 0.880 | 0.840 | 0.841 |
| 2c | 33 | 0.715 | 0.801 | 0.640 | 0.853 | 0.752 | 0.794 | 0.869 | 0.876 | 0.864 | 0.851 |
| SWa | 147 | 0.625 | 0.813 | 0.569 | **0.618** | 0.656 | 0.831 | 0.912 | 0.934 | 0.908 | 0.896 |
| SWb | 147 | **0.594** | 0.921 | 0.564 | 0.797 | 0.719 | 0.743 | 0.848 | 0.845 | 0.810 | 0.811 |
| A (real) | 60 | 1.009 | 1.008 | 1.012 | 0.983 | 1.003 | 0.789 | 0.863 | 0.853 | 0.868 | 0.843 |
| B (nominal) | 46 | 0.585 | **0.753** | 0.543 | 0.645 | **0.632** | 1.024 | 1.075 | 1.100 | 0.983 | 1.045 |
| C (volatile) | 41 | 1.019 | 1.055 | 1.035 | 0.963 | 1.018 | 0.800 | 0.893 | 0.841 | 0.882 | 0.854 |
| D (1R+1N+1V) | 60 | 0.612 | 0.750 | **0.530** | 0.813 | 0.676 | 0.789 | 0.863 | 0.890 | 0.868 | 0.852 |

Last row of the table (AR(4) absolute errors): 0.050, 0.027, 0.046, 0.017, (Real) 0.035; 0.021, 0.016, 0.019, 0.035, (Nominal) 0.023.

**Table 4 (3-factor first step):** only the residual-based rules change. Rule 2 collapses (IP 0.918, personal income 1.084, Real avg 0.937); Rule 1 improves (Real 0.804, Nominal 0.790 — best nominal average in either table); SWa Real 0.707, SWb 0.743; 2c Real 0.752. Screening is thus highly sensitive to what the first step classifies as "common".

Interpretation:
- **Nominal factors (46 series) forecast real activity best** (Real avg 0.632 vs. 0.759 for SW) — the first SW factor is real, so nominal factors are dominated in the full panel and better estimated from a panel where they dominate (oversampling of real series). Real factors (Rule A) add nothing beyond four own lags for real targets.
- For inflation, nominal factors are useless (ratios > 1; lagged prices already contain them); no rule clearly beats SW, but 33 series (Rule 2) match 147.
- Across all 147 targets (6-factor first step): SW is the single best rule for only ~10% of series (Fig. 1; SWa, SWb, B win more often but none dominates); **SWb beats SW for ~65% of series** (Fig. 2).

## Critical assessment

- **Convincing:** the mechanisms are clean and the oversampling design is a genuinely useful insight — PCA extracts what dominates the panel, not what predicts the target. The empirical point (fewer or reweighted series do as well or better) survives across targets, and the nominal-factor result for real activity is large.
- **Fragile:** (i) no standard errors or Diebold–Mariano tests for any ratio, with overlapping 12-month errors and 11 rules tried (data snooping); (ii) Rules 1, 2, SWa, SWb use full-sample residual covariances (look-ahead) — the real-time versions 1c/2c give smaller or mixed gains (Real 0.743/0.752 vs. SW 0.759; Nominal worse, 0.841/0.851 vs. 0.808); (iii) results flip with the first-step factor count (Rule 2: 0.723 → 0.937); (iv) group definitions are the authors' judgment; (v) Monte Carlo $T$ and full grid values are not reported, so Table 1 is not exactly replicable.
- Arithmetic inconsistency: Rule 1 "73 dropped, leaving 71" from 147 (147 − 73 = 74). Stated sample start "1959:3–1970:1" with first forecast target "1971:2" vs. table label 71:1–97:12 are also slightly inconsistent.

## Practical relevance for a quant PM

- For any PCA-based signal (macro factor, statistical risk model, PCA residual stat-arb), panel composition is part of the estimator: near-duplicate series (e.g. many IP sub-indices, overlapping yield maturities) inflate one direction and crowd out others. Check $\hat\tau^*$-type residual row sums and $R_i^2$ dispersion, not just $N$.
- Cheap fixes: weight columns by inverse residual row-sum (SWb) or inverse residual variance (SWa) before PCA — multiply standardized columns by $\sqrt{w_i}$; or extract factors block-by-block (e.g. nominal vs. real, sector blocks) when the target loads on a non-dominant factor.
- Choose the number of factors for the forecasting target, not for panel fit; a factor that is 3rd–6th in the full panel may be 1st in a sub-panel.
- Any screening rule must be run recursively in a backtest; the full-sample versions overstate gains.
