# Measuring volatility with the realized range

**Authors:** Martin Martens and Dick van Dijk. **Version:** July 15, 2005 working paper, 31 PDF pages, with printed text and table pages 1–30 after the title page. **Source:** [VolatilityHighLow_MartensVanDijk_2005.pdf](../../Finance/VolatilityHighLow_MartensVanDijk_2005.pdf). This note uses the supplied working paper's results, not a later publication's revised tables. The other Martens–van Dijk filenames in the library are aliases or related versions of this work, not additional independent contributions.

## Why this matters

A squared return retains only two prices from an interval. A high-low range uses information about the path between them. The paper's innovation is to apply the Parkinson range estimator repeatedly within a day and sum the interval variance estimates. This “realized range” can achieve the precision of return-based realized variance at a coarser sampling frequency. Coarser intervals may be useful because very high-frequency prices are contaminated by bid-ask bounce and imperfect observation of the efficient-price path.

The substantive finding is more qualified than “ranges are robust to noise.” With the same interval length, bid-ask bounce can contaminate ranges more strongly than squared returns. Sparse trading also creates a downward range bias by missing the actual extrema. The realized range nevertheless performs well for many moderately spaced observations because its ideal statistical efficiency is high, and opposing biases sometimes partly cancel. Cancellation is a property of the setting, not an estimator guarantee.

The paper contributes a transparent Monte Carlo comparison and evidence from S&P 500 futures and S&P 100 stocks. It does not derive an implementable optimal sampling-frequency selector or a general noise-robust estimator. Formal high-frequency range asymptotics are attributed to concurrent work by Christensen and Podolskij. The empirical forecasting comparisons are mainly devices for assessing information in the competing variance measures; they are not a clean out-of-sample trading strategy with transaction costs.

## Estimator, units, and the ideal efficiency calculation

Section 2 starts with a geometric Brownian price,

$$
dP_s=\mu P_s\,ds+\sigma P_s\,dB_s.
$$

The log price $p_s=\log P_s$ has drift $\mu^*=\mu-\sigma^2/2$ and diffusion coefficient $\sigma$. Normalize a day to one and divide it into $I$ equal subintervals of length $\Delta=1/I$. For interval $i$, let $H_{t,i}$ and $L_{t,i}$ be its highest and lowest prices, and let $C_{t,i}$ be its closing price. Define the interval log return and log range as

$$
r_{t,i}=\log C_{t,i}-\log C_{t,i-1},\qquad
R_{t,i}=\log H_{t,i}-\log L_{t,i}.
$$

The two daily variance estimators are

$$
RV_t=\sum_{i=1}^I r_{t,i}^2,\qquad
RR_t=\frac1{4\log2}\sum_{i=1}^I R_{t,i}^2.
$$

The range must be squared before aggregation and divided by $4\log2$. Neither the sum of unsquared ranges nor the square of the sum estimates the same object. Both quantities have squared-log-return units; volatility in standard-deviation units requires a square root afterward. If returns are expressed in percent instead of decimals, both variance measures multiply by $10^4$.

For a continuously observed path with constant volatility and zero log drift, both interval estimators are unbiased for $\sigma^2\Delta$. Their variances are

$$
\operatorname{Var}(r_{t,i}^2)=2\sigma^4\Delta^2,
$$

$$
\operatorname{Var}\left(\frac{R_{t,i}^2}{4\log2}\right)
=\left(\frac{9\zeta(3)}{(4\log2)^2}-1\right)\sigma^4\Delta^2
\approx0.407\sigma^4\Delta^2,
$$

where $\zeta(3)=\sum_{k\geq1}k^{-3}$. Independent Brownian increments then give daily estimator variances $2\sigma^4\Delta$ and approximately $0.407\sigma^4\Delta$. The efficiency ratio is about 4.91 in variance, or about 2.22 in standard error. It is not a fivefold reduction in standard error.

