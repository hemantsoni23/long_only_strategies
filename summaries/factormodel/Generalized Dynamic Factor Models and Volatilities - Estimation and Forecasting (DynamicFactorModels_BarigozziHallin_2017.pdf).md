# Generalized Dynamic Factor Models and Volatilities: Estimation and Forecasting

Matteo Barigozzi and Marc Hallin, *Journal of Econometrics*, 2017, DOI: 10.1016/j.jeconom.2017.08.010. The library source is a 15-page article-in-press proof, with final volume and page numbers unfilled. Page references below refer to that PDF.

Source: [original PDF](../../Finance/DynamicFactorModels_BarigozziHallin_2017.pdf).

## Why this matters and what is new

A return can be idiosyncratic in a linear factor model while its volatility is driven by a market-wide shock. If a risk model puts time variation only into the variance of return factors, it can miss common changes in the magnitudes of stock-specific returns. Conversely, a direct factor analysis of volatility proxies can find common variance movements without explaining their relationship to return-common and return-specific risks.

This paper connects the two decompositions. It first separates a large return panel into common and idiosyncratic components and extracts their linear innovations. It then estimates a second dynamic factor model from the joint panel of logarithms of the two sets of squared innovations. Every stock consequently has four volatility-related components: common and idiosyncratic variation in the volatility of its common return, and common and idiosyncratic variation in the volatility of its idiosyncratic return.

The earlier Barigozzi–Hallin paper focused on recovering market volatility shocks. The contribution here is forecasting: a predictor obtained by forecasting the four log components and exponentiating, and another obtained by fitting GARCH dynamics to their exponentials. The exercise uses 90 S&P 100 constituents, daily data during 2000–2009, and rolling forecasts during the financial crisis and its aftermath. Many aggregate forecast losses improve substantially over univariate GARCH. The improvement is heterogeneous across horizons, stocks, sectors, and crisis phases.

The authors are unusually explicit about what is heuristic. Their primary factor theory is about orthogonality and best *linear* prediction. It does not imply all the conditional independence assumptions needed to interpret the final predictor as an exact conditional variance. That distinction is indispensable for implementation.

## First layer: common and idiosyncratic returns

Let $Y_{it}$ be a demeaned return, with cross-sectional index $i$ and time $t$. For every finite $n$, the vector process $Y_{n,t}$ is strictly stationary, has finite second moments, and has a spectral density matrix $\Sigma_{Y;n}(\theta)$. The generalized dynamic factor model is

$$
Y_{it}=X_{it}+Z_{it}
=\sum_{k=1}^{q}b_{ik}(L)u_{kt}+Z_{it}.
$$

The common shocks $u_t$ are orthonormal white noise. The filters $b_{ik}(L)$ are one-sided and square summable. Common shocks and idiosyncratic components are orthogonal at every lead and lag. The idiosyncratic panel may have cross-sectional and serial dependence, but its spectral eigenvalues remain bounded as the number of stocks increases. The number $q$ is minimal among representations satisfying these conditions.

Identification uses a spectral separation: the first $q$ eigenvalues of the return spectral density diverge with $n$, almost everywhere in frequency, while the $(q+1)$st stays bounded. This separates pervasive common variation from weak residual dependence. It does not identify economic labels or causal shocks, nor does a single dynamic shock imply that one contemporaneous static principal component captures all common return dynamics.

The paper adds a rational-spectrum condition to obtain a convenient one-sided representation. Partition the cross-section into blocks of $q+1$ stocks. There is a block-diagonal autoregressive filter $A_n(L)$ and a loading matrix $H_n$ such that

$$
[I_n-A_n(L)]Y_{n,t}=H_nu_t+\widetilde Z_{n,t},
\qquad \widetilde Z_{n,t}=[I_n-A_n(L)]Z_{n,t}.
$$

The filtered common part is now a static factor model. Its innovation is $e_{n,t}=H_nu_t$. The common return itself is recovered through the inverse stable filter. Low-dimensional block VARs avoid estimating a fully unrestricted $n$-dimensional autoregression.

For each filtered idiosyncratic series, fit a stable univariate AR:

$$
[1-c_i(L)]\widetilde Z_{it}=v_{it}.
$$

The $v_{it}$ are innovations relative to each series' own linear past, not necessarily relative to the entire residual panel. Weak cross-sectional dependence can still be useful for forecasting a particular stock. Replacing a multivariate residual predictor by individual ARs is an approximation justified pragmatically by limited dependence, not by exact independence.

