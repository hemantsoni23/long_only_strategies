# The Statistics of the Information Ratio

Philippe Bertrand and Costin Protopopescu (2010), *International Journal of Business* 15(1), 71–86. [Source PDF](../../Finance/InformationRatioEstimation_BertrandProtopopescu_2010.pdf). All 17 PDF pages, including the two-page mathematical appendix and the final reproduction notice, were read. The moment matrix, derivatives, calibration, and central numerical sensitivity figures were checked visually.

## Why this matters

An information ratio is an estimated ratio of an active mean to tracking-error volatility. Its uncertainty depends on more than the precision of the mean alone. Estimation of the denominator and its covariance with the numerator matter, particularly when active returns are asymmetric or heavy-tailed. Bertrand and Protopopescu give a delta-method variance expressed through the joint raw moments of portfolio and benchmark returns, then investigate how its value changes when selected moments are varied.

The main theorem is implementable and has a simpler equivalent representation: apply the ordinary ratio-of-mean-to-standard-deviation calculation to the single active-return series. The two-variable formulation is useful for decomposing where active-return moments come from; a stochastic benchmark does not create a fundamentally new type of statistic. The source’s Gaussian special case reduces exactly, at first asymptotic order, to the familiar $1+IR^2/2$ variance factor.

Several details require qualification before implementation. The stated Gaussian covariance matrix does not produce the correlation and information ratio quoted beside it. Finally, holding high-order raw moments fixed while changing means and covariances does not automatically define a feasible probability distribution. The numerical plots are therefore reported as source sensitivity calculations, rather than validated comparative statics of an identified family of return distributions.

## The statistic and assumptions

For a synchronized one-period portfolio return $P_t$ and benchmark return $B_t$, define active return $A_t=P_t-B_t$. Let

$$
\mu=E[A_t]=\mu_P-\mu_B,
\qquad v=\operatorname{Var}(A_t)
=\sigma_P^2+\sigma_B^2-2\rho\sigma_P\sigma_B,
\qquad \theta=IR=\frac{\mu}{\sqrt v}.
$$

This is benchmark-relative average return divided by tracking-error volatility. It is not the regression alpha divided by residual volatility unless additional restrictions make those objects coincide. A separate risk-free return does not enter the active-return definition. Both return legs must use matching dates, currency, period length, and accounting treatment.

The core asymptotic calculation requires that the joint vectors $(P_t,B_t)$ are independent and identically distributed across dates, that relevant fourth moments exist, and that $v>0$. Contemporaneous cross-correlation between the two legs is allowed. Saying only that each marginal return series is iid is insufficient if cross-date dependence remains in the joint vectors. For the Gaussian simplification, joint normality is sufficient; normal marginals alone do not imply a normal active return.

The source uses empirical raw moments with denominator $T$. Its tracking-error estimate consequently has denominator $T$, not $T-1$. Using the unbiased sample variance changes finite-sample quantities but not the leading asymptotic formula. Throughout this note, $\Omega$ denotes the variance of the limiting $\sqrt T$-scaled error, while $\Omega/T$ is the approximate sampling variance of the estimated ratio. This distinction prevents an extra factor of $T$ from entering the code.

## A reproducible five-moment calculation

Define population raw moments $m_{kl}=E[P_t^kB_t^l]$, estimates

$$
\hat m_{kl}=\frac1T\sum_{t=1}^{T}P_t^kB_t^l,
$$

and the vector

$$
M=(m_{10},m_{01},m_{20},m_{02},m_{11})'.
$$

It is useful to distinguish the active raw second moment $q$ from its variance:

$$
\mu=m_{10}-m_{01},\qquad
q=m_{20}+m_{02}-2m_{11},\qquad v=q-\mu^2,
\qquad \varphi(M)=\mu v^{-1/2}.
$$

Let $h_t=(P_t,B_t,P_t^2,B_t^2,P_tB_t)'$. The iid multivariate central limit theorem gives

