# Dynamic factor models with infinite-dimensional factor space: Asymptotic analysis

**Mario Forni, Marc Hallin, Marco Lippi, and Paolo Zaffaroni.** *Journal of Econometrics* 199 (2017), 74–92. DOI: 10.1016/j.jeconom.2017.04.002. Source: [DynamicFactorModels_ForniHallinLippiZaffaroni_2017.pdf](../../Finance/DynamicFactorModels_ForniHallinLippiZaffaroni_2017.pdf). All 19 local PDF pages, including Appendices A–E, were read; critical estimation, simulation, and forecast pages were rendered and inspected. The cited online Appendices F and G are absent from the local file. Attempts to retrieve the publisher supplement and institutional working versions did not yield those appendices. Their detailed numerical tables and complete 73-series data dictionary are consequently not reconstructed here.

## Why this matters and what is new

A panel can be driven by a few economic shocks while requiring arbitrarily many contemporaneous static factors. If each observed series filters the shocks differently, adding variables can keep increasing the rank of the contemporaneous common-component covariance. An estimator that assumes a fixed finite static factor space then imposes more structure than a fixed number of primitive shocks alone warrants.

The 2015 companion paper established a useful representation: small blocks of $q+1$ common components, driven by $q$ shocks, generically admit finite autoregressive representations. Applying these block filters to the entire panel turns the dynamically heterogeneous common part into a static rank-$q$ component. The 2017 paper supplies the sample estimator, consistency rates, and numerical evaluation. These are distinct contributions and distinct papers, not duplicate versions of one work.

The central result is that a feasible, one-sided estimator of shocks and impulse responses can be consistent without a fixed finite-dimensional static factor space. Its first stage estimates common covariances in the frequency domain. Its second stage fits low-dimensional autoregressions to those estimated common covariances. A third stage uses ordinary principal components after filtering. The frequency-domain stage uses the whole available estimation window to learn parameters, but the resulting shock filter is causal: it does not require future observations when applied at the endpoint.

This matters for forecasting and structural analysis. A two-sided common-component smoother can look excellent in the interior of a sample and deteriorate at the forecast origin, where future observations do not exist. The proposed representation addresses that endpoint problem. It does not automatically identify economically meaningful shocks, eliminate all tuning choices, or imply that the common-component forecast is the optimal forecast of a serially correlated idiosyncratic component.

## Model and assumptions

For series $i=1,\ldots,n$, write

$$
x_{it}=\chi_{it}+\xi_{it},\qquad
\chi_{it}=b_i(L)u_t=\sum_{k\geq0}b_{ik}u_{t-k},
$$

where $u_t$ is a $q\times1$ vector of orthonormal white-noise common shocks, $q$ is fixed, and $b_{ik}$ is a $1\times q$ row vector. The scalar filters are rational:

$$
b_{if}(L)=\frac{c_{if}(L)}{d_{if}(L)}.
$$

Numerator and denominator degrees are uniformly bounded by $s_1$ and $s_2$. The denominators have roots uniformly outside the unit circle, and numerator coefficients are uniformly bounded. These restrictions produce uniformly decaying impulse responses but allow heterogeneous denominators across series, which is what permits an infinite-dimensional static factor space.

The idiosyncratic component has a linear-process representation using a countable set of orthonormal innovations. Its coefficients decay geometrically in lag, with uniformly bounded sums across both relevant cross-sectional indices. Common and idiosyncratic innovations are orthogonal; the paper's joint innovation construction is independent over time. Moment assumptions bound the $p$th moments uniformly for some $p>4$.

The common spectral density has exactly $q$ strong eigenvalues: after division by $n$, they remain bounded away from zero and separated from one another uniformly over frequency. The remaining spectral eigenvalues remain bounded. This is a pervasiveness and eigenvalue-separation condition, not a condition that every asset has a large loading on every shock.

The panel is partitioned into blocks of $q+1$ variables. For block $j$, the common component satisfies

$$
A_j(L)\chi_{j,t}=R_j u_t,
\qquad
A_j(L)=I-\sum_{\ell=1}^{S_j}A_{j\ell}L^\ell.
$$

The finite orders are bounded by a common $S$, with the representation result providing the generic bound $S\leq q s_1+q^2s_2$. Stability and uniqueness hold for the selected blocks under the maintained assumptions. The earlier representation theorem is generic; the sampling theorem needs quantitative regularity beyond a statement that singular parameter configurations have measure zero.

