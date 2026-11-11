# Nested Performance Attribution

Jose Menchero. *The Journal of Performance Measurement*, Fall 2004, pp. 41–50. Source: [PortfolioPerformance_Menchero_2004a.PDF](../../Finance/PortfolioPerformance_Menchero_2004a.PDF), 10 pages. The alternate library filename `PortfolioPerformance_Menchero2004a.PDF` represents the same work. This paper is distinct from Menchero's 2004 multiperiod arithmetic-attribution paper.

## Why this matters

An attribution system can reconcile perfectly to active return and still answer the wrong question. If a manager chooses securities directly, a sector-allocation effect can suggest a decision the manager never made. If a manager first chooses capitalization buckets, then styles within those buckets, and finally securities, a two-level sector/security report combines distinct decisions. Menchero provides a recursive accounting framework in which the attribution hierarchy follows the assumed investment process.

The central result is an exact, single-period decomposition, not an estimator of manager skill. At every node, a parent's within-group active return separates into allocation among its children and selection within those children. Repeating that identity produces as many levels as the decision process requires, with no residual. The same holdings and returns can legitimately produce different security-level effects under different hierarchies, because each effect measures a different conditional decision.

The contribution is narrower than inventing hierarchical attribution. Menchero credits Geenen and coauthors (2001) and Levecq (2004), develops their mathematical framework and aggregation identities, and proposes a holdings-level formula that treats a security as the final allocation category. The paper's practical novelty is the combination of a consistent recursion and a security contribution that recognizes both held securities and opportunities deliberately underweighted or not held.

## Scope, inputs, and notation

The maintained setting is a long-only, single-period, buy-and-hold portfolio. There is one common return for each security in the portfolio and benchmark. Let $w_k$ be portfolio weight, $b_k$ benchmark weight, and $r_k$ security return over the same period. The universe is the union of portfolio and benchmark constituents, so an unheld benchmark security has $w_k=0$, not a missing observation. Weights satisfy

$$
\sum_k w_k=\sum_k b_k=1,
\qquad R=\sum_k w_kr_k,
\qquad B=\sum_k b_kr_k.
$$

Returns and weights are dimensionless decimals in calculations. A return contribution of $0.0001$ is one basis point. The source's illustrative tables display weights, returns, and attribution effects as percentages; its prose also expresses effects in basis points. Convert percentage inputs to decimals before multiplication, then multiply the resulting return contribution by 10,000 to report basis points.

A hierarchy assigns every security to one child of each relevant parent. Its groups partition the universe. For node $g$, define portfolio and benchmark weights and within-group returns by

$$
W_g=\sum_{k\in g}w_k,\qquad
\bar W_g=\sum_{k\in g}b_k,
$$

$$
R_g=\frac{\sum_{k\in g}w_kr_k}{W_g},\qquad
B_g=\frac{\sum_{k\in g}b_kr_k}{\bar W_g}.
$$

At the root, $W_0=\bar W_0=1$, $R_0=R$, and $B_0=B$. Bars mark benchmark weights; $B_g$ is a benchmark return, not a weight. Distinguishing those objects is important because the source's successive levels use closely related notation.

The example requires only beginning weights, the security returns, and classification labels. It does not require forecasts, a covariance matrix, a risk model, an optimizer, or an estimate of expected alpha. Those additional inputs would be needed to interpret whether a realized allocation was a sensible ex ante choice, but they are outside this accounting exercise.

## A bottom-up attribution

For a manager who chooses securities without a preliminary sector decision, Menchero assigns security $k$ the contribution

$$
C_k^{(0)}=(w_k-b_k)(r_k-B).
$$

The active weight is measured relative to the benchmark security weight, and the security's performance is measured relative to the whole benchmark. Summing gives

$$
\sum_k C_k^{(0)}
=\sum_k(w_k-b_k)r_k-B\sum_k(w_k-b_k)
=R-B.
$$

The second term vanishes because the two sets of weights each sum to one. This proof explains why subtracting the benchmark return changes individual contributions without changing their total.

The sign has a direct interpretation. Overweighting an outperformer or underweighting an underperformer creates a positive contribution. Underweighting an outperformer or overweighting an underperformer creates a negative contribution. An unheld benchmark constituent can contribute positively or negatively, because omission is an active position relative to the benchmark.

