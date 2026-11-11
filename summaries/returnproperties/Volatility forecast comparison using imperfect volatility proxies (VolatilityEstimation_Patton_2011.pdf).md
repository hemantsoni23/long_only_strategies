# Volatility forecast comparison using imperfect volatility proxies

**Andrew J. Patton (2011).** *Journal of Econometrics* 160, 246–256. DOI: 10.1016/j.jeconom.2010.03.034. Source: [VolatilityEstimation_Patton_2011.pdf](../../Finance/VolatilityEstimation_Patton_2011.pdf). All 11 PDF pages, including the mathematical appendix, were inspected. References below use journal pages.

## Why this matters

A volatility forecast can win a large-sample comparison because the scoring rule rewards a biased response to measurement noise. More data do not solve that problem: they estimate the wrong ranking more precisely. Patton characterizes the loss functions that preserve forecast rankings when a conditionally unbiased proxy replaces latent conditional variance. He then isolates the subset whose rankings are unchanged by rescaling returns, derives the direction and magnitude of distortions under commonly used alternatives, and illustrates the distinction with IBM data.

The paper’s contribution is primarily an evaluation theory. It does not propose a new volatility process or establish a universally best scoring function. Robustness here means robustness of population forecast rankings to proxy noise under stated conditions. It does not mean robustness to outliers, arbitrary measurement bias, structural breaks, or model misspecification. Two robust loss functions can legitimately rank two imperfect forecasts differently because they encode different penalties.

For a researcher choosing risk forecasts, the operational implication is to specify the target, information set, proxy, and loss together. An accurate high-frequency proxy improves statistical power. A robust loss protects the ranking against a different failure: a persistent change in the objective caused by the proxy’s distribution.

## Target, information, and the precise robustness claim

Let $\mathcal F_{t-1}$ denote information available when forecasting the period-$t$ return. The target is $v_t=\sigma_t^2=\operatorname{Var}(r_t\mid\mathcal F_{t-1})$. The paper assumes zero conditional mean, so $v_t=E(r_t^2\mid\mathcal F_{t-1})$. If that assumption is relaxed, squared returns estimate the conditional second moment, and a variance forecast requires appropriate centering.

A candidate forecast $h_{i,t}>0$ is measurable with respect to the forecast information set. A proxy $Y_t=\widehat\sigma_t^2\ge0$ is observed after the period. The key restriction is

$$
E(Y_t\mid\mathcal F_{t-1})=v_t.
$$

Unconditional unbiasedness is insufficient. The conditioning information must contain the information used to construct the compared forecasts; otherwise proxy errors can be systematically associated with a forecast even if their overall mean is zero.

A loss $L(Y,h)$ is robust when the ordering of expected losses for any two forecasts is the same with $Y_t$ as with $v_t$. The definition concerns expected rankings, not equality of observed losses, equal realized rankings in every sample, or equality of absolute average loss levels. A noisy proxy can make finite-sample rankings unstable even when the expected comparison is correct.

The formal characterization uses a sufficiently rich class of nonnegative, conditionally absolutely continuous proxy distributions; twice continuously differentiable losses; a unique pointwise minimum at $Y=h$; positive forecasts in a compact set whose interior contains the optimal conditional mean; and integrability/differentiation conditions. These restrictions are in assumptions A1–A5 on p. 251. They matter when using negative powers, logarithms, zero returns, or distributions with very heavy tails.

The forecasts themselves need not be unbiased. Indeed, the IBM illustration compares two imperfect procedures. Conditional unbiasedness is required of the proxy for the latent target, not of every forecasting model entering the competition.

## Why familiar scores select the wrong variance

Sections 2.1–2.2 calculate the forecast $h_t^*$ minimizing the conditional expected proxy loss. With squared returns as proxy, many popular criteria target something other than conditional variance. Let $Y=r_t^2$ and suppress conditioning notation. The mechanisms can be derived directly:

