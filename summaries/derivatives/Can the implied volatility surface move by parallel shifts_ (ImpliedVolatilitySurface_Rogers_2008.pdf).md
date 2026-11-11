# Can the implied volatility surface move by parallel shifts?

L. C. G. Rogers and M. R. Tehranchi, *Finance and Stochastics* 14 (2010), 235–248, DOI 10.1007/s00780-008-0081-9; published online 15 November 2008. The local filename uses the online-publication year. Source: [ImpliedVolatilitySurface_Rogers_2008.pdf](../../Finance/ImpliedVolatilitySurface_Rogers_2008.pdf). PDF page 1 is printed p. 235. The full 14-page article and all proofs in it are covered here.

## Why this matters

An implied-volatility surface can be fitted accurately at a date and still evolve inconsistently with an underlying martingale. A familiar scenario generator adds the same volatility shock to every strike and expiry. Rogers and Tehranchi show that an exact global version of this specification is extraordinarily restrictive: parallel shifts cannot be downward; with an additional moment-growth condition, they cannot be upward either. A surface that is constant through calendar time, when indexed by relative strike and time to expiry, characterizes an exponential Lévy model under a continuity condition.

These are restrictions on a complete continuum of option prices and on their conditional evolution. They do not invalidate a finite-grid stress scenario, a local approximation to a dominant volatility factor, or an empirically observed approximately parallel move. The distinction between exact structure and approximation matters because the proof uses arbitrarily long expiries and all strikes. Nor is the result a claim that every individual long-dated implied volatility must increase day by day. The general statement is a limiting inequality involving a limit superior.

The article also gives model-independent long-maturity flattening results, sharp slope constants for total implied variance, and an extreme-strike bound. The flattening does not require a Gaussian central limit theorem for returns. It follows from the martingale property and the geometry of option prices. The paper is theoretical: it has no calibration sample, Monte Carlo study, trading portfolio, measured forecast improvement, or market estimate to reproduce.

## Normalization and exactly what is shifted

Interest rates are zero, dividends absent, and the pricing probability is denoted $P$. The stock $S$ is a nonnegative true $P$-martingale with $S_0=1$. Sections 3–4 impose Assumption A1, strict positivity at all finite times almost surely, to permit normalization by $S_t$. Deterministic nonzero rates can be handled by discounting; stochastic rates or dividends would require a different setup. A positive strict local martingale is not covered by simply relabeling it a martingale.

Let $k$ be log strike relative to current spot, $K=S_te^k$, and let $\tau$ denote remaining time to expiry. Define the normalized Black–Scholes price, using the Gaussian upper tail $\overline\Phi$,

$$
f(k,v)=\overline\Phi\left(\frac{k}{\sqrt v}-\frac{\sqrt v}{2}\right)
-e^k\overline\Phi\left(\frac{k}{\sqrt v}+\frac{\sqrt v}{2}\right),\qquad v>0,
$$

with $f(k,0)=(1-e^k)^+$. Total implied variance $V_t(k,\tau)$ is the unique nonnegative solution of

$$
E\left[\left(\frac{S_{t+\tau}}{S_t}-e^k\right)^+\middle|\mathcal F_t\right]
=f(k,V_t(k,\tau)).
$$

The implied volatility is $\Sigma_t(k,\tau)=\sqrt{V_t(k,\tau)/\tau}$. The conjecture concerns

$$
\Sigma_t(k,\tau)=\Sigma_0(k,\tau)+\xi_t
\quad\text{for every }k\in\mathbb R,\ \tau>0,\ t\ge0.
$$

Thus the shift is additive in volatility, identical across both coordinates, and expressed at fixed relative log strike and fixed remaining maturity. This differs from shifting total variance, shifting annualized variance, or keeping an absolute strike and calendar expiry fixed while spot and time change. It also differs from saying that the surface is flat across strikes. A nonflat initial smile may be constant through calendar time under an exponential Lévy model.

Two identities drive the analysis. First,

$$
f_k=-e^k\overline\Phi\left(\frac{k}{\sqrt v}+\frac{\sqrt v}{2}\right),\qquad
f_v=\frac{\phi(k/\sqrt v-\sqrt v/2)}{2\sqrt v}>0.
$$

