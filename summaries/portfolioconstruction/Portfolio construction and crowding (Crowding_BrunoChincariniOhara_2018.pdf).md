# Portfolio construction and crowding

Salvatore Bruno, Ludwig B. Chincarini, and Frank Ohara. *Journal of Empirical Finance* 47 (2018), 190–206. DOI: 10.1016/j.jempfin.2018.02.003. Source: [original PDF](../../Finance/Crowding_BrunoChincariniOhara_2018.pdf), 17 pages, including the complete optimization appendix. References below use journal pages and numbered exhibits/equations.

## Why this matters

Different investment managers can hold similar portfolios even when their expected-return signals are unrelated. Shared covariance models and shared portfolio constraints map heterogeneous signals into a much smaller set of feasible, apparently attractive exposures. Diversification across alpha models alone may therefore exaggerate diversification across implemented portfolios.

The paper tests this mechanism using 100 randomly generated alpha signals, real US stock data, and three commercial risk models. Its strongest empirical result concerns long-only portfolios: imposing the usual fully invested constraint creates much more positive holdings similarity than unconstrained signal optimization. A spectral modification of the covariance matrix and diversification across risk-model providers both reduce measured similarity in these simulations.

The contribution is a portfolio-construction experiment and a tractable holdings-similarity measure. The paper does not observe managers' proprietary alpha forecasts, establish the causes of a historical liquidation episode, or estimate a causal relation between its crowding statistic and market impact. Its systemic-risk conclusions are interpretations of simulated portfolio overlap, not measured losses in a fire-sale model.

## What the crowding measure actually measures

Let $w_i\in\mathbb R^N$ be manager $i$'s vector of stock weights, and let $M$ be the number of managers. Pairwise similarity is the cosine

