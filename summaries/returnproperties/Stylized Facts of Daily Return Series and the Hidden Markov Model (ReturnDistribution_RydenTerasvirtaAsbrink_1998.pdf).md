# Stylized Facts of Daily Return Series and the Hidden Markov Model

**Tobias Rydén, Timo Teräsvirta, and Stefan Åsbrink (1998).** *Journal of Applied Econometrics* 13, 217–244. Source: [ReturnDistribution_RydenTerasvirtaAsbrink_1998.pdf](../../Finance/ReturnDistribution_RydenTerasvirtaAsbrink_1998.pdf). The full scanned 28-page article was read using OCR and direct inspection of its model equations, tables, figures, and spectral-density appendix. Page references below use journal pagination.

## Why this matters

A small Gaussian hidden Markov model can generate returns with negligible linear predictability, persistent absolute returns, non-Gaussian unconditional distributions, and a Taylor effect. These features do not require an exponentially distributed absolute return or a continuously evolving latent volatility process. The paper makes that alternative concrete through analytical moment and autocovariance formulas, maximum-likelihood estimation, bootstrap selection of the number of regimes, and an extensive subsample experiment on the S&P 500.

Its most useful result is qualified. Two or three volatility states reproduce many distributional properties, especially after outlier reduction, but generally fail to reproduce the very slow decay of absolute-return autocorrelations. Exceptional observations can also absorb an entire regime, making estimated states unstable across subsamples. A fitted “high-volatility regime” may therefore be a device for accommodating a few observations rather than a stable economic state.

The contribution is an empirical and statistical modeling cycle, not the invention of the hidden Markov model. It differs from applications that choose two regimes in advance: the authors explicitly confront the nonstandard state-number testing problem and evaluate whether fitted models reproduce the properties that motivated them. There is no out-of-sample investment strategy or claim of profitable return direction prediction.

## The empirical targets

The starting point is a collection of properties identified in earlier work by Granger and Ding. Four concern temporal dependence: little autocorrelation in signed returns, slowly declining positive dependence in absolute and squared returns, strongest transformed-return dependence near the first absolute power, and little dependence in return signs. Three concern distributions: independence between sign and magnitude, approximate equality of the mean and standard deviation of absolute returns, and an approximately exponential absolute-return distribution after outlier reduction.

An exponential nonnegative variable has mean equal to standard deviation, skewness two, and non-excess kurtosis nine. These moment properties are the benchmarks labeled PED1–PED3 in the article. The paper does not assume they hold exactly in each S&P subsample; it asks whether fitted mixtures can approximate them.

A two-normal zero-mean mixture provides an instructive preliminary calculation. Normalize one standard deviation to one, let the other be $s$, and assign stationary weight $a$ to the first. Then, for $q> -1$,

$$
E|r|^q=c_q[a+(1-a)s^q],
\qquad c_q=\frac{2^{q/2}\Gamma((q+1)/2)}{\sqrt\pi}.
$$

Central moments of $|r|$ follow from these raw moments. Figures 1–3 vary mixture weight and relative scale. When $s$ is around 2.5 and the low-scale component has weight roughly 0.7–0.9, the three exponential benchmarks can be approximated jointly, allowing some deviation in the mean/standard-deviation ratio. The point is an existence argument about overlapping moment restrictions, not an estimate that all market returns have those parameter values.

A finite Gaussian mixture still has Gaussian-dominated asymptotic tails and all positive moments finite. Matching exponential-like central behavior, skewness, or kurtosis over a finite sample does not make its exact distribution exponential, regularly varying, or genuinely power-tailed. This distinction is important when taking the fitted model beyond the observed return range.

## Model definition and probabilistic structure

Let $S_t\in\{1,\ldots,d\}$ be a first-order Markov chain with row-stochastic transition matrix $P$, where $P_{ij}=P(S_t=j\mid S_{t-1}=i)$. Conditional on the state sequence, returns are independent with

$$
r_t=\sigma_{S_t}\epsilon_t,\qquad \epsilon_t\overset{iid}\sim N(0,1),
$$

