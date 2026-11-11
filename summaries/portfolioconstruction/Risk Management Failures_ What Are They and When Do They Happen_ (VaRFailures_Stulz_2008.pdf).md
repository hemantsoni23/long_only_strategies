# Risk Management Failures: What Are They and When Do They Happen?

**René M. Stulz (2008).** *Journal of Applied Corporate Finance* 20(4), Fall, pp. 39–48. Source: [VaRFailures_Stulz_2008.pdf](../../Finance/VaRFailures_Stulz_2008.pdf). Page references below are printed journal pages; PDF pages 1–10 correspond to pp. 39–48.

## Why this matters

A loss is an outcome; a risk-management failure concerns the information and controls used to choose an exposure. Confusing the two encourages organizations to eliminate attractive risks after bad outcomes while leaving defective measurement processes undiagnosed after good outcomes. Stulz develops a taxonomy for separating these questions, using LTCM and the unfolding 2007–2008 crisis as illustrations.

The paper's contribution is conceptual and organizational. It does not estimate a new statistical model, assemble a controlled sample of failed institutions, or test a trading strategy. Its numerical distributions are thought experiments. Their purpose is to expose identification problems: a single realized loss cannot establish whether the probability, severity, tolerance, communication, or control of that loss was wrong. The practical implication is to evaluate risk management using evidence available before the event, together with the institution's actual capacity to survive adverse scenarios.

## The decision being evaluated

Management and the board choose the firm's risk appetite and strategy. Risk management identifies and measures exposures, communicates their consequences, and helps keep actual exposures consistent with those choices. An accurate model cannot determine the right risk appetite without a corporate objective. Conversely, executives cannot make an informed choice if important risks are omitted or the model's limitations are concealed.

The relevant distinction is between a bad draw from an understood distribution and a flawed understanding of that distribution. This is not a claim that managers can defend every loss by calling it bad luck. Evidence about the original estimates, omitted positions, rejected warnings, feasible hedges, and incentives remains relevant. It is a claim that loss size alone does not identify the failure.

The distinction also applies to capital structure. A firm facing an attractive investment can reduce leverage to preserve its rating, retain leverage and accept a lower rating, or decline the investment. Holding both leverage and rating fixed can forgo value. Whether a decision is sensible depends on the investment opportunity, financial distress costs, and the owners' objectives, not merely on whether its realized outcome later looks favorable (pp. 40–41).

## LTCM: facts and deliberately hypothetical distributions

The paper reports investor returns of 20% for the ten months of 1994, 43% in 1995, 41% in 1996, and 17% in 1997. Before the collapse, LTCM had approximately \$5 billion of capital, assets exceeding \$100 billion, and derivatives with notional principal exceeding \$1 trillion. Notional principal is an exposure descriptor, not a loss estimate or an amount that should simply be added to assets. By mid-September 1998 it had lost more than \$3.5 billion; a private rescue coordinated by the Federal Reserve Bank of New York injected \$3.65 billion (p. 39).

Stulz asks readers to imagine the following annual return distribution, rather than asserting that it was LTCM's true distribution:

$$
R=\begin{cases}0.25,&\text{with probability }0.99,\\-0.70,&\text{with probability }0.01.\end{cases}
$$

Its arithmetic expected return is

$$
E[R]=0.99(0.25)+0.01(-0.70)=0.2405.
$$

An investor who understood and accepted this risk might rationally choose it. A realized 70% loss would not by itself demonstrate that the estimated probability was wrong. The paper's discussion of 99 good years in a century describes an expected count, not a guarantee about any particular century. Nor does a high arithmetic expectation establish suitability for every investor, acceptable drawdown risk, or an optimal leverage policy.

Now suppose the loss probability was actually 25%, while management believed it was 1%. The same realized loss is consistent with the alternative distribution, but its expected return becomes

$$
0.75(0.25)+0.25(-0.70)=0.0125.
$$

The difference between 24.05% and 1.25% is economically decisive even though one observed crash cannot distinguish the two models reliably. Additional information about positions and the original probability assessment is needed.

A third example has a 90% chance of gaining 25%, a 1% chance of losing 70%, and a 9% chance of losing everything. Its arithmetic expectation is still positive, 12.8%. Yet the omitted 9% ruin probability could make the exposure unacceptable. A model can therefore mislead through the distribution's shape and support, not only through an inaccurate variance.

The actual leverage decision illustrates the separation between objectives and measurement. At year-end 1997 LTCM had \$7.4 billion of capital and returned 36% to investors. Retaining its trades with less equity increased leverage. Whether this was a positive-value decision depends on the risks and rewards understood at that time; the later loss does not settle the question. Stulz also notes that LTCM's partners had almost \$2 billion invested at the beginning of 1998. Large managerial equity stakes did not prevent failure, so a simple assertion that equity ownership necessarily solves incentives is inadequate (p. 41).