| Loss | Minimizer of expected loss |
|---|---|
| $(Y-h)^2$ | $E(Y)$ |
| $\log h+Y/h$ | $E(Y)$ |
| $(\log Y-\log h)^2$ | $\exp\{E\log Y\}$ |
| $(\sqrt Y-\sqrt h)^2$ | $(E\sqrt Y)^2$ |
| $(Y/h-1)^2$ | $E(Y^2)/E(Y)$ |
| $\lvert Y-h\rvert$ | A median of $Y$ |
| $\lvert\log Y-\log h\rvert$ | A median of $Y$ |
| $\lvert\sqrt Y-\sqrt h\rvert$ | A median of $Y$ |
| $\lvert Y/h-1\rvert$ | A median under the distribution tilted in proportion to $Y$ |

For the last row, a continuous positive proxy gives the first-order condition $E[Y\mathbf1\{Y\le h\}]=E(Y)/2$. It is not the ordinary median. The ratio orientation is essential: the paper uses actual proxy divided by forecast. Reversing the denominator changes both the optimizer and the necessary moments.

The logarithmic and square-root criteria underforecast the mean by Jensen’s inequality. Absolute-error criteria target central quantiles rather than the mean. The proportional squared criterion overforecasts because it involves a higher moment. None of these facts is a failure of optimization: each procedure is solving the objective it was given.

To quantify the effect, Table 1 assumes standardized Student-$t$ return innovations with degrees of freedom $\nu$, multiplied by $\sqrt v$. For $\nu=6$, $\nu=10$, and the Gaussian limit, respectively, the optimal forecast divided by $v$ is:

| Criterion | $\nu=6$ | $\nu=10$ | Gaussian |
|---|---:|---:|---:|
| MSE or QLIKE | 1.00 | 1.00 | 1.00 |
| Squared log error | 0.22 | 0.25 | 0.28 |
| Squared standard-deviation error | 0.56 | 0.60 | 0.64 |
| Squared proportional error | 6.00 | 4.00 | 3.00 |
| The three ordinary absolute-error variants | 0.34 | 0.39 | 0.45 |
| Absolute proportional error | 2.73 | 2.55 | 2.36 |

Thus a Gaussian squared-return proxy can make a forecast at about 28% of the actual conditional variance optimal under squared log error. This is a population distortion, not a claim that one finite sample will always display that multiplier.

Several formulas make the calculation reproducible. For the standardized Student-$t$ family,

$$
\frac{h^*_{\mathrm{log}}}{v}=(\nu-2)\exp\left\{\psi(1/2)-\psi(\nu/2)\right\},
$$

where $\psi$ is the digamma function. For squared standard-deviation error,

$$
\frac{h^*_{\mathrm{SD}}}{v}=\frac{\nu-2}{\pi}\left[\frac{\Gamma((\nu-1)/2)}{\Gamma(\nu/2)}\right]^2.
$$

Squared proportional loss has optimum $3(\nu-2)/(\nu-4)$ times $v$, requiring $\nu>4$. Outside that range the required fourth return moment is not finite, so an apparently finite numerical backtest does not justify the population formula. The absolute proportional row is based on numerical approximation, reported as approximately $2.36+1/\nu+7.78/\nu^2$, rather than an exact universal identity.

## What better measurement accomplishes

The paper isolates measurement noise using a deliberately simple within-day model: zero-drift Brownian log prices with constant daily variance $v$ and no jumps. Split the trading day into $m$ equal intervals. Intraday returns have variance $v/m$, so

$$
RV_m=\sum_{j=1}^m r_j^2\ \overset{d}=\ \frac vm\chi_m^2,
\qquad E(RV_m)=v,\qquad \operatorname{Var}(RV_m)=\frac{2v^2}{m}.
$$

This is an analytical laboratory for proxy effects, not the empirical assertion that IBM volatility is constant within a day. Its assumptions do not automatically survive stochastic intraday volatility, jumps, overnight periods, or microstructure noise.

