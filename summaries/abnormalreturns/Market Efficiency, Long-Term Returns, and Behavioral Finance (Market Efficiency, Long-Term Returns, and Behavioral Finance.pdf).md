# Market Efficiency, Long-Term Returns, and Behavioral Finance

Eugene F. Fama, *Journal of Financial Economics* 49 (1998), 283–306. Source: [complete 24-page local PDF](<../../Finance/Market Efficiency, Long-Term Returns, and Behavioral Finance.pdf>). References below use printed pages; PDF page 1 is p. 283. This is a methodological review and critique of existing evidence, not a newly assembled security-level event-study dataset. All numerical study results below are results reported by Fama from the cited research, unless identified as an illustration or derivation.

## Why this matters

The paper asks whether long-horizon return anomalies justify replacing market efficiency with behavioral explanations. Its most useful contribution for implementation is a diagnosis of how benchmark error, compounding, overlapping events, changing portfolio composition, and stock weighting alter measured abnormal performance. A researcher reproducing an anomaly must specify an expected-return model and an inference procedure before interpreting a statistically significant return as delayed price adjustment.

Fama's conclusion favors efficiency as a working model. That conclusion should be distinguished from the narrower methodological results. Sensitivity to reasonable controls weakens a particular event-specific explanation; it does not prove that all prices are correct. Conversely, a negative alpha under one imperfect benchmark does not isolate irrationality. The paper recognizes post-earnings-announcement drift as comparatively robust and short-horizon momentum as an unresolved puzzle as of 1998.

## The joint hypothesis and why horizon matters

Let $r_{it}$ be a stock's return and $\widehat\mu_{it}$ its normal-return estimate under a chosen benchmark. The measured abnormal return is $a_{it}=r_{it}-\widehat\mu_{it}$. A test of zero abnormal performance jointly tests market efficiency, the normal-return specification, and relevant statistical assumptions. Failure of any component can reject that joint null.

Fama distinguishes structural model inadequacy from sample-specific patterns. A model such as the CAPM may systematically miss small-stock average returns. Even a correct population model can leave unusual realized returns for a characteristic group over a particular sample. If an event sample is disproportionately drawn from that group, its apparent anomaly can reflect either problem. Matching firms can help with both, but the matching characteristics need not exhaust the relevant dimensions.

For an illustrative constant monthly benchmark error $b$, the expected error in an $N$-month cumulative abnormal return is $Nb$. Under the simplifying weak-dependence scaling discussed in the paper, its standard error grows like $\sqrt N$, so apparent significance grows like $\sqrt N$. For the average abnormal return, bias remains $b$ while its standard error declines like $N^{-1/2}$. Longer horizons therefore do not necessarily make an efficiency test more credible: they can make a small persistent benchmark error more statistically prominent. With serial dependence, the long-run variance replaces the elementary independent-return variance; the square-root statement is not an unrestricted theorem for every return process.

A few-day announcement window limits this problem because expected daily returns are small. Extending the window to years changes both the economic question and the exposure to specification error. It also raises the difficulty of selecting a normal estimation period: many event firms have unusual performance both before and after the event.

## Distinct return objects and their implementation

Using notation introduced here to make the discussion executable, a cumulative abnormal return and an average abnormal return are

$$
CAR_i(N)=\sum_{t=1}^{N}a_{it},\qquad AAR_i(N)=\frac{1}{N}\sum_{t=1}^{N}a_{it}.
$$

A buy-and-hold abnormal return relative to a specified benchmark return sequence $r^B_{it}$ is

$$
BHAR_i(N)=\prod_{t=1}^{N}(1+r_{it})-\prod_{t=1}^{N}(1+r^B_{it}).
$$

The corresponding wealth relative is the ratio of these products. An average of firm-level BHARs, a ratio of aggregate terminal wealths, and the compounded return of a monthly rebalanced portfolio are different statistics. A replication must retain the statistic used by the source study instead of switching silently between them.

Fama prefers monthly AARs or CARs for formal tests, while recognizing that BHARs describe a buy-and-hold investor's experience. His reasons include the monthly horizon used to evaluate the benchmark models, greater skewness after long compounding, and misleading interpretations of continued wealth differences as continued abnormal performance. This is an argument about the null being tested, not a claim that compounded wealth is economically meaningless.

