# Forecasting Macroeconomic Variables Using Collapsed Dynamic Factor Analysis

**Authors:** Falk Bräuning and Siem Jan Koopman. **Publication:** *International Journal of Forecasting* 30 (2014), 572–584. DOI: 10.1016/j.ijforecast.2013.03.004. **Original PDF:** [DynamicFactorModels_Brauning_2014.pdf](../../Finance/DynamicFactorModels_Brauning_2014.pdf).

## Contribution and reason for collapsing the panel

The paper proposes a small state-space model that treats principal components as noisy measurements of latent factors and models them jointly with the variable being forecast. Principal components first reduce a large predictor panel to a few series. A second-stage likelihood then estimates the dynamics of the latent factors, their relevance to the target, and the target's own idiosyncratic dynamics. The authors call this a collapsed dynamic factor model, abbreviated CFM.

The distinctive step is to put the principal components on the left-hand side of a measurement equation. In a conventional diffusion-index forecasting regression, principal components enter as observed predictors. Here they are fallible indicators of an underlying state. Kalman filtering combines their information with target observations and estimated dynamics. The target can therefore help determine the filtered factors relevant for its own prediction, while its separate persistent component need not be mistaken for a common factor.

This is a compromise between a simple principal-components regression and fitting a large dynamic factor likelihood to every original panel series. The observation dimension falls from the number of predictors plus targets to the number of retained components plus targets. Maximum-likelihood estimation then operates on a much smaller model. The proposed advantage is especially plausible when $N$ and $T$ are moderate, principal components are noisy, and estimating a large unrestricted system would consume too many degrees of freedom.

The paper provides Monte Carlo comparisons and two US macroeconomic forecasting exercises. Its empirical results support competitiveness, particularly in some short-sample and GDP nowcasting settings, but not uniform superiority. Long-sample industrial-production results often favor simpler or competing models. All empirical forecasts use final revised data, not actual historical data vintages with publication delays. The distinction is essential when assessing usefulness for a live investment or policy forecasting process.

## The uncollapsed target and predictor model

Let $x_t$ be an $N$-vector of predictors and $F_t$ an $r$-vector of common factors. The predictor model is

$$
x_t=\Gamma_{xx}F_t+\varepsilon_{x,t}.
$$

Factor dynamics are represented in a linear Gaussian state space, possibly with a state larger than $F_t$ to accommodate lags. Let $y_t$ be an $L$-vector of targets, usually with $L\ll N$, and let $\alpha_{y,t}$ contain target-specific components. The joint observation equation is

$$
\begin{bmatrix}y_t\\x_t\end{bmatrix}
=
\begin{bmatrix}\Lambda_{yy}&\Gamma_{yx}\\0&\Gamma_{xx}\end{bmatrix}
\begin{bmatrix}\alpha_{y,t}\\F_t\end{bmatrix}
+
\begin{bmatrix}\varepsilon_{y,t}\\\varepsilon_{x,t}\end{bmatrix}.
$$

Targets load on both their own components and the common factors. Predictors load on the common factors but not on the target-specific state. The general exposition allows contemporaneous covariance between target and predictor measurement disturbances. The later simple forecasting specification uses mutually independent disturbance components, so reproducing an experiment requires distinguishing the general framework from the actual covariance restrictions fitted.

For a scalar target, the paper illustrates $y_t=\mu_t+\psi_t+\Gamma_{yx}F_t+\varepsilon_t$, where $\mu_t$ is a trend and $\psi_t$ a cycle or persistent idiosyncratic component. These components can be specified flexibly within a state-space model. The particular stationary forecasting illustration fixes the mean at $\mu$ and uses first-order dynamics for both the target-specific state and factors.

The main modeling choice is asymmetric: the researcher wants to forecast $y_t$, and the other variables matter through the information they provide. The method does not try to optimize forecasts for every predictor. This makes the reduction sensible but also means it can discard information that would matter for a different target or a broader joint forecasting objective.

## Principal components as measurements rather than exact factors

Choose an $r\times N$ matrix $A_{PC}$ from the leading eigenvectors of the predictor panel covariance matrix and form $z_t=A_{PC}x_t$. The reduced model is written

$$
\begin{bmatrix}y_t\\z_t\end{bmatrix}
=
\begin{bmatrix}\Lambda_{yy}&\Gamma_{yx}\\0&I_r\end{bmatrix}
\begin{bmatrix}\alpha_{y,t}\\F_t\end{bmatrix}
+
\begin{bmatrix}\varepsilon_{y,t}\\\varepsilon_{PC,t}\end{bmatrix}.
$$