and the innovation sequence is independent of the chain. Each $\sigma_i>0$ is constant within the fitted subsample. The state means are fixed at zero; there are no regime-specific return means, autoregressive return coefficients, or transition probabilities depending on observed predictors.

Assume the chain is ergodic. Its stationary row vector $a$ satisfies $aP=a$ and $a\mathbf1=1$, and $P^k\to\mathbf1a$. For two states,

$$
a_1=\frac{1-P_{22}}{2-P_{11}-P_{22}},\qquad
 a_2=\frac{1-P_{11}}{2-P_{11}-P_{22}}.
$$

The unconditional return distribution is the mixture $\sum_i a_iN(0,\sigma_i^2)$. Zero emission means make signed returns uncorrelated at every nonzero lag even when the state process is persistent. Symmetric Gaussian emissions also make signs independent of magnitudes and independent across time under this construction. These features are imposed by the model, not discoveries extracted from its fitted transition probabilities.

Volatility persistence arises because nearby states are dependent. High-volatility observations increase the filtered probability of a high-scale state, and persistent transitions make subsequent magnitudes more likely to be large. The model has no asymmetric response to positive versus negative innovations of equal magnitude. It therefore does not encode an equity leverage effect without an extension.

Expected duration in state $i$ is $1/(1-P_{ii})$ observations when $P_{ii}<1$. This is a geometric duration distribution. A large diagonal entry is not sufficient to make a state empirically important: its stationary entry probability and occupancy can be extremely small. Both persistence and occupancy should be reported when interpreting regimes.

## Exact moments and autocorrelations

For any transform $g$ with adequate moments, define $G_i=E[g(r_t)\mid S_t=i]$ and $G=\operatorname{diag}(G_1,\ldots,G_d)$. Equations (5)–(8) give

$$
E[g(r_t)]=aG\mathbf1,
$$

$$
\operatorname{Cov}(g(r_t),g(r_{t+k}))
=aGP^kG\mathbf1-(aG\mathbf1)^2,\qquad k\ge1.
$$

At lag zero the second conditional moments must be used separately; substituting $k=0$ into the positive-lag expression would omit within-state emission variance. For $g(r)=|r|^q$, set $G_i=c_q\sigma_i^q$ and calculate

$$
\operatorname{Var}(|r|^q)=c_{2q}\sum_i a_i\sigma_i^{2q}
-\left(c_q\sum_i a_i\sigma_i^q\right)^2.
$$

Dividing the positive-lag covariance by this variance gives the model ACF. Thus the Taylor-effect exercise needs no long Monte Carlo simulation: a fitted $P$ and vector of scales determine the entire grid of transformed autocorrelations analytically.

For a two-state chain the nonunit eigenvalue is $\lambda=P_{11}+P_{22}-1$. In that case the positive-lag covariance of any transform is proportional to $\lambda^k$, with an amplitude depending on the difference between state-conditional transformed means. This deduction explains both the flexibility and limitation of the model. State persistence and scale separation can generate sizable magnitude dependence, but a finite-state ergodic chain does not produce genuine hyperbolic long memory. With more states, several exponential modes, and potentially polynomial factors from nontrivial Jordan blocks, remain exponentially bounded.

Near-unit eigenvalues can approximate slow decay over a finite window, but this does not guarantee that maximum likelihood will select the near-unit transitions needed to fit the observed ACF. The likelihood must simultaneously fit the entire distribution and temporal pattern, and the paper finds that those demands can conflict.

## Likelihood evaluation and estimation

For a fixed number of states $d$, the free parameter count is $d(d-1)$ transition probabilities plus $d$ variances, or $d^2$ in total. Let

$$
F_t=\operatorname{diag}\{f(r_t;\sigma_1^2),\ldots,f(r_t;\sigma_d^2)\},
$$

where $f$ is the zero-mean Gaussian density. With stationary initialization, equation (10) is

$$
L(\theta;r_{1:n})=aF_1PF_2\cdots PF_n\mathbf1.
$$

