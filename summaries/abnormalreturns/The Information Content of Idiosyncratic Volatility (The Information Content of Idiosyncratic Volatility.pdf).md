# The Information Content of Idiosyncratic Volatility

George J. Jiang, Danielle Xu, and Tong Yao. *Journal of Financial and Quantitative Analysis* 44(1), February 2009, pp. 1–28, DOI 10.1017/S0022109009090073. [Source PDF](../../Finance/The%20Information%20Content%20of%20Idiosyncratic%20Volatility.pdf). All 28 pages, including footnotes and references, were read. The signal equation, main return and earnings tables, Figure 1, annual timing discussion, disclosure regressions, and investor-sophistication table were checked visually. There is no separate appendix in the supplied source.

## Why this matters

Jiang, Xu, and Yao connect three observations: high past idiosyncratic volatility predicts weak future earnings, weak future earnings accompany low stock returns, and controlling for subsequent earnings surprises substantially attenuates the negative volatility–return relation. This adds information about cash flows to an anomaly otherwise often discussed only through risk, leverage, or investor preferences.

The paper's strongest directly documented result is a predictive association between a backward-looking return statistic and later accounting outcomes. Its proposed explanation is more tentative. Managers may disclose favorable information promptly while withholding bad news; reduced disclosure can increase disagreement and volatility; and less sophisticated investors may fail to infer the adverse earnings information already embedded in high volatility. A limited analyst-rated disclosure sample and investor-ownership sorts are consistent with that story, but do not identify it causally.

For a quantitative researcher, the paper suggests both a useful empirical decomposition and a warning about timing. Subsequent realized earnings are explanatory outcomes, not portfolio-formation inputs. If the volatility coefficient disappears after adding future surprises, that does not mean an investor could have neutralized the signal using those surprises in real time. Nor does attenuation by a correlated future outcome prove a unique causal mediation channel.

The baseline quarterly low-minus-high volatility decile return is 3.28%, with a Carhart four-factor alpha spread of 3.46%. The low/high earnings contrast is economically substantial as well: next-quarter median return on equity is 3.59% versus 1.40%, and the following four-quarter aggregate is 14.38% versus 8.51%. These are historical cross-sectional patterns, not a forecast of current expected strategy performance.

## Sample construction and the signal clock

Stock returns, prices, shares outstanding, and volume come from CRSP. Accounting data come from Compustat, and analyst forecasts and corresponding reported earnings from I/B/E/S. The principal sample runs from January 1974 through December 2002. Forecast-error tests begin in 1980 because of I/B/E/S coverage.

At each calendar-quarter end, a stock must have at least 44 daily return observations during the quarter, a price of at least \$5, and a nonnegative book value of equity. Its fiscal quarters must end in March, June, September, or December so that fiscal earnings can be aligned with calendar-quarter returns. The first three requirements produce 434,326 firm-quarter observations; calendar matching reduces the count to 358,199, or 82.5% of that total. The authors report that removing the fiscal matching requirement does not overturn their findings, whereas the \$5 filter is important for the return relation's robustness.

That price-filter sensitivity is part of the result's scope. It is not legitimate to describe the anomaly as invariant to the investable universe when the source explicitly identifies a consequential exclusion. Conversely, the filter can reduce microstructure contamination; its importance need not imply that the remaining result is spurious. A reproduction should report filtered and unfiltered variants separately.

For each stock and formation quarter $Q0$, estimate the daily regression in source equation (1):

$$
r_{i,d}=\alpha_i+\beta_{i,H}HML_d+\beta_{i,S}SMB_d
+\sum_{\ell=-3}^{3}\gamma_{i,\ell}r_{m,d-\ell}+\varepsilon_{i,d}.
$$

Here $r_m$ is the CRSP value-weighted market return, and $HML$ and $SMB$ are the daily Fama–French factors. The source writes raw daily stock and market returns rather than explicitly subtracting cash in this signal regression. Idiosyncratic volatility, $IVOL_{i,Q0}$, is the standard deviation of the residuals. Its reported values are daily volatility in percentage points, not annualized volatility.

