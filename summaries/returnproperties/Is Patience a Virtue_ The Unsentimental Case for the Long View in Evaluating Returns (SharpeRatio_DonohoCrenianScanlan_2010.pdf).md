# Is Patience a Virtue? The Unsentimental Case for the Long View in Evaluating Returns

David L. Donoho, Robert A. Crenian, and Matthew H. Scanlan. *The Journal of Portfolio Management*, 37(1), Fall 2010, pp. 105–120.

Source: [SharpeRatio_DonohoCrenianScanlan_2010.pdf](<../../Finance/SharpeRatio_DonohoCrenianScanlan_2010.pdf>). References below use printed journal pages and exhibit numbers. The entire article, including endnotes, was inspected; the graphical exhibits and the simulation specification require particular care.

## Why this matters

A manager can have positive, persistent skill and still spend a long time under water. Conversely, a manager with no skill can enter the top performance decile through luck. The paper studies how an allocator's evaluation horizon interacts with these two facts. It constructs artificial manager populations in which true skill is known, then compares allocation rules that use only realized past returns.

The innovation is this controlled separation of latent skill, noisy track records, and subsequent hiring or firing. It is not an empirical test that particular real managers possess persistent alpha. The simulations ask what selection errors arise even in a favorable world where skill never decays. Longer histories help identify skill in that world, and patient selection policies generally produce higher returns and less turnover.

The result is useful as a benchmark for manager monitoring. It is not a theorem that retaining every underperformer is optimal, or that ten-year records should always dominate recent evidence. The authors explicitly recognize that strategy changes can make old data irrelevant. Their main model excludes that possibility, capacity limits, and manager exit from the investable population.

## Signal-to-noise calculation motivating the experiment

Let annual alpha be $a$ and annual residual volatility be $\sigma_a$. Under independent observations and stable parameters, a simple population signal-to-noise calculation gives

$$
t\approx\frac{a}{\sigma_a}\sqrt{Y},
\qquad
Y\approx\left(\frac{t\sigma_a}{a}\right)^2.
$$

With alpha 2%, residual volatility 5%, and a threshold of two, the implied history is 25 years. With alpha 1% and the same volatility, it is 100 years. These are the opening examples on p. 105. They express the difficulty of detecting a small drift through noisy returns; they do not say that every realized sample first becomes significant at exactly those dates. Sequential testing, estimated benchmarks, serial correlation, selection among many managers, and changing skill would require a different inferential analysis.

The square dependence is central. Halving the information ratio requires four times as much independent history to maintain the same signal-to-noise level. Increasing the sampling frequency does not produce proportionately more information about a fixed annual drift when it merely subdivides the same diffusion path.

## The artificial manager economy

The agents are a plan with investable assets, a CIO represented by an allocation algorithm, and managers represented by return generators. In the main selection experiments there are 1,000 managers: 100 skilled and 900 unskilled. The skilled managers share a specified true Sharpe ratio, chosen separately as 0.25, 0.50, 0.75, or 1.00. The remaining managers have a true Sharpe ratio of zero. Within a scenario, skill is constant across the entire history and future evaluation period.

Returns are independent across managers and time. Risk-free return is zero, and managers have zero beta to all market benchmarks. Thus Sharpe and information ratios coincide within this construction. This equivalence would not hold for ordinary total-return managers exposed to different market risks. The authors suggest interpreting their streams as active returns and rescaling volatility accordingly, but do not estimate such residuals from real data.

The intended price process is geometric Brownian motion: normal log increments produce lognormal gross wealth relatives. The sentence on p. 108 describing log returns themselves as lognormal is inconsistent with the independent standard normals in endnote 9. The latter gives the actual algebraic specification:

$$
R_{tm}=v(S_m+Z_{tm}),
\qquad Z_{tm}\sim N(0,1),
\qquad R_{tm}=\log(1+r_{tm}).
$$

Endnote 9 states

$$
v=\frac{\log(1.18)}{\sqrt{252}},
\qquad D=2500,
\qquad M=1000,
$$

and 1,000 Monte Carlo runs. Here $D$ is described as approximately ten years of trading days. The daily volatility is about 0.0104264, giving annual log-return volatility $\log(1.18)=0.1655144$. The article calls this roughly 18% annual volatility. That is an approximation based on its chosen conversion, not the ordinary equality $\sigma_{\mathrm{annual}}=\sqrt{252}\sigma_{\mathrm{daily}}$ with 18% on the left.

