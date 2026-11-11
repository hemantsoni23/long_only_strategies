# Jai Alai arbitrage strategies

Daniel Lane and William T. Ziemba. *The European Journal of Finance* 10(5), October 2004, pp. 353–369. DOI: 10.1080/1351847042000254239. [Source PDF](../../Finance/UniversalPortfolios_LaneZiemba_2004.pdf). The supplied 18-page file has a publisher cover followed by the complete 17-page article; printed page 353 is PDF page 2. The cover's February 2007 online date does not replace the article's 2004 publication year. All pages, formulas, figures, tables, and references were read.

## Why this matters

The paper studies a basic execution problem: an attractive first trade may become a safe two-sided position only if a complementary trade is subsequently available. A completed hedge can have a nonnegative payoff in every terminal state, while the strategy that attempts to assemble it remains risky. The contribution is a two-outcome betting formulation, a small-game optimization model, and simulation heuristics that trade off the entry threshold, the anticipated hedge margin, and the risk of remaining unhedged.

Team Jai Alai provides the setting. Two teams play points until one reaches a target score; fixed-odds tickets can be purchased between points, retain the odds quoted when purchased, and settle at the end of the game. The tickets are not assumed to be freely resalable. This makes the exercise relevant to sequential hedging with illiquid contracts, although the paper does not estimate a financial-market trading strategy.

The exact simultaneous-arbitrage condition is simple and does not require a probability forecast. The sequential strategy does require a forecast of future odds and, for expected-log optimization, outcome probabilities. Those forecasts are supplied by stylized simulation laws rather than a fitted dataset. The source also contains material inconsistencies in its hedge formulas, payout convention, score boundary, and some table descriptions. The reconstructions below distinguish algebraically exact corrections from unresolved simulation details.

## Scores, win probabilities, and quoted odds

Let $K$ be the winning score, and let $(m,n)$ denote current scores for teams A and B. Assume independent points with score-invariant probability $p$ that A wins and $q=1-p$ that B wins. The source primarily studies $K=30$ and $p=0.5$. The probability that A wins the game is

$$
P_A(m,n)=p^{K-m}\sum_{i=0}^{K-n-1}\binom{K-m+i-1}{i}q^i,
\qquad P_B=1-P_A.
$$

The summand counts sequences in which A obtains its required final point after $K-m-1$ earlier A points and $i$ B points. A numerically convenient equivalent is the backward recursion

$$
P_A(m,n)=pP_A(m+1,n)+qP_A(m,n+1),
\quad P_A(K,n)=1,\quad P_A(m,K)=0.
$$

This recursion reconstructs the intended score table without relying on its rounded entries or ambiguous row label. Equal ability implies $P_A(m,n)=1-P_A(n,m)$ and $P_A(m,m)=1/2$.

An odds quote $a$ “to one” is a net-profit multiple: a unit bet wins $a$ plus its returned stake, or loses the unit stake. The gross payoff conditional on winning is therefore $1+a$. Under the paper's initial definition of a common expected gross payout fraction $Q\in(0,1)$, consistent odds satisfy

$$
O_A=\frac Q{P_A}-1,\qquad O_B=\frac Q{P_B}-1.
$$

The printed interval $(1,0)$ and the malformed B formula in equation (1), p. 354, are typographical errors. The formulas above follow from the immediately preceding equalities $P_A=Q/(1+O_A)$ and $P_B=Q/(1+O_B)$. With these definitions, a unit bet on either side has expected gross receipt $Q$ and expected net loss $1-Q$. A fixed expected return per ticket does not by itself guarantee the bookmaker a realized profit regardless of its liability mix.

Multiplication yields the valid identity

$$
O_AO_B=1-\frac{Q(1-Q)}{P_AP_B}.
$$

Given $O_A=a$ and $Q$, the consistent opposite quote is

$$
O_B=\frac{Q(1+a)}{1+a-Q}-1.
$$

For example, $Q=0.85$ and $a=1$ imply $O_B=0.4782609$, agreeing with Table 2. Very likely outcomes can require negative net odds under a fixed $Q$: if $P_B>Q$, then $Q/P_B-1<0$. A venue's minimum payout rule then conflicts with this exact common-payout convention. The source discusses such “minus pools,” but a replication must specify the actual minimum odds and how the payout rule changes at the boundary. Simply imposing a floor alters expected returns and arbitrage opportunities.

## Exact simultaneous hedge geometry

