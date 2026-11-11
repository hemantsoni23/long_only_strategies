# Market reaction to earnings news: A unified test of information risk and transaction costs

Qi Zhang, Charlie X. Cai, and Kevin Keasey, *Journal of Accounting and Economics* 56 (2013), 251–266, doi:10.1016/j.jacceco.2013.08.002. [Source PDF](../../Finance/AbnormalReturnsEarnings_ZhangCaiKeasey_2013.pdf). References below use printed pages, with PDF page 1 corresponding to page 251. The entire 16-page article, including its references and footnotes, was read; there is no separate appendix in the supplied file.

## Why this matters

A strong response to an earnings announcement and substantial subsequent drift need not contradict each other. An announcement can convey more information for an opaque firm while the cost of trading that firm's shares delays full incorporation into price. This paper puts those two channels into the same empirical design. Its central result is that information-risk proxies help explain announcement sensitivity, whereas transaction-cost measures largely absorb the positive relationship between those proxies and later drift.

The distinction matters when deciding whether a post-earnings-announcement drift signal should be concentrated in small, volatile, lightly followed securities. Their higher gross returns may be attached to higher implementation costs. In the paper's quarterly long-short portfolios, several positive four-factor alphas disappear after charging half the quoted spread at entry and half at exit on each side. The design is therefore more informative about the difference between gross opportunity and executable return than a regression of future returns on an uncertainty proxy alone.

The contribution is a unified test of previously developed information-content and trading-friction explanations. The authors do not present a new equilibrium theorem or a fully specified trading optimizer. Their innovations are the joint organization of hypotheses, reduction of eight correlated information proxies to three factors, simultaneous estimation of cost and return equations, and comparison of gross and spread-adjusted drift portfolios. The causal interpretation is stronger than the identification details printed in the paper, so the evidence is best read as a coherent set of conditional associations with explicit economic mechanisms.

## Two channels and their different predictions

The information-content hypothesis starts from a low-information pre-announcement price. If private information acquisition is costly or public information sparse, a common earnings release can convey more incremental information. Conditional on the same measured earnings surprise, the announcement return should be more sensitive for a firm with greater information risk. This is a statement about the relevance of the public signal relative to prior information, not a prediction that its earnings are intrinsically more valuable.

The transaction-cost hypothesis points in the opposite direction at the announcement. Information asymmetry raises adverse-selection costs for liquidity suppliers. Higher spreads or other frictions reduce the incentive to trade against a pricing discrepancy, lowering the immediate response per unit of surprise. The same friction can produce subsequent drift as information reaches prices gradually.

Figure 1, page 254, organizes the signs. Information risk has a positive direct effect on the initial earnings-response coefficient and a negative indirect effect through costs, leaving its combined announcement effect theoretically ambiguous. The permanent information-content effect alone should not predict later drift. The cost channel should generate a positive relation between costs and surprise-aligned subsequent returns. These predictions require that the earnings-surprise proxy measures economically comparable news across firms and that the controls adequately separate information environment from trading costs.

A larger announcement response is not evidence of an absence of underreaction, and it is not evidence of overreaction. The relevant comparison is with the full value implication of the news, which is not observed directly. This is why the paper examines both initial and subsequent responses rather than treating one event-window coefficient as a complete efficiency test.

## Universe, dates, and earnings surprises

The sample spans the first quarter of 1993 through the second quarter of 2007. Companies must have their principal location in the United States and trade on NYSE or AMEX. Nasdaq is absent. Real estate investment trusts and closed-end funds are excluded. Firms need at least ten quarterly earnings reports, at least three years of book and market value data, known announcement dates, and no missing CRSP returns during the 60 trading days following each announcement. The starting dataset has 78,294 firm-quarter observations from 4,445 stocks (pp. 252, 256).

The no-missing-future-return condition is consequential: it selects on post-event data availability and may exclude some difficult delistings or other interrupted histories. The article does not report a delisting-return imputation rule, survivor comparison, or a sensitivity test that relaxes this condition. The final multivariate sample has 44,000 events with all required variables, considerably fewer than the headline universe. Approximately 35% of the larger sample has no analyst coverage; analyst dispersion is available for only 44,538 observations.

