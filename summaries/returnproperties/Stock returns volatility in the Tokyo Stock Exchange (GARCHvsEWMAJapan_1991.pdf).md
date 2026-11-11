# Stock returns volatility in the Tokyo Stock Exchange

Y. K. Tse, *Japan and the World Economy* 3 (1991), 285–298. [Source PDF](../../Finance/GARCHvsEWMAJapan_1991.pdf). This note covers all 14 pages, including the four tables, three figures, footnotes, and references. Printed page 285 is PDF page 1. The empirical results belong to the 1986–1989 Japanese market; the paper provides no later validation.

## Why this matters

A statistically convincing volatility model can produce poor forecasts when its parameters are estimated over a changing regime. Tse documents that distinction using the Topix and Nikkei Stock Average. Conditional heteroskedasticity and nonnormal standardized innovations improve the description of returns, yet a simple exponentially weighted forecast has the lowest reported out-of-sample squared and absolute errors. Better in-sample likelihood does not translate into better prediction of the particular 25-day variance proxy used here.

The contribution is an early comparative experiment in a market moving from the turbulence around the October 1987 crash into quieter conditions. It is not a theorem that EWMA dominates GARCH or an empirical ranking valid across markets. The source itself contrasts its findings with earlier New York evidence and emphasizes the unusual evaluation period. For implementation, its most useful lesson is to separate model fit, parameter stability, aggregation horizon, and forecast-loss definition. Several printed equations require qualifications before the experiment can be turned into executable code.

## Data, timing, and units

The inputs are daily closing index levels from the first trading day of 1986 to the last trading day of 1989, partly obtained from the Nikkei Economic Electronic Database System. Topix is value weighted and covers the First Section of the Tokyo Stock Exchange. The Nikkei Stock Average, abbreviated NSA, is price weighted and contains 225 selected First Section stocks. No individual-stock portfolio is formed.

The return definition is

$$
R_t=\log(I_t/I_{t-1}).
$$

There are 1,072 returns per index. These are index-price returns under the stated construction; no dividend reinvestment adjustment is described. The descriptive analysis partitions the first 1,050 observations into 42 nonoverlapping blocks of 25 days and discards the final 22 observations. The use of 25 trading days reflects the historical exchange calendar: until February 1989 there were two or three Saturday sessions per month. Substituting a modern 21-day month would change both the sample partitions and the forecast target.

For descriptive block $r$, the paper reports

$$
S_r^2=25\frac{\sum_{i=1}^{25}(R_{25(r-1)+i}-\bar R_r)^2}{24}.
$$

The multiplier 25 converts a daily sample variance into an estimate of a 25-day return variance under an uncorrelated-return assumption. This is not the sample variance itself and is not annualized. With decimal returns its units are squared decimal returns. Table 1 gives:

| Index | First 21 blocks, crash omitted | First 21 blocks, crash retained | Last 21 blocks |
|---|---:|---:|---:|
| Topix | 0.003078 | 0.004715 | 0.001192 |
| NSA | 0.002790 | 0.004470 | 0.001143 |

Even after excluding the crash, the last-half average is only about 38.7% of the first-half Topix average and 41.0% of its NSA counterpart. Those ratios concern variances; ratios of standard deviations would be their square roots. The paper reports that Topix fell 15.8% on October 20, 1987 and recovered 9.0% on October 21. The crash block's variance is 0.03682; omitting these two observations reduces the reported value to 0.002456. This illustrates the influence of the two observations rather than a general rule for deleting crashes.

The estimation and forecast experiment uses a different partition from this descriptive display. Initial model fitting uses 547 observations, approximately January 1986–December 1987. The remaining 525 observations form 21 blocks of 25 days. The first forecast therefore targets observations 548–572 and the last targets 1048–1072. It would be incorrect to carry the descriptive deletion of 22 final observations into the forecasting exercise.

## Conditional mean and variance models

The conditional mean is AR(1):

$$
R_t=\beta_0+\beta_1R_{t-1}+\epsilon_t,\qquad
\epsilon_t=\sigma_tu_t.
$$

The standardized innovation has mean zero and variance one. The general conditional-variance specification is

$$
\sigma_t^2=\omega^2+\sum_{i=1}^{p}\alpha_i\epsilon_{t-i}^2+
\sum_{j=1}^{q}\gamma_j\sigma_{t-j}^2,
\qquad \alpha_i,\gamma_j\ge0.
$$

