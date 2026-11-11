# Identification Theory for High Dimensional Static and Dynamic Factor Models

**Authors:** Jushan Bai and Peng Wang. **Publication:** *Journal of Econometrics* 178 (2014), 794–804; available online November 2013. DOI: 10.1016/j.jeconom.2013.11.001. **Source PDF:** [DynamicFactorModels_BaiWang_2014.pdf](../../Finance/DynamicFactorModels_BaiWang_2014.pdf).

## Main contribution

The paper turns identification of a large factor model into identification of a small rotation matrix. Its central result is that three apparently different Jacobian rank conditions are equivalent under stated full-rank assumptions. The largest differentiates directly with respect to all loadings; an intermediate condition works with rotations of the static factor stack; the smallest works with a rotation of only the dynamic factors. If there are $q$ dynamic factors, the smallest test has $q^2$ columns even when the model has thousands of loading parameters.

The economic purpose is to move beyond identifying common components. A principal-components model may consistently recover the common part of every observed series while leaving individual factors and loadings arbitrary up to rotation. That can suffice for forecasting, but it does not suffice for saying that a particular factor is monetary policy, technology, or another structural source of variation. Restrictions intended to support such interpretations must actually eliminate the remaining observational equivalence. The paper provides a tractable way to check whether they do.

The contribution extends the classical restricted static-factor identification framework to finite distributed-lag dynamic factor models, serially correlated factors, VARMA factor dynamics, structural VARs, and nonlinear restrictions such as long-run exclusions. It explicitly allows overidentifying restrictions. The result is not merely a count of restrictions: the restrictions must act independently on the directions of observational equivalence at the parameter values being considered.

This is a theoretical paper. It contains proofs and worked classes of identifying restrictions, not a simulation tournament or an empirical investment application. Its evidence is algebraic equivalence of null spaces and local rank conditions. There are no reported forecast improvements, risk-adjusted returns, confidence intervals for a fitted economic model, or preferred financial dataset to reproduce. Reproducibility here means being able to construct the correct derivative matrix and verify the model assumptions and numerical rank.

## What is assumed identified before the analysis begins

The static starting point is

$$
y_t=\Lambda F_t+e_t,\qquad E[F_tF_t']=I_r,\qquad E[e_te_t']=\Psi,
$$

where $y_t$ is an $N$-vector, $F_t$ an $r$-vector, and $\Lambda$ an $N\times r$ matrix of full column rank. Factors and errors are uncorrelated. Hence

$$
\Sigma_y=\Lambda\Lambda'+\Psi.
$$

The paper assumes that the common covariance $\Lambda\Lambda'$ can be identified in the large-dimensional approximate factor environment. It motivates this assumption through the existing asymptotic factor literature. It does not solve unrestricted covariance decomposition for arbitrary finite $N$, arbitrary $\Psi$, and arbitrary weak signals. The weak-dependence and pervasive-factor structure underlying that decomposition is a prerequisite.

This separation is important. The model can allow cross-sectional correlation in idiosyncratic errors, rather than requiring a diagonal $\Psi$. But allowing an unrestricted error covariance of the same strength as the common covariance would destroy the initial decomposition. “Approximate factor model” provides economic and asymptotic structure; it is not permission to assign any covariance component to either side without restriction.

Once $\Lambda\Lambda'$ is known, $\Lambda$ remains identifiable only up to an orthogonal rotation under the normalization $E[F_tF_t']=I_r$. For any orthogonal $A$, replacing loadings by $\Lambda A'$ and factors by $AF_t$ preserves observables and their common covariance. The remaining problem is to show that the imposed restrictions single out a loading matrix locally.

Local identification at $\Lambda^*$ means that a sufficiently small neighborhood contains no other admissible parameter value with the same identifying information. It is weaker than global identification. Discrete sign changes, permutations, or isolated remote solutions can remain. A numerical optimizer converging repeatedly to one solution also does not establish identification: optimizer behavior and population observational equivalence are different questions.

## Static linear restrictions and the small Jacobian

