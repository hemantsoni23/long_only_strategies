# Thirty Years of Prospect Theory in Economics: A Review and Assessment

Nicholas C. Barberis, *Journal of Economic Perspectives* 27(1), Winter 2013, 173–196, DOI 10.1257/jep.27.1.173. Source: [local PDF](<../../Finance/ProspectTheory_Barberis_2013.pdf>). The file has 25 pages: the article and references occupy the printed 173–196 sequence, followed by a publisher citation page. All pages were inspected. Printed page numbers are used below.

## Why this matters

The paper identifies the main obstacle to using prospect theory in an economic model: laboratory preferences do not determine what an investor, worker, or consumer treats as a gain or loss. The researcher must specify the reference point, the object being evaluated, the horizon, and the treatment of concurrent risks. Those choices are economically substantive. They can change a prediction even when loss aversion and probability-weighting parameters are held fixed.

Barberis's contribution is an assessment and organization of applications, not a new structural estimation or a single new equilibrium model. The review explains how different components of prospect theory generate distinct predictions, where evidence is relatively persuasive, and where common intuitions do not survive formal modeling. For quantitative finance, its most useful distinctions are between preferences for skewness and beliefs about skewness; loss aversion and narrow framing; unrealized gains and realization utility; and an investment outcome's psychological appeal versus its welfare value.

This note reconstructs the mechanisms at the level supported by the review. The article generally does not provide the original studies' full datasets, likelihoods, equilibrium solutions, or standard-error specifications. Reproducing a cited study's coefficients requires that study; inventing a common backtest across the review's examples would misrepresent the source.

## The preference specification and four separate ingredients

The review compares the conventional wealth-based expected-utility evaluation $\sum_i p_iU(W+x_i)$ with cumulative prospect evaluation $\sum_i\pi_i v(x_i)$. Here $W$ is initial wealth, $x_i$ an outcome relative to a reference point, $p_i$ its probability, and $\pi_i$ its rank-dependent decision weight. Outcomes are ordered and zero is included as the reference outcome. The usual increasing, concave wealth utility provides the comparison benchmark; concavity is an additional risk-attitude assumption, not part of the bare expected-utility axioms.

The four ingredients are reference dependence, loss aversion, diminishing sensitivity, and probability weighting. Reference dependence changes the argument of utility from total wealth to an increment relative to a benchmark. Loss aversion makes an equal-sized loss more consequential than a gain. Diminishing sensitivity makes value concave for gains and convex for losses. Probability weighting changes the impact of outcome probabilities, especially at distribution tails.

The illustrative value function is

$$
v(x)=\begin{cases}x^\alpha,&x\ge0,\\-\lambda(-x)^\alpha,&x<0.\end{cases}
$$

The review cites experimental estimates $\alpha=.88$ and $\lambda=2.25$. Figure 1 deliberately uses $\alpha=.5$ and $\lambda=2.5$ to make the curvature and asymmetry easier to see. These plotting values are not the reported experimental calibration. Figure 2 uses

$$
w(p)=\frac{p^\delta}{[p^\delta+(1-p)^\delta]^{1/\delta}},
$$

with $\delta=.65$ for the displayed inverse-S curve and $\delta=1$ for the linear comparison. The review compresses the weighting discussion into a representative function; it is not reporting a new estimate that supersedes the separate gain and loss estimates in the 1992 source.

The weights apply to cumulative tails. For implementation, with increasing positive outcomes, the weight on outcome $i$ is $w(\sum_{j\ge i}p_j)-w(\sum_{j>i}p_j)$; on negative outcomes, it is the increment between the lower-tail cumulative probabilities through $i$ and through the preceding outcome. This is the computational meaning of the review's cumulative-weighting description. Independently substituting $w(p_i)$ for every outcome probability generally implements a different model. A multi-asset application must form the distribution of the chosen evaluation object before calculating ranks and weights.

The important distinction is between a belief and a decision weight. An individual can understand a .001 probability correctly while assigning its extreme payoff disproportionate decision importance. In field data, however, an observed preference for insurance or lottery-like assets may also reflect an incorrect subjective probability. Observed choices alone may not identify which mechanism is responsible.

