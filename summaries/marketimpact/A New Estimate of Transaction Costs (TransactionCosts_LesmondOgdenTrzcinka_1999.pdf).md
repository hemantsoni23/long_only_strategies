# A New Estimate of Transaction Costs

David A. Lesmond, Joseph P. Ogden, and Charles A. Trzcinka, *The Review of Financial Studies* 12(5), Winter 1999, pp. 1113–1141.

Source: [TransactionCosts_LesmondOgdenTrzcinka_1999.pdf](../../Finance/TransactionCosts_LesmondOgdenTrzcinka_1999.pdf). The local PDF has 30 pages, including a ResearchGate cover; journal page 1113 is PDF page 2. References below use journal pages. This note covers the entire article, its appendix, and the displayed tables and figures. It describes the published historical experiment, not current transaction-cost levels.

## Why this matters and what the paper contributes

The paper estimates a stock’s effective round-trip trading-cost threshold from daily stock and market returns, without requiring an observed bid–ask spread or a trade-direction classification. Its identifying observation is that many daily returns are exactly zero. If information is worth less than the cost of acting on it, the marginal informed trader does not trade to incorporate that information into the price. A wider region of inaction produces more zero returns, conditional on the size of market movements and the stock’s residual volatility.

The innovation is a limited-dependent-variable model that jointly estimates market exposure, residual volatility, and separate negative- and positive-information thresholds. The zero observations contribute probability masses to the likelihood; nonzero observations contribute shifted normal densities. Consequently, the estimator uses substantially more information than the unconditional percentage of zero-return days. It is also different from the Roll estimator, which identifies effective spread through first-order return autocovariance.

This is useful for historical or international research where daily return series exist but reliable quotes do not. A researcher can obtain a stock-year friction estimate and compare anomalies, universes, or liquidity regimes using one statistical specification. The article’s validation supports that application: its estimates track quoted spreads and spread-plus-commission measures strongly. However, neither the likelihood nor those correlations identify the cost of executing a particular institutional order, its market impact as a function of size, or its optimal schedule. The quantity estimated is an economically interpreted threshold facing the marginal information trader.

The main sample covers NYSE and AMEX stocks during 1963–1990. The reported mean round-trip cost declines from 10.35% in the smallest combined size decile to 1.23% in the largest. These are historical percentages of value traded, not basis points, and the smallest-decile table has an internal arithmetic inconsistency discussed below. The model should be understood before treating those headline numbers as usable calibration targets.

## Economic mechanism and observation equation

For stock $j$ on trading day $t$, let $R_{jt}$ be the measured daily return, $R_{mt}$ the equally weighted market return, and $R^*_{jt}$ the latent return implied by information before the friction filter. The paper specifies, on pp. 1120–1122,

$$
R^*_{jt}=\beta_jR_{mt}+\epsilon_{jt},\qquad \epsilon_{jt}\sim N(0,\sigma_j^2).
$$

The likelihood treats the daily residuals as independent, with constant parameters within the estimation year. Contemporaneous market information enters through $\beta_jR_{mt}$. Firm-specific information and market information not captured by the contemporaneous index are absorbed into $\epsilon_{jt}$. The authors discuss accumulated information as an economic interpretation; the fitted model does not explicitly maintain a dynamic state containing unincorporated news.

Define lower and upper thresholds $\alpha_{1j}<\alpha_{2j}$, interpreted economically as $\alpha_{1j}<0<\alpha_{2j}$. The observed return is

$$
R_{jt}=
\begin{cases}
R^*_{jt}-\alpha_{1j},&R^*_{jt}<\alpha_{1j},\\
0,&\alpha_{1j}\le R^*_{jt}\le\alpha_{2j},\\
R^*_{jt}-\alpha_{2j},&R^*_{jt}>\alpha_{2j}.
\end{cases}
$$

Equality conventions have no probability consequence under a continuous latent distribution. The threshold subtractions make observed return continuous at either edge of the zero-return band. An information shock just beyond a threshold produces a small observed return, rather than a discrete jump equal to the cost. Figure 2, p. 1121, distinguishes this piecewise observation rule from the smooth conditional expected observed return.

