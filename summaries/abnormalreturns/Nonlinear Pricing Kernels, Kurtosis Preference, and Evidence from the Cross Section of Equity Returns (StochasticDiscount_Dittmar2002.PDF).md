# Nonlinear Pricing Kernels, Kurtosis Preference, and Evidence from the Cross Section of Equity Returns

## Source and scope

**Robert F. Dittmar**, *The Journal of Finance* 57(1), February 2002, pp. 369–403. Original file: [StochasticDiscount_Dittmar2002.PDF](../../Finance/StochasticDiscount_Dittmar2002.PDF).

The complete 35-page article was read, including references. Preference restrictions, conditional parameterizations, estimation equations, all eight tables, and all four figures were visually checked on PDF pp. 5, 8–9, 12–14, 16–17, 20, 22–23, and 25–28, 30–31. Several discrepancies between printed formulas, tables, and prose are identified explicitly below. This note reconstructs the econometric design and its reported evidence; it does not claim an independent replication using the original return and labor-income data.

## Why this matters

A linear pricing kernel restricts expected returns through covariance with a wealth proxy. A cubic kernel adds sensitivity to squared and cubed wealth returns, allowing assets' payoffs in asymmetric and extreme aggregate states to affect prices. Dittmar uses preference restrictions to motivate the signs of these terms, then asks whether nonlinear kernels explain industry returns better than a linear kernel or standard multifactor alternatives.

The empirical result has two parts that must stay together. When aggregate wealth includes a labor-income proxy, polynomial nonlinearities substantially reduce measured pricing distance, and some flexible specifications are not rejected. But their estimated shapes can increase in wealth over parts of the observed support. Imposing the economically important requirement that marginal utility fall as wealth rises materially worsens their fit, and the restricted models are rejected. The paper is therefore evidence for a tension between flexible statistical fit and an economically admissible kernel shape, rather than a clean validation of a four-moment equilibrium model.

For implementation, the most useful lesson is that coefficient signs do not enforce the global shape of a nonlinear kernel. A negative linear coefficient, positive quadratic coefficient, and negative cubic coefficient do not guarantee a positive, decreasing function. Nor does a low in-sample pricing distance establish that a labor-income proxy is a traded risk factor or that its extreme realizations support a robust investment signal. The paper's results are valuable as model diagnostics and as motivation for testing higher-order covariance exposures.

## Novelty and relation to earlier approaches

The paper lies between a tightly parameterized utility model and an unconstrained nonparametric pricing kernel. It uses a finite polynomial, stops at a preference-motivated order, and imposes alternating signs. This reduces the discretion involved in choosing a polynomial solely for fit. It still leaves substantial flexibility in conditional coefficient functions and in the treatment of human capital.

The third-order term is the distinctive addition to a variance-and-skewness model. Standard risk aversion, formulated through decreasing absolute risk aversion and decreasing absolute prudence, gives the derivative signs used to motivate a cubic approximation. A separate assumption discards the pricing contribution of higher powers. Preference theory supplies signs; it does not prove that the Taylor expansion terminates after the cubic term.

The human-capital exercise is equally central. Financial wealth alone gives little evidence that the cubic term improves fit. The substantial gains emerge when labor-income growth enters the proxy for aggregate wealth. This is consistent with higher-order dependence carrying information missed by a market return, but it also increases the importance of proxy construction, scaling, tail observations, and model specification.

## Economic setup and the preference argument

For asset $i$ with net return $R_{i,t+1}$, the conditional Euler equation is

$$
E_t[(1+R_{i,t+1})m_{t+1}]=1.
$$

A positive stochastic discount factor $m_{t+1}$ can be interpreted as a discounted marginal-utility ratio. In the static wealth representation used to motivate the approximation, expand marginal utility in the return on aggregate wealth $R_{W,t+1}$. Absorbing constants and expansion-point terms into coefficients yields

$$
m_{t+1}=d_0+d_1R_{W,t+1}+d_2R_{W,t+1}^2+d_3R_{W,t+1}^3.
$$

Increasing utility and risk aversion require $U'>0$ and $U''<0$. Define absolute risk aversion and absolute prudence by

