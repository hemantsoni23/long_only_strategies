# A New Variance Bound on the Stochastic Discount Factor

## Source and scope

- **Authors:** Raymond Kan and Guofu Zhou.
- **Publication:** *The Journal of Business* 79(2), 2006, pp. 941–961.
- **Original file:** [StochasticDiscount_KanZhou_2006.pdf](../../Finance/StochasticDiscount_KanZhou_2006.pdf).
- **Reading coverage:** all 21 PDF pages, including references; equations on PDF pp. 4–5, both figures on pp. 11 and 13, habit equations on p. 17, and Table 1 on p. 18 visually checked.
- **Type of result:** a population necessary condition for a restricted class of stochastic discount factors, with empirical illustrations. It is not an implementable trading signal or a sufficient asset-pricing test.

## Why this matters

An SDF can be volatile enough to satisfy the ordinary Hansen–Jagannathan bound and still obtain almost none of that volatility from states related to asset payoffs. Kan and Zhou ask how much SDF variation is required when the kernel must be a function of a specified vector of state variables. Their answer multiplies the usual minimum variance by the reciprocal of a multiple correlation squared. Small alignment between the proposed economic states and the payoff-spanned pricing kernel therefore creates a large additional hurdle.

For a quantitative researcher, the diagnostic separates two mechanisms often conflated in model fitting. Raising a risk-aversion parameter can increase the volatility of marginal utility. It does not necessarily give marginal utility the covariance with returns needed to explain expected returns. The second requirement is the issue here. In the authors' historical habit-model illustration, adding habit raises kernel volatility considerably, but the proposed state variables remain weakly related to the return-spanned kernel. The standard variance bound can pass while the state-specific bound fails badly.

The important qualification is that the sharp result is not a restriction on every measurable function of arbitrary states. The principal theorem additionally assumes that the linear projection residual of the minimum-variance SDF has zero conditional mean given the states. Ordinary regression orthogonality does not establish this. Joint ellipticity is one sufficient condition; a correctly specified nonlinear conditional expectation is another route. A replication must check the economic state restriction and the projection restriction separately.

## Novelty and position in the literature

Hansen–Jagannathan asks for the least volatile random variable that prices the test assets at a given mean. Its generality makes the benchmark feasible for every valid SDF, but can make it weak for a particular economic model. A direct Euler-equation test specifies the model much more tightly: a utility function, parameter values, states, and moment conditions. Kan–Zhou occupies an intermediate position. Specify the states and a restriction on how the return-spanned kernel projects onto them, while leaving the functional form of the economic SDF largely unspecified.

This differs from tightening a bound with lagged instruments or managed portfolios. Those methods enlarge the set of payoffs whose prices must be matched. Here the emphasis is restricting the information or states from which a kernel can be constructed. The distinction is material: each candidate state vector generally has its own bound. A consumption kernel and a market-factor kernel are not assessed against one universal state-specific curve.

The paper also distinguishes its result from the exact covariance identity involving the correlation between a fully specified SDF and the minimum-variance SDF. That identity requires knowing the kernel itself. The proposed bound uses moments of the observed states and returns, without choosing a particular nonlinear kernel. It can therefore diagnose a whole class of models before a functional form is estimated.

## Setup and notation

Let $R$ be an $N$-vector of risky gross returns. Write

$$
\mu=E[R],\qquad \Sigma=\operatorname{Var}(R),\qquad E[m]=\mu_m.
$$

The assets are nonredundant, so $\Sigma$ is invertible. Their means are not all identical in the trivial proportional-to-ones case excluded by the authors. The unconditional pricing restrictions are

$$
E[mR]=\mathbf 1_N.
$$

The conditional Euler equation motivates this relation, but the principal bound uses unconditional moments. Satisfaction of this unconditional equation alone does not imply the corresponding conditional pricing relation. If a constant gross risk-free return $R_f$ is available and priced, then $\mu_m=1/R_f$. Otherwise the analysis considers different candidate values of $\mu_m$.

At any specified mean define

