# Stress testing correlation matrices for risk management

**Mike K. P. So, Jerry Wong, and Manabu Asai (2013).** *North American Journal of Economics and Finance* 26, 310–322. DOI: 10.1016/j.najef.2013.02.007. Source: [Stresstesting_SoWongAsai_2013.pdf](../../Finance/Stresstesting_SoWongAsai_2013.pdf). References below identify sections, equations, and tables of that source.

## Why this matters

Changing selected pairwise correlations can make an otherwise valid correlation matrix indefinite. Such a matrix cannot be the covariance structure of any joint random vector. A repair must therefore reconcile desired stressed entries with the remaining entries and with positive semidefiniteness. If downstream calculations require inversion or a nonsingular joint density, strict positive definiteness is additionally useful.

This paper proposes a restricted repair family with three features: group similar desired stressed correlations into blocks, replace each block by one optimized parameter, and shift the matrix's spectrum before normalizing its diagonal. A penalty controls the trade-off between matching the stressed entries and disturbing entries that were meant to remain unchanged. The contribution is a numerical construction, evaluated by matrix errors and computation times. It is not a model of how an economic crisis generates correlations, nor a backtest of portfolio VaR.

## Inputs, target, and comparator methods

Let $\Gamma$ be an original $p\times p$ correlation matrix. A scenario overwrites a selected set $\mathcal S$ of off-diagonal entries with desired values, symmetrically, producing $\Gamma^*$. The diagonal remains one. The resulting matrix can have a negative minimum eigenvalue even if all individual correlations remain between −1 and +1.

The task is to produce a valid $\widetilde\Gamma$ close to the scenario, with possibly different priorities for $\mathcal S$ and its complement. The article's “revised” group means entries deliberately changed by the scenario; “non-revised” entries are original targets that the repair may nevertheless alter.

The first comparator, attributed to Rebonato–Jäckel, decomposes $\Gamma^*=B\Lambda B'$ and clips negative eigenvalues to zero. Let $C=B\max(\Lambda,0)B'$ and $D=\operatorname{diag}(C)$. It returns $D^{-1/2}CD^{-1/2}$. Eigenvalue clipping is a nearest positive-semidefinite projection in Frobenius norm before the diagonal normalization; the subsequent normalization does not generally preserve a claim of global nearestness among all unit-diagonal PSD matrices. The output can be singular.

The second comparator, attributed to Turkay and coauthors, orders unchanged variables first, decomposes contributions associated with unchanged and affected blocks, and repairs the affected residual block spectrally while preserving the unchanged part. In the reported experiment it leaves non-revised correlations exact but substantially misses the revised targets. The paper describes a Cholesky-based implementation; it does not publish code clarifying all handling of indefinite residuals and numerical tolerances.

One qualification to the motivation is essential. The paper says an inverse correlation matrix is required for portfolio standard deviation and VaR. For a fixed portfolio under an ordinary linear covariance model, it is not: variance is $w'D_\sigma\Gamma D_\sigma w$, which is defined even when $\Gamma$ is singular. Positive definiteness matters for particular inverse-based optimizations, densities, and stable solves, rather than every risk calculation. Singular covariance matrices are not universally unusable.

## Blocking construction and positive-definiteness proof

Sort the desired off-diagonal correlations in $\mathcal S$ by value and divide them into $g$ approximately equal-sized blocks $\mathcal S_1,\ldots,\mathcal S_g$. Similar targets therefore share a block. Assign one unknown scalar $r_l$ to every entry in block $l$, preserve symmetry, and leave the other target correlations unchanged:

$$
R_{ii}=1,\qquad
R_{ij}=\begin{cases}r_l,&(i,j)\in\mathcal S_l,\\\Gamma^*_{ij},&(i,j)\notin\mathcal S.\end{cases}
$$

Here blocks are groups of **correlation values**, not necessarily contiguous submatrices of assets. Retain a map from each sorted target to its original pair of indices, and assign both symmetric entries the same value.

Let $\lambda_{\min}(R)$ be the smallest eigenvalue. For a positive tuning value $c$, equation 3 defines

