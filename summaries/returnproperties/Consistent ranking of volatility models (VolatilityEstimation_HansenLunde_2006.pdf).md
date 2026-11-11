# Consistent ranking of volatility models

**Peter Reinhard Hansen and Asger Lunde (2006).** *Journal of Econometrics* 131, 97–121. DOI: 10.1016/j.jeconom.2005.01.005. Source: [VolatilityEstimation_HansenLunde_2006.pdf](../../Finance/VolatilityEstimation_HansenLunde_2006.pdf). This note covers all 25 PDF pages, including both appendices. Page pointers use journal pagination.

## Why this matters

When the outcome being forecast is latent, model selection depends on how the outcome is measured. Hansen and Lunde show that replacing conditional variance by a noisy proxy can change the limiting ranking of volatility models. An inferior forecast may then win with probability approaching one as the evaluation sample grows. This is different from having wide confidence intervals: the comparison can be precise and still target the wrong ordering.

The paper separates the population loss against the true target, the population loss against a proxy, and the empirical average of that proxy loss. It derives sufficient conditions for the first two rankings to coincide and conditions under which the third converges to the second. It then applies the framework to squared-error losses and Mincer–Zarnowitz regressions, illustrating practical consequences with IBM data and simulations.

The innovation is this distinction between measurement-induced changes in the objective and ordinary sampling error. High-frequency realized variance helps with both, but is not automatically unbiased or immune to market microstructure. The article gives a conceptual and partially reproducible experimental framework; several printed formulas and omitted implementation details prevent an exact numerical replication from the PDF alone.

## Three rankings and two kinds of error

Let $H_i=(h_{i,1},h_{i,2},\ldots)$ be the forecast sequence from model $i$. The latent target is $v_t$, its observable proxy is $Y_t$, and a smaller loss $L$ is preferred. In the stationary special case, define

$$
\psi(H_i)=E[L(v_t,h_{i,t})],\qquad
\widetilde\psi(H_i)=E[L(Y_t,h_{i,t})],
$$

and

$$
\widehat\psi_n(H_i)=\frac1n\sum_{t=1}^nL(Y_t,h_{i,t}).
$$

The paper’s general framework permits limits of time averages of expected losses, so stationarity is not needed merely to define the first two criteria. Its assumptions require integrability and finite limits. An almost-sure limit is also introduced for the empirical criterion.

The true ranking is induced by $\psi$, the approximate ranking by $\widetilde\psi$, and the empirical ranking by $\widehat\psi_n$. The difference between the empirical and approximate rankings is sampling error. A difference between true and approximate rankings is called objective-bias. The latter depends on the interaction of loss curvature and measurement error, rather than on the length of the evaluation sample.

Because forecasts can tie, the formal objects are preorderings. The distinction between equivalence and weak asymptotic equivalence matters: a law of large numbers can consistently recover strictly ordered pairs without making two exactly tied forecasts have exactly equal empirical average losses. Claims about consistency should therefore not be extended to perfect finite-sample or asymptotic recovery of all ties.

Let $g(H)=\psi(H)-\widetilde\psi(H)$. If $g(H_i)-g(H_j)=0$ for every compared pair, the true and approximate rankings coincide. This is sufficient, not necessary. A small model-dependent distortion may leave a widely separated pair in the same order. Consequently, failure of a sufficient condition means reversal is possible, not that every dataset or candidate set must exhibit a reversal.

## A usable sufficient condition and its proof

Write $Y_t=v_t+\eta_t$. The main volatility setting assumes $v_t$ and all $h_{i,t}$ are measurable with respect to $\mathcal F_{t-1}$ and

$$
E(\eta_t\mid\mathcal F_{t-1})=0.
$$

The relevant information set must include that used by the forecasts. A proxy with zero unconditional bias can still be unsuitable if its conditional errors are correlated with forecast differences.

Theorem 2 considers a loss having the same functional form for the latent and observed arguments. One sufficient condition is that its first derivative with respect to the target argument does not depend on the forecast. A more useful condition is that its second derivative with respect to the target does not depend on the forecast, combined with the martingale-difference restriction above.

A direct way to see the latter result is to write such a loss locally and globally on its domain as

$$
L(y,h)=A(y)+B(h)y+C(h).
$$

The difference between two forecast losses is affine in $y$. Taking conditional expectations substitutes $v$ for $Y$, while the observation-only term $A(Y)$ cancels. Thus expected pairwise loss differences are exactly preserved. This argument gives the central cancellation without requiring the individual expected loss levels to match.

