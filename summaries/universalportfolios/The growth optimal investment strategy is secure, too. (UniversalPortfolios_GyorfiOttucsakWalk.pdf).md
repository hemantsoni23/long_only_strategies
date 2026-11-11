# The growth optimal investment strategy is secure, too.

László Györfi, György Ottucsák, and Harro Walk. Undated 22-page manuscript in the supplied library copy; its references include work published in 2012. The copy does not establish a publication year, journal, or DOI. [Source PDF](../../Finance/UniversalPortfolios_GyorfiOttucsakWalk.pdf). Page references below are both printed and PDF pages. The complete paper, including proofs and references, was read.

## Why this matters

An asymptotically optimal growth rate does not tell an investor how long losses can persist. This paper connects the log-optimal portfolio to three more operational questions: the probability of falling below a specified exponential wealth path at a finite date, the probability of ever falling below that path after a specified date, and the time required to reach a large wealth target. The useful contribution is to state explicit probability bounds and distinguish what independence, bounded returns, ergodicity, and mixing each supply.

For independent bounded returns, the central result is a direct, valid Hoeffding bound. For general stationary returns, the paper decomposes shortfall risk into a martingale shock and a persistent variation in conditional investment opportunities. The second component cannot be controlled at a universal rate by ergodicity alone. The proposed Markov extension attempts to fill that gap, but its proof requires an additional uniformity condition not established by the stated assumptions. The note preserves the source's claims and identifies that issue rather than turning an asymptotic argument into a finite-horizon capital guarantee.

The empirical exercise is a diagnostic illustration using historical NYSE price relatives. It does not estimate a deployable, net-of-cost loss guarantee, and it does not establish that observed similarity across five lag lengths proves a first-order Markov law. Those distinctions matter because the theoretical bounds concern the true conditional log-optimum, whereas a practitioner trades an estimate of that optimum.

## Market, admissible portfolios, and the oracle

There are $d$ assets. Their positive gross returns at time $n$ are $X_n=(X_n^{(1)},\ldots,X_n^{(d)})$, obtained by dividing each current price by its previous price. The admissible set is the simplex

$$
\Delta_d=\{b\in\mathbb R^d:b_j\geq0,\ \sum_{j=1}^d b_j=1\}.
$$

The investor reallocates all current wealth before each return is realized. No short sales, margin purchases, consumption, transaction costs, or market impact enter the model. A constant portfolio $b$ means constant weights reset each period, not a buy-and-hold position. With initial wealth normalized to one,

$$
S_n(b)=\prod_{i=1}^n\langle b,X_i\rangle,
\qquad \frac{\log S_n(b)}n=\frac1n\sum_{i=1}^n\log\langle b,X_i\rangle.
$$

In the independent and identically distributed case, define

$$
W(b)=E\log\langle b,X_1\rangle,
\qquad b^*\in\arg\max_{b\in\Delta_d}W(b),
\qquad W^*=W(b^*).
$$

Integrability of the logarithm is needed for the strong law. Under that condition, the realized average log return of each fixed portfolio converges almost surely to $W(b)$. Maximizing the expectation therefore maximizes the almost-sure asymptotic rate among fixed portfolios. The later conditional formulation extends the comparison to predictable strategies. An optimizer need not have unique weights if assets are redundant; the results concern its achieved return process and value.

A reproducible finite-distribution implementation replaces the expectation by $\sum_s p_s\log(b^\top x_s)$ and solves a concave maximization over the simplex. For a candidate optimum with strictly positive portfolio returns, the directional derivative toward any feasible $b$ gives

$$
E\frac{\langle b,X\rangle}{\langle b^*,X\rangle}\leq1.
$$