$$
\delta(R,c)=\begin{cases}-\lambda_{\min}(R)+c,&\lambda_{\min}(R)\leq0,\\0,&\lambda_{\min}(R)>0.\end{cases}
$$

The repaired matrix is

$$
\widetilde\Gamma=\frac{R+\delta I}{1+\delta}.
$$

Its diagonal is exactly one. Since an identity shift preserves eigenvectors and shifts every eigenvalue, its eigenvalues are $(\lambda_j(R)+\delta)/(1+\delta)$. If $R$ is not positive definite, the smallest repaired eigenvalue is

$$
\lambda_{\min}(\widetilde\Gamma)=\frac{c}{1-\lambda_{\min}(R)+c}>0.
$$

If $R$ is already positive definite, the repair is simply $R$. Thus the construction is positive definite in exact arithmetic for every $c>0$. This proof also shows that a lower bound on $c$ is **not** an identical lower bound on the final eigenvalue. Large negative original eigenvalues can still produce small normalized minimum eigenvalues. Moreover, the $\lambda_{\min}>0$ branch applies no shift at all; a barely positive $R$ can remain poorly conditioned. The formula guarantees strict positivity, not uniformly excellent conditioning or immunity to finite-precision error.

For an unstressed off-diagonal entry the signed repair error is

$$
\widetilde\Gamma_{ij}-\Gamma^*_{ij}=-\frac{\delta}{1+\delta}\Gamma^*_{ij}.
$$

All such entries shrink toward zero by a common factor. Positive unstressed correlations decrease, while negative ones become less negative. They are not held exactly fixed unless $\delta=0$. For a stressed entry in block $l$, the error is $r_l/(1+\delta)-\Gamma^*_{ij}$.

## Objective and implementation details

The $g+1$ optimization variables are $r_1,\ldots,r_g,c$. Equation 4 minimizes

$$
J(r_1,\ldots,r_g,c)=\sum_{l=1}^{g}\sum_{(i,j)\in\mathcal S_l}\left(\frac{r_l}{1+\delta(R,c)}-\Gamma^*_{ij}\right)^2+\alpha\delta(R,c)^2.
$$

Only one triangular copy of each pair is needed in an implementation; the counting convention must be consistent with $\alpha$. The experiments constrain $c\geq0.1$ and use $\alpha=1$ in simulations, with $\alpha=1$ or 50 in the real-data illustration.

The first term fits stressed targets. The second encourages less shrinkage of non-revised entries. It is a **proxy** for their aggregate squared error, not their exact squared-error sum, which would contain $(\delta/(1+\delta))^2\sum_{\mathcal S^c}(\Gamma^*_{ij})^2$. Increasing $\alpha$ puts more weight on preserving unstressed correlations, generally at the cost of worse target matching in the stressed group.

The objective sums errors rather than averaging by group size. Consequently, the numerical meaning of a fixed $\alpha$ depends on the number of stressed pairs and the error-counting convention. A value selected for one dimension is not automatically an economically equivalent preference at another dimension.

A reconstruction can proceed by storing the target matrix and pair mask; sorting and blocking the targets; building symmetric $R$ for each trial parameter vector; calculating its smallest eigenvalue; computing $\delta$, the objective, and the repaired matrix; and checking symmetry, unit diagonal, minimum eigenvalue, and group errors at the final solution. The proof avoids a full eigenvalue modification, but each objective evaluation still requires a minimum-eigenvalue calculation. Reducing the parameter count does not make the matrix operations dimension-free.

The paper supplies no optimizer name, initialization, bounds on block parameters, derivative method, convergence tolerance, restart policy, random seed, software version, or hardware specification. It does not prove global optimality of the numerical solution. The eigenvalue-dependent objective can be nonsmooth at repeated eigenvalues, and the stated shift rule changes branches at zero. Implementations should document their numerical choices and verify the achieved objective and spectrum rather than assume a convex nearest-correlation solution.

