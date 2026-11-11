# Test Assets and Weak Factors

**Stefano Giglio, Dacheng Xiu, Dake Zhang · Sept 28, 2023 WP version (Chicago Booth WP 21-04, SSRN 3768081) with Internet Appendix · Source file `Finance/weakfactors_GiglioZhou_2023.pdf` (filename says "GiglioZhou"; third author is Dake Zhang) · Monthly, 1976:03–2020:12; 901 Chen–Zimmermann anomaly portfolios + 49 FF industries = 950 assets; robustness on 1,672 Hou–Xue–Zhang portfolios**

## Claim / contribution

Factor strength is a property of the **factor × test-asset universe × sample length**, not of the factor. Adding many uninformative portfolios *dilutes* a factor and biases PCA-based (Giglio–Xiu 2021) risk-premium estimates via errors-in-variables. **Supervised PCA (SPCA)** — iterate {screen assets by correlation with the (residual) target $g_t$ → take one PC of the selected assets → project it out of all assets, their means, and the target} — consistently estimates the risk premium of a chosen (tradable or nontradable, possibly noisy) factor in the presence of weak, omitted and correlated-exposure factors, gives valid $\sqrt T$ inference under stronger conditions, recovers the SDF when $g_t$ spans it, and yields a Sharpe-ratio diagnostic of observable factor models.

## Model and the weak-factor problem

$$r_t=\beta\gamma+\beta v_t+u_t,\qquad g_t=\xi+\eta v_t+z_t,\qquad m_t=1-\gamma'\Sigma_v^{-1}v_t,\qquad \gamma_g=-\mathrm{Cov}(g_t,m_t)=\eta\gamma .$$
$\beta$ is $N\times p$ (constant betas ⇒ characteristic-sorted portfolios), $z_t$ measurement error ⊥ $v_t$; $N,T\to\infty$, $p$ fixed, $\|\Sigma_u\|\lesssim1$. For a tradable target the premium is just its mean excess return; the method matters for nontradables and for diagnosis. Strong factors: all $\lambda_i(\beta'\beta)\asymp N$. Weakness = few exposed assets, small loadings, *or near-collinear loading columns*.

**Proposition 1 (one factor, Gaussian, $z=0$):** if $N/(T\|\beta\|^2)\to B\ge0$ and $\|\beta\|\to\infty$, then
$$\hat\gamma_g^{PCA}\xrightarrow{p}\frac{\eta\gamma}{1+B},$$
i.e. PCA is consistent iff $N/(T\|\beta\|^2)\to0$; the PC can be well correlated with the factor while the premium stays biased (cross-sectional regression needs accurate loadings).

## SPCA (Algorithm 3)

Demeaned returns $X$ ($N\times T$), mean vector $\mu$, demeaned targets $Y$ ($d\times T$). At iteration $k$:
1. Rank assets by $\max_j|\widehat{\mathrm{cov}}(X_{k,i},Y_{k,j})|$ (theory: covariance; empirics: correlation); keep top $\lfloor qN\rfloor$ → set $I_k$ (all assets re-eligible each step).
2. Leading singular triplet of $(X_k)_{I_k}$: $\hat v_k=\sqrt T\,b_k'$.
3. $\hat\beta_{I_k}=T^{-1}(X_k)_{I_k}\hat v_k'$; $\hat\gamma_k=(\hat\beta_{I_k}'\hat\beta_{I_k})^{-1}\hat\beta_{I_k}'(\mu_k)_{I_k}$.
4. $\hat\eta_k=T^{-1}Y_k\hat v_k'$, $\hat\beta_k=T^{-1}X_k\hat v_k'$ for **all** assets; update $X_{k+1}=X_k-\hat\beta_k\hat v_k$, $\mu_{k+1}=\mu_k-\hat\beta_k\hat\gamma_k$, $Y_{k+1}=Y_k-\hat\eta_k\hat v_k$.
5. Stop after $\hat p$ steps (or when the screening statistic falls below cutoff $c$): $\hat\gamma_g^{SPCA}=\sum_k\hat\eta_k\hat\gamma_k$.

