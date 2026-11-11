# Trading Costs and Returns for U.S. Equities: Estimating Effective Costs from Daily Data

Joel Hasbrouck. *The Journal of Finance* 64(3), June 2009, pp. 1445–1477.

Source: [original PDF](../../Finance/MarketImpact_Hasbrouck_2009.pdf), 33 pages. References below use printed journal pages; PDF page 1 is p. 1445. All pages, figures and tables were inspected, including the four rotated pages of Table VI.

## Why this matters and what the paper contributes

Historical asset-pricing research often has daily stock prices extending to 1926 but reliable transaction-level quotes only for a much shorter period. A proxy that recovers actual execution costs from daily prices can extend liquidity research substantially. The difficulty is that ordinary daily price volatility is much larger than a narrow bid–ask bounce, and the standard Roll estimator is undefined whenever the estimated first-order price-change covariance is positive.

Hasbrouck constructs a Bayesian Gibbs estimator of a market-factor extension of the Roll model. It estimates a nonnegative effective half-spread jointly with efficient-price volatility, market beta and unobserved trade directions. It handles days on which CRSP reports a quote midpoint rather than a trade. The innovation is an implementable daily-data estimator, its validation against high-frequency measurements, and its application to the relation between costs and returns over 1926–2006.

The daily estimate has a pooled Pearson correlation of **0.965** with the high-frequency effective-cost measure in a 1993–2005 comparison sample. This is strong evidence for an annual cross-sectional proxy, not proof of accurate estimation for every highly liquid stock or at every frequency. The paper explicitly warns that monthly estimation from about twenty daily observations can be dominated by the prior.

In pricing tests, high-cost stocks generally have higher gross returns. The relation is concentrated in January and often displaces the explanatory role of size. Its magnitude is too large to reconcile easily with compensation for the measured average level of investor turnover. Evidence that common *changes* in effective costs command a separate risk premium is much weaker. The paper therefore supports a useful measurement method more decisively than a complete economic explanation of the return pattern.

## 1. What is being measured

For a single buyer-initiated trade, effective cost is the log transaction price minus the log midpoint of the prevailing quote; for a sale the sign reverses. It is a one-way proportional cost, approximately a percentage for small log differences. A round trip pays roughly twice this amount when conditions are unchanged. It is not the full quoted spread.

The measure concerns execution relative to the prevailing midpoint. A parent order split into many trades may move that midpoint through earlier executions. Effective cost for each child trade does not capture that entire parent-order implementation shortfall. The paper accordingly compares effective costs with a separate price-impact coefficient and does not assume they are identical liquidity objects.

Table I contains a typographical definition of excess returns as subtracting the market return. The pricing equations and accompanying text unambiguously use the risk-free rate: $R_{it}=r_{it}-r_{ft}$. That is the convention used below.

## 2. Latent-price model and identification

Let $p_t$ be the observed log trade price and $m_t$ the efficient log midpoint immediately before the trade. The basic Roll model is

$$
m_t=m_{t-1}+u_t,\qquad p_t=m_t+cq_t,
$$

where $q_t\in\{-1,+1\}$ is the trade sign, equally likely a priori, and $u_t$ is an independent mean-zero efficient-price innovation. The effective cost $c$ is constant over the estimation interval. At the daily frequency, $q_t$ describes the last trade of the day; it is not the sign of aggregate daily order flow.

Differencing eliminates the latent price level:

$$
\Delta p_t=c(q_t-q_{t-1})+u_t.
$$

With independent signs and innovations, $\operatorname{Cov}(\Delta p_t,\Delta p_{t-1})=-c^2$. The classical estimator is the square root of the negative sample covariance. A positive sample covariance makes it infeasible; assigning zero solves the arithmetic problem but produces a pile-up at zero. About one-third of firm-years in the comparison sample have this outcome.

The paper's primary empirical specification adds the market return:

$$
\Delta p_t=c\Delta q_t+\beta_m r_{mt}+u_t,
\qquad u_t\overset{\mathrm{iid}}\sim N(0,\sigma_u^2).
$$