Quarterly earnings before extraordinary items and discontinued operations come from Compustat, daily stock returns from CRSP, and analyst forecasts from I/B/E/S. Compustat market capitalization is used for size-adjusted returns. Define seasonal unexpected earnings and standardized unexpected earnings by

$$
UE_{i,q}=e_{i,q}-e_{i,q-4},\qquad SUE_{i,q}=\frac{UE_{i,q}}{s_{i,q}},
$$

where $s_{i,q}$ is the standard deviation of seasonal earnings differences over the preceding eight quarters. This is source equation (1). The text's variable subscripts alternate between event time and fiscal quarter, but the intended seasonal comparison is clear. The exact treatment of missing historical quarters, zero denominators, splits, and the relationship between the ten-report screen and the history needed for eight seasonal differences is not fully spelled out.

For each calendar quarter, surprise decile cutoffs use the previous quarter's SUE distribution. This lag is an explicit protection against using the current quarter's complete cross-section to classify early announcements. The regression specifications instead use surprise quintile scores from one to five, together with factor quintile scores. The portfolio test uses extreme deciles. One introductory footnote describes a quintile hedge, but equation (5), Table 7, and the detailed portfolio construction specify deciles 10 and 1; that more explicit definition should govern reconstruction.

## Rebuilding the information-risk factors

Table 1 defines eight raw proxies. They measure different concepts and have different information clocks:

| Proxy | Definition and measurement interval |
|---|---|
| ARBI | Residual variance from a market-model regression of excess returns over trading days $[t-252,t-5]$, relative to announcement day $t$ |
| SIGMA | Standard deviation of weekly market-excess returns over the prior year |
| DISP | Standard deviation of analyst earnings forecasts, divided by prior year-end stock price |
| DTO | Average market-adjusted turnover on $[t-1,t]$ less its average on $[t-54,t-5]$ |
| SUV | Two-day unexpected volume from a regression of volume on absolute returns, divided by the estimation-window prediction-error standard deviation |
| MV | Market capitalization in millions of dollars at the previous year-end |
| COV | Number of analysts issuing quarterly forecasts in the 90 days before the announcement |
| AGE | Years since first CRSP coverage |

Some definitions are incomplete for exact coding. SUV's detailed estimation window and regression specification are delegated to the cited literature. Table 1 calls ARBI a residual variance, while the descriptive table reports it in percent and the prose calls the average 2.36% idiosyncratic risk. A variance-versus-standard-deviation choice materially changes factor construction; it cannot be resolved simply by reading the percent sign as a complete definition. This should remain a replication question rather than a silently repaired formula.

DTO and SUV are event-related trading measures, not strictly pre-announcement firm characteristics. DTO explicitly includes announcement-day turnover. Consequently, describing the entire factor set as ex ante information risk overstates its timing. These variables can be available for a day-two portfolio but cannot all be known for a trade before the announcement. Their contemporaneous response may also partly reflect the news itself.

The sample's average capitalization is approximately \$5.218 billion, median \$800 million; average age is 26 years. Covered firms have eight analysts on average and six at the median. Weekly volatility averages 5.04%. Total volatility and arbitrage risk have Pearson correlation 0.92 and Spearman correlation 0.95. These correlations motivate dimensional reduction rather than inclusion of all proxies in one regression.

The authors apply principal-component analysis to the correlation matrix, retain eigenvalues at least one, and rotate the retained factors orthogonally for interpretability. The first three eigenvalues are 2.28, 1.65, and 1.30; the fourth is 0.98. The retained factors explain about 65% of the variation, with reported rotated explained variance totaling 5.23 out of eight standardized inputs. Factor scores have zero mean and unit standard deviation and are stated to be mutually uncorrelated.

Factor 1 is volatility/arbitrage risk: both ARBI and SIGMA load at 0.96, while analyst dispersion loads only 0.28. Factor 2 is opinion divergence/trading activity: DTO and SUV each load at 0.90. Factor 3 initially represents size and information availability, with MV loading 0.83, coverage 0.77, and age 0.50. The authors reverse Factor 3's sign so a higher score consistently means greater information risk. Sign orientation must precede economic interpretation and sorting.