Let $B_A,B_B\geq0$ be stakes at currently available net quotes $a,b>0$. With initial wealth $W$ and unbet cash retained, terminal wealth is

$$
W_A=W+aB_A-B_B,\qquad W_B=W+bB_B-B_A,
\qquad B_A+B_B\leq W.
$$

No-loss stakes must satisfy $aB_A\geq B_B$ and $bB_B\geq B_A$. For nonzero stakes this is equivalent to

$$
\frac1a\leq\frac{B_A}{B_B}\leq b.
$$

The interval is nonempty precisely when $ab\geq1$. Strictly positive guaranteed profit requires $ab>1$. At $ab=1$, the unique nonzero no-loss ratio pays zero net profit in both states. The source's Theorem 1 uses the weak inequality even though its introductory definition asks for a payoff sometimes positive; the weak case is a break-even hedge, not a strict arbitrage.

The condition is utility-independent because it describes payoff feasibility. It does not assert that all utility functions choose the same stake split. If both state profits are strictly positive, an increasing utility objective has an incentive to scale a fixed safe split to its available budget, subject to any omitted exposure or execution limits.

For a fully invested pair, parameterize

$$
B_A=\frac{fW}{1+a},\qquad
B_B=\frac{(1+a-f)W}{1+a}.
$$

The state profits are

$$
\Pi_A=W(f-1),\qquad
\Pi_B=\frac{W\{b(1+a)-f(1+b)\}}{1+a}.
$$

Thus the exact feasible interval is

$$
1\leq f\leq\frac{b(1+a)}{1+b}.
$$

Printed equation (8), p. 357, omits the factor $b$ in its upper bound. It cannot satisfy the preceding profit inequality in general. Also, choosing $f=1$ does not imply $ab=1$: it merely places A's payoff at break-even, leaving B's profit positive when $ab>1$. The source states the stronger implication incorrectly. Its earlier lower bound on $B_A$ likewise requires full budget use; it does not follow from a budget inequality alone because a safe pair can be scaled down.

The maximin hedge equalizes the two state profits. Solving $\Pi_A=\Pi_B$ gives

$$
f^*=\frac{(1+a)(1+b)}{a+b+2},\quad
B_A^*=\frac{W(1+b)}{a+b+2},\quad
B_B^*=\frac{W(1+a)}{a+b+2},
$$

and

$$
\Pi_A^*=\Pi_B^*=W\frac{ab-1}{a+b+2}.
$$

Equation (9), p. 358, has an extra one in its denominator, and the following profit expression lacks necessary grouping. These corrected expressions are derived directly from the printed state profits, and they implement the crossing drawn in Figure 1. They are not an undocumented change in investor preference.

If the pair budget must be fully spent and A wins with probability $P$, maximizing expected log terminal wealth instead gives

$$
\max_{B_A\in[0,W]}\{P\log[(1+a)B_A]+(1-P)\log[(1+b)(W-B_A)]\}.
$$

Its unconstrained maximizer is $B_A=PW$. With the no-loss restrictions, project that value onto $[W/(1+a),bW/(1+b)]$. This is a derived implementation of the paper's log objective; it explains why the maximin split and the growth-optimal split need not coincide. A completed hedge can safely tilt its surplus toward the more probable outcome.

## A consequential payout-convention inconsistency

The source writes actual quotes as $a=O_A(1+r_A)$ and $b=O_B(1+r_B)$. A no-loss opportunity requires $O_AO_B(1+r_A)(1+r_B)\geq1$. If both favorability factors equal $r$ and the base quotes are positive,

$$
r\geq\frac1{\sqrt{O_AO_B}}-1.
$$

Under equation (1)'s gross-payout convention, at a tied score with $Q=0.85$, the two base net quotes are $2Q-1=0.70$. The required equal uplift is therefore $1/0.70-1=42.857\%$. It is not the approximately 20% stated on p. 359.

Figure 3 instead labels the threshold as $r=(1-Q)/Q$, giving 17.647% at $Q=0.85$. This follows from a different convention: discount fair **net-profit** odds by $Q$,

$$
\widetilde O_A=Q\frac{P_B}{P_A},\qquad
\widetilde O_B=Q\frac{P_A}{P_B}.
$$

Then $\widetilde O_A\widetilde O_B=Q^2$, and the quoted Figure 3 threshold follows. Table 7's tied-score “actual odds” of 0.8500 are also consistent with this second convention, whereas equation (1) requires 0.7000. Under the second convention the expected gross payout on A is $P_A+QP_B$, which varies by outcome probability and is not the original common $Q$.

