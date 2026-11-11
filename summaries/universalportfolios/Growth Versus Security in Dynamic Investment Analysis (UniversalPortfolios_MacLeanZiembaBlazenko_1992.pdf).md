# Growth Versus Security in Dynamic Investment Analysis

L. C. MacLean, W. T. Ziemba, and G. Blazenko. *Management Science* 38(11), November 1992, pp. 1562–1585. [Source PDF](../../Finance/UniversalPortfolios_MacLeanZiembaBlazenko_1992.pdf). The complete 24-page scanned article, including proofs, eight figures, five tables, and references, was read with OCR and visual inspection. Printed page 1562 is PDF page 1.

## Why this matters

The paper asks how to choose exposure when maximizing long-run growth produces an uncomfortable wealth path. It organizes the problem around six distinct performance measures: expected wealth, expected logarithmic growth, expected time to a target, terminal target probability, probability of remaining above a prescribed path, and probability of reaching an upper target before a lower boundary. These criteria answer different investment questions. An attractive expected payoff or a high eventual success probability can coexist with an unacceptable waiting time or substantial interim losses.

The proposed practical tool is a family of portfolios mixing the growth-optimal allocation with cash. Varying one scalar traces a growth–security profile that can be computed and discussed with an investor. The authors explicitly distinguish this convenient family from the true efficient frontier over all dynamic strategies. Fractional Kelly is generally an effective exposure-control device, not a proof of optimality for every drawdown or target constraint.

The paper develops random-walk calculations and illustrates them with blackjack, racing, lottery tickets, and an index-futures seasonal spread. Several calculations in the supplied article require correction or qualification. In particular, the printed mean first-passage bounds are not valid generally; a simple exact counterexample is given below. Some numerical examples have inconsistent fractions, capital scales, or return units. This note preserves the source's contributions and empirical illustrations while separating exact identities, approximations, reported outputs, and derived corrections.

## Dynamic investment model and fixed-fraction specialization

There are $n$ risky investments and a cash asset with zero net return. At time $t$, the portfolio is $p_t=(p_{0t},p_{1t},\ldots,p_{nt})$, measurable with respect to past observations, with nonnegative weights summing to one. Risky net returns are $K_{it}$, gross returns are $R_{it}=1+K_{it}$, and $R_{0t}=1$. Wealth follows

$$
Y_t=y_0\prod_{s=1}^t\left(\sum_{i=0}^nR_{is}p_{is}\right).
$$

The log objective requires strictly positive portfolio gross return almost surely and suitable integrability. Long-only weights alone do not prevent zero wealth if all money is invested in an asset that can lose 100%. The statement that fixed-fraction strategies never ruin must therefore be read with the positive-gross-return admissibility condition; it also does not prevent wealth from approaching zero asymptotically.

The source introduces $K_{it}=a_i(t)E_{it}$, with positive deterministic scale $a_i(t)$ and temporally independent errors. Its calculations later specialize to stationary return distributions and a fixed portfolio. A favorable environment has at least one positive expected risky net return. Under an independent stationary model, the growth-optimal portfolio solves

$$
\bar p\in\arg\max_{p_i\geq0,\ \sum_{i=1}^np_i\leq1}
E\log\left(1+\sum_{i=1}^np_iK_i\right).
$$

This is a concave optimization when the return distribution is fixed and the feasible log domain is respected. A finite scenario implementation uses the scenario probabilities and maximizes their weighted log gross returns. It should verify nonnegativity, the joint budget, and first-order directional derivatives at the solution.

The p. 1564 componentwise formula $p_{it}=\min\{a_i(t)^{-1}\bar p_i,1\}$ cannot be used as a general multivariate budget-constrained solution. For example, two base weights of one-half and two scales of one-half produce two proposed weights of one, violating the total budget. A change in scale alters the feasible set in the rescaled variables; joint optimization is required when the candidate rescaling is infeasible. The fixed stationary portfolio formulation below does not depend on that shortcut.

Let $p^0=(1,0,\ldots,0)$ be cash and define

$$
p(\lambda)=\lambda\bar p+(1-\lambda)p^0,\qquad0\leq\lambda\leq1.
$$

If $H=\sum_i\bar p_iR_i$ is the full-Kelly gross portfolio return and $V=H-1$, then the fractional portfolio gross return is $1+\lambda V$. This reduction preserves the entire distribution of the selected risky basket. It does not replace that distribution with only its mean and variance.

