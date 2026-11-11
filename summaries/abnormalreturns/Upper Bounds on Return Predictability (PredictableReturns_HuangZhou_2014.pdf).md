# Upper Bounds on Return Predictability

Dashan Huang and Guofu Zhou. April 2014 working-paper version, first drafted October 2010; supersedes a November 2012 version titled *What is the Maximum Return Predictability Permitted by Asset Pricing Models?* [Supplied PDF](../../Finance/PredictableReturns_HuangZhou_2014.pdf). This note concerns the supplied 37-page draft, including its proofs and eight empirical tables, rather than an assumed later revision. Page references use the PDF page count.

## Why this matters

A predictive regression and an asset-pricing model cannot be evaluated entirely independently. A variable that forecasts excess returns defines a managed trading payoff: invest an amount depending on the variable, and receive that amount times the subsequent excess return. A valid stochastic discount factor must price this payoff as well as the underlying asset. Its covariance with the managed payoff therefore limits the strength of the predictor.

Huang and Zhou turn that observation into a diagnostic for classes of pricing models sharing a state-variable vector. The proposed bound combines the amount of managed-return variation linearly explained by those states with a cap on discount-factor volatility. In the supplied empirical exercise, state variables associated with habit, long-run-risk, and rare-disaster models explain little of the managed payoff. Their reported bounds are consequently much smaller than the fitted predictive $R^2$ for most of ten conventional predictors.

This is a test of economic explanations of predictability, not a trading strategy or an out-of-sample forecasting competition. The useful contribution is a tractable link between predictable returns, state variables, and the volatility a pricing kernel would need. Passing a bound is only a necessary-condition check; it neither identifies a correct stochastic discount factor nor establishes profitable implementation. Rejection applies to a joint collection of pricing, state-proxy, distributional, volatility-cap, and estimation assumptions.

The manuscript presents several of those assumptions more broadly than its proof supports. In particular, linear correlation with states bounds covariance with an arbitrary nonlinear discount factor only under a suitable conditional-mean restriction. No-arbitrage alone does not put an upper limit on discount-factor volatility. The printed risk-aversion and Sharpe-ratio normalization steps also need qualification. This note states the authors' formulas and empirical results, then separates a valid conditional derivation from unresolved claims in the supplied version.

## Predictability and the managed payoff

Let $r_{t+1}$ be a simple excess return and $z_t$ a scalar predictor known at time $t$. The population linear predictive regression is

$$
r_{t+1}=\alpha+\beta z_t+\varepsilon_{t+1},
\qquad
\beta=\frac{\operatorname{Cov}(r_{t+1},z_t)}{\operatorname{Var}(z_t)}.
$$

With an intercept and finite, nonzero variances, its population explanatory fraction is

$$
R^2=\frac{\operatorname{Cov}(r_{t+1},z_t)^2}
{\operatorname{Var}(r_{t+1})\operatorname{Var}(z_t)}.
$$

Write $m_{t+1}=m(x_{t+1})$ for the candidate positive stochastic discount factor, measurable with respect to a $K$-dimensional state vector. Conditional pricing requires $E_t[m_{t+1}r_{t+1}]=0$. Normalize by the unconditional mean, $\widetilde m=m/E[m]$, so that $E[\widetilde m]=1$. This constant rescaling preserves the zero conditional price of excess returns.

Define $\mu_z=E[z_t]$ and the managed payoff

$$
Y_{t+1}=r_{t+1}(z_t-\mu_z).
$$

Provided the products are integrable and the information-dependent strategy belongs to the priced payoff class, conditional pricing and iterated expectations imply $E[\widetilde mY]=0$. Hence

$$
E[Y]=\operatorname{Cov}(r,z)=-\operatorname{Cov}(\widetilde m,Y),
$$

and

$$
R^2=\frac{\operatorname{Cov}(\widetilde m,Y)^2}
{\operatorname{Var}(r)\operatorname{Var}(z)}.
$$

This is the key pricing identity in Appendix A, equations (27)–(29). It requires the conditional pricing restriction, not merely an unconditional discount factor that prices a finite set of buy-and-hold returns. The predictor can also be replaced by a specified function of the information, but choosing that function to maximize forecasting performance changes both the managed payoff and its bound. The paper explicitly leaves the joint optimization over predictor transformations open.

## The state-dependent bound and what its assumptions mean

