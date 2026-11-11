# Model Risk in Portfolio Optimization

David Stefanovits, Urs Schubiger, and Mario V. Wüthrich. *Risks* 2 (2014), 315–348, published August 6, 2014. DOI: 10.3390/risks2030315. The library filename incorrectly suggests “Stepanov” and 2019; the title page establishes the authors and 2014 identity. [Source PDF](../../Finance/ModelRisk_Stepanov_2019.pdf). All 34 pages were read, including the proofs, Wishart appendix, complete equity universe, and references. References below use PDF pages; add 314 for printed journal pagination.

## Why this matters

Optimizing an estimated objective selects portfolios that exploit estimation errors. An unbiased covariance matrix or unbiased expected-return vector therefore does not make the optimized portfolio’s estimated utility unbiased. This paper quantifies that optimism directly: how much better does the chosen portfolio look under its fitted inputs than under the true objective? It derives a finite-sample formula for unconstrained mean–variance optimization, extends the analysis beyond Gaussian marginal returns, and proposes covariance-eigenvalue adjustments intended to reduce the gap.

Three distinctions determine how to use the results. First, the proposed loss is forecast optimism, not the opportunity cost relative to an oracle portfolio. Second, the non-Gaussian theorem uses a single latent scale shared by all observations in a sample. Third, the individual-eigenvalue guarantee assumes known eigenvectors and independence conditions that do not hold automatically for a sample covariance matrix. The empirical procedure relaxes those assumptions and is supported by a historical illustration, not by a general dominance theorem.

The practical contribution is an explicit link between optimized portfolios and inverse covariance moments. Small sample eigenvalues receive special attention because inverses amplify their errors. The paper complements covariance estimators designed to minimize matrix-estimation loss: a matrix can be unbiased while producing severely optimistic optimized performance. Its results motivate validating the portfolio decision, rather than treating accurate-looking average covariance entries as sufficient evidence.

## Objective and the definition of model risk

For a true utility function $U$ and feasible set $A$, define the unique optimal portfolio $w^*=\arg\max_{w\in A}U(w)$. The investor observes $m$ return vectors and constructs estimates $\widehat U$ and possibly $\widehat A$, then chooses $\widehat w=\arg\max_{w\in\widehat A}\widehat U(w)$. The paper’s loss is

$$
L(U,\widehat U,\widehat A)=E[\widehat U(\widehat w)-U(\widehat w)].
$$

The expectation averages over estimation samples. It is not the realized loss on a particular future day. Positive $L$ means the fitted objective overstates the true utility of the selected portfolio. Negative $L$ is possible in the general definition, especially after deliberately biasing the inputs. The familiar oracle regret is instead

$$
L^{\mathrm{oracle}}=E[U(w^*)-U(\widehat w)].
$$

When the feasible set is known and fixed and $E[\widehat U(w)]=U(w)$ for every deterministic $w$, Proposition 1 proves $L\geq0$, strictly when the estimated optimum differs from the unique true optimum with positive probability. The proof uses two inequalities: $U(w^*)\geq U(\widehat w)$, and $\widehat U(\widehat w)\geq\widehat U(w^*)$. Taking expectations of the second inequality and applying unbiasedness at the fixed $w^*$ gives $E\widehat U(\widehat w)\geq U(w^*)$. Consequently

$$
L=L^{\mathrm{oracle}}+E[\widehat U(\widehat w)]-U(w^*)\geq L^{\mathrm{oracle}}.
$$

The excess term captures selection optimism. The result does not automatically apply to an estimated expected-return constraint, since that makes $\widehat A$ random, or to the deliberately biased covariance estimators introduced later.

The main analytical objective is $U(w)=\mu'w-\kappa w'\Sigma w$, with $\kappa>0$, positive-definite $\Sigma$, and unrestricted $w\in\mathbb R^n$. Its optimizer is $w^*=(2\kappa)^{-1}\Sigma^{-1}\mu$. There is no full-investment constraint in this theorem, so scaling all risky weights changes total exposure. For linear constraints $A'w=a$, the source supplies the usual constrained solution:

