# Friction in the Trading Process and the Estimation of Systematic Risk

Kalman J. Cohen, Gabriel A. Hawawini, Steven F. Maier, Robert A. Schwartz, and David K. Whitcomb. Journal of Financial Economics 12 (1983), 263–278. Received December 1981; final version February 1983. [Source PDF](<../../Finance/AsynchronousReturns_CohenHawawiniMaierSchwartzWhitcomb_1983.pdf>).

## Why this matters

A stock's estimated beta can change when returns are measured daily, weekly, or monthly even if its underlying exposure to the market is constant. Information reaches observed prices at different speeds. A contemporaneous regression then compares returns that embody different portions of the same underlying market shocks. The resulting error need not always reduce beta: comparatively fast-adjusting securities can have upward-biased estimates while slow-adjusting securities have downward-biased estimates.

This paper models that timing distortion using a finite distributed delay between latent frictionless returns and observed returns. Its main contribution is a covariance conservation identity: adding contemporaneous and lead-lag cross-covariances recovers the covariance of the underlying returns. That identity motivates a multi-lag extension of the Scholes–Williams beta correction and an alternative based on the limiting beta as the return-measurement interval grows.

For empirical factor research, the paper explains why a low daily beta can partly measure slow price adjustment, rather than low economic risk. It also identifies a difficult tradeoff. Adding more lead-lag terms can reduce omitted-delay bias but increase estimation noise. Aggregating over longer intervals reduces timing distortion but leaves fewer observations and exposes the estimate to changes in the underlying beta.

This is a theoretical paper with proofs and comparisons to other estimators. It does not present a new return panel, numerical simulation, table of estimation errors, or trading-strategy backtest. The empirical results mentioned in its motivation belong to separate cited studies, including the authors' 1983 Management Science paper.

## The latent return and delay model

Returns are logarithms of price relatives adjusted for dividends and splits. For security $j$, the latent return is

$$
r_{j,t}=\alpha_j+\beta_jr_{M,t}+e_{j,t}.
$$

The market returns are iid over time. Each residual sequence is iid with zero mean; residuals are independent across securities and independent of market returns. These assumptions imply that true returns from different, nonoverlapping periods have zero covariance. They also keep the true beta invariant to temporal aggregation when the model parameters are constant.

The observed return is a delayed combination of true returns:

$$
r^o_{j,t}=\sum_{n=0}^{N}\gamma_{j,t-n,n}r_{j,t-n}.
$$

The indexing is consequential. The middle index identifies when the true return originated, and the last index identifies its delay before appearing in the observed return. Thus a shock originating at time $s$ contributes $\gamma_{j,s,n}r_{j,s}$ to the observed return at $s+n$. The delay horizon $N$ is finite.

The assumptions on PDF page 4, printed page 266, are:

- Delay variables for different securities are independent, for all originating dates and delay lengths.
- Delay variables are independent of every latent market shock and security residual.
- The expected delay weight at a given lag is constant through time.
- The expected sum of delay weights attached to a latent return is one.

Writing $g_{j,n}=E[\gamma_{j,t,n}]$, the last two conditions give a time-invariant expected delay profile with $\sum_{n=0}^{N}g_{j,n}=1$. The paper interprets the weights as a delay distribution. Its later ordering proposition imposes explicit restrictions on their expected shape. The normalization is in expectation, rather than a requirement that every realized set of weights sums to one.

The model permits complicated dependence among a particular security's delay variables over time. This is important when a day without a trade causes information to accumulate and appear in a later observed return. Cross-security independence is retained, however, and is a substantial restriction: common liquidity interruptions or coordinated trading delays need not satisfy it.

The delays encompass more than the timing of the last transaction within a day. The authors discuss dealers stabilizing quotes or managing inventory and investors updating their decisions and limit orders only intermittently because information, decision, and transaction costs make continuous adjustment costly. Closing quote data would remove some last-trade staleness but would not necessarily remove those broader delays.

Direct bid-ask-spread terms in the authors' earlier friction equation are omitted here. Their stated rationale is that these terms do not enter the cross-covariance and beta results being studied. That simplification should not be read as a general claim that bid-ask effects never influence individual-security variance or finite-sample beta estimation.

## Covariance conservation and its proof

Let $c_{jk}=\operatorname{Cov}(r_{j,t},r_{k,t})$ for $j\ne k$. Independence of delay variables across securities and independence from latent returns imply

$$
\operatorname{Cov}(r^o_{j,t},r^o_{k,t})
=c_{jk}\sum_{n=0}^{N}g_{j,n}g_{k,n}.
$$

The contemporaneous covariance uses only portions of the same latent innovation that arrive at the same observed date. Different delay profiles spread the rest of that covariance across leads and lags.

To make the entire identity reproducible, define