$$
\sqrt T(\hat M-M)\Rightarrow N_5(0,\Sigma),
\qquad \Sigma=\operatorname{Cov}(h_t).
$$

An unambiguous way to construct all 25 matrix entries is to attach exponent pairs $(a_i,b_i)$ to the five components and use

$$
\Sigma_{ij}=m_{a_i+a_j,b_i+b_j}-m_{a_i,b_i}m_{a_j,b_j}.
$$

This matrix is the covariance of single-observation moment contributions. The covariance of their sample mean is $\Sigma/T$ under iid sampling. The source occasionally uses moment-covariance language without making that scaling explicit; the theorem itself supplies the $1/T$ factor.

For direct implementation, the lower triangle is

$$
\Sigma=\begin{pmatrix}
m_{20}-m_{10}^2 & * & * & * & *\\
m_{11}-m_{10}m_{01} & m_{02}-m_{01}^2 & * & * & *\\
m_{30}-m_{20}m_{10} & m_{21}-m_{20}m_{01} & m_{40}-m_{20}^2 & * & *\\
m_{12}-m_{02}m_{10} & m_{03}-m_{02}m_{01} & m_{22}-m_{02}m_{20} & m_{04}-m_{02}^2 & *\\
m_{21}-m_{11}m_{10} & m_{12}-m_{11}m_{01} & m_{31}-m_{11}m_{20} & m_{13}-m_{11}m_{02} & m_{22}-m_{11}^2
\end{pmatrix},
$$

with the upper triangle completed by symmetry. Fourteen nonconstant moments through total degree four are needed. These are moments *through* degree four, not strictly below four as some source prose suggests.

Differentiating the ratio gives the gradient in the same component order:

$$
g=\nabla\varphi(M)=v^{-3/2}
\begin{pmatrix}q\\-q\\-\mu/2\\-\mu/2\\\mu\end{pmatrix}.
$$

For example, $\partial v/\partial m_{20}=1$, so $\partial\varphi/\partial m_{20}=-\mu/(2v^{3/2})$. The PDF appendix on printed page 85 likewise gives the negative sign for both $m_{20}$ and $m_{02}$ derivatives. Its derivatives agree with the vector above.

The delta method now gives

$$
\sqrt T(\widehat{IR}-IR)\Rightarrow N(0,\Omega),
\qquad \Omega=g'\Sigma g,
\qquad \operatorname{Var}(\widehat{IR})\approx\frac{\Omega}{T}.
$$

The proof is a first-order Taylor expansion at the population moments. With $v>0$, the map is smooth near $M$; the moment error is $O_p(T^{-1/2})$, so the remainder multiplied by $\sqrt T$ is $o_p(1)$. Substituting the multivariate central limit theorem produces the scalar Gaussian limit. The source’s appendix calls on a law of large numbers at this point and retains a five-dimensional normal label for the transformed quantity; the needed result is the central limit theorem and the transformed limit is one-dimensional. These are notation/proof-presentation repairs, not changes to the delta-method argument.

## Equivalent active-return formula and a shorter proof

The following reduction is derived here to make the theorem easier to implement and audit. Write $Z=A-\mu$ and let $\gamma_1=E[Z^3]/v^{3/2}$ and $\gamma_2=E[Z^4]/v^2$ be active-return skewness and ordinary kurtosis. Ordinary kurtosis is 3, rather than 0, for a Gaussian variable.

The first-order influence of the estimated ratio is

$$
\psi(A)=\frac{Z}{\sqrt v}
-\frac{\mu}{2v^{3/2}}(Z^2-v)
=\frac{Z}{\sqrt v}-\frac{IR}{2}\left(\frac{Z^2}{v}-1\right).
$$

Its mean is zero. Squaring and taking expectations gives

$$
\Omega=1-IR\,\gamma_1+\frac{IR^2}{4}(\gamma_2-1).
$$

