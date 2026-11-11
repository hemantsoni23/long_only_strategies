# The Arbitrage Pricing Theory and Multifactor Models of Asset Returns

Gregory Connor and Robert A. Korajczyk, Chapter 4 in R. Jarrow, V. Maksimovic and W. T. Ziemba, editors, *Finance*, Handbooks in Operations Research and Management Science, volume 9, Elsevier/North-Holland, 1995, pp. 87–144.

Source: [complete published chapter](../../Finance/APT_ConnorKorajczyk_1995.pdf), 58 PDF pages. References below use printed pages; add 86 to the PDF page number. The library also contains an annotated copy and the incomplete precursor `EmpiricalAPTFactorModels_ConnorKorajczyk_1993.pdf`. The latter stops during the opening factor-count discussion, with a detached formula on its final page. This note uses the complete 1995 publication, including the remaining empirical topics, applications, conclusion and references.

This is a research survey, not one newly estimated model. Numerical findings below are results the chapter reports from the cited studies, not independent replications. Its contribution is to connect the mathematical versions of the APT to the restrictions empirical researchers actually estimate, and to explain why seemingly similar tests disagree.

## Why this matters

A factor model can explain covariance extremely well while failing a test of expected returns. Conversely, a pricing restriction can escape rejection because its estimates are imprecise. These are different achievements. Connor and Korajczyk organize the literature around that distinction: return comovement, diversification of residual risk, pricing of factor exposures, and the statistical or economic assessment of pricing errors.

For an implementation, the main lesson is to write down exactly what is being asserted. A covariance model identifies a low-dimensional space of systematic shocks; it does not automatically identify economically named factors or prove that a finite set of assets has zero pricing errors. Approximate no-arbitrage restricts the aggregate size of pricing errors under large-market assumptions. Exact linear pricing requires stronger equilibrium conditions or an explicitly imposed finite-sample null. Many published empirical tests concern this stronger null.

The chapter also explains why practical decisions that look incidental can change the conclusion: daily versus monthly returns, asynchronous trading, how portfolios are formed, whether exposures are estimated before the test period, corrections for estimated betas, the covariance weighting of the second-pass regression, and the definition of a factor-mimicking portfolio. Reproducing an APT result therefore requires substantially more than applying principal components and regressing mean returns on loadings.

## 1. The return model and its identification

Let $r$ be the $n$-vector of one-period asset returns, $\mu=E[r]$, $f$ a $k$-vector of mean-zero factor innovations, and $\varepsilon$ residual returns. The basic representation is

