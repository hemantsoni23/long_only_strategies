# Beyond Value at Risk: Forecasting Portfolio Loss at Multiple Horizons

**Authors:** Lisa R. Goldberg, Guy Miller, and Jared Weinstein. **Version:** October 11, 2007 working paper, 34 pages, SSRN identifier 1023441. **Source:** [BeyondVaR_GoldbergMillerWeinstein_2007.pdf](../../Finance/BeyondVaR_GoldbergMillerWeinstein_2007.pdf). Page numbers below refer to the PDF, whose printed numbering coincides. The complete source, both appendices, and critical equations and empirical charts were inspected.

## Why this matters and the actual contribution

A one-day volatility forecast does not determine a ten-day loss distribution when returns are asymmetric, heavy-tailed, serially correlated, or conditionally heteroscedastic. This paper constructs a loss surface: a collection of predictive loss distributions indexed by horizon. Its central mechanism is to estimate an empirical-core/generalized-Pareto-tail distribution of standardized daily innovations, express a multiperiod loss as a weighted sum of those innovations, and aggregate by multiplying characteristic functions. Quantiles and tail expectations can then be extracted from the same forecast distribution.

The distinctive implementation choices are an automated tail-threshold rule based on Kuiper goodness of fit, an autoregressive filter combined with a quickly updating absolute-residual scale, and Fourier aggregation of the filtered innovations. A factor-based extension creates synthetic history for portfolios without sufficiently long observed returns. The empirical contribution compares the resulting forecasts with three Gaussian covariance-based benchmarks for 76 US equity portfolios and several horizons.

Two qualifications are essential before reproducing the method. First, the quantity the authors call expected shortfall is the expected *excess above* VaR. It is not the standard coherent expected shortfall, which is the total expected loss in the tail. Second, their “ES” test uses probability-transformed exceedances, so it tests a feature of tail-distribution calibration rather than directly testing the numerical mean loss beyond the quantile. The results must be interpreted with those definitions intact.

## Loss units, horizons, and tail measures

For a positive-value portfolio, the loss over $T$ trading days beginning at $t$ is

$$
L_t^T=-\log(P_{t+T}/P_t).
$$

For leveraged, long–short, and option portfolios for which log portfolio value may be unsuitable, the proposed alternative is monetary loss $L_t^T=P_t-P_{t+T}$. Both definitions telescope over successive periods when the portfolio-value process and cash-flow convention are consistently defined. They are different units and should not be combined in one calculation. Realized portfolio returns with rebalancing or external flows require a consistent self-financing value series; the paper does not fully specify that accounting.

The loss surface at forecast time $t$ is $\{F_t^T:T>0\}$, where each $F_t^T$ is a predictive CDF of $L_t^T$. Its $p$-quantile is $v_{p,t}^T=(F_t^T)^{-1}(p)$. For continuous distributions, the paper's Eq. (4) defines

$$
e_{p,t}^T=E[L_t^T-v_{p,t}^T\mid L_t^T>v_{p,t}^T].
$$

This note denotes it $e_p$ to distinguish it from conventional expected shortfall $ES_p^{\rm total}=v_p+e_p$. If the CDF has atoms, a coherent quantile-integral definition requires fractional allocation at the boundary. The authors interpolate their empirical CDF to a continuous distribution for testing, but do not give a complete interpolation algorithm.

For a centered normal loss with standard deviation $s$, write $z_p=\Phi^{-1}(p)$ and standard normal density $\varphi$. Then

$$
v_p=sz_p,\qquad e_p=s\left[\frac{\varphi(z_p)}{1-p}-z_p\right],
\qquad ES_p^{\rm total}=s\frac{\varphi(z_p)}{1-p}.
$$

