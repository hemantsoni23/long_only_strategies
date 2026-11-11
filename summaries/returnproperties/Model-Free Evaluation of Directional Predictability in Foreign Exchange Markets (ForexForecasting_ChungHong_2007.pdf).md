# Model-Free Evaluation of Directional Predictability in Foreign Exchange Markets

**Jaehun Chung and Yongmiao Hong. Journal of Applied Econometrics 22, 2007, pp. 855–889. DOI: 10.1002/jae.965.**

**Source:** [ForexForecasting_ChungHong_2007.pdf](../../Finance/ForexForecasting_ChungHong_2007.pdf), complete 35-page article, including equations, all five empirical tables, and references. Page numbers below are printed journal pages. The source refers some normalization formulas and asymptotic proofs to Hong and Chung's 2006 working paper; those items are not an embedded appendix to this PDF.

## Why this matters

A return process can have little predictable conditional mean while the probability of a large positive or negative movement varies substantially over time. For currency risk management, a forecast of a threshold crossing can be useful even when a point forecast of tomorrow's return scarcely improves on zero. Chung and Hong investigate this distinction directly, without choosing a particular autoregression, volatility model, or classifier in advance.

Their main tool is a generalized cross-spectral test. It looks for dependence between a future binary event and nonlinear transformations of lagged returns or interest-rate differentials, accumulating evidence over many lags. Derivatives of the characteristic-function representation then isolate dependence on particular powers of lagged predictors. The paper also extends the exercise to joint threshold crossings in two currencies.

The principal empirical finding is strongest for **large-move events**, at thresholds of half or one sample standard deviation. Ordinary zero-threshold up/down predictability is much less uniform than the article's broad concluding language might suggest. Lagged squared returns are especially informative about large individual-currency moves, whereas the level of interest-rate differentials often contains useful information. Joint large events also display dependence, but with important differences across currency pairs and predictor sets.

These are statistical rejection results. The paper does not estimate calibrated probabilities, show forecasting hit rates, implement a trading policy, or report net investment returns. Larger test statistics measure stronger evidence against a null under a particular design; they are not direct measures of economic forecasting accuracy or expected profit.

## Events, information sets, and the correct null

Let $Y_t$ be a percentage log change in a currency price. This note uses the table convention

$$
Y_t=100\log(S_t/S_{t-1}).
$$

The data section instead writes $100\log(S_{t+1}/S_t)$. These are equivalent only after a consistent index shift. When joining predictors, preserve the information requirement: the event return must occur after the lagged predictor is observed. In particular, do not combine a forward-indexed target with a same-day closing predictor that arrives after the spot quote.

For $c\ge0$, define separate upper- and lower-tail indicators,

$$
Z_t^+(c)=\mathbf1\{Y_t>c\},\qquad
Z_t^-(c)=\mathbf1\{Y_t<-c\}.
$$

The empirical thresholds are $c=a\widehat\sigma_Y$ with $a\in\{0,0.5,1\}$, where $\widehat\sigma_Y$ is the sample standard deviation of that return series. A negative-event indicator is one on a sufficiently large negative return and zero otherwise. At a positive threshold, zero includes both small negative changes and every positive change: this is not a binary classification restricted to large observations.

For own-return history $\mathcal I_{t-1}=\sigma(Y_{t-1},Y_{t-2},\ldots)$, the stated null is

$$
H_0:E[Z_t(c)\mid\mathcal I_{t-1}]=E[Z_t(c)]\quad\text{almost surely}.
$$

An analogous null uses the history of interest-rate differentials $ID_t=r_t^{US}-r_t^{foreign}$. It asks whether that history changes the event probability, without requiring uncovered interest parity's exact relation between expected returns and the interest differential.

Because $Z$ is Bernoulli, its conditional mean determines its conditional distribution. However, the implemented tests largely examine dependence with **each individual lag**, or with a two-currency vector at a common lag. Dependence on an interaction of several different lags can exist even when all individual lag-pair relationships vanish. Thus a rejection provides evidence against the full-history null, while a non-rejection is not proof of independence from every possible function of the full past.

The thresholds use full-sample standard deviations for descriptive inference. An investable extension would need thresholds estimated using only past data or a fixed economic cost scale. The paper does not run that extension. It avoids thresholds above one standard deviation because event counts become small and futures price limits can produce additional clustering and distortions.

## Why variance can predict a threshold event without predicting the mean

Consider the illustrative location-scale process $Y_t=\mu+\sigma_t\varepsilon_t$ with symmetric innovations. Then

$$
P(Y_t>c\mid\mathcal I_{t-1})=1-F_\varepsilon((c-\mu)/\sigma_t).
$$