The numerical examples show what the components are intended to explain. Many people reject an even-probability gamble losing \$100 or gaining \$110, despite its positive mean. Under conventional smooth wealth utility, sustaining that degree of small-stakes aversion can imply implausible aversion at larger scales. Other examples combine willingness to gamble on a .001 chance of winning \$5,000 with willingness to insure against a .001 chance of losing \$5,000. Gonzalez–Wu certainty equivalents cited in the review are \$10 for a .05 chance of \$100 and \$63 for a .9 chance of \$100. These are evidence from earlier studies, not observations collected for this paper.

## Closing an economic model: reference, scope, horizon, and expectations

For a portfolio problem, the review asks whether the investor evaluates total wealth, total stock holdings, or each security separately. It also asks whether the benchmark is zero return, the risk-free return, or expected return, and whether evaluation is weekly, monthly, or annual. These are not interchangeable normalization choices. A security that is a gain relative to purchase price can be a loss relative to an expected or risk-free benchmark.

A useful implementation description is an outcome mapping $x_s(a;r,H,\mathcal F)$, where $a$ denotes the action, $r$ the reference rule, $H$ the horizon, and $\mathcal F$ the grouping of risks into mental accounts. This notation is a reconstruction aid, not an equation printed in the review. Fixing only $v$ and $w$ leaves $x_s$ unspecified and therefore leaves the decision problem incomplete. Endogenous references add a further consistency condition because the action changes the outcome distribution against which it is evaluated.

Kőszegi and Rabin provide the review's leading candidate framework. Individuals compare consumption with expectations held in the recent past. Expectations are initially modeled as rational: they match the distribution of outcomes generated by the optimal plan under those expectations. This is a fixed-point requirement, not permission to choose a convenient reference after observing behavior. The review does not give the full personal-equilibrium definition or algorithm, so a researcher must return to the cited papers to choose among possible equilibrium concepts and resolve multiplicity.

Reference-dependent utility need not replace ordinary utility from consumption levels. The review emphasizes combining the two. A model containing only gains and losses may be a tractable simplification; it does not establish that absolute living standards are irrelevant. Similarly, convexity for losses becomes questionable when additional losses threaten a large fraction of wealth. A small-stakes value function should not automatically be extrapolated to ruin or subsistence without a boundary treatment.

The evidence on experience is mixed. High-stakes game-show and lower-income-country experiments support relevance beyond trivial laboratory stakes. Professional golfers' success probabilities differ for par and non-par putts in a way consistent with a par reference point. Experienced market dealers show weaker endowment effects than novices in some studies. These findings constrain different versions of the theory; they do not support an unrestricted claim that every preference parameter is invariant across populations, experience, incentives, or framing.

## Asset pricing: why positive skewness can lower expected returns

In the Barberis–Huang application summarized on pp. 180–181, investors in a one-period economy apply prospect theory to changes in portfolio value. A sufficiently concentrated holding in a positively skewed stock creates a small probability of a large wealth gain. Tail overweighting makes that opportunity attractive enough to command a higher price and a lower subsequent mean return than in the expected-utility comparison economy. The noteworthy prediction is that even idiosyncratic skewness can be priced, despite being unrelated to market covariance.

This mechanism should not be confused with the conventional claim that all higher moments are priced in every utility model. The review's emphasis is on a specifically strong appetite for lottery-like upside under probability weighting and the resulting willingness to accept low mean returns. A researcher implementing the equilibrium would need the joint payoff distribution, asset supplies, feasible portfolios, and market-clearing conditions, none of which are fully specified in this review. Portfolio-level rank dependence also means one cannot obtain equilibrium prices by applying a fixed scalar discount to each stock's standalone skewness.

The review reports support from studies using several skewness measures and from applications to IPOs, distressed and bankrupt stocks, over-the-counter stocks, and out-of-the-money options. These securities can offer extreme upside despite poor ordinary outcomes. Green and Hwang find that IPOs with higher predicted skewness have lower long-run mean returns. Conglomerate discounts and household underdiversification offer related applications: combining businesses can reduce the lottery-like appeal of a single segment, while concentrated household holdings preserve a chance of an exceptional personal payoff.

The common mechanism is not itself identification. Skewness forecasts can covary with size, distress, liquidity, or other return predictors. The review does not provide common sample dates, sort breakpoints, regression controls, trading lags, or net-of-cost returns for these studies. Its evidence is a narrative synthesis rather than a pooled causal estimate. It also does not claim that a short position in skewed stocks is a free arbitrage; risks and costs of shorting may prevent expected-utility investors from removing the price effect.

## Aggregate equity demand: loss aversion is not enough by itself

