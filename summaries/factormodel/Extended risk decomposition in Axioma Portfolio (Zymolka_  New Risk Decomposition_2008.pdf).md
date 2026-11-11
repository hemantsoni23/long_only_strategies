# Extended risk decomposition in Axioma Portfolio

Axioma Inc., May 14, 2008, five-page methodology/product note. Source: [Zymolka_  New Risk Decomposition_2008.pdf](<../../Finance/Zymolka_  New Risk Decomposition_2008.pdf>). The supplied document names the company rather than an individual author. It includes the covariance decomposition, marginal-risk formulas, a software screenshot, and a notation appendix.

## Why this matters

Standalone factor volatilities cannot reveal whether an exposure hedges the rest of a portfolio. A factor can have substantial standalone risk while reducing total risk through negative covariance. This note adds an additive signed variance allocation to an existing presentation of nonnegative standalone risks and an unassigned covariance term.

The contribution is a software-oriented application of covariance allocation and Euler marginal-risk analysis. It does not estimate a new factor model or demonstrate improved investment performance. Its practical value is making diversifying exposures visible and distinguishing marginal contributions from isolated factor volatility.

## Model and original display

Let $w$ be asset weights, $B$ the factor-by-asset loading matrix, $f=Bw$ portfolio factor exposures, $Q$ factor covariance, and $\Lambda$ specific covariance. Under the model's zero factor-specific covariance assumption,

$
V=w'(B'QB+\Lambda)w=f'Qf+w'\Lambda w,
\qquad \sigma=\sqrt V.
$

The appendix describes diagonal $\Lambda$. Its entries must be specific **variances** for this equation to be dimensionally correct, even where the source loosely calls them specific risks. Weights and covariances must share a consistent decimal-versus-percent convention and return horizon.

Define factor volatility $\sigma_F=\sqrt{f'Qf}$ and specific volatility $\sigma_S=\sqrt{w'\Lambda w}$. Then $\sigma^2=\sigma_F^2+\sigma_S^2$, rather than $\sigma=\sigma_F+\sigma_S$.

The older factor display shows isolated risks $\sigma_i^{\rm stand}=|f_i|\sqrt{Q_{ii}}$ and a separate covariance amount

$
C=\sum_{i\ne j}f_if_jQ_{ij}=2\sum_{i<j}f_if_jQ_{ij}.
$

Thus $\sigma_F^2=\sum_i(\sigma_i^{\rm stand})^2+C$. The covariance amount is in variance units and may be negative. Adding it directly to standalone standard deviations would be incorrect. This display answers what each factor contributes in isolation, not what it contributes to the existing portfolio.

## Signed variance allocation

The proposed allocation is

$
V_i^F=f_i(Qf)_i=f_i^2Q_{ii}+\sum_{j\ne i}f_if_jQ_{ij}.
$

Summing over factors gives exactly $\sum_iV_i^F=f'Qf$. Each unordered pair's total covariance term $2f_if_jQ_{ij}$ is split equally between its two factors. This explains the source's phrase “half to each”: the full pair contribution has the factor two, while each assigned part does not.

A contribution can be negative without any negative variance in the underlying model. $V_i^F$ is an allocated portion of total variance, not the variance of a random variable by itself. The source's occasional wording “individual factor variance” should be understood in this allocated sense. Negative values identify local risk-reducing exposures under the chosen decomposition and covariance matrix.

Groups of factors can be handled by adding member contributions. An asset-level counterpart is $w_a(\Sigma w)_a$, with $\Sigma=B'QB+\Lambda$. Summing over any disjoint asset classification reconciles total variance. Mixing overlapping classifications without an allocation rule would double-count risk; the note's claim of arbitrary classifications does not remove this requirement.

## Marginal and component volatility

For $\sigma_F>0$,

$
\frac{\partial\sigma_F}{\partial f_i}=\frac{(Qf)_i}{\sigma_F},
\qquad V_i^F=f_i\sigma_F\frac{\partial\sigma_F}{\partial f_i}.
$

The signed factor **component volatility** is $f_i(Qf)_i/\sigma_F$ and sums to $\sigma_F$. If attributing total volatility instead, divide each factor variance contribution by $\sigma$, and assign $w'\Lambda w/\sigma$ to specific risk. These total-volatility contributions sum to $\sigma$. The denominator must match the total being decomposed.

A negative component says that scaling an existing exposure slightly toward zero raises risk locally, or scaling it further in its current direction lowers risk locally. A negative marginal derivative alone has a different interpretation if $f_i<0$. Finite removal also differs from an infinitesimal change: removing factor $i$ changes factor variance by $-2V_i^F+f_i^2Q_{ii}$. That independently derived identity avoids treating a signed allocation as the exact risk change from deleting an entire exposure.

At zero factor risk, the gradient expression divides by zero and is not available as written. A positive-semidefinite covariance can produce such a boundary, so a production implementation needs a declared convention rather than silently outputting infinite marginal risk.

## Reconstructible illustration

For an independent numerical illustration, take $f=(1,1)$ and

$
Q=\begin{pmatrix}1&-1.5\\-1.5&4\end{pmatrix}.
$

The matrix is positive definite, with determinant 1.75. Standalone factor volatilities are one and two; their covariance term is -3, yielding factor variance two and volatility $\sqrt2$. Signed allocations are $-0.5$ and $2.5$, adding to two. The first factor is diversifying despite its nonzero standalone volatility. Removing it raises variance from two to four. These figures are a mathematical check of the method, not values claimed in Axioma's screenshot.

The published screenshot reports total active standard deviation around 5% in the old display and a right-hand contribution-to-variance total of 0.25%. These are consistent when decimal variance is formatted as a percentage: $0.05^2=0.0025=0.25\%$. The text calls the latter “total active risk,” but it is a variance presentation, not 0.25% volatility. Its approximate split 0.1705% plus 0.0795% is likewise additive variance, not additive standard deviations.

The Size factor's reported -0.3718% is a share of variance in the screenshot's rightmost column, not a -0.3718 percentage-point standalone volatility. The source also gives a marginal-risk numerical example whose percent/unit conversion is not sufficiently clear to reconstruct from the rounded screenshot alone. The symbolic derivative is the reliable implementation guide; copying the displayed number without its exposure scaling can cause a large unit error.

## What the decomposition does not establish

Factor contributions depend on the factor basis. Rescaling one factor with the inverse exposure/covariance adjustment preserves the underlying model, while rotating or regrouping factors changes how covariance is allocated among named components. A contribution is not a unique causal allocation of realized market loss.

Covariances and exposures are estimates. A historically diversifying component can cease to hedge during a regime change, and a negative factor contribution says nothing about liquidity, expected returns, specific risk added by a feasible trade, transaction costs, or constraints. Holding all other factor exposures fixed may not be achievable by trading actual assets. The source explicitly cautions that its marginal-factor argument does not determine the accompanying specific-risk change.

To implement the method, obtain a symmetric positive-semidefinite covariance matrix, align exposures and weights, compute $f$, then calculate vector $f\odot(Qf)$ and the specific variance. Reconcile variance totals before formatting percentages or converting to volatility contributions. Report the denominator used for contribution percentages and the risk horizon. No empirical validation sample, covariance estimator, exposure fitting method, or backtest is supplied, because this document explains attribution rather than risk-model estimation.

The practical lesson is to report isolated risk and signed portfolio contribution as different quantities. The new allocation exposes hedging effects that isolated factor volatilities hide, while requiring careful units and a local interpretation of marginal-risk statements.
