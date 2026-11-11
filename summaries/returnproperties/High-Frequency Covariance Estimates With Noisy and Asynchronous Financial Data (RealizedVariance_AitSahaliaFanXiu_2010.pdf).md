# High-Frequency Covariance Estimates With Noisy and Asynchronous Financial Data

Yacine Aït-Sahalia, Jianqing Fan, and Dacheng Xiu. *Journal of the American Statistical Association* 105(492), December 2010, 1504–1517. DOI: 10.1198/jasa.2010.tm10163.

Source: [original PDF](../../Finance/RealizedVariance_AitSahaliaFanXiu_2010.pdf), containing a JSTOR cover followed by 14 article pages. Page references below use printed article pagination. The note covers the model, synchronization algorithm, likelihood calculation, theoretical qualifications, simulation, and six-currency futures application.

## Why this matters and the contribution

A covariance estimator built from very short returns faces two distinct problems. Different assets trade at different instants, so nominally simultaneous returns may not cover the same intervals. The prices also contain microstructure noise, which dominates sufficiently short return increments. Both can depress measured correlations as sampling becomes finer, producing an Epps-effect pattern. Correcting only one of the problems is inadequate.

The paper combines a univariate quasi-maximum likelihood variance estimator with a synchronization scheme. It estimates the variance of the sum and difference of two synchronized log-price series and recovers covariance by polarization. The underlying likelihood assumes a simple constant-volatility Gaussian model, but the quasi-likelihood estimates remain consistent under stochastic volatility and non-Gaussian independent noise. The paper proves an optimal $n^{-1/4}$ convergence rate under its observation assumptions, and an explicit central limit theorem in the synchronous setting.

The practical attraction is that the likelihood estimator does not require selecting a smoothing bandwidth. That does not remove decisions about data cleaning, observation selection, optimization constraints, or covariance-matrix repair. The estimator can also produce a matrix that is not positive semidefinite. These limitations matter when the output is used in portfolio optimization rather than merely plotted as a time series of pairwise correlations.

## Model and precise estimand

For two assets, the latent log prices satisfy

$$
dX_{it}=\mu_{it}\,dt+\sigma_{it}\,dW_{it},
\qquad d\langle W_1,W_2\rangle_t=\rho_t\,dt,
\quad i=1,2.
$$

Volatilities are positive, locally bounded Itô semimartingales; drifts are locally bounded and progressively measurable. Prices are observed at asset-specific times with additive level errors,

$$
\widetilde X_{i,t_{i,j}}=X_{i,t_{i,j}}+U_{i,t_{i,j}}.
$$

The basic noise model uses independent and identically distributed error vectors with mean zero, finite fourth moments, and a diagonal cross-asset noise covariance matrix. The univariate setup assumes noise independent of the price and volatility processes. The synchronous appendix also examines correlated cross-asset noise; that extension should not be conflated with the assumptions imposed for the asynchronous theorem.

Write the average variance and covariance rates over $[0,T]$ as

$$
v_i=\frac1T\int_0^T\sigma_{it}^2\,dt,
\qquad c_{12}=\frac1T\int_0^T\rho_t\sigma_{1t}\sigma_{2t}\,dt.
$$

The likelihood's variance parameter converges to $v_i$, not directly to the unnormalized integral. Thus integrated covariance is $Tc_{12}$ and integrated variance is $Tv_i$. If time is normalized to $T=1$, the distinction disappears numerically. Correlation is

$$
r_{12}=\frac{c_{12}}{\sqrt{v_1v_2}}
=\frac{\int_0^T\rho_t\sigma_{1t}\sigma_{2t}\,dt}
{\sqrt{\int_0^T\sigma_{1t}^2\,dt\int_0^T\sigma_{2t}^2\,dt}}.
$$

This is an integrated covariance normalized by integrated variances. It is generally not the ordinary time average of instantaneous $\rho_t$. Any annualization should be applied consistently to all variance and covariance rates; it leaves the correlation unchanged.

## The univariate likelihood as an implementable objective

Suppose a synchronized scalar log-price series has $n+1$ levels and $n$ successive returns $Y$. Under the working model of constant variance rate $v$, independent Gaussian level noise of variance $a^2$, and equal spacing $\Delta$, the return covariance matrix is tridiagonal:

$$
\Omega(v,a^2)_{jj}=v\Delta+2a^2,
\qquad \Omega(v,a^2)_{j,j+1}=\Omega(v,a^2)_{j+1,j}=-a^2.
$$

All other entries are zero. Maximize equation (1),

