# Deep learning with long short-term memory networks for financial market predictions

Thomas Fischer and Christopher Krauss. *European Journal of Operational Research* 270 (2018), 654-669; accepted November 2017 and available online December 2017. DOI: 10.1016/j.ejor.2017.11.054. Source: [SP500PredictionDeepLearning_FisherKrauss_2017.pdf](../../Finance/SP500PredictionDeepLearning_FisherKrauss_2017.pdf). The source filename misspells Fischer as Fisher and uses the acceptance year. All 16 pages, including Appendix Figure A1 and references, were read; the network equations, tables, feature-pattern heatmap, and appendix were visually inspected. Journal page $p$ is PDF page $p-653$.

## Why this matters

The paper demonstrates that a small recurrent network can learn useful cross-sectional short-horizon patterns from raw stock-return sequences. It pools information across roughly 500 stocks, predicts whether each stock will beat the next day's cross-sectional median, and trades the extremes. The LSTM beats a feed-forward neural network and logistic regression, and slightly beats a strong random-forest benchmark over the full 1992-2015 test period.

The economically informative result is more specific than “deep learning predicts stocks.” The network largely selects volatile stocks with sharp recent price moves and trades their subsequent reversal. A simple five-day reversal rule captures about half its gross mean return. The network's incremental edge survives several execution checks over much of the sample, but after 2010 the reported net profitability fluctuates around zero. That deterioration is already in the source, not a conjecture based on later market history.

The headline 0.46% mean daily return and 5.8 Sharpe also require careful interpretation. Positions use the sum of long- and short-leg returns, consistent with 100% long and 100% short exposure. The reported annual Sharpe divides a compounded annual excess return by annualized volatility, producing 5.8261 before costs and 2.3365 after costs. Those figures are not the usual arithmetic daily Sharpe multiplied by $\sqrt{252}$. The paper is a useful controlled historical comparison, but these headline metrics should not be imported unqualified into a portfolio assessment.

## Data universe and point-in-time membership

The authors use Thomson Reuters S&P 500 constituent lists at each month end from December 1989 through September 2015. A binary membership matrix assigns that month's list to the following month. They then download daily total-return indices for all stocks ever in those lists from January 1990 through October 2015. The total-return indices incorporate dividends, splits, and corporate actions.

This reduces the classic survivorship error of testing only today's index constituents. It is an approximate monthly reconstruction, not a daily index-event database. There is a second important universe choice: for each training/trading study period, the eligible set is frozen at the final day of training. All those stocks' available prior histories enter training, even if they were not index members throughout that history. The same names are followed in the next trading year. A stock leaving the index remains tradable in the experiment while it still has price data; new entrants are not added until the next study period.

Thus the deployed universe is known at the start of the trading block, but it is not the exact changing S&P 500 each day. End-of-training membership selection also means the preceding training panel consists of firms surviving to that selection point. This is distinct from using future membership at the end of the out-of-sample year. The paper's survivor-bias protection is substantial but should be described according to the actual procedure.

A stock with no further price data is considered for trading through its last available day, usually around a delisting. The article does not provide a separate delisting-loss convention, handling of final stale quotes, or a security-level availability audit. It also does not report explicit price, volume, spread, or borrowability filters. Using a large-cap index universe mitigates some issues but does not establish that every selected short was executable, particularly around the crisis.

Table 1 gives monthly industry-portfolio descriptive statistics over January 1990-October 2015. The average cross-section has 499.7 stocks, equal-weighted mean monthly return 1.04%, and volatility 4.78%. Technology has mean 1.41% and volatility 8.50%; utilities have 0.85% and 4.54%. These are contextual statistics for monthly equal-weighted industry portfolios, not daily returns of the LSTM strategy.

## Training calendar and observations

The sample is organized into 23 study periods. Each is a rolling block of 1,000 trading days: 750 training days followed by 250 trading days. The block advances 250 days each time, so out-of-sample trading intervals do not overlap, while training histories do. Out-of-sample results span December 1992-October 2015, totaling 5,750 trading days.

