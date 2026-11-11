# Markov-switching Asset Allocation: Do Profitable Strategies Exist?

**Jan Bulla, Sascha Mergner, Ingo Bulla, André Sesboüé, and Christophe Chesneau.** Local manuscript dated January 7, 2010. Source: [MarkovSwitchingTrading_BullaMergnerSesboueChesnau_2011.pdf](../../Finance/MarkovSwitchingTrading_BullaMergnerSesboueChesnau_2011.pdf). The basename contains 2011, but the title page dates this version to 2010. All 20 pages, including references, were read. Printed pages are one less than PDF pages after the title page.

## Why this matters

Regime models often identify bull and bear markets convincingly after the fact yet fail as trading strategies because the current regime is uncertain, parameters are estimated noisily, and frequent switching incurs costs. This paper asks whether a deliberately simple daily volatility-regime rule survives a rolling out-of-sample experiment with explicit transaction costs. Its practical contribution is the combination of a two-state Gaussian hidden Markov model, Viterbi path decoding, a six-observation median filter, and an all-equity/all-cash allocation.

The objective is to reduce exposure during high-volatility periods. The rule does not optimize expected returns or estimate a continuously varying portfolio weight. Higher returns are an empirical side effect in these samples, associated with avoiding some high-volatility declines. The reported out-of-sample result is roughly 41% lower volatility across five indices and annual return improvements ranging from 18.5 to 201.6 basis points after the assumed costs. The Nikkei strategy nevertheless has a negative absolute return. “Profitable” in the paper's conclusion therefore often means outperforming buy-and-hold, not producing a positive return in every market.

## Data and investable comparison

The five index series are DAX, DJIA, NASDAQ 100, Nikkei 225, and S&P 500. Each is studied separately against a cash alternative; the experiment is not an internationally diversified five-index portfolio. The source defines the daily observation as $x_t=\log P_t-\log P_{t-1}$ using index closing prices adjusted for dividends and stock splits. It assumes a constant **3% annual cash return** for all markets and all periods.

| Index | Stated beginning | Observations | Daily mean, basis points | Daily standard deviation | Kurtosis |
|---|---|---:|---:|---:|---:|
| DAX | January 1976 | 7,796 | 3.21 | 1.25% | 10.26 |
| DJIA | January 1976 | 7,823 | 3.45 | 1.02% | 59.09 |
| NASDAQ 100 | October 1985 | 5,383 | 5.18 | 1.79% | 10.04 |
| Nikkei 225 | January 1983 | 5,925 | 1.42 | 1.31% | 7.56 |
| S&P 500 | January 1976 | 7,834 | 3.54 | 1.00% | 43.30 |

These are Table 1's printed values, with units converted explicitly. Kurtosis is the raw fourth standardized moment, not excess kurtosis. The Jarque–Bera statistics reject normality at the 1% level for every index. The authors retain crash observations, including Black Monday in 1987, rather than manually correct outliers. Gaussian **conditional** emissions do not imply a Gaussian unconditional distribution: mixing persistent states can generate heavy tails and volatility clustering, although the two-state mixture need not capture the most extreme tails adequately.

The local manuscript does not state an exact final sample date, vendor, ticker identifiers, holiday handling, or details of the dividend-adjusted series. Its abstract's broad historical description should not be substituted for missing dates. Nor is a historical local money-market series used to validate the fixed 3% cash assumption. A modern reconstruction must preserve this constant-rate experiment first, then treat varying cash yields as a separate sensitivity exercise.

## Hidden Markov model

Let $s_t\in\{1,2\}$ be an unobserved homogeneous, irreducible Markov chain. Its transition matrix is

$$
\Pi=\begin{pmatrix}p_{11}&1-p_{11}\\1-p_{22}&p_{22}\end{pmatrix},
\qquad
p_{ij}=P(s_{t+1}=j\mid s_t=i).
$$

Conditional on the state, the observation follows

$$
x_t=\mu_{s_t}+\epsilon_t,
\qquad
\epsilon_t\mid s_t\sim N(0,\sigma_{s_t}^2).
$$

The HMM construction makes observations conditionally independent given the state path. There is no autoregressive return term, GARCH recursion, time-varying transition covariate, or explicit duration distribution beyond the geometric sojourn times implied by a Markov chain. Relabel the fitted states so that $\sigma_1<\sigma_2$. State 1 then always means low volatility, regardless of the numerical labels returned by an optimizer.

