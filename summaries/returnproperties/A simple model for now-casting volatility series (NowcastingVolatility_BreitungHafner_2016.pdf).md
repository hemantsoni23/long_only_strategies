# A simple model for now-casting volatility series

**Jörg Breitung and Christian M. Hafner (2016).** *International Journal of Forecasting* 32, 1247–1255, DOI 10.1016/j.ijforecast.2016.04.007. Source: [original PDF](../../Finance/NowcastingVolatility_BreitungHafner_2016.pdf), nine pages including both appendices, simulation tables, and the S&P 500 application. References below use printed pages and equation numbers. Several printed identities require qualifications for implementation; these are identified explicitly.

## Why this matters

A forecast of today's variance made yesterday cannot use today's return. After the close, however, the observed return contains information about the day's latent risk. Breitung and Hafner study this latter estimation problem. They show that an invertible ARMA model for log squared returns supplies a very simple current-state filter, closely related to the steady-state linear filter of a stochastic-volatility model.

The useful result is computational. Estimate an ARMA(1,1), extract its innovations, subtract an appropriate fraction of the current innovation from the observed log squared return, and calibrate a scale constant. This produces a nowcast without numerically integrating a nonlinear latent-state model. The paper also compares this estimator with SV and EGARCH and proposes a sign-dependent extension.

The change in information set is fundamental. Better fit to current latent volatility after observing today's return does not prove better forecasting before that return occurs. Nor is the object literally the conditional variance of a return after observing that same return: the latter is zero. The object is a current latent volatility or log-scale estimate. This distinction matters when using the output in a backtest: the date-$t$ nowcast is available after observing $y_t$, so it cannot set an exposure that earns $y_t$.

The symmetric ARMA construction is the clearest contribution. Its relationship to SV is a statement about linear filtering for a given reduced form, with stronger distributional assumptions needed for exact conditional expectations. The asymmetric extension has unresolved timing inconsistencies in the printed derivation and should be treated separately.

## Structural model, notation, and admissible parameters

Let $y_t$ be a zero-mean return and write

$$
y_t=\exp(h_t/2)\xi_t,\qquad E\xi_t=0,\quad E\xi_t^2=1,
$$

$$
h_t=\alpha+\beta h_{t-1}+\kappa\varepsilon_t,
\qquad \varepsilon_t=\log\xi_t^2-C,
\qquad C=E\log\xi_t^2.
$$

The innovations $\xi_t$ are independent and identically distributed. The log-scale innovation is a function of their magnitude, not an independent second shock. Thus this is a degenerate correlated-error version of a stochastic-volatility system. For a standard normal $\xi_t$, $C\approx-1.27036$ and $\sigma_\varepsilon^2=\pi^2/2$. Normal returns innovations do not imply normal log-square innovations.

For $|\beta|<1$ and finite innovation variance,

$$
Eh_t=\frac{\alpha}{1-\beta},\qquad
\operatorname{Var}(h_t)=\frac{\kappa^2\sigma_\varepsilon^2}{1-\beta^2}.
$$

The empirical case has positive persistence near one and a small positive $\kappa$. Symmetry of $\xi_t$ makes the signed return a martingale difference, provided the requisite absolute moment exists: its conditional expectation integrates an odd function of the innovation. Dependence between the magnitude shock and current scale does not itself produce directional return predictability.

Because $h_t$ depends on $\xi_t$, $e^{h_t}$ is a structural scale and is not generally the conventional variance $E(y_t^2\mid\mathcal I_{t-1})$. Direct substitution gives

$$
E(y_t^2\mid\mathcal I_{t-1})
=e^{\alpha+\beta h_{t-1}-\kappa C}
E|\xi_t|^{2(1+\kappa)}.
$$

This expression is a reconstruction from the model and assumes that moment exists. It explains why terminology inherited from independent-noise SV should not be used to identify all variance concepts without qualification. Likewise, the continuous-time integrated variance motivating the introduction is a random realized quantity; its unconditional expectation equals an unconditional return variance under suitable conditions, but the two random objects are not identical.

## ARMA reduction and a usable filter

Define $x_t=\log y_t^2$. Then

$$
x_t=C+h_t+\varepsilon_t.
$$

Substituting the lagged measurement equation into the state equation yields