Within a block, each stock supplies overlapping sequences of 240 daily returns. A sequence ending at $t$ predicts the label at $t+1$. Approximately 510 sequences per stock fall in training and 250 in testing, giving about 255,000 training and 125,000 trading observations per study period for 500 stocks. The source describes about 380,000 sequences per block in total; exact counts depend on histories and endpoint conventions.

These are pooled stock-date examples. There is one fitted classifier per model per study period, rather than one network for each stock. Adjacent sequences share 239 of 240 returns, and observations from different stocks share market conditions. Their count therefore greatly overstates the number of independent statistical observations. The source's “93 examples per parameter” heuristic is not an effective-sample-size calculation.

Parameters remain fixed through the 250-day trading interval. The model is retrained when the study window rolls, approximately annually. Features on each test day use the latest available trailing sequence, but the weights and training normalization are not refit daily. This distinction matters when comparing the design with online learning or daily adaptive systems.

## Feature and label definitions

For total-return index $P_t^s$, define an $m$-day simple return

$$
R_t^{m,s}=\frac{P_t^s}{P_{t-m}^s}-1.
$$

LSTM input is a single feature at each time step: the standardized one-day return

$$
\widetilde R_t^{1,s}
=\frac{R_t^{1,s}-\mu_{train}^{1}}{\sigma_{train}^{1}}.
$$

The training mean and standard deviation are obtained by pooling the training return feature values across the eligible stocks and training dates. The same fitted transformation applies to trading data. It is not per-stock volatility scaling, cross-sectional daily normalization, or use of full-sample moments. A sequence is $(\widetilde R_{t-239}^{1,s},\ldots,\widetilde R_t^{1,s})$.

The binary response is

$$
Y_{t+1}^s=\mathbf 1\left\{R_{t+1}^{1,s}
\geq \operatorname{median}_{j\in\mathcal U_i}R_{t+1}^{1,j}\right\},
$$

where $\mathcal U_i$ is the study-period stock set with available observations. The median is calculated from next-period realized returns when constructing training targets or evaluating predictions; it is not an input available at forecast time. A correct label therefore means relative outperformance, not a positive absolute return. A market crash can contain many class-1 stocks with negative returns.

Random forest, feed-forward DNN, and logistic regression instead receive 31 cumulative-return features with horizons

$$
m\in\{1,2,\ldots,20\}\cup\{40,60,\ldots,240\}.
$$

Logistic inputs use training-set standardization. H2O standardizes the DNN features internally; random forests do not need this scaling. The different representations span about one year, but they do not contain the same information: a 240-element daily sequence preserves intermediate path detail absent from 31 cumulative horizons. The comparison measures architecture plus representation, not a pure recurrence experiment with identical inputs.

## LSTM equations, objective, and hyperparameters

For input $x_t$, previous hidden output $h_{t-1}$, and cell state $s_{t-1}$, the source's LSTM has

$$
f_t=\sigma(W_{f,x}x_t+W_{f,h}h_{t-1}+b_f),
$$

$$
\widetilde s_t=\tanh(W_{s,x}x_t+W_{s,h}h_{t-1}+b_s),
\qquad
i_t=\sigma(W_{i,x}x_t+W_{i,h}h_{t-1}+b_i),
$$

$$
s_t=f_t\odot s_{t-1}+i_t\odot\widetilde s_t,
$$

$$
o_t=\sigma(W_{o,x}x_t+W_{o,h}h_{t-1}+b_o),
\qquad h_t=o_t\odot\tanh(s_t).
$$

Here $\sigma$ is logistic, $\odot$ elementwise multiplication, and weights/biases are shared across sequence positions. The final sequence output feeds a two-unit softmax layer. Its class-1 probability supplies the ranking score. Training minimizes binary-class cross-entropy, equivalently

