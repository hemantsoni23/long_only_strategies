# Predicting stock returns

**Doron Avramov and Tarun Chordia (2006).** *Journal of Financial Economics* 82, 387–415. DOI: 10.1016/j.jfineco.2005.07.014. Source: [AssetPrediction_Avramov_2006.pdf](../../Finance/AssetPrediction_Avramov_2006.pdf). The complete 29-page article was read, including both mathematical appendices, all five tables, Figure 1, and references. Printed page $p$ is PDF page $p-386$. This is distinct from the authors' 2006 *Review of Financial Studies* paper, “Asset Pricing Models and Financial Market Anomalies.”

## Why the stock-level problem changes the question

Failure to forecast the aggregate equity premium does not imply that macroeconomic information is useless for choosing individual stocks. Business conditions may forecast a stock's alpha, its exposure to the market, the market premium, or several of these simultaneously. Avramov and Chordia separate those channels and judge their value through recursively estimated portfolios rather than only through predictive-regression $R^2$.

Their main result is that conditioning stock-level alpha on four macro variables remains useful after the sample in which those variables became prominent predictors of the market premium. Time variation in the market premium itself is much less convincing after 1987. This is evidence about an estimated conditional return system and its portfolio consequences. Calling its intercept “mispricing” does not establish a behavioral interpretation: alpha is relative to the imposed factor model and can include omitted risk compensation.

The implementation contribution is a factor-based covariance structure that accommodates unequal stock histories and integrates estimation risk into one-step predictive moments. With roughly a thousand eligible stocks at a time, estimating an unrestricted return covariance matrix from fewer than five hundred observations is impractical. The authors fit each stock against common factors and instruments, retain diagonal residual covariance, and estimate the factor process using its longer history. This produces tractable portfolio inputs and provides explicit nested experiments for alpha, beta, and premium variation.

The reported returns are large, but the strategy usually invests about 200% of wealth in equities. Its strongest headline alphas also weaken under a conditional four-factor benchmark, and some prose significance claims are inconsistent with the accompanying standard errors. A faithful implementation must retain these qualifications alongside the economic finding.

## Data, eligibility, and decision timing

The underlying monthly sample runs from July 1962 through December 2003, with 497 usable lagged observations in the recursive formulation. The stock universe comprises NYSE- and AMEX-listed common stocks. At a decision date, a security must have a current return and the preceding sixty monthly returns in CRSP, sufficient market-capitalization and trading-volume data, and sufficient COMPUSTAT accounting information to compute book-to-market using the previous December's accounts. The smallest capitalization quartile is excluded. This yields 3,123 distinct stocks, with an average of 973 and median of 988 eligible stocks per month.

Accounting values from the end of year $y-1$ are applied from July of year $y$ through June of $y+1$, following the cited Fama–French convention. Table 1 says size and turnover must be available as of month $t-2$, while its current-return wording and the prose use investment-date language. These should be reconciled into an explicit formation/holding calendar. The paper's coherent payoff convention is that weights determined at $t-1$ multiply returns at $t$; it would be incorrect to condition eligibility on an unknown next-month return merely because a table calls it the “investment month.”

Characteristics are market capitalization in billions of dollars, book-to-market, monthly turnover as shares traded divided by shares outstanding, and cumulative return over the preceding twelve months. They describe and evaluate portfolios; they are not directly included as stock-level predictors in the main optimization. Table 1 reports mean excess return .69% per month, mean size \$2.96 billion, median size \$0.72 billion, mean book-to-market 1.25, mean turnover 5.28%, and mean prior-year return 12.88%. The average within-month cross-sectional standard deviation of excess returns is 8.91%, a different object from the time-series volatility of an optimized portfolio.

The four aggregate instruments are:

| Instrument | Definition | Reported sample mean |
|---|---|---:|
| Dividend yield | Dividends paid on the value-weighted CRSP index over twelve months divided by its current level | 2.84% |
| Default spread | Moody's Baa yield minus Aaa yield | 1.01% |
| Term spread | Treasury yield beyond ten years minus three-month bill yield | .83% |
| Treasury-bill yield | Three-month bill yield | 5.90% |

