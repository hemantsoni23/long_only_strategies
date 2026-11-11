# Replication and Evaluation of Fund of Hedge Funds Returns

Harry M. Kat and Helder P. Palaro, Alternative Investment Research Centre Working Paper No. 0028, 3 January 2006. [Original PDF](../../Finance/HedgeFunds_KatPalaro_2006a.pdf). The source has 24 PDF pages, including references and seven figures. Its sample ends in November 2004; the date on the paper does not imply that it incorporates 2005 returns.

## Why this matters

The paper asks whether a fund of hedge funds supplies a return distribution that an investor could obtain more cheaply by trading liquid futures. This question differs from whether its mean return exceeds a linear factor benchmark. Investors can care about skewness, tail dependence, and how a fund behaves conditional on their existing portfolio. A benchmark that reproduces only volatility or market beta can therefore miss economically relevant features.

Kat and Palaro apply a distribution-replication method to 485 funds of hedge funds. Their reported average cost of reproducing a payoff associated with an initial investment of 100 is 99.36. Bootstrap intervals lie entirely below 100 for 389 funds and entirely above 100 for 55. These are striking results relative to the authors’ chosen investment opportunity set and fitted distributions. They are not direct estimates of annual alpha, and the experiment does not establish that a feasible investor could have identified and implemented each cheapest strategy in real time.

The paper’s worked example also exposes an important limitation. Its replica closely matches some robust distributional statistics and dependence measures but misses three large losses. Ordinary skewness changes from negative to positive, while excess kurtosis falls sharply. The correct interpretation is evidence about the cost of reproducing a fitted, low-dimensional description of returns, with meaningful residual uncertainty about rare events and implementation.

## Contribution and economic object

The earlier Amin–Kat approach discussed in the paper replicated a fund’s marginal return distribution. The Kat–Palaro method additionally targets its joint distribution with a representative investor’s portfolio. This is the substantive extension: two investments with the same marginal distribution can have different diversification value if their bad outcomes occur in different states of the investor’s portfolio.

Here the representative portfolio contains 50% S&P 500 exposure and 50% long-dated US Treasury bond exposure. A reserve asset supplies another state variable from which a contingent payoff can be constructed. The source uses nearby Eurodollar futures as that reserve asset. It is consequently an interest-rate-sensitive traded exposure, not a riskless cash account merely because it is called a reserve asset.

The complete-market intuition is that sufficiently rich dynamic trading can replicate a contingent payoff. It does not by itself identify the desired payoff, make markets complete in practice, or establish the cost of trading with frictions. The empirical procedure combines a statistical description of returns, an optimization over payoff functions, and a particular option-pricing model. Each layer contributes assumptions to the final performance measure.

The paper is an application of the authors’ earlier methodological work. It gives the major procedural steps but delegates important distributional parameterizations, the cheapest-payoff algorithm, and the transaction-cost pricing machinery to that work and to Boyle and Lin (1997). A reconstruction should distinguish the statistical target, which can be stated precisely, from implementation details that cannot be recovered uniquely from this PDF.

## Data, timing, and investable building blocks

The data are from TASS as of November 2004. The authors select 485 funds of hedge funds with at least four years of return history and convert non-US-dollar returns into dollars. The reported fund returns are net of all fees. The PDF does not identify individual funds, give the exchange-rate series or conversion timing, explain whether any currency hedging is assumed, or supply a fund-level inclusion file.

The minimum-history requirement is consequential: funds failing early cannot enter this sample. Moreover, the database contains no fund deaths before 1994. The authors acknowledge the associated survivorship issue. This is not a survivorship-free population of every fund that an investor could have selected at every historical date.

The history-length distribution in Table 5 is:

| Years of available history | Funds |
|---|---:|
| 4–5 | 89 |
| 5–6 | 81 |
| 6–7 | 62 |
| 7–8 | 52 |
| 8–9 | 43 |
| 9–10 | 40 |
| 10–12 | 53 |
| 12–14 | 31 |
| 14 or more | 34 |

The counts sum to 485; 367, or 75.7%, are in bins shorter than ten years. At the database endpoint, 208 funds have stopped reporting and 277 remain live. Stopping reporting is the observable classification; it need not always establish liquidation or investor loss.

The replicating instruments are nearby S&P 500 and Eurodollar futures traded at the CME and Treasury bond futures traded at the CBOT. The futures data come from Commodity Systems Inc.; one-month US-dollar LIBOR comes from Datastream. Futures positions are described as fully collateralized. The transaction-cost assumption is one basis point each way, or 0.0001 per one-way trade, for all three futures markets. It is a trading-cost input, not a one-basis-point annual management fee.

