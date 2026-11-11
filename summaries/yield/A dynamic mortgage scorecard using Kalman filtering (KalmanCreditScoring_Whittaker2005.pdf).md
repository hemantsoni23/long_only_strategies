# A dynamic mortgage scorecard using Kalman filtering

**Joe Whittaker, Chris Whitehead, and Mark Somers.** Nine-page manuscript, associated with Lancaster University and Scimetrics. [Source PDF](../../Finance/KalmanCreditScoring_Whittaker2005.pdf). The filename supplies 2005, but the supplied manuscript does not print a publication year, journal, or DOI; those details are not inferred. All nine pages, including the references, were read. Equations, sampling definitions, coefficient table, and monitoring plots were checked against rendered pages. Page numbers below are the manuscript's own.

## Why this matters

A scorecard can retain almost the same ranking power while becoming materially miscalibrated. A common shift in good-loan log odds changes the predicted bad rate and the meaning of a fixed acceptance cutoff without changing the ordering of customers. Monitoring only a Gini coefficient can therefore miss a decision-relevant deterioration in the calibration of a fixed scorecard.

This manuscript proposes a practical diagnostic: fit logistic regressions to successive cohorts of newly observed outcomes, combine their noisy coefficient estimates with a Kalman filter, and compare the resulting coefficient and score trajectories with simulated paths under the baseline scorecard. Its distinctive feature is the integration of dynamic coefficient smoothing with sequential, pathwise tolerance limits conditioned on the actual covariates of incoming borrowers. The Kalman filter, logistic likelihood, and parametric bootstrap are established components; their organization into a scorecard-monitoring system is the contribution.

The commercial mortgage illustration finds a rising intercept and declining risk estimates while the Gini remains broadly stable. This motivates recalibration rather than automatically rebuilding all attribute effects. The result is a retrospective monitoring illustration, not evidence that dynamically replacing the origination model produces higher out-of-time profits. The source also leaves an important prior-probability issue unresolved: half the Goods are sampled out of baseline estimation, but a corresponding intercept correction or matching monitoring-sample design is not documented.

## Logistic score and observation construction

Let $Y_i=1$ denote a Good outcome and $z_i\in\mathbb R^p$ include an intercept and dummy-coded applicant attributes. The model is

$$
\mu_i=P(Y_i=1\mid z_i)=\frac{e^{\beta'z_i}}{1+e^{\beta'z_i}},
\qquad \operatorname{logit}\mu_i=\beta'z_i.
$$

Thus higher scores mean lower bad risk. The corresponding Bad probability is $1-\mu_i$. In the mortgage illustration, a Bad reaches at least two months in arrears within 18 months of joining. The introduction describes missing at least two consecutive payments; a reproducible outcome should follow a documented arrears-status algorithm because missed payments and arrears duration can differ after catch-up payments or restructuring.

For the cohort whose outcomes become observable at time $t$, the logistic log likelihood is

$$
\ell_t(\beta)=\sum_{i=1}^{n_t}
\left[Y_{ti}\beta'z_{ti}-\log(1+e^{\beta'z_{ti}})\right].
$$

The score and information are

$$
U_t(\beta)=Z_t'(Y_t-\mu_t),\qquad
\mathcal I_t(\beta)=Z_t'W_tZ_t,
\quad W_{t,ii}=\mu_{ti}(1-\mu_{ti}).
$$

A local maximum-likelihood estimate $\widehat\beta_t$ supplies a compressed observation, with approximate sampling distribution

$$
\widehat\beta_t\mid\beta_t\ \dot\sim
N(\beta_t,V_t),\qquad V_t=\mathcal I_t(\widehat\beta_t)^{-1}.
$$

The dot emphasizes a large-sample approximation. The raw response remains Bernoulli; the filter operates on locally fitted coefficients, not directly on individual outcomes. There must be enough informative observations in each cohort for the coefficient estimate and its covariance to be meaningful. Full-rank covariates, enough outcomes in each relevant group, and absence of complete or quasi-complete separation matter in addition to the total cohort count.

