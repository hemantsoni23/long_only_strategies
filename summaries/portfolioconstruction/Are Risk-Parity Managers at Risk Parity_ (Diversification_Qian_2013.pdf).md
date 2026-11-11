# Are Risk-Parity Managers at Risk Parity?

Edward Qian. *The Journal of Portfolio Management*, Fall 2013, printed pp. 20, 22–26 in the supplied copy. Source: [Diversification_Qian_2013.pdf](../../Finance/Diversification_Qian_2013.pdf). All seven PDF pages were inspected, including Exhibits 1–5 and the reporting-history endnote. The PDF jumps from printed p. 20 to p. 22; no missing analysis is assumed or reconstructed from the pagination alone.

## Why this matters

A portfolio can allocate equal risk to its named holdings while concentrating most of its economic exposure in one direction. Likewise, substantial bond notionals and leverage do not establish that a manager is balancing growth and inflation risks. Qian turns this observation into a manager-diagnostic exercise: estimate effective exposures from returns, translate those exposures into risk contributions, and aggregate them into economically meaningful groups. Applied to seven products marketed as risk parity, the exercise identifies three whose estimated risk balance differs substantially from the author's definition.

The practical contribution is a way to interrogate a product label when holdings are unavailable. It is not a new optimal risk-parity algorithm, and it does not prove that equal contributions to three risks maximize utility or expected returns. The central empirical claim concerns the exposure composition of a small historical manager sample. An implementer should distinguish that diagnostic claim from both a forecast of subsequent performance and a general prescription for portfolio design.

## What is being equalized?

The author rejects three shortcuts. First, equal capital allocation is not equal risk allocation: a conventional 60/40 stock/bond portfolio is said to obtain approximately 90–95% of its risk from stocks. Second, equal contributions by individual asset label depend on how the universe is partitioned. Four equity categories and one bond category can place 80% of risk in equities even when each category contributes one fifth. Reversing the counts creates the reverse problem. Third, a formally balanced number of equity and fixed-income categories does not fix the problem if the fixed-income categories contain growth-sensitive credit exposures.

In particular, the article treats high yield as predominantly equity risk. Investment-grade credit and emerging-market debt combine interest-rate and equity risks; inflation-linked bonds combine interest-rate and inflation risks. Thus, a position's contractual description as a bond is insufficient for its economic classification. The correct unit for the author's argument is the underlying risk premium or exposure, rather than the instrument count or capital committed.

Qian organizes macroeconomic sensitivity around growth and inflation and proposes that an asset-allocation risk-parity portfolio should have balanced contributions from three tradable risk sources: equity, interest rates, and inflation. Stocks proxy equity risk, nominal government bonds mainly proxy interest-rate risk, and commodities proxy inflation risk. These are operational asset-based proxies for macroeconomic risks; the study does not estimate innovations to a structural growth-and-inflation model. Nor does it require that every reported contribution be exactly one third. Its favorable classifications allow substantial differences across the three sources.

The portfolio construction examples support a general lesson independent of the three-source choice: equal-risk optimization is only meaningful relative to an economically defensible representation of the opportunity set. Splitting an existing holding into several nearly identical line items should not transform a concentrated economic exposure into a diversified one.

## Manager sample and return-based design

The sample contains seven risk-parity managers from eVestment, anonymized A through G. The stated sample is October 2009 through September 2012, using monthly returns. That nominally supplies 36 monthly observations per manager, but the endnote says one manager stopped reporting in June 2012. The paper does not identify that manager or explain whether its regression uses 33 observations, whether all fits use a common shorter sample, or whether another missing-data treatment was applied. A faithful replication must retain this uncertainty.

The short window is deliberate. Many other managers did not have sufficient return histories, and the author argues that strategies changed after the 2008 crisis, making older returns less representative of then-current styles. This reduces historical comparability while potentially improving relevance to the 2009–2012 product definitions. It also makes the sample conditional on available histories. The paper supplies no population count, asset-weighting scheme, backfill assessment, fee convention, share-class identifiers, or disclosure of whether the anonymous series are live composites or another reporting unit.

The style analysis extends Sharpe's return-based approach from long-only unlevered portfolios to long-only leveraged portfolios. Twelve return indices represent the candidate exposures. This is a moderate universe chosen to cover manager investments without creating an unnecessarily large collinearity problem. The author acknowledges that effective asset weights can be sensitive to the index selection, while arguing that aggregate economic risk allocations are more robust because substitution tends to occur between indices with similar risks. No formal sensitivity table establishes the size of that robustness.

A useful implementation reconstruction is to collect a monthly manager vector $y$ and an aligned matrix $X$ of index returns and solve a nonnegative regression,

