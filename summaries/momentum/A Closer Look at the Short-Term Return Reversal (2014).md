# A Closer Look at the Short-Term Return Reversal
**Authors:** Zhi Da, Qianqiu Liu, Ernst Schaumburg
**Year:** 2014
**Journal/Venue:** Management Science 60(3), 658-674
**Source file:** `Finance/AbnormalReturnsMomentum_DaLiuSchaumburg_2014.pdf`

## Question

Both leading explanations of one-month reversal, sentiment-driven overreaction and liquidity-driven price pressure (Grossman-Miller; Campbell, Grossman, Wang), predict that only the **nonfundamental** part of last month's return should reverse. The paper strips fundamental components from past returns, shows that sorting on what remains gives a far stronger reversal, and then uses this cleaner signal to show that the two explanations act on different legs: liquidity on the long (loser) side, sentiment plus short-sale constraints on the short (winner) side.

## Decomposition

Realized return minus three "fundamental" pieces: expected return, cash-flow news, discount-rate news. Discount-rate news is assumed negligible at monthly frequency. Because prices may deviate from value, the components do not add up as in Campbell-Shiller (1988). All quantities are measured relative to industry averages (11 I/B/E/S sectors).

- **Expected return** $\mu_t$: Fama-French three-factor model, betas from rolling 60-month windows (minimum 36), premia set to sample-average factor returns. Results are insensitive to using CAPM or a five-factor model; at monthly horizon $\mu_t$ is small relative to realized returns.
- **Cash-flow news** $CF_{t+1}$ (following Da and Warachka 2009, Easton-Monahan 2005): monthly revisions of I/B/E/S consensus forecasts. Expected earnings are built with a three-stage model: A1, A2 forecasts for years 1-2, long-term growth (LTG) through year 5, linear convergence to an economy-wide steady-state growth rate over years 6-10, then a terminal value. Book value evolves by clean surplus with a 5% payout; expected log accounting returns $e_{t+j}=\log(1+X_{t+j}/B_{t+j-1})$ are discounted with $\rho=0.95$, and
$$CF_{t+1}=E_{t+1}\sum_{j\ge0}\rho^j e_{t+j+1}-E_t\sum_{j\ge0}\rho^j e_{t+j+1}$$
(Vuolteenaho 2002). Months run from one I/B/E/S consensus date (third Thursday) to the next; earnings-announcement months use the realized earnings surprise. Monthly differencing removes slow-moving analyst biases; industry demeaning removes biases common within an industry.
- **Residual return:** $\text{Residual}_{t+1}=r_{t+1}-\mu_t-CF_{t+1}$, analogous at monthly frequency to Daniel-Titman's (2006) "intangible" return.

**Sample:** January 1982 to March 2009; stocks with I/B/E/S coverage and price at least \$5. About 2,350 stocks per month, one-third of CRSP by count but about 75% by market cap; average cap about \$2.5bn, about eight analysts per stock. This is a large, liquid universe where standard reversal is weak.

## Main results (Table 2; equal-weighted decile long-short, one-month holding)

| Strategy | Raw | FF3 alpha | 5-factor alpha (+MOM, DMU) |
|---|---|---|---|
| A. Standard reversal (Jegadeesh 1990) | 0.67% (t=2.53) | 0.33% (1.37) | -0.19% (-0.85) |
| B. Within-industry raw-return reversal | 1.20% (5.87) | 0.92% (5.11) | 0.46% (2.77) |
| C. Within-industry residual reversal (benchmark) | 1.57% (9.48) | 1.34% (9.28) | 0.91% (6.02) |
| D. Residual reversal, no industry control | 1.13% | 0.84% | 0.26% (insig.) |

- The benchmark's FF3 alpha is four times the standard strategy's. Its monthly Sharpe ratio is 0.52 raw (0.53 FF3-adjusted), against 0.14 (0.08) for standard reversal.
- Industry demeaning alone does a lot (A to B): industry momentum (Moskowitz-Grinblatt) masks stock-level reversal in large stocks. Removing cash-flow news adds a further, separate gain (A to D: the 5-factor improvement of 45 bp is significant, t=4.50).
- **Portfolio anatomy (Table 3):** the extreme residual deciles are stocks whose prices moved **against** their news. Decile 1 has residual -18.1%, raw return -11.3%, and cash-flow news +5.5%. Decile 10 has residual +24.6%, raw return +16.8%, and cash-flow news -9.0%. Expected returns are almost flat across deciles (1.1-1.2%). The extremes are smaller, less covered, higher-IVOL and more Amihud-illiquid, though not penny stocks (average prices of about \$31 and \$38).
- **Costs:** turnover is about 90% per month on each leg and quoted spreads are 46 and 43 bp, giving an estimated cost of about 80 bp per month. The cost-adjusted FF3 alpha is about 0.54% per month (t=3.90). This uses quoted half-spread-type estimates only; price impact is not modeled.

