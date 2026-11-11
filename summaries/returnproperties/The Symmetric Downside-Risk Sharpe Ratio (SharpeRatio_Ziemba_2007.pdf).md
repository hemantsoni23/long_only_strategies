# The Symmetric Downside-Risk Sharpe Ratio

William T. Ziemba. *The Journal of Portfolio Management*, Fall 2005, pp. 108–122. Subtitle: “And the Evaluation of Great Investors and Speculators.” Source: [SharpeRatio_Ziemba_2007.pdf](../../Finance/SharpeRatio_Ziemba_2007.pdf), 15 pages. The PDF's publication year is **2005**; 2007 in the library filename is not the article's publication year.

## Why this matters

Ordinary volatility penalizes unusually large positive returns as well as losses. That can produce an unappealing ranking when comparing a manager with occasional large gains against a manager whose returns are smooth partly because assets are infrequently marked. Ziemba proposes replacing full variance in the Sharpe ratio with twice a lower partial second moment. The factor of two constructs a hypothetical symmetric risk measure from the observed downside while preserving the ordinary Sharpe ratio's rough scale near a centered symmetric distribution.

The empirical question is whether that change improves the assessment of investors such as Berkshire Hathaway relative to institutions with smoother returns. In the source's monthly sample, Berkshire's reported annualized ratio rises from 0.773 to 0.917, but it still falls just below the Ford Foundation's downside ratio of 0.920. Changing the denominator does not establish the superior investment performance the motivating discussion seeks.

The article explicitly calls the measure ad hoc and does not establish its statistical properties or characterize when it can mislead. Its contributions are a simple performance convention and an extensive historical illustration, accompanied by a discussion of Kelly growth and risk. The note therefore separates three ideas: the exact definition of the downside statistic, descriptive investor rankings, and long-run growth-optimal investment theory. None alone proves the other two.

## Definition and normalization

Let $r_i$ be a portfolio's simple return in observation $i$, $n$ the total number of observations, $a$ a downside target, and $\bar r=n^{-1}\sum_i r_i$. The source uses $a=0$, applied to the portfolio's raw return rather than its excess return over cash. Define

$$
\widehat L_2(a)=\frac{1}{n-1}\sum_{i=1}^n(r_i-a)^2\mathbf1_{\{r_i<a\}}.
$$

Only below-target observations contribute to the numerator, but the denominator is based on **all** observations, not the number of losses. The symmetric downside deviation is

$$
\widehat\sigma_-=\sqrt{2\widehat L_2(a)},
$$

and the proposed ratio is

$$
S_- =\frac{\bar r-r_f}{\widehat\sigma_-}.
$$

The risk-free return $r_f$, portfolio mean, and downside deviation must refer to a consistent period. The article reports both arithmetic-mean and geometric-mean versions and annualizes statistics estimated from monthly and quarterly data.

The source uses $n-1$, analogous to a sample-variance convention. Since the target $a=0$ is fixed rather than estimated as a sample mean, dividing the sum by $n$ would be the unbiased estimator of the population lower partial second moment under iid observations. The $n-1$ divisor is a convention here, not a general unbiasedness result. A reproduction must nevertheless use the printed convention to match the paper.

The measure incorporates both loss frequency and loss magnitude. If $m$ of the $n$ returns are negative, then

$$
\widehat L_2(0)=\frac{m}{n-1}\left(\frac1m\sum_{r_i<0}r_i^2\right).
$$

It is not the conditional standard deviation of losing observations around their conditional mean. A strategy with many identical negative returns can have zero conditional variance of losses but a strictly positive downside deviation. Confusing those quantities would reverse the interpretation of a seemingly stable losing strategy.

If no observed return is below the target, the downside denominator is zero. A finite reported ratio is then unavailable; a positive numerator should not be advertised as evidence of riskless skill merely because the sample missed a rare loss. This is particularly relevant for annual observations and short-option-like strategies.

## Relation to ordinary Sharpe and Sortino ratios

The factor of two imagines a corresponding upside distribution that mirrors the observed downside. It does not establish that twice the lower partial second moment equals the actual return variance. Equality requires restrictive centering and symmetry conditions. For a distribution symmetric around zero with mean zero,

$$
2E[R^2\mathbf1_{\{R<0\}}]=E[R^2]=\operatorname{Var}(R).
$$

With positive mean, even an exactly normal return distribution generally fails that identity when the target remains zero. For $R\sim N(\mu,\sigma^2)$, set $z=\mu/\sigma$. Direct integration gives

$$
E[R^2\mathbf1_{\{R<0\}}]
=(\sigma^2+\mu^2)\Phi(-z)-\mu\sigma\phi(z).
$$

