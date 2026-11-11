# The Generalized Dynamic-Factor Model: Identification and Estimation

**Authors:** Mario Forni, Marc Hallin, Marco Lippi and Lucrezia Reichlin. **Publication:** *The Review of Economics and Statistics* 82(4), November 2000, 540–554. **Source PDF:** [DynamicFactorModel_ForniHallinLippiReichlin_2000.pdf](../../Finance/DynamicFactorModel_ForniHallinLippiReichlin_2000.pdf). The local file includes the 15-page article and four later citation-list pages; the latter are not part of the paper's analysis.

## Contribution and distinction from static factor extraction

The paper introduces a generalized dynamic factor model combining unrestricted square-summable dynamic responses to common shocks with weakly cross-correlated idiosyncratic components. Its main achievement is to identify and consistently estimate the common component of each observed series as the cross section grows, without requiring residuals to be mutually independent and without restricting common responses to a short finite distributed lag.

The identification device is a separation of dynamic eigenvalues. At almost every frequency, the leading $q$ eigenvalues of the common spectrum diverge with the number of series, whereas the largest idiosyncratic spectral eigenvalue remains bounded. The observed spectrum inherits this separation. Its leading frequency-specific eigenspace then reveals the common dynamic space. Projecting each observed series onto that space across all leads and lags yields its common component asymptotically.

This unifies two useful but previously separate ideas: large approximate factor models that tolerate residual correlation, and dynamic index models that allow series to respond with different timing. The method is especially relevant when a common disturbance produces different lag profiles across assets, countries, or indicators. A static principal component can confuse phase differences with additional contemporaneous dimensions; dynamic principal components allow the weighting to vary by frequency.

The identified objects are the common components, idiosyncratic components, and the minimal number of pervasive dynamic shocks under the assumptions. The paper explicitly does not identify economically labeled structural shocks or their unique impulse-response filters. The resulting estimator is two-sided and designed for historical component extraction. Its main consistency result concerns observations away from sample endpoints, so it is not by itself a ready-to-use real-time trading signal or endpoint nowcast.

## Model and assumptions

For series $i$ and date $t$, the model is

$$
x_{it}=\sum_{j=1}^q b_{ij}(L)u_{jt}+\xi_{it}=\chi_{it}+\xi_{it},
$$

where $L$ is the lag operator, $u_t$ is a $q$-dimensional orthonormal white noise, $\chi_{it}$ is the common component, and $\xi_{it}$ is idiosyncratic. The shock dimension $q$ is finite while the sequence of observed series is conceptually infinite. Each loading filter is one-sided and square summable:

$$
b_{ij}(L)=\sum_{k=0}^{\infty}b_{ij,k}L^k,\qquad
\sum_{k=0}^{\infty}b_{ij,k}^2<\infty.
$$

The setup includes stable autoregressive responses through infinite moving-average expansions. It does not require all series to share the same autoregressive coefficient or a finite common static state dimension. One shock can generate many linearly independent contemporaneous series through heterogeneous propagation filters.

The idiosyncratic vector is stationary for every finite cross section and orthogonal to every common shock at every lead and lag. Orthogonality between common and idiosyncratic components is therefore stronger than zero contemporaneous covariance alone. Residuals may still be correlated with one another across series and dates, subject to the spectral bound below.

Each observed series has a bounded spectral density, though the bound need not be uniform across all series. The model is formulated for zero-mean stationary variables. The authors propose applying it after deterministic detrending when appropriate or after differencing and demeaning difference-stationary data. They do not establish that arbitrary preprocessing preserves the desired economic meaning of a business-cycle component.

Let $S_n(\omega)$ denote the spectrum of the first $n$ observed series, and write $S_n=S_n^\chi+S_n^\xi$. The two decisive assumptions are

$$
\sup_{n,\omega}\lambda_1(S_n^\xi(\omega))<\infty,
$$

and, for $j=1,\ldots,q$,

$$
\lambda_j(S_n^\chi(\omega))\longrightarrow\infty
\quad\text{for almost every }\omega.
$$

The first controls the collective strength of idiosyncratic dependence; the second requires every common shock to be sufficiently pervasive. They distinguish a common component from a merely correlated residual cluster by its behavior as the cross section grows.

## Pervasiveness is stronger than nonzero correlation

The paper gives a useful counterexample. Suppose $x_{it}=b_i u_t+\xi_{it}$ with independent unit-variance white-noise residuals, but $\sum_i b_i^2<\infty$. Every pair can share a nonzero correlation through $u_t$. Nevertheless, the leading spectral eigenvalue remains bounded, because total squared loading strength is bounded. Under the model's asymptotic definition, the entire process can be treated as idiosyncratic and a zero-common-factor representation is admissible.

