# A short proof of the Marchenko–Pastur theorem

Pavel Yaskov, *Comptes Rendus Mathématique* 354 (2016), 319–322. DOI: 10.1016/j.crma.2015.12.008. Source: [MarcenkoPastur_Yaskov_2016.pdf](../../Finance/MarcenkoPastur_Yaskov_2016.pdf), four pages, including both proofs and references.

## Why this matters

The Marchenko–Pastur law describes the bulk eigenvalue distribution of a high-dimensional sample covariance matrix under an identity-like population structure. It underlies many distinctions between sampling noise and economically meaningful covariance structure. This short paper broadens the dependence allowed within an observation vector while weakening a familiar quadratic-form variance condition to convergence in probability.

The innovative step is a resolvent proof that needs concentration of normalized quadratic forms, rather than a vanishing variance for every such form. A second result shows that, for independent centered unit-variance coordinates, this condition is exactly equivalent to a Lindeberg tail condition. The paper is a mathematical limit theorem, not a covariance-cleaning algorithm, a finite-sample factor-significance test, or an empirical finance study.

## Matrix construction and the limiting law

For each pair of dimensions, let $X_{pn}$ be a $p\times n$ matrix whose columns are independent identically distributed copies of a real random vector $x_p$. The dimension-to-sample ratio satisfies $p/n\to c\in(0,\infty)$. The matrix of interest is

$$
C_{pn}=\frac1nX_{pn}X_{pn}^\top.
$$

Its empirical spectral distribution gives mass $1/p$ to each of its $p$ eigenvalues, counting multiplicity. It is an uncentered sample second-moment matrix as displayed; replacing it by a demeaned or standardized correlation matrix is an additional operation.

The limiting distribution is

$$
\mu_c=(1-1/c)^+\delta_0+
\frac{\sqrt{(b-x)(x-a)}}{2\pi cx}\,1_{[a,b]}(x)\,dx,
$$

where $a=(1-\sqrt c)^2$ and $b=(1+\sqrt c)^2$. If $c>1$, the atom at zero reflects the rank deficit when there are more coordinates than observations. The theorem states almost-sure weak convergence of the empirical spectral distribution to this law.

For a finance-oriented implementation, columns would naturally represent independent observations and rows assets or features. The column independence assumption is substantial: arbitrary time-series dependence is not permitted merely because within-column dependence is allowed. Nor does an arbitrary nonidentity population covariance have the displayed identity-population MP limit.

## The central assumption

Assumption (A) requires that for every sequence of deterministic complex $p\times p$ matrices $A_p$ with uniformly bounded spectral norm,

$$
\frac{x_p^\top A_px_p-\operatorname{tr}A_p}{p}\xrightarrow{P}0.
$$

It is a weak law for quadratic forms, normalized by dimension. The trace is the identity-population reference. If coordinates are centered and orthonormal, then $E[x_p^\top A_px_p]=\operatorname{tr}A_p$, but the theorem directly assumes the displayed probability convergence rather than separately requiring a variance estimate.

A preceding line of results assumes that the variance of $x_p^\top A_px_p/p$ tends to zero. Under the appropriate centering, that implies (A), while convergence in probability can hold without the stronger moment convergence. This distinction accommodates heavier tails and more general within-vector dependence. The paper also notes that testing (A) on real symmetric positive-semidefinite matrices is equivalent to its complex-matrix formulation, by decomposition and linearity.

Taking $A_p=I$ shows that normalized squared length must concentrate near one. This alone is weaker than the full condition: concentration is needed in every uniformly bounded quadratic direction, not just in total length. An example class mentioned in Section 2 consists of orthonormal infinite linear combinations, in $L^2$, of independent centered unit-variance innovations. Verifying the associated concentration conditions for that class is referred to other work; the four-page note does not prove that application in detail.

## Independent-coordinate equivalence

Proposition 2.1 assumes independent coordinates $X_{pk}$ with $EX_{pk}=0$ and $EX_{pk}^2=1$. It states that (A) is equivalent to

$$
\frac1p\sum_{k=1}^{p}E[X_{pk}^2,1_{\{|X_{pk}|>\varepsilon\sqrt p\}}]\longrightarrow0
\quad\text{for every }\varepsilon>0.
$$

This is a triangular-array Lindeberg condition. It limits how much of the average second moment can be carried by observations on the dimension-dependent $\sqrt p$ scale. A uniform fourth-moment bound is sufficient for many familiar arguments but is not imposed here.

The proof splits $A_p$ into its diagonal part $D_p$ and off-diagonal remainder. Independence and centering control the off-diagonal second moment by a multiple of $\operatorname{tr}(A_pA_p^*)=O(p)$. After division by $p^2$, this contribution vanishes. Thus the remaining task is a weak law for weighted sums $p^{-1}\sum_k a_k^{(p)}(X_{pk}^2-1)$ with bounded deterministic weights.

