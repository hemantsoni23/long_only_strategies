# Do the stock and CDS markets price credit risk equally in the long-run?

Lidija Lovreta and Zorica Mladenović. *The European Journal of Finance*, published online July 26, 2018, DOI 10.1080/1351847X.2018.1501402. [Source PDF](<../../Finance/Do the stock and CDS markets price credit risk equally in the long run_final.pdf>). The supplied file comprises a publisher cover and the complete 28-page article, including company-level tables, endnotes, references, and Appendices A–B. PDF page numbers are used below; subtract one for printed article pages. An earlier version circulated as *Structural Breaks in the Long-run Equilibrium between the Stock and CDS Markets*. The separately linked publisher supplement was not obtained; the two appendices embedded in this PDF were read.

## Why this matters

A persistent equity–credit pricing gap is not automatically a convergence trade. It can reflect a changing equilibrium, an inappropriate transformation of equity prices, or a pair with no stable long-run relation at all. Lovreta and Mladenović examine this distinction using European investment-grade companies. Their central result is that allowing structural breaks produces much more evidence of cointegration between observed CDS spreads and equity-implied credit spreads than a constant-parameter test does.

The useful contribution is a specification diagnostic for capital-structure research. A model that forces equity-implied and market spreads to coincide can repeatedly enter positions that merely reflect a persistent level difference or a new regime. Estimating a broader long-run relation reduces that problem in the paper's retrospective trading exercise. It does not establish a deployable arbitrage: the spread calibration, pair classification, and equilibrium estimation use the full sample, and transaction costs are omitted.

The title's phrase “price credit risk equally” is stronger than the hypothesis actually tested. Cointegration with an unrestricted slope, intercept, trend, and possible break means that a fitted combination is stationary. It does not imply equal spread levels, a unit hedge ratio, unbiased structural-model prices, or a common market price of credit risk. This distinction matters both when interpreting the 92.1% headline and when defining a trading residual.

## Data, sample selection, and units

The starting universe consists of nonfinancial members of the iTraxx Europe index. Removing banking and financial firms leaves 100 names; requiring market capitalization and CDS data throughout the study leaves 72. The instruments are euro-denominated five-year CDS on senior unsecured debt, with Datastream providing CDS quotes, market capitalization, five-year local swap rates, and short- and long-term liabilities. The final analysis is described consistently in the abstract, methods, appendices, and results as covering 2004–2017, with 731 weekly observations. One sentence in Section 2.1 instead says January 2004–December 2014; this is an unresolved source inconsistency, not an alternative sample implemented here.

The authors exclude private firms and entities no longer separately observable after mergers or acquisitions. Their balanced panel is convenient for comparing tests over the same span but conditions on continued observability. The source argues that excluded delistings reflect transactions rather than default. It does not supply a general proof that selection cannot affect estimated integration or trading performance.

Table 1 describes the 72 names: mean market capitalization is €25,634.32 million, mean leverage 0.53, and mean annual equity volatility 0.30. Corresponding medians are €17,024.62 million, 0.52, and 0.29. Leverage means book total liabilities divided by market capitalization plus those liabilities. Across firms, average market and model spreads are 101.57 and 97.84 basis points. Appendix A identifies every company and its average spreads; these are not a reconstruction of the underlying daily panel.

The structural model is evaluated daily, but econometric tests use weekly observations to reduce microstructure effects. Both spreads are logged. Before testing cointegration, the authors apply ADF and Phillips–Perron tests to levels and first differences. ADF specifications include no deterministic term, a constant, and a constant plus trend. Lag selection starts at 19, from the integer part of $12(T/100)^{1/4}$, and proceeds downward using t-tests; PP uses 19 residual-autocorrelation lags. Nine firms are excluded when one level test rejects a unit root at 5% and the other at least at 10% in either series. The remaining 63 firms form the main cointegration sample, and their first differences reject nonstationarity.

This screening is part of the research design, not evidence that the omitted nine are economically unintegrated. A stationary pair would require a different specification. Nor does failing to reject a unit root establish that an integrated process generated the observations. The paper's reported fractions must retain the denominator 63 rather than being described as percentages of all European firms or all 72 original names.

