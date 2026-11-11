# Kernel Trick for the Cross-Section

**Serhiy Kozak (University of Michigan) · 2019 · Preliminary working paper (6 Apr 2019; first draft 27 Dec 2018; SSRN 3307895), 44 pp. · Source file `Finance/MachineLearning_Kozak_2019.pdf` · Daily CRSP returns 1 Nov 1973 – 29 Dec 2017; 5 Fama–French–Carhart characteristics and 40 anomaly characteristics; stocks above 0.01% of aggregate market cap**

## Claim / contribution

- Characteristic-based SDFs usually assume risk prices are **linear** in a few characteristics. Present-value identities (e.g. the clean-surplus identity $M_t/B_t=\frac1{B_t}\sum_\tau E(Y_{t+\tau}-\Delta B_{t+\tau})/(1+r)^\tau$) imply expected returns are highly **nonlinear** and interactive in B/M, profitability and investment.
- Explicitly adding interactions explodes dimension (100 characteristics → 5,050 second-order terms). The paper applies the **kernel trick** to the *characteristics* that define managed portfolios. PCA over an arbitrarily large, even infinite, set of nonlinear characteristic-managed portfolios is then done through a $T\times T$ matrix, at a cost that does not grow with interaction order.
- The dominant kernel PCs are combined into an SDF / MVE portfolio with the **Kozak–Nagel–Santosh (KNS) economic shrinkage prior**. The SDF stays **linear in stock returns**: nonlinearity is only in portfolio weights, so the MVE portfolio is a tradable stock portfolio.
- Headline: with 40 anomalies, cross-validated MVE Sharpe rises from ~1.5–1.65 (linear) to **>3** (Gaussian kernel). In a true post-2004 holdout, ~0.5 → ~1.0.

## Method

**SDF with characteristic-driven loadings.** $M_{t+1}=1-b_t'(R_{t+1}-E R_{t+1})$ with $b_t=\Phi(Z_t)b$, where $Z_t$ is the $N\times K$ characteristic matrix and $\Phi:\mathbb R^{N\times K}\to\mathbb R^{N\times L}$ an (implicit) feature map. Then
$$M_{t+1}=1-b'(F_{t+1}-EF_{t+1}),\qquad F_{t+1}=\Phi(Z_t)'R_{t+1},$$
turning a conditional problem into a high-dimensional unconditional one. Aggregate conditioning can be added via $z_t\otimes F_{t+1}$, but the paper relies on cross-sectional characteristics only.

**Shrinkage (KNS).** Prior $\mu\sim N(0,\tfrac{\kappa^2}{\tau}\Sigma^2)$, $\tau=\mathrm{tr}\Sigma$ ($\kappa$ = root expected max squared Sharpe under the prior; rules out near-arbitrage and unbounded holdings). Posterior mean:
$$\hat b=(\Sigma+\gamma I)^{-1}\bar\mu,\qquad \gamma=\frac{\tau}{\kappa^2T},$$
equivalently $\min_b(\bar\mu-\Sigma b)'\Sigma^{-1}(\bar\mu-\Sigma b)+\gamma b'b$ (penalized HJ distance) or $\min_b(\bar\mu-\Sigma b)'(\bar\mu-\Sigma b)+\gamma b'\Sigma b$. In PC space, $\hat b_{P,j}=\frac{d_j}{d_j+\gamma}\frac{\bar\mu_{P,j}}{d_j}$: low-variance PCs are shrunk hardest, so the SDF is well approximated by **dominant PCs** (Proposition 1).

**Kernel trick.** With $X_t=\Phi(Z_t)$, instead of the $L\times L$ covariance diagonalize the $T\times T$ matrix
$$\Omega_{ts}=R_{t+1}'\,\tilde K(Z_t,Z_s)\,R_{s+1},\qquad K(Z_t,Z_s)_{ij}=\kappa(Z_{t,i},Z_{s,j})=\phi(Z_{t,i})'\phi(Z_{s,j}),$$
using Mercer's theorem (any positive-definite kernel is an inner product in some Hilbert space). Eigenvectors of $FF'$ are the (scaled) PCs of $F'F$ (Connor–Korajczyk asymptotic PCA). Features are **cross-sectionally centered** (zero-investment portfolios) by double-centering, $\tilde K=(I-M)K(I-M)$, $M=\frac1N\mathbf 1\mathbf 1'$.

