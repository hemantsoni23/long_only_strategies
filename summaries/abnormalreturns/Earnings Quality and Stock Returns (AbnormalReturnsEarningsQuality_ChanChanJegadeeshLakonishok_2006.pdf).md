# Earnings Quality and Stock Returns

**Konan Chan, Louis K. C. Chan, Narasimhan Jegadeesh, and Josef Lakonishok.** *Journal of Business* 79(3), 2006, pp. 1041–1082. [Source PDF](../../Finance/AbnormalReturnsEarningsQuality_ChanChanJegadeeshLakonishok_2006.pdf). PDF page 1 corresponds to journal page 1041. This note includes the operating-performance appendix on PDF pp. 38–40.

## Why this matters

An earnings increase is less encouraging when it is financed by receivables or inventory rather than supported by cash generation. This paper shows that the distinction matters for subsequent stock returns and that a single aggregate accrual number can discard useful information. In particular, increases in accounts payable reduce accounting accruals but predict *lower* subsequent returns in the U.S. sample. The accounting sign of an item is therefore not necessarily the best predictive sign for a stock-selection model.

The basic accrual anomaly predates this paper. The contribution is to investigate its economic interpretation through operating-performance paths, individual working-capital accounts, a sales-based discretionary-accrual decomposition, later special charges, within-industry comparisons, and a U.K. sample. The authors also use historical regression coefficients to construct return forecasts from individual accrual components. Their strongest three-component model produces a 9.7-percentage-point annual spread in both raw and characteristic-adjusted returns between its extreme forecast deciles.

Those are gross portfolio results from historical samples. The paper does not estimate borrow costs, spreads, price impact, turnover-constrained capacity, or current profitability. Its evidence is consistent with a mix of aggressive earnings reporting and delayed recognition of deteriorating operations; it does not identify fraud for every company with high accruals.

## Competing explanations and discriminating predictions

The authors distinguish three explanations. Under earnings manipulation, managers use accounting discretion to maintain reported profitability despite weakening fundamentals. Investors initially overvalue those reported earnings, and later corrections generate disappointing returns. Under extrapolation, firms with rapidly growing sales naturally accumulate working capital, while investors project past growth too far forward. Under delayed response to operating conditions, inventory, receivables, and payables contain bad news that prices absorb slowly even without manipulation.

Several comparisons give the hypotheses different predictions. Manipulation should be particularly visible in abnormally high accruals, followed by earnings deterioration and income-reducing special items. Extrapolation should produce return predictability in the accrual component mechanically associated with sales growth. Delayed response to deteriorating operations can make rising payables unfavorable even though payables enter total accruals with a minus sign.

The hypotheses are not mutually exclusive. Slowing sales can cause inventory accumulation, pressure managers to recognize revenue aggressively, and expose previously excessive investor expectations simultaneously. The paper's preferred interpretation emphasizes manipulation, but its own payables results resist a pure manipulation story. In addition, the claim that a business-condition explanation should affect all working-capital components uniformly is an identifying intuition, not a theorem: different accounts can have different adjustment speeds and measurement quality.

## Universe, accounting definitions, and information timing

The U.S. sample includes domestic primary common stocks on NYSE, AMEX, and Nasdaq with CRSP and current or research Compustat coverage. It excludes financial companies, SIC 6000–6999, closed-end funds, investment trusts, units, and foreign companies. A stock is removed at formation when it is both priced below \$5 and in the bottom three NYSE-based market-capitalization deciles. This is a joint low-price/small-size filter, not a blanket exclusion of every stock below \$5 or every small stock.

Portfolios form at the end of April from 1971 through 1995. Accounting observations become eligible four months after fiscal year-end, regardless of the firm's fiscal year-end month. The 1971 start reflects fewer than 400 eligible companies in earlier years. The paper does not provide a complete annual universe-count or firm-year reconciliation, so exact sample replication requires reconstructing the specified filters from the source databases.

Let $\overline A_{it}=(A_{it}+A_{i,t-1})/2$. Before scaling, accruals are

$$
ACC_{it}=\Delta CA_{it}-\Delta CL_{it}-DEP_{it}
$$

$$
=(\Delta AR_{it}+\Delta INV_{it}+\Delta OCA_{it})
-(\Delta AP_{it}+\Delta OCL_{it})-DEP_{it}.
$$

