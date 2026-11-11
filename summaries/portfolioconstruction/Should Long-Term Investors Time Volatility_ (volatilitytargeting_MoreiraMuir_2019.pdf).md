# Should Long-Term Investors Time Volatility?

**Alan Moreira and Tyler Muir.** Working paper dated January 12, 2018; 61 PDF pages including Appendices A–E. The library basename contains 2019. This note follows the supplied working paper, rather than silently substituting a later published version.

**Source:** [volatilitytargeting_MoreiraMuir_2019.pdf](../../Finance/volatilitytargeting_MoreiraMuir_2019.pdf). Page references below use the printed pagination, one less than the PDF page number. Reported numerical results belong to this source; algebra explicitly labeled “reconstruction” is derived here to make the implementation internally consistent.

## Why this matters

Reducing equity exposure when variance rises is natural for a short-horizon mean–variance investor. A long-term investor has an additional reason to hold equities after an adverse price movement: part of the movement may represent a temporary increase in discount rates that raises future expected returns. The substantive question is whether this intertemporal hedging demand largely cancels the incentive to reduce risk when volatility rises.

The paper estimates a joint process for expected returns and volatility and solves an infinite-horizon consumption–portfolio problem. Its baseline result is that substantial volatility timing remains attractive even for long-term investors. At risk aversion five and an effective 20-year consumption horizon, a simple volatility-only rule captures about 83% of the reported gains from optimally timing both expected return and variance. The estimated annual certainty-equivalent benefit is 2.36% of wealth, versus 2.84% for full timing.

The genuinely new mechanism is the **composition of volatility**. A volatility increase caused mainly by permanent cash-flow shocks raises long-horizon risk. An increase caused mainly by temporary discount-rate shocks can be less damaging because those shocks reverse. Merely making investors patient does not determine which case applies. The speed of mean reversion and the fraction of variance attributable to discount-rate shocks must be specified together.

The source has consequential inconsistencies among its SDEs, displayed HJB, shock-sign conventions, and certainty-equivalent formulas. A reproducer should not copy every displayed equation into code and expect the reported tables. This note gives a coherent reconstruction from the stated primitive processes and identifies the points where the original implementation remains uncertain. No numerical optimization or backtest has been independently rerun here.

## State variables and primitive return process

Use $y_t$ for the instantaneous expected equity excess return, $v_t$ for instantaneous return variance, and $x_t=\log(v_t-v_0)$ for transformed variance. The variance floor is $v_0=0.07^2$. This notation avoids the paper’s occasional use of a volatility symbol for a derivative with respect to transformed variance.

The risky asset and two state processes, expressed in annual time, are

$$
\frac{dS_t}{S_t}=(r+y_t)dt+\sqrt{v_t}\,dB_{S,t},
$$

$$
dy_t=\kappa_\mu(\bar\mu-y_t)dt+
\kappa_\mu\sqrt{\alpha}\sqrt{v_t}\,dB_{\mu,t},
$$

$$
dx_t=\kappa_\sigma(\bar x-x_t)dt+\nu\,dB_{\sigma,t},
\qquad v_t=v_0+e^{x_t}.
$$

The source initially writes the expected-return diffusion coefficient as $\sigma_\mu\sqrt{v_t}$ and then imposes $\sigma_\mu=\kappa_\mu\sqrt\alpha$. Here $\alpha$ is the share of instantaneous return variance attributed to discount-rate shocks, not a performance-regression intercept. The correlations satisfy

$$
\operatorname{Corr}(dB_\mu,dB_S)=-\sqrt\alpha.
$$

Consequently, an expected-return innovation generates an immediate price response whose expected subsequent reversal offsets its long-run effect on value. Define the orthogonal cash-flow shock by

$$
dB_c=\frac{dB_S+\sqrt\alpha\,dB_\mu}{\sqrt{1-\alpha}},
\qquad
dB_S=-\sqrt\alpha\,dB_\mu+\sqrt{1-\alpha}\,dB_c.
$$

Let $\rho_\mu=\operatorname{Corr}(dB_\sigma,dB_\mu)$ and let $\rho_c=\operatorname{Corr}(dB_\sigma,dB_c)$ be a **signed** correlation. Since $B_\mu$ and $B_c$ are orthogonal, feasibility requires $\rho_\mu^2+\rho_c^2\le1$. The return–variance-shock correlation implied by this definition is

$$
\rho_S=-\sqrt\alpha\rho_\mu+\sqrt{1-\alpha}\rho_c.
$$

