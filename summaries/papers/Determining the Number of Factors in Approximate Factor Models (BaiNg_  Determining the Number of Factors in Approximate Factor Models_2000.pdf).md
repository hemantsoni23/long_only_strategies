# Determining the Number of Factors in Approximate Factor Models

**Authors:** Jushan Bai and Serena Ng. **Version summarized:** January 31, 2000 working paper, Boston College, 28 PDF pages. **Source:** [BaiNg_  Determining the Number of Factors in Approximate Factor Models_2000.pdf](../../Finance/BaiNg_%20%20Determining%20the%20Number%20of%20Factors%20in%20Approximate%20Factor%20Models_2000.pdf).

This note describes the actual working draft in the library. Its criteria, tables, and qualifications should not be silently replaced with those of a later published version. Printed page numbers are one less than PDF page numbers after the title page.

## Contribution and statistical target

The paper supplies a consistent rule for choosing the number of pervasive static factors when both the number of observed series and the number of time observations are large. The central insight is that estimating the factors creates errors governed by both panel dimensions. A valid complexity penalty must therefore account for both $N$ and $T$, rather than importing an ordinary time-series AIC or BIC penalty unchanged.

The proposed procedure minimizes the residual variance of a principal-components factor model plus a penalty per included factor. The penalty must vanish so that a genuine common direction is not permanently excluded, but it must vanish more slowly than the spurious improvement obtained by fitting additional factors to idiosyncratic variation. The paper derives the relevant overfitting rate, $1/N+1/T$, and constructs panel versions of Mallows's $C_p$ criterion around it.

The theoretical contribution includes an average convergence result for estimated factors up to rotation. The proof does not require uniformly consistent factor estimates at every date, nor a fixed ratio between the growth rates of $N$ and $T$. This makes the selection theory applicable to panels where assets greatly outnumber dates and to panels where a long history contains comparatively fewer series, provided both dimensions ultimately increase and the maintained conditions hold.

The target is the number of factors spanning the common static variation of the panel. It is not the number of predictors that optimally forecast one particular target, the number of economically named risk premia, or the number of independent dynamic innovations. A factor can be pervasive in the panel but irrelevant for predicting a chosen series. Conversely, a useful target-specific forecasting variable need not be a pervasive common factor. This distinction motivates the paper's criticism of selecting the common-factor dimension only through a single forecasting equation.

## Model, dimensions, and pervasiveness

The data-generating model is

$$
X_{it}=\lambda_i^{0\prime}F_t^0+e_{it},\qquad i=1,\ldots,N,\quad t=1,\ldots,T,
$$

where $F_t^0$ is an $r$-vector, $\lambda_i^0$ is its loading for series $i$, and $e_{it}$ is the idiosyncratic component. In matrix form,

$$
X=F^0\Lambda^{0\prime}+e,
$$

with $X$ of dimension $T\times N$, $F^0$ of dimension $T\times r$, and $\Lambda^0$ of dimension $N\times r$. Neither factors nor loadings are observed, and $r$ is unknown but fixed in the asymptotic argument.

The factor second moment converges to a positive-definite matrix, and normalized loading strength satisfies

$$
T^{-1}F^{0\prime}F^0\to\Sigma_F>0,\qquad
N^{-1}\Lambda^{0\prime}\Lambda^0\to D>0.
$$

These conditions ensure that every retained common direction contributes nontrivially as the panel grows. A factor whose influence is confined to a fixed small subgroup, or whose loading strength disappears as $N$ increases, is not covered by the strong-factor argument. The positive-definiteness assumptions also prevent two nominal factors from being asymptotically redundant.

The individual loading vectors are bounded in the main formulation. The draft notes that random loadings can be accommodated with independence from factors and errors and suitable fourth moments. Its Gaussian-loading simulations use that random-loading interpretation. The distinction matters when reproducing the assumptions: Gaussian draws are not uniformly bounded deterministic loadings, but their moment properties fit the extension described by the authors.

The model is static in the observation equation: only $F_t^0$ appears contemporaneously. The factors and errors can nevertheless be serially dependent. “Static” therefore refers to the representation, not to independence across dates. The model can be useful for returns, macroeconomic panels, and demand systems, but those applications require different preprocessing and do not change what the selection criterion estimates.

## Error assumptions and what approximate means

Assumptions A–D are stated on printed pages 5–6. Factor fourth moments are finite. Idiosyncratic errors have mean zero and uniformly bounded eighth moments. Their serial and cross-sectional dependencies are restricted through bounds on aggregate absolute covariance sums, rather than by requiring every covariance to be zero.