The paper notes that small samples can make information matrices singular but supplies no exact treatment. A generalized inverse by itself does not solve separation or identify a coefficient for a category absent that month. Pooling intervals, imposing a proper prior, or using a penalized local fit would change the observation model and should be documented. Such alternatives are sensible extensions, not procedures shown to have been used here. Local-fit uncertainty also ignores randomness in previously selected cutpoints and variables.

## State model and the full Kalman recursion

The hidden state is the current logistic coefficient vector. The source assumes a random walk,

$$
\beta_{t+1}=\beta_t+q_t,\qquad E[q_t]=0,
\qquad \operatorname{Var}(q_t)=Q=\sigma I_p,
$$

and observations

$$
\widehat\beta_t=\beta_t+r_t,\qquad E[r_t]=0,
\qquad \operatorname{Var}(r_t)=V_t.
$$

Observation errors are independent across intervals conditional on the underlying states. Standard Kalman interpretation additionally requires suitable independence or orthogonality between state innovations, past states, and measurement errors. If all these noises are Gaussian and covariance matrices known, the recursion gives the conditional mean and covariance exactly. Here Gaussianity of local estimates and plug-in $V_t$ make it an approximation. The manuscript names the recursion but does not display its complete matrix form; the following is its direct reconstruction.

Let $b_{t-1}$ and $P_{t-1}$ denote the filtered state estimate and error covariance after the previous cohort. Then

$$
b_{t\mid t-1}=b_{t-1},\qquad
P_{t\mid t-1}=P_{t-1}+Q,
$$

$$
S_t=P_{t\mid t-1}+V_t,\qquad
K_t=P_{t\mid t-1}S_t^{-1},
$$

$$
b_t=b_{t-1}+K_t(\widehat\beta_t-b_{t-1}).
$$

A numerically stable covariance update is

$$
P_t=(I_p-K_t)P_{t\mid t-1}(I_p-K_t)'
+K_tV_tK_t'.
$$

In exact arithmetic with the optimal gain this equals $(I_p-K_t)P_{t\mid t-1}$. Linear solves should replace explicit matrix inversion in computation. This numerical recommendation and the displayed Joseph-form covariance update are implementation details derived from the model, not additional algorithms printed in the manuscript.

An equivalent information-form interpretation is

$$
P_t^{-1}=P_{t\mid t-1}^{-1}+V_t^{-1},
\qquad
b_t=P_t\left(P_{t\mid t-1}^{-1}b_{t-1}+V_t^{-1}\widehat\beta_t\right).
$$

The filter weighs a cohort according to its information, not simply its number of borrowers. A large but almost homogeneous cohort may provide little information about some attribute coefficients. Even though $Q$ is diagonal, the posterior covariance and gain need not be: dummy variables and their logistic coefficients are statistically related through the design matrix.

The source calls $\sigma$ the “signal to noise ratio.” In the displayed equation it is actually the scalar increment variance, with observation noise separately represented by $V_t$. Relative smoothing depends jointly on the two, and there is no single dimensionless ratio unless an observation scale is fixed. The reported illustration sets $\sigma=0.002$, so the one-period innovation standard deviation of each coefficient is $\sqrt{0.002}\approx0.0447$ log-odds units under the stated parameterization, not 0.002. At $\sigma=0$ the latent scorecard is constant, while observed coefficient estimates still fluctuate.

Equal process variances are motivated by dummy-coded attributes, but remain a modeling restriction. Reparameterizing the design, changing reference categories, or scaling a covariate generally changes the appropriate covariance structure; an isotropic $Q$ is not invariant to arbitrary recoding. Allowing correlated coefficient drift or a separate intercept variance could be useful, but is not fitted in this paper.

## Initialization and the meaning of adaptation

The filter starts at the baseline coefficient vector $b_0$ but uses a deliberately diffuse covariance, for example $P_0=10^5I_p$. Consequently the initial Kalman gain is close to the identity when local measurement uncertainty is modest relative to that covariance, and $b_1$ is driven primarily by the first new cohort. The baseline sample is not carried forward as a strong prior based on its estimated information. The source emphasizes this choice on pp. 4–5.