The normal CDF on source page 5 has its lower integration endpoint printed as positive infinity; it must be negative infinity. For exponential losses with rate $\lambda$, $v_p=-\log(1-p)/\lambda$ and $e_p=1/\lambda$. For an exact unit-scale Pareto survival $P(L>x)=x^{-\alpha}$ on its support, $v_p=(1-p)^{-1/\alpha}$ and $e_p=v_p/(\alpha-1)$ for $\alpha>1$; the mean excess diverges for $\alpha\leq1$. A merely asymptotic Pareto tail gives corresponding asymptotic formulas, including its scale constant, not an exact unit-scale identity.

These examples explain Figure 1. Normal mean excess shrinks at increasingly extreme quantiles, exponential mean excess is constant, and Pareto mean excess grows. Conventional total ES does not shrink to zero in the normal case. Reading the figure as a statement about standard ES would invert its meaning. Mean excess is also invariant under deterministic translation of losses, so it does not share the cash-translation property of a coherent monetary risk measure.

## Daily filtering and the information set

The source's daily model is

$$
L_t=\kappa L_{t-1}+\delta_t,\qquad
\epsilon_t=\delta_t/s_t.
$$

Innovations $\epsilon_t$ are assumed iid after removing first-order serial dependence and scale variation. There is no intercept in the displayed autoregression. The paper does not specify the estimator for $\kappa$, its fit window, stationarity restriction, refitting schedule, or handling of a nonzero sample mean. An implementation could use a no-intercept least-squares fit, but that is a disclosed reconstruction choice rather than a reported setting.

The scale recursion is unusual and must be copied accurately:

$$
\widehat s_t=0.94\widehat s_{t-1}+0.06|\delta_{t-1}|,
\qquad\widehat s_1=|\delta_1|.
$$

It smooths absolute residuals, not squared residuals and not variance. The half-life is $\log(1/2)/\log(0.94)\approx11.2$ trading days. Although the text calls $s_t$ volatility, the displayed estimator is an absolute-deviation scale. Under Gaussian residuals it is not automatically their standard deviation. Because the empirical innovation distribution is estimated after dividing by this same scale and later multiplied back, consistent scaling can still define a valid location-scale model; one must not additionally force innovations to unit variance without adjusting the reconstruction.

The recursion at forecast origin $t$ uses $\delta_{t-1}$, which is known. The initialized first value uses $\delta_1$, so early initialization and burn-in need explicit treatment before out-of-sample testing. Zero scales require a stated fallback; none is supplied. The paper's introductory description says history is collected through day $t$, but its notation defines $L_t$ as the loss starting at $t$. A no-look-ahead implementation uses only completed losses through $t-1$ when forecasting $L_t$. The source does not settle all calendar conventions.

Filtering does not establish independence by definition. Residual autocorrelation, volatility clustering, and tail dependence should be checked after fitting. The paper displays S&P 500 raw losses and innovations for 1980–2005 but supplies no formal residual-independence diagnostic. Higher-order dynamics and adaptive half-lives are explicitly left for future development.

## Estimating the innovation distribution

Each tail is fitted separately using peaks over thresholds. For a right-tail threshold $u$, let $y_j=\epsilon_j-u>0$ be the $n_u$ exceedances. The generalized Pareto CDF in the paper's reciprocal-shape parameterization is

$$
G_{\alpha,\beta}(y)=1-\left(1+\frac{y}{\alpha\beta}\right)^{-\alpha},
\qquad\beta>0,
$$

with support $y\geq0$ and $1+y/(\alpha\beta)>0$. The usual shape is $\xi=1/\alpha$. Positive $\xi$ gives a heavy unbounded tail, negative $\xi$ gives a finite endpoint, and $\xi=0$ gives $G(y)=1-e^{-y/\beta}$. Thus negative $\alpha$ is permitted; $\alpha=0$ is not. The exponential limit corresponds to infinite $\alpha$.

For finite $\alpha$, the log likelihood derived from this CDF is