Rotated loadings are not automatically the standardized scoring coefficients needed to reproduce scores. The exact rotation criterion, scoring method, estimation sample treatment, and whether scores are fitted once or refreshed over time are not fully reported. A full-sample factor fit can support descriptive inference but is not automatically a point-in-time investment signal. Table 3D also prints Factor 3's minimum as 1.46 and maximum as −13.11, inconsistent with the ordering of extrema, apparently reflecting an incompletely relabeled sign reversal. The intended high-risk direction is explicit in the text; the printed extrema should not be used to set numerical bounds.

## Transaction costs and the joint model

The main cost proxy, BAS, is the average percentage bid-ask spread on announcement day and the following day. The alternative, LDV, uses the Lesmond–Ogden–Trzcinka limited-dependent-variable estimator with daily stock and market returns over the 240 trading days before announcement. The intuition is a no-trade interval: sufficiently small latent return innovations fail to overcome costs, so observed returns are zero. LDV estimates a threshold-related friction from this censoring. This article does not reproduce the latent-return likelihood, threshold parameterization, or estimation constraints; implementing LDV requires the cited method, not merely counting zero-return days.

The cost regression is

$$
Cost_i=a+\sum_{k=1}^{3}\gamma_kF_{ik}+\theta'Z_i+u_i,
$$

where $Z$ includes previous-year book-to-market, ROA and sales growth, a NYSE indicator relative to AMEX, and average price on announcement day and day one. Table 4 uses 44,000 events and heteroskedasticity-consistent statistics. On BAS, coefficients are 0.131 for Factor 1, $t=26.68$; −0.051 for Factor 2, $t=-13.47$; and 0.066 for Factor 3, $t=25.76$. The corresponding LDV coefficients are 0.069, −0.027, and 0.071. Adjusted $R^2$ is 0.2662 for BAS and 0.274 for LDV.

Factor 2's negative sign is a substantive exception to a simple “all information risk raises costs” story. Its trading-volume content can improve liquidity even while disagreement rises. The authors explicitly interpret it as capturing trading activity as well as informational disagreement. Factor 2 should not be pooled indiscriminately with volatility and small size as a uniform adverse-selection measure.

The initial-response equation is

$$
CAR_i=a+bS_i+\sum_{k=1}^{3}\lambda_kF_{ik}S_i+\kappa Cost_iS_i+\eta'X_iS_i+\epsilon_i.
$$

Here $S$ and $F$ are one-to-five quintile scores, and $CAR$ is cumulative size-adjusted return on announcement day and the next day. Controls interacted with surprise are earnings persistence, earnings predictability, a loss indicator, a fourth-fiscal-quarter indicator, previous-fiscal-quarter book-to-market, and market beta. Persistence is described as the autoregressive coefficient estimated over the preceding two years; predictability is the variance of absolute seasonal unexpected earnings over that interval. Beta uses one year of daily returns ending in the month before announcement.

When costs are included, the authors estimate the cost and response equations simultaneously by GMM, motivated by correlated liquidity shocks and cost endogeneity. A reproducible GMM implementation needs moment conditions, instruments, weighting-matrix construction, and covariance estimation. These are not supplied in sufficient detail. Joint estimation can exploit residual correlation, but does not by itself establish that contemporaneous spreads are causally exogenous in the return equation. An instrument's exclusion restriction cannot be inferred merely because a variable occurs in the cost equation.

The two-channel logic can be expressed algebraically without treating it as an identified causal model. If the earnings-response slope is $b+\lambda_kF_k+\kappa Cost$ and the cost equation changes by $\gamma_k$ for a unit change in $F_k$, then its total derivative is $\lambda_k+\kappa\gamma_k$. With $\lambda_k>0$, $\kappa<0$, and $\gamma_k>0$, the cost channel offsets part of the direct information-content response. This is a useful representation of the authors' economic argument. It is not a numerical decomposition one can directly compute from their displayed tables because the cost regression uses standardized continuous factors while the response equation uses factor quintiles, and the system's identifying assumptions remain incomplete.

For Factor 2 the sign changes: its negative association with costs implies that an activity-related liquidity channel could reinforce rather than offset announcement sensitivity. That is one reason its weak two-day interaction should not be forced into the same narrative as Factors 1 and 3. The orthogonality of statistical scores does not imply that every factor acts through an identical economic path.