Three market leads and lags address nonsynchronous trading. The authors state that only information available before quarter-end enters estimation. Therefore the lead structure cannot be implemented by pulling post-formation market returns for the final daily observations. Trimming the last lead-dependent rows is one possible implementation, but the exact endpoint convention and the relation of the 44-observation filter to usable regression rows are not fully disclosed. Robustness checks use no leads/lags, or one and three leads/lags for all factors, with similar author-reported conclusions.

The stock characteristics include log market capitalization, log book-to-market, and momentum. The main text uses the latest reported fiscal-year book value with a four-month reporting lag. Momentum is the arithmetic average of twelve monthly returns ending one month before the current quarter's final month. For a quarter ending in March, this means the twelve months through February. The count remains twelve; it is not an eleven-month signal or a compounded cumulative return. Some table captions abbreviate these definitions; the more explicit text should guide the formation clock.

Leverage is internally inconsistent in the supplied article. Page 5 defines book debt divided by book assets, while Table 1 defines total assets divided by book equity and reports means around 3.7–4.4, consistent with the latter scale. These are materially different variables. The note preserves the ambiguity rather than choosing a definition and presenting it as confirmed source methodology. Both can be implemented as sensitivity cases, but exact replication requires clarification or original code.

## Baseline portfolios and inference

At each quarter-end, stocks are ranked on $IVOL$ into equal-weighted deciles and held for the following quarter, $Q1$. Missing delisting returns are replaced with −30% when the delisting is performance-related and zero otherwise, following the stated Shumway convention. This treatment is especially relevant to the high-volatility group, where distressed stocks may be concentrated. The paper reports that value-weighted versions have similar patterns, but does not tabulate them.

Quarterly portfolio excess returns are regressed on market, size, value, and momentum factors:

$$
R_{p,q}-R_{f,q}=\alpha_p+
 b_M(R_{m,q}-R_{f,q})+b_SSMB_q+b_HHML_q+b_UUMD_q+e_{p,q}.
$$

The cash reference is the three-month Treasury-bill yield, and monthly factors are aggregated to quarters. The exact compounding convention for zero-cost factor returns should be made explicit in a reproduction; a generic instruction to aggregate does not uniquely determine every implementation.

Table 2 uses Newey–West inference with one quarterly lag for returns and alphas and four quarterly lags for characteristics. Quarterly frequency is essential: 3.46% is a quarterly alpha, not a monthly number. Neither multiplying by four nor compounding a constant quarterly alpha creates an independently estimated annual strategy return.

| Quantity | Lowest IVOL decile | Highest IVOL decile | Low minus high |
|---|---:|---:|---:|
| Daily residual volatility | 0.83% | 4.88% | −4.05 percentage points |
| Next-quarter return | 3.83% | 0.55% | 3.28%, $t=2.56$ |
| Quarterly four-factor alpha | 0.25% | −3.21% | 3.46%, $t=4.23$ |
| Log market capitalization | 5.68 | 3.80 | 1.88 |
| Prior-return characteristic | 1.35 | 2.69 | −1.34 |

The return pattern is not monotonic from the very lowest volatility decile onward. Returns rise from 3.83% in decile 1 to 4.49% in decile 6 and then fall, reaching 2.73% and 0.55% in deciles 9 and 10. Alphas are insignificant in deciles 1–8, while deciles 9 and 10 have −1.28% and −3.21%, with $t=-2.95$ and −5.12. The anomaly is largely concentrated in the most volatile stocks' underperformance.

A conventional normal approximation using the displayed spread and $t$ gives a quarterly alpha standard error of about 0.82 percentage points and an approximate 95% interval of 1.86%–5.06%. This interval is derived here from rounded table entries and the reported HAC statistic, not separately reported by the authors. The raw spread is less precisely estimated. The text calls its $t=2.56$ significant at 1%; that is borderline even under a normal two-sided threshold and should not be treated as an exact reported $p<0.01$ result.

## Earnings definitions and horizons

The paper uses three earnings measures with different economic meanings:

$$
ROE_q=\frac{NI_q}{BE_{q-1}},
$$

$$
UE_q=EPS_q-EPS_{q-4},\qquad
SUE_q=\frac{UE_q}{s(UE_{q-1},\ldots)}.
$$