The appendix expresses the same logic through a Taylor expansion. The first-order proxy-error term has expectation zero, and the remaining target-curvature contribution is common to all forecasts. What is crucial is forecast independence of curvature, not that the loss must literally be a quadratic polynomial in the target. A target-only nonlinear term is harmless to rankings.

When curvature depends on the forecast, a small-error expansion gives the diagnostic approximation

$$
E[L(v+\eta,h)-L(v,h)\mid\mathcal F]
\approx\frac12 L_{yy}(v,h)E(\eta^2\mid\mathcal F).
$$

The resulting difference across forecasts can grow with measurement-error variance. This is a local approximation; the paper’s stronger statements about increasing noise require additional regularity assumptions in Appendix B. They are not a universal theorem that variance alone orders the distortion for every nonlinear loss and every error distribution. In particular, larger noise can move observations outside a loss’s domain, as with logarithms.

For empirical averages, Theorem 4 uses stationarity and ergodicity of the proxy-loss process to establish almost-sure convergence to its expected value. Combined with equality of expected pairwise differences, this consistently recovers strict true rankings. A comparison procedure still needs additional assumptions to obtain standard errors and significance tests; ergodicity alone is not a central limit theorem.

## Applying the result to variance forecasts

The price process is expressed in log prices $p_t$, daily returns are $r_t=p_t-p_{t-1}$, and the target is $v_t=\operatorname{Var}(r_t\mid\mathcal F_{t-1})$. The source assumes zero conditional mean, making the squared return conditionally unbiased for variance. If mean effects are retained, the relevant proxy is a suitably centered squared innovation; subtracting an estimated mean introduces its own error.

For squared error,

$$
(Y_t-h_t)^2=(v_t-h_t)^2+2(v_t-h_t)\eta_t+\eta_t^2.
$$

The cross term has zero conditional expectation and the final term is common to every forecast. Thus MSE has the same population ranking under any proxy satisfying the conditional-unbiasedness and moment requirements. A daily squared return can therefore be an extremely noisy but ranking-consistent MSE evaluation target.

The logarithmic loss is

$$
L_{\log}(Y,h)=[\log Y-\log h]^2.
$$

Its second derivative with respect to $Y$ is

$$
L_{yy}(Y,h)=\frac{2[1-\log(Y/h)]}{Y^2}.
$$

The expression printed on p. 106 contains an extra factor inside the numerator; direct differentiation gives the formula above. The essential source conclusion remains correct: the curvature depends on $h$, so conditional unbiasedness in levels does not preserve rankings under squared log loss.

The population optimizer makes the issue transparent. Against a random positive proxy, squared log loss is minimized at $\exp\{E[\log Y\mid\mathcal F]\}$, generally below $E[Y\mid\mathcal F]=v$. If log-proxy bias were zero, the analogous robust argument could instead be applied to log variance. But unbiasedness in levels and unbiasedness in logs are different assumptions.

A log transformation can reduce numerical domination by very large observations while introducing objective-bias. These are separate properties. It is therefore insufficient to justify the transformation solely because the untransformed regression or loss is sensitive to large squared returns.

## Regression-based rankings: what an $R^2$ does and does not measure

The paper also considers regressions of a transformed proxy on a constant and a transformed forecast:

$$
\varphi(Y_t)=a+b\varphi(h_t)+u_t.
$$

Common choices are $\varphi(y)=y$ and $\varphi(y)=\log y$. With a single regressor and intercept, population $R^2$ ranks forecasts according to

$$
\frac{\operatorname{Cov}(\varphi(Y),\varphi(h))^2}
{\operatorname{Var}(\varphi(h))},
$$

since the omitted denominator $\operatorname{Var}(\varphi(Y))$ is common across models evaluated on the same target and dates.

For the level regression, a constant conditional mean of proxy error suffices: the intercept absorbs that constant, and covariance with an available forecast is unchanged. This is weaker than requiring the proxy to be conditionally unbiased. The price is that $R^2$ does not distinguish $h_t$ from $a_0+b_0h_t$ with $b_0\ne0$. A seriously miscalibrated scale or level can achieve the same ranking. Checking intercept zero and slope one is a different forecast-rationality question.

For log regressions, a sufficient and directly interpretable requirement is

$$
E[\log Y_t-\log v_t\mid\mathcal F_{t-1}]=c,
$$

where $c$ is constant. A proxy with multiplicative noise whose conditional log moment is constant satisfies this requirement. Consequently, log-regression $R^2$ is not inherently inconsistent in every model. What fails is the inference that level unbiasedness by itself guarantees its consistency.

