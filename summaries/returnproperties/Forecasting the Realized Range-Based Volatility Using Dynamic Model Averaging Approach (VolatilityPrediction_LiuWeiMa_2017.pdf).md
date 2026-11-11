# Forecasting the Realized Range-Based Volatility Using Dynamic Model Averaging Approach

Jing Liu, Yu Wei, Feng Ma, and M. I. M. Wahab, *Economic Modelling* 61 (2017), 12–26. DOI: [10.1016/j.econmod.2016.11.020](https://doi.org/10.1016/j.econmod.2016.11.020).

Source: [VolatilityPrediction_LiuWeiMa_2017.pdf](../../Finance/VolatilityPrediction_LiuWeiMa_2017.pdf), all 15 PDF pages, including Appendices A and B. Equations below use consistent notation to make the algorithm implementable. Where the printed equations or tables conflict, that conflict is identified rather than silently resolved as an empirical fact.

## Why this matters and the actual contribution

Daily realized-volatility forecasting presents two forms of uncertainty. Parameters within a forecasting model can change, and the identity of the most useful model can change. A jump-augmented model may work well during one episode, a leverage model during another, and an ordinary heterogeneous autoregression during a third. Selecting one specification for the entire sample imposes stability on both dimensions.

The paper applies dynamic model averaging, or DMA, to five heterogeneous autoregressive models of realized range-based volatility. Each model has coefficients updated through a forgetting-factor Kalman filter. Its probability weight is separately updated using recent predictive likelihoods. Dynamic model selection chooses the currently most probable model; dynamic model averaging combines all their forecasts. This is an application of an existing Bayesian forecasting mechanism to range-based volatility, rather than a new derivation of either range estimators or DMA.

The useful methodological idea is the separation of coefficient adaptation from model adaptation. The empirical evidence is more qualified than the abstract suggests. DMA performs strongly on crude-oil futures and survives several model-confidence-set comparisons for the S&P 500. Yet some conventional error measures favor simple combinations, and several appendix entries and sample descriptions are internally inconsistent. A reproduction should preserve the model idea while treating exact rankings as results to verify, not assumptions to build into the implementation.

## Measuring the daily target

Let $p_s$ be the efficient log price. Its continuous component has integrated variance

$$
IV_t=\int_{t-1}^{t}\sigma_s^2\,ds.
$$

With jumps, quadratic variation also contains the sum $J_t$ of squared jumps. A conventional realized variance uses squared nonoverlapping intraday returns. The range estimator instead divides the day into intervals and uses each interval's high-minus-low log-price range $S_{t,i}$:

$$
R_t=\frac{1}{\lambda_{2,m}}\sum_i S_{t,i}^2.
$$

The normalization $\lambda_{2,m}$ is the second moment of a standardized Brownian range observed on the relevant grid. It depends on the number of within-interval observations, denoted $m$. The paper obtains Brownian-range moments by simulation using one million replications. Range efficiency is therefore an ideal-process result conditional on a correctly specified observation scheme, not a blanket guarantee that any high-low series is less noisy than any return-based realized measure.

For a continuous process, the raw range estimator converges to integrated variance. With jumps, its limit is $IV_t+J_t/\lambda_{2,m}$. This differs from quadratic variation. The paper consequently introduces a jump correction involving a bipower estimate $RBV_t$ of the continuous component:

$$
V_t=\lambda_{2,m}R_t+(1-\lambda_{2,m})RBV_t.
$$

Then $V_t$ targets $IV_t+J_t$. For clarity, this note calls the corrected target $V_t$, rather than using the same RRV symbol for the raw and corrected quantities. The algebra matters: simply treating raw range variance as total quadratic variation changes the measured jump component.

A nonnegative jump estimate is

$$
\widehat J_t=\max(V_t-RBV_t,0).
$$

The continuous and significant-jump models additionally use a jump-test statistic $Z_t$ and a significance threshold of 5%. The paper gives a standardized ratio statistic involving a quarticity measure and a range-estimator asymptotic variance constant. However, the full operational definitions of every quarticity and variance-constant input are not self-contained in this PDF. Moreover, a later displayed bipower formula is written using adjacent absolute returns, whereas the earlier discussion concerns range-based bipower variation. These are related estimators but not numerically identical. An exact reproduction needs to settle which construction generated the empirical series, preferably from original code or the authors' data.

All these objects estimate variance, despite the paper's broad use of the word volatility. No square root should be inserted into the regression target merely because the prose says volatility. Table 1 explicitly scales its reported realized measures and jump variations by 10,000. Other tables do not consistently document equivalent scaling, so cross-table or cross-market comparisons should retain the reported units rather than invent a conversion.

## The five individual forecasting models

Define backward-looking averages

$$
V_t^{(5)}=\frac15\sum_{j=0}^{4}V_{t-j},\qquad
V_t^{(22)}=\frac1{22}\sum_{j=0}^{21}V_{t-j}.
$$

The baseline HAR model forecasts the next day's level:

$$
V_{t+1}=c+b_dV_t+b_wV_t^{(5)}+b_mV_t^{(22)}+\varepsilon_{t+1}.
$$

The daily, weekly, and monthly terms capture several persistence scales with few coefficients. This is a restricted finite-lag autoregression, not a mathematical proof of fractional long memory. Each forecasting origin includes the most recent observed day in all three averages.

The jump-augmented model adds $b_J\widehat J_t$. Its purpose is to allow a jump-induced increase in today's total variance to have a different persistence from a continuous fluctuation. A negative jump coefficient conditional on total variance is therefore compatible with jumps raising contemporaneous risk: it can indicate that their contribution decays more rapidly.

The continuous/jump model separates continuous and significant-jump measures at daily, weekly, and monthly frequencies. Its regressor vector contains three continuous components and three significant-jump components, plus an intercept. One reproducibility complication is that printed Equations 13–15 apply a current jump indicator to aggregated weekly or monthly quantities. That is different from first classifying every day and then averaging the classified daily series. These procedures must not be treated as interchangeable without checking the original implementation.

The overnight-information model adds the signed overnight return, defined from the current opening price relative to the previous closing price. It does not simply add the square of the overnight return. An implementation must align the observation time correctly: the overnight term used to predict day $t+1$ must be known at the stated forecast origin, and the target's trading session must be consistently defined.

The leverage specification adds negative-return terms at three horizons. For a horizon $h$, the intended negative-part regressor takes the form

$$
R_t^{(h),-}=\left(\frac1h\sum_{j=0}^{h-1}r_{t-j}\right)
\mathbf1\left\{\sum_{j=0}^{h-1}r_{t-j}<0\right\},
\quad h\in\{1,5,22\}.
$$

This is the negative part of the aggregated return, not the average of individual negative daily returns. The paper calls the model LHAR-RRV-CJ, but its displayed Equation 17 uses the total RRV HAR terms plus negative returns, without the full separate continuous/jump predictor vector. A replication should state whether it follows the displayed equation or the suggestive model name. The displayed equation is the more concrete specification available in the PDF.

## DMA as a reproducible recursion

For model $k$, write the observation and coefficient equations as

$$
V_t=z_{t-1,k}'\beta_{t,k}+\epsilon_{t,k},\qquad
\beta_{t,k}=\beta_{t-1,k}+\eta_{t,k}.
$$

The predictor vector includes the model-specific terms just defined and an intercept. Observation noise has variance $H_{t,k}$, and coefficient innovations have covariance $Q_{t,k}$. Errors are assumed conditionally Gaussian and independent in the way required for the filter.

Let $m_{t-1,k}$ and $C_{t-1,k}$ denote the posterior coefficient mean and covariance after observing day $t-1$. With a coefficient forgetting factor $0<\lambda\leq1$, the prior is

$$
a_{t,k}=m_{t-1,k},\qquad R_{t,k}=C_{t-1,k}/\lambda.
$$

Thus the implied coefficient innovation covariance is

$$
Q_{t,k}=(\lambda^{-1}-1)C_{t-1,k}.
$$

The sentence following Appendix Equation A5 prints the opposite sign. That would make the covariance negative semidefinite when $\lambda<1$ and cannot implement the stated Gaussian random walk. The expression above follows directly from the preceding covariance-inflation equation. The paper also permits zero in an informal range for $\lambda$, but the reciprocal update requires a strictly positive value.

The one-step forecast and predictive variance are

$$
f_{t,k}=z_{t-1,k}'a_{t,k},\qquad
q_{t,k}=H_{t,k}+z_{t-1,k}'R_{t,k}z_{t-1,k}.
$$

After observing $V_t$, compute the innovation, gain, and posterior:

$$
e_{t,k}=V_t-f_{t,k},\qquad
K_{t,k}=R_{t,k}z_{t-1,k}/q_{t,k},
$$

$$
m_{t,k}=a_{t,k}+K_{t,k}e_{t,k},\qquad
C_{t,k}=R_{t,k}-K_{t,k}z_{t-1,k}'R_{t,k}.
$$

These equations repair notation and dimensional inconsistencies in the printed filtering formulas without changing the underlying algorithm. For numerical work, covariance symmetry and nonnegative predictive variances should be checked after each update. A stable equivalent covariance update can be used, but its purpose and any regularization should be documented.

The second forgetting factor, $\alpha$, acts on model probabilities. Let $\pi_{t-1|t-1,k}$ be the previous posterior probability. Before observing day $t$,

$$
\pi_{t|t-1,k}=\frac{\pi_{t-1|t-1,k}^{\alpha}}
{\sum_j\pi_{t-1|t-1,j}^{\alpha}}.
$$

The observation updates these probabilities through predictive likelihoods:

$$
\pi_{t|t,k}=\frac{\pi_{t|t-1,k}\,\varphi(V_t;f_{t,k},q_{t,k})}
{\sum_j\pi_{t|t-1,j}\,\varphi(V_t;f_{t,j},q_{t,j})},
$$

where $\varphi(\cdot;f,q)$ is the normal density with mean $f$ and variance $q$. Computation in log probabilities avoids underflow. Any probability floor would be an implementation choice because the paper does not specify one.

The DMA forecast issued before day $t$ is

$$
\widehat V_{t|t-1}^{DMA}=\sum_k\pi_{t|t-1,k}f_{t,k}.
$$

It must use prior model weights. Using weights updated after observing $V_t$ would leak the target into its own forecast. Dynamic model selection instead takes the forecast from the model with the largest prior probability. With both forgetting factors equal to one, the setup becomes the paper's Bayesian averaging or selection benchmark. Model probabilities can still update through Bayes' rule; this limit does not mean their weights remain literally constant through time.

The reported dynamic setup uses $\lambda=0.99$ and $\alpha=0.94$. For intuition, geometric weights with these factors have half-lives of approximately 69 and 11 observations respectively. Those are calculations from the stated factors, not fitted economic durations. The design permits model relevance to adapt faster than within-model coefficients. The exact initialization of coefficient means, coefficient covariances, model probabilities, and observation-noise variances is not fully specified. Those missing choices prevent an exact numerical reproduction from the PDF alone, particularly during the initial filtering period.

## Combination benchmarks and empirical protocol

Six simpler combinations provide relevant benchmarks. M1 is the equally weighted average, M2 the median, and M3 a symmetrically trimmed mean with 5% trimming. With only five component forecasts, the rounding rule for a 5% trim matters and is not clearly specified. M4–M6 shrink estimated least-squares combination weights toward $1/n$, using shrinkage constants 0.25, 0.5, and 1. Their generic weighting form is

$$
w_{i,t}=\ell_t\widehat\beta_{i,t}+(1-\ell_t)/n,
\qquad
\ell_t=\max\left\{0,1-\frac{\kappa n}{t-h-T_0-n}\right\}.
$$

The denominator requires sufficient estimation observations. The PDF does not completely describe the early-sample handling. Although these are grouped as constant-weight combinations, least-squares weights can change when re-estimated; their distinction from DMA is the absence of its explicit evolving coefficient and probability state, not an assertion that every realized weight is fixed forever.

The oil data are five-minute observations for the one-month WTI futures contract traded on NYMEX, supplied by Tick Data, from January 2, 2007 to May 9, 2014. The stated sample contains 1,851 trading days. The training period comprises the first 1,000 observations, ending December 16, 2010, and the evaluation period runs December 17, 2010 to May 9, 2014 with 850 forecasts. These counts sum to 1,850 rather than 1,851; lag alignment or an excluded observation could explain the difference, but the paper does not resolve it explicitly.

The oil session is described as 6 p.m. through 5:15 p.m. New York time, with a 45-minute break. Short sessions and days with too few transactions are excluded, but the precise thresholds and futures-roll rules are absent. Roll handling is material for both overnight returns and ranges; a reproducer should not splice contracts without documenting the adjustment.

S&P 500 observations run from January 4, 2000 to April 29, 2016, covering the 9:30 a.m.–4 p.m. session. The main text reports 4,012 business days, with 992 out-of-sample forecasts. This implies approximately 3,020 training observations if the reported partition is exhaustive. Appendix robustness claims of 4,020- and 4,120-observation estimation windows exceed the stated total sample and cannot be accepted literally without corrected metadata.

Forecasts are one day ahead, with a fixed-length rolling estimation window advanced each day. The comparison includes five individual HAR models, six combinations, four averaging/selection variants, and GARCH and EGARCH benchmarks: 17 models. There is no allocation or execution experiment. Model performance is statistical predictive performance, without transaction costs, trading constraints, or utility evaluation.

## Loss functions and what the tests establish

The principal confidence-set comparisons use relative forecast errors:

$$
HMSE=\frac1T\sum_t\left(1-\frac{\widehat V_t}{V_t}\right)^2,
\qquad
HMAE=\frac1T\sum_t\left|1-\frac{\widehat V_t}{V_t}\right|.
$$

These losses emphasize proportional accuracy. A given absolute error is much more costly when realized variance is low. Consequently, their rankings need not agree with RMSE, which is often dominated by large high-volatility episodes. Positive targets and a documented policy for near-zero realized variance are necessary for numerical stability; the paper does not give a detailed near-zero rule.

The model confidence set, or MCS, sequentially removes inferior models using range and semiquadratic statistics. The prose discusses a 10% level while several table conventions highlight 25%. A model that survives at a chosen threshold has not been shown to be uniquely best; the procedure has failed to eliminate it relative to the supplied candidate set. A reported value of one should not be interpreted as a 100% probability that the model is optimal.

Appendix B also reports mean error, MAE, RMSE, percentage error, and mixed under/overprediction losses. The mixed losses use a square-root transformation on errors of one sign and an absolute-error transformation on the other. Whether the square-root branch penalizes more heavily depends on the scale of the error: for magnitudes below one it is larger, but above one it is smaller. Thus their asserted asymmetry is unit-dependent and should not be interpreted as a universally ordered economic risk penalty.

## Numerical findings, including contradictory evidence

The in-sample oil HAR estimates have daily coefficient 0.0232, weekly coefficient 0.6771, and monthly coefficient 0.2730, with standard errors 0.0278, 0.0522, and 0.0440 respectively. Its $R^2$ is 0.7798. Adding overnight information raises $R^2$ to 0.7914, with overnight coefficient $-0.0008$ and standard error 0.0002. The dominance of the weekly term is descriptive persistence evidence; it does not identify a particular class of traders as causing volatility.

For the S&P 500, the baseline daily, weekly, and monthly coefficients are 0.1966, 0.5144, and 0.1950, with standard errors 0.0191, 0.0323, and 0.0286. Baseline $R^2$ is 0.5266. The leverage model reaches 0.5827, while the overnight model reaches 0.5422. Jump coefficients are negative conditional on the other regressors: approximately $-0.3517$ for oil and $-0.5156$ for the S&P 500. These results are consistent with jumps having less persistent predictive content than continuous variance.

Under the main oil MCS comparisons, DMA receives values of one across both test statistics and both relative-error losses. That is strong survival evidence within the candidate set. For the S&P 500, DMA's HMSE values are 0.584 and 0.789, and its HMAE values are one. The trimmed combination reaches one under HMSE, while the equal-weight combination also survives. Thus the stock-index evidence does not isolate DMA as the sole acceptable forecast.

Appendix B4 provides more directly interpretable oil error magnitudes:

| Method | MAE | RMSE | Reported percentage error |
|---|---:|---:|---:|
| DMA | 0.396352 | 0.755199 | 0.393964 |
| Dynamic selection | 0.398829 | 0.760614 | 0.396799 |
| Equal-weight combination | 0.413863 | 0.783217 | 0.417234 |
| Basic HAR | 0.427995 | 0.803543 | 0.437009 |
| Bayesian averaging | 0.544212 | 0.828023 | 0.700737 |

These support DMA's oil result in the table's own units. Its RMSE is about 3.6% below the equal-weight combination and 6.0% below basic HAR, calculated from the reported entries. This is a loss reduction, not an annualized volatility change or an investment return.

The S&P 500 conventional-error table tells a different story. Appendix B5 reports DMA MAE of 0.000018 and RMSE of 0.000089, versus 0.000014 and 0.000041 for the equal-weight combination. DMA's percentage-error statistic is lower, 0.669722 versus 0.690905, but its reported RMSE is more than twice as large. This is incompatible with a claim of uniform superiority across all forecast metrics. It may reflect tail errors, a table error, or another implementation inconsistency; the published numbers alone cannot determine which.

There are additional warning signs. The oil appendix reports GARCH forecasts below the realized target for all 850 observations, with errors suggesting an almost zero forecast relative to the target. That warrants a units and implementation audit before treating its very poor ranking as evidence against GARCH generally. The S&P DMA under/over counts are 444 and 548, but the table's associated probability does not match an ordinary two-sided equal-probability binomial calculation. A table labelled as a Diebold–Mariano comparison supplies quantities resembling loss differences without enough standard-error information to reconstruct the claimed significance, and some signs do not reconcile with the RMSE table.

## Robustness, implementation limits, and takeaway

The paper repeats the analysis at ten- and fifteen-minute frequencies. DMA remains competitive, but it is not the top entry in every column. At ten minutes, for example, the S&P Bayesian averaging model receives an HMSE confidence-set value of one while DMA has a lower value. At fifteen minutes, an oil shrinkage combination also obtains the top HMSE value. These findings support examining aggregation frequency and loss sensitivity, not a universal ranking independent of design choices.

Window-length descriptions also differ: the main discussion refers to 900, 1,000, and 1,100 days for oil, while Appendix B discusses 1,000, 1,100, and 1,200. The stock-index window lengths are inconsistent with the total sample as noted above. The parameter-robustness discussion repeats baseline forgetting factors in a way that does not establish a clearly distinct sensitivity exercise. These ambiguities should remain visible in any replication report.

A defensible implementation begins with a transparent target-construction module, then fits the five explicitly documented predictor equations, then adds stable Kalman recursions and probability updating. Forecasts must be stored before observing the target. Each model's forecast, predictive variance, prior weight, posterior weight, and coefficient state should be retained so that an unusual aggregate forecast can be traced to its source. The simplest equal-weight combination is an essential benchmark because it performs well and avoids several undocumented initialization choices.

The paper leaves critical exact-reproduction inputs unresolved: range and bipower construction details, certain jump-test constants, coefficient and variance priors, observation-noise updating, contract rolls, exclusion thresholds, trimming conventions, and inconsistent sample lengths. Filling these gaps with reasonable choices produces a documented implementation of the method, not a claim to have exactly reproduced the authors' numbers.

The strongest supported conclusion is that allowing both model relevance and coefficients to adapt is a plausible and useful forecasting strategy, especially for oil in the reported sample. The broader assertion that DMA dominates every static alternative across markets and criteria is not supported by all of the paper's own tables. For practical use, the first question should be which loss reflects the intended risk decision; the second should be whether DMA improves that loss under a fully specified, genuinely out-of-sample protocol.
