# The Econometrics of Ultra-High-Frequency Data

Robert F. Engle, *Econometrica* 68(1), January 2000, pp. 1–22. [Source PDF](../../Finance/GARCH_Engle_2000.pdf). The supplied file contains a JSTOR cover and the complete twenty-two-page article, including references. All twenty-three PDF pages were read visually. Printed page numbers equal PDF page numbers minus one. There is no separate appendix; the main quasi-likelihood theorem refers to an earlier proof rather than supplying it.

## Why this matters

The time between transactions is an observation, not merely an inconvenient gap in a regularly sampled return series. A long period without trading can convey information about news, liquidity demand, and the next price change. Aggregating trades into fixed clock intervals discards this information and creates many zero-return intervals at fine sampling frequencies. Engle combines a model for transaction arrival times with a model for returns conditional on those times, then distinguishes variance per transaction from variance per unit of time.

The contribution is a general marked-point-process formulation, a semiparametric arrival-hazard estimator based on autoregressive conditional durations, and an IBM application linking durations to volatility. The autoregressive conditional duration, or ACD, model comes from Engle and Russell's earlier work. The paper's advance is to use that structure as one part of a joint model and to show how a flexible duration distribution and an irregular-time GARCH model fit together. It does not estimate a complete structural model of informed trading, nor demonstrate a profitable trading strategy.

For implementation, three distinctions matter. First, estimating a return distribution conditional on an already observed duration differs from forecasting a return before that duration is known. Second, the inverse conditional mean duration generally differs from the conditional mean inverse duration. Third, fitting a conditional mean duration by exponential quasi-likelihood does not establish that durations are exponentially distributed. The IBM results are useful partly because the empirical hazard strongly rejects that simple distributional picture while the mean model remains informative.

## Joint model, conditioning, and likelihood

Let $t_i$ be the time of transaction $i$, $x_i=t_i-t_{i-1}>0$ its duration, and $y_i$ a vector of marks, such as returns, transaction size, or quotes. Let $\mathcal F_{i-1}$ contain past durations and marks. The starting point is

$$
f(x_i,y_i\mid\mathcal F_{i-1};\theta)
=g(x_i\mid\mathcal F_{i-1};\theta_1)
q(y_i\mid x_i,\mathcal F_{i-1};\theta_2).
$$

This factorization is an identity for a joint density, not an assumption that durations and returns are independent. The second factor explicitly conditions on the current duration. The duration model can also include lagged marks, although the particular IBM ACD specification omits them. Omitting past prices, spreads, and volume from $g$ is therefore an empirical restriction; it is not imposed by the framework.

For elapsed time $u=t-t_{i-1}$ since the last event, the conditional arrival intensity is the duration hazard

$$
\lambda_i(t)=
\frac{g(u\mid\mathcal F_{i-1})}
{\int_u^\infty g(s\mid\mathcal F_{i-1})\,ds}.
$$

The survival denominator conditions on the fact that no new transaction has yet occurred. Simply evaluating the density at $u$ would omit that information. The counting-process interpretation is the limiting probability of an event in a short following interval divided by its length. To forecast the next mark without knowing when it occurs, integrate over the duration:

$$
p(y_i\mid\mathcal F_{i-1})
=\int_0^\infty
g(s\mid\mathcal F_{i-1})
q(y_i\mid s,\mathcal F_{i-1})\,ds.
$$

For several future transactions or a fixed clock-time horizon, the paper proposes simulation from the joint density when analytic integration is unavailable. Simulate a duration, then its conditional mark, update the state, and repeat. A calendar-horizon forecast requires stopping or accounting for the last interval at the horizon; a fixed number of simulated trades answers a different question.

The conditional log likelihood is the sum of the log duration and conditional-mark densities. If their parameter blocks are variation free, separate maximization recovers the joint optimum. When parameters estimated from the duration model enter the return model through expected durations, that separation no longer gives the efficient joint maximum likelihood estimator. Engle uses consistent first-step estimates in the second step and regards the potential efficiency loss as manageable with a large transaction sample. Large sample size does not itself remove generated-regressor uncertainty; a modern implementation should account for it when conducting joint inference.

