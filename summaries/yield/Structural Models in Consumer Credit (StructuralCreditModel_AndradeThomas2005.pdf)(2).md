# Structural Models in Consumer Credit

Fabio Wendling Muniz de Andrade and Lyn Thomas. Working paper, source filename dated 2005, 20 PDF pages. The title page does not supply a publication date. Source: [StructuralCreditModel_AndradeThomas2005.pdf](../../Finance/StructuralCreditModel_AndradeThomas2005.pdf). Page references below use the PDF's printed pagination.

## Why this matters and what is new

The paper transfers the first-passage logic of corporate structural credit models to consumer lending. Its state variable is the value of access to future credit, represented empirically by a credit-bureau score, rather than the market value of a firm's assets. Default occurs when creditworthiness falls below a threshold. The resulting predictor combines today's score with the volatility of that individual's past scores. A portfolio extension adds a common macroeconomic state to the score dynamics and simulates a distribution of default rates.

The useful empirical finding is that historical score volatility contains ranking information beyond the current score: in the main Brazilian sample, the Kolmogorov–Smirnov separation statistic rises from 41.0 to 46.6 percentage points. The simplest zero-drift diffusion performs best among eight specifications. The more tentative claim concerns capital: the proposed portfolio model gives lower extreme default-rate quantiles than a Vasicek comparison. Those lower quantiles are model outputs, not demonstrated improvements in tail accuracy.

The distinction between discrimination and calibration is central. The model can improve which borrowers are ranked as risky while producing poorly calibrated borrower probabilities. The source's own probability-band table shows this clearly. Also, the macroeconomic calibration uses a balance-weighted stock of delinquent credit, whereas the borrower experiment uses the occurrence of any adverse bureau report during a future year. These are different outcomes and require a measurement bridge that the paper does not estimate.

## Economic mechanism: credit reputation as the state variable

Section 2, pp. 2–4, starts with latent creditworthiness $Q_i$. The probability that a lender accepts a future application, $P_{a,i}=f(Q_i)$, increases with creditworthiness. The value to the consumer of future access to borrowing, $R_i=h(P_{a,i})$, increases with acceptance probability. Consequently $R_i=g(Q_i)$ is increasing.

A default becomes public to lenders and damages future borrowing access. The consumer compares the value of preserving that access with the debt obligation. In the stylized decision, paying preserves $R_i$, while default avoids paying debt $D_i$ but loses that reputation value. Default is attractive when $R_i<D_i$, equivalently when

$$
Q_i<K_{Q,i},\qquad K_{Q,i}=g^{-1}(D_i).
$$

This motivates a barrier model. It does not establish a market-traded asset valuation or risk-neutral option-pricing equation. The empirical probabilities are intended as physical default probabilities. The functions connecting creditworthiness, acceptance, and reputation are assumed monotone, not estimated separately.

The treatment of liquidity constraints is particularly restrictive. A consumer whose cash flow is insufficient to service debt can borrow further, increasing total obligations and hence the default threshold. Alternatively, cash-flow uncertainty can enter through a stochastic threshold. The paper does not solve a household budget problem with borrowing limits, unemployment insurance, bankruptcy law, or lender-specific refusal. Continued access to refinancing while distressed is a substantive assumption, not a consequence of the barrier construction.

Empirically, the model replaces unobserved $Q_i$ by a transformed bureau score and uses a common, constant barrier for the cross-section. That simplifies implementation but loses the individually varying debt and reputation thresholds suggested by the theory. An individual score's measurement error, rating-system revisions, and update frequency are not modeled separately from genuine changes in creditworthiness.

## Data, endpoint, and score transformation

Section 3 uses Serasa, a Brazilian credit-information provider. The main sample contains 1,000 randomly selected consumers with recorded credit activity. Each has 37 monthly bureau scores, January 2000 through January 2003, giving 36 monthly increments. Outcomes are observed over February 2003–January 2004.

The outcome is the appearance of a negative public or private bureau record relating to any credit operation at any lender. Such records commonly concern obligations 30–60 days overdue. This is broader than default on a particular bank's loan and differs from a 90-day regulatory definition. There are 359 bad and 641 good consumers: an observed 12-month bad rate of 35.9%. A lender reproducing the exercise must construct the same any-lender event definition; substituting charge-off on its own loans changes both prevalence and meaning.

Let $q_{it}$ denote the original bureau score on a 0–1,000 scale. The source associates $q/1000$ with survival probability and transforms it into log survival odds:

$$
S_{it}=\log\left(\frac{q_{it}}{1000-q_{it}}\right).
$$