A simulation can draw independent standard normals $Z_\mu,Z_c,Z_0$ and construct $Z_\sigma=\rho_\mu Z_\mu+\rho_cZ_c+\sqrt{1-\rho_\mu^2-\rho_c^2}Z_0$. This directly enforces the positive-semidefinite correlation restriction. It also makes a sign error visible before estimation.

For the displayed OU process, $\operatorname{Var}(x)=\nu^2/(2\kappa_\sigma)$. If the parameter $\bar v$ is intended to equal $E[v_t]$, the mathematically consistent centering is

$$
\bar x=\log(\bar v-v_0)-\frac{\nu^2}{4\kappa_\sigma}.
$$

The supplied paper instead prints subtraction of $\nu^2/(2\kappa_\sigma)$ on p. 10. Given its equation (3), that subtracts the full stationary log-variance rather than half of it. The expression above is a reconstruction, not a claim about which formula the authors actually used in their code. A different diffusion normalization could change the conversion, but it would need to be stated consistently.

The sign convention also needs reconciliation. Equations (5)–(6) define cash-flow correlation directly, whereas footnote 14 uses an opposite-sign description. Table 1 lists positive values 0.669 and 0.743 for the discount-rate and cash-flow correlations. Reading both as the signed correlations just defined gives $\rho_S\approx+0.103$ at $\alpha=0.449$, whereas the calibration discussion and return-on-volatility-change moment emphasize a negative leverage relation. The table values alone do not identify whether a minus sign is implicit in its cash-flow parameter. Implementations must explicitly declare that mapping rather than silently treating positive 0.743 as a negative correlation.

## Preferences, wealth, and a consistent HJB

Preferences are continuous-time Epstein–Zin recursive utility with risk aversion $\gamma$ and, in the baseline, elasticity of intertemporal substitution equal to one. The aggregator is

$$
\mathcal F(C,J)=\beta(1-\gamma)J
\left[\log C-\frac{\log((1-\gamma)J)}{1-\gamma}\right].
$$

Here $\beta$ is time preference. The optimal consumption rate is $C_t=\beta W_t$, so $1/\beta$ is an effective horizon; it is not a fixed terminal liquidation date. At $\beta=0.05$, the effective horizon is 20 years. The baseline has $\gamma=5$ and risk-free rate $r=0.01$.

For risky weight $w_t$, wealth evolves as

$$
\frac{dW_t}{W_t}=(r+w_ty_t-C_t/W_t)dt+w_t\sqrt{v_t}\,dB_{S,t}.
$$

The baseline does not impose a long-only restriction, leverage cap, transaction costs, or an intermediate drawdown constraint. It assumes the state variables are observable. These are economically significant simplifications when interpreting an optimal weight as a proposed trading rule.

The covariance between the return shock and the expected-return state is $-\alpha\kappa_\mu v_tdt$. Thus the HJB reconstructed from the primitive SDEs is

$$
\begin{aligned}
0=\sup_{w,C}\{&\mathcal F(C,J)+(rW+wyW-C)J_W
+\tfrac12w^2W^2vJ_{WW}\\
&+wW[-\alpha\kappa_\mu vJ_{Wy}+\nu\sqrt v\rho_SJ_{Wx}]\\
&+\kappa_\mu(\bar\mu-y)J_y+\kappa_\sigma(\bar x-x)J_x\\
&+\tfrac12\alpha\kappa_\mu^2vJ_{yy}+\tfrac12\nu^2J_{xx}
+\kappa_\mu\sqrt\alpha\sqrt v\nu\rho_\mu J_{yx}\}.
\end{aligned}
$$

The value function is homogeneous:

$$
J(W,y,x)=\frac{W^{1-\gamma}}{1-\gamma}
\exp((1-\gamma)g(y,x)).
$$

Substituting into the portfolio first-order condition gives the coherent rule

$$
w^*(y,x)=\frac{y}{\gamma v}
+\frac{1-\gamma}{\gamma}
\left[-\alpha\kappa_\mu g_y+
\frac{\nu\rho_S}{\sqrt v}g_x\right].
$$

The first term is myopic demand; the second and third terms hedge changes in expected returns and transformed variance. Their signs depend on the derivatives of the value function and the signed shock correlations. A long horizon therefore does not imply a universally positive variance hedge or no need to de-risk.

For numerical implementation, define the state generator contribution