There is also a units gap: a daily return formula requires a daily Sharpe input. If $S_m$ in the displayed equation were literally set to the stated annual levels 0.25–1.00, annualized log-return Sharpe ratios would be larger by $\sqrt{252}$. A dimensionally coherent reconstruction must instead use $s_m=S_m^{\mathrm{annual}}/\sqrt{252}$ in that daily equation, or specify another explicit drift convention. The source does not print this conversion. It also does not clearly distinguish a Sharpe ratio of log returns from one based on simple returns.

For example, with daily normal log return mean $a_d$ and variance $v^2$, the exact one-year gross-return expectation is $\exp(252a_d+252v^2/2)$. Mean log return, expected simple return, and geometric growth differ. A replication should keep these quantities separate rather than use the term annual return for all three.

## Experiments on drawdown

The first illustration contains nine independent five-year wealth paths, each generated with expected Sharpe ratio 0.5. Their starting values are normalized to \$1. Some paths rise strongly, some barely recover their starting value, and some decline. The panels use different vertical scales, so visual slopes should not be compared without reading the axes. The absence of a losing outcome in nine supplementary ten-year paths is explicitly not claimed as proof that a loss is impossible.

The drawdown experiments then use annual volatility described as 18% and true Sharpe levels 0.25, 0.5, 0.75, and 1. They distinguish three objects:

1. The probability that a manager is currently in a drawdown that has already lasted at least a specified number of trading days.
2. The probability that the longest drawdown encountered in a trailing three-year history lasts at least that many days.
3. The distribution of the deepest drawdown over that history, expressed as wealth remaining relative to the preceding high-water mark.

These are different distributions. A current spell is not the longest completed spell in a window, and a drawdown that is still ongoing is censored. The paper defines the reference high-water mark relative to the last three years, but it does not provide precise pseudocode for rolling-window boundary handling, censored spells, or the inclusion of peaks before the window.

Exhibit 2 and the accompanying text report that more than half the managers with true Sharpe 0.25 are currently in a drawdown lasting at least a year. The fraction is around one quarter for true Sharpe 0.75 and one seventh for true Sharpe 1. These are approximate graphical findings. Exhibit 3 concerns the maximum duration over three years and gives much higher probabilities at the same duration threshold.

Some prose on p. 111 does not agree with the adjacent depth graph. It says that two in five Sharpe-one managers have a drawdown of at least 15%, and describes a median decline in value of 80 cents from an initial dollar. Exhibit 4 instead plots wealth **remaining** as a fraction of the high-water mark, with the Sharpe-one curve crossing probability one half around 0.78. It is therefore inappropriate to translate that sentence into a measured median loss of 80%. The chart is consistent with a drawdown on the order of one fifth, and its probability at 0.85 remaining wealth is much higher than 40%. These discrepancies should remain visible until original output is available.

The robust qualitative point survives those numerical inconsistencies: high true skill does not prevent prolonged or material drawdowns in a noisy diffusion. The paper does not estimate the probability that an observed drawdown was caused by declining skill, since declining skill is excluded by construction.

## Ranking skilled managers among unskilled managers

For each simulated universe, the authors rank all managers by historical returns over horizons from one to ten years. Because volatility is common, return ranking is a natural simplified performance statistic. It is not a ranking by a separately estimated alpha after heterogeneous factor exposures.

Exhibit 5 reports the average percentile rank of skilled managers, where a lower percentile is better. For true Sharpe 1, the text gives approximately the 22nd percentile using one-year history, the 14th using five years, and the 12th using ten years. Exhibit 6 measures a different statistic: the number of truly skilled managers among the 100 top-ranked managers. The source reports:

| True Sharpe of skilled managers | One-year ranking | Five-year ranking | Ten-year ranking |
|---|---:|---:|---:|
| 0.50 | 35 of 100 | approximately 45 of 100 | 49 of 100 |
| 1.00 | 65 of 100 | 81 of 100 | 84 of 100 |

The five-year figure for Sharpe 0.5 is approximate; the prose supplies a 28% increase from the one-year count rather than a full numerical table. With 100 skilled managers in a top-decile portfolio of size 100, the count also gives both recall and precision in this special balanced setup. In a different prevalence or selection fraction, those measures would differ.

These numbers demonstrate the intended mechanism: short-window winners contain both good managers and unusually lucky unskilled managers. A longer window lets drift accumulate relative to noise. The source emphasizes diminishing marginal benefits beyond five years, but the magnitude of those benefits depends on the unresolved specification issues discussed below.

## An analytical check on the published ranking figures

