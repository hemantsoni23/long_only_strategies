# VaR and expected shortfall in portfolios of dependent credit risks: Conceptual and practical insights

**Rüdiger Frey and Alexander J. McNeil.** *Journal of Banking & Finance* 26 (2002), 1317–1334. PII S0378-4266(02)00265-0. **Source:** [RiskMeasures_FreyMcNeil2002.pdf](../../Finance/RiskMeasures_FreyMcNeil2002.pdf), 18 pages. The complete paper, Appendix A, four tables, and Figure 1 were inspected. References below use printed pages. The numerical results are controlled model comparisons, not estimates from a historical obligor panel.

## Why this matters

A credit model can match each obligor's default probability and a pairwise correlation while still produce radically different catastrophic portfolio losses. Changing the risk measure from VaR to expected shortfall does not remove this dependence-model uncertainty. Conversely, using an accurate dependence model does not repair VaR's tendency to reward concentrated positions when their default probabilities fall below the quantile threshold.

The paper separates those two problems. First, it constructs a realistic small-bond example in which VaR prefers concentration and shows why optimizing a VaR criterion actively exploits the defect. Second, it expresses several industry credit models as Bernoulli mixtures, making the systematic default-probability distribution the common object of comparison. For a large homogeneous portfolio, the tail of that mixing distribution approximates portfolio VaR and ES directly, avoiding simulation of every obligor.

The practical contribution is a common model language and an asymptotic calculation, supported by two numerical experiments with different calibration constraints. Holding **asset correlation** fixed and holding **default correlation** fixed are different experiments. Confusing them would obscure the paper's main result.

## Loss convention and atom-corrected expected shortfall

Here $L$ denotes a loss, so large positive values are adverse. Capital earns no interest in the basic risk-measure discussion. The parameter $\alpha$ is a high coverage probability, such as 0.99; the adverse-tail probability is $1-\alpha$. Thus the notation runs in the opposite direction from Acerbi's profit-left-tail convention.

The loss quantile is

$$
q_\alpha(L)=\inf\{l:P(L\le l)\ge\alpha\},
\qquad \operatorname{VaR}_\alpha(L)=q_\alpha(L).
$$

For a continuous integrable loss distribution, ES is $E[L\mid L\ge q_\alpha(L)]$. For arbitrary integrable distributions, the paper distinguishes generalized ES:

$$
\operatorname{GES}_\alpha(L)
=\frac{E[L1_{\{L\ge q\}}]+q\{1-\alpha-P(L\ge q)\}}{1-\alpha},
\quad q=q_\alpha(L).
$$

Equivalently, average all losses strictly above $q$ and only enough of the mass at $q$ to fill probability $1-\alpha$. GES is the coherent quantity. A raw conditional expectation beyond a discrete quantile can include too much threshold mass and need not be subadditive. The paper's continuous mixing distributions permit the simpler ES formula in its large-portfolio calculations; the finite default-count distribution remains discrete.

For loss variables, coherence means cash translation $\rho(L+c)=\rho(L)+c$, monotonicity in the loss, positive homogeneity, and subadditivity. Coherence does not guarantee a statistically accurate loss distribution. It does guarantee consistent aggregation of risks evaluated under the same joint model.

## Exact bond example: concentration looks safer to VaR

Section 2.3 specifies 50 independent identically distributed default indicators $Y_i\sim\operatorname{Bernoulli}(0.02)$. Every bond costs 95, pays 100 if it survives, and pays zero on default. Its loss is $L_i=100Y_i-5$, taking values $-5$ with probability 0.98 and 95 with probability 0.02.

Both compared portfolios cost 9,500. Portfolio A holds 100 units of one bond; portfolio B holds two units of each of the 50 bonds. At 95% coverage,

$$
\operatorname{VaR}_{0.95}(L_A)=-500,
$$

because the 2% default event lies beyond the quantile. Portfolio B has $L_B=200M-500$, where $M\sim\operatorname{Binomial}(50,0.02)$. Its 95th-percentile default count is three, so

$$
\operatorname{VaR}_{0.95}(L_B)=200(3)-500=100.
$$

VaR allows a withdrawal of 500 from the concentrated position while requiring 100 of additional capital for the diversified one. Both portfolios have the same expected loss, $-300$, since $E[L_i]=-3$. The counterexample therefore does not arise from different expected profitability or invested amounts.

For a law-invariant coherent measure, subadditivity and homogeneity imply $\rho(2\sum_iL_i)\le100\rho(L_1)=\rho(100L_1)$, so the diversified position cannot receive a larger risk value. This comparison uses a common risk rule and identical marginal bond distributions.

