# Stochastic Discount Factor Bounds with Conditioning Information

## Source and scope

**Wayne E. Ferson and Andrew F. Siegel**, *The Review of Financial Studies* 16(2), Summer 2003, pp. 567–595, DOI 10.1093/rfs/hhg004. Original PDF: [StochasticDiscount_FersonSiegel_2003.pdf](../../Finance/StochasticDiscount_FersonSiegel_2003.pdf). The article was previously titled *Optimal Moment Restrictions on Stochastic Discount Factors*.

All 36 PDF pages were read: the 29-page article, the JSTOR cover, and six pages of appended linked references. Key formulas on PDF pp. 6–11, the data tables on p. 13, the two figures on pp. 15–16, the simulation tables on pp. 18 and 22, and the inference formula/tables on pp. 25–26 were checked visually. Some equations disappear entirely in the PDF's text layer, so the mathematical reconstruction below uses the page images.

## Why this matters

A high sample Sharpe ratio can be an optimization artifact. Since an HJ variance bound is a transformation of the maximum attainable Sharpe ratio, the same artifact can make an estimated asset-pricing restriction look much stronger than its population counterpart. Adding lagged instruments multiplies the number of apparent test assets, sometimes doubling the estimated lower bound through sampling bias alone. A model may then be rejected because the researcher optimized against noise.

Ferson and Siegel make two decisions explicit: how conditioning information is incorporated and how the resulting bound's sampling distribution is handled. A theoretically tighter bound need not provide the most useful empirical diagnostic when its conditional moments are misspecified or its estimates are noisy. Their comparison gives a practical role to managed portfolios that remain valid even when they fail to be optimal.

The paper is useful when evaluating a consumption kernel, a factor SDF, or any proposed pricing model with lagged information. It is also relevant to portfolio researchers: the same bias arises when estimating the best Sharpe ratio from many assets and predictors. This is a diagnostic and inference paper, not evidence that the optimized portfolios earn their sample Sharpe ratios after costs or outside the estimation period.

## Contribution and distinctions

The article compares four constructions: fixed-return HJ bounds, multiplicative instrument bounds, bounds from unconditionally efficient managed portfolios (UE), and the optimal Gallant–Hansen–Tauchen (GHT) bound. It supplies a convenient closed form for GHT, a finite-sample correction that is exact for the fixed-bound estimator under independent normal returns, an approximate correction for optimized bounds, and a simulation comparison calibrated to annual, quarterly, and monthly datasets.

It does not claim that the UE or optimal frontier is newly discovered here. UE portfolios come from Ferson–Siegel (2001), while the optimal restriction comes from GHT (1990). The contribution is the tractable implementation and evidence on finite-sample performance. The simulation also assesses Hansen–Heaton–Luttmer (HHL) asymptotic standard errors for the fixed and multiplicative bounds. It does not extend those standard errors to the optimized UE and GHT estimators.

Keep three concepts separate. **Population validity** means every admissible pricing kernel lies above the bound. **Tightness** compares valid population restrictions. **Statistical reliability** concerns the location and dispersion of an estimated bound. The paper shows that a procedure can perform well on one dimension and poorly on another.

## Pricing setup and the fixed bound

Let $R_t$ be an $n$-vector of gross asset returns, $Z_{t-1}$ the chosen public instruments, and $e$ the vector of ones. A valid SDF satisfies

$$
E[m_tR_t\mid Z_{t-1}]=e.
$$

The instruments are taken as given; selecting them is not part of the paper's optimization. The analysis does not impose SDF positivity. Finite second moments, invertible relevant covariance matrices, and the integrability needed for managed payoffs are implicit in the displayed formulas.

With no conditioning information, set $E[R]=\mu$, $\operatorname{Var}(R)=\Sigma$, and fix the kernel mean $\bar m=E[m]$. The minimum-variance kernel is

$$
m_F=\bar m+(e-\bar m\mu)'\Sigma^{-1}(R-\mu),
$$

with variance

