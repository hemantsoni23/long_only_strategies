# The hidden dangers of historical simulation

**Matthew Pritsker (2006).** *Journal of Banking & Finance* 30, 561–582; available online June 14, 2005. DOI: 10.1016/j.jbankfin.2005.04.013. Source: [VaRFailures_Pritzker_2006.pdf](../../Finance/VaRFailures_Pritzker_2006.pdf). The source filename misspells the author's surname; the bibliographic name is Pritsker. This note covers the journal article, including Appendix A, rather than its earlier 2001 working-paper version.

## Why this matters

Historical simulation appears to avoid distributional assumptions by replaying actual past returns. It nevertheless assumes that a weighted mixture of past shocks adequately describes today's conditional risk. Pritsker shows that ordinary and exponentially weighted historical quantiles can respond very slowly to volatility changes, with a built-in asymmetry: a large gain provides little immediate warning of future loss risk even when its magnitude signals rising volatility.

The paper combines a general quantile-update result, GARCH calculations, and simulations in which true conditional risk is known. That design allows measurement of forecast errors hidden from ordinary real-data backtests. A second contribution examines filtered historical simulation: modeling volatility helps, but empirical innovation resampling trades tail-sampling uncertainty against the implausibility of treating dependence as constant over a long history.

These results concern particular estimators and specified data-generating processes. They are not a theorem that every historical-data risk model fails, or that a chosen parametric volatility model is the true model of financial markets.

## What is estimated

The paper uses $c=0.01$ to mean a 1% **loss-tail probability**, conventionally a 99% VaR confidence level. To avoid the article's occasionally confusing “confidence” terminology, let $v_{t,c}$ be a positive loss threshold and $q_{t,c}$ the corresponding lower return quantile, so $v_{t,c}=-q_{t,c}$ for a unit linear position.

Historical simulation revalues today's portfolio under each of the last $N$ observed risk-factor moves. For the simple single-asset positions studied here, this is a history of returns $r_{t-1},\ldots,r_{t-N}$. Equal weights produce the ordinary empirical CDF. The Boudoukh–Richardson–Whitelaw (BRW) version puts geometrically declining weights on older observations:

$$
w_i=\frac{(1-\lambda)\lambda^{i-1}}{1-\lambda^N},\qquad i=1,\ldots,N,
\qquad G_t(x)=\sum_{i=1}^{N}w_i\mathbf1\{r_{t-i}\leq x\}.
$$

For $\lambda\to1$, weights tend to $1/N$. The experiments use $\lambda=0.97$ and 0.99. This changes observation probabilities, not the magnitudes of past returns; old returns are not rescaled to today's volatility.

Because $G_t$ is discrete, the paper defines two bracketing return-quantile estimators and studies the one it calls $BRW^u$, the negative of the first observed return at which cumulative weight reaches $c$. BRW's original implementation interpolates smoothly between brackets; the article says numerical results are similar, but its formal propositions and reported analysis use the simpler bracket estimator. Interpolation conventions must therefore be retained in replication.

In the initial illustration, $N=250$. At the 1% tail, equal-weighted VaR corresponds to the third-lowest observation under the stated convention. Inserting an unprecedented large negative return generally promotes the old second-lowest return into that position, rather than making the new crash itself the quantile. If the second and third observations are close, the risk estimate barely changes.

## October 1987: responsiveness and sign asymmetry

Figures 1–3 compare historical simulation and both BRW decays around October 19, 1987 for long and short S&P 500 positions. VaR is plotted as a negative return in these figures, whereas this note generally uses positive loss magnitudes.

For the long position, historical VaR barely reacts to the crash. BRW reacts sharply because the newest observation's normalized weight exceeds 1% for both reported decay settings with $N=250$: the crash can become the estimated 1% quantile itself. For the short position, the crash is a large gain. Its magnitude does not enter the lower P&L tail, and the corresponding risk estimates do not rise until later adverse short-position returns during the market recovery.

The point is not that a gain is itself a loss. In a volatility model, a large move of either sign can signal a larger future scale. A tail-only empirical update can miss the positive-P&L signal. In the 5% VaR illustration, losses on the long position exceed the nominal threshold on 25% of October trading days. This is a short historical episode, not an independently designed statistical test of all future periods.

