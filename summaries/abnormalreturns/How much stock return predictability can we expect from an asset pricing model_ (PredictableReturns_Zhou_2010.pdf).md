# How much stock return predictability can we expect from an asset pricing model?

Guofu Zhou. *Economics Letters* 108 (2010), 184-186. DOI: 10.1016/j.econlet.2010.05.008. Source: [PredictableReturns_Zhou_2010.pdf](../../Finance/PredictableReturns_Zhou_2010.pdf). All three source pages, including the proof, numerical table, and references, were read; equations and Table 1 were checked against rendered pages. The filename year agrees with publication. This is a short theoretical note with an illustrative calibration, not an out-of-sample trading study.

## Why this matters

A predictive regression can have a very small $R^2$ and still be difficult for an asset-pricing model to explain. The relevant comparison is between observed predictability and the predictability permitted by the model's stochastic discount factor (SDF). An SDF driven by state variables that correlate weakly with the payoff-spanned pricing kernel may require enormous variance to price observed assets. If one also limits the economically plausible variance of that SDF, its allowance for predictable returns becomes correspondingly small.

Zhou combines Ross's predictability bound with the state-variable SDF variance bound of Kan and Zhou. The proposed improvement multiplies Ross's bound by a squared multiple correlation. In the consumption example, correlations of 0.15 and 0.10 reduce a monthly $R^2$ ceiling of 7.9% to approximately 0.17775% and 0.079%. Several ordinary forecasting regressions then exceed the proposed ceiling despite explaining less than 1% of monthly return variance.

The contribution is this composition of two existing inequalities and the resulting model diagnostic. It is not a new predictor, a proof that high forecast accuracy is attainable, or an investment rule. Its empirical conclusion also depends on an auxiliary SDF-variance ceiling, imported correlations, and the scope of the pricing restrictions. These qualifications are essential because neither an unconstrained SDF nor a generic consumption-based model has a finite variance ceiling merely by being an SDF.

## Objects and assumptions

Write the excess return on an asset or portfolio as

$$
R_{t+1}=\mu(I_t)+\epsilon_{t+1},\qquad
\mu(I_t)=E[R_{t+1}\mid I_t],\qquad E[\epsilon_{t+1}\mid I_t]=0.
$$

The population predictive coefficient of determination is

$$
R^2=\frac{\operatorname{Var}(\mu(I_t))}{\operatorname{Var}(R_{t+1})}.
$$

A linear predictive regression, $R_{t+1}=\alpha+\beta z_t+\epsilon_{t+1}$, is the empirical special case. The predictor $z_t$ is known at the forecast origin. The state vector $x$ determining the SDF is a different object: in the application it is consumption growth, not the valuation ratio or interest rate used to forecast returns. Confusing these two roles would turn the same model bound into ten unrelated predictor-specific correlations.

Let $R_f$ be the constant net risk-free rate and let $r$ be the vector of gross returns on $N$ risky assets. An SDF satisfies the conditional pricing equations

$$
E[m_{t+1}r_{j,t+1}\mid I_t]=1,
$$

and consequently the unconditional moment condition $E[mr]=\mathbf 1_N$. With constant $R_f$, pricing the risk-free payoff fixes $\mu_m=E[m]=1/(1+R_f)$. Ross's inequality, quoted as the lemma on p. 184, is

$$
R^2\leq (1+R_f)^2\operatorname{Var}(m).
$$

The note does not rederive Ross's lemma or enumerate all the auxiliary assumptions behind the numerical ceilings taken from Ross. It specifically retains constant interest rates and later invokes a restriction on economically plausible SDF variance. One must not replace the right-hand side with a calibrated constant without retaining that extra restriction.

For the risky-asset vector, define $\mu=E[r]$ and the nonsingular covariance matrix $\Sigma=\operatorname{Var}(r)$. The paper constructs the default SDF

$$
m_0=\mu_m+(\mathbf 1_N-\mu_m\mu)'\Sigma^{-1}(r-\mu).
$$

Its mean is $\mu_m$, and direct substitution gives

$$
E[rm_0]=\mu\mu_m+\Sigma\Sigma^{-1}(\mathbf 1_N-\mu_m\mu)
=\mathbf 1_N.
$$

Thus it prices the stated assets unconditionally by construction. It is the affine projection of a pricing kernel onto the span of their returns. The note assumes nonredundant assets and excludes a trivial proportional-mean configuration; nonzero $\operatorname{Var}(m_0)$ is needed for the multiple correlation below to be well-defined.

Regress $m_0$ on a constant and $K$ state variables:

$$
m_0=a+b'x+e_0.
$$

OLS gives $E[e_0]=0$ and $\operatorname{Cov}(e_0,x)=0$. The proposition assumes the stronger statement

