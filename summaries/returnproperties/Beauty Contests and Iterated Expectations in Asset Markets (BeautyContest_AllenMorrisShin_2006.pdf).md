# Beauty Contests and Iterated Expectations in Asset Markets

Franklin Allen, Stephen Morris, and Hyun Song Shin. *The Review of Financial Studies* 19(3), 2006, 719–752. DOI: 10.1093/rfs/hhj036.

Source: [original PDF](../../Finance/BeautyContest_AllenMorrisShin_2006.pdf). All 34 pages were read, including Appendices A and B; the central equations, proof recursions, and appendix algebra were inspected visually. PDF page 1 is journal page 719. This is a theoretical paper, without an empirical dataset or calibrated investment backtest. Numerical checks below are independently derived illustrations, explicitly distinguished from results reported in the article.

## Why this matters

A rational trader who must sell before an asset pays its final dividend needs to forecast the resale price. That price depends on the next cohort's beliefs, which depend on later beliefs. Averaging across differently informed traders does not preserve the ordinary law of iterated expectations. Consequently, today's consensus forecast of the final payoff and today's price need not coincide even after averaging away supply noise.

The contribution is to make this mechanism precise in a competitive, Gaussian, constant-absolute-risk-aversion market with learning from prices. The authors show that higher-order beliefs give public information disproportionate weight, producing slow adjustment toward fundamentals. Irrational beliefs are not necessary. However, short horizons, heterogeneous information, and noisy prices are substantive assumptions. The resulting drift is a statement about a model's conditional mean price path, not a measured momentum premium or a free arbitrage.

For someone implementing the paper, the central task is to keep three objects separate: each person's conditional expectation, the average of those expectations, and the expectation conditional only on public information. Replacing all three with one representative-agent forecast removes the mechanism by construction.

## A transparent example of failure of the averaging tower property

Let the terminal fundamental be $\theta\sim N(y,1/\alpha)$, where $y$ is publicly known and $\alpha>0$ is prior precision. Each member of a continuum observes $x_i=\theta+\epsilon_i$, with independent Gaussian errors of precision $\beta>0$. Assume the population average error is zero. Initially ignore learning from prices and suppose no new information arrives.

An individual's posterior mean is

$$
E_i[\theta]=\frac{\alpha y+\beta x_i}{\alpha+\beta}.
$$

Define $r=\beta/(\alpha+\beta)$. Averaging across individuals gives

$$
\bar E[\theta]=(1-r)y+r\theta.
$$

The average forecast contains the true fundamental in this expression because individual signal noise cancels in the population. This does not mean that an individual knows $\theta$ or directly observes the average forecast.

When someone predicts that average, the common public term is already known, while the fundamental must again be estimated. Iterating and averaging therefore gives equation (1):

$$
\bar E^k[\theta]=(1-r^k)y+r^k\theta.
$$

Since $0<r<1$, higher orders move toward $y$. For example, if prior and private precisions are equal, the weights on $\theta$ at orders one, two, and three are $1/2$, $1/4$, and $1/8$. This is a direct mathematical illustration, not an empirical calibration in the paper.

Individual conditional expectations still satisfy the tower property when nested over that individual's increasing information. The failure concerns compositions of *different averaged operators*. Public information also has a valid tower property. There is no violation of probability theory.

The same calculation is a two-state Markov-chain operation with matrix

$$
B=\begin{pmatrix}1&0\\1-r&r\end{pmatrix}
$$

acting on $(y,\theta)'$. The public state is absorbing. Repeated application transfers weight away from the fundamental state. The Gaussian example gives a particularly simple direction and rate of convergence. The article explicitly warns that the one-step direction need not hold for arbitrary distributions. Its cited more general convergence result is not a license to extend every Gaussian comparative static to every information structure.

If one simply postulates $p_t=\bar E_t[p_{t+1}]$ and liquidation at date $T$, the example gives a fundamental weight $r^{T-t}$. The main model instead liquidates at $T+1$, so its comparable exponent is $T-t+1$. Confusing these conventions creates an off-by-one error at the final trading date.

## Full economic environment

There are trading dates $1,\ldots,T$ and liquidation at $T+1$, with $p_{T+1}=\theta$. The fundamental is drawn before first-period trading and then remains fixed. The plotted “change in fundamentals” is the realization away from the prior mean, not a sequence of independent fundamental innovations.