These are conditioning variables known at the preceding date in the model. Exact release timestamps, revised-data conventions, and the chosen long-Treasury series are not supplied as executable data definitions. In particular, a yield quoted annually is not automatically the monthly risk-free investment return used in portfolio arithmetic.

The initial training window contains 120 observations. Estimation then expands by one observation each month. First formation is July 1972 and first realized return August 1972; final formation is November 2003 and final realized return December 2003. This produces 377 realized returns. Some prose describes the formation-date span as an “investment period,” so date labels should not be mistaken for a one-month disagreement in the tested payoff series. The pre-discovery comparison is August 1972–December 1987; the later comparison is January 1988–December 2003.

The later period is outside the historical data used in the cited predictor-discovery studies. It is still an ex post research design: the four-variable choice and model families were not frozen by a live 1987 investment process. The source's phrase “purely out-of-sample” should be understood as its chronological estimation/discovery split, not evidence of an untouched contemporary validation sample.

## Conditional return model and nested restrictions

Let $r_{t+1}$ contain the $N_t$ investable stocks' excess simple returns, $f_{t+1}$ contain $K$ traded-factor excess returns, and $z_t$ contain $M$ macro instruments. The structural specification is

$$
r_{t+1}=\alpha(z_t)+\beta(z_t)f_{t+1}+v_{t+1},
$$

$$
\alpha(z_t)=\alpha_0+\alpha_1z_t,\qquad
\beta(z_t)=\beta_0+\beta_1(I_K\otimes z_t),
$$

$$
f_{t+1}=a_f+A_fz_t+v_{f,t+1},\qquad
z_{t+1}=a_z+A_zz_t+v_{z,t+1}.
$$

The stock regression can be estimated linearly in coefficients by including $1$, $z_t$, $f_{t+1}$, and $f_{t+1}\otimes z_t$. This does not mean realized $f_{t+1}$ is known when allocating: it is integrated using the separately fitted factor forecast. The model has $q=1+M+K+KM$ coefficients per stock in its unrestricted form. Here the main portfolio construction uses $K=1$, the market excess return, and $M=4$, giving ten stock-regression coefficients.

Stock-specific shocks have covariance $C$, assumed diagonal, and are orthogonal to factor innovations. Factor innovations have covariance $\Sigma_{ff}$. Both stock and factor innovations may covary with predictor innovations. Conditional on parameters,

$$
\mu_t=\alpha(z_t)+\beta(z_t)(a_f+A_fz_t),\qquad
S_t=\beta(z_t)\Sigma_{ff}\beta(z_t)'+C.
$$

When both beta and the factor premium vary, the conditional mean is quadratic in instruments despite the linear coefficient regressions. The covariance is also quadratic in instruments through beta. A simple linear stock-return forecasting regression generally does not reproduce this system.

The tested strategy families are IID, with all three variation channels suppressed; TV-beta, allowing only $\beta_1$; TV-RP, allowing only $A_f$; TV-alpha, allowing only $\alpha_1$; and TV-All, allowing all three. A separate MKT strategy allocates between cash and the market index using the four instruments. Most stock strategies are estimated both with unrestricted pricing intercepts, UN, and with CAPM restrictions $\alpha_0=\alpha_1=0$, RE. TV-alpha has no corresponding restricted-alpha version. A constant unrestricted alpha is retained in the UN cases even when alpha *variation* is disabled.

Diagonal $C$ is a substantial regularization assumption. It makes estimation possible, but it also excludes residual industry and other stock-to-stock dependence. Out-of-sample evaluation is valuable evidence about the resulting portfolio rule; it does not prove that the diagonal assumption is innocuous or that a better residual-risk model would leave allocation and inference unchanged.

## Estimation with unequal histories and parameter risk

For stock $i$, retain only its $T_i$ usable observations, with response $r_i$ and design $G_i$. Estimate

