# A Forecast Comparison of Volatility Models: Does Anything Beat a GARCH(1,1)?

Peter R. Hansen and Asger Lunde, *Journal of Applied Econometrics* 20 (2005), 873–889, DOI 10.1002/jae.800. [Original PDF](../../Finance/GARCH_HansenLunde_2005.pdf). All 17 pages were read, including references. The model table, loss functions, realized-variance scaling, bootstrap formulas, result tables and principal performance plots were visually checked. The article refers to a separate 2001 technical appendix; it is not included in this PDF and was not identified by the local filename search. Results requiring that supplement are not claimed to have been independently reproduced.

## Why this matters

The question is whether additional volatility-model complexity improves one-day-ahead variance forecasts enough to survive a comparison against hundreds of alternatives. Looking only at the lowest average loss after searching 330 models overstates the evidence. Conversely, a multiple-comparison procedure dominated by a few unstable models can fail to detect real improvements. The paper combines a relatively precise realized-variance evaluation proxy with the superior predictive ability test, SPA, to address both problems.

Its historical answer depends on the asset. For the Deutsche-mark/US-dollar exchange-rate sample, it finds no significant improvement over GARCH(1,1). For IBM returns, several alternatives outperform that benchmark, with asymmetric responses to positive and negative shocks appearing important. The best overall sample performance is attributed to A-PARCH(2,2). This is not a proof that GARCH(1,1) is optimal for exchange rates generally, nor that A-PARCH(2,2) is uniquely best for stocks. SPA tests a benchmark against a specified family; it does not identify a unique population winner.

## Forecasting object and experimental timing

Let $r_t=\log P_t-\log P_{t-1}$. A model specifies conditional mean $m_t$, variance $f_t=h_t^2>0$, residual $\epsilon_t=r_t-m_t$, and standardized residual $e_t=\epsilon_t/h_t$. The source uses $\sigma_t^2$ for the latent conditional variance and $h_t^2$ for a model forecast. Keeping $f_t$ for the latter avoids confusing variance with its square root.

The data are divided once into an estimation period $t=-R+1,\ldots,0$ and an evaluation period $t=1,\ldots,n$. Parameters are estimated by maximum likelihood on the first period. Those estimates then generate one-step-ahead forecasts over the evaluation period. Variance states can update with newly observed daily returns while the estimated parameter vector remains fixed. The article does not describe rolling or expanding-window parameter re-estimation, and it should not be introduced into a claimed replication.

| Dataset | Estimation period | $R$ | Evaluation period | $n$ |
|---|---|---:|---|---:|
| DM/USD spot exchange rate | October 1, 1987–September 30, 1992 | 1,254 | October 1, 1992–September 30, 1993 | 260 |
| IBM stock returns | January 2, 1990–May 28, 1999 | 2,378 | June 1, 1999–May 31, 2000 | 254 |

Each model is estimated from daily returns, not from the intraday variance measure. Intraday data supply the subsequent evaluation target. This separation is material: the experiment does not compare GARCH models fitted jointly to daily returns and realized measures, nor models using realized variance as a forecast regressor.

The conditional-mean alternatives are zero, a constant, and $m_t=\mu_0+\mu_1\sigma_{t-1}^2$, the source's lagged-variance GARCH-in-mean specification. It is not a contemporaneous standard-deviation-in-mean formula. The standardized density is Gaussian or Student with estimated degrees of freedom, not restricted to an integer. Because the residual is standardized to variance one, a Student implementation needs the corresponding variance normalization and degrees of freedom above two. The paper does not give all numerical parameter constraints used in optimization.

## The 330-model universe

There are 55 variance specifications, crossed with three mean choices and two innovation densities, giving $55\times3\times2=330$. Thirteen variance families use all four combinations $(p,q)\in\{1,2\}^2$; ARCH uses only order one, and H-GARCH and Aug-GARCH use only $(1,1)$. Here $p$ counts variance lags and $q$ residual lags. The latter two restrictions reflect computational cost.

The table's names must be tied to formulas, because the literature has used the same acronym for different specifications. The ordinary GARCH benchmark is

$$
f_t=\omega+\sum_{i=1}^{q}\alpha_i\epsilon_{t-i}^2+
\sum_{j=1}^{p}\beta_j f_{t-j}.
$$

ARCH removes the variance-lag sum. IGARCH imposes total squared-shock and variance persistence one; the printed parameterization sets the first shock coefficient to $1-\sum_{i=2}^{q}\alpha_i-\sum_j\beta_j$. Taylor/Schwert GARCH models $h_t$ using absolute residuals and lagged $h_t$. NGARCH models $h_t^\delta$ using $|\epsilon|^\delta$ and lagged $h^\delta$, with an estimated power.

