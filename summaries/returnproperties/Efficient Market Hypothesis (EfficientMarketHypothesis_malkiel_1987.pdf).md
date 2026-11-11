# Efficient Market Hypothesis

Burton G. Malkiel, entry originally published in The New Palgrave: A Dictionary of Economics, first edition, 1987, edited by John Eatwell, Murray Milgate, and Peter Newman. Supplied reprint DOI 10.1057/978-1-349-95121-5_42-1. Source: [EfficientMarketHypothesis_malkiel_1987.pdf](../../Finance/EfficientMarketHypothesis_malkiel_1987.pdf), seven pages. This is a historical literature synthesis, not a new empirical test or a statement about the evidence available today.

## Why this matters

The entry separates informational efficiency from a literal independent, identically distributed random-walk model. It also explains why an abnormal-return test jointly evaluates efficiency and the asset-pricing model used to define normal returns. These distinctions help prevent a statistically predictable return pattern from being mistaken automatically for a feasible economic profit, or a failed CAPM adjustment from being interpreted automatically as informational mispricing.

Malkiel's position is broadly favorable to efficiency while acknowledging anomalies, private-information profits, and episodes of speculative excess. The contribution is an organizing account of the research literature as of 1987. The source contains no newly estimated coefficient table, original sample construction, or complete experimental code that could be recreated from these pages.

## Information sets and the economic claim

A market is efficient with respect to an information set when publicly revealing that information would not change security prices. The corresponding trading claim is that using that set cannot generate abnormal economic profit. Information-set qualification is essential: an argument about historical prices differs from one about all public disclosures or privately held information.

Weak-form efficiency concerns past prices. Semi-strong efficiency expands the set to all publicly available relevant information, including accounting reports and announcements. Strong-form efficiency includes information held privately by any participant. The entry explicitly says the strongest form is refuted by evidence that insiders can profit before announcements. It therefore does not maintain that all three versions are equally supported.

Economic profit must account for risk, execution and information costs. The entry discusses professional management results after fees, and the possibility that costly research earns positive gross returns but no excess net return. Its cited Grossman–Stiglitz argument supplies a reason that complete costless revelation is not an adequate model of incentives to acquire information. The entry summarizes that result; it does not derive its equilibrium or estimate information costs.

A schematic empirical decomposition, included here to clarify the joint test, is

$
R_{i,t}-R_{f,t}=\alpha_i+\beta_i^\top F_t+\epsilon_{i,t}.
$

A nonzero estimated $\alpha_i$ can reflect an incomplete benchmark $F_t$, measurement problems, sampling or selection, as well as mispricing. This equation is explanatory notation, not a regression newly fitted by Malkiel in the entry. The economic opportunity also depends on whether the information and execution prices were available before the return occurred.

## Random walk versus weak efficiency

The strict random-walk model described in the entry assumes serially independent returns with distributions constant through time. Historical studies found small successive-return correlations, and tests of runs, spectral patterns, and filter trading rules generally failed to deliver dependable abnormal profits after costs. The entry cites Bachelier, Working, Cowles and Jones, Kendall, Roberts, Osborne, Fama, Fama and Blume, and Solnik as parts of that evidence.

Uncorrelated returns are weaker than independent returns. Predictable conditional variance can coexist with little predictable conditional mean. The entry acknowledges variance predictability, slight persistence in daily runs, and changing return distributions, concluding that a strict statistical random walk does not hold literally. Its language about news-driven random price changes is an intuition for rapid incorporation of information, not a proof that every efficient asset return must be iid.

For illustration, a process with $E[\epsilon_{t+1}\mid\mathcal I_t]=0$ can still have $E[\epsilon_{t+1}^2\mid\mathcal I_t]$ varying with recent conditions. Neither a variance forecast nor a tiny positive serial correlation proves an after-cost abnormal trading profit. Appropriate risk compensation and feasible execution remain part of the economic claim. This distinction is the substantive point of the entry's discussion of departures from a pure random walk.

The entry discusses January and weekend effects, especially high early-January returns for small firms and negative Friday-close-to-Monday-close average returns. Malkiel argues that many detected effects are small relative to the costs faced by ordinary investors. This is his historical assessment, not a cost model newly estimated here, and it should not be generalized to every later calendar strategy or market.

