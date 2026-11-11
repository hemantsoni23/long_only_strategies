# High Frequency Analysis of Lead-Lag Relationships between Financial Markets

**Frank de Jong and Theo Nijman (1997).** *Journal of Empirical Finance* 4, 259–277. Source: [original PDF](../../Finance/NonSynchronousTrading_deJongNijman_1997.pdf). The full nineteen-page article, Appendices A–B, and empirical tables were read; the interval-overlap equation, covariance formulas, carry relation, and lead–lag table were also checked in page images.

## Why this matters and what is new

A price series observed at irregular transaction times is not an ordinary regularly sampled return series with a few harmless missing entries. A price difference between observed transactions accumulates all underlying returns since the preceding observation. Inserting zero returns into empty clock intervals and assigning the accumulated move to the next trade redistributes genuine covariance across apparent leads and lags. This is especially damaging when the purpose of the analysis is precisely to measure which market incorporates information first.

De Jong and Nijman turn that accumulation into an estimable linear equation. Products of actually observed price changes have expectations equal to weighted sums of the underlying return covariances. The weights depend only on the overlap of observation intervals after shifting them by each possible lag. Regressing observed products on these known overlap counts estimates the latent covariance function without filling missing prices.

The innovation is not an assumption that efficient returns are serially independent. The estimator explicitly allows nonzero own and cross covariances over a chosen range of lags, unlike corrections that impose contemporaneous-only latent dependence. The article also derives dependence-aware standard errors, a bid–ask extension, and an application to the S&P 500 cash index and its futures.

“Arbitrarily high frequency” describes the absence of an intrinsic imputation interval in the model. It does not mean unlimited resolution from finite data: timestamps, observation density, identification, truncation, and sampling uncertainty still constrain inference. Nor does the method make endogenous transaction times innocuous. Independence between the price process and observation times is a central maintained assumption.

## Latent process and observed returns

Let $p_t$ and $q_t$ denote two log-price processes on an underlying discrete clock grid. Their levels may be nonstationary, while their increments $\Delta p_t=p_t-p_{t-1}$ and $\Delta q_t=q_t-q_{t-1}$ are stationary. The initial derivation assumes zero mean and no deterministic component. Define

$$
\gamma_k=\operatorname{Cov}(\Delta p_t,\Delta q_{t-k}).
$$

Positive $k$ means the $q$ return occurs earlier than the $p$ return. This convention is essential: reversing either the ordering of the assets or the sign of the lag reverses the verbal interpretation of a lead.

Suppose $p$ is observed at times $a_i$ and $q$ at times $b_j$. Distinct letters are used here to make the two observation sequences explicit; the original uses related $t$ subscripts. Let

$$
A_i=p_{a_{i+1}}-p_{a_i}=\sum_{t=a_i+1}^{a_{i+1}}\Delta p_t,
\qquad
B_j=q_{b_{j+1}}-q_{b_j}=\sum_{s=b_j+1}^{b_{j+1}}\Delta q_s.
$$

These are returns over observed intervals, which may span different numbers of latent periods. Their product is $Y_{ij}=A_iB_j$. Conditional on transaction times independent of the price process,

$$
E[Y_{ij}\mid\{a,b\}]
=\sum_{t=a_i+1}^{a_{i+1}}\sum_{s=b_j+1}^{b_{j+1}}\gamma_{t-s}.
$$

Thus the missing prices never have to be imputed. Their underlying increments enter through the covariance sum. A level-variable missing-data method that simply skips absent observations would not preserve this relation for accumulated returns.

The observation-time assumption is stronger than saying the data are irregular. If volatility shocks accelerate trading or signed innovations alter the next trade time, conditioning on observed intervals may change the relevant distribution of returns. The regressors constructed below then need not be exogenous. The paper recognizes this limitation and does not model the joint return–duration process.

## The overlap regression and an implementable estimator

For each possible covariance lag $k$, define the overlap count

$$
x_{ij}(k)=\max\{0,\min(a_{i+1},b_{j+1}+k)-\max(a_i,b_j+k)\}.
$$

This is Eq. (5), with Appendix A providing its derivation. Shift the second return interval by $k$ periods. Every latent period in the intersection then corresponds to one pair of increments separated by $k$. With integer timestamps on the base grid, the difference between the upper and lower endpoints is the number of such pairs. Half-open intervals $(a_i,a_{i+1}]$ and $(b_j+k,b_{j+1}+k]$ make the endpoint convention unambiguous.