The framework also admits latent states, but integrating them out generally requires simulation or other filtering methods. The paper does not implement such a latent-state model. Its empirical attraction is that conditional-duration and conditional-variance states can instead be updated deterministically from observed histories.

## ACD scale model and distribution-robust mean estimation

Define

$$
\psi_i=E[x_i\mid\mathcal F_{i-1}],\qquad
x_i=\psi_i\varepsilon_i,\qquad
E[\varepsilon_i]=1.
$$

For the scale-family hazard construction, the positive disturbances $\varepsilon_i$ are independent and identically distributed with density $p_0$, survival $S_0$, and hazard $\lambda_0=p_0/S_0$. Then

$$
g(x_i\mid\mathcal F_{i-1})
=\frac1{\psi_i}p_0(x_i/\psi_i),
\qquad
\lambda_i(t)=\frac1{\psi_i}
\lambda_0\!\left(\frac{t-t_{i-1}}{\psi_i}\right).
$$

Both the elapsed-time argument and the hazard level scale with $\psi_i$. This is an accelerated-failure-time model. It is generally different from multiplying an unchanged baseline hazard by an exponential covariate function, as in a proportional-hazards model. Particular exponential or Weibull specifications can connect the two.

A consequential implementation correction is needed in printed equation (15), on PDF page 8. The displayed duration contribution is $\log p_0(x_i/\psi_i)$ without the scale Jacobian. Under the immediately preceding definition of $p_0$ as the density of $\varepsilon_i$, the proper contribution is

$$
\log g(x_i\mid\mathcal F_{i-1})
=\log p_0(x_i/\psi_i)-\log\psi_i.
$$

This follows directly by change of variables and is a correction to the displayed expression, not a claim about the author's software. The subsequent exponential quasi-likelihood, equation (21), includes the required $\log\psi_i$ term and is the appropriate implementable objective.

With a unit-mean exponential reference density, maximize

$$
\ell_N(\theta)
=-\sum_{i=1}^N
\left[\log\psi_i(\theta)+\frac{x_i}{\psi_i(\theta)}\right].
$$

Correct specification of the conditional mean makes the score a martingale difference even when the exponential density is wrong. With $d_i=\partial\log\psi_i/\partial\theta$, the log-likelihood score is

$$
s_i=(x_i/\psi_i-1)d_i.
$$

Its conditional expectation is zero at the true mean parameters. In a positive-information convention, the expected negative Hessian is $E[d_id_i^\top]$. A robust asymptotic covariance takes the sandwich form

$$
\operatorname{Avar}(\widehat\theta)
=\frac1N A^{-1}BA^{-1},
\quad
A=E[d_id_i^\top],
\quad
B=E[s_is_i^\top].
$$

Sample analogues use the fitted derivatives and score outer products. Under the correctly specified conditional mean, the score has no serial covariance at nonzero lags, despite dependence in durations. If that mean restriction fails, the simple sandwich is not automatically a cure for misspecification.

The population reason that exponential quasi-likelihood identifies the mean can be made explicit. Write the true conditional mean as $\psi_{0i}$ and a candidate as $\psi_i=a_i\psi_{0i}$. Conditional on the past, the expected candidate-minus-true log criterion is

$$
E[\ell_i(\psi_i)-\ell_i(\psi_{0i})\mid\mathcal F_{i-1}]
=-\log a_i-a_i^{-1}+1\le0.
$$

Equality holds only at $a_i=1$. This derivation uses the conditional first moment, not an exponential conditional density. Identifying the mean function as a function of the parameters, controlling the stochastic criterion uniformly, and establishing its limiting curvature are the additional steps supplied by the theorem's assumptions. The score calculation also shows why multiplying all durations by a fixed unit conversion should change the fitted level parameter but not the dimensionless dynamics. Calendar seconds, seasonally normalized durations, and trades as an event index must nevertheless remain separate in output labels.