This filtering distinction also matters in interpreting outputs: $v_{it}$ is an innovation of the *filtered* idiosyncratic series. It should not be mislabeled the raw $Z_{it}$ or a directly observed return innovation.

## Volatility definition and the second factor layer

Define the log-squared innovation proxies

$$
s_{it}=\log e_{it}^2,
\qquad w_{it}=\log v_{it}^2.
$$

Strict stationarity of returns is imposed because nonlinear transformations now enter the analysis. Additional assumptions require finite second moments and spectral densities for these log proxies. Finite variance of a return alone does not ensure every log-square moment needed here, and exact zero residuals make the logarithm undefined. The source does not report a numerical floor or zero-handling rule.

The paper distinguishes squared volatility from ordinary conditional variance. For the common component its definition is

$$
V^2_{X;it\mid t-1}
=E[e_{it}^2\mid X_{n,t-1},X_{n,t-2},\ldots].
$$

Because $e_{it}$ is a *linear* prediction error, its conditional mean need not be zero. This is the expected squared deviation from a linear predictor, not automatically the conditional variance around the true conditional mean. Conditioning on the common component's history also need not equal conditioning on the full return panel's history. For the idiosyncratic component, the analogous conditioning set is the own past of $\widetilde Z_i$.

After centering, the empirical specification is

$$
s_{it}-\mu_{s,i}=\chi_{s,it}+\xi_{s,it}
=d_{s,i}(L)\varepsilon_t+\xi_{s,it},
$$

$$
w_{it}-\mu_{w,i}=\chi_{w,it}+\xi_{w,it}
=d_{w,i}(L)\varepsilon_t+\xi_{w,it}.
$$

The same scalar volatility shock $\varepsilon_t$ drives both common components. This gives the multiplicative identities

$$
e_{it}^2=\exp(\mu_{s,i})\exp(\chi_{s,it})\exp(\xi_{s,it}),
$$

$$
v_{it}^2=\exp(\mu_{w,i})\exp(\chi_{w,it})\exp(\xi_{w,it}).
$$

These identities explain why simply fitting a volatility model to the sum of the two return innovations discards information.

One qualification to the source's compressed block argument is important. Finding one dynamic factor separately in $s$ and $w$ does not logically establish that they share the *same* factor: two blocks can each have one unrelated shock. The joint panel must also have the claimed one-factor structure, or equivalent common-space evidence must hold. The empirical method directly applies a rank-one decomposition to the combined $2n$ panel. A replication should test or explicitly impose that joint rank rather than infer it solely from the two marginal counts.

## The estimation algorithm

The empirical application sets the return and volatility factor counts to one, following the Hallin–Liška criterion. Consequently each block has two series. Section 2.2 provides the following sequence.

First estimate the return spectral density with a lag-window estimator,

$$
\widehat\Sigma_Y(\theta)=\frac1{2\pi}
\sum_{k=-(T-1)}^{T-1}K(k/B_T)e^{ik\theta}\widehat\Gamma_Y(k).
$$

For positive $k$, $\widehat\Gamma_Y(k)$ is the sample lag-$k$ cross-covariance. Set $\widehat\Gamma_Y(-k)=\widehat\Gamma_Y(k)'$ to maintain a Hermitian spectrum; the shorthand printed with $|k|$ must not be read as assigning identical nonsymmetric matrices at positive and negative lags.

At each frequency obtain the largest eigenvalue $\widehat\lambda_1(\theta)$ and corresponding unit eigenvector $\widehat p_1(\theta)$. The common spectrum estimate is

$$
\widehat\Sigma_X(\theta)=
\widehat\lambda_1(\theta)\widehat p_1(\theta)\widehat p_1(\theta)^*,
$$

and the residual spectrum is the total minus this component. Inverse Fourier transformation gives common-component autocovariances. From the two-by-two diagonal blocks of those autocovariances, estimate stable bivariate VAR filters using Yule–Walker equations and choose orders by BIC. It is the estimated common autocovariance structure that enters this step; fitting unrelated VARs to raw pairs without this construction is not the stated estimator.

Filter observed returns by the block-diagonal VAR operator. Project the resulting panel onto its leading static principal component to estimate $e_{n,t}$. Subtract that common innovation from the filtered panel to get $\widehat{\widetilde Z}_{n,t}$. Fit BIC-selected univariate ARs to these residual series and retain their innovations $\widehat v_{it}$.

