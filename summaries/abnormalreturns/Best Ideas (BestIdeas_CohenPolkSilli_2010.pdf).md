# Best Ideas

Randolph B. Cohen, Christopher Polk, and Bernhard Silli. Working paper, draft dated May 1, 2010; first draft November 7, 2005. Source: [BestIdeas_CohenPolkSilli_2010.pdf](../../Finance/BestIdeas_CohenPolkSilli_2010.pdf). This note summarizes the full 54-page supplied draft, including its figures and seven tables. The 2009 file in the library is another version of the same work, not a separate research contribution. Printed page numbers are two below PDF page numbers.

## Why this matters

A mutual fund can contain information about security selection even when its aggregate net return is disappointing. The paper asks whether managers' largest active convictions identify better stocks than the rest of their holdings. Instead of ranking funds by historical alpha, it tries to infer a manager's current preferred stock from portfolio weights relative to a benchmark, adjusting those weights for idiosyncratic risk. It then evaluates the future returns of the inferred choices across managers.

The important innovation is the within-manager distinction between high-conviction positions and portfolio holdings included for other reasons. Performance of a complete fund mixes stock selection, diversification, liquidity management, scale, fees, and incentives. A stock-level conviction proxy can uncover selection ability obscured by that mixture. The paper reports economically large abnormal returns on selected best ideas, with much smaller returns as one moves down the inferred ranking.

This is primarily a test of manager information at the true holdings date. The baseline does not delay portfolio formation until holdings are publicly released, and it does not deduct execution costs or management fees. Its estimates therefore should not be advertised as the realizable alpha of an outsider's public-filings strategy. It also does not show that concentrating every existing mutual fund would preserve the measured return at the same scale.

## Reverse engineering conviction from portfolio weights

Section 3 starts with a mean–variance investor choosing weights $w_f$ over $N$ risky securities. With expected excess returns $\mu_f$, covariance matrix $\Omega$, and positive risk-aversion parameter $k$, the unconstrained problem is

$$
\max_{w_f}\;w_f^\top\mu_f-\frac{k}{2}w_f^\top\Omega w_f.
$$

Its first-order condition gives $\mu_f=k\Omega w_f$. Using the same covariance matrix and risk-aversion coefficient for the market portfolio, $\mu_M=k\Omega w_M$, yields the subjective expected-return difference

$$
\alpha_f=\mu_f-\mu_M=k\Omega(w_f-w_M).
$$

The paper interprets this as the manager's subjective CAPM alpha vector. It then assumes a single common covariance factor:

$$
\Omega=D+\sigma_M^2\beta\beta^\top,
\qquad D=\operatorname{diag}(\sigma_{\epsilon,1}^2,\ldots,\sigma_{\epsilon,N}^2).
$$

$D$ contains stock-specific residual variances, $\beta$ the market betas, and $\sigma_M^2$ market variance. If the fund and market have the same aggregate beta, the common-factor contribution vanishes because $\beta^\top(w_f-w_M)=0$. Thus

$$
\alpha_{if}=k\sigma_{\epsilon,i}^2(w_{if}-w_{iM}).
$$

The best idea is the held stock with the highest value of this score. Multiplying all scores by the same positive $k$ does not affect its identity. A given overweight is interpreted as stronger conviction when it consumes more idiosyncratic risk. For example, equal overweights in two stocks do not imply equal conviction if their residual variances differ substantially. The paper uses variance, not residual standard deviation.

A second benchmark restricts the comparison to the stocks the fund actually holds. If $H_f$ is that set and $MC_i$ is market capitalization, define

$$
w_{ifV}=\frac{MC_i}{\sum_{j\in H_f}MC_j},\qquad i\in H_f.
$$

The portfolio-alpha score is then $\sigma_{\epsilon,i}^2(w_{if}-w_{ifV})$. This attempts to remove the effect of a manager's restricted investment universe. It is a value-weighted portfolio of the fund's held names, not the fund's actual weight vector and not a self-declared commercial benchmark.

Two simpler robustness scores drop the variance multiplier: market tilt $w_{if}-w_{iM}$ and portfolio tilt $w_{if}-w_{ifV}$. For each of the four scores, first identify a maximum within each fund, then rank those maxima across funds. The main tests retain only the top quartile of fund maxima, reducing the influence of funds that barely deviate from passive weights. This is not equivalent to selecting the top quartile of all stock positions pooled together.

The derivation is a motivation, not an exact inverse optimization for constrained real funds. Long-only restrictions, industry mandates, trading costs, nonunit beta, additional factors, different covariance estimates, and state-dependent risk aversion can all change the mapping. In particular, the source says homogeneous risk aversion is without loss of generality because the ranking is ordinal. Dropping a common positive multiplier is valid, but arbitrary heterogeneity relative to the market is stronger: with $k_f\ne k_M$, the difference is $k_f\Omega w_f-k_M\Omega w_M$, not $k_f\Omega(w_f-w_M)$. Its additional terms need not preserve stock ranks. Likewise, replacing the full market by a restricted universe does not automatically satisfy equal-beta assumptions. A reproducer should implement the published scores as observable heuristics without treating all of these generalizations as proved.