The leading term is the uncertainty of the mean. The skewness term is twice the numerator–denominator covariance contribution with its sign retained. The final term measures denominator uncertainty. The formula demonstrates that all the source’s bivariate raw-moment dependence ultimately enters through the first four moments of the active return. It also supplies an independent check on the five-variable matrix calculation.

For example, the raw moments needed for the active series can be recovered from

$$
E[A^3]=m_{30}-3m_{21}+3m_{12}-m_{03},
$$

$$
E[A^4]=m_{40}-4m_{31}+6m_{22}-4m_{13}+m_{04},
$$

then centralized using $\mu$ and $q$. Alternatively, compute them directly from observed $P_t-B_t$, which avoids cancellation among separately rounded bivariate moments. The source does not print this scalar expression; it is an equivalent derivation, not a separately claimed result of the authors.

If the pair is jointly Gaussian, then $A$ is Gaussian, $\gamma_1=0$, and $\gamma_2=3$. Therefore

$$
\Omega=1+\frac{IR^2}{2},\qquad
\operatorname{se}(\widehat{IR})\approx
\sqrt{\frac{1+IR^2/2}{T}}.
$$

This proves the source’s Theorem 2 without expanding all bivariate Gaussian moments. It is an asymptotic standard error, not an exact finite-sample normal sampling law. The formula also shows that zero population active performance does not mean zero estimation uncertainty: at $IR=0$, the standard error is $1/\sqrt T$.

For a general feasible non-Gaussian distribution, $\Omega\ge0$ because it is a variance. A negative quadratic form is a diagnostic of numerical failure, erroneous derivatives, or an infeasible supplied moment set. It is not meaningful evidence of exceptionally precise estimation.

## Simulation inputs and the calibration discrepancy

The source starts from a simulated bivariate Gaussian population. Its surrounding text identifies portfolio and benchmark means of 13% and 10%, and the displayed covariance matrix is

$$
\begin{pmatrix}0.04&0.0256\\0.0256&0.0256\end{pmatrix}.
$$

The standard deviations are thus 20% and 16%. With those entries, the correlation is $0.0256/(0.20\times0.16)=0.80$, tracking-error variance is $0.0144$, and $IR=0.03/0.12=0.25$. The prose instead states correlation 0.85 and $IR=0.2835$. Those latter two numbers are mutually consistent if the off-diagonal covariance is $0.0272$, because the resulting active variance is $0.0112$. This is a proposed calibration repair inferred from arithmetic; the source does not identify which displayed input was used in its simulation.

The reported realized raw moments are as follows. Returns are represented as decimals, so a raw moment of total degree $k+l$ has the corresponding power of return units.

| Moment | Value | Moment | Value |
|---|---:|---|---:|
| $m_{10}$ | 0.12760 | $m_{01}$ | 0.09986 |
| $m_{20}$ | 0.056175 | $m_{02}$ | 0.035624 |
| $m_{11}$ | 0.040084 | $m_{30}$ | 0.017468 |
| $m_{03}$ | 0.008728 | $m_{21}$ | 0.012698 |
| $m_{12}$ | 0.010080 | $m_{40}$ | 0.00917 |
| $m_{04}$ | 0.00364 | $m_{31}$ | 0.00653 |
| $m_{13}$ | 0.00410 | $m_{22}$ | 0.00502 |

Using these printed, rounded inputs gives active mean $0.02774$, raw active second moment $0.011631$, active variance $0.0108614924$, and estimated $IR\simeq0.2661716$. The implied contemporaneous correlation is about 0.8547085. The variance spread is approximately 0.01424, consistent with the value used by the source. These realized moments are therefore close to the stated 0.85 calibration, but they cannot establish the exact unreported random sample or settle the covariance typo with certainty.