This is a useful optimality check and explains the paper's quoted relative-wealth property. Applied conditionally each period, the wealth ratio of any predictable competitor to the conditional log-optimum is a nonnegative supermartingale. Consequently $E(S_n/S_n^*)\leq1$ when both start at one. This is a statement about relative wealth denominated in the oracle portfolio. It is not $E S_n\leq E S_n^*$, stochastic dominance in dollar wealth, or a guarantee that $S_n^*$ exceeds its initial value.

The source discusses that distinction on pp. 8–9. A portfolio maximizing arithmetic expected return can have much larger expected terminal wealth than the log-optimum, while its typical multiplicative path is inferior. Changing the objective changes the optimal allocation; a logarithmic transformation does not settle an investor's preference over terminal losses.

## Independent returns: a finite-date lower-tail bound

The extra assumption for Theorem 1 is a deterministic support restriction, not an observed-sample truncation:

$$
0<a_1<1<a_2<\infty,
\qquad a_1\leq X_n^{(j)}\leq a_2\quad\text{almost surely for every }n,j.
$$

Set $K=\log a_2-\log a_1$. Because weights are nonnegative and sum to one, every portfolio gross return also lies in $[a_1,a_2]$, and its log return lies in an interval of length $K$. Let $Y_i=\log\langle b^*,X_i\rangle$. The $Y_i$ are independent, bounded, and have mean $W^*$. For any $R<W^*$, the event $S_n^*<e^{nR}$ is exactly

$$
\frac1n\sum_{i=1}^n(Y_i-W^*)<-(W^*-R).
$$

Hoeffding's inequality therefore gives the source's Theorem 1, pp. 5–6:

$$
P\{S_n^*<e^{nR}\}\leq
\exp\left[-\frac{2n(W^*-R)^2}{K^2}\right].
$$

No Gaussian approximation is involved. The relevant distance is the gap between the target log-growth rate and the optimal expected log-growth rate. The guarantee weakens quadratically as this gap shrinks, and broad support bounds can make it very conservative. The boundedness assumption excludes returns arbitrarily close to zero, even though the investor is long-only. It is stronger than observing no extreme losses in a historical panel.

The strong law alone implies that, for each fixed $R<W^*$, a random finite time eventually exists after which $S_n^*\geq e^{nR}$ forever. The paper represents this by the increasing lower envelope $\inf_{m\geq n}m^{-1}\log S_m^*$, which converges to $W^*$. The concentration result quantifies the probability distribution of an admissible deterministic starting date.

## An eventual lower envelope and its numerical meaning

Write

$$
c=\frac{2(W^*-R)^2}{K^2}.
$$

A union bound over all future dates, followed by summation of a geometric series, yields Corollary 1, p. 7:

$$
P\{\exists m\geq n:S_m^*<e^{mR}\}
\leq\sum_{m=n}^{\infty}e^{-cm}
=\frac{e^{-cn}}{1-e^{-c}}.
$$

The bound can always be capped at one. It controls the whole future path after $n$, rather than only the single terminal observation. If $W^*>0$, choosing $R=0$ bounds the probability of ever subsequently falling below starting wealth. A sufficient integer horizon for failure probability at most $\alpha$ is

$$
n\geq\left\lceil\frac{\log[1/\{\alpha(1-e^{-c})\}]}{c}\right\rceil.
$$

For small $c$, stable numerical code should evaluate $1-e^{-c}$ using an exponential-minus-one routine rather than subtracting nearly equal floating-point values.

A derived scale calculation illustrates the limitation. Use the paper's illustrative support endpoints $a_1=0.7$, $a_2=1.2$, take $R=0$, and hypothetically set the true $W^*$ to the reported empirical strategy mean $0.00118$ per day. Then $K=0.5389965$ and $c=9.58566\times10^{-6}$. The sufficient horizon for $\alpha=0.05$ is 1,517,995 trading days, roughly 6,072 years at 250 trading days per year. This is not a paper-reported forecast, and substituting an empirical strategy mean for the unknown oracle value is not statistically justified. It shows why an exponential rate can be mathematically strong yet numerically uninformative for an investment mandate.

