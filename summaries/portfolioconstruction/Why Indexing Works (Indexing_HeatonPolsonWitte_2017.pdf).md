# Why Indexing Works

J. B. Heaton, N. G. Polson, and J. H. Witte. First draft October 2015; source draft February 2017. SSRN 2673262. Source: [original PDF](../../Finance/Indexing_HeatonPolsonWitte_2017.pdf), six PDF pages. This short theoretical and simulation paper contains approximately 1,957 source words; the note follows its substantive scope rather than adding a long literature survey. Page references use the PDF.

## Why this matters

A randomly selected stock can have the same expected return as a diversified index yet have a greater than 50% probability of underperforming it. The reason is the right-skewed distribution of terminal wealth: a small number of very large winners pull the average above the outcome of the typical stock. A broad index captures those winners automatically, whereas a concentrated selection often omits them.

The paper uses an elementary example and a heterogeneous-drift geometric Brownian model to explain this mechanism. It offers a distributional argument for indexing that does not require concentrated managers to have systematically negative expected alpha before costs. It also does not prove that every active strategy underperforms, that stock selection skill is impossible, or that diversification dominates every probability-of-success objective.

The main quantities are terminal wealth, its mean and median, and probabilities relative to specified thresholds. Confusing these quantities would turn a valid skewness argument into an incorrect claim about expected returns.

## The five-stock example

Consider five equally funded stocks. Four return 10% and one returns 50%. Buying all five produces an 18% return. Now enumerate the five possible one-stock portfolios and ten equally weighted two-stock portfolios. Across these 15 selections, ten have return 10%, four have return 30%, and one has return 50%.

The mean return across the selections is still 18%, but the median is 10% and ten of the fifteen portfolios underperform the index. Hence a two-thirds underperformance probability coexists with zero average underperformance. The rare outcomes containing the winner compensate for the more numerous portfolios without it.

This enumeration weights each of the 15 portfolios equally, so one-stock selections receive total probability one-third and two-stock selections two-thirds. It is not an equal-weighted average over the two portfolio-size classes. Each size class nevertheless has the same expected return as the index when its subsets are sampled uniformly. The basic conclusion does not depend on that incidental weighting convention.

The example also distinguishes between a diversified realized benchmark and a mean across hypothetical selections. Here the full universe is fixed, so the realized benchmark is exactly 18%. In the stochastic model below the authors approximate a large-universe benchmark by its expectation; that additional approximation needs a cross-sectional independence condition.

## The stochastic model and notation

There are $N$ stocks with initial values $S_{i0}=1$. Each stock has a drift drawn once at the start of the holding horizon and retained throughout it:

$$
\mu_i\sim N(\widehat\mu,\widehat\sigma^2).
$$

Conditional on its drift, a stock follows geometric Brownian motion with common volatility parameter $\sigma>0$:

$$
\frac{dS_{it}}{S_{it}}=\mu_i\,dt+\sigma\,dW_{it},\qquad 0\leq t\leq T.
$$

The drift draw and the Brownian shock are independent. The original equation suppresses the stock subscript on $W$. For the paper's large-cross-section diversification argument, the intended interpretation must additionally permit idiosyncratic shocks and sufficiently weak cross-stock dependence. If exactly the same Brownian motion drives all stocks, averaging does not remove that common shock. This is a source specification gap, not a minor implementation detail.

Integrating the equation gives

$$
\log S_{iT}=\mu_iT-\frac12\sigma^2T+\sigma W_{iT}.
$$

Unconditionally over both drift heterogeneity and the terminal shock, define

$$
m=\widehat\mu T-\frac12\sigma^2T,\qquad
v=\sigma^2T+\widehat\sigma^2T^2.
$$

Then $\log S_{iT}\sim N(m,v)$, so

$$
E[S_{iT}]=e^{m+v/2}=e^{\widehat\mu T+\widehat\sigma^2T^2/2},
\qquad \operatorname{median}(S_{iT})=e^m.
$$