## Six measures and their operational differences

For a fixed portfolio, the source defines three growth measures:

$$
G_1(t)=E Y_t,\qquad
G_2(t)=\frac1tE\log Y_t,\qquad
G_3(U)=E\tau_U,
$$

where $\tau_U=\inf\{t:Y_t\geq U\}$. Higher values are desirable for the first two; smaller values are desirable for the third. Long-run log growth is $\phi=\lim_{t\to\infty}G_2(t)$.

The security measures are

$$
S_1(t,b_t)=P(Y_t\geq b_t),
$$

$$
S_2(\{b_t\})=P(Y_t\geq b_t\text{ for every }t\geq1),
$$

and

$$
S_3(L,U)=P(\tau_U<\tau_L),\qquad
\tau_L=\inf\{t:Y_t\leq L\},\quad L<y_0<U.
$$

A terminal target probability allows an earlier loss and subsequent recovery; a path constraint does not. The upper-before-lower probability ignores how long success takes. The paper pairs expected wealth with terminal security, log growth with path security, and inverse expected target time with upper-before-lower probability. These are presentation choices, not mathematical equivalences.

An efficient frontier optimizes one measure subject to a required level of another over the complete feasible strategy class. Figure 1 deliberately draws the fractional-Kelly path inside that frontier. Its simplicity comes from fixing the risky composition and varying exposure, thereby excluding many wealth-dependent or time-dependent controls. Cash maximizes certain downside-protection measures, but it cannot reach a strictly higher target: the cash endpoint has $\tau_U=\infty$ and upper-target success probability zero when $U>y_0$. A limiting small-positive-exposure result must not be assigned mechanically to exactly zero exposure.

## Exact accumulation and a terminal normal approximation

For independent identically distributed portfolio returns, set

$$
J_\lambda=\log(1+\lambda V),\quad
\mu_\lambda=EJ_\lambda,\quad
\sigma_\lambda^2=\operatorname{Var}(J_\lambda),\quad z_0=\log y_0.
$$

Log wealth is the random walk $Z_t=z_0+\sum_{s=1}^tJ_{\lambda,s}$. Equations (2)–(3), p. 1567, imply the exact formulas

$$
E Y_t=y_0(1+\lambda EV)^t,
\qquad
\frac1tE\log Y_t=\mu_\lambda+\frac{z_0}t.
$$

The first formula needs independence across periods; merely zero autocorrelation is not sufficient to factor the expectation of a product. The second follows from linearity of expectation and stationarity of the mean log return, with weaker dependence requirements.

For terminal security the paper uses a normal approximation to accumulated log wealth:

$$
P(Y_t\geq b_t)\approx
1-\Phi\left(\frac{\log b_t-z_0-t\mu_\lambda}{\sqrt t\,\sigma_\lambda}\right).
$$

This is not an exact lognormality assumption established by the investment model. It can be poor for a short horizon, discrete large jumps, or lottery-like returns whose mean is dominated by extremely rare prizes. The denominator is the standard deviation of accumulated log wealth. Table 2's notation should be interpreted consistently with the explicit normal formula in equation (4), not as a second exact law.

The mean and median of a lognormal approximation differ: its median is $y_0e^{t\mu_\lambda}$, whereas its mean incorporates a variance term. This distinction becomes important in the racing table, whose last row uses a symbol previously defined as a mean but is explicitly labeled a median in its footnote.

## Computing path survival without a Gaussian approximation

Equations (5)–(7), p. 1568, propose a sequential convolution for survival above a log boundary $b_t^*=\log b_t$. A clean reconstruction uses an unnormalized surviving measure $q_t$, avoiding confusing conditional-normalization indices. Start with a point mass at $z_0$. For a jump distribution $F_J$,

$$
q_t(dz)=\mathbf1\{z\geq b_t^*\}\int q_{t-1}(dx)F_J(dz-x).
$$

Its total mass is $P(Z_s\geq b_s^*,1\leq s\leq t)$. For discrete jumps, this is a finite or countable sum; for continuous jumps, it is a quadrature or convolution. The infinite-horizon survival probability is the decreasing limit of these masses. If conditional densities are used instead, normalize each surviving measure by its previous survival mass and multiply the one-step conditional survival probabilities. This is the same probability structure intended by the source.