## Reconstructing the equity-implied spread

The CreditGrades transformation is given in Equations (1)–(4), PDF pages 5–6. Let $V$ be asset value, $S$ market equity value, $D$ book total liabilities, and $\sigma$ asset volatility. Over the pricing horizon the model assumes

$$
\frac{dV_t}{V_t}=\sigma\,dW_t.
$$

The default barrier is random:

$$
LD=\bar L D\exp(\lambda Z-\lambda^2/2),\qquad Z\sim N(0,1).
$$

Here $\bar L=E[L]$, and $\lambda^2=\operatorname{Var}(\log L)$. The source's prose loosely calls this a standard deviation; $\lambda$ is the standard deviation of log recovery, not of recovery itself. Issue-specific recovery $R$ is a separate parameter. Define

$$
d=\frac{V_0}{\bar L D}e^{\lambda^2},\qquad
A_t=\sqrt{\sigma^2t+\lambda^2}.
$$

The placement of $e^{\lambda^2}$ is important: it multiplies $V_0/(\bar L D)$, as the rendered formula confirms. The CreditGrades survival expression is

$$
P(t)=\Phi\!\left(-\frac{A_t}{2}+\frac{\log d}{A_t}\right)
-d\Phi\!\left(-\frac{A_t}{2}-\frac{\log d}{A_t}\right).
$$

For constant pricing rate $r$, let

$$
\xi=\frac{\lambda^2}{\sigma^2},\qquad
z=\sqrt{\frac14+\frac{2r}{\sigma^2}},
$$

$$
G(u)=d^{z+1/2}\Phi\!\left(-\frac{\log d}{\sigma\sqrt u}-z\sigma\sqrt u\right)
+d^{-z+1/2}\Phi\!\left(-\frac{\log d}{\sigma\sqrt u}+z\sigma\sqrt u\right).
$$

The maturity-$t$ par spread is

$$
c(t)=r(1-R)
\frac{1-P(0)+e^{r\xi}[G(t+\xi)-G(\xi)]}
{P(0)-e^{-rt}P(t)-e^{r\xi}[G(t+\xi)-G(\xi)]}.
$$

The asset/equity link is the approximation $V=S+\bar L D$, giving

$$
\sigma=\frac{S}{S+\bar L D}\,\sigma_S^*.
$$

Consequently a constant reference equity volatility does not mean constant asset volatility: leverage changes as equity value and debt change. The model transforms equity information together with accounting debt and interest rates; it is not a function of equity prices alone.

For each company, $\bar L$ minimizes the sum of squared differences between observed and model CDS spreads using all available observations. The cross-sectional average fitted value is 0.58. The remaining settings are $\lambda=0.30$, issue recovery $R=0.40$, maturity five years, and the local five-year swap rate as the interest-rate input. Reference equity volatility is the annualized standard deviation of continuously compounded returns over the full sample, held fixed across dates. The authors deliberately avoid repeated recalibration, which would import subsequent CDS movements into the equity-implied series. Nevertheless the initial full-sample calibration and volatility use future information relative to historical trade dates.

A convenient independent implementation check uses the discounted survival annuity $B(t)=\int_0^t e^{-ru}P(u)\,du$. Integration by parts gives the equivalent expression

$$
c(t)=(1-R)\frac{1-e^{-rt}P(t)-rB(t)}{B(t)}.
$$

This identity includes the model's initial default mass $1-P(0)$ and is a derived numerical check rather than an additional empirical result. It also avoids the explicit $0/0$ of the closed form at $r=0$. Both formulas should agree before calibration. A test using $S=D=100$, $\bar L=0.58$, $\sigma_S^*=0.30$, $\lambda=0.30$, $r=0.02$, $R=0.40$, and $t=5$ was checked by direct Simpson integration of the annuity; these are synthetic inputs, not a fitted company.