As an explanatory calculation beyond the printed table, generalized 95% ES of A is $[0.02(9500)+0.03(-500)]/0.05=3500$. For B, the exact binomial formula gives approximately 186.053 monetary units:

$$
\operatorname{GES}_{0.95}(L_B)
=200\left[3+\frac{E[(M-3)^+]}{0.05}\right]-500.
$$

These values were calculated from the source's stipulated distribution; they are not empirical estimates or numbers reported by the authors. They illustrate how the corrected tail average recognizes diversification without ignoring the adverse default state.

## Optimizing the defective criterion

Section 2.4 gives a nonnegative, unlevered allocation among cash and the 50 bonds, with fixed initial capital $V$. The criterion is

$$
\max_\theta\{E[-L(\theta)]-\lambda\operatorname{VaR}_\alpha(L(\theta))\},
\qquad \lambda>0.
$$

For a fixed investment in cash, every risky allocation has the same expected loss because the bond prices and expected payoffs are identical. Minimizing VaR therefore determines the risky composition. Concentrating in one name attains the lowest possible loss outcome at the 95% quantile and hence is optimal for this criterion. The conclusion is that concentration is an optimizer, not that it must be the unique optimizer: other sufficiently concentrated allocations can share the same quantile.

There is a small but important algebraic omission in the source's subsequent bond-versus-cash comparison on p. 1323. The text drops $\lambda$ and compares a bond risk-adjusted return with the raw cash return. For the objective as printed, if cash earns deterministic return $r$ and $x$ currency units are placed in the single risky bond, then

$$
L(x)=\frac{x}{95}L_1-r(V-x),
$$

and translation plus homogeneity give

$$
E[-L(x)]-\lambda\operatorname{VaR}_{0.95}(L(x))
=\frac{x(3+5\lambda)}{95}+(1+\lambda)r(V-x).
$$

Thus the endpoint comparison is $(3+5\lambda)/95$ versus $(1+\lambda)r$, under this explicit full-profit-and-loss convention. A different convention excluding cash profits from the penalized loss would yield another threshold, but must be stated. This reconstruction repairs the bookkeeping without changing the paper's concentration argument.

Lemma 2.7 proves that a law-invariant coherent risk measure is minimized, among fully risky portfolios of the same value, by equal investment in the identical names. Appendix A averages an arbitrary weight vector over all permutations. Exchangeability leaves every permuted portfolio's risk unchanged; convexity makes the risk of the averaged vector no larger. The average vector is equal-weighted. Independence is stronger than needed for this symmetry step; exchangeability supplies the distributional invariance.

The lemma does not prove uniqueness, or a strictly interior allocation between cash and the diversified risky portfolio. With a linear mean-minus-homogeneous-risk objective, the remaining cash/risky scale decision can again be an endpoint choice. Its robust implication concerns optimal **risky composition** under symmetry.

## The common Bernoulli-mixture representation

Fix a horizon $[t,t+\Delta t]$, typically one year. All obligors start outside default. Let $W$ be a low-dimensional common factor vector and specify conditional default probabilities $Q_i(W)\in[0,1]$. Conditional on $W$, the indicators $Y_i$ are independent Bernoulli variables:

$$
P(Y_i=1\mid W)=Q_i(W),\qquad
P(Y=y\mid W)=\prod_iQ_i(W)^{y_i}[1-Q_i(W)]^{1-y_i}.
$$

Dependence arises from shared variation in the conditional probabilities. Conditional independence does not imply unconditional independence. The framework models default losses only; rating migration losses are excluded from the experiments even where the named industry model can represent them.

CreditRisk+ is written as $Q_i(W)=1-\exp(-w_i^\top W)$ with independent gamma factors and nonnegative intensity combinations. Its customary Poisson representation allows repeated default counts; taking the event of at least one Poisson arrival gives the Bernoulli probability above for a unit horizon. At low intensities the distinction is small, but the count process and capped default indicator are not identical objects.

CreditMetrics/KMV is generated by Gaussian latent firm variables

$$
X_i=a_i^\top H+\sigma_i\epsilon_i,
\qquad Y_i=1_{\{X_i\le D_i\}},
$$

where $H$ is Gaussian and the standard-normal idiosyncratic shocks are independent of one another and of $H$. Conditional probabilities become $Q_i(H)=\Phi((D_i-a_i^\top H)/\sigma_i)$. The industry labels differ in interpretation and calibration of thresholds and factors, while sharing this conditional probability structure in the stylized comparison.