Second, the Gaussian Mills ratio satisfies $0\le1-x\overline\Phi(x)/\phi(x)\le1/(1+x^2)$ for $x\ge0$. Monotonicity in $v$ translates an upward volatility move into larger call and put prices at every strike; the Mills bound translates near-maximal call prices into large total implied variance.

## The long-maturity representation

A nonnegative martingale has an almost-sure limit $S_\infty$. Lemma 3.3 shows that the following are equivalent: $S_t\to0$ in distribution; $S_t\to0$ almost surely; a fixed-strike call price increases to 1 for some positive strike; the same holds for every strike; and $V_0(k,\tau)\to\infty$ for some, hence every, $k$. The identity behind the equivalence is

$$
1-E[(S_\tau-K)^+]=E[S_\tau\wedge K].
$$

This does not contradict $E[S_t]=1$ at every finite date. A martingale can fail to be uniformly integrable, with increasingly rare large outcomes carrying its mean while it converges to zero almost surely. If instead $P(S_\infty>0)>0$, total implied variance at fixed $k$ has a finite limiting value, and annualized implied volatility tends to zero.

When $S_t\to0$, the divergence of $V_0(k,\tau)$ is uniform on compact sets of $k$. The proof uses continuity and monotone convergence of the reciprocal variance together with Dini's theorem. This uniformity is required to control a smile segment rather than a single strike.

Lemma 3.6 gives, for every finite $M$ and fixed $t$,

$$
\lim_{\tau\to\infty}\sup_{|k|\le M}
\left|\Sigma_t(k,\tau)-
\sqrt{-\frac8\tau\log E[S_{t+\tau}\wedge1\mid\mathcal F_t]}\right|=0.
$$

The expression on the right is independent of $k$. Its financial object is a capped stock payoff, not an unconditional return variance. Conditional prices of that bounded claim determine the leading long-expiry implied-volatility scale. The normalization cap 1 is arbitrary up to multiplicative constants inside the expectation; their logarithms disappear at the scale $1/\tau$.

For the main asymptotic step, write $x_1=\sqrt v/2-k/\sqrt v$ and $x_2=\sqrt v/2+k/\sqrt v$. Then

$$
1-f(k,v)=\overline\Phi(x_1)+e^k\overline\Phi(x_2)
=\phi(x_1)\left[\frac4{\sqrt v}+O(v^{-3/2})\right]
$$

uniformly for bounded $k$. Consequently $-8\log(1-f(k,v))=v+O(\log v)$ there. Taking square roots makes the error vanish. The capped-payoff identity then supplies the conditional expression in Lemma 3.6. The case where the conditional stock limit has positive probability of being nonzero is handled separately: both implied volatility and the logarithmic representation tend to zero.

Corollary 3.7 states the compact-strike flattening result

$$
\lim_{\tau\to\infty}\sup_{k_1,k_2\in[-M,M]}
|\Sigma_0(k_2,\tau)-\Sigma_0(k_1,\tau)|=0.
$$

It does not provide a universal numerical expiry at which a smile is approximately flat, a universal convergence rate, or control of strikes moving outward with maturity. Those restrictions are crucial for applying the result to a finite set of traded options.

## Why a parallel shift cannot be negative

Theorem 3.1 states, under A1, that for $0\le s\le t$ and any fixed $k_1,k_2$,

$$
\limsup_{\tau\to\infty}
\{\Sigma_t(k_1,\tau)-\Sigma_s(k_2,\tau)\}\ge0
\quad\text{almost surely}.
$$

The probabilistic tool is Lemma 3.2: for nonnegative integrable random variables $X_p$, $\liminf X_p^{1/p}\le\liminf(E[X_p])^{1/p}$ almost surely. Fatou's lemma and Hölder's inequality prove it by ruling out the event where the left side exceeds the deterministic right side.

Apply this tool to the martingale $M_t(T)=E[S_T\wedge1\mid\mathcal F_t]$, normalized by $M_0(T)$, as terminal maturity $T$ tends to infinity. It restricts how its exponential decay rate can change with information. Lemma 3.6 turns that decay-rate comparison into the volatility inequality. The paper first compares remaining maturities $T-t$ and $T$, then uses monotonicity of total implied variance in maturity to state the result at a common remaining maturity.

If the exact parallel-shift representation holds, the common-strike volatility difference equals $\xi_t-\xi_s$ independently of maturity. The limiting inequality forces $\xi_t\ge\xi_s$; in particular $\xi_t\ge0$ because $\xi_0=0$. Thus the only possible exact shift process is nondecreasing. A two-sided Brownian level factor for the entire global surface is already inconsistent without the extra moment assumption used below.