For diagonal emission-density matrix $D(x_t)$ with entries $\phi(x_t;\mu_j,\sigma_j^2)$ and initial row distribution $\pi$, the likelihood is

$$
L(\theta)=\pi D(x_1)\Pi D(x_2)\cdots\Pi D(x_T)\mathbf1.
$$

Here $\theta=(\mu_1,\mu_2,\sigma_1,\sigma_2,p_{11},p_{22})$ if the initial distribution is stationary. The paper says it estimates stationary HMMs by maximum likelihood following Bulla and Berzel (2008). Under that stationary interpretation,

$$
\pi_1=\frac{1-p_{22}}{2-p_{11}-p_{22}},\qquad
\pi_2=\frac{1-p_{11}}{2-p_{11}-p_{22}}.
$$

A practical implementation should evaluate the likelihood using scaled forward recursions or log-sum-exp, constrain volatilities positive and probabilities to their admissible range, and relabel after each fit. These numerical devices implement the stated likelihood; the source does not disclose its starting values, number of restarts, convergence tolerance, variance floors, failed-fit handling, or code. Because Gaussian-mixture likelihoods can have problematic boundary solutions and local maxima, those omissions matter for exact replication.

Two states are chosen after preliminary comparisons. The authors report that a third state tends to isolate outliers, but do not provide a model-selection table, information-criterion threshold, or formal holdout comparison supporting the choice. It is part of the research design rather than an independently validated optimal number of regimes.

## State decoding and why Viterbi is used

Viterbi decoding finds the single most probable complete state path conditional on the observations:

$$
(\hat s_1,\ldots,\hat s_T)
=\arg\max_{j_1,\ldots,j_T}P(s_1=j_1,\ldots,s_T=j_T\mid x_{1:T}).
$$

In contrast, local smoothing independently chooses the most probable state at each time using $P(s_t=j\mid x_{1:T})$. The sequence of individually most probable states need not be the most probable joint path. The two methods therefore optimize different classification criteria.

For reproducibility, a log-domain Viterbi recursion can be written

$$
\delta_1(j)=\log\pi_j+\log\phi(x_1;\mu_j,\sigma_j^2),
$$

$$
\delta_t(j)=\log\phi(x_t;\mu_j,\sigma_j^2)
 +\max_i\{\delta_{t-1}(i)+\log p_{ij}\}.
$$

Store each maximizing predecessor and backtrack from the best final state. This supplies the algorithmic detail implicit in the paper's reference to Viterbi; it is not an additional fitted model. Tie-breaking and probability clipping should be documented if used.

The source's motivation experiment simulates **50,000 series of length 250** from an HMM calibrated to S&P 500 data. It compares Viterbi with local smoothing classified as low volatility when its probability exceeds 0.5. Average errors are 3.48% for Viterbi and 3.16% for smoothing. Both have much worse classification near boundaries: approximately 10% at the beginning and 6.5% at the end. Average regime switches fall from 2.92 under smoothing to 2.55 under Viterbi.

Figure 1 is important because real-time decisions always sit at a data boundary. Good interior retrospective classification is not representative of the endpoint decision available to a trader. Viterbi is selected despite a slightly higher average classification error because its path changes less often. The paper does not provide a simulation seed, exact unrounded calibration vector, or sufficient detail to establish whether every numerical estimation step was repeated in each simulated sample. The figure motivates the design; it is not itself an out-of-sample investment test.

## Rolling trading rule and its information set

For each index and each forecast date after an initial 2,000 observations, fit the HMM to the rolling window $x_{t-1999},\ldots,x_t$. Calculate its Viterbi path and retain its terminal state $\hat s_t$. Compute next-state probabilities using the row $\Pi_{\hat s_t,\cdot}$ and select the more probable next state. This last selection is the natural implementation of the paper's predicted-state description; a probability tie convention is not specified.

The forecast conditions on a **hard decoded terminal state**. It is not the usual probability-weighted HMM forecast $P(s_t=\cdot\mid x_{1:t})\Pi$. Using that filtered-probability forecast would be a legitimate alternative experiment but would change the published method. With both diagonal transition probabilities above 0.5, the most probable next state equals the decoded current state, although the transition matrix is still part of the fitted model.

Let $a_{t+1}$ denote this raw next-day state forecast, preserving the value originally produced at each earlier forecast origin. The source's six-observation median rule is

$$
b_{t+1}=\left\lfloor\operatorname{median}
(a_{t-4},a_{t-3},a_{t-2},a_{t-1},a_t,a_{t+1})\right\rfloor.
$$