The asymmetric families include the following source specifications:

$$
\begin{aligned}
\text{A-GARCH: } f_t&=\omega+\sum_i(\alpha_i\epsilon_{t-i}^2+\gamma_i\epsilon_{t-i})+\sum_j\beta_jf_{t-j},\\
\text{NA-GARCH: } f_t&=\omega+\sum_i\alpha_i(\epsilon_{t-i}+\gamma_i h_{t-i})^2+\sum_j\beta_jf_{t-j},\\
\text{V-GARCH: } f_t&=\omega+\sum_i\alpha_i(e_{t-i}+\gamma_i)^2+\sum_j\beta_jf_{t-j}.
\end{aligned}
$$

Threshold GARCH models standard deviation with

$$
h_t=\omega+\sum_i\alpha_i[(1-\gamma_i)\epsilon_{t-i}^{+}-(1+\gamma_i)\epsilon_{t-i}^{-}]
+\sum_j\beta_jh_{t-j},
$$

where $\epsilon^+=\max(\epsilon,0)$ and $\epsilon^-=\min(\epsilon,0)$. In the source's GJR convention the extra indicator is for a **positive** shock:

$$
f_t=\omega+\sum_i[\alpha_i+\gamma_i1\{\epsilon_{t-i}>0\}]\epsilon_{t-i}^2+\sum_j\beta_jf_{t-j}.
$$

The sign of a fitted asymmetry coefficient therefore cannot be interpreted using software that places its indicator on negative shocks without a parameter conversion.

The log-GARCH family in this table uses $\log h_t=\omega+\sum_i\alpha_i|e_{t-i}|+\sum_j\beta_j\log h_{t-j}$. EGARCH instead has

$$
\log f_t=\omega+\sum_i[\alpha_i e_{t-i}+
\gamma_i(|e_{t-i}|-E|e_{t-i}|)]+\sum_j\beta_j\log f_{t-j}.
$$

The expectation in that centering term depends on the standardized innovation density. A-PARCH, the family producing the reported best overall model, uses

$$
h_t^\delta=\omega+\sum_i\alpha_i(|\epsilon_{t-i}|-\gamma_i\epsilon_{t-i})^\delta
+\sum_j\beta_jh_{t-j}^\delta.
$$

For equal-magnitude shocks and positive $\gamma_i$, the negative shock contributes $(1+\gamma_i)^\delta$ and the positive one $(1-\gamma_i)^\delta$. This is the mechanism behind its asymmetric response. NGARCH is this equation with $\gamma_i=0$. GQ-ARCH adds linear lagged residuals, squared residuals and cross-products of different lagged residuals to a variance recursion. H-GARCH and Aug-GARCH are flexible nesting families with shifted shocks and power transformations.

A complete reproduction of all 330 fits still needs clarification of Table I's final two rows. H-GARCH prints $e_t$ without the lag inside a term multiplying lagged volatility; a causal forecast would need the appropriate lagged residual. The Aug-GARCH row contains a lag index $j$ inside sums indexed by $i$ and prints a squared lagged transformed state in its final term. Those displays do not uniquely specify a working recursion without the underlying definition or code. This note does not silently choose a repair and claim to reproduce those fits. The table also does not report every fitted coefficient, initialization, admissibility bound, optimizer setting or convergence outcome. The count of models and central forecast experiment are reconstructable; bit-for-bit recovery of the full fitting exercise is not.

The restriction to at most two lags is a scope choice. The authors argue that larger orders are unlikely to reverse their conclusions because extra lags seldom improve the reported out-of-sample results. That is an empirical judgment about their model universe, not a theorem excluding higher-order, long-memory, stochastic-volatility or other forecasting models.

## Realized variance and its adjustment

For intraday log returns $r_{t,i}$, define $RV_t=\sum_i r_{t,i}^2$. With negligible intraday conditional means and conditionally uncorrelated increments, $E(RV_t\mid\mathcal F_{t-1})$ approximates the next day's conditional variance. Increasing sampling frequency can reduce measurement noise, but excessively fine sampling introduces microstructure dependence. Realized quadratic variation or integrated variance is not generally identical to the ex ante conditional variance; the source acknowledges this in its footnote. The proxy is useful because it is more informative than a single squared daily return, not because arbitrary infill sampling makes tomorrow's random integrated variance deterministic today.

