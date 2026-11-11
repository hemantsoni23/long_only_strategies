# Temporal Aggregation of GARCH Processes

Feike C. Drost and Theo E. Nijman, *Econometrica* 61(4), July 1993, 909–927. [Original PDF](../../Finance/garchaggregation_1993.pdf). The local file has 20 pages including a JSTOR cover; the article and its mathematical appendix occupy PDF pages 2–20. All pages were read. Equations, the aggregation diagrams, Tables I–IV, and the appendix's moment conditions were also checked visually.

## Why this matters

Changing a return sampling interval changes the statistical object being modeled. A daily GARCH model does not become a weekly model by multiplying its conditional variance by five, and an independent standardized innovation at one frequency need not remain independent at another. Drost and Nijman identify a class of **weak GARCH models** that is closed under temporal aggregation, derive explicit GARCH(1,1) transformations, and explain how higher frequency information can identify lower frequency volatility dynamics more precisely than a short low frequency sample.

The distinction between a linear projection and a conditional expectation is central. The aggregation formulas describe the best linear predictor of squared observations from a specified history. They do not generally deliver the full conditional variance given every measurable function of that history, or a likelihood with independent Gaussian or Student innovations. The paper supplies counterexamples to both stronger claims. Its exchange-rate exercise illustrates parameter transformations rather than conducting an out-of-sample trading or risk-management experiment.

## Three definitions and the information they retain

The paper's order convention is GARCH$(p,q)$ with $p$ lags of the variance and $q$ lags of squared innovations. This reverses conventions found in some software. Let $L$ be the lag operator, let $y_t$ be a zero-mean innovation with a finite fourth moment, and write

$$
B(L)h_t=\psi+[A(L)-1]y_t^2,\qquad
A(L)=1+\sum_{i=1}^{q}\alpha_iL^i,\qquad B(L)=1-\sum_{i=1}^{p}\beta_iL^i.
$$

The usual nonnegative coefficient restrictions and a stable variance recursion are convenient sufficient restrictions. The source discusses weaker restrictions through the coefficients of $B(L)^{-1}[A(L)-1]$; nonnegative individual coefficients are not a necessary characterization of every valid model. Stability of the polynomials and existence of the required moments are assumptions, not consequences of calling a model GARCH.

A **strong** model has $y_t=\sqrt{h_t}\xi_t$ with independent, identically distributed $\xi_t$, mean zero and variance one. A **semistrong** model instead requires $E(y_t\mid\mathcal F_{t-1})=0$ and $E(y_t^2\mid\mathcal F_{t-1})=h_t$, where $\mathcal F_{t-1}$ is the complete past. Standardized innovations need not be independent. A **weak** model requires only

$$
P(y_t\mid\mathcal H_{t-1})=0,\qquad P(y_t^2\mid\mathcal H_{t-1})=h_t,\qquad
\mathcal H_{t-1}=\operatorname{span}\{1,y_{t-j},y_{t-j}^2:j\ge1\},
$$

where $P$ denotes the mean-square linear projection. Thus $y_t^2-h_t$ is orthogonal to the listed regressors. Orthogonality to this linear span does not mean orthogonality to every nonlinear function of past observations. Strong implies semistrong implies weak; the converse implications fail.

The results also use symmetry or suitable mixed-moment restrictions. For implementation, the appendix's explicit version is more informative than a generic statement about symmetric marginal distributions:

$$
E[y_ty_{t-i}y_{t-j}]=0\quad(0\le i\le j),
$$

$$
E[y_ty_{t-i}y_{t-j}y_{t-k}]=0
\quad(0\le i\le j\le k,\ i\ne0\ \text{or}\ j\ne k).
$$

These conditions eliminate third moments and fourth cross-products other than paired-square configurations. Marginal symmetry by itself is not a sufficient operational check on all such joint moments. A replication should verify the actual mixed moments required by the proof rather than infer them from a symmetric histogram.

Two aggregation operations are different. **Stocks** mean retaining $y_{mk}$ at every $m$th date; the word does not mean equity securities. **Flows** mean nonoverlapping sums $Y_k=\sum_{i=0}^{m-1}y_{mk-i}$. Returns over a longer holding interval are flow aggregates when one-period returns add, as log returns do. Arithmetic simple returns compound and require a separate approximation before these sums describe them.

## GARCH(1,1): common quantities and moment existence

