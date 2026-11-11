# Asset pricing with liquidity risk

Viral V. Acharya and Lasse Heje Pedersen. *Journal of Financial Economics* 77 (2005), 375–410. DOI: 10.1016/j.jfineco.2004.06.007. Source: [LiquidityTrading_AcharyaPedersen_2005.pdf](../../Finance/LiquidityTrading_AcharyaPedersen_2005.pdf). The source contains the full article and proofs. References below use journal pages; PDF page 1 is page 375.

## Why this matters

A stock can be expensive to trade on average, become expensive to trade when other assets do, lose value when market liquidity disappears, or become difficult to sell precisely when market returns are poor. These are distinct properties. Acharya and Pedersen derive a model that puts all four in one pricing equation rather than adding an arbitrary liquidity factor to the ordinary CAPM.

The theoretical contribution is a CAPM for returns after liquidation costs, with a decomposition into the usual return covariance and three liquidity covariances. The especially novel channel is the covariance between an asset's own liquidation cost and the market return: investors dislike assets whose sale becomes costly when their aggregate wealth falls. The model also connects persistent illiquidity to low contemporaneous prices and high future required returns.

Empirically, the paper estimates these channels using daily CRSP data aggregated to monthly portfolios. Liquidity-adjusted pricing improves the fit for portfolios sorted on liquidity, liquidity variability, and size. It does not explain the book-to-market effect. Its numerical attribution of about 1.1 percentage points annually to liquidity risk relies on a common-price-of-risk restriction and a calibrated holding period. It is not an unrestricted, precisely identified estimate of three separate risk premia.

## Economy, trading friction, and investor problem

Time is discrete. A new generation of $N$ investors arrives each period and lives for two dates, $t$ and $t+1$. Investor $n$ has initial endowment $e_t^n$, consumes at the second date, and has constant absolute risk aversion $A^n$. Preferences are represented by $-E_t\exp(-A^n W_{t+1}^n)$. Investors can borrow or lend at an exogenous **gross** risk-free return $r^f>1$.

There are $I$ risky securities with fixed share supplies $S^i$. Security $i$ has ex-dividend price $P_t^i$, dividend $D_t^i$, and per-share selling cost $C_t^i$. A young investor buys at $P_t^i$ and, on liquidation, receives $P_{t+1}^i-C_{t+1}^i$ plus the dividend. Short positions are prohibited. The friction is exogenous and stochastic; the model does not derive it from a limit order book, asymmetric information, or dealer funding constraints.

For a vector $y^n\geq0$ of share holdings,

$$
W_{t+1}^n=(P_{t+1}+D_{t+1}-C_{t+1})^\top y^n+r^f(e_t^n-P_t^\top y^n).
$$

Dividends and costs follow vector autoregressions with scalar persistence parameters:

$$
D_t=\bar D+\rho_D(D_{t-1}-\bar D)+\epsilon_t,
\qquad
C_t=\bar C+\rho_C(C_{t-1}-\bar C)+\eta_t.
$$

Here $0\leq\rho_D,\rho_C\leq1$, the means are positive, and innovations are independent over time and jointly normal, with covariance matrices $\Sigma_D$, $\Sigma_C$, and $\Sigma_{CD}=E[\epsilon_t\eta_t^\top]$. The common persistence across securities is a simplifying notation choice. Cross-security and dividend–cost correlations are allowed.

Conditional normality and exponential utility reduce the portfolio problem to maximizing expected wealth minus $A^n/2$ times its variance. If $V=\operatorname{Var}_t(P_{t+1}+D_{t+1}-C_{t+1})$, the unconstrained demand is

$$
y^n=\frac{1}{A^n}V^{-1}\left(E_t[P_{t+1}+D_{t+1}-C_{t+1}]-r^fP_t\right).
$$

This inverse requires the usual nonsingularity qualification. Define aggregate risk aversion $A=(\sum_n1/A^n)^{-1}$. Market clearing implies

$$
r^fP_t=E_t[P_{t+1}+D_{t+1}-C_{t+1}]-AVS.
$$

The appendix solves this equation using a stationary linear price rule:

$$
P_t=U+\frac{\rho_D}{r^f-\rho_D}D_t-\frac{\rho_C}{r^f-\rho_C}C_t.
$$

For implementation, define

$$
V=\operatorname{Var}\left(\frac{r^f}{r^f-\rho_D}\epsilon_t-\frac{r^f}{r^f-\rho_C}\eta_t\right),
$$

and then

$$
U=\frac{1}{r^f-1}\left[\frac{r^f(1-\rho_D)}{r^f-\rho_D}\bar D-\frac{r^f(1-\rho_C)}{r^f-\rho_C}\bar C-AVS\right].
$$

These equations provide a direct theoretical reconstruction from chosen primitive parameters. In this equilibrium, $y^n=(A/A^n)S$, which is nonnegative, so the initially ignored short-sale constraint does not bind. Conditional normality is also verified by the linear solution. Uniqueness is stated for the linear equilibrium class, not for every conceivable nonlinear equilibrium.

The model forces every generation to liquidate after one period. This makes net returns sufficient for the investment problem, but removes endogenous decisions about when to trade. Normal cost innovations can also generate negative costs, one reason the authors explicitly restrict short selling. The Gaussian economy should be understood as a tractable analytical representation rather than a literal globally positive model of all prices and execution costs.

## Deriving the four pricing channels

Define the gross asset return and the relative liquidation cost by

$$
r_{t+1}^i=\frac{D_{t+1}^i+P_{t+1}^i}{P_t^i},\qquad c_{t+1}^i=\frac{C_{t+1}^i}{P_t^i}.
$$

The market counterparts use value weights based on the outstanding supplies and current prices. Proposition 1, p. 381, says that the conditional CAPM holds for net returns:

$$
E_t[r_{t+1}^i-c_{t+1}^i]=r^f+\lambda_t\frac{\operatorname{Cov}_t(r_{t+1}^i-c_{t+1}^i,r_{t+1}^M-c_{t+1}^M)}{\operatorname{Var}_t(r_{t+1}^M-c_{t+1}^M)},
$$

where $\lambda_t=E_t[r_{t+1}^M-c_{t+1}^M-r^f]$. The proof can be understood through an imagined frictionless economy whose dividends are $D-C$. Its equilibrium holdings remain feasible in the actual economy and generate the same net payoff, so its CAPM transfers to the economy with costs.

Expanding the covariance gives

$$
E_t[r^i]-r^f=E_t[c^i]+\lambda_t\left(\beta_{1,t}^i+\beta_{2,t}^i-\beta_{3,t}^i-\beta_{4,t}^i\right).
$$

All four betas share the denominator $\operatorname{Var}_t(r^M-c^M)$. Their respective numerators are

$$
\operatorname{Cov}_t(r^i,r^M),\quad
\operatorname{Cov}_t(c^i,c^M),\quad
\operatorname{Cov}_t(r^i,c^M),\quad
\operatorname{Cov}_t(c^i,r^M).
$$

The signs have specific economic content. Common illiquidity, $\beta_2$, raises required returns because the asset is hard to sell when everything else is. Positive $\beta_3$ lowers required returns because an asset that pays well when market costs rise provides insurance. Positive $\beta_4$ also lowers required returns: costs are then relatively low in down markets. Conversely, the empirically common negative $\beta_4$ is undesirable because the asset becomes costly to liquidate as aggregate wealth declines. With positive $\lambda$, these statements follow directly from the pricing equation.

The market beta in this decomposition is not exactly the conventional CAPM beta, because its denominator includes market liquidity innovations. A software implementation must not combine conventional market betas with the three new betas unless it explicitly rescales the denominator. Similarly, these are covariances with **illiquidity**; replacing costs by a liquidity index reverses the relevant signs.

## Persistence and the limits of the comparative statics

The price rule makes clear that persistent cost increases reduce current prices. Proposition 2 states a positive effect of current cost on the conditional expected return for a portfolio $q$ when $\rho_C>0$ and $E_t[P_{t+1}^q+D_{t+1}^q]>\rho_C P_t^q$. The condition is satisfied, for example, by positive-price portfolios with expected gross returns of at least one. It should not be discarded when applying the result to arbitrary long–short portfolios.