This calculation explains the gain from retaining path extrema. It also explains why the advantage is less important in an ideal world with free continuous observation: either estimator approaches integrated variance as the mesh shrinks. The practical case arises because observation and noise constrain that mesh. The finite-interval unbiasedness result assumes zero log drift and constant volatility. The paper cites an extension to intraday varying variance, but does not prove it here. Finite drift, jumps, dependent observation times, and market frictions should not be swept into the simple exact Brownian formulas.

## Reconstructing the simulation

Section 3 simulates 1,000 independent 24-hour days. Each starts at price one. There are $J=8{,}640{,}000$ latent observations per day, corresponding to 100 per second. Set annual standard deviation to 0.21 and annual trading days to $D=250$. Simulate independent log increments

$$
p_{t,j}-p_{t,j-1}\sim N\left(0,\frac{0.21^2}{250J}\right).
$$

Daily true variance in decimal-return units is $0.21^2/250=0.0001764$. The simulation tables use 4.41 as the true variance level. This is consistent with multiplying annual decimal variance by 100, equivalently multiplying daily decimal variance by 25,000. It is not the variance of each simulated increment, despite the abbreviated table captions. This scale reconstruction follows from the stated 21% annual standard deviation and the table values; a replication should report the conversion explicitly.

Partition each day into intervals of 1, 2, 3, 4, 5, 10, 20, 30, 45, 60, 90, 120, 180, 240, 360, 720, or 1,440 minutes. Compute $RR$ from all retained observations inside each interval, while $RV$ uses adjacent interval endpoints. Across days report mean, standard deviation, and root mean squared error relative to the known daily variance, all in the same display units. At 1,440 minutes the estimators reduce to the daily range and daily squared return.

Four observation environments are compared. The first uses the dense latent grid without additional frictions. The second retains each latent observation independently with probability $\pi=0.001$, giving an average observation every ten seconds. More generally, a desired mean gap $\tau$ seconds corresponds to $\pi=1/(100\tau)$. The third observes a price displaced from the latent price by plus or minus half a fixed spread, with equal probabilities. The fourth combines thinning with these bid/ask displacements.

The main text sets the spread to $s=0.0005$ on the starting price of one. Tables 3 and 4 instead print $s=0.005$. These differ by a factor of ten. The main-text value is consistent with the reported $RV$ upward bias: at one-minute spacing, $I=1{,}440$ and the approximate added daily variance from independent bid/ask signs is $Is^2/2$. With $s=0.0005$ this becomes 4.5 in the tables' display units, agreeing with the increase from 4.41 to 8.909. With $s=0.005$ it would be roughly one hundred times larger. This arithmetic strongly supports 0.0005, but the caption discrepancy remains an error in the supplied source.

The source does not specify random seeds, handling of intervals with no retained price, interpolation or previous-tick rules at boundaries, or exact inclusion of interval endpoints in the high and low. In a replication these choices should be recorded. Thinning is independent of volatility here; it is not an endogenous trade-arrival model. The price spread is fixed in price units rather than fixed as a fraction of the evolving price.

## What the simulated numbers establish

Table 1's five-minute dense-grid range has mean 4.365, standard deviation 0.151, and RMSE 0.157; realized variance has mean 4.428, standard deviation 0.343, and RMSE 0.344. The slight negative range bias persists even on the fine grid because a discretely sampled maximum falls short of the true continuous maximum and a sampled minimum exceeds the true minimum. At one minute the range mean is 4.296 and RMSE 0.134, compared with realized-variance RMSE 0.159. The finite-grid bias prevents treating this simulation as literal continuous observation.

Under ten-second average trading gaps, Table 2 shows a severe one-minute range bias: mean 2.433 and RMSE 1.978, while realized variance remains near 4.413 with RMSE 0.161. At five minutes range RMSE is 1.107 versus 0.348 for realized variance. At thirty minutes, however, the comparison reverses: 0.615 versus 0.891. The minimum reported range RMSE rounds to 0.615 at both thirty and forty-five minutes. The text emphasizes roughly forty-five minutes; the rounded table does not support a unique minimum between those two choices.

