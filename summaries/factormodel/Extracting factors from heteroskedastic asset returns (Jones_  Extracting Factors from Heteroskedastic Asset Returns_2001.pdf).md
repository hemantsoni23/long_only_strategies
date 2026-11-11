# Extracting factors from heteroskedastic asset returns

Christopher S. Jones. *Journal of Financial Economics* 62 (2001), 293–325.

Source: [complete 33-page PDF](../../Finance/Jones_%20%20Extracting%20Factors%20from%20Heteroskedastic%20Asset%20Returns_2001.pdf). Page references below use the printed journal pagination. The source contains the theory, algorithms, all simulation and empirical tables, nine figures, and references.

## Why this matters and the specific contribution

Large-cross-section principal components can estimate common return factors accurately when the average idiosyncratic variance is constant through time. That qualification is easy to miss. Individual securities may be heteroskedastic without breaking the estimator if their volatility fluctuations average out. But if idiosyncratic volatility rises across much of the universe in the same month, the time cross-product matrix contains a changing diagonal component. Ordinary principal components can then mistake a high-volatility date for a common return factor.

Jones adapts a classical factor-analysis algorithm to remove this time-varying diagonal contribution before identifying the low-rank common component. The heteroskedastic factor analysis estimator, HFA, works on a matrix indexed by dates, not the conventional covariance matrix indexed by stocks. It remains computationally manageable when the number of stocks greatly exceeds the number of observations. The closest benchmark is the asymptotic principal-components estimator of Connor and Korajczyk, denoted CK in the paper.

The empirical importance is unusually concrete. For 1989–1993, the source reports that a single CK factor explains only 8.2% of value-weighted market return variation, versus 57.3% for the HFA factor. That is a difference in the estimated common factor span, not a small standard-error correction. HFA also produces much more stable factors when the security cross-section is randomly split. The gains are strongest in samples with pronounced common idiosyncratic volatility and in an unbalanced panel that includes securities with missing observations.

The novelty should be stated narrowly. The numerical factor-analysis machinery comes from earlier statistical work, and the paper acknowledges related unpublished work by Louis Scott. Its contribution is the large-cross-section return-model argument, the heteroskedastic extraction procedure in that setting, and the simulation and asset-pricing evidence. It is not a new economic theory identifying what the latent factors mean.

## Return model and the source of PCA inconsistency

Let $R$ be the $N\times T$ matrix of excess returns, with a stock in each row and a date in each column. The underlying model is

$$
r_t^{(N)}=B^{(N)}h_t+e_t^{(N)}.
$$

The loading matrix $B^{(N)}$ is $N\times K$ and constant within the estimation sample. The $K$-vector $h_t$ contains factor realizations, including their potentially time-varying expected premia. In the maintained exact-pricing formulation there is no separate unrestricted asset-specific intercept. Idiosyncratic returns have zero mean conditional on factors and are serially uncorrelated. Weak cross-sectional dependence is allowed, subject to conditions that make the cross-sectional averages converge.

Assume

$$
N^{-1}B^{(N)\prime}B^{(N)}\longrightarrow M\succ0.
$$

The normalization identifies a factor space, not a unique economic factor basis. If $H$ is the $K\times T$ matrix of factor realizations, the time cross-product converges, for fixed $T$, to

$$
C=\frac1N R'R\longrightarrow H'MH+D=F'F+D,
\qquad F=M^{1/2}H.
$$

Here $D=\operatorname{diag}(d_1,\ldots,d_T)$, where $d_t$ is the limiting cross-sectional average idiosyncratic variance at date $t$. Off-diagonal idiosyncratic terms disappear because idiosyncratic returns are serially uncorrelated; common-factor/error cross-products disappear by the maintained orthogonality and cross-sectional law of large numbers. An unrestricted time covariance matrix for idiosyncratic errors would not reduce to this diagonal problem.

If $D=dI_T$, adding it shifts all eigenvalues equally and leaves the eigenvectors of $F'F$ unchanged. The leading CK eigenvectors can then recover the factor span. If $D$ has unequal diagonal entries, its contribution changes eigenvectors as well as eigenvalues. A date with unusually large $d_t$ can dominate a principal component even though it contains no additional common-factor realization. Increasing $N$ estimates this contaminated limit more precisely; it does not remove the inconsistency.

