# Transaction costs and crowding

Ludwig B. Chincarini, *Quantitative Finance* 18(8), 2018, pp. 1389–1410, DOI 10.1080/14697688.2017.1342856. Accepted June 9, 2017; first published online August 18, 2017. This note uses all 22 pages of the published PDF, including both optimization appendices. PDF page 1 corresponds to journal page 1389.

Source: [Crowding_Chincarini_2018.pdf](../../Finance/Crowding_Chincarini_2018.pdf).

## Why this matters

Managers with unrelated alpha forecasts can still end up in similar portfolios because they share risk models, constraints, liquidity preferences, and cost models. The paper tests the specific claim that incorporating common transaction costs necessarily increases crowding by forcing everyone into the same liquid stocks.

Its simulation produces a more qualified result. With independent random alphas, adding realistic costs generally reduces long-only holdings similarity as individual portfolio sizes rise from \$500 million to \$5 billion. At \$20 billion the relationship becomes less monotone and depends on the impact model and period. Market-neutral similarity is much smaller and often statistically unchanged. Shared factor alphas yield additional exceptions.

The second contribution is computational: fit each stock's total portfolio cost contribution by a linear-plus-quadratic function of its portfolio weight, then insert that approximation into a quadratically constrained optimization. This makes nonquadratic impact functions easier to incorporate. The experiments measure holdings similarity, not crisis losses or equilibrium price effects, and they do not prove a universally safe portfolio size.

## Defining crowding and its limitations

For nonzero portfolio weight vectors $w_i,w_j$, define cosine similarity

$$
s_{ij}=\frac{w_i^Tw_j}{\|w_i\|_2\|w_j\|_2}.
$$

With $M$ managers, the similarity matrix has unit diagonal, and average crowding is

$$
C=\frac{\sum_{i=1}^{M}\sum_{j=1}^{M}s_{ij}-M}{M^2-M}
 =\frac1{M(M-1)}\sum_{i\ne j}s_{ij}.
$$

Long-only similarities lie between zero and one; signed portfolios can have negative pairwise similarity. The measure uses holdings weights, not returns, and does not de-mean vectors as a Pearson correlation would. It is invariant to multiplying an entire portfolio by a positive constant. Consequently it cannot by itself distinguish a small collection of similar trades from the same positions at systemically dangerous dollar scale.

The article's three-stock example has weight columns $(0.4,0.4,0.2)$, $(0.8,0.1,0.1)$, and $(0.45,0.45,0.10)$. Pairwise similarities are approximately 0.7796, 0.9831, and 0.7906, giving $C\approx0.8511$ by direct averaging. The text prints 0.8454. The example's displayed weight matrix and similarities therefore do not reproduce its final number exactly.

The paper also defines $\Omega=C_p/C_\alpha$, comparing optimized-holdings crowding with alpha-vector crowding. If $C_\alpha$ is positive and well away from zero, a ratio above one can describe increased similarity. For independent random alphas, however, its expectation is approximately zero and realized values can be negative. Dividing by this small, sign-changing denominator makes $\Omega$ unstable. Large positive or negative ratios are not reliable evidence of large economic crowding.

The published tables illustrate this directly. Some long-only ratios are negative hundreds or negative tens of thousands despite positive $C_p$. The prose often discusses their magnitudes without their printed signs. Report actual $C$ and its uncertainty as the primary result. Also distinguish an average of monthly ratios from a ratio of time-averaged crowding; they need not agree.

Opposing signed portfolios can offset in this measure. They may nevertheless trade many of the same illiquid securities or face common financing shocks. The author notes that absolute similarities would measure a different type of fragility; the selected metric does not capture all liquidation risk.

## Data and alpha generation

The universe is updated monthly to the 2,000 largest US stocks by end-of-month market capitalization over 2006–2013. FactSet supplies monthly returns and fundamentals. MSCI-Barra, Axioma, and Northfield supply monthly factor-model components, from which full stock covariance matrices are reconstructed. Securities are matched across sources by CUSIP. Results anonymize these providers as risk models 1, 2, and 3, so no particular numbered column should be assigned to a vendor.

The experiment constructs 100 random-alpha portfolios per month and risk model. Each manager's stock signals are drawn independently from a zero-mean multivariate normal whose covariance is diagonal, using historical asset variances on that diagonal. Signals across stocks therefore have different scales tied to historical volatility, while their cross-correlations are set to zero. This differs from independent identically distributed unit-normal alphas. The exact historical estimation window and seeds for these random draws are not fully specified.