The same result cannot be read as a maximum-drawdown bound. The threshold $e^{mR}$ is anchored to initial wealth and calendar time; drawdown is measured relative to a running peak. Nor does it protect against interim losses before $n$.

## Time spent below a nearly optimal benchmark

Pages 7–8 address a different asymptotic regime. Suppose $\sigma^2=\operatorname{Var}(Y_i)$ is positive and finite. Instead of holding $R$ fixed below $W^*$, let it approach the optimum at the central-limit rate:

$$
R_n=W^*-\frac{m\sigma}{\sqrt n},\qquad m>0.
$$

Define the occupation fraction

$$
A_n=\frac1n\sum_{j=1}^n
\mathbf1\{S_j^*<e^{jR_n}\}.
$$

Donsker's invariance principle applied to centered partial sums implies

$$
A_n\ \Rightarrow\ \int_0^1\mathbf1\{B(u)+mu\leq0\}\,du,
$$

where $B$ is standard Brownian motion. The limiting occupation fraction is random, rather than collapsing to zero. Intuitively, the benchmark is being raised toward optimal growth at exactly the scale of cumulative fluctuations. It is therefore possible to obtain asymptotically optimal growth while spending a substantial and randomly varying fraction of a long sample below that moving benchmark.

The source gives the generalized arcsine distribution explicitly. For standard normal density $\varphi$ and distribution function $\Phi$, its cumulative distribution on $0\leq x\leq1$ is

$$
F_m(x)=2\int_0^x
\left[\frac{\varphi(m\sqrt{1-u})}{\sqrt{1-u}}+m\Phi(m\sqrt{1-u})\right]
\left[\frac{\varphi(-m\sqrt u)}{\sqrt u}-m\Phi(-m\sqrt u)\right]du.
$$

At $m=0$ the integrand becomes $1/[\pi\sqrt{u(1-u)}]$, recovering the usual arcsine law. This provides a useful normalization check. For increasingly large standardized gaps $m$, the occupation fraction converges toward zero. The same qualitative disappearance occurs for a fixed benchmark rate strictly below $W^*$. Neither statement implies that the number of bad days is bounded uniformly across investment opportunities or that the initial drawdown is small.

## First passage to a large wealth target

For a fixed portfolio with positive $W(b)$, let

$$
\tau_b(s)=\inf\{n\geq1:S_n(b)\geq s\},\qquad s>1.
$$

The logarithm converts the problem into first passage of a random walk with positive drift through $a=\log s$. The renewal results invoked on pp. 9–10 give, with the corresponding integrability conditions,

$$
\frac{\tau_b(s)}{\log s}\to\frac1{W(b)}\quad\text{almost surely},
\qquad
\frac{E\tau_b(s)}{\log s}\to\frac1{W(b)}.
$$

The log-optimum minimizes this leading-order coefficient among the constant portfolios being compared. This is asymptotic target-time optimality. It does not say that the fixed log-optimal allocation minimizes expected hitting time for every finite target, or against every strategy allowed to adapt exposure as it approaches a boundary.

The paper makes the overshoot correction explicit through a bound attributed to Lorden. Define $Y_b=\log\langle b,X_1\rangle$, $\mu_b=E Y_b>0$, and $v_b^+=E[(Y_b^+)^2]$. Then the stated comparison is

$$
\frac{\log s}{W^*}-\frac{\log s}{\mu_b}-\frac{v_b^+}{\mu_b^2}
\leq E\tau_*(s)-E\tau_b(s)
\leq\frac{\log s}{W^*}-\frac{\log s}{\mu_b}+\frac{v_*^+}{(W^*)^2}.
$$

The leading difference grows with $\log s$; overshoot contributes an additive constant when these positive-part second moments are finite. Bounded returns ensure that requirement. Small drift makes the correction large, so an asymptotic ranking need not be decisive at a modest target.

