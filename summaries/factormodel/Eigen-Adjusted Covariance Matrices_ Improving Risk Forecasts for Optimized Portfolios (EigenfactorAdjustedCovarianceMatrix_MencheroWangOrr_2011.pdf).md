# Eigen-Adjusted Covariance Matrices: Improving Risk Forecasts for Optimized Portfolios

Jose Menchero, Jun Wang, and D. J. Orr. MSCI Research Insight, May 2011. Source: [original PDF](../../Finance/EigenfactorAdjustedCovarianceMatrix_MencheroWangOrr_2011.pdf), 21 PDF pages. Page references below refer to the PDF. This note covers the complete report, both mathematical appendices, all five figures, and Table 1.

## Why this matters and what is new

A covariance estimator can forecast the risk of individual securities and randomly chosen portfolios accurately while systematically understating the risk of portfolios selected by optimization. The optimizer searches the estimated risk surface, so its holdings depend on the same estimation errors that determine its reported risk. Testing a risk model only on portfolios independent of its covariance estimates misses this selection effect.

The report diagnoses the effect using covariance eigenvectors, interpreted as portfolios. Small estimated eigenvalues disproportionately represent directions whose risk has been underestimated; large eigenvalues tend to overestimate risk. An optimizer using inverse covariance loads strongly on the former. The proposed correction estimates this selection bias by simulating new samples from the observed covariance, comparing their estimated eigenportfolio risks with risks under the known simulation covariance, and adjusting the original eigenvalues by rank. The eigenvectors themselves remain unchanged.

The innovative component is this targeted, simulation-based correction to the risks of optimized combinations. It is not simply a uniform volatility multiplier and is not a forecast of investment alpha. A further empirical multiplier, set to 1.4, strengthens the correction beyond the Gaussian stationary simulation. This last step is important: the successful empirical method combines a principled bootstrap diagnostic with a calibrated departure from its idealized model.

## Returns, portfolios, and the covariance being estimated

The empirical universe consists of the 50 largest US stocks as of July 30, 2010 that have complete histories from July 1, 1993 to July 30, 2010. There are 4,303 daily observations. Thus the universe is selected using end-of-sample size and survival; it is not a sequence of contemporaneously investable top-50 universes.

Let $r_{nt}$ denote stock $n$'s daily return and $R_{mt}$ the capitalization-weighted return of these 50 stocks. The report defines 51 return coordinates:

$$
f_{0t}=R_{mt},\qquad f_{nt}=r_{nt}-R_{mt},\quad n=1,\ldots,50.
$$

The first coordinate is the market, while each remaining coordinate is a stock financed by a short market position. The report often denotes the number of stocks by $N=50$, although the augmented covariance has 51 coordinates. Distinguish these counts when coding the experiment.

At each forecast date, estimate covariance from the preceding $T=200$ daily observations, subtracting each coordinate's sample mean and dividing by $T-1$:

$$
V_{0t}=\frac{1}{T-1}\sum_{s=t-T}^{t-1}(f_s-\bar f_t)(f_s-\bar f_t)'.
$$

The estimate and portfolio holdings are known at the beginning of day $t$; the next daily return is the out-of-sample realization. The resulting main evaluation window is April 15, 1994–July 30, 2010, containing 4,103 trading days. There is no exponential weighting in this experiment.

An augmented holding vector $h=(h_0,h_1,\ldots,h_{50})'$ earns

$$
h'f_t=\sum_{n=1}^{50}h_nr_{nt}+\left(h_0-\sum_{n=1}^{50}h_n\right)R_{mt}.
$$

This identity makes the coordinate convention explicit. Setting $h_0=0$ gives a dollar-neutral stock-minus-market portfolio. The optimized portfolios use the report's investability constraint $h_0=\sum_{n=1}^{50}h_n$, which cancels the additional market overlay and leaves a portfolio of the 50 stocks. These are different restrictions, applied to different diagnostics.

The augmented representation is nearly redundant. If market capitalization weights were constant throughout an estimation window, a fixed weighted sum of relative returns would be exactly zero. Their movement through time removes exact redundancy in the reported sample, but the smallest eigenvalue is still particularly small. Treating this coordinate as an ordinary independent tradable asset without the stated constraint would distort optimization.

## The bias statistic