In particular, the covariance matrix of each chosen block's stacked lags must remain uniformly invertible. Assumption 7 expresses this through a positive lower bound on its determinant. This excludes blocks becoming arbitrarily close to an uninformative or singular configuration as the panel grows. A second additional condition requires the transformed common loading matrix to remain pervasive: the positive eigenvalues of $RR'/n$ are bounded away from zero and separated. Strong common spectra before filtering do not by themselves remove the need to check the transformed representation.

Stacking the filters gives block-diagonal $A(L)$ and

$$
Z_t=A(L)x_t=Ru_t+\Psi_t,qquad \Psi_t=A(L)\xi_t.
$$

The assumptions guarantee that the transformed disturbance remains idiosyncratic. Ordinary PCA can now recover a rank-$q$ static component. The block filter is the device that permits static PCA at this stage without assuming a finite static factor dimension for the original panel.

## Estimation, with implementable conventions

Start with a training window of $T$ observations. Demean and, for the empirical exercises, standardize each series using that window. Keep the scaling parameters for later inverse transformation. Select the dynamic shock count $q$, a spectral bandwidth $B_T$, a lag-window kernel, block orders, and an ordering of the variables. Their selection must use training data when evaluating forecasts.

For nonnegative lags define

$$
\widehat\Gamma_x(h)=\frac1T\sum_{t=h+1}^T x_t x_{t-h}',
\qquad
\widehat\Gamma_x(-h)=\widehat\Gamma_x(h)'.
$$

The transpose for negative lags is essential in a multivariate implementation. The compact printed formula using $|h|$ should not be read as permission to use the same nonsymmetric covariance at positive and negative lags. Form the Hermitian lag-window spectral estimate

$$
\widehat\Sigma_x(\theta)=\frac{1}{2\pi}
\sum_{h=-B_T}^{B_T}K(h/B_T)\widehat\Gamma_x(h)e^{-ih\theta}.
$$

At each frequency retain the $q$ largest eigenvalues and their eigenvectors. If these are $\widehat\Lambda_q(\theta)$ and $\widehat P_q(\theta)$,

$$
\widehat\Sigma_\chi(\theta)=
\widehat P_q(\theta)\widehat\Lambda_q(\theta)\widehat P_q(\theta)^*.
$$

The star denotes conjugate transpose. Inverse Fourier integration gives estimated common-component covariances at the required lags. The source uses the grid $\theta_h=\pi h/B_T$ and a Riemann approximation with spacing $\pi/B_T$. Use a consistent periodic endpoint convention; do not double-count $-\pi$ and $\pi$ as separate full-weight frequencies. Verify that the reconstructed zero-lag covariance agrees with the integrated spectrum under the chosen $1/(2\pi)$ normalization.

For block $j$, let $w_{j,t}$ stack its $S_j$ lagged common-component vectors. Construct

