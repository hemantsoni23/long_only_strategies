# How common are common return factors across the NYSE and Nasdaq?

**Amit Goyal, Christophe Pérignon, and Christophe Villa.** *Journal of Financial Economics* 90 (2008), 252–271. DOI: 10.1016/j.jfineco.2008.01.004. Source: [PervasiveFactors_GoyalPerignonVilla_2008.pdf](../../Finance/PervasiveFactors_GoyalPerignonVilla_2008.pdf). References below use printed article pages; the local PDF has 20 pages. The source and its two appendices were inspected, including the rendered factor-comparison tables.

## Why this matters

A factor can be pervasive within one market without being pervasive in every market. Pooling returns and retaining the largest principal components answers which directions explain the most pooled variance. It need not identify the intersection of the factor spaces that drive each market separately. If one group is larger, more volatile, or more heavily exposed to its own factor, pooled principal components can devote a leading direction to that group's specific risk. Labeling this direction an economy-wide factor then confuses a union of risks with their intersection.

The paper develops multiple-group factor analysis, MGFA, to estimate common pervasive directions while respecting a known partition of assets. It first estimates each group's factor space, converts that space into an orthogonal projection, and combines the projections with equal group weight. Directions present in all groups receive the largest eigenvalues. The application treats NYSE/Amex and Nasdaq as two groups. Its main empirical conclusion is that three-factor descriptions of the individual exchanges do not represent the same three-dimensional space, while a lower-dimensional common component can be constructed that fits both groups more evenly than pooled factors.

This is a statistical identification contribution, not a demonstration that the recovered factors are independently priced or a trading strategy. The distinction matters when building a risk model: a global block and group-specific blocks should span the risks present, whereas a universal pricing model requires additional restrictions on expected returns. The paper's pricing simulation illustrates the consequences of misclassifying factors, but its empirical application does not estimate an investable alpha after costs.

## Model: intersection rather than pooled variance

Let group $g=1,\ldots,G$ have $N_g$ assets observed over $T$ dates. Use $R_g$ for its $N_g\times T$ excess-return matrix. A convenient transposed version of the paper's factor model is

$$
R_g'=F_g B_g'+E_g',
$$

where $F_g$ is $T\times K_g$, $B_g$ is $N_g\times K_g$, and $K_g$ remains small while the cross-section grows. Individual factors are not identified independently of a nonsingular rotation. The object of interest is the column space $\mathcal S_g=\operatorname{col}(F_g)$.

A pervasive factor has exposures sufficiently widespread that the associated eigenvalue of the common return covariance diverges with group size. Idiosyncratic covariance has bounded largest eigenvalue under the approximate-factor assumptions. Weak residual cross-correlation is allowed; an additional omitted factor whose influence grows throughout a fixed fraction of the cross-section is not automatically an admissible bounded-eigenvalue disturbance.

Define the union and intersection dimensions as

$$
K=\dim(\mathcal S_1+\cdots+\mathcal S_G),\qquad
K_C=\dim(\mathcal S_1\cap\cdots\cap\mathcal S_G).
$$

A common pervasive factor lies in every group space. A group-specific factor may affect one group, or a subset of groups, without lying in the full intersection. Thus $K$ is not generally $K_C+\sum_g(K_g-K_C)$: some directions can be shared by only two of three groups, producing overlap outside the full intersection. This possibility is explicitly explored in the simulations.

The asymptotic construction treats the number of groups as fixed, with their cross-sectional sizes increasing. The paper's baseline asymptotic sequence keeps group sizes close to $N/G$ plus fixed offsets. Its unequal-size numerical experiments also examine a much less balanced finite sample. Those experiments are useful evidence about finite-sample behavior, but should not be substituted for the exact asymptotic assumptions.

## MGFA algorithm and its geometry

For each group, asymptotic principal components analysis, APCA, begins with

$$
\Omega_g=\frac{1}{N_g}R_g'R_g.
$$

Let $J_g$ contain the $K_g$ leading orthonormal eigenvectors of $\Omega_g$. Their $T$-dimensional span estimates the group factor space. Construct

$$
P_g=J_gJ_g',\qquad P=\sum_{g=1}^G P_g.
$$