The standard deviation for $SUE$ uses the preceding eight quarters of unexpected earnings, with a minimum of four. It encodes a seasonal-random-walk earnings benchmark. It is not an analyst forecast surprise and not necessarily a shock relative to the full public information set.

The analyst-based measure is

$$
FER_{q\mid Q0}=\frac{EPS_q-\widehat{EPS}_{q\mid Q0}}{BPS_{\mathrm{previous\ year}}},
$$

where the consensus forecast is observed in the final month of the formation quarter. I/B/E/S supplies both actual and forecast EPS, and Compustat supplies book equity per share. The authors adjust shares to align per-share units across providers. Stock splits and differing earnings definitions make that alignment a necessary replication step, not a cosmetic data merge.

The analysis considers $Q0$ earnings because they are usually not yet announced at the close of $Q0$, as well as $Q1$ earnings and a four-quarter aggregate. $ROE4$ and $SUE4$ aggregate quarters $Q1$ through $Q4$. $FER4$ instead aggregates $Q0$ through $Q3$, because the relevant I/B/E/S forecasts cover those four quarters. Those horizons must not be presented as identical. The four-quarter earnings information can affect returns in $Q1$ through changing expectations even before all those earnings are realized.

For each volatility decile, Table 3 reports the time-series average of the *cross-sectional median* earnings measure. It is not an average firm-level ROE or the ROE of an aggregated balance sheet. This choice reduces the influence of accounting-ratio outliers but changes the estimand.

| Earnings outcome | Lowest IVOL decile | Highest IVOL decile | Difference and HAC $t$ |
|---|---:|---:|---:|
| $ROE_{Q0}$ | 3.61% | 1.03% | 2.58 points, 5.90 |
| $ROE_{Q1}$ | 3.59% | 1.40% | 2.19 points, 5.39 |
| $ROE4$ | 14.38% | 8.51% | 5.87 points, 4.76 |
| $SUE_{Q0}$ | 0.23 | −0.23 | 0.46, 13.4 |
| $SUE_{Q1}$ | 0.19 | −0.13 | 0.33 reported, 9.88 |
| $SUE4$ | 0.46 | −0.03 | 0.49, 3.34 |
| $FER_{Q0}$ | −0.05 | −1.32 | 1.27, 9.02 |
| $FER_{Q1}$ | −0.06 | −0.88 | 0.82, 7.20 |
| $FER4$ | −0.36 | −2.76 | 2.40, 5.73 |

The small $SUE_{Q1}$ subtraction discrepancy can arise from rounding the two reported endpoints. Analyst forecast errors are mostly negative, consistent with optimistic forecasts. The FER numbers are book-equity-scaled earnings errors in the table's percent-style reporting, not percentage errors relative to EPS; a −0.88 value must not be described as an earnings miss of 0.88% relative to the forecast.

Figure 1 follows fixed portfolios formed at $Q0$ across four quarters before and after formation. The low-minus-high volatility difference remains negative, ROE remains higher for low-volatility stocks, and the positive SUE difference decays toward zero by $Q4$. It does not reverse sign in the displayed horizon. Persistence does not mean zero turnover: among high-IVOL stocks, 63% remain in the same quintile at $Q1$ and 42% at $Q4$; corresponding low-IVOL proportions are 66% and 55%.

The discussion of “remaining” versus “migrating” high-IVOL stocks contains a numerical interpretation problem. It reports $ROE4$ of 11.65 and 7.66 for the two groups, respectively, but then says the relation is mainly driven by the remaining group. Without the underlying sampling uncertainty, group composition, and calculations, that conclusion cannot be reconstructed from the means alone. Both next-quarter ROE figures, 1.58 and 1.83, are below the middle portfolio's level.

## Earnings regressions and future-outcome controls

Quarterly cross-sectional earnings regressions include twelve industry indicators, IVOL, log size, log book-to-market, momentum, and lagged profitability:

$$
ROE_{i,h}=\sum_{k=1}^{12}a_kIND_{ik}
+b_1IVOL_i+b_2\log SIZE_i+b_3\log(B/M)_i
+b_4PrRet_i+b_5LAGROE_{i,h}+u_i.
$$

