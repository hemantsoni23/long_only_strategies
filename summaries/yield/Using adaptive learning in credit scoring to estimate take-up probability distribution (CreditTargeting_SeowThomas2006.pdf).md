# Using adaptive learning in credit scoring to estimate take-up probability distribution

Hsin-Vonn Seow and Lyn C. Thomas. *European Journal of Operational Research* 173 (2006), 880–892. DOI: 10.1016/j.ejor.2005.06.058. Accepted June 9, 2005; available online November 15, 2005.

Source: [original PDF](../../Finance/CreditTargeting_SeowThomas2006.pdf). All 13 pages were read, including every theorem, numerical table, and reference. The equations and tables on printed pages 882–891 were checked visually. The discussion below distinguishes the printed model, a coherent interpretation under richer feedback, and derivations needed if only the actual offer’s acceptance or rejection is observed.

## Why this matters

A lender can correctly identify a creditworthy customer and still earn nothing if the customer declines the offered terms. Conversely, a highly attractive product may win acceptance but earn little per accepted account. Optimal targeting therefore concerns expected profit, acceptance uncertainty, and the information gained by making an offer. The paper treats data collection as a decision: the product offered today determines both current revenue and what the lender learns for future customers.

Its distinctive structure is an ordered menu. More attractive products have higher acceptance probabilities but lower profit per acceptance. Acceptance or rejection is linked across products, so the offers are not independent arms of a conventional bandit. The paper proposes a Bayesian dynamic program, derives threshold properties for a reduced recursion, and gives small numerical examples. It does not estimate a model from a real credit-card campaign or demonstrate realized profit improvements.

Two issues limit direct implementation. The initial Bellman equation treats different latent reasons for rejecting an offer as if they generated separately observed posterior states. A binary response alone does not reveal those reasons. The subsequent simplification deletes a common continuation term and replaces the future value function, claiming that an action-independent cost preserves the optimal policy. A common term can be removed from a one-step maximization while holding continuation values fixed; that fact alone does not justify the recursive substitution. These are distinct issues, beyond several local typographical errors in the formulas.

The paper remains useful as a formulation of learning while pricing, but its compact Beta-state recursion should not be presented as an established optimal policy for ordinary binary acceptance data without additional assumptions or a repaired argument.

## Products, horizon, and rewards

Let products be indexed $k=1,\ldots,K$, ordered from most attractive to least attractive to the customer. The assumed acceptance probabilities and profits per accepted offer satisfy

$$
p_1\geq p_2\geq\cdots\geq p_K,
\qquad 0\leq P_1\leq P_2\leq\cdots\leq P_K.
$$

The paper motivates this with credit-card interest rates, limits, fees, introductory terms, and ancillary benefits. The ordering assumption is much stronger than saying that average take-up falls with price: for a given customer, rejecting a more attractive offer implies rejecting all less attractive offers, and accepting a less attractive offer implies accepting all more attractive offers. Multiple product features need not admit such a universal ordering in practice.

Customers are homogeneous, with a fixed population acceptance structure. There is no arrival-specific covariate, evolving macro state, competition response, or drift in preferences. The number of remaining customers is geometrically distributed. After the current customer there is another with probability $\beta$, where $0<\beta<1$. This is equivalent to geometric discounting across successive customer decisions:

$$
V^\pi=E^\pi\left[\sum_{t=0}^{\infty}\beta^t P_{a_t}Y_t\right].
$$

The current customer is included, so the expected customer count is $1/(1-\beta)$. Values are total expected profit over that random horizon, not automatically profit per applicant. At $\beta=.5$, the expected count is two; at $\beta=.999$, it is 1,000.

Profit $P_k$ is treated as known and received when the customer accepts. The model contains no explicit PD, loss given default, funding cost, balance dynamics, credit-limit utilization, customer attrition, or delayed profit realization. If $P_k$ is to mean net lifetime account value, all those components must be estimated outside this model. The source does not do so. Nor does it model acceptance-induced changes in borrower risk: customers accepting a more expensive offer can be a selected risk pool even when the unconditional applicant population is homogeneous.

If the acceptance probabilities were known, one would simply choose $\arg\max_k p_kP_k$. Under uncertainty, the policy can sacrifice immediate expected reward to learn which product will be profitable later. Immediate responses are assumed available before the next decision; delayed or missing responses would require a different state.

## Conditional probabilities and Beta notation

For two offers, define

