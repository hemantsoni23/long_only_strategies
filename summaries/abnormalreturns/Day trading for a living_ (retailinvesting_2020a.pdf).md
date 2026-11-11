# Day trading for a living?

Fernando Chague, Rodrigo De-Losso, and Bruno Giovannetti, working paper, June 13, 2020. Source: [retailinvesting_2020a.pdf](../../Finance/retailinvesting_2020a.pdf), nine PDF pages, SSRN 3423101. This note concerns this working-paper version and its Brazilian equity-futures cohort.

## Why this matters

The question is whether persistent retail day trading plausibly provides a living, and whether traders improve with experience. The contribution is an administrative-data study of new entrants rather than a survey of survivors or an advertisement featuring successful traders. Even among traders who persist for more than 300 trading days, almost all lose after exchange and brokerage fees. The surviving winners face substantial daily profit variation. This is evidence about a particular opportunity set and entry cohort; it is not a causal experiment assigning people to trade, nor an estimate for all trading styles, markets, or periods.

## Population, timing, and outcome construction

The Brazilian securities regulator, CVM, supplied anonymized transaction records for individual day traders in mini-Ibovespa futures during 2012–2017. The authors identify 19,646 entrants during 2013–2015. Entry is defined relative to observed activity: a 2013 entrant did not trade in 2012, a 2014 entrant did not trade in 2012–2013, and similarly for 2015. The term new therefore means new within the observation history, not necessarily a person who has never traded before in another market or before 2012.

Entrants during 2016–2017, numbering 53,246, are excluded so the selected entrants have an opportunity to be followed for at least two years. This is an opportunity for follow-up, not a claim that every entrant traded continuously for two years. The empirical unit for the learning panel is an investor's active trading day. A person trading intermittently has a different calendar-time trajectory from someone trading daily even if both reach the same experience count.

The distribution of trading persistence is central to interpreting the sample:

| Number of active trading days | Entrants | Share |
|---|---:|---:|
| 1 | 1,111 | 5.7% |
| 2–50 | 9,978 | 50.8% |
| 51–100 | 3,100 | 15.8% |
| 101–200 | 2,738 | 13.9% |
| 201–300 | 1,168 | 5.9% |
| More than 300 | 1,551 | 7.9% |

The prose sometimes describes the persistent group as trading at least 300 days, whereas the displayed grouping uses more than 300. An exact replication should resolve that boundary from the authors' code or data rather than silently choose an alternative.

Gross daily profit is distinguished from profit net of exchange and brokerage fees. Net profit excludes income taxes and expenditures on platforms or courses. Consequently the reported net outcome can exceed disposable income from trading. The paper does not give a complete executable fee schedule, contract-position reconstruction, capital account, or dollar-conversion rule. Those are missing replication inputs, particularly if one wants to rebuild profit from raw transactions rather than use the authors' prepared investor-day observations.

For trader $i$ with $T_i$ active days, the descriptive quantities can be written as

$
\bar\pi_i=T_i^{-1}\sum_{d=1}^{T_i}\pi_{id},\qquad
s_i=\left[\frac{1}{T_i-1}\sum_d(\pi_{id}-\bar\pi_i)^2\right]^{1/2}.
$

Here $\pi_{id}$ is daily net profit in the paper's US-dollar units. This notation clarifies what the reported mean and standard deviation measure; it is not a return normalized by invested capital. The observations do not establish an annualized investment Sharpe ratio, risk of ruin, or required working capital.

## Profitability and income comparisons

Among the 1,551 persistent traders, only 47 have positive net average profit: approximately 3.0%, leaving 97% losing. Seventeen, or about 1.1%, exceed the Brazilian minimum-wage comparison of \$16 per day. Eight, or about 0.5%, exceed the initial bank-teller salary comparison of \$54 per day. The wage comparisons incorporate the paper's annual salary and legal-benefit conventions: annual amounts are \$3,965.96 for minimum wage and \$13,648.86 for the teller benchmark. They are income reference points, not adjustments for trading capital, employment security, or equivalent hours worked.

The best trader earns an average \$310 daily but has daily-profit standard deviation \$2,560. Across the eight traders exceeding the teller threshold, standard deviations range from \$632 to \$3,308. Figure 2 plots the means and standard deviations of the 47 profitable persistent traders, making clear that positive average income can coexist with losses large relative to a day's typical earnings. It would be incorrect to infer that the maximum daily loss equals a reported standard deviation or to assume normal profit tails from this plot.

Figure 1 compares positive-profit fractions across persistence groups. Gross profitability falls from roughly 35% among one-day traders to approximately 12% for the persistent group; after fees, the corresponding shares are roughly 30% and 3%. These are approximate readings of the figure. The dashed intervals are labeled 95% confidence intervals, but the exact interval construction is not specified. The 47, 17, and eight counts above are reported numerical outcomes rather than readings from that graph.

The persistence comparison conditions on behavior chosen after entry. People may stop because of losses, financial constraints, or a change of interests; others may persist for reasons unrelated to skill. Thus the cross-group slope is not a randomized estimate of the effect of trading another day. It nevertheless directly challenges the narrower proposition that merely persisting selects a group that usually earns a viable living.

## Learning specification and statistical evidence

The learning analysis retains the 1,551 persistent traders and uses 714,637 investor-day observations. Regressions include trader fixed effects and investor-clustered standard errors. One specification relates daily profit to the sequential count of a trader's active days; another replaces the trend with indicators for the first and last thirds of each trader's observations, leaving the middle third as reference.

A schematic expression for the first specification is

$
\pi_{id}=a_i+b\,d+u_{id}.
$

The coefficient $b$ measures the within-trader dollar-profit association with active-day experience in this selected panel. Fixed effects absorb persistent level differences between traders. They do not control automatically for calendar-market conditions, changing position size, or a strategy change correlated with experience.

Table 1 reports a gross-profit trend of $0.005$ with standard error $0.011$, statistically insignificant. The net-profit trend is $-0.019$ with standard error $0.011$, marked significant only at the 10% level. This is approximately a 1.9-cent reduction in daily dollar profit per additional active trading day within that specification, not a 1.9% reduction in returns. The gross and net specifications have reported $R^2$ values of 1.32% and 2.04%.

In the tercile regressions, gross-profit first- and last-third coefficients are $-0.533$ and $-0.120$, with standard errors $2.490$ and $3.396$. Net-profit coefficients are $1.742$ and $-5.769$, with standard errors $2.757$ and $3.596$. They do not establish an improving terminal segment relative to the middle segment. The paper concludes that its analysis supplies no evidence of learning. This is a conclusion about these profit specifications and this selected population; it does not prove that no trader learns anything or that all imaginable risk-adjusted skill measures must be constant.

## Replication limits and interpretation

A faithful reproduction needs the regulator's transaction data, the entrant-screening history, definitions of an active day and intraday position closure, the exact fee and currency conversions, and the persistent-cohort boundary. To reproduce Table 1 it also needs the handling of ties in tercile assignment, the precise day-count convention, and the fixed-effect estimation sample. Neither income taxes nor course costs should be added and still labeled as the published net-profit measure; they belong in a separately labeled extension.

There is no reported randomized training intervention, volume-normalized learning test, or counterfactual employment model. The paper discusses competition from high-frequency trading as a possible explanation, but does not identify that mechanism causally. Its strongest result is the unfavorable realized distribution of after-fee dollar income among persistent retail entrants. A practical evaluation of day trading should start with that distribution and its income volatility rather than treat a handful of positive averages as a generally attainable salary.
