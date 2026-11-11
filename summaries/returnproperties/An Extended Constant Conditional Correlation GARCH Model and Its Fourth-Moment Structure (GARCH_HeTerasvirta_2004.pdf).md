# An Extended Constant Conditional Correlation GARCH Model and Its Fourth-Moment Structure

Changli He and Timo Teräsvirta (2004), *Econometric Theory* 20, 904–926. [Source PDF](../../Finance/GARCH_HeTerasvirta_2004.pdf). This note covers all 23 PDF pages, including the proofs and references. Page references below refer to PDF pages unless a printed page is specified.

## Why this matters

Constant conditional correlation does not imply that volatility shocks remain within individual assets. The paper extends the usual CCC specification by allowing full matrices in the conditional-variance recursion, while preserving a fixed correlation matrix for standardized shocks. It then derives fourth moments and the complete correlation structure of squared observations. These quantities determine whether volatility diagnostics, squared-return regressions, and conventional standard errors have the population moments they presume.

The useful distinction is between contemporaneous correlation of returns and propagation of their conditional variances. A fixed return correlation matrix can coexist with asymmetric cross-lag correlations of squared returns, nonmonotone volatility autocorrelations, and substantial transmission between assets. Conversely, a fitted model can have finite unconditional variances but infinite fourth moments. A high persistence estimate cannot be interpreted safely without specifying which of these two moment conditions is being checked.

The contribution is analytical rather than a new forecasting contest. The paper generalizes diagonal CCC variance dynamics, obtains second- and fourth-moment conditions and formulas for the second-order model, derives squared-return correlations, and illustrates the formulas using simulations of theoretical correlation functions and previously estimated exchange-rate models. It does not estimate a new large covariance model or establish out-of-sample portfolio gains.

Several qualifications matter for implementation. The printed innovation assumptions allow distributions whose squared components are negatively associated. Under that generality, two positivity statements in the paper are too broad; an explicit counterexample appears below. There is also a printed first-order correlation recursion that does not agree with the preceding moment recursion. These are derived checks of particular claims, not a claim that the main Gaussian examples or all the moment theory are invalid.

## Model, normalization, and admissibility

Write returns as $y_t=\mu+\varepsilon_t$, with

$$
\varepsilon_t=D_tz_t,\qquad D_t=\operatorname{diag}(\sqrt{v_{1t}},\ldots,\sqrt{v_{Mt}}).
$$

The source writes the conditional standard deviations as $h_t$ and their elementwise squares as $h_t^{(2)}$; this note uses $v_t$ for the variance vector. The innovations $z_t$ are independent and identically distributed, independent of the past, with zero mean and positive definite covariance matrix $R$. Its diagonal entries equal one. Thus the scale is identified and

$$
E_{t-1}\varepsilon_t=0,\qquad
E_{t-1}(\varepsilon_t\varepsilon_t')=D_tRD_t.
$$

Let $x_t=\varepsilon_t^{(2)}$ denote elementwise squared shocks, and set $Z_t=\operatorname{diag}(z_{1t}^2,\ldots,z_{Mt}^2)$. Then $x_t=Z_tv_t$. The extended CCC recursion is

$$
v_t=a+\sum_{i=1}^{q}A_ix_{t-i}+\sum_{j=1}^{p}B_jv_{t-j}.
$$

Here $a$ is an $M$-vector and the coefficient matrices are $M\times M$. Positive components of $a$ and nonnegative entries in the matrices are sufficient to preserve positive variances. The paper does not claim these restrictions are necessary. They are a transparent implementation domain, especially when checking the positive-system arguments and examples.

The usual CCC model restricts every $A_i,B_j$ to be diagonal. The extension permits, for example, a squared shock in asset two to raise the next conditional variance of asset one through $(A_1)_{12}$. This affects the marginal variance processes while $R$ remains constant. It is not a dynamic conditional-correlation model, and the full conditional covariance still changes as $D_t$ changes.

For the principal second-order case, define

$$
C_{it}=A_iZ_t+B_i,\qquad \bar C_i=EC_{it}=A_i+B_i,\quad i=1,2.
$$

Then

$$
v_t=a+C_{1,t-1}v_{t-1}+C_{2,t-2}v_{t-2}.
$$

Although the innovation vectors are independent through time, $C_{1t}$ and $C_{2t}$ share the same $Z_t$ and are dependent. Moreover, $C_{1,t-1}$ is related to the innovation that enters the second lag of the adjacent recursion. Treating this equation as a scalar AR(2) with two independent random coefficients gives incorrect fourth moments.

## Second moments and the fourth-moment operator

With the source's positivity and innovation conditions, a spectral-radius restriction

$$
\rho(\bar C_1+\bar C_2)<1
$$

provides the stationary finite-second-moment case used in the paper. Its unconditional variance vector is

$$
m=Ev_t=Ex_t=(I-\bar C_1-\bar C_2)^{-1}a.
$$

This is a mean equation for conditional variances, not the covariance matrix of $v_t$. The off-diagonal unconditional return covariance is $R_{ij}E\sqrt{v_{it}v_{jt}}$, so it cannot generally be obtained by substituting $\sqrt{m_im_j}$.

For fourth moments define

$$
J_{ij}=E(z_{it}^2z_{jt}^2),\qquad H=E(v_tv_t'),\qquad Q=E(x_tx_t').
$$

Independence of current innovations and current variances implies $Q=J\odot H$, where $\odot$ is elementwise multiplication. Gaussian innovations give $J_{ij}=1+2R_{ij}^2$, including $J_{ii}=3$. For a non-Gaussian distribution, specifying $R$ does not specify $J$; it is a separate required input.

The following restates the paper's second-order fourth-moment solution in compact notation. All vectorization is columnwise. Let $K$ be the commutation matrix satisfying $K\operatorname{vec}(X)=\operatorname{vec}(X')$, and define