$$
q_1=p_1,
\qquad q_2=P(\text{would accept 2}\mid\text{would accept 1}),
\qquad p_2=q_1q_2.
$$

For $K$ offers, $p_k=\prod_{j=1}^{k}q_j$. This parameterization enforces ordered marginal acceptance probabilities when each $q_j\in[0,1]$.

The paper writes $B(r_j,n_j)$ for a Beta distribution whose shape parameters in conventional notation are $r_j$ and $n_j-r_j$:

$$
f_j(q)=\frac{q^{r_j-1}(1-q)^{n_j-r_j-1}}{B(r_j,n_j-r_j)},
\qquad E[q_j]=\frac{r_j}{n_j}.
$$

Thus $n_j$ is total prior precision, not the second Beta shape parameter. A proper prior requires $0<r_j<n_j$. The numerical tables include $r_j=0$ and $r_j=n_j$; these should be interpreted as degenerate endpoint beliefs, not proper Beta densities with a zero shape parameter. The text calls the $q_j$ Bernoulli variables, but they are Bernoulli *probability parameters*; individual acceptance-stage outcomes are the Bernoulli variables.

The compact model also needs independent prior factors for the $q_j$ to replace $E[q_1q_2]$ by $(r_1/n_1)(r_2/n_2)$. The factorized Beta description and the displayed products imply that modeling choice, although the independence assumption is not separately emphasized.

For an observed Bernoulli success at stage $j$, $(r_j,n_j)$ becomes $(r_j+1,n_j+1)$; for an observed failure it becomes $(r_j,n_j+1)$. Acceptance of offer 2 reveals success at both stages under the nesting assumption. Rejection of offer 1 reveals failure at stage 1. Rejection of offer 2, however, does not reveal whether stage 1 failed or stage 1 succeeded and stage 2 failed. This is the essential information distinction.

## The printed two-offer Bellman equation

Let $s=(r_1,n_1,r_2,n_2)$, $a=r_1/n_1$, and $b=r_2/n_2$. Define successor states

$$
s_{1+}=(r_1+1,n_1+1,r_2,n_2),\qquad
s_{1-}=(r_1,n_1+1,r_2,n_2),
$$

$$
s_{++}=(r_1+1,n_1+1,r_2+1,n_2+1),\qquad
s_{+-}=(r_1+1,n_1+1,r_2,n_2+1).
$$

Equation (1), printed p. 883, is

$$
V(s)=\max\left\{
 aP_1+\beta[aV(s_{1+})+(1-a)V(s_{1-})],
 abP_2+\beta[abV(s_{++})+a(1-b)V(s_{+-})+(1-a)V(s_{1-})]
\right\}.
$$

The second action has three branches: acceptance, rejection at the second stage after first-stage success, and rejection at the first stage. This is a valid recursion for an augmented-feedback model in which the first failed stage is actually revealed. An offer experiment that observes a reservation threshold or obtains additional reliable responses to the more attractive variants could potentially generate such information. The source’s motivating binary offer process does not specify that extra observation.

If the lender sees only “offer 2 rejected,” its posterior density is instead

$$
f^-(q_1,q_2)=\frac{(1-q_1q_2)f_1(q_1)f_2(q_2)}{1-ab}.
$$

Using $1-q_1q_2=(1-q_1)+q_1(1-q_2)$ shows that this posterior is a mixture of the two Beta-product successor beliefs:

$$
f^-=\frac{1-a}{1-ab}f_{1-}
+\frac{a(1-b)}{1-ab}f_{+-}.
$$

The lender can calculate those mixture weights but does not observe which component generated the rejection. Its next action must be chosen using the mixture, not separately optimized conditional on an unobserved branch. Averaging optimized future values over the branches generally confers the value of extra information. The correct binary-feedback continuation is $(1-ab)V(f^-)$, not $(1-a)V(f_{1-})+a(1-b)V(f_{+-})$.

The distinction appears even with independent uniform priors. Then $a=b=1/2$, the rejection weights are $2/3$ and $1/3$, and direct integration gives

$$
E[q_1\mid\text{reject 2}]=E[q_2\mid\text{reject 2}]=\frac49,
\qquad E[q_1q_2\mid\text{reject 2}]=\frac5{27}.
$$

Their posterior covariance is $5/27-(4/9)^2=-1/81$. This derived example demonstrates that binary feedback destroys the independent-Beta state family. Updating both marginal means and multiplying them would produce the wrong next-offer acceptance probability. Repeated rejections require a joint density, a mixture representation, or a controlled approximation.