The alternative holdings formula discussed in the paper is $w_k(r_k-B)$. It also sums to active return, but gives zero contribution to every unheld security and can assign a negative contribution to an underweighted underperformer that Menchero regards as a successful active decision. Reconciliation alone therefore does not select an economically appropriate attribution convention. The chosen formula should match the question being asked.

There is no contradiction between a security producing a positive realized return and receiving negative attribution. Attribution measures the portfolio's position relative to its benchmark opportunity cost. Nor does a positive contribution establish a correct forecast: a manager can benefit by accident, and classification does not identify the causal source of the investment decision.

## Two-level sector allocation and selection

For sector $i$, the allocation effect is

$$
A_i=(W_i-\bar W_i)(B_i-B),
$$

and the selection effect is

$$
S_i=W_i(R_i-B_i).
$$

Selection is weighted by the **portfolio** sector weight. Consequently, it combines what a benchmark-weighted Brinson presentation would call pure selection and interaction. To see this explicitly,

$$
W_i(R_i-B_i)
=\bar W_i(R_i-B_i)
 +(W_i-\bar W_i)(R_i-B_i).
$$

A report that also adds a separate interaction effect to Menchero's $S_i$ would double count it. This convention is not a minor display choice when sectors have materially different active weights.

Define the sector's total effect $T_i=A_i+S_i$. Expanding gives

$$
T_i=W_iR_i-\bar W_iB_i-(W_i-\bar W_i)B.
$$

Summing over sectors recovers $R-B$. Summing the bottom-up contributions of securities in sector $i$ recovers precisely this same $T_i$:

$$
\sum_{k\in i}(w_k-b_k)(r_k-B)=T_i.
$$

Thus a sector's total contribution aggregates consistently across the bottom-up and two-level views, even though its allocation and selection components change the explanation. Notice that $T_i$ is not simply the difference of sector-weighted returns $W_iR_i-\bar W_iB_i$. The latter omits the portfolio-wide benchmark opportunity-cost adjustment. Individual sectors' weight differences do not vanish; only their sum does.

Within sector $i$, define conditional weights $u_{ik}=w_k/W_i$ and $\bar u_{ik}=b_k/\bar W_i$. Security selection is

$$
C_{ik}^{(1)}=W_i(u_{ik}-\bar u_{ik})(r_k-B_i).
$$

Its sum over securities is $S_i$, because the conditional weights each sum to one. A stock can have positive bottom-up contribution and negative within-sector selection: its active position relative to its own sector may differ from its active position relative to the whole portfolio, and its relevant comparison return has changed from $B$ to $B_i$.

## Nested attribution and its proof

Now suppose sector $i$ contains subsectors $j$. Let $W_{ij}$ and $\bar W_{ij}$ be absolute weights, with conditional weights $u_{ij}=W_{ij}/W_i$ and $\bar u_{ij}=\bar W_{ij}/\bar W_i$. The subsector allocation effect is

$$
A_{ij}^{(2)}=W_i(u_{ij}-\bar u_{ij})(B_{ij}-B_i),
$$

and subsector selection is

$$
S_{ij}^{(2)}=W_{ij}(R_{ij}-B_{ij}).
$$

These satisfy $\sum_j(A_{ij}^{(2)}+S_{ij}^{(2)})=S_i$. The outer factor is $W_i$, the portfolio weight of the parent, not its benchmark weight. Omitting it converts the calculation into a return on the sector's internal capital rather than a contribution to the whole portfolio.

For a general parent $p$ and child $c$, use

$$
A_{p\to c}=W_p
\left(\frac{W_c}{W_p}-\frac{\bar W_c}{\bar W_p}\right)
(B_c-B_p),\qquad
S_c=W_c(R_c-B_c).
$$

The local accounting identity is

$$
\sum_{c\subset p}(A_{p\to c}+S_c)=W_p(R_p-B_p)=S_p.
$$

To verify it, the allocation sum is

$$
\sum_c A_{p\to c}
=\sum_c W_cB_c-W_p\sum_c\frac{\bar W_c}{\bar W_p}B_c
=\sum_c W_cB_c-W_pB_p,
$$

where the terms involving $B_p$ cancel because both conditional-weight systems sum to one. The selection sum is $W_pR_p-\sum_cW_cB_c$. Adding eliminates the intermediate benchmark returns. Applying the identity recursively replaces a parent's selection residual by the next level's allocations and selections.