A second experiment uses value, momentum, and low-beta signals. Value is latest reported book value per share divided by current price; momentum is the compounded eleven-month return lagged one month; low beta is the negative slope from a 60-month regression on S&P 500 total returns. Fundamental information is reportedly lagged to avoid look-ahead, but precise release-date and database-vintage rules are absent.

For each signal cross-section, calculate quartiles and $IQR=Q_3-Q_1$. Values outside $[Q_1-3IQR,Q_3+3IQR]$ are marked as outliers. Estimate z-scores using non-outlier observations, then assign outliers the highest or lowest retained z-score. This is not simply clipping all z-scores at three standard deviations.

To express signals in return units, set

$$
\widetilde Z_{it}=Z_{it}\sigma_{r,t}+\mu_{r,t}.
$$

The text describes the scaling moments using past twelve-month returns divided by twelve, while the December 2013 illustration describes a monthly return cross-section with mean 4.22% and standard deviation 4.71%. The exact historical aggregation deserves clarification rather than assuming a square-root-of-time volatility conversion. The factor experiment allocates equal shares of its manager population to the three signal types; the number of distinct optimized portfolios within each type is not fully clarified in the table descriptions.

Point-in-time membership, delisting-return treatment, missing accounting data, the precise covariance vintages, and cross-vendor matching losses are additional missing inputs. Access to historical proprietary risk and cost parameters is required for exact replication.

## Portfolio problems and constraints

The article discusses both maximizing net expected return for a target risk and minimizing risk for a target net expected return. The table notes identify the reported portfolios as the latter construction. This distinction matters when reproducing results: do not assume every table uses the alpha-maximizing formulation illustrated first in Appendix 1.

For long-only portfolios, weights sum to one, each lies in $[0,0.10]$, and sector weights equal those of the monthly capitalization-weighted top-2,000-stock benchmark. The risk-target version uses the S&P 500's prior 60-month historical volatility; if infeasible, the nearest feasible target is used. The return-target version uses historical annualized S&P volatility divided by $\sqrt{12}$ as a monthly target alpha. This is an illustrative target-return choice, not an empirical expected-return forecast; a feasibility fallback is mentioned without a complete deterministic search algorithm.

Market-neutral portfolios have signed weights in $[-0.10,0.10]$, long exposure summing to one, short exposure summing to minus one, sector neutrality, and beta neutrality. The beta estimates use five years of returns. Gross exposure is intended to be two and net exposure zero. The alternative risk target is described as 5% volatility, but Appendix Equations A3 and A9 print variance forms $w^T\Sigma w$ equal to volatility quantities rather than squared targets. An implementation must use consistent variance units and state the chosen annualization.

Liquidity constraints were explored but omitted from reported results because larger portfolios frequently became infeasible. Appendix 1 gives a position bound $|w_i|V\le c\,ADV_i^{\$}$, combining it with the 10% name bound. The discussion mentions typical 15% participation and feasibility problems even when raising trial limits from 30% toward 70%. These limits are absent from the core tables. The published conclusions therefore do not establish that large portfolios can actually be built or unwound within realistic one-day participation limits.

## Impact models and cost approximation

Transaction cost model 1 adapts Almgren and coauthors' equity-impact specification. For a signed trade of $n_i$ shares, daily share volume $V_i$, shares outstanding $N_i$, daily volatility $\sigma_i$, and execution duration $T$ days, the printed formula is

$$
c_i=\frac{I_i}{2}+\operatorname{sgn}(n_i)\eta\sigma_i
       \left|\frac{n_i}{V_iT}\right|^{3/5},
\qquad
I_i=\gamma\sigma_i\frac{n_i}{V_i}
       \left(\frac{N_i}{V_i}\right)^{1/4}.
$$

Parameters are $\gamma=0.314$, $\eta=0.142$, and $T=1$. The coefficient is 0.314 in the actual PDF; duplicated extraction layers can corrupt it. The first term is $I_i/2$, not $2I_i$. Signed impact is converted to a positive cost through an absolute value before adding the spread.

Model 2 is the Northfield monthly specification

$$
c_i=B_i|n_i|+C_i|n_i|^{1/2},
$$

with proprietary stock-specific coefficients available from March 2009. Its output is percentage price movement. Total per-trade cost adds half the spread in percentage points and commissions:

$$
tc_i=\text{commission}_i+
 100\frac{\text{ask}_i-\text{bid}_i}{2p_i}+|c_i|.
$$