$$
\min_{w\geq0,\alpha}\ \sum_{t\in\mathcal T}(y_t-\alpha-X_t w)^2.
$$

This equation formalizes the stated extension, but is not a fully specified optimization problem printed in the article. In particular, the source does not state whether an intercept is included, whether the regression uses total or excess returns, or whether leverage is capped. The usual unlevered restriction $\mathbf1^\top w=1$ must be relaxed to accommodate the reported exposures above 100%. A replication should report its chosen intercept, financing, and constraints explicitly rather than present them as documented author settings.

If total returns are used for a levered portfolio, financing is economically material. A natural cash treatment is

$$
r_{p,t}=\sum_jw_jr_{j,t}+(1-\mathbf1^\top w)r_{f,t}+\epsilon_t.
$$

Equivalently, regress excess returns on index excess returns under a common borrowing/lending rate. The article does not establish that it uses this treatment or disclose actual financing spreads. Estimated exposure sums should therefore be interpreted as style-implied leverage, not an audited balance-sheet or derivatives-notional measure.

## Reported effective exposures

Exhibit 1, printed p. 23, gives the following coefficients as percentages of portfolio capital. The table below preserves the twelve proxy labels and reported rounded values.

| Index | A | B | C | D | E | F | G |
|---|---:|---:|---:|---:|---:|---:|---:|
| DJ-UBS commodities | 18 | 7 | 15 | 25 | 21 | 13 | 17 |
| Barclays US Treasury | 0 | 43 | 66 | 38 | 65 | 17 | 0 |
| WGBI ex US | 87 | 93 | 57 | 93 | 52 | 9 | 74 |
| Barclays MBS | 0 | 0 | 0 | 0 | 0 | 18 | 7 |
| Citi US TIPS | 57 | 79 | 46 | 29 | 55 | 50 | 37 |
| Barclays Credit | 30 | 18 | 7 | 0 | 0 | 15 | 0 |
| Citi emerging-market debt | 0 | 7 | 0 | 1 | 0 | 0 | 14 |
| Barclays US high yield | 1 | 0 | 4 | 0 | 0 | 8 | 32 |
| S&P 500 | 0 | 0 | 8 | 15 | 4 | 37 | 2 |
| MSCI ex US | 22 | 11 | 3 | 0 | 28 | 19 | 19 |
| Russell 2000 | 13 | 9 | 15 | 5 | 8 | 0 | 15 |
| MSCI emerging markets | 0 | 2 | 5 | 0 | 0 | 1 | 9 |
| Reported total leverage | 228 | 269 | 226 | 205 | 232 | 188 | 225 |
| Reported $R^2$ | 92 | 94 | 95 | 82 | 89 | 96 | 96 |

Summing rounded coefficients does not always reproduce the reported total exactly; for example, D's displayed constituents sum to 206%, while total leverage is 205%. This is a rounding issue in the published presentation, not a reason to silently alter a coefficient. The analysis lacks full-precision fitted weights and return residuals.

Six fits have $R^2$ of 89% or more; D is lowest at 82%. These are in-sample explanatory measures with up to twelve candidate exposures and only about three years of monthly observations. They establish that combinations of the chosen indices track the reported manager series reasonably well, not that the inferred weights are uniquely identified holdings.

B has the highest leverage at 269%, but its heavy sovereign-bond and TIPS exposure need not produce the highest volatility. F has only 188% reported leverage, yet its four equity index coefficients plus high yield total approximately 65% of capital. For F, leverage and economically risky asset composition point in different directions. The comparison illustrates why notional exposure is not itself a risk contribution.

## From exposures to risk allocations

After estimating effective weights, Qian uses a covariance matrix from a longer history of monthly index returns. The three-year manager window is considered too short and too dependent on its macroeconomic environment for estimating strategic risk allocations. Unfortunately, the article does not give the covariance window's beginning or end, index-extension methods, currency treatment, or covariance estimator. This missing specification is a principal obstacle to numerical replication of Exhibits 2–3.

The standard volatility contribution calculation consistent with the risk-budgeting framework is

$$
\sigma_p=\sqrt{w^\top\Sigma w},\qquad
RC_j=\frac{w_j(\Sigma w)_j}{\sigma_p},\qquad
q_j=\frac{w_j(\Sigma w)_j}{w^\top\Sigma w}.
$$

Here $RC_j$ is in volatility units, $q_j$ is a fraction of total risk, and $\sum_jq_j=1$ when the covariance model covers the portfolio. These equations are an explicit reconstruction of the implied calculation; the article describes the operation verbally rather than providing formulas and software. Negative marginal contributions are mathematically possible when assets hedge others. One should not replace this calculation by proportional standalone volatilities, since that drops the covariance effects being measured.

