# On the Forecasting Accuracy of Multivariate GARCH Models

Sébastien Laurent, Jeroen V. K. Rombouts, and Francesco Violante, January 28, 2011. [Source PDF](../../Finance/multivariateGARCHAccuracy_LaurentRomboutsViolante_2011.pdf). This note covers the complete local 30-page version, including references. The separately mentioned online supplementary Tables A1–A5 are not contained in this PDF and were not available among the locally identified source files. Subsample findings below are therefore attributed to the main text, not to an independently inspected supplement.

## Why this matters

A covariance forecast is useful only relative to a target, a horizon, and a loss function. This paper makes that dependence concrete by comparing 125 multivariate GARCH specifications for ten equities over a long forecast period containing both quiet and crisis markets. It combines noisy realized-covariance targets with multiple-model inference rather than declaring the smallest observed loss the winner.

The most useful result is not a single model recommendation. Quadratic losses tend to retain many models, while a loss that penalizes covariance underprediction sharply can select a different family. Short crisis intervals can dominate a decade's average loss. A large model confidence set can reflect low power or highly variable losses, rather than many economically interchangeable models.

The empirical contribution is a broad, internally organized comparison of available MGARCH architectures. The paper does not introduce DCC, orthogonal GARCH, MCS, SPA, or the underlying robust-loss theory. It applies those methods across model families, volatility regimes, proxies, and horizons. Its conclusions are confined to a ten-stock universe and statistical covariance losses; it does not measure portfolio utility, turnover, transaction costs, or realized investment returns.

The source's preferred benchmark is Engle DCC with asymmetric marginal volatility. However, the concluding assertion that this benchmark is not outperformed regardless of evaluation period is broader than its own SPA table supports. The exact table evidence is retained below so that a replication does not inherit that overstatement.

## Target, observations, and forecasting clock

