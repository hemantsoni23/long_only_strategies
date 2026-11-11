# Determining the Number of Primitive Shocks in Factor Models

**Authors:** Jushan Bai and Serena Ng. **Source:** *Journal of Business & Economic Statistics* 25(1), January 2007, pp. 52–60. DOI: 10.1198/073500106000000413. **Original PDF:** [MacroLatentFactorModels_BaiNg_2007.pdf](../../Finance/MacroLatentFactorModels_BaiNg_2007.pdf).

## Contribution and the object being counted

The paper develops a consistent procedure for estimating how many independent common innovations drive a large panel of time series. This number is generally smaller than the number of contemporaneous principal components required to summarize the panel. The contribution is a bridge between these two dimensions: estimate the static factor space by principal components, fit a vector autoregression to those estimated factors, and estimate the rank of the resulting innovation covariance matrix. One thereby counts dynamic common shocks without estimating dynamic factors in the frequency domain.

This distinction matters economically. Several principal components can reflect different lags and propagation channels of the same primitive disturbance. Conversely, treating the first two principal components as a complete description of economic uncertainty can miss additional common disturbances that explain less variation but remain pervasive. A model with seven static factors need not contain seven independent innovations. The empirical illustration finds four dynamic shocks behind seven full-sample static factors in a panel of 132 US macroeconomic series.

The word “primitive” has a precise statistical meaning here. It refers to the minimum dimension of mutually uncorrelated innovations that span the innovations of the common factor process. It does not mean that the procedure identifies technology, monetary policy, fiscal policy, or any other economically labeled structural shock. Rotations of a shock basis remain possible. Counting independent disturbances and identifying their economic interpretation are separate tasks.

The main theoretical results are in Sections 2–4, the simulation design and estimates in Section 5 and Tables 1–2, and the macroeconomic application in Section 5.1 and Tables 3–4. The method replaces an informal explained-variance threshold with a shrinking threshold justified by the estimation rate of the relevant matrix. It is a consistency procedure, rather than a conventional fixed-size hypothesis test with a reported asymptotic significance level.

## Reduced-rank innovations in an observed VAR

Start with an observed, stationary, $r$-dimensional process $F_t$ satisfying a stable finite-order VAR:

$$
A(L)F_t=u_t,\qquad A(L)=I_r-A_1L-\cdots-A_pL^p.
$$

Stability requires the roots of the determinant of the autoregressive polynomial to lie outside the unit circle. The innovations are independent and identically distributed, with a finite moment of order $4+\delta$ for some positive $\delta$. Suppose the innovations admit the representation

$$
u_t=R\varepsilon_t,\qquad R\in\mathbb R^{r\times q},\qquad \operatorname{rank}(R)=q\le r,
$$

where the $q$ components of $\varepsilon_t$ are mutually uncorrelated and have a nonsingular diagonal covariance matrix $\Sigma_\varepsilon$. Then

