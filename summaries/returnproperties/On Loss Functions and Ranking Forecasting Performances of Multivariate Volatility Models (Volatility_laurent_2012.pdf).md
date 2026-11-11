# On Loss Functions and Ranking Forecasting Performances of Multivariate Volatility Models

**Sébastien Laurent, Jeroen V. K. Rombouts, and Francesco Violante.** Manuscript dated July 6, 2011. Source: [Volatility_laurent_2012.pdf](../../Finance/Volatility_laurent_2012.pdf). The year in the library basename differs from the manuscript date. This note covers all 26 PDF pages, including the complete proof appendix; printed page numbers run from an unnumbered title page to p. 25.

## Why this matters

A covariance forecasting competition can choose the wrong model even with a long evaluation sample and a formally correct significance test. The problem is that the covariance being forecast is latent. Researchers replace it with a realized covariance matrix, but changing the quality of that proxy can change what an apparently reasonable loss function rewards.

The paper's central contribution is a multivariate characterization of losses whose expected pairwise differences are invariant to conditionally unbiased measurement noise. Those losses have a Bregman form. It also characterizes the smaller class depending only on forecast errors: positive-definite quadratic forms in the unique entries of the covariance-error matrix. Its empirical illustration varies the intraday sampling frequency while holding forecasting models fixed. This cleanly distinguishes losses that merely lose precision as the proxy deteriorates from losses that change their population target.

The conclusion is not that there is one universally best covariance forecast. A consistent loss preserves its own target ranking, while different consistent losses can embody different economic or statistical priorities. Nor does consistency make a poor proxy harmless: noisy proxies leave less power to distinguish models. The implementation lesson is to choose the evaluation target and loss deliberately before interpreting model-confidence sets.

## Forecasting object and assumptions

Let $\mathcal F_{t-1}$ be the information available when forecasts are made. The target $\Sigma_t$ is a symmetric positive-definite conditional covariance matrix for an $N$-vector of returns. Competing forecasts $H_{m,t}$ are $\mathcal F_{t-1}$-measurable matrices in a compact subset of the positive-definite cone. The observed proxy is $Y_t=\widehat\Sigma_t$. Its crucial property is conditional unbiasedness:

$$
E[Y_t\mid\mathcal F_{t-1}]=\Sigma_t.
$$

Unconditional unbiasedness is insufficient if proxy bias co-varies with information used by the forecasting models. The paper supposes at least one conditionally unbiased proxy exists. That is an assumption about the measurement process, not something proved for every realized covariance series in the empirical application.

Write $K=N(N+1)/2$, $s_t=\operatorname{vech}(\Sigma_t)$, $y_t=\operatorname{vech}(Y_t)$, and $h_t=\operatorname{vech}(H_t)$, where vech stacks the unique triangular entries. Measurement error is $\xi_t=y_t-s_t$. For a sequence of proxies indexed by accuracy $a$, the conditional error covariance is $V_t^{(a)}=E_{t-1}[\xi_t^{(a)}\xi_t^{(a)\prime}]$, finite and tending to zero as accuracy increases.

The paper normalizes loss to zero exactly when target and forecast agree, and requires integrability, continuity, identification of the correct covariance, and differentiability sufficient for the arguments. Its stronger characterization invokes a rich class of absolutely continuous distributions on positive-definite matrices, an interior conditional mean, and interchange of derivatives and expectations. These qualifications matter when a proxy is rank deficient, a forecast is on a constraint boundary, or inverse and logarithmic terms have infinite expectations.

For forecasts $H_l,H_m$, ranking consistency means

$$
E[L(\Sigma_t,H_l)]\ge E[L(\Sigma_t,H_m)]
\quad\Longleftrightarrow\quad
E[L(Y_t,H_l)]\ge E[L(Y_t,H_m)].
$$

This is a population property. Sample averages may still order two nearly tied models incorrectly, especially when the proxy is noisy or losses have heavy tails. A correct test controls its stated inferential object; it cannot repair a loss that measures the wrong object.

## Bregman characterization and exact cancellation

Use a strictly convex differentiable function $\phi$ of the unique covariance coordinates. The nonnegative divergence is

$$
D_\phi(y,h)=\phi(y)-\phi(h)-\nabla\phi(h)'(y-h).
$$