This identity explains the paper's empirical pattern; it is not an estimated model in the article. If $c=\mu=0$, changing a symmetric distribution's scale leaves the up probability at one half. At a positive threshold, higher volatility increases the probabilities of both upper and lower crossings even when the mean remains zero. With nonzero mean, changes in scale can also affect the zero-threshold sign probability. Time-varying asymmetry creates further possibilities.

Accordingly, predicting the occurrence of a large negative move need not mean predicting whether the next large move will be negative rather than positive. A variance predictor can warn of both. This distinction is critical when interpreting the stronger statistics at nonzero thresholds as directional forecasting evidence.

## Generalized cross-spectrum and the test numerator

For a scalar predictor $X_t$, which can be a return or an interest differential, define a characteristic-function covariance at positive lag $j$:

$$
\sigma_{ZX,j}(u,v)=E[e^{i(uZ_t+vX_{t-j})}]-E[e^{iuZ_t}]E[e^{ivX_{t-j}}].
$$

The generalized cross-spectrum Fourier-transforms these lagged dependence measures. Characteristic functions exist without ordinary moment assumptions, so the omnibus construction can detect nonlinear relationships not visible in ordinary covariance. Its asymptotic validity still requires dependence and stationarity conditions; existence of a characteristic function is not itself a complete testing theorem.

Differentiating once with respect to the event coordinate and evaluating at zero gives

$$
\sigma^{(1,0)}_{ZX,j}(0,v)=i\operatorname{Cov}(Z_t,e^{ivX_{t-j}}).
$$

For a binary target, vanishing of this expression for every $v$ characterizes constancy of the conditional event probability given that lagged predictor. The sample estimator uses the $T-j$ aligned observations and lag-specific empirical marginal means. The smoothed spectral estimator in equation (10) uses a kernel $k(j/p)$ and finite-sample factor $(1-j/T)^{1/2}$.

By Parseval's identity, the quadratic discrepancy from the null flat spectrum can be computed directly in the lag domain:

$$
\widehat Q(1,l)=\sum_{j=1}^{T-1}k^2(j/p)(T-j)
\int\left|\widehat\sigma^{(1,l)}_{ZX,j}(0,v)\right|^2dW(v).
$$

For the omnibus test, $l=0$ and $W$ is the standard normal distribution. For derivative tests with $l\ge1$, the weight is concentrated at $v=0$, so the integral evaluates the relevant derivative at zero. The factor $T-j$ already appears in this definition; adding an extra sample-size multiplier because the adjacent prose refers to $TQ$ would change the statistic.

A useful exact implementation shortcut follows from the normal weighting. For a given lag, let $n=T-j$, $x_a$ be the aligned predictor values, and $a_a=z_a-\bar z$ with the mean taken over those aligned observations. Then the omnibus integral is

$$
\frac1{n^2}\sum_{a=1}^{n}\sum_{b=1}^{n}a_a a_b
\exp\left[-\frac12(x_a-x_b)^2\right].
$$

This is a mathematical reconstruction from the stated characteristic-function integral, not code supplied by the authors. It avoids quadrature error by using the characteristic function of a standard normal weight. It also shows why scaling $X$ matters for a fixed frequency weight: multiplying the predictor by a constant changes the kernel distances. Numerical centering, normalization, and rate units must therefore match the original preprocessing.

## Derivative tests: what their names actually measure

For $l=1,2,3,4$,

$$
\sigma^{(1,l)}_{ZX,j}(0,0)=i^{l+1}\operatorname{Cov}(Z_t,X_{t-j}^{l}).
$$

The complex phase disappears after taking squared modulus. The derivative test numerators therefore accumulate squared lagged covariances between the event and the predictor's first through fourth raw powers. The source calls these level, volatility, skewness, and kurtosis tests.

Those labels are useful mnemonics, but require care. $X^2$ is not a separately estimated conditional variance, and $X^3$ and $X^4$ are not normalized conditional skewness and kurtosis. Nonzero mean and variance changes can affect raw powers. A significant cubic or fourth-power test does not uniquely identify a time-varying third or fourth conditional central moment. Likewise, dependence on a power does not prove that a polynomial forecasting model will be stable or optimal.

A final family replaces the predictor with its own directional indicator, yielding $M_{ZZ}(1,0)$ for returns and the analogous interest-differential direction test. For positive thresholds, the target and predictor indicator definitions must be kept consistent with the corresponding positive or negative event. The paper says it centers/rescales interest differentials at zero; exact additional scaling and the indicator threshold convention need to be reproduced from original implementation material.

