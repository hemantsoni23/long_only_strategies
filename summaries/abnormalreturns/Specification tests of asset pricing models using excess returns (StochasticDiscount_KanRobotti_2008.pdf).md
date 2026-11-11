# Specification tests of asset pricing models using excess returns

## Source and scope

**Raymond Kan and Cesare Robotti**, *Journal of Empirical Finance* 15 (2008), pp. 816–838, DOI 10.1016/j.jempfin.2008.03.003. Original file: [StochasticDiscount_KanRobotti_2008.pdf](../../Finance/StochasticDiscount_KanRobotti_2008.pdf).

All 23 PDF pages were read, including Appendix A's proofs. Critical equations and all five empirical tables were visually checked on PDF pp. 6, 10–12, 14–17, and 19. A printed error in the parameter influence function was independently checked by differentiation and a finite-difference calculation; it is identified below. No original empirical data or author code accompany this local PDF.

## Why this matters

Excess-return pricing equations are homogeneous in the stochastic discount factor. If its mean is not identified, an apparently harmless choice of intercept can make a poor economic model look good by shrinking its kernel toward zero. Kan and Robotti show that a fixed-intercept linear SDF can have its measured pricing performance changed dramatically merely by adding constants to its factors. Models that span the same centered factor information can consequently receive different rankings.

Their solution is to compare kernels with a common mean, ordinarily one, and to measure the distance to correctly pricing kernels with that same mean. For a linear SDF this means centering the factors and weighting expected-return errors by the inverse covariance matrix of excess returns. The resulting distance has a transparent geometric interpretation and is invariant to nonsingular affine changes of factor coordinates.

A second contribution concerns coefficient inference. A fitted model can be wrong and still produce a well-defined best-fitting parameter. Its sampling uncertainty then includes terms discarded by standard errors derived under exact pricing. These terms can be especially large for macroeconomic factors that are poorly mimicked by asset returns. A high conventional factor t-statistic is therefore not sufficient evidence that the factor carries a reliably estimated risk price.

## Setup, normalization, and the failure of fixed intercepts

Let $r$ be an $N$-vector of zero-cost payoff returns, conventionally excess returns, and $f$ a $K$-vector of factors with $N>K$. Define

$$
\mu_f=E[f],\quad\mu_r=E[r],\quad
V_{ff}=\operatorname{Var}(f),\quad
C=\operatorname{Cov}(r,f),\quad\Sigma=\operatorname{Var}(r),
$$