Returns satisfy $r_t=\mu+\varepsilon_t$, with a constant conditional mean and conditional covariance $H_t=E_{t-1}(\varepsilon_t\varepsilon_t')$. The empirical target is open-to-close covariance. Overnight returns are excluded from both the daily model inputs and the intraday proxy; the paper treats overnight variation as separately occurring jumps. Consequently the estimated matrices are not close-to-close daily risk forecasts and do not cover overnight exposure.

The data source is Tick Data's One-Minute Equity Data database. The ten stocks are Abbott Laboratories, BP, Colgate-Palmolive, Eastman Kodak, FedEx, Coca-Cola, PepsiCo, Procter & Gamble, Wal-Mart, and Wyeth. They were selected for liquidity over the analyzed period. That historical selection is a limitation for extrapolation to a prospective investable universe.

The source reports observations from March 2, 1988 through December 27, 2008. Prices are restricted to the official 9:30 a.m.–4:00 p.m. session, described as 390 observations per day. Weekends, holidays, shortened or delayed sessions, days with missing values, and days with constant prices are removed. The methods text reports 5,226 retained trading days, exactly equal to the 2,740 estimation days plus 2,486 forecast days. Table 2 instead labels its descriptive sample as 5,229 observations. This three-observation difference is unresolved in the local source. The reported endpoint should also be treated as a source label pending the actual calendar file, rather than reconstructed by assuming every calendar date is a trading session.

The initial estimation window ends March 31, 1999. Forecast evaluation starts April 1, 1999. Models are reestimated every 22 trading days using the latest 2,740 observations; coefficients remain fixed between reestimations, while the conditional states are updated daily. Forecast horizons are one, five, and twenty days. The paper describes $k$-step-ahead covariance matrices, not cumulative $k$-day return covariances. A reproduction must keep those targets distinct: the covariance on day $t+k$ differs from the sum of daily conditional covariances over the next $k$ days.

Unconditional means are subtracted before quasi-maximum-likelihood estimation. The precise sample used to compute each demeaning constant is not specified sufficiently to settle whether it is recalculated in every rolling window. That choice should be logged because using a full-sample mean would introduce future information, even if its practical impact on volatility estimates were small.

The evaluation periods are:

| Period | Source date description | Observations |
|---|---|---:|
| Dot-com and aftermath | April 1999–March 2003 | 1,050 |
| Calm markets | April 2003–July 2007 | 1,080 |
| Financial crisis | August 2007–December 2008 | 356 |
| Full forecast sample | April 1999–December 2008 | 2,486 |

These divisions are retrospective descriptions of market conditions, not a documented real-time regime classifier. The paper's narrative also describes the last period as ending near the September–October 2008 crisis peak, whereas the full sample endpoint is stated as December 27. The observation counts sum correctly, but exact date alignment requires the original cleaned data.

## The 125-model universe

The comparison has 105 conditional-correlation models, 17 orthogonal models, and three BEKK-type specifications. The 105 models combine five correlation architectures with 21 marginal variance configurations. All assets within a configuration use the same model family and order, with asset-specific fitted parameters.

The five correlation architectures are constant conditional correlation (CCC), Engle DCC (DCCE), asymmetric DCC (DCCA), Tse–Tsui DCC (DCCT), and a DECO-based estimator. The 21 marginal configurations comprise two ARCH orders, one APARCH(1,1), six EGARCH combinations with $p\in\{0,1,2\}$ and $q\in\{1,2\}$, four GARCH combinations with $p,q\in\{1,2\}$, four GJR combinations with those same orders, and one each of HGARCH, IGARCH, FIGARCH, and RiskMetrics.

The orthogonal family uses the first 17 configurations: ARCH, APARCH, EGARCH, GARCH, and GJR, with the same order grid. It omits the four additional long-memory, integrated, and RiskMetrics specifications. The three remaining models are diagonal BEKK, scalar BEKK, and multivariate RiskMetrics. Fully unrestricted BEKK is excluded for computational tractability.

This enumerates the experiment but does not fully specify every univariate recursion. The source delegates detailed parameterizations to the cited literature and G@RCH 6 software. In particular, its EGARCH(0,1) label includes the asymmetric response relevant to the benchmark comparison; translating that order label into another package without checking its treatment of signed and absolute standardized shocks can change the model. Software order conventions, innovation normalization in APARCH/EGARCH, fractional truncation rules, parameter constraints, and starting values remain replication inputs.

### BEKK and targeting

The common BEKK equation is

$$
H_t=C+A\varepsilon_{t-1}\varepsilon_{t-1}'A'+BH_{t-1}B'.
$$

For diagonal BEKK, $A$ and $B$ are diagonal. For scalar BEKK, $A=aI$ and $B=bI$. Covariance targeting sets

$$
C=\bar H-A\bar HA'-B\bar HB',
$$

where $\bar H$ is the sample unconditional covariance target. This enforces the mean equation when the process is stationary; it does not automatically guarantee that $C$ is positive definite for arbitrary fitted matrices. An implementation must preserve the optimizer's admissible domain.

The source describes RiskMetrics with smoothing parameter $0.96$ and writes a restriction $a+b=1$ after defining $A=aI,B=bI$ in the quadratic BEKK expression. Those conventions cannot literally be combined: the coefficients multiplying covariance terms in BEKK are $a^2,b^2$. The conventional recursion consistent with a covariance smoothing weight of $0.96$ is

$$
H_t=0.04\,\varepsilon_{t-1}\varepsilon_{t-1}'+0.96H_{t-1},
$$

or $A=\sqrt{0.04}I,B=\sqrt{0.96}I$ in BEKK notation. This is an explicit reconstruction of the intended weighting convention; the local PDF does not expose executable code confirming how the authors implemented the notation.

### Orthogonal GARCH

Let $V$ contain unconditional marginal variances on its diagonal. Diagonalize the unconditional correlation matrix as $PLP'$, with orthogonal $P$ and diagonal eigenvalue matrix $L$. Define whitened factors and their diagonal conditional covariance by

$$
f_t=L^{-1/2}P'V^{-1/2}\varepsilon_t,\qquad
S_t=\operatorname{diag}(\sigma_{f1,t}^2,\ldots,\sigma_{fN,t}^2).
$$

Then

$$
H_t=V^{1/2}PL^{1/2}S_tL^{1/2}P'V^{1/2}.
$$

All ten components are retained; this is a rotation and conditional-diagonality restriction, not a low-rank approximation. Unconditional orthogonality alone does not prove conditional independence. The model assumes that the conditional factor covariance is diagonal and estimates each factor's volatility separately.

### Conditional correlation

Write $D_t=\operatorname{diag}(\sigma_{1t}^2,\ldots,\sigma_{Nt}^2)$ and $u_t=D_t^{-1/2}\varepsilon_t$. Engle DCC uses

$$
H_t=D_t^{1/2}R_tD_t^{1/2},\qquad
Q_t=(1-\alpha-\beta)\bar Q+\alpha u_{t-1}u_{t-1}'+\beta Q_{t-1},
$$

$$
R_t=\operatorname{diag}(Q_t)^{-1/2}Q_t\operatorname{diag}(Q_t)^{-1/2}.
$$

Here $\operatorname{diag}(Q_t)$ means the diagonal matrix formed from the diagonal entries. The target is the empirical second moment of standardized shocks. The paper itself notes that this familiar target is not exactly the population mean target implied by the nonlinear DCC normalization, while citing evidence that the resulting bias is small in the referenced setting.

DCCA adds a term driven by $n_{t-1}n_{t-1}'$, where $n_t=u_t\odot1_{\{u_t<0\}}$. To preserve a specified unconditional latent target, a corresponding subtraction of the mean asymmetric term would be required in the intercept. The main text mentions the additional term but does not fully print that targeted intercept or its positivity constraints. A replication should recover the actual software convention rather than silently use a different asymmetric-DCC implementation.

DCCT models correlations directly:

$$
R_t=(1-\theta_1-\theta_2)\bar R+\theta_1\Psi_{t-1}+\theta_2R_{t-1},
$$

$$
(\Psi_{t-1})_{ij}=
\frac{\sum_{m=1}^{K}u_{i,t-m}u_{j,t-m}}
{\sqrt{\sum_{m=1}^{K}u_{i,t-m}^2\sum_{m=1}^{K}u_{j,t-m}^2}},
\qquad K\ge N.
$$

The precise $K$ used is not supplied in the main text. CCC holds $R_t$ fixed. The DECO implementation is more subtle than its label: the authors estimate correlation dynamics under an equicorrelation simplification, then use the estimated dynamic parameters to forecast pair-specific correlations. The forecasts are therefore not constrained to have all off-diagonal entries equal.

Marginal variances are estimated first, followed by the correlation target and dynamic parameters. This staged procedure reduces computation, at a potential efficiency cost. The experiment uses quasi-likelihood and OxMetrics 6/G@RCH 6, not a claim that all models are correctly Gaussian.

## Realized targets and why the loss matters

For intraday log-return vectors $r_{t,j}^{(\Delta)}$, the basic proxy is

$$
\widehat\Sigma_t^{(\Delta)}
=\sum_jr_{t,j}^{(\Delta)}r_{t,j}^{(\Delta)\prime}.
$$

The primary interval is five minutes. One- and thirty-minute sampling provide robustness checks. A second proxy adds Bartlett-weighted lagged cross-products, described as a Newey–West-style realized kernel with $q=1$ in the empirical checks. Exact endpoint handling and the source's $q$ versus $q+1$ lag convention are not fully spelled out, so the code or the cited implementation is needed for exact reproduction.

The realized matrix estimates ex-post intraday variation; the conditional covariance forecast is its conditional expectation under suitable martingale and measurement assumptions. These are distinct objects even when both are called volatility. Higher-frequency measurement can reduce sampling noise but also increase nonsynchronous-trading and market-microstructure effects. The source reports some one-minute correlation attenuation and little evidence of it at five minutes or slower.

For a target $\Sigma$ and positive definite forecast $H$, the four losses are

$$
L_E=\|\operatorname{vech}(\Sigma-H)\|^2,\qquad
L_F=\operatorname{tr}\{(\Sigma-H)'(\Sigma-H)\},
$$

$$
L_S=\operatorname{tr}(H^{-1}\Sigma)-\log|H^{-1}\Sigma|-N,
$$

$$
L_b=\frac{\operatorname{tr}(\Sigma^b-H^b)}{b(b-1)}
-\frac{\operatorname{tr}\{H^{b-1}(\Sigma-H)\}}{b-1},\qquad b=3.
$$

Euclidean loss counts each distinct covariance once; Frobenius loss counts off-diagonal errors twice. Stein loss is scale invariant and strongly penalizes covariance underprediction in relative eigenvalue directions. Cubic loss weights large covariance levels more heavily and penalizes overprediction more strongly in the scalar comparison. A matrix need not overpredict another in every direction, so these descriptions do not establish a Loewner-order bias from a ranking alone.

For a scalar target of one, forecasts $0.5$ and $1.5$ have equal squared error $0.25$. Their Stein losses are approximately $0.30685$ and $0.07213$, while cubic losses are $0.08333$ and $0.16667$. This derived example makes the opposing asymmetry explicit. Multiplying all returns by $c$ multiplies covariance by $c^2$, quadratic losses by $c^4$, and cubic loss by $c^6$, while leaving Stein loss unchanged.

Robust ranking with a noisy proxy depends on conditional unbiasedness, not merely high sampling frequency. In these losses, the target-only nonlinear term cancels between competing forecasts; the remaining loss difference is affine in the target. If proxy error has conditional mean zero given forecast information, expected pairwise loss differences are preserved. Finite-sample rankings, standard errors, and test power can still change. The result does not guarantee immunity to biased proxies or validate an arbitrary intraday cleaning rule.

## MCS and SPA inference

For a current model set $\mathcal M$ of size $M$, let $L_{i,t}$ be the realized loss, $d_{ij,t}=L_{i,t}-L_{j,t}$, and $d_{i,t}=M^{-1}\sum_jd_{ij,t}$. The MCS tests equal expected loss within the current set. The paper uses

$$
t_i=\frac{\sqrt T\,\bar d_i}
{\sqrt{\widehat{\operatorname{Var}}(\sqrt T\,\bar d_i)}},
\qquad T_D=M^{-1}\sum_{i\in\mathcal M}t_i^2.
$$

A block bootstrap supplies the null distribution. If equality is rejected, the model with the largest $t_i$ is removed and the procedure is repeated. The stated settings are 10,000 bootstrap samples and block length two. The reported MCS threshold is $\alpha=0.25$. Although the paper sometimes calls $\alpha$ a confidence level, its algorithm describes a $(1-\alpha)$ confidence set; the retained-table cutoff is a p-value of about $0.25$.

Membership means failure to eliminate under this sequential procedure, not proof of equal predictive accuracy or a 75% posterior probability that each retained model is best. Sampling dependence matters, especially for multiple-step forecasts. The short block length is a reported design choice; the source does not present a sensitivity analysis proving its adequacy at every horizon.

The variance discussion contains a checked algebraic misprint. Since $\bar d_i=\bar L_i-\bar L$, the identity is

$$
\operatorname{Var}(\bar d_i)=\operatorname{Var}(\bar L)
+\operatorname{Var}(\bar L_i)-2\operatorname{Cov}(\bar L_i,\bar L)
$$

$$
=\operatorname{Var}(\bar L)\left[1+VR_i-2\sqrt{VR_i}\,\operatorname{Corr}(\bar L_i,\bar L)\right],
\qquad
VR_i=\frac{\operatorname{Var}(\bar L_i)}{\operatorname{Var}(\bar L)}.
$$

Printed equation (14) has a plus sign between the outside variance and the dimensionless bracket, where multiplication is required. The identity above follows directly from variance of a difference. Large relative variance or low correlation with the average loss can inflate the denominator and retain an inferior model. Statements that the worst model is removed presume rejection of the equal-loss null; without rejection, no elimination occurs.

For SPA, fix benchmark zero and define $d_{0j,t}=L_{0,t}-L_{j,t}$. Positive mean differences favor a competitor. The null is that no competitor has positive expected advantage; the statistic is a studentized maximum of the sample mean differences, with the standard nonnegative truncation used in SPA implementations. The paper prints the untruncated maximum and delegates bootstrap centering details to Hansen. It reports lower, consistent, and upper p-value variants, again with 10,000 bootstrap samples and block length two. Table 5 highlights non-rejection at the 10% significance threshold.

The displayed hypotheses concern expected loss differences. The broad introductory language describing these as conditional-predictive-ability tests should not be read as a test of equality conditional on every market state or instrument. Regime-specific results arise from splitting the evaluation sample.

## Main numerical results

For the full one-day sample, MCS sizes are 39 under Euclidean loss, 10 under Stein loss, and 20 under cubic loss. Frobenius results are not tabulated; the authors report similar rankings and a set contained in the Euclidean set. The full-sample leaders illustrate the change in objective:

| Loss | Smallest reported sample loss | Model | Retained models |
|---|---:|---|---:|
| Euclidean | 3.468 | Orthogonal GJR(2,1) | 39 |
| Stein | 3.496 | DCCT–IGARCH(1,1) | 10 |
| Cubic | 91.98 | Orthogonal GJR(2,1) | 20 |

Euclidean table losses are divided by $N(N+1)/2=55$ and cubic losses by $N^2=100$. Stein loss is reported without this division. These numerical levels are not directly comparable across loss functions. The source does not provide a complete return-unit specification sufficient to infer every raw loss scale solely from Table 2; percentage-return scaling is consistent with the descriptive magnitudes, but code should verify it.

Under Euclidean loss, orthogonal and DECO models dominate the retained full-sample set. Under Stein loss, every retained model belongs to a conditional-correlation family, frequently with integrated or fractionally integrated marginal variances. Orthogonal models perform well under cubic loss and poorly under Stein loss. The authors interpret that pattern as underprediction; it is suggestive objective-dependent evidence, not a direct signed matrix-bias test.

The main text reports dot-com MCS sizes of 38, two, and eight for Euclidean, Stein, and cubic losses. The Stein set contains DCCE–IGARCH and DCCT–IGARCH; the cubic set contains orthogonal models. During calm markets, the Euclidean set expands to 74 of 125 candidates and the Stein set contains 12, including ordinary CCC/GARCH specifications. During the crisis, sizes are 39, 26, and 26. The average Euclidean loss is described as about $2.7$ in the dot-com period, $0.3$ in the calm period, and $14.5$ during the crisis.

Those magnitudes explain why a short turbulent period can dominate full-sample quadratic evaluation. They do not establish a stable real-time switching strategy. The subgroup tables themselves reside in the unavailable supplement, so the reported counts and descriptions are not a substitute for recovering its complete model membership.

Proxy robustness is substantial but not exact invariance. For one-minute realized covariance, Euclidean MCS sizes are 25, 26, 60, and 47 across full, dot-com, calm, and crisis samples. With the one-minute adjusted proxy they are 35, 33, 71, and 38. At five minutes the adjusted-proxy sizes are 40, 30, 71, and 38. Thirty-minute raw sizes are 41, 41, 73, and 37, versus 40, 59, 66, and 35 for the adjusted version. Thus higher frequency does not uniformly shrink every set; the crisis raw one-minute count, for example, exceeds the primary count.

At five days, the full-sample Euclidean MCS contains 16 models, led by orthogonal GJR(1,1) with loss $4.300$. At twenty days it contains 12, led by orthogonal APARCH(1,1) with loss $5.020$. Orthogonal specifications dominate both lists. In the calm subsample, the main text reports only CCC–EGARCH(2,1) at five days and three retained models at twenty days. Greater separation of long-run targets and smoother forecast sequences are offered as explanations; shrinking MCS size is an empirical feature here, not a general horizon theorem.

## The benchmark conclusion requires qualification

The six SPA benchmarks cross CCC, DCCE, and orthogonal structures with GARCH(1,1) and EGARCH(0,1). For the preferred DCCE–EGARCH benchmark, the consistent p-values printed in Table 5 are:

| Evaluation sample | Euclidean | Stein | Cubic |
|---|---:|---:|---:|
| Full | .11 | .00 | .08 |
| Dot-com | .75 | .00 | .09 |
| Calm | .23 | .00 | .03 |
| Crisis | .04 | .23 | .04 |

At a 10% significance threshold, these results reject the no-superior-competitor null in many cells. Even at 5%, the Stein results for the first three periods and the crisis Euclidean/cubic results reject. Values printed as $0.00$ are rounded p-values, not proof of mathematical zero probability.

This directly qualifies the abstract and conclusion's blanket non-rejection language. A supported interpretation is that asymmetric DCCE is a useful parsimonious benchmark whose relative performance varies with loss and period. The table does not support universal dominance or universal non-rejection. Likewise, CCC–GARCH's calm-period consistent p-values are $.02,.82,.21$ across the three losses, so a generic claim that constant correlation cannot be rejected in calm markets must retain its loss-specific scope.

Some reported lower/consistent/upper triplets also violate their expected ordering, such as CCC–GARCH full-sample cubic values $.03,.02,.02$ and CCC–EGARCH crisis cubic values $.09,.02,.02$. These cells were checked visually. The note uses the explicitly labeled consistent p-values and leaves the anomalous bound labels unresolved rather than rearranging the table.

## What a faithful replication still needs

The local source specifies the architecture grid, rolling schedule, principal targets, loss formulas, and major inference settings. It does not supply cleaned intraday prices, corporate-action adjustments, exact retained dates, executable estimation code, optimizer tolerances, convergence/failure treatment, parameter starting values, state initialization, the DCCT window length, fractional-lag truncation, exact EGARCH order conventions, or the supplementary tables.

Multi-step DCC forecasts also require care: the expectation of a normalized latent matrix is not generally the normalization of its expectation. The paper does not detail whether its software uses a plug-in approximation or simulation for every nonlinear specification. A reproduction must document that convention and align each forecast with its target date, while excluding unavailable endpoint forecasts consistently across models.

The final comparison should retain loss sequences for every model, not only ranks. These permit independent checks of units, overlapping-horizon dependence, crisis contributions, the variance decomposition, and MCS elimination paths. All models must share target dates and proxies; selectively dropping failed forecasts changes the experiment.

The strongest practical lesson is methodological: compare a manageable model universe under economically interpretable covariance losses, preserve a common information set, and report uncertainty and regime sensitivity. The paper supports that workflow. Its results do not establish that a single historical winner will remain best, that non-rejection proves equal quality, or that statistical covariance accuracy translates automatically into a profitable portfolio.