For example, write $\tau_{ij,t}=E[e_{it}e_{jt}]$ and suppose it is bounded in absolute value by $|\tau_{ij}|$. One key requirement is

$$
N^{-1}\sum_{i=1}^N\sum_{j=1}^N|\tau_{ij}|\le M.
$$

This permits local or weak cross-sectional dependence whose aggregate contribution grows only linearly in panel width. It rules out putting an additional pervasive disturbance into the idiosyncratic errors while continuing to call the model an $r$-factor model. A similar average bound controls serial covariance of the cross-sectional error inner products. A joint time-and-cross-section covariance bound and a fourth-moment bound for centered error products support the proof's stochastic inequalities.

Heteroskedasticity across series and dates is allowed. There is no requirement that each date have the same idiosyncratic variance, an advantage over procedures that infer factor count through comparisons of residual variance across separate time periods. The conditions still require bounded moments and controlled dependence; arbitrary volatility explosions or persistent common variance components cannot be assumed harmless.

Factors and errors need not be independent. Assumption D instead bounds the average squared factor-error sample covariance at the appropriate rate:

$$
E\left[\frac1N\sum_i\left\|\frac1{\sqrt T}\sum_tF_t^0e_{it}\right\|^2\right]\le M.
$$

The draft gives an example in which an error is an independent disturbance multiplied by the norm of the factor vector. This creates conditional heteroskedastic dependence without necessarily violating the required bound. The statistical result is therefore more flexible than classical Gaussian factor analysis, but its flexibility is expressed in precise moment restrictions rather than in a claim of unrestricted robustness.

## Principal-components estimation for a candidate dimension

For each candidate $k$, solve the least-squares problem

$$
V(k)=\min_{F^k,\Lambda^k}\frac1{NT}\sum_{i,t}(X_{it}-\lambda_i^{k\prime}F_t^k)^2.
$$

A normalization is needed because loading and factor scales offset one another. Under $F^{k\prime}F^k/T=I_k$, the estimated factor matrix is $\sqrt T$ times the eigenvectors of $XX'$ corresponding to its largest $k$ eigenvalues. The loadings are $\widehat\Lambda^{k\prime}=\widehat F^{k\prime}X/T$. Alternatively, normalize $\Lambda^{k\prime}\Lambda^k/N=I_k$, use $\sqrt N$ times the leading eigenvectors of $X'X$ as loadings, and set $\widehat F^k=X\widehat\Lambda^k/N$.

Both routes yield the same fitted common component and residual objective. Choose the smaller covariance matrix computationally: the $T\times T$ route is attractive when there are many more series than dates; the $N\times N$ route is attractive in the reverse configuration. A singular-value decomposition of $X$ provides an equivalent implementation without separately forming either covariance matrix.

If $d_1\ge\cdots\ge d_{\min(N,T)}$ are the singular values of $X$, then

$$
V(k)=\frac{\|X\|_F^2-\sum_{j=1}^kd_j^2}{NT}.
$$

This expression is an implementation identity from the least-squares problem. It allows all candidate objectives to be computed from one decomposition and makes clear why fit alone always favors more factors. Each added component removes a nonnegative singular-value contribution, including contributions caused by idiosyncratic sampling variation.

The draft's factor convergence theorem uses a particular rescaled estimator, denoted $\widehat F^k$, that spans the same estimated column space as its other principal-components constructions. This detail matters when $k$ exceeds the true dimension: an arbitrary normalization that forces every extra factor to have unit variance should not be substituted into an assertion that extra rescaled directions converge toward a lower-dimensional true space. The factor-count criterion itself depends on fitted projections and is invariant to these invertible rescalings.

## Factor consistency and the smaller-dimension rate

Define $C_{NT}=\min(\sqrt N,\sqrt T)$. Theorem 1 establishes, for a suitable rotation or rectangular transformation $H^k$,

$$
C_{NT}^2\left[\frac1T\sum_t\|\widehat F_t^k-H^{k\prime}F_t^0\|^2\right]=O_p(1).
$$

The transformation has rank $\min(k,r)$. The economically meaningful object is the factor space and associated common component, not any unnormalized factor coordinate. The average squared error is therefore of order $1/\min(N,T)$ under the stated assumptions.

This result is deliberately weaker than a uniform bound over all dates and strong enough for factor-number selection. The loss function averages residual squared errors over the panel, so average convergence is the relevant control. Requiring the maximum factor estimation error over every time observation to vanish can impose stronger growth conditions that are unnecessary for this objective.

