# Advances in Prospect Theory: Cumulative Representation of Uncertainty

Amos Tversky and Daniel Kahneman, *Journal of Risk and Uncertainty* 5 (1992), 297–323. Source: [complete 27-page local PDF](<../../Finance/Advances in Prospect Theory- Cumulative Representation of Uncertainty.pdf>). Page references below use printed pages; PDF page 1 is printed page 297. The mathematical appendix, experiment tables, and references are included in the inspected source.

## Why this matters

This paper supplies a usable replacement for the original prospect theory's separable probability weights. Its innovation is to weight cumulative events, separately on the gain and loss sides of a reference point. This preserves stochastic dominance while accommodating loss aversion, diminishing sensitivity, overweighting of small probabilities, and different attitudes toward gains and losses. It also extends the model from lotteries with stated probabilities to uncertain acts whose event weights need not be additive probabilities.

For a researcher implementing behavioral preferences, the important object is a ranking of complete outcome distributions. Applying a weight independently to each individual probability is generally a different model. Likewise, moving the reference point, merging identical outcomes, or changing which outcomes count as gains can change the computation. The paper gives a representation theorem, a parsimonious parametric specification, and elicitation evidence. It does not estimate an investment strategy or establish that these preferences maximize long-run wealth.

## Outcomes, reference point, and decision weights

Let a finite state space be $S$, with at least three states for the appendix's characterization. An act $f$ maps each state to a real outcome measured relative to a reference point normalized to zero. Positive and negative parts are $f^+(s)=\max(f(s),0)$ and $f^-(s)=\min(f(s),0)$. The value function $v$ is continuous and strictly increasing, with $v(0)=0$. A capacity $W$ maps events into $[0,1]$, is monotone under inclusion, and satisfies $W(\varnothing)=0$, $W(S)=1$. It need not be additive.

There are two capacities, $W^+$ for gains and $W^-$ for losses. Rank distinct outcomes as $x_{-m}<\cdots<x_{-1}<0<x_1<\cdots<x_n$, allowing a zero-outcome event separately. Let $A_i$ be the event producing $x_i$. For a gain, the decision weight is the difference between weights on two upper-tail events. For a loss, it is the difference between weights on two lower-tail events:

$$
\pi_i^+=W^+\!\left(\bigcup_{j=i}^{n}A_j\right)-W^+\!\left(\bigcup_{j=i+1}^{n}A_j\right),\qquad i>0,
$$

$$
\pi_i^-=W^-\!\left(\bigcup_{j=-m}^{i}A_j\right)-W^-\!\left(\bigcup_{j=-m}^{i-1}A_j\right),\qquad i<0.
$$

The empty union has weight zero. The valuation is

$$
V(f)=\sum_{i=1}^{n}\pi_i^+v(x_i)+\sum_{i=-m}^{-1}\pi_i^-v(x_i).
$$

These are the substantive content of equations (1)–(2), printed pp. 299–301. An outcome's weight depends on its rank and the events beyond it, not just its own event. Equal outcomes should be merged before computing the sums; a split of one outcome into several identical branches must not change its valuation. Decision weights are nonnegative by capacity monotonicity. For a mixed act, the combined weights on nonzero gains and losses need not sum to one; renormalizing them would change the model.

For risky prospects with known probabilities $p_i$, write $W^+(A)=w^+(P(A))$ and $W^-(A)=w^-(P(A))$. Replace each union above by its total probability. This is a restriction of the uncertainty model, not a requirement that every ambiguous event have an agreed objective probability. With nonadditive capacities, knowing weights on single states is insufficient to value arbitrary unions. An implementation under uncertainty therefore needs an explicit event-capacity specification, which the paper does not estimate generally.

The two capacities are consequential. A single standard rank-dependent cumulative representation links positive and negative weighting by $w^-(p)=1-w^+(1-p)$. Cumulative prospect theory relaxes that duality. The experiments find weights below one-half for probability one-half on both sides, inconsistent with imposing that restriction. Conversely, simply using the same probability-weighting function for gains and losses does not recreate the old separable weighting formula: the cumulative increments remain essential.

## A concrete parametric implementation

The experimental specification uses a two-part power value function and a one-parameter probability-weighting family (printed pp. 309–313):

$$
v(x)=\begin{cases}x^\alpha,&x\ge0,\\-\lambda(-x)^\beta,&x<0,\end{cases}
\qquad
w_\eta(p)=\frac{p^\eta}{\left[p^\eta+(1-p)^\eta\right]^{1/\eta}}.
$$