The matrix product sums over every hidden-state path without enumerating $d^n$ sequences. Evaluation is linear in sample length for fixed $d$, with standard dense operations of order $nd^2$. A numerical implementation should scale the forward probabilities at every step to avoid underflow:

1. Start with the predicted row vector $q_1=a$.
2. Form $c_t=q_tF_t\mathbf1$ and add $\log c_t$ to the log likelihood.
3. Normalize $\alpha_t=q_tF_t/c_t$.
4. Set $q_{t+1}=\alpha_tP$ and continue.

These scaled equations are an implementation of the reported likelihood, not a different estimator. A one-step predictive variance, if needed later, is $q_{t+1}(\sigma_1^2,\ldots,\sigma_d^2)'$. The original experiment does not evaluate that forecast out of sample.

The authors use downhill simplex optimization, with 200 random starting points for two states and 500 for three states. This is intended to reduce the chance of retaining a local maximum. State labels can be permuted without changing the likelihood; reported regimes are sorted by increasing standard deviation. Constraints must enforce nonnegative transition probabilities, row sums one, and positive variances. The paper does not state the random-start distribution, numerical parameterization, exact tolerance, variance floors, or random seed values.

Fixing all means at zero prevents the usual unrestricted Gaussian-mixture singularity in which a component mean is placed on one observation and its variance collapses. The source explicitly retains an exception when an observation is exactly zero. Demeaning and finite precision can make this relevant. A production implementation should detect it and disclose any positive variance floor rather than quietly changing the likelihood.

Random multistarts reduce risk but do not prove a global optimum. That limitation becomes visible in the empirical results: some fitted three-state likelihoods are lower than their nested two-state counterparts. A mathematically correct global maximization could not produce a negative likelihood-ratio statistic for nested classes.

## Selecting the number of states

State-number inference is nonregular. If two states have identical emissions or a state disappears, transition parameters become unidentified under the smaller model. A usual chi-squared likelihood-ratio reference distribution with the difference in parameter counts is therefore inappropriate.

The article discusses penalized likelihood, maximizing $\log L(\widehat\theta_d)-w_{n,d}$. AIC corresponds to $w_{n,d}=d^2$, and BIC to $w_{n,d}=\tfrac12d^2\log n$ in this maximization convention. These penalties can be viewed as LR thresholds between adjacent state counts, but they do not provide a conventional known test size under the unidentified null.

The chosen approach is a parametric $m$-out-of-$n$ bootstrap. Fit the null model on $n$ observations, simulate shorter samples of length $m$ from that fitted model, refit both null and alternative to each simulated sample, and compute the LR statistic. The asymptotic rationale uses $m/n\to0$ to reduce the smoothness requirements involved in bootstrapping the nonstandard statistic.

The empirical settings are $n=1,700$, $m=800$, and $K=50$ bootstrap replications. If $k$ simulated LR values exceed the observed value, the reported p-value is

$$
\widehat p=\frac{k+1}{K+1}.
$$

Its smallest possible value is $1/51\approx0.0196$, printed as 0.02. These are not accurately measured tiny tail probabilities; the bootstrap is coarse. With only 50 replications, decisions near 5% are sensitive to a few simulated outcomes.

Section 4.2 explicitly describes comparing with an observed LR computed from $m$ observations. The subsequent subsample description gives the 1,700-observation fits and 800-observation bootstrap setting, but does not fully specify which 800 observations form the corresponding observed statistic. Exact replication requires resolving that indexing choice. It would be incorrect to silently compare an $n$-sample statistic with an $m$-sample reference distribution while claiming literal reproduction of the procedure.

The sequence tests one against two states, then two against three. Three against four is not attempted because of computational cost. Thus “three states selected” means that two is rejected within the explored sequence, not that three is proven optimal among all state counts.

## Spectral model evaluation

The Gaussian innovations cannot be reconstructed exactly because the state path is unobserved, even with known parameters. The authors therefore do not apply ordinary residual portmanteau tests as if regime classifications were error-free. They evaluate the spectrum of demeaned absolute returns using Milhøj’s goodness-of-fit statistic.