Write the fine-frequency recursion as

$$
h_t=\psi+\alpha y_{t-1}^2+\beta h_{t-1},\qquad
\delta=\alpha+\beta<1,\qquad v=E(y_t^2)=\frac{\psi}{1-\delta}.
$$

Let $\kappa=E(y_t^4)/v^2$ be **return kurtosis**, not excess kurtosis and not standardized-innovation kurtosis. For a strong model with $\kappa_\xi=E(\xi_t^4)$,

$$
\kappa=\frac{\kappa_\xi(1-\delta^2)}{1-\delta^2-(\kappa_\xi-1)\alpha^2}.
$$

The denominator must be positive. Equivalently $\delta^2+(\kappa_\xi-1)\alpha^2<1$. A finite unconditional variance alone is insufficient for this paper's fourth-moment aggregation theory. Gaussian innovations have $\kappa_\xi=3$; a standardized Student distribution with five degrees of freedom has $\kappa_\xi=9$.

Set $\eta_t=y_t^2-h_t$. Its orthogonality gives the squared-series ARMA representation

$$
y_t^2=\psi+\delta y_{t-1}^2+\eta_t-\beta\eta_{t-1}.
$$

This representation, together with the fourth-moment identities, is what can be aggregated. It is not necessary to postulate an independent low-frequency shock distribution.

## Exact stock-sampling transformation

For sampling every $m$th observation, denote the weak GARCH coefficients by $\psi_m,\alpha_m,\beta_m$. Equations (9)–(12) imply

$$
\psi_m=\psi\frac{1-\delta^m}{1-\delta},\qquad
\alpha_m=\delta^m-\beta_m,
$$

$$
\frac{\beta_m}{1+\beta_m^2}=Q_m^{S}
=\frac{\beta\delta^{m-1}}
{1+\alpha^2(1-\delta^{2m-2})/(1-\delta^2)+\beta^2\delta^{2m-2}}.
$$

Select the invertible root, $|\beta_m|<1$. A numerically convenient expression, continuous at $Q=0$, is

$$
\beta_m=\frac{2Q}{1+\sqrt{1-4Q^2}}.
$$

The discriminant and admissibility constraints should be checked. The other quadratic root is reciprocal and corresponds to the noninvertible representation. In particular, stock sampling an ARCH(1), where $\beta=0$, gives another weak ARCH(1), with $\alpha_m=\alpha^m$.

For a proof at $m=2$, eliminate the intervening squared observation:

$$
y_t^2=\psi(1+\delta)+\delta^2y_{t-2}^2+\eta_t+\alpha\eta_{t-1}-\beta\delta\eta_{t-2}.
$$

On the coarse grid the final three terms have nonzero covariance only at lag zero and one. Match their covariance ratio to an invertible MA(1), producing the equation above. The general case repeats this argument after multiplying by the finite geometric lag polynomial. Unconditional variance stays $v$, as it must when observations are sampled rather than summed.

The source's illustrative starting pair $(\beta,\alpha)=(0.8,0.05)$ maps approximately to $(0.677,0.046)$ at $m=2$, $(0.488,0.034)$ at $m=4$, and $(0.254,0.018)$ at $m=8$. These are rounded illustrative values. Figure 1 follows repeated doubling and halving for several initial persistence levels. Although $\alpha_m$ need not be monotone at every point on every path, total persistence is exactly $\delta^m$ and vanishes as the interval grows. The stock transformation does not require a separate kurtosis input once the admissible fine-frequency variance parameters are given.

## Exact flow transformation and its kurtosis dependence

For $Y_k=\sum_{i=0}^{m-1}y_{mk-i}$, use bars for the coarse coefficients. Define

$$
C=\alpha(1-\beta\delta),\qquad D=1-\beta^2-2\alpha\beta,\qquad F_m=m-1-m\delta+\delta^m,
$$

$$
a_m=m(1-\beta)^2+
\frac{2m(m-1)(1-\delta)^2D}{(\kappa-1)(1-\delta^2)}
+\frac{4F_mC}{1-\delta^2},\qquad b_m=\frac{C(1-\delta^{2m})}{1-\delta^2}.
$$

Then source equations (13)–(18) give

$$
Q_m^{F}=\frac{a_m\delta^m-b_m}{a_m(1+\delta^{2m})-2b_m},\qquad
\bar\beta_m=\frac{2Q_m^{F}}{1+\sqrt{1-4(Q_m^{F})^2}},
$$

