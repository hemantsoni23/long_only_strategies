# Estimating Betas from Nonsynchronous Data

Myron Scholes and Joseph Williams. Journal of Financial Economics 5 (1977), 309–327. Received November 1976; revised October 1977. [Source PDF](<../../Finance/AsynchronousReturns_ScholesWilliams_1977.pdf>).

## Why this matters

A daily return calculated from the last reported trade need not cover the same time interval as another stock's daily return. The calendar labels agree while the underlying economic intervals overlap only partly. A contemporaneous market regression can therefore give a misleading estimate of systematic risk even when the latent return process has a constant beta.

The paper derives a correction that uses information displaced into adjacent days. Add the slopes from separate regressions on the previous, current, and next market return, then divide by one plus twice the market's first-order autocorrelation. The denominator matters because nonsynchronous observations distort the market index as well as the individual stock. The result is computationally simple and does not require knowing every trade time.

The empirical comparison uses daily NYSE and ASE returns from 1963–1975. In the lowest trading-volume quintile, ordinary daily OLS betas average 21.8% below the corrected estimates; in the highest quintile, they average 5.0% above them. Those are differences between estimators under the maintained model, not errors measured against directly observed true betas.

Beyond beta estimation, the paper shows that random observation times can alter covariance, autocorrelation, and kurtosis even when latent returns have independent Gaussian increments. Some apparently dynamic behavior in daily data can thus come from the observation process. The theory does not imply that all serial dependence or heavy tails in actual returns arise this way.

## Latent prices, observed prices, and the sampling clock

Let the latent log-price process for security $n$ have stationary independent increments with per-period mean $\mu_n$, variance $\sigma_n^2$, and cross-security covariance $\sigma_{nm}$. The main exposition assumes jointly normal increments. A footnote allows broader infinitely divisible independent-increment processes for the relevant moment results; the Gaussian kurtosis calculation uses the stronger normality assumption.

The latent return over the calendar interval $[t-1,t]$ is $r_{n,t}$. With fixed market-index weights $x_{nM}$,

$$
r_{M,t}=\sum_nx_{nM}r_{n,t},
\qquad
r_{n,t}=\alpha_n+\beta_nr_{M,t}+\epsilon_{n,t},
$$

$$
\beta_n=\frac{\sigma_{nM}}{\sigma_M^2},
\qquad
\alpha_n=\mu_n-\beta_n\mu_M.
$$

The last trade within period $t$ occurs at $t-s_{n,t}$, where $0\leq s_{n,t}\leq1$. The variable $s_{n,t}$ is the fraction of the period between that trade and the calendar close. When prices are available for two consecutive periods, the measured return is over

$$
[t-1-s_{n,t-1},\,t-s_{n,t}],
$$

whose length is $L_{n,t}=1-s_{n,t}+s_{n,t-1}$. Figure 1, PDF page 4, draws these intervals for two stocks and shows why a measured return can overlap both contemporaneous and adjacent-period returns of another stock.

The paper excludes returns involving periods with no trade rather than treating an unchanged recorded price as a zero economic return. This restriction is integral to its one-lead/one-lag construction. It does not establish that one lag corrects arbitrarily long nontrading episodes or slower information incorporation into quotes.

For the simplified formulas, the vector $S_t=(s_{1,t},\ldots,s_{N,t})$ is iid over calendar time. Components within a date may be dependent. Conditional return moments also assume the observation times do not reveal additional price-process information beyond the interval lengths: the conditional increments have the specified drift and covariance rates. Endogenous trading triggered by particular latent price shocks can violate that construction.

The measured market return is the same weighted combination of measured asset returns, $r^s_{M,t}=\sum_nx_{nM}r^s_{n,t}$. The superscript $s$ denotes sampled returns, not a new asset or a power. Its population contemporaneous regression is

$$
r^s_{n,t}=\alpha_n^s+\beta_n^sr^s_{M,t}+\epsilon^s_{n,t},
$$

with $\beta_n^s=\operatorname{Cov}(r^s_n,r^s_M)/\operatorname{Var}(r^s_M)$ and $\alpha_n^s=E[r^s_n]-\beta_n^sE[r^s_M]$. These are properties of the observed regression and need not equal the latent parameters.

## Observed moments and a source sign correction

