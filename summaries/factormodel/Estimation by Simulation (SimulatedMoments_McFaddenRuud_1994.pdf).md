# Estimation by Simulation

Daniel McFadden and Paul A. Ruud. *Review of Economics and Statistics* 76(4), November 1994, pp. 591–608.

Source: [SimulatedMoments_McFaddenRuud_1994.pdf](../../Finance/SimulatedMoments_McFaddenRuud_1994.pdf), 19 PDF pages including the JSTOR cover. The full article, all five tables, and Appendices A–C were read. The [published-paper copy hosted on Ruud's Vassar site](https://facultysites.vassar.edu/paruud/courses/simulation/McFadden%20Ruud%20-%20RESTAT%20-%20Estimation%20by%20Simulation.pdf) supplied searchable text for the local image-only scan. Equations and numerical tables were visually checked in the local source. Page references below are printed pages.

## Why this matters

Simulation makes an otherwise intractable likelihood or moment condition computable, but computational feasibility does not guarantee statistical validity. A probability simulator can be unbiased while its logarithm, reciprocal, or score ratio is biased. With a fixed number of draws per observation, those nonlinear biases need not disappear as the dataset grows. Conversely, an unbiased moment simulator can remain consistent with very few draws, although the added simulation variance can make it practically unattractive.

McFadden and Ruud organize these issues around an approximate score and a simulated correction to its model-implied mean. Their contribution is broader than a recipe for multinomial probit: it is a way to turn computationally convenient, potentially biased score approximations into valid estimating equations. The framework also clarifies conditional versus unconditional simulation, the information lost through partial observation, and why trying to mimic ideal weights with noisy ratios can make an estimator worse.

The empirical illustrations are controlled Monte Carlo exercises for binary probit and trivariate tobit. They are not financial return experiments. Their relevance to quantitative research is methodological: latent-factor models, censored data, choice models, and structural likelihoods often contain the same difficult integrations. The paper provides a basis for deciding where a finite simulation budget should go and for separating score-approximation error from the noise introduced by correcting that error.

## Start with the moment equation, not the simulated likelihood

For observations $(Y_n,X_n)$ and parameter $\theta$, suppose an ideal moment condition is

$$
E[s(\theta_0;Y,X)\mid X]=0.
$$

A familiar form is $s=W(X,\theta)[T(Y,X,\theta)-E_\theta(T\mid X)]$. $T$ is a tractable statistic and $W$ a weighting matrix. Many exponential-family scores have this structure. If an unbiased simulator of the conditional expectation is available, replacing that expectation by an average of $R$ independent simulated statistics preserves the moment restriction.

When the simulated statistics have the same conditional distribution as the observed statistic and the weights are fixed conditional on $X$, their variance adds a factor $1+1/R$ to the corresponding classical moment-estimator covariance. This simple factor depends on that particular design. A variance-reduced simulator, random approximate weights, or a different bias-correction construction need not have the same factor.

The difficult part is often the weighting function. For discrete choice, ideal weights contain derivatives of log probabilities. A simulated probability may be unbiased, but a derivative divided by that simulated probability is generally biased. A random weight can still be valid if it is independent of the simulated residual and preserves identification, but it need not be efficient. Reusing the same draws in weights and residuals can create correlation that invalidates the zero-mean restriction.

The general construction begins with a convenient approximation $g(\theta;Y,X,\omega_1)$. The auxiliary variable $\omega_1$ contains fixed approximation coefficients or simulated random numbers. Define its model-implied mean, conditional on those coefficients, as

$$
b(\theta;X,\omega_1)
=E_\theta[g(\theta;Y^\theta,X,\omega_1)\mid X,\omega_1].
$$

Use an unbiased simulation $\widehat b$ of this expectation, driven by an additional random stream $\omega_2$, and form

$$
e(\theta;Y,X,\omega_1,\omega_2)
=g(\theta;Y,X,\omega_1)-\widehat b(\theta;X,\omega_1,\omega_2).
$$

At the truth the two terms have the same conditional expectation. The correction removes the mean error of the approximation, not necessarily its inefficiency. Identification still requires that the resulting population moment uniquely identify $\theta_0$; subtracting a mean does not magically create information about an unidentified parameter.

One direct correction draws $R_2$ artificial outcomes from the model at the trial parameter and averages $g$ over them, keeping the approximation draws $\omega_1$ fixed. Reusing those approximation draws across the observed and synthetic evaluations can reduce noise. Independence is needed between the outcome-generation stream and the stream used to construct random weights or approximations when the proof relies on their conditional separation. This is a more precise rule than either “reuse every draw” or “never reuse draws.”

If the approximate score is already unbiased, subtracting an additional simulated expectation of zero only adds noise. The authors emphasize this case: bias correction is a tool for an identified bias, not a mandatory decoration of every simulated estimator.

## Discrete choice: two routes to the score

Let alternative $j$ have latent utility $u_j=x_j'a(\theta,\eta)$, where the random coefficients are generated from a known innovation law. The observed indicator $Y_j$ is one for the maximizing alternative. For multinomial probit, $a=\beta(\theta)+\Gamma(\theta)\eta$ with standard-normal $\eta$. Choice probabilities are normal orthant probabilities in utility differences.

The observed score can be written

$$
s(\theta;Y,X)=\sum_jY_j\nabla_\theta\log P_j(X,\theta)
=W(X,\theta)[Y-P(X,\theta)].
$$

The second equality follows from $\sum_j\nabla P_j=0$. Unconditional simulation generates complete artificial choices at the covariates and estimates the whole probability vector, regardless of the observed choice. Indicator averages are unbiased but can be discontinuous in parameters. Smooth importance-sampling probabilities can facilitate optimization, yet ratios used as ideal weights remain a separate source of bias.

The conditional route starts from the latent likelihood. If $Y=\tau(Y^*)$ and $L^*$ is the latent log likelihood, differentiation under the integral gives the score identity

$$
\nabla_\theta L(\theta;Y)
=E_\theta[\nabla_\theta L^*(\theta;Y^*)\mid Y].
$$

Simulate latent variables conditional on the observed outcome and average their exact latent scores. For a chosen alternative, this means sampling utility differences in its admissible orthant. Only the observed choice's conditional distribution is required. Exact rejection sampling can supply the correct truncated law, but becomes expensive when the observed event has small model probability.

An approximating truncated sampler or approximate latent score changes the mean, so a correction may again be required. Thus feasible conditional and unconditional methods can converge to the same approximate-score-plus-correction architecture. The label “conditional simulation” does not by itself guarantee that the score simulator is unbiased.

The source's equation (14), p. 601, writes an inverse log likelihood in an intermediate ratio where the inverse likelihood is required. The conditional-expectation identity above is the correct implementation target: its denominator is $\exp L$, not $L$. Normalizing a conditional density by a log likelihood would produce neither a density nor a score.

## General asymptotics and what fixed simulation budgets permit

The paper's generic theory assumes independent observations and independent simulation vectors across observations, conditional on the data. It is not a theorem for an arbitrary serially correlated financial time series. A time-series application requires additional laws of large numbers, central limit conditions, and long-run covariance treatment beyond this article's setup.

Let $e_n(\theta)$ be an $M$-vector of simulated moments and let $D$ be the minimum-distance weight matrix. The estimator approximately minimizes

$$
\overline e_N(\theta)'D\overline e_N(\theta),
\qquad
\overline e_N=N^{-1}\sum_{n=1}^Ne_n,
$$

to an objective error $o_p(N^{-1})$. The parameter set is compact and convex, the truth is interior, and the target nonsimulated moment and its derivative satisfy continuity and integrable-envelope conditions. The identifying derivative $G=-E[\partial s(\theta_0)/\partial\theta']$ must have full column rank; with overidentification it is rectangular, so “nonsingular” should be understood through $G'DG$ rather than as a literal square-matrix requirement.

Two simulation-specific conditions do the main work. First, the centered simulation residual process must be stochastically equicontinuous: small parameter changes produce small aggregate centered changes with high probability, even if individual draws jump. Second, the approximation bias must vanish uniformly after multiplying the average moment bias by $\sqrt N$. Mere pointwise consistency of a simulated probability does not establish either condition.

The asymptotic covariance is

$$
V=(G'DG)^{-1}G'D\Sigma DG(G'DG)^{-1},
$$

where

$$
\Sigma=\Sigma_M+\Sigma_S,
\qquad \Sigma_M=\operatorname{Var}[s(\theta_0;Y,X)],
$$

$$
\Sigma_S=\lim_{N\to\infty}
E\{\operatorname{Var}_\omega[e(\theta_0;Y,X,\omega)\mid Y,X]\}.
$$

The conditional centering makes simulation noise orthogonal to the classical data component. Efficient weighting within the selected moment family uses $D=\Sigma^{-1}$ and gives $(G'\Sigma^{-1}G)^{-1}$. The sentence below Theorem 1 on p. 598 omits this final inverse; the full sandwich formula fixes its intended meaning.

With exact score moments and information matrix $I$, the just-identified covariance becomes

$$
I^{-1}+I^{-1}\Sigma_SI^{-1}.
$$

A fixed number of unbiased independent draws per observation can therefore yield consistency and asymptotic normality. Its simulation contribution persists in the limiting variance. If the score approximation has bias of order $R^{-1}$, the usual centered first-order limit instead requires $R/\sqrt N\to\infty$, under the uniform smoothness conditions producing that rate. Letting $R$ increase very slowly may remove consistency bias but still leave first-order bias at the statistical scale.

For an exactly unbiased score simulator, only variance reduction is needed to recover the MLE limit: a diverging draw count can make simulation variance disappear. The paper gives positive-power growth as an example. The relevant distinction is whether one is eliminating a first-order bias or merely an extra variance term; these demands imply different simulation budgets.

## Singular transformations, importance sampling, and discontinuities

The bias-rate argument expands a smooth transformation $h(Z)$ around the expectation $\mu$ of an unbiased simulator $Z$. With a uniformly Lipschitz derivative, the linear term has mean zero and the remainder is bounded by a constant times $E|Z-\mu|^2=O(R^{-1})$. This yields the stated $R/\sqrt N$ condition.

Probabilities create a serious boundary problem. Even if the true probability is bounded away from zero, a simulator can produce values near zero, making its reciprocal or score ratio explosive. Importance estimates of probabilities can even exceed one. An estimator built from those values can violate moment bounds or acquire singular weights absent from the actual likelihood.

The paper proposes censoring an approximation outside a safe region as one remedy. Its second clause of Lemma 1 claims the same rate using only a Lipschitz transformation. That weaker condition alone generally bounds absolute transformation error by $O(R^{-1/2})$, not $O(R^{-1})$: the kinked function $h(z)=|z-\mu|$ illustrates the difference. The stated first-order rate should therefore be used with a verified smooth Taylor remainder or a separately proved bias bound. This qualification concerns the rate justification, not the general usefulness of controlling singular simulated weights.

Importance sampling provides a flexible way to simulate a mean correction. In conventional density notation, if $Z\sim q$ and the target density is $p_\theta$, the correction uses

$$
\frac1R\sum_{r=1}^R
 g(\theta;Z_r,X,\omega_1)
 \frac{p_\theta(Z_r\mid X)}{q(Z_r\mid X)}.
$$

The proposal must cover the target support and the weighted function must have adequate moments. This expression makes the density ratio explicit; the source's abbreviated notation around Lemma 2 should not be implemented as division by a proposal density without the corresponding target integrand. A proposal that visits a tail too rarely can be unbiased while having unusably large variance.

For rejection samplers, the accepted draw may change discontinuously as the parameter changes. The paper's “probably Lipschitz” condition permits this: within a radius $\delta$, the probability of a discontinuity is bounded by a random envelope times $\delta$, while outside that event the simulator is Lipschitz. The envelope has a finite third moment and also controls the simulator's magnitude. Appendix C uses a dyadic parameter partition to bound squared brackets by order $\delta$, leading to a finite entropy sum and stochastic equicontinuity.

For an acceptance region defined by smooth inequalities, sufficient conditions include Lipschitz movement of each boundary, bounded densities near those boundaries, and control of the expected number of rejection trials. Rare acceptance is doubly costly: it increases computation and can violate the moment condition needed to control discontinuities. Fixing a random stream across trial parameters helps define the comparison, but does not remove these mathematical requirements.

## Conditional simulation and missing information

Let $I_*$ be the information matrix if the latent data were fully observed and $I$ the information in the actual observations. For $R$ independent exact conditional latent-score draws per observation,

$$
\Sigma_S=\frac{I_*-I}{R}.
$$

This is a direct application of total variance to the latent score. The missing-information matrix measures how much the unobserved portion can fluctuate after conditioning on what was observed. Conditional simulation is particularly attractive when observation retains most of the latent information. With severe censoring or coarse choices, the missing-information term can be large.

For unconditional model-outcome simulation of a deterministic moment function, $\Sigma_S=\Sigma_M/R$, giving the familiar $1+1/R$ factor. Neither construction universally dominates the other. Approximation quality, the cost and variance of conditional sampling, and the quality of the chosen moments jointly determine efficiency. Comparing the same raw number of draws is not necessarily a comparison at equal computing cost.

The paper also interprets auxiliary-model moment matching through this framework. A tractable quasi-score can replace an intractable structural score, and simulations can center it. The auxiliary fit is a way of choosing informative moment functions, not a proof that its linear combination is optimal for estimating the structural parameters. Richer auxiliary models can improve approximation but also consume finite-sample information and computation. This discussion motivates examining the information content of moments rather than choosing them solely because an auxiliary likelihood is easy to optimize.

## Binary probit experiment: exact reconstruction

The model has $P(Y=1\mid x)=\Phi(x'\beta)$, with $x=(1,x_2)'$, $x_2$ standard normal truncated to $[-2,2]$, and true coefficients $(\beta_1,\beta_2)=(0,1)$. Each sample contains 50 observations. The comparisons use 1,000 experiments, with draw counts $R=1,5,10$. The single reported coefficient distribution in Table 1 is centered near the true slope of one; the table does not provide a separate intercept distribution.

The intentionally poor probability simulator draws $w\sim\operatorname{Exp}(1)$ and uses

$$
\widetilde p_y(\beta;w)
=\frac{\varphi((2y-1)w-x'\beta)}{\exp(-w)},
\qquad y\in\{0,1\}.
$$

Integrating over the exponential draw maps the positive or negative half-line into the normal probability. Averaging $R$ draws remains unbiased for $P(Y=y\mid x)$. Maximum simulated likelihood maximizes the sum of logarithms of these averages; the log transformation introduces finite-$R$ bias.

The simplest MSM solves

$$
\sum_nx_n\{Y_n-\widetilde p_{1,n}(\beta;\omega_{1n})\}=0.
$$

A weighted version tries to mimic the exact probit score weight $\varphi(x'\beta)/[P_1(1-P_1)]$. To keep probability approximations in the unit interval, the authors normalize independently simulated outcome probabilities:

$$
\widetilde g_y=\frac{\widetilde p_y}{\widetilde p_0+\widetilde p_1}.
$$

The weight uses $\partial\widetilde g_1/\partial\mu$ divided by $\widetilde g_1(1-\widetilde g_1)$, with $\mu=x'\beta$, while the residual retains the unbiased $\widetilde p_1$. Separate streams are used for weight and residual. Normalization can stabilize the support without making the random weight unbiased or preventing it from becoming extreme near zero and one.

The exact MLE in Table 1 has mean 1.0929, standard deviation 0.2917, median 1.0545, and lower/upper quartiles 0.8848/1.2496. Thus even the nonsimulated benchmark has a finite-sample mean above the true slope. Tables 2–4 report differences from that sample's MLE, not errors relative to the true parameter.

| Estimator minus MLE | $R$ | Mean difference | Standard deviation |
|---|---:|---:|---:|
| Unweighted MSM | 1 | −0.0831 | 0.5498 |
| Unweighted MSM | 5 | −0.0093 | 0.3675 |
| Unweighted MSM | 10 | 0.0128 | 0.3102 |
| MSL | 1 | −0.5305 | 0.3381 |
| MSL | 5 | −0.2796 | 0.2500 |
| MSL | 10 | −0.1855 | 0.2152 |
| Weighted MSM | 5 | −0.0484 | 0.3487 |
| Weighted MSM | 10 | −0.0305 | 0.2807 |
| Bias-corrected MSL score | 1 | 0.0218 | 0.8019 |
| Bias-corrected MSL score | 5 | 0.0105 | 0.3528 |
| Bias-corrected MSL score | 10 | 0.0009 | 0.2993 |

Weighted MSM at $R=1$ was numerically unstable and omitted; its blank table cells are failures, not zero errors. At $R=10$, plain MSL still has a mean difference of −0.1855. Bias correction reduces that difference to 0.0009, at the cost of increasing its standard deviation from 0.2152 to 0.2993. At $R=1$ the corrected estimator is workable but very noisy. The results demonstrate a bias–variance tradeoff, not uniform superiority in mean squared error at every draw count.

To reproduce the correction cleanly, define $a_i=\partial\log\widetilde p_i/\partial\mu$ using the approximation stream. The corrected score is

$$
x_n\left[a_{Y_n}(\beta;\omega_{2n})
-\sum_{i=0}^1a_i(\beta;\omega_{2n})
\widetilde p_i(\beta;\omega_{1n})\right].
$$

Conditional on the approximation stream, the model expectation of the first term equals the expectation of the correction. This implements the article's general centering principle. The displayed expression on p. 604 includes an extra $Y_n$ factor on the observed-score term, which would incorrectly discard the zero-outcome score; the formula above removes that inconsistency rather than reproducing it in code.

The text on p. 604 says the unweighted MSM variants have smaller simulation variances than the weighted versions at $R=5,10$. The tabulated standard deviations show the reverse: 0.3675 exceeds 0.3487 and 0.3102 exceeds 0.2807. The numerical tables support only a modest weighted improvement accompanied by stability problems, which is the interpretation retained here.

Clamping probabilities away from boundaries is not a universal fix. The article explains that if a weight's numerator can approach zero while its denominator is bounded, the estimating equations can acquire spurious boundary roots. A robust implementation should inspect the moment residual, weight distribution, and parameter-boundary behavior, not merely accept optimizer convergence.

## Trivariate tobit experiment and unresolved reporting limits

The latent response is $Y_j^*=x_j\beta+\epsilon_j$, $j=1,2,3$, with common $\beta=1$ and

$$
\Omega=\begin{pmatrix}2&0.7&0\\0.7&1&0\\0&0&1\end{pmatrix}.
$$

Covariates are independent across observations and jointly normal with mean $(1,1,1)'$ and covariance $2I_3$. Observed outcomes are $Y_j=\max(Y_j^*,0)$. The source starts by describing an earlier 500-observation multinomial design, but explicitly says its Table 5 uses a single dataset of 50 observations. The distinction should be preserved rather than silently treating 500 as the tobit sample size.

Conditional latent draws are obtained by a truncated-normal Gibbs sampler run for 10 cycles. Parameters are updated through iterated generalized least squares in a simulated EM procedure. There are 100 simulation experiments on the fixed dataset, with $R=1$ and $R=5$ draws per observation, independent across observations.

At $R=1$, the difference between simulated and exact MLE has mean −0.0044, standard deviation 0.0189, median −0.0036, and quartiles −0.0170/0.0080. At $R=5$, the corresponding values are −0.0060, 0.0084, −0.0058, and −0.0121/0.0002. The variance ratio $(0.0189/0.0084)^2=5.06$ is consistent with a substantial $1/R$ simulation-noise component. These are simulation differences conditional on one dataset, not the full repeated-sample estimator distribution.

The source reports an approximate MLE sampling standard deviation of 0.0331 and says $R=1$ increases it by 50%. That claim does not follow from the table. Adding independent first-order variances gives $\sqrt{0.0331^2+0.0189^2}=0.0381$, about a 15% increase; for $R=5$ it gives 0.0341, about 3.2%. This is a diagnostic arithmetic reconstruction under the orthogonality approximation, not a replacement experiment. The paper supplies no additional covariance calculation explaining its 50% statement.

Ten Gibbs cycles do not establish exact sampling from the conditional distribution. The source does not report initialization, convergence diagnostics, thinning, seeds, iterative stopping rules, or full covariance-parameter update details. It reports little bias relative to the MLE and argues conditional simulation is efficient in this less-censored setting, but it provides no Monte Carlo standard errors or formal significance test supporting every verbal comparison. Exact numerical reproduction therefore requires implementation choices beyond the article.

The practical lesson is specific: center a computational approximation when its mean is wrong, preserve independence where a residual–weight orthogonality argument requires it, measure the noise introduced by the correction, and inspect rare-event and boundary behavior. Consistency is a minimum requirement. A simulator that satisfies it can still be too noisy, unstable, or costly to use effectively.