At every trading date, a unit mass of young investors enters. Each investor lives two periods: trade when young, then liquidate, consume, and exit when old. Investors have enough endowment that wealth constraints never bind. Their utility over old-age consumption is

$$
u(c)=-\exp(-c/\tau),\qquad \tau>0,
$$

where $\tau$ is risk tolerance, the reciprocal of absolute risk aversion. There are no imposed position limits, short-sale constraints, transaction costs, or borrowing fees. The numeraire setup has no explicit nonzero interest-rate discount factor in the pricing equations.

A young trader at date $t$ observes

$$
\mathcal I_{it}=\{y,p_1,\ldots,p_t,x_{it}\},\qquad
x_{it}=\theta+\epsilon_{it},\quad \epsilon_{it}\sim N(0,1/\beta).
$$

Private errors are independent across traders and dates. The current price is in the information set: equilibrium is a rational-expectations fixed point in which the market-clearing price itself carries information. Previous cohorts' private signals are not inherited. Public price history survives, while private knowledge is replaced by fresh noisy observations.

Net asset supply at date $t$ is $s_t\sim N(0,1/\gamma_t)$, with $\gamma_t>0$. Supply shocks are independent across dates and independent of fundamentals and private signal errors. Their role is to prevent prices from fully revealing $\theta$. The source acknowledges that independent net supplies are a stylized device. It sketches noise-trader cohorts that reverse their trades after one period, rather than deriving supply from an optimizing liquidity-demand model. Positive or negative Gaussian net supply is permitted.

The stochastic primitives and equilibrium price rule are common knowledge. Traders are competitive price takers. The article works with a linear Gaussian equilibrium; the proof of its qualitative results exploits that structure rather than giving a general uniqueness theorem for arbitrary nonlinear equilibria.

## Demand, clearing, and the higher-order pricing equation

A young trader values next period's resale price. With conditionally normal payoffs and exponential utility, optimal risky holdings are

$$
h_{it}=\tau\frac{E_{it}[p_{t+1}]-p_t}{v_t},\qquad
v_t=\operatorname{Var}(p_{t+1}\mid\mathcal I_{it}).
$$

The variance is the same across investors because their signal precisions coincide; signal realizations change their posterior means, not their posterior variances. Aggregating over the unit mass and equating demand to $s_t$ yields

$$
p_t=\bar E_t[p_{t+1}]-\frac{v_t}{\tau}s_t.
$$

At $T$, replace $p_{T+1}$ by $\theta$. The last term is the compensation needed to absorb the current supply shock. It is not an arbitrary pricing error. Positive supply lowers the price conditional on the belief term.

Future supply shocks have zero mean conditional on earlier information and their associated conditional variances are deterministic in the linear Gaussian equilibrium. Repeated substitution therefore gives equation (9):

$$
p_t=\bar E_t\bar E_{t+1}\cdots\bar E_T[\theta]
-\frac{v_t}{\tau}s_t.
$$

Only the current explicit supply-premium term remains after the recursion. Earlier shocks still influence current beliefs through observed price history, so this formula does not say that price depends solely on the current shock. Nor can the iterated average be collapsed to $\bar E_t[\theta]$.

## Extracting independent signals from price history

The authors write prices as a triangular linear system:

$$
p_t=\lambda_t y+\kappa_t\theta-\sum_{j=1}^{t}\phi_{tj}s_j.
$$

Let $\Phi$ be the lower triangular matrix of supply coefficients and let $\lambda,\kappa$ be the corresponding vectors. Inverting the nonsingular triangular system gives

$$
\Phi^{-1}(p-\lambda y)=(\Phi^{-1}\kappa)\theta-s.
$$

Writing $k_j=(\Phi^{-1}\kappa)_j$, the normalized price innovation is

$$
\xi_j=\theta-\frac{s_j}{k_j},\qquad \rho_j=\gamma_j k_j^2.
$$

The signals $\xi_j$ are independent conditional on $\theta$. Nonsingularity requires nonzero diagonal supply loadings; triangularity alone would not suffice. The economically relevant equilibrium construction has these nonzero loadings. The $\rho_j$ are endogenous precisions, not free data inputs.