The extensions replace Gaussian latent dependence by a common scale mixture. With a positive scale variable $W$ independent of the Gaussian factors, the conditional probabilities have the form $\Phi(c_iW-w_i^\top H)$. Choosing $\nu W^2\sim\chi_\nu^2$ yields a Student-$t$ latent model. A common scale must be shared across names to obtain the multivariate-$t$ copula; giving every name an independent scale would define a different dependence model.

CreditPortfolioView uses a logistic rather than a probit link: $Q_i(H)=\operatorname{logistic}(c_i-w_i^\top H)$. The source presents these as simplified representations for comparison, not full reproductions of every operational feature of the industry packages.

## Homogeneous groups and what correlations identify

For a homogeneous group, conditional default probabilities are the same random variable $Q$ for every name. Then $M\mid Q\sim\operatorname{Binomial}(m,Q)$, and

$$
p=E[Q],\qquad p_k=P(Y_1=\cdots=Y_k=1)=E[Q^k].
$$

For distinct names,

$$
\operatorname{Cov}(Y_i,Y_j)=\operatorname{Var}(Q),\qquad
\rho_Y=\frac{E[Q^2]-p^2}{p(1-p)}.
$$

Matching $p$ and $\rho_Y$ fixes the first two moments of $Q$. It does not fix higher joint-default probabilities or the extreme tail of $Q$. A two-parameter mixing family is pinned down by those two moments within that family, but competing families can remain materially different.

The homogeneous distributions are: transformed gamma $Q=1-e^{-Y}$ with $Y\sim\operatorname{Gamma}(a,b)$ using **rate** $b$; probit-normal $Q=\Phi(Z)$ with $Z\sim N(\mu,\sigma^2)$; and logit-normal $Q=\operatorname{logistic}(Z)$ with normal $Z$. For the Gaussian latent model, the common **asset** correlation is $\rho=\sigma^2/(1+\sigma^2)$, which is not $\rho_Y$.

The transformed-gamma density is

$$
g(q)=\frac{b^a}{\Gamma(a)}[-\log(1-q)]^{a-1}(1-q)^{b-1},\quad0<q<1.
$$

For small $q$, replacing $-\log(1-q)$ by $q$ makes its shape close to a beta density. The paper describes this approximation as essentially equivalent in the relevant low-default region. It is not an exact identity; substituting a beta distribution in extreme-tail calculations changes the model and should be recorded.

## Experiment 1: hold default probabilities and asset correlations fixed

Tables 1–2 use 1,000 obligors, each with default probability 5%, and unit loss given default. Group 1 has latent asset correlation 10%; Group 2 has 20%. The authors compare Gaussian, multivariate-$t_{10}$, and multivariate-$t_5$ latent models, with one million Monte Carlo replications per reported comparison. Loss is the number of defaults and has expectation 50 in every case.

A direct reconstruction draws a common standard normal $H$, independent idiosyncratic normals $\epsilon_i$, and forms $A_i=\sqrt\rho H+\sqrt{1-\rho}\epsilon_i$. In the Gaussian case default occurs at $A_i\le\Phi^{-1}(0.05)$. In the $t_\nu$ case use $A_i/\sqrt{S/\nu}$ with common independent $S\sim\chi_\nu^2$ and default threshold $t_\nu^{-1}(0.05)$. Since $\nu>2$, its linear correlation remains $\rho$. Equivalently, draw the common factors and then one binomial count conditional on their default probability; this avoids explicitly generating 1,000 idiosyncratic normals.

| Group | Risk | Gaussian | $t_{10}$ | $t_5$ |
|---|---|---:|---:|---:|
| 1 | 99% VaR | 170 | 255 | 320 |
| 1 | 99.9% VaR | 242 | 384 | 482 |
| 2 | 99% VaR | 250 | 327 | 389 |
| 2 | 99.9% VaR | 386 | 512 | 600 |

These are reported simulated counts rounded to the nearest unit. Group 1's 99.9% VaR nearly doubles from 242 to 482 when Gaussian dependence is replaced by $t_5$, despite unchanged expected defaults and asset correlation. Group 2's corresponding loss rises from 38.6% to 60.0% of the unit-exposure portfolio.

The source does not report random seeds, quantile interpolation choices, repeated simulation runs, or confidence intervals. At the 99.9th percentile, one million independent replications leave roughly 1,000 draws in the nominal exceedance tail. That is a useful count, not a money-denominated quantile standard error; translating probability uncertainty to loss uncertainty depends on the local discrete distribution. Exact last-unit reproduction should not be claimed without the missing simulation inputs.