This distinction also explains why missing observations matter. Even when each security has constant idiosyncratic variance, the average variance of securities observed at a particular date can vary as the sample composition changes. A large unbalanced panel can therefore create precisely the diagonal heterogeneity that CK cannot remove. More observations are useful only if the estimator accommodates the resulting composition effect.

The assumptions do not permit arbitrary dependence. Strong residual cross-sectional dependence can itself constitute an omitted pervasive factor. Serially correlated idiosyncratic returns create off-diagonal contamination. Changing loadings violate the fixed-$B$ decomposition. HFA corrects a specific heteroskedasticity problem; it does not solve all forms of latent-factor misspecification.

## HFA algorithm with consistent matrix dimensions

Section 2.1 gives an iterative factor-analysis construction. The following orientation is used throughout this note: $G=F'$ is $T\times K$, so the fitted common time covariance is $GG'$. The input is the uncentered cross-product of excess returns. Removing each stock's sample mean at this stage would change a model in which factor means carry expected returns.

For a specified $K$:

1. Form $C=R'R/N$ and initialize $D^{(0)}=\tfrac12\operatorname{diag}(C)$.
2. At iteration $a$, whiten the time cross-product as $S^{(a)}=(D^{(a)})^{-1/2}C(D^{(a)})^{-1/2}$.
3. Obtain the leading $K$ orthonormal eigenvectors $V_K$ and their diagonal eigenvalue matrix $\Lambda_K$.
4. Set $G^{(a+1)}=(D^{(a)})^{1/2}V_K(\Lambda_K-I_K)^{1/2}$.
5. Update $D^{(a+1)}=\operatorname{diag}(C-G^{(a+1)}G^{(a+1)\prime})$ and repeat.

The square root in step 4 requires the selected eigenvalues to be at least one. Step 5 must leave positive diagonal entries for the next whitening step. Negative uniqueness estimates are the familiar factor-analysis boundary problem. The source notes that problematic negative estimates did not occur in its reported applications; it does not supply a universally valid clipping or constrained-optimization rule. Adding one is a methodological extension and must be documented.

**Dimensional correction to the source:** its notation for the estimated factor matrix switches orientation, and the product printed in the diagonal update is inconsistent with the displayed $T\times K$ construction. With the orientation above the residual matrix is necessarily $C-GG'$, not $C-G'G$. This is an algebraic correction, not a change to the intended method.

The algorithm is borrowed from Gaussian factor analysis, but the consistency argument is based on the return cross-product limit. It is not a claim that the full $N\times T$ return panel has a correctly specified multivariate Gaussian likelihood. Conversely, the existence of that limit does not by itself establish global convergence of every iterative initialization or identification of every low-rank-plus-diagonal decomposition. Identification of the factor space, a valid positive diagonal solution, and convergence to the appropriate solution remain necessary qualifications.

For reporting and comparison, the extracted factor series are orthogonalized by Gram–Schmidt without an intercept. Normalize the first column; regress each subsequent column on its predecessors without a constant; normalize the residual. A thin QR decomposition implements the same span-preserving operation. Factor means are not subtracted. Signs are arbitrary, and factor-by-factor labels should not be interpreted economically without a separate identification scheme.

Unlike ordinary PCA, HFA factors estimated for $K$ and $K+1$ are not automatically nested: the diagonal $D$ is reestimated when $K$ changes. Run the full iteration separately for each requested dimension. The paper examines several dimensions, often one through twelve, but supplies no new automatic criterion for choosing $K$.

The computational advantage comes from reducing the problem to $T\times T$. Forming $C$ costs approximately $O(NT^2)$, after which each iteration involves a time-matrix eigendecomposition. An implementation should avoid constructing an $N\times N$ dense covariance matrix merely to reproduce this estimator.

## Missing-observation extension

Let $R_m$ replace unobserved returns by zero for the purpose of computing a numerator, and let $I$ be the corresponding $N\times T$ observation indicator. The pairwise time cross-product is

$$
C_{st}=\frac{(R_m'R_m)_{st}}{(I'I)_{st}}.
$$

The denominator is the number of securities observed at both dates. Zero filling therefore does not mean treating a missing observation as a genuine zero return. Dividing by $N$ after zero filling would implement a different estimator.

Each date pair must have a positive and sufficiently large overlap. The asymptotic argument also requires the relevant cross-sectional averages over those overlaps to converge to compatible loading and residual moments. A pattern of missingness that selectively changes the common loading distribution can change the target matrix, not merely its diagonal. Pairwise estimated matrices need not be positive semidefinite in finite samples; the source does not prescribe a nearest-positive-definite repair. Any such repair, overlap threshold, or missingness screen should be reported as an additional implementation choice.

