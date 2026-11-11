# Inference and Stochastic Volatility

Alireza Javaheri, *Wilmott magazine*, technical article, pp. 56–63. Source: [Javaheri_  Inference and Stochastic Volatility_2007.pdf](<../../Finance/Javaheri_  Inference and Stochastic Volatility_2007.pdf>), eight PDF pages. The filename supplies 2007, but the displayed article pages do not establish an issue date or DOI.

## Why this matters

Historical-price estimation of a stochastic-volatility model can produce volatility-of-volatility and return/variance correlation estimates very different from option-implied values. Such discrepancies are often interpreted as model misspecification or potential trading opportunities. This article asks a prior question: are the historical estimates precise enough to support that interpretation?

The contribution is a set of controlled Heston-model simulations that separates one-parameter estimation, joint estimation, longer observation histories, higher sampling frequency, and repeated-path sampling distributions. It demonstrates that a filter can recover a plausible volatility level while estimating the parameters governing volatility innovations very poorly. Its strongest evidence is the sampling-distribution experiment, which reveals uncertainty hidden by a single optimized parameter vector.

The study does not supply a new exact likelihood estimator or a formal consistency proof. It uses approximate filtered likelihoods and refers to an earlier filtering paper for implementation details. Claims about eventual consistency therefore need to be distinguished from the finite Monte Carlo evidence actually presented.

## Model, units, and simulation law

The square-root stochastic-variance model is

$$
\frac{dS_t}{S_t}=\mu_Sdt+\sqrt{v_t}\,dB_t,
\qquad dv_t=(\omega-\theta v_t)dt+\xi\sqrt{v_t}\,dZ_t,
\qquad d\langle B,Z\rangle_t=\rho\,dt.
$$

Variance $v_t$ is annualized. The speed of variance mean reversion is $\theta$, its long-run level is $\omega/\theta$, and $\xi$ scales innovations in variance. The correlation $\rho$ controls leverage-type co-movement between price and variance shocks. The experiment treats $\mu_S=0.025$ as known and estimates $\Psi=(\omega,\theta,\xi,\rho)$.

The displayed discrete equations are Euler updates for variance and log price:

$$
\log S_{k+1}=\log S_k+(\mu_S-v_k/2)\Delta+\sqrt{v_k\Delta}\,B_k,
$$

$$
v_{k+1}=v_k+(\omega-\theta v_k)\Delta+\xi\sqrt{v_k\Delta}\,Z_k,
$$

with independent shock pairs over time, standard Gaussian marginals, and contemporaneous correlation $\rho$. Daily experiments use $\Delta=1/252$. The true parameter vector is $(0.10,10.0,0.03,-0.50)$. Its long-run variance is 0.01, corresponding to 10% annualized volatility, and its variance mean-reversion half-life is $\log 2/10\approx0.0693$ years. Those last two quantities are direct implications of the specified parameters, not separately estimated results.

The source does not give a random seed, initial variance, exact positivity treatment for the Euler scheme, or source code. Even when the continuous process has nonnegative variance, Euler simulation can require a rule when a discretized value becomes negative. Those missing choices matter for exact reproduction. The favorable positivity parameters here do not eliminate the need to specify the algorithm.

## Estimation procedure and the one-parameter experiment

The author applies filtered maximum likelihood using an extended Kalman filter (EKF), unscented Kalman filter (UKF), and two particle-filter variants labeled EPF and UPF. Particle-filter results in Table 3 use 1,000 simulations. The article refers readers to Javaheri, Lautier, and Galli's earlier filtering work for filter definitions. It does not restate every transition/observation covariance update, proposal, resampling rule, sigma-point parameter, likelihood normalization, or optimizer stopping condition.

In the first experiment, a simulated path has 5,000 daily observations. All parameters except the one being estimated are fixed at their true values. These are four separate conditional estimation exercises, not a joint four-parameter estimate. The stated starting vector is $(0.15,15,0.02,-0.50)$, with the relevant component used as the initial point for its corresponding optimization.

| Filter | Estimated $\omega$ | Estimated $\theta$ | Estimated $\xi$ | Estimated $\rho$ |
|---|---:|---:|---:|---:|
| EKF | 0.098212 | 10.188843 | 0.052324 | -0.873571 |
| UKF | 0.107281 | 10.089381 | 0.000001 | 0.598434 |
| EPF | 0.098287 | 10.130531 | 0.044437 | -0.827729 |
| UPF | 0.100581 | 10.221816 | 0.051902 | -0.487695 |