Proposition 3 qualifies the negative contemporaneous relation between returns and illiquidity. Its proof gives

$$
\operatorname{Cov}_t(c_{t+1}^q,r_{t+1}^q)=\frac{1}{(P_t^q)^2}\left[\frac{r^f}{r^f-\rho_D}q^\top\Sigma_{CD}q-\frac{\rho_C}{r^f-\rho_C}q^\top\Sigma_Cq\right].
$$

The sign is negative only when the second term dominates. Strong positive covariance between dividend news and cost news can overturn it. Thus “illiquidity increases imply falling returns” is a conditional model result, not a mathematical identity. The empirical article principally tests the cross-sectional pricing equation rather than estimating all primitive autoregressive parameters of this equilibrium.

## From daily observations to a monthly cost proxy

The empirical source is daily CRSP returns and volume from July 1, 1962 through December 31, 1999, for NYSE and AMEX common shares. Nasdaq is excluded to avoid inconsistency from interdealer volume and its shorter available history. The monthly tests use 1964–1999. Book values come from COMPUSTAT using the authors' described stockholders' equity, deferred-tax, investment-tax-credit, and preferred-stock adjustments.

For stock $i$ and month $t$, the raw proxy is the mean of $|R_{itd}|/V_{itd}$ over valid days, with dollar volume expressed in millions. It is an Amihud measure of price change per volume rather than a directly observed round-trip cost. Equation (18) converts it to a cost-like percentage:

$$
c_{it}^{(\%)}=\min\{0.25+0.30\,ILLIQ_{it}P^M_{t-1},\;30.00\}.
$$

Here $P^M_{t-1}$ is the ratio of market capitalization at the preceding month-end to market capitalization at the end of July 1962. It is not the market's monthly return. The scaling mitigates secular changes in the raw proxy. The constants match the approximate level and cross-sectional dispersion of effective half-spreads in external evidence. The 30-percent cap reduces domination by very-low-volume observations.

The numerical formula is in percentage units. For equations computed with decimal returns, divide the resulting costs by 100; for percentage returns, keep both series consistently in percentages. Covariance ratios are invariant to a common scaling of all relevant return and cost series, but not to scaling only the costs. The cost floor is 0.25 percent, not 25 percent.

For similarly formed size deciles, the normalized proxy averages 1.24 percent, versus 1.11 percent in the half-spread comparison, and has standard deviation 0.37 percent. This is a calibration of a noisy proxy to a cost scale, not a measurement of each investor's actual execution cost. It is especially consequential because the level premium depends directly on that scale.

## Portfolio construction and timing

The monthly market portfolio includes stocks priced between \$5 and \$1,000 at the beginning of the month and with at least fifteen days of return and volume observations in that month. Test portfolios are formed annually. Eligible stocks have beginning-of-year prices in the same range and at least 100 daily observations in the previous year.

The authors construct separate sets of 25 portfolios using prior-year average daily illiquidity, prior-year standard deviation of daily illiquidity, or beginning-of-year capitalization. They also sort first into five book-to-market groups and then into five size groups within each book-to-market group. This is a sequential sort, not necessarily identical to independently intersecting two quintile sorts. Book-to-market availability in the preceding year constrains that sample.

For each month, both the portfolio return and portfolio cost are averages using the chosen portfolio weights. The main specification uses value-weighted test portfolios against an equally weighted market. That market convention differs from the theoretical value-weighted aggregate wealth portfolio. The authors motivate equal weighting as a rough compensation for omitted illiquid wealth such as private businesses and real estate, then check value-weighted-market alternatives. The distinction must be retained when reconstructing the main tables.

Delisting treatment follows Shumway: recorded delisting outcomes are retained, including complete losses, and missing returns for specified performance-related CRSP deletion codes receive a 30-percent loss. The article does not provide code for every CRSP merge, return-field combination, or weight update. It also does not impose a fully detailed modern publication-lag protocol for accounting data. These are implementation gaps, particularly if the objective is a point-in-time tradable replication rather than reproducing the historical cross-sectional exercise.