Let $X_t=|r_t|$, $M_1=\operatorname{diag}(E[X_t\mid S_t=i])$, $M_2=\operatorname{diag}(E[X_t^2\mid S_t=i])$, and $B=P-\mathbf1a$. The appendix derives

$$
2\pi g(\omega)=aM_2\mathbf1-(aM_1\mathbf1)^2
+2aM_1(B\cos\omega-B^2)(I-2B\cos\omega+B^2)^{-1}M_1\mathbf1.
$$

For Gaussian emissions, $M_{1,ii}=\sqrt{2/\pi}\sigma_i$ and $M_{2,ii}=\sigma_i^2$. The proof uses $P^k-\mathbf1a=B^k$, spectral radius below one, and summation of the matrix geometric series for positive and negative autocovariances. It supplies a directly computable spectral density without simulation.

For Fourier frequencies $\omega_j=2\pi j/n$, define $z_j=I(\omega_j)/g(\widehat\theta,\omega_j)$. The statistic in equation (12) is

$$
W=\frac{(2\pi/n)\sum_{j=1}^{n-1}z_j^2}
{[(2\pi/n)\sum_{j=1}^{n-1}z_j]^2}.
$$

A common normalization of the periodogram cancels from this ratio. Large $W$ indicates poor spectral fit. Apply it to $|r_t|-\overline{|r|}$, not raw signed returns whose flat spectrum is largely built into the model.

The reference distribution is again approximated parametrically with 50 replications, now of full sample length $m=n$. The authors acknowledge that a completely formal justification for their HMM application is lacking and that the test can have low power. Reducing bootstrap length here would further weaken an already weak diagnostic. Nonrejection should consequently not be read as a certificate that the model reproduces all dependence or its entire conditional distribution.

## Dataset and preprocessing

The S&P 500 series contains 17,055 daily observations from 3 January 1928 through 30 April 1991 and was supplied by William Schwert. The first 55 observations are omitted; the remaining 17,000 are split chronologically into ten consecutive, nonoverlapping blocks of 1,700, labeled A through J. Each block is demeaned separately before fitting.

The article defines returns as first differences of logarithmed prices or the price index. It does not give a complete modern data-vendor specification, dividend adjustment rule, exact date boundaries for all ten blocks, or a treatment of historical trading-calendar differences. Reconstruct the original observation sequence before matching block indices; replacing it with a different contemporary “S&P 500” history may change both values and dates.

A second experiment clips each block’s returns to its own mean plus or minus four estimated standard deviations. This is winsorization: observations outside the interval are replaced by the endpoint, not removed. It is performed separately by block, whereas the comparison literature used a threshold estimated across the full series. The distinction affects how many early and late observations are altered.

Both the raw and clipped series are fitted and evaluated. Clipping is an analytical sensitivity exercise, not a claim that crash observations are mistakes. Since sample mean and scale use the full block, this design is retrospective and cannot be represented as a real-time trading procedure. There is no holdout period, transaction-cost model, rebalancing rule, or portfolio construction in the experiment.

## State selection and representative parameter estimates

All ten blocks reject the single-state model at the bootstrap’s minimum reported p-value of 0.02, both before and after clipping. For the raw data, E, F, and H do not reject two states against three: p-values are 0.25, 0.43, and 0.39. The remaining blocks select three within the tested sequence.

After clipping, E has p-value 0.57. F and H produce slightly negative fitted LR values, approximately −0.031 and −0.12, despite 500 starts, and are retained as two-state cases. These values reveal incomplete numerical maximization; they are not valid negative evidence against adding states. B is borderline, with reported p-value 0.04, and is retained as three-state. Removing the influence of the October 1987 crash does not reduce J to two states under this procedure.

The two-state estimates from Table VII are particularly reproducible:

| Block | $P_{11}$ | $P_{22}$ | $\sigma_1$ | $\sigma_2$ | Stationary low-state weight |
|---|---:|---:|---:|---:|---:|
| E | 0.964 | 0.892 | 0.0049 | 0.0109 | 0.750 |
| F | 0.987 | 0.902 | 0.0049 | 0.0139 | 0.884 |
| H | 0.995 | 0.989 | 0.0063 | 0.0126 | 0.691 |

