# Asset Pricing with Omitted Factors

**Authors:** Stefano Giglio (Yale, NBER, CEPR) and Dacheng Xiu (University of Chicago)  
**Publication:** *Journal of Political Economy*, 2021, 129(7), pp. 1947-1990 (previously circulated as "Inference on Risk Premia in the Presence of Omitted Factors")  
**Source file:** `Finance/OmittedFactor_GiglioXiu.pdf` (main text and appendices A-B; the online appendix and Table B1 itself are not in the file)

---

## 1. Question

How do you estimate the risk premium of an observable factor $g_t$ (liquidity, intermediary capital, consumption growth, or a traded factor) when the econometrician does not know or observe all the other priced factors, and $g_t$ may be measured with error? Both standard estimators -- two-pass cross-sectional regression (Fama-MacBeth) and the mimicking-portfolio projection -- are biased under omitted factors, and the literature's fix has been ad hoc choice of controls (FF3) or projection bases (e.g. MMV 2009 projecting consumption onto four size/BM portfolios).

## 2. Model and the two biases

Excess returns on $n$ assets and $d$ observable factors:

$$
r_t = \beta\gamma + \beta v_t + u_t,\qquad g_t = \delta + \eta v_t + z_t,
$$

with $v_t$ the $p$ mean-zero factor innovations, $\gamma$ their premia, $z_t$ measurement error orthogonal to $v_t$ (may correlate with $u_t$). The target is $\gamma_g = \eta\gamma$: the expected excess return of a portfolio with unit beta on $g$ and zero beta on everything else.

- **Two-pass with $v_{2t}$ omitted:** bias enters twice -- in the time-series betas (through $\mathrm{Corr}(v_1,v_2)$) and in the cross-sectional step (through the cross-sectional correlation of $\beta_1,\beta_2$). Measurement error $z_t$ adds attenuation in $\hat\beta_1$.
- **Mimicking portfolio** on a chosen basis $\breve r_t$:
$$
\gamma_g^{MP} = \big\{(\breve\beta\Sigma_v\breve\beta^\top+\breve\Sigma_u)^{-1}(\breve\beta\Sigma_v\eta^\top + \breve\Sigma_{z,u})\big\}^\top\breve\beta\gamma ,
$$
which equals $\eta\gamma$ only if the basis is (i) diversified ($\breve\Sigma_u\approx0$) and (ii) spans all $p$ factors ($\breve\beta$ invertible). Omitting spanning portfolios biases it; the $\breve\Sigma_{z,u}$ term biases it further unless measurement error is uncorrelated with the basis residuals. With fixed $n$, two-pass and mimicking estimates differ even in population for nontradable factors.

## 3. Rotation invariance and the three-pass estimator

If one observes only $\hat v_t = Hv_t$ for unknown invertible $H$, the model rewrites with $\hat\beta=\beta H^{-1}$, $\hat\gamma = H\gamma$, $\hat\eta=\eta H^{-1}$, and
$$
\hat\eta\hat\gamma = \eta H^{-1}H\gamma = \eta\gamma .
$$
$\eta$, $\gamma$ and $\beta$ are not identified; the product is. PCA recovers the factor space up to such an $H$ when factors are pervasive (Bai-Ng 2002, Bai 2003). Hence:

1. **PCA:** eigen-decompose $n^{-1}T^{-1}\bar R^\top\bar R$ ($\bar R$ = demeaned $n\times T$ returns); $\hat V = T^{1/2}(\xi_1,\dots,\xi_{\hat p})^\top$, $\hat\beta = T^{-1}\bar R\hat V^\top$.
2. **Cross-section:** $\hat\gamma = (\hat\beta^\top\hat\beta)^{-1}\hat\beta^\top\bar r$ (OLS; GLS/WLS give no first-order gain).
3. **Time series:** $\hat\eta = \bar G\hat V^\top(\hat V\hat V^\top)^{-1}$, which also strips out $z_t$.