## Data and portfolio formation

Holdings come from Thomson Reuters; stock returns cover NYSE, AMEX, and NASDAQ through CRSP. The holdings sample is January 1984–December 2007. The reported return regressions run from January 1985–December 2007, giving 276 monthly return observations before any missing-data losses. Funds must be US domestic equity funds, exceed \$5 million in net assets, and have at least five recorded holdings. Index, tax-managed, and international funds are excluded. Table 1 further requires holdings disclosed within the preceding six months.

The sample grows from 421 funds managing about \$56 billion at year-end 1984 to 1,348 funds managing \$2.542 trillion at year-end 2007. Mean stock count rises from 50 to 111. The sample peaks above 2,300 funds in 1998–1999 and then declines; it is not a panel of the same managers surviving throughout the period. “Manager” is inferred from a fund portfolio, not a verified persistent individual decision maker across job changes.

At the start of each quarter, identify each eligible manager's best idea from holdings at their actual holdings date, apply the cross-manager conviction cutoff, and assemble the selected names. Each manager contributes equal weight in the principal long-only portfolio. If two managers select the same stock, that name receives twice the weight of a name selected once. The paper also reports qualitatively similar results with unique names equally weighted, market-cap weighting, and weighting by the dollars invested in the best idea, but it does not give complete return tables for every alternative.

Hold the portfolio through the quarter and record monthly returns; rebalance at the next quarterly formation. The source does not provide a full code-level rule for stale non-quarter-end holdings, within-quarter weight drift, delisting returns, missing prices, minimum residual-variance history, or stock-level ties. Most consequentially, it calls residual variance the most recent CAPM estimate but does not clearly specify the estimation frequency, lookback, or minimum observations for the score. These are material reproducibility gaps, because the score directly multiplies this estimate.

The main portfolio's selected stocks are quite dispersed across managers. Figure 1 reports that about 62% of selected names are best ideas for only one manager, fewer than 18% for two, about 8% for three, and fewer than 7% for more than five. This is not a single crowded consensus portfolio, although manager decisions and underlying information are not independent.

## Comparators and factor models

The paper uses three return comparators. First, compare the long-only best-idea basket to Treasury bills. Second, subtract the return of a characteristic-matched DGTW benchmark for each stock before aggregation. Third, build a within-manager best-minus-rest spread: long the best idea and short the fund's remaining stocks, normalized in proportion to the manager's remaining position weights. For manager $f$ with best stock $i_f$, that last return is

$$
BMR_{ft}=R_{i_f,t}
-\sum_{j\in H_f\setminus\{i_f\}}
\frac{w_{jf}}{1-w_{i_ff}}R_{jt}.
$$

The spread reduces common manager style and industry exposure, but it is not guaranteed to be factor neutral. For example, the best idea can have different growth and momentum characteristics from the rest. Section 5.2 says these spreads are aggregated using dollars invested in best ideas, whereas Table 2's caption describes an equal-dollar position for every manager. Exact replication should run and report both rather than silently choose one and claim the ambiguity is resolved.

Monthly Carhart regressions use market, size, value, and momentum factors. The six-factor specification adds an idiosyncratic-volatility factor and a short-term-reversal factor:

$$
r^{test}_t=\alpha_6+bMKT_t+sSMB_t+hHML_t+mMOM_t
+iIDI_t+rSTREV_t+\epsilon_t.
$$

The volatility factor is a value-weighted high-minus-low-idiosyncratic-volatility stock portfolio constructed following the cited Ang and coauthors method; other factors are drawn from the Kenneth French library. The additional factors are especially relevant because the selection score intentionally favors some high-idiosyncratic-variance stocks and can mechanically load on past price changes. DGTW matching controls size, book-to-market, and momentum characteristics, whereas factor regressions control return covariation. Neither guarantees a perfect asset-pricing benchmark.

Tables report coefficient $t$-statistics but do not give a fully specified HAC bandwidth or an alternative resampling procedure. Many related strategies, cutoffs, factors, and subsamples are examined without a reported familywise or false-discovery correction. Forward returns are out of sample relative to each observed holding; the 1985–2007 exercise is not a separately locked model-development and validation split.

## Principal results: strong but benchmark sensitive

Table 2's headline results are monthly. The following numbers express returns and alphas in percentage points per month, with intercept $t$-statistics in parentheses:

| Test portfolio | Mean return | Four-factor alpha | Six-factor alpha |
|---|---:|---:|---:|
| Market-alpha best ideas, minus bills | 1.23 | 0.40 (1.86) | 0.82 (4.38) |
| Portfolio-alpha best ideas, minus bills | 1.36 | 0.53 (2.85) | 0.87 (5.15) |
| Market-alpha ideas, DGTW adjusted | 0.65 | 0.53 (2.71) | 0.83 (4.42) |
| Portfolio-alpha ideas, DGTW adjusted | 0.72 | 0.64 (3.69) | 0.88 (5.11) |
| Market-score best-minus-rest | 0.39 | 0.34 (1.61) | 0.79 (4.49) |
| Portfolio-score best-minus-rest | 0.55 | 0.48 (2.68) | 0.85 (5.44) |

The approximately 1.2%–2.6% quarterly alpha emphasized by the paper is simple multiplication of monthly intercepts by three, not a directly observed net quarterly arbitrage profit. Likewise, multiplying 0.87% by twelve gives a 10.44% arithmetic annualization, not a realized compound growth rate.

The long-only baskets have market beta about 1.23, negative HML loadings around −0.49 and −0.48, and positive momentum coefficients 0.27 and 0.23. They favor high-beta growth stocks with prior strength. Their positive volatility-factor loadings are 0.46 and 0.37. Because high-volatility stocks perform poorly relative to simpler benchmarks, including the volatility factor raises measured alpha substantially. The stronger six-factor finding is therefore economically intelligible but also heavily conditional on the benchmark choice. The 0.40% market-score four-factor estimate has $t=1.86$, not conventional two-sided 5% significance.

Table 3 changes the conviction cutoff. Using all managers, six-factor alphas fall to 0.45% and 0.36% monthly, with $t=3.44$ and $3.15$; four-factor alphas are only 0.18% and 0.20%, with $t=1.23$ and $1.66$. In the top 5% of conviction maxima, six-factor alphas rise to 1.01% and 1.17%, $t=3.62$ and $4.37$. The corresponding four-factor figures are 0.54% and 0.76%, $t=1.82$ and $2.74$. Larger score magnitude is associated with stronger performance, but this cutoff comparison is not an independently optimized investment rule.

Dropping the idiosyncratic-variance multiplier weakens the results. In the top-quartile simple market-tilt portfolio, four- and six-factor alpha are 0.15% and 0.19%, with $t=1.59$ and $1.99$. For simple portfolio tilt they are 0.31% and 0.32%, with $t=3.29$ and $3.34$. These results support a conviction interpretation beyond one specific risk estimate, while showing that the headline magnitude depends substantially on the risk-weighted score.

## Rank decay, liquidity, popularity, and fund characteristics

Figure 3 replaces each best idea with successively lower-ranked positions, requiring managers to hold at least twenty names. Six-factor alpha declines as one moves from first through second, third, fourth, fifth, and tenth ideas. The paper's sentence saying it can “reject” positive alpha appears to reverse its intended inference; the plotted positive estimates and surrounding discussion indicate tests against zero, not proof that alpha is negative. Figure 4 shows no reversal of best-idea abnormal returns through twelve months, with cumulative performance slightly above 10% for the variance-weighted scores. These are overlapping holding-horizon plots, and the draft does not provide complete covariance estimates for all event-time points.

Table 4 contains a substantive labeling inconsistency. Its title and surrounding text call the top-three/top-five exercises best-minus-rest tests, but the caption and regression labels describe long-only excess returns, and market betas remain around 1.23–1.24 rather than near zero. The displayed six-factor alphas are 0.41% and 0.45% for the top three ideas, falling to 0.30% and 0.33% for the top five. These numbers support declining rank performance, but should not be asserted unambiguously to describe a dollar-neutral spread. The text says selected positions are weighted by the manager's position size within fund and equally across managers; the remaining implementation ambiguity requires author code.

Table 5 splits best ideas by preceding-quarter average relative bid–ask spread. Less-liquid selections have six-factor alphas of 1.00% and 1.07% monthly, with $t=3.88$ and $4.59$; more-liquid selections have 0.26% and 0.20%, with $t=1.20$ and $1.01$. The corresponding four-factor alphas for less-liquid selections are only 0.38% and 0.50%. Thus the large advantage is concentrated where implementation costs and model sensitivity are also greater. The authors state that additional liquidity-factor controls do not eliminate the finding, but the PDF does not show those complete estimates.

Popularity is constructed by ranking a stock's score within each manager's portfolio and summing its percentage ranks across managers. It therefore incorporates both breadth of ownership and within-fund conviction; it is not the average conviction conditional on ownership. Below-median-popularity ideas earn six-factor alpha around 1.01% under both main scores, with $t=4.27$ and $4.95$. Above-median groups earn 0.24% and 0.54%, with $t=0.77$ and $1.68$. The evidence is consistent with information being more valuable when fewer peers share it.