$$
s_{ij}=\frac{w_i'w_j}{\sqrt{w_i'w_i}\sqrt{w_j'w_j}}.
$$

Normalize every nonzero weight vector to unit Euclidean length and arrange the columns in $Q$. The similarity matrix is $S=Q'Q$, with unit diagonal. The aggregate statistic is

$$
C=\frac{\sum_{i=1}^M\sum_{j=1}^M s_{ij}-M}{M^2-M}.
$$

This is the average signed cosine across distinct pairs. Counting each unordered pair once gives the same number. The measure ignores overall position scale: doubling one manager's entire portfolio does not change it. Consequently it does not incorporate assets under management, market depth, or the dollar amount that would have to be liquidated.

For long-only portfolios, similarities are nonnegative and a high $C$ straightforwardly indicates overlapping allocation directions. In long-short portfolios, opposite directions have negative similarity and can cancel positive similarities in the average. A value near zero does not establish that every pair is dissimilar. The paper partly addresses this by also examining the dispersion of pairwise similarities.

The same construction is applied to alpha vectors, producing $C_\alpha$, and to optimized holdings, producing $C_p$. The relative measure is

$$
\Omega=\frac{C_p}{C_\alpha}.
$$

Independent symmetric random signals have expected signed similarity zero. Their finite-sample average can be tiny, positive, or negative, making this ratio unstable. Tables containing very large or negative $\Omega$ values should not be read as stable multiplicative measures of systemic risk. In Table 3, for example, positive long-only crowding is accompanied by ratios near minus 80,000 because the denominator is very slightly negative.

The paper also reports S.D.R., the ratio of cross-sectional standard deviations of portfolio and signal similarities, averaged through time. This is a standard-deviation ratio, not a variance ratio. An S.D.R. of 1.08 corresponds to approximately 16.6% more variance if interpreted as a single ratio, not 8% more variance. The alpha rows report the level of signal-similarity dispersion rather than a ratio to itself.

The simple three-portfolio example in Section 2 uses columns $(0.4,0.4,0.2)'$, $(0.8,0.1,0.1)'$, and $(0.45,0.45,0.1)'$. Pairwise cosines are approximately 0.7796, 0.9831, and 0.7930, producing $C=0.8519$. This offers a small unit test for normalization and exclusion of the diagonal.

## The optimization mechanism and its limits

For the conventional unconstrained mean-variance objective

$$
\max_w\left\{\alpha'w-\frac{\lambda}{2}w'\Sigma w\right\},
$$

the solution is $w=\lambda^{-1}\Sigma^{-1}\alpha$. With $\Sigma=U\Lambda U'$, it becomes

$$
w=\frac{1}{\lambda}\sum_{k=1}^N u_k\frac{u_k'\alpha}{\lambda_k}.
$$

Small covariance eigenvalues amplify alpha projections in their directions. This explains why small estimated-risk directions can have disproportionate influence. It does not prove that all alpha vectors converge to the same signed portfolio: the projection can be positive or negative, can vanish, and may be spread over several close eigenvalues. Indeed, under independent centrally symmetric zero-mean alphas and an unconstrained common linear map, expected signed pairwise cosine remains zero by symmetry. Positive long-only similarity requires attention to the constraints as well as the inverse covariance.

The paper's language that expected returns matter relatively little should therefore be understood as a warning about conditioning, not a general limit theorem for arbitrary alpha inputs. Its constraint experiments later show that the fully invested long-only requirement is the dominant contributor to positive $C$ in the specified design.

The worked covariance example has unit variances and correlation 0.9 between stocks 1 and 2, with stock 3 independent. Its eigenvalues are 0.1, 1, and 1.9. The normalized inverse-covariance allocation $w=\Sigma^{-1}\alpha/(\mathbf1'\Sigma^{-1}\alpha)$ gives approximately $(25.64,25.64,48.72)\%$ for equal alphas 0.1. Increasing the first alpha to 0.12 produces $(73.17,-19.51,46.34)\%$. Increasing the third alpha to 0.12 as well gives $(66.96,-17.86,50.89)\%$, calculated directly from the displayed matrix. The paper prints the first weight of the last example near 70%; that printed triplet does not sum to 100%. These examples concern normalized inverse-covariance portfolios, which should not be confused with the general fully invested fixed-risk-aversion solution.

## The Marchenko–Pastur adjustment

The authors interpret much of the covariance spectrum as sampling noise, using a random-matrix benchmark. For an independent unit-variance $T\times N$ data matrix $X$ and covariance $X'X/T$, define $q=N/T$. The standard Marchenko–Pastur continuous density has support

$$
\lambda_-=(1-\sqrt q)^2,\qquad \lambda_+=(1+\sqrt q)^2,
$$

and density

$$
p(x)=\frac{\sqrt{(\lambda_+-x)(x-\lambda_-)}}{2\pi qx},\quad x\in[\lambda_-,\lambda_+].
$$

If $q>1$, there is additionally a mass at zero. The paper prints $p=T/N$ while using formulas associated with $N/T$. A replication must choose a consistent convention; the expressions above correct the aspect-ratio notation rather than silently mixing definitions.

The proposed MPA method retains the eigenvalues above the upper noise threshold and reconstructs covariance from their eigenvectors:

$$
\Sigma_{\rm MPA}=U_K\Lambda_KU_K'.
$$

Here $K$ is the set of retained modes. The paper does not specify replacing discarded eigenvalues by a positive floor, their average, or a residual diagonal. This matters because the displayed reconstruction is rank deficient whenever fewer than $N$ modes survive. It assigns zero risk to the discarded subspace. In an unconstrained alpha maximization this can create unbounded or nonunique solutions; in bounded portfolio problems the solution can depend on constraints and numerical treatment of the nullspace.

A positive spectral floor might be a useful modification, but it would be an additional estimator and should not be represented as the authors' procedure. Exact replication needs their implementation or an explicit declaration of how the singular matrix is handled. The paper's intuition of suppressing noisy eigenvectors is not by itself a proof that zeroing their variances makes subsequent optimization safer.

The random-matrix null also assumes a particular scale and independent standardized observations. Applying its unit-variance threshold directly to heterogeneous stock covariance or to a commercial structured factor covariance is not automatically justified. The report does not fully specify the whitening, variance normalization, or calibration that reconciles those objects. Its classification of modes as noise is consequently a heuristic diagnostic rather than a formal test of every commercial-model eigenvalue.

For exponentially weighted observations, the paper uses the sum of decay weights as an effective history length: $T_{\rm eff}=1/(1-\delta)$, with $\delta=2^{-1/h}$ for half-life $h$ measured in daily observations. A two-year half-life of approximately 504 trading days produces about 728 effective days. This differs from the effective sample size of a weighted mean, $(\sum a_t)^2/\sum a_t^2=(1+\delta)/(1-\delta)$ for an infinite geometric sequence. Replacing one by the other changes the threshold; retain and disclose the paper's convention when reproducing it.

## Data and signal generation

The stock universe comprises the 3,000 largest US stocks, updated monthly, over 2006–2013. Returns are obtained through FactSet. The risk inputs come from Barra USE4, Northfield US Fundamental, and Axioma US Robust. Securities are matched by CUSIP, and portfolio comparisons use the common universe covered by the risk models. The paper anonymizes the empirical columns as Risk Models 1, 2, and 3; it does not disclose which provider corresponds to each column.

For every month the authors generate 100 random alpha vectors. Their cross-stock covariance is diagonal, with variances related to the historical variances of individual stock returns, so the draws are not necessarily identically scaled across stocks. The same alpha inputs are used for all three risk models, allowing the effect of the risk model to be compared while holding the signal realization fixed. The expected correlation across managers' alpha signals is zero.

The article does not publish the complete random seeds, the exact historical window used to scale every alpha draw, all vendor model vintages, the monthly timestamps of risk-model snapshots, or the full matched security panel. Those inputs are necessary for bit-for-bit reproduction. A new implementation should preserve the monthly matching and common-alpha design and label any choices used to fill these gaps.

This is primarily an experiment in holdings geometry. The simulated alphas are not fitted to future returns, and the paper does not claim that their realized investment Sharpe ratios establish profitable alpha. Common constraints, covariance estimates, and random signals generate the objects on which crowding is measured.

## Portfolio programs and source inconsistencies

The appendix describes alpha maximization at a target variance. For long-only holdings, the displayed program is

$$
\max_w\alpha'w\quad\text{subject to}\quad
w'\Sigma w=\sigma_{S\&P500}^2,\quad
\mathbf1'w=1,\quad0\leq w_i\leq0.10,\quad Sw=s_{\rm benchmark}.
$$

The benchmark sector weights are those of the capitalization-weighted 3,000-stock universe; $S$ is its sector-membership matrix. The target volatility is estimated from 60 months of S&P 500 returns. If that volatility is infeasible, the closest feasible level is used, without a fully specified numerical selection rule.

Equality to a quadratic risk target is not the same as the convex risk-cap formulation $w'\Sigma w\leq\sigma^2$. A replication must identify which is actually solved. Moreover, the table captions describe volatility minimization, and the main text discusses a target alpha equal to half a historical S&P 500 volatility scale. These are related efficient-frontier formulations only when their targets are matched appropriately. The article does not fully reconcile the reported implementation with the appendix's target-risk formulation. It would be inaccurate to present a single perfectly specified program as unambiguously generating every table.

For market-neutral portfolios the intended restrictions are zero net investment, a gross-exposure limit of two, sector neutrality, beta neutrality, and weights between minus and plus 10%. CAPM betas use five years of historical returns. The text states a target volatility of 5%, but Equation 29 sets $w'\Sigma w=0.05$. Since the left side is variance, 5% volatility would require 0.0025 in decimal-return units. The printed equation corresponds instead to approximately 22.36% volatility if annual variance is intended. The paper does not resolve which convention the implementation used.

The appendix constructs nonnegative buy and sell legs, $w=w^B-w^S$, and imposes $\mathbf1'w^B=\mathbf1'w^S=1$. This guarantees net zero and actual gross exposure at most two. It need not guarantee exactly two because the same stock can appear in both legs. The proposed penalty $-\lambda(\mathbf1'w^B+\mathbf1'w^S)$ is constant under those exact leg-budget equalities, so it cannot remove overlapping buy and sell positions as written. One must distinguish this mathematical issue from a practical implementation that may have used inequalities or additional restrictions.

The liquidity version bounds a position by a fraction of average daily dollar trading volume. With portfolio value $V_t$, the intended symmetric bound is

$$
|w_{it}|\leq\min\left(0.10,\frac{c\,ADTV_{it}}{V_t}\right).
$$

The study discusses a 30% volume threshold; Appendix A.3 cites 15% as a typical industry value. Portfolio notional, the ADTV estimation window, and whether the constraint should apply to a position or an incremental trade are not sufficiently documented to reproduce the liquidity cases exactly. Borrow availability is explicitly excluded. Costs and turnover penalties are not part of the main comparison.

MATLAB and CPLEX are used, with the authors reporting substantial computational difficulties in versions before MATLAB 2014a. Solver tolerances, treatment of singular MPA covariance, infeasibility fallback, and the complete optimization code are absent. Those are material omissions given the formulations above.

## Main empirical results

Tables 1 and 2 average monthly statistics within 2006–2009 and 2010–2013. The clearest comparison is the raw long-only crowding measure:

| Period | Risk model | Regular $C$ | MPA $C$ |
|---|---|---:|---:|
| 2006–2009 | 1 | 0.85 | 0.73 |
| 2006–2009 | 2 | 0.86 | 0.73 |
| 2006–2009 | 3 | 0.86 | 0.72 |
| 2010–2013 | 1 | 0.71 | 0.57 |
| 2010–2013 | 2 | 0.71 | 0.57 |
| 2010–2013 | 3 | 0.70 | 0.56 |

Thus the adjustment reduces long-only similarity by roughly 14–16% in the first period and about 20% in the second, using the rounded table values. The source marks differences between original portfolio and alpha crowding, and between MPA and regular crowding, as significant at the 99% level. It does not give enough information about the test statistic, treatment of dependent portfolio pairs, or time-series dependence to reconstruct those significance claims independently.

Market-neutral raw crowding is zero to the displayed two decimals. Its relative ratios are unstable and sometimes negative. In 2006–2009 the unadjusted S.D.R. values for ordinary market-neutral portfolios are 1.016, 1.020, and 1.029; MPA gives approximately 1.000 in each case. With liquidity constraints, the corresponding values are 1.038, 1.056, and 1.070, versus roughly 1.008–1.009 after MPA. In 2010–2013, liquidity-constrained regular values reach 1.083–1.084 for two models. These results support an effect on the distribution of pairwise similarity even when the signed average hides it.

They do not establish that market-neutral portfolios have large positive aggregate overlap comparable to long-only portfolios. Nor do they justify treating the noisy ratio $\Omega$ as a reliable risk multiplier. Figure 4's similarity distributions are useful precisely because they preserve information that the signed mean discards.

## Which constraints generate the effect?

Table 3 repeats the comparison during 2009, progressively adding restrictions. In Scenario 1 the long-only optimization retains nonnegative positions, but removes full investment and sector restrictions and allows positions up to one. Market-neutral portfolios have no net, gross, sector, or long-short bounds. This is described as the unconstrained baseline, although the long-only case still has sign restrictions.

Scenario 2 adds full investment for long-only portfolios and net-zero/gross restrictions for market-neutral portfolios. Scenario 3 adds sector matching or sector neutrality. Scenario 4 adds 10% position bounds and beta neutrality for the market-neutral case.

The regular long-only $C$ values are only 0.03, 0.04, and 0.05 in Scenario 1. They jump to 0.91, 0.91, and 0.92 when the investment-budget constraint is added. Subsequent sector and position restrictions leave them near 0.89. The MPA values in Scenario 2 are 0.70, 0.75, and 0.75; in Scenario 4 they are about 0.78 for all three models.

This decomposition changes the interpretation of the paper. A common inverse-covariance map is not by itself sufficient to explain the large positive crowding measure. Fully investing a portfolio that cannot short forces managers into a shared positive region of the weight space, and the common risk model helps determine where within that region they concentrate. The result is about a joint construction pipeline, not merely a correlation between alpha models.

For market-neutral portfolios, the signed mean remains small. In the lightly constrained case, however, S.D.R. can reach 1.29, 1.53, and 1.58, while the MPA alternatives are near one. This indicates more dispersed pairwise alignments, consistent with both similarly and oppositely directed exposures being strengthened.

## Diversifying the risk models across managers

The final experiment mixes portfolios generated by different providers. For each month, the authors sample manager portfolios from the three risk-model populations in specified proportions, preserving the associated alpha vectors, and compute aggregate similarity. A 90/10/0 mix, for example, uses 90 portfolios constructed with one model and 10 with another.

Table 4 reports that a single-provider long-only population has $C$ around 0.85–0.86 during 2006–2009. A 33/33/34 split across providers produces 0.51, roughly a 40% reduction. Other mixtures differ: a 45/45/10 allocation gives 0.52, whereas 45/10/45 gives 0.63. Hence it is the interaction of specific models, not simply the count of vendors, that matters.

The market-neutral result is mixed. The equal-provider split has $\Omega=1.92$, exceeding the ratios for all three single-provider populations in that period. The authors acknowledge that other combinations yield lower relative crowding. Because the denominator is near zero, this part of the comparison should be interpreted especially cautiously.

No equilibrium price response is solved, and no financing shock or liquidation process is simulated. The policy suggestion that provider diversity can reduce systemic concentration is plausible within the long-only portfolio experiment, but the strength of a resulting reduction in financial-system risk is not quantified.

## A faithful reconstruction and the remaining uncertainties

A useful reproduction should maintain a month-by-month audit trail containing the matched universe, point-in-time model covariance, signal random seed and scaling, portfolio program and target, solver status, MPA eigenvalue threshold and normalization, all final weights, and both signed similarity distributions and their summaries. It should recompute the toy similarity example before attempting the commercial-model experiment.

Several source issues must remain visible: the inconsistent Marchenko–Pastur aspect ratio; unspecified covariance scaling; the singularity of the spectral reconstruction; the target-alpha versus target-risk formulation; the 5% variance/volatility mismatch; the constant leg-budget penalty; and missing liquidity notionals and solver settings. Correcting them may produce a better-defined extension, but cannot be claimed to recover the original unpublished code exactly.

The paper's durable finding is narrower and more useful than a universal claim that optimization causes systemic crises. Under realistic shared long-only mandates, independent signals can become strongly aligned positions. Evaluating diversification after risk modeling and constraints, and inspecting full distributions of exposure similarity, reveals a source of concentration that signal correlations alone will miss.