$$
d=\mathbf 1_N-\mu_m\mu,
\qquad
m_0=\mu_m+d'\Sigma^{-1}(R-\mu).
$$

This is the minimum-variance SDF for these unconditional pricing equations and this mean. Its variance is

$$
V_0=\operatorname{Var}(m_0)=d'\Sigma^{-1}d.
$$

Indeed,

$$
E[m_0R]=\mu_m\mu+\Sigma\Sigma^{-1}d=\mathbf 1_N.
$$

Here the matrix expression uses the corresponding column-vector orientation. For any other valid $m$ with the same mean, $m-m_0$ is orthogonal to the span of constants and returns, implying

$$
\operatorname{Cov}(m,m_0)=V_0,
\qquad
\operatorname{Var}(m)=V_0+\operatorname{Var}(m-m_0)\ge V_0.
$$

The last inequality is the ordinary HJ variance bound. Strict positivity of the SDF is not imposed in this construction. No-arbitrage positivity restrictions may generate different, tighter bounds; the paper's closed-form result is based on linear pricing and second moments.

## The state-specific inequality and its proof

Suppose the economic kernel is $m=m(x)$ for a $K$-vector of states $x$. Consider the population linear projection

$$
m_0=\alpha+\beta'x+\varepsilon_0.
$$

A linear projection always gives $E[\varepsilon_0]=0$ and $E[(x-E[x])\varepsilon_0]=0$. The theorem requires the stronger property

$$
E[\varepsilon_0\mid x]=0.
$$

Thus the conditional expectation $q(x)=E[m_0\mid x]$ equals the affine projection $\alpha+\beta'x$. This condition ensures orthogonality to *every* square-integrable function of $x$, rather than only to its linear components:

$$
E[\varepsilon_0m(x)]
=E\{m(x)E[\varepsilon_0\mid x]\}=0.
$$

Consequently,

$$
V_0=\operatorname{Cov}(m,m_0)=\operatorname{Cov}(m,q).
$$

Cauchy–Schwarz then gives

$$
V_0^2\le \operatorname{Var}(m)\operatorname{Var}(q).
$$

If $\rho_{x,m_0}^2$ denotes the population multiple $R^2$ from the projection of $m_0$ onto $x$, then

$$
\operatorname{Var}(q)=\rho_{x,m_0}^2V_0,
$$

and hence

$$
\boxed{\operatorname{Var}[m(x)]\ge
\frac{V_0}{\rho_{x,m_0}^2}.}
$$

For standard deviations, the multiplier is $1/\rho_{x,m_0}$, not $1/\rho_{x,m_0}^2$. The multiple correlation is nonnegative; for a single state it is the absolute value of the ordinary correlation. This unit distinction matters when interpreting the paper's figures and empirical table.

The proof can alternatively be written with $\Sigma_{xx}=\operatorname{Var}(x)$ and $\Sigma_{xm}=\operatorname{Cov}(x,m)$. Combining the vector Cauchy–Schwarz inequality with the variance explained by the projection of $m$ on $x$ produces the same result. The conditional-expectation proof makes especially clear where the assumption enters and why replacing it by ordinary OLS orthogonality is invalid.

### A printed equality-case error

Proposition 1 and its proof on journal pp. 944–945 state that equality holds if and only if $m(x)=\alpha+\beta'x$, using the coefficients of the projection of $m_0$ on $x$. This statement is not consistent with the pricing covariance identity except in the special case $\rho^2=1$. The visual source confirms that this is printed in the paper, rather than an extraction artifact.

The equality condition implied by the proof is instead

$$
m(x)-\mu_m
=\frac{V_0}{\operatorname{Var}(q)}[q(x)-\mu_m]
=\frac{q(x)-\mu_m}{\rho_{x,m_0}^2},
$$

provided this random variable also satisfies all the individual asset-pricing equations. To see the problem immediately, setting $m=q$ yields $\operatorname{Cov}(m,m_0)=\operatorname{Var}(q)=\rho^2V_0$, whereas a valid SDF must yield $V_0$. Equality in a single aggregate covariance bound does not by itself guarantee that every test asset is priced. The inequality remains valid under its assumptions; the printed characterization of equality should not be implemented literally.