At date $t$, define total posterior precision

$$
Q_t=\alpha+\beta+\sum_{j\le t}\rho_j.
$$

Then equation (11) is

$$
E_{it}[\theta]=\frac{\alpha y+\beta x_{it}+\sum_{j\le t}\rho_j\xi_j}{Q_t}.
$$

The cross-sectional average replaces $x_{it}$ by $\theta$. The public posterior excludes the private term and uses denominator $\alpha+\sum_{j\le t}\rho_j$. These two posteriors should never be interchanged.

## Matrix implementation of higher-order beliefs

Use the state vector $z=(y,\xi_1,\ldots,\xi_T,\theta)'$. Define $B_t$ as a $(T+2)$-dimensional row-stochastic matrix. Its first $t+1$ rows preserve the already-known coordinates $y,\xi_1,\ldots,\xi_t$. Every remaining row, including the fundamental row, is

$$
b_t=\left(\frac{\alpha}{Q_t},\frac{\rho_1}{Q_t},\ldots,
\frac{\rho_t}{Q_t},0,\ldots,0,\frac{\beta}{Q_t}\right).
$$

An unrevealed future price signal has conditional mean equal to the posterior mean of $\theta$, explaining why those rows coincide. Averaging over private signals yields $\bar E_t z=B_tz$.

The product order is important:

$$
\bar E_t\bar E_{t+1}\cdots\bar E_T z
=B_TB_{T-1}\cdots B_tz\equiv B_t^*z.
$$

The latest-date matrix is on the left. Reversing this order incorrectly allows future signal realizations to enter an earlier forecast. Let the last row of $B_t^*$ be

$$
b_t^*=(a_t^*,r_{1t}^*,\ldots,r_{tt}^*,0,\ldots,0,b_t^*{}_{\theta}).
$$

For clarity below, call its final component $u_t^*$. Then

$$
p_t=a_t^*y+\sum_{j\le t}r_{jt}^*\xi_j+u_t^*\theta-\frac{v_t}{\tau}s_t.
$$

The row sums to one. Consequently, conditional on fixed $y,\theta$ and averaging over all supply shocks,

$$
E_s[p_t]=a_t^*y+(1-a_t^*)\theta,
\qquad E_s[\bar E_t\theta]=\frac{\alpha}{Q_t}y+
\left(1-\frac{\alpha}{Q_t}\right)\theta.
$$

Lemma 4 in the printed article writes an averaged price equal to a row times the random vector $z$. To use that display literally, the right side must also be averaged: $b_t^*E_s[z]$. Keeping this expectation explicit avoids treating realized noisy price signals as their means.

## Theorems and proof mechanism

For positive finite precisions and risk tolerance, the backward recursions establish

$$
0<a_T^*<a_{T-1}^*<\cdots<a_1^*<1,
$$

and

$$
a_t^*>\alpha/Q_t\quad(t<T),\qquad a_T^*=\alpha/Q_T.
$$

Thus mean prices retain more weight on the prior mean than consensus fundamental forecasts do. If $\theta>y$, expected prices rise toward $\theta$; if $\theta<y$, they fall. Mean price and mean consensus coincide at the final *trading* date, but need not equal the fundamental until liquidation. This is Proposition 2 and the mean-path content of Proposition 1, not a claim that every realized price path is monotone.

Appendix A makes the proof implementable. At $T$, initialize the starred weights to the ordinary posterior weights. Moving from $t$ to $t-1$, the mass on the now-unobserved signal $\xi_t$, plus the mass on $\theta$, is redistributed according to the date-$t-1$ posterior:

$$
a_{t-1}^*=a_t^*+\frac{\alpha}{Q_{t-1}}(r_{tt}^*+u_t^*),
$$

$$
r_{j,t-1}^*=r_{jt}^*+\frac{\rho_j}{Q_{t-1}}(r_{tt}^*+u_t^*),\quad j<t,
$$

$$
u_{t-1}^*=\frac{\beta}{Q_{t-1}}(r_{tt}^*+u_t^*).
$$

Each step adds positive mass to the absorbing public-prior state. Backward induction also shows that the starred weights on known price signals exceed their single-step posterior counterparts before the final date. This is the nonhomogeneous Markov-chain explanation: earlier public information repeatedly receives weight because it helps forecast what others will think.