$$
C_j=E[w_{j,t}w_{j,t}'],\qquad
D_j=E[\chi_{j,t}w_{j,t}'],\qquad
[A_{j1}\ \cdots\ A_{jS_j}]=D_jC_j^{-1}.
$$

Replace all covariances by their frequency-domain common-component estimates. The dimensions are $(q+1)S_j$ square for $C_j$ and $(q+1)\times(q+1)S_j$ for $D_j$. This is a Yule–Walker calculation on estimated common covariances, not an ordinary VAR regression of raw noisy series. Applying an ordinary VAR directly to raw $x_{j,t}$ generally targets different coefficients because its lag covariances contain idiosyncratic contributions.

Apply the estimated filters to observed data and collect $\widehat Z_t$. Compute its covariance and its leading $q$ eigenvectors $P_Z$ and eigenvalues $\Lambda_Z$. One internally consistent normalization is

$$
\widehat R=P_Z\Lambda_Z^{1/2},\qquad
\widehat v_t=\Lambda_Z^{-1/2}P_Z'\widehat Z_t.
$$

The recovered shock vector has sample covariance identity under the corresponding covariance convention, while $\widehat R\widehat v_t$ is the rank-$q$ fitted transformed component. The estimator is identified only up to an orthogonal rotation and, under separated eigenvalues and a fixed ordering, sign conventions. Physical shocks require an additional identifying restriction.

Once the impact loading is identified, impulse responses follow by inverting each block filter. With $B_{j0}=R_j$,

$$
B_{jh}=\sum_{\ell=1}^{\min(S_j,h)}A_{j\ell}B_{j,h-\ell},\qquad h\geq1.
$$

This recursion avoids repeatedly solving a spectral factorization at each horizon. It also provides a useful stability diagnostic: estimated impulse responses should decay when the block autoregression is stable. Unstable or ill-conditioned sample blocks require an explicit treatment; silently clipping roots or adding a ridge changes the reported estimator and should be recorded as an extension.

## Structural normalization and a source formula correction

The numerical exercises impose a recursive contemporaneous identification using the first $q$ variables. Let their reduced-form impact matrix be nonsingular $C$, and let $H$ be the lower triangular Cholesky factor of $CC'$, so $HH'=CC'$. Define

$$
Q=C^{-1}H,\qquad QQ'=I.
$$

Then the identified responses and shocks are

$$
B_h^*=B_hQ,\qquad
u_t^*=Q'u_t=H'C^{-\prime}u_t=H^{-1}Cu_t.
$$

These equations preserve $B_hu_t=B_h^*u_t^*$. The source's shock-transform expression on the simulation identification page omits an inverse in the corresponding transpose term; the transformation above is the algebraically consistent version. It is stated as a correction derived from the normalization, not a second identifying assumption.

When averaging across variable permutations, keep the economic anchor variables and their recursive order fixed after restoring the original series labels. Rotating each run with a different first-$q$ economic block would average different structural objects. Common-component forecasts are rotation invariant if shocks and loadings are rotated together, but individual impulse responses are not.

## Rates and proof logic

The lag-window kernel is even, bounded, and compactly supported, with $K(u)-1=O(|u|^\kappa)$ near zero, finite squared integral, and the regularity needed to control differences on the frequency grid. The bandwidth is bounded between powers of $T$, with lower exponent $\underline\delta$ and upper exponent $\overline\delta$ satisfying

$$
0<\underline\delta<\overline\delta<1,
\qquad
\underline\delta(2\kappa+1)>1.
$$

For the Bartlett kernel, $\kappa=1$ and the lower exponent must exceed $1/3$. The common practical choice $B_T\asymp\sqrt T$ satisfies the relevant bias-versus-stochastic-error condition.

The resulting error scale is

$$
\zeta_{nT}=\max\left\{n^{-1/2},
\sqrt{\frac{B_T\log B_T}{T}}\right\}.
$$

The paper establishes this order for estimated common spectral entries on the grid, the required common covariances, block autoregressive coefficients, transformed loadings and shocks, and fixed impulse-response coefficients, with the identification qualifications stated in the propositions. A fixed row or lag result should not be promoted to a uniform guarantee over every date, every growing forecast horizon, or arbitrarily many badly conditioned blocks.

With $B_T\asymp\sqrt T$, the time-series component is roughly $T^{-1/4}\sqrt{\log T}$. This is slower than the familiar static-factor rate involving $T^{-1/2}$. The gain is weaker structural restriction on the original common process, not faster convergence in every model. If the finite-static-space model is exactly correct and well estimated, its stronger assumptions can be useful.

The proofs in Appendices A–E proceed through a chain of error controls. Moment and coefficient-decay assumptions imply weak physical dependence of the observed panel. This supports maximal spectral-estimation bounds over the frequency grid. Spectral pervasiveness and eigenvalue separation allow the leading dynamic eigencomponents to be isolated despite bounded idiosyncratic spectra. Fourier inversion transfers these bounds to common autocovariances. Uniform invertibility of the small block covariance matrices then transfers them to the autoregressive coefficients. Finally, transformed pervasiveness permits PCA perturbation arguments for $R$ and $u_t$, and stable filter inversion gives the impulse responses.

Each assumption has an operational failure mode. Closely spaced dynamic eigenvalues complicate eigenvector identification; a nearly singular lag covariance magnifies first-stage errors; an unstable estimated block filter amplifies long-horizon responses; weak transformed loadings make shocks noisy. A large panel does not fix all these problems merely by increasing $n$.

## Averaging over block orderings

The model does not attach economic significance to the order in which variables are placed into blocks. A finite-sample estimator nevertheless depends on that order. The paper proposes averaging estimates over random permutations to reduce this arbitrary variability. For impulse responses, restore original variable labels and align structural rotations before averaging coefficient arrays. For forecasts, average forecasts for the same target, date, and horizon.

A complete average over permutations has no greater expected quadratic loss than a randomly selected ordering under the relevant symmetry argument. A finite average over 30 permutations approximates that idea; it does not provide an exact guarantee for every realized dataset. When $n$ is not divisible by $q+1$, randomly omitted remainder variables vary across permutations and each series is averaged over the runs in which it appears.

There is an important distinction between averaging estimators before measuring loss and averaging separate losses. If $\widehat B^{(p)}$ is an impulse-response estimate under ordering $p$, the intended procedure evaluates

$$
\left\|\frac1\mu\sum_{p=1}^{\mu}\widehat B^{(p)}-B\right\|^2.
$$

It is not the same as $\mu^{-1}\sum_p\|\widehat B^{(p)}-B\|^2$. The latter expression appears in the source's averaging discussion, but cannot by itself explain decreasing expected error as the number of identically distributed permutations increases. The surrounding discussion and Figure 1 concern the former estimator-averaging operation. This distinction should be resolved explicitly when replicating the figure.

## Simulation design and reported outcomes

Model I has two common shocks and heterogeneous autoregressive propagation:

$$
x_{it}=\frac{a_{i1}}{1-\alpha_{i1}L}u_{1t}
+\frac{a_{i2}}{1-\alpha_{i2}L}u_{2t}+\xi_{it}.
$$

The shocks and idiosyncratic terms are independent standard normal variables. Loadings are drawn uniformly on $[-1,1]$ and autoregressive coefficients on $[-0.8,0.8]$. The experiment crosses $n=30,60,120,240$ with $T=60,120,240,480$, using 500 replications. This is a genuine infinite-static-dimension design as cross-sectional heterogeneity increases.

The FHLZ estimator uses a Bartlett kernel with bandwidth proportional to $\sqrt T$, BIC-selected small-block autoregressive orders, and, where stated, averaging over 30 permutations. For impulse-response and shock comparisons $q$ is imposed. The benchmark FGLR structural factor estimator works with a finite number of static factors and a VAR; static factor counts are either selected using Bai–Ng $IC_{p2}$ or imposed when the simulation makes that feasible. Lag orders are selected by BIC. The source does not fully specify the maximum candidate block/VAR lag order in the main PDF.

Impulse-response error sums squared errors over variables, shocks, and horizons zero through 60, normalized by the corresponding sum of squared true responses. Shock errors use a comparable normalization. Forecast comparisons in this simulation measure deviation from the oracle predictable common component, not simply squared error against the realized noisy observation. This distinction is crucial: unpredictable innovations and idiosyncratic noise are not included as an unavoidable benchmark variance in the same way as ordinary realized-return MSFE.

For forecasting, the feasible shock number uses the Hallin–Liška logarithmic information criterion with the stated penalty choice and a stability-interval calibration. The nested cross-sections have sizes $\lfloor3n/4+jn/40\rfloor$, $j=1,\ldots,10$, with $T$ fixed and bandwidth tied to $\sqrt T$. The paper specifies selection from the second stability interval. A full implementation still needs the original criterion's numerical calibration grid and tie rules; they are not supplied as executable code here.

The main-text results report impulse-response errors up to 50–60% below FGLR and common-component forecast errors 20–40% below the Stock–Watson static-factor forecast across the Model I configurations. The static factor estimator selects an average of about 2.01 factors at $n=30,T=60$ and 4.00 at $n=240,T=480$: increasing static dimension approximates the heterogeneous dynamic structure but does not eliminate the observed finite-sample advantage.

Figure 1 shows substantial gains from averaging the first few permutations and then flattening. For example the curves stabilize fairly quickly around five to ten permutations in the larger panels; the smallest panel improves more gradually. The figure is about normalized response-estimation loss, not percentage returns or an out-of-sample trading Sharpe ratio.

Model II is favorable to finite-static-factor methods. It has $n=120,T=240$ and

$$
F_t=DF_{t-1}+Ku_t,\qquad x_t=\Lambda F_t+\xi_t.
$$

Entries of $\Lambda$ and $K$ are drawn uniformly on $[-1,1]$. A random transition matrix is scaled by its spectral norm and multiplied by a draw between 0.4 and 0.9 to control persistence. Static dimensions are drawn from $r=4,6,8,12$ and dynamic dimensions from $q=2,4,6$, using admissible combinations with $r>q$. Shocks and idiosyncratic innovations are normal. The main text reports that averaged FHLZ performs better than FGLR across the estimated-dimension comparisons and remains best in most cases when FGLR is given the correct static dimension. Forecast comparisons likewise favor FHLZ in most configurations. These are numerical findings, not a theorem of universal dominance.

## Quarterly U.S. forecasting experiment

The empirical panel contains 73 quarterly U.S. series, including 12 series associated with the Survey of Professional Forecasters. Raw observations cover 1968Q4–2010Q4; stationarity transformations yield 1969Q1–2010Q4, 168 observations. Real quantities are generally first log differenced, while prices and monetary aggregates are generally second log differenced. The complete series-by-series transformation dictionary is in missing Appendix G, so the exact 73-column panel cannot be rebuilt from the local main paper alone.

The targets are real GDP, real private fixed investment, real consumption expenditure, the number unemployed, and CPI. Estimation uses rolling windows of 68 quarters, equivalent to 17 years. The first window is 1969Q1–1985Q4; horizons are one through four quarters. This is a rolling, not expanding, design. Every window is standardized afresh and forecasts are converted back using its training-window scale and mean.

The main text describes forecast origins through 2009Q4 but also reports $101-h$ forecasts at horizon $h$. Those counts do not follow directly from a common 1985Q4–2009Q4 origin range. A replication needs an explicit origin–target date table rather than silently choosing one of these descriptions. Similarly, wording describing the target as a difference of an already transformed series conflicts with the interpretation as growth in a level over $h$ periods. For a first-differenced log input, the corresponding level-growth target is the sum of predicted differences; second-differenced price data require the appropriate integration using the known initial inflation rate. This is a mathematically consistent reconstruction, but the source's exact target convention should be confirmed from code or the supplement before claiming exact replication.

The baseline spectral bandwidth is eight, approximately $\sqrt{68}$. Bandwidths 12 and 16 give similar qualitative results, while four is worse. The Hallin–Liška procedure applied to the first window suggests four shocks. Reported FHLZ configurations include $(q,B)=(3,8),(4,8),(3,12)$. The Stock–Watson alternatives consider two, four, or six static factors and target lag orders zero, one, or four, with additional BIC choices. Reported benchmark specifications include $(r,p)=(2,0),(4,0),(6,0),(4,1)$. A univariate AR(4) is the forecast benchmark. Response filters are truncated at 60 lags.

The paper calls its relative error measure RMSFE, but the described comparison is a ratio of mean squared forecast errors, not necessarily a ratio of their square roots. A value 0.8 in that convention means 20% lower MSE; it does not mean 20% lower root-MSE. The main text reports broad forecast improvements except for consumption, especially for GDP and inflation, with long-horizon improvements around 30% for investment and inflation and 15–20% for GDP and unemployment. It reports several statistically significant Diebold–Mariano comparisons. Exact model-by-target cells, standard errors, and significance markers are in absent Appendix F and cannot responsibly be supplied from those qualitative statements.

## Boundaries of reproducibility and interpretation

The theoretical estimator is reconstructible from the main paper: spectral common covariance estimation, block Yule–Walker filtering, PCA of transformed observations, shock normalization, response recursion, and permutation averaging are all specified. The proof conditions also identify where the method can fail. A robust implementation should record block conditioning, filter roots, sensitivity to bandwidth, the common eigengap, and the chosen shock dimension.

The exact numerical experiments are only partially reproducible from this local file. Missing items include the detailed supplementary tables, the complete empirical panel dictionary, several numerical selection-grid conventions, and resolution of the forecast-count and target-transformation wording. The source's shock-rotation and averaging expressions require the algebraic qualifications given above. These limitations concern exact reproduction, not the existence of the estimator or the main consistency result.

Finally, forecasting the common component is not identical to forecasting all of $x_t$ when idiosyncratic components are serially correlated. One can add a model for the residual predictable component, but that is an extension requiring its own validation. The paper's contribution is a causal, flexible common-shock estimator whose finite-sample performance can be competitive even against more restrictive static-factor methods. It is not a license to assume every forecast gain survives data revisions, unstable groupings, misspecified structural restrictions, or a different information set.