Each entry comes from a different historical rolling window. Recomputing all past predictions with the newest fitted model would not reproduce the rule. The median filter is trailing, not centered, and does not use returns from the day being predicted.

Because labels are 1 and 2, the integer-part convention has a substantive tie effect. Three low and three high forecasts have median 1.5, which floors to 1. Thus cash requires at least four high-volatility forecasts among the six; a three–three tie selects equities. A generic median implementation that rounds to nearest integer, or a majority rule that retains the previous position on ties, changes the strategy. Initial handling before six raw forecasts exist is not specified; the reported forecast counts equal $N-2000$, so simply dropping five more observations would change those counts.

Set the equity weight for the next return interval to

$$
w_{t+1}=\mathbf1\{b_{t+1}=1\}.
$$

Otherwise hold cash. There is no shorting, leverage, partial allocation, volatility targeting, or optimization over expected returns. The daily refit uses information through $t$ to choose the position earning the next day's return. The source does not specify whether execution occurs at the close, next open, or another timestamp. Since $x_t$ requires the closing price, a same-close fill assumes the close can be observed and acted on without delay; a live implementation must resolve that timing and include a delay sensitivity test.

Transaction costs are **10 basis points per one-way switch**, so a complete equity-to-cash-to-equity round trip costs 20 basis points before compounding. The source suggests institutional futures execution as a rationale but does not simulate futures rolls, basis, margin, financing, market impact, or variable spreads. It also leaves the exact cash daily-rate conversion and multiplicative versus additive cost bookkeeping unspecified.

A coherent reconstruction, explicitly a convention rather than a recovered source-code detail, would take daily cash log return $c_d=\log(1.03)/A$ for $A$ trading days per year and net log return

$$
y_{t+1}=w_{t+1}x_{t+1}+(1-w_{t+1})c_d
 +|w_{t+1}-w_t|\log(1-0.001).
$$

This charges one cost for each full switch. It requires separate choices for initial entry and final liquidation. Report those choices instead of asserting they are documented by the paper.

## Fitted regimes and in-sample benchmark

Table 2 reports the following full-sample estimates. Means are daily basis points and volatilities daily percent.

| Index | $p_{11}$ | $p_{22}$ | $\mu_1$ | $\mu_2$ | $\sigma_1$ | $\sigma_2$ |
|---|---:|---:|---:|---:|---:|---:|
| DAX | 0.991 | 0.977 | 6.94 | −6.62 | 0.786 | 2.01 |
| DJIA | 0.992 | 0.950 | 4.99 | −6.66 | 0.776 | 1.98 |
| NASDAQ 100 | 0.994 | 0.985 | 10.70 | −9.22 | 1.090 | 2.90 |
| Nikkei 225 | 0.980 | 0.989 | 10.60 | −3.43 | 0.468 | 1.58 |
| S&P 500 | 0.991 | 0.968 | 5.90 | −5.31 | 0.712 | 1.67 |

Both states are persistent. For example, the S&P 500 parameters imply expected durations of roughly $1/(1-.991)=111$ trading days in state 1 and $1/(1-.968)=31$ days in state 2. The Nikkei reverses the usual persistence ordering: its high-volatility state lasts longer. The prose says variances differ by a factor of two to three, but the table shows that description applies approximately to **standard deviations**; variance ratios are their squares, and Nikkei's standard-deviation ratio itself exceeds three.

All high-volatility mean estimates are negative while low-volatility means are positive, although means do not directly determine the allocation. This association helps explain the return improvement. It does not prove that a future high-volatility regime must have negative expected return, particularly around rebounds.

Table 3's retrospective Viterbi strategy has reported annual returns/volatilities of 13.8%/10.7% for DAX, 11.2%/11.6% for DJIA, 19.8%/14.8% for NASDAQ, 11.6%/4.3% for Nikkei, and 12.4%/10.1% for S&P 500. Corresponding buy-and-hold values are 6.2%/19.8%, 7.6%/16.1%, 9.3%/28.3%, 1.4%/20.7%, and 7.9%/15.7%. These results exclude transaction costs and use future observations to decode past states. They demonstrate retrospective separation, not achievable historical trading performance.

Local smoothing produces similar risk and somewhat higher returns in some cases, but more transitions: DAX 86 versus Viterbi's 60, DJIA 74 versus 54, NASDAQ 38 versus 28, Nikkei 62 versus 46, and S&P 500 82 versus 58. Figure 2 visually shows large declines classified into the high-volatility state. The future information embedded in those state paths is why the much stronger in-sample returns cannot be used as the investment conclusion.

