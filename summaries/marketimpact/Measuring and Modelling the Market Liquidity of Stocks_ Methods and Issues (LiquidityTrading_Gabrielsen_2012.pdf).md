# Measuring and Modelling the Market Liquidity of Stocks: Methods and Issues

Alexandros Gabrielsen, Massimiliano Marzo, and Paolo Zagaglia. *Journal of Finance and Investment Analysis* 1(4), 2012, 89–129. [Source PDF](../../Finance/LiquidityTrading_Gabrielsen_2012.pdf). References below use printed pages; PDF page 1 is printed page 89. All 41 supplied pages, including the references, were read.

## Why this matters and what the paper contributes

A liquidity variable can be easy to calculate and still answer the wrong investment question. High turnover may reflect information-driven disagreement; a narrow displayed spread may cover little size; a large permanent response to a trade may represent price discovery rather than an execution inefficiency. This survey organizes these distinctions around volume, price dynamics, and transaction costs. Its most useful contribution is the progression from inexpensive daily proxies to models that distinguish the order-processing, inventory, and information components of spreads.

This is a methodological review, not a new estimator, original stock-selection experiment, or execution backtest. The authors explicitly distinguish their emphasis on spread decomposition and intraday information from earlier liquidity surveys. The equations and empirical findings are chiefly attributed to earlier papers. Its investment relevance is therefore in selecting and interpreting a measurement system, rather than extracting a newly documented premium. A reader should not treat the paper's 2012 publication date as the vintage of the underlying trading data: the main numerical decomposition discussed here uses 1992 observations.

The review also requires unusually careful transcription. Several displayed formulas contain sign, normalization, or dimensional problems. This note identifies those problems where they affect implementation and gives derived coherent versions when possible. Such reconstructions are algebraic explanations of the survey, not a claim that the cited original papers made the same mistakes. No original sources beyond the supplied survey were used to certify those attributions.

## What liquidity measurements can and cannot identify

The opening sections define liquidity as the ability to exchange an asset promptly at low cost. They distinguish depth, meaning orders on both sides of the current price; breadth, meaning substantial buying and selling volume; and resiliency, meaning replenishment of orders after prices move. These dimensions are related, but a scalar liquidity ranking does not preserve all three. A transaction-cost measure also depends on the trade's size and required completion time. A small trade at a displayed quote and a large urgent portfolio rebalance face different constraints even in the same stock.

The market mechanism matters. A dealer's individual spread compensates that dealer for providing immediacy. The best market spread is formed from the highest bid and lowest ask across dealers and can be narrower. In an order-driven market, limit orders provide much of the same service, but ownership of inventory and responsibility for quote revisions differ. Consequently a decomposition estimated in one institution should not be carried to another solely because both datasets contain a bid and an ask.

The central identification problem is that information and inventory management can generate similar immediate quote changes. Following a public purchase, a dealer may raise quotes because the buyer knows that value is high, or because the dealer has sold inventory and wants to discourage further purchases. Price direction alone does not distinguish these explanations. Order-flow predictability, future reversals, quote dynamics, and economic restrictions supply the additional information. The survey's organization is valuable because it makes clear how much more a structural interpretation requires than an observable spread.

## Daily volume and price-impact proxies

Let $P_{it}$ be a stock's transaction price, $V_{it}$ its traded volume, and $R_{it}$ a return. Volume must carry an explicit unit: shares and currency turnover are not interchangeable. Section 3, pp. 93–100, reviews several related proxies.

The liquidity ratio in equation (1) divides total currency turnover by accumulated absolute price movement:

$$
LR_i=\frac{\sum_t P_{it}V_{it}}{\sum_t |PC_{it}|}.
$$

Here $V$ is share volume if $PV$ is currency turnover. More turnover per unit of price movement is interpreted as greater liquidity. There is a material ambiguity in the source: the prose calls $PC$ a percentage change but defines it as $P_t-P_{t-1}$. A price difference and a percentage return produce different units and different cross-sectional rankings when prices differ. An implementation must choose and label one. Replacing $PC$ with a return gives turnover per unit return; retaining the printed difference gives turnover per currency price change. Neither should be presented as an unambiguous transcription of both the printed definition and the prose.