$$
\bar\alpha_m=\delta^m-\bar\beta_m,\qquad
\bar\psi_m=m\psi\frac{1-\delta^m}{1-\delta},
$$

$$
\bar\kappa_m=3+\frac{\kappa-3}{m}
+\frac{6(\kappa-1)F_mC}{m^2(1-\delta)^2D}.
$$

Several easy transcription errors materially change this transformation. The last term in $a_m$ has denominator $1-\delta^2$, while the last term in $\bar\kappa_m$ has $(1-\delta)^2D$. The denominator of $Q_m^F$ contains $-2b_m$, without an extra $\delta^m$. The formula requires return kurtosis $\kappa$, not $\kappa_\xi$. These details were checked against the typeset equations and independently against covariance matching.

Unconditional variance is $mv$, so $\bar\psi_m/(1-\bar\alpha_m-\bar\beta_m)=mv$. This equality does not make the period-by-period coarse projection equal to $m$ times the current fine projection. Flow aggregation also does not generally preserve the ARCH subclass: cross-products of fine returns create a moving-average component in squared aggregate returns.

Here is a separate implementation check derived from moments. Normalize by $v^2$ and define $c_0=\kappa-1$, $c_1=c_0C/D$. The normalized variance and lag-one covariance of squared flow sums are

$$
g_0=mc_0+6c_1\sum_{i=1}^{m-1}(m-i)\delta^{i-1}+2m(m-1),\qquad
g_1=c_1\left(\frac{1-\delta^m}{1-\delta}\right)^2.
$$

Put $\rho=g_1/g_0$. Matching the squared ARMA(1,1) autocorrelation yields

$$
Q=\frac{\delta^m-\rho}{1+\delta^{2m}-2\rho\delta^m},\qquad \bar\kappa_m=1+g_0/m^2.
$$

These expressions agree with the closed form and are useful unit checks. They use the mixed-moment restrictions above. For near-unit persistence, geometric sums or stable exponential calculations avoid cancellation; formulas written with $1-\delta$ should not be evaluated by substituting $\delta=1$ into a stationary model.

The normal-innovation example starting around $(\beta,\alpha,\kappa)=(0.871,0.051,3.11)$ maps at $m=2$ to roughly $(0.800,0.050,3.26)$. Changing the standardized innovations to Student five changes the starting return kurtosis to about 10.47 and yields roughly $(0.777,0.073,7.68)$ instead. Figure 2 shows these distinct paths. The displayed starting values are rounded, so recomputing from exactly the printed decimals need not reproduce every third decimal of the graph's underlying calculation.

A consequence for disaggregation is that low-frequency variance coefficients alone generally do not identify fine-frequency flow coefficients. Kurtosis supplies additional information. Even with that information, an admissible higher frequency embedding need not exist. One must solve the transformation subject to positivity, stationarity, moment existence and invertibility; a solver's numerical root is not sufficient. The source expressly warns that repeatedly disaggregating a fitted model is not always possible, whether because of sampling error or genuine non-embeddability.

## Why the stronger GARCH classes are not closed

Example 3 begins with a Gaussian strong ARCH(1), $y_t=\xi_t\sqrt{\psi+\alpha y_{t-1}^2}$, and samples every second observation. The coarse conditional variance is $h_t^{(2)}=\psi(1+\alpha)+\alpha^2y_{t-2}^2$. With $\lambda_t=\psi/h_t^{(2)}$, its standardized coarse shock can be expressed as

$$
v_t=\xi_t\sqrt{\lambda_t+(1-\lambda_t)\xi_{t-1}^2}.
$$

The conditional second moment is one, but the conditional fourth moment is

$$
E(v_t^4\mid\mathcal F_{t-2})=3\{1+2(1-\lambda_t)^2\}.
$$

It depends on the past through $\lambda_t$. Thus the sampled process can be semistrong without possessing independent identically distributed standardized shocks. Matching a variance recursion is not enough to preserve a Gaussian innovation law.

