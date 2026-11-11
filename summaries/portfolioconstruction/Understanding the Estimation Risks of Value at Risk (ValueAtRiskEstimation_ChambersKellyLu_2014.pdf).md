# Understanding the Estimation Risks of Value at Risk

Donald R. Chambers, Michael A. Kelly, and Qin Lu. *The Journal of Alternative Investments* 16(3), Winter 2014, pp. 64–85. Source: [ValueAtRiskEstimation_ChambersKellyLu_2014.pdf](../../Finance/ValueAtRiskEstimation_ChambersKellyLu_2014.pdf). All 23 supplied PDF pages were read visually: 22 article pages including endnotes and references, followed by a journal contents page. Printed page numbers equal PDF page numbers plus 63 for the article.

## Why this matters

A VaR number depends on the estimator, portfolio representation, return horizon, and available data. Treating a quoted confidence level as a guarantee conceals all four dependencies. This paper organizes the main estimation approaches and shows why methods that agree for approximately Gaussian returns can disagree dramatically for alternative investments. Its empirical illustration deliberately gives three return series identical means and volatilities. The remaining differences in VaR therefore expose distribution shape and estimation-method effects rather than simple differences in leverage or average return.

The contribution is primarily a methodological synthesis and a controlled descriptive comparison, rather than a new universal VaR estimator. The article brings historical quantiles, conditional quantile regression, volatility models, extreme-value methods, Cornish–Fisher approximations, nonlinear portfolio exposures, normal mixtures, and jump diffusion into one implementation framework. Its most useful result is a warning supported by numbers: matching the first two moments does not match tail risk, and adding estimated higher moments does not automatically improve a quantile estimate.

The authors also distinguish a risk statistic from a risk-management system. A quantile omits the size of losses beyond it; stale marks can suppress measured volatility; changing positions make historical portfolio returns an imperfect proxy for current exposure; and compensation or capital rules can encourage positions whose risks the chosen estimator misses. Those are mechanisms, not estimated causal effects in this paper. The empirical section is not an out-of-sample forecasting competition or a demonstration that any single method has correct future coverage.

## Probability, sign, horizon, and units

Use $R_h$ for a portfolio return over horizon $h$ and $p$ for the lower-tail probability, such as $p=0.01$. Define the return quantile

$$
q_p(h)=\inf\{r:F_{R_h}(r)\ge p\}.
$$

For initial value $W>0$, a corresponding positive monetary loss VaR is $-Wq_p(h)$ when the quantile is negative. Most equations and the empirical tables in this article instead report the **signed return quantile**: a value of $-2.87\%$ is a loss threshold, not a positive capital requirement. For a continuous distribution, the probability of falling below this threshold is $p$; discreteness requires distinguishing strict and weak inequalities. VaR is neither a worst possible loss nor an expected tail loss.

The paper sometimes uses the same symbol for a low return quantile and a high loss quantile. This note keeps those objects separate. In the extreme-value formulas below, $L=-R$ denotes positive loss, and its target quantile is at probability $1-p$. All returns in equations are decimal fractions unless a displayed table explicitly gives percentages. Dollar quantities require multiplication by $W$ once, not twice.

The basic Gaussian return quantile is

$$
q_p=\mu+z_p\sigma,\qquad z_p=\Phi^{-1}(p).
$$

At $p=0.05$, $z_p\simeq-1.645$. The source's example has daily volatility $1.5\%$, negligible mean, and value \$100,000. Its signed threshold is $-2.4675\%$, or −\$2,467.50; expressed as a positive loss VaR, the amount is \$2,467.50. This is conditional on the normal model, not an empirical statement that an option portfolio is normally distributed.

With independent Gaussian increments having constant per-period mean and variance, an additive $h$-period return has quantile $h\mu+z_p\sqrt h\sigma$. That result does not justify mechanically scaling every estimated daily quantile by $\sqrt h$. Mean accumulation, changing conditional variance, dependence, nonlinear rebalancing, and simple-return compounding require separate treatment. The empirical demonstration estimates each horizon from returns measured at that horizon.