$$
\Gamma_{jk}(h)=
\operatorname{Cov}(r^o_{j,t+h},r^o_{k,t}).
$$

For $h\geq0$,

$$
\Gamma_{jk}(h)=
c_{jk}\sum_{m=0}^{N-h}g_{j,m+h}g_{k,m},
$$

and negative $h$ reverse which security receives the longer delay. Every ordered pair of delay weights appears exactly once when $h$ runs from $-N$ to $N$. Consequently,

$$
\sum_{h=-N}^{N}\Gamma_{jk}(h)
=c_{jk}\left(\sum_ng_{j,n}\right)
\left(\sum_mg_{k,m}\right)
=c_{jk}.
$$

This is Proposition 1 and the core of its appendix proof, PDF pages 13–14. It is a finite-horizon long-run covariance identity. The factorization uses independence between securities' delay variables; it does not require independence of a given security's delay variables across time.

With nonnegative expected delay weights and positive $c_{jk}$, the contemporaneous overlap cannot exceed one. But the beta regression has an observed market variance in its denominator, which is distorted as well. Covariance attenuation alone therefore cannot determine the sign of beta bias.

## The market-index qualification

The paper defines both observed and latent market indices using the same weights:

$$
r^o_{M,t}=\sum_kx_kr^o_{k,t},
\qquad
r_{M,t}=\sum_kx_kr_{k,t}.
$$

It sums Proposition 1 over assets to obtain the security-market covariance identity and then the market variance identity:

$$
\operatorname{Cov}(r_j,r_M)
\approx\sum_{h=-N}^{N}\operatorname{Cov}(r^o_{j,t+h},r^o_{M,t}),
$$

$$
\operatorname{Var}(r_M)
\approx\operatorname{Var}(r^o_M)
+2\sum_{h=1}^{N}\operatorname{Cov}(r^o_{M,t+h},r^o_{M,t}).
$$

The approximation symbols here preserve an explicit qualification in source footnotes 5 and 6. Proposition 1 is established for two different securities. Summing over all index components introduces own-variance terms, for which a security's delay variables generally are not independent. The authors argue these terms become insignificant in a well-diversified index and print the corollaries as equalities.

That is an economic large-portfolio approximation, not an exact consequence of the stated assumptions for an arbitrary finite index. A narrow index, a large constituent weight, or substantial idiosyncratic variance can make the omitted terms matter. The subsequent beta consistency claim inherits this qualification. More observations over time do not by themselves make a fixed large constituent's contribution vanish.

An exact expression for the difference can be constructed by defining

$$
d_j=\sum_{h=-N}^{N}
\operatorname{Cov}(r^o_{j,t+h},r^o_{j,t})
-\operatorname{Var}(r_{j,t}).
$$

Then the security-market long-run covariance differs from its true counterpart by $x_jd_j$, and the market long-run variance differs by $\sum_jx_j^2d_j$, provided the cross-security identities hold. This decomposition is derived here to expose the scope of the source's approximation; the paper does not estimate these unknown corrections.

## The multi-lag beta estimator

Let $V_M^o=\operatorname{Var}(r_M^o)$. Define population regression slopes

$$
\beta_j^o=
\frac{\operatorname{Cov}(r^o_{j,t},r^o_{M,t})}{V_M^o},
\qquad
\beta_{j,h}^o=
\frac{\operatorname{Cov}(r^o_{j,t+h},r^o_{M,t})}{V_M^o},
$$

and market serial slopes

$$
\rho_M(h)=
\frac{\operatorname{Cov}(r^o_{M,t+h},r^o_{M,t})}{V_M^o}.
$$

With stationarity, $\rho_M(h)=\rho_M(-h)$. Proposition 2 rearranges the preceding identities into

$$
\beta_j^o
=\beta_j\left(1+2\sum_{h=1}^{N}\rho_M(h)\right)
-\sum_{h=1}^{N}
\left(\beta_{j,h}^o+\beta_{j,-h}^o\right),
$$

subject to the index-diversification approximation. Solving for the latent beta gives the correction. In sample notation, equation (5) is

$$
\widehat\beta_j=
\frac{b_j^o+\sum_{h=1}^{N}(b_{j,h}^o+b_{j,-h}^o)}
{1+\sum_{h=1}^{N}(b_{M,h}^o+b_{M,-h}^o)}.
$$

Each $b$ is a slope from a separate simple OLS regression with an intercept. The numerator is not a sum of partial coefficients from a single multiple regression containing every market lead and lag. Correlation among the regressors makes those coefficients different objects.

The source retains separately estimated market lead and lag slopes because finite-sample endpoint conventions may use slightly different sets of observations. In population the two slopes agree. A practical implementation should document common-date alignment, centering, the observations discarded at each endpoint, and how the denominator is constructed.

