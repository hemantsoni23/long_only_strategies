# A Backtesting Protocol in the Era of Machine Learning

Rob Arnott, Campbell R. Harvey, and Harry Markowitz. Working-paper version dated October 29, 2018; SSRN identifier 3275654 appears in the supplied PDF. Source: [Backtesting_ArnottCampbellMarkowitz.pdf](../../Finance/Backtesting_ArnottCampbellMarkowitz.pdf), eighteen pages. All pages, references, the ticker-strategy chart, and the complete seven-category protocol were inspected. This note summarizes the supplied working-paper version without assuming later revisions.

## Why this matters

An attractive investment backtest is the output of a research process, not an isolated statistical observation. That process may include hundreds of abandoned signals, transformations, sample changes, hyperparameter searches, and repeated inspections of supposed holdout data. If only the successful endpoint is reported, ordinary significance tests do not describe the selection that produced it. Machine learning increases the number and flexibility of these choices, while the number of independent financial histories remains limited.

The paper's contribution is a structured protocol intended to reduce false and exaggerated discoveries across the full research process. Its seven categories cover motivation, multiple testing, data, validation, model dynamics, complexity, and organizational incentives. It is a methodological argument with illustrative empirical evidence, not a new estimator, theorem, or randomized evaluation of research teams. Reimplementing this work means making the proposed controls operational and auditable; it does not mean reconstructing a proprietary alpha model.

The authors seek a balance between accepting false strategies and missing useful ones. Rejecting every model would eliminate false positives but defeat the purpose of research. They do not derive an optimal significance threshold or a decision-theoretic solution to that tradeoff. The protocol is meant to improve the credibility of evidence, not certify a strategy as true.

## Demonstration: a convincing strategy built from ticker letters

Exhibit 1 presents a long-short NYSE-stock strategy over January 1963–December 2015. The paper describes 1963–1988 as the development period and 1989–2015 as a subsequent validation period, with stronger performance in the latter. The chart uses monthly cumulative scaled returns on a logarithmic percentage scale, with NBER recessions shaded. A figure note says the strategy return is scaled to match S&P 500 minus Treasury bill volatility over the period.

The apparently attractive properties are nearly 6% annual alpha, substantial statistical significance, no statistically significant correlations with common value, size, momentum, or market factors, less than 10% annual turnover, and a gain of nearly 50% during the financial crisis. These are the authors' approximate descriptive claims; the PDF supplies no complete regression table, exact alpha standard error, precise crisis interval, or detailed transaction-cost calculation supporting them.

The signal is the third letter of a company's ticker. The plotted strategy goes long stocks with S in the third position and short stocks with U there, equally weighting each side. More generally, a rule such as A(1) minus B(1) buys stocks with A as the first ticker letter and shorts those with B. Searching pairs of letters across the first three positions produces thousands of possibilities. The selected S(3) minus U(3) history can pass a simple chronological split despite lacking an economic mechanism.

An explicit reconstruction of a letter strategy at a rebalance date is

$$
r_{a,b,k,t}=\frac{1}{|\mathcal L_{a,k,t}|}\sum_{i\in\mathcal L_{a,k,t}}r_{i,t}
-\frac{1}{|\mathcal S_{b,k,t}|}\sum_{i\in\mathcal S_{b,k,t}}r_{i,t},
$$

where the two sets are eligible NYSE securities whose contemporaneous ticker has letter $a$ or $b$ in position $k$. This formalizes the description; it does not resolve missing implementation inputs. The paper does not disclose the raw security database, ticker-history treatment, short-ticker exclusions, share-class filters, delisting returns, rebalancing calendar, empty-group handling, borrow availability, or leverage normalization. It also does not provide a full search log proving which other models and validation views were inspected before selecting the chart.

For orientation, three positions times $26\times25$ ordered distinct-letter pairs gives 1,950 elementary signed comparisons; treating opposite directions as one unsigned pair gives 975. These are derived counts for a simple search definition, not the authors' reported exact search count. The paper refers more broadly to all potential combinations. The full discovery process may involve additional choices that cannot be inferred from the displayed winner.

