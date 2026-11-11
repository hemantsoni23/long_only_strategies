# Is There a Positive Relationship between Stock Market Volatility and the Equity Premium?

**Chang-Jin Kim, James C. Morley, and Charles R. Nelson.** *Journal of Money, Credit and Banking* 36(3), Part 1 (June 2004), 339–360. Source: [VolatilityAnomaly_KimMorley_2004.pdf](../../Finance/VolatilityAnomaly_KimMorley_2004.pdf). The library copy contains the complete article, including the filtering appendix, plus a JSTOR cover sheet. Printed page numbers below refer to the article.

## Why this matters

A negative association between a month's return and its volatility need not mean that investors demand less compensation for bearing risk. An unexpected, persistent increase in required returns lowers today's price because it raises discount rates for future cash flows. The immediate capital loss and the higher expected return subsequently earned are different quantities. Mixing them can reverse the apparent sign of the risk–return relationship.

This paper makes that distinction estimable in a two-state model. It combines a present-value identity, Markov-switching dividend-news variance, and alternative assumptions about when investors learn the volatility state. Its useful contribution is an explicit connection between a volatility-feedback coefficient and the state-dependent expected-return premium. The empirical exercise also shows that assumptions about investors' information can be as consequential as the choice of volatility model.

The strongest evidence is for postwar U.S. monthly returns under the partial-revelation specification. The unrestricted feedback estimate is negative and precisely estimated; imposing the paper's pricing restriction produces a positive high-volatility premium without materially worsening fit. The full-revelation version has negative feedback too, but its pricing restriction is rejected. Accordingly, the results support a particular structural explanation rather than establish a universal, model-free positive risk–return relation.

## Economic model and notation

Let $r_t$ denote the continuously compounded market excess return during month $t$. The paper first develops the model for log returns and then applies it to excess returns. In that application, cash-flow news should be understood as dividend news relative to future interest rates. Let $S_t\in\{0,1\}$ be a latent volatility regime, with 0 denoting low volatility. Dividend-news innovations satisfy

$$
\varepsilon_t\mid S_t=j\sim N(0,\sigma_j^2),\qquad 0<\sigma_0<\sigma_1.
$$

The transition probabilities are $P(S_t=0\mid S_{t-1}=0)=q$ and $P(S_t=1\mid S_{t-1}=1)=p$. In row-previous, column-current order, the transition matrix is

$$
P=\begin{pmatrix}q&1-q\\1-p&p\end{pmatrix}.
$$

Write $\lambda=p+q-1$ for persistence. For an ergodic chain, the stationary high-volatility probability is $\pi_1=(1-q)/(2-p-q)$, and expected low- and high-state durations are $1/(1-q)$ and $1/(1-p)$ months. Persistence matters because news about the current state changes expected risk compensation for many subsequent months.

The partial-equilibrium expected-return assumption is

$$
E[r_{t+j}\mid\mathcal I_t]=\mu_0+\mu_1P(S_{t+j}=1\mid\mathcal I_t).
$$

Here $\mu_0$ is the expected return in a perfectly anticipated low state, and $\mu_1$ is the increment in a perfectly anticipated high state. The specification does not force the average premium and its marginal response to risk to have the same sign. A positive historical average return therefore does not mechanically imply $\mu_1>0$. Nor is $\mu_1$ itself a variance slope: the implied slope between the two news-variance levels would be $\mu_1/(\sigma_1^2-\sigma_0^2)$.

The model builds on the Campbell–Shiller log-linear present-value relation. Log prices reflect discounted future dividends and returns, with linearization parameter $\rho$, set to 0.997 in the restricted empirical specifications. Unexpected returns decompose into cash-flow news and revisions to future discount rates. The paper writes

$$
r_t=E[r_t\mid\mathcal I_{t-1}]+f_t+\varepsilon_t,
$$

where $f_t$ is the negative revision in discounted expected future returns. It distinguishes investors' end-of-period information before the final return is realized, $\mathcal I'_t$, from the larger information set including that return. This distinction is intended to avoid a mechanically circular causal explanation in which the return being modeled is also the contemporaneous explanatory variable.

The estimating equation, Eq. (7), is