The lagged ROE is the corresponding outcome four quarters earlier. For analyst-based earnings, the last regressor becomes the appropriately scaled consensus forecast observed at formation. This tests whether IVOL contains information beyond either past seasonal earnings or analysts' forecasts.

Table 3B reports IVOL coefficients of −0.79, −0.67, and −1.74 for $ROE_{Q0}$, $ROE_{Q1}$, and $ROE4$, with $t=-12.9,-11.5,-10.1$. For the I/B/E/S outcome versions they are −0.67, −0.62, and −1.63, with $t=-12.8,-13.3,-7.37$. These are in the source's volatility and ROE scaling. The precision supports a strong conditional association; it does not imply that volatility mechanically causes accounting losses.

The return regression then adds one realized earnings-surprise measure to a baseline containing IVOL, size, book-to-market, momentum, leverage, and a Pastor–Stambaugh liquidity measure estimated from daily formation-quarter data. Source equation (5) is an explanatory regression of $Q1$ return. Its results are:

| Added earnings outcome | IVOL coefficient | HAC $t$ |
|---|---:|---:|
| None | −0.91 | −4.11 |
| $SUE_{Q0}$ | −0.67 | −3.01 |
| $SUE_{Q1}$ | −0.16 | −0.69 |
| $SUE4$ | 0.21 | 0.85 |
| $FER_{Q0}$ | −0.15 | −0.42 |
| $FER_{Q1}$ | 0.22 | 0.54 |
| $FER4$ | 0.90 | 1.93 |

Later earnings outcomes subsume much of the negative coefficient. However, the analyst-error specifications use a shorter and selected sample, so comparing their coefficients directly with the full-sample baseline can mix outcome-control and sample effects. The paper's broad claim that size, value, and momentum significance is unaffected also needs qualification: Table 4 shows book-to-market becoming insignificant in the FER specifications and momentum losing significance in some of them.

A separate exercise fixes the sample to firms with valid $SUE_{Q1}$. The low-minus-high IVOL quintile alpha spread is 2.57% per quarter, $t=3.74$. Sorting on future $SUE_{Q1}$ within each IVOL group and averaging across volatility groups gives an 8.03% contemporaneous alpha spread, $t=23.20$. The ratio $2.57/8.03\approx0.32$ illustrates that IVOL captures only part of the earnings-related return dispersion. It is not a variance-explained statistic or an estimate of a causal mediation percentage. The future-SUE portfolios are explicitly untradable at formation.

The source also reports untabulated checks with a high-IVOL interaction, EGARCH forecasts, and characteristic subsamples. Adding future earnings makes the high-IVOL interaction insignificant; the expected-volatility relation estimated with EGARCH remains distinct; and most characteristic subsamples lose a negative IVOL coefficient after future-earnings controls. These findings are author-reported, with no complete EGARCH specification or coefficient tables in the supplied file.

## Alternative explanations and the annual timing ambiguity

The authors test whether IVOL is a proxy for growth extrapolation, investment, accruals, or underreaction to earnings news. The annual design forms information from July of year $t-1$ through June of year $t$, then examines subsequent outcomes. Sales growth uses the fiscal year ending in calendar year $t-1$; long-term analyst growth is observed in June $t$. Capital expenditure is scaled by beginning-of-year assets, and R&D expenditure by June market capitalization. Long-term-growth tests cover 1982–2002, analyst-revision tests 1980–2002, and most accounting tests 1974–2002.

A consequential wording issue appears on p. 17: after defining formation and holding periods, the article says IVOL is averaged over the four quarters in the *holding* period. Taken literally, that uses future information. The surrounding predictive design suggests that the intended input may be the formation-period average, but the supplied PDF does not resolve this. A deployable reproduction should use only completed formation quarters and label that choice as an interpretation; a literal-source sensitivity run should be separately marked as forward-looking. The ambiguity applies to these annual extensions, not to the clearly lagged quarterly baseline.

Accruals follow the balance-sheet expression

$$
ACC=\frac{(\Delta CA-\Delta CASH)
-(\Delta CL-\Delta STD-\Delta TP)-DEP}{ATA},
$$