$$
\mathcal L=-\sum_n\left[Y_n\log p_n+(1-Y_n)\log(1-p_n)\right].
$$

This objective weights classification probability accuracy across pooled examples; it does not directly optimize expected return, turnover, portfolio risk, or tail losses. Return magnitudes enter indirectly through features, not through a profit-weighted target.

The chosen architecture has one scalar input feature, 240 time steps, one LSTM layer with 25 hidden units, and the two-output dense layer. For $h=25$ and $i=1$, the recurrent layer has

$$
4(hi+h+h^2)=4(25+25+625)=2700
$$

parameters. The dense output adds $25\times2+2=52$, giving 2,752 total. The paper calls 2,752 parameters “for the LSTM”; more precisely it is the full network count including the output layer. This arithmetic correction leaves the stated implemented architecture unchanged.

The optimizer is RMSprop. Input and recurrent dropout are both 0.1, motivated by experiments on 1991, outside the out-of-sample trading period. Maximum training duration is 1,000 epochs; early stopping patience is ten. Eighty percent of training examples are randomly allocated to fitting and 20% to validation. After each epoch, validation cross-entropy is evaluated, and the best checkpoint is restored when stopping.

Random assignment creates extensive overlap between fitting and validation sequences, and can place same-date stocks in both groups. This makes validation less independent than a purged chronological holdout. It does not directly put future trading-year labels into training, but it can favor an overly optimistic stopping criterion. A stricter replication would retain the source split for reproduction and compare a chronological, date-grouped validation design as an explicitly new robustness experiment.

The PDF does not specify all optimizer settings, mini-batch size, initialization seeds, exact installed Keras/TensorFlow versions, or sequence-state reset implementation. It gives Python 3.5 and the relevant software families, with GPU training for LSTM and CPU cluster training for the other models. Those details are insufficient for bitwise reproducibility or for quantifying variation across random restarts. The article reports no distribution of trading performance across seeds.

## Benchmark configurations

The random forest uses 1,000 trees, maximum depth 20, and approximately $\sqrt{31}$ candidate features per split. Trees use bootstrap training samples and random feature selection. The ensemble predicts class probabilities/rankings from the committee. This is the strongest single-model benchmark in the predecessor Krauss-Do-Huck study and is not a deliberately weak baseline.

The DNN has 31 inputs, hidden layers of 31, 10, and 5 neurons, and two output units. Hidden activations are two-channel maxout, outputs softmax; dropout is 0.5 and L1 shrinkage is 0.00001. It follows the earlier study's configuration. The logistic model selects L2 regularization from 100 logarithmically spaced choices between 0.0001 and 10,000 by five-fold cross-validation on the training set, using L-BFGS with 100 maximum iterations. The source does not fully disambiguate whether its verbal “regularization” grid refers to scikit-learn's inverse-strength parameter or a direct penalty coefficient, so original code is needed for an exact reconstruction.

The benchmark models share training/trading dates and labels, but not validation protocols, feature detail, or computational budgets. The evidence supports superiority to these specified implementations. It does not demonstrate that every tuned feed-forward model or tree ensemble is dominated by recurrence.

## Ranking, position sizing, and transaction-cost convention

At each signal date, rank $p_{t+1|t}^s$ from highest to lowest. Buy the top $k$ stocks and sell short the bottom $k$, with equal weights within each leg. The study examines $k=10,50,100,150,200$ and emphasizes $k=10$. For the reported long-short scaling,

$$
r_{LS,t+1}=\frac1k\sum_{s\in L_t}R_{t+1}^{1,s}
-\frac1k\sum_{s\in S_t}R_{t+1}^{1,s}.
$$

Each side has unit notional, so gross exposure is two and net dollar exposure zero. The baseline enters and exits at closes with one-day holding periods. Signals themselves include the closing return, making same-close execution an idealized assumption. There is no risk optimizer, sector-neutrality constraint, beta-neutrality constraint, or volatility targeting. Approximate market neutrality is an ex-post finding.