The recursion is exact before state-grid approximation or horizon truncation. A reproducible numerical implementation should specify its log-wealth grid, interpolation, jump quadrature, boundary convention, truncation horizon, and residual survival tail. None of these numerical tolerances is documented in the article. A predefined exponential floor $b_t=y_0a^t$ also differs from a drawdown floor based on the running maximum; the latter requires an additional state variable.

## Upper-before-lower probability and overshoot bounds

Assume bounded log jumps $j_-\leq J\leq j_+$, with $j_-<0<j_+$ and positive drift $\mu=EJ>0$. Write $l=\log L$, $u=\log U$. The exact hitting probability solves

$$
\beta(z)=E\beta(z+J),\quad l<z<u;\qquad
\beta(z)=0\ (z\leq l),\quad\beta(z)=1\ (z\geq u).
$$

For a nondegenerate jump law with both signs, there is a nontrivial positive root $\theta<1$ of $E\theta^J=1$, in addition to the root one. Then $\theta^{Z_t}$ is a martingale. For a bounded exit interval, optional stopping and the possible upper and lower overshoots yield equation (9), p. 1569:

$$
\frac{\theta^z-\theta^l}{\theta^{u+j_+}-\theta^l}
\leq\beta(z)\leq
\frac{\theta^z-\theta^{l+j_-}}{\theta^u-\theta^{l+j_-}}.
$$

These are bounds, not exact probabilities unless the overshoot structure makes them coincide. The source reports their midpoint as a convenient estimate. The approximation uncertainty is at most half the bound width if the assumptions hold. A stable implementation can solve for $s=\log\theta<0$ using $Ee^{sJ}=1$, exclude the trivial root $s=0$, and evaluate differences of exponentials stably.

The negative-drift and zero-drift cases require separate interpretation; at zero drift the two roots coalesce, so substituting $\theta=1$ directly gives indeterminate fractions. For positive drift and bounded two-sided jumps, the stopped martingale argument is much stronger than simply fitting a convenient exponential shape to a difference equation.

## A failure of the printed mean first-passage bounds

The exact mean time to an upper target satisfies

$$
\eta(z)=1+E\eta(z+J),\quad z<u;\qquad\eta(z)=0\quad z\geq u.
$$

The particular solution $-z/\mu$ in equation (10) is correct, and harmonic functions can be added. But the boundary condition must hold on the full overshoot region, and the admissible growth of the solution as $z\to-\infty$ matters. An arbitrary exponential harmonic component does not become the expected passage time merely by fitting one endpoint.

Equation (11), p. 1570, defines $u_-=u-j_-$ and $u_+=u+j_+$ and claims bounds of the form

$$
\frac{u_-\theta^{z-u_-}-z}{\mu}
\leq\eta(z)\leq
\frac{u_+\theta^{z-u_+}-z}{\mu}.
$$

A derived exact counterexample shows that these inequalities fail even at a full-Kelly allocation. Let a risky asset have gross outcomes $e$ and $e^{-1}$, with up probability $p=e/(1+e)$ and down probability $1-p=1/(1+e)$. Cash returns one. At full investment, $E(1/R)=1$, so the derivative of $E\log[1+f(R-1)]$ at $f=1$ is zero; concavity makes $f=1$ the Kelly optimum. Its log jump is $J=\pm1$, its drift is $\mu=2p-1=0.462117\ldots$, and its nontrivial root is $\theta=e^{-1}$. Start at $z=0$ and target $u=1$. Both $u_-$ and $u_+$ equal two, so both printed bounds equal $2e^2/\mu\approx31.979$. The actual mean time for the biased nearest-neighbor walk to hit one is $1/\mu\approx2.164$. There is no overshoot at that integer boundary. This construction respects the long-only cash/risky-asset model and belongs to the fractional-Kelly family at $\lambda=1$.

For positive drift and the integrability needed for Wald's identity, the valid reconstruction is

$$
E\tau_U=\frac{u-z+E O}{\mu},\qquad
O=Z_{\tau_U}-u\in[0,j_+],
$$

hence

$$
\frac{u-z}{\mu}\leq E\tau_U\leq\frac{u-z+j_+}{\mu}.
$$

The exact lattice example gives zero overshoot and therefore $1/\mu$ periods. This correction is derived here; it is not presented as a published erratum. It means that the article's very large numerical waiting-time estimates and the stopping-time part of its tradeoff proof cannot be accepted solely on the basis of equation (11). The valid upper-before-lower bounds use a different stopped-martingale argument and are not invalidated by this counterexample.

