# Hedge Fund Tail Risk: An Investigation in Stressed Markets

**Authors:** Monica Billio, Lorenzo Frattarolo, Loriana Pelizzon. **Publication:** *The Journal of Alternative Investments*, Spring 2016, pp. 109-124. **Source:** `Finance/SystemicRiskTailRisk_BillioFrattaroloPelizzon_2016.pdf`, 17 PDF pages. The complete article was read and its image-based empirical exhibits inspected visually. The authors' [extended version and technical appendix](https://www.unive.it/web/fileadmin/user_upload/dipartimenti/DEC/doc/Pubblicazioni_scientifiche/working_papers/2016/WP_DSE_billio_frattarolo_pelizzon_01_16.pdf), dated 7 November 2016, was also checked for the model and differentiation details. Numerical results below refer to the supplied journal article.

## Contribution and the economically relevant finding

The paper develops a regime-dependent system for measuring the contribution of hedge-fund strategies to portfolio volatility, value-at-risk, and expected shortfall. Its contribution is to estimate state-dependent exposures and state probabilities using Markov switching rather than asking a risk controller to supply subjective crisis scenarios and probabilities. The empirical application asks whether strategies that appear to diversify an equity portfolio also protect a portfolio of hedge-fund strategies against joint extreme losses.

The important finding is that market beta is an incomplete description of that protection. Dedicated short bias naturally offsets equity-market exposure, but its exposure to other common risks, especially credit and liquidity-related stress, can reduce its hedge value. Convertible arbitrage and equity market neutral can contribute little to ordinary volatility while still contributing positively to tail losses. Emerging-markets strategies are substantial risk contributors across the reported measures.

The paper's most sweeping prose says that all strategies lose their hedging value during crisis periods. The tabulated averages support a more qualified conclusion. Dedicated short bias remains a negative contributor to portfolio VaR and expected shortfall on average even in the specified crisis subsample, although its contribution becomes far less negative in the multifactor model. The monthly plots can exhibit individual periods with little or reversed protection. The supported statement is that hedge effectiveness is state dependent and can deteriorate sharply; it is not that every displayed crisis-period average shows zero or negative diversification benefit.

This distinction matters for asset allocation. A manager should examine the portfolio's conditional tail composition, not assume that a negative stock-market beta guarantees protection from every crisis mechanism. But the paper does not establish that short-biased strategies can never hedge a crisis, nor does it provide an optimized investable allocation. The empirical portfolio is an equally weighted combination of eight strategy indexes.

## Data and experimental timing

The data are monthly aggregate hedge-fund strategy-index returns from the Dow Jones Credit Suisse database, January 1994 through December 2011. The full sample has 216 observations per strategy. The eight selected equity-related indexes are convertible arbitrage, dedicated short seller or short bias, emerging markets, equity market neutral, long-short equity, distressed, event-driven multi-strategy, and risk arbitrage.

The database description reports asset-weighted indexes of funds meeting a minimum of US\$50 million in assets, a one-year track record, and current audited financial statements. Returns are net of fund fees. Index constituents are rebalanced monthly and the fund universe is revised quarterly. New funds enter prospectively, which is intended to reduce instant-history bias; closed funds can remain represented. These features mitigate some selection problems but do not make an index a directly investable portfolio or eliminate every reporting and valuation bias.

The experiment uses expanding estimation windows. The first 132 monthly observations, January 1994 through December 2004, estimate parameters available at the end of 2004. Forecasts then cover January 2005. Each step adds one observation and repeats estimation and forecasting through December 2011, yielding 84 months of evaluation. An expanding window gives increasing statistical precision under parameter stability, but also retains old regimes even when the hedge-fund industry changes.

The full-sample parameter tables use all 216 observations and therefore are descriptive fits, not the parameter estimates available for each historical forecast. They should not be substituted into the out-of-sample exercise. Forecast state probabilities, filtered using available data and advanced through the transition mechanism, are likewise different from probabilities smoothed using future observations. Using the latter in a historical forecast would introduce look-ahead information.

The benchmark portfolio holds one eighth of its capital in each strategy index. There is no optimized weight selection, trading-cost model, redemption constraint, lockup simulation, or additional fund-of-funds fee layer. The paper acknowledges that an actual fund of funds invests in individual managers and faces a different fee and investment structure. Its results concern risk representation at the strategy-index level, not a directly demonstrated implementable performance improvement.

## Risk factors and the two model specifications