## Quantile-update theorem and its scope

Proposition 1 states that, for the studied bracket estimator, if today's loss does not exceed today's forecast,

$$
-r_t<v_{t,c}^{BRW},
$$

then the next estimate cannot increase:

$$
v_{t+1,c}^{BRW}\leq v_{t,c}^{BRW}.
$$

The proof tracks empirical probability weight below the old return quantile. The new non-tail observation adds no mass there, existing retained observations receive lower weights, and dropping the oldest observation cannot restore the missing lower-tail weight. Consequently the new lower return quantile cannot move in the direction that would increase the positive VaR magnitude. The argument examines separately whether the dropped observation was in the old tail.

This result does not require a GARCH data-generating process. It is a property of the rolling empirical quantile update. It concerns the fixed return/P&L representation under that update; it should not be automatically extended to arbitrary changing portfolios or a nonlinear revaluation whose entire historical P&L vector changes with current market levels.

If the current forecast is conditionally correct for a continuous distribution, the estimate can rise only on an event with probability at most $c$. A non-exceedance prevents an increase; an exceedance is a **necessary**, not generally sufficient, condition for an increase. That logical distinction is important for interpreting the later probability formulas.

Appendix A.1 prints a new-observation weight with numerator and denominator reversed. The normalized weight is the $w_1=(1-\lambda)/(1-\lambda^N)$ expression above, which sums correctly with the retained observations; the reciprocal cannot be a probability weight for the stated parameters.

## Conditional risk under GARCH

For the theoretical comparison, returns satisfy

$$
r_t=\sqrt{h_t}u_t,\qquad
h_{t+1}=a_0+a_1r_t^2+b_1h_t.
$$

The assumptions are $a_0,a_1,b_1>0$, $a_1+b_1<1$, and iid, continuous, symmetric innovations with mean zero and unit variance. The innovation CDF is $F$. Long-run variance is $\bar h=a_0/(1-a_1-b_1)$. For a unit long position,

$$
v_{t,c}=-F^{-1}(c)\sqrt{h_t}.
$$

At $h_t=\bar h$, substituting the variance recursion gives

$$
\frac{v_{t+1,c}}{v_{t,c}}=\sqrt{1+a_1(u_t^2-1)}.
$$

True conditional VaR increases exactly when $|u_t|>1$. Its probability is $2F(-1)$, or approximately **31.73%** for Gaussian innovations. This is much larger than the at-most-1% increase frequency allowed by a correct current 1% historical quantile's non-exceedance restriction.

Combining the variance increase with the region where the empirical update cannot increase gives probability $2F(-1)-c$, approximately **30.73%** at $c=0.01$ under Gaussian innovations. This is the event that true risk rises while the current shock lies outside the loss-exceedance region. Because Proposition 1 supplies a necessary condition only, the formula is most safely interpreted as the guaranteed blind-region probability, or a lower bound on total nondetection without additional assumptions about what the estimator does after an exceedance. The source labels it an exact nondetection probability; its simulations allow additional misses.

For a fractional true-VaR increase greater than $x>0$, define

$$
a(x)=\sqrt{1+\frac{x^2+2x}{a_1}},\qquad
k=-1+\sqrt{1-a_1+a_1\{F^{-1}(c)\}^2}.
$$

The probability in that blind region is

$$
P\{\Delta v/v>x,\ \text{no required upward update}\}=\begin{cases}2F(-a(x))-c,&0<x<k,\\F(-a(x)),&x\geq k.\end{cases}
$$

Here $x=0.25$ means a 25% increase, not a 0.25% increase. Below the boundary, both moderate adverse and favorable shocks contribute; above it, the very large favorable shocks alone still force no upward empirical update. The branches agree at $a(x)=-F^{-1}(c)$. The assumptions of an initially correct quantile and variance at its long-run level are essential. The result is not an unconditional formula for accumulated multi-day forecast error.

## Calibration and simulation design