$$
\hat\gamma_g = \hat\eta\hat\gamma = \bar G\hat V^\top(\hat V\hat V^\top)^{-1}(\hat\beta^\top\hat\beta)^{-1}\hat\beta^\top\bar r .
$$

Each element of $g_t$ is estimated separately: adding or dropping other observables does not change a factor's estimate (unlike two-pass). With an unrestricted zero-beta rate $\gamma_0$, step 2 is run after projecting out $\iota_n$: $\tilde\gamma_g = \bar G\hat V^\top(\hat V\hat V^\top)^{-1}(\hat\beta^\top M_{\iota}\hat\beta)^{-1}\hat\beta^\top M_{\iota}\bar r$.

**Three equivalent readings.**
- *PC-augmented two-pass:* two-pass with $g_t$ plus $p-1$ arbitrary controls is correct for any controls that, together with $g_t$, span $v_t$; PCs are such controls. Numerically identical to the three-pass order of operations.
- *Regularized mimicking portfolio:* Proposition 1 shows $\gamma_g^{MP}-\eta\gamma = o_p(1)$ as $n\to\infty$ if the projection weights are $w\propto\beta H$ (or even $w=I_n$, i.e. all assets). The PCs are exactly $\hat V = (\hat\beta^\top\hat\beta)^{-1}\hat\beta^\top\bar R$, i.e. $w=\hat\beta(\hat\beta^\top\hat\beta)^{-1}$; projecting on all $n$ assets is inefficient and infeasible when $n>T$. So in large $n$ the two classical approaches converge, and the three-pass is where they meet.
- *SDF:* $m_t = 1-\gamma^\top\Sigma_v^{-1}v_t$ is rotation invariant; steps 1-2 estimate it, step 3 computes $-\mathrm{Cov}(g_t,m_t)=\eta\gamma$.

## 4. Asymptotics (n, T both large)

Key identifying assumption (A6): **all latent factors are pervasive**, $n^{-1}\beta^\top\beta\to\Sigma_\beta\succ0$. Weak *latent* priced factors are excluded; weak *observable* factors are allowed. Errors may be heteroskedastic and dependent in both dimensions.

**Theorem 1.** $\hat\gamma - H\gamma = H\bar v + O_p(n^{-1}+T^{-1})$, $\hat\eta-\eta H^{-1} = T^{-1}\bar Z\bar V^\top H^\top + O_p(n^{-1}+T^{-1})$, and if $T^{1/2}/n\to0$, $\sqrt T(\hat\gamma_g-\eta\gamma)\Rightarrow N(0,\Phi)$, where $\Phi$ depends only on $\Sigma_v$, $\eta$, $\gamma$ and the long-run covariances $\Pi_{11},\Pi_{12},\Pi_{22}$ of $(\mathrm{vec}(ZV^\top), V\iota_T)$.

- $\Phi$ does **not** involve $\Sigma_u$ or first-pass beta error: no Shanken correction, no need to estimate the $n\times n$ residual covariance. With all factors observed and no measurement error, $\Phi=\Pi_{22}=\Sigma_v$ -- the variance of the factor sample mean, i.e. the efficiency bound, attained without knowing factor identities.
- The dominant error is $\bar v$ (the sample mean of factor innovations) plus the time-series regression error of $g$ on $v$. Precision is governed by $T$, not $n$.
- Newey-West estimators $\hat\Pi_{11},\hat\Pi_{12},\hat\Pi_{22}$ give feasible SEs. A consistent estimator of $p$ is in the online appendix; consistency of $\hat\gamma_g$ holds for any $\check p\ge p$.

**Mixed frequency (Theorem 2).** Running steps 1-2 on high-frequency returns and step 3 on aggregated factors gives $\hat\gamma_g^m = \hat\gamma_g + O_p(n^{-1}+T^{-1})$: no first-order gain, because the binding error is the mean return $\bar v$, which depends on sample span, not sampling frequency.

