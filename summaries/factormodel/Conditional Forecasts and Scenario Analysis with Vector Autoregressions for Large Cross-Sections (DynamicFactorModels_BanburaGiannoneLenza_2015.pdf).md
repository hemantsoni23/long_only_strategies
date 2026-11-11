# Conditional Forecasts and Scenario Analysis with Vector Autoregressions for Large Cross-Sections

**Marta Bańbura, Domenico Giannone, Michele Lenza · 2015 · *International Journal of Forecasting* 31, 739–756 (doi 10.1016/j.ijforecast.2014.08.013) · Source: `Finance/DynamicFactorModels_BanburaGiannoneLenza_2015.pdf` · Data: 26 quarterly euro-area macro/financial series, 1995Q1–2012Q4**

## Claim / contribution

1. **Algorithm.** Conditional forecasts (projections of some variables on assumed future paths of others) for *any* linear Gaussian state-space model are computed by treating the unconstrained future values as **missing data** and running the Kalman filter/smoother; the full predictive distribution comes from a simulation smoother. Building on Clarida–Coyle (1984), this makes the problem recursive: the largest matrix inverted does not depend on the horizon, unlike Waggoner–Zha (1999) (and Jarociński 2010), whose cost scales with the number of restrictions.
2. **Empirics.** A BVAR in (log-)levels, a BVAR in differences and a 3-factor DFM on the same 26 euro-area series give (i) similar, highly correlated unconditional forecasts that beat a random walk for most real/credit variables at short horizons; (ii) similar scenario responses to a world-GDP shock; (iii) conditional forecasts given only real GDP, HICP and the short rate that track most other variables well — "only a few sources drive the bulk of fluctuations" — with post-2008 breakdowns in money and credit.

## Models

**VAR.** $y_t=c+A_1y_{t-1}+\dots+A_py_{t-p}+\varepsilon_t$, $\varepsilon_t\sim N(0,\Sigma)$: $pn^2+n(n+1)/2+n$ parameters (4 lags: 171 for $n=6$; roughly 2k, 10k, 50k for $n=20,50,100$).

**DFM** (on stationary, standardized $\Delta y_t$):
$$\Delta y_t=\nu+\Lambda F_t+e_t,\qquad F_t=\Phi_1F_{t-1}+\dots+\Phi_sF_{t-s}+u_t,$$
$u_t\sim N(0,Q)$, $e_t\sim N(0,\Gamma_d)$ with $\Gamma_d$ diagonal (exact-factor QML likelihood). By Doz–Giannone–Reichlin (2012) QML is consistent for *approximate* factor models (weakly cross-correlated $e_t$, pervasive factors) with no restriction on $n$ relative to $T$.

**Specifications.** DFM: $r=3$ factors (meant to capture real activity, prices, interest rates — a judgment call, not a selection criterion), factor VAR with $s=4$. BVAR in differences: 4 lags; BVAR in levels: 5 lags (to match the differenced dynamics).