Unlike a sum of raw return covariance matrices, $P$ gives each group the same total weight per retained direction. Multiplying all returns in a group by a scalar changes its eigenvalues but does not change $P_g$. An orthogonal rotation of $J_g$ also leaves $P_g$ unchanged. Different group sizes or loading magnitudes therefore do not mechanically dominate the second-stage comparison.

The estimated common factor space consists of the eigenvectors of $P$ corresponding to its $K_C$ largest eigenvalues. Factor scales can subsequently be fixed by multiplying these unit-length eigenvectors by $\sqrt T$. Asset loadings can then be estimated by regression on the resulting factors. The projection, rather than an arbitrary sign or scale of an individual eigenvector, is the central estimator.

The population geometry explains why the construction works. For any unit vector $z$,

$$
z'Pz=\sum_g\|P_gz\|^2\leq G.
$$

Equality holds precisely when $z$ lies in every group space. Consequently an eigenvalue equal to $G$ identifies an intersection direction. A factor present in only two of three mutually orthogonal group structures receives eigenvalue two, not three. A factor unique to one group receives eigenvalue one. These exact statements concern the population projections; estimated sample eigenvalues usually fall short of these ideal values.

The leading $K_C$ eigenvectors also maximize the sum of squared projection lengths onto the group spaces. Equivalently, they minimize aggregate projection loss subject to orthonormality. This gives a consensus factor estimator when estimated group spaces do not have an exact intersection. It does not mean every estimated common vector is literally contained in each estimated group space.

For two groups, principal-angle geometry gives an additional implementation check. If $c_j$ is a canonical correlation between two orthonormal group bases, the nontrivial eigenvalues of their summed projections occur as $1+c_j$ and $1-c_j$. The common consensus direction bisects the corresponding group directions. Its squared correlation with either group is $(1+c_j)/2$. These are mathematical consequences of using the same pair of orthogonal projections, not extra empirical findings.

The group-specific population component is the part of $\mathcal S_g$ orthogonal to the common space. A practical implementation projects group factors through $I-J_CJ_C'$ and constructs an orthonormal basis for the intended residual dimension $K_g-K_C$. In finite samples the estimated consensus space need not be contained in $\mathcal S_g$, so simply counting all nonzero singular values of this residual matrix can overstate the residual dimension. A fixed-dimension SVD construction is a transparent implementation choice; the source does not fully specify numerical tolerances for this step.

Likewise, the rank of a noisy finite-sample sum $P$ is not a consistent automatic count of economically pervasive union factors. Generic estimation noise can give positive eigenvalues to every estimated group direction. Factor-number selection has to precede or accompany the geometric calculation.

The paper also uses Jones's heteroskedastic factor analysis, HFA, to estimate each group space before applying MGFA. This changes the first-stage estimator, not the second-stage projector logic. HFA is attractive when idiosyncratic variances differ considerably across stocks. However, the local source refers to the earlier HFA method rather than supplying a complete optimizer, initialization, convergence tolerance, and all regularization details. An exact HFA replication requires that methodological reference or the original code.

## Selecting dimensions and comparing spaces

Appendix A gives the Bai–Ng information criteria used to help choose factor counts. If $V(k)$ is mean squared reconstruction error using $k$ factors and $\hat\sigma^2$ estimates residual variance, their forms are

$$
PC_j(k)=V(k)+k\hat\sigma^2g_j(N,T),\qquad
IC_j(k)=\log V(k)+kg_j(N,T),
$$

with penalties

$$
g_1=\frac{N+T}{NT}\log\frac{NT}{N+T},\quad
g_2=\frac{N+T}{NT}\log\min(N,T),\quad
g_3=\frac{\log\min(N,T)}{\min(N,T)}.
$$

These are minimized. A statement about maximization in the appendix should not be implemented literally. The empirical comparisons search one through eight factors. Different criteria give different answers; the final choices of three group factors and two common factors incorporate economic judgment rather than being unanimous outputs of a single consistent selection rule.

Canonical correlation analysis compares spaces without requiring factors to have matching labels. Let the covariance matrices of two centered factor vectors be $\Sigma_{11}$, $\Sigma_{22}$, and $\Sigma_{12}$. The eigenvalues of

$$
\Sigma_{11}^{-1}\Sigma_{12}\Sigma_{22}^{-1}\Sigma_{21}
$$