$$
r=\mu+Bf+\varepsilon,\qquad E[f]=0,\qquad E[\varepsilon]=0,\qquad E[f\varepsilon']=0.
$$

Writing $\Omega=E[ff']$ and $V=E[\varepsilon\varepsilon']$ gives

$$
\Sigma=B\Omega B'+V.
$$

Here $B$ has $n$ rows and $k$ columns. For nonsingular $\Omega$, $B=\operatorname{Cov}(r,f)\Omega^{-1}$. These are projection coefficients; interpreting them as structural economic exposures requires additional identification.

### Strict versus approximate factor structure

A strict factor model makes $V$ diagonal. If individual residual variances are uniformly bounded and portfolio weights satisfy $\|w_n\|^2\to0$, then

$$
\operatorname{Var}(w_n'\varepsilon)
=w_n'V_nw_n
\le \max_i V_{ii}\,\|w_n\|^2\longrightarrow0.
$$

Equal weighting is one example, since $\|w_n\|^2=1/n$; the important condition is dispersion of weights rather than equal weighting itself. A portfolio can have many positions and still fail this condition if a few dominate its squared weights.

An approximate factor model permits residual correlation but keeps $\|V_n\|_{\mathrm{op}}$ bounded as $n$ increases. The same argument works with the operator-norm bound replacing the largest diagonal variance. Small industry blocks with bounded block size and bounded residual variances are an intuitive example. In contrast, residual exposures shared by an ever-growing fraction of the universe can create another pervasive factor and violate the bounded-residual condition.

After normalizing $\Omega=I_k$, pervasive factors require the smallest eigenvalue of $B_n'B_n$ to diverge. For $k$ equal-sized sectors with unit within-sector loadings, $B_n'B_n=(n/k)I_k$. The relevant diverging eigenvalues of $B_nB_n'$ are its $k$ nonzero ones, not all $n$ eigenvalues. The spectral characterization is that the leading $k$ covariance eigenvalues diverge while the remainder remain bounded. The full converse theorem in Chamberlain and Rothschild uses additional regularity, including a uniform positive lower bound on the covariance eigenvalues; the short survey statement should not be interpreted without those conditions.

Approximate factor structure is a second-moment restriction. Cross-sectional mixing or other distributional assumptions used to justify a law of large numbers or a central limit theorem are further assumptions, not automatic consequences of a bounded residual covariance spectrum. See §§2.1–2.4, pp. 88–92.

### Rotation, normalization and economic interpretation

For any nonsingular $k\times k$ matrix $L$,

$$
B^*=BL,\qquad f^*=L^{-1}f
$$

leaves returns unchanged. If expected returns are $\mu=\lambda_0\mathbf1+B\lambda$, the corresponding transformed price vector is $\lambda^*=L^{-1}\lambda$. Individual factor labels and their premia depend on normalization; the fitted expected-return vector does not.

Economic variables can fix an interpretable rotation only when they span the same factor space. An imperfectly correlated macroeconomic proxy introduces measurement error and potentially omitted-factor risk. It is not merely a change of coordinates. Likewise, comparing premia from separately estimated statistical models without aligning their rotations is generally meaningless.

There are visible normalization errors in the whitening illustration on p. 89. For implementation, if $V$ is positive diagonal, set $C=V^{-1/2}B$ after taking $\Omega=I_k$. Then

$$
V^{-1/2}\Sigma V^{-1/2}=CC'+I_n.
$$

If $J$ contains the leading normalized eigenvectors of this whitened covariance and their eigenvalues are $d_1,\ldots,d_k$, a valid loading matrix is

$$
B=V^{1/2}J\operatorname{diag}\!\left(\sqrt{d_1-1},\ldots,\sqrt{d_k-1}\right)Q,
$$

where $Q$ is orthogonal. The identity matrix is $n$-dimensional; the common eigenvalues are $d_j-1$, not squared total covariance eigenvalues. Returning to original asset units also requires the $V^{1/2}$ scaling. This is a reconstruction of the intended normalization, not a verbatim implementation of the printed display.

### Conditional models

The conditional analogue is

$$
r_t=E_{t-1}[r_t]+B_{t-1}f_t+\varepsilon_t,
\qquad
\Sigma_{t-1}=B_{t-1}\Omega_{t-1}B_{t-1}'+V_{t-1}.
$$

Conditional betas and factor covariances cannot both be freely time-varying and economically identified without restrictions. A time-dependent rotation can move variation between them. An implementation must specify which objects are fixed, parameterized by predetermined instruments, or estimated over rolling windows. Unconditional tests can fail even if an appropriate conditional relation holds, because averaging products of time-varying exposures and premia does not equal multiplying their unconditional means.

## 2. What no-arbitrage and equilibrium actually imply

### Exact pricing in a noiseless model

Project mean returns on the constant and loadings:

$$
\mu=\lambda_0\mathbf1+B\lambda+\eta,
\qquad \eta'\mathbf1=0,\quad \eta'B=0.
$$

With no residual uncertainty, a portfolio with weights $\eta$ has zero cost, zero factor exposure and certain payoff $\eta'\mu=\eta'\eta$. Unless $\eta=0$, that is an arbitrage. This argument requires a meaningful full-rank constant-and-beta design. If the constant is already in the factor loading span, a separately normalized zero-beta return needs special treatment. An available risk-free asset fixes the intercept under the usual convention.

### Approximate pricing in a large market

With residual uncertainty, use $w_n=\eta_n/(\eta_n'\eta_n)$. It has zero cost, no factor exposure and expected payoff one, while

$$
\operatorname{Var}(w_n'r_n)
=\frac{\eta_n'V_n\eta_n}{(\eta_n'\eta_n)^2}
\le \frac{\|V_n\|_{\mathrm{op}}}{\eta_n'\eta_n}.
$$

If aggregate squared pricing error diverges while residual covariance remains bounded, this sequence approaches a riskless positive payoff at zero cost. Excluding such asymptotic opportunities leads to a bound on aggregate squared errors, schematically

$$
\sum_{i=1}^n\eta_i^2\le C.
$$

It follows that average squared error is at most $C/n$, and at most $C/a^2$ assets can have $|\eta_i|\ge a$. It does **not** follow that every individual asset is exactly priced. A finite number of exceptional errors is compatible with the result.

Without a quantitatively specified bound, an approximate restriction on one fixed finite universe may be weak empirically: any finite vector has finite squared norm. This motivates the chapter's discussion of Shanken's testability criticism and of stronger equilibrium versions. Repackaging assets or using imperfect proxies also complicates attempts to treat an approximate result as a unique finite-dimensional pricing equation. See §§3.1–3.2, pp. 92–96.

### Why stronger equilibrium assumptions help

For an investor with optimal portfolio $w$ and normalized initial wealth, a first-order condition is

$$
E[u'(w'r)r]=\gamma\mathbf1.
$$

Substitution yields

$$
\mu=\lambda_0\mathbf1+B\lambda
-\frac{E[u'(w'r)\varepsilon]}{E[u'(w'r)]},
$$

where $\lambda_0=\gamma/E[u']$ and $\lambda=-E[u'f]/E[u']$. The residual term has a **minus** sign when derived from that first-order condition; equation (8) on p. 97 prints a plus sign. The sign does not change an argument establishing that the term vanishes, but it matters if one interprets a nonzero idiosyncratic risk premium.

If optimal wealth depends only on the factors and $E[\varepsilon\mid f]=0$, the numerator vanishes exactly. Conditional mean independence is stronger than the model's initial zero linear covariance condition. Other equilibrium arguments assume that optimal portfolios become well diversified, or impose preferences, endowments or production conditions that make the relevant residual premium small.

For quadratic utility, the residual term involves $Vw$. A valid useful bound is $|(Vw)_i|\le\|V\|_{\mathrm{op}}\|w\|$, or $|(Vw)_i|\le\sqrt{V_{ii}}\sqrt{w'Vw}$. The bound written near the bottom of p. 97 omits the square-root scaling needed for the displayed vector component. Bounded marginal-utility curvature and a sufficiently diversified portfolio can support the limiting argument; diversification does not follow just from calling an investor rational.

The survey also distinguishes an efficient combination of factor portfolios from the stronger claim that the factor portfolios span the entire mean-variance frontier. The CAPM singles out the market portfolio; multifactor restrictions typically assert that some combination is efficient. Dynamic extensions must confront time-varying return betas even when cash-flow loadings are fixed, maturity-specific bond risks, and nonlinear pricing kernels. None of these extensions automatically reduces to applying a static regression to a longer return history. See §§3.3–3.6, pp. 96–102.

## 3. Estimation and tests: a reproducible specification

### Cross-sectional premia and the two-pass procedure

Suppose $B$ is known and stable. In each period estimate

$$
r_t=\mathbf1F_{0t}+BF_t+\varepsilon_t.
$$

The factor coefficient is a realized factor return: in the elementary model $F_t=\lambda+f_t$. It is not the risk premium alone. Averaging through time estimates the unconditional premium under stationarity and suitable moment conditions.

With $X=[\mathbf1,B]$ and a positive-definite cross-sectional weighting matrix $W$,

$$
\widehat\theta_t=(X'WX)^{-1}X'Wr_t.
$$

The first row of this linear map defines a unit-cost zero-beta portfolio; the factor rows define zero-cost portfolios with unit exposure to their corresponding factor and zero exposure to the others. These identities follow from $(X'WX)^{-1}X'WX=I$. They require full column rank and unconstrained positions.

In practice betas are estimated in a first time-series pass. The second pass then uses noisy regressors. This creates errors-in-variables bias and changes the covariance of estimated average premia. Forming test portfolios can reduce exposure-estimation error, but can also reduce cross-sectional beta dispersion and power. Treating first-pass estimates as fixed is not generally justified. Time-series variation in the second-pass coefficients supplies the familiar Fama–MacBeth standard errors, while corrections for estimated betas remain necessary under the conditions discussed in the chapter. Serial dependence calls for an appropriate covariance estimator; that is an implementation requirement, not a claim that the chapter supplies a universal HAC formula.

A characteristic test augments the equation with predetermined $Z_{t-1}\delta$. The null is $\delta=0$ after conditioning on the specified exposures. Its rejection challenges the joint model—factor selection, estimated betas, constant or conditional pricing restrictions, and omitted state variables—not just the abstract existence of arbitrage-free prices.

### Statistical factors and factor-mimicking portfolios

Gaussian maximum-likelihood factor analysis fits a strict covariance model $\Sigma=BB'+D$, with diagonal $D$, by minimizing, up to constants,

$$
\log|\Sigma|+\operatorname{tr}(S\Sigma^{-1}).
$$

A replication must state centering, the covariance divisor, number of factors, rotation, starting values, convergence rule and handling of boundary or inadmissible uniqueness estimates. Classical unrestricted covariance estimation becomes problematic when the number of assets is large relative to the number of dates. The chapter explains why early studies broke universes into small groups and why later EM implementations could work with much larger cross sections.

For a chosen set of linear exposure and budget constraints $A'w=c$, minimum residual variance has solution

$$
w=V^{-1}A(A'V^{-1}A)^{-1}c,
$$

when the indicated inverses exist. This is a useful reconstruction of the optimization logic, not an assertion that every reviewed study used identical constraints. In particular, equation (24), p. 117, imposes unit budget and zero exposure to all factors other than the target; it does **not** fix the target exposure to one. Its factor-specific portfolio must not be silently confused with the zero-cost unit-exposure portfolio from the cross-sectional regression. A subsequent normalization or subtraction of a zero-beta portfolio changes that convention.

Asymptotic principal components instead diagonalizes the $T\times T$ matrix $R'R/n$, allowing the number of assets to exceed the number of periods. The leading eigenvectors recover a factor time-series space under large-cross-section restrictions on residual dependence and moments. Simplifications in which the residual contribution converges to a scalar identity involve restrictions on residual time dependence and time variation in variance. They do not follow solely from the word “approximate.” Statistical factor extraction also does not, by itself, provide an out-of-sample tradable portfolio.

### Time-series pricing, spanning and macroeconomic restrictions

For traded excess-return factors $F_t$, estimate

$$
R_t=\alpha+BF_t+\varepsilon_t.
$$

Exact pricing sets $\alpha=0$. For raw returns and raw factor-portfolio returns, a zero-beta formulation instead imposes $\alpha=\lambda_0(\mathbf1-B\mathbf1)$. Mean-variance spanning generally requires **both** a zero intercept and loading rows that sum to one. The chapter's equivalence language on p. 117 relies on its preceding pricing setup; neither restriction should be discarded in an unrestricted spanning test.

With observable mean-zero macroeconomic innovations, a joint model can be written $R_t=B\lambda+Bf_t+\varepsilon_t$. The nonlinear restriction is that the intercept vector lies in the column space of $B$. Iterated nonlinear seemingly unrelated regression estimates coefficients and premia together, imposing cross-equation restrictions rather than treating estimated exposures as known. A valid implementation must reproduce the macro innovation filters and observation timing, not simply substitute current raw levels of economic series. See §4, pp. 103–124.

## 4. Empirical evidence and the design choices behind it

### Early statistical-factor tests

Roll and Ross (1980) use daily returns on **1,260 firms from July 1962 through December 1972**, arranged alphabetically into **42 groups of 30**. They estimate five-factor maximum-likelihood models within each group and run generalized least-squares cross-sectional regressions. Both raw-return and excess-return specifications are considered, with a **6% annual risk-free rate** in the latter construction. As many as four factors have significant estimated premia.

A same-sample relation between mean returns and residual risk initially looks damaging. When return means, factor exposures and standard deviations are estimated on disjoint every-sixth-observation subsamples, only **3 of 42 groups** retain a significant standard-deviation relation. The chapter specifies interlaced date positions rather than three contiguous historical regimes. Separating estimation errors therefore materially changes the inference. A zero-beta-return equality test across 38 groups does not reject; factor premia themselves cannot be compared directly across separately rotated groups.

Shanken's asynchronous-trading analysis is particularly consequential: the corrected mean pairwise covariance is approximately twice the uncorrected value, and **97% of corrected covariances are higher**. Changes in factor portfolios are not simply harmless rotations. Daily data increase the number of observations while potentially worsening synchronization bias. Brown and Weinstein's split-group tests, using the same broad period and 1,260 stocks, find substantially more rejection of common pricing restrictions; the chapter reports rejection in about half the cases even after their posterior-odds adjustment. These results concern different maintained restrictions, not interchangeable tests of one universal null.

Chen (1983) uses four four-year intervals over **1963–1978**, with **1,064, 1,562, 1,580 and 1,378** firms. Ten statistical factors are extracted from the first 180 alphabetically ordered firms; five mimicking portfolios are constructed with no-short restrictions and a penalty against unequal weights. Odd dates estimate exposures and even dates supply cross-sectional observations. In a nonnested combination of APT and CAPM fitted returns, estimated APT weights range from **0.938 to 1.006**. Yet tests often reject both pure-model endpoint hypotheses. A weight near one is therefore not proof that the APT is exactly correct. The chapter does not supply the portfolio penalty calibration or a complete optimizer specification needed to reproduce these weights.

### Macroeconomic factors and the sensitivity of size results

Chen, Roll and Ross (1986) examine 20 size portfolios over **January 1958–December 1984**, using **60-month exposure-estimation windows**. Their five macroeconomic factors are industrial-production growth, unexpected inflation, changes in expected inflation, a low-grade corporate-bond versus long-government-bond return spread, and a long-government-bond versus Treasury-bill return spread. Industrial production enters with a one-month lead in the return-exposure measurement. This is a way to align news measurement; it cannot be read as an available ex ante trading signal.

Industrial production, unexpected inflation and the default-related spread are significant; the term-related spread is marginal. Market and consumption variables add little conditional on those factors. Oil is significant only in the **1958–1967** subperiod. Expected inflation is obtained from a particular inflation model, so reproducing “unexpected inflation” requires reproducing that filter and its information set.

Chan, Chen and Hsieh (1985) use each calendar year **1958–1977** as a test year and the preceding five years for estimation. Eligible NYSE firms exist at the beginning of the estimation interval and have prices at its end. Twenty portfolios are sorted by size at the **end** of that interval; their earlier returns are then used to estimate exposures. Monthly cross-sectional regressions are run in the next year. This construction differs from forming a historical portfolio using only information available at each historical date.

The reported average small-minus-large return is **0.956% per month**. Listed contributions include **0.453%** from the low-grade bond premium, **0.352%** from the market premium, **0.204%** from industrial production, and **0.120%** unexplained. These listed entries sum to **1.129%**, so they are not an exhaustive additive decomposition as presented; omitted factor contributions or further detail from the original study are required to close the identity. The unexplained small-minus-large difference is not statistically significant. A log-size characteristic becomes significant when market beta is included but not when only the prespecified macro exposures are used.

Shanken and Weinstein (1990) revisit this evidence over **1958–1983**, split into **1958–1967, 1968–1977 and 1978–1983**. They correct standard errors for estimated betas, consider 20, 60 and 120 portfolios, compare prior and contemporaneous exposure estimation, and restrict the premia of traded factors to their sample mean returns where appropriate. Crucially, they form portfolios each December and concatenate the subsequent annual return histories, rather than backfilling portfolios chosen at the end of a five-year interval.

With 20 portfolios, prior betas and unrestricted premia, none of the premia are significant at 5% in the subperiods; only industrial production is significant in the full period. More test portfolios improve precision, and market-premium significance can reappear under contemporaneous betas or restrictions on traded factors. The result is not that one specification conclusively wins, but that errors-in-variables corrections, information timing and restrictions have first-order effects on inference. See pp. 111–115.

### Large-cross-section time-series tests

Lehmann and Modest (1988) use **1963–1982**, divided into four five-year intervals. Firms must have complete daily observations within the interval; **750 stocks are randomly selected** in each block. An EM algorithm fits the full 750-by-750 covariance model. Models with **5, 10 and 15 factors** generate factor portfolios; **weekly** returns are then used in pricing tests. Five or twenty test portfolios are sorted on size at the start of the interval, prior-year dividend yield, or prior-year variance; zero-dividend firms receive a separate dividend group.

With five size portfolios, both CAPM and APT specifications reject at 5%. With twenty size portfolios, CAPM continues to reject while APT generally does not. The chapter explicitly treats loss of power as a possible explanation for this apparent improvement. Dividend-yield and variance portfolios are less damaging to the APT. The stronger hypothesis that the factor portfolios span the whole mean-variance frontier is strongly rejected. The complete-case and random-selection design must be replicated to compare numerical tests; it is not the same as using every currently available stock.

Connor and Korajczyk (1988a) use monthly **1964–1983** data in four five-year blocks, with **1,487, 1,720, 1,734 and 1,745** complete-history NYSE/AMEX stocks. Returns are in excess of one-month Treasury bills. They estimate five- and ten-factor models by asymptotic principal components and test ten equally weighted size portfolios, sorted at the beginning of each block, as well as individual securities. Portfolio residual covariance is unrestricted; individual-security tests permit residual correlation within three-digit SIC industry blocks.

Their test statistics use modified likelihood-ratio procedures with finite-sample Gaussian adjustments. The chapter points to the relevant distributional results rather than giving all computational details; substituting a generic asymptotic chi-squared statistic is not an exact replication. January dummies distinguish average pricing errors from seasonal effects.

The APT and value-weighted CAPM reject zero intercepts on size portfolios, while the equally weighted CAPM does not. January coefficients reject the market models more readily than the APT. APT regressions have typical explanatory power around **98%**, versus roughly **75%** for CAPM, producing much more precise intercept estimates. Thus a smaller but precisely measured APT error can reject while a larger, imprecise market-model error does not. Individual-stock tests provide less discrimination. This is a concrete example of why rejection frequency and economic model accuracy cannot be ranked mechanically.

### Joint estimation and Bayesian interpretations

McElroy and Burmeister (1988) analyze **70 stocks monthly from January 1972 through December 1982** using macroeconomic factors and iterated nonlinear SUR. All estimated premia except unexpected deflation are significant, and the cross-equation restrictions are not rejected. Their factor construction includes particular historical demeaning and market-residual conventions. Those conventions are part of the model; the chapter is insufficient to reconstruct every innovation series numerically.

Bayesian work by McCulloch and Rossi changes the question from a tail probability under an exact null to posterior odds or economic consequences of restrictions. In their analyses of the Connor–Korajczyk sample, a one-factor model is generally rejected unless priors are very diffuse, whereas a five-factor model is favored except under sufficiently informative priors. Prior sensitivity is evidence that likelihood information alone is limited, not a reason to report an unconditional posterior verdict.

Their utility-based comparisons also use **weekly NYSE/AMEX data from January 1, 1963 through December 31, 1987**, with ten size portfolios rebalanced monthly. Restricted zero-alpha and unrestricted models imply different certainty equivalents for an exponential-utility investor under normal returns. Posterior uncertainty is wide in five-year samples and tighter over the full sample. The chapter does not report enough utility calibration or numerical certainty-equivalent estimates to reproduce an economic value figure; none should be supplied by inference.

## 5. How many factors, and which ones?

The APT does not give an a priori number of priced factors. Under a strict Gaussian model, the chapter reports the factor-count likelihood-ratio statistic

$$
\left[T-1-\frac{2n+5}{6}-\frac{2k}{3}\right]
\log\frac{|\widehat\Sigma_k|}{|\widehat\Sigma|},
$$

with asymptotic chi-squared degrees of freedom $[(n-k)^2-n-k]/2$. Here $\widehat\Sigma_k$ is the constrained maximum-likelihood covariance and $\widehat\Sigma$ is unrestricted; the asymptotic regime is large $T$ at fixed $n$. Determinants, admissible model dimension and the small-sample correction all matter.

On p. 125 the survey says **32 of 42** Roll–Ross groups have five-factor test p-values below **0.50**, not 0.05. That reported threshold should not be silently converted into a conventional significance claim. Subsequent studies increase group size from 30 to 60, 120 and 180 and obtain more statistically significant factors. This can reflect additional weak covariance structure, finite-sample distortions when $n/T$ grows, or the attempt to fit an approximate model using a strict diagonal-residual model.

Brown's simulation argument shows why sample eigenvalues can be misleading: even when only a few population eigenvalues grow with universe size, finite-$T$ sample behavior can suggest either a dominant single factor or many factors. Tests based on whether added factors explain a diversified portfolio also retain finite-portfolio residual effects. Connor and Korajczyk's alternative uses changes in average residual variance as factors are added and finds roughly **one to six** statistical factors. Its asymptotic null concerns the limiting improvement; sample residual variance mechanically decreases when a component is added.

Characteristic models specify exposures from size, book-to-price, dividend yield or industry attributes. Such characteristics can be useful, but asserting that they span $B$ is an additional restriction. A return spread associated with a characteristic does not itself prove compensation for systematic risk. Lagged-return proxies, discussed through Mei's work, are also noisy loading proxies: spanning $k$ factor directions requires sufficiently many linearly independent realizations, not one arbitrary lagged-return vector. The chapter does not supply a single universally preferred factor-selection rule or a complete common tuning protocol. See §§5.1–5.2, pp. 125–129.

## 6. International tests and practical applications

International implementations must choose a return currency and distinguish common global risks, country-specific risks, and market segmentation. Equal prices of common risks do not imply that every country's assets have identical loadings or that local risks cannot be priced. Exchange-rate changes may be spanned by existing factors or introduce additional risks, depending on the maintained assumptions.

Cho, Eun and Senbet (1986) use **349 stocks from 11 countries, January 1973–December 1983**, and examine **55 country pairs** with interbattery factor analysis. At 5%, zero-beta-return equality rejects for **3 of 55 pairs**, common-premium equality for **30 of 55**, and the joint hypothesis for **32 of 55**. The method identifies factors common to each pair and cannot fully characterize country-specific factors. These overlapping tests are dependent; their counts are not 55 independent demonstrations of a particular segmentation mechanism.

Korajczyk and Viallet (1989) study France, Japan, the United States and the United Kingdom over **January 1969–December 1983**, with **4,211–6,692 securities** across estimation samples. Monthly domestic and international statistical-factor models are tested on size portfolios. Rejections are heavily influenced by the early period, particularly observations before February 1974. APT errors are generally smaller than CAPM errors, without a clear universal winner between domestic and international specifications.

Gultekin and coauthors compare **110 Japanese and 110 US stocks weekly over 1977–1984**, splitting around the December 1980 change in Japanese capital controls. Equal risk prices reject before but not after the change. Larger subsequent standard errors supply a power-based alternative to a pure integration interpretation.

Korajczyk and Viallet (1992) expand to **23,587 firms** in five countries over **January 1974–December 1988**, with approximately **8,010–11,659 firms per month**. Tests include currency-forward returns and lagged forward–spot spreads as conditioning variables. The joint zero-intercept and zero-predictability restrictions reject even though factors explain some of the variation. These studies show why unconditional equity-factor fit should not be extrapolated automatically to conditional currency pricing. The chapter's international section gives study architectures and comparisons, not all exchange-rate, forward-contract or data-cleaning inputs required for exact replication.

In performance evaluation, multifactor alpha measures abnormal performance relative to the specified benchmark. The chapter discusses **130 mutual funds, monthly January 1968–December 1982**, for which factor-estimation methods and the choice between risk-free and zero-beta conventions change rankings. More than five factors have less effect on rankings than the broader benchmark choice. Average estimated performance is negative. That observation combines manager behavior, fees, sampling error and benchmark specification; it is not a model-free causal estimate of skill.

For cost of capital, the operational formula is a zero-beta or risk-free rate plus exposures times factor premia. Both loading estimation and the imprecision of mean factor returns matter. For event studies, extra factors can reduce residual variance but add coefficient-estimation error. The cited simulation and empirical comparisons do not establish that more factors always improve power: benefits differ between diversified portfolios and individual securities. Many event-study uses require an adequate conditional expected-return benchmark rather than a test of the APT pricing restriction itself. See §5.3 and §6, pp. 129–136.

## 7. What a faithful reproduction can and cannot claim

A replication should freeze the asset universe and complete-history rules, observation frequency, currency and risk-free convention before choosing a factor estimator. It should record whether factor estimation is in-sample, preceding-window or rolling; whether test-portfolio memberships are historically investable; and whether factor proxies contain leads or full-sample fitted quantities. The different timing conventions in the studies above are substantive differences.

Next, specify the covariance model, number of factors, normalization and portfolio constraints. State the tested null explicitly: zero alphas, a zero-beta restriction, no incremental characteristic premium, common prices across groups, full mean-variance spanning, or factor-count sufficiency. These hypotheses do not have the same degrees of freedom or economic content. Align rotations before comparing individual statistical-factor premia.

Finally, report the size and units of pricing errors alongside uncertainty, covariance-fit statistics and test p-values. Corrections for estimated exposures, asynchronous trading and finite-sample distributions can reverse formal conclusions. An economically small rejection in a precise model can coexist with a large undetected error in a noisy one. Portfolio choices based on estimated expected returns add another layer of uncertainty that covariance fit alone cannot remove.

The chapter does not provide machine-readable data, exact return-cleaning rules for every study, all factor-innovation code, every optimizer setting, or full numerical tables of premiums and standard errors. It also does not establish investable net returns after turnover, borrowing constraints, spreads and market impact. Its strongest practical result is a framework for designing and diagnosing a multifactor asset-pricing experiment: approximate diversification logic, exact pricing restrictions, statistical identification, and economically relevant model comparison must be kept explicit throughout.
