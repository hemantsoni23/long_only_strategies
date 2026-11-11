# Asset Pricing at the Millennium

John Y. Campbell, *The Journal of Finance* 55(4), August 2000, pp. 1515–1567. Source: [AssetPricing_Campbell_2000.pdf](../../Finance/AssetPricing_Campbell_2000.pdf), 53 pages. This note covers the complete survey, including its footnotes and references. Printed page $p$ corresponds to PDF page $p-1514$. The paper has no separate empirical appendix, original regression tables, or figures. Numerical evidence is attributed to the studies and samples identified in the survey, not to a new Campbell 2000 dataset.

## Why this matters: one set of restrictions for several kinds of evidence

Campbell organizes asset pricing around a stochastic discount factor, or SDF, that values every traded payoff. This creates a common language for equity-premium evidence, the term structure, cross-sectional factor models, long-horizon portfolio choice, consumption-based equilibrium, heterogeneous households, and behavioral models. The distinctive contribution is the synthesis: a model explaining stock returns must also face restrictions from interest rates, consumption, and investors' intertemporal choices. Success in fitting one collection of average returns is insufficient.

The survey separates restrictions that follow from no arbitrage from restrictions requiring economics. Existence of a positive SDF is broad and by itself explains little. Economic content enters when its conditional mean, volatility, dependence on state variables, and relation to marginal utility are specified. Stock-market risk premia require a volatile SDF; stable short real rates require a comparatively stable conditional mean; cross-sectional returns identify the directions of risk that covary with it. Matching all three disciplines a model more sharply than any one statistic.

This is a record of the field around 2000, not a statement about the current empirical status of every anomaly or model. Campbell's scope is primarily U.S. risk–return relations. Asymmetric information, corporate finance, microstructure, international finance, most derivatives, and most continuous-time technical developments are explicitly outside the survey. The replication objective is therefore to reconstruct its equations and diagnostic experiments while identifying where the underlying cited papers are needed for full implementation.

## The basic pricing equation and its assumptions

Let $P_{it}$ be an asset's price known at time $t$, and $X_{i,t+1}$ its random next-period payoff, including any dividend and resale value. Under the no-arbitrage setting discussed in Section I, a positive random variable $M_{t+1}$ satisfies

$$
P_{it}=E_t[M_{t+1}X_{i,t+1}].
$$

In a finite-state interpretation, $M$ equals state price divided by physical probability. Complete markets make this SDF unique; incomplete markets generally leave multiple SDFs that agree on the span of traded payoffs. A zero-cost strategy is handled directly by the price–payoff equation and should not be assigned a return by division through zero.

For a nonzero-price asset, define gross return $G_{i,t+1}=X_{i,t+1}/P_{it}=1+R_{i,t+1}$, where the paper uses $R$ for net return. Then

$$
1=E_t[M_{t+1}G_{i,t+1}].
$$

An unconstrained investor with time-separable utility and discount parameter $δ$ supplies a candidate SDF

$$
M_{t+1}=\delta\frac{U'(C_{t+1})}{U'(C_t)}.
$$

This follows from equating the marginal utility cost of buying an extra unit with its expected marginal utility payoff. It applies to assets the investor can trade freely at an interior optimum. Binding constraints generally change equality conditions into inequalities; consumption of a nonparticipating household cannot automatically be substituted into the same equality.

If a conditionally risk-free gross real return $G_{f,t+1}$ exists,

$$
E_t[M_{t+1}]=1/G_{f,t+1},\qquad
E_t[R^e_{i,t+1}]=-\frac{\operatorname{cov}_t(M_{t+1},R^e_{i,t+1})}{E_t[M_{t+1}]},
$$

where $R^e_i=R_i-R_f$. A payoff performing poorly when marginal utility is high needs a positive premium. Its standalone variance is not the relevant risk measure; covariance with the SDF is.

The distinction between real and nominal matters. With price level $Q_t$, the nominal SDF is $M^N_{t+1}=M_{t+1}Q_t/Q_{t+1}$. Nominal bills are not literally risk-free in consumption units; realized inflation creates real risk. Even indexed bonds can have an indexation lag. The survey treats short nominal bills as a practical proxy when inflation uncertainty is small, while acknowledging that it is an approximation.

## Mean–variance bounds and what the data imply