For exchange rates the paper uses 288 intraday returns per day, corresponding to five-minute intervals over 24 hours. For IBM it constructs a cubic smoothing spline through intraday midquotes from TAQ between 9:30 and 16:00 Eastern time, then extracts 130 artificial three-minute returns. There are 480 hypothetical three-minute intervals in a full day, so the observed trading session covers $130/480$ of that grid. The intraday returns are derived from the spline rather than raw regularly spaced trades.

The full-day proxy is

$$
y_t=\widehat c\,RV_t,\qquad
\widehat c=
\frac{n^{-1}\sum_{t=1}^{n}(r_t-\widehat\mu_t)^2}
{n^{-1}\sum_{t=1}^{n}RV_t}.
$$

The reported factors are .8418 for exchange rates and 4.4938 for IBM. The latter exceeds the simple clock-time ratio $480/130=3.6923077$. The source discusses sampling variation, induced intraday autocorrelation, overnight volatility and omitted conditional means as possible explanations, without identifying one empirically. The factor is estimated ex post over the evaluation sample. It is an evaluation-target normalization, not a coefficient available for live forecasting on the first evaluation day. The exact common mean estimator $\widehat\mu_t$ used for this scaling is not fully documented in the article.

Scaling makes the sample average proxy match the sample average squared daily innovation; it does not prove conditional unbiasedness on every date. A constant factor also assumes a stable relation between trading-session and full-day variation. A changing overnight share could violate that relation.

The authors say the common ex post adjustment is unlikely to favor a model because it does not use its forecasts. That is not mathematical invariance of rankings to the scale factor. For example, the difference of two squared-variance losses is

$$
(y-f_0)^2-(y-f_k)^2=2y(f_k-f_0)+f_0^2-f_k^2.
$$

Changing only $y$ changes the first term relative to the second and can change a ranking. The adjustment and the robustness checks therefore matter to the substantive conclusion.

## Six loss criteria and what each measures

For target variance $y_t>0$ and forecast $f_t>0$, average the following daily losses:

| Criterion | Daily loss | Main scale |
|---|---|---|
| MSE1 | $(\sqrt{y_t}-\sqrt{f_t})^2$ | squared volatility error |
| MSE2 | $(y_t-f_t)^2$ | squared variance error |
| QLIKE | $\log f_t+y_t/f_t$ | Gaussian quasi-likelihood loss up to constants |
| R2LOG | $[\log(y_t/f_t)]^2$ | squared log-ratio |
| MAE1 | $\lvert\sqrt{y_t}-\sqrt{f_t}\rvert$ | absolute volatility error |
| MAE2 | $\lvert y_t-f_t\rvert$ | absolute variance error |

MSE2 has fourth-power return units; MAE2 and MSE1 have squared-return units; MAE1 has return units. R2LOG is dimensionless. A common change of return units shifts QLIKE by a common constant and rescales the other level losses, without affecting within-criterion rankings when target and forecasts are changed together. It is different from changing only the proxy adjustment.

The source rejects Mincer–Zarnowitz regression $R^2$ as its primary ranking criterion because an intercept and slope fitted after the fact can repair a badly scaled forecast. High correlation with realized volatility need not mean an unbiased or well-calibrated forecast. The reported losses evaluate the forecast levels directly.

Proxy noise is also loss dependent. If the target proxy is conditionally unbiased for the desired variance and forecasts are measurable at the forecast date, expected differences in MSE2 and QLIKE preserve the corresponding latent-variance ranking: their pairwise loss differences are linear in $y_t$. The other four criteria contain nonlinear transformations or absolute values of $y_t$ and do not inherit that result from conditional unbiasedness alone. A more precise realized proxy helps, but does not make all six criteria mathematically equivalent. The paper's separate work on consistent ranking addresses this broader issue; the 2005 experiment is not a general proof of robustness for arbitrary noisy proxies.

## SPA and reality-check inference

For benchmark model zero and each alternative $k$, set

$$
X_{k,t}=L(y_t,f_{0,t})-L(y_t,f_{k,t}),\qquad
\lambda_k=EX_{k,t},\qquad
H_0:\lambda_k\le0\ \text{for every }k.
$$

Positive expected differential means the alternative beats the benchmark. The same model universe must be retained throughout the comparison. Selecting a model after observing its evaluation performance and applying an ordinary pairwise test ignores the search.

The source assumes a stationary loss-difference vector, suitable mixing, and a moment of order above two, sufficient for a multivariate central limit theorem and stationary-bootstrap approximation. No candidate model need be the true conditional variance model. These are nevertheless substantive assumptions: similar model names do not guarantee finite loss-difference moments, and structural changes can make both inference and interpretation problematic. Finite-sample initialization and estimated parameters also need the regularity underlying the referenced testing theory; stationarity of raw returns alone is not a blanket proof for every fitted forecast sequence.