$$
\ell(\alpha,\beta)
=-n_u\log\beta-(\alpha+1)\sum_{j=1}^{n_u}
\log\left(1+\frac{y_j}{\alpha\beta}\right).
$$

The authors use maximum likelihood. The displayed likelihood here makes the optimization reconstructible, but their solver, starting values, parameter bounds, convergence rule, and small-sample failure treatment are unreported. Endpoint constraints must be imposed for every observation. Fitted heavy tails with $\alpha\leq1$ do not have finite mean excess; a numerical grid that truncates the tail can conceal that fact.

For the full right-tail CDF, an explicit splice consistent with the described method is

$$
\widehat F(x)=1-\frac{n_u}{n}\left[1-G_{\widehat\alpha,\widehat\beta}(x-u)\right],
\qquad x\geq u.
$$

The factor $n_u/n$ preserves the estimated probability assigned to the tail; fitting a conditional excess law without this factor is insufficient. Fit the gain tail by applying the same procedure to $-\epsilon_t$, and retain the empirical distribution in the central region. Ties at the threshold and interpolation through the empirical core need an implementation convention. The paper states the construction but does not report all such details.

The automated threshold rule uses the Kuiper statistic, the sum of the largest positive and negative discrepancies between empirical and fitted CDFs. Let $K_n$ be its null CDF. Candidate thresholds are chosen to leave 25, 50, 75, and successive multiples of 25 exceedances. The selected threshold is the smallest candidate $u$ for which

$$
K_{n_u}\big(D^+_u+D^-_u\big)<0.95.
$$

Equivalently, choose the most inclusive candidate tail whose fit is not rejected at a nominal 5% level. This is not minimization of out-of-sample forecast error. The ordering of candidates matters because the fit can improve and deteriorate as the threshold changes. Rules when no candidate passes, or when both tails' accepted regions would overlap, are not supplied.

The source says the Kuiper reference distribution is distribution-free and can be simulated once for each sample size. That statement applies to a fully specified continuous null. Here Pareto parameters are fitted on the same observations, and the threshold is also selected. Their fitted-parameter and selection effects are not automatically covered by that reference law. A parametric bootstrap that refits within each simulation would be a possible modification, not a setting reported in the paper. Its nominal p-values should therefore not be treated as fully calibrated confidence statements without further work.

The S&P 500 illustration reports an optimal threshold of 1.02%, $\widehat\alpha=9.55$, and $\widehat\beta=0.57$ using the 1980–2005 sample. These are source-reported display units. Since $\epsilon_t$ is dimensionless after dividing a return by a return scale, the percentage labeling of innovation plots is ambiguous. A reproduction must retain one consistent numerical scaling across $u$, $\beta$, innovations, and rescaling; it cannot blindly interpret every printed percent sign as an additional factor of 0.01.

Appendix A provides the extreme-value motivation, rather than a proof that any finite sample tail follows a Pareto law exactly. Its labels inadvertently interchange the Gumbel and Weibull cases: positive $\xi$ is Fréchet, zero $\xi$ Gumbel, and negative $\xi$ Weibull. A uniform distribution has a finite-endpoint Weibull domain, not the Gumbel domain claimed in the text. The appendix also writes an excess survival probability where its theorem requires an excess CDF. These notation errors do not change the intended generalized-Pareto fitting algorithm when the explicit CDF above is used.

## Temporal aggregation by characteristic functions

Iterating the AR(1) and summing daily losses gives the exact identity

$$
L_t^T=a_TL_{t-1}+
\sum_{i=0}^{T-1}b_{T-i}s_{t+i}\epsilon_{t+i},
\quad
b_l=\frac{1-\kappa^l}{1-\kappa},
\quad a_T=\frac{\kappa-\kappa^{T+1}}{1-\kappa}.
$$

The crucial approximation is to freeze future scale at its current forecast: $s_{t+i}=s_t$ throughout the horizon. Then