Cauchy–Schwarz applied to the excess-return equation gives

$$
\frac{\sigma_t(M_{t+1})}{E_t[M_{t+1}]}
\geq\frac{|E_t[R^e_{i,t+1}]|}{\sigma_t(R^e_{i,t+1})}.
$$

Taking the maximum over feasible portfolios gives the tightest Sharpe-ratio bound. Hansen–Jagannathan extend the analysis to multiple risky assets without requiring an observed riskless asset, tracing the minimum possible SDF variance against its assumed mean. The minimum-variance kernel is a linear combination of payoffs and a constant in the unrestricted projection problem; requiring strict positivity can strengthen the bound. Those are distinct restrictions and should not be conflated.

The unconditional version follows by taking unconditional expectations of the original pricing equation. Its mean kernel is $E[1/G_f]$, not $1/E[G_f]$. Conditional moments cannot simply be replaced by averages without preserving this nonlinear distinction. Predictive instruments can also construct managed portfolios, increasing exposure when expected returns are high. If their feasible Sharpe ratio is greater, the SDF bound tightens. In a reproducible test, instruments must be observed before the return interval, and an in-sample optimized managed portfolio should not be described as an out-of-sample investment result.

For quarterly U.S. data over 1947Q2–1996Q4, the survey quotes a mean log real bill return of 0.8% per year and annualized standard deviation 1.76%, perhaps half of the latter reflecting ex post inflation surprises. Equity has an annualized Sharpe ratio near 0.5. Thus an SDF with mean near one needs annualized volatility on the order of 50%. Aggregate consumption-growth volatility is approximately 1%, making ordinary power-utility marginal utility far too smooth unless risk aversion is very large.

The number 50 is an optimistic curvature scale based on kernel volatility: actual pricing also requires the right correlation with returns. A kernel with enough variance but poor alignment with payoffs can still fail. More frequent observations improve measurement of some moments but do not substitute for more calendar time when estimating a mean return. Selection of successful national markets and unobserved catastrophic states complicate historical inference. A disaster explanation for the stock–bill premium specifically requires sufficiently different effects on equities and short debt; a catastrophe destroying both equally need not explain their spread.

Under conditional joint lognormality, writing $m=\log M$ and $r_i=\log G_i$ yields useful exact relations:

$$
r_{f,t+1}=-E_t[m_{t+1}]-\frac12\operatorname{var}_t(m_{t+1}),
$$

$$
E_t[r_{i,t+1}]-r_{f,t+1}+\frac12\operatorname{var}_t(r_{i,t+1})
=-\operatorname{cov}_t(r_{i,t+1},m_{t+1}).
$$

The own-variance term is the Jensen correction. A log expected excess return and an arithmetic expected excess return are different quantities. The distributional assumption is essential: these log relations are not exact for an arbitrary return distribution.

## Predictability as an empirical restriction

The return-predictability evidence summarized in Section I.A.4 is more specific than the statement that valuation ratios matter. For the postwar quarterly U.S. sample described in Campbell (1999), regressions on log dividend yield have reported explanatory power around 2% at a monthly return horizon, 18% annually, and 34% over two years. These numbers concern different cumulative horizons; they do not imply a 34% monthly forecasting fit. Longer horizons magnify the cumulative effect of persistent expected returns while reducing the number of effectively independent observations.

A replication must distinguish two inference problems. Overlapping returns induce serially dependent regression errors even when underlying one-period innovations are independent. Persistent predictive variables whose innovations covary with returns create additional small-sample bias even without overlap. A conventional heteroskedasticity correction alone addresses neither problem fully. Campbell cites alternative long-overlap asymptotics and Monte Carlo corrections rather than presenting a new chosen estimator. He characterizes the evidence as statistically meaningful but not overwhelming, and notes that the late-1990s run-up weakened conventional mean-reversion evidence.

Candidate predictors include past returns, dividend and earnings yields, book-to-market, payout ratios, the equity share of new financing, long–short and credit yield spreads, short-rate changes, and consumption relative to income and wealth. They are alternative information variables discussed across studies, not one predetermined multivariate specification fitted in this survey. Many also track the business cycle. The economically central finding is that expected returns and volatility do not move proportionately: conditional Sharpe ratios appear countercyclical. A model with a fixed price of risk and only changing volatility can consequently miss an important dimension of the evidence. To test that dimension, estimate conditional means and second moments on a common information set and sample, preserve their joint estimation uncertainty, and then examine the implied conditional reward-to-risk ratio. That is the methodological implication of the surveyed GMM work, not a newly reported calculation in this article.