Example 4 is stronger: it starts from an ARCH(1) with independent shocks having probabilities $P(\xi=0)=1-\alpha$ and $P(\xi=\pm1/\sqrt\alpha)=\alpha/2$. Here $0<\alpha<1$, $\kappa_\xi=1/\alpha$, and the finite-fourth-moment condition holds because $\alpha^2\kappa_\xi=\alpha<1$. Squared returns reset to zero or progress through a discrete sequence. For two-period sums, certain observed preceding sums reveal a reset in the hidden fine path. The next conditional second moment on these events equals $\psi(2+\alpha)$, independently of the preceding sum's magnitude. A nontrivial linear GARCH conditional-variance recursion would vary with that magnitude. The resulting contradiction establishes that semistrong models are not generally closed under flow aggregation. The weak projection nevertheless retains a GARCH representation.

## Higher orders and the role of the conditional mean

Suppose the observed process satisfies an ARMA mean equation $\Phi(L)y_t=\Theta(L)\varepsilon_t$ of orders $(P,Q)$, with weak GARCH$(p,q)$ innovations. Let the aggregation filter $W(L)$ have degree $w$, followed by sampling every $m$th date, and put $r=\max(p,q)$. Theorem 1 gives the upper bounds

$$
\widetilde P=P,\qquad
\widetilde Q=P+\left\lfloor\frac{Q-P+w}{m}\right\rfloor,\qquad
\widetilde p=\widetilde q=r+\frac{\widetilde Q(\widetilde Q+1)}2.
$$

The formula concerns a valid resulting polynomial representation; cancellations and special structures can reduce the actual order. In a special factorization case the GARCH orders reduce to $(r+\lfloor(p-r)/m\rfloor,r)$. Consequently a pure GARCH process sampled as stocks has this latter order bound, while a pure GARCH flow has bound $(r,r)$. The mean dynamics matter: an ARMA(1,1)–GARCH(1,1) can become ARMA(1,1)–GARCH(2,2). Reaggregating that representation naively gives a bound of GARCH(3,3), although the restrictions inherited from the fine model reduce it to GARCH(2,2). Orders are not independent labels that can be propagated without their coefficient restrictions.

The appendix's proof is constructive. For a polynomial $P(L)=\prod_i(1-p_iL)$, define $P_m(L^m)=\prod_i(1-p_i^mL^m)$ and the finite multiplier $\bar P_m(L)=\prod_i\sum_{j=0}^{m-1}p_i^jL^j$, so $P_m(L^m)=\bar P_m(L)P(L)$. This converts the fine AR polynomial into a coarse one. The remaining finite moving-average covariance sequence can be spectrally factored to obtain the coarse mean innovations $\zeta_t=\Psi(L)\varepsilon_t$.

Squaring $\zeta_t$ separates squared innovations from cross-products. The source's $\Psi^2(L)=\sum_i\psi_i^2L^i$ means **coefficient-wise squaring**, not the polynomial product $\Psi(L)\Psi(L)$. The mixed-moment assumptions make the squared-innovation innovations orthogonal to the cross-product component. If the filter coefficients $\psi_i$ obey a recurrence of order $\widetilde Q$, their squares obey a recurrence with at most $\widetilde Q(\widetilde Q+1)/2$ characteristic pair-products. Multiplication by that recurrence polynomial leaves a finite coarse moving-average covariance sequence. Spectral factorization supplies the variance-lag coefficients; subtracting the moving-average polynomial from the squared-series autoregressive polynomial supplies the squared-innovation coefficients. This explains the triangular-number term in the theorem and why a general implementation needs numerical covariance factorization.

## Estimation and the exchange-rate illustration

For nondegenerate GARCH(1,1), the squared-series first two autocorrelations identify coarse persistence through $\delta_m=\rho_2/\rho_1$. Solve

$$
\rho_1=\frac{(\delta_m-\beta_m)(1-\beta_m\delta_m)}{1+\beta_m^2-2\beta_m\delta_m},\qquad
\psi_m=(1-\delta_m)E(y_{mk}^2).
$$

Under the paper's ergodicity and moment assumptions, consistent sample moments produce consistent parameter estimates and transformations. The zero-autocorrelation boundary is not identified by this ratio: if $\rho_1=0$, dividing by it is invalid and distinct variance parameterizations may collapse to the same homoskedastic projection. Normal quasi-likelihood consistency for a correctly specified semistrong variance does not automatically extend to an arbitrary weak GARCH model. The paper explicitly declines to prove consistency of the classical quasi-likelihood estimator in that setting. Simulation evidence elsewhere suggesting small bias is not a theorem here, and Student quasi-likelihood is an additional issue.