$$
L_t^T=a_TL_{t-1}+s_t\Delta_t^T,
\qquad\Delta_t^T=\sum_{i=0}^{T-1}b_{T-i}\epsilon_{t+i}.
$$

If $\phi_\epsilon(v)=E[e^{iv\epsilon}]$, independence implies

$$
\phi_\Delta(v)=\prod_{l=1}^T\phi_\epsilon(b_lv),
\qquad
\phi_{L_t^T}(v)=e^{iva_TL_{t-1}}\prod_{l=1}^T\phi_\epsilon(s_tb_lv).
$$

This is Eq. (12), with the location and scale restoration made explicit. At $T=1$, $a_1=\kappa$ and $b_1=1$, recovering the daily model. At $\kappa=0$, the aggregate is an iid sum of scaled innovations. At $\kappa=1$, the displayed fractions are replaced by their limits $b_l=l$ and $a_T=T$; a stationarity constraint would ordinarily exclude this case but is not reported. Near one, stable geometric-sum evaluation avoids cancellation.

The inverse Fourier transform returns the aggregate density or CDF. With the stated characteristic-function convention, a density inversion uses $(2\pi)^{-1}\int e^{-ivx}\phi(v)dv$ when the relevant regularity holds. Appendix B's informal assertion that applying a Fourier transform again returns the distribution omits the inverse sign and normalization; numerical code must select a consistent pair. A mixed empirical-core/tail law may include atoms before interpolation, so density-only formulas require care.

No transform grid size, frequency spacing, loss-domain bounds, tail truncation, damping, interpolation, or aliasing controls are reported. These are not cosmetic choices for extreme quantiles and mean excess. A reproduction should verify total mass, CDF monotonicity, one-day reconstruction, and a Gaussian benchmark, and document convergence as the grid and tail domain expand. Such checks are requirements of a faithful numerical implementation, not empirical tests already performed in the source.

The aggregation is exact conditional on iid innovations and the frozen-scale approximation. It does not integrate over future volatility updates. If one instead applies the absolute-residual recursion recursively to simulated future shocks, later scales depend on earlier innovations and the simple characteristic-function product no longer describes that process. This distinction is particularly important at five- and ten-day horizons.

## Factor-based synthetic history

When direct history is insufficient, the authors use a linear factor model. In asset-vector notation, losses are $l_t=X\Lambda_t+e_t$, where $X$ contains exposures and $\Lambda_t$ factor losses. For portfolio weights $w$, the common component is $w'X\Lambda_t$ and the specific component is $w'e_t$. They fit the non-Gaussian loss-surface model to the common component and convolve it with an independent normal distribution for the specific component.

With diagonal specific covariance $S$, that added normal variance is $w'Sw$. Independence between common and specific losses and diversification of specific risk are assumptions. A concentrated portfolio with asymmetric or dependent residuals may violate them. The paper does not report how point-in-time exposures are held fixed or changed when constructing synthetic history, nor the full horizon treatment of specific covariance. Applying today's exposures to an old factor history is conceptually possible, but exact exposure dating must be disclosed rather than inferred.

The S&P 500 comparison labels direct-history forecasts EVT and synthetic-history forecasts FactorEVT. Section 6 reports data from January 2, 1981 through December 20, 2005, with an out-of-sample period beginning January 3, 2001. The earlier illustrative plots instead begin in January 1980. These are distinct source descriptions and should not be silently merged. The text initially lists one-, two-, five-, and ten-day horizons, while Figure 9 and its discussion include intermediate horizons. It reports similar performance, slightly favoring FactorEVT, with exceptions including one-day 95% VaR for both models and five-, six-, and nine-day mean-excess diagnostics for direct EVT. Exact plotted z-scores are not tabulated.

## Broad test portfolios, timing, and benchmarks