## Standardization, bandwidth, and inferential assumptions

The standardized scalar statistic in equation (14) is

$$
M_{ZX}(1,l)=
\frac{\widehat Q(1,l)-\widehat C_{ZX}(1,l)\sum_{j=1}^{T-1}k^2(j/p)}
{\sqrt{\widehat D_{ZX}(1,l)}}.
$$

The centering and variance factors account for sampling variation in the quadratic statistic and serial dependence in predictors. They cannot be replaced by an ordinary regression standard error or an independent-lag chi-squared formula. **The source does not print their scalar expressions**, referring instead to Hong and Chung (2006). The 2007 PDF consequently permits a precise implementation of events, transformations, and the quadratic numerator, but not a verified numerical reproduction of the published scalar $M$ values without that methodological reference or original code. A public author-page link to the companion working paper was located but returned an unavailable PDF; no unverified formula has been substituted here.

The reported null limit is standard normal, and rejection is **upper-tailed**: the paper uses approximately **1.65 at 5%** and **2.33 at 1%**. Negative $M$ values are not significant evidence in the opposite direction. They indicate a quadratic dependence measure below its estimated null centering. The statistic itself does not identify the sign of the predictive relationship because its numerator aggregates squared covariances.

The empirical kernel is **Bartlett**, $k(x)=(1-|x|)\mathbf1\{|x|\le1\}$. Reported tables use a **preliminary or pilot lag order of 21**. The source describes a data-driven bandwidth choice based on minimizing an asymptotic integrated mean-squared error and distinguishes this from its pilot order. It does not provide all plug-in calculations or the realized selected bandwidth for each test. A fixed Bartlett truncation at 21 is therefore a transparent reconstruction variant, but should not automatically be called the original implementation.

Robustness uses pilot orders roughly 11–50; one prose footnote says through 51 while the table notes say through 50. Only the 21-pilot results are displayed. There is no published multiple-testing adjustment over currencies, signs, thresholds, moments, pairs, and pilot choices. Many reported statistics are very large, but borderline single tests should not be interpreted at face value as familywise discoveries.

High-order derivative tests need corresponding finite moments and stronger regularity than the bounded characteristic-function omnibus test. Interest-rate differentials have first-order autocorrelations near one, creating a further finite-sample challenge for a strictly stationary framework. These issues are part of the inferential design, not solved merely by describing the approach as model-free.

## Joint events and two-currency predictors

For currencies 1 and 2, define

$$
Z_t^+(c_1,c_2)=\mathbf1\{Y_{1t}>c_1,Y_{2t}>c_2\},\qquad
Z_t^-(c_1,c_2)=\mathbf1\{Y_{1t}<-c_1,Y_{2t}<-c_2\},
$$

with $c_k=a\widehat\sigma_{Y_k}$ and common multiplier $a=0,0.5,1$. The scale is currency-specific, so a one-standard-deviation event is not a common percentage move across currencies.

For a joint lagged predictor, replace $e^{ivX_{t-j}}$ by $e^{i(vX_{1,t-j}+wX_{2,t-j})}$. The omnibus quadratic measure integrates over independent normal weights in $v$ and $w$. The Gaussian-kernel shortcut becomes

$$
\exp\left[-\frac12\{(x_{1a}-x_{1b})^2+(x_{2a}-x_{2b})^2\}\right]
$$

inside the same centered-event double sum. This tests independence of the event from the **predictor vector**. It does not require the two predictors to be independent of each other, despite the source's loose use of “mutually independent” in describing the characteristic-function condition.

The mixed derivative family differentiates $l$ times in **each** predictor coordinate. At zero it corresponds, up to a complex phase, to

$$
\operatorname{Cov}(Z_t,X_{1,t-j}^{l}X_{2,t-j}^{l}).
$$

Thus the $l=1$ joint test concerns the product of the two lagged returns, not two separate linear coefficients. Its results cannot be read as an ordinary two-regressor conditional-mean test. The authors also run scalar tests using each currency's predictor individually. Comparing these constructions reveals whether joint-event dependence is associated with one component or with joint functions, but different test powers prevent a mechanical causal decomposition.

Equation (21) prints joint normalization factors in terms of the estimated Bernoulli event probability and generalized predictor covariance functions. Its notation appears to use cross-covariances between the two scalar predictor series rather than a fully explicit covariance kernel for the vector-valued transform. It also uses a one-dimensional argument in a centering term where the quadratic statistic has two frequency coordinates. These details require checking against the underlying methodological derivation or code; implementing them literally without validation is not enough to claim a reproducible calibrated test. The paper states that the joint asymptotic proof is an extension of the companion work rather than providing it here.

