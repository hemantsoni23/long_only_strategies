# A Tale of Two Time Scales: Determining Integrated Volatility With Noisy High-Frequency Data

Lan Zhang, Per A. Mykland, and Yacine Aït-Sahalia. *Journal of the American Statistical Association* 100(472), December 2005, 1394–1411. DOI: 10.1198/016214505000000169.

Source: [original PDF](../../Finance/RealizedVariance_ZhangMyklandAitSahalia_2005.pdf). The source has 18 pages, including the technical appendices. References below use printed article pages and equation numbers. This note describes the paper's original two-scale estimator; subsequent multi-scale refinements are outside its scope.

## Why this matters and what is new

The paper changes the answer to an important measurement question: should an analyst throw away high-frequency prices to avoid market microstructure noise? With ordinary realized variance, finer sampling eventually makes the estimate worse. Noise in price levels becomes first differences in returns, and squaring those returns accumulates a positive bias at every observation. Sampling once every five minutes is a practical compromise, but it is neither a universal optimum nor a consistent solution under fixed nonzero noise.

The innovation is to use two sampling scales for different purposes. Average realized variances across many sparse, interlaced grids to measure the latent price variation with reduced noise. Use all observations to estimate the noise contribution, then subtract the appropriate multiple of that estimate. The resulting two-scale realized variance, usually called TSRV, consistently estimates integrated variance without discarding the high-frequency information. Its original convergence rate is $n^{-1/6}$, slower than the noise-free $n^{-1/2}$ rate but fundamentally different from the inconsistency of uncorrected realized variance.

The paper also derives a sampling-frequency comparison, a finite-sample correction, asymptotic inference, and a Monte Carlo experiment. These are measurement results, not evidence of trading profitability. An implementation must distinguish the raw bias-corrected estimator, its finite-sample adjusted version, and the uncorrected subgrid average; their formulas and sampling errors differ.

## Observation model, target, and assumptions

On a fixed interval $[0,T]$, the latent log price follows a continuous Itô process

$$
dX_t=\mu_t\,dt+\sigma_t\,dB_t.
$$

Observations at $0=t_0<\cdots<t_n=T$ are

$$
Y_{t_i}=X_{t_i}+\varepsilon_i.
$$

There are $n+1$ price observations and $n$ full-grid returns. The errors are independent and identically distributed, have zero mean and variance $\eta^2=E(\varepsilon_i^2)$, and are independent of the entire efficient-price process. Here $\eta^2$ denotes noise variance; the article uses other letters for some of its asymptotic variance quantities. This note keeps those concepts separate.

The estimand is

$$
IV_T=\langle X,X\rangle_T=\int_0^T\sigma_t^2\,dt.
$$

Despite the paper's use of “integrated volatility,” this is a variance quantity, in squared log-return units. Its square root is integrated standard deviation. The companion integrated quarticity is

$$
IQ_T=\int_0^T\sigma_t^4\,dt.
$$

The high-frequency asymptotics increase the number of observations over fixed $T$, rather than extending the time horizon. The principal limit results assume continuous drift and diffusion coefficients, local regularity, and volatility bounded away from zero, with localization used in the proofs. Sampling intervals have maximum order $1/n$, and the subgrids are regularly allocated by observation index. The appendix's Condition E imposes a filtration regularity condition that permits a stable martingale central limit theorem; Brownian filtrations provide the motivating example. Stable convergence makes the limiting Gaussian noise independent of the original price process while allowing its conditional variance to depend on the realized volatility path.

The model allows stochastic volatility and leverage within the efficient-price process. It does not automatically accommodate serially correlated observation noise, price-dependent noise, bid–ask discreteness with arbitrary dependence, or irregular endogenous sampling. These are substantive assumptions, not cosmetic conveniences. Some early variance comparisons require $E\varepsilon_i^4<\infty$. An interesting feature of the final two-scale theorem is that cancellation removes the noise fourth-moment term, allowing that result under a finite noise second moment.

## Why using every return fails without correction

Write the full-grid realized variance as