The empirical example reuses Baillie–Bollerslev estimates for six exchange rates against the US dollar, New York market, March 1, 1980–January 28, 1985. Weekly and monthly intervals are represented by five and twenty daily observations. Intraday disaggregation assumes eight hours per day and ignores seasonal patterns. The source does not supply the raw observations or a fresh estimation experiment. Table II compares direct weekly estimates with values transformed from daily estimates:

| Currency | Daily $(\beta,\alpha,\kappa_\xi)$ | Direct weekly | Implied weekly |
|---|---|---|---|
| French franc | .829, .114, 4.92 | .655, .144, 5.13 | .589, .157, 5.81 |
| Italian lira | .848, .113, 3.89 | .658, .187, 3.00 | .663, .157, 5.13 |
| Japanese yen | .941, .049, 5.62 | .927, .072, 6.65 | .839, .112, 4.71 |
| Swiss franc | .907, .073, 3.41 | .784, .121, 3.00 | .792, .112, 4.05 |
| British pound | .910, .061, 4.16 | .842, .049, 3.00 | .768, .096, 4.09 |
| German mark | .881, .085, 3.41 | .636, .249, 3.00 | .728, .113, 4.11 |

For comparability the authors report standardized-innovation kurtosis values obtained from the strong-model identity, even though not every coarse process is strong. These columns must not be read as evidence of independent Student shocks at every frequency. The direct weekly yen estimate has persistence $.999$ and fourth-moment coefficient $.999^2+(6.65-1)(.072)^2>1$. Its return fourth moment does not exist under that fitted strong specification; the paper consequently leaves its implied monthly values blank.

Table III's unconstrained hourly disaggregation gives $(\beta,\alpha,\kappa_\xi)$ respectively: franc $(.957,.035,7.36)$, lira $(.936,.059,2.66)$, yen $(.990,.009,18.12)$, Swiss franc $(.958,.039,2.31)$, pound $(.979,.017,7.62)$, and mark $(.928,.067,1.69)$. Two additional column groups impose hourly Gaussian kurtosis three or Student-six kurtosis six. Their reported kurtosis columns are then **implied daily** values, not the imposed hourly values. For example, the yen has hourly $(.978,.020)$ with implied daily kurtosis 3.32 under the Gaussian constraint, and $(.985,.014)$ with implied daily kurtosis 3.78 under the Student-six constraint. This distinction is essential when reconstructing the table.

Table IV's daily-implied monthly $(\beta,\alpha,\kappa_\xi)$ values are: franc $(.206,.103,6.27)$, lira $(.325,.126,6.04)$, yen $(.661,.157,5.48)$, Swiss franc $(.553,.115,4.54)$, pound $(.472,.083,4.17)$, and mark $(.411,.090,4.36)$. Weekly-implied values are respectively $(.299,.109,5.56)$, $(.391,.119,4.48)$, unavailable for yen, $(.570,.101,3.90)$, $(.593,.037,3.26)$, and $(.426,.187,6.26)$. Direct monthly estimation used only 59 observations and did not reject homoskedasticity, while aggregation implied substantial monthly dynamics. That discrepancy concerns information and test power; nonrejection is not proof that the monthly process has constant variance.

## Reproduction boundaries

The closed-form GARCH(1,1) transformations can be implemented from the equations here. Start by recording whether data are sampled or summed, the mean model, the units and moment conventions. Check finite fourth moments before converting innovation kurtosis to return kurtosis. Transform variance, persistence, and kurtosis jointly, select the invertible root, and verify both the unconditional variance identity and squared-series covariance matching. For inverse transformations, report inadmissibility or multiple roots instead of forcing a fine-frequency model.

Exact reconstruction of the empirical tables requires the original unrounded daily and weekly estimates, their covariance matrices, the original return data and calendar treatment, mean-equation dummies and estimation details from the earlier exchange-rate study. The article's menu-driven program was available on request but is not embedded in the local PDF. Rounded table inputs allow numerical validation, not exact recovery of hidden digits or uncertainty estimates. General higher-order implementation also needs a reliable spectral-factorization routine and checks for cancellation and positivity. No risk quantiles, realized-volatility evaluation, transaction costs, or investment profits are estimated in this paper. Its durable contribution is a coherent change-of-frequency model for second and fourth moments, with clear limits on the stronger probabilistic interpretation that can accompany that model.
