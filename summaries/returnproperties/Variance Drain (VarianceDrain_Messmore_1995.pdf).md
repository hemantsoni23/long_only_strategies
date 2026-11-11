# Variance Drain

**Tom Messmore.** *The Journal of Portfolio Management* 21(4), Summer 1995, pp. 104–110. Source: [VarianceDrain_Messmore_1995.pdf](../../Finance/VarianceDrain_Messmore_1995.pdf). All seven PDF pages, including both appendices, were inspected. Printed page numbers below are 104–110; PDF page numbers are 1–7.

## Why this matters

A portfolio's average one-period return does not generally equal the constant return that reproduces its accumulated wealth. Messmore calls the difference “variance drain” and argues that its magnitude deserves attention comparable to fees, transaction costs, and manager selection. A strategy that preserves arithmetic return while lowering variability may deliver more compound wealth even without producing conventional one-period alpha.

The article's contribution is an accessible derivation and practical calibration of the approximation $C\approx R-\sigma^2/2$, together with proposed portfolio-management applications. It is not a new general theorem that growth depends only on mean and variance. Nor does it present a tested volatility-control trading strategy. Its evidence consists of an illustrative parameter table, one 100-observation simulation, and a comparison with published stock-market summary statistics. The appendices require care: changing to log-return notation does not make the economic effect of volatility disappear, and a growth approximation does not establish a universal investor utility function.

## Exact accounting before approximation

Let $r_i$ be the simple total return over equal-length period $i$, written as a decimal, and let $N$ be the number of periods. For example, 5% means $0.05$. Assume $1+r_i>0$ when using logarithms. Define the arithmetic return, descriptive variance, and compound return as

$$
R=\frac1N\sum_{i=1}^N r_i,
\qquad
\sigma^2=\frac1N\sum_{i=1}^N(r_i-R)^2,
$$

$$
1+C=\left[\prod_{i=1}^N(1+r_i)\right]^{1/N}.
$$

These are Equations (1)–(4), printed pp. 104–105. The divisor in the variance is $N$, not $N-1$: the immediate problem is describing this realized sequence, not producing an unbiased estimate of an unknown population variance. An implementation using a statistics package's sample-standard-deviation default must change that default or explicitly convert it.

With reinvestment and no external cash flows, terminal wealth is $W_N=W_0(1+C)^N$. The geometric mean concerns gross returns $1+r_i$; multiplying the net returns $r_i$ is incorrect. If external cash flows exist, first obtain a suitable time-weighted return series. Messmore does not specify a cash-flow-adjustment estimator, tax convention, or treatment of fees in the reported market data.

An exact and numerically convenient identity is

$$
\log(1+C)=\frac1N\sum_{i=1}^N\log(1+r_i).
$$

Use a stable `log1p` implementation for the right side and `expm1` for its inverse. For strictly positive gross returns, the arithmetic–geometric mean inequality gives $C\le R$, with equality exactly when every return is equal. This result needs no normality, independence, stationarity, or large sample. Reordering the same realized returns does not change either mean, although it can change interim drawdowns and the outcome for an investor making withdrawals.

The source illustrates constant 5% returns over three years, which have $R=C=5\%$. For returns of 5%, 15%, and −5%, it obtains $R=5\%$ and

$$
C=(1.05\times1.15\times0.95)^{1/3}-1
  =0.04681575\ldots.
$$

The realized gap is therefore approximately 31.84 basis points per year. It is an accounting difference between two return measures, not a fee charged to the account. The realized history does not itself identify a feasible alternative portfolio earning a constant 5%.

## Derivation of the half-variance approximation

Expanding the variance gives the exact identity

$$
\frac1N\sum_i r_i^2=R^2+\sigma^2.
$$

Messmore then truncates $\log(1+x)=x-x^2/2+x^3/3-\cdots$ after the quadratic term. Substituting on both sides of the log-wealth identity gives

$$
C-\frac{C^2}{2}
\approx R-\frac{R^2+\sigma^2}{2},
$$

or

$$
C\approx R-\frac{\sigma^2}{2}
       +\frac{C^2-R^2}{2}.
$$

Dropping the final squared-mean difference produces the main formula, Equation (16), printed p. 106:

$$
C\approx R-\frac{\sigma^2}{2}.
$$

There are two approximations here: truncating logarithms and neglecting a remaining term involving both means. Neither operation becomes exact merely because the variance has been measured precisely. The Taylor series used by the source has radius one around zero; simple returns near −100% are especially problematic because their logarithms become very negative. A return greater than 100% is also outside the stated series range. Descriptive mean and variance can remain finite while the log-growth loss is arbitrarily large near ruin.