$$
RV_{\mathrm{all}}=\sum_{i=1}^n(Y_{t_i}-Y_{t_{i-1}})^2.
$$

Conditional on the efficient-price path,

$$
E(RV_{\mathrm{all}}\mid X)=RV_X+2n\eta^2,
\qquad RV_X=\sum_{i=1}^n(\Delta X_i)^2.
$$

Thus $RV_X$ approaches $IV_T$, but the noise bias grows linearly with $n$. The dominant conditional variance is $4nE\varepsilon_i^4$, with a correction involving $8RV_X\eta^2-2\operatorname{Var}(\varepsilon_i^2)$; see the early noise decomposition and its appendix proof. Adjacent observed returns share the same level error with opposite signs, so treating their squared errors as independent gives the wrong variance.

The very dominance of noise makes

$$
\widehat{\eta^2}=\frac{RV_{\mathrm{all}}}{2n}
$$

a consistent estimator of noise variance. This is not an estimator of efficient-return variance. Under the fourth-moment assumptions, its $\sqrt n$ asymptotic variance is $E\varepsilon_i^4$. A corresponding fourth-moment estimate can be built from fourth powers of observed returns:

$$
\widehat{E\varepsilon^4}=\frac{1}{2n}\sum_{i=1}^n(\Delta Y_i)^4-3(\widehat{\eta^2})^2.
$$

Subtracting another $(\widehat{\eta^2})^2$ gives an estimate of $\operatorname{Var}(\varepsilon_i^2)$. These formulas rely on the independent, identically distributed level-noise model. They should not be transferred unchanged to correlated return noise.

## Sparse sampling and what its optimum actually means

Suppose only $m$ regularly spaced returns are used. The leading bias is $2m\eta^2$, while the efficient-price discretization variance is $2T IQ_T/m$. The leading mean squared error used for the sparse-sampling comparison is

$$
\operatorname{MSE}_{\mathrm{sparse}}\approx4m^2\eta^4+\frac{2T IQ_T}{m}.
$$

Consequently,

$$
m^*_{\mathrm{sparse}}=\left(\frac{T IQ_T}{4\eta^4}\right)^{1/3}.
$$

Here $\eta^4=(\eta^2)^2$. The comparison uses a small-noise approximation: the optimized number of sparse returns need not increase without bound when noise variance is fixed. It therefore does not turn the uncorrected sparse estimator into a consistent estimator under the paper's principal fixed-noise infill experiment.

For irregular sparse grids, equation (31) introduces the quadratic variation of time, $H(t)$, through accumulated squared time intervals. The discretization variance involves $\int H'(t)\sigma_t^4\,dt$ rather than simply $IQ_T$. This is why an implementation cannot mix calendar-time and transaction-time frequency formulas without checking the grid assumptions.

The optimal frequency depends on both noise and volatility. A five-minute rule has no universal theoretical status here. Higher noise favors fewer returns; higher integrated quarticity favors finer sampling. Since $IQ_T$ is latent, the optimum is an oracle calculation unless a separate estimator or prior-period input is supplied.

## Constructing the interlaced subgrids

Choose an integer $K$ and partition the observation indices into $K$ disjoint grids. Grid $k$, for $k=0,\ldots,K-1$, contains indices

$$
k,\;k+K,\;k+2K,\ldots\leq n.
$$

Calculate the realized variance on each grid using returns between successive observations in that grid. If grid $k$ contains $n_k$ returns, define

$$
RV_{\mathrm{avg}}=\frac1K\sum_{k=0}^{K-1}RV_k,
\qquad
\bar n=\frac1K\sum_{k=0}^{K-1}n_k=\frac{n-K+1}{K}.
$$

The exact $\bar n$ matters for finite-sample correction. Substituting $n/K$ everywhere silently changes edge weights. All grids receive equal weight in the paper's construction; weighting them by return counts produces a different estimator.

The noise bias of the average is $2\bar n\eta^2$. Its leading noise variance is $4(\bar n/K)E\varepsilon^4$, much smaller than using one of the grids alone. However, the latent returns on different grids overlap in calendar time and are strongly correlated. The efficient-price discretization variance is asymptotically

