# Fourth Moment Structure of the GARCH (p,q) Process

Changli He and Timo Teräsvirta, *Econometric Theory* 15 (1999), 824–846. [Original PDF](../../Finance/GARCH_HeTerasvirta_1999.pdf). All 23 pages, including the references and the full proof appendix, were read. The principal existence condition, moment and autocorrelation formulas, and critical appendix constructions were checked visually. This is the higher-order standard GARCH paper, distinct from the authors' 1999 papers about a family of first-order models and about second-order autocorrelation shapes, and from their later exponential-GARCH work.

## Why this matters

A fitted GARCH model can have finite unconditional variance while its fourth moment is infinite. In that case, population kurtosis and the usual autocorrelation function of squared returns are not finite objects, however plausible a sample plot looks. This paper supplies a necessary and sufficient fourth-moment condition and formulas for the fourth moment and the complete squared-return autocorrelation function of a general standard GARCH process.

The contribution beyond earlier results is not just the familiar GARCH(1,1) formula. It is the treatment of arbitrary finite lag orders, including the initial squared-return autocorrelations that cannot be recovered from the later-lag recursion alone. Those quantities permit an internally consistent comparison between a fitted model and empirical kurtosis and squared-return dependence. The article is theoretical: it contains no financial dataset, fitted empirical parameter table, forecasting contest, or trading result.

The note first sets out the paper's notation and explicit second-order formulas, then provides a separately derived finite-matrix implementation for arbitrary orders. That alternative computation is labeled as a reconstruction, not attributed to the paper. It makes the general result executable without requiring an implementation to reproduce every bespoke matrix in the long appendix.

## Model, conventions, and the first moment check

The source uses $u_t=\varepsilon_t\sqrt{h_t}$, with independent identically distributed innovations, $E\varepsilon_t=0$, $E\varepsilon_t^2=\nu_2$ and $E\varepsilon_t^4=\nu_4$. It does **not** impose $\nu_2=1$ throughout. Therefore $h_t$ is the conditional scale squared; the conditional variance of $u_t$ is $\nu_2h_t$. Confusing these when using a nonstandardized innovation distribution changes both existence conditions and reported kurtosis.

Pad the shorter coefficient sequence with zeros and use a common order $p$:

$$
h_t=\alpha_0+\sum_{i=1}^{p}\beta_i h_{t-i}
+\sum_{i=1}^{p}\alpha_i u_{t-i}^2,\qquad \alpha_0>0,\quad \alpha_i,\beta_i\ge0.
$$

Here the first GARCH order counts variance lags and the second counts squared-return lags. In the general derivation the source initially takes positive terminal coefficients and $p\ge2$; the lower-order results follow by setting appropriate coefficients to zero in its explicit corollaries. This should not be mistaken for excluding GARCH(1,1). The analysis concerns the causal stationary process initialized in the remote past, rather than arbitrary transient moments after a finite initialization.

Define random coefficients and their moments:

$$
c_{it}=\beta_i+\alpha_i\varepsilon_t^2,\qquad
\gamma_{i1}=Ec_{it}=\beta_i+\alpha_i\nu_2,
$$

$$
\gamma_{i2}=Ec_{it}^2=\beta_i^2+2\alpha_i\beta_i\nu_2+\alpha_i^2\nu_4,
\qquad \gamma_j=\sum_{i=1}^{p}\gamma_{ij}\quad(j=1,2).
$$

For distinct coefficient indices, the same-time products are

$$
\widetilde\gamma_{ij}=E(c_{it}c_{jt})
=\beta_i\beta_j+(\alpha_i\beta_j+\alpha_j\beta_i)\nu_2+\alpha_i\alpha_j\nu_4,
$$

$$
\overline\gamma_{i1}=E(\varepsilon_t^2c_{it})=\beta_i\nu_2+\alpha_i\nu_4.
$$

The different $c_{it}$ at a given time share the same squared innovation and are not independent. Replacing $\widetilde\gamma_{ij}$ by $\gamma_{i1}\gamma_{j1}$ would remove precisely the dependence that matters for the fourth moment.

The finite second-moment condition is $\gamma_1<1$. Then