Table 6 sorts funds into terciles by normalized Herfindahl concentration and by assets. Concentrated-fund best ideas produce six-factor alpha 0.42% or 0.46%, versus 0.10% or 0.12% for the least concentrated group. However, Section 5.4 says it starts from the full-manager universe while the caption says top-quartile maxima; this discrepancy matters for reproducing those smaller figures. Small- and large-fund six-factor estimates in the size split are much closer: 0.86% versus 0.80% for the market score, and 0.89% versus 0.83% for the portfolio score. The stronger broad claim that small-fund ideas dominate should not conceal how modest these particular differences are or substitute separate significance tests for a direct difference test.

Finally, Table 7 sorts the rest of each manager's portfolio by past correlation with the best idea. The high-minus-low correlation spread has six-factor alpha 0.45% or 0.31% monthly, with $t=3.18$ and $2.96$; four-factor alphas are weaker and insignificant. The interpretation is that low-correlation positions may be included for diversification despite lower expected alpha. The correlation estimation window is not fully specified, and this association does not establish the manager's motive causally.

## Decentralized allocation: mechanism and corrected arithmetic

Section 6 explains why a manager maximizing its own Sharpe ratio can give the client too little exposure to its strongest ideas. In the first example, three mutually uncorrelated assets have equal volatility and expected returns 7%, 2%, and 1%, with zero risk-free rate. Unconstrained risky-portfolio weights are proportional to means, giving 70%, 20%, and 10%. A manager holding only the last two assets chooses weights two-thirds and one-third, which is optimal when the client allocates 30% to that manager.

If the client fixes the manager allocation below 30%, the best within-manager allocation changes. At a 20% allocation, approximately 16% of total wealth should go into the stronger idea. At a 10% allocation, allowing shorts makes the optimum about 11% in the stronger idea and −1% in the weaker; with long-only constraints, the entire 10% active sleeve goes into the stronger idea. These are illustrations of global portfolio optimization, not estimates from the fund data.

The second example assumes $N$ equally skilled managers, each with one unit-beta stock whose annual alpha is 4%, total volatility 40%, and independent residual return across managers. The market premium is 6% and market volatility 15%. If every manager puts fraction $w$ into its idea and $1-w$ into the market, an equal allocation across managers yields

$$
E[R]=0.06+0.04w,\qquad
\operatorname{Var}(R)=0.15^2+\frac{w^2(0.40^2-0.15^2)}{N}.
$$

Differentiating the Sharpe ratio gives the interior optimum

$$
w^*=\frac{0.04(0.15)^2N}{0.06(0.40^2-0.15^2)}
\approx0.10909N.
$$

This reconstruction gives 10.91% for one manager, 54.55% for five, and 545.45% for fifty. The source reports roughly 11%, 47%, and 468%, which do not all follow from its stated total-volatility assumptions. The latter two numbers instead resemble treating 40% as residual volatility. The qualitative argument survives this arithmetic inconsistency: diversification across independent ideas permits a much larger concentration inside each sleeve. Under the stated assumptions and fifty managers, global unconstrained Sharpe ratio is about 0.86, while prohibiting market shorting limits $w$ to one and gives about 0.63; keeping the one-manager weight gives about 0.43.

The implied leverage is a theoretical result under known alpha, independent residuals, constant variance, zero financing friction, and no price impact. It is not a practical recommendation for 545% single-name sleeves. Correlated errors across managers, alpha decay with capital, estimation uncertainty, and tail dependence can remove much of the apparent gain. The paper offers regulatory constraints, asset-gathering incentives, manager career risk, and investor reliance on standalone fund metrics as explanations for diluted best ideas; the empirical tests do not separately identify their contributions.

## What a reproduction can establish

The most defensible replication target is a holdings-date stock-selection result: construct the four observable conviction scores, preserve the distinction between within-fund maxima and cross-fund cutoffs, and reproduce the three benchmark comparisons across the stated months. Before claiming a public trading strategy, rebuild the information set using actual release dates and account for turnover, bid–ask spreads, market impact, financing, and taxes. The paper's reference to unpublished public-date profitability is not a substitute for those checks; a footnote's pointer to Figure 5 also does not supply such a test, since Figure 5 is the stylized allocation example.

A faithful extension should disclose choices for all unresolved inputs, especially residual-variance estimation and contradictory portfolio-weight descriptions. Its conclusion can then distinguish three propositions: managers' holdings reveal predictive ranking information; public investors can harvest that information after delay and costs; and reorganizing the asset-management industry to concentrate portfolios would improve equilibrium investor welfare. The supplied paper offers substantial evidence for the first and an economic argument for the third, while leaving the second and the full causal welfare claim incompletely established.