are squared canonical correlations. Appendix B writes the statistic as $\rho^2$ and uses an approximate standard error $2\rho(1-\rho^2)/\sqrt T$. The displayed confidence intervals in the empirical tables agree with this squared-correlation convention. Thus the numerical entries below should be interpreted as squared canonical correlations, even though the tables repeatedly call them “canonical correlations.” Taking another square would misstate the degree of common variation.

For example, a reported value $0.924$ is already a squared relationship; its corresponding correlation is approximately $0.961$. The intervals rely on the distributional and regularity arguments behind the cited canonical-correlation analysis. They are not a generic block-bootstrap correction for dependent monthly returns, and ordinary interior asymptotic approximations need special care near zero or one and for coincident population roots.

An exact implementation also needs a decision about centering. The APCA formula is written as an uncentered return cross-product, whereas canonical correlation is described with covariance matrices. The tabulated eigenvalues of $P$ and canonical roots do not always satisfy the simple two-projection identity if treated as calculations from identical centered bases. For instance the first-window HFA second squared canonical root is $0.720$, while the second eigenvalue of $P$ is $1.824$, rather than $1+\sqrt{0.720}\approx1.849$. The source does not reconcile this discrepancy. It should be preserved as a replication issue rather than silently forcing the two sets of reported numbers to agree.

## Monte Carlo design and what it establishes

The baseline experiment has three groups, $T=60$ observations, $N_g=1{,}000$ assets per group, and 1,000 replications. Five orthogonal normally distributed factor series have mean zero and unit variance. Two factors are common to every group; the remaining three are specific to groups one, two, and three. Loadings are drawn from a normal distribution with mean one and variance one. The disturbance is $\sqrt3$ times an independent standard normal innovation.

The recovered factor span is evaluated by a trace-based explained-variation statistic. With true factor matrix $F$ in $T\times K$ orientation and estimated projection $P_{\hat F}$, write it as

$$
S=\frac{\operatorname{tr}(F'P_{\hat F}F)}{\operatorname{tr}(F'F)}.
$$

It is invariant to estimated factor rotations and avoids claiming that a PCA eigenvector has the same economic label as a simulated primitive factor. The source separately measures recovery of the common space and of all pervasive factors.

In Table 1, pooled APCA recovers the common component with mean $S=0.9510$ and simulation standard deviation $0.0330$. MGFA gives $0.9992$ with standard deviation $0.0001$. Both recover the full factor space at approximately $0.9987$. Thus pooled estimation can find almost all relevant return variation while still selecting the wrong common subspace.

Several changes isolate the mechanism. Increasing the mean common loading to two improves APCA common recovery to $0.9801$, against MGFA's $0.9994$. Increasing the group-specific loading mean instead drives pooled APCA recovery down to $0.3447$, while MGFA remains at $0.9991$. Making group sizes $2{,}000$, $1{,}000$, and $500$ gives common-space recovery $0.9180$ versus $0.9991$. When a factor is shared by a subset of groups, pooled APCA gives $0.6881$ and MGFA $0.9992$. The latter case tests the distinction between the full intersection and partial sharing.

In the baseline the leading eigenvalues of the projection sum are approximately $2.997$, $2.994$, $1.014$, $1.000$, and $0.986$, close to the ideal pattern $3,3,1,1,1$. These are a direct diagnostic for the construction. Where there are no common factors, an entry indicating successful classification is not the same as an explained-variation ratio for a nonempty common factor matrix.

Table 2 introduces extra within-industry cross-correlation by partitioning each group into subgroups and adding subgroup shocks with random loadings. With ten subgroups, baseline common-space recovery falls to about $0.9401$ for pooled APCA and $0.9916$ for MGFA. Under stronger correlation and unequal group sizes, full-space recovery can fall to $0.7804$ for APCA versus $0.9849$ for MGFA. These are finite-sample robustness results. A shock loading on a fixed fraction of an ever-growing group can itself create a diverging covariance eigenvalue, so the simulation's “nonpervasive” nuisance terminology should not be treated as proof that every such sequence satisfies bounded idiosyncratic eigenvalues.