Let $\omega_k^2$ be the long-run variance of $\sqrt n\,\bar X_k$. A consistently scaled observed statistic is

$$
T_{\mathrm{SPA}}=\max_k\frac{\sqrt n\,\bar X_k}{\widehat\omega_k}.
$$

The reality check uses the unstudentized maximum $\max_k\sqrt n\,\bar X_k$. Multiplying every observed and bootstrap statistic by the same positive constant would not change its $p$-value. What is invalid is using different scaling for the observed and bootstrap statistics. The printed definition on PDF page 7 omits $\sqrt n$, while the bootstrap statistic in equation (2), PDF page 8, includes it and defines $\widehat\omega_k^2$ as a long-run variance. The implementation here explicitly uses $\sqrt n$ on both sides. This is an algebraically necessary consistency clarification, not a claim about what the authors' unavailable code actually did.

The stationary bootstrap resamples the entire vector $X_t$ using common time indices across models, preserving cross-model dependence. In the standard construction, choose a random starting index; at each step continue to the next index with probability $1-q$ or restart uniformly with probability $q$, wrapping at the sample boundary. The reported implementation uses $q=.5$ and $B=10{,}000$ replications. This corresponds to mean block length two under that restart-probability convention. The random seed and block-length sensitivity results are not reported.

For bootstrap averages $\bar X_{b,k}^*$ estimate

$$
\widehat\omega_k^2=\frac nB\sum_{b=1}^{B}(\bar X_{b,k}^*-\bar X_k)^2.
$$

The same scalar standardizer is used across replications for each model. A zero long-run variance requires separate handling; division by zero is not an admissible test statistic.

Recenter bootstrap averages under the null using three mean estimates:

$$
\widehat\lambda_k^l=\min(\bar X_k,0),\qquad
\widehat\lambda_k^c=\bar X_k\,1\{\bar X_k\le-A_{k,n}\},\qquad
\widehat\lambda_k^u=0,\qquad
A_{k,n}=\tfrac14n^{-1/4}\widehat\omega_k.
$$

Then

$$
Z_{b,k}^{*,i}=\bar X_{b,k}^*-\bar X_k+\widehat\lambda_k^i,\qquad
T_b^{*,i}=\max_k\frac{\sqrt n\,Z_{b,k}^{*,i}}{\widehat\omega_k},
\qquad i\in\{l,c,u\}.
$$

The empirical tail fraction $B^{-1}\sum_b1\{T_b^{*,i}>T_{\mathrm{SPA}}\}$ is the reported $p$-value construction. If the observed maximum is nonpositive, the source sets the $p$-value to one. The consistent centering preserves clearly negative mean differentials, removing poor alternatives from the relevant asymptotic maximum, while treating alternatives near the null boundary as zero.

The ordering is $\widehat\lambda^l\le\widehat\lambda^c\le\widehat\lambda^u$, hence the same bootstrap draws give $p_l\le p_c\le p_u$. The text on PDF page 8 once describes the lower and upper bounds in the reverse order, but the formulas, subscripts, subsequent explanation and result tables support the ordering stated here. The original White reality check corresponds to the unstudentized statistic with upper recentering, RC$_u$.

Studentization addresses a different problem from recentering. A poorly performing alternative with very erratic losses can inflate the right tail of an unstudentized maximum and obscure a stable improvement by a good model. Recentring keeps obviously inferior means negative; studentization also controls differences in long-run variability. Neither procedure turns nonrejection into evidence that the benchmark is uniquely optimal.

## Main numerical findings

Table II's consistent SPA $p$-values are:

| Criterion | DM/USD ARCH(1) | DM/USD GARCH(1,1) | IBM ARCH(1) | IBM GARCH(1,1) |
|---|---:|---:|---:|---:|
| MSE1 | .0179 | .4589 | .0002 | .0300 |
| MSE2 | .0748 | .7652 | .0001 | .0288 |
| QLIKE | .0184 | .7707 | <.0001 | .0463 |
| R2LOG | .0002 | .3269 | .0011 | .0630 |
| MAE1 | .0002 | .3296 | .0086 | .0051 |
| MAE2 | .0011 | .2920 | .0100 | .0065 |