This matters for interpretation: the baseline is principally a comparison model and a generator of null bootstrap outcomes. The dynamic trajectory is largely estimated from post-baseline observations. A reader expecting all historical observations to enter a cumulative fit would implement a different method by initializing with the baseline inverse information.

With positive process variance, uncertainty is injected each period, preventing old evidence from accumulating without limit. The resulting weights on older data decay through products of gain complements. This differs from choosing one fixed exponential forgetting factor: local information varies with cohort size, composition, and outcomes, and so does $K_t$. The manuscript tunes $\sigma$ by simulations or resampling the baseline and by visual comparison of resulting paths. It says likelihood is insensitive to alternative settings and leaves a more objective selection method for future work. No tuning grid, loss function, sensitivity table, or power curve is given.

## Tracked statistics and conditional null simulation

The basic monitored quantities are the individual coefficients. The source also tracks expected Bad rates in attribute groups, score quantiles such as the 25th, 50th, and 75th percentiles, and a Gini coefficient. Dynamic scores for current cohort members are $s_{ti}=b_t'z_{ti}$; baseline scores on those same members are $s^0_{ti}=b_0'z_{ti}$. Comparing the two on identical covariates helps separate coefficient change from a different mix of customers.

For a subgroup $A_t$, a natural expected Bad-rate statistic consistent with the model is