The market term helps distinguish efficient price movements from reversible trading effects. It assumes that market returns are independent of the trade-direction changes. A market portfolio can diversify idiosyncratic bid–ask bounce, but systematic closing-price behavior would challenge the assumption. The model also assumes Gaussian, serially independent innovations within a firm-year and constant $c$ and $\beta_m$ over that interval.

For a CRSP no-trade observation reported as the midpoint, fix $q_t=0$, so $p_t=m_t$. Deleting these dates would make successive efficient-price innovations span varying numbers of trading days and introduce heteroskedasticity. Retaining them as ordinary trades would falsely attribute a zero-cost midpoint observation to bid or ask execution. Fixing the sign to zero handles the known observation mechanism directly without estimating a no-trade probability.

The observed-price likelihood is invariant to changing the sign of both $c$ and every $q_t$. A nonnegative prior for $c$ resolves this mirror-image identification problem using the economic meaning of costs. It is not evidence that the unconstrained likelihood alone distinguishes buys from sells.

## 3. Gibbs sampler in implementable form

Let $n=T-1$ be the number of differenced observations. Conditional on the current signs, define the design matrix with rows $(q_t-q_{t-1},r_{mt})$, response $y_t=\Delta p_t$, and coefficient vector $b=(c,\beta_m)'$. The model is ordinary Gaussian regression conditional on latent signs.

With prior mean $b_0$ and covariance $V_0$, and current $\sigma_u^2$, calculate

