# Identification and Valuation Implications of Financial Market Spirals

**Pankaj K. Jain, Ajay K. Mishra, and Thomas H. McInish (2013).** Chapter 29 in *Rethinking Valuation and Pricing Models*, pp. 471–483. DOI: 10.1016/B978-0-12-415875-7.00029-4. Source: [SystemicRisk_JainMishraMcinish_2013.pdf](../../Finance/SystemicRisk_JainMishraMcinish_2013.pdf). References below use the printed chapter pages.

## Why this matters

Funding pressure, forced sales, worsening liquidity, and declining collateral values can reinforce one another. Such mechanisms are well developed in the theoretical literature, but applying them to ordinary equity data requires observable proxies. This chapter proposes signed, ten-day measures of persistent spread deterioration and price deterioration, and relates those measures to contemporaneous valuation multiples.

The innovation is an empirical construction and its valuation association. The chapter does **not** estimate a structural funding-liquidity feedback model, observe margin calls directly, identify causal fire sales, or establish a profitable return-prediction strategy. Its “spiral” variables are functions of quotes and prices. Understanding exactly what they count is essential before treating them as measures of systemic distress.

## Sample and observable inputs

The stated sample covers S&P 500 firms from November 1982 through December 2010. Daily CRSP inputs include closing bid, closing ask, price, volume, market capitalization, ticker, and PERMCO. Datastream supplies price-to-book value (PTBV), dividend per share (DPS), total assets, return on equity, and market valuation variables. The stated mnemonic list includes PTBV, DPS, TA, ROE, MV, and P/E; a footnote identifies total assets and ROE as DWTA and DWRE.

The final panel contains 476 firms. The text describes firms with data available “throughout” the period, but does not provide dated constituent membership, entry/exit rules, or a firm list. Consequently, one cannot establish whether the sample uses historical membership or conditions on survival or later inclusion. The large differences in variable availability also make a literally balanced complete-data panel implausible.

Table 29.1 reports 2,015,260 nonmissing price and spread observations, 1,550,914 P/E observations, 848,074 PTBV observations, 1,688,046 total-asset observations, and 1,667,167 ROE observations. Valuation ratios therefore define substantially different effective samples. Mean P/E is 26.24, median 19.8; mean PTBV is 3.74, median 2.85. Mean daily quoted spread is 0.67% of the quote midpoint, with median 0.28%. These are pooled stock-day descriptions, not equal-weighted averages of firm-level sample statistics.

For firm $i$ on trading day $t$, define the quoted percentage spread

$$
S_{i,t}=100\frac{A_{i,t}-B_{i,t}}{(A_{i,t}+B_{i,t})/2},
$$

where $A$ and $B$ are closing ask and bid. Figure 29.1 describes monthly changes as $100\log(S_t/S_{t-1})$, alongside average returns, illustrating spread widening around market crises. The chart is descriptive and does not isolate funding shocks from common news or other market changes.

Several data issues require resolution before replication. Table 29.1 contains negative spreads down to −6.45% and a reported stock return minimum of −353.08%. Negative quoted spreads require a cleaning or timing explanation, and a −353.08% observation cannot be a conventional simple return on an unlevered stock. No log-return convention or correction rule is supplied. CRSP price-sign handling, corporate actions, quote quality, stale observations, and winsorization are unspecified.

The ROE row also appears internally inconsistent: visual inspection shows a minimum of −71.67, maximum of 140.13, and standard deviation of 184.21. A variable confined to that range cannot have that standard deviation. This is a source-table problem, not a reason to silently substitute a corrected number. Total assets are labeled in millions of dollars, but no reconciliation with the much larger market-value figures is supplied. Exact units and Datastream scaling need verification from the original data.

## Illiquidity score: equations 29.1–29.4

Let $y(t)$ be the calendar year of observation $t$. For each firm compute the mean quoted spread $\bar S_{i,y-1}$ and standard deviation $\sigma^S_{i,y-1}$ from the previous calendar year. A daily indicator is

$$
s_{i,t}=\begin{cases}
+1,&S_{i,t}>S_{i,t-1}\ \text{and}\ S_{i,t}>\bar S_{i,y-1}+0.5\sigma^S_{i,y-1},\\
-1,&S_{i,t}<S_{i,t-1}\ \text{and}\ S_{i,t}<\bar S_{i,y-1}-0.5\sigma^S_{i,y-1},\\
0,&\text{otherwise}.
\end{cases}
$$

Positive values signify worsening liquidity: the spread both widens today and lies unusually high relative to its prior-year level. Negative values signify a narrowing spread already below its historical benchmark. A small move from an unusually high spread need not qualify as an improvement, and an ordinary widening near the historical mean need not qualify as deterioration.

The coefficient is **one-half of a standard deviation**, not 0.5% of a standard deviation. Visual inspection of the equations confirms multiplication by 0.5; extraction artifacts can obscure this distinction.

