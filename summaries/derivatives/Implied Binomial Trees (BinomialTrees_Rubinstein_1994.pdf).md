# Implied Binomial Trees

Mark Rubinstein, *The Journal of Finance* 49(3), July 1994, 771–818; presidential address to the American Finance Association. Source: [BinomialTrees_Rubinstein_1994.pdf](../../Finance/BinomialTrees_Rubinstein_1994.pdf). The 49-page supplied scan includes a JSTOR cover; printed p. 771 is PDF p. 2. This note covers the complete article, both appendices, figures and numerical tables.

## Why this matters

An option smile implies that a single Black–Scholes volatility cannot price all strikes simultaneously. Rubinstein proposes a two-stage response. First select a discrete terminal risk-neutral distribution that prices the observed stock and European calls inside their bid–ask ranges while remaining close to a prior. Then turn that distribution into an entire recombining binomial tree by backward recursion. The tree supplies local volatility, conditional terminal distributions, prices of earlier-expiring or path-dependent derivatives, and hedge ratios.

The second stage is not identified by terminal option prices alone. Its uniqueness depends on an additional assumption: all paths reaching the same terminal node have equal risk-neutral probability. Along with ordered terminal nodes, recombination and the chosen interest/payout structure, that assumption selects one dynamic model from many with the same terminal distribution. This is the key distinction between information extracted from option prices and structure imposed to use that information for hedging or exotic valuation.

The paper also documents a large deterioration in the cross-strike fit of Black–Scholes for S&P 500 options after the 1987 crash. It does not establish a profitable trading anomaly or demonstrate superior realized hedging. Several proposed economic tests are left for future work. A good contemporaneous fit is partly guaranteed by construction and should not be confused with out-of-sample validation of the inferred dynamics.

## Cross-strike evidence and the minimax statistic

For two otherwise identical European calls with different strikes, let $C_i$ be market price and $B_i(\sigma)$ its Black–Scholes value at a common volatility. The minimax dollar discrepancy is

$$
e_{\$}=\min_{\sigma\ge0}\max_{i=1,2}|B_i(\sigma)-C_i|.
$$

Because each call value increases with volatility, the optimum lies between the individual implied volatilities and equalizes the opposite-signed dollar errors. It gives a lower bound on the error that any single-volatility fit must make for at least one call. The dollar measure is multiplied by $100/S$ to express it per \$100 of underlying. A negative sign is attached when the higher-strike option has the lower implied volatility. The minimax percentage statistic instead minimizes the maximum absolute error divided by the corresponding market option price; its optimizing volatility generally differs from the dollar version.

Tables I–II sample each trading day from 2 April 1986 through 31 August 1992, using S&P 500 calls with 125–215 days to expiry. Pairs are selected near target moneyness midpoints in intervals: roughly −9% versus −3%, −3% versus +3%, +3% versus +9%, and −9% versus +9%, measured by strike relative to contemporaneous index. For example the extreme pair chooses strikes near −9% and +9%, from the −12% to −6% and +6% to +12% bins. The tables report yearly medians, not means or regression coefficients. Exact observation counts, missing-day rules and sampling time for this daily statistic are not specified in these tables.

For the extreme ITM/OTM pair, signed median percentage errors are −0.7% in 1986, −1.6% in 1987, −7.0% in 1988, −7.7% in 1989, −11.2% in 1990, −13.1% in 1991 and −15.3% in 1992. The corresponding scaled dollar errors are −0.044, −0.118, −0.551, −0.599, −0.908, −0.887 and −0.858 dollars per \$100 of index. Percentage errors and scaled dollar errors need not rank years identically because option price levels and moneyness affect their normalization.

The 1986 extreme-pair dollar bound of about 4.4 cents per \$100 becomes roughly 10 cents at an index level near 225. The 1992 percentage spread is much larger: the near-money pair has median −8.8% and the out-of-money pair −14.2%. The author describes the −9% to +9% implied-volatility span as about 1.5 percentage points in 1986, roughly 18.5% to 17%, versus about 6.5 points in 1992, roughly 19% to 12.5%. Figure 1 shows a relatively flat precrash smile on 1 July 1987; Figure 2 shows a pronounced downward smile on 2 January 1990.