With bid-ask bounce alone, Table 3's five-minute range mean rises to 8.200 and RMSE to 3.795, whereas realized variance has mean 5.325 and RMSE 1.010. A densely observed range tends to include an ask near the efficient high and a bid near the efficient low, expanding the observed range by roughly the spread. Squaring produces a cross term involving the efficient range as well as a spread-squared term. Return-based variance has a different bias mechanism, arising from changes in transaction side across endpoints. This is why range efficiency in the ideal model does not translate into noise robustness at the same frequency.

The best reported range RMSE under bounce alone is 1.082 at ninety minutes. The best realized-variance RMSE is 0.705 at ten minutes. Thus even after selecting the best frequency on each reported grid, realized variance wins this particular environment. It would be inaccurate to generalize the paper's favorable combined-friction example to every simulation case.

With both frictions, Table 4 reports range RMSE 0.698 at forty-five minutes versus the best realized-variance RMSE 0.722 at ten minutes. At thirty minutes the comparison is 0.711 versus 0.934. Partial cancellation of missing-extrema bias and spread expansion explains why combining two frictions can improve the range's apparent performance. It does not imply that adding noise is a stable estimation strategy.

There is an internal inconsistency in Table 4's forty-five-minute range row: mean 5.543, standard deviation 0.507, and RMSE 0.698 cannot all hold around truth 4.41. The implied RMSE from that mean and dispersion is about 1.241. The text repeats 0.698 as the optimum. The retained note therefore reports the stated RMSE conclusion while flagging that row; it does not fabricate a corrected mean. This also limits confidence in the small numerical margin of 0.024 between the reported best estimators. Monte Carlo confidence intervals for that difference are not supplied.

## Futures data and descriptive evidence

The futures sample spans January 4, 1999 to February 23, 2004, with 1,289 trading days. The study uses the most liquid S&P 500 contract, typically rolling about a week before maturity, and never computes a return using prices from different contracts. Exact contract-selection and roll-day rules are not supplied beyond that description. The daytime floor session is 09:30–16:15 Eastern time, with electronic trading during the remainder of the day. Average transaction counts are 3,223 during the floor session and 1,802 outside it.

The initial estimator uses five-minute daytime ranges or returns and fifteen-minute overnight intervals. This separates the more and less actively traded sessions. The paper studies 54 frequency combinations: nine daytime lengths of 1, 2.5, 5, 15, 27, 33.75, 45, 81, and 405 minutes, crossed with six nighttime lengths of 5, 15, 45, 115, 207, and 1,035 minutes. These choices divide the 405-minute and 1,035-minute sessions exactly. Clock conventions around daylight saving and short sessions are not fully described.

In daily percentage-return-squared units, Table 5 reports means of 1.792 for squared close-to-close returns, 1.533 for realized range, and 1.818 for realized variance. Their time-series standard deviations are 3.263, 1.408, and 1.879 respectively. The empirical variance scale differs from the simulation display scale: the futures daily return standard deviation is about 1.339%, consistent with $\sqrt{1.792}$. Annualization then gives roughly 21%–21.4%, depending on the annual-day convention.

The smaller range dispersion partly reflects its lower mean. Scaling its standard deviation by $1.792/1.533$ gives about 1.646, still below 1.879. This supports the possibility of lower measurement noise, but observed time-series dispersion combines true variance dynamics and estimator error. It is not a direct observation of estimator MSE because the true daily integrated variance is unknown. The correlation between range and realized variance is 0.969.

