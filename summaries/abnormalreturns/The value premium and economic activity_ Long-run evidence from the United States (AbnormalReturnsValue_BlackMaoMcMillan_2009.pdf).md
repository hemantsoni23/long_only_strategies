# The value premium and economic activity: Long-run evidence from the United States

**Angela J. Black, Bin Mao, and David G. McMillan (2009).** *Journal of Asset Management* 10(5), 305–317, doi:10.1057/jam.2009.15. The article was received in revised form on 3 July 2008. Source: [AbnormalReturnsValue_BlackMaoMcMillan_2009.pdf](../../Finance/AbnormalReturnsValue_BlackMaoMcMillan_2009.pdf). The local PDF contains the complete 13-page published article; printed page 305 is PDF page 1. This note uses that version, including its endnotes and references. There is no separate appendix in the file.

## Why this matters

The paper asks whether the accumulated performance of value relative to growth stocks shares a long-run stochastic trend with macroeconomic variables. This is a different question from whether contemporaneous HML returns covary with economic news or whether macroeconomic exposures price the cross-section. Its distinctive object is the logged **value premium price index**, abbreviated VPPI: a positive index constructed from value-minus-growth return data. The authors fit a five-variable Johansen vector error-correction model using monthly US data from January 1959 through December 2005. They find evidence for two cointegrating relations and report one normalized relation in which VPPI is negatively associated with industrial production and M2 and positively associated with a long-government-bond index.

The closest predecessor identified by the article is Black, Fraser, and McMillan's work on the long-run fundamentals of international value premiums, cited in its bibliography as a 2005 work in *International Review of Economics and Finance* 16, 113–129. The present contribution is a US macroeconomic cointegration application, not a new structural value model, a new tradable factor, or a newly measured value return premium. Johansen's method provides the econometric machinery. Zhang's costly-capital-reversibility model supplies an interpretation, but its structural parameters are neither estimated nor tested here.

For a quantitative researcher the useful empirical target is modest and precise: can the reported cointegration rank, normalized coefficients, and adjustment loadings be reproduced from a well-defined set of index series? The paper's stronger conclusion, that these relations favor rational compensation for nondiversifiable risk over investor error, requires additional restrictions that the fitted model does not supply. Cointegration is compatible with long-run economic comovement, but it does not itself identify a priced risk, its market price, or an implementable timing rule.

## Data, transformations, and the economic object

Table 1, printed page 308/PDF page 4, defines five monthly variables. There are 564 level observations and 563 first differences before losses from autoregressive lags. All levels enter in natural logarithms. The stated sources are Ibbotson Association for VPPI, CPI, and the long-government-bond index; seasonally adjusted industrial production and seasonally adjusted M2 come from DataStream because the desired adjusted versions were unavailable in Ibbotson.

| Symbol used here | Paper label | Actual series described in Table 1 | Difference |
|---|---|---|---|
| $v_t$ | LVPPI | Log value premium price index | Log monthly value-premium index return |
| $i_t$ | LIP | Log seasonally adjusted industrial production index | Monthly industrial-production growth |
| $m_t$ | LMS | Log seasonally adjusted M2 money supply | Monthly M2 growth |
| $c_t$ | LCPI | Log consumer price index | Monthly inflation |
| $b_t$ | LIR | Log long-term government bond price index | Monthly government-bond return |

The notation $b_t$ deliberately avoids calling the last variable an interest-rate level. The paper repeatedly does so in its prose, but Table 1 defines a bond price index, its first difference is explicitly a bond return, and endnote 1 says the ten-year long-government-bond return is used. Figure 2 also shows a strongly trending accumulated series rather than a recognizable yield history. A reproduction should therefore obtain the stated Ibbotson bond index and document precisely whether it includes reinvested income; it should not silently substitute the ten-year Treasury yield. The distinction changes the economic interpretation because bond prices and yields ordinarily move in opposite directions for a given duration and cash-flow schedule.

The paper does not disclose sufficient information to reconstruct VPPI uniquely. It says that the monthly price series is derived from returns and represents buying value while shorting growth, but it does not supply the Ibbotson series identifier, underlying value and growth stock definitions, portfolio weights, rebalancing rule, initial index value, financing convention, or a recursion for the index. These are first-order inputs rather than cosmetic metadata. If $r^V_t$ and $r^G_t$ are simple returns, three plausible constructions are different:

$$
W_t=W_{t-1}(1+r^V_t-r^G_t),
$$

