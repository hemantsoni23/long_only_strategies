# The Message in Daily Exchange Rates: A Conditional-Variance Tale

**Richard T. Baillie and Tim Bollerslev. Originally published in Journal of Business & Economic Statistics 7(3), July 1989.** The supplied file is the January 2002 twentieth-anniversary reprint in volume 20(1), pp. 60–68, retaining the original article's 1989 header. References below use the reprint's printed pages.

**Source:** [ForexForecasting_BaillieBollerslev_1989.pdf](../../Finance/ForexForecasting_BaillieBollerslev_1989.pdf), ten PDF pages including a JSTOR cover. The complete article, equations, seven tables, and references were inspected. No separate appendix or code is embedded.

## Why this matters

A currency's next return can be difficult to predict in the mean while its risk is strongly predictable. Treating a near-martingale return series as independent Gaussian noise throws away that distinction. Baillie and Bollerslev show that six daily exchange-rate series have little ordinary return autocorrelation but pronounced volatility clustering, fat tails, and calendar effects. Their parsimonious model combines a GARCH(1,1) variance, explicitly filtered calendar interventions, and standardized Student-$t$ innovations.

The useful methodological contribution is the combination. Conditional Gaussian GARCH produces an unconditional heavy-tailed mixture, but it does not account for all of the observed daily tail behavior. An unconditional heavy-tailed distribution alone does not describe clustering. A conventional additive day-of-week dummy in a GARCH recursion also propagates its effect through future variance in a way the authors want to avoid. Their intervention filter separates a calendar-specific pulse from the persistent response to stochastic innovations.

They then reestimate suitable models at weekly, fortnightly, and four-weekly frequencies. Evidence for conditional heavy tails and variance dynamics weakens with aggregation, but this is accompanied by a large reduction in sample size. The paper is an in-sample statistical characterization, not a demonstration of profitable currency timing or a calibrated risk-neutral option-pricing model.

## Data, units, and sampling

The data are **New York foreign-exchange opening bid prices** from Data Resources Incorporated for France, Italy, Japan, Switzerland, the United Kingdom, and West Germany against the U.S. dollar. The reported span is March 1, 1980 through January 28, 1985, with 1,245 price observations and 1,244 daily changes. Preserve the historical market calendar: the starting calendar date is not a license to insert artificial weekend quotes.

For each currency, the modeled return is

$$
r_t=100(\log s_t-\log s_{t-1}).
$$

Thus the mean is in percentage points per sampled interval and variance is in squared percentage points. Changing to decimal returns rescales mean parameters by 1/100 and variance parameters by 1/10,000, while leaving the GARCH persistence parameters unchanged. The source's interpretation of negative drifts reflects dollar appreciation over this historical sample. The raw quote orientation must be verified against the original DRI series before replicating signs with a contemporary vendor.

There are **35 nonweekend market closures**, coded through a vacation indicator. The day associated with a return is the day of its ending opening quote: a Monday return compares Monday's opening bid with the previous available quote, normally Friday's opening bid. This timing helps explain why the full weekend information effect may not be confined to Monday.

The lower-frequency datasets select every Wednesday, every second Wednesday, and every fourth Wednesday. When a selected Wednesday is a market closure, the following Thursday is used. The resulting return samples have **255 weekly, 127 fortnightly, and 63 four-weekly observations**. The final frequency is called monthly in the tables, but it is not calendar-month-end sampling. Different weekdays and alternative fortnightly/four-weekly starting Wednesdays were checked without markedly different conclusions, although the full alternative estimates are not reported.

## Initial diagnosis: unit roots do not imply independent returns

Section 2 fits log-level regressions with and without a deterministic trend and applies Phillips–Perron statistics. Long-run innovation variances use autocovariances through lag **22**, approximately one trading month, with a Newey–West-type correction. The exact statistic formulas are referenced to Perron's work rather than reproduced in the article.

The three reported 5% critical values are −3.41, 6.25, and −2.86 for the trend $t$ statistic, joint trend/unit-root statistic, and intercept-only $t$ statistic, respectively. None of the six currencies rejects the corresponding unit-root hypothesis. For example, the French statistics are −2.613, 3.435, and −0.679; the Japanese statistics are −2.695, 4.127, and −1.935 (Table 1). Non-rejection supports modeling changes rather than a stationary log level, but does not establish an exact random walk.

The initial constant-mean Gaussian model is

$$
r_t=b_0+\epsilon_t,\qquad \epsilon_t\mid\mathcal F_{t-1}\sim N(0,\omega_0).
$$

Table 2 shows little evidence of serial correlation in returns through fifteen lags: Ljung–Box $Q(15)$ ranges from 13.483 for West Germany to 24.987 for Japan. The analogous statistics on squared residuals are much larger, ranging from 25.864 for France to 252.640 for Switzerland. France is only just significant at the 5% threshold, while the other currencies give much stronger evidence against conditional homoskedasticity.