Theorem 1 requires an interior identified parameter in a compact parameter space, positive measurable conditional means, continuous second derivatives, uniform laws of large numbers, suitable Hessian convergence, nonsingular information and score covariance, and a score central limit theorem. The result does not prove these conditions for every ACD recursion. Engle specifically warns that unit roots in the duration dynamics complicate verification. The asymptotic argument can relax independent disturbances for estimation of the mean; estimating a single baseline hazard from standardized residuals requires the stronger common-distribution scale-family structure.

## Semiparametric hazard and IBM duration evidence

After fitting $\psi_i$, form $\widehat\varepsilon_i=x_i/\widehat\psi_i$. Estimate their baseline hazard nonparametrically and rescale it to obtain the transaction-specific intensity. The paper uses a nearest-neighbor estimator. For ordered standardized durations $u_{(j)}$, a window extending approximately $k$ observations to either side gives

$$
\widehat\lambda_0(u_{(j)})
=\frac{2k}
{n_j\{u_{(j+k)}-u_{(j-k)}\}},
$$

where $n_j$ is the number still at risk at that duration. This is failures divided by risk-set exposure, with a variable bandwidth. At the sample boundaries the window must be modified; the first window covers the smallest $2k$ durations. The PDF explains that boundary idea but does not give production code, a complete tie rule, or every endpoint convention. The IBM figures use 2,000 neighbors on each side. A flat hazard would be consistent with an exponential standardized duration; a declining hazard is not.

The IBM transaction data come from the NYSE TORQ database for November 1990 through January 1991, initially about 60,000 trades. Trades outside 9:30 a.m.–4:00 p.m., trades without reported quotes, Thanksgiving Friday, the day before Christmas, and the day before New Year are removed. Overnight durations are excluded. Consolidating to unique transaction times leaves 52,146 times and removes zero durations. Table I contains 52,145 observations after endpoint adjustment; the conclusion mentions 52,144 transactions. These closely related counts should not be conflated into a single unexplained sample size.

The source interprets simultaneous transactions as one ownership-transfer event whose size can be aggregated into a mark. It does not fully specify the tie-breaking and quote-selection code. Those details matter for reconstructing midquotes, total trade size, and the large-trade indicator. The retained timestamps have a one-second lower resolution; inverse durations are consequently bounded within each intraday adjustment scale. That empirical truncation matters later when expectations of reciprocal durations are discussed.

Durations are first divided by a fitted time-of-day pattern. Engle estimates a piecewise-linear spline with knots at 9:30, 10:00, 11:00, noon, 1:00, 2:00, 3:00, 3:30, and 4:00. The resulting dimensionless durations measure time relative to the normal duration at that point in the trading day. Their observed range is 0.027–23.8 and standard deviation is 1.32. The Ljung–Box statistic at fifteen lags is 8,040; the first fifteen autocorrelations lie roughly between 0.075 and 0.15. The first two hundred autocorrelations are positive.

Two conditional-mean models are fitted. The ordinary ACD(1,1) is

$$
\psi_i=\omega+\alpha x_{i-1}+\beta\psi_{i-1}.
$$

The component version separates a slowly moving duration level:

$$
q_i=\rho q_{i-1}+\omega(1-\rho)
+\varphi(x_{i-1}-\psi_{i-1}),
$$

$$
\psi_i=q_i+\alpha(x_{i-1}-q_{i-1})
+\beta(\psi_{i-1}-q_{i-1}).
$$

The second specification is an ACD(2,2) written through its roots. Here $\omega$ is the long-run level of the component equation, rather than the intercept of the ordinary ACD(1,1). Substituting the $q$ recursion gives the paper's explicit second-order representation, so this component formulation is sufficient to implement the model. Initialization, admissible parameter constraints and optimizer tolerances are not fully specified in the PDF.