Conditional on timing, the mean measured return is $\mu_nL_{n,t}$. Under iid timing, $E[L_{n,t}]=1$, so the observed mean remains $\mu_n$. The law of total variance gives

$$
\operatorname{Var}(r^s_{n,t})
=\sigma_n^2+2\mu_n^2\operatorname{Var}(s_n).
$$

Adjacent observed intervals for the same security share an endpoint but do not overlap. Their random lengths move in opposite directions when that endpoint moves. Consequently,

$$
\operatorname{Cov}(r^s_{n,t},r^s_{n,t-1})
=-\mu_n^2\operatorname{Var}(s_n).
$$

These are equations (6) and (8), equivalently written in the source using the coefficient of variation $v_n=\sigma_n/\mu_n$. The direct formulas above avoid division by zero when $\mu_n=0$. They also show why the variance inflation and own-return negative autocovariance can be small for daily data: both are proportional to the squared daily drift.

For two securities, the expected contemporaneous overlap is $1-E|s_n-s_m|$. Including the covariance of their random conditional means gives

$$
\operatorname{Cov}(r^s_{n,t},r^s_{m,t})
=\{1-E|s_n-s_m|\}\sigma_{nm}
+2\mu_n\mu_m\operatorname{Cov}(s_n,s_m).
$$

For a current return of $n$ and a previous-period return of $m$, the overlap has expected length $E[(s_n-s_m)_+]$. The consistent adjacent covariance is

$$
\operatorname{Cov}(r^s_{n,t},r^s_{m,t-1})
=E[(s_n-s_m)_+]\sigma_{nm}
-\mu_n\mu_m\operatorname{Cov}(s_n,s_m).
$$

The minus sign in the final term is a derived correction to printed equation (9), which has a plus sign. Appendix equation (A3), PDF page 17, gives the general timing contribution as

$$
\mu_n\mu_m
\operatorname{Cov}(s_{n,t}-s_{n,t-1},
                  s_{m,t-1}-s_{m,t-2}).
$$

With iid vectors across dates this equals $-\mu_n\mu_m\operatorname{Cov}(s_n,s_m)$. The same correction is necessary for equation (9) to reduce to the negative own-autocovariance in equation (8) when $n=m$. Appendix equation (A7) repeats the sign inconsistency in its intermediate braces. These are internal algebraic checks of the local printed source, not an official published erratum.

Adding contemporaneous covariance and both adjacent cross-covariances now cancels all timing-mean terms and reconstructs $\sigma_{nm}$:

$$
\operatorname{Cov}(r^s_{n,t},r^s_{m,t})
+\operatorname{Cov}(r^s_{n,t},r^s_{m,t-1})
+\operatorname{Cov}(r^s_{n,t-1},r^s_{m,t})
=\sigma_{nm}.
$$

The overlap terms cancel because $(a-b)_++(b-a)_+=|a-b|$. Under the iid timing assumption, covariances at larger lags vanish. The main beta estimator follows from this identity and is preserved when the intermediate sign is corrected.

For daily stocks the paper reports typical coefficients of variation around 30–40. The drift-squared terms are then small relative to the diffusion variance. Contemporaneous covariances are approximately attenuated by incomplete overlap, whereas adjacent cross-covariances recover the displaced co-movement. In a diversified portfolio with mainly positive constituent correlations, reduced pairwise covariance can lower measured portfolio variance even though each constituent's measured variance is slightly increased.

Random interval lengths also produce a normal mixture. Under the Gaussian model, the source derives

$$
\kappa(r^s_{n,t})
=3\{1+2\operatorname{Var}(s_n)\}+O(v_n^{-2}).
$$

Thus measured returns can be leptokurtic although true increments are Gaussian. At zero drift the leading expression is exact: conditional variance is $\sigma_n^2L_{n,t}$, and $E[L^2]=1+2\operatorname{Var}(s_n)$. This observation is useful as a diagnostic but does not calibrate the full tail behavior of actual equity returns.

## Deriving the beta and alpha correction

Define the adjacent simple-regression slopes by which market date appears on the right-hand side:

$$
\beta_n^{s,-}=
\frac{\operatorname{Cov}(r^s_{n,t},r^s_{M,t-1})}
{\operatorname{Var}(r^s_{M,t-1})},
\qquad
\beta_n^{s,+}=
\frac{\operatorname{Cov}(r^s_{n,t},r^s_{M,t+1})}
{\operatorname{Var}(r^s_{M,t+1})}.
$$

