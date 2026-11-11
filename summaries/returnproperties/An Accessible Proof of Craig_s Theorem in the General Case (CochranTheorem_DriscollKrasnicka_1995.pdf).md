# An Accessible Proof of Craig's Theorem in the General Case

Michael F. Driscoll and Barbara Krasnicka, *The American Statistician* 49(1), February 1995, pp. 59–62. JSTOR 2684814. The local filename refers to Cochran's theorem, but the actual paper concerns Craig's independence theorem. The PDF includes a cover, the end of an unrelated preceding article, and teaching-material reviews after this paper's references; these neighboring items are not part of its argument.

Source: [CochranTheorem_DriscollKrasnicka_1995.pdf](../../Finance/CochranTheorem_DriscollKrasnicka_1995.pdf).

## Why this matters

Portfolio risk estimates, regression sums of squares, and Gaussian likelihood diagnostics often involve quadratic forms of the same data vector. Zero covariance between such statistics is generally weaker than independence. Craig's theorem supplies exact algebraic conditions for independence under joint normality, including nonzero means and singular covariance.

The paper's contribution is a proof intended to require only linear algebra and calculus. It separates the mean-dependent and covariance-dependent restrictions through cumulants and a confluent Vandermonde-type determinant. The theorem is established prior literature; the novelty claimed here is an accessible proof for the general singular case, together with corrections to an earlier proof's determinant argument.

A reader implementing the theorem can use the four displayed matrix conditions directly. A reader reproducing the proof should notice that its spectral expansion, as printed, needs additional treatment of zero-eigenvalue terms when the covariance is singular. The distinction between a correct criterion and an incomplete intermediate calculation matters.

## Exact statement and conventions

Let $x\sim N_p(\mu,V)$, where $V$ is symmetric positive semidefinite and may be singular. Let $A$ and $B$ be real symmetric $p\times p$ matrices. Define scalar quadratic forms $q_A=x^TAx$ and $q_B=x^TBx$. The theorem states that they are independent if and only if

$$
VAVBV=0,\qquad VAVB\mu=0,\qquad
VBVA\mu=0,\qquad \mu^TAVB\mu=0.
$$

All four conditions are needed in the stated generality: one matrix equation, two vector equations, and one scalar equation. In a nonsingular covariance model these reduce to $AVB=0$. In a centered model, $\mu=0$, only the first condition remains. A constant quadratic form is independent of every other random variable, so singular and degenerate cases should not be excluded merely for convenience.

Independence concerns the two scalar statistics, not independence of all coordinates of $x$. The theorem assumes genuine joint normality. An approximately normal marginal distribution or zero sample correlation is insufficient to invoke an exact result about the joint statistics.

The equivalent support formulation in the final section is

$$
z^TAVBw=0\quad\text{for all }z,w\in\mu+\mathcal R(V).
$$

Here $\mathcal R(V)$ is the range, equal to the row space for symmetric $V$. The Gaussian vector lives on this affine subspace almost surely. Expanding the bilinear expression over $z=\mu+Vu$ and $w=\mu+Vv$ yields precisely the four conditions. This formulation shows why checking only the range of covariance is insufficient when the mean shifts the support away from the origin.

## Whitened representation for implementation

A useful reconstruction starts with a thin covariance factor $V=TT^T$, where $T$ has $r=\operatorname{rank}(V)$ independent columns. Write $x=\mu+Tz$ with $z\sim N_r(0,I)$. Define

$$
C=T^TAT,\quad D=T^TBT,\quad
 d=T^TA\mu,\quad e=T^TB\mu.
$$

Then

$$
q_A=z^TCz+2d^Tz+\mu^TA\mu,
\qquad q_B=z^TDz+2e^Tz+\mu^TB\mu.
$$

The general criterion is equivalently

$$
CD=0,\qquad Ce=0,\qquad Dd=0,\qquad d^Te=0.
$$