This extension allows the author to compare a small panel of long-lived stocks with a much larger panel containing entrants and exits. The empirical benefit is not evidence that all missingness is ignorable. It shows that the proposed construction can use substantially more available return data in the particular sample.

## Data, universes, and descriptive volatility evidence

The data are CRSP monthly NYSE, AMEX, and Nasdaq returns over 1979–1998, analyzed as excess returns. Four separate five-year panels require complete returns over their respective 60 months. A 20-year balanced panel requires all 240 months; a second 20-year panel includes firms with missing observations.

| Sample | Total firms | NYSE | AMEX | Nasdaq |
|---|---:|---:|---:|---:|
| 1979–1983 | 3,340 | 1,647 | 524 | 1,169 |
| 1984–1988 | 3,619 | 1,510 | 445 | 1,664 |
| 1989–1993 | 4,364 | 1,765 | 531 | 2,068 |
| 1994–1998 | 4,792 | 2,026 | 472 | 2,294 |
| 1979–1998, balanced | 1,281 | 889 | 124 | 268 |
| 1979–1998, missing observations allowed | 19,144 | 4,736 | 2,101 | 12,307 |

The unbalanced long panel contains approximately five times as many return observations as the balanced panel. Its 19,144 firms are not all observed simultaneously. The balanced 20-year universe disproportionately contains long-lived large companies, so differences between the two long panels combine information gains with a change in economic composition.

Table 1 measures variation and persistence in $\sqrt{d_t}$. With one factor, the reported standard deviations across dates are 1.88, 1.90, 5.20, and 2.66 in the four five-year blocks, versus 1.79 in the balanced long panel and 3.87 in the unbalanced long panel. The table does not explicitly label the numerical return unit, so these numbers are best retained on its stated return scale rather than converted into annualized volatility. The unusually large 1989–1993 value is the key comparison. Across models and samples the autocorrelation of $\sqrt{d_t}$ is generally about 0.21–0.50, indicating persistent variation rather than isolated independent variance noise.

Exact share-code filters, delisting-return conventions, data vintage, and all missing-observation screens are not enumerated sufficiently to reconstruct the historical stock lists from a current database. The paper is also not a forecast exercise: the factor span is estimated using the whole sample under evaluation. There is no rolling training window, trade implementation lag, turnover constraint, or transaction-cost model.

## Simulation: identification accuracy and iteration choice

The simulations calibrate returns to the empirical panels under two designs. CK estimates provide homoskedastic calibrations; HFA estimates provide heteroskedastic calibrations. Estimated factor-date rows are resampled, and estimated loading rows are resampled across stocks. Firm-specific unconditional residual variances are retained with their loading rows. In the heteroskedastic design, the factor realization and its associated common variance state are resampled together, preserving their empirical contemporaneous association.

A useful implementation representation is

$$
R_{it}^{*}=b_i^{*\prime}f_t^*+
\sqrt{\omega_i^*}\,z_{it}\sqrt{d_t^*/\bar d},
\qquad z_{it}\sim N(0,1),
$$

with the final multiplier omitted in the homoskedastic design. This expresses the source's matched resampling and variance scaling; the exact normalization must agree with the calibrated factor and loading matrices. All simulated pricing intercepts are zero. Conditional errors are independent across stocks and dates, so these simulations are more restrictive than the weak cross-sectional dependence allowed by the theoretical argument. They do not test every admissible approximate-factor error structure.

The source uses 5,000 replications. It evaluates $K=1,3,6,12$; an isolated prose reference to “two” factors should not override the tables' explicit three-factor columns. Estimated factors are compared with the true factor span by regressing each true factor on all estimated factors plus a constant. Average and minimum $R^2$ values summarize recovery. This permits rotations and permutations of the estimated factors. The minimum across a particular true-factor basis is not itself a canonical-correlation invariant under arbitrary rotations of that true basis, although exact span recovery is invariant.

A convergence experiment calibrated to 1994–1998 compares 1, 3, 5, 10, 25, and 100 HFA iterations. For twelve factors, mean recovery $R^2$ rises from 0.963 after one iteration to 0.974 after five and 0.975 after 100; minimum recovery rises from 0.892 to 0.934 and 0.937. Simulation standard errors of the mean statistics are below 0.001. The remaining reported analyses use five iterations. This is an empirical computational compromise, not a universal tolerance guarantee.