Let $\rho_M^s$ be the first-order autocorrelation of the observed market index. Stationarity makes the market variances in these three regressions equal in population. Summing the covariance conservation identity over index weights yields

$$
\sigma_{nM}=
\operatorname{Var}(r_M^s)
(\beta_n^{s,-}+\beta_n^s+\beta_n^{s,+}),
$$

$$
\sigma_M^2=
\operatorname{Var}(r_M^s)(1+2\rho_M^s).
$$

Therefore

$$
\beta_n=
\frac{\beta_n^{s,-}+\beta_n^s+\beta_n^{s,+}}
{1+2\rho_M^s}.
$$

The sample estimator in equation (20) replaces these quantities by the three separate OLS slopes and a sample autocorrelation:

$$
\widehat\beta_n=
\frac{b_n^-+b_n+b_n^+}{1+2\widehat\rho_M},
\qquad
\widehat\alpha_n=\bar r_n^s-\widehat\beta_n\bar r_M^s.
$$

The means in the source use the interior dates $t=2,\ldots,T-1$, so adjacent market observations are available. Each constituent slope is estimated with an intercept. Summing coefficients from one regression containing all three market returns is a different estimator because those coefficients are partial slopes in the presence of correlated regressors.

The denominator is a market measurement correction. If observed market variance is understated, the preceding variance identity implies positive observed market autocorrelation. Ignoring the denominator overstates the covariance recovered by the numerator relative to true market variance.

For the observed regression, $\alpha_n^s=\alpha_n+(\beta_n-\beta_n^s)\mu_M$. Under a positive market drift, a downward beta distortion corresponds to an upward alpha distortion. The paper discusses downward beta bias for infrequently traded assets and possible downward bias for extremely fast-trading assets relative to the rest of the market; other assets must compensate because index-weighted betas average to one. The actual high-volume portfolio in its empirical sample instead has an upward OLS beta distortion, consistent with its position relative to the value-weighted market.

These are model-based directional arguments. Trading volume is only a proxy for the unobserved timing distribution, and the precise sign depends on relative overlap with the market, not merely on whether a stock has a large or small absolute volume.

## Instrumental-variable form and inference

The paper also constructs an instrumental-variable estimator with the moving sum

$$
z_t=r^s_{M,t-1}+r^s_{M,t}+r^s_{M,t+1}.
$$

Using demeaned observations on the interior sample,

$$
\widehat\beta_n^{IV}=
\frac{\sum_t(z_t-\bar z)(r^s_{n,t}-\bar r_n^s)}
{\sum_t(z_t-\bar z)(r^s_{M,t}-\bar r_M^s)},
\qquad
\widehat\alpha_n^{IV}=
\bar r_n^s-\widehat\beta_n^{IV}\bar r_M^s.
$$

The instrument pools market information across the whole interval that can overlap an observed stock return. The authors establish asymptotic equivalence to the ratio of the three OLS slopes. Exact finite-sample equality need not hold if each regression uses different endpoint observations, means, or market variances.

The inclusion of $t+1$ makes the estimator retrospective: it needs an adjacent future observation to estimate historical exposure. That is not a defect for ex post beta estimation. A live implementation must wait for the last required observation and cannot treat the resulting beta as available at the earlier close.

For the paper's standard-error formulas, let $\omega_n^{s\,2}$ and $\rho_n^s$ denote the variance and first-order autocorrelation of the observed-regression residuals, let $\rho_z$ be the first-order autocorrelation of $z_t$, and define

$$
\gamma_{M,z}=
\frac{\operatorname{Cov}(r^s_{M,t},z_t)}
{\operatorname{Var}(z_t)}.
$$

Equations (25)–(26), PDF pages 10–11, give the model-specific approximations

$$
\operatorname{SE}(\widehat\beta_n)^2
\approx
\frac{\omega_n^{s\,2}}{T-2}
\frac{1+2\rho_n^s\rho_z}
{\gamma_{M,z}^2\operatorname{Var}(z_t)},
$$

$$
\operatorname{SE}(\widehat\alpha_n)^2
\approx
\mu_M^2\operatorname{SE}(\widehat\beta_n)^2
+\frac{\omega_n^{s\,2}}{T-2}(1+2\rho_n^s).
$$