Martin's index, equation (2), aggregates squared price changes relative to trading volume:

$$
MLI_t=\sum_i\frac{(P_{it}-P_{i,t-1})^2}{V_{it}}.
$$

Larger values signify greater illiquidity. The source favors daily calculation, followed by weighted aggregation for longer horizons. It does not supply a universal weighting rule. Because prices enter in levels, stock splits, currencies, and price-level differences must be controlled before comparing securities. The measure does not distinguish a temporary execution concession from a permanent information-driven repricing.

Hui–Heubel's five-day measure in equation (3) is

$$
LR_{HH}=\frac{(P_{\max}-P_{\min})/P_{\min}}{V/(S\bar P)},
$$

where $S$ is outstanding shares and $\bar P$ average closing price. The numerator is the range relative to the minimum; the denominator is intended to normalize turnover by capitalization. The definition of $V$ as total volume of assets does not specify its units sufficiently. For the denominator to be a dimensionless turnover ratio, $V$ must be currency volume; using shares would leave an extra inverse-price unit. The five-day range can miss fast liquidity disturbances and includes news unrelated to execution costs. The authors also caution against substituting bid–ask quotations for transaction-price extrema, because their variation can be smaller.

Ordinary turnover avoids that particular unit ambiguity:

$$
TR_{it}=\frac{\text{shares traded}_{it}}{\text{shares outstanding}_{it}},\qquad
\overline{TR}_{iT}=\frac{1}{N_T}\sum_{t=1}^{N_T}TR_{it}.
$$

The averaging period can be a day, month, or a longer collection of subperiods. The survey describes Datar–Naik–Radcliffe regressions of monthly returns on turnover, log book-to-market, lagged log capitalization, and beta, and reports a negative association between returns and turnover after controls. It supplies no coefficient table, sampling uncertainty, or complete replication protocol for that study. Turnover is a trading-activity proxy, not a direct measurement of a marginal order's cost or a pure measure of available resting liquidity.

The market-adjusted index uses two regressions, equations (6)–(7):

$$
R_{it}=\alpha_i+\beta_iR_{mt}+\epsilon_{it},\qquad
\epsilon_{it}^{2}=\phi_{0i}+\phi_{1i}\Delta V_{it}+\eta_{it}.
$$

Here $\Delta V$ denotes the daily percentage change in currency volume. A small $\phi_1$ is interpreted as weak price sensitivity to volume and hence greater liquidity. This interpretation depends on the first-stage market model adequately removing nonliquidity return variation. Firm-specific news can drive both squared residuals and turnover; the second regression does not independently identify a causal price-impact curve. Windows, missing-volume treatment, and inference for the generated squared residuals are not specified in the review.

Amihud's proxy in equation (8) is the mean daily absolute return divided by currency volume:

$$
ILLIQ_{iT}=\frac{1}{D_T}\sum_{t=1}^{D_T}\frac{|R_{it}|}{V_{it}}.
$$

Its advantage is wide data availability. Its units are inverse currency when returns are fractions, and changing from dollars to millions of dollars rescales it by a million. The survey describes an annual cross-sectional normalization by the market mean and regressions of monthly returns on lagged illiquidity, turnover, volume, price, capitalization, dividend yield, past returns, volatility, and beta. The cited NYSE study spans 1964–1997; illiquidity is positively associated with expected returns and turnover negatively associated. These are reviewed findings, not new results estimated by Gabrielsen and coauthors. The survey does not provide a complete set of eligibility filters or numerical coefficient estimates, and it should not substitute for the underlying paper when reproducing the premium.

Finally, the Marsh–Rock measure changes the scaling variable from traded volume to the number of transactions. Equation (10) takes the mean absolute percentage price change per transaction:

$$
LR_{MR}=\frac{100}{M}\sum_{m=1}^{M}\left|\frac{P_m-P_{m-1}}{P_{m-1}}\right|.
$$

Two stocks can have equal daily volume but different numbers of trades, and therefore different values of this statistic. The construction assumes that ordinary price changes are not strongly dependent on trade size, apart from large blocks. The review admits that the appropriate aggregation horizon is not fixed by the measure. Splitting one economic order into many reported trades can change transaction-based statistics without proportionately increasing accessible liquidity.

