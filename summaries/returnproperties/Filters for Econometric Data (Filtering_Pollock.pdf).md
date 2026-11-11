# Filters for Econometric Data

D. S. G. Pollock, seven-page teaching document, undated in the supplied file. Source: [Filtering_Pollock.pdf](../../Finance/Filtering_Pollock.pdf). The note covers Wiener-Kolmogorov estimation, polynomial detrending, the Hodrick-Prescott filter, and a finite-sample Butterworth construction.

## Why this matters

Differencing a trending series can suppress precisely the slow fluctuations a researcher wants to study. Pollock develops finite-sample filtering through covariance-based signal estimation, then shows how polynomial detrending and smoothing fit the same matrix framework. The useful methodological content is the handling of short trended sequences and boundary conditions, rather than a new empirical forecast test.

For financial research, this framework makes two assumptions visible: what is assigned to signal versus noise, and what information a filtered value uses. A whole-sample smoother is not a real-time trading signal. This document gives retrospective filters; it supplies no out-of-sample forecasting or portfolio-performance evidence.

## The covariance estimator and its domain

Let the observed vector be $y=\xi+\eta$, with independent zero-mean Gaussian signal and noise, having covariance matrices $\Omega_\xi$ and $\Omega_\eta$. Seek a linear estimate $x=\Psi y$. The least-squares projection condition is orthogonality of the residual to observations:

$
0=\operatorname{Cov}(\xi-\Psi y,y)=\Omega_\xi-\Psi(\Omega_\xi+\Omega_\eta).
$

Therefore

$
x=\Omega_\xi(\Omega_\xi+\Omega_\eta)^{-1}y,
\qquad h=\Omega_\eta(\Omega_\xi+\Omega_\eta)^{-1}y,
\qquad x+h=y.
$

The matrix order matters: covariance matrices need not commute. Joint Gaussianity makes the linear projection equal to the full conditional expectation. With only second moments and orthogonality, the same formula remains the best linear estimator, but need not be the unrestricted conditional mean. The document's discussion of conditional expectations should be understood under its Gaussian assumptions, not as a formula for any pair of dependent variables.

Nonzero means require centering and adding the signal mean back. Singular covariance requires a suitable generalized-inverse/support treatment rather than an unconditional ordinary inverse. Neither extension is the empirical subject of this note.

## Difference matrices and the polynomial null space

Let $D$ be the $(T-2)\times T$ matrix whose rows apply second differences, with entries $(1,-2,1)$ at consecutive positions. For $T=5$,

$
D=\begin{pmatrix}1&-2&1&0&0\\0&1&-2&1&0\\0&0&1&-2&1\end{pmatrix}.
$

This removes the two artificial initial rows of a square lag-operator representation. Its null space consists of vectors linear in time, including constants. The source writes $Q'=D$, so $Q$ has dimension $T\times(T-2)$.

The least-squares linear-trend fit and residual are

$
x_{\rm linear}=[I-D'(DD')^{-1}D]y,
\qquad e=D'(DD')^{-1}Dy.
$

These are complementary orthogonal projections. The residual contains the same linear information as the second-difference vector $g=Dy$: $g=De$ and $e=D'(DD')^{-1}g$. “Same information” is an invertible relation between those subspaces, not identical spectra. Differencing strongly attenuates frequencies near zero, whereas the detrended residual retains a different representation of slow fluctuations.

Figures 2-5 illustrate quarterly log consumption in the UK, 1955-1994, with a fitted linear trend and periodograms of levels, differences, and detrended residuals. The source does not identify the data series or its transformations sufficiently to reproduce every ordinate. These figures are explanatory examples, with no estimated treatment effect, standard errors, or forecast accuracy measure.

## Short trended sequences without arbitrary signal initialization

Suppose the differenced signal is $\delta=D\xi$ with covariance $\Omega_\delta$, while the noise remains stationary with covariance $\Omega_\eta$. Then $g=Dy=\delta+D\eta$. Assuming the components are independent and zero-mean after differencing,

$
\operatorname{Var}(g)=\Omega_\delta+D\Omega_\eta D',
\qquad \operatorname{Cov}(\eta,g)=\Omega_\eta D'.
$