$$
V_*=(X'X/\sigma_u^2+V_0^{-1})^{-1},
\qquad
b_*=V_*(X'y/\sigma_u^2+V_0^{-1}b_0).
$$

Draw from $N(b_*,V_*)$ restricted to $c\ge0$. This is a jointly truncated regression posterior, not independent draws from its univariate marginals. Conditional-draw or truncated-normal routines must preserve the posterior correlation between cost and beta.

The empirical coefficient priors are independent $c\sim N^+(0,0.05^2)$ and $\beta_m\sim N(1,1)$. The zero in the half-normal notation is the underlying untruncated normal location; the actual prior mean of $c$ is $0.05\sqrt{2/\pi}\approx0.0399$. This distinction is consequential when the true cost is far below four percent.

Given coefficients and signs, compute $u_t=y_t-X_tb$ and draw the innovation variance from its inverse-gamma conditional posterior. For an unambiguous implementation, define a shape–scale convention by

$$
f(s\mid a,b)\propto s^{-a-1}\exp(-b/s),\qquad s>0.
$$

Then the conjugate update is $a_*=a_0+n/2$ and $b_*=b_0+\sum_tu_t^2/2$. The paper prints its update as $\beta_*=[\beta^{-1}+\sum u_t^2/2]^{-1}$ and reports prior hyperparameters $\alpha=\beta=10^{-12}$. Thus its printed $\beta$ is an inverse-scale convention in that display. Mapping both printed statements literally to the density above gives $b_0=10^{12}$, which is not the usual weak small-hyperparameter prior and would dominate annual daily returns. The density convention or reported hyperparameter needs verification against the original implementation before claiming exact numerical replication. One should not silently mix the printed update with a software library's different inverse-gamma convention. A reconstruction using $a_0=b_0=10^{-12}$ in the explicitly defined convention is a documented choice, not a uniquely established reading of both printed statements.

### Drawing the signs

For an interior date $t$, changing $q_t$ affects only innovations $u_t$ and $u_{t+1}$. Compute those two residuals twice, once with $q_t=+1$ and once with $q_t=-1$, holding all other current draws fixed. The log posterior odds are

$$
\ell_t=-\frac{u_t(+1)^2+u_{t+1}(+1)^2
-u_t(-1)^2-u_{t+1}(-1)^2}{2\sigma_u^2}.
$$

Draw $q_t=+1$ with logistic probability $1/(1+e^{-\ell_t})$. Computing log odds avoids numerical underflow from multiplying normal densities. The first sign affects only $u_2$; the last affects only $u_T$. Known midpoint signs remain zero throughout. Sweep sequentially, using freshly updated earlier signs and previous values of later signs.

The initialization sets unknown signs to the sign of the most recent price change, with the first sign arbitrarily positive, and initializes $\sigma_u^2=0.0004$. The paper does not spell out every tie-handling detail for zero price changes. Coefficients need no initial values because they are drawn first. Each empirical chain uses **1,000 sweeps**, discards the first **200**, and takes the mean of the remaining **800** draws for its reported point estimate. Experiments up to 10,000 sweeps reportedly do not materially alter mean estimates. Random seeds, multiple-chain diagnostics and effective sample sizes are not supplied.

A proper informative-enough coefficient prior is essential. Some sign configurations make $\Delta q_t$ identically zero, rendering the likelihood uninformative about $c$ for that sweep. In that case its draw is governed by the prior. Extremely diffuse priors can generate unrealistic excursions even if such configurations occur rarely.

## 4. What the estimator can resolve

The illustration simulates 250 observations with $\sigma_u=0.02$ and $\beta_m=0$. It uses exactly the same innovation and sign realizations for two series, changing only $c$ from **0.01 to 0.10**. For this illustration the cost prior is the more diffuse $N^+(0,1)$, and the chain runs **10,000 sweeps**, discarding **2,000**.

The 90% posterior regions in Figure 1 are large and negatively sloped when $c=0.01$, but compact around the truth when $c=0.10$. Large bounce makes signs easy to infer. Small bounce can instead be explained by different combinations of efficient volatility and transaction costs. These are Bayesian posterior regions, even though the caption uses confidence-region terminology.

A two-basis-point cost against daily volatility of several percent is intrinsically difficult to recover from one year of closing prices. Nonnegativity prevents an impossible estimate; it does not manufacture information. The prior can then pull estimates upward. Monthly samples of roughly twenty observations are especially problematic: apparent time variation can reflect prior shrinkage and sampling noise rather than economic liquidity variation. Grouping stocks into portfolios does not necessarily remove a common direction of bias.

Other mechanisms can also create daily return reversals, including inventory control, changing preferences or risk exposures. The estimator measures the component of daily price behavior consistent with its assumed transitory-cost model. The TAQ validation is therefore necessary; the mere existence of a Gibbs algorithm does not identify bid–ask costs independently of the maintained return process.

## 5. Data, sample selection and validation construction

The main sample is CRSP daily data for **1926–2006**, limited to ordinary common shares with share codes **10 or 11**, a valid price on the final trading day of the year, and no exchange-listing change or large split in the final three months. Effective costs are estimated annually using prices and dividends. The paper does not define the numerical threshold for a “large” split or fully specify every price/dividend adjustment and stale-price filter. Reproducing these eligibility conditions matters because they select the firm-years that enter later sorts.

The validation selects about **150 NASDAQ and 150 NYSE/Amex stocks per year**, using capitalization-stratified random draws, over **1993–2005**. Of 3,900 proposed firm-years, **3,777** match TAQ after requiring unique matching tickers, a correlation above **0.9** between TAQ and CRSP closing prices, and disagreement about whether trading occurred on fewer than **2%** of dates. These are matched firm-year observations, not necessarily 3,777 distinct companies. The random draw and exact exclusion list are not supplied.

The TAQ benchmark averages trade-level log effective costs, weighted by the trade's dollar value; unweighted averages give similar results. The prevailing quote is the most recent quote at least **two seconds before** the trade. This historical alignment convention is part of the experiment and is not a recommendation for present-day ultrafast data. The article notes that reporting conventions may have changed within the validation period. Complete trade-sign classification and quote-cleaning code are not reproduced.

A second TAQ measure estimates price impact from five-minute aggregates:

$$
\Delta p_{i\tau}=\lambda_i\,\mathrm{SignedSqrtDollarVolume}_{i\tau}+e_{i\tau}.
$$

The implementation text estimates this monthly and averages the monthly coefficients for annual comparisons. Table I instead describes annual estimation. That discrepancy should be resolved against code rather than blending the procedures. The exact aggregation of signed square-root trade values must also be preserved; it is not automatically equivalent to taking the square root of a net signed dollar total.

Daily competitors are the modified Roll moment estimate, the proportion of days with unchanged closing prices, and Amihud's mean absolute-return-to-dollar-volume ratio over positive-volume dates. The moment estimator uses trading days only and assigns zero to positive sample autocovariance. The paper omits the Pastor–Stambaugh measure from the individual-stock horse race because of its large individual-stock sampling error.

## 6. Validation results and interpretation

Table II gives mean TAQ cost **0.0106**, median **0.0054** and standard deviation **0.0146**. The Gibbs counterparts are **0.0112**, **0.0061** and **0.0141**. In approximate units, mean one-way costs are 106 and 112 basis points; these are averages of a broad capitalization-stratified historical cross-section, not present-day large-cap quotes. Both distributions are strongly right-skewed.

| Comparison with TAQ effective cost | Gibbs | Modified Roll |
|---|---:|---:|
| Pearson correlation | 0.965 | 0.878 |
| Spearman rank correlation | 0.872 | 0.636 |
| Pearson partial correlation | 0.943 | 0.805 |
| Spearman partial correlation | 0.678 | 0.382 |

Partial correlations control for log end-of-year share price and log market capitalization. Pearson and rank measures answer different questions: rank fidelity is lower than level correlation, although Gibbs remains better than the moment estimator in these comparisons. The reported correlations pool firms and years; annual cross-sectional averages are similar. The lowest annual Gibbs–TAQ Pearson correlation is **0.903 in 2005**.

Regressing the TAQ estimate on the daily Gibbs estimate gives intercept **0.001** and slope **0.935**, close to but not exactly the ideal zero and one. Neither regression standard errors nor a full interval for every validation correlation is reported. The analysis validates measurement on matched observations; it is not an out-of-time prediction contest.

TAQ effective cost and the TAQ impact coefficient correlate **0.513**. Gibbs cost correlates **0.450** with that impact coefficient, while Amihud's measure correlates **0.668**. Thus the strongest proxy for effective spread is not the strongest proxy for a different liquidity dimension. Selecting a measure should follow the economic target.

In Figure 2 the TAQ median declines from roughly **1% in 1993 to 0.4% in 2005**, while the 95th percentile declines from about **5% to 2%**. Changes in market design and sample composition can both contribute. Cross-sectional dispersion exceeds the aggregate time-series movement, helping explain why annual cross-sectional validation looks especially strong.

## 7. Long historical costs and closing-trade directions

Historical costs peak after the 1929 crash and in the Depression, especially among small stocks. Low prices with a fixed one-eighth-dollar tick are a plausible contributor to high proportional costs. After the Depression, average costs for the upper three NYSE/Amex capitalization quartiles remain below about 1%; the smallest quartile carries most of the long-run variation. NASDAQ estimates shown in the historical plots begin in **1985**. Changes in listing and delisting composition limit causal interpretations of trends.

The sampler also provides posterior mean signs $\widehat q_{it}$. Across roughly **22,000 firms and 21,520 trading dates**, the pooled mean is **−0.008** and standard deviation **0.379**. Posterior means lie between −1 and +1 and are shrunk toward zero; midpoint dates are fixed at zero. Their variance **0.143** should not be compared mechanically with the unit variance of actual latent binary signs as if both were observed versions of the same statistic.

Average first-order autocorrelation of estimated signs is **−0.32**, while their autocovariance is **−0.042**. The latter is small relative to unit latent-sign variance, but neither statistic is a clean independent test of the imposed latent-sign process. Posterior estimates reuse neighboring prices and contain shrinkage. Correlations between $\Delta\widehat q$ and market returns have first, median and 99th percentiles **−0.091, −0.004 and 0.072**.

Cross-stock estimated trade-direction commonality is modest in magnitude but statistically detectable in the very large panel: mean correlation with the daily cross-sectional average is **0.093**. Tests using cross-firm independence should not be mistaken for dependence-robust inference. Quarter-end and year-end closing trades are more ask-oriented in Figure 4, consistent with institutional trading or window dressing. The evidence does not identify that mechanism causally.

This seasonality matters because transaction-based monthly returns contain endpoint bid–ask effects. However, December closes tend to be slightly ask-oriented, while January closes show little directional tendency. A simple story in which December bid prices reverse to January ask prices therefore does not explain the subsequent January cost–return result.

## 8. Asset-pricing experiment: timing, portfolios and inference

Expected excess returns are modeled as factor compensation plus characteristics:

$$
E[R_t]=B\lambda+Z_t\delta,
\qquad R_t=a+Bf_t+u_t.
$$

The factors are either the market excess return alone or the three Fama–French market, size and book-to-market factors. Characteristics include a constant, prior-year Gibbs cost, January, and interactions of January/non-January indicators with cost and relative size. Relative size is log market capitalization at the previous year-end minus the sample median of log capitalization, then averaged across portfolio constituents.

The cost specification uses either one coefficient on $c$ or separate coefficients on $cJ_t$ and $c(1-J_t)$, never all three simultaneously. The full panel equation is

$$
R_{it}=\delta_0+B_i\lambda+\delta_JJ_t
+\delta_{cJ}c_{it}J_t+\delta_{cN}c_{it}(1-J_t)
+\delta_{sJ}s_{it}J_t+\delta_{sN}s_{it}(1-J_t)+e_{it}.
$$

Portfolios form annually using prior-year capitalization, cost and Gibbs beta; current-year return information is not used for membership. Returns and characteristics are equally weighted. A benchmark uses **ten NYSE size portfolios, 1927–1998**. The main NYSE sample uses **25 portfolios, 1927–2006**, formed first into five Gibbs-beta groups and then five cost groups within each. The analogous Amex and NASDAQ samples cover **1963–2006** and **1985–2006**. The reported timing for NASDAQ should be followed literally; the source does not fully reconcile the first formation-year data requirement with the historical plot starting in 1985.

The factor loadings used in the pricing regression differ from the prior-year Gibbs betas used in formation. They are OLS time-series loadings of portfolio returns on factors over the **full pricing sample**. Consequently this is an explanatory asset-pricing test, not a real-time return forecast using recursively estimated pricing betas.

Joint GMM estimation uses the time-series regression normal equations and the cross-sectional pricing normal equations:

$$
E[u_t]=0,\quad E[f_t\otimes u_t]=0,
\quad E[B'(R_t-B\lambda-Z_t\delta)]=0,
\quad E[Z_t'(R_t-B\lambda-Z_t\delta)]=0.
$$

Point estimates equal the associated two-pass OLS procedure. GMM standard errors account for estimated factor loadings and heteroskedasticity; the paper relates them to the Shanken correction under normality. It does not describe a general serial-correlation bandwidth or a correction propagating every Gibbs cost estimate's posterior uncertainty. Those should not be assumed merely because the final estimator is called GMM.

## 9. Pricing results: strong seasonality, difficult economic magnitude

The following entries reproduce Table VI's three-factor specification (10), which includes cost, January and relative-size interactions. Parentheses contain the reported GMM $t$ statistics.

| Sample | January cost coefficient | Other-month cost coefficient | January relative-size coefficient |
|---|---:|---:|---:|
| NYSE size benchmark, 1927–1998 | 3.9220 (2.09) | 1.2858 (1.51) | 0.0044 (0.40) |
| NYSE beta/cost portfolios, 1927–2006 | 3.2411 (2.03) | 0.9815 (1.46) | −0.0078 (−1.19) |
| Amex, 1963–2006 | 6.2380 (4.42) | 1.0028 (3.16) | 0.0191 (1.48) |
| NASDAQ, 1985–2006 | 1.6187 (2.07) | 0.0442 (0.24) | −0.0088 (−1.12) |

A coefficient of 3.2411 means that a one-percentage-point increase in the log cost characteristic is associated with about **3.24 percentage points higher January gross excess return**, holding the other regressors fixed. It is not a 3.24-basis-point effect. January relations are statistically stronger than other-month relations. In this demanding specification, non-January NYSE coefficients have positive point estimates but do not pass a conventional two-sided 5% threshold; Amex does, while NASDAQ has essentially no estimated non-January effect.

Without seasonal decomposition, the three-factor cost coefficients are **1.3733** for the size benchmark, **1.1446** for main NYSE, **1.4107** for Amex and **0.2676** for NASDAQ, with $t$ statistics **1.92, 1.94, 3.56 and 1.64**, respectively. Formal significance therefore depends on sample and specification. The robust qualitative observation is concentration of the relation in January, not universal rejection in every column.

The straightforward cost-compensation story is strained by magnitude. A round trip held for two months incurs approximately $2c$, suggesting a coefficient of one on $c$ in expected monthly gross return and six annual round trips. Historically observed average NYSE turnover is much lower; the article cites **12% in 1960 and 103% in 2005**. January coefficients near four require extremely active marginal investors under this simple story. Marginal and average investors need not be identical, but that possibility is not an estimated explanation.

Two robustness exercises matter. Reestimating costs on years ending in June and forming portfolios at June-end leaves the seasonal result essentially unchanged, reducing concern about a mechanical December estimation/formation artifact. Subtracting squared prior-year portfolio-average cost from monthly excess return addresses a transaction-price return bias discussed by Blume and Stambaugh. Coefficients and $t$ statistics fall slightly without changing the overall result. This adjustment is not a full deduction of actual strategy trading costs and must not be labeled a net-return backtest.

## 10. Dynamic costs and the weaker liquidity-risk evidence

To estimate variation without repeatedly fitting very short samples, replace constant cost with $c_{it}=Z_{it}\gamma_i$ directly inside the observation equation:

$$
\Delta p_{it}=(q_{it}Z_{it}-q_{i,t-1}Z_{i,t-1})\gamma_i
+\beta_{im}r_{mt}+u_{it}.
$$

Conditional on signs, this is again linear regression. Drawing signs requires using the current and lagged costs separately. A nonnegative coefficient alone does not guarantee $Z_{it}\gamma_i\ge0$ for arbitrary signed regressors; an implementation needs compatible restrictions over the actual covariate domain.

A latent common-cost model is $c_{it}=\gamma_{0i}+\gamma_{1i}z_t$. Half-unit-normal priors on $z_t$ help normalize scale and constrain its sign, but cost positivity also requires compatible loading/intercept restrictions. The paper does not give all those details in this short extension. It assumes cross-firm independence of $q$ and $u$ conditional on the common structure, so the market factor accounts for shared efficient-price innovations.

Estimated common cost factors correlate with average TAQ effective costs at **0.447 daily** and **0.670 monthly**. The cross-sectional correlation between factor loadings inferred from daily prices and those estimated from daily TAQ costs is only **0.328**, with modest gains from portfolio aggregation. In the full historical return sample, cost-factor innovations add little explanatory power and their estimated price of risk is insignificant and changes sign. Complete details are referred to an earlier working paper.

This is an important separation: annual effective-cost levels validate strongly, but factor innovations and liquidity-risk exposures validate much less strongly. The published source does not support transferring the 0.965 level correlation to every generated dynamic liquidity variable.

## Reproduction limits and practical use

The sampler's latent-sign conditionals, coefficient priors, iteration counts and annual validation design are unusually explicit. Exact replication still needs the inverse-gamma convention resolved, original preprocessing and split thresholds, random sample/chain seeds, TAQ sign and quote filters, handling of failed or short firm-years, and the detailed dynamic-factor implementation. The article's suggested source code and historical estimates are not embedded in this PDF.

A useful reconstruction should validate against high-frequency effective costs on the same sample before interpreting estimated return premia. It should retain posterior uncertainty, inspect sensitivity to annual versus shorter windows and to the cost prior, and distinguish one-way spread costs from parent-order impact. The results establish a strong historical measurement tool and a persistent seasonal characteristic relation. They do not identify a unique causal liquidity premium, eliminate generated-regressor uncertainty, or demonstrate an implementable after-cost investment strategy.