## Historical and conditional quantile approaches

Historical VaR ranks past outcomes and estimates a low order statistic. Its attraction is that it does not impose Gaussian shape. Its limitation is that the observed sample must represent the distribution relevant to current positions and the future horizon. A static portfolio's historical returns may be usable directly; a changing portfolio may instead require revaluing today's positions under historical factor moves. Backfilled strategy returns introduce additional model choices and potential data snooping. Smoothing and stale prices remain problems even when no parametric density is fitted.

A reproducible historical estimator must specify the observation window, simple versus log returns, data adjustments, treatment of missing observations, order-statistic index, and interpolation rule. With $n$ observations, the number expected in a tail of probability $p$ is only $np$. A monthly 1% quantile based on 232 observations is determined by roughly two or three outcomes. More history increases the number of observations but may combine different regimes or exposures. The paper emphasizes this tradeoff rather than supplying a universal optimal window.

The source also reviews quantile regression. A consistent implementation solves

$$
\widehat\beta_p=\arg\min_\beta\sum_t\rho_p(R_t-X_t^{\mathsf T}\beta),
\qquad
\rho_p(u)=u[p-\mathbf1\{u<0\}],
\qquad
\widehat q_{p,t}=X_t^{\mathsf T}\widehat\beta_p.
$$

Equation (1) in the article labels the minimized objective itself $q_t$. The fitted quantile is the predictor evaluated at the minimizing coefficient, as written here; the minimized check-loss value is not a return threshold. Regressors must also be available at the forecast origin. This is an estimate of a conditional quantile, not necessarily an estimate of conditional standard deviation, despite the source's occasional volatility terminology.

The CAViaR discussion introduces a dynamic quantile recursion of the form

$$
q_{p,t}=\beta_0+\sum_{j=1}^{m}\beta_jq_{p,t-j}
+g(\beta_{m+1},\ldots,\beta_{m+n};\mathcal F_{t-1}).
$$

A simple specialization includes a lagged quantile and $|R_{t-1}|$. The function, lag orders, initialization, estimation criterion, and parameter restrictions must be chosen before this becomes executable. The article supplies a family of models and an illustrative specification, not a fitted CAViaR model or numerical comparison in its empirical section.

## Conditional volatility and linear factor models

For a zero-mean EWMA model, the variance forecast is

$$
\sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)R_{t-1}^2.
$$

The source gives the familiar RiskMetrics values $\lambda=0.94$ for daily data and $0.97$ for monthly data. These are stated conventions, not estimates fitted in this article. Conditional normality then gives $q_{p,t}=z_p\sigma_t$. The source's $\sqrt h$ horizon extension is a modeling approximation when future variance changes; it is not a distribution-free property of EWMA forecasts.

A consistent GARCH(1,1) notation is

$$
R_t=\mu+\epsilon_t,\quad \epsilon_t=\sigma_tZ_t,
\qquad
\sigma_t^2=\omega+a\epsilon_{t-1}^2+b\sigma_{t-1}^2.
$$

For unit-variance independent innovations, forecast variances from origin $t$ satisfy

$$
v_1=\omega+a\epsilon_t^2+b\sigma_t^2,
\qquad
v_j=\omega+(a+b)v_{j-1},\quad j\ge2.
$$

The standard positivity conditions are $\omega>0$, $a,b\ge0$; $a+b<1$ gives a finite stationary unconditional variance in this specification. The article's equations (8) and (10) swap the labels on the lagged variance and squared innovation. The equations above use one consistent convention rather than importing that mismatch. The proposed multistep approximation is

$$
q_p(h)\approx h\mu+z_p\sqrt{\sum_{j=1}^{h}v_j}.
$$

Even with conditionally Gaussian one-period innovations, a multistep GARCH return need not be Gaussian conditional on today's information: future shocks change future variances. Summing forecast variances supplies a second moment, not automatically an exact Gaussian quantile. Heavy-tailed innovations require their own quantiles and horizon treatment. The paper discusses misspecification and estimation burdens but does not calibrate or backtest these models in its demonstration.