The source formulates a more general sufficient condition in terms of all conditional moments of measurement error multiplied by derivatives of $\varphi$. Using an infinite Taylor expansion requires its convergence and relevant interchanges; the simple conditional-mean condition above states the cancellation needed in the covariance calculation without assuming that smoothness alone establishes an infinite expansion. The article’s formula for the higher derivatives of the logarithm on p. 108 also has a factorial in the denominator where repeated differentiation gives a factorial in the numerator. This typo does not change the constancy argument.

These caveats help delimit the empirical interpretation. When proxy changes alter an $R^2$ ranking, the effect may reflect objective-bias, finite-sample variation, different conditional proxy biases, or some combination. Since true variance is unobserved in the real-data application, that application cannot by itself identify which component caused every individual switch.

### An explicit measurement-error decomposition for regression fit

The level-regression result can be sharpened into a useful reconstruction formula. Under conditional unbiasedness, write $Y=v+\eta$ and assume the second moments needed below exist. Since both $v$ and an available forecast $h$ are measurable before the period, $\operatorname{Cov}(\eta,v)=\operatorname{Cov}(\eta,h)=0$. Therefore

$$
\operatorname{Var}(Y)=\operatorname{Var}(v)+\operatorname{Var}(\eta),
\qquad
R^2(Y,h)=R^2(v,h)\frac{\operatorname{Var}(v)}{\operatorname{Var}(v)+\operatorname{Var}(\eta)}.
$$

The attenuation factor is common across forecasts evaluated against the same proxy. This derivation explains how all models can have much lower observable $R^2$ values while their ordering remains correct. It is a consequence of the source's assumptions, not an additional empirical estimate of the measurement-error variance in IBM data.

It also makes clear why scale calibration cannot be inferred from $R^2$. If $h=10v$, the regression can rescale the forecast and achieve the same explanatory power as $h=v$, even though a direct squared-error score strongly prefers the correctly scaled forecast. A model-selection pipeline should not report regression ranking as though it also established accurate absolute risk levels.

For MSE, pairwise differences have an analogous simplification. For forecasts $h_i$ and $h_j$,

$$
D_t(Y)=L(Y,h_i)-L(Y,h_j)
=2Y(h_j-h_i)+h_i^2-h_j^2,
$$

so

$$
D_t(Y)-D_t(v)=2\eta_t(h_j-h_i).
$$

The proxy's squared-error term cancels before averaging. This identity is why calculating pairwise uncertainty directly is preferable to combining separate average-loss standard errors as though the losses were independent. Conditional measurement noise contributes $4(h_j-h_i)^2\operatorname{Var}(\eta_t\mid\mathcal F_{t-1})$ to the one-period variance of the difference, even though it contributes no conditional bias.

For serially dependent loss differences, the variance of their sample mean also depends on lagged covariances. The paper's consistency result alone does not select a HAC bandwidth or bootstrap block length. Those choices, together with any parameter-estimation corrections, belong in an explicitly documented inference implementation. Making the proxy more precise reduces one source of uncertainty; it does not eliminate the need to account for serial dependence or the fact that forecasts were estimated.

## IBM data, estimation windows, and three proxies

Section 4.1 uses IBM TAQ data from 3 January 1995 through 21 February 2002, totaling 1,795 trading days. The first 1,250 observations, ending 13 December 1999, form the estimation sample. The remaining 545 observations are used for out-of-sample evaluation. The models are estimated from daily close-to-close returns; intraday midquotes from 9:30 a.m. to 4 p.m. construct a measure of open-to-close variation.

The eight reported models are ARCH(1), GARCH(1,1), EGARCH(1,1), APARCH(1,1), threshold GARCH(1,1), FIGARCH(0,0), FIGARCH(1,1), and FIAPARCH(1,1). Their definitions are referenced to the original model papers. The PDF does not report every parameter estimate, optimization constraint, likelihood innovation distribution, fractional-lag truncation, initialization rule, or exact re-estimation schedule for this eight-model comparison. Therefore the experiment’s structure can be reconstructed, but exact fitted forecasts cannot be recovered solely from its tables.

The three proxies are:

$$
Y_t^{sc}=\widehat c\,RV_t,
\qquad Y_t^{on}=RV_t+(p_t^{open}-p_{t-1}^{close})^2,
\qquad Y_t^{sq}=(p_t^{close}-p_{t-1}^{close})^2.
$$

The printed scaling factor is the **average of ratios**,

$$
\widehat c=\frac1n\sum_{t=1}^n\frac{r_t^2}{RV_t}.
$$

It is not the ratio of average squared returns to average realized variance. These produce different values and should not be substituted silently. The exact dates used to estimate the scaling factor are not fully specified by the notation in the PDF. A real-time replication should identify a training-only choice and disclose any departure from the published implementation.