At an individual-security leaf, $R_k=B_k=r_k$, so its own remaining selection residual is zero. Its allocation relative to its parent becomes the final security-selection contribution. Therefore the total active return equals the sum of allocation effects over all edges of the tree, including edges ending in securities. This is the unifying interpretation: a final security choice is an allocation decision at the most granular level.

The proof is local and telescopes. It permits different branches to have different depths, provided every branch ends in a complete partition and the same weighting conventions are used. It does not require balanced sector sizes or a common number of securities per node. However, changing the order of classifications changes intermediate benchmark returns and conditional weights, and therefore changes the allocations attributed to each decision.

## Complete numerical example

The source's twelve-stock example is synthetic. Each row supplies the full input needed to reproduce its single-period attribution. Large, medium, and small refer to size; value and growth are the nested style classifications.

| Security | Size | Style | Portfolio weight, % | Benchmark weight, % | Return, % |
|---|---|---|---:|---:|---:|
| AAA | Large | Value | 12.21 | 18.00 | 1.30 |
| BBB | Large | Value | 16.20 | 14.25 | 3.60 |
| CCC | Large | Growth | 8.32 | 18.31 | 7.35 |
| DDD | Large | Growth | 14.20 | 14.50 | 8.70 |
| EEE | Medium | Value | 7.29 | 6.40 | 4.70 |
| FFF | Medium | Value | 10.30 | 4.10 | 6.05 |
| GGG | Medium | Growth | 7.40 | 7.30 | 10.32 |
| HHH | Medium | Growth | 5.30 | 8.05 | 8.86 |
| III | Small | Value | 6.20 | 1.09 | 10.75 |
| JJJ | Small | Value | 3.45 | 1.44 | 8.46 |
| KKK | Small | Growth | 5.38 | 2.71 | 13.98 |
| LLL | Small | Growth | 3.75 | 3.85 | 11.42 |

Both weight columns sum to 100%. Recalculation from these displayed inputs gives $R=6.926634\%$, $B=6.427252\%$, and $R-B=49.9382$ basis points. The paper displays these as 6.93%, 6.43%, and 50 basis points. The extra digits here document arithmetic from the printed inputs; they do not imply more precise original data.

In the bottom-up view, AAA contributes 29.6868 basis points: it underperforms the benchmark, but the portfolio underweights it. CCC contributes −9.2183 basis points because its 7.35% return exceeds the benchmark return while the portfolio holds much less of it. JJJ contributes 4.0858 basis points because it is overweight and outperforms the overall benchmark. These agree with the paper's rounded +30, −9, and +4 basis points.

Aggregating first by size gives:

| Size | Portfolio weight, % | Benchmark weight, % | Portfolio return, % | Benchmark return, % | Allocation, bp | Selection, bp |
|---|---:|---:|---:|---:|---:|---:|
| Large | 50.93 | 65.06 | 5.08315 | 5.15568 | 17.9673 | −3.6938 |
| Medium | 30.29 | 25.85 | 7.25995 | 7.79667 | 6.0802 | −16.2572 |
| Small | 18.78 | 9.09 | 11.38841 | 11.63396 | 50.4530 | −4.6114 |
| Total | 100.00 | 100.00 | 6.92663 | 6.42725 | 74.5006 | −24.5624 |

The manager benefits strongly from an overweight to small stocks and an underweight to large stocks. Yet the portfolio underperforms each corresponding size benchmark internally. An attribution system that reports only the total +49.9382 basis points hides this distinction. Conversely, describing the internal shortfall as failed stock selection is premature if style allocation was a separate decision inside each size bucket.

Adding the style layer resolves that question. The exact reconstruction from the printed weights gives:

| Decision level | Contribution, bp |
|---|---:|
| Size allocation | 74.5006 |
| Style allocation within size | −54.0972 |
| Security selection within size/style | 29.5348 |
| Total | 49.9382 |

The paper's individually rounded +75, −54, and +30 basis points sum to +51, while the rounded total is +50. This is rounding, not a missing economic effect. Production reports should reconcile on unrounded values and disclose any display residual.

JJJ illustrates why attribution can change sign without inconsistency. It is overweight relative to the entire benchmark and earns more than the total benchmark, hence the +4 basis points in the bottom-up view. Inside small stocks, its portfolio conditional weight is approximately 18.37%, versus 15.84% in the small-stock benchmark; it earns 8.46% against the small-stock benchmark's approximately 11.63%. That is an overweight to a relative underperformer and gives approximately −2 basis points of size-relative selection.

