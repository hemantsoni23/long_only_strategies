# Time Series Factor Analysis with an Application to Measuring Money

**Paul D. Gilbert and Erik Meijer.** November 2005. University of Groningen, Research School SOM, Research Report 05F10. This note concerns the 36-page working paper supplied in the library, including its simulation, Canadian application, figures, and references; it has no separate appendix.

**Source:** [Original PDF](<../../Finance/GilbertMeijer_%20%20Time%20Series%20Factor%20Analysis%20with%20an%20Application%20to%20Measuring%20Money_2005.pdf>). Page references below use the PDF's printed page numbers, which equal its PDF page numbers.

## Why this matters and what is new

The paper separates **measurement of latent economic quantities** from **modeling their dynamics**. A dynamic factor model generally estimates a measurement equation together with a transition model for the factors. An incorrect transition model can then distort the estimated measurement relationship and the resulting historical factor series. This is especially undesirable when a statistical agency supplies one measurement series to researchers who disagree about economic dynamics. Gilbert and Meijer instead estimate stable factor loadings from first differences, then apply those loadings to levels to obtain contemporaneous factor scores.

Their time series factor analysis, or TSFA, is a fixed, relatively small cross-section method. It does not rely on increasing the number of indicators to eliminate idiosyncratic noise. Its principal contributions are the conditions under which ordinary covariance-based factor estimation remains consistent for dependent, potentially nonstationary level data; treatment of nonzero means and intercepts; the case for Bartlett rather than regression factor scores; and a simulation explanation of apparently systematic score errors. The monetary application asks whether transactions and savings behavior can be measured more consistently than by conventional sums of financial instruments when those instruments change function.

The method is deliberately incomplete as an economic model. It neither forecasts money demand nor estimates causal effects of money on inflation. Its results establish a measurement procedure and illustrate its behavior. The paper's favorable comparisons with monetary aggregates are descriptive, and its discussion of superiority to misspecified dynamic factor analysis is preliminary rather than a documented horse race.

## Measurement model and the role of differencing

Let $y_t$ be an $M$-vector of observed indicators, $\xi_t$ a $k$-vector of latent factors, and $\varepsilon_t$ an $M$-vector of measurement errors or unique components. The level model is

$$
y_t=\alpha_t+B\xi_t+\varepsilon_t.
$$

Here $B$ is an $M\times k$ time-invariant, full-column-rank loading matrix. The intercept can vary, but its increment is assumed constant: $\alpha_t-\alpha_{t-1}=\tau$. In the Canadian application both $\alpha_t$ and $\tau$ are set to zero. This zero-intercept restriction is substantive: zero factors should explain zero holdings, and the level origin affects economic growth-rate interpretations.

Define $\Delta z_t=z_t-z_{t-1}$. Differencing preserves the loading matrix:

$$
\Delta y_t=\tau+B\Delta\xi_t+\Delta\varepsilon_t.
$$

Integrated levels need not have convergent sample covariances. Their increments can nevertheless admit stable average first and second moments. The paper states five probability-limit conditions on pages 7–8. Writing $T$ for the number of differences used in estimation, these are

$$
T^{-1}\sum_t\Delta\xi_t\xrightarrow{p}\kappa,
\qquad
T^{-1}\sum_t\Delta\varepsilon_t\xrightarrow{p}0,
$$

$$
T^{-1}\sum_t(\Delta\xi_t-\kappa)(\Delta\xi_t-\kappa)'\xrightarrow{p}\Phi,
$$

$$
T^{-1}\sum_t\Delta\varepsilon_t\Delta\varepsilon_t'\xrightarrow{p}\Omega,
\qquad
T^{-1}\sum_t(\Delta\xi_t-\kappa)\Delta\varepsilon_t'\xrightarrow{p}0.
$$

The limits are finite and $\Phi,\Omega$ are positive definite. These assumptions permit serial dependence and time variation in individual-date moments, provided the stated averages converge. They do not require Gaussianity or covariance-stationary levels. Conditional heteroskedasticity is compatible with the framework when the needed moments and limits exist. Conversely, arbitrary dependence, divergent variance, or remaining unit roots in differences do not become harmless simply because TSFA avoids a transition equation. Further differencing is possible if the same conditions then hold, but interpretation and score recovery still require the level measurement model.