For jointly Gaussian factor returns $X_h\sim N(m_h,C_h)$ and a linear exposure vector $w$, the return $w^{\mathsf T}X_h$ has quantile

$$
q_p=w^{\mathsf T}m_h+z_p\sqrt{w^{\mathsf T}C_hw}.
$$

The source specializes to Brownian increments with $m_h=\alpha h$ and $C_h=h\Sigma$. Multiplication by portfolio value converts a fractional-return approximation to currency. Joint normality matters: individually normal marginals alone do not establish that every weighted combination is normal. Likewise, a weighted sum of constituent log returns is generally not the exact log return of a discretely rebalanced portfolio. A production calculation must state its exposure and P&L approximation rather than treating the distributional equation as a pricing model.

## Extreme-value estimates require an explicit tail convention

The article reviews both block extremes and peaks over a threshold. These are tail models, not methods that remove the need for distributional assumptions. Their usefulness depends on a suitable domain of attraction, a defensible threshold or block size, and treatment of temporal dependence. They exchange a model for the entire distribution for a model of its far tail.

For clarity, the following is a consistent **loss-tail reconstruction** of the source's formulas. Let the maximum of $n$ independent losses have approximate generalized extreme-value CDF

$$
H(x)=\exp\left\{-\left[1+\xi\frac{x-m}{s}\right]^{-1/\xi}\right\},
\qquad s>0,
$$

on its support. Since $H(x)\approx F_L(x)^n$, the one-period loss quantile at confidence $1-p$ is

$$
\operatorname{VaR}_{1-p}\approx m+\frac{s}{\xi}
\left\{[-n\log(1-p)]^{-\xi}-1\right\}.
$$

For $\xi=0$, take the continuous limit $m-s\log[-n\log(1-p)]$. Here $m,s,\xi$ are parameters for the block maximum, not the original single-period mean and standard deviation. The article uses minimum returns and a different shape-sign convention; mixing that convention with an upper loss tail reverses signs. Estimating the block law from $T=ng$ observations also creates a tradeoff: large blocks improve an extreme-value approximation but leave fewer blocks $g$ for parameter estimation.

For peaks over a loss threshold $u$, let $N_u$ of $N$ observations exceed $u$. A generalized Pareto approximation for the excess $Y=L-u\mid L>u$ is

$$
G(y)=1-\left(1+\xi y/\beta\right)^{-1/\xi},
\qquad y\ge0,\quad 1+\xi y/\beta>0,
$$

where $\beta>0$. The associated unconditional survival approximation is

$$
\Pr(L>x)\approx\frac{N_u}{N}
\left[1+\xi\frac{x-u}{\beta}\right]^{-1/\xi}.
$$

Setting this probability to $p<N_u/N$ gives

$$
\operatorname{VaR}_{1-p}\approx
u+\frac{\beta}{\xi}\left[\left(\frac{N_u}{Np}\right)^\xi-1\right].
$$

At $\xi=0$ the formula is $u+\beta\log[N_u/(Np)]$. This formulation makes the threshold and exceedance frequency explicit. The source moves between return minima and high-threshold exceedances and uses a location parameter in its GPD expression; those labels should not be transferred to code without identifying which tail and variable are being modeled.

The article does not choose a threshold, fit a tail shape, supply declustering rules, or report EVT forecasts for the demonstration. Its endnotes emphasize the block-size/sample-size tradeoff and threshold sensitivity. The formulas provide a method to implement once those inputs are supplied, not a numerical result about the two observed funds.

## Cornish–Fisher and nonlinear Gaussian exposures

The Cornish–Fisher expansion adjusts a normal quantile using standardized skewness $S$ and **excess** kurtosis $K$:

$$
z_{CF}=z_p+\frac{z_p^2-1}{6}S
+\frac{z_p^3-3z_p}{24}K
-\frac{2z_p^3-5z_p}{36}S^2,
\qquad q_p^{CF}=\mu+\sigma z_{CF}.
$$