This follows by substituting $TT^T$ into each original restriction and using the full column rank of $T$. It also gives an intuitive sufficiency proof. The symmetric matrices $C$ and $D$ act on orthogonal subspaces when $CD=0$. The linear part of each form has no component in the other form's quadratic subspace. In the remaining common nullspace, the two linear Gaussian components are orthogonal because $d^Te=0$. The forms consequently depend on disjoint independent Gaussian directions, apart from additive constants.

This is an explanatory coordinate reconstruction, not an empirical experiment reported by the authors. It avoids forming inverses of $V$ and is useful when risk models have redundant exposures or deterministic coordinates.

## Cumulants: the paper's analytical starting point

For any real symmetric matrix $C_0$, the $n$th cumulant of $x^TC_0x$ is

$$
\kappa_n(C_0\mid\mu,V)
 =2^{n-1}(n-1)!
 \left\{\operatorname{tr}[(C_0V)^n]
       +n\mu^TC_0(VC_0)^{n-1}\mu\right\}.
$$

For $n=1$ this is the mean, $\operatorname{tr}(C_0V)+\mu^TC_0\mu$. For $n=2$ it gives the familiar variance formula

$$
\operatorname{Var}(x^TC_0x)
 =2\operatorname{tr}[(C_0V)^2]+4\mu^TC_0VC_0\mu.
$$

Independence of $q_A$ and $q_B$ implies, for all real $s,t$ and every positive integer $n$,

$$
\kappa_n(sA+tB)=s^n\kappa_n(A)+t^n\kappa_n(B).
$$

Conversely, additive cumulants of every order imply a factorized joint moment-generating function in a neighborhood of zero. Finite-dimensional Gaussian quadratic forms have such a local analytic MGF, so this step is stronger than an unsupported assumption that any arbitrary moment sequence determines a distribution.

Substituting the theorem's four algebraic conditions eliminates mixed products and immediately proves sufficiency. Necessity is harder because the trace and mean terms can cancel at low orders. A covariance calculation alone does not separate them.

## How the determinant argument separates restrictions

For fixed $s,t$, collect the distinct nonzero eigenvalues $\lambda_1,\ldots,\lambda_k$ occurring among $sAV$, $tBV$, and $(sA+tB)V$. The authors represent cumulants through eigenvalue multiplicities and mean-related spectral coefficients. Additivity gives linear equations whose unknowns are differences of these coefficients between the combined matrix and its two components.

The coefficient columns have the forms $\lambda_j^n$ and $n\lambda_j^{n-1}$. These are power sequences and their derivatives, explaining the appearance of a confluent Vandermonde matrix. After scaling and reordering rows and columns, the matrix $L_k$ has paired columns built from $\lambda_j^n$ and $n\lambda_j^n$, with powers descending from $2k$ to 1. Its determinant is

$$
\det L_k=(-1)^k\prod_{i=1}^k\lambda_i^3
                 \prod_{i<j}(\lambda_i-\lambda_j)^4.
$$

All eigenvalues in this list are distinct and nonzero, so the determinant does not vanish. The coefficients must therefore vanish separately. The paper proves the factorization by induction: isolate a pair of columns, use a Schur complement with a nonsingular smaller matrix, establish multiplicity of each root and eigenvalue difference, then determine the remaining constant from the highest-degree coefficient.

The authors specifically correct two issues in an earlier proof: using an inverse of a block without first establishing its nonsingularity, and assigning the Schur-complement determinant an oversimplified form. The induction supplies the missing justification. These corrections are mathematical proof details, not changes to the economic meaning of the independence condition.

After separating the spectral coefficients, the intended conclusion is additivity of trace powers separately from additivity of mean terms:

$$
\operatorname{tr}[((sA+tB)V)^n]
 =s^n\operatorname{tr}[(AV)^n]+t^n\operatorname{tr}[(BV)^n],
$$