## Innovation filtering and beta estimation

Liquidity levels are persistent: the market series has monthly autocorrelation around 0.87. The empirical model therefore uses innovations, not raw persistent levels, in liquidity-risk covariances. Write $u_{c,t}^p=c_t^p-E_{t-1}c_t^p$ and $u_{r,t}^M=r_t^M-E_{t-1}r_t^M$.

The liquidity filter has a nonstandard but important normalization. First truncate each raw stock illiquidity at $(30-0.25)/(0.30P^M_{t-1})$ and aggregate to a portfolio raw measure $L_t^p$. Estimate the market equation

$$
0.25+0.30L_t^MP^M_{t-1}=a_0+a_1(0.25+0.30L_{t-1}^MP^M_{t-1})+a_2(0.25+0.30L_{t-2}^MP^M_{t-1})+u_{c,t}^M.
$$

The same market-capitalization normalization date appears in all three terms. Running an ordinary AR(2) on previously stored $c_t,c_{t-1},c_{t-2}$ would use different capitalization dates and mix price-index changes into liquidity innovations. Portfolio innovations are computed analogously with the **same fitted AR coefficients**, rather than fitting an independent autoregression for every portfolio.

The market filter has $R^2=78$ percent; innovation standard deviation is 0.17 percent and residual autocorrelation is $-0.03$. AR(1) produces residual autocorrelation $-0.29$, while AR(3) adds little fit. Figure 1 shows recognizable crisis spikes. Correlation with the Pastor–Stambaugh liquidity innovation series is $-0.33$, partly reflecting the opposite liquidity versus illiquidity sign convention.

Market return innovations come from an AR(2) augmented with beginning-of-month information: return, volatility, average illiquidity, log average dollar volume, and log average turnover measured over the previous six months, plus log market capitalization lagged one month. The paper identifies these inputs but does not supply a complete executable feature-construction recipe.

With $D=\operatorname{Var}(u_r^M-u_c^M)$, the unconditional betas are

$$
\beta_1^p=\frac{\operatorname{Cov}(r^p,u_r^M)}{D},\quad
\beta_2^p=\frac{\operatorname{Cov}(u_c^p,u_c^M)}{D},\quad
\beta_3^p=\frac{\operatorname{Cov}(r^p,u_c^M)}{D},\quad
\beta_4^p=\frac{\operatorname{Cov}(u_c^p,u_r^M)}{D}.
$$

These use the entire 1964–1999 monthly sample. The use of unfiltered asset returns in two numerators is intentional in the displayed unconditional equations. The unconditional result requires additional assumptions, such as constant conditional innovation covariances; averaging a conditional CAPM does not automatically produce an unconditional CAPM without qualification. Full-sample beta estimation also means this is an explanatory pricing exercise, not a rolling out-of-sample portfolio rule.

## Holding-period adjustment and inference

Define $\beta_{net}=\beta_1+\beta_2-\beta_3-\beta_4$. The primary cross-sectional regression is

$$
E[r^p-r^f]=\alpha+kE[c^p]+\lambda\beta_{net}^p.
$$

The theoretical model has $\alpha=0$ and one liquidation per model period. Monthly sampling is shorter than the presumed investor holding period, so the empirical level-cost term is scaled by $k$. For illiquidity-sorted portfolios, average monthly turnover calibrates $k=0.034$, implying approximately 29 months per full turnover. The approximation assumes that the relevant return and innovation aggregation behaves suitably across horizons. It does not mean each individual investor literally holds each asset for exactly 29 months.

With fixed $k$, subtract $kE[c^p]$ from the dependent variable and estimate the intercept and one risk price. Reported goodness of fit is nevertheless evaluated against the same gross excess-return dependent variable for model comparisons. The unrestricted variants estimate $k$, add conventional-risk exposure separately from net beta, or free each beta's risk price. Because net beta contains $\beta_1$, a negative coefficient on an additional $\beta_1$ regressor is not by itself a negative total market-risk price.