The ten-day illiquidity variable is

$$
S^{(10)}_{i,t}=\sum_{j=0}^{9}s_{i,t-j}.
$$

It lies between −10 and +10. A value of +10 requires ten qualifying deterioration days, and −10 requires ten qualifying improvement days. Intermediate values are **net signed counts**, not the number of consecutive days in a run. For example, six positive and four negative indicators give +2, the same value as two positive indicators and eight zeros. The measure does not preserve their order within the window. A zero score can reflect cancellation and need not mean unchanged liquidity on all ten days.

The author's language about spiral “length” should therefore be read as a persistence proxy rather than an exact run-length statistic. Its sign also does not establish a funding mechanism: news-driven increases in adverse selection could produce widening spreads without forced deleveraging.

## Loss score: equations 29.5–29.8

For prices, the historical center differs from the spread center. Define the previous calendar year's high–low midpoint

$$
H_{i,y-1}=\frac{\max_{u\in y-1}P_{i,u}+\min_{u\in y-1}P_{i,u}}{2}.
$$

The source describes a positive loss indicator when today's price declines and lies at least half a standard deviation below that midpoint, and a negative indicator when price rises and lies sufficiently above it:

$$
p_{i,t}=\begin{cases}
+1,&P_{i,t}<P_{i,t-1}\ \text{and}\ P_{i,t}<H_{i,y-1}-0.5\sigma^P_{i,y-1},\\
-1,&P_{i,t}>P_{i,t-1}\ \text{and}\ P_{i,t}>H_{i,y-1}+0.5\sigma^P_{i,y-1},\\
0,&\text{otherwise},
\end{cases}
\qquad
P^{(10)}_{i,t}=\sum_{j=0}^{9}p_{i,t-j}.
$$

The notation $\sigma^P$ here makes a dimensionally coherent reconstruction explicit: it denotes a previous-year standard deviation of prices. The source reuses the earlier $\sigma_{i,av(y-1)}$ symbol without clearly redefining it after identifying it as a spread standard deviation. The exact implementation of this scale is therefore unresolved. It would be dimensionally inappropriate to subtract a percentage-spread standard deviation directly from a dollar price.

The midpoint is not the prior-year average price, although the conclusion loosely describes it that way. Corporate-action adjustment is particularly important for any historical *price-level* comparison; a split can otherwise create an artificial persistent loss signal. The chapter does not specify its adjustment policy.

The price and spread thresholds are fixed from the previous year rather than estimated from a rolling contemporaneous window. Replication needs at least one prior year of data before the first scored day, but initialization and minimum-observation requirements are absent. A half-standard-deviation criterion is a descriptive threshold; it is not a hypothesis test with a stated significance level, despite the prose's use of “statistically significant” price changes.

## Alternative construction and frequency evidence

The alternative measures drop the $0.5\sigma$ terms while retaining both the comparison with the previous day and the comparison with the prior-year benchmark. They do **not** merely count all upward spread changes or all negative returns. They retain a historical-state condition.

Table 29.2 counts **overlapping firm-day windows**, not independent spiral episodes. Selected endpoints and centers are:

| Ten-day score | Spread, sigma | Spread, alternative | Price loss, sigma | Price loss, alternative |
|---|---:|---:|---:|---:|
| −10 | 15 | 41 | 509 | 592 |
| −5 | 189,715 | 271,280 | 242,098 | 265,114 |
| 0 | 293,262 | 136,569 | 146,501 | 23,852 |
| +5 | 66,734 | 59,435 | 181,347 | 205,849 |
| +10 | 3 | 4 | 308 | 355 |

The extreme +10 spread score is very rare. The loss-score histograms in Figure 29.2 are bimodal, with many observations around positive and negative five. A zero count is not generally the most frequent outcome for every measure, and even a modal zero would not show that the market is unchanged most of the time. The ten-day windows share nine indicator observations with adjacent windows, so frequency counts should not be read as counts of independent events.

The table footnotes contain erroneous equation references and confusing language about setting the standard deviation to zero. The operational distinction is clearer in the main prose: the alternative simply omits the half-standard-deviation buffer. The chapter does not state clearly which variant is used in every subsequent regression, so that choice must remain visible in a reconstruction.

## Valuation regressions

The dependent variable is a contemporaneous multiple, either firm PTBV or firm P/E. For each outcome $V_{i,t}$ the full reported specification has the form

$$
V_{i,t}=b_0+b_1P^{(10)}_{i,t}+b_2S^{(10)}_{i,t}+b_3V^{M}_t+b_4(r^M_t-r^f_t)+b_5\log(TA_{i,t})+b_6ROE_{i,t}+b_7D_{i,t}+\varepsilon_{i,t}.
$$