## Market data and alignment

The six currencies are Australian dollar (AD), Canadian dollar (CD), British pound (BP), Japanese yen (JY), Swiss franc (SF), and Deutschemark (DM). Spot prices are Federal Reserve New York noon buying rates for cable transfers, quoted in foreign currency units per U.S. dollar. Futures are CME daily closing prices from Datastream, denoted with an F prefix.

All series begin **December 1, 1987**. AD, CD, BP, JY, and SF spot series end **April 30, 2003**, with 3,875 observations; corresponding futures series have 3,901 observations. Spot DM ends **December 31, 1998**, with 2,787 observations, while futures DM ends **December 14, 2001**, with 3,557. The spot/futures count difference reflects distinct trading calendars.

For interest differentials the source uses three-month LIBOR for the U.S. dollar and foreign currencies, except that the Canadian series uses a three-month Treasury-bill rate. This is a real instrument mismatch: it should not be silently replaced with Canadian LIBOR if reproducing the original experiment. The differentials are matched to currency sample endpoints and centered at zero for the tests.

Spot and futures quotations should not be assumed to have the same orientation merely because both are called returns. A positive change in a foreign-currency-per-dollar spot quote means dollar appreciation, while a conventionally reciprocal futures quote means foreign-currency appreciation. The article does not give a complete futures series-code or reciprocal-conversion specification. Keep “positive price change” distinct from “foreign currency appreciation” until each quote convention is verified.

The source also does not specify the continuous-futures construction, roll dates, back-adjustment, stale-price handling, full holiday joins, exact interest-rate timestamp, or complete rate-unit conversion. Those choices can create artificial threshold crossings or look-ahead information. Its return measure excludes interest carry and is explicitly a price-change measure, not a complete funded investment return.

Selected Table I diagnostics provide useful checks:

| Series | Return SD, percentage points | Kurtosis | First-lag return correlation | First-lag squared-return correlation |
|---|---:|---:|---:|---:|
| AD spot | 0.612 | 8.487 | 0.012 | 0.209 |
| CD spot | 0.310 | 5.278 | 0.036 | 0.128 |
| BP spot | 0.591 | 5.597 | 0.060 | 0.142 |
| JY spot | 0.708 | 7.084 | 0.035 | 0.209 |
| SF spot | 0.721 | 4.499 | 0.027 | 0.123 |
| DM spot | 0.668 | 4.778 | 0.037 | 0.152 |
| JY futures | 0.758 | 10.451 | −0.010 | 0.100 |

Sample means are close to zero. The near-unit first-order correlations of the interest differentials, approximately 0.999–1.000, contrast with these weak return correlations. The table's interest-rate means and standard deviations use a scale that should be checked against its percentage label and source rate conversion before direct numerical replication.

## Individual-currency results: keep zero thresholds separate

Table II reports own-return-based tests. Representative omnibus values are:

| Target series and sign | $a=0$ | $a=0.5$ | $a=1$ |
|---|---:|---:|---:|
| AD positive | 4.93 | 10.84 | 15.48 |
| AD negative | 4.96 | 9.73 | 16.52 |
| CD negative | 1.22 | 8.23 | 17.56 |
| BP positive | −0.38 | 6.37 | 13.97 |
| BP negative | −0.10 | 17.47 | 22.68 |
| JY positive | 0.26 | 3.05 | 7.23 |
| DM negative | −0.04 | 1.64 | 8.41 |
| DM futures positive | 4.03 | 0.18 | 1.29 |

This is broad large-event dependence, not universal ordinary sign predictability. BP and JY spot fail the zero-threshold test in both directions, as does DM spot; several futures cases also fail. The DM futures positive-event sequence is a counterexample to monotonic improvement as the threshold rises. Stronger rejection at larger thresholds is a common pattern with exceptions, not a theorem or a statement about classifier accuracy.

The squared-return derivative results illustrate the volatility mechanism. For BP negative events, $M_{ZY}(1,2)$ rises from **0.92** at zero threshold to **27.60** at half a standard deviation and **46.19** at one standard deviation. For JY negative events, the sequence is **−1.34, 7.87, 26.11**. For CD negative events it is **−0.54, 9.78, 30.76**. These contrasts show why an event-risk model may benefit from lagged volatility even when ordinary directional timing remains weak.

Raw-cubic and raw-fourth-power tests sometimes reject strongly, especially for large spot movements, but not uniformly. For example, BP negative one-standard-deviation events have fourth-power statistic **24.22**, whereas many futures fourth-power results are much smaller. The direction-only test for BP negative events is **−1.03, 8.08, 22.66** across thresholds. None of these squared-statistic results alone says whether a positive lagged event predicts continuation or reversal.