**Ridge (Theorem 3).** Projecting $g$ on all assets with ridge, $\hat\gamma^\mu_g = \bar G\bar R^\top(\bar R\bar R^\top+\mu I_n)^{-1}\bar r$, is consistent for suitable $\mu$ ($\mu/(nT)\to0$, $\mu^{-1}(nT^{1/4}+n^{1/4}T)\to0$) but less efficient: three-pass keeps only the top $\hat p$ singular triplets, ridge shrinks all of them and so carries idiosyncratic noise.

**Weak-factor diagnostics.** $R^2_g = \eta\Sigma_v\eta^\top/(\eta\Sigma_v\eta^\top+\Sigma_z)$, estimated by $\hat\eta\hat V\hat V^\top\hat\eta^\top/\bar G\bar G^\top$; Wald test of $H_0:\eta=0$, $\hat W = T\hat\eta(\hat\Sigma_v^{-1}\hat\Pi_{11}\hat\Sigma_v^{-1})^{-1}\hat\eta^\top\sim\chi^2_{\hat p}$ (Theorem 4, with local power against $\eta=\eta_0T^{-1/2}$). Inference on $\gamma_g$ stays valid even when $g$ is useless -- the estimate simply goes to zero.

## 5. Empirical application

**Data.** 647 monthly portfolios, 1976-2010: US equities sorted on many characteristics, Treasuries, corporate bonds, currencies (sample start set by the non-equity data). Tradable $g$: MKT, SMB, HML, RMW, CMA, MOM, BAB, QMJ. Nontradable: AR(1) innovations in IP growth; VAR(1) innovations in the first three PCs of Ludvigson-Ng's 279 macro-finance series; Pastor-Stambaugh liquidity; He-Kelly-Manela and Adrian-Etula-Muir intermediary factors; four Novy-Marx (2014) placebos (Manhattan temperature, global land temperature anomaly, El Nino, sunspots, in AR(1) innovations); MMV aggregate and stockholder consumption growth.

**Number of factors.** Eigenvalues drop noticeably after the 7th; the paper's estimator also picks $\hat p=7$. Seven PCs give a cross-sectional $R^2$ of 59% on 647 assets (vs 73% for FF3 on 25 size/BM portfolios -- a cross-section 26 times smaller); 10 and 13 PCs give 66% and 68%.

**Momentum illustration** (bps/month). Note on signs: the PDF text extraction renders minus signs as "2" (e.g. "g 5 bg" for $=$), so the figures below are read accordingly; the text itself describes both mimicking estimates as negative.

| Estimator | MOM premium |
|---|---|
| Time-series mean (benchmark) | 69 (SE 24) |
| Two-pass, no controls | about -201, strongly significant |
| Two-pass, + market | 20, insignificant |
| Two-pass, + FF3 | 71 |
| Mimicking, onto market | about -5 |
| Mimicking, onto FF3 portfolios | about -21, significant |
| Three-pass, $\hat p=7$ | 49, significant |

**Patterns across Table B1** (as described in the text):
- Two-pass: estimates swing sharply with the control set; three of the four Novy-Marx noise factors get huge, significant premia -- the weak/noisy-factor pathology.
- Mimicking: sign flips across bases (BAB and CMA negative when projected on the market, positive on FF3); often the wrong sign relative to the mean for traded factors; projection on all 647 assets infeasible ($n>T$).
- Three-pass: traded factors are close, economically and statistically, to their average excess returns. Significant nontradable premia: Pastor-Stambaugh liquidity, both intermediary-capital factors, Ludvigson-Ng macro PC1, and MMV stockholder consumption growth. Novy-Marx factors insignificant. IP growth marginally significant but economically negligible.
- $R^2_g$ is very heterogeneous: near 1 for MKT and SMB, about 2% for IP. The Wald test fails to reject weakness for several (not all) nontradable factors.

**Zero-beta rate and the market premium.** With an unrestricted zero-beta rate, Fama-MacBeth on FF3 reproduces the familiar puzzle: a zero-beta rate well above the T-bill and a negative market premium (about -24 bps/month under the sign reading above). Since $R^2_g$ for the market is high, measurement error is not the explanation; the three-pass estimate of the market premium is positive in all specifications. Other results with estimated $\gamma_0$ are broadly similar to the baseline.