| Currency | Gaussian-model variance | Raw residual kurtosis | Squared-residual $Q^2(15)$ |
|---|---:|---:|---:|
| France | 0.563 | 11.292 | 25.864 |
| Italy | 0.407 | 4.915 | 118.161 |
| Japan | 0.450 | 8.178 | 127.574 |
| Switzerland | 0.581 | 4.208 | 252.640 |
| United Kingdom | 0.430 | 4.814 | 102.707 |
| West Germany | 0.495 | 4.205 | 156.834 |

Kurtosis here is the fourth standardized moment, with a Gaussian benchmark of **3**, not excess kurtosis with a benchmark of zero. The prose's asymptotic statement should be interpreted as applying to the centered quantity $\widehat m_4-3$ when comparing with a zero-mean normal limit. Heavy tails can also affect finite-sample behavior of the autocorrelation diagnostics.

A martingale-difference mean permits conditional variance dependence. A strict independent-increment random walk does not. Moreover, the efficient-market discussion should not be overextended: spot exchange-rate changes alone omit interest-rate carry, financing, and risk premia. The paper's descriptive conditional-mean findings do not prove that all economically relevant currency excess returns have zero conditional expectation.

## The calendar-adjusted daily model

Let $D_{jt}$ indicate Monday through Friday for $j=1,\ldots,5$. Let $V_t=1$ on the first observation after a nonweekend closure, and zero otherwise. Let $W81_t=1$ for Wednesdays before **October 1, 1981**. Before that date, foreign-currency transactions on Wednesday could clear on Friday while corresponding dollar transactions cleared on Monday; the dummy tests the potential effect of the two-day interest timing difference.

The conditional mean in equation (5) is

$$
r_t=b_0+\sum_{j=1}^{5}b_jD_{jt}+b_8W81_t+\epsilon_t.
$$

There is no autoregressive return term in the reported final model. The calendar coefficients are normalized to sum to zero across weekdays, so $b_0$ is an average weekday component rather than an omitted-day baseline. The source estimates a possible vacation dummy in the mean as a diagnostic, but does not retain it.

Define the deterministic variance intervention

$$
g_t=\sum_{j=1}^{5}\omega_jD_{jt}+\omega_6V_t+\omega_7V_{t-1},
\qquad \rho=\alpha_1+\beta_1.
$$

The conditional variance is

$$
h_t=\omega_0(1-\rho)+\alpha_1\epsilon_{t-1}^{2}+\beta_1h_{t-1}+g_t-\rho g_{t-1}.
$$

Equivalently, the intervention is filtered by $(1-\rho L)$. This exact term is easy to miss when transcribing the printed equation. Replacing it with $+g_t$ alone changes the model and its interpretation.

Why use the filter? A one-off calendar pulse of size $\omega_j$ raises contemporaneous variance by that amount. The next period's expected GARCH propagation would be $\rho\omega_j$, which the lagged intervention subtracts. This makes the pulse interpretation comparable to standard intervention analysis. The two vacation coefficients deliberately allow a closure-related effect over two successive sampled observations.

The weekday variance coefficients are also normalized to sum to zero. An unrestricted intercept plus all five weekday effects would be collinear; one must impose a normalization or omit a category during estimation and transform afterward. The paper discusses the exceptional integrated-variance case separately. Its reported $\omega_0$ in the daily parameterization is not the same object as the intercept called $\omega_0$ in the lower-frequency ordinary GARCH equations.

Negative weekday coefficients are permissible because they are deviations around a positive baseline. They do not mean negative conditional variance. Numerical estimation must nevertheless enforce $h_t>0$ for every observation and every evaluated parameter vector. Simply imposing positive $\omega_0,\alpha_1,\beta_1$ is not a complete positivity check once signed intervention terms are included.

## Conditional distribution and maximum likelihood

The innovations have the variance-standardized Student-$t$ representation

$$
\epsilon_t=\sqrt{h_t}\,z_t,\qquad
z_t=\sqrt{\frac{\nu-2}{\nu}}\,T_\nu,\qquad \nu>2.
$$

Here $T_\nu$ is an ordinary Student-$t$ variable. This scaling is indispensable: it makes $\operatorname{Var}(z_t)=1$, so $h_t$ is the conditional variance rather than an unadjusted scale parameter.

A complete per-observation log likelihood is

$$
\ell_t=\log\Gamma\left(\frac{\nu+1}{2}\right)
-\log\Gamma\left(\frac\nu2\right)
-\frac12\log[\pi(\nu-2)]-\frac12\log h_t
-\frac{\nu+1}{2}\log\left(1+\frac{\epsilon_t^2}{h_t(\nu-2)}\right).
$$

