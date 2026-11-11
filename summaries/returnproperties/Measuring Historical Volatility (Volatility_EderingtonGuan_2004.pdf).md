# Measuring Historical Volatility

**Louis H. Ederington and Wei Guan, August 2004 working paper.** Source: [original PDF](../../Finance/Volatility_EderingtonGuan_2004.pdf), 23 PDF pages, including five tables and endnotes. This note describes this dated manuscript rather than importing results from the authors' distinct paper *Forecasting Volatility*. Printed text pages 6–12 contain the methods and results; PDF pages 18–22 contain the numerical tables. Several blanket claims in the narrative disagree with individual table cells, so the comparisons below follow the actual numbers.

## Why this matters

Historical standard deviation is a convenient volatility forecast, but squaring returns makes a short estimation window sensitive to isolated large observations. Lengthening the window reduces that sensitivity while also discarding useful information about recent changes in volatility. The paper proposes an equally simple alternative: average absolute return deviations and multiply by the Gaussian conversion factor $\sqrt{\pi/2}$. This adjusted mean absolute deviation, or AMAD, downweights large observations relative to the root mean square without requiring a longer lookback.

The contribution is a systematic forecast comparison of this elementary estimator with rolling historical standard deviations and GARCH(1,1), across nine series, four lookbacks, and four forecast horizons. It is not a claim that absolute deviations estimate the population standard deviation more efficiently under iid normal sampling. The paper explicitly acknowledges the opposite classical efficiency result. The empirical question is whether a less outlier-sensitive input better predicts a noisy future volatility measure in financial time series.

This distinction matters when choosing a risk estimator. An estimator can be biased for a static population standard deviation yet forecast a changing, finite-horizon realized target well. Conversely, success under mean absolute forecast error does not establish that the estimator gives the best variance forecast, option price, or tail-risk forecast. The manuscript studies forecast errors in annualized standard-deviation units; it does not value options using the competing inputs, report hedging performance, or test a trading rule.

The motivating example uses S&P 500 returns over July 5, 1967–July 11, 2002. The largest 1% of absolute deviations contribute 24.5% of total squared deviations. Under a simple independent-occurrence calculation, a 20-day window contains no such observation with probability $0.99^{20}\approx81.8\%$ and at least one with probability approximately 18.2%. The authors use this to illustrate unstable short-window estimates. The occurrence calculation is illustrative, not an estimated iid model of extremes: clustered financial shocks need not arrive independently.

## Exact estimators and units

Let $R_t=\log(P_t/P_{t-1})$. For a dividend-paying stock, endnote 4 replaces the numerator with $P_t+D_t$. Define the centered return $r_t=R_t-\mu$. The paper uses the average daily return over the entire data period as $\mu$, not the rolling-window sample mean and not zero. Its historical standard-deviation estimator, equation (1), is

$$
STD_t(n)=\sqrt{\frac{252}{n}\sum_{j=0}^{n-1}r_{t-j}^2}.
$$

The denominator is $n$, because the formula treats the centering mean as fixed. Replacing it with a sample standard deviation using a local mean and denominator $n-1$ changes the experiment. A library routine whose defaults subtract a rolling mean will not reproduce the paper without explicit adjustment.

The unannualized mean absolute deviation and annualized adjusted measure, equations (2)–(3), are

$$
MAD_t(n)=\frac1n\sum_{j=0}^{n-1}|r_{t-j}|,
\qquad
AMAD_t(n)=\sqrt{\frac{252\pi}{2}}\,MAD_t(n).
$$

This is **mean** absolute deviation around the specified mean. It is neither median absolute deviation nor average deviation around a fitted median. No robust median-based scale constant, such as the one commonly applied to median absolute deviations, belongs in this calculation. Nor should the absolute observations be squared before averaging: that would return to the estimator being compared.

The factor 252 annualizes daily variance, and its square root annualizes standard deviation. The annualization convention is shared by both forecasts and their target. Values in the tables are decimals of annualized volatility: an error of 0.03679 is 3.679 annualized volatility percentage points. It is not a 3.679% relative error, a variance error, or an annual investment return. The same convention is used for the interest-rate and exchange-rate transformations, whose underlying economic interpretations differ from stock total returns.