## Large-portfolio limit and its assumptions

Let $L^{(m)}=\sum_{i=1}^mE_iY_i$, where exposures have finite mean $\mu_E$ and finite variance. Under the natural independent-exposure interpretation, conditional laws of large numbers give

$$
\frac{L^{(m)}}m\longrightarrow\mu_EQ.
$$

The source's abbreviated statement introduces iid exposures but does not explicitly spell out their independence from the common factors and default indicators. That independence, or an equivalent conditional-mean restriction, is needed for the limit to equal the **constant** $\mu_E$ times $Q$. With systematic exposure or recovery dependence, the limit can instead be a different conditional expected loss. Unit exposures in the numerical examples avoid this ambiguity.

Proposition 3.2 imposes regularity at the chosen mixing-distribution quantile, expressed by $G(q_\alpha(Q)+\delta)>\alpha$ for every $\delta>0$. Its applications use strictly positive continuous mixing densities, avoiding both quantile gaps and threshold atoms. Then

$$
\operatorname{VaR}_\alpha(L^{(m)})\approx m\mu_Eq_\alpha(Q),
\qquad
\operatorname{ES}_\alpha(L^{(m)})\approx m\mu_EE[Q\mid Q\ge q_\alpha(Q)].
$$

The convergence statements are exact limits; using them at $m=1000$ is an approximation. These formulas remove idiosyncratic sampling variation, not systematic default uncertainty. For unit exposures, conditional default-rate variance is $Q(1-Q)/m$, while unconditional systematic variance approaches $\operatorname{Var}(Q)$. Diversification therefore does not drive total default-rate uncertainty to zero.

For continuous $Q$ supported in $[0,1]$,

$$
E[Q\mid Q\ge q_\alpha]
=q_\alpha+\frac1{1-\alpha}\int_{q_\alpha}^{1}[1-G(q)]\,dq.
$$

The printed upper integration limit is infinity, which is equivalent because the survival function is zero above one. With an atom at the threshold, use the generalized ES formula rather than the raw conditional average. Concentrated exposures, heterogeneous probabilities, or factor-dependent loss given default require additional work; the displayed homogeneous approximation does not cover them automatically.

## Separating finite-portfolio error from mixing-model error

For a unit-exposure homogeneous group, the exact finite default-count distribution is itself a one-dimensional mixture:

$$
P(M=k)=\binom mk\int_0^1q^k(1-q)^{m-k}\,dG(q),
\qquad k=0,\ldots,m.
$$

Thus a deterministic quadrature implementation can compute the finite CDF, select the smallest integer $k_\alpha$ with cumulative probability at least $\alpha$, and calculate generalized ES through

$$
\operatorname{GES}_\alpha(M)
=k_\alpha+\frac{E[(M-k_\alpha)^+]}{1-\alpha}.
$$

These formulas are direct consequences of the paper's Bernoulli-mixture setup. They provide an optional independent check on simulation and on the asymptotic approximation; they are not claimed as calculations performed in the reported tables. For $m=1000$, avoid direct products of large binomial coefficients and very small powers: use a stable binomial-probability recurrence or log probabilities, and integrate over the mixing variable's natural normal or gamma coordinate where appropriate.

The variance decomposition clarifies why the approximation improves while model uncertainty remains. Since $E[M\mid Q]=mQ$ and $\operatorname{Var}(M\mid Q)=mQ(1-Q)$,

$$
\operatorname{Var}(M/m)=\operatorname{Var}(Q)+\frac{E[Q(1-Q)]}{m}.
$$

The second term disappears with granularity, but the first persists. A model can have a small finite-name correction and still have a badly wrong tail because its $G$ is wrong. Comparing a simulation with its own large-portfolio limit validates the approximation inside that model; it does not validate the model against competing dependence laws.

For unit exposures the normalized loss is bounded by one, which supplies uniform integrability for tail-average convergence once the required distribution and quantile conditions hold. With random exposures, finite second moments and the appropriate independence conditions control the remaining sampling component. Neither argument says that a fixed finite book with one dominant obligor is well approximated by a homogeneous infinitely granular limit. The relevant concentration diagnostics belong to the exposure distribution, not merely to the number of account records.

## A reconstructible moment-calibration procedure

For the probit-normal model, a Gaussian one-factor parameterization with default probability $p$ and asset correlation $\rho$ gives

$$
\mu=\frac{\Phi^{-1}(p)}{\sqrt{1-\rho}},\qquad
\sigma=\sqrt{\frac\rho{1-\rho}},\qquad
q_\alpha(Q)=\Phi(\mu+\sigma\Phi^{-1}(\alpha)).
$$