## The reduction and its evidence boundary

Section 3 introduces a state-dependent “fee” equal to $\beta(1-a)V(s_{1-})$, common to both current actions. It then writes a modified recursion

$$
\widetilde V(s)=a\beta\max\left\{
B_1+\widetilde V(s_{1+}),
 bB_2+b\widetilde V(s_{++})+(1-b)\widetilde V(s_{+-})
\right\},
\qquad B_k=P_k/\beta.
$$

Removing the common term from the two action values in equation (1) does preserve their immediate ordering when the original $V$ at future states is held fixed. But equation (2) goes further: it replaces future $V$ by $\widetilde V$ and deletes the failure continuation recursively. A state-dependent fee changes the desirability of future states, so action independence at the current state does not by itself establish policy equivalence. The paper provides no transformation of the full value function that makes that substitution follow algebraically.

Equation (2) is nevertheless a well-defined reduced control problem. It can be interpreted as removing continuation after a first-stage failure, while updating $q_1$ only along surviving first-stage-success paths. Its policy properties can be analyzed on that basis. The issue is transferring those properties to equation (1), and then transferring equation (1) to the binary-feedback offer problem. Those are two separate claims requiring justification.

Starting from $(R_1,N_1)$, the reduced recursion advances the first pair deterministically to $(R_1+s,N_1+s)$. Set

$$
\beta_s=\beta\frac{R_1+s}{N_1+s},
\qquad W_s(r,n)=\widetilde V(R_1+s,N_1+s,r,n).
$$

It satisfies

$$
W_s(r,n)=\beta_s\max\left\{
B_1+W_{s+1}(r,n),
\frac rn B_2+\frac rn W_{s+1}(r+1,n+1)
+\left(1-\frac rn\right)W_{s+1}(r,n+1)
\right\}.
$$

This is a practical way to compute the reduced problem without storing all four state dimensions. The index $s$ counts the success-path increments in that recursion. It should not be identified uncritically with the count of all actual offers in the original model, since real offers can fail at stage 1.

Starting value iteration at zero gives nonnegative iterates. With nonnegative rewards bounded by $P_2$, a safe total-value bound is $P_2/(1-\beta)$. The bound printed in Lemma 1, $B_2/\beta$, is not generally valid as $\beta$ approaches one. The usual discounted bounded-reward argument supplies the needed convergence bound without relying on that expression.

## Threshold arguments and local printed errors

Lemma 1 asserts that the reduced value is nondecreasing in $r$ and $s$ and nonincreasing in $n$ when the other arguments are fixed. The intuition is specific: increasing $r$ at fixed $n$ improves the second-stage acceptance belief; increasing $n$ at fixed $r$ lowers it; increasing $s$ raises $\beta_s$ toward $\beta$. It is not a theorem that “more data always raises value” under arbitrary changes in Beta parameters.

As $s\to\infty$, $\beta_s\to\beta$. This limit corresponds to $q_1$ becoming concentrated at one along the all-success path, not to learning an arbitrary fixed $q_1$. The reduced limiting problem has one safe alternative, offer 1, which leaves $(r,n)$ unchanged, and one learning alternative, offer 2.

If offer 1 is optimal at a limiting state, repeating it has value

$$
W_\infty(r,n)=\frac{\beta B_1}{1-\beta}=\frac{P_1}{1-\beta}.
$$

Monotonicity in $r$ implies that the set attaining this floor is an initial interval in $r$, yielding a threshold $r^*(n)$. Above it, experimenting with offer 2 has positive value. The threshold is nondecreasing in $n$ at fixed success count. The presentation of the proof mixes the safe action’s bracketed value with the discounted value, but the constant-floor argument can be stated coherently as above for the reduced limiting problem.

For finite $s$, define the excess value over the always-offer-1 baseline:

$$
D_s(r,n)=W_s(r,n)-W_s(0,n).
$$

Subtracting that baseline from the reduced recursion gives

$$
D_s(r,n)=\beta_s\max\left\{
D_{s+1}(r,n),
\frac rn B_2-B_1+\frac rn D_{s+1}(r+1,n+1)
+\left(1-\frac rn\right)D_{s+1}(r,n+1)
\right\}.
$$