With a known population mean and $r\sim N(0,\sigma^2)$, $E|r|=\sigma\sqrt{2/\pi}$, so the unannualized adjusted mean absolute deviation is unbiased for $\sigma$. The normal integral is straightforward: symmetry doubles the integral of $r$ times the Gaussian density over the positive half-line, yielding $\sigma\sqrt{2/\pi}$. This establishes the correction constant and its distribution dependence. Normality here refers to log returns; saying that log returns themselves are lognormal would be incorrect.

If the mean is estimated from the same finite sample, the exact unbiasedness statement requires modification. The manuscript's full-period estimated mean is close to a fixed centering convention for short windows, but it is not literally the known population mean. Moreover, it uses future data relative to most forecast origins. That is a small-looking but genuine departure from a strictly real-time experiment. A faithful replication should preserve it first; an implementable extension should use zero or a recursively estimated mean and report the resulting change separately.

## Robustness is not distribution-free consistency

For a general centered distribution with finite variance, AMAD converges to $\sqrt{\pi/2}E|r|$, whereas standard deviation converges to $\sqrt{E[r^2]}$. These need not be equal. The Gaussian correction is therefore a maintained calibration, not a universal conversion. Even a symmetric distribution can have a different ratio of first absolute moment to standard deviation. Skewness and kurtosis alone do not fully describe the discrepancy.

A useful algebraic interpretation, not a separate empirical result of the manuscript, comes from a conditionally Gaussian scale mixture: $r=\sigma_tZ$, with $Z$ standard normal and independent of the scale. Averaging absolute returns targets $E[\sigma_t]$ after the Gaussian correction, while averaging squared returns and taking a square root targets $\sqrt{E[\sigma_t^2]}$. Jensen's inequality makes the first no larger than the second. Thus conditional Gaussianity does not make a pooled-window AMAD automatically unbiased for the square root of average variance when volatility changes inside the window.

The outlier argument should also be kept precise. Absolute deviations grow linearly with a return, whereas squared deviations grow quadratically; AMAD is consequently less sensitive to extreme observations than variance-based scale. Its influence is still unbounded. It does not completely reject contaminated observations, protect against arbitrary data errors, or guarantee correct risk estimates during a genuine regime change. A crash can be noise about future routine volatility or evidence that future risk has increased; the forecast evaluation determines which treatment worked in these historical samples.

Under iid normal returns and a known mean, the variance of the unannualized AMAD is $(\pi/2-1)\sigma^2/n$. By the delta method, the root-mean-square estimator has leading variance $\sigma^2/(2n)$. The latter is smaller. This derived comparison explains why the paper's finding cannot be justified by claiming superior Gaussian sampling efficiency. Its gains concern empirical forecasting with persistence, tails, finite windows, and a future target, rather than estimating a single fixed normal scale from iid observations.

## Forecast target and competing GARCH model

At the end of day $t$, predict the annualized realized standard deviation of the next $s$ daily centered returns:

$$
RLZ_t(s)=\sqrt{\frac{252}{s}\sum_{j=1}^{s}r_{t+j}^2}.
$$

Both STD and AMAD are judged against this same root-mean-square target. The authors do not substitute future AMAD as the target for their favored estimator. For the historical estimators, the forecast is simply today's $STD_t(n)$ or $AMAD_t(n)$, used unchanged for a given horizon. Lookback $n$ and forecast horizon $s$ are independent design dimensions; matching them is not an assumed optimality condition.

The GARCH competitor, equation (7), is

$$
v_{t+1}=\alpha_0+\alpha_1r_t^2+\beta v_t.
$$

Parameters are estimated using 1,260 daily observations, approximately five years, with re-estimation every 40 trading days. Between re-estimation dates the conditional-variance recursion can still be updated with new daily returns; holding parameters fixed is different from holding the state fixed. The paper cites successive forward substitution for multiday variance forecasts and references Ederington and Guan's separate forecasting paper for the procedure.

A reconstruction consistent with this recursion forecasts $v_{t+1|t}$ directly and then applies $v_{t+j|t}=\alpha_0+(\alpha_1+\beta)v_{t+j-1|t}$ for $j\ge2$. To compare with $RLZ_t(s)$, form $\sqrt{252s^{-1}\sum_{j=1}^s v_{t+j|t}}$. This formula is the natural variance-aggregation implementation of the stated procedure. It is not exactly $E_t[RLZ_t(s)]$, because expectation and square root do not commute. The distinction can matter under loss measured on standard deviations.