## What the fractional-Kelly tradeoff establishes

The main valid growth calculation can be proved directly along the one-dimensional family:

$$
\phi'(\lambda)=E\frac{V}{1+\lambda V},\qquad
\phi''(\lambda)=-E\frac{V^2}{(1+\lambda V)^2}\leq0.
$$

Because $\lambda=1$ maximizes log growth over the feasible family, $\phi$ is nondecreasing on $[0,1]$. Strict growth before the optimum needs nondegeneracy; at an interior unconstrained Kelly optimum the derivative at one is zero, contrary to an unqualified strictly positive derivative throughout the closed interval. Expected wealth increases with $\lambda$ when $EV>0$, directly from its exact formula. Maximizing expected wealth over the full strategy class is not the same as maximizing log growth.

The downside-probability monotonicity has a simple pathwise proof under the restricted benchmarks used by Lemmas 3.2 and 3.4. For $0\leq\lambda_1<\lambda_2$, concavity of log and its value zero at cash imply

$$
\log(1+\lambda_1V_s)\geq
\frac{\lambda_1}{\lambda_2}\log(1+\lambda_2V_s).
$$

Summing along any realized path gives the same inequality for cumulative log gains. If the higher-exposure path is above a nonpositive cumulative log boundary, the lower-exposure path is also above it. Thus the events are nested for an exponential fallback floor $y_0a^t$ with $a\leq1$, and for terminal preservation of initial wealth. Security is nonincreasing as exposure rises. This proves a non-strict probability ordering without differentiability of a discrete distribution. It does not extend automatically to a target above starting wealth: cash cannot achieve such a target.

The stopping-rule result in Lemma 3.5 concerns midpoints of the proposed bounds, reciprocal upper/lower targets $U=ky_0$, $L=y_0/k$, and an additional “flexibility” condition. In compact notation, its condition compares $l_-' /l_-$, $E[J'\theta^J]/E[J\theta^J]$, and $u_+' /u_+$, with derivatives along the portfolio family. Differentiating the root equation gives