$$
\frac{4T}{3\bar n}IQ_T,
$$

not the variance obtained by pretending the $K$ efficient-price estimates are independent. The factor $4/3$ arises from the triangular pattern of overlap; equations (43)–(50) derive the weights explicitly. For the uncorrected average, the analogous small-noise optimal count is $(T IQ_T/(6\eta^4))^{1/3}$.

## Two-scale correction and finite-sample adjustment

The raw estimator is

$$
\widehat{IV}_{\mathrm{TSRV}}=RV_{\mathrm{avg}}-\frac{\bar n}{n}RV_{\mathrm{all}}.
$$

Both noise contributions have the same expectation, so their difference removes the growing noise bias. The subtraction also removes a small multiple of efficient-price variation. The paper therefore proposes the adjusted version

$$
\widehat{IV}_{\mathrm{adj}}=
\frac{RV_{\mathrm{avg}}-(\bar n/n)RV_{\mathrm{all}}}{1-\bar n/n}.
$$

This is the “first-best” estimator used in the simulation comparison. The adjustment is asymptotically negligible at the principal rate, but materially improves small-sample centering. It is not an assertion of exact finite-sample unbiasedness for every stochastic-volatility path: subgrids omit different pieces at the endpoints.

A related improved noise estimator is

$$
\widehat{\eta^2}_{\mathrm{corr}}=
\frac{RV_{\mathrm{all}}-RV_{\mathrm{avg}}}{2(n-\bar n)}.
$$

For reproducibility, retain raw and adjusted estimates, $n$, $K$, $\bar n$, the two component realized variances, and the noise estimate. This exposes failures caused by indexing or inconsistent units. A negative TSRV can occur in finite samples. The paper's asymptotic theory does not justify silently replacing it with zero; any positivity repair should be separately documented, together with its effect on inference.

## Rate, optimal scale, and confidence intervals

The corrected estimator balances noise error of order $\sqrt n/K$ against discretization error of order $\sqrt{K/n}$. Setting

$$
K\sim c n^{2/3}
$$

balances them and yields the central limit result, for equidistant observations,

$$
n^{1/6}(\widehat{IV}_{\mathrm{TSRV}}-IV_T)
\ \Longrightarrow_{\mathrm{stable}}\ \sqrt{s^2}\,Z,
\qquad
s^2=8c^{-2}\eta^4+\frac43cT IQ_T,
$$

where $Z$ is standard Normal and independent of the original process. The two terms represent residual observation noise and efficient-price discretization, respectively. This conditional, path-dependent variance is not generally replaceable by one unconditional constant.

Minimization with respect to $c$ gives

$$
c^*=\left(\frac{12\eta^4}{T IQ_T}\right)^{1/3}.
$$

The article also discusses minimizing expected variance using an expectation of quarticity. It explicitly leaves the theoretical treatment of using same-day data to choose the optimal scale unresolved; prior data offer a cleaner basis for feasible tuning. A replication should identify whether its $K$ is oracle, prior-period, or estimated from the same interval. Rounding and bounds for $K$ are implementation choices that must be recorded, not hidden behind the asymptotic formula.

Given a consistent estimate of $s^2$, the ordinary standard error of the unscaled estimator is $n^{-1/6}\sqrt{\widehat{s^2}}$. A first-order interval is the estimator plus or minus the appropriate Normal quantile times that standard error. Normal intervals need not remain positive. Transformations or truncations change the procedure and are not supplied as universal fixes by this paper.

There is a normalization issue worth preserving when implementing the higher-order variance correction. Equation (59) defines the leading variance for the *scaled* statistic, while equation (60) gives the actual noise variance with an $n^{-1/3}$ leading factor. Equation (61), as printed, adds the second-order correction to $s^2$ without that factor. To use the same $s^2$ for the variance of the unscaled estimator requires $n^{-1/3}s^2$. This is an algebraic reading of the displayed formulas, not evidence that the authors' simulation code used the printed normalization.

