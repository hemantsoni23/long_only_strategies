# The Economic Value of Volatility Timing Using “Realized” Volatility

**Jeff Fleming, Chris Kirby, and Barbara Ostdiek.** Working paper dated December 29, 2001; 48 PDF pages. This is the paper adding intraday realized covariance to the authors’ earlier volatility-timing framework, and is distinct from their 2001 *Journal of Finance* article titled *The Economic Value of Volatility Timing* without the final phrase.

**Source:** [timingvolatility_Fleming_2001.pdf](../../Finance/timingvolatility_Fleming_2001.pdf). References to numbered pages below use the printed pagination; tables and figures follow the references. All numerical performance estimates are reported from the source, not results of an independently rerun backtest.

## Why this matters

More precise volatility estimates are not automatically more valuable investment inputs. A covariance forecast can improve a statistical loss while producing worse portfolio weights, especially when matrix inversion amplifies small errors. This paper evaluates intraday information by the portfolio decisions it supports: does estimating daily covariance from five-minute returns improve the performance of a daily-rebalanced stocks–bonds–gold portfolio, and how much would a risk-averse investor pay for that improvement?

The authors’ innovation is an economic evaluation of realized covariance with explicit corrections for nontrading periods and measurement bias. They compare a smoothed estimator based on daily returns with a parallel estimator based on high-frequency returns. Expected returns are held constant, so the daily allocation changes come from covariance forecasts. A bootstrap varies the uncertain expected-return inputs, and utility-equivalent fees quantify the incremental value of the better risk input.

The headline finding is an incremental benefit commonly around 50–200 basis points per year from moving from daily-return covariance estimates to corrected realized-covariance estimates. The source also reveals why that result cannot be reduced to “sum intraday squared returns and invert”: unadjusted realized covariance performs poorly, overnight information matters, and bias corrections deliver a large part of the economic gain.

## Investment problem and return conventions

There are three risky futures contracts and a risk-free asset. For contract $i$, the daily return is the simple price change divided by its previous price. Let $R_t$ be the three-vector of these returns, $\mu=E[R_t]$ the assumed constant mean vector, and $\Sigma_t=\operatorname{Var}(R_t\mid\mathcal I_{t-1})$ the conditional covariance matrix available before the return is earned.

For a target daily expected excess return $\mu_p$, the minimum-variance risky weights solve

$$
\min_w w'\Sigma_t w
\quad\text{subject to}\quad w'\mu=\mu_p,
$$

with solution, equation (1),