Printed p. 885 instead has $(r/n)B_1-B_2$. The displayed expression above is a direct derived correction: the uncertain offer earns $B_2$ on success and the subtracted safe baseline earns $B_1$.

Theorem 2 describes a region where offer 1 is used forever and a complementary region where offer 2 is used for at least one future customer. The proof compares $D_s$ with its limiting value and uses positive products of future discount factors to transfer a strictly positive limiting advantage back to finite $s$. The printed inequality for the sufficiently large time index is reversed; convergence requires times beyond a sufficiently large threshold.

The corollary states that offer 2 is immediately optimal when $r/n>B_1/B_2=P_1/P_2$. Its exchange argument moves a profitable experiment ahead of a string of safe offers. The immediate-profit difference needed there is again $(r/n)B_2-B_1$; the proof prints the factors in the wrong order. The experimental section on p. 887 also prints the myopic inequality backwards. The coherent myopic rule is offer 2 when $(r/n)P_2>P_1$.

Crucially, the authors do not prove the complete finite-$s$ threshold policy for the intermediate region between the never-experiment boundary and the myopic boundary. They explicitly conjecture a function $r^*(s,n)$ and assume that form when presenting their numerical calculations. The note therefore does not promote that conjecture into a theorem, even within the reduced model.

## Numerical examples and what can be reproduced

There is no available campaign data in the paper. Numerical examples solve the stated model rather than estimating probabilities from realized credit applications. The authors use upper and lower value-function bounds attributed to MacQueen and Porteus to stop calculations, but do not give the tolerance, state truncation, software, or code. Prior parameters and reward examples are supplied; no standard errors are relevant to deterministic value tables unless numerical approximation error is quantified, which it is not.

Table 1 uses $P_1=10$, $P_2=25$, $\beta=.5$, and $(r_1,n_1)=(6,16)$. It reports the modified, fee-adjusted values, denominated in pounds:

| $(r_2,n_2)$ | Reported value | Offer |
|---|---:|---:|
| $(0\text{–}1,3)$ | 4.7481 | 1 |
| $(2,3)$ | 7.9144 | 2 |
| $(3,3)$ | 11.8702 | 2 |
| $(0\text{–}9,24)$ | 4.7481 | 1 |
| $(10,24)$ | 4.9490 | 2 |
| $(11,24)$ | 5.4406 | 2 |
| $(12,24)$ | 5.9351 | 2 |
| $(13,24)$ | 6.4297 | 2 |
| $(23,24)$ | 11.3757 | 2 |
| $(24,24)$ | 11.8702 | 2 |

These values are not actual undiscounted profit per applicant. For comparison, under the original fixed-population model the always-offer-1 policy has expected total value $P_1E[q_1]/(1-\beta)=10(6/16)/.5=7.5$, whereas the table’s modified safe value is 4.7481. That derived comparison illustrates the importance of the transformation; it is not a claim that the table incorrectly computes its own modified value.

The text also calls 12.5 the profit per applicant for independent uniform priors. It does not supply enough surrounding numerical detail to reconcile this phrase with the modified-value examples. Under $P_2=25$, $\beta=.5$, and uniform priors, 12.5 is the total expected reward of always offering product 2, since its immediate mean reward is 6.25. It should not be read as an empirically observed customer margin or automatically as a verified optimal value.

Tables 2–5 use $P_1=20$, $P_2=50$, and $\beta=.999$. The myopic acceptance threshold is $P_1/P_2=.4$. Tables 2 and 3 compare $(r_1,n_1)=(4,5)$ and $(16,20)$, both with mean .8, and report identical threshold schedules for the displayed $n_2\leq30$. Equality in those examples does not prove that only the mean matters.

Tables 4 and 5 give a counterexample within the reported calculations: priors $(2,3)$ and $(16,24)$ have the same mean $2/3$ but different precision. At $n_2=16$, the maximum $r_2$ still assigned to offer 1 is 5 for the first prior and 6 for the second. Thus the first offer-2 success counts are 6 and 7, matching the discussion of the switch. This distinguishes a threshold defined as the last safe count from a threshold defined as the first experimental count.

Table 6 fixes $n_1=24$ and varies $r_1$ across 1, 4, 8, 16, 22, 23, and 24. The nearby prose says the ratio $r_1/n_1$ is held fixed; the table plainly does not do that. Both its mean and uncertainty change. For example, at $n_2=10$, the reported last-offer-1 threshold falls from 3 for low $r_1$ to 2 for $r_1=23$ or 24. The table cannot isolate a pure effect of greater prior precision. The nearby verbal claim about becoming more willing to use offer 1 also needs care: lowering a last-offer-1 threshold expands the region choosing offer 2.