For the demeaned sample covariance

$$
S_{\Delta y}=T^{-1}\sum_t(\Delta y_t-\overline{\Delta y})(\Delta y_t-\overline{\Delta y})',
$$

expansion of the measurement equation gives

$$
\overline{\Delta y}\xrightarrow{p}\mu=\tau+B\kappa,
\qquad
S_{\Delta y}\xrightarrow{p}\Sigma=B\Phi B'+\Omega.
$$

The proof mechanism is direct: the constant intercept disappears upon centering, the factor and error quadratic terms converge to their respective limits, and the cross terms vanish. The standard covariance factor model therefore reappears in differences, with the same $B$ needed to measure levels. This is the central reason ordinary factor-analysis software can be used.

There is a qualification to the source's page 7 discussion. It says a contemporaneous condition $E(\Delta\varepsilon_t\mid\Delta\xi_t)=0$, together with finite limiting covariances, implies the required zero sample limits. Conditional mean zero motivates population orthogonality, but by itself does not supply a law of large numbers under unrestricted serial dependence. For implementation, retain the explicit probability-limit assumptions, or establish suitable dependence and moment conditions that imply them. This qualification does not alter the covariance identity above.

## Identification, estimation, rotation, and inference

The limiting covariance identifies neither the loading orientation nor an unrestricted unique covariance. The application assumes diagonal $\Omega$. A factor transformation $\xi_t^*=H^{-1}\xi_t$, $B^*=BH$, $\Phi^*=H^{-1}\Phi H^{-\prime}$ leaves $B\Phi B'$ unchanged for any nonsingular $H$. Restrictions or a rotation convention must therefore determine orientation and scale before individual factors can be compared.

The paper uses the Ledermann counting condition

$$
(M-k)^2\geq M+k
$$

and assumes identification. This is not a universal guarantee of a unique, admissible solution at every parameter value. Positive uniquenesses, nonsingular factor covariance, a full-rank loading matrix, and a locally well-defined orientation remain necessary for the subsequent formulas. With six indicators and two factors the covariance model has four degrees of freedom. With three factors the count reaches zero. The paper describes the latter as saturated; more precisely, zero overidentifying degrees of freedom removes the usual covariance-fit test, while admissibility constraints and exceptional identification cases still matter.

Covariance parameters minimize the Gaussian discrepancy, source equation (6):

$$
Q(\theta)=\log\det\Sigma(\theta)
+\operatorname{tr}\{\Sigma(\theta)^{-1}S_{\Delta y}\},
\qquad
\Sigma(\theta)=B\Phi B'+\Omega.
$$

This is quasi-maximum likelihood, not the full likelihood of the observed time series. It ignores serial conditional distributions, need not assume normal observations, and does not use all potentially informative mean restrictions. Consistency follows from covariance convergence, identification, and regularity ensuring convergence of the minimizer. It does not establish finite-sample unbiasedness or efficiency against a correctly specified dynamic model.

For the empirical and simulation estimates, the authors use direct oblimin with the quartimin criterion and Kaiser normalization, allowing correlated factors. They implement rotations using the Bernaards–Jennrich gradient-projection functions in R. Quartimin seeks a relatively simple loading pattern, with each indicator concentrated on one factor. That preference is economically debatable for bank accounts used simultaneously for spending and savings. The report names the method but does not specify optimizer starts, convergence tolerances, uniqueness bounds, or sign/permutation alignment across repeated fits. These should be made explicit in a reproduction rather than silently presumed.

Means require a separate identification decision. If $\tau$ is unrestricted, setting $\kappa=0$ gives $\widehat\tau=\overline{\Delta y}$. If $\tau=0$, the paper uses