The intercept is written as $\omega^2$, and Table 2 reports $\omega$, not the variance intercept. The estimation uses returns in percent. Consequently a table value $\omega=0.2013$ means an intercept $0.2013^2$ in squared percentage-return units, not a decimal-return variance of 0.2013. Converting a percent-return variance to decimal-return variance divides by 10,000.

The ARCH alternative sets all $\gamma_j=0$ and uses linearly declining coefficients:

$$
\alpha_i=\alpha\frac{2(p+1-i)}{p(p+1)},\qquad i=1,\ldots,p.
$$

The weights sum to one, so the sum of the ARCH coefficients is $\alpha$. This reduces the number of free variance parameters even when $p$ is large. The paper searches integer orders from 12 through 20 and chooses the largest likelihood. Because the constrained weight profiles differ with $p$, these alternatives are not nested in the ordinary likelihood-ratio sense. Their selected orders are retained throughout the subsequent forecasting experiment.

The other alternative is GARCH(1,1):

$$
\sigma_t^2=\omega^2+\alpha\epsilon_{t-1}^2+\gamma\sigma_{t-1}^2.
$$

For a covariance-stationary specification with unit-variance innovations, the unconditional innovation variance is $\omega^2/(1-\alpha-\gamma)$ when $\alpha+\gamma<1$. For the restricted ARCH model the corresponding denominator is $1-\alpha$. These identities are useful diagnostics; the paper's normal Topix ARCH estimate has $\alpha>1$, so it cannot be assigned a finite stationary variance through this formula.

The AR(1) choice captures the small but significant first-order return autocorrelation described in the earlier study. A low-coefficient MA(1) could be empirically difficult to distinguish. Day-of-week dummies are omitted despite the existence of weekday effects in the market; the paper appeals to prior evidence about their limited effect on dependence, rather than testing that omission afresh here.

## Nonnormal likelihood and its admissibility

The nonnormal specification uses a truncated Gram–Charlier expansion:

$$
f(u)=\phi(u)\psi(u),\qquad
\psi(u)=1+\frac{\lambda_3}{6}(u^3-3u)
+\frac{\lambda_4}{24}(u^4-6u^2+3).
$$

Here $\phi$ is the standard normal density. Gaussian orthogonality gives $E[u]=0$, $E[u^2]=1$, $E[u^3]=\lambda_3$, and $E[u^4]=3+\lambda_4$, provided the expression is a valid density. Thus $\lambda_4$ is excess kurtosis, although the source calls it a standardized measure of kurtosis. Setting both coefficients to zero recovers normality.

Integrating to one is insufficient: the quartic $\psi$ can be negative. The paper estimates without a global positivity constraint and retains only estimates judged to define valid densities. It explicitly declines squared-polynomial or constrained alternatives because they alter the immediate moment interpretation. A faithful implementation should therefore check global nonnegativity after fitting, not just positivity at the observed residuals. For a quartic with positive leading coefficient, evaluate its real stationary points and its tails. Merely obtaining a finite sample log-likelihood does not establish admissibility outside the sample.

For raw residuals $\epsilon_t$ and conditional standard deviations $\sigma_t$, change of variables implies the log-likelihood contribution

$$
\ell_t=-\log\sigma_t-\frac{\epsilon_t^2}{2\sigma_t^2}
+\log\psi(\epsilon_t/\sigma_t)+\text{constant}.
$$

Printed Eq. (8), visually checked on PDF page 6, omits $\sigma_t^2$ from the denominator of the quadratic term while Eq. (2) defines $\epsilon_t$ as an unstandardized residual. The expression above follows directly from the density and is an algebraic reconstruction, not evidence about the actual estimation code. Literal use of the printed quadratic term would not be the likelihood of Eq. (3).

The initial 547-observation fits include separate mean-shift indicators for October 20 and 21, 1987. In a heteroskedastic dynamic model this is not generally equivalent to deleting those observations: fitted residuals affect later conditional variances, and a mean parameter affects the variance recursion indirectly. The paper expressly warns against treating the familiar linear-regression deletion equivalence as applicable here.

## Initial estimation results

The following values are transcribed from Table 2. N denotes normal innovations and NN the Gram–Charlier specification. The rows for $\alpha$, $\gamma$, and the order must be read with the different model structures above.