The article's coin-mixture example shows that a long-volatility increase is possible in a general model. With equal probabilities, the stock is either constant at 1 or follows $\exp(W_t-t/2)$. Before the branch is revealed, positive probability of a nonzero limiting stock gives initial long implied volatility zero. After a positive amount of observation, on the Brownian branch the conditional implied volatility is 1. This establishes the possibility of an upward revision in long volatility; it is not an example of a whole surface making an exact parallel shift.

## The extra condition that rules out upward shifts

Define the moment-growth functional

$$
g_p(t)=\begin{cases}
\dfrac{\log E[S_t^p]}{p(p-1)},&p\notin\{0,1\},\\
E[S_t\log S_t],&p=1,\\
-E[\log S_t],&p=0.
\end{cases}
$$

These quantities are nonnegative and nondecreasing where defined; they are finite for $0<p<1$. Theorem 4.1 requires that for each $t\ge0$ there exist a real $p$ and some $\tau>0$, potentially depending on $t$, such that

$$
g_p(t+\tau)\le g_p(t)+g_p(\tau)<\infty.
$$

Under this condition and exact parallel shifts, $\xi_t=0$ almost surely. The condition is substantive, not merely finite moments. It asserts subadditivity at an appropriate pair of horizons. For a Black–Scholes exponential martingale with constant volatility $\sigma$, $g_p(t)=\sigma^2t/2$ for all $p$, so equality holds. Exponential Lévy models likewise have additive logarithmic moments whenever the relevant moment is finite.

The proof combines convex order with this condition. Since $\xi_t\ge0$, every normalized conditional call on $R=S_{t+\tau}/S_t$ costs at least the corresponding unconditional call on $S_\tau$. Put–call parity gives the same ordering for puts because both variables have mean 1. A twice differentiable convex payoff admits the static decomposition

$$
G(s)=G(1)+(s-1)G'(1)
+\int_1^\infty(s-K)^+G''(K)\,dK
+\int_0^1(K-s)^+G''(K)\,dK.
$$

Positive option weights imply $E[G(R)\mid\mathcal F_t]\ge E[G(S_\tau)]$. Taking the strictly convex functions $G_p(s)=s^p/[p(p-1)]$, with the logarithmic limits at $p=0,1$, multiplying by the appropriate current-state factor and averaging yields the reverse inequality $g_p(t+\tau)\ge g_p(t)+g_p(\tau)$. The assumed upper bound forces equality. Because the payoff weights are strictly positive, equality forces equality of the option prices for almost all strikes, then the common volatility shift must vanish. The argument needs the stated integrability; it does not establish the unrestricted conjecture by declaring the moment condition automatic.

For a diffusion $dS_t=S_t\sigma_t\,dW_t$, an additional short-maturity regularity result cited from Durrleman identifies spot volatility with the limiting at-the-money implied volatility. Exact parallel shifts would then make $\sigma_t$ nondecreasing. This excludes most familiar mean-reverting stochastic-volatility specifications from the exact-shift class even when the moment condition has not been checked. The identification is a cited result under regularity, not proved for every process in this article.

## Constant surfaces and the distinction from variance shifts

Theorem 4.4, attributed to Balland, assumes $\Sigma_t(k,\tau)=\Sigma_0(k,\tau)$ for all coordinates and $S_t\to1$ in distribution as $t\downarrow0$. All normalized conditional call prices then equal their time-zero counterparts. Calls at every strike determine the distribution, so the conditional law of $S_{t+\tau}/S_t$ is independent of $\mathcal F_t$ and depends only on $\tau$. Hence $\log S$ has stationary independent increments; stochastic continuity supplies the exponential Lévy conclusion. The theorem concerns a time-invariant surface in the stated coordinates, not a Black–Scholes surface with one constant number.

Remark 4.3 distinguishes volatility from average variance using a deterministic time change of Brownian motion. The consistent martingale construction is

$$
S_t=\exp(W_{t^2}-t^2/2).
$$

Conditional log-return variance is $(t+\tau)^2-t^2$, independent of strike. It follows that

$$
V_t(k,\tau)=(t+\tau)^2-t^2,\qquad
\Sigma_t(k,\tau)^2=\tau+2t.
$$