Write linear restrictions as

$$
M\operatorname{vec}(\Lambda)=m,
$$

where vectorization stacks columns. Let $D_r$ be the duplication matrix mapping the lower-triangular vector of a symmetric matrix to its full vectorization, and let $D_r^+$ be its Moore–Penrose inverse. The small rank condition is

$$
\operatorname{rank}
\begin{bmatrix}
D_r^+\\
M(I_r\otimes\Lambda)
\end{bmatrix}=r^2.
$$

This is the Bekker condition revisited in Section 2. The paper derives it by introducing an identified representative $C=\Lambda A'$ and solving for $\Lambda=CA$. The restrictions become $M(I_r\otimes C)\operatorname{vec}(A)=m$. Orthogonality supplies $A'A=I_r$. Evaluating the Jacobian of these two sets of restrictions at $A=I_r$ gives the displayed matrix, apart from a factor of two in the orthogonality rows that does not change rank.

The alternative direct-loading condition has $Nr$ columns:

$$
\operatorname{rank}
\begin{bmatrix}
D_N^+(\Lambda\otimes I_N)\\
M
\end{bmatrix}=Nr.
$$

Both tests describe the same local ambiguity, but the first removes the nuisance dimensions that are already pinned down by the common covariance. When $N$ is large and $r$ is small, this reduction is substantial. It also makes the economic content easier to see: only rotations still need to be constrained.

To interpret the rank condition, perturb the rotation as $A=I_r+\epsilon Y$. Orthogonality to first order gives $Y+Y'=0$, so the remaining directions are skew-symmetric. Their dimension is $r(r-1)/2$. The loading restrictions must eliminate every nonzero such $Y$ through

$$
M\operatorname{vec}(\Lambda Y)=0.
$$

Merely writing down $r(r-1)/2$ restrictions is therefore an order condition, not a sufficient rank condition. Redundant exclusions or restrictions with zero derivatives along the relevant rotations do not identify the model. A lower-triangular leading $r\times r$ loading block with nonzero diagonal is a familiar sufficient example in the paper; the nonzero diagonal is substantive because it anchors the factor directions.

## Nonlinear static restrictions and eigenvalue separation

For smooth restrictions $\phi(\Lambda)=0$, replace $M$ by the derivative of the restriction map:

$$
\operatorname{rank}
\begin{bmatrix}
D_r^+\\
\phi_\Lambda(I_r\otimes\Lambda)
\end{bmatrix}=r^2,
\qquad
\phi_\Lambda=\frac{\partial\phi}{\partial\operatorname{vec}(\Lambda)'}.
$$

Section 2.3 studies the normalization that $\Lambda'\Lambda$ is diagonal with distinct diagonal elements arranged in decreasing order. If $J_r$ selects its strictly lower-triangular elements, the zero restrictions are $J_r\operatorname{vec}(\Lambda'\Lambda)=0$. Their derivatives, combined with the orthogonality conditions, have a determinant involving differences between diagonal elements. Distinct eigenvalues remove continuous rotations; repeated eigenvalues leave rotations within the repeated-eigenvalue subspace.

An elementary two-factor illustration clarifies this claim. Let $\Lambda'\Lambda=\operatorname{diag}(d_1,d_2)$ and perturb by a skew-symmetric rotation with one free angle. The first-order change in the off-diagonal Gram entry is proportional to $d_1-d_2$. If that difference is zero, the diagonalization restriction cannot distinguish the angle. If the difference is small, the restriction distinguishes it only weakly. This illustrates the paper's algebra and also explains why a formally full-rank sample Jacobian may be poorly conditioned.

The ordering restriction resolves a permutation convention; a positive-loading or another explicit sign convention may still be needed to compare factors across runs. The local derivative calculation does not automatically impose those discrete choices. A careful implementation keeps equality restrictions, inequality conventions, and numerical sign alignment conceptually separate.

## Finite distributed-lag dynamic models

The dynamic observation equation is

$$
y_t=\Lambda_0f_t+\Lambda_1f_{t-1}+\cdots+\Lambda_sf_{t-s}+e_t,
$$