Thus detecting correlations does not prove the existence of a pervasive factor in this framework. A sector-specific or localized source of dependence can be economically important without belonging to the common component defined by diverging spectral eigenvalues. The classification depends on how the observed sequence expands, an issue relevant to panels formed by adding many similar assets or countries.

Conversely, residual dependence need not be zero to remain idiosyncratic. The source gives a nearest-neighbor covariance example with unit variances and nonzero correlations only between adjacent units. Such dependence can have a bounded largest eigenvalue even in a growing panel. Averaging across a large cross section still suppresses it, though less trivially than averaging independent noise.

Divergence is required almost everywhere rather than at every frequency. Differencing can annihilate common variation at frequency zero without destroying its common-factor status over the rest of the spectrum. For example, differencing a common white-noise component introduces the transfer function $1-e^{-i\omega}$, which vanishes at zero. This motivates the almost-everywhere formulation and avoids excluding ordinary transformed economic series for a single-frequency degeneracy.

These assumptions are population properties. A finite sample cannot conclusively distinguish a slowly diverging eigenvalue from a large but eventually bounded one without stronger rate restrictions. That limitation later explains why the paper uses a heuristic factor-count rule rather than claiming a universally consistent finite-sample test for $q$ under its very general assumptions.

## Observable spectral separation

Proposition 1 shows that the first $q$ dynamic eigenvalues of the observed spectrum diverge and the $(q+1)$st remains uniformly bounded. The argument uses eigenvalue bounds for the sum of positive semidefinite matrices:

$$
\lambda_j(S_n^\chi)\le\lambda_j(S_n)
\le\lambda_j(S_n^\chi)+\lambda_1(S_n^\xi).
$$

For $j\le q$, divergence of the common eigenvalue passes through to the observed eigenvalue. For $j=q+1$, the common spectrum has rank at most $q$, so the upper bound reduces to the bounded idiosyncratic maximum. The assumption about unobserved pieces thus becomes a recognizable property of the observed population spectrum.

“Dynamic eigenvalue” means an eigenvalue as a function of frequency. It is not an eigenvalue of the ordinary contemporaneous covariance matrix. Spectral decomposition uses the entire collection of lagged covariance matrices and therefore distinguishes relationships whose timing differs across series.

The paper cites a companion representation result establishing the converse under the relevant formulation: the observed spectral eigenvalue separation can imply a common-plus-idiosyncratic representation. In this article, the factor representation is assumed from the outset and the main work concerns recovery and estimation. The note should not attribute the full independent representation theory to the empirical estimator alone.

For implementation, it is the leading spectral subspace that matters. Signs or complex phases of individual eigenvectors are arbitrary, and rotations within a retained eigenspace do not change the projection. Building the estimator from the projector rather than trying to align every eigenvector by its sign at every frequency avoids attaching economic meaning to an arbitrary numerical basis.

## Population estimator and proof mechanism

Let $p_{nj}(\omega)$ be normalized row eigenvectors of $S_n(\omega)$, ordered by eigenvalue. Their Fourier coefficients define two-sided filters $p_{nj}(L)$. The dynamic principal-component series are $p_{nj}(L)x_{nt}$. Different components are orthogonal at all leads and lags, not merely contemporaneously.

The projection of series $i$ onto the space generated by all leads and lags of the first $q$ components is

$$
\chi_{it,n}=K_{ni}(L)x_{nt},
$$

where the frequency response is the $i$th row of the leading-eigenspace projector:

$$
K_n(\omega)=\sum_{j=1}^q p_{nj}(\omega)^*p_{nj}(\omega).
$$

Here the star is conjugate transpose. Proposition 2 states that $\chi_{it,n}\to\chi_{it}$ in mean square for every fixed series and date as $n\to\infty$.

The proof has two components. First, the coefficients applied to idiosyncratic noise become diffuse. Because a single series has bounded spectral density while a common eigenvalue diverges, its coordinate in the corresponding normalized eigenvector must vanish. The squared norm of the reconstruction filter for a fixed series therefore tends to zero after integration over frequency. The bounded idiosyncratic spectral norm then forces the variance of filtered idiosyncratic contamination to vanish.

Second, the retained principal-component space must contain the common information asymptotically. The Appendix normalizes the leading dynamic components and shows that their projections onto the common-shock space have vanishing residual spectra. The reverse projection has a residual with the same spectral trace, so the spaces approach one another. This supports recovery of the common component, rather than merely proving that some filtered noise disappears.

