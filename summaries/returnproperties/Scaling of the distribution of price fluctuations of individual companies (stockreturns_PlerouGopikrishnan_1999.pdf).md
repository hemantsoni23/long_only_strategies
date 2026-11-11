# Scaling of the distribution of price fluctuations of individual companies

Vasiliki Plerou, Parameswaran Gopikrishnan, Luís A. Nunes Amaral, Martin Meyer, and H. Eugene Stanley. *Physical Review E* 60, 6519–6529 (December 1999).

Source: [original PDF](../../Finance/stockreturns_PlerouGopikrishnan_1999.pdf), 11 pages, including the appendix on volatility and size and the methodological footnotes. Printed pages, equations, figures, and Table I are the locators below. This is the individual-company study, distinct from the same team's companion paper on financial market indices.

## Why this matters

Diversifying across hundreds of stocks and aggregating returns across many observations do not automatically produce a Gaussian return distribution at the horizons represented in this paper. The authors study individual-stock returns across two large US datasets and compare their standardized distributions with a market index. They find heavy tails with survival indices near three, broad persistence of distributional shape up to approximately sixteen trading days, and a slower transition toward Gaussian behavior than an independence argument might suggest. An experiment that independently shuffles company returns produces much more Gaussian synthetic aggregates.

The innovative empirical component is the combination of a large cross-section, multiple sampling horizons, a size-conditioned normalization that improves scale estimation, and a cross-company dependence experiment. The output is a collection of stylized facts and diagnostics rather than a fitted structural model. An educated reader should be able to reconstruct those diagnostics, while recognizing that the finite samples do not prove a universal asymptotic law or a unique mechanism behind the tails.

The practical modeling target is joint: a candidate multivariate return generator should reproduce company-level tail behavior, its evolution with horizon, the relation between volatility and capitalization, and the extent to which tails survive aggregation across correlated companies. Matching one unconditional stock-return histogram is insufficient to meet that target.

## Datasets, universe, and the observation clock

The high-frequency source is TAQ for January 1994–December 1995, spanning NYSE, AMEX, and Nasdaq. The authors select the 1,000 companies with the largest capitalization on January 3, 1994, among companies that existed throughout the two-year period. Footnote 23 supplies this survival requirement. It introduces a selection condition that matters when interpreting the results as representative of the broader equity universe: newly listed, disappearing, or otherwise noncontinuous firms are excluded from this high-frequency panel.

Prices are sampled at five-minute intervals. Each company contributes approximately 40,000 observations, yielding about 40 million sampled records overall. The original underlying transaction count is of order one billion. Five-minute records and transactions are therefore not interchangeable units. Large stocks have several transactions within a sampling interval, while some smaller firms trade only approximately every fifteen minutes. A reproduction needs an explicit stale-price/previous-trade rule; the source does not completely specify that implementation.

The long-horizon source is CRSP: roughly 35 million daily observations for approximately 16,000 companies during 1962–1996. The database has NYSE, AMEX, and Nasdaq histories with different entry dates; Nasdaq coverage begins in 1972. CRSP's permanent identifiers enable linkage across identifier changes. The paper also describes monthly records and analyzes horizons up to about 46 months, or roughly four years. Table I converts one day to 390 minutes and one month to 22 days. The long panel is broader and covers a much longer period than the TAQ survivor panel, so cross-frequency comparisons also involve changes in universe and sample period.

An S&P 500 series sampled more frequently than once per minute during January 1984–December 1996 provides the index comparison. It contains more than 4.5 million source points. It should not be mistaken for an exactly synchronized constituent portfolio over the entire company sample.

The time clock advances through exchange working hours, removing nights, weekends, and holidays as elapsed time. Crucially, footnote 22 states that **overnight returns are retained**. Removing overnight returns produces a slightly larger estimated tail exponent. Omitting nontrading elapsed hours therefore does not mean omitting the close-to-open price change. This detail is essential for reconstructing the sampled return series and its extreme observations.

## Return construction and cleaning

For company $i$, let $S_i(t)$ denote market capitalization, defined as price times shares outstanding. The measured return is

$$
G_i(t,\Delta)=\log S_i(t+\Delta)-\log S_i(t).
$$

The paper approximates this by the proportional capitalization change for small moves, but the defining statistic is logarithmic. A replication should preserve the log definition. Market-capitalization changes and shareholder total returns are not automatically the same object. In particular, changes in shares outstanding, distributions, splits, and corporate actions require explicit handling; the paper's description should not be silently replaced by an assumed CRSP total-return field.

Footnote 25 describes two cleaning operations. Very large spikes caused by missing digits in recorded prices are removed with a threshold. The authors vary the threshold, find no effect on their reported results, and check removed observations individually to confirm recording errors. Exact numerical thresholds and the full list of exclusions are absent. Returns occurring overnight purely because shares outstanding change are set to zero in the authors' treatment of splits and takeovers. This is the reported rule; it is not a complete general specification for every corporate event.