## Conditional factors and cross-sectional interpretation

Suppose the SDF is conditionally linear in zero-mean, mutually orthogonal factors:

$$
M_{t+1}=a_t-\sum_{k=1}^K b_{kt}f_{k,t+1}.
$$

Let $β_{ikt}=\operatorname{cov}_t(R^e_i,f_k)/\operatorname{var}_t(f_k)$. Then

$$
E_t[R^e_i]=\sum_k\beta_{ikt}\lambda_{kt},\qquad
\lambda_{kt}=\frac{b_{kt}\operatorname{var}_t(f_k)}{a_t}.
$$

Campbell's equation (8) labels the covariance numerator's component $b_{kt}\operatorname{var}_t(f_k)$ as a risk price before division by $E_tM=a_t$ through equation (5). The normalization above makes $λ$ directly a contribution to expected excess return. With correlated factors, use the full factor covariance matrix rather than separate univariate covariance ratios.

A conditional factor model does not generally imply the same unconditional factor model. Time variation in $a_t$, $b_t$, factor moments, and exposures introduces additional unconditional covariances. If coefficient functions are linear in a predetermined instrument vector $z_t$, an unconditional representation includes original factors, instruments, and products $z_t f_{t+1}$. Omitting the interaction terms is an additional restriction, not a harmless shortcut. This is the central rationale for scaled factor models.

Section I.B discusses size, value, and momentum. Small stocks earn higher average returns than their market betas alone explain; high book-to-market stocks outperform low book-to-market stocks; recent winners over roughly three to twelve months continue to outperform, whereas longer-horizon losers can reverse. Three-factor market–size–value models and momentum augmentation summarize those patterns, but a useful factor is not automatically an identified economic risk.

Campbell distinguishes data snooping, inadequate market proxies, conditional-model effects, genuinely additional priced risks, transient mistakes, and persistent biased expectations. Human capital is a major omitted component of aggregate wealth: labor income is roughly two-thirds of U.S. GDP. That motivates additional proxies but does not make labor-income growth an exact return on human wealth. A “distress” label similarly requires an explanation of why distress covaries with marginal utility and why its price is sufficiently large.

Momentum is particularly difficult to obtain from a simple varying-discount-rate story that readily produces value. Evidence favoring one mechanism needs additional implications, such as behavior around earnings announcements, exposure to state innovations, or changes after an effect becomes widely known. The survey does not supply the stock screens, accounting lags, portfolio breakpoints, rebalancing rules, or covariance estimation choices needed to recreate the original anomaly studies; those must be recovered from the cited research rather than inferred here.

## Prices, cash flows, and discount-rate news

A constant expected gross return implies the familiar present-value relation after imposing a vanishing expected discounted terminal price. Constant expected dividend growth then gives a Gordon formula. Applying that formula while allowing its supposedly constant growth and discount rates to change is a heuristic comparative exercise, not a fully dynamic model.

The Campbell–Shiller log-linearization begins with the identity $G_{t+1}=(P_{t+1}+D_{t+1})/P_t$. Let lowercase denote logarithms, and set

$$
\rho=\frac1{1+\exp(\overline{d-p})},\qquad
k=-\log\rho-(1-\rho)\log(1/\rho-1).
$$

Then $r_{t+1}\approx k+\rho p_{t+1}+(1-\rho)d_{t+1}-p_t$. Iteration with $\rho^j(p_{t+j}-d_{t+j})\rightarrow0$ gives

$$
p_t-d_t\approx\frac{k}{1-\rho}+
E_t\sum_{j=0}^{\infty}\rho^j(\Delta d_{t+1+j}-r_{t+1+j}).
$$

This is accounting plus approximation and a terminal restriction, not a behavioral theory. In the quoted postwar data, an annual price/dividend ratio of 26.4 suggests annual $ρ\approx0.964$. Mixing an annual calibration with quarterly dividend units would change the discounting weights and is a replication error.

Unexpected returns decompose as