For each fund, volatility and correlation inputs are estimated over its available track record; the risk-free input is the average one-month rate over that same period. Different funds therefore face different historical calibration windows. A cross-sectional comparison of their replication costs is not a comparison under one common market environment.

Before fitting distributions, the authors apply a Geltner unsmoothing procedure to fund returns. The PDF does not give the precise estimating equation, treatment of negative serial correlation, parameter restrictions, or initialization. It also does not state a separate backfill deletion rule. Contract rolls, portfolio rebalancing, collateral returns, the futures notional convention, and the exact transaction-cost charging rule are not specified sufficiently to reproduce a trading ledger.

## The five-step procedure

The source’s procedure can be organized as follows.

1. Obtain monthly fund returns, investor-portfolio returns, and reserve-asset returns. Correct fund returns for serial dependence associated with smoothing.
2. Fit a joint distribution of the fund and investor portfolio, and a joint distribution of the investor portfolio and reserve asset. The fitting exercise considers 54 candidate joint distributions and selects by AIC.
3. Starting from an investment of 100, find the cheapest payoff function of the traded building blocks that produces the desired joint return distribution.
4. Price that payoff using the multivariate option model with transaction costs attributed to Boyle and Lin. Use the fund-specific volatility, correlation, and interest-rate estimates.
5. Compare the resulting price, called the KP measure, with 100 and assess estimation uncertainty by bootstrap.

A measure below 100 means that, within this fitted and priced benchmark, the fund’s distribution can be obtained with less initial capital. A measure above 100 means that the fund supplies the target distribution more cheaply than the replication benchmark. This direction of the comparison is essential. The measure is in units of initial capital per 100, not percentage points of annual return.

### A precise representation of the target

The following notation reconstructs the statistical objective; it is not a claim that the paper prints these optimization equations. Let $X$ denote a monthly fund return, $P$ the investor-portfolio return, and $R$ the reserve-asset return. Let $D$ be the fitted physical joint distribution of $(X,P)$ and $B$ the fitted physical joint distribution of $(P,R)$. A terminal payoff $g(P,R)$ is admissible when

$$
\mathcal L_B\left(\frac{g(P,R)}{100}-1,P\right)=D.
$$

This requires matching the fund’s joint distribution with the portfolio, not merely matching $E[X]$ and $\operatorname{Var}(X)$. It also requires the portfolio marginal in the two fitted bivariate distributions to be compatible. Independently fitting inconsistent marginals would not define this problem coherently; the source does not describe how this compatibility is imposed.

If $\mathcal C(g)$ is the cost assigned by the specified pricing and trading model, the economic objective is

$$
K=\inf_{g:\,\mathcal L_B(g/100-1,P)=D}\mathcal C(g).
$$

In a frictionless pricing model one might write a discounted risk-neutral expectation for $\mathcal C$. That shortcut is not the transaction-cost-inclusive pricing calculation used here. Neither the full cost functional nor the numerical optimization is printed in this paper, so replacing it by a simple discounted sample mean would change the method.

### A feasible conditional-quantile construction

One can make the distribution-matching step explicit without pretending to recover the cheapest-payoff algorithm. Suppose the distributions are continuous. Define

$$
U=F_{R\mid P}(R\mid P),\qquad
\widetilde X=F^{-1}_{X\mid P}(U\mid P),\qquad
g(P,R)=100(1+\widetilde X).
$$

Conditional on $P=p$, the probability-integral transform makes $U$ uniform. Applying the conditional quantile of the target return then gives $\Pr(\widetilde X\le x\mid P=p)=F_{X\mid P}(x\mid p)$. Integrating over the common portfolio marginal establishes the desired joint distribution.

This is a derived feasible construction, not a proof of minimum cost. Replacing $U$ by $1-U$ also preserves conditional uniformity but can allocate payoffs to states with different prices. Cost minimization must choose among such allocations under the pricing model. This is precisely the part for which the source refers readers to the earlier method.

For example, a Gaussian target copula with parameter $\rho$ gives

$$
\widetilde X=F_X^{-1}\!\left[\Phi\left\{\rho\Phi^{-1}(F_P(P))+\sqrt{1-\rho^2}\,\Phi^{-1}(U)\right\}\right].
$$