The Appendix decomposes estimation error into four terms: expected error covariance, fluctuations of error inner products around their expectations, and two factor-error cross terms. The expected serial covariance term contributes an order $1/T$ average bound; the remaining terms are controlled at order $1/N$ under the covariance and moment assumptions. This decomposition explains the appearance of both dimensions, rather than simply postulating an effective sample size.

The rate has a practical implication even before a formal selection criterion is introduced. Adding thousands of highly informative series does not replace a short time history in every estimation step, and extending the history cannot fully offset a cross section that fails to reveal a common direction. The theorem lets either dimension grow faster, but both must grow; it is not a guarantee of consistency with one dimension literally held fixed forever.

## The selection theorem and penalty formulas

For a fixed finite upper bound $k_{\max}>r$, consider

$$
IC(k)=V(k)+k\,g(N,T),\qquad
\widehat r=\arg\min_{0\le k\le k_{\max}}IC(k).
$$

Theorem 2 gives consistency if

$$
g(N,T)\to0,\qquad C_{NT}^2g(N,T)\to\infty.
$$

The first condition prevents persistent underfitting; the second prevents fitting vanishing idiosyncratic improvements as additional factors. The candidate upper bound is fixed in the theorem, and the true dimension must lie below it. A routine whose chosen rank hits the upper bound should not claim that it has established a fully adequate factor count.

Let $\widehat\sigma^2$ consistently estimate average idiosyncratic variance. The draft proposes three panel-$C_p$ criteria:

$$
PC_{p1}(k)=V(k)+k\widehat\sigma^2\frac{N+T}{NT}\log\left(\frac{NT}{N+T}\right),
$$

$$
PC_{p2}(k)=V(k)+k\widehat\sigma^2\frac{N+T}{NT}\log C_{NT}^2,
$$

$$
PC_{p3}(k)=V(k)+k\widehat\sigma^2\frac{\log C_{NT}^2}{C_{NT}^2}.
$$

The variance estimate provides scale consistency between the residual objective and its penalty. The suggested operational choice is $\widehat\sigma^2=V(k_{\max})$. The same variance estimate is used across candidate $k$, rather than allowing each candidate to redefine its own penalty scale.

All three penalties satisfy the asymptotic conditions. However, $1/N+1/T$ and $1/\min(N,T)$ differ in finite samples, by up to a factor of two. The logarithmic arguments also differ. The draft's simulations favor the first two criteria because these finite-sample differences provide a useful correction to the weakest-dimension asymptotic rate.

The criterion called $IC$ in this working draft is a generic residual-level criterion. The named recommended criteria are the displayed panel-$C_p$ forms. This version should not be summarized as if it had already presented every later logarithmic information-criterion variant associated with the authors.

## Why underfitting and overfitting require different arguments

For $k<r$, dropping a genuine strong common direction produces a positive limiting loss gap. The Appendix expresses it as a trace involving the omitted factor covariance and the positive-definite limiting loading second moment. Because both matrices contain nontrivial variation in the omitted direction, the gap cannot vanish. Estimated factors introduce smaller approximation errors, and a penalty that converges to zero cannot compensate indefinitely for this fixed loss.

For $k>r$, the fit improvement is only

$$
V(r)-V(k)=O_p\left(\frac1N+\frac1T\right).
$$

The model already contains the common space, so extra factors primarily fit errors. The penalty increment $(k-r)g(N,T)$ must dominate that stochastic improvement. This is the exact reason the second condition in Theorem 2 is needed. A penalty going to zero is necessary but not enough.

The comparison clarifies why the same penalty cannot be chosen by looking only at the total number $NT$ of entries. Those entries are linked through latent factors and estimated loadings; the effective error scale is not the independent-observation scale $1/(NT)$. A penalty proportional to that smaller quantity would generally be too permissive.

As a concrete calculation, if $N=T=M$, the second panel penalty per factor, divided by $\widehat\sigma^2$, is $2\log M/M$, whereas the third is $\log M/M$. They are asymptotically equivalent in the sense required for consistency but not equal in a finite panel. The third criterion therefore accepts some marginal components that the second rejects. The small-panel results in the tables exhibit precisely this overfitting pattern.

## Competing penalties and failure regimes

The draft compares the proposed criteria with three alternatives. Its first alternative replaces the logarithm with $\log(N+T)$ while retaining $(N+T)/(NT)$. This performs well in many practical configurations but can fail the vanishing-penalty condition under sufficiently extreme relative growth. For example, if $N$ grows exponentially in $T$, then $\log(N+T)/T$ need not go to zero. The point is theoretical generality, not a claim that ordinary return panels typically have this configuration.

