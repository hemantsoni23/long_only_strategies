# Do Risk Factors Eat Alphas?

Jyh-Huei Lee and Dan Stefek. MSCI Barra Research Insights, April 2008; the cover identifies this as forthcoming in the Summer 2008 *Journal of Portfolio Management*. This note follows the 17-page April document, including its footnotes and exhibits.

Source: [RiskFactorsAlpha_LeeStefek_2008.pdf](../../Finance/RiskFactorsAlpha_LeeStefek_2008.pdf). The library file `AlphaFactor_LeeStefek_2008.pdf` is byte-identical and represents the same work. The later Bender–Lee–Stefek paper on misaligned alphas and risk factors is a separate work.

## Why this matters

An optimizer can transform a reasonable return signal into an unintended trade when its risk model describes nearly the same economic factor using a different exposure vector. The difference between the two vectors can look cheap to the risk model. If that difference is mostly measurement error, inverse-covariance weighting amplifies error rather than investment information.

The paper's counterintuitive result is that a perfect covariance matrix need not produce the highest true information ratio when the supplied alpha is noisy. A deliberately aligned but imperfect risk model can produce a better portfolio because it prevents the optimizer from exploiting discrepancies between the alpha and risk descriptions. This is a joint estimation and portfolio-construction result. It does not establish that inaccurate risk forecasts are intrinsically desirable, or that deleting factors is a sound general risk-management policy.

The contribution has three parts: an explicit decomposition of the optimizer's response to alpha; a controlled single-factor model explaining why misalignment favors noise; and a multifactor comparison of practical remedies. The evidence consists of analytical calculations and simulations calibrated to a Barra factor structure. It is not a historical trading-strategy backtest.

## Model, dimensions, and portfolio objective

For $n$ assets, let $r$ be the vector of returns. The manager uses separate linear descriptions of risk and expected exceptional return:

$$
r=X_R f_R+u_R,\qquad r=X_A f_A+u_A.
$$

The matrices $X_R$ and $X_A$ contain asset exposures, with potentially different numbers and definitions of factors. The risk-model covariance is

$$
\Sigma_R=X_R F_R X_R'+\Delta_R,
$$

where $F_R$ is the covariance of risk-factor returns and $\Delta_R$ is a diagonal specific covariance. The alpha vector is $\alpha=X_A w$, where $w$ supplies the alpha-factor forecasts. Similar economic labels do not imply identical columns in $X_A$ and $X_R$.

The paper first studies unconstrained active weights $h$ and positive risk aversion $\lambda$:

$$
\max_h\left\{\alpha'h-\frac{\lambda}{2}h'\Sigma_Rh\right\},
\qquad h^*=\lambda^{-1}\Sigma_R^{-1}\alpha.
$$

This is the exact unconstrained solution when $\Sigma_R$ is positive definite. Budget neutrality, position bounds, turnover penalties, and transaction costs are not part of this displayed problem. Adding such restrictions changes the formula. In particular, an implementation should not silently insert a full-investment constraint and still claim to reproduce equation (7).