$$
Q_t=Q_{t-1}\frac{1+r^V_t}{1+r^G_t},
$$

$$
D_t=P^V_t-P^G_t.
$$

The first compounds a unit-capital return spread under a particular reset convention; the second is a relative wealth ratio; the third is a difference of separately scaled indices. Their log changes need not agree, and the third need not remain positive. These equations are distinctions introduced in this note, not formulas supplied by the paper. Exact replication needs the authors' actual VPPI convention. In particular, a zero-cost long–short position does not have a uniquely defined percentage return until capital, collateral, and financing are specified.

CPI is not seasonally adjusted. Table 1 says the seasonally adjusted DataStream CPI was found stationary and its descriptive statistics were similar to the unadjusted series. That is an unusual reason for choosing one version: selecting a transformation partly to obtain common integration orders can affect a cointegration result. The reported analysis can be reproduced as stated, but the choice should subsequently be checked using a predeclared series definition. The long-bond index is not seasonally adjusted either. The paper gives no vintage date, release lag, revision policy, missing-data protocol, or seasonal-adjustment identifier. Consequently its full-sample explanatory exercise cannot be treated as a point-in-time forecast test.

## Descriptive evidence and diagnostic targets

Table 2, printed page 309/PDF page 5, reports the following first-difference statistics. Means and standard deviations are percentages per month; skewness and kurtosis are dimensionless. Reported Jarque–Bera probabilities round to 0.00 for every series.

| Monthly change | Mean | Standard deviation | Skewness | Kurtosis | Jarque–Bera |
|---|---:|---:|---:|---:|---:|
| CPI | 0.34 | 0.32 | 0.76 | 4.45 | 102.97 |
| Industrial production | 0.27 | 0.81 | −0.02 | 9.56 | 1008.01 |
| Long-government-bond index | 0.58 | 2.74 | 0.28 | 5.39 | 141.99 |
| M2 | 0.56 | 0.34 | 0.66 | 6.36 | 314.65 |
| Value premium index | 0.35 | 3.00 | 0.06 | 5.19 | 112.81 |

The 0.35% average is the mean log change in the selected VPPI, not a factor-regression alpha and not a net return on a specified hedge fund portfolio. Multiplying by 12 would give an annualized mean log growth approximation, not a tested annual investment performance statistic. The paper does not report a Sharpe ratio, maximum drawdown, trading-cost estimate, or formal comparison with a market or multifactor model.

The level standard deviations are 0.67 for log CPI, 0.40 for log industrial production, 1.06 for the log bond index, 0.96 for log M2, and 0.67 for log VPPI. These are useful for checking transformations, although sample level dispersion in trending series is not a stationary risk measure. Figure 1 shows VPPI's upward movement over much of the sample, interrupted by declines around the 1987 crash and the late-1990s episode. Figures 2 and 3 contrast trending levels with fluctuating first differences. Visual trends motivate unit-root work; they do not establish it.

The authors state that Augmented Dickey–Fuller and Phillips–Perron tests classify all five series as $I(1)$. Endnote 3 says the full test results are available on request. No test statistics, deterministic-term specifications, lag choices, bandwidths, or break allowances are supplied. Thus “all variables are $I(1)$” is a reported finding rather than an independently auditable table result. Given the long sample and changes in monetary regimes, a modern reproduction should record how the classification responds to deterministic trends and breaks without presenting those additional checks as something the original authors performed.

## Econometric specification and estimation

Let the five-dimensional state be $y_t=(v_t,i_t,m_t,c_t,b_t)'$. A level VAR of order $p$ is equivalently written as the vector error-correction model in equation (1), printed page 307/PDF page 3:

$$
\Delta y_t=\Pi y_{t-1}+\sum_{j=1}^{p-1}\Gamma_j\Delta y_{t-j}+B x_t+\varepsilon_t,
$$

$$
\Pi=\sum_{j=1}^{p}A_j-I_5,
\qquad
\Gamma_j=-\sum_{\ell=j+1}^{p}A_\ell.
$$

Here $A_j$ are level-VAR coefficient matrices, $x_t$ collects deterministic terms, $B$ is their coefficient matrix, and the innovation vector is assumed independently and identically distributed in the paper's exposition. If $\Pi$ has reduced rank $r$, it can be factored as

$$
\Pi=\alpha\beta',
$$

with $\alpha$ and $\beta$ both $5\times r$. The columns of $\beta$ span stationary combinations of levels, while $\alpha$ determines how each equation responds to disequilibrium. This is a reduced-form model. There is no household optimization, stochastic discount factor, production function, or structural shock identification in the empirical specification.

