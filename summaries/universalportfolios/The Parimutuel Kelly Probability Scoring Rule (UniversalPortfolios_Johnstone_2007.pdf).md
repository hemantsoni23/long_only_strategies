# The Parimutuel Kelly Probability Scoring Rule

David J. Johnstone. *Decision Analysis* 4(2), June 2007, 66–75. DOI 10.1287/deca.1070.0091. Source: [UniversalPortfolios_Johnstone_2007.pdf](../../Finance/UniversalPortfolios_Johnstone_2007.pdf). The supplied ten-page scan was read visually in full, including Figure 1, the appendix, and references. References below use printed pages.

## Why this matters

A scoring rule can reward accurate probabilities and still give a forecaster incentives to misreport. The distinction turns on the benchmark, payout function, and forecaster's influence on prices. Johnstone connects three objects that are often treated separately: the ordinary logarithmic probability score, a competitive score relative to other forecasters, and wealth growth from Kelly betting. He then replaces exogenous betting odds with odds determined by the forecasters themselves. The resulting parimutuel score has a direct economic interpretation, but it is not a strictly proper probability score.

For a quantitative research organization, this identifies a design choice rather than one universally preferable performance measure. An analyst rewarded for expected log score against a fixed benchmark optimally reports an honest subjective probability. An analyst whose report changes the consensus price against which performance is measured generally shades the report toward the rival consensus. The distortion becomes small when each analyst has little market influence and rival probabilities remain away from certainty. The paper therefore offers a model of the difference between a prediction market and a pure probability-elicitation mechanism.

Its contributions are analytical: a betting interpretation of the Kilgour–Gerchak competitive logarithmic score, an endogenous parimutuel benchmark, and an explicit conditional best-response formula. Figure 1 consists of illustrative calculations, not an empirical forecasting tournament. The source contains no stock universe, historical forecast panel, fitted coefficients, statistical significance tests, transaction costs, or out-of-sample trading results.

## Reports, beliefs, and proper scores

A binary outcome is $x\in\{0,1\}$. Forecaster $i$, among $n>1$ participants, reports $p_i$ for outcome one. Write $s_i=p_i^*$ for that forecaster's honest subjective probability. The distinction between $p_i$ and $s_i$ is essential: the strategic problem chooses the report while holding the belief fixed.

The individual logarithmic score is

$$
f_i(p_i;x)=x\log p_i+(1-x)\log(1-p_i).
$$

For interior beliefs, its subjective expected value is uniquely maximized at $p_i=s_i$. Differentiating gives $s_i/p_i-(1-s_i)/(1-p_i)=0$, and strict concavity gives the unique optimum. Equivalently, the expected-score loss from a false report is the Bernoulli relative entropy

$$
\mathbb E_i[f_i(s_i;x)-f_i(p_i;x)]
=s_i\log\frac{s_i}{p_i}+(1-s_i)\log\frac{1-s_i}{1-p_i}\ge0.
$$

The relative-entropy expression is a direct reconstruction of this properness property. It measures disagreement with the forecaster's own belief, not proof that the belief is objectively correct. Properness induces honest reporting; it does not supply calibration or information quality.

The Kilgour–Gerchak competitive score subtracts the average score of the other participants:

$$
G_i(p_1,\ldots,p_n;x)=f_i(p_i;x)
-\frac1{n-1}\sum_{j\ne i}f_j(p_j;x).
$$

Holding other reports fixed, the second term does not depend on $p_i$, so the maximizer of expected $G_i$ remains $s_i$. Also, $\sum_iG_i=0$ outcome by outcome. This is self-financing in score units, and adding a fixed payment $B/n$ produces a fixed aggregate reward $B$. The same competitive construction can be applied to the quadratic score $-(x-p_i)^2$, although the paper thereafter concentrates on logarithmic scoring.

The qualification about utility is substantive. Strict properness assumes maximization of expected numerical score, or linear utility of its monetary equivalent. A concave transformation of the payout need not preserve honest reporting. The source discusses sufficiently small payments as an approximation under which utility is nearly linear, not an exact solution for arbitrary risk preferences. Nor is a positive flat payment a universal bound on losses when unrestricted log scores can approach negative infinity. A practical bounded-payment protocol needs an explicit report domain or another payoff construction.