The next step aggregates contributions into equity, interest-rate, and inflation sources. For pure proxy groups, contributions can be summed directly. For hybrid classes, the paper's verbal classifications are not enough to recover a unique numerical allocation: credit, emerging-market debt, and TIPS contain more than one source. A factor decomposition could write returns as $r=Bf+u$ and exposures as $b=B^\top w$, giving factor contributions $b_k(\Omega b)_k/\sigma_p$ when factors have covariance $\Omega$. But that is one possible reconstruction, not a disclosed author procedure. The loadings, residual-risk allocation, and mapping of hybrid classes must be obtained or explicitly chosen to reproduce the reported bars.

Uniformly scaling all risky weights changes volatility and absolute contributions proportionally but leaves fractional contributions unchanged under a fixed covariance model. Therefore, simply raising or lowering leverage cannot fix an unbalanced vector of risk shares. The exposure composition must change. This mathematical implication explains the paper's distinction between leveraging low-risk assets and actually balancing economic risks.

## Main findings and event comparisons

Exhibit 3 aggregates equity and inflation contributions as “risk-on,” and interest-rate contributions as “risk-off,” reflecting the market behavior of 2009–2012. The exact printed allocations are:

| Manager | Risk-on | Risk-off |
|---|---:|---:|
| A | 67% | 33% |
| B | 33% | 67% |
| C | 60% | 40% |
| D | 64% | 36% |
| E | 66% | 34% |
| F | 86% | 14% |
| G | 93% | 7% |

F and G are judged too exposed to growth-sensitive assets, despite substantial fixed-income notionals. G's 93/7 split resembles the economic imbalance of a conventional 60/40 portfolio. B fails the author's criterion in the opposite direction: approximately 67% interest-rate risk, 21% equity risk, and 13% inflation risk, with the apparent 101% total due to rounding. This is a more defensive allocation under the selected historical interpretation. A, C, D, and E are classified as reasonably balanced. The text describes their individual three-way contributions as roughly 20–40%; the plot places A's equity bar slightly above 40%, so the interval should not be mistaken for a formal decision boundary.

The study then compares exposure estimates with returns in selected market episodes. December 2010 is the risk-on example, with rising risky assets and rising government bond yields. Exhibit 4 plots December returns against estimated equity-plus-inflation risk shares. Visually, the manager near 33% risk-on earned roughly 0.1%, while the high-risk-on managers earned about 3.8%; these are graph readings, not tabulated exact estimates. The relationship is positive but not perfectly monotonic among the intermediate managers.

August–September 2011 is the risk-off example. Risky assets sold off while Treasury yields fell to new lows. Exhibit 5 shows that managers with small interest-rate risk allocations suffered the largest losses. The plot places the 7% risk-off manager near −13.5%, the 14% manager near −8.5%, and the 67% manager near −1.7%, again approximately. A 60% MSCI World/40% WGBI comparator lost 6.6% over those two months. F and G therefore underperformed even that risk-concentrated benchmark during the chosen defensive episode.

These examples are economically consistent with the estimated exposures. They are not independent out-of-sample tests: both episodes belong to the return window used to infer styles. The paper reports no regression slopes, standard errors, formal correlation tests, or confidence intervals for the seven-point event comparisons. Its description of the events as validation is best understood as an in-sample interpretation check, not a statistical rejection of alternative models.

## What can and cannot be reproduced

The analysis can be rebuilt as a transparent sequence: obtain the seven monthly manager histories; align the twelve index histories; fit a documented long-only leverage-permitting style model; preserve unrounded coefficients and residuals; estimate an explicitly specified longer-run covariance matrix; map pure and hybrid exposures to the three economic sources; calculate contributions; and reproduce the two selected event plots. Repeating the fit with fewer redundant indices and alternative covariance windows would test the claimed robustness of aggregated risk shares. Such sensitivity work is a proposed extension, not a reported robustness result.

Exact reproduction from the PDF alone is not possible. Manager identities, fees, currencies, financing conventions, one incomplete history, regression intercept and constraints, the longer covariance window, and the numerical hybrid-risk mapping are undisclosed. Nor is there a prospective rebalance rule or trading strategy to reproduce: this is an ex post exposure diagnosis, not a specified investable backtest.

The substantive takeaway is to evaluate the risk composition behind an allocation product, particularly where instrument labels obscure credit or inflation sensitivity. The finding that three of seven products depart from one definition of risk parity should not be generalized to the entire manager universe. It also does not establish that those departures were mistakes: they could reflect deliberate strategic views, changing exposures, model misspecification, or reporting differences. The paper's useful discipline is to make that distinction observable and discussable through economic risk contributions.
