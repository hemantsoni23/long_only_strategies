# Implied Expected Returns and the Choice of a Mean-Variance Efficient Portfolio Proxy

David Ardia and Kris Boudt. *The Journal of Portfolio Management*, Summer 2015, pp. 68–81. Source: [original PDF](../../Finance/Impliedalpha_ArdiaBoudt_2015.pdf), 14 scanned pages. All pages, equations, seven exhibits, and endnotes were read visually because the PDF contains no usable text layer. References below use the journal's printed page numbers.

## Why this matters and the paper's contribution

Reverse portfolio optimization turns a chosen reference portfolio into a vector of expected returns. The usual choice is the capitalization-weighted market, but that choice embeds an economic assumption: the reference portfolio is treated as mean-variance efficient. If an alternative allocation is a better efficient-portfolio proxy, its implied returns may be more useful inputs for subsequent portfolio construction.

Ardia and Boudt compare eight such proxies, including equal weighting, fundamental weighting, and four risk-based allocations. They evaluate the implied one-month stock-return forecasts against four time-series forecasting models. The central empirical result is that risk-based proxies make forecasts substantially less dispersed across stocks and more stable through time. Their accuracy advantage over market-capitalization-implied returns is small; their improvement over the selected time-series forecasts is larger.

This distinction is the paper's contribution. It does not demonstrate that a risk-based allocation recovers objectively true expected returns, nor does it provide a full after-cost backtest of a second optimizer using the forecasts. Lower instability is potentially valuable for turnover and robustness, but the resulting trading-cost saving remains an implication rather than a measured outcome in this article.

## Reverse optimization, including the intercept

There are $N$ risky assets with arithmetic expected-return vector $\mu$ and covariance $\Sigma$ over the intended holding horizon. For risk aversion $\gamma>0$, the fully invested mean-variance problem is