## Fixed-odds Kelly interpretation

Let $\pi\in(0,1)$ be the probability implied by an exogenous, commission-free betting market. The paper writes the odds parameter as

$$
\theta=\frac{\pi}{1-\pi}.
$$

Under its convention, a unit stake on outcome one pays a net gain $1/\theta$ if successful. Confusing that convention with quoted net odds reverses the sizing formula. A forecaster acting on report $p_i$ makes a net stake, as a fraction of initial wealth,

$$
\lambda_i=p_i-(1-p_i)\theta
=\frac{p_i-\pi}{1-\pi}.
$$

A negative $\lambda_i$ corresponds to taking the other side of the bet, with the equivalent stake adjusted by the reciprocal odds. The framework allows that two-sided implementation without commission or bookmaker overround.

The appendix on p. 74 supplies a direct derivation. Allocate fraction $u$ of wealth to the outcome-one claim and $1-u$ to the outcome-zero claim. The state wealths are $uW(1+1/\theta)$ and $(1-u)W(1+\theta)$. Expected log wealth has derivative $p_i/u-(1-p_i)/(1-u)$, giving $u=p_i$. Netting the opposing positions gives exactly $\lambda_i=p_i-(1-p_i)\theta$.

The resulting wealth multiplier is

$$
h_i(p_i;x,\pi)=
\begin{cases}
p_i/\pi,&x=1,\\
(1-p_i)/(1-\pi),&x=0.
\end{cases}
$$

Thus

$$
\log h_i=f_i(p_i;x)-[x\log\pi+(1-x)\log(1-\pi)].
$$

The second term is the same for all forecasters and independent of an individual report. Ordinary log score therefore measures potential Kelly log return up to a common state-dependent constant. Comparing two forecasters eliminates the market odds entirely:

$$
\log\frac{h_i}{h_j}=f_i-f_j.
$$

No observed market price is needed to compare those hypothetical Kelly performances. This remains a preference-specific economic interpretation: a decision-maker who uses forecasts to satisfy a liability constraint, minimize a different loss, or combine them with private information need not rank forecasters according to this payoff.

Let $H_i=(\prod_{j\ne i}h_j)^{1/(n-1)}$. The competitive score can be written

$$
G_i=\log h_i-\log H_i.
$$

It is the difference between the individual's log wealth multiplier and that of a geometric-average rival. The related outcome benchmarks are $q_i^1=(\prod_{j\ne i}p_j)^{1/(n-1)}$ and $q_i^0=(\prod_{j\ne i}(1-p_j))^{1/(n-1)}$. They are unnormalized geometric pools and generally do not sum to one. Renormalizing them changes score levels and is not part of the printed definition. Because they omit $i$'s report, however, neither benchmark creates own-report price impact.

## Wealth redistribution and the change in objective

Section 4.1 describes an alternative reward mechanism. Endow participants with total capital $B>0$, initially perhaps $W_i^0=B/n$, and after each outcome redistribute the same total according to their hypothetical Kelly gains:

$$
W_i^t=B\frac{h_i^tW_i^{t-1}}{\sum_j h_j^tW_j^{t-1}}.
$$

The common market-probability factor cancels. If outcome one occurs, this is $Bp_i^tW_i^{t-1}/\sum_jp_j^tW_j^{t-1}$; for outcome zero, replace each report by its complement. The update conserves $\sum_iW_i^t=B$ exactly. It resembles multiplicative forecast weighting and exposes an important difference from additive competitive scores: an individual's own report enters the normalizing denominator.

The paper describes long-run honesty under this wealth reward as effectively proper. That discussion requires care when implementing a finite tournament. Maximizing expected terminal monetary wealth is not identical to maximizing expected log wealth, and normalization creates endogenous price impact. For one round with equal capital, the normalized update is precisely the parimutuel wealth multiplier developed next, whose log score the paper explicitly shows is improper. The finite-round payout cannot be declared strictly proper by appealing to the fixed-odds Kelly derivation alone.