## Assumptions, generalizations, and edge cases

Joint ellipticity of $x$ and $R$, with the required finite moments and nonsingular state covariance, makes the relevant conditional expectation affine. Multivariate normality is a special case. The economic kernel itself need not be elliptically distributed because it can be a nonlinear function of the states. This is an important distinction: an exponential marginal-utility kernel can be considered even when the state-return system is modeled with an elliptical distribution.

The authors discuss transformations $y=g(x)$ that may give a more appropriate joint distribution. Such transformations must preserve the proposed economic kernel's representability in the selected state variables. A researcher cannot simply choose an attractive transformation and assume that every function of the original state has become a function of the transformed state when the transformation loses information.

More generally, let $q(x)=E[m_0\mid x]$ be nonlinear. Exactly the same proof gives

$$
\operatorname{Var}[m(x)]\ge
\frac{V_0^2}{\operatorname{Var}(E[m_0\mid x])}.
$$

Equivalently, divide $V_0$ by the correlation squared between $m_0$ and its conditional expectation. This expression clarifies why the linear $R^2$ cannot be used without the additional assumption: a nonlinear conditional expectation may explain substantially more variation than a linear regression, making the linear-based claimed bound spuriously high.

When $\rho^2=1$, the inequality reduces to the HJ bound. When $\rho^2=0$ and $V_0>0$, no finite-variance SDF measurable with respect to these states can satisfy the required pricing covariance. This is an impossibility statement under the projection restriction, not merely evidence that risk aversion should be increased. The degenerate case $V_0=0$ must be treated separately rather than evaluated through an undefined ratio.

Adding state variables weakly increases the population explained variance and weakly lowers the state-specific hurdle, holding the test assets and the kernel mean fixed. Adding assets changes the return-spanned kernel itself and is a different exercise. In samples, multicollinearity, covariance estimation error, and state selection can make apparent comparisons less clean than the population statement.

## Shape of the bound as the kernel mean varies

The ordinary HJ variance frontier is quadratic in $\mu_m$. Kan–Zhou's is generally a ratio of a fourth-degree polynomial and a second-degree polynomial. Set

$$
a=\mu'\Sigma^{-1}\mu,\quad
b=\mu'\Sigma^{-1}\mathbf 1,\quad
c=\mathbf 1'\Sigma^{-1}\mathbf 1,
$$

so $V_0=a\mu_m^2-2b\mu_m+c$. Let $C=\operatorname{Cov}(x,R)$ and define

$$
M=\Sigma^{-1}C'\Sigma_{xx}^{-1}C\Sigma^{-1},
$$

$$
a_1=\mu'M\mu,\qquad
b_1=\mu'M\mathbf 1,\qquad
c_1=\mathbf 1'M\mathbf 1.
$$

Then

$$
\operatorname{Var}[m(x)]\ge
\frac{(a\mu_m^2-2b\mu_m+c)^2}
{a_1\mu_m^2-2b_1\mu_m+c_1}.
$$

This follows by substituting $\operatorname{Cov}(x,m_0)=C\Sigma^{-1}d$ into the explained-variance formula. With one state, the denominator can vanish at a particular mean even when it is positive elsewhere. Thus a vertical asymptote is an economically meaningful consequence of the model restriction, not necessarily a numerical failure. A computation should distinguish this population geometry from near-singular estimated covariance matrices.

Figure 1 uses monthly returns on the 25 Fama–French size/book-to-market portfolios, January 1952–December 2002. It plots variance, not standard deviation. For a market-return state alone, the illustrated curve diverges near $\mu_m=0.9901$, corresponding to a monthly risk-free rate of approximately 1%. Adding SMB and HML lowers the state-specific bound. Over the plotted range, the authors report improvements over the HJ variance bound from 34% to 646%. Those percentages describe this sample and mean range; they are not universal constants.

## Empirical estimators and consumption applications

For $T$ observations the paper first estimates returns' means and covariance. Its displayed HJ estimator includes the normal-theory bias adjustment borrowed from Ferson–Siegel:

$$
\widehat V_0(\mu_m)=
\left(1-\frac{N+2}{T}\right)
(\mathbf 1-\mu_m\widehat\mu)'
\widehat\Sigma^{-1}
(\mathbf 1-\mu_m\widehat\mu)
-\frac{N}{T}\mu_m^2.
$$

The new estimated variance bound is $\widehat V_0/\widehat\rho^2$. The displayed correction addresses the HJ numerator under its distributional conditions. It does not establish that the nonlinear ratio involving an estimated small $R^2$ is unbiased. A practical study should report sampling uncertainty for the complete ratio, not inherit an unbiasedness claim from its numerator.

For power utility,

$$
m=\delta\left(\frac{C_{t+1}}{C_t}\right)^{-\gamma}
=\delta e^{-\gamma x_{t+1}},
\qquad x_{t+1}=\log(C_{t+1}/C_t).
$$

Under the required assumptions, the variance of this kernel must exceed the consumption-state bound. Increasing $\gamma$ changes its volatility; low state-return correlation simultaneously raises the required volatility. The paper also treats marginal utility ratios that depend on both consumption levels and growth by conditioning on current consumption and imposing constant conditional first and second moments for the relevant state/kernel system. This stronger setup should not be mistaken for an assumption-free result for arbitrary preferences.

A simple market illustration uses an approximately 8% annual excess mean and 16% annual standard deviation, giving a Sharpe ratio around 0.5. Taking the kernel mean near 0.99 gives an HJ standard-deviation hurdle about 0.5. If the consumption-growth/market-return correlation is 0.2, the new standard-deviation hurdle is about 2.5: five times higher, or 25 times higher in variance. These are illustrative annual inputs, not the monthly numbers in Table 1.

For 25 size/book-to-market portfolios and consumption growth, Figure 2 has a markedly higher variance scale and another pole. The text reports a maximum squared correlation of only 0.0078 over the plotted mean range, corresponding to a variance multiplier of at least about 128. The source contains unresolved documentation inconsistencies: the figure caption says durable consumption and February 1959–December 2002, whereas the adjacent prose says nondurable per-capita consumption from Citibase and mentions February 1952. Table 1 explicitly uses February 1959–December 2002. A replication should preserve this discrepancy and obtain the original input series rather than silently choose one description.

## Habit-model experiment and reported magnitudes

The Campbell–Cochrane kernel is

$$
m_{CC}=\delta
\left(\frac{S_{t+1}C_{t+1}}{S_tC_t}\right)^{-\gamma},
\qquad S_t=\frac{C_t-X_t}{C_t},
$$

where $X_t$ is latent habit and $S_t$ is the surplus-consumption ratio. The states are log consumption growth and log surplus-consumption growth. The latter is generated from a specified model, rather than observed directly. The paper uses the nonlinear surplus-ratio dynamics from Campbell–Cochrane, persistence $\phi=0.989$ monthly, risk-aversion values from 2 to 20, and discount factors selected to give a log risk-free rate of 0.0783% monthly, approximately 0.94% annually. Consumption-growth mean and volatility are estimated from the sample. These model-generated states are part of the identifying assumptions.

The complete state-generation equations are important because different habit recursions can produce different state-return correlations. With $s_t=\log S_t$, $c_t=\log C_t$, and consumption-growth mean $g$ and standard deviation $\sigma_c$, source equations (44)–(45) specify

$$
s_{t+1}=(1-\phi)\bar s+\phi s_t
+\lambda(s_t)(c_{t+1}-c_t-g),
$$

$$
\bar S=\sigma_c\sqrt{\frac{\gamma}{1-\phi}},
\qquad \bar s=\log\bar S,
\qquad s_{\max}=\bar s+\frac12(1-\bar S^2),
$$

$$
\lambda(s)=
\begin{cases}
\bar S^{-1}\sqrt{1-2(s-\bar s)}-1,&s<s_{\max},\\
0,&s\ge s_{\max}.
\end{cases}
$$

