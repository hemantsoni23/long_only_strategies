# General properties of backtestable statistics

Carlo Acerbi and Balazs Szekely, MSCI Inc., January 24, 2017 working paper, SSRN 2905109. The local filename says 2018, but the cover dates the actual version to 2017. This note covers all 30 PDF pages, including Appendix A and the numerical illustrations on the final page. Regulatory statements in the paper describe its historical setting.

Source: [Backtesting_Acerbi_2018.pdf](../../Finance/Backtesting_Acerbi_2018.pdf).

## Why this matters

A forecast of a risk statistic cannot be compared directly with its eventual true value: one observes a realized profit or loss, not the conditional distribution or its true quantile, variance, or expected shortfall. A usable validation procedure needs an observable function of forecasts and outcomes whose expectation has a known interpretation.

This paper formalizes that requirement, separates directional validation from relative forecast scoring, and introduces two important distinctions. A backtest can detect the direction of forecast error without measuring its economic magnitude; the authors call magnitude identification “sharpness.” A statistic that cannot be tested in isolation may nevertheless admit a useful test with an auxiliary forecast, provided auxiliary error has a controlled sign and small local effect. Their “ridge” construction delivers this property for variance using the mean, and expected shortfall using VaR.

The most useful implementation result is the expected-shortfall residual in Equations 47–48. Its dependence on quantile error is locally muted and has a known downward bias. That does not make it immune to sampling error, prove that ES alone is elicitable, or establish finite-sample size control for every forecasting process.

## Experiment, sign conventions, and domains

At time $t-1$ a model forecasts a scalar statistic $y_t$ of the next outcome $X_t$. The actual conditional distribution is $F_t$; a model may also issue a full predictive distribution $P_t$, with $y_t=y(P_t)$. The observed pair is $(y_t,x_t)$. Forecasts must precede outcomes. The statistic's true value $y(F_t)$ generally remains unobservable.

The paper treats $X$ as profit/loss, with adverse outcomes in its lower tail. The tail probability $\alpha$ is small. Define $u_+=\max(u,0)$ and $u_-=\max(-u,0)$. Quantile, VaR, tail mean, and ES obey

$$
q_\alpha=F^{-1}(\alpha),\qquad
\operatorname{VaR}_\alpha=-q_\alpha,\qquad
\operatorname{ES}_\alpha=-\frac1\alpha\int_0^\alpha q_u\,du.
$$

For general distributions the quantile may be an interval; Appendix A defines its lower and upper endpoints. ES remains single valued when its lower-tail integral exists. A lower-tail mean is not necessarily $E[X\mid X<q_\alpha]$ when there is an atom at the threshold. The identity valid with atoms is

$$
\operatorname{ES}_\alpha=-q+\frac1\alpha E[(X-q)_-]
$$

for a valid $\alpha$-quantile $q$. It allocates the appropriate portion of threshold mass to the tail, rather than changing the effective tail probability.

All existence statements depend on a distribution class and integrability conditions. A result on a restricted smooth family is not automatically a result on every distribution. Variance requires a second moment; the ES residual requires an integrable lower tail. The expectile identifying equation needs a first moment, whereas its usual squared-error score needs stronger integrability if its expectation is to be finite.

## Three forecast properties

Elicitability means that there is a score $S(y,x)$ with true statistic minimizing expected score:

$$
y(F)=\arg\min_y E_F[S(y,X)].
$$

Examples include squared error for the mean, absolute error for the median, quantile loss $\alpha(x-y)_+ +(1-\alpha)(x-y)_-$, and asymmetric squared error for expectiles. Comparing models' mean realized scores is a relative contest: the lowest score can still belong to a bad model, and the score does not reveal whether forecasts are systematically too high or too low.

Identifiability requires an observable function $I(y,x)$ such that $E_F[I(y,X)]=0$ exactly at the true statistic. A derivative of a suitable expected score often supplies this function. Identification alone need not order errors in a sensible direction away from the root.

The authors define backtestability more restrictively: an identifying function $Z(y,x)$ must have expectation strictly increasing in the forecast $y$. Consequently

