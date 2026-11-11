# The alpha factor asset pricing model: A parable

Wayne E. Ferson, Sergei Sarkissian, and Timothy Simin. *Journal of Financial Markets* 2 (1999), 49–68. Source: [AlphaFactorAssetPricing_FersonSarkissianSiImin_1999.pdf](../../Finance/AlphaFactorAssetPricing_FersonSarkissianSiImin_1999.pdf), 20 pages including both appendices. Printed page numbers are used below; subtract 48 to obtain the PDF page. The alphabet anomaly is deliberately manufactured. This is a calibrated counterexample to an identification argument, not evidence that firms with particular names actually earn abnormal returns.

## Why this matters

A characteristic predicts returns. A researcher sorts stocks on that characteristic, constructs a long–short portfolio, estimates stock exposures to that portfolio, and finds that those exposures explain the characteristic's return premium. It is tempting to conclude that the characteristic was a proxy for economic risk. The paper demonstrates that the same sequence can succeed when the characteristic is unrelated to systematic risk by construction. The portfolio can repackage the original anomaly without explaining its economic origin.

The contribution is narrower and more useful than claiming that characteristic portfolios are invalid. They are legitimate return portfolios and may be good forecasting instruments or hedges. What fails is the inference from successful beta pricing to a risk-based account of the premium. A model can appear to pass the familiar tests—significant factor loadings, small time-series intercepts, and an insignificant characteristic after controlling for its factor beta—because the factor has inherited the characteristic's cross-sectional pattern. Establishing economic risk requires additional restrictions or evidence about the underlying shocks and their prices.

The counterexample also explains a seeming paradox: a market factor can be necessary for zero time-series intercepts even when cross-sectional variation in market beta explains none of the expected-return differences. Its job can be to absorb the common mean return. This distinguishes fitting return levels from explaining differences across assets.

## The mechanism in its simplest form

Let $R_t$ be an $N$-vector of returns and $d$ a fixed characteristic vector centered so that $d'\mathbf1=0$. A monthly cross-sectional OLS regression on an intercept and $d$ produces the slope portfolio

$$
f_t=(d'd)^{-1}d'R_t=w'R_t,\qquad w=d/(d'd).
$$

The weights sum to zero and have unit exposure to $d$. Suppose the researcher next regresses each asset's time-series return on $f_t$. The resulting loadings are proportional, across assets, to $\operatorname{Cov}(R_t,f_t)=\operatorname{Var}(R_t)d/(d'd)$. If $d$ is an eigenvector of the return covariance matrix, these loadings line up with $d$ and therefore with the expected returns that motivated the sort. A completely transparent case is $\operatorname{Var}(R_t)=\sigma^2 I$: then the beta vector is exactly $d$. There is no common risk in that example, but the characteristic factor appears to price the assets perfectly.

This argument is about the same assets appearing in both the test cross section and the constructed factor. Idiosyncratic return covariance with a portfolio containing the asset is enough to manufacture the desired loading pattern. It is not necessary for the factor to be an externally specified economic shock. Adding a predictable, common time-varying anomaly strengthens the unconditional covariance channel while leaving conditional unexpected-return risk unchanged.

A simple spread portfolio approximates the slope portfolio's role. Both are long high-characteristic assets, short low-characteristic assets, and have zero net investment. The exact OLS weights minimize squared weights under their linear constraints; a general minimum-variance interpretation requires the corresponding covariance assumptions or a GLS construction. The paper's broad discussion of regression portfolios should not be read as saying arbitrary OLS portfolios minimize variance under every return covariance matrix. The spread implementation avoids estimating a full covariance matrix but generally is not identical to the slope portfolio.

## A reconstructible version of the experiment

The numerical example uses $T=377$ monthly observations, August 1963 through December 1994, and $N=100$ portfolios. Start with NYSE and AMEX firms in CRSP. Each month sort firms using the first two letters of their names. Special symbols precede numbers, and numbers precede letters. Divide the sorted list into 100 equal-count groups; if the number of firms is not divisible by 100, remove the extra firms at the end of the alphabet for that month. Compute equally weighted returns within each group and subtract the Ibbotson Associates one-month Treasury-bill return. Constituents are allowed to change monthly.

The artificial excess-return vector is equation (1), printed page 53:

$$
r_t=\mu\mathbf1+\delta_0+\Delta'z_{t-1}+\varepsilon_t.
$$