Inside small value, however, JJJ's conditional portfolio weight is approximately 35.75%, versus 56.92% in the corresponding benchmark. The small-value benchmark earns approximately 9.45%, above JJJ's 8.46%. The manager underweights that within-style underperformer, producing approximately +2 basis points at the final security-selection level. The small-value allocation itself detracts approximately 10 basis points because the portfolio overweights a style that underperforms the broader small-stock benchmark. These are different conditional decisions, not three competing estimates of one immutable security alpha.

## Implementation and reconciliation controls

A minimal implementation first validates the security universe, missing returns, and weight normalization. It then aggregates from leaves upward to calculate $W_g$, $\bar W_g$, $R_g$, and $B_g$ at every node. Only after those quantities are available should it walk downward to calculate edge allocations. This avoids inconsistencies from using independently supplied sector returns that may not match the security data.

Useful controls are algebraic rather than statistical: children must sum to each parent's weights; each benchmark-parent return must equal the benchmark-weighted average of its children's returns; each local allocation-plus-selection sum must equal the parent residual; and the sum of all final effects must equal total active return. The complete numerical example above passes the final identity to floating-point precision, with a residual of approximately $-2.6\times10^{-18}$ in decimal return.

For a node with zero portfolio weight but positive benchmark weight, the conditional portfolio weight is undefined. The expanded expression

$$
A_{p\to c}=\left(W_c-W_p\frac{\bar W_c}{\bar W_p}\right)(B_c-B_p)
$$

avoids dividing by $W_p$. Similarly, the expanded within-parent security expression is $(w_k-W_pb_k/\bar W_p)(r_k-B_p)$. These forms supply a useful limiting implementation when a whole portfolio group is absent. They do not solve the case of zero benchmark weight: then $B_p$ and the benchmark conditional distribution are not defined by the original benchmark. A benchmark extension or explicit policy is needed. The paper's positive-weight example does not specify that policy.

A classification change is also an input change, not a cosmetic report change. An investment committee should fix the hierarchy from the investment mandate or documented workflow before examining realized results. Choosing whichever hierarchy produces the most flattering attribution is a form of explanatory hindsight. Maintaining several labeled views may be informative, but the differences should not be interpreted as independent evidence of several sources of skill.

One should not silently extend the formulas to daily trading within a monthly period. Beginning holdings times end-to-end returns cease to represent actual realized contributions when trades occur. Cash flows, fees, currencies, corporate actions, and transactions require consistent return/contribution conventions. The paper cites other work for multiperiod linking and long/short generalizations; it does not derive those extensions here. In particular, a signed weight of zero can conceal offsetting long and short positions, making conditional normalization problematic even when gross exposure is substantial.

## Interpretation, limits, and reproducibility

The paper supplies an exact answer to an accounting question: given a benchmark, a classification hierarchy, and a single-period holdings model, which conditional allocation decisions account for realized active return? It does not prove that the manager consciously made those decisions, that the hierarchy is unique, or that the realized contributions forecast future performance. A covariance-based risk attribution would answer another question and should not be read into these formulas.

All inputs to the twelve-stock demonstration are printed, so the numerical example is reproducible without external market data. The remaining implementation choices are explicit extensions: treatment of absent benchmark sectors, within-period trading, short positions, fees, and multiperiod linking. An actual manager study would also require dated holdings, the appropriate benchmark version, corporate-action adjustments, consistent prices, and contemporaneous evidence of the decision hierarchy. Those are not missing inputs to the synthetic example; they are missing inputs to an empirical application.

The most useful result for a quantitative investment process is the recursive identity. It lets the organization ask whether broad allocations helped, whether conditional allocations offset them, and whether final security choices added value, while preserving a single reconciled total. The example shows why the economic interpretation must travel with the hierarchy: +4, −2, and +2 basis points for JJJ are all defensible only when their reference decisions are stated.

## Source and verification record

All ten PDF pages, including endnotes and references, were read. PDF pages 3–8 were visually checked for the holdings table, attribution equations, hierarchy diagrams, and numerical examples. The note's high-precision example was independently recomputed from the printed twelve-stock inputs. The resulting total and all hierarchy levels reconcile; no empirical return series or statistical skill test is claimed. Companion scratch files for this batch contain the numerical reconstruction and the recursive identity audit.