Why iterate: with $g=v_1$, half the assets loading on $v_1+v_2$ and half on $v_2$ only, a one-shot screen drops the second group and PCA recovers $v_1+v_2$; after projection the residual target correlates with the second group through $v_1-v_2$, so a second screen recovers the missing direction. Unknown zero-beta rate: apply SPCA to cross-sectionally demeaned returns $M_\iota r_t$. $q=1$ reproduces PCA.

## Theory

- **Key assumption:** an (unknown) subset $I_0$ of size $N_0\to\infty$ in which all relevant factors are strong, $\lambda_{\min}(\beta_{I_0}'\beta_{I_0})\asymp N_0$. No method can price a factor nothing in the universe loads on.
- **Thm 1 (consistency):** if $\log(NT)(N_0^{-1}+T^{-1})\to0$, $c\to0$, $\sqrt{\log(NT)}[(qN)^{-1/2}+T^{-1/2}]/c\to0$, $qN/N_0\to0$, then $\hat\gamma_g\to_p\eta\gamma$. Only directions correlated with $g$ must be recovered; factors orthogonal to $g$ can be missed harmlessly.
- **Thm 2 (inference):** with rich supervision ($\lambda_{\min}(\eta'\eta)$ bounded away from 0, so $d\ge p$), $N_0/\sqrt T\to\infty$, $\sqrt T/(qN)\to0$: $\hat p\to p$ and $\sqrt T(\hat\gamma_g-\eta\gamma)\Rightarrow N(0,\Phi)$, error $O_p(T^{-1/2})+O_p((qN)^{-1})$; $\Phi$ from a Newey–West estimator on $\eta v_t+z_t(v_t'\Sigma_v^{-1}\gamma)$. In the empirics this is why the *joint* (all targets) estimation carries standard errors.
- **Thm 3 (SDF):** $\hat m_t=1-\hat\gamma'\hat v_t$ with $T^{-1}\sum(\hat m_t-m_t)^2=O_p(T^{-1}+\log N_0/N_0)$ under spanning. SPCA recovers the full SDF iff $g_t$ is spanned by all SDF factors (Thm 5 bounds the SPCA Sharpe between the $g$-span optimum and the true optimum).
- **Alternatives (Thm 4):** Ridge SDF error $\lesssim T^{-1}+(N+T)/(\lambda_pT)$ — fails with weak factors; Lasso $\lesssim\|b\|_1\sqrt{\log N/T}$ — consistent regardless of strength but slow (fast only if the SDF is sparse in test assets, $\|b\|_0^2\log N/T\to0$). PCA, rpPCA, Ridge and PLS are inconsistent under weak factors. (Eq. 17, the $N>T$-friendly form of the Kozak–Nagel–Santosh objective, prints $b'\hat\Sigma b$ twice; it should be $b'\hat\Sigma b-2b'\bar r+p_\mu(b)$.)

## Tuning

Chronological 50/50 split. In the training half, for each $p\in\{3,5,7,11\}$ (from a scree plot: ≥3 strong factors, 4–11 possibly weak), choose $\lfloor qN\rfloor\in\{100,150,\dots\}$ by **3-fold random CV repeated 100 times** (median choice), maximizing the hedge $R^2$ of the SPCA mimicking portfolio for $g_t$. Evaluation: fixed training weights, contemporaneous $R^2=1-\|Y_{ev}-wX_{ev}\|^2/\|Y_{ev}\|^2$ in the second half (no re-estimation). Normalized eigenvalue strength is *not* used for tuning (selected noise can look strong).

## Simulations ($N=1000$, 1,000 reps; 4 factors calibrated to Mkt/SMB/HML + $V$; factor s.d. 0.04/0.03/0.03/0.02; idio s.d. 0.01–0.09 inverse-gamma; $\beta_V$ from mixture $a\,N(0,1)+(1-a)N(0,0.1^2)$; optimal monthly SR ≈0.25)

Scenarios: (a) strong ($a=0.5$); (b) weak ($a=0.05$); (c) + measurement error; (d) correlated exposures $\beta_V=-\beta_{HML}+e$; (e) (d) with HML omitted from $g$; (f) (d) + measurement error. Competitors get infeasible oracle tuning (true $p$, population moments). SPCA is centered in all six; four-split survives (b),(d) but not (c),(e); PCA/PLS survive (c) but fail (e); two-pass only (a); Lasso/Ridge shrinkage-biased even in (a).

Scenario (f), $T=240$ (bp/month; true premia Mkt 53.7, SMB 21.7, HML 25.4, $V$ 40.0):

| Estimator | HML bias / RMSE | $V$ bias / RMSE |
|---|---|---|
| SPCA | −3.2 / 18.4 | −3.5 / 13.2 |
| PCA | −37.0 / 39.9 | −36.9 / 37.8 |
| rpPCA | 14.7 / 29.1 | 14.1 / 24.5 |
| PLS | −5.2 / 18.6 | −5.6 / 13.7 |
| Lasso | −18.1 / 23.9 | −17.6 / 21.1 |
| Ridge | −3.2 / 12.0 | −17.8 / 21.2 |
| Four-split | 51.5 / 62.9 | 36.8 / 51.7 |
| Two-pass | 33.3 / 39.5 | 18.6 / 28.4 |

At $T=480$ SPCA's $V$ RMSE falls to 9.5 (PCA 24.5). **Size of 5% $t$-tests** (Fig. 2, scenario f): SPCA Mkt 6.6%, SMB 5.0%, HML 5.2%, $V$ 5.2%; PCA 6.6%, 4.9%, **67.4%, 98.4%**.

SDF recovery (Table 2, $T=240$, MSE): SPCA 0.020, PCA 0.069, rpPCA 0.150, PLS 0.022, Lasso 0.040, Ridge 0.052; SPCA $\hat p=4.315$ (s.d. 0.598). OOS Sharpe (Table 3, population moments): SPCA 0.233, PCA 0.104, rpPCA 0.238, PLS 0.224, Lasso 0.210, Ridge 0.206; optimum 0.263 (rpPCA's edge comes from oracle Sharpe tuning). Fig. 3: supervised by all four factors or by a noisy SDF, SPCA peaks at $p=4$; supervised by the market only, neither SPCA nor PCA recovers the weak factor.

## Empirical results (CZ data; Table 4, bp/month; RP from training half, $R^2$ = OOS hedge)

| Factor | mean train / eval | SPCA RP, $p$=3/5/7/11 (#assets) | OOS $R^2$ ($p$=11) | Joint RP (s.e.) |
|---|---|---|---|---|
| Market | 74 / 62 | 68 / 70 / 72 / 74 (100) | 0.99 | 73 (26) |
| HML | 39 / −7 | 50 / 37 / 39 / 44 | 0.79 | 54 (18) |
| RMW | 37 / 28 | −8 / 40 / 33 / 27 | 0.66 ($p$=3: −0.18) | 23 (9) |
| CMA | 26 / 19 | 36 / 40 / 27 / 31 | 0.53 | 34 (11) |
| Momentum | 91 / 30 | 67 / 86 / 102 / 101 | 0.88 | 96 (23) |
| BAB | 126 / 56 | 112 / 120 / 112 / 128 | 0.45 | 93 (20) |
| QMJ | 41 / 39 | −9 / 28 / 31 / 36 | 0.78 | 20 (10) |
| PS liquidity | — | 70 / 85 / 83 / 95 (550–900) | 0.03 | 105 (25) |
| Intermediary capital | — | 112 / 101 / 121 / 116 (100–350) | 0.52 | 109 (41) |
| Financial uncertainty | — | −61 / −48 / −40 / −41 | 0.10 | −46 (17) |
| Macro uncertainty | — | −7 / −10 / −10 / −16 | 0.09 | −19 (10) |
| IP growth | — | −4 / −4 / −5 / −2 (950) | 0.00 | −2 (3) |
| Consumption | — | 2 / 3 / 3 / 2 (950) | −0.01 | 2 (2) |

- Tradable SPCA premia are never significantly different from average returns at 5% (except QMJ at $p=3$). Heatmaps: the best hedges sit at $q<1$ (few assets); SPCA reaches momentum $R^2>70\%$ with 3 factors, PCA needs ≥6.
- Nontradables: most (IP, consumption, LN macro PCs, term, credit, unemployment, sentiment, oil) are unhedgeable (OOS $R^2\le0$, SPCA selects all 950 assets ≈ PCA) and not priced; intermediary capital (R² > 0.5) and liquidity carry positive premia, uncertainty indices negative premia. The introduction's "almost none of the non-tradable factors are priced, except intermediary capital" is stronger than Table 4, where liquidity and financial (and marginally macro) uncertainty are also significant. Units of nontradable premia depend on the target's scaling.
- Asset selection (Table 5): momentum's first screen picks IntMom/Mom portfolios (corr ≤0.44); after projection, residual correlations rise to 0.79 (Mom12mOffSeason); intermediary capital loads on bank (0.90) and financial (0.84) industries, idio-vol and illiquidity sorts; liquidity on payout-yield and beta sorts.
- **Removing informative sorts (HXZ, $p=9$, hedge $R^2$):** value 64%→47% (PCA) vs 74%→62% (SPCA); momentum 76%→48% vs 86%→77%; profitability 41%→14% vs 71%→60%.
- **HXZ robustness (Table 6, $p$=3/5/6/9):** broadly similar but with notable level differences — BAB is barely hedgeable ($R^2$ 0.04–0.08) and priced at 27–47bp vs 112–128 in CZ; HML 16–24; liquidity joint 37 (18); intermediary capital 90 (37); financial uncertainty −18 (11). Premium estimates for poorly hedged factors are universe-dependent.
- **Model diagnosis (Fig. 9, OOS Sharpe of SPCA-SDF vs model):** market SR 0.45; SPCA SR rises with $p$ well above CAPM and FF3 in both datasets; FF5 matches SPCA in HXZ but not in CZ; adding MOM, BAB, QMJ shrinks the gap, still nonzero in CZ. HXZ has more assets but diagnoses *fewer* missing factors — $N$ is not a proxy for exposure richness.

## Critical assessment

- **Convincing:** clean diagnosis of why "more test assets" can hurt; the Monte Carlo is adversarial to SPCA (competitors get oracle tuning) yet SPCA dominates on bias and test size; the drop-the-informative-sorts exercise is a nice empirical check.
- **Caveats:** requires an informative subset to exist and constant betas; Thm 2 needs $d\ge p$ (single-target runs have no s.e.); random-fold CV on time series ignores serial dependence/instability; finite-sample screening near ties can be unstable; $q$ grid starting at 100 assets is ad hoc; tradable-factor means differ strongly between halves (HML 39 vs −7, momentum 91 vs 30, BAB 126 vs 56), so "hedge well" ≠ "premium stable"; Sharpe comparisons in Fig. 9 have no confidence bands; the complete-panel requirement fixes the universe; nontradable premia depend on target scaling; missing calibration details (full factor covariance, measurement-error variances) for exact replication.

## Practical relevance for a quant PM

- Before interpreting a (non)significant premium from a big anomaly panel, check the scree plot: absent a clear eigen-gap, PCA/Fama–MacBeth premia for non-pervasive factors are biased toward zero and their $t$-stats badly oversized.
- SPCA is a practical recipe for **factor-mimicking/hedging portfolios of macro or liquidity risks**: screen → PC → deflate → repeat, tune the number of assets by OOS hedge $R^2$; it gets good hedges with few factors.
- Use the SPCA-SDF Sharpe vs your factor model's Sharpe as a missing-factor diagnostic, and vary the asset universe — conclusions about "which factors are priced" are universe-specific.