The components use historical Compustat annual item numbers. Noncash current-asset change is the change in item 4 less the change in cash, item 1. Adjusted current-liability change is the change in item 5, minus changes in short-term debt, item 34, and income taxes payable, item 71. Depreciation and amortization are item 14. Receivables, inventory, other current assets, payables, and other current liabilities are items 2, 3, 68, 70, and 72. Each accrual amount or component is divided by $\overline A$ before comparison across firms.

Earnings are operating income after depreciation, item 178, before interest, taxes, and special items. The study's cash-flow measure is constructed as operating earnings minus accruals; it should not be silently replaced by a modern statement-of-cash-flows field. The authors deliberately use balance-sheet accruals to obtain a long history extending before widespread cash-flow statements in 1988. They acknowledge that acquisitions, divestitures, and similar balance-sheet changes can contaminate this measure, but do not rebuild the study with cash-flow-statement accruals.

Table 1 shows why the distinction can be economically large. Mean scaled earnings are 0.121 and cash flow 0.133; mean accruals are −0.012 with cross-sectional standard deviation 0.102. Receivables and inventory changes have standard deviations 0.073 and 0.071, whereas depreciation averages 0.045 with standard deviation 0.028. Median receivables and inventory each account for roughly one-fifth of total assets. Modest-looking changes in working capital can therefore account for a substantial portion of operating income.

The four-month lag is a conservative uniform availability convention, not a verification of every actual release timestamp. A robustness test restricts firms to those announcing earnings by the end of April and obtains a first-year abnormal accrual spread of 9.8%, $t=6.43$. Moving formation to the end of June gives qualitatively similar results. Those checks address publication timing, but neither provides a full point-in-time accounting database with revisions removed.

## Portfolio formation and abnormal-return construction

The main sorts allocate stocks to ten equal-count accrual groups, with equal weights within each portfolio. Returns are annual buy-and-hold returns for each of the first three years after formation. If a stock delists during a holding year, its position subsequently earns the CRSP value-weighted market return through that year's end. At the next annual holding interval, remaining stocks are rebalanced to equal weights. This replacement rule must be reproduced separately from how the initial delisting payoff is encoded in CRSP; the article does not supply a detailed missing-delisting-return imputation rule.

Abnormal returns use characteristic matches, not a CAPM or Fama–French regression alpha. At each April formation, NYSE size quintiles are calculated, but the smallest quintile is split into its first and second deciles, producing six size groups. Independent book-to-market quintiles produce 30 intersections. Equal-weight buy-and-hold returns of those groups serve as controls. A stock's abnormal return is its raw return minus the return of its assigned size/book-to-market control portfolio.

In notation, for a stock assigned at formation to control group $g(i,t)$,

$$
AR_{i,t+1}=R_{i,t+1}-R^{\mathrm{control}}_{g(i,t),t+1}.
$$

The same accounting signal can be evaluated for multiple subsequent annual horizons, but these are not three independent experiments. Firms and calendar returns recur across cohorts. The article reports time-series means and $t$-statistics; it does not supply a modern two-way clustered or fully specified overlapping-cohort inference scheme for every portfolio table.

## Earnings surprises conditional on accrual quality

The first exercise independently sorts earnings change and accruals into quintiles, producing 25 equal-weight portfolios. Earnings surprise is the annual change in operating earnings divided by average assets. It is not an analyst-consensus surprise or a seasonal quarterly SUE.

Holding accrual category fixed, high-minus-low earnings-change portfolios generate an average abnormal spread of 4.2% over the following year. Holding earnings change fixed, low-minus-high accrual portfolios average 6.2%. Thus accrual quality adds at least as much separation in this design as the earnings-change signal.

Table 2 gives a particularly useful comparison. Among the highest earnings-change quintile, the low-accrual portfolio earns 17.0% raw and 2.6% abnormal, while the high-accrual portfolio earns 12.0% raw and −1.2% abnormal. Even apparently favorable earnings growth therefore comes with a negative abnormal return when accruals are high. Across all five earnings-change categories, high-accrual abnormal returns are negative. This establishes conditional predictive content; it does not isolate an exogenous effect of changing accruals while keeping business conditions fixed.

## The aggregate accrual effect is asymmetric

At formation, the lowest accrual decile averages −16.2% of assets in accruals, 7.1% in earnings, and 23.3% in constructed cash flow. The highest decile averages +18.9% in accruals, 17.6% in earnings, and −1.3% in cash flow. Its strong reported income therefore coincides with negative constructed operating cash flow.