Drift parameters can be close to truth when the others are supplied. Innovation parameters are far less stable. UKF's correlation even has the wrong sign in this run. A favorable value for one parameter/filter combination does not establish superiority: UPF's correlation is close to truth while its $\xi$ remains high. Figures 2–5 display sharp versus flat or irregular parameter profiles. Some graphs labeled log likelihood have minima at the indicated optimum, so a reproducer must verify whether the plotted objective is a negative likelihood or uses another sign convention. Literal maximization of a curve with the displayed minimum would be inconsistent with its caption.

## More observations at the same daily interval

Table 4 varies sample length while estimating $\xi$ or $\rho$ separately with EKF. The reported estimates are:

| Daily observations | $\widehat\xi$ | $\widehat\rho$ |
|---:|---:|---:|
| 5,000 | 0.052324 | -0.873571 |
| 50,000 | 0.036463 | -0.608088 |
| 100,000 | 0.033400 | -0.556868 |
| 500,000 | 0.031922 | -0.532142 |

The table gives starting values $\xi_0=0.03$ and $\rho_0=-0.040$. These differ from the first experiment's general starting vector and should be retained as reported. In this sequence, estimates move closer to the true values as the path grows. At 252 observations a year, 50,000 daily observations represent about 198 years; 500,000 represent about 1,984 years. The point is limited information at realistic horizons, not a recommendation to fit one stationary regime across centuries.

The article interprets this pattern through consistency of maximum likelihood. A finite sequence of simulation results cannot prove consistency, and approximate-filter likelihood estimators require their own assumptions. Discretization, filter approximation, identifiability, and optimizer behavior do not automatically disappear merely because a method is called MLE.

## Joint estimation is substantially harder

The joint experiment starts at $(0.15,15,0.02,-0.40)$ and estimates all four parameters with EKF, keeping the stock drift known. Table 7 reports:

| Observations | $\widehat\omega$ | $\widehat\theta$ | $\widehat\xi$ | $\widehat\rho$ |
|---:|---:|---:|---:|---:|
| 5,000 | 0.150854 | 15.294576 | 0.266175 | -0.128835 |
| 50,000 | 0.126387 | 12.748852 | 0.020521 | -1.000000 |
| 100,000 | 0.136023 | 13.700906 | 0.044353 | -0.439961 |
| 500,000 | 0.100097 | 10.030336 | 0.061688 | -0.257305 |
| 1,000,000 | 0.105264 | 10.548642 | 0.043818 | -0.356234 |
| 2,000,000 | 0.103183 | 10.334876 | 0.039767 | -0.374677 |
| 4,000,000 | 0.105292 | 10.538019 | 0.043288 | -0.347562 |
| 5,000,000 | 0.101097 | 10.118951 | 0.028588 | -0.514346 |

The sequence is not monotone in estimation accuracy. At 500,000 observations the drift parameters are close to truth but $\xi$ is roughly twice the true value and correlation remains materially wrong. At 50,000, correlation is on the negative boundary. Jointly moving $\omega$ and $\theta$ can preserve a plausible long-run ratio while leaving their separate estimates uncertain. This is why inspecting only a fitted volatility level understates parameter risk.

The author reports only marginal improvements from other filters in this experiment and omits their numerical results. That supports a statement about what was reported, not a comprehensive ranking of all possible filtering implementations. Optimization settings, boundary constraints beyond the visible correlation limit, and repeated-start diagnostics are not disclosed.

## Observation transformations and what they recover

For log returns, the state affects conditional mean at order $\Delta$, but the return noise is of order $\sqrt\Delta$. That weak mean sensitivity makes a basic linearized filter poorly informative about variance from a single small increment. The article describes variance as unobservable if price itself is used and the mean observation gradient is zero. This is a statement about that mean-based linearization, not a general impossibility of learning volatility: the conditional return variance still depends on $v$, and squared returns or likelihood information can identify it under suitable conditions.

Ignoring the smaller drift contribution, the transformed observation is

$$
z_k=\log[(\log S_{k+1}-\log S_k)^2]\approx\log v_k+\log\Delta+\log B_k^2.
$$