**Robustness (online appendix, not in this file):** 10 and 13 PCs, equity-only test assets, subsamples and alternative portfolios, PCA variants that also weight cross-sectional pricing (in the spirit of Connor-Korajczyk and Lettau-Pelger's RP-PCA), and ridge instead of PCA -- all reported as similar.

## 6. Limitations stated or implied

- **Pervasiveness of priced latent factors** is the load-bearing assumption. A priced but weak latent factor is lost by PCA and reintroduces omitted-variable bias; the authors defer this to the online appendix and cite Onatski (2012).
- **Constant betas and premia.** Reasonable for characteristic-sorted portfolios, not for individual stocks; conditional extensions need conditioning variables.
- **Choice of $p$.** Underselection recreates the bias; overselection is benign asymptotically. Finite-sample efficiency loss relative to observed factors can be material when $n$ is modest.
- **Low $R^2_g$ is not uniquely noise.** It could also reflect test assets that fail to span the factor, or too few PCs (the paper's footnote 21) -- conclusions on "unpriced" macro factors are conditional on the 647-portfolio span.
- **Precision is T-limited.** 35 years of monthly data; the leading error is the sample mean of factor innovations, so large cross-sections do not buy tighter confidence intervals.

## 7. Assessment

**Convincing.** The identification argument is short and correct: the premium of a projection onto a spanned space is invariant to the basis. The unification (two-pass and mimicking portfolios converge as $n\to\infty$ with PC bases) and the result that $\Sigma_u$ drops out of $\Phi$ are clean and practically useful. The traded-factor check (three-pass ≈ time-series mean) and the placebo check (Novy-Marx factors ≈ 0) are the right external validations and both pass.

**Fragile.** The significance of nontradable premia rests on the specific 647-asset span and $\hat p=7$; the 59% cross-sectional $R^2$ means a sizeable part of expected returns is not captured by the PCs, and the method says nothing about whether that residual is mispricing or weak factors. Only the full table (not in this extraction) lets one judge how close "close to the average" is factor by factor. A 49 bp estimate for MOM against a 69 bp mean is within error but shows the finite-sample cost.

**Practical relevance for a quant researcher.**
- To price any factor proxy (a macro series, a sentiment index, a proprietary risk measure), regress it on the top PCs of a broad, multi-asset portfolio panel and multiply by the PCs' cross-sectional premia; report $\hat\gamma_g$, HAC SE, $R^2_g$, the Wald weakness test and sensitivity to $\check p$.
- Treat any Fama-MacBeth price of risk without spanning controls as uninterpretable; results that depend on "+market" versus "+FF3" are warning signs, not robustness.
- The step-3 projection $\hat\eta\hat V_t$ is a denoised, tradable (PC-based) mimicking portfolio for $g_t$ -- useful for hedging or tilting toward nontradable exposures.
- Running placebo series through the same pipeline is cheap and should be standard.

## 8. Relation to literature

Builds on two-pass regressions (Jensen-Black-Scholes 1972; Fama-MacBeth 1973), large-$n$ risk-premia work (Gagliardini-Ossola-Scaillet 2016; Bai-Zhou 2015; Connor-Hagmann-Linton 2012), misspecification and weak-factor critiques (Kan-Zhang 1999; Jagannathan-Wang 1998; Kleibergen 2009; Gospodinov-Kan-Robotti 2013, 2014; Bryzgalova 2015), mimicking portfolios (Huberman-Kandel-Stambaugh 1987; Breeden-Gibbons-Litzenberger 1989), and PCs in asset pricing (Chamberlain-Rothschild 1983; Connor-Korajczyk 1986, 1988; Kozak-Nagel-Santosh 2018). It adds a second argument to Lewellen-Nagel-Shanken (2010) for many test assets: not only to avoid a low-dimensional test, but to control for omitted factors. The invariance result is distinct from Roll-Ross/HKS results on rotations preserving pricing ability: it concerns the premium of an individual factor.