The lesson is not that every chronological holdout is useless or that every strategy without an obvious story must be false. It is that a selected narrative and one apparently successful holdout do not identify the probability that the entire research process found a real effect. The example relies on a single realized history, and the displayed risk scaling itself uses a period-level volatility comparison rather than a documented causal trading rule. It is an illustration of selection risk, not a deployable strategy specification.

## Economic motivation as a restriction on search

The first category requires a logical economic hypothesis before estimating the model. It should explain why the predictor might relate to returns and what observations would contradict that mechanism. The authors argue that finance's limited data make theory-guided restrictions particularly valuable. Asking a flexible algorithm to search every field in Compustat and I/B/E/S for a successful long-short portfolio gives it many opportunities to exploit noise.

The distinction is between a hypothesis that constrained the search and an explanation invented after a profitable pattern appeared. If the opposite result could have elicited an equally persuasive story, the story has little evidentiary value. A reproducible record therefore needs a dated hypothesis, expected direction, candidate variables, eligible assets, and planned falsification checks. Those record fields are an operational translation of the recommendation, not a form supplied by the authors.

The paper does not prohibit observation from informing theory in all science. It explicitly recognizes the productive interaction of exploratory data analysis and later theoretical development, including in medicine. Its concern is that finance cannot readily generate a new large independent experiment after exploratory selection. An exploratory finding should remain labeled exploratory until new evidence tests it, rather than be retroactively treated as an ex ante hypothesis.

A second illustration comes from a cited study examining approximately 2.1 million accounting-based strategies. Seventeen survived that study's statistical and economic hurdles. One sorts using long-term debt issuance minus redeemable preferred stock, divided by minimum rental commitments four years ahead. Arnott, Harvey, and Markowitz use the odd construction to question economic interpretation even after formal corrections. They do not reproduce those millions of tests in this paper. Their criticism is about the credibility and interpretability of a mechanism, not a newly estimated failure rate for the seventeen strategies.

## Count the search, including implicit choices

The second category requires tracking successful and unsuccessful models, variables, and combinations. Significance must be judged relative to what could have been selected, including correlations among candidates. Twenty nearly identical return series do not create the same selection opportunity as twenty largely independent series. The paper does not supply a specific multiple-testing estimator or an effective-number-of-tests formula; it points to related methodological work.

Its statement that approximately one of twenty null strategies can cross a two-sigma threshold should be read as a heuristic. For independent standard normal test statistics, the two-sided probability of $|Z|>2$ is about 4.55%, while the one-sided probability of $Z>2$ is about 2.275%. Under those assumptions, the probability of at least one exceedance among twenty tests is respectively

$$
1-(1-0.0455)^{20}\approx0.606,
\qquad
1-(1-0.02275)^{20}\approx0.369.
$$

These are explanatory calculations, not reported empirical estimates. Expected false-positive counts and the probability of at least one discovery are different quantities. Nor is a frequentist tail probability the posterior probability that a discovered investment effect is false. Dependence between tests, nonnormal errors, and adaptive stopping alter the simple calculation.

Interactions expand the search. Twenty original variables permit $\binom{20}{2}=190$ distinct pairwise interactions. The source argues that selecting only two attractive interactions from this menu should not be portrayed as a mere twenty-two-test exercise. The 190 count is the number of possible pairs; including all original main effects would produce 210 candidate features under that simple specification. More complex transformations or models create a still larger search space. Conversely, a genuinely prespecified pair of interactions is not automatically equivalent to an unrestricted search over every pair; the point is to disclose how the pairs were chosen.

The “parallel universe” example addresses implicit selection. A researcher may test one variable and stop at success even though nineteen other plausible variables were waiting in the agenda. A different order could have required twenty attempts to reach the same winner. Reporting only the realized successful test can conceal the selection opportunity. The operational implication is to record the full agenda and stopping rule, not merely files containing completed successful regressions.

## Fix sample and data decisions before viewing success