$$
\max_{w:\mathbf1'w=1}\left\{w'\mu-\frac{\gamma}{2}w'\Sigma w\right\}.
$$

The Lagrange multiplier $\ell$ on the budget constraint satisfies

$$
\mu-\gamma\Sigma w-\ell\mathbf1=0,
$$

which gives the reverse-optimization mapping

$$
\mu=\ell\mathbf1+\gamma\Sigma w.
$$

For known positive-definite $\Sigma$, fixed $\gamma$, and fixed $\ell$, this assigns expected returns to a proposed fully invested proxy $w$. Conversely $w=\gamma^{-1}\Sigma^{-1}(\mu-\ell\mathbf1)$ satisfies the first-order conditions. Strict concavity gives the unique optimum when covariance is positive definite.

The intercept is essential. A fully invested portfolio is unaffected by adding the same constant to every asset's expected return, so its holdings alone cannot identify the common expected-return level. Neither $\ell$ nor $\gamma$ is identified merely by observing $w$. The authors impose $\ell=r_f$, the risk-free rate, and use $\gamma=2.4$ in the baseline, with 1 and 5 in sensitivity analysis. These are normalization choices informed by the reverse-optimization tradition, not empirical estimates of investors' preferences in the sample.

All returns and covariances must share a horizon. With monthly arithmetic returns in decimal units, the input covariance is monthly arithmetic covariance and $r_f$ is a monthly return. Feeding weekly log covariance directly into this formula would change the implied premium's scale. The article explicitly transforms covariance before calculating expected returns.

For stock $i$,

$$
\mu_i-r_f=\gamma\operatorname{Cov}(r_i,r_p)
=\gamma\sigma_i\left(\sigma_iw_i+\sum_{j\ne i}\rho_{ij}\sigma_jw_j\right),
\qquad r_p=w'r.
$$

This shows how changing proxy weights propagates into expected returns. A stock's premium is not determined by its own portfolio weight alone; volatility and covariance with all other holdings also matter. For two proxies using the same covariance and normalizations,

$$
\Delta\mu=\gamma\Sigma\Delta w.
$$

This is a useful interpretation and implementation check: allocation differences are filtered through the risk model. Large allocation differences need not imply equally extreme return differences if they cancel in covariance space.

The first-order identity is familiar; the new question is which portfolio to insert into it and how the resulting forecasts behave out of sample. The study evaluates that question rather than estimating an unconstrained vector of means from historical averages.

## The eight efficient-portfolio proxies

The first proxy is current capitalization weighting, $w_{{\rm mkt},i}=MC_i/\sum_jMC_j$. It is efficient under the CAPM assumptions, but the authors argue that a restricted equity universe and realistic market frictions do not automatically satisfy those assumptions.

The smoothed capitalization proxy uses median capitalization weights over five weeks. The article describes the median operation but does not spell out its final normalization; componentwise medians need not sum to one, so a reproducible implementation must disclose the renormalization used to satisfy the stated full-investment condition.

The fundamental proxy averages four separately normalized measures of company size. Book equity uses the most recently observed fiscal-year value. Dividends, net operating cash flow, and sales use five-year trailing averages of annual observations. For fundamental variable $x_{ki}$,

$$
w_{{\rm fund},i}=\frac14\sum_{k=1}^4
\frac{\max(x_{ki},0)}{\sum_j\max(x_{kj},0)}.
$$

Negative observations are clipped at zero before normalization. Net operating cash flow is operating income before depreciation minus total accruals. Accounting information is lagged one quarter. The source does not fully specify treatment of missing fundamental histories or a metric whose clipped cross-sectional sum is zero; those choices must be documented in replication.

Equal weighting assigns $w_{{\rm ew},i}=1/N$. Its implied excess returns are proportional to each covariance row sum. It is not equivalent to assuming equal expected returns unless that row-sum structure happens to be constant.

Inverse-volatility weighting uses

$$
w_{{\rm iv},i}=\frac{1/\sigma_i}{\sum_j1/\sigma_j}.
$$

This equalizes individual volatility-scaled dollar allocations but generally does not equalize total risk contributions when correlations differ. Under special equal-correlation and equal-Sharpe-ratio conditions it can coincide with a maximum-Sharpe portfolio; those conditions are theoretical motivation rather than empirical assumptions verified for every date.

Equal-risk-contribution weights satisfy

$$
RC_i^{\%}(w)=\frac{w_i(\Sigma w)_i}{w'\Sigma w}=\frac1N.
$$

The source solves a sum-of-squared-deviations objective, minimizing $\sum_i(RC_i^{\%}-1/N)^2$ under full investment. Endnote 3 describes a numerical fallback using nonnegative unnormalized variables $u$, with $w=u/(\mathbf1'u)$ and $\mathbf1'u>0$. A modern implementation may use another equivalent risk-budgeting algorithm, but should verify the resulting contribution equations rather than assume that inverse-volatility weights solve them.

The maximum-diversification proxy maximizes

$$
DR(w)=\frac{w'\sigma}{\sqrt{w'\Sigma w}},
$$

where $\sigma$ is the vector of individual volatilities. For nonnegative fully invested weights, the denominator is no greater than the weighted average volatility, so $DR\geq1$. The portfolio coincides with a maximum-Sharpe allocation when excess expected returns are proportional to individual volatility. The paper relies on the cited maximum-diversification construction and does not supply complete solver settings and bound conventions for this proxy. The nonnegative-weight qualification is important: the displayed diversification inequality is not a general statement for unrestricted signed portfolios.

Finally, the risk-efficient proxy uses semideviation as a substitute for expected excess return. Stocks are sorted into ten semideviation groups. Let $J$ be the $N\times10$ group-indicator matrix and let $\xi_j$ be the median semideviation in group $j$. The proxy solves

$$
\max_w\frac{w'J\xi}{\sqrt{w'\Sigma w}},\qquad
\mathbf1'w=1,\qquad \frac{1}{2N}\leq w_i\leq\frac{2}{N}.
$$

The prose on p. 71 gives an upper bound of $1/N$, but the explicit constraint on p. 72 gives $2/N$. The former would force equal weights under full investment, so the latter is the coherent displayed specification followed here. The semideviation reference threshold and all numerical optimization details are not fully restated in the article; it points to the underlying risk-efficient indexing methodology.

## Universe, information timing, and covariance estimation

The data span January 1984–December 2012. At each month-end, the universe is the 100 largest S&P 500 equities with no missing observations in the estimation sample. The authors call this the S&P 100 universe for convenience; it should not be replaced silently by the official S&P 100 constituent list. Eligibility and size are reassessed monthly, so the universe changes.

Adjusted prices, market capitalization, and fundamentals come from COMPUSTAT. Sector results use ten GICS groups. US Fama–French and Carhart factors are taken from Kenneth French's data library. The risk-free rate is the three-month US Treasury bill. Forecasts are made at month-end for the following month, and proxy portfolios are rebalanced at that same frequency.

The baseline rolling history is three years, corresponding to 156 weekly observations for covariance estimation and approximately 36 monthly observations for return-model estimation. Consequently the baseline evaluation starts in January 1987 and ends in December 2012, producing 312 monthly forecast observations. Two- and four-year histories are used in robustness comparisons. The paper does not provide the security identifier panel, all membership-history cleaning decisions, or a detailed rule for return availability around delistings and corporate actions.

Covariance is estimated from weekly log returns using an exponentially weighted moving average with decay 0.94. The estimator is initialized at a Ledoit–Wolf shrinkage estimate of unconditional covariance over the estimation window. The resulting weekly log-return covariance is projected to a monthly arithmetic-return covariance following Meucci's horizon-transformation approach.

The article does not print the complete transformation code, centering convention, weekly sampling day, exact week-to-month factor, or assumed log-return mean used in the transformation. Under a multivariate-normal log-return model, a mathematically consistent transformation for a horizon with log means $a_i$ and log covariance $V$ is

$$
\operatorname{Cov}(R_i,R_j)=
\exp(a_i+a_j+V_{ii}/2+V_{jj}/2)\{\exp(V_{ij})-1\}.
$$

This formula is supplied here as an implementation clarification, not as evidence that the authors used particular unreported mean or horizon inputs. Simply scaling a weekly covariance by the number of weeks is an approximation to the arithmetic transformation, not its general exact form.

The decay parameter is applied to weekly observations. Using 0.94 on daily data creates a very different effective memory. Likewise, the one-quarter lag on annual accounting information is a specific source convention; it is not a guarantee that every historical filing was available within that lag. Reproduction using actual publication timestamps would be a useful additional check.

## Time-series baselines

Four alternatives directly forecast monthly stock returns: a constant mean, an AR(1), a Fama–French three-factor model, and a Carhart four-factor model. They are estimated by ordinary least squares using monthly returns over the rolling history. The factor returns themselves follow AR(1) forecasting equations.

A consistent implementation of the AR(1) baseline estimates an intercept and slope using information available through the forecast date and forms the next-month conditional mean. For a factor model, forecast each factor one month ahead and combine those forecasts with the stock's fitted factor exposures and any included regression intercept. The article describes this structure but does not state every regression convention, such as treatment of intercepts in all factor-return forecasts, so those should be declared rather than inferred from a software default.

These are deliberately limited comparators. Endnote 2 excludes forecasts using state variables such as dividend-price ratios. The study is not a tournament against all conditional-mean estimators, modern shrinkage forecasts, or machine-learning methods. Its conclusions about time-series forecasting refer to these four models and their short rolling estimation samples.

There is also no separate cross-validation process selecting a winning proxy before the reported evaluation period. The paper compares prespecified alternatives and reports robustness over a few choices of risk aversion and history length. Choosing the best method after seeing its full-sample accuracy would add a selection step absent from the experiment.

## Performance of the proxy portfolios

Exhibit 1 first checks the portfolios from which expected returns are extracted. All are evaluated with month-end rebalancing during the 312-month out-of-sample window. The following are reported annualized mean returns, annualized volatilities, annualized Sharpe ratios, and empirical monthly 5th-percentile returns, which the paper labels VaR95:

| Proxy | Mean % | Volatility % | Sharpe | Monthly VaR95 % |
|---|---:|---:|---:|---:|
| Capitalization | 10.10 | 15.67 | 0.41 | -7.02 |
| Smoothed capitalization | 10.18 | 15.91 | 0.41 | -7.37 |
| Fundamental | 9.47 | 16.22 | 0.35 | -7.77 |
| Equal weights | 10.60 | 15.80 | 0.44 | -7.65 |
| Inverse volatility | 10.73 | 14.51 | 0.48 | -6.10 |
| Equal risk contribution | 10.79 | 14.22 | 0.50 | -5.97 |
| Maximum diversification | 10.45 | 14.38 | 0.47 | -6.06 |
| Risk efficient | 10.92 | 14.66 | 0.49 | -6.36 |

The risk-based alternatives have similar mean returns and lower volatility and downside losses. The paper reports volatility differences significant at 1%. These are not net-of-cost comparisons. Endnote 5 notes that practical smart-beta products often rebalance quarterly or annually to reduce turnover, whereas monthly rebalancing is chosen here to align portfolio formation with forecast evaluation.

Sector composition helps explain the differences. Maximum diversification allocates on average 5.71% to financials and 6.63% to industrials, versus 13.39% and 9.81% for capitalization weighting. It places 19.99% in consumer staples, 17.13% in healthcare, and 7.47% in utilities, compared with 14.98%, 12.63%, and 1.48% for the market proxy. Thus the lower-risk portfolio is not sector neutral. Its behavior cannot be attributed solely to a universal stock-level improvement independent of sector allocation.

Exhibit 2 reports average stock volatility around 28.18% annualized and average correlation around 31.31% across the universe. Higher-risk and more correlated sectors have larger covariances with many proxies and therefore higher reverse-implied expected returns. Maximum diversification reduces the average covariance with the proxy, helping explain why it produces less aggressive implied premiums.

## Forecast levels, accuracy, and the importance of units

Exhibit 3 reports average annualized predicted returns of 10.61% for capitalization-implied returns, 10.59% for smoothed capitalization, 10.85% for fundamental, 10.87% for equal weights, 10.01% for inverse volatility, 9.42% for equal risk contribution, 7.31% for maximum diversification, and 9.47% for risk efficient. The four time-series alternatives range from 16.29% to 17.23%.

These are averages of forecasts, not realized strategy returns. Maximum diversification is notably more conservative, but conservative forecasts need not be more accurate in every market. Figure 4 shows large time variation: covariance-implied forecasts rise during volatile episodes because risk premiums are mechanically proportional to covariance, while extrapolative time-series forecasts can turn negative after price declines. Neither response is proof of the true conditional mean's behavior.

Forecast precision is measured monthly across the 100 stocks and then averaged across months. For model $a$, define

$$
HR_t^a=\frac1{N_t}\sum_i\mathbf1\{\operatorname{sign}(\widehat\mu_{i,t}^a)=\operatorname{sign}(r_{i,t+1})\},
$$

$$
RMSFE_t^a=\sqrt{\frac1{N_t}\sum_i(r_{i,t+1}-\widehat\mu_{i,t}^a)^2}.
$$

This order of aggregation matters: averaging monthly cross-sectional root mean squared errors is generally different from taking one root after pooling every squared error.

Exhibit 5's column heading misleadingly prints percent for RMSFE, but its note and Exhibit 6 specify **per mille**. Thus 79.24 means 0.07924 in decimal returns, or 7.924 percentage points, not 79.24%.

| Method | Hit ratio % | RMSFE, per mille | Cross-stock forecast SD % | Time-series forecast SD % | Forecast lag-1 correlation % |
|---|---:|---:|---:|---:|---:|
| Capitalization implied | 55.46 | 79.24 | 0.28 | 0.59 | 55.52 |
| Smoothed capitalization implied | 55.46 | 79.23 | 0.28 | 0.60 | 55.55 |
| Fundamental implied | 55.46 | 79.33 | 0.29 | 0.64 | 55.17 |
| Equal-weight implied | 55.46 | 79.24 | 0.29 | 0.62 | 55.58 |
| Inverse-volatility implied | 55.46 | 79.16 | 0.23 | 0.52 | 58.18 |
| Equal-risk-contribution implied | 55.47 | 79.15 | 0.20 | 0.48 | 60.36 |
| Maximum-diversification implied | 55.47 | 79.18 | 0.11 | 0.34 | 65.24 |
| Risk-efficient implied | 55.46 | 79.15 | 0.20 | 0.49 | 59.75 |
| Constant mean | 53.84 | 80.51 | 1.16 | 1.29 | 26.87 |
| AR(1) | 53.46 | 81.80 | 1.85 | 2.08 | 9.35 |
| Fama–French | 53.45 | 80.87 | 1.29 | 1.54 | 22.71 |
| Carhart | 53.35 | 81.13 | 1.33 | 1.59 | 21.15 |

Capitalization-implied RMSFE is lower than every time-series comparator at the reported 1% level. Within implied-return methods, the inverse-volatility improvement over capitalization is significant at 5%, and the risk-efficient improvement at 10%. The article says other risk-based accuracy differences are not statistically significant. It would be wrong to label the smallest displayed number a decisively superior forecast without those qualifications.

The size of the within-family accuracy improvement is tiny. A fall from 79.24 to 79.15 per mille equals 0.09 per mille, or 0.009 percentage points of RMSFE, approximately a 0.11% relative reduction. By comparison the difference from the constant-mean baseline is 1.27 per mille, approximately a 1.58% relative reduction. These calculations contextualize the statistically reported differences.

Hit ratios barely differ among implied-return methods. Because risk-free rates and covariance-implied premiums are often positive, a directional hit ratio should be compared with a simple always-positive benchmark before being interpreted as substantial market-timing skill. The paper does not report that extra comparison. A similar hit ratio across proxies can coexist with different forecast magnitudes, cross-sectional rankings, and squared errors.

## Stability is the more substantial result

Cross-sectional dispersion is the monthly standard deviation of the 100 forecasts, averaged through time. Time-series instability is computed separately for individual stocks with at least twelve consecutive forecast observations, then averaged across stocks in the union of the changing universe. Lag-one forecast autocorrelation is aggregated in the same stock-first spirit.

Maximum-diversification-implied returns reduce cross-stock forecast dispersion from 0.28% to 0.11%, approximately 61%, compared with the capitalization proxy. Time-series forecast standard deviation falls from 0.59% to 0.34%, approximately 42%, while autocorrelation rises from 0.5552 to 0.6524. Equal risk contribution also reduces both dispersion measures meaningfully.

The difference from time-series baselines is larger still: the constant-mean forecasts have cross-stock dispersion 1.16% and time-series standard deviation 1.29%; AR(1) reaches 1.85% and 2.08%. The authors report economically and statistically significant differences at 1% for the broad stability comparisons.

Greater persistence is useful when it reflects stable information, but it is not independently proof of accuracy. A constant or overly smoothed forecast is also stable. The value here is the combination of substantially reduced variability with similar or slightly better measured accuracy in the stated sample. Whether that translates into superior optimizer performance depends on the covariance used downstream, portfolio constraints, and costs, none of which is fully tested in a forecast-to-trading exercise here.

Statistical significance throughout the article uses $t$ tests with heteroskedasticity- and autocorrelation-consistent standard errors (endnote 6). The HAC kernel, bandwidth, finite-sample corrections, and exact series used for every portfolio-volatility comparison are not fully specified. The reported significance levels are source findings; the note does not imply that independent replication of each $p$ value is possible from the tables alone.

## Robustness and combinations

Exhibit 6 changes the estimation window to two, three, or four years and risk aversion to 1, 2.4, or 5. Implied-return RMSFE changes little with the window length. Increasing the mean-estimation sample helps the time-series models: the constant-mean RMSFE falls from 80.77 to 80.18 per mille between two and four years, while AR(1) falls from 83.05 to 81.19. These remain above the implied-return alternatives.

At a three-year window, capitalization-implied RMSFE is 79.20, 79.24, and 79.84 for the three risk-aversion values. Equal-risk-contribution figures are 79.19, 79.15, and 79.43; maximum-diversification figures are 79.23, 79.18, and 79.25. The paper does not find differences caused by changing risk aversion statistically significant at 1%. This supports local robustness, not invariance to arbitrary horizons, covariance estimators, or much more extreme risk-aversion choices.

Forecast combinations are formed separately within all four time-series forecasts, all eight implied forecasts, and the four risk-based implied forecasts. Four rules are compared: simple average; componentwise median; weights proportional to the previous month's hit ratio; and weights inversely proportional to a twelve-month average squared forecast error. The last rule starts with equal weights for its first eleven months, as specified in endnote 7. Performance weights must use only previously observed errors.

For equal-weight aggregation, the time-series combination has hit ratio 53.73% and RMSFE 80.70 per mille. The all-implied combination has 55.46% and 79.20, while the risk-based combination has 55.46% and 79.15. Its cross-sectional dispersion is 0.18%, time-series standard deviation 0.45%, and lag-one forecast correlation 60.76%. Median and performance-weighted combinations yield very similar results.

These combinations reduce the need to select a single winner with hindsight. Their main benefit in this experiment is retaining the stability of the family; there is no large additional accuracy gain from elaborate weighting. The implementation of inverse-error weights requires a rule for zero or missing errors, which the paper does not detail, although the empirical setting evidently avoids a reported failure.

## What can be concluded and what remains to reproduce

The evidence favors reverse-implied means as stable alternatives to short-window time-series mean estimates for the selected large-US-stock universe. Among efficient-portfolio proxies, risk-based allocations materially reduce the variability of expected-return inputs; their average forecast-error advantage over capitalization weighting is modest. This is a useful reason to test alternatives to a market-capitalization prior, rather than treat that prior as compulsory.

A complete replication still requires point-in-time universe membership and accounting availability, return adjustments, weekly calendar conventions, covariance initialization and horizon projection, precise smart-beta optimization domains, missing-value handling, HAC settings, and forecast-combination initialization. The paper supplies enough structure to reconstruct the experiment's architecture, but not enough to reproduce every table exactly without choices on those items.

Finally, implied returns inherit the risk model and chosen proxy. The mapping does not transform an arbitrary portfolio into independently verified alpha. Its practical purpose is to supply coherent, comparatively stable inputs whose assumptions can be inspected. The reported gains should be judged against that purpose, with forecast accuracy, forecast stability, proxy-portfolio performance, and downstream trading performance kept separate.