The ordinary ACD estimates are $\alpha=0.0631$, $\beta=0.9309$, with robust t-statistics 22 and 296. The reported log likelihood is −71,986. The component estimates in Table I are:

| Parameter | Estimate | Robust standard error |
|---|---:|---:|
| $\omega$ | 1.074 | 0.151 |
| $\rho$ | 0.99915 | 0.00032 |
| $\varphi$ | 0.019 | 0.002 |
| $\alpha$ | 0.052 | 0.003 |
| $\beta$ | 0.911 | 0.005 |

Its reported log likelihood is −71,937.113, about 49 points higher. The slow root implies a half-life $\log(0.5)/\log(0.99915)\approx815$ trades, which the source translates to less than six hours at the average trading rate. It is a transaction-count half-life; clock-time decay changes with trading intensity. Although very persistent, the estimate's conventional confidence interval excludes one.

Engle computes the ACD estimates with GARCH software using $\sqrt{x_i}$ as the dependent variable and no mean intercept. The Gaussian variance objective then has the same optimizer as the exponential duration objective, up to scaling and constants. Reported software likelihoods should therefore be compared using consistent conventions rather than assumed equal to an independently coded normalized density without adjustment.

Standardized-duration Ljung–Box statistics fall to 32.8 for levels and 31.2 for squares, still above the cited fifteen-lag 5% cutoff of 25. The fitted model improves dependence substantially but does not eliminate it. The empirical hazard drops sharply at short standardized durations and then declines more slowly, broadly resembling a Weibull with shape below one. The figure is more sharply curved near zero than the cited Weibull shape 0.8. There is no numerical hazard grid in the PDF from which to reproduce the plot exactly.

## Returns, transaction variance, and time-normalized variance

Let $r_i$ be the return between successive transaction-time midquotes. Conditional on the current duration and past information, define

$$
h_i=\operatorname{Var}(r_i\mid x_i,\mathcal F_{i-1}),
\qquad
\sigma_i^2=\operatorname{Var}(r_i/\sqrt{x_i}\mid x_i,\mathcal F_{i-1}).
$$

Thus $h_i=x_i\sigma_i^2$. This is conditional variance accounting, not a Brownian-time-scaling assumption that makes $\sigma_i^2$ independent of $x_i$. The next transaction's variance forecast before its arrival is $E[x_i\sigma_i^2\mid\mathcal F_{i-1}]$, which generally does not factor into $\psi_iE[\sigma_i^2\mid\mathcal F_{i-1}]$. The mean of the next return also enters the unconditional predictive return variance through the law of total variance.

More explicitly, let $\mu_i(x)=E[r_i\mid x_i=x,\mathcal F_{i-1}]$. For the original, unnormalized return,

$$
\operatorname{Var}(r_i\mid\mathcal F_{i-1})
=E[x_i\sigma_i^2\mid\mathcal F_{i-1}]
+\operatorname{Var}(\mu_i(x_i)\mid\mathcal F_{i-1}).
$$

The second term matters when duration predicts the mean. This identity is a derived clarification of the paper's conditioning, not an additional estimated result. For clock-time portfolio risk, one must also aggregate an uncertain number of future returns and their dependence. Summing a fixed number of conditional trade variances is not generally the same forecast. A practical simulation would produce both the next-trade distribution and the return distribution over a specified number of seconds, with their respective timing assumptions recorded. The source does not report either type of out-of-sample density calibration.

The empirical price is the midpoint of the bid and ask at the transaction time. In the historical sample, quotes lie on an eighth-dollar grid and midquotes on a sixteenth-dollar grid. Midquotes reduce bid–ask bounce but do not eliminate measurement noise or discreteness. The paper motivates an ARMA(1,1) for time-normalized returns by writing observed log price as a latent martingale plus serially dependent rounding error. This is a rough approximation; it is not a fully estimated state-space model of the quote process.