Here $\mu$ is the grand mean of the actual alphabet-portfolio excess returns; $\delta_0$ is a centered $100\times1$ vector of constant anomalous expected returns; $z_{t-1}$ is a demeaned $2\times1$ vector containing the lagged three-month Treasury-bill yield and S&P 500 dividend yield; and $\Delta$ is a $2\times100$ matrix. The error $\varepsilon_t$ is transformed from actual portfolio residuals to impose a chosen conditional covariance structure. Neither $\delta_0$ nor $\Delta$ is intended to represent compensation for risk.

For $\delta_0$, the paper specifies 100 equally spaced entries centered at zero, with the maximum absolute entry equal to half the difference between 1.09% and 0.31% per month, the high- and low-book-to-market returns used for calibration. Thus the stated endpoint scale is 0.39% monthly. The early alphabet receives the positive anomaly. This is a calibration to a familiar economically meaningful spread, not an estimate of a name effect from observed returns.

Construct $\Delta$ by regressing an HML-like return on a constant and the two lagged instruments. For each instrument, make a centered, equally spaced sequence across 100 portfolios whose endpoint difference equals that instrument's HML regression coefficient. Then multiply column $i$ of this preliminary $\Delta$ by the square root of the $i$th entry of an equally spaced sequence from 1 to 55. This deliberate asymmetry makes the simulated return patterns resemble the empirical book-to-market pattern. It means that reproducing the experiment is more involved than imposing a linear, time-invariant characteristic spread.

The calibration HML data were provided by Campbell Harvey. Footnote 4 specifies independent size and book-to-market classifications: size groups use 30%, 40%, and 30% breakpoints; NYSE book-to-market breakpoints also use 30%, 40%, and 30%. The HML return is the average of small/high and big/high minus the average of small/low and big/low. Portfolio returns are value weighted. The timing described uses book equity for June of year $t$, market equity at December of year $t$, size at June $t+1$, and returns from July $t+1$ through June $t+2$. These are the paper's conventions; substituting a current downloaded HML series need not reproduce the original coefficients.

To create the unexpected-return matrix, regress each actual alphabet-portfolio excess-return series on the lagged instruments, producing residual matrix $E$ of dimension $T\times N$. Regress these residuals on the residual from projecting S&P 500 excess returns on the same instruments. The resulting exposures determine a single-index covariance component. The source writes the target covariance as

$$
V_\varepsilon=bb'+\sigma^2I,\qquad \sigma^2=0.0013.
$$

It selects $\sigma^2$ as the median eigenvalue of the difference between the empirical residual covariance and $bb'$. The factor normalization needs care: if $b$ contains regression slopes on an unstandardized market residual, the systematic covariance is $b\operatorname{Var}(u_m)b'$, not simply $bb'$. Equivalently, absorb the market residual's standard deviation into $b$. Appendix A expressly permits this general factor-covariance formulation. The printed operational description does not completely specify that scaling, so it should be documented in a replication rather than silently assumed away.

With $S_E$ the covariance of $E$, an explicit row-oriented implementation of the stated whitening and recoloring operation is

$$
\mathcal E=E S_E^{-1/2}V_\varepsilon^{1/2}.
$$

Use symmetric matrix square roots and one consistent sample covariance divisor. Then $\operatorname{Cov}(\mathcal E)=V_\varepsilon$ up to numerical precision. This transformation preserves much of the realized residual time-series information while replacing cross-sectional covariance; it is not an independent Gaussian Monte Carlo draw. No simulation seed is needed for this step. The constructed covariance is intended to make the alphabet characteristic unrelated to systematic exposures. Exact orthogonality should be checked numerically because empirical market betas having no visible trend in alphabet position is weaker than $d'b=0$ exactly.

## Reproducing the three apparent empirical successes

The first stage is a monthly cross-sectional regression of the 100 artificial returns on an intercept and alphabet position $A_i$. The paper describes the position scale as ranging from 0.6 to −0.59 in equal increments. Preserve this stated scale and record the exact implementation; slope coefficients depend on characteristic normalization. Average the 377 monthly coefficients. The reported intercept is 0.009 and the alphabet slope is 0.0033, with Fama–MacBeth $t=4.24$ for the slope. Returns are decimals, so these are 0.9% and 0.33% per month respectively. The latter is per unit of the particular alphabet regressor, not automatically the return on a fully invested long–short portfolio.

The slope time series is the “alpha” factor. Construct a second factor, AMZ, independently of the slope weighting: long an equally weighted average of portfolios 1–40 and short an equally weighted average of portfolios 61–100. Omit portfolios 41–60. Each leg has weight one. AMZ is therefore a transparent 40%-versus-40% characteristic spread, not an extreme-decile strategy.

Next estimate full-sample time-series regressions for each artificial portfolio:

$$
r_{it}=a_i+\beta_{im}r_{mt}+\beta_{if}f_t+u_{it},
$$

where $f_t$ is either the slope series or AMZ. The paper discusses S&P 500 exposures in the construction and reports equally weighted market-return regressions in Table 1; reproducing particular reported columns requires preserving that distinction. Do not replace every market series by one modern benchmark and expect exact agreement. The factor loads positively on early-alphabet portfolios and negatively on late-alphabet portfolios, as desired. For the slope-factor specification, the estimated intercepts run from −0.0019 to 0.0028 monthly, and the largest absolute intercept $t$-statistic is 1.45. These non-rejections are finite-sample results, not proof that every population pricing error is zero.

Finally, the “acid test” places market beta, characteristic-factor beta, and the characteristic into a return cross section. The correlation between the alphabet measure and its estimated alpha beta is 0.984. Instead of estimating the displayed unrestricted multiple regression literally, the authors implement a sequential procedure because of the near-collinearity. In each month first regress returns on a constant, market beta, and alpha beta (or AMZ beta). Regress the first-stage residuals plus its intercept on a constant and the original alphabet variable. Table 2 takes beta prices from the first step and the alphabet coefficient from the second.

This sequencing is essential for reproducing Table 2. It is not ordinary Frisch–Waugh–Lovell estimation of the full joint regression: that would also residualize the alphabet regressor against the beta regressors. The paper's finding is a small residual characteristic pattern after giving the factor betas first access to the shared explanatory variation. The construction and ordering should accompany any interpretation of the characteristic's insignificance.

| Table 2 specification | Mean market-beta coefficient | Mean constructed-factor coefficient | Residual alphabet coefficient | Maximum monthly cross-sectional $R^2$ |
|---|---:|---:|---:|---:|
| Alpha slope factor | −0.0003 ($t=-0.0788$) | 0.0032 ($t=4.0446$) | 0.0001 ($t=1.0651$) | 0.36 |
| AMZ factor | −0.0012 ($t=-0.3635$) | 0.0024 ($t=3.9943$) | 0.0002 ($t=1.5820$) | 0.33 |

The minimum monthly $R^2$ is reported as 0.0 in both cases. These values describe month-by-month realized-return cross sections, not a 36% ceiling on explaining unconditional means. Both constructed factors are apparently priced while the original characteristic becomes insignificant. Yet the experiment was designed without a systematic-risk explanation of that characteristic.

Table 1 further shows the intended separation: representative early- to late-alphabet mean returns decline from 1.08% to 0.72% monthly, while monthly standard deviations stay roughly 5.5–5.9% and market betas remain near one. Alpha loadings span approximately 0.424 to −0.624 in its displayed extreme groups. These are properties of the artificial portfolios and should not be treated as independent empirical evidence about actual stocks' names.

## The general appendix argument, with a necessary algebraic correction

Appendix A writes conditional expected excess returns as

$$
E_t[r_{t+1}]=\mu\mathbf1+\Theta C_t,
\qquad r_{t+1}=E_t[r_{t+1}]+\varepsilon_{t+1}.
$$

$\Theta$ is a centered $N\times K$ matrix of fixed characteristics, $C_t$ is a $K$-vector known at time $t$, and $V_\varepsilon=BB'+D$. The definition of characteristics unrelated to risk is $\Theta'B=0$. In a large-market setting the residual covariance $D$ must be sufficiently well behaved, for example with bounded eigenvalues, for diversified residual risk to vanish. These are substantive assumptions; orthogonality to one observed market proxy alone does not establish orthogonality to every possible economic risk.