An equivalent way to implement the population correction is to sum sample cross-covariances and divide by the corresponding sum of market autocovariances, using a common normalization and sample window. This makes the long-run covariance interpretation clear. If separate OLS regressions use different market variances, their sum is not numerically identical to a common-denominator covariance calculation in finite samples.

For $N=1$, the formula reduces to the Scholes–Williams expression: the sum of lagged, contemporaneous, and leading simple slopes divided by one plus twice the market's first-order serial correlation. With delay horizons longer than one period, omitting higher-order terms generally leaves a nonzero population distortion.

Consistency also requires sample moments to converge. The source allows dependence among a security's delay variables, but constant first moments alone are not a complete ergodicity or mixing assumption. A reproduction should assume or assess enough weak dependence for the estimated covariances to converge, along with a nonzero long-run market variance. Standard iid OLS standard errors are not automatically valid for the ratio of many correlated estimated slopes.

## Increasing the measurement interval

Proposition 4 concerns nonoverlapping returns aggregated over $L$ elementary periods. Because returns are logarithmic, aggregation is addition. With a finite delay horizon, the proportion of a long block affected by shocks crossing its endpoints declines as the block length grows. Expected weight on the contemporaneous aggregated return approaches one, while expected weights on other aggregated periods approach zero. The observed beta therefore approaches the latent beta under the same model and index assumptions.

The paper suggests estimating betas at several interval lengths and fitting a function with an asymptote. The asymptote estimates the long-interval beta. It does not specify in this article a unique regression function, a grid of intervals, weights for the second-pass regression, or an estimator of its uncertainty. Those details belong to implementation and to the separate empirical paper, not to a fully defined algorithm here.

There are two limits to distinguish. Increasing $L$ reduces population timing bias. Obtaining a statistically consistent estimate at that $L$ also requires enough nonoverlapping blocks. In a fixed history of $T$ elementary observations, there are only about $T/L$ blocks. Letting $L$ grow without extending the historical span eventually destroys estimation precision. The source's notation for an asymptotic estimator should not be interpreted as a prescription to estimate a regression with one enormous observation.

A useful derived expression makes the boundary argument explicit. For stationary observed series, the covariance of two length-$L$ sums is

$$
\operatorname{Cov}(R^o_j(L),R^o_M(L))
=\sum_{h=-(L-1)}^{L-1}(L-|h|)\Gamma_{jM}(h).
$$

If the relevant covariance sequence vanishes beyond $N$ and $L>N$, this equals $LA-B$, where $A=\sum_h\Gamma_{jM}(h)$ and $B=\sum_h|h|\Gamma_{jM}(h)$. The market variance similarly equals $LD-E$. Hence the population aggregated slope is

$$
\beta_j^o(L)=\frac{LA-B}{LD-E},
\qquad
\lim_{L\to\infty}\beta_j^o(L)=\frac{A}{D}.
$$

This derivation requires the finite-support covariance condition, including treatment of own-index contributions; it is not a claim that arbitrary dependent random delays imply that condition for every individual autocovariance. For this special case, the derivative beyond the delay horizon has sign determined by $BD-AE$. The convergence is monotone wherever the denominator stays positive. The paper's broader introductory language about monotonic convergence should not replace a check of the conditions or be generalized to every finite-sample sequence of estimated betas.

## Cross-sectional bias and relative delay

Proposition 5 states that the index-weighted average observed beta equals one:

$$
\sum_jx_j\beta_j^o=1.
$$

This follows directly by summing the covariance numerators when the index uses those same weights. The true betas also average to one against the corresponding latent index. Therefore their weighted distortions sum to zero. It does not follow that every stock's beta is unbiased, that the unweighted mean bias is zero, or that positive and negative distortions have equal magnitudes.

The paper defines security $j$ to have cumulatively greater expected delay than $i$ when

$$
\sum_{n=p}^{N}g_{j,n}>
\sum_{n=p}^{N}g_{i,n},
\qquad p=1,\ldots,N.
$$

This is a strict ordering of every tail of the expected delay distribution. Proposition 6 further requires every security's expected delay weights to decrease with lag, with at least one strict decrease; securities $i$ and $j$ must otherwise have equal true betas, equal index weights, and the same covariances with other securities. Their relevant covariances must be positive. Under these restrictions, the more delayed security has a smaller observed beta.

The restrictions are part of the result. It is not a general theorem that a smaller firm must have a smaller observed beta, nor does a comparison between two securities alone establish that either beta lies above or below its true value. The argument connects a relative delay ordering to a relative distortion when the other determinants are held fixed.

For a clean proof, let

$$
\Delta_p=\sum_{n=p}^{N}(g_{j,n}-g_{i,n})>0.
$$