The simple special case $x_{it}=u_t+\xi_{it}$ makes the first mechanism transparent. The reconstruction is the cross-sectional average, $u_t+n^{-1}\sum_i\xi_{it}$, and independent unit-variance residuals contribute variance $1/n$. The general estimator extends this diversification across both series and time with data-dependent frequency weights.

## Identification and overestimating the factor count

Because the population projection is a function of the observable process, any alternative representation satisfying the assumptions must yield the same limiting common component and hence the same residual. Corollary 1 also fixes the minimal common shock count. It does not fix the shock basis: different orthogonal or dynamic representations of the same common space can remain observationally equivalent.

Corollary 2 considers retaining a fixed number $q^*>q$ of dynamic components. The average across series of the expected squared difference between the overfitted and correctly specified projections tends to zero. Extra retained eigenvalues are bounded, so their total added variance divided by the growing number of series disappears.

This is a cross-sectional average asymptotic result, not a claim that extra components never harm a particular series or finite sample. It does not justify choosing a number of factors that grows rapidly with panel width, and it does not establish real-time forecast robustness. The practical suggestion to err modestly upward in factor count should be understood within those limits.

Underspecifying $q$ is different. Omitting a diverging common direction can remove a nonvanishing part of the common component. The paper's factor-count discussion consequently emphasizes a spectral gap and the behavior of eigenvalues as series are added, while acknowledging that finite-sample selection remains heuristic under its broad conditions.

## Sample algorithm in reproducible form

Section IV supplies the estimator. After making the panel stationary and fixing its scale, choose an integer lag-window width $M$. Estimate autocovariance matrices $\widehat\Gamma_k$ for $k=0,\ldots,M$, and use $\widehat\Gamma_{-k}=\widehat\Gamma_k'$. Form a Bartlett-window spectral estimate on $2M+1$ equally spaced frequencies:

$$
\widehat S_n(\omega_h)=\sum_{k=-M}^{M}\widehat\Gamma_k
\left(1-\frac{|k|}{M+1}\right)e^{-ik\omega_h},\qquad
\omega_h=\frac{2\pi h}{2M+1}.
$$

A conventional constant spectral normalization can be included consistently; it does not change eigenvectors. At each frequency, obtain the first $q$ eigenvectors and construct their projector $\widehat K_n(\omega_h)$. Invert the discrete Fourier transform:

$$
\widehat K_{n,k}=\frac1{2M+1}\sum_{h=0}^{2M}\widehat K_n(\omega_h)e^{ik\omega_h},\qquad k=-M,\ldots,M.
$$

The common-component estimate is

$$
\widehat\chi_{nt}=\sum_{k=-M}^{M}\widehat K_{n,k}x_{n,t-k},
$$

using only available terms near the endpoints. A code implementation must preserve the Fourier sign convention, covariance orientation, and conjugate symmetry so the resulting reconstructed series are real up to floating-point error. At $M=0$, this reduces to ordinary static principal-component projection, providing a useful limiting check.

The same $M$ serves as the spectral lag window and the reconstruction-filter truncation. The simulations use $M=\operatorname{round}((2/3)T^{1/3})$. The theory requires $M\to\infty$ and a restriction of order $M^3/T$ bounded for the stated proof. The authors tried information criteria for bandwidth selection but report that ordinary AIC and BIC tended to choose too small a window; they leave a more satisfactory data-dependent rule for further work.

## Consistency, endpoints, and information availability

The sample theorem strengthens the process assumptions to obtain uniformly consistent spectral estimates for each fixed finite cross section. The paper assumes a linear-process representation with finite fourth moments and a weighted absolute-summability condition on filter coefficients. It then combines spectral estimation with the large-cross-section population recovery result.

The conclusion is formulated as follows: for any desired error probability and tolerance, choose a sufficiently large cross section, then a sufficiently large time length depending on that cross section and tolerance. The paper does not provide a simple unrestricted joint $n/T$ rate guarantee. Its discussion explicitly identifies sharper rate characterization as further work.

The estimator also requires a central date sequence $t^*(T)$ whose relative position stays away from both endpoints. A two-sided filter at a fixed early date is forever missing presample observations. At the last date, it is missing future observations. Merely increasing panel width does not supply those time observations. Consequently, interior consistency should not be restated as endpoint consistency.

This is operationally important for financial use. Reconstructing a historical common component with future data can be appropriate for decomposing variance or studying synchronization. Feeding that same reconstruction into a historical trading backtest would introduce future information unless a genuinely one-sided or forecast-based endpoint method were separately specified and evaluated. The article's euro-area indicator is an estimated historical component, not evidence of a publication-time tradable signal.