$$
\widehat\kappa=
(\widehat B'\widehat\Omega^{-1}\widehat B)^{-1}
\widehat B'\widehat\Omega^{-1}\overline{\Delta y}.
$$

Both $\tau$ and $\kappa$ cannot be freely recovered from $M$ means without restrictions. Joint fitting of means and covariances was explored but not found to improve estimates in the authors' experimentation; the reported analysis uses covariance fitting followed by mean treatment.

For inference, the probability-limit assumptions are supplemented by a central limit theorem. If $s=\operatorname{vech}(S_{\Delta y})$ and $\sigma_0=\operatorname{vech}(\Sigma_0)$,

$$
\sqrt T(s-\sigma_0)\Rightarrow N(0,\Upsilon_0).
$$

The long-run covariance $\Upsilon_0$ concerns the vector of contemporaneous quadratic products, not just the original indicator increments. A HAC estimator can accommodate serial covariance among those products. With a differentiable identified estimator and $J_0=\partial\widehat\theta/\partial s'$ evaluated at the limit,

$$
\sqrt T(\widehat\theta-\theta_0)
\Rightarrow N(0,J_0\Upsilon_0J_0').
$$

Thus robust parameter standard errors use $J\widehat\Upsilon J'/T$, including the rotation derivative when orientation is estimated by rotation. The paper cites derivative formulas rather than printing an implementation and reports no empirical HAC bandwidth, kernel choice, or robust loading standard errors. Its consistency assumptions alone do not prove this CLT, especially under unrestricted heteroskedasticity or long memory.

## Recovering factor levels without a factor transition model

“Prediction” in this paper means contemporaneous recovery of $\xi_t$, not forecasting $\xi_{t+1}$. With fixed $M$, adding more dates estimates $B$ more precisely but does not eliminate the unique noise in a particular $y_t$. Without specifying useful dynamic dependence, the score predictor deliberately uses only the same-date indicator vector.

Let $\gamma_t=E\xi_t$, $\Gamma_t=\operatorname{Cov}(\xi_t)$, $\Psi_t=\operatorname{Cov}(\varepsilon_t)$, and $\Sigma_{y,t}=B\Gamma_tB'+\Psi_t$, with contemporaneous factor-error orthogonality. The regression predictor is

$$
\widehat\xi_t^R=\gamma_t+
\Gamma_tB'\Sigma_{y,t}^{-1}(y_t-\alpha_t-B\gamma_t).
$$

It minimizes mean squared error among affine predictors when these moments are known. It requires the level-factor mean and covariance, which are precisely the time-varying objects the method seeks to avoid modeling. Integrated factor levels make these requirements particularly unattractive.

The Bartlett predictor instead treats the factor realization as an unknown coefficient in a cross-sectional GLS problem:

$$
\widehat\xi_t^B=
(B'\Psi_t^{-1}B)^{-1}B'\Psi_t^{-1}(y_t-\alpha_t).
$$

It does not require $\gamma_t$ or $\Gamma_t$. Under the additional assumption that level errors are serially independent with constant covariance $\Psi$, differencing gives $\Omega=2\Psi$. Multiplying the weight matrix by a scalar has no effect on GLS, so with zero intercept the empirical score becomes

$$
\widehat\xi_t=
(\widehat B'\widehat\Omega^{-1}\widehat B)^{-1}
\widehat B'\widehat\Omega^{-1}y_t.
$$

Importantly, the estimate is applied to **level data** after fitting $B$ and $\Omega$ to **differences**. One does not cumulate noisy differenced scores with an arbitrary starting value. If level errors are serially correlated, $\Omega=2\Psi$ generally fails. An arbitrary positive-definite weight $W$ still gives a left inverse $(B'WB)^{-1}B'W$ and, for known $B$ and zero-mean errors, an unbiased level score. It need not be efficient, and the finite-sample plug-in predictor need not be unbiased.

The two predictors also have different variances. Defining $\Lambda_t=\Gamma_t^{-1}+B'\Psi_t^{-1}B$, the source obtains

$$
\operatorname{Cov}(\widehat\xi_t^R)=\Gamma_t-\Lambda_t^{-1},
\qquad
\operatorname{Cov}(\widehat\xi_t^B)=\Gamma_t+(B'\Psi_t^{-1}B)^{-1}.
$$

Both have unconditional mean $\gamma_t$ with known parameters. Regression scores shrink variation; Bartlett scores add measurement noise. Equality of means does not mean equality of distributions or identical conditional bias. The latter covariance inflation motivates a special adjustment when constructing simulation truth, but the authors explicitly do not impose that adjustment on scores in the actual application.

## Simulation: design and what the apparent bias means

The simulation uses six indicators, two factors, and 215 monthly level observations patterned on the Canadian application. It runs 100 replications, all conditional on the **same factor path**. The design is not 100 independent economic histories drawn from an estimated transition equation.

First fit the empirical model. Compute its Bartlett scores and linearly transform them so that the sample covariance of their first differences equals the fitted $\widehat\Phi$. These transformed scores become fixed truth $\widetilde\xi_t$. The covariance matching avoids attributing the Bartlett predictor's noise inflation to the true factors. The precise transformation, including the choice among matrices satisfying the covariance constraint and the handling of the mean, is not printed. Different admissible transformations need not preserve the same economically interpreted orientation.

For replication $r$, independently draw level errors across dates from a zero-mean normal distribution with covariance $\widehat\Psi=\widehat\Omega/2$, then construct

$$
y_t^{(r)}=\widehat B\widetilde\xi_t+\varepsilon_t^{(r)}.
$$

Refit the factor model to first differences, use the same oblimin/quartimin rotation and Kaiser normalization, and compute unadjusted Bartlett level scores. The covariance-matching transformation used to create truth is **not** repeated on estimated scores, because it changes their bias properties. Serially independent level errors imply serially dependent differenced errors, so this experiment genuinely differs from i.i.d. factor analysis of increments.

Figure 1 initially looks alarming: in the first replication the estimated first factor increasingly overshoots the true path and the second factor lies persistently below it. Yet using the true loading and error parameters makes the predicted path nearly coincide with truth. Across all 100 replications, the mean predicted paths lie much closer to truth, with substantial dispersion. The plotted mean plus/minus two standard deviations is a visual summary of Monte Carlo dispersion, not a demonstrated confidence band for every sample or every date. Figure 2 shows that differences of the fitted factors track true changes much better than their levels do.

Table 1 quantifies the loading uncertainty. Values below are reported true loading, Monte Carlo bias, and Monte Carlo standard deviation, respectively:

| Indicator | Factor 1: true / bias / SD | Factor 2: true / bias / SD |
|---|---:|---:|
| Currency | 8.8 / −0.4 / 2.1 | 5.2 / −0.7 / 2.9 |
| Personal chequing | 23.8 / −2.5 / 5.9 | −12.6 / 0.4 / 8.9 |
| Non-bank chequing | 5.2 / −0.4 / 1.5 | −2.0 / −0.1 / 1.9 |
| Non-personal demand and notice | 36.8 / −1.3 / 6.9 | 16.9 / −2.5 / 11.0 |
| Non-personal term | −2.8 / 1.0 / 9.6 | 31.0 / 0.4 / 10.5 |
| Investment | 2.6 / 2.5 / 12.4 | 47.6 / −0.4 / 17.4 |

There is considerable sampling variation, especially in cross-loadings. The small biases relative to dispersion explain why a smooth discrepancy within one sample should not be read as systematic estimator bias across repeated samples. Only 100 replications are reported, without a seed or simulation uncertainty for the tabulated statistics.

The exact decomposition, source equation (9), explains the effect. Put

$$
\widehat L'=(\widehat B'\widehat\Omega^{-1}\widehat B)^{-1}
\widehat B'\widehat\Omega^{-1}.
$$

Since $\widehat L'\widehat B=I$,

$$
\widehat\xi_t-\xi_t
=-\widehat L'(\widehat B-B)\xi_t+\widehat L'\varepsilon_t.
$$

The first term is a sample-specific matrix error multiplying the whole factor path. Positive, persistent, increasing factors turn it into a smooth error with a common sign over long intervals. The second term is same-date measurement noise. In this experiment the first component dominates, although standard fixed-date asymptotic intuition emphasizes the second.

An additional asymptotic qualification is necessary. The paper labels the first term $O_p(T^{-1/2})$. That rate is justified pointwise when $\xi_t$ remains bounded in probability and the loading estimator has the claimed root-$T$ rate. It is not a uniform conclusion for an integrated factor evaluated at $t=T$. If $\xi_T=O_p(\sqrt T)$, multiplying by an $O_p(T^{-1/2})$ loading error yields only an $O_p(1)$ bound; a deterministic linear trend can amplify it further. Thus endpoint level errors need not become negligible under the paper's broad nonstationary setting. Differencing the decomposition replaces $\xi_t$ by $\Delta\xi_t$, which explains the much more favorable behavior of changes without requiring precise level recovery.

The indicator residuals do not provide a free bias correction. For fixed estimated $\widehat B$, minimizing

$$
(y_t-\widehat Bx)'W(y_t-\widehat Bx)
$$

over $x$ already produces the Bartlett form. With $W=\widehat\Omega^{-1}$ the fitted score is therefore optimal for this particular cross-sectional criterion. No alteration of the score alone can lower the same weighted residual sum of squares. This does not prove optimality among estimators that change loadings, impose economic restrictions, or exploit dynamics; it explains why simply “correcting” the visible residual path is not justified.

## Canadian money application and reported results

The sample contains 215 months, January 1986 through November 2003. Indicators are real Canadian-dollar balances per capita. They are not seasonally adjusted: currency's Christmas and September movements may contain information that distinguishes transactions from savings. The six series are currency, personal chequing deposits, non-bank chequing deposits, non-personal demand and notice deposits, non-personal term deposits, and investment. Non-personal accounts are primarily business accounts; non-bank institutions include trust companies and credit unions.

Detailed instrument categories are combined where financial innovation causes substitution without necessarily changing the underlying economic purpose. Savings bonds and mutual funds exemplify the motivation for the investment grouping. The paper delegates the exact source-series definitions and continuity adjustments to Gilbert and Pichette (2003) and Kottaras (2003). It does not provide the numerical panel, precise deflator/base year, population series, data-vintage identifiers, missing-value policy, or category aggregation map. Those omissions prevent reconstruction of the exact six inputs from this PDF alone.

The eigenvalues of the sample correlation matrix of differenced indicators are 2.08, 1.39, 0.85, 0.69, 0.65, and 0.33. The two-above-one heuristic and the anticipated transactions/savings interpretation motivate two factors. The third eigenvalue and ambiguity in corporate versus household behavior suggest a possible third factor, but six indicators provide no overidentifying covariance degrees of freedom for that specification. The number-of-factors decision is therefore exploratory rather than supported by a formal dependent-data selection test.

The nominal likelihood-ratio statistic is 3.19 on four degrees of freedom, and the comparative fit index is 1.0. The authors explicitly acknowledge that conventional p-values are incorrect because normal i.i.d. assumptions fail. These numbers describe a close covariance fit under the chosen discrepancy; they do not validate a calibrated test or establish correct measurement of money's economic functions.

Table 2 reports the following fitted loadings and communalities:

| Indicator | Unstandardized F1 | Unstandardized F2 | Standardized F1 | Standardized F2 | Communality |
|---|---:|---:|---:|---:|---:|
| Currency | 8.84 | 5.20 | 0.66 | 0.39 | 0.59 |
| Personal chequing | 23.82 | −12.57 | 0.54 | −0.28 | 0.37 |
| Non-bank chequing | 5.18 | −1.97 | 0.48 | −0.18 | 0.26 |
| Non-personal demand and notice | 36.78 | 16.94 | 0.77 | 0.35 | 0.72 |
| Non-personal term | −2.84 | 31.02 | −0.04 | 0.44 | 0.20 |
| Investment | 2.60 | 47.63 | 0.02 | 0.40 | 0.16 |

The estimated correlation of the **differenced** factors is 0.0095, nearly zero despite allowing an oblique rotation. Standardized pattern loadings are not generally correlations under oblique rotation; communalities include cross terms involving the factor covariance. Here the near-zero correlation makes the squared-loading intuition approximately applicable.

The second factor loads strongly on term deposits and investment, suggesting savings. The first loads more on transaction-related accounts, suggesting transactions money. But currency and business demand deposits also load on factor two, while personal and non-bank chequing carry negative factor-two loadings. Those signs complicate a literal savings interpretation. They could reflect an unsuitable rotation or a missing third factor separating corporate behavior. The paper does not settle this identification problem.

Differenced communalities range from 0.16 to 0.72. Under additional assumptions of i.i.d. level errors and the simulation factor covariance, tentative level communalities are 0.998, 0.992, 0.979, 0.999, 0.996, and 0.995 in the same indicator order. Differencing removes large common level variation while doubling the variance of independent level errors. Consequently a low differenced communality need not mean the level measurement is useless. Conversely the spectacular level communalities are conditional calculations, not an independent proof against spurious common trends.

Figures 5–6 show that estimated indicator levels can miss substantial portions of observed balances while tracking monthly movements more closely. The currency seasonal pattern appears in its prediction; investment remains nonseasonal. The level mismatch is consistent with the simulation's loading-error explanation, but in actual data model misspecification is also possible because true factors are unknown.

For comparison with conventional aggregates, factor one is scaled to have the same sample mean as real per-capita M1, and factor two the same mean as real per-capita M2++. These are plotting/index normalizations, not estimated economic restrictions. Figure 7 shows slower second-half growth in the transactions score than in M1 and much larger cyclical movement in the savings score than in M2++. Figure 8 shows that monthly changes in the first score resemble M1 changes but have a lower average, while changes in the second score are substantially more volatile than M2++ changes. The suggested consistency with business cycles or inflation is qualitative; no forecast-loss comparison, inflation regression, out-of-sample test, or welfare calculation is reported.

## Subsample stability and a reproducible implementation boundary

Section 6 repeats estimation on January 1986–December 1989, January 1986–December 1994, January 1995–November 2003, and January 2001–November 2003. These contain respectively 48, 108, 107, and 35 monthly levels, calculated from the stated dates. The last is especially small. Figures 9–10 show no consistent improvement in indicator fit from shortening the sample, with differenced fit generally more stable than level fit. Figure 11 shows broadly similar factor behavior except for the 35-month sample, where level scores differ markedly. The authors attribute much of this to loading uncertainty and regard the evidence as encouraging for stable measurement despite financial innovation. There is no formal structural-break test or confidence interval establishing constant loadings.

A faithful reproduction would assemble the six continuity-adjusted, real per-capita, unadjusted monthly level series; preserve the zero-intercept restriction; difference each series; calculate the sample covariance; fit the two-factor diagonal-uniqueness model; rotate using direct quartimin and Kaiser normalization; retain the fitted $B,\Omega,\Phi$ and mean treatment; and apply the Bartlett matrix to the original levels. It should then reconstruct indicators, compare differences separately from levels, scale factors only for the stated M1/M2++ plots, and repeat the four subsample fits. Comparisons across fits must control signs, permutations, scales, and rotation conventions rather than mistake a relabeling for economic instability.

One implementation detail is unresolved by the paper's notation: it describes 215 monthly observations and also writes sums over $T$ differences. First-differencing 215 available levels yields 214 increments unless a preceding month is supplied. A replication should record which convention was used; the PDF does not state whether December 1985 was available for that purpose. Exact simulation reproduction additionally requires the fitted uniqueness matrix, full factor path, covariance-matching transformation, random seed, and numerical optimization settings. Rounded loadings and figures are insufficient to recover those inputs.

The useful takeaway is a disciplined measurement architecture: estimate stable cross-sectional structure using increments, recover contemporaneous levels without imposing an economic transition equation, and carry loading uncertainty into interpretation of the resulting index. It is especially attractive when a common measurement series must support competing economic models. It remains vulnerable to unstable loadings, poorly identified orientation, correlated unique components, and weak sample information. The paper shows why plausible movements and precise levels are different achievements; it does not establish that its two rotated factors are definitive replacements for monetary aggregates.