$$
m_h=Eh_t=\frac{\alpha_0}{1-\gamma_1},\qquad
Eu_t^2=\nu_2m_h.
$$

Assume $0<\nu_2<\infty$ and finite $\nu_4$. For a nondegenerate squared innovation, $\nu_4>\nu_2^2$. If the squared innovation is constant, some variance and correlation expressions become degenerate and their denominators must be checked separately. A mean-zero innovation need not be Gaussian or symmetric for the displayed squared-moment calculations; only the stated moments and independence enter them.

## The general fourth-moment theorem and its proof structure

Rewriting the variance recursion gives $h_t=\alpha_0+\sum_i c_{i,t-i}h_{t-i}$. Squaring and taking expectations yields the source's central identity

$$
Eh_t^2=\alpha_0^2+2\alpha_0\gamma_1m_h+\gamma_2Eh_t^2
+2\sum_{l<m}E(c_{l,t-l}c_{m,t-m}h_{t-l}h_{t-m}).
$$

The difficult terms are the mixed products. They cannot be factored into separate means because later variance values contain earlier innovations. Lemmas 1–5 repeatedly substitute the variance recursion until each mixed term is a linear combination of $m_h$ and $Eh_t^2$:

$$
E(c_{l,t-l}c_{m,t-m}h_{t-l}h_{t-m})
=\alpha_0\gamma_{l1}\gamma_{m1}M_1(l,m)m_h
+\gamma_{l1}M_2(l,m)Eh_t^2.
$$

The $M$ functions are deterministic functions of the coefficient moments. The appendix tracks distinct products of variance lags using $p^*=p(p-1)/2$ states and a transition expectation matrix $\Gamma$. Its spectral radius must be below one so the remaining remote-past terms vanish and the geometric matrix sum converges to $(I-\Gamma)^{-1}$. This is an explicit condition in the derivation, not an assumption that arbitrary matrix inverses exist.

Within that setup, Theorem 1 says that the fourth moment exists precisely when

$$
\gamma_2+2\sum_{l<m}\gamma_{l1}M_2(l,m)<1.
$$

Its value is

$$
Eu_t^4=
\frac{\alpha_0^2\nu_4[1+\gamma_1+
2\sum_{l<m}\gamma_{l1}\gamma_{m1}M_1(l,m)]}
{(1-\gamma_1)[1-\gamma_2-2\sum_{l<m}\gamma_{l1}M_2(l,m)]}.
$$

For an actual implementation, the matrix procedure below computes the same moments without treating the $M$ symbols as unexplained numerical inputs. The theorem's form remains useful: it displays the additional positive cross-lag contribution missing from the tempting but generally insufficient test $\gamma_2<1$.

The appendix carefully separates constant-times-variance terms, squared-variance terms, and unresolved mixed terms. Products of recursion matrices are factored into expectations only when their innovation timing permits this. Lemma 4 explicitly notes that the squared-variance vector is not independent of the neighboring matrix product. Same-time cross moments $\widetilde\gamma_{ij}$ are retained there. Lemma 5 then collects the coefficients, and substitution into the squared recursion proves the moment formula. Lemmas 6–9 perform a related construction for $E(u_t^2u_{t-n}^2)$, with separate initialization for $n\le p$ and a companion recursion thereafter.

## Explicit GARCH(2,2) formulas

For $p=2$, set $g=\gamma_{11}$, $d=\gamma_{21}$, $q=\gamma_{12}+\gamma_{22}$, and $t=\widetilde\gamma_{12}$. These shorthand letters refer to moments, not raw GARCH coefficients. Define

$$
S_1=(1+g+d)(1-d)+2gd,\qquad
S_2=(1-q)(1-d)-2gt.
$$

Assuming the finite-variance condition $g+d<1$, the fourth-moment condition is $S_2>0$, equivalently

$$
q(1-d)+2gt+d<1.
$$

The source states $d<1$ explicitly, which already follows from $g+d<1$ under nonnegative coefficients. The fourth moment and kurtosis are

$$
Eu_t^4=\frac{\alpha_0^2\nu_4S_1}{(1-g-d)S_2},
\qquad
K_u=\frac{Eu_t^4}{(Eu_t^2)^2}
=\frac{\nu_4S_1(1-g-d)}{\nu_2^2S_2}.
$$