This equation makes clear why a copula parameter is not generally the ordinary Pearson correlation between nonnormal observed returns. It also shows that accurately modeling the marginal tails remains necessary even when the dependence transformation is known exactly.

## The worked fund example

The anonymous fund XYZ began in 1985. Table 1 gives a monthly standard deviation of 0.0370 before unsmoothing and 0.0424 afterward. These correspond to approximately 12.8% and 14.7% under square-root-of-12 scaling. First-order autocorrelation falls from 0.138 to 0.008. Skewness is −1.726 before and −1.746 after; excess kurtosis is 11.505 and 11.581. Unsmoothing therefore raises estimated volatility but does not eliminate the pronounced left-tail behavior.

For orientation, a conventional first-order smoothing model would be

$$
X_t^{\rm obs}=\theta X_{t-1}^{\rm obs}+(1-\theta)X_t^{\rm latent},
\qquad
X_t^{\rm latent}=\frac{X_t^{\rm obs}-\theta X_{t-1}^{\rm obs}}{1-\theta}.
$$

With independent latent innovations and $\theta=\rho_1$, this implies an unsmoothed standard deviation multiplier $\sqrt{(1+\rho_1)/(1-\rho_1)}$. Applying it to 0.0370 and 0.138 gives about 0.0425, close to the reported 0.0424. This is a useful consistency check, not verification that the authors use precisely this estimator and boundary treatment.

The reported selected distributions and parameters are:

| Component | Selected family and printed parameters |
|---|---|
| Fund XYZ | Student $t$: $\mu=0.0101$, $\sigma=0.0406$, degrees of freedom 4.0544 |
| Investor portfolio | Normal: $\mu=0.0101$, $\sigma=0.0282$ |
| Reserve asset | Johnson: $\xi=0.0031$, $\lambda=0.0046$, $\gamma=-0.60$, $\delta=1.599$ |
| Fund–portfolio copula | Gaussian, $\rho=0.754$ |
| Portfolio–reserve copula | Gumbel, parameter 1.3349 |

The paper refers to its methodological predecessor for parameterizations. In particular, one should not silently interpret the printed Student $\sigma$ as either its conventional scale parameter or its unconditional standard deviation; these differ. The Johnson family and its transformation likewise need the authors’ convention for exact replication.

For the Gaussian copula, the implied Kendall coefficient is $2\arcsin(0.754)/\pi\approx0.544$, close to the empirical 0.540. This supports the distinction between the latent Gaussian dependence parameter 0.754 and the observed Pearson coefficient 0.714.

The fitted payoff in Figure 1 increases in both building-block returns and is nonlinear. The source interprets it as involving long exposure to the building blocks. The surface is not a list of fixed portfolio weights: a dynamically replicated nonlinear payoff has state-dependent exposures, and neither its numerical grid nor its hedge trajectory is supplied.

The calculated KP measure is 99.53. The replica has a reported monthly mean return of 1.50%, compared with 1.02% for the fund. The initial capital difference is 0.47 per 100, while the monthly mean difference is 0.48 percentage points. They are different objects. A particular rescaling of a 99.53-cost payoff to 100 would produce a mean near 1.50%, but the source does not provide enough normalization details to treat that observation as an independently reproduced pricing calculation.

## What the replica matches, and what it misses

Table 2 compares the unsmoothed fund with the replicating strategy:

| Statistic | XYZ | Replica |
|---|---:|---:|
| Monthly mean | 0.0102 | 0.0150 |
| Monthly standard deviation | 0.0424 | 0.0388 |
| Ordinary skewness | −1.7463 | 0.1184 |
| Robust skewness | −0.1600 | −0.1269 |
| Excess kurtosis | 11.5812 | 1.2691 |
| Robust excess kurtosis | 0.4366 | 0.6889 |
| Pearson correlation with portfolio | 0.714 | 0.721 |
| Kendall dependence | 0.540 | 0.548 |

The robust measures are attributed to Hinkley and to Crow–Siddiqui, but their exact quantile conventions are not printed. They should be reproduced from the cited definitions rather than inferred from labels.

The univariate Kolmogorov–Smirnov statistic is 0.054 with approximate $p=0.862$; the bivariate statistic is 0.056 with approximate $p=0.924$. These fail to reject the corresponding distributional comparisons under the authors’ calculations. A large $p$-value is not proof of equivalence, and the source does not provide an equivalence margin or enough detail about adjustment for fitting the distributions on these same data.