The off-diagonal entries are the complements of the diagonal entries. Standard deviations are in decimal daily log-return units: 0.0049 is about 0.49% per day. From the rounded transition estimates, E’s expected durations are about 27.8 and 9.3 observations, F’s about 76.9 and 10.2, and H’s about 200 and 90.9. These duration calculations are implications of the fitted model, not additional source estimates.

Clipped estimates in Table VIII are E: diagonals 0.963 and 0.931, scales 0.0046 and 0.0092, low-state weight 0.648; F: 0.985 and 0.930, scales 0.0047 and 0.0107, weight 0.822; H: 0.995 and 0.989, scales 0.0062 and 0.0124, weight 0.686. These relatively stable examples contrast with more fragile three-state fits.

Raw block G has

$$
P_G=\begin{pmatrix}.970&.029&.001\\.043&.955&.002\\.361&.332&.307\end{pmatrix},
\qquad \sigma_G=(.0039,.0087,.2372),
$$

with stationary weights approximately $(.600,.399,.001)$. The third standard deviation, 23.72% in daily decimal-return units, is extraordinary; the regime is visited extremely rarely and lasts only about 1.44 observations on average. This fitted tail component badly distorts unconditional higher moments even though the sample block itself does not have comparably extreme absolute-return kurtosis.

After clipping, G becomes

$$
P_G^{clip}=\begin{pmatrix}.953&.029&.018\\.416&.340&.244\\.057&.000&.943\end{pmatrix},
\qquad \sigma_G^{clip}=(.0040,.0068,.0090),
$$

with weights $(.647,.029,.324)$. It now has persistent low and high regimes and an infrequent intermediate regime. The same nominal state count thus represents a very different stochastic mechanism after modest-looking preprocessing.

Raw block J has scales $(.0078,.0150,.0745)$ and weights $(.861,.133,.006)$. Its highest-scale state has $P_{33}=.223$. After clipping, the scales become $(.0060,.0115,.0190)$ and weights $(.613,.293,.094)$, with $P_{33}=.944$. These figures demonstrate why comparing only the number of states conceals changes in regime meaning.

All displayed matrices are rounded source estimates. Rows can differ slightly from one through rounding; simulations should either use the original full-precision fit or explicitly renormalize rounded rows. That adjustment changes the implied stationary vector slightly and should not be mistaken for disagreement with the published estimates.

## Goodness of fit, Taylor effects, and failure of long persistence

For raw three-state fits, the spectral test rejects A at approximately 0.04 and G at 0.02; C is borderline at 0.10. The remaining tested three-state fits have larger p-values. After clipping, G still fails, while the others in the corresponding table do not reject at 5%. Testing two-state models directly can also fail to reject cases for which the LR test prefers three states. The authors interpret this discrepancy partly as low power of the broad goodness-of-fit test.

Tables I and IV compare mean/standard-deviation ratios, skewness, and non-excess kurtosis of absolute returns with their analytical mixture counterparts. Broadly, fitted models reproduce lower versus higher skewness and kurtosis across blocks, with raw G a conspicuous failure. Clipping materially improves agreement. This supports a flexible mixture explanation of central and higher-moment properties but does not establish stability of the mixture as a structural law.

Figure 4 compares empirical and fitted absolute-return ACFs over the first 50 lags. Fitted decay is usually faster, especially for C, D, and G. The same broad limitation remains after clipping. The model can be highly persistent, but maximum-likelihood fits that accommodate the marginal distribution do not satisfactorily reproduce the full slow-decay pattern.

The Taylor-effect exercise evaluates $q=0.2,0.4,\ldots,2.0$ and selects the exponent maximizing lag-one autocorrelation. In the raw data the maximizing exponents for A–J are $(1.4,1.4,1.4,1.0,1.2,1.6,1.4,1.2,1.8,1.2)$; fitted-model values are $(1.0,1.4,1.4,1.6,1.2,1.4,0.8,1.2,1.4,1.0)$, as Table XIII records.