Table III uses interest differentials. BP positive-event omnibus values are **1.29, 24.69, 32.28**, and its corresponding first-power tests are **1.55, 25.46, 26.40**. This close pattern supports the relevance of the differential's level. JY spot negative-event omnibus values are **0.08, −0.75, 0.23**, giving a clear exception. Canadian-dollar futures negative-event values are **19.04, 7.80, 5.73**, declining rather than rising with threshold. Again, the detailed evidence is heterogeneous.

The article interprets level, volatility, and higher-power rejections as guidance for model construction. It expressly notes that these results do not guarantee a simple polynomial model will forecast well out of sample. A forecast model still needs regularization, probability calibration, and honest validation, none of which are specified or evaluated in this paper.

## Joint-event results and their exceptions

There are fifteen unordered currency pairs. The published joint tables display **negative spot joint events**; analogous positive and futures results are described qualitatively and said to be available from the authors. They are not fully tabulated in the supplied PDF, so their exact values cannot be reconstructed from its prose.

In Table IV, using joint lagged returns, AD–CD omnibus statistics are **0.87, 1.96, 4.69** across thresholds; BP–DM values are **1.01, 4.77, 12.39**; SF–DM values are **0.26, 1.05, 3.92**. These are examples of stronger large-event evidence despite weak ordinary joint-sign dependence. BP–DM's mixed first-power statistics are **0.48, 18.11, 25.82**; recall that this derivative concerns the product of the two lagged returns.

The separate-component tests add useful detail. For BP–DM joint negative events at one standard deviation, the squared-return statistics are **21.84** using BP history and **15.31** using DM history. Both individual risk histories carry information about the joint event. That does not establish that a changing correlation, rather than changing marginal event probabilities, is the sole source of joint predictability.

Table V uses interest differentials. BP–SF joint omnibus values are **15.49, 35.82, 30.07**; BP–DM values are **13.84, 36.36, 31.56**. Strong dependence is visible in these pairs. In contrast, AD–CD values are **6.61, 1.63, 0.30**, while JY–DM values are **1.61, 0.40, −0.41**. Large-event predictability from rates is therefore not universal and can be weaker than ordinary-event dependence.

These exceptions matter for diversification applications. One cannot use the paper's broad conclusion to assume every pair has a reliably forecastable crash probability. Nor are one-standard-deviation events equivalent to rare catastrophic crashes; the thresholds were deliberately limited to retain statistical power.

## Reproduction workflow and what remains unavailable

A faithful implementation begins by rebuilding the spot, futures, and rate panels with original conventions, then matching Table I moments and counts. Compute upper and lower events at each full-sample threshold. For each predictor family and positive lag, calculate the characteristic-function covariance and its derivatives, apply Bartlett weights with the paper's pilot/data-driven bandwidth procedure, and evaluate the quadratic forms. Use the correct dependent-predictor centering and variance normalization from the methodological reference or original code before comparing the resulting $M$ statistics with the one-sided critical values.

Next, repeat all scalar tests for each individual currency and rate differential. Build each pair's joint event using currency-specific thresholds and an aligned calendar, then run both vector-predictor and separate-component tests. Report event counts as well as test values, particularly where rare joint events make normalization unstable. The paper does not publish every pair-specific event count or its full handling of such degeneracy; one Table V entry is explicitly N/A.

Exact replication remains limited by missing scalar normalization formulas, incompletely explicit joint normalization, bandwidth plug-in details, futures construction, predictor rescaling, and timing/calendar joins. These are not minor cosmetic choices: they affect the statistics. The note therefore provides a reproducible specification of the target events and dependence measures while identifying the additional material needed for exact published inference.

A new empirical extension should predeclare the test family, account for multiple comparisons, examine regime stability, and then train a probability model using only past information. Compare it with unconditional-event and volatility-only benchmarks, evaluate calibration and proper probability scores, and include carry, spreads, and trading costs if the goal is investment. Those steps are proposed follow-on work, not results reported by Chung and Hong.

The source's policy discussion also exceeds what association alone identifies. Dependence between rate differentials and later currency events does not establish that an interest-rate intervention causes a favorable currency movement; common shocks and policy reactions can generate the same association. The paper acknowledges that rejection is not sufficient for successful intervention. Its strongest defensible contribution is empirical evidence that threshold-event dynamics contain information beyond ordinary linear return predictability, together with a flexible diagnostic framework for locating that information.