$$
V_F(\bar m)=(e-\bar m\mu)'\Sigma^{-1}(e-\bar m\mu).
$$

This is $\bar m^2$ times the maximum squared Sharpe ratio relative to the implicit gross risk-free return $1/\bar m$. If an actual constant risk-free asset is priced, its return constrains the allowable mean. Otherwise varying $\bar m$ produces the familiar frontier of candidate kernel means and variances.

The conditional pricing equation implies

$$
E[(m_tR_t-e)f(Z_{t-1})]=0
$$

for every suitable measurable function $f$. This follows by iterated expectations. The paper's wording about conditional independence is unnecessary for this step: the lagged instrument function is measurable at the conditioning date. The managed payoff $R_tf(Z_{t-1})$ has the associated time-$t-1$ price $ef(Z_{t-1})$. Correctly tracking that price is essential; a scaled payoff is not automatically a unit-price return.

## Multiplicative instrument bounds

The common implementation uses a constant and a finite set of lagged instruments and multiplies each basic return by each instrument. If there are $L$ nonconstant instruments, this produces $n(L+1)$ test payoffs. The paper normalizes each instrument by its unconditional mean, writing $\widetilde Z=Z/E[Z]$ component by component, so that

$$
E[m_t(R_t\otimes\widetilde Z_{t-1})]=e.
$$

Apply the ordinary HJ calculation to this expanded vector. This normalization requires nonzero instrument means. A general implementation with zero-mean instruments should retain a payoff-price formulation rather than divide by zero. Sampling error in the estimated instrument means is another input to uncertainty.

The method is easy to compute and does not need a full model of conditional return moments. It includes only a limited family of managed strategies, however. More importantly, its covariance inversion uses the expanded dimension. Estimation error therefore rises with both the number of assets and the number of instruments. A bound's rise after adding instruments is partly an economic question about predictable investment opportunities and partly a statistical question about fitting a larger return space.

## Unconditionally efficient portfolio bounds

Let $x(Z)$ denote portfolio weights with $e'x(Z)=1$ at every date. Define conditional moments

$$
\mu(Z)=E[R\mid Z],\qquad
\Sigma_\varepsilon(Z)=\operatorname{Var}(R\mid Z),
$$

and