Appendix B compares rolling volatility windows of 22, 63, 126, 252, and 1,000 days against the constant reference. The appendix prose says 250 where the table says 252. Its weekly regression includes contemporaneous and one-lag changes in model spreads plus one lag of market-spread changes. Average firm-level adjusted $R^2$ rises from 0.09 for 22 days to 0.20 for 1,000 days and 0.22 for constant volatility; corresponding contemporaneous correlations are 0.09, 0.32, and 0.34. For cross-sectional average spreads the figures are 0.05, 0.46, and 0.50 for adjusted $R^2$, and 0.07, 0.64, and 0.66 for correlation. Newey–West HAC standard errors are used. Over 2013–2017, constant volatility gives average firm $R^2=0.25$ and market-level $R^2=0.60$, against 0.22 and 0.55 for the 1,000-day window. These fit comparisons support the chosen retrospective transformation; they are not out-of-sample forecast comparisons.

## Cointegration with changes in the equilibrium

Write $y_{1t}=\log ICS_t$ and $y_{2t}=\log CDS_t$. A stationary residual can take the form $y_{1t}-a-by_{2t}-gt$, so neither equality of levels nor stationarity of the raw spread difference follows unless additional restrictions hold. The cross-sectional mean log basis drifts downward over the sample, motivating deterministic trends rather than automatically omitting them.

Gregory–Hansen tests admit one unknown break. Let $d_t(\tau)=1\{t>\tau\}$. The four alternatives are

$$
\begin{aligned}
C:\quad y_{1t}&=\mu_1+\mu_2d_t+\beta y_{2t}+e_t,\\
C/T:\quad y_{1t}&=\mu_1+\mu_2d_t+\delta t+\beta y_{2t}+e_t,\\
C/S:\quad y_{1t}&=\mu_1+\mu_2d_t+\beta_1y_{2t}+\beta_2d_ty_{2t}+e_t,\\
C/S/T:\quad y_{1t}&=\mu_1+\mu_2d_t+\delta_1t+\delta_2d_tt
+\beta_1y_{2t}+\beta_2d_ty_{2t}+e_t.
\end{aligned}
$$

For each candidate break within the central 70% of the sample, estimate the regression and compute the residual ADF, $Z_\alpha$, and $Z_t$ statistics. The reported statistics are the infima over break dates, so the most negative value is used. The Phillips statistics employ a quadratic-spectral kernel and Andrews bandwidth; residual ADF lags use the downward t-test procedure. Critical values must correspond to a searched break and the chosen deterministic model, not ordinary residual-ADF values.

The authors also estimate a two-variable VECM,

$$
\Delta y_t=\alpha(\beta'y_{t-1}+\gamma't)+\mu
+\sum_{j=1}^{k-1}\Gamma_j\Delta y_{t-j}+\epsilon_t,
$$

with rank $r$, $2\times r$ adjustment and cointegration matrices, and VAR lag order chosen by reduction from 27. They compare several restrictions on the deterministic terms. Johansen's rank-zero trace statistic is $-T\sum_{j=1}^2\log(1-\hat\lambda_j)$; a rank-one result should also retain the rank-one null against rank two. A full-rank bivariate system is not the intended one-common-trend result.

The Johansen–Mosconi–Nielsen extension permits a broken level or trend. In the source notation its form is

$$
\Delta y_t=\alpha\begin{pmatrix}\beta\\\gamma\end{pmatrix}'
\begin{pmatrix}y_{t-1}\\tE_t\end{pmatrix}
+\mu E_t+\sum_{j=1}^{k-1}\Gamma_j\Delta y_{t-j}
+\sum_{j=1}^{k}\kappa_jD_{t-j}+\epsilon_t.
$$

$E_t$ indicates the two regimes, while impulse terms handle observations near the break. The source sets the first $k$ observations in each regime to zero in these indicators. Its prose describing $D_t$ mixes the time and lag indices; implementation requires a consistent set of transition impulses as in the underlying procedure. The break date is first taken from Gregory–Hansen results and, if insignificant, reconsidered using recursively calculated eigenvalues and trace statistics. Thus this is not a single prespecified-break experiment. The test uses the extension's break-dependent critical values. Unlike the most general Gregory–Hansen alternative, these estimated equations preserve the stochastic slope between the two spreads while changing deterministic components.

Qu's test asks a different question: whether cointegrating rank exceeds zero in at least one segment, allowing temporarily absent cointegration. For segment $k$ of length $n_k$, detrend the vector $y_t$ using the specified deterministic terms to obtain $u_t$, and form