$$
G_{ij}=E(C_{it}\otimes C_{jt}),\qquad
V=(I-\bar C_2\otimes\bar C_2)^{-1}.
$$

The operator appearing in the source's fourth-moment condition is

$$
\Gamma=G_{11}+G_{22}
+(I+K)\left[
(\bar C_1\otimes I)VG_{12}
+(\bar C_1\otimes\bar C_2)VG_{21}
\right].
$$

Finite innovation fourth moments and $\rho(\Gamma)<1$, together with the preceding stationary conditions, give the stated sufficient fourth-moment condition. To evaluate the formula, put

$$
N=(I\otimes\bar C_2)V(a\otimes I)
+(\bar C_2\otimes\bar C_2)V(I\otimes a),
$$

$$
f=\operatorname{vec}(aa')
+\left[
\sum_{i=1}^2(\bar C_i\otimes a+a\otimes\bar C_i)
+(I+K)(\bar C_1\otimes I)N
\right]m.
$$

Then

$$
\operatorname{vec}(H)=(I-\Gamma)^{-1}f,\qquad
\operatorname{vec}(Q)=\operatorname{diag}(\operatorname{vec}J)\operatorname{vec}(H).
$$

The needed $G_{ij}$ follow by expanding $(A_iZ+B_i)\otimes(A_jZ+B_j)$. Since $EZ=I$, the two mixed terms require only first moments, while $E(Z\otimes Z)=\operatorname{diag}(\operatorname{vec}J)$. Matrix ordering must be preserved; these matrices generally do not commute.

The proof expands the outer product of the variance recursion, eliminates cross-lag variance products by repeated substitution, and sums the resulting matrix series. The commutation term accounts for the transpose of the cross product. The Appendix gives these steps rather than assuming the two lag coefficients are independent. The spectral restriction justifies convergence of the moment series. The paper compares this condition with an existing enlarged-state condition in a numerical example; similar admissible regions in that example are not a proof that the operators have identical eigenvalues.

An independent calculation using an enlarged iid random-coefficient state reproduced $H$ from the displayed formula to numerical precision for the paper's Figure 1 coefficient matrices. For $B_{2,11}=0.2,0.3,0.4$, the source operator's spectral radii were approximately $0.7640,0.8479,0.9601$. The enlarged-state operator gave $0.8803,0.9280,0.9827$. The fourth moments agreed, despite these different spectral radii. The intercept used for this check was $(0.1,0.2)'$; the figure's spectral comparison does not require an intercept.

## A direct implementation through an augmented state

A useful independently derived implementation avoids hand-coding the long second-order correlation formulas. Define

$$
s_t=(x_t',x_{t-1}',v_t',v_{t-1}')',\qquad
F=[A_1\ A_2\ B_1\ B_2].
$$

Since $v_t=a+Fs_{t-1}$, the random affine transition has first block $Z_t(a+Fs_{t-1})$, second block $x_{t-1}$, third block $a+Fs_{t-1}$, and fourth block $v_{t-1}$. Denote its coefficient matrix by $L_t$ and its intercept by $d_t$. Both depend only on current $Z_t$, hence are independent of $s_{t-1}$.

The stationary mean is $\bar s=(m',m',m',m')'$. Centering gives

$$
s_t-\bar s=L_t(s_{t-1}-\bar s)+\eta_t,\qquad
\eta_t=d_t+L_t\bar s-\bar s.
$$

Only the first block of $\eta_t$ is nonzero: it equals $(Z_t-I)m$. Consequently $W=E\eta_t\eta_t'$ has top-left block

$$
\operatorname{diag}(m)(J-\mathbf1\mathbf1')\operatorname{diag}(m)
$$

and zero elsewhere. The cross terms with the centered preceding state have zero expectation, even though $L_t$ and $\eta_t$ are dependent, because the preceding state is independent of both and has mean zero. Thus

$$
\operatorname{vec}(\Sigma_s)
=[I-E(L_t\otimes L_t)]^{-1}\operatorname{vec}(W).
$$

This is an alternative sufficient finite-covariance calculation when the operator is stable. It yields $Q-mm'$ from the first diagonal block and $H-mm'$ from the third. Cross-lag covariance is

$$
\operatorname{Cov}(s_t,s_{t-n})=(EL_t)^n\Sigma_s.
$$

Taking the first $M$ rows and columns supplies every squared-return covariance lag, including the first two. The expectations of $L_t\otimes L_t$ require only $J$, because $L_t$ is affine in $z_t^{(2)}$. This state formulation is a reconstruction for implementation and checking, not the paper's stated algorithm. Its higher dimension trades algebraic simplicity for memory cost: a dense fourth-moment system has dimension $(4M)^2$.

## Squared-return correlations and the first-order simplification

Use the source's orientation

$$
\Gamma_x(n)=\operatorname{Cov}(x_t,x_{t-n}),\qquad
D_x=\operatorname{diag}\sqrt{\operatorname{diag}\Gamma_x(0)},
$$

$$
R_x(n)=D_x^{-1}\Gamma_x(n)D_x^{-1}.
$$

Entry $(i,j)$ correlates the current squared return of asset $i$ with the lagged squared return of asset $j$. $R_x(n)$ need not be symmetric. A numerical implementation should record this orientation rather than transpose matrices to match an empirical table.

For $v_t=a+Ax_{t-1}+Bv_{t-1}$, let $C=A+B$. Independence gives an especially transparent derivation:

$$
\operatorname{vec}H=
[I-E(C_t\otimes C_t)]^{-1}
\operatorname{vec}\{aa'+a(Cm)'+(Cm)a'\}.
$$

Then

$$
\Gamma_x(0)=J\odot H-mm',
$$

$$
\Gamma_x(1)=A\Gamma_x(0)+B(H-mm'),
$$

$$
\Gamma_x(n)=C\Gamma_x(n-1),\qquad n\ge2.
$$

The lag-one equation follows from $\operatorname{Cov}(v_{t-1},x_{t-1})=H-mm'$. At lags two and higher, the previous current shock has been integrated out, giving the mean propagation matrix $C$. Therefore

$$
R_x(n)=D_x^{-1}CD_xR_x(n-1),\qquad n\ge2.
$$

These equations are also a compact way to implement the source's first-order corollary. The special displayed expression for $\operatorname{vec}R_x(2)$ after equation (28), on PDF page 10, does not follow from the preceding moment recurrence: it retains an intercept contribution and lacks the required propagation of the lag-one covariance. The centered recursion above follows directly from the model and the source's equation (25). It is the version used for the calculations here.

With diagonal $A,B$, each row $i$ decays geometrically at rate $C_{ii}$. In dimension two, a nonnegative full $C$ has real eigenvalues, since the discriminant is $(C_{11}-C_{22})^2+4C_{12}C_{21}\ge0$. At three or more dimensions, complex conjugate eigenvalues are possible, so individual correlations can rise initially or exhibit damped oscillation. This does not require time-varying $R$.

The Figure 2 trivariate example specifies

$$
a=(0.1,0.2,0.25)',\quad
A=\begin{pmatrix}.05&.25&.06\\.07&.08&.25\\.25&.08&.08\end{pmatrix},
\quad
B=\begin{pmatrix}.05&.40&.05\\.05&.07&.30\\.25&.08&.08\end{pmatrix},
$$

with Gaussian innovation correlations $R_{12}=0.2,R_{13}=0.3,R_{23}=0.23$. Recalculation from these printed inputs gives $m=(1.06587,1.12788,1.14690)'$ and fourth-moment operator radius $0.81364$. The eigenvalues of $A+B$ are $0.831776$ and $-0.210888\pm0.374633i$, whose complex modulus is $0.429911$. The caption instead reports a real eigenvalue $0.858$ and complex modulus $0.432$. The difference in the real eigenvalue exceeds ordinary rounding; the source does not provide alternative coefficients resolving it.

Using the listed matrices, the first asset's squared-return correlations at lags one through five are approximately $0.18226,0.18724,0.19754,0.14009,0.11902$. Thus the intended nonmonotone pattern is obtained. This check supports the mechanism, without asserting exact reproduction of every plotted point from a potentially inconsistent caption.

## Scope of the positivity and kurtosis claims

Marginal kurtosis inflation is straightforward:

$$
\frac{E\varepsilon_{it}^4}{(E\varepsilon_{it}^2)^2}
=E z_{it}^4\,\frac{Ev_{it}^2}{(Ev_{it})^2}
\ge E z_{it}^4.
$$

The inequality is Jensen's inequality for a single nonnegative random variance. It does not imply $E(v_{it}v_{jt})\ge Ev_{it}Ev_{jt}$ for different components. That would require nonnegative covariance between their variances. The elementwise off-diagonal extension in Corollary 1 and the general positive cross-correlation assertion in Property 3 require additional restrictions on innovation dependence.

For a concrete admissible counterexample, let $S$ take values $\pm1$ and $U$ take values $\pm0.5$, independently and equiprobably, and define

$$
z=S(\sqrt{1+U},\sqrt{1-U})'.
$$

These innovations have zero mean, unit marginal variances, and positive definite correlation matrix with off-diagonal $\sqrt{0.75}$. Their fourth-moment matrix has diagonal $1.25$ and off-diagonal $0.75$. Choose $a=(0.8,0.8)'$, $A=0.2I$, and $B=0$. All coefficients satisfy the paper's nonnegativity restrictions. The variance mean is $(1,1)'$ and the fourth-moment operator radius is only $0.05$.

Direct calculation gives $H_{11}=H_{22}=0.96/0.95=1.010526$ but $H_{12}=0.96/0.97=0.989691$. Consequently $Q_{12}=0.742268<0.75=J_{12}m_1m_2$, contradicting the unrestricted off-diagonal inflation statement. The contemporaneous squared-return variance is $0.263158$ in each component and its cross-covariance is $-0.257732$. Since $\Gamma_x(1)=0.2\Gamma_x(0)$, the first-lag cross-correlation is approximately $-0.195876$, not positive.

The diagonal example directly refutes Corollary 1, but Property 3 assumes strictly positive entries in $A$, including off-diagonals. To meet that stronger premise, retain the same innovations and instead set $A_{11}=A_{22}=0.2$, $A_{12}=A_{21}=0.001$, $a=(0.799,0.799)'$, and $B=0$. The variance mean remains $(1,1)'$, the fourth-moment operator radius is $0.05000875$, and the same moment equations give $H_{11}=H_{22}=1.01041811$, $H_{12}=0.98979892$, and first-lag squared-return cross-correlations $-0.19491531$. This strictly positive ARCH example also contradicts Property 3 as printed. Both examples have finite moments and nonzero positive return correlation. They exploit negative dependence between squared innovations. It leaves the marginal kurtosis inequality intact and does not contradict Gaussian illustrations, where squared innovations have nonnegative covariances. For applications with non-Gaussian innovations, a valid joint distribution and its $J$ should be specified before interpreting sign restrictions on volatility cross-correlations.

## Exchange-rate illustration: inputs and reported results

The empirical section reuses Bollerslev's previously estimated weekly exchange-rate models for the Deutschmark, French franc, Italian lira, Swiss franc, and British pound, all against the US dollar. The pre-EMS sample runs from July 1973 to the second week of March 1979, with 299 observations. The EMS sample runs from the third week of March 1979 to the second week of August 1985, with 333 observations.

The current paper supplies the fitted conditional-correlation matrices and resulting theoretical squared-return correlations, but does not reproduce the full intercept, ARCH, and GARCH coefficient estimates. Those are referred to the earlier paper. Thus its displayed material is enough to inspect the qualitative implications but insufficient to rebuild every empirical number without the earlier estimates and data.

Conditional correlations rise broadly across the two periods. For example, Deutschmark–French franc correlation rises from $0.607$ to $0.932$, Deutschmark–Italian lira from $0.425$ to $0.886$, and Swiss franc–British pound from $0.305$ to $0.635$. These are conditional correlations of standardized contemporaneous returns, not squared-return cross-lag correlations.

The following extracts the diagonal theoretical squared-return correlations from Table 2. Values are correlations, with weekly lags.

| Currency | Period | Lag 1 | Lag 2 | Lag 5 | Lag 10 |
|---|---|---:|---:|---:|---:|
| Deutschmark | EMS | .0462 | .0441 | .0384 | .0305 |
| French franc | EMS | .0150 | .0148 | .0144 | .0138 |
| Italian lira | EMS | .2175 | .1821 | .1067 | .0438 |
| Swiss franc | EMS | .2115 | .2096 | .2040 | .1949 |
| British pound | EMS | .1712 | .1652 | .1484 | .1242 |
| Deutschmark | Pre-EMS | .0584 | .0562 | .0502 | .0416 |
| French franc | Pre-EMS | .2039 | .1733 | .1064 | .0472 |
| Italian lira | Pre-EMS | .4939 | .4510 | .3432 | .2177 |
| Swiss franc | Pre-EMS | .3532 | .3454 | .3231 | .2891 |
| British pound | Pre-EMS | .1331 | .1104 | .0511 | .0154 |

The pre-EMS Italian-lira estimate originally violates the finite-fourth-moment condition. The authors reduce the relevant ARCH coefficient to $0.287$ to make the fourth moments exist before computing the displayed correlation functions. This is an analytical adjustment of a prior estimate, not a newly estimated constrained model. It affects interpretation of comparisons involving that series.

Two transcription or orientation issues prevent stronger directional claims. Under the source's definition, diagonal CCC implies that all cross-correlations in row $i$ decay with asset $i$'s variance persistence. Several displayed Table 2 cross-series instead decay with the column asset: for example, the EMS $r_{12}$ sequence decays slowly like the French franc, whereas $r_{21}$ decays like the Deutschmark. This suggests transposed labeling, but the full original parameter set is unavailable here, so the note does not silently assign a lead–lag direction.

Also, the printed pre-EMS $r_{42}$ sequence includes $0.0270,0.0229,0.0014,0.0062$ at lags $1,2,5,10$. The lag-five value was checked visually. It breaks the monotone geometric pattern of the other entries; a value near $0.0141$ would fit that pattern, but this is a diagnostic inference, not an authorized replacement of the reported number.

## Reproduction workflow and limits

A faithful theoretical implementation should accept $a,A_i,B_i,R$ and the innovation fourth-moment matrix $J$ as distinct inputs; verify the positivity domain; check the second-moment restriction; solve for $m$; and check fourth-moment stability before reporting squared-return correlations. Solve linear systems rather than explicitly forming inverses, symmetrize only within floating-point tolerance, and verify that $H-mm'$ and $Q-mm'$ are positive semidefinite. Material violations are evidence of a specification or vectorization error.

Use a fixed columnwise vectorization convention throughout the Kronecker calculations. Validate the general implementation against the first-order formulas, a diagonal univariate special case, and simulation with a declared burn-in and random seed. Monte Carlo is a diagnostic, not a replacement for the moment condition: apparent stability in a finite simulation does not establish finite population fourth moments.

For the empirical illustration, recover the earlier Bollerslev coefficient tables and the exact weekly return construction before claiming numerical replication. The local source does not provide a machine-readable data set, original estimation code, standard errors for the derived correlation functions, or confidence intervals for the period comparison. Its adjusted Italian-lira coefficient and the cross-correlation orientation issue should remain visible in any reproduction.

The economic interpretation is limited accordingly. Higher contemporaneous conditional return correlations after EMS do not imply that every volatility cross-correlation rises, and changes in a fitted correlation function do not establish a causal EMS effect. Parameter uncertainty, unequal sample lengths, and possible fourth-moment failure are substantive constraints. The durable contribution is the mapping from a multivariate variance recursion and innovation moments to its population volatility-dependence structure, together with explicit conditions under which that mapping exists.