$$
r_{t+1}-E_t r_{t+1}=N_{CF,t+1}-N_{DR,t+1},
$$

$$
N_{CF,t+1}=(E_{t+1}-E_t)\sum_{j=0}^{\infty}\rho^j\Delta d_{t+1+j},\qquad
N_{DR,t+1}=(E_{t+1}-E_t)\sum_{j=1}^{\infty}\rho^j r_{t+1+j}.
$$

Positive cash-flow news raises today's price; higher required future returns lower it. Persistent revisions in required returns can therefore create substantial current volatility. With these definitions, variance equals $\operatorname{var}(N_{CF})+\operatorname{var}(N_{DR})-2\operatorname{cov}(N_{CF},N_{DR})$. The prose on p. 1532 says “plus” covariance; that only works if discount-rate news is redefined as its negative price contribution. The equations' sign convention should govern an implementation.

A practical implementation needs a forecasting system, typically a vector autoregression, to compute expectation revisions and infinite sums. The survey does not select a unique state vector, lag order, sample, or residual assignment for that decomposition. Those choices materially affect measured news and must be declared. A decomposition of model-based forecasts is not direct observation of investors' beliefs.

Payout accounting must also be consistent. On a per-share basis, use per-share prices and ordinary dividends; repurchases affect future dividends per remaining share. On a total-firm basis, use total equity value and net cash paid to shareholders, including repurchases and subtracting issuance. Executive option exercises can create offsetting issuance. The survey quotes an approximately one-percentage-point addition to late-1990s S&P 500 dividend yield from net repurchases. Non-dividend-paying firms approached one-quarter of market value in 1993–1997, making a stable dividend process inappropriate for many individual firms. Clean-surplus residual-income valuation is an alternative, but it requires consistent book-value and earnings accounting.

## Bond pricing and why stock-only calibration is inadequate

For a real zero-coupon bond paying one unit of consumption after $n$ periods,

$$
P_{n,t}=E_t[M_{t+1}P_{n-1,t+1}],\quad P_{0,t}=1,
\qquad
P_{n,t}=E_t\prod_{j=1}^nM_{t+j}.
$$

The log yield is $y_{n,t}=-\log P_{n,t}/n$. Bond prices therefore identify the time-series behavior of the SDF, not only its one-period moments. An affine-yield model specifies a state process whose conditional distribution has an exponential-affine transform, allowing log bond prices to be affine in states and their coefficients to be solved backward from maturity. Affine conditional means and variances plus appropriate distributional restrictions are sufficient in the examples discussed; affine moments alone do not establish an affine transform for arbitrary distributions.

The survey describes Gaussian constant-volatility and square-root-style models, multifactor extensions, and the constraints imposed by covariance-matrix admissibility. State-dependent variances must remain nonnegative; a naïve discrete Gaussian approximation to a square-root process can leave its admissible region and should not be treated as an exact implementation. Coupon bonds are sums of zero-coupon claims. Nominal models require the nominal SDF or a joint inflation–real-kernel model.

The numerical evidence quoted from zero-coupon yields estimated from Treasury coupon prices covers January 1952–February 1991. Average log-yield spreads over one-month bills are 33 basis points at three months, 77 at one year, 96 at two years, and 137 at ten years. The yield curve is steep at short maturities and progressively flatter thereafter. The 137-basis-point yield spread can proxy for an expected term premium only under the source's no-expected-long-run-drift qualification; realized long-bond excess returns over this particular period were negative because rates rose.

Yield and forward spreads predict future excess bond returns, contradicting a constant-term-premium expectations hypothesis. High spreads predict rising short rates but falling long rates in the postwar evidence summarized. A one-factor constant-volatility Vasicek model has constant term premia. A one-factor square-root model can vary premia, but the source describes an incorrect sign relating them to the yield spread when average premia are positive. Multiple persistent and transitory states help reconcile slow rate autocorrelation decay with the curvature of average yields.

Treasury-bill Sharpe ratios can look large despite tiny premiums because their excess-return volatility is also tiny. Transaction costs, liquidity services, and portfolio restrictions can then be decisive. Campbell insists that an equity-premium explanation based on bill liquidity also account for long bonds: depressing only the short safe rate tends to imply a large long–short spread, which is not the same phenomenon as a large equity premium.