The S&P-RSM specification has only the S&P 500 total-return factor. The MF-RSM adds a broader collection of factors from Datastream, apart from momentum, which comes from Kenneth French's website. Exhibit 1 defines the factors, and its details matter because similar-sounding labels can refer to different signed series.

The equity-style factors use the monthly return difference between Russell 2000 and Russell 1000 indexes and the difference between Russell 1000 Value and Growth indexes. The table labels the first “Large-Small” while its verbal definition lists the small-cap index first; a reproduction must resolve that sign against the underlying series rather than infer it from the label. Currency exposure is represented by the Bank of England value-weighted U.S. dollar index.

Fixed-income and emerging-market variables include the Barclays U.S. Aggregate Government/Credit return, a term spread defined from ten-year Treasury and three-month Treasury-bill yields, a credit-spread variable defined from Moody's BAA and AAA corporate bond indexes, the MSCI Emerging Markets stock return, and the Barclays Emerging Markets bond return. The remaining factors are the UMD momentum return and the monthly change in VIX. The table's credit-spread wording and its distinction between levels and monthly transformations require careful replication documentation.

The two models can be written using the journal's exhibit notation as

$$
r_{i,t}=\alpha_i(Z^i_t)+\sum_{j=1}^J\beta_{ij}(S_t)F_{j,t}+\omega_i(Z^i_t)\varepsilon_{i,t}.
$$

The common market regime $S_t$ has two states identified from the S&P 500: lower-volatility normal conditions and higher-volatility down-market conditions. The strategy-specific chain $Z^i_t$ captures two idiosyncratic volatility regimes. Factor exposures depend on the market state, while the intercept and idiosyncratic volatility depend on the strategy-specific state. This separates changes in systematic exposure from shifts in unexplained strategy risk.

The appendix specifies Gaussian innovations, independent market and strategy-specific chains, and Hamilton filtering with quasi-maximum-likelihood estimation. Forecast chain probabilities follow from filtered probabilities and transition matrices. Combining each strategy's two idiosyncratic states with the common two-state market process gives four conditional components per strategy. These details were verified in the [technical appendix](https://www.unive.it/web/fileadmin/user_upload/dipartimenti/DEC/doc/Pubblicazioni_scientifiche/working_papers/2016/WP_DSE_billio_frattarolo_pelizzon_01_16.pdf); they do not supply every numerical optimization setting.

For eight strategies, two states per strategy and two common market states generate $2^9=512$ joint configurations. Within each configuration, portfolio means and covariances follow from the strategy model and weights. Mixing over configurations produces a potentially skewed, heavy-looking return distribution even when every state component is Gaussian. A finite Gaussian mixture has Gaussian-type ultimate tails; “fat tails” here describes departures from a single normal at the horizons and probabilities studied, not a proven power-law asymptotic tail.

## From state distributions to portfolio VaR and expected shortfall

Let $p_s$ be the forecast probability of state $s$, and let the conditional portfolio return be normal with mean $\mu_s$ and standard deviation $\sigma_s$. The predictive return distribution is

$$
F_P(x)=\sum_s p_s\Phi\left(\frac{x-\mu_s}{\sigma_s}\right).
$$

For the five-percent lower-return tail, solve $F_P(q)=0.05$ numerically. The journal labels its reported risk levels “95%,” but prints VaR and ES as negative returns. Thus $q$ is a lower-tail return quantile. A positive loss VaR would be $-q$. Keeping that sign convention explicit prevents interpreting a more negative reported VaR as less risk.

The expected shortfall in return units is

$$
e=\frac1\alpha\sum_s p_s\left[\mu_s\Phi(z_s)-\sigma_s\phi(z_s)\right],
\qquad z_s=\frac{q-\mu_s}{\sigma_s},\quad\alpha=0.05.
$$

This is the Gaussian-mixture integral underlying journal equation (5). It averages the entire lower-tail loss region rather than only locating its boundary. The same portfolio can have a relatively moderate quantile but very negative expected shortfall if a low-probability regime generates unusually severe outcomes beyond that quantile.

Neither a mixture VaR nor a mixture ES is obtained by simply averaging each regime's individual VaR or ES at the same probability level. The common mixture threshold $q$ determines how much mass from each component belongs to the overall tail. A high-volatility state can receive much more weight within that tail than its unconditional forecast probability suggests. This is why common stress exposures can matter disproportionately for marginal tail risk.

A separate distinction concerns volatility. The standard deviation of the full mixture is determined by

