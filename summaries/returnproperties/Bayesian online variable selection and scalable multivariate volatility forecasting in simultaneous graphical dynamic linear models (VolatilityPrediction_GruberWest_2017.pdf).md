# Bayesian online variable selection and scalable multivariate volatility forecasting in simultaneous graphical dynamic linear models

**Authors:** Lutz F. Gruber and Mike West. **Publication:** Econometrics and Statistics 3 (2017), 3–22, DOI 10.1016/j.ecosta.2017.03.003. **Source:** [VolatilityPrediction_GruberWest_2017.pdf](../../Finance/VolatilityPrediction_GruberWest_2017.pdf), 20 PDF pages including Appendices A–C. Printed page numbers equal PDF page numbers plus two. This is the adaptive variable-selection extension of the earlier SGDLM work, not a duplicate of the library's note on the original model.

## Why this matters and the specific innovation

A covariance forecast for hundreds of assets must adapt quickly without fitting a fully unconstrained dynamic system from scratch every day. Simultaneous graphical dynamic linear models address the dimensionality problem by giving each return series a small set of contemporaneous predictors, estimating local models largely in parallel, and recoupling them into a coherent joint forecast. The present paper's main addition is a sequential mechanism for changing those predictor sets. Candidates enter a warm-up group, accumulate evidence, compete for a core position, and leave gradually if rejected or displaced.

This is decision-oriented model selection. The goal is a useful covariance and predictive-return distribution, not identifying one uniquely true economic network. Highly correlated stocks can substitute for one another as parents. A selected edge is neither a causal relationship nor a statistically isolated structural channel. The method avoids an exhaustive search over graphs by distributing proposal, learning, acceptance, and retirement across successive filtering dates.

The case study models 400 stocks plus the S&P 500 index. Forecast distributions feed daily minimum-variance and target-return portfolios, some constrained to be forecast-uncorrelated with the index. The authors also use a by-product of approximate Bayesian filtering as a market-stress indicator. Reported portfolio improvements are substantial within the study, but exact replication encounters several unresolved implementation details, including an internally incomplete turnover rule. The methodology should be separated from those empirical and operational limitations.

## Simultaneous model and covariance construction

For series $j=1,\ldots,m$, write

$$
y_{jt}=x_{jt}'\phi_{jt}+y_{sp_t(j),t}'\gamma_{jt}+\nu_{jt},
\qquad \nu_{jt}\mid\lambda_{jt}\sim N(0,\lambda_{jt}^{-1}).
$$

The external predictors $x_{jt}$ are known at the forecast origin. The parental set $sp_t(j)$ contains a subset of the other contemporaneous series and excludes $j$. Stack the local regression coefficients as $\theta_{jt}=(\phi_{jt}',\gamma_{jt}')'$ and, when updating after observing date $t$, use $F_{jt}=(x_{jt}',y_{sp_t(j),t}')'$. Conditional observation errors are independent across series and dates. Dependence in observed returns arises through simultaneous equations, not correlated local residuals.

Let $\Gamma_t$ contain the parental coefficients in their appropriate rows, with zeros elsewhere, and let $\Lambda_t=\operatorname{diag}(\lambda_{1t},\ldots,\lambda_{mt})$. Put $\mu_{jt}=x_{jt}'\phi_{jt}$ and $A_t=(I-\Gamma_t)^{-1}$. Conditional on states and precisions,

$$
y_t\sim N(A_t\mu_t,\Sigma_t),\qquad
\Sigma_t=A_t\Lambda_t^{-1}A_t',
$$

$$
\Omega_t=\Sigma_t^{-1}=(I-\Gamma_t)'\Lambda_t(I-\Gamma_t).
$$