Using ordered generalized eigenvalues $\hat\lambda_1\ge\cdots\ge\hat\lambda_5$, the Johansen rank statistics are

$$
Q_{\mathrm{trace}}(r)=-T\sum_{j=r+1}^{5}\log(1-\hat\lambda_j),
$$

$$
Q_{\max}(r,r+1)=-T\log(1-\hat\lambda_{r+1})
=Q_{\mathrm{trace}}(r)-Q_{\mathrm{trace}}(r+1).
$$

The trace null is rank at most $r$ against a less restricted alternative; the maximum-eigenvalue null is rank $r$ against $r+1$. This notation corrects a printed indexing slip in equation (4), where a time-like subscript appears in the eigenvalue and trace expressions. It does not change the implemented hypothesis or reported table values. The text attributes critical values to Osterwald-Lenum.

The Schwarz information criterion selects six lags, subject to residuals being free of serial correlation; seven lags have the second-smallest criterion and provide the reported sensitivity case. The paper calls this lag count $k$ in the results, after using $k$ for the dimension in its methodological exposition. A software implementation should separate dimension $K=5$ from level-VAR lag order $p$. It also needs to resolve whether the table's “Lags=6” means six level-VAR lags or six lagged differences: the text describes a VAR lag choice, whereas software interfaces can label VECM difference lags directly. Failing to document that mapping produces a one-lag discrepancy.

Both the cointegrating equation and VAR are said to contain an intercept. Exact Johansen deterministic-case restrictions matter for critical values and for whether the levels can exhibit a linear deterministic trend. The paper does not provide a software command or full deterministic design matrix. It reports no criterion values, maximum lag search range, residual autocorrelation test, covariance matrix, or short-run $\Gamma_j$ estimates. Consequently one can reproduce the rank exercise only after making and recording these implementation choices.

A practical estimator reconstruction makes the relation between the VAR and the rank test explicit. Partial out the lagged differences and the chosen unrestricted deterministic terms from both $\Delta y_t$ and $y_{t-1}$. Call the resulting residuals $u_t$ and $w_t$, and form residual covariance blocks $S_{00}=T^{-1}\sum_tu_tu_t'$, $S_{11}=T^{-1}\sum_tw_tw_t'$, and $S_{01}=T^{-1}\sum_tu_tw_t'$, with $S_{10}=S_{01}'$. With a compatible treatment of restricted deterministic terms, the squared canonical correlations solve

$$
\det\left(\lambda S_{11}-S_{10}S_{00}^{-1}S_{01}\right)=0.
$$

The eigenvectors associated with the largest $r$ eigenvalues supply a basis for $\hat\beta$. Conditional on that basis, the adjustment estimate is