The five-moment calculation at these rounded inputs gives $\Omega\simeq1.0461065$. The constructed $\Sigma$ has positive eigenvalues, with its smallest about $3.12\times10^{-5}$. For an explicitly assumed $T=60$, the resulting standard error is approximately 0.1320421. This last sample-size choice is an illustration, not a claimed recovery of the source’s simulation size. The paper does not provide the random seed or the generated observations.

The source motivates simulating rather than using actual returns because it wants controlled sensitivity experiments. It does not present an empirical investment-manager sample in this study. Its brief reference to BARRA’s average information ratios for 300 funds is contextual material, not the dataset used to estimate the displayed moments.

## What the sensitivity figures do and do not establish

The general experiment changes selected low-order moments while fixing simulated third- and fourth-order raw moments. This deliberately leaves the Gaussian family: under joint normality, high moments are determined by the means and covariance matrix. The authors describe the approach as a way to obtain flexible non-Gaussian moment combinations. Flexibility alone, however, does not guarantee that the combinations correspond to any distribution.

The mean experiment scales the active-mean gap, using $\mu_P-\mu_B=K\hat\delta_\mu$ for multipliers such as 0.5, 1, and 1.5, with $K=0$ added in later figures. The variance experiment sets $\sigma_P^2=\sigma_B^2+K\hat\delta_{\sigma^2}$, using $K=-0.5,0,1,1.5$. Correlation is then varied, or one gap multiplier is varied while holding the other fixed.

At the point-estimate level, with a positive active mean and fixed volatilities,

$$
\frac{\partial IR}{\partial\rho}
=\frac{\mu\sigma_P\sigma_B}{v^{3/2}}>0.
$$

For fixed positive $\mu$, $\sigma_B$, and positive $\rho$, the point information ratio is maximized with respect to $\sigma_P\ge0$ at $\sigma_P=\rho\sigma_B$. For nonpositive correlation, its maximum is at the boundary $\sigma_P=0$, when that boundary has a meaningful economic interpretation. These statements require the sign condition on the active mean; they reverse or change character for negative performance. They concern the ratio, not the precision of its estimate.

Figure 1 is captioned as an information-ratio plot, but its internal labels say “Sigma_IR” and one positive-mean multiplier curve declines with correlation. It therefore cannot be treated as a verified graph of the point ratio just defined. This visible labeling/behavior conflict is retained as an unresolved presentation issue.

Figure 2 plots declining standard error against sample size, consistent with the $T^{-1/2}$ factor. The prose says that moving from monthly to weekly observations over five years roughly halves uncertainty. That arithmetic is appropriate if the same iid distributional variance factor is held fixed and only $T$ changes. Actual resampling changes the period of the return and the ratio being estimated. For an annualized ratio under a consistently specified iid model, multiplying by $\sqrt q$ also multiplies its standard error by $\sqrt q$, where $q$ is the observations per year. Increased frequency is therefore not a free precision gain for an unchanged annual estimand; serial dependence further limits that interpretation.

Figures 3–4 report that the standard error can rise or fall with correlation, depending on the mean gap and portfolio volatility. With portfolio volatility 20%, the prose gives the following standard errors:

| Mean multiplier and stated portfolio mean | At $\rho=0.90$ | At $\rho=0.95$ |
|---|---:|---:|
| $K=1.5$, mean 14.50% | 0.1582 | 0.236 |
| $K=0.5$, mean 11.50% | 0.099 | 0.0314 |

For portfolio volatility 22%, it reports approximately 0.10 and 0.070 for $K=1$ at the same two correlations; with zero active mean, it reports 0.129 at both. These are printed source numbers, not independently reproduced observations. The constant 0.129 is numerically consistent with $1/\sqrt{60}$, suggesting a 60-observation calculation, but the paper does not make a complete, consistent numerical recipe explicit. Its portfolio means in these examples use a 3-percentage-point gap, whereas the realized moment gap printed earlier is 2.774 percentage points. Exact reconstruction requires deciding which baseline each figure uses.