Use $w^+=w_\gamma$ and $w^-=w_\delta$. The reported medians of individually estimated parameters are $\alpha=\beta=0.88$, $\lambda=2.25$, $\gamma=0.61$, and $\delta=0.69$. These are descriptive estimates from 25 participants, not universal constants or portfolio-calibrated coefficients. Fits to median data were essentially similar. No standard errors or complete individual dataset accompany the estimates.

With exponents below one, value is concave over gains and convex over losses. The loss multiplier scales the negative branch; the reference-point kink expresses greater sensitivity to a loss than to a comparable gain. The weighting function's inverse-S shape produces overweighting of sufficiently small probabilities and underweighting of sufficiently large ones. It is not correct to infer risk preference from value curvature alone. Both curvature and cumulative weights determine a lottery's certainty equivalent.

A reproducible valuation routine first fixes a reference level and subtracts it from monetary outcomes. Next, combine equal outcomes and their probabilities, verify nonnegative probabilities summing to one, and sort outcomes. Compute lower-tail probabilities for losses and upper-tail probabilities for gains. Apply the appropriate weighting function before taking adjacent differences. Multiply by outcome values and sum. A sure outcome $c$ has value $v(c)$, so recover its certainty equivalent by the inverse value function:

$$
c=\begin{cases}V(f)^{1/\alpha},&V(f)\ge0,\\-\left[-V(f)/\lambda\right]^{1/\beta},&V(f)<0.\end{cases}
$$

This inversion holds for the stated normalized sure-outcome representation. It is not a mean of separately transformed statewise certainty equivalents. Basic numerical checks include a sure gain and a sure loss returning themselves, zero returning zero, invariance to splitting an identical-outcome branch, and dominance preservation for correctly ordered distributions. These are implementation implications of the model, rather than tests reported by the authors.

For a mixed two-outcome gamble paying $G>0$ with probability $p$ and $-L$ otherwise, acceptance against zero requires

$$
w^+(p)G^\alpha\ge\lambda w^-(1-p)L^\beta.
$$

If $\alpha=\beta$, the break-even gain/loss ratio is $[\lambda w^-(1-p)/w^+(p)]^{1/\alpha}$. Thus the minimum gain demanded for a fair mixed gamble does not equal $\lambda$ mechanically. Different weights and curvature matter. Taking a median observed compensation ratio and calling it a direct estimate of loss aversion would omit those components.

There is also a scope qualification to the paper's homogeneity discussion. Pure-gain and pure-loss certainty equivalents can each be proportional to stakes with different power exponents. Global proportionality for mixed gambles with fixed weights and fixed $\lambda$ requires equal exponents: scaling a zero-value mixed gamble by $k$ multiplies its gain term by $k^\alpha$ and its loss term by $k^\beta$. The zero generally disappears if $\alpha\ne\beta$. This is a derived qualification; the reported median exponents happen to satisfy equality.

## Common-consequence evidence under uncertainty

Before the main elicitation exercise, the paper presents two demonstrations that do not require objective event probabilities. Table 1 uses 156 money managers attending a workshop. Events partition the next day's Dow Jones change into $A:d<30$, $B:30\le d\le35$, and $C:d>35$. One choice is between the sure vector $(25000,25000,25000)$ and $(25000,0,75000)$; 68% choose the sure amount. A second choice replaces the common outcome on $A$ by zero: $(0,25000,25000)$ versus $(0,0,75000)$; 77% choose the latter. Fifty-three percent exhibit the particular paired reversal. Amounts are dollars and choices hypothetical; the workshop illustration is not a trading experiment.

Table 2 uses 98 Stanford students and events defined by the outcome margin of a football game, with table partitions $d<0$, $0\le d\le10$, and $d>10$. The first pair is $(10,10,10)$ against $(10,30,0)$; 64% select the former. The second pair is $(0,10,10)$ against $(0,30,0)$; 66% select the latter. Forty-six percent make the paired reversal. Ten percent of participants are randomly selected for payment based on a choice. This payment procedure is separate from the main experiment described below.

The logic is that changing a common consequence should not reverse preferences under the relevant independence requirement, whatever probabilities the individual assigns to the events. Cumulative capacities can make an event's marginal impact depend on the other events accompanying it. Equation (3) formalizes the required inequality of capacity increments. These demonstrations support a departure from additive expected utility, but do not identify a unique weighting function, individual event beliefs, or every parameter of the final model. The Dow choices are presented in the reported order; the source does not establish randomized order as an experimental control.

## Main elicitation experiment: design and complete lottery grid