$$
\mu^T(sA+tB)[V(sA+tB)]^{n-1}\mu
 =s^n\mu^TA(VA)^{n-1}\mu
  +t^n\mu^TB(VB)^{n-1}\mu.
$$

Using the fourth-order trace identity and $V=TT^T$, a mixed coefficient is expressed as a sum of nonnegative squared Frobenius norms. Its vanishing forces $T^TAVBT=0$, hence $VAVBV=0$. The corresponding fourth-order mean identity forces the two vector restrictions. The coefficient of $st$ in the second-order mean identity supplies $\mu^TAVB\mu=0$.

## Qualification of the printed singular-case spectral step

The cumulant formula is valid for singular $V$, but the printed Equation 3 rewrites it using only nonzero eigenvalues of $C_0V$. This is not automatically valid in every singular noncentral case. The matrix $C_0V$ can have a nilpotent part at zero, and a quadratic form restricted to the affine Gaussian support can contain a nonzero linear Gaussian component even when its quadratic eigenvalues are all zero.

A concrete counterexample to that intermediate expansion is

$$
V=\begin{pmatrix}1&0\\0&0\end{pmatrix},\quad
\mu=\begin{pmatrix}0\\1\end{pmatrix},\quad
C_0=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$

Here $x=(Z,1)^T$ and $x^TC_0x=2Z$, with $Z\sim N(0,1)$. Its variance is 4. Yet $C_0V$ is nilpotent and has no nonzero eigenvalues, so the printed nonzero-eigenvalue sum would give zero for every cumulant. The original matrix cumulant formula correctly gives variance 4. This example concerns the proof step, not a counterexample to Craig's theorem.

One way to repair the bookkeeping is to work in the whitened representation and retain the deterministic and linear-Gaussian contributions explicitly. The zero-quadratic-eigenvalue linear component contributes only to cumulants of order at most two. Higher-order equations can still separate the nonzero spectral coefficients through a shifted confluent system; then the first two cumulant equations must be handled with the retained low-order terms. The article does not spell out this repair. A reader seeking a fully rigorous reproduction should supply it rather than applying Equation 3 unqualified to singular affine-support examples.

## A practical independence-checking procedure

Symmetrize numerical inputs if they represent symmetric quadratic forms, and verify that $V$ is positive semidefinite within a disclosed numerical tolerance. Exact mathematical independence is not a floating-point property; thresholding small eigenvalues changes the model's assumed rank.

Compute a thin eigendecomposition or another rank-revealing factor $T$ of $V$. Form $C,D,d,e$ as above and evaluate all four residuals. Use norm-scaled tolerances, reporting the matrix and vector residuals rather than a single unqualified Boolean. In the full-rank case, $AVB$ is a simpler equivalent check. A nearly singular estimate should not be treated as exactly singular without documenting the decision.

These calculations test independence **conditional on** the specified Gaussian law and parameter values. They do not estimate the law, provide finite-sample confidence intervals for estimated covariance, or validate joint normality. Replacing the covariance by a regularized risk estimate and declaring exact statistical independence would conflate an algebraic model implication with empirical evidence.

## Limits and applications

The paper has no dataset, simulation calibration, portfolio performance result, or test-power study. It supplies a theorem and proof strategy. Its relevance to quantitative research is through the dependence structure of Gaussian quadratic diagnostics and risk decompositions, especially when nonzero means or rank deficiency make the usual centered full-rank shortcut inappropriate.

Independence of two quadratic forms does not by itself imply that either is chi-square distributed. Chi-square distribution and Cochran's theorem require additional structure, such as appropriate projection or idempotence properties. The filename should therefore not lead a reproducing reader to apply a chi-square conclusion that this article's independence conditions alone do not establish.

The central actionable result is the four-condition criterion, with the thin-factor representation providing a transparent implementation. The source's intended elementary necessity argument is informative, but its treatment of zero eigenvalues needs the qualification above to cover the full singular noncentral setting as advertised.