| Index/model | $\beta_0$ | $\beta_1$ | $\omega$ | $\alpha$ | $\gamma$ or ARCH order | $\lambda_3$ | $\lambda_4$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Topix GARCH NN | 0.1225 | 0.2316 | 0.2013 | 0.1887 | 0.7957 | fixed 0 | 1.2612 |
| Topix GARCH N | 0.1121 | 0.2825 | 0.2114 | 0.2120 | 0.7723 | 0 | 0 |
| Topix ARCH NN | 0.1300 | 0.2124 | 0.3799 | 0.9614 | $p=17$ | fixed 0 | 1.2901 |
| Topix ARCH N | 0.1192 | 0.2576 | 0.3408 | 1.0324 | $p=16$ | 0 | 0 |
| NSA GARCH NN | 0.1163 | 0.1558 | 0.1854 | 0.1935 | 0.7964 | −0.3303 | 0.9250 |
| NSA GARCH N | 0.1204 | 0.2162 | 0.2082 | 0.1949 | 0.7798 | 0 | 0 |
| NSA ARCH NN | 0.1147 | 0.1618 | 0.3752 | 0.9776 | $p=16$ | −0.3084 | 1.0418 |
| NSA ARCH N | 0.1262 | 0.2093 | 0.3822 | 0.9714 | $p=13$ | 0 | 0 |

For the NN GARCH fits, $\alpha+\gamma$ is 0.9844 for Topix and 0.9899 for NSA. Strong persistence does not imply an exactly integrated process. The normal Topix ARCH estimate 1.0324 is the explicit exception to sums below one. Table 2's NSA normal ARCH order is 13; this is easily misread in text extraction.

The Topix skewness coefficient is removed as insignificant. NSA's GARCH skewness is −0.3303 with standard error 0.1329; its ARCH skewness is −0.3084 with standard error 0.1374. The excess-kurtosis coefficients are about 0.93–1.29 with standard errors about 0.31. The normal model's AR coefficients are consistently larger than the corresponding NN estimates. These are fitted distributional differences, not evidence that the NN models will forecast variance more accurately.

The reported likelihoods for Topix GARCH NN/N are −242.86/−254.17, and for NSA GARCH NN/N −214.80/−224.85. In the ARCH comparisons the selected orders can differ, so a naive nested likelihood-ratio interpretation is not appropriate. The paper uses 30-lag Box–Pierce statistics on residuals and squared residuals. Only the squared-residual diagnostic of NSA ARCH NN is marked significant at 5%, with $Q_2(30)=49.40$. Passing the other diagnostics means the specified tests did not reject; it does not establish structural parameter stability or conditional normality.

## Forecast origins, targets, and competing forecasts

Let $T_s=522+25s$ for forecast block $s=1,\ldots,21$. At each origin, fit on the 300 returns $T_s-299,\ldots,T_s$ and forecast $T_s+1,\ldots,T_s+25$. Move the origin forward 25 days, dropping the oldest 25 observations and adding the newest 25. Thus the window is rolling, not expanding. The first estimation window is observations 248–547.

In these reestimations the crash dummies are not refitted. Instead, the crash observations are adjusted by subtracting previously estimated means, taken as −16% and +9%, respectively. The adjustment is also applied to EWMA. The paper says individual fitted dummy effects differed from the observed returns by no more than two percentage points. This is a material data transformation chosen using the initial estimation sample. The implementation needs to keep raw and adjusted series separate and record precisely which methods consume each; the text is less explicit about the naive forecast's adjustment treatment.

The ex post benchmark for each forecast block is

$$
V_{B,s}^2=q_s\frac{\sum_{i=1}^{25}(R_{T_s+i}-\bar R_s)^2}{24},
\qquad
q_s=\sum_{i=1}^{25}\sum_{j=1}^{25}\widehat\beta_{1,s}^{|i-j|}.
$$

Equivalently $q_s=25+2\sum_{k=1}^{24}(25-k)\widehat\beta_{1,s}^{k}$. The benchmark uses the forecast block's own sample mean, not the historical mean or a risk-free return. Its AR coefficient is estimated at the forecast origin and changes across origins. The paper does not state which model's AR estimate defines a common benchmark when the four fitted models give different coefficients. Reusing a model-specific benchmark for each competitor would change the target across methods; a replication must resolve and disclose this choice.

The footnote's claim of unbiasedness when $\beta_1$ is known is not exact for a sample variance centered on the same correlated observations. For a stationary AR(1) with marginal variance $v$ and $H=25$, elementary covariance algebra gives