$$
w^*=\frac{1}{2\kappa}\left[\Sigma^{-1}-\Sigma^{-1}A(A'\Sigma^{-1}A)^{-1}A'\Sigma^{-1}\right]\mu+\Sigma^{-1}A(A'\Sigma^{-1}A)^{-1}a.
$$

Other numerical examples maximize negative variance, minimize squared differences between variance contributions $RC_i=w_i(\Sigma w)_i$, or maximize the diversification ratio $(\sum_iw_i\sqrt{\Sigma_{ii}})/\sqrt{w'\Sigma w}$. Their utility scales differ, so raw loss magnitudes cannot establish a cardinal welfare ranking across those problems.

## The sampling model: one common variance multiplier

Equation (4) specifies

$$
R_i=\mu+\sqrt W\,\Sigma^{1/2}Z_i,\qquad i=1,\ldots,m,
$$

where the $Z_i$ are independent standard multivariate Gaussians and $W>0$ is independent of all of them, with $E[W]=1$. Crucially, there is one $W$, not independent $W_i$ for each observation. Conditional on $W$, the sample is i.i.d. Gaussian with covariance $W\Sigma$; unconditionally the observations are dependent through their shared volatility state. Each observation has mean $\mu$ and covariance $\Sigma$, but observing a very long sample reveals the realized $W\Sigma$, not necessarily the unconditional $\Sigma$.

This structure permits heavy-tailed marginals, cross-asset tail dependence, and non-Gaussian samples while preserving conditional Wishart calculations. It is a persistent random-scale environment. The paper’s continuous-time illustration uses a random clock $T(t)=Wt$, again preserving the same scale through time. Calling the two-point example a regime-switching model should not be read as a Markov chain that switches within the estimation sample.

The examples are Gaussian $W=1$; a two-point mixture with probabilities $p,1-p$ and values $x_1,x_2=(1-px_1)/(1-p)$; and a standardized Student‑t mixture $W=(\nu-2)/V$, where $V\sim\chi^2_\nu$ and $\nu>2$. The last has covariance $\Sigma$, rather than the unscaled Student‑t covariance inflation. Define $a_1=E[W^{-1}]$ and $a_2=E[W^{-2}]$. Then

$$
(a_1,a_2)=\left(\frac{\nu}{\nu-2},\frac{\nu(\nu+2)}{(\nu-2)^2}\right)
$$

for Student‑t, and $a_j=p/x_1^j+(1-p)/x_2^j$ for the two-point case. Finite negative moments are needed for finite losses; $E[W]=1$ alone does not ensure them.

Use $\widehat\mu=m^{-1}\sum_iR_i$ and the sample covariance with divisor $m-1$. Conditional on $W$,

$$
\widehat\mu\mid W\sim N(\mu,W\Sigma/m),\qquad (m-1)\widehat\Sigma\mid W\sim\mathcal W_n(W\Sigma,m-1),
$$

and the two estimators are conditionally independent. Remark 7 on PDF page 10 accidentally omits $W$ from the Wishart scale; Appendix 1.2 on page 25 gives the correct $W\Sigma$ and uses it in the proof. This is a source correction supported by its own derivation. Conditional independence should not be replaced with unconditional independence in the mixture case.

## Finite-sample theorem and what drives the loss

Write $S=\mu'\Sigma^{-1}\mu$ and

$$
\alpha(d,n)=\frac{d}{d-n-1},\qquad \beta(d,n)=\frac{d(d-1)}{(d-n)(d-n-3)}.
$$

For $m>n+4$, Theorem 2 gives

$$
L=\frac{\alpha(m-1,n)}{4\kappa}\left\{\frac nm[1+\beta(m-1,n)a_1]+[\beta(m-1,n)a_2-a_1]S\right\}.
$$

The dimension/sample ratio and inverse-moment multipliers quantify distinct amplification channels. Positive definiteness only needs $m>n$; finite second inverse-Wishart moments require the stronger theorem condition. Being able to numerically invert the matrix does not mean the expected optimized loss is finite.

To reconstruct the proof, substitute $\widehat w=(2\kappa)^{-1}\widehat\Sigma^{-1}\widehat\mu$ into the loss:

$$
4\kappa L=E[\widehat\mu'\widehat\Sigma^{-1}\widehat\mu]-2\mu'E[\widehat\Sigma^{-1}\widehat\mu]+E[\widehat\mu'\widehat\Sigma^{-1}\Sigma\widehat\Sigma^{-1}\widehat\mu].
$$

Conditional inverse-Wishart identities give $E[\widehat\Sigma^{-1}\mid W]=\alpha W^{-1}\Sigma^{-1}$ and $E[\widehat\Sigma^{-1}\Sigma\widehat\Sigma^{-1}\mid W]=\alpha\beta W^{-2}\Sigma^{-1}$. The three terms are respectively $\alpha(n/m+a_1S)$, $\alpha a_1S$, and $\alpha\beta[(n/m)a_1+a_2S]$. This both derives the formula and exposes the role of the common scale.

Jensen’s inequality gives $a_2\geq a_1^2\geq a_1\geq1$. Hence the Gaussian case minimizes the loss within this class, and nonconstant $W$ raises it. For fixed $n$ and increasing $m$,

$$
L\longrightarrow\frac{a_2-a_1}{4\kappa}S.
$$

The limit is positive for nonconstant scale and nonzero $\mu$. The paper’s wording that it is strictly positive in every non-Gaussian case needs this nonzero-signal qualification; when $\mu=0$, $S=0$ and the fixed-dimension limit is zero. More fundamentally, the persistent limit reflects the common-scale sampling assumption. It should not be cited as proof that all i.i.d. Student‑t estimation error remains irreducible with unlimited data.

When $n,m$ grow with $n/m\to c\in(0,1)$, $\alpha\to(1-c)^{-1}$ and $\beta\to(1-c)^{-2}$. Substituting those limits leaves a positive dimension-related component even in the Gaussian case. A numerical limit for the signal term additionally requires a controlled sequence of $S$ values. As $c$ approaches one, the expression diverges, reflecting the instability of an almost singular empirical covariance matrix.

## Covariance adjustment: guarantees and limits

Let $\widehat\Sigma=\widehat T\operatorname{diag}(\widehat\lambda_1,\ldots,\widehat\lambda_n)\widehat T'$ with ascending eigenvalues. The proposed family is

$$
\widehat\Sigma_C=\widehat T\operatorname{diag}(c_1\widehat\lambda_1,\ldots,c_n\widehat\lambda_n)\widehat T',\qquad c_i>0.
$$

This preserves positive definiteness and the estimated eigenvectors. It need not preserve the ordering of adjusted eigenvalues. The covariance representation remains valid without reordering, provided eigenvalue factors stay paired with their original eigenvectors.

Proposition 3 uses a common factor

$$
\overline c=\beta(m-1,n)\frac{a_2}{a_1}\geq1.
$$

It reduces the proposed loss relative to the unadjusted estimator in the unconstrained mixture model. Explicitly,

$$
L(\overline c)=\frac{\alpha}{4\kappa}\left\{\frac nm\left[\frac1{\overline c}+\frac{\beta a_1}{\overline c^2}\right]+\left[\frac{\beta a_2}{\overline c^2}-\frac{a_1}{\overline c}\right]S\right\}.
$$

The chosen factor cancels the coefficient on $S$ and reduces the remaining terms. Appendix 1.5’s intermediate expanded expression drops the overall $1/(4\kappa)$; the adjacent formulas and Proposition 3 retain it. The expression here restores that algebraic factor.

Uniform scaling is equivalent to raising risk aversion and reducing all unconstrained risky weights by $1/\overline c$. It does not improve their relative composition. Nor is this factor presented as the global minimizer of every economically meaningful loss. In fact, making $\overline c$ arbitrarily large drives weights and this optimism measure toward zero while foregoing investment opportunities. A lower optimism gap alone is not proof of higher true expected utility. The empirical fully invested experiment avoids an all-cash solution, but the theorem does not transfer unchanged to that constraint.

A heuristic alternative sets $c_k=\lambda_k/E[\widehat\lambda_k]$, making each adjusted ordered eigenvalue unbiased in the oracle simulation. The analytically motivated individual rule is

$$
c_k=\lambda_k\frac{E[\widehat\lambda_k^{-2}]}{E[\widehat\lambda_k^{-1}]}.
$$

Theorem 5 proves improvement under additional assumptions: true eigenvectors $T$ are known; $\widehat\Sigma=T\widehat\Lambda T'$; the eigenvalue estimates are independent of the unbiased mean estimate; and the covariance estimator is unbiased. Let $b_k=(T'\widehat\mu)_k$. Under these assumptions,

$$
L_C=\frac1{2\kappa}\sum_k c_k^{-1}\operatorname{Var}(b_k)E[\widehat\lambda_k^{-1}]+\frac1{4\kappa}\sum_kE[b_k^2]\left[c_k^{-2}\lambda_kE[\widehat\lambda_k^{-2}]-c_k^{-1}E[\widehat\lambda_k^{-1}]\right].
$$

The chosen factor makes each square-bracket term vanish. Unbiased eigenvalues and Jensen imply $c_k\geq1$, yielding the comparison with $c_k=1$. This proof does not establish dominance when sample eigenvectors are estimated, when mean and eigenvalues have residual dependence, or when factors themselves are estimated. Section 5 deliberately tests an extension beyond the theorem’s assumptions.

For arbitrary estimated eigenvectors, Theorem 4 can be implemented more compactly by setting $B=\widehat\Sigma_C^{-1}$ and computing

$$
L_C=\frac1{4\kappa}E[\widehat\mu'B\widehat\mu-2\mu'B\widehat\mu+\widehat\mu'B\Sigma B\widehat\mu].
$$

This equivalent matrix expression includes eigenvector error and avoids transcription mistakes in the source’s longer projection expansion. Appendix 1.6 also omits some $1/(2\kappa)$ factors in intermediate projection identities; the final theorem and direct substitution above give the correct normalization.

## Simulation design and numerical checks

Section 5.1 uses $n=50$, true $\mu,\Sigma$ equal to full-period sample estimates from the equity data described below, and independent replications of entire $m$-observation samples. Unconstrained mean–variance uses $\kappa=1$. Sample sizes include 62, 75, 100, 150, and 200. The Gaussian, two-point $(p=0.1,x_1=5,x_2=5/9)$, and Student‑t $(\nu=3)$ models are compared. A faithful replication draws one $W$ per sample, then $m$ independent Gaussian vectors conditional on it. Redrawing $W$ every day tests a different model and will not reproduce Theorem 2.

Figure 1 varies replications from 500 to 10,000 at $m=100$. Its theoretical losses are 1.3814, 2.1236, and 3.8453 for Gaussian, two-point, and Student‑t respectively. Figures 4–12 generally use 1,000 replications. The simulated adjustment factors in those figures use oracle distributional inputs; they should not be confused with the rolling estimated factors in the empirical test.

An independent scalar consistency check gives $\alpha=2.0625$, $\beta=4.3043478$, and mixture inverse moments $(1.64,2.92)$ versus Student‑t moments $(3,15)$. Using the rounded Gaussian loss to infer $S\approx0.0081423$ reproduces the other losses as 2.123627 and 3.845429, consistent with source rounding. This is an internal formula check, not independent recovery of the unpublished full-period covariance matrix. The common adjustment factors are 4.30435, 7.66384, and 21.52174; their analytically adjusted losses are 0.119792, 0.064626, and 0.019167. These agree with the ordering and scale of the adjustment figures.

The source also computes long-only, fully invested minimum-variance, equal-risk-contribution, and maximum-diversification portfolios. Their losses decrease with sample size and appear less sensitive to the mixture law. No expected-return estimate enters those three objectives. However, both the constraints and objective differ from unconstrained mean–variance, and each utility has different units. The experiment does not isolate mean estimation as the only reason for the contrast. Figures 10–12 display losses around $10^{-5}$, $10^{-10}$, and $10^{-1}$ respectively; those orders of magnitude are not directly comparable measures of economic importance.

## Rolling equity experiment and reproducibility

Section 5.2 uses 4,380 daily total-return observations, including dividends, for 50 U.S. large-cap stocks from January 2, 1995 through October 14, 2011. Appendix 3 lists the exact universe, in order: WFC, JPM, C, BAC, AXP, AIG, PNC, GE, UTX, MMM, CAT, BA, UNP, HON, WMT, MCD, CMCSA, DIS, HD, CVS, COST, AAPL, MSFT, IBM, ORCL, INTC, HPQ, EMC, XOM, CVX, SLB, COP, OXY, APC, APA, PG, KO, PEP, MO, CL, F, NKE, KMB, JNJ, PFE, MRK, ABT, BMY, AMGN, and UNH. These are historical source identifiers, not instructions to substitute present-day tickers or successor companies.

Every trading day uses the preceding 100 observations to estimate the mean and covariance. Portfolios are long only and fully invested, with $\kappa=100$, making variance relatively influential. The five strategies are the sample-covariance baseline; uniform Gaussian scaling; uniform Student‑t scaling; individually adjusted Gaussian eigenvalues; and individually adjusted Student‑t eigenvalues. All retain the sample mean. The uniform strategies thus also change the balance between expected returns and risk under the full-investment constraint, rather than merely scaling a fixed relative allocation.

For each individual-adjustment date, regard the current sample covariance as the true simulation covariance, calibrate the chosen mixture model, and simulate $N=1000$ samples of 100 returns. Sort each simulated covariance’s eigenvalues increasingly and calculate

$$
\widehat c_i=\widehat\lambda_i\frac{\sum_{j=1}^{1000}(\widehat\lambda_i^{(j)})^{-2}}{\sum_{j=1}^{1000}(\widehat\lambda_i^{(j)})^{-1}}.
$$

Apply those factors to the current sample eigensystem, solve the constrained quadratic program, and hold the resulting weights over the subsequent return interval. This is a nested parametric simulation procedure. The source says it calibrates a Student‑t model but does not specify the degrees-of-freedom estimator, bounds, rolling versus fixed calibration details, random seeds, or solver tolerances. The simulation’s $\nu=3$ is explicitly stated for Section 5.1; treating it as the Section 5.2 fitted value would invent an input. These omissions prevent exact recreation of the daily weights from the PDF alone.

The stock-selection date and eligibility rule are also absent. A fixed list of companies with a long return history is not a documented point-in-time investable universe and may contain survival or selection effects. The source does not describe delisting treatment, corporate-action series construction, missing observations, or precisely how the initial 100-day burn-in maps to the partial 1995 table row. There are no turnover penalties, bid–ask spreads, commissions, market impact, or tax deductions in the reported objective or performance.

Tables 1–2 give the following full-period results, annualizing return and volatility with 250 trading days:

| Strategy | Return % | Volatility % | Reported Sharpe | Maximum drawdown % | Average turnover % | Average diversification |
|---|---:|---:|---:|---:|---:|---:|
| Sample covariance | 7.63 | 15.06 | 0.51 | 47.80 | 13.38 | 10.05 |
| Uniform Gaussian | 8.03 | 15.01 | 0.53 | 47.16 | 12.78 | 10.10 |
| Uniform Student‑t | 8.66 | 15.00 | 0.58 | 45.31 | 12.25 | 10.15 |
| Individual Gaussian | 7.64 | 14.74 | 0.52 | 45.43 | 11.40 | 11.78 |
| Individual Student‑t | 9.34 | 14.55 | 0.64 | 41.17 | 9.55 | 12.13 |

The best reported variant increases annual return by 1.71 percentage points and lowers volatility by 0.51 points relative to baseline. Its 2008 return is −20.81% versus −27.67%, but it underperforms in other years: 18.27% versus 22.10% in 2009 and 7.85% versus 9.13% in 2010. The evidence is historical and gross. No standard errors, bootstrap confidence intervals, multiple-comparison correction, or formal performance-difference test accompany the tables; “significant improvement” in the prose is not documented statistical significance.

Metric definitions deserve particular care. Remark 14 constructs additive cumulative P&L, $p_1=1$ and $p_t=p_{t-1}+w_{t-1}'r_t$. Drawdown is $\max_{k\leq t}p_k-p_t$, and maximum drawdown is its largest value. This is not a compounded-wealth percentage drawdown normalized by the running peak. The reported Sharpe values numerically match annualized return divided by volatility; no explicit risk-free subtraction is supplied. A replication should preserve these source conventions before presenting conventional alternatives.

Turnover is $\sum_i|w_{t,i}-w_{t-1,i}|$, without a factor of one-half and without adjusting old weights for intervening price moves. It measures changes in target weights, not exact executed turnover. Average diversification is the time average of $(\sum_iw_{t,i}^2)^{-1}$, an effective number of holdings, distinct from the maximum-diversification objective’s volatility ratio. Lower target-weight turnover is encouraging but cannot substitute for a cost model.

## Research interpretation

The analytical result is strongest as a warning about optimization-induced optimism and inverse covariance moments. The covariance adjustment provides a tractable way to moderate it, especially when dimension is large relative to the estimation window. The empirical exercise suggests that individual eigenvalue corrections can alter concentration and turnover even when realized volatility changes only modestly.

For deployment, the missing mixture-calibration specification, uncertain universe selection, nonstandard drawdown convention, and lack of cost or inference analysis are material. A faithful extension should report both the paper’s optimism loss and oracle or realized utility, use point-in-time data, distinguish common-scale and independently mixed sampling experiments, and compare against explicit shrinkage and simple-allocation baselines. The paper supplies neither a universal superiority result over modern covariance estimators nor a net-return estimate. Its durable contribution is to make the interaction between parameter uncertainty and the optimizer mathematically visible.