For another security $k$, summation by parts gives

$$
\sum_{n=0}^{N}g_{k,n}(g_{i,n}-g_{j,n})
=\sum_{p=1}^{N}(g_{k,p-1}-g_{k,p})\Delta_p>0.
$$

Thus the faster security's expected delay profile has greater contemporaneous overlap with every decreasing $g_k$. Multiplying by positive index weights and positive latent covariances produces the ordering in observed betas.

The appendix's PDF page 15 writes several intermediate expressions as if the single-security bracket being rearranged were already the full beta difference. The preceding equation (A.1) includes a negative covariance-weighted prefactor. Keeping that prefactor separate avoids an apparent sign contradiction: the bracket is positive, and its contribution to $\beta_j^o-\beta_i^o$ is negative. The displayed summation-by-parts identity above is a reconstruction of that step, not an official erratum.

## A small numerical diagnostic

The following example is derived for verification and is not a reported experiment. Let all latent returns equal the same iid zero-mean market innovation of unit variance. Half the index weight belongs to a fast group with observed return $r_t$; the other half belongs to a slower group with observed return $(r_t+r_{t-1})/2$. Deterministic weights satisfy the delay-independence conditions, and every true beta is one.

The observed market return is $0.75r_t+0.25r_{t-1}$, with variance 0.625 and first-order autocovariance 0.1875. Its autocorrelation is 0.3. The contemporaneous observed betas are 1.2 for the fast group and 0.8 for the slow group. Their equal-weighted average is one, although both are distorted.

For either group, the sum of contemporaneous, leading, and lagging covariance slopes is $1/0.625=1.6$. Dividing by $1+2(0.3)=1.6$ restores the true beta of one. Omitting the denominator would incorrectly produce 1.6.

At interval length $L\geq1$, the two population betas are

$$
\beta_{\rm fast}^o(L)=\frac{L-0.25}{L-0.375},
\qquad
\beta_{\rm slow}^o(L)=\frac{L-0.50}{L-0.375}.
$$

At $L=5$ these are approximately 1.0270 and 0.9730; at $L=20$, approximately 1.0064 and 0.9936. Even a one-period delay leaves a diminishing boundary effect in longer-period returns. The example verifies the correction and aggregation logic without attributing invented performance numbers to the paper.

## Relation to existing estimators and implementation choices

The Scholes–Williams estimator is recovered when only one lead and lag are relevant. Cohen and coauthors emphasize that the earlier model assumes enough trading within each measurement period to confine the spillover to adjacent observations. A longer price-adjustment mechanism can require additional lags even when a stock trades daily.

The paper criticizes the unnormalized sum associated with Dimson's original derivation and notes that multiple-regression partial slopes do not equal its own simple-regression covariance ratios. That is the authors' claim within their framework; it should not be broadened to say every subsequent distributed-lag beta method is invalid. Their discussion also notes Dimson's response that the empirical bias in his earlier estimator was small and cites an alternative form.

For an implementable study, specify the observation frequency, adjustment convention, index construction, universe, return window, missing-observation policy, and maximum delay $N$. Compute the separate slopes on clearly aligned dates, construct the corrected ratio, and compare it with ordinary contemporaneous OLS and the one-lag correction. Vary $N$ to display sensitivity, rather than treating one undocumented horizon as known.

The alternative interval-extrapolation study requires a nonoverlapping aggregation rule, a chosen interval grid, a functional form for the asymptote, and an uncertainty method that recognizes estimates at different interval lengths are generated from the same history. A block bootstrap or a suitable joint moment calculation could supply inference, but neither is specified in the source.

The article's motivating observations are qualitative: related empirical work finds bias persisting for intervals extending several weeks, a relationship between beta distortion and market capitalization, and upward bias among some large issues versus downward bias among thinner issues. This paper provides no sample counts, regression coefficients, standard errors, or exact numerical effect sizes for those observations. It also provides no transaction-cost or net-performance calculation.

The main practical limitation is identification. Delay profiles are latent, and the observed lead-lag covariances can also reflect genuine information diffusion, changing exposures, common liquidity, or serial dependence in true returns. Correcting every observed lag as if it arose from measurement timing risks removing economically meaningful dynamics. The source model separates these mechanisms by assumption.

## Source map

PDF pages 1–3 motivate the interval effect and discuss longer-lived adjustment. Pages 4–5 specify assumptions and the delay equation. Pages 6–8 give the covariance identities, their diversification footnotes, and the corrected estimator. Pages 9–10 state the interval-limit and cross-sectional propositions. Pages 11–12 compare Scholes–Williams and Dimson. Page 13 concludes and begins the appendix; pages 14–15 complete both proofs. Page 16 contains references. The entire local article, including the appendix, was used for this note.