The initial stock ordering affects pair formation. The source repeats the relevant block fitting and projection steps over 100 randomly generated cross-sectional permutations, restores the original stock order, and averages the estimates. Averaging reduces dependence on arbitrary pairings. A software implementation should save the permutations or random seed, align common-shock signs if it averages separately identified scalar shocks, and prefer averaging invariant common components when possible.

Next compute and center $\log\widehat e_{it}^2$ and $\log\widehat v_{it}^2$. Concatenate them into a $2n$-series panel. Repeat the spectral, block-VAR, and static-component steps on this joint panel, using a potentially different bandwidth $M_T$. Inverting the estimated block filters reconstructs $\widehat\chi_s$ and $\widehat\chi_w$; subtract them from the centered log proxies to obtain $\widehat\xi_s$ and $\widehat\xi_w$.

These steps define the procedure, but the paper does not list the numerical kernel, the two bandwidth choices, frequency grid, maximum candidate VAR/AR orders, stability repair, or all endpoint and inverse-filter truncation conventions. The second bandwidth must also account for first-stage estimation. Section 2.2 explicitly says a formal consistency proof and rates for this *generated-proxy* two-step estimator remained work in progress. Consistency of the underlying GDFM estimator for directly observed data is not a completed proof for the full procedure here.

## Forecasting route one: predict logarithms and exponentiate

For the common log components, the one-step linear predictor drops the unobserved new volatility shock. If $\chi_{s,it}=\sum_{j\ge0}d_{s,i,j}\varepsilon_{t-j}$, then

$$
\widehat\chi_{s,i,t+1\mid t}
=\sum_{k=0}^{k^*}\widehat d_{s,i,k+1}\widehat\varepsilon_{t-k}.
$$

Use the analogous expression for $w$. The empirical truncations are $k^*=h^*=20$. Predict the idiosyncratic log components with their own BIC-selected ARs. The paper also considers heterogeneous autoregressive specifications to capture long-memory-like persistence; the reported tables use HAR-based predictions, with AR results described as similar. Exact HAR lag aggregation and estimation conventions are not written out in this source and should not be silently assumed from the model name.

Restore the estimated log mean and exponentiate:

$$
\widehat e^2_{i,t+1\mid t}
=\exp(\widehat\mu_{s,i}+\widehat\chi_{s,i,t+1\mid t}
+\widehat\xi_{s,i,t+1\mid t}),
$$

with an analogous $\widehat v^2$. The combined forecast, denoted $\mathcal E_Y$ in the paper, is their sum.

Exponentiating a best linear predictor of a logarithm does not produce a best mean predictor on the original scale. If a log forecast error were conditionally Gaussian with variance $\sigma_t^2$, for example, the conditional mean would have an additional $\exp(\sigma_t^2/2)$ multiplier. The source's route-one formula does not include this Jensen correction or a nonparametric smearing estimate. A corrected mean forecast would therefore be a modification, not an exact reproduction.

Likewise, unconditional orthogonality of $e$ and $v$ does not force their conditional cross-product expectation to vanish. Adding their forecasts is an intuitive recombination rather than a theorem giving the full conditional return variance. At horizons above one, a return forecast-error variance would normally account for propagation through return filters; the reported target is the horizon-$h$ daily volatility proxy, not variance of the cumulative $h$-day return.

## Forecasting route two: four component GARCH fits

For each stock the paper models the positive exponential components through four conditional-variance-like recursions. For example,

$$
\exp(\chi_{s,it})=\omega_{s,it}\nu_{s,it}^2,
\qquad
\exp(\xi_{s,it})=h_{s,it}\epsilon_{s,it}^2.
$$

A GARCH(1,1) version is

$$
\omega_{s,it}=\gamma_{s,i}
+\alpha_{s,i}\exp(\chi_{s,i,t-1})
+\beta_{s,i}\omega_{s,i,t-1},
$$

$$
h_{s,it}=c_{s,i}
+a_{s,i}\exp(\xi_{s,i,t-1})
+b_{s,i}h_{s,i,t-1}.
$$