More consequentially, Figure 2 and the discussion identify three large fund losses that the fitted parametric model does not reproduce. These observations help explain the huge discrepancy in ordinary skewness and kurtosis. Robust central-distribution similarity and close dependence coefficients can coexist with materially different extreme-loss exposure. Consequently, the example cannot support a claim that the strategy exactly reproduces every economically relevant tail feature of the observed fund.

The figures for the full sample show broad agreement in volatility and correlation but substantial dispersion in skewness. Their scatterplots are useful diagnostics, not numerical error bounds for every fund. No per-fund file is supplied from which to compute tail-fit tolerances or identify which replication-cost estimates depend most strongly on poor fit.

## Cross-sectional results and uncertainty

Table 3 selects normal marginals for 145 funds, Student marginals for 257, and Johnson marginals for 83. Thus 340 of 485, or 70.1%, select a nonnormal marginal. The selected copula counts are Gaussian 88, Student 49, Gumbel 36, symmetrized Joe–Clayton 40, Cook–Johnson 128, and Frank 144. The 397 non-Gaussian selections are 81.9% of the sample.

These are relative AIC selections within a candidate set. They are not separate formal rejections of a Gaussian null for every selected alternative, nor evidence that a chosen family is the true distribution. Model-selection uncertainty is especially relevant when a fund has only four or five years of monthly observations and the objective depends on tail behavior.

The mean KP measure is 99.36. Of the bootstrap confidence intervals, 389 lie entirely below 100, 41 include 100, and 55 lie entirely above 100. The respective fractions are 80.2%, 8.5%, and 11.3%. The paper does not state the confidence level, bootstrap replication count, resampling unit, block length, or whether each bootstrap draw repeats distribution selection, payoff optimization, and pricing calibration. Calling these “95% intervals” or treating their uncertainty as fully reproducible would therefore add information absent from the source.

There are 70 funds with point estimates above 100. That count is distinct from the 55 whose entire intervals are above 100. Figure 6 is concentrated near 99–100 with a left tail extending toward 94; its shape should not be confused with a distribution of annual excess returns.

The authors report no significant results from broad comparisons of groups organized by starting or ending date. They also document a pronounced descriptive relationship with subsequent reporting status: among 93 funds with KP below 99, 71 have stopped reporting; among 70 above 100, 16 have stopped. These are approximately 76.3% and 22.9%. Mean KP is 98.97 for dead funds and 99.65 for live funds. The paper does not supply enough test detail to turn this descriptive relationship into a calibrated forecast or causal survival effect.

## What a faithful replication would require

A reproducible implementation needs the dated TASS extract, identifiers, share-class and currency handling, all return histories before selection, and a precise treatment of disappearing funds. It also needs futures settlements, rolls, collateral conventions, rate observations, and the timing of the 50/50 portfolio’s rebalancing. Retaining only the final 485 return vectors would conceal important selection decisions.

The statistical stage must specify unsmoothing, all marginal and copula parameterizations, estimation constraints, AIC parameter counts, treatment of common portfolio marginals, and numerical convergence checks. The economic stage needs the admissible payoff class, the cheapest-payoff optimizer, the complete Boyle–Lin pricing equations, trading frequency, and how the one-basis-point transaction cost enters them. Without those pieces, implementing a conditional-quantile map is a useful methodological demonstration but not a replication of the reported KP measures.

The uncertainty stage should state its confidence level and resampling design and account for fitting and selection. Serial dependence and overlapping estimation inputs make an independent-month bootstrap a substantive assumption, not an innocuous default. An out-of-sample evaluation would additionally separate fitting dates from trading dates and record turnover, financing, margin, contract liquidity, and execution costs as they occur.

The benchmark targets dependence with one particular balanced portfolio over monthly horizons. It does not promise to match dependence with every asset, the full serial path of returns, liquidity restrictions, operational risk, or contingent investor access. Nor does its cost comparison place a separate price on due diligence, aggregation of minimum investments, or access to otherwise unavailable managers. The authors themselves warn that apparently attractive funds may be bearing unobserved catastrophic risk.

The paper therefore provides a useful way to ask a sharper benchmarking question: what does it cost, under explicit statistical and pricing assumptions, to manufacture the return distribution an investor values? Its empirical answer is unfavorable to most sampled funds of hedge funds. The strength of that answer remains conditional on distribution fit, in-sample calibration, the chosen investor portfolio, and a replication technology whose crucial numerical details are outside this application paper.