Kurtosis means the raw standardized fourth moment; subtract three for excess kurtosis. It is invariant to the intercept's scale, whereas $Eu_t^4$ scales quadratically with $\alpha_0$. For this case the source's mixed-product coefficients simplify to $M_1(1,2)=1/(1-d)$ and $M_2(1,2)=t/(1-d)$, directly connecting the corollary to the general theorem.

The first two squared-return correlations can be computed without copying their expanded rational expressions. Let $H_2=Eh_t^2=Eu_t^4/\nu_4$, $b_1=\overline\gamma_{11}$, and $b_2=\overline\gamma_{21}$. Then

$$
M_1(1)=\frac1{1-d},\qquad
M_1(2)=\frac{1+g-d}{1-d},
$$

$$
M_2(1)=b_1+\frac{\nu_2t}{1-d},\qquad
M_2(2)=gb_1+b_2+\frac{\nu_2gt}{1-d}.
$$

For $n=1,2$, calculate

$$
J_n=E(u_t^2u_{t-n}^2)
=\alpha_0\nu_2^2M_1(n)m_h+\nu_2M_2(n)H_2,
\qquad
\rho_n=\frac{J_n-(\nu_2m_h)^2}{\nu_4H_2-(\nu_2m_h)^2}.
$$

For $n\ge3$, use $\rho_n=g\rho_{n-1}+d\rho_{n-2}$. These formulas are algebraically the source's Corollary 2 and equations (24)–(25). They make the first-lag initialization explicit and keep the units visible.

The companion matrix used for longer-lag calculations is

$$
\Gamma_*=
\begin{pmatrix}
1&0&0\\
\alpha_0&\gamma_{11}&\gamma_{21}\\
0&1&0
\end{pmatrix}.
$$

The main-text matrix on PDF page 7 correctly has $\gamma_{21}$ in its second row's last position. The repeated matrix on PDF page 21 prints $\gamma_{12}$ there. The correct entry follows both from the main text and from the expected variance recursion: it is the mean second-lag coefficient, not the second moment of the first-lag coefficient. The computations here use $\gamma_{21}$. This is a localized transcription issue; it does not change the corollary's stated formulas.

## A complete finite-matrix implementation for arbitrary orders

The following is an independently derived computational representation of this standard GARCH model. It avoids implementing the appendix's large family of intermediate matrices. It requires only linear algebra and $\nu_2,\nu_4$.

Form a $2p$-dimensional state

$$
X_t=(u_t^2,\ldots,u_{t-p+1}^2,h_t,\ldots,h_{t-p+1})'.
$$

With $z_t=\varepsilon_t^2$, write $X_t=A(z_t)X_{t-1}+b(z_t)$, where $A(z)=A_0+zA_1$ and $b(z)=b_0+zb_1$. Indices in the following construction are one-based:

1. Set row $p+1$ of $A_0$ to $(\alpha_1,\ldots,\alpha_p,\beta_1,\ldots,\beta_p)$.
2. Set row 1 of $A_1$ to the same vector.
3. For $j=2,\ldots,p$, set $(A_0)_{j,j-1}=1$ and $(A_0)_{p+j,p+j-1}=1$ to shift the two lag stacks.
4. All other entries are zero. Set $(b_0)_{p+1}=\alpha_0$ and $(b_1)_1=\alpha_0$, with all other components zero.

This state timing is deliberate. $A(z_t)$ is independent of $X_{t-1}$ because the new innovation is independent of all earlier observations. A state containing lagged random coefficients with overlapping innovation dates would not automatically have this property.

Let $\bar A=A_0+\nu_2A_1$. The state mean is $\mu=(I-\bar A)^{-1}(b_0+\nu_2b_1)$: its first $p$ entries equal $\nu_2m_h$ and its final $p$ entries equal $m_h$. Let $C=\operatorname{Var}(X_t)$ and let $e$ select the first coordinate. Define

$$
\mathcal K=A_0\otimes A_0+
\nu_2(A_0\otimes A_1+A_1\otimes A_0)+\nu_4A_1\otimes A_1,
$$

$$
Q=(\nu_4-\nu_2^2)m_h^2ee'.
$$