The article notes possible application to evolving correlation models, but estimates no dynamic DCC model here. The repair operates on a supplied scenario matrix; it does not infer the scenario probability or its time evolution.

## Simulation design

Section 4 draws independent standard-normal entries in the lower triangle of a matrix $L$, including its diagonal, and forms

$$
\Gamma=D^{-1/2}L'LD^{-1/2},\qquad D=\operatorname{diag}(L'L).
$$

With nonzero Gaussian diagonal entries, $L$ is nonsingular almost surely and this construction is positive definite. It is not a uniform draw over correlation matrices and imposes a particular dependence structure; simulation conclusions are conditional on that design.

A randomly selected subset of $m$ variables has its $m(m-1)/2$ internal pair correlations changed to random targets between 0.6 and 1. Approximately 10% of all distinct off-diagonal pairs are stressed. The source does not explicitly name the random target distribution; a uniform draw is a natural implementation choice but must be disclosed as such. The tables imply $m=32,160,320$ for $p=100,500,1000$, yielding 496, 12,720, and 51,040 stressed pairs respectively.

There are 100 replications for each reported dimension, and $g=1,5,10$ for the proposed method. Evaluation uses mean absolute error and root mean squared error separately for stressed pairs, unstressed pairs, and all pairs, together with minimum eigenvalues and computation time. These are errors relative to the **desired scenario matrix**, not errors relative to a known true crisis correlation matrix. No Monte Carlo standard errors or distribution of runtimes is reported.

### Comparison at dimension 100

Table 1 compares the three methods with $g=1$ for blocking:

| Metric | Spectral clipping | Local repair | Blocking |
|---|---:|---:|---:|
| Reported computation time | 1 second | 240 seconds | 2 seconds |
| Minimum repaired eigenvalue | approximately 0 | approximately 0 | 0.0215 |
| Stressed-pair MAE | 0.2122 | 0.7027 | 0.1127 |
| Stressed-pair RMSE | 0.2265 | 0.7411 | 0.1358 |
| Unstressed-pair MAE | 0.0229 | 0 | 0.0758 |
| All-pair MAE | 0.0419 | 0.0704 | 0.0795 |
| All-pair RMSE | 0.0788 | 0.2346 | 0.1005 |

The average target minimum eigenvalue is −1.8407. Blocking fits the stressed group best and yields a positive eigenvalue buffer, but has the **largest all-pair MAE** among these three outputs. Spectral clipping has the best total MAE and RMSE. Therefore the result is a trade-off between targeted fidelity, validity requirements, and disturbance elsewhere, not unconditional dominance in overall approximation.

### More blocks and larger matrices

At $p=100$, increasing $g$ from 1 to 5 to 10 reduces stressed MAE from 0.1127 to 0.1095 to 0.1084; unstressed MAE is 0.0758, 0.0755, 0.0750. Reported runtime remains two seconds. Gains are present but modest.

At $p=500$, times are 20 seconds, 2.5 minutes, and 4 minutes. Stressed MAE is 0.1002, 0.0964, 0.0964; unstressed MAE is 0.0367, 0.0372, 0.0370. The minimum repaired eigenvalue is around 0.014–0.016. Increasing the number of blocks does not monotonically improve the unstressed group.

At $p=1000$, times are 3, 15, and 35 minutes. Stressed MAE is 0.1000, 0.0975, 0.0965; unstressed MAE is 0.0262, 0.0272, 0.0268. All-pair MAE is 0.0338, 0.0343, 0.0339, so more blocks do not monotonically improve total MAE either. Minimum eigenvalues are 0.0145, 0.0115, and 0.0128. The source presents $g=5$ as a practical compromise, but the unreported hardware and solver prevent treating its runtimes as portable guarantees.

The lower average unstressed error at larger dimensions in this simulation does not prove a general theorem that the algorithm becomes more reliable with dimension. It is a property of these generated matrices and scenarios.

## Hong Kong illustration

Section 5 uses Bloomberg daily prices for 1,188 Hong Kong stocks, January 2009–December 2011, with 743 observations per return series. The authors avoid late 2008 to study a more recent, less abruptly changing correlation structure. This is a scenario illustration using historical estimates, not a replay showing that the method forecast the 2008 crisis.