A forecast must solve the simultaneous system. Substituting future observed parent returns into independent regressions would leak information. Parental sparsity reduces local state dimensions, though zeros in $\Gamma$ do not translate one-for-one into zeros in $\Omega$: shared children and indirect simultaneous links can generate additional precision entries. Positive local precisions and nonsingularity of $I-\Gamma$ produce a positive-definite conditional covariance. The source does not specify a conditioning threshold or rejection rule for nearly singular simulation draws.

At each forecast origin, draw the local parameter/precision states from their prior, construct $A_t\mu_t$ and $\Sigma_t$, then simulate the joint normal return if needed. Predictive moments can also be calculated by averaging conditional moments:

$$
p_t=E(A_t\mu_t\mid D_{t-1}),
$$

$$
P_t=E(\Sigma_t\mid D_{t-1})+
\operatorname{Var}(A_t\mu_t\mid D_{t-1}).
$$

The second term includes state and parameter uncertainty. Averaging only conditional covariance matrices would omit it. Multi-step forecasting repeatedly simulates state evolution and returns rather than treating future parent values as known regressors.

## Normal-gamma filtering and discount evolution

The local prior has the source's normal-gamma parameterization

$$
(\theta_{jt},\lambda_{jt}\mid D_{t-1})\sim NG(a_{jt},R_{jt},r_{jt},s_{j,t-1}),
$$

meaning

$$
\lambda_{jt}\sim\operatorname{Gamma}\left(\frac{r_{jt}}2,\frac{r_{jt}s_{j,t-1}}2\right),
\qquad
\theta_{jt}\mid\lambda_{jt}\sim N\left(a_{jt},\frac{R_{jt}}{s_{j,t-1}\lambda_{jt}}\right).
$$

Gamma's second parameter is a rate. In particular $E\lambda=1/s$, while the marginal Student state distribution has degrees of freedom $r$, center $a$, and scale matrix $R$. A scale matrix is not the covariance: when $r>2$, the latter is $rR/(r-2)$.

After observing the whole return vector, the provisional univariate update is analytic. Suppress $j,t$ where unambiguous and define

$$
e=y-F'a,\quad q=s+F'RF,\quad K=RF/q,
\quad z=\frac{r+e^2/q}{r+1}.
$$

Then