$$
E[e_0\mid x]=0.
$$

This is a conditional linearity assumption, not a consequence of running a linear regression. Joint ellipticity of returns and state variables is offered as a sufficient condition, assuming the relevant moments exist. The paper mentions Student distributions as a plausible elliptical family. Heavy tails without finite second moments would not support the variance calculations; nonelliptical return-consumption dependence may violate conditional linearity even when the linear fit looks innocuous.

Let

$$
\rho_{x,m_0}^2=
\frac{\operatorname{Var}(E[m_0\mid x])}{\operatorname{Var}(m_0)}
=\frac{b'\operatorname{Var}(x)b}{\operatorname{Var}(m_0)}.
$$

Under conditional linearity this is the squared multiple correlation from the linear regression. With one state variable it is the ordinary correlation squared. With several variables it is not any one pairwise correlation and is invariant to nonsingular linear changes of coordinates in $x$.

## The bound and its proof

For an SDF restricted to be a function of the selected state vector, the proposition states

$$
R^2\leq \rho_{x,m_0}^2(1+R_f)^2\operatorname{Var}[m(x)].
$$

The printed proof uses the Kan-Zhou inequality

$$
\operatorname{Var}[m(x)]\geq
\frac{\operatorname{Var}(m_0)}{\rho_{x,m_0}^2},
$$

or equivalently

$$
\operatorname{Var}(m_0)\leq
\rho_{x,m_0}^2\operatorname{Var}[m(x)],
$$

then applies Ross's bound using $m_0$. This is the entire substantive argument on p. 185; the proof is not an independent derivation of Ross's result.

The SDF-variance step can be reconstructed transparently. Write $v=m- m_0$. Since $m$ and $m_0$ have the same mean and price the same payoffs, $v$ is orthogonal to constants and returns, hence to $m_0$. Therefore $\operatorname{Cov}(m,m_0)=\operatorname{Var}(m_0)$. Because $m=m(x)$ is measurable with respect to $x$,

$$
\operatorname{Cov}(m,m_0)
=\operatorname{Cov}(m,E[m_0\mid x]).
$$

Cauchy-Schwarz yields

$$
\operatorname{Var}(m_0)^2
\leq \operatorname{Var}(m)\operatorname{Var}(E[m_0\mid x])
=\operatorname{Var}(m)\rho_{x,m_0}^2\operatorname{Var}(m_0).
$$

Canceling the positive variance proves the stated inequality. This reconstruction is a derivation of the note's imported variance bound. It clarifies why uncorrelated projection residuals alone are insufficient: a nonlinear $m(x)$ need not be uncorrelated with a residual that is only linearly orthogonal to $x$.

The final predictability step requires attention to the asset span. The constructed $m_0$ demonstrably prices the finite vector $r$ unconditionally. This does not by itself establish that it prices all information-conditioned trading strategies or satisfies the conditional pricing restrictions used for return predictability. Applying Ross's lemma to $m_0$ therefore requires it to be admissible for the relevant payoff and information set, not merely for the unconditional moments in equation (5). The note asserts applicability but does not establish this additional projection-to-conditional-pricing step. The safe reading is the paper's proposition **under its invoked Ross conditions**, with this scope condition made explicit; equation (6) alone is not a proof that any finite raw-asset projection supplies the necessary conditional SDF.

This matters to implementation. One should define the priced payoff span, information set, and any managed returns used in the predictability argument before forming the projected kernel. Enlarging a payoff span changes $m_0$, its variance, and its correlation with the proposed states. The reported scalar improvement cannot simply be carried from one asset universe to another.

## Calibration and empirical exercise

The empirical target is monthly S&P 500 excess returns, with Treasury bills approximating the risk-free rate. Ten predictors are taken from the Welch-Goyal data available at Goyal's website, with common availability from December 1926 through December 2008. The paper estimates a separate OLS predictive regression for each predictor. It reports intercepts, slope estimates, $t$ statistics, and in-sample $R^2$ values; there is no forecast-training split, rolling portfolio, transaction-cost analysis, or utility optimization.

Ross's numerical monthly upper bound is 7.9%, based on the additional variance restriction described on p. 184. Zhou imports correlation limits from Kan and Zhou rather than estimating them anew over the return-predictability sample. Consumption growth is the state variable. The two asset sets are a single value-weighted NYSE market index and the 25 Fama-French size/book-to-market portfolios. The corresponding correlation magnitudes are taken to be below 0.15 and 0.10.

Consequently, the ceiling calculations are

$$
B_A=7.9\%\times0.15^2=0.17775\%,\qquad
B_B=7.9\%\times0.10^2=0.07900\%.
$$

Table 1 prints $B_A=0.1777$ and $B_B=0.0790$, with all $R^2$ values and bounds measured in percentage points. The square is consequential: multiplying by 0.15 instead of $0.15^2$ would produce a radically different conclusion.

| Predictor | Slope estimate | Slope $t$ | $R^2$, % | Exceeds A? | Exceeds B? |
|---|---:|---:|---:|---|---|
| Dividend-price ratio | -0.0002 | -0.87 | 0.0766 | No | No |
| Earnings-price ratio | -0.0000 | -0.42 | 0.0178 | No | No |
| Book-to-market | 0.0177 | 2.64 | 0.7059 | Yes | Yes |
| T-bill rate | -0.0828 | -1.42 | 0.2047 | Yes | Yes |
| Default yield spread | 0.3680 | 1.46 | 0.2170 | Yes | Yes |
| Term spread | 0.1704 | 1.22 | 0.1516 | No | Yes |
| Net equity issuance | -0.1406 | -1.91 | 0.3720 | Yes | Yes |
| Inflation | -0.5306 | -1.59 | 0.2560 | Yes | Yes |
| Long-term return | 0.1078 | 1.40 | 0.1997 | Yes | Yes |
| Stock variance | -0.1055 | -0.34 | 0.0121 | No | No |

All regressions are far below Ross's 7.9% calibration. Six exceed A and seven exceed B. This count is calculated directly from the table. The prose's “except three cases” formulation fits B; A has four exceptions, including the term spread. “Bounds fail to bind” in the discussion means that observed $R^2$ exceeds the claimed upper limit, not that the constraint is merely slack. The conclusion's use of “binds” is rhetorically inconsistent with that earlier wording; the inequalities and table remove the ambiguity.

## What the evidence establishes and leaves open

The exercise is an economic restriction check using sample point estimates. It does not supply a sampling distribution for the difference between estimated $R^2$ and the bound, confidence intervals for the consumption correlations, or a joint uncertainty calculation for the variance ceiling. Only book-to-market has a conventionally large slope $t$ statistic in Table 1. A predictor can exceed a very low calibrated bound while its own evidence for nonzero predictability remains weak. Calling each such exceedance a formal statistical rejection would overstate the analysis.

There is also no estimate here of a fully parameterized consumption SDF. The example excludes a class only after imposing all the accompanying restrictions: state measurability, conditional linearity, the imported correlation information, the auxiliary variance ceiling, and the relevant Ross pricing assumptions. It does not reject every nonlinear consumption model, every multistate model, or rational time-varying expected returns as a whole.

Adding economically relevant states may raise the multiple correlation and loosen the bound. This is a meaningful diagnostic, but a higher fitted correlation obtained by searching many states may reflect sampling overfit. A practical model comparison would estimate the state projection using a stated training sample and assess its uncertainty; those exercises are extensions, not results in this paper. Likewise, structural breaks could make a single full-sample projection inappropriate. Zhou explicitly identifies omitted states, structural breaks, and small-sample uncertainty as possible explanations for the numerical violations and leaves their investigation open.

The required inputs for replication extend beyond the three-page PDF: exact historical data vintages and transformations from Welch-Goyal, the risk-free convention, the auxiliary Ross calibration, and the Kan-Zhou correlation calculations for matching consumption definitions and asset samples. The source provides no data files or code and does not resolve sample alignment between the imported correlation estimates and its December 1926-December 2008 regressions. Reproducing Table 1's multiplication is straightforward; reproducing or validating the economic ceiling is a separate empirical task.

The useful implication for a quant research program is to benchmark claimed predictability against the model that is supposed to price it, with the payoff span and conditional information stated precisely. A low return $R^2$ is not automatically innocuous for an economically restrictive SDF. Conversely, a numerical violation of a calibrated inequality is not a substitute for a properly specified statistical test or an implementable forecasting strategy.

## Source map and bibliography

Page 184 contains the predictive-return setup and Ross lemma. Page 185 contains the default SDF, conditional-linearity assumption, proposition, proof, and calibration discussion. Page 186 contains Table 1 and the limitations discussion. The mathematical reconstruction and counts of violated bounds above are explicitly derived from those displays.

The directly relevant antecedents are Stephen A. Ross, *Neoclassical Finance* (2005), p. 56; Raymond Kan and Guofu Zhou, “A New Variance Bound on the Stochastic Discount Factor,” cited by this source for the state-dependent variance restriction; and Ivo Welch and Amit Goyal, “A Comprehensive Look at the Empirical Performance of Equity Premium Prediction,” *Review of Financial Studies* 21 (2008), 1455-1508, for the predictor data. These antecedents were not independently read as part of this source note; their roles here are those described and used in the supplied article.
