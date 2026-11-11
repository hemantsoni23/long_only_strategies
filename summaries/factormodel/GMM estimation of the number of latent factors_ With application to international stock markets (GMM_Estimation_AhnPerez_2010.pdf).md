# GMM estimation of the number of latent factors: With application to international stock markets

Seung C. Ahn and M. Fabricio Perez (2010), *Journal of Empirical Finance* 17, 783–802, DOI 10.1016/j.jempfin.2010.04.005. [Source PDF](../../Finance/GMM_Estimation_AhnPerez_2010.pdf). All 20 pages, including both mathematical and implementation appendices, were read. The rank arguments, GMM specification, selection criteria, simulation tables, and international-market results were checked visually.

## Why this matters

Counting latent factors is difficult when a panel has many dates but only a few assets or portfolios. Procedures justified by both dimensions tending to infinity may perform poorly in precisely that setting. Ahn and Perez turn factor counting into an instrumental-variable specification problem: partition returns into two groups, use one group as instruments for a regression system within the other, and find how many return regressors are needed to explain the cross-group covariance.

The contribution is a computationally simple GMM construction, two factor-count selection rules, and an extension that counts latent directions associated with externally observed candidate factors. It can accommodate heteroskedasticity and serial correlation when the time dimension is large, provided the cross-sectional error orthogonality needed by the return instruments holds. A transposed construction exchanges those restrictions when the cross-sectional dimension is large and time is short.

The paper’s strongest exact-factor result is useful. Some broader statements require additional rank conditions or numerical qualifications. In particular, the local-factor extension equates a cross-covariance rank with the minimum of two loading ranks, which is not generally valid. Repeating random partitions is a practical sensitivity exercise, not a theorem guaranteeing that every local or weak factor will be found. The empirical evidence supports a dominant common direction plus possible regional directions; it does not directly estimate a global factor’s correlation coefficient or establish integration of asset prices.

## Model and the two asymptotic regimes

The starting model is

$$
r_t=\alpha+Bf_t+\varepsilon_t,
$$

where $r_t\in\mathbb R^N$, $f_t\in\mathbb R^{L_0}$, and $B$ is $N\times L_0$. Intercepts absorb factor means, so take $E[f_t]=0$. The number of factors is the minimal dimension of the common component, requiring $\operatorname{rank}(B)=L_0$ and a positive-definite limiting factor second-moment matrix $\Omega_f$.

For fixed $N$ and $T\to\infty$, the source assumes finite factor moments through order four; error orthogonality to current and past factors, $E[\varepsilon_{it}\mid f_1,\ldots,f_t]=0$; and no contemporaneous cross-sectional idiosyncratic covariance, $E[\varepsilon_{it}\varepsilon_{jt}]=0$ for $i\ne j$. Serially dependent and heteroskedastic errors are permitted under mixing and central-limit conditions. Future factors may be correlated with current errors; strict exogeneity is not imposed.

The sufficient mixing condition is expressed as bounded $m^\lambda|\alpha(m)|$ for some $\lambda>2$, alongside the stated moment and central-limit assumptions. The operational requirement is a joint central limit theorem for the means of errors, factor–error products, and centered error cross-products. One must also have the relevant laws of large numbers, finite limiting covariance matrices, and the nonsingularity conditions used in GMM. Unit roots are outside this framework.