Using ordinary kurtosis instead of excess kurtosis adds an erroneous three to $K$. More fundamentally, this is a truncated approximation near a reference distribution. The article itself warns that strong non-normality and extreme confidence levels can produce unreasonable values. Four sample moments do not identify a distribution, and the resulting expression is not guaranteed to define a valid monotone quantile function over all probabilities. A higher-order formula should therefore be checked against tail data, distributional constraints, or numerical inversion rather than presumed superior because it contains more moments.

The delta–gamma approach first approximates currency P&L as a quadratic function of factor changes:

$$
Q=\delta^{\mathsf T}X+\frac12X^{\mathsf T}\Gamma X,
\qquad X\sim N(m,C),
$$

with symmetric $\Gamma$. The coefficients are sensitivities in the chosen factor coordinates; the source notes that they need not equal unscaled option Greeks. Position mapping and pricing units are indispensable. Centering $X=m+Z$ gives

$$
Q=A+B^{\mathsf T}Z+\frac12Z^{\mathsf T}\Gamma Z,
\quad
A=\delta^{\mathsf T}m+\frac12m^{\mathsf T}\Gamma m,
\quad B=\delta+\Gamma m,
\quad Z\sim N(0,C).
$$

The cumulants needed for Cornish–Fisher are

$$
\kappa_1=A+\frac12\operatorname{tr}(\Gamma C),
$$

$$
\kappa_2=\frac12\operatorname{tr}[(\Gamma C)^2]+B^{\mathsf T}CB,
$$

$$
\kappa_3=\operatorname{tr}[(\Gamma C)^3]+3B^{\mathsf T}C\Gamma CB,
$$

$$
\kappa_4=3\operatorname{tr}[(\Gamma C)^4]
+12B^{\mathsf T}C\Gamma C\Gamma CB.
$$

Thus $\sigma_Q=\sqrt{\kappa_2}$, $S_Q=\kappa_3/\kappa_2^{3/2}$, and $K_Q=\kappa_4/\kappa_2^2$. Equations (28)–(30) provide the variance, skewness, and excess kurtosis; the mean above completes the implementation. These identities are exact for the specified quadratic Gaussian model. Cornish–Fisher remains an approximation to its quantile, and the quadratic P&L remains an approximation to the actual portfolio.

The source describes the resulting law as noncentral chi-square. In general, a Gaussian quadratic form is a weighted combination of such components, possibly with negative weights and residual Gaussian terms; it is not necessarily one ordinary noncentral chi-square variable. Characteristic-function inversion, suitable quadrature, or simulation can handle the more general law. None fixes a poor Taylor expansion far from today's market point. Deep out-of-the-money options and other strongly nonlinear tail exposures may require full repricing under scenarios. The paper reviews this tradeoff rather than reporting a newly calibrated derivatives portfolio.

## Normal mixtures and the jump-diffusion correction

The normal-mixture model selects one of two variance regimes:

$$
R_h=ah+Y\sigma_1\sqrt h Z_1+(1-Y)\sigma_2\sqrt h Z_2,
\qquad \Pr(Y=1)=\pi,
$$

where $Y,Z_1,Z_2$ are independent and the $Z$ variables are standard normal. The symbol $\pi$ here is a mixing probability, distinct from the tail probability $p$. This is a random choice of component, not the sum of two simultaneously active Gaussian returns. Both components have the same mean in the article's example. Consequently,

$$
\mu=ah,\qquad
v=h[\pi\sigma_1^2+(1-\pi)\sigma_2^2],\qquad S=0,
$$

$$
K=\frac{3\pi(1-\pi)(\sigma_1^2-\sigma_2^2)^2}
{[\pi\sigma_1^2+(1-\pi)\sigma_2^2]^2}.
$$

The article inserts these moments into Cornish–Fisher. For a finite univariate mixture, an alternative is to solve the exact mixture CDF numerically:

$$
\pi\Phi\left(\frac{q-ah}{\sigma_1\sqrt h}\right)
+(1-\pi)\Phi\left(\frac{q-ah}{\sigma_2\sqrt h}\right)=p.
$$