$$
\theta'=-\theta\log\theta\,
\frac{E[J'\theta^J]}{E[J\theta^J]},
$$

when differentiation is valid and the denominator is nonzero. The source uses this relationship and boundary derivatives to sign the changes in its midpoint formulas. The condition is substantive, and the first-passage-time formula being differentiated is already invalid generally. The final “tradeoff theorem” should therefore not be elevated to a universal theorem about exact stopping times or all security measures.

## Blackjack: a clean small-edge illustration

The blackjack application approximates favorable play by independent even-money wagers with win probability 0.51 and loss probability 0.49. This is a model of a 2% edge, not a full card-counting simulator; splits, doubles, ties, changing deck composition, and betting limits are omitted. A fraction $f$ of current wealth gives

$$
\phi(f)=0.51\log(1+f)+0.49\log(1-f),
\qquad f^*=0.02.
$$

Table 3 reports the following relationship between fractional exposure, normalized growth, and the approximate probability of doubling before halving:

| Fraction of Kelly | Wealth fraction bet | Relative growth | Doubling-before-halving probability |
|---|---:|---:|---:|
| 0.2 | 0.004 | 0.36 | 0.998 |
| 0.4 | 0.008 | 0.64 | 0.94 |
| 0.5 | 0.010 | 0.75 | 0.89 |
| 0.8 | 0.016 | 0.96 | 0.74 |
| 1.0 | 0.020 | 1.00 | 0.67 |
| 1.5 | 0.030 | 0.75 | 0.56 |
| 2.0 | 0.040 | 0.00 | 0.50 |

The growth ratios are rounded and approximately follow $2\lambda-\lambda^2$, obtained from the small-edge quadratic expansion of log growth. The exact logarithmic formula remains the appropriate computational input. Half Kelly preserves roughly three-quarters of growth while increasing the reported boundary-success probability from 67% to 89%. Overbetting beyond Kelly reduces growth in this example. The probability estimates come from the boundary calculations, not a reported sample of casino trials, so they have approximation uncertainty rather than conventional sampling standard errors.

## Racing: simultaneous outcomes and an inconsistent allocation example

The general racing model assigns probability $\pi_{ijk}$ to each ordered top-three finish. Fractions can be placed on win, place, and show tickets for each horse, subject to a total budget. Win tickets pay only for the winner; place and show tickets share their respective net pools across two and three finishing horses. The source's payoff formula subtracts losing stakes and allocates the residual pools after track take and refunding winning stakes. Given the joint finishing probabilities, pool totals, and the bettor's price-taking assumptions, it defines a finite-scenario log-optimization problem. If the bettor materially changes pool sizes, the quoted-return model must be adjusted.

The simplified example uses five simultaneous races, one selected horse per race. Collection probabilities are 0.570, 0.380, 0.285, 0.228, and 0.190, with net odds 1, 2, 3, 4, and 5. Each has expected gross receipt 1.14 per unit stake. The paper prints a Kelly vector including cash of $(0.8529,0.0140,0.0210,0.0141,0.0700,0.0280)$. Its risky weights sum to 0.1471, whereas the next page calls the Kelly betting fraction 6%. These are inconsistent. The source also does not explicitly give the joint outcome law across races, which is required for simultaneous portfolio optimization. Neither the weights nor the 6% description should silently be substituted for the other.

Table 4 starts at \$1,000 and considers 700 periods. It compares the printed Kelly policy, half Kelly, and fixed total betting fractions of 1%, 5%, and 10%, the latter spread in proportions $(0.1,0.3,0.3,0.2,0.1)$. At the \$1,000 target, reported success probabilities are 0.892, 0.961, 0.980, 0.856, and 0.517. At \$10,000 they are 0.603, 0.445, 0.003, 0.512, and 0.304. At \$100,000 they are 0.231, 0.028, 0, 0.148, and 0.141. This demonstrates how reducing exposure can improve capital preservation yet reduce the chance of reaching a high target by a fixed date.

The last row reports \$17,497, \$8,670, \$2,394, \$10,464, and \$1,176. Despite using the earlier mean-wealth symbol, the table footnote explicitly says these are **medians**, based on approximate lognormality. They should not be presented as expected wealth. Given the inconsistent allocation description and missing joint law, this note reports the table rather than claiming to have reproduced it. The cited racetrack evidence about mispriced place and show bets comes from earlier studies; this article does not provide a new raw odds dataset or out-of-sample betting test.

## Lottery: positive edge, tiny exposure, and disputed scales

Table 5 models Canadian-style 6/49 tickets with five mutually exclusive prize categories. Probabilities are the reciprocals of 13,983,816; 2,330,636; 55,492; 1,032; and 57. The residual probability gives no prize. Case A prizes are \$6 million, \$0.8 million, \$5,000, \$150, and \$10; Case B prizes are \$10 million, \$1.2 million, \$10,000, \$250, and \$10. Ticket cost is \$1. These are favorable hypothetical prize scenarios involving carryovers and unpopular selections, not representative unconditional returns from ordinary lottery participation.

The source reports expected receipts 1.181 and 1.827 per ticket, edges of 18.1% and 82.7%, and Kelly fractions $1.1\times10^{-7}$ and $6.5\times10^{-7}$. The displayed prize/probability inputs imply approximately 1.1832 and 1.8279, so even the first expected receipt is only approximately consistent with its table.

For a one-ticket payoff distribution scaled as an investment opportunity, the exact scalar optimization is

$$
\max_{0\leq f<1}\sum_s\pi_s\log[1+f(v_s-1)],
$$

where $v_s$ is gross prize per unit ticket cost, including zero. An interior optimum solves $\sum_s\pi_s(v_s-1)/[1+f(v_s-1)]=0$. A derived bisection calculation on the printed inputs gives about $9.7474\times10^{-8}$ for A and $5.9523\times10^{-7}$ for B. Those figures are not replacements based on unknown original inputs; they document what the displayed distribution itself implies.

There is a separate factor-of-ten inconsistency. Multiplying the source's own printed fractions by a \$10 million bankroll yields 1.1 and 6.5 dollars, yet its table says 11 and 65 tickets. Its stated minimum bankrolls of about \$1 million and \$150,000 likewise disagree with the printed fractions, which require about \$9.09 million and \$1.54 million to fund a one-dollar fraction. The graphs place wagers on the $10^{-7}$ to $10^{-6}$ scale, so the discrepancy cannot be resolved by simply treating every printed fraction as ten times larger.

Pages 1580–1582 report many extreme waiting times, including 294 and 55 billion years for high-confidence tenfold growth under very small bets, assuming 100 draws per year, and millions of years in other configurations. These are source outputs from the disputed target-time machinery, not validated forecasts. For scale, the exact expected log returns at the bisection optima above are approximately $7.7227\times10^{-9}$ and $1.30254\times10^{-7}$ per opportunity. The leading target-time terms $\log(10)/\mu$, divided by 100, are roughly 2.98 million and 176,777 years, before the bounded overshoot correction. This derived comparison is not the same exposure or target specification as every reported figure. It confirms an extremely long horizon while showing why the paper's precise year counts should not be imported without recomputation.

Multiple tickets in one drawing also share the same winning number and need a joint payoff model; multiplying a one-ticket fraction is not equivalent to creating independent repeated opportunities. Carryover availability, taxes, prize-sharing, and number-popularity estimates are treated as favorable inputs. Their uncertainty and temporal persistence are not estimated in this article.

## Index futures: application and reproducibility limits

The final example buys the Value Line index and sells the S&P 500 near year-end to express historical small-stock seasonal outperformance. The paper describes Value Line as a geometric index of about 1,700 securities and the S&P as capitalization-weighted. A spread point is worth \$500. It reports average successful-trade gain 2.85 points and \$1,342.50 after an assumed commission of $1.5\times\$55$; this arithmetic is consistent with $2.85\times500-82.50$.

The supplied approximate distribution uses gains $(7,6,5,4,3,2,1,0,-1)$ with probabilities $(0.007,0.024,0.070,0.146,0.217,0.229,0.171,0.091,0.045)$. These probabilities sum to one but imply mean 2.362, not the stated 2.85. The source reports a full-Kelly investment fraction of 74%. If those gain numbers are interpreted directly as net returns per invested unit, solving $\sum_s\pi_sg_s/(1+fg_s)=0$ gives approximately 0.9291, not 0.74. A missing conversion from spread points to return on committed capital, or different underlying inputs, could explain part of the difference; the paper does not specify enough to decide. Futures margin capital, loss support, and portfolio leverage must be defined before the fraction is implementable.

The paper recommends much smaller exposure because of uncertain estimates, volatility, and margin requirements. It reports an illustrative \$100,000 client account buying five spreads on December 17, 1986 at −22.18 and selling on the following January 14 at −16.47. It calls the gain 5.55 points per contract and \$14,278.50 after costs. The quoted entry and exit differ by 5.71 points, so the stated point gain and cash profit cannot all be reproduced from the supplied figures and the earlier commission convention. This is a reported trade example, not an audited performance series.

Figures 7–8 plot high upper-target success probabilities for fractional exposure, but their inputs inherit the distribution and capital-unit ambiguities. No return observations, precise estimation window, sample size, formal hypothesis test, confidence intervals, roll methodology, slippage model, or stress-margin analysis is supplied here. The paper refers the reader to Clark and Ziemba (1987) and later work for additional seasonal-spread details; those cited studies are not independently replicated in this note.

## Reconstructable contribution and proper use

A practical implementation can retain the paper's six-measure framework, solve the log-optimal scenario problem, sweep fractional exposure, compute exact log moments, and use survival recursion or valid stopped-martingale bounds. The resulting profile should label exact quantities, distributional approximations, and numerical bounds separately. For first-passage time, use the renewal equation with correct boundary and growth conditions, or the Wald/overshoot representation, rather than the printed equation (11).

The paper's central design insight survives its calculation problems: exposure should be evaluated against the investor's actual target, downside floor, and horizon, and a positive expected edge is insufficient. Its illustrations also show why one cannot infer target attainment from a mean or infer a reasonable horizon from a high eventual success probability. What remains unestablished is the universal efficiency of fractional Kelly, a generally valid stopping-time tradeoff theorem as printed, and an exact replication of several reported numerical cases.

Source locations are pp. 1563–1566 for the model and criteria, 1567–1570 for computation, 1570–1574 for tradeoff claims and proofs, 1575–1576 for blackjack, 1577–1578 for racing, 1579–1582 for lottery scenarios, and 1582–1584 for the seasonal spread. The article draws on Kelly (1956), Breiman (1961), Algoet and Cover (1988), Feller's random-walk methods, and earlier applied work. Those references locate the contribution; claims derived or corrected in this note are explicitly identified rather than attributed to those unread external sources.