Benartzi and Thaler's equity-premium explanation evaluates the historical distribution of stock-market returns over an approximately annual horizon. A loss-averse investor finds the dispersed annual distribution unattractive unless the average equity return is high relative to a safe asset. The annual horizon is motivated by how performance is commonly reported, not estimated here as a universal psychological clock.

The argument also requires narrow framing: the investor evaluates stock-market fluctuations separately from other wealth and background risks. This is a separate assumption from loss aversion. When the small \$110/−\$100 gamble is combined with other concurrent financial or labor-income risks, rather than isolated, loss aversion alone need not generate its rejection at plausible parameter values. The review uses this example to explain why a portfolio model must specify which risks are jointly evaluated.

Probability weighting can reinforce a high aggregate equity premium because the market has a negatively skewed crash tail. This does not conflict with lower mean returns for positively skewed individual stocks: the same preference for tail outcomes can make upside lotteries attractive and downside crashes especially unattractive. The sign of skewness and the object being evaluated are decisive.

Barberis describes the premium explanation as plausible but notes few direct empirical tests. Subsequent work has concentrated on formalizing the mechanism. A related household result is that survey measures of loss aversion predict stock-market participation. That association supports relevance to nonparticipation, but the review does not provide the instrument construction, identification strategy, sample size, or coefficient needed for an exact household-data replication. Its claim is not that loss aversion quantitatively accounts for the entire premium and participation distribution without further assumptions.

## Trading over time: the disposition effect and realization utility

The disposition effect is a greater propensity to sell assets above purchase price than assets below it. The review cites evidence for individual investors and mutual-fund managers, and a related Boston condominium result: conditional on expected selling value, sellers facing a loss relative to purchase price post higher asking prices. Purchase price is therefore a candidate reference point for these settings.

The familiar explanation invokes convexity in the loss region: a holder of a losing asset becomes willing to risk further losses for a chance to break even. The review stresses that this intuitive story is not automatically a valid dynamic prediction. Formal models may require a much more convex loss branch than laboratory estimates suggest. Thus an implementation cannot merely label a losing position as risk seeking and assume that an optimal policy necessarily holds it while selling winners.

A different mechanism is realization utility: utility arrives when an asset is sold and a gain or loss relative to purchase is realized. With a sufficiently positive discount rate, even a linear realization-utility function can produce a strong disposition effect. The timing of utility and the reinvestment opportunity matter, not just curvature over terminal wealth. This distinction provides a concrete test of model architecture: terminal gain/loss utility, utility from periodic mark-to-market changes, and utility from realized sales are different objectives.

The review supplies neither the complete stopping problem nor a calibrated trading policy. To reconstruct a cited realization model, one needs the price process, discounting, transaction constraints and costs, purchase-price resetting rule, and admissible liquidation/reinvestment decisions. Treating the review's qualitative result as a ready-made sell threshold would fabricate missing inputs.

## Insurance: a numerical design that separates plausible mechanisms

Sydnor's home-insurance study covers 50,000 customers offered deductibles of \$100, \$250, \$500, and \$1,000. Customers selecting the \$500 deductible pay an average annual premium of \$715, while the alternative \$1,000 deductible costs \$615. With an annual claim frequency around 5%, they pay an extra \$100 to avoid a 5% chance of paying an additional \$500. The expected incremental payout in the simplified comparison is \$25, so the premium difference is four times that expected amount. This last ratio is arithmetic from the reported figures, not a separately estimated coefficient.

Very strong conventional small-stakes risk aversion would be needed to explain that choice. Overweighting the claim state provides an alternative. But the reference rule affects quantitative fit: if current wealth is the benchmark, prospect theory explains only part of the high premium; if anticipated payments enter the reference point, the predictable premium is less painful than an unexpected deductible. Barseghyan and coauthors' structural insurance work likewise finds a role for inflated weights on claim states.

These findings do not fully distinguish decision weighting from overestimated claim probabilities. An empirical reconstruction would need policy menus, household-specific prices, claims or risk estimates, choice timing, and a specified model of beliefs. The review gives the economically revealing comparison but not all those microdata details. Nor does it demonstrate that the same parameters fit stock demand, insurance, and gambling for the same individuals.

The annuitization application uses another framing choice. An annuity is evaluated as the discounted sum of payments received before death minus the initial premium, making early death a large investment loss and long survival a gain. Loss aversion and overweighting early death can then make the product unattractive. This is an explanation of behavior under an investment frame; it is not a welfare proof that annuities are undesirable. Consumption insurance and bequest objectives would require additional model components.