## Variance ratios, efficient prices, and multiple markets

Sections 4.2–4.3, pp. 102–106, interpret liquidity through the separation of permanent price changes and temporary deviations. The market-efficiency coefficient compares a long-interval variance with the variance expected from adding independent short-interval returns. For covariance-stationary short returns $r_t$, define

$$
VR(T)=\frac{\operatorname{Var}(r_t+\cdots+r_{t-T+1})}{T\operatorname{Var}(r_t)}
=1+2\sum_{s=1}^{T-1}\left(1-\frac{s}{T}\right)\rho_s,
$$

where $\rho_s=\operatorname{Cov}(r_t,r_{t-s})/\operatorname{Var}(r_t)$. A random walk with uncorrelated increments has $VR(T)=1$. Negative short-run correlation, as with bid–ask bounce, can produce a ratio below one; positive correlation from slow information incorporation can produce a ratio above one. These are model-dependent interpretations rather than a complete taxonomy of liquidity costs.

The displayed development on p. 103 is internally inconsistent. It defines a quantity called $\rho(1)$ with twice the variance in its denominator, then uses a general formula appropriate to the ordinary autocorrelation. Equation (13) also reverses the short/long variance ordering relative to the preceding discussion. With standard autocorrelation, $VR(2)=1+\rho_1$, not $1+2\rho_1$. The coherent identity above is derived directly by expanding the variance of the sum. For a stationary AR(1) return process, substitute $\rho_s=\phi^s$. The printed expression instead has an unbound exponent $k$. Coding the survey literally would therefore produce a normalization error.

The reported example horizons are two days versus half an hour, one day versus one hour, and two days versus one day. The ratio depends on this choice and on market hours, overnight returns, and sampling conventions. A ratio near one does not establish low trading costs; offsetting sources of positive and negative serial dependence can cancel. Nor is a random walk an observable benchmark immune to specification error.

The VAR discussion writes transaction prices as an efficient common component plus stationary pricing errors. For two venues,

$$
p_t=\begin{bmatrix}1\\1\end{bmatrix}V_t+S_t,\qquad
V_t=V_{t-1}+u_t,
$$

with the two components of $S_t$ zero-mean covariance-stationary. Their dispersion measures deviations from the common value; their difference is stationary, so the two prices are cointegrated. A moving-average representation $\Delta p_t=\sum_{j\geq0}\Psi_j\varepsilon_{t-j}$ gives the long-run impact matrix $\Psi(1)=\sum_j\Psi_j$. The common-trend restriction makes its rows identical in a correctly normalized two-price system. Calling that common row $\psi$, the efficient-price innovation variance is $\psi\Omega\psi'$, where $\Omega=\operatorname{Var}(\varepsilon_t)$.

If venue innovations are uncorrelated, each variance contribution is straightforward to attribute. With contemporaneous covariance, the attribution is not unique. Orthogonalizing innovations produces information-share bounds under alternative orderings rather than one uniquely identified causal contribution. The survey discusses alternatives allowing a generic integrated common factor rather than imposing a random walk, but emphasizes that a nonmartingale factor need not represent an optimally updated expectation. It also warns that forcing asynchronous markets onto apparently simultaneous observations can discard information about price leadership. Lag order, cointegration estimation, orthogonalization ordering, and synchronization choices are therefore part of the result, not incidental data-cleaning decisions.

## Quoted spreads and the Roll benchmark

Let $A_t$ and $B_t$ be best ask and bid. Equations (14)–(15) define the absolute spread $S_t=A_t-B_t$, midpoint $M_t=(A_t+B_t)/2$, and relative spread $S_t/M_t$. The last is a fraction; multiply by 100 for percent or 10,000 for basis points. These quotes measure the terms available for a stated displayed size. They do not fully measure block impact, price improvement, or execution outside the posted spread.

Roll's model, pp. 109–111, assumes an efficient value following a random walk with drift and constant spread $S$:

$$
V_t=V_{t-1}+\mu+\epsilon_t,\qquad P_t=V_t+\frac{S}{2}Q_t.
$$