Repeated wealth selection can favor accurate beliefs under additional assumptions about outcomes, available strategies, and preferences. The supplied article does not provide a general finite-horizon incentive theorem for the normalized terminal payment or prove a unique honest report from expected terminal wealth maximization. These are limits of that interpretation, not a defect in the algebraic capital-conservation identity. A reproduction should specify whether the objective is expected score, expected log capital, or expected terminal currency; those objectives are different games.

## Endogenous parimutuel clearing

Now place all participants in one closed, zero-commission betting market. Given current capital $W_i$ and report $p_i$, each submits the Kelly net stake at the clearing odds. Market clearing requires

$$
\sum_i[p_i-(1-p_i)\theta_k]W_i=0.
$$

Solving for the implied probability gives

$$
\pi_k=\frac{\theta_k}{1+\theta_k}
=\frac{\sum_iW_ip_i}{\sum_iW_i}.
$$

The market consensus is a wealth-weighted arithmetic mean. With equal endowments, or deliberate equalization of forecaster influence, it is $\bar p=n^{-1}\sum_ip_i$. This differs from the unnormalized geometric rival benchmark in $G_i$.

For equal capital, the parimutuel Kelly score is

$$
w_i(p_1,\ldots,p_n;x)=
\begin{cases}
\log p_i-\log\bar p,&x=1,\\
\log(1-p_i)-\log(1-\bar p),&x=0.
\end{cases}
$$

This is equation (10), p. 71. It is the log of actual wealth redistribution in the closed Kelly market. Wealth, rather than the sum of log scores, is conserved. For example, after outcome one, equal-capital wealth multipliers sum to $\sum_i p_i/\bar p=n$, but generally $\sum_iw_i\ne0$. Jensen's inequality instead gives a nonpositive sum of those log multipliers. That distinction prevents an implementation from mistakenly forcing the parimutuel log scores to satisfy the additive zero-sum identity of the Kilgour–Gerchak scores.

The report influences both numerator and price denominator. A report farther from consensus offers a potentially valuable directional bet, but simultaneously pushes the consensus toward the participant and reduces the available edge. The rational report generally balances these effects by moving toward the rivals' average.

## Exact conditional best response

Fix participant $i$'s true belief $s=s_i$, rival average

$$
A=\frac1{n-1}\sum_{j\ne i}p_j,
$$

and write $p$ for the chosen report. For $A,s\in(0,1)$ the expected parimutuel score is

$$
L(p)=s\log\frac{np}{(n-1)A+p}
+(1-s)\log\frac{n(1-p)}{(n-1)(1-A)+1-p}.
$$

This is the source's equation (12). Its derivative is

$$
L'(p)=s\left[\frac1p-\frac1{(n-1)A+p}\right]
+(1-s)\left[-\frac1{1-p}
+\frac1{(n-1)(1-A)+1-p}\right].
$$

Each state log ratio is strictly concave for an interior rival average, so $L$ is strictly concave, its derivative diverges with opposite signs at the endpoints, and the unique interior root is the maximizing report. At $p=s$, the derivative need not vanish. Thus the rule is not strictly proper even for an agent whose objective is exactly the expected parimutuel log score.

For a stable reconstruction of equation (13), define

$$
K=A+s-1,\quad
J=A[2s+(n-1)(1-A)],\quad
C=sA[n-(n-1)A].
$$

Clearing positive denominators reduces the first-order condition to

$$
Kp^2-Jp+C=0.
$$

The admissible root can be calculated as

$$
p^+=\frac{2C}{J+\sqrt{J^2-4KC}}.
$$

This is a rationalized form of the source's expression and avoids subtracting nearly equal numbers. When $K=0$, the polynomial is linear and $p^+=C/J$; the rationalized form has the same limit. The printed equation (13) divides by $2(A+s-1)$, so using it literally without this branch produces an apparent $0/0$ when $A+s=1$. The underlying optimization is regular there. Bisection on the displayed derivative is an equally transparent implementation and supplies a useful independent check.