These statistics reject a common volatility across strikes to an economically visible degree. They do not separate risk-neutral tail probabilities from state prices' risk-premium content, and they do not show that selling expensive-looking low-strike options earns abnormal risk-adjusted returns. The author assumes the model is deficient rather than treating market inefficiency as the explanation; he explicitly says the associated trading strategy has not been tested.

## Recovering a terminal distribution: what goes wrong with naive interpolation

The article first studies a piecewise-uniform terminal density between adjacent traded strikes, with a finite upper endpoint chosen to match the highest-strike call. Let strikes be $0=K_0<K_1<\cdots<K_m<K_{m+1}$ and interval masses $P_1,\ldots,P_{m+1}$. Define $C_0=S\delta^{-n}$ as the prepaid stock price and let $r^n$ be the total gross interest return, with $\delta^n$ the gross payout adjustment. Under uniform density within each interval, call spreads imply the triangular recurrence

$$
P_i=2\left[1-\sum_{\ell<i}P_\ell-
r^n\frac{C_{i-1}-C_i}{K_i-K_{i-1}}\right],\quad i=1,\ldots,m.
$$

The residual mass is $P_{m+1}=1-\sum_{i=1}^mP_i$ and $K_{m+1}=K_m+2r^nC_m/P_{m+1}$. Appendix 1 derives these relations by integrating the call payoff over uniform intervals. No nonnegativity constraint is built into this inversion. Consequently it can generate alternating, negative masses even from arbitrage-free Black–Scholes calls.

Table III demonstrates this with $S=100$, one year, volatility 20%, total interest factor 1.1 and payout factor 1.05, using eleven positive strikes from 75 to 125 in increments of 5. Recovered interval masses include −0.0283, −0.0008, −0.0085 and −0.0338. The test is useful because the true distribution is known; the failure is caused by the imposed interpolation/tail structure, not by market noise. The paper contrasts this with Shimko's procedure of interpolating implied volatility, translating back to option prices, differentiating twice and grafting lognormal tails. Neither method makes unobserved tails uniquely observable.

## The constrained quadratic program

Choose ordered terminal prices $S_j$, $j=0,\ldots,n$, and positive prior risk-neutral masses $P'_j$. The working prior is an ordinary binomial approximation to a lognormal distribution, with volatility based on the average implied volatility of two calls nearest the mean. In the standard tree,