The trade indicator $Q_t$ is $+1$ for an ask-side buyer-initiated trade and $-1$ for a bid-side seller-initiated trade. To obtain the stated covariance, signs must be independent over time, equally probable, and independent of efficient-price innovations; serially uncorrelated public news alone is insufficient. Then

$$
\Delta P_t=\mu+\epsilon_t+\frac{S}{2}(Q_t-Q_{t-1}),\qquad
\operatorname{Cov}(\Delta P_t,\Delta P_{t-1})=-\frac{S^2}{4}.
$$

An implied spread is $\widehat S=2\sqrt{-\widehat c_1}$ when the estimated first-order covariance $\widehat c_1$ is negative. The source prints a sample cross-product mean minus the squared sample mean in equation (20). Small-sample conventions for the two lagged means and denominator need to be stated in code. A nonnegative estimated covariance provides no real-valued Roll estimate under the model; clipping it to zero is an additional implementation choice, not evidence of zero costs.

The p. 109 bullet gives $\operatorname{Cov}(\Delta P_t,\Delta P_{t-1})=-1$ where the subsequent derivation requires $\operatorname{Cov}(\Delta Q_t,\Delta Q_{t-1})=-1$. This distinction is essential dimensionally. The negative price covariance is in squared currency units and equals $-S^2/4$.

The benchmark isolates transitory bounce under restrictive assumptions. Information-driven quote changes, inventory adjustments, serially correlated trade signs, time-varying spreads, and expected-return variation can contaminate it. The survey reports market differences from Huang–Stoll's dealer-versus-auction comparison, but provides no full sampling table or uncertainty measures. Such comparisons are evidence about a particular institutional setting, not proof that modern dealer markets lack adverse selection.

## Information, inventory, and the Stoll decomposition

Glosten's extension separates an order-processing fraction $\gamma$ from an information fraction $1-\gamma$. The survey's equation (21), p. 112, omits the trade sign from the information-driven value change, although its prose says value responds to that sign. The printed equations do not imply its equation (23). One internally consistent reconstruction is

$$
\Delta V_t=\mu+(1-\gamma)\frac S2Q_t+\epsilon_t,\qquad
P_t=V_t+\gamma\frac S2Q_t.
$$

Under the independent-sign assumptions this gives $\Delta P_t=\mu+\epsilon_t+(S/2)Q_t-\gamma(S/2)Q_{t-1}$ and covariance $-\gamma S^2/4$, as reported. The reconstruction makes explicit that $V_t$ is the post-trade value. With $\gamma=1$ it returns to Roll; with $\gamma=0$ the transitory covariance vanishes despite information-related trading costs.

Stoll's model adds an explicit reversal probability $\theta$ and quote-adjustment parameter $\lambda$. To match equations (24)–(26), define $\theta=\Pr(Q_t\ne Q_{t-1})$. The source incorrectly prints an equality in this definition, then uses inequality in the adjacent explanation. Conditional on an initial ask-side transaction, reversal generates a price change $-(1-\lambda)S$ and continuation a change $+\lambda S$; starting at the bid reverses these signs. The two price-change case statements on p. 114 print the same signs for both initial conditions and thus cannot both produce the displayed conditional expectations. The coherent expectations are

$$
E[\Delta P_t\mid Q_{t-1}=+1]=-(\theta-\lambda)S,\qquad
E[\Delta P_t\mid Q_{t-1}=-1]=+(\theta-\lambda)S.
$$

The realized spread is $s=2(\theta-\lambda)S$. Its fraction of the quoted spread is $2(\theta-\lambda)$; the remaining information fraction is $1-2(\theta-\lambda)$. The survey's prose puts $S$ inside an expression described as a fraction, another dimensional error.

The model's identifying moments are

$$
\operatorname{Cov}(\Delta P_t,\Delta P_{t+1})
=S^2\{\lambda^2(1-2\theta)-\theta^2(1-2\lambda)\},
$$

$$
\operatorname{Cov}(\Delta A_t,\Delta A_{t+1})
=\operatorname{Cov}(\Delta B_t,\Delta B_{t+1})
=S^2\lambda^2(1-2\theta).
$$