The source substitutes sample estimates of these moments. Its appendix factors covariance products under the maintained timing and return model. These formulas should not be imported as distribution-free robust standard errors for a heteroskedastic financial return process.

A modern robustness calculation can instead estimate the IV moment equations $E[(1,z_t)^\top(r^s_{n,t}-\alpha-\beta r^s_{M,t})]=0$ and use a heteroskedasticity-and-autocorrelation-consistent covariance matrix for the moments. That is an additional inference method, not what the paper reports. It is especially useful if adjacent observations, missing-data patterns, or volatility clustering produce dependence beyond the model's simple structure.

The denominator must also be checked numerically. A small $\operatorname{Cov}(r_M^s,z)$ creates an unstable ratio. Under the source model it equals the positive latent market variance, but unrestricted sample estimates can be noisy. Neither silently truncating the denominator nor winsorizing the corrected beta is part of the published estimator.

## The empirical design

The empirical sample covers January 1963 through December 1975 and uses daily returns from stocks listed on the New York and American Stock Exchanges. The introductory footnote describes the CRSP daily total-return database, whose broader collection begins in July 1962; the actual portfolio experiment starts in 1963 because earlier trading-volume information is incomplete.

For each calendar year, stocks are ranked by the total number of shares traded during that year. Five portfolios contain successive 20% groups, from the lowest to the highest annual share volume. These are descriptive same-year sorts. The use of the entire year's volume to classify that year's returns would be look-ahead information in a purported live portfolio-selection strategy, but the paper uses the groups to compare measurement distortion.

Daily quintile returns are computed as the logarithm of one plus the arithmetic average of constituent simple returns. The market is value weighted. For a weighted market, the arithmetic aggregation uses its market weights before the logarithm. This empirical return construction differs slightly from a fixed weighted sum of individual log returns in the theory; footnote 12 calls the daily difference small and notes the nonstationarity introduced by value weights.

If a security does not trade on a given day, its return is excluded from portfolio calculations both that day and the following trading day. This prevents a last-trade return spanning a longer gap from being treated as a one-day return in the restricted model. The source says the procedure excludes less than 2% of available securities. It does not give a complete date-by-date exclusion count or a full machine-readable rule for every CRSP missing-price code.

The available number of securities ranges from 1,487 in 1963 to 2,626 in 1973, averaging 2,305 over the 13 years. There are approximately 251 trading days per year. Betas, alphas, lead-lag slopes, market autocorrelation, and residual statistics are estimated for each annual portfolio series. Results are printed for quintiles 1, 3, and 5; quintiles 2 and 4 are omitted to save space.

Share volume proxies for the desired but unavailable number of separate trades. The authors cite the prevalence of trades in 100- and 200-share round lots as support for that proxy. Volume is not turnover, dollar trading volume, bid-ask spread, or direct measurement of the time of the last trade. An exact replication needs to settle volume adjustments around splits and other corporate actions; the article does not document that detail.

## Numerical results and what they establish

Tables 1–3, PDF pages 13–15, compare corrected and ordinary betas. Representative rows are:

| Year | Volume group | Corrected beta | Ordinary contemporaneous beta |
|---|---|---:|---:|
| 1963 | Lowest quintile | 0.544 | 0.303 |
| 1963 | Middle quintile | 0.905 | 0.785 |
| 1963 | Highest quintile | 1.336 | 1.495 |
| 1969 | Lowest quintile | 0.872 | 0.749 |
| 1969 | Middle quintile | 1.330 | 1.257 |
| 1969 | Highest quintile | 1.501 | 1.531 |
| 1975 | Lowest quintile | 0.577 | 0.415 |
| 1975 | Middle quintile | 0.996 | 0.857 |
| 1975 | Highest quintile | 1.172 | 1.174 |

For 1963 the low-volume corrected beta has reported standard error 0.065, compared with 0.031 for the contemporaneous OLS slope. This illustrates a material precision cost: the correction uses additional estimated components. It is inappropriate to compare the two point estimates as though their estimation errors were independent; both use the same return history.

Across all 13 years, the average corrected betas are 0.674, 1.116, and 1.368 for the low-, middle-, and high-volume groups. Thus true-exposure differences, as measured by the maintained correction, also vary with volume. A raw comparison of beta levels would mix those differences with the measurement distortion.