Under heteroskedastic calibration the differences can be large. For 1989–1993 with six factors, Table 3 reports mean recovery $R^2$ of 0.751 for CK and 0.959 for HFA, with minimum values 0.480 and 0.918. With three factors, means are 0.691 and 0.838 and minima 0.469 and 0.719. The larger gains in the most heteroskedastic block fit the proposed mechanism.

The authors also resample entire calendar years instead of isolated months. Factor and variance observations are drawn jointly in 12-month blocks, preserving within-year persistence; five or twenty years are drawn as appropriate. Under the 1989–1993 six-factor calibration, block-bootstrap mean recovery is 0.644 for CK versus 0.968 for HFA, and minimum recovery is 0.181 versus 0.921. Persistence can therefore aggravate ordinary PCA's problem.

HFA is not uniformly better in every finite sample. Under homoskedastic calibration its performance is usually close to CK, but the 1989–1993 one-factor case has mean recovery of about 0.641 for HFA versus 0.766 for CK. Estimating a flexible diagonal can cost precision when it is unnecessary. Both methods are less impressive for weak higher-order factors in the small balanced long panel: for twelve factors, heteroskedastic mean recovery is about 0.833 for CK and 0.871 for HFA. More flexibility cannot replace adequate cross-sectional information.

## Empirical stability and economic benchmark regressions

The real-data stability exercise repeatedly divides the security universe randomly into equal halves, estimates factors independently in each half over the same calendar dates, and regresses the factors from one half on the complete factor span from the other. It performs 5,000 splits for each sample. This is cross-sectional validation, not prediction of future dates. With missing data, equal numbers of firms need not imply equal numbers of observed returns.

Figures 1–3 report mean and minimum cross-half $R^2$. For 1979–1983 with four factors, the plotted mean is roughly 0.65 for CK and 0.85 for HFA, while minimum recovery is below 0.2 for CK and near 0.7 for HFA. These are approximate readings of curves, not table-precision estimates. Above that dimension, some HFA higher-order factors also become unstable. In 1989–1993 even the first CK factor is poorly reproduced across halves, whereas the HFA first factor is much more stable. The unbalanced long panel shows larger HFA gains than the balanced long panel.

A second empirical exercise regresses six benchmark returns on one through twelve estimated factors: value-weighted and equally weighted stock-market returns, Fama–French SMB and HML, Carhart momentum, and a CRSP 30-year fixed-term bond return. Figures 4–9 display adjusted $R^2$ values. With an intercept and $K$ factors, the usual adjustment is

$$
\bar R^2=1-(1-R^2)\frac{T-1}{T-K-1}.
$$

The source's headline 1989–1993 single-factor market figures are 8.2% for CK and 57.3% for HFA; the surrounding empirical figures use adjusted fit measures. They should not be mixed with raw $R^2$ in a numerical replication. HFA's first factor also explains nearly all equally weighted market variation in that sample, while the first CK factor explains less than 60%.

The gains are not identical across benchmarks. Momentum benefits particularly in some subsamples, including 1984–1988. Enlarging the long panel to include missing observations helps some benchmarks more than others; it can improve momentum and equally weighted fit while reducing value-weighted or bond fit. That pattern is consistent with a changed cross-sectional weighting of economic exposures. It does not prove that one estimated factor set dominates for every investment objective.

## Asset-pricing tests and formula qualifications

Section 4.3 tests whether the estimated statistical factors price three return series: the value-weighted market excess return, SMB, and HML. SMB and HML are already return spreads; subtracting the risk-free rate again would be erroneous. Momentum is excluded from these pricing tests because its high turnover complicates the frictionless interpretation.