Assume $\gamma_k=0$ whenever $|k|>K$. Stack $x_{ij}(k)$ for $k=-K,\ldots,K$ into a vector $x_{ij}$. Then

$$
Y_{ij}=x_{ij}^{\mathsf T}\gamma+e_{ij},
\qquad E[e_{ij}\mid x_{ij}]=0.
$$

There is no arbitrary regression intercept in the zero-mean covariance model. Collect the usable $x_{ij}^{\mathsf T}$ as rows of $X$ and $Y_{ij}$ as entries of $y$. The proposed estimator is ordinary least squares,

$$
\widehat\gamma=(X^{\mathsf T}X)^{-1}X^{\mathsf T}y.
$$

An implementation can accumulate the cross-products $X^{\mathsf T}X$ and $X^{\mathsf T}y$ without storing every row, then solve the system with a numerically stable factorization. That is an implementation option, not a separate weighting scheme proposed by the paper. A rank and condition-number check is necessary before interpreting fine-grid estimates.

Only adjacent observed price differences are needed. A return between nonadjacent observations is the sum of adjacent differences, so its product with another return is a corresponding sum of existing products. Such rows do not supply new underlying observations. They could change an arbitrary least-squares weighting, but are informationally redundant. Conversely, all pairs of adjacent observed intervals potentially matter, not only pairs whose endpoints are closest in time.

Rows with $x_{ij}(k)=0$ for every retained $k$ can be discarded because they do not enter either normal equation. The safe computational criterion is the overlap-vector test itself. Sorted intervals allow a moving window to avoid enumerating distant pairs. The authors formulate the method in terms of all relevant products; they do not supply a particular sparse-data implementation or complexity benchmark.

The estimator's consistency requires both the conditional moment relation and sufficient identification, along with time-series regularity for the relevant laws of large numbers. The finite-lag restriction is substantive. If nonzero higher-order covariances are omitted, the regression suffers omitted-variable bias, even when interest centers on only the first lag. Estimating a single desired covariance in isolation is not generally valid.

## Identification, autocovariances, and normalization

Two examples clarify what the overlap matrix can identify. If both prices are observed every period, each usable product loads on exactly one covariance lag. Apart from boundary conventions, $X^{\mathsf T}X$ is diagonal and the estimator reduces to the usual average product for each lag. The unusual-looking regression is therefore a generalization of the standard sample covariance calculation.

If instead both prices are observed only every second period, an observed product has expectation

$$
E[Y_{ij}]=\gamma_{2m-1}+2\gamma_{2m}+\gamma_{2m+1},\qquad m=i-j.
$$

The example with $K=2$ has linearly dependent columns. The available sums do not identify every underlying single-period covariance. Regularly subsampling a process cannot, without extra assumptions, reveal all covariance detail between observations. Irregular spacing can create identifying variation in the overlap weights. The title's high-frequency ambition is therefore conditional on the design matrix, not guaranteed merely by choosing a smaller base unit.

To estimate a series' autocovariances, use its own intervals on both sides of the product. Because $\gamma_{-k}=\gamma_k$, combine the $k$ and $-k$ columns for $k=1,\ldots,K$, while leaving the lag-zero column unchanged. This yields $K+1$ parameters. Treating the symmetric coefficients as unrelated would introduce redundancy and waste the known restriction.

After estimating the two lag-zero variances $\widehat\gamma_0^p$ and $\widehat\gamma_0^q$, cross-correlations are

$$
\widehat\rho_k=
\frac{\widehat\gamma_k}{\sqrt{\widehat\gamma_0^p\widehat\gamma_0^q}}.
$$

The publication does not impose a positive-semidefinite covariance structure through a constrained optimization. Unrestricted finite-sample estimates are therefore not automatically a coherent covariance matrix for every collection of returns. Negative variance estimates or implausible normalized correlations would require diagnosis rather than silent clipping. Similarly, uncertainty in the denominator should be included when deriving uncertainty for normalized correlations; the paper states the normalization but does not provide a complete software recipe for a joint delta-method implementation.

For nonzero means, $E[A_iB_j]$ also contains the product of mean accumulated returns. Simply subtracting the same scalar from every irregular-length interval is inappropriate. A replication must state whether it assumes negligible intraday drift or removes a mean proportional to elapsed periods. The empirical section does not fully document this preprocessing choice.

## A small construction check and correlation uncertainty