The estimated total cost is

$$
c_j=\alpha_{2j}-\alpha_{1j}.
$$

The lower threshold’s magnitude is the selling-side component; the positive threshold is the buying-side component. Their difference is the round-trip quantity, so it must not be halved when comparing it with a full proportional spread plus round-trip commission. The model permits asymmetric thresholds. The reported results generally have $|\alpha_1|>\alpha_2$, consistent with selling being slightly more costly than buying under this interpretation.

For a given market return $m$, the predicted probability of a zero is

$$
p_{0j}(m)=\Phi\!\left(\frac{\alpha_{2j}-\beta_jm}{\sigma_j}\right)-\Phi\!\left(\frac{\alpha_{1j}-\beta_jm}{\sigma_j}\right).
$$

This equation explains why simply ranking zero frequencies is incomplete. The same band produces fewer zeros when residual variation is large or the market-induced conditional mean moves outside the band. A low zero frequency can therefore reflect either low costs or volatile information. The nonzero-return distribution supplies the variation needed to distinguish these effects.

The authors deliberately omit a market-model intercept. If the latent equation instead includes a constant $a_j$, replacing the thresholds by $\alpha_{1j}-a_j$ and $\alpha_{2j}-a_j$ leaves the observed-return likelihood unchanged. Their difference is invariant to that particular reparameterization. Thus the width can be identified even when the location of the band and a constant expected abnormal return cannot be separately identified. This reasoning does not protect the estimator from time-varying omitted expected returns, misspecified betas, or residual heteroskedasticity.

## Likelihood and a reconstructible estimator

For one stock-year, write $y_t=R_{jt}$, $m_t=R_{mt}$, and partition dates by the **observed stock return**: $\mathcal N=\{t:y_t<0\}$, $\mathcal P=\{t:y_t>0\}$, and $\mathcal Z=\{t:y_t=0\}$. The article sometimes describes these as negative and positive “market return” regions. The observation equation and its likelihood require the stock-return partition; market and stock return need not have the same sign.

For parameters $\theta=(\alpha_1,\alpha_2,\beta,\sigma)$, define $a_t=(\alpha_1-\beta m_t)/\sigma$ and $b_t=(\alpha_2-\beta m_t)/\sigma$. Equations (3)–(4), p. 1122, imply

$$
\begin{aligned}
\ell(\theta)= {}&-(n_-+n_+)\log\sigma-\frac{n_-+n_+}{2}\log(2\pi)\\
&-\frac{1}{2\sigma^2}\sum_{t\in\mathcal N}(y_t+\alpha_1-\beta m_t)^2\\
&-\frac{1}{2\sigma^2}\sum_{t\in\mathcal P}(y_t+\alpha_2-\beta m_t)^2\\
&+\sum_{t\in\mathcal Z}\log\{\Phi(b_t)-\Phi(a_t)\}.
\end{aligned}
$$

The nonzero densities need no additional division by the probability of being nonzero: these are unconditional density contributions in a mixed continuous/discrete distribution, not a regression estimated conditional on trading. Likewise, the zero observations must not be replaced by arbitrarily small returns. They are the primary source of information about the band.

All four parameters maximize this likelihood jointly. A sentence on p. 1122 describes the variance in connection with nonzero returns, but the displayed objective makes zero probabilities depend on $\sigma$ too. Estimating variance on nonzeros and then permanently fixing it would be a different procedure unless an external implementation establishes that the authors actually did so.

A practical reconstruction proceeds as follows:

1. Build the full cleaned stock-year return series and align it with the equally weighted market index on identical trading dates. Use decimal returns consistently; convert final widths to percentages only for tables.
2. Preserve exact zeros and separate negative, positive, and zero observations. Record their counts before estimation.
3. Maximize the displayed likelihood with $\sigma>0$ and ordered thresholds. Enforcing $\alpha_1<0<\alpha_2$ follows the economic interpretation, but the paper does not document whether its numerical optimizer imposed both sign constraints.
4. Evaluate zero probabilities through stable log-CDF differences, especially when both endpoints lie deep in a normal tail. A naive subtraction can underflow and falsely destroy an otherwise valid likelihood evaluation.
5. Run several starting values, check optimizer convergence, and inspect the local curvature and boundary behavior. Report $\hat c=\hat\alpha_2-\hat\alpha_1$ alongside counts of zero and nonzero returns and convergence diagnostics.
6. If reporting likelihood-based uncertainty, derive the variance of the difference using the full covariance matrix: $\operatorname{Var}(\hat c)=\operatorname{Var}(\hat\alpha_2)+\operatorname{Var}(\hat\alpha_1)-2\operatorname{Cov}(\hat\alpha_1,\hat\alpha_2)$.

Steps concerning numerical stability, multiple starts, and explicit covariance propagation are implementation recommendations in this note, not procedures documented by the authors. The source does not provide optimizer name, initialization, tolerance, gradient code, failure handling, or per-year counts of rejected numerical fits. It states a minimum of 25 daily returns for numerical convergence, not a proof that 25 observations guarantee identification or reliable standard errors. All-zero samples, very few observations in one tail, or nearly invariant market returns can make estimation weak or degenerate even above that threshold.

## Data construction and historical comparators

Section 3, pp. 1123–1124, obtains daily returns from CRSP for NYSE and AMEX stocks over 1963–1990. A firm must be listed throughout a calendar year. Firms beginning or ending trading within the year are excluded. Market capitalization must be nonzero. The annual cross-section is assigned CRSP size deciles using the prior year-end ranking where available; the source says it uses the current ranking when a prior ranking is unavailable. This fallback is important for a later predictive application: it is not automatically information available at the start of the estimation year.

Annual estimation requires at least 25 daily returns. Missing CRSP return codes below $-1.0$ are removed. The paper does not provide a modern CRSP field-level extraction script, an exhaustive share-code filter, or a complete corporate-action and delisting treatment beyond these restrictions. Such choices must be documented in a new replication. The entire-year listing rule creates a selection boundary that excludes some distressed or newly listed securities.

The market proxy is the CRSP equally weighted NYSE/AMEX index. To examine sensitivity to the index, the authors use an equally weighted portfolio of firms in the same size decile; results are described as similar. They also report that changing index specifications affects cost estimates only slightly in the exercises discussed in the text. These are limited robustness results, not an invariance theorem covering arbitrary benchmarks.

Three quote and commission sources enter the validation. First, NYSE proportional spread observations for 1963–1979 come from the Fitch material used by Stoll and Whaley; they are last-trading-day snapshots rather than full-year daily averages. Second, ISSM provides daily closing bid and ask quotes in 1988–1990. Its stock-year proportional spread is the daily average of

$$
s_t=\frac{\operatorname{Ask}_t-\operatorname{Bid}_t}{(\operatorname{Ask}_t+\operatorname{Bid}_t)/2}.
$$

Third, commission estimates come from published schedules. The early-period comparison uses NYSE minimum schedules for 1963–1974 and holds the 1974 schedule fixed subsequently where specified. The commission is doubled to represent a round trip. Later comparisons use price-based schedules from Scott and from the Bhardwaj–Brooks study. These schedules are proxies for commissions, not actual commissions paid by each marginal trader. Discounts, negotiated fees, and bundled services can make the comparator overstate effective costs.

The paper also calculates a Roll-style estimate. Its handling of positive sample autocovariances is unusual and must be retained for exact replication: it forces positive first-order autocovariances to become negative. Therefore its effective formula is $2\sqrt{|\widehat{\operatorname{Cov}}(R_t,R_{t-1})|}$, rather than setting positive-autocovariance estimates to zero or missing. Comparison against another paper’s “Roll” series without matching this rule can produce misleading differences.