Estimate the stationary noise from $g$ and subtract it from levels:

$
h=\Omega_\eta D'(\Omega_\delta+D\Omega_\eta D')^{-1}Dy,
\qquad x=y-h.
$

This is Equation 17 in dimensionally explicit notation. It avoids assigning arbitrary initial values to an integrated signal by placing the model on its differences and estimating stationary noise. It does not mean that a stationary noise process has an observed zero initial realization; zero mean and zero realized state are different. The finite covariance specification still determines how boundaries are treated.

## Hodrick-Prescott as a variance-ratio smoother

For second-difference white-noise signal innovations and white measurement noise, set $\Omega_\delta=\sigma_\delta^2I$ and $\Omega_\eta=\sigma_\eta^2I$. Let $\lambda=\sigma_\eta^2/\sigma_\delta^2$. The filter becomes

$
x=y-D'(\lambda^{-1}I+DD')^{-1}Dy
=(I+\lambda D'D)^{-1}y.
$

The second equality is the matrix inversion identity and gives an implementation without explicit covariance inversion. Equivalently minimize $\|y-x\|^2+\lambda\|Dx\|^2$. This objective makes the tradeoff concrete: fit observations while penalizing curvature, leaving a two-dimensional unpenalized linear-trend space.

As $\lambda\downarrow0$, $x\to y$. As $\lambda\to\infty$, it tends to the least-squares straight line. Interior infinite-sample gain is $[1+16\lambda\sin^4(\omega/2)]^{-1}$. This frequency expression is an additional derivation from the second-difference symbol; finite-sample endpoint rows need the actual matrix filter. Figure 6 compares 100, 1,600, and 14,400, with larger values passing a narrower low-frequency band. These are illustrative settings, not evidence that any one is optimal for a particular dataset.

The noise-to-curvature variance ratio interpretation depends on the assumed white-noise components. It does not make a conventional fixed $\lambda$ a statistically estimated parameter. No likelihood fit or cross-validated selection rule is supplied here.

## Butterworth construction and a dimensional qualification

The document seeks a sharper lowpass transition than HP provides. It proposes signal/noise difference equations with moving-sum $(1+L)^n$ and difference $(1-L)^n$ components, giving the finite expression

$
x=y-\lambda\Sigma D'(M+\lambda D\Sigma D')^{-1}Dy.
$

For implementation, $\Sigma$ must be $T\times T$ and $M$ must be $(T-2)\times(T-2)$. The printed expressions for $M$ and $D\Sigma D'$ use matrices labeled with order $T$, although the latter has order $T-2$. Boundary rows and the necessary dimension adjustment are not explained. A literal copy is therefore not a complete finite-sample algorithm. Choosing a periodic, padded, or truncated lag matrix can produce different endpoint behavior and must be declared.

The heuristic frequency-domain relation suggests gain $[1+\lambda\tan^{2n}(\omega/2)]^{-1}$ under the corresponding interior normalization, with half-gain cutoff satisfying $\lambda\tan^{2n}(\omega_c/2)=1$. This reconstructs the intended passband/stopband tradeoff; it does not repair the unspecified finite boundary matrices automatically. Figure 7 compares orders six and twelve. Its caption says cutoff $2\pi/3$, while the displayed drop is nearer $\pi/3$ on the plotted axis. That internal discrepancy should be checked before adopting its caption as a calibration.

The text also names the noise process rather than its innovation in one white-noise sentence. The intended independent driving noises should be distinguished from the filtered noise component itself. These qualifications affect transcription, not the general covariance-projection principle.

## Reimplementation limits

A reliable implementation can reproduce the HP and polynomial cases directly from the finite second-difference matrix, using linear solves and checking $x+h=y$ and the two limiting cases. The more general covariance filter requires declared component covariances. The Butterworth case needs a resolved boundary specification and cutoff convention beyond the printed formulas.

All these whole-vector estimates generally use future observations relative to an interior date and change when new data arrive. Any investment application must distinguish retrospective decomposition from a causal filter and evaluate endpoint revisions separately. There are no return forecasts, costs, or strategy tests in the source. Its value is a transparent connection among signal covariance, trend annihilation, curvature penalties, and frequency response, with finite-sample conventions exposed rather than hidden.
