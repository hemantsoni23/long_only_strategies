# Tracking Error: Ex-Ante versus Ex-Post Measures

Soosung Hwang and Stephen E. Satchell, undated ten-page working-paper version. Source: [HwangSatchell_  Tracking Error - Ex-Ante versus Ex-Post Measures.pdf](<../../Finance/HwangSatchell_  Tracking Error - Ex-Ante versus Ex-Post Measures.pdf>). The PDF does not establish a publication date or DOI. Its references include material dated 2001.

## Why this matters

A risk forecast made for today's portfolio is often compared with realized active-return volatility over a period during which the holdings change. These quantities need not estimate the same risk. Even a buy-and-hold portfolio can have changing value weights, and benchmark weights can change as well. The paper isolates the extra variance associated with stochastic active weights and argues that risk budgeting should account for the intended strategy over the evaluation horizon.

Its most useful result is a variance decomposition around average active weights. The result requires conditional-return assumptions that should be made explicit, and it compares population variances rather than guaranteeing an inequality for every realized sample. The paper's absolute-deviation theorem contains a more fundamental mathematical problem. A replication note must distinguish the valid variance argument from the broader claims in the abstract and from that defective proof.

## Quantities and timing

Let $a_t$ be portfolio weights, $b_t$ benchmark weights, and $w_t=a_t-b_t$ active weights selected before next-period returns $r_{t+1}$. For two fully invested portfolios, $\mathbf1^\top w_t=0$. The active return is

$$
R_{t+1}=w_t^\top r_{t+1}.
$$

For a fixed vector $w$ and return covariance $\Omega$, the usual forecast is $\mathrm{TE}(w)=\sqrt{w^\top\Omega w}$. This is a volatility. The paper sometimes discusses its square, the tracking variance, and these units must be kept distinct.

The realized estimator over $T$ active returns is

$$
\widehat{\mathrm{TE}}=\sqrt{\frac{1}{T-1}\sum_{t=1}^{T}(R_t-\bar R)^2}.
$$

The source uses portfolio-return notation inside this expression after describing relative returns; for a tracking-error implementation, the observations must be actual portfolio-minus-benchmark returns. Total portfolio volatility is a different quantity. A constant expected active return is removed by the sample centering.

Random weights arise for reasons other than discretionary trading. Buy-and-hold value weights drift with prices; quarterly rebalancing leaves intra-quarter drift; and a capitalization-weighted benchmark changes as constituent values and membership change. Rebalancing to a fixed active vector before each measurement period is a special case. A passive portfolio that exactly matches the benchmark can still have zero active risk, even though both underlying sets of weights move.

## The variance decomposition with its required assumptions

Write $w_t=m_w+v_t$, where $E[v_t]=0$ and $\operatorname{Var}(w_t)=\Omega_w$. A sufficient set of assumptions for the source's calculation is

$$
E[r_{t+1}\mid w_t]=\mu,
\qquad \operatorname{Var}(r_{t+1}\mid w_t)=\Omega.
$$

Independence of weights and subsequent returns is stronger than necessary but sufficient. Predetermined weights alone are not sufficient: a strategy can select positions using information that changes conditional expected returns or conditional covariance.

The law of total variance gives

$$
\operatorname{Var}(R_{t+1})=E[w_t^\top\Omega w_t]+\operatorname{Var}(w_t^\top\mu).
$$

Expand around $m_w$. Since the centered weights have zero mean,

$$
E[w_t^\top\Omega w_t]=m_w^\top\Omega m_w+\operatorname{tr}(\Omega\Omega_w).
$$

Also, $\operatorname{Var}(w_t^\top\mu)=\mu^\top\Omega_w\mu$. Therefore Theorem 1's decomposition is

$$
\operatorname{Var}(R_{t+1})=m_w^\top\Omega m_w+\operatorname{tr}(\Omega\Omega_w)+\mu^\top\Omega_w\mu.
$$

The first term is the risk of the average active portfolio. The trace term is the average additional conditional variance from dispersion around that average. The last term is variation in conditional active expected return induced by changing weights. Both added terms are nonnegative for positive-semidefinite covariance matrices. Strict positivity needs relevant variation in a risky direction; stochastic weights in a covariance null space need not create extra risk.

An illustrative calculation, not an empirical result from the paper, makes the units clear. Suppose the average active portfolio has monthly tracking variance 0.0004, the trace term is 0.0001, and the mean-return term is zero. Tracking volatility rises from 2.00% to $\sqrt{0.0005}=2.236\%$ per month. The increase in variance is 25%; the increase in volatility is approximately 11.8%. Adding 0.0001 directly to a volatility would be incorrect.

Because active weights sum to zero, $\Omega_w\mathbf1=0$. If expected asset returns are all identical, $\mu=c\mathbf1$, then $\mu^\top\Omega_w\mu=0$. More generally, that term depends on cross-sectional differences in expected returns. The source suggests it may be small in practical cases. Its Remark 2 appears to name the average-portfolio term where the surrounding argument points to the trace term as the remaining source of extra variance. The displayed decomposition resolves that ambiguity.

## What the inequality actually compares

The valid comparison under these assumptions is between unconditional strategy variance and the variance at the **average** active weights. It is not a general inequality against the risk of the initial portfolio $w_0$. If a manager begins with a large active position and subsequently reduces it, initial risk can exceed the strategy's average risk. Without an assumption linking $w_0$ to $m_w$, the decomposition does not order those quantities.