The overlap weights can be checked before any financial data are used. Consider a first observed return spanning latent periods 1, 2, and 3, with endpoints $(0,3)$, and a second spanning periods 3 and 4, with endpoints $(2,4)$. The six underlying increment pairs have lag differences $t-s$ equal to $-2,-3,-1,-2,0,-1$. Hence

$$
E[A_iB_j]=\gamma_{-3}+2\gamma_{-2}+2\gamma_{-1}+\gamma_0.
$$

The overlap formula gives exactly these coefficients. This is a constructed arithmetic check of the paper's estimator, not an empirical example reported by the authors. It verifies both the half-open interval convention and the sign of the lead. Swapping the two return series reverses the covariance-lag orientation. If an implementation instead assigns positive lags to this same arrangement, its verbal conclusions about which market leads will be reversed.

The same example illustrates truncation bias concretely. Choosing $K=1$ discards the terms $\gamma_{-3}$ and $2\gamma_{-2}$; their contribution does not vanish merely because the researcher wants only $\gamma_{-1}$. Across many such rows, omitted terms correlated with retained overlap columns alter the least-squares coefficients. Increasing $K$ is useful only while the resulting columns remain sufficiently identified by the observed interval patterns.

For an autocovariance check, the squared return spanning three latent periods has expectation $3\gamma_0+4\gamma_1+2\gamma_2$ under a zero mean. There are three variance terms and twice each unordered pair of distinct increments. This is why symmetric positive and negative lag columns must be combined rather than treated as independent parameters. Under latent white noise the expression reduces to three times the one-period variance, giving a simple units check.

Correlation uncertainty can also be made explicit. Let $a=\gamma_k$, $b=\gamma_0^p$, and $c=\gamma_0^q$, and let $W$ be the joint covariance matrix of their estimates. For $b,c>0$, the gradient of $\rho=a/\sqrt{bc}$ is

$$
g=\left(\frac{1}{\sqrt{bc}},\ -\frac{\rho}{2b},\ -\frac{\rho}{2c}\right)^{\mathsf T}.
$$

A first-order delta-method variance is $g^{\mathsf T}Wg$. Obtaining $W$ requires cross-covariances between the cross-market and own-market moment estimators, since all use some of the same data. Treating the estimated variances as fixed is a simplifying approximation. The article does not print that complete joint implementation, so this formula states the reconstruction requirement rather than asserting how its original program calculated each normalized standard error.

A joint zero-covariance test does not require normalizing every coefficient first. If $R$ selects the six positive-lag coefficients, the Wald statistic is $(R\widehat\gamma)^{\mathsf T}(R\widehat V R^{\mathsf T})^{-1}(R\widehat\gamma)$, with a six-degree-of-freedom chi-square limit under the maintained regularity conditions and full rank. This connects the dependence-aware covariance estimator directly to the reported Table 4 tests.

## Inference: why ordinary OLS standard errors fail

Different products share underlying returns and often observed interval endpoints. Consequently, $e_{ij}$ can be correlated with $e_{gh}$ even when the two regression rows differ. Heteroskedasticity alone is not the whole problem. With $\Sigma=E[ee^{\mathsf T}\mid X]$, Eq. (11) gives

$$
\operatorname{Var}(\widehat\gamma\mid X)
=(X^{\mathsf T}X)^{-1}X^{\mathsf T}\Sigma X(X^{\mathsf T}X)^{-1}.
$$

Appendix B derives the product-error covariance using fourth moments of the latent increments. In the Gaussian case, the fourth-moment decomposition has two surviving covariance pairings after subtracting $E[Y_{ij}]E[Y_{gh}]$:

$$
\operatorname{Cov}(e_{ij},e_{gh})
=\operatorname{Cov}(A_i,A_g)\operatorname{Cov}(B_j,B_h)
+\operatorname{Cov}(A_i,B_h)\operatorname{Cov}(B_j,A_g).
$$

Each component is itself an overlap-weighted sum of estimated auto or cross covariances. This interval-return notation avoids ambiguity in transposing cross-covariance indices. The formula describes the Gaussian pairing part; it is not valid without qualification for arbitrary non-Gaussian data.

For the explicit non-Gaussian derivation, the paper represents both latent return series as moving averages of a common innovation. The covariance then includes a fourth-cumulant contribution involving $\mu_4-3\sigma^4$ and products of the moving-average coefficients. Gaussian innovations make that term vanish. Otherwise, estimating those coefficients and the innovation's fourth moment can be cumbersome. The shared-innovation representation is a strong additional structure used for this analytic derivation, not a prerequisite for constructing the overlap regressors themselves.