That equation is an implementation consequence of the stated model, not an additional empirical fit. A mixture need not be close to normal merely because its components are normal. Nor does this one-horizon mixture specify how regimes persist across time; horizon aggregation requires an explicit temporal model.

For the jump model, the source allows nonzero-mean normal jumps:

$$
R_h=ah+\sigma\sqrt h Z_0+\sum_{j=1}^{N_h}J_j,
\qquad N_h\sim\operatorname{Poisson}(\lambda h),
\qquad J_j\sim N(m_J,s_J^2),
$$

with independent Brownian, Poisson, and jump components. Equations (39)–(41) in the article omit terms involving $m_J$, even though equation (37) allows that mean to be nonzero. They give the correct simplified variance and zero skewness only when $m_J=0$. A self-contained correction follows from the cumulant generating function

$$
\log E[e^{tR_h}]=ah\,t+\frac12\sigma^2h\,t^2
+\lambda h\left[\exp\left(m_Jt+\frac12s_J^2t^2\right)-1\right].
$$

Its first four cumulants are

$$
\kappa_1=ah+\lambda h m_J,
\qquad
\kappa_2=\sigma^2h+\lambda h(m_J^2+s_J^2),
$$

$$
\kappa_3=\lambda h(m_J^3+3m_Js_J^2),
\qquad
\kappa_4=\lambda h(m_J^4+6m_J^2s_J^2+3s_J^4).
$$

The omitted variance component is the variance of the conditional mean as the jump count changes. Conditional symmetry of each normal component does not imply unconditional zero skewness when those conditional means differ. For $m_J=0$, the source's expressions reduce to $v=h(\sigma^2+\lambda s_J^2)$, $S=0$, and $K=3\lambda s_J^4/[h(\sigma^2+\lambda s_J^2)^2]$, as expected.

These corrected cumulants may be used in Cornish–Fisher, with its existing limitations. A more direct one-dimensional quantile calculation uses

$$
F_{R_h}(r)=\sum_{j=0}^{\infty}
\frac{e^{-\lambda h}(\lambda h)^j}{j!}
\Phi\left(\frac{r-ah-jm_J}{\sqrt{\sigma^2h+js_J^2}}\right).
$$

The no-jump component $j=0$ must be included; the article's intermediate moment sums start at one. Numerical truncation can be controlled by the omitted Poisson probability. This exact conditional-mixture representation is available even though the unconditional law is not normal. The article's claim that nonnormality prevents direct CDF calculation is too strong. No jump intensity, jump mean, or jump variance is estimated in its empirical comparison, so this correction should not be mistaken for a reproduction of a fitted jump model.

## Empirical design: hold mean and variance fixed

The demonstration uses three series: an Excel-generated pseudo-normal series, dividend-adjusted closing returns on the SPDR S&P 500 ETF **SPY**, and dividend-adjusted daily net asset values of the **Merger Fund, MERFX**, representing merger arbitrage. The main sample is **May 17, 1994–September 30, 2013**, selected because daily Merger Fund data are available over that interval. The authors report **4,879 daily returns**, **1,011 Friday-close-to-Friday-close weekly returns**, and **232 calendar-month returns**.

At each frequency, SPY supplies the target sample mean and standard deviation. The pseudo-normal and Merger Fund series are separately transformed to match those two moments. An explicit reconstruction is

$$
\widetilde R_{a,h,t}=\bar R_{SPY,h}
+\frac{s_{SPY,h}}{s_{a,h}}(R_{a,h,t}-\bar R_{a,h}).
$$

The scale is positive, so standardized skewness and excess kurtosis are unchanged by this transformation. The resulting Merger Fund series is labeled **Levered Merger Arb**. It is not the actual unscaled fund track record or a fully specified dynamically levered strategy with funding costs. Moreover, the three frequency-specific transformations need not be the returns of one single investable wealth process. They are controlled comparisons of distribution shape at each horizon.