## Public-announcement evidence and event timing

Semi-strong tests examine how prices adjust to public news. The cited split study associates splits with information about subsequent dividends. Returns before an announcement are not themselves profits available to a trader who first learns the news at the announcement. The relevant inefficiency test concerns abnormal returns after the information becomes available, using an economically defensible benchmark and feasible trading prices.

The entry reports that merger news is rapidly reflected in prices. It also contrasts block-trade studies: one finds permanent price changes consistent with information release, while another using intraday data finds reversals within approximately 15 minutes. That figure is a reported feature of the cited literature, not an event window estimated in this entry. The execution speed and costs of an attempted reversal trade would matter to economic exploitability.

Post-earnings-announcement drift is recognized as contrary evidence. The entry describes a debate over whether incomplete price reactions instead reflect CAPM risk-adjustment errors and notes that subsequent studies retained abnormal returns after proposed corrections. It also discusses exchange price limits in orange-juice futures, where restrictions could prevent immediate information incorporation. These cases qualify the broad claim of rapid adjustment rather than disappear from the review.

No event lists, announcement timestamps, estimation windows, return databases, or cross-event covariance treatment are supplied here. Reproducing those results requires the cited original studies. A researcher should not invent a single standardized event-study protocol and attribute it to all the summarized papers.

## Professional performance and the strong form

Insider evidence is the direct counterexample to strong-form efficiency. Professional-management studies address a related but distinct question: whether typical managers deliver excess net performance. The entry reviews Cowles, mutual-fund evidence, and Jensen's CAPM-based evaluation, concluding that fees often absorb a gross advantage and that exceptional performance shows little persistence.

It reports that about two thirds of US professional pension-fund managers underperformed the unmanaged S&P 500 over the twenty years ending in 1984. The excerpt does not identify all managers, survivorship treatment, portfolio-risk matching, or fee conventions behind that statistic. It is a literature-summary number, not enough information for an independent manager-level audit. Average underperformance also does not logically exclude rare skill, which Malkiel explicitly allows.

The distinction between gross and net skill is particularly useful. An informed manager can earn compensation for information acquisition without providing a free excess return to a fee-paying client. Conversely, an apparent high return without appropriate risk and cost adjustment cannot establish skill. The entry's use of professional evidence is therefore an argument about the difficulty of earning economic profits, not proof that private information never matters.

## Anomalies and the joint-hypothesis problem

The entry discusses value measured by low price–earnings multiples, small-firm returns, excess aggregate price volatility relative to dividends, and discounts on closed-end funds. For size and value, abnormal returns depend on the risk model. For volatility bounds, conclusions depend on the dividend and discounting process. Malkiel contrasts Shiller's rejection with alternative dividend-model arguments by Marsh and Merton and by Kleidon.

This is not a claim that any anomaly can be dismissed without testing. It explains why the test must state its maintained model. A return spread, a price-volatility inequality, and a profitable trading rule are different objects. One cannot move from one to another without assumptions about the cash-flow process, required returns, or trade feasibility.

The closed-end-fund example illustrates another issue: a pattern can persist historically yet diminish when investors recognize and trade it. Malkiel says discounts were eventually largely eliminated in the episode he discusses. No numerical discount series or convergence timetable is provided here, and this 1987 observation should not be presented as a fact about all subsequent funds. Temporary fads can exist in his account even while competition limits durable exploitability.

## How to use this source in research

The entry supports a disciplined test design: specify the information set, the date it is observable, the normal-return model, costs and constraints, and the distinction between discovery and validation. Then test whether the claimed residual opportunity persists under reasonable alternative benchmarks. Those are methodological implications of the review, not an experimental protocol or a new theorem supplied by the author.

Because this source is an encyclopedia entry, its appropriate reproduction target is conceptual: accurately distinguish the three information sets, the stronger iid hypothesis, the role of costs and private information, and the joint test. Numerical replication of its cited findings belongs to the underlying papers. The key takeaway is that efficiency is an economically qualified proposition about information and attainable abnormal profit, while literal randomness and uniformly correct prices are stronger claims that the entry itself does not require.