Kernels:
- Polynomial $\kappa(z_i,z_j)=(c+\langle z_i,z_j\rangle)^d$. For $d=2,c=1$: $\phi(z)=(1,\sqrt2z_1,\sqrt2z_2,z_1^2,z_2^2,\sqrt2z_1z_2)$. $c\to0$ keeps only 2nd-order terms; $c\to\infty$ collapses to linear.
- Gaussian $\kappa(z_i,z_j)=\exp(-c\|z_i-z_j\|^2)$: an infinite-dimensional feature space containing interactions of all orders.

**Out-of-sample PCs and stock holdings (App. A).** With $K\alpha_k=\tilde\lambda_k\alpha_k$, a new observation's PC score is $\langle v_k,\Phi(Z_t)'R_{t+1}\rangle=w_{k,t}'R_{t+1}$, with
$$w_{k,t}'=\lambda_k^{-1/2}\sum_{i=1}^T\alpha_{k,i}R_{i+1}'K(Z_i,Z_t).$$
These are explicit stock weights, computable from current characteristics and **training** returns only. Combining with $\hat b$ gives the MVE portfolio's stock holdings and conditional SDF loadings at each date.

**Data and characteristic processing.** Characteristics are rank-transformed, $rc=\mathrm{rank}/(n_t+1)$ (ties get average rank). They are then centered and scaled by the mean absolute deviation, so each managed portfolio is zero-investment with average absolute weight 1; missing values are set to 0. Size filter: market cap ≥ 0.01% of total market cap (≈ \$2bn if the market is \$20tn). Daily returns; weights drift within the month (monthly-rebalanced buy-and-hold). Daily data are used so that covariance uncertainty is treated as negligible. The 40 anomalies follow Kozak–Nagel–Santosh (value, profitability, issuance, investment, momentum variants, reversals, seasonality, IVOL, beta, price, age, volume…). Annual accounting uses June formation; monthly signals are appropriately lagged (App. C).

**Tuning.** $\gamma$ chosen by 5-fold CV maximizing
$$R^2_{oos}=1-\frac{(\bar\mu_2-\Sigma_2\hat b)'(\bar\mu_2-\Sigma_2\hat b)}{\bar\mu_2'\bar\mu_2}.$$
The kernel parameter $c$ is chosen to maximize the CV Sharpe ratio (32 grid values). **Caveat stated by the author:** in the main results the PCs are built on the full sample and $\kappa,c$ are chosen in sample. Only the post-2004 split is fully out of sample.

**Computation (App. B).** $\Omega$ is ~12,000×12,000 (daily); each entry needs an $N\times N$ kernel matrix → ~$10^{18}$ operations for 32 tuning values. C++/CUDA on an Nvidia Titan V: under an hour. Cost does not rise with interaction order and is linear in the number of base characteristics (vs $O(L^3)$ for explicit PCA).

## Results

**Simulation.** 20 years, 1,000 stocks, one factor with $\beta_{t,i}=c^{(1)}_{t,i}c^{(2)}_{t,i}c^{(3)}_{t,i}$ (triple interaction), plus 2 useless characteristics. PCA on individual stocks fails; PCA on 5 linearly managed portfolios recovers the factor with correlation **0.13**; Gaussian kernel PCA ("CK-PCA") **0.98** (the oracle product sort works by design).

**Five FF–Carhart characteristics (size, value, profitability, investment, momentum):**
- CV Sharpe (annualized): linear ≈0.31; 2nd-order polynomial ≈0.47; Gaussian ≈0.75 (the introduction rounds to 0.2 → 0.7).
- Rank check for the polynomial kernel: 5 (large $c$), 15 (only 2nd-order terms, $c\to0$), 20 (both). Gaussian with small $c$: full rank ≈12,000.
- Projecting the SDF on explicit features (base, 2nd-order interactions, squares, cubes): the polynomial SDF is spanned (R² ≈1 with <15 terms). The Gaussian SDF with 15 features has R² < 0.5; cubic terms (mom³, inv³) are prominent.

**Forty anomaly characteristics:**
- 2nd-order polynomial improves CV Sharpe only mildly. Gaussian kernel: ~1.5 → **above 3** at mid-range $c$ (conclusion: 3.0 vs 1.65).
- Gaussian SDF projection R² stays ≈0.6 even with >30 features. Many top features are interactions (e.g. involving strev, indrr, roea, lev, mom, prof, ivol).

**True holdout (estimate PCs and $b$ pre-2005; apply to post-2004):**

