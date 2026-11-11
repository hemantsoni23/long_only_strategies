# Realized GARCH: A Joint Model for Returns and Realized Measures of Volatility

**Peter Reinhard Hansen, Zhuo Huang, and Howard Howan Shek.** Published online in 2011; final publication *Journal of Applied Econometrics* 27(6), 877–906 (2012), DOI 10.1002/jae.1234. Source: [library PDF](../../Finance/GARCH_HansenHuangShek_2011.pdf), thirty pages including the mathematical appendix. Page pointers below refer to PDF pages because this advance-publication copy lacks final journal pagination. The publication history and existence of supplementary files are confirmed by the [publisher record](https://onlinelibrary.wiley.com/doi/10.1002/jae.1234).

## Why this matters and what is new

A daily squared return is an extremely noisy measurement of daily variance. A model driven only by past squared returns can consequently respond slowly when the underlying variance changes. Intraday realized measures provide more information, but inserting yesterday's realized variance into a GARCH equation alone leaves tomorrow's realized measure unexplained. That incomplete model is inconvenient for forecasting multiple periods or simulating coherent paths of returns and volatility.

The innovation is a joint system with one conditional variance process and an explicit measurement equation linking it to an observed realized measure. The measurement error includes a function of the contemporaneous standardized return. Negative and positive return shocks can therefore affect the observed measure differently, and that asymmetry feeds into future variance. The measurement equation simultaneously completes the predictive model and provides a parsimonious leverage mechanism.

The preferred log-linear version keeps variance positive and turns the log variance and log realized measure into low-order ARMA processes. Joint Gaussian quasi-likelihood estimation is tractable. The evidence covers 28 Dow Jones stocks and SPY, with a separate 2008 evaluation period. Incorporating realized kernels improves the return-density fit, and accounting for leverage markedly improves the joint fit. The source favors a model with one lag of log variance and two lags of the log realized measure.

The paper is particularly useful as an implementation blueprint because the distinction between a forecast variance and its ex-post measurement remains explicit. A realized kernel is not treated as error-free latent variance, and a good joint likelihood is distinguished from a good return likelihood. Important limits remain: the paper does not fully prove its proposed estimator asymptotics, finite moments of log variance do not automatically imply finite return moments, and exact data cleaning and numerical settings are not all contained in the supplied PDF.

## Information, timing, and the joint model

Let $r_t$ denote a mean-zero daily return, or the residual after a separately specified conditional mean. Let $x_t>0$ be a realized measure constructed from intraday prices. Define $\mathcal F_t=\sigma(r_s,x_s:s\leq t)$, including the initialized variance state. The conditional variance is $h_t=\operatorname{Var}(r_t\mid\mathcal F_{t-1})$. Thus $h_t$ is known before the day-$t$ return and realized measure arrive.

The general framework in Section 2 is

$$
r_t=\sqrt{h_t}z_t,\qquad
h_t=v(h_{t-1},\ldots,h_{t-p},x_{t-1},\ldots,x_{t-q}),\qquad
x_t=m(h_t,z_t,u_t).
$$

The primitive innovations satisfy $E z_t=0$, $E z_t^2=1$, $E u_t=0$, and $\operatorname{Var}(u_t)=\sigma_u^2$. The baseline formulation assumes iid sequences and mutual independence. Gaussian distributions are adopted for estimation but weaker moment restrictions underpin the quasi-likelihood score argument.

The measurement equation may relate a 6.5-hour realized measure to a 24-hour return variance. This is allowed because its intercept and slope estimate the relationship rather than force $x_t=h_t$. It is still necessary to align each realized measure with the proper calendar day's return. The day-$t$ realized measure belongs in the update for $h_{t+1}$, not in a purported advance forecast of $r_t$.

The linear specification is $h_t=\omega+\beta h_{t-1}+\gamma x_{t-1}$ and $x_t=\xi+\phi h_t+\tau(z_t)+u_t$. Its algebra is simple, but additive Gaussian measurement errors are difficult to reconcile with an everywhere-positive realized measure. Nonnegative coefficients can keep the variance recursion positive on observed positive data without repairing that measurement-support issue. The log-linear version is both empirically better behaved and the principal model developed below.

Write $y_t=\log h_t$ and $q_t=\log x_t$. The baseline log-linear RealGARCH$(p,q)$ system is

$$
y_t=\omega+\sum_{i=1}^{p}\beta_i y_{t-i}
+\sum_{j=1}^{q}\gamma_j q_{t-j},
$$

$$
q_t=\xi+\phi y_t+\tau(z_t)+u_t,\qquad
\tau(z)=\tau_1z+\tau_2(z^2-1).
$$

The leverage function has mean zero whenever the standardized innovation has mean zero and variance one; normality is unnecessary for this centering. A negative $\tau_1$ creates an asymmetric response, while $\tau_2$ captures a quadratic response to unusually large shocks. Higher-order polynomial terms can be introduced, provided their centering is appropriate for the actual innovation distribution.

An extended model adds $\alpha\log r_{t-1}^2$ to the variance equation. This is a test of whether a daily squared return adds information once realized measures are available. It is not required to obtain leverage: leverage is already transmitted through the measurement equation and subsequent realized-measure lags.

## Dynamics, persistence, and conditions that must not be conflated

Define $w_t=\tau(z_t)+u_t$. For the $(1,1)$ model, substitution yields

$$
y_t=\mu_h+\pi y_{t-1}+\gamma w_{t-1},\qquad
\mu_h=\omega+\gamma\xi,\qquad \pi=\beta+\phi\gamma.
$$

The log realized measure has the ARMA representation

$$
q_t=\phi\omega+(1-\beta)\xi+\pi q_{t-1}+w_t-\beta w_{t-1}.
$$

These expressions show why $\beta$ alone is not persistence. Feedback through the realized measure contributes $\phi\gamma$. For general orders, pad missing coefficients with zeros and examine the autoregressive polynomial whose coefficients are $\beta_i+\phi\gamma_i$. If the extended lagged-log-squared-return term is present, its autoregressive contribution must also be included, together with its additional innovation. A scalar sum near one is a useful descriptive statistic, but stability of a higher-order system requires the appropriate root condition.

For $(1,1)$, $|\pi|<1$ and suitable moments of $w_t$ yield a stationary log-variance representation. If initialized from its invariant law, the paper uses hidden-Markov and mixing results to support stationary ergodic behavior. Positivity of $h_t=\exp(y_t)$ is automatic even when some log-dynamic coefficients are negative. Consequently one should not impose the usual nonnegative linear-GARCH coefficient restrictions indiscriminately on this model.

Stationarity of $y_t$ is different from finiteness of $E h_t$ or $E h_t^2$. Exponential moments of $y_t$ are needed for return variance and kurtosis. A stable log process can have finite polynomial log moments but infinite moments after exponentiation. This distinction matters when simulating long-horizon risk or applying Gaussian quasi-likelihood asymptotics that require finite score moments.

The paper's Section 6.1 prints $\mu=\omega+\phi\xi$ immediately before the $(1,1)$ recursion. Direct substitution into the stated measurement and variance equations gives $\omega+\gamma\xi$, as used above. The notation correction is algebraic; it does not alter the fitted model or imply that unpublished empirical code used the printed typo.

## Leverage and the units of the news-impact curve

The authors define a news-impact curve through the expected change in next period's log variance associated with the current standardized return. Under the stated independence assumptions,

$$
\nu(z)=E(y_{t+1}\mid z_t=z)-E(y_{t+1})=\gamma_1\tau(z).
$$

This is a log-variance displacement. Multiplying by 100 gives an approximate percentage variance displacement; the exact multiplicative variance factor associated with a deterministic log displacement is $\exp[\nu(z)]$. Standard deviation changes have half the log displacement. The article labels the plotted quantity in percentage volatility language, but a replication should preserve the variance units implied by its defining equation.

Figure 1 uses four-term leverage estimates for IBM and SPY. The coefficients are respectively $(-.036,.090,.001,-.003)$ and $(-.068,.081,.014,.002)$. The higher-order terms are small compared with the linear and quadratic terms. Both curves respond more to sufficiently large negative shocks than to similarly sized positive shocks; the SPY asymmetry is especially clear. The approximate plotted displacement at a standardized return near $-2$ is around +13%, compared with about +5% for SPY at +2. These are readings of the plotted log-variance curve, not exact out-of-sample realized changes.

The reported $\rho^-$ and $\rho^+$ are correlations between $w_t$ and $z_t$ conditional on negative and positive $z_t$, respectively. They are not the leverage coefficients themselves and should not be inserted into $\tau(z)$ as parameter replacements. Table III reports SPY values about $-.32$ and $.13$, compared with IBM's $-.32$ and $.24$.

## Joint quasi-likelihood and an implementable estimator

For a fixed initial history, compute the variance recursion, standardized returns $z_t=r_t\exp(-y_t/2)$, and measurement residuals

$$
u_t=q_t-\xi-\phi y_t-\tau_1z_t-\tau_2(z_t^2-1).
$$

The Gaussian criterion, omitting constants independent of parameters, is

$$
\ell(\theta)=-\frac12\sum_t
\left[y_t+r_t^2e^{-y_t}+\log\sigma_u^2+
\frac{u_t^2}{\sigma_u^2}\right].
$$

It is naturally a likelihood for $(r_t,\log x_t)$. A density written for $(r_t,x_t)$ additionally has the Jacobian contribution $-\log x_t$, which does not affect estimates when every model uses the same observed measure. Absolute likelihood levels should only be compared under a common convention. A standard GARCH model does not model $x_t$, so its likelihood cannot be compared directly with a joint Realized GARCH likelihood.

The return contribution is

$$
\ell_r=-\frac12\sum_t[\log(2\pi)+y_t+r_t^2e^{-y_t}].
$$

Use this common partial likelihood to compare return-density performance. The conditioning is on past information, including past realized measures in Realized GARCH. It does not mean conditioning a return forecast on the same day's observed realized kernel. The $r\mid x$ notation in the discussion of Table IV should be read in the context of the explicit factorization on PDF p. 12, not as permission to introduce contemporaneous information.

A practical estimator can reduce the numerical dimension by profiling. Conditional on the dynamic parameters $(\omega,\beta_i,\gamma_j)$ and fixed initial states, all $y_t$ and $z_t$ are known. Regress $q_t$ on $(1,y_t,z_t,z_t^2-1)$ to obtain $(\xi,\phi,\tau_1,\tau_2)$, and set $\sigma_u^2$ to the residual sum of squares divided by the estimation sample size. Then optimize the profiled joint criterion over the dynamic parameters. This profiling construction follows directly from the stated Gaussian likelihood; it is an implementation derivation, not a claim about the authors' software. If restrictions couple the measurement and dynamic parameters, profiling must respect them.

The recursion and derivatives make numerical estimation inexpensive. For $\lambda=(\omega,\beta_1,\ldots,\gamma_q)$, define $d_t=\partial y_t/\partial\lambda$ and $g_t=(1,y_{t-1},\ldots,q_{t-q})^{\mathsf T}$. With parameter-independent initial states,

$$
d_t=g_t+\sum_i\beta_i d_{t-i},\qquad d_s=0\quad(s\leq0).
$$

Since $\partial z_t/\partial y_t=-z_t/2$,

$$
a_t:=\frac{\partial u_t}{\partial y_t}
=-\phi+\frac12z_t\tau'(z_t).
$$

The score for the dynamic block is

$$
\frac{\partial\ell_t}{\partial\lambda}
=\left[\frac12(z_t^2-1)-\frac{u_ta_t}{\sigma_u^2}\right]d_t.
$$

For measurement regressors $m_t=(1,y_t,z_t,z_t^2-1)^{\mathsf T}$, the measurement-parameter score is $u_tm_t/\sigma_u^2$. The score for $s=\sigma_u^2$ is $(u_t^2-s)/(2s^2)$. These derivatives can be checked against finite differences of the likelihood before optimization.

The source's main score proposition agrees with these expressions. Some displayed appendix derivative lines do not: differentiating $-u_t^2/(2\sigma_u^2)$ with respect to $u_t$ gives $-u_t/\sigma_u^2$, not a positive doubled term. Likewise differentiating the measurement score with respect to $s$ gives $-u_tm_t/s^2$. Deriving the Hessian directly from the likelihood or verified score avoids propagating those sign/factor slips. These are mathematical implementation checks, not evidence that the numerical estimates were computed incorrectly.

The supplied paper does not identify the optimization routine, parameter bounds, restart strategy, stopping tolerances, or exact initial backcast. A reconstruction should report these choices. Useful checks are stability of the dynamic polynomial, convergence from several initial values, finite positive fitted variances, and agreement between analytic and numerical gradients. A stationary initialization such as the unconditional log mean is an available choice, not a source-reported setting.

## What the asymptotic argument establishes

Proposition 3 shows that the score is a martingale difference under $E(u_t\mid z_t,\mathcal F_{t-1})=0$, $E(z_t^2\mid\mathcal F_{t-1})=1$, and $E(u_t^2\mid\mathcal F_{t-1})=\sigma_u^2$. With stationarity, ergodicity, and finite relevant matrices, the paper supplies a score central limit theorem and convergence of the average Hessian. At least fourth moments of primitive innovations are needed for the score covariance; a more complex leverage function can require additional moments.

The proposed robust estimator covariance is the sandwich $I^{-1}JI^{-1}/n$, where $I$ is minus the expected Hessian and $J$ is the score covariance. Under correct Gaussian specification, information equality can simplify this expression. The empirical analysis uses robust standard errors rather than assuming exact normality.

Crucially, PDF p. 11 explicitly calls asymptotic normality of the full QMLE a conjecture requiring verification of additional regularity conditions from Straumann and Mikosch. Those conditions are left to future research. Nonstationary and unit-root log-variance cases are also left unresolved. The paper should therefore not be cited as a completed general consistency and normality proof for every Realized GARCH specification, especially when estimated persistence is effectively one.

## Data construction and evaluation design

The application uses 28 DJIA constituent stocks and SPY. The reported stock tickers are AA, AIG, AXP, BA, BAC, C, CAT, CVX, DD, DIS, GE, GM, HD, IBM, INTC, JNJ, JPM, KO, MCD, MMM, MRK, MSFT, PG, T, UTX, VZ, WMT, and XOM. These names identify the historical empirical universe; reproducing it with present-day constituent membership would change the sample.

The overall sample runs from January 1, 2002 through August 31, 2008. Estimation uses January 1, 2002 through December 31, 2007. Out-of-sample evaluation uses January 2 through August 31, 2008. The latter interval ends before the September 2008 Lehman failure and should not be described as covering the entire financial-crisis climax.

The realized measure is a positive realized kernel using the Parzen kernel. The construction follows the positive estimator in Barndorff-Nielsen and coauthors and the detailed implementation in their work on realized kernels from trades and quotes. Its purpose is to estimate quadratic variation while being robust to market microstructure noise. The present paper does not reproduce every intraday cleaning rule or the bandwidth-selection machinery; those referenced estimator details are part of an exact reconstruction's dependencies.

Intraday data cover the regular 9:30 a.m.–4:00 p.m. session. Days with observed high-frequency coverage below 90% of the official 6.5 hours are removed. The threshold is 351 minutes, and the exclusion removes about three observations per year, including some half trading days. This is a span criterion, not simply a requirement that 90% of a fixed grid have nonmissing observations.

Both open-to-close and close-to-close returns are modeled using the open-to-close realized kernel. Models with $\log r_t^2$ replace the argument by $\max(r_t^2,10^{-20})$ to handle exact zero returns. This truncation is unnecessary for the baseline model's return likelihood, which uses squared returns without taking their logarithm. The source does not fully specify price adjustment conventions, high-frequency vendor, final asset-specific sample sizes, or the return-mean preprocessing for every series in this PDF.

For the holdout exercise, the in-sample parameter estimates are plugged into the out-of-sample likelihood. The variance state continues to update as each new return and realized measure becomes available. This is fixed-parameter sequential evaluation, not a fresh full-sample fit to 2008, and not a rolling re-estimation experiment. The principal empirical comparisons are one-day conditional density scores; multi-step forecasting is developed analytically rather than evaluated in a separate broad forecast contest.

A linked Web Appendix contains additional summary statistics, linear-model results, and moment derivations. Retrieval was attempted from both the publisher supplement and the original JAE data archive; these returned access/server errors during preparation. Its contents and the separate archived software were not verified. The supplied main article and all its embedded appendix pages were read. Exact replication inputs missing here should be recovered from those primary supplementary materials rather than invented.

## Parameter estimates and substantive empirical results

For SPY open-to-close returns, the linear $(1,1)$ estimates are approximately $h_t=.09+.29h_{t-1}+.63x_{t-1}$ and $x_t=-.05+1.01h_t-.02z_t+.06(z_t^2-1)+u_t$. The close-to-close model has measurement slope about .74 instead of 1.01. This fits the interpretation that trading-session variance captures only part of daily variance. In the log-linear model, the corresponding scale mismatch is largely captured by a more negative measurement intercept, while $\phi$ remains near one.

Table II gives the following log-linear SPY estimates; coefficients are rounded as in the table:

| Return interval and model | $\omega$ | $\beta$ | $\gamma_1$ | $\gamma_2$ | $\xi$ | $\phi$ | $\sigma_u$ | $\tau_1$ | $\tau_2$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Open-to-close, $(1,1)$ | .06 | .55 | .41 | — | −.18 | 1.04 | .38 | −.07 | .07 |
| Open-to-close, $(1,2)$ | .04 | .70 | .45 | −.18 | −.18 | 1.04 | .38 | −.07 | .07 |
| Close-to-close, $(1,2)$ | .11 | .72 | .48 | −.21 | −.42 | 1.00 | .38 | −.11 | .04 |

The first row's persistence is about .975, and the open-to-close $(1,2)$ model's persistence is .986 using the table's unrounded calculation. Computing persistence from rounded coefficients need not reproduce the reported last decimals. A negative second realized-measure lag is permitted in a log-variance specification and can improve the dynamic shape while keeping every fitted variance positive.

Across all 29 assets, Table III's average $(1,2)$ estimates are approximately $\omega=.01$, $\beta=.79$, $\gamma_1=.41$, $\gamma_2=-.21$, $\xi=-.02$, $\phi=1.04$, $\sigma_u=.41$, $\tau_1=-.03$, and $\tau_2=.09$. Average persistence is .99. The regularity across assets supports a common low-dimensional model architecture; it does not establish that all parameter values can be pooled without an additional estimation exercise.

For SPY open-to-close returns, the conventional log-GARCH return log likelihood is −1752.7. The Realized GARCH $(1,1)$ and $(1,2)$ partial return log likelihoods are −1712.0 and −1710.3, respectively, while their joint likelihoods are −2395.6 and −2388.8. The return-only improvement from −1752.7 to −1710.3 is 42.4 log-likelihood units. It must not be confused with an improvement in annualized return, Sharpe ratio, or trading profit.

The unrestricted $(2,2)$ model with the additional lagged squared-return term has open-to-close joint likelihood −2382.9, versus −2385.1 without that extra term. Removing leverage worsens the joint likelihood to −2495.7. Thus leverage explains far more of the joint likelihood than the extra conventional ARCH input. This comparison is not a guarantee that the leverage version wins every partial return score: joint estimation optimizes both measurements and returns.

## Model comparisons, uncertainty, and the holdout results

Table IV separates three statistics whose scales and interpretations differ. Panel A reports in-sample likelihood ratios $2(\ell_{\mathrm{large}}-\ell_j)$ relative to the $(2,2)$ model including the additional ARCH term. Across assets, the averages are 39.8 for $(1,1)$, 9.6 for $(1,2)$, 20.5 for $(2,1)$, 3.9 for $(2,2)$, and 208.8 for the no-leverage version. The large leverage penalty and the smaller $(1,2)$ loss motivate the preferred parsimonious model.

Panel B reports a differently normalized out-of-sample statistic:

$$
\sqrt{\frac{n}{m}}\,[\ell_{\mathrm{RG}(2,2)}^{\mathrm{out}}-
\ell_j^{\mathrm{out}}],
$$

where $n$ and $m$ are the estimation and holdout sizes. Positive values favor the $(2,2)$ benchmark; negative values favor the alternative. Average values are 4.4 for $(1,1)$, .1 for $(1,2)$, 1.1 for $(2,1)$, 0 for the benchmark, 23.0 without leverage, and 2.1 for the added-ARCH model. For SPY, the $(1,2)$ statistic is −1.2, so the simpler model has the better holdout joint score there.

The asymptotic reference for nested comparisons is a product of independent Gaussian vectors with a misspecification weighting matrix, not an ordinary chi-square likelihood-ratio law. Under correct specification, the cited two-sided critical values are 2.25 and 3.67 for one restriction at 5% and 1%, and 3.05 and 4.83 for two restrictions. The authors regard these as approximate because the log-linear Gaussian model is not exact. Leverage is strongly useful on average, but not every individual holdout comparison favors it; the no-leverage entries for C, DD, and JPM are negative.

Panel C instead compares return-only holdout scores with the best return score among the candidate models. Its statistic is twice the score shortfall. The standard log-GARCH model's average shortfall is 33.5, whereas the Realized GARCH alternatives average roughly .8–1.6. SPY's standard-GARCH shortfall is 40.8, versus .6 for the $(1,2)$ alternative and zero for the best-performing candidate. The source's footnote stresses that this comparison has a nonstandard, generally unknown distribution because one model maximizes return likelihood and others maximize joint likelihood. These are informative score differences, not conventional significance tests with an automatically assigned degree of freedom.

Figures 2 and 3 provide a specification diagnosis: the linear model's measurement residual spread increases markedly with the variance level, and the log model reduces that heteroskedasticity. Adding the quadratic leverage function removes much of the visible dependence between standardized return and measurement residual. The scatterplots support the simpler Gaussian measurement approximation but do not prove residual independence or normality.

Table V makes the uncertainty implications concrete. For the linear $(1,2)$ model, the standard error of $\beta$ is .034 from inverse curvature, .017 from inverse score information, and .125 from the robust sandwich. The corresponding log-linear values are .040, .031, and .053. For $\phi$, the robust standard errors are .212 in the linear model and .069 in the log model. Such differences show why Gaussian information equality should not be imposed on the visibly misspecified linear specification.

## Multi-step prediction and simulation

For $(1,1)$, define $Y_t=(y_t,q_t)^{\mathsf T}$. Its exact linear state recursion is

$$
Y_{t+1}=b+AY_t+\begin{pmatrix}0\\w_{t+1}\end{pmatrix},\qquad
b=\begin{pmatrix}\omega\\\xi+\phi\omega\end{pmatrix},\qquad
A=\begin{pmatrix}\beta&\gamma\\\phi\beta&\phi\gamma\end{pmatrix}.
$$

The zero first innovation reflects that $h_{t+1}$ is already determined by data through $t$. Hence

$$
E(Y_{t+k}\mid\mathcal F_t)=A^kY_t+\sum_{j=0}^{k-1}A^jb.
$$

Higher-order models use a companion state containing the necessary lagged log variances and realized measures. This yields forecasts of logs. Exponentiating an expected log variance gives a geometric forecast, not generally the conditional expectation of variance. A level forecast needs the innovation moment-generating function or simulation to include Jensen's correction.

A coherent simulation step first computes $h_{t+1}$ from the current state, draws independent $z_{t+1}$ and $u_{t+1}$, forms $r_{t+1}=\sqrt{h_{t+1}}z_{t+1}$, and then forms $q_{t+1}=\xi+\phi\log h_{t+1}+\tau(z_{t+1})+u_{t+1}$. Feed the resulting measure into the next update. Drawing future realized measures independently of return shocks would erase the leverage channel that the model was designed to capture.

Because returns are martingale differences, the conditional variance of a cumulative future return is the sum of the expected one-day conditional variances when the required moments exist. Their distributions are nevertheless not independent: today's return affects tomorrow's variance. This dependence can generate skewness for cumulative returns even when each single-day standardized innovation is symmetric.

## Return moments and the boundary of Gaussian simplicity

For Gaussian $z_t$ and $u_t$, the innovation $w_t=\tau_1z_t+\tau_2(z_t^2-1)+u_t$ has moment-generating function

$$
M_w(a)=\frac{\exp\left[-a\tau_2+
\frac{a^2\tau_1^2}{2(1-2a\tau_2)}+
\frac12a^2\sigma_u^2\right]}{\sqrt{1-2a\tau_2}},
\qquad 1-2a\tau_2>0.
$$

This expression follows by completing the square in the Gaussian integral. Under stationary $(1,1)$ dynamics, $y_t=\mu_h/(1-\pi)+\sum_{i\geq0}\gamma\pi^iw_{t-1-i}$. Consequently the source's exact kurtosis formula can be reconstructed compactly as

$$
\frac{E r_t^4}{(E r_t^2)^2}
=3\prod_{i=0}^{\infty}
\frac{M_w(2\gamma\pi^i)}{M_w(\gamma\pi^i)^2},
$$

provided these moments exist. For $0\leq\pi<1$ and positive $\gamma,\tau_2$, the fourth-moment domain requires $4\gamma\tau_2<1$. More general sign patterns require checking every moment-generating-function argument rather than using that sufficient positive-coefficient shortcut. This condition is distinct from log-process stationarity.

A symmetric $z_t$ gives zero single-period return skewness because $h_t$ is predetermined and independent of the current innovation. Figure 4 simulates cumulative returns using the SPY log-linear $(1,2)$ estimates. Skewness falls to approximately −.25 around 100 days and is still roughly −.22 at 250 days. Kurtosis is about 5.3 at short horizons and declines to about 3.8 at 250 days. These are visual readings of model-generated curves, not estimates of empirical sampling uncertainty. The main paper does not specify the path count, seed, or burn-in needed to reproduce the plotted Monte Carlo values exactly.

The practical lesson is that Gaussian primitive shocks need not produce Gaussian unconditional or cumulative returns. The variance mixture and leverage feedback generate economically relevant tail thickness and asymmetry. They do not automatically validate Gaussian tail forecasts at extreme probabilities; the measurement equation, distributional approximation, parameter uncertainty, and moment domain must still be checked.

## Reimplementation priorities and limits

The core contribution is fully operational from daily returns and a positive realized measure: filter a low-dimensional log variance, estimate its joint measurement system, and evaluate forecast densities with the correct information timing. A faithful empirical reconstruction must keep the 2002–2007 estimation window, the eight-month 2008 holdout, the historical universe, and the session-coverage exclusions fixed before comparing alternatives.

The strongest reported evidence concerns conditional density fit and the importance of leverage in the joint system. No transaction-cost model, trading strategy, or portfolio-performance experiment is reported. The paper also does not establish that every intraday estimator, alternative sampling scheme, or later crisis sample will produce the same gains. These are separate empirical questions.

Before treating the note's equations as a production implementation, recover the supplementary data and estimator details, document the variance initialization and optimization constraints, verify the likelihood derivatives, and inspect both standardized-return and measurement residuals. Near-unit persistence and non-Gaussian residuals make robust inference and moment checks consequential. The source's unresolved QMLE regularity conditions and the explicit distinction between log and level forecasts should remain visible in any subsequent use of the model.