The two transaction-cost proxies also have different simultaneity exposure. BAS is measured during the response window and can change with the news and resulting order flow. LDV uses the preceding 240 days, avoiding direct use of the current announcement's spread but potentially missing a sharp event-specific liquidity shock. Agreement between their coefficient signs is informative precisely because their measurement errors and clocks differ. It does not establish that either captures every component of executable cost or provides an excluded instrument for the other.

## Announcement-window results

Table 5 reports returns in percentage-point-scale coefficients. Without costs, the two-day surprise coefficient is 0.323, $t=6.53$. The Factor 1 interaction is 0.018, $t=2.67$, and Factor 3 interaction 0.016, $t=2.38$. Adding BAS increases those interactions to 0.090 and 0.060, with $t=7.83$ and 7.22. Adding LDV gives 0.114 and 0.076, with $t=8.87$ and 8.28. This is the pattern expected when a positive information-content effect was partly offset by a negative cost channel in the omitted-cost specification.

The cost-surprise interaction is −0.818 with BAS, $t=-9.76$, and −0.915 with LDV, $t=-10.78$. These are slope interactions, not unconditional cost effects. They should not be read as the effect of adding a one-percentage-point spread to every stock without checking the exact cost units and all interaction values. The article describes percentage spreads but does not give enough data-processing detail to resolve every raw-versus-percent storage convention from the printed regressions.

Factor 2 does not show a reliable two-day interaction: 0.006 with $t=0.93$ without costs, 0.002 with $t=0.22$ for BAS, and 0.009 with $t=1.30$ for LDV. The last entry is printed with three significance stars despite its small statistic. Similar star inconsistencies occur elsewhere, including sales-growth cost-regression entries with $|t|$ below 1.2. The numerical statistics, rather than the stars, are the defensible basis for interpretation.

The source's illustration holds other terms at zero and computes approximately −0.72% for surprise category one and +0.57% for category five from the no-cost intercept and slope. Because factor scores in this specification run from one to five, setting every interaction factor to zero is outside their observed categorical support. It illustrates the baseline term algebra; it is not a representative fitted return for an actual low- or high-surprise firm.

A robustness response measure extends from four quarters before the announcement through day one after it. Its Factor 1 and Factor 3 interactions remain positive, and cost interactions negative, for both proxies. This wider interval incorporates pre-event price discovery and has much larger coefficients; it should not be labeled a longer purely post-event announcement window. Substituting consensus analyst forecasts for the seasonal expectation model reportedly gives qualitatively similar results, addressing the possibility that surprise measurement is systematically better for opaque firms. Those detailed results are not tabulated.

## Subsequent drift and calendar-quarter inference

The post-event return $R_{1Q}$ runs from day two after the announcement through the day before the next announcement. $R_{4Q}$ instead ends 240 trading days after the event. The regression extends the announcement equation with main-effect controls as well as surprise interactions:

$$
R_{i,h}=a+bS_i+\sum_k\lambda_kF_{ik}S_i+\kappa Cost_iS_i+\sum_j\eta_jX_{ij}S_i+\sum_j\rho_jX_{ij}+\epsilon_i.
$$

Price and institutional ownership are interaction controls, both ranked from one to five. Ownership is the fraction held by Form 13F filers in the preceding quarter. Book-to-market and beta control conventional expected-return variation. The caption states that main effects of variables interacted with surprise are included even though all are not displayed. When costs are present, this equation and the cost equation are jointly estimated by GMM each quarter, and coefficients are averaged in Fama–MacBeth fashion.

Table 6 says there are 56 quarterly regressions, while 1993Q1–2007Q2 contains 58 calendar quarters. The missing endpoints or data filters producing that difference are not explicitly identified. Four-quarter outcomes also overlap across adjacent formation quarters; the article does not specify a corresponding serial-correlation adjustment to the reported average-coefficient statistics. These are material inference and reconstruction gaps.

Without costs, the size-related Factor 3 interaction is positive: 0.161, $t=3.52$, over one quarter and 0.320, $t=3.03$, over four. With BAS, it becomes effectively zero over one quarter and −0.443, $t=-1.31$, over four. With LDV it is −0.215, $t=-1.10$, and −0.123, $t=-0.34$. The positive size-related drift relationship therefore disappears after controlling for measured costs.