$$
A_k=n_k^{-2}\sum_{t\in k}u_tu_t',\qquad
B_k=n_k^{-4}\sum_{t\in k}
\left(\sum_{j\in k,\,j\le t}u_j\right)
\left(\sum_{j\in k,\,j\le t}u_j\right)'.
$$

The generalized eigenvalues solve $\det(\rho B_k-A_k)=0$. For $n=2$ and null rank $r_0=0$, the source defines

$$
\operatorname{Sup}Q^m=\sup_{\Pi\in\Pi_\epsilon}
\frac{\sum_{k=1}^{m+1}\sum_{i=1}^{n-r_0}\rho_i(B_k^{-1/2}A_kB_k^{-1/2})}
{100(n-r_0)}.
$$

Ordered eigenvalues are ascending; the factor 100 belongs to this source's statistic and critical-value normalization. Admissible partitions enforce segment length at least $\epsilon T$, with $\epsilon=0.20$. The authors consider one through three breaks. Their unknown-regime statistics combine one- and two-break versions: with $a=c(\alpha,1,n-r_0,\epsilon)/c(\alpha,2,n-r_0,\epsilon)$, $WQ=\max(\operatorname{Sup}Q^1,a\operatorname{Sup}Q^2)$ and $SQ=\operatorname{Sup}Q^1+a\operatorname{Sup}Q^2$. Exact replication needs the corresponding critical values and GAUSS implementation, credited to Qu but not included in the PDF. Changing trimming or deterministic terms without changing critical values would invalidate inference.

## What the tests actually find

The principal numerical comparisons are as follows; significance thresholds differ across summaries and should not be silently harmonized.

| Procedure or comparison | Reported result among 63 pairs |
|---|---:|
| Standard Engle–Granger, at 5% / 10% | 11 / 19 firms, 17.5% / 30.2% |
| Standard Johansen, reported selected sample | 12 firms, 19.0% |
| Additional firms under broken deterministic Johansen model | 33 firms, 52.4% |
| Combined ordinary and broken Johansen models | 45 firms, 71.4% |
| Gregory–Hansen, all three statistics significant for at least one specification | 48 firms, 76.2% |
| Gregory–Hansen, any statistic significant at 10% | 57 firms, 90.5% |
| Qu, cointegration in one or more segments | 50 firms, 79.4% |
| “Strong” evidence from at least one considered procedure | 58 firms, 92.1% |

Gregory–Hansen's four specifications give all-three-statistic support for 39, 37, 32, and 26 companies for C, C/T, C/S, and C/S/T respectively. Rejection does not itself establish a break: the no-break relation is nested. The source therefore compares ordinary residual tests before describing break evidence. Its aggregate “strong” classification requires all three statistics for Gregory–Hansen or Qu, but 5% significance for the Johansen procedures. The summary is a union across several tests and specifications, not a test with a familywise 5% error rate.

The source reports 76.7% of detected significant break dates between July 2007 and August 2008, with 73.1% between August 2007 and April 2008; 0.4% fall in June 2007 and none in September 2008. These percentages summarize detected dates, not distinct firms. They principally concern the searched Gregory–Hansen dates; they should not be read as a statement about every date later chosen in Table 4. Figure 2's average statistic trough near 2007–2008 is supportive visualization, not an independent cross-sectional test.

Simply splitting into 2004–2007 and 2009–2017 produces less evidence: Engle–Granger finds 39.7% and 44.4%, while ordinary Johansen finds 50.8% and 49.2%. This comparison changes both the treatment of breaks and the available sample size, so it cannot isolate a single causal explanation for increased rejection. It does show why imposing one crisis date on all firms is restrictive.

For Qu's procedure, SQ and WQ reject for 32 and 34 companies at least at 10%. One-break SupQ rejects for 33, while the union allowing more breaks detects multiple regimes for 41 firms. The source classifies nine firms as having one break, six as two, and 35 as at least three. These are outcomes of its testing rules, not consistent estimates of an exact break count established here. Raising minimum segment size to 0.25 produces 52 firms with some-segment cointegration, versus 50 at 0.20; underlying robustness tables are available on request rather than embedded.