$$
E[s_H^2]=v\frac{H-q/H}{H-1},\qquad
\operatorname{Var}\left(\sum_{i=1}^{H}R_i\right)=qv.
$$

Therefore $qs_H^2$ is generally biased for $qv$ when $q\ne H$. This is an additional derived qualification; time-varying conditional variance makes the interpretation still more delicate. The benchmark is an observable variance proxy, not an independently observed conditional variance.

The naive forecast is 25 times the daily sample variance from the 300-observation estimation window, using divisor 299. It does not use the benchmark's $q_s$ multiplier. Printed Eq. (11) specifies the block-level EWMA recursion as

$$
V_{E,s}^2=\theta V_{E,s-1}^2+(1-\theta)V_{N,s-1}^2,
\qquad \theta=0.84.
$$

The subscript in the second term is $N$, the naive-variance notation, as verified on PDF page 10. It should not silently be replaced by the latest squared daily innovation or realized block variance. The initial $V_{E,0}^2$ is described as the sample variance of the last 25 observations in the estimation period. The prose does not fully specify its 25-day scaling or the initialization needed for $V_{N,0}^2$. The smoothing parameter is selected by minimizing in-sample mean squared error and then held fixed throughout all 21 evaluation blocks; the objective's initialization and exact calibration sequence are not supplied. Consequently the reported table can be studied, but its EWMA series is not completely determined by the text alone.

The paper's ARCH aggregation formula also needs care. For a clean reimplementation, define $h_j=E_{T_s}[\epsilon_{T_s+j}^2]$. In an ARCH($p$) model, compute

$$
h_j=\omega^2+\sum_{i=1}^{p}\alpha_i m_{j-i},\qquad
m_k=\begin{cases}\epsilon_{T_s+k}^2,&k\le0,\\h_k,&k>0.\end{cases}
$$

For GARCH(1,1), set $h_1=\omega^2+\alpha\epsilon_{T_s}^2+\gamma\sigma_{T_s}^2$, then

$$
h_j=\omega^2+(\alpha+\gamma)h_{j-1},\qquad j\ge2.
$$

Under fixed parameters and conditionally orthogonal future innovations, the AR(1) return aggregation is exactly

$$
\operatorname{Var}_{T_s}\left(\sum_{j=1}^{H}R_{T_s+j}\right)
=\sum_{j=1}^{H}\left(\sum_{k=0}^{H-j}\beta_1^k\right)^2h_j.
$$

This accounts for an early innovation's effect on all later returns in the block. For $\beta_1\ne1$ the inner sum is $(1-\beta_1^{H-j+1})/(1-\beta_1)$; at one use the finite-sum limit. This conditional variance is a model forecast, whereas the ex post benchmark above is a differently constructed proxy.

Printed Eq. (12) instead applies scalar powers of the sum $\alpha$ to a distributed-lag ARCH model and prints the initial-term exponent as $20-t$ despite a 25-day horizon. A scalar persistence recursion is valid for ARCH(1) or the GARCH conditional-mean recursion, but not generally for the declining-weight ARCH($p$) used here. For example, take $p=2$, intercept 0.1, $\alpha_1=0.4$, $\alpha_2=0.2$, and last squared innovations 1 and 0. Then $h_1=0.5$ and the exact $h_2=0.1+0.4(0.5)+0.2(1)=0.5$, whereas a scalar sum-coefficient recursion gives $0.1+0.6(0.5)=0.4$. With $z=h_1$ and reverse index $t=H-j+1$, the scalar formula's initial-term exponent would be $H-t=25-t$. These are visually checked mathematical inconsistencies, not confirmation that the original numerical program used the printed formula. The recursive implementation above is explicitly reconstructed and may therefore fail to reproduce Table 3 even with the original data.

## Reported forecast errors

For forecast-minus-benchmark errors $e_s=\widehat V_s^2-V_{B,s}^2$, the statistics are mean error, RMSE, mean absolute error, and mean absolute proportional error:

$$
Z_1=\frac1{21}\sum_se_s,\quad
Z_2=\sqrt{\frac1{21}\sum_se_s^2},\quad
Z_3=\frac1{21}\sum_s|e_s|,\quad
Z_4=\frac1{21}\sum_s\frac{|e_s|}{V_{B,s}^2}.
$$