For necessity, applying the condition to equal diagonal weights gives $Z_p=p^{-1}\sum_kX_{pk}^2\to1$ in probability. Positivity and $EZ_p=1$, with a subsequence/Sheffé argument, yield $L^1$ convergence. The proof then invokes a result on independent sums to obtain the appropriate tail condition. For sufficiency, the Marcinkiewicz–Zygmund inequality reduces the expected absolute weighted sum to a square-root sum of centered squared-coordinate terms. Truncating at size $\varepsilon p$ controls the small terms, while the Lindeberg condition controls the large terms. Letting $\varepsilon$ decrease to zero proves the required convergence.

The equivalence uses independent coordinates. It must not be extended to arbitrary dependent coordinates merely because Theorem 2.1 permits dependence under (A).

## Resolvent proof of the spectral limit

For $z$ in the upper half-plane, with $v=\operatorname{Im}z>0$, define the Stieltjes transform using the convention

$$
s_n(z)=\frac1p\operatorname{tr}(C_{pn}-zI)^{-1}.
$$

This convention has positive imaginary part. Changing the resolvent to $(zI-C)^{-1}$ reverses signs and changes the equations. A standard martingale concentration argument first gives $s_n(z)-Es_n(z)\to0$ almost surely. The remaining task is to identify the limit of its expectation.

Set $A_n=X_{pn}X_{pn}^\top$ and add an independent extra column $x_p$, forming $B_n=A_n+x_px_p^\top$. Write

$$
S_n(z)=\operatorname{tr}(A_n-nzI)^{-1}=\frac pn s_n(z).
$$

Exchangeability of the $n+1$ columns and the trace of the identity imply

$$
p=(n+1)E[x_p^\top(B_n-nzI)^{-1}x_p]-nzE\operatorname{tr}(B_n-nzI)^{-1}.
$$

The Sherman–Morrison identity expresses the quadratic form in the rank-one-updated inverse as $u/(1+u)$, where $u=x_p^\top(A_n-nzI)^{-1}x_p$. Assumption (A), applied conditionally to a resolvent independent of $x_p$, makes $u-S_n(z)$ converge to zero in probability. The uniform norm bound on the appropriately scaled resolvent is supplied by $v>0$.

Lemma 3.1 provides the necessary stability controls: resolvent norm at most $1/v$ after the corresponding scaling, a rank-one trace difference bound, a bounded updated quadratic form, and imaginary-part bounds keeping $1+u$ away from a dangerous denominator. These bounds justify converting convergence in probability of the quadratic-form difference into convergence of expectations of the bounded resolvent expressions. A direct unbounded quadratic-form expectation substitution would require stronger moment assumptions and would lose the paper's advantage.

The resulting self-consistency equation is

$$
\frac{ES_n(z)}{1+ES_n(z)}-zES_n(z)=c+o(1).
$$

Every limiting point therefore solves

$$
zS^2+(z-1+c)S+c=0.
$$

The upper-half-plane branch is unique and equals $S=cs(z)$ for the MP transform. Equivalently,

$$
czs(z)^2+(z-1+c)s(z)+1=0.
$$

The correct branch has positive imaginary part and $s(z)\sim-1/z$ at large imaginary argument. Those criteria are essential in a numerical implementation; a quadratic formula without branch selection can produce the wrong transform. Martingale concentration then transfers the deterministic expectation limit to almost-sure transform convergence, and Stieltjes continuity identifies weak convergence of the empirical spectral distributions.

## Reimplementation and boundaries

There are no empirical data, hyperparameters, portfolio rules, or numerical experiments in this source. A computational illustration would be additional work. To check the theorem numerically, one would generate independent columns satisfying a declared instance of (A), form $XX^\top/n$, compute all eigenvalues, and compare the entire empirical distribution with the density and zero atom for the actual ratio $p/n$. Such a simulation illustrates an asymptotic theorem; it cannot establish assumption (A) for arbitrary market data.

The theorem concerns the bulk empirical distribution. Weak convergence does not by itself prove convergence of the largest eigenvalue to $b$, validate a finite-sample upper-edge significance threshold, describe eigenvectors, or identify the economic meaning of outliers. A vanishing fraction of extreme eigenvalues can be invisible to the empirical-distribution limit. Dependence across observation columns, nonstationarity, a nonidentity population covariance, missing-data estimators, and heavy tails that violate quadratic-form concentration require separate analysis.

For covariance research, the practical value is a precise assumption checklist. Independence inside each observation vector is not always necessary, and fourth-moment variance calculations can be stronger than needed. What replaces them is not unrestricted dependence, but dimension-normalized concentration of every bounded quadratic form. The short resolvent argument shows exactly where that property enters and why it is sufficient for the MP bulk law.