The third category addresses sample boundaries, data integrity, transformations, outliers, and winsorization. A model that succeeds only after moving its start date from 1960 to 1970 has incurred an additional selection choice. Deleting crisis periods because they hurt the fit is particularly problematic. The paper's wording is deliberately strict about not changing the sample after research begins; an appropriate implementation should preserve the original result and document any later justified revision as a new analysis.

Bad observations can masquerade as nonlinear structure. The authors place cleaning before model development and recommend systematic integrity tools when datasets become too large for manual inspection. They do not specify a data-quality algorithm. For reproduction, the important distinction is between correcting a demonstrably erroneous record and removing a valid observation because the model cannot explain it. Both the raw observation and the correction rationale should remain traceable.

Volatility scaling, standardization, and other transformations are model choices. Searching ten scaling schemes and reporting only the best is another form of parameter selection. The source asks for advance specification and robustness to small changes. It does not prescribe a particular volatility lookback, z-score window, or rank transform; adding one without disclosure would be inventing a method.

Outliers should generally remain unless an economic or data-quality case for exclusion exists independently of their impact on results. Winsorization is a related choice because it changes influential observations without dropping them. The source contrasts a model that works at a 5% tail cutoff but fails at 1%: selecting 5% after observing that difference is a warning sign. There is no universal preferred cutoff in the protocol. The reproducible object is the chosen rule and its timing, together with sensitivity results, rather than a claim that a particular cutoff prevents overfitting.

## Validation must remain separate from development

The fourth category emphasizes that researchers know much of historical market experience before splitting data. They have lived through booms, crises, and policy changes and may select variables because those events are salient. The paper therefore treats actual future live experience as the strongest out-of-sample evidence. This is an epistemic warning about human conditioning, not a theorem that properly controlled historical validation has no value.

Freshly digitized older data and tests in other countries can strengthen evidence but are not fully independent by default. Historical narratives may already inform the hypothesis, and international market correlations can make the same spurious relationship appear across countries during the same episode. The note recommends broadening evidence while retaining these dependence qualifications.

Repeatedly modifying a model after a holdout failure converts that holdout into development data. The authors give a direct example: identify a reason for out-of-sample failure, modify the original specification, and report that it now works in both periods. The second result no longer carries the original holdout interpretation. Preserving a version history and locking a final model before evaluating new data is an implementation of this principle; the paper does not prescribe nested cross-validation, a particular number of folds, or an embargo scheme.

Trading costs and fees belong in both development and validation results. Implementation shortfall can turn a statistically significant gross return into an economically uninteresting outcome. The protocol does not provide spread, market-impact, borrow, financing, turnover, or capacity formulas. A faithful application must choose those assumptions from the actual strategy and disclose them. It cannot mark the cost requirement complete simply because an uncosted gross Sharpe ratio is high.

The ticker example's low stated turnover is thus only one relevant input. It does not establish zero implementation cost, liquid short availability, or frictionless rebalancing. This is especially pertinent because equal-weighted ticker groups can differ in size and liquidity, characteristics not fully documented in the example.

## Model dynamics and endogenous markets

The fifth category concerns structural change, crowding, and live-model revisions. Financial relationships depend on people, institutions, preferences, and competition; they are not immutable physical constants. A strategy may weaken because an underlying mechanism changed or because trading based on the discovery removed the opportunity.

The authors use a physics analogy to describe how researching and exploiting a relation changes its investment relevance. The economic content is endogenous adaptation, not a literal application of the Heisenberg uncertainty principle. They distinguish the gap created by research selection from the additional erosion caused when capital follows a published result.

Dynamic models can respond to changing conditions, but choosing their adaptation speed, regime variables, and recalibration schedules creates more opportunities to fit historical noise. The source offers no preferred change-point test, rolling window, or Bayesian state model. Any such procedure must itself be treated as a selected component of the research design.

Similarly, disappointing live results do not automatically justify a parameter tweak. Backtests are likely to exaggerate performance to some degree, and fitting recent disappointing outcomes may compound the original selection problem. The recommendation is restraint and explicit awareness of that risk, not an assertion that a live model can never be corrected. A documented bug fix, a new economic hypothesis, and an opportunistic fit improvement have different meanings and should not be combined under one unchanged track record.