$$
r_t=\mu_0+\mu_1a_t+\delta(b_t-a_t)+\varepsilon_t,
\qquad
 a_t=P(S_t=1\mid\mathcal I_{t-1}),\quad
 b_t=P(S_t=1\mid\mathcal I'_t).
$$

A positive revision $b_t-a_t$ means that investors have learned the high-risk state is more likely. A negative $\delta$ converts this news into an immediate price decline. State-dependent news variance and feedback are distinct: $\sigma_j^2$ is not simply the unconditional variance of observed returns within an estimated regime, because return means also depend on state transitions and information revisions.

## The printed pricing restriction and a derivation qualification

The paper imposes the following restriction in its constrained estimates:

$$
\delta=-\frac{\mu_1}{1-\rho\lambda}.
$$

This is the restriction printed in Eqs. (6)–(7) and the notes to Tables 3–4. To reproduce those tables, it should be implemented as printed. With persistent regimes, negative feedback then translates into a positive expected-return increment.

There is, however, an indexing inconsistency in the preceding derivation. On p. 343, the feedback definition uses revisions of $\sum_{j=1}^{\infty}\rho^j r_{t+j}$, and Eq. (3′) gives the state-dependent component of the $j$-ahead expectation as $\mu_1\lambda^j(P(S_t=1\mid\mathcal I_t)-\pi_1)$. Summing those displayed expressions literally yields

$$
\sum_{j=1}^{\infty}(\rho\lambda)^j
=\frac{\rho\lambda}{1-\rho\lambda},
$$

so the corresponding coefficient would be $-\mu_1\rho\lambda/(1-\rho\lambda)$, rather than the printed $-\mu_1/(1-\rho\lambda)$. The constant terms in Eq. (5) similarly omit the leading $\rho$ implied by a sum beginning at one. This is a source inconsistency, not an alternative empirical result demonstrated in the article. The sign argument survives when $\rho\lambda>0$, but the exact mapping from feedback magnitude to risk premium changes. A replication should keep the authors' specification and an index-consistent alternative in separate runs; silently correcting the coefficient would no longer reproduce the reported restricted estimates.

This qualification also prevents treating the relation as an exact present-value theorem without specifying the indexing convention. The underlying present-value relation is itself a log-linear approximation, although the paper cites prior evidence that its approximation error is small for these monthly U.S. data.

## Five information structures

The same return equation generates five economically different specifications (pp. 344–345).

1. **No reaction to regime information.** Set $\mu_1=\delta=0$. Returns have a constant mean but may still have regime-dependent variance. This establishes whether switching is needed before allowing a changing expected return.
2. **Past returns only, no intra-month updating.** Investors use the econometrician's filtered information. Both $a_t$ and $b_t$ equal the predicted high-state probability, so feedback vanishes. Conditional expected returns can still vary through $a_t$.
3. **Current state known throughout the month.** Both probabilities equal $S_t$. The observation mean is $\mu_0+\mu_1S_t$, again without feedback. A negative estimated state-mean increment in this specification can reflect omitted repricing at state changes.
4. **Partial revelation.** The prior is based on past returns, while the end-of-period information is proxied by the current state: $a_t=P(S_t=1\mid r_{1:t-1})$ and $b_t=S_t$. The source calls this partial revelation because the true state proxies information acquired through trading, rather than claiming that investors literally observe the econometrician's state variable without error. That proxy introduces measurement error. The model nests past-returns-only information at $\delta=0$, and current-state-known information at $\mu_1=\delta$.
5. **Full revelation.** Investors know $S_{t-1}$ at the start and $S_t$ at the end. For a transition from $i$ to $j$, the prior is $a_i=1-q$ if $i=0$ and $a_i=p$ if $i=1$, while $b_t=j$. The conditional mean is $\mu_0+\mu_1a_i+\delta(j-a_i)$. The econometrician still does not observe those states and must integrate over them. This version nests the current-state-known specification at $\mu_1=\delta$, but does not nest the past-returns-only model generally.

The distinction between investor knowledge and econometrician knowledge is essential. Using smoothed probabilities as if they were contemporaneously observed signals would both alter the likelihood and introduce future information into an investment implementation. Smoothing is used here for historical interpretation and diagnostics, not to create a real-time trading signal.

## Data and estimation design

The data are CRSP total monthly returns on the value-weighted portfolio of all NYSE-listed stocks, including dividends, less the continuously compounded one-month U.S. Treasury-bill return. Each simple gross return is logged before subtraction. The full period is January 1926–December 2000. The authors estimate January 1926–December 1951 and January 1952–December 2000 separately: 312 and 588 calendar months respectively. The split corresponds to the Fed–Treasury Accord and an earlier literature convention. It is deliberately imposed rather than estimated as a break date.

The stated reason is to distinguish recurring high/low regimes from a one-time structural shift in the volatility process. The long absence of high-volatility episodes during the 1940s and 1950s makes the exact date of the underlying change difficult to identify. These are historical in-sample likelihood exercises, not an out-of-sample forecast comparison. There are no portfolio weights, trading-cost assumptions, rebalancing rules, or net investment returns to reproduce.

Maximum likelihood uses GAUSS OPTMUM, numerical derivatives, appropriate constraints including nonnegative variances, and several initial values. The authors report asymptotic standard errors calculated numerically. A reproducible modern implementation should enforce state ordering and keep $p,q$ strictly between zero and one, but the source does not publish optimization tolerances, the complete initial-value grid, source code, or the CRSP data extract. Those implementation choices must be declared rather than attributed to the paper.

For clarity, the appendix's filter can be written without ambiguous state indices. Let $w_{t-1,i}=P(S_{t-1}=i\mid r_{1:t-1})$. For each transition, compute

$$
\xi_{t,ij}=w_{t-1,i}P_{ij},\qquad
 g_{t,ij}=\frac{1}{\sigma_j}\phi\!\left(\frac{r_t-m_{t,ij}}{\sigma_j}\right),
$$

where $m_{t,ij}$ is the mean implied by the selected information structure. In the partial-revelation case, first calculate $a_t=\sum_i\xi_{t,i1}$ and use $m_{t,ij}=\mu_0+\mu_1a_t+\delta(j-a_t)$. In the full-revelation case, use the state-specific $a_i$ above. The predictive density and filter update are

$$
 f_t=\sum_{i,j}\xi_{t,ij}g_{t,ij},\qquad
 w_{t,j}=\frac{\sum_i\xi_{t,ij}g_{t,ij}}{f_t}.
$$

Initialize with $w_{0,0}=(1-p)/(2-p-q)$ and $w_{0,1}=(1-q)/(2-p-q)$, then maximize $\sum_t\log f_t$. For a constrained run, recompute $\delta$ from the current trial values of $\mu_1,p,q$ and fixed $\rho=0.997$ inside every likelihood evaluation. Estimating an unrestricted model and subsequently substituting a constrained coefficient is not equivalent.

For backward smoothing, Appendix Eq. (A8) prints the following joint-state recursion:

$$
 P(S_t=j,S_{t+1}=\ell\mid r_{1:T})
 =w_{t,j}P_{j\ell}\frac{P(S_{t+1}=\ell\mid r_{1:T})}
 {P(S_{t+1}=\ell\mid r_{1:t})},
$$

Summing over $\ell$ gives $P(S_t=j\mid r_{1:T})$; Appendix Eq. (A9) prints an inconsistent left-hand state/time index for that marginalization. The recursion above is exact when the next observation depends on the next regime alone, conditional on known past observations. This includes the partial-revelation specification. However, the full-revelation observation mean depends on both consecutive states, so that simplification generally discards information in $r_{t+1}$ about $S_t$.

For an exact smoother with transition-dependent emissions, use instead

$$
P(S_t=j,S_{t+1}=\ell\mid r_{1:T})
=\frac{w_{t,j}P_{j\ell}g_{t+1,j\ell}}
{\sum_i w_{t,i}P_{i\ell}g_{t+1,i\ell}}
P(S_{t+1}=\ell\mid r_{1:T}).
$$

Here $g$ is the transition-specific observation density already used in the forward likelihood. This formula is a reconstruction from Bayes' rule; it is not the formula printed in the source. When $g_{t+1,j\ell}$ is independent of $j$, it cancels and recovers the printed expression. The qualification concerns historical probabilities and diagnostics using them; it does not change the forward likelihood recursion or itself demonstrate how the authors' unpublished smoothing code behaved.

## What the baseline models establish

Table 1 first keeps the mean constant. Allowing independent variance switching rather than constant variance raises twice the log likelihood by 86.39 before 1952 and 37.69 afterward. Those tests have nonstandard distributions because a regime probability is unidentified under constant variance. Large statistics alone do not justify applying a conventional chi-square critical value to that comparison.

Conditional on switching, the independence restriction $p=1-q$ is rejected against Markov persistence: likelihood-ratio statistics are 59.49 and 10.68, both reported with $p<0.01$ under the one-degree-of-freedom comparison. The fitted high-state monthly standard deviation falls from 0.12087 prewar to 0.07454 postwar, while high-state persistence falls from 0.96051 to 0.71091. The associated expected durations are approximately 25.3 and 3.5 months. Low-state standard deviations are 0.03929 and 0.03390.

The simple mean specifications do not settle the risk–return question. Under past-returns-only information, allowing a changing mean gives likelihood-ratio statistics of 0.78 ($p=0.38$) and 5.26 ($p=0.02$). Under current-state-known information, the statistics are 4.74 ($p=0.03$) and 7.89 ($p<0.01$), but the estimated high-state mean increments are negative: −0.02820 and −0.03135 per month. The experiment is useful precisely because those negative coefficients arise before feedback is modeled.

## Main estimates and restrictions

The following values are monthly decimal log-return units; the standard errors in parentheses apply to the reported coefficients. Tables 3–4 provide the remaining variance and transition estimates.

| Information and period | Unrestricted $\mu_1$ | Unrestricted $\delta$ | Restricted $\mu_1$ | Restricted $\delta$ |
|---|---:|---:|---:|---:|
| Partial, 1926–1951 | −0.02308 (0.01402) | −0.04014 (0.01809) | 0.00161 (0.00146) | −0.02657 (0.01718) |
| Partial, 1952–2000 | 0.00374 (0.00708) | −0.05549 (0.00783) | 0.00665 (0.00199) | −0.05361 (0.00631) |
| Full, 1926–1951 | −0.02265 (0.01446) | −0.10623 (0.03457) | 0.00613 (0.00367) | −0.08546 (0.03026) |
| Full, 1952–2000 | −0.00673 (0.00888) | −0.08518 (0.01373) | 0.01541 (0.00829) | −0.06670 (0.01594) |

All four unrestricted feedback estimates are negative and statistically significant by the reported asymptotic $t$ statistics: −2.23, −7.09, −3.07, and −6.20. But their corresponding contemporaneous premium increments are usually negative and much less precisely estimated. The economic restriction transfers information from the relatively precise feedback estimate to the weakly identified direct premium increment.

For the partial-revelation postwar model, the unrestricted and restricted log likelihoods are 1080.47246 and 1080.38524. The restriction costs only 0.17 likelihood-ratio units, with reported $p=0.68$. The restricted low-state mean is 0.00444, the high-state increment 0.00665, low/high news standard deviations 0.03190/0.05437, and transition probabilities $q=0.97217$, $p=0.90638$. These provide a compact numerical target for reproducing the most supportive specification.

The partial-revelation prewar restriction is less comfortable: the statistic is 3.21, $p=0.07$, and the positive constrained $\mu_1$ has a $t$ statistic of only 1.10. Under full revelation, the restriction is rejected with statistics 3.95 ($p=0.05$) and 6.55 ($p=0.01$). Full knowledge of the preceding and current regimes therefore does not produce an unambiguously successful structural model, despite negative feedback coefficients. The authors suggest investors may observe the regime with error.

Model nesting matters for other tests too. Partial revelation versus the past-return benchmark tests $\delta=0$, producing statistics 4.83 and 23.50. Comparison with the current-state-known benchmark tests $\mu_1-\delta=0$, producing 0.87 and 20.87. The full-revelation/current-state-known comparisons produce 2.44 and 15.60. Thus evidence that feedback is needed beyond the better no-feedback benchmark is substantially stronger after 1951.

## Economic magnitudes, diagnostics, and interpretation

Using the printed constrained full-revelation model, the authors annualize perfectly anticipated low/high state premiums to 12.4%/20.9% before 1952 and 5.1%/26.2% afterward. These are model-implied state-conditioned premiums, not average realized trading returns. The conversion is consistent with exponentiating twelve times a monthly log mean. For instance, the postwar means are 0.00417 and $0.00417+0.01541$.

The corresponding stationary annualized premiums are 14.3% and 8.2%, versus annualized sample-average excess returns of 6.4% and 6.6%. The prewar gap is attributed to a few large negative repricing events, including the 1929 crash. That interpretation is conditional on the model's division of return innovations into exogenous volatility news and feedback. The full-revelation restriction underlying these striking magnitudes is rejected, so these particular numbers deserve more caution than the sign pattern of unrestricted feedback.

Residual diagnostics use squared standardized residual regressions at lags 1, 6, and 12, with $TR^2$ compared with chi-square distributions, and Jarque–Bera normality tests. Since states are latent, residual construction substitutes smoothed probabilities. For postwar partial revelation with the restriction, ARCH-LM $p$ values are 0.8049, 0.7774, and 0.6259, and the normality $p$ value is 0.5354. In contrast, the constant-variance postwar model has a Jarque–Bera statistic of 269.53. The mixture and feedback structure capture substantial nonnormality in unconditional returns.

Figures 1–2 compare historical returns with smoothed high-state probabilities, both for variance-only and restricted full-revelation models. Their broadly similar regime timing supports the argument that switching is not merely an artifact of allowing a changing mean. It does not independently identify the direction of causality. Likewise, failure to reject remaining ARCH effects is evidence about these diagnostics, not a comprehensive proof against leverage effects or every alternative endogenous-volatility mechanism.

Several source presentation errors should not become data choices. Table 3's second-panel heading reads “1921–2000,” and Table 4's reads “1951–2000”; the text, captions, and sample definitions specify 1952–2000. Table 4 also repeats partial-revelation prose in its column headings even though its information sets and title specify full revelation. Use the equations and stated sample definitions rather than those inconsistent headings.

The practical lesson is to estimate contemporaneous discount-rate news separately from the forward-looking compensation for risk, test the cross-equation restriction rather than simply impose it, and distinguish filtered from smoothed information. The paper offers a compact likelihood-based framework for that exercise. It does not show that a high-volatility signal is profitable after implementation costs, that two states remain adequate in later markets, or that the reported risk premiums are robust to a corrected present-value indexing convention. Those are separate experiments that this source does not perform.