For a daily high–low log-price range $RG$, Brownian scaling gives $E(RG^2)=4\log(2)v$. The adjusted range is $RG^*=RG/[2\sqrt{\log2}]$; its square is unbiased for $v$. Its measurement-error variance is approximately $0.4073v^2$, compared with $2v^2$ for a daily squared return. The raw squared range is not unbiased until this normalization is applied.

Better measurement reduces distortions under nonrobust losses. Table 2 compares the adjusted range with realized variance based on $m=1$, 13, and 78 increments, corresponding approximately to daily, half-hour, and five-minute information within a 6.5-hour trading day. Under the Brownian model, the approximate optimal multipliers are:

| Criterion | Adjusted range squared | $RV_{13}$ | $RV_{78}$ |
|---|---:|---:|---:|
| MSE/QLIKE | 1.00 | 1.00 | 1.00 |
| Squared log error | 0.85 | 0.91 | 0.98 |
| Squared standard-deviation error | 0.92 | 0.96 | 0.99 |
| Squared proportional error | 1.41 | 1.15 | 1.03 |
| Ordinary absolute-error variants | 0.83 | 0.95 | 0.99 |
| Absolute proportional error | 1.19 | 1.10 | 1.02 |

For realized variance, the squared proportional multiplier is exactly $1+2/m$. The squared log multiplier can be written, by the chi-squared log moment, as $(2/m)\exp\{\psi(m/2)\}$; the article’s tabulated expression $\exp(-1.2741/m)$ is a numerical approximation. These should not be interchanged without acknowledging approximation error.

The exact squared-standard-deviation multiplier is

$$
\frac{h^*}{v}=\frac2m\left[\frac{\Gamma((m+1)/2)}{\Gamma(m/2)}\right]^2.
$$

The source also presents the Taylor approximation $1-1/(2m)+1/(16m^2)$. At $m=1$ it gives 0.5625, whereas the exact Gaussian result is $2/\pi\approx0.6366$. Footnote 12 explicitly explains this discrepancy. An implementation should use the exact gamma-function expression or the Gaussian value for $m=1$, rather than treating 0.56 and 0.64 as estimates of two different effects.

For the adjusted range, the corresponding standard-deviation-error multiplier is $2/(\pi\log2)\approx0.9184$. Even a daily high–low therefore leaves nontrivial bias in the optimum under some scores. The conclusion is not that a sufficiently accurate proxy makes the loss irrelevant; it is that proxy precision and loss robustness are separate dimensions of an evaluation design.

## The complete robust class

Proposition 1, p. 251, gives the central necessary-and-sufficient form within assumptions A1–A5:

$$
L(Y,h)=\widetilde C(h)+B(Y)+C(h)(Y-h),
\qquad \widetilde C'(h)=C(h),
$$

where $C$ is strictly decreasing and the functions satisfy the stated smoothness conditions. $B(Y)$ is independent of the forecast, so it does not affect comparisons made on a common realized proxy sequence. If the loss is normalized to be zero at $Y=h$, then $B(Y)=-\widetilde C(Y)$.

A convenient equivalent representation uses a convex function $\phi=-\widetilde C$:

$$
L(Y,h)=\phi(Y)-\phi(h)-\phi'(h)(Y-h).
$$

This is a Bregman-type loss with the forecast in the second argument. Conditional expectation yields

$$
E[L(Y,h)\mid\mathcal F]-L(v,h)
=E[\phi(Y)\mid\mathcal F]-\phi(v).
$$

The right-hand side does not depend on $h$. It therefore cancels from the difference between any two forecasts. This cancellation is the mechanism of robustness. It also explains why the absolute expected loss need not equal the loss against the latent target.