Proposition 1 is printed as an expected-*absolute*-error comparison, $E_s|p_t-\theta|>E_s|\bar E_t\theta-\theta|$ for $t<T$, which is stronger than comparing absolute mean biases. The main-text explanation emphasizes the mean coefficients. A way to complete the interpretation within the Gaussian construction is to note that price's supply-noise loadings are $r_{jt}^*/k_j$, with an additional $v_t/\tau$ on the current shock; consensus loadings are $(\rho_j/Q_t)/k_j$. On the positive-loading equilibrium branch, the starred-weight inequalities increase noise variance as well as absolute mean bias. Expected absolute value of a normal variable increases with both absolute mean and standard deviation. The two error criteria should still be reported distinctly; a mean-path argument alone is not a general proof about arbitrary loss functions.

Proposition 3 concerns $\tau\to0$, meaning extreme risk aversion. Aggressive private-information trading disappears, prices become uninformative, and all price-signal precisions approach zero. The mean price becomes

$$
E_s[p_t]\longrightarrow (1-r^{T-t+1})y+r^{T-t+1}\theta.
$$

This is the earlier no-price-learning example with the main model's liquidation convention. It is a convergence statement about the mean, not concentration of actual prices. Noisy supply can make actual price dispersion very large in this limit.

## An explicit two-trading-date reconstruction

Appendix B supplies a two-date solution, but its short-horizon algebra drops the updated public mean in an intermediate step. The following compact reconstruction retains that state and is derived directly from the demand and clearing equations above. It gives a reproducible example of the paper's mechanism without copying the ambiguous intermediate expressions.

Set $T=2$, so liquidation occurs at date 3. Write $k_2=\tau\beta$ and

$$
\rho_2=\gamma_2(\tau\beta)^2,
\qquad
k_1=\tau\beta\frac{\rho_2}{\beta+\rho_2},
\qquad \rho_1=\gamma_1k_1^2.
$$

Define $A=\alpha+\rho_1$, $Q=A+\beta+\rho_2$, $\xi_1=\theta-s_1/k_1$, and the public date-2 prior

$$
m_2=\frac{\alpha y+\rho_1\xi_1}{A}.
$$

Let

$$
C=\frac{A}{Q},\quad D=\frac{\beta+\rho_2}{Q},\quad e=\frac{D}{\tau\beta}.
$$

The last trading price is

$$
p_2=Cm_2+D\theta-e s_2.
$$

Given date-1 information, $m_2$ is known. Therefore the variance relevant to the first cohort is

$$
v_1=\frac{D^2}{A+\beta}+\frac{e^2}{\gamma_2}.
$$

Set $w=D\beta/(A+\beta)$. The first price is

$$
p_1=(1-w)m_2+w\theta-\frac{v_1}{\tau}s_1.
$$

Although $m_2$ contains information extracted from $p_1$, this is an equilibrium relation, not an exogenous forecasting equation. The price-signal consistency condition is $k_1=\tau w/v_1$. Substituting the expressions for $D,e,v_1$ simplifies exactly to the closed-form $k_1$ above. Thus the equations can be evaluated without a numerical fixed-point search.

For implementation in primitive shocks, let $L=(1-w)\alpha/A$ and $K=1-L$. Then

$$
p_1=Ly+K\theta-\frac{K}{k_1}s_1,
$$

$$
p_2=\frac{\alpha}{Q}y+
\left(1-\frac{\alpha}{Q}\right)\theta
-\frac{\rho_1}{Qk_1}s_1-e s_2.
$$

The $s_1$ term in $p_2$ is essential. Past supply noise changes the public posterior through the first price. On PDF page 28, equation (28) instead replaces the updated public mean by the original $y$ while purporting to describe the realized second price. The following first-price formulas inherit that substitution. Keeping $m_2$ until the final expansion restores price-history learning and agrees with the main text's matrix construction. This is an explicitly derived repair, not an assertion that the printed Appendix B is internally exact as written.

As an independent check, choose $\alpha=\beta=\tau=\gamma_1=\gamma_2=1$. Then $\rho_1=0.25$, $\rho_2=1$, and

$$
p_1=0.58119658y+0.41880342\theta-0.83760684s_1,
$$