The root lies between $A$ and $s$. As $n$ grows with both fixed away from the boundary, each individual's influence on the mean vanishes and $p^+\to s$. A first-order expansion derived from the derivative makes the rate explicit:

$$
p^+-s=\frac{(A-s)s(1-s)}{nA(1-A)}+O(n^{-2}).
$$

The sign is toward consensus. This expansion is not uniform as $A$ approaches zero or one; its denominator also explains why a large headcount alone does not ensure negligible distortion in a nearly unanimous market.

The derivation conditions on a fixed rival average. If an agent is uncertain about rivals' reports, the correct objective averages $L(p;A)$ over the agent's distribution for $A$. Substituting the mean of $A$ inside the logarithms is generally not equivalent. The article's conditional calculations should not be promoted to a solution of every Bayesian reporting game.

## Figure 1 and reproducible numerical results

Figure 1, p. 72, sets $A=0.2$ and $s=0.6$ and compares $n=2,5,100$. It plots expected log utility against the report. The text gives approximate optima of 0.45, 0.5, and 0.6. Direct evaluation of the displayed equations gives:

| Participants $n$ | Optimal report $p^+$ | Expected score at $p^+$ | Expected score at honest report 0.6 |
|---:|---:|---:|---:|
| 2 | 0.442221 | 0.113416 | 0.081093 |
| 5 | 0.512932 | 0.235840 | 0.222169 |
| 100 | 0.594117 | 0.372104 | 0.372032 |

These additional digits are recalculations, not precision claimed by the plotted figure. Scores use natural logarithms and unit initial wealth. There is no sampling error: this is a deterministic evaluation of a specified subjective expectation. For $n=20$, $A=0.1$, and honest belief $s=0.8$, the source reports $p^+=0.745$; recalculation gives approximately 0.744677.

A reproducing program needs only a probability grid, $n,A,s$, and the formula for $L$. Evaluate the objective for interior reports, solve its derivative, verify that the reported maximum lies in $[\min(A,s),\max(A,s)]$, and compare it with the direct quadratic root. Report bounds should be explicit. Clipping to $[\epsilon,1-\epsilon]$ is a practical protocol change, not something silently supplied by the analytical model.

The boundary example on p. 73 is strategically important. If all rivals report zero and the agent assigns positive probability to outcome one, then for any own report $p>0$ the outcome-one multiplier is $n$. Making $p$ arbitrarily small leaves that upside unchanged while making the outcome-zero multiplier $(1-p)/(1-p/n)$ approach one. The best response is therefore the smallest admissible positive report, or a limiting supremum if the report set has no minimum. It is far from honest reporting even for a large population. The symmetric result holds when all rivals report one.

## Interpreting the equilibrium claim

The paper describes near honesty as a Nash-equilibrium strategy under realistic conditions. Its calculations establish a precise conditional best-response property: for many equally influential participants and an interior rival consensus, the optimal report is close to the true belief. They do not establish that truthful reporting is an exact finite-$n$ Nash equilibrium for heterogeneous beliefs. An exact equilibrium would require all reports simultaneously to satisfy their best-response equations, with each rival average generated by those reports.

Likewise, the large-$n$ conclusion relies on small individual influence. With unequal wealth, the relevant issue is a participant's capital share, not merely the number of names in the pool. A dominant account can have appreciable effect on $\pi_k$ even with many small rivals. Extending equation (13) to unequal wealth requires deriving the corresponding own-weight derivative; it is not justified by substituting an informal effective headcount.

The practical distinction is between eliciting beliefs and evaluating a specified economic action. Fixed-benchmark log scoring is strictly proper for expected-score maximizers. Competitive subtraction of other participants' scores preserves that property. Endogenous parimutuel pricing produces an interpretable trading game and an explicit shading incentive. Choosing among them requires deciding whether honest probabilities, relative statistical skill, or wealth in a closed betting market is the intended output. The paper supplies equations for those distinctions; it does not make their objectives interchangeable.