Thus larger $S$ means better creditworthiness. The denominator uses the scaled score; applying a logit directly to an unscaled value such as 700 is invalid. Scores at 0 and 1,000 give infinite transformed values. The paper does not report an endpoint-clipping rule or the frequency of endpoint observations, so this is an unresolved data-processing input.

The dynamics below describe increments of transformed scores. Volatility has units of log-odds per square root of time. A standard deviation of score levels over 37 months is not interchangeable with the diffusion standard deviation estimated from the 36 increments.

## Candidate dynamics and estimation

The source's equations (1)–(2), pp. 4–5, combine drift, Brownian movement, normally distributed jumps arriving according to a Poisson process, and a Bernoulli indicator of whether the score changes. The printed differential equations omit the time differential on the drift. A coherent discrete monthly representation of the intended components is

$$
\Delta S_{i,t}=C_{i,t}\left[\mu_i\Delta t+\sigma_i\sqrt{\Delta t}\,Z_{i,t}+\sum_{j=1}^{N_{i,t}}A_{i,t,j}\right],
$$

where $Z$ is standard normal, $N$ is Poisson with mean $\lambda\Delta t$, jumps $A$ are normal with location $\mu_a$ and scale $\sigma_a$, and $C$ is Bernoulli with change probability $p_c$. The Brownian, Poisson, and jump-amplitude terms are independent in the specification. Monthly implementation takes $\Delta t=1$. The explicit sum over jumps and time scaling above clarify the stochastic interpretation; the paper does not supply simulation code establishing every discretization choice.

Zero inflation means that a whole observed-period increment is zero when $C=0$. An independently redrawn Bernoulli variable at every instant is not by itself a well-defined continuous-time process; its interpretation needs a sampling interval. Likewise, normal jump amplitudes permit positive as well as negative jumps even though the motivating examples are adverse life events.

All eight candidates include volatility. Their additional components are:

| Model | Drift | Jumps | Zero inflation | KS, percentage points |
|---|---|---|---|---:|
| 1 | Yes | Yes | Yes | 44.9 |
| 2 | Yes | Yes | No | 44.4 |
| 3 | Yes | No | Yes | 46.2 |
| 4 | Yes | No | No | 45.9 |
| 5 | No | Yes | Yes | 45.7 |
| 6 | No | Yes | No | 44.8 |
| 7 | No | No | Yes | 45.7 |
| 8 | No | No | No | 46.6 |

The estimation method is Markov chain Monte Carlo. Drift and volatility are individual-specific parameter vectors; other parameters are estimated at portfolio level. This pooling is important because there are only 36 increments per borrower. The paper does not report priors, chain lengths, burn-in, proposals, convergence diagnostics, or whether posterior means, modes, or draws feed the forecast. Exact replication of its fitted parameters is therefore impossible from the paper alone. Substituting maximum likelihood for the zero-drift Gaussian case would be a defensible new implementation, but would not replicate the reported estimation procedure.

For each model and borrower, simulate 10,000 future paths over 12 months. A path defaults if it crosses the threshold at any point; the empirical crossing fraction is the predicted probability. A common threshold $K$ is varied over a feasible range. For ranking, the chosen $K$ maximizes KS; for portfolio calibration, it can instead be selected to match the mean simulated default probability to an observed default rate. These are separate objectives and need not produce the same barrier.

The source does not specify the threshold grid spacing, monitoring mesh, or whether crossings between sampled dates are handled with a Brownian bridge. A monthly endpoint simulation misses intra-month crossings, so it will generally produce a smaller first-passage probability than a continuous-monitoring formula at the same parameters. The maximal binomial Monte Carlo standard error from 10,000 independent path indicators is 0.005, or half a percentage point, before parameter uncertainty. This standard error is a derived diagnostic, not a source-reported confidence interval.

## Closed form for the selected diffusion

The best specification is simply

$$
S_i(t)=S_i(0)+\sigma_i W_i(t).
$$

For $S_i(0)>K$ and $\sigma_i>0$, define $\tau_i=\inf\{u\geq0:S_i(u)\leq K\}$. The reflection principle gives the source's equation (3), p. 9:

$$
P(\tau_i\leq t)=2\Phi\left(\frac{K-S_i(0)}{\sigma_i\sqrt t}\right).
$$

The factor of two distinguishes default at any time before the horizon from merely ending below the barrier. The model therefore ranks borrowers, for a fixed horizon and barrier, by their standardized distance $(S_i(0)-K)/\sigma_i$. High volatility raises default probability when the borrower starts above the barrier. Starting at or below it means immediate default, probability one; the displayed formula must not be applied there because it can exceed one. With zero volatility and a starting score above $K$, default probability is zero in this specification.