The paper cites earlier evidence that eight popular factors averaged 5.8% returns before publication and 2.4% afterward, a decline near 60%. These numbers are supporting evidence from another study, not a new estimate in this paper. Post-publication deterioration can reflect selection, arbitrage, structural change, or a combination; the protocol does not identify their separate causal shares.

## Complexity, regularization, and interpretability

The sixth category links model flexibility to the effective amount of evidence. Roughly fifty-five years of monthly history provide fewer than 700 time observations; quarterly macroeconomic histories from around 1960 offer only a little over 200. Cross-sectional stock counts do not turn correlated market histories into independent macroeconomic realizations. This motivates caution about extensive hyperparameter tuning and flexible nonlinear models for low-frequency predictions.

The authors contrast finance with data-rich applications and argue that regularization and structure are necessary. They do not prove that every machine-learning application with a given sample size must fail. The relevant burden is whether the model's flexibility, signal strength, and dependence structure can be supported by available information. High-frequency data can provide more observations, but that is not a universal escape from market dependence or implementation constraints.

The simple illustration is polynomial regression: adding powers of a predictor usually improves in-sample fit, while potentially damaging out-of-sample performance. A more complex method should beat a simpler benchmark by an economically meaningful amount, not merely improve a selected metric marginally. The source gives no numeric switching threshold or specific loss function.

Interpretability is another control. Managers should understand what a system predicts and under what conditions it is likely to fail. The paper refers to interpretable classification and policy-design research, but does not implement those methods. It does not establish that a compelling explanation is sufficient evidence; the earlier warning about after-the-fact stories applies equally to explanations of nonlinear models.

## Research culture and delegated work

The final category treats incentives as part of the statistical process. Rewarding only impressive backtests encourages hidden trials, discarded failures, and motivated reasoning. A sound process rewards question formulation, careful testing, and useful negative results. Management and researchers should expect most experiments to fail to uncover a deployable positive effect.

Delegated analysis creates the same issue at another level. Assistants may search until they find support for a supervisor's hypothesis because that outcome seems desirable. The protocol asks supervisors to make truth-seeking expectations explicit and monitor the work. In operational terms, a delegated result should include attempted specifications, failed checks, data changes, and limitations, not only the best chart. The article provides no controlled study quantifying how much this organizational change improves future returns, so the claim is a reasoned design recommendation rather than an estimated causal effect.

## An auditable implementation of the protocol

The following sequence translates the source's recommendations into research artifacts. It is an implementation proposal consistent with the paper, not an additional validated method:

1. Before testing, record the economic mechanism, competing explanations, universe, sample, data vintage, transformations, portfolio rule, evaluation metric, and planned candidate set.
2. Preserve every attempted specification and outcome, including failed models and changes to samples or preprocessing. Separate planned sensitivity checks from revisions motivated by observed performance.
3. Develop a simple baseline and compare added flexibility under the same data, cost, and validation conventions. Track dependent strategies and interaction searches when interpreting statistical evidence.
4. Freeze the candidate before final validation. Record every access to validation outcomes, and relabel reused periods as development data after a modification.
5. Report gross and net results, exposure and liquidity assumptions, and implementation shortfall. Retain evidence about regimes and adverse episodes rather than deleting them for better fit.
6. In live use, distinguish monitoring from retuning. Treat substantive revisions as new versions requiring new evidence and preserve the original model's realized history.
7. Evaluate researchers and delegated work by the quality and completeness of evidence, including credible rejection of an idea.

The publication does not specify enough detail to reproduce the ticker backtest exactly, does not provide a machine-learning model or hyperparameter grid, and does not supply a formal multiple-testing adjustment. Nor does it empirically compare research organizations that adopt the protocol with those that do not. Its value is the explicit connection between apparently innocuous research choices and the selection of a reported winner. A reproducing team should preserve that connection: the object under scrutiny is the entire discovery process that generated the strategy, rather than the final return series alone.