with current assets, cash, current liabilities, short-term debt, taxes payable, depreciation, and average total assets defined as in source equation (6). Analyst revision is the change in consensus annual EPS forecast from the previous quarter divided by quarter-end price, averaged over the four formation quarters. $LAGSUE$ is the corresponding average past standardized surprise.

Table 6 shows high-IVOL stocks with higher forecast growth and R&D intensity, less favorable revisions and past surprises, and lower disclosure ratings. The shapes vary; many relations are not monotonic. For example, sales growth rises through the middle/high deciles and then falls, while capital expenditure initially falls before rising. Describing all these variables as simple monotonic substitutes for IVOL would lose information.

In annual earnings regressions, IVOL remains significantly negative after the growth, investment, accrual, and past-news controls. Coefficients across the first ten specifications range from −1.44 to −1.90, with robust $t$-statistics from approximately −4.19 to −7.53. Return-regression coefficients remain negative as well, from −1.37 to −2.06, with $t$-statistics between about −2.09 and −3.12. R&D has a positive return coefficient, accruals a negative one, and revisions/past surprises positive coefficients. These tests reject simple subsumption by the measured characteristics; they do not exclude more general versions of the proposed mechanisms.

## Disclosure: suggestive evidence with limited attenuation

AIMR disclosure ratings cover 1986–1996 and 8,735 firm-year observations, concentrated in large and medium firms with substantial analyst following. Analysts on industry committees score annual reporting, quarterly reporting, and investor relations on adequacy, timeliness, and clarity. Scores are combined into a total rating. This measures perceived reporting quality, not directly the amount of adverse private information withheld by managers.

The lowest-IVOL decile has a mean disclosure score of 72.65 and the highest 64.76. Table 6 prints their difference as 6.89 with $t=6.48$, but the displayed endpoints subtract to 7.89. The subtraction here is a derived arithmetic check; the original data are needed to determine which reported cell is wrong. Both versions imply poorer disclosure ratings among more volatile firms.

The introduction says disclosure predicts earnings and returns negatively, but the detailed discussion and Tables 7–8 show positive coefficients. For future four-quarter ROE, DISC has coefficient 1.84 with $t=2.16$, and IVOL is −1.07 with $t=-1.82$. For next-quarter returns, DISC has coefficient 9.05 with $t=1.84$, and IVOL is −1.20 with $t=-1.62$. The printed disclosure-variable scaling is insufficiently explicit to interpret these as effects of a one-point increase on the raw 0–100 rating scale. It is safer to report the coefficients as printed and their direction than to calculate a return change from an assumed scale.

The same-sample footnotes are more informative than comparing the disclosure regression with a different full-sample specification. For earnings, excluding DISC from the valid-DISC sample gives an IVOL coefficient of −1.46, $t=-2.01$; including it gives −1.07, $t=-1.82$. The coefficient magnitude falls by about 27%, derived from the displayed values. For returns, the same-sample coefficient changes from −1.37, $t=-1.89$, to −1.20, $t=-1.62$: only about a 12% reduction. The baseline on that restricted sample was already short of 5% significance.

Thus loss of significance does not mean disclosure has economically explained the entire anomaly. The remaining point estimate is large relative to the same-sample baseline, and the disclosure coefficient itself is only marginally significant for returns. Selection into analyst ratings, measurement error, correlated business characteristics, and limited sample length are live alternative interpretations. The authors acknowledge the narrow and indirect nature of the disclosure evidence; that caution is more defensible than a causal claim that withholding bad news has been established.

## Investor sophistication and the short-sale proxy

The final tests ask whether the earnings relation remains across investor clienteles while the return anomaly weakens where investors are presumed more sophisticated. Each quarter, stocks are first sorted into quintiles of an ownership or analyst-coverage measure, then into equal-weighted IVOL quintiles within those groups. Table 9 reports next-quarter four-factor alphas and SUE. Alpha inference uses one quarterly HAC lag; SUE inference uses four.

For low institutional ownership, the low-minus-high IVOL alpha spread is 2.97% per quarter, $t=2.67$; for the next ownership group it is 2.96%, $t=2.77$. In the highest-ownership group it is only 0.32%, $t=0.36$. Yet the earnings-surprise differences remain significant across all five groups, including 0.26 in the lowest and 0.25 in the highest. This pattern is consistent with differences in how earnings information is priced rather than differences in whether IVOL contains earnings information at all.