At $\mu=0$ this is $\sigma^2/2$. As the mean shifts upward, both loss probability and loss magnitudes change, so the downside denominator responds to location as well as dispersion. The proposed ratio therefore rewards favorable shifts through both numerator and denominator. It is not simply an estimate of the ordinary Sharpe ratio with upside observations removed as noise.

A Sortino-style ratio with the same numerator, target, and lower-partial-moment denominator but without the factor of two satisfies $S_-=S_{\mathrm{Sortino}}/\sqrt2$. The ranking is then unchanged. Actual Sortino implementations may use different targets, numerators, and sample divisors, so this relationship requires conventions to be aligned explicitly.

Changing the downside target changes the economic question. Zero measures outright nominal losses. A risk-free target measures failure to beat cash; an inflation target measures loss of purchasing power; a liability-growth target measures failure to meet obligations. The paper chooses zero for convenience and interpretation, while acknowledging that other targets are possible. It should not be silently rewritten as a shortfall relative to the same cash return used in the numerator.

Positive scaling is straightforward if returns, target, and reference return are all scaled consistently. Adding a cash return while leaving the downside target fixed at zero is different: it changes which observations count as losses. Thus the familiar invariance intuitions for the ordinary excess-return Sharpe ratio do not transfer without qualification.

## Data, frequency, and the actual comparison

The article assembles returns for Windsor, Berkshire Hathaway, Quantum, Tiger, the Ford Foundation, Harvard's endowment, the S&P 500, U.S. Treasuries, Treasury bills, and inflation. Harvard is available quarterly rather than monthly. Main tables identify 172 monthly observations, 57 quarterly observations, and fourteen annual observations. Captions describe December 1985–April 2000, while some prose and figures refer to an ending month of March 2000. Other figures cover longer histories, including 1977–2000, and the Berkshire book-value table spans 1965–2004.

These samples should not be treated as one interchangeable panel. The 172 monthly and 57 quarterly counts do not imply precisely identical endpoints, and the fourteen calendar-year observations cover 1986–1999. Exact time stamps and original series would be needed to resolve the boundary conventions. The note preserves the reported counts rather than inventing a harmonized sample.

The ordinary and downside ratios computed from monthly arithmetic returns and then annualized are:

| Investment | Ordinary Sharpe | Symmetric downside Sharpe |
|---|---:|---:|
| Ford Foundation | 0.970 | 0.920 |
| Tiger | 0.879 | 0.865 |
| S&P 500 | 0.797 | 0.696 |
| Berkshire Hathaway | 0.773 | 0.917 |
| Quantum | 0.622 | 0.458 |
| Windsor | 0.543 | 0.495 |

Berkshire is the only member of this table whose ratio increases when the denominator changes. It moves ahead of Tiger and the S&P 500, but Ford remains slightly higher. That difference is only 0.003 in the displayed ratios; the paper supplies no confidence interval establishing that the ranking is statistically meaningful.

The reported monthly-based annual arithmetic mean for Berkshire is 25.77%, ordinary volatility 26.54%, and symmetric downside deviation 22.36%, with annualized cash return 5.27%. Thus $(25.77-5.27)/22.36=0.916816$, which rounds to 0.917. Ford's corresponding mean is 14.29%, ordinary volatility 9.30%, and downside deviation 9.81%; the rounded inputs give $(14.29-5.27)/9.81=0.919470$. The tiny difference between that calculation and the printed 0.920 can be explained by rounding of table inputs, not by an identified residual risk adjustment.

Berkshire has greater terminal wealth growth in these illustrations, yet a lower or similar risk-adjusted ratio because its losses are larger. The measure does not purport to maximize terminal wealth, and an investor's ranking can differ depending on risk aversion, liquidity needs, and horizon. Comparing a mean-to-risk ratio with cumulative wealth requires stating the objective.

## Quarterly and annual evidence

Quarterly data permit Harvard to enter the comparison. The source reports the following annualized arithmetic-return statistics:

| Investment | Mean, % | Ordinary volatility, % | Ordinary Sharpe | Downside deviation, % | Downside Sharpe |
|---|---:|---:|---:|---:|---:|
| Berkshire | 26.81 | 29.50 | 0.729 | 28.00 | 0.769 |
| Quantum | 22.79 | 25.33 | 0.691 | 24.17 | 0.724 |
| Tiger | 17.42 | 15.40 | 0.788 | 16.35 | 0.742 |
| Ford | 14.71 | 9.43 | 0.999 | 8.89 | 1.060 |
| Harvard | 15.44 | 9.45 | 1.074 | 10.24 | 0.991 |
| S&P 500 | 17.91 | 15.05 | 0.839 | 19.78 | 0.638 |

The cash return used here is approximately 5.29% annualized. Harvard leads Ford under ordinary Sharpe, while Ford leads Harvard under symmetric downside Sharpe. Both lead Berkshire in this quarterly comparison. Computing Harvard's downside ratio from the displayed numbers gives $(15.44-5.29)/10.24=0.991211$, consistent with the table.