$$
\begin{aligned}
\mathcal Gg={}&\kappa_\mu(\bar\mu-y)g_y+\kappa_\sigma(\bar x-x)g_x\\
&+\tfrac12\alpha\kappa_\mu^2v[g_{yy}+(1-\gamma)g_y^2]\\
&+\tfrac12\nu^2[g_{xx}+(1-\gamma)g_x^2]\\
&+\kappa_\mu\sqrt\alpha\sqrt v\nu\rho_\mu
[g_{yx}+(1-\gamma)g_yg_x].
\end{aligned}
$$

The reduced HJB, with $w=w^*$, is

$$
0=\beta(\log\beta-g)+r-\beta+wy-\tfrac\gamma2w^2v
+w(1-\gamma)[-\alpha\kappa_\mu vg_y+\nu\sqrt v\rho_Sg_x]
+\mathcal Gg.
$$

This provides a self-contained PDE without ambiguous volatility-coordinate derivatives. The paper’s equation (10) instead prints $-\sqrt\alpha v$ as the wealth–expected-return covariance coefficient, which does not follow from its SDE parameterization. Its displayed hedging formulas also have signs or factors inconsistent with the stated value function and covariance structure. These differences affect an actual solver. The reconstruction should be tested against the authors’ implementation before claiming replication of Tables 2–10.

## Estimation design and reported calibration

The empirical moments use US equity returns from the French/CRSP data and valuation information from Shiller over 1926–2015. Daily returns are aggregated to monthly returns and realized monthly variance; long-horizon predictive moments use valuation ratios. The model is simulated at daily frequency and its moments are constructed to correspond to the empirical monthly and longer-horizon quantities.

The model does not generate dividends or construct a synthetic price–dividend ratio. The empirical valuation-ratio regressions are used to infer the variability and persistence of the expected-return process; simulated predictability must therefore be matched using the model’s expected-return information, rather than pretending the model supplies a dividend series. In the estimation exercise, realized variance is reconstructed from simulated daily returns as it is in the data, so the econometrician does not simply observe the model’s instantaneous variance without measurement error. That is distinct from the portfolio problem, in which the investor is initially assumed to observe the state.

The seven-percent volatility floor is separately calibrated rather than identified jointly by all nine moments. The authors motivate it using the minimum VIX of about 10% over 1990–2015 and the longer historical sample. Their reason for referring to implied volatility is that a realized-volatility minimum is contaminated by measurement noise. This is a modeling calibration with an economic rationale, not a demonstrated hard lower bound on equity volatility. Changing the floor affects the inverse-variance exposures in quiet states and should be part of numerical sensitivity analysis.

The monthly realized variance sums squared daily demeaned excess returns. The source uses 22-day notation, as in the related volatility-managed-portfolio paper. Annual equity premiums and average variance, log realized-variance dispersion and persistence, return predictability, contemporaneous leverage, volatility-managed alpha, and the conditional risk–return slope jointly identify the calibration.

| Target moment, Table 1 | Data | Model | Reported SE |
|---|---:|---:|---:|
| Annual equity premium | 0.078 | 0.074 | 0.017 |
| Annualized average realized variance | 0.028 | 0.032 | 0.006 |
| Variance of log realized variance | 1.109 | 1.075 | 0.175 |
| Monthly lag-one log-variance coefficient | 0.722 | 0.734 | 0.046 |
| One-year predictive regression $R^2$ | 0.082 | 0.052 | 0.042 |
| Five-year predictive regression $R^2$ | 0.234 | 0.169 | 0.079 |
| Return coefficient on contemporaneous log-variance change | −0.023 | −0.023 | 0.002 |
| Managed-market alpha, annual return units | 0.048 | 0.051 | 0.017 |
| Future-return coefficient on realized variance | −0.186 | 0.319 | 0.880 |

The last moment is very imprecise: the positive fitted slope is not evidence that the data precisely establish a positive risk–return relation. The model also understates the one- and five-year predictive $R^2$s at the point estimate, although the reported uncertainty is considerable.

The estimated parameters, using the source’s labels, are:

| Parameter | Estimate | SE |
|---|---:|---:|
| Average variance $\bar v$ | 0.034 | 0.006 |
| Variance mean-reversion speed $\kappa_\sigma$ | 2.961 | 0.613 |
| Transformed-variance diffusion parameter $\nu$ | 4.347 | 0.469 |
| Mean equity premium $\bar\mu$ | 0.069 | 0.016 |
| Discount-rate variance share $\alpha$ | 0.449 | 0.143 |
| Expected-return mean-reversion speed $\kappa_\mu$ | 0.129 | 0.108 |
| Variance/discount-rate shock correlation parameter | 0.669 | 0.131 |
| Variance/cash-flow shock correlation parameter | 0.743 | 0.154 |