Gaussian GARCH models are fitted to daily log USD exchange-rate returns for the British pound, Belgian franc, Canadian dollar, French franc, Deutsche mark, Japanese yen, Dutch guilder, Swedish kronor, Swiss franc, and Italian lira. The calibration period is January 2, 1973–November 6, 1997. Table 1A parameters are:

| Currency | $a_0$ | $a_1$ | $b_1$ |
|---|---:|---:|---:|
| British pound | $7.059\times10^{-7}$ | 0.08428 | 0.9010 |
| Belgian franc | $1.177\times10^{-6}$ | 0.1141 | 0.8690 |
| Canadian dollar | $1.088\times10^{-7}$ | 0.1232 | 0.8697 |
| French franc | $6.746\times10^{-7}$ | 0.1446 | 0.8586 |
| Deutsche mark | $1.115\times10^{-6}$ | 0.09343 | 0.8856 |
| Japanese yen | $2.147\times10^{-6}$ | 0.05810 | 0.9165 |
| Dutch guilder | $6.888\times10^{-7}$ | 0.1043 | 0.8865 |
| Swedish kronor | $2.470\times10^{-6}$ | 0.1588 | 0.8031 |
| Swiss franc | $1.261\times10^{-6}$ | 0.09751 | 0.8857 |
| Italian lira | $2.618\times10^{-8}$ | 0.2057 | 0.8428 |

The French-franc and Italian-lira estimates violate $a_1+b_1<1$. The author acknowledges that the stationary theoretical results do not strictly apply to those estimates. Italian-lira simulations are omitted because volatility is explosive; French-franc results are still shown. Do not initialize these two using a positive stationary long-run variance that their fitted parameters do not possess.

Theory curves use low, mean, and high fitted shock sensitivities near 0.05810, 0.1184, and 0.2057, for Gaussian and standardized Student-$t_{10}$ innovations. Standardizing a Student variable requires multiplication by $\sqrt{(\nu-2)/\nu}$ for $\nu>2$; otherwise the stated unit-variance assumption is violated. Large $a_1$ makes the magnitude of missed updates more important. The paper reports roughly a 4% blind-region probability for a greater-than-25% VaR rise at the high shock sensitivity, versus about a 7% rise at low sensitivity.

Section 3.2 generates 200 years of daily data from each included calibrated process and applies the historical and BRW estimators while comparing them with the known conditional VaR. Table 3 uses Gaussian simulation results; Figure 5 also illustrates Student-$t_{10}$ innovations for sterling. The paper's initial estimator illustration explicitly uses a 250-day history; the later simulation description does not separately restate every window and initialization convention. Burn-in, random seeds, trading-days-per-year convention, and exact quantile implementation beyond the defined bracket remain necessary replication choices.

The design deliberately uses simple spot positions to exclude valuation approximation, derivative Greeks, changing portfolio composition, and risk-factor mapping errors. Its observed errors therefore isolate the distributional shortcut within the stipulated model. They do not measure all errors a real institution faces.

## Results: slow updates and persistent error

Table 3 reports that about 94%–96% of true one-day VaR increases are not accompanied by an increase in the estimator. For sterling, the conditional nondetection fractions are 94.28% for BRW 0.97, 95.91% for BRW 0.99, and 95.54% for ordinary historical simulation. The unconditional probabilities of a rise and a miss are 0.3180, 0.3235, and 0.3222. These are different denominators from the 31.73% theoretical probability of any true rise at $h_t=\bar h$.

The theoretical mean missed increase for sterling is 5.49% under Gaussian innovations and 6.04% under standardized $t_{10}$; corresponding standard deviations are 5.34% and 6.86% (Table 2). Heavier tails slightly reduce the incidence of the blind region but increase the typical size of a missed rise.

Selected sterling results from Table 4 are:

| Method | Exceedance frequency | Reported percentage RMSE | Correlation with true VaR level | Correlation with true VaR change |
|---|---:|---:|---:|---:|
| BRW 0.97 | 1.93% | 23.98% | 0.81 | 0.33 |
| BRW 0.99 | 1.38% | 23.90% | 0.70 | 0.31 |
| Historical simulation | 1.52% | 28.65% | 0.50 | 0.23 |

