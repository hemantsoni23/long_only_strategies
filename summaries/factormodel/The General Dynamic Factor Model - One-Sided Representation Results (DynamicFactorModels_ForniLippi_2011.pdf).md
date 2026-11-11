# The General Dynamic Factor Model: One-Sided Representation Results

**Mario Forni, Marco Lippi · 2011 · *Journal of Econometrics* 163, 23–28 (doi 10.1016/j.jeconom.2010.11.003) · Source: `Finance/DynamicFactorModels_ForniLippi_2011.pdf` · Pure theory: representation results + estimation sketch; no data, no simulations, no consistency proof**

## Claim / contribution
Almost all practical DFMs assume the common components span a **finite-dimensional** space (finite number $r$ of static factors, "AF"). That rules out trivial models such as $x_{it}=\frac{1}{1-\alpha_iL}u_t+\xi_{it}$ with $\alpha_i\sim U[-0.9,0.9]$: one shock, infinitely many static factors. The unrestricted generalized DFM of Forni–Hallin–Lippi–Reichlin (2000) handles this via dynamic principal components, but its filters are **two-sided** (use future $x$) and are useless at the end of the sample. Assuming a **rational** common spectral density, the paper shows the general model can be rewritten as
$$H_n(L)x_{nt}=R_nv_t+H_n(L)\xi_{nt},$$
with $H_n(L)$ a *finite* (block-diagonal) matrix polynomial, $R_n$ $n\times q$, both obtainable from the common spectrum, and $H_n(L)\xi_{nt}$ still idiosyncratic — i.e. a **static factor model with exactly $q$ factors** in the filtered data, estimable with present and past observations only.

## Setup
$x_{nt}=\chi_{nt}+\xi_{nt}$, $\chi_{nt}=B_n(L)u_t$ (nested $B_n$), with
- A1 $u_t$ orthonormal $q$-dim white noise, square-summable $b_{ij}(L)$; A2 $\xi_{nt}$ weakly stationary; A3 $\xi_{nt}\perp u_s$ for all $n,t,s$;
- A4 first eigenvalue of the idiosyncratic spectrum $\lambda^\xi_{n1}(\theta)\le\bar\lambda$ for all $n,\theta$; A5 $q$-th eigenvalue of the common spectrum $\lambda^\chi_{nq}(\theta)\to\infty$ for all $\theta$.

Forni–Lippi (2001): stationarity plus "$q$-th eigenvalue of $\Sigma^x_n$ diverges, $(q+1)$-th bounded" is equivalent to this representation; then $q$, $\chi_{it}$, $\xi_{it}$ are unique (A4 allows e.g. correlated neighbours $\xi_{it},\xi_{i+1,t}$). $B_n(L)$ and $u_t$ are **not** unique: any all-pass $\mathcal B(L)$ with $\mathcal B(z)\mathcal B'(z^{-1})=I_q$ on $|z|=1$ gives $\tilde B_n=B_n\mathcal B$, $\tilde u_t=\mathcal B'(L^{-1})u_t$ — structural shocks need extra identification.