$$
\operatorname{Var}(R_P)=\sum_s p_s(\sigma_s^2+\mu_s^2)-\left(\sum_s p_s\mu_s\right)^2.
$$

Appendix B.2 explicitly forecasts volatility by averaging state standard deviations with forecast state probabilities. That statistic differs from the full mixture standard deviation because it omits nonlinear aggregation and dispersion of state means. The formula above is an explanatory probability identity; matching the authors' volatility forecasts requires their stated probability-weighted average instead.

## The portfolio perturbation and marginal-risk derivatives

The paper considers a financed reallocation toward strategy $i$. Starting with portfolio $P$, construct

$$
R_{P'}(w)=wR_i+(1-w)R_P.
$$

Then evaluate the derivative at $w=0$. This increases strategy $i$ while proportionally reducing the existing portfolio, including its existing holding in strategy $i$. It is not the same as adding an unfinanced unit of the strategy while holding every other position constant.

In state $s$, define the directional changes

$$
a_s=\mu_{i,s}-\mu_{P,s},\qquad
b_s=\rho_{iP,s}\sigma_{i,s}-\sigma_{P,s}.
$$

The mean derivative is $a_s$, and equation (4) gives the volatility derivative $b_s$. A high standalone strategy volatility does not automatically imply a positive $b_s$: sufficiently low or negative correlation with the portfolio can offset it. Conversely, a low-volatility strategy can increase portfolio risk if its covariance is large relative to the risk of the portfolio being displaced.

The exact state variance along the perturbation is

$$
\sigma_{P',s}^2(w)=w^2\sigma_{i,s}^2+(1-w)^2\sigma_{P,s}^2+2w(1-w)\operatorname{Cov}(R_i,R_P\mid s).
$$

Differentiating its square root at zero yields the preceding $b_s$. This derivation shows why the portfolio's original volatility is subtracted. Omitting that term changes the question from a financed allocation shift to an unfinanced marginal holding contribution.

For mixture quantiles, differentiating the defining identity $\sum_s p_s\Phi(z_s)=\alpha$ while holding forecast state probabilities fixed gives the internally consistent formula

$$
q'=
\frac{\sum_s p_s\phi(z_s)\sigma_s^{-1}(a_s+z_sb_s)}
{\sum_s p_s\phi(z_s)\sigma_s^{-1}}.
$$

This follows because $z'_s=(q'-a_s-z_sb_s)/\sigma_s$. The printed expression in journal equation (7), repeated in the extended appendix, displays a minus sign before the $z_sb_s$ term. Under the definitions printed in the same source, implicit differentiation gives a plus sign. A direct finite-difference check of the mixture quantile is therefore essential; the displayed derivative should not be copied into code without verification.

For expected shortfall, differentiating the integral and using the quantile constraint simplifies to

$$
e'=\frac1\alpha\sum_s p_s\left[a_s\Phi(z_s)-b_s\phi(z_s)\right].
$$

Terms involving $z'_s$ cancel because their common coefficient is the portfolio threshold and the derivative of total tail probability is zero. These equations are explanatory derivations from the article's mixture setup. If one reports positive loss risk, the corresponding derivatives are $-q'$ and $-e'$. Sign comparisons must therefore distinguish return quantiles, positive losses, and normalized contribution percentages.

## Percentage contributions require an additional convention

The reported exhibits present percentage contributions that approximately sum to one hundred across strategies. The financed perturbation derivatives described above do not themselves have that property. If the original portfolio has weights $x_i$, the weighted sum of its financed directions is zero, so their weighted risk derivatives also sum to zero for a differentiable risk function.

For a degree-one homogeneous risk measure $\mathcal R(x)$, an ordinary Euler contribution is $x_i\partial_i\mathcal R$, and these contributions sum to total risk. If $D_i$ denotes the financed direction derivative toward strategy $i$, then

$$
D_i=\partial_i\mathcal R-\mathcal R,
\qquad
\frac{x_i\partial_i\mathcal R}{\mathcal R}
=x_i\left(1+\frac{D_i}{\mathcal R}\right).
$$

This gives one coherent bridge between the two objects, but the supplied main text does not clearly spell out the exact normalization used in each percentage table. The distinction should remain explicit until code or further implementation details are available. It also means that the prose interpretation of a minus twenty-percent marginal contribution as the exact risk reduction from completely removing a strategy is too strong. An infinitesimal derivative is a local slope; a finite removal requires recomputing the entire portfolio risk.

The practical approach is to report the raw directional derivative, the positive-loss sign convention, and any normalized Euler contribution separately. Then check each against a small finite reallocation and verify whichever adding-up identity is intended. This prevents a seemingly plausible percentage attribution from answering a different portfolio question than the one the investor asked.

## Numerical evidence from the exhibits

Exhibit 2 shows strong nonnormality in several monthly strategy returns. Convertible arbitrage has reported skewness minus 2.55 and kurtosis 15.46. Equity market neutral has skewness minus 11.99, kurtosis 164.07, and a minimum monthly return of minus 40.45 percent. Emerging markets has monthly standard deviation 4.33 percent and minimum return minus 23.43 percent. These observations motivate attention to tail behavior, but also mean that a handful of extreme observations can heavily influence regime identification in a 216-month sample.

For the S&P-only model over January 2005-December 2011, Exhibit 5 reports dedicated short seller contributions of minus 16.31 percent to volatility, minus 64.03 percent to VaR, and minus 67.62 percent to ES. Emerging markets contributes 89.20, 104.56, and 98.21 percent, respectively. Contributions can exceed one hundred because negative contributions elsewhere offset them. These are attribution percentages, not standalone returns or standalone loss probabilities.

The multifactor estimates in Exhibit 6 show a substantially weaker tail hedge from short bias. Full-period contributions are minus 12.93 percent to volatility, minus 30.30 percent to VaR, and minus 41.93 percent to ES. Emerging markets contributes 92.79 percent of volatility attribution but 52.46 percent of VaR and 59.57 percent of ES. Thus adding factors redistributes tail-risk attribution rather than uniformly increasing every strategy's percentage share.

The multifactor model also demonstrates why standalone risk and portfolio contribution differ. Dedicated short seller has standalone forecast VaR minus 15.02 percent and ES minus 18.27 percent in the full-period table, yet negative portfolio tail contributions. Emerging markets has lower standalone tail-loss magnitudes, minus 7.03 and minus 9.45 percent, but positive and large portfolio contributions. The allocation question depends on the joint distribution and the portfolio being displaced.

Convertible arbitrage has a full-period multifactor volatility contribution of minus 3.08 percent but VaR and ES contributions of plus 1.23 and plus 1.20 percent. Equity market neutral similarly has volatility contribution minus 1.33 percent and positive VaR and ES contributions of 1.76 and 1.21 percent. These are direct examples of strategies that diversify dispersion while adding to modeled downside-tail risk.

## Crisis subsamples and source inconsistencies

The actual exhibit panels label the pre-Lehman subsample January 2005-November 2008, the meltdown subsample December 2008-June 2009, and the post-Lehman period July 2009-December 2011. These boundaries differ from the surrounding prose, which initially describes a split around July/August 2008. They also place the September 2008 failure within the panel called pre-Lehman. Reproduction should use the printed panel dates when matching those numbers and separately test economically motivated alternative dates.

In Exhibit 6, dedicated short seller's ES contribution weakens from minus 49.41 percent in the pre-Lehman panel to minus 14.97 percent in the meltdown panel, before returning to minus 37.24 percent afterward. Its VaR contribution moves from minus 35.58 to minus 7.87 and then minus 27.93 percent. Its volatility contribution changes from minus 16.10 to plus 1.43 and then minus 11.77 percent. The crisis panel therefore shows a loss of volatility hedging and sharply reduced, but still negative average, tail contributions.

The monthly plots in Exhibits 7-9 add timing information. They show diminished negative contributions around the crisis and occasional positive contributions, including some months for dedicated short bias. Long-short equity and distressed strategies contribute relatively more to tail measures than to volatility. These plots support time variation that whole-period averages conceal, but they are model-based forecast-attribution paths rather than directly observed causal contributions to realized losses.

Several narrative figures also differ from the visually inspected tables. For instance, the prose beside Exhibit 5 cites dedicated-short contributions that do not match that exhibit's Panel A. The reliable approach is to state exactly which table and panel supplies each number, as done here, instead of blending prose and table values into a supposedly exact result. These discrepancies are limitations of the source's presentation, not evidence that the qualitative mechanism is absent.

## Reproducibility boundaries and conclusions

The model can be reconstructed at the architectural level from the supplied equations, factors, state definitions, sample window, and portfolio design. Exact numerical replication still requires estimation choices the article says are available on request: initialization, optimizer settings, constraints, handling of local maxima, labeling of states across successive fits, factor covariance treatment, and the percentage-contribution normalization. A research implementation should preserve those choices in a run record rather than claim that the paper fully specifies them.

A useful verification sequence is to compare full-sample descriptive moments, fit the common market regime, fit strategy-specific models, form the 512 component distributions, calculate mixture quantiles and tail integrals, and check analytic derivatives against finite differences. Forecast comparisons must then repeat estimation using each expanding window. The VaR root should satisfy the mixture probability equation numerically, and ES should be no greater than the lower-return VaR in the return convention. Violations indicate a sign, integration, or probability-normalization error.

The paper offers an economically useful warning: exposure to a market index cannot summarize every mechanism through which hedge-fund strategies lose together. Risk contributions can change more dramatically in tails than in ordinary volatility, and diversification inferred from normal states may weaken when common non-equity exposures dominate. The evidence supports examining credit and liquidity-related common exposures and state-dependent attribution. It does not establish a universal failure of all hedges or a fully validated systemic-causality model. Its most usable output is the joint-distribution and marginal-reallocation framework, accompanied by careful treatment of the source's conventions and incomplete implementation details.

## What the mixture adds, and how to test the claimed hedge mechanism

The mixture model distinguishes three sets of state weights that answer different questions. The forecast probabilities $p_s$ describe how likely each regime is before observing the next return. Conditional on a portfolio return lying below the mixture VaR, the posterior state probability becomes

$$
\Pr(s\mid R_P\leq q)=\frac{p_s\Phi(z_s)}{\alpha}.
$$

Conditional on a return near the quantile boundary, the corresponding density weights are proportional to $p_s\phi(z_s)/\sigma_s$. These are the weights that appear in the quantile derivative. The distinction explains why a strategy's contribution to volatility, VaR, and ES can disagree without any inconsistency: the measures emphasize different portions of the predictive distribution and different effective combinations of states.

For example, a low-probability state can dominate ES if its mean is sufficiently negative or its volatility sufficiently high. Increasing a strategy's exposure to that state can worsen average losses beyond the threshold even if it has little effect on ordinary forecast variance. A different state can have high density near the VaR boundary and strongly affect the quantile derivative while contributing relatively little to the deepest losses. These are mathematical consequences of the mixture setup, not new empirical estimates. They give a concrete interpretation of why the article's volatility attribution is not a sufficient proxy for its tail attribution.

The funded perturbation also has a useful practical scale. With eight equal portfolio weights, shifting a fraction $w$ from the existing portfolio into strategy $i$ changes its own weight from one eighth to one eighth plus seven eighths of $w$, while every other weight falls by one eighth of $w$. A one-percentage-point perturbation therefore increases the target strategy by 0.875 percentage points, not by a full percentage point. Risk changes predicted by a derivative must be interpreted using that exact financing direction.

An implementation can verify this by evaluating risk at small positive and negative perturbations, such as one tenth of a percentage point in $w$, then comparing the central finite difference with the analytic formula. It should repeat the comparison at several step sizes to distinguish truncation error from numerical error in quantile root finding. For a larger proposed reallocation, recompute the mixture distribution directly rather than extrapolating the local derivative. This is particularly important when state probabilities put substantial density near the chosen loss threshold.

The empirical attribution to credit and liquidity mechanisms remains model dependent. The paper compares a market-only specification with a richer factor set, but does not randomize exposures or identify an exogenous shock that isolates a causal liquidity channel. Several factors can co-move during crises, and changing the factor set can redistribute fitted coefficients. The correct evidentiary statement is that a model incorporating additional common risk variables materially changes inferred tail contributions, consistently with the authors' mechanism. It is stronger than the evidence to assign every residual hedge failure uniquely to liquidity.

Forecast calibration would provide another important layer of evaluation. Across 84 monthly forecasts, a five-percent VaR should produce only about 4.2 violations on average under calibration. That is a small number for distinguishing competing tail models, particularly when crisis observations cluster. The article focuses on evolving estimated contributions rather than presenting a comprehensive exceedance-coverage and expected-shortfall backtest. Its use of future forecast dates demonstrates an information-timing design, but does not by itself prove that forecast tail probabilities are statistically accurate. The contribution estimates are most credible when accompanied by both distributional calibration and stability checks on factor specification and regime identification.

For use in allocation meetings, the most informative presentation would show the portfolio's actual weights, the forecast state probabilities, the raw reallocation derivative, and the associated finite-change stress result together. A percentage contribution alone obscures the financing convention and can magnify apparently dramatic movements when the denominator, total measured risk, is small.