At the cutoff the first branch equals zero, so the piecewise definition joins continuously. For each specified $\gamma$, estimate $g$ and $\sigma_c$ from monthly log consumption growth and recompute $\bar S$, $\bar s$, and the cutoff. Starting from a recorded $s_0$, feed each dated consumption innovation through the recurrence, exponentiate to recover $S_t$, and evaluate the kernel. The two regression states are then $c_{t+1}-c_t$ and $s_{t+1}-s_t$ on the same dates as asset returns. Reusing one habit path across different curvature values would generally fail to reproduce this calibration because $\bar S$ itself depends on $\gamma$.

Source equation (46) sets the log risk-free rate to

$$
r_f=-\log\delta+\gamma g-\frac{\gamma}{2}(1-\phi).
$$

Thus the monthly calibration uses $r_f=0.000783$ and

$$
\delta=\exp\left[\gamma g-\frac{\gamma}{2}(1-\phi)-0.000783\right].
$$

The target kernel mean associated with this constant risk-free rate is $e^{-r_f}$. This supplies the missing operational link between the verbal calibration and Table 1. The PDF does not document a complete initialization and burn-in protocol for the extracted latent series; those remain replication inputs to record rather than silently infer. In particular, choosing $s_0=\bar s$ is a natural reconstruction choice, not a reported implementation fact. Numerical checks should verify the sensitivity cutoff before taking its square root, preserve the monthly units of $g$, $\sigma_c$, $\phi$, and $r_f$, and report how many observations reach the zero-sensitivity branch.

Table 1 reports SDF **standard deviations**, as dimensionless kernel quantities. Selected rows are:

| Curvature $\gamma$ | Consumption kernel SD | Habit kernel SD | Market HJ SD bound | Market state correlation | Market new SD bound | 25-portfolio HJ SD bound | 25-portfolio state correlation | 25-portfolio new SD bound |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.0148 | 0.1358 | 0.1886 | 0.146 | 1.2931 | 0.4603 | 0.095 | 4.8279 |
| 4 | 0.0293 | 0.2072 | 0.1886 | 0.143 | 1.3182 | 0.4603 | 0.097 | 4.7664 |
| 10 | 0.0713 | 0.3563 | 0.1886 | 0.140 | 1.3456 | 0.4603 | 0.096 | 4.7880 |
| 16 | 0.1118 | 0.4819 | 0.1886 | 0.139 | 1.3557 | 0.4603 | 0.095 | 4.8510 |
| 20 | 0.1383 | 0.5638 | 0.1886 | 0.139 | 1.3590 | 0.4603 | 0.094 | 4.8941 |

The single-asset test uses the value-weighted NYSE market portfolio. The second uses the 25 Fama–French portfolios. At $\gamma=2$, habit raises SDF standard deviation to roughly 9.2 times that of the basic consumption kernel, but still misses even the market HJ bound. At $\gamma\ge4$, habit passes that ordinary market bound. At $\gamma\ge16$, it also passes the ordinary 25-portfolio bound. Across the displayed range, it fails the new state-specific bound by a large margin.

The authors report that curvature of at least 129 is required for their habit-model implementation to pass the new bound. This is a numerical conclusion for their calibration, generated habit series, asset menu, and sample. It is not a theorem that every habit model needs that parameter. In particular, weak correlations estimated under the assumed state specification and distributional approximation do most of the work.

## Reproduction plan and missing inputs

A direct reproduction should implement the following sequence:

1. Obtain the exact vintage of monthly market and 25-portfolio returns and the risk-free series. Retain gross-return conventions and state precisely which assets enter $R$.
2. Obtain the consumption series, population adjustment, seasonal treatment, and timestamps. Resolve the durable/nondurable and 1952/1959 source discrepancies before labeling a result a replication.
3. Generate the habit series from the specified recurrence, recording its initial condition, burn-in, parameter calibration, and treatment of the sensitivity-function cutoff. Those implementation choices are not fully supplied as a reproducible data package in this PDF.
4. For each kernel mean, estimate $\widehat\mu$, $\widehat\Sigma$, the minimum-variance kernel, and the projection on the chosen states. Report covariance condition numbers and the estimated $R^2$.
5. Apply the documented HJ numerator correction and construct both variance and standard-deviation bounds. Flag negative corrected variances or essentially zero denominators instead of replacing them silently.
6. Compute candidate model kernels on the same dates, with exactly matched normalization, and compare their standard deviations to the corresponding bounds.
7. Repeat inference over the whole pipeline, including estimated states and ratios. Use a time-series procedure appropriate to the data dependence; this is a proposed robustness step, not an inferential result supplied by the paper.