The annualized variance surface therefore makes exact upward shifts $2t$, although the volatility shift $\sqrt{\tau+2t}-\sqrt\tau$ varies with maturity. Its moment functional grows quadratically, violating the theorem's subadditivity condition. The supplied paper prints $-t^4/2$ in the exponent alongside $W_{t^2}$. That literal process is not a mean-one martingale: its expectation is $\exp((t^2-t^4)/2)$. The $-t^2/2$ expression above is a derived correction consistent with the subsequent printed formulas, not a verbatim transcription.

## Sharp slope restrictions

Section 5 examines the time-zero surface without requiring strict positivity in every example. Let $[\underline k(\tau),\overline k(\tau)]$ be the smallest interval containing the support of $\log S_\tau$, allowing infinite endpoints. Outside that interval the option has no time value and total implied variance is zero. Within it the implied-variance inverse is smooth in call price even when the stock distribution has atoms. The one-sided call derivatives are

$$
D_+C(k)=-e^kP(S_\tau>e^k),\qquad
D_-C(k)=-e^kP(S_\tau\ge e^k).
$$

Set $d_2=k/\sqrt V+\sqrt V/2$. Implicit differentiation gives

$$
D_+V=2\sqrt V\,
\frac{\overline\Phi(d_2)-P(S_\tau>e^k)}{\phi(d_2)},\qquad
D_-V=2\sqrt V\,
\frac{\overline\Phi(d_2)-P(S_\tau\ge e^k)}{\phi(d_2)}.
$$

The difference between strict and weak inequalities preserves atoms correctly. In particular $D_-V\le D_+V$, and their gap is $2\sqrt V\,P(S_\tau=e^k)/\phi(d_2)$. A smooth-density assumption would hide precisely this distinction. The right derivative exists except possibly at the lower support endpoint, and the left derivative except possibly at the upper endpoint; endpoints must not be discarded silently.

Theorem 5.1 establishes $D_+V<4$ on the nonnegative log-strike side and $D_-V>-4$ on the nonpositive side, at the points where these derivatives are defined. These are one-sided upper/lower bounds, not the universal finite-maturity claim $|V_k|<4$ at every strike. If $S_t\to0$ in distribution, then on every fixed compact interval,

$$
\limsup_{\tau\to\infty}\sup_{|k|\le M}
\max\{|D_-V(k,\tau)|,|D_+V(k,\tau)|\}\le4.
$$

For example, the upper estimate follows from dropping a nonnegative digital probability in the derivative formula and applying the Mills bound:

$$
D_+V<2\sqrt V\,\frac{\overline\Phi(d_2)}{\phi(d_2)}
<\frac4{1+2k/V}
$$

when $d_2>0$. A symmetric put representation supplies the lower bound. Since $V$ diverges uniformly on compact $k$-sets under the stock-limit assumption, these bounds approach $\pm4$. Converting to volatility multiplies the variance slope by $1/(2\sqrt{\tau V})$, giving vanishing implied-volatility slopes in this regime. The separate flattening corollary also covers the regime where variance remains bounded and volatility itself goes to zero.

The sharpness example chooses independent random variables $\zeta\sim\operatorname{Exp}(1)$ and $T$ with survival probability $P(T\ge t)=\min(1,1/t)$. With a filtration that reveals $\zeta$ at time 1 and survival thereafter, set $S_t=1$ before time 1, $S_t=t\zeta$ for $1\le t<T$, and $S_t=0$ after $T$. Conditional survival offsets deterministic growth, making $S$ a martingale. For $t\ge1$,

$$
E[(S_t-K)^+]=e^{-K/t}.
$$

The derivative $D V(k,t)$ tends uniformly to $-4$ on each compact $k$-interval. This example reaches zero and explicitly falls outside A1; it proves sharpness for the broader nonnegative-martingale slope theorem, not for an everywhere strictly positive subclass. No return normality is involved.

The final theorem concerns a different asymptotic direction: fixed maturity and $k\to+\infty$. It proves

$$
\sqrt{2k}-\sqrt{V(k,\tau)}\longrightarrow\infty,
$$