For the three-year example, the population-form variance is $0.00666667$. The formula predicts $C=4.66667\%$, approximately 1.49 basis points **below** the exact value. This direct calculation is useful because the article also claims that the approximation is always slightly upward-biased. That universal statement is not supported. Even the sign of $C^2-R^2$ cannot be inferred from $C\le R$ without further restrictions on their signs, and the omitted higher-order log terms introduce additional error.

The symmetric two-period example on printed p. 106 has returns $+5\%$ and $-5\%$. Its exact compound return is $\sqrt{0.9975}-1=-0.00125078$, or **−0.125078%**. The source's displayed −0.0013% is a decimal-to-percent error. The half-variance approximation gives −0.125%, correctly close but slightly above the exact result in this particular case.

For an additional diagnostic, derived here rather than reported in the article, expand around $R$ instead of zero. Put $\epsilon_i=r_i-R$. When deviations are small compared with $1+R$,

$$
\frac1N\sum_i\log(1+r_i)
\approx\log(1+R)-\frac{\sigma^2}{2(1+R)^2},
$$

and consequently

$$
R-C\approx\frac{\sigma^2}{2(1+R)}.
$$

This retains the mean-dependent curvature ignored by the half-variance rule. It predicts 4.68254% for the three-year example, but it is still a local approximation, not a universally superior estimator. Higher centered moments matter when deviations are not small. Both formulas should be checked against the exact geometric return whenever the actual return sequence is available.

## Parameter experiment and its economic scale

Exhibit 1, printed p. 107, constructs hypothetical annual means from 2% to 20% in two-percentage-point steps and sets $R/\sigma=0.75$. This is a mean-to-volatility ratio, not an excess-return Sharpe ratio: no risk-free rate is subtracted. For each row, calculate $\sigma=R/0.75$, variance, half-variance, estimated compound return, and the drain divided by $R$.

| Assumed annual arithmetic return | Assumed annual volatility | Half-variance drain, percentage points | Estimated compound return | Drain as percent of arithmetic return |
|---|---:|---:|---:|---:|
| 2% | 2.67% | 0.0356 | 1.9644% | 1.78% |
| 6% | 8.00% | 0.3200 | 5.6800% | 5.33% |
| 10% | 13.33% | 0.8889 | 9.1111% | 8.89% |
| 12% | 16.00% | 1.2800 | 10.7200% | 10.67% |
| 16% | 21.33% | 2.2756 | 13.7244% | 14.22% |
| 20% | 26.67% | 3.5556 | 16.4444% | 17.78% |

These selected rows are reconstructed from the table's generating rule; slight last-digit differences reflect rounding. The labels bills, bonds, and stocks are loose illustrations, not estimated asset-class parameters. The paper explicitly acknowledges that some low-return rows have implausibly high volatility for those labels. It offers no cross-sectional test of a constant 0.75 ratio.

The scaling is the practical message. At 8% volatility, the approximation gives a 32-basis-point annual gap; at 16%, 128 basis points; at 18%, 162 basis points. The paper compares the resulting amounts with institutional management fees and active-manager outperformance. Its illustration that a gap exceeding 1% on \$100 million corresponds to more than \$1 million is an annual-rate comparison. It should not be interpreted as cash that can be recovered without changing exposures, expected returns, costs, or constraints.

## Simulation design and reported outcome

Exhibit 2 uses **100 simulated annual returns** from a normal distribution with mean 12% and standard deviation 16%. It reports a single sample's descriptive statistics and geometric return. There is no reported random seed, generator, code, path vector, repeated-simulation count, confidence interval, or formal goodness-of-fit test. Independence is natural for reconstructing the stated random-normal experiment, but the article does not document a serial-dependence implementation.

The target moments imply a half-variance prediction of $0.12-0.16^2/2=10.72\%$. The realized sample has mean 11.66% and standard deviation 16.39%. Its predicted compound return is

$$
0.1166-\frac{0.1639^2}{2}=0.103168395,
$$

or 10.3168%, shown as 10.32% in the source. The actual geometric return is 10.40%. Thus the approximation error for this sample is about −8 basis points. The predicted sample drain is 1.34 percentage points, compared with the actual $11.66-10.40=1.26$ percentage points. Comparing 10.40% with the population-moment prediction 10.72% mixes sampling error with approximation error; comparing it with 10.32% better isolates the latter for this realized sample.