The PDF supplies analytical formulas, historical summary results, calibration choices, and graphical evidence. It does not include original data files, executable estimation code, an identified consumption-series vintage, or confidence intervals for all the empirical ratio bounds. It therefore supports reconstruction of the method and a benchmark comparison, but does not by itself make every numerical result exactly reproducible.

## Limitations and interpretation

Passing the bound is only necessary. It does not establish that a kernel prices all assets, is positive, prices dynamically managed returns, or has a credible economic interpretation. Failing a correctly applicable bound rejects at least one element of the state/kernel/pricing setup, but does not identify which element failed. Weak linear correlation is especially informative only after the conditional-expectation restriction has been defended.

The paper's discussion of measurement error is a useful intuition rather than a universal measurement-error theorem. Noisy state proxies can increase kernel volatility and make the ordinary HJ test easier to pass; they can also reduce estimated state-return correlation and raise this bound. But arbitrary noise can change the conditional-expectation assumption, the interpretation of the true state restriction, and the estimation error of the denominator. These effects need a specified measurement model.

The central reusable contribution is the conditional-projection inequality. It makes the source of required SDF volatility explicit, provides a simple diagnostic for weakly connected state variables, and shows why adding volatility to an economic kernel is insufficient. Its main practical hazards are treating a linear projection as a conditional expectation, confusing variance with standard deviation, overlooking the dependence of the bound on the kernel mean, and interpreting a necessary bound as a complete pricing test.

## An analytical check on the conditional-expectation assumption

The following constructed example is a useful implementation test; it is not an empirical result in the paper. Let $x$ be standard normal and let the single gross return and candidate kernel be

$$
R=0.9+0.1x^2,
\qquad m=0.4+0.5x^2.
$$

Both are positive. Their moments satisfy $E[R]=1$, $E[m]=0.9$, $\operatorname{Var}(R)=0.02$, and $\operatorname{Var}(m)=0.5$. Since $E[x^4]=3$,

$$
E[mR]=0.36+0.49E[x^2]+0.05E[x^4]=1.
$$

Thus $m$ really is a valid SDF for this asset and mean. The minimum-variance formula gives

$$
m_0=0.9+\frac{1-0.9}{0.02}(R-1)
=0.4+0.5x^2=m.
$$

But the linear regression of $m_0$ on $x$ has zero slope because $\operatorname{Cov}(x,x^2)=0$. Its linear $R^2$ is zero. Inserting this zero into the state-specific denominator would incorrectly suggest that no finite-variance SDF measurable in $x$ can price the asset. The error is exactly the missing hypothesis: the regression residual is $0.5(x^2-1)$, whose conditional expectation given $x$ is itself, not zero.

Using the actual conditional expectation fixes the issue. Here $q(x)=E[m_0\mid x]=m_0$, its explained variance is 0.5, and the generalized conditional-projection bound returns 0.5, attained by the displayed kernel. Equivalently, augmenting the regressor basis with $x^2$ makes the conditional expectation linear in the enlarged basis.

This example supplies a concrete diagnostic for empirical work. A small linear $R^2$ can reflect an economically weak state variable, or it can reflect an inadequate projection basis. These have different implications. The bound is compelling only after the relation between the state variables and the payoff-spanned kernel has been modeled adequately. Testing a few extra powers in a finite sample does not establish the exact conditional-expectation hypothesis, and searching over bases can introduce its own estimation bias. Nevertheless, plotting regression residuals against the states and comparing out-of-sample nonlinear fits is more informative than treating the ordinary OLS orthogonality conditions as proof of the theorem's stronger assumption.