A reconstruction should save raw price and shares series, corporate-action flags, the reason each observation is changed, and sensitivity to the spike filter. Aggressive removal of genuine extreme moves could mechanically increase the estimated tail exponent. The paper's manual confirmation is therefore material evidence, but the absence of the precise filter prevents exact reproduction of that step.

## Two normalizations, with different purposes

For the five-minute company-level analysis, calculate each company's full-period mean and standard deviation:

$$
\mu_i(\Delta)=\langle G_i(t,\Delta)\rangle_T,\qquad
v_i^2(\Delta)=\langle G_i(t,\Delta)^2\rangle_T-\mu_i(\Delta)^2,
$$

$$
g_i(t,\Delta)=\frac{G_i(t,\Delta)-\mu_i(\Delta)}{v_i(\Delta)}.
$$

The average is over the company's two-year time series. This removes company-specific unconditional scale. It does not produce a real-time risk forecast and does not filter conditional volatility. Ten randomly selected companies illustrate the dispersion of raw distributions and their improved agreement after normalization; the tail-exponent histogram is computed across all 1,000 firms, not only the illustrated ten.

The authors then pool standardized observations into a single empirical distribution to obtain more tail events. Individual-stock positive-tail exponents have a mode near three, but they are dispersed. The pooled curve must not be interpreted as proof that every stock has the same exponent. Stocks are also dependent, so 40 million observations do not represent 40 million independent draws for statistical inference.

At longer horizons, individual volatility estimates become unstable: the source contrasts roughly 40,000 five-minute records per firm with only about 400 observations at 500 minutes. To reduce this scale-estimation problem, it groups returns by capitalization. Section III.B says to assign each return according to capitalization at the beginning of its interval. This timing makes size a conditioning variable known before that return, although the bin mean and variance are still estimated using the full pooled sample.

For a size bin $B$, pool all eligible company-interval observations and define

$$
\mu_B(\Delta)=\frac{1}{n_B}\sum_{(i,t)\in B}G_i(t,\Delta),
\qquad
v_B^2(\Delta)=\frac{1}{n_B}\sum_{(i,t)\in B}G_i(t,\Delta)^2-\mu_B(\Delta)^2,
$$

$$
g_B(t,\Delta)=\frac{G_i(t,\Delta)-\mu_B(\Delta)}{v_B(\Delta)}.
$$

These equations make the paper's averaging notation explicit. The operation pools returns, rather than averaging already estimated company volatilities. The source describes uniform log-capitalization bins. Figure 5 illustrates four thirty-minute bins with endpoints $10^{9.8},10^{10.2},10^{10.4},10^{10.6},10^{10.8}$; the first displayed interval is wider than the later ones despite the uniform-bin description. Figure 7's daily illustrations use endpoints $10^5,10^6,10^7,10^8,10^9$. The exact complete bin grid, small-bin treatment, and capitalization-unit implementation are not fully documented.

Section IV also uses wording about “average” capitalization when describing the daily bins. The earlier start-of-interval rule is explicit; a replica should disclose whether it applies that rule throughout and test the alternative if needed, rather than conceal the wording ambiguity. Membership changes as firms grow or shrink, which is especially important over the 35-year daily sample.

At thirty minutes, direct company normalization yields positive-tail index $3.21\pm0.08$, while size-bin normalization yields $3.23\pm0.05$. Figure 6 shows close agreement of the distributions. This supports the size-bin procedure for the displayed comparison. It does not show that size alone explains all cross-sectional volatility differences or that the two methods are interchangeable in every market.

## Tail estimators and uncertainty

The central tail statistic is the survival probability, separately by sign:

$$
\Pr(g>x)\sim C_+x^{-\alpha_+},\qquad
\Pr(g<-x)\sim C_-x^{-\alpha_-}.
$$

A corresponding density decays as $x^{-(1+\alpha)}$. Thus “exponent three” in this paper means an inverse-cubic survival tail, not a density proportional to $x^{-3}$. The five-minute pooled log-log regression fits use $2\le |g|\le80$, giving $\alpha_+=3.10\pm0.03$ and $\alpha_-=2.84\pm0.12$ (equation 7).

The alternative is a local inverse-slope estimator related to Hill estimation. For a descending sequence of positive magnitudes $x_k$, empirical survival is approximately $k/N$. A consistent positive inverse slope can be written

$$
\zeta_k=-\frac{\log(x_{k+1}/x_k)}{\log((k+1)/k)}.
$$