A separate tail bound follows without identifying the full first-passage distribution. If $\tau_*(e^{nR})>n$, then terminal wealth at time $n$ is below $e^{nR}$. Hence

$$
P\{\tau_*(e^{nR})>n\}\leq
P\{S_n^*<e^{nR}\}\leq e^{-cn}.
$$

The converse implication fails: wealth can cross the target and subsequently fall below it. The source correctly uses an inequality rather than equating these events.

## Predictable portfolios and the residual opportunity term

Let $\mathcal F_{i-1}=\sigma(X_1,\ldots,X_{i-1})$. A dynamic portfolio $b_i$ is $\mathcal F_{i-1}$-measurable and lies in $\Delta_d$. The oracle maximizes $E[\log\langle b_i,X_i\rangle\mid\mathcal F_{i-1}]$ at each date. Its myopia means that the objective separates into one-period conditional log returns; it does not mean that the portfolio ignores historical information.

For any predictable strategy, write $Y_i=\log\langle b_i,X_i\rangle$ and

$$
G_i=E(Y_i\mid\mathcal F_{i-1}),\qquad D_i=Y_i-G_i.
$$

The $D_i$ are martingale differences. Under $\sum_iE(D_i^2)/i^2<\infty$, their average converges almost surely to zero. The source assumes a uniform second-moment bound in its dynamic comparison, which supplies this summability. Conditional optimality compares each competitor and oracle using the same information set, giving the asymptotic relative-growth inequality

$$
\limsup_{n\to\infty}\frac1n\log\frac{S_n}{S_n^*}\leq0.
$$

Under the stationary ergodic setting and appropriate integrability, the oracle growth rate equals the expected infinite-past conditional optimum,

$$
W^*=E\left[\sup_{b\in\Delta_d}E\{\log\langle b,X_0\rangle\mid X_{-1},X_{-2},\ldots\}\right].
$$

These established results are attributed to Algoet and Cover. The source's particular shortcut toward the last limit needs the qualification below, but that shortcut does not invalidate the general underlying log-optimal growth result.

For bounded returns, every $D_i$ lies in an interval of width $K$, whose lower endpoint can depend on $\mathcal F_{i-1}$. Conditional Hoeffding–Azuma therefore applies. With $\epsilon=(W^*-R)/2$, Theorem 2, pp. 13–14, is

$$
P\{S_n^*<e^{nR}\}
\leq\exp\left[-\frac{n(W^*-R)^2}{2K^2}\right]
+P\left\{\frac1n\sum_{i=1}^nG_i^*<R+\epsilon\right\}.
$$

The proof splits the event that average realized growth is below $R$ into either average conditional growth below $R+\epsilon$, or an average martingale deviation below $-\epsilon$. This decomposition is valid and useful. The first exponential term controls surprises around conditional opportunities. The remaining probability controls the opportunities themselves. Stationarity and ergodicity do not give a distribution-free convergence rate for that second term.

There is an important source-level proof gap on pp. 13 and 15. The paper compares optimized conditional values under nested information sets directly, path by path. If $\mathcal G\subset\mathcal F$ and

$$
V_{\mathcal H}=\sup_bE[\log\langle b,X\rangle\mid\mathcal H],
$$

then the generally valid comparison is

$$
E[V_{\mathcal F}\mid\mathcal G]\geq V_{\mathcal G},
$$

not $V_{\mathcal F}\geq V_{\mathcal G}$ in every realized state. Information may reveal that opportunities are worse than their unconditional average. A one-asset example already disproves the pointwise claim: the asset pays either gross return $0.5$ or $2$ with equal probability, coarse information reveals nothing, and fine information reveals which outcome occurs. The coarse expected log return is zero, while the fine value is $\log0.5<0$ in the bad state. This example concerns the asserted information inequality; it is not an empirical model for stock returns. The source's pathwise sandwich and the proposed probability enlargement on p. 15 therefore cannot be used as written. This is a derived correction to the proof, not a claim that information reduces expected optimal value.

