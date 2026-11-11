# In Search of Distress Risk

John Y. Campbell, Jens Hilscher, and Jan Szilagyi. *The Journal of Finance* 63(6), December 2008, pp. 2899–2939. Source: [CreditRisk_Campbell_2008a.pdf](../../Finance/CreditRisk_Campbell_2008a.pdf), 41 PDF pages. The complete article, data appendix, rotated tables, figures, and references were read. Printed page $p$ is PDF page $p-2898$.

## Why this matters

The paper separates two questions often conflated in equity factor discussions: which firms are likely to fail, and whether investors earn compensation for holding their equity. A richer monthly failure model predicts corporate distress better than the authors' implementation of Merton distance to default. Stocks ranked as distressed then earn lower average returns despite higher volatility, stronger market exposure, and substantial small-cap and value-factor loadings. Risk adjustment makes the underperformance larger rather than explaining it away.

This challenges the interpretation that the size and value premiums are simply payment for bearing default risk. It also offers an implementable historical distress score, with important qualifications: its future-horizon score is a conditional failure probability at a particular date, not cumulative default probability over a year; the strategy evidence is gross of trading and borrowing costs; and the strongest effects occur in stocks that are difficult to trade or short.

The paper does not prove that a current distress strategy is profitable, that all credit risk is negatively priced, or that a particular behavioral explanation is correct. It establishes an empirical equity-return puzzle in a 1981–2003 portfolio sample and documents which explanations survive its diagnostics.

## Contribution relative to earlier work

Dynamic failure prediction follows Shumway and Chava–Jarrow rather than treating each firm as a single static observation. Accounting-based bankruptcy scores and structural default models are prior benchmarks. The extensions are market-value scaling of accounting variables, smoothed histories of profitability and stock performance, additional cash, market-to-book, and share-price variables, and horizon-specific estimation. The asset-pricing contribution is to sort stocks using recursively estimated failure scores and examine return, factor exposure, size/value, liquidity, ownership, earnings-announcement, and predictor-level evidence together.

The model is deliberately reduced form. It does not identify the causal effect of leverage, liquidity, or volatility on failure. Its coefficients weight correlated predictors to forecast an event. For example, size changes sign after price per share is included at the shortest horizon; that is a conditional forecasting relationship, not evidence that making a firm larger causes imminent failure.

## Event definitions and sample construction

The bankruptcy indicator equals one in a month with a Chapter 7 or Chapter 11 filing. The KRIS/Chava–Jarrow data combine the Wall Street Journal Index, SDC, SEC filings, and the CCH Capital Changes Reporter. Bankruptcy observations span January 1963–December 1998. Acquisition or a nonbankruptcy disappearance does not count as bankruptcy.

The broader failure indicator covers January 1963–December 2003 and includes bankruptcy, financially motivated delisting, or a D rating. This catches some out-of-court distress and firms whose stock disappears before formal default. It also makes the target sensitive to exchange listing rules. Financial delistings include failure to maintain minimum capitalization or price and certain filing/payment failures; mergers and minor filing delays are examples of nonfinancial exits.

CRSP daily and monthly equity data are merged with quarterly COMPUSTAT accounts. The best full-sample regression contains 1,695,036 firm-months and 1,614 failures; the bankruptcy regression has 1,282,853 firm-months and 797 bankruptcies. These are complete-input modeling samples, not the total counts in the event database. Table I, for example, records 324 failures among an average 8,817 active firms in 2001, a 3.67% annual ratio. Failures and bankruptcies closely coincide early in the sample but diverge sharply in the late 1990s.

Quarterly accounting availability is sparse before the early 1970s. Thus the nominal 1963 start overstates the weight of that early period in the estimation. All firm-months receive equal likelihood weight, so the statistical model is heavily influenced by small listed companies and later years with more observations. The sample is not initially restricted to CRSP share codes 10 and 11, though the authors report robustness to that restriction. Financial firms are retained; sector interactions are examined rather than imposing a blanket exclusion.