$$
x_t=\alpha^*+\beta x_{t-1}+(1+\kappa)\varepsilon_t-\beta\varepsilon_{t-1},
\qquad \alpha^*=\alpha+(1-\beta)C.
$$

Set

$$
u_t=(1+\kappa)\varepsilon_t,\qquad
\theta=\frac{\beta}{1+\kappa}.
$$

The reduced form is therefore

$$
x_t=\alpha^*+\beta x_{t-1}+u_t-\theta u_{t-1}.
$$

The moving-average convention has a minus sign. Software using $u_t+\vartheta u_{t-1}$ must be passed $\vartheta=-\theta$. For the general parameterization, stationarity and invertibility require $|\beta|<1$ and $|\theta|<1$, with $1+\kappa\ne0$. The paper's simpler condition $1+\kappa>\beta$ is adequate in its positive-parameter region, not a complete condition for arbitrary signs.

For $\beta\ne0$ and $\theta\ne0$, the structural transformations are

$$
\kappa=\frac{\beta}{\theta}-1,
\qquad \sigma_\varepsilon^2=
\left(\frac{\theta}{\beta}\right)^2\sigma_u^2.
$$

The current scale is reconstructed by

$$
h_t=x_t-\frac{\theta}{\beta}u_t-C.
$$

In this structural model it is measurable from the infinite current-and-past return history when the ARMA is invertible. Operationally, obtain $\widehat u_t$ from the fitted innovations recursion and calculate the right-hand side. The exact measurable-state claim is specific to the one-shock structural model; an independent-noise SV state is not exactly observed this way.

Expanding the inverse MA polynomial gives

$$
h_t=
\frac{\theta\alpha^*}{\beta(1-\theta)}-C
+\left(1-\frac{\theta}{\beta}\right)
\sum_{j=0}^{\infty}\theta^j x_{t-j}.
$$

The printed Eq. (21) omits the final $-C$ relative to Eq. (20). Its displayed expression therefore corresponds to $h_t^*=h_t+C$, which is also the unscaled quantity used later for empirical calibration. Keeping these two objects distinct removes the apparent inconsistency. The coefficient on current $x_t$ is $1-\theta/\beta=\kappa/(1+\kappa)$. Positive past weights decline geometrically at rate $\theta$ in the empirical parameter region.

For implementation, the finite recursion is preferable to evaluating a long sum. Initialize the ARMA consistently with the selected likelihood, compute innovations sequentially, and reconstruct $h_t^*$. A fixed fitted model supplies causal current-state filtering; a full-sample parameter fit remains retrospective even when the filtering recursion itself uses no future observations.

## Estimation, scale calibration, and inference

Estimate the ARMA on transformed returns, with intercept $\alpha^*=(1-\beta)\mu_x$, where $\mu_x$ is the unconditional mean of $x_t$. Section 3 recommends exact likelihood with stationary initial conditions because $\theta$ is close to one. It warns against conditional nonlinear least squares with zero initial values. The empirical section nevertheless reports nonlinear least-squares estimation of the ARMA using numerical optimization. Exact reproduction should recognize this methodological inconsistency rather than assuming the recommended estimator generated the table.

Without specifying the distribution of $\xi_t$, $C$ is unknown. First construct

$$
\widehat h_t^*=x_t-(\widehat\theta/\widehat\beta)\widehat u_t.
$$

Then use the normalization $E\xi_t^2=1$:

$$
\widehat c=\frac1T\sum_t y_t^2e^{-\widehat h_t^*},
\qquad \widehat C=-\log\widehat c,
\qquad \widehat h_t=\widehat h_t^*+\log\widehat c.
$$

Consequently the level estimate is $\widehat c\exp(\widehat h_t^*)$. This calibration is not achieved by simply setting $C=-1.27$ unless normal innovation assumptions are imposed. In a prospective exercise, fit the calibration constant on historical data only; otherwise future squared returns affect current volatility scale.

The log transform creates large negative observations when returns approach zero. The authors recommend replacing $y_t^2$ by $y_t^2+0.001\widehat\sigma_y^2$ before taking logs. This is a numerical modification of the measurement equation, not an exact identity of the original model. Record the variance estimate used, whether it is training-only, and how zero returns are handled. The article suggests this adjustment but does not completely document its use in each reported experiment.