A replication should report its endpoint handling and whether the loss criterion includes truncated boundary estimates. The source explains unavoidable truncation but does not fully document every computational convention used in the simulation code. Such choices can matter materially in samples as short as 20 periods.

## Simulation design

Section V studies four two-shock models. All common shocks, idiosyncratic shocks and loading coefficients are independent standard-normal draws, except autoregressive parameters, which are uniform on $[-0.8,0.8]$. The models are:

$$
\text{M1: }x_{it}=a_i u_{1t}+b_i u_{2t}+\sqrt2\,\xi_{it}.
$$

M2 uses the same expression for even-numbered series and replaces both common shocks by their one-period lags for odd-numbered series. Its purpose is to test whether dynamic extraction correctly aligns delayed responses without increasing the number of underlying shocks.

$$
\text{M3: }x_{it}=a_{0i}u_{1t}+a_{1i}u_{1,t-1}
+b_{0i}u_{2t}+b_{1i}u_{2,t-1}+2\xi_{it}.
$$

$$
\text{M4: }x_{it}=\frac{a_i}{1-c_iL}u_{1t}
+\frac{b_i}{1-d_iL}u_{2t}+\sqrt{2.5}\,\xi_{it}.
$$

The noise scales make common and idiosyncratic variance approximately comparable on average. In M4, heterogeneous autoregressive responses create the case that a short finite static stack handles less naturally. Stable coefficients prevent explosive simulated series.

The grid uses $n=10,20,50,100$ and $T=20,50,100,200$, with 400 replications for each model and size combination. The lag-window rule is the one stated above. Performance is measured by normalized squared reconstruction error,

$$
R(\widehat\chi,\chi)=\frac{\sum_{i,t}(\widehat\chi_{it}-\chi_{it})^2}{\sum_{i,t}\chi_{it}^2}.
$$

Table 1 reports its mean and standard deviation across replications. This is error in estimating a known simulated common component, not out-of-sample prediction error or realized investment performance.

An infeasible comparator regresses observations on the true common shocks and their lags, with lag length chosen by AIC; it is reported for $n=100$. Even this comparator estimates response coefficients and approximates infinite autoregressive responses with a finite lag structure. Therefore beating it in M4 does not mean beating an oracle supplied with every true model parameter.

## Simulation results and their interpretation

In M1, mean normalized error falls from 0.554 with standard deviation 0.281 at $n=10,T=20$ to 0.059 with standard deviation 0.008 at $n=100,T=200$. At $n=100,T=100$, the proposed estimate gives 0.084, while the true-shock regression comparator gives 0.030. Static data provide no inherent dynamic-filter advantage, and parameter information available to the comparator helps substantially.

M2 shows the value of aligning delayed common responses. At $n=100,T=100$, the reported mean is 0.016 with standard deviation 0.041, against 0.052 for the true-shock regression comparator. At $T=200$, the values are 0.009 and 0.025. The dispersion relative to the small mean also warns against describing performance using the mean alone.

For M3 at $n=100,T=100$, normalized error is 0.103, falling to 0.067 at $T=200$. The comparator gives 0.051 and 0.025. For M4, however, the proposed method at $n=100,T=100$ gives 0.108 versus 0.114 for the comparator, and at $T=50$ gives 0.167 versus 0.199. At $T=200$, the comparator is slightly better, 0.067 versus 0.073.

These results support the claim that frequency-domain projection can recover common components in modest samples, particularly when the common responses have meaningful dynamics. They do not establish a universal numerical convergence rate or superiority over every state-space or one-sided estimator. The source supplies no simulation random seed, full initialization/burn-in convention for M4, or code-level tie-breaking details. Those should be documented in a new replication rather than invented as features of the original experiment.

## What the delayed-response experiment isolates

Model M2 illustrates the difference between contemporaneous dimension and dynamic dimension without requiring an infinite filter. At a fixed date, even-numbered series load on two current shocks, while odd-numbered series load on two previous shocks. Since the shocks are white noise, these current and previous values constitute four independent contemporaneous random quantities. A purely static representation can therefore need four coordinates to recover the common variation of the full panel. Yet only two new common innovations arrive each period. In the frequency domain, the odd-series responses differ by a phase factor, and the common spectrum still has rank two.