Project the managed payoff on the state vector:

$$
Y=a+b'x+u,
\qquad
b=\Sigma_{xx}^{-1}\Sigma_{xY},
$$

where $\Sigma_{xx}=\operatorname{Var}(x)$ is nonsingular. Ordinary projection gives $E[u]=0$ and $E[ux]=0$. To replace covariance with a nonlinear $m(x)$ by covariance with the linear projection, one needs the stronger condition

$$
E[u\mid x]=0.
$$

Under that condition $\operatorname{Cov}(u,\widetilde m(x))=0$, and Cauchy–Schwarz yields

$$
\begin{aligned}
\operatorname{Cov}(\widetilde m,Y)^2
&=(b'\Sigma_{x\widetilde m})^2\\
&\le (\Sigma_{xY}'\Sigma_{xx}^{-1}\Sigma_{xY})
(\Sigma_{x\widetilde m}'\Sigma_{xx}^{-1}\Sigma_{x\widetilde m})\\
&\le (\Sigma_{xY}'\Sigma_{xx}^{-1}\Sigma_{xY})\operatorname{Var}(\widetilde m).
\end{aligned}
$$

Define the multiple-correlation coefficient and the scaled coefficient

$$
\rho_{xY}^2=
\frac{\Sigma_{xY}'\Sigma_{xx}^{-1}\Sigma_{xY}}{\operatorname{Var}(Y)},
\qquad
\phi_{xY}^2=
\rho_{xY}^2\frac{\operatorname{Var}(Y)}{\operatorname{Var}(r)\operatorname{Var}(z)}.
$$

The resulting core inequality is

$$
R^2\le\phi_{xY}^2\operatorname{Var}(\widetilde m).
$$

This formulation makes three distinctions clear. First, the relevant covariance is with the **managed payoff** $r(z-\mu_z)$, not simply with the asset return $r$. Second, $\rho^2$ is a multiple correlation bounded by one, whereas $\phi^2$ includes a variance ratio and need not be bounded by one. The improvement over a bound omitting $\phi^2$ is empirical, not automatic for every joint distribution. Third, this is a population statement. A small fitted sample correlation can be noisy, especially when the states are generated regressors.

A sufficient condition for $E[Y\mid x]$ to be affine is appropriate joint normality of $(Y,x)$. Suitable joint elliptical distributions also have this property under moment conditions. Normal or elliptical **marginal states alone** do not suffice: a nonlinear payoff can have zero linear correlation with a normal state and still covary with a nonlinear function of that state. The appendix's wording that elliptically distributed states are sufficient is therefore incomplete without a restriction on the joint law or the conditional mean.

The first proof route says $(x,Y)$ are jointly normal conditional on time-$t$ information but then uses unconditional covariance matrices in equation (30). Conditional normality with changing conditional means and variances does not in general imply the unconditional linear conditional-mean identity. The second route explicitly assumes a conditional-zero residual, but its decomposition and conditioning notation vary. The safe reusable result is the inequality above under the stated unconditional residual restriction, or a separately derived conditional analogue with all terms consistently conditioned. The paper conjectures that relaxing its distributional restrictions would not alter the empirical conclusions; it does not prove that extension.

A more general route would use $E[Y\mid x]$ rather than its linear projection, giving $R^2\le\operatorname{Var}(E[Y\mid x])\operatorname{Var}(\widetilde m)/[\operatorname{Var}(r)\operatorname{Var}(z)]$. This follows from the same covariance argument and is a **derived alternative**, not the authors' estimated bound. It illustrates why nonlinear state dependence can matter and why small linear correlations alone cannot reject every nonlinear model sharing those states.

## Two proposed volatility caps and necessary qualifications

The authors' first reported bound is

$$
\overline R^2_{RA}=\phi_{xY}^2\gamma^2\sigma^2(r_{mkt}),
$$

where $\gamma$ is a maximum risk-aversion parameter and $r_{mkt}$ denotes the market return. The corresponding Ross benchmark used in their tables is $\gamma^2\sigma^2(r_{mkt})$. Their numerical choice is $\gamma=5$. The paper motivates this using external risk-aversion estimates and a comparison with a CRRA investor's discount factor. It should be treated as an economic restriction rather than a deduction from positive prices alone.

Appendix A.1, PDF page 24, claims that for lognormally distributed optimal wealth, bounded risk aversion implies $\operatorname{Var}(\widetilde m)\le\gamma^2\sigma^2(r_{mkt})$. There is an important exact-versus-approximate issue in the displayed argument. If $\log W\sim N(\mu,v)$ and the CRRA discount factor is proportional to $W^{-\gamma}$, direct lognormal moments give

$$
\frac{\operatorname{Var}(W^{-\gamma})}{E[W^{-\gamma}]^2}
=\exp(\gamma^2v)-1.
$$

For $v>0$ this exceeds $\gamma^2v$. Thus the latter is a first-order approximation to the normalized-SDF variance in that example, not its exact upper bound. The manuscript additionally moves between a variance of log wealth in the proof and a variance of simple market returns in the empirical formula. Their relationship needs specification. This note preserves the reported $RA$ numbers as the authors' calculations; it does not certify the exact proposition from the printed proof. Replacing the scalar cap with another justified upper bound would preserve the core projection argument, but requires redoing the empirical thresholds and inference.

The second reported bound is

$$
\overline R^2_{SR}=\phi_{xY}^2h^2\operatorname{SR}_{mkt}^2,
\qquad h=2,
$$

motivated by ruling out unusually attractive risk-return opportunities. A clean sufficient assumption is an upper cap on the **normalized** SDF standard deviation, $\operatorname{Std}(\widetilde m)\le h\operatorname{SR}_{mkt}$. This is an additional good-deal restriction. No-arbitrage by itself supplies pricing-kernel existence and lower volatility requirements associated with priced Sharpe ratios; it does not imply an upper cap on every admissible SDF. A good deal with high but finite Sharpe ratio is also not the same object as a riskless arbitrage.

The source instead writes its equation (10) for the unnormalized $m$. Under that convention the normalized variance bound is

$$
\operatorname{Var}(\widetilde m)
\le \frac{h^2\operatorname{SR}_{mkt}^2}{E[m]^2}.
$$

The appendix drops the square on $h$ in an intermediate line and states that $1/E[m]^2$ equals the risk-free rate. With a constant gross risk-free return $R_f$, pricing gives $E[m]=1/R_f$, so that factor is $R_f^2$. With a time-varying risk-free return known at time $t$, conditional pricing gives $E_t[m]=1/R_{f,t}$ and the unconditional normalization needs separate treatment. Approximating a monthly gross risk-free return by one can make the difference numerically small, but it does not resolve the notation or turn the cap into a no-arbitrage theorem.

The numerical closeness of the two bounds in some samples reflects the selected $\gamma$ and $h$ and the historical market mean and variance. It is not a general identity. Increasing either calibration parameter relaxes its bound quadratically. A rejection can therefore indicate failure of the selected volatility cap, the state representation, the linear conditional-mean restriction, or pricing itself; the test alone cannot allocate responsibility among them.

## State variables associated with the three model families

For habit formation, the source writes

$$
m_{t+1}=\delta\left(\frac{S_{t+1}}{S_t}\frac{C_{t+1}}{C_t}\right)^{-A},
\qquad x_{t+1}=(\Delta c_{t+1},\Delta s_{t+1})',
$$

where $S=(C-X)/C$ is surplus consumption relative to an unobserved habit level. The latent log surplus ratio is generated recursively as

$$
s_{t+1}=(1-\varphi)\bar s+\varphi s_t+
\lambda(s_t)(\Delta c_{t+1}-\bar c),
$$

with $\lambda(s)=\bar S^{-1}\sqrt{1-2(s-\bar s)}-1$ below the cutoff $\bar s+(1-\bar S^2)/2$ and zero above it. The steady-state ratio is $\bar S=\sigma_c\sqrt{\gamma/(1-\varphi)}$, and $\bar s=\log\bar S$. The paper says it follows Campbell–Cochrane in extracting this process, but does not provide a complete frequency-specific calibration, initialization, burn-in, or uncertainty treatment. Therefore the bound is free of the final SDF functional-form parameters only conditional on a chosen state series; extracting that series is itself model dependent.

The long-run-risk discussion uses persistent latent expected consumption growth and stochastic consumption variance, with consumption and dividend innovations modeled as normal. Its log-linearized SDF initially depends on current latent states, next-period latent states, and consumption growth. After projecting the latent states on the risk-free rate and dividend-price ratio, the displayed log SDF contains $r_{f,t}$, $dp_t$, $r_{f,t+1}$, $dp_{t+1}$, and $\Delta c_{t+1}$. Yet the empirical state vector retained in equation (16) is only

$$
x_{t+1}=(\Delta c_{t+1},r_{f,t+1},dp_{t+1})'.
$$

Known time-$t$ terms can be treated specially in a consistently conditional argument, but they cannot simply be discarded from the unconditional representation $m=m(x_{t+1})$ used in the proof. The supplied version does not fully reconcile this step. It also relies on the proposed observable-state projection and log-affine approximation rather than an exact measurement of the latent economic states.

For rare disasters, consumption growth has an ordinary normal component and a disaster loss $\log(1-b)$ with time-varying probability $p_t$, $0<b<1$. An increasing relation between dividend-price ratio and disaster probability is used to justify

$$
x_{t+1}=(\Delta c_{t+1},dp_{t+1})'.
$$

That observable proxy avoids directly estimating disaster probabilities but imports the model's invertibility and measurement assumptions. In particular, a mixture containing disasters does not automatically satisfy the joint-normal or affine-conditional-mean restriction used by the bound. The test of this proxy vector is consequently broader in economic aspiration than the rigorously established statistical domain.

## Data, predictor definitions, and information availability

Monthly observations span January 1959–December 2012. The market return is the S&P 500 total simple return minus the Treasury bill return. Ten predictors are drawn mainly from Welch–Goyal data: log dividend-price ratio; three-month bill yield; long-term government yield; long-term government bond return; term spread; Moody's BAA-minus-AAA yield spread; corporate-minus-government long-term bond return spread; the monthly sum of squared daily S&P returns; aggregate investment-capital ratio; and the consumption-wealth cointegration residual, $cay$.

The last two variables are quarterly. For monthly regressions, the paper assigns a first-quarter value to March, April, and May, and analogously for other quarters. A variable observed only after quarter-end may not actually be known at the March formation date. The article does not supply vintage data, release-date lags, or recursively estimated $cay$ coefficients. This matters because conditional pricing requires the predictor to be in the investor's information set. A predictive regression using revised or retrospectively fitted data is not automatically a test of a feasible time-$t$ managed payoff.

Consumption is seasonally adjusted real per-capita nondurables and services consumption, constructed using nominal NIPA series, deflators, and population. The description refers to Tables 2.3.5, 2.8.5, 2.1, 2.6, 2.3.4, and 2.8.4. It first describes consumption growth as a percentage change, whereas the model sections use log differences. Exact aggregation, annualization, and the chosen transformation need to be established for re-estimation. Size, book-to-market, momentum, and ten industry portfolio returns come from Ken French's library. The source labels small, median, and large portfolios but does not fully specify their constituent sort breakpoints or portfolio-file vintage.

There is a quarterly-sample inconsistency. The general data section says 1947Q1–2012Q4, whereas the quarterly results and Table 2 specify 1952Q1–2012Q4. The latter is the appropriate label for the reported table; the reason for dropping the earlier observations is not given. Friction-proxy exercises use still different samples: August 1962–December 2012 for monthly liquidity and 1968Q1–2009Q4 for quarterly broker-dealer leverage.

These are full-sample univariate regressions with fitted $R^2$. There is no rolling forecast evaluation, training/validation selection, portfolio optimizer, rebalance strategy, transaction-cost backtest, or realized utility calculation. Positive in-sample $R^2$ alone is not evidence of statistically significant or out-of-sample predictability: a fitted intercept-and-slope regression produces nonnegative $R^2$ by construction. The relevant reported inference concerns the difference between a fitted explanatory fraction and an estimated bound.

## Moment estimation and the inequality test

For each asset, predictor, and state family, construct

$$
y_{t+1}=(r_{t+1},z_t,r_{t+1}z_t,x_{t+1}')'.
$$

Its means and second moments suffice to calculate $R^2$, $\Sigma_{xY}$, and the bound, because centering $z$ converts $rz$ into $Y=rz-\mu_zr$. The exactly identified GMM system equates sample means and second moments to their population counterparts. A computational implementation should use the distinct elements of the symmetric second-moment matrix to avoid redundant moment coordinates.

Let $g(\theta)=R^2-\overline R^2$ and let $S$ be the long-run covariance of the moment functions. The article applies the delta-method Wald statistic

$$
W=\frac{Tg(\widehat\theta)^2}
{\nabla g(\widehat\theta)'\widehat S\nabla g(\widehat\theta)},
$$

and displays a $\chi^2_1$ limit. For the stated one-sided null $g\le0$, the sign must also be retained: a large negative gap supports the bound rather than rejects it. Equivalently, use the signed standardized gap and an upper-tail critical value. A squared statistic alone cannot distinguish the two directions; at an inequality boundary, critical-value conventions must be specified. The manuscript does not report the long-run covariance kernel, bandwidth, derivative implementation, exact p-values, or full standard errors.

Regular delta-method behavior can also fail when both the predictive covariance and relevant state covariances are zero, because the squared quantities have zero first derivatives at that point. Persistent predictors, generated state series, and overlapping repeated quarterly values complicate finite-sample behavior. These are reasons to examine the test's calibration, not evidence that the published star patterns have been independently overturned. The paper does not present a simulation study of these inference issues or a multiplicity adjustment across its many predictor–asset–state combinations.

For a reconstruction, align each $r_{t+1}$ with an actually available $z_t$, calculate all means and covariances on the same complete-observation sample, solve rather than explicitly invert the state covariance matrix, retain unrounded estimates, calculate both calibrated caps, and estimate the joint long-run covariance before differentiating the gap. State estimation should be repeated inside any resampling procedure intended to account for its uncertainty. That final step is a proposed improvement rather than a described author procedure.

## Reported market and portfolio evidence

Table 1's monthly Ross benchmark is 5.09% of return variance. Predictive $R^2$ ranges from 0.02% for long-term yield to 1.62% for $cay$, so none exceeds that benchmark. The new bounds are much smaller. Selected reported values, all in percentage points of explained return variance, are:

| Predictor | Fitted $R^2$ | Habit $RA/SR$ bounds | Long-run-risk $RA/SR$ bounds | Disaster $RA/SR$ bounds |
|---|---:|---:|---:|---:|
| Dividend-price ratio | 0.23 | 0.00 / 0.00 | 0.05 / 0.04 | 0.03 / 0.03 |
| Long-term bond return | 0.90 | 0.02 / 0.02 | 0.05 / 0.05 | 0.05 / 0.05 |
| Stock variance | 1.09 | 0.08 / 0.07 | 0.20 / 0.17 | 0.07 / 0.06 |
| Investment-capital ratio | 0.65 | 0.11 / 0.09 | 0.13 / 0.11 | 0.11 / 0.09 |
| Consumption-wealth ratio | 1.62 | 0.02 / 0.02 | 0.03 / 0.02 | 0.01 / 0.01 |

Displayed zeros are rounded, not necessarily population zeros. All these cells are marked as rejecting at 5% in the source. Across all ten predictors, long-term yield is the only monthly predictor without a rejection for each of the three state families. The table's $\phi$ entries are dimensionless numbers such as 0.07, not already squared percentages. For example, $0.07^2\times5.09\%$ is approximately 0.025%, consistent with a displayed 0.02% after using unrounded inputs. Applying 7% twice or failing to square $\phi$ would produce a materially wrong bound.

Quarterly Table 2 uses the 16.7% Ross benchmark. $cay$ has fitted $R^2=4.77\%$, versus habit bounds 0.29% and 0.31%, long-run-risk bounds 0.35% and 0.38%, and disaster bounds 0.22% and 0.24%. Investment-capital ratio has $R^2=2.78\%$. Not every predictor rejects: for habit, long-term bond return has $R^2=1.18\%$ versus bounds 1.47% and 1.59%, and default yield spread has 0.31% versus 0.33% and 0.36%. Thus the table gives eight habit rejections, although the prose claims nine. Long-run-risk tables also have eight rejections, with long-term yield and term spread unstarred; the disaster table marks all ten.

Portfolio results retain substantial heterogeneity. In Table 5, $cay$ predicts the small, median, and large size portfolios with $R^2$ of 0.61%, 0.94%, and 1.67%. In Table 6, stock variance gives 0.61%, 1.06%, and 1.84% across low, median, and high book-to-market groups. Therefore the narrative that portfolio predictability is generally smaller than market predictability has meaningful exceptions. Table 7 gives long-term bond-return $R^2$ of 1.29% for losers, 1.80% for the middle momentum group, and 0.38% for winners.

One Table 7 star is inconsistent with a one-sided exceedance: the habit-model winner portfolio with default yield spread has fitted $R^2=0.03\%$, an $SR$ bound of 0.08%, and a 5% rejection marker. Since the point estimate lies below the bound, that marker cannot indicate a positive bound violation. It may be a table error or reflect an inappropriate two-sided test; the source does not resolve it.

Industry Table 8 uses only dividend-price ratio, term spread, and $cay$. The strongest $cay$ fit is “Other” at 1.68%, closely followed by nondurables at 1.67%; energy is only 0.09%. Dividend-price ratio has almost no explanatory power for energy or manufacturing, while term spread reaches 1.04% for durables and essentially zero for health. Many large fitted fractions exceed all reported model-family bounds, but several low-predictability cells are unstarred. It is not correct to describe every industry as significantly predictable under every predictor.

## Friction proxies and the limits of the conclusion

The friction extension multiplies the SDF by $\Lambda_t/\Lambda_{t+1}$ and adds $\Delta\omega_{t+1}=\log(\Lambda_{t+1}/\Lambda_t)$ to the state vector. A liquidity factor from Pástor–Stambaugh and a broker-dealer leverage factor from Adrian–Etula–Muir proxy for this extra state. This is an augmented-state pricing exercise, not a deduction of executable returns after specified commissions, impact, spreads, or funding haircuts.

On a fixed sample, adding regressors to the linear projection of $Y$ weakly increases its explained variance and hence relaxes the bound under the same cap. Tables 3 and 4 also change the sample, however, so their differences from baseline tables cannot be attributed entirely to adding the friction variable. The monthly liquidity sample has Ross benchmark 5.19%; habit $cay$ bounds increase to 0.06% and 0.05%, versus fitted $R^2=1.64\%$. Most rejections remain, but habit default spread is unstarred despite a positive estimated gap, illustrating the distinction between a numerical exceedance and a statistically reported rejection.

The quarterly leverage sample has benchmark 18.5%. Long-run-risk dividend-price ratio has fitted $R^2=0.93\%$, below its $RA$ bound 1.21% but above its $SR$ bound 0.56%, which is marked significant. Long-run-risk $cay$ is 5.10%, versus bounds 0.71% and 0.33%. The two caps therefore need not reach the same rejection decision, and additional states do permit some previously difficult cases while leaving large gaps elsewhere.

The defensible empirical conclusion is that the chosen state proxies have weak linear covariance with many predictor-managed payoffs, producing small bounds under the authors' volatility calibrations. A model designer should examine whether missing state information, nonlinear state dependence, measurement error, or a different admissible SDF volatility explains the gap. It is too broad to infer that every rational model sharing the named economic theme is impossible: the test requires explicit payoff measurability, a valid state representation, the projection restriction, and a justified cap.

The paper supplies neither raw aligned data nor executable estimation code, exact GMM tuning choices, point-in-time predictor vintages, full habit calibration, or finite-sample test diagnostics. Its own conclusion leaves structural breaks and parameter instability for future work. The core managed-payoff inequality is a valuable organizing device; the supplied version's stronger model-rejection language should be read with these mathematical and empirical qualifications.

## Source and intellectual context

The entire PDF was read, including Appendix A on pages 21–25 and all eight tables on pages 30–37. The critical inequalities, normalizations, and table entries were inspected visually. Equations (3)–(6) introduce pricing and the state coefficient; equations (22)–(39) contain the risk-aversion proof; equation (40) and the following normalization contain the Sharpe-ratio argument; equations (18)–(21) describe GMM and Wald inference. All corrections and alternative formulas in this note are identified as derivations rather than attributed to the authors.

The draft situates its work relative to Kirby (1998) on pricing restrictions on predictive regressions, Ross (2005) on predictability bounds, Hansen and Jagannathan (1991) on SDF variance restrictions, Kan and Zhou on state-dependent variance bounds, Zhou (2010) on a prior predictability bound, and Cochrane and Saá-Requejo (2000) on good-deal restrictions. Its economic state constructions draw on Campbell–Cochrane habit, Bansal–Yaron long-run risks, and variable-disaster models. Those references motivate the test; this note's numerical record is confined to the supplied April 2014 Huang–Zhou draft.