Let $P_R=X_R(X_R'X_R)^{-1}X_R'$ be the ordinary least-squares projection onto the risk exposures, assuming full column rank. Define

$$
\alpha_{\parallel}=P_R\alpha,\qquad
\alpha_{\perp}=(I-P_R)\alpha.
$$

Then $X_R'\alpha_\perp=0$. A portfolio proportional to $\alpha_\perp$ has no exposure to the modeled common factors, but it still has specific risk. “Orthogonal alpha” therefore means orthogonal to the risk-factor exposure space, not riskless return.

For the explanatory derivation, the authors assume equal specific variances, $\Delta_R=\sigma_s^2I$. Applying the matrix inversion lemma gives their equation (7):

$$
h^*=\frac{1}{\lambda\sigma_s^2}\alpha_\perp+
\frac{1}{\lambda\sigma_s^2}
\left[I-X_R(X_R'X_R+\sigma_s^2F_R^{-1})^{-1}X_R'\right]\alpha_\parallel.
$$

This expression presumes the inverses displayed exist. Directly solving the positive-definite covariance system is preferable numerically; explicit inversion is unnecessary. The factor-spanned part is shrunk and rotated according to modeled common risk, whereas the orthogonal part receives only the specific-risk penalty.

For a single standardized risk exposure $x_R$, $x_R'x_R=n$, and factor variance $\sigma_{f_R}^2$, the result becomes

$$
h^*=\frac{1}{\lambda\sigma_s^2}
\left[\alpha_\perp+
\frac{\sigma_s^2}{n\sigma_{f_R}^2+\sigma_s^2}\alpha_\parallel\right].
$$

The relative preference for orthogonal alpha grows with $n\sigma_{f_R}^2/\sigma_s^2$. A broad universe makes diversified specific-risk exposure cheap. This is useful when the orthogonal component contains valid information and harmful when it mainly contains alpha-estimation error. The decomposition diagnoses a mechanism; it does not determine which case holds without additional information about the signal.

## Concrete timing mismatch: momentum

The opening example, pages 3–4, uses the S&P 500 as both investment universe and benchmark. At the beginning of month $t$, the alpha momentum signal sums returns from $t-2$ through $t-13$. It therefore uses twelve months while omitting the most recent month. The risk momentum signal sums $t-1$ through $t-12$. Both are twelve-month signals, but their windows differ by one month.

Each alpha and risk exposure is normalized to zero mean and unit standard deviation across the U.S. equity model's estimation universe. The authors modify the Barra U.S. equity model's momentum definition and choose risk aversion so that the resulting portfolio has unit exposure to the alpha signal.

The optimizer achieves this desired alpha exposure while carrying much less exposure to the risk momentum factor. The algebra of the two windows explains the resulting bets: their difference emphasizes the return from $t-13$ and the negative of the return from $t-1$. The portfolio can therefore become a large trade on two individual months, even though the manager intended a twelve-month momentum position. Exhibit 1 contrasts the unintended monthly exposures with the exposures obtained when risk momentum is replaced by the alpha definition.

The source does not identify a dated covariance snapshot, exact stock list, portfolio weights, or a subsequent return evaluation. Consequently, this illustration supports the existence of an optimization distortion; it does not quantify the historical profitability or transaction costs of the resulting month-specific trade. Its reproducible element is the window construction and the constrained exposure comparison, subject to obtaining the original model inputs.

## A controlled model of exposure error

The analytical experiment assumes the true return process

$$
r=xf+u,\qquad
\Sigma_{\rm true}=\sigma_f^2xx'+\sigma_s^2I,
$$

with standardized true exposure $x$, common-factor return $f$, and normally distributed specific returns. The alpha and risk systems observe noisy exposure vectors:

$$
x_A=\rho_Ax+\epsilon_A,\qquad
x_R=\rho_Rx+\epsilon_R,
$$

$$
\epsilon_A\sim N(0,(1-\rho_A^2)I),\qquad
\epsilon_R\sim N(0,(1-\rho_R^2)I).
$$

The errors are uncorrelated with true exposures, returns, and one another. The parameters $\rho_A$ and $\rho_R$ measure accuracy relative to the true exposure. The analytical computations additionally impose the sample inner-product conditions $x'\epsilon_A=x'\epsilon_R=\epsilon_R'\epsilon_A=0$ (page 7, footnote 5). Independent finite Gaussian draws satisfy these conditions in expectation, not exactly in every draw. A replication of the analytical curves must use the stipulated inner products, or explicitly construct orthogonal noise; an ordinary Monte Carlo with unrestricted draws is only an approximation to those curves.

Factor-return and factor-covariance estimation noise is set aside. The authors motivate this by a very large estimation universe and long estimation history. Under the stipulated normalization, projecting true returns on the noisy exposures scales their factor return by the exposure accuracy. The alpha forecast is $x_AE(f_A)$, while the risk model uses its own exposure and factor variance. Specific risk is nevertheless assumed known correctly.

The correlation between the two noisy exposure vectors is $\rho_{AR}=\rho_A\rho_R$ under the orthogonality assumptions. Their alpha decomposition is

$$
\alpha_\parallel=\rho_{AR}x_R E(f_A),\qquad
\alpha_\perp=(x_A-\rho_{AR}x_R)E(f_A).
$$

When risk is perfect, $\rho_R=1$, the parallel part points along true alpha and the perpendicular part is simply $\epsilon_AE(f_A)$. The optimizer's relative preference for the latter is therefore a preference for noise. A perfect covariance matrix correctly recognizes the genuine factor as risky; it cannot know that the apparently diversifiable alpha component is erroneous.

When $\rho_R<1$, substituting the two exposure equations gives the paper's footnote-6 decomposition:

$$
\alpha_\perp=
\left[\rho_A(1-\rho_R^2)x+
\epsilon_A-\rho_A\rho_R\epsilon_R\right]E(f_A).
$$

Now the risk-orthogonal component includes some true alpha. Degrading the risk exposure can therefore improve the optimized portfolio's true information ratio, despite worsening the risk representation. This result depends on the particular independent-error construction. Correlated measurement errors, systematic bias, additional factors, and time-varying risk could change the ordering.

## Analytical comparisons and numerical scale

The single-factor example uses 500 stocks, annual common-factor volatility of 1.5%, and annual specific volatility of 30%. Risk-exposure accuracy takes the values $1.0$, $0.9$, and $0.8$. Alpha accuracy varies from $0.75$ to $1.0$. The maximum attainable information ratio is normalized to one, and each candidate portfolio is evaluated using the true covariance and true expected return.

These are ex ante information ratios, not averages of realized return-to-volatility ratios. There are no confidence intervals or sampling $t$ statistics for the analytical curves. Exhibit 2 shows that the perfect-risk portfolio's information ratio is approximately 0.60 at $\rho_A=0.75$, compared with approximately 0.70 and 0.77 for risk accuracies 0.9 and 0.8. These values are readings from the graph, not a numerical data table. As alpha becomes nearly exact, the perfect-risk solution regains the advantage.

Next the authors align risk completely with the alpha exposure:

$$
\Sigma_A=\sigma_{f_A}^2x_Ax_A'+\sigma_s^2I.
$$

Because alpha lies in this model's sole factor direction, the optimized weights are proportional to $x_A$. The optimizer can no longer exploit an orthogonal discrepancy. Evaluating those weights under the true model yields equation (15):

$$
IR_A=\frac{\rho_AE(f)}
{\sqrt{\rho_A^2\sigma_f^2+\sigma_s^2/n}}.
$$

The variance terms under the square root are essential. The expression is independent of a positive scalar rescaling of the portfolio; changing risk aversion changes exposure size, not this unconstrained information ratio.

A useful implementation check, derived from the formula, is the ratio to the perfect-alpha optimum:

$$
\frac{IR_A}{IR_{\max}}=
\frac{\rho_A\sqrt{\sigma_f^2+\sigma_s^2/n}}
{\sqrt{\rho_A^2\sigma_f^2+\sigma_s^2/n}}.
$$

With the stated parameters and $\rho_A=0.75$, this ratio is about 0.862. This is a calculation from the paper's equation and inputs, not an independently reported empirical estimate. It explains why the aligned curve in Exhibit 3 remains much nearer one than the perfect-risk curve at the same alpha accuracy.

Exhibit 4 repeats the comparison with annual factor volatilities of 0.5%, 1%, 1.5%, and 2%, maintaining the other settings. Misalignment is most damaging for the stronger common factors because the optimizer suppresses factor-spanned alpha more aggressively relative to orthogonal error. Alignment delivers less incremental benefit when factor risk is small relative to average diversified specific risk.

In the simple model, the aligned risk forecast is correct for portfolios proportional to the alpha exposure, despite being an imperfect covariance model for arbitrary portfolios. This statement is portfolio-specific. It does not imply that the aligned model forecasts every portfolio correctly, nor that the same property survives a restricted investment subset. The multifactor experiment explicitly shows that aligned approaches can misforecast risk.

## Four remedies and an implementable emulation

Pages 10–11 distinguish four interventions:

1. Drop the related factors from the risk model.
2. Substitute the alpha exposures for the related risk exposures while retaining the existing factor covariance and specific risk.
3. Rebuild a risk model using the alpha factors and retained risk factors, re-estimating factor returns and their covariance.
4. Emulate that rebuilt model using the existing risk model.

Dropping a factor and substituting an exposure are different operations. The former removes modeled common risk, while the latter keeps a covariance structure but associates it with a different loading vector. Rebuilding requires historical estimation work; substitution alone does not recreate that work.

For emulation, form the $n\times K_C$ exposure matrix $X_C$ from the alpha factors and retained risk factors. With diagonal weighting matrix $W$, define the factor-portfolio matrix

$$
B_C=(X_C'WX_C)^{-1}X_C'W.
$$

Each row is an asset portfolio with unit exposure to its corresponding new factor and zero exposure to the other columns of $X_C$: $B_CX_C=I$. Full rank and a consistent factor normalization are necessary. In the numerical exercise, $W=I$; the source notes that other weighting choices are used in practice.

These are weighted-regression factor portfolios. Their minimum-norm interpretation uses the metric implied by $W^{-1}$; with arbitrary $W$, they should not be described as the minimum-variance portfolios under the entire old covariance matrix. That stronger assertion would require a different optimization.

The emulated factor covariance and asset covariance are

$$
F_C=B_C(X_RF_RX_R')B_C',
\qquad \Sigma_C=X_CF_CX_C'+\Delta_R.
$$

Equation (18) uses the old model's common-factor covariance, not its full covariance including specific risk. Replacing the inner term with $\Sigma_R$ changes the method and passes specific risk through the factor portfolios before adding a specific-risk matrix again. A replication should preserve the published construction and assess its consequences explicitly.

A practical numerical sequence is to normalize and assemble $X_C$, solve the weighted least-squares systems for $B_C$, form the common-factor covariance mapping, symmetrize numerical roundoff, and check positive semidefiniteness before optimizing. A diagonal positive specific covariance makes $\Sigma_C$ positive definite even when the mapped common-factor covariance is rank deficient. These computational checks are implementation guidance, not additional estimators proposed in the paper.

## Multifactor simulation design and results

The richer experiment treats the Barra U.S. equity model as the true data-generating covariance. It contains 55 industry factors and 13 style factors, including value and momentum. Exposures are assumed fixed through time. The alpha model uses value and momentum, while the risk model retains the full factor list.

True alpha is the equally weighted average of the true value and momentum exposures. The manager's alpha is the equally weighted average of noisy estimates of those two exposures. Both value and momentum have the same accuracy within each model, permitting one $\rho_A$ and one $\rho_R$. Errors in the alpha and risk exposure estimates are uncorrelated. The risk model knows every other exposure and specific risk correctly; its accuracy for value and momentum is set to 0.9.

The authors again use the S&P 500 as investment universe and benchmark. For each alpha-accuracy setting and method, they average 100 simulations. Each simulation generates different value and momentum exposures for the alpha and risk models and re-estimates the models. They calculate the optimized portfolios' ex ante information ratios with the true model. There is no rolling training/validation/test schedule and no realized price path or transaction-cost simulation.

In the unconstrained long-short results, Exhibit 6, substitution, rebuilding, and emulation produce very similar and substantially better information ratios than the perfect-risk portfolio when alpha is materially noisy. At the left of the graph, $\rho_A=0.75$, the perfect-risk result is roughly 0.39, the manager's imperfect-risk result about 0.50, dropping factors about 0.58, and the three alignment methods about 0.60–0.62. These are approximate exhibit readings. The comparison is internally normalized; it should not be presented as an achievable annual live-strategy information ratio.

Exhibit 7 evaluates risk forecast accuracy as forecast active volatility divided by true active volatility. The perfect model is at 100%. Dropping factors underforecasts, falling approximately from 87% to 64% across the plotted alpha accuracies. Substitution overforecasts at poor alpha accuracy, approximately 123% at 0.75, but falls below 100% near the high-accuracy end. Emulation increasingly underforecasts as alpha becomes accurate, because the underlying risk model from which it is built is imperfect. Rebuilding with alpha factors also overforecasts over much of the range, unlike the exact aligned-portfolio property of the single-factor example.

This distinction is operationally important: a method can improve true return per unit risk while delivering a biased risk forecast. Portfolio selection and risk calibration must therefore be evaluated separately. A risk-targeting process that scales weights with the biased forecast can materially change leverage, even if the unscaled information ratio is unchanged.

Finally, Exhibits 8A and 8B impose long-only holdings and target active risk levels of 1.5% and 3%. Preventing short positions reduces the optimizer's ability to exploit noisy relative-exposure trades. The information-ratio differences narrow, and the differences narrow further in the displayed 3% case. The source does not provide the full optimization specification, benchmark weight snapshot, or target-risk calibration procedure needed to recreate every point. In particular, a reproducer must distinguish active weights from total holdings when imposing long-only bounds.

## Reproduction limits and research use

The analytical mechanism and covariance mappings can be reproduced from the equations and stated parameter values. Exact reproduction of the multifactor exhibits requires missing inputs: the dated Barra covariance and exposure snapshot, S&P 500 constituent and benchmark weights, the exposure-noise generation and normalization details, random seeds, and complete optimization settings. Graphs provide approximate outcomes, not machine-readable results or Monte Carlo uncertainty.

The paper intentionally omits much covariance-estimation error, assumes constant true exposures, treats specific risk as known, and ignores trading costs and implementation frictions. Its strongest result is consequently the mechanism linking exposure mismatch to optimizer amplification of noisy alpha. It offers useful candidate remedies, with controlled evidence of their behavior, rather than a universally preferred production risk model.

For a quantitative research pipeline, the appropriate diagnostic is to project alpha into and outside the modeled factor space, inspect the economic content of the orthogonal component, and compare resulting portfolios using an independent risk assessment. Alignment should be judged by true or held-out portfolio outcomes and calibration, not only by the apparent smoothness of optimized holdings. Those held-out tests are a natural application of the paper's argument; they are not tests carried out in this source.