The more practical estimator in Eq. (14) is a sandwich that replaces relevant error cross-moments by residual products:

$$
\widehat V=(X^{\mathsf T}X)^{-1}
\left[\sum_{ij}\sum_{gh}x_{ij}x_{gh}^{\mathsf T}
\widehat e_{ij}\widehat e_{gh}\,I_{ij,gh}\right]
(X^{\mathsf T}X)^{-1}.
$$

Here $I_{ij,gh}$ identifies pairs of product errors allowed to be correlated under the maintained dependence structure. It is not merely an indicator that the rows are identical. Constructing its support requires attention to both interval overlap and the retained covariance dependence; a diagonal White estimator would omit shared-return effects. The authors allow this inference support to be shorter than the covariance vector estimated in the first stage. That saves computation but adds an assumption.

In the empirical application, the standard-error calculation assumes only the variance and first-order covariances are nonzero, even when point estimates extend to six or fifteen lags. The tables describe a one-lag/lead window. This choice is particularly important because the index point estimates show dependence beyond one minute. The reported $t$-statistics should be understood as conditional on the authors' inference truncation; robustness to a longer dependence window is not reported.

## Bid–ask and observed-regressor extensions

To distinguish latent equilibrium increments from transaction bounce, let an observed price be

$$
p_i=\pi_{a_i}+b_i\delta,
$$

where $b_i\in\{-1,+1\}$ identifies bid or ask execution and $\delta=S/2$ is a fixed half-spread in the chosen price units. Adjacent observed returns include $(b_{i+1}-b_i)\delta$. If the signs have zero mean, are serially uncorrelated, and are independent of the latent price and observation-time processes, products of same-series observed returns satisfy

$$
E[Y_{ij}]=x_{ij}^{\mathsf T}\gamma+d_{ij}\delta^2,
$$

where $d_{ii}=2$, $d_{i,i+1}=d_{i,i-1}=-1$, and $d_{ij}=0$ otherwise. Add $d$ as a regressor and interpret its coefficient as $\delta^2$; the spread estimate is twice its square root when the coefficient is nonnegative. Its units follow the observed-price representation; one should not call a log-price half-spread a dollar spread without conversion.

This generalizes a Roll-style bounce decomposition to irregular intervals and serially correlated equilibrium increments. It inherits the strong economic restrictions of that decomposition. The paper gives an asymmetric-information market as a counterexample: there can be a positive spread without negative return autocorrelation, in which case this approach may estimate zero spread. The article does not specify an automatic treatment of a negative estimated spread-squared coefficient.

If trade signs are observed, the actual product $(b_{i+1}-b_i)(b_{j+1}-b_j)$ can replace its unconditional expected value as a regressor. The authors state that this accommodates serially correlated signs and dependence on previous prices. That claim still relies on the stated exogeneity of the resulting regression. Expanding observed-return products also generates cross terms between latent increments and sign changes; arbitrary contemporaneous information dependence does not disappear simply because the signs are observed. The note therefore treats this extension as a conditional moment model, not a universal cure for adverse selection.

Additional deterministic or observed regressors can similarly be included only when their conditional moment restrictions are justified. They cannot be added solely because an ordinary least-squares package accepts extra columns.

## S&P 500 empirical design

The data come from ISSM and cover the last quarter of 1993, but the tape supplies only **nineteen complete trading days**. The exact list of days is not printed. Cash-index observations are timestamped at whole minutes; futures observations are timestamped to the second. For each chosen interval the authors retain the last trade or index report. An interval without a transaction is left missing, rather than filled with a zero return.

The analysis uses ten-, five-, and one-minute grids. The generic estimator can use all adjacent raw observations; this empirical implementation first discretizes within those grids, so it does not literally use every within-minute futures transaction. It corrects for missing grid observations while retaining the actual interval lengths between available observations.

The December 1993 futures contract is used before December 15 and the March 1994 contract after December 15. The exact treatment of the rollover date itself is not detailed. Overnight returns are excluded because their covariance structure is unlikely to match intraday returns. The futures trading session is shorter than the index-reporting period, which partly explains unequal observation totals.