For normalized convex losses, Jensen’s inequality makes that common difference nonnegative. For another normalization, such as QLIKE written as $\log h+Y/h$, the expected level can differ by a different forecast-independent amount. Statements that noisy-proxy losses must always be larger should consequently specify their normalization; the ranking result is the invariant claim.

MSE is obtained up to an irrelevant positive factor by choosing $C(h)=-h$. QLIKE follows from $C(h)=1/h$. A normalized version is

$$
L_{\mathrm{QLIKE}}(Y,h)=Y/h-\log(Y/h)-1.
$$

At $Y=0$ this normalized expression diverges because of a term involving only the observation. Pairwise forecast comparisons can instead use $\log h+Y/h$, which remains finite for positive forecasts. One must nevertheless verify the relevant integrability assumptions for the chosen theoretical statement.

The appendix establishes necessity by exploiting how the optimum must behave for every eligible proxy distribution with the same conditional mean. This forces the forecast derivative into a form linear in the proxy’s deviation from the forecast; integrating produces the stated family. The result is stronger than demonstrating that a few familiar losses happen to work.

Proposition 2 adds two uniqueness statements, subject to the same qualifications and irrelevant constants. Among robust losses depending only on the error $Y-h$, squared error is the admissible form. Among robust losses depending only on the ratio $Y/h$, QLIKE is the admissible form. These restrictions explain why a superficially similar absolute or squared relative-error criterion does not inherit QLIKE’s guarantee.

### Pairwise noise, inference, and the role of forecast separation

The robust family also gives an explicit expression for the noise added to a pairwise comparison. Write $Y=v+\eta$ and compare $h_1$ with $h_2$. Observation-only terms cancel, leaving

$$
[L(Y,h_1)-L(Y,h_2)]-[L(v,h_1)-L(v,h_2)]
=[C(h_1)-C(h_2)]\eta.
$$

This identity is exact, not a small-noise Taylor approximation. Conditional unbiasedness removes its expected value, but the conditional variance contribution is $[C(h_1)-C(h_2)]^2\operatorname{Var}(\eta\mid\mathcal F)$. Closely related forecasts can consequently have highly correlated individual losses and relatively precise differences, while widely separated forecasts amplify proxy noise differently under different scores.

For half-MSE, $C(h)=-h$, so the loading on proxy noise is $h_2-h_1$. For QLIKE, $C(h)=1/h$, so the loading is $1/h_1-1/h_2$. These expressions show why the same proxy can lead to different test power under different robust losses. They also identify a numerical risk: extremely small positive forecasts can make QLIKE loss differences sensitive to even moderate observations. Positivity alone is weaker than a useful lower bound for numerical stability.

The distinction between a finite expected comparison and a finite variance for a test statistic should be retained. Some forecast-independent terms can have problematic moments while canceling from a difference; conversely, a finite sample average of a difference does not guarantee the long-run variance needed for a Gaussian test exists. The formal assumptions should be checked for the difference and forecast process actually used, especially with negative-power losses and heavy-tailed returns.

A simple two-point comparison illustrates how objective distortion differs from noise. Suppose the latent variance is fixed and consider forecasts equal to $v$ and to a fixed multiple $cv$. Under squared log loss, the difference in conditional expected proxy loss is determined by the proxy's expected log, not its arithmetic mean. If $E\log Y=\log v+\delta$ with $\delta<0$, the proxy comparison favors a forecast centered at $e^\delta v$. An arbitrarily large sample converges to that preference. Increasing the sample size reduces uncertainty about $\delta$'s consequences but does not set $\delta$ to zero.

Under the normalized Bregman form, by contrast, the common Jensen term removes itself from every pairwise comparison. This is why absolute loss magnitudes across proxies are not directly comparable measures of economic improvement. Replacing squared returns by a less noisy realized measure may lower every normalized average loss, even if forecasts remain unchanged. The relevant evidence for choosing a forecast is the relative loss on a common target sequence, accompanied by its uncertainty.