At a five-percent threshold, DM/USD GARCH(1,1) is not rejected under any criterion. ARCH(1) is rejected under five, with MSE2 the exception. The deliberately poor ARCH(1) reference demonstrates some ability to detect inferiority in this application; it does not establish power against every small improvement over GARCH(1,1).

For IBM, GARCH(1,1) is rejected under five of the six consistent SPA comparisons; R2LOG at .0630 is the exception. The QLIKE interval from lower and upper centering is [.0379,.0528], so the .0463 consistent value is relatively close to the conventional threshold. MSE1 gives [.0245,.0358], MSE2 [.0260,.0316], MAE1 [.0040,.0058], and MAE2 [.0054,.0078]. These are recentering bounds, not confidence intervals for an economic improvement.

The original reality-check $p$-values for the IBM GARCH benchmark are .2811, .1472, .3750, .6039, .1522 and .1734 in the same criterion order. It rejects none at five percent. For IBM ARCH(1), original RC values are .0164, .0205, .0017, .0713, .1399 and .1941; three criteria fail to reject even that deliberately weak reference. The comparison illustrates loss of power in this dataset, not invalidity of the reality check's null-size control.

The naive selected-model $p$-values for the IBM GARCH benchmark are .0355, .0409, .0213, .0166, .0026 and .0026. They do not adjust for the complete search. A naive value can be larger than SPA's value because the model with smallest average loss need not have the largest studentized improvement. This is why the adjustment cannot be understood as simply multiplying every naive value by 329.

The main density figures place all 330 average sample performances on a horizontal axis of **negative average loss**, so farther right is better. They are distributions across candidate models, not sampling distributions or confidence bands. For exchange rates the GARCH benchmark lies near the best performers. Student innovations have a modest average advantage for some losses. For IBM, asymmetric models perform better, especially under MAE2; Gaussian specifications do better on average, although the best MAE2 model has Student innovations. The three mean specifications have nearly overlapping performance distributions. These descriptive group comparisons are not separately randomized or individually corrected tests of a causal “leverage effect.”

## Robustness and reproduction limits

Table III recomputes IBM GARCH-benchmark SPA comparisons with seven realized-variance constructions: splines with 50 knots/three-minute sampling and 250 knots/two-minute sampling; a Fourier method with $M=85$; linear interpolation at five and one minutes; and previous-tick sampling at five and one minutes.

Across these proxies, MSE1 $p$-values range from .0103 to .0271, MSE2 from .0082 to .0280, and QLIKE from .0112 to .0457. Thus rejection under these three criteria persists across all seven reported methods. R2LOG ranges from .0340 to .0998, MAE1 from .0039 to .0960, and MAE2 from .0056 to .0888; conventional five-percent conclusions for those criteria are sensitive to the proxy. The paper's broad statement of robustness should be read with these numerical qualifications.

The first Table III column is close to, but not identical with, the main IBM results; for example, MSE1 is .0271 there versus .0300 in Table II. The article does not explain every such difference. Bootstrap simulation variation is a possible contributor, but without stored draws or the supplement it cannot be identified as the exact cause. With 10,000 independent bootstrap replications, a tail probability around .05 has Monte Carlo standard error about .00218; this is only simulation uncertainty, not total statistical uncertainty.

A reproducible implementation should freeze the sample split and complete model list before examining evaluation losses; fit every model with documented initialization and constraints; preserve unsuccessful fits and their handling in the audit; recursively forecast using only preceding daily information; construct the same common variance target; retain a full date-by-model loss matrix; and bootstrap its vector rows with shared indices. Report the consistent SPA result together with the lower and upper centering values, benchmark identity, and proxy sensitivity. The six loss criteria constitute six separate questions; this paper's within-criterion correction does not automatically adjust for subsequently selecting the most favorable loss function or asset.

Exact numerical reproduction requires the daily and intraday data, TAQ filtering and corporate-action treatment, spline settings and complete proxy construction, the common mean used in scaling, all fitted parameter vectors, starting values and optimizer choices, the exact mean/density variant of each displayed benchmark, and the bootstrap seed or draws. The missing technical appendix and ambiguities in the last model-table rows are additional limitations. The published main text does not provide a full per-model loss table, so exact economic loss reductions cannot be recovered from its $p$-values alone.

The experiment covers two assets and about one year of evaluation for each, with different historical periods. It establishes evidence about relative variance-forecast performance in those settings. It does not measure tail-risk accuracy, option-pricing errors, portfolio utility, turnover, transaction costs or trading profitability. Its strongest transferable lesson is methodological: compare forecast levels against a well-understood target, preserve the entire model search in inference, and distinguish a rejected benchmark from identification of a unique best model.