## Long-horizon portfolio choice: preferences, hedging, and learning

For a one-period investor consuming terminal wealth, the optimal payoff is an inverse marginal utility function of the SDF, $X^*=U'^{-1}(M/θ_t)$, where the known multiplier enforces the budget constraint. In a multiperiod setting, the analogous conditions hold across consumption dates, but determining portfolio weights requires dynamic trading opportunities and state dynamics.

Myopic choice is a special case. For an investor without labor income and with standard time-separable utility, log utility or power utility with IID returns gives sufficient conditions. Otherwise, changes in future investment opportunities create hedging demands in addition to the current mean–variance trade-off. A short safe asset is not necessarily safe for a long consumption horizon because it must be rolled over at uncertain rates. A real zero-coupon bond maturing at a fixed terminal consumption date is safe for that particular payment; a stream of consumption requires a corresponding duration structure.

Epstein–Zin preferences separate relative risk aversion $γ$ from elasticity of intertemporal substitution $ψ$. A standard equivalent form of equation (16) is

$$
U_t=\left[(1-\delta)C_t^{1-1/\psi}
+\delta\left(E_tU_{t+1}^{1-\gamma}\right)^{(1-1/\psi)/(1-\gamma)}
\right]^{1/(1-1/\psi)}.
$$

With $θ=(1-\gamma)/(1-1/\psi)$ and gross return $G_{p,t+1}$ on the investor's total wealth portfolio, the standard implied kernel is

$$
M_{t+1}=\delta^{\theta}(C_{t+1}/C_t)^{-\theta/\psi}G_{p,t+1}^{\theta-1}.
$$

The prose after equation (16) prints an unexponentiated discount factor; the displayed preference recursion requires the $δ^{\theta}$ normalization used here. Limit cases such as $ψ=1$ or $γ=1$ should be taken analytically rather than evaluated through an undefined ratio. Time-separable power utility is the case $γ=1/ψ$. In this framework portfolio choice can be myopic at $γ=1$ even when $ψ$ differs; at $ψ=1$ the consumption/wealth ratio is constant, but hedging demand generally remains.

If stock returns are negatively correlated with innovations to their expected premium, stocks hedge deteriorating future investment opportunities: they pay well when expected future returns fall. The models surveyed then increase equity demand for investors with risk aversion above one. This result assumes a known return process and does not justify unconditional buy-and-hold advice. Investors also time their exposures as expected returns change, and not everyone can simultaneously follow the same aggregate buying rule in equilibrium.

Learning can reverse the hedge. If a positive realized return raises the estimated long-run mean, current returns and revisions to future opportunities become positively correlated. For conservative long-horizon investors this can lower stock demand. Model uncertainty is therefore not a small cosmetic adjustment to a known-parameter strategy.

Labor income changes effective exposures too. Riskless labor income resembles an implicit safe asset and can tilt financial holdings toward equities; income highly correlated with equity resembles an implicit risky holding and does the opposite. Unhedgeable income risk encourages precautionary saving and can reduce risk-taking. Flexible labor supply provides another adjustment margin. The survey reports qualitative implications of calibrated life-cycle models but does not provide their transition matrices, retirement rules, borrowing constraints, tax schedules, or policy grids, so no unique allocation path can be reproduced from this article alone.

## Equilibrium mechanisms and their distinct failures

A representative-agent power-utility economy with exogenous aggregate consumption has $M=\delta(C_{t+1}/C_t)^{-\gamma}$. It faces three separate puzzles: the equity premium is too high for ordinary curvature and smooth consumption; stock returns are too volatile; and raising curvature can produce an implausibly high risk-free rate because it simultaneously reduces intertemporal substitution.

In the homoskedastic lognormal endowment case where dividends equal consumption, the survey derives

$$
r_{e,t+1}-E_t r_{e,t+1}
=(\Delta c_{t+1}-E_t\Delta c_{t+1})
+(1-\gamma)(E_{t+1}-E_t)\sum_{j=1}^{\infty}\rho^j\Delta c_{t+1+j}.
$$

With IID consumption growth, the news about future growth vanishes, leaving stock innovations as smooth as current consumption. With predictable growth, higher expected cash flows and higher discount rates can offset, exactly at $γ=1$ in this expression. This explains why fitting a large average premium alone does not solve volatility.