$$
\operatorname{sign} E_F[Z(y,X)]
 =\operatorname{sign}[y-y(F)].
$$

At a fixed actual distribution, progressively larger overpredictions yield progressively larger positive expectations, and progressively worse underpredictions yield more negative expectations. This is a particular scalar definition of backtesting, not an impossibility theorem about every conceivable multivariate validation procedure.

Canonical examples are

$$
Z_\mu(y,x)=y-x,
\qquad Z_q(y,x)=1_{\{x\le y\}}-\alpha,
$$

$$
Z_{e_\alpha}(y,x)=(1-\alpha)(x-y)_--\alpha(x-y)_+.
$$

The mean residual is increasing for every outcome. The quantile residual is a step function, so strict monotonicity of its expectation requires a correspondingly increasing CDF over the relevant forecast domain. Continuity at the quantile ensures the zero-expectation identity. Ties need care: for an atom, $F(q)-\alpha$ need not vanish even at a correct quantile. The paper allows a selectable coefficient at $x=y$, but this does not provide a universal fixed-coefficient solution for arbitrary atoms.

Propositions 3.4–3.7 analyze uniqueness in the usual smooth families of quantile and mean identification functions. For a quantile, $I=g'(y)(1_{x\le y}-\alpha)$ can be monotone for every outcome only when $g''=0$; otherwise the sign-changing indicator term makes its derivative negative somewhere. For a mean, $I=\phi''(y)(y-x)$ has derivative $\phi'''(y)(y-x)+\phi''(y)$, forcing $\phi'''=0$ over an unrestricted outcome domain. Thus the canonical functions are essentially unique up to positive scale in the analyzed setting.

Integrating a monotone identifying function in its forecast argument gives a convex expected score with its minimum at the true statistic. Conversely, differentiating a smooth strictly convex score supplies a monotone identifying function, subject to the stated regularity and integrability conditions. The variance and ES are not singly elicitable on the broad distribution classes considered, so they fail this scalar backtestability definition. Restricting distributions or adding auxiliary forecasts changes the question.

## Relative rankings and absolute testing

For recorded forecasts and outcomes, compute $\bar z=T^{-1}\sum_t Z(y_t,x_t)$. Its sign estimates average directional error; distance from zero may help compare models whose errors are on the same side. Opposite signs need a separate prudential preference. Positive and negative errors can cancel across dates, so a small pooled residual does not prove every conditional forecast is correct. This directional comparison also should not be mistaken for a proper-score ranking of arbitrary competing forecasting systems.

Section 3.1.2 constructs an absolute test by generating the reference distribution of $\bar Z$ from stored predictive distributions $P_t$. In a lower-tail test for underestimation of a positively oriented risk measure, a negative realized mean is adverse. The paper uses $\eta$ for confidence, for example 95%; the nominal rejection probability is $1-\eta$, for example 5%.

The specified simulation is:

1. Fix forecasts and the test window of $T$ dates. Preserve the predictive distributions or enough information to simulate them.
2. For each simulation $i=1,\ldots,M$, draw $X_t^{(i)}\sim P_t$ independently across dates, as specified in the paper.
3. Compute $\bar Z^{(i)}=T^{-1}\sum_t Z(y(P_t),X_t^{(i)})$.
4. Estimate the lower critical point by the empirical $(1-\eta)$ quantile of these simulated means.
5. Reject when the observed $\bar z$ is no greater than that critical point. For a two-sided test, predefine how probability is allocated to both tails.

The source does not fix $M$, integer order-statistic rounding, Monte Carlo error tolerances, or a general procedure for forecast-estimation uncertainty. Its independent draws are a model-reference construction. Overlapping horizons or serially dependent residuals require corresponding dependence treatment; substituting independent draws is not automatically valid. Nor does calibration under the forecast distributions alone prove uniform test size for every actual distribution satisfying only a scalar risk inequality.

Quantile coverage is exceptional. If the conditional quantile is exactly correct under suitable continuity, each hit has conditional probability $\alpha$. The hit count has the familiar binomial null under the appropriate sequential assumptions; its centered mean is $K/T-\alpha$, not itself an unscaled binomial variable. This pivotal null does not require storage of the entire predictive CDF. Merely matching the unconditional average hit frequency does not establish conditional independence or conditional correctness.

The paper explains why simulating a proper score under a forecast model does not automatically create the same absolute test. For squared error at a predicted mean $m_P$,

$$
E_F[(X-m_P)^2]-E_P[(X-m_P)^2]
 =\sigma_F^2-\sigma_P^2+(\mu_F-m_P)^2.
$$

A wrong mean can therefore produce a smaller realized expected score than the forecast-model benchmark if actual variance is sufficiently smaller. Proper scoring compares alternative forecasts under the same actual distribution; it does not impose an ordering across different actual and forecast distributions.

## Sharpness: direction is not economic magnitude

A sharp backtest has expectation $\psi(y,y(F))$, depending on the true distribution only through the true statistic, increasing in the forecast and decreasing in the true value. Knowing its exact expectation then identifies the true statistic by inversion.

The mean residual is sharp because $E[y-X]=y-\mu$. More generally, for $y=g(E[h(X)])$ with strictly monotone $g$, the residual $\nu[g^{-1}(y)-h(x)]$, where $\nu$ is the sign of $g$'s monotonicity, is sharp.

Quantile coverage is not sharp on the unrestricted smooth distribution class. Its expectation is $F(y)-\alpha$. Holding this value fixed holds one probability ordinate fixed, but allows the true quantile to be arbitrarily close to or far from $y$ on the indicated side. Thus an exception rate can establish underestimation without providing a monetary estimate of how much VaR is underestimated. This differs from the separate familiar limitation that VaR itself does not measure loss severity beyond the quantile.

Expectiles contain more magnitude information, but are still not sharp except at $\alpha=1/2$. Let $h(t)=E[Z_{e_\alpha}(t,X)]$. Where differentiable,

$$
h'(t)=\alpha+(1-2\alpha)F(t).
$$

Its slope lies between $a=\min(\alpha,1-\alpha)$ and $b=\max(\alpha,1-\alpha)$. If $h(y)=z>0$, the true expectile lies within the closed outer bounds $y-z/a\le e_\alpha\le y-z/b$; if $z<0$, the ordering reverses to $y-z/b\le e_\alpha\le y-z/a$. Proposition 3.18 specifies which endpoints are unattainable. For the important lower-tail case $\alpha<1/2$, the exact ranges are

$$
z>0:\quad e_\alpha\in(y-z/\alpha,\ y-z/(1-\alpha)],
$$

$$
z<0:\quad e_\alpha\in(y-z/(1-\alpha),\ y-z/\alpha].
$$

At $\alpha=1/2$, $e= y-2z=\mu$. As the expectile level approaches the extreme tails, the range can become very wide. These are limitations even with exact knowledge of the residual expectation; finite-sample estimation adds further uncertainty.

## Ridge construction and its bias

Suppose an auxiliary elicitable statistic $a(F)$ minimizes $E[S(a,X)]$, and the target statistic is a monotone transform of that minimum. Subtracting the score at a forecast auxiliary value from the forecast target gives a residual whose auxiliary error is the excess expected score. Excess score is nonnegative by optimality. Therefore the nuisance bias has a known sign even when its size is unknown.

For variance, the exact residual and expectation are

$$
Z_{\sigma^2}(v,m,x)=v-(x-m)^2,
$$

$$
E_F[Z_{\sigma^2}]=v-\sigma_F^2-(m-\mu_F)^2.
$$

A wrong mean always shifts the residual downward. At the correct mean, the residual identifies variance error exactly. Close to the mean, nuisance error is exactly quadratic. For a standard-deviation forecast $s$, replace $v$ by $s^2$. A zero-mean assumption is therefore relatively robust when the mean error is small compared with volatility, but not justified solely because it is conventional.

The general Proposition 4.2 asserts quadratic nuisance sensitivity from continuous differentiability at the optimum. That smoothness assumption alone is insufficient for an $O(\Delta a^2)$ remainder: it gives zero first derivative and typically an $o(|\Delta a|)$ statement. A bounded local second derivative or a locally Lipschitz first derivative suffices for the claimed quadratic order. The variance example meets the stronger condition exactly. For ES, a finite continuous local density provides the familiar quadratic expansion; continuity of a CDF alone need not provide that rate.

## Expected-shortfall residual and implementation

ES is the minimum expected value of the quantile score modified by an outcome-only term:

$$
\operatorname{ES}_\alpha(F)
 =\min_q\left\{-q+\frac1\alpha E_F[(X-q)_-]\right\}.
$$

Using an ES forecast $e$ and lower-quantile forecast $q$, the paper scales the ridge residual to

$$
Z_{ES}(e,q,x)=\alpha(e+q)-(x-q)_-.
$$

In positive VaR units, with $v=-q$,

$$
Z_{ES}(e,v,x)=\alpha(e-v)+(x+v)1_{\{x+v<0\}}.
$$

This is a single residual for each forecast-outcome pair. Outcomes outside the predicted tail still contribute $\alpha(e-v)$; dropping non-exceedance dates changes the test. Use ex ante forecasts, consistent P&L units and horizons, and the same tail probability for both risk statistics.

Let $q_*$ be a true quantile and $e_*$ the true ES. Define the excess expected modified quantile score

$$
D(q)=E\left[-q+\frac1\alpha(X-q)_-\right]-e_*\ge0.
$$

Then the exact population identity is

$$
E[Z_{ES}]=\alpha(e-e_*)-\alpha D(q).
$$

An underestimated ES gives a negative population residual regardless of quantile error. A correct ES can also give a negative residual if the quantile is wrong, so rejection is not unique attribution of the error to ES. When a density $f(q_*)$ exists with suitable local regularity,

$$
E[Z_{ES}]=\alpha(e-e_*)-
 \frac12 f(q_*)(q-q_*)^2+o((q-q_*)^2).
$$

At a correct quantile, divide the residual expectation by $\alpha$ to obtain ES forecast discrepancy. With quantile error, this estimates that discrepancy minus a nonnegative nuisance term. Calling the procedure sharp therefore requires the auxiliary forecast to be correct, or its bias to be negligible or bounded. The word does not mean a sample residual reveals an exact true ES without uncertainty.

For an empirical deployment, report the mean residual with uncertainty, the quantile coverage diagnostics, the predictive-reference simulation method, and the scale of plausible quantile bias. Testing quantile coverage first does not establish its forecast error is exactly zero; this is one reason the controlled-bias construction is useful.

## Numerical illustration and qualifications

The comparator is the earlier test $Z_2(e,v,x)=\alpha e+x1_{x+v<0}$. At a continuous actual density, its derivative in $v$ is $v f(-v)$, generally nonzero. The ridge residual instead has derivative $F(-v)-\alpha$, zero at a correct quantile. This explains the linear versus second-order sensitivity shown in Figures 4–5.

Example 4.3 uses actual standard-normal P&L and forecast normals $N(\mu_v,\sigma_v^2)$ whose ES is held fixed while VaR varies. It states $T=250$ and confidence 95%. A second experiment sets forecast ES one P&L unit below its actual value. The figures plot population residual expectations against VaR and a rejection region; they do not report Monte Carlo rejection frequencies, real portfolio results, or a complete power study.

There is a numerical inconsistency: the example text specifies a 5% tail, but Figure 4 marks the actual standard-normal VaR around 2.326, consistent with a 1% tail rather than 5% (whose VaR is about 1.645). Figure 5's actual-VaR marker also changes with its example. A reproduction must specify and document its own consistent normal-family parameters rather than infer a fully specified experiment from these axes.

The statement that the ridge procedure “cannot” make the illustrated type-II error concerns its population bias direction. It cannot mean that a finite 250-observation statistical test has zero probability of failing to reject an incorrect model. Tail scarcity, Monte Carlo uncertainty, serial dependence, forecast estimation, and misspecified reference distributions remain relevant.

The central usable result is the exact one-sided excess-score decomposition. It makes variance and ES validation less sensitive to auxiliary forecasts and exposes what exception counts cannot measure. The paper supplies definitions, proofs, and illustrative normal examples; it does not provide production thresholds, a portfolio data experiment, current regulatory requirements, or universal finite-sample guarantees.