$$
\ell(v,a^2)=-\frac12\log\det\Omega-
\frac12Y^\top\Omega^{-1}Y-\frac n2\log(2\pi).
$$

The economically relevant parameter region has nonnegative noise variance and positive efficient-price variance, with a positive definite return covariance matrix. The source gives an explicit inverse in Appendix A.2, but one need not form a dense inverse to implement the same objective. A tridiagonal factorization computes both the log determinant and the quadratic form efficiently. For example, with $d=v\Delta+2a^2$ and $b=-a^2$, an $LDL^\top$ factorization uses $D_1=d$ and $D_j=d-b^2/D_{j-1}$, followed by triangular solves. This computational reformulation is an implementation suggestion, not a separate estimator introduced by the authors.

For irregular generalized sampling times, the quasi-likelihood uses the mean interval $\bar\Delta$, with observation order preserved. Reordering observations or inserting repeated previous prices can change the error's autocorrelation structure and invalidate the intended objective. The article emphasizes that losing some observations is preferable to adding artificial ones that change this structure.

Theorem 1 establishes consistency under stochastic volatility even though the optimized likelihood assumes constant volatility. If $a$ is the noise standard deviation, the scaled variance-rate estimate has mixed-Normal asymptotic variance

$$
V_v=\frac{5a\int_0^T\sigma_t^4\,dt}
{T\left(\int_0^T\sigma_t^2\,dt\right)^{1/2}}
+\frac{3a\left(\int_0^T\sigma_t^2\,dt\right)^{3/2}}{T^2}.
$$

Specifically, $n^{1/4}(\widehat v-v)$ converges stably to that mixed Normal law. The noise-variance estimate converges at rate $n^{-1/2}$, with asymptotic variance $2a^4+\operatorname{Cum}_4(U)=EU^4-a^4$. Their leading estimation errors are asymptotically independent. The fourth cumulant vanishes for Gaussian noise, but Gaussian noise is not required for consistency.

## Covariance from sums and differences

After synchronization, form four scalar series: asset 1, asset 2, their sum, and their difference. Fit the univariate likelihood to each. If the resulting variance-rate estimates are $\widehat v_1$, $\widehat v_2$, $\widehat v_+$, and $\widehat v_-$, equations (2)–(3) give

$$
\widehat c_{12}=\frac{\widehat v_+-\widehat v_-}{4},
\qquad
\widehat r_{12}=\frac{\widehat c_{12}}{\sqrt{\widehat v_1\widehat v_2}}.
$$

These four estimates share data and are statistically dependent. Their standard errors cannot be combined as if they came from independent fits.

Remark 2 proposes a rescaled alternative. For $0<\gamma<1$, fit the variance of $\gamma X_1+(1-\gamma)X_2$ and $\gamma X_1-(1-\gamma)X_2$, and divide their difference by $4\gamma(1-\gamma)$. The unweighted construction corresponds to $\gamma=1/2$. One suggested data-driven weight is $\widehat v_2/(\widehat v_1+\widehat v_2)$. The simulation labels its modified construction QMLE*. The paper does not establish that this particular plug-in choice minimizes every finite-sample criterion.

For more than two assets, compute the pairwise entries and assemble a symmetric matrix. The source explicitly warns that the resulting matrix need not be positive semidefinite, and proposes projection onto that cone as one possibility. Such a projection changes the estimates. Record its norm and convention if used, and keep the original matrix for diagnosis. Similarly, clipping a correlation outside $[-1,1]$ conceals an estimation issue unless the adjustment is declared.

## Generalized synchronization and refresh time

A generalized sampling-time sequence $0=\tau_0<\tau_1<\cdots<\tau_n=T$ must place at least one observation of every included asset in each interval $(\tau_{j-1},\tau_j]$, while its maximum interval length tends to zero asymptotically. Select one observation for each asset from each interval and treat those selected observations as a synchronized vector. The selection need not always be the last tick. The essential restriction is that a new observation of each asset exists in every interval.

The refresh-time procedure is particularly easy to reconstruct. Starting after the last refresh time, locate the first new observation of every asset. Set the next refresh time equal to the latest of those first arrivals. For each asset select its last observation at or before that new refresh time; because every asset has traded, this selected tick lies after the previous refresh time. Repeat until the available common observation period is exhausted. Endpoint handling and a common starting level should be specified when implementing actual daily files.

This procedure avoids arbitrary regular-grid bandwidth selection and retains as many synchronized intervals as possible within this class, according to Remark 3. It nevertheless discards data, especially for a very liquid asset paired with a less liquid one. The liquid asset's selected price may also systematically precede the illiquid asset's price.