Gaussian pseudo-likelihood for the ARMA is simple. If $\xi_t$ is assumed Gaussian, the reduced-form variance restriction is

$$
\sigma_u^2=\frac{\pi^2\beta^2}{2\theta^2}.
$$

One can impose that restriction or model the log-chi-square innovation distribution, but the paper does not advocate these more elaborate likelihoods as its default. Distributional misspecification and tiny-return handling can matter more than small gains in parameter efficiency.

For the minus-MA convention used here, the iid-innovation Gaussian/quasi-likelihood reduced-form covariance is

$$
T\operatorname{Var}\begin{pmatrix}\widehat\beta\\\widehat\theta\end{pmatrix}
\longrightarrow
\frac{1-\beta\theta}{(\beta-\theta)^2}
\begin{pmatrix}
(1-\beta^2)(1-\beta\theta)&(1-\beta^2)(1-\theta^2)\\
(1-\beta^2)(1-\theta^2)&(1-\theta^2)(1-\beta\theta)
\end{pmatrix}.
$$

Appendix A.1 prints a negative off-diagonal element. That sign does not match the stated $u_t-\theta u_{t-1}$ convention. To check it directly, the innovation derivatives are $\partial_\beta u_t=-L(1-\beta L)^{-1}u_t$ and $\partial_\theta u_t=L(1-\theta L)^{-1}u_t$. Their expected product gives information off-diagonal $-1/(1-\beta\theta)$; inverting the two-by-two information matrix gives the positive covariance above. This is a sign-convention correction, not a modification of the fitted ARMA recursion.

Near cancellation makes identification weak: when $\beta$ and $\theta$ nearly coincide, the transformed series approaches white noise even if separate roots are near one. For $\kappa=\beta/\theta-1$, the delta-method gradient is $(1/\theta,-\beta/\theta^2)$. Apply that gradient to the covariance with the corrected sign rather than treating estimated roots as independent. At exact cancellation this nonsingular two-parameter asymptotic formula is inapplicable.

For a true SV process, the corresponding ARMA innovation need only be serially uncorrelated; it need not be independent or a martingale difference. The paper explicitly warns that its closed-form ARMA covariance cannot simply be transferred to SV estimation. A suitable sandwich covariance is needed under that interpretation.

## Relation to stochastic volatility: what is invariant

Consider the independent-error state equation

$$
h_t=\alpha+\beta h_{t-1}+\eta_t,
\qquad x_t=C+h_t+\varepsilon_t,
$$

with independent white innovations $\eta_t$ and $\varepsilon_t$. The implied transformed process has an ARMA(1,1) representation with the same second-order structure when

$$
\sigma_u^2(1+\theta^2)=\sigma_\eta^2+(1+\beta^2)\sigma_\varepsilon^2,
\qquad \theta\sigma_u^2=\beta\sigma_\varepsilon^2.
$$

Thus

$$
\sigma_\varepsilon^2=(\theta/\beta)\sigma_u^2,
\qquad
\sigma_\eta^2=[1-\theta/\beta-\theta(\beta-\theta)]\sigma_u^2.
$$

Notice the first ratio is not squared here; the one-shock structural model has a different decomposition of the same observable second moments. Nonnegative implied variances also restrict which reduced forms admit the independent-noise interpretation.

Proposition 1 extends the linear filtering result to contemporaneously correlated measurement and state errors. Let $c_{\eta\varepsilon}=E\eta_t\varepsilon_t$ and let $P_t$ be the one-step state prediction-error variance. The update gain is

$$
K_t=\frac{P_t+c_{\eta\varepsilon}}
{P_t+2c_{\eta\varepsilon}+\sigma_\varepsilon^2}.
$$

Using the stationary ARMA moment restrictions, Appendix A.2 obtains $K=1-\theta/\beta$. For a fixed reduced form and level normalization, the steady-state linear current filter has the same expression across compatible decompositions. Its estimation error and underlying latent state interpretation need not be the same.

This invariance is not a claim that arbitrary changes in structural covariance leave observable parameters unchanged. Nor does it make a non-Gaussian Kalman filter the exact nonlinear conditional expectation. The article acknowledges nonoptimality outside the Gaussian setting. For Gaussian return innovations, $\log\xi_t^2$ is non-Gaussian, so the linear-projection qualification is relevant in the central example itself. Finite initialization can additionally distinguish a finite-sample state-space filter from the infinite-past formula.