$$
\Sigma_u=E[u_tu_t']=R\Sigma_\varepsilon R',\qquad \operatorname{rank}(\Sigma_u)=q.
$$

Thus the number of shocks is a rank, not the dimension of the observed VAR. A singular innovation covariance is entirely compatible with a well-defined dynamic system. The same lower-dimensional innovation can enter different equations and generate a higher-dimensional state through heterogeneous propagation.

Let $c_1\ge\cdots\ge c_r\ge0$ denote the eigenvalues of a positive semidefinite matrix $C$ whose rank is to be determined. The paper defines two normalized statistics:

$$
D_{1,k}=\left(\frac{c_{k+1}^2}{\sum_{j=1}^r c_j^2}\right)^{1/2},\qquad
D_{2,k}=\left(\frac{\sum_{j=k+1}^r c_j^2}{\sum_{j=1}^r c_j^2}\right)^{1/2}.
$$

For the nondegenerate case with at least one positive eigenvalue, both are zero for $k\ge q$. For $k<q$, both remain positive. The first measures the next omitted eigenvalue; the second measures the whole omitted tail. The denominator is the Frobenius norm of $C$, because its square equals the sum of squared eigenvalues. Consequently, $D_{2,k}$ measures the relative Frobenius distance between $C$ and its best rank-$k$ spectral approximation. These are not ordinary percentages of variance explained, which would use unsquared eigenvalues.

With genuinely observed factors, estimating the VAR and its innovation covariance introduces sampling errors of order $T^{-1/2}$. The article develops a shrinking-threshold rule robust to covariance estimation error, which is especially important once the factors themselves are estimated. Sampling error alone need not lift null eigenvalues in a correctly specified OLS VAR with genuinely observed factors, because its residual matrix preserves the innovation subspace. Proposition 1 chooses the smallest $k$ for which the estimated statistic falls below $mT^{-1/2+\delta}$, with fixed $m>0$ and $0<\delta<1/2$. This cutoff goes to zero more slowly than the sampling error. It eventually admits the true null eigenvalues while rejecting any fixed positive population eigenvalue.

## Why a dynamic factor model can have more static factors than shocks

The panel model is

$$
x_{it}=\lambda_{i0}'f_t+\lambda_{i1}'f_{t-1}+\cdots+\lambda_{is}'f_{t-s}+e_{it},
$$

where $f_t$ has dimension $q$, the distributed loading lag length $s$ is finite, and $e_{it}$ is idiosyncratic. Stack the current and lagged factors:

$$
F_t=(f_t',f_{t-1}',\ldots,f_{t-s}')',\qquad
\Lambda_i=(\lambda_{i0}',\lambda_{i1}',\ldots,\lambda_{is}')'.
$$

The observation equation becomes $x_{it}=\Lambda_i'F_t+e_{it}$. Its written static dimension is $r=q(s+1)$. Calling this representation static says only that the observation equation uses contemporaneous $F_t$. It does not say that $F_t$ has no dynamics.

If $f_t$ follows a stable VAR of order $h$, the stacked process has a finite VAR representation with order $p=\max(1,h-s)$. Its innovations contain the new $q$-vector $\varepsilon_t$ in the first block and zeros in the lag blocks. The old factor values move through the state deterministically once the past is known. Consequently, the innovation covariance of the larger state still has rank $q$.

The paper illustrates this with $h=3$ and $s=1$. Stacking $(f_t',f_{t-1}')'$ converts the original third-order factor dynamics into a second-order VAR for the stack. The transition matrices are constrained, and innovations enter only the current-factor block. This construction explains why estimating unrelated univariate autoregressions for extracted factors is not an acceptable substitute for a joint VAR: principal components identify a rotated factor space, and the rotation generally mixes dynamic relationships across components.

When $f_t$ is an invertible finite moving average, an infinite autoregressive representation exists and can be approximated by a finite VAR. The paper tests such a case in simulations. It explicitly limits Proposition 2 to fixed-order VARs, however. The extension allowing a lag order that increases with sample size is discussed but not established in the article. The favorable moving-average experiment therefore supplies finite-sample evidence beyond the theorem's exact scope, not a proof that all invertible dynamics are covered.

In spectral language,

$$
S_F(\omega)=A(e^{-i\omega})^{-1}R S_\varepsilon(\omega)R'[A(e^{-i\omega})^{-1}]^*,
$$

where the star denotes conjugate transpose. With full-rank shock spectrum and stable invertible filtering, this spectrum has rank $q$. This is the dynamic rank that the paper recovers indirectly in the time domain.

## Effective static rank and factor estimation

The written stack dimension $r$ need not equal the dimension actually supported by the data. Let $r^*$ denote the effective rank of the common static factor structure. The paper allows

$$
q\le r^*\le r.
$$

For example, suppose $F_t=\rho I_rF_{t-1}+R\varepsilon_t$. Because all coordinates share the same scalar autoregressive propagation, the stationary covariance is proportional to $R\Sigma_\varepsilon R'$ and has rank $q$. Writing down five coordinates does not create five independent contemporaneous common directions. Principal components can consistently recover only the effective space of dimension $r^*=q$.

With richer coordinate-specific dynamics, lagged shocks can span more directions, so $r^*$ can exceed $q$. This distinction is central to the simulation comparison between a common autoregressive coefficient and heterogeneous coefficients. It also prevents a common implementation error: interpreting a nominal parameter count in a state representation as an empirically identified factor count.

For a $T\times N$ data matrix $X$, take the eigenvectors of $X'X$ corresponding to its largest eigenvalues, scale them by $\sqrt N$, and collect them in $\widehat\Lambda$. Then set

$$
\widehat F=X\widehat\Lambda/N,\qquad
\widehat\Lambda'\widehat\Lambda/N=I_{r^*}.
$$

This is the paper's normalization. Under strong common factors, suitable moment assumptions, and weak time and cross-sectional dependence in idiosyncratic errors, there is a rotation $H^*$ under which the estimated factors approach $H^*F_t$. The average squared estimation error is of order $1/\min(N,T)$.

The number of static factors is selected with an information criterion of the form $\log\widehat\sigma_k^2+kC_{NT}$. Its penalty must satisfy $C_{NT}\to0$ and $\min(N,T)C_{NT}\to\infty$. Thus selecting the static dimension is an explicit first-stage estimation problem. The dynamic-rank procedure is not a method for bypassing an inadequate choice of the static space.

## The feasible shock-counting rule

Estimate a VAR in all selected principal components jointly. From the residuals, form

$$
\widehat\Sigma_u=T^{-1}\sum_t\widehat u_t\widehat u_t'.
$$

The normalization by $T$ is the paper's notation; a reproduction should also record precisely which observations remain after lagging. Factor estimation makes the covariance error depend on both panel dimensions:

$$
\left\|\widehat\Sigma_u-H^*\Sigma_uH^{*'}\right\|
=O_p\left(\frac{1}{\min(\sqrt N,\sqrt T)}\right).
$$

Rotation changes eigenvalue magnitudes but preserves the relevant innovation rank. Calculate $\widehat D_{1,k}$ and $\widehat D_{2,k}$ from the residual covariance eigenvalues and use

$$
a_{NT}=\frac{m}{\min(N^{1/2-\delta},T^{1/2-\delta})}.
$$

The estimators $\widehat q_3$ and $\widehat q_4$ are the smallest $k$ for which $\widehat D_{1,k}<a_{NT}$ and $\widehat D_{2,k}<a_{NT}$, respectively. The search includes the endpoint at the selected static rank, where the omitted eigenvalue tail is zero. Proposition 2 establishes consistency under the maintained model and regularity conditions.

The proof mechanism is separation. For $k<q$, an omitted population eigenvalue is strictly positive and eventually exceeds a vanishing threshold. For $k\ge q$, the statistics consist only of estimation error, which vanishes faster than the threshold. No full limiting distribution of the eigenvalues, no fourth-moment covariance matrix for all estimated covariance elements, and no numerical rank threshold tied to machine precision are required.

A residual correlation matrix can replace the covariance matrix. Rank is unchanged by nonsingular diagonal rescaling, but finite-sample eigenvalue magnitudes and suitable constants change. The authors recommend $m=1$ for both covariance statistics in their simulations. For correlation matrices, they use $m=1.25$ for the next-eigenvalue statistic and $m=2.25$ for the tail statistic. This is empirical calibration, not a universal optimality result. The tail statistic naturally tends to be larger because it aggregates several residual eigenvalues.

## Simulation design and what must be reproduced

Section 5 evaluates four data-generating processes. Each uses independent standard-normal loading coefficients, idiosyncratic errors, and primitive shocks, with the additional innovation construction described below for the last two designs. The cross-sectional sizes are $N=20,50,100$ and time dimensions are $T=100,200$. Each configuration uses 1,000 replications.

The first design has two dynamic factors following separate MA(1) processes with coefficients $0.2$ and $0.9$. The observation equation loads on the current factors and two lags, giving $q=2$, $s=2$, and nominal static dimension $r=6$. The second also has two dynamic factors, now AR(1) with coefficients $0.2$ and $0.9$, and observations load on the current factors and one lag. Thus its static dimension is four.

The third and fourth designs start with a five-dimensional static factor state driven by three primitive innovations. To create the rank-three innovations, draw three nonzero diagonal elements of a matrix $S$ from a uniform distribution on $[0.8,1.2]$, set its remaining diagonal elements to zero, and generate a random orthonormal matrix $\Gamma$. With $v_t$ an independent five-dimensional standard-normal vector, take $u_t=\Gamma S\Gamma'v_t$. The matrices remain fixed across observations within the generated dataset. The paper describes the orthonormal construction through MATLAB's `orth(rand(r,r))`.

In design 3, $A_1=0.5I_5$, so the effective static rank is three despite the written five-dimensional state. In design 4, $A_1$ is diagonal with entries $0.2,0.375,0.55,0.725,0.9$. The heterogeneous dynamics can produce effective static rank five in sufficiently informative samples while preserving innovation rank three.

For every replication, estimate static factors using principal components and minimize

$$
IC(k)=\log\widehat\sigma_k^2+
 k\frac{\log\min(N,T)}{NT/(N+T)},\qquad k=0,\ldots,2r.
$$

Next fit a VAR(2) to the chosen factor estimates, obtain residual covariance and correlation matrices, and apply both rank rules. The authors report that higher lag orders give similar results. They fix $\delta=0.1$, so the threshold denominator is $\min(N^{0.4},T^{0.4})$. Tables 1 and 2 report average selected counts, rather than selection probabilities or distributions.

Exact bitwise replication needs additional choices that the article does not fully document: random seeds, initialization and burn-in for autoregressive factors, and the detailed treatment of observations lost to lags. These should be recorded in a new implementation rather than silently claimed to reproduce the original random experiment exactly.

## Simulation evidence and finite-sample limits

The strongest result is that the dynamic count can be accurate even when the first-stage static dimension is overestimated. In design 1 at $N=20,T=100$, the mean static count is 10.332 against a nominal true value of six. Nevertheless, the covariance rules with $m=1$ average 1.975 and 2.090 against a true shock count of two. At $N=50,T=100$, both dynamic counts equal 2.000 on average while the mean static count is 6.078.

This robustness has limits. In that small design-1 panel, raising $m$ to two reduces the dynamic averages to 1.137 and 1.307. Reducing it to $0.5$ raises them to 2.355 and 3.925. The threshold constant therefore has a substantial finite-sample economic effect: an aggressive cutoff can erase a real disturbance, and a permissive one can count estimation noise as extra shocks.

Design 2 gives similar evidence. At $N=20,T=100$, the static count averages 6.820 rather than four, while the covariance rules with $m=1$ give 1.995 and 2.223 rather than two. At $N=100,T=100$, both dynamic averages are 2.000. In design 3, where the effective static rank is three, the covariance estimators with $m=1$ average 2.693 and 2.787 at $N=20,T=100$, rising to 2.999 and 2.999 at $N=50,T=100$.

Design 4 highlights a different issue. At $N=100,T=100$, the selected static count averages only 3.001, although rich dynamics yield a five-dimensional static space asymptotically. Both dynamic counts still average 3.000. Recovering the shock dimension can therefore be easier than detecting every contemporaneous state direction. This does not mean the missing static directions are irrelevant for forecasting particular observables.

The correlation versions require their separate constants. For design 2 with $N=50,T=200$, the recommended correlation choices produce averages 2.828 and 2.131, versus 2.000 and 2.026 for the covariance rules with $m=1$. Thus “scale invariant” does not automatically mean more accurate in these designs. The article generally finds the next-eigenvalue rule more attractive than the tail rule when sample dimensions are small.

## Rank geometry and threshold diagnostics

The sample-size scaling can be translated into an operational diagnostic. With the simulation choice $\delta=0.1$ and $m=1$, the covariance threshold is about 0.302 when $\min(N,T)=20$, 0.209 when the smaller dimension is 50, and 0.158 when it is 100. These values are calculated from the stated rule, not additional experimental results. They explain why increasing the time dimension from 100 to 200 cannot by itself tighten the cutoff in an experiment with only 20 series. The weaker panel dimension controls the bound because estimating the factors requires both sufficient cross-sectional information and sufficient time observations.

These thresholds apply to normalized spectral magnitudes. A next-eigenvalue statistic of 0.20 is not a claim that the candidate shock explains 20% of total variance. It says that the next eigenvalue equals 20% of the Euclidean norm of the complete eigenvalue vector. Squaring, summing, and normalizing are integral to the procedure. Replacing the statistic with an ordinary cumulative variance ratio would change both the criterion and its finite-sample calibration.

Another useful diagnostic follows directly from the definitions. For the same matrix and candidate rank, the tail statistic is at least as large as the next-eigenvalue statistic. If both use the same threshold, the tail rule cannot select a smaller dimension. This ordering is visible in the covariance simulations. It need not hold when different constants are used, as in the recommended correlation version. A discrepancy between the two selected counts can therefore reflect a distributed tail of small eigenvalues, not a contradiction between two estimates of the largest omitted eigenvalue.

The distinction between static covariance rank and innovation rank can also be expressed through the stationary covariance of a stable first-order state model. Iterating the state equation gives

$$
\Sigma_F=\sum_{j=0}^{\infty}A^jR\Sigma_\varepsilon R'(A')^j.
$$

Every individual summand has rank at most $q$, but their ranges need not coincide. Their sum can have a larger rank if the dynamics move past shocks into different state directions. When $A=\rho I$, the ranges coincide and static rank collapses to the innovation rank. With heterogeneous dynamics, the span of the columns of $R,AR,A^2R,\ldots$ can be larger. This derivation makes explicit the mechanism behind designs 3 and 4; it is explanatory algebra from their stated model, not an extra empirical claim.

The same logic clarifies what a researcher can learn from overestimating the static dimension. Extra estimated principal components can be dominated by idiosyncratic sampling variation, so their VAR residuals need not add large eigenvalues relative to the genuine common innovation directions. The second stage may discard them. But this observed robustness does not remove the first-stage consistency assumption from the theorem, and it does not imply comparable robustness to omitting an economically important common direction. A shock excluded from the estimated factor space cannot reliably be recovered by examining only that space's residuals.

Finally, covariance and correlation rank agree only under the intended nonzero-variance normalization. If a factor residual has numerically zero variance, dividing by its sample standard deviation to create a correlation matrix is undefined or unstable. In a reproduction, inspect such cases before diagonal rescaling and distinguish an exactly redundant coordinate from a small positive innovation variance. The paper's theoretical rank argument assumes a well-defined representation of the retained space; it does not prescribe an arbitrary numerical tolerance for pathological sample coordinates.

## Macroeconomic application

The empirical panel contains 132 monthly US macroeconomic series from January 1960 through December 2003, totaling 528 observations. It is the Stock–Watson dataset cited in the paper. Series are transformed by logarithms and first or second differences following that dataset's conventions. A faithful reproduction requires the historical dataset and its transformation codes, not a modern substitute assembled from revised series without documentation.

The empirical analysis uses the correlation-based statistics. First, the authors impose different static dimensions. In the full sample, two or three static factors correspond to two or three shocks. With four, five, or six static factors, the selected shock count is three; with seven or eight static factors, it is four. This shows directly that the estimated number of shocks depends on which common static space one asks the procedure to explain.

They then repeat the analysis over expanding samples, reporting 396 estimates with endpoints from December 1970 through December 2003. The article's indexing descriptions differ slightly between the prose and a table note concerning the initial observation count. A reproduction should align actual calendar endpoints and transformations explicitly rather than copy both inconsistent index statements.

Two ways of selecting static factors are considered: an information criterion and explained-variance thresholds of 30%, 40%, 50%, and 60%. Under the information criterion, the mean static count over expanding samples is 5.763, and the mean dynamic counts are 3.864 and 3.119 for the two rules. The full-sample result emphasized in the conclusion is seven static factors and four dynamic factors. The mean variance share explained by selected static factors over expanding samples is 0.430; the full-sample share is 0.460.

For a 60% variance target, the mean selected static count rises to 13.811, with mean dynamic counts of 8.523 and 7.773. These numbers make an important point: there is no single shock count independent of the model-selection objective. A fixed high variance target can retain more directions than the statistical criterion, especially when it tries to explain a substantial fraction of panel-wide variation.

## Panel composition, interpretation, and practical use

Table 4 compares average explanatory power across the entire panel with explanatory power for selected aggregates. Two static factors explain 24.2% of panel variation but 72.3% of industrial-production variation. Four factors explain 35.0% across the panel and 70.6% for CPI in its specified transformed form. Seven explain 46.0% across the panel and 87.5% for industrial production. Retail trade and consumption remain much less well explained: with seven factors, their reported shares are 32.1% and 23.1%.

Thus finding that a few factors explain familiar headline aggregates is not evidence that the same few shocks adequately span a broad macroeconomic panel. Selection of target variables changes the apparent economic dimension. The paper's challenge to earlier two-shock conclusions is specifically about this distinction, rather than a universal claim that every useful business-cycle model must contain exactly four structural disturbances.

For implementation, preserve the full chain from panel transformations to static dimension, VAR specification, residual matrix, threshold constants, and selected dynamic rank. Report both rank rules and sensitivity to plausible constants and lag orders. Check residual serial dependence: a VAR that leaves predictable factor dynamics in its residuals is not measuring the innovation rank assumed by the method. Retain the eigenvalue profile itself so that an estimated count near a threshold is visible rather than buried in a single integer.

The method is useful for deciding how many independent shocks a statistical macro risk system requires, for assessing whether principal components are dynamically redundant, and for choosing a shock dimension before imposing structural identification restrictions. It does not produce expected-return forecasts, portfolio weights, a trading strategy, or economic labels for the innovations. Weak factors, nonstationarity, structural changes, strong idiosyncratic dependence, and an inadequate static representation can all undermine its maintained assumptions. The expanding-sample evidence is informative about instability but is not a formal model of time-varying dimension.

A further interpretive boundary concerns independence. The rank construction uses mutually uncorrelated primitive innovations and second-moment information. It does not establish statistical independence of non-Gaussian economic disturbances, nor rule out nonlinear dependence among them. Calling the resulting dimensions independent risk sources should therefore mean linearly distinct covariance directions unless additional distributional assumptions are supplied. This matters when transferring the procedure from Gaussian simulations to macroeconomic shocks with asymmetric or heavy-tailed joint behavior.

The enduring result is a computationally simple way to separate state dimension from innovation dimension while accounting for the fact that the states themselves are estimated. Its empirical integer should be treated as conditional on the panel, transformations, period, first-stage selection and threshold calibration; the static-to-dynamic distinction is the broader methodological contribution.