Average local slopes in groups, plot their inverse-slope averages against $1/x$, and extrapolate toward $1/x=0$ to estimate $1/\alpha$. Figure 3 uses 1,000 events per point and observations above five standard deviations. The resulting estimates are $2.84\pm0.12$ for positive returns and $2.73\pm0.13$ for negative returns. The figure's text inconsistently describes the sign of the logarithmic slope and prints a range in $g$ where its axis is $1/g$; the definition above resolves the sign and axis conventions needed to reproduce the positive plotted inverse indices. Averaging all selected events without extrapolation is the related Hill alternative discussed by the authors.

Footnote 26 is unusually important: reported exponent errors are regression-fit errors, and the authors themselves say the width of the company-level exponent histogram is a more realistic indication of uncertainty. Neither the small pooled regression error nor the raw observation count establishes precision under temporal and cross-sectional dependence. The source does not report a complete block bootstrap, threshold-selection rule, likelihood comparison against other tail families, or held-out tail validation.

## Results across horizons

Table I below is condensed to retain the main horizon comparisons. One day and longer use CRSP; shorter horizons use TAQ. Tail indices refer to survival functions. Quoted errors preserve the source's reporting convention.

| Horizon | Regression positive | Regression negative | Hill positive | Hill negative |
|---|---:|---:|---:|---:|
| 5 minutes | 3.10 ± 0.03 | 2.84 ± 0.12 | 2.84 ± 0.12 | 2.73 ± 0.13 |
| 10 minutes | 3.32 ± 0.08 | 2.89 ± 0.13 | 3.14 ± 0.10 | 2.68 ± 0.14 |
| 20 minutes | 3.25 ± 0.08 | 2.75 ± 0.10 | 3.32 ± 0.18 | 2.41 ± 0.10 |
| 40 minutes | 3.28 ± 0.08 | 2.61 ± 0.10 | 3.39 ± 0.16 | 2.62 ± 0.11 |
| 80 minutes | 3.50 ± 0.13 | 2.49 ± 0.11 | 3.65 ± 0.26 | 2.53 ± 0.14 |
| 160 minutes | 3.47 ± 0.08 | 2.42 ± 0.09 | 2.9 ± 0.4 | 2.53 ± 0.17 |
| 320 minutes | 3.60 ± 0.10 | 2.54 ± 0.10 | 3.32 ± 0.08 | 3.19 ± 0.05 |
| 1 day | 2.96 ± 0.09 | 2.70 ± 0.10 | 3.05 ± 0.13 | 2.95 ± 0.15 |
| 2 days | 3.09 ± 0.03 | 2.62 ± 0.04 | 3.11 ± 0.09 | 2.90 ± 0.12 |
| 4 days | 3.18 ± 0.05 | 2.75 ± 0.09 | 3.20 ± 0.08 | 2.90 ± 0.10 |
| 8 days | 3.31 ± 0.08 | 2.71 ± 0.03 | 3.25 ± 0.06 | 2.94 ± 0.09 |
| 16 days | 3.43 ± 0.04 | 2.74 ± 0.12 | 3.35 ± 0.04 | 2.93 ± 0.07 |
| 32 days | 3.73 ± 0.04 | 2.63 ± 0.06 | 3.54 ± 0.05 | 2.93 ± 0.08 |
| 64 days | 3.98 ± 0.09 | 2.78 ± 0.07 | 3.89 ± 0.09 | 3.00 ± 0.10 |
| 256 days | 5.06 ± 0.07 | 3.01 ± 0.07 | 4.5 ± 0.6 | 2.92 ± 0.19 |
| 1,024 days | 6.43 ± 0.29 | 3.48 ± 0.07 | 5.11 ± 0.03 | 3.45 ± 0.02 |

At the daily overlap, TAQ estimates are $3.27\pm0.19$ and $2.98\pm0.21$, compared with CRSP's $2.96\pm0.09$ and $2.70\pm0.10$ (Figure 8). The authors regard the datasets as broadly consistent. The estimates should remain labeled by dataset because selection and historical period differ.

From five minutes through approximately sixteen days, the authors describe approximate preservation of standardized tail shape, with exponents generally outside the non-Gaussian stable Lévy range. Exact invariance is too strong: positive-tail indices gradually rise, negative-tail values differ, and estimates depend on the method. In particular, the sixteen-day crossover for individual stocks differs from the approximately four-day crossover reported in the companion index paper. They are empirical summaries of different objects, not conflicting universal constants.

Above sixteen days, the positive tail clearly moves toward Gaussian behavior. The negative tail shows much weaker evidence of convergence and remains approximately power-law-looking even at long horizons; the authors explicitly caution that tail statistics are limited there. The abstract's broad convergence language therefore needs this qualification. A conclusion that both signs become Gaussian after sixteen days would overstate the results.

The additional diagnostic is the absolute fractional moment

$$
\mu_q(\Delta)=\langle|g(\Delta)|^q\rangle,\qquad 0<q<3.
$$