Table 3 introduces missing observations by selecting half the firms and deleting 15 of their 60 observations, replacing missing excess returns with zeros. This is 25% missing for affected firms and 12.5% across the entire balanced panel, not 25% of all cells. Baseline common recovery remains approximately $0.9510$ for APCA and $0.9988$ for MGFA. Random missingness in this experiment is much less adverse than delisting or IPO-related missingness that depends on returns and firm characteristics.

## Pricing simulation: classification matters, but rotations still matter

The two-group pricing exercise uses a factor common to both groups and a second factor specific to the first. It has $T=60$, normally distributed loadings with mean one and variance one, and unit-variance normal residuals. Expected returns satisfy

$$
E[r_i]=\lambda_0+\beta_{i1}\lambda_1+\beta_{i2}\lambda_2,
$$

where the true intercept is $0.05$, common premium $0.20$, and group-specific premium $0.10$. The second group's exposure to the group-specific factor is zero. The exercise considers equal group sizes of 1,000 and an unbalanced case with 1,000 versus 100 assets.

After factor extraction, time-series regressions estimate exposures and cross-sectional regressions estimate premia. MGFA allows the extra direction where it belongs; pooled APCA uses two extracted directions, and the integration-style comparison uses the true common exposure alone while omitting the local priced factor. In the equal-size case MGFA estimates the common premium near $0.1933$ and $0.1935$ in the two groups and the specific premium near $0.0933$. The true-common-factor-only regression gives an intercept about $0.1528$ in group one against $0.0533$ in group two. The omitted specific premium is largely absorbed by the first group's intercept, producing an apparent difference in pricing that is actually a missing-factor problem.

The corresponding pooled APCA premium estimates differ more across groups: approximately $0.2147$ versus $0.1779$ for one direction, and $0.0148$ versus $0.0769$ for the other. These numbers require care because risk-premium coordinates rotate with estimated factors. A coordinate-by-coordinate comparison with primitive factor premia is meaningful only under the experiment's factor alignment and normalization; equality of expected-return predictions is a more rotation-invariant diagnostic. The paper's broad identification warning is stronger than any claim that an arbitrary pooled PCA coefficient has a unique economic price.

The unbalanced case gives MGFA common premium estimates near $0.1939$ and $0.1934$, while the pooled estimates are approximately $0.2075$ and $0.1447$. These remain simulation results. They do not establish empirically that Nasdaq has an exchange-specific priced factor with a given premium.

## Empirical universe and sampling

The application uses monthly CRSP returns from 1978 through 2002, divided into five nonoverlapping 60-month windows: 1978–1982, 1983–1987, 1988–1992, 1993–1997, and 1998–2002. Returns are measured in excess of the one-month Treasury bill rate. The first group combines NYSE and Amex; the second contains Nasdaq. The baseline retains ordinary common shares, CRSP share codes 10 and 11, with complete returns during the window and no exchange switching. Securities traded on other exchanges are excluded.

The complete-case NYSE/Amex counts are 1,690, 1,500, 1,547, 1,763, and 1,760. Nasdaq counts are 1,252, 1,568, 2,210, 2,165, and 2,263. The cross-section is therefore large relative to 60 observations, and its composition is reselected in each window. Complete-case selection can induce survivor bias; the robustness exercise with missing returns addresses this partially, not perfectly.

Average monthly volatility in the first and final windows is about 11.10% and 12.65% for NYSE/Amex and 13.19% and 20.82% for Nasdaq. This growing heteroskedasticity helps explain why plain pooled variance weighting is unattractive. The factor analysis is retrospective within each 60-month block, with no rolling out-of-sample portfolio test, turnover specification, trading-cost model, or hyperparameter selection based on subsequent performance.

## What the exchange comparisons actually show

Table 7 fixes three pervasive factors in each exchange group. Using HFA, the first squared canonical correlations between groups are $0.962$, $0.959$, $0.954$, $0.829$, and $0.879$. Their second roots are $0.720$, $0.689$, $0.369$, $0.451$, and $0.793$, and their third roots are $0.490$, $0.314$, $0.022$, $0.105$, and $0.240$. Thus a leading common direction is strong; the second is less stable; the third is often weak. APCA gives a broadly similar conclusion but differs substantially in some windows, particularly 1988–1992, where its second squared canonical root is $0.814$ against HFA's $0.369$.