## Exact predictors and units

Let $ME$ be equity market capitalization, $TL$ total book liabilities, $NI$ quarterly net income, and $MTA=ME+TL$. The key accounting ratios are

$$
NIMTA=\frac{NI}{MTA},\qquad TLMTA=\frac{TL}{MTA},\qquad CASHMTA=\frac{\text{cash and short-term investments}}{MTA}.
$$

The older comparison variables are $NITA=NI/TA_{adj}$ and $TLTA=TL/TA_{adj}$, where

$$
TA_{adj}=TA+0.1(ME-BE).
$$

Book equity is adjusted similarly when constructing market-to-book. Remaining negative adjusted equity values, just under 2% of observations, are replaced by a small positive value printed as \$1, putting their market-to-book ratios in the right tail. A replication must align this floor with the accounting database's currency units; the prose does not supply a fully executable currency-unit map.

Market variables are

$$
EXRET_{it}=\log(1+R_{it})-\log(1+R_{S\&P500,t}),
\qquad RSIZE_{it}=\log\frac{ME_{it}}{ME_{S\&P500,t}},
$$

and $PRICE=\log[\min(\text{unadjusted price per share},15)]$, with price in dollars. The \$15 upper cap is applied before taking logs. A current split-adjusted historical price is not interchangeable with the contemporaneous nominal share price used to detect proximity to listing thresholds.

Volatility uses daily simple returns over the last three months, annualized and centered at zero rather than the sample mean:

$$
SIGMA_{it}=\left[\frac{252}{N-1}\sum_{k\in\text{last three months}}r_{ik}^2\right]^{1/2}.
$$

It is missing if fewer than five nonzero returns are observed. Missing volatility is replaced by its cross-sectional mean. This retains illiquid firms that may be especially likely to fail; it is an imputation choice, not proof that missingness is innocuous. A missing-volatility dummy is not significant in the authors' tests.

Profitability and excess-return histories use geometrically declining weights with $\phi=2^{-1/3}$, so weight halves every quarter:

$$
NIMTAAVG=\frac{1-\phi^3}{1-\phi^{12}}\sum_{j=0}^{3}\phi^{3j}NIMTA_{\text{quarter }j},
$$

$$
EXRETAVG=\frac{1-\phi}{1-\phi^{12}}\sum_{j=0}^{11}\phi^jEXRET_{t-1-j}.
$$

The quarterly profitability measure must not be annualized before applying the reported coefficients. Missing lags are replaced by cross-sectional means. Market-to-book, $MB$, completes the eight-variable specification.

The authors winsorize model variables at the 5th and 95th percentiles of their pooled firm-month distributions. Accounting data are put on a calendar basis and lagged two months. That is the stated availability convention; it is not equivalent to checking the actual release timestamp of every statement or using a vintage database. Moreover, pooled full-sample winsorization and other full-sample imputation constants create a preprocessing distinction from a strictly prospective implementation even when regression coefficients are estimated using only past outcomes. A modern replication should report both the original preprocessing and training-window-only thresholds rather than claiming the latter reproduces the paper exactly.

## Model, estimation objective, and probability horizon

For an at-risk firm $i$, let $Y_{it}$ indicate failure in month $t$ and $x_{i,t-1}$ contain information assigned to the preceding month-end. The next-period hazard is