## Riskless exchange and the interpretation of endowment effects

The review separates exchange asymmetries from willingness-to-accept/willingness-to-pay gaps. Knetsch's experiment gives participants either a mug or candy, then offers exchange after a short unrelated questionnaire. Eighty-nine percent of mug recipients keep the mug, whereas only 10% of candy recipients choose to exchange for a mug. In Kahneman–Knetsch–Thaler Experiment 5, participants with a mug state acceptable sale prices and others state purchase willingness; median willingness to accept is \$5.75 versus willingness to pay of \$2.25.

Loss aversion can explain both because surrendering an endowed object is evaluated as a loss. But the evidence is not uniquely diagnostic. List finds smaller exchange asymmetries among experienced sports-memorabilia dealers. Plott and Zeiler show that instructions and procedures affect these outcomes, raising possible explanations involving misunderstandings, perceived gifts, and beliefs about object value.

An expectations-based reference offers a different interpretation of experience: dealers anticipate exchanging goods and therefore do not experience the same loss when an object leaves their possession. That is a testable alternative, not a reason to treat every reduction in the effect as automatically supportive. The paper describes the debate as unresolved and emphasizes that the term endowment effect names evidence, which must be distinguished from the theory used to explain it.

## Consumption, pricing, labor, and dynamic consistency

In reference-dependent consumption models, utility can respond both to current consumption relative to recent expectations and to news about future consumption relative to earlier plans. Greater sensitivity to current news than to future news creates an incentive to consume extra now, even though it reduces future resources. Loss aversion can simultaneously motivate precautionary saving to avoid painful downward revisions later. The interaction can generate a hump-shaped life-cycle profile and sluggish adjustment to income shocks. The review supplies mechanisms, not a complete calibrated life-cycle solution.

For retail pricing, a monopolist facing expectations-based loss-averse consumers can prefer alternating regular and sale prices. Occasional attractive sales raise the expectation of obtaining the good; leaving without it at a high price then feels like a loss. Under the cited model, average payment can exceed the consumer's ordinary valuation. Reproducing this result requires specifying consumption and money as separate gain/loss dimensions and solving for consistent purchase expectations. It is not implied by a generic utility function over a single net cash payoff.

The taxi-driver example further illustrates identification of references. Early evidence links daily working hours inversely to realized hourly wages and suggests an income target. The expectations-based extension has both income and hours targets, estimated using a driver's previous income and hours by day of week. Crawford and Meng find stopping behavior consistent with reaching the second of the two targets: the income target after unexpectedly weak early earnings, or the hours target after unexpectedly strong earnings. The distinction is between expected wages and surprises within a shift. It does not predict that drivers necessarily work less on days when expected wages are higher; the review notes that intraday wage surprises are not strongly serially correlated.

Finally, probability weighting in sequential gambling can generate time inconsistency: the action selected upon reaching a state differs from the earlier contingent plan for that state. A dynamic implementation must therefore state whether agents can commit, anticipate future preference changes, or repeatedly reoptimize. Applying a static weighted value function inside a standard expected-utility Bellman recursion without examining this issue is not justified by the review.

## Assessment and limits of reproducibility

Barberis regards reference dependence as foundational, loss aversion as useful across many applications, and probability weighting as especially promising in finance, insurance, and gambling. Diminishing sensitivity plays a less clearly established role, including in the disposition-effect debate. These are the author's judgments about the literature available in 2013, not a contemporary meta-analysis or a formal ranking based on common effect sizes.

The review's practical lesson is to expose the evaluation object, reference update, horizon, beliefs, and timing of utility as explicit model inputs. Parameters and restrictions should then be assessed against observations the model was not chosen solely to explain. Applications based on rational expectations about the reference distribution require a consistency solution; dynamic applications require a treatment of changing plans. Those details are what turn a plausible narrative into a model another researcher can implement.

The source provides no new estimation sample, train/test split, optimizer, common control set, transaction-cost study, or pooled uncertainty interval. Its few numerical examples should be retained with their original provenance. It also separates positive prediction from welfare: explaining low annuitization, casino attendance, or willingness to pay for skewness does not by itself establish a mistake. Narrow framing may offer a clearer case for intervention than a general assertion that all reference-dependent preferences are irrational. The lasting contribution is this disciplined separation of psychological ingredients, economic implementation, and empirical claims.