Annual-frequency ordinary Sharpe ratios tell a somewhat different story: Harvard 1.181, Tiger 1.109, Quantum 1.084, S&P 500 1.033, Ford 1.001, and Berkshire 0.763. Therefore a general statement that Ford has the highest ordinary Sharpe must be restricted to the relevant frequency and subset. The annual table itself does not support that universal ranking.

The source declines to estimate annual downside Sharpe ratios because there are too few annual losses. Of fourteen years, Berkshire has two negative years, Ford one, and Tiger none. This is an appropriate warning about sparse downside data. Monthly observations provide more losses, but do not guarantee independent information about rare annual losses or multi-year drawdowns.

Exhibit 20 reports 58 negative Berkshire months out of 172 and 44 negative Ford months. Berkshire's mean losing-month return is −5.36%, compared with its all-month mean of +2.15%. Ford's table gives −2.24% in losing months and +1.19% across all months; adjacent prose prints −2.44%, an inconsistency. The table value is used here. Multiplying a conditional average monthly loss by twelve, as the discussion does when referring to annualized losses, does not produce an observed annual drawdown, a value-at-risk estimate, or a tail conditional expectation at an annual horizon.

## Compounding, annualization, and valuation smoothing

The article reports arithmetic and geometric means because they describe different investment questions. The arithmetic mean estimates expected one-period return under an appropriate sampling model. The geometric mean summarizes compounded growth. Replacing one with the other is not a general correction for serial dependence or estimation bias.

For a +50% return followed by −50%, final wealth is 75% of initial wealth. The two-period geometric mean is $\sqrt{1.5\times0.5}-1=-13.3975\%$ per period; the article prints −13.7%. The arithmetic mean is zero, correctly describing the average of the two simple returns, but not the realized compound growth rate. The two means answer different questions rather than one being universally erroneous.

Square-root annualization of ordinary volatility follows from independent additive returns. Annual downside moments do not generally equal a fixed multiple of monthly downside moments, even under independence, because gains and losses offset before the annual shortfall indicator is applied. The source's annualized monthly and quarterly downside ratios are reporting conventions. They should not be mistaken for exact ratios computed from the distribution of compounded annual losses.

The paper discusses Lo's correction for ordinary Sharpe ratios under serially dependent returns. That correction concerns the variance of aggregated returns and does not automatically provide an equivalent correction for a lower partial second moment. Estimating a geometric mean likewise does not remove stale-price effects or serial correlation from either denominator.

Valuation smoothing is a particularly serious confounder. The source acknowledges that part of Ford's high Sharpe ratio may arise from private-equity valuations that understate current economic volatility, and that a similar issue applies to Harvard. Downside deviations can also be artificially small when negative economic returns enter reported valuations gradually. Substituting downside risk for full volatility does not repair the measurement problem.

The asset-allocation illustration for Harvard in June 2004 includes private equity, hedge funds, real estate, and other nontraditional assets, and reports total exposure above 100% because of slight leverage. That illustration is later than the principal return sample and should not be treated as exact holdings data for 1986–2000. It supports the plausibility of valuation and liquidity differences, not a retrospective holdings-level risk reconstruction.

## Kelly growth: what is established and what is separate

A substantial portion of the article explains why growth-oriented investors can rationally accept volatile paths. For independent bets paying +1 or −1 per unit staked, with win probability $p$ and loss probability $q=1-p$, betting fraction $f$ of current wealth produces

$$
W_N=W_0(1+f)^M(1-f)^{N-M},
$$

where $M$ is the number of wins. The strong law gives long-run log growth

$$
g(f)=p\log(1+f)+q\log(1-f).
$$

Differentiating yields $g'(f)=p/(1+f)-q/(1-f)$, so the interior optimum is $f^*=p-q$. If a win pays odds $O$ to one and a loss loses the stake, then

$$
g(f)=p\log(1+Of)+q\log(1-f),\qquad
f^*=\frac{pO-q}{O}.
$$

Known probabilities, repeated opportunities, appropriate wealth constraints, and a long-run growth objective are essential. Estimation error in the edge can lead to excessive stakes and substantial losses.

For a frictionless geometric-Brownian risky asset with known drift $\mu$, volatility $\sigma$, and a cash rate $r$, log-optimal risky exposure is $(\mu-r)/\sigma^2$. Its optimal growth rate is

$$
g^*=r+\frac12\left(\frac{\mu-r}{\sigma}\right)^2.
$$

This links **ordinary** Sharpe to optimal log growth under that specific diffusion model. It does not derive the proposed downside Sharpe ratio, nor prove that maximizing downside Sharpe maximizes growth under general returns.