and that $D_+V(k,\tau)<2$ for all sufficiently large $k$, with the threshold depending on maturity/model. The proof uses vanishing call prices, $k/\sqrt v+\sqrt v/2\ge\sqrt{2k}$, and the Mills bound. In particular $e^k\overline\Phi(\sqrt{2k})<1/(2\sqrt{\pi k})\to0$. Combined with the derivative formula, this yields $D_+V<\sqrt{2V/k}$ and eventually the slope bound 2. It is not an assertion that all finite-strike slopes are bounded by 2, nor that the same bound controls the long-maturity compact-strike limit.

## Printed algebra and the formulas used here

Several intermediate expressions in the supplied article should be distinguished from its substantive conclusions. The time-change exponent in Remark 4.3 was discussed above. Three additional corrections matter when reconstructing the proofs.

First, the middle line of equation (5.3), printed p. 245, omits the factor $e^k$ multiplying $P(S_\tau>e^k)$ in the log-strike call derivative. The final line of that equation, reproduced above, is correct because $e^k\phi(k/\sqrt V+\sqrt V/2)=\phi(k/\sqrt V-\sqrt V/2)$.

Second, equation (5.5) prints a denominator $1+k/V$. The direct Mills-ratio substitution gives $1+2k/V$. For $k\ge0$, the printed fraction is a weaker upper bound, although its final strict comparison at $k=0$ does not follow from that fraction alone; strictness is available from the preceding estimate. For negative $k$ used in the compact-interval extension, the corrected denominator should be retained. The limiting constant 4 is unchanged as bounded $k/V$ tends to zero.

Third, the sharpness proof on printed p. 246 states
$E[S_t;S_t<K]/(1-E[(S_t-K)^+])=1/t$. Direct integration of its own exponential example instead gives, with $x=K/t$,

$$
\frac{E[S_t;S_t<K]}{1-E[(S_t-K)^+]}
=\frac{1-(1+x)e^{-x}}{1-e^{-x}}
=1-\frac{x}{e^x-1}\sim\frac{x}{2}.
$$

This still tends to zero uniformly for $K$ in a fixed positive compact interval, so it supports the proof's required limit. It is not identically $1/t$.

There is also an immaterial constant in the logarithmic expansion on printed p. 240. Expanding the displayed Gaussian tails gives

$$
-8\log(1-f(k,v))
=\frac{(v-2k)^2}{v}+4\log v+4\log(2\pi)-8\log4+o(1),
$$

uniformly for bounded $k$, rather than a zero-limit remainder after only the first two terms. The needed $v+O(\log v)$ statement survives. These are algebraic corrections derived from the printed model. They do not amount to a claim that the paper's main parallel-shift theorem is false.

## Implications and boundaries for surface modeling

The theorems provide consistency diagnostics for a proposed stochastic surface. A model that defines a strictly positive martingale stock and claims an exact common volatility shift across all relative strikes and expiries must explain how its shift avoids decreases; with the moment condition, it must actually be constant. Conversely, fitting a finite slice and applying a finite shock does not satisfy the theorem's global premise. Whether a finite shocked surface is free of static arbitrage requires its own option-price monotonicity and convexity checks; these results do not replace them.

A practical long-expiry extrapolation can use the flattening theorem as a qualitative restriction, but the paper gives no calibration algorithm, loss function, interpolation rule, tail splice, or maturity cutoff. It supplies no empirical evidence about how quickly real smiles flatten. The requirement is especially easy to misuse if a system changes from fixed log moneyness to delta coordinates, or from remaining maturity to fixed calendar expiry, during a scenario calculation. Those are different objects from $\Sigma_t(k,\tau)$.

Finally, the universal flattening argument does not imply standardized returns become Gaussian. The paper explicitly points to spectrally negative stable Lévy log returns as a counterexample to that explanation. A flatter long-term implied smile constrains option prices while leaving room for non-Gaussian return distributions, nonuniformly integrable stock dynamics, and information-driven revisions to long-volatility levels.

## Source map

Sections 2–3, printed pp. 236–241, define the surface, prove the capped-payoff representation, and establish the long-volatility inequality. Section 4, pp. 241–243, contains the moment-growth condition, convex-order proof, variance-shift example, and exponential Lévy characterization. Section 5, pp. 243–247, develops one-sided derivatives, the sharp constant 4, and the far-right-wing bound 2. References occupy pp. 247–248. The source cites Balland (2002), Durrleman (2004), Lee (2004), and the Dybvig–Ingersoll–Ross long-rate result as related work; those references were not separately read for this note.