The paper's numerical illustration makes the last point transparent. Suppose the event investment returns 10% in year one and its benchmark returns zero. Over the next four years each doubles. The one-year BHAR is 10 percentage points; the five-year BHAR is $1.1\times2-1.0\times2=0.20$, or 20 percentage points. There is no relative performance during years two through five. The wealth ratio stays 1.1, while the wealth difference grows. Consequently, a rising BHAR curve cannot by itself establish slow information incorporation over the entire plotted horizon.

Normal-return controls considered in Section 4 include a firm-specific market model estimated outside the event period, a comparison-period mean, matching stocks or portfolios on characteristics, and cross-sectional asset-pricing models. Firm-specific models can test responses to corporate events but cannot identify a size anomaly merely by absorbing each firm's average return into its intercept. Characteristic matching and factor regressions can address cross-sectional expected-return differences but impose restrictions that may themselves be wrong. Neither class is uniformly superior.

## Calendar-time portfolios and dependence

For a post-event horizon of $H$ months, construct in each calendar month $t$ the set $E_t$ of firms with an eligible event during the preceding $H$ months. Compute its portfolio return or portfolio abnormal return, then rebuild the eligible set monthly. The paper uses five-year windows for issuance examples and three-year windows for several other events. It does not give one universal definition of the exact event-month boundary, treatment of multiple events, delisting rule, or missing-return convention across all studies.

For weights $w_{it}$ summing to one, the abnormal portfolio return is $A_t=\sum_{i\in E_t}w_{it}a_{it}$. Its variance contains both individual variances and covariances:

$$
\operatorname{Var}(A_t)=\sum_iw_{it}^2\operatorname{Var}(a_{it})+2\sum_{i<j}w_{it}w_{jt}\operatorname{Cov}(a_{it},a_{jt}).
$$

The time series of realized portfolio returns incorporates the effect of contemporaneous dependence without estimating every firm-pair covariance separately. Treating event firms' multiyear BHARs as independent can badly understate uncertainty because many events share the same calendar months. A large cross-section does not create equally many independent long-horizon observations.

This portfolio construction addresses cross-sectional dependence, but valid inference still requires an appropriate time-series variance calculation. Membership changes can generate heteroskedasticity, and serial dependence cannot be assumed away merely because returns have been aggregated. The paper discusses heteroskedasticity refinements but does not supply a universal lag rule, bootstrap scheme, or complete standard-error implementation for a new dataset.

Event clustering also changes the estimand. Equal weighting of calendar months gives a quiet month and an issuance boom equal influence. Event-weighted averages answer a different question. Fama discusses dividing each monthly abnormal return by an estimated standard deviation before averaging standardized returns. That produces an average in standardized units, not an ordinary percentage alpha. It should not be confused with inverse-variance estimation of a common unstandardized return. The economic hypothesis should determine the weighting; a replication must record the variance estimator and whether it weights observations or transforms their units.

## Three-factor regression and changing exposures

Equation (1), printed p. 298, is the main displayed empirical specification:

$$
R_{pt}-R_{ft}=\alpha_p+\beta_p(R_{Mt}-R_{ft})+s_pSMB_t+h_pHML_t+\varepsilon_{pt}.
$$

$R_{pt}$ is a monthly rolling event-portfolio return, $R_{ft}$ the one-month Treasury bill rate, and $R_{Mt}$ the value-weighted NYSE/Amex/Nasdaq market return. $SMB$ represents small-minus-big returns, with the paper describing a split at the NYSE size median. $HML$ represents high-minus-low book-to-market returns, using .7 and .3 breakpoints. The full factor-construction recipe, including portfolio intersections and accounting lags, is delegated to the underlying Fama–French work rather than reproduced here.

The intercept is a monthly abnormal-return estimate under this three-factor specification. It is not a model-free statement about mispricing. Changing membership can make factor slopes time varying; changing membership counts can make residual variance time varying. Moreover, Fama explicitly notes that his own three-factor model has trouble explaining returns of small, low-book-to-market stocks, exactly where many issuance samples concentrate. A negative equal-weight issuance alpha can therefore survive factor adjustment while disappearing under direct characteristic matching.