The manuscript does not state the full GARCH likelihood specification, optimization algorithm, parameter bounds, convergence handling, starting variance, or whether a fixed-length versus expanding estimation sample was used beyond its description of 1,260 observations. A rolling five-year interpretation is natural but should be verified against original code. It also does not print fitted GARCH parameter series. These omissions prevent exact numerical reproduction solely from the PDF, although the basic forecast comparison is readily reconstructible.

## Data, samples, and timing

The nine series comprise the S&P 500 index, the ten-year Treasury rate, the three-month Eurodollar rate, the yen/dollar exchange rate, and five Dow-associated stocks: Boeing, General Motors, International Paper, McDonald's, and Merck. Stocks and the S&P series come from CRSP; the rate and exchange-rate series come from Federal Reserve files. The stocks are a selected set, not a broad cross-section chosen under a documented random-sampling scheme.

The text reports raw equity data from July 2, 1962 through December 31, 2002; ten-year Treasury-rate data from January 2, 1962 through December 31, 2003; and Eurodollar and yen/dollar data from January 1, 1971 through December 31, 2003. Five years are initially used for GARCH estimation. Forecast evaluation ends 120 trading days before the dataset endpoint, leaving more room than the longest 80-day forecast horizon. The rationale for the extra 40-day margin is not fully explained.

Table 1 identifies evaluation periods more precisely: July 5, 1967–July 11, 2002 for equities and the index; November 2, 1966–July 16, 2003 for the Treasury rate; and November 4, 1975–July 16, 2003 for Eurodollars and yen/dollar. These table dates should be checked directly against the reconstructed calendar. They are not perfectly transparent consequences of the rounded “approximately five years” description. Exact per-series forecast counts and a holiday/missing-data ledger are not supplied.

The interest-rate inputs are explicitly rates, not Treasury-bond total-return prices or Eurodollar-futures returns. Applying the generic log-ratio transform to these positive rates measures proportional rate changes. It does not produce a bond holding-period return. A practitioner cannot transfer the reported Treasury result directly to bond price volatility without a duration/convexity mapping. The paper's “T-Bond” table label makes this distinction especially easy to overlook.

Table 1 reports annualized standard deviations of 0.1537 for the S&P, 0.1392 for the Treasury-rate transform, 0.2430 for Eurodollars, and 0.1043 for yen/dollar. The five stock standard deviations range from 0.2482 for Merck to 0.3369 for Boeing. The S&P's skewness is −1.6081 and kurtosis 39.893; Eurodollar skewness is −0.3859 and kurtosis 8.311. Nevertheless, the Kolmogorov–Smirnov distance is 0.2395 for Eurodollars, far larger than 0.0583 for the S&P. Normality is rejected at 1% for all nine series. “Approximately normal” in the conclusion is thus comparative, not a passed formal normality test.

## Evaluation design and statistical claims

The experiment crosses $n\in\{10,20,40,80\}$ with $s\in\{10,20,40,80\}$ trading days. For each series and horizon, compute forecasts and future targets over common origins. With errors $e_t=RLZ_t(s)-F_t(n)$, the reported losses are

$$
RMSFE=\sqrt{T^{-1}\sum_t e_t^2},
\qquad MAFE=T^{-1}\sum_t|e_t|.
$$

Squared loss emphasizes occasional large misses; absolute loss emphasizes typical absolute deviation. Because the conditional mean and median of a skewed target need not coincide, the two criteria can reasonably favor different forecasting rules. This is particularly relevant when GARCH forecasts average variance but AMAD tends to produce a lower, less extreme scale estimate.

The manuscript invokes Diebold–Mariano's $S_1$ statistic for paired predictive-accuracy comparisons. Reimplement it using the time series of loss differentials and an appropriate long-run variance estimate. Successive realized targets overlap for $s>1$, so independent-observation standard errors would be wrong. The supplied text does not state the bandwidth, kernel, finite-sample correction, or cell-level test statistics and $p$ values. It gives only aggregate counts of significant comparisons; those counts should not be converted into precise unreported confidence intervals.

Choosing the best $n$ after seeing the full evaluation period creates another distinction. The table minima establish which lookbacks performed best in that sample; they are not a demonstration of a real-time procedure that selected its lookback without using future losses. An extension should reserve a training period or adopt a nested selection rule before claiming that the best-of-four AMAD is directly tradable. The same issue affects sweeping comparisons between “the AMAD model” and a single fitted GARCH specification.

## Ten- and twenty-day results