Trading costs are five basis points per half-turn. A full long and short round trip produces a 20-basis-point daily deduction under the baseline convention, visible in Table 3: 0.46% gross becomes 0.26% net. Long-leg and short-leg contributions each decline by ten basis points. This is not a turnover-sensitive model of netting overlapping positions across days. Financing, stock-borrow fees, market impact, locate failures, taxes, and short-sale bans are not priced separately. The fixed fee should be viewed as a stylized friction assumption, not a capacity estimate.

## Main results and metric interpretation

Table 3 gives the following full-period results for $k=10$:

| Metric | LSTM | Random forest | DNN | Logistic |
|---|---:|---:|---:|---:|
| Gross mean daily return | 0.46% | 0.43% | 0.32% | 0.26% |
| Net mean daily return | 0.26% | 0.23% | 0.12% | 0.06% |
| Net mean $t$, Newey-West one lag | 9.5792 | 7.5217 | 3.3725 | 1.6666 |
| Daily standard deviation | 2.09% | 2.15% | 2.62% | 2.69% |
| Net fraction of positive days | 55.74% | 54.24% | 51.46% | 50.70% |
| Net maximum drawdown | 52.33% | 73.34% | 91.62% | 98.84% |
| Reported net annualized return | 82.29% | 67.87% | 24.60% | 7.11% |
| Reported net annualized Sharpe | 2.3365 | 1.8657 | 0.5159 | 0.1024 |

The LSTM's worst net day is -21.96%; its 1% net VaR is -5.45% and corresponding conditional VaR -8.21%. A very high full-sample profitability statistic does not imply modest drawdown or a low-risk trading process. The daily distribution has excess kurtosis reported as 11.6967. The forest has more extreme positive skew and kurtosis but lower 1% loss-tail metrics, so LSTM does not dominate every risk dimension.

For the LSTM, the source's gross annual excess return is 1.9360 and annual volatility 0.3323, giving $1.9360/0.3323\approx5.8261$. Net values are 0.7764 and 0.3323, yielding 2.3365. These are based on annualized compounded return quantities. For comparison only, using rounded daily raw means and volatilities gives $\sqrt{252}(0.0046/0.0209)\approx3.49$ gross and $\sqrt{252}(0.0026/0.0209)\approx1.97$ net before a consistent cash/funding adjustment. These are derived approximations, not reestimated performance, and explain why the reported 5.8 should not be interpreted as a conventional arithmetic Sharpe.

LSTM selected-name accuracy is 54.3%. Figure 3 shows its advantage generally strongest for small $k$. It has the highest reported Sharpe through $k=100$; for larger portfolios, the forest's lower volatility can outweigh the LSTM's return advantage. At $k=200$, mean returns are tied. A claim of unconditional superiority across portfolio breadth would therefore be too broad.

## Statistical tests and dependence qualifications

Table 2 reports Diebold-Mariano comparisons of 0/1 classification-error vectors for the selected long/short names: 5,750 dates times 20 names, or 115,000 forecast entries. P-values for LSTM relative to forest, DNN, and logistic are 0.0143, 0.0037, and below 0.0001. The authors apply a three-comparison Bonferroni threshold of 0.0167 and regard all three as significant. Pesaran-Timmermann directional-independence tests also return p-values below reported precision.

The test construction deserves care. Each method selects different names, so loss comparisons are conditional on each method's own selection; they are not necessarily matched forecasts for the same stock-date targets. Flattening stock-date errors into one vector also does not automatically handle cross-sectional dependence or the arbitrary ordering of contemporaneous stocks. The PDF does not establish a complete date-clustered or block-resampling treatment for this panel loss process.