There is no train/test split, forecast validation window, trading strategy, rebalance schedule, or net-return backtest in this paper. Costs are estimated retrospectively from each full calendar year, then compared with contemporary historical quote measures. A strategy using the annual estimate must wait until the estimation data are available; the paper’s cross-sectional correlations do not validate an implementable real-time cost forecast.

## How informative are zero returns?

Table 1 reports that, over 1963–1990, the smallest size decile has 36.6% zero-return days on average, compared with 11.9% for the largest. The maximum firm-year zero fractions are 84.5% and 49.2%, respectively. For 1988–1990, the corresponding means are 43.7% and 11.8%. Average quoted proportional spreads in that later sample are 10.05% and 0.60%; the paper’s adjusted Roll estimates are 5.25% and 0.36%.

Table 2 regresses the zero-return proportion on quoted spread within deciles and in aggregate. All spread coefficients are significant at the 1% level. For the smallest decile, the slope is 0.4565 with standard error 0.0471 and reported $R^2=15.12\%$. For the largest, the slope is 14.8578 with standard error 0.9791 and $R^2=30.76\%$. The pooled sample contains 5,359 firm-years; its slope is 1.9454, standard error 0.0341, and $R^2=37.50\%$. Differences in units matter here: the dependent variable is a fraction of days, and spread is a fraction of price. The steep large-firm slope is not a direct estimate of a trading-cost multiplier.

Appendix A investigates whether recorded zeros miss days with no economically relevant price change. Closing trades can bounce between an unchanged bid and ask. CRSP can also substitute a quote midpoint when no trade occurs, generating a measured change merely because the previous close was a trade away from the midpoint.

The appendix distinguishes seven categories: four with positive volume and three with zero volume. Its corrected zero proportion includes positive-volume bid–ask bounce, recorded zeros with positive volume, zero-volume midpoint transitions with unchanged quotes, and recorded zero-volume zeros. Table A, p. 1139, correctly gives the sum of categories **(2), (3), (4), (6), and (7)**. The preceding prose incorrectly substitutes category (5) for (6); category (5) has changed quotes and is not the intended no-information case.

The observed and adjusted proportions are 43.69% and 54.09% for the smallest decile, a 10.40-percentage-point difference, and 11.80% and 13.62% for the largest, a 1.82-point difference. The authors interpret observed zeros as a conservative but useful indicator and report only modest changes when using the adjusted definition in estimation. Nevertheless, unchanged quotes are themselves an imperfect proxy for no information. The correction is a diagnostic, not an observation of latent fundamental returns.

## Estimated costs and their validation

Table 3’s combined NYSE/AMEX mean widths, from smallest to largest size decile, are 10.35%, 7.09%, 5.59%, 4.49%, 3.83%, 3.19%, 2.76%, 2.28%, 1.84%, and 1.23%. Reported mean-cost test statistics range from 24.6 to 35.6. In a separate NYSE-only sorting exercise, the endpoints are 6.97% and 1.46%. These are different universes and breakpoints; the small-stock comparisons should not be read as a controlled exchange effect.

**Source arithmetic qualification:** the rendered first row of Table 3 reports $\hat\alpha_1=-5.34\%$, $\hat\alpha_2=4.31\%$, and $\hat\alpha_2-\hat\alpha_1=10.35\%$. The first two numbers imply 9.65%, not 10.35%. The headline and text repeat 10.35%, but the source does not resolve which entry is wrong. This note preserves the reported width as a reported result, not as an arithmetically verified estimate. A replication should retrieve underlying estimates instead of silently changing one threshold.

For the 1963–1979 NYSE comparison in Table 4, the smallest decile’s quoted spread is 3.23%, round-trip schedule commission 3.66%, and sum 6.89%, compared with LDV cost 5.82%. The largest decile has 0.76%, 2.10%, and 2.86%, compared with LDV cost 1.43%. The corresponding difference-test statistics are 33.14 and 70.97. Thus LDV is about 15.5% below spread-plus-commission for the small decile and 50% below it for the large decile; these reductions use the comparator as denominator. Calling the comparator “50% above LDV” would be wrong in the latter case—it is 100% above LDV.