Then solve, using column-major vectorization,

$$
\operatorname{vec}(C)=(I-\mathcal K)^{-1}\operatorname{vec}(Q).
$$

Use a linear solve, not an explicitly formed inverse. The covariance solution must be symmetric and positive semidefinite within numerical tolerance. Check that the spectral radius of $\mathcal K$ is below one before interpreting the solution as a stationary finite covariance. Merely obtaining a finite algebraic solution when the spectral radius is at least one can produce a negative or economically meaningless matrix. Under the nonnegative, causal nondegenerate model assumptions, this lifted second-moment stability check implements the fourth-moment restriction.

The proof is short. Center the state:

$$
X_t-\mu=A(z_t)(X_{t-1}-\mu)+(z_t-\nu_2)m_he.
$$

The cross terms have expectation zero because the past centered state has mean zero and is independent of $z_t$. Thus $C=E[A(z_t)CA(z_t)']+Q$, which vectorizes to the equation above. The geometric series in $\mathcal K$ expresses the accumulation of past squared-innovation shocks and parallels the convergence argument in the original appendix.

Recover every quantity of interest as

$$
Eu_t^4=C_{11}+(\nu_2m_h)^2,\qquad
K_u=\frac{C_{11}+(\nu_2m_h)^2}{(\nu_2m_h)^2},
$$

$$
\operatorname{Cov}(X_t,X_{t-n})=\bar A^nC,\qquad
\rho_n=\frac{e'\bar A^nCe}{C_{11}}.
$$

The lag covariance identity follows by conditioning successively on past states. No normal distribution or simulation is used. A second internal check is $Eu_t^4=\nu_4[C_{p+1,p+1}+m_h^2]$. Scaling $\alpha_0$ by a constant should change $Eu_t^2$ by that constant and $Eu_t^4$ by its square, while leaving kurtosis and all correlations unchanged.

The lifted matrix has $(2p)^2$ rows and columns. For large $p$, the symmetry of $C$ or a matrix-free covariance operator can reduce memory, but any such optimization must preserve the cross terms in $\nu_2$. Computing only $E[A]\otimes E[A]$ would omit innovation variance and give the wrong fourth-moment condition.

## Squared-series dependence, special cases, and a qualification

Define $\eta_t=u_t^2-\nu_2h_t$. It is a martingale difference with $E\eta_t^2=(\nu_4-\nu_2^2)Eh_t^2$ when the fourth moment exists. Writing $x_t=u_t^2-Eu_t^2$, the centered squared process satisfies

$$
\left[1-\sum_{i=1}^{p}(\beta_i+\nu_2\alpha_i)L^i\right]x_t
=\left[1-\sum_{i=1}^{p}\beta_iL^i\right]\eta_t.
$$

This provides an independent explanation for the source's recursion $\rho_n=\sum_i\gamma_{i1}\rho_{n-i}$ for $n>p$. It also explains why an exponential envelope governs decay in a fixed finite-order model, although the first few lags can rise or oscillate in shape. Positive variance coefficients do not force the largest squared correlation to occur at lag one.

For GARCH(1,1), put $\delta=\beta+\alpha\nu_2$. The fourth moment exists if $\beta^2+2\alpha\beta\nu_2+\alpha^2\nu_4<1$, and

$$
K_u=\frac{\nu_4(1-\delta^2)}
{\nu_2^2[1-\delta^2-\alpha^2(\nu_4-\nu_2^2)]},
\qquad
\rho_n=\frac{\alpha\nu_2(1-\beta^2-\alpha\beta\nu_2)}
{1-\beta^2-2\alpha\beta\nu_2}\delta^{n-1}.
$$

The innovation fourth moment cancels from this correlation formula. More generally, for a fixed stable squared-series ARMA representation, its normalized autocorrelation is determined by the ARMA coefficients; the innovation fourth moment controls the innovation variance and the existence of the required moments. This observation is useful when checking numerical formulas that seem to depend on $\nu_4$ through many intermediate terms.

The source remarks after Theorem 2 that proximity to its fourth-moment boundary is associated with persistent autocorrelation. That statement needs a qualification if innovation kurtosis is allowed to vary independently of the variance coefficients. A derived counterexample takes $\alpha=\beta=.2$, $\nu_2=1$, $\nu_4=21.9$. The fourth-moment coefficient is $.996$, very close to one, but $\rho_1=.2090909$ and $\rho_n=\rho_1(.4)^{n-1}$: dependence still decays quickly. The return kurtosis is 4599. The exact formulas remain valid; proximity to moment divergence alone does not imply a root near one in the squared-series correlation recursion.

For an ARCH$(p)$, $\beta_i=0$ and the squared process is AR$(p)$ with coefficients $\nu_2\alpha_i$. Its initial correlations follow ordinary Yule–Walker equations. Under $\nu_2=1$, ARCH(2) gives

$$
\rho_1=\frac{\alpha_1}{1-\alpha_2},\qquad
\rho_2=\alpha_2+\frac{\alpha_1^2}{1-\alpha_2},\qquad
\rho_n=\alpha_1\rho_{n-1}+\alpha_2\rho_{n-2}\quad(n\ge3).
$$

Under Gaussian standardized innovations the fourth-moment condition reduces to

$$
3\alpha_1^2+3\alpha_2^2+3\alpha_1^2\alpha_2-3\alpha_2^3+\alpha_2<1.
$$

This is the paper's check against Milhøj's ARCH result. Non-Gaussian innovations change the fourth-moment condition; they do not change the displayed normalized ARCH autocorrelations when $\nu_2$ is held fixed and the fourth moment remains finite.

## Numerical checks and practical use

The following are calculations performed for this note, not empirical estimates or a numerical table from the source. For $\alpha_0=.1$, $(\alpha_1,\alpha_2)=(.1,.05)$, $(\beta_1,\beta_2)=(.5,.2)$ and $(\nu_2,\nu_4)=(1,3)$, the explicit corollary and the matrix implementation agree:

| Quantity | Calculated value |
|---|---:|
| $Eh_t$ | .666666667 |
| $Eu_t^4$ | 1.517706577 |
| Return kurtosis | 3.414839798 |
| $\rho_1$ | .146368715 |
| $\rho_2$ | .149273743 |
| $\rho_3$ | .126156425 |
| Spectral radius of $\mathcal K$ | .807782378 |

The second lag exceeds the first. Holding all coefficients and $\nu_2$ fixed but setting $\nu_4=9$ increases the fourth moment to 7.780979827 and kurtosis to 17.507204611; the correlations remain unchanged. The lifted spectral radius rises to .889365982. A separate check with nonunit $\nu_2=2$, $\nu_4=12$ and smaller ARCH coefficients also matches the source formulas, testing the variance normalization rather than only the standardized special case.

For a Gaussian ARCH(2) with $\alpha_0=.1$, $\alpha_1=.2$, $\alpha_2=.3$, the calculations give $Eh_t=.2$, kurtosis 4.943661972, $\rho_1=.285714286$ and $\rho_2=.357142857$. For a Gaussian GARCH(1,1) with $\alpha=.1$, $\beta=.85$, the kurtosis is 3.774193548 and the first squared correlation is .179069767. These are deterministic algebra checks, not Monte Carlo estimates.

To assess a fitted model, first record its return frequency, mean specification, coefficient convention and innovation normalization. Check the finite-variance condition, then the fourth-moment condition, before reporting kurtosis or squared-return correlations. Compare the model-implied quantities with corresponding statistics of mean-corrected returns or residuals at the same frequency. The comparison is a diagnostic, not an automatically calibrated hypothesis test. Sample kurtosis near the existence boundary can be unstable, and uncertainty in estimated parameters can cross that boundary even when the point estimate passes.

The source does not provide standard errors for estimated kurtosis, confidence regions for the existence condition, or a test for equality between model and empirical correlations. It also does not establish existence of moments above order four, extend the proof to asymmetric or exponential GARCH specifications, or evaluate finite-sample estimators. Those require additional theory and inputs. Reproduction of the theoretical calculations needs only coefficients and innovation moments; any empirical application additionally needs the actual series, the fitted mean and variance models, estimation details, parameter uncertainty and a justified sampling-inference procedure. The article's exact population formulas should not be confused with a promise that a heavy-tailed finite sample can estimate all those quantities accurately.