More explicitly, if $B=8RV_{X,\mathrm{avg}}\eta^2-2\operatorname{Var}(\varepsilon^2)$, the reconciled expansion for ordinary estimator variance is $n^{-1/3}s^2+n^{-2/3}c^{-1}B$. For the $n^{1/6}$-scaled error it is instead $s^2+n^{-1/3}c^{-1}B$. The efficient-price subgrid average in $B$ is latent, so writing the correction does not itself supply a fully feasible plug-in procedure.

## The feasible variance construction in Section 6

The paper supplies more than the instruction “estimate quarticity.” It compares two nested families of subgrids, with $K_1=c_1n^{2/3}$ and $K_2=IK_1=c_2n^{2/3}$. Within each first family grid, retaining every $I$th observation creates the second family. It recommends considering $I=3$ or $4$.

Partition $[0,T]$ into $M$ segments. Calculate cumulative raw two-scale estimates on both families and take their increments over each segment, denoted $\Delta\widehat{IV}_{1,m}$ and $\Delta\widehat{IV}_{2,m}$. Then form

$$
\widehat{s_0^2}=n^{1/3}\sum_{m=1}^M
(\Delta\widehat{IV}_{1,m}-\Delta\widehat{IV}_{2,m})^2.
$$

In the article's sequential limits, first $n\to\infty$ and then $M\to\infty$, equation (69) gives

$$
s_0^2=8\eta^4(c_1^{-2}+c_2^{-2}-c_1^{-1}c_2^{-1})
 +(\sqrt{c_1}-\sqrt{c_2})^2Tq,
\qquad q=\frac43 IQ_T.
$$

Solve this equation for $q$ after estimating $\eta^4$, then insert the result into $s^2=8c^{-2}\eta^4+cTq$. With $c_1=c$, the paper simplifies the construction to approximately $1.866\widehat{s_0^2}-3.611c^{-2}\widehat{\eta^4}$ for $I=3$, and $\widehat{s_0^2}+1.5c^{-2}\widehat{\eta^4}$ for $I=4$. These are estimates of the scaled asymptotic variance. The finite-sample choice of $M$ is not fixed by the asymptotic argument, and the subtractive $I=3$ formula can produce an inadmissible estimate in finite samples. Reporting such an outcome is preferable to silently altering the method.

The discussion also allows noise variance to change across a fixed number of time segments, with local corrections. Applying one pooled noise estimate couples the errors across segments. That distinction matters when aggregating intraday estimates or attempting to attach independent-segment standard errors.

## Monte Carlo design and exact numerical comparison

Section 7 uses 25,000 simulated paths over a 6.5-hour trading day with one-second discretization, giving $n=23,400$. Time is in years, with the day represented as $T=1/252$. The latent process is a Heston-type stochastic-volatility model:

$$
dX_t=(\mu-v_t/2)dt+\sqrt{v_t}\,dB_t,
\qquad
dv_t=\kappa(\alpha-v_t)dt+\gamma\sqrt{v_t}\,dW_t.
$$

The parameters are $\mu=0.05$, $\kappa=5$, $\alpha=0.04$, $\gamma=0.5$, and $\operatorname{Corr}(dB_t,dW_t)=-0.5$. Independent Gaussian level noise has standard deviation $0.0005$, approximately five basis points in log price. Paths are simulated by Euler discretization. The initial variance distribution, random seed, handling of any negative Euler variance, and all operational details of pilot tuning are not specified sufficiently in the experiment description to reproduce the original random draws exactly.

Five methods are compared: all-data realized variance; fixed five-minute sampling; optimally sparse sampling; the uncorrected subgrid average; and adjusted TSRV. The five-minute scheme uses 78 returns. The latent simulated path supplies the realized integrated-variance target and oracle quantities used in theoretical comparisons; this is not a live-data experiment with fully estimated latent inputs.

Table 2 reports the following absolute-error results. Values retain squared log-return units for bias and root mean squared error; variance has the square of those units.