Nineteen subsector counts in Table 5 sum to 1,188. A later sentence says 1,128; the table and repeated stated dimensions support 1,188. With more assets than observations, the ordinary sample correlation matrix is necessarily singular: its rank cannot exceed 742 after demeaning. This reinforces the need to distinguish a PSD empirical input from the strictly positive-definite output.

The selected stressed set contains 367 stocks from banks (11), financial services (94), insurance (6), real estate (140), retail (53), and travel/leisure (63). Their 67,161 distinct internal pairs are approximately 9.53% of all 705,078 pairs, close to the text's 9.51%. It is the **pair share**, not 367 divided by the number of stocks.

Random scenario targets lie in four intervals: [0.3,0.5], [0.5,0.7], [0.7,0.9], and [0.5,0.9]. The first three are interpreted as successively stronger co-movement scenarios; the last tests a wider range. The original matrix reportedly has only 6.36% of correlations above 0.3 and 0.60% above 0.5. Exact stock identifiers, corporate-action adjustments, missing-data treatment, and scenario random seeds are absent.

Selected $g=5$ results from Tables 6–9 are:

| Target interval | Target minimum eigenvalue | Stressed MAE, $\alpha=1$ / 50 | Unstressed MAE, $\alpha=1$ / 50 | All-pair MAE, $\alpha=1$ / 50 |
|---|---:|---|---|---|
| 0.3–0.5 | −18.0737 | 0.0464 / 0.1989 | 0.1127 / 0.1113 | 0.1063 / 0.1197 |
| 0.5–0.7 | −16.6344 | 0.0515 / 0.3037 | 0.1139 / 0.1119 | 0.1080 / 0.1302 |
| 0.7–0.9 | −16.0444 | 0.0754 / 0.4247 | 0.1151 / 0.1125 | 0.1113 / 0.1422 |
| 0.5–0.9 | −16.4088 | 0.1033 / 0.3620 | 0.1146 / 0.1122 | 0.1135 / 0.1360 |

Increasing $\alpha$ buys only a small reduction in unstressed error while greatly worsening stressed-target fidelity in these cases. For the 0.7–0.9 scenario, stressed MAE rises from about 0.075 to 0.425: the output can be valid yet economically far from the requested stress. There is no basis for calling every such error acceptable independently of the portfolio and decision.

The repaired minimum eigenvalues at $g=5,\alpha=1$ are 0.0045, 0.0034, 0.0024, and 0.0028 respectively, smaller than in the synthetic examples. Figures 2–3 show broadly similar error distributions across $g=1,5,10$, and average downward errors in stressed correlations. Larger block counts offer limited benefit here relative to their computational cost. The figures' term “relative error” should not be confused automatically with a percentage error: the explicit tabulated MAE/RMSE definitions concern differences in correlation units.

## Interpretation and limits

The method gives an implementable way to fit selected stress targets while ensuring a legitimate nonsingular correlation matrix, with a transparent algebraic validity proof. It does not preserve non-revised entries exactly, enforce the stressed values as hard constraints, or solve the unrestricted nearest-correlation problem. Numerical fitting and economic stress design remain separate decisions.

No portfolio weights, marginal volatilities, return distribution, loss horizon, VaR confidence level, realized crisis losses, or capital comparison is supplied. Correlation increases do not universally increase risk for arbitrary long–short portfolios; the effect depends on exposures and volatilities. The paper's matrix errors cannot be translated into a universal error in portfolio loss or VaR without those inputs.

For use in quantitative research, preserve both the requested and achieved scenario matrices, report errors by group and important asset pairs, and inspect the spectrum and condition number. Those are consequences of the method's trade-off, not additional validations claimed in the article. Exact numerical replication requires disclosure of the original random generators and optimizer configuration; financial validation additionally requires an economically specified scenario and portfolio. The source demonstrates numerical feasibility under its experiments, rather than establishing the probability or sufficiency of a proposed crisis scenario.