**Two-sidedness of dynamic PCs.** Using the first $q$ eigenvectors $p^x_{nj}(\theta)$ of $\Sigma^x_n(\theta)$, $u_{t,n}=(P_{n1}(L)',\dots)'x_{nt}$ with $P_{nj}$ the inverse Fourier transform of $p^x_{nj}(\theta)/\sqrt{\lambda^x_{nj}(\theta)}$, and $\chi_{it,n}=\operatorname{Proj}(x_{it}\mid u_{s,n},s\in\mathbb Z)\to\chi_{it}$. Example: $\chi_{it}=u_{t-1}$ ($i$ odd), $u_t$ ($i$ even), $\Sigma^\xi=I/2\pi$: first eigenvalue $(1+n)/2\pi$, $P_{n1}(L)=\frac{1}{\sqrt{n(1+n)}}(L^{-1},1,\dots,L^{-1},1)$ — contains the forward shift, so usable only for $t\le T-1$.

**Restricted model (AF).** If $\dim\overline{\operatorname{span}}(\chi_{it},i\in\mathbb N)=r<\infty$: $\chi_{nt}=C_nF_t$, $F_t=N(L)u_t$ ($r$ static factors, which are dynamic processes; "static" refers only to loadings). Contemporaneous PCA of $\Gamma^x_n$ then suffices (Stock–Watson, Bai–Ng, Forni et al. 2005/2009). Under the $1/(1-\alpha_iL)$ example, static-factor-number criteria give $\hat r\to\infty$ with $n$, and any criterion for $q$ based on a VAR for estimated $F_t$ is misspecified; Hallin–Liška (2007) is the only $q$-criterion not requiring finite $r$.

## Key representation results
**A6** $\Sigma^\chi_n(\theta)$ rational ⇒ for $n\ge\bar n$, rank $q$ a.e. and a **fundamental** rational representation $\chi_{nt}=C_n(L)v^{(n)}_t$ (no poles for $|z|\le1$, no zeros for $|z|<1$; $v^{(n)}_t$ in the span of present/past $\chi$), unique up to an orthogonal matrix. $v^{(n)}$ may depend on $n$ and $C_n$ need not be nested (odd/even example: fundamental noise is $u_{t-1}$ for $n=1$, $u_t$ for $n>1$). Nonfundamental case: $b(L)=(1-\alpha^{-1}L)/(1-\alpha L)$, $|\alpha|<1$ — $u_t$ is not recoverable from the past, but $w_t=\frac{1-\alpha L^{-1}}{1-\alpha L}(Lu_t)$ is unit white noise and $\chi_{it}=-\alpha^{-1}w_t$.

**Tall ⇒ generically zeroless.** For rational $n\times q$ $D(L)$ with numerator/denominator degrees $\le p_1,p_2$ (parameter space dimension $nq(p_1+p_2+1)$), $n>q$ ⇒ $\operatorname{rank}D(z)=q$ for all $z\in\mathbb C$ for generic parameters (a zero requires all $q\times q$ minors to vanish at one point; Anderson–Deistler 2008; Deistler et al. 2010). **A7:** $C_n(z)$ zeroless for $n\ge q+1$.

**(F) Finite AR inverse.** Tall zeroless $y_t=D(L)z_t$ ⇒ $A(L)y_t=D(0)z_t$ with $A(L)$ a finite polynomial. Example $q=1$, $\chi_{it}=\alpha_iu_t+\beta_iu_{t-1}$, $i=1,2$: $u_t=(\beta_2\chi_{1t}-\beta_1\chi_{2t})/(\alpha_1\beta_2-\alpha_2\beta_1)$ and, with $\delta=1/(\alpha_1\beta_2-\alpha_2\beta_1)$,
$$\begin{pmatrix}1-\delta\beta_1\beta_2L & \delta\beta_1^2L\\ -\delta\beta_2^2L & 1+\delta\beta_1\beta_2L\end{pmatrix}\begin{pmatrix}\chi_{1t}\\\chi_{2t}\end{pmatrix}=\begin{pmatrix}\alpha_1\\\alpha_2\end{pmatrix}u_t,$$
unique VAR(1) iff $\alpha_1\beta_2\neq\alpha_2\beta_1$. With $n=3$ there are infinitely many VAR(1)s: $u_t=c\chi_t/(c\alpha)$ for any $c\perp\beta$, $c\alpha\neq0$.

**A7′:** for every $n$ and every choice of $q+1$ indices, (i) $C_{n;i_1..i_{q+1}}(z)$ is zeroless and (ii) $\chi_{i_1..i_{q+1},t}$ has a *unique minimum-lag* AR representation. Consequence: present/past of any $q+1$ common components span the same space as all of them, so one can take $v_t$ independent of $n$ and nested $C_n(L)$: $\chi_{nt}=C_n(L)v_t$ (3.15). (A7′ excludes the odd/even example, which satisfies A7.)

**Cointegration (Sec. 3.3).** If $y_{it}=\varphi_{it}+\psi_{it}$ are I(1) and the model holds in first differences, a $q$-subvector of $\varphi$ is cointegrated iff $B_{i_1..i_q}(1)$ is singular; if **all** $q$-subvectors of a $(q+1)$-block are cointegrated, $B_{i_1..i_{q+1}}(z)$ has a zero at $z=1$ and the block has no finite AR representation. No test exists for latent common components in the general model, but only a *partition* into good $(q+1)$-blocks is needed — group variables by economic relationships to avoid "dangerous" blocks.

## Static representation with $q$ factors (Section 4)
Let $n=(q+1)m$, blocks $\chi_{[s]t}$ with minimum-lag AR $A_{[s]}(L)\chi_{[s]t}=R_{[s]}v_t$; stack $H_n(L)=\operatorname{diag}(A_{[1]}(L),\dots,A_{[m]}(L))$, $R_n=(R_{[1]}',\dots,R_{[m]}')'$:
$$\tilde x_{nt}=H_n(L)x_{nt}=R_nv_t+H_n(L)\xi_{nt}=\tilde\chi_{nt}+\tilde\xi_{nt}.\tag{4.19}$$
- **A8:** $q$-th eigenvalue $\nu_n$ of $R_nR_n'$ $\to\infty$ (pervasiveness of *contemporaneous* innovation loadings; not implied by A5 — in the MA(1) example A5 needs $\sum|\alpha_i+\beta_ie^{-i\theta}|^2\to\infty$, A8 needs $\sum\alpha_i^2\to\infty$).
- **A9:** $\lambda_{\max}\{A(e^{-i\theta})A(e^{-i\theta})^*\}\le\bar\mu$ uniformly over all $(q+1)$-blocks and $\theta$. Not implied by stability: $A(L)=\begin{pmatrix}1&\alpha L\\\beta L&1\end{pmatrix}$ is stable for $|\alpha\beta|<1$ but $\|A\|$ is unbounded as $\alpha\to\infty$.
- **Proof:** $a\Sigma^{\tilde\xi}_n(\theta)a^*=aH_n\Sigma^\xi_nH_n^*a^*\le\bar\lambda\bar\mu\|a\|^2$ (block-diagonality keeps $\|H_n\|\le\sqrt{\bar\mu}$ for any $m$); integrating over $\theta$ bounds the covariance eigenvalue of $\tilde\xi$. So (4.19) is an approximate static factor model with $q$ factors.
- **Why blocks:** an arbitrary AR inverse of the whole $\chi_{nt}$ can create a pervasive residual. Example: $\chi_{nt}=\alpha_nu_t+\beta_nu_{t-1}$, $c\perp\beta_n$, $\delta=(c\alpha_n)^{-1}$: $(I-\delta\beta_ncL)\chi_{nt}=\alpha_nu_t$ but $\check\xi_{it}=\xi_{it}+\delta\beta_i(c\xi_{n,t-1})$ — a common term loaded on all series, not idiosyncratic.

## Estimation sketch (Section 5; population, $\Sigma^\chi_n$ known)
1. For each diagonal $(q+1)\times(q+1)$ block of $\Sigma^\chi_n(\theta)$ compute the Wold representation $\chi_{[j]t}=G_{[j]}(L)w_{[j]t}$, $G_{[j]}(0)=I$, innovation covariance $\Gamma_{[j]}$ of rank $q$; $A_{[j]}(L)$ = unique minimum-lag left inverse of $G_{[j]}$.
2. $\Gamma_{[j]}=P_{[j]}\Lambda_{[j]}P_{[j]}'$ ($q$ nonzero eigenvalues); $v_{[j]t}=\Lambda_{[j]}^{-1/2}P_{[j]}'A_{[j]}(L)\chi_{[j]t}$ (orthonormal), $S_{[j]}=P_{[j]}\Lambda_{[j]}^{1/2}$, so $A_{[j]}(L)\chi_{[j]t}=S_{[j]}v_{[j]t}$.
3. Align rotations: $v_{[j]t}=K_{[j]}v_{[1]t}$, $K_{[j]}$ orthogonal,
$$K_{[j]}=E[v_{[j]t}v_{[1]t}']=\frac{1}{2\pi}\int_{-\pi}^{\pi}\Lambda_{[j]}^{-1/2}P_{[j]}'A_{[j]}(e^{-i\theta})\Sigma^\chi_{[j1]}(\theta)A_{[1]}(e^{-i\theta})^*P_{[1]}\Lambda_{[1]}^{-1/2}d\theta .$$
   Then $R_{[j]}=S_{[j]}K_{[j]}$.
4. $v_t=M_nR_n'H_n(L)x_{nt}$ with $M_n=(R_n'R_n)^{-1}$; error $M_nR_n'\tilde\xi_{nt}\to0$ in m.s. since $E\|\hat v_t-v_t\|^2\le C_\xi\operatorname{tr}(R_n'R_n)^{-1}\le qC_\xi/\nu_n$. Recover $\chi_{nt}$ by inverting $H_n(L)$ (one-sided).