| Estimator | Empirical bias | Empirical variance | Empirical RMSE |
|---|---:|---:|---:|
| All observations | $1.1699\times10^{-2}$ | $1.791\times10^{-8}$ | $1.1699\times10^{-2}$ |
| Five-minute sparse | $3.89\times10^{-5}$ | $1.4414\times10^{-9}$ | $5.437\times10^{-5}$ |
| Optimally sparse | $2.18\times10^{-5}$ | $1.59\times10^{-9}$ | $4.543\times10^{-5}$ |
| Subgrid average | $1.926\times10^{-5}$ | $9.41\times10^{-10}$ | $3.622\times10^{-5}$ |
| Adjusted TSRV | $2\times10^{-8}$ | $9\times10^{-11}$ | $9.4\times10^{-6}$ |

The corresponding asymptotic RMSE predictions are $1.1700\times10^{-2}$, $5.442\times10^{-5}$, $4.546\times10^{-5}$, $3.618\times10^{-5}$, and $8.9\times10^{-6}$. Their closeness supports the approximations in this particular calibration. Adjusted TSRV's empirical RMSE is about 5.8 times smaller than the five-minute estimator's. That comparison is not a claim that all practical datasets yield the same improvement.

The table's relative-error rows require care. It defines relative error using $(\widehat{IV}-IV)/IV$, so a reported relative RMSE of $0.065$ corresponds to 6.5%, not 0.065%. The five methods' relative RMSE entries are 340, 1.24, 0.37, 0.28, and 0.065. The prose uses percentage language inconsistently. Interpreting these entries as raw ratios is an inference from the stated normalization, supported by the first-best relative variance of 0.0043, whose square root is approximately 0.0656; treating 0.065 as a literal percent would not be consistent with that arithmetic. Its variance calculation also uses conditioning bins in integrated variance and quarticity; it is not simply the unconditional sample variance of every estimation error pooled together. Bin implementation details should be matched or disclosed when reproducing the comparison.

Figure 1 shows the expected U-shaped tradeoff for uncorrected sparse sampling in the calibration, with the minimum around several minutes. Figure 2 examines the distribution after standardization by the asymptotic variance. These figures support the finite-sample approximation under the chosen stochastic-volatility and independent-noise design. The paper does not provide an empirical asset-universe test, a transaction-cost strategy, or a confidence interval for a universal performance advantage.

## A closer look at the cancellation and overlap calculations

The bias correction also has a useful algebraic implementation check. Ignoring endpoint terms for this leading-order calculation, the noise-only part of the subgrid average is

$$
\frac{2}{K}\sum_i\varepsilon_i^2-
\frac{2}{K}\sum_i\varepsilon_i\varepsilon_{i-K}.
$$

The approximately $1/K$ multiple of full-grid realized variance has noise component

$$
\frac{2}{K}\sum_i\varepsilon_i^2-
\frac{2}{K}\sum_i\varepsilon_i\varepsilon_{i-1}.
$$

Their difference leaves approximately $2/K$ times the difference between the lag-one and lag-$K$ product sums. The potentially problematic centered sum of squared level errors has disappeared. Each remaining product involves two distinct independent errors, so its second moment is $(E\varepsilon^2)^2=\eta^4$. For distinct lags with $K>1$, the leading cross-covariances vanish under centered independent noise, yielding approximately $8n\eta^4/K^2$. With $K=cn^{2/3}$, multiplying this ordinary variance by $n^{1/3}$ gives $8c^{-2}\eta^4$, exactly the noise contribution to the central limit theorem.

This calculation explains both the robustness to a missing fourth noise moment in the final theorem and the failure of a naive independent-return calculation. It does not say that all squared observed-return moments exist, or that every preliminary fourth-moment-based confidence correction remains usable with heavy-tailed noise. The final estimator's cancellation is more specific than a blanket moment assumption on every intermediate statistic.

The discretization contribution can also be checked locally without treating the subgrids as independent. For constant volatility and two overlapping Brownian return intervals $A$ and $B$, the covariance of their squared returns is twice the squared covariance of the returns themselves. If the overlap length is $\ell$, this equals $2\sigma^4\ell^2$. Shifting a length-$K$ interval by one original observation reduces the overlap gradually, producing weights proportional to $1-j/K$. Summing their squares, including both directions of overlap, gives the limiting $4/3$ coefficient. The proof replaces locally constant volatility by the actual volatility path, turning $\sigma^4T$ into integrated quarticity.