A reasonable-looking level correlation can coexist with poor tracking of changes. Across currencies, ordinary historical simulation's reported percentage RMSE ranges from 20.23% to 47.11%, averaging about 32.69% over the nine displayed currencies. The prose's broad “approximately 25%” error description should not replace the method-specific table. Its percentage-RMSE normalization is not fully formalized beyond comparison with true VaR, so an exact implementation should disclose whether normalization occurs before or after averaging squared errors.

Figure 5 shows extended underestimation episodes for simulated sterling, some longer than 0.1 year, with errors reaching roughly 60% in the author's description. The graph is one selected two-year path, not an estimated frequency distribution of worst errors. The study also reports similar historical-simulation problems for expected shortfall, estimated from the three worst observations in a 300-day history, but does not display those extra results.

## Why standard backtests can miss the problem

An exceedance indicator records whether a loss crosses a forecast, discarding how far the forecast lies from the true quantile on most dates. A 1% model produces only about 2.5 expected exceedances in 250 days; even a materially wrong rate can be hard to distinguish with that sample. The paper illustrates low power for an actual 1.5% rate against a 1% null and notes that a one-sided normal approximation needs more than 2.5 years to reject at 95% significance. This is an approximation for a specified comparison, not a universal sample-size guarantee or a full power curve.

For simulated sterling, early exceedance autocorrelations are no larger than about 0.05 and fade quickly. Meanwhile forecast errors measured against the known true VaR persist: historical simulation's lag-50 error autocorrelation is approximately 0.5, versus approximately 0.1 for BRW 0.97. Figure 6 juxtaposes the slowly decaying error dependence with weak dependence in the binary hits. Conditional correctness implies more than a satisfactory unconditional hit rate; failure to reject a limited hit test does not establish it.

The proposed diagnostic is a parametric bootstrap: fit a plausible dynamic model that does not impose the shortcut being evaluated; simulate data from it; compute the true conditional risk under that model; apply the shortcut; and compare risk estimates directly, including persistence and size of errors. This exposes the consequences of a known shortcut. Its external validity remains conditional on the plausibility of the generating model. Good results under one Gaussian GARCH model would not prove adequacy for jumps, asymmetric dynamics, or structural changes.

## Filtered historical simulation: procedure

FHS estimates a volatility model before resampling innovations. Fit GARCH by Gaussian quasi-maximum likelihood, obtain $\widehat h_t$, and form standardized residuals $\widehat u_t=r_t/\sqrt{\widehat h_t}$. Under suitable regularity conditions, Gaussian QMLE can estimate the conditional-variance parameters even if innovations are non-Gaussian; this is not a claim of robustness to a misspecified variance recursion.

Starting from today's conditional variance, generate each ten-day path by drawing an empirical residual, forming $r_{t+1}=\sqrt{h_{t+1}}u_{t+1}$, updating variance through the GARCH recursion, and repeating through day ten. Revalue or aggregate the resulting path for the position, then estimate its 1% quantile and expected shortfall across simulations. For log exchange-rate returns, the position-value mapping and exponentiation convention must be stated; the article does not give a full code-level mapping.

With multiple risk factors, fit marginal volatility models separately but draw a **common historical date's entire residual vector** at each simulated step. This preserves empirical contemporaneous dependence. Drawing each residual coordinate independently would destroy it. Drawing dates independently over time assumes the vector innovations are iid, including a stable dependence structure. No explicit correlation matrix is needed for resampling, but a constant residual dependence assumption remains.

## Dependence instability versus tail-sampling uncertainty

For the correlation check, marginal GARCH models are fitted over January 1973–June 1986, and the standardized residual history is split into halves. Fisher's transform $z(r)=\tfrac12\log[(1+r)/(1-r)]$ is used to compare correlations. With equal independent subsample lengths $n$, the approximate statistic is $\tfrac12(n-3)(z_1-z_2)^2$, compared with a one-degree-of-freedom chi-square law.