The source writes the equivalent formula with a strictly concave $\widetilde C=-\phi$ (Proposition 2, Eq. (5)). Both formulations evaluate the gradient at the forecast. Reversing the arguments generally destroys the relevant mean-target property.

Conditional unbiasedness gives the exact identity

$$
E_{t-1}[D_\phi(y_t,h_t)]
=D_\phi(s_t,h_t)+E_{t-1}[\phi(y_t)]-\phi(s_t).
$$

The final two terms depend on the proxy and its distribution but not on the forecast. Subtract the losses of any two predictable forecasts and these terms cancel. This establishes invariant expected differences, not just invariant minimizers. It also explains why the proxy-based loss itself need not be unbiased for the true loss.

The derivative with respect to the forecast is

$$
\nabla_h D_\phi(y,h)=\nabla^2\phi(h)(h-y).
$$

At the conditional mean, its expectation is zero. The characterization's necessity argument works in the reverse direction: if the expected gradient vanishes at the conditional mean for every admissible distribution, it must be linear in the centered observation, with a matrix coefficient depending on the forecast. Integrating this expression produces the Bregman form up to target-only terms; zero loss on the diagonal fixes the normalization. This is a result for the stated rich distribution class and smoothness assumptions, not a claim that no other loss can happen to rank a particular finite collection of models correctly.

The paper also gives a mixed-derivative condition: the target-coordinate Hessian of loss should not depend on forecast coordinates. For a Bregman loss, the target Hessian is $\nabla^2\phi(y)$, which has exactly this property. A Taylor expansion explains what happens when the condition fails:

$$
E_{t-1}[L(y_t,h)]-L(s_t,h)
\approx\frac12\operatorname{tr}\{L_{ss}(s_t,h)V_t\}.
$$

If this correction differs across forecasts, noise can alter their ranking. Accurate proxies reduce the distortion when the necessary regularity and integrability conditions hold. A ranking with a large genuine loss gap can tolerate more distortion than one between nearly tied models.

The approximate expansion should not be mistaken for an exact finite-noise formula. The manuscript says its Eq. (4) becomes an equality under the mixed-derivative condition, but that condition does not eliminate higher-order target-only terms for a nonquadratic generator. Exact *difference* cancellation follows from the Bregman identity above and does not require claiming that a second-order expansion of each individual expected loss is exact.

## Losses that can be implemented directly

For a fixed symmetric positive-definite $W$, the quadratic family is

$$
L_W(Y,H)=\operatorname{vech}(Y-H)'W\operatorname{vech}(Y-H).
$$

This is Proposition 3's error-only family. It is homogeneous of degree two under common scaling of target and forecast and symmetric under simultaneous sign reversal of the coordinate error. Error-only dependence forces the generator Hessian to be constant; integration yields a quadratic generator plus affine terms, which cancel out of the divergence. A positive-semidefinite $W$ may leave some directions unpenalized and lose the paper's unique-minimizer property.

With $W=I$, variances and unique covariances receive the same coordinate weight. For squared Frobenius loss,

$$
L_F(Y,H)=\operatorname{tr}[(Y-H)^2]
=\sum_i(Y_{ii}-H_{ii})^2+2\sum_{i<j}(Y_{ij}-H_{ij})^2.
$$

The factor of two on off-diagonals matters. Treating vech entries equally is not the same criterion as summing squared errors over all matrix entries. More general $W$ allows correlated coordinate errors to be penalized jointly. Such weights must be fixed or predictable and common across competing forecasts for the conditional cancellation argument; fitting model-specific weights would define a different comparison.

Two other useful generators demonstrate that a consistent loss need not be quadratic. With $\phi(H)=\operatorname{tr}(H\log H-H)$, the matrix logarithm being the principal spectral logarithm,

$$
D_{\mathrm{VN}}(Y,H)=\operatorname{tr}[Y(\log Y-\log H)-Y+H].
$$

This is the von Neumann divergence. With $\phi(H)=-\log\det H$,

$$
D_{\mathrm{Stein}}(Y,H)
=\operatorname{tr}(H^{-1}Y)-\log\det(H^{-1}Y)-N.
$$

Stein loss is homogeneous of degree zero under common rescaling and penalizes small forecast eigenvalues strongly when realized variation lies in those directions. Use a Cholesky solve and log determinants rather than an explicit inverse in numerical work. In one dimension it is $y/h-\log(y/h)-1$, the familiar variance quasi-likelihood divergence. These formulas are derived here from the manuscript's general characterization to make implementation unambiguous.