Define $W=(\Theta'\Theta)^{-1}\Theta'$. The cross-sectional coefficient portfolio is

$$
\widehat C_t=Wr_{t+1}=C_t+W\varepsilon_{t+1},
$$

because $W\mathbf1=0$ and $W\Theta=I_K$. With conditional mean-zero disturbances, its unconditional covariance is

$$
\operatorname{Var}(\widehat C_t)=V_C+W V_\varepsilon W',\qquad V_C=\operatorname{Var}(C_t).
$$

The two components are economically different. $V_C$ is predictable time variation in the anomaly and is not new uncertainty conditional on information at $t$. $W V_\varepsilon W'$ is sampling or residual-return variation. An unconditional regression sees both. Thus a volatile traded portfolio is not, merely by being volatile, proof of exposure to priced conditional uncertainty.

For an intercept-containing time-series regression of returns on these factor portfolios, the population slope matrix, oriented $K\times N$, is

$$
\beta=[V_C+WV_\varepsilon W']^{-1}[V_C\Theta'+WV_\varepsilon].
$$

**Source correction:** printed equation (A.7), page 66, omits $V_C$ from the first inverse bracket although (A.6) identifies that bracket as the inverse covariance of the coefficient portfolio. The formula above follows from (A.1)–(A.6) under the paper's own orthogonality assumptions. The omission does not overturn the qualitative column-space argument, but it changes slope normalization and should not be carried into code.

In the spherical residual case $D=\sigma^2 I$, orthogonality $\Theta'B=0$ implies

$$
WV_\varepsilon=\sigma^2(\Theta'\Theta)^{-1}\Theta',
\qquad WV_\varepsilon W'=\sigma^2(\Theta'\Theta)^{-1}.
$$

Substituting yields $\beta=\Theta'$ exactly, provided the relevant covariance is invertible. This is the strongest demonstration: the betas reproduce the original characteristic directions even if $C_t$ is constant. In more general residual covariance structures the equality need not hold. The numerical AMZ factor is also not exactly the OLS factor, particularly for the middle 20 portfolios it excludes, so exact population pricing is not asserted for that finite-sample implementation.

As $N$ grows, if the coefficient portfolios consistently estimate $C_t$ and residual risk vanishes, a known nonzero characteristic premium creates a large-market arbitrage opportunity after orienting the position appropriately. Under no-arbitrage conditions the anomalous premium must instead disappear. This asymptotic argument does not claim a finite collection of 100 portfolios can deliver a riskless, costless trading profit. Sampling risk and transaction costs remain in the finite example.

## Source limitations that matter for replication

Several printed details prevent an exact numerical replication from the article alone. The original portfolio panels, full loading vectors, two HML predictive slopes, and grand mean are not tabulated. Historical CRSP name handling, ties among two-letter names, and vendor revisions can change alphabet membership. A complete reproduction needs these input files or an explicitly documented reconstruction. The paper reports one calibrated illustration, not a repeated-simulation rejection-frequency study; there is no reported distribution across random seeds or a held-out validation period.

There are also source inconsistencies that should be preserved as warnings rather than converted into invented inputs. Page 56 reports $R^2=0.52$ from regressing the alpha factor on the lagged instruments and then claims $1-(0.0036/0.015)^2=0.51$. The displayed arithmetic is incorrect: its left side is 0.9424. Moreover, $\sigma/10$ is an equal-weight approximation, whereas a slope portfolio's residual variance is $\sigma^2 w'w$ and a 40–40 spread has different gross exposure. The observed regression $R^2$ and the printed approximation cannot jointly validate the variance decomposition numerically. Recompute the decomposition from actual weights.

Footnote 5 motivates the median-eigenvalue choice by making a determinant zero. That is not a general theorem that the median eigenvalue minimizes a standard matrix-norm distance between covariance matrices. Use it as the authors' specified calibration rule, not as a uniquely optimal covariance estimator. Similarly, the relation between the stated $\delta_0$ endpoints and the displayed Table 1 mean spread merits a reconstruction check; the provided tables alone do not supply all underlying calibration values.

Appendix B identifies meaningful sensitivities. Removing the common mean or the market factor makes time-series intercepts significant. Changing $\delta_0$ and $\Delta$ can alter the factor-beta pattern, which was intentionally calibrated to resemble book-to-market portfolios. Alpha-beta explanatory power is relatively stable across these variations, whereas AMZ is more sensitive to time-varying anomalies because it excludes the middle portfolios. If the characteristic is correlated with systematic risk in the covariance construction, the constructed betas can remain priced but cease to absorb the original anomaly completely.

## Interpreting the result without overclaiming

There are two economic readings. If the artificial process is the true process, an anomaly genuinely exists and a characteristic factor disguises rather than explains it. If the observed pattern arose through data mining in a no-arbitrage world, the artificial process can describe the selected in-sample realization; using that same sample to discover the characteristic, build the factor, and test its betas recycles the selection. A fresh sample may then eliminate the apparent premium. Splitting a previously searched sample does not automatically create independent evidence because the discovery already used both halves.

The authors explicitly do not establish that Fama–French factors are spurious. Real characteristics may combine risk exposure and anomalous expected returns, and their net effect is model dependent. The useful lesson for an implementer is to separate three outputs: return prediction, covariance representation, and an economic explanation of expected returns. The parable can generate the first two without the third. A credible extension would test pre-specified characteristics against independently motivated conditional shocks, document information timing and out-of-sample construction, and distinguish systematic uncertainty from predictable variation in expected returns. Those are implications of the identification failure, not additional tests performed in this paper.