### DFM estimation (EM, Appendix B.1)
- Initialize with principal components of standardized data: eigen-decompose $\frac1T\sum\Delta y_t\Delta y_t'$ ($d_1\ge\dots\ge d_n$, eigenvectors $v_j$), $z_{jt}=v_j'\Delta y_t/\sqrt{d_j}$ (unit variance). OLS of $\Delta y_t$ on $z_t$ gives $\Lambda^{(0)}$; $\operatorname{tr}\Gamma_d^{(0)}=d_{r+1}+\dots+d_n$; factor VAR by OLS. One Kalman-smoother pass from these = the Doz et al. (2011) two-step estimator; iterating = QML via EM.
- E-step: Kalman smoother gives $\hat F_t$ and $V_{l,t}=E[(F_t-\hat F_t)(F_{t-l}-\hat F_{t-l})']$. M-step ($s=1$):
$$\hat\Lambda=\Big(\sum_t\Delta y_t\hat F_t'\Big)\Big(\sum_t\hat F_t\hat F_t'+V_{0,t}\Big)^{-1},\quad
\hat\Gamma_d=\tfrac1T\operatorname{diag}\Big(\sum_t\Delta y_t\Delta y_t'-\hat\Lambda\sum_t\hat F_t\Delta y_t'\Big),$$
$$\hat\Phi_1=\Big(\sum_{t\ge2}\hat F_t\hat F_{t-1}'+V_{1,t}\Big)\Big(\sum_{t\ge2}\hat F_{t-1}\hat F_{t-1}'+V_{0,t-1}\Big)^{-1},\quad
\hat Q=\tfrac{1}{T-1}\Big(\sum_{t\ge2}\hat F_t\hat F_t'+V_{0,t}-\hat\Phi_1\sum_{t\ge2}\hat F_{t-1}\hat F_t'+V_{1,t}'\Big).$$
  The covariance corrections $V$ are what distinguish EM from "regress on smoothed factors". Likelihood rises monotonically → local maximum only. Standardization matters for PC initialization (PCs are not scale-invariant; QML is); rescale $\hat\Lambda,\hat\Gamma_d$ afterwards. No stopping tolerance is reported.

### BVAR (Appendix B.2; Giannone–Lenza–Primiceri 2015 hierarchical approach)
- Normal–inverse-Wishart Minnesota prior centered on independent random walks: $E[(A_s)_{ij}]=1$ if $i=j,s=1$, else 0;
$$\operatorname{cov}[(A_s)_{ij},(A_r)_{hm}\mid\Sigma,\lambda,\Psi]=\lambda^2\frac{1}{s^2}\frac{\Sigma_{ih}}{\Psi_{jj}}\ \text{if } m=j,\ r=s;\ 0 \text{ otherwise}.$$
  $\Sigma\sim IW(\Psi,d)$, $d=n+2$ (minimum for $E[\Sigma]=\Psi$ to exist), $\Psi$ diagonal; diffuse intercept.
- **Sum-of-coefficients** prior (Doan–Litterman–Sims 1984), tightness $\mu$: in ECM form $\Delta y_t=c+\Pi y_{t-1}+\sum B_s\Delta y_{t-s}+\varepsilon_t$, shrinks $\Pi\to0$ ($\mu\to0$ = exact differencing). **Dummy-initial-observation** prior (Sims 1993; Sims–Zha 1998), tightness $\delta$. Dummies: $Y_\mu=\operatorname{diag}(\bar y_0)/\mu$, $X_\mu=[0_n,\ \mathbf 1_p'\otimes\operatorname{diag}(\bar y_0)]/\mu$; $Y_\delta=\bar y_0'/\delta$, $X_\delta=[1,\ \mathbf 1_p'\otimes\bar y_0']/\delta$ ($\bar y_0$ = mean of first $p$ obs.). Marginal likelihood = ML(augmented data)/ML(dummies only).
- Posterior: $\beta\mid\Sigma,Y\sim N(\hat\beta,\Sigma\otimes(x'x+\Omega^{-1})^{-1})$, $\hat B=(x'x+\Omega^{-1})^{-1}(x'y+\Omega^{-1}\hat b)$; $\Sigma\mid Y\sim IW(\Psi+\hat\varepsilon'\hat\varepsilon+(\hat B-\hat b)'\Omega^{-1}(\hat B-\hat b),\,T-p+d)$. Closed-form marginal likelihood $p(Y\mid\Psi,\lambda)$ → Metropolis–Hastings on hyperparameters, then conjugate draws of $(\Sigma,\beta)$.
- Hyperpriors: $\lambda\sim$ Gamma (mode 0.2, sd 0.4); $\Psi_{jj}\sim$ inverse-Gamma (scale = shape = $0.02^2$); $\mu,\delta\sim$ Gamma (mode 1, sd 1). BVAR in differences: prior mean 0 (white-noise changes), common $\Psi=\bar\psi I_n$ on standardized data.

### Why BVAR ≈ DFM (Section 2.3; De Mol–Giannone–Reichlin 2008)
Rewrite the differenced VAR on principal components, $\Delta y_t=\sum_s B_sH^{-1}z_{t-s}+\varepsilon_t$. Uniform shrinkage on $B_s$ is *non-uniform* on PC coefficients: prior variance $\propto\lambda^2d_j$. Under an approximate factor structure $d_1..d_r$ grow at rate $n$, $d_{r+1}..d_n$ no faster than $n/\sqrt T$. With
$$\lambda^2=\kappa\,\frac{\sqrt T}{n}\,\frac{1}{T^{\delta}},\qquad 0<\delta<\tfrac12,$$
$\lambda^2d_j\to\infty$ for $j\le r$ (flat prior on factor directions) and $\to0$ for $j>r$; the shrinkage forecast then converges to the infeasible observed-factor forecast. This is an asymptotic rationale — empirically $\lambda$ is learned hierarchically, and finite-sample shrinkage attenuates weak directions smoothly rather than truncating them.

## Conditional forecasting algorithm (Section 3)

State space: $Z_t=C_tS_t+v_t$, $S_{t+1}=G_tS_t+w_t$, $v_t\sim N(0,R_t)$, $w_t\sim N(0,H_t)$. VAR: companion state $S_t=(Y_t',\dots,Y_{t-p+1}')'$, $C_t=(I_n,0)$, $R_t=0$, $\Sigma$ in the top block of $H_t$ (intercept moved into the transition as a constant $\bar c_t$ for speed). DFM: $Z_t=\Delta y_t$, state = stacked factor lags (+ $\nu$), $R_t=\Gamma_d$.

Information set $\Omega=\{Z_{l,t}: l\in I, t\le t_0\}\cup\{Z_{l,t}: l\notin I, t=1..T\}$ — conditioning variables known through $T$, others missing after $t_0$. Drop missing rows of $Z_t,C_t$ (rows/cols of $R_t$) — equivalently set their measurement variance to "∞" (Giannone–Reichlin–Small 2005). The Kalman smoother then gives conditional point forecasts; a draw $j$ of the distribution:
1. draw parameters from the posterior;
2. draw states $S_t\mid\Omega$ with a simulation smoother on the modified system;
3. draw missing measurement errors $v_{i,t}\mid$ observed ones (identically 0 for a VAR);
4. $Z_{i,t}=(C_t)_{i\cdot}S_t+v_{i,t}$.

Smoothing (not filtering) is essential: a restriction at $t_0+8$ informs the path at $t_0+1$. Optional (fn. 13): let the scenario update parameters by iterating steps 1–4 treating the latest conditional forecasts as data — a different target distribution than the frozen pre-scenario posterior.

**Linear-combination conditions** $W_tZ_t$: augment $\check Z_t=(W_tZ_t;Z_t)$, $\check C_t=(W_tC_t;C_t)$, $\check R_t=\begin{pmatrix}W_tR_tW_t'&W_tR_t\\R_tW_t'&R_t\end{pmatrix}$ (preserves dependence between aggregate and components).

**Structural scenarios.** With $\varepsilon_t=\Gamma\eta_t=\sum_i\gamma_i\eta_{i,t}$, $\Gamma\Gamma'=\Sigma$, zeroing shocks $1..s$ = replace $\Sigma$ by $\bar\Sigma=\sum_{i>s}\gamma_i\gamma_i'$ (DFM: same on $Q$). Conditions must be compatible with the reduced-rank $\bar\Sigma$ (e.g. triangular $\Gamma$: cannot impose $\eta_{1,t}=0$ and $\varepsilon_{1,t}\neq0$). Reduced-form conditioning instead averages over all shock combinations consistent with the path (invariant to identification, Waggoner–Zha). Recursive IRFs are a special case (eq. 6): IRF$_{ij}$ = conditional forecast with $\epsilon_{1..i-1,t}=0$, $\epsilon_{i,t}=\gamma_{ii}$ minus unconditional forecast; for $i=1$ this is a generalized IRF (Koop–Pesaran–Potter; Pesaran–Shin).

**Comparison with Waggoner–Zha.** WZ draws the whole shock path satisfying the restrictions: inversion of a $q\times q$ matrix, $q=(n-\#I)(T-t_0)$ restrictions, plus a spectral decomposition of an $n(T-t_0)\times n(T-t_0)$ matrix; Jarociński (2010) reduces this to an SVD of a $q\times n(T-t_0)$ matrix, still growing with $q$.

### Simulation smoothers (Appendix A)
- **Carter–Kohn**: backward sampling, needs (pseudo-)inversions and SVDs of $np\times np$ matrices.
- **Durbin–Koopman (2002)**: simulate $(\tilde S_t,\tilde Z_t)$ unconditionally; smooth $Z_t^*=Z_t-\tilde Z_t$ (with $S_0^*=0$, $\bar c_t=0$); draw $=E[S_t\mid Z^*]+\tilde S_t$. With the **de Jong (1988)** smoother only $F_t$ (size $\le n-\#I$) is inverted:
$E_t=Z_t^*-C_tS^*_{t|t-1}$, $F_t=C_tP_{t|t-1}C_t'+R_t$, $K_t=P_{t|t-1}C_t'F_t^{-1}$, $L_t=I-K_tC_t$; backward $r_{t-1}=C_t'F_t^{-1}E_t+L_t'r_t$, $r_T=0$, $S^*_{t|T}=S^*_{t|t-1}+P_{t|t-1}r_{t-1}$.
  *Reproduction note:* with this filter convention ($K_t$ a filtering gain, prediction $S_{t+1|t}=G_tS_{t|t}+\bar c_t$) the backward step needs the transition, i.e. $\mathcal L_t=G_t(I-K_tC_t)$ in place of $L_t$; the printed recursion omits $G_t'$. Also, the printed $\hat Q$ update writes "$\hat A$" for $\hat\Phi_1$. Both look like typos.
- Run only over $t>t_0$, initializing $S_0=(Y_{t_0}',\dots,Y_{t_0-p+1}')'$, $S_{1|0}=G_0S_0+\bar c_0$, $P_{1|0}=H_0$.

**Table A.1** — seconds per conditional-forecast draw, 26-variable VAR (Matlab R2008a, Intel Core Duo ~2925 MHz, 4.1 GB; average of 1000 reps):

| $p$, $n-\#I$, $T-t_0$ | CK | DK+Hamilton | DK+de Jong | WZ/Jarociński |
|---|---|---|---|---|
| 2, 5, 5 | 0.04 | 0.02 | 0.01 | 0.01 |
| 2, 25, 60 | 0.40 | 0.26 | 0.08 | 39.25 |
| 5, 5, 5 | 0.26 | 0.16 | 0.03 | 0.02 |
| 5, 5, 60 | 3.46 | 2.20 | 0.33 | 2.40 |
| 5, 25, 60 | 3.69 | 2.15 | 0.39 | 39.67 |

WZ/J is competitive only for few restrictions and is invariant to $p$; Kalman methods scale with $p$ but barely with the number of conditioning variables. Extreme case: WZ ≈ 11 h per 1000 draws vs "1–7 min" for DK/de Jong (~100× in the 5/25/60 cell). DK/de Jong is the fastest Kalman method in every cell and is used throughout.

## Data and evaluation design
26 series (AWM 13th update, ECB SDW, Eurostat, Datastream, IMF): world GDP; euro-area GDP, consumption, government consumption, investment, exports, imports, employment, unemployment rate, economic sentiment; oil and non-oil commodity prices; HICP, PPI ex construction, GDP and import deflators, compensation per employee; US 3m LIBOR, 3m EURIBOR, 10y yield; M1, M3, loans to households, loans to NFCs; nominal effective exchange rate; Euro Stoxx. Transformations: $4\times\log$ levels for most; unemployment raw; sentiment and interest rates raw/100. Differenced models first-difference everything → annualized quarterly changes in decimals.

Unconditional evaluation: origins 2004Q1–2012Q4, $h=1,2,4$, expanding window from 1995Q1, full re-estimation (incl. posterior-mode hyperparameters) each step; BVAR point forecasts at the posterior mode (chain rule), DFM via Kalman filter. Target $m^h_{i,t+h}=\frac{100}{h}(y_{i,t+h}-y_{i,t})$ ≈ average annualized % growth. Benchmark: random walk with drift in (log-)levels — the BVAR's dogmatic-prior limit; univariate AR benchmarks reportedly give "very similar outcomes" (not tabulated).

## Main results

**Table 1 (selected) — MSFE ratio vs random walk, $h=1/2/4$:**

| Variable | BVAR levels | BVAR diff. | DFM |
|---|---|---|---|
| Global GDP | 0.61/0.67/0.76 | 0.65/0.69/0.69 | 0.60/0.62/0.63 |
| Real GDP | 0.59/0.78/1.00 | 0.53/0.73/0.88 | 0.56/0.71/0.84 |
| Real consumption | 0.39/0.21/0.27 | 0.41/0.28/0.36 | 0.55/0.41/0.64 |
| Government consumption | 0.54/0.43/0.31 | 0.59/0.44/0.37 | 0.85/0.85/0.91 |
| Employment | 0.16/0.21/0.35 | 0.16/0.20/0.33 | 0.17/0.19/0.33 |
| Unemployment rate | 0.39/0.50/0.72 | 0.35/0.46/0.66 | 0.30/0.40/0.61 |
| Oil price | 1.08/1.34/1.52 | 1.28/1.65/1.79 | 1.93/2.89/3.44 |
| HICP | 1.00/1.42/2.54 | 0.96/1.28/1.79 | 1.55/2.28/3.25 |
| Short-term rate | 0.67/0.94/1.46 | 0.57/0.92/1.64 | 0.72/1.18/1.75 |
| Long-term rate | 0.90/1.01/1.58 | 1.05/1.30/1.64 | 1.08/1.26/1.62 |
| M1 | 0.57/0.60/0.90 | 0.60/0.69/1.23 | 0.89/1.22/1.74 |
| Loans to firms | 0.06/0.09/0.26 | 0.07/0.10/0.25 | 0.15/0.20/0.41 |
| Effective exchange rate | 1.33/1.50/2.13 | 1.38/1.39/1.59 | 1.29/1.43/1.76 |
| Stock prices | 0.83/0.93/1.21 | 0.88/1.02/1.05 | 0.90/1.12/1.50 |

Ratios are of *squared* errors (0.53 ⇒ RMSE ratio ≈ 0.73). Big wins for real activity, labour, credit, M3; failures for commodity prices, the exchange rate, inflation measures (anchored expectations in EMU make the RW hard to beat) and long-horizon rates. The DFM is generally the weakest on nominal variables. Fig. 1: forecasts of the three models are highly correlated across variables (graph only). No tests of equal predictive accuracy or intervals on the ratios.

**Scenario: world GDP +0.1 pp on impact** (full-sample estimation; world GDP at $T+1$ set to its unconditional forecast + 0.1 pp, all else free; response = conditional − unconditional forecast = generalized IRF; 8 quarters). World GDP 0.1% higher on impact, keeps rising for a year, then drifts back; euro-area GDP, exports, imports, unemployment mirror it; HICP peaks after ~1 year; short rate rises (systematic policy) then reverts; BVAR long rates barely move (term spread falls) — **the DFM differs here**; household loans coincident with GDP, firm loans lag; M1 falls (trough after 1–1.5 years, liquidity effect), M3 up via M3–M1 short-term assets. BVAR bands: 25,000 posterior draws, first 5,000 discarded, one *point* conditional forecast per draw (parameter uncertainty only), 5–95% shown; DFM at ML estimates. Validity requires the scenario to be small enough to avoid Lucas-critique shifts.

**Conditional forecasts given realized real GDP, HICP, short rate, 1997–2012** (parameters 1995–2007; 1995–96 initial conditions ⇒ 1997–2007 "in-sample", 2008–2012 "out-of-sample"). Bands here are draws of the conditional forecast (parameter + future-shock uncertainty). Most variables are tracked closely, especially in-sample ⇒ roughly three dimensions capture most of the economy (cf. Giannone–Reichlin–Sala 2004 for the US). Poorly tracked even in-sample: wages, GDP deflator, government consumption, effective exchange rate. Post-2008: money and credit much more subdued than the pre-crisis relations imply; models also disagree more on these variables — evidence of instability confined to a few blocks.

## Critical assessment
- **Convincing:** the missing-data/Kalman formulation is exact for linear Gaussian models, general (any state-space model, any missing pattern, linear combinations, structural subsets) and demonstrably fast; the BVAR–DFM agreement is consistent with the De Mol et al. theory.
- **Fragile/limited:** one short evaluation sample (36 origins, incl. the crisis) without significance tests; DFM factor number chosen by judgment; scenario responses are reduced-form associations, not causal effects; the 2008–12 "out-of-sample" exercise feeds in realized GDP/HICP/rates, so it is a stability check, not a forecast; Figs. 2 and 3 bands measure different uncertainty (parameter-only vs full predictive). Gaussian, linear, constant-parameter — no stochastic volatility (they cite Carriero–Clark–Marcellino as improving accuracy), regime change or nonlinear constraints. Unit handling of the "+0.1 pp" shock on $4\log$ data vs "0.1% level" in the figure should be reconciled in a replication.
- **Typos:** missing $G_t'$ in the printed de Jong backward recursion (as written); $\hat A$ for $\hat\Phi_1$ in the $\hat Q$ update; unhatted $F_t$ in some M-step sums.

## Practical relevance for a quant PM
- A cheap, exact engine for **macro scenario generation**: specify paths (or linear combinations, e.g. a spread or an average) for a handful of drivers and obtain the coherent joint distribution of everything else — directly usable for stress tests or conditional return/factor forecasts if asset returns are added to the state space.
- Implementation recipe: large BVAR with hierarchical Minnesota prior (or a small-$r$ DFM) → state space → drop missing rows → Durbin–Koopman/de Jong simulation smoother per posterior draw. Verify on a small case against the closed-form Gaussian conditioning $\mu_c=\mu+VA'(AVA')^{-1}(a-A\mu)$; exact constraints must hold to machine precision.
- The large MSFE gains for credit and real variables and the failures for commodities, FX and equity prices are a reminder that such models are informative on slow macro aggregates, not on asset prices themselves; use them to condition risk scenarios, not as return forecasters.