Institutional ownership also proxies for short-sale supply. To address that confound, the authors use a linear index adapted from D'Avolio:

$$
y=-0.46SIZE+1.59TURN-0.09CF+0.41GLAM+0.86IPO.
$$

They regress institutional ownership on this index each quarter and use the residual as a sophistication proxy. The source refers to the original study for detailed variable scales and dummy definitions, so equation (8) alone is not enough to implement the index exactly. The paper uses the index directly rather than its logistic transformation and omits some variables from the original model. A residual orthogonal to this particular linear index is not demonstrably orthogonal to actual stock-loan scarcity or every nonlinear borrowing constraint.

The residual-ownership alpha spread is 2.23%, $t=2.43$, in the lowest group and 0.76%, $t=0.83$, in the highest. Active mutual-fund ownership gives 4.09%, $t=3.76$, versus 0.11%, $t=0.13$. Analyst coverage gives 2.34%, $t=2.60$, in the lowest group and −1.13%, $t=-1.15$, in the highest. The earnings differences stay positive and significant. The active-fund data come from Thomson CDA/Spectrum, and the included objectives are aggressive growth, growth, growth and income, and balanced; passive index funds are excluded. Institutional ownership uses Thomson 13F data, and analyst coverage I/B/E/S.

These interactions are descriptive. Ownership and analyst coverage are endogenous to size, information production, expected returns, and trading opportunities. The claim that active funds generally do not lend shares is the source's motivation for a proxy, not a universal fact established by this dataset. Most importantly, a significant spread in one group and an insignificant spread in another does not itself constitute a formal test that the two spreads differ; Table 9 does not report that difference test.

## Replication limits and investment interpretation

The quarterly signal and outcome definitions are sufficiently explicit to reconstruct the main design, subject to the disclosed endpoint, leverage, and accounting-alignment ambiguities. The annual extensions require resolving the IVOL timing language. The disclosure regressions additionally need raw score scaling and historical rating availability. The short-sale index needs external variable definitions, and the liquidity control is referenced rather than fully specified in the article. No original code, full security mapping, or table-specific missing-data protocol is supplied.

A new implementation should preserve actual historical availability for accounting data, forecasts, 13F holdings, and analyst ratings. Quarter-end holdings are not automatically public at quarter-end; the paper's formation descriptions do not establish a filing-delay treatment for every ownership test. Likewise, ex post revised accounting fields and split-adjusted forecast histories need care. These are missing implementation inputs, not findings that the authors definitely used unavailable information.

There is no transaction-cost model, borrow-cost series, turnover-adjusted performance, capacity analysis, or trained prediction model with a held-out test period. The strategy is a quarterly historical sort. Its attractive gross spread largely reflects avoiding or shorting the most volatile stocks; shorting those firms can be difficult precisely when their information environment is poor. A long-only implementation and a levered low-minus-high trade therefore need separate evaluations.

The paper establishes that IVOL contains information about future earnings beyond several standard characteristics and that future earnings outcomes absorb much of its return association. It provides narrower, suggestive evidence about why this information is not fully priced. That distinction makes the research useful: volatility may be an indirect fundamental signal, but future-outcome controls and marginal disclosure regressions should not be promoted into a causal explanation or a fully specified trading algorithm.

## Source map and bibliography

Jiang, George J., Danielle Xu, and Tong Yao (2009), “The Information Content of Idiosyncratic Volatility,” *JFQA* 44(1), 1–28. Sample and signal: pp. 4–7, equation (1), Tables 1–2. Earnings definitions and persistence: pp. 8–13, Table 3, Figure 1. Future-outcome controls: pp. 13–16, equation (5), Tables 4–5. Alternative explanations and annual timing: pp. 16–24, equation (6), Tables 6–8, especially footnotes 10 and 12 for the same-sample disclosure comparisons. Investor sophistication: pp. 24–26, equation (8), Table 9. Conclusions and references: pp. 26–28. Arithmetic corrections and inferential qualifications in this note are distinguished from the source's reported estimates.