Equal- and value-weight portfolios answer different economic questions. Equal weighting places more influence on tiny firms relative to their market capitalization; value weighting is closer to aggregate invested-wealth exposure. Fama also favors value weights because known benchmark errors are concentrated in small stocks. A small-stock-specific anomaly is not disproved simply because its aggregate wealth effect is small, but its statistical interpretation must confront the benchmark's poor performance in that segment.

## Reported evidence by event family

### Equity issuance

Loughran and Ritter's 1970–1990 sample produces five-year terminal-wealth relatives near 0.70 for IPOs and SEOs compared with size-matched stocks. Brav and Gompers' IPO comparison adds book-to-market matching and excludes IPOs and SEOs from the benchmark; the wealth relative rises to slightly above 1.0. Brav and coauthors report a similar disappearance of the SEO discrepancy under size-and-book-to-market matching. The implication is that poor issuance returns are shared with small growth firms rather than necessarily being caused by the issuance event.

Under value weighting, IPO five-year wealth relatives are at least .86 for all six reported benchmarks, with four above .90. SEO relatives are at least .88, with three above .98. These are benchmark-dependent wealth ratios, not monthly alphas or significance levels.

The monthly regression estimates provide a more precise comparison:

| Event/sample as reported | Equal-weight monthly alpha | Value-weight monthly alpha |
|---|---:|---:|
| SEOs, Brav et al., 1975–1992 | −0.42%, $t=-4.8$ | −0.14%, $t=-1.18$ |
| Non-venture-backed IPOs, Brav–Gompers | −0.52%, $t=-2.80$ | −0.29%, $t=-1.84$ |
| SEOs, Mitchell–Stafford 1960–1993, constant slopes | −0.38% | −0.14%, $t=-1.51$ |
| Same SEO sample, time-varying slopes | −0.24%, $t=-3.64$ | −0.07%, $t=-0.81$ |

Venture-backed IPO intercepts are slightly positive in the reviewed study. The source prints a positive $t=4.47$ beside the negative −0.38% constant-slope SEO intercept. That sign is internally inconsistent with a conventional intercept-over-standard-error statistic, so the table above deliberately does not silently propagate it as a valid signed statistic. Its reported absolute magnitude is 4.47. The detailed time-varying-slope specification is not supplied here and must be obtained from the cited study for exact reconstruction.

### Acquiring firms

For Mitchell and Stafford's 1960–1993 mergers, equal-weight three-year post-event buy-and-hold returns are about 4 percentage points below size-and-book-to-market matched portfolios. The three-year rolling calendar-time portfolio has monthly alpha −0.25%, $t=-3.49$, with equal weights, versus −0.11%, $t=-1.55$, with value weights. These two return measures need not coincide arithmetically because they use different compounding and portfolio constructions.

The reviewed negative post-acquisition performance is concentrated in stock-financed mergers. For mergers without new stock issuance, the negative abnormal returns disappear. This makes it difficult to interpret merger underperformance as an independent phenomenon separate from the SEO result. It does not establish a causal financing effect, since payment method is not randomly assigned.

### Stock splits

Studies covering 1975–1991 report roughly 7% abnormal returns during the year after a split. Benchmarks control for size and book-to-market, and one study also controls for prior one-year returns. An earlier 1927–1959 study finds no cumulative abnormal drift over the following 30 months. Fama treats the discrepancy as a failed cross-period robustness test. Different periods and methods are not a controlled random holdout, so this is evidence of instability rather than proof that no regime-specific effect can exist.

The newer studies also show the compounding issue directly: returns in years two and three are near zero relative to benchmarks, but three-year BHAR grows from roughly 7% to 12%. A research implementation should plot incremental abnormal returns as well as cumulative wealth statistics to distinguish subsequent drift from growth of an earlier wealth gap.

### Repurchases and self-tenders

Mitchell and Stafford's 1960–1993 evidence includes 475 self-tenders and 2,542 open-market repurchases. Size-and-book-to-market matched three-year BHARs are about 9% and 19%, respectively. Yet the combined three-year rolling event portfolio's three-factor alpha is only 0.11% per month with equal weights, $t=1.62$, and −0.03% with value weights, $t=-0.34$. These discrepancies show that a large long-horizon characteristic-matched wealth difference need not imply a statistically reliable calendar-time factor alpha.

The comparison does not prove characteristic matching is wrong or factor regression right. The paper's point is that seemingly closely related controls can produce materially different conclusions. Their estimands and benchmark restrictions need to be examined before declaring one procedure a definitive test.