Several source inconsistencies prevent mechanically treating all reported classifications as a verified dataset. PDF page 13 says “remaining 43” after finding 12 of 63, although subtraction leaves 51. Table 3 includes selected rank-zero p-values of 0.06–0.09, whereas later prose defines strong Johansen evidence at 5%. Table 4 includes Henkel, company 29, with a printed rank-zero p-value of 0.29 even though its caption describes all 33 entries as supported cointegration. Some second-rank p-values are also near 0.05–0.10. These entries were checked visually. The note reports the authors' aggregate counts without repairing company classifications by guesswork; reproducing them requires the original code, unrounded tests, and selection rules.

## Capital-structure trading experiment

The pricing-error strategy opens a trade when $CDS_t>1.5ICS_t$ or $ICS_t>1.5CDS_t$. If market CDS is high, sell protection and short equity; if it is low, buy protection and buy equity. CDS notional is €1 and initial capital per position is €0.50. Positions use a static equity hedge and close upon convergence or a maximum 180-day holding period, whichever occurs first. Decisions are weekly. There are no transaction costs. The paper relies on Yu and Duarte–Longstaff–Yu for outstanding-CDS valuation and the hedge ratio; it does not print those implementation formulas. Its specific departure is interpolation between current four- and five-year CDS quotes to mark aging contracts.

The equilibrium-error strategy uses the ordinary or broken Johansen relation selected for that company. Write its residual as $z_t$; enter when

$$
|z_t|>\log(1.5)=0.4054651081,
$$

and exit at the estimated equilibrium, subject to the holding limit. With the normalization $z_t=\log ICS_t-\hat b\log CDS_t-\hat a_t$, positive $z_t$ indicates model-implied spread above the fitted equilibrium relative to CDS. One must translate this sign consistently into protection and stock positions. A cointegration slope in log-spread space is not a number of equity shares; the structural delta hedge remains a separate calculation.

Table 6 supplies the following gross results. “Entry” is trades opened divided by available observations; “converge” and “negative HPR” are proportions of trades. Monthly statistics come from equal weighting open trades' weekly excess returns and compounding to months.

| Trigger and sample | Entry | Converge | Negative HPR | Mean HPR | Mean monthly excess | Annualized Sharpe |
|---|---:|---:|---:|---:|---:|---:|
| Pricing error, no cointegration | 65.47% | 10.75% | 27.81% | 1.32% | 0.15% | 0.49 |
| Pricing error, cointegrated | 48.79% | 16.23% | 23.30% | 2.48% | 0.24% | 0.72 |
| Pricing error, no break | 42.79% | 19.73% | 19.47% | 2.85% | 0.27% | 0.78 |
| Pricing error, one break | 50.97% | 15.16% | 24.47% | 2.36% | 0.23% | 0.64 |
| Equilibrium error, cointegrated | 20.08% | 49.62% | 14.97% | 3.15% | 0.28% | 0.89 |
| Equilibrium error, no break | 17.42% | 51.03% | 12.01% | 2.85% | 0.26% | 0.78 |
| Equilibrium error, one break | 21.24% | 49.22% | 16.04% | 3.26% | 0.29% | 0.80 |

For all cointegrated pricing-error trades, monthly standard deviation is 1.15%, skewness 0.68, and the mean-return t-statistic 2.70. Equilibrium-error trading gives 1.09%, 1.13, and 3.31 respectively. Noncointegrated pricing-error trades have standard deviation 1.04%, skewness −0.82, and t-statistic 1.81. Drawdowns exceeding 20% occur in 1.96%, 1.47%, and 1.18% of trades for noncointegrated pricing-error, cointegrated pricing-error, and cointegrated equilibrium-error portfolios. The authors report a t-statistic of −13.81 for the 1.32% versus 2.48% holding-return comparison, but the dependence treatment for overlapping trades is not specified sufficiently to reproduce that inference.