The cost interaction is positive in both horizons: BAS 8.633, $t=2.29$, and 33.487, $t=2.17$; LDV 7.653, $t=2.09$, and 20.317, $t=2.02$. These estimates support the friction account but are much less precisely estimated than the initial-response interactions. Information risk does not literally become irrelevant in every specification: the Factor 1 interaction is negative and marginally significant in the one-quarter LDV model, and negative with $t=-2.20$ in the four-quarter BAS model. The main result concerns removal of a positive drift association, especially Factor 3, not universal zero coefficients.

## Gross and spread-adjusted hedge returns

For each event, the authors calculate one quarter's post-announcement return, then aggregate events in each calendar quarter into five information-risk quintiles. Within each risk group, the hedge buys surprise decile ten and shorts decile one. The quarterly return is regressed on next quarter's market excess return, SMB, HML, and momentum UMD:

$$
H_t=\alpha+\beta_M(R_{m,t}-R_{f,t})+\beta_SSMB_t+\beta_HHML_t+\beta_UUMD_t+\epsilon_t.
$$

Because announcements occur throughout a calendar quarter and positions end before their next announcements, the event holding intervals do not coincide exactly with the matched calendar-quarter factor returns. The method is a portfolio diagnostic, not a fully documented daily self-financing backtest. The article does not fully specify aggregation weights, cash management, contemporaneous overlapping positions, or how a single capital budget is maintained.

Let $s^{in}$ and $s^{out}$ be entry- and exit-day percentage spreads. The round-trip deduction for one stock is $c=(s^{in}+s^{out})/2$. Entry is day two; exit is the day before the next announcement. For the hedge, subtract the long-side cost and the short-side cost. Operationally the source subtracts costs from the long stock return and adds them to the stock return being subtracted as the short leg. This sign convention correctly charges both sides. It is distinct from BAS in the regressions, which averages spreads on event day and day one.

Table 7 alphas are quarterly decimal returns. In the highest size-related risk group, gross alpha is 0.053, or 5.3%, $t=2.70$; after spreads it is 1.1%, $t=0.57$. The fourth group moves from 3.5%, $t=2.64$, to −0.2%, $t=-0.17$. For the highest disagreement group, 5.1%, $t=2.44$, becomes 1.9%, $t=0.92$. For volatility, the fourth group moves from 3.2%, $t=2.11$, to −0.4%, $t=-0.23$, while the highest group's gross 1.9% is already insignificant, $t=1.03$, and becomes −2.4%.

The evidence is not monotonically increasing across every risk sort. The lowest volatility group has significant gross alpha of 2.3%, $t=3.17$, and the fourth disagreement group has negative gross alpha. No cost-adjusted portfolio shows a statistically significant positive alpha, which supports the authors' narrower implementation conclusion. Nonrejection does not establish an exact zero expected return, and several adjusted alphas are significantly negative rather than simply “explained” by risk factors.

Quoted spread crossing is only one execution model. The test omits explicit commissions, stock-borrow fees and availability, price impact, order size, and capital constraints; passive execution could also differ from paying the quoted half-spread. The exercise shows that a plausible simple trading-cost charge is large relative to these historical gross returns. It does not prove that no feasible earnings strategy can be profitable under any execution policy.

## What can be carried into research

The strongest reusable lesson is to separate a signal's response sensitivity from its friction-conditioned forecast of later returns. Orthogonalized information proxies help manage collinearity, but do not make their economic meanings pure or causal. Event-time trading activity, missing analyst coverage, sample selection on future returns, and imperfect cost measurement all affect the estimated channels.

A faithful reconstruction should lock the NYSE/AMEX historical sample, lagged surprise breakpoints, factor signs, two distinct spread clocks, and one- versus four-quarter outcome definitions before pursuing modern extensions. It should explicitly resolve the ARBI scale, factor scoring and rotation details, GMM moments, calendar-quarter exclusions, and overlapping-return covariance. The paper reports qualitative robustness to a fourth factor dominated by analyst dispersion, a larger sample omitting dispersion and setting uncovered firms' analyst counts to zero, analyst-based surprises, and alternative risk-factor models. Those are supportive author-reported checks, not fully tabulated replications. The published evidence supports transaction costs as an important link between information environment and observed drift; the supplied article leaves enough estimator and portfolio details unspecified that an exact numerical reproduction requires additional documentation.