Its second moment is $\int\Phi(\mu+\sigma z)^2\varphi(z)dz$. For logit-normal mixing, solve the two equations $\int\operatorname{logistic}(\mu+\sigma z)^k\varphi(z)dz=p_k$ for $k=1,2$, constraining $\sigma>0$, and use the same transformed-normal quantile formula with the logistic function.

For transformed-gamma mixing, the moments follow from the gamma Laplace transform:

$$
p=1-\left(\frac b{b+1}\right)^a,
\qquad
p_2=1-2\left(\frac b{b+1}\right)^a+
\left(\frac b{b+2}\right)^a.
$$

Solve for $a,b>0$, then invert the gamma CDF and transform with $1-e^{-y}$ to obtain $q_\alpha(Q)$. Its survival function is the gamma survival probability at $-\log(1-q)$. For each model, integrate its survival function above the quantile and multiply by $m\mu_E$.

These equations supply a reconstruction algorithm; the authors do not tabulate the fitted mixing parameters, integration tolerances, or root-finding settings. Use survival functions directly near one to avoid catastrophic cancellation from computing one minus a nearly unit CDF. Verify both calibrated moments after solving and distinguish numerical quadrature error from the large-portfolio approximation error.

## Experiment 2: hold default correlations fixed

Tables 3–4 fix $p=0.05$ and match default dependence rather than latent asset correlation. Group 1 reports $p_2=0.0037$ and $\rho_Y=0.0255$; Group 2 reports $p_2=0.0052$ and $\rho_Y=0.0578$. These rounded columns are not algebraically exact to all displayed digits. For precise replication, the text identifies the corresponding Gaussian groups as those with asset correlations 0.10 and 0.20; one can compute their unrounded second moments and use them as calibration targets. That is an explicit reconstruction choice, not an unreported table of author parameters.

The portfolio again has 1,000 unit exposures. Risk is estimated from mixing-distribution quantiles and tail integrals rather than by the million-replication Monte Carlo procedure of Table 2.

| Group | Risk | CreditRisk+ | KMV/CreditMetrics | CreditPortfolioView |
|---|---|---:|---:|---:|
| 1 | 99% VaR | 162 | 169 | 175 |
| 1 | 99.9% VaR | 218 | 241 | 265 |
| 1 | 99% ES | 186 | 200 | 214 |
| 1 | 99.9% ES | 241 | 271 | 301 |
| 2 | 99% VaR | 237 | 250 | 268 |
| 2 | 99.9% VaR | 340 | 384 | 445 |
| 2 | 99% ES | 282 | 308 | 344 |
| 2 | 99.9% ES | 380 | 439 | 514 |

Values are reported rounded loss units. Model dispersion is smaller than in the asset-correlation comparison but remains material in the far tail. Group 2's 99.9% ES ranges from 38.0% to 51.4% of total unit exposure. Figure 1 plots the three mixing survival functions on a logarithmic vertical axis; separation becomes pronounced beyond the 99th percentile. Its caption refers to Group 1 in Table 1 while mentioning first and second default moments; the corresponding moments are in Table 3, as explained in the text.

The Gaussian asymptotic VaR values of 169 and 241 versus simulated values of 170 and 242 in Group 1 illustrate that finite-portfolio and limiting calculations are close here but not identical. No universal error bound is supplied. The results do not say that one named industry model is always most conservative: the ordering shown depends on the stipulated calibration, portfolio homogeneity, and tail level.

## Reproduction boundary and takeaway

A faithful replication has three separate parts: the exact 50-bond counterexample and permutation argument; the finite 1,000-name Gaussian versus $t$ simulation under common asset-correlation targets; and the asymptotic mixing-distribution comparison under common default-correlation targets. They use different mathematical inputs and must not be merged into one generic “correlation-controlled” test.

The paper does not estimate default probabilities, correlations, or recoveries from data, and provides no sample dates, rating exclusions, lagging scheme, validation window, transaction costs, or forecasting exercise. These omissions reflect the controlled design. Actual credit implementation would additionally need a calibration population, horizon-consistent probabilities, exposure and recovery dependence, concentration diagnostics, and parameter uncertainty.

The key conclusion is twofold: optimizing VaR can exploit a failure of the risk statistic itself, while measuring a coherent tail average remains vulnerable to an incorrect dependence model. Bernoulli mixtures make the latter vulnerability observable by exposing the distribution of systematic conditional default probabilities. Matching two moments is a calibration constraint, not an identification theorem for extreme credit losses.