High-accrual stocks are also growth stocks: their book-to-market ratio averages 0.58 versus 0.79 in the low decile, and sales growth over the prior three years averages 22.8% versus 7.2%. Their raw returns three and two years before formation are 37.6% and 41.9%, followed by 28.1% in the formation year's preceding return interval. The earlier outperformance makes their subsequent weakness inconsistent with a simple continuation of past price momentum.

| Horizon after formation | Low-accrual raw return | High-accrual raw return | Raw spread | Abnormal spread |
|---|---:|---:|---:|---:|
| First year | 17.8% | 9.0% | 8.8%, $t=3.79$ | 7.4%, $t=3.83$ |
| Second year | 15.7% | 9.7% | 6.0%, $t=3.76$ | 4.4%, $t=2.97$ |
| Third year | 18.9% | 13.2% | 5.7%, $t=3.08$ | 4.3%, $t=2.48$ |

The first-year abnormal legs are +2.6% for low accruals and −4.7% for high accruals. Much of the spread comes from avoiding or shorting the highest-accrual group. The second-versus-ninth-decile raw spread is only 3.8%, well below the extreme-decile result. That concentration matters for implementation: the most attractive signal is partly a short-side, extreme-observation phenomenon, where trading and accounting-data problems can be greatest.

The low-price filter also biases the average preformation return upward by excluding some past losers. The authors state that including all stocks preserves the relative strong past performance of high-accrual firms, but the pre/post average-return comparison should not be interpreted without this sample-selection qualification.

## Operating paths and later special charges

Figure 1 and Appendix Table A1 show a sudden formation-year jump in high-decile accruals: from 5.6% of assets one year earlier to 18.9%. Receivables changes rise from 7.1% to 13.0% and inventory changes from 7.3% to 13.4%. Earnings simultaneously rise from 16.0% to 17.6%, while cash flow falls from 10.5% to −1.3%.

In the next year, high-decile earnings decline to 13.2% of assets and sales turnover falls from 1.844 to 1.722. Three years after formation, earnings are 8.6%, turnover 1.619, and earnings-to-sales 6.3%, compared with 10.5% at formation. The ordering is important: the accrual jump precedes much of the visible earnings deterioration. It fits the possibility that managers temporarily delay recognizing weakening operations.

The low-accrual firms have a different pattern. Earnings decline into formation, reaching 7.1% of assets, then improve to 8.9% the next year. Their formation year is not obviously a prosperous year in which managers could comfortably store excess profits. This weakens a symmetric story in which positive and negative accruals are simply opposite discretionary timing choices.

Special items supply additional evidence. In Table 7's highest accrual quintile, special items are −0.06% of assets at formation, then −0.49%, −0.80%, and −0.97% over the following three years. In the lowest quintile the corresponding values are −0.71%, −0.41%, −0.58%, and −0.63%. Later inventory or receivable write-downs can unwind earlier aggressive reporting through charges investors may regard as nonrecurring.

These charges do not uniquely identify manipulation. A genuine operating slowdown can also induce restructuring and write-downs. Moreover, the surrounding prose reports pre/post averages that do not match the displayed Table 7 entries: for the highest quintile it gives −0.56% postformation, whereas averaging the three printed subsequent-year values gives approximately −0.75%. The note retains the directly tabulated yearly observations rather than silently repairing the prose.

There is another inconsistency in the operating appendix. Table 8 gives high-decile accruals two years after formation as +0.56% of assets; Table A1's corresponding cell is −0.006, or about −0.6%, although its earnings and cash-flow entries imply a positive difference near +0.6%. This suggests a sign or transcription error, but the article does not resolve it. The broad declining path is clear; the disputed cell should not be used as an exact replication target without clarification.

## Individual components contain different information

The account-level sorts in Table 4 are low-minus-high comparisons for the component itself, before applying the accounting sign it has in total accruals.

| Component | First-year raw spread | First-year abnormal spread |
|---|---:|---:|
| Receivables change | 5.4%, $t=2.66$ | 3.1%, $t=2.23$ |
| Inventory change | 9.5%, $t=4.63$ | 7.2%, $t=4.34$ |
| Other current-asset change | 5.4%, $t=4.61$ | 4.5%, $t=4.29$ |
| Payables change | 7.4%, $t=5.86$ | 5.7%, $t=5.79$ |
| Other current-liability change | −0.1%, $t=-0.07$ | −1.7%, $t=-1.28$ |

Inventory produces a spread comparable to the complete accrual measure. Receivables are predictive but less powerful despite having similar cross-sectional dispersion. Inventory can reflect either unsold output or accounting discretion over overhead capitalization and write-downs, so its dominance is not itself a clean identification test.