To examine that asymmetry, the paper considers lead-constrained sampling. To make asset 1 lead, find the first asset-1 observation after the previous sampling time, then the first asset-2 observation after it, and use the latter time as the next boundary. Repeat with the opposite lead order and average the resulting estimates. This is a sensitivity check for synchronization-induced staleness, not a test for an economic causal lead–lag relation.

Assumption 4 is stronger than merely having many observations. The generalized sampling intervals must be independent and identically distributed, independent of prices, volatilities, and noise, with mean $\bar\Delta$. Under these conditions Theorem 3 establishes errors of order $\bar\Delta^{1/4}$ for variance, covariance, and correlation. Trading intensity that responds to volatility or news does not automatically meet these assumptions. The empirical application contains substantial intraday activity variation, so the theorem should be treated as an idealization rather than a literal description of every tick.

The synchronous Theorem 2 gives an explicit mixed-Normal central limit theorem. The asynchronous Theorem 3 establishes consistency and the rate, but does not assert that its limiting variance is exactly the synchronous formula. This distinction is essential before attaching confidence intervals to empirical asynchronous estimates.

## Reconstructing the synchronous uncertainty calculation

Appendix A.1 derives the joint asymptotic covariance of the four likelihood variance estimates and then applies the delta method. A compact equivalent way to organize its formula is to consider two linear-combination processes $P$ and $Q$. Let $s_P^2$ and $s_Q^2$ be their average variance rates, $a_P$ and $a_Q$ their level-noise standard deviations, $b_{PQ}$ their level-noise covariance, and $h_{PQ}(t)$ their instantaneous efficient-price covariance. For nondegenerate noise and variance parameters, the appendix's cross-covariance formula can be written

$$
F(P,Q)=\frac{8a_Pa_Q}{T^{3/2}(a_Qs_P+a_Ps_Q)^3}
\left[
(a_Q^2s_P^2+a_P^2s_Q^2+3a_Pa_Qs_Ps_Q)\int_0^T h_{PQ}(t)^2\,dt
+2b_{PQ}s_P^2s_Q^2\int_0^T h_{PQ}(t)\,dt
+\frac{b_{PQ}^2s_P^3s_Q^3T}{a_Pa_Q}
\right].
$$

This is a restatement of the appendix for $n^{1/4}$-scaled estimation errors, not the variance of the unscaled estimate. The diagonal case reduces to the univariate formula above. For the four linear combinations used here, the required noise covariances and efficient-price covariance functions follow by ordinary bilinear transformations of the two-asset covariance matrices.

Order the four fitted variance rates as $(v_1,v_+,v_-,v_2)$ and construct their $4\times4$ asymptotic covariance matrix $A$ from $F$. The covariance gradient is $g_c=(0,1/4,-1/4,0)^\top$. If $c=(v_+-v_-)/4$, the correlation gradient is

$$
g_r=\left(-\frac{c}{2v_1^{3/2}v_2^{1/2}},
\frac1{4\sqrt{v_1v_2}},
-\frac1{4\sqrt{v_1v_2}},
-\frac{c}{2v_1^{1/2}v_2^{3/2}}\right)^\top.
$$

The scaled limiting variances are $g_c^\top A g_c$ and $g_r^\top A g_r$; ordinary standard errors carry an additional $n^{-1/4}$ factor. This presentation makes the dependence between the four fits explicit. It also exposes a feasibility requirement: integrated squared covariance functions in $F$ are latent and require estimation. The paper gives the theoretical formula and a simulation illustration, but does not supply a complete ready-to-run empirical estimator for every nuisance integral or an asynchronous confidence-band procedure.

The proof separates efficient-price martingale terms, price–noise cross terms, and pure-noise quadratic forms in the likelihood scores. Fourth-order noise cumulants enter intermediate calculations but are lower order for the volatility-rate covariance. A Taylor expansion of the score then yields the joint limit. For asynchronous data, Appendix A.2 modifies the true return covariance to include overlapping latent-price intervals, proves the score approximation uniformly, establishes identification of the average variance, and recovers the convergence rate. The argument depends on preserving the selected observations' temporal ordering and noise structure.

## Monte Carlo design

Section 4 uses 10,000 simulations. The efficient log prices have zero drift and Heston-type variance processes with jumps in variance:

$$
dX_{it}=\sigma_{it}\,dW_{it},
\qquad
d\sigma_{it}^2=\kappa_i(\bar\sigma_i^2-\sigma_{it}^2)dt
+s_i\sigma_{it}\,dB_{it}+\sigma_{it-}^2J_t^V\,dN_{it}.
$$

The specified Brownian covariances are $d\langle W_i,B_j\rangle_t=\delta_{ij}\rho_i dt$ and $d\langle W_1,W_2\rangle_t=\rho dt$. Initial variance is drawn from a Gamma distribution with shape $2\kappa_i\bar\sigma_i^2/s_i^2$ and scale $s_i^2/(2\kappa_i)$. The variance-jump multiplier is lognormal, $J^V=\exp Z$, with the printed normal parameters $(\theta_i,\mu_i)$, and the Poisson process has intensity $\lambda_i$. The source does not make the variance-versus-standard-deviation convention for the second normal parameter explicit in the sentence defining it; reproduce that convention transparently rather than guessing silently.

| Parameter | Asset 1 | Asset 2 |
|---|---:|---:|
| Initial log price | $\log100$ | $\log40$ |
| $\kappa_i$ | 6 | 4 |
| $s_i$ | 0.5 | 0.3 |
| $\bar\sigma_i^2$ | 0.16 | 0.09 |
| Leverage $\rho_i$ | −0.6 | −0.75 |
| Jump intensity $\lambda_i$ | 12 | 36 |
| Log-jump mean $\theta_i$ | −5 | −6 |
| Second log-jump parameter $\mu_i$ | 0.8 | 1.2 |
| Noise standard deviation $a_i$ | 0.005 | 0.001 |

Cross-price Brownian correlation is $\rho=0.5$. Paths are generated by Euler approximation. The experiment description says that time intervals are exponential but immediately describes the data as equally spaced. Those statements conflict literally. The natural distinction between a common grid and an equally spaced grid should be preserved: synchronized exponential times are possible, equally spaced exponential intervals are not. Table 2 identifies *average* spacings of two and thirty seconds; the exact time-grid implementation and seed are not supplied.

The complete common sample is randomly thinned by Bernoulli trials, retaining approximately one half of asset 1 and two thirds of asset 2. Independent Gaussian noise is then added, refresh-time synchronization is applied, and the four quasi-likelihoods are fitted. The mean full-sample count is 11,700 at two seconds and 781 at thirty seconds, consistent with a roughly 6.5-hour simulation horizon. Calendar-to-model time conversion and Euler boundary handling should be documented in a reproduction.

Comparators are two-scale realized covariance, a multivariate realized kernel, and two ideal benchmarks. Full-data realized covariance uses the complete noise-free synchronized path. Hayashi–Yoshida uses asynchronous but noise-free observations. They therefore have informational advantages over the noisy-data estimators and should not be described as directly deployable noisy-data competitors.

The two-scale covariance uses lag-$S$ cross-products divided by $S$, for $S=K,J$, and subtracts $(\bar n_K/\bar n_J)$ times the fine-scale statistic, where $\bar n_S=(n-S+1)/S$ and $1\leq J\ll K=O(n^{2/3})$. The article does not report a complete numerical choice of both scales for every experiment. The kernel uses Parzen weights $1-6x^2+6x^3$ on $[0,1/2]$ and $2(1-x)^3$ on $[1/2,1]$, with endpoint averaging. Its bandwidth is the maximum of the two univariate choices, $H_i=3.5134\xi_i^{4/5}n^{3/5}$, where $\xi_i^2=a_i^2/\sqrt{T\int\sigma_{it}^4dt}$. True latent quantities are used for this bandwidth, an oracle advantage explicitly acknowledged in the source. The endpoint-averaging count is introduced but not fixed numerically in the description.

## Simulation findings without overstating efficiency

At the two-second average spacing, the mean synchronized count is 5,573, compared with raw retained counts of 5,853 and 7,801. Average staleness is 1.92 seconds. Table 2's covariance results are:

| Method | Mean estimated covariance rate | RMSE |
|---|---:|---:|
| Noise-free full-data realized covariance | 0.0583 | 0.0018 |
| QMLE | 0.0584 | 0.0112 |
| Multivariate realized kernel | 0.0584 | 0.0147 |
| Two-scale covariance | 0.0569 | 0.0148 |
| Noise-free Hayashi–Yoshida | 0.0584 | 0.0028 |
| QMLE* | 0.0582 | 0.0108 |