$$
\hat\alpha=S_{01}\hat\beta(\hat\beta'S_{11}\hat\beta)^{-1}.
$$

This reconstruction is standard reduced-rank regression algebra, stated here to make the estimation procedure implementable; the article itself reports the VECM and likelihood-ratio statistics rather than these intermediate matrices. Numerical replication should use a stable generalized eigensolver and check the normalization rather than explicitly invert ill-conditioned matrices. If an intercept is restricted to the cointegration space, the appropriate lagged-level regressor must be augmented before applying this calculation.

The distributional assumptions deserve an explicit audit. The table's strong nonnormality is not by itself proof that the rank conclusions are false, but it means that the simplest finite-sample Gaussian interpretation of the likelihood calculation is not literally supported by the marginal diagnostics. Serial dependence, conditional heteroskedasticity, deterministic misspecification, and breaks can all affect finite-sample calibration. The article does not report a residual bootstrap or heteroskedasticity-robust rank analysis. A replication should first match its conventional inference, then label any alternative calibration as a new robustness exercise. It should also distinguish rejection of rank one from evidence that exactly two economically meaningful equilibria exist: the testing procedure selects a statistical rank under a maintained five-series model, not the number of independent causal channels in the economy.

## Rank tests and reported long-run relations

The numerical rank results are in Tables 3–4, printed pages 312–313/PDF pages 8–9. The following table retains both tests so the selected rank is visible rather than inferred from significance stars.

| Lag setting | Null rank | Trace statistic | Trace 5% critical | Trace probability | Maximum eigenvalue statistic | Maximum 5% critical | Maximum probability |
|---|---:|---:|---:|---:|---:|---:|---:|
| 6 | 0 | 100.740 | 69.819 | 0.000 | 44.197 | 33.877 | 0.002 |
| 6 | 1 | 56.548 | 47.856 | 0.006 | 31.207 | 27.584 | 0.016 |
| 6 | 2 | 25.342 | 29.797 | 0.150 | 16.232 | 21.132 | 0.212 |
| 7 | 0 | 90.697 | 69.819 | 0.0005 | 35.703 | 33.877 | 0.0300 |
| 7 | 1 | 54.994 | 47.856 | 0.0092 | 27.619 | 27.584 | 0.0495 |
| 7 | 2 | 27.374 | 29.797 | 0.0928 | 16.631 | 21.132 | 0.1902 |

Both sequences reject zero and one relation and fail to reject two at 5%. The second relation at seven lags is marginal by the maximum-eigenvalue statistic: probability 0.0495. Thus rank two is the reported decision, but robustness should not be described as overwhelming. Table 3 omits a significance star beside the second maximum-eigenvalue row despite its probability of 0.016; the numerical test supports rejection regardless of that typographical inconsistency.

The authors choose the first eigenvector because it corresponds to the largest eigenvalue and normalize its VPPI coefficient to unity. Table 5 and equations (5)–(6) report:

$$
v_t=10.65-1.37i_t-1.29m_t-0.15c_t+1.29b_t+z_t^{(6)},
$$

$$
v_t=19.45-0.78i_t-1.70m_t-0.49c_t+1.19b_t+z_t^{(7)}.
$$

Here $z_t^{(p)}$ denotes the stationary deviation from the stated relation, added explicitly in this note. The paper prints the equilibrium equalities without a residual. Reported standard errors are:

| Coefficient | Six lags | Standard error | Seven lags | Standard error |
|---|---:|---:|---:|---:|
| Industrial production | −1.37 | 0.58 | −0.78 | 0.56 |
| M2 | −1.29 | 0.55 | −1.70 | 0.60 |
| CPI | −0.15 | 0.62 | −0.49 | 0.63 |
| Bond index | 1.29 | 0.16 | 1.19 | 0.17 |
| Constant | 10.65 | Not reported | 19.45 | 3.70 |

At six lags the paper calls industrial production, M2, and the bond index significant; at seven lags only M2 and the bond index remain significant. CPI is negative and insignificant in both cases, contrary to the positive sign hypothesized in the article. The numerical point estimates preserve their signs across lag choices, but the industrial-production coefficient changes substantially and loses conventional significance. A claim that every macro relation is robust would exceed the table.

The first reported error-correction loadings are −0.0183 for VPPI, 0.002 for industrial production, −0.001 for M2, −0.002 for CPI, and −0.014 for the bond index at six lags. Their standard errors are respectively 0.006, 0.001, 0.0005, 0.0005, and 0.005. At seven lags the corresponding coefficients are −0.017, 0.004, −0.001, −0.002, and −0.013, with standard errors 0.006, 0.002, 0.001, 0.0001, and 0.006 as printed. Rounding makes some stars difficult to reconstruct from ratios; retain the published precision rather than reverse-engineering unreported digits.

A positive VPPI deviation is therefore associated with a negative subsequent VPPI change, conditional on the rest of the reported model. Interpreting −0.0183 as a universal “1.83% monthly convergence rate” is too strong: the macro variables also adjust, there are lagged differences, and the selected rank is two. Only in a deliberately simplified scalar process with all other responses suppressed would an autoregressive coefficient of $1-0.0183$ imply a half-life near 37.5 months. The full system's convergence rates require the complete companion matrix and the omitted second relation.

## Identification and interpretation limits

The most consequential econometric omission is not a missing t-statistic. With $r=2$, the cointegration space is identified, while a particular basis generally is not a uniquely interpretable economic relation. For any nonsingular $2\times2$ matrix $H$,

$$
\alpha\beta'=(\alpha H^{-\mathsf T})(\beta H)'.
$$

Choosing the vector associated with the largest eigenvalue gives a statistical normalization, but does not establish that its coefficients are invariant structural elasticities. A structural interpretation needs restrictions that distinguish the two relations, together with tests of those restrictions. The article supplies neither the second vector nor an economic exclusion scheme. Reproducing only the displayed VPPI equation therefore reproduces a selected summary of the estimated space, not the entire rank-two VECM.

A second issue is the relation between accumulated realized performance and required expected returns. The paper motivates a negative industrial-production relation by arguing that value becomes riskier in bad times, value prices fall relative to growth, and the value premium increases. That argument can describe an increase in a **prospective required return** after a relative price decline. It does not automatically describe an increase in a wealth index formed by cumulating **realized value-minus-growth returns**. If value falls more today, today's value-minus-growth realized return is negative, so a conventionally compounded long-value/short-growth index falls today. The article moves between these concepts without a pricing identity that reconciles them. A reproduction should preserve the empirical VPPI definition and avoid transferring the sign narrative to a different object.

The bond-series issue is similarly substantive. A positive coefficient on an accumulated bond price or return index is not direct evidence that a higher Treasury yield raises the value premium. The authors' discount-rate narrative invokes yields and substitution into interest-bearing securities, while the fitted series reflects bond valuation and carry. To test that narrative one needs an explicitly measured yield and a model appropriate to its integration properties; the article says it avoided short rates because their integration order differed. Substituting a yield after the fact would create a new specification, not repair the original estimate by relabeling it.

Finally, macroeconomic comovement does not discriminate cleanly between rational risk and mispricing. Investor expectations and sentiment can covary with production, money, and inflation. A priced-risk claim would require, for example, a discount-factor covariance restriction and a positive associated price of risk, or a structural model showing why the measured exposure commands compensation. No cross-sectional pricing test, SDF estimate, conditional expected-return test, or competing behavioral likelihood is provided. The final discussion itself invokes institutional demand for value income and individuals' trend chasing in growth, illustrating that the narrative is not exclusively a frictionless rational-risk explanation.

One useful normalization check is to multiply any positive index by a constant before taking logarithms. This adds a constant to the associated log series and should be absorbed by a correctly specified intercept. In contrast, changing the leverage convention when compounding a long–short return changes the entire time path and can change cointegration rank. Index rebasing is therefore a harmless unit change under the maintained model; changing the underlying return recursion is an economic change. This distinction is especially important for VPPI because the paper provides the index's source and interpretation but not its exact construction.

## Reproduction plan and investment relevance

A faithful reproduction starts with the exact Ibbotson series rather than a convenient HML download. Match the 564 months and every transformation, verify the five monthly means and volatilities, and establish the VPPI compounding and bond-index definitions. Record the DataStream codes, seasonal-adjustment flags, CPI version, units, and download vintage. Index rebasing changes log intercepts but should not change slope coefficients in a correctly specified model with an intercept; a discrepancy isolated to the constant may therefore be benign, while different return means indicate a more fundamental construction problem.

Next reproduce the ADF and Phillips–Perron classifications, lag selection, and residual diagnostics. Fit the five-dimensional system at both stated lag settings with an explicit deterministic-case declaration. Store the generalized eigenvalues, effective sample size, all rank statistics, both normalized vectors, all adjustment columns, short-run coefficients, residual covariance, and stability roots. These outputs permit an audit of the reported coefficients and enable the full error-correction dynamics to be studied. The paper's two reported lag choices and its CPI-exclusion check, mentioned without numerical results in endnote 8, are useful replication targets; they are not a broad robustness battery.

Further work should distinguish three questions. First, does rank two survive data-vintage choices, alternative valid deterministic specifications, and economically motivated subsamples? Second, can restrictions on the two-dimensional space identify a stable economic relationship involving VPPI? Third, does any resulting signal improve forecasts using only released information? The third requires a separate rolling or expanding-window exercise with macroeconomic publication delays, real-time revisions, a training period, and a declared forecast horizon. Full-sample fitted disequilibrium is not an admissible historical trading signal.

The paper supplies no position sizing, leverage constraint, financing treatment, turnover, borrow availability, short rebate, transaction-cost model, or execution schedule. A macro timing strategy inferred from its VECM would have to translate a forecast of log VPPI growth into weights on specified value and growth portfolios, then include those costs and compare with a constant value allocation and simple forecast baselines. Because the original VPPI is not fully specified, even that mapping cannot be assumed. The result is most useful as a historical lead about possible long-run comovement and as a case study in the gap between a reduced-form relation and a risk-premium explanation.

The directly supported finding is that the authors' chosen monthly US index system rejects no cointegration and selects rank two over 1959–2005, with the displayed basis vector showing stable signs for M2 and the bond index across six and seven lags. The unresolved construction, identification, and economic-interpretation issues prevent those coefficients from serving as a ready macro hedge ratio or an independently established explanation of the value premium.