Assumption E contains a visible centering error: it defines a vector involving $\operatorname{vech}(\varepsilon_t\varepsilon_t'-\Psi_t)$ but prints $\Psi_t=E[r_tr_t']$. For that vector to have a centered CLT, the appropriate centering is $E[\varepsilon_t\varepsilon_t']$, not the return second moment containing intercept and factor components. This correction is required by the displayed construction.

The exact-factor assumption is substantive. Allowing a general residual covariance across assets while using other assets as contemporaneous instruments would invalidate the moment conditions. It is not repaired merely by estimating a heteroskedasticity-robust weighting matrix.

## Partitioned moment conditions and the rank identification argument

Partition $r_t=(g_t',z_t')'$ into $P$ response-group variables and $Q$ instrument-group variables, with $P+Q=N$. Both group sizes must exceed the factor count for the intended overidentified test. For a candidate count $L$, split $g_t=(y_t',x_t')'$ with dimensions $P-L$ and $L$. Fit the system

$$
y_t=a+Sx_t+u_t,
\qquad q_t=(1,z_t')',
\qquad E[q_tu_t']=0.
$$

Each of the $P-L$ equations uses the same $Q+1$ instruments. There are $(P-L)(Q+1)$ moments and $(P-L)(L+1)$ coefficients, including intercepts. Under regular identification, the overidentification count is

$$
d_L=(P-L)(Q-L).
$$

The core identification proof is short enough to reconstruct. Let $B_y,B_x,B_z$ be the corresponding loading matrices. Taking $a=\alpha_y-S\alpha_x$ removes the means. Cross-group error orthogonality gives

$$
E[(z_t-Ez_t)u_t']=B_z\Omega_f(B_y-SB_x)'.
$$

If $B_z$ has full column rank $L_0$ and $\Omega_f$ is nonsingular, the moments vanish exactly when $B_y=SB_x$. With $L=L_0$ and nonsingular square $B_x$, the unique solution is $S=B_yB_x^{-1}$. With $L<L_0$, the $L$ rows of $B_x$ cannot span all the loading directions in $g_t$ under the source’s full-rank-subset assumption. Some covariance remains unexplained. With $L>L_0$, redundant return regressors generally leave multiple coefficient vectors satisfying the population moments.

This argument shows why the source imposes a strong partition condition: every relevant subset containing enough variables must carry all factor directions. The condition is not implied merely by full rank of the complete loading matrix. Poorly chosen regressors or instrument groups can fail to identify factors even when the complete panel contains them.

There is also a direct data interpretation. In an exact factor model,

$$
C_{zg}=\operatorname{Cov}(z_t,g_t)=B_z\Omega_f B_g'.
$$

The regression system attempts to span the columns of this cross-covariance matrix using the selected $x$ columns. Its natural target is the rank visible across the partition. Under full loading rank in both groups, that rank equals $L_0$.

## Closed-form GMM implementation

Define $m_t(b)=\operatorname{vec}(q_tu_t')$ and $\bar m_T(b)=T^{-1}\sum_t m_t(b)$. For a positive-definite covariance-style weight $W_T(L)$, minimize

$$
c_T(b;L)=T\bar m_T(b)'W_T(L)^{-1}\bar m_T(b).
$$

The paper denotes $W_T$ as a weighting matrix, but it is its inverse that enters the quadratic criterion. Distinguish these conventions in code.

Here is a closed-form reconstruction with an explicit parameter ordering. Put $w_t=(1,x_t')'$ and let $A=[a\ S]$, a $(P-L)\times(L+1)$ coefficient matrix. Stack coefficients equation by equation as $\theta=\operatorname{vec}(A')$. Then

$$
d=\operatorname{vec}\left(T^{-1}\sum_t q_ty_t'\right),
\quad K=T^{-1}\sum_t q_tw_t',
\quad G=I_{P-L}\otimes K,
\quad \bar m_T(\theta)=d-G\theta.
$$

For full-rank $G$,

$$
\hat\theta=(G'W_T^{-1}G)^{-1}G'W_T^{-1}d.
$$

This avoids nonlinear optimization. A practical two-step estimator obtains preliminary residuals using a fixed positive-definite initial weight, estimates the covariance of the moment contributions, then resolves the weighted linear system. The source does not fully specify initial-weight or iteration conventions. A pseudoinverse can compute a minimum when sample matrices are rank deficient, but it does not restore identification or validate the nominal degrees of freedom.

For serially uncorrelated moment contributions, use a White-type estimate $T^{-1}\sum_t(m_t-\bar m)(m_t-\bar m)'$. For dependence, estimate the long-run covariance using a HAC kernel and bandwidth. The simulation uses Newey–West bandwidths zero and three. The zero-bandwidth version reduces to the heteroskedasticity-only matrix. Appendix A reverses the descriptions of when White versus HAC should be used; the main-text footnote and simulations have the correct ordering.

At the correctly specified identified count, let $D$ be the population derivative of the moment vector and let $W$ equal its long-run covariance. Whitening the central-limit vector and projecting away the column space of $W^{-1/2}D$ leaves a standard-normal quadratic form with rank equal to the number of moments minus the number of identified coefficients. Hence

$$
J_T(L_0)=\min_b c_T(b;L_0)
\Rightarrow\chi^2_{(P-L_0)(Q-L_0)}.
$$

For a nonoptimal positive-definite weight, the limit is a weighted sum of independent chi-squared variables, rather than that nominal chi-squared law. Underfitting leaves a nonzero population moment discrepancy, so $c_T/T$ converges to a positive constant and $c_T$ diverges. These are the two facts used to select the count. The paper does not supply a regular chi-squared interpretation for an overfitted, unidentified system.

## Sequential tests, information criteria, and random partitions

The sequential method starts with $L=0$, estimates using the optimal long-run covariance, and tests the moment restrictions. If rejected, increment $L$ and repeat until the first nonrejection. For consistent count selection, its significance level must decline to zero without doing so exponentially fast: $\eta_T\to0$ and $-\log(\eta_T)/T\to0$. The simulations use

$$
\eta_T=0.05\sqrt{500/T},
$$

which equals 5% at $T=500$. Nonrejection at a fixed finite sample is not a proof that the selected count is true. A reproduction should also specify what happens if every admissible count is rejected.

The model-selection method minimizes

$$
MS_T(L)=\frac{c_T(L)}{f(T)}-g(L).
$$

The source prints the following alternatives:

| Criterion | $f(T)$ | $g(L)$ |
|---|---|---|
| BIC1 | $\ln T$ | $(P-L)(Q-L)$ |
| BIC2 | $\log T$ | $(P-L)(Q-L)$ |
| BIC3 | $\ln T$ | $(P-L)(Q+1)$ |
| AIC | 1 | $2(P-L)(Q-L)$ |

BIC1 and BIC2 differ only by the notation $\ln$ versus $\log$. Their sharply different numerical results imply that the authors intend different log bases; interpreting $\log$ as base 10 is consistent with BIC2’s weaker penalty and greater propensity to retain factors. The printed paper does not explicitly state that base. Code must not use natural logarithms for both and then claim to replicate the distinct reported criteria.

For BIC1, multiplying by $\ln T$ yields the equivalent criterion $c_T-d_L\ln T$. Since the total fit improves with additional factor directions but the number of overidentifying restrictions falls, the negative restriction term favors a smaller adequate model. Underfitted models incur an order-$T$ discrepancy that dominates the logarithmic penalty; an adequately specified lower count is favored over redundant higher counts whose fit differences are only order one under the needed regularity. AIC does not have the growing penalty required for count-selection consistency and is included only for comparison.

Unlike the sequential chi-squared test, model selection does not require the optimal covariance weight; a positive-definite convergent weight can suffice. This is useful when the estimated long-run covariance has many noisy entries. It does not permit singular weights, invalid instruments, or arbitrary changes in normalization across candidate counts.

For each count search, retain at least one dependent equation and one overidentifying direction, so use $L\le\min(P,Q)-1$. The appendix’s bound $Q-1$ implicitly needs a compatible $P\ge Q$ split. The authors repeat the exercise over 100 random partitions and call the modal estimated count the highest-frequency, or HF, estimate. Ties, random ordering, and odd-$N$ splits need explicit implementation choices. The complete partition frequency distribution is valuable diagnostic output, not a posterior probability distribution over true factor counts.

## Local factors: a rank qualification needed by the extension

The main text’s Assumption D* sets $L_* =\min\{\operatorname{rank}(B_g),\operatorname{rank}(B_z)\}$. Appendix A then treats this as equivalent to $\operatorname{rank}(B_z\Omega_f B_g')=L_*$. It is not equivalent generally. The observable cross-block rank is at most the smaller loading rank, and can be strictly smaller.

A concrete counterexample has two independent factors with $\Omega_f=I_2$. Let every variable in group $g$ load only on the first factor and every variable in group $z$ only on the second. Both loading blocks have rank one, the full panel has rank two, and the groups can contain arbitrarily many variables. Nevertheless,

$$
B_g=\begin{pmatrix}1&0\\1&0\\1&0\end{pmatrix},
\quad B_z=\begin{pmatrix}0&1\\0&1\\0&1\end{pmatrix},
\quad B_z\Omega_f B_g'=0.
$$

All zero-factor cross-block moments already vanish. The estimator for this partition cannot recover the main text’s proposed $L_*=1$. This does not contradict the full-rank exact-factor theorem, because the strong subset assumption is violated.

Even when the cross-block rank is correctly defined as $r$, the selected $x$ columns must span its column space to make the normalized coefficient representation unique at $L=r$. An arbitrary choice of $r$ regressors need not do so. The appendix’s normalized-null-space argument implicitly needs this column-selection condition. Its discussion of lower derivative rank and generalized inverses cannot by itself justify simultaneous claims of unique coefficient identification under deficient rank.

The reliable interpretation is therefore to count factor directions visible across each partition, check instrument relevance and the rank of the chosen regressor block, and inspect sensitivity across partitions. Random repartitioning can place both local groups on both sides and recover more directions in some datasets, but modal recovery is not guaranteed from the weakened assumption as printed. Weak factors with nonzero but small loadings create a finite-sample power problem even when population rank is technically full.

## Approximate factors, transposition, and candidate factors

The source offers two routes beyond exact cross-sectional errors. First, suppose assets can be allocated to a fixed number of groups, each containing an increasing number of assets, and cross-sectional error covariances are sufficiently weak in aggregate. Equal-weighted group-average idiosyncratic components then vanish in covariance as group sizes grow. Group-specific local factors may remain, but if they are uncorrelated across groups they enter group-specific errors. The portfolio-level model can consequently have an approximately exact cross-group structure for the global factors.

This is an asymptotic diversification argument, not a guarantee that arbitrary finite portfolios remove residual dependence. Group factors correlated across portfolios invalidate the intended exclusion. Nor does averaging preserve every factor: loading cancellation can remove a direction. The source requires rank conditions on the resulting portfolio loadings in addition to weak idiosyncratic dependence.

Second, with large $N$ and fixed small $T$, rewrite the panel asset by asset as

$$
r_{i\cdot}=\alpha_i\mathbf1_T+F\beta_i+\varepsilon_{i\cdot}.
$$

The factor realizations become fixed-dimensional coefficients and loadings play the role of cross-sectional random inputs. The necessary orthogonality is now absence of serial correlation in each asset’s idiosyncratic errors. Cross-sectional dependence can be allowed under a suitable ordering and mixing/CLT conditions. Factor/loadings rank and limiting second-moment assumptions are exchanged correspondingly. This method does not allow unrestricted serial and cross-sectional residual dependence simultaneously merely by transposing a matrix.

For an excess-return specification that removes intercepts through an equilibrium APT restriction, the transposed moments use $\operatorname{vec}\{z_i(y_i-Sx_i)'\}$ without added intercepts. For raw returns, the source proposes demeaning only the response group over its own selected dates, leaving the instrument group undemeaned. If $Q_P=I_P-P^{-1}\mathbf1_P\mathbf1_P'$, then

$$
Q_Pg_i=Q_PF_g\beta_i+Q_P\varepsilon_i^g.
$$

Using only the response-group mean preserves its error orthogonality to disjoint instrument-group dates. Demeaning over all dates would share instrument-group errors across the boundary. Preservation of the factor count additionally requires $\operatorname{rank}(Q_PF_g)=L_0$; absence of global collinearity does not automatically ensure that property for every date subset.

Demeaning also creates a deterministic linear dependence among the $P$ transformed responses. A robust implementation must use an independent contrast basis or otherwise account for redundant moments and their rank when forming covariance inverses and degrees of freedom. The source’s brief transposition recipe does not fully resolve this numerical issue. An alternative is to count the rank of the augmented factor matrix $[\mathbf1_T,F]$ and subtract one. This requires the constant direction to add exactly one rank and the augmented loadings to satisfy the corresponding identification assumptions; subtracting one mechanically is not valid in every degenerate model.

For observable candidate factors $h_t\in\mathbb R^K$, use all returns as the response group and $(1,h_t')'$ as instruments. If $E[\varepsilon_t h_t']=0$, the relevant rank is

$$
L_h=\operatorname{rank}\{\operatorname{Cov}(r_t,h_t)\}.
$$

This measures the dimension of latent-factor combinations associated with $h_t$, potentially smaller than $L_0$. Cross-sectional error covariance is permitted because other returns are no longer the instruments. The exclusion restriction against idiosyncratic returns remains necessary, as do relevant regressor-column rank conditions. A nonzero estimated rank does not measure a correlation magnitude, identify which original factor is involved under rotational indeterminacy, or show that the candidate is priced.

## Simulation design and what the tables show

The baseline simulation has three Gaussian factors and Gaussian loadings calibrated to the Fama–French market, SMB, and HML components of 25 size/book-to-market portfolios. At mean estimated loadings, the source reports common-component variances 21.66, 4.51, and 1.31. Idiosyncratic variances range from 1.21 to 3.79, averaging 2.016, producing stated signal-to-noise ratios about 10.74, 2.23, and 0.65. These are variance ratios, not explained-variance percentages. The printed variance magnitudes use the authors’ calibration units; they should not be interpreted as decimal-return annual variances without the original scaling details.

The first error design is cross-sectionally heteroskedastic and serially uncorrelated. The second uses $\varepsilon_{it}=0.5\varepsilon_{i,t-1}+v_{it}$, choosing innovation variance to preserve the same unconditional idiosyncratic variance. The estimated original residual autoregressions were all below 0.1; the authors deliberately use 0.5 to make a stronger stress. A one-factor design uses HML because it is the weakest baseline factor.

Each of 1,000 simulated datasets is evaluated with 100 random partitions, using approximately half the assets as instruments. Tables 1, 2, and 4 report the average of the resulting modal factor counts across datasets. An average near three does not by itself reveal the probability of selecting three; errors above and below can offset.

Representative results expose both successes and failures:

| Design, true count 3 | $(N,T)$ | SHT | BIC1 | BIC2 | BIC3 |
|---|---|---:|---:|---:|---:|
| Uncorrelated errors, Table 1 | (10,250) | 3.00 | 2.98 | 3.01 | 2.95 |
| Uncorrelated errors | (15,250) | 3.00 | 1.05 | 3.00 | 3.00 |
| Uncorrelated errors | (25,250) | 3.00 | 1.00 | 1.06 | 1.00 |
| Uncorrelated errors | (25,1000) | 3.01 | 3.00 | 3.00 | 3.00 |
| AR(1) errors, SHT bandwidth 3, Table 2 | (10,250) | 3.00 | 2.98 | 3.23 | 2.95 |
| AR(1) errors, SHT bandwidth 3 | (25,500) | 1.00 | 1.00 | 3.00 | 2.74 |
| AR(1) errors, SHT bandwidth 3 | (25,1000) | 3.00 | 3.00 | 3.00 | 3.00 |

For the last row, SHT with bandwidth zero instead averages 5.75, illustrating the cost of ignoring error dependence. At $(25,500)$ bandwidth zero averages 5.70, while bandwidth three averages 1.00; covariance estimation can fail in opposite directions. BIC criteria that do not need optimal weighting are often more stable, but the severe low-$T$ undercounts show that this is not uniform robustness.

The comparison with Bai–Ng criteria is specific to small panels and the calibrations used. In Table 1, several Bai–Ng criteria return eight factors when $N=10$ despite three true factors, whereas some improve markedly at $N=25$. The paper itself stresses that those competing procedures were designed for both dimensions being large. This does not establish a general dominance claim over their intended regime.

To study weak factors, the authors reduce SMB’s signal-to-noise ratio to 0.30 or 0.20 and increase the market component to keep aggregate explanatory power fixed. At $(N,T)=(12,500)$, Table 4’s BIC2 modal-count average falls from 3.00 at 0.30 to 2.75 at 0.20; BIC1 and BIC3 both fall to 2.01 at 0.20. At $(25,1000)$ and SNR 0.20, BIC2 averages 3.00 while the Bai–Ng IC1 entry is 2.05. Detection depends on sample size and criterion, not just a universal SNR boundary.

Table 3 describes partition frequencies within a single simulated dataset rather than averages across 1,000 datasets. Its printed $(12,250)$, SNR-0.20 row has 59% selecting two and 33% selecting three, whereas the prose says 56% and 43%. The table values are retained here. Also, the prose’s broad claim that the correct three-factor mode exceeds 60% at SNR 0.30 has an explicit exception: $(25,250)$ selects at most one factor in 86% of partitions and three in only 5%. These discrepancies rule out reading the suggested 60%/25% frequency thresholds as established decision rules.

In the approximate-factor experiment, 500 individual series receive locally correlated errors

$$
\varepsilon_{it}=v_{it}+\delta\sum_{\substack{h\ne i\\|h-i|\le J}}v_{ht},
\qquad \delta=0.10,\quad J=8,
$$

with the sum truncated at panel endpoints. They are randomly grouped into 10, 12, 15, or 25 portfolios, with $T=250,500,1000$. The source says results resemble Table 1 but does not report all entries. Its practical suggestion of roughly 34 assets per portfolio comes from this one 500-asset design, not a general theorem that 34 holdings eliminate residual covariance.

## International equity application

The empirical panel contains 420 weekly excess-return observations from January 2000 through January 2008 for 11 country indexes. The Americas comprise the US S&P 500, Mexico IPC, and Brazil Bovespa; Europe comprises UK FTSE, Germany DAX, and Switzerland SMI; Asia comprises Japan Nikkei 225, Hong Kong Hang Seng, and Korea Kospi; Africa–Middle East comprises Israel TASE 100 and South Africa Dow Jones Titans 30. Data are from Yahoo Finance except the South African series, obtained from Dow Jones. These are the historical inputs described by the source, not current index specifications.

The study uses White weighting and 100 partitions with BIC1 and BIC2. It does not report enough return-construction detail to reproduce the panel exactly: currency conversion, dividend treatment, the risk-free series used for each excess return, weekly endpoint alignment, holiday handling, and the exact retained observation dates are missing. Index composition and calculation methods also differ across countries, a limitation acknowledged by the authors.

For all countries, the full partition frequency distribution is:

| Selected count | BIC1 | BIC2 |
|---:|---:|---:|
| 0 | 6% | 0% |
| 1 | 92% | 6% |
| 2 | 2% | 36% |
| 3 | 0% | 49% |
| At least 4 | 0% | 9% |
| Mean count | 0.96 | 2.61 |

The large difference between penalties motivates the authors’ interpretation of one strong common factor plus two weaker directions. It is not a direct decomposition into measured factor variances. The three-factor count is the BIC2 mode, but it occurs in fewer than half of partitions.

Regional exclusions yield the following selected-count modes and frequencies:

| Panel | BIC1 mode | BIC2 mode or reported grouped maximum |
|---|---|---|
| Exclude US | 1, 81% | 3, 45% |
| Exclude Americas | 2, 68% | 2, 76% |
| Exclude Europe | 1, 83% | 2, 73% |
| Exclude Asia | 1, 91% | 2, 50% |
| Exclude Africa–Middle East | 1, 67% | At least 3, 73% |

The source associates the weaker directions with Europe and the Americas, because removing either reduces BIC2’s preferred count to two. That is a suggestive subset comparison. Changing the asset universe also changes loading relevance, partition dimensions, moment count, power, and penalty behavior, so it is not a uniquely identified geographic factor attribution. In particular, excluding the Americas increases BIC1’s mode from one to two, and excluding Europe leaves BIC1’s mode at one; the source’s narrative is clearest when read alongside both criteria rather than as a uniform result.

Using US market, SMB, and HML as external instruments produces one associated direction in 71% of BIC1 partitions and 74% of BIC2 partitions. With the US index removed from responses, these percentages become 92% and 56%, respectively; BIC2 selects two directions in the remaining 44%. The prose says both criteria select one factor more frequently after removing the US, but Table 5 contradicts that statement for BIC2. The table is the basis for these numbers.

The candidate-factor result establishes evidence for a low-dimensional association under instrument exogeneity. It does not estimate a numerical “high correlation,” prove that the three US factors span all global return risks, establish equal prices of risk across countries, or test an implementable international asset-pricing strategy. Those stronger interpretations require additional estimation and identification beyond factor counting.

## Reproduction limits and practical use

The note supplies a complete linear-system implementation of the core GMM moments, the proper degrees of freedom under full identification, both count-selection procedures, the random-partition aggregation, and the transposition restrictions. To match the source’s simulated and empirical tables exactly still requires the raw calibration sample, means/covariances of generated factors and loadings, their joint dependence structure, random seeds, initial GMM weight and updating convention, BIC2 log base, odd-panel partition and tie rules, rank tolerances, and the empirical return-construction inputs. Source references to downloadable Gauss code or additional author-provided results are not substitutes for those missing inputs in the supplied PDF.

For an applied risk-model exercise, report the full partition distribution, the selected criterion, weighting choice, admissible rank range, and matrix condition numbers. Separate exact-factor assumptions from assumptions justified only after portfolio averaging. Treat disagreement between BIC1 and BIC2 as evidence about specification sensitivity and weak identification, rather than converting 25% or 60% partition frequencies into calibrated confidence statements. The useful object is an estimate of the dimension supported by the covariance restrictions and the available sample; economic interpretation of each direction remains a separate task.