A faithful methodological reconstruction would draw 100 returns, compute all three statistics using the definitions above, and report both discrepancies. It cannot recover the published sample without its seed or observations. Normal simple returns assign positive probability to returns below −100%; the source specifies no truncation or rejection rule. The probability is very small at these parameters, but the model is not a globally valid limited-liability wealth process. An implementation must disclose its handling rather than silently replacing the distribution.

For a stronger validation beyond the paper, one could repeat the experiment and report the distribution of approximation errors, using heavy-tailed or negatively skewed alternatives as sensitivity tests. Those would be new experiments, not evidence supplied by Messmore. His one-path exercise supports a numerical illustration, not a general statistical accuracy claim across financial return distributions.

## Historical comparison

Printed p. 108 cites Ibbotson Associates' 1995 yearbook and describes large-company stock returns for **1929–1994**. Preserve that stated range when identifying the local article; the underlying annual data are not supplied here. The reported arithmetic mean is 12.2%, volatility 20.3%, and geometric mean 10.2%. The approximation yields

$$
0.122-\frac{0.203^2}{2}=0.1013955,
$$

or 10.1396%, about six basis points below the rounded reported geometric mean. This is the article's main historical check. It does not report standard errors, alternative sample periods, rebalanced portfolio rules, exclusions, or a transaction-cost model. Reproducing the original series would require the cited yearbook and confirmation of its dates and return conventions. The precision of the printed moments also limits the meaning of a difference of a few basis points.

## Portfolio objective and practical proposals

Appendix B proposes using growth as an interpretable objective. With expected return $R$, variance $\sigma^2$, and a return-equivalent aggregate cost term $AOC$, its basic prescription is to maximize approximately

$$
R-\frac12\sigma^2-AOC.
$$

It then introduces an investor-specific multiplier $k$:

$$
R-\frac{k}{2}\sigma^2-AOC.
$$

The source suggests varying $k$ around one and tracing an efficient frontier, for example from 0.50 to 1.50 in increments of 0.05 or 0.10. Relative to the conventional objective $R-\lambda_3\sigma^2-AOC$, the parameters satisfy $k=2\lambda_3$. Raising $k$ from 1 to 1.10 increases the variance penalty by 10%; it does not by itself imply that an independently defined economic risk-aversion measure has increased by exactly that amount.

For portfolio weights $w$, a conventional implementation of the proposed approximation would use $R(w)=w^\top\mu$, $\sigma^2(w)=w^\top\Sigma w$, explicit feasible-set constraints, and a cost function in compatible return units. The source does not estimate $\mu$ or $\Sigma$, solve a concrete portfolio, specify leverage/shorting bounds, or test resulting allocations. Its suggestion to encode hard constraints through prohibitively high penalties is a modeling convention, not a demonstration that a finite penalty enforces them exactly. Explicit constraints are necessary when violation must be impossible.

The operational suggestions on p. 108 aim to avoid unintended risk: control concentration, preserve intended asset and sector exposures, manage cash-flow disturbances, use derivatives where appropriate to maintain exposure, and diversify deliberately. None receives an independent backtest. The causal condition is essential: reducing variance improves this approximation **holding the arithmetic mean and relevant costs fixed**. If the return sacrifice exceeds the reduction in half-variance, estimated compound growth falls.

## Continuous compounding and the limits of the argument

Appendix A defines a continuously compounded rate $\ell_i$ by $e^{t\ell_i}=V_i/V_{i-1}$ for equal subperiod duration $t$. Defining an overall continuous rate $g$ by $e^{Nt g}=V_N/V_0$ gives exactly $g=N^{-1}\sum_i\ell_i$. This is simply additivity of log returns. The appendix calls the equality evidence that variance drain vanishes in the continuous-compounding limit. That interpretation conflates a change of return coordinates with removal of economic variability.

For clarity, a separate standard calculation gives the counterpoint. If wealth satisfies $dW_t/W_t=\mu\,dt+\sigma\,dB_t$, then Itô's formula gives $d\log W_t=(\mu-\sigma^2/2)dt+\sigma dB_t$. Arithmetic drift and expected log-growth drift still differ by half the instantaneous variance rate. This continuous-time example is an explanatory check, not a model estimated by Messmore. Measuring the same wealth process more frequently does not eliminate its diffusion penalty.

A reproducing researcher should therefore keep three quantities distinct: realized arithmetic simple returns, realized geometric simple returns, and average continuously compounded returns. Annualize them using their own definitions. A monthly half-variance number is a per-month approximation; inserting annual volatility and monthly mean in the same formula is inconsistent. The practical value of the paper is its reminder to account for compounding, while its broad claims about bias direction, disappearance under continuous compounding, and universally appropriate growth preferences require the qualifications above.