Scaling the daytime proxy or adding the overnight squared return attempts to align it with the close-to-close target. Neither guarantees conditional unbiasedness without additional assumptions. The source argues that scaled RV is typically the most precise, followed by RV plus overnight squared return, followed by the squared daily return. That ordering is conditional on reasonable assumptions about the components, not a universal identity.

### Fourier construction and a normalization issue

Appendix A uses the Malliavin–Mancino Fourier approach rather than a simple sum of regularly sampled squared returns. Let observed log prices be $p_i=p(t_i)$, and map timestamps to $\tau_i=2\pi(t_i-t_0)/(t_N-t_0)$. The coefficients printed are

$$
a_k=\frac{p_N-p_1}{\pi}+\frac1\pi\sum_{i=1}^{N-1}p_i[\cos(k\tau_i)-\cos(k\tau_{i+1})],
$$

$$
b_k=-\frac1\pi\sum_{i=1}^{N-1}p_i[\sin(k\tau_i)-\sin(k\tau_{i+1})].
$$

The truncation is $m=80$. The displayed statistic is $\pi(2m)^{-1}\sum_{k=1}^m(a_k^2+b_k^2)$. However, equation (A.1) identifies that expression as the zeroth Fourier coefficient $a_0(\sigma^2)$, equal to $1/(2\pi)$ times integrated variance on the transformed interval. The next page labels the same expression $RV_t$ without resolving the factor $2\pi$.

This is a material normalization ambiguity. A conventional integrated-variance implementation must reconcile time transformation and coefficient normalization, and should verify its scale on a simulated constant-volatility Brownian path. Multiplying all daytime RV values by a common constant cancels inside the average-ratio scaled proxy, but does **not** cancel when unscaled daytime RV is added to an overnight squared return. The paper supplies neither code nor an explicit resolution of this discrepancy. The formula should therefore not be used as an unquestioned production estimator.

The method incorporates irregular observations without interpolating a regular price grid. That does not establish robustness to quote errors, bid–ask effects, timestamp conventions, or market microstructure. Cleaning rules and opening/closing quote selection remain unspecified in this PDF.

## Reported IBM results

Table 1 reports MSE in levels and squared log error for the three proxies. The selected entries below retain the original numerical scale; the PDF does not fully document its return-unit convention, so they should not be relabeled as decimal-return variance units.

| Model | MSE scaled RV | MSE RV + overnight | MSE squared return | Log MSE scaled RV | Log MSE RV + overnight | Log MSE squared return |
|---|---:|---:|---:|---:|---:|---:|
| ARCH(1) | 39.924 | 168.30 | 305.06 | 0.492 | 0.599 | 11.882 |
| GARCH(1,1) | 30.722 | 159.77 | 297.01 | 0.298 | 0.479 | 12.441 |
| EGARCH(1,1) | 25.434 | 155.25 | 289.37 | 0.260 | 0.459 | 12.506 |
| APARCH(1,1) | 23.358 | 153.66 | 286.52 | 0.269 | 0.485 | 12.644 |
| Threshold GARCH | 24.711 | 155.00 | 288.49 | 0.261 | 0.471 | 12.594 |
| FIGARCH(0,0) | 31.460 | 161.89 | 299.03 | 0.338 | 0.543 | 12.573 |
| FIGARCH(1,1) | 32.057 | 161.89 | 299.51 | 0.344 | 0.564 | 12.765 |
| FIAPARCH(1,1) | 24.334 | 155.53 | 288.11 | 0.293 | 0.533 | 12.883 |

APARCH wins the level-MSE comparison for every proxy. EGARCH wins squared log error for both intraday-based proxies, while ARCH wins when the target is squared daily return. This is consistent with the paper’s concern, but the empirical table does not reveal the latent true winner under each loss.

Measurement precision changes sharply. APARCH’s reported MSE standard errors are 5.147, 120.01, and 142.54 for scaled RV, RV plus overnight, and squared return. These are standard errors of each model’s average loss, not of the difference between two models. A pairwise difference can be much more precise because the losses share large common movements. The source notes this covariance explicitly and does not justify declaring model superiority simply from non-overlap or overlap of individual intervals.

Table 2’s level-regression $R^2$ values are displayed on a percentage scale. APARCH leads with 36.052, 7.329, and 4.525 for the three proxies; GARCH records 19.907, 4.328, and 1.808. The dramatic decline when using squared returns illustrates how a weak observed fit can result from proxy noise rather than from an absence of conditional-variance predictability.

The log-regression winners change: threshold GARCH gives 52.442 with scaled RV; FIAPARCH gives 42.931 with RV plus overnight; EGARCH gives 2.625 with squared returns. Calibration and proxy precision again have to be distinguished from the ranking itself.