Differentiating the crossing distribution yields equation (4):

$$
f_{\tau_i}(t)=\frac{S_i(0)-K}{\sigma_i\sqrt{2\pi t^3}}\exp\left[-\frac{(S_i(0)-K)^2}{2\sigma_i^2t}\right],\qquad t>0.
$$

The zero-drift hitting-time law is the Lévy distribution, a limiting inverse-Gaussian form. The source calls it inverse Gaussian without this qualification. It has infinite mean hitting time even though eventual crossing has probability one. Neither feature should be interpreted as a realistic statement about a consumer's entire remaining life: the fitted experiment has a 12-month horizon, and drift, debt changes, exits, and score-system changes become important over longer periods.

## Ranking results and probability calibration

KS is the maximum separation between the empirical good and bad score distributions. Reported values use a 0–100 percentage-point scale, so 46.6 corresponds to 0.466. The original bureau score has KS 41.0. The selected diffusion gains 5.6 percentage points, while the more elaborate jump and zero-inflated models perform less well. Short individual histories provide a plausible estimation-error explanation, but the comparison does not isolate that mechanism experimentally.

The authors bootstrap 50,000 samples of 1,000 consumers with replacement and examine differences in KS. They report a first-percentile difference of 0.15 and state significance at 1%. The text does not provide a separate interval for every candidate or enough detail to establish whether the threshold and model choice are repeated inside each bootstrap. Hence this should not be read as a fully adjusted test of the best result after searching eight models and barriers.

A second 1,000-consumer sample is used for validation with the original barrier fixed. Its bureau-score KS is 39.0, versus 43.3 for the structural score, a 4.3-point improvement. Reoptimizing the barrier gives 43.5, but that latter figure uses validation outcomes to tune the model. The paper does not supply the second sample's exact dates, cohort construction, or overlap controls, so one cannot establish a clean chronological out-of-time design.

Table 3 is especially informative about calibration:

| Predicted probability band | Good | Bad | Observed bad fraction |
|---|---:|---:|---:|
| Below 10% | 477 | 108 | 18.5% |
| 10–30% | 77 | 59 | 43.4% |
| 30–50% | 25 | 34 | 57.6% |
| 50–70% | 20 | 29 | 59.2% |
| 70–90% | 15 | 29 | 65.9% |
| 90–100% | 27 | 100 | 78.7% |

Observed risk rises fairly consistently across bands, but the low-risk probabilities are too low and the highest probabilities too high. Maximizing a ranking statistic does not impose calibration. A practical implementation needs a separately trained probability mapping or another calibration objective, evaluated on new outcomes; the paper does not perform a complete such exercise.

## Joint defaults and the missing covariance regularization

Section 4 simulates the 1,000 consumers jointly, with correlated Gaussian score increments and a default barrier. There are 100,000 portfolio scenarios. The default fraction in scenario $b$ is

$$
D_b=\frac1{1000}\sum_{i=1}^{1000}1\{\tau_{i,b}\leq12\}.
$$

This is a count-weighted default distribution, not a credit-loss distribution. Exposure at default, recovery, collateral, and loss given default are absent from this simulation. A portfolio with heterogeneous loan sizes cannot convert these count fractions directly into capital amounts.

The paper describes a correlation matrix estimated from score increments and Cholesky-based Gaussian generation. There is a material unreported implementation step: 1,000 series observed over 36 increments produce a sample covariance matrix of rank at most 35 after demeaning. Ordinary full-rank Cholesky factorization cannot be used without a suitable factorization, regularization, or other handling of singularity. Eigenvalue factorization or shrinkage would resolve the numerical issue, but either must be documented as a reconstruction choice because the source does not specify it.

Mean pairwise estimated correlation is only 0.00095 for monthly changes and 0.0047 for six-month changes. The authors interpret this as bureau scores failing to capture the common economic cycle. That is possible, but short histories, estimation noise, asynchronous bureau updates, and score transformations also affect the evidence. Low mean correlation alone does not identify which mechanism is responsible.

## Adding a common economic state

The extension shifts every individual's unconditional score by the same function of a four-state macroeconomic regime:

$$
S_{c,i}(s)=S_{u,i}+f(s),\qquad K_c(s)=K_u-f(s).
$$

Thus shifting all scores and moving the barrier in the opposite direction are equivalent representations. The common shift introduces dependence that is missing from the small observed average correlations. It also assumes equal additive exposure of all borrowers to the macro state in log-odds units.