This distinction is economically material: it changes the house take, favored-team pricing, and how often a profitable pair appears. The agreement with Figure 3 and several table entries identifies a plausible reconstruction of the simulations, but the supplied paper has no code establishing which convention was used in every experiment. The reported numerical results below remain source results, not validated outcomes of the equation (1) model.

## Full-game expected-log optimization

For small games the paper formulates an optimization over game paths $g\in G$. At each nonterminal decision point, stakes $B_A(i),B_B(i)$ are nonnegative. Every realized path must respect a cumulative cash budget because previous tickets settle only at the game's end:

$$
\sum_{i\in g}\{B_A(i)+B_B(i)\}\leq W_0.
$$

For a path ending in A's victory, terminal wealth is

$$
W(g)=W_0+\sum_{i\in g}a_iB_A(i)-\sum_{i\in g}B_B(i),
$$

with the analogous B expression when B wins. The objective in equation (13), p. 360, is $\max E_g\log W(g)$. Positivity of wealth is required wherever a path has positive probability. Under the Bernoulli-point model, each outcome path has probability given by the product of its point probabilities; if quotes are random, their law must also enter the expectation.

The source adds cross-coverage constraints

$$
\sum_{i\in g}a_iB_A(i)\geq\alpha\sum_{i\in g}B_B(i),\qquad
\sum_{i\in g}b_iB_B(i)\geq\alpha\sum_{i\in g}B_A(i).
$$

At $\alpha=1$ these enforce no net loss for the accumulated pair exposures. For $\alpha<1$, they allow an A-state loss as large as $(1-\alpha)\sum B_B$, and similarly on B. Thus $\alpha=1/2$ implies at least half of total stakes are recovered, but the constraints are stronger and stake-composition dependent; they are not exactly a symmetric 50% loss limit. Unbet cash remains available at settlement. For $\alpha>1$, the pair must supply positive cross-coverage surplus.

A feasible implementation must also impose nonanticipativity: decisions at identical observed histories cannot depend on future points or future quote realizations. The paper discusses advance knowledge of a score-to-odds function or distribution but does not fully specify a stochastic scenario tree. Knowing the distribution of future quotes is different from knowing their realized future values. The latter would be an oracle benchmark rather than a tradable policy.

A race to $K$ has $K^2$ nonterminal score states, paths of $K$ through $2K-1$ points, and $\binom{2K}{K}$ complete point-outcome paths. The paper's small-game counts 2, 6, 20, 70, and 252 match this formula for $K=1,\ldots,5$. For $K=30$, however, it prints $5.91\times10^{16}$ instead of $\binom{60}{30}=1.1826458\times10^{17}$. Either count is computationally prohibitive for naive path enumeration; the discrepancy does not alter the motivation for heuristics.

## Small-game experiments and what they establish

The two- and three-point experiments use $W_0=1$, $\alpha=1$, nominal $Q=0.85$, and $p=0.5$. The first quote perturbation law is independent $N(0,\sigma^2)$ favorability across scores. The second is normal with score-dependent mean

$$
\bar r_i=\begin{cases}
\exp(-M/D)-1,&\text{team }i\text{ leads by }M,\\
\exp(pM/D)-1,&\text{team }i\text{ trails by }M,
\end{cases}
$$