The $T^2$ term arises because each stock's drift is persistent through the entire horizon. Redrawing the drift independently each period would define a different model and would not reproduce this term.

The difference between mean and median grows with both ordinary volatility and uncertainty about the persistent drift. Their ratio is

$$
\frac{E[S_{iT}]}{\operatorname{median}(S_{iT})}
=e^{(\sigma^2T+\widehat\sigma^2T^2)/2}.
$$

This ratio compares the mean with the median. It is not a factor by which every underperforming stock falls behind the index; the lower half of the distribution contains many different terminal values.

## What index is being modeled?

The benchmark is

$$
I_T^N=\frac1N\sum_{i=1}^N S_{iT}.
$$

Because all initial stock values equal one, this corresponds to initially equal capital in each stock, held without rebalancing. Its weights subsequently drift with prices. It can be interpreted as a capitalization-weighted index in this stylized equal-initial-capitalization economy, but it is not a continuously rebalanced equal-weight strategy and does not represent an arbitrary real-world initial capitalization distribution.

Under independent or suitably weakly dependent stocks with finite moments,

$$
I_T^N\longrightarrow E[S_{iT}]
$$

as the universe expands. The relevant convergence is a law-of-large-numbers result; the central limit theorem describes the remaining fluctuation around the mean. A single stock then underperforms the limiting benchmark with probability

$$
P(S_{iT}<E[S_{iT}])=\Phi\left(\frac{\sqrt v}{2}\right)>\frac12.
$$

This probability formula is derived here directly from the model. It clarifies the source's qualitative claim and provides a check on a simulation implementation.

If the source's unsubscripted Brownian motion were interpreted literally as common across all stocks, the conditional cross-sectional limit would instead retain the factor $e^{\sigma W_T-\sigma^2T/2}$. The unconditional expected index remains the expression above, but a realized index does not converge to that constant. Comparing selected stocks with their contemporaneous index then differs from comparing them with the unconditional mean. Correlated stocks and unequal capitalization weights require similarly explicit treatment.

## Calibration and an internal wording issue

The numerical illustration uses a five-year horizon, annual volatility $\sigma=20\%$, a terminal median gain of 10%, and a mean gain of 50%. The model-consistent conditions are

$$
e^m=1.10,\qquad e^{m+v/2}=1.50.
$$

These give

$$
\widehat\mu=\frac{\log(1.10)+\sigma^2T/2}{T}\approx0.03906,
\qquad
\widehat\sigma=\frac{\sqrt{2\log(1.50)-2\widehat\mu T}}{T}\approx0.1297.
$$

The paper rounds these to approximately 4% and 13%. Using the rounded 4% inside the second equation yields a slightly different number, approximately 12.82%. Either round-off convention is close for illustration, but a reproducible implementation should state whether it targets the two terminal moments exactly or adopts the rounded annual parameters.

The source describes the 10% median as an index median in its calibration prose. Under its own large-$N$ approximation, the index is near the 50% mean terminal return. The 10% target is mathematically the median individual-stock terminal return. This note uses that interpretation rather than imposing mutually inconsistent index targets.

For the exact terminal-moment calibration, $v=2\log(1.5/1.1)\approx0.62031$. The derived single-stock probability of finishing below the 50% benchmark gain is about 65.3%. The probability of gaining less than 30% is about 58.4%, while the probability of gaining more than 70% is about 29.0%. These are calculations from the stated model, not separately reported empirical estimates.

## Reconstructing the Monte Carlo experiment

The source describes a universe of 500 stocks and 10,000 Monte Carlo samples, evaluating portfolios of different sizes; Figure 1 displays sizes from one through twenty. A transparent implementation of its intended independent-stock experiment is:

1. Fix $T,\sigma,\widehat\mu,\widehat\sigma$ using the chosen exact or rounded calibration.
2. Generate 500 independent drift draws and independent terminal Brownian shocks for a replication, or draw the equivalent independent lognormal terminal values directly using $m,v$.
3. For portfolio size $k$, select $k$ distinct stock identities uniformly and calculate the equally funded buy-and-hold terminal wealth $P_k=k^{-1}\sum_{i\in A_k}S_{iT}$.
4. Record whether $P_k<1.5$, $P_k>1.5$, $P_k<1.3$, and $P_k>1.7$.
5. Average each indicator over 10,000 replications and plot the resulting probabilities by $k$.

The article does not fully specify whether one fixed universe is repeatedly subsampled or a new universe is regenerated for every Monte Carlo draw, whether portfolio sizes share the same draws, or the random seed. These alternatives agree on some unconditional quantities but differ in conditional sampling uncertainty. A reproduction should report the choice and separately test comparison with the actual same-replication full index if that is the desired financial benchmark.

For independent Bernoulli replications, the maximum standard error of a probability estimate with 10,000 draws is $\sqrt{0.25/10000}=0.005$, giving a rough 95% margin of about one percentage point. Reusing a fixed simulated universe introduces a different conditioning structure, so this bound describes simulation uncertainty under independent replications, not uncertainty in an empirically estimated market model.

No daily path simulation is needed for the source's terminal buy-and-hold payoffs. Directly drawing terminal values reproduces the model more efficiently and avoids discretization error. It would cease to be sufficient if one added rebalancing, stopping rules, margin constraints, or path-dependent selection, none of which is in this experiment.

## What the figure supports

Figure 1's left panel shows a high underperformance probability for concentrated portfolios and a narrowing imbalance as the number of stocks increases. Approximately, the probability below the 50% benchmark declines from around 0.65 for one stock toward roughly 0.54 around twenty stocks. The complementary probability above the benchmark increases correspondingly. These are approximate readings of a graph; the paper does not provide a table of exact plotted values.

The right panel compares more extreme outcomes, below a 30% gain and above a 70% gain. Concentration gives a greater chance of a large upside outcome, but the corresponding chance of substantial benchmark underperformance is larger. With more stocks both extreme probabilities fall and their gap narrows.

The prose suggests that selecting very few securities maximizes the chance of outperforming. That statement requires qualification. The left panel's ordinary probability of exceeding the mean benchmark actually increases with diversification over the displayed range. Concentration enhances the chance of an extreme upside threshold such as 70%, not the general probability of merely beating 50% in the displayed simulation. The choice of success threshold is therefore central to the interpretation.

The experiment does not establish a monotonic theorem for every portfolio size, every correlation structure, or every skewed return distribution. Sums of lognormals generally do not have a lognormal distribution, so replacing their exact simulated distribution by a lognormal with an arbitrary adjusted variance is an approximation, not a formula supplied by this paper.

## Limits and implications

There is no empirical stock-return panel, estimation window, train/test split, transaction-cost model, or fitted manager-skill model. The parameter values are illustrative calibrations. Fixed normally distributed drifts, equal volatilities, simple initial weights, no learning, and incomplete dependence specification restrict economic realism. Drift heterogeneity also grows increasingly influential with the horizon through $T^2$, so long-horizon extrapolation requires care.

Expected returns remain equal for unbiased random selections and the full index before fees. A larger underperformance probability is compatible with occasional very large outperformers that preserve the mean. This distinction is particularly relevant when interpreting the fraction of funds that beat a benchmark: a low fraction alone does not identify a negative cross-sectional mean alpha.

The paper's practical insight is that broad ownership captures rare large winners, while concentrated portfolios require either skill in identifying them or willingness to accept a skewed distribution of relative outcomes. Its model explains how indexing can deliver a more typical outcome near the cross-sectional average without claiming that passive investing wins every path or every objective. Reimplementation should preserve that probability-versus-expectation distinction and make the treatment of a realized versus expected benchmark explicit.