The equal-volatility normal-log-return model permits a useful independent diagnostic. This is a derivation for replication, not an additional result reported by the authors. Under a correctly annualized log Sharpe $S$ and a $Y$-year horizon, standardized cumulative log returns are $N(0,1)$ for unskilled managers and $N(d,1)$ for skilled managers, with $d=S\sqrt Y$.

For skilled prevalence $p=0.1$, the population approximation to the mean percentile rank of a skilled manager is

$$
\bar P=\frac p2+(1-p)\Phi\left(-\frac d{\sqrt2}\right).
$$

The first term reflects the random ordering among equally skilled managers; the second is the probability an unskilled manager outperforms a skilled one. At infinite horizon, mean rank tends toward 5%, not 10%: all skilled managers occupy the top decile, but their average rank is the middle of that decile. Finite-universe rank conventions introduce only small corrections.

For selection fraction 0.1, let $z$ solve

$$
(1-p)[1-\Phi(z)]+p[1-\Phi(z-d)]=0.1.
$$

The expected skilled count in the top 100 is approximately $100[1-\Phi(z-d)]$. Numerical solution gives, for $S=1$, about 33, 67, and 85 skilled managers at one, five, and ten years. For $S=0.5$, the corresponding values are about 20, 36, and 50. These differ materially from the early-horizon figures in the article, even though the ten-year counts are close. Likewise, the $S=1$ mean percentile formula gives about 26.6%, 10.1%, and 6.1% at those horizons.

This does not identify the authors' actual programming choices. It establishes that a straightforward, units-consistent reconstruction of the printed constant-volatility model is not enough to recover all published ranking numbers. Original code, a clarified definition of the horizon, and a clarified annualization convention are needed. One should not silently tune a drift or history offset until the charts match and then call that a replication.

## Selection-period versus future performance

The next experiment forms an equal-weight portfolio of the historical top decile and evaluates one subsequent year. Managers are assumed to have at least ten years of history, so the same population is available for each lookback. The selected historical average is biased upward by selection on favorable realized noise. Future returns have fresh noise, leaving only the selected cohort's mixture of true skill.

Exhibit 7 plots historical and future annualized returns separately. Short lookbacks produce the most spectacular pre-hiring performance and the greatest subsequent disappointment. Longer lookbacks reduce the gap and improve the expected skill composition. The prose reports future returns of 13.2% after selection on three-year history and 20.1% after selection on ten-year history when skilled managers have Sharpe 1. It also reports future returns 52% below selection-period returns for the three-year case, versus about 10% below for the ten-year case.

These are reported simulation numbers, not verified replications. Their exact magnitudes depend on the return definition and compounding convention; they cannot be inferred solely from a Sharpe ratio and the phrase 18% annual volatility. A reconstruction should report arithmetic averages across managers, portfolio compounded returns, and averages across Monte Carlo worlds as separate quantities. Averaging managers' log returns would describe a different wealth process from an equal-weight portfolio of their simple returns.

The economic explanation requires no systematic reversal in an individual manager's skill. Conditioning on a high realized past return selects positive noise. That noise disappears in expectation in a disjoint future period. This is a selection effect in an IID model, rather than evidence of a negative return autocorrelation or of structural deterioration after hiring.

## Dynamic hiring, firing, and rehiring rules

Exhibit 8 defines five CIO algorithms. All start with 100 selected managers, and the text says the held managers are reviewed annually. The selection rule governs entry; the firing and rehiring rules then distinguish persistence from wholesale annual reselection.

| Personality | Initial selection | Firing trigger | Rehiring rule |
|---|---|---|---|
| Ruthless short-term | Top decile of one-year returns | 10% drawdown | Never |
| Forgiving short-term | Top decile of one-year returns | 10% drawdown | New high-water mark |
| Watchful long-term | Top decile of five-year returns | Bottom decile of one-year returns | Top decile of one-year returns |
| Loyal long-term | Top decile of five-year returns | Bottom decile of five-year returns | Top decile of five-year returns |
| Buy and hold | Top decile of five-year returns | Never | Not applicable |

The text does not fully reconcile annual review with a trigger stated as entering a 10% drawdown. Testing the trigger daily and acting immediately differs from checking it once a year or checking whether it was breached during the prior year. It also leaves details of replacement ordering, previously fired candidate eligibility, exact HWM reset rules, and continuing portfolio rebalancing unspecified. These affect turnover and the ability of skilled managers to remain invested.

Exhibit 9 reports ten-year results. For a skilled-manager Sharpe of 1, the gross and net returns, transition counts, and skilled-manager exposure are:

| Rule | Gross annual return | Net annual return | Transactions in ten years | Fraction in skilled managers |
|---|---:|---:|---:|---:|
| Ruthless short-term | 8.06% | 7.69% | 547 | 0.33 |
| Forgiving short-term | 10.10% | 9.72% | 221 | 0.43 |
| Watchful long-term | 15.98% | 15.94% | 116 | 0.72 |
| Loyal long-term | 15.58% | 15.57% | 110 | 0.70 |
| Buy and hold | 14.96% | 14.96% | 100 | 0.67 |

The transaction count includes the original 100 hires: 100 for buy and hold means zero replacements. Thus the ruthless rule makes 447 further counted transactions in this scenario, around 44.7 per year, while the watchful rule makes 16, around 1.6 per year. The table does not represent 547 full-portfolio liquidations.

At true Sharpe 0.75, gross returns are respectively 5.38%, 6.56%, 9.96%, 9.85%, and 9.24%; net returns are 5.00%, 6.14%, 9.91%, 9.84%, and 9.24%. At Sharpe 0.5, net returns are 3.08%, 3.44%, 5.40%, 5.45%, and 5.18%. At Sharpe 0.25, they are 1.79%, 1.82%, 2.54%, 2.64%, and 2.63%. The long-horizon group generally wins, but the small differences within that group at low skill are not supported by reported confidence intervals.

The fixed exit cost is 75 basis points of the assets being moved out of a manager. The authors explicitly say they have not justified that calibration. It is an illustrative transition charge, not an estimated trading-cost model or a 75-basis-point deduction from the entire plan at every firing. At Sharpe 0.75 the ruthless rule loses 0.38 percentage point, about 7% of its gross annual return; the watchful rule loses 0.05 percentage point, about 0.5% of its gross return. Percent changes in return and percentage-point costs must not be conflated.

The final table's fraction in skilled managers is described in the text in terms of portfolio dollar-days. It reflects capital exposure over time, not just the number of distinct skilled managers ever hired. The improvement of watchful over loyal at high skill also shows that the result is more nuanced than indiscriminate patience: long-horizon entry can be combined with a severe short-horizon exit signal.

## A transparent reconstruction protocol

Generate a fixed population of skill labels before generating returns. Record the seed, number of worlds, daily and annual parameter conventions, and normal draw construction. Simulate sufficient prehistory for the longest lookback plus a separate investment period. Endnote 9 gives 2,500 days, whereas ten-year selection followed by ten-year dynamic evaluation requires additional history; the article does not specify exactly how this is allocated or reused.

At each decision date, use only observations available before the next holding period. Rank cumulative log returns or their equivalent compounded wealth relatives, select the prescribed managers, and maintain a separate record of historical eligibility and rehiring status. For wealth accounting, convert log increments into simple returns and apply them to actual capital weights. State whether weights drift between annual reviews or are periodically reset, and charge exit costs only on departing assets.

Use the same simulated manager panels when comparing CIO rules to reduce noise in paired differences. Report Monte Carlo standard errors across independent worlds, not across overlapping daily drawdown observations. For quantiles and drawdown probabilities, specify rolling-window and censoring conventions. Keep the diagnostic normal-mixture ranking calculation as a unit check before implementing the more elaborate dynamic rules.

These instructions reconstruct a defensible experiment; several are explicit choices needed because the paper supplies no code. The reported figures should remain the target for comparison, with discrepancies reported rather than hidden. No seed, error bars, exact output data, detailed sensitivity-study settings, or full event-order specification are supplied.

## Scope of the conclusions

The authors attribute impatience partly to behavioral reactions, career incentives, compensation based on short-run rankings, and doubts about selection skill. These are interpretations and literature-based arguments, not channels identified by the Monte Carlo experiments. The simulated CIOs have no psychology, agency costs, liabilities, or endogenous compensation.

The claimed robustness to dependence and non-lognormal returns is only briefly described; no reproducible settings or numerical sensitivity table is given. It is not generally true that arbitrary fat tails or serial dependence can only strengthen a long-lookback policy. Skill decay, regime changes, survival, changing exposures, persistent manager correlation, and heterogeneous volatilities can alter both rankings and the optimal use of old data.

The enduring lesson is to compare manager-selection algorithms by the future wealth and skill exposure they produce, instead of rewarding spectacular selected backtests. In the article's stable-skill model, a longer entry record reduces selection on luck, and severe turnover can discard useful managers and impose costs. The precise optimal horizon for a real mandate remains an empirical and decision-theoretic question. The printed simulation gaps and inconsistencies mean that the paper is most reliable as a mechanism and experimental design, with its exact numerical results requiring clarification before operational calibration.