The AIC-like alternative uses $2/T$. It goes to zero but does not satisfy the divergence condition after multiplication by $\min(N,T)$. Extra factors can continue to improve fit by an amount comparable to the penalty. The BIC-like alternative uses $\log T/T$. This can work when the time dimension is the smaller dimension, but it need not work when $N$ is much smaller and $N\log T/T$ fails to diverge.

These arguments concern applying the stated conventional-looking penalties to the paper's latent-factor selection problem. They are not a universal dismissal of AIC or BIC for every forecasting or regression problem. The comparison with observed regressors in Section 4 makes the distinction explicit: when the factors are observed, the cross-sectional factor-estimation error is absent and a different selection argument applies.

The source's qualitative conclusion is to use $PC_{p1}$ or $PC_{p2}$ rather than rely on a penalty whose justification depends on the relative shape of the panel. The empirical distinction is strongest when a moderate cross section is paired with a long time series, where time-only penalties become much smaller than the relevant latent-factor estimation scale.

## Monte Carlo design

The simulated observations are

$$
X_{it}=\sum_{j=1}^r\lambda_{ij}F_{tj}+\sqrt\theta\,e_{it}.
$$

Factors and loading entries are standard normal. Baseline errors are also standard normal, independently generated in the stated design. Unconditionally, the common component has variance $r$; setting $\theta=r$ gives equal common and idiosyncratic variance. Results are reported for true ranks $r=1,3,5$, with $k_{\max}=8$ in every experiment and 1,000 replications per configuration. Computations used MATLAB 5.3.

The 15 panel configurations are the five widths $N=100,200,500,1000,2000$ at each of $T=60$ and $T=100$, plus $N=60$ at $T=100,200,500,1000,2000$. The short panels are motivated by asset-pricing samples, while the narrower panels are plausible for countries, regions or sectors. The broad grid is designed to test whether a criterion depends on panel shape in the way predicted by the theory.

A heteroskedastic experiment uses $r=3$, $\theta=3$, and $e_{it}=e_{it}^{(1)}$ at odd dates but $e_{it}=e_{it}^{(1)}+e_{it}^{(2)}$ at even dates, with independent standard-normal components. Thus raw idiosyncratic variance alternates between one and two before multiplication by $\theta$. This is a specific time-heteroskedastic design, not a broad test of serially persistent stochastic volatility or correlated residuals.

Two additional experiments set $r=5$ and vary noise strength to $\theta=2r$ and $\theta=r/2$. They test the effect of lower and higher signal-to-noise ratios. Tables 1–6 report mean selected ranks. They do not provide complete selection-frequency distributions, standard errors across replications, or the joint frequency with which different criteria disagree.

To reproduce the experiment, retain the same candidate cap, variance scaling, panel sizes, and per-replication generation of loadings and factors. Record random seeds, whether columns are sample-demeaned, and any standardization. The draft does not fully document these implementation details; adding them is necessary for a transparent modern reproduction, but one should not claim exact agreement with the original random realizations.

## Numerical results and qualifications

At $r=1$, $N=100$, $T=60$, Table 1 reports mean selected rank 1.000 for both preferred criteria, 2.407 for $PC_{p3}$, and 8.000 for the AIC-like alternative. At $N=T=100$, the third criterion rises to 3.209, while the first two remain at 1.000. The same broad ordering appears for three factors: at $N=T=100$, the first two average 3.000, the third 4.217, and the AIC-like rule 8.000.

The long-history, narrow-panel cases illustrate the time-only BIC failure. With $N=60$, $T=2000$, and $r=3$, the first two proposed criteria average 3.000, while the AIC-like and BIC-like alternatives both select the cap of eight on average. Increasing the history without modifying the panel-aware penalty does not rescue the conventional-looking alternatives.

Time heteroskedasticity leaves the first two rules accurate in the reported experiment. At $N=T=100$, Table 4 gives 3.000 for both, 5.772 for $PC_{p3}$ and the BIC-like rule, and 8.000 for the AIC-like rule. The favorable evidence is about the specified alternating-variance experiment; the simulations do not exhaust the more general dependence permitted by the theorem.

The high-noise table is more nuanced than the source prose suggests. With five true factors, $\theta=10$, $N=100$, and $T=60$, Table 5 gives 4.781 for $PC_{p1}$ and 4.408 for $PC_{p2}$. At $N=60,T=100$, they give 4.749 and 4.394. These are clear average underselection, not exact recovery. Increasing information improves performance: at $N=200,T=100$, the corresponding means are 5.000 and 4.994. The weaker signal exposes finite-sample differences between otherwise consistent penalties.