Figure 5 varies the variance gap and can reverse the ordering of precision curves. Figure 6 varies the mean gap and shows interior minima. The accompanying prose reports a minimizing variance multiplier of 1.21, portfolio volatility 20.74%, mean multiplier 0.73, and portfolio mean 12.19%. The decimal numbers 1.21 and 0.73 are multipliers in the source’s comparative experiment, not raw variance or mean differences despite the notation used in that paragraph. Figure 7 varies the variance gap while keeping several mean-gap multipliers fixed; it displays both a maximum and a minimum, with the zero-mean curve constant.

These outcomes do not contradict the Gaussian theorem because the sensitivity paths do not remain Gaussian. They still need a feasibility check. At a minimum, the low-order covariance matrix and the full five-moment covariance matrix must remain positive semidefinite, and active fourth moments must obey moment inequalities. Positivity of those matrices is necessary, not a general proof that arbitrary specified moments have a joint distribution.

As an illustration of the problem, keep the source’s printed third- and fourth-order moments fixed, set means to 11.5% and 10%, standard deviations to 20% and 16%, and correlation to 0.99. This is a further illustrative stress of the same moment-variation idea, not a reconstruction of a plotted source point. Constructing the required raw first and second moments yields an indefinite $\Sigma$, whose smallest eigenvalue is approximately $-0.000548$. Thus the proposed moment combination cannot be the moments of a real random vector, even though its ordinary two-return covariance matrix is valid. A plotted precision improvement from this kind of path cannot be interpreted as a realizable investment opportunity without specifying a coherent distributional model.

## Implementation, inference, and unresolved inputs

For actual synchronized observations, form active returns and calculate their mean and variance with a documented denominator. Compute the ratio, and either construct the five-moment matrix and gradient or compute the empirical influence values $\hat\psi_t$. The latter gives the direct iid estimate

$$
\hat\Omega=\frac1T\sum_{t=1}^{T}\hat\psi_t^2,
\qquad \widehat{\operatorname{se}}(\widehat{IR})
=\sqrt{\hat\Omega/T}.
$$

With denominator-$T$ sample moments, the mean of these estimated influence values is zero up to numerical precision. Agreement between the active-return and bivariate routes is a useful arithmetic check. Reporting both the general estimate and the Gaussian special case can show how much the result depends on estimated higher moments, but agreement in one sample is not evidence that the tails are Gaussian.

A first-order confidence interval has the form $\widehat{IR}\pm z_{1-\alpha/2}\widehat{\operatorname{se}}$. It inherits the iid, finite-fourth-moment, and nondegenerate-tracking-error assumptions; it is not an exact small-sample interval. Very small tracking error and poorly estimated fourth moments can make the normal approximation unstable. The source does not provide a finite-sample coverage study, a serial-correlation correction, or simultaneous inference for ranking many managers.

Under suitable weak-dependence conditions, the natural extension would replace the iid influence variance by the long-run variance $\sum_{k=-\infty}^{\infty}\operatorname{Cov}(\psi_t,\psi_{t-k})$. That is an implementation direction derived from the same linearization, not a result estimated or validated in this paper. It requires additional conditions and a bandwidth or dependence model. Likewise, a comparison between two estimated managers’ ratios requires their joint covariance; subtracting their point estimates and combining two independent standard errors is generally inappropriate when their returns overlap.

Reproducing the mathematical theorem needs only the moment definitions, gradient, and matrix formula above. Reproducing the exact figures additionally needs the simulation size and seed, unrounded moments, the chosen population covariance, consistent mean-gap baselines, all fixed-varying parameter conventions, and plotting inputs or code. Those are not fully available. The usable contribution is therefore the asymptotic measurement of information-ratio uncertainty and its dependence on active-return shape; the detailed sensitivity figures remain qualified by calibration and moment-feasibility limitations.