Payables provide the sharper sign comparison. High payables changes produce a −3.1% first-year abnormal return, versus +2.6% for the low-payables group. Because increasing payables reduces total accruals, a rigid interpretation that lower accruals always mean deferred earnings and higher future returns gets the sign wrong. Slower payments to suppliers can instead signal cash-flow pressure. This is why the authors later let regression coefficients determine predictive weights rather than impose all weights from the accrual identity.

## The sales-based discretionary decomposition

For a working-capital account $I_{it}$, define its expected level conditional on current sales as

$$
\widehat I_{it}
=\left(\frac{\sum_{k=1}^{5}I_{i,t-k}}
{\sum_{k=1}^{5}Sales_{i,t-k}}\right)Sales_{it}.
$$

The nondiscretionary and discretionary changes are then

$$
NDI_{it}=\widehat I_{it}-I_{i,t-1},
\qquad
DI_{it}=I_{it}-\widehat I_{it},
$$

so $NDI+DI=\Delta I$. These amounts are scaled by average total assets for sorting. The historical ratio smooths five years of account-to-sales relationships; it is a ratio of sums, not an average of annual ratios. Current sales are allowed because they come from the same lagged financial statements used at formation. They are not future sales from the holding period.

The term discretionary is a model residual, not a direct observation of managerial intent. Product mix, credit terms, acquisitions, or structural changes in operating efficiency can also make an account depart from its historical sales ratio. The paper recognizes decomposition error. It does not specify every rule for missing five-year histories or unusual denominator values. It also does not give an equally explicit formula for allocating depreciation between discretionary and nondiscretionary portions when using the broader aggregate predictor set. The three-working-capital-component model is therefore more directly reconstructable than every detail of the six-component discretionary model.

Table 5's discretionary-accrual extreme deciles earn first-year spreads of 7.8% raw, $t=5.50$, and 7.4% abnormal, $t=5.51$. More revealingly, the second-versus-ninth-decile abnormal spread is 5.6%, $t=5.79$, versus 2.5% for total accruals. Removing the sales-related component improves separation away from the most extreme observations.

Nondiscretionary accruals have essentially no first-year predictive spread: 0.4% raw, $t=0.17$, and −0.6% abnormal, $t=-0.26$. This weighs against the paper's particular sales-extrapolation hypothesis. It does not establish that all forms of investor extrapolation are absent, because current sales and stable historical working-capital ratios do not span every possible growth expectation.

Table 6 sharpens the result. Discretionary inventory changes generate a 9.1% first-year abnormal spread, $t=7.02$, versus −1.5%, $t=-0.71$, for nondiscretionary inventory changes. Discretionary receivables changes produce 3.5%, $t=2.99$, and discretionary payables changes 4.1%, $t=4.95$. The latter again has the unfavorable high-payables sign, preserving the evidence for operating-condition information beyond a pure earnings-manipulation interpretation.

## Cross-sectional regressions and prospective forecasts

The regression framework relates subsequent abnormal returns to scaled accounting variables:

$$
AR_{i,t+1}=a_t+b_t^{\mathsf T}X_{it}+u_{i,t+1}.
$$

Table 9 averages coefficients across cross sections and reports their time-series $t$-statistics. Total accruals have coefficient −0.2627, $t=-4.14$. In the three-component raw regression, receivables, inventory, and payables coefficients are −0.1490, −0.2661, and −0.0120, with $t$-statistics −1.69, −2.83, and −0.08. Thus inventory retains the strongest incremental contribution, while payables' univariate signal is largely absorbed jointly.

For discretionary components, the joint coefficients are −0.1784 for receivables, −0.3259 for inventory, and +0.0229 for payables, with $t=-2.60,-4.55,0.18$. The last estimate is insignificant; the paper does not demonstrate a reliably negative conditional payables coefficient after the other discretionary components are included. A 0.01 increase in scaled discretionary inventory corresponds to approximately −0.00326 fitted annual abnormal return under the reported coefficient units, not a 32.6% return effect.

The frequency description is internally inconsistent. The section calls the regressions monthly, while the table describes estimation at each April formation and an annual return dependent variable, then again refers to monthly coefficient averages. The exact cross-sectional frequency, overlapping-return treatment, and standard-error calculation need the authors' implementation to reconcile. A reimplementation should state its chosen interpretation rather than present one as unambiguously specified.