Thus $z_t=F_t+\varepsilon_{PC,t}$. Factor coordinates are aligned with the principal-component coordinates, and uncertainty in those coordinates is represented through an estimated measurement-error covariance. The authors motivate the identity loading through $A_{PC}\Gamma_{xx}\approx I_r$. The approximation becomes more plausible when the leading principal components accurately recover the common space.

This construction is a parsimonious approximation, not a general proof that the leading components are sufficient statistics for forecasting the target. Principal components maximize panel variance explained, which need not equal target predictive relevance. The second-stage likelihood can reweight and smooth the retained information, but it cannot reconstruct a target-relevant direction discarded in the first-stage projection.

The model estimates $\operatorname{Var}(\varepsilon_{PC,t})$ rather than declaring it zero. If this matrix shrinks to zero in a direction, the corresponding latent factor is effectively observed through its principal component. If measurement error is material, the filter balances that observation against predicted factor dynamics and information from the target. The paper's numerical results indicate that this variance is often close to zero for the US panel, but more noticeable in selected weak-signal simulations.

Unlike a full panel likelihood, the collapsed likelihood does not estimate all $Nr$ predictor loadings jointly. Unlike the two-step approach attributed to Doz, Giannone and Reichlin, it does not merely insert first-stage loading and VAR estimates into a large system and then smooth. It estimates the remaining parameters of the small target-plus-component system by maximum likelihood. This comparison concerns the specific procedures implemented in the paper, not every possible later variant of those model families.

## Dynamics, likelihood, and forecasts

The paper's simple forecast illustration is

$$
y_t=\mu+\psi_t+\Gamma_{yx}F_t+\varepsilon_t,
$$

$$
\psi_{t+1}=\phi\psi_t+\kappa_t,\qquad
F_{t+1}=\Phi F_t+\zeta_t,
$$

with $|\phi|<1$, a stable $\Phi$, and serially and mutually independent Gaussian innovations. The principal-component measurement equation is appended to this target equation. The factor innovation covariance, target innovation variance, observation variances, loadings, mean and dynamic coefficients are estimated within the chosen restricted specification.

For known parameters and the available information set $\mathcal I_T$, the forecast is

$$
\widehat y_{T+h}=\mu+\phi^h\widehat\psi_{T|T}+\Gamma_{yx}\Phi^h\widehat F_{T|T}.
$$

The filtered states condition on the target and collapsed predictor history. This is an iterated forecast from one estimated dynamic system. Under the correctly specified Gaussian model it is a conditional mean; with estimated or misspecified parameters it is a plug-in model forecast, not an unconditional guarantee of minimum forecast error.

A reproducible likelihood implementation uses the Kalman prediction errors $v_t$ and their covariances $S_t$. Apart from constants, the Gaussian objective is