The perfect correlation concerns $\varepsilon_t=\log\xi_t^2-C$ and the scale shock, not the signed return innovation $\xi_t$. Under symmetry, a magnitude shock can be perfectly correlated with the scale innovation while the signed return shock is uncorrelated with it. Leverage asymmetry therefore needs a further mechanism.

## Simulation design and numerical evidence

The authors simulate SV, the proposed one-shock model, and symmetric EGARCH. Each design uses persistence $\beta\in\{0.90,0.98\}$, sample size $T\in\{500,2000\}$, and 1,000 replications. Innovations $\xi_t$ are standard normal; independent SV innovations are Gaussian. The source defines $CV=\operatorname{Var}(e^{h_t})/[E(e^{h_t})]^2$, which is conventionally the squared coefficient of variation, and sets it to 1 or 10.

For Gaussian SV,

$$
\sigma_\eta^2=(1-\beta^2)\log(1+CV),
$$

and choosing $E(e^{h_t})=0.0009$ implies

$$
\alpha=(1-\beta)\left[\log(0.0009)-\tfrac12\log(1+CV)\right].
$$

These are exact normal-logvariance moment relations. The weekly standard deviation is 3%, approximately 21.6% annualized using 52 weeks, and return kurtosis is $3(CV+1)$, namely 6 or 33. The article labels Tables 1 and 2 with swapped equation references: Eq. (30) is the one-shock ARMA construction and Eq. (31) is SV. The table descriptions and surrounding simulation discussion determine their meaning.

The stated target is the true simulated log scale, using

$$
\widetilde R_h^2=1-
\frac{\sum_t(h_t-\widehat h_t)^2}{\sum_t(h_t-\bar h)^2}.
$$

This does not reestimate a regression intercept and slope to flatter the fit. It can be negative, and it evaluates scale calibration as well as tracking. Parentheses in the simulation tables are cross-replication standard deviations, not standard errors of the reported average.

Representative results are:

| True process; sample; parameters | EGARCH | SV filter | ARMA filter |
|---|---:|---:|---:|
| SV; 500; $\beta=.90,CV=1$ | .360 (.143) | .528 (.115) | .588 (.095) |
| SV; 2000; $\beta=.98,CV=10$ | .679 (.232) | .807 (.051) | .806 (.051) |
| One-shock; 500; $\beta=.90,CV=1$ | .453 (.170) | .843 (.092) | .917 (.091) |
| One-shock; 2000; $\beta=.90,CV=10$ | .317 (.181) | .964 (.097) | .981 (.099) |
| EGARCH; 2000; $\beta=.90,CV=1$ | .880 (.022) | .763 (.022) | .743 (.042) |
| EGARCH; 2000; $\beta=.98,CV=10$ | .786 (.049) | .947 (.010) | .945 (.011) |

Under true SV, filtering uncertainty remains even with known parameters, so longer samples do not force the score toward one. Under the invertible one-shock model, the state is measurable from current and past transformed returns, so removing parameter uncertainty can approach exact reconstruction. EGARCH is disadvantaged under the first two designs by both its information set and misspecification; under true EGARCH, current information should not confer the same structural advantage.

Exact simulation replication has limits. Burn-in, seeds, optimizer settings, and all initial-state choices are not reported. The description of mapping $CV$ into the one-shock parameters is not fully explicit. The EGARCH calibration uses Gaussian-style exponential-moment expressions for a state driven by $|\xi|$; such a state is not exactly Gaussian, and its uncentered half-normal innovation has nonzero mean. Those expressions should be treated as the authors' stated calibration prescription, not exact lognormal identities for the printed EGARCH recursion. An exact-moment reconstruction would require its half-normal moment-generating function or numerical calibration, and would be a documented deviation from the source experiment.

## Asymmetric extension and a timing problem

The proposed threshold is $d_t=\mathbf1\{y_t>\tau\}$. The structural presentation replaces the current scale coefficient by $\kappa^+$ or $\kappa^-$ depending on this current return regime. The empirical reduced form is

$$
x_t=\alpha^*+\beta x_{t-1}+u_t-
[\theta^+d_t+\theta^-(1-d_t)]u_{t-1}.
$$