and $U=E[rr']=\Sigma+\mu_r\mu_r'$. Relevant matrices are nonsingular and $C$ has full column rank. A correctly pricing SDF $y$ satisfies $E[ry]=0$. With parameters $\lambda$, the error vector is $e(\lambda)=E[ry(\lambda)]$ and a weighted misspecification measure is

$$
Q_W=\min_\lambda e(\lambda)'We(\lambda),
$$

where $W$ is symmetric positive definite. Comparing different models requires a consistent choice of weighting matrix and asset set.

The unrestricted linear form $y=\lambda_0-f'\lambda$ is unusable with only excess returns because $(\lambda_0,\lambda)=(0,0)$ prices every zero-cost payoff trivially. A common convention sets $\lambda_0=1$. It gives

$$
y=1-f'\lambda,\qquad
B=E[rf']=C+\mu_r\mu_f',\qquad
e=\mu_r-B\lambda,
$$

$$
\lambda_W=(B'WB)^{-1}B'W\mu_r,
$$

$$
Q_W=\mu_r'W\mu_r-
\mu_r'WB(B'WB)^{-1}B'W\mu_r.
$$

Adding a constant to $f$ changes $\mu_f$ but not $C$. It therefore changes $B$, the fitted parameters, and the residual distance. Under misspecification, the paper proves that the largest attainable value over factor means is $\mu_r'W\mu_r$, obtained at

$$
\mu_f=-\frac{C'W\mu_r}{\mu_r'W\mu_r},
$$

while the infimum is zero as factor means become arbitrarily large along suitable directions. Large factor means make the $\mu_r\mu_f'$ term dominate the pricing-error design, allowing the model to fit through normalization rather than economically relevant covariance.

The appendix decomposes $C$ into a component along $\mu_r$ and a $W$-orthogonal component. A rank-one inverse identity reduces the distance to a positive numerator divided by $1$ plus a quadratic form in the shifted factor mean. This proves the full range of manipulability. In finite samples residuals are generally nonzero even under a correct population model, so the sample version can be affected as well.

This issue is specific to the specified normalization and test system. The authors note that continuous-updating GMM has an invariance property absent from ordinary two-step and iterative implementations. They also distinguish the gross-return case: including positive-price assets identifies additional scale information, so not every excess-return argument transfers unchanged.

## Centering factors and comparing a common kernel mean

Instead use

$$
y=1-(f-\mu_f)'\lambda.
$$

Now $E[y]=1$ for every parameter vector, and

$$
e(\lambda)=\mu_r-C\lambda.
$$

The misspecification measure depends on the covariance column space, not the arbitrary factor means. An invertible coordinate transformation $\widetilde f=Af+b$ changes the coefficient representation but preserves the kernel family and fitted distance. A common nonzero kernel mean other than one merely rescales squared distances by that common mean squared; rankings are unchanged.

With unit mean, the pricing errors are also expected-return errors:

$$
E[ry]=E[r]+\operatorname{Cov}(r,y).
$$

Thus the model-implied mean excess return is $-\operatorname{Cov}(r,y)$. This interpretation is obscured when two model kernels have substantially different means. Centering does not assert that an actual risk-free asset always has a gross return of one; it is a normalization of the excess-return pricing system. A known constant risk-free gross return would imply kernel mean $1/R_0$ instead.

Estimating $\mu_f$ is part of the procedure, not a nuisance that can always be treated as known. Under exact pricing it drops out of some first-order distance-test results. Under misspecification its role must be handled consistently with the sample mean and covariance estimation.

## Modified HJ distance: definition and proof

Ordinary HJ distance measures the smallest $L^2$ change from a candidate kernel to any correctly pricing kernel, without fixing the repaired kernel's mean. Its squared value uses $U^{-1}$. If candidates are constrained to a common mean, Kan–Robotti argue that the repair should preserve that mean too.

For payoff vector $x$ with price vector $q$, let $E[y]=c$ and $e=E[xy]-q$. The modified distance is

$$
\delta_m^2=
\min_m E[(m-y)^2]
\quad\text{subject to}\quad
E[xm]=q,\quad E[m]=c.
$$

Lagrange multipliers show the least-norm repair is

$$
m^*=y-e'\operatorname{Var}(x)^{-1}(x-E[x]),
$$

which preserves the mean and removes the pricing errors. Hence

$$
\boxed{\delta_m^2=e'\operatorname{Var}(x)^{-1}e.}
$$

For a parametrized candidate, minimize this expression over its parameters. This result applies to nonlinear as well as linear kernels, provided the candidate mean is fixed and the required covariance inverse exists. Neither the original nor modified unconstrained $L^2$ projection imposes positivity of the repaired SDF.

For centered linear factors,

$$
\lambda_m=(C'\Sigma^{-1}C)^{-1}C'\Sigma^{-1}\mu_r,
\qquad e_m=\mu_r-C\lambda_m,
$$

$$
\delta_m^2=e_m'\Sigma^{-1}e_m.
$$

The corresponding standard HJ estimate uses $U^{-1}$ instead. Sherman–Morrison algebra gives

$$
\delta_{HJ}^2=\frac{\delta_m^2}{1+\delta_m^2},\qquad
\lambda_{HJ}=\frac{\lambda_m}{1+\delta_m^2}.
$$

These identities hold exactly for sample analogues too. Therefore centered linear models have identical rankings under the two distances. The change in economic normalization from *raw* to centered factors can change rankings; the monotone transformation between the two *centered* distance definitions cannot. Confusing these two comparisons obscures the paper's main point.

The modified distance also equals a GLS cross-sectional beta-pricing residual criterion. With $\beta=CV_{ff}^{-1}$ and residual covariance $\Sigma_\varepsilon=\Sigma-CV_{ff}^{-1}C'$, the appropriately minimized criterion can be expressed using $\Sigma_\varepsilon^{-1}$ and the span of $\beta$. This connects the SDF geometry with familiar cross-sectional regression tests.

If a constant risk-free gross return $R_0$ is added to the excess-return test assets and the kernel intercept is freely estimated, ordinary HJ distance on the augmented system equals $\delta_m/R_0$. A time-varying short rate does not satisfy that exact constant-rate identity. For models such as a zero-beta CAPM that are not intended to price a lending rate, the paper instead permits excess returns relative to a risky benchmark. The common-mean comparison then restricts the competing zero-beta rates consistently.

## Inference at zero distance and away from zero

Under exact pricing, the sample squared distance is a second-order statistic:

$$
T\widehat Q_W\ \Rightarrow\ 
\sum_{j=1}^{N-K}\xi_j\chi^2_{1,j}.
$$

Let $S_{22}$ be the long-run covariance of the pricing moments $r_ty_t$ at the true parameter. Let $P$ have orthonormal columns spanning the complement of $W^{1/2}C$. Then the $\xi_j$ are eigenvalues of

$$
P'W^{1/2}S_{22}W^{1/2}P.
$$

In the modified-distance test $W=\Sigma^{-1}$. Exact pricing removes first-order contributions from estimating factor means and the consistent weighting matrix in this particular statistic. These cancellations are properties of the null and should not be exported to a misspecified model.

For a nonzero population distance, ordinary delta-method asymptotics apply. Define

$$
u_t=e_m'\Sigma^{-1}(r_t-\mu_r),\qquad
y_t=1-\lambda_m'(f_t-\mu_f).
$$

An influence quantity for $\widehat\delta_m^2$ is

$$
q_t=2u_ty_t-u_t^2+\delta_m^2.
$$

Its long-run variance supplies the asymptotic variance of $\sqrt T(\widehat\delta_m^2-\delta_m^2)$. In a no-serial-correlation implementation, use the sample mean of $\widehat q_t^2$ and divide by $T$ for the variance of the estimator itself. With dependence, use an appropriate long-run covariance estimator. For distance rather than squared distance, divide this asymptotic variance by $4\delta_m^2$.

The null $\delta_m=0$ is precisely where that latter division and first-order approximation fail. A t-ratio formed with the nonzero-distance standard error is not a valid exact-pricing test. The paper emphasizes this distinction when reporting confidence intervals under misspecification. The bounded ordinary squared distance, $\delta_{HJ}^2<1$, also makes finite-sample tail approximation by an unbounded chi-square mixture potentially poor.

## Misspecification-robust coefficient standard errors

Let

$$
H=(C'\Sigma^{-1}C)^{-1},\qquad
A=HC'\Sigma^{-1},\qquad
v_t=(f_t-\mu_f)-C'\Sigma^{-1}(r_t-\mu_r).
$$

Here $v_t$ is the factor-mimicking regression residual. The coefficient influence function derived from the normal equations is

$$
\boxed{q_{\lambda,t}=A(r_t-\mu_r)y_t+Hv_tu_t+\lambda_m.}
$$

The estimator's asymptotic covariance is the long-run covariance of this vector. Under correct specification $e_m=0$, so $u_t=0$ and the middle term disappears. Under misspecification, dropping it discards uncertainty associated with unspanned factor variation interacting with model pricing errors.

**Printed formula correction.** Equation (71), visually checked on journal p. 826, prints $(1-y_t)$ instead of $y_t$ in the first term. This conflicts with the derivative in Lemma 4, the stated correct-model reduction in equation (73), and the transformation to equation (72). Direct differentiation gives the boxed expression above. A numerical directional-derivative check on a nonsingular synthetic covariance system agreed with the corrected formula to $7.3\times10^{-11}$, while the printed expression differed by about 0.689. This is a check of the algebra, not an empirical replication of the paper.

To see the derivative directly, differentiate $C'\Sigma^{-1}(\mu_r-C\lambda_m)=0$. The terms are

$$
d\lambda_m=H(dC)'\Sigma^{-1}e_m
+A\,d\mu_r-A(dC)\lambda_m
-A(d\Sigma)\Sigma^{-1}e_m.
$$

Insert the sample-moment influences $d\mu_r=r_t-\mu_r$, $dC=(r_t-\mu_r)(f_t-\mu_f)'-C$, and $d\Sigma=(r_t-\mu_r)(r_t-\mu_r)'-\Sigma$. The pricing first-order condition $C'\Sigma^{-1}e_m=0$ eliminates constant residual terms and produces the corrected expression. This route avoids transcribing a long Kronecker-product derivative incorrectly.

Under independent elliptical observations with finite fourth moments and kurtosis parameter $\kappa$ (zero in the Gaussian case), the asymptotic covariance of the modified-distance coefficient estimator is

$$
\Omega_{\lambda_m}=
[1+(1+\kappa)\lambda_m'V_{ff}\lambda_m]H
+(1+2\kappa)\lambda_m\lambda_m'
+(1+\kappa)\delta_m^2H(V_{ff}-C'\Sigma^{-1}C)H.
$$

The last term is positive semidefinite. It is large when mispricing is large, tails are heavy, or factors are poorly mimicked by returns. It can vanish for perfectly spanned factors. This monotone covariance comparison is an elliptical-case result for $\lambda_m$; the paper does not establish that every robust standard error increases under every distribution or for the ordinary-HJ coefficient estimator.

For $\lambda_{HJ}=\lambda_m/(1+\delta_m^2)$, a convenient implementation applies the derivative of that transformation jointly to $q_{\lambda,t}$ and $q_t$. Under exact pricing the two coefficient estimators share their first-order distribution. Away from exact pricing their pseudo-true parameters and covariance matrices differ.

## Empirical evidence and its limits

The first application compares Jagannathan–Wang's conditional CAPM (JW) with the Fama–French three-factor model (FF3), using monthly excess returns on 100 size/beta-sorted NYSE–AMEX portfolios, July 1963–December 1990. JW uses a market return, a lagged corporate yield spread, and per-capita labor-income growth. FF3 uses excess market return, SMB, and HML. The table's standard errors assume no serial correlation.

With raw-factor fixed-intercept kernels, Table 1 reports HJ distances of 0.1442 for JW and 0.5494 for FF3, but their estimated kernel means are 0.1228 and 0.9478. Much of the apparent performance gap is therefore a normalization gap. After affine factor shifts, the displayed table gives 0.5832 for JW and 0.0136 for FF3, with kernel means 1.0005 and 0.0050. These numbers illustrate manipulation, not improved economic models.

There are discrepancies between the surrounding prose and Table 1. The table note specifies JW shifts of 0.0171, 0.0121, and 0.0059, whereas the prose prints different precision and a labor-growth shift of 0.059. The prose gives a transformed FF3 distance of 0.0105, while the table displays 0.0136. The table values and table-note shifts are used here; the original code is needed to resolve the discrepancy conclusively.

After centering, the comparison is much closer:

| Quantity | JW | FF3 |
|---|---:|---:|
| Centered ordinary HJ distance | 0.5624 | 0.5726 |
| Modified HJ distance | 0.6802 | 0.6984 |
| Asymptotic zero-distance p-value, ordinary metric | 0.441 | 0.225 |
| Asymptotic zero-distance p-value, modified metric | 0.016 | displayed 0.000 |

The last row's displayed zero is rounded, not a mathematical probability of zero. The sharp p-value differences do not indicate different exact information in the two centered distance statistics: their sample values are monotonic transformations. The authors interpret the discrepancy as evidence that finite-sample asymptotic approximations can be unreliable. An exact test based on one statistic and transformed consistently would give the same probability as the other.

The modified-distance labor-income coefficient has a conventional t-ratio of 2.29 but a misspecification-robust value of 1.53. The robust JW and FF3 distance intervals overlap substantially: modified-distance intervals are (0.5655, 0.8311) and (0.5870, 0.8433). Overlap alone is not a formal paired model-comparison test because the estimates are dependent; it supports the authors' descriptive conclusion that the raw-distance ranking vastly overstated the separation. These intervals are constructed for nonzero distances and must not be repurposed as the null mixture-chi-square test.

The second example uses annual real excess returns on the 25 size/book-to-market portfolios, 1954–2003, comparing a fourth-quarter-to-fourth-quarter consumption-growth CAPM with FF3. Raw-factor distances are 0.2888 versus 0.6316 and kernel means 0.1948 versus 0.6912. Centering and using the modified metric yields 1.4239 versus 1.4048: the ranking reverses, although the distance difference is small. The consumption coefficient t-ratio falls from 13.36 under the original specification/inference to 2.48 with the revised specification and robust error. This change combines normalization and inference adjustments; it should not be attributed wholly to either one.

The third example focuses on robust coefficient errors across six models using 25 size/book-to-market portfolios. Most samples run January 1952–December 2006, 660 months. Consumption data begin February 1959, 575 months. Campbell's model uses February 1952–December 1990, 467 months. These unequal samples prevent interpreting the table as a clean common-sample model-ranking experiment.

Selected conventional and robust t-ratios are:

| Model/factor | Conventional | Robust |
|---|---:|---:|
| CAPM market | 3.33 | 3.32 |
| Consumption CAPM growth | 2.96 | 1.91 |
| JW labor income | −2.89 | −1.39 |
| Campbell labor income | 2.28 | 1.43 |
| Campbell relative Treasury-bill rate | −2.40 | −1.79 |
| FF3 market | 4.37 | 4.37 |
| FF3 HML | 5.60 | 5.61 |

These results fit the factor-mimicking explanation: macroeconomic factors can have a large unspanned component, whereas stock-return factors are better represented in the test-asset space. The historical “FF5” in this paper is the 1993 stock-and-bond specification adding TERM and DEF to market/SMB/HML. It is not the later profitability/investment five-factor model. Its weaker robust t-ratios should be read with that identity in mind.

A coefficient called “priced” here is a statistically nonzero coefficient in a specified best-fitting kernel, conditional on the other factors, test assets, weighting metric, and data frequency. It is not automatically a structural preference parameter or the factor's own expected return. Under misspecification it is a pseudo-true coefficient selected by the loss function. Near-zero factor-return covariance also threatens the full-rank identification assumption; robust standard errors do not cure unidentified factors.

## Reproduction protocol and missing inputs

A reproducible implementation can use a small sequence of matrix and time-series operations:

1. Align all factors and excess returns, document gross/net and decimal/percentage conventions, and use a common calendar when comparing models. Distinguish factors measured in returns, growth rates, and yield spreads.
2. Compute sample means and covariances with a stated denominator. Form $C$, $\Sigma$, and $U$, and check rank/conditioning before inversion. Report factor-mimicking fit because it controls the scale of the robustness adjustment.
3. Fit the centered model with covariance weighting, obtain $\widehat\lambda_m$, $\widehat e_m$, and $\widehat\delta_m^2$, and verify $C'\Sigma^{-1}e_m\approx0$.
4. Calculate ordinary centered HJ quantities independently and verify the exact monotone-transform identities. This is a strong internal check of centering, weights, and coefficient normalization.
5. Build the corrected coefficient influence vectors and distance influence series. Their sample means should be approximately zero. Estimate long-run covariances; divide by sample size before reporting coefficient standard errors.
6. Use the mixture-chi-square framework for exact-pricing tests and the nonzero-distance delta method for estimation around a misspecified model. Do not select the inference formula merely because it produces a favorable result.
7. Apply arbitrary nonsingular affine factor transformations as an implementation audit. The fitted centered kernel, residual criterion, and economic results should remain invariant, although coefficient coordinates and individual coefficient interpretations can change under factor mixing.

The PDF gives sufficient algebra to implement these steps and enough table values to check scale. Exact replication requires the original 100-portfolio file, the vintage and timing of JW labor income/yield spreads, the annual consumption construction, Campbell's factor file, the historical bond factors, and the authors' numerical treatment of the table/prose discrepancies. Those files are not included. The paper's reported applications assume uncorrelated influence quantities over time; extending them to a HAC estimator is supported by the theory but is a new robustness exercise.

No trading costs, portfolio turnover, capacity, or out-of-sample profit results are reported. The distance measures diagnose how a kernel fits the chosen pricing equations. Their value for investment research is methodological: comparisons should survive changes of factor units and origins, and coefficient significance should survive allowing the model to be imperfect. Neither a low distance nor a robust t-statistic alone establishes a monetizable strategy.

## Portfolio interpretation of the modified distance

The geometry gives a useful economic interpretation and an independent numerical check. Let $\lambda$ minimize the centered criterion and let $e=\mu_r-C\lambda$. Its first-order condition is

$$
C'\Sigma^{-1}e=0.
$$

Define the zero-cost portfolio weights $w=\Sigma^{-1}e$. The portfolio is covariance-orthogonal to every included factor because $C'w=0$. Its mean and variance satisfy

$$
E[w'r]=w'\mu_r=w'e=\delta_m^2,
\qquad
\operatorname{Var}(w'r)=w'\Sigma w=\delta_m^2.
$$

The equality in the mean follows from $w'C\lambda=0$. Provided the distance is positive, this portfolio therefore has squared Sharpe ratio $\delta_m^2$. More generally, for any weights $a$ satisfying $C'a=0$,

$$
(a'\mu_r)^2=(a'e)^2
\le (a'\Sigma a)(e'\Sigma^{-1}e),
$$

so no such factor-orthogonal portfolio has a larger squared Sharpe ratio. Thus the modified distance measures the maximum squared Sharpe ratio left in the test-asset span after imposing covariance orthogonality to the factors. This derivation is a consequence of the paper's population projection geometry, not a reported trading backtest.

This interpretation clarifies the role of the asset menu. Adding assets expands the possible residual portfolio directions and can reveal misspecification missed by a smaller test set. In an estimated sample it also increases covariance estimation noise and may make the apparent best residual portfolio unstable. The formula does not account for position limits, transaction costs, estimation risk, or out-of-sample degradation. If $\delta_m=0$, the particular weights above are zero and there is no nontrivial residual direction obtained from them; the zero-distance conclusion concerns the population model restrictions.

The same geometry makes affine invariance operational. For new factors $f^*=Af+b$ with nonsingular $A$, centering removes $b$, and the new covariance is $C^*=CA'$. Setting $\lambda^*=A'^{-1}\lambda$ preserves the random variable $\lambda' (f-\mu_f)$, the fitted expected-return vector, and the minimized modified distance. A replication can use arbitrary nonzero changes of units and additive shifts as a deterministic diagnostic: the criterion and fitted kernel should remain unchanged after transforming coefficients appropriately. Failure of this check often indicates uncentered factors, mismatched sample dates, or inconsistent covariance normalization.

## Mean-zero influence functions as a formula check

The corrected coefficient influence function in the main derivation can be checked without simulation. By the optimality condition,

$$
E[(r-\mu_r)y]=-C\lambda,
\qquad A C=I_K.
$$

Consequently $E[A(r-\mu_r)y]=-\lambda$. Also $v$ is the residual from the linear projection of centered factors on centered returns, while $u$ is a linear combination of centered returns. Hence $E[vu]=0$. Adding the final $+\lambda$ makes the complete influence function have expectation zero, as it must.

Using the printed $(1-y)$ in place of $y$ reverses the first expectation: it produces $+\lambda$, so retaining the final $+\lambda$ gives mean $2\lambda$ in general. This is a second, elementary reason the printed expression cannot be the influence function. It complements the derivative calculation and finite-difference check and avoids relying on the corrected expression merely because it resembles a familiar regression formula.

An empirical implementation should check that estimated influence series have sample means close to zero under internally consistent moment definitions, and should compare an analytic derivative with a numerical perturbation of the moment vector. These checks test algebra and code. They do not establish that asymptotic inference is reliable in a short or weakly identified financial sample, and they do not replace the required serial-dependence adjustment.