Several printed examples require correction. On p. 8, the stated homogeneity degrees for squared error, relative entropy, and Itakura–Saito loss are in reversed order at the endpoints: they are two, one, and zero respectively. The printed eigenvalue expression for von Neumann loss in Eq. (8) is not consistent with its stated generator and eigenvalue/eigenvector assignments. Most decisively, printed Eq. (9) for Stein loss is zero for all scalar target/forecast pairs because its two scalar terms cancel. It cannot be a strictly discriminating loss. Also, the manuscript uses $\widetilde C(H)=\log|H^2|=2\log\det H$; this generates twice the Stein formula above, an irrelevant positive factor for ranking, but not the displayed Eq. (9).

The appendix contains related sign slips: the mean-optimal expected forecast Hessian equals $-\Lambda$, so the concave-generator Hessian $\Lambda$ must be negative definite, consistent with Proposition 2, despite a sentence on p. 19 calling it positive definite. The integrated expression must have $-\widetilde C(Y)$ and the gradient term specified in Eq. (5). The correct main characterization should be used rather than transcribing those inconsistent intermediate lines.

Global convexity in the *forecast* should also be distinguished from strict propriety for the mean. Bregman divergences are convex in their first argument, but need not be globally convex in their second. Scalar Stein loss has second forecast derivative $(2y-h)/h^3$, which becomes negative for $h>2y$. Thus a blanket strict-convexity requirement in forecast space is stronger than what all the manuscript's named examples satisfy. The cancellation result and mean minimizer remain valid for the correctly oriented divergence.

## Empirical experiment

The data are euro, British-pound, and Japanese-yen exchange rates expressed in U.S. dollars. The estimation sample is January 6, 1987–December 28, 2001, with 3,666 trading days. The forecast-evaluation sample extends through August 26, 2004 and contains 660 trading days. Table 2's model-confidence-set calculations use 650 observations. That difference should be retained rather than assuming every loss table uses 660 observations; the paper does not fully spell out the alignment of the ten-day horizon and common evaluation sample.

For an intraday grid of width $\Delta$, calculate realized covariance as

$$
Y_{t,\Delta}=\sum_{k=1}^{M_\Delta}r_{t,k}r_{t,k}',
$$

using synchronized intraday return vectors. The experiment uses 17 grids: 5, 10, 15, 20, 30, and 40 minutes; 1 hour; 1 hour 20 minutes; 1 hour 40 minutes; 2 hours; 2 hours 40 minutes; 3, 4, 6, 8, and 12 hours; and one day. A full 24-hour day provides 288 five-minute intervals but only one daily return outer product. With three assets, an eight-hour grid is the coarsest one capable of giving rank three; twelve-hour and daily proxies are necessarily rank deficient. Frobenius and absolute-entry losses remain computable there, while positive-definite log-determinant formulas do not apply without additional treatment.

The article calls five-minute covariance the most accurate proxy in its experiment. That should not be interpreted as a theorem that the highest available frequency is always best. Microstructure noise, stale prices, asynchronous observations, and market closures can bias very finely sampled realized covariance. No new microstructure-robust estimator is developed here. Conditional unbiasedness and sufficient synchronization are maintained assumptions whose practical validity must be checked in a new dataset.

There are 24 forecasting specifications (Table 1): constant conditional correlation and dynamic conditional correlation, each paired with GARCH, asymmetric-power GARCH, exponential GARCH, GJR, integrated GARCH, and univariate RiskMetrics variance models; orthogonal and generalized orthogonal models, each paired with the first five of those variance models; plus diagonal BEKK and multivariate RiskMetrics. That is $2\times6+2\times5+2=24$.

Estimation is quasi-maximum likelihood, using the authors' OxMetrics 6/G@RCH 6 programs. Forecast horizons are one and ten steps. The published experiment compares squared Frobenius loss with the sum of elementwise absolute errors, denoted $L_{1M}$. The latter is not a mean-consistent covariance loss: absolute errors target coordinate medians rather than means. A noisy outer product can have a highly skewed distribution, so reducing sampling frequency can systematically change which forecast this criterion prefers.

To reconstruct the design, retain exactly the same model forecasts while recomputing the evaluation proxy at each grid. Otherwise the effect of noisy evaluation targets becomes entangled with different model estimation. Rank models by average loss, plot differences from the average loss across models, and apply the same inference procedure to each loss/proxy combination. The experiment does not train its models on each of the 17 realized-covariance grids; those grids are the evaluation intervention.