$$
P'_j={n\choose j}(p')^j(1-p')^{n-j}.
$$

Use more terminal states than observed option constraints. For simultaneous stock bid/ask $S^b,S^a$ and call quotes $C_i^b,C_i^a$, solve

$$
\min_{P_0,\ldots,P_n}\sum_{j=0}^n(P_j-P'_j)^2
$$

subject to

$$
P_j\ge0,\qquad \sum_jP_j=1,
$$

$$
S^b\le \frac{\delta^n}{r^n}\sum_jP_jS_j\le S^a,
$$

$$
C_i^b\le\frac1{r^n}\sum_jP_j(S_j-K_i)^+\le C_i^a,
\qquad i=1,\ldots,m.
$$

Rates here are gross returns per tree step, not continuously compounded rates. A code implementation can equivalently parameterize them as exponentials of continuously compounded rates times step length, but must apply that convention consistently. Options are not payout protected; the extra $\delta^n$ in the stock constraint accounts for payouts accruing to the stockholder.

This is a convex quadratic program with linear constraints and a strictly convex objective, so a nonempty feasible set has a unique selected minimizer. That mathematical uniqueness is conditional on the terminal grid and prior. The data alone generally leave many feasible distributions. The objective selects the least-squared change in probability masses, rather than maximizing a likelihood or estimating a sampling distribution. A nonuniform grid changes how a squared-mass penalty acts on density; the method is not invariant to arbitrary rebinning.

The program reproduces its prior when the prior model prices fall within all quote intervals. Adding more informative strikes should reduce prior sensitivity over the observed region, but finite tails remain exposed to the chosen grid and prior. A nonnegative solution prices the included claims consistently within their spreads; it does not guarantee the finite grid can represent every otherwise arbitrage-free market dataset. An infeasible solve should trigger a check of quote synchronization, parity, dividends, rates and support before an arbitrary relaxation is imposed.

Rubinstein reports using NAG optimization software and a 200-step tree for S&P 500 observations three times a day from 1986 to 1992. The solve took a few seconds per snapshot and converged whenever the dataset was free of the general arbitrages considered. The statement is an empirical implementation report, without a hardware benchmark, solver tolerance, condition-number study or precise count of failed/filtered snapshots. Butterfly inconsistencies are described as the commonest market arbitrage pattern encountered.

Binding quote constraints have Lagrange multipliers. Under the source's convention a positive multiplier marks a binding bid and a negative multiplier a binding ask. Their magnitudes describe sensitivity of the prior-distance objective to constraint movement; they are not option alphas or standard errors. Buying large-negative-multiplier options and selling large-positive-multiplier options is suggested as a future test, not reported as a completed profitable strategy.

## The assumptions that identify the tree

The baseline construction assumes two successors per node, a recombining tree, terminal prices ordered from lowest to highest, constant per-step interest return (and a specified payout adjustment), and equal probability for every path ending at the same terminal node. The last condition says that, conditional on a total number of up moves, their order is exchangeable. It is stronger than recombination of prices: different orderings can reach the same state but carry different probabilities in a general model.

Ordered terminal states also matter. Permuting terminal prices while keeping their probabilities produces the same terminal payoff distribution after relabeling, but a different interior tree and local volatility. Therefore neither the dynamic allocation of risk across time nor the exercise value of an American option follows from a single terminal density without restrictions.

Let terminal returns be $R_j=S_j/S_*$, where $S_*$ is the fitted current stock value consistent with the probability-weighted terminal expectation. Put $a=r/\delta$ for the gross capital-growth discount factor. Consistency requires

$$
a^n=\sum_jP_jR_j.
$$

When interest and payout inputs are fixed, this relation fixes the compatible fitted spot; alternatively, with normalized returns given it defines the implied per-step factor. It should not be treated as a second independent free parameter after all those inputs have already been fixed.

Each terminal node is reached by ${n\choose j}$ paths. Initialize the per-path mass $w_{n,j}=P_j/{n\choose j}$ and the terminal node value $R_{n,j}=R_j$. Recursively for $k=n-1,\ldots,0$ and $j=0,\ldots,k$,

$$
w_{k,j}=w_{k+1,j}+w_{k+1,j+1},\qquad
p_{k,j}=\frac{w_{k+1,j+1}}{w_{k,j}},
$$

$$
R_{k,j}=\frac{(1-p_{k,j})R_{k+1,j}+p_{k,j}R_{k+1,j+1}}a.
$$

The source's “one–two–three” recursion is precisely sum the path masses, divide to obtain the up probability, then discount the expected successor value. The mass $w_{k,j}$ is for one ordered prefix, not the unconditional probability of node $(k,j)$. The latter is ${k\choose j}w_{k,j}$ under the equal-path assumption. Mixing these two quantities gives an incorrect backward recursion.

Positive terminal masses keep all reachable transition probabilities strictly between zero and one. The current state is a discounted convex combination of its successors, so the riskless capital-growth factor lies between the local down and up gross moves. This proves one-step no-arbitrage within the constructed market. Zero terminal masses require care: the article suggests replacing zeros by tiny positives, but such replacement changes quote fit unless followed by a feasibility check. Alternatively unreachable zero-mass states can be handled explicitly without claiming a hedge there.

The recursion has quadratic work in the number of steps and can use rolling arrays if the full tree is unnecessary. For a 200-step tree the paper counts 40,200 move sizes, 20,100 probabilities and one interest factor, 60,301 unknowns, yet solves them by local recursion rather than a simultaneous nonlinear system. This is the algorithmic contribution once the terminal probabilities are supplied.

## Conditional probabilities, pricing and hedge calculations

There is also a direct conditional-distribution formula. After a particular prefix containing $u$ up moves and $d$ down moves, define falling factorials $(z)_q=z(z-1)\cdots(z-q+1)$ and

$$
L_j(u,d)=\frac{(j)_u(n-j)_d}{(n)_{u+d}}.
$$

Then

$$
P_j\mid(u,d)=\frac{L_j(u,d)P_j}{\sum_\ell L_\ell(u,d)P_\ell}.
$$

Impossible terminal counts have zero likelihood. This is sampling an ordered prefix without replacement from a terminal path with $j$ up moves, then applying Bayes' rule. For one up move, the likelihood is $j/n$ and the unconditional up probability is $\sum_j(j/n)P_j$. For one down move it is $(n-j)/n$. These formulas reproduce the recursive tree and directly price terminal European payoffs conditional on an interior node.

With $k=u+d$, the interior stock is $a^{-(n-k)}\sum_jP_j\mid(u,d)S_j$, and a European payoff $H(S_j)$ is valued as $r^{-(n-k)}\sum_jP_j\mid(u,d)H(S_j)$. A European option expiring at the terminal date therefore needs no whole-tree backward pricing once its terminal distribution is known. Earlier maturities do depend on the selected interior structure.

For an American claim, backward induction takes the maximum of exercise payoff and discounted expected continuation value at each node. A down-and-out barrier replaces the node value by its rebate whenever the stock is at or below the barrier. Lookbacks and Asians can be simulated forward using the node transition probabilities while retaining the running extremum or average on each simulated path. These are model-pricing recipes, not completed empirical experiments in the article. Discrete monitoring on tree dates differs from continuous monitoring, and no barrier or path-functional discretization-error study is supplied.

For constant gross payout factor $\delta$, the source's first-step hedge ratio is

$$
\Delta=\frac{C_u-C_d}{\delta(S_u-S_d)}.
$$

Compute successor hedge ratios analogously from the next two levels and approximate gamma by $[\Delta_u-\Delta_d]/[\delta(S_u-S_d)]$. The payout factor matters because a share's return includes the payout in addition to its ex-payout successor price. These are finite-tree replication/difference quantities under the inferred dynamics, not automatically sensitivities of a freshly recalibrated surface to a spot bump.

The ordinary binomial theta formula $(C_{ud}-C)/(2h)$ is generally unsuitable because the recombined middle stock after two steps need not equal current stock. The article instead uses the local-volatility PDE to approximate calendar-time theta:

$$
\Theta\simeq\frac{(\log r)C-\log(r/\delta)\,S\Delta
-\tfrac12v_{\mathrm{step}}S^2\Gamma}{h},
$$

where $v_{\mathrm{step}}$ is the local variance of log returns over one step. This is a continuation-region diffusion approximation; at exercise boundaries or for a coarse non-diffusive tree it needs qualification. Vega is not one uniquely defined scalar in a model with a whole local-volatility structure. A quote-vega calculation requires specifying which quotes change, how the distribution is refitted, and whether the tree is rebuilt.

## Numerical tree example in Appendix 2

The worked three-step example uses terminal returns $(0.7827,0.9216,1.0851,1.2776)$ with probabilities $(0.1,0.4,0.3,0.2)$. Step length is approximately 0.167 years, interest factor about 1.017, and payout factor 1.008. The implied capital-growth factor is

$$
a=\left[0.1(0.7827)+0.4(0.9216)+0.3(1.0851)+0.2(1.2776)\right]^{1/3}
\simeq1.0089.
$$

Per-path terminal probabilities from low to high are $0.1$, $0.4/3$, $0.3/3$, and $0.2$. The first up probability is 0.5333; after an up move it is 0.5625 and after a down move 0.5. At the final branching stage, the up probabilities from highest, middle and lowest nodes are about 0.6667, 0.4286 and 0.5714. First-step return nodes are approximately 1.0961 and 0.9100. Second-step return nodes are 1.2023, 0.9826 and 0.8542, with unconditional node probabilities 0.300, 0.467 and 0.233.

This provides an unusually useful small deterministic test case: a reimplementation can verify normalization, terminal recovery, node versus path masses, and discounted conditional means before fitting market quotes. The displayed rates and node values are rounded, so exact agreement beyond the printed precision is not meaningful.

Two printed slips affect such a check. On p. 808 the displayed numerator for the mixed up/down conditional probability repeats $(n-j)$; it should be $j(n-j)/[n(n-1)]$ before normalization, as follows from the general falling-factorial formula on p. 809. On p. 817 the substituted number in the $R[dd]$ calculation is 0.531, whereas the preceding probability calculation gives 0.571 and that value produces the displayed node 0.8542. These are derived corrections to the intermediate expressions; the general recursion and the example's final tree are consistent with the corrected quantities.

## January 1990 calibration and the implied volatility structure

The detailed snapshot uses June S&P 500 options on 2 January 1990, with 164 days to maturity and a quoted index of 354.75. The discussion identifies a 10:00 a.m. Chicago snapshot, while the captions of Figures 4–5 say 11:00 a.m.; Tables IV–VI and the surrounding text use 10:00 a.m. This unresolved caption discrepancy should be preserved in any data reconstruction. Thirteen puts and fifteen calls are combined into strike-level bid and ask observations; the author says bid/ask quotes are averaged at common strikes. Put information is usable through European put–call parity, with consistent rate and dividend inputs.

The trades did not occur simultaneously. A footnote says elaborate adjustments were applied to bring observed option prices to their probable snapshot-time levels, but does not give a reproducible adjustment algorithm. The stock is assigned a two-tick bid–ask interval around the dividend-adjusted index. Figure 4 lists a zero-strike/prepaid-stock quote near 349.16–349.26 and 16 option constraints. The prior volatility is about 17%, using nearby strikes 350 and 355. The posterior is more negatively skewed and kurtotic, with a small lower-tail mode. Its global risk-neutral volatility is about 20%, while local volatility at the initial node is 20.4%. The interest-rate input shown is 9.0% annually.

Table IV reports annualized local volatility across future nodes, conditional on the original tree remaining the model. For an index level near 302 after 12 days, local volatility is 77.2%; at the same index after 91 days it is 41.7%. If the index stays near 355, local volatility is 18.5% after 12 days and 14.5% after 91 days. At index 400 after 27 days it is 4.4%. The mechanism therefore encodes a much larger immediate volatility response to a rapid downside move than to the same index decline spread over time.

The source calls a decline from 355 to 302 “18 percent.” Using the initial value as denominator gives approximately 14.9%; the actual node values and table volatilities are the relevant reproducible quantities. These future volatilities are conditional model implications from a single calibration, not realized subsequent measurements or estimates with confidence bands.

Table V distinguishes global remaining-horizon volatility from one-step local volatility. At index 302 after 12 days, global volatility is 38.0%, much less than the local 77.2%. At the starting node it is 20.0%. The author also calculates at-the-money Black–Scholes implied volatility from the conditional tree: about 17% initially, rising to approximately 39% for the downside scenario, and falling to approximately 9% when the index reaches 400 after 27 days. “Local,” “global” and “Black–Scholes implied” volatility are therefore different objects even inside one calibrated model.

For clarity, local log-return mean and variance at a branch with capital moves $d,u$ are

$$
\mu_{\mathrm{step}}=(1-p)\log d+p\log u,
$$

$$
v_{\mathrm{step}}=(1-p)(\log d-\mu_{\mathrm{step}})^2
+p(\log u-\mu_{\mathrm{step}})^2.
$$

Annualized local volatility divides the variance by step length before taking a square root. Global volatility uses the full conditional terminal log-return distribution and remaining horizon. An option's implied volatility is obtained by repricing that option and inverting Black–Scholes. Equating these three would misread both Tables IV–V and the tree's economics.

## Physical probabilities require an additional economic model

Risk-neutral terminal probabilities do not determine real-world probabilities or expected returns. Rubinstein illustrates the extra assumptions with a complete-markets representative investor maximizing expected utility of terminal total wealth. Given utility $U$ and terminal total wealth proportional to $\delta^nR_j$, the first-order conditions give

$$
Q_j=\frac{P_j/U'(\delta^nR_j)}{\sum_\ell P_\ell/U'(\delta^nR_\ell)}.
$$

The common discount factor cancels on normalization. For CRRA coefficient $\gamma$, this amounts to tilting by $(\delta^nR_j)^\gamma$. With logarithmic utility, $Q_j\propto P_j\delta^nR_j$. Figure 5 reports a cumulative risk premium around 3.2–3.3% for that example; using the more curved utility $-w^{-0.65}$ produces about 5% in the discussion. Those numbers are conditional on imposed preferences and the representative-agent interpretation, not inferred solely from option prices.

Log utility also provides a myopic node-level conversion: the physical up probability is $q=p\,\delta u/r$, and the total expected gross return is $m=\delta[(1-q)d+qu]$. Table VI reports the implied annualized local mean structure under that assumption: its initial value is 13.6%, compared with the 9% riskless rate, and it varies sharply with state. The cumulative premium over the full 164-day horizon and the initial annualized local mean are not directly interchangeable. The claim that physical and risk-neutral distributions can look similar in this one example is not a general identification result.

## Extensions, validation opportunities and missing inputs

Known time-dependent interest factors can be obtained from discount-bond ratios and inserted into the backward recursion. Node-dependent rates or payouts can also be supplied, but must satisfy the discounted expectation relation that returns the root stock value. To retain a recombining Markov tree, the rate/payout input cannot depend on the order of prior moves when those paths reach the same node. The article discusses rather than estimates these extensions.

Earlier-maturity options can replace the equal-terminal-path restriction with information about interior distributions. In a two-step example, if first-step up and down probabilities are $P_u,P_d$, then $p[d]=1-P_0/P_d$ and $p[u]=P_2/P_u$, with mixed path masses $P_d-P_0$ and $P_u-P_2$. Nonnegativity imposes compatibility restrictions. Generalizing requires interior marginals across the time grid, which are not traded at every sufficiently fine date. Interpolation across maturities is identified as future work, and the article contrasts its terminal-distribution approach with contemporaneous Dupire and Derman–Kani constructions using multiple maturities.

Three suggested empirical checks remain distinct from the reported fit: trade using binding-constraint multipliers; use a long-maturity fitted tree to price contemporaneous shorter-maturity options not used in calibration; and compare the evolving conditional tree with future option surfaces along the realized index path. The paper provides no out-of-sample design, transaction-cost model, rebalancing frequency, risk-adjusted P&L or confidence intervals for those tests. Its use of bid–ask intervals constrains calibration prices; it is not a completed transaction-cost accounting for a strategy.

A reproduction also needs the underlying quote database, synchronization adjustment, dividend forecasts, interest-rate convention, exact snapshot selection, prior-tree support and spacing, handling of zero probabilities, solver settings and grid-refinement diagnostics. The article gives an implementable optimization and tree recursion but not all of those operational inputs. A terminal-price fit should therefore be audited separately from robustness of the inferred tail masses, sensitivity of local volatility to the prior, pricing of uncalibrated maturities, and actual hedging performance.

## Source map

Section I, pp. 772–778, contains the minimax evidence, Tables I–II and smile figures. Section II, pp. 779–785, compares distribution-recovery procedures and states the constrained quadratic program. Sections III–V, pp. 785–795, define the identifying assumptions, backward recursion and extensions. Section VI, pp. 795–804, develops local/global volatility and preference-dependent mean structures; Tables IV–VI span pp. 798–807. Section VII, pp. 805–810, covers valuation and Greeks; pp. 810–812 discuss related methods and open tests. Appendix 1, pp. 812–814, derives the piecewise-uniform inversion, and Appendix 2, pp. 815–817, supplies the three-step numerical tree. References conclude on p. 818.