where $D=K-\text{leader's score}$. The source's preceding notation sets $r_A=r_B$, whereas this second mean law differentiates the two teams. Their joint noise dependence is therefore not fully specified. An untruncated normal law also permits $r<-1$, producing negative multiplied quotes; the paper gives no clipping, rejection, or minimum-odds rule for that event.

Table 3 reports zero betting when $\sigma=0$. For two-point games under the first law, $\sigma=0.1$ gives one bet game in ten, full unit commitment when betting, and reported average fund gain 0.0005 per game played. At $\sigma=0.2$, five of ten games are bet, average commitment is 84% in those games, and average gain is 0.0073. The second law at $\sigma=0.2$ gives two bet games in ten, full commitment, and average gain 0.0119.

For three-point games, the first law with $\sigma=0.2$ gives seven bet games in ten, 80% average commitment, and average gain 0.0193. The second law gives three in ten at $\sigma=0.1$, 75% commitment, and gain 0.0098; at $\sigma=0.2$ it gives five in ten, 60% commitment, and gain 0.0059. These ten-game results do not establish monotonic improvement with quote variance: the last comparison declines. The paper additionally reports total expected gains of 1–2% in sets of 25 games, without enough detail to independently reproduce that summary.

The main qualitative observation is that the optimizer often selects opposite-team bets at different score states. More variable quotes provide more opportunities for a favorable pair, but also greater uncertainty about whether its second leg can be obtained. No statistical uncertainty, solver choice, tolerances, random seed, or independent test sample accompanies the small-game results.

## Sequential single-pair policy

The heuristic on pp. 362–365 starts with a favorability threshold $r_0$. Before each point, it generates the two quotes, checks whether an initial ticket exceeds that threshold, and, after entry, waits for an opposite ticket that completes the desired pair. A uniform random draw determines the point winner under the fixed $p$. Bets settle only after the game. The parameters are searched across simulated sets of games.

With zero anticipated margin and an initial A quote $a$, a one-unit pair uses first stake $1/(1+a)$ and reserves $a/(1+a)$ for B. Completion at $b=1/a$ breaks even in both states; a larger B quote supplies a surplus. A high entry threshold may select a larger initial edge but leave too little time for the hedge to complete. A low threshold produces more early entries and more completions, often with smaller surplus. Figure 4 illustrates that total simulated gain can vary nonmonotonically with $r_0$ and differ sharply across game sets.

For an anticipated product margin $\eta>0$, the bettor expects $ab=1+\eta$ and uses the corresponding endpoint or maximin split. The source denotes this margin by $m$, which should not be confused with the score. The first stake is determined before the actual second quote is known, so the planned margin may fail to materialize. An underestimated margin also creates an opportunity cost: the completed split may be less desirable than a split chosen with hindsight. This is a genuine decision under uncertainty, not a guaranteed arbitrage initiated at the first ticket.

In Table 4, game 10 begins with a B stake 0.8581 at quote 0.1654 and later an A stake 0.1419 at quote 7.6719. A's victory yields approximately $0.1419(7.6719)-0.8581=0.23054$, consistent with the reported 0.2304 after underlying rounding. The displayed B loss −0.8531 appears inconsistent with its 0.8581 stake. Game 11 has an unmatched A stake 0.0306 that loses. Game 21 pairs B stake 0.6493 at 0.5401 with A stake 0.3507; B's victory yields approximately zero, matching the table.

The table has a further replication issue: two games finish with a winning score of 31 although the model describes first to 30. A direct reconstruction using the net-profit-discount convention reproduces the first two examples' base odds with $K=31$: at score $(18,23)$ the B quote is 0.128798, and at $(14,23)$ the A quote is 25.747968. The third example's 0.4466 B quote at $(0,3)$ and 2.0653 A quote at $(1,5)$ instead match $K=30$. This agreement is evidence of mixed score conventions in the examples, not proof of the unpublished simulator's implementation.

The source says an uncompleted first leg invariably loses. That is not a general theorem of the stated random-quote model: the initially backed team could win even if no acceptable second quote appeared. The illustrated loss demonstrates completion risk, but does not establish that every unmatched ticket must lose.

Table 5 reports total gains for 100-game sets under the score-dependent law with $\sigma=0.2$. At zero anticipated margin, all three split policies coincide: gains for $r_0=0,0.05,0.10,0.20$ are 1.41, 0.47, −0.22, and 2.22 betting units. At $\eta=0.20,r_0=0.20$, the endpoint, maximin, and opposite endpoint policies report 3.09, 4.09, and 5.17 units. At the same margin with $r_0=0.10$, they lose 1.47, 1.50, and 1.57 units. These are totals in the paper's fixed betting-unit convention; they should not be labeled annual returns or percentages of fully reserved capital.

The paper also evaluates an “automatic,” score-dependent stake split, but does not give an explicit formula sufficient to reconstruct it. Table 6 reports:

| Anticipated margin $\eta$ | $r_0=0$ | $r_0=0.05$ | $r_0=0.10$ | $r_0=0.20$ |
|---|---:|---:|---:|---:|
| 0 | 1.41 | 0.47 | −0.22 | 2.22 |
| 0.05 | 2.11 | 1.03 | −0.02 | 3.55 |
| 0.10 | 2.49 | 2.33 | 0.02 | 3.61 |
| 0.20 | 0.94 | 0.02 | −1.24 | 3.12 |

The authors describe a reduction in the variance of gains from about 6 to 4. They do not specify the precise variance estimator, sampling unit, number of independent replications, or confidence interval. Their statement that policy differences are not significant is not accompanied by a reported test statistic. The automatic policy is therefore a promising reported heuristic, not a fully specified algorithm whose statistical superiority has been established.

## Multiple unfinished pairs and capital accounting

The final simulation allows several pairs during a game. Each pair receives the same unit budget; total available stake capital is capped at 60 units. At each decision point, completing an existing unmatched pair takes priority over starting another one. The automatic split policy is retained. This priority rule is important because previously bought tickets cannot be liquidated to finance an attractive new trade.

Table 8 uses the score-dependent favorability law with $\sigma=0.3$ and 100-game sets. Reported total gains are:

| Anticipated margin $\eta$ | $r_0=0$ | $r_0=0.05$ | $r_0=0.10$ | $r_0=0.20$ |
|---|---:|---:|---:|---:|
| 0 | −1.96 | 2.12 | 11.29 | 17.21 |
| 0.05 | −0.76 | 4.51 | 13.27 | 19.12 |
| 0.10 | −0.79 | 3.77 | 10.34 | 17.26 |
| 0.20 | 2.83 | 4.74 | 8.19 | 14.17 |

The largest displayed total is 19.12 units at $(\eta,r_0)=(0.05,0.20)$; it is an in-sample parameter-grid outcome, not an independently validated optimum. Increasing the assumed margin to 0.20 at the same threshold lowers the total to 14.17, consistent with more demanding completion requirements.

The source reports one to twenty completed hedges in simulated games, at most three uncompleted pairs in the examined sets, approximately a 60–40 split between winning and losing games, losses no greater than one unit in the reported simulations, and gains as high as three units. None is a deterministic loss bound. With several unmatched first legs, realized losses depend on all their stakes and on the common game outcome. The paper reports gain variance around 40 versus 6 for the single-pair case, reflecting the extra aggregate exposure, but again does not supply inference details.

Table 7's worked multi-pair game ends with A stakes totaling 7.5549 lost and B net winnings of 8.7968, giving net gain 1.2419. The preceding prose calls this 24% of a betting unit; that description does not match the table's arithmetic. The table should be retained as a unit-denominated example, with the discrepancy disclosed. A return on committed capital would require dividing by an explicitly defined capital base, such as actual stakes or the full 60-unit reserve. Different denominators answer different questions.

## Replication specification and remaining evidence gaps

A faithful reimplementation can recover the state probability recursion, no-loss feasibility region, corrected stake geometry, and the broad threshold-and-completion heuristic. It must make additional choices that the source leaves unresolved: whether $Q$ discounts gross payout or fair net odds; whether each experiment stops at 30 or 31; the joint and serial distribution of quote shocks; truncation and minimum-odds rules; quote arrival and trade timing; the automatic split formula; which unmatched pair is completed first when several qualify; and the exact cash-reservation convention. These choices should be exposed as model parameters rather than silently selected to fit a reported table.

For an independent simulation, one would predeclare training games for parameter selection and a separate evaluation set, report net profit in units alongside maximum tied-up capital, separate completed-pair surplus from unmatched-leg profit or loss, and retain every quote and stake in an event log. Such a protocol is a proposed replication design, not an experiment performed in the article. The paper provides no random seeds, source code, raw simulation paths, standard errors, commissions, ticket limits, latency model, counterparty failures, or independently estimated player probabilities.

The authors mention preliminary observations of pricing inefficiency at a Mexico City fronton but do not present a timestamped odds dataset or an empirical test of the Gaussian quote models. They explicitly call for more data and more realistic score-dependent point probabilities. Their financial analogies—nonmarketable currency hedges, agricultural delivery contracts, and warrant positions—illustrate the sequential completion problem. They do not establish that those markets share the simulated profit opportunity or the same terminal-state structure.

The durable result is the distinction between payoff certainty after both legs are locked and execution risk before the second leg exists. The exact two-state hedge algebra is usable immediately after correcting the printed slips. The simulation claims require a reconstructed and documented model before they can support capital allocation. The relevant source pointers are pp. 354–359 for probabilities, pricing, and perfect hedges; pp. 360–361 for the small-game program; pp. 362–365 for single-pair heuristics; and pp. 366–367 for multiple pairs. The references to Kelly (1956), MacLean–Ziemba–Blazenko (1992), and Shaw–Thorp–Ziemba (1995) identify the paper's growth-optimal and sequential-arbitrage background; this note does not claim an independent empirical validation of those cited applications.