### Listings, dividends, spinoffs, and proxy contests

For new NYSE listings and Nasdaq-to-Amex moves in 1962–1990, Dharan and Ikenberry report a three-year CAR of −7.02%, $t=-2.78$, under size-and-book-to-market controls. The negative performance is confined to firms below the NYSE–Amex size median. Fama argues that incomplete cross-firm covariance adjustment may undermine significance. He cites other event samples in which ignoring covariance makes the estimated standard error about 50% too small, but explicitly does not claim that this exact correction applies to listings. A replication must estimate the relevant covariance effect rather than halve this study's $t$ statistic mechanically.

Dividend initiations and omissions are studied over 1964–1988. Initiation underperformance is not the claim: the initially reported effect is positive post-initiation performance, which disappears under size-and-book-to-market benchmarks in a subsequent review. Negative omission performance survives that comparison but is concentrated in the second half of the sample. The appropriate next empirical test in the paper is a new sample, not an automatic declaration that both effects are eliminated.

For spinoffs and parents in 1965–1988, positive three-year BHARs relative to size-and-industry matches are confined to firms subsequently acquired. Reported $t$ statistics range from .58 to 2.55, with event returns treated as independent. For proxy contests in 1968–1987, overall post-event negative returns are not statistically reliable. Significance appears only for roughly 50 contests where dissidents win board representation, a subgroup result the paper regards as lacking an ex ante prediction. These are distinct concerns: dependence, selective subsamples, and possible takeover composition should not be merged into one generic explanation.

## What the behavioral-model comparison actually tests

The paper reviews two specific models rather than all possible behavioral finance. In Barberis–Shleifer–Vishny, actual earnings follow a random walk, but investors infer either a mean-reverting or a trending regime. Belief in mean reversion creates underreaction; a sufficiently persistent run induces trend extrapolation and eventual reversal. In Daniel–Hirshleifer–Subrahmanyam, overconfidence in private signals and biased attribution of public information generate short-run continuation and eventual correction. These are qualitative model accounts in this review; their state transitions, equilibrium equations, and parameter estimates are not reproduced.

Fama's criticism is that each model should explain events outside the set it was designed to fit. Long-run reversal follows seasoned offerings, listings, and some acquisitions, but continuation appears around dividends, splits, and spinoffs. Table 1 summarizes signs, not effect-size estimates or a formal meta-analysis. Fama explicitly declines to count underreaction versus overreaction because classifications can be ambiguous and the review incomplete. Therefore, the paper's description of a roughly balanced split should not be treated as a computed binomial test.

For the selective-event prediction that announcement and subsequent returns share a sign, the table lists consistency for SEOs, dividends, repurchases, splits, and spinoffs, but conflicts for listings and proxy fights. Acquirers have approximately zero announcement returns followed by negative returns. IPOs have positive early performance followed by negative long-run performance. These observations challenge those models' breadth, subject to the same concerns about whether the underlying abnormal returns are reliable.

## Reconstruction scope and conclusions

This source is sufficient to implement the calendar-time architecture, distinguish return measures, formulate the displayed three-factor regression, and reproduce its simple compounding illustration. It is insufficient to recreate every reviewed dataset. Security identifiers, exact event timestamps, duplicate-event exclusions, delisting treatment, accounting availability lags, portfolio-weight dates, complete factor series, and standard-error code generally reside in the underlying studies. Transaction costs, borrowing costs, execution lags, and an investable strategy specification are not supplied. The reported anomalies are statistical return patterns rather than net executable strategies.

A faithful research reconstruction should hold the event sample fixed while comparing size-only matching, size-and-book-to-market matching, and factor adjustment; calculate both equal- and value-weight results; separate incremental drift from accumulated wealth; and use calendar-time inference that retains overlapping-event dependence. These are operational implications of the paper. They should not be presented as a single experiment Fama ran with one common dataset.

The strongest conclusion is methodological: a long-horizon abnormal-return claim is fragile if a plausible change in benchmark, weighting, dependence treatment, or sample period overturns it. The larger claim that efficiency survives is Fama's interpretation of the evidence available in 1998. The source neither resolves all behavioral models nor establishes the present-day status of the anomalies. Its enduring research contribution is to make the expected-return model and the sampling design part of the object being scrutinized.