| | Linear | Gaussian kernel |
|---|---:|---:|
| 5 FFC characteristics, post-2004 SR | ≈0 | ≈0.2 |
| 40 anomalies, post-2004 SR | ≈0.5 | ≈1.0 |

The CV-optimal $c$ from the pre-2005 period carries over reasonably well. The level drop matches post-publication anomaly decay (App. Table 1, annualized returns scaled to market volatility, pre-2005 → post-2005): Value (A) 11.2 → 0.3; momentum 12m 9.5 → −4.9; ROE 11.9 → −1.2; return on market equity 23.3 → 0.2; seasonality 22.0 → −6.1; industry-relative reversals −35.5 → −8.0; short-term reversal −17.9 → −6.0. Price (−11.0 → −12.6) and NOA (−9.8 → −7.9) are among the few that persist.

**Stock-level risk premia.** $\hat E_t[R_i]=\widehat{\mathrm{cov}}_t(R_i,-SDF)$ from rolling daily covariances. Predictive R² for individual stocks: monthly **0.8%** (constant-mean benchmark 0.2%), daily 0.045% (0.01%). Aggregated: equal-weighted market monthly R² **2.5%** ($t>3$), value-weighted 1.3% ($t=2.5$) (monthly horizon, overlapping daily data).

**Stock-level MVE composition, turnover, costs:** "[TO BE COMPLETED]" in this draft.

## Critical assessment

- **Strengths:** elegant and exact equivalence (linear kernel = standard managed-portfolio PCA; degree-2 kernel = explicit 2nd-order expansion); economically motivated shrinkage rather than generic ML penalties; stock-level holdings recoverable; convincing simulation where linear sorts fail.
- **Weaknesses / caveats:**
  - Headline Sharpe >3 is **not** a real-time result: PCs on the full sample, $\kappa$ and $c$ tuned in sample. The honest number is the post-2004 ~1.0 (vs ~0.5 linear), read off a figure and gross of costs. The conclusion still calls 3.0 "out-of-sample".
  - No turnover, transaction-cost, shorting or capacity analysis (section unfinished). Many important features are reversal-type signals (strev, industry-relative reversal, seasonality), which are turnover-heavy.
  - No standard errors on the Sharpe ratios or on the kernel vs linear difference.
  - Kernel choice imposes structure: the Gaussian kernel weights interactions by $c^q/q!$-type factors, and the ridge prior acts in that geometry, so "all interactions" is a specific weighting.
  - Treating covariances as known with daily data ignores weak-PC estimation error; the conditional SDF normalization ($E_t M=1$) is assumed in the covariance-based premium estimates.
- **Errors / ambiguities in the draft:**
  - The Gaussian series is printed with alternating signs ($1-\langle\cdot\rangle/1!+\langle\cdot\rangle^2/2!-\dots$); for $c=\tfrac12$ it should be $C\sum_q\langle z_i,z_j\rangle^q/q!$ with all plus signs.
  - The PC variance-contribution formula below Eq. 9 is garbled, and the claim that it is "decreasing in $d_j$" is not right as stated. The shrinkage factor $d_j/(d_j+\gamma)$ is increasing in $d_j$, i.e. low-variance PCs are shrunk more.
  - The radial parameter is called $c$ in Eq. 15 but $\sigma^2$ later. The statement that large $c$ ≈ linear holds for the polynomial kernel but is reversed for $\exp(-c\|\cdot\|^2)$ taken literally (large $c$ gives full rank).
  - Eq. 10 treats features as mean-zero (a second-moment matrix) while calling it a covariance.
  - The predictive-R² formula mixes $\mathrm{var}(\cdot)$ with $\sum r^2$.
  - Some appendix characteristic definitions (issuance ratios, debt-issuance indicator) are inconsistent with their verbal descriptions.

## Practical relevance for a quant PM

- A scalable way to test whether **interactions among existing signals** add to a linear multi-factor book without hand-crafting interaction terms. Start with the linear kernel (reproduces standard characteristic-PCA/KNS), then the degree-2 kernel as a check, then Gaussian with $c$ tuned by chronological validation.
- Output is directly a stock-weight vector (Eq. 37), so risk, turnover and costs can be evaluated. Do that before trusting any Sharpe number here.
- Expect the realistic gain to be the post-2004 magnitude (roughly doubling a modest linear SDF Sharpe), concentrated in nonlinear reversal/momentum/profitability interactions.
- Compute: GPU and blocking are required at daily frequency ($T^2N^2$ kernel evaluations).