$$
\widetilde m=a+Ke,\qquad
\widetilde C=(R-KK'q)z,\qquad
\widetilde n=r+1,\qquad \widetilde s=zs.
$$

These updates treat the observed parent values as regressors for local conditioning. They are not yet the correct joint posterior because the observation system has a Jacobian. The exact posterior within the current prior approximation is

$$
p(\Theta_t,\Lambda_t\mid D_t)
\propto |\det(I-\Gamma_t)|\prod_{j=1}^m
\widetilde p_{jt}(\theta_{jt},\lambda_{jt}\mid D_t).
$$

Sample independently from the provisional normal-gamma factors, compute each sample's absolute determinant, and normalize those determinants into importance weights. The weighting recouples the local posterior samples. Dropping it would fit a product of regressions rather than the specified simultaneous joint model. The absolute determinant should be evaluated stably, for example through sign and log determinant rather than multiplying pivots without scaling; that numerical advice is an implementation implication, not a reported author setting.

For efficient evolution, project the recoupled posterior back onto a product of local normal-gamma forms. Appendix B gives explicit weighted-expectation formulas. For a local state dimension $p_j$, define

$$
m_j=\frac{E(\lambda_j\theta_j)}{E\lambda_j},\qquad
V_j=E\{\lambda_j(\theta_j-m_j)(\theta_j-m_j)'\},
$$

$$
d_j=E\{\lambda_j(\theta_j-m_j)'V_j^{-1}(\theta_j-m_j)\}.
$$

Solve numerically for positive $n_j$ satisfying

$$
\log(n_j+p_j-d_j)-\psi(n_j/2)-\frac{p_j-d_j}{n_j}
-\log(2E\lambda_j)+E\log\lambda_j=0,
$$

then set

$$
s_j=\frac{n_j+p_j-d_j}{n_jE\lambda_j},\qquad C_j=s_jV_j.
$$

All expectations use the recoupled importance sample. The source describes this as variational-Bayes decoupling by KL minimization. For reproduction the displayed moment equations are the decisive specification, rather than assuming that an arbitrary software package's default KL direction implements the same projection. With exact nonsingular moments, $d_j=p_j$ by the trace identity; keeping the printed form is useful for matching its numerical implementation.

The next prior evolves through

$$
a_{j,t+1}=G_{j,t+1}m_{jt},\quad
R_{j,t+1}=G_{j,t+1}C_{jt}G_{j,t+1}'+W_{j,t+1},
\quad r_{j,t+1}=\beta_jn_{jt}.
$$

The scale $s_{jt}$ is carried into the next precision prior. The volatility discount $\beta_j$ lowers information about precision without shifting its mean. Away from retirement interventions, $G=I$. Local external coefficients and parental coefficients have separate discount factors $\delta_{j\phi}$ and $\delta_{j\gamma}$. If $B=GCG'$, the evolved covariance blocks are

$$
R_{\phi\phi}=B_{\phi\phi}/\delta_{j\phi},\qquad
R_{\gamma\gamma}=B_{\gamma\gamma}/\delta_{j\gamma},\qquad
R_{\phi\gamma}=B_{\phi\gamma}/\sqrt{\delta_{j\phi}\delta_{j\gamma}}.
$$

This is equivalent to the source's block formula for $W=R-B$. It preserves cross-block uncertainty consistently rather than discounting only the diagonal blocks. Smaller discounts inject more state uncertainty and increase adaptation; larger values make fitted parent relationships persistent.

## The new parental-selection algorithm

The case study partitions each series' parents into a core group of target size 20, a warm-up group of size 10, and a retirement group of size 10. A candidate receives ten filtering steps before its formal competition with incumbent core predictors. These are user-specified capacities, not posterior estimates of the true graph size. At most about forty parental effects plus the external predictor state are active for a series during transition.

A parallel unconstrained Wishart DLM proposes candidates. Its state discount is 0.95 and covariance discount 0.8, deliberately making it responsive to changing dependence. At each date and for each row $j$, inspect the ten largest absolute off-diagonal precision entries. Among these, select the strongest series absent from the current core and warm-up sets. Introduce it with zero prior coefficient mean and a specified prior variance. The source does not give that variance numerically or fully specify what happens when no eligible candidate exists, ties occur, or a proposed name is already in retirement.

The proposal uses precision entries because, in a joint Gaussian model, the conditional coefficient for series $k$ in the regression for $j$ is $-\Omega_{jk}/\Omega_{jj}$. Within a fixed row, ranking absolute off-diagonal entries is equivalent to ranking the magnitudes of these coefficients. This is not the same as ranking marginal correlations or standardized partial correlations, and may depend on asset return scaling across candidates.

Once introduced, the candidate participates in ordinary joint filtering during ten subsequent observations. It then enters the core provisionally. If this makes the core too large, compare its evidence with incumbent evidence and send the least useful coefficient to retirement. The source defines the score as

$$
SNR_{kjt}=|a_{kjt}|/R_{kkjt}.
$$

That is the formula visible in Section 3.3.3: denominator $R_{kkjt}$, without a square root. Since $R$ was defined as a Student scale matrix, this is not the usual standardized coefficient divided by its standard deviation. The text also calls these posterior values while using prior-symbol notation. A reproducer should confirm the implemented score and timing rather than silently substitute $|a|/\sqrt R$; that change can alter which parent is dropped. The methodological idea survives this ambiguity, but exact graph paths do not.

Retirement avoids an abrupt covariance jump. If a coefficient enters the outgoing group at $t_0$, the corresponding diagonal state-transition element becomes

$$
G_{k,j,t_0+l}=1-\frac1{(\Delta+1)-l},\qquad l=1,\ldots,\Delta,
$$

with $\Delta=10$. Without intervening updates, the product of the first $l$ multipliers is $(\Delta-l)/\Delta$, so the deterministic mean contribution falls linearly to zero. The last multiplier is zero. Filtering meanwhile allows other coefficients to absorb the retiring parent's role. The coefficient can be removed after it has been driven to zero. Initial group construction, covariance expansion for new coefficients, and any special handling of degenerate outgoing covariance blocks require implementation details beyond those printed.

This is not Metropolis–Hastings sampling from a posterior over graph structures. The analogy is proposal followed by delayed evaluation; acceptance is a decision rule, not a detailed-balance probability. It produces one evolving predictive structure, and its selected-edge frequencies should not be interpreted as Bayesian inclusion probabilities from a fully integrated model-space posterior.

## Data, timing, and model settings

The dataset contains SPX plus 400 S&P 500 member stocks continuously listed since 2002. Section 5.1 says data run through the third quarter of 2013, with daily close-to-close log returns; portfolio evaluation is January 2003–September 2013. Introductory and stress-index passages mention 2014, but the explicit data section and performance tables identify the 2003–2013 experiment. The continuous-listing screen conditions on survival and is not a point-in-time changing-index universe.

The PDF does not supply a complete ticker list, price vendor, split/dividend adjustment convention, exact first and last sessions, missing-price treatment, or every initial state hyperparameter. The 2002 history precedes the investment evaluation but a complete initialization recipe is not printed. These omissions matter in reproducing both returns and rapidly evolving covariance states.

Ten SGDLM variants are studied. Models M1–M5 use a local intercept for the external component. Models MA1–MA5 also include the mean of the preceding five one-step forecast errors:

$$
x_{jt}^{err}=\frac15\sum_{k=1}^5(y_{j,t-k}-f_{j,t-k}),
$$

where $f_{j,s}$ was computed using information through $s-1$. This is a lagged error correction predictor, not an average of five future residuals or five raw returns. The contemporaneous parent terms remain in both model families; the source's simplified notation $F=1$ refers to the external component, not removal of the parent model.

All variants use $\beta_j=0.95$ and $\delta_{j\phi}=0.995$. The parental discount rises from 0.995 to 0.999 in increments of 0.001 across M1–M5 and MA1–MA5. These values follow preliminary performance evaluation and qualitative assessment; the paper does not identify an independent untouched hyperparameter-selection sample. Reported practical recommendations favor 0.995–0.997 because larger discounts slow parent turnover.

The forecasting loop is sequential: update on date $t-1$ returns, generate the date $t$ predictive distribution, choose weights, then observe date $t$. Trading is assumed possible at the same closing prices used in the update. That idealized timing leaves no delay for data availability, filtering, optimization, or order execution. It should not be treated as a demonstrated executable closing-auction strategy. The empirical assumptions permit short selling, omit bid-ask spreads, charge 10 basis points of traded volume, and annualize with 252 days.

## Portfolio optimization and the incomplete cost overlay

Let $p_t$ and $P_t$ be predictive mean and covariance. The basic portfolio solves

$$
\min_w w'P_tw\quad\text{subject to}\quad \mathbf1'w=1.
$$

Its unconstrained-short solution is $P_t^{-1}\mathbf1/(\mathbf1'P_t^{-1}\mathbf1)$. Target-return portfolios add $w'p_t=\tau_t$, with $\tau_t=0.10/252$ or $0.15/252$. The source also writes an inequality as a practical equivalent. It is equivalent only when the return constraint binds: if the unconstrained minimum-variance portfolio already exceeds the target, the inequality solution need not equal the equality solution.

Benchmark-neutral portfolios use the index as series one and impose $w_1=0$ and $w'P_{t,\cdot1}=0$. These constraints prevent direct investment in the index and set forecast covariance with it to zero; they do not make realized returns uncorrelated or guarantee zero factor exposure under a misspecified covariance model. Gross leverage, position caps, borrow availability, financing charges, and sector bounds are not specified.

For equality constraints collected as $B'w=b$, a self-contained implementation is

$$
w=P_t^{-1}B(B'P_t^{-1}B)^{-1}b,
$$

provided the matrices are nonsingular and constraints independent. This formula follows from the Lagrange first-order conditions and covers budget, return, benchmark-weight, and benchmark-covariance constraints. It clarifies the model-to-decision map without inventing additional optimization penalties.

The starred strategies P1*–P6* add a turnover-reduction overlay. The paper interpolates between old weights $w$ and the fresh optimum $w^0$ using $w^\lambda=\lambda w+(1-\lambda)w^0$, then says to set expected gain equal to proportional trading cost. As printed, this is

$$
p'(w^\lambda-w)=c\|w^\lambda-w\|_1.
$$

For $0\leq\lambda<1$, both sides scale by $1-\lambda$. The equation reduces to $p'(w^0-w)=c\|w^0-w\|_1$ and cannot select a unique positive partial-trade fraction. Unless the full proposed trade already satisfies equality, only the no-trade solution necessarily satisfies it. Thus an additional nonlinear utility criterion, different gain definition, or implementation rule is needed; the PDF does not provide one. Exact after-cost portfolio reproduction is blocked by this ambiguity. The note does not repair it by inventing a different trading rule and attributing that to the authors.

There is also a return-accounting approximation: $w'y_t$ is a weighted sum of asset log returns, whereas a discretely rebalanced self-financing portfolio's simple return is $\sum_jw_j(e^{y_{jt}}-1)$, before costs. Its log return is not generally $w'y_t$. The paper optimizes the linear log-return moments and reports annualized log performance, without fully detailing the wealth and weight-drift accounting needed to reconcile these objects. This distinction becomes more relevant with unrestricted shorts and leverage.

## Wishart benchmark and reproducible comparison

Appendix A defines the WDLM with common external predictors, matrix-normal state evolution, and inverse-Wishart covariance uncertainty. Given prior parameters $(a,R,r,B)$, its forecast has Student degrees of freedom $r$, center $f=F'a$, and scale $qB/r$, where $q=1+F'RF$. The forecast covariance is $qB/(r-2)$ for $r>2$.

With error $e=y-f$ and gain $K=RF/q$, posterior parameters are

$$
m=a+Ke',\qquad C=R-KK'q,\qquad n=r+1,\qquad D=B+ee'/q.
$$

For random-walk states the next prior has $a^+=m$, $R^+=C/\delta$, $r^+=\beta n$, and

$$
B^+=D\frac{r^++m_{dim}-1}{n+m_{dim}-1},
$$

where $m_{dim}$ is the number of return series, distinguished here from the posterior mean matrix. This is the source's inverse-Wishart parameterization, whose mean is $B/(r-2)$; transplanting a library convention using a different degree-of-freedom definition without conversion would be wrong.

Five portfolio benchmark models W1–W5 use covariance discount 0.95 and local state discounts 0.995–0.999. These are distinct from the more reactive WDLM used to propose parents, whose discounts are 0.8 and 0.95. Confusing the two WDLM roles changes both the graphs and the benchmark performance.

## Forecast and portfolio results, with qualifications

Table 1's predictive log-likelihood improves as parental discount rises: M1 is −661.6 and M5 −642.6 in the reported table scale; MA1 is −662.3 and MA5 −644.3. The prose claims the mean absolute deviation favors discount 0.997, but the table does not support that statement. M3 has MAD $1.408\times10^{-2}$, worse than M4's $1.397\times10^{-2}$; MA3 is $1.491\times10^{-2}$, worse than the other MA entries. This is a source discrepancy, not evidence that a particular discount is universally optimal. The normalization of the displayed aggregate log-likelihood values is not explained sufficiently to reconstruct their scale from individual predictive densities alone.

Table 5 reports a passive SPX Sharpe ratio of 0.31 and equal-weight P0 of 0.41. M1's P1*–P6* ratios are 0.71, 0.79, 0.86, 0.71, 0.76, and 0.84. M2's are 0.82, 0.87, 0.86, 0.81, 0.87, and 0.88. MA5 reaches 0.91 for benchmark-neutral minimum variance P4*. In contrast, W1 ranges from −0.11 to 0.10, and the other Wishart-based portfolios are similarly weak. The source's claim that all models beat SPX plainly applies to SGDLM variants, not to its WDLM benchmark rows.

Appendix C separates return from risk. SPX annualized log return is 6.2% with volatility 19.9%; equal weighting gives 9.1% and 21.9%. M1 P3* gives 12.0% and 14.0%, consistent with its approximately 0.86 ratio. M2 P5* gives 12.4% and 14.2%, while MA5 P4* gives 11.6% and 12.8%. The concluding prose says returns reach 12.1%, but the table contains 12.4%; the table-specific value is retained. No risk-free-rate subtraction series is specified, and the ratios closely match annualized log return divided by volatility. They should not be relabeled as fully documented excess-return Sharpes.

The reported M1 P3* wealth path turns an initial \$1,000 into \$3,862 after stated trading costs. The passive index ends at \$1,996; the best cited Wishart combination W1/P4* ends at \$1,168. The article does not supply turnover totals, gross exposures, borrow costs, confidence intervals for performance differences, or a multiple-testing correction across model/strategy pairs. These are historical case-study outcomes under the stated assumptions, not estimated expected future net returns.

Forecast fit and decision performance rank models differently. M5 has better reported predictive likelihood than M1, yet M1's higher-target portfolios perform better. A decision can be particularly sensitive to errors in particular directions of the mean/covariance forecast that receive modest weight in aggregate density scores. This is the paper's useful decision-theoretic point; the empirical selection still needs independent validation if the best portfolio is chosen after inspecting the same test period.

## Graph behavior, entropy, and computational limits

Plots for 3M show slower coefficient movement and less parental turnover when the parental discount rises to 0.999. The observed parents are not merely same-sector substitutes. Basic materials and utilities are overrepresented in the reported cross-sector summaries, while communications and technology are underrepresented; SPX is the most heavily represented single parent. These findings are descriptive of the selected predictive representation. They do not establish stable causal sector transmission.

The optimized KL discrepancy in the decoupling step rises when the independent normal-gamma approximation becomes poorer. The authors interpret this as a market-wide signal of changing multivariate structure. Their scaled plots move with VIX and the St. Louis financial-stress index, with the SGDLM measure often reacting or normalizing faster. The index is available daily, while the comparison macro-financial measure is weekly. The paper explicitly favors an observational interpretation. It provides no calibrated alarm threshold, lead-time distribution, real-time vintage alignment test, or independent false-positive/false-negative evaluation. A large entropy value can reflect approximation/model stress as well as economic stress.

The computation exploits independent local simulation and GPU parallelism; a 401-dimensional iteration is reported to take about ten seconds on the authors' hardware, and a full analysis less than a day. Their comparison with a five-factor MCMC model used 500 burn-in and 5,000 retained iterations and took more than 25 minutes per refit. A separate unrestricted VAR implementation exceeded available memory. These comparisons establish feasibility on the reported implementation, not an invariant speed ordering across future software or all alternative covariance models.

The PDF omits the importance-sample and predictive-sample counts, random seed, initialization matrices, numerical determinant safeguards, and complete graph-update edge cases. It refers to earlier software for those details. Together with the SNR, turnover, return-accounting, and selection-sample issues, these prevent exact reconstruction of the headline net wealth path from the paper alone. The central algorithm is nevertheless clear: fit small local dynamic models, correct their posterior dependence with determinant weights, project for efficient evolution, and change parent sets gradually using predictive evidence. That is the reusable contribution, with the case study supplying encouraging but conditional economic evidence.