## Out-of-sample findings

Table 4 measures the effect of the median filter on raw rolling Viterbi forecasts:

| Index | Forecasts | Switches before filter | Switches after filter |
|---|---:|---:|---:|
| DAX | 5,796 | 188 | 84 |
| DJIA | 5,823 | 190 | 60 |
| NASDAQ 100 | 3,383 | 59 | 31 |
| Nikkei 225 | 3,925 | 207 | 89 |
| S&P 500 | 5,834 | 134 | 46 |

The reductions range from about 47% to 68%, calculated from the table. The filter changes both costs and market exposure, so its effect cannot be attributed solely to saved commissions. Longer filters delay response; shorter filters trade more. The authors choose six because it works well across the indices and decline market-specific optimization. They do not document a separate validation sample on which this hyperparameter was chosen. Rolling parameter estimation therefore establishes a temporal holdout for daily forecasts, but not necessarily a fully untouched holdout for the research design.

Table 5 reports net out-of-sample performance:

| Index | Buy-and-hold return | Strategy return | Buy-and-hold volatility | Strategy volatility | Buy-and-hold Sharpe | Strategy Sharpe |
|---|---:|---:|---:|---:|---:|---:|
| DAX | 7.24% | 7.76% | 22.0% | 13.0% | 0.292 | 0.437 |
| DJIA | 8.93% | 9.82% | 16.8% | 11.2% | 0.417 | 0.646 |
| NASDAQ | 6.82% | 8.63% | 32.0% | 14.0% | 0.272 | 0.464 |
| Nikkei | −4.30% | −2.28% | 22.6% | 13.9% | Not reported | Not reported |
| S&P 500 | 8.37% | 8.56% | 16.5% | 10.3% | 0.390 | 0.577 |

Using rounded table values, volatility reductions are approximately 40.9%, 33.3%, 56.3%, 38.5%, and 37.6%, averaging 41.3%. The largest return improvement is Nikkei, approximately 202 basis points; the smallest is S&P 500, approximately 19. The text supplies more precise figures of 201.6 and 18.5 basis points. Do not infer further precision from the rounded table.

There is a reporting ambiguity in the performance statistics. The displayed Sharpe ratios do not equal `(displayed annual mean − 3%)/displayed volatility`: for DAX that expression is about 0.193 rather than 0.292. Similarly, Table 1's daily DAX mean multiplied by 250 is 8.025%, whereas Table 3 lists 6.2%. Different arithmetic versus compound return conventions could explain much of the pattern, but the local manuscript does not define the annualization formulas sufficiently to establish that explanation. Preserve the reported values and identify the ambiguity; do not silently relabel the mean column as a confirmed CAGR. An exact replication must reconcile return transformations and Sharpe calculation from the original series or code.

## Strength of evidence and practical limits

The principal comparison is against an equity buy-and-hold strategy. There is no volatility-matched static equity/cash benchmark, simple moving-average timing rule, historical-volatility threshold, or continuously scaled volatility-targeting rule. Holding cash mechanically lowers risk, so the reported reduction alone does not establish that the HMM is the best way to obtain that risk level. The positive return differences make the experiment more interesting, but their statistical uncertainty is not quantified.

The paper supplies no confidence intervals for return differences, formal Sharpe-difference tests, bootstrap across dependent returns, parameter uncertainty analysis, or multiple-design adjustment. Its use of “significant” should not be read as a documented hypothesis-test result for strategy outperformance. The only explicit distributional test reported is Jarque–Bera on the index returns.

Material reconstruction gaps are the exact sample end dates and data identifiers; the HMM optimizer and boundary controls; the choice and validation of the six-day filter; warm-up and initial position handling; execution timestamps; cash and cost compounding conventions; and performance annualization. These do not prevent implementing the stated algorithm, but they do prevent claiming an exact numerical reproduction from this PDF alone.

The mechanism to test is clear: persistent volatility states may offer enough next-day information to avoid some costly downside exposure, provided a turnover filter prevents endpoint classification noise from causing excessive switches. Its likely failure modes are abrupt crashes before the model reacts, fast recoveries while the strategy remains in cash, changing regime distributions, unstable rolling fits, and cash returns or transaction costs different from those assumed. A useful independent replication would preserve the published rule and then vary those features one at a time, keeping the original results distinct from the new sensitivity evidence.