The broad experiment uses roughly 1,800 liquid stocks from the Barra US Equity Model estimation universe. It forms 52 capitalization-weighted industry portfolios and 24 capitalization-weighted style portfolios. Each style portfolio contains the top or bottom decile of exposure to one of 12 styles: growth, yield, earnings yield, value, earnings variation, volatility, leverage, momentum, currency sensitivity, trading activity, size, and size nonlinearity. Constituents change monthly; weights rebalance daily. Annualized style turnover is reported as approximately 100%–200%, lower for industry portfolios. Transaction costs are not deducted in this risk-forecast comparison.

The overall history runs January 3, 2000 through January 31, 2007. For one-day 95% forecasts, the final 250 days beginning January 4, 2006 form the test period. For 99% forecasts and horizons longer than one day, the final 750 days beginning February 9, 2004 are used. Five- and ten-day 99% results are not evaluated because the sample has too few extreme observations. Exact return-adjustment rules, inclusion of delisted stocks, exposure-availability lags, and the historical portfolio construction before each forecast origin are not fully documented.

The three alternatives are centered conditional Gaussian models, with quantiles and mean excess calculated from the normal formulas and multiperiod risk scaled by square root of time:

| Model | Covariance construction and update |
|---|---|
| RM | Asset covariance estimated from daily data with a 23-day half-life; portfolio variance $w'\Sigma w$. |
| FactorD | Daily factor covariance update, with variances and covariances using a 23-day half-life. |
| FactorM | Monthly factor covariance update; factor variances use a 90-day half-life and correlations a 480-day half-life. |

Both factor alternatives use 64 industry/style factors and variance $w'(XFX'+S)w$. Specific variances in $S$ come from daily data but update monthly. Thus differences between EVT and the benchmarks combine distributional assumptions, update speed, scale methodology, and serial-dependence treatment. They are not a controlled experiment that changes only the tail law. A half-life $h$ corresponds to decay $2^{-1/h}$; this conversion is useful for implementation, but EWMA initialization and finite-history normalization remain unreported.

## What the statistical tests actually test

Let $I_t=\mathbf1\{\ell_t>v_{p,t}\}$ and $N_p=\sum_tI_t$. The VaR diagnostic is

$$
Z_{\rm VaR}=\frac{N_p-N(1-p)}{\sqrt{Np(1-p)}}.
$$

The source's prose mistakenly says the indicator mean is $p$; its equations correctly use $1-p$. Under independent calibrated breaches, the statistic is approximately standard normal, and the paper flags values outside $[-2,2]$. Positive values indicate underforecasting and negative values overforecasting. The approximation is weak with very few expected breaches. Estimation uncertainty and multiple comparisons across related portfolios are not incorporated into the reported rejection counts.

For the tail diagnostic, transform realized losses using the entire predicted CDF: $u_t=F_t(\ell_t)$. Under correct continuous conditional distributions and suitable independence, the PITs are uniform. Conditional on $u_t>p$, they have mean $(1+p)/2$ and standard deviation $(1-p)/\sqrt{12}$. The paper calculates

$$
Z_{\rm tail}=\frac1{\sqrt{N_p}}\sum_{u_t>p}
\frac{u_t-(1+p)/2}{(1-p)/\sqrt{12}}.
$$

This statistic assesses the average location of realized tail PITs. It is not a direct test of $E[L-v_p\mid L>v_p]$, and equality of this transformed mean does not uniquely identify a correct monetary tail expectation. It can also fail to reject some misspecified tail distributions. Calling it an ES diagnostic is the authors' terminology; interpreting it as a validated test of standard ES would be misleading. If $N_p=0$, it is undefined.

For multiperiod forecasts, overlapping realized losses invalidate a naive independent-observation denominator. The paper does not clearly state the sampling stride or dependence adjustment. Its ten-day discussion is consistent with roughly 75 nonoverlapping test observations: zero breaches then gives $Z\approx-1.99$ at 95%, just inside its acceptance interval. With 750 independent observations it would instead give about minus 6.28. This calculation is an inference identifying a missing protocol detail, not proof of the exact schedule used by the authors.