For standard normal $B$, the log-chi-square disturbance has mean approximately -1.27036 and variance $\pi^2/2$. The Harvey–Ruiz–Shephard (HRS) approximation replaces this non-Gaussian disturbance by a Gaussian with those moments. Matching moments does not make the distribution Gaussian. It avoids evaluating a logarithmic observation map at zero noise, which would create a singularity in a naive augmented EKF implementation.

Table 8 shows HRS/EKF estimates still problematic at short sample lengths. With 5,000 observations the joint estimate is $(0.722746,71.753861,0.044602,-1)$; with 500,000 it is $(0.109738,11.020391,0.027140,-0.531481)$. Thus the transformation does not simply solve finite-sample identification.

An alternative particle-filter observation uses $\log|\log S_{k+1}-\log S_k|\approx\tfrac12\log v_k+\tfrac12\log\Delta+\log|B_k|$. The exact density of $\log|B|$ is $f(x)=2e^x\varphi(e^x)$, where $\varphi$ is the standard normal density. Table 9's 5,000-observation joint particle estimate is $(0.147212,14.999999,0.070407,-0.555263)$, which the author does not regard as a clear improvement. Handling zero observed returns and numerical logarithm floors is not specified.

## Higher frequency and sampling distributions

The high-frequency experiment holds the horizon at 5,000 business days but uses 1,000 steps per day: five million observations with $\Delta=1/252{,}000$. EKF gives $(0.090280,9.019962,0.042984,-0.283236)$; EKF/HRS gives $(0.092372,9.224421,0.030951,-0.507763)$. In this simulated example, HRS is particularly close for the innovation parameters. Increasing sampling frequency differs from extending the time span, and the result relies on a clean diffusion simulation. The paper itself cautions that intraday market data bring cleaning and microstructure problems. It does not test the procedure on noisy transaction data.

The most informative uncertainty exercise simulates 500 paths and estimates each path separately. Table 11 gives the following means and cross-path standard deviations:

| Parameter | Truth | Mean, 5,000 observations | SD | Mean, 50,000 observations | SD |
|---|---:|---:|---:|---:|---:|
| $\omega$ | 0.10 | 0.119339 | 0.098996 | 0.102555 | 0.027021 |
| $\theta$ | 10.0 | 11.922715 | 9.673830 | 10.262331 | 2.706564 |
| $\xi$ | 0.03 | 0.056092 | 0.049742 | 0.043839 | 0.013005 |
| $\rho$ | -0.50 | -0.343217 | 0.297434 | -0.351998 | 0.074998 |

These are sampling standard deviations of estimated parameters, not standard errors of the reported Monte Carlo means. Longer histories reduce dispersion substantially, but residual bias in $\xi$ and $\rho$ remains visible even at 50,000 observations. The true correlation is not progressively approached by the two reported means; the main clear improvement for correlation is its smaller dispersion. Figures 10–13 reinforce that individual paths can yield very poor estimates even when an average estimate seems reasonable.

## Interpretation and reproduction limits

Equivalent changes of measure preserve diffusion covariation characteristics within the assumed continuous diffusion model, motivating the comparison of physical and risk-neutral $\xi$ and $\rho$. Historical and option estimates can differ because of sampling uncertainty, approximation, calibration objectives, or model misspecification. The simulations establish that sampling uncertainty is a plausible contributor. They do not show that every empirical discrepancy is harmless or rule out volatility risk premia in drift parameters.

The concluding suggestion of testing a skewness trade—buying out-of-the-money calls and selling puts—is not implemented here. No option sample, strikes, maturities, trading costs, hedging rule, or P&L results are provided. Lack of conclusive profit would also not uniquely identify historical-estimation error as the cause of a discrepancy.

A reproduction should preserve the known drift, true parameters, separate versus joint estimation distinction, observation intervals, and 500-path experiment. It also needs the missing filter details, optimizer, variance boundary treatment, initialization, and random seeds. The appropriate benchmark is recovery of the displayed distributions and tables with Monte Carlo uncertainty, not matching one path exactly. The practical lesson is to quantify parameter uncertainty before interpreting a physical-versus-option calibration gap, and to assess transformed observations and higher-frequency data with their additional assumptions explicitly stated.