To separate them descriptively, the authors calculate

$$
d_{n,y}=\frac{b_{n,y}-\widehat\beta_{n,y}}
{\widehat\beta_{n,y}}
$$

for each portfolio and year. Figure 2, PDF page 16, displays those annual ratios. Their averages are −0.218, −0.082, and +0.050 for quintiles 1, 3, and 5 respectively. These are averages of annual ratios, not the ratio of two pooled beta averages. They indicate how far ordinary OLS falls below or above the corrected estimate.

The low-volume corrected beta exceeds the ordinary beta in every reported year. For high-volume stocks the direction is reversed in the printed comparison. The paper interprets this pattern relative to a value-weighted market heavily influenced by frequently traded stocks. It does not say that low volume causes lower economic beta; indeed, the corrected betas themselves differ markedly across groups.

As volume rises, lagged-market slopes tend to fall, leading-market slopes tend to rise, and residual first-order autocorrelation tends to decrease. The residual standard deviations show no clear cross-group pattern. Market autocorrelation is generally positive and often statistically distinguishable from zero, but not in every year: the printed estimate is −0.058 with standard error 0.063 in 1963, while it is 0.390 with standard error 0.060 in 1969.

The theoretical alpha-bias prediction cannot be verified clearly from the tables because alpha standard errors are too large. The authors explicitly state this limitation. The paper therefore supports the beta-pattern comparison more strongly than a claim that the alpha correction produces a measured economic improvement.

A simple implementation check can reconstruct a reported beta from its adjacent slopes and market autocorrelation. For example, the 1975 low-volume row gives $(0.402+0.415+0.057)/(1+2\times0.258)\approx0.5765$, consistent with the reported 0.577 after rounding. Exact equality should not be demanded from the tables' three-decimal inputs.

## A reproducible implementation and its limits

Begin with adjusted daily simple returns, a documented trade/no-trade indicator, annual share volume, and market-capitalization weights. Reproduce the annual quintile assignment, then apply the no-trade exclusion to both affected days before aggregating returns. Save the number of active constituents and the resulting weights each day so changes in the portfolio are visible.

Convert aggregated simple returns to log returns as in the paper. For each calendar-year series, build aligned records containing the portfolio return and the previous, current, and next market return. Estimate the three simple slopes with intercepts, estimate market autocorrelation on a documented sample, and calculate the corrected beta and alpha. Separately calculate the IV version to assess finite-sample endpoint differences.

Output all three slopes and the denominator, rather than only the final beta. Report the contemporaneous OLS baseline, the corrected estimate, their annual ratio, and the source-style standard errors. If robust inference is added, label it separately. The mean ratio and the ratio of mean betas should be retained as different statistics.

The article does not supply the original observation file, exact constituent identifiers, daily market weights, all portfolio-formation tie rules, or every treatment of missing and delisting observations. It supplies enough design to reproduce the method and the principal comparison, but not a guaranteed bit-for-bit reconstruction of the printed tables from current CRSP vintages.

There are no transaction costs, execution rules, portfolio turnover calculations, forecasts, or net returns from a trading strategy. The empirical objective is estimating exposures, not earning alpha. Same-year sorting and use of a leading market return are therefore legitimate parts of its retrospective design while remaining unavailable as contemporaneous trading inputs.

The most consequential model risks are iid timing, independent latent increments, and the restriction of relevant spillovers to one adjacent period. If quote adjustment is delayed over several days, if true returns contain serial dependence, or if trading times depend on latent shocks, the three-term correction need not recover the desired beta. The method is also an asymptotic correction, not an assertion of exact finite-sample unbiasedness.

## Source map

PDF pages 1–3 introduce the problem and the continuous-time sampling model; page 4 is Figure 1. Pages 5–6 give observed moments and kurtosis. Pages 7–9 derive parameter distortion and the corrected estimators. Pages 10–11 give the IV interpretation and standard-error formulas. Pages 11–12 describe the annual portfolio experiment and its interpretation. Pages 13–15 contain the full printed tables, and page 16 contains Figure 2 and the conclusion. Pages 17–19 contain the appendix proofs and references. All 19 pages, including each table and appendix equation, were read.