The eigenvalue evidence does not mechanically say there are exactly two common factors in every window. The HFA third eigenvalue of $P$ exceeds 1.5 in the first two windows, whereas its second falls below 1.5 in 1993–1997. The authors explicitly adopt two common factors using economic judgment, despite statistical ambiguity. A replication should report sensitivity to $K_C=1,2,3$ rather than describe two as a uniquely estimated truth.

Table 8 compares the selected two-dimensional common space with the three-dimensional factor space of each group. MGFA's smallest nonzero squared canonical relationship with each group is $0.924$, $0.915$, $0.804$, approximately $0.836$, and $0.945$. The equality of the NYSE/Amex and Nasdaq entries reflects the symmetric consensus geometry of two group projections. It is not an independent validation on new returns.

Pooled APCA is much less balanced. Its corresponding NYSE/Amex entries are $0.965$, $0.935$, $0.642$, $0.844$, and $0.834$; Nasdaq entries are $0.831$, $0.815$, $0.883$, $0.649$, and $0.845$. In 1993–1997 the pooled common space fits NYSE/Amex considerably better than Nasdaq, while MGFA gives both approximately $0.836$. The paper also reports that the second common direction from pooled APCA and MGFA can differ sharply late in the sample. This is the empirical counterpart of the simulation's warning: a leading pooled direction need not represent an exchange-neutral common component.

## Robustness and observable factors

The authors randomly divide stocks within an exchange, estimate factor spaces on the halves, and repeat the experiment 1,000 times. If within-exchange factor estimates were intrinsically unstable, low cross-exchange overlap would not establish meaningful segmentation. The within-exchange comparisons are generally stronger than comparisons between exchange groups, but are not uniformly close to one: the Nasdaq third squared canonical root averages about $0.462$ in 1988–1992. This exception limits any blanket claim that all three group factors are precisely identified.

They also divide mixed-exchange samples into random halves. The lower agreement for weaker factors in these exercises reinforces the concern that a small pooled-factor specification does not adequately summarize heterogeneous group structures. It does not by itself identify a unique structural source of exchange differences.

Table 10 relates the two common factors to observable Fama–French and momentum factors. The market's individual squared canonical association falls from $0.913$ in 1978–1982 to $0.714$ in 1998–2002. The size and value factors contain additional information. The smallest squared canonical root between the common two-dimensional space and the three Fama–French factors is $0.991$, $0.987$, $0.981$, $0.955$, and $0.897$. Adding momentum raises these to $0.992$, $0.990$, $0.985$, $0.956$, and $0.936$. The last-window increment is 0.039, appreciably larger than earlier increments. These are contemporaneous spanning comparisons, not tests of incremental expected-return predictability or factor profitability.

The missing-data exercise includes more stocks and replaces missing excess returns with zero. It also removes the first observed return following a missing spell to avoid treating a compounded return over several periods as a single-period return. The resulting counts reach 2,789 NYSE/Amex and 6,163 Nasdaq stocks in the final window. HFA second squared canonical roots across groups become $0.652$, $0.701$, $0.522$, $0.292$, and $0.640$; third roots remain weak. The broad difference between exchange spaces survives, although precise magnitudes and support for a second common direction remain sample-dependent.

## Reimplementation boundaries and practical use

A faithful implementation should retain three distinct records: the transformed return panels, the estimated group projections, and the common projection. Validate idempotence and symmetry of each $P_g$, bound the eigenvalues of $P$ between zero and $G$, and compare projector distances rather than raw signed factors. Keep the within-group dimension rule separate from the common-dimension rule. These checks directly target the method's geometry and avoid confusing numerical rotations with economic changes.

The source provides dates, broad universe rules, factor-count comparisons, and extensive numerical experiments. It does not fully specify HFA numerical settings, all random seeds, a uniform finite-sample threshold for common eigenvalues, or a complete resolution of centered versus uncentered calculations. Its use of squared canonical roots under an unsquared label and the mismatch between some reported projection eigenvalues and canonical roots are material replication qualifications.

The practical takeaway is to distinguish risks shared by all groups from risks important only somewhere in the universe. MGFA gives a simple, interpretable equal-group construction for that purpose. The paper supports using a common block plus group-specific blocks and testing the stability of their dimensions. It does not justify discarding local factors, assuming exactly two structural global shocks, or treating a retrospective common-factor fit as an executable investment result.