## Five distinct failures

| Failure | What goes wrong | Evidence needed to diagnose it |
|---|---|---|
| Inappropriate metric | A correctly calculated number answers the wrong business question. | The decision horizon, survival constraint, and information absent from the selected measure. |
| Mismeasurement of known risks | Probabilities, severities, dependence, or the model family are wrong. | Original estimates, assumptions, data, and evidence about the alternative distribution. |
| Known risks excluded | Material positions or business exposures never enter the central assessment. | Position inventories, reconciliation, new-product coverage, counterparty and business-risk mappings. |
| Communication failure | Relevant information does not reach decision makers in usable form. | Reports, timestamps, audiences, escalation records, and demonstrated understanding. |
| Monitoring or management failure | Actual exposures diverge from intended exposures or hedges cease to work. | Intraday sensitivities, limits, position changes, market states, hedging actions, and contingency plans. |

This table organizes the author's taxonomy into diagnostic questions; it is not a classification fitted to a dataset. Several categories can occur together. A missing position can produce a bad aggregate estimate and also prevent effective escalation.

## Why VaR can be correct and insufficient

For a loss random variable $L$ and confidence level $\alpha$, a conventional definition is

$$
\operatorname{VaR}_{\alpha}(L)=\inf\{\ell:P(L\leq\ell)\geq\alpha\}.
$$

VaR summarizes a quantile, not the conditional average or maximum loss beyond that quantile. A one-day 99% VaR of \$150 million is ordinarily interpreted as a threshold exceeded on approximately 1% of days under the fitted model. It says little about whether those exceedances are \$151 million or several billion dollars. In discrete distributions, exact exceedance probabilities depend on the quantile convention and probability mass at the threshold.

The paper gives a firm with a one-day 1% tail threshold of \$100 million that loses \$10 billion once in 100 trading days (p. 42). The exceedance frequency can look compatible with the forecast even though the severity is devastating. The defensible lesson is about the limits of frequency-based validation. The statement should not be enlarged into a claim that every statistical backtest would approve such a sequence: tests can examine dependence, loss magnitudes, additional distributional forecasts, and information beyond the binary exceedance indicator. Nor does one exceedance in 100 observations establish calibration with useful precision.

UBS reportedly had no daily VaR exceedances in 2006 and 29 in 2007. That contrast can indicate a changed environment or poor adaptation; it does not independently identify the firm's net annual profit, capital adequacy, or ultimate survival. Many moderate exceedances can coexist with gains elsewhere, whereas one extreme loss can threaten the firm.

For LTCM the paper reports eight losing months from March 1994 through December 1997, a worst monthly return of −2.9%, and 37 gaining months. Such a history provides little direct evidence about a rare catastrophic loss. A model can fit ordinary monthly outcomes and still miss a tail that matters to solvency.

There is also a technical boundary in the earlier two-point thought experiment. Stulz describes the annual 99% VaR using the −70% outcome. Under the infimum definition above, a loss distribution placing exactly 99% probability at −25% and 1% at +70% has a 99% loss quantile of −25%, not +70%. The source's intended point is the existence of a 1% annual catastrophic tail; its specific quantile wording depends on convention. The scenario argument does not require that ambiguous boundary claim.

Finally, measurement and action horizons differ. A one-day mark-to-market loss remains mathematically well defined when an asset becomes illiquid, but it is an incomplete measure of the risk borne by a firm forced to retain the asset for weeks or months. Repeated losses, funding needs, and inability to hedge must enter the survival assessment. Extending a daily VaR mechanically by a square-root-of-time rule is not proposed or justified by this paper.

## Estimation error, omitted exposures, and unknown events

Mismeasurement includes the wrong loss probability, the wrong severity conditional on a loss, and the wrong joint distribution. Accurate marginal models do not ensure an accurate portfolio model. Dependence among economically similar exposures can change precisely when capital is scarce. For portfolios with shorts or hedges, a rise in every correlation need not universally increase risk; the economically relevant issue is dependence among the positions' losses and the reliability of the hedging relationships.

Historical estimation is more credible with abundant observations from a reasonably stable process. New products, rare crises, and changes in market structure weaken that basis. The paper argues for judgment about these limitations, rather than a false precision generated by a sophisticated model. It does not supply a numerical correction for parameter uncertainty or a statistical rule for declaring a structural break.