The forecasting exercise uses four predictor sets: six raw accrual components; their discretionary counterparts; raw receivables, inventory, and payables changes; and the discretionary versions of those three accounts. Coefficients are averages from prior cross-sectional regressions. Although called rolling averages, the description says all prior years, implying an expanding history. The first five years initialize the estimates and trading performance begins in year six, avoiding use of future coefficients in the reported trading sample.

Table 10 reports high-minus-low predicted-return spreads:

| Model | Raw spread | Abnormal spread |
|---|---:|---:|
| Six raw components | 8.3% | 7.0% |
| Six discretionary components | 8.9% | 8.8% |
| Three raw working-capital changes | 8.9% | 6.6% |
| Three discretionary working-capital changes | 9.7% | 9.7% |

For the fourth model, the low-prediction portfolio earns −5.9% abnormal and the high-prediction portfolio +3.8%. These comparisons are not strictly matched to the main 1971–1995 accrual sort because the predictive strategy excludes its initial five-year estimation period. Table 10 supplies no spread $t$-statistics, net-cost results, model-selection correction, or separate untouched validation sample. The historical coefficient timing is useful, but it is not a complete modern out-of-sample validation protocol.

## Industry and U.K. evidence

Within-industry sorts use Fama–French industry definitions and quartiles rather than deciles. Industries must average at least 20 eligible firms and cannot have more than five years below that threshold; otherwise observations enter the other category. Across 32 industries, first-year abnormal low-minus-high accrual spreads average 5.0%, with reported cross-industry $t=6.86$, and are positive in 29 cases. Second- and third-year mean spreads are 2.8% and 2.1%, with $t=4.13$ and 2.75.

Examples include construction at 16.2%, toys at 10.9%, and computers at 9.4%, while drugs, mining, and energy have negative first-year spreads. The rank correlation between industry inventory-plus-receivables intensity and the spread is 0.27. This supports economic heterogeneity, but industries share common shocks and the cross-industry statistic is not a substitute for a calendar-time portfolio inference test.

The U.K. sample comprises domestic primary nonfinancial stocks in Xpressfeed, with April formation from 1991 through 2000 and the same four-month accounting lag. First-year total-accrual spreads are 13.5% raw and 10.8% abnormal. Inventory-change spreads are 8.1% raw and 8.0% abnormal. Receivables and payables changes, however, contribute little abnormal spread, 0.8% and 0.7%. The strongest cross-country replication is therefore the aggregate accrual and inventory evidence, not every U.S. component-level finding.

The U.K. table provides no $t$-statistics, and one raw-return cell literally prints “20.095,” an apparent typesetting error. No numerical inference should rely on interpreting that cell without correction from the underlying data. The paper describes the U.K. test as free from data snooping; more cautiously, it is an additional market test that reduces reliance on the original U.S. sample, while retaining common researcher choices and economic linkages.

The international comparison also changes the informational content of the component model. In the U.S., payables provide a strong univariate warning that total accruals partly suppress because of their accounting sign. In the U.K., that same account adds little separation. A universal fixed coefficient on payables is therefore not supported by these two samples. The result motivates estimating component contributions in the relevant accounting and market setting, while recognizing that the U.K. sample has only ten annual formation dates and the table does not quantify its uncertainty. The paper's evidence is strongest for a recurring inventory-related pattern, with the broader component mix remaining context dependent.

## Assessment and source map

The evidence supports treating earnings changes and cash conversion jointly, separating working-capital accounts, and avoiding a mechanical translation from accounting signs to return-forecast signs. It also supports an asymmetric interpretation: the highest accrual firms have particularly poor subsequent outcomes. Its inference about deliberate manipulation is suggestive rather than causal, because the same accounts respond endogenously to operating slowdowns and measurement choices.

The exact replication gaps are the regression-frequency inconsistency, some discretionary-depreciation details, missing-history conventions, a few conflicting printed cells, and incompletely specified delisting and inference treatments. The principal portfolio and decomposition results remain clear. They are historical gross-return evidence, not a net implementable claim after turnover, financing, short availability, and market impact.

Definitions and sample are on PDF pp. 8–10, Eq. (1) and Table 1. Earnings-change interactions and aggregate accrual portfolios are on pp. 11–16, Tables 2–3. Operating paths are Figure 1, p. 17, and Appendix Table A1, pp. 38–40. Component sorts and decomposition are on pp. 19–26, Tables 4–6 and Eqs. (2)–(4). Special items and accrual reversals are Tables 7–8, pp. 27–29. Regressions and prediction models are Tables 9–10, pp. 30–32. Industry and U.K. tests are Tables 11–12, pp. 33–35. Conclusions and references complete pp. 36–42.