## More than two variants

For $K$ offers, the printed equation (4) branches according to the first failed conditional stage. Under actually observed first-failure feedback, define $m_j=r_j/n_j$, acceptance probability $A_k=\prod_{j=1}^k m_j$, and failure-branch probabilities

$$
F_l=\left(\prod_{j=1}^{l-1}m_j\right)(1-m_l),\qquad l\leq k.
$$

Then $A_k+\sum_{l=1}^{k}F_l=1$. Acceptance updates all first $k$ Beta factors as successes; first failure at $l$ updates earlier factors as successes, factor $l$ as failure, and leaves later factors unchanged. The coherent enriched-feedback recursion is

$$
V(s)=\max_k\left\{A_kP_k+\beta\left[A_kV(s^{k,+})+\sum_{l=1}^{k}F_lV(s^{l,-})\right]\right\}.
$$

Several indices and parentheses in the printed many-offer formulas are inconsistent, so implementing them verbatim is unsafe. Under binary feedback, rejection instead has likelihood $1-\prod_{j=1}^kq_j$ and again creates an unobserved mixture over these branches.

The later theorems propose nested boundaries separating always choosing the most attractive remaining variant from experimenting with less attractive variants. Their transfer to the original binary process inherits both the feedback issue and the unproved recursive reduction. The paper’s concise treatment does not supply a complete independently verified proof for every many-offer policy assertion.

Table 7 gives actual, non-fee-adjusted values for $P_1=20$, $P_2=50$, $P_3=80$, $(r_1,n_1)=(6,9)$, and $n_2=9,n_3=10$. With $r_2=4$, offer 2 is selected for $r_3=0$ through 6, with value 29.6296; offer 3 is selected at 7, 8, 9, and 10, with values 33.1852, 37.9259, 42.6667, and 47.4074. With $r_2=3$, offer 1 is selected through $r_3=7$, with value 26.6667; offer 3 is selected at 8, 9, and 10, with values 28.6933, 32.0000, and 35.5556. Table 7’s caption does not state $\beta$, so a reader should not silently import .999 from earlier tables. Several values are consistent with a .5 continuation rate under fixed-offer benchmarks, but that is an inference, not an explicitly reported parameter.

## An implementable binary-feedback formulation

A faithful operational model must first decide what feedback is available. If only the chosen offer’s response is observed, let $\mu$ be the current joint distribution of $q=(q_1,\ldots,q_K)$ and define

$$
A_k(\mu)=E_\mu\left[\prod_{j=1}^{k}q_j\right].
$$

Bayes updates multiply $\mu$ by $\prod_{j\leq k}q_j$ after acceptance or by $1-\prod_{j\leq k}q_j$ after rejection, followed by normalization. Denoting these posterior distributions by $T_k^+\mu$ and $T_k^-\mu$, the correct belief-state Bellman equation is

$$
V(\mu)=\max_k\left\{P_kA_k(\mu)+\beta\left[
A_k(\mu)V(T_k^+\mu)+(1-A_k(\mu))V(T_k^-\mu)
\right]\right\}.
$$

This is a derived repair of the observation model, not an algorithm tested in the source. A finite-grid or particle approximation can represent $\mu$, but introduces integration and approximation error absent from the paper’s simple state counts. A finite-horizon truncation at $H$ has reward-tail bound $P_K\beta^H/(1-\beta)$ for nonnegative bounded rewards. This gives a transparent numerical stopping target, although with $\beta=.999$ the horizon may need to be very large.

Benchmarks should include fixed offers and a myopic policy using the same joint posterior. A clairvoyant policy knowing the true $q$ supplies an upper benchmark; a policy receiving first-failure feedback solves a different information problem. Simulating both without labeling the information difference would overstate achievable learning gains. All such validation is proposed here, not reported empirical evidence.

The source ends by suggesting segmentation with distinct priors and profits, using applicant information to identify a segment. It does not estimate those segments or assess their sample size and stability. Its enduring idea is that a lender should choose data-generating actions with future profit in mind. Its numerical policies require considerably more qualification than the abstract suggests: ordered and stable preferences, a known reward model, immediate feedback, a specified horizon, and a posterior representation consistent with what the lender actually observes.