Let $Y$ be the $T\times m$ matrix of test returns, here $m=3$, and let $X=[\mathbf1,Q]$ contain the constant and the $K$ extracted factors. Fit $Y=XA+E$ by OLS and denote the vector of intercepts by $\hat\alpha$. Let $c=[(X'X)^{-1}]_{11}$. Under the conventional conditional-normal homoskedastic regression assumptions, a consistent GRS expression written directly in terms of residual sums of products is

$$
F_{GRS}=\frac{T-m-K}{m c}\hat\alpha'(E'E)^{-1}\hat\alpha
\sim F_{m,T-m-K}.
$$

If the residual covariance is defined as $\hat\Sigma_u=E'E/(T-K-1)$, the coefficient becomes $(T-m-K)/[m c(T-K-1)]$. **Source normalization issue:** equation (14) uses a denominator involving $T-1$ while describing its covariance estimator as the standard unbiased regression covariance. Those conventions are not simultaneously correct when $K>0$. The $T-1$ version would correspond to $E'E/(T-1)$ instead. Table headings also abbreviate the denominator degrees of freedom inconsistently. The formula above states an internally consistent reconstruction; the published test values below are reported values, not values regenerated from unavailable residuals.

The paper also uses a heteroskedasticity-robust MacKinlay–Richardson Wald test. In column-vectorized coefficient order define

$$
J=I_m\otimes(X'X/T),
\qquad
L=\frac1T\sum_{t=1}^{T}(e_te_t'\otimes x_tx_t'),
\qquad
V=J^{-1}LJ^{-1}.
$$

With the constant in the first column, the intercept selector is $S=I_m\otimes(1,0,\ldots,0)$. The statistic is

$$
W=T\hat\alpha'[SVS']^{-1}\hat\alpha
\overset{a}{\sim}\chi_m^2.
$$

This writes the covariance of the scaled coefficient estimator; division by $T$ is already handled by the leading $T$ in the statistic. The source's displayed selector is inconsistent with the stated column ordering and dimensions; the selector above makes that ordering explicit. A direct sandwich implementation also avoids unnecessarily inverting $L$, which may be singular even when the selected covariance is estimable. This is a contemporaneous heteroskedasticity correction, not a general serial-correlation HAC correction.

Generated factors are treated as sufficiently accurately estimated in the large cross-section. The tests do not supply a finite-$N$ correction for every source of factor-estimation uncertainty. Strong factor-span recovery is relevant evidence, but it is not itself a proof that all finite-sample pricing-test distributions are exact.

In 1989–1993 with one factor, Table 4 reports a GRS value of 1.244 with probability 0.303 for CK and 3.954 with probability 0.013 for HFA. The robust Wald values are 3.628, probability 0.305, and 11.770, probability 0.008. Better factor extraction can therefore strengthen a rejection rather than make a model appear to price better.

For 1994–1998 with three factors, GRS gives 3.247, probability 0.029, for CK versus 2.370, probability 0.081, for HFA. The robust probabilities are 0.012 and 0.043, so both still reject at 5% under that test. Reporting only the homoskedastic comparison would overstate the inferential reversal. The long 20-year samples reject strongly under both extraction methods.

Table 5 helps separate changes in alphas from changes in residual precision. For the 1989–1993 single-factor model, the value-weighted alpha falls from 0.54 under CK to 0.02 under HFA on the table's monthly return scale. Its OLS standard error falls from 0.46 to 0.32, and its White standard error from 0.46 to 0.26. At the same time SMB alpha moves from −0.39 to −0.52 and HML from 0.05 to 0.20. Joint rejection is not determined by the market alpha alone. The table does not explicitly restate the return-unit convention; these values should be retained on the source scale unless the input return normalization is verified.

## What can be reproduced and what remains uncertain

The core estimator can be implemented from the paper: build the time cross-product, initialize a diagonal, alternate whitened leading eigenvectors with diagonal residual updates, orthogonalize without demeaning, and repeat separately for each $K$. The empirical comparisons require matched date windows, matched security panels, the reported five-iteration convention, and identical benchmark return definitions. The simulations require preserving factor/variance date pairing and loading/residual-variance stock pairing; independently resampling those pieces would destroy part of the calibrated structure.

The unavailable historical security lists, data vintage, random seeds, precise missingness screens, and some calibration regression conventions prevent a bit-for-bit reconstruction. Numerical boundary handling, stopping tolerances beyond the fixed iteration counts, and remedies for indefinite pairwise matrices are also unspecified. An implementation should report these choices, inspect positivity and reconstruction residuals, and test sensitivity to iterations and cross-sectional composition.

The practical conclusion is that shared idiosyncratic volatility can corrupt a statistical factor span even in a very large universe. Modeling the time-varying diagonal can recover economically meaningful components that ordinary PCA misses. The limitation is equally important: this is an in-sample statistical extraction improvement under a specific diagonal-noise structure, not proof of better out-of-sample risk forecasts, profitable factor timing, or a universally correct factor count.