Difference habit introduces $S_t=(C_t-X_t)/C_t$, local curvature $γ/S_t$, and

$$
s_{t+1}=(1-\phi)\bar s+\phi s_t+\lambda(s_t)\epsilon_{c,t+1},
\quad
M_{t+1}=\delta(S_{t+1}/S_t)^{-\gamma}(C_{t+1}/C_t)^{-\gamma}.
$$

A sensitivity function decreasing with surplus consumption makes kernel volatility and the price of risk countercyclical. In the Campbell–Cochrane calibration, precautionary saving offsets intertemporal substitution to keep the real risk-free rate constant. The model fits volatility and predictability while retaining high average risk aversion. With constant real rates, all real bonds are riskless; thus it deliberately cannot explain real term premia without an extension. Its artificial-data success for conditional or scaled CAPMs is distinct from an empirical validation on actual assets.

There is a technical approximation in the survey's statement that the maximum Sharpe ratio equals log-SDF volatility. If $m$ is normal with variance $v$, the exact SDF coefficient of variation is $\sqrt{e^v-1}$, approximately $\sqrt v$ only for small $v$. Positivity and the feasible payoff span can further restrict attainable ratios. This distinction matters for calibrations with large kernel volatility.

Heterogeneity changes the aggregation step. Under the Constantinides–Duffie lognormal cross-sectional construction, common power preferences imply

$$
\log M^*_{t+1}-\log M^{RA}_{t+1}
=\frac{\gamma(\gamma+1)}2\operatorname{Var}^*_{t+1}(\Delta c_{k,t+1}).
$$

The true kernel averages individual marginal-utility ratios; the false representative-agent kernel applies marginal utility to aggregate consumption. The cross-sectional variance's level affects rates, and its changing covariance with aggregate returns can affect premiums. A 20% cross-sectional standard deviation is variance 0.04; explaining equity requires movements in that variance, not merely its existence. Permanent shocks are important because transitory income shocks can be smoothed. The source describes evidence that measured heterogeneity alone has limited power unless complemented by high curvature or meaningful constraints.

Limited market participation instead makes the consumption of actual investors the relevant object. Heterogeneous risk aversion also creates state-dependent aggregate risk-bearing capacity because aggressive investors gain wealth share in good states. These are distinct mechanisms and imply different household-level tests.

## Behavioral mechanisms and a reproducible research agenda

Behavioral models combine nonstandard demands with limits on rational investors' capacity or desire to offset them. Fundamental risk, short horizons, noise-trader price risk, and withdrawal of funding after losses can all limit offsetting trades. This is not riskless arbitrage in the technical sense. Purely diversifiable, pervasive mispricing is hard to sustain without additional frictions; a mechanism must explain the systematic risk or trading restriction preventing its removal.

Prospect-theory applications require choices the experimental label does not determine: consumption versus wealth as the utility argument, evaluation frequency, updating of reference wealth, separate mental accounts, and whether realization triggers evaluation. Frequent loss evaluation can create high effective risk aversion; dependence on earlier gains can generate time-varying aversion and volatility. A disposition effect does not follow from prospect theory alone without extra assumptions about accounts and realized versus unrealized losses.

The survey contrasts three explanations of momentum and reversal. Barberis–Shleifer–Vishny use Bayesian switching between two misspecified dividend models, one mean-reverting and one trending, while the true process is a random walk. Daniel–Hirshleifer–Subrahmanyam use overconfidence in private signals and asymmetric self-attribution after public news. Hong–Stein combine slowly diffusing private information with momentum traders who use limited price history. Each needs different information states and updating rules; they are not interchangeable implementations of “investor sentiment.” Their full parameterizations and quantitative fit are not reproduced here.

Campbell's concluding standard is demanding but operational. A proposed SDF should be checked jointly against rates, risk premiums, and factor exposures; a dynamic allocation should include parameter learning and background income; a behavioral model should specify whose beliefs or preferences deviate and why opposing capital cannot erase the effect. Empirical patterns should be tracked across time and after public discovery rather than assumed permanent. The survey supplies the mathematical architecture and key failure modes for such work. It does not supply a single original experiment, one calibrated universal model, or an executable investment strategy, and a faithful reimplementation must preserve those boundaries.