$$
w_t^{MV}=\frac{\mu_p\Sigma_t^{-1}\mu}{\mu'\Sigma_t^{-1}\mu}.
$$

The companion maximum-return problem fixes target conditional standard deviation $\sigma_p$:

$$
\max_w w'\mu
\quad\text{subject to}\quad w'\Sigma_t w=\sigma_p^2.
$$

For the positive-return branch its solution is

$$
w_t^{MR}=\frac{\sigma_p\Sigma_t^{-1}\mu}{\sqrt{\mu'\Sigma_t^{-1}\mu}}.
$$

This second expression is the direct algebraic implementation of the source’s stated optimization problem. Both require a positive-definite covariance estimate and a nonzero mean vector. There is no long-only constraint, leverage cap, or explicit penalty on changing weights. The portfolio return is $R_{pt}=w_t'R_t$.

The numerical targets are 10% annual expected return for the minimum-volatility strategy and 12% annual volatility for the maximum-return strategy. Use internally consistent daily inputs: an arithmetic return target divided by 252 and a standard-deviation target divided by $\sqrt{252}$. These targets select the scale along the conditional risky-asset direction. They do not guarantee an ex post mean of exactly 10% or realized volatility of exactly 12% when the inputs are estimated.

Futures require no initial purchase of the underlying notional. The source’s risky weights describe notional exposures; a cash weight of one minus their sum is an equivalent funded-portfolio representation. Under cost of carry, investing all actual collateral wealth in the risk-free asset and applying the futures exposures approximates the corresponding funded spot portfolio. The reported futures P&L is treated as excess return for Sharpe-ratio purposes. Subtracting another risk-free return from it would double-count financing.

## Daily-return covariance estimator

Sections 2.1–2.2 adapt the rolling estimators studied by Foster–Nelson. For return innovations $e_t=R_t-\mu$, the daily-return estimator uses a common exponential decay across every variance and covariance:

$$
\widehat\Sigma_t=\sum_{k=1}^{\infty}\alpha e^{-\alpha k}e_{t-k}e_{t-k}'.
$$

Equivalently,

$$
\widehat\Sigma_t=e^{-\alpha}\widehat\Sigma_{t-1}
+\alpha e^{-\alpha}e_{t-1}e_{t-1}'.
$$

The precise coefficient is important: the innovation coefficient is $\alpha e^{-\alpha}$, **not** $1-e^{-\alpha}$. The discrete weights sum to $\alpha/(e^\alpha-1)$, which is close to but not exactly one. Replacing the formula with a conventionally normalized EWMA changes the estimator. The paper obtains the displayed weights from a continuous-record approximation and retains them in its GARCH-like recursion.

With positive initial covariance and common positive weights, the recursion preserves positive definiteness. A common decay also limits the parameter count and makes comparisons with the intraday estimator interpretable. The decay parameter is selected by a Gaussian quasi-likelihood based on $e_t=\Sigma_t^{1/2}z_t$ with $z_t$ modeled as standard normal. Up to constants, the objective is

$$
-\frac12\sum_t\left[\log|\Sigma_t|+e_t'\Sigma_t^{-1}e_t\right].
$$

Daily-return estimation gives $\alpha=0.031$ and log likelihood −6,494.5. This corresponds to an exponential weight half-life of $\log2/0.031\approx22.4$ daily observations. The authors estimate the decay using the full sample and explicitly acknowledge possible look-ahead. Although covariance updating itself is lagged, calling the complete experiment an untouched out-of-sample test would be inaccurate.

The source does not specify every initialization choice, including the initial covariance, truncation of the conceptual infinite history, treatment of the mean in all likelihood calculations, and how the initial usable sample is selected. The raw sample has 4,238 daily observations while the main strategy tables use 4,175. Those counts should be matched against implementation records rather than assigning an undocumented 63-day warm-up formula.

## Realized covariance, overnight information, and bias correction

Let $r_{t,j}$ be the vector of five-minute log returns within day $t$. The initial realized covariance is

$$
V_t^{\mathrm{day}}=\sum_j r_{t,j}r_{t,j}'.
$$

Under a continuous semimartingale without observation noise, increasingly fine synchronous returns estimate integrated covariance through quadratic variation. The empirical procedure uses finite five-minute sampling because bid–ask bounce, discreteness, irregular trading, and nonoverlapping market hours violate the idealized measurement setup. A realized covariance for the completed day is also not itself a forecast of the next day.

The smoothed realized-covariance forecast replaces the daily outer product by $V_{t-1}$:

$$
\widetilde\Sigma_t=e^{-\alpha}\widetilde\Sigma_{t-1}
+\alpha e^{-\alpha}V_{t-1}.
$$

To incorporate nontrading periods, the authors add the outer product of the vector of overnight returns to $V_t^{\mathrm{day}}$. This is noisy—one overnight observation is not high-frequency measurement of the entire overnight integrated covariance—but it preserves information that would otherwise be absent.

The daily-return forecast is then used as a reference to correct systematic bias in the smoothed realized estimates. Write $\widehat\sigma_{i,t}^2$ and $\widetilde\sigma_{i,t}^2$ for their diagonal elements. With $q=22$ lagged days, the variance adjustment is

$$
b_{i,t}=\frac{\sum_{l=1}^{q}\widehat\sigma_{i,t-l}^2}
{\sum_{l=1}^{q}\widetilde\sigma_{i,t-l}^2},
\qquad
\widetilde\sigma_{i,t}^{*2}=b_{i,t}\widetilde\sigma_{i,t}^2.
$$

This is a ratio of sums, not an average of daily ratios. The adjustment uses previously available forecasts; it must not incorporate the return being predicted.

For correlations, define $\widehat\rho_{ij,t}=\widehat\sigma_{ij,t}/(\widehat\sigma_{i,t}\widehat\sigma_{j,t})$ and the analogous uncorrected realized correlation $\widetilde\rho_{ij,t}$. The additive correction is

$$
b_{ij,t}=\frac1q\sum_{l=1}^{q}
(\widehat\rho_{ij,t-l}-\widetilde\rho_{ij,t-l}),
$$

$$
\widetilde\rho_{ij,t}^{*}=\operatorname{clip}
(\widetilde\rho_{ij,t}+b_{ij,t},-1,1),
\qquad
\widetilde\sigma_{ij,t}^{*}
=\widetilde\sigma_{i,t}^{*}\widetilde\sigma_{j,t}^{*}
\widetilde\rho_{ij,t}^{*}.
$$

Correlations can be positive, negative, or zero, motivating an additive adjustment rather than the variance ratio. The source reports little sensitivity when $q$ ranges from five to 504 days, and uses 22 in the reported tables.

There is a mathematical implementation limit: bounding each pairwise correlation in $[-1,1]$ does not guarantee a positive-semidefinite three-asset correlation matrix. The original common-weight recursion has a positivity property, but arbitrary subsequent pairwise corrections need not preserve it. The paper does not report a matrix repair rule or the frequency of any resulting violations. A reproduction should diagnose eigenvalues before inversion and label any added repair as an implementation extension.

The realized estimator’s likelihood-selected decay is $\alpha=0.064$, with log likelihood −6,428.8, using the adjusted estimates including overnight returns and bias corrections. Its half-life is approximately 10.8 daily observations. More precise daily measurements permit faster responsiveness, but the statistical estimate of decay is not necessarily the economic optimum.

## Data engineering and trading timing

The sample covers January 3, 1984 through November 30, 2000. The contracts are S&P 500 futures on the Chicago Mercantile Exchange, Treasury bond futures on the Chicago Board of Trade, and gold futures on the New York Mercantile Exchange. Daily gold closing prices come from Datastream; intraday transactions come from the Futures Industry Institute, with S&P futures before 1994 obtained directly from the CME. Days when any of the three markets is closed are excluded.

The nearby contract is used except that stocks switch to the second nearby in the nearby contract’s final week, while bonds and gold switch in the delivery month. A reproducer must carry contract identity across the roll, calculate returns from the intended contract rather than an artificial jump in a concatenated price level, and apply the paper’s roll-cost treatment separately.

The common rebalance time is 1:30 p.m. Central time: gold closes then, whereas bonds close at 2:00 and stocks at 3:15. Trading prices are the gold close and the last stock and bond transactions before 1:30. Daily holding returns span those common times. This avoids taking advantage of later stock or bond closing information for a portfolio supposedly traded at the gold close.

For intraday covariance measurement, the text instructs the researcher to construct a five-minute grid, identify transactions straddling each grid point, and linearly interpolate **log prices** before taking differences. Grid points more than 2.5 minutes outside the first or last transaction are discarded. Table 1’s caption instead describes nearest-transaction prices. The detailed Section 3.2.1 interpolation procedure is the primary specification here, while the caption discrepancy is retained as a replication qualification.

Interpolation can use a later trade to reconstruct an earlier intraday grid price. That is not a look-ahead in tomorrow’s forecast if the whole completed day is known before forecasting, but it is not an executable intraday transaction price. The trading-price series and the measurement-price series should therefore remain distinct. The source’s last-before-1:30 execution convention should govern the rebalance boundary.

Variance uses the returns available over the full common holding day. Covariance is measured from contemporaneous returns during the overlapping portions of the relevant markets’ sessions; the implied correlation is combined with the full-period variances to obtain the covariance input. Thus simply dropping every observation outside the three-way overlap would not reproduce the stated construction.

The authors replace intraday measures by daily-return measures during October 19–30, 1987. Data gaps, price limits, early market closes, and a temporarily increased stock-futures tick size made those intraday observations unreliable. The crash itself is not removed from the main strategy performance; its covariance input is changed. Separate reported robustness samples exclude either those crash days or the entire 1986–1988 period.

Table 1 gives annualized mean futures returns of 9.9%, 6.5%, and −6.6% for stocks, bonds, and gold, with volatilities 16.9%, 10.1%, and 14.3%. Stock–bond, stock–gold, and bond–gold correlations are 0.326, −0.124, and −0.168. Average five-minute return counts are 80, 77, and 72 per day. Lag-one intraday return correlations are −0.010, −0.077, and −0.053. Residual negative dependence, especially in bonds and gold, is consistent with microstructure contamination surviving five-minute sampling.

## Utility-equivalent valuation and bootstrap design

The investor evaluates daily outcomes with fixed initial notional wealth $W_0$ and the source’s quadratic criterion:

$$
\overline U(R_p)=\frac{W_0}{T}\sum_{t=1}^{T}
\left[(1+R_f+R_{pt})-
\frac{\gamma}{2(1+\gamma)}(1+R_f+R_{pt})^2\right].
$$

The empirical calculations use a 6% annual risk-free rate and relative-risk-aversion settings $\gamma=1$ and 10. This is a daily performance evaluation with wealth reset in the criterion, not an infinite-horizon dynamic power-utility solution. Quadratic utility’s risk tolerance is not globally constant over arbitrary wealth levels; the source’s parameterization anchors the reported comparison.

For strategies 1 and 2, solve for a constant daily fee $\Delta$ such that

$$
\overline U(R_{p1})=\overline U(R_{p2}-\Delta).
$$

Select the economically relevant root near zero and annualize as $252\times10{,}000\Delta$ basis points. The fee is a utility-equivalent return deduction, not an observed management charge. A higher Sharpe ratio alone does not uniquely determine the fee, since the criterion also depends on means and risk levels.

The initial “no estimation risk” experiment supplies the full-sample mean vector to each daily optimization. It is an ex post information benchmark. To examine mean uncertainty, the authors draw nonoverlapping blocks of 15 daily return vectors, with replacement, to form artificial samples of $k=1{,}000$, 2,000, 3,000, 4,000, 5,000, or 10,000 observations. Each sample provides a mean vector used with the actual sequence of conditional covariance forecasts. Portfolio weights are then applied to the **actual historical return sequence**.

The static comparator uses the same artificial sample’s mean vector and unconditional covariance matrix to form fixed optimal weights for the same target. This design varies estimated inputs while holding the evaluation history fixed. It is not chronological train/test splitting, and the bootstrap win fractions are not out-of-sample success probabilities for new market histories.

The main experiment accepts 1,000 bootstrap draws satisfying $\mu_s>\mu_b>\mu_g$, $\mu_s>0$, $\mu_b>0$, and $\sigma_s>\sigma_b$. Rejected draws are replaced. The rejected share is 45.3% at $k=1{,}000$ and 9.9% at $k=10{,}000$. This conditions the experiment on economically motivated prior ordering assumptions, biases accepted stock/bond means upward and gold means downward, and changes the covariance distribution. Table 6 removes the exclusions as a robustness test. The exact bootstrap random seed and end-block treatment are not reported.

Tables label the fraction of trials in which the timing strategy has a higher Sharpe ratio as “p-val.” Here 1.00 means that it wins in all or essentially all reported draws. It is **not** a conventional null-hypothesis p-value where a smaller number indicates stronger evidence. The performance-fee histograms in Figures 6–7 use 10,000 draws rather than the 1,000 used for the main tables.

## Main economic results

With full-sample mean inputs, Table 2 gives:

| Objective and covariance input | Mean, annual % | Volatility, annual % | Sharpe ratio |
|---|---:|---:|---:|
| Minimum volatility, daily returns | 10.5 | 11.4 | 0.92 |
| Minimum volatility, realized covariance | 11.7 | 11.3 | 1.03 |
| Maximum return, daily returns | 12.7 | 13.0 | 0.98 |
| Maximum return, realized covariance | 14.2 | 13.0 | 1.09 |

The best ex post static combination has Sharpe ratio approximately 0.81. The dynamic portfolios outperform this static frontier on the observed sample, but use ex post means and full-sample decay estimates. Their conditional covariance updates do not make all inputs ex ante.

Under the more informative $k=10{,}000$ bootstrap means, static/minimum-volatility Sharpe is 0.82, daily-estimator timing is 0.89, and realized-estimator timing is 0.98. The fee for moving from static to realized is 121.0 bp for $\gamma=1$ and 210.4 bp for $\gamma=10$. For the maximum-return objective, the corresponding Sharpes are 0.82, 0.95, and 1.05, and static-to-realized fees are 354.8 and 258.5 bp.

The incremental realized-versus-daily comparison is more directly attributable to intraday information. Table 5 reports:

| Bootstrap input size | Minimum-volatility fee, $\gamma=1$ / $\gamma=10$ | Maximum-return fee, $\gamma=1$ / $\gamma=10$ |
|---|---:|---:|
| 1,000 | 61.8 / 64.0 bp | 116.9 / 119.7 bp |
| 4,000 | 89.4 / 92.9 bp | 128.2 / 130.6 bp |
| 10,000 | 103.0 / 109.7 bp | 135.7 / 137.7 bp |

At $k=1{,}000$, the realized strategy beats its daily counterpart’s Sharpe in 99% of accepted draws for both objectives; the table rounds the win share to 100% at larger input sizes. Removing the mean-order exclusions lowers performance, especially with small samples, but preserves the main ordering. For example, with $k=1{,}000$ and no exclusions, minimum-volatility Sharpes are 0.61 static, 0.64 daily, and 0.69 realized.

The decomposition in Table 7 is particularly instructive. At $k=4{,}000$, using only the preceding day’s raw realized covariance produces minimum-volatility Sharpe 0.81 and maximum-return Sharpe 0.85, versus daily-estimator benchmarks 0.85 and 0.91. The raw realized estimator beats the daily benchmark in only 15% and 5% of draws. For maximum return it produces 18.7% realized volatility against a 12% target, illustrating poor risk calibration.

After smoothing, adding overnight returns, and applying the bias correction, the final Sharpes reach 0.93 and 1.01. For minimum volatility, overnight inclusion raises Sharpe from 0.83 to 0.87, and correction raises it further to 0.93. For maximum return, the corresponding values are 0.86, 0.90, and 1.01. Replacing only the variance entries or only the covariance entries provides smaller gains; both components contribute materially.

## Robustness, horizon, and costs

A more flexible multivariate GARCH comparison uses a BEKK-style recursion with an unrestricted intercept and diagonal lag matrices. Its statistical fit improves on the daily rolling estimator, but its economic portfolio performance is generally worse. At $k=4{,}000$, minimum-volatility Sharpe is 0.83 for GARCH versus 0.85 for daily rolling; maximum-return Sharpe is 0.85 versus 0.91. This supports evaluating the forecast inside the decision problem rather than selecting purely by likelihood.

Decay sensitivity gives the same warning. A daily-estimator decay near 0.005 can be economically preferable to the likelihood-selected 0.031. Table 11 consequently compares realized-covariance decays from 0.020 to 0.175 against daily decay 0.005. The broad region still favors realized covariance, but high risk aversion can reverse the fee advantage at aggressive decays: at 0.175, realized-versus-daily fees for $\gamma=10$ are −57.4 bp for minimum volatility and −102.4 bp for maximum return. A positive Sharpe difference does not guarantee positive utility value at every risk level and tuning choice.

Longer-horizon performance is measured by compounding daily portfolio returns into nonoverlapping weekly, biweekly, monthly, bimonthly, quarterly, semiannual, and annual returns. Trading remains daily. At the annual evaluation horizon there are only 16 observations, so the precision is much lower than for 4,175 daily observations. Table 8’s minimum-volatility Sharpe is 0.92 static versus 1.12 realized, with a 91% bootstrap win share. Maximum-return Sharpe is 0.92 versus 1.01, with a 77% win share. The annual fee for $\gamma=10$ falls to 40.1 bp for maximum return, demonstrating that horizon invariance is only approximate.

The source’s illustrative aggregation discussion uses lognormal compound wealth. A replication should compound simple strategy returns directly rather than apply a lognormal formula to simple-return moments without the appropriate log transformation and serial-covariance terms.

Transaction costs apply to establishing positions, daily rebalancing, rolling contracts, and final liquidation. Static portfolios also incur trades needed to maintain their fixed weights and roll exposures. Costs are proportional to notional traded; the paper does not optimize weights jointly with the costs.

Table 12’s cost label has an unusual unit: it is the **annualized one-way cost of trading one contract every day for a year**, expressed relative to contract notional. Thus a 10% entry corresponds to approximately $0.10/252$, or 3.97 bp per one-way notional trade—not a 10% execution charge. The authors’ example combines approximately \$6 round-trip brokerage and \$50 round-trip spread cost, giving \$28 one-way. Relative to a stock-futures notional of $551.39\times500$, this is about 1.02 bp per trade, or 2.56% in the table’s annualized cost units.

At the 10% cost setting, minimum-volatility means fall from 9.5% to 9.0% for static and from 10.4% to 9.5% for realized timing. The realized strategy’s Sharpe remains 0.84 versus 0.75; fees remain 55.7 and 147.0 bp. For maximum return, mean falls from 13.1% to 11.8% for realized timing, its Sharpe is 0.91 versus static 0.75, and fees are 250.0 and 168.8 bp. These fees compare realized timing with static investment, not the incremental realized-versus-daily gain.

For a \$100 million portfolio, the source estimates average daily trading of 16 stock, 40 bond, and 93 gold contracts, compared with market volumes around 69,000, 290,000, and 31,000. This suggests modest average participation at that scale; it does not establish capacity during stress or account for nonlinear impact at much larger size.

## What a reproduction can and cannot establish

The essential pipeline is fully specified at the conceptual level: align the three futures markets and their rolls, separate execution prices from intraday measurement prices, calculate daily and realized covariance inputs, add overnight information, smooth with the source’s precise exponential recursion, apply lagged bias corrections, generate static and dynamic portfolios from matched mean inputs, and evaluate utility-equivalent fees on common return observations.

Exact reproduction still requires historical data access and clarification of initialization, some interpolation-caption inconsistencies, mean estimation in the likelihood, exceptional-day handling beyond the described crash interval, matrix definiteness after correlation correction, and bootstrap randomization. Full-sample tuning and resampled means also prevent the published experiment from serving as a strictly chronological live-trading validation.

The substantive lesson is that intraday information has economic value when incorporated into a carefully calibrated covariance forecast. The gains arise from the complete estimator and trading design, including overnight and bias treatment. The weak raw-realized results, tuning sensitivity, and difference between likelihood and utility performance are as relevant for implementation as the positive headline fee estimates.