The covariance range is six lags in each direction for five- and ten-minute results and fifteen for one-minute results. Tables 1–2 report index observations of 823, 1,619, and 7,989 across the three frequencies, and futures observations of 760, 1,494, and 6,807. The futures missing fractions are printed as 0%, 1%, and 14%; the surrounding prose says approximately 13% at one minute. This small discrepancy is retained as a source discrepancy rather than replaced with an invented exact denominator.

The cash index itself aggregates many constituent prices. Correcting missing observations in the index and futures series does not reconstruct synchronous efficient prices for all 500 underlying stocks. Constituent staleness and heterogeneous information arrival can remain part of the observed index dynamics.

## Numerical findings and their interpretation

The cash index has little significant serial correlation at ten minutes. At five minutes its first autocorrelation is 0.278, with reported $t=5.09$. At one minute the first eight autocorrelations are positive and marked significant: 0.195, 0.176, 0.144, 0.125, 0.094, 0.082, 0.040, and 0.052. Futures autocorrelation is close to zero at five and ten minutes. At one minute it is −0.287 at the first lag, with $t=13.39$, and higher lags are generally insignificant. The authors interpret the negative first lag as likely bid–ask bounce. No formal rejection of every alternative futures-dynamics model follows from the higher-lag nonsignificance.

For the cross-market calculation, set $p$ to the cash index and $q$ to futures. Selected Table 3 correlations are:

| Lag $k$ | Ten-minute grid | Five-minute grid | One-minute grid |
|---|---:|---:|---:|
| −2 | −0.004 | −0.002 | 0.033 |
| −1 | 0.008 | 0.075 | 0.164 |
| 0 | 0.647 | 0.514 | 0.101 |
| 1 | 0.311 | 0.440 | 0.171 |
| 2 | 0.022 | 0.146 | 0.168 |
| 3 | 0.015 | 0.044 | 0.145 |
| 4 | −0.005 | 0.009 | 0.110 |
| 5 | 0.006 | 0.003 | 0.103 |
| 6 | 0.013 | −0.014 | 0.058 |

Positive lags indicate futures leading cash. The ten-minute $k=1$ estimate is 0.311 with $t=4.43$; on the five-minute grid the $k=1,2$ estimates have $t=6.82,3.17$. At one minute, strong positive forward correlations extend over several minutes. The authors summarize the futures lead as at least ten minutes and the reverse cash lead as at most two minutes.

That summary is not a literal statement that every one-minute coefficient through lag ten is significant. Table 3 has insignificant positive estimates at lags eight and ten, and scattered significant entries at eleven and fourteen. It also has an isolated negative estimate at lag −12 with absolute $t=2.40$, despite the broad conclusion of only a short reverse lead. The main directional pattern is clear, but a precise cutoff cannot be read from a contiguous sequence of individually significant coefficients. No familywise multiplicity adjustment is supplied.

Table 4 jointly tests six covariances in each direction with a $\chi^2(6)$ reference, although the caption also calls them Wald “F-statistics.” For negative lags the statistics are 1.01, 6.73, and 99.35 at ten, five, and one minutes; for positive lags they are 20.45, 61.01, and 167.22. The one-minute test covers the first six lags, not all fifteen estimated coefficients. This supports asymmetric transmission with some short reverse dependence at the finest grid.

## Source qualifications and use in research

There is a sign inconsistency in the article's cost-of-carry discussion. Equation (20) states $F_t=S_t\exp[(r-d)(T-t)]$ for a fixed expiry and constant carry. Differencing its logarithm over a forward interval of length $\Delta t$ gives $\Delta\log F_t=\Delta\log S_t-(r-d)\Delta t$. The printed Eq. (21) uses a plus sign. The sign does not change the covariance argument when carry is deterministic, but a replication should derive the drift from the stated pricing relation rather than copy that line uncritically.

The study does not report executable trading returns, costs, capacity, or a portfolio construction exercise. A lead in observed cash-index returns can reflect the mechanics of index construction and information aggregation, and is not by itself a tradable arbitrage after futures move. The authors' interpretation of faster futures information processing is plausible, but the covariance design does not isolate a unique causal mechanism.

For implementation, the most consequential checks are correct lag orientation, interval endpoint conventions, full rank of the overlap matrix, sensitivity to the maximum covariance lag, and standard errors that include correlated product rows. These are distinct from removing bad ticks or deciding how to handle contract rollover and market closures. The source leaves the exact day list, some cleaning choices, drift treatment, and detailed computational support-mask construction unspecified. Those omissions limit exact numerical reproduction but do not prevent reconstruction of the central overlap-regression estimator.