For non-equidistant observations, the weights in equation (43) use the actual neighboring time increments rather than a simple evenly spaced triangle. Equation (47) defines a weighted quarticity sum and equation (48) assumes its convergence to a limiting random quantity. Only with the equidistant special case does equation (50) identify that quantity as $4IQ_T/3$. Thus the headline equidistant variance formula is not a license to ignore long gaps in a transaction-time series. One may retain the general weighted expression or explicitly construct a grid satisfying the special-case assumptions, while acknowledging any interpolation-induced change in noise dependence.

## Reproduction checks at the estimator level

An implementation can reproduce the estimator separately from reproducing all the inference choices. First, keep the $n+1$ input prices in observation order and calculate the $n$ successive returns once. For each grid offset, use only pairs whose two indices exist in that grid; the total number of such pairs must be $n-K+1$. This identity is a simple way to catch an extra endpoint, omitted offset, or confusion between the number of prices and returns. Calculate $\bar n$ from those actual counts and verify it against $(n-K+1)/K$.

Second, preserve the separation between two units of time. The index gap $K$ counts observations, while $T$ is the model's elapsed time in the units used for $\sigma$ and $IQ$. The simulation has 23,400 seconds of recorded activity but uses a trading day of $1/252$ year for its model horizon. Inserting 23,400 as $T$ while retaining annualized Heston parameters would change the model, not merely improve numerical precision.

Third, test the algebra on input perturbations. Adding a common constant to every log price must leave every statistic unchanged. Multiplying all log-price increments and noise by a constant must multiply variance estimates by its square. Setting $K=1$ makes the raw subtraction degenerate and the adjusted denominator vanish, so the useful estimator requires more than one grid. At the other extreme, grids with almost no returns lose the dense-subgrid approximation. The asymptotic requirements $K\to\infty$ and $K/n\to0$ express those two constraints simultaneously.

Finally, compare Monte Carlo errors with each path's own latent integrated variance. Comparing every estimate with the unconditional mean variance would mix estimator error with genuine path-to-path volatility variation. Likewise, a relative error divides by that path's integrated variance; it places much more weight on low-variance paths than an absolute error criterion. These distinct loss functions explain why the paper reports both absolute and relative comparisons and why their estimator rankings or improvement ratios need not be numerically identical.

## Proof mechanism and limits of generalization

The appendices explain why subtraction works beyond subtracting expected biases. Squared observed returns decompose into efficient-return squares, noise squares, and price–noise cross products. The full-grid and averaged-grid statistics share a large component involving sums of $\varepsilon_i^2$. Subtracting the estimated bias cancels that component. The remaining noise fluctuation is driven by products of distinct level errors, producing the $8\eta^4$ asymptotic contribution and explaining why the final variance need not contain $E\varepsilon^4$.

The efficient-price component is a martingale discretization error. Because the grids overlap, its quadratic variation contains squared triangular overlap weights. Their limit generates $4/3$ in the equidistant case. Endpoint discrepancies have smaller order when $K/n\to0$. Localization and martingale central limit arguments then combine the asymptotically independent noise and discretization components. These are the essential mechanisms to preserve if modifying the method; merely retaining a bias subtraction does not establish the same standard error under a new observation model.

The concluding discussion notes that with price jumps, realized quadratic variation includes the sum of squared jumps. Consistency for that total quantity is different from estimating continuous integrated variance. The continuous-model central limit theorem should not be reused unchanged after adding jumps. Similarly, correlated noise invalidates the simple $2n\eta^2$ bias and the exact cancellation calculations, and price-dependent sampling may invalidate the time-grid arguments.

A faithful replication should first recover the simulation's all-data noise explosion, then the sparse-frequency tradeoff, then the improved centering and RMSE of adjusted TSRV. It should retain the raw components, document units and tuning inputs, and report finite-sample failures of variance or positivity estimates. The practical lesson is to use high-frequency observations to estimate both the signal and its contamination, with uncertainty tied to the sampling scheme and the noise model.