It can be implemented directly as a threshold ARMA innovation recursion and fitted by quasi-likelihood. A sufficient practical invertibility condition is uniform contraction of the regime-specific MA coefficients; full general random-coefficient conditions are not developed in the article.

The claimed structural mapping needs qualification. Eq. (34) has current coefficient $c_t=1+\kappa(d_t)$ multiplying $\varepsilon_t$ and a lag term $-\beta\varepsilon_{t-1}$. Substituting $u_t=c_t\varepsilon_t$ gives

$$
x_t=\alpha^*+\beta x_{t-1}+u_t-
\frac{\beta}{c_{t-1}}u_{t-1},
$$

which depends on $d_{t-1}$, whereas printed Eq. (37) uses $d_t$. The contemporaneous variance/moment discussion does not resolve this index mismatch. Consequently the symmetric nowcast formula cannot be extended to the printed asymmetric reduced form by an unqualified replacement of $\theta$ with its current regime value. A replication should state whether it implements Eq. (34), Eq. (37), or a corrected mapping, and should obtain the authors' code before claiming exact structural replication.

There is also a simple numerical typo: the empirical prose prints $\kappa^\pm=\beta\theta^\pm-1$, but its reported positive values require $\beta/\theta^\pm-1$, as Eqs. (38)–(39) specify. These concerns affect the asymmetric structural interpretation; they do not invalidate the symmetric ARMA algebra. Symmetry-based zero conditional mean also does not automatically carry over when positive and negative return magnitudes receive different scale responses.

## S&P 500 application and practical interpretation

The sample is demeaned daily close-to-close S&P 500 returns from January 1, 1950 through October 25, 2012, with 16,058 observations. The paper does not identify the data vendor, fully specify dividend treatment, or provide a held-out forecasting period. It estimates Gaussian EGARCH, quasi-Gaussian SV using a Kalman filter, symmetric ARMA, and threshold ARMA-L. The threshold is $\tau=-0.01$, approximately one negative unconditional standard deviation in decimal-return units, rather than the more common zero threshold.

Table 4 reports $\widehat\beta=0.9839$ for EGARCH, 0.9932 for SV, 0.9926 for ARMA, and 0.9930 for ARMA-L. The symmetric ARMA has $\widehat\theta=0.9552$, yielding $\widehat\kappa\approx0.03915$ and current-innovation gain about 0.0377. ARMA-L has $\widehat\theta^+=0.9590$ and $\widehat\theta^-=0.9359$, corresponding algebraically to $\kappa^+\approx0.03545$ and $\kappa^-\approx0.06101$ using rounded table entries; the prose's .0353 and .0605 presumably use unrounded estimates.

SV's reported state and measurement innovation variances are 0.0097 (standard error 0.0022) and 5.3156 (0.0950). The ARMA persistence standard error is 0.0015, and the MA-root standard error 0.0038. Strong persistence and substantial measurement noise are therefore central features, not incidental numerical details.

The empirical fit measure substitutes observed $x_t$ for unobserved $h_t$ and compares it to $\widehat h_t^*$ without freely fitting a slope. Values are 0.1020 for EGARCH, 0.1512 for SV, 0.1536 for ARMA, and 0.1562 for ARMA-L. Because the target is noisy log squared returns and the nowcast uses the current observation, these are not independent measurements of latent variance accuracy or next-day forecast performance. The paper reports passing portmanteau tests on squared standardized residuals but omits the full test statistics and lag settings.

Figure 1's ARMA-L and EGARCH series correlate at 91%. EGARCH puts the post-1987 crash peak above its 2008 peak, whereas the updated ARMA series reverses that ordering. The proposed explanation is the contrast between a single exceptionally large return and a sustained period of large absolute returns. This is a descriptive interpretation, not a causal decomposition of the crises.

The paper's defensible practical message is that current return information can sharpen current risk-state estimation, and an ARMA representation makes such updating inexpensive. The symmetric filter is straightforward to rebuild. Using it requires disciplined information timing, level calibration, near-zero-return treatment, and clarity about linear versus nonlinear filtering. The printed asymmetric mapping and some simulation calibration details need further resolution before one can claim complete replication of the more ambitious structural extension.