The state variable comes from 118 monthly observations, July 1994–April 2004, of a Brazilian market default index, MDI. This is the fraction of private-financial-institution consumer-credit balances more than 60 days past due; residential mortgages are excluded. Sort the monthly observations into four default-rate quartiles, with state 1 the least distressed. For each month define $\ell_t=\log[(1-\mathrm{MDI}_t)/\mathrm{MDI}_t]$. Equation (8) defines

$$
f(s)=\operatorname{mean}(\ell_t\mid s_t=s)-\operatorname{mean}(\ell_t).
$$

The average is taken after the log-odds transformation. It is not the log odds of the average default index. Estimated shifts are 0.2795, 0.1044, −0.0023, and −0.3722. These are ex-post state estimates from the complete macro sample, not recursively estimated real-time signals.

The monthly transition matrix, rows denoting the current state and columns the next state, is

$$
P=\begin{pmatrix}
.897&.103&0&0\\
.103&.690&.172&.035\\
0&.167&.733&.100\\
0&.067&.100&.833
\end{pmatrix}.
$$

A reproducible simulation draws the next state from its current row and shifts scores by $f(s_{t+1})-f(s_t)$, or adjusts the common barrier equivalently. The paper does not completely specify the initial-state treatment, dependence between macro innovations and residual score innovations, or monitoring within each monthly transition.

The first-order Markov test contains a source inconsistency. Its statistic comparing first- and second-order transition probabilities is 10.6. The text gives $m(m-1)=12$ degrees of freedom for four states, but quotes a 5% critical value of 51.0. For unrestricted positive-probability transitions, parameter counting gives $m(m-1)^2=36$ degrees of freedom, whose critical value is approximately 51.0; 12 degrees of freedom would give about 21.0. Either reference distribution would fail to reject here, but sparse and zero transition cells further weaken a naive asymptotic test. Nonrejection with 118 months is not proof of a first-order regime process.

## Tail comparison and its interpretation

The historical Basel II comparison on pp. 15–17 uses the homogeneous asymptotic Vasicek distribution. For unconditional default probability $p$ and asset correlation $\rho$, the $a$-quantile of the default fraction is

$$
q_a=\Phi\left(\frac{\Phi^{-1}(p)+\sqrt\rho\,\Phi^{-1}(a)}{\sqrt{1-\rho}}\right).
$$

A constant-LGD unexpected-loss capital expression is $\mathrm{LGD}(q_{.999}-p)$. These historical formulas are objects compared in the paper, not a statement of current regulation. Its other-retail correlation function is

$$
u(p)=\frac{1-e^{-35p}}{1-e^{-35}},\qquad \rho(p)=.03u(p)+.16[1-u(p)].
$$

The $u(p)$ on the right denotes the function defined on the left. The MDI average is 14.8%. Fitting the Vasicek cumulative distribution to the observed MDI distribution by nonlinear least squares gives $\hat\rho=0.0228$, standard error 0.00233, approximate 95% interval [0.0182, 0.0275]. The historical Basel function at $p=.148$ gives 0.0307. Table 7 reports an F statistic of 3716.10, but its degrees-of-freedom totals imply 119 observations whereas the narrative says 118. Serial dependence and the stock nature of MDI also prevent taking the conventional regression uncertainty as a complete measure of calibration risk.

The portfolio comparison then concerns the 1,000-consumer sample, not a portfolio with the MDI mean substituted for its borrower bad rate. Table 8 reports:

| Model | 99th-percentile default fraction | 99.9th-percentile default fraction |
|---|---:|---:|
| Proposed score/state simulation | 46.3% | 47.9% |
| Vasicek with historical Basel correlation | 51.7% | 57.0% |
| Vasicek with estimated implicit correlation | 49.6% | 54.2% |

The first Vasicek comparison is 5.4 and 9.1 percentage points above the proposed model at the two tails. The fitted-correlation comparison is 3.3 and 6.3 points above. These are economically large differences, but none identifies the true quantile. There are only about 100 simulated observations above the 99.9th percentile in 100,000 scenarios, and the macro history is much too short to validate that tail directly. Parameter, regime, covariance, and endpoint-definition uncertainty are not included in the reported quantiles.

The replicable contribution is the progression from a bureau score to a distance-to-barrier predictor and then to joint default scenarios with a common state. The empirical ranking gain survives a second sample, subject to missing cohort details. The capital exercise is best treated as sensitivity evidence: assumptions about dependence and the mapping from delinquent balances to borrower default have a much larger role than the apparent precision of a quoted tail percentile suggests.