Both raw variance series are skewed and heavy-tailed. Log standard deviations are closer to normal but still reject normality: Table 5 gives Jarque–Bera statistics 33.76 for the range transformation and 54.47 for the realized-variance transformation. Standardizing returns by contemporaneously measured realized standard deviations reduces kurtosis from 4.310 to 2.814 with range and 2.748 with realized variance. The range-normalized Jarque–Bera statistic is 5.966, narrowly below the 5% chi-square-two critical value 5.99; the variance-normalized statistic is 7.677. This marginal normality result concerns an ex post standardized series, not a directly tradable forecast-error distribution.

Frequency changes reveal the expected noise tradeoff. At 1/5-minute day/night sampling, Table 7 gives range mean 1.288 and realized-variance mean 1.945. At 27/45 minutes they are 1.662 and 1.707. At a daily interval the Parkinson range mean is 1.731. Increasing sampling frequency lowers the observed range mean, consistent with missing extrema, while increasing return-based variance through transaction noise. These patterns help diagnose bias but do not identify an optimal frequency without a target or model.

## Forecast comparison: raw predictors and fitted rolling filters

Section 4.2 avoids declaring either noisy measure to be the single truth. It evaluates predictors once with $y_t=RV_t$ and again with $y_t=RR_t$. The first predictor is yesterday's raw realized variance; the second is yesterday's raw realized range. For each, regress $y_t$ on an intercept and the lagged predictor to compare $R^2$. Also compare raw-predictor MSE and MAE, which retain sensitivity to level bias that a regression slope can absorb.

For two forecasts $\widehat y_{i,t}$ and $\widehat y_{j,t}$, the paper uses loss differentials. For MSE these are $(y_t-\widehat y_{i,t})^2-(y_t-\widehat y_{j,t})^2$; for MAE replace squared errors with absolute errors. For the $R^2$ comparison it uses fitted regression residual-square differences divided by the sample variance of $y$. The encompassing differential is

$$
d_t=(\widehat y_{j,t}-\widehat y_{i,t})(y_t-\widehat y_{i,t}),
$$

testing whether forecast $j$ adds information beyond $i$. Encompassing tests in both directions can both reject, suggesting that a combination is useful even if neither single predictor dominates everywhere.

The manuscript invokes the Harvey–Leybourne–Newbold modification of the Diebold–Mariano statistic. Its printed equation has a normalization problem: it writes $\bar d/\sqrt{\widehat V(\bar d)}$ but defines $\widehat V(\bar d)=T^{-1}\sum(d_t-\bar d)^2$, the variance of individual differences rather than their sample mean. Under independent differences, the denominator should instead be approximately $\sqrt{T^{-2}\sum(d_t-\bar d)^2}$, equivalently multiplying the printed ratio by $\sqrt T$. Serial dependence requires a long-run variance. One-step forecasting alone does not guarantee independent losses. The numerical testing code is not supplied, so this defect cannot be resolved by assuming the tables literally used the displayed formula.

The alternative forecasting scheme applies an exponential rolling filter separately to squared daily returns, ranges, and realized variances:

$$
s_{t,V}=e^{-\alpha}s_{t-1,V}+\alpha e^{-\alpha}V_{t-1}.
$$

This is the exact recursion in Equation 8. Its new-observation coefficient is $\alpha e^{-\alpha}$, not $1-e^{-\alpha}$. Replacing it with a normalized EWMA silently changes the specified filter. The resulting range-based state is scaled using 22 lagged days:

$$
\widetilde s_{t,RR}=
\frac{\sum_{l=1}^{22}s_{t-l,r^2}}{\sum_{l=1}^{22}s_{t-l,RR}}s_{t,RR},
$$

and analogously for $RV$. The numerator supplies a daily-return variance level, while the intraday input supplies a less noisy dynamic pattern. The first 100 observations initialize the states and are dropped from both raw and filtered comparisons. The decay parameter and its associated bias corrections are estimated by maximum likelihood using the full sample. Consequently the filtered experiment is not fully out of sample even though the state recursion and scaling use lagged inputs. The innovation likelihood, exact initialization statistic, and numerical optimizer are not fully specified.