Log utility has absolute risk aversion $1/W$ and relative risk aversion one. The source's description of its absolute risk aversion as essentially zero should not be treated as a unit-independent economic statement: changing the units of wealth changes the numerical value of absolute risk aversion. The relative-risk-aversion characterization is unambiguous.

The paper also gives a broad asymptotic wealth-dominance statement for a Kelly bettor versus an essentially different bettor. A rigorous application requires conditions on persistent departure from optimal growth. Merely differing infinitely often is not enough without qualification; departures that shrink sufficiently fast can have a finite cumulative growth penalty. The safe interpretation is long-run superiority over fixed or persistently growth-suboptimal rules under the assumed repeated-bet model, not dominance over every alternative path-dependent policy.

## Reproducing the Kelly simulation design

The article reproduces a simulation from Ziemba and Hausch (1986): 1,000 paths of 700 independent wagers, starting with wealth of \$1,000. Five wager types are sampled with the probabilities below. Every wager has an expected net return of 14% per dollar staked; this is an edge, not a 14% probability of success.

| Odds $O$ | Win probability | Probability of selecting wager type | Full-Kelly fraction |
|---:|---:|---:|---:|
| 1 | 0.570 | 0.10 | 0.140 |
| 2 | 0.380 | 0.30 | 0.070 |
| 3 | 0.285 | 0.30 | 0.046667 |
| 4 | 0.228 | 0.20 | 0.035 |
| 5 | 0.190 | 0.10 | 0.028 |

For each wager, draw its type, draw the win/loss outcome with the corresponding probability, and multiply wealth by $1+Of$ on a win or $1-f$ on a loss. Half-Kelly uses half the displayed fraction. Repeating those steps reconstructs the experimental design, but not the original Monte Carlo realizations because the random seed and original draws are absent.

The reported full-Kelly final wealth has minimum \$18, maximum \$483,883, mean \$48,135, and median \$17,269. Half-Kelly has minimum \$145, maximum \$111,770, mean \$13,069, and median \$8,043. Full-Kelly finishes above initial wealth in 870 of 1,000 paths, while half-Kelly does so in 954. Full-Kelly exceeds \$100,000 in 166 paths; half-Kelly does so once.

These results demonstrate a meaningful finite-horizon tradeoff. Full-Kelly has greater mean and median terminal wealth but worse outcomes in some paths and a lower probability of being ahead after 700 bets. A sample minimum of \$18 is not a deterministic lower bound or a stated ruin probability. Nor do the historical gambling and investor examples prove that successful investors estimated probabilities accurately or followed a Kelly rule in their actual portfolios.

## Reproduction requirements and substantive limitations

The tables provide enough aggregate data to verify selected reported ratios, compare rankings, and implement the proposed estimator. They do not provide the complete monthly return panel, precise timestamps, valuation adjustments, fee treatment, index vintages, cash-return series, or underlying private-asset marks. Those inputs are required to reproduce all statistics, charts, and differences between arithmetic and geometric variants.

The sample is intentionally composed of notable investors and institutions. It is not a representative manager universe with a disclosed selection protocol. Survivorship and retrospective selection are therefore central limitations. Differences in mandate, leverage, liquidity, taxes, investable capacity, and public versus private valuation also prevent treating the rankings as clean estimates of manager skill.

The downside measure omits information about the shape and timing of upside outcomes and does not encode path-dependent drawdown preferences. It can be manipulated by smoothing marks or by trading strategies whose rare adverse outcomes have not yet appeared. The source discusses the broader vulnerability of Sharpe measures to option overlays and acknowledges that formal analysis of misleading cases for its own statistic remains open.

For an institutional application, a useful report would retain ordinary Sharpe, the explicitly defined downside ratio, loss counts, largest losses, valuation frequency, serial dependence, compounded growth, and drawdown information side by side. These are different views of the same return history. A single ratio cannot resolve a dispute that is actually about wealth growth, tolerance for interim losses, or comparability of reported valuations.

The paper's durable point is that upside dispersion and downside shortfall need not carry the same economic meaning. Its numerical lesson is more restrained: replacing the denominator materially changes some rankings, yet leaves valuation smoothing, sparse tail data, sample selection, and investment objectives unresolved. Berkshire's improved ratio is an illustration of the convention's consequences, not a statistical proof of superiority.

## Source and verification record

All fifteen pages, including endnotes and references, were read. PDF pages 3–7 and 9–13 were visually inspected for the investor-return tables, Kelly formulas and simulation inputs, downside definition, frequency comparisons, allocation illustration, and final caveats. Selected ratios and the two-period compounding example were independently recomputed. The normal lower-partial-moment identity and normalization qualifications are analytical checks in this note. No claim is made to reproduce the unavailable original investor series or original random simulation draws.