with $q$ dynamic factors. In the initial dynamic development, $f_t$ is serially uncorrelated with covariance $I_q$, and $e_t$ is serially uncorrelated and orthogonal to factors at all leads and lags. Dynamic behavior still exists because a shock affects observations through several loading lags.

Use two distinct loading arrangements:

$$
\Lambda=[\Lambda_0,\Lambda_1,\ldots,\Lambda_s],\qquad
\bar\Lambda=(\Lambda_0',\Lambda_1',\ldots,\Lambda_s')'.
$$

The first has $N$ rows and $q(s+1)$ columns; the second has $N(s+1)$ rows and $q$ columns. They contain the same coefficients in different arrangements. The paper writes restrictions either as $R\operatorname{vec}(\Lambda)=m_2$ or $M\operatorname{vec}(\bar\Lambda)=m_1$. These restriction matrices cannot be exchanged without the corresponding permutation of coefficient order.

Assume

$$
\operatorname{rank}(\Lambda)=q(s+1).
$$

This requires enough observed series and sufficiently distinct loading patterns across current and lagged factors. It rules out cases in which the chosen static stack is redundant. Under this condition, the small dynamic identification test is

$$
\operatorname{rank}
\begin{bmatrix}
D_q^+\\
M(I_q\otimes\bar\Lambda)
\end{bmatrix}=q^2.
$$

The column dimension depends on the number of dynamic factors, not on the number of observed series or loading lags. The number of rows can still grow with the restrictions, and constructing those rows still uses all relevant loadings. Thus the paper reduces the difficult rank dimension rather than claiming that every computational cost is independent of panel size.

## Why dynamic consistency removes rotations of the static stack

A generic static representation stacks $F_t=(f_t',\ldots,f_{t-s}')'$. Without using its temporal structure, one might permit any invertible rotation of this $q(s+1)$-dimensional vector. Most such rotations do not produce another vector whose successive blocks are lags of one common $q$-dimensional process. That temporal overlap is the source of the additional identification information.

Lemma 1 establishes that an admissible stack transformation must have the form

$$
\bar A=I_{s+1}\otimes A,
$$

with the same invertible $q\times q$ matrix in every lag block. To obtain this result, the paper requires the covariance of an augmented stack $G_t=(F_t',f_{t-s-1}')'$ to be positive definite and its sample second moment to converge to that covariance. Comparing the different implied representations of the same transformed $f_t$ gives linear identities in $G_t$. Positive definiteness forces their coefficient matrices to vanish, eliminating off-diagonal blocks and equating the diagonal blocks.

This condition excludes deterministic linear relations among the required lagged factor values. A stationary VAR with nonsingular white-noise innovations satisfies the stated condition. The full-column-rank loading condition and the augmented-state covariance condition play different roles: the first ensures the data contain all specified static directions; the second ensures the temporal stack has the required independent variation.

For a white-noise dynamic factor with unit covariance, the surviving $A$ is orthogonal. Only its $q(q-1)/2$ continuous rotation directions require additional independent restrictions. The proof therefore explains why using a generic identification count for $q(s+1)$ unrelated static factors overstates the remaining freedom. Lag consistency has already removed most of that freedom before any economically motivated exclusions are applied.

## Equivalence of the three dynamic rank tests

Theorem 2 establishes equivalence of three tests when the horizontal loading matrix has full column rank. Their column counts are $q^2$, $[q(s+1)]^2$, and $Nq(s+1)$, respectively. The latter differentiates the identifying moments directly with respect to all loading coefficients. The intermediate test differentiates with respect to a rotation of the whole static stack. The small test uses only the common dynamic-factor rotation.

The paper's proof is best understood through null directions. Let $Y$ be a perturbation of the dynamic rotation, $W$ a perturbation of the static rotation, and $Z$ a perturbation of the loading matrix. Nonidentification means that a nonzero perturbation leaves the relevant moments and restrictions unchanged to first order.

For the small test, the null equations are $Y+Y'=0$ and $M\operatorname{vec}(\bar\Lambda Y)=0$. Such a direction generates a static perturbation $W=I_{s+1}\otimes Y$ and a loading perturbation $Z=\Lambda W$. Therefore any failure of the small test also appears in the larger formulations.

For the converse, the autocovariance restrictions constrain an admissible $W$ to a repeated block-diagonal form. The proof works backward through the lag selectors, showing that off-diagonal blocks vanish and the diagonal blocks coincide. A nonzero static null direction therefore yields a nonzero small null direction. Finally, a loading null direction lies in the column space of $\Lambda$, so $W=\Lambda^+Z$ transfers it back to the static-rotation formulation. Full column rank makes these transformations legitimate.

For one loading lag, the identifying common moments are particularly transparent:

$$
E[y_ty_t']-\Psi=\Lambda_0\Lambda_0'+\Lambda_1\Lambda_1',\qquad
E[y_ty_{t-1}']=\Lambda_1\Lambda_0'.
$$

The first pins down a static common covariance; the second links the lag blocks. For general $s$, the Appendix supplies selection matrices that express all lagged common covariances in a uniform form. An implementation can differentiate these moment equations directly for a small synthetic model to verify that its reduced test agrees with the full test.

## Serial correlation and the importance of innovation normalization

Section 3.3 allows serially correlated factors, represented as

$$
f_t=\sum_{j=0}^{\infty}B_j\varepsilon_{t-j},\qquad B_0=I_q,\qquad E[\varepsilon_t\varepsilon_t']=I_q.
$$

Under the two rank and covariance assumptions, the admissible transformation still acts through one common $q\times q$ matrix. The normalization of both the contemporaneous innovation coefficient and innovation covariance forces that matrix to be orthogonal. Theorem 3 then uses the same small condition as above.

Dropping $B_0=I_q$ changes the identification problem. The transformation need no longer be orthogonal, and the orthogonality rows $D_q^+$ cannot be counted as available information. Corollary 1 replaces the condition with

$$
\operatorname{rank}[M(I_q\otimes\bar\Lambda)]=q^2.
$$

All $q^2$ directions of an unrestricted invertible transformation must now be controlled by loading restrictions. Fixing the leading $q\times q$ block of $\Lambda_0$ to the identity is an example that can do this. By contrast, a triangular loading block that sufficed after covariance normalization may leave scale directions unresolved in the unrestricted case.

This distinction is especially relevant when moving between software packages with different factor normalizations. A condition valid for unit innovations and identity impact does not automatically apply to a model whose factor innovation covariance or contemporaneous impact is freely estimated. The relevant transformation group must be derived from the actual parametrization.

## Joint identification with VARMA restrictions

The parametrized factor process is

$$
f_t=\sum_{i=1}^a\Phi_if_{t-i}+\sum_{j=0}^bB_j\varepsilon_{t-j},\qquad B_0=I_q.
$$

Assumption 3 requires that this VARMA representation be unique if the factor process itself were observed. The paper lists stationarity, invertibility, left-coprimeness of the autoregressive and moving-average matrix polynomials, and a rank condition on their highest-order coefficient blocks as sufficient conditions. A canonical echelon representation is another route. Factor-rotation identification does not cure an intrinsically nonunique VARMA parametrization.

Restrictions can be imposed separately on loadings, autoregressive coefficients, and moving-average coefficients, or jointly across those parameter groups. To reproduce the small test without ambiguity about vectorization, consider a perturbation $Y$ of the common transformation. The corresponding parameter directions are

$$
\delta\bar\Lambda=\bar\Lambda Y,\qquad
\delta\Phi_i=\Phi_iY-Y\Phi_i,\qquad
\delta B_j=B_jY-YB_j.
$$

Stack their vectorizations in the exact order used by the restriction function. The derivative of each commutator is $I_q\otimes\Phi_i-\Phi_i'\otimes I_q$, and analogously for $B_j$. Let $K$ denote the resulting stacked linear map from $\operatorname{vec}(Y)$ to the parameter perturbation. For general nonlinear restrictions $\phi(\theta)=0$, Corollary 4 gives the joint criterion

$$
\operatorname{rank}
\begin{bmatrix}
D_q^+\\
\phi_\theta K
\end{bmatrix}=q^2.
$$

The commutators reveal which restrictions can identify orientation. If a dynamics matrix is a scalar multiple of identity, it commutes with every rotation and supplies no orientation information by itself. Heterogeneous dynamics can provide such information, but the derivative must verify that the chosen restrictions actually exploit it. Restriction counts alone miss this degeneracy.

## Structural VARs and long-run restrictions

The structural case instead writes

$$
f_t=\sum_{i=1}^a\Phi_if_{t-i}+B_0\varepsilon_t,\qquad E[\varepsilon_t\varepsilon_t']=I_q,
$$

with unrestricted $B_0$. Identifying the factor orientation does not identify the structural impact matrix, because the reduced-form innovation covariance identifies $B_0B_0'$, not $B_0$ itself. Theorem 4 therefore works with two sets of unknown local directions: the factor transformation and the structural impact matrix. Its reduced Jacobian has $2q^2$ columns.

For separate linear restrictions on loadings, dynamics and impact, the condition is

$$
\operatorname{rank}
\begin{bmatrix}
M_\Lambda(I_q\otimes\bar\Lambda)&0\\
M_\Phi K_\Phi&0\\
0&M_0\\
D_q^+(B_0B_0'\otimes I_q)&D_q^+(B_0\otimes I_q)
\end{bmatrix}=2q^2,
$$

where $K_\Phi$ stacks the commutator derivatives in the coefficient order selected by $M_\Phi$. The last row block comes from differentiating the identified covariance $AB_0B_0'A'$ at $A=I_q$. Common factors and structural shocks are being identified jointly, so one cannot import a result for an SVAR with observed variables without accounting for the latent-factor rotation.

The paper's worked nonlinear example imposes long-run exclusions. Define

$$
S=\left(I_q-\sum_{i=1}^a\Phi_i\right)^{-1},\qquad
\phi=J\operatorname{vec}(SB_0)=0.
$$

The derivative with respect to the impact matrix is $J(I_q\otimes S)$. For each autoregressive coefficient block, the derivative is $J(B_0'S'\otimes S)$. These are combined with loading restrictions, any additional short-run restrictions, the covariance rows, and the transformation derivatives in the general $2q^2$-column test. Existence of $S$ is necessary for this stated long-run restriction to be meaningful.

The paper stresses that the result is local. Even when an observed-factor SVAR has a global identification result, a model with latent factors need not inherit it. The extra observational equivalence of the latent representation must be addressed directly.

## Reading a failed rank test as an economic ambiguity

A null vector is more informative than a binary failure. Reshape a null vector of the small Jacobian into a matrix $Y$. In the normalized case, the orthogonality rows imply that $Y$ is skew-symmetric. The induced changes $\bar\Lambda Y$ and the associated commutators then show which loading and propagation patterns can move together while preserving the restrictions. This identifies the combination of factors that remains arbitrary. Reporting that direction helps distinguish an insufficient number of restrictions from a poorly chosen set that happens to be redundant at the estimated parameter values.

For a two-factor normalized static model, write

$$
Y=\begin{bmatrix}0&-a\\a&0\end{bmatrix}.
$$

Suppose the first row of the loading matrix is $(\lambda_{11},\lambda_{12})$ and the restriction fixes $\lambda_{12}=0$. The derivative of that restricted entry along the rotation is $-a\lambda_{11}$. A nonzero first loading therefore forces $a=0$ and anchors the local orientation. If $\lambda_{11}=0$ as well, the same zero restriction supplies no first-order information about orientation. This simple calculation explains why the standard triangular normalization requires nonzero diagonal elements. It also shows why changing the ordering of the observables can matter for the numerical quality of a triangular identification scheme.

With an unrestricted invertible transformation instead of an orthogonal one, there are four local directions in a two-factor model, not one. A single zero loading cannot remove scale and shear transformations. The distinction is sometimes hidden by reporting only the final loading matrix, without reporting how innovation variances were normalized. Reproducing the paper's condition requires the normalization to be part of the model specification, because it supplies actual identifying equations.

For dynamic factors, restrictions may be distributed across lag blocks. There is no requirement that all useful restrictions occur in $\Lambda_0$. Because the same $A$ acts on each block, a restriction on a delayed response can identify an orientation left ambiguous by contemporaneous responses. This is one reason the vertically stacked loading matrix appears in the small test. Restrictions on separate lag blocks still have to be linearly independent after multiplication by that stack; simply spreading restrictions over several horizons does not guarantee extra information.

Overidentification also has a precise interpretation. Once the reduced Jacobian has full column rank, additional restrictions may narrow the admissible population model without removing any further local rotation direction. They can be useful for testing substantive implications, but the paper does not develop such overidentification tests or their reference distributions. Identification feasibility and empirical validity of restrictions should therefore be assessed separately. An overidentified model can be uniquely defined and still fit the data badly because its economic assumptions are false.

The SVAR covariance block illustrates a further ambiguity that survives factor identification. Even with a completely fixed factor coordinate system, replacing $B_0$ by $B_0Q$ for an orthogonal shock rotation $Q$ preserves $B_0B_0'$. To identify named structural shocks, restrictions must distinguish these impact rotations. Conversely, restrictions that identify an impact orientation conditional on observed factors may leave the factor coordinate system free when those factors are latent. The joint $2q^2$ formulation is designed to catch both issues at once rather than declaring success after solving only one of them.

## Reproducible implementation and limits

A practical implementation begins by fixing the model class, dimensions, lag order, innovation normalization, and vectorization convention. Verify the horizontal loading rank and the augmented-state covariance assumption before using the dynamic reduction. Write every equality restriction as an explicit function of parameters, including the exact order in which coefficients are stacked. Differentiate that function analytically or with checked automatic differentiation, compose it with the transformation map, and append the appropriate covariance or orthogonality rows.

Compute a singular-value decomposition of the resulting matrix. Report singular values and row/column scaling along with the numerical rank. The paper establishes population rank conditions; it does not specify a universal floating-point threshold, a statistical test for near-singularity, or a finite-sample confidence level for identification strength. A tiny nonzero singular value indicates a direction that may be difficult to distinguish in estimated data even if the formal condition holds.

Several implementation checks follow directly from the theory. A restriction duplicated verbatim must not increase rank. Removing a necessary anchor should reveal a null rotation. When eigenvalues coincide in a diagonal-Gram normalization, the test should lose the corresponding orientation direction. In a small synthetic distributed-lag model satisfying the assumptions, the three rank tests should agree. These are verification procedures implied by the mathematics, not experiments reported in the article.

A positive-definite sample covariance of the augmented factor stack is only a diagnostic for the population assumption. With a short sample, a nearly redundant dynamic representation can look full rank numerically. Conversely, an exact sample rank deficiency caused simply by too few observations does not demonstrate a population impossibility. The analyst should separate the algebraic population condition, the finite-sample dimension constraint, and numerical conditioning when reporting the check.

For scale, consider an illustrative model with $N=200$, $q=3$, and two loading lags. The direct-loading test has 1,800 columns, the static-rotation test has 81, and the dynamic-rotation test has nine. These are calculated dimensions from the paper's formulas, not measured runtime results. The reduction makes it feasible to inspect how an economic restriction acts on the few directions that remain unidentified.

The theory does not choose the correct economic restrictions, determine the number of factors, estimate the model, or guarantee stable finite-sample inference. Nonlinear rank reasoning is a local regularity tool; singular parameter points and remote observationally equivalent solutions require separate analysis. The most useful takeaway is operational: identify the common component first under the factor-model assumptions, then test whether the proposed restrictions eliminate every remaining admissible transformation. Economic labels are justified by that restriction structure and its credibility, not by the visual appearance of estimated factor time series.