The study compares full close-to-close and open-to-close targets, with and without upper truncation of outliers. Its threshold is the median plus four robust standard deviations based on an absolute-deviation measure. The manuscript calls it “Mean Absolute Deviation, MAD,” leaving the centering and scaling convention insufficiently precise. Exact reconstruction requires that convention rather than automatically substituting a modern median-absolute-deviation implementation.

## Empirical comparisons and their limits

For futures, raw range predictors generally dominate, especially at moderate intervals. Tables 8 and 9 print directional tail probabilities whose orientation differs from a conventional two-sided p-value. In the stated convention, values near one favor range. For example, the raw close-to-close comparison at the coarsest frequency has MSE entries 0.992 against both targets; the smoothed, untrimmed close-to-close counterpart has 0.992 against $RV$ and 0.982 against $RR$. After smoothing and bias adjustment, many finer-frequency differences are insignificant. The estimated futures decay parameters lie between 0.13 and 0.25.

There is a frequency-label ambiguity: the design describes the coarse futures pair as 27/45 minutes, while the tables abbreviate its daytime frequency as 30 and surrounding prose sometimes says 30/45. A replication should preserve the exactly dividing 27-minute construction as the documented design and check the table-generation implementation, rather than pretending the discrepancy is absent.

The stock analysis selects S&P 100 constituents as of June 2004. Most series run April 9, 1997 to June 18, 2004, giving 1,808 daily observations, with one-minute open/high/low/close inputs. Full-day estimates add the squared overnight close-to-open return to intraday estimates. The fixed endpoint constituent selection introduces survivorship and composition conditioning. Exact constituent identifiers, shorter-series handling, split adjustments, missing bars, and bad-price filters are not supplied.

Table 10 reports a cross-stock mean of daily mean range variance equal to 4.798. The cross-stock standard deviation of those means is 3.637; the average within-stock time-series standard deviation is 6.372. The text mistakenly describes 3.637 as the average standard deviation of the range. These are distinct quantities and should not be interchanged.

Tables 11 and 12 count significant wins at the one-sided 5% level, written realized-variance wins followed by range wins, out of 100 stocks. In the raw, untrimmed open-to-close five-minute comparison with $RV$ as target, MSE gives 3–48 and MAE 10–64. At thirty minutes MSE gives 0–80 and MAE 0–98. Against $RR$, the corresponding thirty-minute counts are 0–82 and 0–99. These are strong raw-predictor results for ranges at moderate sampling intervals.

The filtered comparisons are more mixed. For untrimmed close-to-close five-minute forecasts against $RV$, MSE counts are 30–1, favoring realized variance. With open-to-close targets and outlier truncation, thirty-minute MSE counts are 1–20 against $RV$ and 1–33 against $RR$, favoring range but leaving most stocks undecided. Estimated stock decay parameters range from 0.10 to 0.41. Claims of universal range superiority would erase this economically meaningful variation across target, filtering, overnight treatment, and outliers.

Finally, the activity regression's verbal interpretation is internally inconsistent. The authors define wins as realized-variance wins minus range wins and inactivity as minutes without a trade, then report a negative relationship while interpreting it as range doing better for more active stocks. With those stated definitions the reported sign implies the opposite. No coefficient or detailed table resolves which definition or sign is mistaken. The intuitive missing-extrema explanation is plausible, but this regression cannot independently verify it as printed.

The usable contribution is an estimator and a disciplined frequency/noise comparison. Ranges can improve moderate-frequency variance measurement, especially where enough observations reveal interval extrema. The paper also demonstrates why raw efficiency, bias adjustment, forecast evaluation, and market microstructure must be considered together. Its strongest limitations for exact replication are the simulation-caption conflicts, testing normalization, full-sample tuning, ambiguous outlier conventions, and incomplete data-cleaning details. None is cured by increasing the nominal sampling frequency.