$$
\widehat\Gamma_i=(G_i'G_i)^{-1}G_i'r_i,\qquad
\widehat c_i=\frac{(r_i-G_i\widehat\Gamma_i)'(r_i-G_i\widehat\Gamma_i)}{T_i}.
$$

For the factor process, let $X$ contain rows $x_t'=(1,z_t')$ over the longer factor/predictor history and $F$ the corresponding next-period factor realizations. Then $\widehat A_F=(X'X)^{-1}X'F$, where $A_F$ stacks factor intercept and slope coefficients, and $\widehat\Sigma_{ff}$ is the factor residual sum-of-products divided by $T$. Stock loadings and residual variances use each stock's history; factor dynamics use all available factor observations. IPOs need not be backfilled with artificial stock returns.

The source assumes Gaussian iid innovations and noninformative parameter priors. Its posterior predictive mean equals the fitted conditional mean, but its predictive covariance is enlarged to reflect uncertainty in coefficients and innovation variances. Appendix A gives

$$
\widetilde\Sigma_{ff}=\frac{T}{T-M-2K-3}\widehat\Sigma_{ff},\qquad
\widetilde c_i=\frac{T_i}{T_i-M-K-KM-3}\widehat c_i,
$$

$$
d_T=\frac{1+(\bar z-z_T)'\widehat V_z^{-1}(\bar z-z_T)}{T},\qquad
V_{f,T}=(1+d_T)\widetilde\Sigma_{ff}.
$$

These degrees-of-freedom corrections are the source's stated predictive formulas, not maximum-likelihood variance estimates. Positive denominators and nonsingular regressor cross-products are necessary. The minimum history substantially exceeds the unrestricted ten-column design dimension, but collinearity still needs an explicit numerical check.

A compact equivalent of Appendix A's partitioned equations (23)–(26) makes the stock-level coefficient-risk adjustment easier to implement. Let $\Omega_i=(G_i'G_i)^{-1}$, $\mu_{f,T}=\widehat A_F'x_T$, and write the next stock-regression row as

$$
g_T(f)=g_{0,T}+L_Tf,
\qquad
g_{0,T}=\begin{pmatrix}x_T\\0_K\\0_{KM}\end{pmatrix},\qquad
L_T=\begin{pmatrix}0_{(M+1)\times K}\\I_K\\I_K\otimes z_T\end{pmatrix}.
$$

Its expected value is $\bar g_T=g_{0,T}+L_T\mu_{f,T}$. Therefore the adjustment in the source is equivalently

$$
d_{iT}=\bar g_T'\Omega_i\bar g_T+
\operatorname{tr}(\Omega_iL_TV_{f,T}L_T').
$$

This is a derived rearrangement of the displayed partition formula, preserving its stock-specific design. The final covariance is

$$
S_T=\operatorname{diag}\{\widetilde c_i(1+d_{iT})\}
+\widehat\beta(z_T)V_{f,T}\widehat\beta(z_T)',
$$

and the predictive mean is $\widehat\alpha(z_T)+\widehat\beta(z_T)\mu_{f,T}$. The factor part creates cross-stock covariance; the stock coefficient-risk contribution remains diagonal under the maintained independence structure. Plugging an estimated factor mean into the design without its covariance term would omit part of the uncertainty adjustment.

Appendix B supplies the iid counterpart. The design becomes $H_i=[1,f']$, factor mean becomes its sample average, $d_T=1/T$, and variance scales are $T/(T-2K-3)$ for factors and $T_i/(T_i-K-3)$ for stock residuals. The analogous quadratic-form expectation using $H_i$ yields the iid stock adjustment. Intermediate restricted strategies require consistent removal of columns and corresponding prior/degrees-of-freedom treatment. The article gives full formulas for TV-All and IID rather than a separate executable derivation for every restriction.

Appendix A also writes a joint predictor likelihood using $W_Z=[X,V_f,V_{rz}]$, where $V_{rz}$ includes one stock-residual column for each of the $N$ securities, padded with zeros outside its history. As printed, $(W_Z'W_Z)^{-1}$ need not exist when this design has more columns than the roughly five hundred time observations. The reported one-step return moments can be evaluated without inverting that full predictor-likelihood design. A literal implementation of every appendix inverse would nevertheless require a rank treatment or further restriction that is not specified. This is a reconstruction limitation, not evidence about what the authors' unavailable code actually did.

## Portfolio objective, leverage, and monthly implementation

The investor has quadratic utility of next-period gross wealth. If $r_{f,t}$ is the simple cash rate and $w_t$ the risky weights, portfolio gross return is $1+r_{f,t}+w_t'r_{t+1}$. Define $\kappa_t=1/\gamma_t-r_{f,t}$, where the paper transforms absolute risk aversion into its relative parameter $\gamma_t$. The equivalent optimization is

$$
\max_{w_t}\quad w_t'\mu_t-
\frac{1}{2\kappa_t}w_t'(S_t+\mu_t\mu_t')w_t,
\qquad
w_{i,t}\ge0,\quad \mathbf1'w_t\le2.
$$

The second moment $S_t+\mu_t\mu_t'$ is required by quadratic utility; replacing it with covariance alone changes the optimization. Concavity requires the intended positive $\kappa_t$. The cash weight $1-\mathbf1'w_t$ can reach −1: the strategy excludes short stock positions but permits borrowing to double equity exposure.

Without constraints,

$$
w_t=\kappa_t\frac{S_t^{-1}\mu_t}{1+\mu_t'S_t^{-1}\mu_t}.
$$

For factor-plus-diagonal covariance, Woodbury inversion reduces the expensive step to the $K$-dimensional factor system. Under constraints, a quadratic-programming solver must solve the full nonnegative allocation problem; simply truncating negative entries of this unconstrained expression is not equivalent. The source specifies no individual-position cap, industry cap, turnover penalty, solver, or convergence tolerances.

Risk aversion is recalibrated each month so that an investor restricted to cash and the unconditional market would invest 100% in the market. Algebraically, for market mean $\mu_M$ and variance $s_M^2$, the unconstrained calibration implies $1/\gamma_t=r_{f,t}+(s_M^2+\mu_M^2)/\mu_M$. This relation is a derived implementation aid and presumes a well-defined positive-mean calibration. The source reports mean $\gamma_t=1.97$, standard deviation .59, and corresponding post-1987 values 2.29 and .35. It is not a fixed-risk-aversion experiment across dates.

A monthly reconstruction should freeze the eligible universe and data at formation; fit stock and factor regressions on their respective available histories; compute predictive moments for each restriction; calibrate risk aversion using the common unconditional-market rule; solve the constrained optimization; and apply weights to the next month's realized excess returns. Portfolio cash accrual, financing, drifted pretrade weights, and trading deductions must be handled consistently. The model uses the risk-free rate for cash and implicit borrowing; a spread over that rate, margin calls, and capacity constraints are not modeled.

## Reported performance and what drives it

Table 2's core unrestricted results use monthly units. Standard errors shown below are those reported in the source.

| August 1972–December 2003 | IID | TV-beta | TV-RP | TV-alpha | TV-All |
|---|---:|---:|---:|---:|---:|
| Mean excess return, % | 1.90 | 1.33 | 3.16 | 2.90 | 3.16 |
| SE of mean, % | .76 | .72 | .80 | .87 | .84 |
| Monthly Sharpe ratio | .13 | .10 | .20 | .17 | .19 |
| CAPM alpha, % | .70 | .18 | 2.10 | 1.90 | 2.12 |
| SE of CAPM alpha, % | .46 | .43 | .60 | .71 | .66 |
| Conditional-beta CAPM alpha, % | .71 | .28 | 1.38 | 2.18 | 2.24 |
| Average equity allocation, % | 200.00 | 200.00 | 195.36 | 199.91 | 200.00 |

A monthly Sharpe ratio is mean excess return divided by monthly standard deviation. Its standard error is calculated using Lo's approach allowing serial dependence; the paper says an iid calculation yields similar inference. These ratios should not be read as annual numbers. TV-All's market beta is 2.17, compared with 2.51 for IID. Its larger alpha does not mean its absolute risk is small.

January 1988–December 2003 distinguishes the channels. TV-RP's CAPM alpha falls from 3.15% in the earlier period to 1.24%, while IID's rises from .08% to 1.56%. TV-alpha achieves mean excess return 3.79%, monthly Sharpe .25, CAPM alpha 2.55% with SE .94%, and conditional-beta CAPM alpha 2.58% with SE .98%. TV-All produces mean 3.58%, Sharpe .25, and CAPM alpha 2.30% with SE .83%. Beta variation alone is less compelling. The comparison supports stock-level conditional intercepts as an important source of the rule's performance, but does not identify them as economically unexplained under every possible pricing model.

CAPM restrictions often reduce both exposure and performance. In the full sample, restricted TV-All invests 179.42% in equities on average versus 200% unrestricted, and its mean return is 3.04%. Its conditional-beta CAPM alpha is 1.55% with SE .61%. Restricted IID invests 94.34% and earns mean .64%. Comparisons therefore combine restrictions on expected returns with changed optimal leverage and diversification; they are not experiments holding portfolio risk constant.

Figure 1 varies the initial estimation length from 120 to 437 months, giving 318 start-date experiments with a common ending date. These are heavily overlapping evaluation windows. TV-All's alpha is consistently higher in the plotted comparisons, with average differences of 88 basis points per month under unrestricted intercepts and 126 basis points under restrictions. Sharpe dominance is not uniform. The figure caption incorrectly maps “9812” to December 1990 and $P=316$; the main text and axis identify December 1998 and $P=437$. The latter mapping is internally consistent with the stated range of experiments.

The terminal gross wealth illustration is dramatic: \$1 becomes about \$6,537 under unrestricted TV-All, \$118.10 under IID, and \$27.60 in the market. Restricted TV-All and IID end around \$11,273 and \$54.40. These are frictionless reinvested wealth paths with the strategy's leverage assumptions. Table 2's separate “Delta Wealth” for a strategy long/market short investment is not the literal difference between these terminal wealth numbers; its exact compounded cash-flow convention is not written out. It should not be reconstructed by subtracting terminal values or presented as the same statistic.

## Stronger benchmarks and limits of statistical significance

The authors evaluate realized returns using Fama–French market, size, and value factors; add momentum; and allow benchmark loadings to vary with the four instruments. A conditional benchmark regression includes both factors and factor-instrument products. Positive alpha relative to that span means the specified linear timing strategies do not explain the intercept; it does not establish superiority to every nonlinear benchmark-timing rule.

For full-sample unrestricted TV-All, the three-factor alpha is 1.88% per month with SE .65%; adding momentum reduces it to 1.32% with SE .66%. Conditional three-factor alpha is 1.89% with SE .65%; conditional four-factor alpha is 1.17% with SE .66%. The last estimate has a ratio of about 1.77, so it is not significant at a conventional two-sided 5% threshold. The paper itself acknowledges that none of the unrestricted TV-RP, TV-alpha, and TV-All strategies beats the conditional four-factor benchmark at 5% over the full sample.

Several surrounding claims need equal care. The post-1987 TV-alpha conditional four-factor alpha is 1.98% with SE .92%, a ratio about 2.15. The prose calls this significant at 1%; the displayed numbers support approximately 5% two-sided normal inference, not 1%. Its post-1987 characteristic-selectivity estimate is 1.81% with SE .96%, and TV-All's is 1.63% with SE .85%; their ratios are about 1.89 and 1.92. These are suggestive at 10%, not conventional two-sided 5% evidence on the displayed standard errors. The note reports the table rather than silently adopting stronger prose labels.

Characteristic selectivity compares the strategy's realized return with a passive portfolio matched on size, book-to-market, and past-year return, following Daniel–Grinblatt–Titman–Wermers. Full-sample TV-All selectivity is 1.14% per month with SE .63%, compared with .71% and .44% for IID. Precise matched-portfolio breakpoints, weighting, and coverage rules are not reproduced in this article, so implementing this diagnostic requires the cited benchmark construction or original authors' files.

The tested family includes multiple restriction choices, benchmarks, subperiods, and start dates. Reported standard errors address individual estimates, not an explicitly multiplicity-adjusted search over all those outcomes. Nor does a significant alpha for one strategy establish that its difference from IID is itself significant; that requires inference on paired return differences or a joint model.

## Style exposure and the business cycle

Table 4 reports averages of portfolio-weighted quintile scores, with one low and five high. Unrestricted TV-All has size score 2.33, book-to-market score 2.86, and momentum score 4.17 over the full period. Its preference is thus for smaller eligible stocks and strong past performers, with only a mild full-sample growth tilt. “Small” is relative to a universe already excluding the smallest quartile. The post-1987 book-to-market score is 3.02, so a growth characterization is not uniform across subperiods or restricted strategies.

For TV-All, momentum score declines from 4.27 in expansions to 3.55 in recessions, while size declines from 2.37 to 2.11. TV-alpha shows similar movements, 4.34 to 3.55 and 2.40 to 2.14. These are descriptive comparisons using NBER recession designations, not a trading rule that necessarily knew recession classifications contemporaneously. The formation rules use the four instruments, not future NBER announcements.

Table 5 examines estimated stock-level alpha and beta functions across the full eligible universe rather than only selected holdings. At each formation date, regress the stock's estimated current alpha or beta on size, book-to-market, and prior-year return, then average coefficients using Fama–MacBeth-style inference corrected for serial correlation. Size slopes are multiplied by 10,000 and book-to-market/momentum slopes by 100 in the table. For TV-All, the full-sample alpha slope on momentum is 3.07 with SE .28 in those displayed units; the size and book-to-market alpha slopes are −.80 with SE .78 and −.04 with SE .03. These estimates help explain why the optimizer likes momentum, but they use generated alpha/beta estimates and do not identify a causal effect of characteristics.

A few secondary printed numbers are internally inconsistent. Table 4's full-sample equal-weighted book-to-market entry is 2.25, whereas Table 1 gives 1.25 and the two subperiod entries in Table 4 are 1.19 and 1.30. It cannot be the corresponding full-period average of those subperiod values. Table 5 also prints the TV-All expansion-minus-recession beta-size difference as 98.31, although its displayed component values −25.91 and −77.50 imply 51.59. These discrepancies do not alter the main reported return table, but they preclude treating every ancillary cell as mechanically consistent.

## Trading costs, selection, and what remains missing

The main performance tables exclude trading costs. The paper reports approximately 70% turnover for post-1987 TV-All and applies a 50-basis-point round-trip cost, producing a 35-basis-point monthly deduction. This is a useful sensitivity calculation, not a full net-return backtest. The exact turnover definition, whether it is normalized by wealth or gross stock exposure, and its relation to one-way trade dollars must be recovered before implementing costs. Apply costs to buys and sells consistently and avoid charging a quoted round-trip rate twice.

After a mechanical .35% subtraction, large CAPM alphas remain, but the weaker conditional four-factor evidence deserves separate evaluation. Costs depend on the stocks actually selected, trade size, spread, market impact, commissions, and financing. Excluding the smallest quartile does not by itself ensure that 200%-gross portfolios with frequent rebalancing have ample capacity. There is no detailed borrowing-rate spread, margin-liquidation simulation, liquidity participation limit, or position-level capacity analysis.

The authors defend the sixty-one-observation history requirement using a conditional ignorability assumption: given observed returns, survival does not depend further on true model parameters, combined with independent stock residuals. Under that assumption survival does not alter the posterior. This is a model statement, not an unconditional proof that database screening cannot create bias. Their discussion explicitly notes that prior dependence across securities could change the result. The paper also asserts that its size screen removes all performance-related delistings in this sample; it does not provide a delisting audit table or code implementing missing terminal returns. A replication must verify this claim against the actual eligibility calendar rather than assume that larger stocks never fail.

The actionable research contribution is a decomposed stock-level conditional-moment model, estimated recursively, with parameter-risk inflation and explicit portfolio restrictions. Reproduction still requires frozen CRSP/COMPUSTAT extracts, delisting conventions, macro series/vintages, exact screening dates, prior specification under each restriction, rank handling, numerical solver settings, matched-characteristic portfolio definitions, covariance estimators and lag choices for inference, and the turnover/financing convention. The main methods are in equations (1)–(16) and Appendices A–B; Tables 2–3 contain performance and its uncertainty; Figure 1 addresses start-date sensitivity; Tables 4–5 describe holdings and fitted functions; Section 4.3 treats costs and sample selection. Related methodological references include Stambaugh (1997), Kandel–Stambaugh (1996), Lo (2002), and Daniel–Grinblatt–Titman–Wermers (1997).