The paper additionally treats 115,000 selections as independent Bernoulli trials under 50% accuracy and reports probability $2.7742\times10^{-187}$ of reaching the observed accuracy by chance. That number relies on the binomial independence idealization. Common market shocks, repeated names, and overlapping sequences make it unsuitable as a literal probability that the research finding is spurious. It also excludes model search and specification choices. The economic return series with time-series inference is more relevant to assessing the traded strategy than that extreme binomial tail.

A simulation of 100,000 random long-short strategies selects ten long and ten short stocks without replacement each day. Mean return across simulations is near zero; the best random strategy achieves about 0.05% per day gross. This shows the learned ranking beats naive random selection in the same universe. It does not benchmark the full research-selection process, establish causal inefficiency, or compare against a tuned family of reversal signals.

## Time variation and what the network selects

Figures 5 and 9 divide performance into a strong 1990s phase, a more moderate 2001-2009 period, and little or no net profitability after 2010. LSTM beats the forest in most early years. The forest does particularly well in the financial crisis, contributing much of its later cumulative profit. From January 2010 through October 2015, forest cumulative profit becomes negative while LSTM is roughly flat after costs.

The paper suggests competition and diffusion of machine-learning strategies as an explanation, but supplies no direct measure of adoption or crowding. LSTMs were introduced only in 1997 and large-scale GPU use came later; deploying the architecture in a 1992 backtest is a retrospective experiment. It does not describe a feasible research process available at the beginning of the test.

To interpret selection, the authors stack 240-day sequences for selected names, convert them to cumulative-return paths, and average across dates and stocks. Both long and short selections have below-market intermediate momentum. The long candidates suffer sharp losses in roughly the last ten days; short candidates rise sharply. Figure 8 quantifies the pattern for top/bottom portfolio sizes from one to 200.

For the top ten, average last-day return is -1.54%, last-five-day return -4.05%, and last-twenty-day return -3.83%. For the bottom ten the counterparts are +1.47%, +4.54%, and +5.62%. The all-stock means are +0.05%, +0.26%, and +1.01%. Over days $t-240$ through $t-20$, top-ten mean return is 9.06%, bottom-ten 7.78%, and cross-sectional mean 11.69%. The source's heatmap thus supports both recent reversal and weaker prior momentum.

Full-sequence daily volatility averages about 3.03% for top-ten names and 3.21% for bottom-ten names versus 2.13% for the full cross-section. Stock-level market betas estimated over those histories are about 1.1937 and 1.2169 versus 1.0465. These figures describe selected stocks before entry, not the beta of their long-short spread. Both legs can contain high-beta names while canceling much of the aggregate market exposure.

Appendix Figure A1 separates top and bottom industry weights. Technology is prominent near the dot-com episode, financials during 2008-2009, and oil/gas after 2014. Much of this occurs in both legs, consistent with selection of volatile sectors rather than a simple sector-direction bet. Equal leg dollars still do not impose sector neutrality name by name or date by date.

A transparent comparison buys the ten worst five-day performers and shorts the ten best, holding one day. It earns 0.23% gross and 0.03% net per day. This confirms reversal explains a substantial component of the opportunity. The remaining gap may reflect volatility conditioning, nonlinear interactions, path detail, or other distinctions; the paper does not identify a unique learned rule or prove that long memory itself creates the incremental return.

## Factor attribution and microstructure checks

Table 4 regresses gross daily long-short returns on market, SMB, HML, momentum, short-term reversal, and long-term reversal. LSTM alpha is 0.0042 per day with standard error 0.0003; $R^2$ is 0.0330. Its market coefficient is -0.0023 (SE 0.0255), SMB -0.0576 (0.0484), HML -0.2192 (0.0574), momentum 0.1241 (0.0345), and short-term reversal 0.3792 (0.0336). The long-term reversal coefficient 0.0549 (0.0683) is insignificant.