In convenient notation, the fitted mean has the form

$$
y_i=b x_i+\phi y_{i-1}+\vartheta e_{i-1}+e_i,
\qquad
\operatorname{Var}(e_i\mid x_i,\mathcal F_{i-1})=\sigma_i^2,
$$

where $y_i$ denotes the adjusted return-per-square-root-time series. The duration regressor is added to the ARMA mean to test whether a long wait predicts a price decline. There is no displayed fitted mean intercept in Table II.

The source also removes time-of-day variation from returns: regress $|r_i/\sqrt{x_i}|$ on the same intraday spline basis, then divide the normalized return by the fitted absolute-return profile. Keep that seasonal scale separate from the dimensionless duration adjustment. To recover variance in original return units, restore the appropriate squared return-seasonality factor and duration units. The paper does not publish spline coefficients or a complete transformation script, and the transition from raw durations to adjusted-duration notation is abbreviated. A replication must explicitly document which duration scale is used at each step.

Figure 3 shows typical durations near ten seconds at the open and nearly forty seconds near lunch. Figure 4 shows a midday trough in the return-normalization profile. The prose's claim that lunchtime volatility is about 40% of the morning peak is not directly recoverable from the plotted ordinate, which is approximately 0.00010 versus 0.00013. The precise seasonal series is therefore a missing replication input, not something to infer by imposing that verbal ratio.

## UHF-GARCH specifications and fitted results

The simplest variance equation is ordinary GARCH applied to the adjusted innovation:

$$
\sigma_i^2=\omega+\alpha e_{i-1}^2+\beta\sigma_{i-1}^2.
$$

Adding $\gamma_1/x_i$ permits a short duration to raise variance per unit of time without a long duration mechanically driving variance negative. The richer specification is

$$
\sigma_i^2=\omega+\alpha e_{i-1}^2+\beta\sigma_{i-1}^2
+\gamma_1x_i^{-1}
+\gamma_2x_i/\psi_i
+\gamma_3\xi_{i-1}
+\gamma_4\psi_i^{-1},
$$

with the slow volatility proxy

$$
\xi_i=0.005(r_{i-1}^2/x_{i-1})+0.995\xi_{i-1}.
$$

The smoothing constant is imposed, not optimized; its half-life is about 138 trades. The displayed $\xi_{i-1}$ in the variance recursion and the indexing in its update should be implemented literally or changed only with an explicit stated convention. It is not a long-run variance estimate inferred from a separately fitted stochastic process.

Table II reports the following variance coefficients. Blank entries mean that the regressor is absent:

| Regressor | Rich equation (40) | Reciprocal-duration equation (39) | Basic equation (38) | Final augmented column |
|---|---:|---:|---:|---:|
| Constant | −0.224 | 0.272 | 0.988 | −0.111 |
| Lagged squared innovation | 0.314 | 0.304 | 0.245 | 0.250 |
| Lagged variance | 0.147 | 0.230 | 0.622 | 0.158 |
| $1/x_i$ | 0.579 | 0.632 |  | 0.587 |
| $x_i/\psi_i$ | −0.055 |  |  | −0.040 |
| Lagged long-volatility proxy | 0.086 |  |  | 0.096 |
| $1/\psi_i$ | 0.484 |  |  |  |
| Lagged spread indicator |  |  |  | 0.736 |
| Size above 10,000 shares |  |  |  | 0.193 |

The corresponding reported log likelihoods are −107,688.9, −108,202.0, −112,246.3, and −107,406.4. They measure in-sample fit; the paper reports no held-out loss comparison. The final table column is labeled equation (42), although the displayed equation (42) in the text is a conditional-expectation calculation, not the spread/size regression. The table itself indicates that the final model omits $1/\psi_i$ while adding the two indicators. The note preserves that displayed specification rather than silently treating every richer column as nested.