Known but excluded risks are a different problem (p. 44). Decentralized systems can leave an entire trading group outside central aggregation. The Union Bank of Switzerland example describes management choosing not to disrupt a successful equity-derivatives group's incompatible systems, followed by a large loss. This is an illustration based on a cited account, not a controlled causal estimate of the computer decision's effect.

Payoff incentives make omissions consequential. A trader paid a share of gains without reimbursing losses has an option-like compensation structure. If controls measure only certain risks, taking unmeasured risks can improve the trader's expected compensation. Newly introduced instruments are especially vulnerable when trading begins before the risk model incorporates them. Banning such trading also has an opportunity cost, so complete coverage and innovation are not costless substitutes.

Regulatory or accounting silos can obscure economic links. A credit-default swap in a trading book combines market exposure with the protection seller's ability to pay. A securitization business can lose fee income, suffer markdowns on retained securities, and lose its ability to distribute new loans at the same time. These are business, market, and credit losses with common drivers; putting them in separate reporting categories does not diversify them.

Unknown causes need not imply unknown aggregate risk. If a well-specified return distribution already captures an ordinary adverse realization, failure to name the particular factory fire causing it need not invalidate the model. The more serious unknown is an event whose possibility would have changed the decision. Scenario analysis should search for such possibilities, while acknowledging that some contingencies cannot be enumerated. The paper suggests capital for residual uncertainty but does not prescribe an amount or an optimization rule.

## Communication, changing exposures, and endogenous crises

Complex, outdated, or misdirected reports can defeat an otherwise good measurement system. Stulz cites UBS's own report on unsuccessful communication of subprime exposures and a supervisory report describing hierarchy as a filter that delayed or distorted information. The proposed standard is usable and timely information reaching the people empowered to act. A black-box system can produce excessive confidence or excessive distrust; technical sophistication alone does not distinguish the two (p. 45).

Monitoring must also follow changes in the exposure function. A derivatives position can change risk without a new trade: a small move in a state variable can substantially alter its sensitivity, possibly reversing its sign. A hedge appropriate at the opening can then amplify exposure later in the day. The paper does not give a specific derivative payoff or calibrated hedge-frequency model, so its example cannot determine an optimal rehedging interval.

Figure 1, p. 46, plots four AAA ABX vintages, 2006-1 through 2007-2, from January 2006 into 2008. Prices are initially close to 100 and then diverge and fall markedly during the second half of 2007 and 2008. The figure illustrates how a short calm history can fail to reveal a later change in risk. The chart provides no downloadable series, estimator, or identification strategy, and is not evidence that all AAA securities shared identical loss distributions.

Contingency plans matter because normal hedging options can disappear when liquidity dries up. For a large institution, liquidation and public information about capital can also affect prices. Stulz describes feedback through markdowns, capital constraints, forced sales, other institutions' losses, and funding costs. His mark-to-market discussion concerns these possible feedback effects, not a proof that accounting caused the crisis or that suppressing marks eliminates economic losses.

Positions can also become too large to exit at quoted prices. LTCM's short index-option exposures illustrate concentration relative to market capacity. Other traders may anticipate a forced liquidation and trade in ways that worsen the distressed institution's losses. Historical models treating returns as exogenous do not automatically capture such strategic interaction. The article supplies mechanisms and references, not an estimated price-impact function, a market-clearing equilibrium, or a forecast of liquidation costs.

## What can and cannot be reproduced

All three illustrative expected-return calculations can be reconstructed from the stated probabilities. The taxonomy can be applied to a documented incident by recording the contemporaneous model, available information, management's tolerance, actual positions, reporting chain, and feasible responses. Such an application would be an extension of the paper, not a replication of a published empirical test.

The author's recommendations are to supplement short-horizon models with enterprise-wide and longer-horizon assessment; examine the effects of crises on franchise survival; and develop economically informed scenarios with credible response plans. One-year default targets are discussed illustratively: the text mentions 0.03% for some high-rating targets and approximately one in 1,000 for an AA example. These are different examples, not an internally consistent calibration to a single specified rating model.

The paper does not disclose institution-level position data, model parameters, ABX data provenance sufficient for exact chart reconstruction, formal scenario probabilities, liquidity haircuts, counterparty networks, or a cost-benefit model of controls. It cannot support a numerical capital recommendation or a claim that a particular control would certainly have saved LTCM or UBS.

Its enduring result is a disciplined evaluation standard. Ask whether the firm understood the relevant distribution and constraints, knowingly accepted the exposure, received actionable information, and maintained its intended risk position as conditions changed. Then evaluate the loss in that context. This makes both criticism and defense of risk management more demanding than pointing to the realized P&L.