The paper reports rejection for 86 of 90 correlation coefficients and acknowledges dependence among tests. Ten currencies have only 45 distinct unordered pairs, so the figure must not be interpreted as 86 independent pairwise discoveries. The full coefficient list and detailed results for adjacent one-year comparisons are not displayed. The latter comparisons still find instability, although with fewer rejections.

A shorter residual window may reduce dependence drift but gives fewer tail draws. Section 4.1 isolates that trade-off's sampling side with a **single sterling position**, treating its parameters, present variance, and residual history as known. It uses unit-variance Student innovations with degrees of freedom 3, 5, 7, 10, 20, and the Gaussian limit $\nu=\infty$. The last case is infinity, not a Cauchy distribution with one degree of freedom, despite poor text extraction of the symbol.

Residual-history lengths are $N=500,1250,1875,2500$. For every distribution/window specification, 1,000 FHS estimates are calculated, each from 10,000 ten-day paths. The “true” benchmark uses one million paths drawn from the actual innovation distribution. Thus the benchmark is itself a high-precision Monte Carlo estimate, not an analytically exact ten-day risk. These experiments omit parameter-estimation uncertainty and multivariate dependence changes to isolate empirical-residual sampling.

| Innovation law and history | VaR mean / median error | VaR 2.5% / 97.5% error percentiles | ES mean / median error | ES 2.5% / 97.5% error percentiles |
|---|---|---|---|---|
| $t_3$, 500 days | +3.87% / −5.15% | −32.14% / +95.11% | −8.33% / −17.11% | −44.24% / +83.01% |
| Gaussian, 500 days | −0.01% / −0.22% | −16.57% / +18.52% | −0.28% / −0.79% | −15.93% / +18.02% |
| $t_3$, 2500 days | +1.22% / +0.20% | −17.40% / +27.64% | +0.14% / −5.17% | −28.75% / +67.57% |
| Gaussian, 2500 days | −0.18% / −0.24% | −7.90% / +7.92% | +0.14% / −0.09% | −7.99% / +9.12% |

Errors are percentages of the corresponding true risk measure, not percentage points of portfolio returns. The percentile ranges describe repeated-estimator uncertainty under the experiment, rather than confidence intervals on a single observed portfolio loss. The last Table 6 heading prints “7.5%”; the text and ordering indicate the intended upper endpoint is 97.5%.

For $t_3$ and 500 observations, standard deviations of VaR and ES errors are about 37.8%. A mean near zero can hide a skewed distribution and a negative median. With 2500 observations, $t_3$ ES error still has a 23.82% standard deviation and a long upper tail. The author ultimately emphasizes variability and dependence instability over the earlier working paper's focus on median downward bias.

The tail-count arithmetic explains the problem. The chance that 500 iid residuals contain no draw from either 0.2% tail is $0.996^{500}\approx13\%$, while a ten-day path has probability $1-0.996^{10}\approx4\%$ of at least one such draw. Omitting these events can distort a 1% multi-day loss tail. Conversely, a single very extreme observation can receive empirical probability 1/500 = 0.2%, exceeding its true tail probability and producing overestimation. More simulation paths reduce resampling noise conditional on the history but cannot create tail information absent from that history.

## Reproduction limits and implications

The paper provides the main recursions, theorem assumptions, calibration dates, many fitted parameters, and simulation counts. Exact table replication additionally requires raw exchange-rate and S&P series conventions, initial variance and burn-in, random seeds, precise historical windows in each experiment, quantile/tail-mean conventions, and the current variance used for the FHS exercise. Table 1B intercepts use a visibly different numerical scale from Table 1A without an explicit scale reconciliation; they should not be combined in code under an assumed common return unit. Some robustness and correlation tests are available only in the cited working paper or on request.

The practical lesson is to evaluate conditional responsiveness, not just average exception frequency. Ordinary historical resampling and geometric weighting do not automatically absorb the information in large favorable moves. Volatility filtering directly addresses that defect, but introduces model dependence and leaves tail and cross-sectional sampling problems. A credible validation therefore distinguishes the distributional shortcut, the volatility model, the residual-history choice, and the diagnostic's statistical power. No single passing short backtest establishes that all four are adequate.