## The Markov extension and its missing uniformity

Theorem 3 assumes a stationary first-order Markov chain on a denumerable set $S\subset[a_1,a_2]^d$, irreducibility, aperiodicity, and continuity of the transition kernel in total variation:

$$
\sup_{H\subset S}|\nu(H\mid x')-\nu(H\mid x)|\to0
\quad\text{as }x'\to x.
$$

Its claimed conclusion is that positive constants $c,C,c^*,C^*$ exist such that

$$
P\{S_n^*<e^{nR}\}\leq
\exp\left[-\frac{n(W^*-R)^2}{2K^2}\right]+Ce^{-cn},
$$

and the probability of any violation after $n$ is at most $C^*e^{-c^*n}$. The constants depend on the growth gap, return bounds, and the chain's ergodic behavior; the paper gives no numerical calibration.

The proof on pp. 19–20 first obtains convergence to the invariant distribution for each starting state. It also correctly uses the contraction of total variation under a Markov transition to transfer one-step continuity to later transition laws. It then asserts convergence uniformly over all starting states. That last implication is not justified by boundedness of $S$ alone. A bounded countable set need not be compact: for example, $S=\{1+1/(n+1):n\geq0\}$ excludes its accumulation point. Every state is isolated in its relative topology, so continuity at every state imposes no useful uniform mixing restriction.

For a concrete diagnosis, embed a reflected nearest-neighbor random walk on the nonnegative integers in this $S$, give it a positive self-loop probability, and choose downward drift away from every positive state. The chain is irreducible, aperiodic, and positive recurrent with a stationary distribution. It is not uniformly convergent in total variation: starting far enough from zero, a chain taking bounded steps cannot approach the stationary mass near zero within a fixed number of periods. The embedding preserves this obstruction while satisfying the source's pointwise continuity condition. This establishes a failure of the proof's uniform-convergence inference. It does not, by itself, compute a counterexample to every particular wealth bound in the theorem.

A sufficient repair is to impose uniform total-variation mixing directly, for example through a finite-state irreducible aperiodic model or an appropriate uniform minorization condition. Then the bounded conditional-value process $G_i^*=g(X_{i-1})$ inherits mixing, and the paper's concentration route can proceed. Its quoted Collomb bound has the form

$$
\exp\left\{\frac nm\left[
3\sqrt e\,\varphi_m+
\frac38\frac{1+4\sum_{i=1}^m\varphi_i}{m}
-\frac{\epsilon}{4K}
\right]\right\},
$$

where $\varphi_i$ are mixing coefficients. If $\varphi_i\to0$, choose a fixed sufficiently large block length $m$ so that the bracket is negative; for sufficiently large $n$ this yields exponential decay. Summing the resulting geometric bounds gives the eventual-envelope statement. A practical implementation still needs an actual bound on mixing coefficients or a specified transition model. The source's final extension remark about Harris recurrence should not be treated as supplying those missing uniform quantitative inputs.

## The historical kernel experiment

Pages 15–18 describe two adjusted-close panels: 36 NYSE stocks over 5,651 trading days spanning 22 years and ending in 1985, and 19 stocks over 11,178 trading days spanning 44 years and ending in 2006. Prices are corrected for dividends and splits. The source does not provide exact starting dates, complete ticker lists, survivorship and delisting rules, missing-value handling, or an unambiguous assignment of each displayed histogram to one of the panels. It points to an external benchmark data page but does not include the underlying observations.

For lag length $k=1,\ldots,5$ and scale index $\ell=1,\ldots,10$, flatten the preceding $k$ return vectors into a $dk$-dimensional history. The neighborhood at time $n$ is

$$
J_n(k,\ell)=\{i:k<i<n,\ \|X_{i-k}^{i-1}-X_{n-k}^{n-1}\|\leq r_{k,\ell}\},
$$

with

$$
r_{k,\ell}^2=0.0002dk+0.00002dk\ell.
$$

Only previously observed outcomes enter the fit. When the neighborhood is nonempty, the portfolio maximizes $\sum_{i\in J_n}\log\langle b,X_i\rangle$ over the simplex. When empty, it uses equal weights. The diagnostic $Z_{n,k}$ is the optimized historical objective divided by the neighborhood size; it estimates a conditional optimal value. The realized next-day diagnostic is $Z'_{n,k}=\log\langle\widehat b_n,X_n\rangle$. These are different objects: in-sample optimized neighbor returns need not equal subsequently realized portfolio returns.

The displayed experiments use $\ell=7$, so the squared radius is $0.00034dk$. The paper reports these daily log-return statistics:

| Statistic | Coke return | Estimated conditional optimum, $k=1$ | Realized kernel portfolio, $k=1$ |
|---|---:|---:|---:|
| Minimum | −0.2836 | −0.0080 | −0.1535 |
| First quartile | −0.0074 | 0.00061 | −0.0077 |
| Median | 0 | 0.0010 | 0.0003 |
| Mean | 0.00053 | 0.0019 | 0.00118 |
| Third quartile | 0.0083 | 0.0018 | 0.0093 |
| Maximum | 0.1796 | 0.1092 | 0.1522 |

Figures 1 and 3 show broadly similar central daily-return shapes for Coke and the fitted portfolio; Figure 2 is sharply concentrated near a small positive conditional value with a long right tail. The reported mean of the optimized conditional diagnostic is about 61% above the realized strategy's mean, although the paper does not test or decompose this difference. Maximization of noisy local estimates offers one possible explanation; it is not established causally by these summaries.

Using 250 trading days per year, $e^{250(0.00118)}-1=34.31\%$ and $e^{250(0.00053)}-1=14.17\%$. The source reports approximately 34% and 14%. Its p. 18 prose accidentally repeats $0.00118$ for Coke; the Coke statistics and the 14% annualization require $0.00053$. The correction follows directly from the printed earlier statistic and the compounding calculation. These annualizations describe sample geometric growth, not expected future annual returns.

The authors report that the five conditional-value histograms look similar across $k$, motivating their Markov model. Equality of such scalar summaries is much weaker than equality of conditional return distributions. The radius also changes with dimension and lag length, so this is not a controlled specification test of memory order. No confidence intervals, formal Markov test, separate validation period, optimization tolerances, turnover statistics, transaction-cost deductions, or comparison with standard portfolio benchmarks are provided. The two historical panels do not validate the deterministic support bounds for future observations.

## What can be reconstructed and what remains open

The paper supplies enough information to reproduce the theoretical independent-return bound, its union-bound extension, the occupation-time limit, and the neighborhood selection and log-optimization rule. With the historical return panels and a specified simplex solver, one could recreate the empirical diagnostics, subject to the unresolved panel selection and initialization details. It does not provide the data or a complete trading-cost-aware backtest.

The most transferable insight is the decomposition into conditional opportunities and unpredictable shocks. A concentration bound for shocks does not remove estimation error in the opportunity process. For deployment, one would need a defensible lower confidence bound on achievable conditional growth, support or tail assumptions, dependence controls, and the loss of growth caused by implementation costs. None can be inferred from a positive historical average alone.

The note's two proof qualifications are derived checks of the supplied manuscript. The independent bounded-return theorem and martingale decomposition remain usable. The Markov exponential guarantee should be applied only after independently establishing the uniform mixing input. The bibliography inside the source locates the relevant foundations: Algoet and Cover (1988) for log-optimal relative growth, Hoeffding (1963) and Azuma (1967) for concentration, Lorden (1970) for overshoot bounds, Takács (1996) for the generalized arcsine law, and Collomb (1984) for the mixing inequality. Those references are reported as the paper's foundations, not as separately reread sources for this note.