Table 1, p. 116, illustrates their identifying logic. Pure processing has $\theta=1/2,\lambda=0$: negative transaction covariance $-S^2/4$ and zero quote covariance. Pure information has $\theta=1/2,\lambda=1/2$: both covariances are zero. The inventory case has $\theta>1/2,\lambda=1/2$: both are negative, between $-S^2/4$ and zero. Covariance signs alone do not estimate a mixture without the model's constant-spread and transition assumptions.

The survey describes realized-price comparisons at four horizons: a first trade between five and ten minutes, the first trade at least five minutes later, a first trade between 30 and 35 minutes, and the first trade at least 30 minutes later. Too short a horizon can capture continuation before reversal; too long a horizon introduces unrelated news. Those timing rules are different experiments and should remain separate. The text provides no universal optimal horizon or numerical robustness table.

## Huang–Stoll: why predictable order flow matters

The three-part model on pp. 117–119 uses $\eta$ for information, $\delta$ for inventory, and $1-\eta-\delta$ for processing. With constant traded spread $S$, the baseline equations are

$$
\Delta V_t=\eta\frac S2Q_{t-1}+\epsilon_t,\qquad
M_t=V_t+\delta\frac S2\sum_{i=1}^{t-1}Q_i,
$$

$$
P_t=M_t+\frac S2Q_t+u_t.
$$

The cumulative signed flow is an inventory proxy under the model's trade-size convention, not measured dealer inventory. The observation error $u_t$ accommodates transactions that do not lie exactly on the modeled effective half-spread. Differencing identifies only $\delta+\eta$ from the immediate midpoint response. A two-term transaction-price regression cannot separately label its information and inventory effects.

Introduce $E[Q_{t-1}\mid Q_{t-2}]=(1-2\theta)Q_{t-2}$, where $\theta$ is the reversal probability. Efficient-value changes must respond to unexpected flow, giving

$$
\Delta V_t=\eta\frac S2\{Q_{t-1}-(1-2\theta)Q_{t-2}\}+\epsilon_t.
$$

It follows that

$$
\Delta P_t=\frac S2Q_t+(\delta+\eta-1)\frac S2Q_{t-1}
-\eta\frac S2(1-2\theta)Q_{t-2}+\zeta_t,
\qquad \zeta_t=\epsilon_t+u_t-u_{t-1}.
$$

Joint estimation with the sign-transition equation identifies the three fractions, subject to the noise and conditional-moment assumptions. The implementation consequence is visible algebraically: if $\theta=1/2$, the identifying second-lag coefficient vanishes and this specification cannot separately recover $\eta$ and $\delta$ from it. Near that value the separation can be weak. If $u_t$ is independent observation noise, differencing it also induces serial dependence in the regression disturbance, so independent-error standard errors are not automatically justified.

The survey reports, for actively traded large-cap stocks in 1992, average processing, information, and inventory shares of 61.8%, 9.6%, and 28.7%, respectively. They sum to 100.1% because of reported rounding. These are percentages of the modeled traded spread, not percentages of returns or asset value. The discussion attributes a smaller information fraction for large trades to negotiation outside the market. It supplies neither the full sample selection nor estimates by size with confidence intervals, so this should remain a reviewed interpretation rather than a calibrated universal rule.

## Joint quote and transaction-return restrictions

The final empirical framework, pp. 119–122, moves to logarithms. Let $P_t$ be log transaction price, $M_t$ log midpoint, and $W_t=P_t-M_t$. Then transaction returns satisfy $R_t^p=R_t^m+W_t-W_{t-1}$. Positive $W$ means a transaction above the midpoint, normally a public purchase; the text's phrase “public dealer purchases” is ambiguous about whose side is being described. The claim that effective spreads are always less than quoted spreads also requires trades to remain inside or at the relevant quotes; the accounting identity alone does not guarantee it.

The quote-return regression includes lagged quote returns, lagged S&P 500 futures returns, $W_{t-1}$, cumulative stock volume $H_{t-1}$, large-buy and large-sell indicators, and depth imbalance. In compact form,

$$
R_t^m=\eta_0+\eta_1R_{t-1}^m+\eta_2R_{t-1}^{F}+\eta_3W_{t-1}
+\eta_4H_{t-1}+\eta_5L_{t-1}^{A}+\eta_6L_{t-1}^{B}+\eta_7Z_{t-1}+\epsilon_t.
$$