At the ten-day horizon, AMAD has lower RMSFE than STD in all 36 same-lookback comparisons. The manuscript says the same is true for MAFE, but Table 2 contradicts that statement in two cells: GM at $n=10$ has 0.07905 for AMAD versus 0.07839 for STD; McDonald's at $n=10$ has 0.08463 versus 0.08448. Both exceptions use the short lookback that otherwise performs poorly. They do not reverse the broad result, but “all 36 under both losses” is inaccurate.

The following Table 2 entries preserve identical lookbacks within each comparison. All errors are annualized volatility decimals.

| Series, lookback | STD RMSFE | AMAD RMSFE | STD MAFE | AMAD MAFE |
|---|---:|---:|---:|---:|
| S&P 500, 40 days | .06964 | .06477 | .03882 | .03679 |
| Treasury rate, 40 days | .05216 | .05095 | .03789 | .03638 |
| Eurodollar, 40 days | .11163 | .10834 | .07886 | .07342 |
| Yen/dollar, 80 days | .04148 | .04068 | .03027 | .02871 |
| Boeing, 80 days | .12970 | .12504 | .09393 | .08877 |
| International Paper, 80 days | .10979 | .10473 | .07372 | .07050 |

For the S&P at $n=40$, the RMSFE reduction is approximately 7.0% and the MAFE reduction approximately 5.2%, calculated from these cells. GARCH's S&P ten-day RMSFE is 0.06461, marginally better than AMAD(40)'s 0.06477, while its MAFE is 0.03721, worse than AMAD(40)'s 0.03679. This is a clean example of loss-dependent ranking without changing asset, horizon, or sample.

Selecting the best lookback within AMAD, it beats GARCH's ten-day MAFE in all nine series, but wins RMSFE in only four: Eurodollar, yen/dollar, Boeing, and International Paper. GARCH wins the other five RMSFE comparisons. AMAD's best lookbacks are 40 or 80 days, not 10 days. The authors report 31 of 36 same-lookback comparisons significant at 10% and 16 at 5%; because separate test results are not printed, these remain author-reported aggregate claims rather than independently verifiable cell-level inference.

At twenty days, S&P AMAD(40) has RMSFE 0.06109 against STD(40)'s 0.06643 and GARCH's 0.06141. Its MAFE is 0.03434 against 0.03635 and 0.03468. Eurodollar STD(80) has the best RMSFE, 0.09820, compared with AMAD(80)'s 0.09864 and GARCH's 0.10012. Yet AMAD(80)'s Eurodollar MAFE is 0.06798 versus STD(80)'s 0.07106 and GARCH's 0.07588. The same distribution can favor STD for rare large errors and AMAD for typical errors.

There are further small-lookback exceptions in Table 3: GM MAFE favors STD(10), 0.07424 versus 0.07486, as the narrative notes; Eurodollar MAFE also favors STD(10), 0.08025 versus 0.08198, although the prose does not enumerate it. Merck's best AMAD MAFE and GARCH MAFE are both 0.05442 to the printed precision. This should be reported as a numerical tie, not decisive superiority.


## A reproducible forecast-origin ledger

An implementation should store one row per series, origin date, lookback, horizon, and method, with separate columns for the last input date and last target date. For a forecast made after observing day $t$, the historical window ends at $t$ and the target begins at $t+1$. The most common indexing error in this experiment is to include $r_t$ in both the forecast input and the future realized window, making the task partly contemporaneous measurement. Another is to shift the GARCH recursion twice and compare a two-step variance forecast with a one-step target. Explicit date columns make both errors visible.

Only origins with all required historical and future observations belong in a given comparison. If observations are absent because a series was not quoted on a particular calendar date, “20 days” should mean 20 retained daily observations under a documented calendar, not an unexamined 20-calendar-day offset. A rate series with a missing quotation and a stock series with an exchange holiday need not have identical calendars. The paper supplies the intended trading-day convention but not the complete common-origin ledger.

The GARCH re-estimation schedule also needs an anchor. Number the eligible observations after the initial 1,260-point fit and re-estimate at every fortieth subsequent observation under the chosen schedule. Record the exact last date entering each parameter fit. On intervening dates, update $v_t$ using the newest squared return while retaining that parameter vintage. If a fit fails, a fallback such as retaining the prior valid parameters must be separately identified; dropping only difficult volatility episodes could materially bias the comparison. No original fallback is reported.

To reproduce a Diebold–Mariano comparison, define paired loss differences on exactly the same origins. For squared-error comparison one may use $d_t=e_{A,t}^2-e_{B,t}^2$; for absolute loss use $d_t=|e_{A,t}|-|e_{B,t}|$. A positive sample mean means method B has lower average loss. The generic statistic is