$$
p_2=0.30769231y+0.69230769\theta-0.15384615s_1-0.61538462s_2.
$$

The consensus mean at date 1 places only $0.44444444$ on $y$, compared with price's $0.58119658$. At date 2 both means place $0.30769231$ on $y$. Substitution into aggregate demand gives market-clearing residuals below $10^{-15}$ in a nonzero-shock numerical check. These numbers illustrate internal consistency; they are not fitted to market data or reported as a numerical experiment by the authors.

## Long-lived traders and the limits of the analogy

The long-horizon comparison keeps the same investors through both trading dates and maximizes utility of terminal consumption. Date-1 holdings now include a hedge against the investment opportunity at date 2. Dropping this hedging demand would merely reimpose the short-horizon model.

Appendix B expresses this precisely. Let $\eta=\operatorname{Var}_{i1}(p_2)$, $\chi=\operatorname{Var}_{i2}(\theta)$, and let $\psi$ be the coefficient on $p_2$ in the date-2 posterior mean, holding date-1 information fixed. Conditional on date 1, the date-2 posterior mean is perfectly correlated with $p_2$. Demand is

$$
h_{i1}=\tau\left[
\left(\frac{1}{\eta}+\frac{(1-\psi)^2}{\chi}\right)
(E_{i1}p_2-p_1)
+\frac{1-\psi}{\chi}
\left(E_{i1}E_{i2}\theta-E_{i1}p_2\right)
\right].
$$

The second term is the intertemporal hedge. The appendix obtains its moments from the joint Gaussian price and posterior distribution. It does not supply a calibrated empirical estimate of that hedge.

In the limit of extremely noisy supplies, $(\gamma_1,\gamma_2)\to(0,0)$, Proposition 7 states that the long-lived model has

$$
E_s[p_1]=E_s[p_2]=\frac{\alpha}{\alpha+\beta}y+
\frac{\beta}{\alpha+\beta}\theta.
$$

The corresponding short-lived first price instead has fundamental weight $r^2$, while its second price has weight $r$. The extra first-period public-information bias therefore depends on horizons. The authors suggest an intermediate model in which traders face an uncertain need to consume early; this is a proposed extension, not a fully estimated hybrid model in the source.

The comparison also explains why known fundamental mispricing need not generate demand sufficient to remove it. Investors who must liquidate early face a noisy resale price and cannot simply wait for terminal convergence. Risk neutrality or infinitely precise private information are limiting cases that can make trading aggressive enough to reveal fundamentals; ordinary finite-risk-tolerance investors do not have that property.

## Reproduction and interpretation boundaries

A general-horizon implementation must jointly solve endogenous price precisions and conditional resale-price variances, then construct the belief matrices. Treating $\rho_t$ as arbitrary exogenous inputs reproduces the belief-composition calculation but not necessarily a market-clearing equilibrium. Check positivity, stochastic-matrix row sums, product ordering, posterior variance formulas, market clearing, and the terminal condition. In a finite-agent simulation, private errors do not cancel exactly; that introduces additional aggregate noise beyond the continuum model and should be labeled an approximation.

The figures are schematic. The paper supplies no calibrated parameter table, simulation seed, number of Monte Carlo paths, empirical universe, sample dates, inference procedure, or transaction-cost schedule. There is consequently no empirical performance number to reproduce. The two-date numerical example above is an algebra check designed to expose state-variable and timing errors.

The “bubble” language is qualified in the article. Prices can systematically depart from the average assessment of terminal fundamentals, but this finite-horizon model does not generate the usual narrative of a rapid speculative run-up followed by a sudden crash. Similarly, its mean drift resembles momentum, but no profitable observable-information trading strategy follows automatically. The conditional mean path is calculated holding the true, generally unobserved $\theta$ fixed.

Finally, failure of the averaged tower property is not a blanket claim that every arbitrage-pricing construction fails. The discussion distinguishes a universal martingale measure usable across different information sets from ordinary single-information-set pricing. The practical lesson is narrower and more useful: resale horizons and common information can cause prices to react less to dispersed private evidence than the average fundamental forecast does, even when every trader reasons rationally. A replication should preserve that distinction rather than replacing it with an unexplained behavioral underreaction coefficient.