Table 3 multiplies the first three statistics by 1,000; it does not multiply $Z_4$ by 100. A displayed proportional error of 0.796 means 79.6%, not 0.796%. The reported values are:

| Index/model | $1000Z_1$ | $1000Z_2$ | $1000Z_3$ | $Z_4$ |
|---|---:|---:|---:|---:|
| Topix naive | 0.464 | 2.324 | 1.545 | 1.080 |
| Topix ARCH N | 0.958 | 2.809 | 1.969 | 1.537 |
| Topix GARCH N | 0.453 | 2.999 | 2.528 | 1.994 |
| Topix ARCH NN | 2.399 | 4.012 | 3.088 | 2.365 |
| Topix GARCH NN | 2.433 | 5.225 | 3.358 | 2.615 |
| Topix EWMA | 0.081 | 2.140 | 1.220 | 0.796 |
| NSA naive | 0.743 | 1.704 | 1.343 | 1.356 |
| NSA ARCH N | 0.653 | 1.711 | 1.244 | 1.099 |
| NSA GARCH N | 0.160 | 1.931 | 1.674 | 1.712 |
| NSA ARCH NN | 1.889 | 3.327 | 2.313 | 2.340 |
| NSA GARCH NN | 1.575 | 2.701 | 1.961 | 2.105 |
| NSA EWMA | 0.355 | 1.375 | 0.983 | 0.994 |

EWMA wins RMSE, absolute error, and proportional error for both indices. It does not have the smallest absolute mean error for NSA: normal GARCH has 0.160 versus EWMA's 0.355. The source's broad claim of the best forecasts should therefore be understood in terms of its main loss comparisons, not dominance in every reported column. Relative to the naive forecast, EWMA's RMSE is about 7.9% lower for Topix and 19.3% lower for NSA. These are arithmetic comparisons of reported values, not statistical significance estimates.

The NN models fit better in sample but forecast worse than their normal counterparts under all three nonnegative error losses. Figures 2–3 show a normal-GARCH forecast peak near evaluation block 5 while observed block variance has dropped. EWMA approaches the lower post-crash level more smoothly. These plots support the regime-adaptation interpretation but do not uniquely identify parameter instability as the cause; benchmark construction and forecast equations also matter.

Table 4 reports the variation of fitted $\omega$ across the 21 rolling fits. For Topix, mean/standard deviation is 0.4225/0.1796 for GARCH N, 0.3792/0.1395 for GARCH NN, 0.5334/0.1395 for ARCH N, and 0.6205/0.1479 for ARCH NN. NSA counterparts are 0.5188/0.1937, 0.5063/0.1851, 0.4980/0.1103, and 0.5394/0.0862. These are dispersions of an estimated intercept scale across overlapping estimation windows. They are neither standard errors of an average nor a formal break-test statistic, and they do not measure variation in the full forecast function.

## What can and cannot be reproduced

The source gives the historical universe, sample lengths, rolling-window timing, constrained ARCH weights, selected orders, density family, initial parameter estimates, and aggregate error tables. It does not supply the daily levels, complete trading-date index, initial variance backcasts, optimization constraints or tolerances, 21 sets of rolling coefficients, forecast vectors, or code. The crash-adjustment allocation, benchmark AR coefficient, EWMA initialization and scaling, and printed aggregation formula require resolution before exact numerical replication can be claimed.

An implementation should first reproduce the descriptive block partition, then the initial likelihood fits in percentage units, then the 21 rolling forecast origins. Check each fitted innovation density globally, retain the distinction between $\omega$ and $\omega^2$, and store daily variance forecasts before aggregation. Use one explicit benchmark per index and date. Retain a literal-source branch and a corrected-recursion branch if investigating the printed discrepancies; do not call differences between those branches reproduced published results.

The paper reports only 21 forecast losses per index and no uncertainty intervals, pairwise forecast tests, multiple-comparison correction, or economic-loss evaluation. The observation that a model improves RMSE does not show a statistically reliable advantage, superior option prices, reduced margin shortfalls, or profitable trading after costs. Option pricing and variation-margin management motivate the exercise, but neither is implemented. No option chain, transaction-cost model, position sizing, or realized investment P&L is supplied.

The results are most informative as a warning about extrapolating a fitted persistent variance process across a sharp decline in volatility. The historical experiment favors the simple forecast in its reported evaluation; the model equations and missing inputs limit stronger claims about exact replication or general forecasting superiority.