After clipping, the empirical maxima are $(1.6,1.6,2.0,1.4,1.4,2.0,1.8,1.4,2.0,2.0)$ and model maxima are $(0.8,0.8,1.4,1.4,1.2,1.4,1.0,1.2,1.6,1.8)$. Thus a ridge below power two is common in the models, but “the maximum is exactly at one” is too strong. Clipping weakens the empirical effect, moving several maxima to the upper boundary of the tested grid. A boundary maximum at two does not establish that two is optimal over all possible exponents.

### Numerical moment discrepancies behind the diagnosis

The moment comparisons are more informative than an overall statement that Gaussian mixtures fit well. In raw block G, Table I reports an empirical absolute-return mean/standard-deviation ratio of 1.04, skewness 2.25, and kurtosis 12.4. Its fitted HMM instead implies 0.49, 30.93, and 1,357. These are population moments of the fitted finite mixture, not Monte Carlo noise. The rarely occupied scale of 0.2372 dominates the high powers in the moment formulas even though its stationary weight is only about 0.001.

For raw J, empirical skewness and kurtosis are 9.99 and 208, while the model gives 7.26 and 117. The model captures the direction of unusually heavy sample tails but materially understates their magnitudes. For raw E, empirical kurtosis is 27.1 and fitted kurtosis is 8.23 despite a reasonable mean/standard-deviation comparison, 1.04 versus 1.10. Agreement in one low-order ratio therefore does not establish agreement in the fourth moment.

After clipping, G's empirical ratio, skewness, and kurtosis become 1.07, 1.83, and 7.29; fitted values are 1.09, 1.80, and 7.30. J similarly improves to empirical skewness 2.18 and kurtosis 10.2 versus model values 2.14 and 9.97. These comparisons explain why the paper regards the distributional fit as much improved after outlier reduction, while the persistent failure of G's spectral test shows that marginal improvement does not repair all temporal structure.

To reproduce these statistics without simulation, write the first four raw absolute-return moments as $m_j=c_j\sum_i a_i\sigma_i^j$. Then the centered quantities are

$$
\mu_2=m_2-m_1^2,\quad
\mu_3=m_3-3m_1m_2+2m_1^3,\quad
\mu_4=m_4-4m_1m_3+6m_1^2m_2-3m_1^4.
$$

The reported ratio is $m_1/\sqrt{\mu_2}$, skewness is $\mu_3/\mu_2^{3/2}$, and kurtosis is $\mu_4/\mu_2^2$. No subtraction of three is made for these kurtosis comparisons. Confusing this convention with excess kurtosis would shift every fourth-moment benchmark, including the exponential target of nine. Full-precision transition and scale estimates are especially important in the outlier regimes because high powers amplify rounding errors.

## Reimplementation boundary and takeaways

The model, likelihood, transformed moments, ACF, spectrum, clipping rule, state-selection sequence, sample lengths, and bootstrap counts are reconstructible from the source. Exact table reproduction additionally needs the original return vector, block-to-date mapping, observed 800-point LR subset choice, optimizer parameterization and starts, bootstrap refitting conventions, and full-precision estimates. The PDF does not provide those items completely.

For a fresh implementation, the natural checks are that forward probabilities sum to one, row transitions are valid, stationary probabilities solve $aP=a$, likelihood is invariant to state relabeling, and every fitted larger model achieves at least the embedded smaller model’s likelihood. Analytical moments and ACFs can then be checked against long simulations using the fitted parameters. These are implementation checks implied by the mathematics, not further experiments reported in the paper.

The results support finite-state Gaussian scale mixtures as a parsimonious benchmark for return magnitudes and distributional shape. They also identify a concrete limitation: an attractive likelihood and plausible marginal moments can coexist with incorrect persistence and unstable rare states. For risk simulation or forecasting, inspect the transition dynamics and the outlier sensitivity before assigning economic meaning to a regime or using its tail behavior beyond the observed sample.