The article's displayed likelihood suppresses a parameter-independent normalizing constant. Such constants do not change estimates or nested likelihood-ratio differences if treated consistently, but they matter when matching absolute log-likelihood levels across implementations.

The paper also considers a power-exponential conditional density. Its maximized likelihood is lower than the Student-$t$ likelihood in every case examined, while mean and variance parameter estimates are similar. The two families are not nested, so this comparison is not a conventional nested likelihood-ratio test. Only the Student-$t$ results are tabulated; the proposed Hausman-type comparison is not implemented.

Estimation uses the **Berndt–Hall–Hall–Hausman algorithm with numerical derivatives**, jointly including the degrees-of-freedom parameter. Initialization of variance, numerical derivative step sizes, optimizer tolerance, boundary handling, and random or deterministic starting values are not stated. Those are genuine reproduction gaps, especially because estimated persistence is close to one.

## Daily parameter estimates and diagnostics

Table 3 gives the following core parameters. Degrees of freedom and persistence below are calculated from the published inverse degrees of freedom and GARCH coefficients, which are rounded.

| Currency | $\omega_0$ | $\alpha_1$ | $\beta_1$ | $\rho$ | $1/\nu$ | Approximate $\nu$ |
|---|---:|---:|---:|---:|---:|---:|
| France | 0.505 | 0.114 | 0.829 | 0.943 | 0.140 | 7.14 |
| Italy | 0.403 | 0.113 | 0.848 | 0.961 | 0.093 | 10.75 |
| Japan | 0.402 | 0.049 | 0.941 | 0.990 | 0.159 | 6.29 |
| Switzerland | 0.537 | 0.073 | 0.907 | 0.980 | 0.054 | 18.52 |
| United Kingdom | 0.404 | 0.061 | 0.910 | 0.971 | 0.109 | 9.17 |
| West Germany | 0.448 | 0.085 | 0.881 | 0.966 | 0.054 | 18.52 |

The standard errors for $\alpha_1$ are 0.025, 0.023, 0.011, 0.017, 0.017, and 0.018 in that order; those for $\beta_1$ are 0.035, 0.031, 0.013, 0.020, 0.025, and 0.026. All six processes are highly persistent. A conventional test in the source does not reject $\alpha_1+\beta_1=1$ for any currency. This is non-rejection near a boundary, not proof that the true model is integrated GARCH.

As a derived scale illustration, the deterministic decay half-life $\log(1/2)/\log\rho$ is about 12 observations for France and 69 for Japan. These are calculations from point estimates in the simplified variance propagation, not confidence intervals, calendar-day estimates, or reported out-of-sample forecast durations.

The estimated weekday mean effects are largest and positive on Wednesday for every currency. France, for example, has $b_0=-0.073$ and weekday effects $(−0.025,−0.006,0.081,−0.032,−0.018)$. Its Wednesday mean outside the pre-October-1981 effect is therefore approximately $−0.073+0.081=0.008$ percentage points. The additional early-Wednesday coefficient is 0.130 (0.084). The analogous early-Wednesday coefficients are positive for all six currencies but individually insignificant at conventional levels.

The Monday variance effects are all positive: 0.183, 0.102, 0.120, 0.099, 0.069, and 0.121. Thursday effects are all negative: −0.103, −0.060, −0.097, −0.052, −0.062, and −0.076. These are variance shifts in squared percentage-point units, not percentage changes in volatility. For France, the Monday baseline is approximately $0.505+0.183=0.688$ before stochastic deviations and holiday effects, compared with Thursday's approximately 0.402. Taking square roots would give a different relative change in standard deviation.

Both reported vacation coefficients are positive for every currency. The immediate and next-observation coefficients are (0.202, 0.260) for France, (0.083, 0.197) for Italy, (0.090, 0.125) for Japan, (0.318, 0.335) for Switzerland, (0.350, 0.206) for the United Kingdom, and (0.186, 0.299) for West Germany. An additional second lag of the vacation indicator is not supported: the reported LM statistics range from 0.274 to 2.177. A vacation dummy in the mean is also insignificant at 10%, with LM statistics between 0.087 and 2.451.

Joint tests are more revealing than individual dummy $t$ ratios. Table 4's joint mean-calendar test has $p$ values 0.011, 0.008, 0.104, 0.091, 0.252, and 0.038. Thus conventional 5% evidence is clear for France, Italy, and Germany, weaker for Japan and Switzerland, and absent for the United Kingdom. The joint variance-calendar test rejects for every currency, with reported $p$ values no greater than 0.004. The vacation-only variance test is strongest for France, Switzerland, the United Kingdom, and Germany; Japan has $p=0.306$.