With lower noise, Table 6 gives exact-looking means of 5.000 for the first two criteria throughout the reported grid. Yet a rounded mean equal to the true rank does not logically establish that every replication selected that rank: over- and underselection could offset, and rounding could hide rare errors. The draft explicitly makes the stronger inference in its discussion, but the table alone does not support it. The safest description is the reported mean, with the absence of full selection frequencies acknowledged.

## Scale, marginal components, and implementation checks

The residual-level criteria are invariant to a common change in measurement scale when the noise estimator is scaled consistently. Multiplying the whole panel by a scalar multiplies both $V(k)$ and $\widehat\sigma^2$ by its square, leaving the minimizing rank unchanged. This property does not extend to multiplying different columns by different scalars. Column standardization changes the least-squares weighting of the panel and can change the selected dimension. In a returns application, covariance-based extraction emphasizes high-volatility securities more heavily than extraction from standardized returns. Either can be a deliberate modeling choice, but they answer different weighted approximation problems.

The singular-value representation yields a useful marginal interpretation. For a fixed penalty scale, moving from $k$ to $k+1$ reduces the fit term by $d_{k+1}^2/(NT)$ and raises the complexity term by $\widehat\sigma^2p_{NT}$, where $p_{NT}$ is the selected penalty formula without the variance multiplier. Thus a component is worthwhile only if its normalized squared singular value exceeds that threshold. This is a derived interpretation of the criterion, not an alternative rule with a different normalization. It makes possible a direct numerical check of a software implementation against the full residual calculation.

For example, at $N=T=100$, the second penalty scale is approximately $0.0921$ and the third is $0.0461$, before multiplication by the noise estimate. These calculated values follow from $2\log(100)/100$ and $\log(100)/100$. A marginal sample component can therefore be included under the third criterion but excluded under the second over a substantial interval. The difference is large enough to matter in the finite panels used in the Monte Carlo, despite both rules satisfying the same limiting theorem.

The choice $V(k_{\max})$ for noise scale also deserves an explicit check. If the cap is too low to include the common space, the residual scale contains omitted common variation and can increase the penalty, reinforcing underselection. If the cap is very large in a small sample, residual noise can be fitted away, lowering the scale and making extra factors cheaper. The theorem uses a bounded cap above the truth; it does not justify moving the cap arbitrarily close to the sample rank. Reporting the noise estimate alongside the selected dimension reveals this channel and makes a later rerun interpretable when the candidate range changes.

## Model-use implications and limitations

The criterion is directly useful when a researcher needs a statistical dimension for a large static common component. In an equity risk model, it can help decide how many principal-component directions are supported by the return panel under the assumed residual structure. It does not decide whether those directions are economically interpretable, priced, stable through time, or useful after transaction costs. No portfolio backtest or factor-risk-premium estimation is included in this working draft.

In macroeconomic forecasting, a consistent panel factor count supplies one candidate summary of available information. The optimal forecasting subset can be smaller, and lagged factors can enter a target equation differently. Dimension selection for the common space should therefore be distinguished from target-specific forecast model selection, rather than assigning both jobs to a single integer.

For dynamic data, the source gives the example $X_{it}=af_t+bf_{t-1}+e_{it}$. A static representation may need two factor coordinates even though only one dynamic factor process appears. More general distributed responses can require still more static coordinates. The draft's selection theory therefore does not directly count primitive dynamic shocks. Using its output as an upper bound in a suitable dynamic representation is different from identifying the innovation dimension itself.

The zero-factor candidate is part of the stated minimization. Excluding it in software would impose common variation rather than let the criterion assess whether any retained direction clears the penalty. That implementation choice should be explicit even when the substantive application strongly expects common factors.

The supplied source is visibly unfinished in places and should be read as a working version. Its useful technical claims are the average factor-space convergence rate, the two penalty conditions, the explicit panel-$C_p$ formulas, and the associated simulation design. The limitations are equally specific: strong pervasive factors, bounded and weakly dependent idiosyncratic variation, fixed finite candidate dimension in the theorem, and no guarantee that finite-sample rank selection is exact in low-signal panels. A reproducible use of the method should report the full criterion curves and residual eigenvalue profile, the cap and noise estimate, and sensitivity to reasonable preprocessing choices, rather than presenting the selected rank without its supporting configuration.