The market multiple $V^M$ matches the dependent variable: S&P 500 PTBV for the PTBV regression and S&P 500 P/E for the P/E regression. Excess return is the **market** return minus the risk-free rate from the Fama–French library, not the firm's own excess return. The table captions specify the natural log of total assets in millions of dollars; the body labels that regressor simply TA.

The dividend indicator is inconsistent across descriptions. The equation discussion says one on an **ex-dividend date**, whereas the table captions and interpretation refer to whether a firm **pays a dividend**. These indicators have different meanings and frequencies. The paper supplies no code or distribution to settle the choice.

There are three pooled OLS models per outcome: the two spiral scores only; those scores plus the market multiple and market excess return; and the full set including size, ROE, and dividend indicator. No firm or date fixed effects, instrumental variables, standard-error clustering, lagged-score specification, or panel dependence correction is reported. Fundamental-data publication lags and point-in-time availability are also unspecified.

### PTBV results: Table 29.3

| Model | Loss coefficient, $t$ | Illiquidity coefficient, $t$ | Observations | $R^2$ |
|---|---|---|---:|---:|
| 5.1 | −0.034, −13.22 | −0.003, −0.77 | 848,064 | 0.0002 |
| 5.2 | −0.030, −11.67 | −0.008, −2.00 | 848,064 | 0.0010 |
| 5.3 | −0.032, −15.30 | −0.049, −15.56 | 834,231 | 0.0306 |

In the full model the other coefficients are intercept 3.18, market PTBV 0.002, market excess return 0.021, log assets −0.58, ROE 0.004, and dividend indicator −0.63. Their reported $t$-statistics are 89.21, 66.66, 2.86, −95.87, 98.12, and −27.35 respectively.

The text says both spiral coefficients are significant at 1% in all three models. The table contradicts that claim: the first illiquidity coefficient is insignificant and the second is marked only at 5%. The full-model illiquidity association is much stronger than the simpler specifications. That sensitivity, coupled with the changing sample and omitted fixed effects, deserves attention.

A one-unit increase in a score is associated with a change in the *level* of PTBV, not a percentage return. Holding other regressors fixed, a move from zero to +10 would imply −0.32 PTBV units for the loss score and −0.49 for the spread score using full-model coefficients. These are linear-model arithmetic illustrations, not causal estimates or validated extrapolations at the very rare endpoints.

### P/E results: Table 29.4

| Model | Loss coefficient, $t$ | Illiquidity coefficient, $t$ | Observations | $R^2$ |
|---|---|---|---:|---:|
| 6.1 | −0.33, −73.41 | −0.37, −54.64 | 1,550,914 | 0.008 |
| 6.2 | −0.33, −73.18 | −0.37, −54.16 | 1,550,914 | 0.008 |
| 6.3 | −0.36, −80.04 | −0.33, −48.88 | 1,525,707 | 0.060 |

Full-model controls are intercept 35.41, market P/E 0.015, market excess return 0.11, log assets −1.36, ROE −0.004, and dividend indicator −10.13. Their reported $t$-statistics are 743, 16.68, 7.17, −106.78, −29.37, and −205.36. A ten-unit score increase corresponds algebraically to −3.6 P/E units for the loss score or −3.3 for the spread score. Those are multiple points, not percent changes in price or expected return.

The regressions explain little of the pooled variation: at most 3.06% for PTBV and 6% for P/E. Large reported $t$-statistics arise in enormous repeated daily panels and cannot establish robust inference when the treatment of serial and cross-sectional dependence is unreported. Overlapping score windows and persistent valuation/fundamental variables make that omission material.

## What the evidence establishes

The chapter finds negative contemporaneous associations between adverse signed scores and valuation ratios, especially in the fully controlled models. This is consistent with a liquidity discount, but it does not identify that explanation uniquely. Price appears directly in both the loss score and the numerator of valuation ratios, creating a mechanical channel for association. Common shocks, omitted firm characteristics, and reverse causality are also possible. No direct funding or margin variable verifies a feedback spiral.

There is no estimated crisis interaction, event-level causal design, out-of-sample forecast, or portfolio backtest. Thus statements that the measures capture a stock's prospective “vulnerability” should be distinguished from the actual contemporaneous regression design. Lower current multiples are not themselves evidence of higher subsequent returns or a priced systematic spiral factor.

An exact reproduction remains blocked by constituent selection, quote and return cleaning, fundamental-data timing, price adjustment, the loss-scale definition, dividend-indicator definition, variant selection, and inference conventions. A transparent implementation can reproduce the proposed score logic while explicitly presenting those alternatives; it cannot claim to reproduce the published coefficients without resolving them.

The useful takeaway is a compact observable diagnostic: combine the direction of today's move with its position relative to a prior-year benchmark, then aggregate signed indications over ten days. This can summarize persistent deterioration. It should retain its status as a proxy, with the window arithmetic and data defects visible, rather than be treated as proof that a self-reinforcing funding spiral has been identified.
