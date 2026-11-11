# Comparison of the Different Brinson Methods

Undated four-page methods document, without a named author in the supplied pages. Source: [PortfolioPerformance_Axioma.PDF](../../Finance/PortfolioPerformance_Axioma.PDF). It describes three attribution methods implemented in the Poseidon API and cites Brinson-Hood-Beebower, Brinson-Fachler, Litterman, and Bacon. A filename alone is insufficient to establish individual authorship.

## Why this matters

Two correct attribution systems can give different sector allocation effects because they use different reference returns. This document compares a cash-relative allocation convention, a benchmark-relative convention, and a two-effect version that folds interaction into selection. Its central algebra clarifies why benchmark-relative effects need not add to the raw active contribution of each sector even though they add to total active return across sectors.

The source treats some of these differences as correctness failures. A more precise reading is that they allocate the same total return relative to different counterfactuals. An implementation should preserve the chosen convention and explain the group-level reconciliation rather than silently switch definitions when market returns are negative.

## Inputs and assumptions

For one period, let portfolio asset weights be $w_k$ and benchmark weights $b_k$, with common asset return $r_k$. For a nonoverlapping group $g$, define $W_g=\sum_{k\in g}w_k$, $B_g=\sum_{k\in g}b_k$, and within-group returns $P_g=\sum_{k\in g}w_kr_k/W_g$, $R_g=\sum_{k\in g}b_kr_k/B_g$. The raw active contribution is

$
C_g=W_gP_g-B_gR_g.
$

The overall benchmark return is $R_B=\sum_gB_gR_g$. For the standard portfolio-level identities assume both sets of weights sum to one. Weights should refer to the same start-of-period or otherwise consistently defined exposure basis. Cash, missing groups, shorts, and off-benchmark holdings require explicit policies.

Normalized group returns are undefined at zero group weight. In particular, an off-benchmark sector with $B_g=0$ needs a reference return even though the displayed benchmark-weight formula cannot produce one. A zero **net** group weight can also conceal offsetting long and short assets. The four-page note does not define these production cases, multi-period linking, flows, corporate actions, currency attribution, or transaction costs.

## Method 1: raw group-return allocation

The first method uses

$
S_g=B_g(P_g-R_g),\quad A_g^{(1)}=(W_g-B_g)R_g,\quad I_g=(W_g-B_g)(P_g-R_g).
$

Expansion immediately gives $C_g=A_g^{(1)}+S_g+I_g$. This is a group-by-group exact identity. Interaction measures the joint effect of changing the group weight and changing its within-group return. It is not mathematically meaningless, even if it is not a separately controlled management decision.

If a sector's benchmark return is negative, overweighting it produces a negative allocation effect under this convention, even if the sector loses less than the whole benchmark. The source calls this incorrect. It is more accurate to say the comparison is against a zero-return/cash reference rather than against the benchmark's alternative opportunity. The arithmetic still reconciles exactly.

## Method 2: benchmark-relative allocation

Keep $S_g$ and $I_g$, but replace allocation by

$
A_g^{(2)}=(W_g-B_g)(R_g-R_B).
$

Now overweighting an outperforming sector has a positive allocation effect even when its absolute return is negative. At group level,

$
C_g=A_g^{(2)}+S_g+I_g+(W_g-B_g)R_B.
$

The final term is the explicit reconciliation to raw group active contribution. It is not an unexplained numerical residual. Summing over groups eliminates it whenever $\sum_gW_g=\sum_gB_g$, so total attribution is exact. Thus the source's statement that decomposition is “broken” applies only if one insists on raw group contribution as the quantity attributed by each row; it is not a failure to reconcile total active return.

If leverage, cash coverage, or benchmark normalization makes weight totals differ, the reconciliation term does not disappear. The right fix is to include all exposures and funding consistently or retain the residual, not to assume the fully invested cancellation.

## Method 3: fold interaction into selection

The two-effect variant uses

$
S_g^{(3)}=W_g(P_g-R_g)=S_g+I_g,
\qquad A_g^{(3)}=A_g^{(2)}.
$

There is no separately displayed interaction. Its economics have not vanished; the joint weight/selection effect has been assigned to selection. The same group reconciliation term remains:

$
C_g=A_g^{(3)}+S_g^{(3)}+(W_g-B_g)R_B.
$

This can be a useful reporting convention if the manager takes responsibility for selection at actual allocated weights. Conversely, benchmark-weighted selection is useful for a counterfactual holding group allocation fixed. Neither partition uniquely identifies causal manager decisions from observed returns alone.

## Numerical reconstruction

The following independent example checks the identities; it is not a dataset reported in the source. Take two groups, with benchmark weights 50/50, portfolio weights 60/40, and equal portfolio and benchmark within-group returns of -5% and -15%. The benchmark loses 10%, the portfolio loses 9%, and active return is +1 percentage point.

Method 1 allocates -0.5 points to the overweight first group and +1.5 points to underweighting the second, totaling +1. Method 2 allocates +0.5 to each. Its first row differs from raw active contribution by -1 point, and the second by +1 point: these are exactly $(W_g-B_g)R_B$. Selection and interaction are zero because within-group returns match. This demonstrates that negative returns are compatible with both valid identities and that row meanings differ.

For a nonzero interaction check, let one group's active weight be 0.10 and its within-group excess return be 0.02. Interaction is 0.002, or 0.2 percentage points. Moving from Method 2 to Method 3 adds exactly that amount to selection and removes the separate interaction entry, leaving the group aggregate unchanged.

## Implementation and source limits

Build all group contributions from a shared asset-return and weight table, validate normalized weight totals, and compute the three definitions side by side. Reconcile each group using its declared reference and reconcile the portfolio using the budget condition. Distinguish percentage points of return from relative percentages. A meaningful verification compares the sums to directly calculated $\sum_kw_kr_k-\sum_kb_kr_k$ rather than testing only one formula against a rewritten copy of itself.

The document offers an algebraic comparison, not an empirical evaluation of attribution quality. Its preference for Method 2 and its criticism of interaction are judgments about interpretation. There is no experiment showing one method identifies actual investment skill better. The reusable result is the exact set of identities and the budget condition under which benchmark-relative row adjustments cancel.