$$
A(W)=-\frac{U''(W)}{U'(W)},
\qquad P(W)=-\frac{U'''(W)}{U''(W)}.
$$

Decreasing absolute risk aversion implies $U'''>0$ under these assumptions. The additional decreasing-prudence restriction is

$$
P'(W)=\frac{[U'''(W)]^2-U''''(W)U''(W)}{[U''(W)]^2}<0.
$$

Since $U''<0$, this inequality implies $U''''<0$. The corresponding Taylor coefficients alternate in sign:

$$
d_1<0,\qquad d_2>0,\qquad d_3<0.
$$

These are necessary sign implications of the preference argument, not sufficient conditions for every aspect of decreasing absolute risk aversion or prudence. A general cubic satisfying these signs need not be the exact marginal-utility ratio of a globally well-behaved utility function. It can become negative, and its derivative

$$
m'(R_W)=d_1+2d_2R_W+3d_3R_W^2
$$

can be positive over an interval. Both issues matter in the empirical estimates.

The truncation assumption is substantive. The paper explicitly assumes that covariances of asset returns with powers of aggregate wealth above the third are unimportant for pricing. The fact that the authors cannot sign higher derivatives from their chosen preference conditions does not imply those derivatives or their pricing effects are zero. Heavy-tailed data can make omitted higher-order terms especially consequential, and finite moments sufficient for the empirical criterion and its standard errors are also needed.

Taking unconditional expectations of the Euler equation gives

$$
E[1+R_i]=\frac{1}{E[m]}-\frac{\operatorname{Cov}(1+R_i,m)}{E[m]}.
$$

For fixed polynomial coefficients,

$$
\operatorname{Cov}(R_i,m)
=d_1\operatorname{Cov}(R_i,R_W)
+d_2\operatorname{Cov}(R_i,R_W^2)
+d_3\operatorname{Cov}(R_i,R_W^3).
$$

The second and third powers connect this representation to coskewness and cokurtosis after accounting for centering terms. They are not simply the asset's own skewness and kurtosis. A security matters because its payoff covaries with aggregate states, not merely because its standalone return distribution has a large fourth moment. With time-varying coefficients, the relevant covariances also involve the conditioning information; one cannot replace each coefficient by its mean without changing the model.

Kurtosis here motivates sensitivity to extreme outcomes. The fourth standardized moment is not a universal measure of bimodality, despite loose wording in the source. The reproducible object is the relevant cross moment or polynomial covariance, which should be stated and estimated directly.

## Conditional coefficients and information timing

Let $Z_t$ contain a constant and four lagged information variables. The sign-constrained specification in source equation (8) is

$$
m_{t+1}=(d_0'Z_t)^2-(d_1'Z_t)^2R_{W,t+1}
+(d_2'Z_t)^2R_{W,t+1}^2-(d_3'Z_t)^2R_{W,t+1}^3.
$$

The $d_j$ in this equation are parameter vectors, unlike the scalar coefficients in the preceding static expression. Squaring each linear index imposes the desired coefficient sign in every information state. It also makes the optimization nonlinear and creates sign-equivalent parameterizations: replacing a whole vector $d_j$ by $-d_j$ leaves its coefficient function unchanged. Standard errors and optimization diagnostics therefore need to respect local identification and the parameterization used for joint tests.

The four nonconstant instruments are the lagged excess return on the value-weighted CRSP market index, the CRSP dividend yield, the spread between Treasury-bill yields closest to three months and one month, and the return on the bill closest to one month. All information must be dated at $t$ when it multiplies the payoff at $t+1$. The distinction between a yield, a holding-period return, and an excess return is material; these series cannot be substituted without changing the regressors.

The use of conditioning variables has two separate effects. It creates managed-payoff moment restrictions, and it makes the kernel coefficients functions of information. A replication should preserve both. Estimating a static cubic and merely multiplying its pricing errors by instruments is a different model from the paper's conditional cubic.

A one-month Treasury bill is added to the 20 industry portfolios. Its moment restriction helps anchor the mean of the kernel to a risk-free pricing relation. For a gross return known at $t$, this is $E_t[m_{t+1}]=1/R_{f,t}$. Averaging this relation does not generally give the inverse of the average risk-free return. The bill therefore supplies more than another risky cross-sectional observation.

## Human capital and an unresolved printed specification

The market-only specification proxies aggregate wealth with a broad equity return. The human-capital version is motivated by an approximation

$$
R_W=\theta_0+\theta_1R_{vw}+\theta_2R_{lbr},
$$

where $R_{lbr}$ is constructed from per-capita labor income. Labor income is total personal income less dividend income, drawn from NIPA data through DataStream. The intended proxy is a smoothed growth measure with a one-month information lag.

There are two material printing ambiguities. Source equation (16) displays

$$
R_{lbr,t+1}=\frac{L_t+L_{t-1}}{L_{t-1}+L_{t-2}},
$$

without subtracting one. Its surrounding interpretation and reported small labor-return moments are consistent with a net growth rate, namely the displayed ratio minus one. The difference is not cosmetic when the variable is squared and cubed. Because conditional coefficient restrictions also matter, a researcher should obtain the original construction rather than treat the two conventions as automatically equivalent.

Second, source equation (17) prints the labor term with exponent $n-1$ inside a sum over $n=1,2,3$, whereas the tables and discussion label linear, quadratic, and cubic labor terms. It also displays an unsquared intercept function, unlike equation (8). The reported evidence is most naturally understood as a separable polynomial with corresponding market and labor powers, but the literal equation is not sufficient to reconstruct an unambiguous parameterization.

For a transparent reconstruction, one would explicitly declare the candidate basis

$$
1,\ R_{vw},\ R_{lbr},\ R_{vw}^2,\ R_{lbr}^2,
\ R_{vw}^3,\ R_{lbr}^3,
$$

and specify the intercept and signed coefficient functions separately. This is an operational interpretation, not a claim that the PDF proves this exact code was estimated. Cubing a linear aggregate-wealth proxy would also generate cross terms such as $R_{vw}^2R_{lbr}$ and $R_{vw}R_{lbr}^2$. The reported main specification omits such terms; the author says untabulated inclusion improves the results qualitatively. The separable polynomial is consequently an additional approximation to a literal cubic in total wealth.

## Estimation and distance interpretation

Let $G_{t+1}=1+R_{t+1}$ be the 21-vector of gross test-asset returns and let $Z_t$ be the five-vector of instruments. For parameters $\vartheta$, define

$$
h_{t+1}(\vartheta)
=[G_{t+1}m_{t+1}(\vartheta)-\mathbf1_{21}]\otimes Z_t,
\qquad
\bar h_T(\vartheta)=\frac1T\sum_t h_{t+1}(\vartheta).
$$

There are 105 unconditional moments. With market wealth alone, a degree-$j$ polynomial with five parameters per coefficient index has $5(j+1)$ parameters: 10 for linear, 15 for quadratic, and 20 for cubic. Human-capital terms add coefficient blocks; the exact count depends on resolving the intercept and exponent ambiguities above.

The paper minimizes a quadratic form

$$
\widehat\vartheta=\arg\min_\vartheta
\bar h_T(\vartheta)'W_{HJ}\bar h_T(\vartheta).
$$

The Hansen–Jagannathan weighting matrix is the inverse second-moment matrix of instrument-managed gross payoffs. Writing $X_{t+1}=G_{t+1}\otimes Z_t$,

$$
W_{HJ}=\left[\frac1T\sum_t X_{t+1}X_{t+1}'\right]^{-1}.
$$

The inverse is essential. Equation (14) and some captions print the payoff second moment without its inverse, while the explanatory text explicitly describes the inverse. Using the uninverted matrix would change the criterion and remove the stated distance interpretation. This is a source-document inconsistency confirmed visually, not an OCR correction made silently.

The square root of the minimized criterion is an SDF distance in the payoff-induced quadratic norm. It measures the smallest mean-square correction needed to turn the proxy into a kernel satisfying the tested linear pricing restrictions. Its units are kernel units, not percentage returns or an annualized Sharpe ratio. Because the weighting matrix depends on the test payoffs rather than on each model's pricing-error covariance, model comparisons do not mechanically reward a model for generating noisier errors. Sampling distributions still depend on the data-generating process and estimated parameters, so the minimized number is not automatically a conventional optimally weighted GMM chi-square statistic.

The source reports specification-test p-values and joint Wald tests for coefficient blocks, using heteroskedasticity/autocorrelation-consistent inference. It also mentions untabulated iterated-GMM checks. The underlying returns, instrument observations, exact numerical optimizer settings, and a complete executable inference procedure are not supplied in the PDF. A replication should retain the distinction between a block's marginal significance and the overall model's pricing adequacy.

## Sample and empirical design

The sample contains 390 monthly observations from July 1963 through December 1995. The 20 industry portfolios are **equally weighted**, formed from two-digit SIC classifications as in Moskowitz and Grinblatt (1999). They are not the standard modern Fama–French industry portfolios. Asset returns, market returns, dividend yield, bill yields, and the risk-free return come from CRSP; labor-income inputs come from NIPA through DataStream.

Table I reports returns in decimal monthly units. For example, utilities have mean 0.0097 and standard deviation 0.0368, corresponding to 0.97% and 3.68% per month. Electrical equipment has mean 0.0148 and standard deviation 0.0740. The nearby prose gives a different range of mean returns; the tabulated values should be retained as the numerical benchmark. A basis-point conversion is $0.0001=1$ basis point, so 0.0097 is 97 basis points, not 0.97 basis points.

Table II regresses each industry's next return on the four nonconstant instruments and jointly tests their coefficients. Most industries show evidence of predictability in this sample. Petroleum is an exception, with p-value 0.825; utilities have 0.074. These tests motivate including conditioning information, but they are in-sample joint tests across many portfolios and do not establish usable out-of-sample forecasts.

The estimation compares nested polynomial degrees, human-capital inclusion, Fama–French factor augmentation, a power-utility benchmark, and global shape restrictions. This design is informative because it distinguishes three changes that are otherwise easy to conflate: adding nonlinearity, changing the wealth proxy, and relaxing functional-form restrictions. It also creates multiple comparisons, so a single favorable p-value should not be treated as a complete model-selection result.

## Main results: where the nonlinear gains arise

Tables III–IV report the following HJ distances and specification p-values:

| Wealth proxy | Linear distance | Quadratic distance | Cubic distance |
|---|---:|---:|---:|
| Equity market only | 0.735 (0.000) | 0.709 (0.001) | 0.703 (0.000) |
| Including labor proxy | 0.719 (0.000) | 0.629 (0.100) | 0.578 (0.229) |

Parentheses contain the printed p-values. A printed 0.000 is rounded, not literally a probability of zero. The table-based p-value for the linear human-capital model differs from a prose value of 0.019; neither value supports acceptance at conventional levels.

With market wealth alone, adding a quadratic term reduces distance by roughly 3.5%, and adding the cubic reduces it only slightly further. The quadratic coefficient block is significant at 0.027, while the cubic block has p-value 0.654. All three models fail the overall specification test. This is weak evidence for a useful market cubic term.

With the labor proxy included, quadratic and cubic terms lower distance much more. The cubic's 0.578 distance is about 19.6% below the human-capital linear value of 0.719. The market cubic block is insignificant, with p-value 0.945, whereas the labor cubic block is printed as 0.000. The empirical importance of the cubic therefore comes primarily from the labor component, not a general statement that every third-order wealth exposure is priced.

The coefficient magnitudes also reveal a scaling issue. In Table IV's cubic model, the coefficient evaluated at mean instruments on the labor square is approximately 17,374.873 and on the labor cube approximately −72,319.964. These large numbers multiply very small powers of a decimal labor-growth proxy. They are not directly comparable with the coefficient on a monthly equity return, and they are not estimates of a constant relative-risk-aversion parameter. Changing labor growth from decimals to percent units changes squared and cubed regressors by factors of $10^4$ and $10^6$ respectively.

A nonrejected distance test does not establish the kernel's economic admissibility. The reported tests concern a finite asset/instrument menu. The subsequent shape checks show why the unrestricted sign-constrained model's apparent success cannot be interpreted as a complete utility-based explanation.

## Factor comparisons and the power-utility benchmark

Table V compares the polynomial kernels with a conditional Fama–French three-factor kernel and augments the nonlinear kernels with SMB and HML. The visually verified table reports the factor-only model's distance as 0.632 with p-value 0.008. The surrounding prose instead gives 0.714 with p-value 0.000. This discrepancy changes the apparent size of the nonlinear model's advantage: the human-capital quadratic distance of 0.629 is only slightly smaller than the table's factor-only value, while the cubic value of 0.578 is more clearly smaller.

The quadratic-plus-factor model has distance 0.588 and p-value 0.040. Its SMB block has p-value 0.005 and HML has 0.525. The cubic-plus-factor model has distance 0.555 and p-value 0.140, while SMB and HML block p-values are 0.621 and 0.941. Conditional on this sample, basis, instruments, and nonlinear specification, the additional factor blocks are not significant in the cubic model. This does not establish that size and value are economically redundant in all portfolios, nor that the cubic spans their realized returns.

The power-utility benchmark is

$$
m=a_0(1+R_W)^{-a_1},
\qquad
R_W=a_2R_{vw}+(1-a_2)R_{lbr}
$$

for the human-capital version. The weighted-combination form reduces numerical instability in the estimation. Without human capital, Table VI reports $a_0=1.014$, $a_1=3.963$, and distance 0.740. With human capital it reports $a_0=1.036$, $a_1=3.671$, $a_2=0.558$, and the same rounded distance 0.740. Both specifications are rejected. The human-capital parameters are very imprecise: reported p-values for $a_1$ and $a_2$ are 0.743 and 0.733.

The comparison is not fully matched in flexibility. The polynomial coefficient functions vary with instruments, whereas the power-utility parameters are fixed. The author addresses this partly with an untabulated fixed-coefficient cubic, reporting distance 0.634 versus 0.740 for power utility, approximately a 14% reduction. Even this is a comparison of different functional families and parameter counts, not a controlled claim that an additional moment alone causes all of the improvement.

## What the distance decomposition and figures show

If $\widetilde p$ is the minimum correction to an approximate kernel needed for tested pricing restrictions, the HJ distance decomposes as

$$
\|\widetilde p\|
=\sqrt{[E(\widetilde p)]^2+\operatorname{Var}(\widetilde p)}.
$$

Table VII shows that the correction's standard deviation dominates its mean. The market-only linear model has mean correction 0.0003 and standard deviation 0.7346. The human-capital cubic has mean correction 0.0017 and standard deviation 0.5779. Thus the cubic's improvement mostly reduces the variability of the correction required to price the asset menu; it does not come from a large reduction in the average correction.

There is another source inconsistency: Table VII's power row has distance 0.7836, whereas Table VI reports 0.740. The PDF does not reconcile this difference. It should not be averaged or silently substituted when reconstructing either table.

Figure 1 evaluates the coefficient functions at mean instruments and plots kernels over the observed market/labor return ranges. The nonlinear surfaces bend upward in some regions. These pictures directly motivate the additional shape restrictions. They are slices at a particular information state, not a complete verification of every realized conditional kernel, and a reconstruction should inspect the whole sample as well as the mean-instrument slice.

Figures 3–4 place model kernel means and standard deviations against an HJ volatility bound. The human-capital nonlinear kernels have substantially greater volatility than their market-only versions. The cubic can supply enough volatility in magnitude, yet its mean places the point outside the admissible bound. A finite-sample failure to reject a distance restriction and a point estimate outside a bound can coexist because these are different statistical diagnostics with sampling uncertainty. Neither graphic makes exact population pricing a demonstrated fact.

The labor series is much smoother in ordinary standard deviation: approximately 0.4% monthly versus 4.3% for the market. Its excess kurtosis is reported as 5.87 versus 2.70. This helps explain why its nonlinear powers can matter despite its low variance. It does not prove that kurtosis is the causal economic channel, and the influence of rare observations should be inspected before extrapolating the coefficients.

## Global shape restrictions and the central qualification

The paper next imposes nonnegativity of the kernel and nonpositivity of its derivative over the empirical return support. For a quadratic, the derivative condition is

$$
d_{1t}+2d_{2t}R_{W,t+1}\le0.
$$

For a cubic it is

$$
d_{1t}+2d_{2t}R_{W,t+1}+3d_{3t}R_{W,t+1}^2\le0.
$$

Source equations (24)–(26) implement restrictions through coefficient clipping. For example, the cubic coefficient is bounded above by

$$
d_{3t}\leftarrow\min\left\{d_{3t},
-\frac{d_{1t}+2d_{2t}R_{W,t+1}}{3R_{W,t+1}^2}\right\},
$$

and the quadratic case uses

$$
d_{1t}\leftarrow\min\{d_{1t},-2d_{2t}R_{W,t+1}\}.
$$

When this cubic constraint binds, source equation (25) additionally prescribes

$$
d_{1t}\leftarrow\min\{d_{1t},-d_{2t}R_{W,t+1}\}.
$$

The source cites Chen–Knez for implementing kernel nonnegativity during GMM estimation, without supplying executable constraint code. A faithful reproduction needs to document the order of these operations, behavior at zero returns, and their extension to both wealth proxies. Because the adjustment depends on the realized argument, simply differentiating an unclipped polynomial with fixed coefficients does not by itself verify the derivative of the resulting piecewise function. Author code or an explicit reconstructed piecewise definition is needed before claiming exact shape replication.

Table VIII reports restricted distances 0.698 for linear, 0.668 for quadratic, and 0.645 for cubic, with all three p-values printed as 0.000. The quadratic and cubic fit substantially worse than the corresponding less-restricted values 0.629 and 0.578. Figure 2 shows much flatter, nearly linear surfaces across most of the observed range, with stronger curvature principally at low labor returns.

Two comparison cautions are necessary. First, the restricted linear distance 0.698 is lower than the earlier 0.719. A genuinely nested restriction cannot improve an exactly minimized identical objective, so this points to an unresolved difference in numerical optimization or implemented parameterization. Second, the text says the globally restricted nonlinear models outperform the Fama–French model, but their distances 0.668 and 0.645 exceed Table V's 0.632. That prose claim agrees with its alternative factor distance 0.714, not with the printed table. The defensible result is the deterioration within the nonlinear specifications and their rejection under shape restrictions; the cross-model ranking is not unambiguous in this document.

## Reproduction protocol and missing inputs

A serious reconstruction should first resolve the labor-return convention, equation (17)'s exponents and intercept, and the table/prose discrepancies. Until then, different plausible implementations should be labeled separate reconstructions, not pooled as one exact replication.

1. Recover the 20 equally weighted SIC industry portfolios, monthly CRSP market/bill variables, and the historical NIPA per-capita income series. Match all 390 dates and document revisions, missing values, industry membership, and return conventions.
2. Build the lagged instrument matrix and the smoothed labor-growth proxy without using income information published after the portfolio date. The paper's calendar lag does not itself resolve modern real-time data-vintage availability.
3. Form the 105 moment series and the managed-payoff second-moment matrix. Check rank, conditioning, and the inverse weighting convention before optimizing any model.
4. Estimate each declared polynomial specification from multiple starting points. Preserve sign-equivalent solutions, objective values, gradient norms, and convergence diagnostics. Rescale regressors internally if needed, transforming coefficients back to the original decimal units for reporting.
5. Compute specification tests and joint coefficient-block tests with an explicitly stated long-run covariance estimator. Reproduce the printed distance tables before attempting new economic interpretations.
6. Inspect kernels and derivatives for every observed information state and across a clearly defined return grid. Separately report negative-kernel violations, increasing-kernel intervals, and the influence of tail observations.
7. Repeat with the declared global restrictions and verify that restricted minima cannot beat unrestricted minima when the objective and nested parameter spaces really are identical. This is a powerful numerical consistency check highlighted by the source's linear-model discrepancy.
8. For an extension rather than a historical replication, evaluate out-of-sample pricing errors and tail sensitivity. A positive, decreasing spline or another shape-preserving family could separate insufficient polynomial flexibility from the economic shape restriction; such an extension is not tested in this paper.

The PDF supplies source descriptions, formulas, coefficients evaluated at mean instruments, distances, p-values, and graphical diagnostics. It does not provide the full estimated coefficient vectors, original data files, data vintages, optimizer settings, or code resolving the ambiguous equations. Coefficients evaluated at average instruments are insufficient to regenerate the entire time series of conditional kernels. Exact replication therefore requires additional inputs even though the main economic and econometric mechanisms can be reconstructed.

## Limits and practical interpretation

The evidence concerns historical industry portfolios and a particular instrument set. It is not a result for individual stocks, transaction-cost-adjusted portfolios, live trading signals, or future samples. Labor-income growth is a proxy for human-capital returns, not a directly traded total-return series. Its smoothing and measurement can affect both higher moments and timing.

The higher-order terms depend strongly on extreme observations and on the chosen units. Coefficient significance does not remove uncertainty about the wealth proxy, the truncated expansion, or the global shape of marginal utility. Nonrejection of one flexible model also does not establish that the polynomial is structurally identified as representative-agent preferences.

The most durable contribution is the disciplined combination of preference-motivated signs, nonlinear pricing tests, and explicit shape diagnostics. The empirical success is qualified: labor-related nonlinearities improve pricing fit, while imposing a decreasing kernel exposes a substantial unresolved specification problem. A usable implementation should preserve that tension and the source's numerical ambiguities rather than promote the unconstrained cubic into a validated economic law.