The source calls $\nu$ “variance of variance,” but equation (3) uses it as a diffusion coefficient, whose square enters infinitesimal variance. It also gives qualitative annual-persistence descriptions that should not replace the SDE conversion. Under the displayed expected-return drift, conditional-mean persistence over one year is $e^{-\kappa_\mu}$; at 0.129 this is about 0.879, and its mean-reversion half-life is about 5.37 years. These are derived translations, distinct from rounded correlations of simulated or aggregated variables in later tables.

Appendix A uses simulated method of moments with a criterion weighted by the inverse of the estimated covariance matrix of empirical moments. The influence-function approach estimates their joint sampling distribution. Parameter uncertainty is propagated by drawing 1,000 moment vectors from that estimated distribution, reestimating the model for each, and using the resulting parameter dispersion. Correlation feasibility and parameter bounds must be imposed during estimation. The parameter list in the appendix omits one correlation that is present in Table 1, another detail to resolve against code.

The paper does not report enough numerical settings to rerun this estimation identically: the complete data-vintage files, exact simulation step convention, simulation length and burn-in, random seeds, optimization initialization and tolerances, and handling of infeasible moment draws are not supplied. Estimation uncertainty here concerns a specified stochastic model; it does not include uncertainty about the model class itself.

## Solving the portfolio problem and simplifying the policy

Appendix B approximates $g(y,x)$ using bivariate Chebyshev polynomials of order six. Derivatives are computed from the polynomial representation, the implied optimal portfolio is inserted into the HJB, and the residual is projected onto the full approximation basis. MATLAB’s `fsolve` chooses coefficients making the projected residuals zero. Increasing the order to ten reportedly leaves baseline results unchanged while increasing computation time.

The state-domain bounds, scaling into the Chebyshev domain, projection nodes or quadrature, initial coefficient vector, and solver tolerances are not reported. These are needed for reliable reproduction, especially because inverse variance becomes large near the floor and expected-return states have unbounded support. A reconstruction should check residuals away from collocation nodes, convergence under a larger state domain, and policy/value agreement rather than relying solely on an optimizer’s termination flag.

The paper then projects the fully optimal policy onto simple portfolios under the model’s stationary distribution:

$$
\widetilde w^*(y,v)=a^*+b^*\frac{y}{\gamma v},
\qquad
\widetilde w^v(v)=a^v+b^v\frac{\bar\mu}{\gamma v}.
$$

The first approximation combines a constant equity allocation with the myopic optimal portfolio. The second uses only variance information plus a constant equity allocation. These coefficients arise from a projection of the optimal policy, rather than a directly stated separate constrained optimization over all affine policies. The source evaluates the utility associated with the resulting rules.

At the baseline, the full-policy projection has approximately $a^*=0.14$, $b^*=0.99$, and the variance-only rule has $a^v=0.14$, $b^v=0.89$. The constant benchmark is

$$
\bar w=\frac{\bar\mu}{\gamma\bar v}.
$$

Using Table 1, this is $0.069/(5\times0.034)\approx0.406$. It is the source’s myopic fixed allocation, not necessarily the globally optimal constant allocation for every long-horizon objective. An affine weight evaluated at average states is also not generally equal to its stationary mean, because $E[1/v]\ne1/E[v]$.

The approximation loss reported near the baseline is about 0.02 percentage point annually. The paper’s tables sometimes express utility changes through a raw ratio notation, but the text interprets them as annual equivalent fees. They should be compared using a properly normalized certainty-equivalent calculation.

## Certainty-equivalent fees: reconstruction and source warning

For a fixed policy $w$, let $g_w$ solve its value equation and define

$$
M_w=E\left[e^{(1-\gamma)g_w(y,x)}\right],
$$

where the expectation is over stationary states. With $\gamma>1$, the multiplicative value-function prefactor is negative. Taking an unadjusted ratio of negative utility levels and calling it a welfare gain can therefore give the wrong sign or scale.

For a risk-free investor receiving an additional wealth-flow rate $f$, the reduced equation gives

$$
g_0(f)=\log\beta+\frac{r+f-\beta}{\beta}.
$$

Equating $M_w$ to $e^{(1-\gamma)g_0(f_w)}$ yields

$$
f_w=\frac{\beta}{1-\gamma}\log M_w-\beta\log\beta-r+\beta.
$$