The paper generates pseudo-normal observations using Excel's uniform random-number function and inverse normal CDF. It does not provide a seed or saved draw vector. It also does not state all conventions needed to reproduce the adjusted historical series, such as the exact vendor extract, nontrading-day treatment, return formula, or sample-moment and percentile-function options. Recalculating formulas from printed moments is possible; exact replication of the historical quantiles requires the original observations and these choices.

Exhibit 5 reports the following common first two moments and series-specific shape estimates. The column labeled “Kurtosis” behaves as **excess kurtosis**, as shown by the near-zero normal-series values and the definition used in equation (25).

| Frequency | Common mean | Common SD | SPY skewness | SPY excess kurtosis | Scaled MERFX skewness | Scaled MERFX excess kurtosis |
|---|---:|---:|---:|---:|---:|---:|
| Daily | 0.0423% | 1.2539% | 0.1182 | 10.1155 | −0.2096 | 35.4885 |
| Weekly | 0.1962% | 2.4964% | −0.5500 | 6.2188 | −0.6608 | 21.4156 |
| Monthly | 0.8125% | 4.4133% | −0.6632 | 1.0052 | −1.7151 | 5.1750 |

The pseudo-normal skewness/excess-kurtosis pairs are respectively $(-0.0065,0.0269)$, $(-0.0749,0.0817)$, and $(0.2288,-0.1078)$. These are finite-sample values, not exact zeros imposed by the construction. SPY's daily skew is positive even though its weekly and monthly skews are negative. The paper links this to large positive daily rebounds within a sharply negative October 2008. Declining kurtosis with longer return intervals is an observation about these samples; it does not identify a unique temporal mechanism or establish independent increments.

An introductory illustration uses a **different sample**, S&P 500 daily returns over **1993–2012**. There the reported daily SD is 1.21%, so three SDs equal 3.63%. A normal lower-tail probability beyond three SDs is approximately 0.135%, whereas the reported frequency of losses beyond 3.63% is 0.77%, about 5.70 times as large. The endnote compares normal-model conditional tail loss 3.97% with observed 5.25% and emphasizes that both event frequency and event size differ. This introductory illustration must not be merged with the main 1994–2013 SPY/MERFX dataset.

## What the quantile comparisons actually show

Exhibit 6 compares historical order statistics, a Gaussian plug-in quantile, and the four-moment Cornish–Fisher approximation. It does **not** empirically compare every method reviewed earlier: there are no estimated EVT, CAViaR, GARCH, delta–gamma, mixture, or jump forecasts in this table. Because all three series have matched first two moments, the Gaussian estimate is identical across assets at a given frequency and probability.

The 1% lower-tail return quantiles are:

| Frequency | Method | Pseudo-normal | SPY | Scaled MERFX |
|---|---|---:|---:|---:|
| Daily | Historical | −2.89% | −3.36% | −4.09% |
| Daily | Gaussian | −2.87% | −2.87% | −2.87% |
| Daily | Cornish–Fisher | −2.89% | −5.72% | −13.45% |
| Weekly | Historical | −6.02% | −6.77% | −8.12% |
| Weekly | Gaussian | −5.61% | −5.61% | −5.61% |
| Weekly | Cornish–Fisher | −5.79% | −9.97% | −18.91% |
| Monthly | Historical | −8.40% | −13.33% | −19.23% |
| Monthly | Gaussian | −9.45% | −9.45% | −9.45% |
| Monthly | Cornish–Fisher | −8.51% | −11.91% | −15.47% |

The daily empirical normal quantile is close to its fitted Gaussian value, which is consistent with a large sample from a normal generator. For SPY and scaled MERFX, the same daily Gaussian number misses the more negative historical 1% quantiles. But Cornish–Fisher moves much farther than the historical values: for scaled MERFX it produces −13.45% versus −4.09%. Adding skewness and kurtosis to a truncated expansion is not equivalent to recovering the observed tail.

The relative ordering also changes with probability. For scaled MERFX, the rest of the reported comparison is:

| Frequency | Tail probability | Historical | Gaussian | Cornish–Fisher |
|---|---:|---:|---:|---:|
| Daily | 5% | −1.59% | −2.02% | −1.20% |
| Daily | 10% | −0.89% | −1.56% | **1.63%** |
| Weekly | 5% | −3.32% | −3.91% | −3.28% |
| Weekly | 10% | −1.93% | −3.00% | **0.63%** |
| Monthly | 5% | −7.61% | −6.45% | −7.89% |
| Monthly | 10% | −3.69% | −4.84% | −4.79% |

The positive daily and weekly 10th-percentile Cornish–Fisher estimates are printed results, not missing minus signs. Independent substitution of Exhibit 5's rounded moments gives approximately **+1.62979%** and **+0.62945%**, respectively. At the daily 1% tail it gives **−13.45056%**. These checks reproduce the reported approximation from its inputs; they do not validate it as the true quantile. At very high excess kurtosis, the polynomial correction can dominate the baseline normal quantile and give a misleading tail description.

Using the same independent calculation for all three series and all three probabilities reproduces the displayed Gaussian and Cornish–Fisher rows to rounding. For example, the common daily Gaussian 1% value is −2.87471%, and the monthly SPY Cornish–Fisher 1% value is −11.91319%. The numerical precision is from recalculation using rounded table inputs, not from recovery of the original data. Historical quantiles cannot be reconstructed from these four moments.

The monthly sample illustrates sampling limitations even without intentional nonnormality. Its pseudo-normal historical 1% quantile is −8.40%, versus −9.45% from fitted mean and SD. The article describes the monthly 1% estimate as the second-worst observation, whereas the daily 10% estimate is around the 488th worst. A particular software percentile rule may interpolate rather than select exactly that rank; the source does not identify the rule. Either way, 232 observations provide very little direct information about a 1% tail. The paper does not supply confidence intervals or repeated-simulation coverage experiments for these historical estimates.

## Reproduction boundaries and practical interpretation

A faithful reproduction should first recover the adjusted SPY and MERFX observations and match the published dates, frequencies, and counts. It should calculate daily, weekly, and monthly returns from the chosen data convention; generate and retain the pseudo-normal draws; apply the moment-matching transformation separately at each frequency; and reproduce Exhibit 5 before computing VaR. Historical quantile indexing, sample SD, skewness, and excess-kurtosis conventions must be explicit. Then compute Gaussian and Cornish–Fisher estimates at $p=0.01,0.05,0.10$, preserving signed-return units and separating original table rounding from recalculated values.

The paper gives enough information to reproduce the parametric table arithmetic, but not the exact historical dataset or random realization. It gives model families and useful analytical formulas, but not all parameters, thresholds, initialization rules, or portfolio sensitivities for an empirical implementation of every family. Extending the demonstration to those methods would be new work and should be labeled accordingly. The same applies to rolling forecasts, out-of-sample backtests, bootstrap confidence intervals, transaction costs, liquidity horizons, and full derivatives repricing.

The empirical design isolates shape by equalizing means and SDs, but it does not eliminate estimation uncertainty in higher moments. Tail observations dominate sample kurtosis, and the smaller monthly sample has its own uncertainty. Nor is an empirical historical quantile a known population truth against which every parametric estimate can be scored without qualification. The source's exercise is descriptive evidence of disagreement and sensitivity, not a statistical ranking of forecast accuracy.

The practical lesson is to match the estimator to the mechanism generating portfolio loss. Linear Gaussian factor models can be transparent when their assumptions are defensible. Conditional volatility models address changing scale but do not automatically handle asymmetric jumps. Tail models depend on threshold choices and extreme observations. Delta–gamma methods address local nonlinearity but can fail far from the expansion point. Simulation expands the range of scenarios that can be priced, while leaving scenario probabilities and valuation accuracy as model inputs. None of these categories resolves incentives, stale marks, or incomplete position data by itself.

For alternative investments, the strongest conclusion is therefore methodological: report which quantity was estimated, at which horizon, from which exposures and observations, and under which approximation. The paper's large numerical disagreements make those distinctions economically material. The corrected jump cumulants and explicit sign conventions in this note preserve that aim while preventing several printed simplifications from becoming implementation errors.