Forest alpha is 0.0034 with $R^2=0.1338$; DNN alpha 0.0021 with $R^2=0.1825$; logistic alpha 0.0014 with $R^2=0.1734$. These regressions show less linear exposure for LSTM to the selected benchmark factors. Low $R^2$ does not establish independence from liquidity provision, nonlinear risk, or execution conditions. Alpha is gross, and the six-factor specification is not a complete economic explanation of intraday reversal payoffs.

The key microstructure issue is bid-ask bounce: recent losers may close near bids and winners near asks, producing apparent next-day reversal when prices return toward midquotes. The authors therefore use QuantQuote minute-binned transactions from January 1998-October 2015. Each 391-minute day is divided into 23 bins of 17 minutes. Features use the 22nd bin's VWAP and execution uses the 23rd, giving an actual interval between signal and fill. Subsequent training, target generation, and backtesting use these data; the first pre-1998 training block necessarily uses Thomson Reuters history.

A weekly variant uses five-day return steps, five-day targets, and 52-step input sequences. Five staggered subportfolios avoid choosing one arbitrary weekday; each is offset one day and marked to market daily, with returns averaged across them. A further weekly version delays execution one entire day after the signal.

| 1998-2015 variant | Net mean daily return | Net mean $t$ | Net annual return | Reported net Sharpe | Net max drawdown |
|---|---:|---:|---:|---:|---:|
| Daily, closing prices | 0.20% | 5.9313 | 53.76% | 1.4233 | 52.30% |
| Daily, late-day VWAP | 0.16% | 5.1980 | 42.87% | 1.2091 | 68.22% |
| Weekly, close | 0.11% | 4.1749 | 26.04% | 0.7988 | 40.41% |
| Weekly, VWAP | 0.09% | 3.6172 | 21.03% | 0.6589 | 58.08% |
| Weekly, close with one-day wait | 0.09% | 3.4622 | 20.52% | 0.6274 | 37.94% |

These results materially strengthen the claim that closing-price bounce is not the entire historical effect. They also show the opportunity shrinking with more conservative execution and horizon assumptions. VWAP is a benchmark average, not a guarantee of fills at arbitrary participation. No impact curve or capacity analysis is supplied, and post-2010 flattening remains across the variants.

## Replication boundary and assessment

A reproduction needs historical index membership, security mapping, total-return and delisting treatment, exact train/test endpoints, optimizer defaults and seeds, state resets, all cross-validation settings, score tie handling, capital normalization, cash and borrow accounting, and exact cost netting. The source supplies enough to rebuild the research design, but not to guarantee its numerical tables or assess feasible institutional scale.

The useful advance is a pooled sequence model that autonomously extracts path-dependent short-term reversal patterns and performs well against specified contemporary baselines. The central limitations are dependence in overlapping observations, random validation, unequal feature representations, incomplete execution/capacity modeling, and a historical edge concentrated before the most recent six years of the sample. A credible continuation would start from the VWAP/delayed variants, retain date-grouped evaluation, and assess whether any incremental sequence information remains after a rich transparent reversal/volatility baseline. Those would be new experiments; the article itself ends in October 2015.

## Source map and intellectual position

Sections 2-3, pp. 655-658, define the universe, windows, features, LSTM, and baselines. Tables 2-3 and Figures 3-5, pp. 659-662, cover accuracy and performance. Figures 7-8 and Table 4, pp. 664-665, interpret selection and risk exposures. Table 5 and Figure 9, pp. 666-667, contain microstructure checks; Appendix Figure A1 is p. 668.

The closest empirical antecedent is Krauss, Do, and Huck (2017), “Deep Neural Networks, Gradient-Boosted Trees, Random Forests: Statistical Arbitrage on the S&P 500,” whose data and benchmarks anchor the comparison. Hochreiter and Schmidhuber (1997) supply the LSTM architecture; Gal and Ghahramani (2016) motivate recurrent dropout. Jegadeesh (1990), Lehmann (1990), and Lo and MacKinlay (1990) provide the reversal context. The paper's novelty is their large-scale financial application and interpretation, not invention of recurrence or discovery of short-term reversal.