The annual fee-equivalent advantage of policy $b$ over policy $a$ is consequently

$$
\Delta f_{b,a}=\frac{\beta}{1-\gamma}\log\left(\frac{M_b}{M_a}\right).
$$

This algebra follows directly from the paper’s stated value-function form. Appendix C’s printed risk-free value and fee expressions omit factors of $1-\gamma$ relative to that form. Its raw formulas should not be used without reconciling the normalization. The published fee numbers below are preserved as reported, not recalculated using an assumed correction.

The corresponding initial-wealth equivalent is $\exp(\Delta f/\beta)-1$. At $\Delta f=0.0236$ and $\beta=0.05$, it is approximately 60.3%, which matches the paper’s approximate 60% wealth-equivalent interpretation. This is a model-based lifetime-utility comparison, not an expected one-year excess return of 60%.

## Baseline results and horizon dependence

The local sensitivity measure is

$$
\zeta=-\frac{d\log w^*}{d\log v}.
$$

Despite occasional prose references to volatility, the denominator is **variance**. The paper evaluates the response around median states to a one-standard-deviation variance increase and allows the associated expected-return response. This is a directional response, not a partial derivative holding expected return fixed. Its myopic counterpart is $1-d\log y/d\log v$, which the source estimates at 0.96. Holding $y$ fixed instead would give exactly one for the myopic rule. A value 0.85 corresponds locally to roughly an 8.5% weight decrease for a 10% variance increase along the specified response; a 10% standard-deviation increase changes variance by about 21% and is a different experiment.

At the baseline, the optimal-policy elasticity is about 0.85, compared with about 0.96 for the comparison myopic response reported in the paper’s exercise. Intertemporal hedging attenuates but does not eliminate de-risking. The source’s fully optimal annual fee gain is 2.84%, while variance-only timing earns 2.36%, or 82.92% of the total.

| Effective horizon, $\gamma=5$ | Variance-only fee, %/year | Full-timing fee, %/year |
|---|---:|---:|
| 10 years | 2.69 | 3.14 |
| 20 years | 2.36 | 2.84 |
| 50 years | 2.02 | 2.59 |
| 100 years | 1.87 | 2.42 |

A longer horizon lowers these gains but leaves them substantial in the calibrated baseline. At 20 years, variance-only/full-timing gains are 3.88%/4.71% for risk aversion three and 1.21%/1.41% for risk aversion ten. The lower-risk-aversion investor has larger risky exposures and therefore larger absolute fee benefits; this does not imply that greater risk tolerance is universally desirable.

The mechanism is that expected-return variation is persistent and its innovations are relatively small compared with the immediate change in risk. Long-term investors do hold a hedging position associated with future opportunities, but a largely static hedging component need not neutralize the short-run variation in myopic demand. The fitted affine rule captures this separation particularly well.

## The volatility-composition experiment

The alternative model holds permanent cash-flow variance fixed at $v_0$ and attributes all variation above that floor to discount-rate shocks. Its return shock can be written

$$
\sqrt v\,dB_S=-\sqrt{v-v_0}\,dB_\mu+\sqrt{v_0}\,dB_c,
$$

with expected-return diffusion coefficient $\kappa_\mu\sqrt{v-v_0}$. The discount-rate share is now

$$
\alpha(v)=1-\frac{v_0}{v},
$$

which increases with variance. This changes the economic meaning of a volatility spike, rather than just changing the persistence of an otherwise identical risk process.

Table 6 varies $\kappa_\mu$ across 0.06, 0.15, 0.25, 0.40, and 0.60. Under constant composition, the reported elasticities are 0.88, 0.83, 0.80, 0.76, and 0.71; variance-only fees are 2.44%, 2.10%, 1.86%, 1.59%, and 1.31% annually. Under increasing discount-rate composition, elasticities fall to 0.52, 0.39, 0.33, 0.28, and 0.23. Variance-only fees become 1.65%, 1.62%, 1.48%, 0.03%, and −0.36%, whereas full-timing fees rise from 2.73% to 5.40% across the same grid.

Thus there are admissible scenarios in which the simple variance-only policy is unattractive. If high variance signals especially rapid reversal, a long-term investor can lose by responding to variance without also exploiting its expected-return information. The paper does not prove that volatility timing is always beneficial.