$$
\widehat p_{B,t}(A_t)=\frac1{|A_t|}\sum_{i\in A_t}
\frac1{1+\exp(b_t'z_{ti})}.
$$

The source shows such a statistic for the Csal2 group but does not give its exact aggregation code. No loan-size weighting is reported. Under the usual rank convention, a Gini can be written $2\operatorname{AUC}-1$, with appropriate orientation for Good scores. The paper does not specify its treatment of tied scores or finite-sample Gini estimation, so this identity is an implementation convention rather than a verbatim source formula.

The null hypothesis fixes the true scorecard at the fitted baseline $b_0$. For each bootstrap path and each new cohort, hold the actual observed covariates fixed and simulate independent Bernoulli outcomes with

$$
P(Y^*_{ti}=1\mid z_{ti})=\operatorname{logit}^{-1}(b_0'z_{ti}).
$$

Fit a new local logistic model to that cohort's simulated outcomes, calculate its own information matrix, and pass both through that bootstrap path's Kalman recursion. Continue path by path across time. Recomputing local covariance matters: under the null, outcome variation affects both the coefficient estimate and its estimated precision. The paper suggests, for example, 1,000 such paths; it does not unequivocally identify the exact simulation count used in every illustration.

These are conditional, parametric null bands. They preserve realized changes in the covariate distribution and cohort size, while testing whether outcomes remain consistent with the fixed baseline response relation. They do not model the future covariate distribution. They treat the estimated baseline as given rather than resampling its uncertainty, and independent Bernoulli simulation does not capture extra outcome dependence among borrowers exposed to common shocks. Those distinctions affect calibration of the alarm rate.

## Sequential tolerance limits: what the probability guarantee means

Choose a horizon $T$ and desired whole-path coverage 0.90. At each date, choose a band containing fraction

$$
c=0.9^{1/T}
$$

of the simulated paths that have survived all previous bands. Remove paths that first exit; construct the next date's band using the survivors. This conditional selection is the essential step. It is not equivalent to drawing independent 90% pointwise confidence intervals.

In an ideal population simulation, if each step retains exactly fraction $c$ of the survivors, the probability of remaining inside through date $T$ is

$$
\prod_{t=1}^T P(\text{inside at }t\mid\text{survival through }t-1)
=c^T=0.90.
$$

Independence between dates is not required for this chain-rule calculation. Empirical quantiles, finite bootstrap counts, ties, and a chosen allocation between upper and lower tails make actual coverage approximate. The paper does not specify the tail allocation or integer rounding of discarded paths.

For $T=12$, the retained fraction is approximately 0.99126 each period, corresponding to 0.874% conditional attrition. For a 36-period horizon it is about 0.99708, or 0.292% attrition. With 1,000 paths, a 36-step procedure initially discards only about three paths per date, making tail placement sensitive to Monte Carlo resolution. These are derived numerical implications. The manuscript gives 12 as an example horizon and plots 36 monitoring periods, but does not state the exact horizon/reset configuration used for every plotted band.

The 90% statement applies separately to each tracked statistic. It is not 90% simultaneous coverage across eight coefficients, multiple score quantiles, subgroup rates, and Gini statistics. Nor does repeatedly resetting a new monitoring horizon preserve a lifetime 10% false-alarm rate. The source correctly says the limits adjust for previous testing within a trajectory, but supplies no familywise adjustment across the entire dashboard. A crossing is a monitoring signal conditional on this design, not an unconditional probability that the model has changed.

## Mortgage sample, baseline, and timing

The private database contains roughly 180,000 accepted mortgage applicants, about 30 variables, and approximately seven years of monthly arrears/balance records beginning in 1997. The authors do not know the actual admission scorecard. Clients joining during the first 12 months form the baseline; clients joining in the following 36 months supply monitoring cohorts. The exact lender, geography, dates, observation exclusions, closure/censoring rules, and raw data are not supplied.

The outcome needs an 18-month performance window. A real-time implementation can use a joining cohort only once its labels have matured or under a separately modeled partial-outcome scheme. Section 3 defines update time by when outcomes are ascertained; the illustration indexes cohorts by joining month. The paper does not provide the mapping from joining month to actual decision-date availability. Its plots should therefore not be read as proving that an alarm was available contemporaneously with those borrowers' origination. Using the full future outcome at origination would be look-ahead.

After sampling half the Goods, the baseline contains 12,656 Goods and 836 Bads, or 13,492 observations. The reported bad rate is 6.20%. Five variables produce seven nonreference dummy attributes plus an intercept, with no interactions:

| Variable | Reference category | Higher categories |
|---|---|---|
| Pension | No | Yes |
| Restat | 0 | 1 |
| Advance | at most 40,000 | above 40,000 through 57,000; above 57,000 |
| Tbank | at most 5 | above 5 through 9; above 9 |
| Csal | at most 19,271.7 | above 19,271.7 |

The source does not define all units or attribute abbreviations. Monetary denominations and time units should not be invented. Residential status is included through logistic modeling although its marginal information value is not predictive, illustrating that marginal screening can differ from conditional contribution.

The baseline coefficients are intercept 1.486; Pension2 0.444; Restat2 0.253; Advance2 0.219; Advance3 0.545; Tbank2 0.361; Tbank3 0.695; and Csal2 0.304. All nonreference coefficients raise Good log odds. The reported baseline Gini is 0.336. The lowest possible score is 1.486, with all reference categories, but the average bad rate must be averaged over the actual attribute distribution rather than obtained from the intercept alone.

## The sampling-offset issue

Sampling on outcomes alters the intercept of a logistic model. If Goods are included with probability $s_G$ and Bads with probability $s_B$, independently of covariates within each outcome, then

$$
\frac{P_s(G\mid z)}{P_s(B\mid z)}
=\frac{s_G}{s_B}\frac{P(G\mid z)}{P(B\mid z)}.
$$

Therefore population Good log odds equal sample Good log odds minus $\log(s_G/s_B)$. With half the Goods and all Bads, the required population offset is $+\log2\approx0.6931$. Slopes remain unchanged under the correctly specified logistic model and this class-only sampling design. Absolute probabilities do not.

The manuscript does not state whether it corrects the intercept, applies the same outcome sampling to all monitoring cohorts, or adjusts the bootstrap target. The displayed 6.20% rate equals the sampled baseline's rate. If “half” is exact and every Bad is retained, the unsampled baseline would have 25,312 Goods and 836 Bads, with Bad rate approximately 3.20%; this is a conditional calculation, not an independently observed population statistic.

If monitoring uses a different Good sampling fraction without an offset, an apparent common intercept shift could partly be a sampling artifact. If baseline and monitoring are sampled identically, that particular comparison may remain meaningful on the sampled scale, although population PDs still need correction. The omission does not invalidate the filtering idea or prove that the observed drift is artificial. It prevents an unqualified interpretation of the displayed absolute rates and intercept trend until the sampling protocol is resolved.

## Findings and their scope

With $\sigma=0.002$, five coefficient paths remain within their displayed limits: Advance2, Advance3 just within, Tbank2, Tbank3, and Csal2. Intercept and Restat2 cross, and Pension2 crosses at about monitoring month 30. The rendered Restat2 path trends downward while the intercept trends upward; “similar” in the prose should not be interpreted as identical direction. The source gives graphical paths rather than an exact month-by-month coefficient table, so more precise crossing dates are unavailable.

The expected Csal2 Bad rate and the score quantiles cross their limits. Score quantiles shift upward in broadly parallel fashion. The tracked Gini stays within its limits, roughly constant and somewhat below the initial estimate. Gini based on the unchanged baseline card on new customers is usually slightly lower than the dynamic version, but no large systematic separation is reported.

The authors suggest a parsimonious alternative $s_t(z)=a_t+\beta'z$ with time-varying intercept and stable slopes. A common intercept shift preserves within-cohort ranking exactly, so unchanged discrimination is consistent with changed calibration. It changes each borrower's odds by the same multiplicative factor, not each borrower's probability by the same additive amount; the introductory claim that an intercept change reduces all risks “by the same amount” needs this log-odds qualification. Also, subgroup membership and borrower mix can change quantiles across cohorts even under fixed coefficients, which is why conditioning the simulated bands on actual covariates is valuable.

The illustration does not estimate a macroeconomic cause, a structural break date, expected loan profit, or the loss from retaining the old cutoff. It gives no formal model comparison between an intercept-only drift process and all-coefficient random walks, and no out-of-time forecast evaluation. Several coefficient crossings make the stable-slopes interpretation plausible as a simplification, not conclusively established. An unchanged Gini does not prove that every segment retains the same error rates.

## Replication boundary and useful extensions

A replication needs borrower-level cohort dates, matured outcomes, unchanged covariate definitions, sampling probabilities, baseline selection code, local-fit settings, and exact simulation controls. The key source inputs still missing are the private records, category handling for sparse months, offset convention, baseline uncertainty treatment, exact horizon and path count, tail quantiles, and any band-reset rule. The finite-sample distribution of logistic estimates, including possible separation, should be reflected in the bootstrap exactly as in the observed path.

The method monitors accepted borrowers under a historical policy. It cannot infer risk for rejected applicants whose outcomes are absent, nor separate changes in applicant quality from changes in admission policy without further information. The unknown original approval scorecard is therefore a substantive limitation, not merely missing metadata. The model is also conditioned on a selected set of variables and cutpoints; changes outside that representation can remain hidden in aggregate diagnostics.

The source proposes varying the Good/Bad definition, running segment-specific cards, adding alternative predictors, comparing paths with macroeconomic variables, and extending the framework to churn, profit, or continuous responses. These are research directions, not evaluated results. For the supplied mortgage evidence, the main operational insight is narrower and useful: track calibration and ranking separately, recognize outcome maturation delays, and evaluate a coefficient trajectory against sequential null variation rather than an arbitrary two-sample comparison.

## Source map and bibliography

Pages 1–2 give the motivation and logistic sampling approximation; pp. 3–5 specify the state model, initialization, bootstrap, and sequential limits. Pages 6–7 define the mortgage sample and baseline; pp. 7–8 show all coefficient and summary-statistic paths; p. 9 gives extensions and references. The source draws on Kalman (1960), Harvey (1990), West and Harrison (1997), logistic-regression texts by McCullagh and Nelder and Hosmer and Lemeshow, and Thomas, Edelman, and Crook (2002) on credit scoring. Those references were not separately reviewed here. The complete filter equations, chain-rule coverage argument, sampling-offset derivation, and numerical implications above are reconstructions explicitly distinguished from reported findings.
