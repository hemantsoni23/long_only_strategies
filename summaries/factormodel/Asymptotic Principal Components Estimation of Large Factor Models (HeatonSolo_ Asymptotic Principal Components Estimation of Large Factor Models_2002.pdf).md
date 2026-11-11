# Asymptotic Principal Components Estimation of Large Factor Models

**Chris Heaton (Macquarie/UNSW) & Victor Solo (UNSW) · working paper "Work in Progress", 23 Dec 2002 · Source file `Finance/HeatonSolo_ Asymptotic Principal Components Estimation of Large Factor Models_2002.pdf` · Theory + illustration on the Stock–Watson (1998) U.S. monthly macro panel (149 series, Mar 1959–Dec 1998)**

## Claim / contribution

Large-$N$ PCA forecasting theory (Stock–Watson 1998, Bai–Ng 2002, Forni–Hallin–Lippi–Reichlin 2000) lets $p\to\infty$ with bounded idiosyncratic eigenvalues and diverging factor eigenvalues, i.e. it implicitly sends a **noise-to-signal ratio** to zero. The authors replace "$p$ large" by an explicit, estimable ratio $\rho$ and give a finite-sample bound on how far the (population-)PCA diffusion-index forecast can be from the infeasible factor forecast. On the Stock–Watson data the estimated bound is uninformative (> 0.4 even with one factor, > 4 with six), so "the asymptotics apply" cannot be taken for granted. The paper is explicitly preliminary.

## Setup

$$
x_t=Bf_t+n_t,\qquad y_t=\beta'f_t+v_t,\qquad E f_tf_t'=I_k,\ E n_tn_t'=\Psi\ \text{(diagonal)},\ E v_t^2=\sigma_v^2 .
$$

$\Omega=BB'+\Psi=Q\Lambda Q'+Q_\perp\Lambda_\perp Q_\perp'$ ($\Lambda$: top $k$ eigenvalues of $\Omega$); $BB'=UDU'$. Noise-to-signal ratio

$$
\rho=\frac{\sigma^2\,\mathrm{tr}(\Lambda^{-1})}{k}=\frac{\sigma^2}{\lambda},\qquad \sigma^2=\lambda_{\max}(\Psi),\quad \lambda=\frac{k}{\mathrm{tr}(\Lambda^{-1})}\ \text{(harmonic mean of retained eigenvalues)},
$$

so $\rho$ is driven by the **largest idiosyncratic variance** and the **weakest retained eigenvalue** (the text prints "$\lambda=k\,\mathrm{tr}(\Lambda^{-1})$", a typo given $\rho=\sigma^2/\lambda$). Forecasts:
- ideal: $f_{Qt}=\Lambda^{-1/2}Q'x_t$ (unit covariance), $\beta_Q=T^{-1}\sum_t f_{Qt}y_t$, $s_{Qh}=\beta_Q'f_{Qh}$;
- empirical: same with $\hat Q,\hat\Lambda$ from the sample covariance (then $\hat\beta_Q$ is OLS on PC scores).