The authors test the joint composition-and-speed mechanism using conditional return autocorrelation. They compare the correlation of next year’s return with the preceding month’s return between high- and low-variance states, with states classified using month $t-1$’s realized variance above or below the sample median, as in equation (20). The paired returns are $R_{t,t+12}$ and $R_{t-1,t}$, so the volatility classification must retain that stated lag. The observed high-minus-low difference is 0.00452, displayed as 0.452 after multiplication by 100 in Table 7.

For increasing discount-rate composition, simulated differences, in the same multiplied-by-100 units, are −2.812, −6.012, −8.791, −11.808, and −14.362 across the five $\kappa_\mu$ values. The reported simulation p-values are 0.332, 0.166, 0.087, 0.038, and 0.023. They come from 10,000 simulated samples of the historical length. The fast-reversal cases with the weakest timing benefits imply much more negative high-volatility autocorrelation than observed. This constrains their joint plausibility; it is not a separate rejection of every model with time-varying discount-rate shares.

## Parameter uncertainty versus the cost of estimating a trading rule

The paper distinguishes two exercises. First, reestimating the stochastic model for perturbed empirical moments produces uncertainty about the optimal policy itself. Table 8 gives 5th/50th/95th percentiles of 0.60/0.76/0.93 for the variance elasticity, 0.60%/2.04%/5.53% for variance-only fees, and 1.61%/3.01%/6.25% for full-timing fees. These bands are asymmetric and model-dependent; the median need not equal the baseline point-estimate result.

Second, an investor has finite data to estimate forecasting relationships. In this experiment the underlying states provide the signals, but their forecasting coefficients must be estimated from simulated samples of 60, 90, or 180 years. The resulting policy is evaluated after estimation; the experiment does not solve a full Bayesian learning problem with continual parameter updates.

| Estimation sample | Variance-only mean fee | Variance-only 5th percentile | Full-timing mean fee | Full-timing 5th percentile |
|---|---:|---:|---:|---:|
| 60 years | 1.95% | 1.49% | −0.54% | −13.33% |
| 90 years | 2.03% | 1.50% | 0.21% | −8.93% |
| 180 years | 2.10% | 1.58% | 1.70% | 0.16% |
| Known parameters | 2.36% | — | 2.84% | — |

The expected-return forecasting coefficient is much harder to learn than the variance forecasting coefficient. A theoretically superior full-information policy can therefore perform much worse when its expected-return signal is estimated imprecisely. This is a quantitative result under the paper’s simulation and signal observability assumptions, not a statement that every machine-learned mean forecast is harmful.

The regression design uses next-period returns for mean forecasting and squared-return information for variance forecasting. Exact transformations and fitted-policy implementation should be verified against the original code because the prose and displayed squared-return notation do not resolve every centering detail. Training-sample length is enormous by practical standards, yet mean estimation remains costly; extrapolating the full-information 2.84% benefit into a short real dataset would be unjustified.

## Additional robustness and reproducibility limits

The baseline monthly variance process loses persistence too rapidly at longer horizons. Table 10 contrasts empirical log-variance autocorrelations of 0.72, 0.58, and 0.45 at one, three, and twelve months with baseline fitted values about 0.73, 0.40, and 0.03. Alternative persistence calibrations improve the long-horizon fit. The associated variance-only fee estimates are about 2.16%, 2.18%, and 2.28%, and full-timing estimates 2.64%, 2.66%, and 2.45%. These are the table’s own alternative-calibration results, not identical to the earlier baseline 2.36% and 2.84% figures.

The authors also change intertemporal substitution to 0.2 and 2. Baseline responses remain broadly similar, although composition-dependent hedging can change more strongly with preferences. Discussions of labor income and habits are qualitative qualifications rather than a fully estimated labor-income or habit model solved in this paper.

Appendix D allows expected returns to include a direct variance component, $y_t=z_t+\delta(v_t-E[v_t])$, and reestimates the model. Its prose reports $\delta=-0.55$, whereas the adjacent table reports −0.23. The table’s variance-only fee rises to 3.23% and full timing to 3.70%, a share of 87.29%. Both versions imply a negative direct risk–return relation, but the coefficient discrepancy prevents a unique literal reproduction.

The paper’s central economic mechanism is reproducible from its primitive structure: distinguish permanent from transitory return shocks, model their connection to volatility, solve a long-horizon portfolio problem, and compare full information with a variance-only policy. Exact numerical reproduction is conditional on resolving the centering, signed-correlation, HJB, and fee-normalization inconsistencies, obtaining the source code or equivalent numerical settings, and matching the empirical moment construction. The reported quantitative results should remain labeled as source estimates until those checks have been completed.