Figure 3 shows substantial common time variation, notably the sharp small-stock cost increase during the mid-1970s and another increase late in the sample. The authors report an 85% correlation in annual cost comparisons for the endpoint deciles. Falling prices are an important historical contributor: the smallest NYSE decile’s average price falls from \$13.68 in 1970 to \$2.55 in 1975. Such price effects are one reason not to transport the historical percentages directly to another market regime.

Table 4 also regresses LDV on separate spread and commission proxies. In the smallest decile, the spread coefficient is 0.5765 (standard error 0.0271), commission coefficient 1.6275 (0.0433), and $R^2=78.31\%$. For the largest decile, the corresponding values are 0.5148 (0.0313), 0.3402 (0.0192), and 31.56%. The aggregate regression uses 20,370 firm-years and has $R^2=80.85\%$. Adding inverse price increases explanatory power in the source’s robustness exercise, but substantially reduces commission coefficients. Neither coefficient is a structural decomposition of individual investors’ actual trading bills: prices, spreads, commissions, impact, and trader composition are correlated.

Table 5 sorts NYSE securities into five price groups. For prices at or below \$5 in 1982–1986, spread-plus-commission is 12.535% and LDV is 10.121%; above \$20, the values are 2.095% and 1.789%. In 1988–1990, the same endpoints are 13.848% versus 12.056% and 2.013% versus 1.522%. The table labels these statistics as medians, despite passages in the prose calling LDV values averages. The final printed price-bin inequality is reversed; the discussion establishes that the intended final group is prices above \$20. The earlier-period comparator is drawn from the published Bhardwaj–Brooks material, so it is not a freshly reconstructed matched daily execution dataset.

Finally, Table 6 directly regresses LDV width on average quoted spread in 1988–1990. The pooled regression is approximately

$$
\hat c_j=0.0047+1.6495\,\bar s_j+u_j,
$$

with standard errors 0.0004 and 0.0081, 5,359 firm-years, and reported $R^2=88.47\%$. The smallest decile’s slope is 1.5595 (0.0319), with $R^2=82.15\%$; the largest is 1.4664 (0.0674), with $R^2=47.72\%$. Across deciles, $R^2$ ranges from 46.46% to 91.76%. The pooled Roll comparison has approximately 77% explanatory power, while the zero-frequency comparison has 37.50%.

This is the strongest evidence that conditioning zeros on return dynamics extracts useful cost-related information. It does **not** mean LDV equals the quoted spread: its slope is materially above one, its intercept is nonzero, and its interpretation includes broader costs. The article’s statement that it accurately estimates spread should therefore be read as strong association with a spread-related friction measure, not numerical identity. Reported regression standard errors are not described as clustered by firm and year; the source does not establish that all generated-regressor uncertainty is propagated through these validation regressions.

## Boundaries and practical use

The model is parsimonious enough to reproduce from the printed likelihood, but its economic interpretation is conditional. A zero may reflect costs, discreteness, stale prices, little information, halted trading, or the data vendor’s recording conventions. Fat tails, conditional volatility, changing beta, and serially correlated information can change the relative probability of zeros and nonzeros without a change in actual execution costs. Annual constant thresholds average over those changes.

The daily frequency also limits identification in highly liquid markets with almost no zeros. Conversely, very illiquid stocks may have so few nonzero observations that tail parameters and threshold width are poorly pinned down. The source does not provide a modern simulation study mapping these failure regimes, a universally valid minimum sample size, or out-of-sample confidence intervals for prospective trading costs.

A disciplined use is to treat LDV as one annual friction characteristic, retain its diagnostics, and compare it with actual quote or execution data when available. For a historical strategy, estimate on a completed window, lag the characteristic, and test whether it predicts the costs relevant to the strategy’s order size and holding period. Those steps extend the paper; they are not results it already establishes. The paper’s enduring contribution is a coherent mixed-density estimator that makes zero returns informative while separating their cost interpretation from unconditional volatility and market movement.