At thirty seconds, QMLE covariance is 0.0582 with RMSE 0.0241, the kernel 0.0575 with 0.0270, two-scale covariance 0.0543 with 0.0256, and QMLE* 0.0575 with 0.0232. The corresponding synchronized count is 372 and average staleness 28.7 seconds. QMLE has a useful advantage in this calibration, while its error remains substantially larger than that of the noise-free benchmarks.

The diagonal comparisons reveal an additional issue with using one multivariate bandwidth for assets with different noise levels. At two seconds, the asset-1 variance estimate is 0.1603 for QMLE, 0.1967 for the kernel, and 0.1565 for two-scale covariance; their RMSEs are 0.0242, 0.0466, and 0.0306. Asset 2 has much less noise, and the same methods give 0.0906, 0.0920, and 0.0883. Rate optimality does not imply uniformly minimal finite-sample variance across every configuration.

Figure 2 compares standardized synchronous covariance and correlation estimates with a standard Normal density, using one-second average spacing. It supports the synchronous distribution approximation in the simulated design. It does not establish coverage for the asynchronously sampled empirical currency series.

## Currency-futures sample and processing

The empirical application covers Australian dollar, Canadian dollar, euro, British pound, Japanese yen, and Swiss franc futures on CME, quoted as US-dollar values of a unit of foreign currency. The period is January 1, 2007 through June 30, 2009. Cleaned transaction data are identified as available from Tick Data, Inc.; automatic contract rolling creates continuous records, but the exact roll trigger and adjustment convention are not specified.

All timestamps use exchange time in Chicago. A trading day runs from 5 p.m. on the preceding date to 4 p.m. on the current date, excluding the one-hour closure and its possible reopening jump. The study removes Saturdays and Sundays, US federal holidays, the day after Thanksgiving, December 24–26, and December 31–January 2, leaving 618 days. Multiple trades at an identical timestamp are replaced by their average price. The source does not supply the complete vendor cleaning specification, trade-condition filters, missing-day rules, or contract identifiers.

Average daily trade counts are 6,142 for AUD, 5,898 for CAD, 17,097 for EUR, 10,508 for GBP, 11,685 for JPY, and 6,284 for CHF. Lag-one log-return correlations range from −0.0651 to −0.1186, whereas lag-two and lag-three correlations are much smaller. This is compatible with an MA(1)-like observation-error effect, but does not prove all the independence assumptions. Reported average intertrade intervals appear calculated over 24 hours, while the described trading session lasts 23 hours; an implementation should explicitly choose the session denominator rather than infer it from rounded table entries.

Pairwise refresh-time synchronization supplies daily estimates. Figure 4 plots five-day moving averages for presentation. The caption does not state whether that smoother is trailing or centered, so it should not be turned into a predictive trading signal without specifying timing.

## Empirical results and robustness

Table 5's average correlations are all positive. The strongest is EUR–CHF at 0.6409, followed by EUR–GBP at 0.4703 and GBP–CHF at 0.4051. AUD–JPY is only 0.0061 and CAD–JPY 0.0203. These are averages across the sample; individual days can have negative correlations, as the plots show. Correlations involving JPY decline during the most stressed portions of the crisis. The authors discuss carry-trade unwinds and currency roles as possible explanations, without identifying a causal model that isolates these mechanisms.

The lead-constrained synchronization check produces similar averages: EUR–CHF is 0.6475, AUD–JPY 0.0064, and CAD–JPY 0.0201. Table 5 puts refresh-time estimates above the diagonal and averages of the two lead-constrained estimates below it. The apparent asymmetry is therefore a comparison of procedures, not an asymmetric covariance matrix.

The intraday check separates 5 p.m.–7 a.m., 7 a.m.–11 a.m., and 11 a.m.–4 p.m., all Chicago time. The surrounding prose mistakenly prints “11 p.m.” in two places; Table 6 and the description of the active US–European overlap identify 11 a.m. as the intended boundary. For EUR–JPY the three mean correlations are 0.1801, 0.2663, and 0.1939; for GBP–JPY they are 0.0692, 0.1746, and 0.0929. The middle session is often higher, but not universally: EUR–CHF is 0.6685, 0.6341, and 0.5754. The paper describes some differences as not significant, but the table does not provide standard errors, test statistics, or a multiple-comparison procedure to reproduce those significance statements.

The study is descriptive, with no estimation/validation split, portfolio backtest, transaction costs, or predictive-performance evaluation. Its central contribution is an implementable covariance measurement method and evidence that it behaves sensibly in a crisis-era currency dataset. A faithful reproduction should recover the sample count, session filters, synchronization counts, likelihood estimates, and table averages before drawing economic conclusions from the plotted correlations.