The primary sample comprises 25 graduate students from Berkeley and Stanford, 12 men and 13 women, without special training in decision theory. Each attends three approximately one-hour sessions several days apart and receives a flat total participation payment of \$25. Lottery choices are hypothetical; there is no choice-contingent payoff in this main exercise. The study therefore estimates expressed choices under its procedure rather than incentives from a portfolio or market setting.

For each two-outcome prospect, a computer displays the prospect and its expected value alongside seven sure amounts. The first seven amounts are described as logarithmically spaced between outcome endpoints. Participants choose between the prospect and each sure amount. A second set of seven amounts is linearly spaced over a narrowed range, described as from 25% above the lowest amount accepted to 25% below the highest amount rejected. The certainty equivalent is the midpoint of the final acceptance/rejection bracket. Inconsistent response patterns prompt repetition.

The source does not supply the original executable, all interface instructions, the transformation used for logarithmic spacing when endpoints include zero or negative numbers, or the precise signed-amount implementation of the percentage expansion. These omissions matter for an exact recreation of the adaptive elicitation. One can reproduce the economic design and target lotteries, but should document any newly chosen grid convention instead of presenting it as the authors' software. A footnote says an IBM disk with instructions and procedures could be obtained from the authors; it is not part of this PDF.

There are 28 positive and 28 corresponding negative prospects, six repeated prospects across sessions, and eight mixed or tradeoff problems. Table 3's complete median certainty-equivalent grid is below. In each row, $p$ is the probability of the larger absolute outcome: for the positive prospect $(a,b)$ it is the probability of $b$, and for its negative counterpart it is the probability of $-b$. Values and certainty equivalents are dollars, with negative signs indicating losses.

| Positive endpoints $(a,b)$ | Ordered probabilities $p$ | Median gain CE, same order | Median loss CE, same order |
|---|---|---|---|
| $(0,50)$ | .10, .50, .90 | 9, 21, 37 | −8, −21, −39 |
| $(0,100)$ | .05, .25, .50, .75, .95 | 14, 25, 36, 52, 78 | −8, −23.5, −42, −63, −84 |
| $(0,200)$ | .01, .10, .50, .90, .99 | 10, 20, 76, 131, 188 | −3, −23, −89, −155, −190 |
| $(0,400)$ | .01, .99 | 12, 377 | −14, −380 |
| $(50,100)$ | .10, .50, .90 | 59, 71, 83 | −59, −71, −85 |
| $(50,150)$ | .05, .25, .50, .75, .95 | 64, 72.5, 86, 102, 128 | −60, −71, −92, −113, −132 |
| $(100,200)$ | .05, .25, .50, .75, .95 | 118, 130, 141, 162, 178 | −112, −121, −142, −158, −179 |

The two-stage brackets make these estimated indifference values, not direct bids with unlimited numerical precision. Across signs, comparing a CE with its expected value determines the observed risk attitude: a CE above expected value indicates seeking, including when both are negative. A loss CE closer to zero than its expected loss therefore indicates risk seeking, not aversion.

## Fourfold pattern, reliability, and loss compensation

Table 4 divides prospects into low probability, $p\le.10$, and moderate/high probability, $p\ge.50$. For low-probability gains, 78% of responses are risk seeking, 12% neutral, and 10% averse. For moderate/high-probability gains the percentages are 10%, 2%, and 88%. For low-probability losses they are 20%, 0%, and 80%; for moderate/high-probability losses, 87%, 7%, and 6%. Those percentages refer to the aggregate classification reported in the table. Individual rows omit neutral choices in their comparison; the aggregate row includes them, so the denominators should not be conflated.

Every participant predominantly shows aversion for high-probability gains and seeking for high-probability losses; 22 of 25 show the complete fourfold pattern. This is more specific than a single claim that people are risk averse or prefer lotteries. The estimated weighting and value functions explain why the direction reverses with both sign and probability. Nonetheless, the pattern is not a deterministic description of every choice or a claim of exact reflection symmetry for every gain/loss pair.

Repeated-choice reliability is limited. The average cross-subject correlation for the six repeated prospects is .55. Average within-category association is .41; the four category diagonals in Table 5 are .41, .39, .40, and .44. Between-category correlations are much weaker and sometimes negative. The table's distinct off-diagonal entries are .17, −.23, .05, .05, −.18, and .06 in the reported category ordering. Seventy-eight percent of 403 cross-sign correlations are negative. A single stable risk-aversion coefficient would fail to describe this structure, but the noise also cautions against treating every estimated individual parameter difference as durable heterogeneity.