Two analogous recursions apply to $w$. The paper allows higher orders and uses BIC, which mostly selects (1,1). Estimation is Gaussian quasi-maximum likelihood. Computationally, a positive component $a_t$ can enter the familiar variance objective $\sum_t[\log h_t+a_t/h_t]$, equivalent to using a pseudo-return whose square is $a_t$. A symmetric GARCH likelihood needs no sign information. Extending it to a leverage model would require signs, for which the original common or idiosyncratic return innovations are available.

The proposed forecast recombination is

$$
\widehat V^2_{Y;i,t+h\mid t}
=\widehat\omega_{s,i,t+h\mid t}\widehat h_{s,i,t+h\mid t}
\exp(\widehat\mu_{s,i})
+\widehat\omega_{w,i,t+h\mid t}\widehat h_{w,i,t+h\mid t}
\exp(\widehat\mu_{w,i}).
$$

For a GARCH(1,1) component, one first evaluates the one-step recursion using observed component values, then iterates expected future squared inputs and conditional scales for longer horizons. The paper describes multistep generalization rather than providing every recursive indexing convention.

The product formula has an exact conditional-mean interpretation only under additional assumptions. The authors display an Assumption C with standardized innovation sequences that are independent and identically distributed and independent across the relevant component pairs. Without the needed independence,

$$
E[\nu_{s,it}^2\epsilon_{s,it}^2\mid\mathcal I_{t-1}]
$$

does not generally equal one, so a product of conditional scales is insufficient. The authors explicitly decline to impose these restrictive conditions as a realistic description of the data and treat the forecasts empirically. Thus a report of good loss performance should not be converted into a claim that the model nonparametrically identifies every conditional variance.

A third reported predictor uses $\widehat\omega_s+\widehat\omega_w$, called market squared volatility. This drops the stock-specific scale factors and log-mean restoration present in the total predictor. It is an empirical restricted predictor in the table's convention, not algebraically the entire market-driven contribution to original-return variance under an arbitrary normalization.

## Data, information timing, and comparison design

The data consist of daily adjusted closing-price log returns from Yahoo Finance, January 26, 2000–December 9, 2009, giving 2,500 trading observations. Stocks without a full observation period are excluded, leaving 90 series. Appendix Table 7 names every retained ticker. This is a complete-history constituent sample, not a dynamically investable historical universe; the paper does not resolve the index-membership vintage or survivor-selection consequences.

Each forecast uses a rolling estimation sample of 2,000 observations. The estimation and forecast procedure is repeated for the 500 days from December 14, 2007 through December 9, 2009. Forecast horizons are 1, 2, 5, and 10 trading days. Means, filters, component estimates, and GARCH fits should be computed using only the current estimation window. Exact treatment of the final few observations at longer horizons, and whether all tuning choices are reselected at every origin, is not fully documented.

The evaluation proxy is Parkinson's daily squared log range,

$$
\rho_{it}=\frac{[\log p^{\mathrm{high}}_{it}
-\log p^{\mathrm{low}}_{it}]^2}{4\log2}.
$$

Its units are squared log returns per day. It uses the intraday high and low, whereas the input returns are based on consecutive adjusted closes. Drift, jumps, overnight movements, price adjustments, and microstructure can make the proxy differ from the desired close-to-close conditional variance. The paper invokes literature on range efficiency and forecast ranking with imperfect proxies; that does not make this range universally conditionally unbiased under every data-generating process.

The baseline is a separate AR-GARCH on each raw return series. Competitors also include a multivariate vech-GARCH fitted by composite likelihood and static factor GARCH with either one or three factors. Static principal components are extracted first, then AR-GARCH models are fitted to factors and idiosyncratic components. Bai–Ng and Alessi criteria select three static factors; the one-factor variant is also tested because extra estimated factors may increase second-stage error. These three static factors should not be confused with the one dynamic factor in the proposed model.

For each stock and horizon, compute the root mean squared difference between its daily target-date proxy and the forecast made $h$ trading days earlier. Divide that stock's RMSE by its univariate-GARCH RMSE, then average ratios across stocks or a sector. This is not a ratio of pooled RMSEs. The proof's displayed loss formula has inconsistent forecast-origin indexing and omits $h=10$ from one list; a reimplementation must use a coherent target/origin convention and match all four table horizons. Table 5 is a ten-period table despite a copied five-period caption.

## Results, heterogeneity, and uncertainty

