# Tests of risk premia in linear factor models

**Frank Kleibergen (2009).** *Journal of Econometrics* 149, 149–173. DOI: 10.1016/j.jeconom.2009.01.013. [Original PDF](../../Finance/RiskPremiaTest.pdf). All 25 PDF pages, including Appendices A–H and references, were read. The note distinguishes the paper’s assumptions and reported findings from algebraic reconstructions and corrections to printed formulas.

## Why this matters

A precisely estimated factor loading and a precisely estimated factor price are different objects. A cross-sectional regression of average returns on estimated loadings can produce a finite, apparently significant price for a factor that hardly explains any return variation. The loading estimates then contribute mostly estimation noise to the second regression. Adding portfolios on which the factor has no exposure can concentrate the resulting estimator around an economically uninformative value. Ordinary errors-in-variables standard-error corrections do not restore identification.

Kleibergen develops tests that remain asymptotically pivotal under the paper’s central limit assumption when loadings are small or zero. The construction borrows the logic of weak-instrument inference: impose the candidate risk premium when estimating the loadings, obtain a pricing residual asymptotically independent of that restricted loading estimate, and test orthogonal components of the residual. The empirical consequence is substantial. Confidence sets for two selected premia exclude zero but are unbounded, while the set for a scaled consumption-growth premium is the entire real line. A conventional bounded interval would convey information that these data do not establish.

The contribution is primarily inferential. It does not propose a new traded factor, forecasting rule, or portfolio strategy. Its practical use is to prevent a factor-pricing exercise from turning imprecise exposure estimates into spurious evidence about economic compensation. A nonrejection can mean insufficient identification; it need not validate the model.

## Model, units, and the crucial probabilistic assumption

Let $R_t\in\mathbb R^n$ be asset returns in excess of the riskless return, $F_t\in\mathbb R^k$ observed factors, $\beta\in\mathbb R^{n\times k}$ loadings, $\lambda_1$ a common zero-beta return, and $\lambda\in\mathbb R^k$ factor risk premia. The pricing restrictions are

$$
E[R_t]=\iota_n\lambda_1+\beta\lambda,
\qquad \operatorname{Cov}(R_t,F_t)=\beta V_F,
\qquad E[F_t]=\mu_F.
$$

$V_F$ is positive definite. A premium has the units of its associated factor per observation period; changing a factor’s scale changes its loading and premium reciprocally. The paper’s quarterly empirical estimates are not annualized in this note, and premia on macroeconomic quantities cannot be relabeled as portfolio percentage returns without the original factor normalization.

The population representation is

$$
R_t=\iota_n\lambda_1+\beta(F_t-\mu_F+\lambda)+u_t.
$$

Writing $f_t=F_t-\bar F$ gives the paper’s sample-centered representation

$$
R_t=\iota_n\lambda_1+\beta(f_t+\lambda)+\varepsilon_t,
\qquad \varepsilon_t=u_t+\beta(\bar F-\mu_F).
$$