Inference uses GMM to account for the first-stage estimated betas, with Newey–West covariance estimation using two lags. Point estimates coincide with the relevant OLS or Fama–MacBeth estimates; naive second-stage OLS standard errors do not reproduce the stated inference. The source discusses the moment framework but does not provide software, optimization settings, or a full numerical replication package.

## Empirical findings, identification, and limits

Table 1 shows that more illiquid portfolios also have greater liquidity risk. Average cost rises from 0.25 percent in portfolio 1 to 8.83 percent in portfolio 25. Average monthly excess return rises from 0.48 to 1.10 percent, though not monotonically at every step. The reported beta columns are multiplied by 100; for example, portfolio 25's displayed $\beta_4=-4.52$ means $-0.0452$ in unscaled units.

Identification is difficult because the risk measures are strongly correlated. Across the 25 liquidity portfolios, $\operatorname{Corr}(\beta_1,\beta_3)=-0.972$ and $\operatorname{Corr}(\beta_2,\beta_4)=-0.941$. These correlations are not evidence that the channels are mathematically identical; they mean the observed cross-section supplies little independent variation for pricing them separately.

Table 4 reports the main fit:

| Test portfolios | Liquidity-adjusted $R^2$ | Standard CAPM $R^2$ | Common risk price | Risk-price $t$ |
|---|---:|---:|---:|---:|
| Illiquidity | 0.732 | 0.653 | 1.512 | 2.806 |
| Illiquidity variability | 0.865 | 0.726 | 1.471 | 2.817 |

These are the fixed-$k$ specifications. When $k$ is freely estimated, it is 0.042 for illiquidity portfolios and 0.062 for variability portfolios, with fits of 0.825 and 0.886. Improvement from a calibrated liquidity adjustment is distinct from evidence that every liquidity-risk channel is separately priced. In a specification controlling separately for market beta and fixed level cost, net beta has $t=1.102$ for illiquidity portfolios but $t=2.615$ for variability portfolios. The paper appropriately characterizes the incremental evidence as weak rather than definitive.

Under the common-price restriction, the annual expected-return difference between the most and least illiquid portfolios decomposes into approximately 0.08 percentage point for commonality in costs, 0.16 for return exposure to market illiquidity, and 0.82 for own-cost exposure to market returns. The rounded sum is about 1.1 percentage points, with a reported 95-percent interval of 0.24–1.88. The calibrated level effect is 3.5 points, giving 4.6 points combined. These are model-attributed contributions, not four independently estimated strategy alphas; other risk contributions and residual pricing errors remain.

Alternative weighting schemes preserve much of the improvement but weaken some significance. With value-weighted test portfolios and market, the standard CAPM has essentially zero cross-sectional $R^2$, while the fixed-$k$ liquidity model reaches 0.486; its common-risk-price $t$ is only 1.627. Size portfolios show improved fit but limited precision. For book-to-market-by-size portfolios, the constrained model's adjusted fit is 0.406 versus 0.229 for CAPM. Allowing unrestricted prices improves fit further but produces unstable, sometimes incorrectly signed and insignificant prices. Book-to-market remains important when included directly. A high fit from those unrestricted regressions should not be presented as successful explanation of the value effect.

Specification tests likewise support relative improvement, not universal acceptance. For illiquidity portfolios, the fixed-$k$ zero-pricing-error test has $p=8.5$ percent, compared with 0.5 percent for CAPM. The estimated common risk price exceeds the observed net market premium, with a restriction-test $p=6.6$ percent. Failure to reject some restrictions in a highly collinear, 25-portfolio setting can reflect low power. The authors explicitly raise that concern for book-to-market portfolios.

The practical contribution is a precise way to organize liquidity exposure and distinguish average costs from state-dependent sale difficulty. A reproduction should first match proxy units, truncation, sort timing, the shared liquidity filter, market weighting, and full-sample beta calculations before testing risk prices. Extending the result to live risk management requires different work: point-in-time estimation, uncertainty in costs, endogenous holding periods, broader market-wealth proxies, and potentially funding or liquidation constraints. Those extensions are economically motivated by this paper, but they are not established by its empirical tables.