For any portfolio, let $R_t$ be its realized daily return and $\sigma_t$ its risk forecast at the beginning of that day. The standardized realization is $b_t=R_t/\sigma_t$. The report's bias statistic is the sample standard deviation of these standardized returns:

$$
B=\left[\frac{1}{\tau-1}\sum_{t=1}^{\tau}(b_t-\bar b)^2\right]^{1/2}.
$$

$B>1$ indicates that realized variation exceeds forecast risk; $B<1$ indicates overprediction. Because the forecast changes through time, this is not generally equal to unconditional realized volatility divided by the average predicted volatility. The distinction matters especially through crises.

Under approximately independent Gaussian standardized returns, the report gives a rough 95% interval $1\pm\sqrt{2/\tau}$ (p. 4). This is a normal approximation for a sample standard deviation, not a robust interval valid under arbitrary serial dependence or heavy tails. The authors emphasize large systematic biases, since forecast noise, nonlinear division by an estimated volatility, and fat tails can also move the statistic away from one.

Four portfolio classes provide the diagnostic. First are individual stock-relative returns. Second are 100 fixed random portfolios, with independent standard normal stock-relative coefficients and zero market-coordinate weight. Third are eigenfactor portfolios, recalculated daily from $V_{0t}$. Fourth are portfolios optimized against fixed random alpha vectors using each day's risk estimate.

The distinction between fixed random weights and optimized weights is essential. Both can have complicated long and short positions, but only the latter systematically choose directions favored by estimation error in the particular covariance being tested.

## Eigenfactors and optimization bias

Suppress the time subscript. Write the symmetric eigendecomposition

$$
V_0=U_0D_0U_0',\qquad U_0'U_0=I,
$$

with the eigenvalues in $D_0$ sorted from smallest to largest. Column $u_k$ of $U_0$ is a portfolio with Euclidean norm one and predicted variance $d_k=u_k'V_0u_k$. Eigenfactor returns are $u_k'f_t$. They are uncorrelated under the fitted covariance; they need not be uncorrelated out of sample or under the true covariance.

The smallest eigenvector minimizes estimated variance over vectors satisfying $u'u=1$. This is not the fully invested minimum-variance problem $\mathbf1'w=1$. Its signs and normalization are arbitrary, which is harmless for a variance diagnostic but important for interpreting holdings.

For an unconstrained portfolio with target alpha one, the standard solution is