$$
\ell(\theta)=-\frac12\sum_t\left[\log|S_t|+v_t'S_t^{-1}v_t\right].
$$

The sum includes only observed components at each date. Missing measurements remove corresponding update rows; they do not require filling the target with its eventual realized value. This equation is the standard state-space likelihood underlying the paper's estimation description. The article does not provide a complete optimizer configuration or all numerical initialization choices, so these must be specified in a reproduction.

The SW comparison uses direct horizon-specific regressions of $y_{t+h}$ on current and lagged target values and extracted factors. Its regression coefficients are reestimated separately for each horizon. Consequently, differences between SW and CFM reflect both factor treatment and forecast construction. A comparison should not attribute the entire MSE difference to measurement-error correction alone.

## Mixed frequencies and the cumulator construction

For quarterly targets and monthly predictors, the latent dynamics evolve monthly. The quarterly target is observed only when the corresponding quarterly measurement is available; other monthly target rows are missing. The paper adds a cumulator state intended to connect monthly latent growth to quarterly growth.

For its illustrative aggregation rule, let $y_t$ be annualized monthly latent growth and define

$$
y^C_{t+1}=\delta_t y^C_t+\frac13y_{t+1},\qquad
\delta_t=\begin{cases}0,&t\text{ is a quarter end},\\1,&\text{otherwise.}\end{cases}
$$

Observe $y_t^C$ at quarter ends and observe the principal components every available month. The reset prevents growth from accumulating indefinitely across quarters. A state vector $(y_t,y_t^C,\psi_t,F_t')'$ then contains the latent monthly target, accumulated quarterly target, idiosyncratic state, and common factors.

There are implementation-relevant inconsistencies in the supplied source's mixed-frequency formulas on p. 577. Equation (14) averages monthly values with indices shifted one month earlier than the stated quarter-end accumulation recursion. In addition, the displayed explicit transition matrix has a leading one in its second row, although solving the preceding implicit transition equation and using the stated cumulator gives a zero there. These are visible in the rendered PDF, not merely extraction artifacts.

For the stationary zero-mean illustration, direct substitution of the stated recursions yields the internally consistent transition rows

$$
T_t=
\begin{bmatrix}
0&0&\phi&\Gamma_{yx}\Phi\\
0&\delta_t&\phi/3&\Gamma_{yx}\Phi/3\\
0&0&\phi&0\\
0&0&0&\Phi
\end{bmatrix}.
$$

This is an algebraic reconstruction from the paper's equations, not a claim about the authors' unpublished code. A reproduction should record which convention it uses and test quarterly accumulation on a deterministic monthly sequence before evaluating forecasts.

There is also an economic aggregation qualification. Averaging annualized monthly log growth exactly gives annualized endpoint-to-endpoint quarterly log growth under aligned indices. Published quarterly GDP is a flow aggregated over a quarter, whose log growth is generally not the same endpoint identity. The article acknowledges the flow distinction, but its displayed averaging rule should not be treated as a universally exact mapping for arbitrary quarterly GDP definitions. The aggregation operator must match the data being forecast; changing it creates a modified implementation whose results may differ from the table.

## How a new observation changes the target forecast

The Kalman update makes the information-combination mechanism explicit. If the predicted state has mean $a_t$ and covariance $P_t$, and the available observation has loading matrix $Z_t$ and noise covariance $H_t$, then its innovation covariance is $S_t=Z_tP_tZ_t'+H_t$. The gain is $K_t=P_tZ_t'S_t^{-1}$ and the updated state mean is $a_t+K_t v_t$. This standard recursion shows how the estimated principal-component noise changes the response to a new panel observation: increasing its measurement variance reduces the weight on that innovation, conditional on the rest of the system.

A target observation can also change the common-factor estimate because the target loads on the factor state. The update allocates its surprise between the common factors, the target-specific state and observation error according to their predicted covariances. A persistent target deviation need not be assigned entirely to the panel factor. Conversely, a broad panel movement can revise the factor state and thereby revise a target forecast even when the target itself has not yet been released.

In a missing-target month, only the observed component rows participate in this update. The state still propagates and accumulates monthly information toward the quarterly target. This explains the practical attraction of the state-space framework for a jagged observation calendar. It does not by itself solve first-stage PCA on an arbitrarily missing predictor panel: the principal components still need to be constructed under an explicit missing-data convention. The article emphasizes the framework's flexibility but does not supply every algorithmic detail for that first-stage problem.

These recursions are also useful verification targets. Setting component measurement noise near zero should force the corresponding filtered state toward its observed component coordinate. Removing target observations should prevent direct target updates, and increasing an observation variance should change the gain continuously. Such checks validate the intended statistical mechanism without inventing additional predictive evidence beyond the paper's experiments.

## Monte Carlo data-generating process

The simulated panel and target satisfy

$$
x_{it}=\sum_{j=1}^r\lambda_{ij}f_{jt}+\xi_{it},\qquad y_t=x_{0t},
$$

with $r=2$ common factors. Predictor loadings are drawn from a standard normal distribution. The factor and idiosyncratic processes are

$$
f_{j,t+1}=\rho f_{jt}+u_{jt},\quad u_{jt}\sim N(0,1-\rho^2),
$$

$$
\xi_{i,t+1}=d\xi_{it}+v_{it}.
$$

The factor innovation scaling gives unit stationary factor variance. The covariance of idiosyncratic innovations is

$$
Q_{ij}=\sqrt{q_iq_j}\,\tau^{|i-j|}(1-d^2),\qquad
q_i=\frac{c_i}{1-c_i}\sum_{j=1}^r\lambda_{ij}^2.
$$

With the corresponding stationary initialization, the fraction of the variance of $x_{it}$ attributable to its idiosyncratic component is $c_i$. The parameter $d$ controls serial persistence; $\tau$ controls cross-sectional correlation. In the ordinary designs, $c_i$ is uniform on $[C,1-C]$, giving mean one-half.

The reported panel widths are $N=10,50,100$ and time dimensions $T=50,100$. Horizons are $h=1,2,3,6,12$. Every experiment uses 5,000 simulated forecasts. All methods are supplied the correct number of factors and the intended lag specification, so these experiments do not include the practical error from selecting model dimension. The AR benchmark is explicitly AR(2).

Table 1 uses $\rho=0.9$, $d=0$, $\tau=0$, and $C=0.1$. Table 2 uses $\rho=0.9$, $d=0.5$, $\tau=0.5$, and $C=0.1$. Table 3 keeps the latter persistence and correlation parameters but fixes $c_i=0.9$, making common-factor variation only 10% of each series' variance. This is a weak signal-to-noise design, not a formal asymptotic weak-factor loading sequence.

The prose calls the first experiment homoskedastic, but its table caption and variance formula retain random $c_i$ and loading-dependent $q_i$. The explicit stated DGP should govern a reproduction. The source also does not spell out every target-index loading draw, target-error covariance convention, random seed, initial-state treatment, and numerical likelihood constraint. Those omissions prevent a claim of exact code-level reproducibility from the article alone.

## Benchmarks and simulation findings

Seven methods are compared: random walk, local level, AR(2), partial least squares, SW principal-component forecasting, DGR smoothed-factor forecasting, and CFM. Partial least squares constructs components to maximize covariance with the target, giving it a different first-stage objective from PCA. Local level uses a random-walk target level without common-factor information.

In the exact-factor design at $N=50,T=100,h=6$, Table 1 reports MSE 0.9605 for CFM, 1.0235 for SW, 1.0236 for DGR, and 1.0021 for AR. The CFM reduction relative to SW is about 6.2%, calculated from those entries. At $h=1$ in the same panel, PLS has MSE 0.6602, CFM 0.6685, and SW 0.6731. The collapsed model therefore does not dominate the targeted component method at the shortest horizon.

In the approximate-factor design with the same panel dimensions, Table 2 gives $h=6$ MSEs of 0.9665 for CFM, 1.0101 for SW, and 1.0077 for DGR. At $h=12$, the respective numbers are 1.1180, 1.2020, and 1.2081. The longer-horizon advantage is meaningful but moderate. With $N=10,T=50,h=6$, AR is 1.0038 and CFM 1.0090, another case where a simple univariate model remains competitive.

The weak-signal experiment provides a more direct test of noisy component estimates. At $N=10,T=50,h=1$, CFM has MSE 0.8350, compared with 0.8570 for SW, 0.8593 for DGR, and 0.8382 for AR. At $N=10,T=100,h=1$, CFM is 0.7419 against 0.7762 for both AR and SW. At $N=100,T=100,h=12$, CFM is 1.0792 and AR 1.1019, while SW is 1.1510.

These results support the mechanism that a small dynamic system can moderate errors from treating estimated components as exact regressors. They do not establish that all gains arise from this mechanism, since methods differ in estimation and multi-step forecasting design. The tables report average squared errors without Monte Carlo uncertainty intervals. Small differences should be read in that light, especially where several methods are nearly tied.

## Empirical data and evaluation protocol

Both applications use the Stock–Watson panel of 132 monthly US indicators covering 1960–2003, with transformations referred to the underlying dataset documentation. The targets are monthly industrial production and quarterly GDP. Parameters and factors are estimated recursively. The authors evaluate mean squared error and mean absolute error, comparing short and long evaluation samples.

The empirical study explicitly excludes publication delays and data-vintage revisions. It uses final revised data. Therefore it is a recursive or pseudo-real-time exercise conditional on revised observations, not a reconstruction of what a forecaster could actually have known on each historical release date. The ability of a state-space model to handle missing observations does not change this limitation in the reported evaluation.

For industrial production, Table 4 labels the short evaluation period 1990–2003 and the long period 1970–2003, with an initial estimation window beginning ten years earlier. Models are compared with one, two, three, and a Bai–Ng-selected number of factors; the source says the latter is seven for this dataset. The table presents horizons one, two, three and six months, although the prose discusses horizons through six more generally.

The source contains date/count discrepancies that should be resolved before claiming exact replication. Table 4's note associates 138 and 378 forecasts with calendar intervals whose inclusive monthly counts differ. Table 5 labels its short GDP sample 1992–2003 but its note gives an earlier starting quarter with a count of 43 forecasts. Those descriptions cannot all be taken literally at once. A new implementation should publish the actual forecast-origin list, target dates, lag losses and end-of-sample trimming, rather than silently guessing the intended sample.

Forecast-comparison markings use two-sided Diebold–Mariano tests at the 15% significance level. This is a relatively permissive threshold, and the article reports only some significant differences. It does not provide the full horizon-specific long-run variance estimation settings or a multiple-comparison adjustment. The markings should not be restated as broad 5% significance or as evidence that every favorable MSE difference is statistically established.

## Industrial-production results

The short-sample results favor CFM at several horizons. With two factors, its MSEs at $h=1,2,3,6$ are 0.5886, 0.5901, 0.6264, and 0.6439. The corresponding DGR values are 0.5882, 0.6243, 0.6652, and 0.6795. Thus DGR is slightly better at one month, while CFM gains at later horizons. The two-factor CFM MAEs are 0.6012, 0.6033, 0.6310, and 0.6597.

With three factors in the short sample, CFM reports MSE 0.5829 at two months and 0.6339 at six months. The AR benchmark gives 0.6083 and 0.6781. These comparisons are useful evidence that collapsing the panel can add information beyond the target's own lag structure in that evaluation period.

Long-sample evidence is less favorable. With two factors and a one-month horizon, CFM MSE is 0.7151, compared with 0.6491 for SW and 0.6414 for DGR. At six months, CFM is 0.8713 versus 0.7980 for SW and 0.7998 for DGR. AR gives 0.8100 at six months. The proposed model is therefore materially worse than several alternatives in this configuration.

The authors report that estimated principal-component measurement noise is near zero in the empirical panel. That weakens the particular errors-in-variables rationale for large empirical gains in this dataset, even though the dynamic target model and forecast construction still differ. Their overall finding is that factor models do not dramatically beat simple autoregressions for this target, particularly at longer horizons.

The paper discusses large errors before the Great Moderation. That historical interpretation is plausible, but comparing the numerical size of MSE with MAE is not itself a scale-invariant outlier diagnostic because they use different units. The table supports comparison of the same loss across models and samples; a stronger claim about outliers would require the forecast-error distribution or a common-scale diagnostic.

## Quarterly GDP results

The GDP comparison includes random walk, local level with a cumulator, an autoregressive latent monthly model with a cumulator, pooled bridge equations, the mixed-frequency Banbura–Rünstler factor method, and CFM. Bridge-equation forecasts combine individual-indicator forecasts with weights based on inverse historical MSE. The factor methods are evaluated at one, two, three and six months before the target quarter-end measurement under the paper's convention.

At one month, the forecast origin is in the second month of the quarter; at two months it is in the first month. These are nowcasts of an ongoing quarter in the source's stylized timing. They should not be interpreted as an actual release-calendar study, since the experiment explicitly omits publication delays.

In the short sample, the one-factor CFM has one-month MSE 0.2652, compared with 0.3329 for the corresponding BR model and 0.3003 for bridge equations. With the Bai–Ng-selected factors, the CFM MSE is 0.2681 against BR's 0.4640. At six months, three-factor CFM gives 0.3377, compared with BR's 0.3499 and bridge equations' 0.3506. These are reported loss values, not percentage growth forecasts.

Long-sample results depend strongly on dimension and horizon. With one factor at one month, BR is better: 0.5441 versus CFM's 0.6270. With two factors, CFM improves to 0.5493 while BR is 0.8596. With the selected factor count at two months, CFM is 0.4671, BR 0.7190, and bridge equations 0.7650. At six months with three factors, BR is 0.7756 and CFM 0.9435, reversing the ranking again.

The useful empirical conclusion is that jointly modeling the target and collapsed components can substantially improve some GDP forecasts, especially compared with a poorly performing higher-dimensional comparator. It is not that extra factors always help, or that CFM is the best model at every forecast origin and horizon. Factor count remains an important modeling choice whose panel-wide variance criterion need not optimize the target forecast.

## Reproduction requirements and practical takeaways

A faithful reimplementation should save the exact panel version and transformations, every recursive training endpoint, the component normalization, the target's exclusion or inclusion in the predictor panel, factor-count choices, and the fitted covariance structure. Principal components and scaling must be recomputed using only the observations permitted at each origin; full-sample component extraction would introduce information unavailable to the recursive forecaster. It should also record stationarity constraints, starting values, optimizer tolerances, failed fits and boundary measurement-variance estimates.

For mixed-frequency work, test the aggregation algebra and calendar alignment independently of the optimizer. The source's printed inconsistencies leave enough ambiguity that agreement with one equation is not sufficient. For comparison methods, preserve direct versus iterated forecasting, lag specifications and component counts; replacing them with better-tuned modern variants would answer a different benchmarking question.

The framework is appealing when the target has distinct dynamics and a moderate predictor panel contains a small common space. It provides a disciplined way to smooth noisy component estimates while retaining a manageable likelihood. Its limitations are equally clear: first-stage projection can lose useful information, Gaussian and linear specifications can be wrong, parameter uncertainty is not automatically reflected in plug-in forecasts, and favorable revised-data results do not establish live performance after publication lags and revisions. The paper's substantive innovation is the target-centered measurement model for principal components, together with evidence showing when that parsimonious construction is competitive.