Target of comparison: the infeasible signal $s_h=\beta'f_h$ (not $y_h$; the shock $v_h$ is excluded). Population predictability $r^2=\beta'\beta/(\beta'\beta+\sigma_v^2)$. Asymptotic regimes: (I) $T\to\infty$, $\rho$ fixed; (II) $(1/T,\rho)\to(0,0)$, with convergence shown via Markov's inequality.

Assumptions (Theorem 1): $f_t,n_t,v_t$ mutually independent, serially uncorrelated, Gaussian, zero mean; the forecast observation $h$ is independent of the estimation sample. Much stronger than approximate dynamic factor models (no cross-correlated or serially correlated noise).

## Results

**Theorem 1 (ideal forecast).** With $e_h=s_{Qh}-s_h$,

$$
\frac{E|e_h|}{\sqrt{\beta'\beta}}\ \le\ k\sqrt{\rho+\frac{2}{r^2T}}\;+\;k\sqrt{\rho\Big(1+\frac{2}{r^2T}\Big)} .
$$

- $T\to\infty$ at fixed $\rho$: bound → $2k\sqrt\rho$ — population PCA's approximation error does not vanish with more time series data.
- $\rho\to0$ at finite $T$: residual $k\sqrt{2/(r^2T)}$ from estimating $\beta$; convergence in $T$ is faster the more $y$ is driven by the factors ($r^2$ high).
- The bound **increases in $k$** (linearly, and through $\rho$ if added eigenvalues are small) — extra factors can make the guarantee worse.
- The authors chose the first-moment measure because a variance-ratio version $\mathrm{var}(e_h)/\beta'\beta$ was "tedious and under development". Via Markov, $P(|e_h|>a\sqrt{\beta'\beta})\le$ bound$/a$.

Proof sketch (Appendix): split $e_h=e_a+e_b$ with $e_a=(S_{xy}'Q\Lambda^{-1}Q'B-\beta')f_h$ (attenuation + estimation of the cross moment) and $e_b=S_{xy}'Q\Lambda^{-1}Q'n_h$ (noise passed through the PC weights). Gaussian fourth moments give $\mathrm{var}(a'S_{wu}b)\le\frac2T a'\Gamma_wa\,b'\Gamma_ub$; Lemma 4 ($\Lambda=Q'(UDU'+\Psi)Q$) and Lemma 5 (eigenvalues of $I-M$, $M=D^{1/2}R\Lambda^{-1}R'D^{1/2}$, $R=U'Q$, equal those of $\Lambda^{-1/2}Q'\Psi Q\Lambda^{-1/2}$) bound the bias by $\sigma^2k/\lambda$. This yields $E e_a^2/\beta'\beta\le k^2(\rho+2/(r^2T))$ and $E e_b^2/\beta'\beta\le k^2\rho(1+2/(r^2T))$; Jensen and the triangle inequality give the theorem.

**Theorem 2 (empirical vs. ideal).** If the eigenvalues in $\Lambda$ are distinct, then for fixed $\rho$ and fixed $p$, $\hat e_h=\hat s_{Qh}-s_{Qh}\to_p0$ as $T\to\infty$ (implicit-function theorem → continuity of eigen-decomposition + Slutsky). No rate; joint asymptotics for the empirical forecast with $(1/T,\rho)\to(0,0)$ are left open. The continuity argument also needs a gap $\lambda_k>\lambda_{k+1}$ between retained and discarded eigenvalues, which the stated condition (distinct retained eigenvalues) does not guarantee — e.g. it is vacuous for $k=1$.

## Testing whether $\rho$ is small

Since $\sigma^2=\max_i\Psi_{ii}$ is non-smooth, test a lower bound on the large-$T$ bound: $(k/p)\,\mathrm{tr}(\Psi)\,\mathrm{tr}(\Lambda^{-1})\le k\sigma^2\mathrm{tr}(\Lambda^{-1})$, so

$$
L=2\sqrt{\tfrac kp\,\mathrm{tr}(\Psi)\mathrm{tr}(\Lambda^{-1})}\ \le\ 2k\sqrt\rho,\qquad
H_0:\ \mathrm{tr}(\Psi)\mathrm{tr}(\Lambda^{-1})=\frac{\delta^2p}{4k}\ \ \text{vs.}\ \ H_1:\ >,
$$

with $\delta$ the tolerated probability bound. Estimation by Gaussian ML static factor analysis, allowing an unbalanced panel via selection matrices $W_t$: $\ell=-\tfrac12\sum_t\ln|W_t\Omega W_t'|-\tfrac12\sum_t\mathrm{tr}[x_tx_t'(W_t\Omega W_t')^{-1}]$. The information matrix is singular for $k>1$ (rotational non-identification), handled by a generalized inverse (Silvey; Aitchison–Silvey; Poskitt–Tremayne; Breusch 1986 shows any g-inverse works); $W\sim\chi^2_1$ asymptotically. **Caveat:** the printed statistic $W=[\mathrm{tr}(B'\Psi^{-1}B)-\delta]^2h'H^-h$ does not match the hypothesis; a correct Wald form would be $[\hat g-\delta^2p/(4k)]^2/(\hat h'\widehat{\mathrm{Var}}(\hat\theta)\hat h)$ with $g=\mathrm{tr}(\Psi)\mathrm{tr}(\Lambda^{-1})$ and $h=\nabla g$ (the paper's $h$ — $[-2\mathrm{tr}(\Psi)\mathrm{vec}(Q\Lambda^{-2}Q'B),\ \mathrm{tr}(\Lambda^{-1})\mathbf 1-\mathrm{tr}(\Psi)\mathrm{diag}(Q\Lambda^{-2}Q')]$ — is this gradient). Rejection only rules out a small *upper bound*; it does not show that actual forecast errors are large.

## Empirical illustration

Stock–Watson (1998) data, differenced, balanced, 149 series standardized; ML factor models with $k=1,\dots,6$ started from scaled PCs, cyclic-ascent (claimed globally convergent) then a BFGS variant of Jöreskog (1967). Any series whose $\Psi_{ii}$ fell below 0.01 was dropped (Heywood cases): none for $k=1$; #118 (10y Treasury − fed funds) for $k=2,3$; #34 (unemployment 15–26 weeks), #117 (5y − FF), #118 for $k=4$–6.

Table 2 — estimated eigenvalues ($\sigma^2=\max\Psi_{ii}$):

| $k$ | $\sigma^2$ | $\lambda_1$ | $\lambda_2$ | $\lambda_3$ | $\lambda_4$ | $\lambda_5$ | $\lambda_6$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.9979 | 23.3310 | | | | | |
| 2 | 0.9976 | 23.4656 | 12.4886 | | | | |
| 3 | 0.9977 | 23.3902 | 11.5909 | 6.2631 | | | |
| 4 | 0.9967 | 23.4642 | 11.7010 | 6.5298 | 5.2616 | | |
| 5 | 0.9924 | 23.4755 | 11.6957 | 6.9046 | 6.1765 | 5.2074 | |
| 6 | 0.9910 | 22.7434 | 11.8037 | 7.2244 | 6.1791 | 5.1982 | 5.0458 |

Table 3 — noise-to-signal statistics ($\delta=0.01$):

| $k$ | $\rho$ | $2k\sqrt\rho$ | $L$ | $\widehat{\mathrm{tr}\Psi\,\mathrm{tr}\Lambda^{-1}}$ | $H_0$ value $\delta^2p/4k$ | Wald $W$ |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.0428 | 0.4136 | 0.3807 | 5.3984 | 0.00373 | 273 |
| 2 | 0.0612 | 0.9895 | 0.8647 | 13.8337 | 0.00185 | 431 |
| 3 | 0.0960 | 1.8591 | 1.5870 | 31.0628 | 0.00123 | 563 |
| 4 | 0.1174 | 2.7415 | 2.2760 | 47.2704 | 0.00091 | 754 |
| 5 | 0.1244 | 3.5274 | 2.8449 | 59.0808 | 0.00073 | 976 |
| 6 | 0.1354 | 4.4149 | 3.4696 | 72.7305 | 0.00060 | 1179 |

Authors' reading: signals exceed noise "by one order of magnitude or less"; as probability bounds the values are "quite useless"; the lower bound $L$ is reasonably close to $2k\sqrt\rho$; $H_0$ is rejected by orders of magnitude for every $k$. Arithmetic check: $L$ reproduces with $p=149,148,148,146,146$ for $k=1$–5, but the $k=6$ row ($L$ and $\delta^2p/4k$) implies $p=145$, one fewer series than Table 1's three omissions — a small internal inconsistency.

## Critical assessment

- **Useful insight:** what matters is not $p$ but signal strength relative to the *worst* idiosyncratic variance and the *weakest* retained factor. With standardized data $\sigma^2\le1$ and here ≈ 1 (some series are almost pure noise), so $\rho\approx\mathrm{tr}(\Lambda^{-1})/k$ and the bound is dominated by the small eigenvalues (≈ 5–7 for factors 3–6 out of total variance 149). Adding an irrelevant series can only raise $\sigma^2$; adding factors with small eigenvalues raises $\rho$ and the bound.
- **Limits:** (i) a conservative *upper* bound — large values show the theorem cannot certify PCA, not that PCA forecasts are bad (Stock–Watson found them good empirically); (ii) the $\max\Psi_{ii}$ and Cauchy–Schwarz steps make it loose, and the factor $k$ is crude; (iii) i.i.d. Gaussian, diagonal-$\Psi$ assumptions exclude the cross-correlated, serially dependent noise of real macro panels (cf. Boivin–Ng 2006) and the static ML estimation ignores dynamics; (iv) no forecasting target, horizon or out-of-sample evaluation is used — Table 3 is purely about $x$; (v) no standard errors for $\hat\rho$; the sample changes with $k$ because series are dropped; (vi) typos: $e_h=s_{Qt}-s_t$ (should be $h$), missing transposes on $Q$ in the proof, the $\lambda$ definition, and the Wald display noted above.
- **Status:** preliminary; Theorem 2 lacks rates and the fully empirical small-noise theory is unfinished.

## Practical relevance for a quant PM

- A cheap diagnostic before trusting PCA factors in a macro or statistical risk model: fit a factor model (or use a PCA/ML split of $\Omega$), compute $\rho=\max_i\hat\Psi_{ii}\cdot\mathrm{tr}(\hat\Lambda^{-1})/k$ and $2k\sqrt{\rho}$. Values well below 1 give a meaningful guarantee on $E|e_h|/\sqrt{\beta'\beta}$; values ≥ 1 mean you are relying on empirical performance, not theory.
- Implies preferring few strong factors and curating the panel (drop near-pure-noise series, which inflate $\max\Psi_{ii}$), or using full ML factor analysis (which weights by $\Psi^{-1}$) when $\rho$ is not small — consistent with the "more data is not always better" evidence.
- The bound is relative to the *signal* $\sqrt{\beta'\beta}$ and worsens as $1/r^2$: for low-$R^2$ targets (return forecasting), estimation error of $\beta$ dominates unless $T$ is very large.