The apparent benefit comes mainly from the broken-equilibrium subsample. Its mean HPR rises from 2.36% to 3.26%, while the stable subsample remains at 2.85%. For 2009–2017, the source reports mean monthly excess return and Sharpe of 0.21% and 0.75 for the cointegrated portfolio, versus 0.14% and 0.55 for noncointegrated names. Restricting the return-evaluation period does not by itself turn full-sample pair selection and parameter estimation into an out-of-sample design.

The important operational conclusion is to distinguish a known persistent level difference from an unexpected residual movement. The paper does not establish that its 0.89 gross Sharpe survives CDS bid–ask costs, stock borrow, margin, collateral funding, asynchronous quotes, estimation error, or real-time break detection. The 50%-of-notional capital convention also affects reported returns and does not specify a feasible stressed margin policy.

## Liquidity correlates and their interpretation

The dependent variable in the final cross-sectional probits equals one for a pair classified as cointegrated by ordinary or broken Johansen tests. There are 63 observations. Eight univariate specifications and one joint specification examine equity illiquidity, CDS quote staleness, funding exposure, idiosyncratic equity risk, average CDS spread, leverage, equity volatility, and firm size; robust standard errors are reported.

Equity illiquidity is the mean Amihud price-impact ratio, scaled by $10^6$ and logged. PZERO is the percentage of zero CDS-spread changes. Idiosyncratic risk is $\log[(1-R^2)/R^2]$ from a market regression on STOXX Europe 50 excess returns. Size is log market capitalization. The funding dummy is constructed in stages: regress weekly CDS changes on current and lagged implied-spread changes and lagged CDS changes; regress the resulting CDS innovations on changes in the euro TED spread and iTraxx; mark firms whose TED coefficient is statistically significant. TED here means three-month EURIBOR minus three-month German Treasury-bill yield, not the US dollar convention.

PZERO has coefficient −0.158 with standard error 0.07 in its univariate probit, and −0.236 with standard error 0.11 jointly. The funding dummy has −0.749 (0.37) univariately and −0.927 (0.42) jointly. Both remain significant at 5%; the other explanatory variables are not. Joint pseudo-$R^2$ is 0.164. These coefficients are latent-index slopes, not percentage-point marginal probabilities. The mean-spread and volatility scaling used in the estimation must be obtained before comparing coefficient magnitudes across variables.

This evidence links weak integration to stale CDS quotes and funding-related price movements. It does not identify a causal effect of liquidity: the dependent variable is an estimated test decision, quote staleness changes test power, the funding dummy is itself generated by a significance test, and 63 observations provide little room for robust joint inference. Within the cointegrated subset, the same variables do not significantly distinguish stable from broken relations.

## Replication sequence and remaining inputs

A faithful reproduction would first recover the 72-name panel and exact historical iTraxx selection rule, match contracts and currencies, align observations and accounting release dates, and reproduce five-year implied spreads in consistent decimal units. The synthetic formula check above returns 72.5184551 basis points from both the analytic formula and a 10,000-subinterval Simpson annuity, with survival probabilities $P(0)=0.9995348891$ and $P(5)=0.9400029213$; it validates transcription and pricing arithmetic, not the empirical calibration.

Next reproduce the nine unit-root exclusions, run the full menu of deterministic and break specifications, retain all rank decisions and dates, and reconcile the ambiguous table classifications. Only then construct the retrospective trading groups, signals, marks, hedge shares, capital accounts, and monthly indices. Appendix A's firm identifiers are essential because company numbers in the test tables are not a sorted risk ranking. The final probit must use the same pair classifications as the trading tables.

The PDF does not supply the raw Datastream panel, calibration optimizer and bounds, exact weekly quote alignment, treatment of accounting-data availability, all selected lag orders, all break-search decisions, critical-value simulation settings, complete CDS marking and hedge code, or a fully specified overlapping-trade inference procedure. These are material missing inputs. An investment implementation would additionally require an expanding or rolling training scheme, a real-time break rule, and executable cost and collateral data. Those would be a new experiment rather than a literal reproduction of the published Sharpe ratios.

The source's narrower finding survives these qualifications: under its particular CreditGrades transformation, standard full-sample constant-parameter cointegration tests frequently miss relationships recoverable with deterministic changes or segmented regimes. The researcher should model those changes explicitly and test whether they can be recognized using only information available before committing capital.