The average pools normalized observations. Similar moment curves across intraday horizons support approximate distributional similarity; long-horizon curves approach a Gaussian benchmark. Since normalization imposes unit second moment, agreement at order two is automatic. Orders near three are sensitive to the extreme observations, and finite-sample values do not establish existence of population moments. Approximate tail indices near three suggest finite variance but do not guarantee finite third or fourth moments.

## Cross-company aggregation experiment

The paper asks why the index tail resembles company tails even though a large independent sum with finite variance should approach a Gaussian under suitable regularity conditions. It constructs partial capitalization-weighted aggregates

$$
G^{(N)}(t,\Delta)=\sum_{i=1}^Nw_i(t)G_i(t,\Delta),\qquad
w_i(t)=\frac{S_i(t)}{\sum_{j=1}^NS_j(t)}.
$$

This weighted sum of company log returns is a small-change approximation to the log return of the aggregate capitalization. With frozen shares, the exact capitalization-return identity instead involves the logarithm of a weighted sum of gross returns. The displayed construction should therefore be implemented as the paper's statistic, not silently relabeled an exact investable index return.

Footnote 35 states that the largest-100 and largest-500 fixed-company aggregates are not literally the official S&P 100 or S&P 500. Official constituents reflect industry representation and change over time, whereas the constructed group is based on initial capitalization. The authors judge the difference negligible for their studied period. A replica should preserve the distinction and report the construction explicitly.

At five-minute frequency, independently shuffle each company's return sequence, thereby preserving its empirical marginal distribution while disrupting original cross-company alignment. Construct aggregates for $N=1,10,100,500$ from the shuffled series and normalize each aggregate. Figure 11 shows progressively more Gaussian distributions as $N$ increases. The original index retains a much heavier tail. Footnote 36 also compares an unweighted sum of returns to address the possibility that a few high-capitalization firms alone dominate the weighted aggregate.

The necessary implementation detail is **independent permutations for each company**. A common permutation would preserve synchronous cross-sectional dependence and would not perform the intended experiment. The exact random seed, number of permutation replications, confidence envelope, and handling of weights during permutation are not reported. The source characterizes weights as weakly time-dependent but does not give a complete weight-freezing protocol for the shuffled experiment.

This diagnostic supports a role for dependence in sustaining aggregate tails. It is not a complete decomposition into market factors, sectors, contagion, or order-flow mechanisms. Independent shuffling also destroys each company's time dependence and alignment with common volatility regimes. Moreover, the central limit theorem requires more than a finite variance: no dominant summand and suitable dependence/heterogeneity conditions matter. A finite portfolio can remain heavy-tailed far into its extreme tail even when its central distribution becomes more Gaussian. The evidence concerns the displayed range and sample, rather than an exact asymptotic theorem for every portfolio.

## Volatility versus capitalization

The appendix and Figure 4 report an approximate relation

$$
v_B(\Delta)\propto S^{-\beta(\Delta)}.
$$

At a one-day horizon, the fitted region has $\beta\approx0.2$: larger companies exhibit smaller return variability. At the largest capitalizations, the relation flattens. At longer horizons, the exponent declines, reaching approximately 0.09 around 1,000 days. No comprehensive confidence intervals, exact size-fit boundaries, or structural identification are provided.

This result motivates the bin normalization, but the normalization must use measured bin variance rather than assuming a universal $S^{-0.2}$ formula everywhere. The flat high-capitalization region and horizon dependence would otherwise be lost. Similarities to size-scaling results for firm sales or research budgets are analogies in the discussion; they do not establish a common economic mechanism.

## What a faithful replication can and cannot claim

A faithful reconstruction needs separate TAQ and CRSP pipelines, documented universe membership and survival selection, preserved overnight changes, a corporate-action and bad-record audit, explicit sampling strides, and both company and size-bin normalizations. It should report signed survival tails, estimator sensitivity, company-level exponent dispersion, fractional moments, and original versus independently shuffled aggregates. To reproduce the cross-sectional claims, retain both capitalization-weighted and unweighted checks and identify the official index separately from the constructed one.

Missing inputs include the exact original extracts, complete capitalization-bin grid, cleaning thresholds, all corporate-action decisions, stale-price rules, long-horizon overlap choices, Hill tuning outside the displayed example, shuffle conventions, and dependence-robust uncertainty. No transaction-cost assumption, rebalancing rule, or portfolio-performance statistic is supplied because this is a distributional study rather than a strategy backtest.

The paper's strongest contribution is the empirical conjunction of heavy individual tails, slow and asymmetric horizon evolution, a systematic size–volatility relation, and dependence-sensitive aggregation. Those are useful reconstruction targets. The exact tail index, sixteen-day crossover, and apparent scale collapse remain sample- and method-dependent findings, with clear limits imposed by survival selection, pooling, and extreme-event scarcity.