## Robustness (Tables 4-5)

- Profits are concentrated in month 1: 1.57%, then 0.40% (t=2.51) in month 2, then about zero. This argues against a missing risk factor.
- Calendar-month returns: 1.74% raw, FF3 alpha 1.63%. Mid-quote returns (bid-ask bounce control): 2.11% raw, FF3 1.97%, 5-factor 1.79%.
- **Nonparametric version:** within industry, a 3x3 double sort on past return and forecast revision FREV that buys losers with upward revisions and sells winners with downward revisions earns 1.86% raw and 1.72% FF3 (t=12.24). Its correlation with the parametric strategy is 0.76, so the result does not hinge on the valuation-model assumptions.
- Ex-January: FF3 alpha 1.23%. By decade, FF3 alpha falls from 2.00% (1980s) to 1.33% (1990s) to 1.04% (2000-09), all significant; the 5-factor alpha is insignificant in the 1990s. It is significant in all 11 industries. Excluding earnings-announcement months: FF3 1.58%, so the result is not post-earnings drift.
- Stronger among small, value, illiquid (FF3 2.23% vs 0.68%), low-coverage, high-IVOL and rising-distress (EDF) stocks. The large-stock tercile still has FF3 alpha 0.73% (t=4.80).

## Long vs short leg (Tables 6-8)

Time-series regressions of each leg's FF3-adjusted excess return on lagged market-wide variables (Newey-West, 12 lags):
- **Long leg (buy residual losers):** loads positively on lagged detrended Amihud illiquidity and on S&P 500 realized volatility (a VIX proxy, as in Nagel 2012), and not on sentiment. Correlations of the long alpha with amihud and rv are 0.24 and 0.23; with IPO count and equity share they are -0.10 and -0.03. The interpretation is compensation for liquidity provision after forced selling (Shleifer-Vishny 1992; Coval-Stafford 2007). Fire sales are more common than fire purchases.
- **Short leg (sell residual winners):** loads on lagged number of IPOs and equity share in new issues (Baker-Wurgler sentiment components; turnover-type components deliberately excluded as liquidity-contaminated). Correlations of the short alpha with these are 0.43 and 0.57. This is consistent with Miller (1977): optimism plus short-sale constraints produce overpricing that corrects slowly. It parallels Stambaugh-Yu-Yuan (2012), who find sentiment effects confined to anomaly short legs.
- The pattern survives Baker-Wurgler macro controls, removal of industry controls, and holds across 14 characteristic subsamples.
- **Cross-section (Fama-MacBeth):** residual-return reversal is stronger for high-Amihud stocks **only among losers**. Among winners, significant reversal appears **only for stocks without listed options**. Optionable winners, which are easier to short, do not reverse.

## Assessment

- **Convincing:** the core empirical point is simple and robust. Past return conditioned on news matters, and the price-news disagreement signal (parametric or nonparametric) roughly quadruples reversal alpha in a large-cap, analyst-covered universe where the plain signal is dead. The month-1 concentration and the leg-specific loadings give a coherent economic story, and the optionability test on winners is a clean way to identify a short-sale-constraint channel.
- **Fragile or open:** (i) the 5-factor alpha declines over time (insignificant in the 1990s) and the sample ends in 2009; post-2009 performance, with lower spreads and heavier liquidity-provision competition, is untested. (ii) The cost estimate uses quoted spreads and equal weights at about 90% turnover, with no impact costs. For a capacity-constrained book, the illiquid and high-IVOL concentration of the profits matters. (iii) The leg attribution rests on aggregate time-series loadings with modest correlations (0.2-0.6) and a handful of proxies; liquidity and sentiment are acknowledged to be intertwined. (iv) The cash-flow proxy depends on analyst coverage and on valuation-model choices (payout, $\rho$, steady-state growth), though the double-sort check mitigates this. (v) Decile construction is equal-weighted within industry; value-weighted results are not the headline.
- **Practical use:** for a short-horizon equity signal, (1) residualize past-month returns against industry and against contemporaneous fundamental news (revisions or earnings surprises), not just against factors; (2) expect the long leg to pay more after illiquidity and volatility spikes and the short leg after issuance-heavy, high-sentiment periods, which suggests conditional leg weighting; (3) winners with listed options are poor short candidates for this signal.
- See also: "Decomposing Short-Term Return Reversal (2011)", the same authors' earlier paper.