After fitting, standardized-residual $Q(15)$ values range from 8.445 to 17.297, and squared-standardized-residual $Q^2(15)$ from 7.579 to 26.625. The model substantially reduces dependence, but Japan's latter value is marginal at a conventional fifteen-degree-of-freedom reference threshold. Estimated-parameter effects and heavy tails complicate exact finite-sample calibration; these diagnostics should not be marketed as conclusive proof of an independent innovation sequence.

For $\nu>4$, standardized Student-$t$ kurtosis is $3(\nu-2)/(\nu-4)$. France retains a sizable mismatch: sample standardized-residual kurtosis is **7.372**, versus fitted conditional kurtosis **4.915**. Other comparisons are Italy 3.873 versus 3.890, Japan 4.909 versus 5.621, Switzerland 3.395 versus 3.413, the United Kingdom 4.904 versus 4.160, and Germany 3.535 versus 3.414. The authors judge France the clearest remaining tail failure. Conditional finite fourth moments do not alone guarantee a finite unconditional GARCH fourth moment; that additionally depends on the stochastic variance recursion.

## What changes with temporal aggregation

At each lower frequency, the authors select the most parsimonious model not rejected at 5% relative to a Student-$t$ GARCH(1,1) benchmark. Daily calendar dummies are not carried unchanged into these lower-frequency models. The exercise reestimates each process rather than mechanically exponentiating daily persistence or multiplying daily variance by the interval length.

Weekly GARCH estimates remain substantial:

| Currency | Weekly ARCH coefficient | Weekly GARCH coefficient | Conditional distribution retained |
|---|---:|---:|---|
| France | 0.144 | 0.655 | Student-$t$, $1/\nu=0.147$ |
| Italy | 0.187 | 0.658 | Gaussian |
| Japan | 0.072 | 0.927 | Student-$t$, $1/\nu=0.177$ |
| Switzerland | 0.121 | 0.784 | Gaussian |
| United Kingdom | 0.049 | 0.842 | Gaussian |
| West Germany | 0.249 | 0.636 | Gaussian |

Weekly squared-residual $Q^2(10)$ remains significant for Italy (26.131) and Germany (23.194). The article traces these to lag seven in Italy and lags seven and eight in Germany, without offering a firm economic explanation. The weekly model is therefore not uniformly adequate merely because its distribution is simpler.

At the fortnightly frequency, Gaussian ARCH(1) is retained for France, Italy, and Japan, with coefficients 0.478 (0.184), 0.423 (0.211), and 0.346 (0.171). The other three currencies use constant conditional variance. Conditional normality is retained for all six. This change reflects both temporal aggregation and the smaller sample of 127 observations.

At four-weekly frequency, Table 7 reports constant-variance Gaussian models for all currencies. Sample kurtoses are 4.643, 3.670, 3.447, 3.790, 3.109, and 3.434, respectively. France is the notable tail exception discussed in the text. Its August 1982 observation, associated with the Mauroy government's austerity program, lies roughly four standard deviations from the mean. Removing it reduces French kurtosis to **3.469**. This is an explanatory sensitivity calculation, not a recommendation to delete adverse events from risk estimation.

The prose refers to France as an exception concerning monthly departures, while the displayed table gives a constant-variance model. A replication should distinguish the clearly documented kurtosis exception from a claim that Table 7 estimates a monthly French ARCH coefficient; no such coefficient is shown.

The authors explicitly leave open how much apparent convergence to normality is attributable to the loss of statistical power. The sample falls from 1,244 daily returns to only 63 four-weekly returns. A failure to reject conditional heteroskedasticity or nonnormality in the latter sample is not evidence that extreme monthly currency risk disappears.

## Reimplementation and interpretation

An implementation should preserve the quote timestamps and market calendar, construct weekday and closure dummies, fit the normalized mean and filtered-variance equations jointly by Student-$t$ likelihood, and inspect standardized residuals. It should then recreate the exact Wednesday subsamples and perform the nested simplifications at each frequency. The benchmark tests are the table's parameter scales, likelihood differences, residual autocorrelation statistics, and kurtosis comparisons—not just a visually plausible volatility path.

Missing details include the original DRI data vintage and exact quote orientation, all holiday dates, presample variance initialization, numerical optimization settings, and the precise handling of parameter-boundary tests. Data substitutions and alternative standard errors should be recorded as reconstruction choices. The Student-$t$ normal limit occurs at $1/\nu=0$, a boundary; modern inferential choices may differ from the paper's conventional asymptotic treatment.

The durable result is that weak mean dependence can coexist with strong, persistent conditional risk. Calendar effects, volatility persistence, and conditional tails each explain a different feature of daily currency returns. Their relative importance depends on frequency, and the remaining French tail problem shows why a compact model still needs residual checks. The paper gives a practical physical-measure return-density model; converting it into an option-pricing model or a profitable trading strategy requires additional assumptions and evidence.