This also constrains how missing data should be handled. If two candidate forecasts are evaluated on different dates, observation-only terms no longer cancel over the same sample, and changing market regimes can contaminate the comparison. A faithful implementation should use a common intersection of dates for each reported pair or explicitly define a missing-data estimand. The IBM table compares common forecast sequences against alternative common proxies; it does not evaluate a separate optimized date sample for each model.

Finally, the asymmetry parameter and proxy frequency should be fixed for the substantive question before interpreting test significance. The source illustrates multiple losses to show legitimate differences in preferences. It does not supply a multiple-testing procedure for searching those losses until one model becomes significant. A later research application that performs such a search must account for it separately.

## Homogeneity and a usable one-parameter family

Robustness alone does not guarantee invariance to units. A nonhomogeneous loss can place different relative weight on high- and low-volatility periods after returns are rescaled. Proposition 3 shows that homogeneity is sufficient to prevent this: if $L(aY,ah)=a^kL(Y,h)$ for $a>0$, multiplication by the common positive factor leaves rankings unchanged. Rescaling returns by $c$ rescales variances by $a=c^2$.

Proposition 4 characterizes the homogeneous robust family with parameter $b$ and degree $b+2$:

$$
L_b(Y,h)=\frac{Y^{b+2}-h^{b+2}}{(b+1)(b+2)}-\frac{h^{b+1}(Y-h)}{b+1},\qquad b\notin\{-1,-2\}.
$$

The continuous special cases are

$$
L_{-1}(Y,h)=h-Y+Y\log(Y/h),
$$

and

$$
L_{-2}(Y,h)=Y/h-\log(Y/h)-1.
$$

At $b=0$, this is one-half squared error. Differentiating with respect to $h$ gives $h^b(h-Y)$, which makes the conditional-mean optimum transparent. This derivative is also a useful numerical check of an implementation of the generic expression and its limiting cases.

The parameter controls asymmetry. Relative to squared error, negative $b$ gives greater penalties for underprediction of variance; positive $b$ tilts toward overprediction penalties in the paper’s comparison at fixed true variance. It also changes the weighting of volatility states and the moment requirements for inference. Extremely negative powers should not be used without examining behavior near zero and very small forecast values.

The paper supplies an appendix counterexample showing that robust but nonhomogeneous losses can reverse rankings after a change of units. The issue is not whether the true conditional variance remains optimal—it does under the relevant assumptions—but whether two imperfect alternatives retain their order. Selecting the loss parameter is therefore part of defining the research objective, not another parameter to tune on the same comparison sample until the preferred model wins.

## IBM experiment: reconstructing the comparison

Section 4 uses IBM TAQ data from January 1993 through December 2003. The target is conditional variance of the daily **open-to-close** return, rather than close-to-close variance including overnight exposure. Approximately the first year, 272 observations, initializes the procedures; the remaining 2,500 observations, January 1994–December 2003, form the comparison period.

The first forecast is a 60-observation rolling average of past squared daily returns:

$$
h_{1,t}=\frac1{60}\sum_{j=1}^{60}r_{t-j}^2.
$$

The second is RiskMetrics with fixed decay parameter 0.94:

$$
h_{2,t}=0.94h_{2,t-1}+0.06r_{t-1}^2.
$$

Both use information preceding the forecast period. The rolling expression is an average of squared returns under the zero-mean convention, not a sample variance recomputed around the rolling sample mean. The decay coefficient is prescribed, not estimated from the test period. The paper states the initialization sample length but does not fully specify the numerical seed for the initial RiskMetrics variance.

Four proxies evaluate the same forecast sequences: daily squared return and realized variance from 65-minute, 15-minute, and five-minute returns. The NYSE session runs 9:30–16:00, or 390 minutes. Thus the intraday proxies contain 6, 26, and 78 intervals. Footnote 13 explains the otherwise unusual 65-minute spacing: it divides the session exactly. Replacing it with hourly observations changes both the coverage and the number of increments.