The essential condition is the paper’s Assumption 1, a joint central limit theorem for the sum of $\varepsilon_t$ and its products with $F_t$, with covariance $Q\otimes\Omega$, where $Q=E[(1,F_t')'(1,F_t')]$. Under this assumption its Lemma 1 gives

$$
\sqrt T
\begin{pmatrix}
\bar R-\iota_n\lambda_1-\beta\lambda\\
\operatorname{vec}(\widehat\beta-\beta)
\end{pmatrix}
\Rightarrow
\begin{pmatrix}\psi_R\\\operatorname{vec}(\Psi_\beta)\end{pmatrix},
$$

with independent normal blocks having covariances $\Omega$ and $V_F^{-1}\otimes\Omega$.

This separable covariance is an assumption to verify, not a consequence of constant unconditional variances alone. There is a subtle issue in the paper’s claim that independent disturbances in the original population model automatically suffice. Under independent Gaussian $u_t$ and $F_t-\mu_F$, with fixed nonzero $\beta$, direct calculation instead gives

$$
\operatorname{Var}\{\sqrt T(\bar R-E[R_t])\}
=\Omega_u+\beta V_F\beta',
\qquad
\operatorname{Avar}\{\sqrt T\operatorname{vec}(\widehat\beta-\beta)\}
=V_F^{-1}\otimes\Omega_u.
$$

The common sample-mean term in $\varepsilon_t$ cannot be discarded merely because its variance at an individual date tends to zero. Thus the two blocks generally do not share the same $\Omega$ in that unconditional interpretation. For a scalar illustration with $\beta=0.5$, $V_F=4$, and $\Omega_u=1$, the mean block has variance 2 while the loading block has variance 0.25. Choosing $\Omega=2$ to fit the first block would incorrectly give 0.5 for the second. A sufficient interpretation for the paper’s simulation is a fixed, sample-demeaned factor sequence and independently generated homoskedastic Gaussian $\varepsilon_t$ in the centered representation. The following tests are stated under Assumption 1; their applicability to an unconditional factor-mean estimation problem requires a compatible joint covariance argument. This qualification is a derivation in this note, not a correction supplied by the author. For the local weak-loading sequence $\beta=B/\sqrt T$, the additional mean covariance $\beta V_F\beta'$ tends to zero. The qualification concerns the fixed nonzero-loading unconditional interpretation; it does not by itself invalidate the local weak-loading experiment.

## Why two-pass estimation breaks down

The first pass estimates

$$
\widehat\beta=
\left[\sum_t(R_t-\bar R)f_t'\right]
\left[\sum_t f_tf_t'\right]^{-1}.
$$

Let $Z=(\iota_n,\widehat\beta)$. The Fama–MacBeth estimator is $(Z'Z)^{-1}Z'\bar R$, equivalently the time average of cross-sectional coefficients obtained with the same estimated loadings. The GLS alternative replaces the Euclidean metric with $\widehat\Omega^{-1}$, where the unrestricted time-series residual covariance uses divisor $T-k-1$.

With a fixed, full-rank cross-sectional design $(\iota_n,\beta)$, standard asymptotic arguments can support normal inference. To expose the failure near nonidentification, take $\beta=B/\sqrt T$ and define $M_1=I_n-\iota_n\iota_n'/n$. The factor-premium component has the following reconstructed limit under Lemma 1:

$$
\widehat\lambda-\lambda\Rightarrow
\big[(B+\Psi_\beta)'M_1(B+\Psi_\beta)\big]^{-1}
(B+\Psi_\beta)'M_1(\psi_R-\Psi_\beta\lambda).
$$

The right side is a random ratio of correlated quantities. There is no $\sqrt T$ concentration of $\widehat\lambda$ about $\lambda$ in this local sequence. When $B=0$, the true premium is unidentified and the limit of the estimator itself is

$$
(\Psi_\beta'M_1\Psi_\beta)^{-1}\Psi_\beta'M_1\psi_R.
$$

It remains random even as the time sample grows. If the true mean return is a fixed vector outside the zero-beta pricing restriction, the corresponding second-pass coefficient can diverge at rate $\sqrt T$. Whitening changes the metric but does not remove the weak-identification problem. The source characterizes a multivariate-$t$ limit for GLS in the zero-loading case; finite absolute moments require orders strictly below its degrees of freedom, rather than including the boundary implied by the paper’s loose phrase “up to” $n-k$.

There is a separate many-assets mechanism. Keep only $n_1$ nonzero-loading assets, let $n_1$ stay fixed, and let $n/T\to c$. Most rows then add loading-estimation noise instead of population exposure information. The source’s Eq. (12) reports a bias toward $\mu_F$ of $(\beta_1'\beta_1+W)^{-1}W(\mu_F-\lambda)$, defining $W=\lim\operatorname{tr}(\Omega)/n\,V_F^{-1}$. Its own Appendix B, Box IV, contains $(n/T)(\Psi_\beta'\Psi_\beta/n)$. With that definition of $W$, this term tends to $cW$, so the corresponding scaling is

$$
(\beta_1'\beta_1+cW)^{-1}cW(\mu_F-\lambda).
$$

This is a correction to the displayed scaling, or equivalently requires redefining $W$ to absorb $c$. It is not a new proof of the paper’s entire many-assets limit. The qualitative conclusion is the same: adding many uninformative assets can pull a premium estimate toward the factor mean. The fixed-$n$ pivotal test theorems below should not be treated as a uniform high-dimensional guarantee for arbitrary $n/T$.

## Restricted loadings and the independent pricing residual

Remove the common zero-beta return by taking differences relative to the last asset. Set $p=n-1$,

$$
X_t=R_{1:n-1,t}-\iota_pR_{nt},
\qquad B=\beta_{1:n-1,:}-\iota_p\beta_{n,:},
\qquad E[X_t]=B\lambda.
$$

Let $J=(I_p,-\iota_p)$ and $\Sigma=J\Omega J'$. For a candidate $\lambda_0$, define

$$
\widehat V_F=T^{-1}\sum_t f_tf_t',
\qquad Q_0=\widehat V_F+\lambda_0\lambda_0',
$$

$$
\widetilde B_0=
\left[T^{-1}\sum_t X_t(f_t+\lambda_0)'\right]Q_0^{-1},
\qquad e_0=\bar X-\widetilde B_0\lambda_0,
$$

$$
d_0=1-\lambda_0'Q_0^{-1}\lambda_0
=\frac{1}{1+\lambda_0'\widehat V_F^{-1}\lambda_0}>0.
$$

This is a no-intercept restricted time-series regression, recomputed for each tested premium. It is not the ordinary first-pass beta estimate held fixed over the confidence-set grid. Use residuals $a_t=X_t-\widetilde B_0(f_t+\lambda_0)$ and, matching the main-text Theorem 3 convention,

$$
\widetilde\Sigma_0=(T-k)^{-1}\sum_t a_ta_t'.
$$

Appendices also use $T-k-1$, while Gaussian maximum likelihood uses $T$. Those divisors are asymptotically equivalent for fixed dimensions, but not numerically identical. A replication must record one convention throughout; the formulas here use $T-k$ for the tests and $T$ for the likelihood objective. The $X_t$ in these residuals is the asset-difference return, without subtracting its sample mean. Demeaning it would remove the pricing information being tested.

Lemma 2 establishes, under the null and Assumption 1, asymptotic independence of $\sqrt T e_0$ and $\sqrt T\operatorname{vec}(\widetilde B_0-B)$. Their limiting covariances are $d_0\Sigma$ and $Q_0^{-1}\otimes\Sigma$, interpreted through probability limits of the sample matrices. The result follows by an explicit linear transformation of the joint Gaussian limit: subtract the restricted-loading estimation error times $\lambda_0$ from the average-return error. The cross-covariance cancels exactly.

The independence is the mathematical reason for imposing the null in the first stage. Ordinary two-pass Wald residuals contain beta-estimation errors multiplied by the tested premium and do not have the required independence from the estimated beta matrix.

For a directly checkable proof in the fixed-factor Gaussian experiment, let $\eta_t=J\varepsilon_t$ be the contrasted error, $A=T^{-1/2}\sum_t\eta_t$, and $H=T^{-1/2}\sum_t\eta_tf_t'$. They are independent with covariances $\Sigma$ and $\widehat V_F\otimes\Sigma$. The restricted-loading error multiplied by $\sqrt T$ is $D=(H+A\lambda_0')Q_0^{-1}$, and the residual error is $A-D\lambda_0$. Now $\operatorname{Cov}(A,\operatorname{vec}D)=(\lambda_0'Q_0^{-1})\otimes\Sigma$, while $\operatorname{Var}(\operatorname{vec}D)=Q_0^{-1}\otimes\Sigma$. Subtracting $D\lambda_0$ therefore makes the cross-covariance zero and leaves variance $d_0\Sigma$. Joint normality converts zero covariance into independence. This calculation also shows exactly which step a nonseparable or time-dependent covariance would change.

## LM, joint pricing, and overidentification tests

Write $B_0=\widetilde B_0$ and $S=\widetilde\Sigma_0$ for this section. Assume $p>k$ for a nontrivial overidentification test and sufficient residual observations for $S$ to have full rank. Provided the indicated matrices are invertible, the two LM statistics are

$$
\operatorname{FM\!LM}(\lambda_0)=
\frac{T}{d_0}
e_0'B_0(B_0'S B_0)^{-1}B_0'e_0,
$$

$$
\operatorname{GLS\!LM}(\lambda_0)=
\frac{T}{d_0}
e_0'S^{-1}B_0(B_0'S^{-1}B_0)^{-1}B_0'S^{-1}e_0.
$$

Each tends to $\chi_k^2$ under the null, including local-to-zero or zero population loadings under the stated Gaussian-limit conditions. The estimated loading matrix may still have full column rank from sampling variation. Exact finite-sample rank failures require reporting that the statistic is undefined; silently using a pseudoinverse changes its rank and reference degrees of freedom.

The GLS version is invariant to nonsingular transformations of the asset-difference returns. The FM version is not. In particular, a claim that every variant is invariant to the arbitrary reference-asset transformation would conflict with this distinction. Whitening gives the geometric interpretation: $y=\sqrt{T/d_0}S^{-1/2}e_0$ is asymptotically standard normal independently of the loading estimate, and GLS-LM is its squared projection onto $\operatorname{col}(S^{-1/2}B_0)$.

The factor Anderson–Rubin statistic tests the entire pricing restriction at the candidate premium:

$$
\operatorname{FAR}(\lambda_0)=\frac{T}{d_0}e_0'S^{-1}e_0
\Rightarrow\chi_p^2.
$$

It tests both the value of the premium and whether the model prices the asset means. Its larger degrees of freedom can reduce power relative to a targeted premium test. Define

$$
J_{\rm GLS}=\operatorname{FAR}-\operatorname{GLS\!LM}.
$$

This is the squared orthogonal-complement component of $y$, tends to $\chi_{p-k}^2$, and is asymptotically independent of GLS-LM. An analogous $J_{\rm FM}=\operatorname{FAR}-\operatorname{FM\!LM}$ uses projection onto $\operatorname{col}(S^{1/2}B_0)$ and has the same degrees of freedom and independence relationship with FM-LM.

LM alone can fail to reject at a poor fit: its score is zero not only at the likelihood maximum but also at other stationary points. The paper therefore combines a pricing-misspecification test with an LM test. Reject if $J$ exceeds its $1-\alpha_J$ critical value, or if LM exceeds its $1-\alpha_L$ critical value. Independence gives overall asymptotic rejection probability

$$
\alpha=1-(1-\alpha_J)(1-\alpha_L)
=\alpha_J+\alpha_L-\alpha_J\alpha_L.
$$

The paper’s following prose prints a plus sign before the product; that is an arithmetic error. Its chosen 1% and 4% components yield 4.96%, close to the reported 5%, not 5.04%. This combination checks both model fit and the premium while avoiding the particularly weak power of LM at a bad stationary point.

## Conditional likelihood ratio and scaling corrections

For one factor, the main-text CLR form is

$$
\operatorname{CLR}(\lambda_0)
=\frac12\left[
\operatorname{FAR}-r+
\sqrt{(\operatorname{FAR}+r)^2-4rJ_{\rm GLS}}
\right].
$$

Conditional critical values depend on $r$. Given $r\ge0$, draw independently $U\sim\chi_k^2$ and $V\sim\chi_{p-k}^2$, and simulate

$$
C(r)=\frac12\left[
U+V-r+\sqrt{(U+V+r)^2-4rV}
\right].
$$

For $k=1$ this supplies the paper’s conditional calibration; for multiple factors the corresponding expression supplies a bound using a rank-strength statistic. As $r\to0$, the expression becomes $U+V$; as $r\to\infty$, it tends to $U$. A fixed chi-square cutoff therefore cannot replace conditional calibration over an arbitrary strength range.

There are consequential printing differences. Main-text Eq. (27) defines $r=Q_0B_0'S^{-1}B_0$ for $k=1$, without $T$. Appendix F instead includes $T$ in its strength matrix and uses the raw second moment $M_X=T^{-1}\sum_tX_tX_t'$ in that derivation. Moreover, its final line for LR omits the outer $1/2$ that is present in Eq. (27) and follows from its preceding eigenvalue formula. The appendix also uses a first-order logarithm expansion: its quadratic expression should not be presented as the exact finite-sample Gaussian log-likelihood ratio.

A coherent Gaussian-limit reconstruction based on Lemma 2 is

$$
r=TQ_0B_0'S^{-1}B_0\quad(k=1),
$$

or the smallest eigenvalue of $TQ_0^{1/2}B_0'S^{-1}B_0Q_0^{1/2}$ for the multivariate strength bound. The $T$ is required because $\operatorname{Var}(\widetilde B_0)$ is of order $1/T$: with $B_0=O_p(T^{-1/2})$, this statistic is $O_p(1)$; without $T$ it collapses toward zero. Under the local weak-loading experiment, $M_X$ and the residual covariance have the same leading probability limit. Under fixed strong loadings they need not agree. This reconstructed convention is mathematically motivated and explicitly differs from the inconsistent printed definitions; the paper’s unavailable simulation code is needed to establish its exact numerical implementation.

One should implement the readily specified LM/FAR tests first and treat CLR reproduction as requiring these declared choices. Computing an exact concentrated likelihood ratio separately is useful, but its conditional reference distribution must be justified for that exact statistic rather than automatically borrowed from the quadratic approximation.

## Maximum likelihood and nuisance premia

The paper gives an eigenvalue route to the Gaussian maximum likelihood estimate that avoids selecting an arbitrary stationary point. Define $z_t=(1,f_t')'$, $M_{zz}=T^{-1}\sum_tz_tz_t'$, $M_{zX}=T^{-1}\sum_tz_tX_t'$, and $M_X=T^{-1}\sum_tX_tX_t'$. Solve the generalized eigenproblem

$$
M_{zX}M_X^{-1}M_{zX}'q_j=\theta_jM_{zz}q_j.
$$

Order the eigenvalues from largest to smallest. Stack the eigenvectors for the largest $k$ roots as $(q_1,\ldots,q_k)=(w_1',W_2')'$, with $w_1$ a $1\times k$ row and $W_2$ a $k\times k$ matrix. If $W_2$ is nonsingular,

$$
\widehat\lambda_{\rm ML}=W_2^{-\prime}w_1'.
$$

The covariance in the likelihood is the residual second moment with divisor $T$; the $M_X$ above is the raw second moment used in the eigenproblem, not that residual covariance. The exact determinant decomposition is proportional to $\prod_{j=1}^k(1-\theta_j)$, so choosing the largest roots minimizes the determinant without requiring the appendix’s logarithm approximation. Singular $W_2$ signals a boundary or unbounded parameterization and cannot be fixed by arbitrarily truncating the premium.

For strongly identified interior parameters the source’s information-matrix calculation yields

$$
\widehat{\operatorname{Var}}(\widehat\lambda_{\rm ML})
=\frac{1+\widehat\lambda_{\rm ML}'\widehat V_F^{-1}\widehat\lambda_{\rm ML}}{T}
(\widetilde B'\widetilde\Sigma^{-1}\widetilde B)^{-1}.
$$

This is useful as a comparison but does not make MLE-based Wald intervals valid under weak identification. The numerator is the familiar error-in-variables inflation; the loading-information matrix can still be nearly singular.

For a subset test partition $\lambda=(\nu',\theta')'$, with $k_\nu+k_\theta=k$. At a candidate $\theta_0$, estimate $\nu$ by the null-restricted maximum likelihood procedure. The paper obtains this by residualizing both $X_t$ and $(1,f_{1t}')'$ against $f_{2t}+\theta_0$, then applying the eigenvalue construction to those residuals. Evaluate the full statistics at $(\widetilde\nu(\theta_0),\theta_0)$.

Theorem 9 gives bounding, potentially conservative, reference distributions: GLS-LM is bounded by $\chi_{k_\theta}^2$, FAR by $\chi_{n-k_\nu-1}^2$, and the pricing statistic uses $\chi_{n-k-1}^2$. The CLR bound draws the first component with $k_\theta$ degrees of freedom and the second with $n-k-1$, conditional on the corresponding strength statistic. These are not ordinary plug-in exact chi-square identities after estimating nuisance premia. Confidence sets invert the nonrejection region over the entire parameter domain; a large finite grid is not evidence that a set is bounded.

## Experiments and what they show

The simulations use the covariance and loadings associated with Lettau–Ludvigson’s 25 size and book-to-market portfolios, a demeaned value-weighted return factor, and a reported $T=143$. The source describes quarterly observations from 1963Q3 through 1998Q3; those endpoints contain 141 quarters inclusively, not 143. Reproduction therefore requires the actual observation dates rather than silently choosing one of these conflicting descriptions.

Panel 1 separates several mechanisms. With zero loadings and a correctly specified mean, increasing $T$ through 143, 429, 858, and 1,430 leaves the premium estimator’s spread materially nonzero. With zero loadings and an independently drawn misspecified mean vector from $N(0,I_n)$, its spread increases. For the many-assets illustration only the first loading is 0.25, the true premium is 5, and the common zero-beta return is 4.18. Adding assets with zero loadings, from $n=2$ through 10, 17, and 25, shifts the estimator toward the demeaned factor mean of zero. A further misspecification experiment adds a vector drawn from $N(0,0.04I_n)$. These are simulation inputs in the source’s return units, not annual percentage estimates. Figure 1.4’s caption uses the mean $\iota_n\lambda_1+5\beta+c$, whereas adjacent prose drops the factor 5; the caption and the stated premium-5 comparison identify the coherent design.

Panel 2 generates independent Gaussian errors with the fitted covariance, keeps the observed demeaned factor sequence, and uses loading multipliers 1, 0.5, and 0.25. It tests $\lambda_0=10$ across a range of true premia. Rejection frequency at 10 is size; elsewhere it is power. This distinction matters because a curve that rejects often at the null is not a powerful valid test.

At full loadings FM-Wald and MLE-Wald have roughly nominal size in the displayed experiment, while GLS-Wald is already distorted. At half and quarter loadings the Wald tests become materially unreliable. LM tests preserve size much better but develop power troughs away from the null because of additional stationary points. The combined $J$–LM tests and CLR avoid those troughs in the illustrated designs. FAR tends to have lower power because it uses 24 degrees of freedom, compared with one for a single-premium LM test. These are graphical findings, not precisely tabulated rejection percentages.

The paper attributes GLS-Wald’s problem partly to inversion of a large residual covariance matrix estimated from the same returns. Its Appendix G supplies geometric discussion, but this is not a license to invert a nearly singular covariance at any dimension. A replication must check $T$, the residual rank, eigenvalues, and conditioning. The PDF does not provide random seeds, Monte Carlo replication counts, numerical power arrays, or a complete numerical covariance matrix; exact curve reproduction is unavailable from the printed article alone.

## Empirical premium estimates and confidence sets

The three models and targeted premia are: market return plus labor-income growth, targeting $\lambda_{\Delta y}$; $cay$, market return, and their product, targeting the scaled-market premium; and $cay$, consumption growth, and their product, targeting the scaled-consumption premium. Here $cay$ is the source’s consumption–aggregate wealth variable. Its construction and the underlying time series are referred to Lettau–Ludvigson; they are not supplied numerically in this PDF.

Table 1 reports the following estimates, with Shanken-corrected standard errors first and uncorrected errors second for the two-pass estimators:

| Target | FM estimate | FM SE, corrected / uncorrected | GLS estimate | GLS SE, corrected / uncorrected | MLE estimate | MLE SE |
|---|---:|---:|---:|---:|---:|---:|
| Labor-income growth | 1.26 | 0.66 / 0.37 | 0.17 | 0.17 / 0.16 | 6.13 | 5.67 |
| Scaled market return | 1.14 | 0.46 / 0.31 | 0.17 | 0.16 / 0.15 | 1.80 | 0.87 |
| Scaled consumption growth | 0.060 | 0.025 / 0.017 | 0.027 | 0.011 / 0.010 | 0.008 | 0.060 |

The table itself does not support the text’s blanket assertion that all corrected FM estimates exclude zero at a two-sided 95% normal cutoff: $1.26/0.66=1.909$, below 1.96. The other corrected FM ratios are approximately 2.478 and 2.400. The labor-income interval computed from its printed corrected SE is approximately $[-0.034,2.554]$. The discrepancy may concern the plotted calculation or the printed table, but cannot be resolved by changing the significance convention without evidence. It does not overturn the paper’s main identification comparison.

Panel 3 explicitly plots **one minus the p-value**, so the 0.95 horizontal line is a rejection threshold on that transformed axis. A conventional p-value implementation rejects below 0.05. The labels prevent reversing the confidence-set inclusion rule.

The source reports that FAR, CLR, and combined $J_{\rm GLS}$–GLS-LM sets for labor-income growth and scaled market return are unbounded but exclude zero. This is evidence against zero conditional on the maintained model and inference assumptions, coupled with poor information about the magnitude. For the scaled consumption-growth premium their sets contain the whole real line. The appropriate conclusion is that these tests do not identify its price: they neither establish a priced factor nor reject the model simply from the lack of a finite interval. The article gives plots and qualitative set descriptions rather than numerical finite endpoints or a full grid, so none are invented here.

## Reproduction sequence and limits

An implementable exercise begins by obtaining the exact aligned return and factor matrix, recording excess-return construction, factor scaling, centering, dates, and missing-data rules. Recompute ordinary first-pass betas and FM/GLS estimates as diagnostics. Then remove the common zero-beta return by a fixed asset contrast, compute $\widehat V_F$, and for every null premium recompute $Q_0$, restricted loadings, residual covariance, $d_0$, and the LM/FAR/$J$ statistics. Use linear solves and symmetric factorizations rather than literal inverse multiplication. Verify numerically that FAR minus each LM is nonnegative within rounding and that the GLS statistic is invariant to nonsingular changes of the asset-difference basis.

Declare the residual-covariance divisor, the corrected union-test size, and the chosen CLR strength convention before calculating p-values. For subset inference profile nuisance premia under every tested null, using the largest-root eigenvalue solution and checking singular blocks. To classify a confidence set, expand the grid in both directions and examine analytic tail limits; distinguish an empty set, disjoint intervals, half-lines, the whole line, and a bounded interval. Reporting only the interval around a preferred point estimate defeats the purpose of weak-identification inference.

The substantive limits are the maintained pricing restriction, the separable joint Gaussian-limit covariance, constant error covariance in the analyzed model, and sufficient residual rank for the matrix operations. Heteroskedasticity, serial dependence, factor-mean uncertainty, data-dependent portfolio selection, and growing dimension require additional arguments. In particular, the conclusion’s discussion of sorted portfolios does not prove validity for arbitrary selection on the same returns: the needed conditional moments and limit assumption must survive that selection. No trading-cost, out-of-sample investment, or economic-welfare result is estimated here. The paper’s value is a disciplined statement of how little a two-pass premium estimate may identify, together with concrete tests that expose that uncertainty under their stated conditions.