## Simulation design, numerical results, and unresolved inputs

The simulation uses GARCH, EGARCH, and APARCH data-generating processes calibrated to IBM estimates. There are 500 trials, with 5,000 observations for initial estimation and an additional 100, 250, or 500 observations for recursive one-step-ahead evaluation. Unlike the empirical eight-model table, the figure labels compare seven models: ARCH, GARCH, EGARCH, APARCH, threshold GARCH, a two-component model, and a two-component threshold model. Treating these as the same candidate set would misreplicate the experiment.

Using $\epsilon_t$ for the return innovation and $\sigma_t$ for its conditional standard deviation, the reported recursions are

$$
\sigma_t^2=0.043+0.121\epsilon_{t-1}^2+0.846\sigma_{t-1}^2,
$$

$$
\log\sigma_t^2=-0.121+0.163\frac{|\epsilon_{t-1}|-0.478\epsilon_{t-1}}{\sigma_{t-1}}+0.975\log\sigma_{t-1}^2,
$$

and, as printed,

$$
\sigma_t^{0.433}=-0.025+0.078(|\epsilon_{t-1}|-0.555\epsilon_{t-1})^{0.433}+0.918\sigma_{t-1}^{0.433}.
$$

The negative APARCH intercept is present in the rendered original, not an extraction artifact. A literal recursion can produce a negative right-hand side after sufficiently small innovations, incompatible with a positive fractional power of standard deviation. The PDF does not explain a constraint, truncation, alternative parameterization, or correction. Replacing −0.025 with +0.025 would be an unverified alteration. Exact reproduction requires clarification or original code.

The source also does not fully specify the simulation innovation distribution, burn-in, initial variances, numerical estimators for all candidates, or all parameter constraints. The EGARCH expression uses an uncentered absolute standardized innovation; converting it to a centered parameterization requires adjusting its intercept. These are material inputs, particularly when comparing simulated selection frequencies.

Figures 1–3 compare losses against both actual conditional variance and the squared-return proxy. With a GARCH generating process and 500 forecast observations, GARCH wins MSE against true variance in about 67% of trials and squared log loss in about 79%. Against squared returns, its win frequencies fall to about 26% and 8%, respectively. The two-component threshold model wins squared log loss against squared returns about 43% of the time.

With EGARCH generating the data and 500 forecasts, the true EGARCH wins approximately 75% under MSE against true variance and 84% under squared log loss against true variance. Its squared-return-proxy win rates are approximately 44% and 18%. The two-component threshold competitor wins about 50% under the latter criterion. These figures illustrate that more evaluation observations need not rescue a distorted objective.

The APARCH case is more distinctive. At 500 forecasts, the true APARCH wins approximately 98% under latent-target MSE and 99% under latent-target log loss; proxy-based frequencies are about 60% and 42%. It remains the most frequent winner because competing models reproduce its unusual power dynamics poorly. This does not invalidate the theory: a distortion need not reverse a sufficiently large true separation. Lower-ranked models can still be reordered.

A proportion from 500 independent trials has binomial Monte Carlo standard error at most about 2.24 percentage points, an uncertainty calculation supplied here rather than reported as a confidence interval in the paper. The figures give rounded frequencies, not exact trial counts or a hypothesis test establishing all differences.

## How to use the result responsibly

A reconstruction should first establish a consistent target horizon and units, then create forecasts without look-ahead, then calculate several clearly defined proxies. It should separately inspect calibration, loss rankings, and uncertainty in pairwise loss differences. Simulations should preserve the latent variance path so that proxy-based and latent-target rankings can be compared directly.

The theoretical checks are simple and valuable. Under conditionally unbiased simulated noise, pairwise MSE differences should have the same expectation with true and measured variance. Squared log loss should generally fail that check. For a multiplicative proxy with constant conditional log bias, log-regression $R^2$ can retain its ranking even though squared log loss remains biased toward a different level. These checks separate mechanisms that the word “logarithmic” otherwise obscures.

The article provides an additional reason to use precise realized measures, while explicitly warning that excessively high-frequency returns suffer microstructure bias. Its consistency argument does not allow arbitrarily fine sampling of noisy observed prices. A lower-variance proxy is not necessarily a better evaluation target if it acquires a model-dependent conditional bias.

The findings concern forecast assessment, not portfolio returns or execution performance. No trading rule, transaction-cost schedule, leverage constraint, or economic-utility comparison is supplied. The practical contribution is to prevent a research process from selecting the wrong volatility model because it confuses what was observed with what it intended to predict.