$$
DM=\frac{\overline d}{\sqrt{\widehat\omega/T}},
\qquad
\widehat\omega=\widehat\gamma_0+2\sum_{l=1}^{L}k_l\widehat\gamma_l,
$$

where $\widehat\gamma_l$ are autocovariances of $d_t$ and $k_l$ define a chosen long-run variance estimator. The root in RMSFE is monotone, so comparing mean squared losses gives the same ranking as comparing their square roots. It does not make the loss-difference time series independent. Overlapping future windows create dependence, and persistent forecasts can extend dependence beyond mechanical overlap; the bandwidth should be justified rather than inferred from an unreported setting.

The target itself has finite-sample noise. Even if future daily returns were iid normal with constant variance, the square root of their average square is not an unbiased estimate of the population standard deviation. A forecast that is optimal for latent variance is therefore not automatically optimal for this observed standard-deviation target. This is one reason to keep conclusions tied to the actual loss and target used. It is also why a ranking change under a different future volatility proxy would not necessarily contradict the manuscript.

A minimal verification set should recover the full-sample descriptive moments, compare independently calculated AMAD and STD values on a few dated windows, and reproduce selected table cells before evaluating aggregate rankings. Preserve original precision during loss calculations and round only the reported tables: very small differences, including the printed Merck tie, can reverse under premature rounding. These controls implement the paper's experiment without adding a new optimized model or retrospectively choosing favorable dates.

## Longer horizons and limits of the conclusion

At eighty days, longer historical windows generally become more valuable. AMAD(80) improves on AMAD(40) for every market under both reported losses. That is a result within the tested maximum of 80 days, not evidence that 80 is globally optimal or that still longer lookbacks cannot help. For the S&P, AMAD(80) has RMSFE 0.05926 and MAFE 0.03567; STD(80) gives 0.06535 and 0.03846; GARCH gives 0.05994 and 0.03638.

The long-horizon exceptions are economically informative. For Eurodollars at eighty days, STD(80) gives RMSFE 0.08238 and MAFE 0.06254, beating AMAD(80)'s 0.08678 and 0.06516. GARCH's 0.08351 RMSFE is between them, while its 0.06763 MAFE is worse than both. For yen/dollar, STD(80) gives 0.02940 RMSFE and 0.02215 MAFE, also below AMAD(80)'s 0.03013 and 0.02247. These counterexamples establish that the Gaussian absolute-moment correction is not harmless across all return shapes and horizons.

Merck particularly favors GARCH at longer horizons. At eighty days GARCH yields RMSFE 0.05890 and MAFE 0.04366, versus AMAD(80)'s 0.06607 and 0.04767. A claim that simplicity incurs no forecasting cost everywhere would therefore overstate the evidence. Conversely, International Paper strongly favors AMAD(80), with RMSFE 0.07367 versus GARCH's 0.08343 and MAFE 0.04884 versus 0.05684. Cross-series variation matters as much as the average ranking.

The narrative also says STD(80) beats AMAD(80) by both criteria for yen/dollar at the 40- and 80-day horizons. Table 4 only supports the RMSFE comparison at 40 days: 0.03206 versus 0.03220. MAFE instead favors AMAD, 0.02331 versus 0.02368. At 80 days both criteria do favor STD. This distinction avoids turning an approximate narrative summary into a false table transcription.

The authors attribute Eurodollar weakness to its greater deviation from normality. That is a plausible interpretation supported by the large normality-test distance, but the study does not isolate distributional shape experimentally from rate-level effects, persistence, structural changes, or data discreteness. It also contains no simulation holding dynamics fixed while changing the innovation distribution. The association is therefore evidence consistent with the calibration explanation, not a causal decomposition of forecast errors.

For reproduction, retain the full-period centering convention, exact annualization, common forecast origins, raw rate transformations, and every $n$–$s$ pair before judging rankings. Separate table-cell comparisons from authors' aggregate significance statements. Then test a genuinely recursive mean and prespecified window rule, explicitly handling overlapping losses. Option-pricing use additionally requires a risk-neutral variance assessment, maturity-specific dynamics, and pricing/hedging evaluation; this paper supplies none of those. Its defensible practical conclusion is narrower and useful: a Gaussian-scaled rolling mean absolute deviation is a strong low-complexity baseline for historical volatility forecasts, with clear distributional and loss-function qualifications.