This example gives a precise meaning to the claim that dynamic extraction accommodates timing. It does not create extra economic information or assume that current shocks are observable. It recognizes that a lead-lag relationship links what appear contemporaneously to be separate common directions. The reconstructed historical component can use neighboring dates to recover that relationship, which also explains why the advantage is tied to a two-sided information set.

For M4, heterogeneous autoregressive coefficients produce a stronger distinction. Different responses have different infinite lag profiles. A fixed finite stack of shocks gives only an approximation unless the collection of response filters admits a suitable finite-dimensional reduction. The spectral estimator operates on the common dynamic space directly, while the infeasible regression comparator still chooses a finite number of lags. Its oracle access is to shocks, not to the infinite response functions. This is why the numerical comparison must be interpreted as a comparison of estimation strategies with different approximation errors.

These examples also suggest useful implementation diagnostics. A static simulated model should reduce to ordinary principal-component projection when the lag window is set to zero. A delayed two-shock model should display two strong spectral eigenvalues even if its ordinary covariance requires more directions. When reconstructing real-valued data, frequency conjugate pairs must produce real filter coefficients after the inverse transform. These checks follow from the specified models and algebra; they are proposed verification steps, not additional simulation results claimed by the authors.

## Euro-area coincident indicator

The empirical panel pools seven quarterly macroeconomic categories across ten euro-area countries, excluding Luxembourg. The countries listed are Germany, France, Italy, the Netherlands, Ireland, Spain, Finland, Austria, Belgium and Portugal. Categories are GDP, private consumption, investment, CPI, the long-minus-short interest-rate spread, economic sentiment, and industrial production. Missing country-category series leave 63 series; Ireland has no GDP, consumption or investment series in this panel.

The source describes a 1985–1996 sample and reports $T=51$. The precise quarterly endpoints are not given in the accompanying text, and the stated year span does not uniquely reconcile that count. This is a replication detail requiring the original dataset. GDP, consumption and investment use seasonally adjusted constant-1990-price national-currency data; GDP sources are OECD except Germany and Portugal, for which IMF is used. Table 2 lists the sources and remaining transformations by category.

Variables are logged and differenced, except the spread, which is left in levels, and sentiment, which is logged without differencing. Series are divided by their standard deviations. Spectral analysis retains three dynamic factors using a 5% marginal explained-variance rule. This is the heuristic criterion proposed by the paper, not a reported formal test with a sampling significance level.

The authors estimate each available country's GDP common component and combine these using GDP-level weights to construct a euro-area coincident indicator. Other variables affect the indicator through the estimated dynamic space rather than through arbitrary equal weighting. The method automatically uses lead-lag relationships, allowing a leading indicator to contribute with a shifted weight when reconstructing contemporaneous GDP common variation.

The exact weight reference period, currency conversion convention and reversal of the preliminary standardization are not fully specified in the article. Those details are necessary to reproduce an economically scaled aggregate. A simple weighted average of standardized country growth components is not automatically equivalent to a GDP-share-weighted growth rate in original units.

## Empirical findings and use boundaries

Table 3 attributes 85% of aggregate euro-area GDP variance to the common component, leaving 15% idiosyncratic. Aggregate common shares are 70% for consumption, 57% for investment, 74% for CPI, 95% for the spread, 99% for sentiment and 80% for industrial production. National GDP common shares vary substantially: Germany 68%, France 70%, Italy 54%, the Netherlands 35%, Spain 96%, Finland 46%, Austria 55%, Belgium 55%, and Portugal 54%.

High common variance does not necessarily make a variable a good coincident index. Table 4 reports average contemporaneous correlation of each common component with the other categories' common components. For the aggregate, GDP is 0.58, investment 0.55, industrial production 0.51, sentiment 0.41, consumption 0.36, spread 0.14, and CPI -0.20. Sentiment is overwhelmingly common but less synchronized contemporaneously than GDP, consistent with a possible leading role.

The GDP-based choice is therefore supported by its synchronization, not just by its variance share. Three retained dynamic factors also undermine the idea that all relevant comovement in this panel is adequately summarized by one single common shock. Nevertheless, these are in-sample decomposition results conditional on transformations, panel composition, spectral bandwidth and the chosen factor count. They do not identify causal mechanisms behind the components.

For research use, the paper supplies a powerful decomposition of large panels with heterogeneous timing and residual correlation. The enduring lesson is that commonality is about pervasive dynamic dependence, and that a useful aggregate index can be a weighted combination of reconstructed common components rather than one raw factor. Any practical extension to live forecasting or portfolio decisions must explicitly address endpoint information, factor-count and bandwidth sensitivity, data revisions and changing loading structures. Those extensions are outside the demonstrated results of this article.