Nor does a population inequality imply that each sample realized volatility exceeds a forecast. A sample can contain unusually quiet returns. Even the sample variance has estimation uncertainty, and taking its square root adds nonlinear estimation effects. The abstract's assertion that ex-post tracking error is always larger than planned tracking error should therefore be read much more narrowly than its literal wording.

There is a second comparison worth distinguishing. Averaging correctly specified conditional **variances** over the realized strategy already includes $E[w_t^\top\Omega w_t]$, including the trace contribution. Relative to that average, only variation in conditional means remains in the law-of-total-variance decomposition. A current conditional risk forecast need not be biased for its own next-period target merely because it is smaller than the unconditional variance of a changing strategy.

If conditional returns depend on the holdings information, the general identity is instead

$$
\operatorname{Var}(R_{t+1})=E[w_t^\top\Omega(w_t)w_t]+\operatorname{Var}[w_t^\top\mu(w_t)].
$$

A richer information set can replace conditioning on weights. In that setting, an unconditional $\Omega$ and the covariance of weights alone do not recover the source's three terms. Dynamic volatility targeting is an example where positions deliberately depend on a forecast risk state, making this limitation operationally relevant.

## Estimation and the gap between diagnosis and forecast

The paper proposes storing historical weights and estimating

$$
\widehat m_w=\frac1T\sum_t w_t,
\qquad \widehat\Omega_w=\frac1T\sum_t w_tw_t^\top-\widehat m_w\widehat m_w^\top.
$$

Together with estimates of return means and covariance, these permit an ex-post decomposition. The $1/T$ normalization shown here matches the source's population-moment-style estimator. An unbiased sample covariance uses a different finite-sample adjustment; either convention should be declared rather than mixed across terms.

For an ex-ante strategy forecast, future weight dispersion is unknown. The authors suggest that rebalancing frequency, turnover restrictions, or exposure limits could inform a strategy-specific model for $\Omega_w$. They do not provide such a fitted model or a closed-form turnover-to-risk mapping. A replication can verify the algebra on simulated independent weights and returns or estimate the decomposition on stored holdings, but claiming a validated prospective correction requires additional work beyond this source.

Return serial correlation is another separate issue. Even if monthly tracking variance is known, annual variance is not automatically twelve times monthly variance. It also contains lagged active-return covariance terms. The introduction acknowledges earlier work on this problem. The stochastic-weight decomposition does not remove it, and combining annualization assumptions with weight-drift adjustments without distinguishing them can obscure the actual source of forecast error.

## The absolute-deviation result is not established

Equation 3 defines a sample mean absolute deviation centered on the sample active-return mean, using a $1/(T-1)$ normalization. In Theorem 2, however, the proof switches to $E|w_t^\top r_{t+1}|$, an uncentered absolute-return moment. These are different risk measures if expected active return is nonzero.

The proof then effectively replaces $E|m_w^\top r|$ by $|m_w^\top\mu|$. This is not a valid equality: absolute value is convex, so generally $E|Z|\geq|EZ|$. The source's claimed upper bound,

$$
E|w_t^\top r|\leq |m_w^\top\mu|+E|v_t^\top r|,
$$

can fail even with fixed weights. Take $w=(1,-1)$, zero-mean asset returns with a nondegenerate difference, and $v=0$. The proposed right-hand side is zero, while the left-hand side is strictly positive. This is an independent counterexample to the theorem as printed. It also contradicts the accompanying claim that fixed-weight absolute tracking deviation equals the absolute expected active return.

The triangle inequality supplies the valid general bound

$$
E|(m_w+v)^\top r|\leq E|m_w^\top r|+E|v^\top r|.
$$

It does not justify replacing the first term by the absolute mean. Under independence and $Ev=0$, conditional Jensen also implies $E_v|(m_w+v)^\top r|\geq|m_w^\top r|$ for each fixed $r$, giving an ordering for the **uncentered** absolute-return moment after integrating over returns. This is a corrected mathematical observation under stronger assumptions, not the paper's reported theorem, and it does not automatically settle comparisons of centered sample MAD.

Finally, uncorrelated weights and returns do not imply $E|v^\top r|$ is near zero. Zero covariance controls signed products, not their absolute values. The source's remarks about many stocks require additional assumptions about scale and diversification. They are not demonstrated by uncorrelatedness alone.

## Evidence, practical use, and limits

The paper contains theoretical arguments and references to outside industry experience, not an original empirical sample or simulation study. Its mention that some annual tracking-error estimates may roughly double comes from cited or observed external calculations, without a reproducible dataset, strategy specification, or uncertainty analysis here. No universal multiplier is calibrated. The decomposition also does not establish a contractual conclusion about performance fees; it establishes that the risk target and measurement horizon need precise definitions.

For a practical implementation, align positions and subsequent returns, construct true active returns, and decide whether the target is current conditional risk or unconditional risk of a future strategy. Compare realized variance both with average holdings risk and with average conditional risk. Estimate or simulate the holdings process before using a prospective adjustment. Retain the source's three-term variance formula only when its constant conditional-moment assumptions are defensible.

The reliable takeaway is that strategy evolution belongs in a horizon-level risk forecast. The stronger claims that realized risk must exceed any planned figure, that every stochastic position produces a strictly positive increment, or that the absolute-deviation theorem is established are not supported by the calculations as written.