Table 1 reports mean GARCH persistence and cross-sectional dispersion for the four positive components. The return-common/volatility-common component has mean persistence 0.994, cross-sectional standard deviation 0.001. The return-common/volatility-idiosyncratic component has 0.912 (0.038). The return-idiosyncratic/volatility-common component has only 0.608 (0.410), whereas the component idiosyncratic at both levels has 0.969 (0.118). These parenthesized quantities describe variation across stocks, not standard errors of average persistence.

The lower and much more heterogeneous persistence of the common volatility component within idiosyncratic returns illustrates the benefit of separating the four processes. A single persistence parameter on an aggregate volatility series would hide these differences. It is not evidence that every stock has exactly the cross-sectional mean dynamics.

The all-stock mean relative RMSEs for the full 2007–2009 evaluation period are:

| Forecast | 1 day | 2 days | 5 days | 10 days |
|---|---:|---:|---:|---:|
| Log-component/HAR route, $\mathcal E_Y$ | 0.745 | 0.616 | 0.908 | 0.801 |
| Four-component GARCH total, $V_Y^2$ | 0.670 | 0.582 | 0.828 | 0.762 |
| Restricted market predictor | 0.651 | 0.583 | 0.782 | 0.739 |
| Static factor GARCH, one factor | 0.964 | 0.974 | 0.979 | 0.954 |
| Static factor GARCH, three factors | 0.963 | 0.972 | 0.978 | 0.947 |
| Composite-likelihood vech-GARCH | 0.778 | 0.671 | 0.914 | 0.819 |

Thus the four-component total forecast's one-day value 0.670 corresponds to an average stock-level RMSE ratio 33.0% below the baseline. It does not mean variance is lower by 33%, that every stock improves, or that a portfolio earns a higher Sharpe ratio.

Tables 2–5 split the period at December 11, 2008. At five days during the first, crisis-heavy segment, the log route has relative RMSE 1.084 and the total GARCH route 1.010; both are worse than the univariate baseline on this average measure. The one-factor static competitor is 1.005. In the later segment the same three values are 0.516, 0.647, and 1.001. This is a strong regime contrast. During abrupt highly collinear market movements, a simple static factor can be competitive; during quieter periods, separating idiosyncratic dynamics appears more useful.

Sector results likewise vary. In the full period at one day, the total predictor has a ratio of 0.390 for industrials, 0.599 for energy, and 0.703 for financials, but 0.950 for information technology and 0.911 for consumer staples. In the first segment, information technology and staples have ratios above one, 1.130 and 1.115. Claims of universal dominance would therefore misrepresent the tables.

Table 6 and Figures 2–3 give individual examples. At one day, the total predictor's ratio is 0.313 for JPMorgan, 0.508 for Bank of America, 0.285 for Dell, and 0.853 for IBM. At five days, Morgan Stanley has 1.056, showing an individual failure even when the full-panel average improves. Figure 1 uses rolling 20-day windows and cross-sectional medians and quartiles; these are descriptive performance distributions, not confidence bands for a population treatment effect.

The article does not report a full set of formal pairwise loss-difference tests, standard errors for the displayed mean ratios, or correction for selecting among models and horizons. Its verbal use of significant improvement should therefore be read alongside the actual descriptive evidence rather than as a supplied inferential rejection for every comparison.

## Reimplementation priorities and limits

A faithful implementation should preserve the sequence: return spectrum, common autocovariances, low-dimensional block filters, common innovations, idiosyncratic AR innovations, joint log-volatility spectrum, four components, and forecast recombination. Direct PCA on squared returns or GARCH on return factors alone is a different model.

The unresolved inputs that most affect numerical matching are the two spectral kernels and bandwidths, Fourier grid, VAR/AR candidate orders, treatment of near-zero innovations, 100 permutation draws, component centering within rolling windows, HAR construction, GARCH initialization and constraints, optimizer failure handling, and exact multi-horizon evaluation alignment. Original code or documented choices would be needed for exact table replication. A transparent reconstruction can choose and report these, but should label them as choices.

The method supplies marginal volatility predictors, not a validated full portfolio covariance matrix, tail distribution, or value-at-risk model. The paper lists portfolio optimization and conditional prediction intervals as extensions. Its lasting insight is the usefulness of a second common-factor structure in nonlinear transformations of return innovations. Its practical evidence supports investigating that structure while retaining the mathematical distinction between linear orthogonality, nonlinear dependence, conditional mean prediction, and empirical proxy forecasting.