$$
h_\alpha=\frac{V_0^{-1}\alpha}{\alpha'V_0^{-1}\alpha}.
$$

Its numerator expands as $\sum_k u_k(u_k'\alpha)/d_k$, exposing the disproportionate influence of small eigenvalues. The authors generate 100 independent standard normal raw alpha vectors. At every date they subtract each vector's current market-capitalization-weighted mean, making the alpha market-neutral in the chosen sense. The raw alpha draws are fixed through the experiment; their daily demeaning changes with capitalization weights.

These alphas are synthetic expected-return inputs. The unit-alpha normalization is a device for comparing risk at the same modeled objective, not evidence that the signals predict future returns. In the empirical augmented-coordinate implementation, the investability constraint must also be imposed. Appendix B's simple inverse-covariance formulas by themselves omit this extra constraint.

A transparent constrained implementation, derived here, minimizes $h'Vh$ subject to $C'h=d$, where $C$ contains the alpha vector and the vector encoding $h_0-\sum_nh_n=0$. For nonsingular matrices and independent constraints,

$$
h=V^{-1}C(C'V^{-1}C)^{-1}d,\qquad d=(1,0)'.
$$

Equivalently map stock holdings $w$ to augmented holdings with $h=Pw$, where $P$ has first row $\mathbf1'$ and the remaining rows $I$. Optimize using stock-space covariance $P'VP$ and the correspondingly transformed alpha. This is an algebraic implementation clarification, not an additional empirical result from the report.

Figure 1 shows stock and random-portfolio bias statistics close to one. Eigenfactor biases instead decline strongly with eigenvalue rank: the smallest modes have values around 1.7 and the largest around 0.9, read approximately from the figure. The 100 optimized portfolios cluster around $B=1.45$. A standard idealized large-sample relation cited by the authors predicts

$$
\sigma_{\rm true}\approx\frac{\sigma_{\rm predicted}}{1-N/T}.
$$

For $N=50,T=200$, this gives 1.333, less than the observed 1.45. The formula concerns optimized portfolio volatility; it is not an instruction to apply a square root to the denominator, and it is not claimed to capture the empirical covariance dynamics exactly.

## Reconstructing the eigenvalue correction

Appendix A, pp. 11–12, supplies the algorithm. It is repeated for each daily covariance estimate, using the same estimation-window length as the original estimator.

1. Diagonalize the observed $V_0$ to obtain $U_0,D_0$. Treat $V_0$ as the true covariance within the simulation.
2. For simulation $m$, generate a matrix $b_m$ of $T$ independent Gaussian observations. Its $k$th row has variance $d_{0k}$, and rows are independent. Set $f_m=U_0b_m$.
3. Compute a new sample covariance $V_m$ using the same estimator as for $V_0$, then diagonalize it as $U_mD_mU_m'$, again sorting eigenvalues in ascending order.
4. Evaluate each simulated sample eigenvector under the simulation truth. The matrix $\widetilde D_m=U_m'V_0U_m$ contains these true variances on its diagonal. Its off-diagonal elements generally are not zero.
5. For each ordered mode, compare true with fitted standard deviation and average over simulations:

$$
\lambda(k)=\frac{1}{M}\sum_{m=1}^{M}\sqrt{\frac{\widetilde D_m(k,k)}{D_m(k,k)}}.
$$

The averaging occurs after taking the square root of each variance ratio. A square root of an average ratio, or a ratio of two average variances, is a different estimator. Modes are matched by sorted rank within each simulated covariance, not by attempting to track the identity or sign of individual eigenvectors across simulations.

6. Strengthen the simulated adjustment with the empirical parameter $a$:

$$
\gamma(k)=1+a\{\lambda(k)-1\},\qquad a=1.4.
$$

7. Change the original eigenvalues and rotate back:

$$
\widetilde d_{0k}=\gamma(k)^2d_{0k},\qquad
\widetilde V_0=U_0\operatorname{diag}(\widetilde d_{0k})U_0'.
$$

Squaring $\gamma$ is necessary because the Monte Carlo correction is a volatility multiplier while the diagonal contains variances. There is no subsequent step restoring the original diagonal, no replacement of eigenvectors, and no assumption that the altered eigenvalues retain their original ordering. Symmetry and nonnegative eigenvalues follow directly; strict positive definiteness requires positive original eigenvalues and nonzero multipliers.

Appendix A writes uncentered matrix products divided by $T-1$ while describing an unbiased sample covariance. Those statements are compatible only if centering is implicit. To reproduce the main text's estimator, explicitly subtract the simulated sample mean before dividing by $T-1$. If the known zero population mean is used without centering, the unbiased divisor is $T$. This small but concrete implementation distinction should not be left to a matrix-library default.

The report does not provide $M$, random seeds, a Monte Carlo convergence tolerance, or the detailed fitting procedure that selected $a=1.4$. These omissions prevent exact numerical duplication of the figures. A replication can choose and disclose $M$, repeat with larger $M$ to measure simulation stability, and preserve 1.4 as the reported empirical calibration; it should not pretend these additional settings came from the authors.

## What the simulation and adjustment reveal

The Gaussian experiment already produces a substantial rank-dependent bias. For the smallest eigenfactor, the report describes a mean simulated volatility adjustment around 1.5, with 98% of daily estimates between about 1.4 and 1.6. For the largest mode, the mean is about 0.96, with 98% between about 0.9 and 1.0. These are distributions over forecast dates, not confidence intervals for a single fitted parameter.

The empirical enhancement has a nonlinear effect on variance. For illustration, calculated from the specified rule, $\lambda=1.5$ becomes $\gamma=1.7$, multiplying variance by 2.89. A largest-mode value $\lambda=0.96$ becomes $\gamma=0.944$, multiplying variance by about 0.891. This is a substantial change in the relative pricing of low- and high-variance directions, even when many individual covariance entries change less conspicuously.

The rationale for $a>1$ is that real returns violate the stationary Gaussian model and have stronger optimized-risk bias than the Monte Carlo predicts. This is an empirical explanation, not a theorem proving that nonstationarity or heavy tails always call for precisely this adjustment. The authors do not report a distinct training sample for selecting the amplification and a later untouched sample for evaluating it.

Figure 3 confirms that the adjusted eigenfactor and optimized-portfolio biases lie near one. Random portfolio biases remain near one. Individual stock forecasts acquire a mild systematic tilt: low-volatility stocks have bias statistics around 0.9, while high-volatility stocks reach roughly 1.1. Thus the method improves calibration in optimizer-selected directions while sacrificing some stock-level calibration.

The mechanism is visible through squared projections of individual stocks onto the eigenbasis. Each coordinate vector has projection weights summing to one. A low-volatility stock tends to load more on small-eigenvalue modes whose variances are increased; a high-volatility stock loads more on modes whose variances are reduced. Figure 4 illustrates this for Chevron and Citigroup at the end of the sample. It would therefore be incorrect to judge the method only by whether the original single-stock diagonal remains unchanged: deliberately changing that diagonal is part of the reported result.

## Realized risk reduction, not merely more conservative forecasts

A risk adjustment could make reported risk larger without improving realized portfolios. The report separately reoptimizes using $\widetilde V_0$ and measures out-of-sample realized volatility.

For fully invested global minimum-variance portfolios, reported annualized volatility falls from 14.64% with the sample covariance to 13.98% with the eigen-adjusted covariance. The capitalization-weighted market's volatility is 19.84%. The optimizer improvement is 0.66 percentage points annually, or about 4.5% relative to the original portfolio's volatility.

For the 100 portfolios constrained to modeled alpha one, the mean adjusted-to-original realized-volatility ratio is 0.936: a 6.4% reduction. Figure 5 shows improvements across the simulated alpha portfolios. Holding the modeled numerator fixed would correspond to an information-ratio improvement of approximately $1/0.936-1=6.8\%$, an algebraic implication. It is not a measured increase in realized alpha or net investment returns.

Table 1 varies the estimation length while holding the 50-stock universe fixed. All entries use the common 3,797-day evaluation window July 3, 1995–July 30, 2010, so changing $T$ does not change the evaluation dates:

| Estimation days | Sample $B$ | Adjusted $B$ | Sample realized volatility | Adjusted realized volatility |
|---:|---:|---:|---:|---:|
| 60 | 7.78 | 0.89 | 8.04 | 3.86 |
| 100 | 2.25 | 0.97 | 4.57 | 3.66 |
| 200 | 1.45 | 1.02 | 3.77 | 3.53 |
| 300 | 1.30 | 1.03 | 3.60 | 3.48 |
| 400 | 1.23 | 1.04 | 3.53 | 3.46 |
| 500 | 1.20 | 1.05 | 3.51 | 3.45 |

The volatility columns reproduce the source's numerical scale for unit-alpha portfolios; the table itself does not label a percent sign or state an annualization convention. They should not be confused with the explicitly annualized fully invested portfolio figures above. Ratios within each row are unambiguous. At 60 days, the adjustment lowers realized volatility by approximately 52%; at 500 days, the reduction is about 1.7%.

Near the dimension-to-sample-size boundary, inversion makes the unadjusted optimizer extremely unstable. Lengthening the sample improves it substantially. The adjusted method is much less sensitive to $T$, but its bias rises from modest overprediction at $T=60$ to modest underprediction at $T=500$. More observations also span a longer history and potentially more regime change, so this is not a controlled experiment varying only Gaussian sampling noise.

## Reproduction boundaries and practical interpretation

A faithful implementation needs the original stock identities, capitalization histories and return adjustments, daily window alignment, market-coordinate construction, and synthetic alpha draws. The report provides the selection rule and sample dates but not a machine-readable panel or all data-cleaning choices. It does not specify trading costs, turnover limits, financing costs, position limits, or a long-only restriction for the random-alpha optimizations. Those omissions matter because unconstrained inverse-covariance portfolios can be difficult to trade even when their statistical risk improves.

The study compares sample and adjusted covariances; it is not a comprehensive comparison with shrinkage estimators, covariance factor models, robust optimizers, or modern nonlinear spectral shrinkage. It also does not establish that a parameter calibrated on this selected universe generalizes to a wider contemporary market. The bootstrap treats the fitted covariance as truth, so it estimates selection effects conditional on an imperfect model rather than identifying the true population covariance.

For implementation, the most informative validation is therefore threefold: check risk calibration for fixed portfolios, check it for portfolios selected using the model, and check the realized risk of reoptimized holdings. These answer different questions. The report's contribution is to make the second question explicit and show that a correction targeted at it can also improve the third. Its evidence supports an optimization-aware risk diagnostic and a useful covariance adjustment, subject to the universe, calibration, and execution limitations just identified.