The large-trade indicators require volume strictly above 10,000 shares, with $L^A=1$ when $W>0$ and $L^B=1$ when $W<0$. The depth variable is log ask depth minus log bid depth. Futures returns proxy early incorporation of public information; lagged quote returns allow delayed adjustments; deviations from midpoint carry trade information. The review describes $H$ as cumulative traded volume without enough detail to reconstruct a signed dealer-inventory series, so the variable definition needs verification before reproducing that interpretation.

Assuming $W_t=\rho W_{t-1}+\xi_t$ yields a second regression with the same covariates but the $W_{t-1}$ coefficient constrained to $\eta_3^p=\eta_3+\rho-1$. This separates an information term $\eta_3$, an order-arrival persistence term $\rho$, and mechanical bounce $-1$. The equations can be estimated jointly by GMM. The survey cites an application to the 20 most actively traded NYSE stocks, but does not state a complete instrument list, GMM weighting construction, sampling interval, data filters, or covariance estimator.

Pure-processing restrictions include $\eta_3=0,\eta_3^p=-1$; pure-information restrictions include $\eta_3=1,\eta_3^p=0$. Inventory and induced-arrival theories impose intermediate coefficients and further sign restrictions. A negative $\rho$ represents reversal in transaction location relative to the midpoint. A positive depth coefficient is discussed as an inventory/order-inducement channel, whereas a negative one can indicate depth conveying selling pressure. These are joint model tests, not standalone causal interpretations of individual regression coefficients. Statistical power and correlations among regressors are missing from the survey's account.

## How to use the review without overstating its evidence

A reproducible measurement exercise must first specify the economic object: posted immediacy cost at stated size, realized concession at a stated horizon, response to signed flow, or a low-frequency characteristic used in expected-return tests. Next specify currency and share units, corporate-action treatment, trade and quote timestamps, venue aggregation, sign classification, overnight boundaries, and the sampling horizon. Intraday models additionally require an explicit noise process and inference robust to the serial dependence implied by the model. These are requirements implied by the formulas above; the survey does not supply a ready-made universal cleaning pipeline.

A further distinction is aggregation across stocks versus aggregation through time. Averaging stock-level price-impact ratios weights securities differently from dividing total price movement by total volume, while averaging quoted spreads by trade count emphasizes active periods rather than the time an investor actually faces each quote. The review supplies formulas for particular proxies but does not standardize these weights across them. Cross-measure comparisons should therefore retain the chosen weighting and sampling convention as part of each estimator’s definition.

The article's empirical content is mostly qualitative synthesis, with the 61.8/9.6/28.7 decomposition the principal numerical example. There is no new portfolio, cost-adjusted Sharpe ratio, trading rule, holdout period, or capacity experiment to reproduce. Its regulatory discussion argues that automation, transparent order priority, competition among intermediaries, and connections across fragmented venues can improve liquidity. Those are institutional arguments, not identified policy-effect estimates in this paper.

The practical value lies in matching data and assumptions to the question. Daily turnover and absolute-return/volume ratios are economical screening variables. Quote and transaction data can reveal more, but structural spread components require stronger assumptions and careful treatment of predictable flow. The source's transcription problems reinforce this distinction: a useful conceptual survey is not automatically a safe numerical specification. The original studies and their data protocols remain necessary for reproducing the empirical estimates reviewed here.

## Bibliographic guide

The source's references identify the main building blocks as Roll (1984), *A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market*; Glosten (1987), *Components of the Bid-Ask Spread and the Statistical Properties of Transaction Prices*; Stoll (1989), *Inferring the Components of the Bid-Ask Spread: Theory and Empirical Tests*; Huang and Stoll (1994), *Market Microstructure and Stock Return Predictions*; Huang and Stoll (1997), *The Components of the Bid-Ask Spread: A General Approach*; Hasbrouck (1993), *Assessing the Quality of a Security Market*; and Amihud (2002), *Illiquidity and Stock Returns: Cross Section and Time Series Effects*. These references are background reviewed by Gabrielsen, Marzo, and Zagaglia; this note's source is the supplied 2012 article.