The spread indicator uses the previous spread exceeding 0.003; the accompanying paragraph does not fully define its normalization. The size threshold is 10,000 shares. Their robust z-statistics are 11.29 and 1.624 respectively, so the size effect is marginal, not conventional two-sided 5% evidence. In the rich equation, reciprocal duration, duration surprise, slow volatility, and inverse expected duration have z-statistics 19.69, −5.807, 6.235 and 5.554.

The rich model's duration coefficient in the conditional mean is −0.004, with z-statistic −1.892; the final augmented version gives −0.007 with z-statistic −4.027. Thus evidence that a long wait precedes a lower return depends on specification. The AR and MA coefficients are strongly significant. Negative MA coefficients also underline why midpoint sampling alone does not remove short-horizon price-measurement effects.

A negative variance intercept in the rich models is an important implementation constraint. Nonnegative individual GARCH coefficients no longer guarantee that the complete expression stays positive because the duration-surprise coefficient is negative too. The fitted path must remain positive for likelihood evaluation, and out-of-sample simulation needs an admissible parameter/state region or an explicitly changed positive-link model. The PDF does not provide a global positivity theorem or describe any clipping rule. Adding an arbitrary floor would change the specification.

## Forecast interpretation and limits

Because $E[x_i/\psi_i\mid\mathcal F_{i-1}]=1$, the duration-surprise coefficient contributes a constant to the one-step expected variance rate:

$$
E[\sigma_i^2\mid\mathcal F_{i-1}]
=\omega+\alpha e_{i-1}^2+\beta\sigma_{i-1}^2
+\gamma_1E[x_i^{-1}\mid\mathcal F_{i-1}]
+\gamma_2+\gamma_3\xi_{i-1}+\gamma_4\psi_i^{-1}.
$$

In contrast, the reciprocal-duration and expected-intensity terms inherit persistent duration dynamics. Engle explicitly observes that $E[1/x_i\mid\mathcal F_{i-1}]\ne1/\psi_i$. Jensen's inequality gives $E[1/x_i\mid\mathcal F_{i-1}]\ge1/\psi_i$ when the expectation is finite. An untruncated exponential duration has infinite reciprocal expectation; the source's lower timestamp resolution avoids that problem for its retained empirical durations. A forecast simulator that uses a continuous fitted hazard down to zero would need to confront this issue again.

The conventional GARCH persistence sum is 0.867 in the basic model, 0.534 in the reciprocal-duration model, 0.461 in the richer model, and 0.408 in the final column. The source's description of all richer sums as just below one-half is approximate: the reciprocal-duration column is above one-half. More substantively, a low $\alpha+\beta$ is not evidence of low total persistence when persistent duration and long-volatility variables enter the equation.

The economic interpretation compares three mechanisms. “No trade means bad news” predicts lower returns after long waits. “No trade means no news” predicts lower variance when trading is slow. Liquidity-trader bunching can instead associate slow trading with a more informed residual trader population and greater volatility. The fitted negative duration-mean effects and positive reciprocal-duration variance effects favor the first two channels in this sample. They do not identify informed-trader types, establish causation, or rule out mixtures of the mechanisms.

All fitted return models retain significant serial-correlation diagnostics. For the rich model, the fifteen-lag Ljung–Box statistics are 67.156 for standardized residuals and 157.0 for their squares. The final augmented model gives 40.810 and 169.12. The basic model's squared-residual statistic is smaller, 30.422 with reported p-value 0.004, despite its worse likelihood. Better in-sample density fit and cleaner residual dependence are different criteria.

A reproducible study therefore needs the original TORQ records, quote-merging and simultaneous-trade rules, seasonal spline coefficients, exact return and spread scaling, initial conditions, parameter constraints, optimizer tolerances, and the hazard tie/boundary convention. The paper mentions EViews 3.1 and an original program location but supplies neither code nor those data in the PDF. No modern-market validation, transaction-cost analysis, or live trading result is provided. The durable method is the explicit joint treatment of event timing and returns, with forecast conditioning and units kept consistent.