The paper argues that these proxies are plausibly conditionally unbiased for this liquid stock at the selected frequencies. It explicitly notes that this assumption is less plausible at one-second or 30-second frequencies and may fail even at five minutes for less liquid assets. It does not provide a complete TAQ cleaning specification, quote/trade selection rule, treatment of opening and closing timestamps, or a released dataset in the PDF. Those are remaining replication inputs, not details that can safely be inferred from the table.

Five loss parameters are evaluated: $b\in\{1,0,-1,-2,-5\}$. A Diebold–Mariano–West comparison is applied to the loss differential. If $d_t=L(Y_t,h_{1,t})-L(Y_t,h_{2,t})$, a positive statistic favors RiskMetrics. In generic form the statistic is $\sqrt T\bar d/\sqrt{\widehat\Omega}$, where $\widehat\Omega$ estimates the appropriate long-run variance and any estimation effects must be handled consistently. The PDF does not give the full bandwidth, finite-sample correction, or implementation choices required to reproduce every reported statistic exactly.

Table 3 reports:

| $b$ | Daily squared return | 65-minute RV | 15-minute RV | Five-minute RV |
|---|---:|---:|---:|---:|
| 1 | −1.58 | −1.66 | −1.30 | −1.35 |
| 0, MSE | −0.59 | −0.80 | −0.03 | −0.13 |
| −1 | 1.30 | 1.04 | 1.65 | −1.55 |
| −2, QLIKE | 1.94 | 2.21 | 2.73 | 2.41 |
| −5 | −0.17 | 0.25 | 1.63 | 0.65 |

The two-sided 5% reference threshold is 1.96 in absolute value. QLIKE favors RiskMetrics significantly with all three intraday proxies; the daily squared-return result is significant only at approximately the 10% level. MSE point estimates favor the rolling-window forecast, but none is statistically significant. The $b=-1$ five-minute entry is negative as printed; robustness is a population claim and does not preclude finite-sample sign changes.

The experiment supports two separate propositions. Improving the proxy can sharpen inference, as seen in QLIKE’s stronger significance with intraday data. Choosing a different robust loss can change the economically relevant ranking of imperfect models. It does not show that RiskMetrics is universally superior, that the rolling forecast is unbiased, or that all robust criteria must agree.

## Replication checks and practical limits

A minimal faithful implementation should verify positivity of forecasts, common date alignment, matching open-to-close horizons, and absence of contemporaneous returns in either forecasting recursion. It should compute loss differences directly where observation-only terms cancel, which avoids unnecessary numerical instability from very small proxies. Unit-rescaling tests should leave the sign of comparisons unchanged for the homogeneous family.

Analytical tests can be performed before using market data. Simulate a fixed Gaussian variance and verify that MSE and QLIKE select it, while squared log error selects approximately 0.2807 times that variance. Increase the number of within-day observations and verify convergence of the nonrobust optima toward the target according to the chi-squared formulas. These are proposed implementation checks derived from the theory, not additional results reported in the empirical section.

Proxy bias remains the main boundary of the guarantee. An omitted overnight component, excessive market microstructure noise, or a conditional mean treated incorrectly can violate the required conditional expectation. A precise but biased proxy is not repaired by choosing QLIKE. Conversely, a conditionally unbiased proxy can be so noisy that useful finite-sample discrimination is impossible.

The formal test also needs the relevant moments and temporal dependence assumptions. The paper observes that MSE-based inference typically imposes stronger moment requirements than QLIKE-based inference, but refers to related work for the complete power and moment analysis. It does not authorize conventional normal critical values under every heavy-tailed return process.

Finally, a variance score is not an investment utility function. Translating these forecasts into leverage, option positions, or capital limits requires a separate decision model, constraints, and costs. The paper’s durable contribution is a way to ensure that the statistical comparison is about the intended latent variance target before such economic decisions are made.