Important inputs remain undisclosed in this PDF: exact raw-price provider and cleaning rules, construction of the pre-euro history, time-zone/day boundaries, missing-quote synchronization, conditional-mean specification, orders and initialization for every GARCH variant, forecast recursion details for nonlinear ten-step models, and whether parameters are held fixed or re-estimated through the holdout. The paper cites model references and software but does not provide all those numerical choices. It would be misleading to fill them with standard defaults and claim exact replication.

## Results and uncertainty

With squared Frobenius loss, CCC-GARCH is the best one-step forecast at almost all sampling frequencies. CCC/DCC models with GARCH or GJR variances form the strongest cluster. Integrated specifications generally perform poorly, apart from RiskMetrics variants ranking nearer the middle. Rankings are particularly stable between five minutes and one hour. At coarser frequencies they become noisier, which is compatible with invariant expected rankings and larger sampling variation.

Under absolute-entry loss, RiskMetrics variants improve steadily as the proxy becomes less accurate. With grids of two hours or coarser, they appear far better than alternatives in the one-step comparison. Figures 1–2 therefore illustrate a population-target problem rather than a finding that coarser market data reveals superior RiskMetrics dynamics. The ten-step comparison exhibits the same concern, with smoother forecasts and larger between-cluster loss differences moderating some movements in ranks.

The model-confidence-set procedure starts from all 24 models and sequentially evaluates equal predictive ability. The source uses the $T_D$ deviation-from-average statistic in MULCOM, a significance level of 0.1, 10,000 bootstrap resamples, and 650 evaluation observations (Table 2). Interpreted conventionally, this is a 90% model confidence set, although the surrounding prose calls 0.1 a confidence level. Bootstrap block length and dependence scheme are not reported here, so the exact p-values and membership cannot be regenerated from the table alone.

The most informative contrast is at the endpoints. For one-step Frobenius evaluation at five minutes, the retained set is CCC-GARCH and CCC-GJR. At eight hours it contains twelve models. For ten-step Frobenius evaluation, the five-minute set contains only CCC-GARCH, while the eight-hour set contains seventeen models, counted directly from Table 2. The text describes the latter as two thirds of 24; the printed membership list is slightly larger. Reduced measurement precision broadens the plausible set rather than establishing a new strong winner.

At eight hours, absolute-entry loss selects only RiskMetrics-family models: the multivariate, DCC, and CCC variants at one step, and DCC-RiskMetrics at ten steps. These sets have no overlap with their five-minute counterparts. Thus an apparently decisive small confidence set can be especially misleading when the criterion is inconsistent for the intended covariance target.

The source also says that a high-precision confidence set is always contained in a lower-precision one. This describes the main empirical tendency, not a mathematical implication of population ranking consistency. Finite-sample MCS selections need not nest across noisy proxies. Table 2 itself swaps O-GARCH for O-EGARCH between the two coarsest one-step Frobenius columns. The reliable conclusion is loss of discrimination as precision deteriorates, rather than guaranteed set inclusion.

## Reuse and boundaries

A sound implementation separates three decisions: what covariance is being forecast, how it is measured ex post, and what errors matter. The Bregman identity supplies a useful unit test: simulate an unbiased proxy around a known covariance, compare average pairwise losses, and verify that the limiting difference matches the exact-target difference. Quadratic loss additionally admits an analytic check because its proxy-noise contribution is $\operatorname{tr}(WV_t)$, common to all forecasts.

For a portfolio application, a squared error in a fixed predictable portfolio variance, $(w'(Y-H)w)^2$, is a quadratic loss in covariance coordinates, although it is not strictly identifying for the whole covariance matrix. This is a derived application of the characterization, not an empirical experiment in the paper. If the weights themselves are optimized differently from each model's covariance, the common-loss cancellation argument does not directly compare the resulting investment strategies. That would require a separate economic evaluation.

The study establishes neither superior realized investment returns nor superior option pricing. Its conclusion explicitly leaves economic loss and alternative robust covariance proxies for later work. Its contribution is more basic and reusable: a testing framework should preserve the covariance-ranking question under measurement noise, and its uncertainty should reflect the quality of the evaluation data. Correcting the manuscript's illustrative formulas is necessary to implement that contribution faithfully.