In practice: plug in the FHLR (2000) estimate $\hat\Sigma^\chi_n(\theta)$ (first $q$ dynamic PCs of a smoothed periodogram); consistency for $n,T\to\infty$ is **left for future research** and would need extra conditions for periodogram consistency.

## Critical assessment
- **Solid:** the zeroless-tall-system argument and the block construction are elegant; the "no pervasive leakage" proof is short and clean, and the counterexample shows block-diagonality is essential, not cosmetic. The case against AF (a single shock with heterogeneous AR(1) propagation) is compelling and relevant to any panel with heterogeneous persistence.
- **Gaps:** no finite-sample theory, no algorithm for choosing minimum-lag AR orders or the block partition from noisy estimates, no guidance when $n$ is not a multiple of $q+1$; A7′ (every block zeroless with unique minimum-lag AR) and A9 (uniform filter bound) are strong and untestable; near-zero determinants (e.g. $\alpha_1\beta_2\approx\alpha_2\beta_1$) make recovery ill-conditioned.
- **Typos/inconsistencies:** (5.22) stacks $S_{[j]}K_{[j]}'$ although $v_{[j]}=K_{[j]}v_{[1]}$ implies $S_{[j]}K_{[j]}$; the claim that $R_n$ has mutually orthogonal columns is not implied by the blockwise construction (the bound above holds regardless); the A9 example's trace is printed as $|1+\alpha e^{-i\theta}|^2+|1+\beta e^{-i\theta}|^2$, whereas $\operatorname{tr}AA^*=2+|\alpha|^2+|\beta|^2$ — conclusion unaffected; $\Lambda_{[j]}$ is said to have "eigenvectors" on its diagonal (eigenvalues meant).

## Practical relevance for a quant PM
- If a return or macro panel has heterogeneous lead–lag responses to a few shocks (sector returns reacting at different speeds, macro series with different persistence), static PCA will need ever more factors and misstate the shock dimension; a dynamic-factor approach with $q$ small is the right object.
- The one-sided construction is what makes the GDFM usable for real-time forecasting/nowcasting and for risk models without look-ahead: filtering with small $(q+1)$-dimensional VARs, then cross-sectional averaging, recovers common innovations. Estimate $\hat\Sigma^\chi$ on a training window only to keep it truly out-of-sample.
- Practical cautions: pick blocks from economically related series, check block-VAR conditioning (small determinants/large filter norms amplify noise), and determine $q$ with a dynamic criterion (Hallin–Liška) rather than from a static-factor VAR.