The simulations set commissions to zero. They do not use the illustrative \$0.005-per-share commission mentioned in the motivation. Price, volatility, impact, alpha, and spread must share consistent percentage or decimal units throughout.

As an illustration, a 1% position in a \$500 million portfolio means a \$5 million trade. December 2013 AT&T has price \$35.16, daily volume 18.93 million shares, and a one-cent spread. Reported cost is 0.0232% of traded value, or \$1,160. AGL Resources has price \$47.23, daily volume 490,000 shares, and a two-cent spread; reported cost is 0.1621%, or \$8,105. These are modeled impact-plus-spread examples, not realized execution measurements.

For every stock, month, and portfolio-size scenario, evaluate cost over candidate weights from zero to 10%. Multiply the per-trade percentage cost by portfolio weight to get the cost contribution to total portfolio return. Fit, without an intercept,

$$
\widetilde{tc}_i(w_i)\approx a_iw_i+b_iw_i^2,
\qquad 0\le w_i\le0.10.
$$

The exact weight-grid density and regression weighting are unspecified. Refit for each AUM scenario: the share quantity represented by a given portfolio weight changes with AUM. This approximation fits total portfolio cost contribution, not merely impact per share. The author reports adjusted $R^2$ between 0.9998 and 1 across December 2013 stocks, with about 0.9999 for both illustrated securities. High fit over this interval does not validate extrapolation or prove equally small errors at the optimizer's most consequential marginal trades.

The paper's displayed costs use final position weights. It says portfolios rebalance monthly but does not fully specify whether all costs in the simulation apply to a newly built portfolio, incremental trades from drifted prior holdings, or a liquidation-and-rebuild convention. For a conventional sequential implementation, costs should depend on $\Delta w$ after marking existing holdings to market; adding that state is a substantive reconstruction choice, not something fully described by the supplied formulas.

## Optimization implementation and appendix repairs

A dimensionally consistent long-only minimum-risk reconstruction of the stated approach is

$$
\min_w w^T\Sigma w,
\qquad
(\mu-a)^Tw-w^T\operatorname{diag}(b)w\ge\mu_T,
$$

together with the budget, sector, and name constraints. If $b_i\ge0$, the net-alpha superlevel constraint is convex. For maximum net alpha, minimize $w^T\operatorname{diag}(b)w-(\mu-a)^Tw$ subject to an upper bound on variance. Under the standard solver objective $\tfrac12w^TQw+c^Tw$, the cost quadratic requires $Q=2\operatorname{diag}(b)$.

Appendix 2's printed maximum-return matrix uses $Q=\operatorname{diag}(b)$ under that same one-half objective, omitting this factor of two. Its market-neutral risk-target substitution also contains a negative risk-bound sign and inconsistent factors. These should be checked against the intended economic objective rather than copied verbatim into a solver.

The market-neutral implementation introduces net weights $w$ and nonnegative long and short auxiliaries $u,v$, with $w=u-v$, $\sum u=\sum v=1$. Costs are represented on those nonnegative auxiliaries. This establishes net zero, but does not ensure that the actual net portfolio has gross exposure two: simultaneous positive $u_i$ and $v_i$ cancel in $w_i$. The appendix recognizes overlap and proposes a penalty proportional to $\sum u+\sum v$. With both sums fixed at one, that penalty is a constant and cannot discourage overlap. This is a genuine limitation of the printed formulation.

A reproduction should check achieved gross exposure and overlapping auxiliaries explicitly. Enforcing complementarity or using a formulation with a gross-exposure inequality changes the optimization problem and should be disclosed. The paper reports MATLAB 2014a, adjusted optimization routines, and IBM CPLEX through MATLAB, but not solver tolerances, feasibility-repair details, all auxiliary penalties, or random seeds.

## Simulation design and principal results

For each month and risk model, construct portfolios with no costs and with costs at individual AUM of \$500 million, \$5 billion, and \$20 billion. Store weights, then compute monthly similarity matrices and crowding. Model 1 covers 2006–2013. Model 2 starts March 2009. Tables split January 2006–February 2009 from March 2009–2013. These are historical-input simulations with fictitious alpha forecasts, not observations of actual fund portfolios.

For random-alpha long-only portfolios, the main absolute crowding numbers are:

| Period and impact model | Risk model | No costs | \$500m | \$5bn | \$20bn |
|---|---:|---:|---:|---:|---:|
| 2006–Feb 2009, TC1 | 1 | 0.58 | 0.49 | 0.42 | 0.50 |
| Same | 2 | 0.60 | 0.45 | 0.38 | 0.43 |
| Same | 3 | 0.59 | 0.46 | 0.38 | 0.46 |
| Mar 2009–2013, TC1 | 1 | 0.37 | 0.32 | 0.29 | 0.38 |
| Same | 2 | 0.41 | 0.27 | 0.25 | 0.32 |
| Same | 3 | 0.39 | 0.31 | 0.27 | 0.36 |
| Mar 2009–2013, TC2 | 1 | 0.37 | 0.34 | 0.30 | 0.26 |
| Same | 2 | 0.41 | 0.33 | 0.27 | 0.22 |
| Same | 3 | 0.39 | 0.33 | 0.28 | 0.24 |

The initial decline is robust in these columns. TC1 then turns upward between \$5bn and \$20bn, while TC2 continues declining. One TC1 column reaches 0.38 versus a no-cost 0.37, so even the random-alpha result does not mean costs always reduce crowding at the largest tested size.

For the early TC1 period, average long-only holding counts rise from 63/75/64 without costs to 102/138/114 at \$5bn and 157/217/176 at \$20bn across risk models 1/2/3. This supports the mechanism that nonlinear cost discourages concentrated positions. Broader holdings and lower cosine similarity can coexist. It does not prove that every additional name provides independent liquidity in a stress event.

The tables mark many long-only differences from no-cost portfolios as significant at 99% or 95%. The exact test statistic, dependence correction, and treatment of simulation-versus-time-series uncertainty are not fully reported. The many portfolio pairs share managers and are not independent observations; inference cannot safely be reproduced by treating every pair as independent.

Random-alpha market-neutral $C$ values mostly round to zero. The source reports no significant average difference from no-cost portfolios. Their volatile $\Omega$ ratios are especially hard to interpret because alpha crowding is nearly zero. Figure 5, whose vertical axis extends far beyond the feasible range of absolute cosine crowding, concerns these relative measures despite generic “average crowding” labeling.

## Shared-factor results and important exceptions

With factor alphas, reported alpha crowding is 0.09 in the early period and 0.12 later. Early long-only TC1 crowding falls from 0.52/0.42/0.55 without costs to 0.46/0.37/0.44 at \$5bn. At \$20bn it rebounds to 0.51/0.43/0.49. The risk-model-2 figure slightly exceeds its no-cost counterpart.

Later TC1 results are less supportive of a universal reduction. Risk model 1 goes from 0.40 without costs to 0.41, 0.44, and 0.52 across increasing sizes. Risk model 2 goes from 0.38 to 0.34, 0.35, and 0.42; model 3 goes from 0.46 to 0.45, 0.44, and 0.52. TC2 remains more favorable: at \$20bn these columns are 0.35, 0.30, and 0.36 versus no-cost 0.40, 0.38, and 0.46.

The prose describes the 0.40 to 0.41 to 0.44 sequence as a decline, which it is not. It also sometimes drops negative signs on market-neutral factor-crowding values. For example, early Table 3 risk-model-1 market-neutral crowding is printed −0.02 rather than +0.02, and risk-model-3 at \$20bn is −0.06 rather than +0.06. The signed nature of the statistic makes those differences substantive.

The conclusion discusses portfolios above \$20bn, but the reported size grid ends at \$20bn. Statements about a threshold beyond that point are extrapolations or mechanism arguments, not an additional documented simulation panel. Likewise this design cannot identify the actual cause of the August 2007 quant crisis. The historical crisis dates appear on simulated crowding plots, without an endogenous liquidation model or causal event identification.

## Practical takeaways

The useful result is that common costs do not mechanically imply convergence into a tiny set of liquid stocks. A properly incorporated nonlinear cost can diversify independent-alpha portfolios and reduce their average holdings similarity. The direction changes with alpha structure, impact specification, AUM, period, and constraints.

For implementation, first reproduce cost units and the per-stock quadratic fit, then validate net-alpha, sector, beta, budget, and actual gross-exposure constraints independently of the solver status. Use absolute crowding alongside liquidity-weighted concentration, signed and unsigned overlap, and aggregate dollar exposure. The paper's $\Omega$ is particularly unreliable when baseline alpha similarity is near zero.

This is evidence about a controlled portfolio-construction channel, not a measured capacity limit or proof of resilience to joint unwinds. Missing proprietary inputs, ambiguous turnover costing, unstable ratios, and appendix formulation errors limit exact reproduction. Those limits leave the main comparative experiment informative while preventing its numerical AUM levels from becoming universal risk-management rules.