$$
\Lambda(Z)=\left[\mu(Z)\mu(Z)'+\Sigma_\varepsilon(Z)\right]^{-1}
=E[RR'\mid Z]^{-1}.
$$

For a target unconditional mean $\mu_p$, the portfolio minimizes $E[(x'R)^2]$ subject to the pointwise budget condition and $E[x'\mu(Z)]=\mu_p$. The second-moment matrix, rather than the covariance matrix alone, enters because the conditional expected return can vary with $Z$ while the target mean is unconditional.

Define the constants

$$
\alpha_1=E\left[\frac{1}{e'\Lambda e}\right],\qquad
\alpha_2=E\left[\frac{e'\Lambda\mu(Z)}{e'\Lambda e}\right],
$$

$$
\alpha_3=E\left[\mu(Z)'\left(\Lambda-
\frac{\Lambda ee'\Lambda}{e'\Lambda e}\right)\mu(Z)\right].
$$

Then, in row-vector form, the efficient weights are

$$
x(Z)'=\frac{e'\Lambda}{e'\Lambda e}
+\frac{\mu_p-\alpha_2}{\alpha_3}
\mu(Z)'\left(\Lambda-
\frac{\Lambda ee'\Lambda}{e'\Lambda e}\right).
$$

The first term has weights summing to one. The second lies in the zero-budget direction because the matrix in parentheses annihilates $e$. This gives a useful implementation check independent of the objective calculation. The coefficient is common across states because the target constraint is on the unconditional mean.

The resulting variance frontier is

$$
\sigma_p^2=
\alpha_1+\frac{\alpha_2^2}{\alpha_3}
-\frac{2\alpha_2}{\alpha_3}\mu_p
+\frac{1-\alpha_3}{\alpha_3}\mu_p^2.
$$

Its global minimum occurs at

$$
\mu_p^*=\frac{\alpha_2}{1-\alpha_3},\qquad
(\sigma_p^*)^2=\alpha_1-\frac{\alpha_2^2}{1-\alpha_3}.
$$

These formulas presume a nondegenerate frontier; $\alpha_3=0$ or $1-\alpha_3=0$ requires separate treatment. The paper constructs two frontier portfolios, one at the global minimum and one with a target equal to the grand mean of asset returns. Any fixed mixture of these two traces the relevant unconditional frontier. Applying the fixed HJ formula to their realized returns gives the UE bound.

The crucial robustness property is economic, not a claim that estimation error disappears. If conditional moments are wrong, the calculated weights may fail to be efficient, but still describe an admissible managed portfolio as long as they use available information and satisfy the budget constraint. Pricing that portfolio remains a valid requirement. The resulting population bound is weaker, rather than automatically invalid. Using fitted weights and returns from the same estimation sample still creates selection bias; the finite-sample work addresses that separate problem.

## The optimal conditional-information bound

For the GHT construction define, at each $Z$,

$$
\alpha(Z)=e'\Sigma_\varepsilon(Z)^{-1}e,\quad
\beta(Z)=e'\Sigma_\varepsilon(Z)^{-1}\mu(Z),\quad
\gamma(Z)=\mu(Z)'\Sigma_\varepsilon(Z)^{-1}\mu(Z).
$$

Let $\zeta(Z)=E[m\mid Z]$. Conditional on this mean, the least variable pricing kernel is

$$
m_*=\zeta(Z)+[e-\zeta(Z)\mu(Z)]'
\Sigma_\varepsilon(Z)^{-1}[R-\mu(Z)].
$$

Its conditional second moment is

$$
E[m_*^2\mid Z]
=\alpha(Z)-2\beta(Z)\zeta(Z)
+[1+\gamma(Z)]\zeta(Z)^2.
$$

Thus choose the entire function $\zeta$ to minimize the expectation of this quadratic, subject only to $E[\zeta]=\bar m$. A Lagrange multiplier common across states yields

$$
\zeta(Z)=\frac{\beta(Z)}{1+\gamma(Z)}+
\frac{1}{1+\gamma(Z)}
\frac{\bar m-E[\beta(Z)/(1+\gamma(Z))]}
{E[1/(1+\gamma(Z))]}.
$$

Substitution gives the optimal variance bound

$$
V_O(\bar m)=
\frac{\{\bar m-E[\beta/(1+\gamma)]\}^2}
{E[1/(1+\gamma)]}
+E[\alpha]-E\left[\frac{\beta^2}{1+\gamma}\right]-\bar m^2.
$$

Only four unconditional averages of conditional-moment functions are needed, and they can be estimated once for an entire grid of kernel means. This makes the formula computationally convenient. Unlike the UE portfolio calculation, substituting incorrect conditional moments into this expression need not yield a valid restriction on the true pricing kernel.

The optimal bound can exceed the UE bound because UE weights must sum to one state by state. With one basic asset, a fully invested portfolio cannot vary its weight at all; general scaled payoffs can still exploit conditioning information. Thus the two constructions need not coincide even with perfectly known moments. The optimal method's greater flexibility is a population advantage bought at the cost of stronger modeling demands.

## Finite-sample bias correction

Use the sample mean $\widehat\mu$ and covariance $S$ computed with denominator $T$. The plug-in fixed variance bound is

$$
\widehat V=(e-\bar m\widehat\mu)'S^{-1}(e-\bar m\widehat\mu).
$$

For independent multivariate normal returns, with $T>n+2$,

$$
E[\widehat V]=\frac{T}{T-n-2}V+
\frac{n}{T-n-2}\bar m^2.
$$

Therefore

$$
\boxed{\widehat V_{adj}=
\left(1-\frac{n+2}{T}\right)\widehat V
-\frac{n}{T}\bar m^2.}
$$

This corrects a variance estimator, not its square root. It can be negative in finite samples; this is not a negative population variance. Clipping at zero for display is different from claiming the clipped statistic is unbiased. The source's Figure 2 sets negative adjusted values to zero before plotting the volatility frontier.

For multiplicative bounds the authors apply the same correction with $n(L+1)$ replacing $n$. This is a useful approximation rather than a general exact theorem for products of returns and instruments. The expanded payoffs need not be jointly normal or independent, and instrument means are estimated. The simulations deliberately include these complications and show that the adjustment often works well.

For optimized bounds the proposed correction is

$$
\widehat V_{*,adj}=
\frac{T-n-2}{T}\widehat V_*
-\frac{n}{T}\bar m^2
+\frac{2}{T}\widehat{\operatorname{Var}}[E(m\mid Z)].
$$

The derivation conditions on $Z$ and applies the fixed-bound expectation relation to the conditional residual-return problem. It treats parameters in $E(m\mid Z)$ at their probability limits, which is why it is approximate. In the examples the final positive variance term contributes less than 0.2% of the total adjustment. The main effect is a degrees-of-freedom shrinkage, but that shrinkage does not fully capture the estimation complexity of the optimized conditional moments.

## Data, experiments, and numerical results

The annual dataset has 95 observations, 1891–1985: real stock-index and short-term bill returns from the Shiller data, with their lagged returns as instruments. The quarterly dataset has four Treasury-bill maturity portfolios, with three-month holding periods, real returns deflated using the nondurable-goods CPI component, and lagged returns/consumption information. The reported simulation has $T=93$ and 20 effective multiplicative assets. There is a source inconsistency: the text describes 1964Q3–1987Q4, while Table 1 labels 1964Q4–1986Q4 even though that interval does not contain 93 quarters. Exact calendar alignment must be recovered from the original data rather than inferred from the inconsistent labels.

Monthly data comprise 25 value-weighted SIC industry portfolios, February 1963–December 1994, $T=383$, with lagged one-month Treasury yield and S&P 500 dividend yield. The Fama–French model illustration uses July 1963–December 1994 to align with the separately estimated candidate kernels. The lagged monthly instruments have autocorrelations near 0.98. Return predictability is modest, with industry regression $R^2$ values roughly 0.02–0.10, but an optimized combination can still make conditioning information useful.

The baseline estimates conditional means by regression on instruments and conditional covariance by the residual covariance, held constant across dates. A VAR(1) models the instruments; return conditional means use the same lagged information. The simulation calibrates the covariance of return and instrument shocks, generates instruments recursively, and forms artificial returns from their conditional means plus innovations. Each artificial economist reestimates the model and the bounds using the same sample size as the actual dataset. There are 5,000 repetitions. A much longer artificial sample of one million observations supplies the model-specific population benchmark; it is not a claim about a known true economic SDF.

Table 3's monthly results at $E[m]=1$ are:

| Bound | Effective assets | Population variance bound | Mean unadjusted estimate | SD of estimate | Mean adjusted estimate | Adjusted SD |
|---|---:|---:|---:|---:|---:|---:|
| Fixed | 25 | 0.104 | 0.200 | 0.058 | 0.121 | 0.054 |
| Multiplicative | 75 | 0.313 | 0.626 | 0.114 | 0.304 | 0.092 |
| UE | 25 | 0.329 | 0.523 | 0.096 | 0.421 | 0.089 |
| Optimal | 25 | 0.386 | 0.615 | 0.115 | 0.506 | 0.107 |

Every entry concerns the variance of a dimensionless SDF. The SD columns describe sampling dispersion of the estimated variance bound, not SDF volatility. This distinction prevents misreading a simulation standard error as another point on the volatility frontier.

The raw monthly multiplicative estimate is twice the benchmark, a 100% upward bias. Correction lowers its mean to 0.304 versus 0.313, approximately −3%. The UE and optimal corrections are less effective: substantial positive biases remain despite their smaller raw biases. The baseline quarterly multiplicative mean is 1.564 versus a benchmark of 0.914, about 71% high, and its adjusted mean is 0.979, about 7% high using the rounded table values. The text reports an 8.5% figure; a replication should distinguish the text's reported comparison from arithmetic on the rounded displayed values.

For the annual sample the true fixed, multiplicative, UE, and optimal bounds are 0.197, 0.211, 0.203, and 0.212. These small differences reflect weak predictive information. Once uncertainty is included, the annual bounds provide little restriction on a positive SDF variance. In the monthly sample the fixed benchmark 0.104 is less than two adjusted standard errors above zero. The paper consequently emphasizes the combination of bound location and sampling precision rather than the raw curve alone.

As a diagnostic comparison, two adjusted standard deviations below the monthly population benchmark gives approximately 0.128 for the multiplicative bound, 0.148 for UE, and 0.173 for optimal. Those numbers are illustrative thresholds derived from simulation dispersions; they are not universal critical values or a substitute for the joint sampling distribution of a particular candidate SDF and the bound.

### The model-rejection illustration

The Fama–French SDF is a linear function of three factors. The unconditional version has fixed coefficients; the conditional version allows coefficients to vary linearly with the Treasury-yield and dividend-yield instruments. Before bias adjustment both appear below the conditional-information bounds. The raw multiplicative bound even lies above the nominally optimal bound, an ordering impossible for correctly computed population bounds on the same information set. The authors identify misspecification or sampling error as the explanations.

After adjustment the conditional model lies only 0.64 standard errors below the optimal bound, whereas the unconditional model lies 2.49 standard errors below it. Thus bias correction changes the illustrative conclusion for the conditional model; using the optimal instead of multiplicative bound changes the conclusion for the unconditional model. The source explicitly ignores sampling error in the plotted candidate SDF points. These examples therefore illustrate economically material estimation bias, rather than furnish complete hypothesis tests of the factor models.

## Robustness experiments

The first alternative replaces normal innovations by resampling observed residual vectors. This preserves empirical nonnormality while retaining the basic conditional-mean structure. The relative pattern is similar: large multiplicative bias, lower UE sampling dispersion, and useful fixed/multiplicative correction. The empirical residual sample limits what kinds of extreme-tail behavior this experiment can represent.

Two heteroscedastic designs follow. Model I uses a common factor innovation with time-varying variance plus residual noise with a fixed covariance. Its log squared innovation is regressed on instruments and transformed back with a scale correction for Jensen's inequality. Model II gives each asset its own conditional standard deviation, based on regressions of absolute residuals, while keeping correlations fixed. The model-II conditional covariance is shrunk toward the unconditional covariance to match the degree of predictability in squared residuals.

These designs change the population bounds themselves, so each receives a new long-simulation benchmark. They are not simply robustness checks around one fixed truth. The synthetic economist knows the functional forms but must estimate their parameters. The experiments therefore investigate parameter estimation under specified families, not unrestricted uncertainty about the family itself.

Model I gives some severe exceptions to the broad message that correction performs well. For annual data, the true fixed bound falls to 0.035 while the raw and corrected means are 0.214 and 0.184. The true monthly fixed bound is 0.050 and the corrected mean 0.121. Quarterly optimal-bound sampling SD is 1.765 in the displayed table, far above the 0.34-scale values seen in some other designs. These cases should not be hidden behind a claim of universal robustness.

Model II looks closer to the baseline. In monthly data its true multiplicative bound is 0.313, raw mean 0.647, and corrected mean 0.323. The true UE bound is 0.320 and corrected mean 0.412; true optimal 0.381 and corrected mean 0.478. The degrees-of-freedom correction continues to remove much of the multiplicative bias but leaves a sizable remainder in optimized bounds.

## Asymptotic standard errors and a reproducible workflow

For fixed or multiplicative payoffs $X_t$ and their lagged prices $P_{t-1}$, set

$$
\widehat a=S^{-1}(\overline P-\bar m\widehat\mu).
$$

The HHL influence quantity displayed in the paper is

$$
\varphi_t=-[\widehat a'(X_t-\widehat\mu)]^2
-2\widehat a'(\bar mX_t-P_{t-1}).
$$

Estimate the long-run variance of $T^{-1}\sum_t\varphi_t$ to obtain a standard error for the estimated variance bound. For fixed returns $X_t=R_t$ and $P=e$; multiplicative tests use the corresponding scaled payoff and price vectors. Centering constants do not affect the long-run variance, but payoff normalization and the price vector must be consistent.

The authors choose autocovariance lags from significant sample autocorrelations of this quantity, yielding one lag annually/monthly and four quarterly. In annual and quarterly simulations the asymptotic standard errors usually understate empirical dispersion by less than 10%. With 25 monthly assets or 75 multiplicative payoffs, understatement is worse, often exceeding 20%, and some heteroscedastic cases deteriorate further. For example, monthly model-II multiplicative sampling SD is 0.125 while the average unadjusted asymptotic SE is only 0.038. A reproduction should retain the table's exceptions rather than report only the generally favorable summary.

To reproduce the analysis, first fix returns, instruments, sample dates, and payoff-price normalization. Estimate all four raw bounds over a common grid of $\bar m$. Verify pointwise budget constraints in the UE strategies and all covariance ranks. Apply the correction to variances before any square root or truncation. Report raw estimates, corrected estimates, and uncertainty together. Reestimate the complete procedure in each simulation, including conditional moments and instrument normalizations. Record the random seed, the fitted VAR coefficients, the shock-resampling scheme, and the long-simulation benchmark separately for every data-generating process.

The PDF provides formulas, data descriptions, SIC classifications, selected summary statistics, simulation counts, and numerical results. It does not supply executable code, full parameter matrices, the historical industry return file, a uniquely consistent quarterly date description, or the separate Fama–French kernel estimates. Those inputs are required for exact numerical replication. For a new application, uncertainty in the candidate model's kernel must also be included; the illustrative charts do not do so.

The transferable lesson is to distinguish the economic information supplied by instruments from the extra dimensions they create in estimation. UE bounds offer a useful compromise when conditional moments are uncertain, because an imperfect strategy remains priceable. The optimal bound is attractive when those moments are credible and maximum population tightness matters. Neither choice removes the need to account for fitting error, dependence, and the number of tested payoffs.

## Implementation checks for a new conditional-bound application

The distinction between admissibility and efficiency provides a practical verification hierarchy. First check that every proposed managed payoff has the stated trading-date price. For a unit-budget UE portfolio, the weights must sum to one at each date, not merely on average. Second check its estimated moments and the resulting frontier calculation. Third assess how close its strategy is to the population-optimal strategy. Failure at the third step reduces tightness; failure at the first invalidates the economic interpretation of the test payoff.

For multiplicative bounds, instruments alter both payoffs and prices. Multiplying a gross return by an instrument produces a payoff whose price is that instrument, rather than automatically one. Any normalization using an estimated instrument mean must therefore be applied to both sides of the pricing equation. Centering an instrument to mean zero also changes how a scaled payoff should be treated: it need not represent a conventional unit-price gross return. Writing the payoff vector and its price vector explicitly is safer than passing every scaled series to software that assumes identical prices.

Population ordering is a useful diagnostic, but sample ordering is not a theorem for independently estimated curves. If a raw multiplicative curve exceeds an estimated optimal curve, first compare their asset menus, dates, kernel means, and information sets. Then inspect estimation error and conditional-moment specification. A numerical optimizer's failure is another possibility. The paper's own ordering reversal illustrates why automatically sorting the curves or forcing the reported values to obey population inequalities would conceal meaningful evidence.

A modern out-of-sample extension could estimate the conditional-moment model on a training period, freeze a fully specified rule, and evaluate its managed payoffs on later observations. This would make the distinction between feasible strategy construction and favorable in-sample fitting easier to observe. It would still require time-series inference and would not reproduce the paper's same-sample estimates. The contribution of this extension would be robustness to fitting error, whereas the source's analytical bias corrections address a different, explicitly modeled finite-sample mechanism.