$$
p_{it}=\Pr(Y_{it}=1\mid\mathcal F_{t-1},\text{firm at risk})
=\frac{1}{1+\exp[-(\alpha+\beta'x_{i,t-1})]}.
$$

The dynamic panel logit maximizes the sum of Bernoulli log-likelihood terms $Y\log p+(1-Y)\log(1-p)$ over observed at-risk firm-months. Repeated survival observations matter: using only one pre-failure snapshot and one surviving-firm snapshot changes the estimand and can distort coefficients. The paper reports asymptotic $z$-statistics and McFadden pseudo-$R^2=1-L_1/L_0$, where $L_0$ is the constant-only log likelihood. Pseudo-$R^2$ is not a fraction of binary-outcome variance explained.

The best full-sample short-horizon score in Table III is

$$
\eta=-9.08-29.67NIMTAAVG+3.36TLMTA-7.35EXRETAVG+1.48SIGMA
+0.082RSIZE-2.40CASHMTA+0.054MB-0.937PRICE.
$$

These are rounded published coefficients and should not be treated as the exact internal estimates. The dynamic hazard framework does not in itself make observations independent across firms: correlated macro shocks and omitted frailty can affect inference and aggregate calibration.

For a future horizon, the paper estimates separate coefficients using current predictors to explain failure at a future date conditional on survival to the preceding date and continued data availability. It does not model predictor transitions. Equation (4) makes this explicit. Table IV labels predictors by their additional lag, with a baseline column labeled zero; reproducing it requires preserving the authors' index convention when mapping statement dates, signal dates, and failure months.

A twelve-month-ahead conditional monthly hazard is not a cumulative twelve-month default probability. Even if a monthly hazard were constant, cumulative default under no competing exits would be $1-(1-p)^{12}$. With changing hazards and acquisition/delisting exits, further assumptions are required. The authors expressly decline to construct that cumulative model. The portfolio sort can use the horizon-specific score as a ranking without solving that separate problem.

## Failure-prediction results

Replacing the five-variable baseline with the eight-variable model increases pseudo-$R^2$ for failure prediction over 1963–2003 from 0.270 to 0.312. For bankruptcies through 1998 it rises from 0.260 to 0.299. At the sample-mean firm, a one-standard-deviation increase in leverage raises predicted failure probability by 156% relative to its initial value; analogous effects are +64% for volatility, −44% for profitability, −56% for price, −28% for past excess return, and −21% for cash. These are local comparisons at a specified starting firm, not constant percentage effects everywhere in the cross-section.

The twelve-month-lag model used as the portfolio-score reference is

$$
\eta_{12}=-9.16-20.26NIMTAAVG+1.42TLMTA-7.13EXRETAVG+1.41SIGMA
-0.045RSIZE-2.13CASHMTA+0.075MB-0.058PRICE.
$$

Again, the strategy reestimates coefficients historically rather than applying these full-sample values to all years. The share-price coefficient is insignificant at this horizon, while relative size now has the economically familiar negative sign.

Table IV's pseudo-$R^2$ declines from 0.312 at baseline to 0.188, 0.114, 0.061, and 0.044 at six-, twelve-, twenty-four-, and thirty-six-month lags. Volatility's coefficient stays near 1.3–1.5; leverage falls from 3.36 to 0.643; the market-to-book coefficient rises from 0.054 to 0.125; size becomes more negative. The persistent market characteristics consequently matter more at distant horizons, while leverage and recent returns are especially useful near failure.

The observations and event counts change with horizon. At twelve months there are 1,565,634 observations and 1,968 failures, more failures than at baseline because a usable earlier observation can survive missing data immediately before failure. This is not a cumulative-count interpretation. A common-observation subsample gives similar qualitative horizon patterns, reducing concern that changing sample composition alone explains the coefficient evolution.

## Structural benchmark and its scope

The appendix solves the Merton equity-value and equity-volatility equations for asset value $V$ and asset volatility $\sigma_V$:

$$
ME=V\Phi(d_1)-BD e^{-rT}\Phi(d_2),\qquad
\sigma_E=\Phi(d_1)\frac{V}{ME}\sigma_V,
$$

where $d_1=[\log(V/BD)+(r+\sigma_V^2/2)T]/(\sigma_V\sqrt T)$ and $d_2=d_1-\sigma_V\sqrt T$. The debt barrier is short-term debt plus half long-term debt, and $T=1$ year. Starting values are $V=ME+BD$ and $\sigma_V=\sigma_E ME/(ME+BD)$.

The resulting distance is

$$
DD=\frac{\log(V/BD)+r+0.06-\sigma_V^2/2}{\sigma_V}.
$$

The common 6% premium is an empirical drift proxy. It avoids extremely noisy firm-specific mean returns but is not derived from the Merton pricing equations. Missing debt barriers are imputed from full-sample median $BD/TL$ ratios; zero barriers use a median for a small-positive-barrier subset. Barrier leverage and volatility are winsorized at 0.5% and 99.5% before solving to improve convergence. These preprocessing choices are part of this particular benchmark. It is not Moody's proprietary EDF database or an exact replication of every other published DD implementation.

In Table V, DD alone has in-sample pseudo-$R^2$ 0.159 at baseline, 0.066 at twelve months, and 0.026 at thirty-six months. The reduced form has 0.312, 0.114, and 0.044. Adding DD raises the twelve-month value only to 0.117. DD even has a positive conditional coefficient at the shortest horizon after other predictors enter, reflecting overlap among correlated inputs rather than a literal claim that safer firms fail more.

Annual expanding-estimation predictions from 1981–2003 yield pseudo-$R^2$ 0.156 and 0.064 for DD alone at baseline and twelve months, versus 0.310 and 0.108 for the richer model. Similar in- and out-of-sample fits partly reflect the concentration of events late in the sample when training and full-sample coefficients are close. The result supports freeing functional-form restrictions and adding inputs; it does not show that structural ideas have no information.

## Aggregate calibration and omitted common risk

Figure 1 compares annual average fitted and realized failures for firms with usable predictors. The model captures broad trends and the early-1990s and early-2000s spikes, but misses persistent periods: it overpredicts around 1974–1975 and the early 1990s and underpredicts much of the 1980s. Year dummies remain statistically useful. Hence good cross-sectional discrimination does not eliminate time-varying baseline risk or correlated failure shocks.

Possible causes include financial innovation, changing bankruptcy practices, macro shocks, and direct inter-firm effects. The paper discusses these as frailty or common omitted influences without estimating a full correlated-default model. Sector and size/leverage interactions add little in the preferred specification; some macro spread interactions help explain time effects. For portfolio credit-loss aggregation, these results caution against treating fitted firm hazards as independent Bernoulli draws.

## Portfolio formation and delisting treatment

Each January from 1981 through 2003, the future-horizon model is reestimated with historically available outcomes. Stocks are sorted into probability percentile bins 0–5, 5–10, 10–20, 20–40, 40–60, 60–80, 80–90, 90–95, 95–99, and 99–100. Positions are value weighted at formation and held for a year, with weights drifting with returns. Stocks priced below \$1 at formation are excluded. The strategy deliberately concentrates bins in the tails and avoids monthly resorting, though the authors say monthly rebalancing yields similar results.

The long–short decile portfolio buys the safest 10% and shorts the most distressed 10%; the quintile version uses 20% on each side. These are percentile-based portfolios, not optimized portfolios with explicit factor neutrality. Their substantial negative HML and SMB loadings matter when interpreting alpha.

CRSP delisting returns are used when available; the sample includes 6,481 such observations. Otherwise the last complete monthly return is used, which can act as a sale before the actual delisting loss and bias distressed-stock returns upward. Delisting proceeds are reinvested proportionally in remaining portfolio constituents. Stocks that reenter after a first delisting are not restored. Failure is treated as an exit even if CRSP continues to report later stock returns. A median-delisting-return sensitivity strengthens the result slightly, according to the text.

The \$1 filter, annual holding period, and delisting adjustments reduce particular microstructure concerns but do not measure execution cost. No borrow availability, loan fee, recall, buy-in, financing, or capacity model is supplied. These omissions are especially relevant because the paper's preferred economic interpretation emphasizes limits to arbitrage.

## Returns, risk adjustment, and uncertainty

Table VI reports annualized arithmetic mean returns and regression intercepts from monthly data. “Excess return” here is return over the market, not over Treasury bills. Market coefficients in those regressions are therefore the portfolio's ordinary market beta minus one. This explains why safe portfolios have negative reported market coefficients without necessarily having negative raw betas.

| Portfolio | Market-relative mean, %/year | CAPM alpha | Three-factor alpha | Four-factor alpha | Annual portfolio SD |
|---|---:|---:|---:|---:|---:|
| Safest 5% | 3.30 | 2.70 | 5.91 | 2.51 | 11.7% |
| 90–95th distress percentile | −7.97 | −10.86 | −18.03 | −9.81 | 22.5% |
| 95–99th percentile | −6.80 | −9.54 | −16.30 | −8.40 | 25.7% |
| Most distressed 1% | −16.14 | −18.56 | −24.15 | −20.24 | 39.5% |
| Safe-minus-distressed deciles | 9.66 | 12.05 | 22.65 | 12.07 | 26.4% |
| Safe-minus-distressed quintiles | 6.30 | 8.58 | 17.27 | 8.10 | 21.4% |

For the decile spread, mean-return $t=1.76$, CAPM-alpha $t=2.21$, three-factor-alpha $t=6.04$, and four-factor-alpha $t=3.37$. The raw gross return is much less precisely estimated than the three-factor alpha. Momentum explains a substantial portion: adding UMD reduces the alpha from 22.65% to 12.07% annually, but leaves a significant residual. It is misleading either to call the entire effect ordinary momentum or to quote only the 22.65% figure as an investable neutral return.

The decile spread loads −0.565 on the market, −1.435 on HML, and −1.462 on SMB in the three-factor regression. Distressed stocks are risky under those factors, so subtracting their modeled compensation makes their residual returns worse. The strongest distress portfolio also has individual-stock volatility of 94.3%, compared with 35.2% in the safest 5%. Considerable volatility remains after diversification, and distressed individual and portfolio returns are positively skewed.

Mean fitted future-date failure probabilities range from 0.011% in the safest bin to 0.803% in the highest-distress bin. Those are the model's conditional monthly event probabilities at the selected horizon. They should not be presented as 1.1 versus 80.3 basis points of cumulative annual default probability.

Figure 4 shows uneven realized performance: raw safe-minus-distressed returns are concentrated in the late 1980s and late 1990s, with negative returns late in the sample. Factor-adjusted cumulative performance is steadier. This distinction is important for a PM who must finance and tolerate the actual portfolio path rather than a regression residual series.

## Size, value, ownership, and liquidity diagnostics

Double sorts first form size or book-to-market quintiles using NYSE breakpoints, then distress quintiles within them. The safe-minus-distressed three-factor alpha is 17.49% annually in the smallest-size group and 10.18% in the largest, both statistically significant. Raw means are 10.81% and 1.73%. The spread in log failure probability is also twice as large among small stocks: 2.60 versus 1.27. Regressing spread returns without an intercept on the log-probability difference yields fairly similar risk-adjusted return per distress unit across size groups, around 6.3–7.5 percentage points annually. Thus concentration in small stocks partly reflects stronger distress separation, not an entirely different return mechanism.

The anomaly exists among both growth and value stocks. Adjusting for factors and for distress spread reduces the differences across book-to-market groups. That weakens a simple claim that the distress result is solely an extreme-growth or small-stock artifact.

Table VIII residualizes characteristics on size, with time controls, before taking high and low terciles. The safe-minus-distressed three-factor alpha is 11.62% versus 20.68% for high versus low analyst coverage, and 11.93% versus 22.60% for high versus low institutional holdings. Low-price stocks show a stronger effect as well. These patterns are consistent with slower information diffusion and greater shorting difficulty, but do not separately identify those mechanisms.

The largest contrast is contemporaneous turnover: alpha is −6.45% in the high-turnover group and 36.52% in the low-turnover group. The authors explicitly say this cannot be used as a prospective trading filter because turnover is observed during the return month; lagged turnover does not reproduce it. Contemporaneous institutional selling also concentrates underperformance. Those are explanatory diagnostics, not extra tradable alpha signals available at formation.

## Explanations tested, and explanations left open

Removing three-day earnings-announcement windows barely changes the distress spread. Table IX replaces each stock's window return with factor-implied benchmark returns. The decile three-factor alpha is then 22.64%, versus 22.65% originally, and the four-factor alpha is 12.24%, versus 12.07%. Distressed stocks do not disproportionately disappoint during announcements; some announce positive abnormal returns. This weakens a narrow earnings-surprise correction story, but it does not disprove all mispricing because information may arrive at other times or announcement survival may itself be good news.

Fama–MacBeth regressions show several failure predictors also predict equity returns. Beginning-of-year profitability, past excess returns, volatility, cash, and market-to-book contribute in the direction of distressed underperformance. Leverage and price have the same sign in return and failure regressions, so the score is not a uniform set of negative-alpha exposures. Beginning-of-month past return becomes insignificant, consistent with short-term reversal offsetting medium-term momentum. The aggregate score's return relation is therefore broader than one known anomaly but does not establish a distinct causal “distress factor.”

The safe-minus-distressed decile return correlates 0.22 with monthly VIX changes from 1990 onward. Distressed stocks tend to lose when marketwide risk or risk aversion rises, which is hard to reconcile with their low mean returns as ordinary compensation for bad-state exposure. The long–short return also correlates 0.29 with growth in aggregate institutional equity ownership. The latter is circumstantial support for changing demand, not an exogenous identification strategy.

The remaining hypotheses include unexpected changes in debtholder bargaining power, institutional preference shifts, overvaluation, investor demand for positively skewed lottery-like payoffs, and private benefits enjoyed by controlling shareholders. The paper has no direct test of the private-benefit hypothesis. Positive skewness and trading-friction patterns are compatible with several mechanisms and cannot uniquely select one.

## Replication priorities and practical use

A faithful implementation needs the original event file and its date/exit rules, a CRSP–COMPUSTAT link valid through time, fiscal-to-calendar alignment, original nominal prices, S&P 500 capitalization, split and delisting handling, and the vintage factor data. The article supplies formulas and key historical settings but not all merge rules, data revisions, rounding precision, or clustering choices required for a fully reproducible executable pipeline.

The first validation should reproduce failure counts, predictor distributions, Table III coefficients, Table IV horizon counts, and Table V expanding-window fits before attempting portfolio returns. Then reconstruct annual formation, tail breakpoints, drifting weights, failure exits, and the distinction between market-relative returns and bill-excess factor regressions. A separate prospective version should use actual statement release dates, training-only preprocessing, and a carefully matured outcome window so a long-horizon label is never used before it is observable.

For investment research, the score is most defensible initially as a distress exposure and stock-selection diagnostic. A net-return test would require historically available borrow, transaction costs, realistic trading participation, and factor-constrained alternatives. One should compare a distress composite with its constituent signals under identical implementation assumptions rather than infer incremental alpha from a predictive failure model alone. The paper's central finding is robust enough to challenge a simple positive distress-premium story, while its strongest gross returns remain inseparable from material implementation frictions.

## Source map

Campbell, Hilscher, and Szilagyi (2008), “In Search of Distress Risk.” Event definitions and preprocessing: pp. 2903–2912, Tables I–III. Horizon model and structural comparison: pp. 2912–2916, Tables IV–V. Aggregate calibration: Figure 1, p. 2917. Portfolio construction and main results: pp. 2918–2923, Table VI and Figures 2–4. Characteristic and announcement diagnostics: Tables VII–X, pp. 2924–2931. Explanations and VIX evidence: pp. 2927–2936, Figure 5. Variable and DD construction: Appendix, pp. 2935–2937. References: pp. 2937–2939. External literature is attributed as discussed by this source and is not independently re-reviewed here.