## Empirical results with the chart counts made explicit

The following counts are read from the rendered bar charts. Entries are total flagged portfolios, with overforecast/underforecast counts in parentheses. All tests cover 76 portfolios unless the zero-exceedance issue below applies.

| Horizon and diagnostic | FactorM | FactorD | RM | EVT |
|---|---:|---:|---:|---:|
| 1 day, 95% VaR, Figure 12 | 13 (10/3) | 8 (8/0) | 2 (2/0) | 4 (4/0) |
| 1 day, 95% tail PIT, Figure 14 | 13 (0/13) | 7 (0/7) | 8 (0/8) | 1 (0/1) |
| 1 day, 99% VaR, Figure 16 | 24 (10/14) | 13 (5/8) | 10 (0/10) | 10 (10/0) |
| 1 day, 99% tail PIT, Figure 18 | 11 (2/9) | 9 (0/9) | 11 (0/11) | 11 (5/6) |
| 5 days, 95% VaR, Figure 20 | 9 (8/1) | 5 (5/0) | 0 (0/0) | 1 (1/0) |
| 5 days, 95% tail PIT, Figure 22 | 4 (0/4) | 7 (0/7) | 4 (0/4) | 7 (3/4) |

EVT's clearest advantage is the one-day 95% tail diagnostic: one flagged portfolio versus seven to thirteen. It is less prone to underforecasting at one-day 99% VaR, but its ten flagged forecasts all err in the conservative direction, while RM's ten all err in the opposite direction. Equal rejection counts therefore do not mean economically identical behavior. At 99% tail PIT, EVT does not have fewer total flags than the alternatives; its advantage is chiefly the balance of signs relative to RM and FactorM. At five days it has no clear tail-diagnostic dominance.

No model has a flagged ten-day 95% VaR forecast under the source's test. That apparent success is weak evidence: 19 FactorM portfolios, seven FactorD portfolios, and five each for RM and EVT have no VaR exceedances, leaving no data for their tail diagnostic. Figure 24 therefore includes only 57, 69, 71, and 71 portfolios, respectively. Figure 25's totals are 19, 10, 8, and 8, but its caption calls the no-breach cases “underforecasts” while the chart places them with the blue overforecast group. Neither label turns an undefined tail test into a valid rejection. These totals should not be treated as comparable ordinary test failures.

The source calls forecasts inside the acceptance band unbiased. Failure to reject with a small sample is not proof of unbiasedness. Portfolio returns overlap cross-sectionally, so even the usual expectation of approximately 5% false flags under independent tests cannot be turned into a simple binomial comparison of models here. There are no reported confidence intervals for differences in rejection counts, and no realized capital or allocation utility comparison.

## Reproduction limits and the research implication

The paper makes the main distributional pipeline reconstructible: lagged AR filtering, absolute-residual scaling, separate Pareto tails with an empirical core, a specified candidate-threshold grid, and weighted characteristic-function aggregation under frozen scale. Exact reproduction still requires the raw Barra histories, point-in-time portfolio and exposure rules, AR estimation settings, expanding versus rolling distribution windows, refitting frequency, Kuiper calibration, CDF interpolation, transform discretization, and multiperiod test sampling. None should be invented or described as an author setting.

A useful reproduction would first recover the one-day forecast law and verify its units, then compare Fourier aggregation with independent draws from that same fitted law while holding scale fixed. A separate experiment could relax frozen scale or recalibrate the threshold test, but that would be a model extension. The supplied empirical evidence is strongest for reducing some short-horizon tail underforecasting in the studied equity sample. It does not validate general ten-day extreme-risk accuracy, derivative portfolios, an intraday implementation, or coherent expected-shortfall optimization. Those limits preserve the value of the contribution: a common forecast distribution makes its assumptions and its several risk measures explicit, while also making it possible to diagnose precisely where the empirical support is thin.