Table 6 elicits an $x$ making equal-probability prospects $(a,b)$ and $(c,x)$ indifferent. Its median solutions and reported compensation ratios are:

| $a$ | $b$ | $c$ | Median $x$ | Positive compensation ratio |
|---:|---:|---:|---:|---:|
| 0 | 0 | −25 | 61 | 2.44 |
| 0 | 0 | −50 | 101 | 2.02 |
| 0 | 0 | −100 | 202 | 2.02 |
| 0 | 0 | −150 | 280 | 1.87 |
| −20 | 50 | −50 | 112 | 2.07 |
| −50 | 150 | −125 | 301 | 2.01 |
| 50 | 120 | 20 | 149 | .97 |
| 100 | 300 | 25 | 401 | 1.35 |

There is a printed sign defect worth correcting for replication: the Table 6 caption gives $(x-b)/(c-a)$, which would be negative for these rows. The positive ratios shown in the table are $(x-b)/(a-c)$. This arithmetic correction does not alter the observations. The last two rows translate earlier mixed prospects into gains, and their compensation ratios fall substantially. Thus a gain-domain curvature argument alone does not account for the mixed-domain tradeoffs; the reference point changes the valuation.

The estimation uses nonlinear regression separately for each participant. The paper does not report a complete fitting objective, observation weights, parameter bounds, initialization, numerical optimizer, or uncertainty estimates. Accordingly, a reconstruction can fit the listed median CEs or available individual data under an explicitly chosen loss function, but cannot claim to reproduce the original optimization exactly. A recommended implementation should compare predicted and observed CEs across the full grid rather than fitting only fair binary gambles, which would confound weighting and loss sensitivity. This recommendation is a methodological inference from the identification structure.

## What the representation theorems establish

The appendix (printed pp. 318–321) assumes a continuous, complete, transitive, strictly statewise monotone preference on finite-state real-valued acts. Two acts are comonotonic when they have no states ranked in opposite order. Restricted independence within a common ranking is weaker than unrestricted independence: the model need not preserve an ordering when a change moves an outcome across ranks or signs.

Theorem 1 starts with cumulative representations on the nonnegative and nonpositive domains. It extends them to the full cumulative prospect representation exactly when preferences satisfy comonotonic independence and double matching. Double matching says that if $f^+\sim g^+$ and $f^-\sim g^-$, then $f\sim g$. The condition lets the two parts be joined consistently. It does not say gains and losses have identical value scales.

The proof first constructs additive representations within each comonotonic set. Positive and negative domain representations identify their scales there. Double matching aligns the relative scales across ranking regions. Certainty equivalents then connect comparisons across different regions, yielding the global sum of gain and loss evaluations. The proof's substantive role is to show consistency of this construction rather than just propose a convenient numerical formula.

Theorem 2 distinguishes tradeoff consistency, comonotonic tradeoff consistency, and sign-comonotonic tradeoff consistency. The first supports expected utility; the second supports a single cumulative utility representation. Restricting consistent tradeoffs to comonotonic acts whose compared consequences have a common sign, together with double matching, gives cumulative prospect theory. The necessity argument cancels common decision weights to compare value intervals; a contradictory interval ordering would violate the axiom. For sufficiency, sign-restricted consistency yields the two domain representations and the conditions needed for Theorem 1.

These theorems do not derive the power exponents, inverse-S shape, or numerical loss multiplier. Those are additional behavioral specifications supported by the experiments. Nor do they formalize how a person chooses a reference point or frames a problem. A computer implementation that supplies its own dynamic reference rule adds a model component beyond this source.

## Boundaries and practical takeaways

Cumulative weighting resolves the original separable formulation's dominance problem, but that consistency also limits what it explains: observed choices violating dominance in complicated presentations require framing, editing, noise, or another mechanism. The model is a representation of preferences over outcomes; it is not a general account of information acquisition, belief updating, or learning.

The empirical support is a small, educated convenience sample with hypothetical main-task choices, limited retest reliability, and incomplete original software. The illustrations involving professionals and incentivized students are separate designs and should not be pooled into the 25-person parameter fit. External high-stakes experiments discussed in the paper are supporting literature rather than additional data generated here.

For reproduction, retain the full lottery grid, distinguish sign-specific cumulative weights from branch weights, keep reference-point choices explicit, and expose the estimation choices absent from the paper. For interpretation, the central result is a coherent combination of rank dependence and gain/loss asymmetry. Importing the five median parameters into an asset-pricing or portfolio model requires new assumptions about whose preferences matter, evaluation horizon, joint distributions, reference wealth, and market clearing. The paper supplies none of those investment-specific inputs.
